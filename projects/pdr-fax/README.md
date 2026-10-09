# pdr-fax: Supreme Court No. 17-1705

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/17-1705
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-1705.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-1705_d18f.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 32 min on 4 CPU cores
- Audio length: 1:00:25.536 (3625.536 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.0 MB
- Official words: 11263 (plus 10 `(Laughter.)` markers), in 378 speaker turns
- ASR words: 10726
- Official words matched to an ASR word: 10439 of 11263 (**92.68%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.68% (threshold 85%).

491 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
cluster if it ends at the word's end, and is left alone otherwise. When the only sound in the span
is right at its start (or there's none), followed by a second or more of silence, the word is cut
to that sound, at least 0.2 s from its start. This trimmed 12 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-1705 2018 pdr-fax --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-49.9 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:10:47.700 | 647.700 | under speech | 0.00 | 0.00 | - | - | providing a private cause of action. So, if I think -- if I were to think -- I'm not there yet -- that there's no due -- There's hope. You're telling me there's hope. |
| 2 | 0:23:10.280 | 1390.280 | big | 1.48 | 1.30 | 28.5 | 37.0 | question too, which you can tell me both, and that is what happens -- a lot of rules are -- these are my only two questions. Can I -- shall I ask both? |
| 3 | 0:30:49.020 | 1849.020 | medium | 2.94 | 1.25 | 15.0 | 25.8 | Bob must pay the government $100 every year. All right? And a young man is born after the regulation is adopted, and he didn't -- he didn't read the Federal Register. |
| 4 | 0:30:55.940 | 1855.940 | medium | 1.66 | 1.05 | 15.5 | 19.9 | man is born after the regulation is adopted, and he didn't -- he didn't read the Federal Register. Shocking, huh? Yes. Maybe a lot of people don't read the Federal Register. |
| 5 | 0:30:59.560 | 1859.560 | medium | 1.56 | 0.40 | 10.9 | 14.7 | he didn't -- he didn't read the Federal Register. Shocking, huh? Yes. Maybe a lot of people don't read the Federal Register. Maybe they can't read it. It's in eight-point font. |
| 6 | 0:33:50.360 | 2030.360 | big | 3.60 | 3.10 | 21.8 | 28.4 | you if you'd like. It says: Rule at the beginning of the APA means the whole or part of an agency statement of general or -- oh, that's rule. Wrong place. |
| 7 | 0:34:07.300 | 2047.300 | under speech | 0.00 | 0.00 | - | - | or -- oh, that's rule. Wrong place. God, that's -- here -- where is it? Definitions. Well, it says order somewhere. I just read it. Okay. Let somebody else ask a few questions. |
| 8 | 0:40:18.100 | 2418.100 | small | 0.98 | 0.05 | 6.9 | 17.5 | PDR had other options available to it, other than taking a Hobbs Act petition in 2006. Do you know how many pages were issued in the Federal Register in 2018? |
| 9 | 0:40:38.460 | 2438.460 | medium | 0.84 | 0.55 | 23.3 | 30.7 | saw somebody riding home on the Metro at midnight in Washington, D.C., reading the Code of Federal Regulations, and I thought: Only in Washington, D.C., could you see this sight. |
| 10 | 0:40:45.820 | 2445.820 | under speech | 0.00 | 0.00 | - | - | and I thought: Only in Washington, D.C., could you see this sight. But you think people out in other parts of the country are -- they're waiting for the latest addition -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.480 to 0:03:09.480, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.480] MR. PHILLIPS: Thank you, Mr. Chief Justice, and may it please the Court: The most startling comment in the Fourth Circuit's opinion in this case is the following one: "We need not harmonize the FCC's rule with the underlying statute." I would have thought, in any ordinary instance of judicial review of administrative agency decision-making, that's a statement that ought to leap out off the page, and when it's being applied in the context of a private right of action brought as a class action by private plaintiffs against a private defendant who is seeking to assert that the statute is not violated by the action of the defendant, the idea that the court of appeals will say, no, no, there's no opportunity and no reason for the courts to entertain the agency's standard to be applied in those circumstances is one that, it would seem to me, you could only justify in extraordinary circumstances that are candidly not presented.

[0:01:02.400] JUSTICE SOTOMAYOR: That -- that -- that's a bit what's unusual about this case. It's a different question whether the court of appeals can do it because the Hobbs Act gives it exclusive jurisdiction, and I think the exclusive jurisdiction has to mean something. And that it then doesn't become a matter of jurisdiction; it becomes a matter of how much, if any, deference this interpretation is due than the question we granted cert on, which is, what does the district court -- what can the district court do as opposed to the court of appeals?

[0:01:40.140] MR. PHILLIPS: Can --

[0:01:41.140] JUSTICE SOTOMAYOR: So, here, the district court, I understand, didn't think it was challenging the validity of the order, or that you were, of -- of the FDC interpretation. It was interpreting it.

[0:01:54.780] MR. PHILLIPS: Right.

[0:01:55.940] JUSTICE SOTOMAYOR: So where does that leave --

[0:01:56.620] MR. PHILLIPS: But it was interpreting it in -- in -- in light of the statute, candidly.

[0:02:00.520] JUSTICE SOTOMAYOR: Well, but --

[0:02:01.480] MR. PHILLIPS: Can -- can --

[0:02:01.480] JUSTICE SOTOMAYOR: -- yes, I agree with you, it's interpreting, but that's what applied challenges are about, aren't they? They're here's the statute, here's the interpretation, your facts are unique, and we now as judges decide whether or not that uniqueness falls within or without the interpretive guideline or the -- the statute.

[0:02:26.920] MR. PHILLIPS: I mean, there --

[0:02:27.370] JUSTICE SOTOMAYOR: That's a normal process, isn't it?

[0:02:28.780] MR. PHILLIPS: Right. There -- there are two things that come out of that question that I'd like to address. The first one is, what is the -- the work that's done by the requirement of exclusive jurisdiction in the Hobbs Act? And we would say that the exclusive jurisdiction under the Hobbs Act says the court of appeals can decide whether and only -- you know, whether they can enjoin, set aside, suspend in whole or part --

[0:02:49.720] JUSTICE SOTOMAYOR: Put that aside, because that's -- assuming I don't accept that, that the court of appeals has exclusive jurisdiction, period, and we have plenty of statutes that give courts of appeals exclusive jurisdiction over matters. So, if you're not challenging the validity of the Hobbs Act, how do you -- and you accept it on its

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 20, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/17-1705
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/17-1705/17-1705_20190620-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.7 MB)
- Length: 0:02:49.247 (169.247 s)
- Words: 417, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 390 of Whisper's 417 words (93.5%; Oyez has 413).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:09.360 | 17 |
| JUSTICE BREYER | 0:00:10.960 | 0:02:47.280 | 399 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Breyer has our opinion this morning in Case 17-1705, PDR Network v. Carleton and Harris Chiropractic.

[0:00:10.960] JUSTICE BREYER: there are several Federal statutes known as the Hobbs Act. This one is quite technical and has to do with regulatory agencies. And it says that the final order of, for example, a Federal Communications Commission, that the court of appeals, Federal court of appeals, will have, quote, exclusive jurisdiction to enjoin, set aside, suspend, or determine the validity of the order. In this case, a district court wanted to determine the validity of the order, and the court of appeals to the Fourth Circuit said, no, just the court of appeals, you have to take the order as given. Well, the case is more difficult than my summary made it sound, and what we're doing is sending it back because we think we can't answer the question until the court of appeals decides two preliminary matters. The first matter is what kind of an order is this? It's a rule, but is it a legislative rule, which is just like law, or is it an interpretive rule, which is just the FCC's idea of a law, of what the statute means, and it isn't a law itself automatically. And we want them to answer that because we think that if it's an interpretive rule, maybe, we're not saying definitely, the district court could go ahead. And then the next question we want them to answer is whether the party here, the PDR network, had a, quote, prior and adequate opportunity to actually go to the court of appeals when the first rule came out. Did they have a chance to get the thing reviewed at all? Because if they didn't, then they have a stronger claim that the district court should review it now. Again, we don't say anything definitely. All we do is we send the case back and we ask the court of appeals to decide those two preliminary questions, and then maybe, eventually, we will answer the question that the parties wanted us to answer. Oh, wait. There are several, yes. Breyer. Actually, we didn't even agree on that. There is a majority for it. And that majority vacates the judgment, sends it back to determine they consider these issues. Justice Thomas has filed an opinion concurring in the judgment in which Justice Gorsuch joins. Justice Kavanaugh has filed an opinion concurring in the judgment in which Justice Thomas, Justice Alito, and Justice Gorsuch join.

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:10.960-0:00:11.580: "Breyer,"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:07.280 | Carleton and | Carlton & |
| 0:00:21.200 | of, | (nothing) |
| 0:00:22.040 | a | the |
| 0:00:44.400 | to | for |
| 0:00:46.340 | just | as |
| 0:00:57.200 | we're | we are |
| 0:00:59.440 | can't | cannot |
| 0:01:08.440 | It's | It is |
| 0:01:20.460 | and | (nothing) |
| 0:01:21.040 | isn't | is not |
| 0:01:26.400 | it's | it is |
| 0:01:28.500 | we're | we are |
| 0:01:52.260 | didn't, | did not, |
| 0:01:58.360 | don't | do not |
| 0:02:16.660 | Oh, wait. There are several, yes. Breyer. | (nothing) |
| 0:02:19.600 | didn't | did not |
