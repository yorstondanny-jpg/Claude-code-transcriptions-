# granholm-wine: Supreme Court No. 03-1116

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-1116/20041207a_03-1116.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2004/03-1116.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 18 min on 4 CPU cores
- Audio length: 1:01:00.539 (3660.539 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.3 MB
- Official words: 10384 (plus 15 `(Laughter.)` markers), in 369 speaker turns
- ASR words: 10363
- Official words matched to an ASR word: 9558 of 10384 (**92.05%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.05% (threshold 85%).

352 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 20 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 03-1116 2004 granholm-wine --model small.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2004/03-1116.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-1116/20041207a_03-1116.delivery.mp3

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-50.3 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:21:28.060 | 1288.060 | big | 3.76 | 3.60 | 28.1 | 35.0 | our clients want to -- want to pay taxes, want to sign up for permits, want to play on a -- Well -- -- level playing field -- -- well, they do today, I'm sure, but -- |
| 2 | 0:21:52.640 | 1312.640 | under speech | 0.00 | 0.00 | - | - | of out-of-state wineries. It requires that they keep and supply sales records on a monthly basis, that they keep those records for three years -- Maybe we're getting ripped off. I -- |
| 3 | 0:25:53.260 | 1553.260 | under speech | 0.00 | 0.00 | - | - | a showing that you say is virtually impossible to make. Your Honor, that's not before, and if there were other reasons -- No, but I think it is -- -- the state could -- |
| 4 | 0:28:05.100 | 1685.100 | under speech | 0.00 | 0.00 | - | - | reading of the case. Now -- I disagree that that is a necessary reading -- And I know it -- -- of the case. -- involved pineapple wine and all that. I know that, but -- |
| 5 | 0:28:59.820 | 1739.820 | under speech | 0.00 | 0.00 | - | - | prevail in this case without overruling Bacchus, but we have suggested that -- Well, why don't you focus on that? Because it's a little hard to plan on overruling that case. |
| 6 | 0:36:17.660 | 2177.660 | under speech | 0.00 | 0.00 | - | - | if we find that material sustains your burden, that's fine, you win; and if it doesn't, you lose. I don't know why we have to let you go back and -- |
| 7 | 0:37:48.700 | 2268.700 | under speech | 0.00 | 0.00 | - | - | So she says, "Put those three things together, and we win." That's her point. Now, what's your response? We disagree with that entire position. The text -- I know you do. |
| 8 | 0:40:56.400 | 2456.400 | small | 1.02 | 0.05 | 8.1 | 16.9 | make of that. I -- as I indicated, I don't believe Bacchus overrules those cases; it didn't even cite most of those cases. But -- Well, the dissent seemed to think so -- |
| 9 | 0:43:13.880 | 2593.880 | under speech | 0.00 | 0.00 | - | - | that question really isn't presented here, because -- But could Congress pass a law forbidding it? That's a difficult question, because -- Yeah. All right. But I need an answer to it. |
| 10 | 0:54:31.200 | 3271.200 | medium | 0.74 | 0.60 | 16.7 | 18.7 | states have, in fact, joined New York and Michigan in asking the Court not to -- States don't like federal regulation -- -- restrict that. -- of any sort, of course. I know that. |
| 11 | 0:57:51.540 | 3471.540 | big | 3.02 | 1.25 | 20.5 | 31.2 | federal courts. And, of course, the federal agency, the Tax and Trade Bureau, can revoke a permit if state law is violated. In the -- Who's going to count the bottles? |
| 12 | 0:58:19.980 | 3499.980 | small | 1.04 | 0.10 | 11.3 | 20.7 | "What enforcement by -- is done of in-state wineries." In that regard, the answer was, "None." How do you count bottles? I would have thought the consumers have all the bottles. |
| 13 | 0:58:31.900 | 3511.900 | under speech | 0.00 | 0.00 | - | - | have all the bottles. That's exactly right. And, certainly in the directly shipping context in-state, that is emphatically the case. I think they were referring to full bottles. I guess -- |
| 14 | 0:58:34.218 | 3514.218 | under speech | 0.00 | 0.00 | - | - | And, certainly in the directly shipping context in-state, that is emphatically the case. I think they were referring to full bottles. I guess -- With direct shipping -- They've all been drinking -- |
| 15 | 0:59:43.080 | 3583.080 | big | 5.26 | 4.95 | 29.8 | 38.7 | all 50 states and open offices in order to do this -- if you could drive out to Middleburg and visit Juanita Swedenburg's winery -- and she invites you to do so -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.560 to 0:03:09.560, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.560] MR. BOLICK: Justice Stevens, and may it please the Court: For 124 years, as state power over alcohol has ebbed and flowed, one principle has remained virtually constant, that states may regulate alcohol by one set of rules, not by two. New York and Michigan consigned out- of-state wine, and only out-of-state wine, to the three- tier system for closing the market to thousands of small family-run wineries and their customers for the benefit of a liquor distributor oligopoly. Discrimination is the core concern of the Commerce Clause, and it sends a powerful signal that the state is engaged, not in legitimate regulation, but in economic protectionism. The states and the liquor distributors make a sweeping argument that this Court has consistently rejected, that the Twenty-First Amendment creates plenary state authority.

[0:01:06.440] JUSTICE KENNEDY: Well, under your view, could the three-tier system, itself, be challenged by a New Jersey wholesaler wanting to sell in New York, or a New York wholesaler wanting to sell in New Jersey?

[0:01:19.380] MR. BOLICK: Yes, Justice Kennedy.

[0:01:20.540] JUSTICE KENNEDY: So, under your view, the whole three-tier system has to go down?

[0:01:24.100] MR. BOLICK: No, Justice Kennedy. So long as the state does not discriminate against out-of-state entities, it is free to, as this Court --

[0:01:33.120] JUSTICE KENNEDY: Well, under my hypothetical. I don't know exactly how -- the way it works, you have to be a New York wholesaler to sell to a New York retailer. Under your view, a New Jersey wholesaler could sell to a New York retailer.

[0:01:44.240] MR. BOLICK: That is -- or a challenge, as you ask the question, Justice Kennedy, could be mounted to that, under the same theory that we're advocating here. The state may have a different set of defenses that it doesn't have here. But --

[0:01:57.980] JUSTICE KENNEDY: But so far as -- the rationale is the same.

[0:02:00.540] MR. BOLICK: The --

[0:02:00.740] JUSTICE KENNEDY: It seems to me that, under your rationale, that that in-state licensing system has to fall if there's a New Jersey wholesaler.

[0:02:09.020] MR. BOLICK: It has to pass constitutional muster.

[0:02:11.260] JUSTICE BREYER: And when you say there is no precedent -- I mean, I think a much more modest claim than you're making, the claim simply that a state cannot discriminate against out-of-state liquor -- i.e., the physical liquid -- which is really more modest and keeps the three-tier effect -- now, your -- that claim, that they couldn't do that, was really what was advanced in Young's Market. I read the briefs in that case. The briefs presented that Court -- you could have written those briefs. And the difficulty for you is, it articulated that more modest version very clearly, made a tremendously strong case, that was not forbidden by Section 2 of the Twenty-First Amendment. And this Court squarely rejected it.

[0:02:57.380] MR. BOLICK: Your Honor, Young's Market -- the result in Young's Market was correct --

[0:03:00.740] JUSTICE BREYER: The result, I understand, you could put on the basis of there being no discrimination.

[0:03:05.760] MR. BOLICK: Exactly.

[0:03:06.620] JUSTICE BREYER: Reading Justice Brandeis' opinion, I
