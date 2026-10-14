# gant-car: Supreme Court No. 07-542

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2008/07-542/20081007a_07-542.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2008/07-542.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 42 min on 4 CPU cores
- Audio length: 0:49:23.984 (2963.984 s)
- `audio/argument.mp3`: mono, 64 kbps, 23.7 MB
- Official words: 8790 (plus 7 `(Laughter.)` markers), in 225 speaker turns
- ASR words: 8841
- Official words matched to an ASR word: 8147 of 8790 (**92.68%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 2 words longer than 3 s outside laugh positions.
  Offending words: "Buie," 2319.240-2326.740, "where" 2453.800-2457.160. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 92.68% (threshold 85%).

320 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 14 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 07-542 2008 gant-car --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2008/07-542.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2008/07-542/20081007a_07-542.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00:11.920 | 11.920 | big | 6.72 | 6.50 | 23.6 | 33.4 | We'll hear argument next in Kennedy v. Plan Administrator for DuPont Savings and Investment Plan. Mr. Furlow. I'm sorry. We won't. |
| 2 | 0:00:29.280 | 29.280 | big | 1.40 | 1.25 | 27.6 | 35.6 | Investment Plan. Mr. Furlow. I'm sorry. We won't. It's still early in the term. Case 07-542, Arizona v. Gant. Mr. Maziarz. Do you have any views on the other case? |
| 3 | 0:08:53.240 | 533.240 | big | 2.34 | 2.20 | 27.3 | 34.2 | car? Yes. Well, Your Honor, it's my understanding -- I'm not an expert on this, but it's my understanding from reading some of these cases - I'd really like to meet him. |
| 4 | 0:09:07.740 | 547.740 | under speech | 0.00 | 0.00 | - | - | I wouldn't. I'll bet you that in most of those cases the -- the felon got out the other -- other door of the car while the policeman was searching the vehicle. |
| 5 | 0:24:24.480 | 1464.480 | medium | 1.38 | 0.60 | 23.1 | 32.5 | protecting - He says, "Let me lock my car." You know, "I park it on the street all the time. It's a lousy car any way. Nobody wants to steal it." |
| 6 | 0:27:55.040 | 1675.040 | small | 0.96 | 0.00 | 5.8 | 11.8 | you arrest somebody, have them stand right near the car while you search it. Okay? Make sure that he's near enough that, you know, he's a threat to your safety. |
| 7 | 0:31:01.727 | 1861.727 | under speech | 0.00 | 0.00 | - | - | search of the person? I mean, if the police arrest Mother Teresa, they are still entitled to frisk her, right, even though there's little likelihood that she has a Gatt? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:33.020 to 0:03:33.020, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:33.020] MR. MAZIARZ: Mr. Chief Justice, and may it please the Court: More than 27 years ago in Belton this Court applied its prior decisions in Chimel and Robinson to the arrest of a recent occupant of an automobile. The Court sought to forge a workable straightforward rule that could be easily applied and predictably enforced by law enforcement officers in the field in this dangerous and dynamic situation. After careful consideration, this Court held that the passenger compartment of the vehicle was deemed to be under the immediate control of the arrestee. The Court also made clear that the search need only be a contemporaneous incident of the arrest. There are three reasons, all well-established by this Court's case law, why officers, law enforcement officers, need not demonstrate a threat to their safety or need to preserve evidence prior to searching an automobile incident to arrest, even if all of the recent occupants of the vehicle have been arrested and secured. First, neither justification need exist in a particular case. This Court has made clear in Robinson that a search incident to arrest requires no additional justification. It's the fact of arrest that justifies the search. Second, the search need only be a contemporaneous incident of the arrest or substantially contemporaneous with the arrest. Obviously a search can be contemporaneous even if the arrestee has been secured.

[0:02:07.380] JUSTICE GINSBURG: But not if it occurred in the station house, right, if the -- if the arrestee had been taken into the station house?

[0:02:17.160] MR. MAZIARZ: Correct. That would be remote in time and location, Your Honor.

[0:02:19.260] JUSTICE KENNEDY: Or location.

[0:02:20.660] MR. MAZIARZ: Time and location, Your Honor.

[0:02:21.740] JUSTICE GINSBURG: Well, why isn't this situation more like the station house than it is like - the Belton situation is the police apprehend the -- a driver. They are concerned about weapons, about being assaulted. But here we have someone who is locked up inside a police car, handcuffed, can't go anywhere. That sounds to me more like the station house than it does the urgent situation where the police have a legitimate concern for their own safety.

[0:03:04.400] MR. MAZIARZ: The arrestee is still at the same location at the scene of the arrest. It's not remote in place or time because it -- it -- the arrest and the search occur in a short period of time at the scene of the -- of the arrest. And while he -- the arrestee is secured to one degree or another, in Belton this Court wanted a workable, straightforward rule that officers could apply across the board and not have to look at particular facts and circumstances. So -

[0:03:29.740] JUSTICE KENNEDY: And this is important, but you had three -- three points. One was the

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - April 21, 2009.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2008/07-542
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2008/07-542/20090421o_07-542.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.6 MB)
- Length: 0:02:14.530 (134.530 s)
- Words: 329, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 316 of Whisper's 329 words (96.0%; Oyez has 326).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:09.820 | 18 |
| JUSTICE STEVENS | 0:00:09.820 | 0:02:13.360 | 310 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Stevens has our opinion this morning in Case 07-542, Arizona v. Gant. This case comes to us

[0:00:09.820] JUSTICE STEVENS: from the Supreme Court of Arizona. It raises an important Fourth Amendment issue. Acting on an anonymous tip that a residence in Tucson was being used to sell drugs, two police officers knocked on the front door and asked to speak to the owner. Respondent Rodney Gant answered the door and, after identifying himself, stated that he expected the owner to return later. The officers left the residence and conducted a records check which revealed that Gant's driver's license had been suspended, and there was an outstanding warrant for his arrest for driving on a suspended license. The officers returned to the house that evening and recognized Gant when his car entered the driveway. They arrested him, handcuffed him, and locked him in the back seat of a squad car. Two officers then searched his car and discovered a bag of cocaine in the pocket of a jacket on the back seat. After Gant was charged with two drug offenses, he moved to suppress the evidence seized from his car on the ground that the warrantless search was unreasonable because he posed no threat to the officers after he was locked in the back of the patrol car and because he was arrested for a traffic offense for which no evidence could be found in his vehicle. When asked at the suppression hearing why the search was conducted, Officer Griffith responded, Because the law says we can do it. The Arizona Supreme Court held that the search violated the Fourth Amendment. For reasons stated at length in an opinion filed with the clerk, we agree with their conclusion and we affirm their judgment. Justice Scalia has filed a concurring opinion. Justice Alito has filed a dissenting opinion joined in full by the Chief Justice and Justice Kennedy and in part by Justice Breyer. Justice Breyer has also filed a dissent.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:19.060 | a residence | residents |
| 0:00:45.480 | an | (nothing) |
| 0:00:48.420 | (nothing) | with the -- |
| 0:00:53.320 | the | (nothing) |
| 0:01:10.500 | a | the |
| 0:01:14.460 | charged | changed |
