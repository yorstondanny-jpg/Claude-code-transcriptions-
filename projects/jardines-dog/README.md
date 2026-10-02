# jardines-dog: Supreme Court No. 11-564

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2012/11-564
- Audio: https://www.supremecourt.gov/media/audio/mp3files/11-564.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2012/11-564.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 45 min on 4 CPU cores
- Audio length: 1:01:40.323 (3700.323 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.6 MB
- Official words: 11957 (plus 0 `(Laughter.)` markers), in 342 speaker turns
- ASR words: 11676
- Official words matched to an ASR word: 11232 of 11957 (**93.94%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 93.94% (threshold 85%).

472 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 1 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 19 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 11-564 2012 jardines-dog --model medium.en --opinion --mentions "Girl Scout(s),trick-or-treat(er)(s),salesman/salesmen,dog,Franky,knock/knocker,porch,front door,cookie(s),leash,Halloween"

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| Girl Scout(s) | 5 | 5 |
| trick-or-treat(er)(s) | 3 | 3 |
| salesman/salesmen | 4 | 4 |
| dog | 144 | 169 |
| Franky | 7 | 7 |
| knock/knocker | 42 | 46 |
| porch | 6 | 6 |
| front door | 49 | 52 |
| cookie(s) | 2 | 2 |
| leash | 9 | 9 |
| Halloween | 0 | 0 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:13.620 | 13.620 | MR. GARRE | dog | Thank you, Mr. Chief Justice, and may it please the Court: In the three prior cases in which this Court has held that a dog sniff is not a search, this Court has emphasized that a dog sniff is unique, both in terms of the manner in which information is obtained and the nature of the information revealed. |
| 0:00:28.560 | 28.560 | MR. GARRE | dog | As to the latter point, this Court has emphasized that a drug detection dog reveals only the presence of contraband, and that no one has a legitimate expectation of privacy in that. |
| 0:01:09.000 | 69.000 | MR. GARRE | dog | Well, Justice Kennedy, in the Caballes case, the contraband wasn't visible before the dog alerted. |
| 0:02:00.740 | 120.740 | JUSTICE GINSBURG | dog | Mr. Garre, does your argument mean -- you say minimally intrusive, and that the dog will detect only contraband, that the police then are to go into a neighborhood that's known to be a drug dealing neighborhood, go into -- just go down the street, have the dog sniff in front of every door, or go into an apartment building? |
| 0:02:29.020 | 149.020 | MR. GARRE | knock/knocker | Your Honor, they could do that, just like the police could go door to door and then knock on the doors and hope that they will find out evidence of wrongdoing that way. |
| 0:02:57.040 | 177.040 | JUSTICE GINSBURG | dog | Suppose -- suppose the house had on the lawn, no dogs allowed? |
| 0:03:09.040 | 189.040 | MR. GARRE | front door | Homeowners can restrict access to people who come up to their front door by putting gates or a sign out front. |
| 0:03:43.140 | 223.140 | JUSTICE SCALIA | dog | Why isn't it the same thing with the dog? |
| 0:03:43.600 | 223.600 | JUSTICE SCALIA | dog | This dog was brought right up -- right up to the -- to the door of the house. |
| 0:03:53.340 | 233.340 | MR. GARRE | front door | Your Honor, first of all, I think that, as this case comes to the Court, the police were lawfully present at the front door. |
| 0:04:02.200 | 242.200 | MR. GARRE | front door | The police officer could go up to the front door and knock and detect the smell of marijuana, just like Officer Pedraja did. |
| 0:04:03.160 | 243.160 | MR. GARRE | knock/knocker | The police officer could go up to the front door and knock and detect the smell of marijuana, just like Officer Pedraja did. |
| 0:04:47.600 | 287.600 | MR. GARRE | salesman/salesmen | It's well established, we think, going back to the common law, that there is an implied consent for people, visitors, salesmen, Girl Scouts, trick-or-treaters, to come up to your house and knock on the door -- |
| 0:04:48.160 | 288.160 | MR. GARRE | Girl Scout(s) | It's well established, we think, going back to the common law, that there is an implied consent for people, visitors, salesmen, Girl Scouts, trick-or-treaters, to come up to your house and knock on the door -- |
| 0:04:48.740 | 288.740 | MR. GARRE | trick-or-treat(er)(s) | It's well established, we think, going back to the common law, that there is an implied consent for people, visitors, salesmen, Girl Scouts, trick-or-treaters, to come up to your house and knock on the door -- |
| 0:04:50.200 | 290.200 | MR. GARRE | knock/knocker | It's well established, we think, going back to the common law, that there is an implied consent for people, visitors, salesmen, Girl Scouts, trick-or-treaters, to come up to your house and knock on the door -- |
| 0:04:54.380 | 294.380 | JUSTICE GINSBURG | dog | Yes, but not implied consent for the policeman to come up with the dog. |
| 0:04:56.880 | 296.880 | JUSTICE GINSBURG | dog | The only purpose of the dog is to detect contraband. |
| 0:05:04.440 | 304.440 | JUSTICE GINSBURG | Girl Scout(s) | So you can say, yes, there's an implied invitation to the Girl Scout cookie seller, to the postman, even to the police officer, but not police officer with dog, when the only reason for having the dog is to find out if there's contraband in the house. |
| 0:05:05.020 | 305.020 | JUSTICE GINSBURG | cookie(s) | So you can say, yes, there's an implied invitation to the Girl Scout cookie seller, to the postman, even to the police officer, but not police officer with dog, when the only reason for having the dog is to find out if there's contraband in the house. |
| 0:05:12.420 | 312.420 | JUSTICE GINSBURG | dog | So you can say, yes, there's an implied invitation to the Girl Scout cookie seller, to the postman, even to the police officer, but not police officer with dog, when the only reason for having the dog is to find out if there's contraband in the house. |
| 0:05:20.860 | 320.860 | MR. GARRE | Girl Scout(s) | Well, Justice Ginsburg, first of all, I think, if the Girl Scout or the salesman or the trick-or-treater brought up a dog with them, there would be complied consent for that too, at least as long as the dog was on a leash. |
| 0:05:21.780 | 321.780 | MR. GARRE | salesman/salesmen | Well, Justice Ginsburg, first of all, I think, if the Girl Scout or the salesman or the trick-or-treater brought up a dog with them, there would be complied consent for that too, at least as long as the dog was on a leash. |
| 0:05:23.000 | 323.000 | MR. GARRE | trick-or-treat(er)(s) | Well, Justice Ginsburg, first of all, I think, if the Girl Scout or the salesman or the trick-or-treater brought up a dog with them, there would be complied consent for that too, at least as long as the dog was on a leash. |
| 0:05:24.000 | 324.000 | MR. GARRE | dog | Well, Justice Ginsburg, first of all, I think, if the Girl Scout or the salesman or the trick-or-treater brought up a dog with them, there would be complied consent for that too, at least as long as the dog was on a leash. |
| 0:05:28.440 | 328.440 | MR. GARRE | leash | Well, Justice Ginsburg, first of all, I think, if the Girl Scout or the salesman or the trick-or-treater brought up a dog with them, there would be complied consent for that too, at least as long as the dog was on a leash. |
| 0:05:30.300 | 330.300 | JUSTICE GINSBURG | dog | This is not any dog. |
| 0:05:32.120 | 332.120 | JUSTICE GINSBURG | dog | This is a drug detecting dog. |
| 0:05:37.040 | 337.040 | MR. GARRE | dog | But I don't think it changes the subjective purpose of why they brought the dog with them. |
| 0:05:46.800 | 346.800 | JUSTICE SOTOMAYOR | dog | At least in the cities that I've lived in, you have to have a dog on a leash. |
| 0:05:47.240 | 347.240 | JUSTICE SOTOMAYOR | leash | At least in the cities that I've lived in, you have to have a dog on a leash. |
| 0:05:53.760 | 353.760 | JUSTICE SOTOMAYOR | dog | If you're allergic to animals, you don't want dogs walking around at your door. |
| 0:05:57.620 | 357.620 | MR. GARRE | dog | Well, you can certainly put the "No Dogs Allowed" sign out front. |
| 0:06:08.260 | 368.260 | JUSTICE SOTOMAYOR | dog | Do you think homeowners freely let dogs just come into their apartment? |
| 0:06:15.840 | 375.840 | MR. GARRE | dog | This search took place, the dog walked up the same way that a salesman would and alerted at the front of the door. |
| 0:06:17.500 | 377.500 | MR. GARRE | salesman/salesmen | This search took place, the dog walked up the same way that a salesman would and alerted at the front of the door. |
| 0:06:23.460 | 383.460 | JUSTICE SOTOMAYOR | knock/knocker | You're invited to knock on my door because you're a dog? |
| 0:06:24.505 | 384.505 | JUSTICE SOTOMAYOR | dog | You're invited to knock on my door because you're a dog? |
| 0:06:28.400 | 388.400 | MR. GARRE | dog | No, I think -- and certainly this is true in my neighborhood, Your Honor, is neighbors can bring their dog up on the leash when they knock on your front door, and I think that's true in most neighborhoods in America. |
| 0:06:29.180 | 389.180 | MR. GARRE | leash | No, I think -- and certainly this is true in my neighborhood, Your Honor, is neighbors can bring their dog up on the leash when they knock on your front door, and I think that's true in most neighborhoods in America. |
| 0:06:29.580 | 389.580 | MR. GARRE | knock/knocker | No, I think -- and certainly this is true in my neighborhood, Your Honor, is neighbors can bring their dog up on the leash when they knock on your front door, and I think that's true in most neighborhoods in America. |
| 0:06:30.060 | 390.060 | MR. GARRE | front door | No, I think -- and certainly this is true in my neighborhood, Your Honor, is neighbors can bring their dog up on the leash when they knock on your front door, and I think that's true in most neighborhoods in America. |
| 0:06:34.180 | 394.180 | MR. GARRE | dog | Homeowners that don't like dogs and want them off their property have a way to combat that, and that's putting a fence around it to say, no dogs -- |
| 0:06:42.080 | 402.080 | JUSTICE SOTOMAYOR | dog | -- all the drug dealers, put up a sign that says "No dogs." |
| 0:06:52.640 | 412.640 | JUSTICE SOTOMAYOR | knock/knocker | I -- I let people knock on my door because they have to say something to me. |
| 0:06:56.920 | 416.920 | JUSTICE SOTOMAYOR | dog | I don't let a dog come up to my door -- I don't willy-nilly invite it to come up to my door. |
| 0:07:16.320 | 436.320 | MR. GARRE | knock/knocker | And I think -- Your Honor, I think the reason why that doesn't work here is that if you ask that question with respect to the officer, I think it's well settled or accepted that police officers can walk up the front path, absent a sign or something, knock on the door -- |
| 0:07:20.820 | 440.820 | JUSTICE SOTOMAYOR | porch | That implied consent, does that include them coming up and -- up to your porch and sweeping stuff into a garbage pan? |
| 0:07:29.060 | 449.060 | MR. GARRE | knock/knocker | I think that we're talking about going up there, knocking on the door. |
| 0:07:30.740 | 450.740 | JUSTICE SCALIA | knock/knocker | Police officers can come there to knock on the door, but I thought you've conceded that police officers can't come there to look into the house with binoculars, right? |
| 0:08:18.240 | 498.240 | JUSTICE BREYER | knock/knocker | You do expect people to come up and come into the house, knock on the door, maybe even with dogs. |
| 0:08:21.040 | 501.040 | JUSTICE BREYER | dog | You do expect people to come up and come into the house, knock on the door, maybe even with dogs. |
| 0:08:28.080 | 508.080 | JUSTICE BREYER | knock/knocker | Do you expect them to sit there for 5 to 15 minutes, 15 minutes, not knocking on the door, doing nothing? |
| 0:08:37.780 | 517.780 | JUSTICE BREYER | knock/knocker | Anyone coming to your door and not knocking. |
| 0:09:48.600 | 588.600 | MR. GARRE | dog | Your Honor, what I think you can say there is implied consent to is a dog accompanying a person on a leash walking up to the front door, taking a sniff in a matter of seconds, not minutes -- |
| 0:09:50.920 | 590.920 | MR. GARRE | leash | Your Honor, what I think you can say there is implied consent to is a dog accompanying a person on a leash walking up to the front door, taking a sniff in a matter of seconds, not minutes -- |
| 0:09:51.880 | 591.880 | MR. GARRE | front door | Your Honor, what I think you can say there is implied consent to is a dog accompanying a person on a leash walking up to the front door, taking a sniff in a matter of seconds, not minutes -- |
| 0:10:01.100 | 601.100 | JUSTICE KAGAN | dog | I mean, the record suggests that he put the dog on a very long leash, the dog goes back and forth, tries to figure out where the smell is coming from. |
| 0:10:02.340 | 602.340 | JUSTICE KAGAN | leash | I mean, the record suggests that he put the dog on a very long leash, the dog goes back and forth, tries to figure out where the smell is coming from. |
| 0:10:12.160 | 612.160 | JUSTICE KAGAN | dog | It's not just -- you know, my first thought was you go up to the door, the dog barks once, and that's it. |
| 0:10:15.540 | 615.540 | JUSTICE KAGAN | dog | But you read the record, this dog is there for some extended period of time, going back and forth and back and forth, trying to figure out where the greatest concentration of the smell is. |
| 0:10:31.620 | 631.620 | MR. GARRE | dog | Your Honor, I think what the record shows is, is that the dog was on the scene, i.e., at the curb, walking up, going back into the car, and then leaving, for a total of 5 to 10 minutes. |
| 0:10:45.800 | 645.800 | MR. GARRE | dog | It's not -- the dog isn't up there for 5 to 10 minutes. |
| 0:11:37.260 | 697.260 | MR. GARRE | dog | And so what you're talking about, although we talk about what's going on in the home, really what's happening here is odor of illegal contraband is being blown out into the street and someone is coming up to it and using their God-given senses in a way that humans and dogs have used for centuries and detecting that. |
| 0:11:50.920 | 710.920 | CHIEF JUSTICE ROBERTS | dog | I understood the issue before us to be whether or not under the Fourth Amendment it is a search for a dog to come up to the door and sniff, not with respect to -- we're not making a judgment, I thought, on the probable cause in light of the totality of the circumstances, but the ground of decision below was this is a search when the dog sniffs. |
| 0:12:04.840 | 724.840 | MR. GARRE | dog | That you need probable cause just for the dog to sniff. |
| 0:12:07.180 | 727.180 | MR. GARRE | dog | And the dog sniff itself clearly is not a physical invasion in the same way that looking is not a physical invasion under the common law. |
| 0:12:13.900 | 733.900 | MR. GARRE | dog | And the dog, we think -- |
| 0:12:22.060 | 742.060 | JUSTICE SCALIA | front door | It's the sniffing at this point, the sniffing at a person's front door, right? |
| 0:12:32.860 | 752.860 | MR. GARRE | Franky | Well, that's true, Your Honor, but I think if it wasn't a search for the police officer to walk up there and sniff and report smelling live marijuana, then it wasn't a search when Franky walked up there and alerted to the presence of an illegal narcotic. |
| 0:12:55.080 | 775.080 | MR. GARRE | knock/knocker | I think it's been conceded in this case, at least it was below, that the officer could walk up there, knock on the door, report the smell of marijuana, and that that was not a search. |
| 0:13:29.420 | 809.420 | MR. GARRE | Franky | Well, first of all, Franky's nose is not technology. |
| 0:13:34.480 | 814.480 | MR. GARRE | dog | It's -- he's using -- he's availing himself of God-given senses in the way that dogs have helped mankind for centuries. |
| 0:13:50.000 | 830.000 | JUSTICE KAGAN | dog | So does that mean that if we invented some kind of little machine called a, you know, smell-o-matic and the police officer had this smell-o-matic machine, and it alerted to the exact same things that a dog alerts to, it alerted to a set of drugs, meth and marijuana and whatever else, the police officer could not come to the front door and use that machine? |
| 0:14:00.060 | 840.060 | JUSTICE KAGAN | front door | So does that mean that if we invented some kind of little machine called a, you know, smell-o-matic and the police officer had this smell-o-matic machine, and it alerted to the exact same things that a dog alerts to, it alerted to a set of drugs, meth and marijuana and whatever else, the police officer could not come to the front door and use that machine? |
| 0:14:15.640 | 855.640 | MR. GARRE | dog | And I think that's an important distinction because, as we read Kyllo, the Court was very concerned about advances in technology, and that's just not true for a dog's nose. |
| 0:14:20.160 | 860.160 | JUSTICE KAGAN | Franky | So your basic distinction is the difference between like a machine and Franky. |
| 0:14:22.840 | 862.840 | JUSTICE KAGAN | Franky | That we should not understand Franky as kind of a sense-enhancing law enforcement technology, but we should think of him as just like a guy. |
| 0:14:34.420 | 874.420 | MR. GARRE | Franky | One is Franky is using the same sense of smell that dogs have used for centuries. |
| 0:14:37.140 | 877.140 | MR. GARRE | dog | One is Franky is using the same sense of smell that dogs have used for centuries. |
| 0:14:41.000 | 881.000 | MR. GARRE | dog | So this isn't a case where if you allow a dog to sniff today, he might use x-ray vision in the future. |
| 0:14:45.720 | 885.720 | MR. GARRE | Franky | And the other thing is that Franky -- that the use of dogs for their sense of smell, which everyone agrees is extraordinary, mankind has been using them for law enforcement type purposes for centuries. |
| 0:14:47.620 | 887.620 | MR. GARRE | dog | And the other thing is that Franky -- that the use of dogs for their sense of smell, which everyone agrees is extraordinary, mankind has been using them for law enforcement type purposes for centuries. |
| 0:15:01.720 | 901.720 | JUSTICE GINSBURG | dog | You said centuries, but I think you recognize that it wasn't until the seventies when the dogs were used to find culprits. |
| 0:15:13.500 | 913.500 | MR. GARRE | dog | But they've -- we've been using dogs to track thieves for centuries going back before the founding. |
| 0:15:19.360 | 919.360 | MR. GARRE | dog | Scotland Yard -- Scotland Yard used dogs to track Jack the Ripper. |
| 0:15:30.800 | 930.800 | JUSTICE SOTOMAYOR | dog | Mr. Garre, there's no dispute that dogs can smell what human beings can't; is that correct? |
| 0:15:41.900 | 941.900 | JUSTICE SOTOMAYOR | dog | It's not that we can find a machine to put it on a human being to enhance their sense of smells; dogs can do something human beings can't. |
| 0:16:03.820 | 963.820 | MR. GARRE | dog | He's -- the dogs, no doubt, have an enhanced sense of smell compared to the officer. |
| 0:16:25.680 | 985.680 | MR. GARRE | dog | Here, you're using the drug detection dog to smell the odor of marijuana that is being pumped out of the house into the street. |
| 0:17:05.780 | 1025.780 | MR. GARRE | dog | And I think, here, one way to resolve it is to say people who live in grow houses with a distinct odor of marijuana, who know that that is being pumped out into the street because of the air conditioning that they need to run the grow houses, there is no invasion in their -- in their expectation of privacy when either a man or a dog, when lawfully present on the property, uses their God-given senses to detect that. |
| 0:17:39.540 | 1059.540 | MS. SAHARSKY | dog | The first is the question of whether the officer and the dog were lawfully in place, whether they could approach the front door, was conceded below. |
| 0:17:42.000 | 1062.000 | MS. SAHARSKY | front door | The first is the question of whether the officer and the dog were lawfully in place, whether they could approach the front door, was conceded below. |
| 0:17:55.380 | 1075.380 | JUSTICE GINSBURG | dog | I didn't -- I didn't understand the concession to be that the police had come to the door with the dog, the sole purpose of the dog being to detect contraband. |
| 0:18:07.740 | 1087.740 | MS. SAHARSKY | dog | The court of appeals, the Florida Court of Appeals, found that the dog and the officer were lawfully in place. |
| 0:18:21.540 | 1101.540 | MS. SAHARSKY | porch | Before the Florida Supreme Court at oral argument, Respondent conceded that there was no reasonable expectation of privacy in the porch, and the Florida Supreme Court accepted that concession. |
| 0:18:33.820 | 1113.820 | MS. SAHARSKY | front door | In the brief in opposition to cert, Respondent said that the police could approach the front door for a knock and talk, and made no separate argument about the dog's presence there making it not lawful. |
| 0:18:34.480 | 1114.480 | MS. SAHARSKY | knock/knocker | In the brief in opposition to cert, Respondent said that the police could approach the front door for a knock and talk, and made no separate argument about the dog's presence there making it not lawful. |
| 0:18:37.160 | 1117.160 | MS. SAHARSKY | dog | In the brief in opposition to cert, Respondent said that the police could approach the front door for a knock and talk, and made no separate argument about the dog's presence there making it not lawful. |
| 0:18:41.740 | 1121.740 | MS. SAHARSKY | dog | So as this case comes to the Court, it is with the dog and the officer lawfully in place at the front door, approaching the front door just like any Girl Scout, trick-or-treater, or anyone else could. |
| 0:18:44.440 | 1124.440 | MS. SAHARSKY | front door | So as this case comes to the Court, it is with the dog and the officer lawfully in place at the front door, approaching the front door just like any Girl Scout, trick-or-treater, or anyone else could. |
| 0:18:46.680 | 1126.680 | MS. SAHARSKY | Girl Scout(s) | So as this case comes to the Court, it is with the dog and the officer lawfully in place at the front door, approaching the front door just like any Girl Scout, trick-or-treater, or anyone else could. |
| 0:18:47.160 | 1127.160 | MS. SAHARSKY | trick-or-treat(er)(s) | So as this case comes to the Court, it is with the dog and the officer lawfully in place at the front door, approaching the front door just like any Girl Scout, trick-or-treater, or anyone else could. |
| 0:18:55.320 | 1135.320 | MS. SAHARSKY | front door | And just to respond, Justice Ginsburg, to the questions that you raised, the police officer's purpose in approaching the front door does not mean that the officer can't come to the door. |
| 0:19:11.940 | 1151.940 | JUSTICE GINSBURG | dog | You're agreeing with Mr. Garre that the police could take a dog and go down every house on the street, every apartment in the building? |
| 0:19:22.180 | 1162.180 | MS. SAHARSKY | dog | Well, assuming that the police can lawfully be in the place that they are going with the dog, which is conceded here -- |
| 0:19:26.160 | 1166.160 | MS. SAHARSKY | front door | If they are approaching the front door using the normal path, because the dog only detects contraband, yes, they could be used in those circumstances, but that's not happening. |
| 0:19:28.460 | 1168.460 | MS. SAHARSKY | dog | If they are approaching the front door using the normal path, because the dog only detects contraband, yes, they could be used in those circumstances, but that's not happening. |
| 0:20:06.820 | 1206.820 | JUSTICE GINSBURG | dog | They have not dealt with the dog sniff in the context of a home that's not seized. |
| 0:20:23.800 | 1223.800 | MS. SAHARSKY | dog | But in Caballes, where admittedly the Court did not decide this specific issue, it distinguished the case of Kyllo as saying that that was finding out about lawful activity in the home, and that a person -- the critical distinction between Kyllo and the dog sniff in Caballes is that a person does not have a reasonable expectation of privacy in contraband. |
| 0:22:17.680 | 1337.680 | MS. SAHARSKY | dog | All the dog sniff allows is for the police to try to go to a magistrate and establish probable cause to get a warrant. |
| 0:24:43.620 | 1483.620 | MS. SAHARSKY | dog | And just to be clear, the question about whether folks have a reasonable expectation of privacy with respect to contraband in their house has to take into account two facts: First, that we're only talking about contraband; but, also, that dogs have been used and known for centuries for their sense of smell. |
| 0:24:52.120 | 1492.120 | JUSTICE BREYER | dog | Yes, but I -- what I'm curious about, and it's an unanswered question for me, is we are considering whether the dog sniff is permissible, so I wanted to know what a dog sniff at the front door involves. |
| 0:24:57.180 | 1497.180 | JUSTICE BREYER | front door | Yes, but I -- what I'm curious about, and it's an unanswered question for me, is we are considering whether the dog sniff is permissible, so I wanted to know what a dog sniff at the front door involves. |
| 0:25:14.440 | 1514.440 | JUSTICE BREYER | dog | The officer, the dog officer, said he was in a rush that day and it didn't take more than 5 to 10 minutes. |
| 0:25:31.640 | 1531.640 | JUSTICE BREYER | knock/knocker | And my question really is whether an ordinary homeowner expects people to walk down the curtilage and, with a big animal, and the animal -- they don't knock. |
| 0:25:58.160 | 1558.160 | MS. SAHARSKY | dog | I think the 5 to 10 minutes, like counsel said, was the whole process of -- of bringing the dog up to the door, et cetera. |
| 0:26:01.340 | 1561.340 | MS. SAHARSKY | dog | But putting that to the side, what the dog is doing is sniffing things that have been exposed to the public from inside the house, smells that the officer himself could smell, could smell in -- in plain smell. |
| 0:26:13.540 | 1573.540 | MS. SAHARSKY | dog | And the Court has said in other cases, like in Place, that what the dog is doing is very limited in scope; it happens very quickly; there is no physical invasion; it's something that actually this Court has said in Florida v. Royer is something that we want officers to do, because it -- |
| 0:26:28.440 | 1588.440 | CHIEF JUSTICE ROBERTS | dog | Does the dog, as soon as he or she is at the door, sniff and sit or sniff and not sit, or does the dog -- I mean, you've talked about the sniff is immediate. |
| 0:26:47.100 | 1607.100 | MS. SAHARSKY | dog | The -- the dog sniff I think took seconds or maybe a minute or 2 minutes -- |
| 0:26:57.720 | 1617.720 | MS. SAHARSKY | dog | That they were -- that they met at the front gate, that they were walking up to the -- to the door, that the dog did the sniff, that the -- that he talked to the other officer, and then he went back to his car, which was parked I think some -- some length of time away. |
| 0:27:10.880 | 1630.880 | CHIEF JUSTICE ROBERTS | dog | So the officer walks to the door, the dog sniffs right away and then? |
| 0:27:13.560 | 1633.560 | MS. SAHARSKY | dog | Well, the dog sniffs. |
| 0:27:54.980 | 1674.980 | MR. BLUMBERG | dog | Mr. Chief Justice, and may it please the Court: Police officers taking a narcotics detection dog up to the front door of a house is a Fourth Amendment search for two distinct and separate reasons. |
| 0:27:55.960 | 1675.960 | MR. BLUMBERG | front door | Mr. Chief Justice, and may it please the Court: Police officers taking a narcotics detection dog up to the front door of a house is a Fourth Amendment search for two distinct and separate reasons. |
| 0:28:11.400 | 1691.400 | MR. BLUMBERG | dog | First, when police reveal any details inside a home which an individual seeks to keep private, that is a Fourth Amendment search and that is exactly what a narcotics detection dog is doing, revealing details in the home the individual seeks to keep private. |
| 0:31:11.860 | 1871.860 | MR. BLUMBERG | dog | There were mothballs there, and Detective Bartelt, the dog handler that was standing at the front door as well, testified without contradiction or without hesitation he didn't smell anything. |
| 0:31:13.720 | 1873.720 | MR. BLUMBERG | front door | There were mothballs there, and Detective Bartelt, the dog handler that was standing at the front door as well, testified without contradiction or without hesitation he didn't smell anything. |
| 0:33:23.160 | 2003.160 | MR. BLUMBERG | dog | Well, the -- when a police officer takes a narcotics detection dog up to the front door of the house, that is also a Fourth Amendment search because that is a physical trespass upon the constitutionally protected area of the curtilage of the home. |
| 0:33:24.040 | 2004.040 | MR. BLUMBERG | front door | Well, the -- when a police officer takes a narcotics detection dog up to the front door of the house, that is also a Fourth Amendment search because that is a physical trespass upon the constitutionally protected area of the curtilage of the home. |
| 0:33:43.080 | 2023.080 | JUSTICE ALITO | dog | Has there -- do you have a single case holding that it is a trespass for a person with a dog to walk up to the front door of a house? |
| 0:33:45.240 | 2025.240 | JUSTICE ALITO | front door | Has there -- do you have a single case holding that it is a trespass for a person with a dog to walk up to the front door of a house? |
| 0:33:56.220 | 2036.220 | MR. BLUMBERG | dog | Well, there are cases that go back to the -- I'm sorry, I don't have the, the citations -- but there are cases in the 1700s that established that basically a dog running on to someone else's property is a trespass. |
| 0:34:03.440 | 2043.440 | MR. BLUMBERG | dog | I thought your question was if a dog comes on to private property -- |
| 0:34:04.780 | 2044.780 | JUSTICE ALITO | dog | If a dog on a leash is brought up to the front door of a person's house, was that a trespass at the time when the Fourth Amendment was adopted? |
| 0:34:05.640 | 2045.640 | JUSTICE ALITO | leash | If a dog on a leash is brought up to the front door of a person's house, was that a trespass at the time when the Fourth Amendment was adopted? |
| 0:34:06.840 | 2046.840 | JUSTICE ALITO | front door | If a dog on a leash is brought up to the front door of a person's house, was that a trespass at the time when the Fourth Amendment was adopted? |
| 0:34:51.440 | 2091.440 | JUSTICE BREYER | dog | -- to protect a person with a dog coming up to the door and going (indicating), all right? |
| 0:35:19.340 | 2119.340 | JUSTICE BREYER | dog | He says, we go back to the 17th century, as far as you want, and there is no law that says there is any kind of expectation in a homeowner that a person won't walk up to the dog -- to the door with a dog on a leash and sniff, which, as he says -- which your opponents say is what happened here. |
| 0:35:21.320 | 2121.320 | JUSTICE BREYER | leash | He says, we go back to the 17th century, as far as you want, and there is no law that says there is any kind of expectation in a homeowner that a person won't walk up to the dog -- to the door with a dog on a leash and sniff, which, as he says -- which your opponents say is what happened here. |
| 0:35:59.080 | 2159.080 | JUSTICE GINSBURG | dog | The court said, the officer and the dog were lawfully present at the defendant's front door, and we were told that that was conceded by you a number of times. |
| 0:36:01.620 | 2161.620 | JUSTICE GINSBURG | front door | The court said, the officer and the dog were lawfully present at the defendant's front door, and we were told that that was conceded by you a number of times. |
| 0:36:16.780 | 2176.780 | MR. BLUMBERG | dog | What I -- what I said in the Florida Supreme Court, I was given a hypothet about an officer coming up by himself without the dog to knock on the front door and talk to the homeowner. |
| 0:36:17.760 | 2177.760 | MR. BLUMBERG | knock/knocker | What I -- what I said in the Florida Supreme Court, I was given a hypothet about an officer coming up by himself without the dog to knock on the front door and talk to the homeowner. |
| 0:36:18.360 | 2178.360 | MR. BLUMBERG | front door | What I -- what I said in the Florida Supreme Court, I was given a hypothet about an officer coming up by himself without the dog to knock on the front door and talk to the homeowner. |
| 0:36:33.180 | 2193.180 | MR. BLUMBERG | dog | And I said the dog. |
| 0:36:45.360 | 2205.360 | MR. BLUMBERG | knock/knocker | If the police officer is perform -- is knocking on the door, part of a knock and talk, yes; but, if the police -- |
| 0:36:53.060 | 2213.060 | JUSTICE KAGAN | dog | So the difference is the dog. |
| 0:36:54.880 | 2214.880 | JUSTICE KAGAN | dog | So what difference does the dog make? |
| 0:36:56.100 | 2216.100 | JUSTICE KAGAN | dog | Suppose the dog were not doing this ten-minute bracketing that Justice Breyer was talking about. |
| 0:37:03.420 | 2223.420 | JUSTICE KAGAN | dog | The dog comes up, takes a sniff, barks, sits down. |
| 0:37:09.200 | 2229.200 | JUSTICE KAGAN | dog | And, you know, to make it even more, the dog is not a scary-looking dog, the dog is a Cockapoo. |
| 0:37:27.100 | 2247.100 | MR. BLUMBERG | Franky | Well, whether it's a Cockapoo or Franky, who, from all the pictures, appears to be a very cute dog, it's not what the dog looks like, it's what the dog is doing on the front porch, which is -- |
| 0:37:29.500 | 2249.500 | MR. BLUMBERG | dog | Well, whether it's a Cockapoo or Franky, who, from all the pictures, appears to be a very cute dog, it's not what the dog looks like, it's what the dog is doing on the front porch, which is -- |
| 0:37:33.780 | 2253.780 | MR. BLUMBERG | porch | Well, whether it's a Cockapoo or Franky, who, from all the pictures, appears to be a very cute dog, it's not what the dog looks like, it's what the dog is doing on the front porch, which is -- |
| 0:37:33.840 | 2253.840 | JUSTICE KAGAN | dog | The dog does what your neighbor's dog does. |
| 0:37:36.500 | 2256.500 | MR. BLUMBERG | dog | Well, no, this dog -- the neighbor's dog does not search for evidence on your front porch. |
| 0:37:40.260 | 2260.260 | MR. BLUMBERG | porch | Well, no, this dog -- the neighbor's dog does not search for evidence on your front porch. |
| 0:37:52.620 | 2272.620 | JUSTICE SCALIA | dog | But, Mr. Blumberg, I think you're, with respect, misguided to concede that if it was just the officer alone without the dog, it would be perfectly okay. |
| 0:38:05.020 | 2285.020 | JUSTICE SCALIA | knock/knocker | And I would assume you would say that if the officer walks up there with no intention to knock and talk, but just walks up to the door with the intention of sniffing at the door, you would consider that to be a violation, wouldn't you? |
| 0:38:29.020 | 2309.020 | MR. BLUMBERG | front door | It depends what the officer does at the front door, not what his state of mind is. |
| 0:38:32.480 | 2312.480 | MR. BLUMBERG | front door | If the officer goes up to the front door and starts sniffing around the cracks and crevices -- |
| 0:38:38.440 | 2318.440 | CHIEF JUSTICE ROBERTS | front door | Yes, sure, if he's down on his knees; but, what if he goes up to the front door and sniffs? |
| 0:40:08.860 | 2408.860 | JUSTICE SCALIA | knock/knocker | The reason for the officer going onto protected property, if he's going on just to knock on the door to sell tickets to the Policeman's Ball, that's fine. |
| 0:40:51.520 | 2451.520 | MR. BLUMBERG | front door | This Court's decisions establish that a police officer does not have to close his eyes when he goes up to the front door of a house to do a knock and talk. |
| 0:40:52.740 | 2452.740 | MR. BLUMBERG | knock/knocker | This Court's decisions establish that a police officer does not have to close his eyes when he goes up to the front door of a house to do a knock and talk. |
| 0:41:03.320 | 2463.320 | MR. BLUMBERG | knock/knocker | Anything that he naturally observes using his ordinary senses when he is there for a lawful purpose such as a knock and talk is fine. |
| 0:41:12.440 | 2472.440 | CHIEF JUSTICE ROBERTS | dog | If the police go by with their dog intending to sniff, and the dog alerts, on the sidewalk but two feet away is the front door, that's okay, right? |
| 0:41:18.680 | 2478.680 | CHIEF JUSTICE ROBERTS | front door | If the police go by with their dog intending to sniff, and the dog alerts, on the sidewalk but two feet away is the front door, that's okay, right? |
| 0:41:27.720 | 2487.720 | MR. BLUMBERG | dog | No, it's not okay, respectfully, because the dog would still be revealing details inside the home that the officer could not reveal using his or her ordinary senses. |
| 0:41:42.040 | 2502.040 | CHIEF JUSTICE ROBERTS | dog | The policeman is walking down the sidewalk with his dog, the dog stops and alerts. |
| 0:41:54.900 | 2514.900 | CHIEF JUSTICE ROBERTS | dog | There's been no entry onto the property, just a policeman walking with his dog. |
| 0:42:00.540 | 2520.540 | MR. BLUMBERG | dog | Well, but I assume on your hypothet it's a policeman walking with his narcotics detection dog up and down the street. |
| 0:42:02.640 | 2522.640 | MR. BLUMBERG | dog | A dog that he knows is trained -- |
| 0:42:04.580 | 2524.580 | CHIEF JUSTICE ROBERTS | dog | He's walking the dog. |
| 0:42:08.760 | 2528.760 | CHIEF JUSTICE ROBERTS | dog | He's walking the K-9 dog, and the dog alerts on a house without any trespass. |
| 0:42:31.740 | 2551.740 | MR. BLUMBERG | front door | This is an easier case, of course, because the police officer in this case -- and not only the facts of this case, but the question presented is going up to the front door of a home. |
| 0:42:51.440 | 2571.440 | JUSTICE ALITO | dog | But that's not true of dogs. |
| 0:42:52.080 | 2572.080 | JUSTICE ALITO | dog | Dogs were around. |
| 0:42:55.060 | 2575.060 | MR. BLUMBERG | dog | Dogs were around, Justice Alito -- |
| 0:43:09.840 | 2589.840 | MR. BLUMBERG | dog | But in 1791, dogs had not been trained to detect criminal activity within a house -- not -- I'm sorry -- |
| 0:43:19.300 | 2599.300 | MR. BLUMBERG | dog | Dogs have been tracking people -- |
| 0:43:35.860 | 2615.860 | JUSTICE ALITO | front door | So in 1791, if someone -- if the police were using -- or somebody was using a bloodhound to track -- someone who was suspected of a crime, and the bloodhound -- and they used the bloodhound to track the person to the front of -- to the front door of a house, would that have been regarded as a trespass? |
| 0:43:52.220 | 2632.220 | MR. BLUMBERG | front door | Well, the -- I do not have a case that says that taking a bloodhound up to the front door of a house would be a trespass. |
| 0:44:14.180 | 2654.180 | MR. BLUMBERG | front door | I don't believe a homeowner, back in the 1700's, impliedly consented to police coming up to the front door of his house with a bloodhound, even though everybody knew they could do that. |
| 0:46:04.760 | 2764.760 | JUSTICE KENNEDY | dog | I frankly think that might be harder than the dog case or that you can make a stronger case for a reasonable expectation of privacy. |
| 0:46:15.300 | 2775.300 | JUSTICE KENNEDY | dog | If the -- if the homeowner is making a lot of marijuana with -- with odors coming out, he knows that a dog or a person might smell it. |
| 0:48:01.620 | 2881.620 | MR. BLUMBERG | front door | It's the front door. |
| 0:48:04.600 | 2884.600 | MR. BLUMBERG | front door | No, no, it's the front door of the home here. |
| 0:48:07.820 | 2887.820 | CHIEF JUSTICE ROBERTS | front door | But there is an implied license to walk up to the front door, right? |
| 0:48:18.580 | 2898.580 | MR. BLUMBERG | Girl Scout(s) | To do certain things such as to try to and sell Girl Scout cookies, to knock -- even a police officer can go on to the curtilage, to knock on to the door -- I'm sorry -- to knock on the front door, to try and engage the person inside the home in a conversation. |
| 0:48:18.960 | 2898.960 | MR. BLUMBERG | cookie(s) | To do certain things such as to try to and sell Girl Scout cookies, to knock -- even a police officer can go on to the curtilage, to knock on to the door -- I'm sorry -- to knock on the front door, to try and engage the person inside the home in a conversation. |
| 0:48:19.540 | 2899.540 | MR. BLUMBERG | knock/knocker | To do certain things such as to try to and sell Girl Scout cookies, to knock -- even a police officer can go on to the curtilage, to knock on to the door -- I'm sorry -- to knock on the front door, to try and engage the person inside the home in a conversation. |
| 0:48:25.600 | 2905.600 | MR. BLUMBERG | front door | To do certain things such as to try to and sell Girl Scout cookies, to knock -- even a police officer can go on to the curtilage, to knock on to the door -- I'm sorry -- to knock on the front door, to try and engage the person inside the home in a conversation. |
| 0:48:41.420 | 2921.420 | JUSTICE SOTOMAYOR | dog | Have you conceded that the police officer sans dog, if he had come up to the door and knocked, that that would have been permissible, that that was not a search or seizure? |
| 0:48:44.700 | 2924.700 | JUSTICE SOTOMAYOR | knock/knocker | Have you conceded that the police officer sans dog, if he had come up to the door and knocked, that that would have been permissible, that that was not a search or seizure? |
| 0:48:52.500 | 2932.500 | MR. BLUMBERG | front door | If what the police officer was doing at the front door was a knock and talk. |
| 0:48:53.300 | 2933.300 | MR. BLUMBERG | knock/knocker | If what the police officer was doing at the front door was a knock and talk. |
| 0:49:10.220 | 2950.220 | JUSTICE SOTOMAYOR | knock/knocker | Would he have had a right to walk up to the door, knock on it, and start asking questions? |
| 0:49:13.100 | 2953.100 | MR. BLUMBERG | dog | Without the dog. |
| 0:49:15.700 | 2955.700 | JUSTICE SOTOMAYOR | dog | Let's -- sans dog, yes. |
| 0:49:30.260 | 2970.260 | MR. BLUMBERG | front door | A police -- there's implied consent for a police officer to go up to the front door, knock on the door and attempt to engage the person in the house in conversation if they open the door. |
| 0:49:30.940 | 2970.940 | MR. BLUMBERG | knock/knocker | A police -- there's implied consent for a police officer to go up to the front door, knock on the door and attempt to engage the person in the house in conversation if they open the door. |
| 0:49:44.960 | 2984.960 | JUSTICE ALITO | front door | If you took a poll of people and said do you want -- do you want police officers who suspect you of possibly engaging in criminal conduct to come to your front door and knock on the door so they can talk to you and attempt to get incriminating information out of you, would most people say, yes, I consent to that? |
| 0:49:45.540 | 2985.540 | JUSTICE ALITO | knock/knocker | If you took a poll of people and said do you want -- do you want police officers who suspect you of possibly engaging in criminal conduct to come to your front door and knock on the door so they can talk to you and attempt to get incriminating information out of you, would most people say, yes, I consent to that? |
| 0:50:04.700 | 3004.700 | MR. BLUMBERG | front door | And I think at this point it's customary for people to expect that police officers may come to your front door and knock on your front door to try and talk to you. |
| 0:50:05.300 | 3005.300 | MR. BLUMBERG | knock/knocker | And I think at this point it's customary for people to expect that police officers may come to your front door and knock on your front door to try and talk to you. |
| 0:50:14.320 | 3014.320 | JUSTICE SOTOMAYOR | dog | I guess the bottom line is that are you taking -- it sounds to me like you're saying there's no implied consent to bring a dog on to my property. |
| 0:50:18.660 | 3018.660 | MR. BLUMBERG | dog | And certainly not a narcotics detection dog. |
| 0:50:23.500 | 3023.500 | JUSTICE SOTOMAYOR | dog | You're -- Mr. Garre said differently, that there is an implied consent for your neighbor to bring the dog up for anyone else but a police officer. |
| 0:50:40.720 | 3040.720 | MR. BLUMBERG | dog | I think a strong argument can be made that there is no implied consent for anyone to bring a dog up to the front door of your house, because, as you pointed out, a lot of people don't like -- don't like dogs and -- and some people are allergic to dogs. |
| 0:50:41.580 | 3041.580 | MR. BLUMBERG | front door | I think a strong argument can be made that there is no implied consent for anyone to bring a dog up to the front door of your house, because, as you pointed out, a lot of people don't like -- don't like dogs and -- and some people are allergic to dogs. |
| 0:50:50.520 | 3050.520 | JUSTICE GINSBURG | dog | I thought you were talking about a dog trained to detect contraband -- |
| 0:50:54.640 | 3054.640 | JUSTICE GINSBURG | dog | -- not just any old dog. |
| 0:50:56.940 | 3056.940 | MR. BLUMBERG | dog | We are, but I believe the hypothet was just any dog. |
| 0:50:59.040 | 3059.040 | MR. BLUMBERG | dog | But certainly, when it's -- when it's a dog trained to detect contraband, there's no question that no one impliedly consents to that happening and there's no question, as Justice Breyer pointed out, that a homeowner has a reasonable expectation of privacy that that's not going to happen. |
| 0:51:16.180 | 3076.180 | JUSTICE ALITO | dog | You draw a distinction between dogs that are not drug detection dogs and ordinary dogs. |
| 0:51:38.320 | 3098.320 | MR. BLUMBERG | knock/knocker | In terms of the right of that officer to come up to the house and knock on the front door? |
| 0:51:38.320 | 3098.320 | MR. BLUMBERG | front door | In terms of the right of that officer to come up to the house and knock on the front door? |
| 0:51:38.320 | 3098.320 | JUSTICE ALITO | knock/knocker | To knock on the front door, yes. |
| 0:51:38.800 | 3098.800 | JUSTICE ALITO | front door | To knock on the front door, yes. |
| 0:51:48.500 | 3108.500 | MR. BLUMBERG | knock/knocker | You impliedly consent and you have no reasonable expectation of privacy that any type of police officer is going to come and knock on your front door and try and talk to you. |
| 0:51:49.000 | 3109.000 | MR. BLUMBERG | front door | You impliedly consent and you have no reasonable expectation of privacy that any type of police officer is going to come and knock on your front door and try and talk to you. |
| 0:52:15.900 | 3135.900 | JUSTICE BREYER | dog | Do people come up to the door with dogs? |
| 0:52:17.620 | 3137.620 | JUSTICE BREYER | dog | Do the dogs breathe? |
| 0:52:46.120 | 3166.120 | MR. BLUMBERG | dog | And -- and just to clear up the factual, I don't believe that -- that what happened here in terms of the use of the drug detection dog took 5 to 15 minutes. |
| 0:53:04.280 | 3184.280 | MR. BLUMBERG | front door | It certainly took, I would say, at least 1 or 2 minutes, because what happened -- and again, this is on 96, 97 and 98 -- the officer goes from the street over the curb, up to the front door of the house, with the dog basically dragging him up to the front door of the house. |
| 0:53:05.920 | 3185.920 | MR. BLUMBERG | dog | It certainly took, I would say, at least 1 or 2 minutes, because what happened -- and again, this is on 96, 97 and 98 -- the officer goes from the street over the curb, up to the front door of the house, with the dog basically dragging him up to the front door of the house. |
| 0:53:14.940 | 3194.940 | MR. BLUMBERG | dog | They go up this walkway -- and a picture of the home is -- is in the appendix to the brief -- and then the dog crosses the -- into the alcove, the area right in front of the house. |
| 0:53:20.760 | 3200.760 | MR. BLUMBERG | dog | And once he gets in that area, the dog starts violently bracketing back and forth, pulling on the leash. |
| 0:53:24.440 | 3204.440 | MR. BLUMBERG | leash | And once he gets in that area, the dog starts violently bracketing back and forth, pulling on the leash. |
| 0:53:25.900 | 3205.900 | MR. BLUMBERG | dog | The dog handler testified that the other officer had to stay back, because it was so violent that people could get knocked down by what's happening. |
| 0:53:32.450 | 3212.450 | MR. BLUMBERG | knock/knocker | The dog handler testified that the other officer had to stay back, because it was so violent that people could get knocked down by what's happening. |
| 0:53:35.370 | 3215.370 | MR. BLUMBERG | dog | And for a period of time the dog goes back and forth, back and forth, and then at some point goes to the crack on the bottom of the front door, sniffs that, and then the process finally stops, he sits down. |
| 0:53:41.650 | 3221.650 | MR. BLUMBERG | front door | And for a period of time the dog goes back and forth, back and forth, and then at some point goes to the crack on the bottom of the front door, sniffs that, and then the process finally stops, he sits down. |
| 0:53:58.030 | 3238.030 | JUSTICE GINSBURG | dog | Mr. Blumberg, the Florida appellate court, yes, the court of appeals, did say that that the officer and the dog were lawfully present. |
| 0:54:20.950 | 3260.950 | MR. BLUMBERG | dog | There is a whole section in the opinion in the Third District Court of Appeals saying the officer and the dog were lawfully present. |
| 0:54:32.710 | 3272.710 | MR. BLUMBERG | dog | That -- that issue -- that part of the opinion goes: We find that the officer and the dog were lawfully present. |
| 0:55:03.110 | 3303.110 | MR. BLUMBERG | porch | The Third District Court of Appeal decided the officer had the right to go up and be there on the front porch with the dog. |
| 0:55:03.670 | 3303.670 | MR. BLUMBERG | dog | The Third District Court of Appeal decided the officer had the right to go up and be there on the front porch with the dog. |
| 0:55:12.130 | 3312.130 | MR. BLUMBERG | knock/knocker | There is a passage in the decision of the Florida Supreme Court that says an officer going up to the door -- can go up to the door and do a knock and talk, but when the officer goes up with a narcotics detection dog, that is a qualitatively different matter. |
| 0:55:15.570 | 3315.570 | MR. BLUMBERG | dog | There is a passage in the decision of the Florida Supreme Court that says an officer going up to the door -- can go up to the door and do a knock and talk, but when the officer goes up with a narcotics detection dog, that is a qualitatively different matter. |
| 0:55:32.270 | 3332.270 | CHIEF JUSTICE ROBERTS | knock/knocker | So what if there is some person who has, you know, the best sense of smell in the department, and they say, well, let's use him to go do the knock and talks when we suspect drugs; that way, he may discover the odor of marijuana when other people wouldn't. |
| 0:55:58.190 | 3358.190 | MR. BLUMBERG | knock/knocker | So they weren't really going up there to do a knock -- |
| 0:55:58.790 | 3358.790 | CHIEF JUSTICE ROBERTS | knock/knocker | To do a knock and talk. |
| 0:55:59.490 | 3359.490 | CHIEF JUSTICE ROBERTS | knock/knocker | You said knock and talks are okay. |
| 0:56:02.310 | 3362.310 | MR. BLUMBERG | knock/knocker | Well, but there's -- knock and talks are okay; but, under your hypothet, it appears that the knock and talk was -- was not really what the officer was going up there for. |
| 0:56:18.030 | 3378.030 | JUSTICE SOTOMAYOR | knock/knocker | They knock to hope the person comes to the door and that they can see something from the door. |
| 0:56:26.490 | 3386.490 | JUSTICE SOTOMAYOR | knock/knocker | They knock -- they always have a dual motive. |
| 0:56:50.110 | 3410.110 | JUSTICE SOTOMAYOR | knock/knocker | He knocks, and he says to the neighbor, who are you? |
| 0:57:18.090 | 3438.090 | MR. BLUMBERG | front door | No, no. What's not okay is if he goes up there to perform a search, or if he conducts a search -- and, again, back to the facts of this case, when a police officer goes up to the front door with a narcotics detection dog, there is no question what that officer is doing. |
| 0:57:19.610 | 3439.610 | MR. BLUMBERG | dog | No, no. What's not okay is if he goes up there to perform a search, or if he conducts a search -- and, again, back to the facts of this case, when a police officer goes up to the front door with a narcotics detection dog, there is no question what that officer is doing. |
| 0:57:28.510 | 3448.510 | MR. BLUMBERG | dog | And, therefore, if you go to Jones, the officer and the dog have entered -- have physically trespassed, because there is no consent to do that, onto a constitutionally protected area, the curtilage of the home, and performed a search. |
| 0:58:16.970 | 3496.970 | MR. BLUMBERG | dog | I don't believe any court has faced this issue as to whether or not taking a police dog up to the front door of a house is a trespass under the common law. |
| 0:58:17.710 | 3497.710 | MR. BLUMBERG | front door | I don't believe any court has faced this issue as to whether or not taking a police dog up to the front door of a house is a trespass under the common law. |
| 0:58:43.930 | 3523.930 | MR. GARRE | dog | With respect to the bracketing, bracketing just means that the dog is getting excited, moving his head around. |
| 0:58:47.490 | 3527.490 | MR. GARRE | dog | This is a passive alert dog. |
| 0:58:51.830 | 3531.830 | MR. GARRE | dog | It's no different than what a neighbor's dog would do when they get to the front door. |
| 0:58:52.910 | 3532.910 | MR. GARRE | front door | It's no different than what a neighbor's dog would do when they get to the front door. |
| 0:58:59.930 | 3539.930 | JUSTICE SOTOMAYOR | dog | I thought what the dog does, according to the police officer's testimony, is he gave him a long leash so the dog would lead him to the drugs. |
| 0:59:05.330 | 3545.330 | JUSTICE SOTOMAYOR | leash | I thought what the dog does, according to the police officer's testimony, is he gave him a long leash so the dog would lead him to the drugs. |
| 0:59:09.770 | 3549.770 | JUSTICE SOTOMAYOR | dog | And what the dog did, I thought, according to what I read, was go past the motorcycle to make sure -- I mean, the officer said this -- you don't know if the drugs are in the motorcycle, you don't know if they're in the garage, you don't know where they might be. |
| 0:59:22.910 | 3562.910 | JUSTICE SOTOMAYOR | dog | So the dog is permitted to roam around until he catches the scent. |
| 0:59:35.170 | 3575.170 | MR. GARRE | front door | They're walking up the common path, and you can see it from the picture at the -- appended to the brief, and then up to the front door. |
| 0:59:36.330 | 3576.330 | MR. GARRE | front door | It's near the front door where he alerted by sitting down. |
| 0:59:57.970 | 3597.970 | MR. GARRE | porch | It says that, under Florida law, there is no reasonable expectation of privacy in a porch, taking into account that visitors and salesmen can come up to the front door. |
| 1:00:00.950 | 3600.950 | MR. GARRE | salesman/salesmen | It says that, under Florida law, there is no reasonable expectation of privacy in a porch, taking into account that visitors and salesmen can come up to the front door. |
| 1:00:03.290 | 3603.290 | MR. GARRE | front door | It says that, under Florida law, there is no reasonable expectation of privacy in a porch, taking into account that visitors and salesmen can come up to the front door. |
| 1:01:12.810 | 3672.810 | JUSTICE KAGAN | knock/knocker | So that your implied consent or expectations about your neighbor might differ fundamentally, you know, if the neighbor comes and knocks on your door, or if the neighbor brings his magnifying glass and his microscope and everything else and starts testing everything around it. |
| 1:01:28.110 | 3688.110 | MR. GARRE | dog | Well, and I think that gets back to our point that this is a dog that's been used by humans for centuries by scent. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.880 to 0:03:07.880, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.880] MR. GARRE: Thank you, Mr. Chief Justice, and may it please the Court: In the three prior cases in which this Court has held that a dog sniff is not a search, this Court has emphasized that a dog sniff is unique, both in terms of the manner in which information is obtained and the nature of the information revealed. As to the latter point, this Court has emphasized that a drug detection dog reveals only the presence of contraband, and that no one has a legitimate expectation of privacy in that.

[0:00:34.980] JUSTICE KENNEDY: I mean, that just can't be a proposition that we can accept across the board. Nobody under that view has an interest in contraband in their home. The question is, can you find out the contraband? It's just a circular argument. And if -- and in the -- was it the Caballes case that talked about that, if I have the right name? That was where the contraband was visible; it was almost like the smoking gun falls out. Well, of course, there's no interest in the smoking gun when it falls out in front of you. So I just don't think that works.

[0:01:05.460] MR. GARRE: Well, Justice Kennedy, in the Caballes case, the contraband wasn't visible before the dog alerted. In the home case, we're not saying that you don't have a legitimate expectation of privacy in the home. Of course, you do. The question is whether you have a legitimate expectation --

[0:01:19.760] JUSTICE SOTOMAYOR: So doesn't that mean that what's in your home that's not visible to the public has an expectation of privacy as well?

[0:01:30.560] MR. GARRE: Not when it comes to contraband, Your Honor. And we think that the Kyllo case helps --

[0:01:34.800] JUSTICE SOTOMAYOR: But that -- that is circular. Then why do you need a search warrant? If you have no expectation of privacy in the contraband, why bother even with a search warrant?

[0:01:44.120] MR. GARRE: Because, Your Honor, when you have a search warrant and you go into a home, there's going to be a lot of private information that you're going to come across, even if your expectation is finding evidence of a crime.

[0:01:53.260] JUSTICE GINSBURG: Mr. Garre, does your argument mean -- you say minimally intrusive, and that the dog will detect only contraband, that the police then are to go into a neighborhood that's known to be a drug dealing neighborhood, go into -- just go down the street, have the dog sniff in front of every door, or go into an apartment building? Is that -- I gather that that is your position.

[0:02:26.240] MR. GARRE: Your Honor, they could do that, just like the police could go door to door and then knock on the doors and hope that they will find out evidence of wrongdoing that way. But the two responses this Court has always pointed to is the restraint on resources and the check of community hostility. Here, the police were combatting a serious epidemic of grow houses, hundreds of houses each year that were a scourge to the community, not only in terms just of the drugs that they were growing --

[0:02:51.920] JUSTICE GINSBURG: Suppose -- suppose the house had on the lawn, no dogs allowed?

[0:03:00.260] MR. GARRE: I think that would be different, Your Honor. It would be -- and that's a way in which the house is different than a car. Homeowners can restrict access to

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - March 26, 2013.

- Oyez page: https://www.oyez.org/cases/2012/11-564
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2012/11-564/20130326o_11-564.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.3 MB)
- Length: 0:05:09.264 (309.264 s)
- Words: 723, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 709 of Whisper's 723 words (98.1%; Oyez has 721).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:07.000 | 16 |
| JUSTICE SCALIA | 0:00:08.660 | 0:05:08.640 | 704 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Scalia has the opinion of the Court this morning in Case 11-564, Florida v. Jardines.

[0:00:08.660] JUSTICE SCALIA: come out from behind these briefs here. This case is here on writ of certiorari from the Supreme Court of Florida. The police received a tip that the Respondent, Joelle Jardine, was growing marijuana in his home. A surveillance team went to the home but saw nothing. Two officers then took a dog trained to detect the smell of illegal drugs and approached Jardine's home. The dog and his handler walked up to the front porch. After sniffing around and going back and forth on the porch, the dog eventually sat down in front of Jardine's front door, which is what he was trained to do upon finding the odor's strongest point. The officers then secured a search warrant using what they had learned as establishing probable cause, and marijuana plants were found in the home. At trial, Jardines moved to suppress that evidence, arguing that when the officers brought the dog up to his door, they had searched his home without probable cause in violation of the Fourth Amendment. The trial court agreed with him, so did the Supreme Court of Florida, and so do we. The Fourth Amendment protects the right of the people to be secure in their persons, houses, papers, and effects against unreasonable searches and seizures. This case does not concern what it means for a search to be unreasonable. Rather, the question here is more fundamental. What actions constitute a search? The basic rule is that a search occurs for Fourth Amendment purposes when the government physically intrudes for investigative purposes on one of the areas that the amendment protects, that is, intrudes onto persons, houses, papers, or effects. Our later cases have supplemented this test, but the basic approach keeps easy cases easy, and by those lights, this is an easy case indeed. First, there is no doubt that the officers physically intruded into an area protected by the Fourth Amendment. In our law of search and seizure, the home is first among equals. At the amendment's absolute core is the right of a man to retreat into his own home and there be free from the State's gaze. The area immediately surrounding the home, which is called the curtilage, has long been regarded as part of the home itself. The police cannot, without a warrant based on probable cause,

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:08.660-0:00:09.300: "Scalia"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:27.140 | Joelle Jardine, | Joelis Jardines |
| 0:04:12.200 | sweep | slip |
| 0:04:56.300 | filed | flied |
| 0:05:00.280 | join. | joined. |
| 0:05:08.240 | join. | joined. |
