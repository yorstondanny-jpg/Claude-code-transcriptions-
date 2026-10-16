# schein-martian: Supreme Court No. 17-1272

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/17-1272
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-1272.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-1272_nd89.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 56 min on 4 CPU cores
- Audio length: 0:58:50.928 (3530.928 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.2 MB
- Official words: 10504 (plus 5 `(Laughter.)` markers), in 262 speaker turns
- ASR words: 10193
- Official words matched to an ASR word: 9874 of 10504 (**94.00%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.00% (threshold 85%).

333 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 3 times. ASR words with no official counterpart
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

    python3 transcribe.py 17-1272 2018 schein-martian --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.2 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:18:09.540 | 1089.540 | under speech | 0.00 | 0.00 | - | - | Okay. Now suppose it's really weird. I mean, you want to say no exception at all? He says, my claim here is a Martian told me to do it. Okay? |
| 2 | 0:35:08.960 | 2108.960 | under speech | 0.00 | 0.00 | - | - | standard points to. But -- but what does even that mean? Clearly, there's a bona fide dispute when two parties are litigating all the way to the United States Supreme Court. |
| 3 | 0:36:24.120 | 2184.120 | under speech | 0.12 | 0.00 | - | - | answer the question presented -- Oh, no. -- and you give up and go back to the court of appeals on the first one? Absolutely not, Your Honor. I didn't think so. |
| 4 | 0:42:06.600 | 2526.600 | under speech | 0.00 | 0.00 | - | - | is doing. And we would warmly -- It's pretty theoretical. And that's an argument. We -- we would warmly invite a DIG if the Court would like to -- to DIG the case. |
| 5 | 0:53:12.810 | 3192.810 | under speech | 0.00 | 0.00 | - | - | saying that in this case it -- it is highly unlikely to have any effect on the ultimate outcome. Well, that's only because you intend to win all the other questions. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.080 to 0:03:08.080, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.080] MR. SHANMUGAM: Thank you, Mr. Chief Justice, and may it please the Court: The Federal Arbitration Act requires courts to enforce arbitration agreements according to their terms. This case involves a straightforward application of that principle in the context of arbitrability, specifically where the parties have agreed to delegate to the arbitrator the authority to decide whether claims are subject to arbitration. Where the parties have so agreed, the Arbitration Act requires a court to honor that agreement. A court does not have the power to decide the issue of arbitrability for itself and to short-circuit the arbitrator's ability to do so.

[0:00:45.120] JUSTICE GINSBURG: Mr. Shanmugam, can we back up and have you explain why we even get to a question, the question presented, because Schein has no arbitration agreement with Archer, so how -- what is this agreement? It's not between Archer and Schein. How does Schein get to claim the benefit of an agreement Schein did not make?

[0:01:14.380] MR. SHANMUGAM: Justice Ginsburg, there is a question in the case concerning non-parties. The agreements in question are agreements with some of the defendants, not all of them. And so, therefore, as to the non-signatory defendants, there is a question reserved by the court of appeals about the doctrine of equitable estoppel, and that would be an issue for the court of appeals to address on remand if this Court agrees with us on the question presented. That is obviously a discrete issue, not reached by the court of appeals in the decision below, and, again, an issue that would be open on remand. But, on the question presented, I think our submission is quite straightforward. The "wholly groundless" exception on which the court of appeals relied has no footing in the text of the Arbitration Act. Where the parties have agreed to delegate the issue of arbitrability to the arbitrator, the merits of that issue are for the arbitrator and wholly for the arbitrator to decide. Sections 2, 3, and 4 of the Arbitration Act all point in the same direction: Where you have a valid delegation, that is treated, as this Court has indicated, like an antecedent agreement to arbitrate, and all there is for a court to do is to determine, first, that that provision is itself valid and, second, to determine whether the opposing party is, in fact, resisting the enforcement of that provision.

[0:02:43.120] JUSTICE ALITO: How do we take this --

[0:02:43.120] CHIEF JUSTICE ROBERTS: I'm not sure your answer to Justice Ginsburg is totally responsive. The -- the question of whether or not there is a valid arbitration agreement between the parties is antecedent to an order compelling arbitration. The court makes that decision. And I wonder why this isn't a -- a similar question. I mean, your friend on the other side makes the argument that, well, parties would not have agreed to

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 08, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/17-1272
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/17-1272/17-1272_20190108-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.3 MB)
- Length: 0:05:20.810 (320.810 s)
- Words: 769, transcribed by faster-whisper `small.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 1 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: "court." 135.260-138.560.
- Cross-check: Oyez's unofficial transcript agrees with 750 of Whisper's 769 words (97.5%; Oyez has 771).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.960 | 0:00:10.460 | 19 |
| JUSTICE KAVANAUGH | 0:00:12.040 | 0:05:19.210 | 745 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.960 to 0:03:00.960, with each speaker's start time.

[0:00:00.960] CHIEF JUSTICE ROBERTS: In case number 17-1272, Henry Schein v. Archer and White-Sales, Inc., Justice Kavanaugh has the opinion of the Court.

[0:00:12.040] JUSTICE KAVANAUGH: This is a case about arbitration. In 1925, Congress passed and President Coolidge signed the Federal Arbitration Act. Under the act, arbitration is a matter of contract, and courts must enforce arbitration contracts according to their terms. Applying the act, we have held that parties may agree to have an arbitrator decide not only the merits of a particular dispute, but also gateway questions of arbitrability, such as whether the parties' agreement covers a particular controversy. Even when the parties' contract delegates the threshold arbitrability question to an arbitrator, the Fifth Circuit, in this case, and some other courts of appeals, have determined that the court, rather than an arbitrator, should decide the threshold arbitrability question if, under the contract, the argument for arbitration is wholly groundless. Those courts have reasoned that the wholly groundless exception enables courts to block frivolous attempts to transfer disputes from the court system to arbitration. The question here is whether the wholly groundless exception is consistent with the text of the act and with our precedent. We conclude that it is not. We must interpret the act as written, and the act, in turn, requires that we interpret the contract as written. When the parties' contract delegates the arbitrability question to an arbitrator, a court may not override the contract. In those circumstances, a court possesses no power to decide the arbitrability issue. That conclusion follows not only from the text of the act, but also from precedent. We have held that a court may not rule on the potential merits of the underlying claim that is assigned by contract to an arbitrator, even if the claim appears to the court to be frivolous. That principle applies with equal force to the court. A court may not decide a merits question that the parties have delegated to an arbitrator. A court may not decide an arbitrability question that the parties have delegated to an arbitrator. In an attempt to overcome the statutory text in this court's cases, the party opposing arbitration here, a business known as Archer and White, advances several arguments. In cases like this, as Archer and White sees it, the arbitrator will inevitably conclude that the dispute is not subject to arbitration, and then send the case back to the district court. So why waste the time and money? The short answer is that the act contains no wholly groundless exception, and we

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:05.960 | and | & |
| 0:00:12.360 | a | the |
| 0:02:15.260 | court. | threshold issue of arbitrability. Just as |
| 0:02:38.760 | and | & |
| 0:02:43.620 | and | & |
| 0:03:07.500 | and | & |
| 0:03:17.720 | and | & |
| 0:03:42.900 | and | & |
| 0:04:35.760 | party's | parties' |
| 0:05:06.770 | and | & |
