# sturgeon-hovercraft-2: Supreme Court No. 17-949

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2018/17-949
- Audio: https://www.supremecourt.gov/media/audio/mp3files/17-949.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2018/17-949_758b.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 64 min on 4 CPU cores
- Audio length: 1:00:48.288 (3648.288 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.2 MB
- Official words: 10271 (plus 6 `(Laughter.)` markers), in 260 speaker turns
- ASR words: 9867
- Official words matched to an ASR word: 9610 of 10271 (**93.56%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.56% (threshold 85%).

453 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 5 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 10 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 17-949 2018 sturgeon-hovercraft-2 --model medium.en --opinion --mentions "hovercraft,moose,Sturgeon,river,Nation River,Alaska,ANILCA,park,ranger,navigable,waters,regulation,statute,drafted,section,public lands,Yukon" --long-questions 10

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE BREYER, 0:31:10.340 to 0:33:40.740 (150.4 s, 352 words)

> So your point here, which we'll hear something about probably on rebuttal, is that there's some other statutes here that, whatever it says in -- in 103(c), give direct authority to the Secretary to do this. I see where you're driving at. But I'd like to go back to 103(c) because the question that Justice Kagan asked was a question that was in my mind too, and it is to do with the word "solely." And either they -- he can answer this on rebuttal too if he wants. Imagine something like Yellowstone, not perfectly, but it's a square and it is mostly -- it's federal, but there are a few houses belonging to Smith and Jones that are private, and the -- pass a statute, a reg, and the reg says: Oh, no bonfires within the boundaries of the park, which means Smith can't do it either. Now is that a reg that is a reg solely relating to lands to which the U.S. has title? Well, I can -- the argument that it couldn't possibly be for the purposes of this statute is you wouldn't need -- you wouldn't need sentence 2 at all if that were the case. You just wouldn't need it, period, because it wouldn't apply to the river regardless because it says it wouldn't. Okay? So sentence 2 must have some purpose. And, therefore, when the national park system has a reg which says "applies within the boundaries of a national park," that is a rule that relates only to public lands. And if it doesn't -- see, without that, this is meaningless, and so it must mean that, and so it must be that that kind of thing is what you can't do to enclaves within public lands in this area. And the river is such an enclave because it is not a piece of property to which the United States has title. Now that, I think, is their argument. I've had a hard time grasping the arguments in this case, but I think that that is their argument. If I am right, what's the answer to it, if there is one?

### 2. JUSTICE BREYER, 0:45:31.640 to 0:47:01.500 (89.9 s, 236 words)

> Can I go back to this question because this is obviously the question that's bothering some of us, okay? And it seems to me you sort of answered it both ways. You're not -- I -- I started out thinking that if a reg applies to Mr. Smith's inholding in Yosemite because it applies to all of Yosemite, that that is solely public lands. Why? Because if the only things that count as a reg for public lands -- we've said this three times -- are -- are those regs that say they don't apply to Smith's inholding, you don't need this statute, okay? That's the basic thing. Now some of what you said seems to agree with that and some of it does not. But what I took your basic arguments to be, one, that water, unlike Mr. Smith's cabin, is close enough to public lands that it's out of this thing. Two, even if it isn't, there are other statutes that give specific authority to the government to regulate the water. And one of them might be general. One of them might be the ones you just started off your argument with. One of them might be -- I don't know. There are two or three on that. Now I think I've got this very helpful argument right at least to what you're arguing. And is there something else, or do I have it so wrong it's hardly worth answering?

### 3. JUSTICE SOTOMAYOR, 0:00:50.360 to 0:02:06.080 (75.7 s, 151 words)

> I'm sorry, but ANILCA in many places puts statutory duties on the government, on the Park Service. So, for example, the statute expands the Glacier Bay National Monument. It says that the monument shall be managed for the following purposes among others, to protect a segment of the Alsek River fish and wildlife habitats and migration routes and a portion of the Fairweather Range. Or take another example. ANILCA creates the Kobuk Valley National Park, which it says shall be managed for the following purposes: among others, to keep it in an undeveloped state. So the agency has a statutory duty -- duty to manage these parks for the purpose of maintaining the Kobuk River, the Alsek River, and other rivers. If the Park Service can't do what you say, any regulation on these rivers, how can the Secretary fulfill the statutory duties and -- under ANILCA, unless it's under its organic powers?

### 4. JUSTICE GORSUCH, 0:27:00.120 to 0:28:15.520 (75.4 s, 184 words)

> -- I'd just like to understand your argument on the terms of -- of the '76 Act itself a little bit better. It says the Secretary may prescribe regulations concerning boating and other activities on or relating to water within system units. And I'm -- I'm paraphrasing, but I think that's about it. And I'd understand your argument better, I think, if the -- if the statute read that the Secretary could regulate water in or relating to system units, so not just water within system units but also water outside system units, like the water here that might have some downstream effect, say. But that's not what the statute says. It says that the -- it may prescribe regulations concerning boating or other activities that themselves relate to water in system units. So I would think that the government would have to prove some nexus between boating or the other activities and the water within the government's system units. And I just didn't see that story told here, how Mr. Sturgeon's hovercraft would in some way impact water within the system units, meaning public -- public lands, public waters.

### 5. JUSTICE SOTOMAYOR, 0:56:46.310 to 0:57:59.250 (72.9 s, 155 words)

> -- you don't have title to the water. I mean, you suggest that there are some cases who say effectively it is, but effectively is different than is. Navigable waters are navigable waters. We rarely think of them as someone having title to them, but we do think of them as having interest in them. And if there's two interests, the federal government's and the state's, don't they win? Because, if they have an interest, they have a public interest that, by statute, is being directed. I mean, there are 26 rivers designated as wild and scenic rivers here. There are all sorts of -- I've mentioned this repeatedly -- all sorts of statutory obligations that the government's being given under this particular Act to preserve these waterways in a particular way. So I -- I -- I don't understand. If you don't have title, does this -- at least with respect to navigable waters, do you have any claim whatsoever?

### 6. JUSTICE KAGAN, 0:10:32.100 to 0:11:15.120 (43.0 s, 100 words)

> Okay, could I ask you to go back to the applicable -- regulations applicable solely to public lands? And you suggested that that language is what distinguishes Park Service regulations from, let's say, EPA regulations. But, when I read that language, "regulations applicable solely to public lands," it seems to be making a distinction between regulations that apply solely, exclusively to public lands and those that apply more broadly to both public and private lands. That seems to be the distinction this makes on its face. So I guess I don't quite get how -- how you make it into something different.

### 7. JUSTICE SOTOMAYOR, 0:18:06.580 to 0:18:47.220 (40.6 s, 89 words)

> I don't think you've answered my question. How is the government, the federal government, supposed to fulfill its statutory duties? There are many rivers here that they're given explicit obligations. Your basically saying 103(c) trumps that doesn't make much sense to me. If a statute tells the government do this and at the same time reserves some rights to the state, doesn't the federal government's obligation to do this, the explicit obligation to deal with certain rivers in a particular way, trump any other exemption that you might have?

### 8. CHIEF JUSTICE ROBERTS, 0:44:36.040 to 0:45:15.900 (39.9 s, 132 words)

> -- adequate account of -- of the third sentence. I mean, you're trying to minimize it by saying it's maps. The third sentence has to illuminate the first two. And what it says is, if a state, a native corporation, or an owner wants to convey lands to the Secretary, it can. In other words, if you -- the -- the -- the Secretary, feels that you need to have authority over areas that you don't, it tells you in -- in the third sentence how to do it: get the state or the native corporation to convey it to you. That would be an odd sentence to include if this were not -- if this were a -- a -- a protection you could write around just by saying, oh, and, by the way, this applies to the -- the inholders.

### 9. JUSTICE KAGAN, 0:43:26.060 to 0:43:59.100 (33.0 s, 105 words)

> But just on the face of things, Mr. Kneedler, if -- if the Park Service issues a regulation and the regulation says this applies only to public lands within a park, right, and you're not a public land within a park, you're a private land within a park, what kind of assurance do you need? It's like you know that you're not a public land, so it doesn't matter that you're in the park. You don't need a special statute to tell you that, do you? You only need a special statute if the special statute exempts you from something that would otherwise apply to you.

### 10. JUSTICE SOTOMAYOR, 0:38:44.380 to 0:39:14.960 (30.6 s, 53 words)

> Can I summarize what I think you said? Are you saying that 103(c) basically, because of the navigational servitude, the other regulations you've pointed to, doesn't permit the government to regulate activities on the territorial lands or -- or on the submerged lands, but it does give it basically plenary authority over navigable waters?

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-51.2 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:07:36.100 | 456.100 | under speech | 0.00 | 0.00 | - | - | Engineers is fine with you, the EPA is fine. But not the Park Service? It's not that we don't like the Park Service, as it -- it's that layer of regulation -- |
| 2 | 0:15:18.920 | 918.920 | under speech | 0.28 | 0.10 | 13.9 | 15.8 | want you to reserve your time. I'd rather you reserved your time. I'll ask them. Oh, okay. Thank you. If there are no other questions, I will reserve my time. |
| 3 | 0:15:22.960 | 922.960 | medium | 8.50 | 1.70 | 11.5 | 22.1 | you reserved your time. I'll ask them. Oh, okay. Thank you. If there are no other questions, I will reserve my time. Thank you. Good -- good choice. Thank you, counsel. |
| 4 | 0:38:14.800 | 2294.800 | small | 0.58 | 0.10 | 24.2 | 33.1 | hovercraft traffic. Well, the -- And while -- while you may think a hovercraft is unsightly, I mean, if you're trying to get from point A to point B, it's pretty beautiful. |
| 5 | 0:47:02.980 | 2822.980 | under speech | 0.00 | 0.00 | - | - | helpful argument right at least to what you're arguing. And is there something else, or do I have it so wrong it's hardly worth answering? No, I -- I think it's -- |
| 6 | 0:47:35.400 | 2855.400 | under speech | 0.00 | 0.00 | - | - | I think -- But that is not really involved here. Here, we're only talking about -- Counsel -- Waters which were not -- -- Justice Alito has been trying to ask a question. I'm sorry. |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| hovercraft | 7 | 7 |
| moose | 0 | 0 |
| Sturgeon | 4 | 4 |
| river | 48 | 56 |
| Nation River | 0 | 0 |
| Alaska | 28 | 31 |
| ANILCA | 38 | 41 |
| park | 112 | 134 |
| ranger | 0 | 0 |
| navigable | 39 | 42 |
| waters | 67 | 75 |
| regulation | 55 | 65 |
| statute | 52 | 56 |
| drafted | 0 | 0 |
| section | 15 | 15 |
| public lands | 41 | 51 |
| Yukon | 7 | 7 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:04.300 | 4.300 | CHIEF JUSTICE ROBERTS | Sturgeon | We'll hear argument first this morning in Case 17-949, Sturgeon versus Frost. |
| 0:00:11.500 | 11.500 | MR. FINDLEY | Sturgeon | Mr. Chief Justice, and may it please the Court: Mr. Sturgeon is asking that this Court restore the balance that -- that Congress struck when enacting ANILCA. |
| 0:00:16.480 | 16.480 | MR. FINDLEY | ANILCA | Mr. Chief Justice, and may it please the Court: Mr. Sturgeon is asking that this Court restore the balance that -- that Congress struck when enacting ANILCA. |
| 0:00:17.600 | 17.600 | MR. FINDLEY | ANILCA | ANILCA is unique and represents a series of bargains and compromises. |
| 0:00:27.840 | 27.840 | MR. FINDLEY | public lands | A centerpiece of this balancing was ensuring that the over 18 million acres of non-public lands and waters about to be surrounded by the new ANILCA parks and preserves would not be subject to a new array of federal regulation. |
| 0:00:29.100 | 29.100 | MR. FINDLEY | waters | A centerpiece of this balancing was ensuring that the over 18 million acres of non-public lands and waters about to be surrounded by the new ANILCA parks and preserves would not be subject to a new array of federal regulation. |
| 0:00:31.440 | 31.440 | MR. FINDLEY | ANILCA | A centerpiece of this balancing was ensuring that the over 18 million acres of non-public lands and waters about to be surrounded by the new ANILCA parks and preserves would not be subject to a new array of federal regulation. |
| 0:00:31.740 | 31.740 | MR. FINDLEY | park | A centerpiece of this balancing was ensuring that the over 18 million acres of non-public lands and waters about to be surrounded by the new ANILCA parks and preserves would not be subject to a new array of federal regulation. |
| 0:00:35.760 | 35.760 | MR. FINDLEY | regulation | A centerpiece of this balancing was ensuring that the over 18 million acres of non-public lands and waters about to be surrounded by the new ANILCA parks and preserves would not be subject to a new array of federal regulation. |
| 0:00:37.540 | 37.540 | MR. FINDLEY | section | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:39.200 | 39.200 | MR. FINDLEY | statute | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:41.680 | 41.680 | MR. FINDLEY | public lands | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:42.720 | 42.720 | MR. FINDLEY | waters | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:45.020 | 45.020 | MR. FINDLEY | ANILCA | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:45.520 | 45.520 | MR. FINDLEY | park | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:49.740 | 49.740 | MR. FINDLEY | regulation | Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation. |
| 0:00:51.660 | 51.660 | JUSTICE SOTOMAYOR | ANILCA | I'm sorry, but ANILCA in many places puts statutory duties on the government, on the Park Service. |
| 0:00:58.980 | 58.980 | JUSTICE SOTOMAYOR | park | I'm sorry, but ANILCA in many places puts statutory duties on the government, on the Park Service. |
| 0:01:02.380 | 62.380 | JUSTICE SOTOMAYOR | statute | So, for example, the statute expands the Glacier Bay National Monument. |
| 0:01:14.900 | 74.900 | JUSTICE SOTOMAYOR | river | It says that the monument shall be managed for the following purposes among others, to protect a segment of the Alsek River fish and wildlife habitats and migration routes and a portion of the Fairweather Range. |
| 0:01:24.680 | 84.680 | JUSTICE SOTOMAYOR | ANILCA | ANILCA creates the Kobuk Valley National Park, which it says shall be managed for the following purposes: among others, to keep it in an undeveloped state. |
| 0:01:27.620 | 87.620 | JUSTICE SOTOMAYOR | park | ANILCA creates the Kobuk Valley National Park, which it says shall be managed for the following purposes: among others, to keep it in an undeveloped state. |
| 0:01:42.360 | 102.360 | JUSTICE SOTOMAYOR | park | So the agency has a statutory duty -- duty to manage these parks for the purpose of maintaining the Kobuk River, the Alsek River, and other rivers. |
| 0:01:44.800 | 104.800 | JUSTICE SOTOMAYOR | river | So the agency has a statutory duty -- duty to manage these parks for the purpose of maintaining the Kobuk River, the Alsek River, and other rivers. |
| 0:01:50.440 | 110.440 | JUSTICE SOTOMAYOR | park | If the Park Service can't do what you say, any regulation on these rivers, how can the Secretary fulfill the statutory duties and -- under ANILCA, unless it's under its organic powers? |
| 0:01:55.520 | 115.520 | JUSTICE SOTOMAYOR | regulation | If the Park Service can't do what you say, any regulation on these rivers, how can the Secretary fulfill the statutory duties and -- under ANILCA, unless it's under its organic powers? |
| 0:01:57.000 | 117.000 | JUSTICE SOTOMAYOR | river | If the Park Service can't do what you say, any regulation on these rivers, how can the Secretary fulfill the statutory duties and -- under ANILCA, unless it's under its organic powers? |
| 0:02:02.780 | 122.780 | JUSTICE SOTOMAYOR | ANILCA | If the Park Service can't do what you say, any regulation on these rivers, how can the Secretary fulfill the statutory duties and -- under ANILCA, unless it's under its organic powers? |
| 0:02:07.120 | 127.120 | MR. FINDLEY | ANILCA | ANILCA, as this Court recognized in the first decision, specifically invoked the Organic Act and said these parks shall be managed in accord with the Organic Act and in accord with the provisions of ANILCA. |
| 0:02:13.340 | 133.340 | MR. FINDLEY | park | ANILCA, as this Court recognized in the first decision, specifically invoked the Organic Act and said these parks shall be managed in accord with the Organic Act and in accord with the provisions of ANILCA. |
| 0:02:19.760 | 139.760 | MR. FINDLEY | ANILCA | And this Court recognized that ANILCA carries many provisions specifically modifying the Park Service's Organic Act authority, Section 103(c) being one of them. |
| 0:02:23.380 | 143.380 | MR. FINDLEY | park | And this Court recognized that ANILCA carries many provisions specifically modifying the Park Service's Organic Act authority, Section 103(c) being one of them. |
| 0:02:25.240 | 145.240 | MR. FINDLEY | section | And this Court recognized that ANILCA carries many provisions specifically modifying the Park Service's Organic Act authority, Section 103(c) being one of them. |
| 0:02:28.740 | 148.740 | MR. FINDLEY | park | To your question, how can the Park Service fulfill its duties: In understanding ANILCA it's understanding the debate about ANILCA, it was very important what land went into conservation system units, but it was equally important what land did not get included within conservation system units. |
| 0:02:31.340 | 151.340 | MR. FINDLEY | ANILCA | To your question, how can the Park Service fulfill its duties: In understanding ANILCA it's understanding the debate about ANILCA, it was very important what land went into conservation system units, but it was equally important what land did not get included within conservation system units. |
| 0:02:43.020 | 163.020 | MR. FINDLEY | ANILCA | ANILCA was not just a park enabling statute. |
| 0:02:44.120 | 164.120 | MR. FINDLEY | park | ANILCA was not just a park enabling statute. |
| 0:02:44.580 | 164.580 | MR. FINDLEY | statute | ANILCA was not just a park enabling statute. |
| 0:02:48.440 | 168.440 | MR. FINDLEY | ANILCA | As this Court recognized in Amoco when it was -- first addressed ANILCA, it was resolving multiple land use disputes within Alaska. |
| 0:02:51.760 | 171.760 | MR. FINDLEY | Alaska | As this Court recognized in Amoco when it was -- first addressed ANILCA, it was resolving multiple land use disputes within Alaska. |
| 0:02:57.400 | 177.400 | JUSTICE SOTOMAYOR | navigable | Under your theory, the state manages all navigable waters between federal lands or between state lands. |
| 0:02:58.080 | 178.080 | JUSTICE SOTOMAYOR | waters | Under your theory, the state manages all navigable waters between federal lands or between state lands. |
| 0:03:04.140 | 184.140 | JUSTICE SOTOMAYOR | waters | And I mean not waters but lands -- |
| 0:03:10.700 | 190.700 | JUSTICE SOTOMAYOR | park | How does the Park Service engage in its statutory obligations if it can't do what you say? |
| 0:03:17.920 | 197.920 | MR. FINDLEY | park | The Park Service, for all those purposes, it can regulate submerged lands and waters where title did not pass to the state at statehood. |
| 0:03:21.480 | 201.480 | MR. FINDLEY | waters | The Park Service, for all those purposes, it can regulate submerged lands and waters where title did not pass to the state at statehood. |
| 0:03:25.460 | 205.460 | MR. FINDLEY | waters | It can manage public waters. |
| 0:03:27.000 | 207.000 | MR. FINDLEY | navigable | It can manage any non-navigable waters. |
| 0:03:27.660 | 207.660 | MR. FINDLEY | waters | It can manage any non-navigable waters. |
| 0:03:28.780 | 208.780 | JUSTICE SOTOMAYOR | waters | There's no public waters. |
| 0:03:32.440 | 212.440 | JUSTICE SOTOMAYOR | waters | Under your theory, all the waters belong to the state. |
| 0:03:35.600 | 215.600 | MR. FINDLEY | navigable | Only navigable waters where title to the submerged lands passed at -- |
| 0:03:36.160 | 216.160 | MR. FINDLEY | waters | Only navigable waters where title to the submerged lands passed at -- |
| 0:03:46.580 | 226.580 | JUSTICE SOTOMAYOR | river | -- what you're saying is that a good portion of the Act with all of the preservations of the rivers that the Act imposes upon the Park Service, it cannot do any of that work? |
| 0:03:50.200 | 230.200 | JUSTICE SOTOMAYOR | park | -- what you're saying is that a good portion of the Act with all of the preservations of the rivers that the Act imposes upon the Park Service, it cannot do any of that work? |
| 0:03:56.900 | 236.900 | MR. FINDLEY | navigable | It cannot do that work on any of the specific navigable waters, but it can protect the watershed. |
| 0:03:57.420 | 237.420 | MR. FINDLEY | waters | It cannot do that work on any of the specific navigable waters, but it can protect the watershed. |
| 0:03:59.720 | 239.720 | MR. FINDLEY | Yukon | The Yukon-Charley is a very good example of that. |
| 0:04:02.100 | 242.100 | MR. FINDLEY | Yukon | The Yukon-Charley -- again, think of the balancing of ANILCA that this Court recognized -- some of its conservation purposes is equally important to balance the economic needs of the State of Alaska. |
| 0:04:04.360 | 244.360 | MR. FINDLEY | ANILCA | The Yukon-Charley -- again, think of the balancing of ANILCA that this Court recognized -- some of its conservation purposes is equally important to balance the economic needs of the State of Alaska. |
| 0:04:11.680 | 251.680 | MR. FINDLEY | Alaska | The Yukon-Charley -- again, think of the balancing of ANILCA that this Court recognized -- some of its conservation purposes is equally important to balance the economic needs of the State of Alaska. |
| 0:04:12.820 | 252.820 | MR. FINDLEY | Yukon | The Yukon-Charley met goal number one by putting 1.7 million acres of land into the preserve to protect lakes, streams, and the watershed. |
| 0:04:22.560 | 262.560 | MR. FINDLEY | river | And you protect the river by regulating those 1.7 million acres of public lands that's regulated under the watershed -- |
| 0:04:25.820 | 265.820 | MR. FINDLEY | public lands | And you protect the river by regulating those 1.7 million acres of public lands that's regulated under the watershed -- |
| 0:04:29.220 | 269.220 | MR. FINDLEY | river | -- that protects the river. |
| 0:04:30.680 | 270.680 | JUSTICE SOTOMAYOR | park | -- difference that a park is designated as a wild and scenic river? |
| 0:04:33.020 | 273.020 | JUSTICE SOTOMAYOR | river | -- difference that a park is designated as a wild and scenic river? |
| 0:04:36.520 | 276.520 | MR. FINDLEY | river | The Wild and Scenic Rivers Act was even specifically amended by ANILCA to make sure it wasn't covering state land that goes into the site of the river, and the Wild and Scenic Rivers Act itself recognizes state ownership of submerged lands. |
| 0:04:38.880 | 278.880 | MR. FINDLEY | ANILCA | The Wild and Scenic Rivers Act was even specifically amended by ANILCA to make sure it wasn't covering state land that goes into the site of the river, and the Wild and Scenic Rivers Act itself recognizes state ownership of submerged lands. |
| 0:04:49.460 | 289.460 | MR. FINDLEY | river | In the Wild and Scenic Rivers Act, there's nothing about those designations that undoes the central compromise that was through 103(c). |
| 0:04:59.700 | 299.700 | JUSTICE KAGAN | public lands | And you don't think it makes any difference if there are public lands on both sides of a river? |
| 0:05:01.820 | 301.820 | JUSTICE KAGAN | river | And you don't think it makes any difference if there are public lands on both sides of a river? |
| 0:05:04.640 | 304.640 | JUSTICE KAGAN | river | In other words, both banks of a river are public lands, but still the federal government cannot regulate the river running through those lands? |
| 0:05:05.560 | 305.560 | JUSTICE KAGAN | public lands | In other words, both banks of a river are public lands, but still the federal government cannot regulate the river running through those lands? |
| 0:05:14.000 | 314.000 | MR. FINDLEY | park | The Park Service may not. |
| 0:05:17.000 | 317.000 | MR. FINDLEY | park | That was a power that was not delegated to the Park Service. |
| 0:05:19.100 | 319.100 | MR. FINDLEY | park | An example that even the Park Service brings up in its brief is the Yukon-Kuskokwim Wildlife Refuge. |
| 0:05:20.920 | 320.920 | MR. FINDLEY | Yukon | An example that even the Park Service brings up in its brief is the Yukon-Kuskokwim Wildlife Refuge. |
| 0:05:25.820 | 325.820 | MR. FINDLEY | park | So there's a very specific provision directing that the Park Service may not impede access to these rivers. |
| 0:05:28.460 | 328.460 | MR. FINDLEY | river | So there's a very specific provision directing that the Park Service may not impede access to these rivers. |
| 0:05:30.320 | 330.320 | MR. FINDLEY | Alaska | Particularly in that area of Alaska where there are no roads, the Yukon and the Kuskokwim River are the arteries of commerce that's helpful to get to and from villages. |
| 0:05:32.620 | 332.620 | MR. FINDLEY | Yukon | Particularly in that area of Alaska where there are no roads, the Yukon and the Kuskokwim River are the arteries of commerce that's helpful to get to and from villages. |
| 0:05:33.560 | 333.560 | MR. FINDLEY | river | Particularly in that area of Alaska where there are no roads, the Yukon and the Kuskokwim River are the arteries of commerce that's helpful to get to and from villages. |
| 0:05:40.980 | 340.980 | MR. FINDLEY | ANILCA | And the specific mandate in ANILCA is we are about to surround these highways with these federal lands, we're going to put them in a conservation system unit, that's great, but please do not block access to the highway. |
| 0:05:52.000 | 352.000 | MR. FINDLEY | river | And that's the point of exempting the rivers. |
| 0:05:57.380 | 357.380 | CHIEF JUSTICE ROBERTS | waters | So an agency like EPA is -- is fully empowered to regulate the waters? |
| 0:06:06.860 | 366.860 | MR. FINDLEY | park | It's just simply that extra layer of Park Service regulation that was not supposed to apply once these lands and waters were surrounded by. |
| 0:06:07.280 | 367.280 | MR. FINDLEY | regulation | It's just simply that extra layer of Park Service regulation that was not supposed to apply once these lands and waters were surrounded by. |
| 0:06:11.060 | 371.060 | MR. FINDLEY | waters | It's just simply that extra layer of Park Service regulation that was not supposed to apply once these lands and waters were surrounded by. |
| 0:06:12.940 | 372.940 | MR. FINDLEY | ANILCA | -- the ANILCA parks. |
| 0:06:12.940 | 372.940 | MR. FINDLEY | park | -- the ANILCA parks. |
| 0:06:29.300 | 389.300 | MR. FINDLEY | section | When it comes to interpreting the Organic Act, against Section 103(c), those aren't necessarily implicated, although, as this Court recognized in the first decision, the state's power over its navigable waters does raise significant issues of state sovereignty. |
| 0:06:36.580 | 396.580 | MR. FINDLEY | navigable | When it comes to interpreting the Organic Act, against Section 103(c), those aren't necessarily implicated, although, as this Court recognized in the first decision, the state's power over its navigable waters does raise significant issues of state sovereignty. |
| 0:06:36.940 | 396.940 | MR. FINDLEY | waters | When it comes to interpreting the Organic Act, against Section 103(c), those aren't necessarily implicated, although, as this Court recognized in the first decision, the state's power over its navigable waters does raise significant issues of state sovereignty. |
| 0:06:42.200 | 402.200 | MR. FINDLEY | navigable | And any time this Court addresses a case of navigable waters, the refrain rings throughout these cases that the state's ownership of the submerged lands and control and ownership of the resources within it is a hallmark of state -- state sovereignty and a hallmark of federalism. |
| 0:06:42.600 | 402.600 | MR. FINDLEY | waters | And any time this Court addresses a case of navigable waters, the refrain rings throughout these cases that the state's ownership of the submerged lands and control and ownership of the resources within it is a hallmark of state -- state sovereignty and a hallmark of federalism. |
| 0:06:56.920 | 416.920 | MR. FINDLEY | park | Where the clear statement rule comes into play is the Park Service's fallback argument here, which is, well, if you look at reserve water rights, this can turn these into public lands and actually make these part of the park. |
| 0:07:02.840 | 422.840 | MR. FINDLEY | public lands | Where the clear statement rule comes into play is the Park Service's fallback argument here, which is, well, if you look at reserve water rights, this can turn these into public lands and actually make these part of the park. |
| 0:07:06.440 | 426.440 | MR. FINDLEY | ANILCA | And there's nothing in ANILCA that's a clear statement saying we are going to take the state's submerged lands, make them public lands, and actually include them in the parks. |
| 0:07:10.760 | 430.760 | MR. FINDLEY | public lands | And there's nothing in ANILCA that's a clear statement saying we are going to take the state's submerged lands, make them public lands, and actually include them in the parks. |
| 0:07:12.680 | 432.680 | MR. FINDLEY | park | And there's nothing in ANILCA that's a clear statement saying we are going to take the state's submerged lands, make them public lands, and actually include them in the parks. |
| 0:07:16.320 | 436.320 | MR. FINDLEY | statute | When we were here last time, we talked about when that happens, the enabling statute is very clear. |
| 0:07:17.820 | 437.820 | MR. FINDLEY | statute | And the statute that added Lake Ozette to the Olympic National Park actually specifically said we are adding the submerged lands to the park, so -- |
| 0:07:20.460 | 440.460 | MR. FINDLEY | park | And the statute that added Lake Ozette to the Olympic National Park actually specifically said we are adding the submerged lands to the park, so -- |
| 0:07:25.900 | 445.900 | CHIEF JUSTICE ROBERTS | park | So you just -- it -- it -- you just don't like the Park Service. |
| 0:07:32.360 | 452.360 | CHIEF JUSTICE ROBERTS | park | But not the Park Service? |
| 0:07:33.820 | 453.820 | MR. FINDLEY | park | It's not that we don't like the Park Service, as it -- it's that layer of regulation -- |
| 0:07:35.600 | 455.600 | MR. FINDLEY | regulation | It's not that we don't like the Park Service, as it -- it's that layer of regulation -- |
| 0:07:44.400 | 464.400 | JUSTICE ALITO | section | Which sentence of Section 3103(c) do you think wins this case for you? |
| 0:07:57.760 | 477.760 | MR. FINDLEY | statute | The second -- second sentence does the most work, but the second sentence needs to be read in conjunction with all three sentences and in conjunction with the context of the statute. |
| 0:08:03.880 | 483.880 | JUSTICE ALITO | statute | I've burned up an awful lot of gray cells trying to put together the pieces of this statute. |
| 0:08:19.540 | 499.540 | MR. FINDLEY | waters | So you -- you -- the first sentence of 103(c) has just told you that any non-public land, whether it's state land, submerged -- submerged lands, waters, native corporation, or private land, it is not going to be part of the park. |
| 0:08:23.000 | 503.000 | MR. FINDLEY | park | So you -- you -- the first sentence of 103(c) has just told you that any non-public land, whether it's state land, submerged -- submerged lands, waters, native corporation, or private land, it is not going to be part of the park. |
| 0:08:24.520 | 504.520 | JUSTICE ALITO | park | It's not a portion of the park? |
| 0:08:25.560 | 505.560 | MR. FINDLEY | park | It's not a portion of the park. |
| 0:08:54.540 | 534.540 | MR. FINDLEY | public lands | Again, shorthand, non-public lands. |
| 0:08:58.020 | 538.020 | MR. FINDLEY | regulation | They shall not be subject to regulations applicable solely to public lands within the units. |
| 0:08:59.560 | 539.560 | MR. FINDLEY | public lands | They shall not be subject to regulations applicable solely to public lands within the units. |
| 0:09:09.020 | 549.020 | MR. FINDLEY | park | And that's the function of the word "solely," is to distinguish between park management regulations and the regulations Mr. Chief Justice was talking about, Coast Guard, EPA and -- |
| 0:09:09.720 | 549.720 | MR. FINDLEY | regulation | And that's the function of the word "solely," is to distinguish between park management regulations and the regulations Mr. Chief Justice was talking about, Coast Guard, EPA and -- |
| 0:09:22.320 | 562.320 | JUSTICE ALITO | ANILCA | I understand that lands is defined by ANILCA to include inter -- water and waters and interests therein, but the second sentence after referring to lands then refers to a conveyance, which I take it means the transfer of title. |
| 0:09:24.520 | 564.520 | JUSTICE ALITO | waters | I understand that lands is defined by ANILCA to include inter -- water and waters and interests therein, but the second sentence after referring to lands then refers to a conveyance, which I take it means the transfer of title. |
| 0:09:41.340 | 581.340 | JUSTICE ALITO | navigable | And nobody really has title to navigable waters. |
| 0:09:41.880 | 581.880 | JUSTICE ALITO | waters | And nobody really has title to navigable waters. |
| 0:09:49.580 | 589.580 | MR. FINDLEY | Alaska | First of all, the submerged lands were conveyed to Alaska. |
| 0:10:09.460 | 609.460 | MR. FINDLEY | waters | In terms of having title to water, this Court has, in U.S. v. California, and PPL Montana, certainly suggested with very strong language that, with -- with the Submerged Lands Act, with title to the submerged lands, and with ownership and control of all the resources within there, that is effectively title to the waters. |
| 0:10:10.600 | 610.600 | JUSTICE ALITO | public lands | No, I mean as to the public lands. |
| 0:10:11.600 | 611.600 | JUSTICE ALITO | public lands | So public lands are defined -- I mean, lands are defined the same way. |
| 0:10:23.600 | 623.600 | JUSTICE ALITO | navigable | Public means, I take it, title in the United States, but the United States does not have title to navigable waters, is that right? |
| 0:10:24.480 | 624.480 | JUSTICE ALITO | waters | Public means, I take it, title in the United States, but the United States does not have title to navigable waters, is that right? |
| 0:10:34.700 | 634.700 | JUSTICE KAGAN | regulation | Okay, could I ask you to go back to the applicable -- regulations applicable solely to public lands? |
| 0:10:36.920 | 636.920 | JUSTICE KAGAN | public lands | Okay, could I ask you to go back to the applicable -- regulations applicable solely to public lands? |
| 0:10:42.400 | 642.400 | JUSTICE KAGAN | park | And you suggested that that language is what distinguishes Park Service regulations from, let's say, EPA regulations. |
| 0:10:43.580 | 643.580 | JUSTICE KAGAN | regulation | And you suggested that that language is what distinguishes Park Service regulations from, let's say, EPA regulations. |
| 0:10:49.120 | 649.120 | JUSTICE KAGAN | regulation | But, when I read that language, "regulations applicable solely to public lands," it seems to be making a distinction between regulations that apply solely, exclusively to public lands and those that apply more broadly to both public and private lands. |
| 0:10:50.640 | 650.640 | JUSTICE KAGAN | public lands | But, when I read that language, "regulations applicable solely to public lands," it seems to be making a distinction between regulations that apply solely, exclusively to public lands and those that apply more broadly to both public and private lands. |
| 0:11:17.340 | 677.340 | MR. FINDLEY | Sturgeon | And Mr. Sturgeon's position, as with the state, is that "solely" distinguishes between the generally applicable regulations that we talked to Mr. Chief Justice about, Coast Guard, EPA, and so on, and park management regulations. |
| 0:11:21.520 | 681.520 | MR. FINDLEY | regulation | And Mr. Sturgeon's position, as with the state, is that "solely" distinguishes between the generally applicable regulations that we talked to Mr. Chief Justice about, Coast Guard, EPA, and so on, and park management regulations. |
| 0:11:26.720 | 686.720 | MR. FINDLEY | park | And Mr. Sturgeon's position, as with the state, is that "solely" distinguishes between the generally applicable regulations that we talked to Mr. Chief Justice about, Coast Guard, EPA, and so on, and park management regulations. |
| 0:11:30.100 | 690.100 | MR. FINDLEY | statute | If you were to take the word "solely" out of the statute, you would have inadvertently exempted these lands from a myriad of other federal regulation that applied before ANILCA and that was certainly intended to apply -- apply after ANILCA. |
| 0:11:34.080 | 694.080 | MR. FINDLEY | regulation | If you were to take the word "solely" out of the statute, you would have inadvertently exempted these lands from a myriad of other federal regulation that applied before ANILCA and that was certainly intended to apply -- apply after ANILCA. |
| 0:11:35.600 | 695.600 | MR. FINDLEY | ANILCA | If you were to take the word "solely" out of the statute, you would have inadvertently exempted these lands from a myriad of other federal regulation that applied before ANILCA and that was certainly intended to apply -- apply after ANILCA. |
| 0:11:40.780 | 700.780 | MR. FINDLEY | park | If you look, I mean, the Park Service in its argument about Section 103(c) and argument -- |
| 0:11:42.420 | 702.420 | MR. FINDLEY | section | If you look, I mean, the Park Service in its argument about Section 103(c) and argument -- |
| 0:11:45.500 | 705.500 | JUSTICE KAGAN | public lands | -- but -- but I guess solely to public lands, is like if you take out the -- if you take out the word "solely," this -- this is saying solely to public lands as compared to what, as compared to -- to public lands and something else, meaning non-public lands. |
| 0:12:03.020 | 723.020 | JUSTICE KAGAN | public lands | And that seems to be the distinction it's drawing: solely to public lands, or to public lands and something else, non-public lands. |
| 0:12:13.200 | 733.200 | MR. FINDLEY | regulation | If a regulation is promulgated only to apply to public lands, it already only applies to public lands. |
| 0:12:15.520 | 735.520 | MR. FINDLEY | public lands | If a regulation is promulgated only to apply to public lands, it already only applies to public lands. |
| 0:12:21.960 | 741.960 | MR. FINDLEY | park | And if it doesn't prohibit the Park Service from issuing the exact regulation at issue here, which is a regulation designed to touch both public and non-public land, that sentence actually doesn't prohibit anything. |
| 0:12:23.400 | 743.400 | MR. FINDLEY | regulation | And if it doesn't prohibit the Park Service from issuing the exact regulation at issue here, which is a regulation designed to touch both public and non-public land, that sentence actually doesn't prohibit anything. |
| 0:12:36.940 | 756.940 | MR. FINDLEY | statute | If you want to understand its prohibitive effect, you look at this came into the statute, it was not a last-minute technical addition. |
| 0:12:42.520 | 762.520 | MR. FINDLEY | ANILCA | It was introduced in the House by Representative Seiberling a year and a half before ANILCA was passed, and he specifically said the fact that these non-public lands were within the units drawn on the map does not change the status of that state native for private land. |
| 0:12:46.480 | 766.480 | MR. FINDLEY | public lands | It was introduced in the House by Representative Seiberling a year and a half before ANILCA was passed, and he specifically said the fact that these non-public lands were within the units drawn on the map does not change the status of that state native for private land. |
| 0:12:56.300 | 776.300 | MR. FINDLEY | park | And that goes back to, if we're about to surround these lands with the parks, they were already subject to a rich matrix of federal regulations before ANILCA. |
| 0:12:59.240 | 779.240 | MR. FINDLEY | regulation | And that goes back to, if we're about to surround these lands with the parks, they were already subject to a rich matrix of federal regulations before ANILCA. |
| 0:13:00.120 | 780.120 | MR. FINDLEY | ANILCA | And that goes back to, if we're about to surround these lands with the parks, they were already subject to a rich matrix of federal regulations before ANILCA. |
| 0:13:03.540 | 783.540 | MR. FINDLEY | regulation | You are not going to subject them to any new array of federal regulation merely because of them being surrounded by the park. |
| 0:13:06.180 | 786.180 | MR. FINDLEY | park | You are not going to subject them to any new array of federal regulation merely because of them being surrounded by the park. |
| 0:13:11.060 | 791.060 | JUSTICE KAGAN | public lands | I -- I understand what -- I think it's a good point, the point you make about, look, if it were public lands versus public and non-public lands, this would not be doing very much. |
| 0:13:57.520 | 837.520 | MR. FINDLEY | statute | If the language weren't read in context with all three sentences, and read in context with the statute, the meaning becomes clearer. |
| 0:14:08.520 | 848.520 | MR. FINDLEY | regulation | And perhaps in hindsight they could have written something about applicable solely to land, you know, solely land management power, but what your -- the "solely" is drawing that distinction of the regulations that only could come into play after the passage of ANILCA. |
| 0:14:12.520 | 852.520 | MR. FINDLEY | ANILCA | And perhaps in hindsight they could have written something about applicable solely to land, you know, solely land management power, but what your -- the "solely" is drawing that distinction of the regulations that only could come into play after the passage of ANILCA. |
| 0:14:16.100 | 856.100 | MR. FINDLEY | section | And it's important to keep in mind that, without provisions like Section 103(c), there is no ANILCA. |
| 0:14:18.480 | 858.480 | MR. FINDLEY | ANILCA | And it's important to keep in mind that, without provisions like Section 103(c), there is no ANILCA. |
| 0:14:19.800 | 859.800 | MR. FINDLEY | ANILCA | There are no ANILCA parks. |
| 0:14:20.260 | 860.260 | MR. FINDLEY | park | There are no ANILCA parks. |
| 0:14:23.320 | 863.320 | MR. FINDLEY | statute | And the -- the large debate, it took two years to pass the statute, there were issues relating to the Native Claims Settlement Act, there were issues related to the Statehood Act, and it was a very large debate, that this Court recognized in Amoco, of what lands will go into a conservation system unit and be subject to much more rigorous conservation regulations and which lands will not go into these things. |
| 0:14:36.720 | 876.720 | MR. FINDLEY | regulation | And the -- the large debate, it took two years to pass the statute, there were issues relating to the Native Claims Settlement Act, there were issues related to the Statehood Act, and it was a very large debate, that this Court recognized in Amoco, of what lands will go into a conservation system unit and be subject to much more rigorous conservation regulations and which lands will not go into these things. |
| 0:14:40.520 | 880.520 | CHIEF JUSTICE ROBERTS | park | Did the -- the Park Service had no -- no regulatory authority over these areas prior to ANILCA or -- |
| 0:14:44.520 | 884.520 | CHIEF JUSTICE ROBERTS | ANILCA | Did the -- the Park Service had no -- no regulatory authority over these areas prior to ANILCA or -- |
| 0:14:54.140 | 894.140 | JUSTICE BREYER | park | Well, I mean, that seems the question to me, that -- that the Park Service has a reg, imagine, that says no bonfires in Yellowstone, within the boundaries of Yellowstone. |
| 0:15:36.020 | 936.020 | MS. BOTSTEIN | ANILCA | Mr. Chief Justice, and may it please the Court: Understanding ANILCA requires understanding remote Alaska. |
| 0:15:38.620 | 938.620 | MS. BOTSTEIN | Alaska | Mr. Chief Justice, and may it please the Court: Understanding ANILCA requires understanding remote Alaska. |
| 0:15:44.700 | 944.700 | MS. BOTSTEIN | river | In most of the state, a vast wilderness that is more than twice the size of Texas, our rivers are our only roads. |
| 0:15:50.560 | 950.560 | MS. BOTSTEIN | park | When Congress surrounded many of these crucial state waterways with federal park areas, it consciously chose not to take away state control over these crucial rivers. |
| 0:15:55.780 | 955.780 | MS. BOTSTEIN | river | When Congress surrounded many of these crucial state waterways with federal park areas, it consciously chose not to take away state control over these crucial rivers. |
| 0:16:06.200 | 966.200 | MS. BOTSTEIN | Alaska | Instead, Congress left them under state control as part of its commitment to providing adequate opportunity for satisfaction of the economic and social needs of the State of Alaska and its people. |
| 0:16:09.280 | 969.280 | MS. BOTSTEIN | park | This Court should reject the Park Service's continuing attempts to commandeer control of Alaska's navigable waters, because that is not what Congress intended. |
| 0:16:12.280 | 972.280 | MS. BOTSTEIN | Alaska | This Court should reject the Park Service's continuing attempts to commandeer control of Alaska's navigable waters, because that is not what Congress intended. |
| 0:16:12.960 | 972.960 | MS. BOTSTEIN | navigable | This Court should reject the Park Service's continuing attempts to commandeer control of Alaska's navigable waters, because that is not what Congress intended. |
| 0:16:13.400 | 973.400 | MS. BOTSTEIN | waters | This Court should reject the Park Service's continuing attempts to commandeer control of Alaska's navigable waters, because that is not what Congress intended. |
| 0:16:26.350 | 986.350 | CHIEF JUSTICE ROBERTS | park | Well, "commandeer" is strong language, but what -- what do you say for the -- the Park Service's argument that, with respect to their reserved water rights and so on, that you would be creating a checkerboard sort of situation where the Park Service has authority with respect to some areas but not others along -- along the river? |
| 0:16:42.180 | 1002.180 | CHIEF JUSTICE ROBERTS | river | Well, "commandeer" is strong language, but what -- what do you say for the -- the Park Service's argument that, with respect to their reserved water rights and so on, that you would be creating a checkerboard sort of situation where the Park Service has authority with respect to some areas but not others along -- along the river? |
| 0:16:44.780 | 1004.780 | MS. BOTSTEIN | park | It is true that both within these park areas there are areas of mixed jurisdiction. |
| 0:16:54.380 | 1014.380 | MS. BOTSTEIN | park | Congress absolutely knew that because it created islands of private and native corporation land that were beyond the reach of park management regulation and, similarly, with the waters. |
| 0:16:55.180 | 1015.180 | MS. BOTSTEIN | regulation | Congress absolutely knew that because it created islands of private and native corporation land that were beyond the reach of park management regulation and, similarly, with the waters. |
| 0:16:57.280 | 1017.280 | MS. BOTSTEIN | waters | Congress absolutely knew that because it created islands of private and native corporation land that were beyond the reach of park management regulation and, similarly, with the waters. |
| 0:17:08.880 | 1028.880 | MS. BOTSTEIN | waters | So, even along large waters, there is a mixed jurisdiction. |
| 0:17:13.680 | 1033.680 | CHIEF JUSTICE ROBERTS | park | But what authority would you say that the Park Service has? |
| 0:17:17.500 | 1037.500 | CHIEF JUSTICE ROBERTS | river | I mean, you're asserting authority with respect to the river. |
| 0:17:18.280 | 1038.280 | CHIEF JUSTICE ROBERTS | park | The Park Service in, apart from inholdings, has authority with respect to the land. |
| 0:17:34.040 | 1054.040 | MS. BOTSTEIN | park | What Congress did was mandated cooperative management as a primary management tool in these parks, so -- and -- and this gets back to the first question from the Court. |
| 0:17:39.400 | 1059.400 | MS. BOTSTEIN | park | Justice Sotomayor asked how can the Park Service fulfill its statutory mission if it doesn't have title to all the lands and the waters. |
| 0:17:43.320 | 1063.320 | MS. BOTSTEIN | waters | Justice Sotomayor asked how can the Park Service fulfill its statutory mission if it doesn't have title to all the lands and the waters. |
| 0:17:55.920 | 1075.920 | MS. BOTSTEIN | Alaska | What Congress said is you work together and create a management plan for each area, identify areas of concern on public and non-public land, and work with landowners and the State of Alaska to try to cooperatively resolve those conflicts because Congress knew it wasn't giving sole and exclusive jurisdiction to the federal government. |
| 0:18:16.000 | 1096.000 | JUSTICE SOTOMAYOR | river | There are many rivers here that they're given explicit obligations. |
| 0:18:28.680 | 1108.680 | JUSTICE SOTOMAYOR | statute | If a statute tells the government do this and at the same time reserves some rights to the state, doesn't the federal government's obligation to do this, the explicit obligation to deal with certain rivers in a particular way, trump any other exemption that you might have? |
| 0:18:42.580 | 1122.580 | JUSTICE SOTOMAYOR | river | If a statute tells the government do this and at the same time reserves some rights to the state, doesn't the federal government's obligation to do this, the explicit obligation to deal with certain rivers in a particular way, trump any other exemption that you might have? |
| 0:18:52.380 | 1132.380 | MS. BOTSTEIN | regulation | No, Your Honor, because the statutory mission is limited to regulation on the public lands, on the federal lands. |
| 0:18:53.420 | 1133.420 | MS. BOTSTEIN | public lands | No, Your Honor, because the statutory mission is limited to regulation on the public lands, on the federal lands. |
| 0:18:58.020 | 1138.020 | MS. BOTSTEIN | public lands | Congress reserved state lands, non-public lands to Alaska, private landowners, or native corporations. |
| 0:18:59.680 | 1139.680 | MS. BOTSTEIN | Alaska | Congress reserved state lands, non-public lands to Alaska, private landowners, or native corporations. |
| 0:19:05.800 | 1145.800 | JUSTICE SOTOMAYOR | river | Many of these rivers are specifically named in the statute. |
| 0:19:08.600 | 1148.600 | JUSTICE SOTOMAYOR | statute | Many of these rivers are specifically named in the statute. |
| 0:19:15.620 | 1155.620 | JUSTICE SOTOMAYOR | river | And your position or your co-counsel's position is that all of these rivers belong to the state? |
| 0:19:18.260 | 1158.260 | MS. BOTSTEIN | navigable | The navigable rivers that were state -- that were not federal owner -- in ownership that passed to the state under the Submerged Lands Act, yes. |
| 0:19:18.820 | 1158.820 | MS. BOTSTEIN | river | The navigable rivers that were state -- that were not federal owner -- in ownership that passed to the state under the Submerged Lands Act, yes. |
| 0:19:28.420 | 1168.420 | JUSTICE SOTOMAYOR | navigable | Well, we have a problem with whether you can own navigable waters, but that's a different issue. |
| 0:19:29.060 | 1169.060 | JUSTICE SOTOMAYOR | waters | Well, we have a problem with whether you can own navigable waters, but that's a different issue. |
| 0:19:36.000 | 1176.000 | MS. BOTSTEIN | river | What Congress did, Your Honor, was said -- you know, when Congress names the rivers as part of a watershed, in part what it's saying is, on the public lands, your statutory mission is to regulate in a way that protects these watersheds, protects access to the watersheds, protects the watersheds, but, at the same time, it is the state that has jurisdiction over the water themselves. |
| 0:19:40.840 | 1180.840 | MS. BOTSTEIN | public lands | What Congress did, Your Honor, was said -- you know, when Congress names the rivers as part of a watershed, in part what it's saying is, on the public lands, your statutory mission is to regulate in a way that protects these watersheds, protects access to the watersheds, protects the watersheds, but, at the same time, it is the state that has jurisdiction over the water themselves. |
| 0:20:03.880 | 1203.880 | MS. BOTSTEIN | park | And if there's any doubt about this, if you look through Title 16, when Congress created different national parks, it used vastly different jurisdictional language. |
| 0:20:13.360 | 1213.360 | MS. BOTSTEIN | park | When Congress created Yellowstone, which Justice Breyer mentioned, this is what it said: The Yellowstone National Park, as its boundaries now are defined or as they may hereinafter be defined or extended, shall be under the sole and exclusive jurisdiction of the United States. |
| 0:20:27.320 | 1227.320 | MS. BOTSTEIN | park | That's a very clear statement that says we drew a circle and everything within it is federal; the Park Service can manage it. |
| 0:20:32.580 | 1232.580 | MS. BOTSTEIN | section | It does violence to Congress's differing intent to interpret Section 103(c) to mean the same as what -- sole and exclusive federal jurisdiction. |
| 0:20:41.360 | 1241.360 | MS. BOTSTEIN | Alaska | And Congress had very good reasons for giving Alaska more sovereign power, reserving more sovereign power to Alaska than it did to Wyoming, because this statute is not a pure conservation statute. |
| 0:20:48.560 | 1248.560 | MS. BOTSTEIN | statute | And Congress had very good reasons for giving Alaska more sovereign power, reserving more sovereign power to Alaska than it did to Wyoming, because this statute is not a pure conservation statute. |
| 0:20:52.580 | 1252.580 | MS. BOTSTEIN | statute | This is also a statute that fulfills the promises made to Alaska at statehood and in the Native Claims Settlement Act about local control and self-sufficiency designed by Alaskans. |
| 0:20:55.180 | 1255.180 | MS. BOTSTEIN | Alaska | This is also a statute that fulfills the promises made to Alaska at statehood and in the Native Claims Settlement Act about local control and self-sufficiency designed by Alaskans. |
| 0:21:23.620 | 1283.620 | JUSTICE SOTOMAYOR | public lands | I don't know how we can give different meaning to public lands in two provisions of the same Act. |
| 0:21:31.860 | 1291.860 | MS. BOTSTEIN | ANILCA | Your Honor, giving effect to Congress's intent in ANILCA does -- may require preserving the rural subsistence priority in Title 8 of the legislation, even if it does require a different statutory definition. |
| 0:21:45.520 | 1305.520 | MS. BOTSTEIN | regulation | Now no party has challenged the current federal subsistence management -- subsistence regulations. |
| 0:21:51.700 | 1311.700 | MS. BOTSTEIN | Alaska | The briefing certainly reflects this is an issue of great concern to the people of Alaska and its rural residents. |
| 0:22:06.900 | 1326.900 | MS. BOTSTEIN | statute | Title 8 could have been its own statute. |
| 0:22:51.920 | 1371.920 | MS. BOTSTEIN | statute | The statute -- |
| 0:22:54.640 | 1374.640 | MS. BOTSTEIN | statute | The statute does contain one definition. |
| 0:23:02.060 | 1382.060 | MS. BOTSTEIN | statute | We've cited to the Court in our brief cases that do suggest, in these long complicated statutes, we do look to Congress's intent in the context of the statute, and that can mean that a term does have different meaning in different sections when that is what Congress -- |
| 0:23:10.580 | 1390.580 | MS. BOTSTEIN | section | We've cited to the Court in our brief cases that do suggest, in these long complicated statutes, we do look to Congress's intent in the context of the statute, and that can mean that a term does have different meaning in different sections when that is what Congress -- |
| 0:23:17.500 | 1397.500 | JUSTICE SOTOMAYOR | river | -- why isn't an -- all of the references to the government's control of rivers in this Act a similar statement of purpose? |
| 0:23:32.240 | 1412.240 | MS. BOTSTEIN | river | Because those need to be read in the context of 103(c), which doesn't say the federal government can come in and regulate these rivers if we don't -- |
| 0:23:39.160 | 1419.160 | JUSTICE SOTOMAYOR | statute | -- subsistence living, but you're arguing that the purpose of the statute is reflected in its structure and words. |
| 0:23:53.580 | 1433.580 | JUSTICE SOTOMAYOR | river | And the structure and words here are giving the government defined statutory duties for any number of rivers within this compound. |
| 0:24:07.160 | 1447.160 | MS. BOTSTEIN | park | Your Honor, the statutory duties that the Park Service is given, is delegated to regulate for non-subsistence purposes, is limited by Section 103(c) and -- |
| 0:24:13.880 | 1453.880 | MS. BOTSTEIN | section | Your Honor, the statutory duties that the Park Service is given, is delegated to regulate for non-subsistence purposes, is limited by Section 103(c) and -- |
| 0:24:25.600 | 1465.600 | MS. BOTSTEIN | regulation | We are not challenging the federal subsistence management regulations -- |
| 0:24:27.460 | 1467.460 | JUSTICE KAVANAUGH | Alaska | Does the State of Alaska agree with those decisions? |
| 0:24:56.040 | 1496.040 | MS. BOTSTEIN | Alaska | And, certainly, Congress had good reasons for treating Alaska differently than other states in the main body of the statute because this comes back to the Congress's special solicitude for Alaska and its uniqueness, which are concerns this Court spoke about in its 2016 opinion. |
| 0:25:01.120 | 1501.120 | MS. BOTSTEIN | statute | And, certainly, Congress had good reasons for treating Alaska differently than other states in the main body of the statute because this comes back to the Congress's special solicitude for Alaska and its uniqueness, which are concerns this Court spoke about in its 2016 opinion. |
| 0:25:25.480 | 1525.480 | MS. BOTSTEIN | river | This is a situation where people are living and working along these rivers and using them for transportation, for commerce, for fishing. |
| 0:25:48.520 | 1548.520 | MS. BOTSTEIN | statute | And Congress wanted to effectuate those purposes in this statute. |
| 0:26:02.920 | 1562.920 | MR. KNEEDLER | statute | Mr. Chief Justice -- excuse me -- and may it please the Court: I'd like to identify at the outset two statutes that have not been discussed which we think are very important to understand the provisions of ANILCA at issue here. |
| 0:26:08.640 | 1568.640 | MR. KNEEDLER | ANILCA | Mr. Chief Justice -- excuse me -- and may it please the Court: I'd like to identify at the outset two statutes that have not been discussed which we think are very important to understand the provisions of ANILCA at issue here. |
| 0:26:11.320 | 1571.320 | MR. KNEEDLER | statute | The first is a general statute enacted in 1976 and added to the Park Service's general authorities, which is reproduced in our -- in our brief at page 8a, and it says the Secretary, under such terms and conditions, et cetera, will have the authority to issue regulations concerning boating and other activities on or relating to water located within system units. |
| 0:26:14.500 | 1574.500 | MR. KNEEDLER | park | The first is a general statute enacted in 1976 and added to the Park Service's general authorities, which is reproduced in our -- in our brief at page 8a, and it says the Secretary, under such terms and conditions, et cetera, will have the authority to issue regulations concerning boating and other activities on or relating to water located within system units. |
| 0:26:29.720 | 1589.720 | MR. KNEEDLER | regulation | The first is a general statute enacted in 1976 and added to the Park Service's general authorities, which is reproduced in our -- in our brief at page 8a, and it says the Secretary, under such terms and conditions, et cetera, will have the authority to issue regulations concerning boating and other activities on or relating to water located within system units. |
| 0:26:42.120 | 1602.120 | MR. KNEEDLER | park | That is a general authority, contrary to Petitioner's argument, that specifically delegates to the Park Service, along with the Coast Guard, power to regulate navigable waters in the national park system. |
| 0:26:45.720 | 1605.720 | MR. KNEEDLER | navigable | That is a general authority, contrary to Petitioner's argument, that specifically delegates to the Park Service, along with the Coast Guard, power to regulate navigable waters in the national park system. |
| 0:26:46.340 | 1606.340 | MR. KNEEDLER | waters | That is a general authority, contrary to Petitioner's argument, that specifically delegates to the Park Service, along with the Coast Guard, power to regulate navigable waters in the national park system. |
| 0:26:52.140 | 1612.140 | MR. KNEEDLER | Alaska | So the question here is whether that was somehow abrogated when it comes to Alaska. |
| 0:27:08.300 | 1628.300 | JUSTICE GORSUCH | regulation | It says the Secretary may prescribe regulations concerning boating and other activities on or relating to water within system units. |
| 0:27:25.500 | 1645.500 | JUSTICE GORSUCH | statute | And I'd understand your argument better, I think, if the -- if the statute read that the Secretary could regulate water in or relating to system units, so not just water within system units but also water outside system units, like the water here that might have some downstream effect, say. |
| 0:27:42.380 | 1662.380 | JUSTICE GORSUCH | statute | But that's not what the statute says. |
| 0:27:45.180 | 1665.180 | JUSTICE GORSUCH | regulation | It says that the -- it may prescribe regulations concerning boating or other activities that themselves relate to water in system units. |
| 0:28:06.120 | 1686.120 | JUSTICE GORSUCH | Sturgeon | And I just didn't see that story told here, how Mr. Sturgeon's hovercraft would in some way impact water within the system units, meaning public -- public lands, public waters. |
| 0:28:06.800 | 1686.800 | JUSTICE GORSUCH | hovercraft | And I just didn't see that story told here, how Mr. Sturgeon's hovercraft would in some way impact water within the system units, meaning public -- public lands, public waters. |
| 0:28:13.560 | 1693.560 | JUSTICE GORSUCH | public lands | And I just didn't see that story told here, how Mr. Sturgeon's hovercraft would in some way impact water within the system units, meaning public -- public lands, public waters. |
| 0:28:15.020 | 1695.020 | JUSTICE GORSUCH | waters | And I just didn't see that story told here, how Mr. Sturgeon's hovercraft would in some way impact water within the system units, meaning public -- public lands, public waters. |
| 0:28:22.040 | 1702.040 | MR. KNEEDLER | statute | This is a general statute that applies within -- |
| 0:28:27.240 | 1707.240 | JUSTICE GORSUCH | statute | -- whether you even qualify -- whether you even qualify under this statute before we get to abrogation. |
| 0:28:40.920 | 1720.920 | JUSTICE GORSUCH | ANILCA | Within the outer boundaries but -- but not necessarily from -- we know from ANILCA, within the unit itself. |
| 0:29:00.100 | 1740.100 | MR. KNEEDLER | navigable | Well, non-navigable waters -- I mean, first of all, we're talk -- we're talking in -- in this instance about a -- a river that runs through federal lands on both sides. |
| 0:29:00.900 | 1740.900 | MR. KNEEDLER | waters | Well, non-navigable waters -- I mean, first of all, we're talk -- we're talking in -- in this instance about a -- a river that runs through federal lands on both sides. |
| 0:29:05.700 | 1745.700 | MR. KNEEDLER | river | Well, non-navigable waters -- I mean, first of all, we're talk -- we're talking in -- in this instance about a -- a river that runs through federal lands on both sides. |
| 0:29:13.440 | 1753.440 | MR. KNEEDLER | navigable | And it's -- it's been determined to be navigable, but it is -- it is within the federal -- the federal bounds. |
| 0:29:23.080 | 1763.080 | MR. KNEEDLER | navigable | Well, it would -- it would affect the non-navigable waters within the area. |
| 0:29:23.780 | 1763.780 | MR. KNEEDLER | waters | Well, it would -- it would affect the non-navigable waters within the area. |
| 0:29:27.300 | 1767.300 | MR. KNEEDLER | river | There could be stretches of the river that would be non-navigable under this Court's decision in PPL. |
| 0:29:28.000 | 1768.000 | MR. KNEEDLER | navigable | There could be stretches of the river that would be non-navigable under this Court's decision in PPL. |
| 0:29:34.440 | 1774.440 | JUSTICE GORSUCH | hovercraft | I'm wondering whether you have any argument that the use of the hovercraft outside the system units, boating activity outside the system unit -- premise me -- work on that premise -- would have any effect on the water within the system unit? |
| 0:29:48.120 | 1788.120 | MR. KNEEDLER | hovercraft | Well, it -- it has -- it has -- a hovercraft could have -- they're very loud, they're unsightly, and I don't -- I don't read this to say that the effect has to be on the water. |
| 0:29:58.360 | 1798.360 | MR. KNEEDLER | regulation | The purpose of giving the regulation, regulatory authority to the Park Service is to enable it to fulfill the purposes of the park as a whole, not just the waters. |
| 0:30:01.100 | 1801.100 | MR. KNEEDLER | park | The purpose of giving the regulation, regulatory authority to the Park Service is to enable it to fulfill the purposes of the park as a whole, not just the waters. |
| 0:30:05.860 | 1805.860 | MR. KNEEDLER | waters | The purpose of giving the regulation, regulatory authority to the Park Service is to enable it to fulfill the purposes of the park as a whole, not just the waters. |
| 0:30:07.940 | 1807.940 | JUSTICE GORSUCH | hovercraft | Do we know from the record that the hovercraft could be heard within the system unit itself? |
| 0:30:33.000 | 1833.000 | MR. KNEEDLER | statute | But if I could go to the second statutory provision I wanted -- wanted to cite, this is in 410hh-2 that we cite in our brief, again, against the backdrop of the 1976 statute, it says "the Secretary shall administer the lands, waters, and interests therein added to existing areas or established by the foregoing sections of ANILCA" -- the one that lists the parks -- "in accordance with the Organic Act as amended and supplemented." |
| 0:30:37.220 | 1837.220 | MR. KNEEDLER | waters | But if I could go to the second statutory provision I wanted -- wanted to cite, this is in 410hh-2 that we cite in our brief, again, against the backdrop of the 1976 statute, it says "the Secretary shall administer the lands, waters, and interests therein added to existing areas or established by the foregoing sections of ANILCA" -- the one that lists the parks -- "in accordance with the Organic Act as amended and supplemented." |
| 0:30:42.820 | 1842.820 | MR. KNEEDLER | section | But if I could go to the second statutory provision I wanted -- wanted to cite, this is in 410hh-2 that we cite in our brief, again, against the backdrop of the 1976 statute, it says "the Secretary shall administer the lands, waters, and interests therein added to existing areas or established by the foregoing sections of ANILCA" -- the one that lists the parks -- "in accordance with the Organic Act as amended and supplemented." |
| 0:30:43.840 | 1843.840 | MR. KNEEDLER | ANILCA | But if I could go to the second statutory provision I wanted -- wanted to cite, this is in 410hh-2 that we cite in our brief, again, against the backdrop of the 1976 statute, it says "the Secretary shall administer the lands, waters, and interests therein added to existing areas or established by the foregoing sections of ANILCA" -- the one that lists the parks -- "in accordance with the Organic Act as amended and supplemented." |
| 0:30:45.380 | 1845.380 | MR. KNEEDLER | park | But if I could go to the second statutory provision I wanted -- wanted to cite, this is in 410hh-2 that we cite in our brief, again, against the backdrop of the 1976 statute, it says "the Secretary shall administer the lands, waters, and interests therein added to existing areas or established by the foregoing sections of ANILCA" -- the one that lists the parks -- "in accordance with the Organic Act as amended and supplemented." |
| 0:31:02.640 | 1862.640 | MR. KNEEDLER | waters | This provision, far from abrogating the Secretary's authority, confirms that with respect to the waters that were added to the -- to the parks, to the park system -- |
| 0:31:05.020 | 1865.020 | MR. KNEEDLER | park | This provision, far from abrogating the Secretary's authority, confirms that with respect to the waters that were added to the -- to the parks, to the park system -- |
| 0:31:15.000 | 1875.000 | JUSTICE BREYER | statute | So your point here, which we'll hear something about probably on rebuttal, is that there's some other statutes here that, whatever it says in -- in 103(c), give direct authority to the Secretary to do this. |
| 0:31:56.120 | 1916.120 | JUSTICE BREYER | statute | Imagine something like Yellowstone, not perfectly, but it's a square and it is mostly -- it's federal, but there are a few houses belonging to Smith and Jones that are private, and the -- pass a statute, a reg, and the reg says: Oh, no bonfires within the boundaries of the park, which means Smith can't do it either. |
| 0:32:03.440 | 1923.440 | JUSTICE BREYER | park | Imagine something like Yellowstone, not perfectly, but it's a square and it is mostly -- it's federal, but there are a few houses belonging to Smith and Jones that are private, and the -- pass a statute, a reg, and the reg says: Oh, no bonfires within the boundaries of the park, which means Smith can't do it either. |
| 0:32:22.840 | 1942.840 | JUSTICE BREYER | statute | Well, I can -- the argument that it couldn't possibly be for the purposes of this statute is you wouldn't need -- you wouldn't need sentence 2 at all if that were the case. |
| 0:32:35.040 | 1955.040 | JUSTICE BREYER | river | You just wouldn't need it, period, because it wouldn't apply to the river regardless because it says it wouldn't. |
| 0:32:46.840 | 1966.840 | JUSTICE BREYER | park | And, therefore, when the national park system has a reg which says "applies within the boundaries of a national park," that is a rule that relates only to public lands. |
| 0:33:01.400 | 1981.400 | JUSTICE BREYER | public lands | And, therefore, when the national park system has a reg which says "applies within the boundaries of a national park," that is a rule that relates only to public lands. |
| 0:33:15.360 | 1995.360 | JUSTICE BREYER | public lands | And if it doesn't -- see, without that, this is meaningless, and so it must mean that, and so it must be that that kind of thing is what you can't do to enclaves within public lands in this area. |
| 0:33:18.400 | 1998.400 | JUSTICE BREYER | river | And the river is such an enclave because it is not a piece of property to which the United States has title. |
| 0:34:08.780 | 2048.780 | MR. KNEEDLER | waters | The -- the Submerged Lands Act conveyed to the state only submerged lands and interests in waters. |
| 0:34:10.860 | 2050.860 | MR. KNEEDLER | waters | It did not convey the waters themselves. |
| 0:34:17.460 | 2057.460 | MR. KNEEDLER | park | And so that -- so the second sentence of 103(c) does not affect the Park Service's regulation of navigable waters -- |
| 0:34:18.260 | 2058.260 | MR. KNEEDLER | regulation | And so that -- so the second sentence of 103(c) does not affect the Park Service's regulation of navigable waters -- |
| 0:34:19.580 | 2059.580 | MR. KNEEDLER | navigable | And so that -- so the second sentence of 103(c) does not affect the Park Service's regulation of navigable waters -- |
| 0:34:19.820 | 2059.820 | MR. KNEEDLER | waters | And so that -- so the second sentence of 103(c) does not affect the Park Service's regulation of navigable waters -- |
| 0:34:40.140 | 2080.140 | MR. KNEEDLER | waters | No, that -- that's -- that's critical to the point I was making before, that the 1976 Act is one of general applicability, specifically giving the Secretary the authority to regulate waters, including navigable waters. |
| 0:34:41.440 | 2081.440 | MR. KNEEDLER | navigable | No, that -- that's -- that's critical to the point I was making before, that the 1976 Act is one of general applicability, specifically giving the Secretary the authority to regulate waters, including navigable waters. |
| 0:34:43.320 | 2083.320 | MR. KNEEDLER | statute | And the other statute I mentioned specifically says that the Secretary may regulate the waters added to these park units according to the general authorities, which includes the '76 Act, and that ties directly to the fact that the waters, the navigable waters, were not conveyed to the state, and, therefore, the Secretary's regulatory authority over such waters is not -- is not -- |
| 0:34:47.360 | 2087.360 | MR. KNEEDLER | waters | And the other statute I mentioned specifically says that the Secretary may regulate the waters added to these park units according to the general authorities, which includes the '76 Act, and that ties directly to the fact that the waters, the navigable waters, were not conveyed to the state, and, therefore, the Secretary's regulatory authority over such waters is not -- is not -- |
| 0:34:48.960 | 2088.960 | MR. KNEEDLER | park | And the other statute I mentioned specifically says that the Secretary may regulate the waters added to these park units according to the general authorities, which includes the '76 Act, and that ties directly to the fact that the waters, the navigable waters, were not conveyed to the state, and, therefore, the Secretary's regulatory authority over such waters is not -- is not -- |
| 0:34:57.280 | 2097.280 | MR. KNEEDLER | navigable | And the other statute I mentioned specifically says that the Secretary may regulate the waters added to these park units according to the general authorities, which includes the '76 Act, and that ties directly to the fact that the waters, the navigable waters, were not conveyed to the state, and, therefore, the Secretary's regulatory authority over such waters is not -- is not -- |
| 0:35:12.920 | 2112.920 | JUSTICE SOTOMAYOR | statute | Under your reading of this statute, what sorts of regulations can't you pass? |
| 0:35:15.260 | 2115.260 | JUSTICE SOTOMAYOR | regulation | Under your reading of this statute, what sorts of regulations can't you pass? |
| 0:35:41.320 | 2141.320 | MR. KNEEDLER | Alaska | The one were the inholdings, so the issue here was -- that was different about Alaska was that, within the outer boundaries, there were lands selected by the state or selected by native corporations, and Congress did not want them to be administered just like the Park Service lands themselves, the -- the -- the usual Park Service lands. |
| 0:35:52.160 | 2152.160 | MR. KNEEDLER | park | The one were the inholdings, so the issue here was -- that was different about Alaska was that, within the outer boundaries, there were lands selected by the state or selected by native corporations, and Congress did not want them to be administered just like the Park Service lands themselves, the -- the -- the usual Park Service lands. |
| 0:36:11.500 | 2171.500 | MR. KNEEDLER | navigable | It was not about navigable waters. |
| 0:36:11.960 | 2171.960 | MR. KNEEDLER | waters | It was not about navigable waters. |
| 0:36:20.700 | 2180.700 | MR. KNEEDLER | navigable | -- of navigable waters -- |
| 0:36:21.140 | 2181.140 | MR. KNEEDLER | waters | -- of navigable waters -- |
| 0:36:32.360 | 2192.360 | JUSTICE GORSUCH | Alaska | Does the government claim plenary authority over all waterways in Alaska? |
| 0:36:35.680 | 2195.680 | MR. KNEEDLER | navigable | No. We're only -- we're only talking here about waterways, navigable waterways within national parks. |
| 0:36:38.240 | 2198.240 | MR. KNEEDLER | park | No. We're only -- we're only talking here about waterways, navigable waterways within national parks. |
| 0:37:16.460 | 2236.460 | MR. KNEEDLER | navigable | I -- I -- I -- it's -- it's pretty close to plenary, but this Court has recognized that there is -- but the Secretary hasn't exercised it to that degree, but -- but the -- this Court has recognized in cases involving navigable water that the fact that the state owns the submerged lands does not interfere with Congress's ability to regulate the waters -- |
| 0:37:22.520 | 2242.520 | MR. KNEEDLER | waters | I -- I -- I -- it's -- it's pretty close to plenary, but this Court has recognized that there is -- but the Secretary hasn't exercised it to that degree, but -- but the -- this Court has recognized in cases involving navigable water that the fact that the state owns the submerged lands does not interfere with Congress's ability to regulate the waters -- |
| 0:37:27.240 | 2247.240 | CHIEF JUSTICE ROBERTS | Alaska | The navigational servitude, I mean, that's really about if Alaska decided to, you know, build a bridge across the river and things like that. |
| 0:37:29.840 | 2249.840 | CHIEF JUSTICE ROBERTS | river | The navigational servitude, I mean, that's really about if Alaska decided to, you know, build a bridge across the river and things like that. |
| 0:37:34.020 | 2254.020 | CHIEF JUSTICE ROBERTS | regulation | I don't know that it reaches as far to justify any type of regulation on -- on the water. |
| 0:37:38.620 | 2258.620 | MR. KNEEDLER | park | Well, Congress regulates, again, outside of parks, regulates extensively navigable waters for dredging and filling, for -- |
| 0:37:41.280 | 2261.280 | MR. KNEEDLER | navigable | Well, Congress regulates, again, outside of parks, regulates extensively navigable waters for dredging and filling, for -- |
| 0:37:41.760 | 2261.760 | MR. KNEEDLER | waters | Well, Congress regulates, again, outside of parks, regulates extensively navigable waters for dredging and filling, for -- |
| 0:37:44.300 | 2264.300 | CHIEF JUSTICE ROBERTS | navigable | It regulates navigable waters. |
| 0:37:44.300 | 2264.300 | CHIEF JUSTICE ROBERTS | waters | It regulates navigable waters. |
| 0:38:04.380 | 2284.380 | CHIEF JUSTICE ROBERTS | regulation | They -- what they don't agree is that that is a lever that gives you authority to do this sort of day-to-day regulation, such as, you know, the hovercraft traffic. |
| 0:38:07.020 | 2287.020 | CHIEF JUSTICE ROBERTS | hovercraft | They -- what they don't agree is that that is a lever that gives you authority to do this sort of day-to-day regulation, such as, you know, the hovercraft traffic. |
| 0:38:09.740 | 2289.740 | CHIEF JUSTICE ROBERTS | hovercraft | And while -- while you may think a hovercraft is unsightly, I mean, if you're trying to get from point A to point B, it's pretty beautiful. |
| 0:38:25.220 | 2305.220 | MR. KNEEDLER | Alaska | Well, there are -- there are -- there are a number of instances within the Act in which Congress has specifically required the Secretary to accommodate, to take into account what's different about Alaska, by requiring them to accommodate methods of transportation like air. |
| 0:38:40.360 | 2320.360 | MR. KNEEDLER | park | The fact that the Secretary is -- is permitted to regulate boating only subject -- only reasonably means that he can regulate boating, means the National Park Service can regulate boating -- |
| 0:38:42.560 | 2322.560 | MR. KNEEDLER | waters | -- on -- on waters within the park. |
| 0:38:43.900 | 2323.900 | MR. KNEEDLER | park | -- on -- on waters within the park. |
| 0:38:55.280 | 2335.280 | JUSTICE SOTOMAYOR | regulation | Are you saying that 103(c) basically, because of the navigational servitude, the other regulations you've pointed to, doesn't permit the government to regulate activities on the territorial lands or -- or on the submerged lands, but it does give it basically plenary authority over navigable waters? |
| 0:39:13.860 | 2353.860 | JUSTICE SOTOMAYOR | navigable | Are you saying that 103(c) basically, because of the navigational servitude, the other regulations you've pointed to, doesn't permit the government to regulate activities on the territorial lands or -- or on the submerged lands, but it does give it basically plenary authority over navigable waters? |
| 0:39:14.540 | 2354.540 | JUSTICE SOTOMAYOR | waters | Are you saying that 103(c) basically, because of the navigational servitude, the other regulations you've pointed to, doesn't permit the government to regulate activities on the territorial lands or -- or on the submerged lands, but it does give it basically plenary authority over navigable waters? |
| 0:39:19.280 | 2359.280 | MR. KNEEDLER | park | I think it gives it -- it preserves for the -- through the Park Service whatever the scope of authority that -- that Congress would have or the federal government has over navigable waters. |
| 0:39:24.920 | 2364.920 | MR. KNEEDLER | navigable | I think it gives it -- it preserves for the -- through the Park Service whatever the scope of authority that -- that Congress would have or the federal government has over navigable waters. |
| 0:39:25.380 | 2365.380 | MR. KNEEDLER | waters | I think it gives it -- it preserves for the -- through the Park Service whatever the scope of authority that -- that Congress would have or the federal government has over navigable waters. |
| 0:39:29.340 | 2369.340 | JUSTICE SOTOMAYOR | regulation | -- basically saying, whatever the regulations were under the Organic Act or even under this Act, and charging you with taking care of certain parks, that the navigable waters are part of that charge? |
| 0:39:38.420 | 2378.420 | JUSTICE SOTOMAYOR | park | -- basically saying, whatever the regulations were under the Organic Act or even under this Act, and charging you with taking care of certain parks, that the navigable waters are part of that charge? |
| 0:39:39.880 | 2379.880 | JUSTICE SOTOMAYOR | navigable | -- basically saying, whatever the regulations were under the Organic Act or even under this Act, and charging you with taking care of certain parks, that the navigable waters are part of that charge? |
| 0:39:40.440 | 2380.440 | JUSTICE SOTOMAYOR | waters | -- basically saying, whatever the regulations were under the Organic Act or even under this Act, and charging you with taking care of certain parks, that the navigable waters are part of that charge? |
| 0:39:50.940 | 2390.940 | MR. KNEEDLER | regulation | And the uplands are different, and that's really what drove 103(c), was to make sure that these land selections were not going to be subject to the general regulations of the Park Service. |
| 0:39:51.840 | 2391.840 | MR. KNEEDLER | park | And the uplands are different, and that's really what drove 103(c), was to make sure that these land selections were not going to be subject to the general regulations of the Park Service. |
| 0:39:56.860 | 2396.860 | MR. KNEEDLER | regulation | There -- there are -- there are really only three sets of regulations that the Park Service has applied in -- in -- outside of federally owned lands. |
| 0:39:57.940 | 2397.940 | MR. KNEEDLER | park | There -- there are -- there are really only three sets of regulations that the Park Service has applied in -- in -- outside of federally owned lands. |
| 0:40:05.480 | 2405.480 | MR. KNEEDLER | regulation | One is the regulation of navigable waters pursuant to an express statutory authorization in the '76 Act. |
| 0:40:06.660 | 2406.660 | MR. KNEEDLER | navigable | One is the regulation of navigable waters pursuant to an express statutory authorization in the '76 Act. |
| 0:40:07.040 | 2407.040 | MR. KNEEDLER | waters | One is the regulation of navigable waters pursuant to an express statutory authorization in the '76 Act. |
| 0:40:13.640 | 2413.640 | MR. KNEEDLER | regulation | The other two have to do with the regulation of solid waste pursuant to a specific statutory directive to regulate within the boundaries of national park units, just like this statute talks about within system units, and the other is mining in areas of the national park system, which the Park Service has applied regulations there. |
| 0:40:23.200 | 2423.200 | MR. KNEEDLER | park | The other two have to do with the regulation of solid waste pursuant to a specific statutory directive to regulate within the boundaries of national park units, just like this statute talks about within system units, and the other is mining in areas of the national park system, which the Park Service has applied regulations there. |
| 0:40:24.840 | 2424.840 | MR. KNEEDLER | statute | The other two have to do with the regulation of solid waste pursuant to a specific statutory directive to regulate within the boundaries of national park units, just like this statute talks about within system units, and the other is mining in areas of the national park system, which the Park Service has applied regulations there. |
| 0:40:39.306 | 2439.306 | MR. KNEEDLER | park | The Park Service -- |
| 0:40:56.120 | 2456.120 | CHIEF JUSTICE ROBERTS | public lands | It's only because you don't think that water is included in public lands that their argument doesn't work? |
| 0:41:07.340 | 2467.340 | MR. KNEEDLER | regulation | The second argument is, if you have a regulation that, in the case -- examples I mentioned, regulations issued pursuant to statutory directive to apply to both public and non-public lands within the national park, that comes within the reference they are not regulations applicable solely to -- |
| 0:41:16.640 | 2476.640 | MR. KNEEDLER | public lands | The second argument is, if you have a regulation that, in the case -- examples I mentioned, regulations issued pursuant to statutory directive to apply to both public and non-public lands within the national park, that comes within the reference they are not regulations applicable solely to -- |
| 0:41:18.360 | 2478.360 | MR. KNEEDLER | park | The second argument is, if you have a regulation that, in the case -- examples I mentioned, regulations issued pursuant to statutory directive to apply to both public and non-public lands within the national park, that comes within the reference they are not regulations applicable solely to -- |
| 0:41:23.980 | 2483.980 | MR. KNEEDLER | public lands | -- public lands and -- |
| 0:41:28.960 | 2488.960 | CHIEF JUSTICE ROBERTS | regulation | -- that's the -- that's one of your arguments that causes me concern, because you're saying that if the regulation applies to the -- the private or state land, then it is not a regulation solely applicable to public land and, therefore, it's not covered. |
| 0:41:44.960 | 2504.960 | CHIEF JUSTICE ROBERTS | park | But the -- the sentence is obviously designed to protect the state, the natives, and the private landholders against the federal government or the Park Service to whatever extent we can debate. |
| 0:41:48.340 | 2508.340 | CHIEF JUSTICE ROBERTS | park | But to say that all the Park Service has to do to get around it is say, oh, and this applies to the inholdings, that can't be right. |
| 0:41:58.600 | 2518.600 | MR. KNEEDLER | park | Well, I'm -- I'm not saying -- I'm not -- in fact, I would disclaim the proposition that the Park Service could treat them as -- as -- as -- the same way it treats regular Park Service lands. |
| 0:42:09.000 | 2529.000 | MR. KNEEDLER | regulation | And the only examples where it has issued regulations that go beyond that are pursuant to specific statutory directive, of which the 1976 Act regulating waters is one. |
| 0:42:16.720 | 2536.720 | MR. KNEEDLER | waters | And the only examples where it has issued regulations that go beyond that are pursuant to specific statutory directive, of which the 1976 Act regulating waters is one. |
| 0:42:23.820 | 2543.820 | JUSTICE KAGAN | public lands | -- I understand your view, Mr. Kneedler, what you're saying this means is that non-public lands shall not be subject to regulations that are applicable only to public lands. |
| 0:42:27.140 | 2547.140 | JUSTICE KAGAN | regulation | -- I understand your view, Mr. Kneedler, what you're saying this means is that non-public lands shall not be subject to regulations that are applicable only to public lands. |
| 0:42:31.460 | 2551.460 | JUSTICE KAGAN | statute | And you don't need a statute to tell you that. |
| 0:42:33.500 | 2553.500 | JUSTICE KAGAN | public lands | Of course, non-public lands aren't subject to regulations applicable solely to public lands. |
| 0:42:36.240 | 2556.240 | JUSTICE KAGAN | regulation | Of course, non-public lands aren't subject to regulations applicable solely to public lands. |
| 0:42:40.240 | 2560.240 | JUSTICE KAGAN | statute | If that's what the statute was saying, who would need a statute? |
| 0:42:44.580 | 2564.580 | MR. KNEEDLER | statute | Well, I -- I think the purpose of the statute -- and, again, I think this comes through in the legislative history that -- that is cited on the other side -- the native groups were concerned, and as was the state, that because large tracts of land that they had selected were going to be included within the -- in the -- within the outer boundaries, that they were not going to be -- that they would be treated just like -- they wanted assurance that they wouldn't be treated just like Park Service. |
| 0:43:08.220 | 2588.220 | MR. KNEEDLER | park | Well, I -- I think the purpose of the statute -- and, again, I think this comes through in the legislative history that -- that is cited on the other side -- the native groups were concerned, and as was the state, that because large tracts of land that they had selected were going to be included within the -- in the -- within the outer boundaries, that they were not going to be -- that they would be treated just like -- they wanted assurance that they wouldn't be treated just like Park Service. |
| 0:43:13.240 | 2593.240 | MR. KNEEDLER | section | It's important to recognize that this is subsection (c) of a section that deals with maps. |
| 0:43:23.820 | 2603.820 | MR. KNEEDLER | regulation | It isn't -- it -- it doesn't -- you would think if there was some major substantive change -- work that this was supposed to do aside from the substantive regulations, it would appear elsewhere. |
| 0:43:28.960 | 2608.960 | JUSTICE KAGAN | park | But just on the face of things, Mr. Kneedler, if -- if the Park Service issues a regulation and the regulation says this applies only to public lands within a park, right, and you're not a public land within a park, you're a private land within a park, what kind of assurance do you need? |
| 0:43:30.120 | 2610.120 | JUSTICE KAGAN | regulation | But just on the face of things, Mr. Kneedler, if -- if the Park Service issues a regulation and the regulation says this applies only to public lands within a park, right, and you're not a public land within a park, you're a private land within a park, what kind of assurance do you need? |
| 0:43:34.100 | 2614.100 | JUSTICE KAGAN | public lands | But just on the face of things, Mr. Kneedler, if -- if the Park Service issues a regulation and the regulation says this applies only to public lands within a park, right, and you're not a public land within a park, you're a private land within a park, what kind of assurance do you need? |
| 0:43:48.500 | 2628.500 | JUSTICE KAGAN | park | It's like you know that you're not a public land, so it doesn't matter that you're in the park. |
| 0:43:49.720 | 2629.720 | JUSTICE KAGAN | statute | You don't need a special statute to tell you that, do you? |
| 0:43:53.160 | 2633.160 | JUSTICE KAGAN | statute | You only need a special statute if the special statute exempts you from something that would otherwise apply to you. |
| 0:44:05.620 | 2645.620 | MR. KNEEDLER | statute | I think that the -- I think that there was a lot of debate about -- about different versions of the statute. |
| 0:44:09.580 | 2649.580 | MR. KNEEDLER | section | And I -- and I think if you -- if you recall, as I said, this was in a section dealing with maps, and the statute required that the -- that the -- that the lot -- the boundaries -- that maps be published identifying what the parks were. |
| 0:44:11.060 | 2651.060 | MR. KNEEDLER | statute | And I -- and I think if you -- if you recall, as I said, this was in a section dealing with maps, and the statute required that the -- that the -- that the lot -- the boundaries -- that maps be published identifying what the parks were. |
| 0:44:18.140 | 2658.140 | MR. KNEEDLER | park | And I -- and I think if you -- if you recall, as I said, this was in a section dealing with maps, and the statute required that the -- that the -- that the lot -- the boundaries -- that maps be published identifying what the parks were. |
| 0:44:32.420 | 2672.420 | MR. KNEEDLER | public lands | And so subsection (c) says, well, yeah, that -- that may be the boundaries of what was designated, but we want to be clear that it's only -- it's only the public lands that will be deemed to be portions -- |
| 0:45:29.060 | 2729.060 | MR. KNEEDLER | park | I mean, I think -- I think this provision was in there because if the -- if you had native or state selected lands or native lands, the corporation -- the native corporation, they were -- if they decided to sell their land, this just says that the Park Service could purchase it. |
| 0:45:56.420 | 2756.420 | JUSTICE BREYER | public lands | You're not -- I -- I started out thinking that if a reg applies to Mr. Smith's inholding in Yosemite because it applies to all of Yosemite, that that is solely public lands. |
| 0:46:02.780 | 2762.780 | JUSTICE BREYER | public lands | Because if the only things that count as a reg for public lands -- we've said this three times -- are -- are those regs that say they don't apply to Smith's inholding, you don't need this statute, okay? |
| 0:46:12.260 | 2772.260 | JUSTICE BREYER | statute | Because if the only things that count as a reg for public lands -- we've said this three times -- are -- are those regs that say they don't apply to Smith's inholding, you don't need this statute, okay? |
| 0:46:28.140 | 2788.140 | JUSTICE BREYER | public lands | But what I took your basic arguments to be, one, that water, unlike Mr. Smith's cabin, is close enough to public lands that it's out of this thing. |
| 0:46:34.880 | 2794.880 | JUSTICE BREYER | statute | Two, even if it isn't, there are other statutes that give specific authority to the government to regulate the water. |
| 0:47:05.920 | 2825.920 | MR. KNEEDLER | regulation | -- I think it's basically correct, but there is the category of regulations that are not applicable solely to public lands because -- because they have been made applicable to inholdings within the Park Service. |
| 0:47:08.620 | 2828.620 | MR. KNEEDLER | public lands | -- I think it's basically correct, but there is the category of regulations that are not applicable solely to public lands because -- because they have been made applicable to inholdings within the Park Service. |
| 0:47:14.860 | 2834.860 | MR. KNEEDLER | park | -- I think it's basically correct, but there is the category of regulations that are not applicable solely to public lands because -- because they have been made applicable to inholdings within the Park Service. |
| 0:47:30.916 | 2850.916 | MR. KNEEDLER | waters | Waters which were not -- |
| 0:47:58.300 | 2878.300 | MR. KNEEDLER | regulation | Well, in the 1999 regulations that Congress allowed to go into effect, the -- the Park Service by rule identified the Park Service units or the areas added or expanded by ANILCA in which there were reserved water rights. |
| 0:48:03.160 | 2883.160 | MR. KNEEDLER | park | Well, in the 1999 regulations that Congress allowed to go into effect, the -- the Park Service by rule identified the Park Service units or the areas added or expanded by ANILCA in which there were reserved water rights. |
| 0:48:10.140 | 2890.140 | MR. KNEEDLER | ANILCA | Well, in the 1999 regulations that Congress allowed to go into effect, the -- the Park Service by rule identified the Park Service units or the areas added or expanded by ANILCA in which there were reserved water rights. |
| 0:48:24.120 | 2904.120 | MR. KNEEDLER | Yukon | In fact, the one we have here is the Yukon-Charley Rivers National Preserve, and it -- and it specifically defines as one of the purposes to preserve the entire Charley river basin, including streams and lakes. |
| 0:48:24.940 | 2904.940 | MR. KNEEDLER | river | In fact, the one we have here is the Yukon-Charley Rivers National Preserve, and it -- and it specifically defines as one of the purposes to preserve the entire Charley river basin, including streams and lakes. |
| 0:48:40.240 | 2920.240 | MR. KNEEDLER | waters | So that -- that clearly identifies the protection of the integrity of those waters and the -- and the -- the scenic values associated with them. |
| 0:48:46.020 | 2926.020 | MR. KNEEDLER | park | That's why we have national parks. |
| 0:49:09.780 | 2949.780 | JUSTICE ALITO | navigable | -- to regulate the navigable waters? |
| 0:49:10.340 | 2950.340 | JUSTICE ALITO | waters | -- to regulate the navigable waters? |
| 0:49:55.040 | 2995.040 | JUSTICE ALITO | park | As to water for which there is a reserved right, the federal government, the Park Service can do -- can regulate completely, as it -- is that right? |
| 0:50:02.620 | 3002.620 | MR. KNEEDLER | park | I -- I wouldn't -- I -- I -- I think within the national park system it overlaps with the 1976 statute that I -- that I mentioned, which I -- I think directly -- you don't have to go through the reserved water rights approach to get there -- within national parks, the -- the -- Katie John's subsistence use could have been satisfied by relying on the 1976 Act and not relying on reserved water rights. |
| 0:50:05.540 | 3005.540 | MR. KNEEDLER | statute | I -- I wouldn't -- I -- I -- I think within the national park system it overlaps with the 1976 statute that I -- that I mentioned, which I -- I think directly -- you don't have to go through the reserved water rights approach to get there -- within national parks, the -- the -- Katie John's subsistence use could have been satisfied by relying on the 1976 Act and not relying on reserved water rights. |
| 0:50:23.640 | 3023.640 | MR. KNEEDLER | navigable | And all we have here are navigable waters within national parks. |
| 0:50:24.320 | 3024.320 | MR. KNEEDLER | waters | And all we have here are navigable waters within national parks. |
| 0:50:25.360 | 3025.360 | MR. KNEEDLER | park | And all we have here are navigable waters within national parks. |
| 0:50:39.060 | 3039.060 | JUSTICE ALITO | Alaska | -- slip in one more question since you referred to Katie -- to Katie John, and I'll ask you the same question that was asked of counsel for Alaska. |
| 0:50:56.720 | 3056.720 | MR. KNEEDLER | regulation | I -- I -- I would certainly hope not, but -- but, I mean, I think Petitioners have a different -- Petitioner and the State have a difficult argument because Katie John and the regulations implementing it, once the Congress specifically allowed to go into effect with full knowledge that Katie John was out there, it turns on the definition of public lands, which is a term that runs throughout the Act, which is, we think, a good reason why -- why it should be upheld. |
| 0:51:04.760 | 3064.760 | MR. KNEEDLER | public lands | I -- I -- I would certainly hope not, but -- but, I mean, I think Petitioners have a different -- Petitioner and the State have a difficult argument because Katie John and the regulations implementing it, once the Congress specifically allowed to go into effect with full knowledge that Katie John was out there, it turns on the definition of public lands, which is a term that runs throughout the Act, which is, we think, a good reason why -- why it should be upheld. |
| 0:51:15.820 | 3075.820 | MR. KNEEDLER | regulation | At the very least, Katie John demonstrates the importance of federal regulation of waters within these areas, in that instance for -- for subsistence uses. |
| 0:51:16.600 | 3076.600 | MR. KNEEDLER | waters | At the very least, Katie John demonstrates the importance of federal regulation of waters within these areas, in that instance for -- for subsistence uses. |
| 0:51:29.480 | 3089.480 | MR. KNEEDLER | park | One of the -- one of the things the Park Service could never do is grant access to private lands. |
| 0:51:33.180 | 3093.180 | MR. KNEEDLER | park | The Park Service not only regulates things that you can't do in national parks but things that they have to allow, like access, camping, picnicking. |
| 0:51:42.620 | 3102.620 | MR. KNEEDLER | park | Well, obviously, the Park Service cannot allow people to have private -- have access to the private inholdings. |
| 0:51:49.980 | 3109.980 | MR. KNEEDLER | park | So one of the reasons why the Park Service might want to acquire the adjacent lands or the inholdings would be for the purpose of allowing public access to those areas. |
| 0:52:02.400 | 3122.400 | MR. KNEEDLER | ANILCA | But I also want to underscore that there are so many provisions of ANILCA that specifically refer to water and, in fact, the regulation of water. |
| 0:52:05.380 | 3125.380 | MR. KNEEDLER | regulation | But I also want to underscore that there are so many provisions of ANILCA that specifically refer to water and, in fact, the regulation of water. |
| 0:52:11.020 | 3131.020 | MR. KNEEDLER | park | One of the ones I mentioned, 3170(a), specifically allows the Park Service to regulate boating in -- in these areas. |
| 0:52:20.480 | 3140.480 | MR. KNEEDLER | regulation | That picks up on the 1976 Act, the general application that is made specific here by allowing regulation of boating. |
| 0:52:29.440 | 3149.440 | MR. KNEEDLER | river | There's the Wild and Scenic Rivers Act, which the whole purpose of designating a river within these national parks is to preserve -- |
| 0:52:34.100 | 3154.100 | MR. KNEEDLER | park | There's the Wild and Scenic Rivers Act, which the whole purpose of designating a river within these national parks is to preserve -- |
| 0:52:35.940 | 3155.940 | MR. KNEEDLER | river | -- the river. |
| 0:52:37.360 | 3157.360 | JUSTICE KAVANAUGH | park | -- that says that the Park Service has plenary authority over all the navigable rivers within the conservation system unit, nor is there any indication by any member of Congress of such a authority? |
| 0:52:40.120 | 3160.120 | JUSTICE KAVANAUGH | navigable | -- that says that the Park Service has plenary authority over all the navigable rivers within the conservation system unit, nor is there any indication by any member of Congress of such a authority? |
| 0:52:40.680 | 3160.680 | JUSTICE KAVANAUGH | river | -- that says that the Park Service has plenary authority over all the navigable rivers within the conservation system unit, nor is there any indication by any member of Congress of such a authority? |
| 0:52:57.860 | 3177.860 | MR. KNEEDLER | park | Well, I mean, putting to one side whatever we might mean by plenary, the 1976 Act specifically gives the parks -- |
| 0:53:03.080 | 3183.080 | JUSTICE KAVANAUGH | Alaska | This would have been a huge deal for the people of Alaska and the representatives from Alaska to accept full or close to full Park Service authority over all the navigable rivers, yet -- |
| 0:53:08.100 | 3188.100 | JUSTICE KAVANAUGH | park | This would have been a huge deal for the people of Alaska and the representatives from Alaska to accept full or close to full Park Service authority over all the navigable rivers, yet -- |
| 0:53:09.800 | 3189.800 | JUSTICE KAVANAUGH | navigable | This would have been a huge deal for the people of Alaska and the representatives from Alaska to accept full or close to full Park Service authority over all the navigable rivers, yet -- |
| 0:53:10.140 | 3190.140 | JUSTICE KAVANAUGH | river | This would have been a huge deal for the people of Alaska and the representatives from Alaska to accept full or close to full Park Service authority over all the navigable rivers, yet -- |
| 0:53:21.900 | 3201.900 | MR. KNEEDLER | waters | I -- I -- I see no indication in that, and this 1410hh-2 that I mentioned specifically says that the waters added to these areas are subject to regulation under the Park Service's general authority, which includes the 1976 Act. |
| 0:53:24.580 | 3204.580 | MR. KNEEDLER | regulation | I -- I -- I see no indication in that, and this 1410hh-2 that I mentioned specifically says that the waters added to these areas are subject to regulation under the Park Service's general authority, which includes the 1976 Act. |
| 0:53:25.500 | 3205.500 | MR. KNEEDLER | park | I -- I -- I see no indication in that, and this 1410hh-2 that I mentioned specifically says that the waters added to these areas are subject to regulation under the Park Service's general authority, which includes the 1976 Act. |
| 0:53:33.900 | 3213.900 | MR. KNEEDLER | park | I think the extraordinary thing would be to say that -- that the federal government through the Park Service did not have the authority to regulate navigable waters, not just any navigable waters but navigable waters in park areas set aside for the very purpose, often express purpose of preserving the values of the rivers and lakes and streams that were in their midst. |
| 0:53:36.860 | 3216.860 | MR. KNEEDLER | navigable | I think the extraordinary thing would be to say that -- that the federal government through the Park Service did not have the authority to regulate navigable waters, not just any navigable waters but navigable waters in park areas set aside for the very purpose, often express purpose of preserving the values of the rivers and lakes and streams that were in their midst. |
| 0:53:37.620 | 3217.620 | MR. KNEEDLER | waters | I think the extraordinary thing would be to say that -- that the federal government through the Park Service did not have the authority to regulate navigable waters, not just any navigable waters but navigable waters in park areas set aside for the very purpose, often express purpose of preserving the values of the rivers and lakes and streams that were in their midst. |
| 0:53:47.460 | 3227.460 | MR. KNEEDLER | river | I think the extraordinary thing would be to say that -- that the federal government through the Park Service did not have the authority to regulate navigable waters, not just any navigable waters but navigable waters in park areas set aside for the very purpose, often express purpose of preserving the values of the rivers and lakes and streams that were in their midst. |
| 0:53:53.780 | 3233.780 | MR. KNEEDLER | statute | The -- this -- this -- this is a very water-centric statute. |
| 0:54:00.080 | 3240.080 | MR. KNEEDLER | navigable | And I think it would turn it upside down to say that Congress, of all things, was incapable of regulating the navigable waters within -- within the park system. |
| 0:54:00.520 | 3240.520 | MR. KNEEDLER | waters | And I think it would turn it upside down to say that Congress, of all things, was incapable of regulating the navigable waters within -- within the park system. |
| 0:54:02.000 | 3242.000 | MR. KNEEDLER | park | And I think it would turn it upside down to say that Congress, of all things, was incapable of regulating the navigable waters within -- within the park system. |
| 0:54:03.560 | 3243.560 | CHIEF JUSTICE ROBERTS | waters | Well, but, I mean, the waters are very important to Alaskan way of life in the way they aren't elsewhere. |
| 0:54:19.340 | 3259.340 | CHIEF JUSTICE ROBERTS | river | And I -- I guess the argument on the other side, it would be pretty extraordinary if you go to the trouble to say you only can regulate lands with respect to which you have title, and you say from that you get the authority over the rivers, even though title in the submerged lands is in the state? |
| 0:54:27.720 | 3267.720 | MR. KNEEDLER | navigable | Well, our argument doesn't depend on the title question or -- or control over navigable waters. |
| 0:54:28.160 | 3268.160 | MR. KNEEDLER | waters | Well, our argument doesn't depend on the title question or -- or control over navigable waters. |
| 0:54:35.020 | 3275.020 | MR. KNEEDLER | ANILCA | But, on the points you mentioned, ANILCA itself embodies the compromise or the -- or the balance of the competing values. |
| 0:54:41.480 | 3281.480 | MR. KNEEDLER | park | In most parks, you can't hunt. |
| 0:54:57.840 | 3297.840 | MR. KNEEDLER | park | There's specific provisions for access to inholdings, something that you don't normally have in other national parks, but, because there were inholdings, there are provisions for that. |
| 0:55:06.860 | 3306.860 | MR. KNEEDLER | Alaska | The very things that make Alaska different are accommodated in this statute. |
| 0:55:09.640 | 3309.640 | MR. KNEEDLER | statute | The very things that make Alaska different are accommodated in this statute. |
| 0:55:12.460 | 3312.460 | MR. KNEEDLER | Alaska | But one of the things that -- that is not different about Alaska is the importance of the federal government having control over the navigable waters that are the centerpiece of the parks. |
| 0:55:16.300 | 3316.300 | MR. KNEEDLER | navigable | But one of the things that -- that is not different about Alaska is the importance of the federal government having control over the navigable waters that are the centerpiece of the parks. |
| 0:55:16.780 | 3316.780 | MR. KNEEDLER | waters | But one of the things that -- that is not different about Alaska is the importance of the federal government having control over the navigable waters that are the centerpiece of the parks. |
| 0:55:18.880 | 3318.880 | MR. KNEEDLER | park | But one of the things that -- that is not different about Alaska is the importance of the federal government having control over the navigable waters that are the centerpiece of the parks. |
| 0:55:20.280 | 3320.280 | MR. KNEEDLER | Alaska | What is different about Alaska is the large tracts of inholdings, which is really what the focus of 103(c) was. |
| 0:55:30.120 | 3330.120 | MR. KNEEDLER | park | And in that situation and only in very limited circumstances has the Park Service ever applied regulations that go beyond simply the public lands to -- to embrace the broader -- the broader system of -- of -- of lands. |
| 0:55:31.680 | 3331.680 | MR. KNEEDLER | regulation | And in that situation and only in very limited circumstances has the Park Service ever applied regulations that go beyond simply the public lands to -- to embrace the broader -- the broader system of -- of -- of lands. |
| 0:55:34.580 | 3334.580 | MR. KNEEDLER | public lands | And in that situation and only in very limited circumstances has the Park Service ever applied regulations that go beyond simply the public lands to -- to embrace the broader -- the broader system of -- of -- of lands. |
| 0:55:41.880 | 3341.880 | MR. KNEEDLER | Yukon | And, again, this is the Yukon-Charley River's national monument. |
| 0:55:42.780 | 3342.780 | MR. KNEEDLER | river | And, again, this is the Yukon-Charley River's national monument. |
| 0:55:48.600 | 3348.600 | MR. KNEEDLER | park | It would be extraordinary to conclude that the Park Service, without some express statement to that effect in the -- in the statute, could not regulate it. |
| 0:55:52.540 | 3352.540 | MR. KNEEDLER | statute | It would be extraordinary to conclude that the Park Service, without some express statement to that effect in the -- in the statute, could not regulate it. |
| 0:55:55.280 | 3355.280 | MR. KNEEDLER | statute | And, as I say, this statute giving it the authority to regulate waters is -- is explicit on that point. |
| 0:55:57.540 | 3357.540 | MR. KNEEDLER | waters | And, as I say, this statute giving it the authority to regulate waters is -- is explicit on that point. |
| 0:56:09.670 | 3369.670 | MR. FINDLEY | ANILCA | Counsel several times cited the provision of ANILCA, saying these parks and preserves shall be governed in accord to the Organic Act. |
| 0:56:10.690 | 3370.690 | MR. FINDLEY | park | Counsel several times cited the provision of ANILCA, saying these parks and preserves shall be governed in accord to the Organic Act. |
| 0:56:15.690 | 3375.690 | MR. FINDLEY | statute | Counsel forgot to finish the provision of the statute that says "and as amended or modified by ANILCA." |
| 0:56:18.630 | 3378.630 | MR. FINDLEY | ANILCA | Counsel forgot to finish the provision of the statute that says "and as amended or modified by ANILCA." |
| 0:56:23.150 | 3383.150 | MR. FINDLEY | ANILCA | So every time they refer to the Organic Act they have to read it together with ANILCA. |
| 0:56:25.050 | 3385.050 | MR. FINDLEY | section | And you have to read it with Section 103(c), at the very front of the statute, it's a linchpin, and it's foundational. |
| 0:56:27.710 | 3387.710 | MR. FINDLEY | statute | And you have to read it with Section 103(c), at the very front of the statute, it's a linchpin, and it's foundational. |
| 0:56:36.810 | 3396.810 | MR. FINDLEY | park | And what it's designed to do is say, if the federal government doesn't have title, it's not public land, it is not part of the park, and it's there to prevent the Park Service from using its Organic Act authority to regulate extraterritorially to land that -- |
| 0:56:57.910 | 3417.910 | JUSTICE SOTOMAYOR | navigable | Navigable waters are navigable waters. |
| 0:56:58.370 | 3418.370 | JUSTICE SOTOMAYOR | waters | Navigable waters are navigable waters. |
| 0:57:21.870 | 3441.870 | JUSTICE SOTOMAYOR | statute | Because, if they have an interest, they have a public interest that, by statute, is being directed. |
| 0:57:26.170 | 3446.170 | JUSTICE SOTOMAYOR | river | I mean, there are 26 rivers designated as wild and scenic rivers here. |
| 0:57:56.330 | 3476.330 | JUSTICE SOTOMAYOR | navigable | If you don't have title, does this -- at least with respect to navigable waters, do you have any claim whatsoever? |
| 0:57:56.970 | 3476.970 | JUSTICE SOTOMAYOR | waters | If you don't have title, does this -- at least with respect to navigable waters, do you have any claim whatsoever? |
| 0:58:03.610 | 3483.610 | MR. FINDLEY | waters | What matters here is that the United States does not have title to those waters and does not have title to the submerged lands. |
| 0:58:08.570 | 3488.570 | MR. FINDLEY | public lands | Once that's the case, they aren't public lands. |
| 0:58:11.690 | 3491.690 | MR. FINDLEY | park | And the Park Service may not use its Organic Act authority to reach out and regulate them. |
| 0:58:16.470 | 3496.470 | MR. FINDLEY | park | You asked the Park Service early on a very foundational question: What does 103(c) prohibit in your view? |
| 0:58:26.190 | 3506.190 | MR. FINDLEY | park | And 20 minutes later there was no answer from the Park Service. |
| 0:58:33.730 | 3513.730 | MR. FINDLEY | public lands | The reality is, in their view, any time they feel it is necessary or appropriate to regulate outside the boundaries of public lands, they feel they can do that. |
| 0:58:39.350 | 3519.350 | MR. FINDLEY | section | Now they feel, well, we haven't done it that often, but this is exactly what Section 103(c) was designed to prevent. |
| 0:59:06.850 | 3546.850 | MR. FINDLEY | regulation | All of that is exterritorial regulation. |
| 0:59:08.110 | 3548.110 | MR. FINDLEY | section | That is what Section 103(c) was specifically designed to prevent, so every time the Park Service wanted to promulgate a regulation to reach out to non-public land that is not part of the unit, the State of Alaska, a native corporation, or a private party did not have to go petition the court and say: Please don't do this. |
| 0:59:12.770 | 3552.770 | MR. FINDLEY | park | That is what Section 103(c) was specifically designed to prevent, so every time the Park Service wanted to promulgate a regulation to reach out to non-public land that is not part of the unit, the State of Alaska, a native corporation, or a private party did not have to go petition the court and say: Please don't do this. |
| 0:59:14.210 | 3554.210 | MR. FINDLEY | regulation | That is what Section 103(c) was specifically designed to prevent, so every time the Park Service wanted to promulgate a regulation to reach out to non-public land that is not part of the unit, the State of Alaska, a native corporation, or a private party did not have to go petition the court and say: Please don't do this. |
| 0:59:18.890 | 3558.890 | MR. FINDLEY | Alaska | That is what Section 103(c) was specifically designed to prevent, so every time the Park Service wanted to promulgate a regulation to reach out to non-public land that is not part of the unit, the State of Alaska, a native corporation, or a private party did not have to go petition the court and say: Please don't do this. |
| 0:59:26.870 | 3566.870 | MR. FINDLEY | ANILCA | That was the central deal of ANILCA. |
| 0:59:28.090 | 3568.090 | MR. FINDLEY | waters | And the waters were as crucial to that as a native corporation land and the other inholdings. |
| 0:59:36.130 | 3576.130 | MR. FINDLEY | Alaska | As my friend from the state made very clear, and for the State of Alaska, the rivers are the roads. |
| 0:59:36.930 | 3576.930 | MR. FINDLEY | river | As my friend from the state made very clear, and for the State of Alaska, the rivers are the roads. |
| 0:59:40.590 | 3580.590 | MR. FINDLEY | river | And while the Act constantly references rivers and waters, you need to give effect to both dual balancing that Congress was doing. |
| 0:59:41.330 | 3581.330 | MR. FINDLEY | waters | And while the Act constantly references rivers and waters, you need to give effect to both dual balancing that Congress was doing. |
| 0:59:52.530 | 3592.530 | MR. FINDLEY | waters | By adding over 100 million acres of land, public land to these units, you are achieving significant protection of the waters, and you're also protecting all waters where the -- where the state does not own the submerged lands. |
| 0:59:57.570 | 3597.570 | MR. FINDLEY | regulation | So regulation of those public lands, indeed, protects the waters. |
| 0:59:58.450 | 3598.450 | MR. FINDLEY | public lands | So regulation of those public lands, indeed, protects the waters. |
| 1:00:00.090 | 3600.090 | MR. FINDLEY | waters | So regulation of those public lands, indeed, protects the waters. |
| 1:00:06.110 | 3606.110 | MR. FINDLEY | river | What we are talking about here is the state's authority to retain primary control over the use of its rivers that run by the parks and are surrounded by the parks. |
| 1:00:07.710 | 3607.710 | MR. FINDLEY | park | What we are talking about here is the state's authority to retain primary control over the use of its rivers that run by the parks and are surrounded by the parks. |
| 1:00:12.050 | 3612.050 | MR. FINDLEY | river | The federal government, of course, retains control of the rivers. |
| 1:00:15.930 | 3615.930 | MR. FINDLEY | regulation | As we've talked about, the Clean Air Act applies, Coast Guard regulations apply, federal criminal law applies. |
| 1:00:18.930 | 3618.930 | MR. FINDLEY | river | These rivers are already significantly protected. |
| 1:00:21.290 | 3621.290 | MR. FINDLEY | hovercraft | I mean, the hovercraft rule, to come back to what brought us here today, why is that rule there? |
| 1:00:27.830 | 3627.830 | MR. FINDLEY | river | It's not there to protect the quality of the river. |
| 1:00:31.090 | 3631.090 | MR. FINDLEY | park | It's there because of sound and it's there because the Park Service wants to restrict access to remote areas of the parks, while the State of Alaska has a very different view about access to the remote areas of the state. |
| 1:00:35.530 | 3635.530 | MR. FINDLEY | Alaska | It's there because of sound and it's there because the Park Service wants to restrict access to remote areas of the parks, while the State of Alaska has a very different view about access to the remote areas of the state. |
| 1:00:41.250 | 3641.250 | MR. FINDLEY | ANILCA | And that's a judgment call that ANILCA should leave to the State of Alaska. |
| 1:00:42.690 | 3642.690 | MR. FINDLEY | Alaska | And that's a judgment call that ANILCA should leave to the State of Alaska. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.140 to 0:03:07.140, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.140] MR. FINDLEY: Thank you. Mr. Chief Justice, and may it please the Court: Mr. Sturgeon is asking that this Court restore the balance that -- that Congress struck when enacting ANILCA. ANILCA is unique and represents a series of bargains and compromises. A centerpiece of this balancing was ensuring that the over 18 million acres of non-public lands and waters about to be surrounded by the new ANILCA parks and preserves would not be subject to a new array of federal regulation. Section 103(c) of the statute preserved the status of these non-public lands and waters by excluding them from ANILCA's parks and preserves and specifically exempting them from park management regulation.

[0:00:50.360] JUSTICE SOTOMAYOR: I'm sorry, but ANILCA in many places puts statutory duties on the government, on the Park Service. So, for example, the statute expands the Glacier Bay National Monument. It says that the monument shall be managed for the following purposes among others, to protect a segment of the Alsek River fish and wildlife habitats and migration routes and a portion of the Fairweather Range. Or take another example. ANILCA creates the Kobuk Valley National Park, which it says shall be managed for the following purposes: among others, to keep it in an undeveloped state. So the agency has a statutory duty -- duty to manage these parks for the purpose of maintaining the Kobuk River, the Alsek River, and other rivers. If the Park Service can't do what you say, any regulation on these rivers, how can the Secretary fulfill the statutory duties and -- under ANILCA, unless it's under its organic powers?

[0:02:07.120] MR. FINDLEY: ANILCA, as this Court recognized in the first decision, specifically invoked the Organic Act and said these parks shall be managed in accord with the Organic Act and in accord with the provisions of ANILCA. And this Court recognized that ANILCA carries many provisions specifically modifying the Park Service's Organic Act authority, Section 103(c) being one of them. To your question, how can the Park Service fulfill its duties: In understanding ANILCA it's understanding the debate about ANILCA, it was very important what land went into conservation system units, but it was equally important what land did not get included within conservation system units. ANILCA was not just a park enabling statute. As this Court recognized in Amoco when it was -- first addressed ANILCA, it was resolving multiple land use disputes within Alaska.

[0:02:52.040] JUSTICE SOTOMAYOR: You haven't answered my question. Under your theory, the state manages all navigable waters between federal lands or between state lands. And I mean not waters but lands --

[0:03:05.240] MR. FINDLEY: Yes.

[0:03:05.240] JUSTICE SOTOMAYOR: -- in terms of the territorial

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 26, 2019.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2018/17-949
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2018/17-949/17-949_20190326-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:57.822 (297.822 s)
- Words: 664, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 1 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: "chapters" 138.060-141.560.
- Cross-check: Oyez's unofficial transcript agrees with 636 of Whisper's 664 words (95.8%; Oyez has 672).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:01.700 | 0:00:08.080 | 14 |
| JUSTICE KAGAN | 0:00:08.840 | 0:04:56.540 | 642 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:01.700 to 0:03:01.700, with each speaker's start time.

[0:00:01.700] CHIEF JUSTICE ROBERTS: In Case 17-949, Sturgeon v. Frost, Justice Kagan has the opinion of the Court.

[0:00:08.840] JUSTICE KAGAN: The Alaska National Interest Lands Conservation Act, called ANILCA for short, set aside more than 100 million acres of federally owned land in Alaska for preservation. With that land, Congress created ten new national parks. But in drawing the boundaries of those new parks, Congress made an unusual choice. Instead of enclosing only lands the Federal Government owns, Congress decided to track Alaska's natural terrain. The result was to sweep into the parks more than 18 million acres of land owned by the State, Native tribes, or private parties. And similarly, waters that the Federal Government doesn't own also wound up within the boundaries of the new parks. This case is mainly about the Park Service's authority to regulate those non-federally owned lands and waters. The case was brought by an Alaskan named John Sturgeon, who likes to hunt moose. To reach his favorite hunting ground, he used to travel by hovercraft over a stretch of the Nation River that flows through the Yukon-Charlie Preserve, one of the new parks ANILCA created. But one fateful day, park rangers stopped Sturgeon and told him that operating a hovercraft within a national park violates a Park Service regulation, which indeed it does. Sturgeon responded by bringing this lawsuit, arguing that the Park Service can't enforce that regulation on the part of the Nation River in the Yukon-Charlie. The suit has a complicated history. In fact, this is the second time it's reached this Court. But now we finally resolve it for good by saying that Sturgeon can take his hovercraft out of storage. The first question we consider is whether the Nation River counts as public land under ANILCA. The phrase public land is a defined term in the chapters and interests that the Federal Government owns. If the Nation River were public land, everyone agrees the Park Service could regulate it. After all, it would be the Federal Government's own property. But for various reasons, we reject the Government's argument that it holds a property interest in the Nation River. That brings us to the question whether the Park Service can regulate non-federally owned lands and waters within Alaskan National Parks. If the Park Service has that kind of regulatory authority, then it can enforce its rule against hovercrafts on the Nation River. But if the Park Service's

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:23.880 | ten | 10 |
| 0:01:22.660 | -Charlie | Charley |
| 0:01:51.260 | -Charlie. The | Charley. This |
| 0:02:18.060 | chapters | Statute that basically means old lands, waters |
| 0:02:26.540 | (nothing) | a |
| 0:02:32.760 | own | owned |
| 0:03:22.500 | won't | would not |
| 0:03:25.980 | I'll | I will |
| 0:03:40.860 | didn't | did not |
| 0:03:55.480 | weren't | were not |
| 0:03:58.160 | aren't | are not |
| 0:03:59.800 | can't | cannot |
| 0:04:03.300 | Justice | just as |
| 0:04:10.980 | it on non -federally | at a non-federally |
| 0:04:16.040 | recognize | have recognized |
