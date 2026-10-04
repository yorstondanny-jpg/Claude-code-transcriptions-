# horne-raisins-2013: Supreme Court No. 12-123

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2012/12-123
- Audio: https://www.supremecourt.gov/media/audio/mp3files/12-123.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2012/12-123_l537.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 56 min on 4 CPU cores
- Audio length: 0:59:24.957 (3564.957 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.5 MB
- Official words: 10142 (plus 6 `(Laughter.)` markers), in 244 speaker turns
- ASR words: 9941
- Official words matched to an ASR word: 9548 of 10142 (**94.14%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.14% (threshold 85%).

373 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 3 times. ASR words with no official counterpart
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

    python3 transcribe.py 12-123 2012 horne-raisins-2013 --model medium.en --opinion --mentions "raisins,reserve,percent,ton(s),fine,penalty,farmers,handler,Horne,wild animals,dancing,California" --long-questions 10 --opinion-full-text

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE BREYER, 0:19:08.200 to 0:20:07.600 (59.4 s, 220 words)

> I'm just trying to get to what you're arguing about. And I might be off base by now. I feel like handlers, purchasers, raisins, like an old Abbott and Costello movie. I just want to see if I'm right. Tell me. Just say you're wrong and I don't go into it further. There -- there are some people, they've been -- they are either -- they have some raisins, all right. And these particular people, whom the Department has said have acquired the raisins, it said they acquired the raisins. And so they're there with some raisins, and then the government says, do this thing with your raisins. And they don't want to do it, so they don't. They don't do it even though the law says do it. And then they say the law is unconstitutional and, moreover, you fined us a huge amount of money and we don't want to pay it because the law is unconstitutional, and we consider that money that we paid. Call it a fine, call it what you want. We consider we shouldn't have paid it and now we want it back and we want compensation and we think it's a taking and where do we go. Can't we make that argument in the Ninth Circuit? It's something like that; isn't that what we're arguing about?

### 2. JUSTICE GINSBURG, 0:12:44.020 to 0:13:38.140 (54.1 s, 122 words)

> Mr. McConnell, would you explain the -- if they were just handlers and weren't producing any raisins, if they were just handlers, do they have a claim and where? And if they were just producers -- I take it from the question I asked and the question Justice Kagan asked that if they were just producers, the raisins got set aside, they were paid for only the ones that went to market, they could go to the Court of Claims. But now they're just handlers, as this entity is for most of the raisins that are involved, some 80 percent, right? It's only about 20 percent is their own. So could this work for someone who was just a handler, doesn't produce any raisins?

### 3. JUSTICE SOTOMAYOR, 0:15:47.100 to 0:16:40.420 (53.3 s, 98 words)

> What is -- what is the value in permitting a party who doesn't own property to raise a taking claim on behalf of other people? Meaning, doesn't the system have an interest in ensuring that people comply with their legal obligations, and to the extent that you choose to violate the law the way they have here, that the fine is punitive and not compensatory. Meaning, you don't own the raisins, but you were obligated to put raisins aside for someone else. You were their agent and you failed to meet a government obligation that was independently on you.

### 4. JUSTICE SOTOMAYOR, 0:00:25.760 to 0:01:15.620 (49.9 s, 87 words)

> -- because it has confused me. As I look at the captions of the cases, there appear to be two different partnerships: One partnership, known as Raisin -- doing business as Raisin Valley Farms, has Mr. Horne and his wife as the partners. Larsen Valley, the producer -- not the producer, the handler -- has four other, the Hornes, plus two other people. So who owns the raisins? Isn't that the first partnership of the husband and wife? And isn't the handler a second partnership that does the business of handling?

### 5. JUSTICE SOTOMAYOR, 0:46:01.810 to 0:46:44.870 (43.1 s, 97 words)

> All right. It almost seems to me, and I'll ask Mr. McConnell when he gets up at rebuttal, that there is some sort of due process challenge going on here that's been created by the labels they did in this new situation -- in this new business venture. In the normal situation, the handler, I'm being told, would actually have title to the raisins, and they would pay the producers for the raisins. So there would be property taking. In that situation, where the handlers actually own the property, would they be able to raise a taking defense?

### 6. JUSTICE BREYER, 0:44:50.250 to 0:45:33.010 (42.8 s, 143 words)

> No, no. No, it doesn't go to the merits. It goes to whether or not it makes sense to think that the Court of Claims has something to say about this. And suppose we did this. Suppose we said, given the fact that you filed your thing, whatever it was -- you know, late, and the -- and the light of this very enlightening discussion which has been helpful, we think this is the kind of program and challenge to the program where there isn't going to be a remedy really in the Court of Claims and they ought to go ahead in the Ninth Circuit, and in light of all these enlightening things that we'll write, you just decide the merits of -- is that -- now, I'm sure you're going to say that's absolutely terrible, it won't work at all. So tell me why not.

### 7. JUSTICE GINSBURG, 0:41:27.990 to 0:42:10.610 (42.6 s, 78 words)

> Mr. Palmore, am I incorrect in thinking that the government is saying, handlers cannot raise the constitutionality of the Raisin Marketing Order? You've told us that the producers can go to the Court of Claims. What about the handlers? They're at least being fined for violating the Act, and it's their position that the whole thing is unconstitutional. Can they raise the constitutionality of the whole arrangement defensively, or they simply can't raise the constitutionality of the Act?

### 8. JUSTICE BREYER, 0:37:08.910 to 0:37:48.990 (40.1 s, 123 words)

> Fine. So they're making that kind of constitutional claim. Now, I would think if all you told me was that and I knew nothing about all these statutes, I would say that's the kind of claim that should be made in a Federal district court, period, not the Court of Claims. Because their government isn't going to compensate them for anything. That's against the whole point of the program. Either this program is valid or it isn't. And if it isn't, some authoritative set of courts should tell us that. So I have a feeling this is somehow not a right fit with the Court of Claims. Now, you explain to me why that purely instinctive feeling at this point is completely wrong.

### 9. JUSTICE KAGAN, 0:50:23.790 to 0:51:03.230 (39.4 s, 124 words)

> Mr. Palmore, what would be wrong -- would anything be wrong -- with a -- with a disposition of this Court that went something like this: Everybody agrees that this is not a jurisdictional issue, including the government, so they got that wrong. Now, as to this whole business about the Tucker Act and whether the Tucker Act provides a remedy, the government only started talking about that in a petition for rehearing en banc, and the government can't do that. You know, it can't introduce an argument like this in a petition for rehearing en banc. So that's waived. And now, the Ninth Circuit can go and try to figure out whether this marketing order is a taking or it's just the world's most outdated law. (Laughter.)

### 10. JUSTICE KAGAN, 0:21:13.520 to 0:21:51.860 (38.3 s, 119 words)

> I think that's true, Mr. McConnell, as to part of the fine, that part of the fine falls under Apfel, but not the other part. As to the compensation part, it seems to me you have a pretty decent Apfel argument. But as to the penalty part, I don't really understand how the Apfel argument would go. It seems to me that as to the penalty part, the key thing is that if they had handed over the raisins, they could have gone to the Court of Federal Claims and had the compensation done there. And the fact that the government is penalizing them for not complying with the marketing order does not fall within the rationale of Apfel.

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-48.4 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:20:09.940 | 1209.940 | big | 2.28 | 2.05 | 28.2 | 36.1 | where do we go. Can't we make that argument in the Ninth Circuit? It's something like that; isn't that what we're arguing about? That's almost exactly right. But not quite. |
| 2 | 0:26:47.370 | 1607.370 | medium | 1.58 | 1.15 | 17.0 | 22.1 | Ninth Circuit panel accepted their view, issued a new opinion, stripping out the entire merits, and substituting this jurisdictional holding that is producing so much enjoyment for us this morning. |
| 3 | 0:31:30.310 | 1890.310 | small | 0.80 | 0.05 | 10.4 | 15.5 | that provides a judicial review mechanism only for handlers. Yes, but part of -- part of that penalty was -- you know, your raisins or your life, right? I mean, it was -- |
| 4 | 0:51:03.230 | 3063.230 | big | 3.74 | 1.20 | 24.9 | 37.5 | So that's waived. And now, the Ninth Circuit can go and try to figure out whether this marketing order is a taking or it's just the world's most outdated law. |
| 5 | 0:52:49.420 | 3169.420 | under speech | 0.00 | 0.00 | - | - | through 11 of our brief, we cite communication after communication where USDA told them -- Now, can an acquirer of my car, for example -- I don't know. Forget that. A bailee? |
| 6 | 0:56:46.230 | 3406.230 | big | 2.64 | 2.50 | 25.3 | 35.8 | you should affirm. However, I do recognize -- Do you think we should reach the merits, which is a very different question? Well, it depends on what you mean by "merits." |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| raisins | 88 | 114 |
| reserve | 14 | 15 |
| percent | 2 | 2 |
| ton(s) | 1 | 1 |
| fine | 17 | 19 |
| penalty | 11 | 12 |
| farmers | 0 | 0 |
| handler | 70 | 81 |
| Horne | 16 | 17 |
| wild animals | 0 | 0 |
| dancing | 0 | 0 |
| California | 2 | 2 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:00:05.620 | 5.620 | CHIEF JUSTICE ROBERTS | Horne | We'll hear argument first this morning in Case 12-123, Horne v. Department of Agriculture. |
| 0:00:42.940 | 42.940 | JUSTICE SOTOMAYOR | Horne | As I look at the captions of the cases, there appear to be two different partnerships: One partnership, known as Raisin -- doing business as Raisin Valley Farms, has Mr. Horne and his wife as the partners. |
| 0:00:51.260 | 51.260 | JUSTICE SOTOMAYOR | handler | Larsen Valley, the producer -- not the producer, the handler -- has four other, the Hornes, plus two other people. |
| 0:00:54.340 | 54.340 | JUSTICE SOTOMAYOR | Horne | Larsen Valley, the producer -- not the producer, the handler -- has four other, the Hornes, plus two other people. |
| 0:00:59.560 | 59.560 | JUSTICE SOTOMAYOR | raisins | So who owns the raisins? |
| 0:01:07.840 | 67.840 | JUSTICE SOTOMAYOR | handler | And isn't the handler a second partnership that does the business of handling? |
| 0:01:20.320 | 80.320 | MR. MCCONNELL | Horne | The other two partners in Lassen were Laura Horne's parents, now deceased. |
| 0:02:36.020 | 156.020 | JUSTICE SOTOMAYOR | raisins | Well, it does to my mind because what is the claim, assuming that the producer owns -- the producer entity owns the raisins. |
| 0:02:39.860 | 159.860 | JUSTICE SOTOMAYOR | handler | What exactly is being taken from the handlers? |
| 0:02:43.660 | 163.660 | JUSTICE SOTOMAYOR | raisins | Is it the percentage -- it can't be the raisins because they don't own them. |
| 0:02:54.900 | 174.900 | JUSTICE SOTOMAYOR | handler | What is it that's being taken from the handler entity? |
| 0:03:00.730 | 180.730 | MR. MCCONNELL | Horne | The order in this case was issued against the -- the Hornes in their capacity as a handler only, so the entire fine was paid by them. |
| 0:03:02.180 | 182.180 | MR. MCCONNELL | handler | The order in this case was issued against the -- the Hornes in their capacity as a handler only, so the entire fine was paid by them. |
| 0:03:04.240 | 184.240 | MR. MCCONNELL | fine | The order in this case was issued against the -- the Hornes in their capacity as a handler only, so the entire fine was paid by them. |
| 0:03:07.540 | 187.540 | MR. MCCONNELL | fine | None of the fine is attributable to anyone in their capacity as a producer. |
| 0:03:21.840 | 201.840 | JUSTICE SOTOMAYOR | fine | What is the -- what was taken from them -- you're saying it's just the fine, that the fine is a taking or -- what was the interest that they're claiming was taken by the government? |
| 0:03:30.440 | 210.440 | JUSTICE SOTOMAYOR | raisins | They didn't own the raisins, so they get paid a fee for handling. |
| 0:03:47.360 | 227.360 | MR. MCCONNELL | Horne | So, in the demand letter from the Department of Agriculture addressed to the Hornes, they -- they asked the Hornes to deliver California raisins, or the dollar equivalent. |
| 0:03:50.680 | 230.680 | MR. MCCONNELL | California | So, in the demand letter from the Department of Agriculture addressed to the Hornes, they -- they asked the Hornes to deliver California raisins, or the dollar equivalent. |
| 0:03:51.720 | 231.720 | MR. MCCONNELL | raisins | So, in the demand letter from the Department of Agriculture addressed to the Hornes, they -- they asked the Hornes to deliver California raisins, or the dollar equivalent. |
| 0:04:02.000 | 242.000 | MR. MCCONNELL | California | Now, what is the legal significance of that, California raisins or the dollar equivalent? |
| 0:04:02.640 | 242.640 | MR. MCCONNELL | raisins | Now, what is the legal significance of that, California raisins or the dollar equivalent? |
| 0:05:51.440 | 351.440 | JUSTICE GINSBURG | Horne | Am I right in thinking that there is no dispute on that point, that the -- the takings claim could have been asserted by the Hornes, as producers, in the Court of Federal Claims? |
| 0:06:23.820 | 383.820 | JUSTICE GINSBURG | fine | -- jurisdictional or not, as a practical matter, producers who are not subject to fine as handlers, but the producers of the raisins whose raisins are being segregated, could they go to the Court of Federal Claims and say my raisins have been taken? |
| 0:06:24.720 | 384.720 | JUSTICE GINSBURG | handler | -- jurisdictional or not, as a practical matter, producers who are not subject to fine as handlers, but the producers of the raisins whose raisins are being segregated, could they go to the Court of Federal Claims and say my raisins have been taken? |
| 0:06:26.720 | 386.720 | JUSTICE GINSBURG | raisins | -- jurisdictional or not, as a practical matter, producers who are not subject to fine as handlers, but the producers of the raisins whose raisins are being segregated, could they go to the Court of Federal Claims and say my raisins have been taken? |
| 0:06:43.380 | 403.380 | MR. MCCONNELL | handler | The -- whether the claim is being brought in the capacity of producer or handler I think is not relevant to one of our arguments, and it is relevant to the other argument. |
| 0:06:59.780 | 419.780 | MR. MCCONNELL | handler | No, no. No, we're representing people who are both producers and handlers. |
| 0:07:14.980 | 434.980 | MR. MCCONNELL | handler | In the ordinary case, the ordinary relationship between a producer and a handler, the producer is not paid for the reserve raisins and therefore any payment that would come, any lawsuit on behalf of those raisins would go to the producer, and that would go I think to the Court of Claims. |
| 0:07:17.740 | 437.740 | MR. MCCONNELL | reserve | In the ordinary case, the ordinary relationship between a producer and a handler, the producer is not paid for the reserve raisins and therefore any payment that would come, any lawsuit on behalf of those raisins would go to the producer, and that would go I think to the Court of Claims. |
| 0:07:18.120 | 438.120 | MR. MCCONNELL | raisins | In the ordinary case, the ordinary relationship between a producer and a handler, the producer is not paid for the reserve raisins and therefore any payment that would come, any lawsuit on behalf of those raisins would go to the producer, and that would go I think to the Court of Claims. |
| 0:07:40.740 | 460.740 | MR. MCCONNELL | raisins | They received full value -- market value for their raisins. |
| 0:07:44.840 | 464.840 | MR. MCCONNELL | Horne | The only people who are out any money in this case are the Hornes in their capacity as handler. |
| 0:07:46.380 | 466.380 | MR. MCCONNELL | handler | The only people who are out any money in this case are the Hornes in their capacity as handler. |
| 0:08:04.880 | 484.880 | JUSTICE SOTOMAYOR | raisins | It belonged to the producers who supplied them with the raisins and expected payment for them -- |
| 0:08:18.360 | 498.360 | MR. MCCONNELL | handler | It is the handlers who have been held responsible. |
| 0:08:46.560 | 526.560 | MR. MCCONNELL | raisins | They were held responsible because in their -- in their processing capacity, when they were doing the stemming, the seeding, the fumigating, the packing, that this was regarded by the Department of Agriculture as possession -- physical possession of the raisins and acquisition of the raisins, even though they never had title to the raisins. |
| 0:08:58.500 | 538.500 | MR. MCCONNELL | raisins | It's the Department of Agriculture that has attached to them a possessory interest in the raisins and then assessed them the full monetary equivalent of those raisins, full market value, $484,000 for the market value because it's -- because under this very unusual regulatory scheme the government regards them as having possessed the raisins even though that -- that is not -- |
| 0:09:28.360 | 568.360 | JUSTICE KAGAN | Horne | Could I -- along the lines of what Justice Ginsburg was saying, suppose that the Hornes had given over all the raisins, right, but that they thought that this was improper, that this marketing order was -- it was a violation of the takings clause. |
| 0:09:30.580 | 570.580 | JUSTICE KAGAN | raisins | Could I -- along the lines of what Justice Ginsburg was saying, suppose that the Hornes had given over all the raisins, right, but that they thought that this was improper, that this marketing order was -- it was a violation of the takings clause. |
| 0:09:49.940 | 589.940 | JUSTICE KAGAN | raisins | They gave -- they gave over the raisins, they say we're entitled to compensation. |
| 0:09:59.920 | 599.920 | MR. MCCONNELL | raisins | If they had -- if they had not been paid for the raisins, they had taken raisins to a handler, received no money for them, I think that they could go to the Court of Claims. |
| 0:10:02.020 | 602.020 | MR. MCCONNELL | handler | If they had -- if they had not been paid for the raisins, they had taken raisins to a handler, received no money for them, I think that they could go to the Court of Claims. |
| 0:10:06.620 | 606.620 | JUSTICE KAGAN | Horne | In other words, the Hornes did what the marketing order suggested they should do. |
| 0:10:10.400 | 610.400 | JUSTICE KAGAN | raisins | They gave over the raisins. |
| 0:10:40.640 | 640.640 | MR. MCCONNELL | raisins | -- because what they -- what they knew was that they were not going to be compensated for the raisins, and therefore they came up with a -- with a plan, a business plan that they believed made -- eliminated any handler and made it unnecessary for any of the independent producers, on whose behalf they're operating, to turn over raisins to the government. |
| 0:10:50.100 | 650.100 | MR. MCCONNELL | handler | -- because what they -- what they knew was that they were not going to be compensated for the raisins, and therefore they came up with a -- with a plan, a business plan that they believed made -- eliminated any handler and made it unnecessary for any of the independent producers, on whose behalf they're operating, to turn over raisins to the government. |
| 0:11:13.420 | 673.420 | MR. MCCONNELL | handler | The plan was ultimately rejected and we haven't brought a -- a cert petition on it, but the plan actually complies with the -- with the language of the -- of the regulation because they believe that in their capacity as handler, as processor, that they never acquired the raisins. |
| 0:11:16.860 | 676.860 | MR. MCCONNELL | raisins | The plan was ultimately rejected and we haven't brought a -- a cert petition on it, but the plan actually complies with the -- with the language of the -- of the regulation because they believe that in their capacity as handler, as processor, that they never acquired the raisins. |
| 0:11:20.240 | 680.240 | MR. MCCONNELL | handler | "Acquisition" is the key term for becoming a handler under the rule. |
| 0:11:28.440 | 688.440 | MR. MCCONNELL | ton(s) | And they believe that since they were simply providing a service for -- for $12 a ton to their neighbors, that they never acquired the raisins, they never possessed the raisins, and therefore no one had to comply the regulation. |
| 0:11:31.800 | 691.800 | MR. MCCONNELL | raisins | And they believe that since they were simply providing a service for -- for $12 a ton to their neighbors, that they never acquired the raisins, they never possessed the raisins, and therefore no one had to comply the regulation. |
| 0:11:36.980 | 696.980 | JUSTICE SCALIA | raisins | Well, some of the raisins were their own. |
| 0:11:37.400 | 697.400 | JUSTICE SCALIA | raisins | Some of the raisins were their own. |
| 0:11:56.860 | 716.860 | JUSTICE KENNEDY | penalty | Well, to get you back to the -- the jurisdiction point, let's -- let's just assume a hypothetical case where a regulated entity has to pay an exaction which it deems to be a penalty. |
| 0:12:02.140 | 722.140 | JUSTICE KENNEDY | penalty | It waits until the penalty's assessed and then when the penalty's assessed it says, this is a taking. |
| 0:12:50.220 | 770.220 | JUSTICE GINSBURG | handler | Mr. McConnell, would you explain the -- if they were just handlers and weren't producing any raisins, if they were just handlers, do they have a claim and where? |
| 0:12:53.020 | 773.020 | JUSTICE GINSBURG | raisins | Mr. McConnell, would you explain the -- if they were just handlers and weren't producing any raisins, if they were just handlers, do they have a claim and where? |
| 0:13:08.380 | 788.380 | JUSTICE GINSBURG | raisins | And if they were just producers -- I take it from the question I asked and the question Justice Kagan asked that if they were just producers, the raisins got set aside, they were paid for only the ones that went to market, they could go to the Court of Claims. |
| 0:13:19.060 | 799.060 | JUSTICE GINSBURG | handler | But now they're just handlers, as this entity is for most of the raisins that are involved, some 80 percent, right? |
| 0:13:24.700 | 804.700 | JUSTICE GINSBURG | raisins | But now they're just handlers, as this entity is for most of the raisins that are involved, some 80 percent, right? |
| 0:13:27.360 | 807.360 | JUSTICE GINSBURG | percent | But now they're just handlers, as this entity is for most of the raisins that are involved, some 80 percent, right? |
| 0:13:28.900 | 808.900 | JUSTICE GINSBURG | percent | It's only about 20 percent is their own. |
| 0:13:35.880 | 815.880 | JUSTICE GINSBURG | handler | So could this work for someone who was just a handler, doesn't produce any raisins? |
| 0:13:37.660 | 817.660 | JUSTICE GINSBURG | raisins | So could this work for someone who was just a handler, doesn't produce any raisins? |
| 0:13:40.060 | 820.060 | MR. MCCONNELL | handler | So if they are just a handler -- |
| 0:13:47.820 | 827.820 | MR. MCCONNELL | handler | -- as the Department of Agriculture treated them, as far as the Department of Agriculture is concerned they are only a handler. |
| 0:14:04.960 | 844.960 | JUSTICE GINSBURG | handler | Apparently it wasn't enough just to be a handler or just to be a producer. |
| 0:14:20.340 | 860.340 | JUSTICE GINSBURG | handler | The claim that you're making turns on the coincidence of being both the producer and a handler. |
| 0:14:24.800 | 864.800 | MR. MCCONNELL | Horne | I think that we -- that the Hornes ought to prevail on either -- in either of their capacities. |
| 0:14:29.300 | 869.300 | JUSTICE GINSBURG | handler | So any handler, any handler could be making the same claim? |
| 0:14:33.080 | 873.080 | MR. MCCONNELL | handler | Any handler who has a business model that is similar to this. |
| 0:14:37.900 | 877.900 | MR. MCCONNELL | handler | But most handlers -- |
| 0:14:43.220 | 883.220 | MR. MCCONNELL | handler | So most handlers, if they're in compliance with the order, they take all the raisins from the producers, they only pay for -- for the free pool of raisins. |
| 0:14:48.880 | 888.880 | MR. MCCONNELL | raisins | So most handlers, if they're in compliance with the order, they take all the raisins from the producers, they only pay for -- for the free pool of raisins. |
| 0:14:54.940 | 894.940 | MR. MCCONNELL | reserve | They don't pay for the reserve raisins and they never have any interest in the reserve raisins. |
| 0:14:55.280 | 895.280 | MR. MCCONNELL | raisins | They don't pay for the reserve raisins and they never have any interest in the reserve raisins. |
| 0:15:02.020 | 902.020 | MR. MCCONNELL | Horne | In this case, the Hornes did not operate that way. |
| 0:15:07.980 | 907.980 | MR. MCCONNELL | raisins | The -- the producers received full value for all of their raisins. |
| 0:15:21.100 | 921.100 | MR. MCCONNELL | Horne | The -- the entire pocketbook injury in this case is borne by the Hornes in their capacity as a handler. |
| 0:15:23.460 | 923.460 | MR. MCCONNELL | handler | The -- the entire pocketbook injury in this case is borne by the Hornes in their capacity as a handler. |
| 0:15:25.300 | 925.300 | JUSTICE SOTOMAYOR | Horne | In the Horne model, the handlers buy -- buy the free raisins and then pay the producers, is that what it -- |
| 0:15:26.420 | 926.420 | JUSTICE SOTOMAYOR | handler | In the Horne model, the handlers buy -- buy the free raisins and then pay the producers, is that what it -- |
| 0:15:29.460 | 929.460 | JUSTICE SOTOMAYOR | raisins | In the Horne model, the handlers buy -- buy the free raisins and then pay the producers, is that what it -- |
| 0:15:37.460 | 937.460 | JUSTICE SOTOMAYOR | raisins | Oh, so that's the difference in this model, they don't take title to the raisins is what you're saying? |
| 0:15:39.860 | 939.860 | MR. MCCONNELL | Horne | And the Hornes believed that this would mean that they were not handlers. |
| 0:15:43.720 | 943.720 | MR. MCCONNELL | handler | And the Hornes believed that this would mean that they were not handlers. |
| 0:15:46.500 | 946.500 | MR. MCCONNELL | handler | And that -- and they were found to be handlers anyway. |
| 0:16:20.240 | 980.240 | JUSTICE SOTOMAYOR | fine | Meaning, doesn't the system have an interest in ensuring that people comply with their legal obligations, and to the extent that you choose to violate the law the way they have here, that the fine is punitive and not compensatory. |
| 0:16:26.180 | 986.180 | JUSTICE SOTOMAYOR | raisins | Meaning, you don't own the raisins, but you were obligated to put raisins aside for someone else. |
| 0:16:46.940 | 1006.940 | JUSTICE SOTOMAYOR | raisins | Since you didn't own the raisins, the taking is the fine is what you want to call the taking. |
| 0:16:48.400 | 1008.400 | JUSTICE SOTOMAYOR | fine | Since you didn't own the raisins, the taking is the fine is what you want to call the taking. |
| 0:16:56.240 | 1016.240 | MR. MCCONNELL | raisins | The taking is what the government demanded, which was either give me your house or give me your money, give me your raisins or give us the monetary equivalent. |
| 0:17:00.400 | 1020.400 | JUSTICE SOTOMAYOR | raisins | But they're not your raisins. |
| 0:17:00.871 | 1020.871 | JUSTICE SOTOMAYOR | raisins | They’re not your raisins. |
| 0:17:04.920 | 1024.920 | MR. MCCONNELL | raisins | By the time -- by the time this order was enforced, the raisins were gone and so as a practical matter, only one of those two alternatives was left as a matter of timing. |
| 0:17:24.340 | 1044.340 | JUSTICE ALITO | raisins | Well, but in answer to Justice Ginsburg's question that -- you said the producers could go to the -- the Court of Federal Claims to contest the taking of -- producers could go to contest the taking of raisins. |
| 0:17:26.560 | 1046.560 | MR. MCCONNELL | raisins | If they had not been paid for the raisins. |
| 0:17:38.200 | 1058.200 | MR. MCCONNELL | handler | It withdraws Tucker Act jurisdiction only for handlers. |
| 0:17:40.707 | 1060.707 | JUSTICE ALITO | handler | Only for handlers. |
| 0:18:34.920 | 1114.920 | MR. MCCONNELL | handler | Each of those was -- please substitute the word "handler" for each of those. |
| 0:18:37.300 | 1117.300 | MR. MCCONNELL | handler | It's only the handlers that are regulated under this -- under this program. |
| 0:18:45.980 | 1125.980 | MR. MCCONNELL | handler | So -- and -- and my clients were treated as handlers. |
| 0:19:04.040 | 1144.040 | MR. MCCONNELL | handler | And it's -- it's I think quite a Catch 22 for the government to come along and say, although we are fining you $700,000 in your capacity as a handler, you're not a handler for purposes of challenging the legality of that order. |
| 0:19:13.340 | 1153.340 | JUSTICE BREYER | handler | I feel like handlers, purchasers, raisins, like an old Abbott and Costello movie. |
| 0:19:15.600 | 1155.600 | JUSTICE BREYER | raisins | I feel like handlers, purchasers, raisins, like an old Abbott and Costello movie. |
| 0:19:27.700 | 1167.700 | JUSTICE BREYER | raisins | There -- there are some people, they've been -- they are either -- they have some raisins, all right. |
| 0:19:33.720 | 1173.720 | JUSTICE BREYER | raisins | And these particular people, whom the Department has said have acquired the raisins, it said they acquired the raisins. |
| 0:19:37.400 | 1177.400 | JUSTICE BREYER | raisins | And so they're there with some raisins, and then the government says, do this thing with your raisins. |
| 0:19:55.460 | 1195.460 | JUSTICE BREYER | fine | Call it a fine, call it what you want. |
| 0:20:21.420 | 1221.420 | MR. MCCONNELL | fine | They have not yet paid the fine. |
| 0:20:51.300 | 1251.300 | MR. MCCONNELL | Horne | We could not go to the court -- the Hornes could not go to the Court of Claims right now. |
| 0:20:59.100 | 1259.100 | MR. MCCONNELL | fine | What the government says is that they should pay the $700,000 fine first and then go to the Court of Claims to get it back. |
| 0:21:16.040 | 1276.040 | JUSTICE KAGAN | fine | I think that's true, Mr. McConnell, as to part of the fine, that part of the fine falls under Apfel, but not the other part. |
| 0:21:27.160 | 1287.160 | JUSTICE KAGAN | penalty | But as to the penalty part, I don't really understand how the Apfel argument would go. |
| 0:21:32.940 | 1292.940 | JUSTICE KAGAN | penalty | It seems to me that as to the penalty part, the key thing is that if they had handed over the raisins, they could have gone to the Court of Federal Claims and had the compensation done there. |
| 0:21:36.740 | 1296.740 | JUSTICE KAGAN | raisins | It seems to me that as to the penalty part, the key thing is that if they had handed over the raisins, they could have gone to the Court of Federal Claims and had the compensation done there. |
| 0:21:54.820 | 1314.820 | MR. MCCONNELL | fine | Well, the most pertinent case for that part of the fine, for the penalty part, is Missouri Pacific Railroad v. Nebraska. |
| 0:21:55.440 | 1315.440 | MR. MCCONNELL | penalty | Well, the most pertinent case for that part of the fine, for the penalty part, is Missouri Pacific Railroad v. Nebraska. |
| 0:22:28.400 | 1348.400 | MR. MCCONNELL | fine | That gets up to this Court and an opinion by Mr. -- Justice Holmes, the Court holds that that is a taking and that the railroad is entitled to challenge the taking in the form of the fine. |
| 0:22:29.520 | 1349.520 | MR. MCCONNELL | penalty | So for -- for the penalty portion, the punishment portion of the fine, Missouri Pacific Railroad is actually the more pertinent decision. |
| 0:22:32.720 | 1352.720 | MR. MCCONNELL | fine | So for -- for the penalty portion, the punishment portion of the fine, Missouri Pacific Railroad is actually the more pertinent decision. |
| 0:24:09.460 | 1449.460 | JUSTICE SOTOMAYOR | raisins | Mr. McConnell, in -- in -- if the producers had decided to challenge this as a Tucker Act violation, they would have had to hand over the raisins? |
| 0:24:13.460 | 1453.460 | JUSTICE SOTOMAYOR | raisins | Or could they have just held on to the raisins and said, I'm not handing it over until I get just compensation? |
| 0:24:23.280 | 1463.280 | MR. MCCONNELL | raisins | So had they held on to their own raisins and sold them, I assume, you don't -- not just left them rot, if they had sold them, then the Department of Agriculture would have called them a handler because anyone who sells raisins is called a handler, and then they would be fined in their capacity as a handler and it would be a somewhat similar case to this one. |
| 0:24:33.280 | 1473.280 | MR. MCCONNELL | handler | So had they held on to their own raisins and sold them, I assume, you don't -- not just left them rot, if they had sold them, then the Department of Agriculture would have called them a handler because anyone who sells raisins is called a handler, and then they would be fined in their capacity as a handler and it would be a somewhat similar case to this one. |
| 0:26:49.650 | 1609.650 | MR. MCCONNELL | reserve | May I reserve the remaining time? |
| 0:27:22.070 | 1642.070 | MR. PALMORE | raisins | Raisins and money. |
| 0:29:46.510 | 1786.510 | MR. PALMORE | raisins | And moreover, they decided something separate, which is at JA-305 they said something different, which is the kind of threshold defect in the takings claim turning on raisins, which is there is a capacity problem. |
| 0:30:04.450 | 1804.450 | MR. PALMORE | reserve | The capacity problem is this: In 2002, after having been strictly raisin producers since 1969, entering into a market where there was a reserve requirement from the beginning, they knew what they were getting into, they decided to adopt a new business model, as Petitioner's counsel says. |
| 0:30:25.710 | 1825.710 | MR. PALMORE | handler | But what they did was they took on the obligations of a handler. |
| 0:30:26.790 | 1826.790 | MR. PALMORE | handler | They became raisin handlers in 2002. |
| 0:30:34.110 | 1834.110 | MR. PALMORE | handler | And what came with that status were a series of regulatory obligations that apply only to handlers and under the AMAA can apply only to handlers: The requirement to have raisins inspected, the requirement to file truthful reports, the requirement to make records available, and the requirement to separate out raisins into what's called free tonnage and reserve tonnage, any raisins processed, it doesn't matter who owns them. |
| 0:30:39.610 | 1839.610 | MR. PALMORE | raisins | And what came with that status were a series of regulatory obligations that apply only to handlers and under the AMAA can apply only to handlers: The requirement to have raisins inspected, the requirement to file truthful reports, the requirement to make records available, and the requirement to separate out raisins into what's called free tonnage and reserve tonnage, any raisins processed, it doesn't matter who owns them. |
| 0:30:50.170 | 1850.170 | MR. PALMORE | reserve | And what came with that status were a series of regulatory obligations that apply only to handlers and under the AMAA can apply only to handlers: The requirement to have raisins inspected, the requirement to file truthful reports, the requirement to make records available, and the requirement to separate out raisins into what's called free tonnage and reserve tonnage, any raisins processed, it doesn't matter who owns them. |
| 0:30:54.610 | 1854.610 | MR. PALMORE | handler | Those are handler-specific regulatory obligations that were imposed upon them, and they violated every single one of them, willfully and intentionally, in order to secure an unfair competitive advantage. |
| 0:31:13.530 | 1873.530 | MR. PALMORE | handler | And what the USDA did was impose penalties on them for the violation of law that -- that attached to them only as raisin handlers. |
| 0:31:22.050 | 1882.050 | MR. PALMORE | handler | And then they invoked the judicial review proceedings in Section 14 that provides a judicial review mechanism only for handlers. |
| 0:31:24.590 | 1884.590 | JUSTICE SCALIA | penalty | Yes, but part of -- part of that penalty was -- you know, your raisins or your life, right? |
| 0:31:27.430 | 1887.430 | JUSTICE SCALIA | raisins | Yes, but part of -- part of that penalty was -- you know, your raisins or your life, right? |
| 0:31:32.790 | 1892.790 | JUSTICE SCALIA | penalty | -- you don't have to pay the penalty if you give us the raisins. |
| 0:31:34.070 | 1894.070 | JUSTICE SCALIA | raisins | -- you don't have to pay the penalty if you give us the raisins. |
| 0:31:37.310 | 1897.310 | MR. PALMORE | raisins | They have to give the raisins. |
| 0:31:40.696 | 1900.696 | JUSTICE SCALIA | raisins | You mean they -- Is that right, they have to give the raisins? |
| 0:31:45.870 | 1905.870 | MR. PALMORE | raisins | They are under a regulatory obligation to provide the raisins. |
| 0:31:52.270 | 1912.270 | JUSTICE SCALIA | raisins | -- that amounts to the same thing, your raisins or the penalty, right? |
| 0:31:52.390 | 1912.390 | JUSTICE SCALIA | penalty | -- that amounts to the same thing, your raisins or the penalty, right? |
| 0:32:02.290 | 1922.290 | MR. PALMORE | raisins | Mr. McConnell referred to a demand letter saying your raisins or your money. |
| 0:32:06.790 | 1926.790 | MR. PALMORE | handler | There was an initial demand letter saying: You are a handler; you have to comply; we're going to come get the raisins. |
| 0:32:09.050 | 1929.050 | MR. PALMORE | raisins | There was an initial demand letter saying: You are a handler; you have to comply; we're going to come get the raisins. |
| 0:32:14.630 | 1934.630 | MR. PALMORE | raisins | The second demand letter said, we showed up -- literally it says, we showed up with our truck, you didn't provide the raisins, so now you have got to provide the cash equivalent. |
| 0:32:27.350 | 1947.350 | MR. PALMORE | reserve | Not just the failure to reserve, but all these handler-specific obligations. |
| 0:32:28.310 | 1948.310 | MR. PALMORE | handler | Not just the failure to reserve, but all these handler-specific obligations. |
| 0:32:31.950 | 1951.950 | MR. PALMORE | raisins | They didn't make raisins available for inspection. |
| 0:32:38.330 | 1958.330 | MR. PALMORE | handler | There were a whole host of regulatory violations that were at issue here, and when they invoked the handler review action in the district court they could assert defenses as a handler. |
| 0:33:16.490 | 1996.490 | MR. PALMORE | raisins | We have been talking about the claim involving the raisins, which fails for a to capacity reason and a just compensation reason. |
| 0:36:46.530 | 2206.530 | JUSTICE BREYER | raisins | What it does is it takes raisins that we grow, in effect throws them in the river. |
| 0:37:00.990 | 2220.990 | JUSTICE BREYER | raisins | And they think as a matter of policy that just hurts people by raising prices, and as a matter of constitutional law it takes raisins from some people that belong to them and uses them for this bad purpose. |
| 0:37:08.910 | 2228.910 | JUSTICE BREYER | fine | Fine. |
| 0:37:55.090 | 2275.090 | MR. PALMORE | raisins | Justice Breyer, we've now shifted back to the -- the first theory about the property, which is the raisins. |
| 0:38:00.970 | 2280.970 | MR. PALMORE | raisins | What they could have done in 2002, would they have been a producer of raisins, solely a producer of raisins for decades, at any point during -- between 1969 and 2002, they could have gone to the Court of Claims and said, this reserve requirement, is a taking of my raisins, I want my just compensation. |
| 0:38:10.430 | 2290.430 | MR. PALMORE | reserve | What they could have done in 2002, would they have been a producer of raisins, solely a producer of raisins for decades, at any point during -- between 1969 and 2002, they could have gone to the Court of Claims and said, this reserve requirement, is a taking of my raisins, I want my just compensation. |
| 0:38:37.250 | 2317.250 | JUSTICE SCALIA | raisins | Did -- did Congress create a statute in which we're going to take your raisins and then you can go to the Court of Claims and get your money back. |
| 0:39:00.250 | 2340.250 | JUSTICE SCALIA | raisins | But to say that Congress contemplated -- you know, we'll take your raisins and then you sue in the Court of Claims, they give you your money back. |
| 0:39:20.770 | 2360.770 | MR. PALMORE | reserve | Raisin producers, or in the Cal-Almond case it was an almond producer, went to the Court of Claims and said this reserve requirement is a taking, I want my money. |
| 0:39:39.430 | 2379.430 | MR. PALMORE | reserve | That said, we do agree that it is actually a close question whether Congress would have intended compensation to be provided in a situation like this one, in the event the raisin reserve program were found to be a taking. |
| 0:40:05.050 | 2405.050 | JUSTICE SCALIA | raisins | You think that the way the statute is supposed to operate, once it is held that this is an unconstitutional taking, is that every year, the government takes the raisins and every year, the grower goes to the Court of Claims and gets the money back for the raisins. |
| 0:40:21.070 | 2421.070 | JUSTICE SCALIA | raisins | Every year we're going to take raisins and every year we're going to pay you in the Court of Claims. |
| 0:40:53.270 | 2453.270 | MR. PALMORE | reserve | A reserve requirement is only one way of complying with the kind of supply control provisions of the statute. |
| 0:41:11.530 | 2471.530 | MR. PALMORE | reserve | But I'd also point out that in this Court's precedence in Monsanto and Regional Rail, those were both statutory schemes which had their own compensation mechanism, as does this one, this reserve raisins that producers do get paid sometimes for them in a smaller amount. |
| 0:41:12.110 | 2472.110 | MR. PALMORE | raisins | But I'd also point out that in this Court's precedence in Monsanto and Regional Rail, those were both statutory schemes which had their own compensation mechanism, as does this one, this reserve raisins that producers do get paid sometimes for them in a smaller amount. |
| 0:41:34.510 | 2494.510 | JUSTICE GINSBURG | handler | Mr. Palmore, am I incorrect in thinking that the government is saying, handlers cannot raise the constitutionality of the Raisin Marketing Order? |
| 0:41:48.250 | 2508.250 | JUSTICE GINSBURG | handler | What about the handlers? |
| 0:42:24.610 | 2544.610 | MR. PALMORE | raisins | If the property is the raisins, they can't raise that in this proceeding. |
| 0:42:44.690 | 2564.690 | MR. PALMORE | fine | If the claim -- if the claim is that the money that was taken from me, the fine, that itself is a taking, then we think that claim can and must be brought in the context of the AMAA proceeding. |
| 0:43:01.070 | 2581.070 | MR. PALMORE | fine | That was not how the Court of Appeals understood the claim here to be, and there's no precedent for the idea that a fine for violation of law can be articulated as a taking of the lawbreaker's property without just compensation. |
| 0:43:31.790 | 2611.790 | JUSTICE KENNEDY | penalty | I -- I thought that what we were going to decide was whether or not, assuming you can go to the Court of Claims, you must go to the Court of Claims, can you prefer to wait, have a penalty assessed against you and say this is unconstitutional, it's a taking. |
| 0:43:48.050 | 2628.050 | MR. PALMORE | fine | But, Justice Kennedy, the -- the Ninth Circuit didn't understand the taking claim to be that the fine for my violation of law is a taking of my money. |
| 0:43:59.730 | 2639.730 | MR. PALMORE | raisins | They understood the claim to be that the taking of producers' raisins is a taking, and we lawfully resisted it because it was an unconstitutional taking. |
| 0:44:29.050 | 2669.050 | JUSTICE BREYER | raisins | So the poor children with their noses pressed to the glass because they can't pay the raisins, their parents are the ones who are paying the compensation. |
| 0:46:21.990 | 2781.990 | JUSTICE SOTOMAYOR | handler | In the normal situation, the handler, I'm being told, would actually have title to the raisins, and they would pay the producers for the raisins. |
| 0:46:28.070 | 2788.070 | JUSTICE SOTOMAYOR | raisins | In the normal situation, the handler, I'm being told, would actually have title to the raisins, and they would pay the producers for the raisins. |
| 0:46:38.530 | 2798.530 | JUSTICE SOTOMAYOR | handler | In that situation, where the handlers actually own the property, would they be able to raise a taking defense? |
| 0:46:53.550 | 2813.550 | MR. PALMORE | handler | If the handler is actually buying raisins from the producer, the handler never takes title to the reserve raisins. |
| 0:46:55.330 | 2815.330 | MR. PALMORE | raisins | If the handler is actually buying raisins from the producer, the handler never takes title to the reserve raisins. |
| 0:46:59.070 | 2819.070 | MR. PALMORE | reserve | If the handler is actually buying raisins from the producer, the handler never takes title to the reserve raisins. |
| 0:47:01.510 | 2821.510 | MR. PALMORE | reserve | And he doesn't pay for the reserve raisins. |
| 0:47:01.790 | 2821.790 | MR. PALMORE | raisins | And he doesn't pay for the reserve raisins. |
| 0:47:04.550 | 2824.550 | MR. PALMORE | raisins | He takes title to the free-tonnage raisins and the title to the reserve raisins passes, as a matter of law, from the producer to the Raisin Administrative Committee. |
| 0:47:07.270 | 2827.270 | MR. PALMORE | reserve | He takes title to the free-tonnage raisins and the title to the reserve raisins passes, as a matter of law, from the producer to the Raisin Administrative Committee. |
| 0:47:12.590 | 2832.590 | MR. PALMORE | handler | The handler never owns those raisins. |
| 0:47:13.830 | 2833.830 | MR. PALMORE | raisins | The handler never owns those raisins. |
| 0:47:19.410 | 2839.410 | JUSTICE SOTOMAYOR | raisins | So they are missing a business opportunity because they can't take title to those raisins. |
| 0:47:23.510 | 2843.510 | MR. PALMORE | raisins | They would never pay for those -- they would never pay for those raisins because they can't take title. |
| 0:47:27.370 | 2847.370 | MR. PALMORE | raisins | They can't lawfully take title to those raisins. |
| 0:47:44.810 | 2864.810 | JUSTICE SOTOMAYOR | handler | Whether it's a taking -- whether there's a takings claim for the handler because the handler is being asked to do things -- |
| 0:47:49.070 | 2869.070 | MR. PALMORE | handler | But the handler's property is not being taken, and that's critical. |
| 0:47:54.770 | 2874.770 | MR. PALMORE | handler | There are separate takings claims that handlers have advanced that -- that could be asserted through this process. |
| 0:48:02.350 | 2882.350 | MR. PALMORE | raisins | For instance, there was a case called Lion Raisins from the Federal Circuit that we cite in our brief, in which the issue was that the handler provided bins to store the raisins, and he didn't get his bins back. |
| 0:48:06.310 | 2886.310 | MR. PALMORE | handler | For instance, there was a case called Lion Raisins from the Federal Circuit that we cite in our brief, in which the issue was that the handler provided bins to store the raisins, and he didn't get his bins back. |
| 0:48:11.790 | 2891.790 | MR. PALMORE | handler | That was a handler takings claim, and that had to be asserted in the context of this handler review scheme. |
| 0:48:19.050 | 2899.050 | MR. PALMORE | handler | But the handler doesn't own the raisins under this scheme. |
| 0:48:20.990 | 2900.990 | MR. PALMORE | raisins | But the handler doesn't own the raisins under this scheme. |
| 0:48:51.210 | 2931.210 | MR. PALMORE | handler | And if someone wants to take on both roles, they will be regulated only as a handler. |
| 0:48:57.530 | 2937.530 | MR. PALMORE | handler | So the regulatory obligations that applied to Petitioners when they adopted this business model were handler-only regulatory obligations, and then this is a handler judicial review proceeding. |
| 0:49:37.650 | 2977.650 | MR. PALMORE | raisins | But there's no unfairness or no due process issue here at all because they -- in 2002, when -- when Petitioners decided to engage in this, these regulatory violations in order to secure an unfair advantage over their competitors, as was found by the ALJ at JA41, at that point they could have sought compensation for the past 6 years of raisins that they had provided. |
| 0:49:48.990 | 2988.990 | MR. PALMORE | handler | And to the extent they wanted to claim going forward, they could have continued to use compliant handlers and sued every month for compensation in the Court of Claims. |
| 0:51:26.530 | 3086.530 | MR. PALMORE | handler | But there's a separate issue in that there's this capacity issue, which is a separate point that the Ninth Circuit made at JA305, when it pointed out that this was a producer claim, and that's something that -- that was strictly a producer claim and wasn't -- wasn't a fit for this handler review action, and that's something that could also be considered on remand. |
| 0:52:05.770 | 3125.770 | JUSTICE BREYER | handler | There is some opinion here which says these handlers acquired the raisins. |
| 0:52:07.130 | 3127.130 | JUSTICE BREYER | raisins | There is some opinion here which says these handlers acquired the raisins. |
| 0:52:21.530 | 3141.530 | MR. PALMORE | handler | There was no question under the regulatory scheme here that Petitioners were handlers. |
| 0:52:30.310 | 3150.310 | MR. PALMORE | handler | And a handler is anyone who sells raisins. |
| 0:52:31.950 | 3151.950 | MR. PALMORE | raisins | And a handler is anyone who sells raisins. |
| 0:54:50.857 | 3290.857 | JUSTICE KENNEDY | penalty | No, no. In the administrative proceeding where they are charged with -- where a penalty is being assessed against them. |
| 0:58:10.950 | 3490.950 | JUSTICE SOTOMAYOR | handler | Well, they've conceded that it doesn't apply to handlers. |
| 0:58:12.990 | 3492.990 | MR. MCCONNELL | handler | To handlers. |
| 0:58:33.130 | 3513.130 | MR. MCCONNELL | handler | And secondly, we certainly -- and then that is in our capacity as handler. |
| 0:58:38.130 | 3518.130 | MR. MCCONNELL | raisins | Essentially, the Department of Agriculture's view is that during those couple of days when the raisins are going through our packing plant, that we acquired them and possessed them during those couple of days and that we should have given them their -- their share. |
| 0:58:48.470 | 3528.470 | MR. MCCONNELL | raisins | That's raisins, that's not money. |
| 0:58:53.650 | 3533.650 | MR. MCCONNELL | raisins | But by the time they get around to enforcing that and so forth, the raisins are gone and now the money stands in -- stands in for the raisins. |
| 0:59:17.410 | 3557.410 | MR. MCCONNELL | handler | Whatever might be, that taking, that taking is in the capacity as a handler. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:09.240 to 0:03:09.240, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:09.240] MR. MCCONNELL: Mr. Chief Justice, and may it please the Court: There's a surprising number of difficult merits questions lurking in this case, mostly involving whether there was a taking, and if so, how it should be conceptualized and valued.

[0:00:22.840] JUSTICE SOTOMAYOR: Could I -- could I just stop you on a factual matter --

[0:00:25.740] MR. MCCONNELL: Certainly.

[0:00:25.760] JUSTICE SOTOMAYOR: -- because it has confused me. As I look at the captions of the cases, there appear to be two different partnerships: One partnership, known as Raisin -- doing business as Raisin Valley Farms, has Mr. Horne and his wife as the partners. Larsen Valley, the producer -- not the producer, the handler -- has four other, the Hornes, plus two other people. So who owns the raisins? Isn't that the first partnership of the husband and wife? And isn't the handler a second partnership that does the business of handling?

[0:01:16.640] MR. MCCONNELL: The other two partners in Lassen were Laura Horne's parents, now deceased.

[0:01:23.080] JUSTICE SOTOMAYOR: But the estates have been substituted.

[0:01:24.400] MR. MCCONNELL: Substituted. That's right.

[0:01:25.620] JUSTICE SOTOMAYOR: So isn't it two legal entities, one who owns and one who handles? One partnership produces, one partnership handles?

[0:01:35.200] MR. MCCONNELL: The Department of Agriculture did not distinguish among them.

[0:01:38.240] JUSTICE SOTOMAYOR: Well, I don't care if they did or they didn't. I mean, we should know. Are they two separate legal entities? One who produces --

[0:01:45.880] MR. MCCONNELL: They are separate -- they are separate legal entities, all effectively controlled by the same family.

[0:01:51.720] JUSTICE SOTOMAYOR: Well, that's -- you know, in the cat -- you get some limited liability by creating separate entities, so the creature who owns is one partnership, and the -- and the entity that produces, that handles, is a second one.

[0:02:07.640] JUSTICE SCALIA: I assume this is one of those difficult merits questions you were alluding to, it doesn't go to whether there's jurisdiction, but to whether the claim of a taking can be asserted by the partnership in question, isn't it?

[0:02:23.660] MR. MCCONNELL: That's right, Justice Scalia.

[0:02:24.500] JUSTICE SCALIA: I don't -- I don't see how it goes to jurisdiction, which is the only question before us.

[0:02:27.220] JUSTICE SOTOMAYOR: Well, it does to my mind because what is the claim, assuming that the producer owns -- the producer entity owns the raisins. What exactly is being taken from the handlers? Is it the percentage -- it can't be the raisins because they don't own them.

[0:02:45.500] MR. MCCONNELL: Well, Justice Sotomayor, I'm -- I'm delighted to preview our -- our argument on the merits on that.

[0:02:51.840] JUSTICE SOTOMAYOR: What -- what do they own?

[0:02:52.600] MR. MCCONNELL: So the -- so the --

[0:02:52.820] JUSTICE SOTOMAYOR: What is it that's being taken from the handler entity?

[0:02:56.380] MR. MCCONNELL: The order in this case was issued against the -- the Hornes in their capacity as a handler only, so the entire fine was paid by them. None of the fine is attributable

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 10, 2013.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2012/12-123
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2012/12-123/20130610o_12-123.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.5 MB)
- Length: 0:05:58.687 (358.687 s)
- Words: 748, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 722 of Whisper's 748 words (96.5%; Oyez has 749).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:06.380 | 15 |
| JUSTICE THOMAS | 0:00:07.260 | 0:05:57.120 | 729 |

### Full text, as plain text

Whisper's wording, the whole announcement, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: Justice Thomas has our opinion this morning in Case 12-123, Horne v. Department of Agriculture.

[0:00:07.260] JUSTICE THOMAS: This case comes to us on a writ of certiorari to the United States Court of Appeals for the Ninth Circuit. During the Great Depression, Congress enacted the Agricultural Marketing Agreement Act of 1937. I will refer to this as the Marketing Agreement Act. This Act stabilized, was enacted to stabilize agricultural commodity prices. California raisins are one of the many commodities regulated by the Act. Pursuant to the Marketing Agreement Act, the Secretary of Agriculture issued regulations creating the Raisin Administrative Committee. Each year, the Raisin Administrative Committee recommends whether to place a percentage of the raisin crop in a so-called reserve pool that is not sold on the open market. If a reserve pool is established, raisin handlers are required to set aside a portion of the raisins they receive from producers and hold them in the pool. Producers receive no upfront compensation for these raisins. The Raisin Administrative Committee then decides whether to give the raisins away or sell them in foreign markets. Petitioners are California raisin growers who became frustrated with this regulatory scheme. Since the regulations apply only to raisin handlers, petitioners decided to process and sell their own raisins without using a third-party handler in an effort to avoid the requirement that they contribute raisins to the reserve pool. They also agreed to process raisins from 60 other farms. The Department of Agriculture determined that petitioners were raisin handlers and demanded that they turn over the requisite percentage of raisins. After petitioners refused, the Department of Agriculture initiated administrative proceedings seeking civil penalties and reimbursement for the raisins that petitioner refused to surrender. Petitioners argued that they were producers, not handlers, and therefore did not have to give up the raisins. They also argued that the raisin regulations violated the Fifth Amendment prohibition against taking property without just compensation. An administrative law judge found that petitioners were handlers and that they had violated the raisin regulations. He imposed fines and rejected petitioners' takings defense. On appeal, a judicial officer agreed. Petitioners then sought review in the Federal, in Federal district court, which concluded that petitioners were handlers rather than producers and rejected petitioners' takings claims on the merits. The Ninth Circuit affirmed. It agreed that petitioners were handlers, but concluded that it lacked jurisdiction to adjudicate the takings claims because it was not ripe. According to the Ninth Circuit, petitioners raised their takings claims as producers, not handlers, and thus were required to pay the fines and then file suit in the Court of Federal Claims. In an opinion filed with the clerk today, we reverse. Although petitioners argued before the agency that they were producers and thus not subject to the raisin regulations, both the agency and the district court concluded that they were handlers. Because the raisin regulations imposed duties on petitioners only in their capacity as handlers, petitioners' takings claims, raised as a defense against fines imposed for violating those duties, is necessarily raised in that same capacity. In finding otherwise, the Ninth Circuit confused petitioner's statutory argument that they were producers with their constitutional argument that, even assuming they were handlers, the fines violated the Fifth Amendment. As a result, the relevant question is whether a Federal court has jurisdiction to adjudicate a takings defense raised by a handler. Petitioners were subject to a final agency order imposing fines and thus suffered an injury sufficient for Article III jurisdiction. The government argues that petitioner's claim is unripe because the Tucker Act affords them a remedy. The Tucker Act normally requires people who want or individuals who want to sue the United States for damages to bring their suits in the court of Federal claims. However, when the statute contains its own self-executing remedial scheme, Tucker Act jurisdiction is replaced by that scheme. In this case, we conclude that the Marketing Agreement Act provides such a comprehensive remedial scheme and that nothing in the Marketing Agreement Act borrows handlers from raising constitutional defenses to the Department of Agriculture's enforcement action. Accordingly, petitioners are free to raise their takings claims in these proceedings. Indeed, it would make little sense to force a party to pay an assessed fine in one proceeding and then turn around and sue for recovery of that same money in another. We therefore reverse the judgment of the Ninth Circuit. The opinion of the Court is unanimous.

### Words Whisper invented

Words that only Whisper has, and runs of 3 or more words where Whisper and Oyez's transcript disagree, were re-transcribed on their own, with 6 s either side. These Whisper words aren't in Oyez and weren't heard again, so they were dropped from the files:

- 0:00:06.980-0:00:07.260: "Horne, Jr.:"

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:00.000 | Justice | (nothing) |
| 0:00:22.140 | to this | just |
| 0:00:27.580 | (nothing) | act -- was inducted to -- |
| 0:01:12.480 | producers | procedures |
| 0:01:15.600 | Producers | Procedures |
| 0:02:33.620 | argued | argue |
| 0:02:59.840 | the Federal, in | (nothing) |
| 0:03:17.780 | lacked | lacks |
| 0:03:22.200 | ripe. | right. |
| 0:04:02.360 | raised | to raise |
| 0:04:23.340 | the fines | defines |
| 0:04:38.200 | a | (nothing) |
| 0:05:06.200 | the | a |
| 0:05:24.560 | borrows | bars |
| 0:05:28.960 | (nothing) | Department of Agriculture's -- |
