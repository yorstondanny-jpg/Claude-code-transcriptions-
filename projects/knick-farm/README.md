# knick-farm: Supreme Court No. 17-647

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/17-647
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-647.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-647_aplc.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 25 min on 4 CPU cores
- Audio length: 1:02:04.608 (3724.608 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.8 MB
- Official words: 5112 (plus 0 `(Laughter.)` markers), in 151 speaker turns
- ASR words: 4993
- Official words matched to an ASR word: 4847 of 5112 (**94.82%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.82% (threshold 85%).

199 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 11 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-647 2018 knick-farm --model medium.en --pdf-url https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-647_aplc.pdf --opinion

## Petitioner's opening, first 3 minutes

Everything said from 0:07:30.653 to 0:10:30.653, official wording, with each turn's start time. Interruptions from the bench are included.

[0:07:30.653] JUSTICE GINSBURG: question, is there a taking, you can bring in federal court. Then -- and if the answer to that is yes, then the whole inverse condemnation proceeding goes forward in -- in federal court with --

[0:07:45.813] MR. BREEMER: I understand your -- your question, Your Honor. Once a takings determination is made, then a federal court would hold a -- a damages proceeding, just like it does in other Section 1983 contexts, unreasonable seizure, due -- due process deprivations. And it -- it would be easier in a takings context than those other contexts because damages for a taking is simply just compensation. So a federal court --

[0:08:09.713] JUSTICE GINSBURG: But how would this -- and that's what -- that's what inverse condemn -- condemnation is as well. So how do -- how does step 2 -- step 1, is there a taking? Yes. Something else happens in federal court. How would -- does that something else differ from an inverse condemnation proceeding in state court?

[0:08:34.413] MR. BREEMER: It -- it doesn't. It's -- it's dual -- the inverse condemnation rights. The Fifth Amendment under First English incorporates a right of inverse condemnation under the federal Constitution. The states have also inverse condemnation procedures, but, again, the question is when you have a federal claim, when your claim is that the takings provision in the Fifth Amendment is violated -- excuse me, not violated, when it's implicated so that there's a just compensation remedy, do you have to go use a state inverse condemnation instead of the Fifth Amendment's inverse condemnation procedure that's recognized as self-executing.

[0:09:08.313] JUSTICE KAGAN: Right --

[0:09:08.813] JUSTICE ALITO: Let me see --

[0:09:08.873] JUSTICE KAGAN: -- but usually --

[0:09:08.873] JUSTICE ALITO: -- if I understand your claim, because a little -- some of the questions and the discussion up to this point is a bit confusing to me. I thought your claim was that there is a violation of the takings clause and you can, therefore, bring a suit under 1983 when the state does something that constitutes a taking but at the same time says we're not paying you anything for this. Now it's not a question of when they would have to pay once they've admitted that there's a taking, but when they do something that constitutes a taking, and they say, no, this isn't a taking at all, and, therefore, you're getting zero, which I understand to be your claim here, then you can go directly to federal court and bring an action under 1983. And to require you to go to state court before you do that is essentially to require you to exhaust state remedies before you can bring a 1983 claim, which is never required under 1983. I thought that that was your argument.

[0:10:14.173] MR. BREEMER: Right. And that is one of our arguments, is that when the government, the township here in this case, invades property without -- without condemning it, it's clear that it's not compensating and that your claim --

[0:10:26.573] JUSTICE KAGAN: Well, how --

[0:10:26.913] MR. BREEMER: -- accrues at that --

[0:10:26.913] JUSTICE KAGAN: -- is it clear that it's not compensating? In other words, what Justice Alito says

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 21, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/17-647
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/17-647/17-647_20190621-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.9 MB)
- Length: 0:07:55.847 (475.847 s)
- Words: 1227, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1206 of Whisper's 1227 words (98.3%; Oyez has 1226).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:07:54.760 | 1223 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court this morning in Case 17-647, Nick v. The Township of Scott. Rosemary Nick owns 90 acres of land in Scott Township, Pennsylvania. Nick's property includes a single-family residence where she resides, a grazing area for horses, and, as is relevant today, a small graveyard where some ancestors of Nick's neighbors are allegedly buried. Such family cemeteries are fairly common in rural Pennsylvania, where backyard burials have been permitted for a long time. Now, the township passed an ordinance in 2012 requiring that all cemeteries, including small graveyards on private property like Nick's, be kept open and accessible to the general public during daylight hours. Now, Nick filed a lawsuit in Federal court alleging that, by opening up her land to all comers, the ordinance took her property without just compensation in violation of the Takings Clause of the Fifth Amendment. Normally, a plaintiff complaining of unconstitutional conduct by State or local officials is able to proceed directly to Federal court under the Civil Rights Act of 1871. But 34 years ago, in a case called Williamson County v. Hamilton Bank, we held that a Takings plaintiff like Nick cannot bring her Federal claim in Federal court until she has sought and been denied compensation in State court under State law. So the district court dismissed Nick's complaint. The Third Circuit Court of Appeals affirmed, and we granted review to reconsider our decision in Williamson County. The Williamson County court held that a property owner has no Federal Takings claim until he is litigated and lost in State court because it believed that a government does not necessarily violate the Takings Clause at the time it takes property without paying for it. All the clause requires at the time of the taking, Williamson County thought, is that the government give the property owner some means of obtaining compensation after the fact. A violation occurs, if at all, only later when the government denies the property owner compensation in such a post-taking proceeding. Since there is no violation at the time of the taking itself, the property owner cannot go to Federal court at that time because he can only go to Federal court to remedy a violation. Now, the Williamson County court anticipated that an unsuccessful Takings plaintiff would be able to go to Federal court with the Federal Takings claim when the State court denies him compensation. There would be a violation at that time. But 20 years later, we issued another decision called San Remo Hotel v. San Francisco.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:03.160 | 17 -647, Nick | 17-647, Knick |
| 0:00:05.960 | The | (nothing) |
| 0:00:08.400 | Rosemary Nick | Rose Mary Knick |
| 0:00:13.600 | Nick's | Knick's |
| 0:00:21.060 | (nothing) | as |
| 0:00:25.300 | Nick's | Knick's |
| 0:00:42.720 | graveyards | graveyard |
| 0:00:44.800 | Nick's, | Knick's, |
| 0:00:51.420 | Nick | Knick |
| 0:01:26.380 | Nick | Knick |
| 0:01:37.200 | Nick's | Knick's |
| 0:02:33.040 | he | you |
| 0:03:08.260 | He's | He is |
| 0:04:55.280 | Stari | stare |
| 0:07:20.840 | Nick | Knick |
