# raich-marijuana: Supreme Court No. 03-1454

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-1454/20041129a_03-1454.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2004/03-1454.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 61 min on 4 CPU cores
- Audio length: 0:59:53.639 (3593.639 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.8 MB
- Official words: 10645 (plus 8 `(Laughter.)` markers), in 244 speaker turns
- ASR words: 10472
- Official words matched to an ASR word: 10101 of 10645 (**94.89%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.89% (threshold 85%).

291 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 17 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 03-1454 2004 raich-marijuana --model medium.en --opinion --long-questions 10

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE BREYER, 0:51:32.360 to 0:52:54.960 (82.6 s, 238 words)

> -- which was brought up before, and I just -- I've never understood this. I'm not an expert. I don't honestly know, if I really think about it, despite all the papers and so forth, whether it's true that medical marijuana is helpful to people in ways that pills are not. I really don't know. So I would have thought that the people, like your clients, who have a strong view about it, would go to the FDA, and they would say to the FDA, "FDA, take this off the list. You must take it off the list if it has an accepted medical use and it isn't lacking in safety." The FDA will say yes or it will say no. If it says yes, they win. If they say no, they can come right into court and say, "That's an abuse of discretion." The Court says yes or no. If it says yes, they win. If it says no, it must be because it wasn't an abuse of discretion, in which case, I, as a judge, and probably as a person, would think it isn't true that marijuana has some kind of special use. So that would seem to me to be the obvious way to get what they want. That seems to me to be relevant to the correct characterization. And while the FDA can make mistakes, I guess medicine by regulation is better than medicine by referendum.

### 2. JUSTICE SOUTER, 0:23:42.700 to 0:24:57.580 (74.9 s, 197 words)

> May I go back to your point a few minutes ago about -- it was, sort of, a categoric point -- you, in effect, said, "If this argument succeeds with respect to medical use of marijuana, the next argument is going to be recreational use, and there's no real way to distinguish between them." Wouldn't this be a way to distinguish between them? That in deciding what class you are going to -- or what subclass you're going to consider from which to generalize, you simply ask the question, "What good reasons are there to define a subclass this way?" In this particular case, the good reasons to define a subclass of medical usage are the benefits - whether you accept the evidence is another thing -- but the benefits which the doctors say that, under present circumstances, you can get from smoking it, as opposed to taking the synthesized drug. There's no such argument, I would guess, in favor of recreational marijuana usage as a separate category. And, for that reason, isn't there a -- isn't there a good reason to categorize this as narrowly as the Respondents are doing here, just medical usage, without any risk of generalizing to recreational usage?

### 3. JUSTICE SOUTER, 0:35:04.320 to 0:35:56.500 (52.2 s, 153 words)

> But even if we accept your definition of economic, I don't see that it is a basis upon which we ought to make a category decision. You say it's non-economic because one of these people is a -- is a self-grower, another one is getting it from a friend for nothing. But I don't see what reason that you have given, or any reason that you haven't given, for us to believe that, out of -- now I'm going to assume, for the sake of argument, a hundred-thousand potential users -- everybody is going to get it from a friend or from plants in the backyard. Seems to me the sensible assumption is, they're going to get it on the street. And once they get it, under California law, it's not a crime for them to have it and use it. But they're going to get it in the street. Why isn't that the sensible assumption?

### 4. JUSTICE SOUTER, 0:46:42.782 to 0:47:27.680 (44.9 s, 124 words)

> Your whole argument for triviality, though, goes -- your whole argument for triviality, though, goes back to your disagreement with the government about how many people are involved, because I take it you accept the assumption that the more people who are involved -- if there are millions and millions, it is unlikely that this licensed activity is going to be without an effect on the market. So the whole argument boils down to how many people are going to be involved. You don't accept the government's 100,000-dollar figure. Let me ask you a question that would -- that would get to, maybe, a different number, and that is, do you know how many people there are in California who are undergoing chemotherapy at any given time?

### 5. JUSTICE SOUTER, 0:47:57.360 to 0:48:42.060 (44.7 s, 103 words)

> -- lots and lots. They -- a hundred-thousand cancer patients undergoing chemotherapy does not seem like an implausible number. And, in fact, if that number is a plausible one today, its plausibility reflects, among other things, the fact that there is a controversy as to whether California's law, in fact, is enforceable, or not. And the reason -- there is reason to assume that -- if we ruled your way, that that number would go up. So, if you accept that line of argument, then your argument, that the effect, whatever it may be, is going to be trivial, seems to me unsupportable. Am I missing something?

### 6. JUSTICE BREYER, 0:30:08.820 to 0:30:52.440 (43.6 s, 121 words)

> I mean, I don't understand. Is there any authority in the commerce cases for -- an X, which is there in the middle of a state, and it doesn't move one way or the other -- now, Congress' power does extend to the X if the state doesn't say something about the X. But if the state says something about the X, then Congress' power does not extend to it. That's hard for me to accept, because I don't see -- whether it's commerce or not commerce, whether it affects something or doesn't affect something, doesn't seem to me to have much to do with whether the state separately regulates it, and I can't find any support at all for that in any case.

### 7. JUSTICE GINSBURG, 0:12:32.880 to 0:13:14.960 (42.1 s, 91 words)

> -- but there is, in this record, a showing that, for at least one of the two plaintiffs, there were some 30-odd drugs taken, none of them worked. This was the only one that would. And it - Justice Souter asked you about these two plaintiffs. The law can't be made on the basis of those two plaintiffs. But let's suppose that you're right, generally. If there were to be a prosecution of any of the plaintiffs in this case, would there be any defense, if there were to be a federal prosecution?

### 8. JUSTICE SCALIA, 0:27:38.080 to 0:28:20.120 (42.0 s, 104 words)

> Well, you know, Congress has applied this theory in other contexts. One is the protection of endangered species. Congress has made it unlawful to possess ivory, for example. It doesn't matter whether you got it lawfully, or not; or eagle feathers, the mere possession of it, whether you got it through interstate commerce or not. And Congress' reasoning is, "We can't tell whether it came through interstate commerce or not, and to try to prove that is just beyond our ability; and, therefore, it is unlawful to possess it, period." Now, are those -- are those laws, likewise, unconstitutional, as going beyond Congress' commerce power?

### 9. JUSTICE GINSBURG, 0:37:02.960 to 0:37:43.240 (40.3 s, 78 words)

> -- if one takes your view, that this is non-economic activity, so it's outside Congress' commerce power, then explain to me why, if you have someone similarly situated in a neighboring state, somebody whose doctor says, "This person needs marijuana to live," but that state doesn't have a Compassionate-Use Act -- it's just as isolated -- no purchase, no sale, grown at home, good friend grows it -- and yet you say Congress could regulate that, if I understand your brief properly.

### 10. JUSTICE BREYER, 0:39:57.080 to 0:40:35.020 (37.9 s, 90 words)

> I thought we didn't need to reach all that here, for the reason that the connection here, which is an enforcement-related connection and a market-related connection, is actually, I have to confess, a little more obvious and a little more close than what I had to -- what I had to say in Lopez to -- was the connection between guns, education, communities, and business. So I would have thought, given the -- and I believe that, you know -- but, I mean -- but that was far further than this, which is just direct.

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:32:09.000 | 1929.000 | under speech | 0.20 | 0.00 | 6.8 | 7.0 | given the state scheme, the federal scheme is really necessary to include this. That's a task, and I'm trying to make it as complicated as I can in my question. |
| 2 | 0:33:45.000 | 2025.000 | under speech | 0.02 | 0.00 | - | - | more people in the illicit drug market, because that's going to drive the price up. No, no, we don't want more people - Of course not. -- in the illicit drug market. |
| 3 | 0:33:47.620 | 2027.620 | under speech | 0.06 | 0.00 | - | - | to drive the price up. No, no, we don't want more people - Of course not. -- in the illicit drug market. Of course not. And we don't want low prices, either. |
| 4 | 0:39:29.680 | 2369.680 | medium | 2.76 | 0.80 | 10.5 | 17.4 | a new framework, I take it, and it's very interesting. And one of the things that interests me -- I guess, on your framework, Lopez should have come out my way. |
| 5 | 0:39:44.020 | 2384.020 | medium | 0.80 | 0.55 | 23.7 | 32.0 | guns in schools as part of a national gun-control regulatory scheme. Justice Breyer, that's the reason why that exception has to be narrowly treated, so it doesn't reach your result. |
| 6 | 0:46:00.200 | 2760.200 | under speech | 0.00 | 0.00 | - | - | impact, that it will increase the interstate demand, or decrease the interstate demand? So there are three alternatives. Which is the one we should follow? Can I pick "trivial impact"? |
| 7 | 0:46:39.820 | 2799.820 | small | 0.48 | 0.15 | 13.5 | 18.5 | seems to me. It's the other way around. Well, it would reduce demand and reduce prices, I think. But - If you reduce demand, you reduce prices? Are you sure? Yes. |
| 8 | 0:47:57.360 | 2877.360 | under speech | 0.00 | 0.00 | - | - | don't know the number of people using chemotherapy. But whatever the number - How many people are there in California? What's the population? Thirty-four million. Thank you, Justice Kennedy. Lots -- lots - |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.000 to 0:03:08.000, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.000] MR. CLEMENT: Justice Stevens, and may it please the Court: Through the Controlled Substances Act, Congress has comprehensively regulated the national market in drugs with the potential for abuse. And with respect to Schedule I substances, like marijuana, that have both a high potential for abuse and no currently accepted medical use in treatment, Congress categorically prohibits interstate trafficking outside the narrow and carefully controlled confines of federally approved research programs.

[0:00:36.340] JUSTICE O'CONNOR: Well, Mr. Clement, the -- I think it is reasonably clear that Congress spoke very broadly in the Act, and the question, for me, turns on whether Lopez and Morrison dictate some concerns with its application in this context.

[0:00:59.400] MR. CLEMENT: Well, with respect, Justice O'Connor, I don't think either Lopez or Morrison casts any doubt on the constitutionality of the Controlled Substances Act, and I think, in particular, that's because the decisions in Lopez and Morrison cited, with approval, cases like Darby and Wickard, and preserved those cases. And, of course, the concurring opinion of Justice Kennedy did so, as well.

[0:01:20.620] JUSTICE O'CONNOR: Well, but in Wickard, of course, you had a wheat grower, a small farmer, and his wheat did, in part, go in the national market. You don't have that here. As I understand it, if California's law applies, then none of this home-grown for medical-use marijuana will be on any interstate market. And it is in the area of something traditionally regulated by states. So how do you distinguish Morrison? And how do you distinguish Lopez?

[0:01:57.160] MR. CLEMENT: Well, Justice O'Connor, let me first say that I think it might be a bit optimistic to think that none of the marijuana that's produced consistent with California law would be diverted into the national market for marijuana. And, of course, the Controlled Substances Act is concerned, at almost every step of the Act, with a concern about diversion, both of lawful substances from medical to non-medical uses and from controlled substances under Schedule I into the national market.

[0:02:20.920] JUSTICE O'CONNOR: Well, in looking at this broad challenge, do we have to assume that the State of California will enforce its law? I mean, if it turns out that it isn't and that marijuana is getting in the interstate market, that might be a different thing.

[0:02:35.660] MR. CLEMENT: Well, with respect, Justice O'Connor, on this record, I don't think that there's any reason to assume that California is going to have some sort of almost unnatural ability to keep one part of a fungible national drug market separate. And I think Congress, here, made important findings that you've alluded to, not just that there's a national market, not just that the intrastate and the interstate markets are linked, but that drugs are fungible, and that because drugs are fungible, it's simply not feasible, in Congress' words, to regulate and separately focus on only drugs that have traveled on interstate commerce.

[0:03:07.860] JUSTICE STEVENS: Well,

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 06, 2005.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2004/03-1454
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2004/03-1454/20050606o_03-1454.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.0 MB)
- Length: 0:04:14.903 (254.903 s)
- Words: 576, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 559 of Whisper's 576 words (97.0%; Oyez has 571).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE REHNQUIST | 0:00:00.000 | 0:00:06.800 | 15 |
| JUSTICE STEVENS | 0:00:08.520 | 0:04:13.620 | 560 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE REHNQUIST: The opinion of the Court in Gonzalez v. Wright will be announced by Justice Stevens.

[0:00:08.520] JUSTICE STEVENS: This case comes to us from the Court of Appeals for the Ninth Circuit. California is one of at least nine States that authorize the use of marijuana for medicinal purposes. The question presented in this case is whether the power vested in Congress by Article I, Section 8 of the Constitution to make all laws which shall be necessary and proper for carrying into execution its authority to regulate interstate commerce includes the power to prohibit the local cultivation and use of marijuana in compliance with California law. Respondents are seriously ill California residents. Their doctors have concluded after unsuccessfully prescribing a host of conventional medicines that marijuana is the only drug available that provides effective treatment. Both women have been using marijuana as a medication for several years pursuant to their doctor's recommendation, and both rely heavily on cannabis to function on a daily basis. While Respondents' activities do not violate California law, they do violate the Federal Controlled Substance Act of 1970, a comprehensive regulatory statute which, among other things, categorically prohibits the manufacture, distribution, or possession of marijuana for any purpose. After agents from the Drug Enforcement Administration seized and destroyed their cannabis plants, Respondents filed this action to prohibit enforcement of the Federal statute to the extent that it prevents them from cultivating marijuana for their personal medical use. The district court denied relief, but the Court of Appeals for the Ninth Circuit held that as applied to their activities, the CSA exceeded Congress power under the Commerce Clause. Because of the obvious importance of the case, we granted certiorari. The case is extremely troublesome because Respondents have made such a strong showing that they will suffer irreparable harm if denied the use of marijuana to treat their serious medical ailments. But the question before us is not whether marijuana does in fact have valid therapeutic purposes, nor whether it is good policy for the Federal government to enforce the Controlled Substances Act in these circumstances. Rather, the only question before us is whether Congress has the power to prohibit Respondents' activities. California law does not really affect our answer to that question, for it is well settled that the outer limits of congressional power under the Commerce Clause are defined exclusively by Federal law. The Supremacy Clause unambiguously provides that

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.920 | Gonzalez v. Wright | Gonzales versus Raich |
| 0:02:20.980 | ailments. | illness. |
| 0:02:29.300 | (nothing) | a |
| 0:03:29.020 | use | used |
| 0:03:49.560 | reasons | reason |
| 0:04:09.260 | 3 | three |
| 0:04:09.700 | the vote. | (nothing) |
