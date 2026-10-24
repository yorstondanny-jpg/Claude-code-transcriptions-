# warhol-prince: Supreme Court No. 21-869

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2022/21-869
- Audio: https://www.supremecourt.gov/media/audio/mp3files/21-869.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/21-869_986b.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 64 min on 4 CPU cores
- Audio length: 1:42:29.064 (6149.064 s)
- `audio/argument.mp3`: mono, 64 kbps, 49.2 MB
- Official words: 19768 (plus 16 `(Laughter.)` markers), in 391 speaker turns
- ASR words: 18966
- Official words matched to an ASR word: 18442 of 19768 (**93.29%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
  Not counted: `117` 5830.670-5833.870 (3.20 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 93.29% (threshold 85%).

813 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 24 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 21-869 2022 warhol-prince --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-45.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:32:51.210 | 1971.210 | under speech | 0.26 | 0.00 | 10.2 | 11.8 | is copyright. Yes. And I think that copyright's directly at issue in this case. The -- let's say that I'm both a Prince fan, which I was in the '80s, and -- |
| 2 | 0:32:52.290 | 1972.290 | big | 6.88 | 5.05 | 23.8 | 33.8 | Yes. And I think that copyright's directly at issue in this case. The -- let's say that I'm both a Prince fan, which I was in the '80s, and -- No longer? |
| 3 | 0:33:00.010 | 1980.010 | under speech | 0.00 | 0.00 | - | - | And I think that copyright's directly at issue in this case. The -- let's say that I'm both a Prince fan, which I was in the '80s, and -- No longer? Well -- |
| 4 | 0:33:04.250 | 1984.250 | big | 1.80 | 1.65 | 26.7 | 31.9 | directly at issue in this case. The -- let's say that I'm both a Prince fan, which I was in the '80s, and -- No longer? Well -- -- so only on Thursday nights. |
| 5 | 0:34:13.070 | 2053.070 | big | 1.30 | 1.15 | 26.6 | 33.3 | very unlikely if it was just one of you that -- that -- that anyone would see you. Oh, no, no. I -- I'm going to market it to all my Syracuse buddies. |
| 6 | 0:34:25.030 | 2065.030 | small | 0.44 | 0.30 | 31.2 | 33.1 | quite reasonably look at that and say that this is not the kind of -- of productive creativity promoting use that is -- is -- So, in other words, you would sue me? |
| 7 | 0:36:42.830 | 2202.830 | small | 0.52 | 0.00 | 0.5 | 3.1 | or message? Maybe. But I don't think that in that kind of hypothetical that that would win the day. Justice Sotomayor? I think my colleague, Justice Thomas, needs a lawyer. |
| 8 | 0:42:11.750 | 2531.750 | under speech | 0.00 | 0.00 | - | - | meaning or message, but I would have to -- The movie? -- but I would probably have to learn more and read the books and see the movies to give you a -- |
| 9 | 0:58:59.610 | 3539.610 | under speech | 0.00 | 0.00 | - | - | lithograph or any editing. I guarantee the air-brushed pictures of me look better than the real pictures of me, and they have a very different meaning and message to me. |
| 10 | 0:59:04.670 | 3544.670 | medium | 0.62 | 0.45 | 21.5 | 26.7 | me, and they have a very different meaning and message to me. What do you think -- Well, I think that's not right. I mean, I think you would look at -- |
| 11 | 1:00:23.950 | 3623.950 | under speech | 0.14 | 0.00 | - | - | hypothetical. Everything he said about Warhol versus a Goldsmith is the same article you could have said about the audiences that want to watch "Mork and Mindy" versus "Happy Days." |
| 12 | 1:31:39.590 | 5499.590 | under speech | 0.00 | 0.00 | - | - | a yes or a no if I can get one out of you. Can I say to -- yes to part of your question and explain why? Is that 109 okay? |
| 13 | 1:31:42.710 | 5502.710 | small | 0.34 | 0.20 | 25.7 | 28.7 | to -- yes to part of your question and explain why? Is that 109 okay? You -- you can do whatever you want. I was just hoping for a yes or no. |
| 14 | 1:34:45.170 | 5685.170 | under speech | 0.00 | 0.00 | - | - | or you could say just essential, and I think that covers it. But I think the 113 best way to explain what the -- Okay. Those are going to be in -- |
| 15 | 1:35:07.830 | 5707.830 | medium | 0.90 | 0.75 | 21.7 | 25.7 | side wins? If you're going for the straightforward clarity of a one-word answer, I would say essential. The reason we use -- No, you can use multiple words. What's the formulation? |
| 16 | 1:36:30.110 | 5790.110 | under speech | 0.00 | 0.00 | - | - | your considerations here is necessary or at least useful. That's how I would phrase it for your opinion. Very helpful, thank you. Justice Barrett? So you would leave out "essential"? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:10.200 to 0:03:10.200, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:10.200] MR. MARTINEZ: Mr. Chief Justice, and may it please the Court: Both courts below agreed and Goldsmith doesn't dispute that Warhol's Prince Series can reasonably be perceived to convey a fundamentally different meaning or message from Goldsmith's photograph. The question in this case is whether that different meaning or message should play a role, any role, in the fair use analysis. Our answer is yes. Warhol's transformative meaning puts points on the board under Factor 1 of the four-factor balancing test. Goldsmith and the Second Circuit say no. Warhol's new meaning is categorically irrelevant and can't be considered as part of Factor 1 or any other factor. I want to emphasize three points. First, the precedent supports us. Campbell unambiguously requires an examination of meaning or message. Google reaffirms that test and cites Warhol's Soup Cans as a paradigmatic example of when it's satisfied. Goldsmith's test is at odds with both cases. Second, our approach, unlike Goldsmith's, maintains a balance between protecting artists' rights to monetize their works and encouraging new and important follow-on expression. We give follow-on artists credit for innovation at Factor 1 while recognizing that Factor 4 and the other factors will sometimes cut decisively the other way. Goldsmith's necessity test, by contrast, upends that balance. It banishes transformative meaning from the equation altogether, and by doing so, it violates 107's text, contradicts precedent, and undermines copyright's key goal, promoting creativity for the public good. Finally, the stakes for artistic expression in this case are high. A ruling for Goldsmith would strip protection not just from this Prince Series but from countless works of modern and contemporary art. It would make it illegal for artists, museums, galleries, and collectors to display, sell, profit from, maybe even possess a significant quantity of works. It would also chill the creation of new art by established and up-and-coming artists alike. These results are repugnant to copyright and to the First Amendment. You should reject them. We ask you to reaffirm Campbell and reverse the decision below.

[0:02:23.480] JUSTICE THOMAS: Could you give us an example of any follow-on work that fails your test?

[0:02:29.780] MR. MARTINEZ: Sure. I think a classic example would be a -- a book-to-movie adaptation. I think that would be a follow-on work. It would be a derivative work. I think, if you -- if someone were to, you know, try to do that, I think that the -- the original creator, the author of the book, could very easily assert that that was not fair use and would have a -- a winning case under Factor 4 and probably also under Factor 1. And, certainly, that would be a -- a kind of classic example of a follow-on work that would not count.

[0:02:58.120] JUSTICE SOTOMAYOR: Why? I mean, derivative works are generally in a different medium, and almost all of them, even a dramatization on -- on theater or even

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 18, 2023.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2022/21-869
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2022/21-869/21-869_20230518-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 13.2 MB)
- Length: 0:10:56.640 (656.640 s)
- Words: 1365, transcribed by faster-whisper `small.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 1290 of Whisper's 1365 words (94.5%; Oyez has 1370).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:01.700 | 4 |
| JUSTICE SOTOMAYOR | 0:00:01.700 | 0:10:55.000 | 1358 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Sotomayor has the

[0:00:01.700] JUSTICE SOTOMAYOR: opinion of the court today in 201869, Andy Warhol Foundation v. Goldsmith. This copyright case involves not one but two artists. The first, Andy Warhol, is well known. Warhol's images of products like Campbell's soup cans and celebrities like Marilyn Monroe appear in museums around the world, at least to people close to my age. The second, Lynn Goldsmith, is less well known, but she too is successful in her field. Goldsmith is a professional photographer. She specializes in concert and portrait photography of rock and roll musicians, and she commonly licenses her photographs to magazines and other publications. Goldsmith has captured some of the 20th century's greatest rock stars, Bob Dylan, Mick Jagger, Patty Smith, Bruce Springsteen, and as relevant here, Prince. In 1984, Vanity Fair sought to license one of Goldsmith's copyright photographs of Prince to use as an artist's reference for an illustration in its magazine. Goldsmith agreed on the condition that they used be for one time only. Vanity Fair hired Andy Warhol as the artist to create the illustration. Warhol made a purple silk screen portrait of Prince using Goldsmith's photography, and Vanity Fair published the purple prints alongside an article about Prince. Vanity Fair credited Smith for the source photograph and paid her $400. Warhol, however, did not stop with the Vanity Fair illustration. He derived 15 additional works from Goldsmith's photograph, now known as the Prince Series. Goldsmith did not know about the Prince Series until decades later, when she saw an orange silk screen portrait of Prince on the cover of a magazine published by Conde Nast. Conde Nast's parent company is Vanity Fair. The year was 2016 and Prince had just died. Conde Nast wanted to publish a special tribute to the musician. A contacted Warhol's successor and interest, the Andy Warhol Foundation for the Visual Arts Inc., about the possibility of reusing Vanity Fair's purple prints. After the foundation informed Conde Nast about the other Prince Series images, however, Conde Nast opted to use orange prints instead. It paid the Warhol Foundation $10,000 to do so.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.940 | 201869, | 21-869, Andy Warhol Foundation v. Goldsmith. Justice Sotomayor has the opinion of the Court today in 21-869, |
| 0:00:37.780 | is | was |
| 0:01:01.880 | Patty | Patti |
| 0:01:14.940 | artist's | artist |
| 0:01:21.840 | they used | the use |
| 0:01:41.600 | prints | Prince |
| 0:02:16.160 | Conde | Cond� |
| 0:02:17.520 | Conde | Cond� |
| 0:02:27.660 | Conde | Cond� |
| 0:02:32.000 | A | It |
| 0:02:32.880 | Warhol's | Warhol |
| 0:02:33.980 | and | in |
| 0:02:43.240 | prints. | Prince. |
| 0:02:46.800 | Conde | Cond� |
| 0:02:51.480 | Conde | Cond� |
| 0:02:53.840 | prints | Prince |
| 0:03:09.840 | Conde | Cond� |
| 0:03:14.000 | recognized | recognize |
| 0:03:18.320 | prints, | prince, |
| 0:03:21.460 | the | to |
| 0:03:23.520 | does | is |
| 0:03:24.080 | alter it. | altered. |
| 0:03:53.560 | uses | use is |
| 0:03:55.600 | close quote. Ways | weighs |
| 0:03:58.220 | Warhol | Warhol's |
| 0:04:01.660 | Conde | Cond� |
| 0:04:32.420 | supplanting | some planting |
| 0:04:35.000 | adds | add |
| 0:04:47.140 | comping | copying |
| 0:04:55.400 | asks | asked |
| 0:05:52.240 | therefore, | there for |
| 0:06:15.180 | It | (nothing) |
| 0:06:23.200 | copyright at | copyrighted |
| 0:06:40.620 | prints | Prince |
| 0:06:41.360 | Conde | Cond� |
| 0:06:50.480 | print | Prince |
| 0:07:00.020 | prints | Prince |
| 0:07:00.840 | Conde | Cond� |
| 0:07:02.640 | share, | (nothing) |
| 0:07:09.460 | prints | Prince |
| 0:07:11.220 | prints | Prince |
| 0:07:13.560 | prints. | Prince. |
| 0:07:35.040 | is | weighs |
| 0:08:17.280 | A. Cuffe Rose | Acuff-Rose |
| 0:08:22.940 | Two | 2 |
| 0:08:25.940 | Orbison's | Orbison |
| 0:08:29.280 | Two | 2 |
| 0:08:49.600 | (nothing) | for |
| 0:08:54.620 | Two | 2 |
| 0:09:59.260 | Rain | Reign |
| 0:10:10.800 | Alice's | Alice |
| 0:10:35.520 | uses | use is |
