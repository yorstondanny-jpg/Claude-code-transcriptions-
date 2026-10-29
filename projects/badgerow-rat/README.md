# badgerow-rat: Supreme Court No. 20-1143

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2021/20-1143
- Audio: https://www.supremecourt.gov/media/audio/mp3files/20-1143.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2021/20-1143_bqmc.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 90 min on 4 CPU cores
- Audio length: 0:51:44.952 (3104.952 s)
- `audio/argument.mp3`: mono, 64 kbps, 24.8 MB
- Official words: 9576 (plus 1 `(Laughter.)` markers), in 125 speaker turns
- ASR words: 9355
- Official words matched to an ASR word: 8978 of 9576 (**93.76%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.76% (threshold 85%).

240 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 3 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 8 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 20-1143 2021 badgerow-rat --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-42.0 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:17:26.100 | 1046.100 | medium | 0.86 | 0.75 | 26.7 | 31.0 | enforce the award. Congress did not repeat that language in Section 9 or in Section 10. So you could call them an arbitration rat or a judicial lion, I suppose. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.920 to 0:03:07.920, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.920] MR. GEYSER: Thank you, Mr. Chief Justice, and may it please the Court: The question presented is whether Vaden's look-through approach applies to applications to enforce or vacate an arbitration award under Sections 9 and 10 of the Federal Arbitration Act. The answer is controlled by the FAA's plain text, and the competing statutory arguments are not close. The look-through approach is no ordinary jurisdictional doctrine. It is an express textual departure from the well-pleaded complaint rule. This textual exception is found solely in Section 4. It applies exclusively to petitions under that single section. Congress did not repeat this unique language anywhere else in the Act. In fact, there's not a single textual hint in any other section that a look-through analysis is allowed or appropriate. Yet, according to Respondents, the look-through approach somehow applies to every section of the FAA instead of the single section where it actually appears. Respondents' theory fails on every conceivable level. For over a century now, the well-pleaded complaint rule has governed the exercise of jurisdiction in federal courts. That's the rule that applies unless Congress says otherwise. And Congress said otherwise in Section 4 alone. Congress did not isolate the look-through clause in Section 4 because it wanted it applied in other sections where it was excluded. Nor did Congress endorse Respondents' notion of an upside-down default rule, where courts ignore the face of the well-pleaded filing and instead look to a nonexistent, phantom pleading that never appears in any court. Respondents' theory would require overturning bedrock jurisdictional doctrine and abandoning this Court's fidelity to the statutory text. There is simply no basis for saying the look-through approach applies in Sections 9 and 10 without judicially rewriting the statute or rendering Section 4's express look-through clause wholly superfluous. I welcome the Court's questions.

[0:02:06.360] JUSTICE THOMAS: Counsel, we have said or suggested from time to time that the FAA doesn't provide federal question jurisdiction. So how do you square that with the notion that Section 4, Section 8, provide such jurisdiction?

[0:02:24.560] MR. GEYSER: Well, I think the best reading of this Court's cases is it was referring generally to the idea that when an action arises under federal law, then the federal law itself provides jurisdiction. The Court wasn't parsing the individual sections of the Act and saying whether there's a specific independent grant of jurisdiction. But, ultimately, I don't think it matters because there are only two ways to read Section 4. We read Section 4 as providing jurisdiction. But the alternative is to read Section 4 as providing an instruction to courts on how to exercise jurisdiction under sections like 1331 and 1332, and that instruction says you can look through to the underlying dispute. Now that's the departure from the well-pleaded complaint rule that traditionally governs every

## Opinion announcement

No opinion announcement recording found on https://www.oyez.org/cases/2021/20-1143. Nothing was transcribed.
