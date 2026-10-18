# tyler-surplus: Supreme Court No. 22-166

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2022/22-166
- Audio: https://www.supremecourt.gov/media/audio/mp3files/22-166.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/22-166_h4d8.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 55 min on 4 CPU cores
- Audio length: 1:40:50.544 (6050.544 s)
- `audio/argument.mp3`: mono, 64 kbps, 48.4 MB
- Official words: 18199 (plus 11 `(Laughter.)` markers), in 453 speaker turns
- ASR words: 13606
- Official words matched to an ASR word: 13227 of 18199 (**72.68%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 3 words longer than 3 s outside laugh positions.
  Offending words: "Be --" 4048.760-4059.000, "she" 4379.850-4382.945, "is" 4851.880-4855.860. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- FAIL: match rate over 85%. 72.68% (threshold 85%).

2768 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 16 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 28 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 27
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 22-166 2022 tyler-surplus --model medium.en --pdf-url https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/22-166_h4d8.pdf --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-44.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:08:53.800 | 533.800 | under speech | 0.00 | 0.00 | - | - | For purposes of this case, yes, Your Honor. Why for purposes of this case? Are you reserving the possibility of challenging Nelson itself? I -- I personally don't like Nelson, but -- |
| 2 | 0:09:27.920 | 567.920 | medium | 1.84 | 0.80 | 22.0 | 33.6 | opportunity to claim the surplus in this case, unlike in Nelson, Nelson, even if you think it's binding, is -- it -- it's completely distinguishable. Why do you personally not like Nelson? |
| 3 | 0:26:07.220 | 1567.220 | small | 1.03 | 0.05 | 6.0 | 12.3 | the value to the estate, but I think it gets harder, the line-drawing gets harder, if they're being clever the way that you're being -- I mean, that's a clever idea. |
| 4 | 0:38:54.020 | 2334.020 | under speech | 0.00 | 0.00 | - | - | one that's at issue here. Your friend doesn't like Nelson and thinks it's inconsistent with Knick. What do you think? So we're perfectly fine with Nelson, Justice Kagan. I think -- |
| 5 | 0:38:56.840 | 2336.840 | under speech | 0.00 | 0.00 | - | - | friend doesn't like Nelson and thinks it's inconsistent with Knick. What do you think? So we're perfectly fine with Nelson, Justice Kagan. I think -- Both personally and as the government. |
| 6 | 0:43:26.582 | 2606.582 | under speech | 0.00 | 0.00 | - | - | sort of as the Court said in Horne, it's different when you come in and you physically take the property. Well, it said it's different when it's raisins in Horne. |
| 7 | 0:59:27.096 | 3567.096 | under speech | 0.00 | 0.00 | - | - | 1292, is that right, Mr. Katyal? I think 1272 if I recall. '72, all right. Well, you know, a funny thing happened after that. It was called the Magna Carta. |
| 8 | 1:01:05.280 | 3665.280 | under speech | 0.00 | 0.00 | - | - | equivalent to the states' after the founding or that Ms. Tyler is a vassal or anything like that. We're simply -- Good. I'm glad -- I'm glad to hear that. That's progress. |
| 9 | 1:18:16.740 | 4696.740 | under speech | 0.16 | 0.00 | - | - | bridge too far. And as long as it's a reasonable -- That's a bridge too far? Yeah. But the $7, $5 for a million dollars is not a bridge too far? |
| 10 | 1:23:46.480 | 5026.480 | under speech | 0.00 | 0.00 | - | - | there's a -- that would be a reasonable condition on ownership because there is no tradition that goes back that could be looked to. Well, there weren't cars at the time. |
| 11 | 1:29:43.280 | 5383.280 | under speech | 0.00 | 0.00 | - | - | the fact that nobody thought there was any problem with this, so there was no litigation to had -- be had. Well, I think Jefferson would. He was always money-strapped. 103 |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.760 to 0:03:08.760, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.760] MS. MARTIN: Mr. Chief Justice, and may it please the Court: When the government takes property to satisfy a debt and takes more than what is owed, it has a constitutional duty to return or pay for the excess. Here, Geraldine Tyler owed $15,000, which included nearly $13,000 in penalties, interest, and related costs. To satisfy that debt, Hennepin County took Ms. Tyler's former home, which was worth much more than that, and later sold it for $40,000. The county kept all $40,000 for public uses. By taking absolute title to Ms. Tyler's property, including the value that exceeded the debt, the county has taken private property without just compensation. The county could have collected the debt without violating the Constitution by following the traditional common law rule still followed in most states and still followed in Minnesota in nearly every other debt collection circumstance. Under that rule, the county should have taken the property, sold it, paid the debts from the proceeds, and refunded the remainder to Ms. Tyler. Instead, the county took everything. The county apparently does not dispute that Ms. Tyler had a property interest in her former home or in its value. Instead, it asserts that the government may redefine private property by statute. The consequence of that would be an unlimited power to define away private property and to confiscate it to pay debts, no matter how valuable the property or how small the debt. But this Court's takings decisions and hundreds of years of common law, Minnesota's own treatment of debts in nearly every other debt collection circumstance confirm that the county has taken private property for which it must pay just compensation. If not remedied with just compensation, then the confiscation acts as a fine punishing Ms. Tyler for the public offense of failing to timely pay her property taxes. The confiscation of her property should therefore be subject to scrutiny under the Excessive Fines Clause because it goes well beyond compensating the government for any loss. This Court has repeatedly held that an economic sanction that serves in part to punish is a fine within the meaning of the Eighth Amendment. I welcome the Court's questions.

[0:02:30.020] JUSTICE THOMAS: If there was no differential in the -- if -- if there was no surplus equity, would there be a taking?

[0:02:39.340] MS. MARTIN: Yes, Your Honor -- well, are you asking if the property was worth less than what she owed the county?

[0:02:45.860] JUSTICE THOMAS: Or worth this -- this $15,000.

[0:02:49.180] MS. MARTIN: There -- there would be a taking, but just compensation would be paid at the time of the taking of absolute title because -- by forgiving the debt.

[0:02:58.360] JUSTICE THOMAS: So, normally, we say that a takings claim accrues when the government takes the property. And how would

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 25, 2023.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2022/22-166
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2022/22-166/22-166_20230525-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 3.0 MB)
- Length: 0:02:26.928 (146.928 s)
- Words: 399, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 389 of Whisper's 399 words (97.5%; Oyez has 394).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:02:26.100 | 395 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court this morning in Case 22-166, Tyler v. Hennepin County. Hennepin County is where Minneapolis is. In 2010, Geraldine Tyler, who is now 94, moved from her condominium to an apartment building for seniors. She failed to pay the property taxes on the condo for three years, so Hennepin County seized it and sold it. The home sold for $40,000. Tyler owed only $15,000 in taxes and late fees. But the county kept the extra $25,000 for itself. Tyler sued, claiming that the county had violated the Takings Clause of the Fifth Amendment, which prohibits the government from taking a person's property without providing just compensation. The Eighth Circuit Court of Appeals dismissed her suit because Minnesota law authorized the county to keep any surplus in the event of a tax sale. We granted certiorari to resolve this important constitutional question, which has divided courts around the country. Now Tyler acknowledges that she has to pay her property taxes, and she agrees that the county could sell her condo to recover those unpaid property taxes. But she argues that the county cannot keep the extra value of her home beyond what she owed. We agree. The principle that the surplus from a tax sale of property belongs to the taxpayer goes back to the Magna Carta in 1215. It was the rule at common law in England and here, and has always been the rule in a clear majority of the states. It was even the rule in Minnesota until they changed the law in 1935. That rule, that any surplus goes to the taxpayer, is also the rule in Minnesota when a home is sold because of a failure to pay a mortgage. The state just wants an exception for itself when it is the one taking real property in this sort of case. Minnesota says it can keep the surplus because the law in that state is that any surplus is not protected property. But we have long held that a government cannot change the rules about what counts as property just so it can avoid having to comply with the takings clause. That would make the clause a dead letter, and we're not going to do that. The opinion of the court is unanimous. Justice Gorsuch has filed a concurring opinion in which Justice Jackson joins.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:11.760 | who is | who's |
