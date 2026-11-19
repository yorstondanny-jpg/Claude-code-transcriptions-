# Hall v. Swift, 9th Circuit, 15 Oct 2019 (0:00 to 21:00)


## Transcription

- Clip: 0:00:00.000 to 0:21:00.000 of the source, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 10.08 MB).
- Length: 0:21:00.042 (1260.0 s).
- Words: 3465. Lines: 50.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 8; words over 3 s re-timed from a window re-run: 0.
- Match rate: 93.25%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (3384 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 93.25% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py ninth-hall-v-swift "/home/user/pending-review-pipeline/work/swift-haters/src/full.mp3" --start 0.0 --end 1260.0 --title "Hall v. Swift, 9th Circuit, 15 Oct 2019 (0:00 to 21:00)"
```

_Generated 2026-11-19 by `recast.py`._

## Speakers (hand labelled, 19 Nov 2026)

Whisper has no speaker labels here. Speakers were set by hand from the content (who is asking, who names whom) only around the passages used: Ms. Bogorad (for the songwriters), Mr. Anderson (for Taylor Swift), and the judges as JUDGE (the panel named on tape: Judges Owens, Lee and Hurwitz). Elsewhere a long turn may hold a judge's short question under the lawyer's name.
