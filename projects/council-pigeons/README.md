# council-pigeons

Recast animation pilot: real public-meeting audio, to be performed by pigeons. The transcribed clip
is candidate 1 below: a St. Petersburg City Council committee working out what a flashing red light
means.

## Copyright status

**Public record of a Florida city; no copyright claim on the recording.** The clip is the City of
St. Petersburg's own recording of a public meeting of its Housing, Land Use and Transportation
Committee, served from the city's Granicus archive. Florida's Constitution (Art. I, §24) and the Public
Records Act (Chapter 119, Florida Statutes) make recordings like this public records open to anyone.
Florida courts have held that an agency can't claim copyright in its public records unless a statute
specifically lets it (*Microdecisions, Inc. v. Skinner*, 889 So. 2d 871 (Fla. 2d DCA 2004)), and no
statute covers meeting video.

One caveat, recorded for completeness: the city's archive listing page
(`stpete.granicus.com/ViewPublisher.php?view_id=6`) has a generic site footer reading "City of St.
Petersburg ©2014, All Rights Reserved." The player page for this meeting carries no notice. Under
*Microdecisions* that footer doesn't make the recording copyrightable, but it's there. This is a summary
of the public-records position, not legal advice.

The speakers are labelled by role, not name: a council member (elected, speaking in session) and a
city transportation staff member. No private citizens speak in the clip.

## Source

- Body: City of St. Petersburg, FL, City Council: Housing, Land Use and Transportation Committee.
- Meeting date: May 14, 2026 (1 h 18 min recording).
- Official archive: https://stpete.granicus.com/player/clip/7152?view_id=6&redirect=true (Granicus
  clip 7152, listed at https://stpete.granicus.com/ViewPublisher.php?view_id=6).
- Audio file: the city's MP3 for that clip,
  `https://archive-video.granicus.com/stpete/stpete_36be91c4-9a49-42fe-84a6-133513ef433b.mp3`
  (the server wants a browser user agent and a `stpete.granicus.com` referer).
- Clip: 0:24:14.0 to 0:24:58.4 of the meeting (1454.0 to 1498.4 s), 44.4 s.

## Speakers

| label | who | how assigned |
|---|---|---|
| COUNCIL MEMBER | committee member asking the questions | lower voice (about 120 Hz median pitch) |
| CITY STAFF | transportation staff presenting the plan | higher voice (about 200 Hz) |

Turns were set by hand from a pitch track and the sense of the exchange. "Correct." at 0:30 is spoken
in the council member's voice (checking their own rule, not being told they're right). The
"I don't, I'm like it's flashing" run jumps in pitch, so it could be a second voice cutting in, but it
reads as one speaker and is labelled that way.

## Candidates

All three are from official Granicus archives of Florida local governments, confirmed by downloading
the audio and transcribing the stretch with Whisper. Timestamps are from the start of each meeting
recording. Candidates 2 and 3 were checked with `small.en` on a window and are good to about ±2 s.

| # | body | date | timestamps | official source |
|---|---|---|---|---|
| 1 (transcribed) | St. Petersburg City Council, Housing, Land Use and Transportation Committee | May 14, 2026 | 0:24:14 to 0:24:58 (44 s) | https://stpete.granicus.com/player/clip/7152?view_id=6&redirect=true |
| 2 | Pinellas County Board of County Commissioners, regular meeting | Nov 18, 2025 | 1:52:00 to 1:52:45 (45 s) | https://pinellas.granicus.com/player/clip/2973?view_id=1&redirect=true |
| 3 | Pinellas County Board of County Commissioners, work session / agenda briefing | May 14, 2026 | 1:03:26 to 1:04:00 (34 s) | https://pinellas.granicus.com/player/clip/3077?view_id=1&redirect=true |

**1. "What's the flashing red?"** In a discussion of pedestrian hybrid beacons, a council member asks
what a flashing red light means. Staff answer with a long, deadpan, by-the-book explanation (railroad
signals, "hence the red indication"). The council member boils it down: solid red is a stoplight,
flashing red is a stop sign. "Is that the best way to remember?" "Yes, yes indeed." Then the confession:
"Hopefully I've been doing it right... it's flashing... Can I go?" The loudest pause in the clip
(laughs.md #1) is the beat before "Can I go?". It's funny because a committee in charge of traffic
policy discovers, on the record, that it isn't sure about red lights. Nobody is mocked: the council
member is the butt of their own joke. Basis: the public-records position above (City of St.
Petersburg, Florida).

**2. "A lot of emails about nude beaches."** During commissioner reports, a county commissioner
recounts a "Great American Teach-In" visit to a fifth-grade class: told not to be partisan, the
commissioner was asked what kind of emails a commissioner gets and answered "a lot of emails about nude
beaches." The teacher didn't appreciate it, "but the kids got a good laugh though... You asked, so. It
is true, it is true, it is true." Deadpan self-report from an elected official in session. No one is
named apart from the school. Basis: Pinellas County, Florida public record; same Florida law as above.
The Pinellas Granicus pages carry no copyright notice.

**3. "They're laughing at me, Commissioner Scott."** At a budget work session, a recreation district
director (staff, so unnamed here) wraps up an earnest budget update ("Thank you for listening to me,
Babylon, because I could go on and on. Any questions?", where Whisper and the captions both write
"Babylon" for what is probably "babble"), then catches the board grinning: "They're
laughing at me, Commissioner Scott. I see it. I appreciate it, but I see it." (Whisper hears "They're
laughing at me"; the county's own captions have "Quit laughing at me". Check by ear before using.)
The next speaker, a library director, opens with "I'm just gonna spend all my time thanking everybody.
Is that fine?" Basis: Pinellas County, Florida public record, as for 2.

How they were found: the auto-generated captions (`/videos/<clip>/captions.vtt`) for the latest 120
meetings each from St. Petersburg, Pinellas County, San Jose, Fresno and Rancho Palos Verdes were
searched for "laugh". The hits were then checked against the audio. Fresno and Rancho Palos Verdes
publish no caption text. Political items, public comment from private citizens, and anything about
crime or grief were skipped.

## Transcription

- Clip: 0:24:14.000 to 0:24:58.400 of the source, re-encoded to mono 64 kbps MP3 (`audio/source.mp3`, 0.36 MB).
- Length: 0:00:44.434 (44.4 s).
- Words: 129. Lines: 8.
- Model: faster-whisper `medium.en` (CPU, int8, beam 5, word timestamps, no VAD filter). There is no official transcript: the wording is Whisper's, unedited.
- Music and sound cues Whisper writes as words (bracketed text, a lone "Music") are dropped: 0 tokens here.
- Words over 1.5 s trimmed to the voiced audio: 0; words over 3 s re-timed from a window re-run: 0.
- Match rate: 97.67%. With no official wording, this is Whisper against itself: a second, independent pass over 30 s windows (127 words) agrees with this share of the first pass's words.

## Sanity checks

| check | result | detail |
|---|---|---|
| time order | PASS | 0 words start before the previous word; 0 end before they start |
| max duration | PASS | 0 words longer than 3 s |
| match rate | PASS | 97.67% (threshold 85%) |

## Files

- `audio/source.mp3`: the clip.
- `audio/words.json`: one entry per word, `{"w", "s", "e", "speaker"}` (seconds into source.mp3).
- `lines.json`: one entry per line, `{"speaker", "s", "e", "text"}`; a new line starts on a speaker change or after a sentence end followed by 0.7 s of silence.
- `laughs.md`: every pause of 0.4 s or more, ranked by loudness, and the loudest short bursts.

Regenerate with:

```
python3 recast.py council-pigeons "https://archive-video.granicus.com/stpete/stpete_36be91c4-9a49-42fe-84a6-133513ef433b.mp3" --start 1454.0 --end 1498.4 --speakers "0=COUNCIL MEMBER,2.3=CITY STAFF,25.0=COUNCIL MEMBER,32.5=CITY STAFF,33.4=COUNCIL MEMBER,34.5=CITY STAFF,36.5=COUNCIL MEMBER" --title "council-pigeons" --referer "https://stpete.granicus.com/player/clip/7152"
```

_Generated 2026-10-05 by `recast.py`._
