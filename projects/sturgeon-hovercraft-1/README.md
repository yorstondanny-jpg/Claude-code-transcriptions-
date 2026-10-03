# sturgeon-hovercraft-1: Supreme Court No. 14-1209

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2015/14-1209
- Audio: https://www.supremecourt.gov/media/audio/mp3files/14-1209.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2015/14-1209_jqei.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 66 min on 4 CPU cores
- Audio length: 1:02:00.777 (3720.777 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.8 MB
- Official words: 10717 (plus 8 `(Laughter.)` markers), in 315 speaker turns
- ASR words: 10657
- Official words matched to an ASR word: 10090 of 10717 (**94.15%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.15% (threshold 85%).

316 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 25 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 2
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 14-1209 2015 sturgeon-hovercraft-1 --model medium.en --opinion --mentions "hovercraft,moose,Sturgeon,river,Nation River,Alaska,ANILCA,park,ranger,navigable,waters,regulation,statute,drafted,section,public lands,Yukon" --long-questions 10

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE BREYER, 0:27:17.220 to 0:28:36.600 (79.4 s, 211 words)

> As I read it -- as I read it, it's complicated, but in a sense it's simple. Yosemite has some private land within it and a lot of public. You know, there's some houses in Yosemite owned by private people. There are interior regs that apply to all of Yosemite, such as certain fireplace regs. There are some that only apply to the park but not the private people. What this statute says is the latter. Doesn't deprive -- apply to that land that you gave to Alaska. That's what the statute says. And what the reg says is that our hovercraft reg applies to everything within Yosemite, if this were Yosemite. This navigable waters, whether the land around it is owned by James Jones, the private person, or whether it's owned -- whether it's part of Yosemite Park. That's what it seemed to say to me. Now, there are two problems with what I just read. One is the third sentence and the word "unit." And the second problem is the NPS, the National Park Service, is it really all of Yosemite, you know, with that private thing or is it just the public part? Now, that's at least a sorry. I shouldn't have got into it. It's too complicated. Skip the question. (Laughter.)

### 2. JUSTICE SCALIA, 0:39:49.860 to 0:41:06.380 (76.5 s, 173 words)

> Let's -- let's talk about your authority. I don't even get to the second sentence. I just get to the first sentence. The authority of the Park Service comes from the statute which authorizes the Secretary of Interior to, quote, "prescribe such regulations necessary or proper for the use and management of system units, including those concerning boating and other activities. Only here the CSU's are park system units." That's 13.013(c). As a result, non-Federal holdings unambiguously fall outside the scope of the Secretary's authority because of the first sentence. "Only those lands within the boundaries of any conservation system unit which are public lands as such term is defined in this Act shall be deemed to be included as a portion of such unit." If it's not within the unit, it's not within the basic authority of the Park Service to issue regulations, period. So you -- you have to show that -- I think the Federal government holds title to the water. I don't think you can show. Nobody holds title to the water.

### 3. JUSTICE BREYER, 0:11:51.640 to 0:13:00.380 (68.7 s, 174 words)

> And then once you have that, you have this regulation applying to this portion of the river. So now we look to the statute to see if anything there takes away what the regulations seem to give. And the only part of the statute -- though it's an important part -- that supports you is the second sentence. But as I read that second sentence, it says that, "The regulations that apply solely to public lands within such units," you see, "are the ones that don't apply to the private land up in Yukon-Charley. But I've just read you a regulation, which, on my reading of it, is the Hovercraft Regulation, and does not apply solely to public lands within National Park Service units, either in Alaska or anywhere else. And therefore, the statute doesn't stop it. Now, that's -- that's -- and I want to -- I don't know if I can do this orally; I just tried to, which is to put the argument against you as best I could, and I want to hear the reply.

### 4. JUSTICE KAGAN, 0:24:31.240 to 0:25:24.400 (53.2 s, 156 words)

> And I guess part of my question about this is, I look at that map, you know, and that map of this area has all this green land, which green represents real Federal park land, and there's a river that runs through it. And -- and you're saying that that river that runs through the park land, and nobody can do anything on -- or the Feds can't do anything on? I mean, this isn't the inholdings. I mean, I can understand the argument with respect to the inholdings and the rivers that are running through the inholdings. But this is the rivers that are running through the park land. Now, it seems to me a very strange thing that Congress would have created Federal lands in a Federal park land but said that the Federal Park Service can't have anything to do with the rivers. The rivers are like an important part of the park, aren't they?

### 5. JUSTICE ALITO, 0:38:19.720 to 0:39:05.680 (46.0 s, 106 words)

> Well, you -- you want to talk about waters, and -- and after this question I won't say anything more on this, but is the Ninth Circuit's holding limited to waters? The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. And since these are not Alaska-specific, those -- those regulations apply. So they understand it to apply to something more than just navigable waters.

### 6. JUSTICE SOTOMAYOR, 0:07:21.760 to 0:08:07.340 (45.6 s, 90 words)

> Your reading on a practical basis with respect to the navigable waters makes almost no sense to me. I'm looking at a map attached to the petition of the State of Alaska. It's attached to the end of the brief. And it seems like these national parks are spread along the coast of Alaska in a haphazard way, meaning the national parks have jurisdiction over a small strip along the coast of Alaska. Presumably you're not arguing that this agreement controls the U.S. servitude of navigable waters around those strips.

### 7. JUSTICE BREYER, 0:10:46.960 to 0:11:28.860 (41.9 s, 96 words)

> Well, now, you look at what they say about that, and you get, when they're defining the Yukon-Charley River's National Preserve, it says that that national preserve -- which is the whole thing, which includes the section of the river that we're talking about -- contains public lands. It doesn't say it's identical with the public lands. And then in another place it says, "Only those lands within the portion which are public lands shall be deemed to be included a portion of such unit," not that they make up the whole of such unit. At least we --

### 8. JUSTICE BREYER, 0:42:14.380 to 0:42:55.440 (41.1 s, 130 words)

> I read that first sentence. It's very interesting, because the tone of voice is the only way I can deal with this case. Watch. Imagine we have a valley that's a public land, and that valley traverses the boundary of the unit. Some of it's inside and some of it's outside. Now, only those lands within the boundaries of any conservation system which are public -- within the boundaries of any conservation system which are public lands shall be deemed to be included as a portion of the unit. So the only part of that valley that it's a portion of the unit is that part of the valley that's within the boundary of the unit. The part that's outside the boundary of the unit is not part of the unit.

### 9. JUSTICE ALITO, 0:29:59.020 to 0:30:36.800 (37.8 s, 106 words)

> Well, before you get to that, could we begin with what the Ninth Circuit decided? You're entitled to defend the judgment on any ground that you like, but -- that was presented below, but the only issue we have to -- we have to reach is the correctness of the Ninth Circuit's decision. Now, I understand what the Ninth Circuit to have held, to be this, that the hovercraft rule is not barred by the second sentence of Section 103(c) of ANILCA, because the hovercraft rule does not apply only in Alaska, because it applies throughout the country. Is that -- that's a correct understanding of what they held?

### 10. JUSTICE KAGAN, 0:46:05.780 to 0:46:40.620 (34.8 s, 92 words)

> And if I'm looking at the right section, I mean, I would have thought that that was key to your argument, because it says in these management plans what you need is a -- is a "description of privately owned areas which are within such unit." So it's clearly contemplating that there are these private areas that are within the unit. And then as you say, it goes on and says we want in these plans some idea of what regulations are going to be applying on those private lands within the unit.

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-53.6 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:11:38.440 | 698.440 | medium | 0.92 | 0.80 | 29.1 | 32.9 | we -- What are -- what are you quoting from? I'm -- I'm quoting from regulations which are 54 U.S.C. -- I don't know. I'll -- I'll have to show you later, because I'm quoting -- |
| 2 | 0:11:45.520 | 705.520 | big | 1.48 | 1.35 | 34.1 | 42.4 | to show you later, because I'm quoting -- We're going to get into numbers, and I -- I just thought this case is too complicated to ask anything, but you've tempted me. |
| 3 | 0:16:55.560 | 1015.560 | small | 0.48 | 0.30 | 23.6 | 30.2 | do that for me. It may not have been the perfect way for Congress to go about and do it, but that's -- Well, tell me the imperfect way. Well, "solely." |
| 4 | 0:28:36.600 | 1716.600 | small | 0.36 | 0.05 | 8.9 | 13.5 | know, with that private thing or is it just the public part? Now, that's at least a sorry. I shouldn't have got into it. It's too complicated. Skip the question. |
| 5 | 0:31:45.060 | 1905.060 | big | 1.60 | 1.45 | 25.9 | 33.1 | based its decision on until page 49, and you devoted exactly a paragraph to it. And why don't you concede that it's wrong? It's a ridiculous interpretation, is it not? |
| 6 | 0:45:00.200 | 2700.200 | under speech | 0.12 | 0.00 | - | - | it is a statute. It's the Act of 1976. I understand that the numbering is -- it's an unusually high -- It's not the numbering. It's -- it says regulations -- oh, I see. |
| 7 | 0:55:36.100 | 3336.100 | under speech | 0.00 | 0.00 | - | - | the park. So you're saying it applies within -- it is within the boundaries of the unit, although the unit consists of just the public land. Who drafted this? This is -- |
| 8 | 0:58:03.400 | 3483.400 | medium | 3.58 | 0.80 | 16.9 | 28.5 | This regulation is a rule that's been written to apply, regardless of who owns the lands in the parks. It's an exercise of our narrow authority -- No. That's you winning. |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| hovercraft | 19 | 20 |
| moose | 0 | 0 |
| Sturgeon | 5 | 5 |
| river | 33 | 41 |
| Nation River | 1 | 1 |
| Alaska | 37 | 46 |
| ANILCA | 31 | 33 |
| park | 127 | 166 |
| ranger | 0 | 0 |
| navigable | 43 | 44 |
| waters | 74 | 80 |
| regulation | 83 | 95 |
| statute | 51 | 59 |
| drafted | 1 | 1 |
| section | 26 | 26 |
| public lands | 44 | 47 |
| Yukon | 5 | 5 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:03.800 | 3.800 | CHIEF JUSTICE ROBERTS | Sturgeon | We'll hear argument next in Case 14-1209, Sturgeon v. Frost. |
| 0:00:11.000 | 11.000 | MR. FINDLEY | ANILCA | Thank you, Mr. Chief Justice, and may it please the Court: ANILCA was the result of a grand bargain. |
| 0:00:15.100 | 15.100 | MR. FINDLEY | ANILCA | Congress enacted ANILCA to finally resolve land ownership in Alaska, a process that began with the Statehood Act and continued with the Native Claims Settlement Act, both statutes that granted land to the State and native corporations to further economic development and self-sufficiency for Alaska and its people. |
| 0:00:18.140 | 18.140 | MR. FINDLEY | Alaska | Congress enacted ANILCA to finally resolve land ownership in Alaska, a process that began with the Statehood Act and continued with the Native Claims Settlement Act, both statutes that granted land to the State and native corporations to further economic development and self-sufficiency for Alaska and its people. |
| 0:00:25.180 | 25.180 | MR. FINDLEY | statute | Congress enacted ANILCA to finally resolve land ownership in Alaska, a process that began with the Statehood Act and continued with the Native Claims Settlement Act, both statutes that granted land to the State and native corporations to further economic development and self-sufficiency for Alaska and its people. |
| 0:00:34.620 | 34.620 | MR. FINDLEY | ANILCA | ANILCA very carefully balanced conservation with those important goals. |
| 0:00:47.780 | 47.780 | JUSTICE KAGAN | navigable | Your argument applies to the navigable rivers generally; is that right? |
| 0:00:48.320 | 48.320 | JUSTICE KAGAN | river | Your argument applies to the navigable rivers generally; is that right? |
| 0:00:52.280 | 52.280 | JUSTICE KAGAN | navigable | In other words, to the navigable rivers running through the federally owned land as well as to those running through the inholdings? |
| 0:00:52.800 | 52.800 | JUSTICE KAGAN | river | In other words, to the navigable rivers running through the federally owned land as well as to those running through the inholdings? |
| 0:01:00.860 | 60.860 | MR. FINDLEY | navigable | If a navigable river is surrounded by the outer boundaries of the park, yes, that's covered by Section 103(c). |
| 0:01:01.200 | 61.200 | MR. FINDLEY | river | If a navigable river is surrounded by the outer boundaries of the park, yes, that's covered by Section 103(c). |
| 0:01:03.360 | 63.360 | MR. FINDLEY | park | If a navigable river is surrounded by the outer boundaries of the park, yes, that's covered by Section 103(c). |
| 0:01:04.760 | 64.760 | MR. FINDLEY | section | If a navigable river is surrounded by the outer boundaries of the park, yes, that's covered by Section 103(c). |
| 0:01:27.420 | 87.420 | MR. FINDLEY | hovercraft | On either side of where his hovercraft was stopped was Federal public land. |
| 0:01:39.640 | 99.640 | JUSTICE KENNEDY | navigable | Is it conceded by all or is it not that this is navigable -- that these are navigable waters? |
| 0:01:41.420 | 101.420 | JUSTICE KENNEDY | waters | Is it conceded by all or is it not that this is navigable -- that these are navigable waters? |
| 0:01:45.060 | 105.060 | MR. FINDLEY | Alaska | And the Ninth Circuit issued decision in 2001 called Alaska v. United States by Judge Kleinfeld which adjudicated the Nation River navigable. |
| 0:01:48.120 | 108.120 | MR. FINDLEY | Nation River | And the Ninth Circuit issued decision in 2001 called Alaska v. United States by Judge Kleinfeld which adjudicated the Nation River navigable. |
| 0:01:48.340 | 108.340 | MR. FINDLEY | river | And the Ninth Circuit issued decision in 2001 called Alaska v. United States by Judge Kleinfeld which adjudicated the Nation River navigable. |
| 0:01:48.600 | 108.600 | MR. FINDLEY | navigable | And the Ninth Circuit issued decision in 2001 called Alaska v. United States by Judge Kleinfeld which adjudicated the Nation River navigable. |
| 0:01:56.380 | 116.380 | JUSTICE SOTOMAYOR | hovercraft | So you're claiming a right not merely to use the hovercraft in the nonpublic lands. |
| 0:02:04.800 | 124.800 | JUSTICE SOTOMAYOR | navigable | You're claiming that there's no residual right to control navigable waters in the Federal lands area? |
| 0:02:05.420 | 125.420 | JUSTICE SOTOMAYOR | waters | You're claiming that there's no residual right to control navigable waters in the Federal lands area? |
| 0:02:09.340 | 129.340 | MR. FINDLEY | Sturgeon | What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks. |
| 0:02:12.660 | 132.660 | MR. FINDLEY | park | What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks. |
| 0:02:16.640 | 136.640 | MR. FINDLEY | regulation | What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks. |
| 0:02:18.340 | 138.340 | MR. FINDLEY | navigable | What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks. |
| 0:02:18.800 | 138.800 | MR. FINDLEY | waters | What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks. |
| 0:02:20.580 | 140.580 | MR. FINDLEY | ANILCA | What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks. |
| 0:02:23.940 | 143.940 | JUSTICE SOTOMAYOR | ANILCA | So what do you do about the ANILCA provision that says that boating and other water activities within public lands, within Federal public lands can be regulated? |
| 0:02:30.280 | 150.280 | JUSTICE SOTOMAYOR | public lands | So what do you do about the ANILCA provision that says that boating and other water activities within public lands, within Federal public lands can be regulated? |
| 0:02:38.520 | 158.520 | MR. FINDLEY | waters | And those apply to all kinds of waters that are not navigable. |
| 0:02:39.740 | 159.740 | MR. FINDLEY | navigable | And those apply to all kinds of waters that are not navigable. |
| 0:02:41.840 | 161.840 | MR. FINDLEY | waters | Those apply to Federal waters and those -- |
| 0:02:45.020 | 165.020 | JUSTICE SOTOMAYOR | waters | It says any waters in the jurisdiction of the United States. |
| 0:02:48.960 | 168.960 | MR. FINDLEY | navigable | It doesn't say navigable waters. |
| 0:02:49.740 | 169.740 | MR. FINDLEY | waters | It doesn't say navigable waters. |
| 0:02:55.020 | 175.020 | JUSTICE SOTOMAYOR | navigable | What says it excludes navigable waters? |
| 0:02:55.720 | 175.720 | JUSTICE SOTOMAYOR | waters | What says it excludes navigable waters? |
| 0:02:58.260 | 178.260 | MR. FINDLEY | public lands | You turn back to the definition of public lands in the statute, which makes clear for anything to be public lands, the United States must hold title. |
| 0:02:59.200 | 179.200 | MR. FINDLEY | statute | You turn back to the definition of public lands in the statute, which makes clear for anything to be public lands, the United States must hold title. |
| 0:03:09.580 | 189.580 | MR. FINDLEY | navigable | The United States does not hold title to the submerged lands or the navigable waters. |
| 0:03:10.040 | 190.040 | MR. FINDLEY | waters | The United States does not hold title to the submerged lands or the navigable waters. |
| 0:03:11.500 | 191.500 | MR. FINDLEY | navigable | So those navigable waters, they aren't public lands. |
| 0:03:11.920 | 191.920 | MR. FINDLEY | waters | So those navigable waters, they aren't public lands. |
| 0:03:12.760 | 192.760 | MR. FINDLEY | public lands | So those navigable waters, they aren't public lands. |
| 0:03:14.240 | 194.240 | MR. FINDLEY | section | Section 103(c) makes crystal clear they're not part of the park and they are not subject to regulations solely enacted to manage our claim. |
| 0:03:17.340 | 197.340 | MR. FINDLEY | park | Section 103(c) makes crystal clear they're not part of the park and they are not subject to regulations solely enacted to manage our claim. |
| 0:03:18.980 | 198.980 | MR. FINDLEY | regulation | Section 103(c) makes crystal clear they're not part of the park and they are not subject to regulations solely enacted to manage our claim. |
| 0:04:08.360 | 248.360 | JUSTICE SCALIA | park | So it -- it -- it may well be, you think, that the Federal government would have authority to do this in the exercise of its navigational servitude even though it doesn't have authority to do it, as you assert, under the Park Service? |
| 0:04:11.200 | 251.200 | MR. FINDLEY | park | Our objection is to the Park Service asserting its regulation on these navigable waters. |
| 0:04:12.940 | 252.940 | MR. FINDLEY | regulation | Our objection is to the Park Service asserting its regulation on these navigable waters. |
| 0:04:14.120 | 254.120 | MR. FINDLEY | navigable | Our objection is to the Park Service asserting its regulation on these navigable waters. |
| 0:04:14.540 | 254.540 | MR. FINDLEY | waters | Our objection is to the Park Service asserting its regulation on these navigable waters. |
| 0:04:18.840 | 258.840 | MR. FINDLEY | park | Our position is Congress expressly denied this authority to the Park Service in 103(c). |
| 0:04:23.540 | 263.540 | JUSTICE SCALIA | park | Whether if the Park Service can't do it somebody else can do it? |
| 0:04:30.760 | 270.760 | MR. FINDLEY | ANILCA | I mean, ANILCA makes crystal clear that Federal government is not bereft of authority over navigable waters. |
| 0:04:35.380 | 275.380 | MR. FINDLEY | navigable | I mean, ANILCA makes crystal clear that Federal government is not bereft of authority over navigable waters. |
| 0:04:35.800 | 275.800 | MR. FINDLEY | waters | I mean, ANILCA makes crystal clear that Federal government is not bereft of authority over navigable waters. |
| 0:04:44.880 | 284.880 | MR. FINDLEY | ANILCA | The specific issue here was you -- you had pockets of land that were about to be surrounded by these new ANILCA CSUs. |
| 0:04:46.600 | 286.600 | MR. FINDLEY | navigable | Those included State navigable waters, and that included over 40 percent of the native corporation land selections under the Native Corporation Settlement Act. |
| 0:04:47.060 | 287.060 | MR. FINDLEY | waters | Those included State navigable waters, and that included over 40 percent of the native corporation land selections under the Native Corporation Settlement Act. |
| 0:04:56.260 | 296.260 | MR. FINDLEY | park | The concern was whoa, if you're about to surround us with these parks, we don't want to be part of the parks and we don't want to be subject to park regulation. |
| 0:04:59.960 | 299.960 | MR. FINDLEY | regulation | The concern was whoa, if you're about to surround us with these parks, we don't want to be part of the parks and we don't want to be subject to park regulation. |
| 0:05:02.100 | 302.100 | MR. FINDLEY | park | The idea was if you weren't part of the park, you weren't subject to park regulation the day before ANILCA was enacted, and that status quo carries through after ANILCA was enacted. |
| 0:05:03.340 | 303.340 | MR. FINDLEY | regulation | The idea was if you weren't part of the park, you weren't subject to park regulation the day before ANILCA was enacted, and that status quo carries through after ANILCA was enacted. |
| 0:05:04.500 | 304.500 | MR. FINDLEY | ANILCA | The idea was if you weren't part of the park, you weren't subject to park regulation the day before ANILCA was enacted, and that status quo carries through after ANILCA was enacted. |
| 0:05:09.480 | 309.480 | JUSTICE KENNEDY | regulation | Suppose you have a regulation or a statute that's applicable to all United States parks. |
| 0:05:11.020 | 311.020 | JUSTICE KENNEDY | statute | Suppose you have a regulation or a statute that's applicable to all United States parks. |
| 0:05:13.800 | 313.800 | JUSTICE KENNEDY | park | Suppose you have a regulation or a statute that's applicable to all United States parks. |
| 0:05:17.520 | 317.520 | MR. FINDLEY | regulation | If it's a regulation that the Park Service -- |
| 0:05:18.360 | 318.360 | MR. FINDLEY | park | If it's a regulation that the Park Service -- |
| 0:05:21.660 | 321.660 | JUSTICE KENNEDY | statute | No, let's say -- let's say first it's a statute, suppose a Federal statute. |
| 0:05:27.660 | 327.660 | JUSTICE KENNEDY | park | So you need a permit for a fire in a Federal park. |
| 0:05:31.960 | 331.960 | MR. FINDLEY | regulation | You have to look at whether this is a regulation that was solely enacted to manage park land. |
| 0:05:33.840 | 333.840 | MR. FINDLEY | park | You have to look at whether this is a regulation that was solely enacted to manage park land. |
| 0:05:35.800 | 335.800 | MR. FINDLEY | hovercraft | The hovercraft regulation we have here, it's crystal clear. |
| 0:05:36.240 | 336.240 | MR. FINDLEY | regulation | The hovercraft regulation we have here, it's crystal clear. |
| 0:05:39.740 | 339.740 | MR. FINDLEY | regulation | That's exactly that type of regulation where the Park Service made a judgment call about what it believed was appropriate or not appropriate to occur on public land. |
| 0:05:40.460 | 340.460 | MR. FINDLEY | park | That's exactly that type of regulation where the Park Service made a judgment call about what it believed was appropriate or not appropriate to occur on public land. |
| 0:05:47.360 | 347.360 | MR. FINDLEY | park | If the Park Service -- this is a Park Service regulation issued under the Organic Act and you read this code of Federal regulations and the Park Service is saying, we want fires here on public lands; we want fires here not on public lands. |
| 0:05:48.740 | 348.740 | MR. FINDLEY | regulation | If the Park Service -- this is a Park Service regulation issued under the Organic Act and you read this code of Federal regulations and the Park Service is saying, we want fires here on public lands; we want fires here not on public lands. |
| 0:05:55.400 | 355.400 | MR. FINDLEY | public lands | If the Park Service -- this is a Park Service regulation issued under the Organic Act and you read this code of Federal regulations and the Park Service is saying, we want fires here on public lands; we want fires here not on public lands. |
| 0:05:59.220 | 359.220 | MR. FINDLEY | regulation | That's the type of regulation Section 103(c) is talking about. |
| 0:05:59.680 | 359.680 | MR. FINDLEY | section | That's the type of regulation Section 103(c) is talking about. |
| 0:06:10.520 | 370.520 | MR. FINDLEY | regulation | If the EPA says, look, we're concerned about Clean Air Act emissions from fire smoke and we are going to issue a generally applicable regulation across the United States on when you can burn wood and when you can't, that is not the type of regulation that Section 103(c) reaches. |
| 0:06:15.860 | 375.860 | MR. FINDLEY | section | If the EPA says, look, we're concerned about Clean Air Act emissions from fire smoke and we are going to issue a generally applicable regulation across the United States on when you can burn wood and when you can't, that is not the type of regulation that Section 103(c) reaches. |
| 0:06:21.580 | 381.580 | JUSTICE ALITO | navigable | Was it limited to navigable waters? |
| 0:06:22.060 | 382.060 | JUSTICE ALITO | waters | Was it limited to navigable waters? |
| 0:06:25.100 | 385.100 | MR. FINDLEY | waters | The Ninth Circuit did not reach the unnavigable waters issues at all. |
| 0:06:30.920 | 390.920 | MR. FINDLEY | statute | The Ninth Circuit took a very strained, improper reading of the statute and looked at Section 103(c) and said, well, it only applies to Alaska-specific regulations. |
| 0:06:32.340 | 392.340 | MR. FINDLEY | section | The Ninth Circuit took a very strained, improper reading of the statute and looked at Section 103(c) and said, well, it only applies to Alaska-specific regulations. |
| 0:06:35.780 | 395.780 | MR. FINDLEY | Alaska | The Ninth Circuit took a very strained, improper reading of the statute and looked at Section 103(c) and said, well, it only applies to Alaska-specific regulations. |
| 0:06:36.680 | 396.680 | MR. FINDLEY | regulation | The Ninth Circuit took a very strained, improper reading of the statute and looked at Section 103(c) and said, well, it only applies to Alaska-specific regulations. |
| 0:06:39.320 | 399.320 | MR. FINDLEY | statute | And it was a reading that reads the statute out of context. |
| 0:06:51.600 | 411.600 | MR. FINDLEY | park | It's contrary to the text and leads to an incredibly absurd result that, frankly, no -- there's evidence Congress thought this is what was going to happen was that these islands of non-Federal land that were excluded from the parks, under the Ninth Circuit's ruling, they cannot take advantage of all of the rules in Alaska that Congress specifically loosened for Alaska parks. |
| 0:06:57.100 | 417.100 | MR. FINDLEY | Alaska | It's contrary to the text and leads to an incredibly absurd result that, frankly, no -- there's evidence Congress thought this is what was going to happen was that these islands of non-Federal land that were excluded from the parks, under the Ninth Circuit's ruling, they cannot take advantage of all of the rules in Alaska that Congress specifically loosened for Alaska parks. |
| 0:07:00.880 | 420.880 | MR. FINDLEY | Alaska | You can camp in Alaska parks. |
| 0:07:01.240 | 421.240 | MR. FINDLEY | park | You can camp in Alaska parks. |
| 0:07:17.560 | 437.560 | MR. FINDLEY | Alaska | Instead, that non-Federal land is subject to the more restrictive nationwide rules that were not promulgated to be tailored to Alaska. |
| 0:07:27.200 | 447.200 | JUSTICE SOTOMAYOR | navigable | Your reading on a practical basis with respect to the navigable waters makes almost no sense to me. |
| 0:07:27.720 | 447.720 | JUSTICE SOTOMAYOR | waters | Your reading on a practical basis with respect to the navigable waters makes almost no sense to me. |
| 0:07:35.200 | 455.200 | JUSTICE SOTOMAYOR | Alaska | I'm looking at a map attached to the petition of the State of Alaska. |
| 0:07:43.040 | 463.040 | JUSTICE SOTOMAYOR | park | And it seems like these national parks are spread along the coast of Alaska in a haphazard way, meaning the national parks have jurisdiction over a small strip along the coast of Alaska. |
| 0:07:46.460 | 466.460 | JUSTICE SOTOMAYOR | Alaska | And it seems like these national parks are spread along the coast of Alaska in a haphazard way, meaning the national parks have jurisdiction over a small strip along the coast of Alaska. |
| 0:08:05.240 | 485.240 | JUSTICE SOTOMAYOR | navigable | Presumably you're not arguing that this agreement controls the U.S. servitude of navigable waters around those strips. |
| 0:08:05.740 | 485.740 | JUSTICE SOTOMAYOR | waters | Presumably you're not arguing that this agreement controls the U.S. servitude of navigable waters around those strips. |
| 0:08:09.680 | 489.680 | MR. FINDLEY | section | We're not claiming that Section 103(c) trumps the navigable -- navigational servitude. |
| 0:08:11.280 | 491.280 | MR. FINDLEY | navigable | We're not claiming that Section 103(c) trumps the navigable -- navigational servitude. |
| 0:08:13.900 | 493.900 | MR. FINDLEY | ANILCA | What we're claiming is ANILCA makes crystal clear for submerged lands and navigable waters owned by the State, they aren't public lands; they aren't part of the park. |
| 0:08:17.200 | 497.200 | MR. FINDLEY | navigable | What we're claiming is ANILCA makes crystal clear for submerged lands and navigable waters owned by the State, they aren't public lands; they aren't part of the park. |
| 0:08:17.660 | 497.660 | MR. FINDLEY | waters | What we're claiming is ANILCA makes crystal clear for submerged lands and navigable waters owned by the State, they aren't public lands; they aren't part of the park. |
| 0:08:19.460 | 499.460 | MR. FINDLEY | public lands | What we're claiming is ANILCA makes crystal clear for submerged lands and navigable waters owned by the State, they aren't public lands; they aren't part of the park. |
| 0:08:21.720 | 501.720 | MR. FINDLEY | park | What we're claiming is ANILCA makes crystal clear for submerged lands and navigable waters owned by the State, they aren't public lands; they aren't part of the park. |
| 0:08:26.560 | 506.560 | JUSTICE SOTOMAYOR | navigable | So you're saying that the U.S. can't control the navigable servitude in any part of that coast. |
| 0:08:32.680 | 512.680 | MR. FINDLEY | park | The Park Service hasn't been delegated that authority. |
| 0:08:37.200 | 517.200 | MR. FINDLEY | section | It was expressly denied that authority by Section 103(c). |
| 0:08:50.560 | 530.560 | JUSTICE SOTOMAYOR | waters | "Waters in the jurisdiction"? |
| 0:08:53.180 | 533.180 | JUSTICE SOTOMAYOR | navigable | You don't think navigable waters are within the jurisdiction of the United States in Federal lands? |
| 0:08:54.240 | 534.240 | JUSTICE SOTOMAYOR | waters | You don't think navigable waters are within the jurisdiction of the United States in Federal lands? |
| 0:09:00.020 | 540.020 | MR. FINDLEY | regulation | That's within the regulation that the Park Service promulgated nationwide, saying we're going in -- the hovercraft is one of many regulations that they assert to apply within the jurisdiction of the Park Service. |
| 0:09:00.820 | 540.820 | MR. FINDLEY | park | That's within the regulation that the Park Service promulgated nationwide, saying we're going in -- the hovercraft is one of many regulations that they assert to apply within the jurisdiction of the Park Service. |
| 0:09:03.920 | 543.920 | MR. FINDLEY | hovercraft | That's within the regulation that the Park Service promulgated nationwide, saying we're going in -- the hovercraft is one of many regulations that they assert to apply within the jurisdiction of the Park Service. |
| 0:09:09.160 | 549.160 | MR. FINDLEY | section | Section 103(c), which is the -- which is the specific park-enabling statute, denied the Park Service jurisdiction over nonpublic land which includes these navigable waters. |
| 0:09:11.980 | 551.980 | MR. FINDLEY | park | Section 103(c), which is the -- which is the specific park-enabling statute, denied the Park Service jurisdiction over nonpublic land which includes these navigable waters. |
| 0:09:12.820 | 552.820 | MR. FINDLEY | statute | Section 103(c), which is the -- which is the specific park-enabling statute, denied the Park Service jurisdiction over nonpublic land which includes these navigable waters. |
| 0:09:17.680 | 557.680 | MR. FINDLEY | navigable | Section 103(c), which is the -- which is the specific park-enabling statute, denied the Park Service jurisdiction over nonpublic land which includes these navigable waters. |
| 0:09:18.060 | 558.060 | MR. FINDLEY | waters | Section 103(c), which is the -- which is the specific park-enabling statute, denied the Park Service jurisdiction over nonpublic land which includes these navigable waters. |
| 0:09:26.500 | 566.500 | CHIEF JUSTICE ROBERTS | navigable | So if the -- as it often does elsewhere, if the Army Corps of Engineers have issues with respect to things that the State is doing on the navigable waters or, you know, other people are building a -- a -- a damn or a fish -- I forget what they are called -- the Corps of Engineers can come in and say, you can't do that. |
| 0:09:26.940 | 566.940 | CHIEF JUSTICE ROBERTS | waters | So if the -- as it often does elsewhere, if the Army Corps of Engineers have issues with respect to things that the State is doing on the navigable waters or, you know, other people are building a -- a -- a damn or a fish -- I forget what they are called -- the Corps of Engineers can come in and say, you can't do that. |
| 0:09:40.660 | 580.660 | MR. FINDLEY | ANILCA | I mean -- and that's exactly what ANILCA was meant to remain unaffected by the law was those generally applicable rights that -- |
| 0:10:04.620 | 604.620 | MR. FINDLEY | park | The question is the Park Service can't throw its hat in the ring and in addition apply its park regulations on top of everything else. |
| 0:10:08.520 | 608.520 | MR. FINDLEY | regulation | The question is the Park Service can't throw its hat in the ring and in addition apply its park regulations on top of everything else. |
| 0:10:11.300 | 611.300 | JUSTICE BREYER | regulation | But it says in the regulation -- look at the regulation. |
| 0:10:15.300 | 615.300 | JUSTICE BREYER | hovercraft | It says, "The Hovercraft Regulation applies to waters subject to the jurisdiction of the United States." |
| 0:10:15.760 | 615.760 | JUSTICE BREYER | regulation | It says, "The Hovercraft Regulation applies to waters subject to the jurisdiction of the United States." |
| 0:10:17.440 | 617.440 | JUSTICE BREYER | waters | It says, "The Hovercraft Regulation applies to waters subject to the jurisdiction of the United States." |
| 0:10:27.000 | 627.000 | JUSTICE BREYER | park | "Within the boundaries of the National Park Service" -- that's the tougher part -- "including navigable waters." |
| 0:10:30.840 | 630.840 | JUSTICE BREYER | navigable | "Within the boundaries of the National Park Service" -- that's the tougher part -- "including navigable waters." |
| 0:10:31.500 | 631.500 | JUSTICE BREYER | waters | "Within the boundaries of the National Park Service" -- that's the tougher part -- "including navigable waters." |
| 0:10:37.560 | 637.560 | JUSTICE BREYER | river | So the question, I would think, would be is this portion of the river within the boundaries of the National Park Service? |
| 0:10:40.080 | 640.080 | JUSTICE BREYER | park | So the question, I would think, would be is this portion of the river within the boundaries of the National Park Service? |
| 0:10:44.860 | 644.860 | MR. FINDLEY | park | It is within the outer boundaries of the park. |
| 0:10:46.200 | 646.200 | MR. FINDLEY | park | It is not part of the park pursuant to -- |
| 0:10:52.300 | 652.300 | JUSTICE BREYER | Yukon | Well, now, you look at what they say about that, and you get, when they're defining the Yukon-Charley River's National Preserve, it says that that national preserve -- which is the whole thing, which includes the section of the river that we're talking about -- contains public lands. |
| 0:10:53.340 | 653.340 | JUSTICE BREYER | river | Well, now, you look at what they say about that, and you get, when they're defining the Yukon-Charley River's National Preserve, it says that that national preserve -- which is the whole thing, which includes the section of the river that we're talking about -- contains public lands. |
| 0:10:59.960 | 659.960 | JUSTICE BREYER | section | Well, now, you look at what they say about that, and you get, when they're defining the Yukon-Charley River's National Preserve, it says that that national preserve -- which is the whole thing, which includes the section of the river that we're talking about -- contains public lands. |
| 0:11:06.340 | 666.340 | JUSTICE BREYER | public lands | Well, now, you look at what they say about that, and you get, when they're defining the Yukon-Charley River's National Preserve, it says that that national preserve -- which is the whole thing, which includes the section of the river that we're talking about -- contains public lands. |
| 0:11:11.860 | 671.860 | JUSTICE BREYER | public lands | It doesn't say it's identical with the public lands. |
| 0:11:18.180 | 678.180 | JUSTICE BREYER | public lands | And then in another place it says, "Only those lands within the portion which are public lands shall be deemed to be included a portion of such unit," not that they make up the whole of such unit. |
| 0:11:31.220 | 691.220 | JUSTICE BREYER | regulation | I'm quoting from regulations which are 54 U.S.C. -- I don't know. |
| 0:11:54.720 | 714.720 | JUSTICE BREYER | regulation | And then once you have that, you have this regulation applying to this portion of the river. |
| 0:11:57.300 | 717.300 | JUSTICE BREYER | river | And then once you have that, you have this regulation applying to this portion of the river. |
| 0:11:59.200 | 719.200 | JUSTICE BREYER | statute | So now we look to the statute to see if anything there takes away what the regulations seem to give. |
| 0:12:03.120 | 723.120 | JUSTICE BREYER | regulation | So now we look to the statute to see if anything there takes away what the regulations seem to give. |
| 0:12:06.400 | 726.400 | JUSTICE BREYER | statute | And the only part of the statute -- though it's an important part -- that supports you is the second sentence. |
| 0:12:17.900 | 737.900 | JUSTICE BREYER | regulation | But as I read that second sentence, it says that, "The regulations that apply solely to public lands within such units," you see, "are the ones that don't apply to the private land up in Yukon-Charley. |
| 0:12:21.640 | 741.640 | JUSTICE BREYER | public lands | But as I read that second sentence, it says that, "The regulations that apply solely to public lands within such units," you see, "are the ones that don't apply to the private land up in Yukon-Charley. |
| 0:12:29.720 | 749.720 | JUSTICE BREYER | Yukon | But as I read that second sentence, it says that, "The regulations that apply solely to public lands within such units," you see, "are the ones that don't apply to the private land up in Yukon-Charley. |
| 0:12:32.740 | 752.740 | JUSTICE BREYER | regulation | But I've just read you a regulation, which, on my reading of it, is the Hovercraft Regulation, and does not apply solely to public lands within National Park Service units, either in Alaska or anywhere else. |
| 0:12:35.540 | 755.540 | JUSTICE BREYER | hovercraft | But I've just read you a regulation, which, on my reading of it, is the Hovercraft Regulation, and does not apply solely to public lands within National Park Service units, either in Alaska or anywhere else. |
| 0:12:40.780 | 760.780 | JUSTICE BREYER | public lands | But I've just read you a regulation, which, on my reading of it, is the Hovercraft Regulation, and does not apply solely to public lands within National Park Service units, either in Alaska or anywhere else. |
| 0:12:42.700 | 762.700 | JUSTICE BREYER | park | But I've just read you a regulation, which, on my reading of it, is the Hovercraft Regulation, and does not apply solely to public lands within National Park Service units, either in Alaska or anywhere else. |
| 0:12:44.420 | 764.420 | JUSTICE BREYER | Alaska | But I've just read you a regulation, which, on my reading of it, is the Hovercraft Regulation, and does not apply solely to public lands within National Park Service units, either in Alaska or anywhere else. |
| 0:12:47.420 | 767.420 | JUSTICE BREYER | statute | And therefore, the statute doesn't stop it. |
| 0:13:12.100 | 792.100 | MR. FINDLEY | park | But prior to 1996, the Park Service did not apply this regulation to navigable waters. |
| 0:13:14.160 | 794.160 | MR. FINDLEY | regulation | But prior to 1996, the Park Service did not apply this regulation to navigable waters. |
| 0:13:15.580 | 795.580 | MR. FINDLEY | navigable | But prior to 1996, the Park Service did not apply this regulation to navigable waters. |
| 0:13:15.960 | 795.960 | MR. FINDLEY | waters | But prior to 1996, the Park Service did not apply this regulation to navigable waters. |
| 0:13:23.400 | 803.400 | MR. FINDLEY | navigable | 1.2(b) where they say now we're going to apply this to navigable waters without regard to ownership of the submerged lands. |
| 0:13:24.380 | 804.380 | MR. FINDLEY | waters | 1.2(b) where they say now we're going to apply this to navigable waters without regard to ownership of the submerged lands. |
| 0:13:28.280 | 808.280 | MR. FINDLEY | Sturgeon | And that is what Mr. Sturgeon is objecting to. |
| 0:13:43.540 | 823.540 | JUSTICE KAGAN | regulation | And I think that the question that Justice Breyer is putting to you is this question about what this provision means: "Shall be subject to the regulations applicable solely to public lands." |
| 0:13:46.100 | 826.100 | JUSTICE KAGAN | public lands | And I think that the question that Justice Breyer is putting to you is this question about what this provision means: "Shall be subject to the regulations applicable solely to public lands." |
| 0:13:58.480 | 838.480 | JUSTICE KAGAN | public lands | And this does not apply solely to public lands. |
| 0:14:00.660 | 840.660 | MR. FINDLEY | regulation | Because the regulation never should have been allowed to reach out to the public land. |
| 0:14:05.540 | 845.540 | MR. FINDLEY | hovercraft | The Hovercraft Regulation, as promulgated in 1983, was a regulation promulgated solely to manage park land. |
| 0:14:05.900 | 845.900 | MR. FINDLEY | regulation | The Hovercraft Regulation, as promulgated in 1983, was a regulation promulgated solely to manage park land. |
| 0:14:11.720 | 851.720 | MR. FINDLEY | park | The Hovercraft Regulation, as promulgated in 1983, was a regulation promulgated solely to manage park land. |
| 0:14:16.240 | 856.240 | MR. FINDLEY | regulation | What 103(c) says, it was a permanent barrier to take in that regulation and extending it out to nonpublic land. |
| 0:14:26.080 | 866.080 | MR. FINDLEY | regulation | The fact that they did it in 1996, and the fact that they've gotten away with it for over 20 years, does not suddenly make the regulation -- |
| 0:14:28.020 | 868.020 | JUSTICE KENNEDY | statute | I -- I don't understand why the statute that Justice Breyer is focusing on, that part of the statute. |
| 0:14:33.360 | 873.360 | JUSTICE KENNEDY | park | Applies just to park regulations and not to something from the EPA or the Federal Aeronautics Administration. |
| 0:14:33.540 | 873.540 | JUSTICE KENNEDY | regulation | Applies just to park regulations and not to something from the EPA or the Federal Aeronautics Administration. |
| 0:14:48.140 | 888.140 | MR. FINDLEY | regulation | Because that would not be a regulation solely enacted to manage park land. |
| 0:14:49.820 | 889.820 | MR. FINDLEY | park | Because that would not be a regulation solely enacted to manage park land. |
| 0:14:57.140 | 897.140 | JUSTICE KENNEDY | regulation | But it -- it -- it -- but it -- it talks about regulations applicable solely to public lands. |
| 0:14:58.920 | 898.920 | JUSTICE KENNEDY | public lands | But it -- it -- it -- but it -- it talks about regulations applicable solely to public lands. |
| 0:15:03.700 | 903.700 | JUSTICE KENNEDY | regulation | But is -- is -- is that all Forest Service regulations? |
| 0:15:10.500 | 910.500 | JUSTICE KENNEDY | regulation | Are you saying that that's a -- the same as Forest Service regulations? |
| 0:15:13.020 | 913.020 | MR. FINDLEY | regulation | Forest Service regulations are also solely enacted to manage those public lands. |
| 0:15:16.700 | 916.700 | MR. FINDLEY | public lands | Forest Service regulations are also solely enacted to manage those public lands. |
| 0:15:20.740 | 920.740 | MR. FINDLEY | statute | To answer your question, if you take the word "solely" out of the statute, you've inadvertently created a statute which says none of these private lands within the ANILCA parks are subject to any regulations applicable to public lands. |
| 0:15:25.400 | 925.400 | MR. FINDLEY | ANILCA | To answer your question, if you take the word "solely" out of the statute, you've inadvertently created a statute which says none of these private lands within the ANILCA parks are subject to any regulations applicable to public lands. |
| 0:15:25.620 | 925.620 | MR. FINDLEY | park | To answer your question, if you take the word "solely" out of the statute, you've inadvertently created a statute which says none of these private lands within the ANILCA parks are subject to any regulations applicable to public lands. |
| 0:15:27.220 | 927.220 | MR. FINDLEY | regulation | To answer your question, if you take the word "solely" out of the statute, you've inadvertently created a statute which says none of these private lands within the ANILCA parks are subject to any regulations applicable to public lands. |
| 0:15:28.580 | 928.580 | MR. FINDLEY | public lands | To answer your question, if you take the word "solely" out of the statute, you've inadvertently created a statute which says none of these private lands within the ANILCA parks are subject to any regulations applicable to public lands. |
| 0:15:40.280 | 940.280 | JUSTICE KAGAN | statute | But it seems to me that if you took it out of the statute, what you would have was to something that says no private lands shall be subject to the regulations applicable to public lands. |
| 0:15:46.120 | 946.120 | JUSTICE KAGAN | regulation | But it seems to me that if you took it out of the statute, what you would have was to something that says no private lands shall be subject to the regulations applicable to public lands. |
| 0:15:47.600 | 947.600 | JUSTICE KAGAN | public lands | But it seems to me that if you took it out of the statute, what you would have was to something that says no private lands shall be subject to the regulations applicable to public lands. |
| 0:15:53.600 | 953.600 | JUSTICE KAGAN | regulation | If -- if it had said that, no private lands shall be subject to the regulations applicable to public lands, you wouldn't be here. |
| 0:15:54.780 | 954.780 | JUSTICE KAGAN | public lands | If -- if it had said that, no private lands shall be subject to the regulations applicable to public lands, you wouldn't be here. |
| 0:16:02.360 | 962.360 | JUSTICE KAGAN | regulation | It says, "No private lands shall be subject to the regulations applicable solely" -- exclusively, only -- "to public lands." |
| 0:16:06.340 | 966.340 | JUSTICE KAGAN | public lands | It says, "No private lands shall be subject to the regulations applicable solely" -- exclusively, only -- "to public lands." |
| 0:16:12.080 | 972.080 | MR. FINDLEY | Sturgeon | And again, though, however, you take out the word "solely," not only, I suppose, will Mr. Sturgeon win, but you have a lot of in-holding owners that would be happy to know they're not subject to the Clean Water Act, the Clean Air Act, the Voting Rights Act, or anything else. |
| 0:16:26.880 | 986.880 | JUSTICE KAGAN | statute | So you're saying that the word "solely" distinguishes between statutes like the Clean Air Act and park land statutes? |
| 0:16:29.700 | 989.700 | JUSTICE KAGAN | park | So you're saying that the word "solely" distinguishes between statutes like the Clean Air Act and park land statutes? |
| 0:16:40.040 | 1000.040 | JUSTICE KAGAN | park | Because I understand why Congress might have wanted to distinguish between, like, the Clean Air Act and park statutes. |
| 0:16:40.900 | 1000.900 | JUSTICE KAGAN | statute | Because I understand why Congress might have wanted to distinguish between, like, the Clean Air Act and park statutes. |
| 0:17:03.120 | 1023.120 | JUSTICE KAGAN | statute | How does that distinguish between two different kinds of generally-applicable statutes, one generally applicable in applying to park lands and not park lands, and another generally applicable in the sense of applying to both public and private lands within parks. |
| 0:17:06.720 | 1026.720 | JUSTICE KAGAN | park | How does that distinguish between two different kinds of generally-applicable statutes, one generally applicable in applying to park lands and not park lands, and another generally applicable in the sense of applying to both public and private lands within parks. |
| 0:17:18.360 | 1038.360 | MR. FINDLEY | section | Read that sentence in context with both the first sentence of Section 103(c) and the third sentence, and then read it in context with the purpose of the statute. |
| 0:17:22.400 | 1042.400 | MR. FINDLEY | statute | Read that sentence in context with both the first sentence of Section 103(c) and the third sentence, and then read it in context with the purpose of the statute. |
| 0:17:25.280 | 1045.280 | MR. FINDLEY | park | The first sentence says these lands are not part of the park. |
| 0:17:33.500 | 1053.500 | MR. FINDLEY | park | And the third sentence makes clear that if the Federal government -- or the Park Service, excuse me -- wants to regulate these lands, wants them to be part of the park, they have to go out and acquire them. |
| 0:17:42.520 | 1062.520 | MR. FINDLEY | park | There wouldn't be any purpose for that third sentence if the Federal government -- or, excuse me -- the Park Service already had authority of those nonpublic lands. |
| 0:17:48.580 | 1068.580 | MR. FINDLEY | statute | And if you take a step back and you look at the overall purpose of the statute -- and again 101(d) of the statute makes clear that this is a balancing statute. |
| 0:17:54.480 | 1074.480 | MR. FINDLEY | statute | This is not just a conservation statute. |
| 0:18:05.600 | 1085.600 | MR. FINDLEY | regulation | Again, I would direct you to, if -- if there's any doubt, look at the 1979 Senate report, makes crystal clear about what regulations were meant to be affected by this and which were not. |
| 0:18:35.780 | 1115.780 | MS. BOTSTEIN | Alaska | Thank you, Mr. Chief Justice, and may it please the Court: This case is about honoring Congress's mandate to protect Alaska's sovereignty in the face of the Park Service's rapidly-expanding interpretation of its own jurisdiction under ANILCA. |
| 0:18:38.280 | 1118.280 | MS. BOTSTEIN | park | Thank you, Mr. Chief Justice, and may it please the Court: This case is about honoring Congress's mandate to protect Alaska's sovereignty in the face of the Park Service's rapidly-expanding interpretation of its own jurisdiction under ANILCA. |
| 0:18:42.920 | 1122.920 | MS. BOTSTEIN | ANILCA | Thank you, Mr. Chief Justice, and may it please the Court: This case is about honoring Congress's mandate to protect Alaska's sovereignty in the face of the Park Service's rapidly-expanding interpretation of its own jurisdiction under ANILCA. |
| 0:18:45.380 | 1125.380 | MS. BOTSTEIN | ANILCA | Congress provided in ANILCA that Alaska would lose over 100 million acres of land. |
| 0:18:45.960 | 1125.960 | MS. BOTSTEIN | Alaska | Congress provided in ANILCA that Alaska would lose over 100 million acres of land. |
| 0:18:55.600 | 1135.600 | MS. BOTSTEIN | waters | But at the same time, Congress provided concrete protection against further encroachments on the lands and waters that Alaska did retain. |
| 0:18:56.060 | 1136.060 | MS. BOTSTEIN | Alaska | But at the same time, Congress provided concrete protection against further encroachments on the lands and waters that Alaska did retain. |
| 0:18:59.400 | 1139.400 | MS. BOTSTEIN | park | This Court should reject the Park Service's attempt to redefine the Federal/State balance that Congress chose. |
| 0:19:06.540 | 1146.540 | MS. BOTSTEIN | ANILCA | We know from ANILCA that Congress intended to provide unique management rules for Alaska, and there are good reasons for that. |
| 0:19:10.540 | 1150.540 | MS. BOTSTEIN | Alaska | We know from ANILCA that Congress intended to provide unique management rules for Alaska, and there are good reasons for that. |
| 0:19:17.320 | 1157.320 | MS. BOTSTEIN | Alaska | This was the continuation in a trilogy of legislation that began with the Alaska Statehood Act and the Alaska Native Claims Settlement Act, and this piece of legislation furthered the goals of those predecessors. |
| 0:19:29.680 | 1169.680 | MS. BOTSTEIN | statute | One purpose of the statute was to provide adequate opportunity for the satisfaction of the economic and social needs of the State of Alaska and its people. |
| 0:19:36.640 | 1176.640 | MS. BOTSTEIN | Alaska | One purpose of the statute was to provide adequate opportunity for the satisfaction of the economic and social needs of the State of Alaska and its people. |
| 0:19:48.340 | 1188.340 | MS. BOTSTEIN | park | And that means that the National Park Service's authority in other States or in other parks are not the baseline here. |
| 0:19:57.640 | 1197.640 | MS. BOTSTEIN | park | The starting point is the power that Congress gave to the National Park Service and other Land Management agencies in regulating ANILCA parks. |
| 0:20:01.660 | 1201.660 | MS. BOTSTEIN | ANILCA | The starting point is the power that Congress gave to the National Park Service and other Land Management agencies in regulating ANILCA parks. |
| 0:20:05.020 | 1205.020 | MS. BOTSTEIN | section | And what Congress did in Section 103(c) was to set aside the inholdings of the State, private, and native corporation lands that might be surrounded by the parks, but should not be regulated as though they were in fact part of the parks. |
| 0:20:14.780 | 1214.780 | MS. BOTSTEIN | park | And what Congress did in Section 103(c) was to set aside the inholdings of the State, private, and native corporation lands that might be surrounded by the parks, but should not be regulated as though they were in fact part of the parks. |
| 0:20:29.820 | 1229.820 | MS. BOTSTEIN | waters | The submerged lands and the waters that accompany them. |
| 0:20:46.760 | 1246.760 | MS. BOTSTEIN | park | I understand the Park Service's argument to be that the -- the submerged -- the waters and the submerged lands have somehow become public lands. |
| 0:20:52.280 | 1252.280 | MS. BOTSTEIN | waters | I understand the Park Service's argument to be that the -- the submerged -- the waters and the submerged lands have somehow become public lands. |
| 0:20:55.920 | 1255.920 | MS. BOTSTEIN | public lands | I understand the Park Service's argument to be that the -- the submerged -- the waters and the submerged lands have somehow become public lands. |
| 0:21:00.960 | 1260.960 | MS. BOTSTEIN | section | I mean, I understand their argument here to say, well, Section 103(c) doesn't apply to the waters because those are, in fact, not Alaska's waters. |
| 0:21:02.920 | 1262.920 | MS. BOTSTEIN | waters | I mean, I understand their argument here to say, well, Section 103(c) doesn't apply to the waters because those are, in fact, not Alaska's waters. |
| 0:21:04.960 | 1264.960 | MS. BOTSTEIN | Alaska | I mean, I understand their argument here to say, well, Section 103(c) doesn't apply to the waters because those are, in fact, not Alaska's waters. |
| 0:21:13.460 | 1273.460 | MS. BOTSTEIN | waters | This Court's cases have held that control over lands and waters is an unmistakable and central part of a State sovereignty. |
| 0:21:25.460 | 1285.460 | JUSTICE GINSBURG | navigable | What does that do to Federal right to control, whether it's titled or not, all navigable waters? |
| 0:21:26.140 | 1286.140 | JUSTICE GINSBURG | waters | What does that do to Federal right to control, whether it's titled or not, all navigable waters? |
| 0:21:34.820 | 1294.820 | MS. BOTSTEIN | ANILCA | Congress hasn't given that and ANILCA doesn't delegate the authorization to control navigation to the Park Service as part of Park Service regulation. |
| 0:21:40.660 | 1300.660 | MS. BOTSTEIN | park | Congress hasn't given that and ANILCA doesn't delegate the authorization to control navigation to the Park Service as part of Park Service regulation. |
| 0:21:43.140 | 1303.140 | MS. BOTSTEIN | regulation | Congress hasn't given that and ANILCA doesn't delegate the authorization to control navigation to the Park Service as part of Park Service regulation. |
| 0:21:45.560 | 1305.560 | MS. BOTSTEIN | park | And I think even the Park Service isn't asserting that it has. |
| 0:21:57.800 | 1317.800 | MS. BOTSTEIN | waters | Your Honor, Congress has the power to control navigation in these waters through exercise of the navigational servitude. |
| 0:22:03.100 | 1323.100 | MS. BOTSTEIN | park | Congress hasn't given that power to the National Park Service. |
| 0:22:13.500 | 1333.500 | JUSTICE KENNEDY | regulation | Well, suppose there were a Coast Guard regulation that -- applicable to all throughout the United States. |
| 0:22:19.720 | 1339.720 | JUSTICE KENNEDY | river | Could that be applied to this river? |
| 0:22:26.620 | 1346.620 | JUSTICE KENNEDY | park | Well, why is the -- so you're -- you're just saying that the Park Service lacks authority to promulgate this regulation quite without regard to this statute, which doesn't help me very much. |
| 0:22:29.060 | 1349.060 | JUSTICE KENNEDY | regulation | Well, why is the -- so you're -- you're just saying that the Park Service lacks authority to promulgate this regulation quite without regard to this statute, which doesn't help me very much. |
| 0:22:30.960 | 1350.960 | JUSTICE KENNEDY | statute | Well, why is the -- so you're -- you're just saying that the Park Service lacks authority to promulgate this regulation quite without regard to this statute, which doesn't help me very much. |
| 0:22:35.940 | 1355.940 | MS. BOTSTEIN | statute | We're saying this statute, the enabling legislation of the parks, sets the ground rules for what authority the National Park Service has. |
| 0:22:37.960 | 1357.960 | MS. BOTSTEIN | park | We're saying this statute, the enabling legislation of the parks, sets the ground rules for what authority the National Park Service has. |
| 0:22:49.540 | 1369.540 | JUSTICE SOTOMAYOR | hovercraft | You're not saying that the Coast Guard couldn't come in and say no hovercrafts around the Alaskan coast. |
| 0:22:56.280 | 1376.280 | MS. BOTSTEIN | regulation | The Coast Guard could enact regulations to regulate navigation in the water. |
| 0:22:58.900 | 1378.900 | MS. BOTSTEIN | river | The River and Harbors Act gives the Coast Guard that explicit delegation. |
| 0:23:07.840 | 1387.840 | JUSTICE SOTOMAYOR | park | How about if they wanted to say, in this alcove, the Coast Guard, not the Park Service, says you can't have hovercrafts, that would be okay? |
| 0:23:10.950 | 1390.950 | JUSTICE SOTOMAYOR | hovercraft | How about if they wanted to say, in this alcove, the Coast Guard, not the Park Service, says you can't have hovercrafts, that would be okay? |
| 0:23:18.560 | 1398.560 | JUSTICE KAGAN | river | If I understand what you're saying, you're saying with respect to a river that's smack in the middle of federally owned lands, okay, a river that's in the middle of federally owned lands, what cannot happen is that the EPA can't come in and say there's some terrible pollution in this river, and we need to address it. |
| 0:23:40.460 | 1420.460 | MS. BOTSTEIN | waters | I mean, first, the -- the waters go with the submerged lands. |
| 0:23:44.400 | 1424.400 | MS. BOTSTEIN | Alaska | If the submerged lands pass to the State of Alaska, then there are some lands that are going to be State owned together with the water column itself. |
| 0:23:50.860 | 1430.860 | MS. BOTSTEIN | section | And what Section 103(c) places limits on is the Park Service's ability to regulate that in the same fashion it wants to regulate the rest -- |
| 0:23:55.080 | 1435.080 | MS. BOTSTEIN | park | And what Section 103(c) places limits on is the Park Service's ability to regulate that in the same fashion it wants to regulate the rest -- |
| 0:24:05.980 | 1445.980 | JUSTICE KAGAN | park | It's only the Park Service that can't do it? |
| 0:24:14.980 | 1454.980 | MS. BOTSTEIN | waters | Or another Land Management agency that is regulating -- is attempting to regulate the lands and waters that are not part of the park as though they were part of the park. |
| 0:24:16.900 | 1456.900 | MS. BOTSTEIN | park | Or another Land Management agency that is regulating -- is attempting to regulate the lands and waters that are not part of the park as though they were part of the park. |
| 0:24:23.360 | 1463.360 | MS. BOTSTEIN | park | We're saying that the Park Service is not the policeman here, because it is Congress that needs to give an agency power to regulate -- |
| 0:24:42.840 | 1482.840 | JUSTICE KAGAN | park | And I guess part of my question about this is, I look at that map, you know, and that map of this area has all this green land, which green represents real Federal park land, and there's a river that runs through it. |
| 0:24:44.260 | 1484.260 | JUSTICE KAGAN | river | And I guess part of my question about this is, I look at that map, you know, and that map of this area has all this green land, which green represents real Federal park land, and there's a river that runs through it. |
| 0:24:48.480 | 1488.480 | JUSTICE KAGAN | river | And -- and you're saying that that river that runs through the park land, and nobody can do anything on -- or the Feds can't do anything on? |
| 0:24:50.440 | 1490.440 | JUSTICE KAGAN | park | And -- and you're saying that that river that runs through the park land, and nobody can do anything on -- or the Feds can't do anything on? |
| 0:25:03.120 | 1503.120 | JUSTICE KAGAN | river | I mean, I can understand the argument with respect to the inholdings and the rivers that are running through the inholdings. |
| 0:25:06.800 | 1506.800 | JUSTICE KAGAN | river | But this is the rivers that are running through the park land. |
| 0:25:08.620 | 1508.620 | JUSTICE KAGAN | park | But this is the rivers that are running through the park land. |
| 0:25:15.920 | 1515.920 | JUSTICE KAGAN | park | Now, it seems to me a very strange thing that Congress would have created Federal lands in a Federal park land but said that the Federal Park Service can't have anything to do with the rivers. |
| 0:25:21.040 | 1521.040 | JUSTICE KAGAN | river | Now, it seems to me a very strange thing that Congress would have created Federal lands in a Federal park land but said that the Federal Park Service can't have anything to do with the rivers. |
| 0:25:21.980 | 1521.980 | JUSTICE KAGAN | river | The rivers are like an important part of the park, aren't they? |
| 0:25:23.500 | 1523.500 | JUSTICE KAGAN | park | The rivers are like an important part of the park, aren't they? |
| 0:25:25.220 | 1525.220 | MS. BOTSTEIN | river | The rivers are an important part of the park, but the control over the rivers is Alaska's, is Alaska's by sovereign right. |
| 0:25:27.360 | 1527.360 | MS. BOTSTEIN | park | The rivers are an important part of the park, but the control over the rivers is Alaska's, is Alaska's by sovereign right. |
| 0:25:31.000 | 1531.000 | MS. BOTSTEIN | Alaska | The rivers are an important part of the park, but the control over the rivers is Alaska's, is Alaska's by sovereign right. |
| 0:25:43.460 | 1543.460 | JUSTICE KENNEDY | navigable | But that's not true as to navigable waters. |
| 0:25:43.940 | 1543.940 | JUSTICE KENNEDY | waters | But that's not true as to navigable waters. |
| 0:25:46.060 | 1546.060 | JUSTICE KENNEDY | navigable | The Federal government can regulate navigable waters. |
| 0:25:46.620 | 1546.620 | JUSTICE KENNEDY | waters | The Federal government can regulate navigable waters. |
| 0:25:50.180 | 1550.180 | MS. BOTSTEIN | ANILCA | ANILCA does not talk about navigable waters. |
| 0:25:51.620 | 1551.620 | MS. BOTSTEIN | navigable | ANILCA does not talk about navigable waters. |
| 0:25:52.160 | 1552.160 | MS. BOTSTEIN | waters | ANILCA does not talk about navigable waters. |
| 0:25:59.820 | 1559.820 | MS. BOTSTEIN | park | It is about the Land Management agency's ability to regulate parks. |
| 0:26:02.580 | 1562.580 | MS. BOTSTEIN | park | And our position is that the park -- the park management can't encompass State waters and lands. |
| 0:26:06.920 | 1566.920 | MS. BOTSTEIN | waters | And our position is that the park -- the park management can't encompass State waters and lands. |
| 0:26:12.120 | 1572.120 | MS. BOTSTEIN | Alaska | Alaska's waters are used in ways that are different from the lower 48 in, for example, the Yukon Flats National Wildlife Refuge, there are three villages of less than one hundred people that are hundreds of miles from any road. |
| 0:26:12.680 | 1572.680 | MS. BOTSTEIN | waters | Alaska's waters are used in ways that are different from the lower 48 in, for example, the Yukon Flats National Wildlife Refuge, there are three villages of less than one hundred people that are hundreds of miles from any road. |
| 0:26:18.080 | 1578.080 | MS. BOTSTEIN | Yukon | Alaska's waters are used in ways that are different from the lower 48 in, for example, the Yukon Flats National Wildlife Refuge, there are three villages of less than one hundred people that are hundreds of miles from any road. |
| 0:26:26.900 | 1586.900 | MS. BOTSTEIN | Alaska | And this is common in Alaska. |
| 0:26:28.060 | 1588.060 | MS. BOTSTEIN | river | So these rivers are the way that you would travel to get medical care or groceries or obtain school books for your children. |
| 0:26:35.580 | 1595.580 | MS. BOTSTEIN | Alaska | And Alaska's ability to make choices about what sort of conduct is permissible on the rivers furthers its ability to provide economic and self-sufficiency for its people, which was one of Congress's primary goals in passing this legislation. |
| 0:26:41.100 | 1601.100 | MS. BOTSTEIN | river | And Alaska's ability to make choices about what sort of conduct is permissible on the rivers furthers its ability to provide economic and self-sufficiency for its people, which was one of Congress's primary goals in passing this legislation. |
| 0:26:54.720 | 1614.720 | MS. BOTSTEIN | park | The idea that the creation of a park somehow transforms Alaska's waters into Federal waters, Alaska lands into Federal lands without a clear statement would dramatically change Alaska's sovereign ability to control its property in a way that this Court never has sanctioned and should not do so now. |
| 0:26:57.240 | 1617.240 | MS. BOTSTEIN | Alaska | The idea that the creation of a park somehow transforms Alaska's waters into Federal waters, Alaska lands into Federal lands without a clear statement would dramatically change Alaska's sovereign ability to control its property in a way that this Court never has sanctioned and should not do so now. |
| 0:26:58.160 | 1618.160 | MS. BOTSTEIN | waters | The idea that the creation of a park somehow transforms Alaska's waters into Federal waters, Alaska lands into Federal lands without a clear statement would dramatically change Alaska's sovereign ability to control its property in a way that this Court never has sanctioned and should not do so now. |
| 0:27:42.920 | 1662.920 | JUSTICE BREYER | park | There are some that only apply to the park but not the private people. |
| 0:27:45.800 | 1665.800 | JUSTICE BREYER | statute | What this statute says is the latter. |
| 0:27:51.140 | 1671.140 | JUSTICE BREYER | Alaska | Doesn't deprive -- apply to that land that you gave to Alaska. |
| 0:27:53.060 | 1673.060 | JUSTICE BREYER | statute | That's what the statute says. |
| 0:27:57.020 | 1677.020 | JUSTICE BREYER | hovercraft | And what the reg says is that our hovercraft reg applies to everything within Yosemite, if this were Yosemite. |
| 0:28:02.840 | 1682.840 | JUSTICE BREYER | navigable | This navigable waters, whether the land around it is owned by James Jones, the private person, or whether it's owned -- whether it's part of Yosemite Park. |
| 0:28:03.400 | 1683.400 | JUSTICE BREYER | waters | This navigable waters, whether the land around it is owned by James Jones, the private person, or whether it's owned -- whether it's part of Yosemite Park. |
| 0:28:11.180 | 1691.180 | JUSTICE BREYER | park | This navigable waters, whether the land around it is owned by James Jones, the private person, or whether it's owned -- whether it's part of Yosemite Park. |
| 0:28:24.500 | 1704.500 | JUSTICE BREYER | park | And the second problem is the NPS, the National Park Service, is it really all of Yosemite, you know, with that private thing or is it just the public part? |
| 0:28:56.200 | 1736.200 | MS. BOTSTEIN | park | Analytically, the Court would first look to the enabling legislation that creates a specific park. |
| 0:29:02.080 | 1742.080 | MS. BOTSTEIN | park | In the case of Yosemite, there's actually a clear congressional indication that says the Park Service has sole and exclusive jurisdiction over park lands. |
| 0:29:08.180 | 1748.180 | MS. BOTSTEIN | ANILCA | Here we would look to ANILCA and specifically the limitations in Section 103(c), which tell the Park Service, in fact, you cannot manage State and private lands as though they were public lands. |
| 0:29:10.780 | 1750.780 | MS. BOTSTEIN | section | Here we would look to ANILCA and specifically the limitations in Section 103(c), which tell the Park Service, in fact, you cannot manage State and private lands as though they were public lands. |
| 0:29:13.280 | 1753.280 | MS. BOTSTEIN | park | Here we would look to ANILCA and specifically the limitations in Section 103(c), which tell the Park Service, in fact, you cannot manage State and private lands as though they were public lands. |
| 0:29:19.060 | 1759.060 | MS. BOTSTEIN | public lands | Here we would look to ANILCA and specifically the limitations in Section 103(c), which tell the Park Service, in fact, you cannot manage State and private lands as though they were public lands. |
| 0:29:34.220 | 1774.220 | MS. KOVNER | park | Mr. Chief Justice, and may it please the Court: When Congress created new park units in Alaska for the express purpose of protecting their waters, their free-flowing rivers and their fish, it didn't simultaneously strip the Park Service of preexisting authorities to achieve those goals by regulating navigable waters. |
| 0:29:35.040 | 1775.040 | MS. KOVNER | Alaska | Mr. Chief Justice, and may it please the Court: When Congress created new park units in Alaska for the express purpose of protecting their waters, their free-flowing rivers and their fish, it didn't simultaneously strip the Park Service of preexisting authorities to achieve those goals by regulating navigable waters. |
| 0:29:38.560 | 1778.560 | MS. KOVNER | waters | Mr. Chief Justice, and may it please the Court: When Congress created new park units in Alaska for the express purpose of protecting their waters, their free-flowing rivers and their fish, it didn't simultaneously strip the Park Service of preexisting authorities to achieve those goals by regulating navigable waters. |
| 0:29:40.480 | 1780.480 | MS. KOVNER | river | Mr. Chief Justice, and may it please the Court: When Congress created new park units in Alaska for the express purpose of protecting their waters, their free-flowing rivers and their fish, it didn't simultaneously strip the Park Service of preexisting authorities to achieve those goals by regulating navigable waters. |
| 0:29:50.060 | 1790.060 | MS. KOVNER | navigable | Mr. Chief Justice, and may it please the Court: When Congress created new park units in Alaska for the express purpose of protecting their waters, their free-flowing rivers and their fish, it didn't simultaneously strip the Park Service of preexisting authorities to achieve those goals by regulating navigable waters. |
| 0:29:58.640 | 1798.640 | MS. KOVNER | park | And I think it might make sense just to clarify our argument to first explain what those preexisting authorities are and why they let the Park Service -- |
| 0:30:20.500 | 1820.500 | JUSTICE ALITO | hovercraft | Now, I understand what the Ninth Circuit to have held, to be this, that the hovercraft rule is not barred by the second sentence of Section 103(c) of ANILCA, because the hovercraft rule does not apply only in Alaska, because it applies throughout the country. |
| 0:30:25.540 | 1825.540 | JUSTICE ALITO | section | Now, I understand what the Ninth Circuit to have held, to be this, that the hovercraft rule is not barred by the second sentence of Section 103(c) of ANILCA, because the hovercraft rule does not apply only in Alaska, because it applies throughout the country. |
| 0:30:27.360 | 1827.360 | JUSTICE ALITO | ANILCA | Now, I understand what the Ninth Circuit to have held, to be this, that the hovercraft rule is not barred by the second sentence of Section 103(c) of ANILCA, because the hovercraft rule does not apply only in Alaska, because it applies throughout the country. |
| 0:30:31.920 | 1831.920 | JUSTICE ALITO | Alaska | Now, I understand what the Ninth Circuit to have held, to be this, that the hovercraft rule is not barred by the second sentence of Section 103(c) of ANILCA, because the hovercraft rule does not apply only in Alaska, because it applies throughout the country. |
| 0:30:40.500 | 1840.500 | MS. KOVNER | hovercraft | I think you're right that they were saying that hovercraft rule isn't covered by the second sentence. |
| 0:30:54.020 | 1854.020 | MS. KOVNER | regulation | But I think they say this rule is out for two reasons: One is that conservation-specific unit, and the other is -- and I direct you to 24a and 26a -- they talk about whether the regulation is generally applicable or not. |
| 0:31:00.400 | 1860.400 | MS. KOVNER | public lands | And I take that to mean, essentially whether it applies only on public lands, in which case it's out, or whether it's the very limited class of rules that the Park Service is allowed to write in the way that Justice Breyer alludes to, to apply to both public and private lands. |
| 0:31:05.340 | 1865.340 | MS. KOVNER | park | And I take that to mean, essentially whether it applies only on public lands, in which case it's out, or whether it's the very limited class of rules that the Park Service is allowed to write in the way that Justice Breyer alludes to, to apply to both public and private lands. |
| 0:31:13.520 | 1873.520 | MS. KOVNER | park | And so if I could just explain the Park Service's -- |
| 0:31:21.340 | 1881.340 | JUSTICE ALITO | hovercraft | Well, no. I want to -- I understand the -- the holding -- and I -- I stand ready to be corrected -- to be what I stated: That the hovercraft rule is not barred because it isn't Alaska-specific. |
| 0:31:24.140 | 1884.140 | JUSTICE ALITO | Alaska | Well, no. I want to -- I understand the -- the holding -- and I -- I stand ready to be corrected -- to be what I stated: That the hovercraft rule is not barred because it isn't Alaska-specific. |
| 0:32:05.580 | 1925.580 | JUSTICE SOTOMAYOR | statute | I think they start with that Federal lands, as defined under the statute, are only lands that the U.S. has title to. |
| 0:32:16.400 | 1936.400 | MS. KOVNER | public lands | We think public lands are slightly more expansive than that. |
| 0:32:20.220 | 1940.220 | JUSTICE SOTOMAYOR | statute | Read the statute -- |
| 0:32:22.680 | 1942.680 | JUSTICE SOTOMAYOR | statute | -- in the statute -- |
| 0:32:28.340 | 1948.340 | JUSTICE SOTOMAYOR | section | I'm going -- I'm in the definition section. |
| 0:32:31.600 | 1951.600 | MS. KOVNER | public lands | So we're on 3a of our appendix, and it defines public lands to mean lands situated in Alaska, which are Federal lands. |
| 0:32:34.600 | 1954.600 | MS. KOVNER | Alaska | So we're on 3a of our appendix, and it defines public lands to mean lands situated in Alaska, which are Federal lands. |
| 0:32:50.460 | 1970.460 | MS. KOVNER | waters | "Lands" is defined to include not just lands and waters, but also interests therein. |
| 0:32:55.140 | 1975.140 | MS. KOVNER | public lands | And what we get from that, Your Honor, is that public lands includes interests in water that the United States holds title to. |
| 0:33:51.960 | 2031.960 | JUSTICE SCALIA | river | And you're -- you're telling us that the river, that the government holds title to the river. |
| 0:33:57.880 | 2037.880 | JUSTICE SCALIA | river | It has usufructuary rights in the river. |
| 0:34:18.700 | 2058.700 | MS. KOVNER | regulation | And the interest has been defined by regulation. |
| 0:34:50.440 | 2090.440 | MS. KOVNER | ANILCA | So I think that move is made by ANILCA, the statute. |
| 0:34:51.020 | 2091.020 | MS. KOVNER | statute | So I think that move is made by ANILCA, the statute. |
| 0:34:51.640 | 2091.640 | MS. KOVNER | ANILCA | It's ANILCA-specific, because ANILCA says if you hold title to an interest, like a reserved water right interest, then that is a public land, and it can be regulated as public lands. |
| 0:35:01.740 | 2101.740 | MS. KOVNER | public lands | It's ANILCA-specific, because ANILCA says if you hold title to an interest, like a reserved water right interest, then that is a public land, and it can be regulated as public lands. |
| 0:35:07.900 | 2107.900 | JUSTICE SOTOMAYOR | waters | That gets you to regulating the waters in Federal -- in -- in -- in Federal units, because the U.S. under ANILCA only controls lands within the conservation units that are public lands. |
| 0:35:16.220 | 2116.220 | JUSTICE SOTOMAYOR | ANILCA | That gets you to regulating the waters in Federal -- in -- in -- in Federal units, because the U.S. under ANILCA only controls lands within the conservation units that are public lands. |
| 0:35:26.480 | 2126.480 | JUSTICE SOTOMAYOR | public lands | That gets you to regulating the waters in Federal -- in -- in -- in Federal units, because the U.S. under ANILCA only controls lands within the conservation units that are public lands. |
| 0:35:35.440 | 2135.440 | MS. KOVNER | waters | We only have authority to regulate the lands in which we have reserved water rights, and those are only waters within the park's units. |
| 0:35:36.800 | 2136.800 | MS. KOVNER | park | We only have authority to regulate the lands in which we have reserved water rights, and those are only waters within the park's units. |
| 0:35:39.520 | 2139.520 | JUSTICE SOTOMAYOR | hovercraft | So -- and does the no-hovercraft rule apply to the nonpublic lands? |
| 0:35:51.100 | 2151.100 | MS. KOVNER | hovercraft | No. The hovercraft rule only applies on public lands, and so it doesn't apply on inholdings. |
| 0:35:53.180 | 2153.180 | MS. KOVNER | public lands | No. The hovercraft rule only applies on public lands, and so it doesn't apply on inholdings. |
| 0:36:08.100 | 2168.100 | JUSTICE BREYER | hovercraft | -- that the hovercraft rule was like a rule that applies to all of Yosemite, say a campfire rule that applies even to John Jones's house. |
| 0:36:19.340 | 2179.340 | JUSTICE BREYER | navigable | I mean, it could be the navigable waters. |
| 0:36:19.760 | 2179.760 | JUSTICE BREYER | waters | I mean, it could be the navigable waters. |
| 0:36:31.180 | 2191.180 | MS. KOVNER | navigable | The first is on Federally-owned lands, and the second is on -- on navigable waters. |
| 0:36:31.900 | 2191.900 | MS. KOVNER | waters | The first is on Federally-owned lands, and the second is on -- on navigable waters. |
| 0:36:32.940 | 2192.940 | JUSTICE BREYER | navigable | I thought the navigable waters are not. |
| 0:36:33.480 | 2193.480 | JUSTICE BREYER | waters | I thought the navigable waters are not. |
| 0:36:39.220 | 2199.220 | JUSTICE BREYER | regulation | But you still have the authority to regulate them, because the regulation that does it is not a regulation that applies solely to public lands. |
| 0:36:42.220 | 2202.220 | JUSTICE BREYER | public lands | But you still have the authority to regulate them, because the regulation that does it is not a regulation that applies solely to public lands. |
| 0:36:48.180 | 2208.180 | MS. KOVNER | regulation | No. So the -- the way that the regulations are written as -- it's 1.2, and it -- it says they apply in two places: Federally-Owned lands, and also on navigable waters that are within the parks. |
| 0:36:57.100 | 2217.100 | MS. KOVNER | navigable | No. So the -- the way that the regulations are written as -- it's 1.2, and it -- it says they apply in two places: Federally-Owned lands, and also on navigable waters that are within the parks. |
| 0:36:57.500 | 2217.500 | MS. KOVNER | waters | No. So the -- the way that the regulations are written as -- it's 1.2, and it -- it says they apply in two places: Federally-Owned lands, and also on navigable waters that are within the parks. |
| 0:36:58.520 | 2218.520 | MS. KOVNER | park | No. So the -- the way that the regulations are written as -- it's 1.2, and it -- it says they apply in two places: Federally-Owned lands, and also on navigable waters that are within the parks. |
| 0:36:59.580 | 2219.580 | JUSTICE BREYER | navigable | Now, navigable waters that are within the boundaries of the National Park Service. |
| 0:37:00.180 | 2220.180 | JUSTICE BREYER | waters | Now, navigable waters that are within the boundaries of the National Park Service. |
| 0:37:02.880 | 2222.880 | JUSTICE BREYER | park | Now, navigable waters that are within the boundaries of the National Park Service. |
| 0:37:20.000 | 2240.000 | MS. KOVNER | navigable | Well, I think the -- the difficulty is, Your Honor, we think that the navigable waters are not like John Jones's house. |
| 0:37:20.340 | 2240.340 | MS. KOVNER | waters | Well, I think the -- the difficulty is, Your Honor, we think that the navigable waters are not like John Jones's house. |
| 0:37:42.280 | 2262.280 | JUSTICE BREYER | public lands | Either they are Federal lands and this is part of a reg that applies to Federal lands; or they are not Federal lands, in which case this reg applies to both nonfederal and -- I mean nonpublic lands and public lands. |
| 0:37:55.560 | 2275.560 | CHIEF JUSTICE ROBERTS | public lands | Well, but if that's right, I mean, it -- it -- it's right because the question is do these things apply solely to public lands. |
| 0:38:01.680 | 2281.680 | CHIEF JUSTICE ROBERTS | public lands | And you say, well, the second sentence doesn't matter because we say they don't apply solely to public lands. |
| 0:38:18.260 | 2298.260 | MS. KOVNER | waters | And in particular, we are acting here pursuant to an express grant of authority to regulate waters within the parks. |
| 0:38:19.320 | 2299.320 | MS. KOVNER | park | And in particular, we are acting here pursuant to an express grant of authority to regulate waters within the parks. |
| 0:38:20.960 | 2300.960 | JUSTICE ALITO | waters | Well, you -- you want to talk about waters, and -- and after this question I won't say anything more on this, but is the Ninth Circuit's holding limited to waters? |
| 0:38:31.740 | 2311.740 | JUSTICE ALITO | Alaska | The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. |
| 0:38:38.560 | 2318.560 | JUSTICE ALITO | park | The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. |
| 0:38:41.240 | 2321.240 | JUSTICE ALITO | regulation | The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. |
| 0:38:46.800 | 2326.800 | JUSTICE ALITO | Sturgeon | The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. |
| 0:38:49.180 | 2329.180 | JUSTICE ALITO | section | The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. |
| 0:38:51.640 | 2331.640 | JUSTICE ALITO | ANILCA | The -- the State of Alaska on page 20 and 21 of their brief cite a notice in the Federal Register by the Park Service in which they defend the regulation of nonfederal oil and gas activities on the basis of Sturgeon, on the ground that Section 103(c) of ANILCA applies only to Alaska-specific regulations. |
| 0:38:57.900 | 2337.900 | JUSTICE ALITO | Alaska | And since these are not Alaska-specific, those -- those regulations apply. |
| 0:39:00.140 | 2340.140 | JUSTICE ALITO | regulation | And since these are not Alaska-specific, those -- those regulations apply. |
| 0:39:04.700 | 2344.700 | JUSTICE ALITO | navigable | So they understand it to apply to something more than just navigable waters. |
| 0:39:05.280 | 2345.280 | JUSTICE ALITO | waters | So they understand it to apply to something more than just navigable waters. |
| 0:39:11.380 | 2351.380 | MS. KOVNER | regulation | So I think the long-standing interpretation for 20 years, so that in a notice and comment regulation of what this provision means, is that it only limits rules that are written solely to apply to public lands. |
| 0:39:17.160 | 2357.160 | MS. KOVNER | public lands | So I think the long-standing interpretation for 20 years, so that in a notice and comment regulation of what this provision means, is that it only limits rules that are written solely to apply to public lands. |
| 0:39:18.940 | 2358.940 | MS. KOVNER | park | And as to what the Park Service can do when it -- |
| 0:39:21.600 | 2361.600 | JUSTICE ALITO | Alaska | It's solely to apply to Alaska -- |
| 0:39:28.040 | 2368.040 | JUSTICE ALITO | Alaska | Solely to apply to nonpublic units to lands in Alaska. |
| 0:39:31.660 | 2371.660 | MS. KOVNER | regulation | The regulation, the 20-year regulation I'm alluding to, says if it's a rule that applies to both public and private lands, then it's not covered by this provision. |
| 0:39:57.340 | 2397.340 | JUSTICE SCALIA | park | The authority of the Park Service comes from the statute which authorizes the Secretary of Interior to, quote, "prescribe such regulations necessary or proper for the use and management of system units, including those concerning boating and other activities. |
| 0:39:59.240 | 2399.240 | JUSTICE SCALIA | statute | The authority of the Park Service comes from the statute which authorizes the Secretary of Interior to, quote, "prescribe such regulations necessary or proper for the use and management of system units, including those concerning boating and other activities. |
| 0:40:04.420 | 2404.420 | JUSTICE SCALIA | regulation | The authority of the Park Service comes from the statute which authorizes the Secretary of Interior to, quote, "prescribe such regulations necessary or proper for the use and management of system units, including those concerning boating and other activities. |
| 0:40:18.260 | 2418.260 | JUSTICE SCALIA | park | Only here the CSU's are park system units." |
| 0:40:40.780 | 2440.780 | JUSTICE SCALIA | public lands | "Only those lands within the boundaries of any conservation system unit which are public lands as such term is defined in this Act shall be deemed to be included as a portion of such unit." |
| 0:40:52.180 | 2452.180 | JUSTICE SCALIA | park | If it's not within the unit, it's not within the basic authority of the Park Service to issue regulations, period. |
| 0:40:53.740 | 2453.740 | JUSTICE SCALIA | regulation | If it's not within the unit, it's not within the basic authority of the Park Service to issue regulations, period. |
| 0:41:11.360 | 2471.360 | MS. KOVNER | regulation | So if I could walk through that authority that Your Honor is discussing and show why it allows us to enact the regulation here. |
| 0:41:20.500 | 2480.500 | MS. KOVNER | park | I agree, Your Honor, that the authority under (a) is general authority to prescribe only those rules that are necessary for the protection of the system units, meaning the parks. |
| 0:41:30.640 | 2490.640 | JUSTICE SOTOMAYOR | waters | You're -- you're conceding that the waters are outside of that? |
| 0:41:36.160 | 2496.160 | MS. KOVNER | public lands | I'm conceding -- well, we haven't -- our first argument, Your Honor, is that no, these are public lands. |
| 0:41:42.380 | 2502.380 | MS. KOVNER | public lands | But if -- I think Justice Scalia's premise is what is our authority to regulate if they are not public lands. |
| 0:41:50.200 | 2510.200 | MS. KOVNER | waters | It has always been understood to allow us to regulate waters that are within the boundaries of the parks regardless of who owns them. |
| 0:41:52.560 | 2512.560 | MS. KOVNER | park | It has always been understood to allow us to regulate waters that are within the boundaries of the parks regardless of who owns them. |
| 0:42:02.960 | 2522.960 | MS. KOVNER | waters | And just to focus on the language of it, it's a very specific express grant of authority to regulate waters within parks. |
| 0:42:03.700 | 2523.700 | MS. KOVNER | park | And just to focus on the language of it, it's a very specific express grant of authority to regulate waters within parks. |
| 0:42:05.220 | 2525.220 | MS. KOVNER | park | It says we can -- the Park Service can enact rules, quote, "concerning boating and other activities, not just on but also relating to waters that are located within" -- |
| 0:42:12.240 | 2532.240 | MS. KOVNER | waters | It says we can -- the Park Service can enact rules, quote, "concerning boating and other activities, not just on but also relating to waters that are located within" -- |
| 0:42:34.400 | 2554.400 | JUSTICE BREYER | public lands | Now, only those lands within the boundaries of any conservation system which are public -- within the boundaries of any conservation system which are public lands shall be deemed to be included as a portion of the unit. |
| 0:43:17.240 | 2597.240 | MS. KOVNER | statute | The statutes that Congress has enacted draw a distinction between land that is within the boundaries of the unit, which includes private lands, and lands -- |
| 0:43:49.000 | 2629.000 | JUSTICE SCALIA | regulation | You're quoting from the regulations -- |
| 0:43:50.660 | 2630.660 | JUSTICE SCALIA | statute | -- right from the statute. |
| 0:43:55.000 | 2635.000 | MS. KOVNER | statute | From -- so on 7a of our appendix, it's a statute. |
| 0:43:56.120 | 2636.120 | MS. KOVNER | statute | It's a statute that was enacted in 1976, and it expressly grants the Park Service the authority to enact rules concerning boating and other activities on or relating to waters. |
| 0:44:00.280 | 2640.280 | MS. KOVNER | park | It's a statute that was enacted in 1976, and it expressly grants the Park Service the authority to enact rules concerning boating and other activities on or relating to waters. |
| 0:44:07.440 | 2647.440 | MS. KOVNER | waters | It's a statute that was enacted in 1976, and it expressly grants the Park Service the authority to enact rules concerning boating and other activities on or relating to waters. |
| 0:44:09.140 | 2649.140 | JUSTICE SOTOMAYOR | statute | Can you tell me whether that statute violates this statute? |
| 0:44:17.580 | 2657.580 | MS. KOVNER | park | I think that's -- I think it's whether this provision prohibits the Park Service from exercising that authority or whether -- |
| 0:44:34.300 | 2674.300 | MS. KOVNER | public lands | And the text says you can't apply on lands that were conveyed to the State or to private parties those rules that are applicable solely to public lands within conservation system units. |
| 0:44:47.120 | 2687.120 | JUSTICE SCALIA | regulation | It's a regulation. |
| 0:44:49.940 | 2689.940 | MS. KOVNER | statute | It is -- it is a statute. |
| 0:44:59.100 | 2699.100 | JUSTICE SCALIA | regulation | It's -- it says regulations -- oh, I see. |
| 0:45:01.780 | 2701.780 | JUSTICE SCALIA | statute | The statute is addressing regulations. |
| 0:45:02.960 | 2702.960 | JUSTICE SCALIA | regulation | The statute is addressing regulations. |
| 0:45:05.060 | 2705.060 | JUSTICE SCALIA | statute | That's the subtitle in the statute. |
| 0:45:13.180 | 2713.180 | MS. KOVNER | park | Is -- is this authority one that gives the Park Service the ability to regulate lands whether they are public or private? |
| 0:45:20.420 | 2720.420 | MS. KOVNER | regulation | And as a result, this is not a regulation -- if you think that waters within the parks are private lands, this is not the kind of regulation that's carved out by the text. |
| 0:45:22.180 | 2722.180 | MS. KOVNER | waters | And as a result, this is not a regulation -- if you think that waters within the parks are private lands, this is not the kind of regulation that's carved out by the text. |
| 0:45:23.080 | 2723.080 | MS. KOVNER | park | And as a result, this is not a regulation -- if you think that waters within the parks are private lands, this is not the kind of regulation that's carved out by the text. |
| 0:45:33.740 | 2733.740 | MS. KOVNER | statute | And if you also look to other provisions of the statute, it confirms it in two ways, if I could just focuses on two of them. |
| 0:45:42.020 | 2742.020 | MS. KOVNER | statute | The first is, if you look at the management plan of the statute of ANILCA, it expressly contemplates that the Park Service is going to be able to regulate private lands under some circumstances. |
| 0:45:42.660 | 2742.660 | MS. KOVNER | ANILCA | The first is, if you look at the management plan of the statute of ANILCA, it expressly contemplates that the Park Service is going to be able to regulate private lands under some circumstances. |
| 0:45:45.480 | 2745.480 | MS. KOVNER | park | The first is, if you look at the management plan of the statute of ANILCA, it expressly contemplates that the Park Service is going to be able to regulate private lands under some circumstances. |
| 0:46:03.660 | 2763.660 | MS. KOVNER | regulation | And it does that by saying, you need your management plan to describe the activities that are occurring on private lands and to describe any methods you're going to use -- the methods you're going to use to control those activities, including, quote, "issuance or enforcement of regulations." |
| 0:46:07.460 | 2767.460 | JUSTICE KAGAN | section | And if I'm looking at the right section, I mean, I would have thought that that was key to your argument, because it says in these management plans what you need is a -- is a "description of privately owned areas which are within such unit." |
| 0:46:35.200 | 2795.200 | JUSTICE KAGAN | regulation | And then as you say, it goes on and says we want in these plans some idea of what regulations are going to be applying on those private lands within the unit. |
| 0:46:43.760 | 2803.760 | MS. KOVNER | statute | And if I could just focus on the one other part of the statute that confirms that this reading is correct, that the Park Service isn't being stripped of its preexisting authority to regulate rivers. |
| 0:46:47.780 | 2807.780 | MS. KOVNER | park | And if I could just focus on the one other part of the statute that confirms that this reading is correct, that the Park Service isn't being stripped of its preexisting authority to regulate rivers. |
| 0:46:50.840 | 2810.840 | MS. KOVNER | river | And if I could just focus on the one other part of the statute that confirms that this reading is correct, that the Park Service isn't being stripped of its preexisting authority to regulate rivers. |
| 0:46:53.440 | 2813.440 | MS. KOVNER | statute | It's if you look at the other provisions of the statute that very clearly confirm the Park Service is going to have the authority to regulate rivers. |
| 0:46:56.360 | 2816.360 | MS. KOVNER | park | It's if you look at the other provisions of the statute that very clearly confirm the Park Service is going to have the authority to regulate rivers. |
| 0:46:58.500 | 2818.500 | MS. KOVNER | river | It's if you look at the other provisions of the statute that very clearly confirm the Park Service is going to have the authority to regulate rivers. |
| 0:47:04.020 | 2824.020 | MS. KOVNER | park | The first is, when Congress is setting aside land for parks -- and let me use the park here as an example -- it states it's -- its purposes. |
| 0:47:10.900 | 2830.900 | MS. KOVNER | Yukon | So it says "We are creating here the Yukon-Charley Rivers Preserve. |
| 0:47:11.760 | 2831.760 | MS. KOVNER | river | So it says "We are creating here the Yukon-Charley Rivers Preserve. |
| 0:47:20.220 | 2840.220 | MS. KOVNER | Yukon | And our purposes are to ensure the protection of," quote, "the entire Yukon-Charley basin, including the lakes and the streams. |
| 0:47:26.000 | 2846.000 | MS. KOVNER | park | So that provision confirms that Congress is contemplating by setting aside this land as parks, we're going to have this preexisting authority to regulate waters within the parks still in place. |
| 0:47:29.280 | 2849.280 | MS. KOVNER | waters | So that provision confirms that Congress is contemplating by setting aside this land as parks, we're going to have this preexisting authority to regulate waters within the parks still in place. |
| 0:47:34.820 | 2854.820 | MS. KOVNER | river | And just one other example of these provisions is the Wild and Scenic River Act provisions that are in the statute. |
| 0:47:36.960 | 2856.960 | MS. KOVNER | statute | And just one other example of these provisions is the Wild and Scenic River Act provisions that are in the statute. |
| 0:47:42.880 | 2862.880 | MS. KOVNER | river | And Congress sets aside as a special type of conservation system unit wild and scenic rivers. |
| 0:47:44.800 | 2864.800 | MS. KOVNER | river | These are entirely composed of rivers. |
| 0:47:45.900 | 2865.900 | MS. KOVNER | park | And says, Park Service, you are supposed to protect those pursuant to your Organic Act authority in these wild and scenic water provisions. |
| 0:48:07.040 | 2887.040 | CHIEF JUSTICE ROBERTS | park | What does -- you -- on page 24, and I think you have mentioned this several times, so -- you talk about this isn't a problem because your authority is circumscribed and you have the inholdings are -- have substantial protections against Park Service regulation. |
| 0:48:07.740 | 2887.740 | CHIEF JUSTICE ROBERTS | regulation | What does -- you -- on page 24, and I think you have mentioned this several times, so -- you talk about this isn't a problem because your authority is circumscribed and you have the inholdings are -- have substantial protections against Park Service regulation. |
| 0:48:16.040 | 2896.040 | MS. KOVNER | statute | So I want to make clear, our authority is very narrow, and we can only regulate where there is some statute that authorizes us to regulate inholdings and -- |
| 0:48:20.640 | 2900.640 | CHIEF JUSTICE ROBERTS | statute | Do you -- do you think the statute that authorizes you to regulate is the one that says "the Secretary shall prescribe such regulations as the Secretary considers necessary or proper"? |
| 0:48:26.540 | 2906.540 | CHIEF JUSTICE ROBERTS | regulation | Do you -- do you think the statute that authorizes you to regulate is the one that says "the Secretary shall prescribe such regulations as the Secretary considers necessary or proper"? |
| 0:48:56.640 | 2936.640 | MS. KOVNER | park | And so, for example, if the Park Service regulates some activity on private lands that is going to cause danger or harm to the system units that's -- that adjoins them, that's the only circumstance in which authority to regulate -- |
| 0:49:16.420 | 2956.420 | MS. KOVNER | park | We think it's clear that the Park Service can't simply treat inholdings as though they were public lands. |
| 0:49:19.420 | 2959.420 | MS. KOVNER | public lands | We think it's clear that the Park Service can't simply treat inholdings as though they were public lands. |
| 0:49:21.500 | 2961.500 | MS. KOVNER | park | And the only case in which the Park Service has tried to use its authority to regulate inholdings under that provision is this case where there is going to be some kind of harm to the actual public lands that befalls the park's units. |
| 0:49:28.720 | 2968.720 | MS. KOVNER | public lands | And the only case in which the Park Service has tried to use its authority to regulate inholdings under that provision is this case where there is going to be some kind of harm to the actual public lands that befalls the park's units. |
| 0:49:35.820 | 2975.820 | JUSTICE KENNEDY | regulation | But is that true even if it's a -- the regulation is nation -- applicable nationwide? |
| 0:49:42.100 | 2982.100 | MS. KOVNER | park | We think that nationwide, yes, the Park Service's authority to regulate inholdings is quite limited. |
| 0:50:02.400 | 3002.400 | MS. KOVNER | regulation | I think that we think -- and we've said for 20 years in a regulation that's entitled the Chevron difference that what the "solely" phrase does is it carves out the rules that are applicable solely to public lands. |
| 0:50:09.340 | 3009.340 | MS. KOVNER | public lands | I think that we think -- and we've said for 20 years in a regulation that's entitled the Chevron difference that what the "solely" phrase does is it carves out the rules that are applicable solely to public lands. |
| 0:50:43.200 | 3043.200 | MS. KOVNER | regulation | I mean, there's a -- it's been a very long-standing limitation on how this has been construed that we're not going beyond the kinds of regulations I've described to pervasive regulation. |
| 0:50:49.000 | 3049.000 | MS. KOVNER | section | There might be, if we tried to interpret our authority under this section more broadly, there might be a clear statement problem then, but there's certainly no clear statement problem -- |
| 0:51:14.520 | 3074.520 | JUSTICE SOTOMAYOR | regulation | Some might argue that your proposed regulations on oil contravene the intent of this provision. |
| 0:51:31.740 | 3091.740 | MS. KOVNER | regulation | I -- I think Your Honor is right, that some people might say that that's not an appropriate regulation, and they will be able to challenge it nationwide as not an appropriate exercise of our authority. |
| 0:51:45.500 | 3105.500 | MS. KOVNER | park | But what's never been disputed in this case is that, in general, under the 1976 Act, this very specific authorization of the Park Service to regulate waters within units, we have the authority to regulate waters in units -- |
| 0:51:46.360 | 3106.360 | MS. KOVNER | waters | But what's never been disputed in this case is that, in general, under the 1976 Act, this very specific authorization of the Park Service to regulate waters within units, we have the authority to regulate waters in units -- |
| 0:52:00.060 | 3120.060 | JUSTICE ALITO | section | What can you do about why this provision that you -- you reproduce on 7a gets around the first section of 103(c)? |
| 0:52:04.720 | 3124.720 | JUSTICE ALITO | regulation | This -- that provision allows regulation of waters within Service units, but the first section, as I read it, says that nonpublic land within the boundaries of -- of a CSU is not part of the CSU. |
| 0:52:06.220 | 3126.220 | JUSTICE ALITO | waters | This -- that provision allows regulation of waters within Service units, but the first section, as I read it, says that nonpublic land within the boundaries of -- of a CSU is not part of the CSU. |
| 0:52:08.540 | 3128.540 | JUSTICE ALITO | section | This -- that provision allows regulation of waters within Service units, but the first section, as I read it, says that nonpublic land within the boundaries of -- of a CSU is not part of the CSU. |
| 0:52:30.860 | 3150.860 | MS. KOVNER | waters | And just to read the language, it's concerning boating or other activities on or relating to waters located within system units. |
| 0:52:35.300 | 3155.300 | MS. KOVNER | regulation | And that's always been understood to allow the regulation of all the waters in system units, regardless of their ownership. |
| 0:52:36.240 | 3156.240 | MS. KOVNER | waters | And that's always been understood to allow the regulation of all the waters in system units, regardless of their ownership. |
| 0:52:41.820 | 3161.820 | MS. KOVNER | river | And I think it makes sense, because you can't regulate or protect a river piecemeal, stretch by stretch. |
| 0:52:45.980 | 3165.980 | MS. KOVNER | river | If Congress -- when Congress set aside these rivers and said the Park Service is going to be able to protect the entire river and stream and basin, protecting the rivers and streams and basins that are Federal property is going to require setting a rule for the whole river, and enforcing the rule on the whole -- |
| 0:52:46.740 | 3166.740 | MS. KOVNER | park | If Congress -- when Congress set aside these rivers and said the Park Service is going to be able to protect the entire river and stream and basin, protecting the rivers and streams and basins that are Federal property is going to require setting a rule for the whole river, and enforcing the rule on the whole -- |
| 0:52:59.220 | 3179.220 | JUSTICE SCALIA | statute | 100751 is a general statute; it applies everywhere, right? |
| 0:53:04.040 | 3184.040 | JUSTICE SCALIA | section | And -- and 3101, Section 103 is specific to Alaska, isn't it? |
| 0:53:06.280 | 3186.280 | JUSTICE SCALIA | Alaska | And -- and 3101, Section 103 is specific to Alaska, isn't it? |
| 0:53:16.460 | 3196.460 | JUSTICE SCALIA | Alaska | So this general provision is limited by what Congress has said about Alaska. |
| 0:53:21.920 | 3201.920 | JUSTICE SCALIA | public lands | And that sentence says, "Only those lines within the boundaries of any CSU which are public lands shall be deemed to be included as a portion of such unit." |
| 0:53:32.980 | 3212.980 | JUSTICE SCALIA | park | And if you read that back into 100751, it seems to me the Park Service doesn't have jurisdiction. |
| 0:53:47.360 | 3227.360 | MS. KOVNER | park | So then we look to the Park Service's authorities and we say, does the Park Service's authority depend on this water being part of the unit? |
| 0:54:03.100 | 3243.100 | MS. KOVNER | waters | And the answer is no. If you look at (b), it's an authorization to impose rules concerning boating and -- and other activities on or relating to waters located within. |
| 0:54:04.560 | 3244.560 | JUSTICE BREYER | regulation | The regulation itself says, it says water -- "Hovercraft regulation applies to, quote, 'waters subject to the jurisdiction of the United States within the boundaries of the National Park Service.'" |
| 0:54:09.360 | 3249.360 | JUSTICE BREYER | hovercraft | The regulation itself says, it says water -- "Hovercraft regulation applies to, quote, 'waters subject to the jurisdiction of the United States within the boundaries of the National Park Service.'" |
| 0:54:12.360 | 3252.360 | JUSTICE BREYER | waters | The regulation itself says, it says water -- "Hovercraft regulation applies to, quote, 'waters subject to the jurisdiction of the United States within the boundaries of the National Park Service.'" |
| 0:54:18.680 | 3258.680 | JUSTICE BREYER | park | The regulation itself says, it says water -- "Hovercraft regulation applies to, quote, 'waters subject to the jurisdiction of the United States within the boundaries of the National Park Service.'" |
| 0:54:21.460 | 3261.460 | JUSTICE BREYER | park | And then the National Park Service somewhere has a definition that equates it with the unit. |
| 0:54:27.980 | 3267.980 | JUSTICE BREYER | park | The National Park Service is defined identically to system units. |
| 0:54:48.000 | 3288.000 | JUSTICE BREYER | public lands | So if we -- Justice Scalia's point is this seems to take the private land, the in-holdings, and say they're not part of the unit; only the public lands are part of the unit -- |
| 0:54:50.760 | 3290.760 | JUSTICE BREYER | hovercraft | -- and then the Hovercraft Regulation applies only to the unit. |
| 0:54:51.240 | 3291.240 | JUSTICE BREYER | regulation | -- and then the Hovercraft Regulation applies only to the unit. |
| 0:55:04.180 | 3304.180 | MS. KOVNER | regulation | So I think Your Honor's suggesting that the regulations themselves say they don't apply -- |
| 0:55:13.640 | 3313.640 | MS. KOVNER | park | There's this distinction between what's within the boundaries of the park and what is park lands. |
| 0:55:19.180 | 3319.180 | MS. KOVNER | section | And Your -- Your Honor, this is established in Section 103, among other places, where it talks about whether land is within the boundaries of the system unit -- |
| 0:55:25.384 | 3325.384 | MS. KOVNER | park | -- versus being within the park. |
| 0:55:34.940 | 3334.940 | JUSTICE BREYER | drafted | Who drafted this? |
| 0:55:40.900 | 3340.900 | MS. KOVNER | regulation | And to be clear, there's never been any -- to be clear, there's never been any dispute that the regulations are written to apply to these lands. |
| 0:55:44.980 | 3344.980 | MS. KOVNER | section | The only question in this case is whether Section 103 strips that authority. |
| 0:55:52.860 | 3352.860 | JUSTICE SOTOMAYOR | statute | So if Congress passed a new statute, it could limit or expand 103 as it chose, correct? |
| 0:56:01.300 | 3361.300 | MS. KOVNER | section | And Your Honor, just -- if I could leave the Court with -- I mean, in interpreting Section 103, this provision that talks about rules solely applicable to public lands, and whether that removes the Park Service's preexisting authority to regulate waters in the parks, I would just ask the Court to look to all the other provisions of the statute that clearly contemplate -- of ANILCA, the statute -- that clearly contemplate the Park Service is going to retain the authority to protect park's waters. |
| 0:56:05.680 | 3365.680 | MS. KOVNER | public lands | And Your Honor, just -- if I could leave the Court with -- I mean, in interpreting Section 103, this provision that talks about rules solely applicable to public lands, and whether that removes the Park Service's preexisting authority to regulate waters in the parks, I would just ask the Court to look to all the other provisions of the statute that clearly contemplate -- of ANILCA, the statute -- that clearly contemplate the Park Service is going to retain the authority to protect park's waters. |
| 0:56:08.240 | 3368.240 | MS. KOVNER | park | And Your Honor, just -- if I could leave the Court with -- I mean, in interpreting Section 103, this provision that talks about rules solely applicable to public lands, and whether that removes the Park Service's preexisting authority to regulate waters in the parks, I would just ask the Court to look to all the other provisions of the statute that clearly contemplate -- of ANILCA, the statute -- that clearly contemplate the Park Service is going to retain the authority to protect park's waters. |
| 0:56:10.300 | 3370.300 | MS. KOVNER | waters | And Your Honor, just -- if I could leave the Court with -- I mean, in interpreting Section 103, this provision that talks about rules solely applicable to public lands, and whether that removes the Park Service's preexisting authority to regulate waters in the parks, I would just ask the Court to look to all the other provisions of the statute that clearly contemplate -- of ANILCA, the statute -- that clearly contemplate the Park Service is going to retain the authority to protect park's waters. |
| 0:56:14.500 | 3374.500 | MS. KOVNER | statute | And Your Honor, just -- if I could leave the Court with -- I mean, in interpreting Section 103, this provision that talks about rules solely applicable to public lands, and whether that removes the Park Service's preexisting authority to regulate waters in the parks, I would just ask the Court to look to all the other provisions of the statute that clearly contemplate -- of ANILCA, the statute -- that clearly contemplate the Park Service is going to retain the authority to protect park's waters. |
| 0:56:16.540 | 3376.540 | MS. KOVNER | ANILCA | And Your Honor, just -- if I could leave the Court with -- I mean, in interpreting Section 103, this provision that talks about rules solely applicable to public lands, and whether that removes the Park Service's preexisting authority to regulate waters in the parks, I would just ask the Court to look to all the other provisions of the statute that clearly contemplate -- of ANILCA, the statute -- that clearly contemplate the Park Service is going to retain the authority to protect park's waters. |
| 0:56:24.420 | 3384.420 | JUSTICE ALITO | river | Let's say that part of a river is within a CSU. |
| 0:56:28.140 | 3388.140 | JUSTICE ALITO | statute | And do you read this statute to mean that the --the Park Service could regulate boating 500 miles downstream from that part of the -- on that river, because it's relating to waters that are within the CSU? |
| 0:56:30.040 | 3390.040 | JUSTICE ALITO | park | And do you read this statute to mean that the --the Park Service could regulate boating 500 miles downstream from that part of the -- on that river, because it's relating to waters that are within the CSU? |
| 0:56:36.540 | 3396.540 | JUSTICE ALITO | river | And do you read this statute to mean that the --the Park Service could regulate boating 500 miles downstream from that part of the -- on that river, because it's relating to waters that are within the CSU? |
| 0:56:38.520 | 3398.520 | JUSTICE ALITO | waters | And do you read this statute to mean that the --the Park Service could regulate boating 500 miles downstream from that part of the -- on that river, because it's relating to waters that are within the CSU? |
| 0:56:41.160 | 3401.160 | MS. KOVNER | park | The Park Service has -- has consistently understood its authority to be regulating the park's -- within the park's boundaries. |
| 0:56:48.240 | 3408.240 | MS. KOVNER | regulation | It's never sought to enact a regulation outside of the park's boundaries. |
| 0:56:49.900 | 3409.900 | MS. KOVNER | park | It's never sought to enact a regulation outside of the park's boundaries. |
| 0:56:55.600 | 3415.600 | MS. KOVNER | park | But this 1976 provision has uniformly been understood to confer on the Park Service -- |
| 0:57:04.940 | 3424.940 | JUSTICE BREYER | regulation | Two, the second sentence does not bar this regulation. |
| 0:57:39.200 | 3459.200 | MS. KOVNER | public lands | Your Honor, this case could be sent back to address both that and to address the question of what is public lands, which is a question that wasn't addressed below. |
| 0:57:55.420 | 3475.420 | MS. KOVNER | park | And we think it would be sufficient to say the second sentence doesn't -- the text clearly indicates the second sentence doesn't prohibit the application of those rules that are validly written to apply to both public and private lands within the parks. |
| 0:57:56.260 | 3476.260 | MS. KOVNER | regulation | This regulation is a rule that's been written to apply, regardless of who owns the lands in the parks. |
| 0:57:59.820 | 3479.820 | MS. KOVNER | park | This regulation is a rule that's been written to apply, regardless of who owns the lands in the parks. |
| 0:58:42.860 | 3522.860 | MS. KOVNER | statute | And "conservation system units" is defined in the statute to be parks units in Alaska. |
| 0:58:43.780 | 3523.780 | MS. KOVNER | park | And "conservation system units" is defined in the statute to be parks units in Alaska. |
| 0:58:44.400 | 3524.400 | MS. KOVNER | Alaska | And "conservation system units" is defined in the statute to be parks units in Alaska. |
| 0:58:47.180 | 3527.180 | MS. KOVNER | regulation | And we think, yes, the plain text of this regulation only limits those kinds of rules. |
| 0:58:58.600 | 3538.600 | JUSTICE ALITO | Alaska | So if there's a rule that applies to conservation -- it applies to Alaska, and it applies to the National Mall, that would be that you can't have a Hovercraft in Alaska or in the tidal basin. |
| 0:59:03.320 | 3543.320 | JUSTICE ALITO | hovercraft | So if there's a rule that applies to conservation -- it applies to Alaska, and it applies to the National Mall, that would be that you can't have a Hovercraft in Alaska or in the tidal basin. |
| 0:59:22.880 | 3562.880 | MS. KOVNER | ANILCA | And the reason I don't think that's ridiculous or irrational, Your Honor, is because when ANILCA was enacted, there was a very well-settled regulatory regime that didn't subject private lands to any kind of plenary authority. |
| 0:59:40.160 | 3580.160 | MS. KOVNER | park | And what it was concerned about was that the Park Service would deviate from that approach in Alaska when these new lands were added. |
| 0:59:42.120 | 3582.120 | MS. KOVNER | Alaska | And what it was concerned about was that the Park Service would deviate from that approach in Alaska when these new lands were added. |
| 1:00:17.280 | 3617.280 | MR. FINDLEY | ANILCA | It's about to be surrounded by these ANILCA parks. |
| 1:00:17.660 | 3617.660 | MR. FINDLEY | park | It's about to be surrounded by these ANILCA parks. |
| 1:00:20.220 | 3620.220 | MR. FINDLEY | section | What does 1 -- Section 103(c) doing? |
| 1:00:23.280 | 3623.280 | MR. FINDLEY | ANILCA | It is saying before ANILCA was passed, you're not part of the park and you're not subject to Park Service regulation. |
| 1:00:25.220 | 3625.220 | MR. FINDLEY | park | It is saying before ANILCA was passed, you're not part of the park and you're not subject to Park Service regulation. |
| 1:00:27.380 | 3627.380 | MR. FINDLEY | regulation | It is saying before ANILCA was passed, you're not part of the park and you're not subject to Park Service regulation. |
| 1:00:29.120 | 3629.120 | MR. FINDLEY | ANILCA | The day after ANILCA was part -- excuse me. |
| 1:00:29.600 | 3629.600 | MR. FINDLEY | ANILCA | The day after ANILCA is passed, you're still not part of the park and you're still not subject to Park Service regulation. |
| 1:00:33.120 | 3633.120 | MR. FINDLEY | park | The day after ANILCA is passed, you're still not part of the park and you're still not subject to Park Service regulation. |
| 1:00:35.420 | 3635.420 | MR. FINDLEY | regulation | The day after ANILCA is passed, you're still not part of the park and you're still not subject to Park Service regulation. |
| 1:00:45.220 | 3645.220 | MR. FINDLEY | regulation | They're relying on the Organic Act which allows them to enact any regulations they feel necessary at any time. |
| 1:00:51.000 | 3651.000 | MR. FINDLEY | regulation | They've already done that with the 9(b) oil and gas regulations, seeking to apply those to non-Federal land within Alaska. |
| 1:00:55.460 | 3655.460 | MR. FINDLEY | Alaska | They've already done that with the 9(b) oil and gas regulations, seeking to apply those to non-Federal land within Alaska. |
| 1:01:04.980 | 3664.980 | MR. FINDLEY | park | And the hits are going to keep on coming unless this Court stops this interpretation and goes back to what 103(c) was meant to do, which was to prevent the Park Service from taking these lands that aren't owned by the government and regulating them as though they are part of the park. |
| 1:01:16.020 | 3676.020 | MR. FINDLEY | ANILCA | And the second point want -- I -- I want to make -- I imagine about 45 seconds at this point: There's a lot of discussion about whether ANILCA covers navigable waters or not. |
| 1:01:16.840 | 3676.840 | MR. FINDLEY | navigable | And the second point want -- I -- I want to make -- I imagine about 45 seconds at this point: There's a lot of discussion about whether ANILCA covers navigable waters or not. |
| 1:01:17.300 | 3677.300 | MR. FINDLEY | waters | And the second point want -- I -- I want to make -- I imagine about 45 seconds at this point: There's a lot of discussion about whether ANILCA covers navigable waters or not. |
| 1:01:24.160 | 3684.160 | MR. FINDLEY | statute | And in that circumstance, it's a question of is anything in the statute clearly saying we are taking away State authority over navigable waters? |
| 1:01:27.960 | 3687.960 | MR. FINDLEY | navigable | And in that circumstance, it's a question of is anything in the statute clearly saying we are taking away State authority over navigable waters? |
| 1:01:28.460 | 3688.460 | MR. FINDLEY | waters | And in that circumstance, it's a question of is anything in the statute clearly saying we are taking away State authority over navigable waters? |
| 1:01:30.300 | 3690.300 | MR. FINDLEY | navigable | You will not find the term navigable waters in the statute once. |
| 1:01:30.880 | 3690.880 | MR. FINDLEY | waters | You will not find the term navigable waters in the statute once. |
| 1:01:31.560 | 3691.560 | MR. FINDLEY | statute | You will not find the term navigable waters in the statute once. |
| 1:01:34.180 | 3694.180 | MR. FINDLEY | park | Let's contrast this to other park-enabling legislation. |
| 1:01:37.480 | 3697.480 | MR. FINDLEY | park | This is for Olympic National Park, and you'll find this at 16 U.S.C. |
| 1:01:44.060 | 3704.060 | MR. FINDLEY | park | And here's what it says: "The boundary of Olympic National Park Washington is" -- if I may just finish the quote -- "is hereby revised to" -- "is hereby revised to include within the park all submerged lands and waters of Lake Ozette, Washington, and the Ozette River, Washington." |
| 1:01:52.780 | 3712.780 | MR. FINDLEY | waters | And here's what it says: "The boundary of Olympic National Park Washington is" -- if I may just finish the quote -- "is hereby revised to" -- "is hereby revised to include within the park all submerged lands and waters of Lake Ozette, Washington, and the Ozette River, Washington." |
| 1:01:55.720 | 3715.720 | MR. FINDLEY | river | And here's what it says: "The boundary of Olympic National Park Washington is" -- if I may just finish the quote -- "is hereby revised to" -- "is hereby revised to include within the park all submerged lands and waters of Lake Ozette, Washington, and the Ozette River, Washington." |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.800 to 0:03:06.800, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.800] MR. FINDLEY: Thank you, Mr. Chief Justice, and may it please the Court: ANILCA was the result of a grand bargain. Congress enacted ANILCA to finally resolve land ownership in Alaska, a process that began with the Statehood Act and continued with the Native Claims Settlement Act, both statutes that granted land to the State and native corporations to further economic development and self-sufficiency for Alaska and its people. ANILCA very carefully balanced conservation with those important goals.

[0:00:40.160] JUSTICE KAGAN: Mr. -- Mr. Findley, can I ask two quick clarifying questions just so I understand what's at issue here? Your argument applies to the navigable rivers generally; is that right? In other words, to the navigable rivers running through the federally owned land as well as to those running through the inholdings?

[0:01:00.600] MR. FINDLEY: If a navigable river is surrounded by the outer boundaries of the park, yes, that's covered by Section 103(c).

[0:01:06.140] JUSTICE KAGAN: And is there any information in the record about whether your client actually was running his boat on the portions which were -- are within the federally owned parts, or instead it's the inholdings? Is that what you called them?

[0:01:23.320] MR. FINDLEY: That is one word for it.

[0:01:24.260] JUSTICE KAGAN: Yes.

[0:01:24.260] MR. FINDLEY: He was within the shore. On either side of where his hovercraft was stopped was Federal public land.

[0:01:30.040] JUSTICE KAGAN: Was Federal --

[0:01:30.340] MR. FINDLEY: Yes.

[0:01:30.720] JUSTICE KAGAN: Was Federal public land?

[0:01:32.300] MR. FINDLEY: Yes, exactly.

[0:01:32.900] JUSTICE KAGAN: Okay. Thank you.

[0:01:33.944] MR. FINDLEY: Oh, sure.

[0:01:34.640] JUSTICE KENNEDY: Just, again, a preliminary question.

[0:01:36.440] MR. FINDLEY: Sure.

[0:01:37.040] JUSTICE KENNEDY: Is it conceded by all or is it not that this is navigable -- that these are navigable waters?

[0:01:42.180] MR. FINDLEY: Yes. And the Ninth Circuit issued decision in 2001 called Alaska v. United States by Judge Kleinfeld which adjudicated the Nation River navigable.

[0:01:49.180] JUSTICE KENNEDY: And that's not contested here?

[0:01:50.580] MR. FINDLEY: No, it is not contested here.

[0:01:51.680] JUSTICE SOTOMAYOR: So you're claiming a right not merely to use the hovercraft in the nonpublic lands. You're claiming that there's no residual right to control navigable waters in the Federal lands area?

[0:02:08.660] MR. FINDLEY: What Mr. Sturgeon is arguing -- we've been very specific about that -- is that the Park Service does not have authority to issue its Park Management Regulations to cover State navigable waters that run through these ANILCA parks.

[0:02:21.180] JUSTICE SOTOMAYOR: So what do you do about the ANILCA provision that says that boating and other water activities within public lands, within Federal public lands can be regulated?

[0:02:36.960] MR. FINDLEY: Yes. And those apply to all kinds of waters that are not navigable. Those apply to Federal waters and those --

[0:02:43.280] JUSTICE SOTOMAYOR: That's not what it says. It says any waters in the jurisdiction of the United States.

[0:02:48.140] MR. FINDLEY: It doesn't say navigable waters. And there is --

[0:02:51.500] JUSTICE SOTOMAYOR: Well, it could apply to both, is what I'm saying. What says it excludes navigable waters?

[0:02:56.440] MR. FINDLEY: You turn back to the definition of public lands in the statute, which makes clear for anything to be public lands, the United States must hold title. And there really is no dispute. The United States

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 22, 2016.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2015/14-1209
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2015/14-1209/14-1209_20160322-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.7 MB)
- Length: 0:07:02.034 (422.034 s)
- Words: 996, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (1 turn), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 974 of Whisper's 996 words (97.8%; Oyez has 992).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:07:00.800 | 984 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court in Case 14-1209, Sturgeon v. Frost. For almost 40 years, John Sturgeon has hunted moose along the Nation River in Alaska. Parts of the river are shallow and difficult to navigate, so he travels by hovercraft. While hunting in 2007, Sturgeon piloted his hovercraft over a stretch of the Nation River that flows through the Yukon-Charlie River's National Preserve. The Yukon-Charlie Preserve is a conservation system unit located in Alaska that is managed by the National Park Service. Alaska law permits the use of hovercraft. Park Service regulations do not. Park Service rangers approached Sturgeon, informing him that hovercraft were prohibited within the preserve under Park Service regulations. Sturgeon protested that the regulations did not apply because the river itself was owned by the State of Alaska, not the Federal Government. The rangers were unmoved and ordered Sturgeon to take his hovercraft out of the preserve. He complied, heading home without a moose. Sturgeon filed suit against the Park Service in the United States District Court for the District of Alaska, seeking declaratory and injunctive relief permitting him to operate his hovercraft within the boundaries of the Yukon-Charlie Preserve. Alaska intervened in support of Sturgeon. Now, land management is a complicated issue in Alaska arising from its unique history. When Alaska became a State, 98 percent of its land was owned by the Federal Government. The Statehood Act allowed Alaska to select about a third of that land, 103 million acres, for State ownership. The Act did not, however, address the rights of Alaska Natives, so in 1971 Congress passed the Alaska Native Claims Settlement Act, ANCSA, allowing Alaska Natives to select 40 million acres within the State. ANCSA also directed the Secretary of the Interior to select up to 80 million acres of unreserved Federal land in Alaska for addition to the national park system, subject to congressional approval. When Congress failed to approve the Secretary's selections, however, President Carter unilaterally designated 56 million acres of Federal land in Alaska as national monuments. President Carter's actions were unpopular among many Alaskans who were concerned that the new monuments would be subject to restrictive Federal regulations. Protesters demonstrated in Fairbanks, and more than 2,500 Alaskans participated in what was known as the Great Denali-McKinley Trespass. The goal of the trespass was to break over 25 Park Service rules in a two-day period, including by camping, hunting, snowmobiling, setting campfires, shooting guns, and unleashing dogs. Congress once again stepped in to settle the controversy, passing the Alaska National Interest Lands Conservation Act, or ANILCA. That law addresses

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:24.740 | -Charlie | Charley |
| 0:00:26.780 | The | (nothing) |
| 0:00:28.260 | -Charlie | Charley |
| 0:01:19.180 | -Charlie | Charley |
| 0:01:31.420 | percent | (nothing) |
| 0:01:38.180 | (nothing) | a |
| 0:02:09.920 | Secretary's | secretary |
| 0:03:49.180 | title, | titled |
| 0:03:58.860 | (nothing) | and |
| 0:04:53.740 | end quote. | (nothing) |
