#!/usr/bin/env python3
"""Supreme Court oral argument transcription pipeline.

Downloads the argument audio and official transcript from supremecourt.gov,
runs faster-whisper for word timings, aligns the ASR words to the official
wording, and writes words.json / lines.json / laughs.md / README.md.

Usage:
    python3 transcribe.py 14-275 2014 horne-raisins
    python3 transcribe.py 14-275 2014 horne-raisins --model small.en

The year is the Court's term year as used in supremecourt.gov URLs
(the October 2014 term covers arguments heard in spring 2015).

Requires: ffmpeg, pdftotext (poppler-utils), pip install faster-whisper.
"""
import argparse
import datetime
import difflib
import json
import re
import subprocess
import sys
import time
import urllib.request
from urllib.parse import urljoin
from pathlib import Path

import numpy as np

SCOTUS = "https://www.supremecourt.gov"
UA = {"User-Agent": "Mozilla/5.0 (transcription pipeline)"}
MAX_MP3_BYTES = 90 * 1024 * 1024
LAUGH = "(Laughter.)"

SPEAKER_RE = re.compile(
    r"^((?:CHIEF )?JUST(?:ICE)? [A-Z'\-]+|(?:MR|MS|MRS|GENERAL)\.? [A-Za-z'\-]+(?: [A-Z'\-]{2,})?|GENERAL [A-Za-z'\-]+|"
    r"THE CLERK|THE MARSHAL|QUESTION)\s*:\s*(.*)$"
)
SECTION_RE = re.compile(r"^(ORAL ARGUMENT OF|REBUTTAL ARGUMENT OF|ON BEHALF OF|P R O C E E D I N G S)")
TIME_RE = re.compile(r"^[(\[]\d{1,2}:\d{2} [ap]\.m\.[)\]]$")  # "(10:04 a.m.)", "[10:04 a.m.]" before ~2006


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def fetch(url, dest=None):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    if dest:
        Path(dest).write_bytes(data)
    return data


# --------------------------------------------------------------------------- sources

def transcript_link(html, case):
    """First link to this case's argument transcript PDF: 14-275_2b8e.pdf, 11-626.pdf,
    11-796-1j43.pdf, or an older /pdfs/transcripts/ path; failing that, a PDF link whose text
    is the docket number."""
    pat = r"""['"]([^'"]*(?:argument_transcripts|pdfs/transcripts)/[^'"]*/%s(?:[_-][^'"/]*)?\.pdf)['"]""" % re.escape(case)
    m = re.search(pat, html)
    if m:
        return m.group(1)
    m = re.search(r"""<a\s+href=['"]([^'"]+\.pdf)['"][^>]*>\s*%s\b""" % re.escape(case), html, re.I)
    return m.group(1) if m else None


def find_sources(case, year, pdf_url=None, mp3_url=None):
    """The MP3 comes from the case's audio page. The transcript PDF comes from the same page,
    or failing that from the term's transcript listing, where the PDF name can carry a suffix
    that can't be guessed (14-275_2b8e.pdf)."""
    page_url = f"{SCOTUS}/oral_arguments/audio/{year}/{case}"
    list_url = f"{SCOTUS}/oral_arguments/argument_transcript/{year}"
    if not (pdf_url and mp3_url):
        html = fetch(page_url).decode("utf-8", "replace")
        if not mp3_url:
            m = re.search(r"""['"]([^'"]*/mp3files/[^'"]*\.mp3)['"]""", html)
            if not m:
                sys.exit(f"No MP3 link on {page_url}; pass --mp3-url (oyez.org has copies)")
            mp3_url = urljoin(page_url, m.group(1))
        if not pdf_url:
            link = transcript_link(html, case)
            base = page_url
            if not link:
                log(f"No transcript link on {page_url}, trying {list_url}")
                link, base = transcript_link(fetch(list_url).decode("utf-8", "replace"), case), list_url
            if not link:
                sys.exit(f"No transcript link for {case} on {page_url} or {list_url}; pass --pdf-url")
            pdf_url = urljoin(base, link)
    return page_url, urljoin(SCOTUS + "/", mp3_url), urljoin(SCOTUS + "/", pdf_url)


def prepare_audio(src, dest):
    """Mono 64 kbps MP3, metadata stripped."""
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(src),
                    "-ac", "1", "-b:a", "64k", "-map_metadata", "-1", str(dest)], check=True)
    size = dest.stat().st_size
    if size >= MAX_MP3_BYTES:
        sys.exit(f"{dest} is {size/1e6:.1f} MB, over the 90 MB limit")
    return size


def audio_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(out.stdout.strip())


# --------------------------------------------------------------------------- ASR

def run_asr(audio, model_name, cache, checkpoint_every=20):
    """Whisper over the whole file, with word timestamps. Progress is saved to <cache>.partial
    every few segments, so a run that dies (a container restart, say) resumes from the last saved
    segment instead of starting over; Whisper loses its running context only at that seam."""
    if cache.exists():
        data = json.loads(cache.read_text())
        if data.get("model") == model_name:
            log(f"Using cached ASR {cache}")
            return data
    partial = cache.with_name(cache.name + ".partial")
    words, offset, prev_elapsed, resumed = [], 0.0, 0.0, []
    if partial.exists():
        p = json.loads(partial.read_text())
        if p.get("model") == model_name:
            words, offset, prev_elapsed = p["words"], p["upto"], p.get("elapsed_s", 0.0)
            resumed = p.get("resumed_at", []) + [offset]
            log(f"Resuming ASR from {offset:.1f} s ({len(words)} words saved)")
    from faster_whisper import WhisperModel
    log(f"Loading {model_name}")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    duration = audio_duration(audio)
    if offset > 0:
        pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{offset:.3f}", "-i", str(audio), "-ac", "1",
                              "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
        source = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    else:
        source = str(audio)
    segments, info = model.transcribe(source, language="en", word_timestamps=True,
                                      vad_filter=False, beam_size=5)
    t0 = time.time()
    for k, seg in enumerate(segments, 1):
        for w in seg.words:
            words.append({"w": w.word.strip(), "s": round(offset + w.start, 3), "e": round(offset + w.end, 3),
                          "p": round(w.probability, 3)})
        el = prev_elapsed + time.time() - t0
        print(f"\r  {offset + seg.end:7.1f}/{duration:.0f}s audio, {el:6.0f}s elapsed", end="", flush=True)
        if k % checkpoint_every == 0:
            partial.write_text(json.dumps({"model": model_name, "upto": round(offset + seg.end, 3),
                                           "elapsed_s": round(el, 1), "resumed_at": resumed, "words": words}))
    print()
    data = {"model": model_name, "duration": duration,
            "elapsed_s": round(prev_elapsed + time.time() - t0, 1), "words": words}
    if resumed:
        data["resumed_at"] = resumed
    cache.write_text(json.dumps(data))
    if partial.exists():
        partial.unlink()
    return data


# --------------------------------------------------------------------------- official transcript

BOILERPLATE_RE = re.compile(r"^(Official( - Subject to Final Review)?|.*\bReporting (Company|Corporation)\b.*"
                            r"|.*www\.\S+\.com.*|.*\bFOR[- ]DEPO\b.*)$", re.I)


def clean_pdf_lines(text):
    """pdftotext -layout output -> list of body text lines, boilerplate removed. Page headers and
    footers are caught by pattern and, for reporters not seen before, by repetition: a line that
    appears on at least half the pages is page furniture, not speech."""
    text = text.replace("\u00ad", "-")  # the PDFs use soft hyphens for every hyphen/dash
    pages = max(1, text.count("\f"))
    # whitespace collapsed, so a footer spaced differently on each page still counts as repeated
    raw_lines = [re.sub(r"\s+", " ", r.replace("\f", "")).strip() for r in text.splitlines()]
    counts = {}
    for r in raw_lines:
        if r and not r.isdigit():
            counts[r] = counts.get(r, 0) + 1
    repeated = {r for r, c in counts.items() if c >= max(5, pages // 2)}
    out = []
    for line in raw_lines:
        if not line or line in repeated or BOILERPLATE_RE.match(line):
            continue
        line = re.sub(r"^\d{1,2}(\s+|$)", "", line)  # transcript line number / page number
        line = re.sub(r"\s+", " ", line).strip()
        if line:
            out.append(line)
    return out


def parse_transcript(pdf):
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True,
                          text=True, check=True).stdout
    lines = clean_pdf_lines(text)
    start = next(i for i, l in enumerate(lines) if l.startswith("P R O C E E D I N G S"))
    end = next(i for i, l in enumerate(lines) if re.match(r"^[(\[]?Whereupon", l))
    turns = []
    section = ""  # current argument heading, e.g. "ORAL ARGUMENT OF ... ON BEHALF OF THE PETITIONER"
    in_heading = False  # headings can run over several all-caps lines ("FOR UNITED STATES, AS ...")
    for line in lines[start + 1:end]:
        if SECTION_RE.match(line) or TIME_RE.match(line):
            if re.match(r"^(ORAL|REBUTTAL) ARGUMENT OF", line):
                section = line
            elif SECTION_RE.match(line) and not line.startswith("P R O"):
                section += " " + line
            in_heading = True
            continue
        m = SPEAKER_RE.match(line)
        if in_heading and not m and line == line.upper():
            section += " " + line
            continue
        in_heading = False
        if m:
            turns.append({"speaker": re.sub(r"^(CHIEF )?JUST ", r"\1JUSTICE ", m.group(1).upper()),
                          "text": m.group(2), "section": section})
        elif turns:
            turns[-1]["text"] += " " + line
    for t in turns:
        t["text"] = re.sub(r"\s+", " ", t["text"]).strip()
    return turns


def tokenize_turn(text):
    """Split turn text into official words. Punctuation-only tokens ("--") are glued to a
    neighbouring word; "(Laughter.)" is kept as one marker token."""
    # "(Laughter.)", "(Laughter).", "(A little laughter.)", "[Laughter.]" (before ~2006): one marker
    text = re.sub(r"[(\[]\s*[^()\[\]]*?\blaughter\b[^()\[\]]*[)\]]\.?", f" {LAUGH} ", text, flags=re.I)
    toks = []
    pending_prefix = ""
    for tok in text.split():
        if tok != LAUGH and not re.search(r"\w", tok):
            if toks and toks[-1] != LAUGH:
                toks[-1] += " " + tok
            else:
                pending_prefix += tok + " "
            continue
        if pending_prefix and tok != LAUGH:
            tok, pending_prefix = pending_prefix + tok, ""
        toks.append(tok)
    return toks


def norm(w):
    return re.sub(r"[^\w]", "", w.lower().replace("’", "'")).replace("_", "")


# --------------------------------------------------------------------------- alignment

STRETCH_S = 1.5  # an ASR word this long next to squeezed missed words has swallowed their audio
MIN_ROOM_S = 0.06  # per missed word; less than this counts as squeezed


def align(official, asr, duration):
    """official: list of dicts with "w"; asr: list of dicts with w/s/e.
    Returns per-official-word (s, e), the number of official words matched to ASR words,
    and the number of matched words whose span was shared with squeezed missed words."""
    a = [norm(w["w"]) for w in official]
    b = [norm(w["w"]) for w in asr]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    times = [None] * len(a)
    is_match = [False] * len(a)
    missed_runs = []
    matched = 0

    def spread(i1, i2, s, e):
        e = max(e, s)
        step = (e - s) / (i2 - i1)
        for k, i in enumerate(range(i1, i2)):
            times[i] = (s + k * step, s + (k + 1) * step)

    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                times[i1 + k] = (asr[j1 + k]["s"], asr[j1 + k]["e"])
                is_match[i1 + k] = True
            matched += i2 - i1
        elif op == "replace":
            spread(i1, i2, asr[j1]["s"], asr[j2 - 1]["e"])
        elif op == "insert":
            pass  # ASR words with no official counterpart: dropped
        elif op == "delete":
            # official words the ASR missed: spread across the gap between neighbours
            s = asr[j1 - 1]["e"] if j1 > 0 else 0.0
            e = asr[j1]["s"] if j1 < len(asr) else duration
            spread(i1, i2, s, e)
            missed_runs.append((i1, i2))

    # Whisper sometimes drops a stretch of speech and stretches the neighbouring word over it.
    # When missed words have no room and a neighbour is stretched, they share its span.
    shared = 0
    for i1, i2 in missed_runs:
        s, e = times[i1][0], times[i2 - 1][1]
        if e - s >= MIN_ROOM_S * (i2 - i1):
            continue
        nxt, prv = i2, i1 - 1
        if nxt < len(a) and is_match[nxt] and times[nxt][1] - times[nxt][0] > STRETCH_S:
            spread(i1, nxt + 1, s, times[nxt][1])
            shared += 1
        elif prv >= 0 and is_match[prv] and times[prv][1] - times[prv][0] > STRETCH_S:
            spread(prv, i2, times[prv][0], e)
            shared += 1
    return times, matched, shared


def build_words(turns, asr_words, duration, voiced, audio, model_name, window_cache):
    official = []  # every token incl. laugh markers, with turn index
    for ti, t in enumerate(turns):
        for tok in tokenize_turn(t["text"]):
            official.append({"w": tok, "speaker": t["speaker"], "turn": ti})
    spoken = [o for o in official if o["w"] != LAUGH]
    times, matched, shared = align(spoken, asr_words, duration)
    for o, (s, e) in zip(spoken, times):
        o["s"], o["e"] = round(float(s), 3), round(float(e), 3)
    trimmed = trim_stretched(spoken, voiced)
    rewindowed = rewindow_long_words(spoken, audio, model_name, voiced, window_cache)
    # enforce monotonic order (spread words can only touch the matched words around them)
    last, clamped = 0.0, 0
    for o in spoken:
        clamped += int(o["s"] < last)
        o["s"] = max(o["s"], last)
        o["e"] = max(o["e"], o["s"])
        last = o["s"]
    # laugh markers: from end of the previous word to start of the next
    for i, o in enumerate(official):
        if o["w"] == LAUGH:
            prev = next((official[k] for k in range(i - 1, -1, -1) if official[k]["w"] != LAUGH), None)
            nxt = next((official[k] for k in range(i + 1, len(official)) if official[k]["w"] != LAUGH), None)
            o["s"] = prev["e"] if prev else 0.0
            o["e"] = max(nxt["s"], o["s"]) if nxt else round(duration, 3)
    return official, matched, len(spoken), shared, clamped, trimmed, rewindowed


# --------------------------------------------------------------------------- laughs

HOP = 0.05  # seconds per loudness frame


def loudness(audio):
    """Per-frame loudness in dBFS, the room floor (20th percentile), a loud mask (12 dB above
    that floor, for laugh bursts) and a voiced mask (12 dB above the silence level, the 5th
    percentile, for trimming words; quiet speakers fall under the loud mask)."""
    sr = 16000
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(audio), "-ac", "1", "-ar", str(sr),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    h = int(sr * HOP)
    nf = len(x) // h
    db = 20 * np.log10(np.sqrt((x[: nf * h].reshape(nf, h) ** 2).mean(axis=1) + 1e-12))
    floor = float(np.percentile(db, 20))
    silence = float(np.percentile(db, 5))
    return db, floor, db > floor + 12, db > silence + 12, silence


def find_quotes(official, quotes, mp3, out_dir, window=10.0):
    """Each quote's exact place in the argument (official words, matched ignoring case,
    punctuation and hyphens), a `window`-second stretch centred on it, everything said in that
    stretch, and a clip of it saved as out_dir/quote_N.mp3."""
    spoken = [o for o in official if o["w"] != LAUGH]
    key = lambda t: re.sub(r"[^a-z0-9]", "", t.lower())
    keys = [key(o["w"]) for o in spoken]
    rows = []
    for n, q in enumerate(quotes, 1):
        target = key(q)
        hit = None
        for i in range(len(spoken)):
            acc, j = "", i
            while j < len(spoken) and len(acc) < len(target):
                acc += keys[j]
                j += 1
            if acc == target or (acc.startswith(target) and j - i > 1):
                hit = (i, j)
                break
        exact = hit is not None
        if not hit:  # closest stretch, for wording that differs slightly
            n_words = max(1, len(q.split()))
            best = max(range(len(spoken)), key=lambda i: difflib.SequenceMatcher(
                None, "".join(keys[i:i + n_words]), target).ratio())
            hit = (best, best + n_words)
        i, j = hit
        s0, s1 = spoken[i]["s"], spoken[j - 1]["e"]
        mid = (s0 + s1) / 2
        w0 = max(0.0, mid - window / 2)
        w1 = w0 + window
        out_dir.mkdir(parents=True, exist_ok=True)
        clip = out_dir / f"quote_{n}.mp3"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{w0:.3f}", "-t", f"{window:.3f}", "-i", str(mp3),
                        "-ac", "1", "-b:a", "64k", str(clip)], check=True)
        around, cur = [], None
        for o in official:
            if o["s"] >= w1 or o["e"] <= w0:
                continue
            if cur and cur[1] == o["speaker"]:
                cur[2].append(o["w"])
            else:
                cur = [o["s"], o["speaker"], [o["w"]]]
                around.append(cur)
        rows.append({"quote": q, "exact": exact, "speaker": spoken[i]["speaker"], "s": s0, "e": s1,
                     "text": " ".join(o["w"] for o in spoken[i:j]), "w0": w0, "w1": w1,
                     "clip": f"audio/quotes/{clip.name}",
                     "around": [(a, spk, " ".join(ws)) for a, spk, ws in around]})
    return rows


def longest_questions(official, turns, n=10):
    """The n longest turns by a justice, timed from first word to last in the audio: each is
    uninterrupted by definition, since the transcript starts a new turn when anyone else speaks."""
    by_turn = {}
    for o in official:
        by_turn.setdefault(o["turn"], []).append(o)
    rows = []
    for ti, ws in by_turn.items():
        spk = turns[ti]["speaker"]
        spoken = [o for o in ws if o["w"] != LAUGH]
        if "JUSTICE" not in spk or not spoken:
            continue
        rows.append({"speaker": spk, "s": spoken[0]["s"], "e": spoken[-1]["e"],
                     "dur": round(spoken[-1]["e"] - spoken[0]["s"], 2), "words": len(spoken),
                     "text": " ".join(o["w"] for o in ws)})
    rows.sort(key=lambda r: -r["dur"])
    return rows[:n]


def measure_laughs(official, db, silence, hop=HOP, edge=0.05, words_before=30):
    """Each official (Laughter.) marker in the audio: its time (end of the word before), the
    words before it, and the room inside the pause that follows, up to the next transcribed
    word: how long, how many seconds are 12 dB or more over the silence floor, and the mean
    (energy) and peak loudness in dB over that floor."""
    rows = []
    for i, o in enumerate(official):
        if o["w"] != LAUGH:
            continue
        before = [p["w"] for p in official[:i] if p["w"] != LAUGH][-words_before:]
        nxt = next((p for p in official[i + 1:] if p["w"] != LAUGH), None)
        t0, t1 = o["s"], (nxt["s"] if nxt else o["e"])
        i0, i1 = int(np.ceil((t0 + edge) / hop)), min(int((t1 - edge) / hop), len(db))
        seg = db[i0:i1] if i1 > i0 else db[0:0]
        if len(seg):
            mean = round(float(10 * np.log10(np.mean(10 ** (seg / 10))) - silence), 1)
            peak = round(float(seg.max() - silence), 1)
            loud = round(float((seg > silence + 12).sum() * hop), 2)
        else:
            mean = peak = None
            loud = 0.0
        pause = round(t1 - t0, 2)
        if pause < 0.3:
            size = "under speech"  # the next word starts at once; any laugh is under the voice
        elif loud >= 1.0 and (mean or 0) >= 20:
            size = "big"
        elif loud >= 0.4:
            size = "medium"
        else:
            size = "small"
        rows.append({"t": t0, "next": t1, "speaker": o["speaker"], "before": " ".join(before),
                     "pause": pause, "loud_s": loud, "mean_over": mean, "peak_over": peak, "size": size})
    return rows


def rank_pauses(official, db, silence, min_gap=0.4, edge=0.1, hop=HOP):
    """Every gap of min_gap s or more between consecutive official words, with the room's
    loudness inside it (energy mean and peak, edge s trimmed off each side against word bleed)
    in dB over the silence level. Loudest first."""
    spoken = [o for o in official if o["w"] != LAUGH]
    pauses = []
    for k in range(1, len(spoken)):
        g0, g1 = spoken[k - 1]["e"], spoken[k]["s"]
        if g1 - g0 < min_gap:
            continue
        i0, i1 = int(np.ceil((g0 + edge) / hop)), min(int((g1 - edge) / hop), len(db))
        if i1 <= i0:
            continue
        seg = db[i0:i1]
        mean = 10 * np.log10(np.mean(10 ** (seg / 10)))
        pauses.append({"s": g0, "e": g1, "k": k, "over": round(float(mean - silence), 1),
                       "peak_over": round(float(seg.max() - silence), 1),
                       "loud_s": round(float((seg > silence + 12).sum() * hop), 2)})
    pauses.sort(key=lambda p: p["over"], reverse=True)
    return pauses, [o["w"] for o in spoken]


def voiced_runs(voiced, s, e, bridge=0.25):
    """(start, end) of voiced stretches between s and e, merging gaps shorter than bridge."""
    i0, i1 = int(np.ceil(s / HOP)), min(int(e / HOP), len(voiced))
    runs = []
    for i in range(i0, i1):
        if not voiced[i]:
            continue
        t0, t1 = i * HOP, (i + 1) * HOP
        if runs and t0 - runs[-1][1] < bridge:
            runs[-1][1] = t1
        else:
            runs.append([t0, t1])
    return runs


def trim_stretched(spoken, voiced, max_len=STRETCH_S, edge=0.3):
    """Whisper sometimes stretches a word over the pause after (or before) it. For a word longer
    than max_len, drop voiced blips lying wholly within `edge` s of either end (bleed from the
    neighbouring words); if what's left sits inside the span, trim the word to it. Citations
    ("989.166(c)") are left alone: they really do take seconds to say. Returns the count trimmed."""
    trimmed = 0
    for o in spoken:
        s, e = o["s"], o["e"]
        if e - s <= max_len or is_citation(o["w"]):
            continue
        all_runs = voiced_runs(voiced, s, e)
        runs = [r for r in all_runs if not (r[1] <= s + edge or r[0] >= e - edge)]
        if not runs:
            # only blips at the edges (or none): if a second or more of silence follows the
            # word's start, the word is the short, quiet sound right there, not bleed, and the
            # rest of the span is a pause; keep at least 0.2 s from the start
            head = [r for r in all_runs if r[1] <= s + edge]
            rest = [r for r in all_runs if r[0] > s + edge]
            gap_start = head[-1][1] if head else s
            gap_end = rest[0][0] if rest else e
            if gap_end - gap_start >= 1.0:
                ne = max(gap_start, s + 0.2)
                if ne < e:
                    o["e"] = round(float(ne), 3)
                    trimmed += 1
            continue
        # voiced audio split by a second or more of silence: Whisper's word starts are the reliable
        # edge (it stretches words into the pause after them), so keep the first cluster if it
        # starts near the word's start, else the last if it ends near the word's end
        clusters = [[runs[0]]]
        for r in runs[1:]:
            if r[0] - clusters[-1][-1][1] >= 1.0:
                clusters.append([r])
            else:
                clusters[-1].append(r)
        if len(clusters) > 1:
            if abs(clusters[0][0][0] - s) <= edge:
                runs = clusters[0]
            elif abs(clusters[-1][-1][1] - e) <= 0.15:
                runs = clusters[-1]
            else:
                continue
        # move an edge only by a clear margin, not by frame rounding
        ns = runs[0][0] if runs[0][0] - s >= 0.1 else s
        ne = runs[-1][1] if e - runs[-1][1] >= 0.1 else e
        if ne - ns >= 0.1 and (ns > s or ne < e):
            o["s"], o["e"] = round(float(ns), 3), round(float(ne), 3)
            trimmed += 1
    return trimmed


def is_citation(w):
    return len(re.findall(r"\d", w)) >= 3


class WindowASR:
    """Whisper on a short stretch of the recording, heard without the rest of it. Results are
    cached by window in a JSON file so re-runs don't re-transcribe."""

    def __init__(self, audio, model_name, cache):
        self.audio, self.model_name, self.cache = audio, model_name, cache
        self.store = json.loads(cache.read_text()) if cache.exists() else {}
        self.model = None

    def get(self, ws, we):
        key = f"{self.model_name}:{ws:.3f}-{we:.3f}"
        if key not in self.store:
            if self.model is None:
                from faster_whisper import WhisperModel
                log(f"Re-transcribing short windows with {self.model_name}")
                self.model = WhisperModel(self.model_name, device="cpu", compute_type="int8")
            pcm = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ws:.3f}", "-t", f"{we - ws:.3f}",
                                  "-i", str(self.audio), "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                                 capture_output=True, check=True).stdout
            x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
            segs, _ = self.model.transcribe(x, language="en", word_timestamps=True, vad_filter=False,
                                            beam_size=5)
            self.store[key] = [{"w": w.word.strip(), "s": round(ws + float(w.start), 3),
                                "e": round(ws + float(w.end), 3)} for seg in segs for w in seg.words]
            self.cache.write_text(json.dumps(self.store))
        return self.store[key]


def rewindow_long_words(spoken, audio, model_name, voiced, cache, limit=3.0, pad=3.0):
    """For words still longer than `limit` s, re-transcribe the audio around them (pad s either
    side) and re-align that stretch of official words to the fresh ASR. Heard without an hour of
    context, Whisper often picks up the cross-talk it skipped the first time. New times are kept
    only if they fit between the unchanged neighbours and bring the word under the limit.
    Window ASR is cached in `cache`. Returns the number of long words fixed."""
    long_idx = [i for i, o in enumerate(spoken) if o["e"] - o["s"] > limit and not is_citation(o["w"])]
    if not long_idx:
        return 0
    wasr, fixed = WindowASR(audio, model_name, cache), 0
    for i in long_idx:
        o = spoken[i]
        if o["e"] - o["s"] <= limit:  # fixed by an earlier window
            continue
        ws, we = max(0.0, o["s"] - pad), o["e"] + pad
        win = wasr.get(ws, we)
        # official words wholly inside the window, bounded by untouched neighbours
        k0 = next(k for k in range(i, -1, -1) if k == 0 or spoken[k - 1]["s"] < ws)
        k1 = next(k for k in range(i, len(spoken)) if k == len(spoken) - 1 or spoken[k + 1]["e"] > we)
        lo = spoken[k0 - 1]["e"] if k0 > 0 else 0.0
        hi = spoken[k1 + 1]["s"] if k1 + 1 < len(spoken) else we
        win = [w for w in win if w["s"] >= lo - 0.05 and w["e"] <= hi + 0.05]
        if not win:
            continue
        times, _, _ = align(spoken[k0:k1 + 1], win, hi)
        new = [(min(max(a, lo), hi), min(max(b, lo), hi)) for a, b in times]
        ok = all(new[k][0] >= new[k - 1][0] for k in range(1, len(new)))
        ni = i - k0
        if ok and new[ni][1] - new[ni][0] <= limit:
            for k, (a, b) in enumerate(new):
                spoken[k0 + k]["s"], spoken[k0 + k]["e"] = round(float(a), 3), round(float(b), 3)
            fixed += 1
    trim_stretched(spoken, voiced)
    return fixed


def loud_bursts(asr_words, db, floor, loud, n=10, max_len=2.0, hop=HOP):
    """Loud stretches inside real pauses between ASR words (gaps of 0.4 s or more, with 0.1 s
    trimmed off each edge so word onsets and tails don't count). Returns the n loudest that
    last 0.3 s to max_len and the ones that run max_len or longer."""
    nf = len(db)
    edges = [0.0] + [t for w in asr_words for t in (w["s"], w["e"])] + [nf * hop]
    short, long_ = [], []
    for g0, g1 in zip(edges[0::2], edges[1::2]):
        if g1 - g0 < 0.4:
            continue
        i, end = int(np.ceil((g0 + 0.1) / hop)), int((g1 - 0.1) / hop)
        while i < end:
            if not loud[i]:
                i += 1
                continue
            j = i
            while j < end and loud[j]:
                j += 1
            dur = (j - i) * hop
            burst = {"s": round(i * hop, 3), "e": round(j * hop, 3), "dur": round(dur, 2),
                     "peak_db": round(float(db[i:j].max()), 1),
                     "mean_db": round(float(db[i:j].mean()), 1)}
            if dur >= max_len:
                long_.append(burst)
            elif dur >= 0.3:
                short.append(burst)
            i = j
    short.sort(key=lambda b: b["mean_db"], reverse=True)
    return short[:n], long_


def fmt_ts(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h)}:{int(m):02d}:{s:06.3f}"


# --------------------------------------------------------------------------- checks

def sanity_checks(words, match_rate):
    order_bad = [i for i in range(1, len(words)) if words[i]["s"] < words[i - 1]["s"]]
    inverted = [i for i, w in enumerate(words) if w["e"] < w["s"]]
    long_bad, long_numbers = [], []
    for i, w in enumerate(words):
        if w["w"] == LAUGH:
            continue
        before_laugh = i + 1 < len(words) and words[i + 1]["w"] == LAUGH
        if w["e"] - w["s"] > 3.0 and not before_laugh:
            # a citation like "989.166(c)" is one official word but takes seconds to say
            (long_numbers if is_citation(w["w"]) else long_bad).append(i)
    short = sum(1 for w in words if w["w"] != LAUGH and w["e"] - w["s"] < 0.02)
    return {
        "time_order": {"ok": not order_bad and not inverted,
                       "detail": f"{len(order_bad)} words start before the previous word; "
                                 f"{len(inverted)} words end before they start"},
        "max_duration": {"ok": not long_bad,
                         "detail": f"{len(long_bad)} words longer than 3 s outside laugh positions",
                         "examples": [(words[i]["w"], words[i]["s"], words[i]["e"]) for i in long_bad[:10]],
                         "numbers": [(words[i]["w"], words[i]["s"], words[i]["e"]) for i in long_numbers]},
        "short_words": short,
        "match_rate": {"ok": match_rate > 85.0, "detail": f"{match_rate:.2f}% (threshold 85%)"},
    }


# --------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("case", help="docket number, e.g. 14-275")
    ap.add_argument("year", help="term year used in supremecourt.gov URLs, e.g. 2014")
    ap.add_argument("project", help="output folder name under projects/")
    ap.add_argument("--model", default="medium.en", help="faster-whisper model (default medium.en)")
    ap.add_argument("--pdf-url", help="override the transcript PDF URL")
    ap.add_argument("--mp3-url", help="override the audio URL (e.g. an oyez.org MP3)")
    ap.add_argument("--mentions", help="comma-separated terms to list in a Key mentions table, "
                    "e.g. \"Girl Scout(s),salesman/salesmen,front door\"")
    ap.add_argument("--quotes", help="'|'-separated lines to locate in the argument, each with a "
                    "10-second clip around it")
    ap.add_argument("--long-questions", type=int, default=0, metavar="N",
                    help="list the N longest uninterrupted turns by a justice")
    ap.add_argument("--opinion", action="store_true",
                    help="also fetch and transcribe the opinion announcement from oyez.org (Whisper only)")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent / "projects" / args.project
    audio_dir, work = root / "audio", root / "work"
    audio_dir.mkdir(parents=True, exist_ok=True)
    work.mkdir(exist_ok=True)

    page_url, mp3_url, pdf_url = find_sources(args.case, args.year, args.pdf_url, args.mp3_url)
    log(f"audio {mp3_url}\n           transcript {pdf_url}")

    mp3 = audio_dir / "argument.mp3"
    if not mp3.exists():
        orig = work / "original.mp3"
        log("Downloading audio")
        fetch(mp3_url, orig)
        prepare_audio(orig, mp3)
        orig.unlink()
    pdf = work / "transcript.pdf"
    if not pdf.exists():
        log("Downloading transcript")
        fetch(pdf_url, pdf)
    duration = audio_duration(mp3)

    asr = run_asr(mp3, args.model, work / f"asr_{args.model}.json")
    asr_words = asr["words"]
    log(f"ASR: {len(asr_words)} words")

    turns = parse_transcript(pdf)
    log(f"Official transcript: {len(turns)} speaker turns")
    db, floor, loud, voiced, silence = loudness(mp3)
    official, matched, n_spoken, shared, clamped, trimmed, rewindowed = build_words(
        turns, asr_words, duration, voiced, mp3, args.model, work / f"asr_windows_{args.model}.json")
    match_rate = 100.0 * matched / n_spoken
    log(f"Matched {matched}/{n_spoken} official words ({match_rate:.2f}%)")

    words_out = [{"w": o["w"], "s": o["s"], "e": o["e"], "speaker": o["speaker"]} for o in official]
    (audio_dir / "words.json").write_text(json.dumps(words_out, indent=1, ensure_ascii=False) + "\n")

    lines = []
    for ti, t in enumerate(turns):
        tw = [o for o in official if o["turn"] == ti and o["w"] != LAUGH] or \
             [o for o in official if o["turn"] == ti]
        if not tw:
            continue
        lines.append({"speaker": t["speaker"], "s": tw[0]["s"], "e": tw[-1]["e"],
                      "text": " ".join(o["w"] for o in official if o["turn"] == ti)})
    (root / "lines.json").write_text(json.dumps(lines, indent=1, ensure_ascii=False) + "\n")

    # laughs.md
    bursts, long_bursts = loud_bursts(asr_words, db, floor, loud)
    floor = round(floor, 1)
    laugh_times = [o["s"] for o in official if o["w"] == LAUGH]
    near = lambda b: "yes" if any(t - 1 <= b["s"] <= t + 5 for t in laugh_times) else ""
    overlap = lambda b: sum(1 for o in official if o["w"] != LAUGH and o["s"] < b["e"] and o["e"] > b["s"])
    md = [f"# Laughter: {args.case}", "",
          "## (Laughter.) in the official transcript", "",
          "Time is the end of the word before the marker. The 25 official words before it follow.", ""]
    if not laugh_times:
        md += ["None: this transcript has no (Laughter.) markers.", ""]
    for i, o in enumerate(official):
        if o["w"] != LAUGH:
            continue
        before = [p for p in official[:i] if p["w"] != LAUGH][-25:]
        md += [f"### {fmt_ts(o['s'])} ({o['s']:.3f} s), during {o['speaker']}'s turn", "",
               "> " + " ".join(p["w"] for p in before) + " **(Laughter.)**", ""]
    md += ["## Loudest short bursts outside speech (likely laughs)", "",
           f"Runs of 50 ms frames at least 12 dB above the room floor ({floor} dBFS), inside pauses "
           "of 0.4 s or more between ASR words (0.1 s trimmed off each side), lasting 0.3 to 2 s, "
           "ranked by mean loudness. \"Near marker\" means it starts between 1 s before and 5 s "
           "after a (Laughter.) time above. \"Official words\" counts official words whose aligned "
           "time overlaps the burst: these are words the ASR missed, so a burst with a count is more "
           "likely cross-talk than a laugh. Laughs in court often overlap speech, which the ASR "
           "then stretches its words over, so this list misses those.", "",
           "| # | start | end | start (s) | end (s) | length (s) | mean dBFS | peak dBFS | near marker | official words |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for k, b in enumerate(bursts, 1):
        md.append(f"| {k} | {fmt_ts(b['s'])} | {fmt_ts(b['e'])} | {b['s']:.3f} | {b['e']:.3f} | "
                  f"{b['dur']:.2f} | {b['mean_db']} | {b['peak_db']} | {near(b)} | {overlap(b)} |")
    if long_bursts:
        md += ["", "## Loud stretches of 2 s or more outside speech", "",
               "Same test, but too long for the list above. Listed because a long laugh falls here.", "",
               "| start | end | start (s) | end (s) | length (s) | mean dBFS | near marker | official words |",
               "|---|---|---|---|---|---|---|---|"]
        for b in sorted(long_bursts, key=lambda b: b["s"]):
            md.append(f"| {fmt_ts(b['s'])} | {fmt_ts(b['e'])} | {b['s']:.3f} | {b['e']:.3f} | "
                      f"{b['dur']:.2f} | {b['mean_db']} | {near(b)} | {overlap(b)} |")
    pauses, spoken_words = rank_pauses(official, db, silence)
    laugh_rows = measure_laughs(official, db, silence)
    long_qs = longest_questions(official, turns, args.long_questions) if args.long_questions else None
    quotes = [q.strip() for q in args.quotes.split("|") if q.strip()] if args.quotes else []
    quote_rows = find_quotes(official, quotes, mp3, audio_dir / "quotes") if quotes else None
    md += ["", "## Every pause of 0.4 s or more, loudest room first", "",
           f"Gaps of 0.4 s or more between consecutive official words, ranked by how loud the room "
           f"is inside the gap: energy mean (and peak) of 50 ms frames, 0.1 s trimmed off each side, "
           f"in dB over the silence level ({silence:.1f} dBFS, the quietest 5% of the recording). "
           "A laugh shows up as a loud pause; a quiet one is a real silence. \"Loud s\" is how many "
           "seconds of the pause are 12 dB or more over the floor: a short loud pause is often "
           "cross-talk the ASR missed, a long loud one is more likely laughter. Laughs that overlap "
           "speech leave no pause and can't appear here. \"Marker\" shows a transcript (Laughter.) "
           "inside the pause. The words are the 20 official words before the pause.", "",
           "| rank | start | end | start (s) | end (s) | length (s) | dB over floor | peak over floor | loud s | marker | 20 words before |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r, pz in enumerate(pauses, 1):
        before = " ".join(spoken_words[max(0, pz["k"] - 20):pz["k"]]).replace("|", "\\|")
        marker = "(Laughter.)" if any(pz["s"] - 0.01 <= t <= pz["e"] for t in laugh_times) else ""
        md.append(f"| {r} | {fmt_ts(pz['s'])} | {fmt_ts(pz['e'])} | {pz['s']:.3f} | {pz['e']:.3f} | "
                  f"{pz['e'] - pz['s']:.2f} | {pz['over']} | {pz['peak_over']} | {pz['loud_s']:.2f} | {marker} | {before} |")
    (root / "laughs.md").write_text("\n".join(md) + "\n")

    checks = sanity_checks(words_out, match_rate)
    for k, v in checks.items():
        if not isinstance(v, dict):
            continue
        log(f"check {k}: {'PASS' if v['ok'] else 'FAIL'} {v['detail']}")
    opening_start, opening = petitioner_opening(official, turns)
    opinion = process_opinion(args.case, args.year, root, work, args.model) if args.opinion else None
    if opinion and opinion.get("found"):
        log(f"Opinion announcement: {opinion['words']} words, {fmt_ts(opinion['duration'])}")
    elif opinion:
        log(f"No opinion announcement on {opinion['page_url']} {opinion.get('error', '')}")
    terms = [t.strip() for t in args.mentions.split(",") if t.strip()] if args.mentions else []
    mentions = key_mentions(official, terms) if terms else None
    stats = {
        "terms": terms, "mentions": mentions, "laugh_rows": laugh_rows, "long_qs": long_qs, "long_n": args.long_questions, "quote_rows": quote_rows, "quotes": quotes, "silence_db": round(silence, 1),
        "opening_start": opening_start, "opening": opening, "opinion": opinion,
        "case": args.case, "year": args.year, "page_url": page_url, "mp3_url": mp3_url,
        "pdf_url": pdf_url, "model": args.model, "duration": duration,
        "asr_elapsed_s": asr.get("elapsed_s"), "asr_words": len(asr_words),
        "official_words": n_spoken, "matched": matched, "shared": shared, "clamped": clamped, "trimmed": trimmed, "rewindowed": rewindowed, "match_rate": match_rate,
        "turns": len(lines), "laugh_markers": sum(o["w"] == LAUGH for o in official),
        "mp3_bytes": mp3.stat().st_size, "pauses": len(pauses), "checks": checks,
        "generated": datetime.date.today().isoformat(),
    }
    (work / "stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    write_readme(root, stats)
    log(f"Wrote {root}")
    if not all(v["ok"] for v in checks.values() if isinstance(v, dict)):
        sys.exit("Sanity checks failed, see README.md")


ABBREV = {"mr.", "mrs.", "ms.", "dr.", "v.", "st.", "no.", "u.s.", "e.g.", "i.e.", "vs.", "jr.", "sr."}


def term_regex(term):
    """'Girl Scout(s)' -> regex. '(x)' is optional, '/' separates alternatives, spaces and hyphens
    match either, and normal endings (s, es, 's, ed, ing) are allowed. Whole words only, so
    'Franky' doesn't match 'frankly'."""
    alts = []
    for alt in term.split("/"):
        alt = alt.strip().lower()
        parts = re.split(r"(\([^)]*\))", alt)
        rx = ""
        for part in parts:
            if part.startswith("("):
                rx += f"(?:{re.escape(part[1:-1])})?"
            else:
                rx += re.sub(r"\\[ -]|\\-|[ -]", "[ -]", re.escape(part))
        alts.append(rx)
    return re.compile(r"(?<![a-z])(?:" + "|".join(alts) + r")(?:s|es|'s|s'|ed|ing)?(?![a-z])", re.I)


def key_mentions(official, terms):
    """Every sentence in the argument that mentions one of `terms`: (time of the matching word,
    speaker, term, full sentence). One row per term per sentence."""
    sentences, cur = [], []
    for o in official:
        if o["w"] == LAUGH:
            continue
        if cur and cur[-1]["turn"] != o["turn"]:
            sentences.append(cur)
            cur = []
        cur.append(o)
        last = re.sub(r"[\"')\]]+$", "", o["w"].lower())
        if re.search(r"[.?!]$", last) and last not in ABBREV:
            sentences.append(cur)
            cur = []
    if cur:
        sentences.append(cur)
    rows = []
    for sent in sentences:
        text = " ".join(o["w"] for o in sent)
        for term in terms:
            rx = term_regex(term)
            # the word where a match starts; two-word terms ("front door") span words
            hits = []
            for k, o in enumerate(sent):
                m = rx.search(" ".join(x["w"] for x in sent[k:k + 3]))
                if m and m.start() < len(o["w"]):
                    hits.append(o)
            if hits:
                rows.append((hits[0]["s"], sent[0]["speaker"], term, text, len(rx.findall(text))))
    rows.sort(key=lambda r: r[0])
    return rows


OYEZ_API = "https://api.oyez.org"


def oyez_speaker(name):
    """Oyez speaker name -> transcript style label ("JUSTICE GINSBURG", "CHIEF JUSTICE ROBERTS")."""
    if not name:
        return "UNKNOWN"
    last = re.sub(r",? (Jr|Sr|II|III)\.?$", "", name).split()[-1].upper()
    return f"CHIEF JUSTICE {last}" if last in ("ROBERTS", "REHNQUIST", "BURGER", "WARREN") else f"JUSTICE {last}"


def chief_justice_on(title):
    """Chief Justice on the date in an Oyez title like 'Opinion Announcement - June 12, 2014'."""
    m = re.search(r"(\d{4})\s*$", title or "")
    year = int(m.group(1)) if m else 2100
    return "CHIEF JUSTICE ROBERTS" if year >= 2006 else "CHIEF JUSTICE REHNQUIST"


def process_opinion(case, year, root, work, model_name):
    """Opinion announcement from Oyez: audio/opinion.mp3, opinion_words.json, opinion_lines.json.
    Wording and times are Whisper's alone (there is no official transcript); speaker names come
    from the turn boundaries in Oyez's own transcript. Returns facts for the README."""
    case_url = f"{OYEZ_API}/cases/{year}/{case}"
    info = {"case_url": case_url, "page_url": f"https://www.oyez.org/cases/{year}/{case}", "found": False}
    try:
        cdata = json.loads(fetch(case_url))
    except Exception as exc:  # network or API change: report rather than fail the whole run
        info["error"] = str(exc)
        return info
    ann = cdata.get("opinion_announcement") or []
    info["count"] = len(ann)
    if not ann:
        return info
    media = json.loads(fetch(ann[0]["href"]))
    mp3_url = next((m["href"] for m in media.get("media_file") or [] if m.get("mime") == "audio/mpeg"), None)
    if not mp3_url:
        info["error"] = "announcement listed but no MP3 file"
        return info
    info.update(found=True, title=ann[0].get("title"), media_url=ann[0]["href"], mp3_url=mp3_url)
    mp3 = root / "audio" / "opinion.mp3"
    if not mp3.exists():
        log(f"Downloading opinion announcement {mp3_url}")
        fetch(mp3_url, mp3)  # kept as published: re-encoding a 32 kbps file gains nothing
    info["duration"] = audio_duration(mp3)
    info["mp3_bytes"] = mp3.stat().st_size

    asr = run_asr(mp3, model_name, work / f"asr_opinion_{model_name}.json")
    info["asr_elapsed_s"] = asr.get("elapsed_s")
    words = [{"w": w["w"], "s": w["s"], "e": w["e"]} for w in asr["words"]]
    _, _, _, voiced, _ = loudness(mp3)
    info["trimmed"] = trim_stretched(words, voiced)
    info["rewindowed"] = rewindow_long_words(words, mp3, model_name, voiced,
                                             work / f"asr_windows_opinion_{model_name}.json")

    turns, oyez_words = [], []
    for sec in (media.get("transcript") or {}).get("sections") or []:
        for t in sec.get("turns") or []:
            text = " ".join(b["text"] for b in t.get("text_blocks") or [])
            name = (t.get("speaker") or {}).get("name")
            turns.append({"speaker": oyez_speaker(name) if name else None, "text": text,
                          "s": float(t["start"]), "e": float(t["stop"])})
            oyez_words += text.split()
    # Oyez sometimes lists no speaker names. The text says who: "Justice Kennedy has our opinion"
    # is the Chief Justice introducing the case, and the next turn is that justice
    inferred = 0
    for k, t in enumerate(turns):
        m = re.match(r"\s*Justice (\w+) has (?:our|the) (?:opinion|announcement)", t["text"])
        if m and t["speaker"] is None:
            t["speaker"] = chief_justice_on(ann[0].get("title", ""))
            inferred += 1
            if k + 1 < len(turns) and turns[k + 1]["speaker"] is None:
                turns[k + 1]["speaker"] = f"JUSTICE {m.group(1).upper()}"
                inferred += 1
    for t in turns:
        if t["speaker"] is None:
            t["speaker"] = "UNKNOWN"
    info["speaker_turns"] = len(turns)
    info["speakers_inferred"] = inferred

    # Whisper can invent or mangle text. Words only Whisper has, and runs of 3+ words where
    # Whisper and Oyez's transcript disagree, are re-transcribed on their own (6 s either side). If Whisper added words Oyez lacks
    # and the re-run doesn't hear them, they weren't said: drop them. If the words differ and the
    # re-run agrees with Oyez, use the re-run's words and times for that stretch.
    wasr = WindowASR(mp3, model_name, work / f"asr_windows_opinion_{model_name}.json")
    dropped, redone = [], []
    if oyez_words:
        a, b = [norm(w["w"]) for w in words], [norm(w) for w in oyez_words]
        drop, subs = set(), {}

        def contains(needle, hay):
            needle = [x for x in needle if x]
            if not needle:
                return True
            m = difflib.SequenceMatcher(None, needle, hay, autojunk=False).find_longest_match(
                0, len(needle), 0, len(hay))
            return m.size >= 0.6 * len(needle), m

        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            # words only Whisper has: any length; words Whisper and Oyez disagree on: 3 or more
            if not (op == "delete" or (op == "replace" and i2 - i1 >= 3)):
                continue
            # spoken "quote ... close quote": Oyez leaves it out and Whisper may write it as a
            # quotation mark, so neither source can confirm it; never drop it
            if "quote" in " ".join(a[i1:i2]) and all(x in ("quote", "close", "end", "unquote")
                                                      for x in a[i1:i2] if x):
                continue
            raw = wasr.get(max(0.0, words[i1]["s"] - 6), words[i2 - 1]["e"] + 6)
            win = [norm(w["w"]) for w in raw]
            if contains(a[i1:i2], win)[0]:
                continue  # the re-run hears Whisper's words too: keep them
            text = " ".join(w["w"] for w in words[i1:i2])
            oy = [x for x in b[j1:j2] if x]
            if op == "delete" or not oy:
                drop.update(range(i1, i2))
                dropped.append((words[i1]["s"], words[i2 - 1]["e"], text))
                continue
            ok, m = contains(oy, win)
            if ok and m.size == len(oy):
                lo = words[i1 - 1]["e"] if i1 > 0 else 0.0
                hi = words[i2]["s"] if i2 < len(words) else words[i2 - 1]["e"]
                new = [dict(w) for w in raw[m.b:m.b + m.size]]
                if not all(lo - 0.05 <= w["s"] <= w["e"] <= hi + 0.05 for w in new):
                    step = (words[i2 - 1]["e"] - words[i1]["s"]) / len(new)
                    for k, w in enumerate(new):
                        w["s"] = round(words[i1]["s"] + k * step, 3)
                        w["e"] = round(words[i1]["s"] + (k + 1) * step, 3)
                subs[i1] = (i2, new)
                redone.append((words[i1]["s"], text, " ".join(w["w"] for w in new)))
        out, k = [], 0
        while k < len(words):
            if k in subs:
                out += subs[k][1]
                k = subs[k][0]
                continue
            if k not in drop:
                w = words[k]
                # invented words sat on top of real speech: a squeezed word right after them
                # gets their time back
                if k > 0 and k - 1 in drop and w["e"] - w["s"] < 0.05:
                    w["s"] = max(next(words[j]["s"] for j in range(k - 1, -1, -1)
                                      if j - 1 < 0 or j - 1 not in drop), out[-1]["e"] if out else 0.0)
                out.append(w)
            k += 1
        words = out
        a = [norm(w["w"]) for w in words]
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        agree = sum(bl.size for bl in sm.get_matching_blocks())
        info["oyez_agree"] = (agree, len(a), len(b))
        def same(x, y):
            # spelling and formatting only: spacing, hyphens, punctuation, case, "v."/"versus",
            # and "quote ... close quote", which justices say aloud and Oyez leaves out
            f = lambda t: re.sub(r"\b(close )?quote\b", "", re.sub(r"\bversus\b", "v", t.lower()))
            g = lambda t: re.sub(r"[^a-z0-9]", "", f(t)).replace("judgement", "judgment")
            return g(x) == g(y)

        info["diffs"] = [(words[i1]["s"] if i1 < len(words) else words[-1]["e"], wt, ot)
                         for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"
                         for wt, ot in [(" ".join(w["w"] for w in words[i1:i2]), " ".join(oyez_words[j1:j2]))]
                         if not same(wt, ot)]
    info["dropped"], info["redone"] = dropped, redone

    # Speakers: each Oyez turn boundary is snapped to the longest pause between words within
    # 1.5 s of it, then every word takes the speaker of the turn it falls in.
    cuts = []
    for t in turns[1:]:
        # prefer a pause after a sentence end ("v." doesn't count), then the longest pause
        ends = lambda w: (bool(re.search(r"[.?!][\"')]*$", w)) and
                          re.sub(r"[\"')]+$", "", w.lower()) not in ABBREV)
        gaps = [(ends(words[k - 1]["w"]), words[k]["s"] - words[k - 1]["e"], k) for k in range(1, len(words))
                if abs((words[k - 1]["e"] + words[k]["s"]) / 2 - t["s"]) <= 1.5]
        cuts.append(max(gaps)[2] if gaps else
                    next((k for k, w in enumerate(words) if w["s"] >= t["s"]), len(words)))
    for k, w in enumerate(words):
        w["speaker"] = turns[sum(1 for c in cuts if k >= c)]["speaker"] if turns else "UNKNOWN"
    (root / "opinion_words.json").write_text(json.dumps(words, indent=1, ensure_ascii=False) + "\n")

    lines = []
    for w in words:
        if lines and lines[-1]["speaker"] == w["speaker"]:
            lines[-1]["e"] = w["e"]
            # Whisper splits "13-7451" into "13" "-7451": rejoin in the text, keep both timed words
            lines[-1]["text"] += ("" if re.match(r"^(-|[,.]\d)", w["w"]) else " ") + w["w"]
        else:
            lines.append({"speaker": w["speaker"], "s": w["s"], "e": w["e"], "text": w["w"]})
    (root / "opinion_lines.json").write_text(json.dumps(lines, indent=1, ensure_ascii=False) + "\n")

    info["words"] = len(words)
    # first 3 minutes as plain text, one paragraph per speaker turn
    opening = []
    if words:
        t0 = words[0]["s"]
        for w in words:
            if w["s"] >= t0 + 180:
                break
            if opening and opening[-1][1] == w["speaker"]:
                opening[-1][2] += ("" if re.match(r"^(-|[,.]\d)", w["w"]) else " ") + w["w"]
            else:
                opening.append([w["s"], w["speaker"], w["w"]])
    info["opening"] = opening
    info["lines"] = [(l["speaker"], l["s"], l["e"], len(l["text"].split())) for l in lines]
    order_bad = sum(1 for i in range(1, len(words)) if words[i]["s"] < words[i - 1]["s"])
    long_bad = [(w["w"], w["s"], w["e"]) for w in words if w["e"] - w["s"] > 3.0 and not is_citation(w["w"])]
    info["checks"] = {"order_bad": order_bad, "long_bad": long_bad}
    return info


def petitioner_opening(official, turns, seconds=180.0):
    """Everything said in the first `seconds` of the petitioner's opening argument, as
    (start time, speaker, text) per turn. Interruptions from the bench are included."""
    first = next((i for i, t in enumerate(turns)
                  if re.search(r"ON BEHALF OF (THE )?PETITIONERS?\b", t.get("section", ""))
                  and t["section"].startswith("ORAL ARGUMENT")), None)
    if first is None:
        return None, []
    words = [o for o in official if o["turn"] >= first]
    start = next(o["s"] for o in words if o["w"] != LAUGH)
    out = []
    for o in words:
        if o["s"] >= start + seconds:
            break
        if out and out[-1][1] == o["speaker"] and out[-1][3] == o["turn"]:
            out[-1][2].append(o["w"])
        else:
            out.append([o["s"], o["speaker"], [o["w"]], o["turn"]])
    return start, [(s0, spk, " ".join(ws)) for s0, spk, ws, _ in out]


def write_readme(root, st):
    c = st["checks"]
    mark = lambda ok: "PASS" if ok else "FAIL"
    ex = c["max_duration"]["examples"]
    long_note = ""
    if ex:
        long_note = ("\n  Offending words: " + ", ".join(f"\"{w}\" {s:.3f}-{e:.3f}" for w, s, e in ex)
                     + ". Left as the ASR timed them: none of the timing rules below could place them "
                     "with confidence, and a re-transcription of the window didn't help. This is "
                     "usually overlapping speech, where two people talk at once and the ASR hears "
                     "only one; the transcript's word order then can't match the audio. Check by ear.")
    nums = c["max_duration"]["numbers"]
    if nums:
        long_note += ("\n  Not counted: " + ", ".join(f"`{w}` {s:.3f}-{e:.3f} ({e - s:.2f} s)" for w, s, e in nums)
                      + ". A citation is one official word but is spoken as several; its time is the real "
                      "time taken to say it.")
    text = f"""# {root.name}: Supreme Court No. {st['case']}

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: {st['page_url'] if "supremecourt.gov" in st['mp3_url'] else "none on supremecourt.gov for this term"}
- Audio: {st['mp3_url']}{"" if "supremecourt.gov" in st['mp3_url'] else chr(10) + "  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own."}
- Official transcript: {st['pdf_url']}

## Numbers

- ASR model: faster-whisper `{st['model']}`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: {st['asr_elapsed_s'] / 60:.0f} min on 4 CPU cores
- Audio length: {fmt_ts(st['duration'])} ({st['duration']:.3f} s)
- `audio/argument.mp3`: mono, 64 kbps, {st['mp3_bytes']/1e6:.1f} MB
- Official words: {st['official_words']} (plus {st['laugh_markers']} `(Laughter.)` markers), in {st['turns']} speaker turns
- ASR words: {st['asr_words']}
- Official words matched to an ASR word: {st['matched']} of {st['official_words']} (**{st['match_rate']:.2f}%**)

## Sanity checks

- {mark(c['time_order']['ok'])}: words in time order. {c['time_order']['detail']}.
  ({st['clamped']} spread words had to be nudged forward to keep order before this check ran.)
- {mark(c['max_duration']['ok'])}: no word longer than 3 s except before a laugh. {c['max_duration']['detail']}.{long_note}
- {mark(c['match_rate']['ok'])}: match rate over 85%. {c['match_rate']['detail']}.

{c['short_words']} words are shorter than 20 ms. These are official words the ASR didn't produce,
mostly repeats, false starts and cross-talk ("the -- the --", "I -- I think"), squeezed into the
small gap between the ASR words either side. Their order is right; their exact times are not.

## Files

- `audio/argument.mp3`: the argument audio (and `audio/quotes/`, 10-second clips, when quotes are asked for).
- `audio/words.json`: every official word in order, `{{"w", "s", "e", "speaker"}}`, times in seconds.
  `(Laughter.)` markers are included as entries of their own, running from the end of the word
  before to the start of the word after.
- `lines.json`: one entry per speaker turn, `{{"speaker", "s", "e", "text"}}`.
- `laughs.md`: each `(Laughter.)` with its time and the 25 words before it, the 10 loudest
  sub-2-second bursts outside speech, and every pause of 0.4 s or more ranked by how loud the
  room is, with the 20 words before it.
- `work/`: the raw ASR output (`asr_*.json`), the transcript PDF and run stats, kept so the
  alignment can be re-run without re-transcribing.

## How times are assigned

Official and ASR words are lowercased, stripped of punctuation and aligned with
`difflib.SequenceMatcher` (autojunk off). Matched words keep their ASR start and end.
Where the official transcript has different words from the ASR, the official words are spread
evenly across the time of the ASR words they replace; official words the ASR missed entirely are
spread across the gap between the neighbouring ASR words. If that gap is too small (under 60 ms
a word) and the neighbouring ASR word is stretched past 1.5 s, the ASR has dropped speech and
spread the neighbour over it, so the missed words share that neighbour's span instead. This
happened {st['shared']} times. ASR words with no official counterpart
are dropped. Punctuation-only tokens such as `--` are attached to the neighbouring word.

Whisper also stretches single words over the pause after or before them. Any word still longer
than 1.5 s is checked against the audio: voiced stretches (12 dB over the silence level, the
quietest 5% of the recording) inside
its span are found, blips within 0.3 s of either end are treated as bleed from the neighbouring
words, and the word is trimmed to what remains. If nothing remains it is left alone, as are
citations such as `989.166(c)`. When the voiced audio falls in clusters split by a second or
more of silence, the word keeps the first cluster if it starts within 0.3 s of the word's start
(Whisper's starts are reliable; it stretches words into the pause after them), else the last
cluster if it ends at the word's end, and is left alone otherwise. When the only sound in the span
is right at its start (or there's none), followed by a second or more of silence, the word is cut
to that sound, at least 0.2 s from its start. This trimmed {st['trimmed']} words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed {st['rewindowed']}
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py {st['case']} {st['year']} {root.name} --model {st['model']}{' --opinion' if st.get('opinion') else ''}{(' --mentions ' + chr(34) + ','.join(st['terms']) + chr(34)) if st.get('terms') else ''}{(' --quotes ' + chr(34) + '|'.join(st['quotes']) + chr(34)) if st.get('quotes') else ''}{(' --long-questions ' + str(st['long_n'])) if st.get('long_n') else ''}
"""
    text += readme_extras(st)
    (root / "README.md").write_text(text)


def readme_extras(st):
    out = ""
    if st.get("long_qs"):
        out += (f"\n## The {len(st['long_qs'])} longest uninterrupted questions from a justice\n\n"
                "Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from "
                "its first word to its last. Longest first; official wording.\n")
        for k, r in enumerate(st["long_qs"], 1):
            out += (f"\n### {k}. {r['speaker']}, {fmt_ts(r['s'])} to {fmt_ts(r['e'])} "
                    f"({r['dur']:.1f} s, {r['words']} words)\n\n> {r['text']}\n")
    if st.get("quote_rows"):
        out += ("\n## Quotes\n\nEach line's exact place in the argument (official wording; matched ignoring "
                "case, punctuation and hyphens), and the 10 seconds of audio centred on it: the window's "
                "times, a clip of it, and everything said in it.\n")
        for k, r in enumerate(st["quote_rows"], 1):
            note = "" if r["exact"] else " (closest match; the wording differs)"
            out += (f"\n### {k}. \"{r['quote']}\"\n\n"
                    f"- Said by {r['speaker']}, {fmt_ts(r['s'])} to {fmt_ts(r['e'])} "
                    f"({r['s']:.3f} to {r['e']:.3f} s){note}: \"{r['text']}\"\n"
                    f"- 10-second window: {fmt_ts(r['w0'])} to {fmt_ts(r['w1'])} ({r['w0']:.3f} to "
                    f"{r['w1']:.3f} s), clip [`{r['clip']}`]({r['clip']})\n\n")
            out += "\n".join(f"> [{fmt_ts(a)}] {spk}: {txt}" for a, spk, txt in r["around"]) + "\n"
    if st.get("laugh_rows"):
        rows = st["laugh_rows"]
        out += (f"\n## The official laughs, measured in the audio\n\nEach `(Laughter.)` in the transcript, "
                "at the end of the word before it, with the 30 words before. The room is measured in the "
                "pause that follows, up to the next transcribed word: its length, how many seconds are "
                f"12 dB or more over the silence floor ({st['silence_db']} dBFS, the quietest 5% of the "
                "recording), and the mean and peak loudness over that floor. \"Big\" is at least 1 s "
                "loud at a mean of 20 dB or more; \"medium\" at least 0.4 s loud. \"Under speech\" "
                "means the next word starts within 0.3 s, so any laughter is under someone's voice and "
                "can't be measured this way: listen to those.\n\n"
                "| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |\n"
                "|---|---|---|---|---|---|---|---|---|\n")
        out += "\n".join(
            f"| {k} | {fmt_ts(r['t'])} | {r['t']:.3f} | {r['size']} | {r['pause']:.2f} | {r['loud_s']:.2f} | "
            f"{r['mean_over'] if r['mean_over'] is not None else '-'} | "
            f"{r['peak_over'] if r['peak_over'] is not None else '-'} | {r['before'].replace('|', '/')} |"
            for k, r in enumerate(rows, 1)) + "\n"
    if st.get("terms"):
        rows = st["mentions"] or []
        out += ("\n## Key mentions\n\nEvery sentence in the argument that mentions one of these terms, "
                "official wording, with the time of the word and the speaker. Terms match whole words "
                "with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence "
                "that mentions two terms appears once for each.\n\n| term | sentences | times said |\n|---|---|---|\n")
        for term in st["terms"]:
            tr = [r for r in rows if r[2] == term]
            out += f"| {term} | {len(tr)} | {sum(r[4] for r in tr)} |\n"
        if rows:
            out += "\n| time | time (s) | speaker | term | sentence |\n|---|---|---|---|---|\n"
            out += "\n".join(f"| {fmt_ts(t0)} | {t0:.3f} | {spk} | {term} | {txt.replace('|', '/')} |"
                              for t0, spk, term, txt, _ in rows) + "\n"
    if st.get("opening"):
        out += ("\n## Petitioner's opening, first 3 minutes\n\n"
                f"Everything said from {fmt_ts(st['opening_start'])} to "
                f"{fmt_ts(st['opening_start'] + 180)}, official wording, with each turn's start time. "
                "Interruptions from the bench are included.\n\n")
        out += "\n\n".join(f"[{fmt_ts(s0)}] {spk}: {txt}" for s0, spk, txt in st["opening"]) + "\n"
    op = st.get("opinion")
    if op is None:
        return out
    out += "\n## Opinion announcement\n\n"
    if not op.get("found"):
        why = f" ({op['error']})" if op.get("error") else ""
        return out + (f"No opinion announcement recording found on {op['page_url']}{why}. "
                      "Nothing was transcribed.\n")
    ck = op["checks"]
    ag = op.get("oyez_agree")
    agree_txt = (f"{ag[0]} of Whisper's {ag[1]} words ({100 * ag[0] / ag[1]:.1f}%; Oyez has {ag[2]})"
                 if ag else "nothing (Oyez has no transcript for this recording)")
    long_txt = (", ".join(f"\"{w}\" {a:.3f}-{b:.3f}" for w, a, b in ck["long_bad"])
                if ck["long_bad"] else "none")
    out += f"""The justice reading the decision from the bench, {op['title']}.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: {op['page_url']}
- Audio: {op['mp3_url']} (saved unchanged as `audio/opinion.mp3`: {op['mp3_bytes']/1e6:.1f} MB)
- Length: {fmt_ts(op['duration'])} ({op['duration']:.3f} s)
- Words: {op['words']}, transcribed by faster-whisper `{st['model']}` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript ({op['speaker_turns']} turn{'s' if op['speaker_turns'] != 1 else ''}), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.{(chr(10) + "  Oyez lists no names for " + str(op['speakers_inferred']) + " of these turns, so they come from the text: a turn that opens " + chr(34) + "Justice X has our opinion" + chr(34) + " is the Chief Justice introducing the case, and the next turn is Justice X.") if op.get('speakers_inferred') else ''}
- Word times: Whisper's, with the same stretched-word trimming as the argument ({op['trimmed']}
  trimmed, {op['rewindowed']} re-transcribed).
- Checks: {ck['order_bad']} words out of time order; words longer than 3 s: {long_txt}.
- Cross-check: Oyez's unofficial transcript agrees with {agree_txt}.

Files: `opinion_words.json` (`{{"w", "s", "e", "speaker"}}`) and `opinion_lines.json`
(`{{"speaker", "s", "e", "text"}}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
""" + "\n".join(f"| {spk} | {fmt_ts(a)} | {fmt_ts(b)} | {n} |" for spk, a, b, n in op["lines"]) + "\n"
    if op.get("opening"):
        t0 = op["opening"][0][0]
        out += (f"\n### First 3 minutes, as plain text\n\nWhisper's wording, {fmt_ts(t0)} to "
                f"{fmt_ts(t0 + 180)}, with each speaker's start time.\n\n")
        out += "\n\n".join(f"[{fmt_ts(a)}] {spk}: {txt}" for a, spk, txt in op["opening"]) + "\n"
    out += "\n### Words Whisper invented\n\n"
    if op.get("dropped"):
        out += ("Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's "
                "transcript disagree, were re-transcribed on their own, with 6 s either side. These "
                "Whisper words aren't in Oyez and weren't heard again, so they were dropped from the "
                "files:\n\n")
        out += "\n".join(f"- {fmt_ts(a)}-{fmt_ts(b)}: \"{txt}\"" for a, b, txt in op["dropped"]) + "\n"
    else:
        out += "None found.\n"
    if op.get("redone"):
        out += ("\nWhere Whisper's words differed from Oyez's and the re-run agreed with Oyez, the "
                "re-run's words and times replace the first pass:\n\n")
        out += "\n".join(f"- {fmt_ts(a)}: \"{old}\" became \"{new}\"" for a, old, new in op["redone"]) + "\n"
    if op.get("diffs"):
        out += ("\n### Where Whisper and Oyez disagree\n\n"
                "Whisper's wording is what's in the files. Check these by ear; Oyez is not "
                "always right either (\"--\" there often marks a repeat Oyez left out). "
                "Spelling and formatting differences (\"video games\"/\"videogames\", hyphens, "
                "spoken \"quote\" and \"close quote\") are not listed.\n\n"
                "| time | Whisper | Oyez |\n|---|---|---|\n")
        out += "\n".join(f"| {fmt_ts(t0)} | {wt.replace('|', '/') or '(nothing)'} | {ot.replace('|', '/') or '(nothing)'} |"
                          for t0, wt, ot in op["diffs"]) + "\n"
    return out


if __name__ == "__main__":
    main()
