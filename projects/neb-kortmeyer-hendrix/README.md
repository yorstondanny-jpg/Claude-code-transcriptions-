# Kortmeyer v. Hendrix, Nebraska Supreme Court, 2 Apr 2026 (0:00 to 8:00)


## Transcription

- Clip: 0:00:00.000 to 0:08:00.000 of the source, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 3.84 MB).
- Length: 0:08:00.024 (480.0 s).
- Words: 1145. Lines: 32.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 1; words over 3 s re-timed from a window re-run: 0.
- Match rate: 96.24%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (1161 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 96.24% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py neb-kortmeyer-hendrix "/home/user/pending-review-pipeline/work/kortmeyer-mowing/src/full.mp3" --start 0.0 --end 480.0 --title "Kortmeyer v. Hendrix, Nebraska Supreme Court, 2 Apr 2026 (0:00 to 8:00)"
```

_Generated 2026-11-13 by `recast.py`._
