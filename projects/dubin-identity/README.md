# dubin-identity: Supreme Court No. 22-10

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2022/22-10
- Audio: https://www.supremecourt.gov/media/audio/mp3files/22-10.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/22-10_f3b7.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 89 min on 4 CPU cores
- Audio length: 1:32:29.184 (5549.184 s)
- `audio/argument.mp3`: mono, 64 kbps, 44.4 MB
- Official words: 16636 (plus 8 `(Laughter.)` markers), in 403 speaker turns
- ASR words: 16072
- Official words matched to an ASR word: 15775 of 16636 (**94.82%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- FAIL: no word longer than 3 s except before a laugh. 1 words longer than 3 s outside laugh positions.
  Offending words: "titles" 987.200-990.820. Left as the ASR timed them: none of the timing rules below could place them with confidence, and a re-transcription of the window didn't help. This is usually overlapping speech, where two people talk at once and the ASR hears only one; the transcript's word order then can't match the audio. Check by ear.
  Not counted: `101` 5271.440-5278.080 (6.64 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 94.82% (threshold 85%).

534 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 9 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 21 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 22-10 2022 dubin-identity --model medium.en --pdf-url https://www.supremecourt.gov/oral_arguments/argument_transcripts/2022/22-10_f3b7.pdf --opinion --long-questions 10

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE ALITO, 0:14:17.860 to 0:15:30.440 (72.6 s, 193 words)

> Your argument has a lot of intuitive appeal because this does not seem like what one normally thinks of as identity theft, but I'm wondering if you are trying to get too much out of the caption of this -- out of -- of this provision. And I know it's a little -- it's unfair to ask you about a case that we heard argument in last week, but I know you follow our cases, so I'm going to do it. If you just want to take a pass, that's fine. But we heard very extensive argument on the meaning of Section 230 of the Communications Act, which provides -- has been held by the lower courts to provide pretty broad immunity from civil liability for Internet service providers. But the -- the caption of that section is "Protection for Good Samaritan Blocking and Screening of Offensive Material." So the -- the interpretation that the lower courts have given to that provision goes way beyond what you might think of just by looking at the caption. So, I mean, how far can we go in reading -- taking the caption as the gloss on the actual text of the statute?

### 2. JUSTICE GORSUCH, 0:56:11.200 to 0:57:13.640 (62.4 s, 156 words)

> Counsel, it seems to me you've just given up the ghost and -- and clarified things substantially that every time anyone overbills for anything, that triggers this statute, and all you have to prove -- now it may be small, as the amounts here were, $338, or it might be rounding up, a lawyer rounding up his hours to the next tenth of an hour, but that is still identity theft because you are using somebody's identity in a way that is unlawful and perhaps arguably exceeds their permission. If that's true, where do we stand in terms of federalism, given that (a)(7) speaks in much the same language and would seem to federalize pretty much every state misrepresentation claim? Where do we stand in terms of vagueness, notice to the world, fair notice to the world? I'm not sure most waiters in America appreciate that they're committing identity theft when they bill for that bottle of wine.

### 3. JUSTICE KAVANAUGH, 1:21:53.080 to 1:22:53.700 (60.6 s, 139 words)

> In the court of appeals, Judge Costa's opinion said that this Court's precedents had sent an "unmistakable" message that "[c]ourts should not assign federal criminal statutes [of] a 'breath-taking' scope when a narrower reading is reasonable." And the Petitioner also cites a long line of cases you're familiar with, Marinello, Van Buren, Kelly, the list goes on, where we have rejected, I would say, the broadest interpretation of criminal statutes, the literal reading as compared to the ordinary reading of criminal statutes, based on fair notice concerns and not trapping the unwary or increasing the sentence on an unwary person. So what -- why does this case not fall within that concern and with that body of precedent about reading it as broadly as you possibly could and thereby raising fair notice concerns of the kinds that Judge Costa raised?

### 4. JUSTICE ALITO, 0:30:17.560 to 0:31:11.660 (54.1 s, 136 words)

> Suppose we think that "without lawful authority" can plausibly be read in a number of different ways. Then you need something to persuade us that you -- we should adopt your interpretation. Now one would be something, the force you can get from the title. Put that aside. Another would be perhaps some version of the Rule of Lenity. But you have accepted some limiting principles. So you would not read "without lawful authority" in its broadest sense, which might be where the Rule of Lenity would lead. So, in the next case -- suppose we rule in your favor. The next case involves a different type of service, and the case after that involves a person who was once a patient of this doctor but hasn't been for a while. How would you justify your limiting principles?

### 5. JUSTICE JACKSON, 1:14:02.880 to 1:14:56.920 (54.0 s, 144 words)

> Of course, that's not the function of mandatory minimums. I mean, they're not really -- I appreciate that it has a higher top level, but Congress, when it -- when it enacts a mandatory minimum, is constraining judicial discretion with respect to what you can impose as a penalty. And usually Congress does that in situations in which it has identified substantially more serious or more egregious conduct on the part of the person who is subject to the mandatory minimum. And what's strange to me about your argument is that you're saying, in this situation, unlike many others, we don't care about that. We're not focused on the fact that it's necessarily more egregious. We're just looking at the list of offenses, and, to the extent a misdemeanor could be charged in the other world, that -- that justifies a two-year mandatory minimum in this one?

### 6. JUSTICE KAVANAUGH, 1:23:42.240 to 1:24:30.400 (48.2 s, 116 words)

> Well, that's similar to an argument I heard years ago from the government about mens rea: Don't worry about mens rea requirements for sentence enhancements as opposed to the crime itself. And I didn't find that persuasive then because the concern about sentence enhancements is -- is still, as Justice Gorsuch said earlier, you know, the -- the ordinary citizen may know, okay, well, this is going to trigger a certain amount of punishment, but you're on no notice that it could trigger a mandatory minimum or a significantly increased amount of punishment. So don't the same concerns about fair notice still kick in in that situation, where you're talking about an enhancement as to the underlying crime?

### 7. JUSTICE KAGAN, 1:18:10.340 to 1:18:57.180 (46.8 s, 115 words)

> Mr. Suri, you -- just on this question of "without lawful authority," different kind of issue, in your brief, you say that means if he uses it with permission -- no, sorry, if he uses it without permission or -- here's what I want to ask you about -- if he uses it with permission but the conferral of that permission contravened some other law. So suppose somebody had said to this doctor -- that Patient L had said to this doctor, you know, you gave me five hours of service X, but you've been a great doctor; I'm happy for you to bill 20 hours of some more expensive service. Would that count as without lawful authority or not?

### 8. JUSTICE JACKSON, 0:20:36.900 to 0:21:21.940 (45.0 s, 112 words)

> -- because it uses almost identical terms, right, "knowingly transfer, possess, or use," and then we have "in connection with" unlawful activity. So that's kind of like the base offense. And then, in 1028A, we have the aggravated offense, where they say not just "in connection with" but "during and in relation to" the particular enumerated crimes. So it seemed to me to be a -- a familiar structure in penalty statutes at least, where Congress -- you have -- you -- you have one that doesn't have a mandatory minimum that's sort of the base, and then you get aggravated with this different level of, you know, egregiousness. Is that -- is that close to your argument?

### 9. JUSTICE SOTOMAYOR, 0:32:39.040 to 0:33:23.440 (44.4 s, 97 words)

> If you take the government's definition at face value, it's hard to define exactly what their definition is because every time you point to something that seems absurd, they come up with a limiting rule. So the vagueness is a problem. But let's talk about those absurdities. The patient tells the doctor: You can submit this a month later, it's okay by me, a co-conspirator, in other words. The government -- on the government's reading, even though they have the permission of the person to use their name in the fraud, that would still be aggravated theft, correct?

### 10. JUSTICE JACKSON, 0:48:35.740 to 0:49:19.720 (44.0 s, 108 words)

> So you've given us a number of ways in which we could rule in your favor and things we can look at and rely on. I -- I was trying to keep a list. We have title, the Rule of Lenity, all the statutory terms have meaning, federalism canon, and then there was this talk of constitutional avoidance. And I am interested in particular in sort of the species of constitutional avoidance that I was bringing up with you before, which basically looks at this provision in context and in relation to (a)(7). In other words, this is an aggravated penalty and we have a mandatory minimum that attaches.

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-43.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:40:54.940 | 2454.940 | under speech | 0.00 | 0.00 | - | - | offense that uses somebody's name becomes identity theft. Whether it's in a restaurant billing scenario, a healthcare billing scenario, or lawyers who round their hours up, and I'm sure nobody -- |
| 2 | 0:54:31.640 | 3271.640 | medium | 1.12 | 0.90 | 16.8 | 20.8 | hours. Would that be sufficient to violate this provision? Yes, Justice Thomas. And I appreciate that that may seem an unattractive result. Well, I think unattractive is -- is an understatement. |
| 3 | 0:57:45.640 | 3465.640 | big | 2.44 | 1.95 | 27.4 | 36.1 | them -- -- then we'd have a serious federalism problem, wouldn't we? -- if you read them the same, you'd be creating a federalism problem that you could avoid by reading them differently. |
| 4 | 0:59:00.260 | 3540.260 | under speech | 0.00 | 0.00 | - | - | fraud in America is within the scope of the Commerce Clause, counsel? If that's a problem, Justice Gorsuch, it's attributable to the Court's Commerce Clause cases and not to this -- |
| 5 | 1:09:42.040 | 4182.040 | medium | 1.52 | 0.80 | 21.9 | 31.5 | of the calendar year period. Now, Justice Gorsuch, I -- I must get back to this question of "in connection with" and the federalism problems. Well, let's -- let's -- let's skip that. |
| 6 | 1:09:51.280 | 4191.280 | medium | 1.08 | 0.90 | 20.7 | 25.8 | let's -- let's skip that. I think we've beaten that horse, but I do have another question for you since you -- you looked over here. Maybe you -- maybe you regret that. |
| 7 | 1:09:53.300 | 4193.300 | big | 2.50 | 1.55 | 25.7 | 35.9 | I think we've beaten that horse, but I do have another question for you since you -- you looked over here. Maybe you -- maybe you regret that. I regret it already. |
| 8 | 1:20:12.700 | 4812.700 | small | 0.54 | 0.15 | 14.2 | 20.2 | not psychological services now but something else entirely. How does the Judge Sutton test work with relationship to those hypotheticals -- I think -- -- which also means with connection to those hypotheticals. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.780 to 0:03:06.780, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.780] MR. FISHER: Mr. Chief Justice, and may it please the Court: The Fifth Circuit's decision here stretches the aggravated identity theft statute beyond its breaking point. Overbilling Medicaid by $101 may provide fodder for a simple healthcare fraud prosecution, but, as even the concurring judges below recognized, it does not meet any ordinary understanding of the term "identity theft." Nor, for two independent reasons, does Mr. Dubin's conduct fall within the terms of Section 1028A. First, he did not use Patient L's name in relation to his healthcare fraud offense. That statutory element requires that the use of the name be instrumental, not merely incidental, to the fraud. In a fraud case, another way to think about that is it requires the name to be the "who" in the fraud, that is, misrepresenting who received services, not merely how or when those services were received. And Mr. Dubin's conduct falls only in the latter camp. Second, Mr. Dubin did not use Patient L's identity without lawful authority. He had permission to use Patient L's identity to bill Medicaid for psychological services, and that's precisely what he did. A contextual perspective confirms this analysis. The federal fraud statute that's the predicate here, like the other federal fraud statutes, covers an enormously broad swath of conduct, and, therefore, Congress has made prison time discretionary in those instances. And as the Federal Defenders' brief explains, the median sentence in a fraud case in this country is 12 months. Twenty-five percent of offenders receive only probation. The -- this statute, by contrast, requires a two-year mandatory minimum. So all indications are what Congress was doing is targeting a particularly egregious form of fraud, use of somebody's name through stealing it, misappropriating it, or -- or impersonating the person, identity theft. But, if the government is right and if the Fifth Circuit is right about how broad the statute is, what it would do is it would transform fraud prosecutions to having every one of them be essentially an aggravated identity theft prosecution too, and that would thwart Congress's careful design. The Court should reverse, and I'm happy to answer any questions the Court has.

[0:02:18.440] JUSTICE THOMAS: Mr. Fisher, you said that -- that Mr. Dubin was authorized to use the -- Patient L's identity. Was Dubin authorized to use Patient -- Patient L's identity for this particular transaction?

[0:02:40.480] MR. FISHER: Well, I think the best I can answer is yes, he was in the sense that he was authorized to use Patient L's identity for billing Medicaid. That was the name that was at the center --

[0:02:48.300] JUSTICE THOMAS: Well, I understand -- that's a little broader. Well, you could say that if you drop a car off at a valet, your Porsche -- I don't have one -- but, if you had a Porsche, you'd be concerned about the use of it, and the valet is authorized to drive it generally but not to drive

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 08, 2023.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2022/22-10
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2022/22-10/22-10_20230608-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 6.5 MB)
- Length: 0:05:22.776 (322.776 s)
- Words: 642, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 592 of Whisper's 642 words (92.2%; Oyez has 620).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:05.740 | 12 |
| JUSTICE SOTOMAYOR | 0:00:07.340 | 0:05:21.880 | 627 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Sotomayor has the opinion in case 2210, Dubin versus United States.

[0:00:07.340] JUSTICE SOTOMAYOR: I won't be as entertaining. There is no dispute that petitioner David Fox Dubin defrauded Medicaid by overbilling it. He did so primarily by exaggerating the credentials of one of his employees when billing for services that were actually provided to a patient. The question in this case is whether in doing so, petitioner also committed aggravated identity theft. The relevant provision 18 U .S .C. section 1028A applies to a defendant who, quote, during and in relation to any predicate offense, knowingly transfers, possesses, or lawful authority, a means of identification of another person. Here petitioner billed for services actually provided to a patient using that patient's means of identification, i .e., their Medicaid reimbursement number. The question is, this question is critical because section 2028A imposes a harsh two-year mandatory minimum sentence on top of any sentence for the predicate offense of fraud. The government advances a nearly limitless interpretation of section 1028A under which a defendant commits aggravated identity theft anytime someone else's means of identification plays some role in an offense. Under this reading, if a lawyer inflated her billable hours by rounding up from 2.9 to 3 and billed her client using his name, she would have committed aggravated identity theft. The text and context of section 1028A do not support this sweeping reading. Instead, a defendant uses another person's means of identification in relation to a predicate offense when the means of identification is at the crux of what makes the conduct criminal rather than merely an ancillary feature of a billing method. When the predicate offense involves fraud or deceit, this requires using the means of identification specifically to defraud or deceive. Such fraud or deceit about identity can often be captured by a rule of thumb. The statute applies when the fraud goes to who is involved rather than just how or when services were provided. From top to bottom, the text and context support this narrower reading. First, the two key terms, use and in relationship to, have been singled

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:07.440 | won't | would not |
| 0:00:40.200 | section | (nothing) |
| 0:00:51.900 | (nothing) | uses without |
| 0:01:09.360 | The question is, | (nothing) |
| 0:01:13.040 | section | (nothing) |
| 0:01:27.380 | a | are |
| 0:01:29.980 | section | (nothing) |
| 0:01:52.840 | billed | build |
| 0:02:00.500 | and | in |
| 0:02:01.640 | section | (nothing) |
| 0:02:04.160 | this sweeping reading. Instead, a | the sweepingreading, insteada |
| 0:02:51.620 | and | in |
| 0:02:57.160 | use | used |
| 0:03:27.920 | section | (nothing) |
| 0:04:13.520 | section | (nothing) |
| 0:04:26.920 | garden variety overbuilding | garden-variety overbilling |
| 0:04:41.300 | Section | (nothing) |
| 0:04:43.580 | the | a |
| 0:05:09.480 | section | in |
