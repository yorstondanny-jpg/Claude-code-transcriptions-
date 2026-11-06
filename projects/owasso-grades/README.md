# owasso-grades: Supreme Court No. 00-1073

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2001/00-1073/20011127a_00-1073.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2001/00-1073.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 28 min on 4 CPU cores
- Audio length: 0:57:27.641 (3447.641 s)
- `audio/argument.mp3`: mono, 64 kbps, 27.6 MB
- Official words: 9782 (plus 12 `(Laughter.)` markers), in 272 speaker turns
- ASR words: 9733
- Official words matched to an ASR word: 9345 of 9782 (**95.53%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.53% (threshold 85%).

296 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 3 times. ASR words with no official counterpart
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 00-1073 2001 owasso-grades --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2001/00-1073.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2001/00-1073/20011127a_00-1073.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:03:10.720 | 190.720 | big | 2.12 | 1.95 | 24.2 | 27.9 | Your Honor. Both the decisions of this Court, with all due respect, are sometimes difficult for a practicing attorney to discern a clear line of -- They're hard for us, too. |
| 2 | 0:09:55.400 | 595.400 | medium | 1.40 | 0.75 | 16.4 | 20.7 | either to erase it, or erases it herself, or himself. What's your definition of maintain, what, a week, a month? I don't think that -- Make me an offer. What's your -- |
| 3 | 0:10:17.840 | 617.840 | under speech | 0.00 | 0.00 | - | - | I think Congress was talking about -- and the legislative history bears this out. I know Your Honor is not particularly persuaded by that -- Some of my colleagues like that stuff. |
| 4 | 0:37:37.720 | 2257.720 | small | 0.50 | 0.00 | 5.0 | 9.8 | I remember in my third grade, my teacher, who thought it was her job to teach, had problems sometimes with discipline. And I might talk too much. I used to. |
| 5 | 0:38:50.613 | 2330.613 | under speech | 0.00 | 0.00 | - | - | for reasoned self-discipline. She says to the whole class -- that's how she keeps order in her class. That used to be true in the third grade. My teacher, Miss Rosmond -- |
| 6 | 0:38:57.340 | 2337.340 | under speech | 0.00 | 0.00 | - | - | the whole class -- that's how she keeps order in her class. That used to be true in the third grade. My teacher, Miss Rosmond -- -- whom I recall with fondness, did -- |
| 7 | 0:40:11.460 | 2411.460 | small | 2.10 | 0.15 | 7.3 | 14.4 | in which a teacher would run his or her classroom -- Senator -- -- for teaching and disciplinary purposes. And -- and if so, do we think that the Congress agreed with Senator Buckley? |
| 8 | 0:40:43.820 | 2443.820 | small | 0.52 | 0.00 | 2.9 | 5.8 | no gold stars on the -- on the paper that goes back to the student that any other student can see, or in these days, a Post-it with a happy face? |
| 9 | 0:52:40.640 | 3160.640 | under speech | 0.00 | 0.00 | - | - | as adults, I'm not doing this. I'm out of this class. I don't want people knowing what my -- I understand it's a -- You're out of the college. I mean, that -- |
| 10 | 0:53:44.870 | 3224.870 | under speech | 0.00 | 0.00 | - | - | was the intent of the teacher to make a record. A -- a good alternate name for this statute would have been the Anti -- the Prevention of Mutiny Among Students Act? |
| 11 | 0:54:46.520 | 3286.520 | big | 2.28 | 1.95 | 20.5 | 24.6 | paper. Encourage the parent to come and -- and be informed as to what is happening -- To have the student grade their own paper might have some problems with it too. |
| 12 | 0:55:16.720 | 3316.720 | medium | 5.12 | 1.85 | 19.2 | 30.8 | because they could write the answers on their hand. Well, you need two cheaters for that to work, whereas if you grade your own paper, it only takes one. Right? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:33.560 to 0:03:33.560, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:33.560] MR. RICHARDSON: Mr. Chief Justice, and may it please the Court: The issue presented by this case is whether Congress, in enacting the Family Educational Rights and Privacy Act, intended to prohibit the common and longstanding practice of peer grading of routine homework papers, quizzes, and tests. Congress did not intend FERPA to apply to such routine classroom activities, because Congress was concerned only with information that might have a long-term negative impact on a student's academic or career opportunities.

[0:01:02.140] QUESTION: Mr. --

[0:01:02.220] QUESTION: Did you take the position in the court of appeals that there is no private contract?

[0:01:11.080] MR. RICHARDSON: We did not raise that issue in the court of appeals, Your Honor. No, we did not.

[0:01:16.200] QUESTION: The court of appeals discussed it.

[0:01:18.720] MR. RICHARDSON: The court of appeals raised it sua sponte, and it has been raised in amicus briefs submitted -- in fact, three amici have discussed it.

[0:01:26.200] QUESTION: Why didn't you raise the issue? Why isn't that more important than what you did raise?

[0:01:31.600] MR. RICHARDSON: Candidly, Your Honor, we didn't raise it for a number of reasons. Number 1, because in the district court there was a Fourteenth Amendment claim which clearly was actionable under section 1983. Number 2, quite honestly we believe the merits argument regarding FERPA was stronger than the section 1983 argument. Remember --

[0:01:49.740] QUESTION: Well, I just don't know if it's a good practice for you to force us to reach an issue you think is important if there's no cause of action anyway. That just doesn't seem to me an orderly way to proceed.

[0:02:02.720] MR. RICHARDSON: Well, in hindsight I would agree with the Court that we should have approached it a different way. Please recall, however, that at the time this case was filed, at the time the court of -- at the time the district court entered its decision, and at the time the briefs were submitted in the Tenth Circuit, the Christiansen decision had not come down. We did not have the benefit -- we were under the impression, I should say, that we -- that the family policy compliance officer's letter would be accorded Chevron deference, as the district court did. We did not know that the Court was going to decide Christiansen and hold that such opinion letters were not entitled to such deference. We made a tactical decision to focus on the merits rather than focus --

[0:02:42.840] QUESTION: Well --

[0:02:42.840] MR. RICHARDSON: -- on the 1983 aspect of it.

[0:02:44.220] QUESTION: -- you also certainly had some justification on the private cause of action. Seeing a number of decisions from this Court which have come out 5 to 4 one way and then 5 to 4 the other way --

[0:02:55.300] MR. RICHARDSON: That's very true, Your Honor.

[0:02:56.540] QUESTION: -- you're not sure that you're going to prevail on that.

[0:02:59.120] MR. RICHARDSON: That's very true, Your Honor. Both the decisions of this Court, with all due respect, are sometimes difficult for a practicing attorney to discern a clear line of --

[0:03:08.980] QUESTION: They're hard for us, too. (Laughter.)

[0:03:12.840] MR. RICHARDSON: And the other factor I would say is that the two decisions that the Tenth Circuit cited from other courts of appeals, the only two decisions that we were aware of from the Second Circuit, the Fay v. South Colonie School District decision, and from the Fifth Circuit, Tarka v. Cunningham, both of those courts of appeals had held that FERPA was actionable under 1983, so

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - February 19, 2002.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2001/00-1073
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2001/00-1073/20020219o_00-1073.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.3 MB)
- Length: 0:05:07.383 (307.383 s)
- Words: 801, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 762 of Whisper's 801 words (95.1%; Oyez has 815).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE REHNQUIST | 0:00:00.000 | 0:00:08.700 | 20 |
| JUSTICE KENNEDY | 0:00:09.280 | 0:05:06.620 | 781 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE REHNQUIST: The opinion of the Court in No. 001073, Owasso Independent School District v. Falvo, will be announced by Justice Kennedy.

[0:00:09.280] JUSTICE KENNEDY: The Respondent's children are enrolled in the Owasso School District, which is a suburb of Tulsa, Oklahoma, and the teachers there sometimes ask the students to score each other's papers and assignments as the teacher explains the correct answers to the entire class, and this is called peer grading. The Respondent, the parents, claim that peer grading violates a Federal statute, which is called the Family Educational Rights and Privacy Act of 1974, and the act is sometimes referred to as FERPA. Asserting a violation of the act, the parents filed a 1983 action against the school district and other school officials. The act authorizes Federal funds to be withheld from school district that permits students' education records or the information contained in the record to be released without the parents' written consent. At the outset, we note that it's an open question whether the act provides private parties, like these parents, with a cause of action enforceable under 1983, and we've granted certiorari on this issue in another case, which we will hear later this term. For purposes of the present case, the Court assumes without deciding that FERPA provides private parties, like the parents, with a cause of action enforceable under 1983. The question now is, do they prevail in saying that these peer grading mechanisms are a violation of the act? The school district and the United States contend that education records include only institutional records, like student grade point averages, standardized test scores, and the records of disciplinary actions. But the parents, adopting the Tenth Circuit's reasoning, contend that teachers' grade books and the grades within are maintained by the teacher and are thus covered by the act. And the Court of Appeals reasoned that if the teacher cannot disclose the grades once they're written in the grade book, it makes no sense to permit the disclosure immediately beforehand. So the Court thus held, and the parents agree, that student graders maintain the grades under the act until they're reported to the teacher so they cannot be disclosed. Two statutory indicators show that the Ninth that the Tenth Circuit erred, first student papers are maintained by the student graders. In their view, and we conclude that this is incorrect, the word maintain suggests FERPA records will be kept in a filing cabinet in a records room at the school or on a permanent, secure database, perhaps even after the The student graders only handle assignments for a few minutes as the teacher calls out the answers. Second, a student grader is

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:01.200 | in | (nothing) |
| 0:00:13.480 | (nothing) | in |
| 0:00:18.260 | ask | asked |
| 0:00:32.980 | (nothing) | where the students grade each other’s papers. Now, |
| 0:00:48.480 | a | the |
| 0:01:03.120 | contained | contain |
| 0:01:08.780 | outset, | offset |
| 0:01:11.460 | it's | as |
| 0:01:18.460 | under | in the |
| 0:01:19.740 | we've | we have |
| 0:01:39.960 | these | this |
| 0:01:48.460 | contend | contain |
| 0:01:59.200 | adopting | adapting |
| 0:02:00.140 | Circuit's | Circuit |
| 0:02:01.820 | that | the |
| 0:02:07.500 | are | (nothing) |
| 0:02:14.320 | they're | they are |
| 0:02:26.180 | they're | they are |
| 0:02:31.800 | Ninth that the | (nothing) |
| 0:02:32.960 | erred, | aired: |
| 0:02:48.160 | on | in |
| 0:02:48.780 | secure | secured |
| 0:02:53.200 | (nothing) | student is no longer enrolled, |
| 0:03:15.300 | they're | they are |
| 0:03:36.180 | to | of |
| 0:04:19.940 | An | at |
| 0:04:21.200 | counseled | counsel |
| 0:04:21.960 | Respondent seemed | respondents seem |
| 0:04:33.200 | a | (nothing) |
| 0:04:38.280 | We doubt | With that |
| 0:04:41.360 | with | which |
| 0:04:50.740 | instructional | instruction on |
| 0:04:51.860 | in | and |
| 0:04:53.320 | the | this |
| 0:04:54.720 | is | does |
| 0:04:58.440 | statute | stature |
| 0:05:05.540 | comparing | concurring |
