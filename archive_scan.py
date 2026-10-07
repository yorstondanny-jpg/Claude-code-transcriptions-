#!/usr/bin/env python3
"""Laugh scan over the whole transcript archive: every oral argument transcript PDF on supremecourt.gov
for a range of October Terms, laughter counted with laugh_scout.scan (same markers, same rules).

Usage:
    python3 archive_scan.py <out dir> [first term] [last term]      (default 2005 to the current term)

Progress is appended to <out dir>/scan.jsonl one transcript at a time, so a run that dies resumes
where it stopped. Arguments from 1 May 2020 to 30 September 2021 (by telephone, no courtroom) are
listed but not scanned. Writes <out dir>/archive.json (every transcript, most laughs first).
"""
import concurrent.futures as cf
import datetime
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote, urljoin

from laugh_scout import SCOTUS, fetch, fmt_clock, scan

PHONE = (datetime.date(2020, 5, 1), datetime.date(2021, 9, 30))
ROW_RE = re.compile(r"<tr\b.*?</tr>", re.S | re.I)
LINK_RE = re.compile(r"""<a\s+href=['"]([^'"]+\.pdf)['"][^>]*>\s*([^<]+?)\s*</a>""", re.I)
DATE_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(\d{2,4})\b")


def listing(term):
    """[(docket, case, date, pdf url)] from one term's transcript listing."""
    url = f"{SCOTUS}/oral_arguments/argument_transcript/{term}"
    page = fetch(url).decode("utf-8", "replace")
    rows = []
    for tr in ROW_RE.findall(page):
        link, date = LINK_RE.search(tr), DATE_RE.search(tr)
        if not link or not date:
            continue
        text = re.sub(r"<[^>]+>", " ", tr[link.end():])
        case = html.unescape(re.sub(r"\s+", " ", DATE_RE.sub("", text))).strip()
        m, d, y = map(int, date.groups())
        y += 2000 if y < 100 else 0
        rows.append({"docket": html.unescape(link.group(2)).strip(), "case": case,
                     "argued": datetime.date(y, m, d).isoformat(), "term": term,
                     "url": quote(urljoin(url, html.unescape(link.group(1))), safe=":/%")})
    return rows


def scan_one(row):
    r = scan(fetch(row["url"]))
    per10 = round(10 * len(r["laughs"]) / r["minutes"], 2) if r["minutes"] else None
    return {**row, "count": len(r["laughs"]), "minutes": r["minutes"], "start": fmt_clock(r["start"]),
            "end": fmt_clock(r["end"]), "laughs_per_10_min": per10, "laughs": r["laughs"],
            "checks": {"found_proceedings": r["found_proceedings"], "found_end": r["found_end"],
                       "end_note": r["end_note"]}}


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today()
    first = int(sys.argv[2]) if len(sys.argv) > 2 else 2005
    last = int(sys.argv[3]) if len(sys.argv) > 3 else (today.year if today.month >= 10 else today.year - 1)
    progress = out / "scan.jsonl"
    done = {}
    if progress.exists():
        for line in progress.read_text().splitlines():
            r = json.loads(line)
            done[r["url"]] = r
    rows, skipped = [], []
    for term in range(first, last + 1):
        try:
            t_rows = listing(term)
        except Exception as e:
            print(f"OT{term}: no listing ({e})")
            continue
        for r in t_rows:
            d = datetime.date.fromisoformat(r["argued"])
            (skipped if PHONE[0] <= d <= PHONE[1] else rows).append(r)
        print(f"OT{term}: {len(t_rows)} transcripts")
    todo = [r for r in rows if r["url"] not in done]
    print(f"{len(rows)} to scan ({len(rows) - len(todo)} already done), {len(skipped)} telephone arguments skipped")
    with progress.open("a") as f, cf.ThreadPoolExecutor(4) as ex:
        futs = {ex.submit(scan_one, r): r for r in todo}
        for n, fut in enumerate(cf.as_completed(futs), 1):
            row = futs[fut]
            try:
                res = fut.result()
            except Exception as e:
                print(f"  failed {row['docket']} {row['url']}: {e}")
                continue
            done[res["url"]] = res
            f.write(json.dumps(res, ensure_ascii=False) + "\n")
            f.flush()
            if n % 50 == 0:
                print(f"  {n}/{len(todo)}")
    results = sorted((done[r["url"]] for r in rows if r["url"] in done),
                     key=lambda r: (-r["count"], -(r["laughs_per_10_min"] or 0)))
    (out / "archive.json").write_text(json.dumps(
        {"generated": today.isoformat(), "terms": [first, last], "scanned": len(results),
         "missing": [r for r in rows if r["url"] not in done], "telephone_skipped": skipped,
         "results": results}, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {out / 'archive.json'}: {len(results)} transcripts")


if __name__ == "__main__":
    main()
