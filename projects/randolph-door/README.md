# randolph-door: Supreme Court No. 04-1067

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/04-1067/20051108a_04-1067.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2005/04-1067.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 27 min on 4 CPU cores
- Audio length: 0:57:40.362 (3460.362 s)
- `audio/argument.mp3`: mono, 64 kbps, 27.7 MB
- Official words: 10530 (plus 8 `(Laughter.)` markers), in 334 speaker turns
- ASR words: 10312
- Official words matched to an ASR word: 9949 of 10530 (**94.48%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.48% (threshold 85%).

308 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 12 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 04-1067 2005 randolph-door --model small.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2005/04-1067.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/04-1067/20051108a_04-1067.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-48.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:20:28.200 | 1228.200 | small | 0.60 | 0.05 | 6.1 | 14.1 | what happens, I imagine that it would make a difference if the person who wants to -- who was invited in by the wife, is larger or smaller than the husband. |
| 2 | 0:20:33.240 | 1233.240 | under speech | 0.00 | 0.00 | - | - | in by the wife, is larger or smaller than the husband. And I think he probably would not go in if he thought he was a -- could not do so -- |
| 3 | 0:33:36.540 | 2016.540 | under speech | 0.12 | 0.00 | - | - | right to keep the policeman out than she has to have the policeman in? I think everybody makes their -- And vice versa. Yes. I think that -- Right. -- that's the point -- |
| 4 | 0:46:03.840 | 2763.840 | under speech | 0.00 | 0.00 | - | - | don't know what I'd do. If I imagine myself in a normal social situation, I think probably, if I am the typical person, which may or may not be, I -- |
| 5 | 0:51:54.320 | 3114.320 | under speech | 0.00 | 0.00 | - | - | Souter, let me return -- I want to make sure I -- But the -- I -- you assume we got -- there goes the -- that -- there goes any bright line administrable rule, I guess. |
| 6 | 0:54:47.300 | 3287.300 | small | 1.26 | 0.05 | 4.5 | 13.6 | I -- what the Courts of Appeals have confronted repeatedly, and uniformly agree -- and it's in our brief -- is that children satisfy the Matlock and Rodriguez -- So -- -- standard. -- would a mother-in-law. |
| 7 | 0:56:38.480 | 3398.480 | small | 0.60 | 0.25 | 14.1 | 17.6 | and get a warrant, which will define -- Was there anybody in that case who -- since I wrote it, I guess I'm supposed to know it in detail, but I don't -- |
| 8 | 0:56:46.940 | 3406.940 | under speech | 0.00 | 0.00 | - | - | There was nobody giving consent, was there? Oh, Justice -- Was there? Justice Breyer -- I'll go back and read it. -- she said, "I think you should" -- she said -- I'll reread it. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.120 to 0:03:06.120, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.120] MS. SMITH: Mr. Chief Justice, and may it please the Court: The question presented in this case is whether one occupant can give law enforcement valid consent to search the common areas of a premises shared with another, even though another occupant is present and objects to the search. The State of Georgia submits that the answer to this case is a resounding yes. It is reasonable to recognize that a person who satisfies Matlock's definition of common authority -- that is, a definition that is not based upon property-law concepts, but one who has mutual use of property by virtue of having joint access or control for most purposes -- can give consent for a search of that premises, in his or her own right.

[0:00:53.320] JUSTICE O'CONNOR: Do we look to what is socially acceptable? Is there some language to that effect in some of our cases?

[0:01:00.280] MS. SMITH: There has been some of that in some of the prior cases, Your Honor, that you do look to social norms. You've also said --

[0:01:06.500] JUSTICE O'CONNOR: Do you think it is the norm that, if there are co-inhabitants of a house or apartment, that it's okay to let a stranger in, against the express wishes of your spouse or co- inhabitant?

[0:01:25.760] MS. SMITH: I think that is --

[0:01:26.640] JUSTICE O'CONNOR: You think that's socially acceptable?

[0:01:28.100] MS. SMITH: I think it is -- I think it is common, Your Honor. As much as one would like to think --

[0:01:32.580] JUSTICE O'CONNOR: Well, it might be common, but I'm not sure that's an acceptable kind of performance.

[0:01:39.300] MS. SMITH: Well, I think, Your Honor, we have what we have called either adduced expectation of privacy or a limited expectation of privacy or what we called a shared expectation of privacy, by making the decision, long before police appear at the door, to share this premises with someone. And by --

[0:01:57.272] JUSTICE O'CONNOR: What --

[0:01:57.388] MS. SMITH: -- that decision --

[0:01:57.620] JUSTICE O'CONNOR: -- what if the spouse had put a sign up, "No police allowed here"?

[0:02:02.260] MS. SMITH: I don't think that, even as -- in -- one could ensure that the spouse would honor the other person's wishes. I think this case is here to give some substance to the recognition in Matlock of the ability of the cotenant to consent, in his or her own right.

[0:02:21.900] JUSTICE KENNEDY: What --

[0:02:21.900] JUSTICE SOUTER: Is --

[0:02:21.900] JUSTICE KENNEDY: What about the extent of the search? Can the wife say, "It's okay for you to come in, and you can look in my husband's top drawer"?

[0:02:29.040] MS. SMITH: I think, Your Honor, that would be a question of fact, under the circumstances, to see whether the husband has exhibited some exclusive use of that drawer or whether the facts would demonstrate that she puts socks in there for him, she puts --

[0:02:44.440] JUSTICE KENNEDY: I mean, how does the --

[0:02:44.440] MS. SMITH: -- notes in there --

[0:02:45.140] JUSTICE KENNEDY: -- how does the policeman --

[0:02:45.140] MS. SMITH: -- for him --

[0:02:45.820] JUSTICE KENNEDY: -- so, how is the policeman supposed to know that?

[0:02:47.400] MS. SMITH: Well, I think -- looking -- we measure what is reasonable on the part of the police by looking to what they know. And Rodriguez made very clear, one does -- a policeman doesn't simply accept every invitation to enter. If there's some ambiguity or some uncertainty, the policeman has a duty to

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 22, 2006.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2005/04-1067
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/04-1067/20060322o_04-1067.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:31.673 (271.673 s)
- Words: 659, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 631 of Whisper's 659 words (95.8%; Oyez has 644).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| JUSTICE SOUTER | 0:00:00.000 | 0:04:30.900 | 651 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] JUSTICE SOUTER: Justice Souter has the opinion in number 04-1067, Georgia v. Randolph. This case comes to us on writ of certiorari to the Supreme Court of Georgia. The police responded to a call to go to a go to the home of Scott and Janet Randolph, where Janet told the police that there was evidence of Scott's drug use inside. Scott refused permission to search the house, but Janet consented. She led an officer to a bedroom where he observed a straw with powdery residue he suspected was cocaine. The officer collected the straw. Scott was later convicted of possession of cocaine after his motion to suppress that evidence was denied. The Supreme Court of Georgia held that the evidence had been illegally seized and should have been suppressed. We granted certiorari to resolve a split of authority on whether a physically present cooccupant's stated refusal to permit entry renders a warrantless search invalid as to him, despite a cooccupant's consent. We hold that the cooccupant's refusal is effective, and so affirm the Supreme Court of Georgia. In the United States v. Matlock, we held that a consent to search by one who possesses common authority over premises is valid as against an absent, non-consenting person with whom that authority is shared. We explained there that the common authority is not synonymous with a property interest, but instead is in significant part a function of commonly held understandings about the authority that co-inhabitants may exercise in ways that affect each other's interests. It is fair to say that a caller standing at the door of a shared premises would typically not go inside, despite one cooccupant's invitation, if the other occupants stood there saying, stay out. The visitor's reticence would reflect the common understanding that one co-tenant generally has no right to prevail over the express wishes of another in understanding which is in fact borne out in property law. Since the co-tenant wishing to open the door to a third party thus has no recognized authority in law or social practice to prevail over a present and objecting co-tenant, his disputed invitation without more gives a police officer no better claim to reasonableness in entering than the officer would have had in the absence of any consent at all. Accordingly, in the balancing of compelling in competing individual and government interests entailed by the bar to unreasonable searches, disputed permission is no match for the objecting individual's claim to the centuries-old principle of respect for the inviolability

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.520 | number 04 -1067, | No. 04-1067, |
| 0:00:16.800 | The | (nothing) |
| 0:00:18.760 | go to a | (nothing) |
| 0:00:58.580 | a | the |
| 0:01:20.980 | the | (nothing) |
| 0:02:04.640 | occupants | occupant |
| 0:02:15.400 | in | an |
| 0:02:44.820 | compelling in | (nothing) |
| 0:03:54.520 | the | a |
