#!/usr/bin/env python3
"""Assets for video 29: Abraham Lincoln is in the Wrestling Hall of Fame - frontier wrestler, about 300 matches, one loss (1832, Thompson),
the New Salem fight with Jack Armstrong, and the 1858 almanac trial that freed Jack's son Duff. Wrestling-poster world (new palette):
tangerine-pink starburst arena with a turquoise ring (hook + loop, a "?" moon = open loop resolved by the almanac), turquoise-gold trophy
hall, butter-yellow prairie, peach-teal 1832 army camp, mint misty New Salem, coral sunset fight circle, honey firefly dusk, oxblood courtroom,
bright navy moon meadow, amber candlelit study. Cute cast (new): classic Abe (stovepipe, chin beard, black coat), young Abe (linen shirt,
rope belt), Jack Armstrong (coonskin cap, buckskin fringe), Thompson (kepi, cross-belt coat), Duff (freckles, patched shirt), the witness
(straw hat, glasses). The murder charge stays cute: gavel, stamp, sweat drop only. usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v29_assets import *

ROOT = B.ROOT
TANG, TURQ, CYAN, GOLD, OX, NAVY, MINT, CRM = (255, 140, 60, 255), (40, 190, 180, 255), (34, 224, 255, 255), (250, 196, 60, 255), (120, 40, 50, 255), (30, 50, 110, 255), (150, 230, 200, 255), (252, 244, 226, 255)
LA.NEW.update({
    'abe': dict(sk=0, style='side', hair=(44, 34, 34, 255), suit=(44, 40, 54, 255), shade=(30, 28, 38, 255), body='blackcoat', xhat='stovepipe', beard=(44, 34, 34, 255)),
    'abe58': dict(sk=0, style='side', hair=(44, 34, 34, 255), suit=(44, 40, 54, 255), shade=(30, 28, 38, 255), body='blackcoat', xhat='stovepipe', band2=(150, 40, 50, 255)),
    'abey': dict(sk=0, style='curly', hair=(44, 34, 34, 255), suit=(240, 228, 200, 255), shade=(214, 200, 170, 255), body='linen', acc=(170, 120, 70, 255)),
    'jack': dict(sk=0, style='curly', hair=(206, 104, 50, 255), suit=(200, 150, 100, 255), shade=(172, 124, 80, 255), body='fringe', acc=(230, 60, 70, 255), xhat='coonskin', hatc=(150, 100, 60, 255), stache=(206, 104, 50, 255)),
    'thompson': dict(sk=2, style='part', hair=(30, 24, 24, 255), suit=(50, 74, 150, 255), shade=(38, 56, 120, 255), body='soldier', acc=(220, 70, 70, 255), xhat='kepi', hatc=(64, 90, 170, 255)),
    'duff': dict(sk=0, style='curly', hair=(236, 124, 60, 255), suit=(120, 184, 226, 255), shade=(96, 152, 194, 255), body='patched', acc=(244, 130, 160, 255), freckles=1),
    'witness': dict(sk=1, style='bald', hair=(60, 40, 30, 255), suit=(170, 120, 210, 255), shade=(140, 96, 176, 255), body='overalls', acc=(250, 240, 200, 255), xhat='straw', hatc=(244, 212, 120, 255), glasses=1),
})


def gloss(d, x, y, w, h): d.ellipse(x, y, w, h, fill=(255, 255, 255, 120))


def neon3(a, b, c, w=900, h=560):                            # 3-line hook sign: small top line, two big lines
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 44, fill=(50, 20, 70, 255), outline=LINE, width=16); d.rrect(34, 34, w - 34, h - 34, 30, outline=CYAN, width=8)
    d.text(w / 2, h * 0.2, a, LA.fit(a, 96, w - 160), CYAN, stroke=6, stroke_fill=LINE)
    for k, (t, col) in enumerate(((b, YEL), (c, TANG))): d.text(w / 2, h * (0.47 + 0.27 * k), t, LA.fit(t, 140, w - 110), col, stroke=7, stroke_fill=LINE)
    return d.out()


def belt():                                                  # glossy gold championship belt with a star plate and a face
    d = Draw(1400, 700); d.rrect(40, 260, 1360, 460, 90, fill=(60, 40, 90, 255), outline=LINE, width=14)
    for x in (180, 1220): d.ellipse(x, 360, 110, 100, fill=GOLD, outline=LINE, width=12); d.text(x, 360, '*', 120, OX)
    d.ellipse(700, 360, 330, 290, fill=GOLD, outline=LINE, width=16); d.ellipse(700, 360, 270, 230, outline=(255, 236, 150, 255), width=12); gloss(d, 560, 200, 90, 40)
    eyes(d, 700, 360, 0.95, 'happy'); return d.out()


def masked(no=False):                                        # cute masked pro wrestler (no: big red X - NOT a pro wrestler)
    d = Draw(1100, 1300); d.rrect(260, 620, 840, 1180, 160, fill=(255, 120, 160, 255), outline=LINE, width=14)
    for sg in (-1, 1): d.ellipse(550 + sg * 340, 760, 130, 150, fill=(255, 210, 170, 255), outline=LINE, width=12)
    d.rect(300, 1060, 800, 1120, GOLD); d.dot(550, 400, 290, (60, 120, 240, 255)); d.ellipse(550, 400, 290, 290, outline=LINE, width=14)
    for sg in (-1, 1): d.poly([(550 + sg * 40, 210), (550 + sg * 240, 300), (550 + sg * 200, 400), (550 + sg * 60, 340)], fill=YEL)
    d.poly([(550, 130), (590, 200), (510, 200)], fill=YEL); eyes(d, 550, 410, 1.2, 'shocked' if no else 'happy'); gloss(d, 420, 220, 80, 36)
    if no: d.stroke([(150, 150), (950, 1150)], (240, 40, 60, 255), 70); d.stroke([(950, 150), (150, 1150)], (240, 40, 60, 255), 70)
    return d.out()


def ruler():                                                 # height chart: 6 FT 4 with tick marks and a happy face
    d = Draw(500, 1600); d.rrect(120, 40, 380, 1580, 30, fill=(255, 236, 170, 255), outline=LINE, width=12)
    for k in range(0, 77, 2): y = 1560 - k * 19.5; d.stroke([(120, y), (120 + (90 if k % 12 == 0 else 45), y)], LINE, 7 if k % 12 == 0 else 4)
    for f in range(1, 7): d.text(300, 1560 - f * 12 * 19.5, str(f), 70, OX)
    d.rrect(90, 40, 410, 110, 20, fill=(240, 60, 80, 255), outline=LINE, width=10); eyes(d, 250, 700, 0.55, 'happy'); return d.out()


def flop():                                                  # the one loss: young Abe flat on his back, boots up, spiral eyes, dizzy stars
    d = Draw(1600, 900); d.ellipse(800, 800, 700, 70, fill=(190, 150, 100, 255)); d.rrect(300, 560, 1000, 760, 100, fill=(240, 228, 200, 255), outline=LINE, width=12)
    for x in (1040, 1160): d.rrect(x - 50, 380, x + 50, 720, 40, fill=(90, 70, 60, 255), outline=LINE, width=10)
    d.dot(230, 640, 170, (255, 222, 196, 255)); d.ellipse(230, 640, 170, 170, outline=LINE, width=12); d.chord(230, 600, 176, 140, 180, 360, fill=(44, 34, 34, 255))
    for sg in (-1, 1): [d.arc(230 + sg * 60, 650, 10 + k * 12, 10 + k * 12, k * 90, k * 90 + 300, LINE, 6) for k in range(3)]
    for k in range(5): a = k * 1.256; x, y = 230 + 260 * math.cos(a), 360 + 70 * math.sin(a); d.text(x, y, '*', 120, YEL, stroke=5, stroke_fill=LINE)
    return d.out()


def brawl():                                                 # the New Salem tussle: dust cloud, flying boots and fists, POW stars
    d = Draw(1500, 1200)
    for x, y, r in ((500, 650, 300), (800, 560, 340), (1050, 690, 280), (750, 820, 300)): d.dot(x, y, r, (240, 220, 190, 255))
    for x, y, r in ((500, 650, 300), (800, 560, 340), (1050, 690, 280), (750, 820, 300)): d.ellipse(x, y, r, r, outline=(200, 170, 130, 255), width=10)
    for x, y, a in ((260, 420, -0.6), (1260, 460, 0.6), (330, 980, 0.4), (1220, 1000, -0.3)): d.rrect(x - 70, y - 50, x + 70, y + 50, 40, fill=(255, 222, 196, 255) if a > 0 else (90, 70, 60, 255), outline=LINE, width=10)
    d.dot(640, 520, 120, (255, 222, 196, 255)); d.ellipse(640, 520, 120, 120, outline=LINE, width=10); d.chord(640, 494, 124, 100, 180, 360, fill=(44, 34, 34, 255)); eyes(d, 640, 530, 0.45, 'happy')
    d.dot(920, 560, 120, (255, 222, 196, 255)); d.ellipse(920, 560, 120, 120, outline=LINE, width=10); d.chord(920, 520, 130, 110, 180, 360, fill=(150, 100, 60, 255)); eyes(d, 920, 570, 0.45, 'shocked')
    for x, y in ((420, 260), (1100, 250), (760, 180)): d.text(x, y, '*', 150, YEL, stroke=6, stroke_fill=LINE)
    return d.out()


def crowd(cheer=False):                                      # row of tiny chibi frontier folk, waving hats and coins
    d = Draw(2200, 800); cols = [(240, 120, 90, 255), (90, 180, 170, 255), (250, 200, 80, 255), (160, 120, 210, 255), (120, 190, 110, 255)]
    for k in range(11):
        x = 110 + k * 198; y = 360 + (k % 2) * 50 - (40 if cheer and k % 2 else 0)
        d.rrect(x - 70, y + 70, x + 70, y + 330, 50, fill=cols[k % 5], outline=LINE, width=8); d.dot(x, y, 78, (255, 222, 196, 255) if k % 3 else (196, 136, 96, 255)); d.ellipse(x, y, 78, 78, outline=LINE, width=8)
        eyes(d, x, y + 10, 0.36, 'shocked' if cheer and k % 3 == 0 else 'happy'); arm = -1 if k % 2 else 1
        d.stroke([(x + arm * 60, y + 120), (x + arm * 110, y - (90 if cheer else 10))], cols[k % 5], 22)
        if k % 3 == 1: coin(d, x + arm * 112, y - (130 if cheer else 50), 34)
        elif k % 3 == 2: d.ellipse(x + arm * 110, y - (110 if cheer else 30), 50, 20, fill=(120, 80, 50, 255), outline=LINE, width=6)
    return d.out()


def bets():                                                  # bet pile: money bag + coins + bills with faces
    d = Draw(1200, 1000); d.chord(600, 860, 520, 120, 180, 360, fill=(120, 190, 110, 255))
    d.dot(600, 560, 300, (200, 160, 100, 255)); d.ellipse(600, 560, 300, 300, outline=LINE, width=14); d.poly([(500, 270), (700, 270), (660, 330), (540, 330)], fill=(170, 130, 80, 255), outline=LINE, width=10)
    d.text(600, 620, '$', 260, (60, 130, 70, 255), stroke=10, stroke_fill=LINE); eyes(d, 600, 470, 0.7, 'happy'); gloss(d, 470, 420, 60, 30)
    for k, (x, y) in enumerate(((220, 820), (330, 880), (900, 840), (1020, 880), (980, 760))): coin(d, x, y, 80, 'happy' if k % 2 else 'shocked')
    return d.out()


def pals():                                                  # handshake of friendship: two hands, sparkles, a heart
    d = Draw(1400, 900); d.rrect(80, 380, 620, 560, 60, fill=(240, 228, 200, 255), outline=LINE, width=12); d.rrect(780, 380, 1320, 560, 60, fill=(200, 150, 100, 255), outline=LINE, width=12)
    d.ellipse(700, 470, 190, 120, fill=(255, 222, 196, 255), outline=LINE, width=12); [d.stroke([(620 + k * 50, 400), (640 + k * 50, 540)], (220, 180, 150, 255), 6) for k in range(4)]
    d.dot(640, 200, 70, (255, 80, 120, 255)); d.dot(760, 200, 70, (255, 80, 120, 255)); d.poly([(578, 230), (822, 230), (700, 380)], fill=(255, 80, 120, 255)); gloss(d, 620, 170, 26, 14)
    for x, y in ((300, 200), (1100, 220), (1160, 700), (240, 720)): d.text(x, y, '*', 110, YEL, stroke=5, stroke_fill=LINE)
    return d.out()


def bench(bang=False):                                       # 1858 judge's bench with a gavel (bang: gavel down, impact lines)
    d = Draw(1600, 1100); d.rrect(120, 420, 1480, 1080, 30, fill=(140, 70, 50, 255), outline=LINE, width=14); d.rrect(80, 360, 1520, 450, 20, fill=(110, 50, 40, 255), outline=LINE, width=12)
    for x in (350, 800, 1250): d.rrect(x - 160, 560, x + 160, 960, 20, outline=(90, 40, 30, 255), width=12)
    d.dot(800, 170, 120, GOLD); d.ellipse(800, 170, 120, 120, outline=LINE, width=10); d.text(800, 176, '*', 150, OX); eyes(d, 800, 760, 0.8, 'shocked' if bang else 'happy')
    if bang: d.rrect(1060, 300, 1300, 360, 20, fill=(120, 70, 40, 255), outline=LINE, width=10); d.stroke([(1180, 300), (1320, 120)], (120, 70, 40, 255), 26); [d.stroke([(1180 + 160 * math.cos(a), 330 + 90 * math.sin(a)), (1180 + 240 * math.cos(a), 330 + 130 * math.sin(a))], YEL, 14) for a in (3.6, 4.2, 5.2, 5.8)]
    else: d.rrect(1080, 220, 1320, 280, 20, fill=(120, 70, 40, 255), outline=LINE, width=10); d.stroke([(1200, 280), (1200, 360)], (120, 70, 40, 255), 26)
    return d.out()


def tag():                                                   # price tag: FREE, $0, happy face
    d = Draw(1000, 700); d.poly([(220, 80), (940, 80), (940, 620), (220, 620), (60, 350)], fill=(120, 230, 170, 255), outline=LINE, width=14); d.dot(170, 350, 40, WT); d.ellipse(170, 350, 40, 40, outline=LINE, width=8)
    d.text(600, 250, '$0', 220, (30, 110, 70, 255), stroke=8, stroke_fill=LINE); eyes(d, 600, 470, 0.8, 'happy'); gloss(d, 380, 140, 90, 28); return d.out()


def moon(mode='default'):                                    # giant moon with a face (q: "?" open loop, set: half sunk behind a hill, sleepy)
    d = Draw(1300, 1300); y = 650 if mode != 'set' else 820
    d.dot(650, y, 520, (255, 246, 200, 255)); [d.dot(650 + dx, y + dy, r, (240, 224, 170, 255)) for dx, dy, r in ((-250, -180, 70), (220, 160, 90), (-120, 260, 50), (260, -230, 44))]
    d.ellipse(650, y, 520, 520, outline=LINE, width=14); gloss(d, 470, y - 330, 120, 50)
    if mode == 'q': d.text(650, y - 20, '?', 520, (120, 70, 200, 255), stroke=14, stroke_fill=LINE)
    elif mode == 'set': [d.arc(650 + sg * 130, y - 40, 50, 30, 20, 160, LINE, 12) for sg in (-1, 1)]; d.chord(650, 1300, 760, 300, 180, 360, fill=(60, 110, 90, 255), outline=LINE, width=14); d.rect(0, 1280, 1300, 1300, (60, 110, 90, 255)); [d.text(1000 + k * 90, 300 - k * 80, 'Z', 90 + k * 20, (150, 130, 255, 255), stroke=5, stroke_fill=LINE) for k in range(3)]
    else: eyes(d, 650, y, 1.4, 'happy')
    return d.out()


def almanac(mode='closed'):                                  # 1857 almanac: closed green cover / open pages with the moon chart and a red circle
    if mode == 'closed':
        d = Draw(1800, 1100); d.rrect(480, 40, 1320, 1060, 30, fill=(60, 140, 100, 255), outline=LINE, width=16); d.rect(480, 40, 550, 1060, (40, 100, 70, 255))
        d.rrect(600, 150, 1220, 400, 20, fill=CRM, outline=LINE, width=10); d.text(910, 235, 'ALMANAC', 110, OX); d.text(910, 340, '1857', 90, (40, 100, 70, 255))
        d.dot(910, 640, 130, (255, 240, 180, 255)); d.ellipse(910, 640, 130, 130, outline=LINE, width=10); eyes(d, 910, 900, 0.7, 'happy'); gloss(d, 680, 110, 80, 30); return d.out()
    d = Draw(1800, 1100); d.poly([(80, 160), (900, 220), (900, 1060), (80, 1000)], fill=CRM, outline=LINE, width=14); d.poly([(1720, 160), (900, 220), (900, 1060), (1720, 1000)], fill=CRM, outline=LINE, width=14)
    for k in range(8): y = 300 + k * 85; d.stroke([(160, y), (820, y + 20)], (200, 190, 170, 255), 10)
    for k in range(5):
        x = 1040 + k * 140; y = 380 + k * 70; d.dot(x, y, 52, (255, 236, 160, 255)); d.ellipse(x, y, 52, 52, outline=LINE, width=8)
        if k > 2: d.chord(x, y, 54, 54, 0, 180, fill=(60, 80, 130, 255))
    d.stroke([(980, 880), (1680, 880)], (60, 110, 90, 255), 12); d.ellipse(1600, 760, 120, 120, outline=(240, 40, 60, 255), width=16); eyes(d, 480, 760, 0.6, 'shocked'); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def rays(d, cx, cy, n, r, col):
    for k in range(n): a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 0.5) / n; d.poly([(cx, cy), (cx + r * math.cos(a0), cy + r * math.sin(a0)), (cx + r * math.cos(a1), cy + r * math.sin(a1))], fill=col)


def arena(path):                                             # tangerine-pink starburst wrestling arena: spotlights, crowd rows, banners
    im = sky((255, 120, 70), (255, 90, 150), 0.9); d = Draw(W2, H2); rays(d, 1200, 420, 28, 1600, (255, 190, 90, 110))
    for row, (y, col) in enumerate(((620, (120, 50, 120, 255)), (700, (100, 40, 104, 255)), (780, (80, 30, 90, 255)))):
        for x in range(20 + row * 40, W2, 110): d.dot(x, y, 44, col); d.rrect(x - 44, y + 30, x + 44, y + 160, 30, fill=col)
    for x in (300, 900, 1500, 2100): d.rect(x - 70, 80, x + 70, 330, (40, 190, 180, 255)); d.poly([(x - 70, 330), (x + 70, 330), (x, 390)], fill=(40, 190, 180, 255)); d.text(x, 200, '*', 120, YEL, stroke=5, stroke_fill=LINE)
    fl(d, (90, 40, 90, 255)); im.alpha_composite(d.out()); [glow(im, x, 40, 260, (255, 250, 220, 120), 70) for x in (500, 1200, 1900)]; im.convert('RGB').save(path)


def trophyhall(path):                                        # turquoise-gold Hall of Fame gallery: columns, gold frames, red rope
    im = sky((30, 140, 150), (120, 220, 210), 1.0); d = Draw(W2, H2)
    for x in range(100, W2, 400): d.rect(x - 50, 60, x + 50, 940, (230, 246, 240, 255)); d.rect(x - 70, 60, x + 70, 110, (250, 214, 120, 255)); d.rect(x - 70, 880, x + 70, 940, (250, 214, 120, 255))
    for x in range(300, W2, 400): d.rrect(x - 110, 250, x + 110, 520, 14, fill=(255, 240, 200, 255), outline=GOLD, width=22); d.dot(x, 370, 60, (240, 180, 160, 255)); d.text(x, 470, '*', 70, GOLD)
    d.stroke([(0, 760), (600, 800), (1200, 760), (1800, 800), (W2, 760)], (220, 50, 70, 255), 16); fl(d, (170, 60, 70, 255)); im.alpha_composite(d.out()); glow(im, 1200, 200, 600, (255, 250, 220, 70), 120); im.convert('RGB').save(path)


def prairie(path):                                           # butter-yellow golden hour prairie: big sun, hills, log cabin, rail fence, sunflowers
    im = sky((255, 200, 110), (255, 240, 190), 1.0); d = Draw(W2, H2); d.dot(1700, 420, 200, (255, 250, 210, 255))
    hills(d, 700, (150, 190, 90, 255), 70, 3); hills(d, 800, (120, 170, 80, 255), 50, 4, 1.0)
    d.rect(300, 560, 720, 840, (160, 100, 60, 255)); [d.stroke([(300, y), (720, y)], (120, 70, 40, 255), 8) for y in range(580, 840, 40)]; d.poly([(260, 570), (510, 400), (760, 570)], fill=(110, 70, 50, 255), outline=LINE, width=8); d.rect(470, 700, 550, 840, (90, 60, 40, 255))
    for x in range(900, W2, 260): d.stroke([(x, 940), (x + 10, 780)], (140, 90, 50, 255), 14); d.stroke([(x - 130, 820), (x + 140, 830)], (160, 110, 60, 255), 10); d.stroke([(x - 130, 880), (x + 140, 870)], (160, 110, 60, 255), 10)
    for x in range(60, W2, 190): y = 760 + (x * 37) % 90; d.stroke([(x, 940), (x, y)], (90, 140, 60, 255), 8); [d.ellipse(x + 26 * math.cos(a), y + 26 * math.sin(a), 18, 18, fill=YEL) for a in np.linspace(0, 6.28, 9)]; d.dot(x, y, 18, (140, 90, 40, 255))
    fl(d, (180, 160, 80, 255)); im.alpha_composite(d.out()); glow(im, 1700, 420, 420, (255, 240, 180, 110), 90); im.convert('RGB').save(path)


def camp(path):                                              # 1832 army camp at dusk: peach-teal sky, tents, flag, campfire glow
    im = sky((60, 140, 160), (255, 190, 150), 1.0); d = Draw(W2, H2); hills(d, 760, (80, 120, 120, 255), 60, 2)
    for k, x in enumerate(range(150, W2, 420)): d.poly([(x - 180, 940), (x, 640 + (k % 2) * 40), (x + 180, 940)], fill=(244, 236, 214, 255), outline=LINE, width=10); d.poly([(x - 30, 940), (x, 760), (x + 30, 940)], fill=(110, 90, 80, 255))
    d.rect(1180, 300, 1192, 700, LINE); d.rect(1192, 300, 1400, 420, (220, 70, 70, 255)); [d.rect(1192, 300 + k * 40, 1400, 320 + k * 40, WT) for k in range(0, 3)]
    fl(d, (150, 120, 100, 255)); im.alpha_composite(d.out()); glow(im, 1800, 900, 300, (255, 170, 80, 120), 70); im.convert('RGB').save(path)


def salem(path):                                             # mint misty morning New Salem: log cabins, mill wheel, river, round trees
    im = sky((150, 220, 200), (240, 250, 230), 1.0); d = Draw(W2, H2); d.rect(0, 820, W2, 900, (110, 190, 210, 255))
    for x in (200, 700, 1900, 2250): ptree(d, x, 820, 1.2, (90, 170, 110, 255))
    for k, x in enumerate((950, 1350)): d.rect(x, 560, x + 300, 820, (170, 110, 70, 255)); [d.stroke([(x, y), (x + 300, y)], (120, 80, 50, 255), 8) for y in range(580, 820, 36)]; d.poly([(x - 30, 570), (x + 150, 440), (x + 330, 570)], fill=(110, 80, 60, 255), outline=LINE, width=8)
    d.dot(1700, 760, 120, (150, 110, 70, 255)); d.ellipse(1700, 760, 120, 120, outline=LINE, width=10); [d.stroke([(1700, 760), (1700 + 120 * math.cos(a), 760 + 120 * math.sin(a))], LINE, 8) for a in np.linspace(0, 6.28, 9)]
    fl(d, (120, 170, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 800, (255, 255, 250, 90), 160); im.convert('RGB').save(path)


def duskring(path):                                          # coral sunset fight circle: sun disc, wagons, bunting
    im = sky((255, 110, 90), (255, 200, 120), 1.0); d = Draw(W2, H2); d.dot(1200, 640, 260, (255, 230, 150, 255)); hills(d, 760, (190, 90, 90, 255), 50, 3)
    for x in (300, 2000): d.rect(x - 160, 640, x + 160, 820, (150, 100, 70, 255)); d.chord(x, 650, 170, 120, 180, 360, fill=(250, 240, 220, 255), outline=LINE, width=8); [d.dot(x + sg * 110, 850, 60, (110, 70, 50, 255)) for sg in (-1, 1)]
    d.stroke([(0, 150), (1200, 230), (W2, 150)], LINE, 5)
    for x in range(30, W2, 90): y = 160 + 70 * math.sin(x / W2 * math.pi); d.poly([(x, y), (x + 60, y), (x + 30, y + 70)], fill=[TURQ, YEL, WT][(x // 90) % 3])
    fl(d, (200, 150, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 640, 520, (255, 220, 150, 110), 100); im.convert('RGB').save(path)


def fireflies(path):                                         # honey-gold dusk meadow with fireflies and a fence
    im = sky((240, 150, 80), (255, 220, 140), 1.0); d = Draw(W2, H2); hills(d, 760, (160, 140, 70, 255), 60, 3)
    for x in (200, 2200): ptree(d, x, 900, 1.5, (110, 140, 60, 255))
    r = np.random.RandomState(9); [d.dot(r.randint(0, W2), r.randint(200, 900), r.choice([8, 10, 14]), (255, 250, 170, 255)) for _ in range(70)]
    fl(d, (170, 140, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def court(path):                                             # 1858 oxblood courtroom: wood panels, tall windows, green lamps
    im = sky((120, 40, 50), (190, 90, 80), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.rrect(x + 30, 560, x + 270, 900, 10, outline=(90, 30, 36, 255), width=12)
    for x in (400, 1200, 2000): d.chord(x, 220, 160, 160, 180, 360, fill=(220, 240, 250, 255)); d.rect(x - 160, 220, x + 160, 500, (220, 240, 250, 255)); d.rrect(x - 160, 60, x + 160, 500, 2, outline=GOLD, width=16); d.stroke([(x, 60), (x, 500)], GOLD, 10)
    for x in (800, 1600): d.rect(x - 6, 0, x + 6, 260, LINE); d.chord(x, 300, 90, 60, 180, 360, fill=(60, 170, 110, 255), outline=LINE, width=8)
    fl(d, (150, 90, 70, 255)); im.alpha_composite(d.out()); [glow(im, x, 320, 200, (220, 255, 200, 110), 60) for x in (800, 1600)]; im.convert('RGB').save(path)


def jail(path):                                              # lilac stone jail: block wall, barred window with a moon, little cot
    im = sky((140, 130, 180), (200, 190, 230), 1.0); d = Draw(W2, H2)
    for j, y in enumerate(range(40, 940, 110)):
        for x in range(-100 + (j % 2) * 120, W2, 240): d.rrect(x + 6, y + 6, x + 234, y + 104, 16, fill=(170, 160, 205, 255), outline=(130, 120, 170, 255), width=6)
    d.rrect(900, 150, 1500, 560, 20, fill=(60, 80, 160, 255), outline=LINE, width=14); d.dot(1340, 280, 60, (255, 246, 200, 255)); [d.rect(x - 14, 150, x + 14, 560, (90, 90, 110, 255)) for x in range(990, 1500, 100)]
    d.rrect(1700, 700, 2200, 820, 20, fill=(240, 120, 140, 255), outline=LINE, width=10); [d.rect(x, 820, x + 30, 940, (90, 80, 100, 255)) for x in (1720, 2150)]
    fl(d, (130, 120, 150, 255)); im.alpha_composite(d.out()); glow(im, 1200, 350, 400, (220, 230, 255, 90), 90); im.convert('RGB').save(path)


def moonfield(path):                                         # bright navy moon meadow: stars, silver hills, a haystack
    im = sky((40, 70, 150), (110, 150, 210), 1.0); d = Draw(W2, H2); stars(d, 110, 600, 11)
    hills(d, 700, (70, 110, 150, 255), 80, 3); hills(d, 800, (60, 120, 110, 255), 50, 4, 0.7); d.chord(1900, 900, 200, 180, 180, 360, fill=(220, 190, 110, 255), outline=LINE, width=8)
    fl(d, (90, 130, 120, 255)); im.alpha_composite(d.out()); glow(im, 1200, 600, 900, (220, 230, 255, 60), 200); im.convert('RGB').save(path)


def study(path):                                             # amber candlelit study: bookshelves, window, candle glow
    im = sky((200, 120, 50), (255, 200, 120), 1.0); d = Draw(W2, H2)
    for x0 in (60, 1700):
        d.rect(x0, 80, x0 + 640, 900, (130, 80, 50, 255))
        for y in range(120, 880, 160): d.rect(x0 + 20, y + 130, x0 + 620, y + 150, (100, 60, 40, 255)); [d.rect(x0 + 30 + k * 60, y + 10 + (k % 3) * 10, x0 + 80 + k * 60, y + 130, [(200, 70, 60, 255), (60, 130, 100, 255), (230, 180, 80, 255), (90, 100, 180, 255)][k % 4]) for k in range(10)]
    d.rrect(950, 160, 1450, 600, 20, fill=(60, 80, 150, 255), outline=(110, 70, 40, 255), width=24); d.dot(1300, 300, 50, (255, 246, 200, 255))
    fl(d, (150, 100, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 700, 500, (255, 210, 120, 110), 120); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast4(('abe', 'abe58', 'abey', 'jack', 'thompson', 'duff', 'witness'))
    multi = dict(belt={'default': belt()}, masked={'default': masked(), 'no': masked(True)}, ruler={'default': ruler()}, flop={'default': flop()}, brawl={'default': brawl()},
                 crowd={'default': crowd(), 'cheer': crowd(True)}, bets={'default': bets()}, pals={'default': pals()}, bench={'default': bench(), 'bang': bench(True)},
                 tag={'default': tag()}, moon={k: moon(k) for k in ('default', 'q', 'set')}, almanac={'default': almanac(), 'open': almanac('open')})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ, RB = (110, 50, 140, 255), (30, 130, 130, 255), (170, 50, 60, 255)
    cards = dict(hookc=neon3('A PRESIDENT IN THE', 'WRESTLING', 'HALL OF FAME!'),
                 notpro=stamp('NOT A PRO!', 700, RB, 150, -4),
                 abec=P_('ABRAHAM', 'LINCOLN', PU, 880, 130, 190, YEL),
                 ft64=M.bigneon('6 FT 4', 'FRONTIER WRESTLER', 900, YEL, CYAN),
                 y1832=M.cal('ONE LOSS', '1832', RB),
                 thomp=P_('A SOLDIER', 'NAMED THOMPSON', (40, 70, 150, 255), 920, 120, 120, YEL),
                 salemc=stamp('NEW SALEM', 760, TQ, 150, 3),
                 jackc=P_('JACK', 'ARMSTRONG', (150, 90, 50, 255), 860, 130, 180, YEL),
                 betc=M.bigneon('CROWDS', 'BET MONEY!', 800, YEL, (120, 230, 140, 255)),
                 friendc=stamp('HIS FRIEND!', 720, (230, 80, 120, 255), 150, 4),
                 y1858=M.cal('TRIAL', '1858', OX),
                 duffc=P_("JACK'S SON", 'DUFF', (60, 120, 170, 255), 820, 130, 200, YEL),
                 freec=M.bigneon('FOR', 'FREE!', 640, YEL, (120, 230, 140, 255)),
                 moonc=stamp('BY MOONLIGHT?', 860, NAVY, 130, -3),
                 setc=stamp('ALMOST SET!', 760, PU, 150, 4),
                 notg=M.bigneon('NOT', 'GUILTY!', 700, YEL, CYAN),
                 savedc=P_('WON A FRIEND,', 'SAVED HIS SON', TQ, 960, 120, 130, YEL))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    CE.tiles(T('mat.jpg'), (40, 190, 180), (34, 172, 164)); CE.tiles(T('marble.jpg'), (230, 240, 236), (214, 226, 222)); M.sandtex(T('prairie.jpg'), (190, 170, 90), (176, 156, 80)); M.sandtex(T('campdirt.jpg'), (170, 136, 110), (156, 124, 100))
    M.sandtex(T('grass.jpg'), (120, 170, 110), (108, 156, 100)); M.sandtex(T('dust.jpg'), (210, 160, 120), (196, 148, 110)); M.sandtex(T('meadow.jpg'), (180, 150, 80), (166, 138, 72)); CE.tiles(T('courtfl.jpg'), (170, 100, 80), (156, 90, 72))
    CE.tiles(T('stone.jpg'), (150, 140, 180), (136, 126, 166)); M.sandtex(T('nightgr.jpg'), (90, 130, 130), (80, 120, 120)); CE.tiles(T('studyfl.jpg'), (170, 110, 70), (156, 100, 62)); CE.tiles(T('pave.jpg'), (120, 100, 90), (106, 88, 78))
    B.tex_wood(T('wood.jpg')); G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(arena=arena, trophyhall=trophyhall, prairie=prairie, camp=camp, salem=salem, duskring=duskring, fireflies=fireflies, court=court, jail=jail, moonfield=moonfield, study=study)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
