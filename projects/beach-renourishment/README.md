# beach-renourishment: Supreme Court No. 08-1151

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-1151/20091202a_08-1151.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2009/08-1151.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 44 min on 4 CPU cores
- Audio length: 1:03:02.687 (3782.687 s)
- `audio/argument.mp3`: mono, 64 kbps, 30.3 MB
- Official words: 11559 (plus 11 `(Laughter.)` markers), in 350 speaker turns
- ASR words: 11213
- Official words matched to an ASR word: 10598 of 11559 (**91.69%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 2 words longer than 3 s outside laugh positions.
  Offending words: "oceanography" 2648.500-2651.820, "what" 2669.100-2673.300. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 91.69% (threshold 85%).

538 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 18 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 08-1151 2009 beach-renourishment --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2009/08-1151.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-1151/20091202a_08-1151.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:08:00.380 | 480.380 | medium | 1.52 | 0.95 | 17.0 | 23.9 | that cannot be -- So what does the statute say about your right to have peaceful enjoyment of your land? Well, you can have quiet hot dog stands during the daytime. |
| 2 | 0:19:48.960 | 1188.960 | under speech | 0.00 | 0.00 | - | - | that -- that the public can use, and that may wash away in 6 years anyway, and if they're lucky the State won't have enough money to put it back? Or -- |
| 3 | 0:21:06.420 | 1266.420 | small | 0.74 | 0.05 | 9.7 | 12.3 | 200-foot accreting beach. These property owners did not view that they were gaining anything. It may not change the property line, but all of your property might be under water -- |
| 4 | 0:26:34.685 | 1594.685 | under speech | 0.00 | 0.00 | - | - | When I read it, it seemed to me to deal with reliction precisely. I do think that's true, because the majority in Sand Key said that it dealt with them. |
| 5 | 0:26:42.960 | 1602.960 | under speech | 0.14 | 0.00 | - | - | majority in Sand Key said that it dealt with them. If there are no further questions, I’d like to reserve my time for rebuttal. A good lawyerly response. Thank you. |
| 6 | 0:30:03.660 | 1803.660 | under speech | 0.00 | 0.00 | - | - | avulsion, a hurricane may knock down their house. Does that mean the State could come in and knock down the house and say this is an artificial avulsion? No, absolutely -- |
| 7 | 0:39:27.740 | 2367.740 | under speech | 0.00 | 0.00 | - | - | some other act, right? Well, if there was -- if there were some other act where the legislature passes a law -- Right. Well, it's the Spring Break Act of 2010, okay? |
| 8 | 0:42:37.380 | 2557.380 | big | 3.54 | 3.40 | 29.4 | 36.2 | So it's not that it's a taking -- Absolutely. -- and you're compensating; it is a reason why this is a -- I am somewhat putting words in your mouth, but I mean -- |
| 9 | 0:42:45.760 | 2565.760 | big | 1.52 | 1.35 | 31.5 | 36.2 | a reason why this is a -- I am somewhat putting words in your mouth, but I mean -- Well, certainly our position is that there's no -- You won't disagree with that. |
| 10 | 0:44:02.800 | 2642.800 | under speech | 0.00 | 0.00 | - | - | this case it won't make a difference, because it's so reasonable, it’s -- there's not a taking. But what about -- what do you call those -- the spring fling, the spring break -- |
| 11 | 1:00:04.340 | 3604.340 | small | 0.78 | 0.05 | 8.0 | 15.3 | sand. Oh, no, no. This is -- you can't. You can't. What if it's going the opposite way? What if it's -- if they built up sand? I mean -- It's rock. Yes. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:11.680 to 0:03:11.680, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:11.680] MR. SAFRIET: Mr. Chief Justice, and may it please the Court: Today we ask this Court to expressly recognize that a State court decision, unpredictable in terms of relevant precedents, which redefines century-old property rights to no longer exist, violates the Fifth Amendment of the United States Constitution. The Florida Supreme Court suddenly and dramatically redefined littoral property rights, converting oceanfront property into oceanview property to avoid the finding of a taking. It did so in the context of a beach restoration project which could have been accomplished without taking any private property at all. Given this Court's jurisprudence that a State's legislative and executive branches cannot violate the Fifth Amendment, we see no reason why the judicial branch should be treated any differently.

[0:00:57.620] JUSTICE GINSBURG: I thought your basic position in the litigation in Florida was that the Florida legislation violated the takings protection, and so it's kind of strange to switch your target from the legislature, which enacted this measure, and then say, because the judiciary upheld it, the judiciary somehow is complicit in this violation by the legislature implemented by the administrative offices.

[0:01:36.220] MR. SAFRIET: That is correct, Your Honor. Below, the case was litigated as one of a taking by the legislature when it passed the Act. When it passed the Beach and Shore Preservation Act, it contained a provision within section 161.141, which is a savings clause, that said to the extent the beach restoration cannot be accomplished without taking property rights, the requesting authorities have to use eminent domain proceedings to take those rights. At the First District Court of Appeal, they agreed with us that the littoral rights were being taken by the Act of the legislature and that those had to be compensated for. When we arrived at the Florida Supreme Court, again, all of the parties were arguing those issues, whether there was a physical taking of these rights or a regulatory taking of these rights by the Act and whether the savings clause would apply. To everybody's shock, the Florida Supreme Court said: We're going to go back to step one and decide you don't have any littoral rights. The legislature didn't eliminate any protected littoral rights that you thought you once had for over a hundred years as the relevant precedents in common law indicate. So it was that decision of the Florida Supreme Court, that said you have -- no longer have property, that gives rise to the issue before this Court is, can the Florida Supreme Court redefine those 100-year-old rights to no longer exist?

[0:02:52.920] JUSTICE GINSBURG: Applied in a new situation. It was never the kind of situation involved here with the beach restoration project. The -- the precedent did not involve the kind of situation that

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 17, 2010.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2009/08-1151
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-1151/20100617o_08-1151.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 2.2 MB)
- Length: 0:08:31.817 (511.817 s)
- Words: 1320, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (1 turn), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 1256 of Whisper's 1320 words (95.2%; Oyez has 1298).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:08:31.100 | 1315 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Scalia has the opinion of the Court in Case 08-1151, Stop the Beach Renourishment Incorporated v. The Florida Department of Environmental Protection. He has asked that I announce the opinion for him. In this case, on writ of certiorari from the Supreme Court of Florida, we deal with complicated facts and the summary that follows leaves out some minor details. Under Florida law, the State owns, in trust for the public, land permanently submerged beneath navigable waters and the land between the low tide line and the mean high water line. Thus, the mean high water line is the ordinary boundary between private beachfront or littoral property and State-owned land. Littoral owners have certain rights that include, as relevant here, the right to ownership of accretions to their littoral property. An accretion is an addition to shore property that occurs gradually and imperceptibly. An addition created by a sudden change, such as a hurricane, is called an avulsion and does not belong to the littoral owner. When an avulsion occurs, the seaward boundary of littoral property remains what it was, the mean high water line before the event. Thus, when an avulsion has added new land, the littoral owner no longer owns oceanfront, and any later accretions to the new land belong to the owner of the seabed, which is ordinarily the State. Florida's Beach and Shore Preservation Act establishes procedures for restoration projects that consist of depositing sand on eroded beaches. When such a project is undertaken, the Respondent Board of Trustees of the Internal Improvement Trust Fund, which holds title to the seabed, sets a fixed erosion control line to replace the fluctuating mean high water line as the boundary between littoral property and State property. Once the new line is recorded, the common law ceases to apply. Thereafter, when accretion moves the mean high water line seaward, the littoral property remains bounded by the permanent erosion control line and is thus no longer oceanfront property. Respondents of the city of Destin and Walton County sought permits to restore 6.9 miles of beach eroded by several hurricanes, adding about 75 feet of dried sand seaward of the mean high water line, which was to become fixed as the erosion control line. Petitioner, a nonprofit corporation formed by owners of oceanfront property bordering the project, brought an unsuccessful administrative challenge. Respondent, the Florida Department of Environmental Protection, approved the permits and this suit followed. The district court of appeal for the first district concluded that the department's order had eliminated the Petitioner member's right to

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:07.060 | Incorporated v. | Inc. versus |
| 0:00:51.900 | (nothing) | the |
| 0:00:55.600 | an | in |
| 0:01:36.360 | consist | consists |
| 0:02:16.340 | property. Respondents of | property.Respondents, |
| 0:02:29.320 | dried | dry |
| 0:02:41.840 | the | a |
| 0:03:04.640 | and | an |
| 0:03:42.580 | re | we |
| 0:03:43.100 | to | (nothing) |
| 0:03:55.360 | Though | Well, |
| 0:03:56.100 | taking | thinking |
| 0:04:06.980 | have held | upheld |
| 0:04:09.120 | recharacterizes | recharacterize |
| 0:04:41.640 | recommend | recommends |
| 0:04:54.560 | sum, | some, |
| 0:04:59.320 | of | to |
| 0:05:01.320 | exists, | exist. |
| 0:05:23.260 | lack | lacked |
| 0:05:59.800 | there is | there's |
| 0:06:03.100 | than | the |
| 0:06:07.680 | (nothing) | Now |
| 0:06:27.780 | precedence, end quote. | precedents”. |
| 0:07:07.180 | unripe | un-right |
| 0:07:16.820 | jurisdictional, we deem | jurisdictionally deemed, |
| 0:07:53.060 | that | then |
