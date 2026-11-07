# arvizu-wave: Supreme Court No. 00-1519

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2001/00-1519/20011127a_00-1519.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2001/00-1519.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 41 min on 4 CPU cores
- Audio length: 0:56:59.063 (3419.063 s)
- `audio/argument.mp3`: mono, 64 kbps, 27.4 MB
- Official words: 9755 (plus 11 `(Laughter.)` markers), in 209 speaker turns
- ASR words: 9568
- Official words matched to an ASR word: 9237 of 9755 (**94.69%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.69% (threshold 85%).

288 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 6 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 21 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 00-1519 2001 arvizu-wave --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2001/00-1519.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2001/00-1519/20011127a_00-1519.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-44.7 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:06:20.600 | 380.600 | big | 1.28 | 1.15 | 21.4 | 31.5 | limit. That sounds a lot more reasonable then. I mean, gee, if you don't slow down to the speed limit when you see a police car, you're in big trouble. |
| 2 | 0:06:34.260 | 394.260 | under speech | 0.00 | 0.00 | - | - | was not common in the area, and it -- You mean they just keep zipping along at 50 despite seeing a police car. What part of the country is this anyway? |
| 3 | 0:06:37.140 | 397.140 | big | 4.00 | 3.65 | 25.0 | 36.2 | common in the area, and it -- You mean they just keep zipping along at 50 despite seeing a police car. What part of the country is this anyway? It's Arizona. |
| 4 | 0:13:29.590 | 809.590 | under speech | 0.00 | 0.00 | - | - | what about, you know, not -- not waving to the police car as you go by? I don't know when I -- if I were ever exceeding the speed limit and saw -- |
| 5 | 0:13:42.070 | 822.070 | medium | 0.84 | 0.70 | 24.2 | 29.6 | saw a police car, it seems to me I would slow down and -- and try to give the impression that I wasn't slowing down because I saw the police car. |
| 6 | 0:13:45.470 | 825.470 | big | 1.22 | 1.05 | 30.1 | 37.6 | to give the impression that I wasn't slowing down because I saw the police car. I mean, you know, you don't hit the brake and wave at the police officer. |
| 7 | 0:30:02.270 | 1802.270 | big | 1.68 | 1.15 | 21.7 | 29.7 | the -- of the vast desert of Arizona for people to go barreling along at 50 miles an hour past a Border Patrol agent and ordinarily to wave and say hi. |
| 8 | 0:33:34.850 | 2014.850 | small | 1.02 | 0.30 | 19.6 | 28.3 | kind of wave it was? What -- what he says in his testimony is they kind of stuck their hands up and began waving to me like this. Well, I'm sorry. |
| 9 | 0:41:18.550 | 2478.550 | under speech | 0.00 | 0.00 | - | - | was a rehearing in this case, they amended the opinion to add under the circumstances of this case and in this case on many, many times. Maybe not often enough. |
| 10 | 0:48:59.830 | 2939.830 | medium | 2.38 | 1.65 | 18.4 | 28.8 | doesn't -- you know, not everybody is a smuggler in such an area. They drive with their family just for recreation 50 miles out of the way. Their children wave oddly. |
| 11 | 0:54:31.350 | 3271.350 | small | 0.36 | 0.00 | 4.9 | 6.9 | Court has further questions, we submit that the judgment of the court of appeals should be reversed. Tell me. Explain to me again why the shift change is so significant. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:10.840 to 0:03:10.840, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:10.840] MR. SCHLICK: Mr. Chief Justice, and may it please the Court: Since Terry, this Court has held repeatedly that reasonable suspicion analysis requires a common sense evaluation of the totality of the circumstances. The decision below is fundamentally inconsistent with that rule because it requires law enforcement officers to disregard potentially relevant facts when determining whether investigative stop is warranted. This Court's decisions in Cortez and Sokolow are especially clear in rejecting attempts to put categories of facts off limits. In Cortez, the Court held that a vehicle's route, the timing of its trip, and its capacity for carrying illegal aliens together established reasonable suspicion, notwithstanding that each of those facts independently might be consistent with innocent travel. In Sokolow, the Court rejected a rule that would have limited officers' ability to consider the personal characteristics of suspected drug smugglers. The Court held that that sort of rule adds to the difficulty of applying the reasonable suspicion standard. It does not ease it. And the Court further confirmed that innocent facts, facts consistent with innocent travel, in themselves may together establish reasonable suspicion. In this case, the Ninth Circuit attempted to establish a rule that would bar categorically consideration of certain facts that the court deemed innocent. That -- that rule presents two fundamental problems. The first is that it doesn't accommodate the subtleties of real world encounters. For every categorical rule, there would have to be exceptions and subrules, and even if law enforcement officers could be asked to master those, they would still then have to anticipate new situations, and those rules could not provide guidance when --

[0:01:52.080] QUESTION: Mr. Schlick, you said this is an area in which one can use one's common sense, and I thought that what the Ninth Circuit was telling us was that some items in that list under all circumstances wouldn't cast suspicion. And one was -- had a certain familiar ring with me that when you see a police car, you slow down. This wasn't a car that came to a screeching halt or was trying to dodge it, and then it just slowed down. And isn't that a most natural reaction?

[0:02:26.660] MR. SCHLICK: The problem, Justice Ginsburg, was that the Ninth Circuit didn't admit of situations in which deceleration might be relevant. For example, in the Fifth Circuit's Villalobos case, which we cited in our brief, the law enforcement officer pulled in front of the vehicle that was suspected. The vehicle then slowed to drop back away from the law enforcement officer vehicle, and the Border Patrol officer in that case deemed that suspicious, that it appeared that the vehicle had changed its speed in order to increase its distance from the law --

[0:02:53.700] QUESTION: But they weren't talking about that case. They were talking about this case. And I thought what they were saying was that there was nothing suspicious about the slowdown here, and if that's all that you have, it won't do.

[0:03:10.160] MR. SCHLICK: Justice Ginsburg,

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 15, 2002.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2001/00-1519
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2001/00-1519/20020115o_00-1519.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.9 MB)
- Length: 0:03:30.390 (210.390 s)
- Words: 517, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (1 turn), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 482 of Whisper's 517 words (93.2%; Oyez has 520).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE REHNQUIST | 0:00:00.000 | 0:03:29.920 | 516 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE REHNQUIST: I have the opinion of the Court to announce a number 001519, United States v. Arvizu. On a January afternoon four years ago, Border Patrol agent Clinton Stoddard was working at a checkpoint along U .S. Highway 191, about 30 miles north of Douglas, Arizona, which lies on the United States-Mexico border. At the checkpoint, Border Patrol agents stopped cars to look for illegal immigration and smuggling. Smugglers tried to avoid the checkpoint by taking unpaved and primitive back roads around it. Stoddard received a report that a sensor placed along a back road had been triggered, indicating that a vehicle might be following a common smuggling route through a thinly populated area between the highway and a national forest. He drove to investigate and saw respondent's minivan. It slowed dramatically. Respondent who was driving appeared stiff and nervous. Three children were inside. The position of the children's feet in the back seat suggested cargo on the floor. Stoddard followed the minivan and learned that it was registered to a Douglas neighborhood notorious for smuggling. After the minivan turned away from known recreational areas and took the last turn to avoid the checkpoint, Stoddard decided to stop it. A vehicle search uncovered 128 pounds of marijuana, some of it concealed in a duffel bag beneath the children's feet. Respondent was charged with possession with intent to distribute marijuana. He moved to suppress the evidence of the drugs, arguing that the stop was not supported by reasonable suspicion as required by the Fourth Amendment. The District Court ruled against him, but the Court of Appeals for the Ninth Circuit reversed. In an opinion filed with the Clerk of the Court today, we reversed the Court of Appeals. In its opinion, the Court of Appeals set out to clearly delimit the factors an officer can consider in making stops like the one involved here. It held that seven factors, including respondents slowing down, were simply out of bounds in deciding whether there was reasonable suspicion and that the remaining factors did not satisfy the Fourth Amendment. This methodology is totally contrary to our prior decisions. In cases such as Cortez v. United States, we have said that reviewing courts should make reasonable suspicion determination by looking at the totality of the circumstances of each case to see whether the detaining officer has a particularized and objective basis for suspecting legal wrongdoing. This standard allows officers to draw on their own experience and training to make inferences from the cumulative information before them. It isn't reducible to a neat set of rules. In United States v. Socolow, we rejected a holding by the Court of Appeals that sought to

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.660 | a number | in NO. |
| 0:00:13.600 | at | on |
| 0:00:25.780 | stopped | stop |
| 0:00:30.420 | tried | try |
| 0:00:35.220 | it. | them. |
| 0:00:39.380 | a | the |
| 0:00:56.700 | (nothing) | The |
| 0:01:19.520 | checkpoint, | checkpoints, |
| 0:01:28.160 | in | on |
| 0:01:40.720 | (nothing) | any |
| 0:01:49.860 | (nothing) | And |
| 0:01:49.980 | an | (nothing) |
| 0:01:50.440 | filed | followed |
| 0:01:52.320 | reversed | reverse |
| 0:01:58.720 | officer | officers |
| 0:02:03.840 | that | at |
| 0:02:14.300 | did | do |
| 0:02:25.780 | said | siad |
| 0:02:26.100 | (nothing) | the |
| 0:02:26.480 | courts | court |
| 0:02:51.180 | isn't reducible | is irreducible |
| 0:02:55.640 | v. Socolow, | versus Sokolow |
| 0:03:06.880 | fares | fairs |
| 0:03:17.420 | in | on |
| 0:03:23.220 | the | to |
