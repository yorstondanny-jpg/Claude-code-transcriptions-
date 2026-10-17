// Drawing helpers for the 442oons look test: flat fill, one hard shadow tone, even black outline.
const { createCanvas, registerFont } = require('canvas');

const INK = '#1a1a1a';

// a path given as a list of commands: ['M',x,y], ['L',x,y], ['C',x1,y1,x2,y2,x,y], ['Q',x1,y1,x,y], ['Z']
function trace(ctx, cmds) {
  ctx.beginPath();
  for (const c of cmds) {
    const [k, ...a] = c;
    if (k === 'M') ctx.moveTo(a[0], a[1]);
    else if (k === 'L') ctx.lineTo(a[0], a[1]);
    else if (k === 'C') ctx.bezierCurveTo(a[0], a[1], a[2], a[3], a[4], a[5]);
    else if (k === 'Q') ctx.quadraticCurveTo(a[0], a[1], a[2], a[3]);
    else if (k === 'Z') ctx.closePath();
  }
}

// smooth closed shape through points (Catmull-Rom to bezier)
function blob(pts, closed = true, t = 0.5) {
  const n = pts.length, out = [['M', pts[0][0], pts[0][1]]];
  const P = i => closed ? pts[(i + n) % n] : pts[Math.max(0, Math.min(n - 1, i))];
  const last = closed ? n : n - 1;
  for (let i = 0; i < last; i++) {
    const p0 = P(i - 1), p1 = P(i), p2 = P(i + 1), p3 = P(i + 2);
    out.push(['C', p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3,
      p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3, p2[0], p2[1]]);
  }
  if (closed) out.push(['Z']);
  return out;
}

function shape(ctx, cmds, { fill, stroke = INK, lw = 5, shadow, shadowClip } = {}) {
  trace(ctx, cmds);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (shadow) {   // shadow: { cmds, color } drawn clipped inside the shape
    ctx.save(); trace(ctx, cmds); ctx.clip();
    trace(ctx, shadow.cmds); ctx.fillStyle = shadow.color; ctx.fill();
    ctx.restore(); trace(ctx, cmds);
  }
  if (stroke && lw > 0) {
    ctx.lineJoin = 'round'; ctx.lineCap = 'round';
    ctx.strokeStyle = stroke; ctx.lineWidth = lw; ctx.stroke();
  }
}

function line(ctx, cmds, lw = 4, color = INK) {
  trace(ctx, cmds);
  ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.stroke();
}

// darker tint for the hard shadow tone
function shade(hex, k = 0.82) {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.round(((n >> 16) & 255) * k), g = Math.round(((n >> 8) & 255) * k), b = Math.round((n & 255) * k);
  return '#' + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

module.exports = { createCanvas, registerFont, trace, blob, shape, line, shade, INK };
