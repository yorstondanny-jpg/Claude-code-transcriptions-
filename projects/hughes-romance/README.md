# hughes-romance: Supreme Court No. 17-155

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/17-155
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-155.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/17-155_g314.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 19 min on 4 CPU cores
- Audio length: 0:52:24.168 (3144.168 s)
- `audio/argument.mp3`: mono, 64 kbps, 25.2 MB
- Official words: 9052 (plus 4 `(Laughter.)` markers), in 162 speaker turns
- ASR words: 8867
- Official words matched to an ASR word: 8597 of 9052 (**94.97%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.97% (threshold 85%).

264 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 21 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-155 2017 hughes-romance --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.0 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:31:14.980 | 1874.980 | big | 2.10 | 1.35 | 20.0 | 24.0 | us that over time. So, if you ask me to write something better than Marks, I don't know what to say, except what I just said, which will help nobody. |
| 2 | 0:31:25.840 | 1885.840 | under speech | 0.00 | 0.00 | - | - | are in need of guidance on in this case -- Well, what guidance? Yes. So -- I mean, what? Sure. You talk about the French movie. That was great -- I mean fine. |
| 3 | 0:31:31.880 | 1891.880 | small | 0.38 | 0.25 | 30.4 | 35.4 | about the French movie. That was great -- I mean fine. There I say, you mean they really don't want to see The Philadelphia Story? They must be crazy. All right. |
| 4 | 0:31:45.460 | 1905.460 | small | 0.46 | 0.30 | 29.5 | 34.7 | you have, of course, a real French comedy, fine. But suppose you have -- to show off -- Mr. Hulot's Holiday, you know, it's a comedy, but is it romantic, you see. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.660 to 0:03:06.660, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.660] MR. SHUMSKY: Mr. Chief Justice, and may it please the Court: The plurality and the concurrence in Freeman recognized two ways that a sentence following a C-type agreement can be based on the guidelines. Both are correct. Now those opinions differed in their reasoning, such that Freeman itself has no precedential effect under Marks, but the two approaches can be united under a common umbrella, namely, long-standing principles of proximate and multiple causation. And that's because each form of guidelines reliance bears a close connection to the sentence. The first --

[0:00:44.400] JUSTICE SOTOMAYOR: Mr. Shumsky, could you address one issue for me on this question? In a (C) agreement, the government is giving up, often, certain things. Sometimes they dismiss additional charges. Sometimes, as here, they give up filing a persistent felony certificate. Sometimes they agree not to prosecute someone important to the defendant. There are many things that go into that bargain. How is a district court judge to determine whether a departure from the guideline range is justified? In what circumstances is what the government given up valuable enough to keep the original deal and when is it not?

[0:01:38.440] MR. SHUMSKY: Justice Sotomayor, let me answer the question in two parts if I can. First of all, those conditions, the way Your Honor describes C-type agreements, are true also for B-type agreements and for the sort of C-type agreements that the government concedes open the door to eligibility for relief under 3582(c)(2). So this particular category of C-type agreement that the government is proposing to carve out is not different in that way than all of these other categories of agreements. This --

[0:02:12.880] JUSTICE SOTOMAYOR: Except that -- let's take -- dismissing charges, I -- I think it could be seen as relatively easy. How different were the charges and the exposure from what was kept and what was the strength of the government's evidence? And the government could talk about that at sentencing on those charges. But the persistent felony offender certificate is a different judgment, which is: I, the government, think that a sentence of X amount justifies giving up that certificate. How would a district court make up for the loss of that belief by the government?

[0:02:54.200] MR. SHUMSKY: Well, so -- Justice Sotomayor, let me push back a little bit still --

[0:02:57.100] JUSTICE SOTOMAYOR: Okay.

[0:02:57.100] MR. SHUMSKY: -- on the first part of my answer and then -- and then get to the second part. Again, that's no different than in a C-type agreement in which there is a range

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 04, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/17-155
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/17-155/17-155_20180604-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.1 MB)
- Length: 0:04:20.598 (260.598 s)
- Words: 667, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 627 of Whisper's 667 words (94.0%; Oyez has 654).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.680 | 15 |
| JUSTICE KENNEDY | 0:00:08.020 | 0:04:19.680 | 650 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kennedy has the opinion of the court in Case 17-155, Hughes v. United States.

[0:00:08.020] JUSTICE KENNEDY: A Federal statute provides that in certain instances a prisoner who is serving a sentence is eligible for a sentence reduction when the Sentencing Commission has lowered the sentencing guidelines. The eligibility extends to a prisoner who has been sentenced to a term of imprisonment based on a sentencing range that has subsequently been lowered by the Sentencing Commission, and that statute is 18 U .S .C. Section 3582C2. The question here is whether the sentence imposed on the prisoner in this case was based on the guidelines when he enters his guilty plea under an agreement with the prosecution that is called a Type C plea agreement. And that's where the defendant and the government agree that the defendant will plead guilty and then serve a particular sentence, and the Type C agreement that they agree on must be then approved by the trial judge. Seven terms ago, in Freeman v. United States, this Court considered the same question that's involved here. That is, whether the sentence under a Type C agreement is based on the guidelines. In Freeman, no single interpretation or rationale commanded a majority of this Court. Now, Marx v. United States was the case decided in 1977, and Marx discussed what other courts should do when this Court has separate opinions addressing an issue, but when no single rationale commands a majority. So when confronted with the separate opinions on the sentencing question presented in Freeman, various courts of appeals consulted Marx to determine which Freeman opinion to follow, and they reached different conclusions. And in today's case, the Court had asked the parties to address the Marx question as a threshold issue. After consideration of the sentencing issue first discussed in Freeman, and now presented again here, the Court in today's case now has a majority with respect to that substantive sentencing issue. So it's unnecessary to discuss how Marx should be interpreted. The Court holds that a defendant who entered a Type C agreement is eligible for a sentence reduction under 3582c so long as the defendant's sentencing range was part of the framework the district court used in imposing the sentence or accepting the agreement. In the typical sentencing case, there will be no question that the defendant's guideline range was a basis for its sentence, for the guidelines are the starting point for every sentencing calculation in the Federal system. A sentence imposed pursuant to a Type C agreement is no exception to this general rule, although the government and the defendant may agree to a specific sentence. That bargain is contingent on the district courts accepting the agreement, and the guidelines prohibit courts

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:02:37.820-0:02:37.980: "but"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:30.700 | U .S .C. Section | U.S.C. |
| 0:00:42.400 | enters | entered |
| 0:01:10.700 | that's | that is |
| 0:01:13.100 | a Type C | Type-C |
| 0:01:24.060 | Marx | Marks |
| 0:01:25.260 | the | a |
| 0:01:27.540 | Marx | Marks |
| 0:01:30.120 | courts | court |
| 0:01:45.980 | Marx | Marks |
| 0:01:53.900 | Marx | Marks |
| 0:02:11.340 | Marx | Marks |
| 0:02:17.760 | a | (nothing) |
| 0:02:27.680 | the | a |
| 0:02:34.580 | that | of |
| 0:02:36.920 | its | his |
| 0:03:08.340 | the | a |
| 0:03:16.220 | purposes | purpose |
| 0:03:33.860 | Hughes's Type C | Hughes' Type-C |
| 0:03:59.680 | Hughes's | Hughes' |
