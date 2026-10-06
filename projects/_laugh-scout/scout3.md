# Laugh scout 3: object and situation laughs

Official oral-argument transcripts from supremecourt.gov, every "(Laughter.)" counted by `laugh_scout.py` (no audio). Each laugh is classed by what the room laughed at: **O** the object at the centre of the case, **S** the everyday situation, **P** the lawyers' or justices' process (interruptions, procedure, banter about the argument itself). Raw output: `scout3.json`; inputs: `scout3-cases.json`.

## Calibration

| case | docket | argued | expected | counted |
|---|---|---|---|---|
| Yates v. United States | 13-7451 | 5 Nov 2014 | 15 | 15 |
| POM Wonderful LLC v. Coca-Cola Co. | 12-761 | 21 Apr 2014 | 2 | 2 |

Both match, so the counts below are on the same footing as the earlier scouts.

## Ranking by object and situation laughs

| rank | case | docket | argued | O/S laughs | all laughs | minutes |
|---|---|---|---|---|---|---|
| 1 | Collins v. Virginia | 16-1027 | 9 Jan 2018 | 5 | 5 | 55 |
| 2 | Hiibel v. Sixth Judicial District Court of Nevada | 03-5554 | 22 Mar 2004 | 4 | 5 | 61 |
| 3 | Byrd v. United States | 16-1371 | 9 Jan 2018 | 3 | 6 | 62 |
| 4 | Riley v. California | 13-132 | 29 Apr 2014 | 1 | 2 | 59 |
| 5 | Impression Products, Inc. v. Lexmark International, Inc. | 15-1189 | 21 Mar 2017 | 1 | 2 | 62 |
| 6 | Medical Marijuana, Inc. v. Horn | 23-365 | 15 Oct 2024 | 0 | 1 | 68 |

Collins v. Virginia is the only case with 5 or more object/situation laughs (all 5 of its laughs are). Hiibel has 4, plus a borderline fifth about Fifth Amendment doctrine that's counted as process. Its 2004 transcript also labels every justice "QUESTION", so speakers would need Oyez to name them.

## Collins v. Virginia

Docket 16-1027, argued 9 Jan 2018, 55 minutes (11:08 a.m. to 12:03 p.m.), **5 laughs**, 5 object/situation. Transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/16-1027_p4k8.pdf

| # | page:line | speaker | setup line (the words just before the laugh) | class | what the room laughed at |
|---|---|---|---|---|---|
| 1 | 18:2 | JUSTICE GINSBURG | Here we're told that there was a close relationship between the defendant and the homeowner. But suppose there weren't that close relationship. Suppose it was a brand new girlfriend and he never stayed overnight, he was hopeful, but he hadn't. | S | whose driveway it is: a brand-new girlfriend, "he was hopeful, but he hadn't" |
| 2 | 24:1 | JUSTICE BREYER | No, I know that, but I'm saying if he'd had access to it. If they'd said please come to my curtilage. All right? | S | the officer and the tarp: "If they'd said please come to my curtilage" |
| 3 | 37:25 | MR. COX | -- Your Honor, for a lot of residential purposes. They might have storage out there, an extra refrigerator. Somebody might be living out there, if the teenager gets too rambunctious, put them out in the garage. | O | the garage as a place to put a rambunctious teenager |
| 4 | 39:12 | JUSTICE BREYER | Okay. So, fine. Okay. Now, the other Hornbook principle is it's not The Thinker, it's a wisp, a wispy bit of very suspicious drug smoke. | O | Breyer's hypotheticals: not a 2,000-lb statue (The Thinker) but "a wispy bit of very suspicious drug smoke" |
| 5 | 53:25 | CHIEF JUSTICE ROBERTS | automobile in the house, which is not, you know, Jay Leno's house, right, where he's got dozens of rare cars or -- or the Porsche in Ferris Bueller. I mean, you -- you're saying that you -- you don't -- | O | cars in the house: Jay Leno's collection, the Porsche in Ferris Bueller |

## Hiibel v. Sixth Judicial District Court of Nevada

Docket 03-5554, argued 22 Mar 2004, 61 minutes (11:03 a.m. to 12:04 p.m.), **5 laughs**, 4 object/situation. Transcript: https://www.supremecourt.gov/pdfs/transcripts/2003/03-5554.pdf

| # | page:line | speaker | setup line (the words just before the laugh) | class | what the room laughed at |
|---|---|---|---|---|---|
| 1 | 16:21 | QUESTION | It's possible but unlikely. | S | loitering by a jewelry store: buying jewelry for a paramour so the wife won't know, "possible but unlikely" |
| 2 | 32:8 | QUESTION | and he said he's a bad guy because he robbed a lot of jewelry stores under these same circumstances. I mean, you could play with hypotheticals, it seems to me. He has robbed this same jewelry store 10 previous times. | S | a suspect who has robbed the same jewelry store 10 times before |
| 3 | 34:12 | QUESTION | Then why complicate the matter? That is, you've already said a name doesn't normally incriminate you, but it could. Suppose his name is Killer Magee. I don't know. | S | giving your name: "Suppose his name is Killer Magee" |
| 4 | 43:22 | QUESTION | answer -- he can be arrested if he just says I won't answer, but if he says I won't answer on the ground that it might tend to incriminate me, then the policeman would probably have probable cause. Wouldn't he? | P | the Fifth Amendment paradox: saying why you won't answer gives probable cause (doctrine; borderline) |
| 5 | 46:23 | QUESTION | We certainly wouldn't want to encourage that kind of activity, would we? | S | a justice who has been questioned by officers without being told to spread their legs and get frisked |

## Byrd v. United States

Docket 16-1371, argued 9 Jan 2018, 62 minutes (10:04 a.m. to 11:06 a.m.), **6 laughs**, 3 object/situation. Transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2017/16-1371_l6hc.pdf

| # | page:line | speaker | setup line (the words just before the laugh) | class | what the room laughed at |
|---|---|---|---|---|---|
| 1 | 16:17 | JUSTICE ALITO | What about this: A homeowner is going away for a long weekend, arranges with a teenager in the neighborhood to come in and walk and feed the cat and spend quality time with the cat -- | S | Alito's house-sitter hypothetical: a teenager paid to feed the cat "and spend quality time with the cat" |
| 2 | 22:6 | JUSTICE GINSBURG | You're here because you lost below. | P | Ginsburg to the lawyer: "You're here because you lost below" |
| 3 | 36:5 | JUSTICE SOTOMAYOR | the police here said we stopped him because he was driving a rental car. He was doing something totally illegal. Every driving school teaches you to put your hands at a 10 to 2 angle, and they found that suspicious. | S | stopped for driving a rental car, hands suspiciously at 10 and 2 |
| 4 | 40:25 | CHIEF JUSTICE ROBERTS | Well, but this is probably not the only time it's ever happened. And -- | S | lending a rental car to someone not on the agreement: "probably not the only time it's ever happened" |
| 5 | 61:13 | JUSTICE SOTOMAYOR | I know you don't, but I -- I -- | P | Sotomayor and the government lawyer talking over each other |
| 6 | 64:20 | MR. FEIGIN | Okay. | P | the lawyer's "Okay" after Gorsuch says answer straight away |

## Riley v. California

Docket 13-132, argued 29 Apr 2014, 59 minutes (10:34 a.m. to 11:33 a.m.), **2 laughs**, 1 object/situation. Transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2013/13-132_bp7c.pdf

| # | page:line | speaker | setup line (the words just before the laugh) | class | what the room laughed at |
|---|---|---|---|---|---|
| 1 | 24:10 | MR. FISHER | Okay. | P | the lawyer's "Okay" after the Chief says "I'm going to say something first" |
| 2 | 32:1 | JUSTICE KAGAN | to suggest to you is that you call it marginal, but, in fact, most people now do carry their lives on cell phones, and that will only grow every single year as, you know, young people take over the world. | O | phones: people carry their lives on them, "as young people take over the world" |

## Impression Products, Inc. v. Lexmark International, Inc.

Docket 15-1189, argued 21 Mar 2017, 62 minutes (11:21 a.m. to 12:23 p.m.), **2 laughs**, 1 object/situation. Transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2016/15-1189_6468.pdf

| # | page:line | speaker | setup line (the words just before the laugh) | class | what the room laughed at |
|---|---|---|---|---|---|
| 1 | 25:17 | JUSTICE KENNEDY | -- "Do not sell"? This would be a great boom to the sticker business, right? | O | a "Do not sell" sticker on cartridges: "a great boom to the sticker business" |
| 2 | 34:23 | MR. TRELA | Well, that's your prerogative, of course. | P | the lawyer to Breyer: interrupting is "your prerogative, of course" |

## Medical Marijuana, Inc. v. Horn

Docket 23-365, argued 15 Oct 2024, 68 minutes (10:06 a.m. to 11:14 a.m.), **1 laughs**, 0 object/situation. Transcript: https://www.supremecourt.gov/oral_arguments/argument_transcripts/2024/23-365_3307.pdf

| # | page:line | speaker | setup line (the words just before the laugh) | class | what the room laughed at |
|---|---|---|---|---|---|
| 1 | 30:16 | JUSTICE GORSUCH | I know. I know. | P | Gorsuch looked up the Areeda-Hovenkamp treatise; Blatt: "Oh, dear" |
