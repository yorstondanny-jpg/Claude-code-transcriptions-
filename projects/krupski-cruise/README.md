# krupski-cruise: Supreme Court No. 09-337

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/09-337/20100421a_09-337.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2009/09-337.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 64 min on 4 CPU cores
- Audio length: 0:55:15.096 (3315.096 s)
- `audio/argument.mp3`: mono, 64 kbps, 26.5 MB
- Official words: 8748 (plus 11 `(Laughter.)` markers), in 323 speaker turns
- ASR words: 8622
- Official words matched to an ASR word: 8086 of 8748 (**92.43%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 92.43% (threshold 85%).

271 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 2 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 30 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 09-337 2009 krupski-cruise --model medium.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2009/09-337.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/09-337/20100421a_09-337.delivery.mp3 --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-49.2 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:02:41.760 | 161.760 | big | 1.58 | 1.35 | 32.1 | 40.0 | name, probably -- Not just the real name. It's not that Jones pushed her, but his real name is Johnson. It's that Jones -- whoever pushed her; I forget -- but one guy -- |
| 2 | 0:21:37.000 | 1297.000 | small | 1.26 | 0.25 | 11.7 | 17.7 | you happen to know who the right party is? Correct. And -- Ever? Yes. Have you ever driven a car where your wife has said turn left and you’ve turned right? |
| 3 | 0:21:47.300 | 1307.300 | big | 1.42 | 1.25 | 22.3 | 28.0 | Has that ever happened to you? Yes. Was there anything you didn't know? What the facts are here, Your Honor -- No, I'm asking about this question, my hypothetical. You know -- |
| 4 | 0:22:05.560 | 1325.560 | big | 1.22 | 1.05 | 28.1 | 31.7 | being. There are millions of instances in which people do things by mistake where, in fact -- I think your wife made a mistake. I don't think you made a mistake. |
| 5 | 0:22:08.900 | 1328.900 | big | 2.26 | 2.15 | 31.1 | 37.8 | which people do things by mistake where, in fact -- I think your wife made a mistake. I don't think you made a mistake. No, my wife does not make mistakes. |
| 6 | 0:36:17.120 | 2177.120 | under speech | 0.00 | 0.00 | - | - | somewhere written in Blackstone, or maybe it's Lord Coke, I don't know, that says when you use the word "mistake" don't use it in English, use -- use it in Italian. |
| 7 | 0:37:14.600 | 2234.600 | under speech | 0.28 | 0.10 | 21.6 | 25.6 | to sue the company that could give you some money if they are liable? Or would you rather sue the Bank of America that has nothing to do with it? |
| 8 | 0:42:03.360 | 2523.360 | under speech | 0.00 | 0.00 | - | - | filed during the limitations period, and the lawyer -- the plaintiff's lawyer is a solo practitioner, and he or she is out of the office because the lawyer's on a cruise -- |
| 9 | 0:46:45.340 | 2805.340 | under speech | 0.18 | 0.05 | 35.9 | 35.9 | selection. So we know when Costa -- Costa Cruise Lines, or Costa Crociere learns of this, we know that the plaintiff decided -- Now, which is it? Is that a Freudian slip? |
| 10 | 0:46:49.580 | 2809.580 | under speech | 0.00 | 0.00 | - | - | Crociere learns of this, we know that the plaintiff decided -- Now, which is it? Is that a Freudian slip? No. No, because we’re -- because we’re not disputing -- Just a mistake. |
| 11 | 0:49:17.140 | 2957.140 | big | 2.12 | 1.55 | 20.6 | 26.9 | this time. I -- I make the assumption that it's the cruise line, Crociere, that got the award. So the ticket itself confuses the two companies. Is that a mistake, incidentally? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.640 to 0:03:08.640, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.640] MR. BENDURE: Mr. Chief Justice, and may it please the Court: This case revolves around Rule 15(c)(1)(C) of the Federal Rules of Civil Procedure. In pertinent part, if two subsections are -- are satisfied, the rule permits relation back of an amendment adding a new defendant after expiration of the limitations period. The courts below found, and Respondent does not question, that we satisfied the first subsection: Notice and no prejudice. That arose from the service of the original complaint upon Costa Cruise, the agent and corporate affiliate represented by the same attorney as Respondent Costa Crociere.

[0:00:54.520] JUSTICE GINSBURG: Do you know, Mr. Bendure, what exactly the corporate relationship was between the two?

[0:01:02.000] MR. BENDURE: No, Your Honor, not the corporate relation. The functional relationship as described in the affidavit is that Costa Cruise is the booking agent for Costa Crociere. And for the notice procedure, according to the affidavit of Mr. Klutz, Costa Cruise engaged the IRSI adjustment service to resolve claims arising on the ship. So in that respect it was also, in our view, an agent of Costa Crociere. But the specific corporate relationship is not known.

[0:01:37.920] JUSTICE GINSBURG: Thank you.

[0:01:40.180] MR. BENDURE: Because of that timely service on Costa Cruise, we satisfied the first subsection. And as this Court noted in Schiavone, timely service on one defendant may serve to give imputed notice to a related defendant, which is what we have here.

[0:02:00.320] CHIEF JUSTICE ROBERTS: Counsel, your -- your client tripped over the cable, right?

[0:02:04.080] MR. BENDURE: Correct.

[0:02:04.620] CHIEF JUSTICE ROBERTS: What if the case were there were two people behind her and she was pushed? And she didn't know which one pushed her, Jones or Smith. So she sues Jones, and Smith knows all about it because, of course, he's a key witness or whatever. Can he be substituted later on because he was the person she should have sued?

[0:02:28.000] MR. BENDURE: If you're talking about a lack of knowledge of the real name, probably --

[0:02:32.920] CHIEF JUSTICE ROBERTS: Not just the real name. It's not that Jones pushed her, but his real name is Johnson. It's that Jones -- whoever pushed her; I forget -- but one guy -- (Laughter.)

[0:02:43.340] CHIEF JUSTICE ROBERTS: One of the people pushed her, and she named that -- she named the other person. She made a mistake about who pushed her. Can they have substitution in that case?

[0:02:53.500] MR. BENDURE: I would say yes, because -- again, assuming that all of the other criteria are satisfied.

[0:02:59.980] CHIEF JUSTICE ROBERTS: Yes. The non-pusher has notice --

[0:03:02.820] MR. BENDURE: Yes.

[0:03:02.820] CHIEF JUSTICE ROBERTS: -- and everything else. But there’s no relationship between the two of them.

[0:03:07.620] MR. BENDURE: It's -- it's

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 07, 2010.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2009/09-337
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2009/09-337/20100607o_09-337.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:39.536 (279.536 s)
- Words: 650, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (4 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: Whisper skipped 2 stretches of speech: 0:00:06.660 to 0:00:29.260 (49 words recovered); 0:00:29.920 to 0:00:48.600 (51 words recovered). Each was re-transcribed on its own and the words put in.
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 618 of Whisper's 650 words (95.1%; Oyez has 649).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.660 | 14 |
| JUSTICE SOTOMAYOR | 0:00:08.560 | 0:04:38.760 | 635 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Sotomayor has our opinion this morning in Case 09-337, Kripski v. Costa Crociare.

[0:00:08.560] JUSTICE SOTOMAYOR: Rule 15c of the Federal Rules of Civil Procedure governs when an amended pleading, quote, relates back, close quote, to the date of a timely filed original pleading and is thus itself timely even though it's filed outside an applicable statute of limitations, where an amended pleading changes a Sotomayor. a party's name, the rule requires, among other things, that within a certain time period after the pleading was filed, the, quote, ''party to be brought in by amendment'' knew or should have known that the action would have been brought against it, but for a mistake concerning the proper party's In this case, the plaintiff, the petitioner here, was a passenger on a cruise ship when she tripped and broke her leg. To recover for her injury, she sued a company called Costa Cruz, which had issued her ticket. Costa Cruz responded that she should have sued a related company called Costa. I'm going to ask my colleague, Justice Scalia, to say it right. Crociare. I want to put the Spanish accent on it. Crociare instead. After the statute of limitations had expired, she amended her complaint to add Costa Crociare, but the district court held that her complaint did not relate back because she had chosen to sue Costa Cruz instead of Costa Crociare and thus had not made a, quote, mistake concerning the party, the proper party's identity. The court of appeals affirmed on two grounds. It first held that Rule 15c was not satisfied because the plaintiff knew or should have known of the proper defendant before filing her original complaint. The court also held that relation back was not appropriate because the plaintiff had unduly delayed in seeking to amend. We hold that neither of these reasons was a proper ground on which to deny relation back. Relation back under Rule 15c depends on what the party to be added knew or should have known, not on the amending party's knowledge or timeliness in amending. This is clear from the text of the rule, which focuses on what the party to be added knew or should have known. Moreover, that a plaintiff knows of a party's existence does not preclude her from making a mistake with respect to the party's identity. Making a deliberate choice to sue one party instead of another while fully understanding the factual and legal difference between the two parties is the antithesis of making a mistake concerning the proper party's identity.

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:59.600-0:00:59.900: "from her accident, the plaintiff was asked to pay"
- 0:00:59.900-0:00:59.900: "a party's name. After"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.720 | 09 -337, Kripski v. | 09-337 Krupski versus |
| 0:00:05.900 | Crociare. | Crociere. |
| 0:00:14.260 | quote, relates back, close quote, | “relate backs” |
| 0:00:29.260 | Sotomayor. a | party or |
| 0:00:38.480 | the, quote, | (nothing) |
| 0:00:43.860 | would have | would've |
| 0:00:48.600 | (nothing) | identity”. |
| 0:01:02.740 | Cruz, | Cruise |
| 0:01:06.100 | Cruz | Cruise |
| 0:01:11.080 | I'm | -- I am |
| 0:01:16.520 | Crociare. | Crociere Crociere-- |
| 0:01:24.000 | Crociare | Crociere |
| 0:01:31.240 | Crociare, | Crociere |
| 0:01:39.080 | Cruz | Cruise |
| 0:01:41.020 | Crociare | Crociere |
| 0:01:46.880 | (nothing) | of |
| 0:02:05.440 | back | of that |
| 0:02:26.360 | (nothing) | the |
| 0:03:08.260 | (nothing) | own |
| 0:03:38.380 | clerk | court |
| 0:03:39.800 | (nothing) | and |
| 0:03:58.080 | Cruz | Cruise |
| 0:04:01.720 | Crocere | Crociere |
| 0:04:28.860 | Eleventh | 11th |
