# Brewster v. Beck, 9th Circuit, 12 Jan 2017 (window 0:00 to 0:04)


## Transcription

- Clip: 0:00:00.000 to 0:04:00.000 of the source, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 1.92 MB).
- Length: 0:04:00.065 (240.1 s).
- Words: 634. Lines: 13.
- Model: faster-whisper `small.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 4; words over 3 s re-timed from a window re-run: 0.
- Match rate: 95.90%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (642 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 95.90% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py 9th-brewster-v-beck-2017-open "/home/user/pending-review-pipeline/work/brewster-car/full.mp3" --start 0.0 --end 240.0 --title "Brewster v. Beck, 9th Circuit, 12 Jan 2017 (window 0:00 to 0:04)"
```

_Generated 2026-11-28 by `recast.py`._
