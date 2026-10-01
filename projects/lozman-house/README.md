# lozman-house: Supreme Court No. 11-626

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2012/11-626
- Audio: https://www.supremecourt.gov/media/audio/mp3files/11-626.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2012/11-626.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 40 min on 4 CPU cores
- Audio length: 0:59:22.893 (3562.893 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.5 MB
- Official words: 10700 (plus 2 `(Laughter.)` markers), in 227 speaker turns
- ASR words: 10531
- Official words matched to an ASR word: 10193 of 10700 (**95.26%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.26% (threshold 85%).

321 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
cluster if it ends at the word's end, and is left alone otherwise. This trimmed 16 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 11-626 2012 lozman-house --model medium.en

## Petitioner's opening, first 3 minutes

Everything said from 0:00:10.440 to 0:03:10.440, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:10.440] MR. FISHER: Mr. Chief Justice, and may it please the Court: To be a vessel, a structure must be practically capable of maritime transportation, and this case turns on how to assess such practical capability. And that's a question this Court answered over a century ago in Cope and Perry, explaining that practical capability depends not on any physical attribute the structure might have, but rather, on "its purpose," that is, whether its function is to move people or things across water. And that test has been applied numerous times before and since, across decades, providing stability and overall coherence to general maritime law. And of course --

[0:00:50.480] JUSTICE SCALIA: You should have phrased the test that way then, because it really --

[0:00:53.120] MR. FISHER: Pardon me?

[0:00:54.920] JUSTICE SCALIA: That doesn't seem to me a very felicitous description of what -- of what the test is -- is enunciated to be.

[0:01:05.880] MR. FISHER: Well, I think --

[0:01:06.820] JUSTICE SCALIA: The test is whether it's, what, practically able?

[0:01:10.420] MR. FISHER: Practically capable.

[0:01:11.920] JUSTICE SCALIA: Practically capable. Well, you could be practically capable of doing something, even though the purpose of -- of setting the thing up has nothing to do with that.

[0:01:21.680] MR. FISHER: Well, that's not what this Court -- case is saying --

[0:01:23.380] JUSTICE SCALIA: I understand. I'm just saying we ought to get a different test, and let's -- let's get rid of this. If we agree with you, let's get rid of this practically capable test, because practically capable, frankly, would make us come out the other way in this case.

[0:01:37.920] MR. FISHER: With all due respect, I don't think that's correct. In Evansville in 1926, this Court used that exact phrase, practical capability. And it assessed that practical capability by looking at "the function of the structure." Again and again, in Evansville and other cases, this Court asked, was the function of the structure to carry people or things across water.

[0:01:57.120] CHIEF JUSTICE ROBERTS: Well, that just has -- I understand that argument. It's got no connection whatever to the statutory language, right?

[0:02:04.500] MR. FISHER: Well, I think the word capable obviously is in the statute. And what this Court said as recently as Stewart is that capable --

[0:02:10.400] CHIEF JUSTICE ROBERTS: Capable is in the statute, purpose is not, right?

[0:02:14.020] MR. FISHER: Correct. And what this Court said in Stewart is that capable means practically capable, not theoretically capable. There's a range of how broad the word capable can be. And again, going back over a century, every single time this Court's been confronted with that question, it's used the term function to describe whether or not something is practically capable of carrying people or things over water.

[0:02:35.260] JUSTICE GINSBURG: You -- you described cases with this purpose -- or function, the briefs cited the district court decision, Sea Village Marina, that says floating homes like the one here that can be towed and are not in the business of carrying people or goods, but can be towed miles across the water, that those constitute vessels. And this district court
