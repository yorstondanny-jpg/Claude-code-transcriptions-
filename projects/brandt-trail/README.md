# brandt-trail: Supreme Court No. 12-1173

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2013/12-1173
- Audio: https://www.supremecourt.gov/media/audio/mp3files/12-1173.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2013/12-1173_25f3.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 15 min on 4 CPU cores
- Audio length: 1:01:34.315 (3694.315 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.6 MB
- Official words: 4420 (plus 0 `(Laughter.)` markers), in 101 speaker turns
- ASR words: 4466
- Official words matched to an ASR word: 4139 of 4420 (**93.64%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.64% (threshold 85%).

119 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 1 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 7 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 12-1173 2013 brandt-trail --model medium.en --opinion

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 10, 2014.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2013/12-1173
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2013/12-1173/20140310o_12-1173.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:26.475 (266.475 s)
- Words: 726, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 685 of Whisper's 726 words (94.4%; Oyez has 723).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| UNKNOWN | 0:00:00.000 | 0:04:25.840 | 722 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] UNKNOWN: I have the opinion of the Court this morning in Case 12-1173, Marvin M. Brant Revocable Trust v. The United States. This case has its roots in America's westward expansion in the early and mid-19th century. It was during that period that the lands from the Mississippi River to the Pacific Ocean were acquired, filling out what is now the contiguous United States. Now, once that was done, the challenge for the young country was how to develop and settle that vast expanse. Railroads were a key part of the answer. To encourage their construction, Congress granted railroad companies a right of way over public lands, which is what most of the land was at the time. Congress also gave the railroads an enormous amount of public land outright, which they could sell to help finance the construction. The lands over which the railroad tracks were laid were eventually granted to homesteaders or sold to others, but with the railroads, of course, retaining their rights of way over that land. Now, this was how things worked not only for the big lines, such as the Union Pacific, but for the bit players as well. One of the latter was the Laramie-Hans Peak and Pacific Railroad, or the LHP &P. It acquired a right of way and built its line from Laramie, Wyoming to Colmont, Colorado. Its proprietors predicted that it would become, quote, ''one of the most important railroad systems in the country ,'' end quote. It did not. In fact, local said LHP &P stood for late, hard-pressed and panicky. Anyway, the railroad went through several owners until, beginning in 1996, the then owner, the Wyoming and Colorado Railroad, closed the line, tore up the tracks and abandoned its right of way. The land over which the right of way ran was then owned by the Brant family, which had purchased it from the Federal government in 1976. That purchase, of course, was subject to the right of way. When the Wyoming and Colorado abandoned the right of way, a dispute arose over who it went to. The Brant family said it should get the right of way because the right of way was, under the law, something called an easement. An easement is a right to do something over someone else's land, nothing more. Now, when the Wyoming and Colorado stopped using its easement for railroad purposes, the Brants argued, full right to use the land went to them because they owned the underlying parcel. The government saw things differently. According to it, when it sold the land to LHP &P, the predecessor to the Wyoming and Colorado, the government granted more than a mere easement. It granted substantial property rights in the land itself, not just a right of use over the land. That meant that when the railroad left the

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:05.280 | Brant | Brandt |
| 0:00:11.400 | westward | west road |
| 0:00:16.540 | (nothing) | that the -- |
| 0:00:35.580 | (nothing) | to |
| 0:00:56.720 | to | the |
| 0:01:05.080 | worked | work |
| 0:01:13.820 | -Hans | Hahn's |
| 0:01:23.100 | Colmont, Colorado. Its | Coalmont, Colorado.Its |
| 0:01:30.320 | railroad | railroads |
| 0:01:32.140 | ,'' end quote. | (nothing) |
| 0:01:36.000 | LHP &P | LHP&Ps |
| 0:01:39.480 | panicky. | panicking. |
| 0:01:59.980 | Brant | Brandt |
| 0:02:01.520 | purchased it | purchase that |
| 0:02:10.700 | and | in |
| 0:02:15.840 | Brant | Brandt |
| 0:02:32.760 | Brants | Brandt's |
| 0:02:37.100 | owned | own |
| 0:02:47.600 | and | in |
| 0:02:53.420 | in | and |
| 0:02:55.360 | a | the |
| 0:03:01.920 | went | when |
| 0:03:07.400 | (nothing) | It |
| 0:03:11.260 | issue | issues |
| 0:03:13.960 | that | the |
| 0:03:15.280 | it | (nothing) |
| 0:04:07.240 | Brant | Brandt |
| 0:04:08.220 | unencumbered | an encumbered |
| 0:04:10.560 | Brants | Brandt's |
| 0:04:11.340 | to | the |
