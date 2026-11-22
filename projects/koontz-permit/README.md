# koontz-permit: Supreme Court No. 11-1447

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2012/11-1447
- Audio: https://www.supremecourt.gov/media/audio/mp3files/11-1447.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2012/11-1447.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 15 min on 4 CPU cores
- Audio length: 1:03:36.725 (3816.725 s)
- `audio/argument.mp3`: mono, 64 kbps, 30.5 MB
- Official words: 3409 (plus 1 `(Laughter.)` markers), in 92 speaker turns
- ASR words: 3332
- Official words matched to an ASR word: 3116 of 3409 (**91.41%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 91.41% (threshold 85%).

125 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 11-1447 2012 koontz-permit --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:44:56.311 | 2696.311 | big | 2.12 | 1.80 | 28.8 | 37.0 | claim in this case, which is it's hard to see how you can have an exactions takings claim when nothing has ever actually been exacted -- Now, that is a problem. |

## Petitioner's opening, first 3 minutes

Everything said from 0:27:45.151 to 0:30:45.151, official wording, with each turn's start time. Interruptions from the bench are included.

[0:27:45.151] MR. BEARD: Your Honor, nothing was taken, either. In Nollan, you had a permit approval with conditions. It's true that development had not gone forward, but, here, as well, development had not gone forward. Presumably -- theoretically, if the development had gone forward, he might have been subject to conditions that he would have had to satisfy. But I would submit to the Court --

[0:28:06.055] JUSTICE SCALIA: The permit had issued. The permit had issued in both of those cases, and, therefore, the person was saying, to go ahead with this permit, I give up -- I give up this land.

[0:28:18.171] MR. BEARD: The permits in Nollan and Dolan actually did not issue. There was only approval, with conditions, and there is a difference. And that is no different from what happened here. The threat is the same. You don't get a permit issued to you until you --

[0:28:30.651] JUSTICE SCALIA: There was no approval with conditions. There's one thing for -- for a municipality to issue an -- an approval with conditions, and a municipality saying, we can't approval it unless you agree to these conditions. And the person doesn't agree, and the municipality says, we don't approve it.

[0:28:47.711] MR. BEARD: But, in either case, he -- he faces the threat, the unconstitutional condition on his use of his property, you don't get your use until you comply with our conditions. Mr. Chief Justice --

[0:28:58.791] JUSTICE KENNEDY: I -- I have one question. I know we -- you are running short on your rebuttal time. Assume that, when we look at this record, assume we think there is a due process violation, not a taking violation. That is not before us here, is it?

[0:29:15.351] MR. BEARD: No. The due -- there is no due process claim here. There is only a State statute that embodies sort of a due process standard, but there is no due process claim here. And may I reserve the balance of my time, Your Honor?

[0:29:26.411] CHIEF JUSTICE ROBERTS: And I will afford you some additional time, since our questioning intruded on yours.

[0:29:30.551] MR. BEARD: Thank you.

[0:29:32.971] CHIEF JUSTICE ROBERTS: Mr. Wolfson?

[0:29:35.151] MR. WOLFSON: Mr. Chief Justice, and may it please the Court: The parties agree that Florida may require a landowner to perform mitigation as a condition for a permit that would allow the destruction of a wetlands. The parties disagreed as to how much mitigation was appropriate in this case. The district thought that Mr. Koontz's proposal was insufficient to mitigate the -- the damage to wetlands. Mr. Koontz rejected the district's counterproposals, and he refused to do anything more. And the district denied his permit application because he refused to do anything more.

[0:30:07.691] CHIEF JUSTICE ROBERTS: Does it make any difference, in his refusing to do anything more, whether the condition is onsite or offsite?

[0:30:13.691] MR. WOLFSON: I don't think it makes any difference, Mr. Chief Justice, I mean, the -- under the Florida regulatory regime, we cannot demand certain conditions from the landowner. The -- we are obligated -- if the -- if the permit -- the landowner has to establish, under his permit application -- and it's his burden -- that he meets the various standards -- the public interest standard, which includes no adverse impact --

[0:30:38.771] CHIEF JUSTICE ROBERTS: Those are all State -- State law provisions you are talking about.

[0:30:40.431] MR. WOLFSON: Correct. Correct.

[0:30:40.491] CHIEF JUSTICE ROBERTS: What about is there -- is there anything in the Federal Constitution that

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 25, 2013.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2012/11-1447
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2012/11-1447/20130625o_11-1447.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:22.478 (262.478 s)
- Words: 601, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 560 of Whisper's 601 words (93.2%; Oyez has 593).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:10.140 | 16 |
| JUSTICE ALITO | 0:00:10.140 | 0:04:21.670 | 582 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Alito has the opinion of the Court in two cases this morning. The first case

[0:00:10.140] JUSTICE ALITO: is Kunz v. St. Johns River Water Management District number 11-1447. This case involves two of our important land use precedents, Nolan v. California Coastal Commission and Dolan v. City of Tigard. Those cases held that a unit of local government may demand property as a condition of its approval of a land use permit only if the demand has a nexus with and is roughly proportional to the public arms that the proposed land use would cause. Those cases thus serve to place at least some limits on the ability of local authorities to abuse their power. In this case, Petitioner Coy Kuntz applied to the St. Johns River Water Management District for a permit to build on land he owned east of Orlando, Florida. The district denied the application, telling Mr. Kuntz that it would approve the application only if he agreed to pay for improvements to State-owned property several miles away. Mr. Kuntz refused and instead sued in State court, alleging that the district's demand ran afoul of our decisions in Nolan and Dolan. The trial court applied those precedents and ruled for Mr. Kuntz, but the Florida Supreme Court reversed finding Nolan and Dolan distinguishable on two grounds. Today we reject both of those rationales and therefore reverse. First, the Florida Supreme Court thought that it made a difference whether a local authority says your permit is granted on the condition that you give us your property, as opposed to saying your permit is denied because you refuse to give us your property. We hold that Nolan and Dolan cannot be so easily circumvented. They are special applications of the unconstitutional conditions doctrine, which forbids the government from coercing someone into giving up a constitutional right. We have repeatedly held that this doctrine applies with equal force regardless of whether the government phrases its demand as a condition precedent or a condition subsequent to obtaining a governmental benefit. Under that well-settled principle, Nolan and Dolan apply regardless of whether permitting officials use the words only if or not unless. Second, and for similar reasons, we hold that the State Supreme Court should have applied Nolan and Dolan even though Respondent's demand was for money rather than a tangible interest in real property. Demands for money in the land

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:11.180 | Kunz v. St. | Koontz versus Saint |
| 0:00:14.760 | number 11 -1447. | No. 11-1447. |
| 0:00:22.480 | Nolan v. | Nollan versus |
| 0:00:47.200 | serve | served |
| 0:00:56.220 | Kuntz | Koontz |
| 0:00:57.820 | St. | Saint |
| 0:01:08.600 | Kuntz | Koontz |
| 0:01:17.100 | Kuntz | Koontz |
| 0:01:25.660 | Nolan | Nollan |
| 0:01:31.540 | Kuntz, | Koontz, |
| 0:01:35.060 | Nolan | Nollan |
| 0:01:58.230 | opposed | suppose |
| 0:02:01.750 | refuse | refused |
| 0:02:04.910 | Nolan | Nollan |
| 0:02:35.770 | Nolan | Nollan |
| 0:02:39.550 | use | used |
| 0:02:49.950 | Nolan | Nollan |
| 0:03:04.230 | Nolan | Nollan |
| 0:03:36.130 | then | than |
| 0:03:43.150 | Nolan | Nollan |
