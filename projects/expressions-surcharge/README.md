# expressions-surcharge: Supreme Court No. 15-1391

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2016/15-1391
- Audio: https://www.supremecourt.gov/media/audio/mp3files/15-1391.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2016/15-1391_5315.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 49 min on 4 CPU cores
- Audio length: 1:03:15.072 (3795.072 s)
- `audio/argument.mp3`: mono, 64 kbps, 30.4 MB
- Official words: 11468 (plus 5 `(Laughter.)` markers), in 276 speaker turns
- ASR words: 11391
- Official words matched to an ASR word: 10898 of 11468 (**95.03%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "Okay." 1527.620-1547.900. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 95.03% (threshold 85%).

325 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 13 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 15-1391 2016 expressions-surcharge --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-52.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:05:11.260 | 311.260 | big | 1.68 | 1.50 | 30.4 | 39.3 | impose a surcharge. No. No -- Then what's the problem with saying -- you -- you don't -- you're too young to know what the OPA was. I think -- I think so, Justice Breyer. |
| 2 | 0:31:32.860 | 1892.860 | big | 3.42 | 2.90 | 22.0 | 32.4 | good reasons why that has to be done. First, if you're -- or why it's reasonable for -- I thought it was $10 and 2 cents, but I'll think about that while -- |
| 3 | 0:33:11.480 | 1991.480 | big | 1.84 | 1.70 | 28.2 | 35.5 | to understand that if you say $10 plus a 20-cent surcharge, they can't figure out that that's $10.20. And the second reason, Your Honor, I think addresses that concern directly. |
| 4 | 0:33:52.940 | 2032.940 | under speech | 0.04 | 0.00 | - | - | 32.46 plus 2 percent, then you really are requiring people to do some work and you'd rather just have them know that it's -- see, I can't do it that fast. |
| 5 | 0:55:53.960 | 3353.960 | medium | 0.74 | 0.55 | 30.7 | 33.4 | for their lemonade. These are tech savvy kids so they can -- could process a credit card purchase if they wanted to? The statue has no exemption for kids selling lemonade. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.600 to 0:03:07.600, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.600] MR. GUPTA: Mr. Chief Justice, and may it please the Court: This case is about whether the State may criminalize truthful speech that merchants believe is their most effective way of communicating the hidden cost of credit cards to their customers. By design, New York's law suppresses the message that you pay more --

[0:00:25.880] JUSTICE SOTOMAYOR: I'm sorry. I -- I -- you're two groups of -- of Petitioners. One wants to just give a cash price without any information about the surcharge, and the other, I thought, wanted to give two separate prices. So not everybody doesn't want to give truthful information about the surcharge.

[0:00:45.540] MR. GUPTA: No -- well, they do, Your Honor. They all want to do the same thing. They -- they -- I think what you're referring to is that some of them are doing different things now. One of the Petitioners, Expressions Hair Design, is engaging in dual pricing, they're charging two different prices, one for cash, one for credit, but they are trying as hard as they can to describe that as a -- as a discount so that they comply with the law. The other Petitioners right now are refraining from dual pricing altogether, because they don't want to run the risk of -- of failing to comply with this regime. But if we win this case, all of the Petitioners would like to charge two different prices for cash or for credit, and they would like to be able to characterize the price difference as a surcharge for using a credit card.

[0:01:27.160] JUSTICE SOTOMAYOR: That's not what I understood, but your adversary can tell me.

[0:01:31.960] JUSTICE KAGAN: Mr. Gupta, what -- what speech precisely do you think is being restricted?

[0:01:36.980] MR. GUPTA: The -- the message that when you use a credit card, you're paying more, and to be more precise, I think if you look at Joint Appendix 103 through 104, you'll find there the supplemental declaration of Expressions Hair Design where they say exactly what they'd like to do. And if you look at the yellow brief, it's page 1 of the yellow brief, we have a chart. And what we'd like to do, ideally, is describe the pastrami sandwich as $10, and then tell you that it's going to cost a certain percentage more, 2 percent more, to pay with a credit card.

[0:02:10.220] JUSTICE KAGAN: Well, I guess that's why I said like what speech precisely, and you said the message that you're going to pay more if you use a credit card.

[0:02:17.720] MR. GUPTA: Right.

[0:02:17.980] JUSTICE KAGAN: But, you know, as -- this -- this statute is not written in terms of speech, it's -- it's written in terms of imposing a surcharge. And -- and let's say that somebody -- let's say that there is a merchant and the merchant charges the list price for something as a dollar and the person comes up to the cash register and offers a dollar bill.

[0:02:41.380] MR. GUPTA: Uh-huh.

[0:02:42.000] JUSTICE KAGAN: And -- and the cashier says, oh, no. For you it's 95 cents because I impose a surcharge for people who use credit cards; right?

[0:02:54.260] MR. GUPTA: Uh-huh.

[0:02:55.080] JUSTICE KAGAN: Now, would that violate this law?

[0:02:57.180] MR. GUPTA: I -- you know, I don't know, and what -- part of the difficulty is -- and the reason, we have a vagueness challenge --

[0:03:02.480] JUSTICE KAGAN: You don't know? How would it violate the law?

[0:03:04.200] MR. GUPTA: I don't think -- I don't think it would. I don't think it would. And certainly the State hasn't taken that position --

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 29, 2017.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2016/15-1391
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2016/15-1391/15-1391_20170329-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.3 MB)
- Length: 0:05:21.985 (321.985 s)
- Words: 829, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 799 of Whisper's 829 words (96.4%; Oyez has 822).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:05:21.180 | 821 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court this morning in Case 15-1391, Expressions Hair Design v. Schneiderman. Each time a customer pays for an item with a credit card, the merchant selling that item must pay a transaction fee to the company that issued the credit card. The petitioners in this case are New York merchants who say that these transaction fees cost them tens of thousands of dollars every year. Now, rather than increase their prices across the board to absorb these costs, the merchants want to pass the fees along only to their customers who choose to use credit cards. Now, there are two ways they could do this. First, they could charge higher prices to credit card users, a credit card surcharge. Or second, they could lower prices to customers who use cash at cash discount. The merchants who brought this case want to use the former approach, imposing a surcharge for credit. They want to do this to make it clear to their customers that they, the merchants, are not the bad guys. It is the credit card companies that are making them pay more, use a credit card, pay a surcharge. New York, however, has a law prohibiting credit card surcharges. The question before us is whether that law unconstitutionally regulates speech. Specifically, what the merchants want to do is post one cash price and then post an additional credit card surcharge, expressed either as a dollars-in-cents additional amount or a percentage increase. For example, Petitioner Expressions Hair Design might wish to post a sign outside its salon reading haircuts $10. We add 3 percent surcharge if you pay by credit card. Or Petitioner Brooklyn Pharmacy and Soda Fountain might list one of the sundaes on its menu as costing $10 with a 30-cent surcharge for credit card users. Now, the litigating parties all agree that New York's law would prohibit them from doing this. The merchants argue that in doing so, New York's law violates the First Amendment. The court that decided this case below, the Court of Appeals for the Second Circuit based in New York, ruled that the law did not violate the First Amendment. In fact, that court said that the law didn't implicate the First Amendment at all because it regulated only conduct, not speech. We have said that laws that regulate prices are conduct, not speech, regulations. The law that dictates that all New York delis can charge only $10 for their sandwiches just tells the deli owners how much they can collect each time they sell a sandwich. Now, of course, there will be an effect on speech. The waiters and waitresses can't say that the sandwiches cost something else, and the law regulates what deli owners may say on their signs.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:51.800 | at | or |
| 0:01:09.360 | a | of |
| 0:01:33.280 | -in | and |
| 0:01:48.360 | percent | (nothing) |
| 0:01:52.860 | Pharmacy and | Farmacy & |
| 0:02:25.960 | didn't | did not |
| 0:02:38.100 | The | A |
| 0:02:50.440 | an | in |
| 0:02:53.220 | can't | cannot |
| 0:03:12.020 | they're | they are |
| 0:03:29.720 | (nothing) | dollars |
| 0:03:53.480 | the | a |
| 0:03:53.880 | percent | (nothing) |
| 0:03:56.580 | (nothing) | dollars |
| 0:04:01.020 | price, wishes to | (nothing) |
| 0:04:37.400 | refrain | refrained |
