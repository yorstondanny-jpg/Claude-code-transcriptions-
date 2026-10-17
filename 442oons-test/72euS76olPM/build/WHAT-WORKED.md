# 442oons look test: what worked

Section: 0:51.7 to 1:20.9 of "Liverpool 0-3 Man City - the REAL highlights" (29 s, 9 cuts), redrawn shot for shot on the original audio. Cast: the ref, Doku, Gravenberch, Haaland. Everything is drawn in code (node-canvas): no AI image or video generation, no tracing.

Files: `out/ours.mp4` (1080p, original audio), `out/sidebyside.mp4` (theirs left, ours right), `sheets/` (character sheets: photo, their version, our mouth set), `stills/`, and the source (`heads.js`, `cast.js`, `body.js`, `scene.js`, `render.js`).

## What held up
- The look: flat fills, one hard shadow tone, even black line, pink stand with seat arcs, parody ad boards, striped pitch, score bug, the greyed slow-motion beat. On a phone it reads as the same show.
- The timing: cuts on the original's cut points; mouths open only while that character is voiced (Whisper word timings), swapping every 3 frames like theirs.
- Speed: once the rig exists, a new shot is about 10 lines of code, and the 29 s renders in under a minute.

## What didn't, yet
- Faces are recognisable by hair, skin, beard and kit more than by the face itself. Haaland and the ref get closest. Their artist's faces carry more real anatomy (cheekbones, eye shapes, the 3/4 turn). Ours are all front-on.
- Motion is stiffer than theirs: our poses are held and swapped, theirs have more in-betweens (the crawl, the dive, Haaland's run).
- Their wide shots have more people (extra City players waving bananas). We cut those to keep to four faces.

## What a full episode would need
1. A 3/4 head view per player and a better face pass (eyes and brows carry most of the likeness). That's about 30 to 45 minutes per player the first time. After that a player is reusable in every episode, so a squad library builds up.
2. A crawl, dive, celebrate and run cycle library, built once.
3. Their script and audio, as here. Songs and voices stay with their team (Dean Stobbart). We animate.

Rough cost: this test took about 2 hours of build time, faces included. With a player library in place, a 2-minute episode is likely a day's work, most of it on the new faces and the big physical gags.
