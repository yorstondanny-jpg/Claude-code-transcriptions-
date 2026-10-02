# pom-juice: Supreme Court No. 12-761

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2013/12-761
- Audio: https://www.supremecourt.gov/media/audio/mp3files/12-761.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2013/12-761_j5f1.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 37 min on 4 CPU cores
- Audio length: 1:01:51.530 (3711.530 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.7 MB
- Official words: 9488 (plus 2 `(Laughter.)` markers), in 159 speaker turns
- ASR words: 9454
- Official words matched to an ASR word: 8954 of 9488 (**94.37%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.37% (threshold 85%).

204 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 30 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 12-761 2013 pom-juice --model medium.en --opinion --mentions "pomegranate,blueberry,juice,label,0.3,percent,five juices,consumers,unintelligent,fool,feel bad,read,Minute Maid,FDA" --quotes "quite as unintelligent as POM must think they are|Don't make me feel bad because I thought that this was pomegranate juice|it's pomegranate-blueberry-flavored blend of five juices|He sometimes doesn't read closely enough"

## Quotes

Each line's exact place in the argument (official wording; matched ignoring case, punctuation and hyphens), and the 10 seconds of audio centred on it: the window's times, a clip of it, and everything said in it.

### 1. "quite as unintelligent as POM must think they are"

- Said by MS. SULLIVAN, 0:46:54.270 to 0:46:56.930 (2814.270 to 2816.930 s): "quite as unintelligent as POM must think they are."
- 10-second window: 0:46:50.600 to 0:47:00.600 (2810.600 to 2820.600 s), clip [`audio/quotes/quote_1.mp3`](audio/quotes/quote_1.mp3)

> [0:46:50.310] MS. SULLIVAN: or a percentage, and it won't be misleading. Why? Because we don't think that consumers are quite as unintelligent as POM must think they are. They know when something is a favored blend of five juices, non-min- -- the

### 2. "Don't make me feel bad because I thought that this was pomegranate juice"

- Said by JUSTICE KENNEDY, 0:47:04.170 to 0:47:07.630 (2824.170 to 2827.630 s): "Don't make me feel bad because I thought that this was pomegranate juice."
- 10-second window: 0:47:00.900 to 0:47:10.900 (2820.900 to 2830.900 s), clip [`audio/quotes/quote_2.mp3`](audio/quotes/quote_2.mp3)

> [0:47:00.710] MS. SULLIVAN: non-predominant juices are just a flavor.
> [0:47:04.170] JUSTICE KENNEDY: Don't make me feel bad because I thought that this was pomegranate juice. (Laughter.)
> [0:47:09.310] MS. SULLIVAN: Justice Kennedy --

### 3. "it's pomegranate-blueberry-flavored blend of five juices"

- Said by MS. SULLIVAN, 0:47:11.710 to 0:47:16.330 (2831.710 to 2836.330 s): "it's pomegranate-blueberry-flavored blend of five juices."
- 10-second window: 0:47:09.020 to 0:47:19.020 (2829.020 to 2839.020 s), clip [`audio/quotes/quote_3.mp3`](audio/quotes/quote_3.mp3)

> [0:47:07.630] JUSTICE KENNEDY: (Laughter.)
> [0:47:09.310] MS. SULLIVAN: Justice Kennedy -- Justice Kennedy, it's pomegranate-blueberry-flavored blend of five juices. I've found that oftentimes --

### 4. "He sometimes doesn't read closely enough"

- Said by JUSTICE SCALIA, 0:47:21.870 to 0:47:23.710 (2841.870 to 2843.710 s): "He sometimes doesn't read closely enough."
- 10-second window: 0:47:17.790 to 0:47:27.790 (2837.790 to 2847.790 s), clip [`audio/quotes/quote_4.mp3`](audio/quotes/quote_4.mp3)

> [0:47:17.770] MS. SULLIVAN: found that oftentimes -- well --
> [0:47:21.870] JUSTICE SCALIA: He sometimes doesn't read closely enough. (Laughter.)
> [0:47:23.930] MS. SULLIVAN: Yeah, pomegranate-blueberry-flavored

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-45.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:47:07.630 | 2827.630 | big | 1.68 | 1.55 | 26.6 | 29.6 | when something is a favored blend of five juices, non-min- -- the non-predominant juices are just a flavor. Don't make me feel bad because I thought that this was pomegranate juice. |
| 2 | 0:47:23.710 | 2843.710 | under speech | 0.22 | 0.05 | 27.2 | 27.2 | bad because I thought that this was pomegranate juice. Justice Kennedy -- Justice Kennedy, it's pomegranate-blueberry-flavored blend of five juices. I've found that oftentimes -- well -- He sometimes doesn't read closely enough. |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| pomegranate | 23 | 27 |
| blueberry | 15 | 15 |
| juice | 42 | 63 |
| label | 70 | 83 |
| 0.3 | 1 | 1 |
| percent | 7 | 9 |
| five juices | 4 | 4 |
| consumers | 23 | 24 |
| unintelligent | 1 | 1 |
| fool | 0 | 0 |
| feel bad | 1 | 1 |
| read | 1 | 1 |
| Minute Maid | 0 | 0 |
| FDA | 94 | 108 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:25.900 | 25.900 | MR. WAXMAN | label | Coca-Cola's label grossly misleads consumers , as Coke anticipated, but Coke says that it need not answer under the Lanham Act because its label is authorized by FDA regulations. |
| 0:00:27.880 | 27.880 | MR. WAXMAN | consumers | Coca-Cola's label grossly misleads consumers , as Coke anticipated, but Coke says that it need not answer under the Lanham Act because its label is authorized by FDA regulations. |
| 0:00:37.020 | 37.020 | MR. WAXMAN | FDA | Coca-Cola's label grossly misleads consumers , as Coke anticipated, but Coke says that it need not answer under the Lanham Act because its label is authorized by FDA regulations. |
| 0:00:40.060 | 40.060 | MR. WAXMAN | label | The label is not, in fact, authorized for reasons we explain and with which the United States largely agrees, but even if it were consistent with FDA regulations that would not strip POM of its right to prove a willful Lanham Act violation. |
| 0:00:49.420 | 49.420 | MR. WAXMAN | FDA | The label is not, in fact, authorized for reasons we explain and with which the United States largely agrees, but even if it were consistent with FDA regulations that would not strip POM of its right to prove a willful Lanham Act violation. |
| 0:01:09.740 | 69.740 | MR. WAXMAN | label | Here Congress has never precluded or conditioned enforcement of the Lanham Act in food labeling cases, and it is entirely possible, in fact, entirely easy for Coke to comply with both statutory obligations. |
| 0:01:23.260 | 83.260 | JUSTICE SOTOMAYOR | FDA | If there is no private cause of action to enforce the FDA label standards, only the FDA can bring a proceeding to say that an ad violates its regulations, how does a Court below, without interpreting the regulations, go about deciding whether or not a particular ad doesn't comport with the regulations and hence would be subject to the Lanham Act? |
| 0:01:24.900 | 84.900 | JUSTICE SOTOMAYOR | label | If there is no private cause of action to enforce the FDA label standards, only the FDA can bring a proceeding to say that an ad violates its regulations, how does a Court below, without interpreting the regulations, go about deciding whether or not a particular ad doesn't comport with the regulations and hence would be subject to the Lanham Act? |
| 0:02:58.980 | 178.980 | MR. WAXMAN | label | Our submission is that it is entirely irrelevant whether or not the Coke label, in any particular, is consistent with a regulation that implements criminal prohibitions by announcing when and under what limited circumstances the FDA will forebear from exercising its criminal and regulatory penalties. |
| 0:03:13.660 | 193.660 | MR. WAXMAN | FDA | Our submission is that it is entirely irrelevant whether or not the Coke label, in any particular, is consistent with a regulation that implements criminal prohibitions by announcing when and under what limited circumstances the FDA will forebear from exercising its criminal and regulatory penalties. |
| 0:03:38.700 | 218.700 | JUSTICE KENNEDY | label | And so do you concede that under the Lanham Act, plaintiff could not challenge aspects of the a food label that the FDA said is required? |
| 0:03:39.360 | 219.360 | JUSTICE KENNEDY | FDA | And so do you concede that under the Lanham Act, plaintiff could not challenge aspects of the a food label that the FDA said is required? |
| 0:03:51.960 | 231.960 | MR. WAXMAN | FDA | Let me just say, not only is that not this case because the FDA has never examined -- |
| 0:04:03.560 | 243.560 | MR. WAXMAN | FDA | My answer to the question would be, under Wyeth, under this Court's decision in Wyeth, the FDCA and the FDA's regulations interpreting it and applying it, supply a floor and not a ceiling. |
| 0:04:11.760 | 251.760 | MR. WAXMAN | FDA | And the FDA would have no authority -- if the FDA said, This label is fine and you are required to use this label, the question would be, does it have the statutory authority to essentially create an immunity from enforcement of another federal statute that protects a different purpose and a different class of victims? |
| 0:04:15.980 | 255.980 | MR. WAXMAN | label | And the FDA would have no authority -- if the FDA said, This label is fine and you are required to use this label, the question would be, does it have the statutory authority to essentially create an immunity from enforcement of another federal statute that protects a different purpose and a different class of victims? |
| 0:04:43.960 | 283.960 | JUSTICE KAGAN | label | He said, suppose that it said you are required to use this label and only this label, then you would acknowledge that there is an impossibility issue; is that right? |
| 0:04:56.200 | 296.200 | MR. WAXMAN | label | Unless, as in Wyeth, there was, in fact, some possibility to change the label, but if -- and I apologize if I didn't understand the question. |
| 0:04:59.980 | 299.980 | MR. WAXMAN | FDA | If the FDA said, counterfactually, we've examined this label, you are not only permitted to use it but you are required to use it, and unlike what we do with respect to pharmaceuticals, you are not allowed to make any changes. |
| 0:05:03.520 | 303.520 | MR. WAXMAN | label | If the FDA said, counterfactually, we've examined this label, you are not only permitted to use it but you are required to use it, and unlike what we do with respect to pharmaceuticals, you are not allowed to make any changes. |
| 0:05:34.340 | 334.340 | JUSTICE KAGAN | FDA | Let's just focus on the name, which is what the solicitor general says the FDA has considered and has specifically permitted. |
| 0:05:51.260 | 351.260 | JUSTICE KAGAN | FDA | And essentially the FDA has said, This is what counts as misbranding, nothing else counts as misbranding. |
| 0:06:02.200 | 362.200 | JUSTICE KAGAN | FDA | And now you're coming in and under a Lanham Act claim saying, no, the FDA is wrong. |
| 0:06:10.000 | 370.000 | JUSTICE KAGAN | FDA | That the FDA said it's not misbranding, you're saying it is misbranding. |
| 0:06:17.280 | 377.280 | JUSTICE KAGAN | FDA | That seems a quite direct conflict as to what the FDA says versus what you are alleging under the Lanham Act. |
| 0:06:23.600 | 383.600 | MR. WAXMAN | FDA | So we know that that is not, in fact, how the FDA construes its regulation, and we know that because just by examining the FDA's own limited enforcement history, all the parties have cited the Court -- |
| 0:06:36.400 | 396.400 | JUSTICE KAGAN | FDA | Well, just hypothetically, let's say that the FDA said that this name was not misbranding, that this name was fine under their regulations, that they did not count as misbranding. |
| 0:06:48.460 | 408.460 | MR. WAXMAN | label | So we're challenging the label as a whole, which is covered by -- under the -- |
| 0:06:56.600 | 416.600 | JUSTICE KAGAN | label | So I understand that, you would have some claims about different parts of the label. |
| 0:07:02.960 | 422.960 | JUSTICE KAGAN | FDA | But I'm only asking about your claiming as -- your claim as to the specific thing that the FDA ruled on. |
| 0:07:19.060 | 439.060 | MR. WAXMAN | label | And the question is whether Congress gave any indication and it would have to, in this context where the Lanham Act is an express statutory enactment that Congress was well aware of when it enacted the Nutrition Labeling Act and, in fact, was told, not just by the industry, but by OMB, in testimony, that the Lanham Act was being used to police misrepresentations of the character of food products, you would have to conclude that Congress intended to allow the FDA to supply, if you will, the substantive rule of decision under a different statute that uses different words and -- and protects a different class of people when -- and here again, I think it's an important indicator why Congress didn't mean that. |
| 0:07:39.300 | 459.300 | MR. WAXMAN | FDA | And the question is whether Congress gave any indication and it would have to, in this context where the Lanham Act is an express statutory enactment that Congress was well aware of when it enacted the Nutrition Labeling Act and, in fact, was told, not just by the industry, but by OMB, in testimony, that the Lanham Act was being used to police misrepresentations of the character of food products, you would have to conclude that Congress intended to allow the FDA to supply, if you will, the substantive rule of decision under a different statute that uses different words and -- and protects a different class of people when -- and here again, I think it's an important indicator why Congress didn't mean that. |
| 0:07:58.620 | 478.620 | MR. WAXMAN | FDA | The FDA, the misbranding provisions of the FDCA are prohibitions. |
| 0:08:08.880 | 488.880 | MR. WAXMAN | FDA | And the rules that the FDA has promulgated announce essentially an enforcement forbearance. |
| 0:08:26.840 | 506.840 | MR. WAXMAN | juice | They don't represent a judgment and the Federal Register provisions that we've cited that accompanied the promulgation of the juice naming regulations make this as clear as day. |
| 0:09:07.020 | 547.020 | MR. WAXMAN | juice | In fact, they say although for purposes of our forbearance under our government enforcement authority, we will allow you to do one or the other -- and this is 2919 and 2920 of Federal Register 58, We warn manufacturers that even compliance with this, where there is a small amount of the non-predominant juice name has great capacity to mislead and we encourage -- twice in the rulemaking, we encourage manufacturers, nonetheless, to name the juices in the product. |
| 0:09:38.160 | 578.160 | MR. WAXMAN | label | Under those circumstances, the notion that Congress intended this type of regulation to preclude a case in which -- and these are the facts as the Court -- as they come to the Court -- Coke well knew and intentionally designed a label that, in fact, grossly misleads consumers to the economic disadvantage of the company that, in large part, created the market. |
| 0:09:41.240 | 581.240 | MR. WAXMAN | consumers | Under those circumstances, the notion that Congress intended this type of regulation to preclude a case in which -- and these are the facts as the Court -- as they come to the Court -- Coke well knew and intentionally designed a label that, in fact, grossly misleads consumers to the economic disadvantage of the company that, in large part, created the market. |
| 0:09:52.540 | 592.540 | MR. WAXMAN | FDA | And the notion that Congress wanted to allow the FDA to apply substantive rules of decision in that very different inquiry using very different language in a different statute, I think, is completely unsupported. |
| 0:10:29.900 | 629.900 | MR. WAXMAN | label | Well, we have in -- in the course of our complaint, we didn't specify -- I mean, the injunction that we would seek is ceasing to use the label as it currently exists, and of course -- |
| 0:10:33.020 | 633.020 | JUSTICE GINSBURG | label | Without saying what label would be lawful? |
| 0:11:07.840 | 667.840 | MR. WAXMAN | consumers | All that they may -- all they do is make a judgment about whether or not on balance, there is substantial evidence that to the harm of the competitor, a substantial number of consumers are misled, and if so, was it willful. |
| 0:11:29.260 | 689.260 | MR. WAXMAN | label | In Wyeth versus Levine, the plaintiff had all sorts of reasons -- all sorts of different theories about what the warning label should or shouldn't say. |
| 0:11:39.380 | 699.380 | MR. WAXMAN | label | The jury simply decided that it violated the common law of the state of Vermont to use that particular label. |
| 0:11:46.620 | 706.620 | JUSTICE ALITO | percent | Suppose it was 50 percent pomegranate and blueberry. |
| 0:11:47.220 | 707.220 | JUSTICE ALITO | pomegranate | Suppose it was 50 percent pomegranate and blueberry. |
| 0:11:48.320 | 708.320 | JUSTICE ALITO | blueberry | Suppose it was 50 percent pomegranate and blueberry. |
| 0:12:06.660 | 726.660 | MR. WAXMAN | consumers | I mean, we have to come up with -- we have to adduce, it's our burden, substantial evidence to show that a substantial number of competitors -- of consumers are not only misled, but misled to the detriment of our product. |
| 0:12:26.680 | 746.680 | MR. WAXMAN | pomegranate | But Coke's argument, and for that matter the government's argument, with respect to the name itself, would apply if, unlike the eyedropper's worth of pomegranate juice that's in the half-gallon bottle, there were two microns. |
| 0:12:27.320 | 747.320 | MR. WAXMAN | juice | But Coke's argument, and for that matter the government's argument, with respect to the name itself, would apply if, unlike the eyedropper's worth of pomegranate juice that's in the half-gallon bottle, there were two microns. |
| 0:12:48.220 | 768.220 | MR. WAXMAN | consumers | And the evidence shows that over a third of consumers who look at this label believe that pomegranate and blueberry juice, in fact, are the majority juices. |
| 0:12:49.600 | 769.600 | MR. WAXMAN | label | And the evidence shows that over a third of consumers who look at this label believe that pomegranate and blueberry juice, in fact, are the majority juices. |
| 0:12:51.060 | 771.060 | MR. WAXMAN | pomegranate | And the evidence shows that over a third of consumers who look at this label believe that pomegranate and blueberry juice, in fact, are the majority juices. |
| 0:12:52.040 | 772.040 | MR. WAXMAN | blueberry | And the evidence shows that over a third of consumers who look at this label believe that pomegranate and blueberry juice, in fact, are the majority juices. |
| 0:12:52.420 | 772.420 | MR. WAXMAN | juice | And the evidence shows that over a third of consumers who look at this label believe that pomegranate and blueberry juice, in fact, are the majority juices. |
| 0:13:08.620 | 788.620 | JUSTICE ALITO | pomegranate | But let's say there are a few people who are very allergic to pomegranate juice or blueberry juice. |
| 0:13:09.660 | 789.660 | JUSTICE ALITO | juice | But let's say there are a few people who are very allergic to pomegranate juice or blueberry juice. |
| 0:13:10.120 | 790.120 | JUSTICE ALITO | blueberry | But let's say there are a few people who are very allergic to pomegranate juice or blueberry juice. |
| 0:13:11.560 | 791.560 | JUSTICE ALITO | FDA | And so the FDA says, if you put even an eyedropper full of that in your blend, you have to put that prominently on the bottle so that these people will not inadvertently get an allergic reaction. |
| 0:13:32.220 | 812.220 | MR. WAXMAN | consumers | Well, of course, pome -- the only thing that consumers know is that -- from the front label is that there is pomegranate -- arguably pomegranate juice and blueberry juice in here. |
| 0:13:34.460 | 814.460 | MR. WAXMAN | label | Well, of course, pome -- the only thing that consumers know is that -- from the front label is that there is pomegranate -- arguably pomegranate juice and blueberry juice in here. |
| 0:13:35.620 | 815.620 | MR. WAXMAN | pomegranate | Well, of course, pome -- the only thing that consumers know is that -- from the front label is that there is pomegranate -- arguably pomegranate juice and blueberry juice in here. |
| 0:13:38.380 | 818.380 | MR. WAXMAN | juice | Well, of course, pome -- the only thing that consumers know is that -- from the front label is that there is pomegranate -- arguably pomegranate juice and blueberry juice in here. |
| 0:13:38.800 | 818.800 | MR. WAXMAN | blueberry | Well, of course, pome -- the only thing that consumers know is that -- from the front label is that there is pomegranate -- arguably pomegranate juice and blueberry juice in here. |
| 0:13:42.940 | 822.940 | MR. WAXMAN | label | So the question would be whether they had to disclose on the label whether there was also .01 percent strawberry juice or 99.4 percent apple and grape juice. |
| 0:13:45.420 | 825.420 | MR. WAXMAN | percent | So the question would be whether they had to disclose on the label whether there was also .01 percent strawberry juice or 99.4 percent apple and grape juice. |
| 0:13:46.520 | 826.520 | MR. WAXMAN | juice | So the question would be whether they had to disclose on the label whether there was also .01 percent strawberry juice or 99.4 percent apple and grape juice. |
| 0:13:54.040 | 834.040 | MR. WAXMAN | FDA | That's the kind of judgment that we want the FDA to make, because the purpose of the FDCA is protect public health and safety. |
| 0:14:00.300 | 840.300 | MR. WAXMAN | FDA | What the FDA doesn't do, particularly given the criminal nature of its sanctions, is regulate or interpret, apply its forbearance authority with an eye toward, well, what kinds of things are going to so mislead consumers that they think there is going to be a substitute in the marketplace where there isn't. |
| 0:14:14.040 | 854.040 | MR. WAXMAN | consumers | What the FDA doesn't do, particularly given the criminal nature of its sanctions, is regulate or interpret, apply its forbearance authority with an eye toward, well, what kinds of things are going to so mislead consumers that they think there is going to be a substitute in the marketplace where there isn't. |
| 0:14:23.420 | 863.420 | JUSTICE ALITO | percent | Well, what I'm saying is suppose it's the case that for 99.999 percent of the population, the more pomegranate juice, the better, you just can't drink enough of it. |
| 0:14:25.340 | 865.340 | JUSTICE ALITO | pomegranate | Well, what I'm saying is suppose it's the case that for 99.999 percent of the population, the more pomegranate juice, the better, you just can't drink enough of it. |
| 0:14:25.980 | 865.980 | JUSTICE ALITO | juice | Well, what I'm saying is suppose it's the case that for 99.999 percent of the population, the more pomegranate juice, the better, you just can't drink enough of it. |
| 0:14:36.760 | 876.760 | JUSTICE ALITO | FDA | And so the FDA says, you've got to put that on there even if there is just a tincture of pomegranate juice. |
| 0:14:41.160 | 881.160 | JUSTICE ALITO | pomegranate | And so the FDA says, you've got to put that on there even if there is just a tincture of pomegranate juice. |
| 0:14:41.920 | 881.920 | JUSTICE ALITO | juice | And so the FDA says, you've got to put that on there even if there is just a tincture of pomegranate juice. |
| 0:14:50.400 | 890.400 | JUSTICE ALITO | pomegranate | Could you have a Lanham Act claim on the ground for the vast majority of your potential customers, they are going to be misled, because they want pomegranate juice and they are buying this stuff that just has a little bit of it in it? |
| 0:14:51.080 | 891.080 | JUSTICE ALITO | juice | Could you have a Lanham Act claim on the ground for the vast majority of your potential customers, they are going to be misled, because they want pomegranate juice and they are buying this stuff that just has a little bit of it in it? |
| 0:15:04.080 | 904.080 | MR. WAXMAN | FDA | Well, I think the vast -- presumably, and we're talking about a hypothetical regulation, presumably the FDA would promulgate a requirement that, in fact, you must name each of the -- each of the constituent juices in case there is an allergy. |
| 0:15:11.960 | 911.960 | MR. WAXMAN | juice | Well, I think the vast -- presumably, and we're talking about a hypothetical regulation, presumably the FDA would promulgate a requirement that, in fact, you must name each of the -- each of the constituent juices in case there is an allergy. |
| 0:15:19.180 | 919.180 | MR. WAXMAN | consumers | I mean, we wouldn't have an objection -- the argument wouldn't be that consumers are misled by that fact alone. |
| 0:15:24.200 | 924.200 | MR. WAXMAN | consumers | What's misleading consumers here is they have no way on God's green earth of telling that the total amount of blueberry and pomegranate juice in this product can be dispensed with a single eyedropper. |
| 0:15:34.520 | 934.520 | MR. WAXMAN | blueberry | What's misleading consumers here is they have no way on God's green earth of telling that the total amount of blueberry and pomegranate juice in this product can be dispensed with a single eyedropper. |
| 0:15:35.220 | 935.220 | MR. WAXMAN | pomegranate | What's misleading consumers here is they have no way on God's green earth of telling that the total amount of blueberry and pomegranate juice in this product can be dispensed with a single eyedropper. |
| 0:15:35.740 | 935.740 | MR. WAXMAN | juice | What's misleading consumers here is they have no way on God's green earth of telling that the total amount of blueberry and pomegranate juice in this product can be dispensed with a single eyedropper. |
| 0:15:44.695 | 944.695 | MR. WAXMAN | FDA | And the FDA has -- the FDA has explained in this case that it has no expertise, it has no warrant to interpret or understand or apply judgments about what kind of words and symbols and the combination thereof, to use the language of the Lanham Act, will have a tendency to misrepresent the nature or quality of the goods from the perspective of the competitor. |
| 0:16:46.760 | 1006.760 | MR. WAXMAN | label | The state law provision, Justice Kennedy, is Section 110660 of the California Health and Safety Code, which -- the language of which is in haec verba with the very first subsection of the misbranding statute 343(A), which declares misbranded any label which is false in particular -- false and misleading in any particular. |
| 0:17:21.810 | 1041.810 | MR. WAXMAN | FDA | There might be an open question if one of the things that we were challenging in the course of that state lawsuit was the name itself, and the question then would be is this name, in fact, compliant with the FDA regulation? |
| 0:18:32.490 | 1112.490 | MS. SHERRY | label | We have a circumstance here where we have two Federal statutes that cover the same subject matter that apply functionally the same standard to the same words on the same product label. |
| 0:18:38.250 | 1118.250 | MS. SHERRY | FDA | Under the FDCA, we have an authoritative interpretation of that language by the FDA. |
| 0:18:47.070 | 1127.070 | MS. SHERRY | FDA | The FDA considered the exact same question that is being raised here. |
| 0:18:55.890 | 1135.890 | MS. SHERRY | juice | It looked to figure out what an appropriate common or usual name was for a juice blend that had a small amount of a highly flavorful and expensive juice in order to allow consumers to know -- in order to prevent consumers from being misled as to the juice content of that particular product. |
| 0:19:01.890 | 1141.890 | MS. SHERRY | consumers | It looked to figure out what an appropriate common or usual name was for a juice blend that had a small amount of a highly flavorful and expensive juice in order to allow consumers to know -- in order to prevent consumers from being misled as to the juice content of that particular product. |
| 0:19:28.350 | 1168.350 | MS. SHERRY | FDA | It has a number of subsections, one of which gives the FDA authority to establish common or usual names of products. |
| 0:19:49.490 | 1189.490 | MS. SHERRY | juice | And, in fact, that was the purpose of the very regulation at issue here, the idea being by allowing manufacturers to choose to name their juice product based on the juice that flavors the product as opposed to based on the juice that is predominant by volume, that consumers will come to understand that when a juice says pomegranate and blueberry flavored, what it means is that the juice is present as a flavor. |
| 0:19:56.590 | 1196.590 | MS. SHERRY | consumers | And, in fact, that was the purpose of the very regulation at issue here, the idea being by allowing manufacturers to choose to name their juice product based on the juice that flavors the product as opposed to based on the juice that is predominant by volume, that consumers will come to understand that when a juice says pomegranate and blueberry flavored, what it means is that the juice is present as a flavor. |
| 0:19:59.170 | 1199.170 | MS. SHERRY | pomegranate | And, in fact, that was the purpose of the very regulation at issue here, the idea being by allowing manufacturers to choose to name their juice product based on the juice that flavors the product as opposed to based on the juice that is predominant by volume, that consumers will come to understand that when a juice says pomegranate and blueberry flavored, what it means is that the juice is present as a flavor. |
| 0:19:59.990 | 1199.990 | MS. SHERRY | blueberry | And, in fact, that was the purpose of the very regulation at issue here, the idea being by allowing manufacturers to choose to name their juice product based on the juice that flavors the product as opposed to based on the juice that is predominant by volume, that consumers will come to understand that when a juice says pomegranate and blueberry flavored, what it means is that the juice is present as a flavor. |
| 0:20:23.010 | 1223.010 | MS. SHERRY | 0.3 | The argument is because there is only 0.3 percent of pomegranate juice, that it is not actually enough to flavor the beverage. |
| 0:20:23.810 | 1223.810 | MS. SHERRY | percent | The argument is because there is only 0.3 percent of pomegranate juice, that it is not actually enough to flavor the beverage. |
| 0:20:24.550 | 1224.550 | MS. SHERRY | pomegranate | The argument is because there is only 0.3 percent of pomegranate juice, that it is not actually enough to flavor the beverage. |
| 0:20:25.330 | 1225.330 | MS. SHERRY | juice | The argument is because there is only 0.3 percent of pomegranate juice, that it is not actually enough to flavor the beverage. |
| 0:20:37.770 | 1237.770 | MS. SHERRY | percent | But Petitioner's argument with respect to the name would be exactly the same, Justice Alito, if there was 10 percent of pomegranate juice in this product or there was 15 percent. |
| 0:20:38.390 | 1238.390 | MS. SHERRY | pomegranate | But Petitioner's argument with respect to the name would be exactly the same, Justice Alito, if there was 10 percent of pomegranate juice in this product or there was 15 percent. |
| 0:20:38.870 | 1238.870 | MS. SHERRY | juice | But Petitioner's argument with respect to the name would be exactly the same, Justice Alito, if there was 10 percent of pomegranate juice in this product or there was 15 percent. |
| 0:20:57.650 | 1257.650 | JUSTICE SOTOMAYOR | label | Then, Ms. Sherry, you -- the government is taking the position that it's okay for District Courts to determine whether labels, in fact, comply or don't comply with FDA regulations? |
| 0:21:01.530 | 1261.530 | JUSTICE SOTOMAYOR | FDA | Then, Ms. Sherry, you -- the government is taking the position that it's okay for District Courts to determine whether labels, in fact, comply or don't comply with FDA regulations? |
| 0:21:14.490 | 1274.490 | MS. SHERRY | FDA | And let me try to explain why I don't think that’s inconsistent with the notion of the FDA having exclusive enforcement authority with respect to the FDCA. |
| 0:21:24.950 | 1284.950 | MS. SHERRY | FDA | The FDCA and the FDA regulations come up by virtue of the preclusion defense that is being raised by Respondents here. |
| 0:21:35.350 | 1295.350 | MS. SHERRY | FDA | And so in the course of adjudicating that defense, we agree that district courts can look to the FDA regulations to determine compliance, of course, by applying all the normal rules of deference that would otherwise apply in those circumstances. |
| 0:21:50.570 | 1310.570 | JUSTICE KENNEDY | label | Do I understand your position to be that then if the label is specifically authorized, then the Lanham Act is precluded, but if the FDCA has just simply failed to forbid it then it's not? |
| 0:22:14.510 | 1334.510 | MS. SHERRY | FDA | What we're saying is that if the FDA or the FDCA provisions have specifically permitted something here, they've specifically permitted this type of name in certain circumstances, that that is something that should preclude a Lanham Act claim. |
| 0:22:27.010 | 1347.010 | MS. SHERRY | FDA | To the extent the FDCA or the FDA has not spoken to the particular issue with any degree of specificity, we don't see a problem with the Lanham Act claim going forward, because in that case you're not really second- guessing any judgment -- |
| 0:22:43.110 | 1363.110 | JUSTICE GINSBURG | pomegranate | But, Ms. Sherry, applied to this case, so we have -- you said the name is okay, pomegranate and blueberry flavored, but you say the label is something different from the name and the Lanham Act can apply to the label. |
| 0:22:43.650 | 1363.650 | JUSTICE GINSBURG | blueberry | But, Ms. Sherry, applied to this case, so we have -- you said the name is okay, pomegranate and blueberry flavored, but you say the label is something different from the name and the Lanham Act can apply to the label. |
| 0:22:47.690 | 1367.690 | JUSTICE GINSBURG | label | But, Ms. Sherry, applied to this case, so we have -- you said the name is okay, pomegranate and blueberry flavored, but you say the label is something different from the name and the Lanham Act can apply to the label. |
| 0:22:58.230 | 1378.230 | JUSTICE GINSBURG | label | So what parts of the label are you saying are not touched -- are not preempted by the FDA laws? |
| 0:23:07.050 | 1387.050 | JUSTICE GINSBURG | FDA | So what parts of the label are you saying are not touched -- are not preempted by the FDA laws? |
| 0:23:13.310 | 1393.310 | MS. SHERRY | pomegranate | We're drawing a distinction -- when we say the name, we mean the actual words themselves, "pomegranate blueberry flavored blendified juices." |
| 0:23:13.850 | 1393.850 | MS. SHERRY | blueberry | We're drawing a distinction -- when we say the name, we mean the actual words themselves, "pomegranate blueberry flavored blendified juices." |
| 0:23:15.190 | 1395.190 | MS. SHERRY | juice | We're drawing a distinction -- when we say the name, we mean the actual words themselves, "pomegranate blueberry flavored blendified juices." |
| 0:23:16.590 | 1396.590 | MS. SHERRY | label | When we talk about the label more generally, we mean how those words are presented on the label and other aspects of the label. |
| 0:23:38.230 | 1418.230 | MS. SHERRY | FDA | What the FDA said in that letter was that the juice labels at issue there were misleading, not because of the name, but because how the words of the name were displayed on the label, because the words "orange tangerine," for example, were placed next to the picture of an orange, because they were in close proximity to "100 percent" -- |
| 0:23:40.630 | 1420.630 | MS. SHERRY | juice | What the FDA said in that letter was that the juice labels at issue there were misleading, not because of the name, but because how the words of the name were displayed on the label, because the words "orange tangerine," for example, were placed next to the picture of an orange, because they were in close proximity to "100 percent" -- |
| 0:23:40.790 | 1420.790 | MS. SHERRY | label | What the FDA said in that letter was that the juice labels at issue there were misleading, not because of the name, but because how the words of the name were displayed on the label, because the words "orange tangerine," for example, were placed next to the picture of an orange, because they were in close proximity to "100 percent" -- |
| 0:23:56.610 | 1436.610 | MS. SHERRY | percent | What the FDA said in that letter was that the juice labels at issue there were misleading, not because of the name, but because how the words of the name were displayed on the label, because the words "orange tangerine," for example, were placed next to the picture of an orange, because they were in close proximity to "100 percent" -- |
| 0:23:57.530 | 1437.530 | CHIEF JUSTICE ROBERTS | label | What if the label just had the name on it, nothing else? |
| 0:24:03.230 | 1443.230 | CHIEF JUSTICE ROBERTS | label | Could they still sue on the ground that the label was misleading? |
| 0:24:07.650 | 1447.650 | MS. SHERRY | label | Not unless they are able to point to something else on the label that was misleading aside from the actual words in the name. |
| 0:24:19.310 | 1459.310 | MS. SHERRY | juice | The difficulty we have with the naming aspect of the Lanham Act claim here is the arguments that Petitioner is making that they should have instead named this "apple grape juice," that they should have instead included the percentage declarations, are arguments that the FDA specifically considered when it adopted this rule and it ultimately objected. |
| 0:24:24.610 | 1464.610 | MS. SHERRY | FDA | The difficulty we have with the naming aspect of the Lanham Act claim here is the arguments that Petitioner is making that they should have instead named this "apple grape juice," that they should have instead included the percentage declarations, are arguments that the FDA specifically considered when it adopted this rule and it ultimately objected. |
| 0:24:28.285 | 1468.285 | CHIEF JUSTICE ROBERTS | FDA | Does the FDA -- does the FDA take into account purely commercial confusion when it issues -- when it issued its regulations governing the label? |
| 0:24:38.010 | 1478.010 | CHIEF JUSTICE ROBERTS | label | Does the FDA -- does the FDA take into account purely commercial confusion when it issues -- when it issued its regulations governing the label? |
| 0:24:55.850 | 1495.850 | MS. SHERRY | consumers | There were comments with respect to this particular regulation, and the commenters were consumers saying that they were concerned that they were being misled with respect to the juice content. |
| 0:24:59.570 | 1499.570 | MS. SHERRY | juice | There were comments with respect to this particular regulation, and the commenters were consumers saying that they were concerned that they were being misled with respect to the juice content. |
| 0:25:00.910 | 1500.910 | CHIEF JUSTICE ROBERTS | FDA | What does the FDA know about that? |
| 0:25:05.950 | 1505.950 | CHIEF JUSTICE ROBERTS | FDA | I mean, I would understand if it was the FTC or something like that, but I don't know that the FDA has any expertise in terms of consumer confusion apart from any health issues. |
| 0:25:18.370 | 1518.370 | MS. SHERRY | label | The misbranding provisions, 343(a)(1), speak generally about labels that are false or misleading in any particular. |
| 0:25:25.050 | 1525.050 | MS. SHERRY | FDA | And in adopting the common or usual name here, that is something that the FDA was specifically focused on. |
| 0:25:49.490 | 1549.490 | JUSTICE KAGAN | FDA | Ms. Sherry, you know, there is no irreconcilable conflict if we view what the FDA has done as just setting a floor. |
| 0:25:55.010 | 1555.010 | JUSTICE KAGAN | FDA | And you talk a lot about how, oh, the FDA specifically considered this and it decided not to do this. |
| 0:26:06.550 | 1566.550 | JUSTICE KAGAN | FDA | And I guess my question to you is, is that the way you are saying we should know whether the FDA has only set a floor or instead has also set a ceiling, that we're supposed to look to the process and figure out whether the FDA specifically rejected a more extensive proposal, a more aggressive proposal? |
| 0:26:50.550 | 1610.550 | JUSTICE KAGAN | consumers | You've said here is the floor to make it not misleading, but, you know, we are not saying that there are some things that, you know, wouldn't mislead a lot of consumers anyway, and then the Lanham Act can come in and supplement that and really put us in a position where nothing is misleading at all. |
| 0:27:07.750 | 1627.750 | MS. SHERRY | consumers | Number one, because the agency considered why manufacturers would want to actually name their product based on the flavor, because consumers actually do care about the flavor and they care about the taste. |
| 0:27:12.690 | 1632.690 | MS. SHERRY | juice | If the product had the name "apple grape juice," for example, and it in fact tasted like pomegranate blueberry juice, a consumer might be very surprised when he came home and had a sip of that juice and realized it tasted like something very different than what he expected. |
| 0:27:14.830 | 1634.830 | MS. SHERRY | pomegranate | If the product had the name "apple grape juice," for example, and it in fact tasted like pomegranate blueberry juice, a consumer might be very surprised when he came home and had a sip of that juice and realized it tasted like something very different than what he expected. |
| 0:27:15.410 | 1635.410 | MS. SHERRY | blueberry | If the product had the name "apple grape juice," for example, and it in fact tasted like pomegranate blueberry juice, a consumer might be very surprised when he came home and had a sip of that juice and realized it tasted like something very different than what he expected. |
| 0:27:23.390 | 1643.390 | JUSTICE ALITO | pomegranate | You don't think there are a lot of people who buy pomegranate juice because of -- they think it has health benefits and they would be very surprised to find when they bring home this bottle that's got a big picture of a pomegranate on it and it says "pomegranate" on it, that it is -- what is it, less than one-half of one percent pomegranate juice? |
| 0:27:24.070 | 1644.070 | JUSTICE ALITO | juice | You don't think there are a lot of people who buy pomegranate juice because of -- they think it has health benefits and they would be very surprised to find when they bring home this bottle that's got a big picture of a pomegranate on it and it says "pomegranate" on it, that it is -- what is it, less than one-half of one percent pomegranate juice? |
| 0:27:36.290 | 1656.290 | JUSTICE ALITO | percent | You don't think there are a lot of people who buy pomegranate juice because of -- they think it has health benefits and they would be very surprised to find when they bring home this bottle that's got a big picture of a pomegranate on it and it says "pomegranate" on it, that it is -- what is it, less than one-half of one percent pomegranate juice? |
| 0:27:38.050 | 1658.050 | JUSTICE ALITO | FDA | The FDA didn't think that would mislead consumers? |
| 0:27:39.570 | 1659.570 | JUSTICE ALITO | consumers | The FDA didn't think that would mislead consumers? |
| 0:28:39.890 | 1719.890 | MS. SULLIVAN | label | Section 341 makes clear that it also and with respect to the labeling requirements at issue here, quote, "promotes honesty and fair dealing in the interest of consumers." |
| 0:28:44.850 | 1724.850 | MS. SULLIVAN | consumers | Section 341 makes clear that it also and with respect to the labeling requirements at issue here, quote, "promotes honesty and fair dealing in the interest of consumers." |
| 0:28:59.150 | 1739.150 | MS. SULLIVAN | label | And here, the most important data we have about what Congress did that's barely been mentioned by POM or the government, is the enactment in 1990 of the NLEA, the Nutrition Labeling and Education Act, and its express preemption provision. |
| 0:31:56.330 | 1916.330 | JUSTICE KENNEDY | label | Is it part of Coke's narrow position that national uniformity consists in labels that cheat the consumers like this one did? |
| 0:31:57.350 | 1917.350 | JUSTICE KENNEDY | consumers | Is it part of Coke's narrow position that national uniformity consists in labels that cheat the consumers like this one did? |
| 0:32:22.110 | 1942.110 | JUSTICE KENNEDY | label | And if the statute works in the way you say it does and that Coca-Cola stands behind this label as being fair to consumers, then I think you have a very difficult case to make. |
| 0:32:23.330 | 1943.330 | JUSTICE KENNEDY | consumers | And if the statute works in the way you say it does and that Coca-Cola stands behind this label as being fair to consumers, then I think you have a very difficult case to make. |
| 0:32:40.030 | 1960.030 | JUSTICE KENNEDY | label | Do you still have this -- do you still have this label? |
| 0:33:01.550 | 1981.550 | MS. SULLIVAN | label | POM is arguing here that it may challenge Coca-Cola's name and label under the Lanham Act even if that name and label complies with the FDCA and all the relevant implementing regulations. |
| 0:33:21.481 | 2001.481 | MS. SULLIVAN | FDA | So, Justice Kagan, this is exactly your case, where POM said it can say misbranded under the Lanham Act, even where Coca-Cola has complied with all of the authorizations set forth in the FDA. |
| 0:34:20.370 | 2060.370 | MS. SULLIVAN | label | we're talking here about labeling so that consumers have adequate information, at the same time as manufacturers are not put to the burdens and inefficiencies of having constantly shifting labeling standards imposed by juries, which ultimately will cost more to the consumer. |
| 0:34:22.230 | 2062.230 | MS. SULLIVAN | consumers | we're talking here about labeling so that consumers have adequate information, at the same time as manufacturers are not put to the burdens and inefficiencies of having constantly shifting labeling standards imposed by juries, which ultimately will cost more to the consumer. |
| 0:34:43.450 | 2083.450 | JUSTICE SOTOMAYOR | FDA | The FDA just wanted to know what the name should be. |
| 0:35:32.750 | 2132.750 | MS. SULLIVAN | FDA | Justice Sotomayor and Justice Kennedy, I need to make very clear that we believe that under the FDCA and the FDA regulations, Coke's label is as a matter of law not misleading. |
| 0:35:35.070 | 2135.070 | MS. SULLIVAN | label | Justice Sotomayor and Justice Kennedy, I need to make very clear that we believe that under the FDCA and the FDA regulations, Coke's label is as a matter of law not misleading. |
| 0:35:40.590 | 2140.590 | MS. SULLIVAN | FDA | And once we reach that conclusion under FDCA and FDA, Lanham Act can't come in from the side and say, oh, yes, it is, because that would undermine the express preemption provision that was designed to create national uniformity. |
| 0:35:57.830 | 2157.830 | JUSTICE SOTOMAYOR | label | Could the government -- I think what the government is saying nothing about our permission goes to the size of the name on the label -- |
| 0:36:01.290 | 2161.290 | JUSTICE SOTOMAYOR | juice | -- that you can break up the name of the juice into two different sizes so that you are deemphasizing it. |
| 0:36:30.090 | 2190.090 | JUSTICE SOTOMAYOR | juice | It's -- nothing in the regulations talk about using purple instead of whatever that color is that the juice is, that blue, purple, whatever, instead of the color of apple juice. |
| 0:36:36.470 | 2196.470 | JUSTICE SOTOMAYOR | juice | If you use the color of apple juice and grapes, it would be a light color. |
| 0:36:44.490 | 2204.490 | MS. SULLIVAN | label | Justice Sotomayor, there are five different attacks that POM has made on our label, only two of which were addressed in the lower court. |
| 0:36:50.610 | 2210.610 | MS. SULLIVAN | FDA | And we say that we comply with FDA regulations as to all five of them. |
| 0:38:07.630 | 2287.630 | MS. SULLIVAN | label | Justice Ginsburg, POM doesn't just want to enjoin our label. |
| 0:38:12.250 | 2292.250 | MS. SULLIVAN | juice | POM at JA61 said: You should have called it apple grape juice, not pomegranate blueberry juice. |
| 0:38:12.930 | 2292.930 | MS. SULLIVAN | pomegranate | POM at JA61 said: You should have called it apple grape juice, not pomegranate blueberry juice. |
| 0:38:13.090 | 2293.090 | MS. SULLIVAN | blueberry | POM at JA61 said: You should have called it apple grape juice, not pomegranate blueberry juice. |
| 0:38:18.710 | 2298.710 | JUSTICE GINSBURG | label | They just want to say your label is misleading. |
| 0:38:27.010 | 2307.010 | JUSTICE GINSBURG | FDA | And is there -- what statute or regulation of the FDA says that compliance with the permissive regulation of the FDA necessarily renders the label non-misleading? |
| 0:38:37.030 | 2317.030 | JUSTICE GINSBURG | label | And is there -- what statute or regulation of the FDA says that compliance with the permissive regulation of the FDA necessarily renders the label non-misleading? |
| 0:39:20.810 | 2360.810 | MS. SULLIVAN | label | And if you look at the express preemption provision, which is notably called "National Uniform Nutrition Labeling," Section (2) and Section (3) on 5A over to 6A, set forth those portions of the FDCA that will and won't have preemptive force. |
| 0:40:03.910 | 2403.910 | MS. SULLIVAN | label | "Font size" is covered by 343(f), which goes to the presentation of the name and other printed matter on the label. |
| 0:40:45.110 | 2445.110 | MS. SULLIVAN | FDA | Yes, Your Honor, we still win because of your more general approach to preclusion by one Federal statute of another, because the FDA regulations as to misbranding here are far more specific. |
| 0:41:06.750 | 2466.750 | JUSTICE KENNEDY | FDA | You say that even if there's a violation of the FDA regulations, they still couldn't sue under the Lanham Act because that's for the FDA. |
| 0:41:30.610 | 2490.610 | MS. SULLIVAN | FDA | In this case we believe the Lanham Act claim is precluded because POM wants to go above the floor set by the FDCA and the FDA reg. |
| 0:41:45.930 | 2505.930 | MS. SULLIVAN | FDA | POM has said repeatedly in this case, right through the reply brief -- right through its reply brief at Page 17, and I quote, and this has been their position the whole time, POM's challenge does not depend on the FDCA or FDA's regulation. |
| 0:41:53.650 | 2513.650 | MS. SULLIVAN | FDA | Justice Sotomayor, POM is not bringing your hypothetical suit where they come in to enforce the FDCA and the FDA. |
| 0:42:15.090 | 2535.090 | JUSTICE GINSBURG | FDA | And there is no judicial review of the FDA regulations. |
| 0:42:19.290 | 2539.290 | JUSTICE GINSBURG | FDA | There's no private right of action under the FDA. |
| 0:42:49.750 | 2569.750 | MS. SULLIVAN | FDA | But what I'm trying to say here is, to the extent their Lanham Act claims seeks to say, as Justice Kagan said before, You are misbranded for misrepresentations under the Lanham Act, even though Coke has not been misbranded and has not made misrepresentations under FDCA and the FDA regulations, that is a conflict that should be resolved by this Court in the usual manner that statutory construction conflicts are resolved by making the statutes make sense together. |
| 0:43:03.270 | 2583.270 | CHIEF JUSTICE ROBERTS | label | I don't know why -- I don't know why it's impossible to have a label that fully complies with the FDA regulations and also happens to be misleading on the entirely different question of commercial competition, consumer confusion that has nothing to do with health. |
| 0:43:05.250 | 2585.250 | CHIEF JUSTICE ROBERTS | FDA | I don't know why -- I don't know why it's impossible to have a label that fully complies with the FDA regulations and also happens to be misleading on the entirely different question of commercial competition, consumer confusion that has nothing to do with health. |
| 0:44:00.990 | 2640.990 | MS. SULLIVAN | label | Just to be clear, what Congress wanted was national uniformity so that a manufacturer could print one label and sell in the 50 states and not have its juice legal when you leave on the flight in California and illegal when you land in D.C. |
| 0:44:04.670 | 2644.670 | MS. SULLIVAN | juice | Just to be clear, what Congress wanted was national uniformity so that a manufacturer could print one label and sell in the 50 states and not have its juice legal when you leave on the flight in California and illegal when you land in D.C. |
| 0:44:32.900 | 2672.900 | MS. SULLIVAN | pomegranate | I'm saying after the NLEA express preemption provision, a state cannot say that pomegranate-blueberry-flavored blend of five juices -- which is perfectly consistent with the naming regulations, as the U.S. agrees. |
| 0:44:32.900 | 2672.900 | MS. SULLIVAN | blueberry | I'm saying after the NLEA express preemption provision, a state cannot say that pomegranate-blueberry-flavored blend of five juices -- which is perfectly consistent with the naming regulations, as the U.S. agrees. |
| 0:44:34.830 | 2674.830 | MS. SULLIVAN | five juices | I'm saying after the NLEA express preemption provision, a state cannot say that pomegranate-blueberry-flavored blend of five juices -- which is perfectly consistent with the naming regulations, as the U.S. agrees. |
| 0:44:35.030 | 2675.030 | MS. SULLIVAN | juice | I'm saying after the NLEA express preemption provision, a state cannot say that pomegranate-blueberry-flavored blend of five juices -- which is perfectly consistent with the naming regulations, as the U.S. agrees. |
| 0:44:46.750 | 2686.750 | MS. SULLIVAN | juice | Because the naming regulations, Justice Sotomayor, said, you can name your minority juice, your non-predominant juice in either of two ways. |
| 0:45:02.110 | 2702.110 | JUSTICE KENNEDY | label | You want us to -- you want us to write an opinion that said that Congress enacted a statutory scheme because it intended that no matter how misleading or how deceptive a label it is, if it passes the FDA, it cannot -- it -- there can be no liability. |
| 0:45:04.010 | 2704.010 | JUSTICE KENNEDY | FDA | You want us to -- you want us to write an opinion that said that Congress enacted a statutory scheme because it intended that no matter how misleading or how deceptive a label it is, if it passes the FDA, it cannot -- it -- there can be no liability. |
| 0:45:14.030 | 2714.030 | MS. SULLIVAN | FDA | We would want you to say that what misleading is when it is defined by FDA in specific regulations pursuant to a specific statute that specifically seeks national uniformity, in the sense that the manufacturer picks one label and doesn't, as the American Beverage Association brief says at Page 7, create a logistical nightmare that you have to change your label in response to every jury verdict. |
| 0:45:22.390 | 2722.390 | MS. SULLIVAN | label | We would want you to say that what misleading is when it is defined by FDA in specific regulations pursuant to a specific statute that specifically seeks national uniformity, in the sense that the manufacturer picks one label and doesn't, as the American Beverage Association brief says at Page 7, create a logistical nightmare that you have to change your label in response to every jury verdict. |
| 0:45:42.030 | 2742.030 | JUSTICE GINSBURG | consumers | And overwhelmingly, consumers said that they are misled, that they thought that they were getting pure pomegranate, and they were just astonished to find what they were getting was apple juice with, what Mr. Waxman told us, a dropper of blueberry. |
| 0:45:50.230 | 2750.230 | JUSTICE GINSBURG | pomegranate | And overwhelmingly, consumers said that they are misled, that they thought that they were getting pure pomegranate, and they were just astonished to find what they were getting was apple juice with, what Mr. Waxman told us, a dropper of blueberry. |
| 0:45:58.770 | 2758.770 | JUSTICE GINSBURG | juice | And overwhelmingly, consumers said that they are misled, that they thought that they were getting pure pomegranate, and they were just astonished to find what they were getting was apple juice with, what Mr. Waxman told us, a dropper of blueberry. |
| 0:46:05.330 | 2765.330 | JUSTICE GINSBURG | blueberry | And overwhelmingly, consumers said that they are misled, that they thought that they were getting pure pomegranate, and they were just astonished to find what they were getting was apple juice with, what Mr. Waxman told us, a dropper of blueberry. |
| 0:46:10.330 | 2770.330 | JUSTICE GINSBURG | consumers | Suppose -- suppose the reality is that consumers are misled. |
| 0:46:19.450 | 2779.450 | MS. SULLIVAN | FDA | If I suppose that, Your Honor, then the proper procedure for a consumer or a competitor is to go to the FDA and seek FDA's change of its rulemaking. |
| 0:46:33.810 | 2793.810 | MS. SULLIVAN | FDA | Your Honor, in the red addendum -- red brief addendum at Page 17(a) over to 18(a), you'll see that in 21 CFR 102.33(d) FDA said, Your juice will not be misleading if it uses the word "flavored." |
| 0:46:35.270 | 2795.270 | MS. SULLIVAN | juice | Your Honor, in the red addendum -- red brief addendum at Page 17(a) over to 18(a), you'll see that in 21 CFR 102.33(d) FDA said, Your juice will not be misleading if it uses the word "flavored." |
| 0:46:44.430 | 2804.430 | MS. SULLIVAN | label | And in fact, over on 18(a), if you want to see the closest thing to an express authorization of our label here, it's the example that FDA gave on 18(a). |
| 0:46:46.390 | 2806.390 | MS. SULLIVAN | FDA | And in fact, over on 18(a), if you want to see the closest thing to an express authorization of our label here, it's the example that FDA gave on 18(a). |
| 0:46:53.610 | 2813.610 | MS. SULLIVAN | consumers | Because we don't think that consumers are quite as unintelligent as POM must think they are. |
| 0:46:54.930 | 2814.930 | MS. SULLIVAN | unintelligent | Because we don't think that consumers are quite as unintelligent as POM must think they are. |
| 0:46:59.390 | 2819.390 | MS. SULLIVAN | five juices | They know when something is a favored blend of five juices, non-min- -- the non-predominant juices are just a flavor. |
| 0:46:59.630 | 2819.630 | MS. SULLIVAN | juice | They know when something is a favored blend of five juices, non-min- -- the non-predominant juices are just a flavor. |
| 0:47:04.930 | 2824.930 | JUSTICE KENNEDY | feel bad | Don't make me feel bad because I thought that this was pomegranate juice. |
| 0:47:06.990 | 2826.990 | JUSTICE KENNEDY | pomegranate | Don't make me feel bad because I thought that this was pomegranate juice. |
| 0:47:07.430 | 2827.430 | JUSTICE KENNEDY | juice | Don't make me feel bad because I thought that this was pomegranate juice. |
| 0:47:11.970 | 2831.970 | MS. SULLIVAN | pomegranate | Justice Kennedy -- Justice Kennedy, it's pomegranate-blueberry-flavored blend of five juices. |
| 0:47:11.970 | 2831.970 | MS. SULLIVAN | blueberry | Justice Kennedy -- Justice Kennedy, it's pomegranate-blueberry-flavored blend of five juices. |
| 0:47:15.570 | 2835.570 | MS. SULLIVAN | five juices | Justice Kennedy -- Justice Kennedy, it's pomegranate-blueberry-flavored blend of five juices. |
| 0:47:15.870 | 2835.870 | MS. SULLIVAN | juice | Justice Kennedy -- Justice Kennedy, it's pomegranate-blueberry-flavored blend of five juices. |
| 0:47:22.750 | 2842.750 | JUSTICE SCALIA | read | He sometimes doesn't read closely enough. |
| 0:47:26.360 | 2846.360 | MS. SULLIVAN | pomegranate | Yeah, pomegranate-blueberry-flavored blend of five juices. |
| 0:47:26.360 | 2846.360 | MS. SULLIVAN | blueberry | Yeah, pomegranate-blueberry-flavored blend of five juices. |
| 0:47:29.350 | 2849.350 | MS. SULLIVAN | five juices | Yeah, pomegranate-blueberry-flavored blend of five juices. |
| 0:47:29.530 | 2849.530 | MS. SULLIVAN | juice | Yeah, pomegranate-blueberry-flavored blend of five juices. |
| 0:47:35.590 | 2855.590 | JUSTICE SOTOMAYOR | FDA | Wyeth, the FDA actually approves, looks at the label and says, this one is okay. |
| 0:47:39.970 | 2859.970 | JUSTICE SOTOMAYOR | label | Wyeth, the FDA actually approves, looks at the label and says, this one is okay. |
| 0:47:56.150 | 2876.150 | JUSTICE SOTOMAYOR | label | Not only is it not misleading, but it complies with all health requirements, and because the producers of drugs have the ability to change the label without FDA approval, there was -- we found no preemptions and no impossibility. |
| 0:47:56.890 | 2876.890 | JUSTICE SOTOMAYOR | FDA | Not only is it not misleading, but it complies with all health requirements, and because the producers of drugs have the ability to change the label without FDA approval, there was -- we found no preemptions and no impossibility. |
| 0:48:05.190 | 2885.190 | JUSTICE SOTOMAYOR | FDA | The FDA here -- it's even worse, this case. |
| 0:48:07.470 | 2887.470 | JUSTICE SOTOMAYOR | FDA | The FDA doesn't approve the labels. |
| 0:48:08.950 | 2888.950 | JUSTICE SOTOMAYOR | label | The FDA doesn't approve the labels. |
| 0:48:24.170 | 2904.170 | MS. SULLIVAN | FDA | It's true that FDA doesn't pre-approve the label, but they couldn't have gotten closer here, Justice Kennedy, than solving your difficulty by saying that ras-cranberry juice, it's okay if you call it raspberry-and-cranberry-flavored juice drink. |
| 0:48:25.670 | 2905.670 | MS. SULLIVAN | label | It's true that FDA doesn't pre-approve the label, but they couldn't have gotten closer here, Justice Kennedy, than solving your difficulty by saying that ras-cranberry juice, it's okay if you call it raspberry-and-cranberry-flavored juice drink. |
| 0:48:32.450 | 2912.450 | MS. SULLIVAN | juice | It's true that FDA doesn't pre-approve the label, but they couldn't have gotten closer here, Justice Kennedy, than solving your difficulty by saying that ras-cranberry juice, it's okay if you call it raspberry-and-cranberry-flavored juice drink. |
| 0:48:55.690 | 2935.690 | MS. SULLIVAN | label | It is the express preemption provision here that says that Congress wanted nationally uniform labeling regulations whereby a manufacturer could pick one label and stick with it. |
| 0:49:02.610 | 2942.610 | JUSTICE SOTOMAYOR | label | You assume people would pick a label and stick with it. |
| 0:49:10.010 | 2950.010 | JUSTICE SOTOMAYOR | label | The Lanham Act would -- if a Lanham Act claim is bought, and it's upheld, you change the label nationally. |
| 0:49:14.110 | 2954.110 | MS. SULLIVAN | FDA | Oh, but, Your Honor, that's one thing if the FDA decides to adapt its rulemaking. |
| 0:49:17.945 | 2957.945 | MS. SULLIVAN | consumers | Suppose Justice Ginsberg's consumers or competitors showed up and said, Excuse me, we don't think ras-cranberry is clear enough. |
| 0:49:25.970 | 2965.970 | MS. SULLIVAN | FDA | When the FDA issues guidance or changes its rules or issues a new kind of interpretation, that's one agency speaking nationally. |
| 0:49:46.590 | 2986.590 | MS. SULLIVAN | juice | What Mr. Waxman wants to do is invite plaintiffs to walk into every court in the land under Lanham Act claims and create one jury saying, I think you should have called it apple-grape juice, and another saying you should have had the percentage. |
| 0:49:53.970 | 2993.970 | JUSTICE GINSBURG | FDA | Ms. Sullivan, I would like you to respond to this question: In the real world, the FDA has a tremendous amount of things on its plate, and labels for juices are not really high on its list. |
| 0:50:00.450 | 3000.450 | JUSTICE GINSBURG | label | Ms. Sullivan, I would like you to respond to this question: In the real world, the FDA has a tremendous amount of things on its plate, and labels for juices are not really high on its list. |
| 0:50:01.370 | 3001.370 | JUSTICE GINSBURG | juice | Ms. Sullivan, I would like you to respond to this question: In the real world, the FDA has a tremendous amount of things on its plate, and labels for juices are not really high on its list. |
| 0:50:11.830 | 3011.830 | JUSTICE GINSBURG | juice | You are asking us to take what it has said about juice as blessing this label, saying it's not misbranding, when its regulations aren't reviewed by the Court, when there is no private right of action, and say that that overtakes the Lanham Act. |
| 0:50:13.650 | 3013.650 | JUSTICE GINSBURG | label | You are asking us to take what it has said about juice as blessing this label, saying it's not misbranding, when its regulations aren't reviewed by the Court, when there is no private right of action, and say that that overtakes the Lanham Act. |
| 0:50:50.750 | 3050.750 | MS. SULLIVAN | FDA | Of course you don't want the FDA deciding is pomegranate-blueberry or ras-cranberry clear -- that's why they gave specific regulations. |
| 0:50:52.070 | 3052.070 | MS. SULLIVAN | pomegranate | Of course you don't want the FDA deciding is pomegranate-blueberry or ras-cranberry clear -- that's why they gave specific regulations. |
| 0:50:52.070 | 3052.070 | MS. SULLIVAN | blueberry | Of course you don't want the FDA deciding is pomegranate-blueberry or ras-cranberry clear -- that's why they gave specific regulations. |
| 0:50:59.690 | 3059.690 | MS. SULLIVAN | FDA | And contrary to what Mr. Waxman said, the FDA does not just have criminal jurisdiction. |
| 0:51:13.230 | 3073.230 | JUSTICE KENNEDY | FDA | But the point is that it is doubtful that FDA has sufficient resources to police food and beverage labeling. |
| 0:51:16.970 | 3076.970 | JUSTICE KENNEDY | label | But the point is that it is doubtful that FDA has sufficient resources to police food and beverage labeling. |
| 0:51:41.110 | 3101.110 | MS. SULLIVAN | FDA | What we would respectfully suggest you look at is not FDA's latest amicus brief through the U.S., but FDA's authoritative statement about whether its labeling regulations were being implemented. |
| 0:51:46.630 | 3106.630 | MS. SULLIVAN | label | What we would respectfully suggest you look at is not FDA's latest amicus brief through the U.S., but FDA's authoritative statement about whether its labeling regulations were being implemented. |
| 0:51:54.210 | 3114.210 | MS. SULLIVAN | FDA | In the red brief at Page 7, we cite to the rulemaking in which the FDA found after the three-year study -- remember the express preemption provision couldn't go into force until there was a three-year study by the IOM. |
| 0:52:06.690 | 3126.690 | MS. SULLIVAN | FDA | And if you look at Page 7 of the red brief, three-quarters of the way down the page, you'll see FDA in its authoritative statement, irrespective of its amicus brief here, found that 343(f), the presentation regulation, and 343(i), the naming regulation, were being adequately implemented. |
| 0:52:24.830 | 3144.830 | JUSTICE GINSBURG | FDA | So that's contrary to its current position, and I think we have to take it -- the FDA is -- is -- the government is representing the current FDA position. |
| 0:52:35.670 | 3155.670 | MS. SULLIVAN | FDA | But, Your Honor, you don't give our deference to an amicus brief when there's an authoritative prior statement by FDA that these implementation -- for the very reason you suggest, the FDA has other things to do. |
| 0:52:57.130 | 3177.130 | MS. SULLIVAN | FDA | We would respectfully suggest that just as it's too late for Mr. Waxman to change his theory, as you said in Riegel, to a -- we're enforcing the FDA theory -- and he doesn't purport to do it here -- it's -- the FDA, it's too late now to say in an amicus brief that they didn't mean it back in 1993. |
| 0:53:08.670 | 3188.670 | JUSTICE KAGAN | label | Do you think, Ms. Sullivan, that there are any Lanham suits regarding food labels that are allowable? |
| 0:53:46.010 | 3226.010 | MS. SULLIVAN | label | If there's something else that's not covered -- and I would refer Your Honor to -- specifically to religious dietary labeling, bottle container deposit labeling -- those are things that the FDA said in its rulemaking, based on the Congressional record, are outside the specific provisions with preemptive force. |
| 0:53:50.530 | 3230.530 | MS. SULLIVAN | FDA | If there's something else that's not covered -- and I would refer Your Honor to -- specifically to religious dietary labeling, bottle container deposit labeling -- those are things that the FDA said in its rulemaking, based on the Congressional record, are outside the specific provisions with preemptive force. |
| 0:54:22.810 | 3262.810 | MR. WAXMAN | FDA | First of all, this three-year study that she's referring to, as we pointed out in our brief, the IOM and the FDA made absolutely clear repeatedly in that study that they did not look at FDA's enforcement capabilities, its enforcement efforts. |
| 0:54:59.610 | 3299.610 | MR. WAXMAN | FDA | And the FD -- and the FDA itself has made clear, not only in its brief in this case and not only in its enforcement action in the Nestle case, but in the Federal Register discussion of the juice naming regulation, that the fact that the juice may comply -- and here it probably doesn't -- may comply with the naming convention does not mean that it is misleading. |
| 0:55:16.430 | 3316.430 | MR. WAXMAN | juice | And the FD -- and the FDA itself has made clear, not only in its brief in this case and not only in its enforcement action in the Nestle case, but in the Federal Register discussion of the juice naming regulation, that the fact that the juice may comply -- and here it probably doesn't -- may comply with the naming convention does not mean that it is misleading. |
| 0:55:29.170 | 3329.170 | MR. WAXMAN | FDA | The FDA said over and over again in that rulemaking that we strongly caution manufacturers that, in fact, mere compliance with this does not mean that the label is misleading and -- and that manufacturers are under an obligation to ensure that the label is not misleading. |
| 0:55:41.090 | 3341.090 | MR. WAXMAN | label | The FDA said over and over again in that rulemaking that we strongly caution manufacturers that, in fact, mere compliance with this does not mean that the label is misleading and -- and that manufacturers are under an obligation to ensure that the label is not misleading. |
| 0:56:15.070 | 3375.070 | MR. WAXMAN | juice | And also, indeed said, nonetheless, we encourage manufacturers to name all of the juices in a multiple juice product specifically because it was concerned about this. |
| 0:56:46.930 | 3406.930 | MR. WAXMAN | label | This is -- the closest cognate here is 343(a), which provides that a food is misbranded if it is false -- if the label is false and -- false or misleading at any particular. |
| 0:57:23.530 | 3443.530 | MR. WAXMAN | FDA | The FDA wasn't worried here about health or safety. |
| 0:57:36.070 | 3456.070 | MR. WAXMAN | juice | It's because there were concerns about health and safety with this juice naming regulation that they said, in the exercise of our sovereign enforcement authority, we are not going to go after you for complying with this naming convention, because, as they've explained, we don't know anything about how to protect competitors. |
| 0:58:22.610 | 3502.610 | JUSTICE KAGAN | FDA | But, Mr. Waxman, I take it that Ms. Sherry said that the FDA views itself as having a job beyond health and safety, that they view themselves as at least -- not thinking about competitors' welfare or lack thereof, but at least thinking about consumer understanding of labels. |
| 0:58:34.870 | 3514.870 | JUSTICE KAGAN | label | But, Mr. Waxman, I take it that Ms. Sherry said that the FDA views itself as having a job beyond health and safety, that they view themselves as at least -- not thinking about competitors' welfare or lack thereof, but at least thinking about consumer understanding of labels. |
| 0:59:08.870 | 3548.870 | MR. WAXMAN | FDA | But the former is not what the Lanham Act is about, and the latter, the FDA has made perfectly clear is not what the FDCA is about. |
| 0:59:53.430 | 3593.430 | MR. WAXMAN | FDA | They're asking as -- their submission here is not -- not -- not just in an FDA action, enforcement action in court, will we get chevron deference for our interpretation of what the meaning of 343(i)(1) is. |
| 1:00:32.350 | 3632.350 | JUSTICE KENNEDY | FDA | Any authority that the FDA interpretation gets deference is presumed to be correct, or presumed to be not misleading? |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.480 to 0:03:07.480, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.480] MR. WAXMAN: Mr. Chief Justice, and may it please the Court: The Lanham Act provides a remedy for businesses whose market is misappropriated by competitors that misrepresent the character of the goods they sell. This case presents an egregious violation of the law. Coca-Cola's label grossly misleads consumers , as Coke anticipated, but Coke says that it need not answer under the Lanham Act because its label is authorized by FDA regulations. The label is not, in fact, authorized for reasons we explain and with which the United States largely agrees, but even if it were consistent with FDA regulations that would not strip POM of its right to prove a willful Lanham Act violation. Courts are obligated to give full effect to Congressional enactments wherever possible. Here Congress has never precluded or conditioned enforcement of the Lanham Act in food labeling cases, and it is entirely possible, in fact, entirely easy for Coke to comply with both statutory obligations.

[0:01:18.940] JUSTICE SOTOMAYOR: If there is no private cause of action to enforce the FDA label standards, only the FDA can bring a proceeding to say that an ad violates its regulations, how does a Court below, without interpreting the regulations, go about deciding whether or not a particular ad doesn't comport with the regulations and hence would be subject to the Lanham Act?

[0:01:51.840] MR. WAXMAN: Justice --

[0:01:52.220] JUSTICE SOTOMAYOR: Maybe that's a better question for the SG, but I'm trying to figure out --

[0:01:56.540] MR. WAXMAN: Well, let me take a shot at it and, you know, the SG can and Ms. Sullivan can, as well. There's no question under -- as this Court explained in Buckman, that there is no private cause of action to enforce provisions of the FDCA. Now, this Court in Buckman distinguished Medtronic v. Lohr, which provided and held -- and did not and save from preemption a state law that was- that imposed parallel requirements, and in that instance, and this is not a case involving an attempt to enforce parallel requirements under state law or any other law. In those circumstances, as the government explains, of course a court is going to be required to ascertain what those parallel requirements are, and whether they were or weren’t complied with. But this is a case involving a different statute. Our submission is that it is entirely irrelevant whether or not the Coke label, in any particular, is consistent with a regulation that implements criminal

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 12, 2014.

- Oyez page: https://www.oyez.org/cases/2013/12-761
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2013/12-761/20140612o_12-761.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.1 MB)
- Length: 0:04:13.518 (253.518 s)
- Words: 583, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
  Oyez lists no names for 2 of these turns, so they come from the text: a turn that opens "Justice X has our opinion" is the Chief Justice introducing the case, and the next turn is Justice X.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 539 of Whisper's 583 words (92.5%; Oyez has 581).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.320 | 13 |
| JUSTICE KENNEDY | 0:00:07.340 | 0:04:12.860 | 557 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kennedy, has our opinion Case 12-761, Palm Wonderful v. The Coca-Cola Company?

[0:00:07.340] JUSTICE KENNEDY: This is a case about the intersection of two Federal statutes. The first is the Lanham Act. The second is the Federal Food, Drug and Cosmetic Act, also known as the FDCA. The Lanham Act allows certain commercial interests, including competitors, to sue for unfair competition from false or misleading product descriptions. The FDCA, the second act, forbids the misbranding of food and beverages. This includes use, prohibition on use, of false or misleading labeling. There are regulations implementing the FDCA. These regulations include requirements regarding the labeling of beverages composed of multiple juices, referred to often as juice blends. Both parties in this case make juice blends. The Petitioner is Palm Wonderful LLC. Palm makes and sells a pomegranate blueberry juice blend. One of Palm's competitors is the respondent, the Coca-Cola Company. Coca-Cola's Minute Maid Division sells a juice blend with a label that displays the words pomegranate blueberry with far more prominence than the other words on the label. But on close reading, it's disclosed that the juice is a blend of five juices, and in truth, the Coca-Cola product contains but 0.3 percent pomegranate juice and 0.2 percent blueberry juice. Palm sued Coca-Cola under the Lanham Act. Palm alleged that the label for the Coca-Cola juice blend is deceptive and misleading. The Court of Appeals held that the FDCA entrusts matters of juice blending to the expert judgment of the Food and Drug Administration. That agency has not forbidden Coca-Cola's label. So the Court of Appeals for the Ninth Circuit held that Palm's Lanham Act claim is precluded or barred by the FDCA. The Court of Appeals' conclusion was incorrect. Neither the Lanham Act nor the FDCA in express terms forbids Lanham Act claims challenging labels that are regulated by the FDCA. The Lanham Act and the FDCA have coexisted since 1946. If Congress had concluded that Lanham Act suits could interfere with the FDCA, it might well have enacted a provision addressing the issue during these 70 years, and it has not done so. The structures of the FDCA and the Lanham Act reinforce the conclusion we draw from the text. The Lanham Act and the FDCA complement each other in major respects.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:01.860 | (nothing) | in |
| 0:00:02.200 | 12 -761, Palm | 12-761, POM |
| 0:00:22.520 | interests, | interest |
| 0:01:04.360 | Palm | POM |
| 0:01:07.600 | Palm | POM |
| 0:01:13.080 | Palm's | POM's |
| 0:01:32.460 | (nothing) | -- on |
| 0:01:36.050 | (nothing) | it -- |
| 0:01:40.860 | (nothing) | juice -- |
| 0:01:45.160 | but 0 .3 percent | about 0.3% |
| 0:01:48.480 | 0 .2 percent | 0.2% |
| 0:01:51.620 | Palm | POM |
| 0:01:54.320 | Palm | POM |
| 0:02:02.740 | entrusts | entrust |
| 0:02:13.700 | Palm's | POM's |
| 0:02:43.160 | (nothing) | -- it might well |
| 0:02:43.660 | a | the |
| 0:02:45.380 | these | the |
| 0:03:05.160 | interests | interest |
| 0:03:49.800 | (nothing) | had |
| 0:03:51.840 | trick | tricked |
| 0:04:02.900 | Palm's | POM's |
