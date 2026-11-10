# sutton-glasses: Supreme Court No. 97-1943

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/1998/97-1943/19990428a_97-1943.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/1998/97-1943_04-28-1999.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 45 min on 4 CPU cores
- Audio length: 0:59:39.638 (3579.638 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.7 MB
- Official words: 10793 (plus 11 `(Laughter.)` markers), in 368 speaker turns
- ASR words: 10366
- Official words matched to an ASR word: 9950 of 10793 (**92.19%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.19% (threshold 85%).

554 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 10 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 97-1943 1998 sutton-glasses --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/1998/97-1943_04-28-1999.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/1998/97-1943/19990428a_97-1943.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.0 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:09:12.380 | 552.380 | big | 1.96 | 1.05 | 23.7 | 30.3 | person with normal eyesight can do. Well, but -- there again, I don't know where that gets us to draw the line. I have difficulty reading restaurant checks in dim light. |
| 2 | 0:09:31.420 | 571.420 | big | 2.66 | 2.30 | 24.5 | 32.5 | some circumstances I have difficulty. Substantial? That is a limitation. It's certainly not a substantial limitation. Why not? FOURTEENTH STREET, N.W. •202,289-2260 Well, on a case-by-case -- The waiter thinks so. |
| 3 | 0:15:18.920 | 918.920 | under speech | 0.16 | 0.00 | - | - | what -- what is the phrase that's used in connection with the regarded as clause? Because of myths and shibboleths? No, it isn't shibboleths. What -- there's -- Stereotypes. Stereotypes is the word. |
| 4 | 0:22:17.320 | 1337.320 | small | 0.50 | 0.00 | 4.0 | 6.1 | worrying is if you say it should be uncorrected. Yes. And then you read out of the statute people who have glasses like this. I borrowed them from Justice Scalia. |
| 5 | 0:22:21.180 | 1341.180 | under speech | 0.00 | 0.00 | - | - | you read out of the statute people who have glasses like this. I borrowed them from Justice Scalia. But I need them too. That's not true. I need them too. |
| 6 | 0:25:39.790 | 1539.790 | under speech | 0.00 | 0.00 | - | - | that's ridiculous. Well, first of all, in that example, I think the manager is going to choose the person who hits the best and not who has the best eyesight. |
| 7 | 0:25:45.110 | 1545.110 | medium | 0.68 | 0.50 | 20.8 | 23.0 | the best and not who has the best eyesight. No. This is a manner -- this is a manager who plays the odds. It's when Ted was on the way up. |
| 8 | 0:36:36.370 | 2196.370 | big | 5.16 | 4.95 | 29.7 | 35.3 | of General Electric? It predated Chevron. I don't know the exact date. Yes. I mean, that's old, old stuff. I don't even know Skidmore deference anymore. It's not that old. |
| 9 | 0:44:26.030 | 2666.030 | small | 0.47 | 0.00 | 10.2 | 11.6 | limb actually has no substantial limitation in any major life activity, none at all, I would -- Supposing I have an artificial finger and he's afraid I can't honk the horn. |
| 10 | 0:45:15.610 | 2715.610 | under speech | 0.00 | 0.00 | - | - | of course, regarded them in their uncorrected state. No. I think it's sort of a metaphysical statement. United -- Well, this whole act is metaphysical. We've been here for 2 days. |
| 11 | 0:49:46.670 | 2986.670 | small | 0.62 | 0.00 | 0.6 | 2.9 | Scalia, my position is broader than that. 202:239-2260 But what if all -- all professional football -- all professional football leagues thought he was too short? Then he could be a coach. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:11.780 to 0:03:11.780, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:11.780] MR. HUGHES: Mr. Chief Justice, and may it please the Court: Because this matter was decided by the lower court on a motion to dismiss, for purposes of today's argument, United cannot dispute the nature of the discrimination that occurred here. Petitioners have gone to great lengths to make themselves eminently qualified to fill the piloting positions at issue here, but were excluded from those positions by United based not upon their actual abilities, but based only upon its preconceived notion of what a person who shares their impairment can and cannot do. Now, United contends that even if it discriminated in just this manner, it cannot be liable under the Americans with Disabilities Act because, as a matter of law, the ADA can never protect one with severe but correctable myopia. *2 02.z 3 9 - 22 60 United's intuition that myopia is somehow distinct from other correctable impairments does not withstand serious scrutiny. Petitioners here are actually disabled within the meaning of the ADA or, at a minimum, they were regarded as disabled with respect to the ability to work by United.

[0:01:10.140] QUESTION: Is that raised in your petition for certiorari, whether they were regarded as disabled?

[0:01:15.420] MR. HUGHES: Yes, Your Honor, it is.

[0:01:16.340] QUESTION: Whereabouts?

[0:01:16.840] MR. HUGHES: The -- I believe it was the third question presented in our petition, read as followed: Is a commercial pilot regarded as disabled by a major airline that refuses to employ her as a pilot for that airline due to her poor vision?

[0:01:34.040] QUESTION: As far as actual disability is concerned, let me ask the same question that -- that we put to counsel yesterday. If myopia, correctable myopia, which requires nothing more than eyeglasses, is included within the definition of disability, how do you account for the fact that the act itself estimates there are some 43 million disabled people in America?

[0:02:00.800] MR. HUGHES: Justice --

[0:02:01.960] QUESTION: There would be many, many, many more than that if - - if you are counting people who have to v 2 02/289-2260 wear eyeglasses.

[0:02:08.100] MR. HUGHES: I agree, Justice Scalia, that there are more than 43 million Americans who wear glasses. It has never been our position that the mere fact of wearing glasses or, indeed, the mere use of any corrective measure is in itself a disability. Our position is that Congress intended not to identify bright line categories of what are and are not disabilities, but rather to require courts to evaluate the severity of each person's impairment on a case-by-case basis.

[0:02:33.380] QUESTION: How do you find in the text of the statute?

[0:02:33.500] QUESTION: Where do you get that in the statute?

[0:02:36.040] MR. HUGHES: The statute --

[0:02:36.540] QUESTION: It's a nice idea. Maybe they could have done that. How did they do it here?

[0:02:41.000] MR. HUGHES: The statute requires that -- that each impairment be substantially limiting with respect to a major life activity, and moreover, the definition requires a substantial limitation of the major life activities of such individual. I read that as not requiring the court to define each impairment and state each impairment in every case is a disability or is not a disability. That's a different approach that Congress could have followed, but Congress didn't follow that -- 202 289-2260 that approach. Congress required each person's impairment to -- to be evaluated.

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 22, 1999.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/1998/97-1943
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/1998/97-1943/19990622o_97-1943.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.5 MB)
- Length: 0:05:47.690 (347.690 s)
- Words: 787, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 759 of Whisper's 787 words (96.4%; Oyez has 781).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE REHNQUIST | 0:00:00.000 | 0:00:04.340 | 15 |
| JUSTICE O'CONNOR | 0:00:05.240 | 0:05:47.240 | 770 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE REHNQUIST: The opinions of the Court in three cases will be announced by Justice O 'Connor.

[0:00:05.240] JUSTICE O'CONNOR: The first of these is another Americans with Disabilities Act case, Sutton v. United Airlines. The case comes to us on writ of certiorari to the United States Court of Appeals for the Tenth Circuit. In 1990, Congress passed the Americans with Disabilities Act, which several of us have been referring to this morning as the ADA. It prohibits certain employers from discriminating against individuals on the basis of their disabilities. This case concerns the meaning of the term disability, as it's used in the Act. The ADA defines the term to mean, among other things, a physical or mental impairment that substantially limits one or more major life activities or being regarded as having such an impairment. Consequently, individuals have disabilities within the meaning of the ADA if they have actual substantially limiting impairments or are regarded as having such. The petitioners here are twin sisters, both of whom have severe myopia. With the use of corrective measures such as glasses or contact lenses, both have 20-20 vision. In 1992, they applied to the Respondent, a major commercial airline, for employment as commercial airline pilots. The Respondent invited them to an interview, but during their interviews, both petitioners were told they could not work as pilots with United Airlines because they could not meet the Respondent's minimum vision requirement, which is uncorrected visual acuity of 20 over 100 or better. Subsequently, the petitioners filed a complaint claiming that the Respondent discriminated against them on the basis of their actual disability, their poor eyesight. Alternatively, the petitioners claimed they were discriminated against on the basis of a disability they didn't have but were regarded as having. The district court dismissed the complaint for failure to state a claim on which relief could be granted. The United States Court of Appeals for the Tenth Circuit affirmed, and in an opinion filed with the court today, with the clerk today, we also affirm, we hold that whether an individual is actually disabled should be made with reference to any measures that the individual uses to mitigate. Three separate provisions of the ADA read in concert lead us to this conclusion. First, because the ADA's definition of disability is phrased in the present indicative, the definition should be read as requiring that a person be presently, not potentially or hypothetically, substantially limited in order

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:25.600 | of us | others |
| 0:00:40.040 | it's | it has |
| 0:00:43.860 | mean, | me |
| 0:01:50.180 | 20 over 100 | 20/100 |
| 0:02:05.380 | claimed | claim |
| 0:02:24.160 | court today, with the | (nothing) |
| 0:02:38.800 | (nothing) | the impairment. |
| 0:02:48.280 | is | as |
| 0:03:05.280 | that | the |
| 0:03:15.460 | being | (nothing) |
| 0:03:35.020 | (nothing) | a |
| 0:04:16.980 | allege | alleged |
| 0:05:12.840 | them as | and is |
| 0:05:31.420 | allege | alleged |
| 0:05:35.580 | pilots, | pilot, |
