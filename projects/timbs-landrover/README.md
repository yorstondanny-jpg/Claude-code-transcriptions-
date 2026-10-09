# timbs-landrover: Supreme Court No. 17-1091

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/17-1091
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-1091.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-1091_6c36.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 27 min on 4 CPU cores
- Audio length: 0:56:45.336 (3405.336 s)
- `audio/argument.mp3`: mono, 64 kbps, 27.2 MB
- Official words: 9754 (plus 7 `(Laughter.)` markers), in 195 speaker turns
- ASR words: 9349
- Official words matched to an ASR word: 9100 of 9754 (**93.30%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
  Not counted: `34-24-1-4(a),` 3371.620-3375.440 (3.82 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 93.30% (threshold 85%).

389 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
cluster if it ends at the word's end, and is left alone otherwise. When the only sound in the span
is right at its start (or there's none), followed by a second or more of silence, the word is cut
to that sound, at least 0.2 s from its start. This trimmed 18 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-1091 2018 timbs-landrover --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.7 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:15:40.680 | 940.680 | small | 0.42 | 0.00 | 5.7 | 9.3 | punitive in nature, then the defense can be raised. And that makes sense. What is the situation with jail, prison? I have a vague recollection -- often such recollections are incorrect -- |
| 2 | 0:18:16.200 | 1096.200 | medium | 2.64 | 1.55 | 18.4 | 27.2 | offense, so it was -- Yeah, he had a history. -- it was a punishment for recidivist. Absolutely, Your Honor, and thank you for that. Yeah. He also robbed a chicken coop. |
| 3 | 0:27:14.540 | 1634.540 | big | 1.22 | 1.10 | 25.3 | 30.4 | at least agree on that? I have two responses to that. First, with -- Well, I -- I think -- I think a "yes" or "no" would probably be a good starting place. |
| 4 | 0:37:44.620 | 2264.620 | small | 2.72 | 0.05 | 4.8 | 15.6 | that is true. So what is to happen if a state needing revenue says anyone who speeds has to forfeit the Bugatti, Mercedes, or a special Ferrari or even jalopy? |
| 5 | 0:38:08.160 | 2288.160 | under speech | 0.00 | 0.00 | - | - | there is a constitutional limit, which is the proof of instrumentality, the need to prove nexus. That isn't a problem because it was the Bugatti in which he was speeding. |
| 6 | 0:38:43.760 | 2323.760 | big | 3.48 | 2.30 | 27.2 | 37.0 | Louisa Barber case, one person over the -- the passenger limit and the entire ship is forfeit. This is -- history shows us in rem forfeiture -- So if the airplane is speeding -- |
| 7 | 0:46:31.860 | 2791.860 | under speech | 0.00 | 0.00 | - | - | I'm clear, you're asking us to overrule Austin? I think that's the most historically -- Because that's the only way that you can win with a straight face? No, I don't -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.260 to 0:03:06.260, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.260] MR. HOTTOT: Mr. Chief Justice, and may it please the Court: The freedom from excessive fines applies to the states because it is deeply rooted in our nation's history and traditions and fundamental to our scheme of ordered liberty. The State of Indiana appears not to dispute that straightforward answer to the actual question presented. And for good reason. The freedom from excessive fines easily warrants incorporation alongside the Eighth Amendment's other protections. This Court has said just that five times over the last 30 years. Without addressing the incorporation question directly, the State asked whether the clause applies to the states the same way that it applies to the federal government. But 50 years of incorporation precedent holds that incorporated Bill of Rights protections apply to the states the exact same way that they apply to the federal government. There's no reason to adopt the so-called two-track approach at this late stage of the incorporation doctrine, especially --

[0:01:06.440] JUSTICE GINSBURG: Is that so of all incorporations? What about the non-unanimous jury in -- in criminal cases?

[0:01:13.660] MR. HOTTOT: Justice Ginsburg, as the Court recognized in McDonald, the non-unanimous jury in criminal cases is an anomalous decision that results from a one-justice concurrence in the Apodaca case, and there's no reason, as the Court recognized in McDonald, for that to control when there's over 50 years of precedent, beginning in Malloy versus Hogan, Mapp, Aguilar, again in McDonald, rejecting that two-track approach. Adopting the two-track approach at this late stage would only invite further litigation about rights that are already incorporated. When this Court interpreted the Fourth Amendment right to be free from having your cell phone tracked in the Carpenter case, if my friend's argument were correct, we would have to relitigate whether that right applies to the states. Virtually all of the Bill of Rights, with the one exception noted by Justice Ginsburg, has been incorporated on the right-by-right approach used in McDonald, not on the application-by-application approach proposed --

[0:02:16.280] JUSTICE ALITO: There are a few others that have not been incorporated, isn't that right?

[0:02:19.560] MR. HOTTOT: Oh, that's true, absolutely. But that's either because they haven't been addressed by this Court, like in the case of the Third Amendment right against quartering soldiers, or because, as the Court recognized in McDonald, they long predate the era of selective incorporation. So I think it's possible that if the rights at issue in Bombolis and Hurtado were to come before this Court today, the results might be different. But we don't have to get into that history here because the history on the question presented of whether the Excessive Fines Clause applies to the states is clear.

[0:02:52.020] JUSTICE ALITO: What is the provision in the Constitution that you rely on?

[0:02:56.900] MR. HOTTOT: The Section 1 of the Fourteenth Amendment, Your Honor.

[0:02:59.500] JUSTICE ALITO: It's a component of -- of the liberty that's substantively -- substantively protected by the Fourth Amendment's Due

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - February 20, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/17-1091
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/17-1091/17-1091_20190220-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.5 MB)
- Length: 0:06:10.808 (370.808 s)
- Words: 730, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: Whisper skipped a stretch of speech: 0:00:12.800 to 0:00:17.920 (8 words recovered). Each was re-transcribed on its own and the words put in.
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 699 of Whisper's 730 words (95.8%; Oyez has 737).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:07.460 | 15 |
| JUSTICE GINSBURG | 0:00:12.180 | 0:06:09.720 | 707 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: In Case No. 17-1091, Timbs v. Indiana, Justice Ginsburg has the opinion of the Court.

[0:00:12.180] JUSTICE GINSBURG: Ginsburg. dealing in a controlled substance and a related The trial court sentenced Timbs to one year of home detention, five years of probation, and fees and costs totaling some $1,200. The police also seized Timbs's vehicle, a Land Rover SUV he had purchased for about $42,000, with money he received from an insurance policy when his father died. The State engaged a private law firm on a contingent fee basis to bring a civil suit for forfeiture of Timbs's Land Rover. Denying the request, requested forfeiture, the trial court observed that Timbs had recently purchased the vehicle for more than four times the maximum $10,000 monetary fine assessable against him for his drug conviction. Forfeiture of the Land Rover, the Court found, would be grossly disproportionate to the gravity of Timbs's offense and, therefore, unconstitutional under the Eighth Amendment's clause banning excessive fines. The Indiana Supreme Court ruled otherwise, holding that the Excessive Fines Clause constrains only Federal action and does not protect against exorbitant State impositions. We vacate that judgment. The Eighth Amendment's Excessive Fines Clause we hold today is an incorporated protection applicable to the States under the Fourteenth Amendment's Due Process Clause. A bill of rights protection is incorporated, meaning it is applicable to the States as well as the Federal government. We have explained if it is fundamental to our scheme of ordered liberty or deeply rooted in the Nation's history and tradition. The Excessive Fines Clause fits that description. The right to be free from excessive fines is stated in sources ranging from Magna Carta to the English Bill of Rights to State constitutions from the founding era to the present day, and for good reason. Exorbitant tolls undermine other constitutional liberties. Excessive fines historically were used to retaliate against or chill the speech of the sovereign's political adversaries. Even absent a political motive, the government may employ fines in

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:06:03.400-0:06:03.480: "concurrence or"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:01.160 | No. 17 -1091, | number 17-1091 |
| 0:00:12.180 | Ginsburg. | Tyson Timbs pleaded guilty in Indiana State Court to |
| 0:00:17.920 | (nothing) | offense. |
| 0:00:20.360 | Timbs | him |
| 0:00:32.400 | Timbs's | Timbs' |
| 0:00:55.900 | Timbs's | Timbs' |
| 0:00:59.220 | request, | (nothing) |
| 0:01:25.100 | Timbs's | Timbs' |
| 0:03:00.460 | manner | matter |
| 0:03:02.100 | accord | a court |
| 0:03:12.400 | revenue | revenues |
| 0:03:19.540 | cost the | costs a |
| 0:03:26.080 | its | (nothing) |
| 0:03:27.400 | -ramp | rem |
| 0:03:43.100 | -ramp | rem |
| 0:03:52.880 | a | the |
| 0:04:32.900 | -ramp | rem |
| 0:05:03.820 | v. | against |
| 0:05:20.660 | the | his |
| 0:05:24.820 | whether | where the |
| 0:05:40.680 | -ramp | rem |
