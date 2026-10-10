# quon-pager: Supreme Court No. 08-1332

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-1332/20100419a_08-1332.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2009/08-1332.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 41 min on 4 CPU cores
- Audio length: 1:01:38.260 (3698.260 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.6 MB
- Official words: 10257 (plus 8 `(Laughter.)` markers), in 303 speaker turns
- ASR words: 10117
- Official words matched to an ASR word: 9571 of 10257 (**93.31%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.31% (threshold 85%).

373 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 37 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 08-1332 2009 quon-pager --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2009/08-1332.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-1332/20100419a_08-1332.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-47.5 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00:44.800 | 44.800 | medium | 1.82 | 0.70 | 12.3 | 17.9 | Department in text messages on his department-issued pager in light of the operational realities of his workplace, which included the explicit no privacy in text messages policy. The written policy? |
| 2 | 0:14:46.120 | 886.120 | small | 0.44 | 0.15 | 18.0 | 24.6 | to them with e-mail, but that's just -- that's all in the record that suggests that. You know, if they were on duty 24/7, there weren't any off-duty messages, were there? |
| 3 | 0:34:39.440 | 2079.440 | under speech | 0.00 | 0.00 | - | - | 1,800 messages and I wanted to know which are personal and which are work-related, a good way to get at least a good first cut would be to read them. |
| 4 | 0:35:15.100 | 2115.100 | small | 1.12 | 0.00 | 6.0 | 9.0 | my coworkers and their wives and me, which happened to be the case here. Right. So I guess if you had asked for consent, the officer would have said no. |
| 5 | 0:35:36.320 | 2136.320 | under speech | 0.24 | 0.10 | 19.3 | 20.4 | have had the officers themselves count the messages. Well, the officer is going to say, hey, these are all big -- work-related. I’ll tell you that. I only had two. Well -- |
| 6 | 0:45:34.360 | 2734.360 | big | 1.88 | 1.65 | 22.6 | 29.6 | where it's coming from. And he's talking with a girlfriend, and he has a voice mail saying that your call is very important to us; we’ll get back to you? |
| 7 | 0:50:34.700 | 3034.700 | small | 1.22 | 0.05 | 10.4 | 21.9 | be processing the delivery of this message. And -- Well, I didn't -- I wouldn't think that. I thought, you know, you push a button; it goes right to the other thing. |
| 8 | 0:50:38.780 | 3038.780 | big | 2.84 | 2.70 | 29.4 | 35.7 | I wouldn't think that. I thought, you know, you push a button; it goes right to the other thing. Well -- You mean it doesn't go right to the other thing? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.860 to 0:03:07.860, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.860] MR. RICHLAND: Mr. Chief Justice, and may it please the Court: Under the less restrictive constitutional standards applied when government acts as employer, as opposed to sovereign, there was no Fourth Amendment violation here. First, Ontario Police Sergeant Jeff Quon had no reasonable expectation of privacy vis-à-vis the Ontario Police Department in text messages on his department-issued pager in light of the operational realities of his workplace, which included the explicit no privacy in text messages policy.

[0:00:43.960] CHIEF JUSTICE ROBERTS: The written policy? (Laughter.)

[0:00:46.620] CHIEF JUSTICE ROBERTS: The whole -- the argument here, of course, is that that was modified by the instructions he got from the lieutenant. Do we follow the written policy or the policy they allegedly enforced in practice?

[0:00:59.280] MR. RICHLAND: That is the argument, Mr. Chief Justice. But, in fact, there was no inconsistency between the no privacy in text messages aspect of the written policy and the oral information he was given. First of all, the written policy itself was broad enough to cover text messages. It stated, for example, at Appendix 152, that it applied to city-owned computers and all associated equipment. And again at 152: "City-owned computer equipment, computer peripheral, city networks, the Internet, e-mail, or other city-related computer services." And, finally, the agreement to the policy was that it applied -- this is at Appendix 156 -- to city-owned computers and related equipment. So certainly the written policy itself was broad enough to cover text messaging pagers, but in addition to that, nothing in the oral statements made by Lieutenant Duke undermined the no-privacy aspect of the written policy.

[0:02:02.460] CHIEF JUSTICE ROBERTS: Well, we are dealing with Mr. Quon's reasonable expectations, right?

[0:02:06.420] MR. RICHLAND: Yes, yes.

[0:02:06.620] CHIEF JUSTICE ROBERTS: And even with the written policy, he has the instructions -- everybody agrees -- you can use this pager for private communications.

[0:02:13.960] MR. RICHLAND: That’s correct.

[0:02:15.140] CHIEF JUSTICE ROBERTS: We’re not going to audit them. Right? That's what he said. He has to pay for them. Right? Now, most things, if you're paying for them, they’re yours. And this -- it particularly covered messages off-duty. Now, can't you sort of put all those together and say that it would be reasonable for him to assume that private messages were his business? They said he can do it. They said, you’ve got to pay for it. He used it off duty. They said they’re not going to audit it.

[0:02:41.940] MR. RICHLAND: Not when he was told at the same time that these text messages were considered e-mail and could be audited, and that they were considered public records and could be audited at any time; that is, it has to do with a different aspect of what the policy -- the oral policy --

[0:03:03.380] JUSTICE GINSBURG: In addition to -- that was said at the meeting -- and Lieutenant Duke,

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 17, 2010.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2009/08-1332
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-1332/20100617o_08-1332.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.6 MB)
- Length: 0:06:01.822 (361.822 s)
- Words: 913, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (2
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 864 of Whisper's 913 words (94.6%; Oyez has 919).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.620 | 0:00:07.540 | 16 |
| JUSTICE KENNEDY | 0:00:08.140 | 0:06:01.060 | 890 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.620 to 0:03:00.620, with each speaker's start time.

[0:00:00.620] CHIEF JUSTICE ROBERTS: Justice Kennedy has our opinion this morning in Case 08-1332, City of Ontario, California v. Kwan.

[0:00:08.140] JUSTICE KENNEDY: Kennedy. The City of Ontario is a political subdivision of the State of California. This case arose out of incidents when Jeff Kwan was employed by the Ontario Police Department. He was a police sergeant. He was also a member of the Special Weapons and Tactics Team. Those teams are commonly known as SWAT. The city issued pagers to Kwan and other SWAT team members, and these pagers could send and receive text messages. Under the city's service contract, each pager, and therefore each employee who had one, was allotted a limited number of characters sent or received each month. Use in excess of that amount would result in an additional fee. Within the first or second billing cycle, Kwan exceeded his monthly allotment. Lieutenant Duke was the officer in charge of the pagers. He reminded Kwan that under city policies, messages sent on the pagers were not private and could be audited. And Duke told Kwan that Duke could audit the messages. But he suggested that Kwan instead reimbursed the city for the entire overage fee to make an audit unnecessary. Kwan wrote a check to the city for the overage. Over the next few months, Kwan and other employees exceeded their character limits various times. Eventually, Duke informed the city, the chief of police, who was Chief Lloyd Scharf, that he was tired of being a bill collector. Chief Scharf decided to audit the messages on Kwan's pager as well as those of another employee who had exceeded his allowance in order to determine whether the existing character limits were too low and officers were having to pay for work-related messages. The audit revealed that Kwan sent numerous personal messages while on duty. Some were sexually explicit. Kwan was found to have violated department rules. Kwan and other respondents who were individuals who had corresponded with and communicated with Kwan on his pager filed suit. They alleged that the city, the department, and the Chief Scharf had violated their Fourth Amendment rights when reviewing the transcript and the text of Kwan's messages. The district court ruled for the defendants, but the United States Court of Appeals for the Ninth Circuit reversed. The panel concluded that Kwan had a reasonable expectation of privacy in the context of his messages and that the defendants had unreasonably violated that expectation by reviewing the transcript. We granted certiorari. The Fourth Amendment forbids unreasonable searches and seizures, and that provision guarantees the privacy, dignity, and security of persons against arbitrary and invasive acts by officers of the government. The Fourth Amendment applies when the government acts in its capacity as an employer.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:06.720 | v. Kwan. Kennedy. | versus Quon. |
| 0:00:15.420 | Kwan | Quon |
| 0:00:30.000 | Kwan | Quon |
| 0:00:55.540 | Kwan | Quon |
| 0:00:58.340 | Lieutenant | Lt. |
| 0:01:02.520 | Kwan | Quon |
| 0:01:08.960 | Kwan | Quon |
| 0:01:11.920 | Kwan | Quon |
| 0:01:12.660 | reimbursed | reimburse |
| 0:01:17.820 | Kwan | Quon |
| 0:01:18.600 | to | for |
| 0:01:21.840 | Kwan | Quon |
| 0:01:31.320 | was | (nothing) |
| 0:01:38.040 | Kwan's | Quon’s |
| 0:01:47.940 | to | the |
| 0:01:52.460 | Kwan | Quon |
| 0:01:58.660 | Kwan | Quon |
| 0:02:03.380 | Kwan | Quon |
| 0:02:06.600 | had | of course |
| 0:02:10.360 | Kwan | Quon |
| 0:02:19.760 | (nothing) | of -- |
| 0:02:21.720 | Kwan's | Quon’s |
| 0:02:29.800 | Kwan | Quon |
| 0:02:33.540 | (nothing) | and that the trans -- |
| 0:02:51.580 | and | an |
| 0:03:01.260 | presidents | precedents |
| 0:03:06.460 | whether | weather |
| 0:03:15.880 | (nothing) | and |
| 0:03:59.480 | Kwan | Quon |
| 0:04:09.560 | Sharf | Scharf |
| 0:04:10.700 | and ordered | in order |
| 0:04:41.960 | Kwan's | Quon’s |
| 0:04:47.640 | Kwan | Quon |
| 0:04:56.680 | that the | But if a |
| 0:04:59.940 | Kwan's | Quon's |
| 0:05:12.720 | Kwan's | Quon’s |
| 0:05:25.840 | (nothing) | one |
| 0:05:29.820 | post hoc | post-talk |
