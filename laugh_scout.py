#!/usr/bin/env python3
"""Laugh scout: count courtroom laughter in official Supreme Court oral argument transcripts.

Fetches transcript PDFs only (no audio, no ASR). For each case it finds every transcript on the
term's argument_transcript listing whose link text is the docket number (so a re-argued case
gets each argument), counts every "(... laughter ...)" marker in the argument itself (not the
word index), and records page:line, the speaker and the text just before each laugh, plus the
argument length from the transcript's start and end times.

Usage:
    python3 laugh_scout.py projects/_laugh-scout/cases.json projects/_laugh-scout [TOP_N]

cases.json is a list of {"case", "docket", "argued" (YYYY-MM-DD), "note"}.
Requires pdftotext (poppler-utils).
"""
import datetime
import json
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urljoin

SCOTUS = "https://www.supremecourt.gov"
UA = {"User-Agent": "Mozilla/5.0 (laugh scout)"}

LAUGH_MARK = "<laughter>"  # history entry marking a laugh, so lookbacks stop there
# "(Laughter.)", and "[Laughter.]" in transcripts before about 2006
LAUGH_RE = re.compile(r"[(\[]\s*[^()\[\]]*?\blaughter\b[^()\[\]]*[)\]]\.?", re.I)
SPEAKER_RE = re.compile(
    r"^((?:CHIEF )?JUST(?:ICE)? [A-Z'\-]+|(?:MR|MS|MRS|GENERAL)\.? [A-Za-z'\-]+(?: [A-Z'\-]{2,})?|GENERAL [A-Za-z'\-]+|"
    r"THE CLERK|THE MARSHAL|QUESTION)\s*:\s*(.*)$")
TIME_RE = re.compile(r"(\d{1,2}):(\d{2})\s*([ap])\.\s*m\.", re.I)
FURNITURE_RE = re.compile(r"^(Official( - Subject to Final Review)?|.* Reporting (Company|Corporation)|"
                          r".*www\.\S+\.com.*|\d{1,3})$", re.I)


def fetch(url):
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 ** (attempt + 1))


def term_of(argued):
    """October Term year: arguments from October to December are that year's term,
    January to September the previous year's."""
    d = datetime.date.fromisoformat(argued)
    return d.year if d.month >= 10 else d.year - 1


_listings = {}


def transcript_urls(docket, term):
    """Every transcript PDF on the term listing whose link text is this docket number."""
    url = f"{SCOTUS}/oral_arguments/argument_transcript/{term}"
    if url not in _listings:
        _listings[url] = fetch(url).decode("utf-8", "replace")
    pat = re.compile(r"""<a\s+href=['"]([^'"]+\.pdf)['"][^>]*>\s*%s\b[^<]*</a>""" % re.escape(docket), re.I)
    return url, [urljoin(url, m) for m in dict.fromkeys(pat.findall(_listings[url]))]


def to_minutes(h, m, ap):
    h = int(h) % 12 + (12 if ap.lower() == "p" else 0)
    return h * 60 + int(m)


def scan(pdf_bytes):
    """Laughs, argument start/end and page count from one transcript PDF."""
    text = subprocess.run(["pdftotext", "-layout", "-", "-"], input=pdf_bytes,
                          capture_output=True, check=True).stdout.decode("utf-8", "replace")
    text = text.replace("­", "-")
    pages = text.split("\f")
    # PDF page index vs the transcript's printed page number differs by layout (some covers
    # are unnumbered); find the offset at which "PDF page - offset" is printed on most pages
    bare = [{int(l.strip()) for l in pg.splitlines() if re.fullmatch(r"\s*\d{1,3}\s*", l)} for pg in pages]
    offset = max(range(-2, 4), key=lambda k: sum(1 for i, b in enumerate(bare, 1) if (i - k) in b))
    page_hits = sum(1 for i, b in enumerate(bare, 1) if (i - offset) in b)
    laughs, start_t, end_t = [], None, None
    end_note = None
    in_argument = False
    speaker, history = None, []  # history: (speaker, words) of recent body lines
    started = ended = False
    for pi, page in enumerate(pages, 1):
        for raw in page.splitlines():
            line = raw.strip()
            if not line or re.fullmatch(r"\d{1,3}", line):  # blank numbered line or page number
                continue
            if FURNITURE_RE.match(line):
                continue
            lm = re.match(r"^(\d{1,2})\s+(.*)$", line)
            lineno, body = (int(lm.group(1)), lm.group(2).strip()) if lm else (None, line)
            body = re.sub(r"\s+", " ", body)
            if not started:
                if re.match(r"^P\s*R\s*O\s*C\s*E\s*E\s*D\s*I\s*N\s*G\s*S", body):
                    started = True
                continue
            if ended:
                continue
            # start: the last "(10:04 a.m.)" / "[10:04 a.m.]" before the first argument heading
            # (Kyllo opens with a 10:00 ceremony before the case is called at 10:14)
            if (body.startswith("ORAL ARGUMENT OF") and len(body) > len("ORAL ARGUMENT OF") + 2
                    and not re.search(r"\bPAGE\b", body)):  # a real heading, not a contents line
                in_argument = True
            if not in_argument:
                tm = TIME_RE.search(body)
                if tm and body[:1] in "([":
                    start_t = to_minutes(*tm.groups())
                    continue
            if re.match(r"^[(\[]?Whereupon", body):  # Heien (13-604) drops the bracket; old ones use [
                tm = TIME_RE.search(body)
                bare = re.search(r"\bat (\d{1,2}):(\d{2})", body)
                if tm:
                    end_t = to_minutes(*tm.groups())
                elif bare and start_t is not None:
                    # POM (12-761) has "at 12:07," with no a.m./p.m.: take the first matching
                    # clock time after the start
                    end_t = min((to_minutes(bare.group(1), bare.group(2), ap) for ap in "ap"),
                                key=lambda t: (t - start_t) % (24 * 60))
                    end_note = "end time has no a.m./p.m.; read as the first matching time after the start"
                ended = True
                continue
            sm = SPEAKER_RE.match(body)
            if sm:
                speaker = re.sub(r"^(CHIEF )?JUST ", r"\1JUSTICE ", sm.group(1).upper())  # "JUST KAGAN:" typo
                body = sm.group(2)
            # walk the line in order: text goes into the history, and each laugh marker looks
            # back through it to the previous marker or the start of the speaker's turn
            pos = 0
            for lmatch in list(LAUGH_RE.finditer(body)) + [None]:
                seg = body[pos:lmatch.start() if lmatch else len(body)].split()
                if seg:
                    history.append((speaker, seg))
                if lmatch is None:
                    break
                pos = lmatch.end()
                prev_spk = next((spk for spk, _ in reversed(history) if spk != LAUGH_MARK), speaker)
                words = []
                for spk, ws in reversed(history):
                    if len(words) >= 40 or spk != prev_spk:  # a laugh marker or another speaker
                        break
                    words = ws + words
                laughs.append({"page": pi - offset, "pdf_page": pi, "line": lineno,
                               "marker": lmatch.group(0), "speaker": prev_spk,
                               "text": " ".join(words[-40:])})
                history.append((LAUGH_MARK, []))
            history = history[-12:]
    minutes = None
    if start_t is not None and end_t is not None:
        minutes = end_t - start_t if end_t >= start_t else end_t + 12 * 60 - start_t
    return {"laughs": laughs, "start": start_t, "end": end_t, "minutes": minutes,
            "pdf_pages": len(pages), "found_proceedings": started, "found_end": ended,
            "end_note": end_note, "page_offset": offset, "pages_with_printed_number": page_hits}


def fmt_clock(m):
    if m is None:
        return "?"
    h, mm = divmod(m, 60)
    return f"{(h - 1) % 12 + 1}:{mm:02d} {'a.m.' if h < 12 else 'p.m.'}"


def readme(results, missing, cases, top=5, cmd="python3 laugh_scout.py projects/_laugh-scout/cases.json projects/_laugh-scout"):
    date = lambda iso: datetime.date.fromisoformat(iso).strftime("%-d %b %Y")
    label = lambda r: r["case"] + (f" (argument {r['argument']})" if r["arguments_found"] > 1 else "")
    out = ["# Laugh scout", "",
           "Courtroom laughter in the official oral argument transcripts, counted from the PDFs on "
           "supremecourt.gov. No audio was used. Every bracketed marker containing the word "
           "\"laughter\" counts: \"(Laughter.)\", \"(Laughter).\", \"(Laughter)\", \"(A little "
           "laughter.)\", and \"[Laughter.]\" in square brackets as in transcripts before about 2006. Only the argument itself is scanned, from \"P R O C E E D I N G "
           "S\" to \"Whereupon\", so the word index at the back doesn't count. Minutes come from the "
           "start and end times printed in the transcript. The transcript is a stenographer's "
           "record: it marks laughter the reporter noticed, and some reporters mark more than others.",
           "", f"Regenerate with `{cmd}`.",
           "", "## Ranking", "", "Most laughs first; ties broken by laughs per 10 minutes.", "",
           "| # | case | docket | argued | laughs | minutes | per 10 min | transcript |",
           "|---|---|---|---|---|---|---|---|"]
    for k, r in enumerate(results, 1):
        out.append(f"| {k} | {label(r)} | {r['docket']} | {date(r['argued'])} | {r['count']} | "
                   f"{r['minutes'] if r['minutes'] is not None else '?'} | "
                   f"{r['laughs_per_10_min'] if r['laughs_per_10_min'] is not None else '?'} | [PDF]({r['url']}) |")
    out += ["", f"## Every laugh in the top {top}", "",
            "Page:line is the transcript's own numbering (the printed page number, not the PDF page). "
            "The speaker and text are the line or lines just before the marker, up to 40 words, "
            "within that speaker's turn.", ""]
    for r in results[:top]:
        out += [f"### {label(r)}, No. {r['docket']}: {r['count']} laughs in {r['minutes']} minutes", "",
                "| # | page:line | speaker | just before | marker |", "|---|---|---|---|---|"]
        for k, l in enumerate(r["laughs"], 1):
            out.append(f"| {k} | {l['page']}:{l['line']} | {l['speaker'] or '?'} | "
                       f"{l['text'].replace('|', '/')} | {l['marker']} |")
        out.append("")
    out += ["## Transcripts not found", ""]
    if missing:
        out += [f"- {m['case']}, No. {m['docket']} (argued {date(m['argued'])}): nothing on {m['listing']}"
                for m in missing]
    else:
        out.append(f"None. All {len(cases)} transcripts were found"
                   + (", one argument each." if all(r["arguments_found"] == 1 for r in results) else "."))
    notes = []
    for r in results:
        if r["checks"].get("end_note"):
            notes.append(f"- {label(r)}: the end time is printed without a.m./p.m. ({r['end']} assumed).")
        if not r["checks"]["found_end"] or r["minutes"] is None:
            notes.append(f"- {label(r)}: no end time found, so no rate.")
    if notes:
        out += ["", "## Notes", ""] + notes
    return "\n".join(out) + "\n"


def main():
    cases = json.loads(Path(sys.argv[1]).read_text())
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    results, missing = [], []
    for c in cases:
        term = term_of(c["argued"])
        listing, urls = transcript_urls(c["docket"], term)
        if not urls:
            missing.append({**c, "term": term, "listing": listing})
            print(f"{c['docket']}: no transcript on {listing}")
            continue
        for k, url in enumerate(urls, 1):
            r = scan(fetch(url))
            per10 = round(10 * len(r["laughs"]) / r["minutes"], 2) if r["minutes"] else None
            results.append({**c, "term": term, "argument": k, "arguments_found": len(urls), "url": url,
                            "listing": listing, "count": len(r["laughs"]), "minutes": r["minutes"],
                            "start": fmt_clock(r["start"]), "end": fmt_clock(r["end"]),
                            "laughs_per_10_min": per10, "laughs": r["laughs"],
                            "checks": {"found_proceedings": r["found_proceedings"], "found_end": r["found_end"],
                                       "end_note": r["end_note"], "page_offset": r["page_offset"],
                                       "pages_with_printed_number": f"{r['pages_with_printed_number']}/{r['pdf_pages']}"}})
            print(f"{c['docket']} #{k}: {len(r['laughs'])} laughs, {r['minutes']} min, {url}")
    results.sort(key=lambda r: (-r["count"], -(r["laughs_per_10_min"] or 0)))
    (out_dir / "laughs.json").write_text(json.dumps({"generated": datetime.date.today().isoformat(),
                                                     "results": results, "not_found": missing},
                                                    indent=1, ensure_ascii=False) + "\n")
    top = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    cmd = "python3 laugh_scout.py " + " ".join(sys.argv[1:])
    (out_dir / "README.md").write_text(readme(results, missing, cases, top=top, cmd=cmd))
    print(f"wrote {out_dir / 'laughs.json'} and README.md")


if __name__ == "__main__":
    main()
