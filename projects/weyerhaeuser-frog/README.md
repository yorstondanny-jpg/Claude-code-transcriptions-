# weyerhaeuser-frog: Supreme Court No. 17-71

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/17-71
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-71.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-71_b97c.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 15 min on 4 CPU cores
- Audio length: 1:01:31.560 (3691.560 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.5 MB
- Official words: 4011 (plus 1 `(Laughter.)` markers), in 108 speaker turns
- ASR words: 3750
- Official words matched to an ASR word: 3676 of 4011 (**91.65%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 91.65% (threshold 85%).

235 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 12 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-71 2018 weyerhaeuser-frog --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:33:44.002 | 2024.002 | under speech | 0.00 | 0.00 | - | - | area which has very few trees. And we also know that this is a logging company, and so probably they have lots of trees. They like trees, not forever, but -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:21:54.602 to 0:24:54.602, official wording, with each turn's start time. Interruptions from the bench are included.

[0:21:54.602] JUSTICE GORSUCH: for now that I would agree with you and that we could review this. What more would you expect the Secretary to say, or could say, given the state of scientific evidence before the Secretary? That's not clear to me. The Secretary says there's -- there's just not any evidence of the benefits of exclusion that I -- that I can put a number on. And isn't -- isn't the way the statute written put some burden of proof incumbent upon the landowner or lessee to come forward with something quantifying the benefits of exclusion?

[0:22:27.902] MR. BISHOP: Right. Well, certainly, it's permissible for the agency to rely -- to characterize the benefits of inclusion as being biological, which is something that can be described but not quantified. But, on the other side of that ledger, the agency has to meet State Farm standards in identifying what the factors --

[0:22:49.577] JUSTICE GORSUCH: And what -- what -- on that, my question is, what more would you ask the Secretary to do? The Secretary did quantify the economic benefits exclusion and then said, compared to the benefits of inclusion, they're indeterminate. And, therefore, the burden of proving exclusion has not been met. And that burden, it seems to me, rests with you. So suppose I -- there's some judicial review possible here. Do we need to get into how many angels dance on the head of that pin if you -- if you've got no real complaint at the end of the day with the adequacy of the Secretary's --

[0:23:22.642] MR. BISHOP: Well, we do --

[0:23:22.682] JUSTICE GORSUCH: -- reasoning?

[0:23:22.682] MR. BISHOP: -- we do have that complaint. And, certainly, a remand would -- would allow us to explore that. But here, under State Farm, the inputs --

[0:23:29.642] JUSTICE GORSUCH: Well, could you explain that to me?

[0:23:30.922] MR. BISHOP: Yes, the inputs into the decision have to be fair and reasonable and the connection between those inputs and the ultimate decision have to be. Let -- let me give an -- an example of a very basic error that -- an example of an internal inconsistency. So the -- the Service refused to factor in the loss of Unit 1 to housing and to St. Tammany's tax base, and it did that because it found that Unit 1 is only 0.5 percent of developable land in the parish. There's a big problem with that. It included as developable land everything under -- south of Interstate 12, which is not developable because it flooded in Hurricane Katrina, everyone from that area is moving up to -- to us, to the higher ground. It said, in addition, it acknowledged that Unit 1 is particularly attractive for development because Highway 36 runs through it. It's an attractive area for development because it's connected to centers of -- where jobs -- where the jobs are. And yet -- so we have a Unit 1 that is already zoned, it's outside the flood zone, and it's well served by roads connecting it to jobs, but the Service treated every undeveloped area in the parish as fungible and said this just isn't an important development area, even though St. Tammany, as its brief explains in this case, says no, it's a very important development area. The -- that is what you get

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - November 27, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/17-71
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/17-71/17-71_20181127-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.9 MB)
- Length: 0:07:53.966 (473.966 s)
- Words: 1145, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1126 of Whisper's 1145 words (98.3%; Oyez has 1135).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:07:52.900 | 1144 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court today in Case 17-71, Weyerhaeuser v. The United States Fish and Wildlife Service. The amphibian reina civosa is popularly known as the dusky gopher frog, dusky because of its dark coloring and gopher because it lives underground. The frog is about 3 inches long with a large head and plump body. It is noted for covering its eyes with its front legs when it feels threatened, peeking out periodically until danger passes. The dusky gopher frog is native to the open canopy pine forests that used to cover the southeast, but more than 98 of those forests have been removed to make way for urban development, agriculture, and commercial timber farming. The near eradication of the frog's habitat sent the species into severe decline. By 2001, the frog's known wild population had dwindled to a group of 100 frogs at a single pond in southern Mississippi. That same year, the Fish and Wildlife Service listed the dusky gopher frog as an endangered species. Now, whenever the Service lists a new endangered species, it must also designate certain areas as, quote, critical habitat, unquote, for the species. The Endangered Species Act defines critical habitat to include certain areas where the species lives, as well as unoccupied areas that the Service determines to be, quote, essential for the conservation of the species, end quote. Now, after the Service designates land as critical habitat, all agencies of the Federal Government must check with the Service before approving any development that might harm the area. The Service's critical habitat designation for the dusky gopher frog included a timber plantation operated by the petitioner, Weyerhaeuser Company, where the frog had once lived. No frogs had been seen in the area for decades, but the site, dubbed Unit 1 by the Service, still possessed several of the rare ephemeral ponds where the frogs breed. The Service acknowledged that the closed forest canopy created by the close proximity of the timber trees was not hospitable to the frog, but determined that Unit 1 satisfied the statutory definition of unoccupied critical habitat because its rare breeding ponds made it essential for the conservation of the species. Weyerhaeuser and the other owners of Unit 1 challenged the designation in Federal court. Weyerhaeuser argued that Unit 1 cannot be critical habitat for the dusky gopher frog because it is not habitat. The frog cannot survive in the closed canopy plantation in its present state. The court of appeals rejected that position, holding that any land which the Service considers essential for the conservation of the species

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:39.460-0:00:39.840: "percent"
- 0:00:58.320-0:00:58.420: ",000 hundred"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:09.760 | reina civosa | Rana sevosa |
| 0:00:15.480 | of | (nothing) |
| 0:00:20.600 | 3 | three |
| 0:00:35.880 | forests | forest |
| 0:00:49.160 | habitat | habitats |
| 0:01:17.020 | unquote, | (nothing) |
| 0:01:34.180 | end quote. | (nothing) |
| 0:02:54.920 | that | their |
| 0:05:49.760 | with that | without |
| 0:06:28.900 | the | (nothing) |
| 0:07:48.560 | Kavanaugh | Kavanagh |
