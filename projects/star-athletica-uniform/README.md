# star-athletica-uniform: Supreme Court No. 15-866

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2016/15-866
- Audio: https://www.supremecourt.gov/media/audio/mp3files/15-866.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2016/15-866_j426.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 49 min on 4 CPU cores
- Audio length: 1:01:38.088 (3698.088 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.6 MB
- Official words: 10850 (plus 0 `(Laughter.)` markers), in 276 speaker turns
- ASR words: 10687
- Official words matched to an ASR word: 10119 of 10850 (**93.26%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.26% (threshold 85%).

350 words are shorter than 20 ms. These are official words the ASR didn't produce,
mostly repeats, false starts and cross-talk ("the -- the --", "I -- I think"), squeezed into the
small gap between the ASR words either side. Their order is right; their exact times are not.

## Files

- `audio/argument.mp3`: the argument audio.
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
to that sound, at least 0.2 s from its start. This trimmed 16 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 15-866 2016 star-athletica-uniform --model medium.en

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.400 to 0:03:07.400, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.400] MR. BURSCH: Thank you, Mr. Chief Justice, and may it please the Court: Congress did not intend to grant a century-long copyright monopoly in cheerleader uniform design. And there are three points that support that conclusion. First, by subjecting two-dimensional pictures and graphics as well as sculptures to Section 101 separability test, Congress made clear that two-dimensional and three-dimensional designs must be analyzed for separability. Second, under Section 101's text, the dispositive questions are twofold: Whether the deign features can be identified separately from the useful article's utilitarian aspects; and second, whether they can exist independently, that is, the design features do not add to or change the useful article's utilitarian --

[0:00:53.200] JUSTICE GINSBURG: Why, in this case, would we even need to get to any question of separability? What was submitted was a two-dimensional artwork. It may not be like Mondrian, but it is chevrons and other things. They are not submitting the cheerleader's uniform itself. They are not saying anything about the shape of the uniform, the cut of the uniform. They are just saying these zigzag designs -- and you can choose from five different ones that are interchangeable, the design. So why isn't this a -- a case of not -- not part -- the pictorial graphic element is not part of the design of the cheerleader's uniform; it's superimposed on it. It's reproduced on it. It's applied to it.

[0:01:54.880] MR. BURSCH: There two reasons, Justice Ginsburg. First, consider the example where you have a designer who designs a military uniform. And on that military uniform, they design the best desert camouflage that's been ever designed in the history of the world. And they submit it to the copyright office, and they don't claim the design in the uniform, they only claim copyright in the design on the uniform. There is no question they would have the copyright in the design, but the courts would still look to see whether that adds to the utilitarian aspects of that uniform such that that design copyright holder could not prevent the military from producing a military uniform that uses that design. That's why it's so important to understand that in Section 101, not only two-dimensional -- or three-dimensional, but also two-dimensional designs are subject to separability. And there's a second reason, Justice Ginsburg. What you're referring to, generally, is kind of the area of fabric design. And a good example of fabric design is the -- the flowers on the fabric in the Folio Impressions case that we reprint on page 7 of our reply brief. And those flowers, you could expand the design, you could contract the design, you can make any article of clothing out of it whatsoever, you could rotate it 45 degrees, and it always works functionally
