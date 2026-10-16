# babb-boomer: Supreme Court No. 18-882

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2019/18-882
- Audio: https://www.supremecourt.gov/media/audio/mp3files/18-882.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2019/18-882_d1o2.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 35 min on 4 CPU cores
- Audio length: 0:59:20.904 (3560.904 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.5 MB
- Official words: 10400 (plus 3 `(Laughter.)` markers), in 275 speaker turns
- ASR words: 10101
- Official words matched to an ASR word: 9770 of 10400 (**93.94%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
  Not counted: `2302(b)(1)(B),` 1677.300-1680.960 (3.66 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 93.94% (threshold 85%).

382 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 4 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 15 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 18-882 2019 babb-boomer --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-48.1 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:15:59.440 | 959.440 | under speech | 0.14 | 0.00 | - | - | in the course of the, you know, weeks' long process, you know, one comment about age, you know, the hiring person is younger, says, you know, "OK Boomer," you know -- |
| 2 | 0:23:41.300 | 1421.300 | medium | 0.72 | 0.50 | 13.6 | 15.5 | should attend to it. And -- and -- We couldn't agree -- we couldn't agree more. And I understand -- I know where you're going with that, and that's good, that's a good point -- |
| 3 | 0:38:44.500 | 2324.500 | big | 1.12 | 1.00 | 30.8 | 37.7 | person thinks I see her result on this test. It's highly subjective. I'm not sure, but I certainly don't want people who are over the age of 82, et cetera. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.600 to 0:03:09.600, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.600] MR. MARTINEZ: Mr. Chief Justice, and may it please the Court: Section 633a states that all federal personnel actions shall be made free from any discrimination based on age. Both parties agree that that language tracks the text and meaning of Title VII's identical federal sector provision covering race, sex, and religion. Together the two provisions bar discrimination not only in the ultimate outcome of a personnel decision but also in the process of making that decision. That's true regardless of whether the prohibited characteristic at issue is a but-for cause of the final decision. That's the rule that the MSPB and the EEOC have applied in countless cases for many years, but more importantly it flows directly from the statutory text. The phrase "free from any discrimination" governs how the decision shall be made. In other words, the process for making that decision. If that process uses age or race as a negative factor, it's not made free from any discrimination. Congress chose those words carefully rejecting the private sector language later addressed in Gross and Nassar. It did so in the unique federal sector context to create a remedy for violating constitutional equal protection rights. This Court has said that when a plaintiff is subjected to discrimination in the process of being considered for a government benefit, he necessarily suffers a redressable equal protection injury even if he can't prove he otherwise would have received a benefit. That same injury rule governs 633a and Title VII. That rule is fully consistent with common law principles and this Court's but-for causation analysis in other cases. The government, in this case, apparently believes it's perfectly lawful for federal agencies to apply younger-is-better or whiter-is-better hiring policies to individuals who can't prove that they would have been hired but for those policies. That's anti-textual and it's wrong. Decisions applying such blatantly discriminatory policies are obviously not made free from any discrimination. The government's theory contradicts the plain statutory language.

[0:02:18.460] JUSTICE KAVANAUGH: But you say that the but-for causation is not required for liability, but then at the relief stage, as I understand your briefs, you say that but-for causation is required for reinstatement or back pay. And where is that in the statutory text?

[0:02:40.380] MR. MARTINEZ: So we would say that -- that at the -- at the remedial stage, ordinary remedial principles would apply, and those principles would require that the victim, the -- the plaintiff, be made whole for the violation. And under those ordinary principles that I think are undisputed on both sides, if the evidence shows that the -- the person, the plaintiff, couldn't -- wouldn't have gotten hired anyway, they shouldn't get remedies that are specifically and logically tied to that -- that thing that they -- they weren't -- wouldn't have been entitled to the in first place.

## Opinion announcement

No opinion announcement recording found on https://www.oyez.org/cases/2019/18-882. Nothing was transcribed.
