# abitron-influencer: Supreme Court No. 21-1043

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2022/21-1043
- Audio: https://www.supremecourt.gov/media/audio/mp3files/21-1043.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/21-1043_j4pf.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 48 min on 4 CPU cores
- Audio length: 1:27:14.280 (5234.280 s)
- `audio/argument.mp3`: mono, 64 kbps, 41.9 MB
- Official words: 15091 (plus 3 `(Laughter.)` markers), in 287 speaker turns
- ASR words: 14607
- Official words matched to an ASR word: 13998 of 15091 (**92.76%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.76% (threshold 85%).

511 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 12 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 27 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 21-1043 2022 abitron-influencer --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-44.2 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:31:00.160 | 1860.160 | under speech | 0.00 | 0.00 | - | - | somebody might see something on the internet would not satisfy any proximate cause standard. Well, but, I mean, let's say it's, you know, an influencer, what -- whatever that is, but -- |
| 2 | 0:36:07.240 | 2167.240 | big | 2.70 | 1.15 | 21.6 | 34.1 | U.S., we don't think the proximate cause link to the confusion in the United States would be happening. Well, what if they bought 50 and they didn't speak any German -- |
| 3 | 0:49:25.400 | 2965.400 | medium | 1.60 | 0.85 | 24.8 | 33.7 | outcome. Yes. It's just, instead of asking kind of a metaphysical question about a statutory -- a statute's focus, which seems to me to kind of call for a legislative séance -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:14.540 to 0:03:14.540, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:14.540] MR. WALKER: Mr. Chief Justice, and may it please the Court: The Lanham Act does not apply to Petitioners' use of trademarks in foreign countries because nothing in the Act provides the clear, affirmative, and unmistakable indication needed to overcome the presumption against extraterritoriality, especially as to foreign defendants, like Petitioners. The text of the statute never says it applies to uses of trademarks outside the United States. And it is a foundational principle of both U.S. and international trademark law, embodied in multiple treaties, that trademark protections are inherently territorial and do not extend beyond the borders of the country granting protection. Any argument that the Act extends -- departs from that longstanding principle would have to be based on especially compelling evidence. But, here, Hetronic International offers only the text definition of commerce, and this Court has repeatedly rejected the notion that commerce language is enough to extend the law to foreign conduct, even if that language otherwise invokes the full scope of a constitutional commerce power. International also invokes this Court's decision in Steele. But Steele, by its terms, addressed only the Act's application to U.S. citizens acting abroad. There is no reason to discard that self-imposed limit and extend Steele to reach foreign defendants like Petitioners. To the contrary, extending the Lanham Act's reach into foreign countries would create the very risk of international friction that this Court's current extraterritoriality doctrine seeks to avoid. That leads to the suggestion that imposing liability for foreign sales to foreign buyers by foreign companies somehow qualifies as a domestic application of the Act. But, as International itself concedes, applying U.S. law to conduct abroad based on effects in the United States is an extraterritorial application of the law. It is not a way of applying a nonextraterritorial law domestically. Both the text and the focus of the Lanham Act require a domestic use of the mark in commerce. Because Petitioners' foreign sales involve only uses outside the United States, they fall outside the Act's scope. I welcome the Court's questions.

[0:02:25.660] JUSTICE THOMAS: Could you imagine any set of circumstances where a sale that involves an international transaction could also involve conduct in the United States that violates the Lanham Act?

[0:02:37.880] MR. WALKER: So I think one example here would be the -- the 202,000 euros worth of direct sales to U.S. customers. So those sales involved foreign buyers, the Petitioners, who were overseas at the time, but they were sold into the United States to foreign buyers. And I think, in that situation, the mark is being used on those goods in commerce within the territory of the United States. And so we have not disputed that that's permissible domestic application of the Lanham Act here.

[0:03:07.028] JUSTICE SOTOMAYOR: I don't understand what that difference is from the sales to people in foreign countries who designated the United States

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 29, 2023.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2022/21-1043
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2022/21-1043/21-1043_20230629-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.3 MB)
- Length: 0:01:03.576 (63.576 s)
- Words: 127, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 121 of Whisper's 127 words (95.3%; Oyez has 128).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:09.920 | 16 |
| JUSTICE ALITO | 0:00:09.920 | 0:01:02.440 | 111 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Alito has the opinion of the court in two cases this morning. The first is

[0:00:09.920] JUSTICE ALITO: Abatron versus Hetronic. Sections 32 and 43 of the Lanamack prohibit the unauthorized use in commerce of protected trademarks when the use is likely to cause confusion. After a trial, a company called Hetronic International received a large damages award on claims that five foreign entities infringed its trademark rights both domestically and globally. We granted certiorari to review the 10th Circuit's affirmance and based on the presumption against extraterritoriality, we now vacate the judgment and remain the case for further proceedings. Justice Jackson has filed a concurring opinion. Justice Sotomayor has filed an opinion concurring in the judgment which is joined by the Chief Justice, Justice Kagan and Justice Barrett.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:09.920 | Abatron versus | Abitron v. |
| 0:00:16.820 | Lanamack | Lanham Act |
| 0:00:40.200 | 10th | Tenth |
| 0:00:47.680 | remain | remand |
| 0:00:51.680 | a | the |
