#!/usr/bin/env python3
"""Laugh scan over Oyez for Supreme Court terms before 2000 (supremecourt.gov's transcript list starts at 2000).

Usage:
    python3 oyez_scan.py <out dir> <first term> <last term>

Oyez marks the room's laughs as "[Laughter]" in its timed transcripts. For every argument in the range this
writes one line to <out dir>/oyez.jsonl (resumes where it stopped): case, docket, date, the laugh count, and
for each laugh its time, the speaker and the 300 characters before it (the setup). Then <out dir>/oyez.json
lists every argument, most laughs first. Audio: Oyez's mp3 (logged as the source on any Reel that uses it).
"""
import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

API = "https://api.oyez.org"
LAUGH = re.compile(r"\[\s*laughter\s*\]|\(\s*laughter\.?\s*\)", re.I)


def get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "pending-review-scout"})
            with urllib.request.urlopen(req, timeout=40) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


def clock(s):
    s = int(s or 0)
    return f"{s // 60}:{s % 60:02d}"


def scan_audio(case, media):
    d = get(media["href"])
    t = d.get("transcript") or {}
    blocks = []
    for sec in t.get("sections", []) or []:
        for turn in sec.get("turns", []) or []:
            who = ((turn.get("speaker") or {}).get("name")) or "?"
            for b in turn.get("text_blocks", []) or []:
                blocks.append((who, b.get("start"), b.get("text") or ""))
    laughs, prior = [], ""
    for who, start, text in blocks:
        for m in LAUGH.finditer(text):
            setup = (prior + " " + text[:m.start()]).strip()[-300:]
            laughs.append({"t": clock(start), "speaker": who, "setup": setup})
        prior = (prior + " " + text)[-600:]
    mp3 = next((f["href"] for f in (d.get("media_file") or []) if f and f.get("href", "").endswith(".mp3")), "")
    return {"term": case["term"], "docket": case.get("docket_number"), "case": case.get("name"),
            "title": media.get("title"), "laughs": len(laughs), "detail": laughs, "mp3": mp3,
            "has_transcript": bool(blocks)}


def main():
    out, first, last = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True)
    log = out / "oyez.jsonl"
    done = set()
    if log.exists():
        for l in log.read_text().splitlines():
            r = json.loads(l)
            done.add((r["docket"], r["title"]))
    jobs = []
    for term in range(last, first - 1, -1):
        for c in get(f"{API}/cases?per_page=0&filter=term:{term}"):
            try:
                full = get(c["href"])
            except Exception as e:
                print("skip", c.get("href"), e, file=sys.stderr)
                continue
            full["term"] = term
            for m in full.get("oral_argument_audio") or []:
                if (full.get("docket_number"), m.get("title")) not in done:
                    jobs.append((full, m))
        print(f"term {term}: {len(jobs)} arguments queued", file=sys.stderr, flush=True)
    with cf.ThreadPoolExecutor(6) as ex, log.open("a") as f:
        futs = {ex.submit(scan_audio, c, m): (c, m) for c, m in jobs}
        for fut in cf.as_completed(futs):
            try:
                r = fut.result()
            except Exception as e:
                print("fail", futs[fut][1].get("href"), e, file=sys.stderr)
                continue
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
    rows = [json.loads(l) for l in log.read_text().splitlines()]
    rows.sort(key=lambda r: -r["laughs"])
    (out / "oyez.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(f"{len(rows)} arguments, {sum(r['laughs'] > 0 for r in rows)} with a laugh", file=sys.stderr)


if __name__ == "__main__":
    main()
