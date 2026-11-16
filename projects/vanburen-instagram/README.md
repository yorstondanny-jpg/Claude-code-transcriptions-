# vanburen-instagram: Supreme Court No. 19-783

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2020/19-783
- Audio: https://www.supremecourt.gov/media/audio/mp3files/19-783.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2020/19-783_2d8f.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 30 min on 4 CPU cores
- Audio length: 1:06:07.752 (3967.752 s)
- `audio/argument.mp3`: mono, 64 kbps, 31.7 MB
- Official words: 10085 (plus 0 `(Laughter.)` markers), in 163 speaker turns
- ASR words: 9711
- Official words matched to an ASR word: 9473 of 10085 (**93.93%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.93% (threshold 85%).

321 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 8 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 11 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 19-783 2020 vanburen-instagram --model medium.en

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.920 to 0:03:07.920, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.920] MR. FISHER: Mr. Chief Justice, and may it please the Court: The CFAA is an anti-hacking statute. It prohibits obtaining information from a computer without authorization. And to ensure comprehensive coverage, the statute also prohibits "exceeding authorized access." As Judge Kozinski put it, this -- this ensures that the statute covers not just outside but also inside hackers. In this case, however, the government seeks to transform the supplemental prong of the CFAA into an entirely different prohibition. In the government's view, this prong covers obtaining any information via computer that the accessor is not entitled "under the circumstances" to obtain. It is no overstatement to say that this construction would brand most Americans criminals on a daily basis. The scenarios are practically limitless, but a few examples will suffice. Imagine a secretary whose employee handbook says that her e-mail or Zoom account may be used only for business purposes. Or consider a person using a dating website where users may not include false information on their profile to obtain information about potential mates. Or think of a law student who is issued a log -- log-in credentials for Westlaw or Lexis for educational use only. If the government is right, then a computer user who disregards any of these stated use restrictions commits a federal crime. For example, any employee who used a Zoom account over Thanksgiving to connect with distant relatives would be subject to the grace of federal prosecutors. The main argument the government offers in response to that startling result is that a single two-letter word in the CFAA's definition of "exceeds authorized access," the term "so," demands it. But that word requires no such thing. The word simply clarifies that a use -- that the user must be prohibited from obtaining the information merely by a computer. It relieves the government of having to negate every possible alternative means by which the defendant might permissibly have obtained the information at issue. But that is all the word does. It does not transform the CFAA into a sweeping Internet police mandate. The Court should reverse. And I'm happy to take any questions.

[0:02:13.160] CHIEF JUSTICE ROBERTS: Mr. Fisher, in Musacchio versus United States, this is what we said: That statute provides two ways of committing the crime of improperly accessing a protected computer: obtaining access without authorization and obtaining access with authorization but then using that access improperly. You didn't mention that case in your opening brief. The government relied on it. You didn't mention it in your reply brief. I wonder what your -- your answer to that quote is.

[0:02:46.500] MR. FISHER: Mr. Chief Justice, my understanding in that case was the Court was simply giving a thumbnail summary of how the statute works. Of course, the question presented here was not presented there. And, in fact, not even the "exceeds authorized access" prong was at issue there in the conspiracy issue the Court reached. I understood what the Court to be doing in that summary simply to be using
