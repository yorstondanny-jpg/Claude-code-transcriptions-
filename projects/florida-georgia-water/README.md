# florida-georgia-water: Supreme Court No. 142-Orig

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/142-Orig
- Audio: https://www.supremecourt.gov/media/audio/mp3files/142-Orig.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/142-orig_p8k0.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 29 min on 4 CPU cores
- Audio length: 1:01:49.488 (3709.488 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.7 MB
- Official words: 10914 (plus 4 `(Laughter.)` markers), in 280 speaker turns
- ASR words: 10516
- Official words matched to an ASR word: 10064 of 10914 (**92.21%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.21% (threshold 85%).

414 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 7 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 20 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 142-Orig 2017 florida-georgia-water --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:25:52.960 | 1552.960 | under speech | 0.00 | 0.00 | - | - | answer that question is the Corps. And whereas the other case wants to get rid of them, in your case, you don't want them. But I would like them here -- |
| 2 | 0:27:06.940 | 1626.940 | big | 1.60 | 1.45 | 28.4 | 32.8 | the ultimate -- Well, what the Corps has said to me at the moment, I'm assuming, is sort of vague. My question is whether my question was a good question? Well -- |
| 3 | 0:31:33.880 | 1893.880 | under speech | 0.00 | 0.00 | - | - | down the Flint River. And then tomorrow, because they convince the mayor of Atlanta, whatever, to drink more Pepsi or something, or whatever they drink, Coca-Cola, I imagine, and -- and -- |
| 4 | 0:53:12.280 | 3192.280 | under speech | 0.00 | 0.00 | - | - | Could we ask for an amicus brief that does that? I -- I suppose you could if -- What do you think? In other words, what do you think we should do? |

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 27, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/142-Orig
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/142-orig/142-orig_20180627-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.0 MB)
- Length: 0:03:51.027 (231.027 s)
- Words: 593, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 561 of Whisper's 593 words (94.6%; Oyez has 590).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.920 | 0:00:08.340 | 19 |
| JUSTICE BREYER | 0:00:09.400 | 0:03:48.820 | 572 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.920 to 0:03:00.920, with each speaker's start time.

[0:00:00.920] CHIEF JUSTICE ROBERTS: Justice Breyer has the opinion of the court in Case No. 142 on our original docket, Florida v. Georgia.

[0:00:09.400] JUSTICE BREYER: this is a rather technical case in our original jurisdiction. Florida and Georgia for many years have disputed the Division of Water in an interstate water basin that goes from northern Georgia down through Florida and into the Gulf of Mexico. If you want to think of the rivers, there's the Flint River that goes along the eastern side. That's got a big capital Y. It would be on the right side if you looked at the Y. It goes from south of Atlanta down to the bottom of the state. And on the other side is the Chattahoochee, which goes along the western side to the bottom of the state. At the bottom of the state, they mix. They meet in Lake Seminole. They fly going to Florida, and they change their name to the Apalachicola, and they run down to the Gulf. Now, Florida says Georgia takes too much water out of the Flint. We said we'd exercise our original jurisdiction. We appointed a special master. He built a lengthy record, and eventually he filed a 70-page report recommending that this Court deny Florida's claim for relief, because in his view, even if Florida was right about what Georgia is doing with the water, even if there would be weather a significant amount of extra water, if Georgia gave the extra water, would come into Florida, depends upon the U .S. Army Corps of Engineers, which has dams on the Chattahoochee and which is not in the case. So the master's report says Florida failed to show by clear and convincing evidence that even if it was injured, it failed to show that the Court could grant meaningful relief by issuing an equitable decree. Florida took exceptions. It said here the special master applied too strict a standard about relief. And if you had a proper standard, Florida did show enough. So we have reviewed those parts of the record, and it's a big record, to which the master's report and the parties have referred us, and certain other parts that we thought were relevant. And what we do is remand the case to the master for further proceedings. Five of us think that the special master, as Florida said, did apply too strict a standard, and that under a proper standard, Florida did adequately show that relief may be possible with the core operation of the Corps. So we think the master should go on and make factual findings. Did Georgia, in fact, use too much of that Flint River water? And if so, could Florida benefit significantly from a cap on what Georgia does? Four of us dissent on that point. The opinions are lengthy. They're heavily fact-dependent. If you wish to learn something about the beauty and emotional appeal of that beautiful southwestern river,

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:09.400-0:00:10.120: "Breyer,"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:04.180 | No. | number |
| 0:00:20.520 | an | the |
| 0:00:27.120 | want | were |
| 0:00:28.900 | there's | there is |
| 0:00:33.860 | It | (nothing) |
| 0:00:35.960 | the | (nothing) |
| 0:00:49.140 | going to | and go into |
| 0:00:58.920 | of | (nothing) |
| 0:01:00.640 | we'd | we would |
| 0:01:21.680 | weather | whether |
| 0:01:53.860 | It | and |
| 0:01:59.720 | you | he |
| 0:02:10.200 | have | are |
| 0:02:10.680 | us, and | as in |
| 0:02:12.140 | that | (nothing) |
| 0:02:33.140 | Corps. | Court. |
| 0:02:35.180 | the | (nothing) |
| 0:02:53.040 | They're | They are |
| 0:02:53.980 | -dependent. | dependant. |
| 0:02:59.860 | southwestern river, | (nothing) |
| 0:03:02.880 | I'd | I would |
| 0:03:05.280 | one called Cat Chataucci. | going forward Chattahoochee |
| 0:03:17.200 | (nothing) | and |
| 0:03:19.300 | (nothing) | the |
