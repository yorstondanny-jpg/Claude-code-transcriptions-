# snyder-gratuity: Supreme Court No. 23-108

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2023/23-108
- Audio: https://www.supremecourt.gov/media/audio/mp3files/23-108.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2023/23-108_o7jp.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 31 min on 4 CPU cores
- Audio length: 1:38:38.640 (5918.640 s)
- `audio/argument.mp3`: mono, 64 kbps, 47.3 MB
- Official words: 18291 (plus 6 `(Laughter.)` markers), in 619 speaker turns
- ASR words: 17252
- Official words matched to an ASR word: 16731 of 18291 (**91.47%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 91.47% (threshold 85%).

848 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 15 times. ASR words with no official counterpart
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 3
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 23-108 2023 snyder-gratuity --model small.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-43.2 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:12:55.700 | 775.700 | under speech | 0.00 | 0.00 | - | - | contract itself. The doctor who removes your wart, fine. But the doctor who takes your gallbladder out or does your face, like my plastic surgeon, no, that's worth over 5,000. |
| 2 | 0:17:16.720 | 1036.720 | big | 2.10 | 1.25 | 22.7 | 33.5 | I mean, the restaurant example alone, I don't know where it's -- I'm pretty sure Chipotle would be okay, Inn at Little Washington wouldn't, but ask them about The Cheesecake Factory. |
| 3 | 0:43:52.860 | 2632.860 | under speech | 0.02 | 0.00 | - | - | there needs to be the acceptance or the solicitation of money in connection with particular business or transactions. Well, they're definitely going to accept the eight-figure gift when it comes. |
| 4 | 0:49:03.397 | 2943.397 | under speech | 0.00 | 0.00 | - | - | this statute give fair notice to anyone in the world as to -- and I hate to do it, but I'm going to -- the difference between the Cheese Factory and -- Cheesecake. |
| 5 | 0:50:19.340 | 3019.340 | big | 1.40 | 1.05 | 27.1 | 33.7 | think -- Counsel, please. Sure. We're going to have internal emails just like Justice Alito posited. Some people say, oh, I wouldn't go to The Cheesecake Factory, that would look bad -- |
| 6 | 1:26:32.420 | 5192.420 | medium | 1.10 | 0.45 | 23.0 | 29.8 | I'm not saying that they won't have 110 ethics rules. Mm-hmm. The hospitals, the universities, et cetera, they're going to have ethics rules. I don't know about the car dealerships. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.680 to 0:03:07.680, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.680] MS. BLATT: Mr. Chief Justice, and may it please the Court: Section 666 applies to 19 million state, local, and tribal officials and anyone else whose employer receives federal benefits, including 14 million Medicare-funded healthcare workers. Congress did not plausibly subject all of these people to 10 years in prison just for accepting gifts, especially when federal officials face only two years for accepting gifts under 201(c). 666 punishes corruptly receiving anything of value intending to be influenced or rewarded. "Corruptly [...] intending to be influenced" covers classic bribes, where officials get upfront payments in exchange for official conduct, while "corruptly [...] intending to be rewarded" covers bribes paid after the fact and to officials who aren't actually influenced. The government argues "corruptly" under 666 means wrongful, immoral, depraved, or evil. But the government tried this case and countless others on the theory that "corruptly" just meant knowingly. Regardless, the government's new definition is implausible and stunningly vague. No gratuity statute -- that's none whatsoever -- uses the word "corruptly" and for good reason. The government can't tell you what gifts are corrupts -- are corrupt. What gift is too much for the doctor who saves your life? Is pornography an immoral gift? The federalism and due process implications of the government's view are gobsmacking. All states prohibit bribery, but localities and states take an -- infinite approaches to gifts and outside compensation. Affirmance would let federal prosecutors second-guess all of these judgments. Meanwhile, state and local officials will have no way of knowing what gift would subject them to 10 years in prison. Remember, extensive guidance tells federal employees that accepting anything over $20 is a crime. It would be downright Kafkaesque to subject state and local officials to a standardless and severe regime where federal interests are at their weakest. I welcome questions.

[0:02:14.380] CHIEF JUSTICE ROBERTS: Ms. Blatt, if I find a lost pet and return it to the owner and the owner's grateful and gives me $10, that's a reward, right, even though nothing else happened in advance between the owner and -- and me?

[0:02:29.100] MS. BLATT: So, yes, divorced from, you know, a crime that makes it a corrupt -- corruptly giving something of value intending to be rewarded, the word "reward," just divorced from text of a statute, context, common sense at least in this case, sure, "reward" can mean both a bribery and -- a quid pro quo bribery and a gratuity. And we think it's very significant in all the statutes that use "reward" to mean gratuities, they're vastly different in four respects here. They all say, when "reward" is used to mean gratuities -- these are cited at page 31 of our brief. They make clear that no quid pro quo payment is

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 26, 2024.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2023/23-108
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2023/23-108%20/23-108_20240626-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 10.0 MB)
- Length: 0:08:16.440 (496.440 s)
- Words: 1142, transcribed by faster-whisper `small.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1126 of Whisper's 1142 words (98.6%; Oyez has 1140).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.640 | 16 |
| JUSTICE KAVANAUGH | 0:00:07.880 | 0:08:15.520 | 1119 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kavanaugh has the opinion of the court this morning, case 23108, Snyder vs. United States.

[0:00:07.880] JUSTICE KAVANAUGH: In 2013, the city of Portage, Indiana awarded two contracts to a local truck company, Great Lakes Peterbilt, to purchase trash trucks. James Snyder was the mayor of Portage. Now, like many jurisdictions around the country, neither Indiana nor Portage apparently prohibited local officials from obtaining outside employment. And Snyder was a contractor for Great Lakes Peterbilt, the truck company that had provided the trash trucks to Portage, and he performed, he said, consulting services for the company. In 2014, Great Lakes Peterbilt cut a $13,000 check to Snyder. Snyder said that the payment was for his consulting services, but the federal government charged and a federal jury convicted Snyder of accepting an illegal gratuity for the trash truck contract in violation of Section 666 of Title 18. The district court sentenced Snyder to one year and nine months in prison. On appeal, Snyder argued that as a matter of law, Section 666 criminalizes only bribes for future official acts, not gratuities for past acts. The U .S. Court of Appeals for the 7th Circuit disagreed based on that court's precedent interpreting the law to cover both bribes and gratuities. So the Court of Appeals affirmed Snyder's conviction. In light of disagreement in the Courts of Appeals about whether Section 666 covers only bribes or covers both bribes and gratuities, we granted review. We now reverse. All agree that Section 666 prohibits state and local officials from accepting bribes that are promised or given before the official act. Those bribes are punishable by up to 10 years imprisonment. The question, however, is whether this law also makes it a crime for state and local officials to accept gratuities. For example, gift cards, lunches, plaques, books, framed photos, or the like that may be given as a token of appreciation after the official act. Some gratuities can be problematic. Others are commonplace and might be innocuous. A family gives a holiday tip to the mail carrier. Parents send an end-of-the-year gift basket to their child's public school teacher. A college dean gives a college sweatshirt to a city council member who comes to speak at an event. A state legislator's neighbor drops off a gift card to congratulate her for her work on a new law. We conclude that Section 666 does not cover gratuities. There are 19 million state and local officials around the country.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:03.420 | (nothing) | in |
| 0:00:05.240 | vs. | versus |
| 0:01:27.560 | 7th | Seventh |
| 0:03:30.740 | reached | reach |
| 0:04:05.600 | in | and |
| 0:04:34.680 | Congress's | Congress’ |
| 0:05:36.700 | lines | line |
| 0:05:45.120 | Diff | (nothing) |
| 0:06:04.180 | (nothing) | a |
| 0:06:45.380 | axe | ax |
| 0:06:49.460 | latter. | ladder. |
