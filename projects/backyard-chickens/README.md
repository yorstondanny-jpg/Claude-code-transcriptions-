# Casselberry City Commission, 24 Aug 2026, Resolution 26-3589 backyard chicken pilot (15:00 to 30:00 of the meeting recording)


## Transcription

- Clip: whole file, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 7.20 MB).
- Length: 0:15:00.072 (900.1 s).
- Words: 2466. Lines: 79.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 6; words over 3 s re-timed from a window re-run: 0.
- Match rate: 93.39%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (2473 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 93.39% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py backyard-chickens "/home/user/pending-review-pipeline/work/backyard-chickens/clip.wav" --title "Casselberry City Commission, 24 Aug 2026, Resolution 26-3589 backyard chicken pilot (15:00 to 30:00 of the meeting recording)"
```

_Generated 2026-11-18 by `recast.py`._
