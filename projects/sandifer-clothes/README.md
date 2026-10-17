# sandifer-clothes: Supreme Court No. 12-417

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2013/12-417
- Audio: https://www.supremecourt.gov/media/audio/mp3files/12-417.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2013/12-417_o8kg.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 29 min on 4 CPU cores
- Audio length: 0:59:49.799 (3589.799 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.7 MB
- Official words: 10071 (plus 8 `(Laughter.)` markers), in 199 speaker turns
- ASR words: 9838
- Official words matched to an ASR word: 9302 of 10071 (**92.36%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.36% (threshold 85%).

308 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 45 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 12-417 2013 sandifer-clothes --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.1 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:00:52.040 | 52.040 | big | 4.96 | 4.55 | 26.0 | 34.4 | of that in this courtroom: Glasses, necklaces, earrings, wristwatches. There may be a toupee, for all we know. Those things are not commonly referred to as clothes. I resent that. |
| 2 | 0:08:10.260 | 490.260 | under speech | 0.08 | 0.00 | - | - | an old saying that, if it looks like a duck and it swims like a duck and it quacks like a duck, it's a duck. It's a very famous saying. |
| 3 | 0:08:38.000 | 518.000 | under speech | 0.00 | 0.00 | - | - | guns; it's probably not a duck. And yet, if you took a picture of just the duck -- You don't want to say they are "wearing guns," not in this case. |
| 4 | 0:08:43.500 | 523.500 | medium | 0.68 | 0.55 | 20.2 | 26.8 | the duck -- You don't want to say they are "wearing guns," not in this case. No, they are wearing camouflage and holding guns. And holding guns. Holding. I certainly misspoke. |
| 5 | 0:37:16.680 | 2236.680 | under speech | 0.26 | 0.10 | 19.0 | 21.1 | Well, is there anything wrong with what I just said? There is, Your Honor. What? So what of opening your locker? Opening your locker -- Opening your locker is not clothes. |
| 6 | 0:39:15.260 | 2355.260 | big | 1.98 | 1.70 | 20.4 | 28.8 | as it is -- the Congress was after allowing this block of time to be dealt with by -- So maybe we can call them "constructive clothes," which means they're not clothes. |
| 7 | 0:49:56.580 | 2996.580 | small | 0.40 | 0.25 | 31.1 | 34.8 | again, going to be somewhat fact-dependent, and I don't mean to provide a general rule for all cases. Well, actually, that's what we are looking for, so why don't you? |
| 8 | 0:59:42.020 | 3582.020 | medium | 3.36 | 2.20 | 18.5 | 24.3 | this and all this -- these guidance documents, why they've never just like come to everybody's aid and issued a regulation? I do not know, Your Honor. Too complicated is why. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.800 to 0:03:07.800, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.800] MR. SCHNAPPER: Mr. Chief Justice, and may it please the Court: We agree with the government that not everything an individual wears is clothes. We disagree with the government as to the appropriate standard for distinguishing things that are and are not clothes under Section 203(o). I'd like to begin with the area we're -- in which we are in agreement with the government, although not with Respondent. In ordinary parlance, not everything an individual wears would be referred to as clothes. There are examples of that in this courtroom: Glasses, necklaces, earrings, wristwatches. There may be a toupee, for all we know. Those things are not commonly referred to as clothes.

[0:00:51.995] JUSTICE SCALIA: I resent that. (Laughter.)

[0:00:57.000] MR. SCHNAPPER: And nor are neck braces, which I've seen worn in this courtroom. It's also the case that there are any number of things that people wear to do their jobs that are not clothes. The police officers outside the building are wearing guns, radios. I suspect they have handcuffs; I couldn't see those. The quarterback who played for your team yesterday had a quarterback playbook wristband with the plays on -- on his -- on his wrist. Workers wear tool belts. It's -- one of the recurring -- recurring issues that has come up in these cases are knife scabbards. We don't think anyone would, in ordinary parlance, call those things clothes. And we think that's the significant limitation on this. The -- the company's account of this is that everything that you wear to do your job is -- is clothes, and we think that's just not consistent with ordinary language. And although the government's views have, to some extent, evolved over time in all of this, they've always taken the position that not everything you wear are clothes. Even in its -- in the 2002 opinion letter, they drew the line at tools and scabbards. And so even though you could be wearing those things, those are not clothes.

[0:02:20.240] JUSTICE SCALIA: Tools and what?

[0:02:20.660] MR. SCHNAPPER: Scabbards.

[0:02:21.140] JUSTICE SCALIA: Scabbards.

[0:02:22.180] MR. SCHNAPPER: Knife scabbards. The Tenth Circuit holds a knife scabbard as clothes because it's like holsters. I --

[0:02:29.300] JUSTICE GINSBURG: But we're dealing with here, from the picture, that looks like clothes to me.

[0:02:36.220] MR. SCHNAPPER: Your Honor, I think that your question raises an excellent point. One of the problems with the picture is that it withholds from you other information that you would use to assess whether to describe it as clothes. You don't know what --

[0:02:52.880] JUSTICE KENNEDY: Except you would look and say, those clothes probably have something special underneath them. I mean, in ordinary parlance I think that would be a proper use of diction.

[0:03:04.860] MR. SCHNAPPER: If you saw an airbag

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 27, 2014.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2013/12-417
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2013/12-417/20140127o_12-417.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.6 MB)
- Length: 0:06:17.835 (377.835 s)
- Words: 862, transcribed by faster-whisper `small.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
  Oyez lists no names for 2 of these turns, so they come from the text: a turn that opens "Justice X has our opinion" is the Chief Justice introducing the case, and the next turn is Justice X.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 819 of Whisper's 862 words (95.0%; Oyez has 859).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:04.000 | 13 |
| JUSTICE SCALIA | 0:00:06.040 | 0:06:16.380 | 843 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Scalia has the opinion of the Court in two cases this morning.

[0:00:06.040] JUSTICE SCALIA: The first of these is Sandifer v. United States Steel Corporation. That is here on writ of certiorari to the United States Court of Appeals for the Seventh Circuit. It is about what is called in the literature on this subject donning and doffing to good old Anglo-Saxon words that are not much used anymore. Although we still sing Don, we now are gay apparel at Christmas, and I suppose a well-bred gentleman still doffs his hat to a lady. A group of steelworkers sued their employer, United States Steel Corporation, under the Fair Labor Standards Act of 1938. The workers sought back pay for time spent donning and doffing pieces of protective gear. Because of the number of workers involved, possibly 800 or more, the aggregate amounts of time and money at issue are substantial. U .S. Steel contends that its collective bargaining agreement with the workers' union relieves it of the obligation to pay for this donning and doffing time. The union thought that they would prefer to get some other compensation instead. Whether that provision of the collective bargaining agreement is effective depends on 29 U .S .C. Section 2030, which allows unions to bargain over whether employers must pay for, quote, time spent in changing clothes or washing at the beginning or end of each work day. The workers argued that the donning and doffing of protective gear does not count as changing clothes. The district court disagreed, granting summary judgment to U .S. Steel and the 7th Circuit affirmed. We granted certiorari to determine the meaning of the phrase, changing clothes. And today we affirm. The workers argue that protective clothing is not clothes. That seems to us unsupported by both the text of the statute and ordinary logic. We give the word clothes its common and contemporary meaning. Dictionaries from the time of the statute's enactment show that clothes are items that are both designed and used to cover the body and are commonly regarded as articles of dress. While not supporting the workers' argument that protective clothing is ipso facto not clothes, neither does this definition support the construction adopted by some courts and advocated by U .S. Steel here, which says that clothes consist

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:06.560 | these | this |
| 0:00:22.000 | (nothing) | -- in the |
| 0:00:27.080 | to | two |
| 0:00:34.880 | are | Our |
| 0:00:55.440 | time | times |
| 0:01:36.120 | 2030, | 203(o), |
| 0:02:04.600 | 7th | Seventh |
| 0:02:31.560 | show | showed |
| 0:02:45.820 | that | (nothing) |
| 0:03:46.080 | alteration, | alternation |
| 0:03:51.280 | this | the |
| 0:04:00.940 | (nothing) | the |
| 0:04:38.880 | coratlex. | curat lex. |
| 0:05:12.860 | whole | hold |
| 0:05:27.300 | if | (nothing) |
| 0:05:29.140 | non -close | non-clothes |
| 0:05:33.360 | factually terminations | factual determinations |
| 0:05:37.920 | -close | clothes |
| 0:05:45.560 | workday, | work day, but -- |
| 0:06:04.140 | 2030. | 203(o). |
| 0:06:15.840 | 7. | seven. |
