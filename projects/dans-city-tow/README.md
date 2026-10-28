# dans-city-tow: Supreme Court No. 12-52

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2012/12-52
- Audio: https://www.supremecourt.gov/media/audio/mp3files/12-52.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2012/12-52_d1oe.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 23 min on 4 CPU cores
- Audio length: 0:59:19.158 (3559.158 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.5 MB
- Official words: 9336 (plus 9 `(Laughter.)` markers), in 176 speaker turns
- ASR words: 9171
- Official words matched to an ASR word: 8861 of 9336 (**94.91%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.91% (threshold 85%).

226 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 36 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 12-52 2012 dans-city-tow --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-47.9 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:05:08.220 | 308.220 | big | 1.64 | 1.50 | 23.3 | 29.1 | mean, do they have to go to the Department of Transportation? Boston couldn't function. I know that they do tow cars. I don't know that firsthand, but I've seen it. |
| 2 | 0:07:37.940 | 457.940 | medium | 2.12 | 1.65 | 19.6 | 27.7 | him $100. And he tows the vehicle, puts it in my garage and says, give me the $100. And I say, ha, ha, I'm not going to give you $100. |
| 3 | 0:21:16.310 | 1276.310 | big | 4.86 | 4.20 | 26.9 | 36.5 | to eat those words, they were wrong, or -- or somehow you don't come within them? Respectfully, Justice Scalia, I think those words came from your dissent in that case. Ah. |
| 4 | 0:21:22.370 | 1282.370 | big | 3.53 | 3.35 | 29.1 | 36.4 | words, they were wrong, or -- or somehow you don't come within them? Respectfully, Justice Scalia, I think those words came from your dissent in that case. Ah. I forgot that. |
| 5 | 0:21:28.180 | 1288.180 | under speech | 0.00 | 0.00 | - | - | don't come within them? Respectfully, Justice Scalia, I think those words came from your dissent in that case. Ah. I forgot that. So you say they were wrong, you say? |
| 6 | 0:40:59.200 | 2459.200 | medium | 0.90 | 0.75 | 22.4 | 26.9 | its -- its apparent meaning, "related to," and we finally concluded you can't do that. So what do you want us to make up? What kind of a limitation do you -- |
| 7 | 0:51:58.910 | 3118.910 | small | 0.64 | 0.10 | 12.4 | 19.4 | we have two choices. In Morales, since I can mock my own opinions, I wrote at the end, "it's not -- when it's too tenuous, remote or peripheral." That's singularly unhelpful. |
| 8 | 0:52:02.910 | 3122.910 | under speech | 0.00 | 0.00 | - | - | my own opinions, I wrote at the end, "it's not -- when it's too tenuous, remote or peripheral." That's singularly unhelpful. It seems to -- there -- I thought so at the time. |
| 9 | 0:54:30.710 | 3270.710 | big | 1.52 | 1.35 | 30.2 | 37.5 | where the States were trying to use specific guidelines. Well, why doesn't this one really whack them, though? It's treble damages and all that. You can answer my question, yes. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.960 to 0:03:09.960, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.960] MR. BOUFFARD: Mr. Chief Justice, and may it please the Court: The issue in this case is whether Section 14501 of the United States Transportation Code expressly preempts the Respondent's State law consumer protection in tort claims for damages against a tow trucker who towed his vehicle lawfully and then, several months later, disposed of the vehicle after the fees for towing and storage had not been paid. Both of these claims are preempted because they are directed at the conduct -- the type of conduct that tow truck companies all over this country every day engage in, in dealing with a particular type of tow that's referred to in the business as nonconsensual tows.

[0:01:04.900] JUSTICE GINSBURG: Mr. Bouffard, this law, this New Hampshire law, it regulates storage. Is this a law that applies only to the towing companies who tow the automobile and then store it, or does the law apply, say, to a garage, say, someone brings a car to a garage for repairs, and does this storage law regulate garage operations as well as towing operations?

[0:01:39.560] MR. BOUFFARD: Justice Ginsburg, this law regulates abandoned motor vehicles. It's an abandoned motor vehicle law.

[0:01:45.560] JUSTICE GINSBURG: So -- so it would apply to a garage operator.

[0:01:48.320] MR. BOUFFARD: Well, if a garage operator came into possession of an abandoned motor vehicle, then I suppose it would. If -- if you look at the -- at the title to this subchapter of this New Hampshire statute, the title is abandoned vehicles, Your Honor.

[0:02:01.173] JUSTICE GINSBURG: Yes, but what made it abandoned was that they tried to locate the owner, couldn't and so -- this same thing could happen with a garage owner as happened to the towing truck. So there's nothing peculiar about being in the towing business that makes this storage application -- storage statute apply.

[0:02:22.660] MR. BOUFFARD: Well, let me be clear about this statute, Your Honor. It's an abandoned vehicle statute, and what's really important to understand with this case is that none of the Plaintiff's claims rely on this abandoned vehicle statute. The Plaintiff has pled in his complaint a couple of allegations of violations of this abandoned vehicle law, but the substantive rights that were sued upon by the Plaintiff in this case do not live in the abandoned motor vehicle law. The substantive rights that were sued upon by the Plaintiff live in the State's consumer protection law, which is a separate New Hampshire statute, unrelated to the abandoned vehicle law. And

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 13, 2013.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2012/12-52
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2012/12-52/20130513o_12-52.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.4 MB)
- Length: 0:05:31.651 (331.651 s)
- Words: 643, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 610 of Whisper's 643 words (94.9%; Oyez has 640).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:10.780 | 18 |
| JUSTICE GINSBURG | 0:00:10.780 | 0:05:30.560 | 621 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Mr. Ginsburg has our opinion this morning in Case 1252, Dan City Used Cars v. Pelkey. This case

[0:00:10.780] JUSTICE GINSBURG: concerns the preemptive scope of the Federal Aviation Administration Authorization Act of 1994, its acronym, F4A, an act about motor carriers, not airplanes. The F4A bars State laws related to a price, route, or service of any motor carrier with respect to the transportation of property. The question presented is whether that provision precludes State law claims stemming from the storage and disposal of towed vehicles. We hold it does not. Respondent Robert Pelkey owned a Honda Civic, which he parked in the lot of his apartment complex. Tenants were required to remove their cars in the event of a snowstorm, so the snow could be cleared. When it snowed heavily in February 2007 and Pelkey failed to remove his car, his landlord engaged Dan City Used Cars to tow and store the Honda. At the time, an unknown to Dan City, Pelkey was suffering from a grave medical condition. Soon thereafter, he had surgery, suffered a heart attack, and remained hospitalized for two months. New Hampshire's abandoned motor vehicle law allows storage companies to dispose of unclaimed cars if efforts to locate and notify the owner fail. Relying on that law, Dan City set an auction date for Pelkey's car. Pelkey learned of the upcoming auction upon his discharge from the hospital. Two days prior to the scheduled auction, Pelkey's attorney notified Dan City that Pelkey wished to reclaim the car and would pay charges due for towing and storage. Dan City nevertheless proceeded on its disposal course. Attracting no bidders at the auction, Dan City traded the car away. Receiving no proceeds from the sale, Pelkey sued Dan City's in New Hampshire State Court. He alleged that in selling his Honda, Dan City failed to meet requirements of New Hampshire's abandoned vehicle law. Consequently, Pelkey sought damages under New Hampshire's Consumer Protection Act and common law. The trial court granted summary judgment to Dan City, holding

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:00.000 | Mr. | Justice |
| 0:00:04.800 | Dan | Dan's |
| 0:00:28.800 | bars | bar |
| 0:01:21.360 | Dan | Dan's |
| 0:01:28.640 | an | and |
| 0:01:29.500 | Dan | Dan's |
| 0:01:56.520 | Dan | Dan's |
| 0:01:58.640 | for | of |
| 0:02:08.220 | scheduled | schedule of |
| 0:02:11.640 | Dan | Dan's |
| 0:02:20.840 | Dan | Dan's |
| 0:02:27.900 | Dan | Dan's |
| 0:02:35.060 | Dan City's | Dan's City |
| 0:02:42.620 | Dan | Dan's |
| 0:02:58.600 | Dan | Dan's |
| 0:03:49.980 | regress | redress |
| 0:03:50.940 | Dan | Dan's |
| 0:03:56.920 | showing, | towing |
| 0:04:03.980 | it | he |
| 0:04:23.760 | Dan | Dan's |
| 0:04:43.360 | Dan | Dan's |
| 0:04:58.280 | Dan | Dan's |
| 0:05:22.480 | Congress's | Congress' |
