// 442oons look test: 0:51.667 to 1:20.900 of "Liverpool 0-3 Man City - the REAL highlights", redrawn on the original audio.
//   node render.js [--still <t>] [--from t --to t]
const { createCanvas } = require('canvas');
const { spawn } = require('child_process');
const fs = require('fs');
const { figure, POSES, prop } = require('./body');
const { stadium, grey, scoreBug, groundShadow, crash, W, H } = require('./scene');
const C = require('./cast');

const T0 = 51.667, T1 = 80.9, FPS = 30;

// who is voiced when (Whisper word timings); sung lines flap faster and wider
const VOICE = [
  ['DOKU', 54.96, 55.66, 'say'], ['DOKU', 57.14, 59.26, 'say'], ['DOKU', 60.12, 61.46, 'say'],
  ['HAALAND', 64.62, 66.22, 'sing'], ['HAALAND', 66.96, 70.28, 'sing'],
  ['REF', 71.72, 74.36, 'sing'], ['REF', 75.0, 78.4, 'sing'],
];
const SING = ['sing', 'open', 'o', 'sing', 'smile', 'open'], SAY = ['open', 'grimace', 'o', 'open', 'smile'];
function mouth(who, t, rest = 'closed') {
  for (const [w, a, b, kind] of VOICE) if (w === who && t >= a && t <= b) {
    const f = Math.floor(t * FPS / 3);   // a new mouth every 3 frames, like the original
    const set = kind === 'sing' ? SING : SAY;
    return set[(f * 7 + 3) % set.length];
  }
  return rest;
}
const on2 = t => Math.floor(t * 15) / 15;   // animate on 2s
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const P = (base, extra) => Object.assign({}, typeof base === 'function' ? base : base, extra);

// ---- shots ----
const SHOTS = [
  // 1. the dive: Doku flies into Gravenberch, the ref looks on
  [51.667, 53.467, (ctx, t) => {
    const k = ease((t - 51.667) / 1.2);
    stadium(ctx, { z: 0.62, boardY: 300, pan: 0 });
    groundShadow(ctx, 330, 905, 90); groundShadow(ctx, 1240, 905, 90);
    figure(ctx, C.REF, P(POSES.point, { head: { mouth: 'closed', look: [0.8, 0.2], whistle: true } }), { x: 330, y: 680, s: 0.36 });
    figure(ctx, C.GRAVENBERCH, P(POSES.stand, { head: { mouth: k > 0.6 ? 'grimace' : 'closed', look: [0.5, 0.4], brows: k > 0.6 ? 1 : 0 } }), { x: 1240, y: 680, s: 0.36 });
    const dx = 1600 - 420 * k, dy = 640 + 180 * k * k;
    figure(ctx, C.DOKU, { arms: { L: [-160, -170], R: [160, 175] }, legs: { L: [-10, 30], R: [10, -10] }, open: { L: true, R: true },
      head: { mouth: 'o', brows: 1, look: [-0.6, 0] }, headRot: -20 }, { x: dx, y: dy, s: 0.34, rot: -70 - 20 * k });
    if (k > 0.65) crash(ctx, 1150, 880, 70);
  }],
  // 2. slow motion: Doku crawls between the ref's and Gravenberch's legs ("Help!")
  [53.467, 56.4, (ctx, t) => {
    const u = (t - 53.467) / 2.9;
    stadium(ctx, { z: 1.5, boardY: -40, pan: 200, line: false });
    figure(ctx, C.REF, POSES.stand, { x: 180, y: 520, s: 0.95 });
    figure(ctx, C.GRAVENBERCH, POSES.stand, { x: 1780, y: 470, s: 0.95 });
    const reach = Math.sin(on2(t) * 5) * 8;
    figure(ctx, C.DOKU, { arms: { L: [-100 + reach, -60], R: [-70, -40 - reach] }, legs: { L: [12, 30], R: [20, 40] },
      head: { mouth: mouth('DOKU', t), brows: 1, look: [-0.3, -0.5] }, headRot: 8 }, { x: 1140 - 80 * u, y: 880, s: 0.62, rot: -76 });
    grey(ctx);
  }],
  // 3. slow motion, wide: the ref, Doku still crawling, Gravenberch with his hands up ("Tell my...")
  [56.4, 58.133, (ctx, t) => {
    stadium(ctx, { z: 0.7, boardY: 270, pan: 500 });
    groundShadow(ctx, 380, 900, 80); groundShadow(ctx, 1450, 900, 80);
    figure(ctx, C.REF, P(POSES.stand, { head: { look: [0.6, 0.5] } }), { x: 380, y: 670, s: 0.37 });
    figure(ctx, C.GRAVENBERCH, P(POSES.handsUp, { head: { mouth: 'grimace', brows: 1, look: [-0.5, 0.4] } }), { x: 1450, y: 670, s: 0.37 });
    figure(ctx, C.DOKU, { arms: { L: [-100, -62], R: [-72, -40] }, legs: { L: [12, 30], R: [20, 40] },
      head: { mouth: mouth('DOKU', t), brows: 1, look: [-0.2, -0.6] }, headRot: 8 }, { x: 900, y: 850, s: 0.3, rot: -76 });
    grey(ctx);
  }],
  // 4. slow motion close: the ref holds out a Last Will and Testament ("mother! I love you!")
  [58.133, 60.867, (ctx, t) => {
    stadium(ctx, { z: 2.2, boardY: -260, pan: 900, line: false });
    figure(ctx, C.REF, { arms: { L: [-10, -5], R: [40, 60] }, legs: { L: [-4, -2], R: [4, 2] }, hold: { R: 'will' } }, { x: 420, y: 260, s: 1.15 });
    figure(ctx, C.DOKU, { arms: { L: [-95, -40], R: [-60, -20] }, legs: { L: [12, 30], R: [20, 40] },
      head: { mouth: mouth('DOKU', t), brows: 1, look: [-0.7, -0.6] }, headRot: 10 }, { x: 1500, y: 1060, s: 1.05, rot: -72 });
    grey(ctx);
  }],
  // 5a. slow motion wide: Doku lies flat with the will beside him
  [60.867, 63.6, (ctx, t) => {
    stadium(ctx, { z: 0.7, boardY: 270, pan: 700 });
    groundShadow(ctx, 520, 900, 80); groundShadow(ctx, 1460, 900, 80);
    figure(ctx, C.REF, P(POSES.stand, { head: { look: [0.6, 0.6] } }), { x: 520, y: 670, s: 0.37 });
    figure(ctx, C.GRAVENBERCH, P(POSES.handsUp, { head: { mouth: 'grimace', brows: 1, look: [-0.5, 0.6] } }), { x: 1460, y: 670, s: 0.37 });
    ctx.save(); ctx.translate(700, 930); prop(ctx, 'will', [0, 0], 150, 3 / 0.3); ctx.restore();
    figure(ctx, C.DOKU, { arms: { L: [-178, -178], R: [-40, -10] }, legs: { L: [6, 12], R: [14, 20] },
      head: { mouth: mouth('DOKU', t), blink: true }, headRot: 55 }, { x: 1010, y: 905, s: 0.29, rot: -88 });
    grey(ctx);
  }],
  // 5b. colour again: Haaland runs in, pointing ("Born in...")
  [63.6, 65.233, (ctx, t) => {
    const u = ease((t - 63.6) / 1.2), stride = Math.sin(on2(t) * 14);
    stadium(ctx, { z: 0.7, boardY: 270, pan: 700 });
    groundShadow(ctx, 900, 900, 80); groundShadow(ctx, 1500, 900, 80);
    figure(ctx, C.REF, P(POSES.stand, { head: { look: [-0.7, 0.2] } }), { x: 900, y: 670, s: 0.37 });
    figure(ctx, C.GRAVENBERCH, P(POSES.handsUp, { head: { mouth: 'grimace', brows: 1 } }), { x: 1500, y: 670, s: 0.37 });
    figure(ctx, C.DOKU, { arms: { L: [-178, -178], R: [-40, -10] }, legs: { L: [6, 12], R: [14, 20] }, head: { blink: true }, headRot: 55 }, { x: 1180, y: 905, s: 0.29, rot: -88 });
    const run = POSES.run(stride * 0.5);
    figure(ctx, C.HAALAND, Object.assign({}, run, { arms: { L: run.arms.L, R: u > 0.7 ? [95, 92] : run.arms.R }, head: { mouth: mouth('HAALAND', t), brows: -1, look: [0.8, 0] } }),
      { x: -150 + 650 * u, y: 660 - Math.abs(stride) * 12, s: 0.37 });
  }],
  // 6a. close two-shot: Haaland holds a yellow card up to the ref ("...Manchester!")
  [65.233, 67.0, (ctx, t) => {
    stadium(ctx, { z: 2.4, boardY: 300, pan: 1200, line: false });
    figure(ctx, C.HAALAND, { arms: { L: [-8, -4], R: [135, 170] }, legs: { L: [-4, -2], R: [4, 2] }, hold: { R: 'yellow' },
      head: { mouth: mouth('HAALAND', t, 'smile'), look: [0.7, -0.1] } }, { x: 560, y: 1210, s: 1.25 });
    figure(ctx, C.REF, P(POSES.stand, { head: { mouth: 'closed', look: [-0.6, -0.9], brows: 1, whistle: true } }), { x: 1380, y: 1230, s: 1.22 });
  }],
  // 6b. wide: the ref books Gravenberch, Haaland keeps on at him ("You were born in Manchester!")
  [67.0, 71.0, (ctx, t) => {
    const card = t > 69.3 ? 'red' : 'yellow';
    stadium(ctx, { z: 0.72, boardY: 260, pan: 1500 });
    for (const x of [380, 760, 1400]) groundShadow(ctx, x, 900, 80);
    figure(ctx, C.HAALAND, P(POSES.point, { head: { mouth: mouth('HAALAND', t), look: [0.8, 0], brows: -1 } }), { x: 380, y: 668, s: 0.38 });
    const up = ease((t - 67.3) / 0.4);
    figure(ctx, C.REF, { arms: { L: [-14, -8], R: [60 + 90 * up, 90 + 85 * up] }, legs: { L: [-6, -2], R: [6, 2] }, hold: { R: card },
      head: { mouth: 'closed', look: [0.8, 0], whistle: true } }, { x: 760, y: 668, s: 0.38 });
    figure(ctx, C.GRAVENBERCH, P(POSES.handsUp, { head: { mouth: card === 'red' ? 'grimace' : 'open', brows: 1, look: [-0.7, 0] } }), { x: 1400, y: 668, s: 0.38 });
    figure(ctx, C.DOKU, { arms: { L: [-178, -178], R: [-40, -10] }, legs: { L: [6, 12], R: [14, 20] }, head: { blink: true }, headRot: 55 }, { x: 1080, y: 905, s: 0.29, rot: -88 });
  }],
  // 6c. wide: bananas out; the ref sings ("Born in Manchester!")
  [71.0, 74.733, (ctx, t) => {
    const wave = Math.sin(on2(t) * 6) * 18;
    stadium(ctx, { z: 0.72, boardY: 260, pan: 1500 });
    for (const x of [380, 760, 1400]) groundShadow(ctx, x, 900, 80);
    figure(ctx, C.HAALAND, { arms: { L: [-14, -8], R: [160 + wave, 190 + wave] }, legs: { L: [-6, -2], R: [6, 2] }, hold: { R: 'banana' },
      head: { mouth: 'smile', look: [0.6, -0.4] } }, { x: 380, y: 668, s: 0.38 });
    figure(ctx, C.REF, P(POSES.cardUp('red'), { head: { mouth: mouth('REF', t), look: [0.5, -0.3] } }), { x: 760, y: 668, s: 0.38 });
    figure(ctx, C.GRAVENBERCH, P(POSES.handsOnHead, { head: { mouth: 'grimace', brows: 1, look: [-0.6, 0] } }), { x: 1400, y: 668, s: 0.38 });
    figure(ctx, C.DOKU, { arms: { L: [-178, -178], R: [-40, -10] }, legs: { L: [6, 12], R: [14, 20] }, head: { blink: true }, headRot: 55 }, { x: 1080, y: 905, s: 0.29, rot: -88 });
  }],
  // 7. medium: banana, red card, Gravenberch in despair ("I was born...")
  [74.733, 77.167, (ctx, t) => {
    const wave = Math.sin(on2(t) * 6) * 18;
    stadium(ctx, { z: 1.2, boardY: 160, pan: 1900, line: false });
    figure(ctx, C.HAALAND, { arms: { L: [-14, -8], R: [160 + wave, 190 + wave] }, legs: { L: [-6, -2], R: [6, 2] }, hold: { R: 'banana' }, head: { mouth: 'smile', look: [0.7, 0] } }, { x: 230, y: 760, s: 0.62 });
    figure(ctx, C.REF, P(POSES.cardUp('red'), { head: { mouth: mouth('REF', t), look: [0.4, -0.3] } }), { x: 900, y: 760, s: 0.62 });
    figure(ctx, C.GRAVENBERCH, P(POSES.handsOnHead, { head: { mouth: 'grimace', brows: 1, look: [-0.7, 0] } }), { x: 1520, y: 760, s: 0.62 });
  }],
  // 8. closer: the ref and the red card, Gravenberch stares ("...in Manchester!")
  [77.167, 79.267, (ctx, t) => {
    stadium(ctx, { z: 2.0, boardY: 240, pan: 2300, line: false });
    figure(ctx, C.REF, P(POSES.cardUp('red'), { head: { mouth: mouth('REF', t), look: [0.6, -0.2] } }), { x: 620, y: 1030, s: 1.05 });
    figure(ctx, C.GRAVENBERCH, P(POSES.stand, { head: { mouth: 'grimace', brows: 1, look: [-0.8, -0.2] } }), { x: 1400, y: 1040, s: 1.05 });
  }],
  // 9. close-up: Gravenberch can't believe it
  [79.267, 80.9, (ctx, t) => {
    stadium(ctx, { z: 3.0, boardY: 330, pan: 2600, line: false });
    ctx.save(); ctx.translate(120, 120); prop(ctx, 'red', [0, 0], 190, 6); ctx.restore();
    figure(ctx, C.GRAVENBERCH, P(POSES.stand, { head: { mouth: 'grimace', brows: 1, look: on2(t) > 80.1 ? [0, 0] : [-0.5, -0.2] } }), { x: 980, y: 1480, s: 1.6 });
  }],
];

function frame(ctx, t) {
  const shot = SHOTS.find(([a, b]) => t >= a && t < b) || SHOTS[SHOTS.length - 1];
  ctx.save(); shot[2](ctx, t); ctx.restore();
  scoreBug(ctx, 0, 0);
}

async function main() {
  const a = process.argv.slice(2), cv = createCanvas(W, H), ctx = cv.getContext('2d');
  if (a[0] === '--still') {
    for (const ts of a.slice(1)) { const t = parseFloat(ts); frame(ctx, t); fs.writeFileSync(`stills/s_${ts}.png`, cv.toBuffer('image/png')); }
    return;
  }
  const from = a.includes('--from') ? parseFloat(a[a.indexOf('--from') + 1]) : T0, to = a.includes('--to') ? parseFloat(a[a.indexOf('--to') + 1]) : T1;
  const n = Math.round((to - from) * FPS), out = a.includes('--out') ? a[a.indexOf('--out') + 1] : 'out/ours_silent.mp4';
  const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', `${W}x${H}`, '-r', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = 0; i < n; i++) {
    frame(ctx, from + i / FPS);
    const buf = cv.toBuffer('raw');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 90 === 0) process.stderr.write(`frame ${i}/${n}\n`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  console.log('wrote', out, n, 'frames');
}
main();
