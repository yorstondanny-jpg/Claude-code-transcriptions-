# sackett-wetland: Supreme Court No. 21-454

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2022/21-454
- Audio: https://www.supremecourt.gov/media/audio/mp3files/21-454.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/21-454_m5n0.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 28 min on 4 CPU cores
- Audio length: 1:48:05.088 (6485.088 s)
- `audio/argument.mp3`: mono, 64 kbps, 51.9 MB
- Official words: 7623 (plus 2 `(Laughter.)` markers), in 195 speaker turns
- ASR words: 7392
- Official words matched to an ASR word: 7199 of 7623 (**94.44%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.44% (threshold 85%).

238 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 21-454 2022 sackett-wetland --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-44.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:44:29.541 | 2669.541 | small | 1.00 | 0.00 | 5.6 | 9.0 | no surface connection, there cannot be any plausible argument that the wetland itself is -- is inseparably bound up with an abutting water. So your answer is no. Okay. Thank you. |
| 2 | 1:17:04.061 | 4624.061 | under speech | 0.18 | 0.00 | - | - | again, when we start to talk about miles, that sounds too far to be adjacent -- to reasonably be proximate to me. One mile? Again, I see where this is headed. |

## Petitioner's opening, first 3 minutes

Everything said from 0:39:30.721 to 0:42:30.721, official wording, with each turn's start time. Interruptions from the bench are included.

[0:39:30.721] MR. SCHIFF: why something like the significant nexus test is so problematic. It's hard to imagine any other statutory system in -- in the federal code that requires a potentially regulated party to initiate a rather expensive and time-consuming process just to find out whether, in fact, one is regulated. And that's precisely why the jurisdictional determination process has been developed in the -- the age of the significant nexus, because it is a test that's very difficult to know whether, in fact, one is regulated.

[0:39:58.341] JUSTICE SOTOMAYOR: Well, that test applies, as I mentioned, only to connections that are not directly with waters. That's a different issue. But that's not how we've been -- that's not how you briefed this case or what we're looking for. We're looking for a definition that has to do with a -- a connection that exists with traditional navigable waters. We may have to develop, as was the insight of Justice Kennedy in Rapanos, a different test like the significant nexus test for those connections, like here, where there might be a tributary somewhere else.

[0:40:38.501] MR. SCHIFF: Justice Sotomayor, I would say that if the test is subsurface connections to a traditional navigable water, I guarantee you that this case or something like it will be back here in another 16 years and we will be back in the same place that we have been with property owners not knowing whether they're regulated, with the states not knowing what test to apply --

[0:40:57.281] JUSTICE SOTOMAYOR: That's assuming it's sub -- sub -- subsurface water is not differentiated between groundwater.

[0:41:05.361] MR. SCHIFF: Justice Sotomayor, again, I don't think that there is certainly a legal distinction that EPA has ever articulated between the two. And, moreover, I think, as a practical matter to the property owner, if it's subsurface, it doesn't necessarily follow that one standing in a marsh -- the Sacketts' property certainly wasn't a marsh, and there's no reason that --

[0:41:22.981] JUSTICE SOTOMAYOR: Only because they put gravel in it.

[0:41:24.741] MR. SCHIFF: I -- I'm sorry, Your Honor?

[0:41:25.841] JUSTICE SOTOMAYOR: Only because they put gravel in it.

[0:41:28.061] MR. SCHIFF: Well, the original state of the property was, before the -- the -- the -- the top soil was taken out and the gravel was put on it, it looked like a -- a buildable lot. In fact, it was zoned as a buildable lot. It has a sewer hookup. It has an address. Neighbors around that property have built. There was -- there's no sense that this property is something that one might think, ah, there's water somehow flowing underneath, that that connects it to Priest Lake. That's not the type of topography.

[0:41:56.301] CHIEF JUSTICE ROBERTS: Thank you, counsel. Justice Kagan?

[0:41:58.641] JUSTICE KAGAN: Mr. Schiff, do you think there's any third position? I mean, I -- I understand that you don't like the significant nexus test, but I'm going back really to Justice Kavanaugh's point about, you know, take something like you just create a dam so that -- and the dam breaks up any idea that there is a continuous surface connection. So, if I think, well, in that kind of situation, it just -- it just can't -- you -- you can't be right, but I also understand some of your points about the significant nexus test, is there anything in the

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 25, 2023.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2022/21-454
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2022/21-454/21-454_20230525-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 2.2 MB)
- Length: 0:01:50.448 (110.448 s)
- Words: 238, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 232 of Whisper's 238 words (97.5%; Oyez has 235).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.860 | 14 |
| JUSTICE ALITO | 0:00:07.640 | 0:01:48.660 | 223 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Alito has our opinion in case 21-454, Sackett versus the Environmental Protection Agency.

[0:00:07.640] JUSTICE ALITO: This case involves the outer reaches of the Clean Water Act. The Clean Water Act applies to, quote, navigable waters, which it defines as, quote, the waters of the United States. The Environmental Protection Agency asserted jurisdiction over Michael and Chantelle Sackett's lot near a lake in Idaho because the agency believes that the property contains wetlands and constitutes part of the waters of the United States. The Sacketts disagreed, and they sued to preclude enforcement. After seven years of litigation, which included a prior trip to this court, the District Court eventually entered summary judgment in favor of the EPA, and the Ninth Circuit affirmed. For the reasons explained in our opinion, we agree with the Sacketts, and therefore reverse. We hold that the waters of the United States encompass only those relatively permanent standing or continuously flowing bodies of water, forming geographical features that are described in ordinary speech as streams, oceans, rivers, and lakes. The opinion of the court is joined in full by the Chief Justice and Justices Thomas, Gorsuch, and Barrett. Justice Thomas has filed a concurring opinion, which Justice Gorsuch has joined. Justice Kagan has filed an opinion concurring in the judgment, which Justices Sotomayor and Jackson have joined. Justice Kavanaugh has filed an opinion concurring in the judgment, which Justices Sotomayor, Kagan, and Jackson have joined.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:27.000 | Chantelle | Chantall |
| 0:00:28.360 | lot | slot |
