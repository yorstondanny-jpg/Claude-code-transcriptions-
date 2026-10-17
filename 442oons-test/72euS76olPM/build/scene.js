// The 442oons stadium set: flat pink stand with seat arcs, LED ad boards with parody brands, striped pitch.
const { blob, shape, line, INK } = require('./lib');

const W = 1920, H = 1080;
const BOARDS = [
  { t: 'BLACK&BECKER', bg: '#161616', fg: '#ffffff', font: 'bold 64px "DejaVu Sans Condensed"' },
  { t: 'Coca-Iraola', bg: '#e41e26', fg: '#ffffff', font: 'italic bold 66px "DejaVu Serif"' },
  { t: "Dominiko's Pizza", bg: '#1260c4', fg: '#ffffff', font: 'bold 52px "DejaVu Sans"' },
  { t: 'Isaks', bg: '#ffffff', fg: '#1a3fa0', font: 'italic bold 66px "DejaVu Sans"' },
  { t: 'bradidas', bg: '#161616', fg: '#ffffff', font: 'bold 60px "DejaVu Sans"' },
];

// cam: { z: zoom (1 = wide), boardY: top of the ad boards on screen, pan: horizontal offset in px }
function stadium(ctx, cam) {
  const z = cam.z, by = cam.boardY, bh = 86 * z;
  // stand
  ctx.fillStyle = '#f47a79'; ctx.fillRect(0, 0, W, by);
  ctx.strokeStyle = '#e66466'; ctx.lineWidth = Math.max(2, 3 * z); ctx.lineCap = 'round';
  const sp = 120 * z, rh = 70 * z;
  for (let r = 0; by - r * rh > -rh; r++) {
    const y = by - 30 * z - r * rh, off = (r % 2) * sp / 2 - ((cam.pan || 0) * 0.6) % sp;
    for (let x = -sp + off; x < W + sp; x += sp) { ctx.beginPath(); ctx.arc(x, y, 34 * z, Math.PI * 1.1, Math.PI * 1.9); ctx.stroke(); }
  }
  // ad boards
  const bw = 760 * z;
  ctx.save(); ctx.beginPath(); ctx.rect(0, by, W, bh); ctx.clip();
  const start = -(((cam.pan || 0) + (cam.boardOffset || 0)) % (bw * BOARDS.length)) - bw * BOARDS.length;
  for (let i = 0, x = start; x < W; i++, x += bw) {
    const b = BOARDS[((i % BOARDS.length) + BOARDS.length) % BOARDS.length];
    ctx.fillStyle = b.bg; ctx.fillRect(x, by, bw, bh);
    ctx.fillStyle = b.fg; ctx.font = b.font.replace(/(\d+)px/, (m, n) => Math.round(n * z) + 'px'); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText(b.t, x + bw / 2, by + bh / 2 + 3 * z);
  }
  ctx.restore();
  ctx.fillStyle = '#2a2a2a'; ctx.fillRect(0, by + bh, W, 5 * z);
  // pitch: two-tone stripes running across, white touchline
  const py = by + bh + 5 * z;
  const band = 150 * z;
  ctx.fillStyle = '#6de368'; ctx.fillRect(0, py, W, H - py);
  for (let i = 0, y = py; y < H; i++) {
    const h = band * (1 + i * 0.12);
    if (i % 2) { ctx.fillStyle = '#55d05c'; ctx.fillRect(0, Math.floor(y), W, Math.ceil(h) + 1); }
    y += h;
  }
  if (cam.line !== false) { ctx.fillStyle = '#fbfffa'; ctx.fillRect(0, py + 40 * z, W, 7 * z); }
}

function groundShadow(ctx, x, y, w) {
  ctx.fillStyle = 'rgba(0,0,0,0.13)'; ctx.beginPath(); ctx.ellipse(x, y, w, w * 0.16, 0, 0, Math.PI * 2); ctx.fill();
}

// greyed slow motion look (desaturate towards grey-green)
function grey(ctx) {
  const im = ctx.getImageData(0, 0, W, H), d = im.data;
  for (let i = 0; i < d.length; i += 4) {
    const l = 0.3 * d[i] + 0.59 * d[i + 1] + 0.11 * d[i + 2];
    d[i] = l * 0.62 + d[i] * 0.12 + 22; d[i + 1] = l * 0.66 + d[i + 1] * 0.12 + 30; d[i + 2] = l * 0.6 + d[i + 2] * 0.1 + 18;
  }
  ctx.putImageData(im, 0, 0);
}

function scoreBug(ctx, home = 0, away = 0) {
  const x = 22, y = 18, h = 40;
  ctx.font = 'bold 28px "DejaVu Sans"'; ctx.textBaseline = 'middle'; ctx.textAlign = 'center';
  ctx.fillStyle = '#c8102e'; ctx.fillRect(x, y, 70, h); ctx.fillStyle = '#fff'; ctx.fillText('LIV', x + 35, y + h / 2 + 1);
  ctx.fillStyle = '#fff'; ctx.fillRect(x + 70, y, 40, h); ctx.fillStyle = '#111'; ctx.fillText(String(home), x + 90, y + h / 2 + 1);
  ctx.fillStyle = '#5b2a86'; ctx.beginPath(); ctx.arc(x + 130, y + h / 2, 21, 0, Math.PI * 2); ctx.fill();
  ctx.fillStyle = '#fff'; ctx.font = 'bold 16px "DejaVu Sans"'; ctx.fillText('PL', x + 130, y + h / 2 + 1);
  ctx.font = 'bold 28px "DejaVu Sans"';
  ctx.fillStyle = '#fff'; ctx.fillRect(x + 150, y, 40, h); ctx.fillStyle = '#111'; ctx.fillText(String(away), x + 170, y + h / 2 + 1);
  ctx.fillStyle = '#6cabdd'; ctx.fillRect(x + 190, y, 76, h); ctx.fillStyle = '#fff'; ctx.fillText('MCI', x + 228, y + h / 2 + 1);
  ctx.font = 'bold 22px "DejaVu Sans"'; ctx.fillStyle = 'rgba(255,255,255,0.85)'; ctx.textAlign = 'right'; ctx.fillText('DEMO', W - 24, y + h / 2);
}

function crash(ctx, x, y, r) {
  const pts = []; for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2, rr = i % 2 ? r * 0.5 : r; pts.push([x + Math.cos(a) * rr, y + Math.sin(a) * rr]); }
  shape(ctx, blob(pts, true, 0.05), { fill: '#ffd21f', lw: 4 });
  shape(ctx, blob(pts.map(([px, py]) => [x + (px - x) * 0.55, y + (py - y) * 0.55]), true, 0.05), { fill: '#ff8a1f', lw: 0 });
}

module.exports = { stadium, grey, scoreBug, groundShadow, crash, W, H };
