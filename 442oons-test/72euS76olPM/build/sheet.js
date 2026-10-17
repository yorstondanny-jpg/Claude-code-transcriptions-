// Character sheet: real photo | 442oons version | ours in 6 mouth shapes
const { createCanvas, loadImage } = require('canvas');
const { head, MOUTHS } = require('./heads');
const C = require('./cast');
const path = require('path');

const jobs = [
  ['HAALAND', 'photos/erling_3.jpg', [300, 180, 900, 780], 'ref/t65.5.png'],
  ['REF', 'photos/chris_2.jpg', [1100, 180, 1700, 780], 'ref/t65.5.png'],
  ['GRAVENBERCH', 'photos/ryan_1.jpg', [650, 150, 1250, 750], 'ref/t80.png'],
  ['DOKU', 'photos/jeremy_3.jpg', [500, 150, 1100, 750], 'ref/t58.5.png'],
];
const only = process.argv[2];

(async () => {
  for (const [key, photo, crop, refimg] of jobs) {
    if (only && only !== key) continue;
    const W = 3 * 420 + 6 * 0, cv = createCanvas(420 * 5, 420 * 2), ctx = cv.getContext('2d');
    ctx.fillStyle = '#f4f1ea'; ctx.fillRect(0, 0, cv.width, cv.height);
    const p = await loadImage(path.join(__dirname, photo));
    const s = Math.max(420 / p.width, 420 / p.height) * 1.6;
    ctx.save(); ctx.beginPath(); ctx.rect(0, 0, 420, 420); ctx.clip();
    ctx.drawImage(p, 210 - p.width * s / 2, 60 - p.height * s * 0.08, p.width * s, p.height * s); ctx.restore();
    const r = await loadImage(path.join(__dirname, refimg));
    ctx.drawImage(r, crop[0], crop[1], crop[2] - crop[0], crop[3] - crop[1], 0, 420, 420, 420);
    const poses = MOUTHS.map(m => ({ mouth: m })).concat([{ mouth: 'grimace', brows: 1, look: [0.6, -0.3] }, { mouth: 'closed', blink: true, brows: -1 }]);
    poses.forEach((P, i) => {
      const col = 1 + (i % 4), row = Math.floor(i / 4);
      ctx.save(); ctx.translate(col * 420 + 210, row * 420 + 190); ctx.scale(0.95, 0.95);
      head(ctx, C[key], P); ctx.restore();
      ctx.fillStyle = '#444'; ctx.font = '22px sans-serif'; ctx.fillText(P.mouth + (P.brows ? ' / brows ' + P.brows : '') + (P.blink ? ' / blink' : ''), col * 420 + 12, row * 420 + 410);
    });
    ctx.fillStyle = '#000'; ctx.font = 'bold 26px sans-serif'; ctx.fillText('photo', 10, 30); ctx.fillText('442oons', 10, 452);
    require('fs').writeFileSync(path.join(__dirname, 'sheets', key + '.png'), cv.toBuffer('image/png'));
    console.log('sheet', key);
  }
})();
