# collins-motorcycle: Supreme Court No. 16-1027

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/16-1027
- Audio: https://www.supremecourt.gov/media/audio/mp3files/16-1027.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/16-1027_p4k8.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 38 min on 4 CPU cores
- Audio length: 0:55:15.288 (3315.288 s)
- `audio/argument.mp3`: mono, 64 kbps, 26.5 MB
- Official words: 9783 (plus 5 `(Laughter.)` markers), in 276 speaker turns
- ASR words: 9412
- Official words matched to an ASR word: 9187 of 9783 (**93.91%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.91% (threshold 85%).

396 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 9 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 21 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 16-1027 2017 collins-motorcycle --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.7 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:13:35.440 | 815.440 | medium | 3.16 | 2.90 | 19.2 | 28.0 | the defendant and the homeowner. But suppose there weren't that close relationship. Suppose it was a brand new girlfriend and he never stayed overnight, he was hopeful, but he hadn't. |
| 2 | 0:19:50.900 | 1190.900 | under speech | 0.20 | 0.05 | 17.7 | 17.7 | access. And I think it would be -- No, I know that, but I'm saying if he'd had access to it. If they'd said please come to my curtilage. All right? |
| 3 | 0:30:55.400 | 1855.400 | under speech | 0.00 | 0.00 | - | - | of residential purposes. They might have storage out there, an extra refrigerator. Somebody might be living out there, if the teenager gets too rambunctious, put them out in the garage. |
| 4 | 0:32:07.440 | 1927.440 | small | 1.22 | 0.25 | 12.1 | 18.7 | hypothetical, I don't see any. Okay. So, fine. Okay. Now, the other Hornbook principle is it's not The Thinker, it's a wisp, a wispy bit of very suspicious drug smoke. |
| 5 | 0:45:35.020 | 2735.020 | under speech | 0.18 | 0.00 | - | - | not, you know, Jay Leno's house, right, where he's got dozens of rare cars or -- or the Porsche in Ferris Bueller. I mean, you -- you're saying that you -- you don't -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.880 to 0:03:06.880, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.880] MR. FITZGERALD: Thank you, Mr. Chief Justice, and may it please the Court: The warrant requirement for the home and curtilage cannot be overthrown by the automobile exception. Under the Commonwealth's argument, on probable cause alone, an officer may search a vehicle anywhere that he finds it and may go anywhere that he needs to in order to access that vehicle. That rule cannot survive foundational Fourth Amendment principles. Searches of the home and curtilage without a warrant are presumptively unreasonable, as this Court has often recognized. So the rule we ask this Court to adopt is that the automobile exception does not apply to a vehicle found in the curtilage of the home.

[0:00:54.020] JUSTICE GINSBURG: Suppose the -- the police have probable cause to believe that the vehicle is stolen and they even get a warrant to inspect the vehicle. But the vehicle is parked in this port. Do they need -- do they need a warrant to go get the car for which they have a warrant?

[0:01:31.240] MR. FITZGERALD: Well, Your Honor, the -- the warrant would specify the place to be searched for the car. And so, commonly, a warrant would say, for instance, the dwelling and curtilage to look for this motorcycle. So the warrant that authorizes the search of the motorcycle would, by its terms, authorize the intrusion into the curtilage to look for --

[0:01:48.960] JUSTICE ALITO: But what if it didn't? So they have a warrant here, let's say, to search for -- they have probable cause to search this thing covered by a -- a tarp. They have a warrant to search this motorcycle because it's been involved in criminal activity. They want to get the vehicle identification number from it. And they see it. Let's say it's parked two feet from the curb. But arguably -- or it's parked where it is here, maybe in the curtilage, maybe not in the curtilage. The -- that warrant would be insufficient?

[0:02:23.420] MR. FITZGERALD: Well, Your Honor, the Fourth Amendment, by its terms, requires a warrant to specify the place to be searched. So if they've seen the motorcycle in that spot and they get a warrant, the warrant would say this house on Dellmead Avenue, may have included the picture, and it would, by its terms, authorize the access to that.

[0:02:40.940] JUSTICE ALITO: And this is my question about your argument based on the curtilage. We -- we ask whether a search within or outside the curtilage in order to determine whether the Fourth Amendment applies at all. But that's not really the question here because there is probable cause, and there is the motor vehicle exception to the warrant requirement. So the issue is not whether there was a search. Yes, there was a search.

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 29, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/16-1027
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/16-1027/16-1027_20180529-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.4 MB)
- Length: 0:05:46.410 (346.410 s)
- Words: 786, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 759 of Whisper's 786 words (96.6%; Oyez has 778).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.800 | 15 |
| JUSTICE SOTOMAYOR | 0:00:07.980 | 0:05:45.440 | 769 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: In Case No. 16-1027, Collins v. Virginia, Justice Sotomayor has the opinion for the Court.

[0:00:07.980] JUSTICE SOTOMAYOR: Sotomayor This case presents the question whether the automobile exception to the Fourth Amendment permits a police officer, uninvited and without a warrant, to intrude upon the curdleage of a home to search a vehicle parked therein. We hold that it does not. David Rhoads, a police officer in Virginia, was investigating two traffic incidents involving a motorcyclist. After Officer Rhoads learned that the motorcycle likely was stolen and in the possession of petitioner Ryan Collins, he went to Collins' house. From his position on the street, he saw what he appeared to be a motorcycle under a white tarp near the top of the driveway. Acting without a search warrant, Officer Rhoads walked onto the property and up to the motorcycle. He removed the tarp to reveal the license plate and vehicle identification numbers and ran a search of those numbers to confirm that the motorcycle was stolen. He then waited for Collins to return home and arrested him for receiving stolen property. Collins filed a motion to suppress, arguing that Officer Rhoads had trespassed on his curdleage to conduct an investigation in violation of the Fourth Amendment. The trial court denied the motion, and the Court of Appeals of Virginia affirmed, as did the Supreme Court of Virginia, which reasoned that the search was justified pursuant to the automobile exception. This case arises at the intersection of two aspects of our Fourth Amendment jurisprudence. The automobile exception and the protection extended to the curdleage of a house. As to the first, the Court has held that the search of an automobile can be reasonable without a warrant because of the readily mobility of automobiles and the pervasive regulation of vehicles capable of traveling on public highways. In announcing these rationales, the Court emphasized that they apply only to automobiles and not to houses. As to the second, the Court has long made clear that curdleage, the area immediately surrounding and associated with the home, is considered part of the home itself for Fourth Amendment purposes. An intrusion on the curdleage by a law enforcement officer to gather evidence is a search, and such conduct is presumptively unreasonable without a warrant. For reasons we explained in our opinion, the part of the driveway where Collins Motorcycle was searched is curdleage. Virginia contends that Officer Rhodes' intrusion on the curdleage to search the motor of the

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:00.680 | No. 16 -1027, | 16-1027, |
| 0:00:07.980 | Sotomayor | (nothing) |
| 0:00:20.020 | curdleage | curtilage |
| 0:00:27.160 | Rhoads, | Rhodes, |
| 0:00:35.500 | Rhoads | Rhodes |
| 0:00:48.840 | he | (nothing) |
| 0:00:57.120 | Rhoads | Rhodes |
| 0:01:22.180 | Rhoads | Rhodes |
| 0:01:24.380 | curdleage | curtilage |
| 0:01:53.100 | curdleage | curtilage |
| 0:02:23.780 | curdleage, | curtilage, |
| 0:02:35.300 | curdleage | curtilage |
| 0:02:52.600 | curdleage. | curtilage. |
| 0:02:58.280 | curdleage | curtilage |
| 0:02:59.260 | the motor of | (nothing) |
| 0:03:17.720 | curdleage | curtilage |
| 0:03:34.260 | a | (nothing) |
| 0:04:15.320 | interest | interests |
| 0:04:25.040 | interest | interests |
| 0:04:27.300 | curdleage. | curtilage. |
| 0:04:56.220 | curdleage, | cartilage, |
| 0:05:01.340 | curdleage | curtilage |
| 0:05:28.040 | curdleage. | curtilage. |
