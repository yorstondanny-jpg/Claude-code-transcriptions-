# Brewster v. Beck, 9th Circuit, 12 Jan 2017 (window 0:12:00 to 0:28:00 of the court's file; times here are on the clip's clock: add 720 s for the full recording)

## Source and rights

- Recording: the 9th Circuit's own file, https://cdn.ca9.uscourts.gov/datastore/media/2017/01/12/15-55479.mp3 (argued 12 Jan 2017, Pasadena). A federal court's own recording: clear (federal).
- This project is a window, 0:12:00 to 0:28:00 of that file (the end of the owner's lawyer, Mr. Cook, and most of the city's lawyer, Mr. Dermer). Times here are on the clip's clock: add 720 s for the full recording.
- Speakers set by hand from the words and a rough pitch read: JUDGE A grills the city's lawyer from 4:19 to 9:10 (Judge Watford later calls his question "the question you were going to answer for Judge Kozinski"); JUDGE B asks the phone hypothetical and "keep it for a year?"; JUDGE C is Judge Watford from 12:54. A and B may be the same judge: check by ear before any build.
- Panel: Kozinski, McKeown, Watford. Opinion by Judge Kozinski, filed 21 Jun 2017, 859 F.3d 1194: the 30 day impound is a seizure; reversed.
- The loud pause at 8:55.1 (after "I agree. I see.") may be laughter or crosstalk: listen before marking it.

## Transcription

- Clip: 0:12:00.000 to 0:28:00.000 of the source, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 7.68 MB).
- Length: 0:16:00.052 (960.1 s).
- Words: 2745. Lines: 87.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 10; words over 3 s re-timed from a window re-run: 0.
- Match rate: 97.52%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (2742 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 97.52% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py 9th-brewster-v-beck-2017 "/home/user/pending-review-pipeline/work/brewster-car/full.mp3" --start 720.0 --end 1680.0 --speakers "0=MR. COOK,44.9=JUDGE A,67.5=MR. COOK,69.0=JUDGE A,70.8=MR. COOK,104.6=JUDGE C,142.0=MR. COOK,179.5=JUDGE C,191.4=MR. COOK,203.1=JUDGE A,209.3=MR. DERMER,259.1=JUDGE A,290.1=MR. DERMER,312.9=JUDGE A,314.8=MR. DERMER,317.2=JUDGE A,319.6=MR. DERMER,320.4=JUDGE A,335.4=MR. DERMER,345.9=JUDGE A,350.5=MR. DERMER,358.4=JUDGE A,361.1=MR. DERMER,369.1=JUDGE A,374.9=MR. DERMER,375.9=JUDGE A,409.5=MR. DERMER,412.7=JUDGE A,430.9=MR. DERMER,433.0=JUDGE A,442.3=MR. DERMER,446.4=JUDGE A,447.6=MR. DERMER,450.5=JUDGE A,467.0=MR. DERMER,467.9=JUDGE A,484.3=MR. DERMER,488.6=JUDGE A,500.0=MR. DERMER,502.7=JUDGE A,533.4=MR. DERMER,534.7=JUDGE A,540.6=MR. DERMER,543.2=JUDGE A,550.9=MR. DERMER,561.0=JUDGE B,574.3=MR. DERMER,574.9=JUDGE B,596.6=MR. DERMER,617.6=JUDGE B,636.7=MR. DERMER,652.9=JUDGE B,694.6=MR. DERMER,695.4=JUDGE B,705.6=MR. DERMER,720.5=JUDGE B,735.2=MR. DERMER,745.9=JUDGE B,753.1=MR. DERMER,774.6=JUDGE C,869.2=MR. DERMER,919.0=JUDGE C" --title "Brewster v. Beck, 9th Circuit, 12 Jan 2017 (window 0:12:00 to 0:28:00 of the court's file; times here are on the clip's clock: add 720 s for the full recording)"
```

_Generated 2026-11-28 by `recast.py`._
