# ebay-buy-it-now: Supreme Court No. 05-130

Word-timed transcript of the oral argument, for video editing. Wording is the official
transcript's, verbatim; times come from ASR.

## Sources

- Argument page: none on supremecourt.gov for this term
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/05-130/20060329a_05-130.delivery.mp3
  **Not from supremecourt.gov:** the Court's own site has no audio for this argument (its audio pages start with the October 2010 term), so this is Oyez's copy of the Court's recording. The transcript is the Court's own.
- Official transcript: https://www.supremecourt.gov/pdfs/transcripts/2005/05-130.pdf

## Numbers

- ASR model: faster-whisper `small.en`, CPU, int8, `word_timestamps=True`, `vad_filter=False`, beam size 5
- ASR run time: 23 min on 4 CPU cores
- Audio length: 0:59:23.651 (3563.651 s)
- `audio/argument.mp3`: mono, 64 kbps, 28.5 MB
- Official words: 10674 (plus 7 `(Laughter.)` markers), in 158 speaker turns
- ASR words: 10415
- Official words matched to an ASR word: 10063 of 10674 (**94.28%**)

## Sanity checks

- PASS: words in time order. 0 words start before the previous word; 0 words end before they start.
  (0 spread words had to be nudged forward to keep order before this check ran.)
- PASS: no word longer than 3 s except before a laugh. 0 words longer than 3 s outside laugh positions.
- PASS: match rate over 85%. 94.28% (threshold 85%).

340 words are shorter than 20 ms. These are official words the ASR didn't produce,
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
fit between the untouched neighbours and bring the word under 3 s. This fixed 1
words; the window ASR is cached in `work/asr_windows_*.json`. These rules are the only places a
matched word's ASR time changes.

Regenerate with:

    python3 transcribe.py 05-130 2005 ebay-buy-it-now --model small.en --pdf-url https://www.supremecourt.gov/pdfs/transcripts/2005/05-130.pdf --mp3-url https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/05-130/20060329a_05-130.delivery.mp3 --opinion --mentions "troll,Buy It Now,software developer,injunction,bridge"

## The official laughs, measured in the audio

Each `(Laughter.)` in the transcript, at the end of the word before it, with the 30 words before. The room is measured in the pause that follows, up to the next transcribed word: its length, how many seconds are 12 dB or more over the silence floor (-46.5 dBFS, the quietest 5% of the recording), and the mean and peak loudness over that floor. "Big" is at least 1 s loud at a mean of 20 dB or more; "medium" at least 0.4 s loud. "Under speech" means the next word starts within 0.3 s, so any laughter is under someone's voice and can't be measured this way: listen to those.

| # | time | time (s) | size | pause (s) | loud (s) | mean dB over floor | peak dB over floor | 30 words before |
|---|---|---|---|---|---|---|---|---|
| 1 | 0:12:45.740 | 765.740 | under speech | 0.00 | 0.00 | - | - | denying that inventor, you know, the -- what he'd give to Bell Labs -- or whatever Bell Labs is these days -- that does practice the inventions -- I should know that actually, but -- |
| 2 | 0:23:58.620 | 1438.620 | under speech | 0.00 | 0.00 | - | - | around, that you're never entitled to a -- to an injunction. Well, is -- is the troll the scary thing under the bridge, or is it a fishing technique? I -- I want -- |
| 3 | 0:24:03.680 | 1443.680 | under speech | 0.00 | 0.00 | - | - | is the troll the scary thing under the bridge, or is it a fishing technique? I -- I want -- For my clients, it's been the scary thing under the bridge, but -- |
| 4 | 0:34:36.180 | 2076.180 | medium | 0.84 | 0.40 | 19.6 | 27.7 | patent and who is licensing a patent that probably won't be developed very much beyond what it is -- it's fairly easy to -- I'll ask Mr. Waxman. Thank you, Your Honor. |
| 5 | 0:34:46.640 | 2086.640 | under speech | 0.00 | 0.00 | - | - | Thank you, Mr. Minear. Mr. Waxman. Mr. Chief Justice, and may it please the Court: I -- I can anticipate at least one question. Let me just say at the outset -- |
| 6 | 0:49:17.020 | 2957.020 | under speech | 0.00 | 0.00 | - | - | rule 65. But the claim of imprecision here is -- look, I'm not a software developer and I have reason to believe that neither is Your Honor, and I -- I can't -- |
| 7 | 0:49:32.880 | 2972.880 | small | 0.40 | 0.25 | 20.3 | 21.8 | displaying pictures of your wares on a computer network and, you know, picking which ones you want and buying them. I -- I might have been able to do that. Well -- |

## Key mentions

Every sentence in the argument that mentions one of these terms, official wording, with the time of the word and the speaker. Terms match whole words with normal endings (dog, dogs, dog's; knock, knocks, knocking, knocked). A sentence that mentions two terms appears once for each.

| term | sentences | times said |
|---|---|---|
| troll | 8 | 8 |
| Buy It Now | 0 | 0 |
| software developer | 2 | 2 |
| injunction | 65 | 72 |
| bridge | 2 | 2 |

| time | time (s) | speaker | term | sentence |
|---|---|---|---|---|
| 0:01:02.480 | 62.480 | MR. PHILLIPS | injunction | The rule in the Federal Circuit for at least 20 years has been that if you have validity and infringement decided by the jury, that then there is irrebuttable finding of -- of irreparable injury, of inadequate remedy at law, and that the balance of harms decidedly favors the plaintiff, and that the only issue that remains available to the defendant in that circumstance is a heightened scrutiny on the standard of whether or not the -- the public interest commands that an injunction be denied in a particular case. |
| 0:01:31.120 | 91.120 | MR. PHILLIPS | injunction | That -- that is precise -- I think it's the only way to read Judge Bryson's decision, Justice Ginsburg, where the court says, at page 26a, that a permanent injunction will issue once infringement and validity have been adjudged, and then say, to be sure, it will not be so to protect the public interest. |
| 0:01:50.660 | 110.660 | MR. PHILLIPS | injunction | Well, the point is that if an injunction follows with a finding of -- of validity and infringement, then that means that there has to be -- there has to be irreparable injury, inadequate remedy at law, and that the balance of hardships has to tilt in -- in favor of the plaintiff. |
| 0:02:10.320 | 130.320 | MR. PHILLIPS | injunction | And then the only issue that remains is whether or not the public interest justifies not granting an injunction under the circumstances of this case. |
| 0:02:50.720 | 170.720 | MR. PHILLIPS | injunction | Section 283 says explicitly -- and this is at page 1 of the blue brief -- district courts, quote, may -- not shall -- grant injunctions in accordance with principles of equity. |
| 0:05:27.540 | 327.540 | JUSTICE BREYER | injunction | And now would a -- would a court issue an injunction there? |
| 0:06:23.220 | 383.220 | MR. PHILLIPS | injunction | It didn't say, as it could have, that there is presumed -- there's a presumption that we have an injunction. |
| 0:06:29.000 | 389.000 | MR. PHILLIPS | injunction | It didn't say, as it could have, that we shall have a -- shall have either a presumption or an injunction in any particular case. |
| 0:06:51.680 | 411.680 | CHIEF JUSTICE ROBERTS | injunction | You're not suggesting that in a typical run-of-the-mine patent case, no special considerations, it would be wrong to say that in those cases you typically would grant an injunction? |
| 0:08:15.100 | 495.100 | MR. PHILLIPS | injunction | And then you take that finding automatically and you turn it into an injunction. |
| 0:11:35.580 | 695.580 | MR. PHILLIPS | injunction | The -- the district judge didn't just say, I woke up this morning and I felt really good about the defendant, and therefore, I'm not granting an injunction. |
| 0:11:48.580 | 708.580 | CHIEF JUSTICE ROBERTS | injunction | Well, but he said other things too, and one thing he said is, I don't like business method patents very much, and so I'm not going to give an injunction here. |
| 0:12:06.940 | 726.940 | CHIEF JUSTICE ROBERTS | injunction | Is that an appropriate consideration to take into account in determining whether to grant an injunction or not? |
| 0:13:55.560 | 835.560 | JUSTICE KENNEDY | injunction | My concern is if you take that away, I don't know if you've got a lot left for the -- saying no injunction in this case. |
| 0:16:59.520 | 1019.520 | JUSTICE KENNEDY | injunction | Well, but this gives you the advantage of coming in in advance saying, I want -- I -- I want a ruling in advance that I'm not going to violate the injunction. |
| 0:18:33.280 | 1113.280 | MR. PHILLIPS | injunction | And the Court said, under those circumstances, you get an injunction. |
| 0:20:09.960 | 1209.960 | CHIEF JUSTICE ROBERTS | injunction | Why -- why should he lose the leverage of the normal injunction and have substituted for that a duel of experts over what a reasonable royalty should be? |
| 0:22:08.560 | 1328.560 | MR. PHILLIPS | injunction | We'll allow enhanced damages in the interim and even the potential down the road, obviously, of -- of an injunction to serve as enough of a deterrent to protect the right to exclude that the plaintiff has under the statute. |
| 0:22:25.100 | 1345.100 | JUSTICE SCALIA | injunction | I mean, why -- why should I be in better shape, as far as getting an injunction is concerned, if I produce an automobile engine and -- and make some undeterminate profit -- |
| 0:22:52.820 | 1372.820 | JUSTICE SCALIA | injunction | Why -- why does one situation justify an injunction more than the other? |
| 0:23:18.480 | 1398.480 | MR. PHILLIPS | injunction | That's what the injunction is trying to say. |
| 0:23:25.740 | 1405.740 | MR. PHILLIPS | injunction | But if you choose not to occupy it, it's not to say that you abandon your right to an injunction, but that that ought to be a legitimate, individualized consideration, among other considerations -- |
| 0:23:50.960 | 1430.960 | MR. PHILLIPS | troll | Again, it's not -- I'm not looking for a presumption the other way and I'm not looking for categorical rules that say that if you -- if you're a nonperforming entity, that you don't get a license, or even if you're a troll, as that term gets bandied around, that you're never entitled to a -- to an injunction. |
| 0:23:54.520 | 1434.520 | MR. PHILLIPS | injunction | Again, it's not -- I'm not looking for a presumption the other way and I'm not looking for categorical rules that say that if you -- if you're a nonperforming entity, that you don't get a license, or even if you're a troll, as that term gets bandied around, that you're never entitled to a -- to an injunction. |
| 0:23:55.200 | 1435.200 | JUSTICE KENNEDY | troll | Well, is -- is the troll the scary thing under the bridge, or is it a fishing technique? |
| 0:23:56.580 | 1436.580 | JUSTICE KENNEDY | bridge | Well, is -- is the troll the scary thing under the bridge, or is it a fishing technique? |
| 0:24:03.100 | 1443.100 | MR. PHILLIPS | bridge | For my clients, it's been the scary thing under the bridge, but -- |
| 0:24:05.260 | 1445.260 | JUSTICE KENNEDY | troll | I mean, is that what the troll is? |
| 0:24:13.900 | 1453.900 | MR. PHILLIPS | troll | Yes, I believe that's the -- I think that's what -- what it is, although you -- maybe we should think of it more as Orks, now that we have a new generation, but at this point troll is the word that gets -- that gets used. |
| 0:24:46.380 | 1486.380 | MR. MINEAR | injunction | And the United States further submits the patentee's right to an injunction should be covered by the familiar four-factor test this Court has applied in cases such as Weinberger v. Romero-Barcelo. |
| 0:26:30.240 | 1590.240 | CHIEF JUSTICE ROBERTS | injunction | What if by the time you get to the injunction stage, the -- the patent office has, you know, rejected all of the underlying claims in a preliminary way? |
| 0:26:44.680 | 1604.680 | CHIEF JUSTICE ROBERTS | injunction | Can the district court take that into account in deciding not to issue an injunction? |
| 0:27:39.560 | 1659.560 | CHIEF JUSTICE ROBERTS | injunction | Footnote 27 says that's a basis for staying the injunction. |
| 0:27:42.040 | 1662.040 | CHIEF JUSTICE ROBERTS | injunction | It seems to me if it's a basis for staying the injunction, it's a basis not to issue one in the first place. |
| 0:27:48.420 | 1668.420 | MR. MINEAR | injunction | Well, it also might be a -- a basis in terms of how to structure the injunction. |
| 0:29:39.620 | 1779.620 | MR. MINEAR | injunction | And that is why, as Judge Easterbrook noted in the Catheter case, the injunction harnesses the market to determine what the market value of that patent is. |
| 0:30:26.660 | 1826.660 | JUSTICE SCALIA | injunction | They're just talking about, you know, the -- the past actions should -- should be compensable by damages and not -- they should not be subjected to a very threatening injunction. |
| 0:31:05.800 | 1865.800 | MR. MINEAR | injunction | We are suggesting what Justice Kennedy suggested; namely, that the injunction proceedings provide an opportunity to determine whether or not the supposed work-around that eBay has will work or will not, and the injunction will be structured to allow it or not, depending on whether or not it's determined to be infringing. |
| 0:31:29.640 | 1889.640 | MR. MINEAR | injunction | But our view is that by issuing the injunction, the district court, in the proceedings leading up to the injunction, can determine whether or not this work-around is valid or not. |
| 0:31:38.680 | 1898.680 | JUSTICE KENNEDY | injunction | Is there a classic case where the injunction should not be issued? |
| 0:32:02.880 | 1922.880 | MR. MINEAR | injunction | In the case of a nonwillful infringer, for instance, that has made good faith investments that might be set aside by the -- by an injunction, there might be grounds in those circumstances not to issue an injunction. |
| 0:32:10.160 | 1930.160 | MR. MINEAR | injunction | If the injunction would threaten national security, public health and safety, undermine core aspects of commerce -- |
| 0:32:26.680 | 1946.680 | MR. MINEAR | injunction | Well, business processes are not -- the district court clearly erred here in saying that the mere debate about business process patents is a reason for withholding injunctions. |
| 0:32:35.460 | 1955.460 | MR. MINEAR | injunction | That simply is not a sufficient view -- reason in our mind for weighing against the general public interest and the enforceability of patents and the use of injunctions to make sure that those property rights are secure. |
| 0:32:45.640 | 1965.640 | CHIEF JUSTICE ROBERTS | injunction | You're devaluing the value of a particular patent by denying the injunction simply because the people who infringed it weren't willful, and I wonder why that makes sense. |
| 0:35:10.480 | 2110.480 | MR. WAXMAN | injunction | -- that long, perhaps centuries, before Justice Story ever wrote his commentaries on equity, it has been firmly, unequivocally established that a final judgment, not -- we're not talking about an interlocutory order, but a final judgment of patent infringement yields an injunction in all but the very rare case. |
| 0:36:15.900 | 2175.900 | MR. WAXMAN | injunction | And under traditional equity principles, a showing of either of those things, either irreparable injury or a continuing harm, warrants an injunction in the owner's favor unless the offending party can marshal very strong equities otherwise. |
| 0:38:12.280 | 2292.280 | CHIEF JUSTICE ROBERTS | injunction | Is that a factor that a district court could take into account in deciding whether to issue an injunction? |
| 0:38:13.880 | 2293.880 | CHIEF JUSTICE ROBERTS | injunction | Say the injunction question came up right now, today. |
| 0:39:08.740 | 2348.740 | MR. WAXMAN | injunction | It then comes running in and a rule that would allow a district judge now to give notice of that in denying an injunction would basically be a -- an open invitation for everybody to go ahead and try and win at trial, go through the whole multi year process, and if you don't, just put it into reexam. |
| 0:39:52.180 | 2392.180 | MR. WAXMAN | injunction | So we think, in the circumstances of this case, where the district judge had no reason to consider reexam because eBay hadn't invoked reexam at the time, it would be an abuse of discretion for the court to either refuse an injunction or stay it in light of the fact that it's now proceeding. |
| 0:40:59.820 | 2459.820 | JUSTICE BREYER | injunction | Now, couple that with a client or a patentee who also waits for a long time, waits till the invention is embedded in a series of other inventions so that if, in fact, there's an injunction, what will happen is that the patentee will be able to extract far more than this particular invention is worth because the infringer would have to give up the entire invention. |
| 0:41:52.320 | 2512.320 | JUSTICE BREYER | troll | The main point -- what I was trying to do is I was trying to take what I'd call the patent troll case. |
| 0:41:56.240 | 2516.240 | MR. WAXMAN | troll | First of all, this is no patent troll. |
| 0:43:38.820 | 2618.820 | MR. WAXMAN | injunction | The district court decision in this case is the first case in the context of a permanent injunction. |
| 0:43:41.580 | 2621.580 | MR. WAXMAN | injunction | And I'll explain why preliminary injunctions that seek to preserve the status quo are different. |
| 0:43:46.180 | 2626.180 | MR. WAXMAN | injunction | This is the first permanent injunction case I'm aware of that has ever thought that exploiting the patent by licensing it to others to make use of would in -- somehow be costly or disable you from obtaining the relief that section 283 and the -- and tradition provided. |
| 0:44:39.040 | 2679.040 | MR. WAXMAN | injunction | And unless there is an instance in which the patent has expired, the -- the infringer is out of business and can show that it couldn't possibly infringe anymore, an injunction issues to prevent further violation. |
| 0:45:12.840 | 2712.840 | JUSTICE BREYER | injunction | So if you have a case where, on the one hand, it's easier to calculate the damage remedy, and at the same time you fear that to issue an injunction will produce a harm to the other side way out of proportion to, in fact, the value that's being lost by infringing on the patent, then those are two things you'd put in the balance. |
| 0:45:58.080 | 2758.080 | MR. WAXMAN | troll | Professor Lemley testified under oath to Congress that, even though there are problems with patent trolls, in the case of a willful infringer, the law -- equity doesn't balance private harms. |
| 0:47:51.580 | 2871.580 | MR. WAXMAN | injunction | There is no doubt that -- that MercExchange will not be able to start getting patent royalties from AutoTrader unless and until it obtains this injunction. |
| 0:47:57.840 | 2877.840 | CHIEF JUSTICE ROBERTS | troll | Mr. Waxman, you mentioned, in -- in responding to the suggestion that we're dealing with a troll, you described -- what exactly is the invention here? |
| 0:48:37.120 | 2917.120 | CHIEF JUSTICE ROBERTS | injunction | And so isn't that a factor the district court can take into account in deciding whether to issue an injunction because it's going to be hard to issue an injunction to define exactly when it's going to be violated and when it's not? |
| 0:48:49.720 | 2929.720 | MR. WAXMAN | injunction | Well, Mr. Chief Justice, if it turns out that it's too hard and -- and the -- and a specific injunction can't be written, rule 65(d) requires that an injunction not issue. |
| 0:49:01.900 | 2941.900 | MR. WAXMAN | injunction | And in fact, as we've cited in pages 17 and 18 and, I think, 19 of our brief, the Federal Circuit has, in fact, overruled injunctions that were insufficiently precise to satisfy rule 65. |
| 0:49:10.660 | 2950.660 | MR. WAXMAN | software developer | But the claim of imprecision here is -- look, I'm not a software developer and I have reason to believe that neither is Your Honor, and I -- I can't -- |
| 0:49:22.140 | 2962.140 | CHIEF JUSTICE ROBERTS | software developer | I may not be a software developer, but as I read the invention, it's displaying pictures of your wares on a computer network and, you know, picking which ones you want and buying them. |
| 0:51:18.540 | 3078.540 | MR. WAXMAN | injunction | And we certainly agree with the United States that when -- if the judgment is affirmed, the case will go back and the district court will then have to address a point it hasn't addressed yet, which is is the -- is the -- the permanent injunction proposed by MercExchange adequate or inadequate and how can it be made specific, and this supposed work-around -- does it or doesn't it violate the terms of the injunction. |
| 0:52:25.180 | 3145.180 | JUSTICE STEVENS | injunction | What kind of -- what do these injunctions say? |
| 0:53:08.180 | 3188.180 | JUSTICE STEVENS | injunction | But it seems to me a great difference might turn on what exactly the injunction provided. |
| 0:53:09.900 | 3189.900 | JUSTICE STEVENS | injunction | Some injunctions must be -- might be much more burdensome than some others. |
| 0:53:17.740 | 3197.740 | MR. WAXMAN | injunction | And the terms of an injunction are appealable, and the Federal Circuit has reviewed actual terms of permanent injunctions and reversed a number of them and said this is -- this doesn't satisfy rule 65 or it doesn't meet other requirements. |
| 0:54:27.240 | 3267.240 | JUSTICE STEVENS | injunction | Is the draft of the injunction that you want in the record? |
| 0:54:53.580 | 3293.580 | MR. WAXMAN | injunction | But it certainly will have to be changed because the court of appeals invalidated the '176 patent, which the jury found had been infringed, and therefore, it's -- it will need to be revisited when the case goes back for the entry of an injunction. |
| 0:55:16.440 | 3316.440 | MR. PHILLIPS | injunction | That's the proposed permanent injunction, and I won't purport to read the whole thing, but it starts off with anything directly or indirectly, and it goes on for three pages. |
| 0:55:27.980 | 3327.980 | MR. PHILLIPS | injunction | It is, I think, fairly characterized as a very broad injunction. |
| 0:58:06.380 | 3486.380 | MR. PHILLIPS | injunction | And what he did in this case was to go through each of the findings of the district court with respect to the use of the -- of the licensing arrangements, the failure to commercialize this, not being in the business, and said, does any of these rise to the level of the kind of public interest concern that is the only legitimate consideration this court will use in deciding whether or not the district court can justify not granting an injunction in a particular case, instead of what is clearly the traditional approach of equity, which is to say, look at the -- the primary two issues, you know, the flip side of the same thing, so I'll just treat it the one way. |

## Petitioner's opening, first 3 minutes

Everything said from 0:00:06.580 to 0:03:06.580, official wording, with each turn's start time. Interruptions from the bench are included.

[0:00:06.580] MR. PHILLIPS: Thank you, Mr. Chief Justice, and may it please the Court: The fundamental question that's posed in this particular case is whether or not the court of appeals by adopting a rule that declares categorically that three out of the four traditional factors for deciding whether or not to grant permanent injunctive relief will be irrebuttably presumed to be satisfied whenever a jury has found that a patent is valid and has been infringed. The rule in the Federal Circuit for at least 20 years has been that if you have validity and infringement decided by the jury, that then there is irrebuttable finding of -- of irreparable injury, of inadequate remedy at law, and that the balance of harms decidedly favors the plaintiff, and that the only issue that remains available to the defendant in that circumstance is a heightened scrutiny on the standard of whether or not the -- the public interest commands that an injunction be denied in a particular case. And even in that context, the Federal Circuit's rule is extraordinarily stringent because not just any public interest can -- will satisfy, but instead, it has to be a public interest that endangers the public health.

[0:01:16.620] JUSTICE GINSBURG: Is that all in Judge Bryson's decision? I certainly didn't see it there.

[0:01:22.160] MR. PHILLIPS: That -- that is precise -- I think it's the only way to read Judge Bryson's decision, Justice Ginsburg, where the court says, at page 26a, that a permanent injunction will issue once infringement and validity have been adjudged, and then say, to be sure, it will not be so to protect the public interest. And we all know the traditional rule with respect to the grant of injunctive relief is that it's a four-factor test.

[0:01:46.360] JUSTICE GINSBURG: I didn't see anything about irrebuttable presumption.

[0:01:49.440] MR. PHILLIPS: Well, the point is that if an injunction follows with a finding of -- of validity and infringement, then that means that there has to be -- there has to be irreparable injury, inadequate remedy at law, and that the balance of hardships has to tilt in -- in favor of the plaintiff. And then the only issue that remains is whether or not the public interest justifies not granting an injunction under the circumstances of this case. It seems to me there's no other way to read that. And if you read it in the context of the -- of the previous 20 years of decisions from the Federal Circuit, it is absolutely clear. We don't have the opportunity to come back as a defendant in an infringement action and say, Your Honor, in the specific facts of this case, this is someone for whom money damages is a completely adequate remedy. And -- and it seems to me quite clear that section 283 is designed to be exactly the opposite of the way the Federal Circuit has interpreted this -- this scheme. Section 283 says explicitly -- and this is at page 1 of the blue brief -- district courts, quote, may -- not shall -- grant injunctions in accordance with principles of equity. And principles of equity, as Justice Story said almost 200 years ago, systematically reject the idea that you will act on a categorical basis in deciding whether or not to grant or withdraw the

## Opinion announcement

The justice reading the decision from the bench, Opinion Announcement - May 15, 2006.

- Source: this recording comes from Oyez (oyez.org), not from the Supreme Court's own website,
  which publishes argument audio but not opinion announcements. The argument audio above is the
  Court's own.
- Oyez page: https://www.oyez.org/cases/2005/05-130
- Audio: https://s3.amazonaws.com/oyez.case-media.mp3/case_data/2005/05-130/20060515o_05-130.delivery.mp3 (saved unchanged as `audio/opinion.mp3`: 1.1 MB)
- Length: 0:04:22.139 (262.139 s)
- Words: 547, transcribed by faster-whisper `small.en` with the same settings as the
  argument. **There is no official transcript, so the wording is Whisper's.** The only check
  is against Oyez's unofficial transcript (below). Expect the odd misheard word, especially
  names and citations.
- Speakers: from the turn boundaries in Oyez's own transcript (2 turns), each
  boundary moved to the longest pause within 1.5 s of it that follows the end of a sentence
  (or the longest pause, if none does). Oyez's wording is not
  used, except where noted below.
- Word times: Whisper's, with the same stretched-word trimming as the argument (1
  trimmed, 0 re-transcribed).
- Skipped speech: none (no gap of 5 s or more with speech in it).
- Checks: 0 words out of time order; words longer than 3 s: none.
- Cross-check: Oyez's unofficial transcript agrees with 511 of Whisper's 547 words (93.4%; Oyez has 532).

Files: `opinion_words.json` (`{"w", "s", "e", "speaker"}`) and `opinion_lines.json`
(`{"speaker", "s", "e", "text"}`, one entry per speaker turn).

| speaker | start | end | words |
|---|---|---|---|
| CHIEF JUSTICE ROBERTS | 0:00:00.000 | 0:00:07.740 | 14 |
| JUSTICE THOMAS | 0:00:09.000 | 0:04:20.940 | 531 |

### First 3 minutes, as plain text

Whisper's wording, 0:00:00.000 to 0:03:00.000, with each speaker's start time.

[0:00:00.000] CHIEF JUSTICE ROBERTS: The opinion, Justice Thomas, has the opinion in 05-130, eBay Inc. vs. Merck Exchange.

[0:00:09.000] JUSTICE THOMAS: This case comes to us on a writ of certiorari to the United States Court of Appeals for the Federal Circuit. Petitioners eBay and Half .com operate Internet websites that allow private sellers to list goods that they wish to sell. Respondent Merck Exchange holds a business method patent for an electronic market designed to facilitate the sale of goods between private individuals. Merck Exchange sought to license its patent to eBay and Half .com, but the parties failed to reach an agreement. As a result, Merck Exchange filed a patent infringement suit against eBay and Half .com in the United States District Court for the Eastern District of Virginia. A jury found that Merck Exchange's patent was valid, that eBay and Half .com had infringed that patent, and that an award of damages was appropriate. The district court then denied Merck Exchange's motion for permanent injunction relief. The Court of Appeals for the Federal Circuit reversed, applying its general rule that a permanent injunction should issue upon a finding of patent infringement absent exceptional circumstances. We granted certiorari to determine the appropriateness of this general rule. In our opinion filed with the clerk today, we vacate the judgment of the Court of Appeals. Ordinarily, a Federal court considering whether to award permanent injunctive relief to a prevailing plaintiff applies the four-factor test historically employed by courts of equity. A plaintiff must demonstrate, one, that it has suffered an irreparable injury. Two, that remedies available at law, such as monetary damages, are inadequate to compensate for that injury. Three, that considering the balance of hardships between the plaintiff and defendant, a remedy in equity is warranted, and four, that the public interest would not be deserved by a permanent injunction. The decision to grant or deny permanent injunctive relief is an act of equitable discretion by the district court, reviewable on appeal for abuse of discretion. We conclude that these familiar principles apply with equal force to disputes arising under the Patent Act. Nothing in the Patent Act indicates that Congress intended to depart from the long tradition of equity practice. To the contrary, the Patent Act expressly provides that injunctions

### Words Whisper invented

None found.

### Where Whisper and Oyez disagree

Whisper's wording is what's in the files. Check these by ear; Oyez is not always right either ("--" there often marks a repeat Oyez left out). Spelling and formatting differences ("video games"/"videogames", hyphens, spoken "quote" and "close quote") are not listed.

| time | Whisper | Oyez |
|---|---|---|
| 0:00:00.000 | The opinion, | (nothing) |
| 0:00:05.520 | Inc. vs. Merck Exchange. | Incorporated, v. MercExchange. |
| 0:00:26.920 | Merck Exchange | MercExchange |
| 0:00:37.980 | Merck Exchange | MercExchange |
| 0:00:48.320 | Merck Exchange | MercExchange |
| 0:01:00.440 | Merck Exchange's | MercExchange’s |
| 0:01:14.060 | Merck Exchange's | MercExchange’s |
| 0:01:40.300 | our | an |
| 0:02:24.220 | deserved | disserved |
| 0:03:15.520 | (nothing) | a |
| 0:03:56.940 | and | in |
| 0:04:11.480 | Ginsburg. | Ginsberg. |
