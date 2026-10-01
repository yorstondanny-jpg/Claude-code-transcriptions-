# brown-ema-videogames: Supreme Court No. 08-1448

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2010/08-1448
- Audio: https://www.supremecourt.gov/media/audio/mp3files/08-1448.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2010/08-1448.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 45 min on 4 CPU cores
- Audio length: 1:00:36.349 (3636.349 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.1 MB
- Official words: 10588 (plus 13 `(Laughter.)` markers), in 297 speaker turns
- ASR words: 10391
- Official words matched to an ASR word: 9932 of 10588 (**93.80%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.80% (threshold 85%).

343 words are shorter than 20 ms. These are official words the ASR didn't produce,
mostly repeats, false starts and cross-talk ("the -- the --", "I -- I think"), squeezed into the
small gap between the ASR words either side. Their order is right; their exact times are not.

## Files

- `audio/argument.mp3`: the argument audio.
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
cluster if it ends at the word's end, and is left alone otherwise. This trimmed 23 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 08-1448 2010 brown-ema-videogames --model medium.en --opinion

## Petitioner's opening, first 3 minutes

Everything said from 0:00:12.280 to 0:03:12.280, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:12.280] MR. MORAZZINI: Mr. Chief Justice, and may it please the Court: The California law at issue today before this Court differs from the New York law at issue in Ginsberg in only one respect: Where New York was concerned with minors' access to harmful sexual material outside the guidance of a parent, California is no less concerned with a minor's access to the deviant level of violence that is presented in a certain category of video games that can be no less harmful to the development of minors. When this Court in Ginsberg crafted a rule of law that permits States to regulate a minor's access to such material outside the presence of a parent, it did so for two fundamental reasons that are equally applicable this morning in this case. First, this rule permits parents' claim to authority in their own household to direct the upbringing and the development of their children; and, secondly, this rule promotes the States' independent interest in helping parents protect the well-being of children in those instances when parents cannot be present. So this morning, California asks this Court to adopt a rule of law that permits States to restrict minors' ability to purchase deviant, violent video games that the legislature has determined can be harmful to the development and the upbringing --

[0:01:25.520] JUSTICE SCALIA: What's a deviant -- a deviant, violent video game? As opposed to what? A normal violent video game?

[0:01:35.520] MR. MORAZZINI: Yes, Your Honor. Deviant would be departing from established norms.

[0:01:40.300] JUSTICE SCALIA: There are established norms of violence?

[0:01:43.400] MR. MORAZZINI: Well, I think if we look back --

[0:01:44.640] JUSTICE SCALIA: I mean, some of the Grimms' fairy tales are quite grim, to tell you the truth. (Laughter.)

[0:01:49.060] MR. MORAZZINI: Agreed, Your Honor. But the level of violence --

[0:01:52.260] JUSTICE SCALIA: Are they okay? Are you going to ban them, too?

[0:01:54.680] MR. MORAZZINI: Not at all, Your Honor.

[0:01:56.540] JUSTICE GINSBURG: What's the difference? I mean, if you -- if you are supposing a category of violent materials dangerous to children, then how do you cut it off at video games? What about films? What about comic books? Grimms' fairy tales? Why are video games special? Or does your principle extend to all deviant, violent materials in whatever form?

[0:02:31.160] MR. MORAZZINI: No, Your Honor. That's why I believe California incorporated the three prongs of the Miller standard. So it's not just deviant violence. It's not just patently offensive violence. It's violence that meets all three of the terms set forth in --

[0:02:43.440] CHIEF JUSTICE ROBERTS: I think that misses Justice Ginsburg's question, which was: Why just video games? Why not movies, for example, as well?

[0:02:52.280] MR. MORAZZINI: Sure, Your Honor. The California Legislature was presented with substantial evidence that demonstrates that the interactive nature of violent -- of violent video games where the minor or the young adult is the aggressor, is the -- is the individual acting out this -- this obscene level of violence, if you will, is especially harmful to minors.

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 27, 2011.

- Oyez page: https://www.oyez.org/cases/2010/08-1448
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2010/08-1448/20110627o_08-1448.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 2.9 MB)
- Length: 0:11:43.843 (703.843 s)
- Words: 1657, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (1 turn), each
  boundary moved to the longest pause between words within 1.5 s of it. Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 1551 of Whisper's 1657 words (93.6%; Oyez has 1632).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| JUSTICE SCALIA | 0:00:00.000 | 0:11:42.460 | 1647 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] JUSTICE SCALIA: This case is here on writ of certiorari to the United States Court of Appeals for the Ninth Circuit. In 2005, California enacted Assembly Bill 1179, which prohibits the sale or rental of violent video games to minors and requires their packaging to be labeled 18. The Act covers games, quote, in which the range of options available to a player includes killing, maiming, dismembering, or sexually assaulting an image of a human being if those acts are depicted in a manner that a reasonable person considering the game as a whole would find appeals to a deviant or morbid interest of minors, that is patently offensive to prevailing standards in the community as to what is suitable for minors, and that causes the game as a whole to lack serious literary, artistic, political, or scientific value for minors. Violation of the Act is punishable by a civil fine of up to $1,000. Respondents representing the video game and software industries brought a pre-enforcement challenge to the Act alleging that it violates the First Amendment. The district court agreed and permanently enjoined its enforcement. The Court of Appeals for the Ninth Circuit affirmed, and we granted certiorari. California correctly acknowledges that video games qualify as expression protected by the First Amendment. Like books, plays, and movies, video games communicate ideas. The most basic principle of First Amendment law is that government has no power to restrict expression because of its content. There are, of course, exceptions. From 1791 to the present, the First Amendment has permitted restrictions upon the content of speech in a few well-defined and narrowly limited areas, such as obscenity, incitement, and fighting words. Last term, in a case called United States v. Stevens, we held that new categories of unprotected speech may not be added to that list by a legislature that conclude certain speech is too harmful to be tolerated. Without persuasive evidence that a novel restriction on the content of speech is part of a long tradition of proscription, a legislature may not revise the judgment of the American people embodied in the First Amendment that the benefits of constitutional restrictions on the government's power outweigh its costs. That holding controls this case. California's statute mimics the New York statute that we upheld in a case called Ginsburg v. New York. That statute prohibited the sale to minors of sexual material that did not meet our definition of obscenity, but that, quote, appeals to the prurient,

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:02:15.320-0:02:15.380: "could"
- 0:05:36.760-0:05:36.960: "called"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.880 | the | (nothing) |
| 0:01:34.820 | and | in |
| 0:01:54.860 | (nothing) | this -- of |
| 0:02:16.140 | speech is | speeches |
| 0:02:36.340 | outweigh | out way |
| 0:02:38.000 | costs. | cause. |
| 0:02:42.900 | California's | California |
| 0:02:47.940 | Ginsburg v. | Ginsberg versus |
| 0:03:02.040 | interest | interests |
| 0:03:17.700 | could, quote, | Court, |
| 0:03:28.680 | interests | interest |
| 0:03:43.360 | attempts | attempt |
| 0:04:19.160 | (nothing) | The |
| 0:04:27.380 | specially | especially |
| 0:04:31.120 | violence. | violations. |
| 0:04:40.920 | are grim | or Grimm |
| 0:04:43.300 | desserts | deserts |
| 0:04:44.320 | to | the |
| 0:04:45.920 | the | but |
| 0:04:56.900 | doves, | dogs |
| 0:04:58.880 | kill | killed |
| 0:05:07.100 | (nothing) | binds -- |
| 0:05:11.680 | steak, | stake |
| 0:05:27.300 | series | serious |
| 0:06:01.900 | close quote. | His objection -- |
| 0:06:27.380 | these | this |
| 0:07:05.740 | miniscule real -world | minuscule real-world |
| 0:07:27.600 | (nothing) | -- the State's |
| 0:08:21.120 | leave | live |
| 0:08:29.180 | (nothing) | an |
| 0:08:37.300 | (nothing) | the |
| 0:08:53.700 | that | the |
| 0:09:14.860 | contain | contained |
| 0:09:27.200 | (nothing) | -- can readily |
| 0:10:27.960 | add in closing | are enclosing |
