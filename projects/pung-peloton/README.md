# pung-peloton: Supreme Court No. 25-95

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2025/25-95
- Audio: https://www.supremecourt.gov/media/audio/mp3files/25-95.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2025/25-95_32q3.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 39 min on 4 CPU cores
- Audio length: 1:44:31.704 (6271.704 s)
- `audio/argument.mp3`: mono, 64 kbps, 50.2 MB
- Official words: 17782 (plus 6 `(Laughter.)` markers), in 525 speaker turns
- ASR words: 17404
- Official words matched to an ASR word: 16672 of 17782 (**93.76%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.76% (threshold 85%).

457 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 13 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 85 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 25-95 2025 pung-peloton --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-49.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:28:14.840 | 1694.840 | under speech | 0.00 | 0.00 | - | - | case, with a tax debt of about 2200 bucks, it could have been the Peloton bike that was in the house. You think a Peloton bike today is worth $2,000? |
| 2 | 0:37:39.480 | 2259.480 | under speech | 0.00 | 0.00 | - | - | that as the basis for this foreclosure. Correct. So -- How did that happen? I don't think you have a long enough afternoon to explain the story of what happened here. |
| 3 | 0:42:08.180 | 2528.180 | under speech | 0.24 | 0.10 | 34.9 | 36.7 | briefs, it sounds to me like the tax assessor was like Inspector Javert, but it was even worse because Jean Valjean hadn't stolen the bread. I mean, you didn't even -- |
| 4 | 0:57:16.000 | 3436.000 | under speech | 0.00 | 0.00 | - | - | And, you know, the history there is pretty clear that, you know, Cooley's -- Cooley's -- if you invoke Cooley, you -- you -- you've got to eat your Cooley, it seems to me. |
| 5 | 1:24:15.380 | 5055.380 | under speech | 0.00 | 0.00 | - | - | there are a lot of bureaucracies involved and that the right hand's not always talking to the left hand. I appreciate that. We've all been -- we've all encountered that phenomenon. |
| 6 | 1:33:07.940 | 5587.940 | under speech | 0.00 | 0.00 | - | - | which -- but the result of them we believe is the same. 106 I understand that you think all roads lead to Rome and we win. I got -- I appreciate that. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.240 to 0:03:08.240, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.240] MR. ELLISON: Mr. Chief Justice, and may it please the Court: The Fifth Amendment requires just compensation be measured by the value of what's taken. The Sixth Circuit's categorical rule reducing just compensation to surplus auction proceeds in all instances was wrong. This Court has repeatedly confirmed that when the government takes property, the constitutional calculus begins with its fair market value. That is measured from the time of the take. The error here is clear. The Pung home was worth $194,400. The tax debt was roughly $2200. Just compensation meant returning remaining equity. The lower courts erred when holding that the later auction price of just $76,000, less the debt, was categorically the only just compensation owed. But this Court said it directly in Jacobs. An owner is owed just compensation, not inadequate compensation. Following Tyler, there are no windfalls to the government. This case now asks the Court to confirm the other half, that the Constitution likewise forbids confiscatory losses when being -- when being imposed upon a former owner. Federal courts should consider all relevant market -- evidence of market value and determine whether just compensation has, in fact, been paid. In addition to the Fifth Amendment, the Eighth Amendment's Excessive Fines Clause provides a backstop as well. Taking a six-figure home to punish over a small four-figure tax constitutes a fine and was sufficiently alleged to be grossly disproportionate to get past the initial pleading stage. The judgment below should be reversed, and I welcome the Court's questions.

[0:01:50.320] JUSTICE THOMAS: What do you do with the fact that the English and American legal traditions seem to permit these sorts of foreclosures?

[0:02:01.280] MR. ELLISON: So the -- the fact that the -- our history allows for these types of foreclosures is only one half of the equation. The other half of the equation historically is that protections have been built in, for example -- one of many, for example, is personalty has to be taken before real -- the real property, for example. This process that Isabella County undertook lacked that second half of that historical tradition. Yes, surplus is the ultimate outcome if, in fact, the auction resulted in a fair market value. But, when it doesn't result in a fair market value, historically, courts have been allowed to challenge inequity, to set aside the foreclosure itself, or to otherwise award damages or compensation in those particular circumstances.

[0:02:45.560] JUSTICE SOTOMAYOR: I'm sorry, where in your brief did you show -- where in your merits brief did you point to that history?

[0:02:54.460] MR. ELLISON: That history --

[0:02:55.500] JUSTICE SOTOMAYOR: I -- I know that there have been cases that talk about the fairness of an auction and that certain rules were set up to ensure fairness, that it had to be an

## Opinion announcement

No opinion announcement recording found on https://www.oyez.org/cases/2025/25-95. Nothing was transcribed.
