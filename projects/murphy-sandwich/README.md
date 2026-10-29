# murphy-sandwich: Supreme Court No. 16-1067

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/16-1067
- Audio: https://www.supremecourt.gov/media/audio/mp3files/16-1067.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/16-1067_m6hn.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 83 min on 4 CPU cores
- Audio length: 0:53:03.432 (3183.432 s)
- `audio/argument.mp3`: mono, 64 kbps, 25.5 MB
- Official words: 8477 (plus 7 `(Laughter.)` markers), in 257 speaker turns
- ASR words: 8270
- Official words matched to an ASR word: 8001 of 8477 (**94.38%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.38% (threshold 85%).

299 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 5 times. ASR words with no official counterpart
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 16-1067 2017 murphy-sandwich --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-52.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:38:20.973 | 2300.973 | under speech | 0.00 | 0.00 | - | - | ended up on his side. Now, that's a little complicated, but that's where I am at the moment. What do you want to say? A lot, Your Honor. All right. |
| 2 | 0:45:25.790 | 2725.790 | medium | 0.82 | 0.70 | 25.7 | 33.5 | not be sufficient to fulfill that obligation and then specifies a secondary source. I mean, if my -- if my wife gives me a carrot for dinner to satisfy my hunger -- |
| 3 | 0:45:43.650 | 2743.650 | under speech | 0.00 | 0.00 | - | - | lots of other stuff so that I won't be hungry anymore, I don't know -- does that make the carrot sufficient to satisfy my hunger? No, Your Honor. In -- in that -- |
| 4 | 0:45:53.710 | 2753.710 | big | 1.70 | 1.55 | 29.7 | 37.5 | -- it would probably, you know, be an instance of discretion to -- Suppose she knows -- suppose she knows that he is going to eat that delicious turkey sandwich in the refrigerator. |
| 5 | 0:45:59.830 | 2759.830 | big | 2.78 | 2.40 | 26.7 | 32.9 | knows that he is going to eat that delicious turkey sandwich in the refrigerator. Now -- now the carrots are just enough to fill up that little hole that will remain. |
| 6 | 0:46:06.610 | 2766.610 | under speech | 0.00 | 0.00 | - | - | that delicious turkey sandwich in the refrigerator. Now -- now the carrots are just enough to fill up that little hole that will remain. But -- but -- true, but in that circumstance -- |
| 7 | 0:46:27.250 | 2787.250 | big | 2.68 | 1.80 | 27.5 | 35.6 | if that is ultimately not sufficient, they can -- But that's not. It's up to 25 percent. They didn't say 25 percent. Well, for instance -- Twenty-five percent of what she cooks. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:10.040 to 0:03:10.040, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:10.040] MR. BANNER: Mr. Chief Justice, and may it please the Court: When a prisoner wins a civil rights case and he's awarded damages and he's awarded attorney's fees, the prisoner himself has to pay part of the fees out of the damages judgment. The statute at issue in this case specifies the size of the prisoner's share. This is what the statute says: "A portion of the judgment (not to exceed 25 percent) shall be applied to satisfy the amount of attorney's fees." In the 20-plus years since the statute was enacted, virtually all the district courts have interpreted it literally. They identify an appropriate portion of the judgment, not exceeding 25 percent, and they deduct that amount from the attorney fee award payable by the defendant. In our case, the Seventh Circuit read the statute differently to mean that attorney's fees must be taken out of the damages first, up to 25 percent of the damages, so that the defendant is only liable for any fees left over. But the statute does not say that. All it says is that the portion of the judgment -- is that a portion of the judgment no greater than 25 percent must be allocated to fees. Respondents mistakenly suggest that Congress's use of the word "satisfy" indicates that the plaintiff has to pay the largest possible share of the fees in all cases. But that can't be right because the statute itself says what share the plaintiff has to pay: a portion of the judgment, not exceeding 25 percent. The rest of the attorney's fee award in excess of the plaintiff's share is payable by the defendant, up to the statutory cap of 150 percent of the damages. There's nothing in the statute --

[0:01:51.460] JUSTICE SOTOMAYOR: Your adversary points to a number of statutes that use the verb "to satisfy" -- or I guess not the verb, but the proposition "to satisfy" -- to refer to the complete fulfillment of an obligation. How do you distinguish those examples?

[0:02:10.440] MR. BANNER: The word "satisfy" often means the complete fulfillment of an obligation, but in this statute, it can't mean that because the statute makes clear that the plaintiff doesn't have to completely fulfill the obligation to pay attorney's fees. The statute says exactly how much.

[0:02:26.260] JUSTICE KENNEDY: Well, it's sensible to have a cap. It's just a cap.

[0:02:29.260] MR. BANNER: Well, exactly. It's a cap. It's a 25 percent cap. That's right. It's -- it's -- the statute says that the plaintiff's share of the attorney's fees is 25 percent or less of the judgment.

[0:02:41.300] CHIEF JUSTICE ROBERTS: Well, but you start with the notion of satisfaction; in other words, satisfying a debt. I mean, if you owe somebody $100 and you give them 50, that person isn't going to say, well, you've satisfied your obligation.

[0:02:51.740] MR. BANNER: No, that's right. And so the -- the -- the word "satisfy" standing alone sometimes often does mean complete payment, but that would make nonsense of the text of this statute. The text of this statute makes clear that the plaintiff doesn't have to pay the attorney's fees completely.

[0:03:07.060] CHIEF JUSTICE ROBERTS: No, no, I understand the point.

[0:03:07.940] MR. BANNER: Yeah.

[0:03:07.940] CHIEF JUSTICE ROBERTS: But I'm just suggesting that that's not certainly

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - February 21, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/16-1067
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/16-1067/16-1067_20180221-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.5 MB)
- Length: 0:01:58.465 (118.465 s)
- Words: 288, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 1 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 280 of Whisper's 288 words (97.2%; Oyez has 290).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:02.040 | 0:00:08.020 | 13 |
| JUSTICE GORSUCH | 0:00:09.400 | 0:01:57.700 | 274 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:02.040 to 0:03:02.040, with each speaker's start time.

[0:00:02.040] CHIEF JUSTICE ROBERTS: Justice Gorsuch has our opinion this morning in Case 16-1067, Murphy v. Smith.

[0:00:09.400] JUSTICE GORSUCH: This case comes to us from the United States Court of Appeals for the Seventh Circuit. When a prisoner wins a civil rights suit and is awarded attorney's fees, a Federal statute says that, quote, a portion of the judgment not to exceed 25 percent shall be applied to satisfy the amount of attorney's fees awarded. We took this case to resolve a split of authority about how much of the judgment must be so applied. Some circuits have said that district courts have discretion to select the amount a prisoner must pay out of the judgment to his lawyer. By contrast, the Seventh Circuit held that the district court must apply as much of the judgment as necessary, subject to the 25 percent cap, to satisfy the fee award. We think the Seventh Circuit has no context. The statute is phrased in mandatory terms. It says, shall be applied, not may, and it uses no word suggesting discretion. The text also specifies the purpose the district court must pursue when apportioning fees to satisfy the attorney's fee award. And the word satisfy, especially when used in the context of a financial obligation, usually means full payment. Putting these textual clues together, we think the statute tells us the district court must try to fully discharge the fee award from the prisoner's judgment, subject to the 25 percent cap. As our opinion explains, the broader statutory context and our precedent also confirm this result. The judgment of the court of appeals for the Seventh Circuit is therefore affirmed. Justice Sotomayor has filed a dissenting opinion in which Justices Ginsburg, Breyer, and Kagan have joined.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:56.840 | Circuit | Circuit's interpretation |
| 0:00:58.820 | no context. | the better of the text. |
| 0:01:07.820 | word | words |
| 0:01:31.380 | the | that |
