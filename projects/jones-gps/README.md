# jones-gps: Supreme Court No. 10-1259

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2011/10-1259
- Audio: https://www.supremecourt.gov/media/audio/mp3files/10-1259.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2011/10-1259.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 46 min on 4 CPU cores
- Audio length: 1:03:32.180 (3812.180 s)
- `audio/argument.mp3`: mono, 64 kbps, 30.5 MB
- Official words: 11113 (plus 7 `(Laughter.)` markers), in 269 speaker turns
- ASR words: 10953
- Official words matched to an ASR word: 10572 of 11113 (**95.13%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 95.13% (threshold 85%).

328 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
to that sound, at least 0.2 s from its start. This trimmed 17 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 10-1259 2011 jones-gps --model medium.en --opinion --mentions "GPS,device,car,cars,Jeep,vehicle,track,tracking,month,our,us,everybody,Big Brother,1984,beeper,warrant,follow,police,privacy" --long-questions 10

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE SCALIA, 0:03:20.500 to 0:05:05.180 (104.7 s, 268 words)

> I have to give a little prologue to my question. When -- when wiretapping first came before this Court, we held that it was not a violation of the Fourth Amendment because the Fourth Amendment says that the -- the people shall be secure in their persons, houses, papers, and effects against unreasonable searches and seizures. And wiretapping just picked up conversations. That's not persons, houses, papers, and effects. Later on, we reversed ourselves, and, as you mentioned, Katz established the new criterion, which is, is there an invasion of privacy? Does -- are you obtaining information that a person had a reasonable expectation to be kept private? I think that was wrong. I don't think that was the original meaning of the Fourth Amendment. But, nonetheless, it's been around for so long, we're not going to overrule that. However, it is one thing to add that privacy concept to the Fourth Amendment as it originally existed, and it is quite something else to use that concept to narrow the Fourth Amendment from what it originally meant. And it seems to me that when that device is installed against the will of the owner of the car on the car, that is unquestionably a trespass and thereby rendering the owner of the car not secure in his effects -- the car is one of his effects -- against an unreasonable search and seizure. It is attached to the car against his will, and it is a search because what it obtains is the location of that car from there forward. Now, why -- why isn't that correct? Do you deny that it's a trespass?

### 2. JUSTICE ALITO, 0:07:50.920 to 0:09:17.920 (87.0 s, 255 words)

> Well, that seems to get -- to me to get to what's really involved here. The issue of whether there's a technical trespass or not is potentially a ground for deciding this particular case, but it seems to me the heart of the problem that's presented by this case and will be presented by other cases involving new technology is that in the pre-computer, pre-Internet age, much of the privacy -- I would say most of the privacy -- that people enjoyed was not the result of legal protections or constitutional protections; it was the result simply of the difficulty of traveling around and gathering up information. But with computers, it's now so simple to amass an enormous amount of information about people that consists of things that could have been observed on the streets, information that was made available to the public. If -- if this case is decided on the ground that there was a technical trespass, I don't have much doubt that in the near future, it will be possible -- I think it's possible now in many instances -- for law enforcement to monitor people's movements on -- on public streets without committing a technical trespass. So, how do we deal with this? Do we just say, well, nothing is changed, so that all the information that people expose to the public is -- is fair game? There's no -- there's no search or seizure when that is -- when that is obtained because there isn't a reasonable expectation of privacy, but isn't there a real change in -- in this regard?

### 3. JUSTICE SCALIA, 0:40:58.220 to 0:42:15.120 (76.9 s, 212 words)

> Mr. Leckar, your -- all of this discussion -- you're going into it, but the questioning leads you into it -- it seems to me leaps over the difficult part of your case. The issue before us is not -- not in the abstract whether this police conduct is unreasonable. The unreasonableness requirement or the unreasonableness prohibition does not take effect unless there has been a search. And our cases have said that there's no search when -- when you are in public and where everything that you do is open to -- to the view of people. That's the hard question in the case, not whether this is unreasonable. That's not what the Fourth Amendment says, the police can't do anything that's unreasonable. They can do a lot of stuff that's unreasonable without violating the Fourth Amendment, and the -- the protection against that is the legislature. But you have to establish, if you're going to go with Katz, that there has been an invasion of -- of privacy when all that -- all that this is showing is where the car is going on the public streets, where the police could have had round-the-clock surveillance on this individual for a whole month or for 2 months or for 3 months, and that would not have violated anything, would it?

### 4. JUSTICE BREYER, 0:10:54.880 to 0:12:05.580 (70.7 s, 170 words)

> What -- what is the question that I think people are driving at, at least as I understand them and certainly share the concern, is that if you win this case, then there is nothing to prevent the police or the government from monitoring 24 hours a day the public movement of every citizen of the United States. And -- and the difference between the monitoring and what happened in the past is memories are fallible; computers aren't. And no one, or at least very rarely, sends human beings to follow people 24 hours a day. That occasionally happens. But with the machines, you can. So, if you win, you suddenly produce what sounds like 1984 from their brief. I understand they have an interest in perhaps dramatizing that, but -- but maybe overly. But it still sounds like it. And so, what protection is there, if any, once we accept your view of the case, from this slight futuristic scenario that's just been painted and is done more so in their briefs?

### 5. JUSTICE SOTOMAYOR, 0:17:36.420 to 0:18:33.040 (56.6 s, 116 words)

> You're -- you're now suggesting an answer to Justice Kennedy's question, which is it would be okay to take the computer chip, put it on somebody's overcoat, and follow every citizen everywhere they go indefinitely. So -- under your theory and the theory espoused in your brief, you could monitor and track every person through their cell phone, because today the smartphones emit signals that police can pick up and use to follow someone anywhere they go. Your theory is so long as the -- that all -- that what is being monitored is the movement of person, of a person, they have no reasonable expectation that their possessions will not be used by you. That's really the bottom line --

### 6. JUSTICE BREYER, 0:32:59.400 to 0:33:45.640 (46.2 s, 138 words)

> And I think that's the question we've been debating. And I would like to know from you -- what they are saying is that the parade of horribles we can worry with -- worry about when it comes up; the police have many, many people that they suspect of all kinds of things ranging from kidnappings of lost children to terrorism to all kinds of crimes. They're willing to go as far as reasonable suspicion in a pinch. And they say at least with that, you will avoid the 1984 scenario, and you will in fact allow the police to do their work with doing no more than subjecting the person to really good knowledge of where he's going on the open highway. Now, I -- they probably put it better than I did, but I'd appreciate your views on that.

### 7. JUSTICE GINSBURG, 0:15:16.680 to 0:16:02.540 (45.9 s, 109 words)

> Mr. Dreeben, this case started out with a warrant. There was a warrant, and the limits weren't followed. The warrant said 10 days, do this in 10 days, and the police took 11. They were supposed to do it in D.C. Instead, they did it in Maryland. So, the police could have gotten permission to conduct this search. In fact, they had received it. Now, I take it that the practice had been, because it's in the electronic surveillance manual, better get a warrant. Was there any problem about -- when this kind of surveillance is wanted by the government, to get a warrant? Were they encountering difficulty getting warrants?

### 8. JUSTICE GINSBURG, 0:23:52.420 to 0:24:36.540 (44.1 s, 89 words)

> But the Fourth Amendment protects us against unreasonable searches and seizures. And if I were trying to explain to someone, here's the Fourth Amendment, the Fourth Amendment says -- or it has been interpreted to mean that if I'm on a public bus and the police want to feel my luggage, that's a violation; and yet, this kind of monitoring, installing the GPS and monitoring the person's movement whenever they are outside their house in the car, is not? I mean, it just -- something about it that -- just doesn't parse.

### 9. JUSTICE BREYER, 0:53:55.600 to 0:54:36.180 (40.6 s, 117 words)

> Can you take it to Congress the other way? I mean, can you say that a general search of this kind is not constitutional under the Fourth Amendment, but should Congress pick out a subset thereof, say, the -- terrorism or where there is reasonable cause or like the FISA court or special courts to issue special kinds of warrants, that that's a different question which we could decide at a later time? That's a negative way of -- I mean, that way favors you in the result, but I've -- I've been looking for -- if there is a way of going to Congress to create the situations where they can do it, rather than the situations where they can't.

### 10. JUSTICE GINSBURG, 0:10:00.640 to 0:10:39.260 (38.6 s, 80 words)

> There was a third party involved in the telephone -- in the pen register case. And, here, it's the police. Essentially, I think you answered the question that the government's position would mean that any of us could be monitored whenever we leave our homes. So, the only thing secure is the home. Is -- I mean, that is -- that is the end point of your argument, that an electronic device, as long as it's not used inside the house, is okay.

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-45.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:03:16.460 | 196.460 | medium | 1.58 | 0.90 | 18.1 | 22.5 | that there -- about the way in which this beeper was installed. But you can get to that at -- at your convenience. Mr. Dreeben, I'd like to get to it now. |
| 2 | 0:07:16.520 | 436.520 | big | 3.28 | 2.70 | 22.5 | 30.9 | a GPS device on all of our cars, monitored our movements for a month? You think you're entitled to do that under your theory? The Justices of this Court? Yes. |
| 3 | 0:28:57.700 | 1737.700 | medium | 0.96 | 0.85 | 19.5 | 23.2 | not a technical trespass in this particular case. Mr. Jones had the -- Is that right? I don't own my license plate? I didn't know that. How do you know that? |
| 4 | 0:29:01.260 | 1741.260 | big | 1.36 | 1.20 | 21.6 | 24.2 | the -- Is that right? I don't own my license plate? I didn't know that. How do you know that? How do you know that? I paid for my license plate. |
| 5 | 0:29:06.400 | 1746.400 | big | 2.24 | 2.10 | 25.9 | 31.6 | that? How do you know that? I paid for my license plate. We don't need to get into it, but "Live Free or Die" was spelled on the license plate. |
| 6 | 0:37:43.860 | 2263.860 | medium | 0.84 | 0.60 | 23.2 | 28.0 | the time. So, why is this different from that? It's pretty scary. I wouldn't want to live in London under those circumstances. Well, it must be unconstitutional if it's scary. |
| 7 | 0:53:34.920 | 3214.920 | under speech | 0.00 | 0.00 | - | - | Amendment violation so far as domestic security is concerned and gave Congress suggestions. In this particular case, I could probably give you 535 reasons why not to go to Congress -- |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| GPS | 44 | 48 |
| device | 28 | 31 |
| car | 51 | 62 |
| cars | 7 | 8 |
| Jeep | 0 | 0 |
| vehicle | 11 | 11 |
| track | 16 | 17 |
| tracking | 7 | 7 |
| month | 13 | 16 |
| our | 19 | 23 |
| us | 27 | 30 |
| everybody | 5 | 5 |
| Big Brother | 0 | 0 |
| 1984 | 6 | 6 |
| beeper | 13 | 13 |
| warrant | 39 | 43 |
| follow | 22 | 25 |
| police | 59 | 62 |
| privacy | 43 | 49 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:28.120 | 28.120 | MR. DREEBEN | vehicle | What a person seeks to preserve as private in the enclave of his own home or in a private letter or inside of his vehicle when he is traveling is a subject of Fourth Amendment protection. |
| 0:00:37.040 | 37.040 | MR. DREEBEN | car | But what he reveals to the world, such as his movements in a car on a public roadway, is not. |
| 0:00:46.620 | 46.620 | MR. DREEBEN | beeper | In Knotts v. United States, this Court applied that principle to hold that visual and beeper surveillance of a vehicle traveling on the public roadways infringed no Fourth Amendment expectation of privacy. |
| 0:00:48.560 | 48.560 | MR. DREEBEN | vehicle | In Knotts v. United States, this Court applied that principle to hold that visual and beeper surveillance of a vehicle traveling on the public roadways infringed no Fourth Amendment expectation of privacy. |
| 0:00:54.440 | 54.440 | MR. DREEBEN | privacy | In Knotts v. United States, this Court applied that principle to hold that visual and beeper surveillance of a vehicle traveling on the public roadways infringed no Fourth Amendment expectation of privacy. |
| 0:01:00.060 | 60.060 | CHIEF JUSTICE ROBERTS | follow | You're following the car, and the beeper just helps you follow it from a -- from a slightly greater distance. |
| 0:01:00.860 | 60.860 | CHIEF JUSTICE ROBERTS | car | You're following the car, and the beeper just helps you follow it from a -- from a slightly greater distance. |
| 0:01:01.460 | 61.460 | CHIEF JUSTICE ROBERTS | beeper | You're following the car, and the beeper just helps you follow it from a -- from a slightly greater distance. |
| 0:01:11.680 | 71.680 | CHIEF JUSTICE ROBERTS | GPS | The technology is very different, and you get a lot more information from the GPS surveillance than you do from following a beeper. |
| 0:01:13.320 | 73.320 | CHIEF JUSTICE ROBERTS | follow | The technology is very different, and you get a lot more information from the GPS surveillance than you do from following a beeper. |
| 0:01:13.920 | 73.920 | CHIEF JUSTICE ROBERTS | beeper | The technology is very different, and you get a lot more information from the GPS surveillance than you do from following a beeper. |
| 0:01:27.620 | 87.620 | MR. DREEBEN | car | The technology is different, Mr. Chief Justice, but a crucial fact in Knotts that shows that this was not simply amplified visual surveillance is that the officers actually feared detection in Knotts as the car crossed from Minnesota to Wisconsin. |
| 0:01:33.320 | 93.320 | MR. DREEBEN | police | The driver began to do certain U-turns and, the police broke off visual surveillance. |
| 0:01:36.560 | 96.560 | MR. DREEBEN | track | They lost track of the car for a full hour. |
| 0:01:37.260 | 97.260 | MR. DREEBEN | car | They lost track of the car for a full hour. |
| 0:01:41.740 | 101.740 | MR. DREEBEN | beeper | They only were able to discover it by having a beeper receiver in a helicopter that detected the beeps from the radio transmitter in the can of chloroform. |
| 0:01:52.900 | 112.900 | CHIEF JUSTICE ROBERTS | follow | That's a lot of work to follow the car. |
| 0:01:53.380 | 113.380 | CHIEF JUSTICE ROBERTS | car | That's a lot of work to follow the car. |
| 0:01:54.460 | 114.460 | CHIEF JUSTICE ROBERTS | beeper | They've got to listen to the beeper; when they lose it, they've got to call in the helicopter. |
| 0:02:01.780 | 121.780 | CHIEF JUSTICE ROBERTS | car | Here they just sit back in the station, and they -- they push a button whenever they want to find out where the car is. |
| 0:02:03.920 | 123.920 | CHIEF JUSTICE ROBERTS | month | They look at data from a month and find out everywhere it's been in the past month. |
| 0:02:22.120 | 142.120 | JUSTICE KENNEDY | beeper | Well, under that rationale, could you put a beeper surreptitiously on the man's overcoat or sport coat? |
| 0:02:36.280 | 156.280 | MR. DREEBEN | follow | Probably not, Justice Kennedy; and the reason is that this Court in Karo v. United States -- United States v. Karo -- specifically distinguished the possibility of following a car on a public roadways from determining the location of an object in a place where a person has a reasonable expectation of privacy. |
| 0:02:37.020 | 157.020 | MR. DREEBEN | car | Probably not, Justice Kennedy; and the reason is that this Court in Karo v. United States -- United States v. Karo -- specifically distinguished the possibility of following a car on a public roadways from determining the location of an object in a place where a person has a reasonable expectation of privacy. |
| 0:02:43.460 | 163.460 | MR. DREEBEN | privacy | Probably not, Justice Kennedy; and the reason is that this Court in Karo v. United States -- United States v. Karo -- specifically distinguished the possibility of following a car on a public roadways from determining the location of an object in a place where a person has a reasonable expectation of privacy. |
| 0:02:44.720 | 164.720 | JUSTICE KENNEDY | device | Oh, no. This is a special device. |
| 0:02:54.840 | 174.840 | MR. DREEBEN | device | In that event, Justice Kennedy, there is a serious question about whether the installation of such a device would implicate either a search or a seizure. |
| 0:03:11.160 | 191.160 | JUSTICE KENNEDY | beeper | Well -- and on that latter point, you might just be aware that I have serious reservations that there wasn't -- that there -- about the way in which this beeper was installed. |
| 0:03:57.480 | 237.480 | JUSTICE SCALIA | privacy | Later on, we reversed ourselves, and, as you mentioned, Katz established the new criterion, which is, is there an invasion of privacy? |
| 0:04:18.380 | 258.380 | JUSTICE SCALIA | privacy | However, it is one thing to add that privacy concept to the Fourth Amendment as it originally existed, and it is quite something else to use that concept to narrow the Fourth Amendment from what it originally meant. |
| 0:04:31.200 | 271.200 | JUSTICE SCALIA | device | And it seems to me that when that device is installed against the will of the owner of the car on the car, that is unquestionably a trespass and thereby rendering the owner of the car not secure in his effects -- the car is one of his effects -- against an unreasonable search and seizure. |
| 0:04:35.340 | 275.340 | JUSTICE SCALIA | car | And it seems to me that when that device is installed against the will of the owner of the car on the car, that is unquestionably a trespass and thereby rendering the owner of the car not secure in his effects -- the car is one of his effects -- against an unreasonable search and seizure. |
| 0:04:53.380 | 293.380 | JUSTICE SCALIA | car | It is attached to the car against his will, and it is a search because what it obtains is the location of that car from there forward. |
| 0:05:27.400 | 327.400 | JUSTICE KENNEDY | device | There is no consent by the owner of the property to which this device was affixed. |
| 0:05:56.060 | 356.060 | MR. DREEBEN | privacy | Well, this Court thought that it was a technical trespass in Karo and said that made no difference because the purpose of the Fourth Amendment is to protect privacy interests and meaningful interferences with possessory interests, not to cover all technical trespasses. |
| 0:06:07.860 | 367.860 | JUSTICE SCALIA | privacy | So, the -- the privacy rationale doesn't expand it but narrows it in some respects. |
| 0:06:29.220 | 389.220 | MR. DREEBEN | police | In that case, there was absolutely no doubt that the police committed a trespass under local law. |
| 0:07:06.420 | 426.420 | CHIEF JUSTICE ROBERTS | GPS | You think there would also not be a search if you put a GPS device on all of our cars, monitored our movements for a month? |
| 0:07:06.840 | 426.840 | CHIEF JUSTICE ROBERTS | device | You think there would also not be a search if you put a GPS device on all of our cars, monitored our movements for a month? |
| 0:07:08.420 | 428.420 | CHIEF JUSTICE ROBERTS | our | You think there would also not be a search if you put a GPS device on all of our cars, monitored our movements for a month? |
| 0:07:08.640 | 428.640 | CHIEF JUSTICE ROBERTS | car | You think there would also not be a search if you put a GPS device on all of our cars, monitored our movements for a month? |
| 0:07:08.640 | 428.640 | CHIEF JUSTICE ROBERTS | cars | You think there would also not be a search if you put a GPS device on all of our cars, monitored our movements for a month? |
| 0:07:11.060 | 431.060 | CHIEF JUSTICE ROBERTS | month | You think there would also not be a search if you put a GPS device on all of our cars, monitored our movements for a month? |
| 0:07:20.280 | 440.280 | MR. DREEBEN | our | Under our theory and under this Court's cases, the Justices of this Court when driving on public roadways have no greater expectation of -- |
| 0:07:31.580 | 451.580 | CHIEF JUSTICE ROBERTS | GPS | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:31.960 | 451.960 | CHIEF JUSTICE ROBERTS | device | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:33.360 | 453.360 | CHIEF JUSTICE ROBERTS | our | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:33.540 | 453.540 | CHIEF JUSTICE ROBERTS | car | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:33.540 | 453.540 | CHIEF JUSTICE ROBERTS | cars | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:34.180 | 454.180 | CHIEF JUSTICE ROBERTS | follow | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:34.520 | 454.520 | CHIEF JUSTICE ROBERTS | us | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:35.060 | 455.060 | CHIEF JUSTICE ROBERTS | month | So, your answer is yes, you could tomorrow decide that you put a GPS device on every one of our cars, follow us for a month; no problem under the Constitution? |
| 0:07:45.500 | 465.500 | MR. DREEBEN | follow | Well, equally, Mr. Chief Justice, if the FBI wanted to, it could put a team of surveillance agents around the clock on any individual and follow that individual's movements as they went around on the public streets, and they would thereby gather -- |
| 0:08:11.300 | 491.300 | JUSTICE ALITO | privacy | The issue of whether there's a technical trespass or not is potentially a ground for deciding this particular case, but it seems to me the heart of the problem that's presented by this case and will be presented by other cases involving new technology is that in the pre-computer, pre-Internet age, much of the privacy -- I would say most of the privacy -- that people enjoyed was not the result of legal protections or constitutional protections; it was the result simply of the difficulty of traveling around and gathering up information. |
| 0:09:13.000 | 553.000 | JUSTICE ALITO | privacy | There's no -- there's no search or seizure when that is -- when that is obtained because there isn't a reasonable expectation of privacy, but isn't there a real change in -- in this regard? |
| 0:10:07.640 | 607.640 | JUSTICE GINSBURG | police | And, here, it's the police. |
| 0:10:18.880 | 618.880 | JUSTICE GINSBURG | us | Essentially, I think you answered the question that the government's position would mean that any of us could be monitored whenever we leave our homes. |
| 0:10:22.360 | 622.360 | JUSTICE GINSBURG | our | Essentially, I think you answered the question that the government's position would mean that any of us could be monitored whenever we leave our homes. |
| 0:10:35.420 | 635.420 | JUSTICE GINSBURG | device | Is -- I mean, that is -- that is the end point of your argument, that an electronic device, as long as it's not used inside the house, is okay. |
| 0:10:36.900 | 636.900 | JUSTICE GINSBURG | us | Is -- I mean, that is -- that is the end point of your argument, that an electronic device, as long as it's not used inside the house, is okay. |
| 0:10:48.460 | 648.460 | MR. DREEBEN | car | We're not talking about monitoring their conversations, their telephone calls, the interior of their cars, their private letters or packages. |
| 0:10:48.460 | 648.460 | MR. DREEBEN | cars | We're not talking about monitoring their conversations, their telephone calls, the interior of their cars, their private letters or packages. |
| 0:11:07.020 | 667.020 | JUSTICE BREYER | police | What -- what is the question that I think people are driving at, at least as I understand them and certainly share the concern, is that if you win this case, then there is nothing to prevent the police or the government from monitoring 24 hours a day the public movement of every citizen of the United States. |
| 0:11:29.520 | 689.520 | JUSTICE BREYER | follow | And no one, or at least very rarely, sends human beings to follow people 24 hours a day. |
| 0:11:40.360 | 700.360 | JUSTICE BREYER | 1984 | So, if you win, you suddenly produce what sounds like 1984 from their brief. |
| 0:12:13.300 | 733.300 | MR. DREEBEN | beeper | If you go back to 1983, the beeper technology in that case seemed extraordinarily advanced, and there was a potential for it to be used. |
| 0:12:19.000 | 739.000 | MR. DREEBEN | us | If you go back to 1983, the beeper technology in that case seemed extraordinarily advanced, and there was a potential for it to be used. |
| 0:12:37.180 | 757.180 | JUSTICE BREYER | month | This involves every journey for a month. |
| 0:12:41.360 | 761.360 | JUSTICE BREYER | us | So, they say whatever the line is that's going to protect us, it's short of every journey in a month. |
| 0:12:45.140 | 765.140 | JUSTICE BREYER | month | So, they say whatever the line is that's going to protect us, it's short of every journey in a month. |
| 0:12:57.840 | 777.840 | MR. DREEBEN | month | I first want to address the suggestion that you could draw a line somewhere between a month and a trip and have a workable standard for police officers to use. |
| 0:13:00.440 | 780.440 | MR. DREEBEN | police | I first want to address the suggestion that you could draw a line somewhere between a month and a trip and have a workable standard for police officers to use. |
| 0:13:02.180 | 782.180 | MR. DREEBEN | police | Police officers use a variety of investigative techniques which in the aggregate produce an enormous amount of information. |
| 0:13:27.980 | 807.980 | JUSTICE BREYER | us | Well, there is the same kind of guidance that you have in any case of this Court that uses the technique which is used sometimes, and I think it's used for example in the bribing the judge case, you know, with campaign contributions. |
| 0:13:53.500 | 833.500 | JUSTICE BREYER | us | That's not necessarily desirable, but that is a method this Court has sometimes used. |
| 0:14:08.240 | 848.240 | MR. DREEBEN | follow | It involves following one suspected drug dealer as to whom there was very strong suspicion, for a period of time that actually is less than a month, because the beeper technology failed during -- |
| 0:14:15.980 | 855.980 | MR. DREEBEN | month | It involves following one suspected drug dealer as to whom there was very strong suspicion, for a period of time that actually is less than a month, because the beeper technology failed during -- |
| 0:14:17.080 | 857.080 | MR. DREEBEN | beeper | It involves following one suspected drug dealer as to whom there was very strong suspicion, for a period of time that actually is less than a month, because the beeper technology failed during -- |
| 0:14:46.480 | 886.480 | CHIEF JUSTICE ROBERTS | warrant | Well, isn't the normal way in these situations that we draw these limits how intrusive the search can be, how long it can be, is by having a magistrate spell it out in a warrant? |
| 0:14:50.000 | 890.000 | MR. DREEBEN | car | When you're talking about the movements of a car on a public roadway, which even Justice Breyer's question seems to concede could be monitored for a day or perhaps 4 days, there is no Fourth Amendment search, unless -- |
| 0:15:10.460 | 910.460 | MR. DREEBEN | everybody | So does looking at everybody's credit card statement for a month. |
| 0:15:12.420 | 912.420 | MR. DREEBEN | month | So does looking at everybody's credit card statement for a month. |
| 0:15:19.620 | 919.620 | JUSTICE GINSBURG | warrant | Mr. Dreeben, this case started out with a warrant. |
| 0:15:21.520 | 921.520 | JUSTICE GINSBURG | warrant | There was a warrant, and the limits weren't followed. |
| 0:15:24.480 | 924.480 | JUSTICE GINSBURG | follow | There was a warrant, and the limits weren't followed. |
| 0:15:25.460 | 925.460 | JUSTICE GINSBURG | warrant | The warrant said 10 days, do this in 10 days, and the police took 11. |
| 0:15:29.360 | 929.360 | JUSTICE GINSBURG | police | The warrant said 10 days, do this in 10 days, and the police took 11. |
| 0:15:36.280 | 936.280 | JUSTICE GINSBURG | police | So, the police could have gotten permission to conduct this search. |
| 0:15:50.300 | 950.300 | JUSTICE GINSBURG | warrant | Now, I take it that the practice had been, because it's in the electronic surveillance manual, better get a warrant. |
| 0:15:59.200 | 959.200 | JUSTICE GINSBURG | warrant | Was there any problem about -- when this kind of surveillance is wanted by the government, to get a warrant? |
| 0:16:02.080 | 962.080 | JUSTICE GINSBURG | warrant | Were they encountering difficulty getting warrants? |
| 0:16:06.100 | 966.100 | MR. DREEBEN | warrant | In this case, there would not have been any difficulty getting a warrant, Justice Ginsburg. |
| 0:16:07.580 | 967.580 | MR. DREEBEN | warrant | And the warrant authorized things beyond just monitoring the car. |
| 0:16:10.260 | 970.260 | MR. DREEBEN | car | And the warrant authorized things beyond just monitoring the car. |
| 0:16:12.720 | 972.720 | MR. DREEBEN | car | It authorized entering the car in order to install it, which wasn't necessary here. |
| 0:16:18.540 | 978.540 | MR. DREEBEN | car | It also authorized monitoring the car in a location where there was a reasonable expectation of privacy. |
| 0:16:21.860 | 981.860 | MR. DREEBEN | privacy | It also authorized monitoring the car in a location where there was a reasonable expectation of privacy. |
| 0:16:24.760 | 984.760 | MR. DREEBEN | car | This case is only about monitoring a car on public streets. |
| 0:16:31.880 | 991.880 | MR. DREEBEN | police | But I think it's very important to keep in mind that the -- the principal use of this kind of surveillance is when the police have not yet acquired probable cause but have a situation that does call for monitoring. |
| 0:16:39.980 | 999.980 | MR. DREEBEN | police | If the police get an anonymous phone call that a bomb threat is going to be carried out at a mosque by people who work at a small company, the bomb threat on an anonymous call will not provide even reasonable suspicion under this Court's decision in Florida v. J.L. |
| 0:17:11.300 | 1031.300 | CHIEF JUSTICE ROBERTS | warrant | If you get an anonymous tip that there's the same bomb in somebody's house, do you get a warrant or do -- do you just go in? |
| 0:17:21.480 | 1041.480 | MR. DREEBEN | police | Because the -- the police in this situation have the traditional means available to investigate these sorts of tips. |
| 0:17:33.360 | 1053.360 | MR. DREEBEN | follow | They could put teams of agents on all the individuals who are within the pool of suspicion and follow them 24/7. |
| 0:17:49.020 | 1069.020 | JUSTICE SOTOMAYOR | follow | You're -- you're now suggesting an answer to Justice Kennedy's question, which is it would be okay to take the computer chip, put it on somebody's overcoat, and follow every citizen everywhere they go indefinitely. |
| 0:18:02.640 | 1082.640 | JUSTICE SOTOMAYOR | track | So -- under your theory and the theory espoused in your brief, you could monitor and track every person through their cell phone, because today the smartphones emit signals that police can pick up and use to follow someone anywhere they go. |
| 0:18:10.600 | 1090.600 | JUSTICE SOTOMAYOR | police | So -- under your theory and the theory espoused in your brief, you could monitor and track every person through their cell phone, because today the smartphones emit signals that police can pick up and use to follow someone anywhere they go. |
| 0:18:12.580 | 1092.580 | JUSTICE SOTOMAYOR | follow | So -- under your theory and the theory espoused in your brief, you could monitor and track every person through their cell phone, because today the smartphones emit signals that police can pick up and use to follow someone anywhere they go. |
| 0:18:30.060 | 1110.060 | JUSTICE SOTOMAYOR | us | Your theory is so long as the -- that all -- that what is being monitored is the movement of person, of a person, they have no reasonable expectation that their possessions will not be used by you. |
| 0:18:33.840 | 1113.840 | JUSTICE SOTOMAYOR | track | -- to track them, to invade their sense of integrity in their choices about who they want to see or use their things. |
| 0:18:47.860 | 1127.860 | MR. DREEBEN | our | Well, Justice Sotomayor, I think that that goes considerably farther than our position in this case, because our position is not that the Court should overrule United States v. Karo and permit monitoring within a private residence. |
| 0:18:59.600 | 1139.600 | MR. DREEBEN | warrant | That is off limits absent a warrant or exigent circumstances plus probable cause. |
| 0:19:12.320 | 1152.320 | MR. DREEBEN | privacy | And monitoring an individual through their clothing poses an extremely high likelihood that they will enter a place where they have a reasonable expectation of privacy. |
| 0:19:12.560 | 1152.560 | JUSTICE SOTOMAYOR | car | Cars get parked in a garages. |
| 0:19:12.560 | 1152.560 | JUSTICE SOTOMAYOR | cars | Cars get parked in a garages. |
| 0:19:15.820 | 1155.820 | MR. DREEBEN | car | Yes, but a car that's parked in a garage does not have a reasonable expectation of privacy as to its location. |
| 0:19:19.100 | 1159.100 | MR. DREEBEN | privacy | Yes, but a car that's parked in a garage does not have a reasonable expectation of privacy as to its location. |
| 0:19:33.340 | 1173.340 | MR. DREEBEN | privacy | Once the -- once the effect is in the house, under Karo there is an expectation of privacy that cannot be breached without a warrant, and we're not asking the Court to overrule that. |
| 0:19:36.260 | 1176.260 | MR. DREEBEN | warrant | Once the -- once the effect is in the house, under Karo there is an expectation of privacy that cannot be breached without a warrant, and we're not asking the Court to overrule that. |
| 0:19:41.960 | 1181.960 | JUSTICE SOTOMAYOR | warrant | Tell me what the difference between this and a general warrant is? |
| 0:19:44.627 | 1184.627 | MR. DREEBEN | warrant | A general warrant -- |
| 0:19:54.060 | 1194.060 | JUSTICE SOTOMAYOR | our | -- what motivated the Fourth Amendment historically was the disapproval, the outrage, that our Founding Fathers experienced with general warrants that permitted police indiscriminately to investigate just on the basis of suspicion, not probable cause, and to invade every possession that the individual had in search of a crime. |
| 0:19:57.200 | 1197.200 | JUSTICE SOTOMAYOR | warrant | -- what motivated the Fourth Amendment historically was the disapproval, the outrage, that our Founding Fathers experienced with general warrants that permitted police indiscriminately to investigate just on the basis of suspicion, not probable cause, and to invade every possession that the individual had in search of a crime. |
| 0:19:58.780 | 1198.780 | JUSTICE SOTOMAYOR | police | -- what motivated the Fourth Amendment historically was the disapproval, the outrage, that our Founding Fathers experienced with general warrants that permitted police indiscriminately to investigate just on the basis of suspicion, not probable cause, and to invade every possession that the individual had in search of a crime. |
| 0:20:15.207 | 1215.207 | MR. DREEBEN | warrant | A warrant authorizes -- |
| 0:20:25.880 | 1225.880 | MR. DREEBEN | warrant | A warrant authorizes a search. |
| 0:20:30.880 | 1230.880 | MR. DREEBEN | track | This authorizes the ability to track somebody's movements in a car on a public roadway, a subject as to which this Court said in Knotts that no individual has a reasonable expectation of privacy because when they go out in their car, their car is traveling on public roads. |
| 0:20:32.680 | 1232.680 | MR. DREEBEN | car | This authorizes the ability to track somebody's movements in a car on a public roadway, a subject as to which this Court said in Knotts that no individual has a reasonable expectation of privacy because when they go out in their car, their car is traveling on public roads. |
| 0:20:40.740 | 1240.740 | MR. DREEBEN | privacy | This authorizes the ability to track somebody's movements in a car on a public roadway, a subject as to which this Court said in Knotts that no individual has a reasonable expectation of privacy because when they go out in their car, their car is traveling on public roads. |
| 0:20:47.300 | 1247.300 | MR. DREEBEN | police | The police have no obligation to avert their eyes from anything that any member of the public -- |
| 0:20:57.520 | 1257.520 | CHIEF JUSTICE ROBERTS | privacy | Does the reasonable expectation of privacy trump that fact? |
| 0:21:04.680 | 1264.680 | CHIEF JUSTICE ROBERTS | privacy | In other words, if we ask people, do you think it's -- it violates your right to privacy to have this kind of information acquired, and everybody says yes, is it a response that, no, that takes place in public, or is it simply the reasonable expectation of privacy regardless of the fact that it takes place in public? |
| 0:21:07.820 | 1267.820 | CHIEF JUSTICE ROBERTS | everybody | In other words, if we ask people, do you think it's -- it violates your right to privacy to have this kind of information acquired, and everybody says yes, is it a response that, no, that takes place in public, or is it simply the reasonable expectation of privacy regardless of the fact that it takes place in public? |
| 0:21:23.840 | 1283.840 | MR. DREEBEN | privacy | Well, something that takes place in public isn't inherently off limits to a reasonable expectation of privacy. |
| 0:21:33.220 | 1293.220 | MR. DREEBEN | privacy | You go into a phone booth, you're in public; making your calls within the phone booth is subject to a reasonable expectation of privacy. |
| 0:21:40.220 | 1300.220 | MR. DREEBEN | vehicle | But this Court, with full awareness of that holding, in Knotts and in Karo recognized that surveillance of a vehicle traveling on the public roadways doesn't fit that description. |
| 0:21:48.420 | 1308.420 | CHIEF JUSTICE ROBERTS | privacy | You can see, though, can't you, that 30 years ago if you asked people does it violate your privacy to be followed by a beeper, the police following you, you might get one answer, while today if you ask people does it violate your right to privacy to know that the police can have a record of every movement you made in the past month, they might see that differently? |
| 0:21:49.660 | 1309.660 | CHIEF JUSTICE ROBERTS | follow | You can see, though, can't you, that 30 years ago if you asked people does it violate your privacy to be followed by a beeper, the police following you, you might get one answer, while today if you ask people does it violate your right to privacy to know that the police can have a record of every movement you made in the past month, they might see that differently? |
| 0:21:50.340 | 1310.340 | CHIEF JUSTICE ROBERTS | beeper | You can see, though, can't you, that 30 years ago if you asked people does it violate your privacy to be followed by a beeper, the police following you, you might get one answer, while today if you ask people does it violate your right to privacy to know that the police can have a record of every movement you made in the past month, they might see that differently? |
| 0:21:51.540 | 1311.540 | CHIEF JUSTICE ROBERTS | police | You can see, though, can't you, that 30 years ago if you asked people does it violate your privacy to be followed by a beeper, the police following you, you might get one answer, while today if you ask people does it violate your right to privacy to know that the police can have a record of every movement you made in the past month, they might see that differently? |
| 0:22:01.180 | 1321.180 | CHIEF JUSTICE ROBERTS | month | You can see, though, can't you, that 30 years ago if you asked people does it violate your privacy to be followed by a beeper, the police following you, you might get one answer, while today if you ask people does it violate your right to privacy to know that the police can have a record of every movement you made in the past month, they might see that differently? |
| 0:22:06.760 | 1326.760 | MR. DREEBEN | follow | They probably would also feel differently about being followed 24/7 by a team of FBI agents, who gain far more information than a GPS device produces. |
| 0:22:12.720 | 1332.720 | MR. DREEBEN | GPS | They probably would also feel differently about being followed 24/7 by a team of FBI agents, who gain far more information than a GPS device produces. |
| 0:22:13.080 | 1333.080 | MR. DREEBEN | device | They probably would also feel differently about being followed 24/7 by a team of FBI agents, who gain far more information than a GPS device produces. |
| 0:22:14.440 | 1334.440 | MR. DREEBEN | GPS | GPS only gives you the approximate location of the car as it drives on the roads -- |
| 0:22:17.120 | 1337.120 | MR. DREEBEN | car | GPS only gives you the approximate location of the car as it drives on the roads -- |
| 0:22:26.180 | 1346.180 | MR. DREEBEN | GPS | The approximate speed, the location traveled, the -- that -- that is what the GPS provides. |
| 0:22:29.020 | 1349.020 | MR. DREEBEN | car | It doesn't show you where the car stopped. |
| 0:22:31.540 | 1351.540 | MR. DREEBEN | car | It doesn't show you who was driving the car. |
| 0:22:43.420 | 1363.420 | MR. DREEBEN | police | Well, this Court held in Whren v. United States that when the police have probable cause to stop someone for a traffic violation, they can do that. |
| 0:22:51.400 | 1371.400 | JUSTICE GINSBURG | police | That was -- that is when the police came upon the violator. |
| 0:22:57.540 | 1377.540 | JUSTICE GINSBURG | police | The police can say we want to find out more about X, so consult the database, see if there's an indication that he was ever speeding in the last 28 days. |
| 0:23:14.640 | 1394.640 | MR. DREEBEN | police | Justice Ginsburg, it's not very hard for police to follow somebody and find a traffic violation if they want to do that. |
| 0:23:15.080 | 1395.080 | MR. DREEBEN | follow | Justice Ginsburg, it's not very hard for police to follow somebody and find a traffic violation if they want to do that. |
| 0:23:49.020 | 1429.020 | MR. DREEBEN | GPS | If this Court believes that there is an excessive chill created by an actual law or universal practice of monitoring people through GPS, there are other constitutional principles that are available. |
| 0:23:53.560 | 1433.560 | JUSTICE GINSBURG | us | But the Fourth Amendment protects us against unreasonable searches and seizures. |
| 0:24:11.900 | 1451.900 | JUSTICE GINSBURG | police | And if I were trying to explain to someone, here's the Fourth Amendment, the Fourth Amendment says -- or it has been interpreted to mean that if I'm on a public bus and the police want to feel my luggage, that's a violation; and yet, this kind of monitoring, installing the GPS and monitoring the person's movement whenever they are outside their house in the car, is not? |
| 0:24:20.880 | 1460.880 | JUSTICE GINSBURG | GPS | And if I were trying to explain to someone, here's the Fourth Amendment, the Fourth Amendment says -- or it has been interpreted to mean that if I'm on a public bus and the police want to feel my luggage, that's a violation; and yet, this kind of monitoring, installing the GPS and monitoring the person's movement whenever they are outside their house in the car, is not? |
| 0:24:27.060 | 1467.060 | JUSTICE GINSBURG | car | And if I were trying to explain to someone, here's the Fourth Amendment, the Fourth Amendment says -- or it has been interpreted to mean that if I'm on a public bus and the police want to feel my luggage, that's a violation; and yet, this kind of monitoring, installing the GPS and monitoring the person's movement whenever they are outside their house in the car, is not? |
| 0:24:40.200 | 1480.200 | MR. DREEBEN | police | I'm quite sure, Justice Ginsburg, that if you ask citizens whether the police could freely pick up their trash for a month and paw through it, looking for evidence of a crime, or keep a record of every telephone call that they made for the duration and the number that it went through, or conduct intense visual surveillance of them, that citizens would probably also find that to be, in the word that Respondents choose to use -- |
| 0:24:42.340 | 1482.340 | MR. DREEBEN | month | I'm quite sure, Justice Ginsburg, that if you ask citizens whether the police could freely pick up their trash for a month and paw through it, looking for evidence of a crime, or keep a record of every telephone call that they made for the duration and the number that it went through, or conduct intense visual surveillance of them, that citizens would probably also find that to be, in the word that Respondents choose to use -- |
| 0:25:15.900 | 1515.900 | JUSTICE BREYER | track | Start -- what would a democratic society look like if a large number of people did think that the government was tracking their every movement over long periods of time. |
| 0:25:15.900 | 1515.900 | JUSTICE BREYER | tracking | Start -- what would a democratic society look like if a large number of people did think that the government was tracking their every movement over long periods of time. |
| 0:25:54.680 | 1554.680 | MR. DREEBEN | 1984 | First of all, I think the line-drawing problems that the Court would create for itself would be intolerable, and better that the Court should address the so-called 1984 scenarios if they come to pass, rather than using this case as a vehicle for doing so. |
| 0:25:57.760 | 1557.760 | MR. DREEBEN | us | First of all, I think the line-drawing problems that the Court would create for itself would be intolerable, and better that the Court should address the so-called 1984 scenarios if they come to pass, rather than using this case as a vehicle for doing so. |
| 0:25:58.960 | 1558.960 | MR. DREEBEN | vehicle | First of all, I think the line-drawing problems that the Court would create for itself would be intolerable, and better that the Court should address the so-called 1984 scenarios if they come to pass, rather than using this case as a vehicle for doing so. |
| 0:26:03.200 | 1563.200 | JUSTICE SOTOMAYOR | vehicle | This case is not that vehicle. |
| 0:26:05.260 | 1565.260 | JUSTICE SOTOMAYOR | GPS | The GPS technology today is limited only by the cost of the instrument, which frankly right now is so small that it wouldn't take that much of a budget, local budget, to place a GPS on every car in the nation. |
| 0:26:18.360 | 1578.360 | JUSTICE SOTOMAYOR | car | The GPS technology today is limited only by the cost of the instrument, which frankly right now is so small that it wouldn't take that much of a budget, local budget, to place a GPS on every car in the nation. |
| 0:26:20.480 | 1580.480 | JUSTICE SOTOMAYOR | car | Almost every car has it now. |
| 0:26:24.740 | 1584.740 | MR. DREEBEN | track | Well, I think it would be virtually impossible to use the kinds of tracking devices that were used in this case on everyone because -- |
| 0:26:24.740 | 1584.740 | MR. DREEBEN | tracking | Well, I think it would be virtually impossible to use the kinds of tracking devices that were used in this case on everyone because -- |
| 0:26:25.020 | 1585.020 | MR. DREEBEN | device | Well, I think it would be virtually impossible to use the kinds of tracking devices that were used in this case on everyone because -- |
| 0:26:25.980 | 1585.980 | MR. DREEBEN | us | Well, I think it would be virtually impossible to use the kinds of tracking devices that were used in this case on everyone because -- |
| 0:26:48.060 | 1608.060 | MR. DREEBEN | police | I think that -- Justice Scalia, the legislature is a safeguard, and if the Court believes that there needs to be a Fourth Amendment safeguard as well, we have urged as a fallback position that the Court adopt a reasonable suspicion standard which would allow the police to conduct surveillance of individuals in their movements on public roadways, which they can do visually in any event, and would allow the police to investigate leads and tips that arise under circumstances where there is not probable cause. |
| 0:27:10.560 | 1630.560 | MR. DREEBEN | police | As in most reasonable suspicion cases, it's the police at the front end and it's the courts at the back end if there are motions to suppress evidence. |
| 0:27:31.340 | 1651.340 | MR. DREEBEN | 1984 | But fundamentally, just as in the pen register example and in the financial records example, if this Court concludes, consistent with its earlier cases, that this is not a search, yet all Americans find it to be an omen of 1984, Congress would stand ready to provide appropriate protection. |
| 0:27:39.800 | 1659.800 | CHIEF JUSTICE ROBERTS | our | Your -- our questions have eaten into your rebuttal time. |
| 0:27:59.260 | 1679.260 | MR. LECKAR | police | This case can be resolved on a very narrow basis, a very narrow basis: What are the consequences when the police without a warrant install a GPS secretly on the car of any citizen of the United States, and they want to use the evidence gained that way in a criminal trial? |
| 0:28:00.620 | 1680.620 | MR. LECKAR | warrant | This case can be resolved on a very narrow basis, a very narrow basis: What are the consequences when the police without a warrant install a GPS secretly on the car of any citizen of the United States, and they want to use the evidence gained that way in a criminal trial? |
| 0:28:01.680 | 1681.680 | MR. LECKAR | GPS | This case can be resolved on a very narrow basis, a very narrow basis: What are the consequences when the police without a warrant install a GPS secretly on the car of any citizen of the United States, and they want to use the evidence gained that way in a criminal trial? |
| 0:28:03.600 | 1683.600 | MR. LECKAR | car | This case can be resolved on a very narrow basis, a very narrow basis: What are the consequences when the police without a warrant install a GPS secretly on the car of any citizen of the United States, and they want to use the evidence gained that way in a criminal trial? |
| 0:28:09.740 | 1689.740 | MR. LECKAR | our | Our position is that's a seizure. |
| 0:28:13.780 | 1693.780 | JUSTICE ALITO | device | What is the size of this device? |
| 0:28:16.240 | 1696.240 | JUSTICE ALITO | device | What is the size of this device? |
| 0:28:24.800 | 1704.800 | MR. LECKAR | GPS | In -- the record doesn't show in this case, but we know -- we learned last week, Justice Alito, from the NACDL that there's now a GPS on the market that weighs 2 ounces and is the size of a credit card. |
| 0:28:37.440 | 1717.440 | MR. LECKAR | vehicle | Think how easy it would be for any law enforcement agent of the 880,000 in the United States to stick one of those on anybody's vehicle. |
| 0:29:17.320 | 1757.320 | MR. LECKAR | everybody | Everybody agrees here that there is -- that Antoine Jones had the right to control the use of his vehicle. |
| 0:29:23.440 | 1763.440 | MR. LECKAR | vehicle | Everybody agrees here that there is -- that Antoine Jones had the right to control the use of his vehicle. |
| 0:29:34.340 | 1774.340 | CHIEF JUSTICE ROBERTS | GPS | What is your position on the placement of the GPS device on the State-owned license plate? |
| 0:29:34.700 | 1774.700 | CHIEF JUSTICE ROBERTS | device | What is your position on the placement of the GPS device on the State-owned license plate? |
| 0:29:58.380 | 1798.380 | MR. LECKAR | GPS | Well, first of all, Justice -- Chief Justice Roberts, my -- you would probably see the GPS, and in that case, you might have -- |
| 0:30:08.040 | 1808.040 | MR. LECKAR | GPS | In that particular case, what you have done is you have -- the installation of the GPS, it is a seizure. |
| 0:30:13.300 | 1813.300 | MR. LECKAR | GPS | What makes it meaningful is the use of that GPS -- |
| 0:30:21.760 | 1821.760 | JUSTICE SCALIA | car | Look at -- you give the State permission to put the license plate -- to carry -- to have your car carry the State's license plate. |
| 0:30:27.360 | 1827.360 | JUSTICE SCALIA | car | You do not give anybody permission to have your car carry a tracking device. |
| 0:30:28.520 | 1828.520 | JUSTICE SCALIA | track | You do not give anybody permission to have your car carry a tracking device. |
| 0:30:28.520 | 1828.520 | JUSTICE SCALIA | tracking | You do not give anybody permission to have your car carry a tracking device. |
| 0:30:28.940 | 1828.940 | JUSTICE SCALIA | device | You do not give anybody permission to have your car carry a tracking device. |
| 0:30:31.480 | 1831.480 | JUSTICE SCALIA | car | And whether it's put directly on the car or directly on something that the car is carrying doesn't seem to me to make any difference. |
| 0:30:58.740 | 1858.740 | MR. LECKAR | car | If you put it on somebody's briefcase, you put it on somebody's car, you have affected their possessory interest. |
| 0:31:08.840 | 1868.840 | JUSTICE KAGAN | car | Mr. Leckar, I guess I'm not sure I quite understand the argument, because a trespass is accomplished no matter what you put on somebody's car or somebody's overcoat or what have you. |
| 0:31:12.920 | 1872.920 | JUSTICE KAGAN | device | You could put a nonworking device in somebody's car, and it would still be a trespass, but surely the same constitutional problem is not raised. |
| 0:31:14.760 | 1874.760 | JUSTICE KAGAN | car | You could put a nonworking device in somebody's car, and it would still be a trespass, but surely the same constitutional problem is not raised. |
| 0:31:36.200 | 1896.200 | MR. LECKAR | GPS | As I said moments ago, what makes it meaningful, what makes it a meaningful deprivation of a -- of a possessory interest, is once the GPS gets activated. |
| 0:31:39.040 | 1899.040 | MR. LECKAR | follow | We follow what Silverman v. -- |
| 0:31:58.620 | 1918.620 | JUSTICE SCALIA | vehicle | You have to stop the person or stop the vehicle. |
| 0:32:01.900 | 1921.900 | JUSTICE SCALIA | track | What has been seized when you -- when you slap a tracking device on a car? |
| 0:32:01.900 | 1921.900 | JUSTICE SCALIA | tracking | What has been seized when you -- when you slap a tracking device on a car? |
| 0:32:02.200 | 1922.200 | JUSTICE SCALIA | device | What has been seized when you -- when you slap a tracking device on a car? |
| 0:32:02.900 | 1922.900 | JUSTICE SCALIA | car | What has been seized when you -- when you slap a tracking device on a car? |
| 0:32:08.840 | 1928.840 | MR. LECKAR | GPS | Data is seized that is created by the GPS. |
| 0:32:12.440 | 1932.440 | MR. LECKAR | vehicle | Antoine Jones had the right, Your Honor, to control the use of his vehicle. |
| 0:32:41.480 | 1961.480 | JUSTICE BREYER | everybody | So, you already have -- everybody agrees it's at least a search. |
| 0:33:10.020 | 1990.020 | JUSTICE BREYER | police | And I would like to know from you -- what they are saying is that the parade of horribles we can worry with -- worry about when it comes up; the police have many, many people that they suspect of all kinds of things ranging from kidnappings of lost children to terrorism to all kinds of crimes. |
| 0:33:27.480 | 2007.480 | JUSTICE BREYER | 1984 | And they say at least with that, you will avoid the 1984 scenario, and you will in fact allow the police to do their work with doing no more than subjecting the person to really good knowledge of where he's going on the open highway. |
| 0:33:32.360 | 2012.360 | JUSTICE BREYER | police | And they say at least with that, you will avoid the 1984 scenario, and you will in fact allow the police to do their work with doing no more than subjecting the person to really good knowledge of where he's going on the open highway. |
| 0:34:12.100 | 2052.100 | MR. LECKAR | device | That said, what -- what happened here, society does not view as reasonable the concept that the United States Government has the right to take a device that enables them to engage in pervasive, limitless, cost-free -- cost-free surveillance -- that completely replaces the human equation -- |
| 0:34:23.240 | 2063.240 | JUSTICE KENNEDY | police | Suppose the police department says: We've got two things; we can put 30 deputies on this route and watch this person, or we can have a device with a warrant. |
| 0:34:32.260 | 2072.260 | JUSTICE KENNEDY | device | Suppose the police department says: We've got two things; we can put 30 deputies on this route and watch this person, or we can have a device with a warrant. |
| 0:34:33.760 | 2073.760 | JUSTICE KENNEDY | warrant | Suppose the police department says: We've got two things; we can put 30 deputies on this route and watch this person, or we can have a device with a warrant. |
| 0:34:38.760 | 2078.760 | MR. LECKAR | police | What happens is the police have the capacity with GPS to engage in grave abuse, grave abuse of individual and group liberties, Your Honor. |
| 0:34:41.120 | 2081.120 | MR. LECKAR | GPS | What happens is the police have the capacity with GPS to engage in grave abuse, grave abuse of individual and group liberties, Your Honor. |
| 0:35:03.260 | 2103.260 | MR. LECKAR | GPS | Yes, if they use a GPS, Your Honor. |
| 0:35:05.440 | 2105.440 | MR. LECKAR | GPS | Any placement of a GPS on anybody's car or this car -- |
| 0:35:06.800 | 2106.800 | MR. LECKAR | car | Any placement of a GPS on anybody's car or this car -- |
| 0:35:26.740 | 2126.740 | JUSTICE KENNEDY | police | And it seems to me what you're saying is that the police have to use the most inefficient methods. |
| 0:35:32.400 | 2132.400 | JUSTICE KENNEDY | 1984 | I'm fully aware of the 1984 ministry of love, ministry of -- of peace problem. |
| 0:35:52.500 | 2152.500 | MR. LECKAR | police | We're not asking to make the police less efficient than they were before GPS came into effect. |
| 0:35:54.300 | 2154.300 | MR. LECKAR | GPS | We're not asking to make the police less efficient than they were before GPS came into effect. |
| 0:35:58.640 | 2158.640 | MR. LECKAR | GPS | We're simply saying that the use of GPS has grave potential -- grave threats of abuse to privacy; that people have an expectation, Justice Kennedy, that their neighbor is not going to use their car to track them. |
| 0:36:03.340 | 2163.340 | MR. LECKAR | privacy | We're simply saying that the use of GPS has grave potential -- grave threats of abuse to privacy; that people have an expectation, Justice Kennedy, that their neighbor is not going to use their car to track them. |
| 0:36:10.460 | 2170.460 | MR. LECKAR | car | We're simply saying that the use of GPS has grave potential -- grave threats of abuse to privacy; that people have an expectation, Justice Kennedy, that their neighbor is not going to use their car to track them. |
| 0:36:11.120 | 2171.120 | MR. LECKAR | track | We're simply saying that the use of GPS has grave potential -- grave threats of abuse to privacy; that people have an expectation, Justice Kennedy, that their neighbor is not going to use their car to track them. |
| 0:36:19.080 | 2179.080 | MR. LECKAR | car | Antoine Jones had control of that car. |
| 0:36:21.080 | 2181.080 | MR. LECKAR | vehicle | Control of that -- of the vehicle meant that he had a reasonable expectation that society is prepared to view as objectively reasonable. |
| 0:36:52.660 | 2212.660 | MR. LECKAR | car | You have an invasion of his possessory interest, placement on the car. |
| 0:37:07.740 | 2227.740 | MR. LECKAR | police | We're not saying that the police are prohibited from having individual video cameras or several video cameras to surveil people. |
| 0:37:15.620 | 2235.620 | MR. LECKAR | device | What we're saying here is this device, this device that enables limitless, pervasive, indiscriminate -- |
| 0:37:31.320 | 2251.320 | JUSTICE KAGAN | police | I'm told -- maybe this is wrong, but I'm told that if somebody goes to London, almost every place that person goes there's a camera taking pictures, so that the police can put together snapshots of where everybody is all the time. |
| 0:37:34.040 | 2254.040 | JUSTICE KAGAN | everybody | I'm told -- maybe this is wrong, but I'm told that if somebody goes to London, almost every place that person goes there's a camera taking pictures, so that the police can put together snapshots of where everybody is all the time. |
| 0:37:55.020 | 2275.020 | JUSTICE BREYER | track | And, in fact, those cameras in London actually enabled them, if you watched, I got the impression, to track the bomber who was going to blow up the airport in Glasgow and to stop him before he did. |
| 0:38:13.640 | 2293.640 | JUSTICE BREYER | us | But that isn't the issue exactly in front of us. |
| 0:39:24.600 | 2364.600 | JUSTICE KENNEDY | us | You don't want us to do that. |
| 0:39:35.160 | 2375.160 | MR. LECKAR | GPS | Well, but technology, as you observed, Justice Kennedy, is dramatically different with GPS than was present in Karo. |
| 0:39:55.720 | 2395.720 | JUSTICE SOTOMAYOR | track | I don't see that far in the future when those cameras are going to be able to show you the entire world and let you track somebody on the camera from place to place. |
| 0:40:00.360 | 2400.360 | JUSTICE SOTOMAYOR | us | So, if -- give us a theory. |
| 0:40:02.480 | 2402.480 | JUSTICE SOTOMAYOR | police | Is that okay for the police to access those cameras and look at you moving from place to place? |
| 0:40:15.500 | 2415.500 | MR. LECKAR | our | Our theory, Justice Sotomayor, with respect to video camera, if they're targeting an individual -- this presents a grave question. |
| 0:40:29.000 | 2429.000 | MR. LECKAR | police | But if the Court wanted to address that question, once the police target somebody, they want to engage in individualized targeting for use of a pervasive network of cameras, and GPS is like a million cameras. |
| 0:40:36.700 | 2436.700 | MR. LECKAR | GPS | But if the Court wanted to address that question, once the police target somebody, they want to engage in individualized targeting for use of a pervasive network of cameras, and GPS is like a million cameras. |
| 0:40:48.140 | 2448.140 | MR. LECKAR | track | It's 28 cameras, but the equivalent of a camera tracking you every street corner you're on everywhere. |
| 0:40:48.140 | 2448.140 | MR. LECKAR | tracking | It's 28 cameras, but the equivalent of a camera tracking you every street corner you're on everywhere. |
| 0:40:58.060 | 2458.060 | MR. LECKAR | warrant | Once you have individualized suspicion like that, if a court wanted to deal with it, I believe you would have to have a warrant. |
| 0:41:08.420 | 2468.420 | JUSTICE SCALIA | us | The issue before us is not -- not in the abstract whether this police conduct is unreasonable. |
| 0:41:11.840 | 2471.840 | JUSTICE SCALIA | police | The issue before us is not -- not in the abstract whether this police conduct is unreasonable. |
| 0:41:23.700 | 2483.700 | JUSTICE SCALIA | our | And our cases have said that there's no search when -- when you are in public and where everything that you do is open to -- to the view of people. |
| 0:41:40.880 | 2500.880 | JUSTICE SCALIA | police | That's not what the Fourth Amendment says, the police can't do anything that's unreasonable. |
| 0:41:58.700 | 2518.700 | JUSTICE SCALIA | privacy | But you have to establish, if you're going to go with Katz, that there has been an invasion of -- of privacy when all that -- all that this is showing is where the car is going on the public streets, where the police could have had round-the-clock surveillance on this individual for a whole month or for 2 months or for 3 months, and that would not have violated anything, would it? |
| 0:42:02.720 | 2522.720 | JUSTICE SCALIA | car | But you have to establish, if you're going to go with Katz, that there has been an invasion of -- of privacy when all that -- all that this is showing is where the car is going on the public streets, where the police could have had round-the-clock surveillance on this individual for a whole month or for 2 months or for 3 months, and that would not have violated anything, would it? |
| 0:42:05.440 | 2525.440 | JUSTICE SCALIA | police | But you have to establish, if you're going to go with Katz, that there has been an invasion of -- of privacy when all that -- all that this is showing is where the car is going on the public streets, where the police could have had round-the-clock surveillance on this individual for a whole month or for 2 months or for 3 months, and that would not have violated anything, would it? |
| 0:42:09.740 | 2529.740 | JUSTICE SCALIA | month | But you have to establish, if you're going to go with Katz, that there has been an invasion of -- of privacy when all that -- all that this is showing is where the car is going on the public streets, where the police could have had round-the-clock surveillance on this individual for a whole month or for 2 months or for 3 months, and that would not have violated anything, would it? |
| 0:42:17.700 | 2537.700 | JUSTICE SCALIA | privacy | Because there's no invasion of privacy. |
| 0:42:20.180 | 2540.180 | JUSTICE SCALIA | privacy | So, why is this an invasion of privacy? |
| 0:42:42.080 | 2562.080 | JUSTICE SCALIA | privacy | If -- if there is no invasion of privacy for 1 day, there's no invasion of privacy for a hundred days. |
| 0:42:47.060 | 2567.060 | JUSTICE SCALIA | police | Now, it may be unreasonable police conduct, and we can handle that with laws. |
| 0:42:51.300 | 2571.300 | JUSTICE SCALIA | privacy | But if there's no invasion of privacy, no matter how many days you do it, there's no invasion of privacy. |
| 0:43:01.980 | 2581.980 | MR. LECKAR | GPS | A GPS in your car is like -- or anybody's car, is like -- without a warrant, is like having an -- it makes you unable to get rid of an uninvited stranger. |
| 0:43:02.980 | 2582.980 | MR. LECKAR | car | A GPS in your car is like -- or anybody's car, is like -- without a warrant, is like having an -- it makes you unable to get rid of an uninvited stranger. |
| 0:43:05.700 | 2585.700 | MR. LECKAR | warrant | A GPS in your car is like -- or anybody's car, is like -- without a warrant, is like having an -- it makes you unable to get rid of an uninvited stranger. |
| 0:43:14.840 | 2594.840 | JUSTICE SCALIA | police | So is a tail when the police surveil -- surveil you for -- for a month. |
| 0:43:17.600 | 2597.600 | JUSTICE SCALIA | month | So is a tail when the police surveil -- surveil you for -- for a month. |
| 0:43:25.300 | 2605.300 | MR. LECKAR | GPS | But what a GPS does, it involves -- it allows the government to engage in unlimited surveillance through a machine, through a machine robotically. |
| 0:43:37.420 | 2617.420 | MR. LECKAR | police | The record in this case showed that many times the police officers just let -- let the machine go on. |
| 0:43:42.080 | 2622.080 | JUSTICE ALITO | GPS | Suppose that the GPS was used only to track somebody's movements for 1 day or for 12 hours or for 3 hours. |
| 0:43:42.920 | 2622.920 | JUSTICE ALITO | us | Suppose that the GPS was used only to track somebody's movements for 1 day or for 12 hours or for 3 hours. |
| 0:43:43.780 | 2623.780 | JUSTICE ALITO | track | Suppose that the GPS was used only to track somebody's movements for 1 day or for 12 hours or for 3 hours. |
| 0:43:50.380 | 2630.380 | MR. LECKAR | our | Our position, Justice Alito, is no circumstances should a GPS be allowed to be put on somebody's car. |
| 0:43:55.340 | 2635.340 | MR. LECKAR | GPS | Our position, Justice Alito, is no circumstances should a GPS be allowed to be put on somebody's car. |
| 0:43:57.120 | 2637.120 | MR. LECKAR | car | Our position, Justice Alito, is no circumstances should a GPS be allowed to be put on somebody's car. |
| 0:44:03.500 | 2643.500 | MR. LECKAR | our | Our view is the -- the use of a GPS as a search in and of itself should be -- is -- should be viewed as unreasonable. |
| 0:44:05.080 | 2645.080 | MR. LECKAR | GPS | Our view is the -- the use of a GPS as a search in and of itself should be -- is -- should be viewed as unreasonable. |
| 0:44:14.560 | 2654.560 | MR. LECKAR | our | But if the Court were uncomfortable with that, if the Court had concerns with that, we suggested in our brief some -- some possibilities: One day, one trip, one person per day or trip, or perhaps when you use it exactly as a beeper, when you follow it, when you actually physically follow it. |
| 0:44:24.960 | 2664.960 | MR. LECKAR | beeper | But if the Court were uncomfortable with that, if the Court had concerns with that, we suggested in our brief some -- some possibilities: One day, one trip, one person per day or trip, or perhaps when you use it exactly as a beeper, when you follow it, when you actually physically follow it. |
| 0:44:25.540 | 2665.540 | MR. LECKAR | follow | But if the Court were uncomfortable with that, if the Court had concerns with that, we suggested in our brief some -- some possibilities: One day, one trip, one person per day or trip, or perhaps when you use it exactly as a beeper, when you follow it, when you actually physically follow it. |
| 0:44:30.580 | 2670.580 | JUSTICE ALITO | follow | But what is the difference between following somebody for 12 hours, let's say, and monitoring their movements on a GPS for 12 hours? |
| 0:44:34.720 | 2674.720 | JUSTICE ALITO | GPS | But what is the difference between following somebody for 12 hours, let's say, and monitoring their movements on a GPS for 12 hours? |
| 0:44:44.760 | 2684.760 | MR. LECKAR | privacy | Because it's an unreasonable invasion of privacy, Your Honor. |
| 0:44:49.080 | 2689.080 | JUSTICE ALITO | privacy | There's no more -- what -- what is the difference in terms of one's privacy whether you're followed by a police officer for 12 hours and you don't see the officer or whether you're monitored by GPS for 12 hours? |
| 0:44:49.960 | 2689.960 | JUSTICE ALITO | follow | There's no more -- what -- what is the difference in terms of one's privacy whether you're followed by a police officer for 12 hours and you don't see the officer or whether you're monitored by GPS for 12 hours? |
| 0:44:51.220 | 2691.220 | JUSTICE ALITO | police | There's no more -- what -- what is the difference in terms of one's privacy whether you're followed by a police officer for 12 hours and you don't see the officer or whether you're monitored by GPS for 12 hours? |
| 0:44:56.080 | 2696.080 | JUSTICE ALITO | GPS | There's no more -- what -- what is the difference in terms of one's privacy whether you're followed by a police officer for 12 hours and you don't see the officer or whether you're monitored by GPS for 12 hours? |
| 0:45:01.700 | 2701.700 | MR. LECKAR | police | Because -- because what you have here is society does not expect that the police, the human element, would be taken out of -- would be taken out of the surveillance factor. |
| 0:45:12.480 | 2712.480 | JUSTICE ALITO | privacy | Technology is changing people's expectations of privacy. |
| 0:45:19.340 | 2719.340 | JUSTICE ALITO | us | Suppose we look forward 10 years, and maybe 10 years from now 90 percent of the population will be using social networking sites, and they will have on average 500 friends, and they will have allowed their friends to monitor their location 24 hours a day, 365 days a year, through the use of their cell phones. |
| 0:45:37.100 | 2737.100 | JUSTICE ALITO | privacy | Then -- what would the expectation of privacy be then? |
| 0:45:45.140 | 2745.140 | MR. LECKAR | privacy | As Justice Kennedy observed in Quon, cell phones are becoming so ubiquitous, there may be privacy interests. |
| 0:45:46.260 | 2746.260 | MR. LECKAR | our | Our view is that currently the use of a cell phone, that's a voluntary act. |
| 0:46:00.520 | 2760.520 | MR. LECKAR | us | But I started my oral argument with this basic precept, Justice Alito: This case does not require us to decide those issues of emerging technology. |
| 0:46:06.720 | 2766.720 | MR. LECKAR | police | It's a simple case at the core: Should the police be allowed surreptitiously to put these machines on people's cars and either -- call it a seizure, call it a search, call it a search and seizure in the words of Katz, or call it a Fourth Amendment violation. |
| 0:46:11.120 | 2771.120 | MR. LECKAR | car | It's a simple case at the core: Should the police be allowed surreptitiously to put these machines on people's cars and either -- call it a seizure, call it a search, call it a search and seizure in the words of Katz, or call it a Fourth Amendment violation. |
| 0:46:11.120 | 2771.120 | MR. LECKAR | cars | It's a simple case at the core: Should the police be allowed surreptitiously to put these machines on people's cars and either -- call it a seizure, call it a search, call it a search and seizure in the words of Katz, or call it a Fourth Amendment violation. |
| 0:46:25.460 | 2785.460 | JUSTICE ALITO | police | But I just wonder, would Mr. Jones or anybody else be really upset if they found that the police had sneaked up to their car and put an inert device the size of a credit card on the underside of the car? |
| 0:46:27.160 | 2787.160 | JUSTICE ALITO | car | But I just wonder, would Mr. Jones or anybody else be really upset if they found that the police had sneaked up to their car and put an inert device the size of a credit card on the underside of the car? |
| 0:46:29.360 | 2789.360 | JUSTICE ALITO | device | But I just wonder, would Mr. Jones or anybody else be really upset if they found that the police had sneaked up to their car and put an inert device the size of a credit card on the underside of the car? |
| 0:46:37.160 | 2797.160 | JUSTICE ALITO | police | What would they say about that, other than the fact that the police are wasting money doing this? |
| 0:46:47.880 | 2807.880 | JUSTICE ALITO | car | They put it under the car. |
| 0:47:05.020 | 2825.020 | JUSTICE ALITO | car | So, what's you're concerned about is not this little thing that's put on your car. |
| 0:47:17.120 | 2837.120 | JUSTICE KAGAN | police | But to ask Justice Alito's question in a different way, suppose that the police could do this without ever committing the trespass. |
| 0:47:22.200 | 2842.200 | JUSTICE KAGAN | car | Suppose that in the future all cars are going to have GPS tracking systems, and the police could essentially hack into such a system without committing the trespass. |
| 0:47:22.200 | 2842.200 | JUSTICE KAGAN | cars | Suppose that in the future all cars are going to have GPS tracking systems, and the police could essentially hack into such a system without committing the trespass. |
| 0:47:23.260 | 2843.260 | JUSTICE KAGAN | GPS | Suppose that in the future all cars are going to have GPS tracking systems, and the police could essentially hack into such a system without committing the trespass. |
| 0:47:23.760 | 2843.760 | JUSTICE KAGAN | track | Suppose that in the future all cars are going to have GPS tracking systems, and the police could essentially hack into such a system without committing the trespass. |
| 0:47:23.760 | 2843.760 | JUSTICE KAGAN | tracking | Suppose that in the future all cars are going to have GPS tracking systems, and the police could essentially hack into such a system without committing the trespass. |
| 0:47:25.100 | 2845.100 | JUSTICE KAGAN | police | Suppose that in the future all cars are going to have GPS tracking systems, and the police could essentially hack into such a system without committing the trespass. |
| 0:47:42.920 | 2862.920 | MR. LECKAR | privacy | They would know that their privacy rights had been taken away. |
| 0:48:06.820 | 2886.820 | MR. LECKAR | GPS | Justice Alito, what happens here, GPS produces unique data. |
| 0:48:11.520 | 2891.520 | MR. LECKAR | GPS | When you and I drive down the street, we don't emit GPS data. |
| 0:48:13.520 | 2893.520 | MR. LECKAR | GPS | What makes GPS data meaningful is the act -- is the use and placement of the GPS device, that was in this case, in this case, unconsented to by Antoine Jones, unknowingly. |
| 0:48:17.820 | 2897.820 | MR. LECKAR | device | What makes GPS data meaningful is the act -- is the use and placement of the GPS device, that was in this case, in this case, unconsented to by Antoine Jones, unknowingly. |
| 0:48:38.920 | 2918.920 | JUSTICE KENNEDY | police | Suppose the police suspected someone of criminal activity, and they had a computer capacity to take pictures of all the intersections that he drove through at different times of day, and they checked his movements and his routes for 5 days. |
| 0:49:35.080 | 2975.080 | MR. LECKAR | follow | The -- but we don't have any -- society does not expect -- view it as reasonable to have the equivalent of a million video cameras following you everywhere you go. |
| 0:49:45.520 | 2985.520 | MR. LECKAR | device | This is a small device that enables the government to get information of a vast amount of -- |
| 0:50:18.980 | 3018.980 | MR. LECKAR | GPS | If you want to use GPS devices, get a warrant, absent exigent circumstances or another recognized exception to the Fourth Amendment; because of their capacity for -- to collect data that you couldn't realistically get, because of the vanishingly low cost, because of their pervasive nature, that you should get a warrant any time -- you must get a warrant any time you're going to attach a GPS to a citizen's effect or to a citizen's person. |
| 0:50:19.480 | 3019.480 | MR. LECKAR | device | If you want to use GPS devices, get a warrant, absent exigent circumstances or another recognized exception to the Fourth Amendment; because of their capacity for -- to collect data that you couldn't realistically get, because of the vanishingly low cost, because of their pervasive nature, that you should get a warrant any time -- you must get a warrant any time you're going to attach a GPS to a citizen's effect or to a citizen's person. |
| 0:50:21.220 | 3021.220 | MR. LECKAR | warrant | If you want to use GPS devices, get a warrant, absent exigent circumstances or another recognized exception to the Fourth Amendment; because of their capacity for -- to collect data that you couldn't realistically get, because of the vanishingly low cost, because of their pervasive nature, that you should get a warrant any time -- you must get a warrant any time you're going to attach a GPS to a citizen's effect or to a citizen's person. |
| 0:50:52.200 | 3052.200 | CHIEF JUSTICE ROBERTS | warrant | Well, that gets back to Justice Scalia's question, which is you've got to determine that there has been a search first before you impose the warrant requirement. |
| 0:50:55.950 | 3055.950 | CHIEF JUSTICE ROBERTS | warrant | And it seems to me that your -- the warrant requirement applies only with respect to searches, right? |
| 0:51:07.940 | 3067.940 | CHIEF JUSTICE ROBERTS | device | So, while it might seem like a good idea to impose the requirement on this particular technological device, you still have to establish that it's a search. |
| 0:51:13.540 | 3073.540 | MR. LECKAR | police | But if you know, if you the police agents know -- this is the deliberative process. |
| 0:51:16.200 | 3076.200 | MR. LECKAR | device | These devices aren't used for just quick one-off surveillance. |
| 0:51:17.160 | 3077.160 | MR. LECKAR | us | These devices aren't used for just quick one-off surveillance. |
| 0:51:21.340 | 3081.340 | MR. LECKAR | us | They're used to track people over time, as witness this case, every 10 seconds of the day for 28 days. |
| 0:51:21.820 | 3081.820 | MR. LECKAR | track | They're used to track people over time, as witness this case, every 10 seconds of the day for 28 days. |
| 0:51:31.320 | 3091.320 | MR. LECKAR | device | If you know you're going to do that and you know, Justice Roberts, that this device -- this device has an amazingly invasive power and capacity. |
| 0:51:40.420 | 3100.420 | MR. LECKAR | warrant | You get a warrant. |
| 0:51:48.880 | 3108.880 | CHIEF JUSTICE ROBERTS | car | Where's the car? |
| 0:52:19.860 | 3139.860 | CHIEF JUSTICE ROBERTS | privacy | I suppose if you ask people do you think it's a violation of privacy for the police to do this for no reason for a month, maybe they'd come out one way. |
| 0:52:20.460 | 3140.460 | CHIEF JUSTICE ROBERTS | police | I suppose if you ask people do you think it's a violation of privacy for the police to do this for no reason for a month, maybe they'd come out one way. |
| 0:52:22.340 | 3142.340 | CHIEF JUSTICE ROBERTS | month | I suppose if you ask people do you think it's a violation of privacy for the police to do this for no reason for a month, maybe they'd come out one way. |
| 0:52:26.220 | 3146.220 | CHIEF JUSTICE ROBERTS | police | If you asked the people do you think the police have to have probable cause before they monitor for 5 minutes the movements of somebody they think is going to set off a huge bomb, maybe you get a different answer. |
| 0:52:54.080 | 3174.080 | JUSTICE SCALIA | privacy | Of course, a legislature can take care of this, whether or not there is an invasion of privacy. |
| 0:53:45.300 | 3225.300 | MR. LECKAR | us | They came to this Court, and they said we want a workable rule; give us a workable rule. |
| 0:53:49.520 | 3229.520 | MR. LECKAR | us | Circuit, which you should not do, or give us a workable rule. |
| 0:54:19.220 | 3259.220 | JUSTICE BREYER | warrant | I mean, can you say that a general search of this kind is not constitutional under the Fourth Amendment, but should Congress pick out a subset thereof, say, the -- terrorism or where there is reasonable cause or like the FISA court or special courts to issue special kinds of warrants, that that's a different question which we could decide at a later time? |
| 0:54:57.720 | 3297.720 | JUSTICE SCALIA | police | Congress can control police practices that don't violate the Fourth Amendment throughout the country? |
| 0:55:05.120 | 3305.120 | JUSTICE SCALIA | beeper | I mean, maybe interstate, interstate beepers and interstate tracking devices, yes, but so long as you track within -- within the State isn't that okay? |
| 0:55:06.440 | 3306.440 | JUSTICE SCALIA | track | I mean, maybe interstate, interstate beepers and interstate tracking devices, yes, but so long as you track within -- within the State isn't that okay? |
| 0:55:06.440 | 3306.440 | JUSTICE SCALIA | tracking | I mean, maybe interstate, interstate beepers and interstate tracking devices, yes, but so long as you track within -- within the State isn't that okay? |
| 0:55:07.100 | 3307.100 | JUSTICE SCALIA | device | I mean, maybe interstate, interstate beepers and interstate tracking devices, yes, but so long as you track within -- within the State isn't that okay? |
| 0:55:26.960 | 3326.960 | MR. LECKAR | follow | But other legislatures would follow Congress. |
| 0:55:34.240 | 3334.240 | MR. LECKAR | vehicle | But what we have here -- what we have here is a live case of controversy in which Antoine Jones' control of his vehicle was usurped and his car was converted into an electronic GPS transceiver serving the government. |
| 0:55:35.600 | 3335.600 | MR. LECKAR | car | But what we have here -- what we have here is a live case of controversy in which Antoine Jones' control of his vehicle was usurped and his car was converted into an electronic GPS transceiver serving the government. |
| 0:55:37.740 | 3337.740 | MR. LECKAR | GPS | But what we have here -- what we have here is a live case of controversy in which Antoine Jones' control of his vehicle was usurped and his car was converted into an electronic GPS transceiver serving the government. |
| 0:55:57.080 | 3357.080 | JUSTICE ALITO | warrant | There was a warrant -- there was a warrant in this case. |
| 0:56:04.620 | 3364.620 | JUSTICE ALITO | warrant | There was a warrant, and the two violations are violations of a statute and a rule, neither of which may carry an exclusionary rule sanction with them or an exclusionary rule penalty with them. |
| 0:56:27.740 | 3387.740 | JUSTICE ALITO | warrant | So, it's a little strange that we're deciding whether a warrantless search here would have been unconstitutional, when there was a warrant. |
| 0:56:57.560 | 3417.560 | MR. LECKAR | warrant | When -- when the warrant -- |
| 0:56:59.920 | 3419.920 | JUSTICE ALITO | warrant | It is not a warrantless intrusion; there was a warrant. |
| 0:57:01.320 | 3421.320 | MR. LECKAR | warrant | But the warrant was not in effect. |
| 0:57:04.340 | 3424.340 | MR. LECKAR | GPS | At the -- at the time the -- the GPS was placed, Justice Alito, there was no warrant. |
| 0:57:06.860 | 3426.860 | MR. LECKAR | warrant | At the -- at the time the -- the GPS was placed, Justice Alito, there was no warrant. |
| 0:57:13.580 | 3433.580 | JUSTICE GINSBURG | warrant | The warrant expired. |
| 0:57:14.980 | 3434.980 | JUSTICE GINSBURG | warrant | There was no warrant. |
| 0:57:22.320 | 3442.320 | JUSTICE GINSBURG | us | The government certainly could have gone back and said, judge, we didn't make it; we need a little more time; give us 10 more days. |
| 0:57:39.460 | 3459.460 | JUSTICE ALITO | warrant | -- it doesn't vitiate the warrant. |
| 0:57:39.880 | 3459.880 | JUSTICE ALITO | warrant | The warrant doesn't necessarily dissolve or evaporate when the 10 days expire. |
| 0:57:54.640 | 3474.640 | MR. LECKAR | warrant | There's a 1920 Supreme Court decision decided during the Prohibition era that specifically said that when a warrant expires, there is no warrant. |
| 0:57:59.780 | 3479.780 | MR. LECKAR | warrant | When the 10-day rule in that case had expired, there's no warrant. |
| 0:58:15.440 | 3495.440 | MR. DREEBEN | police | Technological advances can make the police more efficient at what they do through some of the examples that were discussed today: Cameras, airplanes, beepers, GPS. |
| 0:58:23.260 | 3503.260 | MR. DREEBEN | beeper | Technological advances can make the police more efficient at what they do through some of the examples that were discussed today: Cameras, airplanes, beepers, GPS. |
| 0:58:24.080 | 3504.080 | MR. DREEBEN | GPS | Technological advances can make the police more efficient at what they do through some of the examples that were discussed today: Cameras, airplanes, beepers, GPS. |
| 0:58:28.280 | 3508.280 | MR. DREEBEN | us | At the same time, technology and how it's used can change our expectations of privacy in the ways that Justice Alito was alluding to. |
| 0:58:29.280 | 3509.280 | MR. DREEBEN | our | At the same time, technology and how it's used can change our expectations of privacy in the ways that Justice Alito was alluding to. |
| 0:58:30.720 | 3510.720 | MR. DREEBEN | privacy | At the same time, technology and how it's used can change our expectations of privacy in the ways that Justice Alito was alluding to. |
| 0:58:36.460 | 3516.460 | MR. DREEBEN | GPS | Today perhaps GPS can be portrayed as a 1984-type invasion, but as people use GPS in their lives and for other purposes, our expectations of privacy surrounding our location may also change. |
| 0:58:39.400 | 3519.400 | MR. DREEBEN | 1984 | Today perhaps GPS can be portrayed as a 1984-type invasion, but as people use GPS in their lives and for other purposes, our expectations of privacy surrounding our location may also change. |
| 0:58:46.140 | 3526.140 | MR. DREEBEN | our | Today perhaps GPS can be portrayed as a 1984-type invasion, but as people use GPS in their lives and for other purposes, our expectations of privacy surrounding our location may also change. |
| 0:58:47.360 | 3527.360 | MR. DREEBEN | privacy | Today perhaps GPS can be portrayed as a 1984-type invasion, but as people use GPS in their lives and for other purposes, our expectations of privacy surrounding our location may also change. |
| 0:58:57.080 | 3537.080 | JUSTICE KAGAN | device | I mean, if you think about this, and you think about a little robotic device following you around 24 hours a day anyplace you go that's not your home, reporting in all your movements to the police, to investigative authorities, the notion that we don't have an expectation of privacy in that, the notion that we don't think that our privacy interests would be violated by this robotic device, I'm -- I'm not sure how one can say that. |
| 0:58:57.680 | 3537.680 | JUSTICE KAGAN | follow | I mean, if you think about this, and you think about a little robotic device following you around 24 hours a day anyplace you go that's not your home, reporting in all your movements to the police, to investigative authorities, the notion that we don't have an expectation of privacy in that, the notion that we don't think that our privacy interests would be violated by this robotic device, I'm -- I'm not sure how one can say that. |
| 0:59:09.440 | 3549.440 | JUSTICE KAGAN | police | I mean, if you think about this, and you think about a little robotic device following you around 24 hours a day anyplace you go that's not your home, reporting in all your movements to the police, to investigative authorities, the notion that we don't have an expectation of privacy in that, the notion that we don't think that our privacy interests would be violated by this robotic device, I'm -- I'm not sure how one can say that. |
| 0:59:15.160 | 3555.160 | JUSTICE KAGAN | privacy | I mean, if you think about this, and you think about a little robotic device following you around 24 hours a day anyplace you go that's not your home, reporting in all your movements to the police, to investigative authorities, the notion that we don't have an expectation of privacy in that, the notion that we don't think that our privacy interests would be violated by this robotic device, I'm -- I'm not sure how one can say that. |
| 0:59:17.800 | 3557.800 | JUSTICE KAGAN | our | I mean, if you think about this, and you think about a little robotic device following you around 24 hours a day anyplace you go that's not your home, reporting in all your movements to the police, to investigative authorities, the notion that we don't have an expectation of privacy in that, the notion that we don't think that our privacy interests would be violated by this robotic device, I'm -- I'm not sure how one can say that. |
| 0:59:50.720 | 3590.720 | JUSTICE KENNEDY | police | Suppose exactly these facts, only the police aren't involved. |
| 1:00:03.740 | 3603.740 | JUSTICE KENNEDY | privacy | Do you think that in most States, that would be an invasion of privacy? |
| 1:00:13.160 | 3613.160 | MR. DREEBEN | privacy | I'm willing to assume that it might be, Justice Kennedy, but I don't think that this Court measures the metes and bounds of the Fourth Amendment by State law invasions of privacy. |
| 1:00:15.740 | 3615.740 | JUSTICE KENNEDY | privacy | We measure it by expectations of privacy under the Katz test if -- that may or may not be controlling. |
| 1:00:30.760 | 3630.760 | MR. DREEBEN | privacy | Yes, but in Greenwood, the Court dealt with a case where California had outlawed taking somebody's garbage, and this Court said that did not define an expectation of privacy for purposes of the Fourth Amendment -- |
| 1:00:34.460 | 3634.460 | JUSTICE KENNEDY | privacy | It found that there was no expectation of privacy. |
| 1:00:38.780 | 3638.780 | JUSTICE KENNEDY | privacy | I am asking you about this case, whether there would be an expectation of privacy -- |
| 1:00:47.560 | 3647.560 | MR. DREEBEN | police | And -- and the fact that something may be a tort for a private person doesn't mean that it's a problem for the police to do it. |
| 1:00:51.020 | 3651.020 | MR. DREEBEN | police | For example, in the Dow Chemical case, where the police used -- EPA in that case actually used cameras to surveil an industrial plant. |
| 1:00:51.400 | 3651.400 | MR. DREEBEN | us | For example, in the Dow Chemical case, where the police used -- EPA in that case actually used cameras to surveil an industrial plant. |
| 1:01:26.300 | 3686.300 | MR. DREEBEN | our | If that kind of abuse comes up, the legislature is the best-equipped to deal with it, if in fact our society regards that as an unreasonable restriction on -- |
| 1:01:31.140 | 3691.140 | JUSTICE SOTOMAYOR | GPS | Do you have any idea of how many GPS devices are being used by Federal Government agencies and State law enforcement officials? |
| 1:01:31.620 | 3691.620 | JUSTICE SOTOMAYOR | device | Do you have any idea of how many GPS devices are being used by Federal Government agencies and State law enforcement officials? |
| 1:01:32.660 | 3692.660 | JUSTICE SOTOMAYOR | us | Do you have any idea of how many GPS devices are being used by Federal Government agencies and State law enforcement officials? |
| 1:01:50.120 | 3710.120 | MR. DREEBEN | us | The FBI requires that there be some reasonable basis for using GPS before it installs it. |
| 1:01:50.560 | 3710.560 | MR. DREEBEN | GPS | The FBI requires that there be some reasonable basis for using GPS before it installs it. |
| 1:02:05.160 | 3725.160 | MR. DREEBEN | GPS | The GPS allowed it to be more effective. |
| 1:02:20.900 | 3740.900 | MR. DREEBEN | privacy | As Justice Kennedy and, I think, Justice Scalia's hypotheticals illustrated, Respondent is essentially conceding that around-the-clock visual surveillance through teams of agents would not have invaded any expectation of privacy. |
| 1:02:23.700 | 3743.700 | MR. DREEBEN | police | This Court said in Knotts that police efficiency has never been equated with police unconstitutionality. |
| 1:02:29.980 | 3749.980 | MR. DREEBEN | GPS | The fact that GPS makes it more efficient for the police to put a tail on somebody invades no additional expectation of privacy that they otherwise would have had. |
| 1:02:31.960 | 3751.960 | MR. DREEBEN | police | The fact that GPS makes it more efficient for the police to put a tail on somebody invades no additional expectation of privacy that they otherwise would have had. |
| 1:02:36.900 | 3756.900 | MR. DREEBEN | privacy | The fact that GPS makes it more efficient for the police to put a tail on somebody invades no additional expectation of privacy that they otherwise would have had. |
| 1:02:44.460 | 3764.460 | MR. DREEBEN | our | When we go out in our cars, our cars have driver's licenses that we carry. |
| 1:02:44.660 | 3764.660 | MR. DREEBEN | car | When we go out in our cars, our cars have driver's licenses that we carry. |
| 1:02:44.660 | 3764.660 | MR. DREEBEN | cars | When we go out in our cars, our cars have driver's licenses that we carry. |
| 1:02:50.080 | 3770.080 | MR. DREEBEN | car | We have license plates on the car. |
| 1:03:01.180 | 3781.180 | JUSTICE SOTOMAYOR | car | You don't seriously argue that there isn't a possessory interest in who puts something on your car and who -- like a -- a sign of some sort. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:08.900 to 0:03:08.900, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:08.900] MR. DREEBEN: Mr. Chief Justice, and may it please the Court: Since this Court's decision in Katz v. United States, the Court has recognized a basic dichotomy under the Fourth Amendment. What a person seeks to preserve as private in the enclave of his own home or in a private letter or inside of his vehicle when he is traveling is a subject of Fourth Amendment protection. But what he reveals to the world, such as his movements in a car on a public roadway, is not. In Knotts v. United States, this Court applied that principle to hold that visual and beeper surveillance of a vehicle traveling on the public roadways infringed no Fourth Amendment expectation of privacy.

[0:00:54.920] CHIEF JUSTICE ROBERTS: Knotts, though, seems to me much more like traditional surveillance. You're following the car, and the beeper just helps you follow it from a -- from a slightly greater distance. That was 30 years ago. The technology is very different, and you get a lot more information from the GPS surveillance than you do from following a beeper.

[0:01:14.860] MR. DREEBEN: The technology is different, Mr. Chief Justice, but a crucial fact in Knotts that shows that this was not simply amplified visual surveillance is that the officers actually feared detection in Knotts as the car crossed from Minnesota to Wisconsin. The driver began to do certain U-turns and, the police broke off visual surveillance. They lost track of the car for a full hour. They only were able to discover it by having a beeper receiver in a helicopter that detected the beeps from the radio transmitter in the can of chloroform.

[0:01:49.060] CHIEF JUSTICE ROBERTS: But that's a good example of the change in technology. That's a lot of work to follow the car. They've got to listen to the beeper; when they lose it, they've got to call in the helicopter. Here they just sit back in the station, and they -- they push a button whenever they want to find out where the car is. They look at data from a month and find out everywhere it's been in the past month. That -- that seems to me dramatically different.

[0:02:09.860] MR. DREEBEN: But it doesn't expose anything, Mr. Chief Justice, that isn't already exposed to public view for anyone who wanted to watch, and that was the crucial principle that the Court applied --

[0:02:20.060] JUSTICE KENNEDY: Well, under that rationale, could you put a beeper surreptitiously on the man's overcoat or sport coat?

[0:02:26.320] MR. DREEBEN: Probably not, Justice Kennedy; and the reason is that this Court in Karo v. United States -- United States v. Karo -- specifically distinguished the possibility of following a car on a public roadways from determining the location of an object in a place where a person has a reasonable expectation of privacy.

[0:02:43.460] JUSTICE KENNEDY: Oh, no. This is a special device. It measures only streets and public elevators and public buildings.

[0:02:49.340] MR. DREEBEN: In that event, Justice Kennedy, there is a serious question about whether the installation of such a device would implicate either a search or a seizure. But if it did not, the public movements of somebody do not implicate a seizure.

[0:03:02.140] JUSTICE KENNEDY: Well -- and on that latter point, you might just be aware that I have serious reservations that there wasn't -- that there --

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - January 23, 2012.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2011/10-1259
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2011/10-1259/20120123o_10-1259.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.7 MB)
- Length: 0:06:50.123 (410.123 s)
- Words: 940, transcribed by faster-whisper `medium.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (2
  trimmed, 0 re-transcribed).
- Skipped speech: Whisper skipped a stretch of speech: 0:00:06.500 to 0:00:40.000 (73 words recovered). Each was re-transcribed on its own and the words put in.
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 913 of Whisper's 940 words (97.1%; Oyez has 943).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.500 | 15 |
| JUSTICE SCALIA | 0:00:07.360 | 0:06:48.880 | 922 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: And Justice Scalia has our opinion this morning in Case 10-1259, United States v. Jones.

[0:00:07.360] JUSTICE SCALIA: This case is here on writ of certiorari to the United States Court of Appeals for the District of Columbia Circuit. In 2004, the Respondent Antoine Jones came under suspicion of trafficking in narcotics. The government obtained from the United States District Court here a warrant authorizing the installation of an electronic tracking device on the Jeep registered to Jones's wife to be installed in the District of Columbia and within 10 days. On the 11th day, and not in the District of Columbia, but in Maryland, agents installed a GPS tracking device on the undercarriage of the Jeep while it was parked in a public parking lot. Over the next 28 days, the government used the device to track the vehicle's movements. In the later trial of Jones and others on drug trafficking charges, the district court suppressed the GPS data obtained while the vehicle was parked at Jones' residence, but admitted the remaining data, which connected Jones to the alleged conspirator's stash house that contained significant amounts of cash and narcotics. The jury returned a guilty verdict, and the district court sentenced Jones to life imprisonment. The D .C. Circuit set the conviction aside, concluding that admission of the evidence obtained by the warrantless use of the GPS tracking device violated the Fourth Amendment. We granted certiorari, and we now affirm. The Fourth Amendment protects, quote, the right of the people to be secure in their persons, houses, papers, and effects against unreasonable searches and seizures. The Jeep is certainly an effect, as that term is used in the amendment. We hold that the government's physical intrusion on the Jeep for the purpose of obtaining information constitutes a search. This type of encroachment on an area enumerated in the amendment would have been considered a search within the meaning of the amendment at the time it was adopted. The text of the amendment reflects its close connection to property, since otherwise it would have referred simply to the right of the people to be secure against unreasonable searches and seizures. That's not what it says. It says to be secure in their persons, houses, papers, and effects against unreasonable searches and seizures. That last phrase would have been superfluous. Consistent with this understanding, our Fourth Amendment jurisprudence was tied to common law trespass, at least until the latter half of the 20th century.

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:00.000 | And | (nothing) |
| 0:00:33.980 | Jones's | Jones' |
| 0:00:47.220 | (nothing) | tracking -- |
| 0:02:47.020 | (nothing) | The -- |
| 0:03:38.720 | (nothing) | -- the |
| 0:03:48.820 | Jones's | Jones' |
| 0:03:56.680 | Kylo v. | Kyllo versus |
| 0:04:06.400 | adopted, close quote. | adapted”. |
| 0:04:27.500 | trespassary | trespassory |
| 0:04:54.720 | Katz | Katz's |
| 0:05:09.680 | (nothing) | had -- had been -- |
| 0:05:17.940 | trespassary | trespassory |
| 0:05:23.920 | v. Cairo, | versus Karo, |
| 0:05:40.520 | Cairo, | Karo, |
| 0:05:47.700 | Cairo | Karo |
| 0:06:08.160 | trespassarily | trespassorily |
