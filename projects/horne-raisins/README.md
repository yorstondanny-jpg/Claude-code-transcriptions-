# horne-raisins: Supreme Court No. 14-275

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: https://www.supremecourt.gov/oral_arguments/audio/2014/14-275
- Audio: https://www.supremecourt.gov/media/audio/mp3files/14-275.mp3
- Official transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2014/14-275_2b8e.pdf

## Numbers

- ASR model: faster-whisper `medium.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 59 min on 4 CPU cores
- Audio length: 1:01:12.372 (3672.372 s)
- `audio/argument.mp3`: mono, 64 kbps, 29.4 MB
- Official words: 10555 (plus 7 `(Laughter.)` markers), in 341 speaker turns
- ASR words: 9826
- Official words matched to an ASR word: 9554 of 10555 (**90.52%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
  Not counted: `989.166(c),` 3524.600-3529.100 (4.50 s). A citation is one official word but is spoken as several; its time is the real time taken to say it.
- PASS: match rate over 85%. 90.52% (threshold 85%).

568 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
happened 9 times. ASR words with no official counterpart
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
to that sound, at least 0.2 s from its start. This trimmed 13 words.

Any word still longer than 3 s gets the audio 3 s either side of it re-transcribed on its own
and that stretch of official words re-aligned to the fresh ASR. Without an hour of context,
Whisper often hears the cross-talk it skipped the first time. The new times are kept only if they
fit between the untouched neighbours and bring the word under 3 s. This fixed 0
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 14-275 2014 horne-raisins --model medium.en --opinion --long-questions 10 --opinion-full-text --opinion-mentions "percentages,dollar amounts,years,raisins,reserve,farmers,Horne/Horn"

## The 10 longest uninterrupted questions from a justice

Each is one justice's turn in the transcript, which ends when anyone else speaks, timed from its first word to its last. Longest first; official wording.

### 1. JUSTICE BREYER, 0:33:51.880 to 0:35:49.540 (117.7 s, 309 words)

> Look -- look. This is -- I'm having trouble with the same thing. I agree so far with what the Chief Justice said. Go back to the New Deal. You can, in fact, burn raisins, the point of which was to have fewer raisins, the result of which was to raise the price of raisins from $100 a pound to -- or a bushel -- to 400. That was thought to make the farmer better off, which it did. And it made the customers worse off. Then someone had a good idea and said it's sort of wasteful to burn raisins. Let's take the raisins we'd otherwise burn and give them to schoolchildren. And maybe we could even sell a few, and if we do, we'll give that extra money to the farmer, too. Now we have schoolchildren with raisins. We have the farmer having more money. Sounds like a pretty good program. Of course, you have taken some raisins. But what I don't see is how either the farmer or the schoolchildren are any the worse off. And if they're no worse off, what compensation are these farmers entitled to? Of course, free riders could become yet better off. They could charge at the higher price that the program creates, $800. But, after all, that isn't the issue because you have to have, as a rule, no free riders. And once you admit that as a rule, everyone, including perhaps these plaintiffs, are better off than none at all. Now, that's a very simple argument. It's what I understand to be the economics of the Brannan Plan, the FDR, the 1949, et cetera. And yet, we've had endless cases, complexities, opinions, and fines. And -- and so, therefore, I'm probably wrong with my simple argument. Of course, I doubt that I'm wrong, but nonetheless, I want you to explain what's wrong with it.

### 2. JUSTICE BREYER, 0:11:59.780 to 0:13:17.040 (77.3 s, 231 words)

> -- the Constitution doesn't forbid takings. It says what you have to do is pay just compensation. Now, it's at that point I want to know what happens, because I guess the government could argue, look at this program, it's a big program. This program, what it does is it gives raisin farmers, at the public's expense, more money. So if, in fact, you don't want us to take your raisins, all right, fine. But there'd be no program if everybody said that. So we have a rule against free riders. Now we'll give you what it cost you to take your raisins. What it cost you is, in fact, the difference between what you receive given the program and what you would receive without the program. That difference works in your favor. It gives you money. It doesn't take money. So there is no compensation due. In fact, if we were to have compensation, you should pay us, the government. So how are you going to get by that part? And if you can't get by that part, how are you going to avoid paying the fine? See, I don't see the relation between the taking argument, which is maybe all we have to decide, and how eventually you either get some money or you don't have to pay the fine. If you have a minute, I'd appreciate just the explanation.

### 3. JUSTICE KAGAN, 0:18:15.933 to 0:18:59.540 (43.6 s, 122 words)

> Can I take you back, Mr. McConnell, to the -- whether it is a taking point? And I've -- I've just been trying to think about whether your argument would apply to other kinds of programs and how it might apply to other kinds of programs. So how about just programs where the government says, give us -- produce records for us. I'm sure that there are a lot of programs like that in the world. And there is something intuitive about your saying, well, the government is asking us to turn over stuff. And I'm wondering, it seems to me that the government asks people to turn over stuff all the time in the form of records. How would that fare under your argument?

### 4. JUSTICE KAGAN, 0:36:22.880 to 0:37:03.420 (40.5 s, 99 words)

> Mr. -- Mr. Kneedler, if -- I largely agree with what the Chief Justice said. I mean, just the way I think about this program is that this does seem a weird historical anomaly. And all -- am I right that all the rest of these agricultural programs are done differently, such that saying that this was a taking would not affect other agricultural programs? And -- and also, are there any other programs out there -- forget agricultural programs -- but are there any other programs out there that we should be concerned about if we were to think about this as a taking?

### 5. JUSTICE SOTOMAYOR, 0:07:14.800 to 0:07:54.340 (39.5 s, 95 words)

> But neither did they -- but it didn't happen that way in Leonard, either. What the Court was basically saying is the government could do this because this is a good in commerce. As long as it could meet the Penn Central test, that there is some nexus between the government's goal and the -- and the -- and -- and the regulation, then it's okay. Now, there they used it to fertilize oyster ponds or to refertilize the oysters. Here they're doing it to maintain prices and giving you whatever left -- whatever is left over on the reserve.

### 6. CHIEF JUSTICE ROBERTS, 0:33:04.780 to 0:33:41.960 (37.2 s, 125 words)

> This -- this is a -- a historical quirk that you have to defend. You could achieve your -- the government's objectives, just as you do in most other cases, through volume limitations that don't require a physical taking. For whatever reason, in the history of the New Deal, this one was set up differently. And so we're here dealing with a classical, physical taking. We are not going to jeopardize the marketing -- the Agriculture Department's Marketing Order regime. And by the way, it better be the Department of Agriculture that takes these -- you said earlier it's Raisin Committee -- or else you're going to have a lot of trouble in your government speech cases, where you always make the point that these committees are, in fact, the government.

### 7. JUSTICE ALITO, 0:50:46.480 to 0:51:22.840 (36.4 s, 108 words)

> Suppose the same sort of program were carried out with respect to real property. Would you -- would you provide the same answers? Suppose that property owners, owners of real property in a particular area, think that the value of their property would be increased if they all surrendered a certain amount of that property to the government for the purpose of producing a -- creating a park or for some other reason. And so they -- they get the municipality to -- to set up this program, and one of them objects to surrendering this part of that person -- of his or her land. Would -- would that not be a taking?

### 8. JUSTICE GINSBURG, 0:09:32.380 to 0:10:07.360 (35.0 s, 81 words)

> If that's your position, why didn't you ask -- you're attacking this reserve arrangement and the -- the possession -- the government's possession of the raisins themselves. And you -- as far as I've heard so far, you are not attacking volume limit; you cannot market more than X amount. Why didn't you then ask the Department of Agriculture for an exemption from the reserve pool? Instead of -- see, what you're trying to do now is to get rid of the volume limit as well.

### 9. JUSTICE BREYER, 0:15:46.785 to 0:16:21.700 (34.9 s, 115 words)

> Okay. So what we should say, in your view, do you have any objection to my writing, if I were to write it, like this, taking. Yeah, it's a taking. Okay. But the Constitution forbids takings without compensation. The object of the program is, at least in general, to give farmers more compensation than they would have without it. Programs can work badly, sometimes they're counterproductive, but if this is working well, that's what happens. So we send it back to the court to see, did the program work well? Did it work to actually make your -- your client better off? What rules do we follow? That's how we should do this, in your opinion.

### 10. CHIEF JUSTICE ROBERTS, 0:28:40.860 to 0:29:10.400 (29.5 s, 111 words)

> Well, but just -- before you do, I mean, the -- the rationale -- I mean, the government can come up with a rationale to justify those examples really easily. You say cellphone providers benefit greatly if there's a broader cellphone market, if more people are using them. So we're going to take every fifth one and give it to people who might otherwise not be able to afford a cellphone. And that will help cellphone manufacturers , because more and more people will have them. More and more people will want them. Therefore, it's okay. That's the same rationale you're applying here. This is for the good of the people whose property we're taking.

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-40.8 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:06:18.540 | 378.540 | small | 0.84 | 0.20 | 16.1 | 23.5 | yes. Well, so I guess what Justice Sotomayor's question is is why wouldn't the same be true as to raisins? Because raisins are not wild animals, even if they're dancing -- |
| 2 | 0:29:49.460 | 1789.460 | under speech | 0.00 | 0.00 | - | - | Central. This is different. This is different because you come up with the truck and you get the shovels and you take their raisins, probably in the dark of night. |
| 3 | 0:39:47.840 | 2387.840 | small | 0.40 | 0.00 | 7.5 | 9.2 | government can prohibit the -- the introduction of harmful pesticides into interstate commerce. I'm not sure it can prohibit the introduction of raisins. I mean, that's a -- you know, dangerous raisins. |
| 4 | 0:52:57.700 | 3177.700 | small | 0.50 | 0.00 | 9.5 | 11.0 | is a sensible program for you to prevail, do you? No, we do not. The question -- I mean, we could think that this is a ridiculous program; isn't that right? |
| 5 | 0:53:14.700 | 3194.700 | under speech | 0.00 | 0.00 | - | - | every grower since 1949 has had a per se takings. Mr. Kneedler, I'd like to get you -- It doesn't help your case that it's ridiculous, though. You -- you acknowledge that. |
| 6 | 1:00:55.200 | 3655.200 | big | 5.54 | 4.95 | 21.2 | 29.0 | unusual. Mr. McConnell, this is probably neither here nor there, but what has the impact of the drought been on the raisin producers? Do you know? It is not good. |
| 7 | 1:01:02.560 | 3662.560 | under speech | 0.00 | 0.00 | - | - | is probably neither here nor there, but what has the impact of the drought been on the raisin producers? Do you know? It is not good. Very carefully guarded response. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:07.700 to 0:03:07.700, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:07.700] MR. MCCONNELL: Mr. Chief Justice, and may it please the Court: Thank you for being willing to hear this little case a second time. It does involve some important principles and the livelihoods of Marvin and Laura Horne, and more indirectly, hundreds of small California raisin growers will be profoundly affected. This is an administrative enforcement proceeding that was brought by the Department of Agriculture against my clients commanding the relinquishment of funds connected to specific pieces of property, namely, reserve-tonnage raisins. My clients appear in their capacity as handlers, but under their -- in the particular facts of this case, the economic circumstances are somewhat different than are ordinarily true in -- in this industry because as handlers, the Hornes actually assumed the full financial responsibility for the raisins that were not turned over to the Department of Agriculture. The producers in this case were fully paid for their raisins. This is a factual finding to be found in the judicial officer's opinion at 66a of the appendix to the -- to the petition. The Hornes paid the producers for their raisins. According to the judicial officer, those raisins became part of the inventory of the Hornes. The -- when the Raisin Administrative Committee, which I'll refer to as the RAC, came after the raisins, it was the Hornes and the Hornes only who bore the economic burden of this taking.

[0:01:45.840] JUSTICE GINSBURG: I thought that -- I thought the growers were paid only for the volume that they were permitted, that was permitted, the permitted volume, and that they were not paid for what is -- goes in the reserve pool.

[0:02:04.480] MR. MCCONNELL: Justice Ginsburg, that is true in the ordinary course. That was not true in this particular case because of the unusual business model of -- of my clients. These producers were paid the -- for all of their raisins.

[0:02:19.920] JUSTICE GINSBURG: Are you objecting to the volume limitation, or is it just that the -- the reserve pool that you find --

[0:02:30.040] MR. MCCONNELL: We --

[0:02:30.770] JUSTICE GINSBURG: -- troublesome?

[0:02:31.500] MR. MCCONNELL: We believe that a volume limitation would be a use restriction. It might possibly be challengeable under the Penn Central Test, but it is -- would not be a per se taking. In this case, because the government, the RAC, which is an agent of the Department of Agriculture, actually takes possession, ownership of the raisins, it is that -- it is that aspect of the case which we're challenging against the taking.

[0:02:54.920] JUSTICE GINSBURG: But that's what so -- so puzzling because if -- if you're not challenging the volume limit itself, you can't sell more than 60 percent of your crop.

[0:03:05.600] MR. MCCONNELL: That's correct.

[0:03:07.500] JUSTICE GINSBURG: And what

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - June 22, 2015.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2014/14-275
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2014/14-275/14-275_20150622-opinion.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.7 MB)
- Length: 0:06:58.325 (418.325 s)
- Words: 1099, transcribed by faster-whisper `medium.en` with the same settings as the
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
- Cross-check: Oyez's unofficial transcript agrees with 1073 of Whisper's 1099 words (97.6%; Oyez has 1103).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:06:57.660 | 1098 |

### Full text, as plain text

Whisper's wording, the whole announcement, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: I have the opinion of the Court in Case No. 14-275, Horn v. United States Department of Agriculture. At 8 o 'clock one April morning in Fresno County, California, government trucks waited outside the raisin handling facility of the Horns, a family of raisin growers. The trucks were there to pick up over a thousand tons of the Horns' raisin crop, even though the government had not paid for those raisins. The government sought the raisins pursuant to the Agricultural Marketing Agreement Act of 1937. That statute was passed during the Great Depression to help respond to the farming crisis at that time. It authorizes the Secretary of Agriculture to promulgate what are known as marketing orders to help maintain stable markets for certain agricultural products. One of those marketing orders, the California Raisin Marketing Order, requires raisin growers like the Horns to set aside a specified portion of their raisin crop in certain years for the government, free of charge. In 2002, that amount was 47 percent. In 2003, 30 percent. The government uses that portion of a grower's raisin crop, what are known as reserve raisins, in ways it thinks best promote the purposes of the marketing order program, such as by selling them in noncompetitive markets, donating them, or otherwise disposing of them. After deducting the expenses of administering the program, the government returns to the growers any net proceeds left over from the sale of the reserve raisins. In one of the two years at issue in this case, those proceeds were less than the cost of producing the raisins. In the other year, they were no net proceeds at all. Now, when the trucks arrived at the Horns' facility, the Horns refused to hand over the raisins. In response, the government assessed a fine against the Horns equal to the fair market value of the raisins, as well as a civil penalty for disobeying the order. The Horns challenged the fine and penalty in Federal District Court, arguing that the government's program took their raisins for public use without just compensation in violation of the Takings Clause of the Fifth Amendment to the Constitution. The Court of Appeals rejected that argument. The Court acknowledged that the government could not physically take real property land without compensation under the Fifth Amendment. It ruled, however, that personal property, like raisins, was entitled to less protection. There had to be a more complicated analysis to determine whether there had been a taking with respect to personal property, even when the government physically took such property. The Court of Appeals also relied on the fact that growers like the Horns retained the right to any net proceeds from the government's use of the raisins. In the Court's view, if the Horns did not wish to give up a portion of their raisins to the government, they could plant something else. Now, this case raises three questions which we answer in turn. The first question is whether a physical appropriation of real and personal property should be treated the same. The answer is yes. The Takings Clause of the Fifth Amendment provides, quote, nor shall private property be taken for public use without just compensation. That clause makes no distinction between real and personal property. The government has a categorical duty to pay just compensation when it takes your car, just as when it takes your home. That has been the rule from before the beginning. Eight hundred years ago in Magna Carta, King John promised not to take, quote, corn or other provisions from anyone without immediately tendering money therefore. So the earliest predecessor of the Takings Clause applied to personal property. The Founding Fathers at the time of the Revolution knew their rights from Magna Carta and objected, even when their own Continental Army took personal property without just compensation. Nothing in this history suggested that the property was entitled to any less protection than real property. Now, personal property can, of course, be subject to stringent government regulation in appropriate cases. But like real property, it cannot be physically taken for public use without just compensation. The second question is whether the government can argue it has not actually taken the grower's property because when it seizes the raisins, it leaves the growers with a contingent interest in any net proceeds from the sales of the raisins. The answer is no. There has still been a physical taking. When property has been physically appropriated, the government is under a categorical duty to pay just compensation. Physical appropriation is the clearest example of a taking. Any payment made to the property owner goes, at most, to the issue of whether he has received just compensation, not whether there has been a taking in the first place. The Constitution does not allow the government to avoid the requirement of just compensation when it takes your car simply because it promises to return the quarters it finds in the seats. The third question presented in this case is whether the government can require the horns to give up a percentage of their raisins as a condition of being allowed to sell the rest. The answer is no. The government argues that the marketing order imposes reasonable conditions on growers who want to sell raisins. It says that if the horns do not like these conditions, they have alternatives. They can plant different crops or, quoting from the government's brief, sell their raisin variety grapes as table grapes or for use in juice or wine. Now, this let them sell wine response is no more comforting than similar retorts have been to others throughout history. The government can, of course, regulate raisin sales in many ways, but it cannot require growers to waive their right to just compensation in exchange for something as basic as the ability to sell their produce. Some products are dangerous or hazardous, and in such cases, government conditions on selling those products, even up to an appropriation of property, may be justified. But raisins are not hazardous products. In light of our answers to these three questions, we hold that the horns cannot be fined for resisting the government's attempt to take their raisins. The judgment of the court of appeals is accordingly reversed. Justices Scalia, Kennedy, Thomas, and Alito have joined this opinion in full. Justices Ginsburg, Breyer, and Kagan have joined all but Part 3. Justice Breyer has filed an opinion concurring in part and dissenting in part in which Justices Ginsburg and Kagan join. Justice Sotomayor has filed a dissenting opinion.

### Announcement mentions

Every sentence in the announcement (Whisper's wording) that mentions: percentages, dollar amounts, years, raisins, reserve, farmers, Horne/Horn. "Percentages" means any "N percent", "dollar amounts" any "$N" or "N dollars", "years" any year from 1600 to 2099. One row per sentence; the time is where the sentence starts.

| term | sentences |
|---|---|
| percentages | 2 |
| dollar amounts | 0 |
| years | 3 |
| raisins | 16 |
| reserve | 2 |
| farmers | 0 |
| Horne/Horn | 12 |

| time | time (s) | speaker | matches | sentence |
|---|---|---|---|---|
| 0:00:00.000 | 0.000 | CHIEF JUSTICE ROBERTS | Horne/Horn | I have the opinion of the Court in Case No. 14-275, Horn v. United States Department of Agriculture. |
| 0:00:08.500 | 8.500 | CHIEF JUSTICE ROBERTS | Horne/Horn | At 8 o 'clock one April morning in Fresno County, California, government trucks waited outside the raisin handling facility of the Horns, a family of raisin growers. |
| 0:00:19.220 | 19.220 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | The trucks were there to pick up over a thousand tons of the Horns' raisin crop, even though the government had not paid for those raisins. |
| 0:00:26.720 | 26.720 | CHIEF JUSTICE ROBERTS | years, raisins | The government sought the raisins pursuant to the Agricultural Marketing Agreement Act of 1937. |
| 0:00:50.980 | 50.980 | CHIEF JUSTICE ROBERTS | Horne/Horn | One of those marketing orders, the California Raisin Marketing Order, requires raisin growers like the Horns to set aside a specified portion of their raisin crop in certain years for the government, free of charge. |
| 0:01:05.120 | 65.120 | CHIEF JUSTICE ROBERTS | percentages, years | In 2002, that amount was 47 percent. |
| 0:01:08.420 | 68.420 | CHIEF JUSTICE ROBERTS | percentages, years | In 2003, 30 percent. |
| 0:01:11.640 | 71.640 | CHIEF JUSTICE ROBERTS | raisins, reserve | The government uses that portion of a grower's raisin crop, what are known as reserve raisins, in ways it thinks best promote the purposes of the marketing order program, such as by selling them in noncompetitive markets, donating them, or otherwise disposing of them. |
| 0:01:28.620 | 88.620 | CHIEF JUSTICE ROBERTS | raisins, reserve | After deducting the expenses of administering the program, the government returns to the growers any net proceeds left over from the sale of the reserve raisins. |
| 0:01:38.780 | 98.780 | CHIEF JUSTICE ROBERTS | raisins | In one of the two years at issue in this case, those proceeds were less than the cost of producing the raisins. |
| 0:01:49.260 | 109.260 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | Now, when the trucks arrived at the Horns' facility, the Horns refused to hand over the raisins. |
| 0:01:54.140 | 114.140 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | In response, the government assessed a fine against the Horns equal to the fair market value of the raisins, as well as a civil penalty for disobeying the order. |
| 0:02:04.300 | 124.300 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | The Horns challenged the fine and penalty in Federal District Court, arguing that the government's program took their raisins for public use without just compensation in violation of the Takings Clause of the Fifth Amendment to the Constitution. |
| 0:02:30.040 | 150.040 | CHIEF JUSTICE ROBERTS | raisins | It ruled, however, that personal property, like raisins, was entitled to less protection. |
| 0:02:47.860 | 167.860 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | The Court of Appeals also relied on the fact that growers like the Horns retained the right to any net proceeds from the government's use of the raisins. |
| 0:02:56.760 | 176.760 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | In the Court's view, if the Horns did not wish to give up a portion of their raisins to the government, they could plant something else. |
| 0:04:27.520 | 267.520 | CHIEF JUSTICE ROBERTS | raisins | The second question is whether the government can argue it has not actually taken the grower's property because when it seizes the raisins, it leaves the growers with a contingent interest in any net proceeds from the sales of the raisins. |
| 0:05:16.200 | 316.200 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | The third question presented in this case is whether the government can require the horns to give up a percentage of their raisins as a condition of being allowed to sell the rest. |
| 0:05:25.760 | 325.760 | CHIEF JUSTICE ROBERTS | raisins | The answer is no. The government argues that the marketing order imposes reasonable conditions on growers who want to sell raisins. |
| 0:05:33.820 | 333.820 | CHIEF JUSTICE ROBERTS | Horne/Horn | It says that if the horns do not like these conditions, they have alternatives. |
| 0:06:21.340 | 381.340 | CHIEF JUSTICE ROBERTS | raisins | But raisins are not hazardous products. |
| 0:06:24.580 | 384.580 | CHIEF JUSTICE ROBERTS | raisins, Horne/Horn | In light of our answers to these three questions, we hold that the horns cannot be fined for resisting the government's attempt to take their raisins. |

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:02.260 | No. 14 -275, Horn | number 14-275, Horne |
| 0:00:16.820 | Horns, | Horne's, |
| 0:00:22.500 | Horns' | Hornes' |
| 0:00:56.960 | Horns | Hornes |
| 0:01:07.980 | percent. | (nothing) |
| 0:01:10.640 | percent. | (nothing) |
| 0:01:46.420 | (nothing) | -- there were |
| 0:01:50.780 | Horns' | Hornes' |
| 0:01:51.800 | Horns | Hornes |
| 0:01:57.320 | Horns | Hornes, |
| 0:02:04.820 | Horns | Hornes |
| 0:02:51.700 | Horns | Hornes |
| 0:02:58.380 | Horns | Hornes |
| 0:03:40.100 | Eight hundred | 800 |
| 0:04:09.260 | (nothing) | property was entitled to any less protection -- personal |
| 0:05:20.420 | horns | Hornes |
| 0:05:35.160 | horns | Hornes |
| 0:06:28.180 | horns | Horne's |
