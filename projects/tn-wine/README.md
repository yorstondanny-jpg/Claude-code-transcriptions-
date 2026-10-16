# tn-wine: Supreme Court No. 18-96

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/18-96
- Audio: https://www.supremecourt.gov/media/audio/mp3files/18-96.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/18-96_09m1.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 47 min on 4 CPU cores
- Audio length: 0:51:03.888 (3063.888 s)
- `audio/argument.mp3`: mono, 64 kbps, 24.5 MB
- Official words: 8364 (plus 5 `(Laughter.)` markers), in 217 speaker turns
- ASR words: 8128
- Official words matched to an ASR word: 7652 of 8364 (**91.49%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 91.49% (threshold 85%).

322 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 25 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 18-96 2018 tn-wine --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-48.2 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:23:28.060 | 1408.060 | big | 4.32 | 2.65 | 22.4 | 33.8 | this issue. Suppose you -- law: Any liquor store has to use paint made in Tennessee, asphalt made in Tennessee for the parking lot, neon -- you know, I can go on. |
| 2 | 0:23:57.120 | 1437.120 | medium | 1.46 | 0.65 | 19.2 | 28.9 | reason for saying the out-of-state owner has to be -- live here for 12 years, as there is to say paint. In fact, a better reason because Tennessee paint's really good. |
| 3 | 0:37:51.160 | 2271.160 | small | 1.02 | 0.00 | 2.9 | 6.9 | and the history and the absence of any discrimination forbidden by others, this has been the law for 100 years. Don't change it. Not all law makes that much sense. |
| 4 | 0:42:26.140 | 2546.140 | medium | 0.52 | 0.40 | 33.9 | 38.7 | because, under these circumstances, as the camel at least, or I guess I'm the nose of the camel, that's not what I'm looking for. I think you may be, yes. |
| 5 | 0:47:44.060 | 2864.060 | under speech | 0.00 | 0.00 | - | - | not a close case. I'm sorry, Your Honor. Isn't that exactly where you want us to go? Not today, of course, but tomorrow or next year. Or maybe not ever. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.160 to 0:03:09.160, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.160] MR. DVORETZKY: Mr. Chief Justice, and may it please the Court: In the wake of the nation's failed experiment with prohibition, the Twenty-First Amendment restored to the states the powers that they previously had under the Wilson and Webb-Kenyon Acts. In exercising those powers, both before prohibition and in its immediate aftermath, states enacted residency requirements, like Tennessee's, to regulate the sale of alcohol within their territory. All along the way, this Court recognized the states' power to do so as part of their virtually complete control over how to structure the liquor distribution system. Under Granholm, that unbroken and undisputed history is dispositive. Residency requirements like Tennessee's are protected from dormant Commerce Clause scrutiny because they were authorized by the Wilson and Webb-Kenyon Acts and uniformly considered constitutional at the time of ratification. Respondents offer --

[0:00:59.920] JUSTICE SOTOMAYOR: Could I ask you to clarify for me your position? Justice Sutton, in his dissent, basically said, if your legislature came and said we don't want out-of-state wholesalers, distributors, or retailers to be in our chain of distribution, because they're going to take business away from our local enterprises, period, end of story -- are you saying that the state can do that? Are you disagreeing with Justice -- with Judge Sutton? Or do you think that there's an economic protectionism -- protection against what a state can do?

[0:01:50.200] MR. DVORETZKY: So I don't think that there is an economic protectionism exception to the Twenty-First Amendment, but even if there were one, as Judge Sutton recognized in applying his test to the two-year residency requirement in this case --

[0:02:01.700] JUSTICE SOTOMAYOR: The problem is --

[0:02:01.700] MR. DVORETZKY: -- we would still prevail.

[0:02:03.000] JUSTICE SOTOMAYOR: Well, except we have a difficulty there, which is you can't look at legislation piecemeal. You have to look at it as a whole. It was written as a whole. It's one paragraph that says two years, plus 10. So it's really 12 years because -- and he said there's no economic justification for a 10-year residency requirement. So what you have to look at is not whether it's two years but whether there's any reason for a 12-year residency requirement. I mean, if he said no to 10, then it's no to 12.

[0:02:41.620] MR. DVORETZKY: So, Justice Sotomayor, that -- that gets us into a severability question. And --

[0:02:45.380] JUSTICE SOTOMAYOR: But -- but let's go back to my initial question. Yes, it does. And -- and that's a separate question, and you can argue that one back and forth. But my fundamental question is the -- you believe the Twenty-First Amendment permits states to discriminate against out-of-state interests, then does that mean Bacchus, Granholm,

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 26, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/18-96
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/18-96/18-96_20190626-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 2.1 MB)
- Length: 0:08:34.743 (514.743 s)
- Words: 1239, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1196 of Whisper's 1239 words (96.5%; Oyez has 1224).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:07.340 | 15 |
| JUSTICE ALITO | 0:00:08.220 | 0:08:33.420 | 1207 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Alito has our opinion in Case 1896, Tennessee Wine and Spirits Retailers v. Thomas.

[0:00:08.220] JUSTICE ALITO: this case concerns the constitutionality of a provision of Tennessee law that imposes a durational residency requirement on all applicants for a license to operate a liquor store. The particular provision at issue is part of a set of very demanding residency requirements. One provision precludes the renewal of a license unless the applicant has resided in Tennessee for 10 consecutive years. Another provision provides that a corporation cannot get a license unless every one of its stockholders is a Tennessee resident. The Court of Appeals for the Sixth Circuit struck down those two provisions as blatant violations of the Commerce Clause, and no one defends them in this Court. This case involves another part of the Tennessee scheme, a provision that requires applicants for a new license to show that they have resided in the State for the previous two years. After the Attorney General of Tennessee advised that this provision unconstitutionally discriminates against interstate commerce, the State's alcoholic beverage commission stopped enforcing it. The Respondents in this case, neither of which satisfied the two-year residency requirement, then applied for licenses. In response, Petitioner, an association of Tennessee liquor retailers, threatened to sue the State if it did not enforce the requirements against Respondents, and this litigation follows. Now, everyone agrees that the State's two-year residency requirement favors the economic interests of in-state residents and citizens over their out-of-state counterparts. And for that reason, the residency requirement implicates the Federal Constitution's Commerce Clause, which provides that Congress shall have the power to regulate commerce among the several States. Although the clause is framed as a positive grant of power to Congress, this Court has long held that it also prohibits State laws that unduly restrict interstate commerce. This interpretation, which is generally known as the Dormant Commerce Clause, has been the subject of thoughtful criticisms by members of this Court in recent years. But the proposition that the Commerce Clause, by its own force, restricts State protectionism has very deep roots that go back as far as Chief Justice Marshall's 24 decision in Gibbons v. Ogden. And that is not surprising. One of the main reasons for calling the Constitutional Convention in Philadelphia in 1787 was to remove the trade barriers that had been erected by the States during the Articles

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:08.220-0:00:08.220: "Alito,"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:01:24.480 | satisfied | satisfy |
| 0:02:42.480 | 24 | 1824 |
| 0:03:52.700 | the | (nothing) |
| 0:03:56.720 | 21st | Twenty-first |
| 0:04:11.840 | regulated, | regulate it |
| 0:05:03.280 | stood | started |
| 0:05:05.460 | 18th | Eighteenth |
| 0:05:17.540 | 21st | Twenty-first |
| 0:05:21.520 | 21st | Twenty-first |
| 0:05:23.360 | 18th | Eighteenth |
| 0:05:35.380 | 21st | Twenty-first |
| 0:07:24.580 | the | a |
| 0:07:28.680 | (nothing) | And |
| 0:08:24.500 | 21st | Twenty-first |
| 0:08:30.980 | descending | dissenting |
