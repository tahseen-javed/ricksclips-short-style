#!/usr/bin/env python3
"""Assets for video 14 (Mars Climate Orbiter, 1998-99: perfect math, wrong units), drawn in code.
New cute cast: the navigator (headset, round glasses, blue sweater), the second navigator (bob hair, headset, teal),
the NASA boss (bald, moustache, grey suit, red tie), the Lockheed engineer (blond quiff, orange sweater).
Hero prop: the cute gold ORBITER (happy / shocked / burning) - it recurs in almost every set.  Other props: the rocket
(on the pad / firing), the radio dish (hopeful / sad), the radar screen, the calculator, the clipboard, the thrust sheet
with the missing label, the 100 % test paper.  Thirteen sets, each its own palette: CR control room at night (navy + amber),
SP deep space with a giant Mars (violet + red), LP launch pad at dawn (pink + gold), TR the cruise (teal), CB chalkboard
office (warm cream + green), NV navigation room (amber CRT), MT meeting at dusk (purple + peach), MA Mars arrival (orange +
blue halo), BN the burn (fire red), DS dish at night (moon blue), UN split room (orange Colorado | blue California),
LB the desk with the missing label (sepia), QN sunny classroom (yellow).
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import corrigan_assets as CA
import catseyes_assets as CE
import lordgta_assets as LA
from assets_base import Draw, LINE, WHITE, H

ROOT = B.ROOT; RED, GOLD = LA.RED, LA.GOLD
dk, glow, plaque, stamp, neon = LA.dk, CE.glow, LA.plaque, LA.stamp, LA.neon
ORNG, TEAL, YEL, SKYB, GOLDL, LIME, PINK = (250, 140, 50, 255), (40, 170, 150, 255), (255, 206, 50, 255), (70, 150, 230, 255), (255, 214, 96, 255), (120, 230, 90, 255), (255, 90, 160, 255)
WT, MARS, CYAN = (250, 250, 245, 255), (226, 104, 56, 255), (120, 220, 255, 255)
LA.NEW.update({
    'nav': dict(sk=1, style='curly', hair=(60, 40, 30, 255), suit=SKYB, shade=(50, 110, 190, 255), body='sweater', glasses=1, freck=1, headset=1),
    'nav2': dict(sk=2, style='bob', hair=(30, 24, 30, 255), suit=TEAL, shade=(30, 136, 120, 255), body='cardigan', band=YEL, headset=1),
    'boss': dict(sk=0, style='bald', hair=(120, 110, 104, 255), suit=(120, 128, 146, 255), shade=(96, 104, 122, 255), body='suit', tie=RED, stache=(110, 90, 80, 255)),
    'lock': dict(sk=0, style='quiff', hair=(240, 200, 90, 255), suit=ORNG, shade=(214, 110, 36, 255), body='sweater', stubble=1),
})


def head(char, expr):
    im = LA.head(char, expr); c = LA.NEW[char]
    if c.get('headset'):                                     # headset: band over the head, ear cup, mic boom
        d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']
        d.arc(cx, cy, R + 14, R + 14, 196, 344, LINE, 30); d.arc(cx, cy, R + 14, R + 14, 198, 342, (90, 96, 110, 255), 14)
        for sg in (-1, 1): d.rrect(cx + sg * (R + 6) - 30, cy - 10, cx + sg * (R + 6) + 30, cy + 90, 22, fill=(60, 64, 76, 255), outline=LINE, width=10)
        d.stroke([(cx - R - 6, cy + 70), (cx - R + 40, cy + 150), (cx - 70, cy + 170)], LINE, 14); d.dot(cx - 66, cy + 170, 20, (60, 64, 76, 255))
        im.alpha_composite(d.out())
    return im


def body(char):
    im = LA.body(char); d = Draw(im.width, im.height)
    if char in ('nav', 'nav2', 'lock'):                      # ID badge on a lanyard
        d.stroke([(200, 470), (250, 590), (300, 470)], (220, 60, 60, 255) if char != 'lock' else (60, 90, 200, 255), 8)
        d.rrect(222, 580, 282, 660, 8, fill=WT, outline=LINE, width=6); d.rect(230, 592, 274, 612, (70, 150, 230, 255) if char != 'lock' else ORNG)
    im.alpha_composite(d.out()); return im


# ------------------------------------------------------------------ hero props
def eyes(d, cx, cy, sz, face):
    sh = face in ('shocked', 'burn')
    for sg in (-1, 1):
        d.ellipse(cx + sg * sz, cy, sz * 0.44, sz * (0.62 if sh else 0.54), fill=WHITE, outline=LINE, width=10)
        d.dot(cx + sg * sz + 6, cy + 10, sz * (0.16 if sh else 0.22), LINE); d.dot(cx + sg * sz + 14, cy - 6, sz * 0.07, WHITE)
        d.ellipse(cx + sg * sz * 1.75, cy + sz * 0.9, sz * 0.38, sz * 0.22, fill=(255, 130, 130, 190))
    if sh: d.ellipse(cx, cy + sz * 1.3, sz * 0.4, sz * 0.5, fill=(120, 30, 40, 255), outline=LINE, width=10)
    elif face == 'sad': d.arc(cx, cy + sz * 1.6, sz * 0.5, sz * 0.32, 200, 340, LINE, 12)
    else: d.chord(cx, cy + sz * 1.05, sz * 0.7, sz * 0.55, 0, 180, fill=(120, 30, 40, 255), outline=LINE, width=12)


def orbiter(face='default'):                                 # gold-foil box, one blue solar wing, white dish, thrusters
    d = Draw(1400, 1000); cx, cy = 900, 520
    if face == 'burn':                                       # fire shell + trail to the upper right
        for k, (c, r) in enumerate((((255, 90, 30, 200), 460), ((255, 160, 40, 220), 400), ((255, 230, 110, 230), 330))):
            d.ellipse(cx, cy + 40, r, r * 0.92, fill=c)
        for k in range(6): d.poly([(cx + 120 + k * 30, cy - 300 + k * 40), (1390, 20 + k * 60), (1390, 70 + k * 60)], fill=(255, 200 - k * 20, 60, 200))
    d.stroke([(cx - 250, cy), (cx - 420, cy)], LINE, 30); d.stroke([(cx - 250, cy), (cx - 420, cy)], (190, 190, 200, 255), 14)
    d.rrect(30, cy - 230, cx - 400, cy + 200, 16, fill=(40, 70, 170, 255), outline=LINE, width=16)
    for x in range(110, cx - 400, 80): d.stroke([(x, cy - 222), (x, cy + 192)], (110, 160, 240, 255), 6)
    for y in range(cy - 150, cy + 200, 80): d.stroke([(38, y), (cx - 408, y)], (110, 160, 240, 255), 6)
    d.stroke([(cx + 80, cy - 220), (cx + 120, cy - 330)], LINE, 22); d.stroke([(cx + 80, cy - 220), (cx + 120, cy - 330)], (200, 200, 210, 255), 10)
    d.ellipse(cx + 140, cy - 360, 190, 80, fill=WT, outline=LINE, width=14); d.ellipse(cx + 140, cy - 366, 140, 52, fill=(220, 226, 236, 255)); d.dot(cx + 140, cy - 370, 18, (255, 90, 80, 255))
    for x in (cx - 130, cx + 130): d.poly([(x - 46, cy + 230), (x + 46, cy + 230), (x + 70, cy + 310), (x - 70, cy + 310)], fill=(120, 124, 136, 255), outline=LINE, width=12)
    d.rrect(cx - 250, cy - 230, cx + 250, cy + 240, 36, fill=(240, 186, 60, 255), outline=LINE, width=18)
    for k in range(7): x = cx - 210 + k * 70; d.stroke([(x, cy - 200), (x + 30, cy - 120), (x - 10, cy - 40)], (255, 226, 130, 255), 8)
    d.rrect(cx - 250, cy + 150, cx + 250, cy + 240, 30, fill=(210, 150, 40, 255), outline=LINE, width=14)
    eyes(d, cx, cy - 20, 92, face)
    return d.out()


def rocket(face='default'):                                  # teal Delta-style rocket, white boosters, stand or flame below
    d = Draw(560, 1700); cx = 280
    if face == 'fire':
        for c, w, h in (((255, 120, 40, 230), 200, 520), ((255, 200, 70, 240), 140, 420), ((255, 250, 200, 255), 70, 300)): d.poly([(cx - w, 1180), (cx + w, 1180), (cx, 1180 + h)], fill=c)
        for x, y, r in ((90, 1600, 100), (470, 1610, 100), (280, 1640, 90), (160, 1520, 70), (400, 1530, 70)): d.ellipse(x, y, r, r * 0.7, fill=(250, 246, 240, 240), outline=LINE, width=8)
    else:
        for x in (150, 410): d.poly([(x - 20, 1180), (x + 20, 1180), (x + 40 * (1 if x > cx else -1), 1690), (x + 40 * (1 if x > cx else -1) - 30, 1690)], fill=(150, 60, 50, 255), outline=LINE, width=8)
        d.rect(100, 1640, 460, 1690, (110, 110, 120, 255))
    for x in (110, 450): d.rrect(x - 40, 760, x + 40, 1180, 30, fill=WT, outline=LINE, width=10); d.poly([(x - 40, 770), (x, 690), (x + 40, 770)], fill=WT, outline=LINE, width=10)
    d.rrect(cx - 110, 260, cx + 110, 1190, 30, fill=(60, 170, 160, 255), outline=LINE, width=14); d.rect(cx - 100, 560, cx + 100, 600, WT); d.rect(cx - 100, 980, cx + 100, 1010, WT)
    d.poly([(cx - 110, 280), (cx, 20), (cx + 110, 280)], fill=WT, outline=LINE, width=14)
    d.ellipse(cx, 420, 50, 50, fill=(170, 220, 255, 255), outline=LINE, width=10); d.dot(cx + 14, 406, 12, WHITE)
    return d.out()


def dish(face='default'):                                    # deep-space dish on a pedestal with a little face
    d = Draw(1100, 1100); cx = 550
    d.poly([(cx - 200, 1090), (cx + 200, 1090), (cx + 110, 640), (cx - 110, 640)], fill=(210, 214, 226, 255), outline=LINE, width=14)
    eyes(d, cx, 820, 62, face)
    d.ellipse(cx, 420, 470, 250, fill=(236, 240, 248, 255), outline=LINE, width=16); d.ellipse(cx, 400, 400, 196, fill=(196, 204, 220, 255))
    for a in (-0.7, 0, 0.7): d.stroke([(cx + 380 * math.sin(a), 420 - 150 * math.cos(a)), (cx, 160)], LINE, 10)
    d.ellipse(cx, 150, 50, 50, fill=(150, 156, 170, 255), outline=LINE, width=10); d.dot(cx, 92, 16, (255, 80, 70, 255))
    return d.out()


def radar():                                                 # amber CRT plot: planned path high (green), real path drifting low (red)
    d = Draw(1200, 900); d.rrect(20, 20, 1180, 880, 60, fill=(214, 200, 170, 255), outline=LINE, width=18)
    d.rrect(90, 90, 1110, 720, 40, fill=(16, 34, 20, 255), outline=LINE, width=12)
    for x in range(150, 1100, 120): d.stroke([(x, 100), (x, 710)], (40, 90, 50, 255), 4)
    for y in range(160, 710, 110): d.stroke([(100, y), (1100, y)], (40, 90, 50, 255), 4)
    d.ellipse(960, 440, 90, 90, fill=MARS, outline=LINE, width=8)
    pts = [(160 + u * 760, 620 - 440 * math.sin(u * 1.4)) for u in np.linspace(0, 1, 12)]
    for k in range(0, 11, 2): d.stroke([pts[k], pts[k + 1]], (120, 255, 140, 255), 12)
    lo = [(160 + u * 790, 620 - 440 * math.sin(u * 1.4) + 260 * u ** 2.2) for u in np.linspace(0, 1, 14)]
    d.stroke(lo, (255, 90, 70, 255), 14); d.poly([(lo[-1][0] + 10, lo[-1][1] + 50), (lo[-1][0] - 40, lo[-1][1] - 10), (lo[-1][0] + 50, lo[-1][1] - 20)], fill=(255, 90, 70, 255))
    for x in (200, 300, 400): d.dot(x, 800, 22, (90, 90, 90, 255))
    d.dot(1030, 800, 20, (255, 170, 60, 255)); return d.out()


def calc():                                                  # calculator with the long decimal on the LCD
    d = Draw(640, 980); d.rrect(20, 20, 620, 960, 60, fill=(70, 76, 96, 255), outline=LINE, width=18)
    d.rrect(70, 80, 570, 290, 24, fill=(180, 210, 150, 255), outline=LINE, width=10); d.text(320, 190, '4.4482216', 92, (30, 44, 30, 255))
    for r in range(4):
        for c in range(4): d.rrect(80 + c * 125, 350 + r * 145, 180 + c * 125, 450 + r * 145, 20, fill=ORNG if c == 3 else (220, 224, 236, 255), outline=LINE, width=8)
    return d.out()


def clip():                                                  # clipboard: big green ticks + 100 %
    d = Draw(700, 900); d.rrect(20, 40, 680, 880, 40, fill=(190, 140, 80, 255), outline=LINE, width=16); d.rrect(70, 110, 630, 840, 16, fill=WT, outline=LINE, width=8)
    d.rrect(230, 10, 470, 110, 24, fill=(160, 164, 176, 255), outline=LINE, width=12)
    for k in range(3): y = 220 + k * 150; d.stroke([(120, y), (170, y + 50), (260, y - 50)], (40, 180, 80, 255), 24); d.rect(300, y - 10, 580, y + 10, (170, 170, 180, 255))
    d.text(350, 740, '100%', 170, (40, 180, 80, 255), stroke=8, stroke_fill=LINE); return d.out()


def sheet():                                                 # thrust printout: the number is there, the label is not
    d = Draw(900, 1100); d.poly([(40, 40), (860, 40), (860, 1060), (40, 1060)], fill=(250, 248, 236, 255), outline=LINE, width=14)
    for y in range(120, 1000, 90):
        if abs(y - 570) > 120: d.rect(100, y, 800 - (y * 37) % 200, y + 16, (180, 180, 190, 255))
    d.text(330, 570, '12.6', 200, LINE); d.rrect(570, 480, 800, 660, 20, outline=(230, 60, 60, 255), width=10)
    d.text(685, 570, '?', 150, (230, 60, 60, 255), stroke=6, stroke_fill=LINE); return d.out()


def test100():                                               # the boss's "perfect" paper
    d = Draw(700, 860); d.poly([(30, 30), (670, 30), (670, 830), (30, 830)], fill=WT, outline=LINE, width=14)
    for y in range(400, 800, 80): d.rect(90, y, 610, y + 14, (180, 186, 200, 255))
    d.ellipse(350, 210, 230, 140, outline=(230, 50, 50, 255), width=14); d.text(350, 210, '100%', 150, (230, 50, 50, 255)); return d.out()


def cal(top, year, col):
    d = Draw(720, 800); d.rrect(20, 60, 700, 780, 40, fill=(255, 246, 236, 255), outline=LINE, width=18); d.rrect(20, 60, 700, 270, 40, fill=col, outline=LINE, width=18)
    d.rect(38, 220, 682, 270, col); d.stroke([(20, 270), (700, 270)], LINE, 14); d.text(360, 168, top, 120, WHITE, stroke=6, stroke_fill=LINE)
    for x in (200, 520): d.rrect(x - 22, 20, x + 22, 120, 18, fill=(150, 150, 160, 255), outline=LINE, width=10)
    d.text(360, 520, year, 230, dk(col, 0.8), stroke=10, stroke_fill=LINE); return d.out()


def bigneon(l1, l2, w, col, col2, h=460):                   # neon sign with two equally big lines
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 40, fill=(34, 14, 58, 255), outline=LINE, width=16); d.rrect(34, 34, w - 34, h - 34, 28, outline=col2, width=8)
    for k, (txt, c) in enumerate(((l1, col), (l2, col2))): d.text(w / 2, h * (0.32 + 0.38 * k), txt, LA.fit(txt, 150, w - 120), c, stroke=7, stroke_fill=LINE)
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
W2, H2 = 2400, 1100
def sky(top, bot, k=1.2): return CA.gradient(top, bot, W2, H2, k).convert('RGBA')
def stars(d, n, ybot, seed=3, col=(255, 250, 230, 230)):
    r = np.random.RandomState(seed)
    for _ in range(n): d.dot(r.randint(0, W2), r.randint(0, ybot), r.choice([3, 4, 6]), col)
def planet(d, cx, cy, r, base, spots, cap=True):
    d.ellipse(cx, cy, r, r, fill=base + (255,), outline=LINE, width=12)
    for k, (u, v, s) in enumerate(spots): d.ellipse(cx + u * r, cy + v * r, s * r, s * r * 0.6, fill=dk(base + (255,), 0.82))
    if cap: d.ellipse(cx - r * 0.1, cy - r * 0.86, r * 0.32, r * 0.1, fill=(250, 250, 255, 255))
MSPOTS = [(-0.4, -0.2, 0.22), (0.3, 0.1, 0.3), (-0.1, 0.5, 0.18), (0.5, -0.45, 0.14), (-0.55, 0.35, 0.12)]
def palm(d, x, base, h, col=(60, 130, 80, 255)):
    d.stroke([(x, base), (x + 20, base - h * 0.5), (x + 50, base - h)], LINE, 34); d.stroke([(x, base), (x + 20, base - h * 0.5), (x + 50, base - h)], (150, 100, 60, 255), 20)
    for a in range(0, 360, 60): r_ = math.radians(a); d.ellipse(x + 50 + 110 * math.cos(r_), base - h + 40 * math.sin(r_), 120, 34, fill=col, outline=LINE, width=8)
def window(d, x0, y0, x1, y1, frame=(250, 250, 245, 255)):
    d.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], outline=frame, width=24); d.stroke([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], frame, 16); d.stroke([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], frame, 16)


def ctrl(path):                                              # night control room: giant screen (Earth -> Mars, red X), consoles, amber desk lamps
    im = sky((28, 46, 92), (64, 90, 140), 1.1); d = Draw(W2, H2)
    for x in range(100, W2, 400): d.rrect(x, 0, x + 220, 26, 8, fill=(210, 230, 255, 255))
    d.rrect(380, 400, 2020, 920, 26, fill=(18, 32, 70, 255), outline=LINE, width=16)
    r_ = np.random.RandomState(5)
    for _ in range(70): d.dot(r_.randint(420, 1980), r_.randint(440, 880), r_.choice([3, 4, 6]), (255, 250, 230, 230))
    d.ellipse(640, 760, 56, 56, fill=(60, 130, 220, 255), outline=LINE, width=8); planet(d, 1450, 730, 112, MARS[:3], MSPOTS)
    for u in np.linspace(0, 1, 16): d.dot(700 + u * 650, 750 - 200 * math.sin(u * 2.8) + 40 * u, 9, (255, 236, 160, 255))
    for a, b in (((1460, 730), (1590, 860)), ((1590, 730), (1460, 860))): d.stroke([a, b], LINE, 44); d.stroke([a, b], (255, 60, 60, 255), 26)
    for x0, x1 in ((40, 340), (2060, 2360)):
        d.rrect(x0, 420, x1, 700, 16, fill=(10, 30, 40, 255), outline=LINE, width=12)
        d.stroke([(x0 + 30 + k * 24, 660 - 160 * abs(math.sin(k * 0.7 + x0))) for k in range(11)], (90, 255, 140, 255), 8)
    d.rect(0, 960, W2, H2, (60, 74, 110, 255)); d.stroke([(0, 960), (W2, 960)], LINE, 8)
    for x in range(0, W2, 300):
        if x + 260 < 380 or x + 40 > 2020: d.rrect(x + 40, 740, x + 260, 840, 10, fill=(18, 28, 50, 255), outline=LINE, width=8); d.rect(x + 60, 758, x + 240, 820, (70, 180, 255, 255))
        d.rrect(x + 10, 900, x + 290, 1000, 16, fill=(52, 64, 92, 255), outline=LINE, width=8)
    for x in (250, 2150): d.dot(x, 880, 22, (255, 180, 70, 255))
    im.alpha_composite(d.out()); glow(im, 1200, 660, 700, (90, 160, 255, 80), 90); glow(im, 1450, 730, 200, (255, 120, 60, 120), 50); glow(im, 1525, 795, 150, (255, 60, 60, 150), 40)
    for x in (250, 2150): glow(im, x, 880, 120, (255, 180, 80, 120), 30)
    im.convert('RGB').save(path)


def space(path):                                             # deep violet space, nebula, a giant Mars, Phobos, a far sun
    im = sky((40, 22, 86), (130, 60, 150), 1.1); d = Draw(W2, H2); stars(d, 220, H2, 7)
    planet(d, 1700, 720, 560, MARS[:3], MSPOTS); d.chord(1700, 720, 560, 560, 300, 480, fill=(40, 10, 40, 110))
    d.ellipse(860, 300, 60, 44, fill=(150, 140, 150, 255), outline=LINE, width=8); d.dot(840, 290, 12, (110, 100, 110, 255))
    d.dot(300, 240, 60, (255, 250, 220, 255))
    im.alpha_composite(d.out()); glow(im, 600, 600, 500, (200, 80, 200, 70), 120); glow(im, 300, 240, 260, (255, 240, 200, 150), 60); glow(im, 1700, 720, 640, (255, 140, 90, 70), 80)
    im.convert('RGB').save(path)


def launch(path):                                            # dawn at the cape: pink-gold sky, sea, red gantry, palms, steam
    im = sky((255, 140, 170), (255, 222, 150), 1.1); d = Draw(W2, H2)
    d.dot(1800, 560, 150, (255, 246, 200, 255)); CA_cl = [(400, 220, 1.0), (1100, 160, 0.8), (2050, 240, 1.0)]
    for x, y, s in CA_cl:
        for dx, dy, r in ((-90, 10, 70), (0, -20, 95), (95, 8, 72)): d.ellipse(x + dx * s, y + dy * s, r * s * 1.3, r * s, fill=(255, 200, 210, 220))
    d.rect(0, 590, W2, 700, (150, 150, 210, 255)); d.stroke([(0, 590), (W2, 590)], LINE, 8)
    for k in range(5): d.stroke([(1800 - 160 + k * 26, 610 + k * 18), (1800 + 160 - k * 26, 610 + k * 18)], (255, 236, 190, 255), 8)
    d.rect(0, 700, W2, H2, (190, 170, 150, 255)); d.stroke([(0, 700), (W2, 700)], LINE, 8)
    for x in (1360, 1560): d.stroke([(x, 700), (x, 110)], LINE, 26); d.stroke([(x, 700), (x, 110)], (210, 70, 50, 255), 14)
    for y in range(130, 700, 80): d.stroke([(1360, y), (1560, y + 80)], (210, 70, 50, 255), 8); d.stroke([(1360, y), (1560, y)], (210, 70, 50, 255), 10)
    d.rrect(1330, 80, 1590, 130, 10, fill=(210, 70, 50, 255), outline=LINE, width=8)
    for x, h in ((140, 360), (420, 300), (2100, 340), (2320, 280)): palm(d, x, 720, h)
    for x, y, r in ((900, 760, 160), (1100, 730, 130), (1700, 760, 170), (1950, 740, 120)): d.ellipse(x, y, r, r * 0.5, fill=(255, 250, 246, 235))
    im.alpha_composite(d.out()); glow(im, 1800, 560, 340, (255, 250, 220, 150), 70); im.convert('RGB').save(path)


def trip(path):                                              # teal cruise: Earth left, Mars right, the dotted nine-month arc, a comet
    im = sky((8, 40, 64), (20, 100, 118), 1.0); d = Draw(W2, H2); stars(d, 180, H2, 11)
    planet(d, 320, 560, 170, (60, 130, 220), [(-0.3, -0.2, 0.3), (0.3, 0.3, 0.25)], cap=False)
    for u, v in ((-0.3, -0.2), (0.3, 0.3)): d.ellipse(320 + u * 170, 560 + v * 170, 50, 30, fill=(90, 190, 100, 255))
    planet(d, 2090, 430, 120, MARS[:3], MSPOTS)
    for u in np.linspace(0.04, 0.95, 24): d.dot(320 + u * 1770, 560 - 420 * math.sin(u * math.pi) - 130 * u, 10, (255, 240, 180, 255))
    d.stroke([(1500, 140), (1900, 60)], (220, 250, 255, 200), 10); d.dot(1500, 140, 16, WT)
    im.alpha_composite(d.out()); glow(im, 1200, 500, 600, (60, 220, 220, 60), 120); glow(im, 320, 560, 230, (120, 200, 255, 120), 50); glow(im, 2090, 430, 180, (255, 140, 90, 110), 40)
    im.convert('RGB').save(path)


def board(path):                                             # warm office: chalkboard full of maths, sunny window, wainscot
    im = sky((252, 240, 214), (238, 216, 180), 1.0); d = Draw(W2, H2)
    d.rrect(240, 110, 1640, 600, 20, fill=(44, 96, 76, 255), outline=(150, 100, 60, 255), width=34)
    CH = (240, 240, 226, 255)
    for row in range(4):
        y = 190 + row * 105; x = 320 + (row % 2) * 60
        for k in range(7):
            w = 60 + (k * 53 + row * 31) % 90; d.stroke([(x, y), (x + w * 0.3, y - 30), (x + w * 0.6, y + 10), (x + w, y - 20)], CH, 7); x += w + 40
            if k == 2: d.stroke([(x - 30, y - 10), (x - 6, y - 10)], CH, 7); d.stroke([(x - 30, y + 6), (x - 6, y + 6)], CH, 7)
    d.stroke([(1200 + k * 30, 520 - 0.004 * (k * 30 - 180) ** 2) for k in range(13)], (255, 220, 120, 255), 8)
    window(d, 1820, 120, 2260, 560); d.rect(1832, 132, 2248, 548, (160, 210, 255, 255)); window(d, 1820, 120, 2260, 560)
    d.rect(0, 640, W2, H2, (176, 122, 80, 255)); d.stroke([(0, 640), (W2, 640)], LINE, 10)
    for x in range(0, W2, 200): d.stroke([(x, 650), (x, H2)], (150, 100, 64, 255), 6)
    im.alpha_composite(d.out()); glow(im, 2040, 340, 360, (255, 250, 220, 150), 70); im.convert('RGB').save(path)


def radarbg(path):                                           # dark navigation room: amber wall plot, tape-reel computers
    im = sky((80, 56, 40), (140, 100, 66), 1.0); d = Draw(W2, H2)
    d.rrect(620, 80, 1780, 610, 20, fill=(60, 40, 16, 255), outline=(90, 80, 70, 255), width=18)
    for x in range(680, 1760, 90): d.stroke([(x, 90), (x, 600)], (90, 60, 20, 255), 3)
    for y in range(140, 600, 80): d.stroke([(630, y), (1770, y)], (90, 60, 20, 255), 3)
    d.ellipse(1640, 360, 60, 60, fill=MARS, outline=LINE, width=6)
    for u in np.linspace(0, 1, 18): d.dot(700 + u * 940, 540 - 330 * math.sin(u * 1.5), 8, (255, 200, 80, 255))
    for x in (60, 330, 1920, 2190):
        d.rrect(x, 150, x + 230, 700, 12, fill=(150, 146, 130, 255), outline=LINE, width=10)
        for cy in (250, 400): d.ellipse(x + 115, cy, 70, 70, fill=(60, 56, 50, 255), outline=LINE, width=8); d.dot(x + 115, cy, 16, (190, 186, 170, 255))
        for k in range(5): d.dot(x + 40 + k * 38, 560, 9, (255, 80, 60, 255) if k % 2 else (255, 210, 80, 255))
    d.rect(0, 700, W2, H2, (96, 74, 58, 255)); d.stroke([(0, 700), (W2, 700)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1200, 345, 650, (255, 170, 60, 90), 90); im.convert('RGB').save(path)


def meet(path):                                              # dusk meeting room: big window on a purple city, falling chart, clock
    im = sky((200, 180, 210), (180, 160, 190), 1.0); d = Draw(W2, H2)
    d.rect(900, 80, 2300, 620, (120, 80, 160, 255))
    for x0, w, h in ((920, 140, 260), (1080, 110, 360), (1210, 170, 220), (1400, 130, 400), (1550, 180, 280), (1750, 120, 340), (1890, 160, 240), (2070, 200, 380)):
        d.rect(x0, 620 - h, x0 + w, 620, (60, 40, 90, 255))
        for j in range(int(h / 60)): d.rect(x0 + 20, 640 - h + j * 60, x0 + 40, 660 - h + j * 60, (255, 210, 120, 255))
    d.dot(1700, 200, 70, (255, 200, 140, 255)); window(d, 900, 80, 2300, 620, (90, 70, 100, 255))
    d.rrect(120, 140, 760, 560, 16, fill=WT, outline=LINE, width=12)
    d.stroke([(180, 220), (320, 260), (440, 330), (560, 420), (700, 500)], (230, 60, 60, 255), 14); d.poly([(700, 520), (720, 470), (670, 486)], fill=(230, 60, 60, 255))
    d.ellipse(830, 130, 50, 50, fill=WT, outline=LINE, width=8); d.stroke([(830, 130), (830, 100)], LINE, 6); d.stroke([(830, 130), (852, 140)], LINE, 6)
    d.rect(0, 660, W2, H2, (120, 96, 140, 255)); d.stroke([(0, 660), (W2, 660)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1700, 200, 280, (255, 200, 150, 120), 60); im.convert('RGB').save(path)


def arrive(path):                                            # Mars arrival: the curved red horizon with a thin blue air halo, the high planned arc
    im = sky((8, 4, 30), (46, 22, 76), 1.1); d = Draw(W2, H2); stars(d, 200, 700, 13)
    d.ellipse(1200, 2500, 1960, 1960, fill=(110, 190, 255, 150)); d.ellipse(1200, 2500, 1900, 1900, fill=MARS, outline=LINE, width=12)
    for u, s in ((300, 1.0), (800, 0.7), (1500, 1.2), (2000, 0.8)): d.ellipse(u, 760 + 60 * s, 120 * s, 30 * s, fill=dk(MARS, 0.82))
    for u in np.linspace(0.02, 0.98, 26): d.dot(100 + u * 2200, 470 - 300 * math.sin(u * math.pi), 9, (120, 255, 150, 255))
    d.ellipse(420, 220, 30, 22, fill=(170, 160, 160, 255), outline=LINE, width=6); d.ellipse(1900, 160, 20, 16, fill=(170, 160, 160, 255), outline=LINE, width=6)
    im.alpha_composite(d.out()); glow(im, 1200, 620, 900, (120, 190, 255, 60), 80); im.convert('RGB').save(path)


def burn(path):                                              # the burn: fiery red air, fire trail from the sky, embers, close red ground
    im = sky((70, 10, 14), (255, 120, 50), 1.0); d = Draw(W2, H2)
    for k in range(5): d.poly([(2300 - k * 40, 0), (2400, 60 + k * 30), (1300 + k * 30, 640 + k * 10)], fill=(255, 200 - k * 30, 70, 150))
    for k in range(40): d.dot((k * 613) % W2, (k * 211) % 640, 4 + k % 4, (255, 220, 120, 230))
    d.poly([(0, 640), (500, 600), (900, 660), (1500, 610), (2000, 650), (2400, 620), (2400, H2), (0, H2)], fill=(150, 56, 40, 255), outline=LINE, width=8)
    for x, s in ((300, 1.0), (1000, 0.6), (1800, 0.9)): d.ellipse(x, 760, 160 * s, 40 * s, fill=(120, 40, 30, 255), outline=LINE, width=6)
    im.alpha_composite(d.out()); glow(im, 1400, 600, 500, (255, 200, 90, 110), 80); im.convert('RGB').save(path)


def dishes(path):                                            # moonlit desert: far dishes, mesas, a warm-lit hut, cacti
    im = sky((8, 16, 54), (50, 80, 140), 1.1); d = Draw(W2, H2); stars(d, 160, 560, 17)
    d.dot(420, 230, 90, (250, 246, 220, 255)); d.dot(450, 210, 20, (220, 216, 190, 255))
    d.poly([(0, 620), (200, 500), (560, 500), (760, 620)], fill=(64, 52, 96, 255), outline=LINE, width=8); d.poly([(1500, 620), (1640, 470), (1900, 470), (2050, 620)], fill=(64, 52, 96, 255), outline=LINE, width=8)
    for x, s in ((1100, 0.8), (2200, 0.6)):
        d.poly([(x - 60 * s, 620), (x + 60 * s, 620), (x + 30 * s, 470), (x - 30 * s, 470)], fill=(190, 200, 220, 255), outline=LINE, width=6)
        d.ellipse(x, 400 - 60 * s, 200 * s, 110 * s, fill=(220, 226, 240, 255), outline=LINE, width=8)
    d.rect(0, 620, W2, H2, (84, 76, 120, 255)); d.stroke([(0, 620), (W2, 620)], LINE, 8)
    d.rect(1700, 520, 1900, 640, (120, 100, 110, 255)); d.poly([(1680, 524), (1800, 470), (1920, 524)], fill=(90, 70, 90, 255), outline=LINE, width=8); d.rect(1740, 560, 1800, 610, (255, 200, 100, 255))
    for x in (300, 900, 2100):
        d.rrect(x - 26, 560, x + 26, 720, 24, fill=(60, 110, 90, 255), outline=LINE, width=8); d.rrect(x + 20, 600, x + 70, 640, 20, fill=(60, 110, 90, 255), outline=LINE, width=6)
    im.alpha_composite(d.out()); glow(im, 420, 230, 220, (240, 240, 255, 110), 60); glow(im, 1770, 585, 120, (255, 200, 100, 140), 30); im.convert('RGB').save(path)


def units(path):                                             # split room: orange Colorado side | blue California side, a bright crack between
    im = sky((255, 170, 90), (230, 130, 60), 1.0); d = Draw(W2, H2)
    d.rect(1200, 0, W2, H2, (80, 140, 230, 255))
    d.rect(220, 120, 820, 520, (170, 220, 255, 255))
    for x0, h in ((220, 220), (420, 330), (620, 260)): d.poly([(x0, 520), (x0 + 180, 520 - h), (x0 + 360, 520)], fill=(140, 120, 170, 255), outline=LINE, width=6); d.poly([(x0 + 130, 520 - h + 60), (x0 + 180, 520 - h), (x0 + 230, 520 - h + 60)], fill=WT)
    window(d, 220, 120, 820, 520)
    d.rect(1580, 120, 2180, 520, (190, 230, 255, 255)); d.rect(1580, 400, 2180, 520, (60, 160, 220, 255)); d.dot(2050, 230, 60, (255, 240, 170, 255)); palm(d, 1700, 520, 300)
    window(d, 1580, 120, 2180, 520)
    pts = [(1200 + (40 if k % 2 else -40), k * 110) for k in range(11)]; d.stroke(pts, LINE, 40); d.stroke(pts, (255, 240, 120, 255), 20)
    d.rect(0, 640, W2, H2, (60, 50, 60, 255)); d.stroke([(0, 640), (W2, 640)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1200, 500, 200, (255, 250, 200, 120), 60); im.convert('RGB').save(path)


def deskbg(path):                                            # sepia desk wall: cork board of notes, a wall calendar crossed off month after month, lamp glow
    im = sky((236, 216, 178), (214, 184, 140), 1.0); d = Draw(W2, H2)
    d.rrect(240, 110, 1100, 580, 18, fill=(196, 150, 100, 255), outline=(120, 80, 50, 255), width=26)
    for k, (x, y) in enumerate(((320, 170), (560, 200), (800, 160), (380, 370), (650, 400), (900, 360))):
        d.rect(x, y, x + 170, y + 140, [(255, 240, 150, 255), (190, 230, 255, 255), (255, 200, 210, 255)][k % 3]); d.dot(x + 85, y + 14, 14, (230, 60, 60, 255))
    d.rrect(1360, 110, 1900, 600, 16, fill=WT, outline=LINE, width=12); d.rect(1372, 122, 1888, 210, (230, 80, 60, 255))
    for r in range(5):
        for c in range(7):
            x, y = 1390 + c * 70, 240 + r * 70; d.rect(x, y, x + 56, y + 56, (240, 236, 226, 255)); d.stroke([(x + 8, y + 8), (x + 48, y + 48)], (230, 60, 60, 255), 6)
    d.rect(0, 660, W2, H2, (150, 104, 70, 255)); d.stroke([(0, 660), (W2, 660)], LINE, 10)
    d.poly([(2080, 160), (2240, 160), (2280, 300), (2040, 300)], fill=(60, 120, 90, 255), outline=LINE, width=10); d.stroke([(2160, 300), (2160, 660)], LINE, 14)
    im.alpha_composite(d.out()); glow(im, 2160, 330, 380, (255, 220, 140, 150), 80); im.convert('RGB').save(path)


def school(path):                                            # sunny classroom: three tall windows, small chalkboard, shape posters, plants
    im = sky((255, 236, 160), (255, 214, 120), 1.0); d = Draw(W2, H2)
    for x0 in (120, 1640):
        d.rect(x0, 100, x0 + 600, 560, (150, 210, 255, 255)); d.dot(x0 + 450, 230, 60, (255, 250, 200, 255)); window(d, x0, 100, x0 + 600, 560)
    d.rrect(860, 160, 1540, 520, 16, fill=(50, 110, 80, 255), outline=(150, 100, 60, 255), width=24); planet(d, 1200, 340, 110, MARS[:3], MSPOTS)
    for x, c in ((900, PINK), (1050, SKYB), (1350, LIME), (1500, ORNG)): d.poly([(x - 40, 620), (x, 560), (x + 40, 620)], fill=c, outline=LINE, width=6)
    for x in (80, 2320): d.rrect(x - 50, 560, x + 50, 660, 16, fill=(210, 110, 70, 255), outline=LINE, width=8); d.ellipse(x, 520, 90, 70, fill=(80, 170, 90, 255), outline=LINE, width=8)
    d.rect(0, 660, W2, H2, (200, 150, 100, 255)); d.stroke([(0, 660), (W2, 660)], LINE, 8)
    im.alpha_composite(d.out())
    for x0 in (120, 1640): glow(im, x0 + 300, 330, 340, (255, 255, 230, 120), 70)
    im.convert('RGB').save(path)


def sandtex(path, c1, c2, n=512, seed=4):                    # speckled floor (sand, carpet, star floor)
    r = np.random.RandomState(seed); d = Draw(n, n, c1 + (255,))
    for _ in range(260): d.dot(r.randint(0, n), r.randint(0, n), r.choice([2, 3, 5]), c2 + (255,))
    d.out().convert('RGB').save(path, quality=92)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in ('nav', 'nav2', 'boss', 'lock'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'smug')]
    multi = dict(orbiter={'default': orbiter(), 'shocked': orbiter('shocked'), 'burn': orbiter('burn')}, rocket={'default': rocket(), 'fire': rocket('fire')},
                 dish={'default': dish(), 'sad': dish('sad')}, radar={'default': radar()}, calc={'default': calc()}, clip={'default': clip()},
                 sheet={'default': sheet()}, test100={'default': test100()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    NAVY, DEEP = (30, 50, 120, 255), (20, 40, 70, 255)
    cards = dict(perfect=plaque("NASA'S MATH", 'WAS PERFECT!', (40, 150, 80, 255), WHITE, 1000, border=GOLDL, bs=150, ss=96, sc=GOLDL),
                 lost=stamp('LOST AT MARS!', 960, (220, 50, 40, 255), 110, -4),
                 m125=neon('$125 MILLION', 'SPACECRAFT', 960, GOLDL, CYAN),
                 date1=cal('DEC 11', '1998', (60, 130, 210, 255)),
                 mco=plaque('MARS CLIMATE ORBITER', 'LAUNCHES!', (200, 70, 50, 255), WHITE, 1040, border=GOLDL, bs=110, ss=96, sc=GOLDL),
                 trip=stamp('A NINE-MONTH TRIP', 1000, (30, 140, 150, 255), 100, 3),
                 burnc=plaque('EVERY ENGINE BURN', 'CALCULATED', (40, 96, 76, 255), WHITE, 1000, border=(255, 220, 120, 255), bs=110, ss=100, sc=(255, 220, 120, 255)),
                 decimal=stamp('TO THE DECIMAL!', 940, (230, 120, 30, 255), 110, -3),
                 drift=stamp('PATH DRIFTING LOWER!', 1060, (220, 60, 50, 255), 96, 3),
                 concerns=stamp('THEY RAISE CONCERNS!', 1060, (230, 130, 40, 255), 96, -3),
                 nobody=stamp('NOBODY FIXES IT!', 980, (110, 110, 130, 255), 106, 4),
                 date2=cal('SEP 23', '1999', (210, 90, 50, 255)),
                 high=plaque('HIGH ABOVE', 'THE MARTIAN AIR', (40, 110, 190, 255), WHITE, 980, border=(150, 230, 255, 255), bs=150, ss=86, sc=(150, 230, 255, 255)),
                 miles40=bigneon('UNDER 40', 'MILES!', 900, (255, 120, 80, 255), GOLDL),
                 contact=stamp('CONTACT LOST!', 920, (220, 40, 50, 255), 116, -4),
                 never=plaque('NEVER CALLS', 'HOME AGAIN', NAVY, WHITE, 960, border=(170, 200, 255, 255), bs=150, ss=100, sc=(170, 200, 255, 255)),
                 numbers=plaque('THE NUMBERS', 'WERE NEVER WRONG', (40, 150, 80, 255), WHITE, 1000, border=GOLDL, bs=150, ss=84, sc=GOLDL),
                 units=stamp('THE UNITS WERE!', 960, (220, 40, 50, 255), 120, -4),
                 pounds=plaque('LOCKHEED MARTIN', 'THRUST IN POUNDS', (230, 120, 40, 255), WHITE, 1000, border=WHITE, bs=120, ss=86, sc=(255, 240, 170, 255)),
                 newtons=plaque("NASA'S SOFTWARE", 'READ IT AS NEWTONS', (40, 100, 200, 255), WHITE, 1000, border=WHITE, bs=120, ss=80, sc=(200, 240, 255, 255)),
                 label=stamp('ONE MISSING LABEL', 1000, (220, 50, 40, 255), 100, -3),
                 months9=plaque('UNNOTICED', 'FOR NINE MONTHS', (120, 84, 50, 255), WHITE, 960, border=GOLDL, bs=160, ss=90, sc=GOLDL),
                 mathperf=stamp('"MY MATH IS PERFECT!"', 1060, (60, 150, 90, 255), 96, 3),
                 askone=stamp('ASK ONE QUESTION', 980, (60, 110, 200, 255), 104, -3),
                 whatunits=bigneon('PERFECT IN', 'WHAT UNITS?', 980, LIME, GOLDL))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (70, 70, 96), (60, 60, 84))
    CE.tiles(T('navtile.jpg'), (78, 96, 146), (66, 84, 130)); sandtex(T('starfloor.jpg'), (66, 36, 106), (255, 240, 220), seed=5); CE.tiles(T('pad.jpg'), (176, 170, 166), (160, 154, 150))
    sandtex(T('starfloor2.jpg'), (24, 90, 104), (220, 250, 255), seed=6); CE.tiles(T('darktile.jpg'), (110, 88, 70), (96, 76, 60)); sandtex(T('carpet.jpg'), (126, 96, 146), (110, 82, 130))
    sandtex(T('redsand.jpg'), (206, 104, 62), (176, 84, 48)); sandtex(T('redsand2.jpg'), (150, 60, 42), (120, 44, 32)); sandtex(T('nightsand.jpg'), (84, 78, 124), (70, 64, 108))
    CE.tiles(T('checker.jpg'), (236, 232, 226), (200, 200, 212)); CE.tiles(T('deskwood.jpg'), (166, 116, 74), (150, 104, 66)); CE.tiles(T('schoolwood.jpg'), (214, 164, 110), (200, 150, 98))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(ctrl=ctrl, space=space, launch=launch, trip=trip, board=board, radarbg=radarbg, meet=meet, arrive=arrive, burn=burn, dishes=dishes, units=units, deskbg=deskbg, school=school)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
