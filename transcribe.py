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
from pathlib import Path

import numpy as np

SCOTUS = "https://www.supremecourt.gov"
UA = {"User-Agent": "Mozilla/5.0 (transcription pipeline)"}
MAX_MP3_BYTES = 90 * 1024 * 1024
LAUGH = "(Laughter.)"

SPEAKER_RE = re.compile(
    r"^((?:CHIEF )?JUSTICE [A-Z'\-]+|(?:MR|MS|MRS|GENERAL)\.? [A-Za-z'\-]+|GENERAL [A-Za-z'\-]+|"
    r"THE CLERK|THE MARSHAL|QUESTION)\s*:\s*(.*)$"
)
SECTION_RE = re.compile(r"^(ORAL ARGUMENT OF|REBUTTAL ARGUMENT OF|ON BEHALF OF|P R O C E E D I N G S)")
TIME_RE = re.compile(r"^\(\d{1,2}:\d{2} [ap]\.m\.\)$")


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

def find_sources(case, year, pdf_url=None, mp3_url=None):
    page_url = f"{SCOTUS}/oral_arguments/audio/{year}/{case}"
    if not (pdf_url and mp3_url):
        html = fetch(page_url).decode("utf-8", "replace")
        if not mp3_url:
            m = re.search(r"""['"]([^'"]*/mp3files/[^'"]*\.mp3)['"]""", html)
            if not m:
                sys.exit(f"No MP3 link on {page_url}; pass --mp3-url (oyez.org has copies)")
            mp3_url = m.group(1)
        if not pdf_url:
            m = re.search(r"""['"]([^'"]*argument_transcripts/[^'"]*\.pdf)['"]""", html)
            if not m:
                sys.exit(f"No transcript link on {page_url}; pass --pdf-url")
            pdf_url = m.group(1)
    if mp3_url.startswith("/"):
        mp3_url = SCOTUS + mp3_url
    if pdf_url.startswith("/"):
        pdf_url = SCOTUS + pdf_url
    return page_url, mp3_url, pdf_url


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

def run_asr(audio, model_name, cache):
    if cache.exists():
        data = json.loads(cache.read_text())
        if data.get("model") == model_name:
            log(f"Using cached ASR {cache}")
            return data
    from faster_whisper import WhisperModel
    log(f"Loading {model_name}")
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    segments, info = model.transcribe(str(audio), language="en", word_timestamps=True,
                                      vad_filter=False, beam_size=5)
    words, t0 = [], time.time()
    for seg in segments:
        for w in seg.words:
            words.append({"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3),
                          "p": round(w.probability, 3)})
        el = time.time() - t0
        print(f"\r  {seg.end:7.1f}/{info.duration:.0f}s audio, {el:6.0f}s elapsed", end="", flush=True)
    print()
    data = {"model": model_name, "duration": info.duration,
            "elapsed_s": round(time.time() - t0, 1), "words": words}
    cache.write_text(json.dumps(data))
    return data


# --------------------------------------------------------------------------- official transcript

def clean_pdf_lines(text):
    """pdftotext -layout output -> list of body text lines, boilerplate removed."""
    text = text.replace("­", "-")  # the PDFs use soft hyphens for every hyphen/dash
    out = []
    for raw in text.splitlines():
        line = raw.replace("\f", "").strip()
        if not line or line in ("Official", "Alderson Reporting Company"):
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
    end = next(i for i, l in enumerate(lines) if l.startswith("(Whereupon"))
    turns = []
    for line in lines[start + 1:end]:
        if SECTION_RE.match(line) or TIME_RE.match(line):
            continue
        m = SPEAKER_RE.match(line)
        if m:
            turns.append({"speaker": m.group(1).upper(), "text": m.group(2)})
        elif turns:
            turns[-1]["text"] += " " + line
    for t in turns:
        t["text"] = re.sub(r"\s+", " ", t["text"]).strip()
    return turns


def tokenize_turn(text):
    """Split turn text into official words. Punctuation-only tokens ("--") are glued to a
    neighbouring word; "(Laughter.)" is kept as one marker token."""
    text = text.replace(LAUGH, f" {LAUGH} ")
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


def build_words(turns, asr_words, duration):
    official = []  # every token incl. laugh markers, with turn index
    for ti, t in enumerate(turns):
        for tok in tokenize_turn(t["text"]):
            official.append({"w": tok, "speaker": t["speaker"], "turn": ti})
    spoken = [o for o in official if o["w"] != LAUGH]
    times, matched, shared = align(spoken, asr_words, duration)
    for o, (s, e) in zip(spoken, times):
        o["s"], o["e"] = round(s, 3), round(e, 3)
    # enforce monotonic order (spread words can only touch the matched words around them)
    last, clamped = 0.0, 0
    for o in spoken:
        clamped += o["s"] < last
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
    return official, matched, len(spoken), shared, clamped


# --------------------------------------------------------------------------- laughs

def loud_bursts(audio, asr_words, n=10, max_len=2.0, hop=0.05):
    """Loud stretches inside real pauses between ASR words (gaps of 0.4 s or more, with 0.1 s
    trimmed off each edge so word onsets and tails don't count). Returns the n loudest that
    last 0.3 s to max_len, the ones that run max_len or longer, and the room floor in dBFS."""
    sr = 16000
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", str(audio), "-ac", "1", "-ar", str(sr),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768.0
    h = int(sr * hop)
    nf = len(x) // h
    db = 20 * np.log10(np.sqrt((x[: nf * h].reshape(nf, h) ** 2).mean(axis=1) + 1e-12))
    floor = float(np.percentile(db, 20))
    loud = db > floor + 12  # 12 dB above the room's quiet level
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
    return short[:n], long_, round(floor, 1)


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
            (long_numbers if len(re.findall(r"\d", w["w"])) >= 3 else long_bad).append(i)
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
    official, matched, n_spoken, shared, clamped = build_words(turns, asr_words, duration)
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
    bursts, long_bursts, floor = loud_bursts(mp3, asr_words)
    laugh_times = [o["s"] for o in official if o["w"] == LAUGH]
    near = lambda b: "yes" if any(t - 1 <= b["s"] <= t + 5 for t in laugh_times) else ""
    overlap = lambda b: sum(1 for o in official if o["w"] != LAUGH and o["s"] < b["e"] and o["e"] > b["s"])
    md = [f"# Laughter: {args.case}", "",
          "## (Laughter.) in the official transcript", "",
          "Time is the end of the word before the marker. The 25 official words before it follow.", ""]
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
    (root / "laughs.md").write_text("\n".join(md) + "\n")

    checks = sanity_checks(words_out, match_rate)
    for k, v in checks.items():
        if not isinstance(v, dict):
            continue
        log(f"check {k}: {'PASS' if v['ok'] else 'FAIL'} {v['detail']}")
    stats = {
        "case": args.case, "year": args.year, "page_url": page_url, "mp3_url": mp3_url,
        "pdf_url": pdf_url, "model": args.model, "duration": duration,
        "asr_elapsed_s": asr.get("elapsed_s"), "asr_words": len(asr_words),
        "official_words": n_spoken, "matched": matched, "shared": shared, "clamped": clamped, "match_rate": match_rate,
        "turns": len(lines), "laugh_markers": sum(o["w"] == LAUGH for o in official),
        "mp3_bytes": mp3.stat().st_size, "checks": checks,
        "generated": datetime.date.today().isoformat(),
    }
    (work / "stats.json").write_text(json.dumps(stats, indent=1) + "\n")
    write_readme(root, stats)
    log(f"Wrote {root}")
    if not all(v["ok"] for v in checks.values() if isinstance(v, dict)):
        sys.exit("Sanity checks failed, see README.md")


def write_readme(root, st):
    c = st["checks"]
    mark = lambda ok: "PASS" if ok else "FAIL"
    ex = c["max_duration"]["examples"]
    long_note = ""
    if ex:
        long_note = "\n  Offending words: " + ", ".join(f"\"{w}\" {s:.3f}-{e:.3f}" for w, s, e in ex)
    nums = c["max_duration"]["numbers"]
    if nums:
        long_note += ("\n  Not counted: " + ", ".join(f"`{w}` {s:.3f}-{e:.3f} ({e - s:.2f} s)" for w, s, e in nums)
                      + ". A citation is one official word but is spoken as several; its time is the real "
                      "time taken to say it.")
    text = f"""# {root.name}: Supreme Court No. {st['case']}

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: {st['page_url']}
- Audio: {st['mp3_url']}
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

- `audio/argument.mp3`: the argument audio.
- `audio/words.json`: every official word in order, `{{"w", "s", "e", "speaker"}}`, times in seconds.
  `(Laughter.)` markers are included as entries of their own, running from the end of the word
  before to the start of the word after.
- `lines.json`: one entry per speaker turn, `{{"speaker", "s", "e", "text"}}`.
- `laughs.md`: each `(Laughter.)` with its time and the 25 words before it, then the 10 loudest
  sub-2-second bursts outside speech.
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
happened {st['shared']} times; it is the only case where a matched word's ASR time changes. ASR words with no official counterpart
are dropped. Punctuation-only tokens such as `--` are attached to the neighbouring word.

Regenerate with:

    python3 transcribe.py {st['case']} {st['year']} {root.name} --model {st['model']}
"""
    (root / "README.md").write_text(text)


if __name__ == "__main__":
    main()
