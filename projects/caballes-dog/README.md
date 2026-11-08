# caballes-dog: Supreme Court No. 03-923

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-923/20041110a_03-923.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2004/03-923.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 20 min on 4 CPU cores
- Audio length: 0:55:05.874 (3305.874 s)
- `audio/argument.mp3`: mono, 64 kbps, 26.5 MB
- Official words: 9402 (plus 9 `(Laughter.)` markers), in 297 speaker turns
- ASR words: 9133
- Official words matched to an ASR word: 8751 of 9402 (**93.08%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.08% (threshold 85%).

331 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 4 times. ASR words with no official counterpart
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 03-923 2004 caballes-dog --model small.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2004/03-923.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-923/20041110a_03-923.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-54.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:05:34.440 | 334.440 | big | 2.56 | 2.40 | 26.5 | 33.4 | that he was someone to look for? Because I don't imagine you arrest everybody on I-80 that goes 70 miles an hour. I've done it many times myself is why - |
| 2 | 0:05:38.380 | 338.380 | big | 1.72 | 1.60 | 34.9 | 42.0 | was someone to look for? Because I don't imagine you arrest everybody on I-80 that goes 70 miles an hour. I've done it many times myself is why - Inadvertently. Inadvertently. |
| 3 | 0:07:13.860 | 433.860 | small | 0.62 | 0.30 | 24.8 | 29.8 | the fact that you don't have a privacy interest in contraband, it doesn't seem to me -- I -- I don't think you need that argument. I think you should use it. |
| 4 | 0:07:50.620 | 470.620 | under speech | 0.18 | 0.05 | 26.2 | 26.2 | at all sure. I would hope the case would come out differently than - Well, what - Do you have any authority for that other than Justice Scalia's speculation about how this - |
| 5 | 0:12:02.522 | 722.522 | under speech | 0.00 | 0.00 | - | - | sauna, and doing other intimate things in the house. I think there was a reference to my lady's bath in the opinion. A nice turn of phrase, as I recall. |
| 6 | 0:20:15.420 | 1215.420 | big | 1.38 | 1.20 | 24.4 | 31.9 | to sniff everything from - But not in 1790. Not - Did you come here - You don't know that, do you? Did you come here having researched all about dogs in 1790? |
| 7 | 0:30:26.080 | 1826.080 | small | 0.60 | 0.25 | 31.3 | 36.7 | car, you might run into people or animals with sharp noses. And a lot of them can detect marijuana. And you know, maybe it's a Limburger cheese. I don't know. |
| 8 | 0:47:11.840 | 2831.840 | small | 1.20 | 0.10 | 8.4 | 18.7 | it you don't -- Sorry it took me so long. Is there anything wrong with the policeman himself taking a sniff? It goes back to - It's the great Limburger cheese robbery. |
| 9 | 0:48:18.400 | 2898.400 | medium | 1.68 | 0.80 | 17.2 | 25.4 | saying you couldn't draw that line, but I'm saying it's pretty tough I think. I guess you're telling me I'm - I'm the underdog in this case. Well, I don't know. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.080 to 0:03:08.080, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.080] MS. MADIGAN: Thank you, Justice Stevens, and may it please the Court: This Court has made clear on several occasions, including 21 years ago in Place and 4 years ago in Edmond, that a sniff by a drug-detection dog is not a Fourth Amendment search, and if something is neither a search nor a seizure, then it requires no Fourth Amendment justification.

[0:00:30.880] JUSTICE SOUTER: Well, we've held that it's certainly not a -- a full-blown search. It's not a search in the classic sense, but a Terry stop isn't an arrest in -- in the classic sense either. We -- we have said that that is a kind of seizure. Why do -- I think your -- your argument assumes that this for -- for purposes of search analogies that something is either a -- a full-dress search or it's not a search at all. Why isn't there a -- a possibility of - of a kind of middle ground on searches just as there is on seizures?

[0:01:06.340] MS. MADIGAN: Well, this Court made clear in Arizona v. Hicks that it did not want to go down the road of creating something known as a quasi-search so that courts and police officers would be in the position of trying to determine whether or not something was a search or not.

[0:01:23.200] JUSTICE SOUTER: Oh, I -- I can -- I can just imagine the problems, but I mean, what -- I think what's -- what the -- what's bothering me about the case is that if we persist in -- in saying that -- that it's -- that it's an either and or question with no question with no possible gradation, then I assume nothing prevents the police from taking the dogs through every municipal garage in the United States and I suppose there's nothing that prevents the police from taking the dogs up to any homeowner's door, ringing the bell, and seeing if the dog gets a sniff of something when the door is opened. We're -- we're opening rather a -- a large vista for -- for dog intrusions, and -- and that's what's -- that's what's bothering me. Why -- why should we -- why should we open that vista if there is a possibility of a -- of a middle ground that would prevent it?

[0:02:17.660] MS. MADIGAN: Well, I would start with the reality that dog sniffs by their very nature, as this Court recognized in both Place and Edmond, are very unique both in terms of the manner in which the sniff is conducted, as well as the content of -- of the information that the sniff reveals, so that a dog sniff is only going to be able to reveal the presence or absence of contraband. And this Court has recognized that individuals have no privacy interest in the possession of contraband.

[0:02:52.040] JUSTICE GINSBURG: Does that imply that your answer is yes to the question? If we say, as you urge, a dog sniff is not a search, then the police are free to parade up and down every street in the country with dogs

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 24, 2005.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2004/03-923
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-923/20050124o_03-923.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.9 MB)
- Length: 0:03:41.597 (221.597 s)
- Words: 465, transcribed by faster-whisper `small.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (1 turn), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 439 of Whisper's 465 words (94.4%; Oyez has 459).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| JUSTICE O'CONNOR | 0:00:00.000 | 0:03:40.780 | 462 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] JUSTICE O'CONNOR: I also have an opinion to announce in 03-923, Illinois v. Kebias, that was authored by Justice Stevens. This is a case that comes to us from the Supreme Court of Illinois. In the opinion authored by Justice Stevens, we answer a narrow question. Whether the Fourth Amendment requires reasonable, articulable suspicion to justify using a drug-detection dog to sniff a vehicle during a legitimate traffic stop. An Illinois State trooper stopped Petitioner Kebias for speeding on an interstate highway when the officer radioed the police dispatcher to report the traffic stop. A member of the State's drug interdiction team overheard the transmission and drove to the scene along with his narcotics detection dog. On arrival, and while the first trooper was writing the warning ticket for speeding, the drug interdiction officer walked the dog around Kebias' car. The dog alerted at the trunk, prompting the officers to open the trunk where they discovered marijuana. Kebias was arrested and charged with a narcotics offense. The trial judge denied the motion to suppress the seized evidence. The Court found no Fourth Amendment violation because the officers did not unnecessarily prolong the traffic stop in order to conduct the dog sniff, and because the particular dog sniff was sufficiently reliable to establish probable cause to search the trunk. The Illinois Supreme Court reversed. In its view, the use of a narcotics detection dog converted the citizen police encounter from a lawful traffic stop into a drug investigation. And because the shift in purpose was not supported by any reasonable suspicion of drug activity, it was unlawful. We granted certiorari to review the Illinois Supreme Court's holding. We now vacate and remand. In our view, conducting a dog sniff would not change the character of a lawful traffic stop unless the dog sniff itself infringed on constitutionally protected privacy interests. Our cases make clear that it did not. To fall within the purview of the Fourth Amendment, police conduct must compromise a legitimate interest in privacy. Because a canine sniff by a well-trained drug detection dog does not itself reveal noncontraband items, and because any interest in possessing contraband cannot be deemed legitimate, the use of a properly trained drug detection dog during a lawful traffic

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:06.080 | v. Kebias, | versus Caballes |
| 0:00:39.640 | Kebias | Caballes |
| 0:01:10.540 | Kebias' | Caballes’ |
| 0:01:19.820 | Kebias | Caballes |
| 0:01:44.180 | establish | establishe |
| 0:01:52.400 | narcotics detection dog | narcotics-detection cog |
| 0:02:02.360 | shift in | shifting |
| 0:02:24.140 | sniff | sniffs |
| 0:02:25.840 | on constitutionally | unconstitutionally |
| 0:02:28.240 | interests. | interest. |
| 0:02:29.960 | make | made |
| 0:02:33.380 | purview | purviews |
| 0:02:41.660 | sniff | sniffs |
| 0:03:04.040 | interests. | interest. |
| 0:03:18.180 | a | the |
