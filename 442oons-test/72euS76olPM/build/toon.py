#!/usr/bin/env python3
"""Photo to 442oons-style flat cel face: grabcut the head, flatten to a few tones, clean ink lines.
  python3 toon.py <photo> <x0,y0,x1,y1 head box in photo px> <out.png> [tones]"""
import sys
import cv2
import numpy as np

src, box, out = sys.argv[1], [int(v) for v in sys.argv[2].split(',')], sys.argv[3]
K = int(sys.argv[4]) if len(sys.argv) > 4 else 5
im = cv2.imread(src)
x0, y0, x1, y1 = box
pad = 40
X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(im.shape[1], x1 + pad), min(im.shape[0], y1 + pad)
im = im[Y0:Y1, X0:X1]
im = cv2.resize(im, (int(im.shape[1] * 900 / im.shape[0]), 900), interpolation=cv2.INTER_CUBIC)
s = 900 / (Y1 - Y0)
rect = (int((x0 - X0) * s), int((y0 - Y0) * s), int((x1 - x0) * s), int((y1 - y0) * s))

# 1. cut the head and shoulders out
mask = np.zeros(im.shape[:2], np.uint8)
bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
cv2.grabCut(im, mask, rect, bg, fg, 6, cv2.GC_INIT_WITH_RECT)
m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
n, lab, st, _ = cv2.connectedComponentsWithStats(m)
if n > 1:
    m = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
m = cv2.GaussianBlur(m, (15, 15), 0); m = np.where(m > 127, 255, 0).astype(np.uint8)

# 2. flatten: strong edge-preserving smoothing, then k-means colours inside the mask
sm = im.copy()
for _ in range(6):
    sm = cv2.bilateralFilter(sm, 9, 40, 9)
sm = cv2.edgePreservingFilter(sm, flags=1, sigma_s=60, sigma_r=0.35)
pix = sm[m > 0].reshape(-1, 3).astype(np.float32)
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1.0)
_, labels, centers = cv2.kmeans(pix, K, None, crit, 4, cv2.KMEANS_PP_CENTERS)
flat = np.zeros_like(im); flat[m > 0] = centers[labels.flatten()].astype(np.uint8)
lab_img = np.full(im.shape[:2], -1, np.int32); lab_img[m > 0] = labels.flatten()
# remove speckles: majority filter on the label map
for _ in range(3):
    flat = cv2.medianBlur(flat, 9)
# saturate a touch, like flat cartoon paint
hsv = cv2.cvtColor(flat, cv2.COLOR_BGR2HSV).astype(np.float32)
hsv[..., 1] = np.clip(hsv[..., 1] * 1.15, 0, 255); hsv[..., 2] = np.clip(hsv[..., 2] * 1.06 + 6, 0, 255)
flat = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

# 3. ink: boundaries between flat regions (thin) + the silhouette (thick)
g = cv2.cvtColor(flat, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(g, 18, 50)
n, lab, st, _ = cv2.connectedComponentsWithStats(edges, connectivity=8)
keep = np.zeros_like(edges)
for i in range(1, n):
    if st[i, cv2.CC_STAT_AREA] > 60:
        keep[lab == i] = 255
inner = cv2.dilate(keep, np.ones((3, 3), np.uint8), iterations=1)
outline = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((11, 11), np.uint8))
ink = cv2.max(inner, outline)
ink = cv2.GaussianBlur(ink, (5, 5), 0)

res = np.full((*im.shape[:2], 4), 0, np.uint8)
res[..., :3] = flat; res[..., 3] = m
a = (ink.astype(np.float32) / 255)[..., None]
res[..., :3] = (res[..., :3] * (1 - a) + np.array([26, 26, 26]) * a).astype(np.uint8)
res[..., 3] = np.maximum(res[..., 3], (ink > 100).astype(np.uint8) * 255)
cv2.imwrite(out, res)
print(out, res.shape)
