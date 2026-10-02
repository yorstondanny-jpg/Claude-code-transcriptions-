# alvarez-medal: Supreme Court No. 11-210

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2011/11-210
- Audio: https://www.supremecourt.gov/media/audio/mp3files/11-210.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2011/11-210.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 70 min on 4 CPU cores
- Audio length: 0:59:15.396 (3555.396 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.4 MB
- Official words: 9282 (plus 10 `(Laughter.)` markers), in 266 speaker turns
- ASR words: 9033
- Official words matched to an ASR word: 8716 of 9282 (**93.90%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.90% (threshold 85%).

325 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 8 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 26 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 11-210 2011 alvarez-medal --model medium.en --opinion --mentions "medal,Medal of Honor,Congressional,hockey,Red Wings,married,starlet,dating,date,daughter,lie,lying,liar,shame,valor,Alvarez"

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-49.5 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:21:03.960 | 1263.960 | under speech | 0.00 | 0.00 | - | - | is the line that was -- So, maybe we allow a certain amount of puffing in political speech as well. And I do think that -- Nobody believes all that stuff, right? |
| 2 | 0:24:21.480 | 1461.480 | medium | 1.02 | 0.50 | 16.9 | 26.3 | And I'm not minimizing it. I too take offense when people make these kinds of claims, but I take offense when someone I'm dating makes a claim that's not true. |
| 3 | 0:24:26.512 | 1466.512 | under speech | 0.00 | 0.00 | - | - | but I take offense when someone I'm dating makes a claim that's not true. And -- and -- And as -- as the father of a 20-year-old daughter, so do I, Justice Sotomayor. |
| 4 | 0:29:30.900 | 1770.900 | big | 5.38 | 5.20 | 24.7 | 30.4 | Well, that's right, and that's certainly a beneficial lie. That's not a statement about one's self. This is -- And now -- Are you hiding Jews in the cellar? Excuse me. Sorry. |
| 5 | 0:45:43.260 | 2743.260 | small | 0.98 | 0.00 | 5.2 | 9.4 | and yet, I can think of instances where we do want to protect false information. And I want you to accept that as a given because that isn't my question. |
| 6 | 0:48:57.040 | 2937.040 | medium | 0.74 | 0.45 | 14.6 | 17.6 | who has won them. All the heroic acts that have -- How about giving a medal of shame to those who have falsely claimed to have earned the medal of valor? |
| 7 | 0:52:52.610 | 3172.610 | under speech | 0.00 | 0.00 | - | - | But that's not -- the answer is would the First Amendment permit that. That's a difficult question, Your Honor. Well, that's sort of the question we have to answer here. Sure. |
| 8 | 0:52:55.020 | 3175.020 | big | 2.12 | 1.75 | 26.9 | 35.2 | answer is would the First Amendment permit that. That's a difficult question, Your Honor. Well, that's sort of the question we have to answer here. Sure. And I get that. |
| 9 | 0:53:16.720 | 3196.720 | under speech | 0.00 | 0.00 | - | - | comes -- when you get into the situation where you're getting something like a date, I do not know that -- I certainly wouldn't consider that a non-de minimis thing of value. |
| 10 | 0:53:21.280 | 3201.280 | under speech | 0.00 | 0.00 | - | - | you're getting something like a date, I do not know that -- I certainly wouldn't consider that a non-de minimis thing of value. But -- Some people might have a different opinion. |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| medal | 38 | 49 |
| Medal of Honor | 7 | 7 |
| Congressional | 4 | 4 |
| hockey | 0 | 0 |
| Red Wings | 0 | 0 |
| married | 0 | 0 |
| starlet | 0 | 0 |
| dating | 1 | 1 |
| date | 4 | 5 |
| daughter | 1 | 1 |
| lie | 18 | 20 |
| lying | 3 | 3 |
| liar | 2 | 2 |
| shame | 2 | 2 |
| valor | 7 | 8 |
| Alvarez | 5 | 5 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:06.340 | 6.340 | CHIEF JUSTICE ROBERTS | Alvarez | We'll hear argument first this morning in Case 11-210, United States v. Alvarez. |
| 0:00:28.200 | 28.200 | GENERAL VERRILLI | valor | The Stolen Valor Act continues that tradition by prohibiting knowingly false statements that one has been awarded a military honor. |
| 0:01:32.040 | 92.040 | JUSTICE SOTOMAYOR | medal | Is that person -- if he's not a veteran having received a medal, is he liable under this Act? |
| 0:04:09.720 | 249.720 | GENERAL VERRILLI | valor | Those are substantial constraints, but they are substantial constraints that are satisfied in this case because the Stolen Valor Act regulates a very narrowly drawn and specific category of calculated factual falsehood, a verifiably false claim that an individual has won a military honor, and that's information that is within you, and only punishes speech about yourself. |
| 0:08:06.900 | 486.900 | JUSTICE KENNEDY | medal | Here it does seem to me that you can argue that this is something like a -- a trademark, a medal in which this -- the government and the armed forces have a particular interest, and we could carve out a narrow exception for that. |
| 0:13:01.900 | 781.900 | GENERAL VERRILLI | valor | And, of course, with respect to the Stolen Valor Act, the -- Congress -- Congress is building the Stolen Valor Act on a statute that Congress enacted in 1923 which prohibited the -- the wearing of medals without justification to wear the medals. |
| 0:13:13.720 | 793.720 | GENERAL VERRILLI | medal | And, of course, with respect to the Stolen Valor Act, the -- Congress -- Congress is building the Stolen Valor Act on a statute that Congress enacted in 1923 which prohibited the -- the wearing of medals without justification to wear the medals. |
| 0:14:09.540 | 849.540 | JUSTICE ALITO | medal | Suppose the statute also made it a crime to represent falsely that someone else was the recipient of a military medal, so that if someone said falsely and knowingly that a spouse or a parent or a child was a medal recipient, that would also be covered. |
| 0:15:25.780 | 925.780 | GENERAL VERRILLI | medal | You have to answer the question in that case of whether there was a material risk of deterring expression that's truthful because what -- who knows whether your grandfather was telling the truth when he -- when he said he won the medal. |
| 0:15:41.040 | 941.040 | JUSTICE GINSBURG | medal | That was -- and that it's not so hard to find out if somebody claims to have the Medal of Honor and he doesn't. |
| 0:15:41.040 | 941.040 | JUSTICE GINSBURG | Medal of Honor | That was -- and that it's not so hard to find out if somebody claims to have the Medal of Honor and he doesn't. |
| 0:16:57.510 | 1017.510 | GENERAL VERRILLI | medal | This is a pinpoint accuracy, a specific verifiable factual claim about yourself, that you've won a medal. |
| 0:18:54.760 | 1134.760 | JUSTICE KAGAN | medal | -- just about your qualifications, about what you've done in your life, your -- you know, whether you have a Medal of Honor, whether you've been in military service, whether you've been to college. |
| 0:18:54.760 | 1134.760 | JUSTICE KAGAN | Medal of Honor | -- just about your qualifications, about what you've done in your life, your -- you know, whether you have a Medal of Honor, whether you've been in military service, whether you've been to college. |
| 0:19:52.560 | 1192.560 | JUSTICE KAGAN | lie | Well, I assume that that would be, in the case of these State statutes, because the State feels that it has a specially important interest in maintaining the political sphere free of lies. |
| 0:20:29.700 | 1229.700 | JUSTICE SCALIA | lying | I suppose that even in the commercial context we allow a decent amount of lying, don't we? |
| 0:22:12.880 | 1332.880 | JUSTICE KENNEDY | medal | On the other hand, I have to acknowledge that this does diminish the medal in many respects. |
| 0:22:57.360 | 1377.360 | JUSTICE SOTOMAYOR | medal | Wouldn't take much to do exactly what Congress said it was doing, which was to protect against fraudulent claims of receiving a medal, and the example it used was someone who used a fraudulent claim of receiving a medal to get money. |
| 0:23:42.820 | 1422.820 | JUSTICE SOTOMAYOR | medal | If that is the core of our First Amendment, what I hear, and that's what I think the court below said, is you can't really believe that a war veteran thinks less of the medal that he or she received because someone's claiming fraudulently that they got one. |
| 0:23:51.420 | 1431.420 | JUSTICE SOTOMAYOR | medal | They don't think less of the medal. |
| 0:24:19.560 | 1459.560 | JUSTICE SOTOMAYOR | dating | I too take offense when people make these kinds of claims, but I take offense when someone I'm dating makes a claim that's not true. |
| 0:24:24.860 | 1464.860 | GENERAL VERRILLI | daughter | And as -- as the father of a 20-year-old daughter, so do I, Justice Sotomayor. |
| 0:24:40.760 | 1480.760 | GENERAL VERRILLI | medal | I mean, at some level, of course, it is true that no soldier charges up Mount Suribachi thinking, well, I'm going to do this because I'll get a medal if I get to the top. |
| 0:24:45.300 | 1485.300 | JUSTICE SOTOMAYOR | medal | Or I'm not going to do this because the medal has been debased. |
| 0:25:06.300 | 1506.300 | GENERAL VERRILLI | medal | And what the medals do is say to the -- to our military this is what we care about. |
| 0:25:32.240 | 1532.240 | GENERAL VERRILLI | medal | And I -- what I think with respect to the government's interest here and why there is a harm to that interest is that the point of these medals is that it's a big deal. |
| 0:25:46.600 | 1546.600 | GENERAL VERRILLI | medal | And for the government to say this is a really big deal and then to stand idly by when one charlatan after another makes a false claim to have won the medal does debase the value of the medal in the eyes of the soldiers. |
| 0:26:12.400 | 1572.400 | JUSTICE SOTOMAYOR | lying | His public position was compromised, as is the case with almost everyone who's caught at lying. |
| 0:27:24.260 | 1644.260 | MR. LIBBY | valor | Thank you, Mr. Chief Justice, and may it please the Court: The Stolen Valor Act criminalizes pure speech in the form of bare falsity, a mere telling of a lie. |
| 0:27:29.860 | 1649.860 | MR. LIBBY | lie | Thank you, Mr. Chief Justice, and may it please the Court: The Stolen Valor Act criminalizes pure speech in the form of bare falsity, a mere telling of a lie. |
| 0:27:31.880 | 1651.880 | MR. LIBBY | lie | It doesn't matter whether the lie was told in a public meeting or in a private conversation with a friend or family member. |
| 0:27:51.020 | 1671.020 | CHIEF JUSTICE ROBERTS | lie | What is -- what is the First Amendment value in a lie, a pure lie? |
| 0:27:54.260 | 1674.260 | MR. LIBBY | lie | Just a pure lie? |
| 0:28:07.500 | 1687.500 | CHIEF JUSTICE ROBERTS | lie | No, not exaggerate -- lie. |
| 0:28:35.640 | 1715.640 | CHIEF JUSTICE ROBERTS | medal | No one is suggesting you can't write a book or tell a story about somebody who earned a Medal of Honor, and it's a fictional character; so, he obviously didn't. |
| 0:28:35.640 | 1715.640 | CHIEF JUSTICE ROBERTS | Medal of Honor | No one is suggesting you can't write a book or tell a story about somebody who earned a Medal of Honor, and it's a fictional character; so, he obviously didn't. |
| 0:28:45.680 | 1725.680 | MR. LIBBY | lie | But there are other things, in addition to the fact that people tell lies allows us to appreciate truth better. |
| 0:28:54.580 | 1734.580 | JUSTICE ALITO | lie | Do you really think that there is -- that the First Amendment -- that there is First Amendment value in a bald-faced lie about a purely factual statement that a person makes about himself, because that person would like to create a particular persona? |
| 0:29:05.240 | 1745.240 | JUSTICE ALITO | medal | Gee, I won the Medal of Honor. |
| 0:29:05.240 | 1745.240 | JUSTICE ALITO | Medal of Honor | Gee, I won the Medal of Honor. |
| 0:29:25.920 | 1765.920 | MR. LIBBY | lie | Well, that's right, and that's certainly a beneficial lie. |
| 0:29:38.760 | 1778.760 | CHIEF JUSTICE ROBERTS | valor | It seems to me that the Stolen Valor Act is more narrow than that. |
| 0:30:03.920 | 1803.920 | MR. LIBBY | valor | Well, perhaps, just dealing with an example under the Stolen Valor Act, if a grandfather were to make up a story that he had won a medal in order to persuade a grandchild to -- |
| 0:30:09.260 | 1809.260 | MR. LIBBY | medal | Well, perhaps, just dealing with an example under the Stolen Valor Act, if a grandfather were to make up a story that he had won a medal in order to persuade a grandchild to -- |
| 0:32:05.360 | 1925.360 | MR. LIBBY | lie | Whether it in fact causes that direct harm, there's still a significant risk of imminent harm resulting from telling a lie to a government investigator. |
| 0:33:42.560 | 2022.560 | JUSTICE KENNEDY | medal | Well, it's a matter -- it's a matter of common sense that it, it seems to me -- that it demeans the medal. |
| 0:33:49.320 | 2029.320 | JUSTICE KENNEDY | medal | Let me ask you this: What do you do with the statute that prohibits the wearing of a medal that has not been earned? |
| 0:33:52.280 | 2032.280 | MR. LIBBY | medal | Wearing medals is a slightly different category because there you're dealing with conduct rather than content. |
| 0:34:19.140 | 2059.140 | MR. LIBBY | medal | It may be or it may be in doubt under certain situations where one is wearing a medal. |
| 0:34:25.995 | 2065.995 | MR. LIBBY | medal | But certainly Congress has an interest in protecting non-expressive purposes of wearing the medals. |
| 0:34:31.240 | 2071.240 | JUSTICE KENNEDY | medal | But I think it is, if the whole purpose of the person who puts the medal on his tuxedo that he didn't earn is an expressive purpose. |
| 0:34:53.500 | 2093.500 | JUSTICE GINSBURG | medal | You wear the medal and you're saying I am a Medal of Honor winner. |
| 0:34:56.140 | 2096.140 | JUSTICE GINSBURG | Medal of Honor | You wear the medal and you're saying I am a Medal of Honor winner. |
| 0:35:30.360 | 2130.360 | JUSTICE GINSBURG | medal | Where you go out in the street with the -- with the medal on you for everybody to see. |
| 0:35:42.620 | 2142.620 | MR. LIBBY | medal | If -- if there's -- if Congress does not have a non-speech purpose for prohibiting the wearing of the medals, then if it's strictly an expressive purpose, then, yes, there would be a significant First Amendment problem. |
| 0:37:55.700 | 2275.700 | MR. LIBBY | lie | Well, when one lies to a government investigator, presumably you're doing it in order to send them in the wrong direction, even if it doesn't do that. |
| 0:39:04.740 | 2344.740 | MR. LIBBY | medal | I mean, it's -- we certainly concede that one typically knows whether or not one has won a medal or not. |
| 0:40:02.250 | 2402.250 | JUSTICE GINSBURG | lie | It's just a bald-faced lie. |
| 0:43:06.920 | 2586.920 | JUSTICE SOTOMAYOR | medal | So, why isn't the outrage that medal winners, legitimately entitled medal winners, experience in seeing fake people or hearing fake people claim a medal -- why isn't that comparable? |
| 0:44:04.300 | 2644.300 | MR. LIBBY | Alvarez | Now, what the Government has suggested is that there's no harm that really results from a single claim, that Mr. Alvarez's falsehood did not cause harm to any individual. |
| 0:45:02.000 | 2702.000 | JUSTICE BREYER | medal | Because, after all, we're willing to protect the Olympics Committee when a false person saying he's the Olympics Committee might deprive the Olympics Committee of a penny, while here they're saying that to win this great medal, say, the congressional Medal of Honor, the highest award in the military the nation can give, you're deserving of the most possible, grandest possible respect, and we don't -- we don't even want you to have to think about somebody having taken that name falsely; and so, we will just criminalize it to discourage such activity that undermines the very thought and purpose of giving the medal. |
| 0:45:03.380 | 2703.380 | JUSTICE BREYER | Congressional | Because, after all, we're willing to protect the Olympics Committee when a false person saying he's the Olympics Committee might deprive the Olympics Committee of a penny, while here they're saying that to win this great medal, say, the congressional Medal of Honor, the highest award in the military the nation can give, you're deserving of the most possible, grandest possible respect, and we don't -- we don't even want you to have to think about somebody having taken that name falsely; and so, we will just criminalize it to discourage such activity that undermines the very thought and purpose of giving the medal. |
| 0:45:03.880 | 2703.880 | JUSTICE BREYER | Medal of Honor | Because, after all, we're willing to protect the Olympics Committee when a false person saying he's the Olympics Committee might deprive the Olympics Committee of a penny, while here they're saying that to win this great medal, say, the congressional Medal of Honor, the highest award in the military the nation can give, you're deserving of the most possible, grandest possible respect, and we don't -- we don't even want you to have to think about somebody having taken that name falsely; and so, we will just criminalize it to discourage such activity that undermines the very thought and purpose of giving the medal. |
| 0:46:13.520 | 2773.520 | MR. LIBBY | lie | If someone tells a lie about having received an honor, there's time for them to be exposed. |
| 0:46:32.740 | 2792.740 | JUSTICE SCALIA | lie | You know, when there's a sanction in place, you think twice before you tell the lie. |
| 0:46:43.280 | 2803.280 | JUSTICE SCALIA | lie | That sanction already exists, and there are a lot of people nonetheless who tell the lie. |
| 0:47:31.000 | 2851.000 | JUSTICE BREYER | lying | Is there anything else -- that the threat of criminal prosecution might discourage from lying who would never be caught. |
| 0:47:58.620 | 2878.620 | JUSTICE BREYER | medal | My theory is that it does hurt the medal, the purpose, the objective, the honor, for people falsely to go around saying that they have this medal when they don't. |
| 0:48:30.300 | 2910.300 | MR. LIBBY | Congressional | There was a congressional hearing that suggested that the military has been a little lax in identifying true heroes and awarding them medals. |
| 0:48:36.540 | 2916.540 | MR. LIBBY | medal | There was a congressional hearing that suggested that the military has been a little lax in identifying true heroes and awarding them medals. |
| 0:48:51.500 | 2931.500 | JUSTICE SCALIA | medal | How about giving a medal of shame to those who have falsely claimed to have earned the medal of valor? |
| 0:48:52.000 | 2932.000 | JUSTICE SCALIA | shame | How about giving a medal of shame to those who have falsely claimed to have earned the medal of valor? |
| 0:48:56.700 | 2936.700 | JUSTICE SCALIA | valor | How about giving a medal of shame to those who have falsely claimed to have earned the medal of valor? |
| 0:49:11.160 | 2951.160 | CHIEF JUSTICE ROBERTS | medal | I mean, it -- I mean, it's still a sanction for telling something that you say is protected under the First Amendment, whether you get 6 months or a medal of shame doesn't matter under your theory. |
| 0:49:11.420 | 2951.420 | CHIEF JUSTICE ROBERTS | shame | I mean, it -- I mean, it's still a sanction for telling something that you say is protected under the First Amendment, whether you get 6 months or a medal of shame doesn't matter under your theory. |
| 0:49:24.400 | 2964.400 | MR. LIBBY | liar | Well, there is a significant difference between a criminal sanction that puts someone in prison versus simply exposing them for what they are, which is a liar. |
| 0:49:26.740 | 2966.740 | MR. LIBBY | Alvarez | And Mr. Alvarez -- whether or not he in fact was sentenced to a crime, he still was exposed for who he was, which was a liar. |
| 0:49:35.740 | 2975.740 | MR. LIBBY | liar | And Mr. Alvarez -- whether or not he in fact was sentenced to a crime, he still was exposed for who he was, which was a liar. |
| 0:50:06.480 | 3006.480 | JUSTICE GINSBURG | Alvarez | Is that -- is that -- that wouldn't reach Alvarez because he didn't obtain anything of value. |
| 0:50:13.560 | 3013.560 | MR. LIBBY | Alvarez | What we do know is that Mr. Alvarez did not obtain a thing of value. |
| 0:50:23.060 | 3023.060 | CHIEF JUSTICE ROBERTS | medal | He was involved -- well, doesn't it help a politician to have a congressional Medal of Honor? |
| 0:50:23.060 | 3023.060 | CHIEF JUSTICE ROBERTS | Medal of Honor | He was involved -- well, doesn't it help a politician to have a congressional Medal of Honor? |
| 0:50:23.060 | 3023.060 | CHIEF JUSTICE ROBERTS | Congressional | He was involved -- well, doesn't it help a politician to have a congressional Medal of Honor? |
| 0:50:47.140 | 3047.140 | CHIEF JUSTICE ROBERTS | lie | But it seems to me that your willingness to say that this statute is valid so long as there's some benefit to the person who lies, it's an awfully big concession. |
| 0:52:24.980 | 3144.980 | JUSTICE SCALIA | Congressional | I'm a congressional Medal of -- the crowd cheers, and they give him a parade down Main Street. |
| 0:52:25.360 | 3145.360 | JUSTICE SCALIA | medal | I'm a congressional Medal of -- the crowd cheers, and they give him a parade down Main Street. |
| 0:52:59.380 | 3179.380 | JUSTICE ALITO | date | Suppose what the person gets is -- is a date with a potential rich spouse. |
| 0:53:10.760 | 3190.760 | MR. LIBBY | date | Your Honor, I think when it comes -- when you get into the situation where you're getting something like a date, I do not know that -- I certainly wouldn't consider that a non-de minimis thing of value. |
| 0:56:32.620 | 3392.620 | JUSTICE KAGAN | lie | The government has a strong interest in the sanctity of the family, the stability of the family; so, we're going to prevent everybody from telling lies about their extramarital affairs. |
| 0:58:11.420 | 3491.420 | JUSTICE SOTOMAYOR | lie | So, in that lie in that context, you can't sanction, but you can sanction that lie in a different context. |
| 0:58:21.660 | 3501.660 | JUSTICE SOTOMAYOR | date | On a date. |
| 0:58:24.080 | 3504.080 | JUSTICE SOTOMAYOR | date | I don't know because, on a date, it doesn't chill political speech, and it will induce a young woman to date someone who she thinks is more of a professional, because that harms the parents, it harms the family. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.220 to 0:03:08.220, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.220] GENERAL VERRILLI: Mr. Chief Justice, and may it please the Court: Military honors play a vital role in inculcating and sustaining the core values of our nation's armed forces. The military applies exacting criteria in awarding honors, and Congress has a long tradition of legislating to protect the integrity of the honors system. The Stolen Valor Act continues that tradition by prohibiting knowingly false statements that one has been awarded a military honor. It regulates a carefully limited and narrowly drawn category of calculated factual falsehoods. It advances a legitimate substantial, and, indeed, compelling governmental interest, and it chills no protected speech. This Court has recognized --

[0:00:56.100] JUSTICE SOTOMAYOR: General, may I pose a hypothetical? During the Vietnam War, a protester holds up a sign that says I won a Purple Heart -- for killing babies. Knowing statement. He didn't win the Purple Heart. As a reader, I can't be sure whether he did and is a combat veteran who opposes the war or whether he's a citizen protesting the war. Is that person -- if he's not a veteran having received a medal, is he liable under this Act?

[0:01:34.000] GENERAL VERRILLI: I think, Your Honor, it would depend on whether that was -- that expression was reasonably understood by the audience as a statement of fact or as an exercise in political theater. If it's the latter, it's not within the scope of the statute --

[0:01:49.380] JUSTICE SOTOMAYOR: Somewhat dangerous, isn't it --

[0:01:49.400] GENERAL VERRILLI: -- and it wouldn't be subject to liability.

[0:01:51.560] JUSTICE SOTOMAYOR: -- to subject speech to the absolute rule of no protection? Which is what you're advocating, I understand.

[0:02:01.680] GENERAL VERRILLI: Well, Your Honor --

[0:02:02.160] JUSTICE SOTOMAYOR: That there are no circumstances in which this speech has value. I -- I believe that's your bottom line.

[0:02:07.980] GENERAL VERRILLI: Well, what -- what I would say with respect to that, Your Honor, is that this Court has said in numerous contexts, numerous contexts, that the calculated factual falsehood has no First Amendment value for its own sake.

[0:02:20.440] JUSTICE SOTOMAYOR: Well, that's not --

[0:02:20.610] JUSTICE KENNEDY: Well, I'm -- I'm not sure that that's quite correct. It has said it often but always in context where it is well understood that speech can injure. Defamation, Gertz -- page 12 of your brief, you make this point, and it's what Justice Sotomayor is indicating. You think there's no value to falsity. But I -- I simply can't find that in our cases, and I -- I think it's a sweeping proposition to say that there's no value to falsity. Falsity is a way in which we contrast what is false and what is true.

[0:02:59.060] GENERAL VERRILLI: I want to be --

[0:02:59.580] JUSTICE KENNEDY: And --

[0:02:59.760] GENERAL VERRILLI: I want to respond with precision, Justice Kennedy, that the -- I think what this Court -- and Gertz is a good example -- has done

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 28, 2012.

- Oyez page: https://www.oyez.org/cases/2011/11-210
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2011/11-210/20120628o_11-210.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.5 MB)
- Length: 0:05:47.716 (347.716 s)
- Words: 912, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 876 of Whisper's 912 words (96.1%; Oyez has 906).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.060 | 13 |
| JUSTICE KENNEDY | 0:00:06.400 | 0:05:46.880 | 894 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Kennedy has the announcement today in Case 11-210, United States v. Alvarez.

[0:00:06.400] JUSTICE KENNEDY: This is an opinion announcing the judgment of the Court in United States v. Alvarez. Lying was his habit. Javier Alvarez is the Respondent here. He lied when he said he played hockey for the Detroit Red Wings and that he once married a starlet from Mexico. But when he lied in announcing he held the Congressional Medal of Honor, Respondent ventured on to new ground. For that lie violates a Federal criminal statute, the Stolen Valor Act of 2005. Respondent was elected to the Three Valley Water District Board in California. At a board meeting, he introduced himself by claiming that he had been a Marine for 25 years, had been wounded in combat, and had won the Congressional Medal of Honor, and none of these statements were true. The Stolen Valor Act, the Federal statute, provides that whoever falsely claims to have won the Congressional Medal of Honor can be fined or imprisoned up for up to one year. Alvarez was convicted under the statute, but the United States Court of Appeals for the Ninth Circuit reversed, it found the statute invalid under the First Amendment. After we granted certiorari, the United States Court of Appeals for the Tenth Circuit in an unrelated case found that the Act was constitutional, so now there is a conflict in the circuits. It's right and proper that Congress, over a century ago, established an award so the nation can hold in its highest respect and esteem those who, in performing the supreme and noble duty of contributing to the defense of the rights and honor of this nation, have acted with extraordinary valor. Fundamental constitutional principles, however, require that laws enacted to recognize the brave must be consistent with the precepts of the Constitution for which they fought. As a general matter, this Court has permitted content-based restrictions only when they are confined to one of the few historic and traditional categories of expression, defamation, obscenity and fraud, are among these few categories of punishable speech. Absent from those few categories where the law does allow content-based restrictions of speech is any general exception to the First Amendment for false statements. A Federal criminal statute does prohibit lying to a government official, but statutes of that sort are inapplicable here. This Court has not endorsed a categorical rule that false statements receive no First Amendment protection. By its plain terms, the Stolen Valor Act applies to speech made at any time, in any place, to any person. And it does so entirely without regard to whether the lie was made for the purpose of material gain. Permitting the government to decree this speech to be a criminal offense, whether shouted from the rooftops or

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:14.700 | Javier | Xavier |
| 0:00:44.740 | he had | he'd |
| 0:00:48.220 | had | who |
| 0:00:49.040 | (nothing) | Medal -- |
| 0:00:53.880 | the | a |
| 0:01:01.180 | up | (nothing) |
| 0:01:22.900 | there is | there's |
| 0:02:20.000 | content -based restrictions | content-based restriction |
| 0:02:21.420 | (nothing) | the |
| 0:02:35.100 | a | the |
| 0:03:00.700 | verily | barely |
| 0:03:28.480 | we have | we've |
| 0:03:39.260 | as it | with |
| 0:03:44.700 | (nothing) | -- of |
| 0:03:58.880 | (nothing) | "I |
| 0:04:07.300 | as | it's |
| 0:04:09.680 | are | were |
| 0:04:21.040 | the | (nothing) |
| 0:04:54.660 | imposter. | impostor. |
| 0:05:03.520 | if | of |
| 0:05:05.140 | reinforce | reenforce |
| 0:05:46.420 | join. | joined. |
