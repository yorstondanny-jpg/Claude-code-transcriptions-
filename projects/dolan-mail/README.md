# dolan-mail: Supreme Court No. 04-848

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/04-848/20051107a_04-848.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2005/04-848.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 29 min on 4 CPU cores
- Audio length: 0:56:53.264 (3413.264 s)
- `audio/argument.mp3`: mono, 64 kbps, 27.3 MB
- Official words: 9712 (plus 11 `(Laughter.)` markers), in 408 speaker turns
- ASR words: 9417
- Official words matched to an ASR word: 8973 of 9712 (**92.39%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
  Not counted: `2680(c)` 527.440-531.000 (3.56 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 92.39% (threshold 85%).

409 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 6 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 35 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 3
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 04-848 2005 dolan-mail --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2005/04-848.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/04-848/20051107a_04-848.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.9 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:09:23.360 | 563.360 | medium | 2.72 | 2.35 | 19.8 | 27.8 | resulting from the accident. It would be precisely the same conduct. Precisely the same under our interpretation of -- That is a good answer. I'm glad you came up with that. |
| 2 | 0:11:37.800 | 697.800 | small | 0.64 | 0.10 | 13.0 | 20.0 | So, if, in fact, they -- the Post Office negligently delays the knowledge that would come to me in the letter, that I have 15 days to claim my billion-dollar inheritance -- |
| 3 | 0:12:03.240 | 723.240 | small | 0.42 | 0.00 | 4.8 | 8.5 | they do is, he puts the mail on the porch, my package, and he rips it open, negligently; and there for everyone to see is the toupee that I ordered. |
| 4 | 0:12:09.460 | 729.460 | big | 4.48 | 3.70 | 24.9 | 36.6 | it open, negligently; and there for everyone to see is the toupee that I ordered. And I sue -- I sue for public humiliation. See? I mean, what about that one? |
| 5 | 0:12:16.020 | 736.020 | small | 0.38 | 0.20 | 31.4 | 35.6 | for everyone to see is the toupee that I ordered. And I sue -- I sue for public humiliation. See? I mean, what about that one? I have that same problem. |
| 6 | 0:26:51.380 | 1611.380 | under speech | 0.26 | 0.00 | 7.2 | 8.6 | letterbomb or, unfortunately, anthrax, or biohazards -- I mean, we ship poisons, we ship medical specimens, we ship live alligators. I mean, every -- you wouldn't believe what goes into the mail. |
| 7 | 0:27:58.860 | 1678.860 | under speech | 0.04 | 0.00 | - | - | driving a postal truck or leaving something on a porch that somebody trips over or walking along the street swinging the live alligator over your head, or whatever you do –- |
| 8 | 0:32:19.240 | 1939.240 | small | 0.52 | 0.10 | 10.9 | 15.3 | in the truck, so my skis, which I have shipped by mail, happen to stick out the side, and, as he walk -- drives along, he just mows down the pedestrians. |
| 9 | 0:53:35.080 | 3215.080 | under speech | 0.00 | 0.00 | - | - | his rebuttal. Do you have any -- I mean, you'll be responsible, if you prevail, for all of us having to go down to the Post Office every time we get -- |
| 10 | 0:53:42.060 | 3222.060 | medium | 0.84 | 0.65 | 23.0 | 26.2 | having to go down to the Post Office every time we get -- -- packages. I mean, it there -- Well, then I'll probably -- -- do you have any response to that policy concern? |
| 11 | 0:53:45.880 | 3225.880 | medium | 3.82 | 1.50 | 16.8 | 24.5 | we get -- -- packages. I mean, it there -- Well, then I'll probably -- -- do you have any response to that policy concern? Then I'll probably be subject to some intentional torts, myself. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.160 to 0:03:07.160, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.160] MR. RADMORE: Mr. Chief Justice, and may it please the Court: The Federal Tort Claims Act's postal-matter exception bars any claim arising out of the failure of the Postal Service to fulfill its duty to deliver mail to its intended destination on time and in good condition, but does not bar any claim arising out of ordinary negligence that happens to occur while the tortfeasor is delivering mail. The Petitioner's construction shields the Government from all claims arising out of loss or damage or delay or destruction of the mail, while allowing claims that do not stem from all -- do not stem from the violation of the unique duty of the Postal Service to make sure that the mail arrives on time and in good condition. It is the construction most faithful with the text and purpose of the Federal Tort Claims Act. The exception bars any claims, whether for personal injury or property damage, that arise while the mail is -- if the mail is lost, misdelivered, damaged, or delayed. The Government argues for a much broader construction that would bar all claims that arise from the handling of mail. The Government's construction depends on a definition of transmission of the mail, viewed in isolation from the rest --

[0:01:38.660] JUSTICE O'CONNOR: Mr. Radmore, what was the purpose of the enactment of the waiver of Federal sovereign immunity here? Was it to allow recovery for auto accidents occurring by postal trucks?

[0:01:55.040] MR. RADMORE: Well, the --

[0:01:56.420] JUSTICE O'CONNOR: Was that basically the purpose?

[0:01:58.380] MR. RADMORE: Justice O'Connor, this Court's decision in Kosak tells us that one of the main purposes in enacting the Federal Tort Claims Act was to allow private persons to be able to make claims against the Postal Service from motor vehicle --

[0:02:13.580] JUSTICE O'CONNOR: Arising --

[0:02:14.040] MR. RADMORE: -- accidents.

[0:02:14.040] JUSTICE O'CONNOR: -- out of auto accidents.

[0:02:15.400] MR. RADMORE: Correct.

[0:02:16.880] JUSTICE O'CONNOR: And do we normally construe waivers of sovereign immunity narrowly?

[0:02:24.000] MR. RADMORE: Well, once you --

[0:02:25.580] JUSTICE O'CONNOR: I thought we did.

[0:02:28.380] MR. RADMORE: But once there's a broad waiver --

[0:02:30.740] JUSTICE O'CONNOR: For auto accidents.

[0:02:32.100] MR. RADMORE: Well --

[0:02:32.120] JUSTICE O'CONNOR: Now, why should we interpret the exception broadly?

[0:02:39.560] MR. RADMORE: Well, the exception -- this Court has told us, in both Smith and Kosak, that it is the -- the lower courts and this Court, when they're viewing an exception to the Federal Tort Claims Act -- that they shouldn't extend the waiver, nor should they view it more narrowly, that they should look at the waiver -- they should look at the exception and make a determination as to what the meaning of the words are, and

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - February 22, 2006.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2005/04-848
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/04-848/20060222o_04-848.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.8 MB)
- Length: 0:03:00.114 (180.114 s)
- Words: 527, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 510 of Whisper's 527 words (96.8%; Oyez has 522).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:07.140 | 15 |
| JUSTICE KENNEDY | 0:00:07.800 | 0:02:59.380 | 512 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kennedy has the opinion in No. 04848, Dolan v. The United States Postal Service.

[0:00:07.800] JUSTICE KENNEDY: As the Chief Justice indicates, this is our opinion in Dolan v. United States Postal Service. Barbara Dolan alleged that the United States Postal Service left mail on her front porch at her residence and that that caused her to slip and fall. She sued the Postal Service for resulting injuries. The district court and the court of appeals ordered her suit dismissed. And now Mrs. Dolan is the Petitioner in this Court, and she asks us to rule that the suit can proceed. The Postal Service is an independent establishment of the government of the United States. That means that it enjoys immunity from suit unless the immunity has been waived. The question here is whether there has been a waiver for suits of this type. The case turns on provisions of the Federal Tort Claims Act. The Act contains a broad waiver of immunity, but the waiver has some exceptions. If one of the exceptions applies, then the immunity from suit has been retained. The exception relevant to this case specifically applies to the Postal Service, and the question we must decide is how far that exception extends. By terms of the exception, immunity is retained, which means suit is barred, proclaims arising out of the loss, miscarriage, or negligent transmission of letters or postal matters. And the key phrase for us here is the meaning of negligent transmission. If considered in isolation, that term could embrace a wide range of negligent acts committed in the course of delivering mail. This could include the creation of slip and fall hazards from leaving mail packets and parcels on the porch of a customer. The government urges us to adopt that interpretation. It notes that each day the Postal Service delivers some 660 million pieces of mail to as many as 142 million different points. It is obviously concerned, then, with the potential for liability from slip and fall suits. We think, though, that we must read negligent transmission in the statute in light of the more narrow phrase, loss or miscarriage of the mail, phrases that would precede it in the same statutory clause. These words refer to destruction of the mail or delivering to the wrong address or delivering it late. And we do not write on a clean slate in this case. In a decision by this Court in a case called Kozak v. United States, the Court held that this provision does not retain immunity for injuries resulting from auto accidents in which employees of the Postal Service were allegedly at fault. Applying that reasoning here, we think the exception does not extend to this case. The exception, as a general rule, does not go beyond negligence, causing mail to be lost or to arrive late or in damaged condition or at the wrong address. In sum, Mrs. Dolan's suit can proceed, and the judgment of the Court of Appeals for the Third Circuit must be reversed. Justice Thomas has filed a dissenting opinion. Justice Alito took no part in the consideration of the decision of the case.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:01:14.860 | terms | turns |
| 0:01:18.860 | proclaims | “for claims |
| 0:01:20.640 | the | a |
| 0:02:09.040 | that would | which |
| 0:02:22.800 | Kozak | Kosak |
| 0:02:52.040 | Third | 3rd |
| 0:02:58.280 | of the | or |
