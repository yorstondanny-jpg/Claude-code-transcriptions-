# needle-caps: Supreme Court No. 08-661

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-661/20100113a_08-661.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2009/08-661.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 60 min on 4 CPU cores
- Audio length: 1:11:18.152 (4278.152 s)
- `audio/argument.mp3`: mono, 64 kbps, 34.3 MB
- Official words: 11924 (plus 8 `(Laughter.)` markers), in 261 speaker turns
- ASR words: 11579
- Official words matched to an ASR word: 11060 of 11924 (**92.75%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "know," 4009.090-4013.770. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
- PASS: match rate over 85%. 92.75% (threshold 85%).

470 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 19 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 08-661 2009 needle-caps --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2009/08-661.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-661/20100113a_08-661.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:10:53.530 | 653.530 | under speech | 0.00 | 0.00 | - | - | a particular -- a single entity’s articulation of rules. Well, Mr. Chief Justice, you are exactly right, and the real -- That you have been begging the question? Is that -- that part? |
| 2 | 0:15:11.610 | 911.610 | under speech | 0.00 | 0.00 | - | - | you want the Patriots to sell T-shirts in competition with the Saints, or whoever. The Red Sox. All right. You see the point? The Red Sox -- I know baseball better. |
| 3 | 0:15:25.070 | 925.070 | medium | 1.04 | 0.90 | 26.9 | 30.7 | the Yankees; is that right? The ability to compete. Yes. Yes. Okay. I don't know a Red Sox fan who would take a Yankees sweatshirt if you gave it away. |
| 4 | 0:16:10.410 | 970.410 | big | 2.20 | 1.80 | 27.4 | 34.7 | fan and easily be persuaded to be a Red Sox fan, but the person who is 3 years old can easily be persuaded. They have very small allowances, the 3-year-olds. |
| 5 | 0:17:29.110 | 1049.110 | under speech | 0.00 | 0.00 | - | - | that was the only issue. That is the only issue, Justice Scalia. Well, why am I worrying about this other stuff? Because counsel has an obligation to respond to questions. |
| 6 | 0:17:44.990 | 1064.990 | medium | 2.32 | 2.00 | 19.0 | 24.5 | blocker. -- to think about the case if I know what's going on. And I'm not certain this is irrelevant, but given Justice Scalia's persuasive remark, I will withdraw my question. |
| 7 | 0:45:57.170 | 2757.170 | medium | 1.84 | 1.55 | 19.5 | 27.6 | talking about T-shirts and helmets, and I -- I thought it's the simplest thing in the world. You pick up the phone and say: Hello, Shanghai, do you have a helmet? |
| 8 | 1:06:48.370 | 4008.370 | under speech | 0.00 | 0.00 | - | - | even ask the question whether under the rule of reason such a thing is reasonable or justified? Your Honor -- I thought I was reducing it to the absurd. But you -- |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.360 to 0:03:07.360, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.360] MR. NAGER: Thank you, Mr. Chief Justice, and may it please the Court: In this case, the Court of Appeals for the Seventh Circuit held that an agreement of the 32 teams of the National Football League was immune from any scrutiny under section 1 of the Sherman Act on the ground that the agreement allegedly fails the plurality of actor requirement of this Court's jurisprudence. The 32 teams of the National Football League are separately owned and controlled profit-making enterprises. Under this Court's decision in NCAA, as well as the Court's more general joint venture jurisprudence, those clubs are entities whose distinct agreements are, indeed, subject to section 1 scrutiny. The fact of the matter is there is a long- standing consensus, judicial and legislative, that agreements among sports teams about whether and how they will participate in the marketplace is subject to scrutiny under the Sherman Act, section 1. The Court's decision in NCAA is most directly on point. In that case, the Court held that a policy of the NCAA that restricted the ability of member institutions of the NCAA to sell TV rights violated section 1. Just as with the NFL, the decisions of the NCAA were ultimately controlled by the vote of its members, and for that reason, the Court held that the NCAA policy was a horizontal restraint, and it --

[0:01:34.453] JUSTICE SOTOMAYOR: But there was no joint venture with respect to the television rights, meaning there was no separate activity, other than the televising of the shows at issue. Here, the Solicitor General is saying there is a joint venture, and it has to do with the licensing of trademarks, with their quality control, et cetera. Isn't that a substantial difference?

[0:02:00.030] MR. NAGER: No, I don't -- I don't think so, because what we’re -- what we’re asking about here is -- is the question of whether or not the agreement of the teams involves a plurality of actors. And just as in NCAA, the members' institutions -- because they controlled the operation of the NCAA and the policy that it was promulgating, there was a plurality of actors. So, too, here, the 32 teams of the National Football League have entered into an agreement and control the use, collectively, of the trademarks and logos of the individual teams. And for that reason, there is concerted activity that is involved. Justice Sotomayor, the point that you raise might be of -- a point of difference that the NFL could argue in the context of an ancillary restraint analysis, in the context of a rule of reason analysis, but it’s not a point of distinction that they can argue properly in the context of the concerted conduct inquiry. The NCAA case simply applies the consistent teachings of this Court in cases like Sealy, BMI, and Copperweld,

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 24, 2010.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2009/08-661
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/08-661/20100524o_08-661.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 0.7 MB)
- Length: 0:02:19.337 (139.337 s)
- Words: 273, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 268 of Whisper's 273 words (98.2%; Oyez has 278).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.420 | 16 |
| JUSTICE STEVENS | 0:00:07.880 | 0:02:18.400 | 256 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Stevens has our opinion this morning, case 08661, American Needle v. The National Football League.

[0:00:07.880] JUSTICE STEVENS: The Washington Redskins football team has its own trade name and trademarks as do each of the 31 other teams in the National Football League. Since 1963, however, all 32 teams have used a jointly owned corporation, National Football League Properties, NFLP, to market their intellectual property. For almost 40 years, NFLP granted non-exclusive licenses to a number of different vendors, one of which was the petitioner in this case, American Needle. In 2000, however, the teams authorized NFLP to grant exclusive licenses, which it did. Because they declined to renew petitioner's license, it brought this action against the teams and NFLP seeking treble damages under the Sherman Act. The district court granted summary judgment to the defendants, holding in effect that the defendants constituted a single economic enterprise incapable of conspiring with itself. The court of appeals affirmed. We granted certiorari and now reverse. We do not reach the question whether petitioner has alleged a violation of the Sherman Act, but we reject the argument that the 32 teams constitute a single entity for antitrust purposes. For reasons stated in an opinion filed with the clerk, we hold that their conduct must be judged under the rule of reason. Our opinion is unanimous. I also have the disposition to announce in number 086261 Robertson v. Watson. The writ of certiorari is dismissed as improvidently granted. The Chief Justice has written a dissent in which Justices Scalia, Kennedy, and Sotomayor have joined. Justice Sotomayor has also filed a brief dissenting statement that Justice Kennedy has joined.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:01.580 | (nothing) | in |
| 0:00:13.860 | (nothing) | as to each |
| 0:00:51.100 | (nothing) | a |
| 0:01:58.400 | v. | against |
| 0:02:03.320 | (nothing) | an |
| 0:02:10.900 | have | had |
