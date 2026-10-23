# prado-navarette: Supreme Court No. 12-9490

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2013/12-9490
- Audio: https://www.supremecourt.gov/media/audio/mp3files/12-9490.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2013/12-9490_p8k0.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 45 min on 4 CPU cores
- Audio length: 1:02:05.662 (3725.662 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.8 MB
- Official words: 11245 (plus 6 `(Laughter.)` markers), in 291 speaker turns
- ASR words: 11091
- Official words matched to an ASR word: 10625 of 11245 (**94.49%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.49% (threshold 85%).

374 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 7 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 24 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 12-9490 2013 prado-navarette --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-48.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:18:58.960 | 1138.960 | medium | 0.60 | 0.45 | 16.3 | 19.0 | just the -- the seriousness of the claim should not affect whether there is, in fact, reasonable suspicion. You get an A for consistency. I'm -- I'm not sure about common sense. |
| 2 | 0:23:29.420 | 1409.420 | small | 0.54 | 0.20 | 15.0 | 21.8 | More than that, I want you to say the Court shouldn't. Let the car go. Bye-bye, Los Angeles. In this case, your -- your grade for consistency depends on this answer. |
| 3 | 0:24:25.520 | 1465.520 | under speech | 0.16 | 0.00 | - | - | But, Your Honor, the -- the idea of running off the road is concealed -- Even if the person weren't drunk, I think it's illegal to run someone else off the road. |
| 4 | 0:33:41.840 | 2021.840 | big | 2.82 | 2.00 | 25.5 | 37.1 | me some other instances where the courts have upheld, well, that's enough. Well, if a caller says -- I'm not saying common sense. I'm saying what the courts have held. Sorry. |
| 5 | 0:42:37.040 | 2557.040 | medium | 1.16 | 0.45 | 17.9 | 24.7 | actions. And when you're dealing with reasonable suspicion -- What about cutting me off too quickly, you know? I think that -- Cuts right in front of me. Really ticks me off. |
| 6 | 0:49:18.100 | 2958.100 | medium | 2.68 | 0.70 | 17.5 | 28.1 | I think what you're saying to me, am I correct, that almost any moving violation counts? Changing a lane without a signal, which seems to be endemic in Washington, but -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.480 to 0:03:06.480, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.480] MR. KLEVEN: Mr. Chief Justice, and may it please the Court: In this case, the Court should hold that officers acting on anonymous tips must corroborate the tips' assertions of illegal conduct, as well as the identifying details before making a stop, whether that tip involves erratic driving, illegal gun possession, or any other allegation of misconduct. Now, the State proposes that the reasonable suspicion rule in-- established in Terry v. Ohio, which courts and law enforcement officials have been applying now for more than 40 years, should be altered so that, now, it applies as a sliding scale where the level of suspicion varies depending on the nature of the crime that an anonymous tipster claims someone has committed.

[0:00:53.120] CHIEF JUSTICE ROBERTS: So if the tip -- so if the tip is, is this car is driving by and throwing bombs out the window, okay, every -- you know, whatever, 500 yards, the police find the car, they have to wait until they see the person actually throw a bomb out the window themselves, before pulling them over?

[0:01:10.880] MR. KLEVEN: Well, Your Honor, in terms of the reasonable suspicion, yes. If there -- if all they have is an anonymous tip and there is no -- they have no way of corroborating any of the -- any of the innocent details, except that they can identify the car, then, yes, under --

[0:01:26.380] CHIEF JUSTICE ROBERTS: So your answer is yes, the car is going there, and he's throwing a bomb out, and it goes off, but he has to wait till he sees them throw out another bomb?

[0:01:34.580] MR. KLEVEN: Your Honor, under the Florida-J.L., the Court has said that when they are looking -- when all that they are able to corroborate are obvious reasonably observable details, such as that, then there is no basis for the Court to go beyond that -- and

[0:01:50.660] JUSTICE GINSBURG: I thought that -- that J.L. gave an example of an exception that the report is somebody is carrying a bomb?

[0:02:01.380] MR. KLEVEN: Well, there is that exception, Your Honor. And in Florida-J.L, it said that it was not -- the Court said that it was not required on the facts of that case to speculate about a situation where such a serious danger --

[0:02:14.080] JUSTICE SCALIA: Throwing bombs doesn't count, but carrying a bomb does, is that it? Were they throwing bombs that they weren't carrying?

[0:02:22.060] MR. KLEVEN: Your Honor, that would not make a difference. However, in this case, in terms of adjusting the reasonable suspicion standard, the Court should not address that. The Court has never said --

[0:02:32.360] JUSTICE ALITO: Excuse me. I'm sorry. Could I ask you what you mean by an "anonymous tip"? Suppose somebody calls up 911 and gives a name? Does that make it not an anonymous tip?

[0:02:45.460] MR. KLEVEN: Your Honor, technically, it would not be, but in the circumstances here, I think it should be treated as an anonymous tip because, again, the name could be false when the tip first comes in. If it's corroborated in some way, then --

[0:03:00.460] JUSTICE ALITO: Well, how would you corroborate it? Let's say the person calls up and gives a name and gives an address? So what would

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - April 22, 2014.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2013/12-9490
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2013/12-9490/20140422o_12-9490.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.8 MB)
- Length: 0:02:51.050 (171.050 s)
- Words: 362, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
  Oyez lists no names for 2 of these turns, so they come from the text: a turn that opens "Justice X has our opinion" is the Chief Justice introducing the case, and the next turn is Justice X.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 345 of Whisper's 362 words (95.3%; Oyez has 359).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.600 | 13 |
| JUSTICE THOMAS | 0:00:07.980 | 0:02:50.220 | 348 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Thomas has our opinion this morning in Case 12-9490, Navarette v. California.

[0:00:07.980] JUSTICE THOMAS: This case comes to us on the writ of certiorari to the California Court of Appeal. The Fourth Amendment permits brief investigative stops when an officer has a reasonable suspicion of criminal activity. Reasonable suspicion requires a particularized and objective basis for suspecting a particular person of criminal conduct. Our previous cases have recognized that under appropriate circumstances, anonymous tips can create reasonable suspicion. In this case, an anonymous 911 caller reported that a specific truck driving southbound on California Highway 1 had run the caller off the road. A California Highway Patrol officer located the truck, stopped it, and discovered 30 pounds of marijuana. Probably shouldn't carry around 30 pounds of marijuana. But Petitioners argued that there was no reasonable suspicion for the traffic stop. But the trial court denied Petitioners' motion to suppress, and California Court of Appeal affirmed. In that opinion, filed with the clerk today, we now affirm the judgment of the California Court of Appeal. We conclude that under the totality of circumstances in this case, the officer had reasonable suspicion that the driver of the truck was intoxicated. First, there were adequate reasons for an officer to believe the caller's account of being run off the road. The caller necessarily claimed eyewitness knowledge of the incident. The timeline of events suggested that the caller had little time to fabricate the report, and the caller used a 911 system which had several technological and regulatory features that deter false reports. The 911 call also created reasonable suspicion of drunk driving. Running another car off the road suggests the sort of impairment that characterizes drunk driving. That conduct bears too much resemblance to classic examples of drunk driving to be dismissed as an isolated recklessness. While there are other potential explanations for the reported behavior, we have consistently recognized that reasonable suspicion need not rule out innocent alternatives. For these reasons and others set forth in our opinion, we affirm the judgment of the California Court of Appeal. Justice Scalia has filed a dissenting opinion in which Justices Ginsburg, Sotomayor, and Kagan have joined.

### Words Whisper invented

None found.

Where Whisper's words differed from Oyez's and the re-run agreed with Oyez, the re-run's words and times replace the first pass:

- 0:00:28.380: "particular person to be authorized an" became "particularized and"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:10.020 | the | a |
| 0:00:13.300 | Appeal. | Appeals. |
| 0:00:37.580 | that | it |
| 0:00:49.520 | a | (nothing) |
| 0:01:05.280 | (nothing) | it |
| 0:01:10.860 | argued | argue |
| 0:01:22.980 | that | an |
| 0:01:26.940 | the | (nothing) |
| 0:01:46.860 | (nothing) | the |
| 0:01:50.480 | events | event |
| 0:01:56.580 | used a | use the |
| 0:02:11.360 | suggests the | suggest to |
| 0:02:22.420 | an | (nothing) |
| 0:02:40.860 | the | (nothing) |
