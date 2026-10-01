# yates-fish: Supreme Court No. 13-7451

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2014/13-7451
- Audio: https://www.supremecourt.gov/media/audio/mp3files/13-7451.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2014/13-7451_k1fk.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 44 min on 4 CPU cores
- Audio length: 0:58:46.792 (3526.792 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.2 MB
- Official words: 9763 (plus 15 `(Laughter.)` markers), in 262 speaker turns
- ASR words: 9773
- Official words matched to an ASR word: 9276 of 9763 (**95.01%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "the" 725.450-728.870. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 95.01% (threshold 85%).

260 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
cluster if it ends at the word's end, and is left alone otherwise. This trimmed 11 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 13-7451 2014 yates-fish --model medium.en --opinion

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.300 to 0:03:09.300, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.300] MR. BADALAMENTI: Mr. Chief Justice, and may it please the Court: The natural, sensible and contextual reading of Section 1519 is that the phrase "record document or tangible object" is confined to records, documents and devices designed to preserve information, the very matters involved in the Enron debacle. Given the expansive Federal nexus of this statute, which is the intent to influence the proper administration of any matter within the jurisdiction of the United States, it is implausible that Congress would have passed sub silentio, an all-encompassing obstruction statute buried within the altering documents provision of the Sarbanes-Oxley Act. A strong textual indicator that Section 1519 is confined to record-related offenses is the inclusion of the unique term "makes false entry in," which Congress only uses in record-related statutes. The canons of ejusdem generis and noscitur a sociis confirm that tangible object is related to the common thread between record and document which are information devices -- information mediums.

[0:01:17.860] JUSTICE GINSBURG: Why should -- why should the expression "tangible object," which stands alone, it's not falsifying documents, why should the word "object" in 1519 be treated differently than the word "other object" in 1512 -- 1512(c)?

[0:01:39.600] MR. BADALAMENTI: Justice Ginsburg, in Section 1519 -- it was passed at the same time as 1512(c) as part of the Sarbanes-Oxley Act. And as this Court held in Russello, when Congress includes different terms in different statutes passed in the same act, it is intended to mean something different.

[0:01:57.160] JUSTICE GINSBURG: So you think there's a difference between "tangible object" and "other object"?

[0:02:01.620] MR. BADALAMENTI: Yes, there is. The first reason is that the inclusion of "makes false entry in" indicates that the phrase "record document and tangible objects" refers to recordkeeping. Another difference is that -- a common sense standpoint -- is that records can only be maintained on tangible mediums. And it's a distinguishing factor between "record document" and "other objects" in 1512(c). It's also limited --

[0:02:28.310] JUSTICE SOTOMAYOR: But how does the Internet -- you could falsify Internet entries, or things that are in the cloud, those are intangible items.

[0:02:38.120] MR. BADALAMENTI: No, those are tangible items, Your Honor, because they are stored on a hard drive somewhere. The cloud is not existing above. It's merely being housed somewhere else that's accessed through the Internet on a tangible device that's designed to preserve that very type of information.

[0:02:56.320] JUSTICE KENNEDY: Suppose a typewriter were used to prepare an incriminating document. The document and the typewriter were destroyed, would that be covered?

[0:03:05.440] MR. BADALAMENTI: The typewriter would not be. The piece of paper that the typewriter is

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - February 25, 2015.

- Oyez page: https://www.oyez.org/cases/2014/13-7451
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2014/13-7451/13-7451_20150225-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.7 MB)
- Length: 0:07:09.296 (429.296 s)
- Words: 769, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause between words within 1.5 s of it. Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 729 of Whisper's 769 words (94.8%; Oyez has 750).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:07.200 | 14 |
| JUSTICE GINSBURG | 0:00:07.980 | 0:07:08.400 | 748 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Ginsburg has our opinion this morning in Case 13-7451, Yates v. United States.

[0:00:07.980] JUSTICE GINSBURG: In the summer of 2007, a Federal agent on patrol in the Gulf of Mexico boarded the Miss Katie, a commercial fishing boat, to check on the vessel's compliance with fishing rules. At the time, Federal conservation regulations prohibited catching Red Grouper less than 20 inches long. A violation of those regulations is a civil offense, not a criminal infraction, punishable only by fine or fishing license suspension. The inspecting officer counted 72 undersized Red Grouper on board the Miss Katie. He placed those fish in crates to separate them from the rest of the ship's catch and told Petitioner Yates, the ship's captain, to leave the fish in the crates until the vessel returned to port. At port, the officer reexamined the fish in the crates. This time, the fish measured slightly lower than they had at sea. A crew member, questioned by the suspicious officer, admitted that at Yates' direction he had thrown the fish in the crates overboard and replaced them with other fish from the catch. For these actions, Yates was charged with violating 18 U .S .C. Section 1519, a felony punishable by up to 20 years in prison. Did 1519 concern the fish disposal in which Yates engaged? One clue to the answer, Congress passed 1519 in 2002 as part of the Sawbains-Oxley Act. That Act was sparked by the Enron Corporation fiasco, a fraud involving massive shredding of incriminating documents. Section 1519 prohibits altering destroying, mutilating, concealing, covering up, falsifying, or making a false entry in any record, document, or tangible object with intent to obstruct the investigation or proper administration of any matter within the jurisdiction of any Federal department or agency. Yates had violated this provision the government charged by destroying or concealing tangible objects, namely 72 small fish thrown overboard at Yates' command. At trial, Yates moved for a

### Words Whisper invented

Runs of 3 or more words where Whisper and Oyez's transcript disagree were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:02:21.220-0:02:21.860: "disability rights in the United States. Yates was charged with"

Where Whisper's words differed from Oyez's and the re-run agreed with Oyez, the re-run's words and times replace the first pass:

- 0:04:59.580: "offense that was" became "events"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:08.780 | the summer | December |
| 0:00:11.160 | a | the |
| 0:01:15.500 | lower | longer |
| 0:01:39.220 | Section | (nothing) |
| 0:01:47.320 | Did | The |
| 0:01:48.640 | concern | concerned |
| 0:02:04.280 | Sawbains -Oxley | Sarbanes-Oxley |
| 0:02:18.700 | Section | (nothing) |
| 0:02:35.340 | (nothing) | a |
| 0:03:07.700 | Sawbains -Oxley | Sarbanes-Oxley |
| 0:03:24.960 | He | who |
| 0:03:30.380 | 3 | three |
| 0:03:37.500 | Section | (nothing) |
| 0:04:09.300 | words | word |
| 0:04:10.260 | mean | means |
| 0:04:11.900 | contexts. | context. |
| 0:04:14.860 | Sawbains -Oxley | Sarbanes-Oxley |
| 0:04:44.360 | Section | (nothing) |
| 0:05:11.680 | Sawbains -Oxley, | Sarbanes-Oxley, |
| 0:05:14.560 | Section | (nothing) |
| 0:05:21.580 | Section | (nothing) |
| 0:05:29.400 | Section | (nothing) |
| 0:06:00.760 | reaching any physical object under the sun, | -- |
| 0:06:19.900 | Section | (nothing) |
| 0:06:32.180 | comprehended. | comprehending. |
| 0:06:40.680 | seed | sea |
| 0:06:57.620 | grouper | groupers |
| 0:07:07.980 | join. | joined. |
