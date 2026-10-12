# riley-phone: Supreme Court No. 13-132

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2013/13-132
- Audio: https://www.supremecourt.gov/media/audio/mp3files/13-132.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2013/13-132_bp7c.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 49 min on 4 CPU cores
- Audio length: 1:01:21.776 (3681.776 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.5 MB
- Official words: 11284 (plus 2 `(Laughter.)` markers), in 230 speaker turns
- ASR words: 11130
- Official words matched to an ASR word: 10752 of 11284 (**95.29%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.29% (threshold 85%).

343 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 23 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 13-132 2013 riley-phone --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-42.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:22:29.000 | 1349.000 | under speech | 0.24 | 0.10 | 14.7 | 15.2 | the amount of information looked at is equivalent to what somebody could have carried around in the old days. Can I say something? I'm going to say something first. Okay. |
| 2 | 0:31:01.600 | 1861.600 | small | 1.28 | 0.15 | 9.6 | 14.4 | but, in fact, most people now do carry their lives on cell phones, and that will only grow every single year as, you know, young people take over the world. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:14.440 to 0:03:14.440, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:14.440] MR. FISHER: Mr. Chief Justice, and may it please the Court: This case involves applying the core protection of the Fourth Amendment to a new factual circumstance. It has always been the case that an occasion of an arrest did not give the police officers authority to search through the private papers and the drawers and bureaus and cabinets of somebody's house, and that protection should not evaporate more than 200 years after the founding because we have the technological development of smartphones that have resulted in people carrying that information in their pockets.

[0:00:44.800] JUSTICE KENNEDY: Just -- just to test the principle for why the police can search and seize some -- some objects. Consider a gun. The arrestee has a gun on his person and the police take the gun. Is part of the reason for that seizure to obtain evidence of the crime or is it just for the safety of the officer and the safety of the community?

[0:01:10.580] MR. FISHER: Well, what this Court said in Robinson at Page 235 is the reason supporting the authority for a search incident to arrest are the two Chimel factors, which are gathering evidence to prevent its destruction, and officer's safety. Now --

[0:01:26.420] JUSTICE KENNEDY: What about gathering evidence in order to make the case? For instance, with the gun, could they take fingerprints? The -- the gun is in the police station where the arrestee is being booked. A, could they take fingerprints? B, could they copy the serial number? C, could they see how many shells were left in the chamber? They obviously have to empty it for safety purposes. All for the purpose of building the case, of -- of obtaining evidence?

[0:01:54.080] MR. FISHER: Yes, of course that's done every day. Once the gun is in the police -- the police department's lawful possession, I think Edwards says that they can do all that.

[0:02:01.920] JUSTICE KENNEDY: So -- so if -- if the proposition then, if the principle then is that some objects that are obtained from the arrestee can be examined in order to build the State's case, is that at least a beginning premise that we can accept in your case, although, obviously, there are problems of the extent and intrusiveness of the search that are -- are in your case, but not in the gun hypothetical.

[0:02:30.340] MR. FISHER: Well, Justice Kennedy, the Court has never described that as one of the things. If you want to think about this case the way you thought about the automobile search in Gant, it would be a beginning premise; but I think you're right, that even if that were a beginning premise, it would be only that, a beginning. In Footnote 9 in Edwards, this Court said that any search incident to arrest still has to satisfy the Fourth Amendment's general -- general reasonableness.

[0:02:52.900] JUSTICE KENNEDY: I think you're right that Gant is probably the best statement in support of the principle that I've -- I've suggested, and then you might say, well, that's limited to automobiles --

[0:03:03.720] MR. FISHER: Right.

[0:03:03.840] JUSTICE KENNEDY: -- and then we're back where we started.

[0:03:05.220] MR. FISHER: Right. And there's important things to understand if you want to start thinking about Gant, because both in terms of its history and its modern application, it's dramatically

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 25, 2014.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2013/13-132
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2013/13-132/20140625o_13-132.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 2.3 MB)
- Length: 0:08:56.764 (536.764 s)
- Words: 1462, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1420 of Whisper's 1462 words (97.1%; Oyez has 1452).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:08:55.980 | 1458 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have our opinion this morning in Case 13-132, Riley v. California, and 13-212, United States v. Worry. These are two separate cases, but we decide them in a single opinion. The question presented in both cases is whether police officers may search a cell phone without a warrant when they seize the phone from a person who has just been arrested. In each case, the relevant events began when the defendant was arrested. Riley, for possession of weapons, worried for a suspected drug deal. Incident to each arrest, police officers searched the defendant and seized a cell phone that he had in his possession. They then searched data on the cell phone, including photos and videos in one case and a contacts list in the other. The search of the cell phone gave the police information about other crimes that the defendant may have committed. Ultimately, information on Riley's cell phone led to attempted murder charges. Information on Worry's cell phone led to serious drug and weapons charges. What is important for our purposes is that in neither case did the police obtain a warrant before searching the defendant's cell phone. We hold today that they were required to do so. The Fourth Amendment protects against, quote, unreasonable searches and seizures, end quote. This Court has said that, as a general rule, a search for evidence of a crime requires a warrant in order to be reasonable. There are, however, some exceptions to that general rule, and a search can be reasonable even without a warrant if it falls within one of those exceptions. The exception at issue here is one for searches incident to arrest. When someone is lawfully arrested, the police may search him and the area immediately around him and inspect physical objects found on his person. We have said that such a search serves two important purposes, removing weapons that the arrestee might use against an officer and discovering evidence that the arrestee might conceal or destroy. In a case from 1973 called United States v. Robinson, this Court held that those two interests categorically justify a search of the person being arrested without the need for an assessment of the risks presented in any given case. As a result, the Court permitted a search of Robinson and of a cigarette pack found in his coat pocket, which turned out to contain heroin capsules. We do not disturb Robinson's holding today, but we declined to extend the search incident to arrest exception from a search of a physical item found on the arrestee to a search of the digital data on a cell phone in the arrestee's possession. In the case of the cell phone, the government's interest in an immediate warrantless search is significantly diminished and the individual's privacy interest is

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:07.760 | v. Worry. | versus Wurie. |
| 0:00:31.020 | worried | Wurie |
| 0:00:35.800 | searched | search |
| 0:00:37.480 | a | the |
| 0:00:41.440 | searched | search |
| 0:00:46.580 | a | the |
| 0:01:01.940 | Worry's | Wurie's |
| 0:01:08.860 | neither | either |
| 0:01:19.360 | (nothing) | -- protects |
| 0:01:23.140 | end quote. | (nothing) |
| 0:01:36.720 | a | the |
| 0:02:13.200 | v. | against |
| 0:02:29.740 | a | his |
| 0:02:39.680 | declined | decline |
| 0:03:31.260 | seized | ceased |
| 0:04:33.820 | text, | texts, |
| 0:05:09.660 | percent | (nothing) |
| 0:05:16.800 | a | to |
| 0:05:28.920 | interests. | interest. |
| 0:05:59.300 | a | (nothing) |
| 0:06:16.860 | a | the |
| 0:06:23.800 | peek | peak |
| 0:06:35.100 | interests, | interest, |
| 0:06:59.820 | a | the |
| 0:07:10.400 | a | (nothing) |
| 0:08:34.020 | seized | ceased |
| 0:08:45.720 | v. Worry | versus Wurie |
