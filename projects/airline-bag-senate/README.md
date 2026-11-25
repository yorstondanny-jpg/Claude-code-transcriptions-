# Senate PSI hearing on airline fees, 4 Dec 2024 (bag bounties)


## Transcription

- Clip: whole file, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 5.95 MB).
- Length: 0:12:24.046 (744.0 s).
- Words: 2491. Lines: 8.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 6; words over 3 s re-timed from a window re-run: 0.
- Match rate: 91.49%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (2458 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 91.49% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py airline-bag-senate "/home/user/pending-review-pipeline/work/airline-bag/src/clip.wav" --title "Senate PSI hearing on airline fees, 4 Dec 2024 (bag bounties)"
```

_Generated 2026-11-25 by `recast.py`._
# Senate PSI hearing on airline fees, 4 Dec 2024 (Sen. Hawley on bag bounties): one stretch

## Source and rights

- Hearing: US Senate Permanent Subcommittee on Investigations (Homeland Security and Governmental Affairs), "The Sky's the Limit: New Revelations About Airline Fees", 4 December 2024.
- Recording: the committee's own stream, https://www-senate-gov-media-srs.akamaized.net/hls/live/2036792/govtaff/govtaff120424/master.m3u8 (2:24:12 long).
- Rights: clear (federal). A Senate subcommittee's own recording of a public hearing.

## This clip is one stretch of the hearing

Segments 407 to 468 of the stream's index_1.m3u8 (12 s each), joined with no gaps. Clip 0.0 = 1:21:12 (4872.0 s) on the stream, read from the start. Add 4872.0 to any time in words.json or lines.json to get the stream time. The scout's 5136 s for "do you pay employees bounties" is clip 264.

## Speakers

Labelled by hand from the words (who is addressed, who answers). Witnesses heard here: Frontier Airlines' chief commercial officer (addressed as Mr. Schroeder; spelling to check against the hearing's witness list) and Spirit Airlines' chief commercial officer (Mr. Klein). Senators: Hassan (0 to 237), the chair (237.7), Hawley (from 239.4).
Not sure, check by ear before use: the crosstalk at 588 to 600 ("not always, sometimes", "you'll never know ... Russian roulette", "I would agree, no idea in the world, I would disagree"); "it's never women more ... miners more" at 495 to 500 is Hawley asking "is it women more? minors more?" heard badly.
Machine transcript, no official wording: "your kid last year" at 478 is probably "you can, last year"; "Hasen" is "Hassan"; "Mr. shorter" at 708 is "Mr. Schroeder"; "fair" at 660 is "fare".
No room laughs found (a hearing room).
