# ransom-apples: Supreme Court No. 09-907

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2010/09-907
- Audio: https://www.supremecourt.gov/media/audio/mp3files/09-907.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2010/09-907.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 37 min on 4 CPU cores
- Audio length: 0:58:53.558 (3533.558 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.3 MB
- Official words: 10030 (plus 2 `(Laughter.)` markers), in 273 speaker turns
- ASR words: 9930
- Official words matched to an ASR word: 9492 of 10030 (**94.64%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.64% (threshold 85%).

219 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 27 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 09-907 2010 ransom-apples --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-48.5 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:04:58.940 | 298.940 | big | 1.50 | 1.35 | 26.0 | 33.4 | you're getting the credit for is simply -- is simply false. You don't do that under either side's interpretation, right? Again, I would perhaps -- I'm trying to help you, Mr. Burke. |
| 2 | 0:09:08.960 | 548.960 | under speech | 0.00 | 0.00 | - | - | dozen apples every month, and they cost you $48 extra. You're not going to say the ownership costs refer to the apples, even if you decorate the car with them. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:12.220 to 0:03:12.220, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:12.220] MR. BURKE: Thank you, Mr. Chief Justice, and may it please the Court: In 2005, Congress passed the Bankruptcy Act. It made a policy decision to limit judicial discretion on a case-by-case basis in the area of reasonable and necessary expenses. It did so by creating a formula that entailed an aggregate set amount of expenses for an individual. Now, Congress could have created this from scratch. It could have used an arbitrary figure. But instead, there were figures that the IRS already had, based on Census Bureau statistics, that said nationwide, in a certain area, an individual would spend this much a month on average. In the case of Mr. Ransom, that's approximately 2500 a month. Forgetting about how it's divided up, if I had 100 people come in and answer the following five questions the same way Mr. Ransom did, and that's age, location, household size, gross income, and if you have a vehicle, how many, they would all get a $2500 standard aggregate deduction, which works out to $150,000 over a 5-year period. Now, the crux of this is whether or not courts are allowed to dig in and cut out pieces of the standard aggregate amount.

[0:01:45.480] JUSTICE ALITO: Why is that the crux of it? Congress made reference to the local standards, right?

[0:01:51.040] MR. BURKE: Yes.

[0:01:51.300] JUSTICE ALITO: And were the -- was the commentary in the Collection Financial Standards in existence at the time when Congress enacted this provision?

[0:02:03.180] MR. BURKE: There was a Collection Financial Analysis that was in place, and it was noted in 1998 as a prior version of the bill that ultimately wasn't passed.

[0:02:13.920] JUSTICE ALITO: And that explains what the IRS understands the local standards to mean; isn't that right?

[0:02:19.560] MR. BURKE: I would disagree with that. I would say -- well, it would -- it would explain what the IRS means, but that's where I would end it, because the IRS standards are used to collect taxes. They are discretionary. They --

[0:02:34.900] JUSTICE ALITO: Well, I understand that, but Congress decided to make reference to the local standards in this bankruptcy provision, didn't it?

[0:02:41.840] MR. BURKE: Standards.

[0:02:42.760] JUSTICE ALITO: Yes.

[0:02:43.940] MR. BURKE: It didn't go beyond that.

[0:02:44.200] JUSTICE ALITO: And this -- and at the time when it did that, there was official IRS commentary regarding the meaning of those standards, correct?

[0:02:53.500] MR. BURKE: For the IRS to use in collecting taxes.

[0:02:55.580] JUSTICE ALITO: And your argument is that Congress intended to adopt the standards promulgated by the IRS, but not the IRS's interpretation of the standards.

[0:03:06.340] MR. BURKE: Correct, not their methodology or interpretation.

[0:03:08.620] JUSTICE GINSBURG: Doesn't the chart say "ownership

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 11, 2011.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2010/09-907
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2010/09-907/20110111o_09-907.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:43.925 (283.925 s)
- Words: 632, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 603 of Whisper's 632 words (95.4%; Oyez has 619).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| JUSTICE KAGAN | 0:00:00.840 | 0:04:43.260 | 631 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.840 to 0:03:00.840, with each speaker's start time.

[0:00:00.840] JUSTICE KAGAN: This case is about the proper interpretation of the Bankruptcy Code. In what's called Chapter 13 Bankruptcy, a person can get relief from all his debts in exchange for an agreement, an agreement to repay his creditors a certain amount of his future income for the next several years. The Bankruptcy Code instructs a person in this situation how to calculate the exact amount that he has to repay his creditors. The Code says to that person, first you take your current income, then you deduct certain defined living expenses. Those defined expenses, the Bankruptcy Code says, are set amounts, not necessarily your actual expenses, but set amounts that the IRS decides are reasonable for various necessary things, like housing or transportation or food. You deduct those expenses from your income, and what's left over is the amount that you are required to repay creditors. Now, the issue in this case is whether the Bankruptcy Code allows a debtor who's making this calculation to deduct an expense that he simply does not have. The expense at issue is for car ownership. The IRS, and again, that's the agency that's authorized to set these reasonable expenses, the IRS says that the average loan or lease payment for a car nationwide is $471 a month. And so the IRS says that's the amount that a person typically can deduct in Chapter 13 Bankruptcy. That's the amount of the car ownership deduction. The petitioner here, whose name is Jason Ransom, he claimed this deduction even though he owned his car free and clear, and he didn't, in fact, make any loan or lease payments on this car. And claiming this deduction allowed him to shield about $28,000 that he otherwise would have had to pay his creditors over the life of his Bankruptcy plan. And he took the car ownership deduction in addition to claiming another deduction that the IRS sets for car operating costs, like fuel and insurance and repairs. So one of his creditors, perhaps not surprisingly, objected. That creditor said that Mr. Ransom wasn't eligible to claim the car ownership deduction because he didn't, in fact, incur any car ownership costs. Today, we hold that this was a valid objection, that Mr. Ransom was not entitled to this deduction under the Bankruptcy Code. We reach this conclusion by looking closely at the language of the statute. The statute authorizes a debtor to deduct,

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:01:00.400 | amount | amounts |
| 0:01:50.600 | claimed | claims |
| 0:02:07.760 | would have | would've |
| 0:02:53.620 | reach | reached |
| 0:03:00.920 | and I'm quoting here, | (nothing) |
| 0:03:10.520 | a | the |
| 0:03:55.200 | make | made |
| 0:04:04.880 | Congress's | Congress' |
| 0:04:24.300 | deduct | deducts |
