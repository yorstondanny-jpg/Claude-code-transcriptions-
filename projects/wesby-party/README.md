# wesby-party: Supreme Court No. 15-1485

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2017/15-1485
- Audio: https://www.supremecourt.gov/media/audio/mp3files/15-1485.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/15-1485_gfbi.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 40 min on 4 CPU cores
- Audio length: 0:55:48.432 (3348.432 s)
- `audio/argument.mp3`: mono, 64 kbps, 26.8 MB
- Official words: 9781 (plus 4 `(Laughter.)` markers), in 237 speaker turns
- ASR words: 9602
- Official words matched to an ASR word: 9354 of 9781 (**95.63%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.63% (threshold 85%).

277 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 21 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 15-1485 2017 wesby-party --model medium.en --opinion

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:05:37.500 | 337.500 | under speech | 0.00 | 0.00 | - | - | arrest report, Your Honor. So -- I mean, the -- I am told, perhaps I shouldn't take this into account, but compared to the Middle Ages with which I am more familiar -- |
| 2 | 0:22:44.300 | 1364.300 | small | 0.64 | 0.20 | 24.9 | 32.0 | officers act in the future as well. And when looked at from the reasonable partygoer's view, there are these parties that, once long ago, I used to be invited to -- |
| 3 | 0:49:16.640 | 2956.640 | under speech | 0.00 | 0.00 | - | - | on the ground, they know their neighborhoods, and that kind of commonsense consideration should -- should play into account. Just out of curiosity, who is the bachelor at this bachelor party? |
| 4 | 0:50:12.540 | 3012.540 | under speech | 0.00 | 0.00 | - | - | that evidence came out at a trial, at the trial after summary judgment. Officer Campanale changed his story -- So Peaches is the host at a bachelor party. Is that it? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.940 to 0:03:07.940, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.940] MR. KIM: Mr. Chief Justice, and may it please the Court: Probable cause is a practical standard, and thus it accounts for the practical limitations that officers face when making arrest decisions, including their inability to look directly into the minds of suspects offering innocent explanations for suspicious conduct. And so, in a case like this one, what the actus reus established and circumstantial evidence of mens rea that is strong or at least fair, arrest is reasonable, and hence constitutional, and more clearly qualified immunity applies. Let's turn to the totality of the circumstances and consider them from the correct perspective.

[0:00:46.640] JUSTICE GINSBURG: Mr. Kim, before you do that, could you clarify the other charges that are in this case, the one relating to disorderly conduct and negligent supervision? Where do they stand? And are they in any way affected by the argument you're making today?

[0:01:05.260] MR. KIM: We do not pursue an argument that probable cause existed for disorderly conduct. As to negligent supervision, that common law claim fails if there was either probable cause or qualified immunity. That's where they stand, Your Honor. If I may turn back to the totality of the circumstances, my clients responded to neighbors' complaints about --

[0:01:24.980] JUSTICE SOTOMAYOR: I'm sorry, I'm not sure I understood what you just said. Whether we hold on qualified immunity grounds or probable cause grounds, I don't think it affects those claims, does it?

[0:01:37.080] MR. KIM: No, that's right, Your Honor.

[0:01:37.440] JUSTICE SOTOMAYOR: So why would our finding of probable cause affect it? I think those stand on their own, don't they?

[0:01:43.840] MR. KIM: No, Your Honor, if -- if there was probable cause, the negligent supervision would fail as a matter of law. That was undisputed in the courts below, and it's undisputed in this Court.

[0:01:52.000] JUSTICE SOTOMAYOR: Well, we'll let your adversary answer that.

[0:01:54.380] MR. KIM: Thank you, Your Honor. So my clients responded to a neighbor's complaints about illegal activities in a house in their residential community that was supposed to be vacant. They found a group of late-night partiers, none of whom claimed any right over the home. The homeowner, Mr. Hughes, confirmed --

[0:02:10.480] JUSTICE SOTOMAYOR: I'm sorry, why isn't there a right? Someone invites me into what they claim is their home or their place of living. Isn't that an invitation?

[0:02:24.060] MR. KIM: Yes, there was a claim of invitation, Your Honor. I was referring to the absence of any claim of any property right over the home. But, yes, there was --

[0:02:31.000] JUSTICE SOTOMAYOR: But I don't --

[0:02:31.400] MR. KIM: -- a claim --

[0:02:31.400] JUSTICE SOTOMAYOR: -- have a property right when I get invited into someone's home.

[0:02:34.300] MR. KIM: To be sure, Your Honor.

[0:02:34.900] JUSTICE SOTOMAYOR: I don't ask to look at their lease. I don't ask to -- for them to establish, to my satisfaction or anyone else's, their right to be there. I assume if they're there, they can invite me in.

[0:02:47.620] MR. KIM: Your Honor, we're not suggesting that there has to be some type of confirmation by any party guest of the inviter's right to invite. What we're saying instead is from the officer's perspective, looking at the totality of the circumstances, there was a fair probability that Respondents were trespassing either knowingly or negligently. This is not about

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 22, 2018.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2017/15-1485
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2017/15-1485/15-1485_20180122-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:42.253 (282.253 s)
- Words: 622, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 596 of Whisper's 622 words (95.8%; Oyez has 613).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:13.580 | 27 |
| JUSTICE THOMAS | 0:00:13.720 | 0:04:41.260 | 593 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Thomas has our opinion today in Case 15-1485, District of Columbia v. Westby, and he's going to announce it himself. This case comes to us on

[0:00:13.720] JUSTICE THOMAS: writ of certiorari to the United States Court of Appeals for the District of Columbia Circuit. In 2008, D .C. police responded to a late-night complaint about loud music and illegal activities in a vacant house. Inside, they found utter bacchanalia. Strippers were giving lap dances in the living room. A naked woman and several men were in the bedroom with a bare mattress and open condoms. The house was largely unfurnished. Cups of alcohol were on the floor, and the officers smelled marijuana. Many partygoers scattered when they saw the uniformed officers, and some hid. The officers questioned everyone and got inconsistent stories. Two of the strippers said that the tenant, known only as Peaches, had given them permission to host a bachelor party in the house, but Peaches was nowhere to be found. When the officers eventually spoke to Peaches by phone, she was nervous, agitated, and evasive. She hung up on them several times. At first, Peaches claimed that she was renting the house and had given the partygoers permission to have the party, but she eventually admitted that that was a lie. The true owner confirmed that he had not given anyone permission to be there. The officer then arrested the partygoers for unlawful entry. The charges were eventually dropped. Several of the partygoers sued for false arrest. The district of the district court concluded that the officers lacked probable cause to arrest the partygoers for unlawful entry. It also determined that two of the officers were not entitled to qualified immunity, a divided panel of the D .C. Circuit affirmed. In an opinion filed with the clerk today, we reverse. We hold that the officers had probable cause to arrest the partygoers. Considering the totality of the circumstances, the officers made an entirely reasonable inference that the partygoers knew they did not have permission to be in the house. Because most homeowners do not live in barren houses where they invite people to have sex and do drugs, the officers could infer that the partygoers knew the party was not authorized. The officers also could infer that the partygoers knew they were not supposed to be in the house because they scattered and hid when the officers arrived.

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:11.680-0:00:12.280: "Thomas, Jr."
- 0:00:13.580-0:00:13.720: "a"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:06.520 | v. Westby, | versus Wesby |
| 0:00:08.060 | he's | he is |
| 0:00:12.280 | case | (nothing) |
| 0:00:20.580 | 2008, D .C. | 2000 DC |
| 0:01:30.520 | renting | running |
| 0:01:57.000 | of the district | (nothing) |
| 0:03:09.460 | lies | lie |
| 0:03:10.480 | a | (nothing) |
| 0:03:12.880 | Peach's | Peaches' |
| 0:03:31.020 | a | the |
| 0:03:52.080 | precedence, | precedents |
| 0:04:05.580 | arrest | arrests |
| 0:04:09.720 | (nothing) | a |
| 0:04:17.240 | a | (nothing) |
