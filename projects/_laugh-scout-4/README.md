# Laugh scout 4: the whole archive

Every oral argument transcript on supremecourt.gov from October Term 2005 to October Term 2026 (the three October 2026 arguments posted so far), scanned for laughter with `archive_scan.py`, which uses the same counter as `laugh_scout.py`: every bracketed marker containing "laughter", from "(Laughter.)" to "(A little laughter.)" and "[Laughter.]", inside the argument itself. Transcripts only, no audio.

- Scanned: 1359 transcripts (re-argued cases count once per argument). Not found: 0.
- Left out: 68 telephone arguments from 1 May 2020 to 30 September 2021 (no courtroom, so no room to laugh).
- Transcripts with no laughter at all: 232.
- Raw data: `archive.json` (every transcript with its laughs, setups, minutes and laughs per 10 minutes), `scan.jsonl` (resume log). Regenerate with `python3 archive_scan.py projects/_laugh-scout-4 2005 2026`; a re-run only scans what's missing.

## Calibration

| case | expected | counted |
|---|---|---|
| Yates v. United States, 13-7451 | 15 | 15 |
| POM Wonderful v. Coca-Cola, 12-761 | 2 | 2 |

## Shortlist

`skip.md` lists everything removed first: cases with project folders, cases in earlier scouts, posted topics, and political, harmful or sensitive cases. The top 40 left by laugh count end at 8 laughs, with ten more tied at 8, so all 50 were read. Each laugh was classed by what the room laughed at: the **object** or **situation** (an everyday thing, a ridiculous scenario) or the **process** (procedure, interruptions, banter about the argument or the justices themselves).

Most of the archive's big laugh counts are process: justices teasing each other and the lawyers. Only six of the 50 had a majority of object or situation laughs, with three more at exactly half. So the 7-laugh tier was read too for cases with an everyday object, which added four that pass (Kentucky v. King, Brigham City, Arizona v. Gant, Timbs).

| docket | case | argued | laughs | object/situation | passes |
|---|---|---|---|---|---|
| 24-354 | FCC v. Consumers' Research | 26 Mar 2025 | 16 | 2 |  |
| 08-970 | Perdue v. Kenny A. | 14 Oct 2009 | 14 | 1 |  |
| 17-1471 | Home Depot U. S. A., Inc. v. Jackson | 15 Jan 2019 | 12 | 0 |  |
| 07-11191 | Briscoe v. Virginia | 11 Jan 2010 | 12 | 0 |  |
| 21-1164 | Wilkins v. United States | 30 Nov 2022 | 12 | 0 |  |
| 22-800 | Moore v. United States | 5 Dec 2023 | 12 | 0 |  |
| 09-337 | Krupski v. Costa Crociere, S. p. A. | 21 Apr 2010 | 11 | 5 |  |
| 04-848 | Dolan v. Postal Service | 7 Nov 2005 | 11 | 8 | yes |
| 10-1472 | Taniguchi v. Kan Pacific Saipan, Ltd. | 21 Feb 2012 | 11 | 0 |  |
| 08-1151 | Stop the Beach Renourishment, Inc. v. Florida Dept. of Environmental Protection | 2 Dec 2009 | 11 | 6 | yes |
| 22-166 | Tyler v. Hennepin County | 26 Apr 2023 | 11 | 2 |  |
| 17-1705 | PDR Network, LLC v. Carlton & Harris Chiropractic, Inc. | 25 Mar 2019 | 10 | 6 | yes |
| 22-324 | O’Connor-Ratcliff v. Garnier | 31 Oct 2023 | 10 | 4 |  |
| 09-291 | Thompson v. North American Stainless, LP | 7 Dec 2010 | 9 | 2 |  |
| 12-17 | McBurney v. Young | 20 Feb 2013 | 9 | 0 |  |
| 08-674 | NRG Power Marketing, LLC v. Maine Pub. Util. Comm’n | 3 Nov 2009 | 9 | 0 |  |
| 09-1298 | General Dynamics Corp. v. United States | 18 Jan 2011 | 9 | 0 |  |
| 12-52 | Dan's City Used Cars, Inc. v. Pelkey | 20 Mar 2013 | 9 | 2 |  |
| 09-5201 | Barber v. Thomas | 30 Mar 2010 | 9 | 0 |  |
| 11-45 | Elgin v. Department of Treasury | 27 Feb 2012 | 9 | 1 |  |
| 11-1545 | Arlington v. FCC | 16 Jan 2013 | 9 | 0 |  |
| 11-864 | Comcast Corp. v. Behrend | 5 Nov 2012 | 9 | 0 |  |
| 08-1196 | Weyhrauch v. United States | 8 Dec 2009 | 9 | 0 |  |
| 15-474 | McDonnell v. United States | 27 Apr 2016 | 9 | 4 |  |
| 18-260 | County of Maui v. Hawaii Wildlife Fund | 6 Nov 2019 | 9 | 4 |  |
| 21-1326 | U.S., ex rel. Schutte v. SuperValu Inc. | 18 Apr 2023 | 9 | 0 |  |
| 22-846 | Dept. of Agric. Rural Dev. v. Kirtz | 6 Nov 2023 | 9 | 1 |  |
| 22-1025 | Gonzalez v. Trevino | 20 Mar 2024 | 9 | 1 |  |
| 23-909 | Kousisis v. United States | 9 Dec 2024 | 9 | 0 |  |
| 22-899 | Smith v. Arizona | 10 Jan 2024 | 9 | 1 |  |
| 22-1219 | Relentless, Inc. v. Dept. of Commerce | 17 Jan 2024 | 9 | 0 |  |
| 15-1256 | Nelson v. Colorado | 9 Jan 2017 | 8 | 0 |  |
| 04-1067 | Georgia v. Randolph | 8 Nov 2005 | 8 | 4 | half |
| 13-1421 | Bank of America, N.A. v. Caulkett | 24 Mar 2015 | 8 | 0 |  |
| 04-1739 | Beard v. Banks | 27 Mar 2006 | 8 | 3 |  |
| 18-1269 | Rodriguez v. FDIC | 3 Dec 2019 | 8 | 0 |  |
| 04-805 | Texaco Inc. v. Dagher | 10 Jan 2006 | 8 | 1 |  |
| 12-417 | Sandifer v. United States Steel Corp. | 4 Nov 2013 | 8 | 3 |  |
| 16-1432 | Sveen v. Melin | 19 Mar 2018 | 8 | 4 | half |
| 17-1094 | Nutraceutical Corp. v. Lambert | 27 Nov 2018 | 8 | 2 |  |
| 05-5992 | Zedner v. United States | 18 Apr 2006 | 8 | 1 |  |
| 06-1456 | Regalado Cuellar v. United States | 25 Feb 2008 | 8 | 4 | half |
| 08-1332 | Ontario v. Quon | 19 Apr 2010 | 8 | 6 | yes |
| 18-938 | Ritzen Group, Inc. v. Jackson Masonry, LLC | 13 Nov 2019 | 8 | 0 |  |
| 04-1350 | KSR International Co. v. Teleflex, Inc. | 28 Nov 2006 | 8 | 0 |  |
| 08-661 | American Needle, Inc. v. National Football League | 13 Jan 2010 | 8 | 5 | yes |
| 23-1095 | Thompson v. United States | 14 Jan 2025 | 8 | 1 |  |
| 156-Orig | New York v. New Jersey | 1 Mar 2023 | 8 | 0 |  |
| 23-1002 | Hewitt v. United States | 13 Jan 2025 | 8 | 0 |  |
| 22-859 | SEC v. Jarkesy | 29 Nov 2023 | 8 | 0 |  |
| 09-1272 | Kentucky v. King | 12 Jan 2011 | 7 | 6 | yes |
| 05-502 | Brigham City v. Stuart | 24 Apr 2006 | 7 | 5 | yes |
| 07-542 | Arizona v. Gant | 7 Oct 2008 | 7 | 4 | yes |
| 17-1091 | Timbs v. Indiana | 28 Nov 2018 | 7 | 4 | yes |
| 16-402 | Carpenter v. United States | 29 Nov 2017 | 7 | 2 |  |
| 17-5554 | Stokeling v. United States | 9 Oct 2018 | 7 | 2 |  |
| 05-130 | eBay Inc. v. MercExchange, L.L.C. | 29 Mar 2006 | 7 | 1 |  |
| 14-1280 | Heffernan v. City of Paterson | 19 Jan 2016 | 7 | 0 |  |
| 16-1144 | Marinello v. United States | 6 Dec 2017 | 7 | 0 |  |
| 23-14 | Diaz v. United States | 19 Mar 2024 | 7 | 0 |  |
| 23-367 | Starbucks Corp. v. McKinney | 23 Apr 2024 | 7 | 0 |  |
| 23-677 | Royal Canin U.S.A., Inc. v. Wullschleger | 7 Oct 2024 | 7 | 0 |  |

## Top 10

Ranked by object/situation laughs, then by how everyday the object is and how much the ruling touches the viewer's own life. Number 10 is at exactly half, below the bar; it's the best of the three half cases.

| # | case | docket | argued | laughs | object/situation | everyday object | the story in one line | title-card question |
|---|---|---|---|---|---|---|---|---|
| 1 | Dolan v. Postal Service | 04-848 | 7 Nov 2005 | 11 | 8 | mail left on the porch | A woman trips over mail her carrier left on the porch and sues; the Post Office says the law bars any claim about the mail. | Can you sue if a delivery left on your doorstep trips you up? |
| 2 | Kentucky v. King | 09-1272 | 12 Jan 2011 | 7 | 6 | the front door | Police smell weed at an apartment door, knock, hear movement and kick it in; the man they were chasing was behind the other door. | Can police kick your door in without a warrant? |
| 3 | Ontario v. Quon | 08-1332 | 19 Apr 2010 | 8 | 6 | a work pager | A SWAT sergeant keeps going over the text limit on his city pager, so the city pulls the transcripts and reads them. | Can your boss read your texts? |
| 4 | Stop the Beach Renourishment, Inc. v. Florida Dept. of Environmental Protection | 08-1151 | 2 Dec 2009 | 11 | 6 | the beach | Florida pumps sand onto an eroding beach, and the new strip in front of the houses becomes public. | Who owns the beach in front of your house? |
| 5 | PDR Network, LLC v. Carlton & Harris Chiropractic, Inc. | 17-1705 | 25 Mar 2019 | 10 | 6 | a fax machine | A chiropractor sues over an unsolicited fax offering a free e-book; the justices mostly laugh at the idea of anyone reading the Federal Register. | Is a free offer still junk mail? |
| 6 | Brigham City v. Stuart | 05-502 | 24 Apr 2006 | 7 | 5 | a screen door | Police at a 3 a.m. party see a fight through the screen door and walk in without a warrant. | Can police walk into your party? |
| 7 | American Needle, Inc. v. National Football League | 08-661 | 13 Jan 2010 | 8 | 5 | team caps and T-shirts | A hat maker loses its licence when the 32 NFL teams hand their headwear licensing to one company. | Can rival teams team up on what you pay for merch? |
| 8 | Arizona v. Gant | 07-542 | 7 Oct 2008 | 7 | 4 | a car | Arrested for driving on a suspended licence and locked in the patrol car, Gant watches police search his car. | Can police search your car after they arrest you? |
| 9 | Timbs v. Indiana | 17-1091 | 28 Nov 2018 | 7 | 4 | a Land Rover | Indiana takes a man's $42,000 Land Rover over a crime with a $10,000 maximum fine. | Can the government take your car? |
| 10 | Georgia v. Randolph | 04-1067 | 8 Nov 2005 | 8 | 4 | the front door (again) | A wife invites police in to search; her husband, standing right there, says no. | Can police come in if your housemate says yes? |

## Deep scout and winner

The top 3 are scouted in `deep-scout.md`: story, the one argument mapped to page:line, laughs inside the fight, the sendable ending with the holding, roles and risks.

**Winner: Dolan v. United States Postal Service (04-848)**, transcribed in `projects/dolan-mail/`.

1. The fight has the laughs inside it: the toupee, the skis that mow down pedestrians, the swinging alligator and "go down to the Post Office every time we get packages" all come from the one question of whether mail on a porch is the Post Office's problem.
2. The object is the most everyday thing in the archive: a delivery left on your doorstep.
3. The ending is one you'd send someone: if your post trips you up, you can take the Post Office to court.

supremecourt.gov only hosts argument audio from October Term 2010, so Dolan's argument audio comes from Oyez (the Court's own recording, via the National Archives).
