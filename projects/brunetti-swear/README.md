# brunetti-swear: Supreme Court No. 18-302

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/18-302
- Audio: https://www.supremecourt.gov/media/audio/mp3files/18-302.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/18-302_5426.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 62 min on 4 CPU cores
- Audio length: 0:13:06.402 (786.402 s)
- `audio/argument.mp3`: mono, 64 kbps, 26.9 MB
- Official words: 9322 (plus 2 `(Laughter.)` markers), in 259 speaker turns
- ASR words: 8908
- Official words matched to an ASR word: 8733 of 9322 (**93.68%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.68% (threshold 85%).

344 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 13 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 18-302 2018 brunetti-swear --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.0 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:16:58.820 | 1018.820 | medium | 1.50 | 0.75 | 28.4 | 39.9 | in order to determine is that mark intended -- will it be -- I don't want to -- I don't want to go through the examples. I really don't want to do that. |
| 2 | 0:38:35.100 | 2315.100 | under speech | 0.00 | 0.00 | - | - | and say, well, look at that, and then, you know, they're going to see the little trademark thing and say, well, it's registered trademark. Well, they won't say that, but -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.580 to 0:03:06.580, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.580] MR. STEWART: Thank you, Mr. Chief Justice, and may it please the Court: The Lanham Act's ban on federal registration of scandalous trademarks is not a restriction on speech but a valid condition on participation in a federal program. On its face, and as applied here, the provision is -- is viewpoint-neutral. The scandalous marks provision is one of many content-based criteria for federal trademark registration, and consideration of a mark's content is essential --

[0:00:31.880] JUSTICE SOTOMAYOR: Could you please tell me how you're defining "scandalous mark"? From your brief, I thought you were giving it a different definition than has been used by the agency for a while.

[0:00:43.400] MR. STEWART: Well, the -- the term -- the adjectives that have sometimes been used as synonyms for "scandalous" by the agency are terms like "shocking," "disgraceful," "offensive," and "disreputable." I think one --

[0:00:54.900] JUSTICE SOTOMAYOR: Well, if you use all those adjectives, you run head-on to Tam.

[0:00:59.120] MR. STEWART: I think one sense in which we have -- the -- I think this has always been at the core of the prohibition, but I think Tam has led us to focus more on limiting the scope of those adjectives. That is, on their face, those adjectives could encompass material that is offensive or shocking because of the outrageous views that it expresses. And we know from Tam that that's --

[0:01:21.860] JUSTICE SOTOMAYOR: But that's viewpoint discrimination.

[0:01:21.860] MR. STEWART: That's viewpoint discrimination. It's not a valid basis for denial of federal registration of a trademark. So I think it has always been the PTO's focus, but, from here on, I believe it will be the exclusive focus on marks that are shocking, offensive -- or offensive because of the mode of expression, not because of the ideas --

[0:01:39.460] JUSTICE GINSBURG: How is -- how is that determined, that a substantial composite of the general public would find the -- the mark shocking or offensive? I mean, if -- considering what's involved in this case, if you were to take a -- a composite of, say, 20-year-olds, do you think that that answer would be they would find it shocking?

[0:02:03.540] MR. STEWART: I -- I think not -- I think there are certainly some segments of society that are more likely to find particular marks shocking than others. I -- the -- the PTO, it -- its initial determination was that this mark would be perceived by a substantial segment of the public as the equivalent of the profane past participle form of a well-known word of profanity and perhaps the paradigmatic word of profanity in our language.

[0:02:32.200] JUSTICE SOTOMAYOR: So why are you using a subjective standard? Why not just something like obscene, vulgar, even profane? But, once you get to shockingly offensive, you get to viewpoint. One way or another, it's always subjective. I -- I -- I -- I can deal with a limiting principle that has its own substance, like obscenity.

[0:02:58.620] MR. STEWART: I -- I would agree that if you just looked at the words like "shocking" and "offensive" on their face and gave them their ordinary

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 24, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/18-302
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/18-302/18-302_20190624-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:53.538 (293.538 s)
- Words: 617, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 595 of Whisper's 617 words (96.4%; Oyez has 618).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.680 | 15 |
| JUSTICE KAGAN | 0:00:07.620 | 0:04:51.720 | 600 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kagan has the opinion of the Court this morning, Case 18-302, Jansu v. Brunetti.

[0:00:07.620] JUSTICE KAGAN: Kagan. The question in this case is whether a particular provision of the Federal trademark statute violates the First Amendment. A trademark, for anyone who doesn't know, is a brand name or a symbol or a saying or something of that kind that identifies a product. And if the trademark is registered with the U .S. Patent and Trademark Office, which I'll call the PTO for short, then the holder of the trademark gets certain legal benefits. But the trademark statute prohibits the PTO from registering certain kinds of trademarks. One of those prohibitions is what's at issue in this case. The statute says that the PTO can't register any immoral or scandalous trademarks. Today, we hold that provision to violate the First Amendment. The most fundamental principle of our free speech law is that the government can't penalize or disfavor or discriminate against expression based on the ideas and the viewpoints that it conveys. The ban on immoral or scandalous trademarks does just that. Trademarks are a kind of expression, and the statute's viewpoint discrimination is apparent from its very language. What does immoral mean? The dictionaries say, and you know this even without the dictionaries, that immoral means inconsistent with rectitude, purity, or good morals, violating principles of morality. And how about scandalous? Not really much different. According to the dictionary, something is scandalous when it gives offense to the conscience or moral feelings or when it's disgraceful or disreputable. So the immoral or scandalous bar allows trademark registration when a mark's message conforms with society's sense of decency and morality, but it prohibits registration of any mark expressing a contrary view when it goes against that societal sense of morality and rectitude. That's exactly the kind of discrimination against ideas that the First Amendment prohibits. Now, if that all sounds a little abstract, here are some examples that may make the point. The PTO rejected as immoral or scandalous trademarks for marijuana cola, and you can't spell health care without THC. Because, the PTO said, they glamorize drug use. But at the same time, the office allowed trademarks with sayings like, say no to drugs and dare to resist drugs.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:03.220 | (nothing) | in |
| 0:00:03.360 | 18 -302, Jansu | 18-302, Iancu |
| 0:00:07.620 | Kagan. | (nothing) |
| 0:00:29.980 | I'll | I will |
| 0:00:46.060 | what's | what is |
| 0:00:50.480 | can't | cannot |
| 0:01:06.640 | can't | cannot |
| 0:01:55.220 | it's | it is |
| 0:02:05.820 | society's sense | society since |
| 0:02:20.440 | That's | That is |
| 0:03:21.020 | express | expressed |
| 0:03:26.960 | doesn't | does not |
| 0:04:00.680 | can't | cannot |
| 0:04:02.180 | Congress's | Congress' |
