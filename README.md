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
| [horne-raisins-2013](projects/horne-raisins-2013/) | Horne v. Department of Agriculture (I), No. 12-123 (plus the opinion announcement) | 20 March 2013 |
| [horne-raisins](projects/horne-raisins/) | Horne v. Department of Agriculture (II), No. 14-275 (plus the opinion announcement) | 22 April 2015 |
| [lozman-house](projects/lozman-house/) | Lozman v. City of Riviera Beach, Florida, No. 11-626 | 1 October 2012 |
| [star-athletica-uniform](projects/star-athletica-uniform/) | Star Athletica, L.L.C. v. Varsity Brands, Inc., No. 15-866 | 31 October 2016 |
| [yates-fish](projects/yates-fish/) | Yates v. United States, No. 13-7451 (plus the opinion announcement) | 5 November 2014 |
| [collins-motorcycle](projects/collins-motorcycle/) | Collins v. Virginia, No. 16-1027 (plus the opinion announcement) | 9 January 2018 |
| [jones-gps](projects/jones-gps/) | United States v. Jones, No. 10-1259 (plus the opinion announcement) | 8 November 2011 |
| [dubin-identity](projects/dubin-identity/) | Dubin v. United States, No. 22-10 (plus the opinion announcement) | 27 February 2023 |
| [raich-marijuana](projects/raich-marijuana/) | Gonzales v. Raich, No. 03-1454 (argument audio from Oyez; plus the opinion announcement) | 29 November 2004 |
| [sturgeon-hovercraft-2](projects/sturgeon-hovercraft-2/) | Sturgeon v. Frost (II), No. 17-949 (plus the opinion announcement) | 14 November 2018 |
| [sturgeon-hovercraft-1](projects/sturgeon-hovercraft-1/) | Sturgeon v. Frost (I), No. 14-1209 (plus the opinion announcement) | 20 January 2016 |
| [pom-juice](projects/pom-juice/) | POM Wonderful LLC v. Coca-Cola Co., No. 12-761 (plus the opinion announcement) | 21 April 2014 |
| [alvarez-medal](projects/alvarez-medal/) | United States v. Alvarez, No. 11-210 (plus the opinion announcement) | 22 February 2012 |
| [bowman-soybean](projects/bowman-soybean/) | Bowman v. Monsanto Co., No. 11-796 (plus the opinion announcement) | 19 February 2013 |
| [jardines-dog](projects/jardines-dog/) | Florida v. Jardines, No. 11-564 (plus the opinion announcement) | 31 October 2012 |
| [brown-ema-videogames](projects/brown-ema-videogames/) | Brown v. Entertainment Merchants Association, No. 08-1448 (argued as Schwarzenegger v. EMA; plus the opinion announcement) | 2 November 2010 |

## Recast pilots

Real public audio for animation pilots, re-performed by animal characters. There's no official
transcript, so `recast.py` uses Whisper's wording, checked against a second independent Whisper
pass. Each project has the same files, with the audio at `audio/source.mp3`, and states the
source's copyright status at the top of its README.

| Project | Source | Copyright status |
|---|---|---|
| [council-pigeons](projects/council-pigeons/) | St. Petersburg, FL City Council committee, 14 May 2026: "What's the flashing red?" (44 s) | Florida public record; no copyright claim on the recording |
| [prelinger-snails](projects/prelinger-snails/) | *Habit Patterns* (Knickerbocker Productions, 1954), Prelinger Archives item HabitPat1954 (14 min) | Public domain per the archive.org item (`licenseurl` creativecommons.org/licenses/publicdomain/) |

    python3 recast.py <project> <audio file or URL> [--start S --end S] [--speakers "0=NARRATOR,12.5=CHAIR"]

Hand-written notes (sources, rights, candidates) go in `projects/<project>/notes.md` and are pasted
into the generated README.

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
argument 49, the 59-minute Yates argument 44, the 61-minute Brown argument 45, the 62-minute Jardines
argument 45, the 70-minute Bowman argument 47 and the 59-minute Alvarez argument 70 (on a
slower machine), and the 62-minute POM argument 37.

Add `--opinion` to also fetch the opinion announcement (the justice reading the decision from
the bench) from oyez.org and transcribe it. There's no official transcript for those, so the
wording is Whisper's, cross-checked against Oyez's unofficial transcript; see the project README.
Add `--mentions "Girl Scout(s),salesman/salesmen,front door"` to list every sentence in the
argument that mentions those terms, with time and speaker, and `--quotes "line one|line two"` to
get each line's exact time and a 10-second clip around it in `audio/quotes/`. The raw ASR is cached in `projects/<name>/work/`, so re-running only redoes the
alignment. While it runs, progress is saved every few segments, so if the run dies (a container
restart, say) the next run resumes where it stopped.

## Laugh scout

`laugh_scout.py` ranks cases by courtroom laughter using the official transcripts alone (no
audio): `python3 laugh_scout.py projects/_laugh-scout/cases.json projects/_laugh-scout`. Results
are in [projects/_laugh-scout](projects/_laugh-scout/) and [projects/_laugh-scout-2](projects/_laugh-scout-2/).
