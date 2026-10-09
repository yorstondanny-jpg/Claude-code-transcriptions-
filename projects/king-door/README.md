# king-door: Supreme Court No. 09-1272

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2010/09-1272
- Audio: https://www.supremecourt.gov/media/audio/mp3files/09-1272.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2010/09-1272.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 25 min on 4 CPU cores
- Audio length: 0:58:35.246 (3515.246 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.1 MB
- Official words: 9481 (plus 7 `(Laughter.)` markers), in 279 speaker turns
- ASR words: 9205
- Official words matched to an ASR word: 8954 of 9481 (**94.44%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.44% (threshold 85%).

317 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 28 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 09-1272 2010 king-door --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.1 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:07:43.280 | 463.280 | under speech | 0.16 | 0.00 | - | - | Probable cause beyond thinking that the evidence -- Beyond the reasonable belief -- -- is being destroyed? Yes. Correct. Okay. That is correct. It might just be somebody going to the toilet, right? |
| 2 | 0:12:42.040 | 762.040 | small | 1.58 | 0.20 | 11.6 | 23.6 | surrounding circumstances, that exigent circumstances may not have existed. What if -- what if the defendants here had not flushed the evidence down but had answered the door and said "Yes?"? |
| 3 | 0:14:21.440 | 861.440 | under speech | 0.00 | 0.00 | - | - | But -- this may be a bit rudimentary, but can you tell me why isn't the evidence always being destroyed when the marijuana is being smoked? Isn't it being burnt up? |
| 4 | 0:17:48.580 | 1068.580 | medium | 2.74 | 0.95 | 14.5 | 23.2 | I guess that a person is entitled to do that. I don't recall it ever happening to me, but maybe -- maybe I'm a likable fellow and people open the door. |
| 5 | 0:33:08.260 | 1988.260 | small | 0.64 | 0.00 | 4.1 | 7.4 | problem I have is there are a lot of constraints on -- on law enforcement, and the one thing that -- that it has going for it is that criminals are stupid. |
| 6 | 0:39:36.000 | 2376.000 | under speech | 0.00 | 0.00 | - | - | circumstances -- and I would think it's reasonably foreseeable, when you knock on the door very politely and say "The police," that somebody might shout out "Hide the pot"; all right? |
| 7 | 0:57:39.960 | 3459.960 | under speech | 0.00 | 0.00 | - | - | in that case, suppression -- once they have entry, the evidence would be suppressed. But they can't gain entry by deception. They can't knock on the door and say "Pizza"; right? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:10.100 to 0:03:10.100, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:10.100] MR. FARLEY: Mr. Chief Justice, and may it please the Court: The issue before you today, of whether or not police can impermissibly create exigent circumstances, arises from the improper suppression of reasonably seized evidence after a reasonable warrantless entry. The test set forth by the Kentucky Supreme Court is improper for several reasons, the first of which is that this Court has routinely held that the subjective intent of police officers when effecting a warrantless entry is irrelevant.

[0:00:42.980] JUSTICE GINSBURG: Where did the -- where did the Kentucky Supreme Court -- where did the Kentucky Supreme Court say that it was looking to a subjective state of mind on the part of the police?

[0:00:57.980] MR. FARLEY: Well, the Kentucky Supreme Court's first prong of their test -- and I believe it's in our petition appendix on page 26 -- I'm sorry. Their -- their discussion starts on page 44a and carries over to 46a. The first question of their test is whether or not the officers acted in bad faith in an attempt to purposefully evade the warrant requirements.

[0:01:42.487] JUSTICE GINSBURG: That didn't -- that didn't apply in this case?

[0:01:45.500] MR. FARLEY: That is correct. The second prong of the Kentucky Supreme Court's test is whether or not the actions of the Respondent in this case or the occupant of the home would have been foreseeable by the police officers before they knocked and announced their presence. Now, the problem with the foreseeability test --

[0:02:03.840] JUSTICE GINSBURG: But why is -- why is that subjective? Why isn't that -- would it be foreseeable to a reasonable police officer similarly situated?

[0:02:13.900] MR. FARLEY: Well, Justice Ginsburg, it -- it isn't directly a subjective inquiry. However, police officers are trained to expect and foresee illegal activity so that they may carry out the duties of their job in protecting the citizens. So under a foreseeability test, a reasonable officer will always foresee illegal activity in response to his actions, be it walking down the street or knocking on your door. A reasonable officer will always foresee illegal activity, and for that reason, the Kentucky Supreme Court's test is completely unworkable. Several of the other circuits and the lower courts have adopted tests that also attempt to add an extra exception, an unwarranted closure of the exigent circumstances exception that narrows the use of that exception by police

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 16, 2011.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2010/09-1272
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2010/09-1272/20110516o_09-1272.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.7 MB)
- Length: 0:02:34.279 (154.279 s)
- Words: 374, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 359 of Whisper's 374 words (96.0%; Oyez has 368).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:02:33.700 | 369 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Alito has the opinion of the Court this morning in Case 09-1272, Kentucky v. King. He has asked that I announce it for him. This case comes to us on a writ of certiorari to the Supreme Court of Kentucky. In this case, police officers smelled marijuana outside an apartment door, knocked loudly, and announced their presence. As soon as the officers began knocking, they heard noises that, in their view, indicated that the occupants were destroying drug-related evidence. The officers entered the apartment without a warrant to prevent the destruction of evidence. Respondent was convicted of drug-related offenses based on evidence that the officers found inside the apartment. Now, it is well established that the rule of exigent circumstances, which includes the need to prevent destruction of evidence, is an exception to the warrant requirement. We do not decide whether exigent circumstances actually existed in this case. We, like the Kentucky Supreme Court, assume that there was an exigency. The question before us concerns an exception to the exigent circumstances rule that has been developed by lower courts. Lower courts have held that when police create an exigency, the search is unconstitutional even though an exigency existed. This is known as the police-created exigency doctrine. The Kentucky Supreme Court applied the police-created exigency doctrine in this case, overturning Respondent's conviction. Assuming there was an exigency, the Kentucky Supreme Court held that the exigent circumstances rule could not justify the search because the police should have foreseen that their conduct would prompt the occupants to destroy evidence. In short, the Court held that the police had impermissibly created the exigency. For the reasons stated in our opinion, we reject this interpretation of the exigent circumstances rule. The conduct of the police prior to their entry into the apartment was entirely lawful. They banged on the door and announced their presence. They did not violate the Fourth Amendment, nor did they threaten to violate the Fourth Amendment. Under these circumstances, the officer's warrantless entry to prevent the destruction of evidence was reasonable. We therefore reverse the judgment of the Kentucky Supreme Court and remand for further proceedings not inconsistent with this opinion. Justice Ginsburg has filed a dissenting opinion.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:10.980 | a | the |
| 0:01:56.040 | reasons | reason |
