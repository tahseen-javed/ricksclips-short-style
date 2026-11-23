#!/usr/bin/env python3
"""Assets for video 04 (the Vasa), drawn in code with the channel builders.
Reuses the video 02/03 cast code so mom, dad, tech and the Viking look identical, and adds four sailors, the
captain, a 1961 diver, shipworms, a gust cloud, the Vasa (one sticker, eight faces), a little Mediterranean
wreck, cards, a Stockholm skyline, an underwater backdrop, a deck sail and palms.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math
import numpy as np
from PIL import Image, ImageDraw
import assets_base as B
import gimli_assets as G
import viking_assets as V
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN = G.RED, G.GOLD, G.GREEN
BLUE, YEL, SAIL, WOOD, MAST = (44, 98, 178, 255), (252, 204, 56, 255), (248, 240, 220, 255), (162, 104, 64, 255), (108, 70, 44, 255)
SEA, FOAM, FIRE, FLAME = (120, 196, 236, 255), (240, 250, 255, 255), (250, 136, 40, 255), (255, 214, 72, 255)
dk = lambda c, f=0.78: tuple(int(v * f) for v in c[:3]) + (255,)
SK = [((246, 214, 190, 255), (222, 184, 160, 255)), ((218, 172, 134, 255), (190, 144, 108, 255)), ((176, 122, 90, 255), (148, 98, 70, 255))]
def P(sk, **kw): return dict(skin=SK[sk][0], sh=SK[sk][1], **kw)
NEW = {
    'sailA': P(0, hat=('knit', (214, 66, 60, 255)), base=(86, 118, 172, 255), shade=(64, 90, 138, 255), collar=1, sash=(214, 66, 60, 255)),
    'sailB': P(1, hat=('knit', (64, 146, 96, 255)), base=(200, 172, 122, 255), shade=(164, 136, 94, 255), beard=(104, 70, 46, 255), sash=BLUE),
    'sailC': P(0, hat=('knit', (62, 112, 196, 255)), base=(240, 236, 226, 255), shade=(204, 200, 190, 255), stripes=(206, 62, 62, 255), freck=1),
    'sailD': P(2, hat=('band', YEL), base=(92, 142, 98, 255), shade=(68, 110, 74, 255), stache=(52, 38, 32, 255), sash=YEL),
    'sailE': P(2, hat=('knit', (240, 140, 50, 255)), base=(126, 92, 160, 255), shade=(98, 70, 128, 255), collar=1),
    'sailF': P(1, hat=('band', (214, 66, 60, 255)), base=(236, 232, 222, 255), shade=(204, 200, 190, 255), stripes=BLUE, beard=(60, 44, 36, 255)),
    'capt':  P(0, hat=('cav', (54, 50, 74, 255)), base=(180, 42, 54, 255), shade=(140, 28, 42, 255), stache=(126, 84, 52, 255), goatee=(126, 84, 52, 255), coat=1, collar=1),
    'diver': P(0, hat=('diver', (222, 164, 76, 255)), base=(92, 100, 118, 255), shade=(68, 74, 90, 255), suit=1),
}


# ------------------------------------------------------------------ cast
def hat(d, k, hc):
    cx, lw = H['cx'], H['lw']
    if k == 'knit':                                          # floppy knitted sailor cap
        d.ellipse(cx + 158, 44, 42, 36, fill=hc, outline=LINE, width=lw)
        d.chord(cx + 10, 150, 204, 146, 180, 360, fill=hc, outline=LINE, width=lw)
        for x in range(cx - 140, cx + 170, 46):
            d.stroke([(x, 150 - 146 * max(0.0, 1 - ((x - cx - 10) / 204.0) ** 2) ** 0.5 + 18), (x, 132)], dk(hc, 0.86), 9)
        d.rrect(cx - 212, 118, cx + 212, 178, 30, fill=dk(hc), outline=LINE, width=lw)
    elif k == 'band':                                        # knotted bandana
        d.chord(cx, 160, 206, 132, 180, 360, fill=hc, outline=LINE, width=lw)
        for x, y in ((cx - 110, 104), (cx - 20, 66), (cx + 80, 94), (cx + 150, 134), (cx - 160, 142)): d.dot(x, y, 12, WHITE)
        for sg in (-1, 1): d.poly([(cx + 190, 150), (cx + 226, 170 + sg * 46), (cx + 204, 162 + sg * 26)], fill=hc, outline=LINE, width=10)
    else:                                                    # captain's cavalier hat with a white plume
        pl = bez((cx + 30, 100), (cx + 110, -6), (cx + 214, 8), (cx + 218, 118))
        d.stroke(pl, LINE, 62); d.stroke(pl, WHITE, 42)
        d.chord(cx, 124, 150, 116, 180, 360, fill=hc, outline=LINE, width=lw)
        d.ellipse(cx, 128, 222, 40, fill=hc, outline=LINE, width=lw); d.dot(cx, 72, 18, GOLD)


def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; k, hc = c['hat']
    if k == 'diver':                                         # brass diving helmet, face in the porthole
        d.rrect(cx - 44, 22, cx + 44, 74, 14, fill=dk(hc), outline=LINE, width=lw)
        d.ellipse(cx, cy, 224, 224, fill=hc, outline=LINE, width=lw); B.cel_shadow(d, cx, cy, 212, dk(hc, 0.86), hc)
        for a in range(0, 360, 30): d.dot(cx + 194 * math.cos(math.radians(a)), cy + 194 * math.sin(math.radians(a)), 10, (252, 224, 150, 255))
        d.ellipse(cx, cy + 4, 166, 166, fill=dk(hc, 0.72), outline=LINE, width=lw); d.ellipse(cx, cy + 4, 142, 142, fill=c['skin'], outline=LINE, width=10)
        bl, br = 98, 24
    else:
        d.ellipse(cx, cy, R, R, fill=c['skin'], outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, c['sh'], c['skin'])
        if 'beard' in c: d.chord(cx, cy + 36, R - 4, 168, 0, 180, fill=c['beard'], outline=LINE, width=lw)
        hat(d, k, hc); bl, br = 122, 30
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * bl, cy + 40, br, 16, fill=BLUSH)
    if c.get('freck'):
        for sg in (-1, 1):
            for dx, dy in ((-14, 0), (8, -10), (10, 12)): d.dot(cx + sg * 118 + dx, cy + 12 + dy, 5, (196, 120, 90, 255))
    B.eyes(d, L, Rr, expr, c['skin']); B.brows(d, L, Rr, expr, ey - 50)
    my = cy + 74
    for key in ('stache', 'beard'):
        if key in c:
            for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 30, my - 50), (cx + sg * 58, my - 40), (cx + sg * 66, my - 22)), c[key], 24)
            my += 12
    B.mouth(d, cx, my, expr)
    if 'goatee' in c: d.poly([(cx - 26, cy + 134), (cx + 26, cy + 134), (cx, cy + 192)], fill=c['goatee'], outline=LINE, width=8)
    if k == 'diver': d.arc(cx - 46, cy - 42, 92, 92, 200, 250, (255, 255, 255, 190), 12)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=c['base'])
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=c['base']); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if 'stripes' in c:
        for y in range(492, 800, 58): t.rect(x0, y, x1, y + 26, c['stripes'])
    if c.get('coat'):
        t.stroke([(230, 470), (230, 800)], LINE, 8)
        for y in (530, 590, 650, 710): t.dot(258, y, 13, GOLD)
    if c.get('collar'): t.poly([(140, 452), (320, 452), (300, 522), (230, 498), (160, 522)], fill=WHITE); t.stroke([(160, 522), (230, 498), (300, 522)], LINE, 6)
    if 'sash' in c: t.rect(x0, 664, x1, 708, c['sash']); t.dot(150, 690, 26, dk(c['sash']))
    if c.get('suit'):
        t.chord(230, 452, 176, 96, 0, 180, fill=(222, 164, 76, 255))
        for x in (110, 170, 290, 350): t.dot(x, 486 if x in (170, 290) else 466, 9, (252, 224, 150, 255))
        for x in (122, 298): t.rrect(x, 600, x + 40, 690, 10, fill=(64, 68, 80, 255), outline=LINE, width=6)
        t.rect(x0, 712, x1, 744, (70, 52, 40, 255))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


# ------------------------------------------------------------------ the Vasa: bow to the right, waterline at y 830 of 1100
SHEER = bez((300, 300), (330, 430), (420, 560), (560, 600)) + bez((560, 600), (800, 640), (1100, 620), (1340, 520))
HULL = [(130, 300)] + SHEER + bez((1340, 520), (1366, 720), (1290, 920), (1120, 1020)) + bez((1120, 1020), (860, 1090), (420, 1080), (200, 900))
def sy(x): return float(np.interp(x, [p[0] for p in SHEER], [p[1] for p in SHEER]))
PORTS = [(x, row) for row in (0, 1) for x in range(420, 1260, 96)]
def py(x, row): return sy(x) + (92 if row == 0 else 186)


def sail(d, x, y0, y1, w, col=SAIL):
    m = (y0 + y1) / 2
    pts = ([(x - w, y0), (x + w, y0)] + bez((x + w, y0), (x + w + 40, m), (x + w + 30, y1), (x + w + 18, y1)) +
           bez((x + w + 18, y1), (x + w * 0.3, y1 + 42), (x - w * 0.3, y1 + 42), (x - w - 18, y1)) + bez((x - w - 18, y1), (x - w - 30, y1), (x - w - 40, m), (x - w, y0)))
    d.poly(pts, fill=col, outline=LINE, width=10)
    for k in (-1, 0, 1): d.stroke([(x + k * w * 0.5, y0 + 12), (x + k * w * 0.56, y1 + 26)], dk(col, 0.9), 5)
    d.stroke([(x - w - 26, y0), (x + w + 26, y0)], LINE, 18); d.stroke([(x - w - 22, y0), (x + w + 22, y0)], MAST, 8)


def flame(d, x, y, s=1.0):
    d.poly([(x - 44 * s, y), (x - 26 * s, y - 96 * s), (x - 4 * s, y - 50 * s), (x + 16 * s, y - 140 * s), (x + 44 * s, y)], fill=FIRE, outline=LINE, width=8)
    d.poly([(x - 22 * s, y), (x - 8 * s, y - 48 * s), (x + 12 * s, y - 80 * s), (x + 24 * s, y)], fill=FLAME)


def vasa(st):
    d = Draw(1500, 1100); bare = st in ('wreck', 'raise', 'rot', 'museum'); wet = st in ('wreck', 'raise')
    wood = {'wreck': (118, 96, 72, 255), 'raise': (128, 100, 72, 255), 'rot': (128, 120, 98, 255), 'museum': (176, 116, 70, 255)}.get(st, WOOD)
    gold = (156, 136, 84, 255) if wet or st == 'rot' else GOLD
    tops = (330, 250, 360) if wet else (300, 170, 420) if st == 'rot' else (150, 36, 110)
    if not wet and st != 'rot':
        for a, b in (((800, 40), (1340, 520)), ((800, 40), (300, 300)), ((1130, 110), (1490, 420)), ((450, 150), (130, 300)), ((1130, 110), (800, 300))):
            d.stroke([a, b], LINE, 5)
    bs = (1420, 476) if wet or st == 'rot' else (1490, 420)
    d.stroke([(1330, 528), bs], LINE, 30); d.stroke([(1330, 528), bs], MAST, 18)
    for x, top in zip((450, 800, 1130), tops):
        d.stroke([(x, sy(x) + 20), (x, top)], LINE, 36); d.stroke([(x, sy(x) + 20), (x, top + 6)], MAST, 22)
        if wet or st == 'rot': d.poly([(x - 18, top + 4), (x - 8, top - 28), (x + 2, top + 2), (x + 12, top - 20), (x + 18, top + 4)], fill=MAST, outline=LINE, width=6)
        elif st == 'museum':
            for yy in (top + 70, top + 210): d.stroke([(x - 150, yy), (x + 150, yy)], LINE, 16); d.stroke([(x - 146, yy), (x + 146, yy)], MAST, 7)
    if not bare:
        burnt = (92, 82, 78, 255) if st == 'burn' else SAIL
        sail(d, 800, 70, 230, 120, burnt); sail(d, 800, 270, 470, 175); sail(d, 1130, 140, 270, 100); sail(d, 1130, 300, 450, 150, burnt); sail(d, 450, 180, 330, 110)
        d.stroke([(150, 304), (112, 126)], LINE, 10); d.rect(112, 128, 262, 222, BLUE); d.rect(150, 128, 174, 222, YEL); d.rect(112, 164, 262, 186, YEL)
        d.rrect(112, 128, 262, 222, 4, outline=LINE, width=7)
        for x, top in ((800, 36), (1130, 106)): d.poly([(x, top), (x + 210, top + 18), (x, top + 34)], fill=BLUE, outline=LINE, width=6); d.stroke([(x + 4, top + 17), (x + 150, top + 18)], YEL, 7)
    m = Draw(1500, 1100); m.poly(HULL, fill=WHITE); d.poly(HULL, fill=wood); t = Draw(1500, 1100)
    t.rect(0, 830, 1500, 1100, dk(wood, 0.62))
    for off in (64, 140, 236): t.stroke([(x, sy(x) + off) for x in range(130, 1380, 20)], dk(wood, 0.8), 12)
    t.rrect(146, 318, 290, 640, 18, fill=gold)
    for x, y in ((184, 384), (252, 384), (184, 476), (252, 476)): t.rrect(x - 22, y - 28, x + 22, y + 28, 8, fill=(66, 56, 78, 255))
    t.dot(218, 572, 34, dk(gold, 0.85)); t.stroke(bez((300, 312), (380, 470), (480, 560), (560, 590)), gold, 14)
    for x, row in PORTS:
        y = py(x, row)
        if not wet and st != 'rot': t.rect(x - 27, y - 66, x + 27, y - 30, RED); t.rect(x - 27, y - 66, x + 27, y - 60, LINE)
        t.rrect(x - 22, y - 22, x + 22, y + 22, 6, fill=LINE)
    if wet or st == 'rot':
        rng = np.random.RandomState(7 if wet else 3)
        for _ in range(26): t.dot(rng.uniform(220, 1300), rng.uniform(560, 1000), rng.uniform(10, 30), (96, 104, 74, 255) if st == 'rot' else (92, 82, 66, 255))
    d.clip(t, m); d.poly(HULL, outline=LINE, width=14)
    d.poly([(1330, 522), (1446, 508), (1462, 540), (1350, 604)], fill=gold, outline=LINE, width=10)
    d.dot(1450, 492, 40, gold); d.ellipse(1450, 492, 40, 40, outline=LINE, width=9); d.dot(1462, 484, 7, LINE)
    for k in range(7): a = math.radians(150 + k * 30); d.dot(1450 + 46 * math.cos(a), 492 + 46 * math.sin(a), 13, dk(gold, 0.85))
    if wet:                                                  # seaweed, and water running off when she comes up
        for x in range(260, 1300, 115): d.stroke(bez((x, sy(x) + 70), (x + 20, sy(x) + 140), (x - 16, sy(x) + 200), (x + 8, sy(x) + 250)), (70, 140, 80, 255), 12)
        if st == 'raise':
            for x in range(230, 1320, 52): y = 840 + (x * 7) % 60; d.stroke([(x, y), (x, y + 46)], SEA, 9); d.dot(x, y + 64, 9, SEA)
    if st == 'rot':
        for x, y in ((520, 720), (760, 760), (980, 700), (1180, 740), (330, 560)): d.ellipse(x, y, 34, 24, fill=LINE)
    if st == 'flood':
        for x in range(420, 1260, 96):
            y = py(x, 1); d.ellipse(x, y + 4, 38, 26, fill=SEA, outline=LINE, width=6)
            d.stroke([(x - 34, y + 34), (x - 16, y + 6), (x + 4, y + 26), (x + 24, y + 2)], FOAM, 9)
        for x in range(260, 1330, 64): d.dot(x, 826 + (x * 13) % 18, 22, FOAM)
    if st == 'war':
        for x in range(420, 1260, 192):
            y = py(x, 0); d.dot(x + 6, y + 6, 26, FLAME)
            for dx, dy, r in ((-40, 34, 42), (10, 46, 52), (60, 30, 40)): d.dot(x + dx, y + dy, r + 7, LINE)
            for dx, dy, r in ((-40, 34, 42), (10, 46, 52), (60, 30, 40)): d.dot(x + dx, y + dy, r, (240, 240, 246, 255))
    if st == 'burn':
        for x in range(330, 1330, 120): flame(d, x, sy(x) + 30, 1.0 + 0.3 * ((x // 120) % 2))
        for x, y in ((800, 300), (1130, 330), (800, 150)): flame(d, x, y, 0.9)
    return d.out()


# ------------------------------------------------------------------ small characters and stickers
def worm(st):
    d = Draw(420, 560); col = (204, 228, 248, 255) if st == 'cold' else (250, 204, 190, 255)
    sp = bez((210, 560), (130, 480), (330, 420), (250, 330)) if st == 'sad' else bez((210, 560), (110, 470), (320, 360), (210, 250))
    d.stroke(sp, LINE, 124); d.stroke(sp, col, 100)
    for i in (9, 15, 21): d.arc(sp[i][0], sp[i][1], 46, 18, 20, 160, dk(col, 0.86), 7)
    hx, hy = sp[-1]
    for sg in (-1, 1):                                       # the two tiny shells it drills with
        d.ellipse(hx + sg * 64, hy - 34, 50, 40, fill=(248, 238, 214, 255), outline=LINE, width=9)
        for r in (14, 28): d.arc(hx + sg * 64, hy - 22, r * 1.4, r, 200, 340, (214, 192, 150, 255), 5)
    d.ellipse(hx, hy, 84, 76, fill=col, outline=LINE, width=10)
    for sg in (-1, 1):
        d.ellipse(hx + sg * 32, hy - 4, 22, 27, fill=LINE); d.dot(hx + sg * 32 + 7, hy - 13, 8, WHITE); d.ellipse(hx + sg * 56, hy + 24, 15, 9, fill=BLUSH)
    if st == 'munch':
        d.ellipse(hx, hy + 34, 28, 24, fill=LINE); d.rect(hx - 16, hy + 12, hx + 16, hy + 22, WHITE)
        for dx, dy in ((-80, 50), (70, 64), (96, 20), (-100, 6)): d.rect(hx + dx, hy + dy, hx + dx + 18, hy + dy + 14, (196, 140, 84, 255))
    elif st == 'cold':
        d.stroke([(hx - 24, hy + 32), (hx - 12, hy + 24), (hx, hy + 32), (hx + 12, hy + 24), (hx + 24, hy + 32)], LINE, 6)
        d.rrect(hx - 90, hy + 58, hx + 90, hy + 88, 14, fill=RED, outline=LINE, width=7); d.rrect(hx + 40, hy + 70, hx + 72, hy + 150, 12, fill=RED, outline=LINE, width=7)
        for sg in (-1, 1): d.stroke([(hx + sg * 112, hy - 30), (hx + sg * 124, hy - 10), (hx + sg * 112, hy + 10)], LINE, 6)
        d.dot(hx + 20, hy - 74, 14, WHITE); d.ellipse(hx + 20, hy - 74, 14, 14, outline=LINE, width=4)
    elif st == 'sad':
        d.arc(hx, hy + 46, 22, 14, 200, 340, LINE, 7); d.ellipse(hx + 40, hy + 34, 9, 14, fill=SEA, outline=LINE, width=4)
    else:
        d.chord(hx, hy + 24, 24, 20, 0, 180, fill=LINE)
    return d.out()


def boat(eaten):
    d = Draw(760, 380); hull = bez((40, 170), (120, 360), (600, 380), (720, 190)) + [(720, 190), (40, 170)]
    d.stroke([(380, 180), (300, 20)], LINE, 26); d.stroke([(380, 180), (300, 26)], MAST, 14)
    d.poly(hull, fill=(150, 104, 70, 255), outline=LINE, width=12)
    for k in range(3): d.stroke([(70 + k * 10, 210 + k * 44), (690 - k * 30, 220 + k * 40)], (118, 80, 54, 255), 8)
    if eaten:
        rng = np.random.RandomState(2)
        for _ in range(14): d.ellipse(rng.uniform(110, 650), rng.uniform(200, 320), rng.uniform(12, 26), rng.uniform(10, 18), fill=LINE)
        for x, y in ((210, 240), (460, 290), (600, 230)): d.dot(x, y, 22, (250, 204, 190, 255)); d.ellipse(x, y, 22, 22, outline=LINE, width=5); d.dot(x - 7, y - 3, 5, LINE); d.dot(x + 7, y - 3, 5, LINE)
    return d.out()


def gust():
    d = Draw(780, 420); bl = [(170, 250, 110), (290, 190, 130), (430, 200, 120), (520, 260, 100), (330, 290, 120), (120, 310, 70)]
    for x, y, r in bl: d.dot(x, y, r + 11, LINE)
    for x, y, r in bl: d.dot(x, y, r, (248, 250, 255, 255))
    for x in (290, 390): d.arc(x, 236, 24, 16, 200, 340, LINE, 9)
    for x in (250, 450): d.ellipse(x, 290, 30, 18, fill=BLUSH)
    d.ellipse(560, 262, 30, 26, fill=LINE, outline=LINE, width=4)
    for y, l in ((190, 150), (262, 190), (334, 140)): d.stroke([(612, y), (612 + l, y - 8)], (170, 206, 236, 255), 14)
    return d.out()


def sun():
    d = Draw(440, 440)
    for k in range(12): a = math.radians(k * 30); d.stroke([(220 + 150 * math.cos(a), 220 + 150 * math.sin(a)), (220 + 205 * math.cos(a), 220 + 205 * math.sin(a))], (250, 170, 40, 255), 24)
    d.ellipse(220, 220, 140, 140, fill=FLAME, outline=LINE, width=12)
    for sg in (-1, 1): d.rrect(220 + sg * 52 - 44, 172, 220 + sg * 52 + 44, 222, 16, fill=LINE)
    d.stroke([(208, 186), (232, 186)], LINE, 10); d.chord(220, 262, 52, 40, 0, 180, fill=LINE); d.ellipse(150, 262, 22, 13, fill=BLUSH); d.ellipse(290, 262, 22, 13, fill=BLUSH)
    return d.out()


def gull():
    d = Draw(360, 220)
    for sg in (-1, 1): d.poly(bez((180, 120), (180 + sg * 60, 30), (180 + sg * 130, 40), (180 + sg * 170, 90)) + [(180 + sg * 120, 100)], fill=WHITE, outline=LINE, width=9)
    d.ellipse(180, 128, 46, 30, fill=WHITE, outline=LINE, width=9); d.poly([(220, 124), (262, 134), (220, 142)], fill=(250, 170, 40, 255), outline=LINE, width=5); d.dot(204, 118, 7, LINE)
    return d.out()


def fish():
    d = Draw(320, 200); d.poly([(60, 100), (10, 40), (10, 160)], fill=(250, 150, 50, 255), outline=LINE, width=9)
    d.ellipse(170, 100, 120, 76, fill=(255, 196, 70, 255), outline=LINE, width=10)
    for x in (140, 180): d.arc(x, 100, 30, 60, 300, 420, (240, 140, 50, 255), 9)
    d.dot(240, 84, 22, WHITE); d.ellipse(240, 84, 22, 22, outline=LINE, width=6); d.dot(246, 84, 10, LINE); d.ellipse(226, 122, 14, 8, fill=BLUSH)
    return d.out()


def bubbles():
    d = Draw(300, 480)
    for x, y, r in ((150, 420, 40), (100, 320, 30), (190, 250, 34), (120, 160, 24), (180, 90, 20), (130, 30, 14)):
        d.ellipse(x, y, r, r, fill=(200, 236, 252, 200), outline=LINE, width=6); d.dot(x - r * 0.35, y - r * 0.35, r * 0.25, WHITE)
    return d.out()


def splash():
    d = Draw(620, 400)
    for a in range(-80, 81, 20):
        r = math.radians(a - 90); x, y = 310 + 250 * math.cos(r), 380 + 330 * math.sin(r)
        d.stroke([(310 + 60 * math.cos(r), 380), (x, y)], LINE, 44); d.stroke([(310 + 60 * math.cos(r), 380), (x, y)], SEA, 28); d.dot(x, y - 20, 18, FOAM)
    d.ellipse(310, 380, 290, 46, fill=FOAM, outline=LINE, width=10)
    return d.out()


def snow():
    d = Draw(700, 560); rng = np.random.RandomState(4)
    for _ in range(16):
        x, y, r = rng.uniform(40, 660), rng.uniform(40, 520), rng.uniform(14, 26)
        for col, w in ((LINE, 14), ((236, 246, 255, 255), 8)):
            for k in range(3): a = math.radians(k * 60); d.stroke([(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], col, w)
    return d.out()


def coldsalt():
    d = G.card(900, 420)
    d.rrect(84, 60, 124, 200, 20, fill=WHITE, outline=LINE, width=9); d.rect(94, 150, 114, 196, BLUE); d.dot(104, 210, 30, BLUE); d.ellipse(104, 210, 30, 30, outline=LINE, width=9)
    d.text(520, 140, "COLD", 92, BLUE, stroke=6, stroke_fill=LINE)
    d.rrect(72, 270, 136, 370, 18, fill=WHITE, outline=LINE, width=9); d.chord(104, 272, 32, 30, 180, 360, fill=(170, 176, 190, 255), outline=LINE, width=8)
    for x in (92, 104, 116): d.dot(x, 262, 4, LINE)
    d.text(520, 316, "BARELY SALTY", 68, LINE); return d.out()


# ------------------------------------------------------------------ props, textures, backdrops
def deck_sail(path): d = Draw(1000, 760); sail(d, 500, 60, 640, 400); d.out().save(path)


def palm(path):
    d = Draw(800, 1100); tr = bez((420, 1090), (380, 800), (330, 500), (400, 300))
    d.stroke(tr, LINE, 70); d.stroke(tr, (176, 124, 78, 255), 50)
    for i in range(3, len(tr) - 2, 3): d.arc(tr[i][0], tr[i][1], 24, 8, 0, 180, (130, 88, 54, 255), 6)
    for a in (-170, -132, -96, -60, -24, 12):
        r = math.radians(a); ex, ey = 400 + 340 * math.cos(r), 330 + 200 * math.sin(r) + 120; mx, my = 400 + 170 * math.cos(r), 300 + 110 * math.sin(r) - 30
        d.poly(bez((400, 300), (mx, my - 40), (ex, ey - 70), (ex, ey)) + bez((ex, ey), (ex, ey - 20), (mx, my + 30), (400, 300)), fill=(84, 170, 86, 255), outline=LINE, width=10)
    for x, y in ((376, 330), (420, 336), (398, 360)): d.dot(x, y, 22, (120, 80, 50, 255))
    d.out().save(path)


def under(path, W=2000, Hh=1000):
    y = np.linspace(0, 1, Hh)[:, None, None]; top, bot = np.array([140, 220, 230]), np.array([56, 140, 182])
    im = Image.fromarray((top + (bot - top) * y * np.ones((1, W, 1))).astype(np.uint8)); dr = ImageDraw.Draw(im, 'RGBA')
    for k in range(7): x = 120 + k * 300; dr.polygon([(x, 0), (x + 120, 0), (x + 430, Hh), (x + 260, Hh)], fill=(255, 255, 255, 30))
    for k in range(30):
        x, n = (k * 397) % W, 6 + (k * 5) % 9; dr.line([(x + 16 * math.sin(j * 0.9 + k), Hh - j * 26) for j in range(n)], fill=(52, 128, 130, 255), width=18)
    im.save(path)


def stockholm(path):
    G.sky(path); im = Image.open(path).convert('RGB'); dr = ImageDraw.Draw(im); W = im.size[0]; base, x, k = 990, 0, 0
    while x < W:
        w, h = 60 + (k * 37) % 70, 70 + (k * 53) % 90; col = [(150, 160, 188), (172, 162, 180), (140, 152, 180), (178, 174, 190)][k % 4]
        dr.rectangle([x, base - h, x + w, base], fill=col); dr.polygon([(x - 4, base - h), (x + w / 2, base - h - 40), (x + w + 4, base - h)], fill=(122, 130, 160))
        if k % 7 == 3: dr.polygon([(x + w / 2 - 12, base - h - 30), (x + w / 2, base - h - 190), (x + w / 2 + 12, base - h - 30)], fill=(112, 120, 150))
        x += w + 4; k += 1
    dr.rectangle([0, base, W, 1080], fill=(84, 138, 190)); im.save(path, quality=92)


def skyplane(path, top, bot, hills=None, W=1800, Hh=800):
    y = np.linspace(0, 1, Hh)[:, None, None]; top, bot = np.array(top), np.array(bot)
    im = Image.fromarray((top + (bot - top) * y ** 1.4 * np.ones((1, W, 1))).astype(np.uint8)); dr = ImageDraw.Draw(im)
    if hills: dr.polygon([(x, Hh - 110 - 60 * abs(math.sin(x / 260.0 + 1))) for x in range(0, W + 1, 20)] + [(W, Hh), (0, Hh)], fill=hills)
    im.save(path)


def tex_water(path, n=512):
    p, q = G.periodic(n, 11, 6), G.periodic(n, 3, 12); a = np.zeros((n, n, 3)) + [60, 134, 200]
    a += (p[..., None] - 0.5) * 36 + (q[..., None] - 0.5) * 18 + (np.clip(p - 0.74, 0, 1) * 4)[..., None] * [110, 120, 110]
    G.save_tex(a, path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = G.head, G.body              # the same faces as videos 02 and 03
    for ch in ('mom', 'dad', 'tech'): layers, faces = B.build_human(ch); items.append((ch, faces['happy']))
    B.human_head, B.human_body = V.head, V.body
    layers, faces = B.build_human('vik'); items.append(('vik', faces['happy']))
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' happy', faces['happy']), (ch + ' shocked', faces['shocked'])]
    multi = dict(vasa={s: vasa(s) for s in ('default', 'flood', 'wreck', 'raise', 'museum', 'war', 'rot', 'burn')},
                 worm={s: worm(s) for s in ('default', 'munch', 'cold', 'sad')}, boat={'default': boat(False), 'eaten': boat(True)})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    B.sparkle(Pp('sparkle.png'))
    cards = dict(cal28=G.cal_card("AUG 10", "1628", ""), cal61=G.cal_card("RAISED", "1961", ""), vtag=V.wtag("VASA", 460, BLUE),
                 decks=V.big_card("2", "GUN DECKS", RED, 560), one=V.wtag("OTHERS: 1", 600, (110, 116, 136, 255)), x30=V.wtag("×30", 360, RED),
                 test=V.wtag("STABILITY TEST", 860, (126, 70, 140, 255), 70), stop=B.sticker_burst("STOP!"), anyway=V.wtag("ANYWAY!", 560, RED),
                 mile=V.wtag("< 1 MILE", 520, BLUE), whole=V.wtag("ALMOST WHOLE!", 820, GREEN, 70), ques=B.sticker_mark('?', GOLD), excl=B.sticker_mark('!', RED),
                 warm=V.wtag("WARM + SALTY", 760, (232, 118, 44, 255), 70), clams=V.wtag("TINY CLAMS", 640, (206, 96, 140, 255)), nom=B.sticker_burst("NOM!"),
                 med=V.wtag("MEDITERRANEAN", 860, (232, 118, 44, 255), 66), y30=V.big_card("30", "YEARS", RED, 520), baltic=V.wtag("BALTIC", 480, BLUE),
                 coldsalt=coldsalt(), nope=B.sticker_burst("NOPE!", (150, 206, 255, 255)), y333=V.big_card("333", "YEARS", BLUE, 600),
                 untouched=V.wtag("UNTOUCHED", 700, GREEN), p98=V.big_card("98%", "ORIGINAL", GREEN, 600), whatif=V.wtag("WHAT IF?", 560, (126, 70, 140, 255)),
                 poof=B.sticker_poof(), million=V.big_card("1M+", "VISITORS A YEAR", GOLD, 760), worst=V.wtag("WORST LAUNCH", 780, RED, 74),
                 hidden=V.wtag("HIDDEN!", 520, GREEN), sank=V.wtag("SANK = SAVED?!", 880, RED, 70), hearts=G.hearts(), gust=gust(), sun=sun(),
                 gull=gull(), fish=fish(), bubbles=bubbles(), splash=splash(), snow=snow(), sparkle=Image.open(Pp('sparkle.png')).convert('RGBA'))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); tex_water(T('water.jpg'))
    stockholm(os.path.join(ROOT, 'bg', 'stockholm.jpg'))
    deck_sail(Pp('sail.png')); palm(Pp('palm.png')); under(Pp('under.png'))
    skyplane(Pp('skyws.png'), (96, 170, 236), (255, 226, 170), (226, 196, 140)); skyplane(Pp('skycb.png'), (170, 196, 222), (236, 242, 248), (226, 236, 246))
    skyplane(Pp('skywr.png'), (138, 140, 172), (204, 194, 204))
    for n in ('sail', 'palm', 'under', 'skyws', 'skycb', 'skywr'): items.append((n, Image.open(Pp(n + '.png'))))
    items.append(('backdrop', Image.open(os.path.join(ROOT, 'bg', 'stockholm.jpg'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
