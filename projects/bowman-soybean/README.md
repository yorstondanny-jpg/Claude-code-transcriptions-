# bowman-soybean: Supreme Court No. 11-796

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2012/11-796
- Audio: https://www.supremecourt.gov/media/audio/mp3files/11-796.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2012/11-796-1j43.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 47 min on 4 CPU cores
- Audio length: 1:09:34.942 (4174.942 s)
- `audio/argument.mp3`: mono, 64 kbps, 33.4 MB
- Official words: 11278 (plus 11 `(Laughter.)` markers), in 222 speaker turns
- ASR words: 11122
- Official words matched to an ASR word: 10723 of 11278 (**95.08%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.08% (threshold 85%).

217 words are shorter than 20 ms. These are official words the ASR didn't produce,
mostly repeats, false starts and cross-talk ("the -- the --", "I -- I think"), squeezed into the
small gap between the ASR words either side. Their order is right; their exact times are not.

## Files

- `audio/argument.mp3`: the argument audio.
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
cluster if it ends at the word's end, and is left alone otherwise. This trimmed 21 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 11-796 2012 bowman-soybean --model medium.en --opinion --mentions "soybean(s),seed(s),generation(s),children,edamame,science project,grain elevator,Roundup,farmer,Bowman,eBay,bank,vaccine"

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-45.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:05:09.920 | 309.920 | small | 1.00 | 0.05 | 7.3 | 18.6 | those seeds for anything else he wants to do. It has nothing to do with those seeds. There are three generations of seeds. Maybe three generations of seeds is enough. |
| 2 | 0:05:27.020 | 327.020 | small | 0.82 | 0.25 | 25.7 | 35.9 | have the Monsanto, the first generation they sold. They have children, which is the second generation. And those children have children, which is the third generation, okay? So bad joke. |
| 3 | 0:30:25.352 | 1825.352 | under speech | 0.00 | 0.00 | - | - | business they would have to comply with seed labeling laws. They do not do so because it's not their business model. That's why it's so cheap. And that's why farmers -- |
| 4 | 0:34:12.060 | 2052.060 | big | 2.74 | 2.10 | 23.9 | 35.2 | make a dozen other copies to give to my friends or sell on eBay. It's a reasonable use, but it's an infringing one. Well, we haven't had that case either. |
| 5 | 0:42:42.060 | 2562.060 | under speech | 0.00 | 0.00 | - | - | a gun. I think you may be able to shoot several -- I don't know whether you can shoot a whole round or whatever. But in any event, it's one event. |
| 6 | 0:42:44.260 | 2564.260 | medium | 1.02 | 0.40 | 12.5 | 15.9 | shoot several -- I don't know whether you can shoot a whole round or whatever. But in any event, it's one event. You can't rob a bank with it, though, right? |
| 7 | 0:45:16.400 | 2716.400 | small | 0.54 | 0.25 | 15.4 | 19.8 | who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 8 | 0:45:44.920 | 2744.920 | under speech | 0.18 | 0.00 | - | - | three points, starting with the edamame and moving up to inadvertent infringers. Edamame is an immature form of the soybean seed. You can plant edamame -- Okay. I'll change the hypothetical. |
| 9 | 0:45:58.020 | 2758.020 | under speech | 0.00 | 0.00 | - | - | my Girl Scout troop and have them do a science experiment, it will rot, but it will not generate. And that -- And I thought I was being so clever, too. |
| 10 | 0:58:22.100 | 3502.100 | under speech | 0.16 | 0.05 | 20.1 | 20.1 | Okay. Vaccines are live. They have live cultures; they can regenerate themselves. If a company develops the vaccine for, you know, H1 -- I shouldn't be using -- an important life-saving vaccine -- |
| 11 | 0:59:07.940 | 3547.940 | small | 1.14 | 0.35 | 13.8 | 23.7 | take vials of their blood and keep selling it? Is that your -- Yes, and keep -- well, keep replicating it in competition. Take another example -- Well, is that how it works? |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| soybean(s) | 37 | 47 |
| seed(s) | 139 | 186 |
| generation(s) | 44 | 56 |
| children | 2 | 3 |
| edamame | 5 | 5 |
| science project | 1 | 1 |
| grain elevator | 33 | 40 |
| Roundup | 25 | 30 |
| farmer | 53 | 58 |
| Bowman | 18 | 18 |
| eBay | 1 | 1 |
| bank | 3 | 3 |
| vaccine | 9 | 11 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:05.840 | 5.840 | CHIEF JUSTICE ROBERTS | Bowman | We will hear argument next this morning in case 11-796, Bowman v. Monsanto Company. |
| 0:00:31.020 | 31.020 | MR. WALTERS | seed(s) | The invention is a bit of DNA that, when inserted into a soy bean seed, makes that seed and all the plants that grow from that seed resistant to the active ingredient in Roundup. |
| 0:00:37.800 | 37.800 | MR. WALTERS | Roundup | The invention is a bit of DNA that, when inserted into a soy bean seed, makes that seed and all the plants that grow from that seed resistant to the active ingredient in Roundup. |
| 0:00:43.380 | 43.380 | MR. WALTERS | seed(s) | Now, the only way to practice that invention is to plant the seed and to grow more seeds. |
| 0:00:50.600 | 50.600 | CHIEF JUSTICE ROBERTS | seed(s) | Why in the world would anybody spend any money to try to improve the seed if as soon as they sold the first one anybody could grow more and have as many of those seeds as they want? |
| 0:01:41.560 | 101.560 | MR. WALTERS | farmer | Under Respondent's theory, any farmer who grows a soy bean seed is infringing the patent, but for the grace of Monsanto. |
| 0:01:43.140 | 103.140 | MR. WALTERS | seed(s) | Under Respondent's theory, any farmer who grows a soy bean seed is infringing the patent, but for the grace of Monsanto. |
| 0:01:48.260 | 108.260 | MR. WALTERS | farmer | And that's -- a lot of farmers in this country, when we have over 90 percent of the acreage that is Roundup Ready. |
| 0:01:51.940 | 111.940 | MR. WALTERS | Roundup | And that's -- a lot of farmers in this country, when we have over 90 percent of the acreage that is Roundup Ready. |
| 0:01:59.720 | 119.720 | JUSTICE SCALIA | farmer | Any farmer who plants and grows soybeans is violating the patent? |
| 0:02:02.920 | 122.920 | JUSTICE SCALIA | soybean(s) | Any farmer who plants and grows soybeans is violating the patent? |
| 0:02:17.740 | 137.740 | JUSTICE SCALIA | seed(s) | I thought that their claim is that he only violates the patent if he tries to grow additional seeds from his first crop. |
| 0:02:25.540 | 145.540 | MR. WALTERS | seed(s) | The reach of Monsanto's theory is that once that seed is sold, even though title has passed to the farmer, and the farmer assumes all risks associated with farming, that they can still control the ownership of that seed, control how that seed is used. |
| 0:02:28.500 | 148.500 | MR. WALTERS | farmer | The reach of Monsanto's theory is that once that seed is sold, even though title has passed to the farmer, and the farmer assumes all risks associated with farming, that they can still control the ownership of that seed, control how that seed is used. |
| 0:02:39.440 | 159.440 | JUSTICE SCALIA | seed(s) | No, not that seed. |
| 0:02:40.940 | 160.940 | JUSTICE SCALIA | seed(s) | It's different seed. |
| 0:02:42.240 | 162.240 | JUSTICE SCALIA | seed(s) | That seed is done. |
| 0:02:45.920 | 165.920 | JUSTICE SCALIA | seed(s) | It's been planted in the ground and has grown other seed. |
| 0:02:47.600 | 167.600 | JUSTICE SCALIA | seed(s) | It's the other seed we are talking about. |
| 0:02:50.300 | 170.300 | JUSTICE SCALIA | seed(s) | It's not the very seed that was sold. |
| 0:03:00.240 | 180.240 | MR. WALTERS | seed(s) | That's correct, Your Honor, but if we don't apply -- if exhaustion is eliminated, rather, for the progeny seed, then you are taking away the ability of people to exchange these goods freely in commerce. |
| 0:03:10.780 | 190.780 | MR. WALTERS | grain elevator | You have essentially a servitude on these things that are exchanged, and every grain elevator who makes a sale is infringing. |
| 0:03:34.620 | 214.620 | JUSTICE KENNEDY | seed(s) | But Monsanto can still prevail if you say that there's a patent infringement, if he plants it for seed and uses the seed to replant. |
| 0:03:53.600 | 233.600 | MR. WALTERS | seed(s) | If you assume that there is exhaustion in the seeds that are sold to the farmer -- let's take our particular case here. |
| 0:03:55.280 | 235.280 | MR. WALTERS | farmer | If you assume that there is exhaustion in the seeds that are sold to the farmer -- let's take our particular case here. |
| 0:03:58.280 | 238.280 | MR. WALTERS | Bowman | Mr. Bowman went to a grain elevator and he bought from the grain elevator without restriction seeds to – and it was his purpose to plant them. |
| 0:03:59.160 | 239.160 | MR. WALTERS | grain elevator | Mr. Bowman went to a grain elevator and he bought from the grain elevator without restriction seeds to – and it was his purpose to plant them. |
| 0:04:03.220 | 243.220 | MR. WALTERS | seed(s) | Mr. Bowman went to a grain elevator and he bought from the grain elevator without restriction seeds to – and it was his purpose to plant them. |
| 0:04:11.420 | 251.420 | MR. WALTERS | seed(s) | Now, the only way that he can make use –- if you assume in the first instance that there is exhaustion to the seeds that Mr. Bowman purchased from the grain elevator, you are taking away any ability for him to use that seed or use the invention. |
| 0:04:12.200 | 252.200 | MR. WALTERS | Bowman | Now, the only way that he can make use –- if you assume in the first instance that there is exhaustion to the seeds that Mr. Bowman purchased from the grain elevator, you are taking away any ability for him to use that seed or use the invention. |
| 0:04:13.120 | 253.120 | MR. WALTERS | grain elevator | Now, the only way that he can make use –- if you assume in the first instance that there is exhaustion to the seeds that Mr. Bowman purchased from the grain elevator, you are taking away any ability for him to use that seed or use the invention. |
| 0:04:30.940 | 270.940 | MR. WALTERS | seed(s) | It has two elements; the first element is planting the crop seed and it's a particular crop seed with all the particular genetics that encode for resistance to Roundup, and then the next step is to apply to the crop and weeds in the field a sufficient amount of glyphosate herbicide. |
| 0:04:37.540 | 277.540 | MR. WALTERS | Roundup | It has two elements; the first element is planting the crop seed and it's a particular crop seed with all the particular genetics that encode for resistance to Roundup, and then the next step is to apply to the crop and weeds in the field a sufficient amount of glyphosate herbicide. |
| 0:04:49.260 | 289.260 | MR. WALTERS | seed(s) | Now, if you say that there is exhaustion in the seeds that Mr. Bowman purchased from the grain elevator, but you say it doesn't apply to the progeny, you are not allowing him to actually practice the invention to grow more seeds. |
| 0:04:50.140 | 290.140 | MR. WALTERS | Bowman | Now, if you say that there is exhaustion in the seeds that Mr. Bowman purchased from the grain elevator, but you say it doesn't apply to the progeny, you are not allowing him to actually practice the invention to grow more seeds. |
| 0:04:51.060 | 291.060 | MR. WALTERS | grain elevator | Now, if you say that there is exhaustion in the seeds that Mr. Bowman purchased from the grain elevator, but you say it doesn't apply to the progeny, you are not allowing him to actually practice the invention to grow more seeds. |
| 0:05:00.260 | 300.260 | JUSTICE BREYER | seed(s) | No, but you are allowing him to use those seeds for anything else he wants to do. |
| 0:05:04.660 | 304.660 | JUSTICE BREYER | seed(s) | It has nothing to do with those seeds. |
| 0:05:05.820 | 305.820 | JUSTICE BREYER | generation(s) | There are three generations of seeds. |
| 0:05:06.720 | 306.720 | JUSTICE BREYER | seed(s) | There are three generations of seeds. |
| 0:05:08.220 | 308.220 | JUSTICE BREYER | generation(s) | Maybe three generations of seeds is enough. |
| 0:05:09.120 | 309.120 | JUSTICE BREYER | seed(s) | Maybe three generations of seeds is enough. |
| 0:05:16.040 | 316.040 | JUSTICE BREYER | generation(s) | First of you have the Monsanto, the first generation they sold. |
| 0:05:18.900 | 318.900 | JUSTICE BREYER | children | They have children, which is the second generation. |
| 0:05:20.440 | 320.440 | JUSTICE BREYER | generation(s) | They have children, which is the second generation. |
| 0:05:22.020 | 322.020 | JUSTICE BREYER | children | And those children have children, which is the third generation, okay? |
| 0:05:23.660 | 323.660 | JUSTICE BREYER | generation(s) | And those children have children, which is the third generation, okay? |
| 0:05:33.720 | 333.720 | JUSTICE BREYER | generation(s) | So we are talking here -- he can do what he wants with the first generation. |
| 0:05:40.960 | 340.960 | JUSTICE BREYER | seed(s) | And moreover, when he buys them from Monsanto, he can make new seeds. |
| 0:05:42.060 | 342.060 | JUSTICE BREYER | generation(s) | He can make generation 2 because they've licensed him to do it. |
| 0:05:46.500 | 346.500 | JUSTICE BREYER | generation(s) | Here, he buys generation 2. |
| 0:05:51.040 | 351.040 | JUSTICE BREYER | seed(s) | Now, he can do what he wants with those seeds. |
| 0:05:58.660 | 358.660 | JUSTICE BREYER | generation(s) | But I'll tell you, there is a problem because the coming about of the third generation is itself the infringement. |
| 0:06:03.100 | 363.100 | JUSTICE BREYER | generation(s) | So the second generation seeds have nothing to do with it. |
| 0:06:03.600 | 363.600 | JUSTICE BREYER | seed(s) | So the second generation seeds have nothing to do with it. |
| 0:06:17.400 | 377.400 | JUSTICE BREYER | generation(s) | If he went into a room and had a box that he bought from a lab and he put rocks in it and he said, hocus-pocus and lo and behold out came the third generation of seeds, he would have infringed Monsanto's patent with that third generation, would he not? |
| 0:06:18.320 | 378.320 | JUSTICE BREYER | seed(s) | If he went into a room and had a box that he bought from a lab and he put rocks in it and he said, hocus-pocus and lo and behold out came the third generation of seeds, he would have infringed Monsanto's patent with that third generation, would he not? |
| 0:06:32.240 | 392.240 | JUSTICE BREYER | seed(s) | You mean if he goes and finds a new way of making these seeds, which happens to do with you pick some grass and you intertwine it and various things like that, and lo and behold you have a perfect copy of Monsanto's patented seed, he hasn't made it, he hasn't infringed? |
| 0:07:08.420 | 428.420 | JUSTICE BREYER | generation(s) | I am saying the problem for you here, I think, is that, infringement lies in the fact that he made generation three. |
| 0:07:12.280 | 432.280 | JUSTICE BREYER | generation(s) | It has nothing to do with generation 2. |
| 0:07:19.000 | 439.000 | JUSTICE BREYER | seed(s) | But that is, in fact, the way he made these seeds. |
| 0:07:21.560 | 441.560 | JUSTICE BREYER | generation(s) | But he can sell, resell generation 2, he can do whatever he wants with it. |
| 0:07:32.320 | 452.320 | JUSTICE BREYER | generation(s) | The only thing he cannot do is he cannot create generation 3, just as he couldn't use generation 2 seeds to rob a bank. |
| 0:07:35.740 | 455.740 | JUSTICE BREYER | seed(s) | The only thing he cannot do is he cannot create generation 3, just as he couldn't use generation 2 seeds to rob a bank. |
| 0:07:36.800 | 456.800 | JUSTICE BREYER | bank | The only thing he cannot do is he cannot create generation 3, just as he couldn't use generation 2 seeds to rob a bank. |
| 0:07:50.260 | 470.260 | JUSTICE BREYER | generation(s) | So it's generation 3 that concerns us. |
| 0:08:09.280 | 489.280 | MR. WALTERS | seed(s) | Justice Breyer, my response is, if you applied the law that way to side making over use, you are eliminating the Exhaustion Doctrine in the context of -- of patented seeds. |
| 0:08:22.680 | 502.680 | JUSTICE GINSBURG | seed(s) | You can use the seed to make new seeds. |
| 0:08:50.060 | 530.060 | MR. WALTERS | seed(s) | If you look at claim 130 again, for example, you are saying he can't practice claim 130, which is certainly embodied in the seeds he purchased from the grain elevator. |
| 0:08:51.200 | 531.200 | MR. WALTERS | grain elevator | If you look at claim 130 again, for example, you are saying he can't practice claim 130, which is certainly embodied in the seeds he purchased from the grain elevator. |
| 0:08:56.620 | 536.620 | JUSTICE GINSBURG | seed(s) | Well, suppose he -- he had never bought any Monsanto seeds. |
| 0:08:59.380 | 539.380 | JUSTICE GINSBURG | grain elevator | He just goes to the grain elevator and 90-odd percent of those seeds have the genetic composition. |
| 0:09:03.740 | 543.740 | JUSTICE GINSBURG | seed(s) | He just goes to the grain elevator and 90-odd percent of those seeds have the genetic composition. |
| 0:09:20.060 | 560.060 | JUSTICE GINSBURG | seed(s) | So he never has to buy any seed, at all, from Monsanto. |
| 0:09:26.020 | 566.020 | MR. WALTERS | seed(s) | Well, in practical matters it doesn't work that way because the seed that's available at a grain elevator is not a very good source of seed and farmers are not going to be able to eliminate the need to go to Monsanto or the other seed companies every year by going to the grain elevator. |
| 0:09:27.440 | 567.440 | MR. WALTERS | grain elevator | Well, in practical matters it doesn't work that way because the seed that's available at a grain elevator is not a very good source of seed and farmers are not going to be able to eliminate the need to go to Monsanto or the other seed companies every year by going to the grain elevator. |
| 0:09:30.900 | 570.900 | MR. WALTERS | farmer | Well, in practical matters it doesn't work that way because the seed that's available at a grain elevator is not a very good source of seed and farmers are not going to be able to eliminate the need to go to Monsanto or the other seed companies every year by going to the grain elevator. |
| 0:09:45.500 | 585.500 | MR. WALTERS | grain elevator | Great evidence of that is the fact that my client, every year that he planted a second crop using the grain elevator seed, he bought high quality seed from Pioneer. |
| 0:09:45.980 | 585.980 | MR. WALTERS | seed(s) | Great evidence of that is the fact that my client, every year that he planted a second crop using the grain elevator seed, he bought high quality seed from Pioneer. |
| 0:09:49.240 | 589.240 | MR. WALTERS | grain elevator | Now, if this grain elevator -- grain elevator seed was so good, why didn't he use it for his first crop? |
| 0:09:49.720 | 589.720 | MR. WALTERS | seed(s) | Now, if this grain elevator -- grain elevator seed was so good, why didn't he use it for his first crop? |
| 0:10:00.080 | 600.080 | JUSTICE BREYER | generation(s) | Now, when you buy generation 2, well, there are a lot of things you can do with it. |
| 0:10:21.600 | 621.600 | JUSTICE BREYER | seed(s) | One, you can't pick up those seeds that you've just bought and throw them in a child's face. |
| 0:10:46.200 | 646.200 | JUSTICE BREYER | generation(s) | And that law you have violated when you use it to make generation 3, just as you have violated the law against assault were you to use it to commit an assault. |
| 0:11:58.160 | 718.160 | JUSTICE SOTOMAYOR | seed(s) | So that's what I think Justice Breyer is saying, which is you can use the seed, you can plant it, but what you can't do is use its progeny unless you are licensed to because its progeny is a new item. |
| 0:13:27.880 | 807.880 | JUSTICE GINSBURG | seed(s) | We've been dealing with an item with the Exhaustion Doctrine and now we have hundreds of items, thousands of items, all growing from that original seed. |
| 0:14:38.520 | 878.520 | MR. WALTERS | farmer | And farmers, when they plant seeds, they don't exercise any control or dominion over -- over their crop. |
| 0:14:39.700 | 879.700 | MR. WALTERS | seed(s) | And farmers, when they plant seeds, they don't exercise any control or dominion over -- over their crop. |
| 0:14:59.700 | 899.700 | JUSTICE SOTOMAYOR | seed(s) | -- in growing the seed? |
| 0:15:17.160 | 917.160 | MR. WALTERS | farmer | You ask any farmer who's lived through a drought or through a terrible flood and they will say they're not the ones who are making these -- |
| 0:15:25.840 | 925.840 | CHIEF JUSTICE ROBERTS | seed(s) | Well, you only need one -- I mean, you throw the seeds on the ground, one or two of them are going to grow and you still have the same case, right? |
| 0:15:35.980 | 935.980 | MR. WALTERS | seed(s) | It doesn't matter how you come into possession with these seeds. |
| 0:15:50.660 | 950.660 | JUSTICE BREYER | generation(s) | I thought you were going to respond to me that my question then makes it infringement when your client buys generation 1 from Monsanto because they buy generation 1 from Monsanto, they plant it in the ground and lo and behold up comes generation 2. |
| 0:16:02.180 | 962.180 | JUSTICE BREYER | generation(s) | And generation 2, on the basis of what I was asking you, is just as much a violation. |
| 0:16:27.640 | 987.640 | JUSTICE BREYER | generation(s) | When you create a new generation, you have made a patented item, which you cannot do without the approval of the patent owner. |
| 0:16:39.260 | 999.260 | JUSTICE BREYER | generation(s) | Therefore, Monsanto gives that approval when you buy generation 1. |
| 0:16:54.140 | 1014.140 | MR. WALTERS | farmer | What Monsanto wants to do in your scenario is they want the farmer to assume all the risks of farming. |
| 0:17:04.840 | 1024.840 | MR. WALTERS | farmer | They want -- but they still want to control and act as owners of the property that is owned, no doubt, by that farmer. |
| 0:17:05.800 | 1025.800 | MR. WALTERS | farmer | When that farmer grows the progeny seed, that they insure the risk that they're not going to have a crop in the first place. |
| 0:17:06.960 | 1026.960 | MR. WALTERS | seed(s) | When that farmer grows the progeny seed, that they insure the risk that they're not going to have a crop in the first place. |
| 0:17:20.560 | 1040.560 | MR. WALTERS | farmer | If they drive to the grain dealer to sell their harvest -- they get one paycheck a year, by the way -- they, if they get into a wreck, that's not Monsanto's problem; that's the farmer's problem. |
| 0:17:24.720 | 1044.720 | MR. WALTERS | farmer | So what they're essentially asking for is for the farmers to bear all the risks of farming, yet they can sit back and control how that property is used. |
| 0:17:40.960 | 1060.960 | MR. WALTERS | farmer | The thing that's very important is this is not a license, this is an outright sale to the farmers of the first generation. |
| 0:17:41.820 | 1061.820 | MR. WALTERS | generation(s) | The thing that's very important is this is not a license, this is an outright sale to the farmers of the first generation. |
| 0:17:45.980 | 1065.980 | MR. WALTERS | seed(s) | And then they are -- they plant those seeds because they have, under the Exhaustion Doctrine, a right to use the invention, and then those progeny seeds are owned outright by every farmer, and they assume all risk of loss. |
| 0:17:53.360 | 1073.360 | MR. WALTERS | farmer | And then they are -- they plant those seeds because they have, under the Exhaustion Doctrine, a right to use the invention, and then those progeny seeds are owned outright by every farmer, and they assume all risk of loss. |
| 0:18:04.520 | 1084.520 | JUSTICE GINSBURG | seed(s) | They may -- the seeds are owned by the farmer. |
| 0:18:07.100 | 1087.100 | JUSTICE GINSBURG | farmer | They may -- the seeds are owned by the farmer. |
| 0:18:11.120 | 1091.120 | JUSTICE GINSBURG | seed(s) | But when he uses them to grow more seeds, he's infringing on that patent. |
| 0:18:20.820 | 1100.820 | MR. WALTERS | grain elevator | And those things get sold to the grain elevators, and now every time the grain elevator makes a sale, it's technically infringing. |
| 0:18:34.480 | 1114.480 | MR. WALTERS | farmer | And one of the main problems is that you have farmers, their main livelihood here is to sell the seeds that they grow. |
| 0:18:37.060 | 1117.060 | MR. WALTERS | seed(s) | And one of the main problems is that you have farmers, their main livelihood here is to sell the seeds that they grow. |
| 0:18:54.220 | 1134.220 | JUSTICE KENNEDY | seed(s) | With some crops if you are going to make seeds, you leave the crop in longer. |
| 0:18:59.640 | 1139.640 | JUSTICE KENNEDY | soybean(s) | In -- what about soybeans? |
| 0:19:00.600 | 1140.600 | JUSTICE KENNEDY | farmer | If the farmer has the north 40 and the south 40, the north 40, he's going to plants soybeans to be used for flour, human consumption, and south 40, he wants seeds. |
| 0:19:04.340 | 1144.340 | JUSTICE KENNEDY | soybean(s) | If the farmer has the north 40 and the south 40, the north 40, he's going to plants soybeans to be used for flour, human consumption, and south 40, he wants seeds. |
| 0:19:08.600 | 1148.600 | JUSTICE KENNEDY | seed(s) | If the farmer has the north 40 and the south 40, the north 40, he's going to plants soybeans to be used for flour, human consumption, and south 40, he wants seeds. |
| 0:19:12.780 | 1152.780 | MR. WALTERS | farmer | You know, most farmers are not growing soybeans for -- for seed. |
| 0:19:14.420 | 1154.420 | MR. WALTERS | soybean(s) | You know, most farmers are not growing soybeans for -- for seed. |
| 0:19:17.000 | 1157.000 | MR. WALTERS | seed(s) | You know, most farmers are not growing soybeans for -- for seed. |
| 0:19:21.505 | 1161.505 | MR. WALTERS | farmer | -- various types of farmers who are -- who are growing foundation seed, for example, that is very close to the -- to the first generation seed that's engineered. |
| 0:19:24.740 | 1164.740 | MR. WALTERS | seed(s) | -- various types of farmers who are -- who are growing foundation seed, for example, that is very close to the -- to the first generation seed that's engineered. |
| 0:19:27.840 | 1167.840 | MR. WALTERS | generation(s) | -- various types of farmers who are -- who are growing foundation seed, for example, that is very close to the -- to the first generation seed that's engineered. |
| 0:19:31.420 | 1171.420 | JUSTICE SCALIA | soybean(s) | I thought soybeans are seeds. |
| 0:19:32.240 | 1172.240 | JUSTICE SCALIA | seed(s) | I thought soybeans are seeds. |
| 0:19:35.720 | 1175.720 | JUSTICE KENNEDY | soybean(s) | But that's -- if you're going to use the soybeans for seeds as opposed to flour, do you leave them in the ground any longer? |
| 0:19:36.520 | 1176.520 | JUSTICE KENNEDY | seed(s) | But that's -- if you're going to use the soybeans for seeds as opposed to flour, do you leave them in the ground any longer? |
| 0:20:08.340 | 1208.340 | JUSTICE KAGAN | seed(s) | Actually, it seems to me that that answer is peculiarly insufficient in this kind of a case because all that has to happen is that one seed escapes the web of these contracts, and that seed because it can self-replicate in the way that it can, essentially makes all the contracts worthless. |
| 0:20:31.540 | 1231.540 | MR. WALTERS | seed(s) | Taking our example here where -- where Petitioner bought commodity seeds, it's an undifferentiated mixture, it can't be overemphasized how different every single seed is, you don't know a Monsanto from a Pioneer from an Asgrow. |
| 0:20:43.540 | 1243.540 | MR. WALTERS | farmer | If I am a farmer, I need a particular maturity bean for my field because I don't want it to mature before it gets high enough for the combine to come around and cut it. |
| 0:20:59.280 | 1259.280 | MR. WALTERS | grain elevator | So if you go to the grain elevator and you don't know what exactly it is that you want and you just get a mixture, that's not going to be real -- competitive at all to Monsanto's first generation seed. |
| 0:21:07.760 | 1267.760 | MR. WALTERS | generation(s) | So if you go to the grain elevator and you don't know what exactly it is that you want and you just get a mixture, that's not going to be real -- competitive at all to Monsanto's first generation seed. |
| 0:21:08.180 | 1268.180 | MR. WALTERS | seed(s) | So if you go to the grain elevator and you don't know what exactly it is that you want and you just get a mixture, that's not going to be real -- competitive at all to Monsanto's first generation seed. |
| 0:21:17.680 | 1277.680 | MR. WALTERS | seed(s) | Now, the possibility of somebody selecting one and saying, ah, that's the exact one that I need for my field, I'm going to cultivate that and let it grow into enough seeds so I can plant my first crop, that would take a number of years to grow a 1,000-acre farm, and it's not -- and by that time, farmers -- the nature would have changed and evolved where you would want the latest in disease resistance by that point. |
| 0:21:27.620 | 1287.620 | MR. WALTERS | farmer | Now, the possibility of somebody selecting one and saying, ah, that's the exact one that I need for my field, I'm going to cultivate that and let it grow into enough seeds so I can plant my first crop, that would take a number of years to grow a 1,000-acre farm, and it's not -- and by that time, farmers -- the nature would have changed and evolved where you would want the latest in disease resistance by that point. |
| 0:21:37.980 | 1297.980 | JUSTICE KENNEDY | Bowman | I thought that's exactly what Bowman did here. |
| 0:21:40.780 | 1300.780 | JUSTICE KENNEDY | grain elevator | He went to a grain elevator and he -- he used the seeds, and -- and he didn't know exactly the percentage mix, but he used them. |
| 0:21:43.080 | 1303.080 | JUSTICE KENNEDY | seed(s) | He went to a grain elevator and he -- he used the seeds, and -- and he didn't know exactly the percentage mix, but he used them. |
| 0:22:00.940 | 1320.940 | MR. WALTERS | Roundup | He selected for the particular trait, Roundup Ready, but there are probably more than a dozen different ways in which the seed can vary -- disease resistance, maturity rates. |
| 0:22:05.620 | 1325.620 | MR. WALTERS | seed(s) | He selected for the particular trait, Roundup Ready, but there are probably more than a dozen different ways in which the seed can vary -- disease resistance, maturity rates. |
| 0:22:16.200 | 1336.200 | CHIEF JUSTICE ROBERTS | seed(s) | I thought what he did was plant all the commodity seeds, and then applied the Roundup, so that all that was left was the Roundup resistance seeds, and then he used those. |
| 0:22:18.500 | 1338.500 | CHIEF JUSTICE ROBERTS | Roundup | I thought what he did was plant all the commodity seeds, and then applied the Roundup, so that all that was left was the Roundup resistance seeds, and then he used those. |
| 0:22:26.520 | 1346.520 | MR. WALTERS | grain elevator | But if you look at a field that you plant with grain elevator seed, it's going to be all different color because they're going to be all different variety, they're all going to mature at a different rate. |
| 0:22:27.080 | 1347.080 | MR. WALTERS | seed(s) | But if you look at a field that you plant with grain elevator seed, it's going to be all different color because they're going to be all different variety, they're all going to mature at a different rate. |
| 0:22:41.060 | 1361.060 | JUSTICE SCALIA | seed(s) | Including the Monsanto seeds? |
| 0:22:42.500 | 1362.500 | MR. WALTERS | seed(s) | Including the Monsanto seeds. |
| 0:22:51.200 | 1371.200 | MR. WALTERS | seed(s) | This is a very poor choice -- choice of seed, but it only makes sense to plant in a risky situation, like when a farmer has been washed out from a flood, for example, and it's late in the -- |
| 0:22:56.200 | 1376.200 | MR. WALTERS | farmer | This is a very poor choice -- choice of seed, but it only makes sense to plant in a risky situation, like when a farmer has been washed out from a flood, for example, and it's late in the -- |
| 0:23:02.880 | 1382.880 | CHIEF JUSTICE ROBERTS | Roundup | No, no. I mean the very first time, you get nothing but Monsanto Ready -- Roundup Ready seeds and you plant those. |
| 0:23:03.580 | 1383.580 | CHIEF JUSTICE ROBERTS | seed(s) | No, no. I mean the very first time, you get nothing but Monsanto Ready -- Roundup Ready seeds and you plant those. |
| 0:23:12.240 | 1392.240 | CHIEF JUSTICE ROBERTS | seed(s) | So that doesn't make the commodity seeds any different? |
| 0:23:16.080 | 1396.080 | MR. WALTERS | seed(s) | The commodity seeds, with -- the Roundup Ready commodity seeds will all grow at different rates and have different disease resistance, different maturity rates. |
| 0:23:17.620 | 1397.620 | MR. WALTERS | Roundup | The commodity seeds, with -- the Roundup Ready commodity seeds will all grow at different rates and have different disease resistance, different maturity rates. |
| 0:23:41.920 | 1421.920 | MR. WALTERS | farmer | They are exactly what a farmer needs for their -- |
| 0:23:43.820 | 1423.820 | JUSTICE SCALIA | seed(s) | So all the Monsanto seeds are not -- are not fungible. |
| 0:23:54.000 | 1434.000 | MR. WALTERS | seed(s) | I mean, they allow these seeds to be dumped into the common grain elevator. |
| 0:23:56.900 | 1436.900 | MR. WALTERS | grain elevator | I mean, they allow these seeds to be dumped into the common grain elevator. |
| 0:24:05.020 | 1445.020 | MR. WALTERS | grain elevator | There were no restrictions on my client when he purchased them from the grain elevator. |
| 0:24:10.840 | 1450.840 | MR. WALTERS | grain elevator | So it's less of a problem for Monsanto for people going to the grain elevator to plant. |
| 0:24:18.820 | 1458.820 | MR. WALTERS | farmer | Nevertheless, it's -- it's an outright sale, an exhaustion applies to that particular sale, and permits that farmer to use it. |
| 0:24:24.720 | 1464.720 | MR. WALTERS | grain elevator | It's never going to be a threat to Monsanto's business -- people planting grain elevator seed. |
| 0:24:25.340 | 1465.340 | MR. WALTERS | seed(s) | It's never going to be a threat to Monsanto's business -- people planting grain elevator seed. |
| 0:24:51.520 | 1491.520 | MR. WALTERS | farmer | And then that's only fair because there, the agent growers are assuming -- well, Monsanto was assuming the risk that the farmers are. |
| 0:24:58.380 | 1498.380 | MR. WALTERS | farmer | And there is some equitability there with the -- the risk sharing between the farmers and Monsanto. |
| 0:25:00.520 | 1500.520 | MR. WALTERS | farmer | Now they want the farmers to take all the risks associated with farming, yet they want to control how they use those seeds all the way down the distribution chain. |
| 0:25:05.260 | 1505.260 | MR. WALTERS | seed(s) | Now they want the farmers to take all the risks associated with farming, yet they want to control how they use those seeds all the way down the distribution chain. |
| 0:26:20.220 | 1580.220 | MS. ARBUS SHERRY | seed(s) | And it said, most notably, there is no seed saving exemption in the Patent Act, there is no research exemption in the Patent Act. |
| 0:26:29.880 | 1589.880 | MS. ARBUS SHERRY | seed(s) | The consequence of Petitioner's argument would be that this Court would not only be reading a seed-saving exemption into the Patent Act, and a research exemption, it would be doing much, much, much more under the guise of patent exhaustion. |
| 0:27:19.220 | 1639.220 | CHIEF JUSTICE ROBERTS | seed(s) | We have never applied the Reinvention Doctrine to articles that reinvent themselves like plant seed. |
| 0:27:51.140 | 1671.140 | MS. ARBUS SHERRY | generation(s) | It's not even limited -- when you talk -- Justice Breyer, you mentioned the three different generations of seeds. |
| 0:27:51.840 | 1671.840 | MS. ARBUS SHERRY | seed(s) | It's not even limited -- when you talk -- Justice Breyer, you mentioned the three different generations of seeds. |
| 0:27:53.460 | 1673.460 | MS. ARBUS SHERRY | generation(s) | There is actually quite a few more generations than those three. |
| 0:28:01.800 | 1681.800 | MS. ARBUS SHERRY | seed(s) | If the concept is the sale of a parent plant exhausts the patentholder's rights, not only with respect to that seed, but with respect to all the progeny seed, we would have to go all the way back to the very first Roundup Ready plant that was created as part of the transformation event. |
| 0:28:07.520 | 1687.520 | MS. ARBUS SHERRY | Roundup | If the concept is the sale of a parent plant exhausts the patentholder's rights, not only with respect to that seed, but with respect to all the progeny seed, we would have to go all the way back to the very first Roundup Ready plant that was created as part of the transformation event. |
| 0:28:12.260 | 1692.260 | MS. ARBUS SHERRY | Roundup | Every single Roundup Ready seed in existence today is the progeny of that one parent plant and, as Your Honor pointed out, that would eviscerate patent protections. |
| 0:28:12.840 | 1692.840 | MS. ARBUS SHERRY | seed(s) | Every single Roundup Ready seed in existence today is the progeny of that one parent plant and, as Your Honor pointed out, that would eviscerate patent protections. |
| 0:28:24.080 | 1704.080 | MS. ARBUS SHERRY | Roundup | There would be no incentive to invest, not just in Roundup Ready soybeans or not even agricultural technology, but it's quite a bit broader than that. |
| 0:28:24.580 | 1704.580 | MS. ARBUS SHERRY | soybean(s) | There would be no incentive to invest, not just in Roundup Ready soybeans or not even agricultural technology, but it's quite a bit broader than that. |
| 0:29:01.260 | 1741.260 | JUSTICE SCALIA | farmer | That's a pretty horrible result, but let me give you another horrible result, and that is if -- if we agree with you, farmers will not be able to do a second planting by simply getting the undifferentiated seeds from -- from a grain elevator because at least a few of those seeds will always be patented seeds, and no farmer could ever plant anything from a grain elevator, which means -- I gather they use it for second plantings where the risks are so high that it doesn't pay to buy expensive seed. |
| 0:29:09.400 | 1749.400 | JUSTICE SCALIA | seed(s) | That's a pretty horrible result, but let me give you another horrible result, and that is if -- if we agree with you, farmers will not be able to do a second planting by simply getting the undifferentiated seeds from -- from a grain elevator because at least a few of those seeds will always be patented seeds, and no farmer could ever plant anything from a grain elevator, which means -- I gather they use it for second plantings where the risks are so high that it doesn't pay to buy expensive seed. |
| 0:29:11.900 | 1751.900 | JUSTICE SCALIA | grain elevator | That's a pretty horrible result, but let me give you another horrible result, and that is if -- if we agree with you, farmers will not be able to do a second planting by simply getting the undifferentiated seeds from -- from a grain elevator because at least a few of those seeds will always be patented seeds, and no farmer could ever plant anything from a grain elevator, which means -- I gather they use it for second plantings where the risks are so high that it doesn't pay to buy expensive seed. |
| 0:29:36.880 | 1776.880 | JUSTICE SCALIA | grain elevator | Now they can't do that anymore because there's practically no grain elevator that doesn't have at least one patented seed in it. |
| 0:29:40.000 | 1780.000 | JUSTICE SCALIA | seed(s) | Now they can't do that anymore because there's practically no grain elevator that doesn't have at least one patented seed in it. |
| 0:29:46.940 | 1786.940 | MS. ARBUS SHERRY | farmer | Despite what Petitioner says, farmers do not generally go to grain elevators, buy commingled grain, plant it in the ground as seed. |
| 0:29:48.560 | 1788.560 | MS. ARBUS SHERRY | grain elevator | Despite what Petitioner says, farmers do not generally go to grain elevators, buy commingled grain, plant it in the ground as seed. |
| 0:29:53.040 | 1793.040 | MS. ARBUS SHERRY | seed(s) | Despite what Petitioner says, farmers do not generally go to grain elevators, buy commingled grain, plant it in the ground as seed. |
| 0:29:54.300 | 1794.300 | MS. ARBUS SHERRY | soybean(s) | If you look at the American Soybean Association brief submitted on behalf of soybean farmers, it says as much. |
| 0:29:57.140 | 1797.140 | MS. ARBUS SHERRY | farmer | If you look at the American Soybean Association brief submitted on behalf of soybean farmers, it says as much. |
| 0:30:02.220 | 1802.220 | MS. ARBUS SHERRY | grain elevator | If you look at the CHS brief, which is submitted on behalf of grain elevators, it also explains that. |
| 0:30:13.280 | 1813.280 | MS. ARBUS SHERRY | grain elevator | The business of grain elevators is not to sell commingled grain as seed. |
| 0:30:17.080 | 1817.080 | MS. ARBUS SHERRY | seed(s) | The business of grain elevators is not to sell commingled grain as seed. |
| 0:30:20.000 | 1820.000 | MS. ARBUS SHERRY | seed(s) | If that was their business they would have to comply with seed labeling laws. |
| 0:30:25.224 | 1825.224 | JUSTICE SCALIA | farmer | And that's why farmers -- |
| 0:30:26.040 | 1826.040 | JUSTICE SCALIA | farmer | -- and that's why farmers want to use it, for a cheap planting. |
| 0:30:30.660 | 1830.660 | MS. ARBUS SHERRY | farmer | But farmers wouldn't be able to use it for another reason as well. |
| 0:30:40.980 | 1840.980 | JUSTICE KENNEDY | Bowman | But correct me -- correct me if I am wrong; I thought that is what Bowman did. |
| 0:30:42.680 | 1842.680 | MS. ARBUS SHERRY | Bowman | Bowman did, absolutely did it in this circumstance. |
| 0:30:45.740 | 1845.740 | MS. ARBUS SHERRY | Bowman | But Bowman also said that he is not aware of other farmers who are engaging in this practice. |
| 0:30:48.000 | 1848.000 | MS. ARBUS SHERRY | farmer | But Bowman also said that he is not aware of other farmers who are engaging in this practice. |
| 0:31:15.760 | 1875.760 | MS. ARBUS SHERRY | seed(s) | So even putting patent law to the side, this is not an economically viable source of seed for farmers, regardless. |
| 0:31:16.200 | 1876.200 | MS. ARBUS SHERRY | farmer | So even putting patent law to the side, this is not an economically viable source of seed for farmers, regardless. |
| 0:31:20.860 | 1880.860 | MS. ARBUS SHERRY | grain elevator | And Petitioner's argument again isn't limited to the grain elevators. |
| 0:31:23.260 | 1883.260 | MS. ARBUS SHERRY | seed(s) | It would apply to saving your own seed and planting it generation after generation. |
| 0:31:24.240 | 1884.240 | MS. ARBUS SHERRY | generation(s) | It would apply to saving your own seed and planting it generation after generation. |
| 0:31:27.100 | 1887.100 | MS. ARBUS SHERRY | seed(s) | It would apply to selling seeds to your neighboring farmer, and it would allow seed companies to essentially compete with Monsanto upon the first sale. |
| 0:31:28.540 | 1888.540 | MS. ARBUS SHERRY | farmer | It would apply to selling seeds to your neighboring farmer, and it would allow seed companies to essentially compete with Monsanto upon the first sale. |
| 0:31:40.780 | 1900.780 | CHIEF JUSTICE ROBERTS | seed(s) | So when -- when are the patent rights exhausted in the seed? |
| 0:31:43.920 | 1903.920 | MS. ARBUS SHERRY | seed(s) | The patent rights are exhausted in the seed at the same time they are exhausted with respect to any other product, upon an authorized sale. |
| 0:31:58.420 | 1918.420 | MS. ARBUS SHERRY | seed(s) | In our view, once there is an authorized sale, you can do what you want with respect to the seed that you've actually purchased. |
| 0:32:05.840 | 1925.840 | MS. ARBUS SHERRY | generation(s) | But you do need permission from the patentholder in order to make a new generation of seed. |
| 0:32:06.640 | 1926.640 | MS. ARBUS SHERRY | seed(s) | But you do need permission from the patentholder in order to make a new generation of seed. |
| 0:32:20.780 | 1940.780 | JUSTICE SOTOMAYOR | seed(s) | Just so I can follow your -- just so I can follow your answer, Monsanto sells the seed to the farmer. |
| 0:32:22.020 | 1942.020 | JUSTICE SOTOMAYOR | farmer | Just so I can follow your -- just so I can follow your answer, Monsanto sells the seed to the farmer. |
| 0:32:23.260 | 1943.260 | JUSTICE SOTOMAYOR | farmer | And you are saying if the farmer grows the seed, he can sell it to anybody he wants, right? |
| 0:32:23.980 | 1943.980 | JUSTICE SOTOMAYOR | seed(s) | And you are saying if the farmer grows the seed, he can sell it to anybody he wants, right? |
| 0:32:39.240 | 1959.240 | MS. ARBUS SHERRY | generation(s) | So if Monsanto authorized that first sale and authorized the planting, they would also have to authorize the sale of the second generation seed because it's a new article. |
| 0:32:39.680 | 1959.680 | MS. ARBUS SHERRY | seed(s) | So if Monsanto authorized that first sale and authorized the planting, they would also have to authorize the sale of the second generation seed because it's a new article. |
| 0:32:52.600 | 1972.600 | MS. ARBUS SHERRY | Roundup | If you look at the technology agreement -- and it's not just because it's a contract because I think it's significant to the analysis -- Monsanto, upon the first sale of the bag of Roundup Ready seed, authorizes the planting for one commercial crop and it authorizes the farmer to sell that as a commercial crop or to use it for any purpose other than replanting. |
| 0:32:53.120 | 1973.120 | MS. ARBUS SHERRY | seed(s) | If you look at the technology agreement -- and it's not just because it's a contract because I think it's significant to the analysis -- Monsanto, upon the first sale of the bag of Roundup Ready seed, authorizes the planting for one commercial crop and it authorizes the farmer to sell that as a commercial crop or to use it for any purpose other than replanting. |
| 0:32:58.580 | 1978.580 | MS. ARBUS SHERRY | farmer | If you look at the technology agreement -- and it's not just because it's a contract because I think it's significant to the analysis -- Monsanto, upon the first sale of the bag of Roundup Ready seed, authorizes the planting for one commercial crop and it authorizes the farmer to sell that as a commercial crop or to use it for any purpose other than replanting. |
| 0:33:06.340 | 1986.340 | MS. ARBUS SHERRY | generation(s) | So if you take that second generation seed -- "second generation" is a bit of a misnomer, but if you take that seed and you follow it through, all of the patent rights with respect to that particular seed have been exhausted. |
| 0:33:06.860 | 1986.860 | MS. ARBUS SHERRY | seed(s) | So if you take that second generation seed -- "second generation" is a bit of a misnomer, but if you take that seed and you follow it through, all of the patent rights with respect to that particular seed have been exhausted. |
| 0:33:18.540 | 1998.540 | MS. ARBUS SHERRY | seed(s) | But you cannot take that seed without separate authorization, plant it in the ground, and come up with the next generation of seed. |
| 0:33:23.040 | 2003.040 | MS. ARBUS SHERRY | generation(s) | But you cannot take that seed without separate authorization, plant it in the ground, and come up with the next generation of seed. |
| 0:34:08.340 | 2048.340 | MS. ARBUS SHERRY | eBay | I can purchase software; one reasonable use would be to make a dozen other copies to give to my friends or sell on eBay. |
| 0:36:17.860 | 2177.860 | MR. WAXMAN | soybean(s) | First of all, Justice Kennedy, soybeans are soybeans. |
| 0:36:30.420 | 2190.420 | MR. WAXMAN | seed(s) | It is not a plant like a flower, geranium for example, which has to be left to go to seed, or alfalfa. |
| 0:36:32.960 | 2192.960 | MR. WAXMAN | seed(s) | The bean is the seed. |
| 0:36:33.760 | 2193.760 | MR. WAXMAN | soybean(s) | All soybeans have to be processed to be used in any way. |
| 0:36:57.840 | 2217.840 | MR. WAXMAN | farmer | Justice Scalia, your question about well, farmers now just can't do second plantings because soybeans are put in huge grain elevators and different varieties are mingled, that is true in the sense that if one or more of those soybeans were protected by a patent, the actual growing of the use of those patented inventions without a license would be infringement, although, of course, if no glyphosate were put on top of it, neither the farmer nor Monsanto would ever know that there was an act of infringement. |
| 0:37:00.560 | 2220.560 | MR. WAXMAN | soybean(s) | Justice Scalia, your question about well, farmers now just can't do second plantings because soybeans are put in huge grain elevators and different varieties are mingled, that is true in the sense that if one or more of those soybeans were protected by a patent, the actual growing of the use of those patented inventions without a license would be infringement, although, of course, if no glyphosate were put on top of it, neither the farmer nor Monsanto would ever know that there was an act of infringement. |
| 0:37:02.640 | 2222.640 | MR. WAXMAN | grain elevator | Justice Scalia, your question about well, farmers now just can't do second plantings because soybeans are put in huge grain elevators and different varieties are mingled, that is true in the sense that if one or more of those soybeans were protected by a patent, the actual growing of the use of those patented inventions without a license would be infringement, although, of course, if no glyphosate were put on top of it, neither the farmer nor Monsanto would ever know that there was an act of infringement. |
| 0:37:33.140 | 2253.140 | MR. WAXMAN | farmer | But more to the point, farmers -- I mean, the planting of second crops, that is crop rotation of interspersing soybeans and winter wheat, is very, very common. |
| 0:37:38.140 | 2258.140 | MR. WAXMAN | soybean(s) | But more to the point, farmers -- I mean, the planting of second crops, that is crop rotation of interspersing soybeans and winter wheat, is very, very common. |
| 0:37:43.580 | 2263.580 | MR. WAXMAN | soybean(s) | There are hundreds of thousands of soybean farmers who do this every year. |
| 0:37:44.020 | 2264.020 | MR. WAXMAN | farmer | There are hundreds of thousands of soybean farmers who do this every year. |
| 0:37:46.940 | 2266.940 | MR. WAXMAN | Bowman | Mr. Bowman has acknowledged that so far as he knows, he's the only one who's doing it this way. |
| 0:38:01.960 | 2281.960 | MR. WAXMAN | soybean(s) | But there are plenty of other ways in which he could obtain a much less expensive crop of -- you know, a particular variety of soybean, so one that will all grow to the same height and germinate at the same time. |
| 0:38:19.480 | 2299.480 | MR. WAXMAN | seed(s) | He said defendant wanted a cheap source of seed for his second crop beans because of the normal risks in growing "wheat beans;" that is, the second crop that follows the harvesting of winter wheat. |
| 0:38:33.500 | 2313.500 | MR. WAXMAN | soybean(s) | Quote, "defendant simply wasn't going to plant the high priced soybean seed after his wheat crop." |
| 0:38:34.160 | 2314.160 | MR. WAXMAN | seed(s) | Quote, "defendant simply wasn't going to plant the high priced soybean seed after his wheat crop." |
| 0:38:39.960 | 2319.960 | MR. WAXMAN | seed(s) | "Defendant could have purchased conventional seed, that is, non-patented seed, and then saved its offspring for wheat beans." |
| 0:38:51.340 | 2331.340 | MR. WAXMAN | seed(s) | In other words, he could have gone and bought a non-patented -- a bag of non-patented seed for much less money, and used it as his second crop, or harvested a portion of it -- and soybeans replicate at a rate between 20 and 80 times in each generation -- and have a perpetual source for his second crop thereafter. |
| 0:38:58.940 | 2338.940 | MR. WAXMAN | soybean(s) | In other words, he could have gone and bought a non-patented -- a bag of non-patented seed for much less money, and used it as his second crop, or harvested a portion of it -- and soybeans replicate at a rate between 20 and 80 times in each generation -- and have a perpetual source for his second crop thereafter. |
| 0:39:03.560 | 2343.560 | MR. WAXMAN | generation(s) | In other words, he could have gone and bought a non-patented -- a bag of non-patented seed for much less money, and used it as his second crop, or harvested a portion of it -- and soybeans replicate at a rate between 20 and 80 times in each generation -- and have a perpetual source for his second crop thereafter. |
| 0:39:14.700 | 2354.700 | JUSTICE GINSBURG | seed(s) | But he couldn't put the herbicide on -- he couldn't -- if he went and bought conventional seeds, not the genetically improved seeds -- |
| 0:39:52.540 | 2392.540 | MR. WAXMAN | soybean(s) | He would have to -- if he wanted to buy plain old, you know, conventional soybeans, he has to control for weeds in the conventional way. |
| 0:40:02.220 | 2402.220 | MR. WAXMAN | seed(s) | "Defendant" -- that is, instead of purchasing conventional seeds and saving them, he says "Defendant decided to purchase a grain dealer's commodity grain because he felt there was a good chance he would obtain mostly grain that would be resistant to glyphosate," and therefore, he could use Monsanto's technology without having to pay for it. |
| 0:40:38.000 | 2438.000 | MR. WAXMAN | soybean(s) | I think the answer is that without the ability -- let's talk about soybeans and then broaden it to other kinds of readily replicable technologies -- without the ability to limit reproduction of soybeans containing this patented trait, Monsanto could not have commercialized its invention, and never would have produced what is, by now, the most popular agricultural technology in America because, as Ms. Sherry was pointing out, the sale of the very first Roundup Ready soybean seed, from which all the trillions of Roundup Ready soybean seeds in existence now derive, would have, under Mr. Bowman's theory, fully exhausted not only Monsanto's rights in that seed that was sold, but in all progeny unto the -- however many generations Justice Breyer thinks is "not too many." |
| 0:41:06.940 | 2466.940 | MR. WAXMAN | Roundup | I think the answer is that without the ability -- let's talk about soybeans and then broaden it to other kinds of readily replicable technologies -- without the ability to limit reproduction of soybeans containing this patented trait, Monsanto could not have commercialized its invention, and never would have produced what is, by now, the most popular agricultural technology in America because, as Ms. Sherry was pointing out, the sale of the very first Roundup Ready soybean seed, from which all the trillions of Roundup Ready soybean seeds in existence now derive, would have, under Mr. Bowman's theory, fully exhausted not only Monsanto's rights in that seed that was sold, but in all progeny unto the -- however many generations Justice Breyer thinks is "not too many." |
| 0:41:09.440 | 2469.440 | MR. WAXMAN | seed(s) | I think the answer is that without the ability -- let's talk about soybeans and then broaden it to other kinds of readily replicable technologies -- without the ability to limit reproduction of soybeans containing this patented trait, Monsanto could not have commercialized its invention, and never would have produced what is, by now, the most popular agricultural technology in America because, as Ms. Sherry was pointing out, the sale of the very first Roundup Ready soybean seed, from which all the trillions of Roundup Ready soybean seeds in existence now derive, would have, under Mr. Bowman's theory, fully exhausted not only Monsanto's rights in that seed that was sold, but in all progeny unto the -- however many generations Justice Breyer thinks is "not too many." |
| 0:41:19.200 | 2479.200 | MR. WAXMAN | Bowman | I think the answer is that without the ability -- let's talk about soybeans and then broaden it to other kinds of readily replicable technologies -- without the ability to limit reproduction of soybeans containing this patented trait, Monsanto could not have commercialized its invention, and never would have produced what is, by now, the most popular agricultural technology in America because, as Ms. Sherry was pointing out, the sale of the very first Roundup Ready soybean seed, from which all the trillions of Roundup Ready soybean seeds in existence now derive, would have, under Mr. Bowman's theory, fully exhausted not only Monsanto's rights in that seed that was sold, but in all progeny unto the -- however many generations Justice Breyer thinks is "not too many." |
| 0:41:28.720 | 2488.720 | MR. WAXMAN | generation(s) | I think the answer is that without the ability -- let's talk about soybeans and then broaden it to other kinds of readily replicable technologies -- without the ability to limit reproduction of soybeans containing this patented trait, Monsanto could not have commercialized its invention, and never would have produced what is, by now, the most popular agricultural technology in America because, as Ms. Sherry was pointing out, the sale of the very first Roundup Ready soybean seed, from which all the trillions of Roundup Ready soybean seeds in existence now derive, would have, under Mr. Bowman's theory, fully exhausted not only Monsanto's rights in that seed that was sold, but in all progeny unto the -- however many generations Justice Breyer thinks is "not too many." |
| 0:41:50.340 | 2510.340 | MR. WAXMAN | soybean(s) | The Department of Agriculture licensed Monsanto to engage in a transformation event; that is, to introduce its recombinant gene into soybean germ plasm. |
| 0:42:43.240 | 2563.240 | JUSTICE SCALIA | bank | You can't rob a bank with it, though, right? |
| 0:42:53.280 | 2573.280 | MR. WAXMAN | bank | And I don't know -- I don't know if you could use it to rob a bank. |
| 0:42:59.760 | 2579.760 | MR. WAXMAN | Roundup | But the point is -- and the -- the Federal Register site for the transformation event with respect to Roundup Ready is -- is provided in a footnote in our brief. |
| 0:43:10.800 | 2590.800 | MR. WAXMAN | soybean(s) | What happens then is that Monsanto uses those transformed cells to grow a soybean plant. |
| 0:43:12.160 | 2592.160 | MR. WAXMAN | soybean(s) | And that soybean plant produces genetic -- produces seeds or soybeans that have the recombinant Roundup Ready technology in it. |
| 0:43:16.300 | 2596.300 | MR. WAXMAN | seed(s) | And that soybean plant produces genetic -- produces seeds or soybeans that have the recombinant Roundup Ready technology in it. |
| 0:43:19.520 | 2599.520 | MR. WAXMAN | Roundup | And that soybean plant produces genetic -- produces seeds or soybeans that have the recombinant Roundup Ready technology in it. |
| 0:43:31.460 | 2611.460 | MR. WAXMAN | seed(s) | Monsanto then provides -- in almost all of the cases, Monsanto engages in licensed sales of those transformed seeds to hundreds of different seed companies that produce different varieties, and they make both conventional seed with a particular varietal makeup and a Roundup Ready version of that variety. |
| 0:43:42.480 | 2622.480 | MR. WAXMAN | Roundup | Monsanto then provides -- in almost all of the cases, Monsanto engages in licensed sales of those transformed seeds to hundreds of different seed companies that produce different varieties, and they make both conventional seed with a particular varietal makeup and a Roundup Ready version of that variety. |
| 0:43:47.420 | 2627.420 | MR. WAXMAN | soybean(s) | Monsanto provides the soybeans that it has transformed to the seed companies, to the hundreds of seed companies for consideration. |
| 0:43:51.080 | 2631.080 | MR. WAXMAN | seed(s) | Monsanto provides the soybeans that it has transformed to the seed companies, to the hundreds of seed companies for consideration. |
| 0:43:56.280 | 2636.280 | MR. WAXMAN | Bowman | Under Mr. Bowman's theory, that was it for all of Monsanto's rights with respect to this technology. |
| 0:44:05.800 | 2645.800 | MR. WAXMAN | seed(s) | The very first time it took an original transformed seed and sold it to a seed company so that it could bulk up and cross-breed and produce different varieties, Monsanto had lost all of its patent rights. |
| 0:44:56.300 | 2696.300 | JUSTICE KAGAN | seed(s) | So that -- you know, seeds can be blown onto a farmer's farm by wind, and all of a sudden you have Roundup seeds there and the person -- farmer is infringing, or there's a 10-year-old who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 0:44:57.900 | 2697.900 | JUSTICE KAGAN | farmer | So that -- you know, seeds can be blown onto a farmer's farm by wind, and all of a sudden you have Roundup seeds there and the person -- farmer is infringing, or there's a 10-year-old who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 0:45:02.140 | 2702.140 | JUSTICE KAGAN | Roundup | So that -- you know, seeds can be blown onto a farmer's farm by wind, and all of a sudden you have Roundup seeds there and the person -- farmer is infringing, or there's a 10-year-old who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 0:45:08.660 | 2708.660 | JUSTICE KAGAN | science project | So that -- you know, seeds can be blown onto a farmer's farm by wind, and all of a sudden you have Roundup seeds there and the person -- farmer is infringing, or there's a 10-year-old who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 0:45:10.520 | 2710.520 | JUSTICE KAGAN | soybean(s) | So that -- you know, seeds can be blown onto a farmer's farm by wind, and all of a sudden you have Roundup seeds there and the person -- farmer is infringing, or there's a 10-year-old who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 0:45:13.360 | 2713.360 | JUSTICE KAGAN | edamame | So that -- you know, seeds can be blown onto a farmer's farm by wind, and all of a sudden you have Roundup seeds there and the person -- farmer is infringing, or there's a 10-year-old who wants to do a science project of creating a soybean plant, and he goes to the supermarket and gets some edamame, and it turns out that it's Roundup seeds. |
| 0:45:17.760 | 2717.760 | JUSTICE KAGAN | Roundup | And, you know, these Roundup seeds are everywhere, it seems to me. |
| 0:45:18.140 | 2718.140 | JUSTICE KAGAN | seed(s) | And, you know, these Roundup seeds are everywhere, it seems to me. |
| 0:45:22.880 | 2722.880 | JUSTICE KAGAN | seed(s) | There's, what, 90 percent of all the seeds that are around? |
| 0:45:34.500 | 2734.500 | MR. WAXMAN | edamame | Let me make -- let me make three points, starting with the edamame and moving up to inadvertent infringers. |
| 0:45:38.220 | 2738.220 | MR. WAXMAN | edamame | Edamame is an immature form of the soybean seed. |
| 0:45:41.320 | 2741.320 | MR. WAXMAN | soybean(s) | Edamame is an immature form of the soybean seed. |
| 0:45:41.820 | 2741.820 | MR. WAXMAN | seed(s) | Edamame is an immature form of the soybean seed. |
| 0:45:43.300 | 2743.300 | MR. WAXMAN | edamame | You can plant edamame -- |
| 0:46:02.940 | 2762.940 | MR. WAXMAN | edamame | Well, it also reminds me that my original answer to Justice Kennedy is wrong, which is that edamame is taken from the pods before the -- the thing becomes actually a seed that can be processed in any other way. |
| 0:46:11.440 | 2771.440 | MR. WAXMAN | seed(s) | Well, it also reminds me that my original answer to Justice Kennedy is wrong, which is that edamame is taken from the pods before the -- the thing becomes actually a seed that can be processed in any other way. |
| 0:46:19.060 | 2779.060 | MR. WAXMAN | Roundup | Your point about the ubiquity of Roundup Ready -- Roundup Ready's use is a fair one. |
| 0:46:29.940 | 2789.940 | MR. WAXMAN | Roundup | The very first Roundup Ready soybean seed was only made in 1996. |
| 0:46:31.760 | 2791.760 | MR. WAXMAN | soybean(s) | The very first Roundup Ready soybean seed was only made in 1996. |
| 0:46:32.520 | 2792.520 | MR. WAXMAN | seed(s) | The very first Roundup Ready soybean seed was only made in 1996. |
| 0:46:40.940 | 2800.940 | MR. WAXMAN | soybean(s) | And it now is grown by more than 90 percent of the 275,000 soybean farms in the United States. |
| 0:46:53.900 | 2813.900 | MR. WAXMAN | soybean(s) | You may very -- with soybeans, the problem of blowing seed is not an issue for soybeans. |
| 0:46:55.500 | 2815.500 | MR. WAXMAN | seed(s) | You may very -- with soybeans, the problem of blowing seed is not an issue for soybeans. |
| 0:46:57.780 | 2817.780 | MR. WAXMAN | soybean(s) | Soybeans don't -- I mean, it would take Hurricane Sandy to blow a soybean into some other farmer's field. |
| 0:47:04.820 | 2824.820 | MR. WAXMAN | farmer | Soybeans don't -- I mean, it would take Hurricane Sandy to blow a soybean into some other farmer's field. |
| 0:47:06.300 | 2826.300 | MR. WAXMAN | soybean(s) | And soybeans, in any event, are -- you know, have perfect flowers; that is, they contain both the pollen and the stamen, so that they -- which is the reason that they breed -- breed true, unlike, for example, corn. |
| 0:47:20.760 | 2840.760 | MR. WAXMAN | farmer | The point that there may be many farmers with respect to other crops, like alfalfa, that may have some inadvertent Roundup Ready alfalfa in their fields may be true, although it's -- it is not well documented. |
| 0:47:28.480 | 2848.480 | MR. WAXMAN | Roundup | The point that there may be many farmers with respect to other crops, like alfalfa, that may have some inadvertent Roundup Ready alfalfa in their fields may be true, although it's -- it is not well documented. |
| 0:47:39.720 | 2859.720 | MR. WAXMAN | farmer | There would be inadvertent infringement if the farmer was cultivating a patented crop, but there would be no enforcement of that. |
| 0:47:47.740 | 2867.740 | MR. WAXMAN | farmer | The farmer wouldn't know, Monsanto wouldn't know, and in any event, the damages would be zero because you would ask what the reasonable royalty would be, and if the farmer doesn't want Roundup Ready technology and isn't using Roundup Ready technology to save costs and increase productivity, the -- the royalty value would be zero. |
| 0:47:58.060 | 2878.060 | MR. WAXMAN | Roundup | The farmer wouldn't know, Monsanto wouldn't know, and in any event, the damages would be zero because you would ask what the reasonable royalty would be, and if the farmer doesn't want Roundup Ready technology and isn't using Roundup Ready technology to save costs and increase productivity, the -- the royalty value would be zero. |
| 0:50:52.540 | 3052.540 | MR. WAXMAN | soybean(s) | So I think you have decided in the context of software, which of course replicates even more readily than soybeans do or vaccines or cell lines or plasmids, that the copies that are actually made when a -- a software is written onto the hard drive of a computer is a different thing than the disk that was sent and is infringing, if it occurs within the United States. |
| 0:50:53.880 | 3053.880 | MR. WAXMAN | vaccine | So I think you have decided in the context of software, which of course replicates even more readily than soybeans do or vaccines or cell lines or plasmids, that the copies that are actually made when a -- a software is written onto the hard drive of a computer is a different thing than the disk that was sent and is infringing, if it occurs within the United States. |
| 0:51:30.940 | 3090.940 | JUSTICE BREYER | generation(s) | I mean, I would have thought it doesn't concern Monsanto's license of generation 1 because, insofar as it's relevant, here generation 1 carries the license that is just permissive. |
| 0:51:38.580 | 3098.580 | JUSTICE BREYER | generation(s) | It is to create generation 2. |
| 0:51:51.240 | 3111.240 | JUSTICE BREYER | generation(s) | But -- but they also said something in the circuit about a license -- about a restriction, implied perhaps, on -- on the use of generation 2 by the grain elevator for creating generation 3, namely you can't do that. |
| 0:51:52.560 | 3112.560 | JUSTICE BREYER | grain elevator | But -- but they also said something in the circuit about a license -- about a restriction, implied perhaps, on -- on the use of generation 2 by the grain elevator for creating generation 3, namely you can't do that. |
| 0:52:57.860 | 3177.860 | MR. WAXMAN | seed(s) | "Even if Monsanto's patent rights in the commodity seeds are exhausted, such a conclusion would be of no consequence because once a grower like Bowman plants the commodity seeds containing Monsanto's Roundup Ready technology and the next generation of seed develops, the grower has created a newly infringing article." |
| 0:53:05.020 | 3185.020 | MR. WAXMAN | Bowman | "Even if Monsanto's patent rights in the commodity seeds are exhausted, such a conclusion would be of no consequence because once a grower like Bowman plants the commodity seeds containing Monsanto's Roundup Ready technology and the next generation of seed develops, the grower has created a newly infringing article." |
| 0:53:09.220 | 3189.220 | MR. WAXMAN | Roundup | "Even if Monsanto's patent rights in the commodity seeds are exhausted, such a conclusion would be of no consequence because once a grower like Bowman plants the commodity seeds containing Monsanto's Roundup Ready technology and the next generation of seed develops, the grower has created a newly infringing article." |
| 0:53:12.240 | 3192.240 | MR. WAXMAN | generation(s) | "Even if Monsanto's patent rights in the commodity seeds are exhausted, such a conclusion would be of no consequence because once a grower like Bowman plants the commodity seeds containing Monsanto's Roundup Ready technology and the next generation of seed develops, the grower has created a newly infringing article." |
| 0:53:28.560 | 3208.560 | MR. WAXMAN | generation(s) | In other words, what the Federal Circuit decided, and it is entirely correct and it should be affirmed on that basis, is what you're calling, I think generation 3, let's say that for simplicity's sake, since generation 1 is the original soybean sold by Monsanto to seed companies, let's just say that the bags of soybean seeds that farmers go to purchase from seed dealers is called generation N and they are licensed to produce generation N plus 1. |
| 0:53:34.520 | 3214.520 | MR. WAXMAN | soybean(s) | In other words, what the Federal Circuit decided, and it is entirely correct and it should be affirmed on that basis, is what you're calling, I think generation 3, let's say that for simplicity's sake, since generation 1 is the original soybean sold by Monsanto to seed companies, let's just say that the bags of soybean seeds that farmers go to purchase from seed dealers is called generation N and they are licensed to produce generation N plus 1. |
| 0:53:36.780 | 3216.780 | MR. WAXMAN | seed(s) | In other words, what the Federal Circuit decided, and it is entirely correct and it should be affirmed on that basis, is what you're calling, I think generation 3, let's say that for simplicity's sake, since generation 1 is the original soybean sold by Monsanto to seed companies, let's just say that the bags of soybean seeds that farmers go to purchase from seed dealers is called generation N and they are licensed to produce generation N plus 1. |
| 0:53:42.220 | 3222.220 | MR. WAXMAN | farmer | In other words, what the Federal Circuit decided, and it is entirely correct and it should be affirmed on that basis, is what you're calling, I think generation 3, let's say that for simplicity's sake, since generation 1 is the original soybean sold by Monsanto to seed companies, let's just say that the bags of soybean seeds that farmers go to purchase from seed dealers is called generation N and they are licensed to produce generation N plus 1. |
| 0:54:41.820 | 3281.820 | MR. WAXMAN | generation(s) | If you're referring to generation N plus 2, the answer is yes, because those are newly infringing products with no exhaustion of Monsanto's rights, and as a consequence farmers have no authority to use, make, sell, or offer to sell without Monsanto's authorization. |
| 0:54:53.820 | 3293.820 | MR. WAXMAN | farmer | If you're referring to generation N plus 2, the answer is yes, because those are newly infringing products with no exhaustion of Monsanto's rights, and as a consequence farmers have no authority to use, make, sell, or offer to sell without Monsanto's authorization. |
| 0:56:39.060 | 3399.060 | MR. WAXMAN | Bowman | Mr. Bowman acknowledges that. |
| 0:57:44.380 | 3464.380 | MR. WAXMAN | soybean(s) | Yes, and I think the reason, if we take it out of the soybean area, let's look at vaccines. |
| 0:57:46.940 | 3466.940 | MR. WAXMAN | vaccine | Yes, and I think the reason, if we take it out of the soybean area, let's look at vaccines. |
| 0:57:48.860 | 3468.860 | MR. WAXMAN | Roundup | Because the Roundup Ready gene essentially immunizes soybean plants from the herbicide in the same way that a life-saving vaccine will immunize individuals that receive it from some external -- it wouldn't be a herbicide -- a life threat. |
| 0:57:51.440 | 3471.440 | MR. WAXMAN | soybean(s) | Because the Roundup Ready gene essentially immunizes soybean plants from the herbicide in the same way that a life-saving vaccine will immunize individuals that receive it from some external -- it wouldn't be a herbicide -- a life threat. |
| 0:57:56.300 | 3476.300 | MR. WAXMAN | vaccine | Because the Roundup Ready gene essentially immunizes soybean plants from the herbicide in the same way that a life-saving vaccine will immunize individuals that receive it from some external -- it wouldn't be a herbicide -- a life threat. |
| 0:58:07.120 | 3487.120 | MR. WAXMAN | vaccine | Vaccines are live. |
| 0:58:14.700 | 3494.700 | MR. WAXMAN | vaccine | If a company develops the vaccine for, you know, H1 -- I shouldn't be using -- an important life-saving vaccine -- |
| 0:58:31.080 | 3511.080 | MR. WAXMAN | vaccine | -- it's unsupportable to say that you cannot sell a quantity of that vaccine without exhausting all of your rights in it. |
| 0:58:42.360 | 3522.360 | MR. WAXMAN | vaccine | I mean, when -- when Schering-Plough or Bristol-Myers develops a vaccine and sells some of it to CVS so I can go in and get injected, they haven't lost all of their patent rights in that vaccine. |
| 0:58:57.140 | 3537.140 | JUSTICE SOTOMAYOR | vaccine | Simplifying this case, you can't take the person who's been given the vaccine and take vials of their blood and keep selling it? |
| 0:59:17.200 | 3557.200 | CHIEF JUSTICE ROBERTS | vaccine | I mean, your example, it seems to me, is not quite on point because it's not a situation where the intended use of the vaccine necessarily results in regeneration of it. |
| 1:00:10.900 | 3610.900 | MR. WAXMAN | soybean(s) | Bacteria replicate themselves, unlike soybeans which require human intervention. |
| 1:01:03.900 | 3663.900 | MR. WAXMAN | seed(s) | And so, like Monsanto with its seeds, I sign -- I provide a copy of the machine to MIT, with a research-only license; that is, you can use this machine to figure out how it works and develop new applications and all that sort of stuff. |
| 1:01:41.860 | 3701.860 | MR. WAXMAN | soybean(s) | Yes, but you can't lease articles like software and, you know, soybeans that consume themselves in any use, other than an art experiment. |
| 1:01:58.460 | 3718.460 | JUSTICE KENNEDY | seed(s) | What about the commodity bin that has 2 percent of the patented seeds in them? |
| 1:02:03.000 | 3723.000 | JUSTICE KENNEDY | seed(s) | Now, you get away from the article by saying, oh, well, almost all seeds are Roundup these days. |
| 1:02:03.460 | 3723.460 | JUSTICE KENNEDY | Roundup | Now, you get away from the article by saying, oh, well, almost all seeds are Roundup these days. |
| 1:02:12.820 | 3732.820 | JUSTICE KENNEDY | seed(s) | But let's have some different commodity where there are three or four different patented items, but 1 percent, 2 percent of the seeds are in the bin. |
| 1:02:27.880 | 3747.880 | JUSTICE KENNEDY | seed(s) | You can't sell them if they know they are going to be used for seeds, and you can't use them for seeds even though there is only 1 percent of the seeds? |
| 1:02:37.380 | 3757.380 | MR. WAXMAN | grain elevator | First of all, because grain elevators are prohibited by State and Federal law from selling seed, period. |
| 1:02:42.300 | 3762.300 | MR. WAXMAN | seed(s) | First of all, because grain elevators are prohibited by State and Federal law from selling seed, period. |
| 1:02:47.880 | 3767.880 | MR. WAXMAN | seed(s) | They can't sell seed. |
| 1:02:53.300 | 3773.300 | MR. WAXMAN | soybean(s) | Number 2, almost all varieties of soybeans or other crop plants are currently protected by the -- under the patent -- the Plant Variety Protection Act. |
| 1:03:37.400 | 3817.400 | MR. WAXMAN | soybean(s) | So irrespective of all of this, whatever happens, even if there is only 1 percent of patented soybeans in a grain elevator, the grain elevator can't sell it as seed both under the Federal and State seed laws and under the Patent Variety Protection Act. |
| 1:03:38.800 | 3818.800 | MR. WAXMAN | grain elevator | So irrespective of all of this, whatever happens, even if there is only 1 percent of patented soybeans in a grain elevator, the grain elevator can't sell it as seed both under the Federal and State seed laws and under the Patent Variety Protection Act. |
| 1:03:42.920 | 3822.920 | MR. WAXMAN | seed(s) | So irrespective of all of this, whatever happens, even if there is only 1 percent of patented soybeans in a grain elevator, the grain elevator can't sell it as seed both under the Federal and State seed laws and under the Patent Variety Protection Act. |
| 1:03:50.960 | 3830.960 | MR. WAXMAN | farmer | That's why the solution for farmers like Monsanto -- like Mr. Bowman, is to simply buy conventional seed, multiply it, you know, 20, 30, 40, 50, 80 times in a single generation and save 1/80th of it to replant in his second crop, if he doesn't want to buy Roundup Ready technology for his second crop and use the glyphosate aerially. |
| 1:03:53.440 | 3833.440 | MR. WAXMAN | Bowman | That's why the solution for farmers like Monsanto -- like Mr. Bowman, is to simply buy conventional seed, multiply it, you know, 20, 30, 40, 50, 80 times in a single generation and save 1/80th of it to replant in his second crop, if he doesn't want to buy Roundup Ready technology for his second crop and use the glyphosate aerially. |
| 1:03:56.760 | 3836.760 | MR. WAXMAN | seed(s) | That's why the solution for farmers like Monsanto -- like Mr. Bowman, is to simply buy conventional seed, multiply it, you know, 20, 30, 40, 50, 80 times in a single generation and save 1/80th of it to replant in his second crop, if he doesn't want to buy Roundup Ready technology for his second crop and use the glyphosate aerially. |
| 1:04:02.740 | 3842.740 | MR. WAXMAN | generation(s) | That's why the solution for farmers like Monsanto -- like Mr. Bowman, is to simply buy conventional seed, multiply it, you know, 20, 30, 40, 50, 80 times in a single generation and save 1/80th of it to replant in his second crop, if he doesn't want to buy Roundup Ready technology for his second crop and use the glyphosate aerially. |
| 1:04:09.740 | 3849.740 | MR. WAXMAN | Roundup | That's why the solution for farmers like Monsanto -- like Mr. Bowman, is to simply buy conventional seed, multiply it, you know, 20, 30, 40, 50, 80 times in a single generation and save 1/80th of it to replant in his second crop, if he doesn't want to buy Roundup Ready technology for his second crop and use the glyphosate aerially. |
| 1:04:36.260 | 3876.260 | MR. WALTERS | farmer | It may be occasional, when a farmer is in a real desperate situation, or it may apply to Mr. Bowman's situation, where he wanted a very cheap source of seed for his second crop. |
| 1:04:39.520 | 3879.520 | MR. WALTERS | Bowman | It may be occasional, when a farmer is in a real desperate situation, or it may apply to Mr. Bowman's situation, where he wanted a very cheap source of seed for his second crop. |
| 1:04:42.640 | 3882.640 | MR. WALTERS | seed(s) | It may be occasional, when a farmer is in a real desperate situation, or it may apply to Mr. Bowman's situation, where he wanted a very cheap source of seed for his second crop. |
| 1:04:49.820 | 3889.820 | MR. WALTERS | grain elevator | But in the record at 153a, among other places, he discusses how he's gone to the grain elevator over the years a number of times, and how other farmers have gone to the grain elevator for generations. |
| 1:04:52.960 | 3892.960 | MR. WALTERS | farmer | But in the record at 153a, among other places, he discusses how he's gone to the grain elevator over the years a number of times, and how other farmers have gone to the grain elevator for generations. |
| 1:04:55.720 | 3895.720 | MR. WALTERS | generation(s) | But in the record at 153a, among other places, he discusses how he's gone to the grain elevator over the years a number of times, and how other farmers have gone to the grain elevator for generations. |
| 1:05:00.260 | 3900.260 | MR. WALTERS | seed(s) | So a ruling in favor of Monsanto here would effectively eliminate that seed -- |
| 1:05:02.180 | 3902.180 | JUSTICE SCALIA | grain elevator | Do you agree that it's unlawful for grain elevators to sell it for replanting? |
| 1:05:10.960 | 3910.960 | MR. WALTERS | grain elevator | And what he is referring to is State labeling laws that prevent grain elevators from actually scooping up grain, packaging it up and saying this is seed, because they all look alike to -- to the eye. |
| 1:05:15.420 | 3915.420 | MR. WALTERS | seed(s) | And what he is referring to is State labeling laws that prevent grain elevators from actually scooping up grain, packaging it up and saying this is seed, because they all look alike to -- to the eye. |
| 1:05:19.460 | 3919.460 | MR. WALTERS | grain elevator | And so grain elevators are certainly not allowed to dupe seed purchasers, but those laws are there to protect the seed purchasers. |
| 1:05:22.020 | 3922.020 | MR. WALTERS | seed(s) | And so grain elevators are certainly not allowed to dupe seed purchasers, but those laws are there to protect the seed purchasers. |
| 1:05:26.760 | 3926.760 | MR. WALTERS | Bowman | Mr. Bowman bought grain without any restrictions on how he could use it. |
| 1:05:43.340 | 3943.340 | MR. WALTERS | Bowman | Did not assert them in this case and could not assert them in this case because there's no single variety that Mr. Bowman planted. |
| 1:06:11.700 | 3971.700 | MR. WALTERS | seed(s) | This is an invention that the only way to use the invention -- now, repeat, the only way to use the invention -- is to plant it and to grow more seeds. |
| 1:06:34.300 | 3994.300 | JUSTICE BREYER | grain elevator | You can go buy them in the grain elevator and sell them for other things. |
| 1:06:49.400 | 4009.400 | JUSTICE BREYER | seed(s) | The invented aspect of the seed is it has a gene in it that repels some other insecticide or something that they have. |
| 1:07:31.400 | 4051.400 | JUSTICE BREYER | grain elevator | The people buying from grain elevators are mostly people who take these chips -- whatever they are, the seeds -- and they sell them for making tofu, they sell them to eat, or this -- there are loads of uses, aren't there? |
| 1:07:36.540 | 4056.540 | JUSTICE BREYER | seed(s) | The people buying from grain elevators are mostly people who take these chips -- whatever they are, the seeds -- and they sell them for making tofu, they sell them to eat, or this -- there are loads of uses, aren't there? |
| 1:07:47.940 | 4067.940 | MR. WALTERS | Bowman | But the only use of the invention is to plant it, and that's the use that Mr. Bowman makes. |
| 1:07:58.180 | 4078.180 | JUSTICE SCALIA | generation(s) | What he is prevented from doing is using the -- the consequences of that planting, the second generation seeds, for another planting. |
| 1:07:58.760 | 4078.760 | JUSTICE SCALIA | seed(s) | What he is prevented from doing is using the -- the consequences of that planting, the second generation seeds, for another planting. |
| 1:08:20.140 | 4100.140 | MR. WALTERS | generation(s) | So -- the judgment in this case was based on acres planted, and so I'm not sure how many -- we talked a bit about the N plus 2 generation, and we don't know in the record what the N plus 2 generation was, in terms of his sales or his yields. |
| 1:09:28.140 | 4168.140 | MR. WALTERS | seed(s) | But you're saying that there's no exhaustion in the progeny where he owns that seed outright. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.300 to 0:03:09.300, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.300] MR. WALTERS: Mr. Chief Justice and may it please the Court: Patent exhaustion provides that once a patented article is sold, it passes outside the protection of the Patent Act, and it is available to be used by the purchaser to practice the invention. Now, what's the invention here? The invention is a bit of DNA that, when inserted into a soy bean seed, makes that seed and all the plants that grow from that seed resistant to the active ingredient in Roundup. Now, the only way to practice that invention is to plant the seed and to grow more seeds.

[0:00:45.440] CHIEF JUSTICE ROBERTS: Why in the world would anybody spend any money to try to improve the seed if as soon as they sold the first one anybody could grow more and have as many of those seeds as they want?

[0:00:59.400] MR. WALTERS: I agree no one would do that, and I don't think that is the situation here. I think we have, and we have explained how Respondents here can protect their invention through contracts. They don't have to sell it outright. They can sell it through an agency model, but the more I think important --

[0:01:16.060] CHIEF JUSTICE ROBERTS: That's true, that's true in the case of any patented article, right?

[0:01:19.880] MR. WALTERS: Correct.

[0:01:20.220] CHIEF JUSTICE ROBERTS: So the patent system is based, I think, on a recognition that contractual protection is inadequate to encourage invention.

[0:01:30.300] MR. WALTERS: Well, part of the patent policy, as well, is to protect the purchaser, and that's been part of this Court's law for more than 150 years. Under Respondent's theory, any farmer who grows a soy bean seed is infringing the patent, but for the grace of Monsanto. And that's -- a lot of farmers in this country, when we have over 90 percent of the acreage that is Roundup Ready. So under Monsanto's theory, there is really no limit by the Exhaustion Doctrine?

[0:01:57.720] JUSTICE SCALIA: I didn't understand that last sentence. Any farmer who plants and grows soybeans is violating the patent?

[0:02:05.300] MR. WALTERS: Is infringing under license by Monsanto. Let's take the first --

[0:02:09.700] JUSTICE SCALIA: I thought that their claim is that he only violates the patent if he tries to grow additional seeds from his first crop. Right? Isn't that the only claim here?

[0:02:22.740] MR. WALTERS: The reach of Monsanto's theory is that once that seed is sold, even though title has passed to the farmer, and the farmer assumes all risks associated with farming, that they can still control the ownership of that seed, control how that seed is used.

[0:02:38.480] JUSTICE SCALIA: No, not that seed. It's different seed. That seed is done. It's been planted in the ground and has grown other seed. It's the other seed we are talking about. It's not the very seed that was sold. Right?

[0:02:53.180] MR. WALTERS: That's correct, Your Honor, but if we don't apply -- if exhaustion is eliminated, rather, for the progeny seed, then you are taking away the ability of people to exchange these goods freely in commerce. You have essentially a servitude on these things

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 13, 2013.

- Oyez page: https://www.oyez.org/cases/2012/11-796
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2012/11-796/20130513o_11-796.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.2 MB)
- Length: 0:04:31.073 (271.073 s)
- Words: 638, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause between words within 1.5 s of it. Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (0
  trimmed, 0 re-transcribed).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 600 of Whisper's 638 words (94.0%; Oyez has 627).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:05.920 | 14 |
| JUSTICE KAGAN | 0:00:07.020 | 0:04:30.260 | 604 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kagan has our opinion this morning in Case 11-796, Bowman v. Monsanto Company.

[0:00:07.020] JUSTICE KAGAN: Monsanto invented and then patented a genetic modification that enables soybean plants to survive exposure to glyphosate, the active ingredient in many herbicides. Monsanto calls seeds carrying this trait round-up-ready seeds. Monsanto will only sell round-up-ready seed to farmers who sign a licensing agreement. That agreement allows farmers to plant one and only one crop of soybeans from the round-up-ready seed they purchase. The farmer can then consume the harvested beans or sell them as a commodity. What the farmer cannot do, according to the agreement, is save and replant the soybeans he harvests. The Petitioner in this case, Vernon Bowman, is a farmer who likes round-up-ready technology. For his first soybean crop each year, Bowman purchased round-up-ready seed from a Monsanto affiliate and complied with the terms of the agreement I just described. But for his riskier second soybean crop of each season, Bowman wanted a way to reap the benefits of Monsanto's technology without paying its premium prices. The answer, Bowman decided, lay in buying seeds from the local grain elevator. Soybeans from a grain elevator are meant for consumption, but because soybeans are themselves seeds, nothing prevented Bowman from planting them. And because most Indiana farmers use round-up-ready seed, Bowman suspected that most of the grain elevator soybeans he purchased would carry the round-up-ready trait. He was right. When Bowman planted the grain elevator soybeans and applied glyphosate to his fields, most of the soybean plants survived. Bowman then saved seed from that crop of round-up-ready beans for his second planting the next year. And Bowman repeated that process year after year for 8 years. So he was able to produce 8 crops of round-up-ready soybeans all without buying any seed from Monsanto. When Monsanto discovered this practice, it sued Bowman for patent infringement. The question here is whether Bowman can defend against Monsanto's suit based on what's called the doctrine of patent exhaustion. Under that doctrine, the authorized sale of a patented article gives the purchaser or any subsequent owner like Bowman the right to use or resell that article without the patent holder's permission. The district court held that patent exhaustion did not protect Bowman's conduct and ordered him to pay damages to Monsanto, the Federal Circuit affirmed. We also agree. We hold that patent exhaustion does not

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:07.020-0:00:07.400: "Kagan."

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:33.500 | one | (nothing) |
| 0:00:42.900 | What | But |
| 0:00:46.160 | save | saved |
| 0:00:46.880 | replant | replants |
| 0:01:12.680 | reap | rip |
| 0:01:21.080 | in | and |
| 0:01:37.080 | use round -up | used Roundup |
| 0:01:54.180 | soybean | soybeans |
| 0:02:06.580 | 8 | eight |
| 0:02:09.520 | 8 | eight |
| 0:02:10.480 | of round -up | a Roundup |
| 0:02:24.940 | Monsanto's | Monsanto |
| 0:02:46.600 | that patent | a patented |
| 0:03:17.240 | But | The |
| 0:03:23.740 | entitle | entitled |
| 0:04:08.500 | the | that |
