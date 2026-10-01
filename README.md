# Supreme Court oral argument transcriptions

Word-timed transcripts of Supreme Court oral arguments, for video editing. The audio and
transcripts are US government works in the public domain.

Each project in `projects/` holds the argument audio, every official word with start and end
times (`audio/words.json`), speaker turns (`lines.json`) and laugh positions (`laughs.md`,
including every pause ranked by room loudness, since transcripts under-mark laughter).
The wording is always the official transcript's; the times come from faster-whisper, aligned
word by word to the official text.

| Project | Case | Argued |
|---|---|---|
| [horne-raisins](projects/horne-raisins/) | Horne v. Department of Agriculture, No. 14-275 | 22 April 2015 |
| [lozman-house](projects/lozman-house/) | Lozman v. City of Riviera Beach, Florida, No. 11-626 | 1 October 2012 |
| [star-athletica-uniform](projects/star-athletica-uniform/) | Star Athletica, L.L.C. v. Varsity Brands, Inc., No. 15-866 | 31 October 2016 |
| [yates-fish](projects/yates-fish/) | Yates v. United States, No. 13-7451 (plus the opinion announcement) | 5 November 2014 |

## Running a new case

    sudo apt-get install -y ffmpeg poppler-utils
    pip install faster-whisper numpy
    python3 transcribe.py <docket> <term year> <project name>

For example `python3 transcribe.py 14-275 2014 horne-raisins`. The term year is the one in the
supremecourt.gov audio URL (`/oral_arguments/audio/2014/14-275`), so an argument heard in
spring 2015 is term 2014. The script finds the MP3 on that page and the transcript PDF on the same page or, failing
that, on the term's transcript listing (`/oral_arguments/argument_transcript/<year>`); pass
`--mp3-url` or `--pdf-url` to override either (for example with an oyez.org MP3), and
`--model small.en` if medium.en is too slow. It exits non-zero if a sanity check fails.

medium.en on a 4-core CPU runs at or a little faster than realtime: the 61-minute Horne
argument took 59 minutes, the 59-minute Lozman argument 40, the 62-minute Star Athletica
argument 49 and the 59-minute Yates argument 44.

Add `--opinion` to also fetch the opinion announcement (the justice reading the decision from
the bench) from oyez.org and transcribe it. There's no official transcript for those, so the
wording is Whisper's, cross-checked against Oyez's unofficial transcript; see the project README. The raw ASR is cached in `projects/<name>/work/`, so re-running only redoes the
alignment.
