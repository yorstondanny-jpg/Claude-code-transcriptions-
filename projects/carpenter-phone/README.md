# carpenter-phone: Supreme Court No. 16-402

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/16-402
- Audio: https://www.supremecourt.gov/media/audio/mp3files/16-402.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/16-402_6khn.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 35 min on 4 CPU cores
- Audio length: 1:22:01.872 (4921.872 s)
- `audio/argument.mp3`: mono, 64 kbps, 39.4 MB
- Official words: 13759 (plus 7 `(Laughter.)` markers), in 339 speaker turns
- ASR words: 13352
- Official words matched to an ASR word: 12952 of 13759 (**94.13%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.13% (threshold 85%).

463 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 30 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 16-402 2017 carpenter-phone --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-49.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:24:17.570 | 1457.570 | big | 1.96 | 1.65 | 24.1 | 31.8 | it seems to me there's a much more normal expectation that businesses have your cell phone data. I think everybody, almost everybody, knows that. If I know it, everybody does. |
| 2 | 0:39:13.910 | 2353.910 | small | 1.02 | 0.30 | 13.4 | 21.1 | but it's okay to get the cell phone records of someone who I -- I don't, but I know that most young people have the phones in the bed with them. |
| 3 | 0:49:18.350 | 2958.350 | small | 1.36 | 0.25 | 9.8 | 17.4 | you can -- But let's just -- let's -- I don't think you can make that assumption. -- let's stick with my hypothetical, counsel, okay? I know you don't like it. I got that. |
| 4 | 0:50:51.410 | 3051.410 | under speech | 0.00 | 0.00 | - | - | property interest, you're not here to deny that that would be a search of my paper and effect? I'm not here to concede it either. Okay. And the reason that -- |
| 5 | 1:00:13.970 | 3613.970 | under speech | 0.08 | 0.00 | - | - | I'd -- -- but how would you draw that line because that's the problem that's -- I'm not going to draw, Justice Breyer -- All right. How would -- how would you like to lose? |
| 6 | 1:10:37.030 | 4237.030 | small | 0.38 | 0.20 | 19.9 | 25.1 | leaving the other for the future. Does that work or does -- No. It -- Now, I know you'd say no -- It doesn't -- doesn't work. -- but I need to know the reason. |
| 7 | 1:20:56.030 | 4856.030 | small | 1.16 | 0.20 | 10.6 | 19.0 | further questions, we ask that you reverse the Sixth Circuit. Could I just ask you this question: Is any of this going to do any good for -- for Mr. Carpenter? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:17.700 to 0:03:17.700, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:17.700] MR. WESSLER: Thank you. Mr. Chief Justice, and may it please the Court: At issue in this case is the government's warrantless collection of 127 days of Petitioner's cell site location information revealing his locations, movements, and associations over a long period. As in Jones, the collection of this information is a search, as it disturbs people's long-standing, practical expectation that their longer-term movements in public and private spaces will remain private.

[0:00:46.040] JUSTICE KENNEDY: So what -- what is the rule that you want us to adopt in this case, assuming that we keep Miller -- Miller and Smith versus Maryland on the books?

[0:00:58.980] MR. WESSLER: The rule we seek is that longer-term periods or aggregations of cell site location information is a search and requires a warrant. We are not asking the Court to overturn those older cases. We think that the -- the lesson to be drawn from Riley and Jones and Kyllo is that any extension of pre-digital precedents to these kinds of digital data must rest on their own bottom.

[0:01:23.880] JUSTICE ALITO: How would you distinguish Miller?

[0:01:26.740] MR. WESSLER: Miller involved more limited records, certainly they could reveal some sensitive information, but more limited records and, as this Court held, they were voluntarily conveyed in that they were created by the passing of negotiable instruments into the stream of commerce to transfer funds. What we have here is both more sensitive and less voluntary.

[0:01:46.460] JUSTICE ALITO: Why is it more -- why is it more sensitive? Why is cell site location information more sensitive than bank records, which particularly today, when a lot of people don't use cash much, if at all, a bank record will disclose purchases? It will not only disclose -- everything that the person buys, it will not only disclose locations, but it will disclose things that can be very sensitive.

[0:02:14.220] MR. WESSLER: I absolutely agree, Justice Alito, that the information in bank records can be quite sensitive, but what it cannot do is chart a minute-by-minute account of a person's locations and movements and associations over a long period regardless of what the person is doing at any given moment.

[0:02:28.560] JUSTICE ALITO: Yeah, I understand that. But why is that more sensitive than bank records that show, for example, periodicals to which a person -- to which a person subscribes or hotels where a person has stayed or entertainment establishments -- establishments that a person has visited --

[0:02:46.240] JUSTICE KENNEDY: And particularly --

[0:02:46.240] JUSTICE ALITO: -- and all sorts of other things.

[0:02:47.980] JUSTICE KENNEDY: Particularly because the information in the bank records that Justice Alito referred to are not publicly known. Your whereabouts are publicly known. People can see you. Surveillance officers can follow you. It seems to me that this is much less private than -- than the case that Justice Alito is discussing.

[0:03:05.980] MR. WESSLER: Well, I -- I don't agree, Your Honor, for the following reason: When a person is engaged in a financial transaction, passing a -- a check, a negotiable instrument, that's

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 22, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/16-402
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/16-402/16-402_20180622-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.8 MB)
- Length: 0:07:17.316 (437.316 s)
- Words: 1106, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1082 of Whisper's 1106 words (97.8%; Oyez has 1100).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:07:16.120 | 1097 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court in Case 16-402, Carpenter v. United States. Cell phones work by continuously scanning their environment, picking up signals from the nearest cell site. Cell sites are antennas, usually on towers, but sometimes on buildings, flag poles, even church steeples. If you have a smartphone or something similar, it taps into the wireless network several times a minute, whether you're using one of its features or not, so long as the power is on. Every time the phone connects to a cell site, it generates a time-stamped record known as cell site location information, or CSLI. CSLI will show that your phone, which usually means you, was near that cell site at a particular time. Phone companies collect that information for their own purposes, currently retaining it for up to five years. That means that anyone with access to CSLI can track your movements over a period of several years. Now, in this case, the police suspected Timothy Carpenter of participating in the armed robbery of several Radio Shack and, ironically enough, T-Mobile stores. They knew his cell phone number and applied for court orders, but not search warrants, to get from his phone company the CSLI for the period during which the robberies took place. Altogether, the government was able to obtain some 13,000 location points cataloging Carpenter's movements over 127 days, more than 100 location points per day. Sure enough, the CSLI placed Carpenter, as the prosecutor told the jury, right where the robberies were at the exact time of the robberies. He was convicted and sentenced to over 100 years. The Fourth Amendment protects the right of the people to be secure in their persons, houses, papers, and effects against unreasonable searches and seizures. Our cases have said that its basic purpose is to safeguard the privacy and security of individuals against arbitrary invasions by government officials and to prevent too permeating police surveillance. Now, there are two major issues that have to be addressed in applying the Fourth Amendment to CSLI. The first is, how can you say that your privacy is invaded by a record of where you've been in public? We think the answer is that there is a difference between where you are at any particular moment in public and a record of where you've been every day, every moment, over several years. Now, in the past, the government could track you at most for a few days with the great expenditure of resources. But with CSLI, our cell phones become like ankle monitors,

### Words Whisper invented

None found.

Where Whisper's words differed from Oyez's and the re-run agreed with Oyez, the re-run's words and times replace the first pass:

- 0:06:55.680: "cases were mended" became "case is remanded"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:02:35.080 | you've | you have |
| 0:03:21.340 | privacy | Privacies |
| 0:04:15.100 | It's | It is |
| 0:04:18.120 | There's | There is |
| 0:04:56.440 | precedence | precedents |
| 0:05:44.940 | is | as |
