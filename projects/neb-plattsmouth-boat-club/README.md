# Plattsmouth Boat Club v. City of Plattsmouth, Nebraska Supreme Court, 19 May 2026 (2:00 to 9:20)


## Transcription

- Clip: 0:02:00.000 to 0:09:20.000 of the source, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 3.52 MB).
- Length: 0:07:20.040 (440.0 s).
- Words: 1231. Lines: 6.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 0; words over 3 s re-timed from a window re-run: 0.
- Match rate: 92.28%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (1232 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 92.28% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py neb-plattsmouth-boat-club "/home/user/pending-review-pipeline/work/plattsmouth/src/full.mp3" --start 120.0 --end 560.0 --title "Plattsmouth Boat Club v. City of Plattsmouth, Nebraska Supreme Court, 19 May 2026 (2:00 to 9:20)"
```

_Generated 2026-11-13 by `recast.py`._
