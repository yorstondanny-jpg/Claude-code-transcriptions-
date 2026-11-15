# Senate Judiciary Committee hearing on card swipe fees, 19 Nov 2024 (five stretches)

## Source and rights

- Hearing: US Senate Committee on the Judiciary, "Breaking the Visa-Mastercard Duopoly: Bringing Competition and Lower Fees to the Credit Card System", 19 November 2024, Dirksen 226. Page: https://www.judiciary.senate.gov/committee-activity/hearings/breaking-the-visa-mastercard-duopoly-bringing-competition-and-lower-fees-to-the-credit-card-system
- Recording: the committee's own stream, https://www-senate-gov-media-srs.akamaized.net/hls/live/2036788/judiciary/judiciary111924/master.m3u8 (2:03:05 long; the hearing starts at about 0:14:00).
- Rights: clear (federal). A congressional committee's own recording of a public hearing.

## This clip is five stretches of the hearing, joined with 1.5 s of silence between them

Times in words.json and lines.json are on the CLIP's clock. Add the offset to get the time in the committee's recording (read from the start with ffmpeg; a seek with -ss on the stream lands about 12 s later).

| Stretch | Clip start | Clip end | Hearing start | Offset to add |
|---|---|---|---|---|
| Prof. Alford's opening ($1,100 a year) | 0.0 | 38.0 | 0:46:00 (2760 s) | 2760.0 |
| Sen. Durbin, then Sen. Graham | 39.5 | 634.5 | 0:57:35 (3455 s) | 3415.5 |
| Sen. Kennedy | 636.0 | 926.0 | 1:25:10 (5110 s) | 4474.0 |
| Sen. Welch | 927.5 | 1092.5 | 1:43:25 (6205 s) | 5277.5 |
| Sen. Hawley | 1094.0 | 1139.0 | 1:51:43 (6703 s) | 5609.0 |

## Speakers

Labelled by hand from the words and checked against frames of the committee's video for the Welch stretch (Ms. Kirkpatrick answers "I don't have the information" and "I would welcome the opportunity"). Witnesses: Bill Sheedy (senior adviser to Visa's CEO), Linda Kirkpatrick (Mastercard, President, Americas), Prof. Roger Alford (Notre Dame), Doug Kantor (National Association of Convenience Stores), Chris Callahan (bookshop owner, not heard here).
Not sure, check by ear and on the video before use: who says "Correct." at 494.4 (labelled Graham); "Senator, we share your values" at 1074 (labelled Sheedy); the short "Yes." answers in the Welch stretch; the fast back and forth at 345 to 466.
Machine transcript, no official wording: "Mr. Shih" at 471 is "Mr. Sheedy"; "pension for regulation" at 877 is "penchant"; "$1 ,100" is "$1,100". Words that straddle a join (0 to 0.5 s and the first word after each silence) are not reliable.

## Transcription

- Clip: whole file, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 9.11 MB).
- Length: 0:18:59.043 (1139.0 s).
- Words: 2644. Lines: 181.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 9; words over 3 s re-timed from a window re-run: 0.
- Match rate: 95.92%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (2638 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | FAIL | 1 words longer than 3 s; "and" 0:13:10.500 to 0:13:14.140 |
| match rate | PASS | 95.92% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py swipe-fees-senate "/home/user/pending-review-pipeline/work/swipe-fees/audio/clip.wav" --speakers "0.00=PROF. ALFORD,39.63=SEN. DURBIN,140.61=MR. SHEEDY,200.73=SEN. DURBIN,211.73=MR. SHEEDY,216.85=SEN. DURBIN,230.45=MR. SHEEDY,239.19=SEN. DURBIN,265.89=MR. SHEEDY,285.95=SEN. DURBIN,317.41=SEN. GRAHAM,337.23=MR. SHEEDY,338.37=SEN. GRAHAM,345.87=MR. KANTOR,346.83=SEN. GRAHAM,357.19=MR. KANTOR,359.73=SEN. GRAHAM,364.21=MR. KANTOR,378.33=SEN. GRAHAM,380.03=MR. KANTOR,382.43=SEN. GRAHAM,397.91=PROF. ALFORD,403.41=SEN. GRAHAM,411.41=PROF. ALFORD,412.91=SEN. GRAHAM,417.85=PROF. ALFORD,419.53=SEN. GRAHAM,423.15=PROF. ALFORD,424.25=SEN. GRAHAM,426.79=PROF. ALFORD,429.61=SEN. GRAHAM,432.83=MR. KANTOR,435.19=SEN. GRAHAM,439.53=MR. KANTOR,445.59=SEN. GRAHAM,446.41=MR. KANTOR,447.95=SEN. GRAHAM,452.85=MR. KANTOR,457.31=SEN. GRAHAM,466.49=PROF. ALFORD,470.09=SEN. GRAHAM,476.73=MR. SHEEDY,479.09=SEN. GRAHAM,482.03=MR. SHEEDY,485.97=SEN. GRAHAM,492.77=MR. SHEEDY,494.33=SEN. GRAHAM,498.13=MR. SHEEDY,505.35=SEN. GRAHAM,513.09=MR. SHEEDY,513.69=SEN. GRAHAM,543.45=MS. KIRKPATRICK,546.77=SEN. GRAHAM,547.67=MS. KIRKPATRICK,555.39=SEN. GRAHAM,559.47=MS. KIRKPATRICK,564.25=SEN. GRAHAM,569.83=MR. KANTOR,576.37=SEN. GRAHAM,579.09=MS. KIRKPATRICK,582.79=SEN. GRAHAM,585.99=MS. KIRKPATRICK,588.61=SEN. GRAHAM,593.01=MS. KIRKPATRICK,594.39=SEN. GRAHAM,632.59=THE CHAIR,635.93=THE CHAIR,640.43=SEN. KENNEDY,656.91=MR. SHEEDY,660.59=SEN. KENNEDY,667.35=MR. SHEEDY,677.11=SEN. KENNEDY,680.87=MR. SHEEDY,685.61=SEN. KENNEDY,692.11=MR. SHEEDY,696.37=SEN. KENNEDY,734.01=PROF. ALFORD,738.93=SEN. KENNEDY,747.19=PROF. ALFORD,750.61=SEN. KENNEDY,752.93=PROF. ALFORD,753.85=SEN. KENNEDY,757.51=PROF. ALFORD,762.57=SEN. KENNEDY,780.53=PROF. ALFORD,787.05=SEN. KENNEDY,927.13=SEN. WELCH,944.89=MR. SHEEDY,946.41=SEN. WELCH,955.89=MR. SHEEDY,957.71=SEN. WELCH,967.65=MS. KIRKPATRICK,969.41=SEN. WELCH,971.73=MS. KIRKPATRICK,973.03=SEN. WELCH,978.23=MS. KIRKPATRICK,979.35=SEN. WELCH,994.13=MS. KIRKPATRICK,1000.01=SEN. WELCH,1004.03=MS. KIRKPATRICK,1006.77=SEN. WELCH,1044.95=MR. SHEEDY,1045.31=SEN. WELCH,1049.65=MS. KIRKPATRICK,1049.95=SEN. WELCH,1062.95=MR. SHEEDY,1063.67=SEN. WELCH,1074.21=MR. SHEEDY,1078.81=SEN. WELCH,1088.83=THE CHAIR,1090.57=SEN. HAWLEY,1103.01=SEN. HAWLEY,1112.83=MS. KIRKPATRICK,1114.47=SEN. HAWLEY,1116.49=MR. SHEEDY,1117.85=SEN. HAWLEY,1119.69=MR. SHEEDY,1121.97=SEN. HAWLEY,1136.47=MR. SHEEDY,1137.93=SEN. HAWLEY" --title "Senate Judiciary Committee hearing on card swipe fees, 19 Nov 2024 (five stretches)"
```

_Generated 2026-11-15 by `recast.py`._
