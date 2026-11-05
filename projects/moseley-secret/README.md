# moseley-secret: Supreme Court No. 01-1015

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2002/01-1015/20021112a_01-1015.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2002/01-1015.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 51 min on 4 CPU cores
- Audio length: 1:02:24.366 (3744.366 s)
- `audio/argument.mp3`: mono, 64 kbps, 30.0 MB
- Official words: 9030 (plus 16 `(Laughter.)` markers), in 284 speaker turns
- ASR words: 8997
- Official words matched to an ASR word: 8607 of 9030 (**95.32%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.32% (threshold 85%).

249 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 25 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 01-1015 2002 moseley-secret --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2002/01-1015.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2002/01-1015/20021112a_01-1015.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-55.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:01:41.120 | 101.120 | under speech | 0.00 | 0.00 | - | - | remote reaches of the economy that was nevertheless enjoined under the FTDA, and demonstrates the dangers of an unchecked FTDA. You mean Tennessee is remote, or this particular business is? |
| 2 | 0:01:48.360 | 108.360 | medium | 2.06 | 1.15 | 15.7 | 23.9 | remote, or this particular business is? Kentucky. Your Honor, this case actually came from Kentucky, and -- Oh, well, Kentucky -- -- I suppose that's even more remote than Tennessee in some cases. |
| 3 | 0:02:01.813 | 121.813 | under speech | 0.00 | 0.00 | - | - | there a Victoria's Secret in this town? There was not at the beginning of this case. The closest one was 60 miles away. We say that the result -- In Tennessee? |
| 4 | 0:03:44.320 | 224.320 | under speech | 0.00 | 0.00 | - | - | a funny example, but it comes from an actual case, and they decide to call themselves Bugwiser Bug Spray, and their slogan is, Where there's life, there's bugs, all right. |
| 5 | 0:19:10.860 | 1150.860 | medium | 2.20 | 1.50 | 15.3 | 21.2 | as whether or not the new entrant had to get permission from the famous mark in order to market this product. Well, that -- most consumers wouldn't even understand that question. |
| 6 | 0:19:18.140 | 1158.140 | big | 2.16 | 2.05 | 27.7 | 33.0 | order to market this product. Well, that -- most consumers wouldn't even understand that question. And that's -- that's part of our point, Your Honor. If -- This sounds like a lawyer's dream. |
| 7 | 0:20:53.240 | 1253.240 | under speech | 0.00 | 0.00 | - | - | off what people can say in commercial contexts. Now, you don't make much a point of that, so don't let me put words in your mouth. Explain it to me. |
| 8 | 0:24:12.360 | 1452.360 | big | 5.50 | 5.35 | 36.6 | 47.1 | years of quality advocacy and dedicated service in the Solicitor's Office -- Solicitor General's Office -- on behalf of the United States. That doesn't mean we're going to rule in your favor. |
| 9 | 0:38:31.420 | 2311.420 | under speech | 0.00 | 0.00 | - | - | far behind understanding you that I don't know whether you have just asserted that that's obviously bad. I think you have. Tiffany's Restaurant is bad. Yes. Okay. I have, and -- |
| 10 | 0:39:49.500 | 2389.500 | under speech | 0.04 | 0.00 | - | - | Tiffany's Restaurant, then you can also have a Tiffany Shoe Store, a Tiffany Pet Store. Very soon Tiffany's no longer -- Where will it all end? Where will it all end? |
| 11 | 0:42:19.380 | 2539.380 | under speech | 0.14 | 0.00 | - | - | something important. It conveys something that consumers -- it signals to consumers. Rolls-Royce is very careful about what products it allows to -- Chevrolet doesn't matter. You can use Chevrolet, because that's -- |
| 12 | 0:42:24.500 | 2544.500 | under speech | 0.00 | 0.00 | - | - | signals to consumers. Rolls-Royce is very careful about what products it allows to -- Chevrolet doesn't matter. You can use Chevrolet, because that's -- Is that right? Or Edsel, even easier -- yes. |
| 13 | 0:44:17.500 | 2657.500 | under speech | 0.02 | 0.00 | - | - | Yes. That's just a -- you know, it's an ordinary product. How can you have an absolutely wonderful toothpaste? Oh, no, you can. You can. There's no Tiffany of toothpastes, right? |
| 14 | 0:48:06.380 | 2886.380 | under speech | 0.10 | 0.00 | - | - | distributed in Elizabethtown. The suggestion is there are some -- 39,000 in Elizabethtown? Yes. There are 39,000 Victoria's Secret catalogues distributed in Elizabethtown, Kentucky in 1998. What's the population of Elizabethtown? |
| 15 | 0:48:13.100 | 2893.100 | big | 3.60 | 3.45 | 26.8 | 35.7 | in Elizabethtown, Kentucky in 1998. What's the population of Elizabethtown? That is a good question, but I -- four, he says, but I think that's his guess. We don't know. I -- |
| 16 | 0:49:30.340 | 2970.340 | big | 1.20 | 1.05 | 29.5 | 33.2 | in and show that? You're confusing the marks. Now, why -- I understand you're confusing the marks. No, you're not confusing the marks. No. I'm -- he's saying I'm confusing the marks. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:54.600 to 0:03:54.600, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:54.600] MR. HIGGINS: Mr. Chief Justice and may it please the Court, counsel: We are here today to obtain a construction of the Federal Trademark Dilution Act, FTDA, that will keep Federal trademark law in its proper bounds. We submit that can be accomplished by choosing objective proof over supposition and inference to guide future FTDA cases. This case from the Sixth Circuit involves a non-identical, non-confusing trademark operating in the remote reaches of the economy that was nevertheless enjoined under the FTDA, and demonstrates the dangers of an unchecked FTDA.

[0:01:37.860] QUESTION: You mean Tennessee is remote, or this particular business is? (Laughter.)

[0:01:41.120] QUESTION: Kentucky.

[0:01:42.320] MR. HIGGINS: Your Honor, this case actually came from Kentucky, and --

[0:01:45.180] QUESTION: Oh, well, Kentucky --

[0:01:45.180] MR. HIGGINS: -- I suppose that's even more remote than Tennessee in some cases. (Laughter.)

[0:01:50.420] QUESTION: Was there a Victoria's Secret in this town?

[0:01:53.040] MR. HIGGINS: There was not at the beginning of this case. The closest one was 60 miles away. We say that the result --

[0:02:00.280] QUESTION: In Tennessee? (Laughter.)

[0:02:01.813] MR. HIGGINS: We say that the result below is contrary to the actual words that Congress used in the FTDA, namely the plain words, causes dilution. If this result stands, the FTDA threatens to usher in an anti-competitive expansion of trademark law into patent- like realm. Perhaps the best example of that is the Second Circuit's Nabisco decision, urged in part here by respondents, which involved a goldfish-shaped cracker, and it -- the court there applied the FTDA to grant exclusionary rights in an unpatented, uncopyrighted design of a product to enjoin a product that they said diluted. That is contrary to this Court's two most recent decisions involving Federal trademark law, the Wal-Mart decision and the TrafFix Devices decision.

[0:03:08.080] QUESTION: Before you -- just would you spend one minute -- it would help me a lot if you explained to me what dilution is, and I'll be specific. It seems to me what you have here is a case of what's called tarnishment, and what tarnishment -- what I think of is this, is it like this, that -- that -- imagine some small shop wants to start a bug spray business. It's a funny example, but it comes from an actual case, and they decide to call themselves Bugwiser Bug Spray, and their slogan is, Where there's life, there's bugs, all right. (Laughter.)

[0:03:44.320] QUESTION: Now, Budweiser is not going to enter the bug spray business. Nobody thinks Budweiser, in fact, is

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 04, 2003.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2002/01-1015
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2002/01-1015/20030304o_01-1015.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.0 MB)
- Length: 0:03:39.899 (219.899 s)
- Words: 526, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 508 of Whisper's 526 words (96.6%; Oyez has 522).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| JUSTICE STEVENS | 0:00:00.000 | 0:03:39.360 | 525 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] JUSTICE STEVENS: The second case I have to announce is Mosley v. Victoria's Secret Catalog, No. 01-1015. In 1995, Congress amended Section 43 of the Trademark Act of 1946 to provide a remedy for the dilution of famous marks. That amendment, known as the Federal Trademark Dilution Act, describes the factors that determine whether a mark is distinctive and famous, and defines the term dilution as the lessening of the capacity of a famous mark to identify and distinguish goods or services. The question we granted certiorari to decide is whether objective proof of actual injury to the economic value of a famous mark, as opposed to a presumption of harm arising from a subjective likelihood of dilution standard, is a requisite for relief under the statute. Petitioners Victor and Kathy Mosley own and operate a retail store named Victor's Little Secret in a strip mall in Elizabethtown, Kentucky. They sell a variety of products, including women's lingerie and adult novelties. Respondents are affiliated corporations that own the Victoria's Secret trademark and operate over 750 Victoria's Secret stores, two of which are in Louisville, Kentucky, a short drive from Elizabethtown. In 1998, they spent over $55 million advertising lingerie bearing the Victoria's Secret trademark. They brought this action alleging that Petitioner's use of the name Victor's Little Secret in a store handling tawdry merchandise was likely to blur and erode the distinctiveness and tarnish the reputation of the Victoria's Secret trademark. The district court found that there was no likelihood of confusion between the marks, but held that the two marks were sufficiently similar to cause dilution and enjoined Petitioner from using the name Victor's Little Secret. The Court of Appeals affirmed, expressly disagreeing with a case decided by the Fourth Circuit involving Barnum and Bailey's claim that the use by the State of Utah of the phrase the, quote, greatest snow on earth on its license plates diluted the value of the phrase the greatest show on earth. The Fourth Circuit had held that the statute requires proof that the junior mark not only gave rise to a mental association with the senior mark, but also caused some actual harm to the famous mark's economic value. We granted certiorari to resolve the conflict. Our examination of the text of the statute convinces us that it does require proof of actual dilution rather than just the likelihood of dilution. In the language of the Act, there must be evidence of a, quote, lessening of the capacity of the mark to identify

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:03.280 | Mosley v. | Moseley against |
| 0:00:05.240 | Catalog, | Catalogue, |
| 0:00:11.900 | Section | Cection |
| 0:00:59.360 | Kathy Mosley | Cathy Moseley |
| 0:01:00.560 | and | an |
| 0:01:37.760 | that | the |
| 0:02:12.960 | and | & |
| 0:02:36.200 | caused | cause |
| 0:02:52.420 | the | a |
| 0:03:17.440 | necessarily | necesarrily |
