// Stocky 442oons figures: FK puppet with kits. Local units: hip centre (0,0), head about 330 units, 1:4 of the body.
const { blob, shape, line, shade, INK } = require('./lib');
const { head } = require('./heads');

const D = Math.PI / 180;
const at = (p, a, L) => [p[0] + L * Math.sin(a * D), p[1] + L * Math.cos(a * D)];   // a: 0 = down, 90 = +x, 180 = up

const KITS = {
  city: { shirt: '#c5e6f8', shirt2: '#f4fbff', sleeve: '#c5e6f8', trim: '#e9f6fd', shorts: '#e9f4fa', socks: '#f2f7fa', boots: '#2fb3c9', text: 'SHAM', textColor: '#ffffff' },
  pool: { shirt: '#c8102e', shirt2: '#c8102e', sleeve: '#c8102e', trim: '#ffffff', shorts: '#c8102e', socks: '#c8102e', boots: '#f2c21b', text: 'scouse\nnotenglish', textColor: '#ffffff', scribble: true },
  ref: { shirt: '#232323', shirt2: '#232323', sleeve: '#232323', trim: '#3a3a3a', shorts: '#1c1c1c', socks: '#1c1c1c', boots: '#141414', badges: true },
};

// tapered capsule from p to q, widths w0 -> w1
function limb(ctx, p, q, w0, w1, fill, lw) {
  const dx = q[0] - p[0], dy = q[1] - p[1], L = Math.hypot(dx, dy) || 1, nx = -dy / L, ny = dx / L;
  ctx.beginPath();
  ctx.moveTo(p[0] + nx * w0, p[1] + ny * w0);
  ctx.lineTo(q[0] + nx * w1, q[1] + ny * w1);
  ctx.arc(q[0], q[1], w1, Math.atan2(ny, nx), Math.atan2(ny, nx) - Math.PI, false);
  ctx.lineTo(p[0] - nx * w0, p[1] - ny * w0);
  ctx.arc(p[0], p[1], w0, Math.atan2(-ny, -nx), Math.atan2(-ny, -nx) - Math.PI, false);
  ctx.closePath();
  ctx.fillStyle = fill; ctx.fill();
  if (lw) { ctx.lineJoin = 'round'; ctx.strokeStyle = INK; ctx.lineWidth = lw; ctx.stroke(); }
}
function chain(ctx, segs, lw) {
  ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  for (const [p, q, w0, w1] of segs) { ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.strokeStyle = INK; ctx.lineWidth = w0 + w1 + 2 * lw; ctx.stroke(); }
  for (const [p, q, w0, w1, fill] of segs) { ctx.beginPath(); ctx.moveTo(p[0], p[1]); ctx.lineTo(q[0], q[1]); ctx.strokeStyle = fill; ctx.lineWidth = w0 + w1; ctx.stroke(); }
}
const lerp = (p, q, t) => [p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t];

function hand(ctx, p, a, fill, lw, open) {
  ctx.save(); ctx.translate(p[0], p[1]); ctx.rotate(-a * D);
  if (open) {   // spread fingers (hands up)
    shape(ctx, blob([[-26, -6], [26, -6], [30, 30], [0, 40], [-30, 30]]), { fill, lw });
    for (const fx of [-24, -9, 7, 22]) limb(ctx, [fx * 0.8, 30], [fx * 1.2, 70], 7, 6, fill, lw);
    limb(ctx, [-26, 14], [-50, 30], 7, 6, fill, lw);
  } else {
    shape(ctx, blob([[-28, -4], [28, -4], [32, 34], [0, 50], [-32, 34]]), { fill, lw });
    line(ctx, [['M', -16, 36], ['Q', 0, 44, 16, 36]], lw * 0.5);
  }
  ctx.restore();
}

function prop(ctx, kind, p, a, lw) {
  ctx.save(); ctx.translate(p[0], p[1]); ctx.rotate(-a * D + Math.PI);
  if (kind === 'yellow' || kind === 'red') {
    ctx.rotate(0.15);
    shape(ctx, blob([[-34, -10], [34, -14], [38, 92], [-30, 96]], true, 0.05), { fill: kind === 'yellow' ? '#ffe11a' : '#e8231c', lw, shadow: { cmds: blob([[10, -20], [50, -20], [50, 100], [14, 100]], true, 0), color: kind === 'yellow' ? '#e9c400' : '#bd1711' } });
  }
  if (kind === 'banana') {
    ctx.rotate(-0.3);
    const b = [['M', -20, 0], ['C', -80, 60, -60, 210, 40, 280], ['C', 20, 200, 10, 90, 30, 10], ['Z']];
    shape(ctx, b, { fill: '#ffe14d', lw, shadow: { cmds: [['M', -10, 20], ['C', -40, 90, -30, 200, 40, 280], ['C', 0, 210, -20, 100, 10, 20], ['Z']], color: '#f0c419' } });
    shape(ctx, blob([[-10, -18], [24, -16], [26, 8], [-14, 8]]), { fill: '#7a5a1c', lw });
  }
  if (kind === 'will') {
    ctx.rotate(0.12);
    shape(ctx, blob([[-70, -10], [70, -14], [74, 170], [-66, 176]], true, 0.04), { fill: '#fbfbf6', lw });
    ctx.fillStyle = '#222'; ctx.textAlign = 'center'; ctx.font = '24px "DejaVu Serif"';
    ['LAST WILL', 'AND', 'TESTAMENT'].forEach((t, i) => ctx.fillText(t, 2, 40 + i * 34));
  }
  ctx.restore();
}

function torso(ctx, who, kit, lw, seed) {
  const T = blob([[-138, -372], [-60, -392], [60, -392], [138, -372], [124, -200], [112, -30], [0, -16], [-112, -30], [-124, -200]]);
  const grad = ctx.createLinearGradient(0, -390, 0, -20); grad.addColorStop(0, kit.shirt); grad.addColorStop(1, kit.shirt2);
  shape(ctx, T, { fill: grad, lw, shadow: { cmds: blob([[70, -400], [160, -400], [160, 0], [60, 0], [76, -200]]), color: 'rgba(0,0,0,0.13)' } });
  // collar
  line(ctx, blob([[-56, -390], [0, -350], [56, -390]], false), lw * 2.2, kit.trim);
  line(ctx, blob([[-60, -394], [0, -346], [60, -394]], false), lw * 0.6);
  if (kit.scribble) {
    let r = seed || 7; const rnd = () => (r = (r * 9301 + 49297) % 233280) / 233280;
    ctx.save(); require('./lib').trace(ctx, T); ctx.clip();
    for (let i = 0; i < 26; i++) { const x = -120 + rnd() * 240, y = -360 + rnd() * 330, a = rnd() * 6.28, l = 14 + rnd() * 26;
      line(ctx, [['M', x, y], ['L', x + Math.cos(a) * l, y + Math.sin(a) * l]], lw * 0.6, 'rgba(255,255,255,0.75)'); }
    ctx.restore();
  }
  if (kit.text) {
    ctx.fillStyle = kit.textColor; ctx.textAlign = 'center';
    if (kit.text === 'SHAM') { ctx.font = 'bold 74px "DejaVu Sans"'; ctx.save(); ctx.translate(0, -210); ctx.rotate(-0.04); ctx.lineWidth = lw * 1.4; ctx.strokeStyle = '#9fcbe6'; ctx.strokeText('SHAM', 0, 0); ctx.fillText('SHAM', 0, 0); ctx.restore(); }
    else { ctx.font = 'bold 40px "DejaVu Sans"'; ctx.fillText('scouse', 0, -220); ctx.font = 'bold 34px "DejaVu Sans"'; ctx.fillText('notenglish', 0, -184); }
  }
  if (kit.badges) {
    shape(ctx, blob([[-96, -300], [-40, -300], [-40, -232], [-68, -214], [-96, -232]], true, 0.1), { fill: '#f6f6f6', lw: lw * 0.7 });
    ctx.fillStyle = '#1d4fa8'; ctx.font = 'bold 13px "DejaVu Sans"'; ctx.textAlign = 'center'; ctx.fillText('REFEREE', -68, -276);
    ctx.font = '9px "DejaVu Sans"'; ctx.fillStyle = '#222'; ctx.fillText('I DO know what', -68, -262); ctx.fillText("I'm doing", -68, -251);
    shape(ctx, blob([[40, -306], [100, -306], [100, -236], [40, -236]], true, 0.1), { fill: '#2b2b2b', lw: lw * 0.7 });
  }
  // shorts
  const sh = blob([[-116, -40], [116, -40], [128, 190], [12, 200], [0, 120], [-12, 200], [-128, 190]], true, 0.2);
  shape(ctx, sh, { fill: kit.shorts, lw, shadow: { cmds: blob([[50, -60], [160, -60], [160, 220], [60, 220]]), color: 'rgba(0,0,0,0.12)' } });
}

// pose: { arms: { L:[upper, fore], R:[upper, fore] }, legs: { L:[thigh, shin], R:[...] }, hold:{L,R}, open:{L,R}, head:{...}, headRot, headDx }
function figure(ctx, who, pose, place) {
  const { x, y, s, rot = 0 } = place;   // y = the hip point on screen
  const kit = KITS[who.kit];
  const lw = Math.max(2.2, Math.min(9, 2 + s * 5.5)) / s;
  const sk = who.skin;
  ctx.save(); ctx.translate(x, y); ctx.scale(s * (pose.flip ? -1 : 1), s); ctx.rotate(rot * D);
  const P = pose;
  const arm = (side) => {
    const [ua, fa] = P.arms[side], sh = [side === 'L' ? -128 : 128, -360];
    const el = at(sh, ua, 205), wr = at(el, fa, 185);
    return { sh, el, wr, fa };
  };
  const leg = (side) => {
    const [ta, sa] = P.legs[side], hp = [side === 'L' ? -64 : 64, 20];
    const kn = at(hp, ta, 290), an = at(kn, sa, 270);
    return { hp, kn, an, sa };
  };
  const drawLeg = (side) => {
    const g = leg(side);
    chain(ctx, [[g.hp, g.kn, 31, 26, sk], [g.kn, g.an, 26, 20, sk]], lw);
    chain(ctx, [[g.hp, lerp(g.hp, g.kn, 0.42), 35, 33, kit.shorts]], lw);
    chain(ctx, [[lerp(g.kn, g.an, 0.2), g.an, 27, 21, kit.socks]], lw);
    // boot points forward and a little out
    ctx.save(); ctx.translate(g.an[0], g.an[1]); ctx.rotate((-g.sa) * D);
    const dir = side === 'L' ? -1 : 1;
    shape(ctx, blob([[-30, -10], [30, -10], [34 + dir * 26, 34], [dir * 40, 52], [-dir * 34, 50], [-34, 30]]), { fill: kit.boots, lw });
    ctx.restore();
  };
  const drawArm = (side) => {
    const a = arm(side);
    chain(ctx, [[a.sh, a.el, 25, 22, sk], [a.el, a.wr, 22, 18, sk]], lw);
    chain(ctx, [[a.sh, lerp(a.sh, a.el, 0.5), 31, 28, kit.sleeve]], lw);
    if (who.kit === 'ref') chain(ctx, [[lerp(a.el, a.wr, 0.8), lerp(a.el, a.wr, 0.92), 16, 16, '#111']], lw * 0.6);
    const h = P.hold && P.hold[side];
    if (h && h !== 'banana') prop(ctx, h, at(a.wr, a.fa, 30), a.fa, lw);
    hand(ctx, a.wr, a.fa, sk, lw, P.open && P.open[side]);
    if (h === 'banana') prop(ctx, h, at(a.wr, a.fa, 20), a.fa, lw);
  };
  const back = P.back || [];   // limbs drawn behind the torso
  for (const k of back) (k[0] === 'a' ? drawArm : drawLeg)(k[1]);
  for (const side of ['L', 'R']) if (!back.includes('l' + side)) drawLeg(side);
  chain(ctx, [[[0, -330], [0, -440], 46, 46, sk]], lw);
  torso(ctx, who, kit, lw, who.seed);
  const front = P.front || [];
  for (const side of ['L', 'R']) if (!back.includes('a' + side) && !front.includes('a' + side)) drawArm(side);
  // head: by default upright on screen even when the body is rotated
  const neck = [P.headDx || 0, -390];
  ctx.translate(neck[0], neck[1]);
  ctx.rotate(-(rot) * D + (P.headRot || 0) * D);
  ctx.translate(0, -158);
  const S = Object.assign({}, who, { lw, noNeck: true });
  ctx.scale(1.18, 1.18);
  head(ctx, S, P.head || {});
  ctx.restore();
  if (front.length) {   // arms over the head (hands on head)
    ctx.save(); ctx.translate(x, y); ctx.scale(s * (pose.flip ? -1 : 1), s); ctx.rotate(rot * D);
    for (const k of front) drawArm(k[1]);
    ctx.restore();
  }
}

const POSES = {
  stand: { arms: { L: [-12, -6], R: [12, 6] }, legs: { L: [-6, -2], R: [6, 2] } },
  handsUp: { arms: { L: [-125, -170], R: [125, 170] }, legs: { L: [-8, -3], R: [8, 3] }, open: { L: true, R: true } },
  handsOnHead: { arms: { L: [-150, 128], R: [150, -128] }, legs: { L: [-6, -2], R: [6, 2] }, front: ['aL', 'aR'] },
  cardUp: (card) => ({ arms: { L: [-14, -8], R: [150, 175] }, legs: { L: [-6, -2], R: [6, 2] }, hold: { R: card } }),
  cardOut: (card) => ({ arms: { L: [-14, -8], R: [100, 140] }, legs: { L: [-6, -2], R: [6, 2] }, hold: { R: card } }),
  point: { arms: { L: [-14, -8], R: [95, 92] }, legs: { L: [-8, -3], R: [8, 3] } },
  banana: { arms: { L: [-14, -8], R: [160, 190] }, legs: { L: [-6, -2], R: [6, 2] }, hold: { R: 'banana' } },
  run: (k) => ({ arms: { L: [-40 + 70 * k, 30 + 60 * k], R: [40 - 70 * k, -30 - 60 * k] }, legs: { L: [-40 + 70 * k, -10 + 40 * k], R: [40 - 70 * k, 10 - 60 * k] } }),
};

module.exports = { figure, POSES, KITS, prop, limb, hand, at };
