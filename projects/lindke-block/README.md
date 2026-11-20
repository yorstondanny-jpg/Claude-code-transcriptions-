# lindke-block: Supreme Court No. 22-611

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2023/22-611
- Audio: https://www.supremecourt.gov/media/audio/mp3files/22-611.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2023/22-611_p3lb.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 41 min on 4 CPU cores
- Audio length: 1:17:21.264 (4641.264 s)
- `audio/argument.mp3`: mono, 64 kbps, 37.1 MB
- Official words: 13965 (plus 4 `(Laughter.)` markers), in 287 speaker turns
- ASR words: 13540
- Official words matched to an ASR word: 13295 of 13965 (**95.20%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.20% (threshold 85%).

403 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 7 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 16 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 22-611 2023 lindke-block --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.1 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:08:45.920 | 525.920 | medium | 1.04 | 0.90 | 23.3 | 33.1 | harassing in my hypothetical has to do with cats. No, I understand. The -- the commenter hates -- Sure. -- cats. Sure. And -- And maybe he hates your children too, I don't know. |
| 2 | 0:14:59.320 | 899.320 | small | 0.46 | 0.10 | 18.3 | 24.0 | not think that surely this could not be the official communication channel. So -- Or what, you know -- Yeah. So I -- I think -- It's not like any town I've ever seen. |
| 3 | 0:19:26.100 | 1166.100 | big | 1.46 | 1.30 | 25.6 | 32.8 | disentangle the two things doesn't really reflect the reality of how social media works. So, Your Honor, I have to push back in two respects. First -- About the dogs or -- |
| 4 | 0:58:21.450 | 3501.450 | medium | 0.92 | 0.80 | 30.4 | 34.8 | that it's not a question of a physical asset. And in what sense is this really private property? They're -- it's just the gathering of the protons or whatever they are. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.040 to 0:03:08.040, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.040] MR. KEDEM: Mr. Chief Justice, and may it please the Court: The dialogue between public officials and their constituents is fundamental to our democracy. Much of that conversation now takes place online, with social media platforms serving as the new town square, where public officials provide important information about what they're doing on the public's behalf and soliciting comments in return. While public officials retain First Amendment rights, use of a private social media account does not immunize an official's conduct from First Amendment or constitutional scrutiny. Under our test for state action, a public official who creates a channel for communicating with constituents about in-office conduct and then blocks a user from that channel must abide by the Constitution. This test, which focuses on how the public official is using and purporting to use that account, is consistent with this Court's precedent under which a public official who purports to act in that capacity is a state actor. It also accords with Section 1983 and the original understanding of what it means to act under color of law. The Sixth Circuit's duty and authority test, by contrast, would provide ready means for public officials to evade the Constitution. Here, for instance, it would mean that the city manager would be free to block from his Facebook page any constituent who is a member of a disfavored race, religion, or political group, free from constitutional constraint. Our test avoids that result while still leaving ample room for public officials to communicate in their personal capacities. I welcome the Court's questions.

[0:01:51.460] JUSTICE THOMAS: Would you also win under the doing your -- doing their jobs test?

[0:01:57.480] MR. KEDEM: Yes, we absolutely would, in part because, as has been pointed out, part of the job of any high-ranking executive official -- and the city manager is essentially just under the mayor in terms of being high up in city government -- part of that job is telling people about what you're doing. And what Mr. Freed was doing with his Facebook account, sometimes multiple times a day, was informing the citizens about what he, as city manager, in his role as city manager, was doing for the town and then communicating directly with constituents about that, sometimes answering their questions about the scope of his orders.

[0:02:34.020] JUSTICE THOMAS: But Ms. Karlan made the point that there were only three instances on the website there in the last case that were personal. In this case, just going through the Joint Appendix, there's quite a bit that is personal. So how would you just -- just factually distinguish that or emphasize the fact -- the fact that --

[0:02:56.480] MR. KEDEM: Sure.

[0:02:56.480] JUSTICE THOMAS: -- the personal here does not override the official?

[0:03:00.600] MR. KEDEM: So there were certainly a lot more personal posts, although the ratio of job-related posts to personal posts changed dramatically at

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 15, 2024.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2023/22-611
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2023/22-611/22-611_20240315-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 7.5 MB)
- Length: 0:06:11.208 (371.208 s)
- Words: 879, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 858 of Whisper's 879 words (97.6%; Oyez has 875).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:03.720 | 13 |
| JUSTICE BARRETT | 0:00:06.800 | 0:06:10.100 | 862 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Barrett has the opinion of the court in two cases this morning.

[0:00:06.800] JUSTICE BARRETT: The first case I have is Linke versus Freed. Like millions of Americans, James Freed maintained a Facebook account on which he posted about a wide range of topics, including his dog, his daughter, and his job. Like many people with a Facebook account, Freed occasionally received unwelcome comments on his posts. In response, Freed took a step familiar to Facebook users. He deleted the comments and he blocked those who made them. For most people, that would have been the end of it, but Kevin Linke, one of the unwelcome commenters, sued Freed for violating his right to free speech. As Linke saw it, Freed's Facebook page was a constitutionally protected public forum from which Linke could not be excluded based on his unwelcome views. Because the First Amendment binds only the government, this claim is a non-starter if Freed posted on Facebook as a private citizen. But here's the wrinkle, Freed is not only a private citizen, but also the city manager of Port Huron, Michigan. And while Freed insists that the account is strictly personal, Linke argues that Freed acted in his official capacity when he silenced Linke's speech. If Freed acted in his official capacity, the First Amendment applies. When a government official posts about job-related topics on social media, it can be difficult to tell whether the speech is official or private. That is true in Freed's case because he posted about his work and Linke's comments were critical of Freed's work, particularly as it related to the pandemic. The Courts of Appeals have disagreed about how to analyze this kind of social media activity. The Second and Ninth Circuits focus on the appearance of the posts, treating speech as official if it comes across that way. The Sixth Circuit, by contrast, focuses on whether the official had legal authority to speak on behalf of the state. Our approach is closer to the Sixth Circuit's. We hold that such speech is attributable to the state only if the official first possessed actual authority to speak on the state's behalf and second, purported to exercise that authority when he spoke on social media. The first prong of this test is grounded in the bedrock requirement that the conduct allegedly causing the deprivation of a federal right be fairly attributable to the state. Our precedent makes clear that an act is not attributable to the state unless it is traceable to the state's power or authority.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:08.600 | Linke | Lindke |
| 0:00:41.940 | Linke, | Lindke, |
| 0:00:42.980 | unwelcome | unwelcomed |
| 0:00:48.960 | Linke | Lindke |
| 0:00:55.840 | Linke | Lindke |
| 0:00:58.940 | unwelcome | unwelcomed |
| 0:01:23.600 | Linke | Lindke |
| 0:01:28.580 | Linke's | Lindke’s |
| 0:01:50.400 | Linke's | Lindke’s |
| 0:02:51.560 | precedent | President |
| 0:03:28.980 | announced | announce |
| 0:04:31.580 | an | (nothing) |
| 0:05:33.800 | (nothing) | have |
| 0:05:46.420 | Linke | Lindke |
