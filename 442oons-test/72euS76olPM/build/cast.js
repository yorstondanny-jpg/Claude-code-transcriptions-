// The four people in 0:52 to 1:21. Face contours and feature positions are measured from the Commons photos
// (origin between the eyes, eyes 82 units apart), then pushed a little: Haaland's jaw, Doku's forehead and nose,
// the ref's brows and nose, Gravenberch's line-up and goatee.
const { blob, shape, line, shade } = require('./heads');

function strands(ctx, list, lw, color) { for (const s of list) line(ctx, blob(s, false), lw, color); }
const J = c => ({ top: c[0][1], templeW: c[2][0], cheekW: Math.max(...c.map(p => p[0])), cheekY: c[4][1], jawW: c[6][0], jawY: c[6][1], chinW: c[8][0], chinY: c[c.length - 1][1] });

const H_CONTOUR = [[0, -128], [66, -118], [100, -80], [110, -30], [108, 20], [103, 70], [88, 116], [60, 146], [28, 160], [0, 163]];
const HAALAND = {
  name: 'Erling Haaland', kit: 'city', seed: 3, skin: '#f7d6b8', lip: '#e3a28e', browColor: '#d9b77e', iris: '#6a95c4',
  contour: H_CONTOUR, jaw: J(H_CONTOUR),
  eyeGap: 41, eyeY: 0, eyeW: 19, eyeH: 6, irisR: 6, browGap: 5, browT: 3.5, lidCrease: true,
  noseY: 59, noseW: 24, mouthY: 104, mouthW: 39, lipFull: 13, chinCleft: true, cheekbone: true,
  neckW: 84, earW: 17,
  hairBack(ctx, S) {   // long hair, slicked back, falling behind the ears to the shoulders
    const c = '#e2bb62';
    for (const side of [-1, 1]) shape(ctx, blob([[side * 80, -120], [side * 112, -70], [side * 118, -10], [side * 112, 60], [side * 96, 74], [side * 100, 0], [side * 92, -60]]), { fill: c, lw: S.lw });
  },
  hairFront(ctx, S) {   // flat, wet look, combed straight back from a high hairline
    const c = '#efd083', d = '#d9b25a';
    const cap = blob([[-104, -40], [-106, -100], [-66, -150], [0, -160], [66, -150], [106, -100], [104, -40], [92, -50], [70, -66], [36, -74], [0, -76], [-36, -74], [-70, -66], [-92, -50]]);
    shape(ctx, cap, { fill: c, lw: S.lw, shadow: { cmds: blob([[30, -165], [130, -140], [130, -30], [96, -46], [66, -66], [30, -76]]), color: d } });
    strands(ctx, [[[-76, -62], [-82, -100], [-60, -138]], [[-38, -72], [-40, -112], [-24, -148]], [[2, -76], [4, -118], [10, -152]], [[40, -73], [48, -110], [54, -142]], [[76, -60], [86, -94], [86, -120]]], S.lw * 0.5, '#b68a34');
  },
};

const R_CONTOUR = [[0, -140], [64, -132], [98, -96], [104, -40], [102, 10], [98, 60], [90, 110], [66, 140], [34, 154], [0, 157]];
const REF = {
  name: 'Referee (Chris Kavanagh)', kit: 'ref', skin: '#f2c3a0', lip: '#cf8f7c', browColor: '#2a221d', iris: '#5d4630',
  contour: R_CONTOUR, jaw: J(R_CONTOUR),
  eyeGap: 41, eyeY: 0, eyeW: 18, eyeH: 7.5, irisR: 6.5, browGap: 6, browT: 7, underEye: true, browFlat: true, lidCrease: true,
  noseY: 70, noseW: 21, mouthY: 110, mouthW: 42, cheekLines: true, neckW: 64, earW: 22,
  beard(ctx, S) {   // stubble on the jaw and upper lip
    ctx.globalAlpha = 0.16;
    shape(ctx, blob([[-100, 40], [-86, 100], [-60, 140], [0, 158], [60, 140], [86, 100], [100, 40], [70, 96], [40, 124], [0, 132], [-40, 124], [-70, 96]]), { fill: '#3a2a22', lw: 0 });
    ctx.globalAlpha = 1;
  },
  hairFront(ctx, S) {   // short, dark, receding at the temples, slight widow's peak
    const c = '#2e2925';
    const cap = blob([[-100, -70], [-104, -110], [-60, -158], [0, -168], [60, -158], [104, -110], [100, -70], [86, -84], [76, -106], [52, -96], [20, -84], [0, -78], [-20, -84], [-52, -96], [-76, -106], [-86, -84]]);
    shape(ctx, cap, { fill: c, lw: S.lw });
    for (const side of [-1, 1]) shape(ctx, blob([[side * 100, -70], [side * 104, -16], [side * 97, -10], [side * 92, -64]]), { fill: c, lw: S.lw * 0.6 });
    for (const yy of [-56, -44]) line(ctx, blob([[-40, yy + 3], [0, yy], [40, yy + 3]], false), S.lw * 0.4, shade(S.skin, 0.66));
  },
  extra(ctx, S, P) {   // headset mic on his left ear
    line(ctx, blob([[104, 24], [100, 74], [72, 108], [52, 116]], false), S.lw * 1.1, '#222');
    ctx.beginPath(); ctx.ellipse(48, 117, 9, 6, 0, 0, Math.PI * 2); ctx.fillStyle = '#222'; ctx.fill();
    if (P.whistle) shape(ctx, blob([[-26, 104], [26, 102], [30, 126], [-24, 128]]), { fill: '#222', lw: S.lw });
  },
};

const G_CONTOUR = [[0, -130], [62, -122], [90, -88], [93, -40], [91, 0], [85, 50], [75, 95], [52, 128], [26, 143], [0, 146]];
const GRAVENBERCH = {
  name: 'Ryan Gravenberch', kit: 'pool', seed: 11, skin: '#94603f', lip: '#6e3e2e', browColor: '#1a1311', iris: '#3b2416',
  contour: G_CONTOUR, jaw: J(G_CONTOUR),
  eyeGap: 41, eyeY: 0, eyeW: 20, eyeH: 8, irisR: 7.5, browGap: 6, browT: 7, lidCrease: true,
  noseY: 46, noseW: 25, mouthY: 82, mouthW: 30, lipFull: 13, neckW: 66, earW: 17,
  hairFront(ctx, S) {   // tight fade, razor-sharp line-up
    const c = '#1b1513';
    const cap = blob([[-94, -40], [-96, -100], [-58, -146], [0, -156], [58, -146], [96, -100], [94, -40], [88, -46], [86, -66], [70, -72], [0, -73], [-70, -72], [-86, -66], [-88, -46]], true, 0.25);
    shape(ctx, cap, { fill: c, lw: S.lw });
  },
  beard(ctx, S) {   // short beard along the jaw, darker goatee
    const c = '#1b1513';
    ctx.globalAlpha = 0.35;
    shape(ctx, blob([[-90, 10], [-84, 70], [-60, 120], [0, 146], [60, 120], [84, 70], [90, 10], [70, 70], [40, 108], [0, 118], [-40, 108], [-70, 70]]), { fill: c, lw: 0 });
    ctx.globalAlpha = 1;
    shape(ctx, blob([[-24, 104], [0, 100], [24, 104], [22, 132], [0, 146], [-22, 132]]), { fill: c, lw: S.lw * 0.4 });
  },
  beardTop(ctx, S) {
    shape(ctx, blob([[-30, 72], [-10, 64], [0, 66], [10, 64], [30, 72], [10, 70], [0, 71], [-10, 70]]), { fill: '#1b1513', lw: S.lw * 0.3 });
  },
};

const D_CONTOUR = [[0, -142], [60, -132], [88, -92], [92, -40], [88, 15], [82, 60], [70, 100], [46, 132], [22, 146], [0, 149]];
const DOKU = {
  name: 'Jeremy Doku', kit: 'city', seed: 5, skin: '#4d3428', lip: '#5a3428', browColor: '#120c0a', iris: '#2a1a12',
  contour: D_CONTOUR, jaw: J(D_CONTOUR),
  eyeGap: 41, eyeY: 0, eyeW: 22, eyeH: 8, irisR: 8.5, browGap: 7, browT: 6, lidCrease: true,
  noseY: 46, noseW: 29, mouthY: 76, mouthW: 36, lipFull: 15, neckW: 60, earW: 15,
  hairBack(ctx, S) {   // locs from a high hairline, hanging past the shoulders, brown at the ends
    for (const side of [-1, 1]) for (let i = 0; i < 6; i++) {
      const x0 = side * (58 + i * 7), x1 = side * (90 + i * 9), len = 150 + i * 16;
      const loc = blob([[x0 - 6, -128 + i * 8], [x1, 10 + i * 10], [x1 + side * 4, len], [x1 + side * 16, len + 6], [x1 + side * 14, 10 + i * 10], [x0 + 8, -130 + i * 8]]);
      shape(ctx, loc, { fill: '#171111', lw: S.lw * 0.6, stroke: '#000', shadow: { cmds: blob([[x1 - 30, len - 60], [x1 + 30, len - 60], [x1 + 30, len + 30], [x1 - 30, len + 30]]), color: '#7a4a2a' } });
    }
  },
  hairFront(ctx, S) {
    const c = '#171112';
    const cap = blob([[-88, -50], [-92, -112], [-54, -160], [0, -170], [54, -160], [92, -112], [88, -50], [80, -62], [62, -80], [30, -86], [0, -88], [-30, -86], [-62, -80], [-80, -62]]);
    shape(ctx, cap, { fill: c, lw: S.lw });
    strands(ctx, [[[-62, -82], [-56, -122], [-30, -158]], [[-24, -88], [-18, -130], [0, -164]], [[14, -88], [20, -132], [34, -160]], [[52, -82], [62, -118], [76, -140]]], S.lw * 0.6, '#3d3030');
  },
  beard(ctx, S) {
    ctx.globalAlpha = 0.85;
    shape(ctx, blob([[-22, 112], [0, 108], [22, 112], [20, 136], [0, 148], [-20, 136]]), { fill: '#120c0a', lw: 0 });
    ctx.globalAlpha = 1;
  },
  beardTop(ctx, S) {
    ctx.globalAlpha = 0.6;
    shape(ctx, blob([[-30, 64], [0, 59], [30, 64], [0, 67]]), { fill: '#120c0a', lw: 0 });
    ctx.globalAlpha = 1;
  },
};

module.exports = { HAALAND, REF, GRAVENBERCH, DOKU };
