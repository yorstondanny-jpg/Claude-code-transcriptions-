# brigham-party: Supreme Court No. 05-502

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/05-502/20060424a_05-502.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2005/05-502.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 37 min on 4 CPU cores
- Audio length: 0:55:14.547 (3314.547 s)
- `audio/argument.mp3`: mono, 64 kbps, 26.5 MB
- Official words: 9408 (plus 7 `(Laughter.)` markers), in 275 speaker turns
- ASR words: 9199
- Official words matched to an ASR word: 8830 of 9408 (**93.86%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "counterfeit" 608.000-611.420. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 93.86% (threshold 85%).

348 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 24 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 05-502 2005 brigham-party --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2005/05-502.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/05-502/20060424a_05-502.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-47.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:04:28.160 | 268.160 | under speech | 0.00 | 0.00 | - | - | kill you in 2 minutes. Well, that -- that's -- Do you really want the policeman to say I got 2 minutes, you know, dial in and get a warrant? That's ridiculous. |
| 2 | 0:20:47.640 | 1247.640 | small | 0.44 | 0.00 | 8.4 | 10.1 | presented, unaware of the fact that that is not -- Oh, no. He knows. He knows. He heard this is what they do at the family reunion. They always reenact this. |
| 3 | 0:37:40.800 | 2260.800 | small | 0.68 | 0.00 | 4.0 | 8.3 | more likely to hear him if he opens the screen door and yells, police? Why doesn't that meet the requirement? I -- this -- why is the trial court obsessed with knocking? |
| 4 | 0:43:35.920 | 2615.920 | small | 2.40 | 0.05 | 13.1 | 28.6 | police -- And -- -- which he thought would be more effective than knocking on -- on the -- you know, the -- the edge of a screen door, which doesn't make a very good knock. |
| 5 | 0:51:56.440 | 3116.440 | big | 5.90 | 5.70 | 23.1 | 32.2 | But the defendants in this case were the adults inside the home. Oh, they charge that the adults were intoxicated. Yes. Well, that's a serious crime in Utah I guess. |
| 6 | 0:52:05.180 | 3125.180 | big | 3.74 | 3.15 | 28.8 | 36.1 | case were the adults inside the home. Oh, they charge that the adults were intoxicated. Yes. Well, that's a serious crime in Utah I guess. We anticipated that comment actually. |
| 7 | 0:52:09.600 | 3129.600 | under speech | 0.00 | 0.00 | - | - | the home. Oh, they charge that the adults were intoxicated. Yes. Well, that's a serious crime in Utah I guess. We anticipated that comment actually. And -- And what's your response? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.640 to 0:03:06.640, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.640] MR. GRAY: Mr. Chief Justice, and may it please the Court: In cases involving safety exigencies, an officer's actions should be judged against a single objective standard of reasonableness, that is, whether the facts and circumstances known to the officers at the time of entry would warrant a reasonable person in believing that immediate intervention is needed to preserve the peace and protect others from harm. When officers have reason to believe that violence is imminent or ongoing, they meet that standard. In this case, the Brigham City officers responded to a complaint at 3:00 a.m. and, upon arriving, witnessed a violent and tumultuous struggle between four adults and a teenager. The officers -- when the juvenile threw a punch is when the officers acted and thereby prevented injury. This is exactly what we would expect officers to do.

[0:01:14.260] JUSTICE SCALIA: What were they doing in the yard anyway? This sort of occurred to me. They couldn't have seen that until they went into the fenced backyard violating the curtilage of the property. How -- was that justified?

[0:01:28.840] MR. GRAY: Yes, it was justified. At that time what they heard from the curb side and then from the front was the same kind of violence going on. They heard that from -- from the time they arrived all the way. They -- they heard the thumping, the shouting, someone saying, get off me, stop, stop. And so what these officers were doing, in the course of that, is investigating that -- that, and it led them to the backyard. Now --

[0:02:00.320] JUSTICE SCALIA: Is any less required to -- to go into the curtilage than is required to go into the house?

[0:02:03.580] MR. GRAY: No.

[0:02:04.300] JUSTICE SCALIA: No. It's the same test?

[0:02:05.880] MR. GRAY: Yes. And again, that was --

[0:02:08.620] JUSTICE SCALIA: So you say that even if he didn't see him throw the punch and -- and draw blood, they could have gone in just because they heard somebody say, stop, stop, get off me?

[0:02:18.260] MR. GRAY: It's our position that they could have, though that's a much closer case. In this case, the officers acted in a very guarded manner. I mean, they -- they proceeded and they investigated step by step and, in fact, did not enter until a punch was thrown and there was --

[0:02:36.120] JUSTICE SOUTER: So what -- what you're saying is they've got to have a reasonable ground to take the first step. That may not be a reasonable ground to have taken the second step right then and there, but it's the same reasonableness standard.

[0:02:46.240] MR. GRAY: Yes, it is.

[0:02:47.020] JUSTICE SOUTER: That's -- that's --

[0:02:47.380] MR. GRAY: Yes.

[0:02:48.020] JUSTICE GINSBURG: One thing that was left out of the succession of acts -- Utah provides for telephone warrants, and there was no attempt to do that. Once they checked to -- to determine that

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 22, 2006.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2005/05-502
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/05-502/20060522o_05-502.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.1 MB)
- Length: 0:04:10.802 (250.802 s)
- Words: 619, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (1 turn), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 606 of Whisper's 619 words (97.9%; Oyez has 614).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:04:10.020 | 614 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion in 05-502, Brigham City v. Stewart. At about 3 o 'clock in the morning, four Brigham City, Utah, police officers responded to a call regarding a loud party at a residence. When they arrived at the house, they heard shouting from inside coming from the back of the house. They proceeded down the driveway to investigate. From the backyard, they could see into the home's kitchen through a screen door and windows. There was an altercation taking place. Four adults were trying to restrain a juvenile. The juvenile broke free and punched one of the adults in the face. The victim went to spit blood into a sink, while the other adults continued trying to subdue the juvenile. One of the officers opened the screen door and yelled in, But the ruckus from the fight was too loud. Nobody heard him. So he stepped into the kitchen and again cried out. As people gradually became aware that the police were on the scene, the altercation subsided. The officers then arrested several of the adults for disorderly conduct, intoxication, and contributing to the delinquency of a minor. The trial court excluded all evidence obtained after the officers entered the home on the ground that the officers' entry violated the Fourth Amendment. On appeal, the Supreme Court of Utah also concluded that the officers' entry was improper. The court said that the injury caused by the juvenile's punch was not serious enough to allow the officers to enter. This is because, the court said, it could not have led a reasonable officer to believe that an unconscious, semi-conscious, or missing person feared injured or dead was in the home. We granted review. The Fourth Amendment generally prohibits officers from entering a private home without a warrant, but there are certain exceptions. For example, officers may enter without a warrant to fight a fire, or when they are in pursuit of a fleeing felon. If the situation confronting officers is serious enough to make immediate entry reasonable, the Fourth Amendment will allow it. One such situation is the need to protect life or avoid imminent serious injury. The defendants in this case don't dispute this, but make two arguments why the officers still could not enter. First, they claim that the officers here were more interested in making arrests than in quelling violence. They want us to consider the officers' subjective motivation for entering the home. Our cases reject this approach. An action is reasonable under the Fourth Amendment as long as the circumstances viewed objectively justify the action. The

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:04.500 | v. Stewart. | versus Stuart. |
| 0:00:52.700 | (nothing) | ‘Police’, |
| 0:02:36.860 | claim | claimed |
| 0:03:28.100 | A | (nothing) |
