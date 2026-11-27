# lozman-arrest: Supreme Court No. 17-21

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/17-21
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-21.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/17-21_ljgm.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 5 min on 4 CPU cores
- Audio length: 0:59:44.088 (3584.088 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.7 MB
- Official words: 1705 (plus 2 `(Laughter.)` markers), in 34 speaker turns
- ASR words: 1667
- Official words matched to an ASR word: 1609 of 1705 (**94.37%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "Councilperson" 1754.550-1758.039. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 94.37% (threshold 85%).

57 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 0 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 5 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-21 2017 lozman-arrest --model medium.en --pdf-url https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/17-21_ljgm.pdf --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:27:50.879 | 1670.879 | under speech | 0.00 | 0.00 | - | - | if I may say, I mean, Ms. Karlan was having some difficulty with hypotheticals. But you might have some difficulty with the facts of your case. So if I could -- |
| 2 | 0:28:27.039 | 1707.039 | small | 0.74 | 0.00 | 6.6 | 10.2 | I'm sure that there's one in every town. And just the nature of our lives and the nature of our criminal statute books, there's a lot to be arrested for. |

## Petitioner's opening, first 3 minutes

Everything said from 0:23:44.899 to 0:26:44.899, official wording, with each turn's start time. Interruptions from the bench are included.

[0:23:44.899] MS. KARLAN: to have probable cause for the -- for the offense of arrest in order to defeat a Fourth Amendment claim. Any probable --

[0:23:52.119] JUSTICE GORSUCH: That's true in the Fourth Amendment context, but would it necessarily hold in the First Amendment context, I believe is the Chief Justice's question?

[0:23:58.679] MS. KARLAN: Sure. And you could reverse in this case on the grounds that you're going to apply Hartman as written and not add a kind of Devenpeck chaser to it, if you will. And that would be a --

[0:24:09.079] JUSTICE SOTOMAYOR: Do you recommend that?

[0:24:10.779] MS. KARLAN: I would -- I would love that.

[0:24:12.459] JUSTICE SOTOMAYOR: In your case.

[0:24:13.599] MS. KARLAN: In our case, we would love that.

[0:24:14.839] JUSTICE SOTOMAYOR: But is it a good rule? Meaning --

[0:24:16.279] MS. KARLAN: We think the best rule is the rule we advocated for, which is that probable cause is relevant evidence but not always dispositive. But, certainly, in our case, if you applied Hartman as written, you would say, well, in Hartman, it was the offenses of prosecution; if you show no probable cause on those, they can't come back and say: Oh, well, there was mail fraud as well. I mean, it's starting to sound --

[0:24:36.179] JUSTICE SOTOMAYOR: If we do away with Devenpeck, though, as -- if I remember here, the -- the sergeant, I think, or whomever initially looked at the case said there is grounds for probable cause, but we're not going to get a conviction, so that's why we're not going to proceed. Now the judge said there's no probable cause on the facts as they existed, but you can well imagine that officers filled with animus could scour the books at the booking station and they could look for something that might fit the day as well but still not have been something they would have otherwise arrested for.

[0:25:23.859] MS. KARLAN: Sure, which is why we think the best rule is that probable cause is relevant but not dispositive. If I may reserve the remainder of my time.

[0:25:31.899] CHIEF JUSTICE ROBERTS: Thank you, counsel. Mr. Dvoretzky.

[0:25:42.799] MR. DVORETZKY: Mr. Chief Justice, and -- and may it please the Court: During Ms. Karlan's argument, I wrote -- wrote down four potential backstops to address the hypothetical -- the hypothetical that Justice Kennedy raised and that Justice Breyer echoed about a police officer dealing with a riot in a bar. I'd like to explain why none of the four that I wrote down are sufficient and why the long-standing common law rule and the rule in Hartman ought to be the one that applies here. The four that I wrote down were pleading standards, qualified immunity, Mt. Healthy, and a distinction between felonies or major crimes and other crimes. First, with respect to the pleading standards, it's critical to understand that police officers must concededly take account of speech when deciding whether to arrest in many situations. The bar example is one of those. And police officers need to have an objective -- an objective basis on which their conduct will be judged. It -- it is virtually impossible for police officers themselves

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 18, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/17-21
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/17-21/17-21_20180618-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:05:02.759 (302.759 s)
- Words: 760, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 721 of Whisper's 760 words (94.9%; Oyez has 755).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.680 | 17 |
| JUSTICE KENNEDY | 0:00:07.820 | 0:05:01.660 | 738 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kennedy, has the opinion of the Court in Case 17-21, Lowesman v. City of Riviera Beach?

[0:00:07.820] JUSTICE KENNEDY: this case involves the intersection of two sets of general principles, principles that define when arrests are lawful and principles that prohibit the government from retaliating against a person for having exercised the right to free speech. Petitioner Fane Lowesman became a resident of the City of Riviera Beach, Florida, in 2006. And from the start, Lowesman was an outspoken critic of city officials and policies. He often expressed these views during City Council meetings. He then, he often expressed those views during City Council meetings, and he also filed a lawsuit alleging that the City Council had violated State open meeting laws. In June of 2006, the City Council held a closed-door session in part to discuss Lowesman's open-meeting lawsuit. According to Lowesman, the transcript of that meeting shows the City Council members devised a plan to intimidate him based on his prior speech and for the lawsuit that he filed. Five months later, the City Council held a public meeting. Lowesman stepped up to the podium during the public comment portion of the meeting. He began to discuss the recent arrests of an official from another jurisdiction. A Council member interrupted Lowesman and directed him to stop making those remarks. When Lowesman refused, the Council member told the police officer in attendance to carry him out of the room. The officer handcuffed Lowesman and escorted him from the meeting. Lowesman later filed this lawsuit against the City under 42 USC 1983. He alleged a number of incidents that, under his theory, showed the City's purpose to harass him in different ways, including the arrest at the City Council meeting. Lowesman claimed that the arrest was to retaliate against him for his protected speech. The jury returned a verdict for the City on all of the claims. Now, this case involves only Lowesman's retaliatory arrest claim. On appeal, the Court of Appeals for the Eleventh Circuit determined that the jury necessarily found that the arrest was supported by probable cause, and it held that the presence of probable cause defeated Lowesman's First Amendment retaliatory arrest claim. The existence of probable cause to arrest on the part of the arresting officer has been conceded by Lowesman in this case. And so the issue the parties deemed central to the case is whether the probable cause for an arrest bars a suit alleging that the arrest was to retaliate for speech protected by the First Amendment. That issue has divided the courts of appeals. But its resolution must await a different case. That is because Lowesman's claim is far afield from the typical retaliatory

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:07.820-0:00:07.960: "Kennedy,"
- 0:05:01.660-0:05:02.060: "Thank you."

Where Whisper's words differed from Oyez's and the re-run agreed with Oyez, the re-run's words and times replace the first pass:

- 0:01:41.980: "U .S .C. Section" became "USC"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:03.140 | 17 -21, Lowesman | 17-21, Lozman |
| 0:00:23.800 | Lowesman | Lozman |
| 0:00:30.920 | Lowesman | Lozman |
| 0:00:38.340 | He then, | (nothing) |
| 0:00:55.460 | Lowesman's | Lozman's |
| 0:00:58.680 | Lowesman, | Lozman, |
| 0:01:13.120 | Lowesman | Lozman |
| 0:01:19.420 | arrests | arrest |
| 0:01:24.520 | Lowesman | Lozman |
| 0:01:25.200 | directed | direct |
| 0:01:28.040 | Lowesman | Lozman |
| 0:01:36.120 | Lowesman | Lozman |
| 0:01:39.020 | Lowesman | Lozman |
| 0:01:52.300 | at | of |
| 0:01:54.600 | Lowesman | Lozman |
| 0:02:06.120 | Lowesman's | Lozman's |
| 0:02:21.220 | Lowesman's | Lozman's |
| 0:02:29.340 | (nothing) | arrest and |
| 0:02:32.780 | Lowesman | Lozman |
| 0:02:56.220 | Lowesman's | Lozman's |
| 0:03:02.760 | Lowesman | Lozman |
| 0:03:06.720 | Lowesman | Lozman |
| 0:03:16.060 | Lowesman | Lozman |
| 0:03:33.600 | Lowesman | Lozman |
| 0:03:39.920 | Lowesman's | Lozman's |
| 0:03:57.720 | Lowesman | Lozman |
| 0:04:02.460 | of | (nothing) |
| 0:04:21.520 | Lowesman | Lozman |
| 0:04:29.360 | Lowesman's | Lozman's |
| 0:04:36.340 | Lowesman | Lozman |
| 0:04:40.700 | Lowesman's | Lozman's |
