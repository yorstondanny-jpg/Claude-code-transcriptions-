#!/usr/bin/env python3
"""Whisper-only transcription for "recast" projects: public audio with no official transcript.

Same outputs as the Supreme Court projects (transcribe.py), named for a single source:

    projects/<project>/audio/source.mp3   mono 64 kbps clip of the source
    projects/<project>/audio/words.json   {"w", "s", "e", "speaker"} per word
    projects/<project>/lines.json         {"speaker", "s", "e", "text"} per line
    projects/<project>/laughs.md          every pause of 0.4 s or more, ranked by room loudness
    projects/<project>/README.md          generated facts and checks, plus notes.md pasted in

Usage:
    python3 recast.py <project> <audio file or URL> [--start S] [--end S]
                      [--speakers "0=NARRATOR,12.5=CHAIR,..."] [--title "..."]

With no official wording to check against, the match rate is Whisper against itself: the whole
file is transcribed once, then again in independent 30 s windows, and the rate is the share of
first-pass words the second pass agrees with. Hand-written sections (sources, rights, picks) go in
projects/<project>/notes.md and are pasted into the README under the generated facts.
"""
import argparse
import datetime
import difflib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

from transcribe import (HOP, WindowASR, audio_duration, fmt_ts, log, loudness, loud_bursts, norm,
                        rewindow_long_words, run_asr, trim_stretched)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def download(url, dest, referer=None):
    """Browser user agent (and a referer, if given): Granicus's media server refuses anything else."""
    import requests
    headers = {"User-Agent": UA}
    if referer:
        headers["Referer"] = referer
    with requests.get(url, headers=headers, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(1 << 20):
                f.write(chunk)


def prepare_clip(src, dest, start=None, end=None):
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y"]
    if start is not None:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(src)]
    if end is not None:
        cmd += ["-t", f"{end - (start or 0):.3f}"]
    cmd += ["-vn", "-ac", "1", "-b:a", "64k", "-map_metadata", "-1", str(dest)]
    subprocess.run(cmd, check=True)


def drop_cues(words):
    """Whisper writes music and sound cues as words: '["Pomp' 'and' 'Circumstance"]', or a lone 'Music'
    over an instrumental stretch. Drop bracketed runs, and 'Music' with 2 s of silence on both sides."""
    out, inside = [], False
    for i, w in enumerate(words):
        t = w["w"].strip()
        if not inside and t[:1] in "[(":
            inside = True
        if inside:
            if t.rstrip(".,!?\"'")[-1:] in "])":
                inside = False
            continue
        gap_before = w["s"] - words[i - 1]["e"] if i else 99
        gap_after = words[i + 1]["s"] - w["e"] if i + 1 < len(words) else 99
        if norm(t) == "music" and gap_before >= 2 and gap_after >= 2:
            continue
        out.append(w)
    return out


def cross_check(words, audio, model_name, cache, duration, win=30.0):
    """Second, independent Whisper pass in win-second windows; share of first-pass words it agrees with."""
    wasr = WindowASR(audio, model_name, cache)
    second, t = [], 0.0
    while t < duration:
        second += wasr.get(t, min(t + win, duration))
        t += win
    a = [norm(w["w"]) for w in words]
    b = [norm(w["w"]) for w in second]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    matched = sum(bl.size for bl in sm.get_matching_blocks())
    return 100.0 * matched / max(len(a), 1), len(second)


def parse_speakers(spec):
    """'0=NARRATOR,12.5=CHAIR' -> [(0.0, 'NARRATOR'), (12.5, 'CHAIR')], sorted by time."""
    out = []
    for part in (spec or "0=SPEAKER 1").split(","):
        t, label = part.split("=", 1)
        out.append((float(t), label.strip()))
    return sorted(out)


def speaker_at(changes, t):
    label = changes[0][1]
    for ct, cl in changes:
        if t + 1e-6 >= ct:
            label = cl
    return label


def make_lines(words, gap=0.7):
    """New line on a speaker change, or after a sentence end followed by gap s of silence."""
    lines = []
    for i, w in enumerate(words):
        prev = words[i - 1] if i else None
        new = (prev is None or w["speaker"] != prev["speaker"]
               or (prev["w"][-1:] in ".?!" and w["s"] - prev["e"] >= gap))
        if new:
            lines.append({"speaker": w["speaker"], "s": w["s"], "e": w["e"], "text": w["w"]})
        else:
            lines[-1]["e"] = w["e"]
            lines[-1]["text"] += " " + w["w"]
    return lines


def rank_pauses(words, db, silence, min_gap=0.4, edge=0.1, hop=HOP):
    """Every gap of min_gap s or more between consecutive words, loudest first (energy mean inside
    the gap, edge s trimmed off each side, in dB over the silence level)."""
    pauses = []
    for k in range(1, len(words)):
        g0, g1 = words[k - 1]["e"], words[k]["s"]
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
    return pauses


def checks(words, match_rate):
    order_bad = sum(1 for i in range(1, len(words)) if words[i]["s"] < words[i - 1]["s"])
    inverted = sum(1 for w in words if w["e"] < w["s"])
    long_bad = [w for w in words if w["e"] - w["s"] > 3.0]
    return {
        "time_order": (not order_bad and not inverted,
                       f"{order_bad} words start before the previous word; {inverted} end before they start"),
        "max_duration": (not long_bad, f"{len(long_bad)} words longer than 3 s"
                         + "".join(f"; \"{w['w']}\" {fmt_ts(w['s'])} to {fmt_ts(w['e'])}" for w in long_bad[:5])),
        "match_rate": (match_rate > 85.0, f"{match_rate:.2f}% (threshold 85%)"),
    }


def write_laughs(root, words, pauses, bursts, floor, silence, title):
    def ctx(k, n=8):
        before = " ".join(w["w"] for w in words[max(0, k - n):k])
        after = " ".join(w["w"] for w in words[k:k + n])
        return before.replace("|", "\\|"), after.replace("|", "\\|")
    out = [f"# Pauses and laughs: {title}\n",
           "There is no official transcript, so there are no laughter markers to copy. Instead, every pause of "
           "0.4 s or more between transcribed words is listed below, loudest first. Loudness is the energy mean "
           f"inside the pause (0.1 s trimmed off each side against word bleed), in dB over the recording's silence "
           f"level ({silence:.1f} dBFS, the 5th percentile of 50 ms frames). A loud pause is one where something "
           "other than transcribed speech is happening: laughter, crosstalk, music, a gavel. A quiet one is dead air. "
           "\"Loud s\" counts the seconds inside the pause at least 12 dB over silence.\n",
           f"{len(pauses)} pauses.\n",
           "| # | start | end | length (s) | mean dB over silence | peak dB over silence | loud s | before | after |",
           "|---|---|---|---|---|---|---|---|---|"]
    for n, p in enumerate(pauses, 1):
        b, a = ctx(p["k"])
        out.append(f"| {n} | {fmt_ts(p['s'])} | {fmt_ts(p['e'])} | {p['e'] - p['s']:.2f} | {p['over']} | "
                   f"{p['peak_over']} | {p['loud_s']} | …{b} | {a}… |")
    out += ["", "## Loudest short bursts outside speech\n",
            f"Runs of 50 ms frames at least 12 dB above the room floor ({floor:.1f} dBFS, 20th percentile) inside "
            "pauses of 0.4 s or more, lasting 0.3 to 2 s, ranked by mean loudness. These are the likeliest laughs.\n",
            "| # | start | end | length (s) | mean dBFS | peak dBFS |", "|---|---|---|---|---|---|"]
    for n, bu in enumerate(bursts, 1):
        out.append(f"| {n} | {fmt_ts(bu['s'])} | {fmt_ts(bu['e'])} | {bu['dur']} | {bu['mean_db']} | {bu['peak_db']} |")
    (root / "laughs.md").write_text("\n".join(out) + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("source", help="audio/video file or URL")
    ap.add_argument("--start", type=float, help="clip start in the source, seconds")
    ap.add_argument("--end", type=float, help="clip end in the source, seconds")
    ap.add_argument("--speakers", help='speaker changes, "0=NARRATOR,12.5=CHAIR" (times in the clip)')
    ap.add_argument("--title", default=None)
    ap.add_argument("--model", default="medium.en")
    ap.add_argument("--referer", help="Referer header for the download (Granicus wants its own site)")
    args = ap.parse_args()

    root = Path("projects") / args.project
    (root / "audio").mkdir(parents=True, exist_ok=True)
    work = root / "work"
    work.mkdir(exist_ok=True)
    src = args.source
    if src.startswith("http"):
        dl = work / ("download" + Path(src.split("?")[0]).suffix)
        if not dl.exists():
            download(src, dl, args.referer)
        src = dl
    mp3 = root / "audio" / "source.mp3"
    prepare_clip(src, mp3, args.start, args.end)
    duration = audio_duration(mp3)
    log(f"{mp3}: {duration:.1f} s, {mp3.stat().st_size / 1e6:.2f} MB")

    tag = "" if args.start is None and args.end is None else f"-{args.start or 0:g}-{args.end or 0:g}"
    asr = run_asr(mp3, args.model, work / f"asr{tag}.json")
    raw = [dict(w) for w in asr["words"] if w["w"]]
    words = drop_cues(raw)
    n_cues = len(raw) - len(words)
    db, floor, loud, voiced, silence = loudness(mp3)
    trimmed = trim_stretched(words, voiced)
    fixed = rewindow_long_words(words, mp3, args.model, voiced, work / f"windows{tag}.json")
    match_rate, n_second = cross_check(words, mp3, args.model, work / f"crosscheck{tag}.json", duration)

    changes = parse_speakers(args.speakers)
    for w in words:
        w.pop("p", None)
        w["speaker"] = speaker_at(changes, w["s"])
    (root / "audio" / "words.json").write_text(json.dumps(words, indent=1, ensure_ascii=False) + "\n")
    lines = make_lines(words)
    (root / "lines.json").write_text(json.dumps(lines, indent=1, ensure_ascii=False) + "\n")

    pauses = rank_pauses(words, db, silence)
    bursts, _ = loud_bursts(words, db, floor, loud)
    title = args.title or args.project
    write_laughs(root, words, pauses, bursts, floor, silence, title)

    st = checks(words, match_rate)
    regen = " ".join(["python3 recast.py", args.project, f'"{args.source}"']
                     + ([f"--start {args.start}"] if args.start is not None else [])
                     + ([f"--end {args.end}"] if args.end is not None else [])
                     + ([f'--speakers "{args.speakers}"'] if args.speakers else [])
                     + ([f'--title "{args.title}"'] if args.title else [])
                     + ([f'--referer "{args.referer}"'] if args.referer else []))
    notes = root / "notes.md"
    clip = ("whole file" if args.start is None and args.end is None
            else f"{fmt_ts(args.start or 0)} to {fmt_ts(args.end) if args.end else 'end'} of the source")
    readme = [f"# {title}\n",
              notes.read_text().strip() + "\n" if notes.exists() else "",
              "## Transcription\n",
              f"- Clip: {clip}, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, "
              f"{mp3.stat().st_size / 1e6:.2f} MB).",
              f"- Length: {fmt_ts(duration)} ({duration:.1f} s).",
              f"- Words: {len(words)}. Lines: {len(lines)}.",
              f"- Model: faster-whisper `{args.model}` (CPU, int8, beam 5, word timestamps, no VAD filter). "
              "There is no official transcript: the wording is Whisper's, unedited.",
              f"- Music and sound cues Whisper writes as words (bracketed text, a lone \"Music\") are dropped: "
              f"{n_cues} tokens here.",
              f"- Words over 1.5 s trimmed to the voiced audio: {trimmed}; words over 3 s re-timed from a window "
              f"re-run: {fixed}.",
              f"- Match rate: {match_rate:.2f}%. With no official wording, this is Whisper against itself: a second, "
              f"independent pass over 30 s windows ({n_second} words) agrees with this share of the first pass's words.",
              "",
              "## Sanity checks\n",
              "| check | result | detail |", "|---|---|---|"]
    for name, (ok, detail) in st.items():
        readme.append(f"| {name.replace('_', ' ')} | {'PASS' if ok else 'FAIL'} | {detail} |")
    readme += ["", "## Files\n",
               "- `audio/source.mp3`: the clip.",
               "- `audio/words.json`: one entry per word, `{\"w\", \"s\", \"e\", \"speaker\"}` (seconds into source.mp3).",
               "- `lines.json`: one entry per line, `{\"speaker\", \"s\", \"e\", \"text\"}`; a new line starts on a "
               "speaker change or after a sentence end followed by 0.7 s of silence.",
               "- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.",
               "", "Regenerate with:", "", "```", regen, "```", "",
               f"_Generated {datetime.date.today().isoformat()} by `recast.py`._"]
    (root / "README.md").write_text("\n".join(readme) + "\n")
    for name, (ok, detail) in st.items():
        log(f"{name}: {'PASS' if ok else 'FAIL'} ({detail})")


if __name__ == "__main__":
    sys.exit(main())
