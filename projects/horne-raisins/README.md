# horne-raisins: Supreme Court No. 14-275

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2014/14-275
- Audio: https://www.supremecourt.gov/media/audio/mp3files/14-275.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2014/14-275_2b8e.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 59 min on 4 CPU cores
- Audio length: 1:01:12.372 (3672.372 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.4 MB
- Official words: 10555 (plus 7 `(Laughter.)` markers), in 341 speaker turns
- ASR words: 9826
- Official words matched to an ASR word: 9554 of 10555 (**90.52%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
  Not counted: `989.166(c),` 3524.600-3529.100 (4.50 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 90.52% (threshold 85%).

568 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 9 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 13 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 14-275 2014 horne-raisins --model medium.en

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-40.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:06:18.540 | 378.540 | small | 0.84 | 0.20 | 16.1 | 23.5 | yes. Well, so I guess what Justice Sotomayor's question is is why wouldn't the same be true as to raisins? Because raisins are not wild animals, even if they're dancing -- |
| 2 | 0:29:49.460 | 1789.460 | under speech | 0.00 | 0.00 | - | - | Central. This is different. This is different because you come up with the truck and you get the shovels and you take their raisins, probably in the dark of night. |
| 3 | 0:39:47.840 | 2387.840 | small | 0.40 | 0.00 | 7.5 | 9.2 | government can prohibit the -- the introduction of harmful pesticides into interstate commerce. I'm not sure it can prohibit the introduction of raisins. I mean, that's a -- you know, dangerous raisins. |
| 4 | 0:52:57.700 | 3177.700 | small | 0.50 | 0.00 | 9.5 | 11.0 | is a sensible program for you to prevail, do you? No, we do not. The question -- I mean, we could think that this is a ridiculous program; isn't that right? |
| 5 | 0:53:14.700 | 3194.700 | under speech | 0.00 | 0.00 | - | - | every grower since 1949 has had a per se takings. Mr. Kneedler, I'd like to get you -- It doesn't help your case that it's ridiculous, though. You -- you acknowledge that. |
| 6 | 1:00:55.200 | 3655.200 | big | 5.54 | 4.95 | 21.2 | 29.0 | unusual. Mr. McConnell, this is probably neither here nor there, but what has the impact of the drought been on the raisin producers? Do you know? It is not good. |
| 7 | 1:01:02.560 | 3662.560 | under speech | 0.00 | 0.00 | - | - | is probably neither here nor there, but what has the impact of the drought been on the raisin producers? Do you know? It is not good. Very carefully guarded response. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.700 to 0:03:07.700, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.700] MR. MCCONNELL: Mr. Chief Justice, and may it please the Court: Thank you for being willing to hear this little case a second time. It does involve some important principles and the livelihoods of Marvin and Laura Horne, and more indirectly, hundreds of small California raisin growers will be profoundly affected. This is an administrative enforcement proceeding that was brought by the Department of Agriculture against my clients commanding the relinquishment of funds connected to specific pieces of property, namely, reserve-tonnage raisins. My clients appear in their capacity as handlers, but under their -- in the particular facts of this case, the economic circumstances are somewhat different than are ordinarily true in -- in this industry because as handlers, the Hornes actually assumed the full financial responsibility for the raisins that were not turned over to the Department of Agriculture. The producers in this case were fully paid for their raisins. This is a factual finding to be found in the judicial officer's opinion at 66a of the appendix to the -- to the petition. The Hornes paid the producers for their raisins. According to the judicial officer, those raisins became part of the inventory of the Hornes. The -- when the Raisin Administrative Committee, which I'll refer to as the RAC, came after the raisins, it was the Hornes and the Hornes only who bore the economic burden of this taking.

[0:01:45.840] JUSTICE GINSBURG: I thought that -- I thought the growers were paid only for the volume that they were permitted, that was permitted, the permitted volume, and that they were not paid for what is -- goes in the reserve pool.

[0:02:04.480] MR. MCCONNELL: Justice Ginsburg, that is true in the ordinary course. That was not true in this particular case because of the unusual business model of -- of my clients. These producers were paid the -- for all of their raisins.

[0:02:19.920] JUSTICE GINSBURG: Are you objecting to the volume limitation, or is it just that the -- the reserve pool that you find --

[0:02:30.040] MR. MCCONNELL: We --

[0:02:30.770] JUSTICE GINSBURG: -- troublesome?

[0:02:31.500] MR. MCCONNELL: We believe that a volume limitation would be a use restriction. It might possibly be challengeable under the Penn Central Test, but it is -- would not be a per se taking. In this case, because the government, the RAC, which is an agent of the Department of Agriculture, actually takes possession, ownership of the raisins, it is that -- it is that aspect of the case which we're challenging against the taking.

[0:02:54.920] JUSTICE GINSBURG: But that's what so -- so puzzling because if -- if you're not challenging the volume limit itself, you can't sell more than 60 percent of your crop.

[0:03:05.600] MR. MCCONNELL: That's correct.

[0:03:07.500] JUSTICE GINSBURG: And what
