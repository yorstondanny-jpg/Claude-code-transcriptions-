// Caricature heads for the 442oons look test. Every head is drawn around (0,0) = the point between the eyes,
// face about 200 units wide; scale with ctx.scale before calling. pose = { mouth, look:[dx,dy], brows, blink, turn }
const { blob, shape, line, shade, INK } = require('./lib');

const MOUTHS = ['closed', 'smile', 'open', 'o', 'grimace', 'sing'];

function mirror(pts) { return pts.map(([x, y]) => [-x, y]).reverse(); }
function sym(half) { return half.concat(mirror(half).slice(1, -1)); }   // half from top centre clockwise to bottom centre

function eyes(ctx, S, P) {
  const t = P.turn || 0, [lx, ly] = P.look || [0, 0];
  for (const side of [-1, 1]) {
    const cx = side * S.eyeGap + t * 14, cy = S.eyeY;
    const w = S.eyeW * (1 + side * t * 0.15), h = S.eyeH;
    if (P.blink) { line(ctx, blob([[cx - w, cy], [cx, cy + h * 0.35], [cx + w, cy]], false), S.lw); continue; }
    const white = blob([[cx - w, cy], [cx - w * 0.4, cy - h], [cx + w * 0.45, cy - h * 0.95], [cx + w, cy - h * 0.05],
      [cx + w * 0.4, cy + h * 0.8], [cx - w * 0.45, cy + h * 0.75]]);
    shape(ctx, white, { fill: '#ffffff', lw: S.lw * 0.8 });
    ctx.save(); require('./lib').trace(ctx, white); ctx.clip();
    ctx.beginPath(); ctx.arc(cx + lx * w * 0.45, cy + ly * h * 0.4, S.irisR, 0, Math.PI * 2);
    ctx.fillStyle = S.iris; ctx.fill();
    ctx.beginPath(); ctx.arc(cx + lx * w * 0.45, cy + ly * h * 0.4, S.irisR * 0.55, 0, Math.PI * 2);
    ctx.fillStyle = '#111'; ctx.fill();
    // upper lid shadow
    ctx.fillStyle = 'rgba(0,0,0,0.12)'; ctx.fillRect(cx - w, cy - h, 2 * w, h * 0.45);
    ctx.restore();
    // heavy upper lid line
    line(ctx, blob([[cx - w * 1.05, cy + h * 0.05], [cx - w * 0.4, cy - h * 1.02], [cx + w * 0.45, cy - h * 0.97], [cx + w * 1.05, cy - h * 0.02]], false), S.lw * 1.25);
    if (S.lidCrease) line(ctx, blob([[cx - w * 0.9, cy - h * 1.3], [cx, cy - h * 1.9], [cx + w * 0.95, cy - h * 1.25]], false), S.lw * 0.55, shade(S.skin, 0.6));
    if (S.underEye) line(ctx, blob([[cx - w * 0.7, cy + h * 1.15], [cx, cy + h * 1.35], [cx + w * 0.7, cy + h * 1.1]], false), S.lw * 0.45, shade(S.skin, 0.6));
  }
}

function brows(ctx, S, P) {
  const t = P.turn || 0, b = P.brows || 0;   // b: -1 angry, 0 neutral, 1 worried/raised
  for (const side of [-1, 1]) {
    const cx = side * S.eyeGap + t * 14, cy = S.eyeY - S.eyeH - S.browGap;
    const inner = [cx - side * S.eyeW * 0.95, cy + (b < 0 ? 10 : b > 0 ? -14 : 0)];
    const mid = [cx + side * S.eyeW * 0.1, cy - (S.browFlat ? 2 : 8) - (b > 0 ? 6 : 0)];
    const outer = [cx + side * S.eyeW * 1.15, cy + 4 + (b > 0 ? 6 : 0)];
    const th = S.browT;
    const pts = side < 0 ? [outer, mid, inner] : [inner, mid, outer];
    const top = pts.map(([x, y], i) => [x, y - th * (i === 1 ? 1 : 0.6)]);
    const bot = pts.slice().reverse().map(([x, y], i) => [x, y + th * (i === 1 ? 0.5 : 0.25)]);
    shape(ctx, blob(top.concat(bot)), { fill: S.browColor, lw: S.lw * 0.5, stroke: shade(S.browColor, 0.55) });
  }
}

function nose(ctx, S, P) {
  const t = (P.turn || 0) * 16, y = S.noseY, w = S.noseW;
  // bridge shadow on one side
  line(ctx, blob([[t - w * 0.25, S.eyeY + 6], [t - w * 0.35, y - 26], [t - w * 0.62, y - 6]], false), S.lw * 0.7, shade(S.skin, 0.62));
  // nostrils and tip
  line(ctx, blob([[t - w, y - 8], [t - w * 1.05, y + 4], [t - w * 0.55, y + 8], [t - w * 0.25, y + 4]], false), S.lw * 0.9);
  line(ctx, blob([[t + w, y - 8], [t + w * 1.05, y + 4], [t + w * 0.55, y + 8], [t + w * 0.25, y + 4]], false), S.lw * 0.9);
  line(ctx, blob([[t - w * 0.25, y + 5], [t, y + 10], [t + w * 0.25, y + 5]], false), S.lw * 0.6, shade(S.skin, 0.55));
}

function mouth(ctx, S, P) {
  const t = (P.turn || 0) * 14, y = S.mouthY, w = S.mouthW, m = P.mouth || 'closed';
  const lipC = S.lip || shade(S.skin, 0.78);
  if (m === 'closed') {
    if (S.lipFull) {   // lower lip as a soft shape, upper lip shadow
      shape(ctx, blob([[t - w * 0.85, y + 2], [t, y + 4], [t + w * 0.85, y + 2], [t + w * 0.45, y + S.lipFull], [t, y + S.lipFull + 3], [t - w * 0.45, y + S.lipFull]]), { fill: lipC, lw: S.lw * 0.5, stroke: shade(lipC, 0.6) });
      shape(ctx, blob([[t - w * 0.85, y + 1], [t - w * 0.3, y - S.lipFull * 0.55], [t, y - S.lipFull * 0.35], [t + w * 0.3, y - S.lipFull * 0.55], [t + w * 0.85, y + 1], [t, y + 3]]), { fill: shade(lipC, 0.85), lw: 0 });
    }
    line(ctx, blob([[t - w, y], [t - w * 0.3, y + 3], [t + w * 0.3, y + 3], [t + w, y]], false), S.lw);
    if (!S.lipFull) line(ctx, blob([[t - w * 0.4, y + 16], [t, y + 19], [t + w * 0.4, y + 16]], false), S.lw * 0.6, shade(S.skin, 0.6));
    return;
  }
  let outer, teethTop = false, teethBot = false, tongue = false;
  if (m === 'smile') { outer = [[t - w * 1.1, y - 6], [t, y + 4], [t + w * 1.1, y - 6], [t + w * 0.6, y + 18], [t, y + 24], [t - w * 0.6, y + 18]]; teethTop = true; }
  if (m === 'open') { outer = [[t - w * 0.9, y], [t, y - 6], [t + w * 0.9, y], [t + w * 0.6, y + 30], [t, y + 38], [t - w * 0.6, y + 30]]; teethTop = true; tongue = true; }
  if (m === 'o') { outer = [[t - w * 0.45, y + 6], [t, y - 6], [t + w * 0.45, y + 6], [t + w * 0.4, y + 30], [t, y + 36], [t - w * 0.4, y + 30]]; tongue = true; }
  if (m === 'grimace') { outer = [[t - w * 1.15, y + 2], [t - w * 0.4, y - 8], [t + w * 0.4, y - 8], [t + w * 1.15, y + 2], [t + w * 0.7, y + 22], [t, y + 16], [t - w * 0.7, y + 22]]; teethTop = teethBot = true; }
  if (m === 'sing') { outer = [[t - w * 0.85, y - 2], [t, y - 10], [t + w * 0.85, y - 2], [t + w * 0.7, y + 40], [t, y + 52], [t - w * 0.7, y + 40]]; teethTop = true; tongue = true; }
  const o = blob(outer);
  shape(ctx, o, { fill: '#5a1a1a', lw: 0 });
  ctx.save(); require('./lib').trace(ctx, o); ctx.clip();
  if (tongue) { ctx.beginPath(); ctx.ellipse(t, y + 44, w * 0.6, 18, 0, 0, Math.PI * 2); ctx.fillStyle = '#d9606a'; ctx.fill(); }
  if (teethTop) { ctx.fillStyle = '#fbfbf6'; ctx.fillRect(t - w * 1.2, y - 14, w * 2.4, m === 'smile' ? 18 : 15); }
  if (teethBot) { ctx.fillStyle = '#fbfbf6'; ctx.fillRect(t - w * 1.2, y + 8, w * 2.4, 20);
    line(ctx, [['M', t - w * 1.2, y + 6], ['L', t + w * 1.2, y + 6]], S.lw * 0.5, '#999'); }
  ctx.restore();
  shape(ctx, o, { lw: S.lw });
  if (m !== 'o') line(ctx, blob([[t - w * 0.35, y + (m === 'sing' ? 62 : m === 'open' ? 48 : 34)], [t, y + (m === 'sing' ? 66 : m === 'open' ? 52 : 37)], [t + w * 0.35, y + (m === 'sing' ? 62 : m === 'open' ? 48 : 34)]], false), S.lw * 0.6, shade(S.skin, 0.6));
}

function face(S, P) {
  if (S.contour) return sym(S.contour);
  // jaw outline from top of forehead clockwise
  const J = S.jaw;   // { top, cheekW, cheekY, jawW, jawY, chinW, chinY, templeW }
  const half = [[0, J.top], [J.templeW * 0.75, J.top + 8], [J.templeW, J.top + 50], [J.cheekW, J.cheekY], [J.jawW, J.jawY],
    [J.chinW, J.chinY - 6], [0, J.chinY]];
  return sym(half);
}

function head(ctx, S, P = {}) {
  const t = P.turn || 0;
  ctx.save();
  S.lw = S.lw || 5;
  const sk = S.skin, skS = shade(sk, 0.84);
  // neck
  if (!S.noNeck) shape(ctx, blob([[-S.neckW, S.jaw.jawY - 10], [S.neckW, S.jaw.jawY - 10], [S.neckW * 1.1, S.jaw.chinY + 90], [-S.neckW * 1.1, S.jaw.chinY + 90]]),
    { fill: sk, shadow: { cmds: blob([[-S.neckW * 1.3, S.jaw.chinY - 30], [S.neckW * 1.3, S.jaw.chinY - 30], [S.neckW * 1.3, S.jaw.chinY + 26], [-S.neckW * 1.3, S.jaw.chinY + 34]]), color: skS } });
  if (S.hairBack) S.hairBack(ctx, S, P);
  // ears
  for (const side of [-1, 1]) {
    const ex = side * (S.jaw.cheekW - 4) + t * 6, ey = S.eyeY + 18;
    const ear = blob([[ex, ey - 32], [ex + side * S.earW, ey - 34], [ex + side * (S.earW + 6), ey - 6], [ex + side * S.earW * 0.7, ey + 28], [ex, ey + 30]]);
    shape(ctx, ear, { fill: sk, lw: S.lw });
    line(ctx, blob([[ex + side * S.earW * 0.3, ey - 18], [ex + side * S.earW * 0.75, ey - 16], [ex + side * S.earW * 0.6, ey + 10]], false), S.lw * 0.6, shade(sk, 0.6));
  }
  // face with a hard shadow down the far side
  const F = blob(face(S, P));
  const shadowSide = S.shadowSide || 1;
  shape(ctx, F, { fill: sk, lw: S.lw, shadow: { cmds: blob([[shadowSide * S.jaw.cheekW * 0.62 + t * 10, S.jaw.top], [shadowSide * 400, S.jaw.top], [shadowSide * 400, S.jaw.chinY + 20], [shadowSide * S.jaw.chinW * 0.4, S.jaw.chinY + 10], [shadowSide * S.jaw.jawW * 0.62, S.jaw.jawY - 20], [shadowSide * S.jaw.cheekW * 0.72, S.jaw.cheekY]]), color: skS } });
  if (S.cheekLines) for (const side of [-1, 1]) line(ctx, blob([[side * S.jaw.cheekW * 0.55, S.noseY - 10], [side * S.jaw.cheekW * 0.62, S.noseY + 22], [side * S.jaw.cheekW * 0.5, S.mouthY + 8]], false), S.lw * 0.5, shade(sk, 0.62));
  if (S.chinCleft) line(ctx, blob([[0, S.jaw.chinY - 30], [2, S.jaw.chinY - 16]], false), S.lw * 0.6, shade(sk, 0.6));
  if (S.browRidge) for (const side of [-1, 1]) line(ctx, blob([[side * (S.eyeGap - S.eyeW), S.eyeY - S.eyeH - S.browGap - 16], [side * S.eyeGap, S.eyeY - S.eyeH - S.browGap - 22], [side * (S.eyeGap + S.eyeW * 1.2), S.eyeY - S.eyeH - S.browGap - 12]], false), S.lw * 0.45, shade(sk, 0.68));
  if (S.cheekbone) for (const side of [-1, 1]) line(ctx, blob([[side * S.jaw.cheekW * 0.92, S.noseY - 22], [side * S.jaw.cheekW * 0.72, S.noseY + 6]], false), S.lw * 0.5, shade(sk, 0.66));
  if (S.beard) S.beard(ctx, S, P);
  eyes(ctx, S, P);
  brows(ctx, S, P);
  nose(ctx, S, P);
  mouth(ctx, S, P);
  if (S.beardTop) S.beardTop(ctx, S, P);
  if (S.hairFront) S.hairFront(ctx, S, P);
  if (S.extra) S.extra(ctx, S, P);
  ctx.restore();
}

module.exports = { head, MOUTHS, blob, shape, line, shade, sym, mirror };
