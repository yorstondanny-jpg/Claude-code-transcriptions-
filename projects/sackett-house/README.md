# sackett-house: Supreme Court No. 10-1062

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2011/10-1062
- Audio: https://www.supremecourt.gov/media/audio/mp3files/10-1062.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2011/10-1062.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 15 min on 4 CPU cores
- Audio length: 1:01:17.153 (3677.153 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.4 MB
- Official words: 3520 (plus 2 `(Laughter.)` markers), in 81 speaker turns
- ASR words: 3493
- Official words matched to an ASR word: 3353 of 3520 (**95.26%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.26% (threshold 85%).

81 words are shorter than 20 ms. These are official words the ASR didn't produce,
mostly repeats, false starts and cross-talk ("the -- the --", "I -- I think"), squeezed into the
small gap between the ASR words either side. Their order is right; their exact times are not.

## Files

- `audio/argument.mp3`: the argument audio (and `audio/quotes/`, 10-second clips, when quotes are asked for).
- `audio/words.json`: every official word in order, `{"w", "s", "e", "speaker"}`, times in seconds.
  `(Laughter.)` markers are included as entries of their own, running from the end of the word
  before to the start of the word after.
- `lines.json`: one entry per speaker turn, `{"speaker", "s", "e", "text"}`.
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
happened 2 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 3 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 10-1062 2011 sackett-house --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:31:24.180 | 1884.180 | medium | 1.02 | 0.75 | 18.6 | 26.0 | But the main point I want to -- Mr. Stewart, I -- They were getting a good night's sleep? But they are getting a good night's sleep before they read your brief? |
| 2 | 0:35:59.400 | 2159.400 | small | 0.92 | 0.30 | 13.1 | 17.8 | that there are things here -- in here that are wrong or compliance measures that you regard as infeasible, you're welcome to tell us. And I think -- Well, that's very nice. |

## Petitioner's opening, first 3 minutes

Everything said from 0:20:00.000 to 0:23:00.000, official wording, with each turn's start time. Interruptions from the bench are included.

[0:20:00.000] JUSTICE SCALIA: the issue would be clear as to what burden the agency has to sustain. But it's -- it's really the dual nature of this process that creates the difficulty, isn't it?

[0:20:16.100] MR. SCHIFF: Yes, Justice Scalia, to some extent it is, of course, the process that -- that Congress --

[0:20:20.380] JUSTICE SCALIA: But that's in the statute. The agency didn't make that up, right? The statute provides for compliance orders, and it calls them "compliance orders," doesn't it?

[0:20:29.980] MR. SCHIFF: It -- it does indeed. And so, even if the Sacketts on remand don't get their ideal mode of judicial review, something is frankly better than nothing. They have been told for 4 years they cannot build their home. They have been threatened with ruinous civil penalties. And, to date, they have had no opportunity for their day in court. The -- the Sacketts cannot trigger an enforcement action. I mean, perhaps if Congress had written the statute differently to allow for some sort of judicial review that the Sacketts could -- could initiate for a compliance order, that might -- that might answer, Justice Scalia, your concerns. But that is not the statute we have. We have a statute where Congress has said EPA can issue a compliance order, and we have in combination with that the presumption in favor of judicial review of final agency action; we have the avoidance canon; all that point to allowing for the Sacketts to get their day in court and at the same time to satisfy and to vindicate Congress's intent. Congress wanted EPA to be able to issue these -- these compliance orders. Congress gave significant statutory penalties for violating these compliance orders. But at the same time, there has to be balance. One cannot tell landowners --

[0:21:40.300] JUSTICE SCALIA: Of course, you know, you're -- you're not going to be out of the woods. Even if you get this APA review, okay, some of the factual questions that go to whether these are wetlands or not are going to be decided giving substantial deference to the agency's determination of the facts, right?

[0:22:01.240] MR. SCHIFF: No, that is correct, Justice Scalia. And that --

[0:22:02.940] JUSTICE SCALIA: And so, even if you lose on that, you might still think you can win when the EPA finally brings a -- a civil action seeking to impose a penalty, where the burden will be on the EPA without -- without any deference to its factfinding. So, you still won't know where you are, will you?

[0:22:25.480] MR. SCHIFF: Well --

[0:22:26.580] JUSTICE SCALIA: You've lost one, but you may win the other. You'll have to roll the dice.

[0:22:30.140] MR. SCHIFF: Well, respectfully, Justice Scalia, it's more than rolling the dice. It's subjecting the -- the Sacketts to an interminable Damoclean sword, if -- if the only way they can get review is simply waiting, well, when will EPA let the sword drop and bring a civil action to enforce this compliance order that who knows how old it is? With EPA's theory of continuing violation, the statute of limitations never even runs. And so, you have the Sacketts who are forever subject to this cloud over themselves, cloud over their title. They can't get anyone to come

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 21, 2012.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2011/10-1062
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2011/10-1062/20120321o_10-1062.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.6 MB)
- Length: 0:06:23.190 (383.190 s)
- Words: 829, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (2
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 800 of Whisper's 829 words (96.5%; Oyez has 829).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:01.500 | 0:00:06.540 | 11 |
| JUSTICE SCALIA | 0:00:07.440 | 0:06:22.520 | 810 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:01.500 to 0:03:01.500, with each speaker's start time.

[0:00:01.500] CHIEF JUSTICE ROBERTS: Justice Scalia has our opinion in Case 10-1062, Sackett v. EPA.

[0:00:07.440] JUSTICE SCALIA: Scalia. I'm tired already. This case is here on writ of certiorari at the United States Court of Appeals for the Ninth Circuit. The Clean Water Act prohibits, quote, the discharge of any pollutant by any person, close quote, into navigable waters, which the Act defines as, quote, the waters, the waters of the United States, close quote. If the Environmental Protection Agency determines that a violation has occurred, it may then either issue a compliance order or initiate a civil enforcement action. If the agency initiates a civil enforcement action and wins, the resulting civil penalty may not exceed $37,500 per day for each violation. But at least as the government tells it, that amount doubles to $75,000 per day when the EPA initiates and wins a civil enforcement action after a person has failed to comply with a compliance order. Michael and Chantelle Sackett, the petitioners here, own a two-thirds-acre residential lot in Bonner County, Idaho. The property lies just north of Priest Lake, but is separated from the lake by several lots with permanent structures on them. In preparation for building a house, the Sacketts filled in part of their lot with rock and dirt. Some months later, they received a compliance order from the EPA, which stated that their residential lot contained navigable waters and that their construction project violated the Act. The compliance order directed them not only to stop filling the lot, but also to restore the lot to its preconstruction condition. And, the agency said, for every day the Sacketts failed to comply, they exposed themselves to an additional $75,000 in potential liability. The Sacketts, who did not believe that their land contained navigable waters, having never seen a ship or other vessel cross their yard, sought declaratory and injunctive relief in the Federal District Court. They argued that the compliance order was arbitrary and capricious under the Administrative Procedure Act. And that it deprived them of due process in violation of the Fifth Amendment. The district court dismissed the claims for want of subject matter jurisdiction, and the Ninth Circuit affirmed. The court of appeals held that the Clean Water Act precluded

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:07.440 | Scalia. | (nothing) |
| 0:00:11.640 | (nothing) | [Laughter] |
| 0:00:13.880 | at | to |
| 0:01:20.180 | a | the |
| 0:01:23.420 | Chantelle | Chantell |
| 0:02:16.500 | exposed | expose |
| 0:02:33.160 | (nothing) | [Laughter] |
| 0:02:40.220 | argued | argue |
| 0:02:52.180 | The | (nothing) |
| 0:03:50.400 | consequences | consequence is |
| 0:03:51.620 | (nothing) | a |
| 0:04:05.220 | (nothing) | -- a permit |
| 0:04:17.100 | (nothing) | the -- |
| 0:05:06.480 | (nothing) | Army |
| 0:05:13.320 | (nothing) | -- is |
| 0:05:15.700 | (nothing) | They -- |
| 0:06:05.420 | is | it |
