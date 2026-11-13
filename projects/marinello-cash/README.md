# marinello-cash: Supreme Court No. 16-1144

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/16-1144
- Audio: https://www.supremecourt.gov/media/audio/mp3files/16-1144.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/16-1144_664d.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 40 min on 4 CPU cores
- Audio length: 1:00:51.816 (3651.816 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.2 MB
- Official words: 10046 (plus 7 `(Laughter.)` markers), in 295 speaker turns
- ASR words: 9604
- Official words matched to an ASR word: 9445 of 10046 (**94.02%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "jury" 3627.110-3630.630. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
  Not counted: `7212(a),` 3078.730-3083.050 (4.32 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 94.02% (threshold 85%).

395 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 31 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 16-1144 2017 marinello-cash --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-52.5 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:14:18.314 | 858.314 | under speech | 0.00 | 0.00 | - | - | think a lot of people do that? I mean, you've got three children and they say they've got five? In my experience -- well, in any case -- Well, your experience because -- |
| 2 | 0:14:25.580 | 865.580 | under speech | 0.00 | 0.00 | - | - | Well, your experience because -- -- experience -- I -- I was responding to Justice -- I mean, people who get caught come to you. So, in your experience, you see a lot of them. |
| 3 | 0:14:38.000 | 878.000 | big | 1.68 | 1.55 | 33.5 | 38.1 | them. Right. There may be a category problem there. I -- I agree. Yeah, there are people who list their dogs as dependents. Well, I'll defer to Justice Ginsburg on that. |
| 4 | 0:23:11.080 | 1391.080 | under speech | 0.00 | 0.00 | - | - | than merely passively receiving taxes. Well, and, of course, all of the conduct or omissions in this case are not in that context. Correct. So -- It's -- it's a friendly amendment. |
| 5 | 0:24:30.920 | 1470.920 | small | 0.33 | 0.00 | 4.7 | 5.3 | your proposal, but in any case, the -- the key part is unless there's a proceeding -- You just helped the government a lot with that statement. I hope I did not. |
| 6 | 0:27:13.460 | 1633.460 | under speech | 0.00 | 0.00 | - | - | a federal felon. Well -- For my -- for my friend's son's snow shoveling business. Well, I -- Right? I think that that -- I mean, the answer is yes, I think, isn't it? |
| 7 | 0:28:04.480 | 1684.480 | under speech | 0.00 | 0.00 | - | - | keeping records, failure to keep records -- Right. -- that you didn't -- that aren't lawfully obliged to be kept. You realize everybody in this audience now knows about the 1099 form, right? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.800 to 0:03:07.800, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.800] MR. HELLMAN: Thank you, Mr. Chief Justice, and may it please the Court: When Congress made it a felony to obstruct the due administration of the tax code, it was not creating an all-purpose tax crime; it was borrowing from a statute that prohibited the obstruction of a pending proceeding. This Court normally presumes that borrowed language carries its meaning with it. And that has to be the case here, for without that limitation, obstruction would swallow up the other crimes that Congress simultaneously enacted and, in particular, it would obliterate the careful line that Congress drew between misdemeanors and felonies. Indeed, the government's interpretation is so broad that it would chill entirely legitimate conduct that Congress never intended to penalize.

[0:00:47.180] JUSTICE GINSBURG: What -- what -- what lawful conduct would the government's reading put at risk?

[0:00:54.480] MR. HELLMAN: Certainly. There's a whole range because obstruction, on their definition, is so broad. For example, you could imagine a situation -- I'll take an everyday taxpayer, someone who pays their gardener, say, in cash, which is one of the predicate acts in this case as well. Paying in cash isn't necessarily illegal under the tax laws, but the test that the government would have is, by paying someone in cash, you're -- you're making it harder for the IRS to assess perhaps your tax liability or perhaps the tax liability of the person that you are paying. And at that question -- at that point, the only question that remains is mens rea, why did you do it? Did you do it for the purpose of obtaining an unlawful benefit? And even -- that benefit need not even be your own under the government's reading; it could be the benefit of the gardener. Or to take another example, imagine a taxpayer who says I'm going to keep every document the law requires under the code. I'll keep every document but no documents more. If the IRS ever came back and looked at that person's tax position, they might say your failure to keep these documents that -- that aren't otherwise required hindered us in our ability to assess your taxes. At that point, again, the only question becomes the why, the mens rea. And with a felony prosecution on the line and with so many acts, the actus reus being so broad, anything that hinders the IRS's ability to carry out a code, obstructs --

[0:02:27.800] JUSTICE SOTOMAYOR: My problem is that I have -- a second question.

[0:02:31.680] MR. HELLMAN: Sure.

[0:02:32.500] JUSTICE SOTOMAYOR: I have a lot of hypotheticals under your definition of what this section means that wouldn't be covered. So how about if an individual knows that the IRS is in the presence of -- press -- in the process of assessing his taxes and he in some way obstructs that process, or an agent -- the agent in 2004 called the defendant and said: You know, I'm deciding whether to open an investigation. I haven't, but I'm just thinking about it. I

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 21, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/16-1144
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/16-1144/16-1144_20180321-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.5 MB)
- Length: 0:05:58.792 (358.792 s)
- Words: 789, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 767 of Whisper's 789 words (97.2%; Oyez has 780).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.380 | 13 |
| JUSTICE BREYER | 0:00:07.280 | 0:05:57.760 | 774 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: And Justice Breyer has our opinion in Case 16-1144, Maranello v. United States.

[0:00:07.280] JUSTICE BREYER: Breyer, there's a statutory clause which is called the omnibus clause in the Internal Revenue Code, and that clause makes it a felony, quote, corruptly or by force to, quote, endeavor to obstruct or impede the due administration of this title, i .e., the tax code. The question here is how broadly we should interpret this language. Does it cover efforts to impede virtually any and every tax-related administrative activity in the Internal Revenue Code? Or is it more limited in scope, covering only specific administrative proceedings such as a pending investigation or audit? Well, we conclude that to show a violation of the clause, the government has to show a nexus between the defendant's conduct and a particular administrative proceeding such as an investigation or an audit or the like. And that proceeding must have been pending or at least reasonably foreseeable at the time the defendant engaged in the instructive conduct, that is, a narrow interpretation. In interpreting the omnibus clause, we follow the approach this Court set forth in the United States v. Aguilar, a case in which we interpreted the statute that made it a felony, very similar language, corruptly or by threats of force to impede the due administration of justice. There we held that the statute contained a similar nexus requirement. We said that the obstructive conduct had to have a nexus to a particular judicial proceeding. We adopted this more targeted interpretation of the statute because we, quote, have traditionally exercised restraint in assessing the reach of a Federal criminal statute out of deference to the prerogatives of Congress and out of concern that a fair warning should be given to the world in language that the common world will understand of what the law intends to do if a certain line is passed. We believe those same considerations apply here. Congress embedded the omnibus clause in the middle of a statutory paragraph that focuses more narrowly upon obstructing government officers or employees, not impeding any and every part of what the government has called the, this is the government's word, quote, continuous, ubiquitous, and universally known tax code. Moreover, to read the statute broadly risks transforming quite a few activities that the code classifies as misdemeanors into felonies. The government points out, correctly, that only corrupt impeding is at issue. It contends

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:00.000 | And | (nothing) |
| 0:00:02.360 | 16 -1144, Maranello v. | 16-1144, Marinello versus |
| 0:00:07.280 | Breyer, there's | There is |
| 0:01:00.040 | and | in |
| 0:01:13.540 | instructive | obstructive |
| 0:01:21.880 | the | (nothing) |
| 0:02:35.360 | the, | these, |
| 0:02:36.260 | (nothing) | are |
| 0:04:15.700 | end quote, | (nothing) |
