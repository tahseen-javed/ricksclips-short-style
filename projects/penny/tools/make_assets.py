#!/usr/bin/env python3
"""Assets for video 26: the penny cost almost 4 cents to make 1 cent - and made a fortune at auction the day it died.
Copper-candy money world: lilac-pink Mint press hall (hook + loop), mint-green Mint facade, plum piggy vault, pastel penny town, buttercup kitchen,
teal living room, magenta sunset parking lot, cyan spotlight stage, sky-blue highway, autumn Philadelphia dusk, red-velvet auction house, pink-gold
sunset cloud heaven. Cute cast (new): Mint press worker (pompom beanie, overalls), couch kid (propeller beanie, hoodie), auctioneer (headset, waistcoat).
The penny itself is the hero (glossy coin with big shiny eyes). usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v26_assets import *

ROOT = B.ROOT
COP, COPD, MAG, MINT, GOLD = (226, 128, 64, 255), (176, 86, 40, 255), (255, 60, 172, 255), (90, 220, 180, 255), (255, 206, 60, 255)
LA.NEW.update({
    'mintw': dict(sk=1, style='curly', hair=(60, 40, 30, 255), suit=(80, 130, 210, 255), shade=(60, 104, 180, 255), body='overalls', acc=(255, 210, 90, 255), xhat='beanie', hatc=(40, 200, 180, 255)),
    'kid': dict(sk=0, style='spiky', hair=(230, 150, 60, 255), suit=(255, 120, 170, 255), shade=(224, 92, 140, 255), body='hoodie', xhat='propeller', hatc=(120, 90, 230, 255), hatc2=YEL),
    'auct': dict(sk=2, style='slick', hair=(30, 24, 30, 255), suit=(230, 180, 60, 255), shade=(200, 150, 40, 255), body='waistcoat', acc=RED, xhat='headset', stache=(30, 24, 30, 255)),
})


def penny(mode='happy'):                                     # the hero: big glossy penny (faces: happy, shocked, sad, crown, halo, gold)
    d = Draw(1000, 1300); im = Image.new('RGBA', (1000, 1300))
    if mode == 'halo':
        for sg in (-1, 1): d.ellipse(500 + sg * 430, 720, 150, 230, fill=WT, outline=LINE, width=12)
        d.ellipse(500, 180, 260, 60, outline=GOLD, width=34); d.ellipse(500, 180, 260, 60, outline=LINE, width=6)
    if mode == 'gold': d.dot(500, 760, 520, (255, 236, 150, 120))
    col, rim = ((250, 200, 70, 255), (210, 150, 30, 255)) if mode in ('gold', 'crown') else (COP, COPD)
    coin(d, 500, 760, 420, {'crown': 'happy', 'gold': 'happy', 'halo': 'happy'}.get(mode, mode), col, rim)
    d.text(500, 1060, 'ONE CENT', 70, dk(rim, 0.7))
    if mode == 'crown':
        d.poly([(320, 380), (360, 200), (430, 320), (500, 160), (570, 320), (640, 200), (680, 380)], fill=GOLD, outline=LINE, width=12); [d.dot(x, y, 22, c) for x, y, c in ((500, 300, RED), (400, 330, MINT), (600, 330, MAG))]
    return d.out()


def press(slam=False):                                       # coin press with a cute face; slam: ram down + sparks + a fresh penny
    d = Draw(1100, 1500); y = 520 if slam else 300
    d.rrect(140, 60, 960, 260, 40, fill=(150, 110, 220, 255), outline=LINE, width=16); [d.rect(x, 240, x + 70, 1300, (120, 90, 190, 255)) for x in (180, 850)]
    [d.rect(x, 240, x + 70, 1300, LINE) for x in ()]; d.rrect(380, 240, 720, y + 160, 30, fill=(200, 200, 214, 255), outline=LINE, width=14); d.rrect(330, y + 140, 770, y + 260, 30, fill=COPD, outline=LINE, width=14)
    d.rrect(100, 1220, 1000, 1440, 40, fill=(150, 110, 220, 255), outline=LINE, width=16); eyes(d, 550, 150, 0.8, 'shocked' if slam else 'happy')
    coin(d, 550, 1120, 110, '', COP, COPD)
    if slam:
        for a in range(0, 360, 40): r_ = math.radians(a); d.stroke([(550 + 150 * math.cos(r_), 1000 + 60 * math.sin(r_)), (550 + 260 * math.cos(r_), 1000 + 110 * math.sin(r_))], GOLD, 16)
    return d.out()


def prow():                                                  # conveyor of fresh pennies, each a little worried
    d = Draw(1800, 700); d.rrect(40, 420, 1760, 560, 60, fill=(80, 80, 100, 255), outline=LINE, width=14); [d.dot(x, 490, 40, (160, 160, 180, 255)) for x in range(140, 1700, 180)]
    for k, x in enumerate(range(220, 1700, 330)): coin(d, x, 290, 130, 'shocked' if k % 2 else 'sad', COP, COPD)
    return d.out()


def scale(tip=False):                                        # balance: WORTH 1c vs COST 4c (tip: the cost side drops)
    d = Draw(1500, 1200); a = 14 if tip else 0; r_ = math.radians(a); cx, cy = 750, 300
    d.rrect(600, 1060, 900, 1160, 30, fill=(120, 90, 190, 255), outline=LINE, width=12); d.rect(725, 300, 775, 1080, (180, 150, 230, 255))
    L_, R_ = (cx - 560 * math.cos(r_), cy - 560 * math.sin(r_)), (cx + 560 * math.cos(r_), cy + 560 * math.sin(r_)); d.stroke([L_, R_], LINE, 26); d.stroke([L_, R_], (250, 220, 120, 255), 14)
    for (x, y), lab, big in ((L_, 'WORTH', False), (R_, 'COST', True)):
        d.stroke([(x, y), (x - 120, y + 300)], LINE, 6); d.stroke([(x, y), (x + 120, y + 300)], LINE, 6); d.chord(x, y + 300, 170, 70, 0, 180, fill=(250, 220, 120, 255), outline=LINE, width=12)
        if big: d.dot(x, y + 210, 120, (120, 200, 120, 255)); d.ellipse(x, y + 210, 120, 120, outline=LINE, width=10); d.text(x, y + 215, '4¢', 120, WT, stroke=6, stroke_fill=LINE)
        else: coin(d, x, y + 250, 60, '', COP, COPD); d.text(x, y + 252, '1¢', 50, WT, stroke=4, stroke_fill=LINE)
        d.text(x, y + 440, lab, 90, WT, stroke=6, stroke_fill=LINE)
    d.dot(cx, cy, 40, GOLD); eyes(d, 750, 700, 0.6, 'shocked' if tip else 'happy'); return d.out()


def mintb():                                                 # U.S. MINT building with columns and a big sign
    d = Draw(1700, 1200); d.poly([(80, 360), (850, 80), (1620, 360)], fill=(250, 246, 236, 255), outline=LINE, width=16); d.rect(120, 360, 1580, 1100, (240, 236, 226, 255)); d.rect(80, 1080, 1620, 1180, (210, 206, 196, 255))
    for x in range(220, 1600, 210): d.rect(x - 40, 520, x + 40, 1080, WT); d.rect(x - 52, 500, x + 52, 540, (220, 216, 206, 255)); d.stroke([(x - 20, 560), (x - 20, 1060)], (226, 222, 212, 255), 8)
    d.rrect(330, 370, 1370, 500, 24, fill=(40, 120, 100, 255), outline=LINE, width=12); d.text(850, 436, 'U.S. MINT', 110, YEL, stroke=6, stroke_fill=LINE); coin(d, 850, 250, 80, 'happy', COP, COPD)
    d.ellipse(850, 1130, 760, 40, outline=LINE, width=10); return d.out()


def piggy(leak=False):                                       # pink piggy bank (leak: crack + coins tumbling out, sad)
    d = Draw(1500, 1200); PK_ = (255, 160, 200, 255)
    for x in (430, 1050): d.rrect(x - 60, 820, x + 60, 1040, 30, fill=dk(PK_, 0.9), outline=LINE, width=12)
    d.ellipse(740, 600, 560, 400, fill=PK_, outline=LINE, width=16); d.ellipse(1240, 600, 110, 130, fill=(255, 190, 220, 255), outline=LINE, width=12); [d.dot(1220 + sg * 34, 600, 18, LINE) for sg in (-1, 1)]
    d.poly([(520, 280), (580, 120), (660, 250)], fill=PK_, outline=LINE, width=12); d.rrect(640, 230, 840, 260, 14, fill=LINE); eyes(d, 1010, 480, 0.8, 'sad' if leak else 'happy'); d.ellipse(560, 420, 140, 50, fill=(255, 255, 255, 110))
    if leak:
        d.stroke([(700, 1000), (760, 880), (720, 800), (800, 700)], LINE, 12)
        for k, (x, y) in enumerate(((700, 1080), (820, 1130), (600, 1150), (900, 1060))): coin(d, x, y, 52, '', COP, COPD)
    return d.out()


def printer():                                               # money printer spitting out winged bills that fly away
    d = Draw(1500, 1300); d.rrect(200, 500, 1100, 1200, 50, fill=(90, 200, 160, 255), outline=LINE, width=16); d.rrect(260, 560, 1040, 700, 20, fill=(40, 60, 70, 255), outline=LINE, width=10)
    d.rect(300, 600, 1000, 660, (120, 230, 190, 255)); eyes(d, 650, 900, 0.9, 'shocked'); [d.dot(x, 1100, 30, c) for x, c in ((400, RED), (500, YEL), (900, MAG))]
    out = d.out()
    for x, y, a in ((560, 380, -10), (900, 240, 12), (1200, 120, -14), (300, 200, 8)):
        b = Draw(600, 300); [b.ellipse(300 + sg * 200, 90, 80, 40, fill=WT, outline=LINE, width=8) for sg in (-1, 1)]; b.rrect(130, 60, 470, 250, 20, fill=(140, 220, 150, 255), outline=LINE, width=10)
        b.dot(300, 155, 50, (100, 180, 110, 255)); b.text(300, 157, '$', 80, WT, stroke=4, stroke_fill=LINE); bo = b.out().rotate(a, expand=True)
        out.alpha_composite(bo, (max(0, int(x - bo.width / 2)), max(0, int(y - bo.height / 2))))
    return out


def pile():                                                  # mountain of 300 billion pennies with a few cheeky faces
    d = Draw(1800, 1000); r = np.random.RandomState(5)
    for k in range(260):
        x = r.randint(80, 1720); h_ = 900 - (1 - abs(x - 900) / 900) * 640; y = r.randint(int(h_), 960); coin(d, x, y, r.randint(40, 70), '', COP if k % 3 else (240, 150, 80, 255), COPD)
    for x, y in ((900, 340), (600, 560), (1240, 600)): coin(d, x, y, 110, 'happy', COP, COPD)
    return d.out()


def jar():                                                   # glass jar stuffed with pennies, cute face on the label
    d = Draw(1000, 1300); d.rrect(150, 260, 850, 1250, 140, fill=(200, 236, 255, 120), outline=LINE, width=16); d.rrect(260, 140, 740, 280, 30, fill=(240, 120, 90, 255), outline=LINE, width=14)
    r = np.random.RandomState(2); [coin(d, r.randint(230, 770), r.randint(560, 1170), 52, '', COP, COPD) for _ in range(46)]
    d.rrect(300, 380, 700, 560, 30, fill=WT, outline=LINE, width=10); eyes(d, 500, 450, 0.6, 'happy'); d.rrect(190, 300, 230, 1100, 20, fill=(255, 255, 255, 150)); return d.out()


def couch(lift=False):                                       # coral couch; lift: cushion pops up, pennies peek out with eyes
    d = Draw(1700, 1100); C_ = (255, 120, 100, 255)
    d.rrect(80, 260, 1620, 760, 80, fill=C_, outline=LINE, width=16); d.rrect(40, 520, 260, 1000, 60, fill=dk(C_, 0.9), outline=LINE, width=14); d.rrect(1440, 520, 1660, 1000, 60, fill=dk(C_, 0.9), outline=LINE, width=14)
    d.rrect(220, 760, 1480, 1000, 40, fill=dk(C_, 0.85), outline=LINE, width=14)
    for k, x in enumerate((560, 1140)):
        if lift and k == 0:
            for j, px in enumerate((420, 560, 700)): coin(d, px, 700, 70, 'shocked' if j == 1 else 'happy', COP, COPD)
            d.rrect(x - 320, 380, x + 300, 560, 50, fill=(255, 160, 140, 255), outline=LINE, width=14)
        else: d.rrect(x - 290, 620, x + 290, 800, 50, fill=(255, 160, 140, 255), outline=LINE, width=14)
    return d.out()


def car():                                                   # tiny cute hatchback
    d = Draw(1300, 800); d.rrect(60, 340, 1240, 640, 90, fill=(90, 190, 250, 255), outline=LINE, width=16); d.chord(620, 360, 380, 250, 180, 360, fill=(90, 190, 250, 255), outline=LINE, width=16)
    d.chord(620, 360, 300, 190, 180, 360, fill=(210, 240, 255, 255)); d.stroke([(620, 170), (620, 360)], LINE, 10)
    for x in (300, 960): d.dot(x, 640, 120, (50, 50, 60, 255)); d.dot(x, 640, 50, (200, 200, 210, 255))
    eyes(d, 1120, 460, 0.5, 'happy'); d.dot(1210, 430, 30, YEL); return d.out()


def thermo(n=1):                                             # cost-o-meter thermometer, n = 1..4 cents (mercury rises, face sweats)
    d = Draw(700, 1500); d.rrect(230, 60, 470, 1260, 120, fill=WT, outline=LINE, width=16); d.dot(350, 1300, 170, RED); d.ellipse(350, 1300, 170, 170, outline=LINE, width=16)
    top = 1180 - n * 250; d.rrect(290, top, 410, 1200, 60, fill=RED)
    for k in range(1, 5): y = 1180 - k * 250; d.stroke([(470, y), (540, y)], LINE, 10); d.text(610, y, '%d¢' % k, 80, LINE)
    eyes(d, 350, 1290, 0.55, 'shocked' if n >= 3 else 'happy')
    if n >= 3: d.ellipse(160, 200, 26, 40, fill=(150, 210, 255, 255), outline=LINE, width=6)
    return d.out()


def ledger():                                                # 'manage it': chunky clipboard ledger with a pencil
    d = Draw(1000, 1200); d.rrect(120, 120, 880, 1140, 40, fill=(160, 110, 70, 255), outline=LINE, width=16); d.rrect(190, 220, 810, 1080, 20, fill=WT, outline=LINE, width=10)
    d.rrect(380, 70, 620, 190, 20, fill=(200, 200, 214, 255), outline=LINE, width=10)
    for y in (560, 660, 760, 860, 960): d.stroke([(250, y), (750, y)], (190, 190, 210, 255), 10); d.text(700, y - 28, '¢', 60, COPD)
    eyes(d, 500, 380, 0.75, 'shocked'); d.stroke([(820, 1100), (980, 760)], (255, 200, 60, 255), 40); d.stroke([(820, 1100), (980, 760)], LINE, 6); return d.out()


def vantr():                                                 # 'ship it': cute armoured coin van
    d = Draw(1600, 1000); d.rrect(80, 260, 1180, 800, 50, fill=(150, 170, 200, 255), outline=LINE, width=16); d.rrect(1160, 420, 1520, 800, 60, fill=(150, 170, 200, 255), outline=LINE, width=16)
    d.rrect(1240, 460, 1460, 600, 20, fill=(210, 240, 255, 255), outline=LINE, width=10); coin(d, 620, 520, 170, 'happy', COP, COPD)
    for x in (360, 1300): d.dot(x, 820, 120, (50, 50, 60, 255)); d.dot(x, 820, 50, (200, 200, 210, 255))
    for y in (380, 520, 660): d.stroke([(0, y), (60, y)], WT, 14)
    return d.out()


def hall():                                                  # Philadelphia brick hall with a white clock tower
    d = Draw(1500, 1500); d.rect(150, 700, 1350, 1440, (190, 80, 60, 255)); d.rect(150, 1400, 1350, 1460, (120, 50, 40, 255)); d.stroke([(150, 700), (1350, 700)], LINE, 14)
    d.rect(560, 260, 940, 700, (180, 72, 56, 255)); d.rect(600, 140, 900, 300, WT); d.poly([(620, 140), (750, 10), (880, 140)], fill=(90, 150, 120, 255), outline=LINE, width=12)
    d.dot(750, 470, 120, WT); d.ellipse(750, 470, 120, 120, outline=LINE, width=12); d.stroke([(750, 470), (750, 390)], LINE, 12); d.stroke([(750, 470), (810, 470)], LINE, 12)
    for x in range(230, 1300, 160):
        if 540 < x < 960: continue
        win(d, x, 860, x + 90, 1040, (255, 230, 150, 255)); win(d, x, 1160, x + 90, 1340, (255, 230, 150, 255))
    d.rrect(660, 1180, 840, 1440, 80, fill=(90, 60, 50, 255), outline=LINE, width=10); return d.out()


def podium():                                                # auction podium with a gavel and an AUCTION plate
    d = Draw(1200, 1100); d.poly([(220, 300), (980, 300), (900, 1060), (300, 1060)], fill=(130, 40, 50, 255), outline=LINE, width=16); d.rrect(160, 240, 1040, 340, 30, fill=(90, 30, 40, 255), outline=LINE, width=14)
    d.rrect(340, 500, 860, 680, 24, fill=GOLD, outline=LINE, width=12); d.text(600, 590, 'AUCTION', 100, (120, 30, 40, 255))
    d.rrect(700, 140, 960, 220, 30, fill=(150, 100, 60, 255), outline=LINE, width=10); d.rect(820, 210, 850, 300, (120, 80, 50, 255)); return d.out()


def cases():                                                 # 232 sets: rows of velvet display cases, each with five shiny pennies
    d = Draw(1700, 1100)
    for j in range(3):
        for i in range(4):
            x, y = 230 + i * 410, 200 + j * 330; d.rrect(x - 180, y - 130, x + 180, y + 130, 24, fill=(30, 40, 90, 255), outline=GOLD, width=14)
            [coin(d, x - 120 + k * 60, y, 36, '', (250, 190, 90, 255) if (i + j) % 2 else COP, COPD) for k in range(5)]
    return d.out()


def crowd():                                                 # tiny chibi bidders waving numbered paddles
    d = Draw(1800, 900); r = np.random.RandomState(7); cols = [(255, 150, 60, 255), (120, 200, 240, 255), (170, 120, 230, 255), (90, 210, 150, 255), (255, 120, 170, 255)]
    for k in range(7):
        x = 160 + k * 245; y = 520 + (k % 2) * 60; c = cols[k % 5]
        d.stroke([(x + 60, y - 40), (x + 120, y - 240)], LINE, 12); d.dot(x + 130, y - 300, 70, WT); d.ellipse(x + 130, y - 300, 70, 70, outline=LINE, width=10); d.text(x + 130, y - 298, str(10 + k * 7), 60, LINE)
        d.rrect(x - 110, y + 80, x + 110, y + 380, 70, fill=c, outline=LINE, width=12); d.dot(x, y, 110, (255, 220, 190, 255)); d.ellipse(x, y, 110, 110, outline=LINE, width=12)
        d.chord(x, y - 10, 112, 100, 180, 360, fill=(60 + k * 20, 40 + k * 10, 30, 255)); eyes(d, x, y + 20, 0.45, 'shocked' if k % 3 == 0 else 'happy')
    return d.out()


def qlot(open_=False):                                       # open loop: velvet-draped auction lot with "?" -> golden penny set with a $ tag
    d = Draw(1200, 1300); d.rrect(200, 1060, 1000, 1240, 30, fill=(90, 30, 40, 255), outline=LINE, width=14)
    if open_:
        d.dot(600, 620, 520, (255, 236, 150, 120)); d.rrect(220, 380, 980, 1060, 40, fill=(30, 40, 90, 255), outline=GOLD, width=20)
        for j in range(2):
            for i in range(3): coin(d, 360 + i * 240, 560 + j * 280, 100, 'happy', (250, 200, 70, 255), (210, 150, 30, 255))
        d.rrect(680, 80, 1140, 300, 30, fill=GOLD, outline=LINE, width=14); d.text(910, 192, 'SOLD!', 110, (150, 30, 40, 255))
    else:
        d.poly([(200, 1060), (300, 320), (600, 220), (900, 320), (1000, 1060)], fill=(170, 30, 60, 255), outline=LINE, width=16); d.poly([(560, 240), (600, 120), (640, 240)], fill=GOLD, outline=LINE, width=10)
        d.text(600, 680, '?', 420, GOLD, stroke=12, stroke_fill=LINE)
    return d.out()


def throne():                                                # golden throne with coin stacks and falling bills
    d = Draw(1400, 1400); d.rrect(300, 120, 1100, 900, 120, fill=GOLD, outline=LINE, width=16); d.rrect(380, 200, 1020, 820, 90, fill=(170, 30, 60, 255))
    d.rrect(220, 820, 1180, 1100, 40, fill=GOLD, outline=LINE, width=16); d.rect(300, 1100, 380, 1360, GOLD); d.rect(1020, 1100, 1100, 1360, GOLD)
    for x in (120, 1280):
        for k in range(6): d.ellipse(x, 1320 - k * 50, 100, 30, fill=(250, 200, 70, 255), outline=LINE, width=8)
    shine(d, 340, 200, 500); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def presshall(path):                                         # hook: lilac-pink Mint press hall, copper coil rolls, pipes, warm lamps
    im = sky((150, 110, 220), (255, 170, 200), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.rect(x, 0, x + 26, 940, (120, 86, 180, 255))
    for x, y, r in ((300, 760, 200), (640, 800, 150), (1900, 760, 210), (2200, 810, 140)): d.dot(x, y, r, COP); [d.ellipse(x, y, r - k * 30, r - k * 30, outline=COPD, width=8) for k in range(0, min(6, r // 30))]; d.dot(x, y, 40, LINE)
    d.stroke([(0, 220), (W2, 220)], (200, 200, 220, 255), 30); d.stroke([(0, 300), (W2, 300)], (180, 180, 200, 255), 18)
    for x in (600, 1200, 1800): d.stroke([(x, 0), (x, 120)], LINE, 6); d.chord(x, 160, 90, 60, 180, 360, fill=(60, 50, 80, 255)); d.dot(x, 170, 30, (255, 240, 180, 255))
    fl(d, (120, 90, 160, 255)); im.alpha_composite(d.out()); [glow(im, x, 220, 220, (255, 230, 170, 110), 60) for x in (600, 1200, 1800)]; im.convert('RGB').save(path)


def mintsky(path):                                           # mint-green morning, cream skyline, round trees
    im = sky((110, 220, 190), (255, 246, 220), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 200)): h_ = 260 + (k * 97) % 260; d.rect(x, 900 - h_, x + 170, 940, (236, 230, 214, 255)); [d.rect(x + 30, 900 - h_ + 40 + j * 70, x + 70, 900 - h_ + 80 + j * 70, (200, 230, 220, 255)) for j in range(h_ // 90)]
    for x in range(100, W2, 380): ptree(d, x, 940, 1.0, (70, 170, 110, 255))
    fl(d, (90, 170, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def vault(path):                                             # plum vault: round vault door, gold coin stacks, spotlights
    im = sky((70, 30, 90), (170, 80, 140), 1.0); d = Draw(W2, H2); d.dot(1200, 480, 420, (110, 110, 130, 255)); d.dot(1200, 480, 340, (150, 150, 170, 255)); d.ellipse(1200, 480, 420, 420, outline=LINE, width=14)
    for a in range(0, 360, 45): r_ = math.radians(a); d.stroke([(1200, 480), (1200 + 300 * math.cos(r_), 480 + 300 * math.sin(r_))], (100, 100, 120, 255), 20)
    d.dot(1200, 480, 80, (200, 200, 214, 255))
    for x in (240, 480, 1920, 2160): [d.ellipse(x, 920 - k * 40, 90, 26, fill=(250, 200, 70, 255), outline=LINE, width=6) for k in range(10)]
    fl(d, (90, 40, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 480, 500, (255, 220, 160, 70), 120); im.convert('RGB').save(path)


def pastel(path):                                            # pastel town sky: blue to peach, soft hills, cloud puffs
    im = sky((130, 190, 250), (255, 214, 190), 1.0); d = Draw(W2, H2); hills(d, 700, (150, 210, 160, 255), 60, 3); hills(d, 800, (120, 190, 140, 255), 50, 4, 1.2)
    for x, y in ((400, 200), (1300, 140), (2000, 240)): [d.dot(x + k * 80, y + (k % 2) * 20, 70, (255, 255, 255, 230)) for k in range(4)]
    fl(d, (130, 200, 140, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def kitchen(path):                                           # buttercup kitchen: tiles, shelf, window, hanging pans
    im = sky((255, 214, 90), (255, 240, 180), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 100):
        for y in range(560, 940, 100): d.rect(x + 4, y + 4, x + 96, y + 96, (255, 250, 236, 255))
    win(d, 1500, 140, 2000, 520, (150, 220, 255, 255)); d.rect(200, 470, 1200, 500, (170, 110, 70, 255))
    for x, c in ((300, RED), (500, (90, 200, 160, 255)), (700, (120, 90, 230, 255))): d.stroke([(x, 120), (x, 250)], LINE, 8); d.dot(x, 300, 70, c); d.ellipse(x, 300, 70, 70, outline=LINE, width=8)
    fl(d, (200, 150, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def living(path):                                            # teal striped living room, floor lamp, frames, window
    im = sky((40, 150, 160), (90, 200, 200), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 50, 940, (70, 180, 186, 255))
    win(d, 1700, 160, 2150, 600, (255, 200, 160, 255)); d.rrect(300, 180, 600, 420, 20, fill=(255, 220, 120, 255), outline=LINE, width=12); d.rrect(700, 220, 900, 400, 20, fill=(255, 150, 170, 255), outline=LINE, width=12)
    d.stroke([(1300, 940), (1300, 300)], LINE, 14); d.chord(1300, 320, 140, 120, 180, 360, fill=(255, 230, 150, 255), outline=LINE, width=10)
    fl(d, (170, 110, 80, 255)); im.alpha_composite(d.out()); glow(im, 1300, 300, 260, (255, 240, 180, 110), 60); im.convert('RGB').save(path)


def parklot(path):                                           # magenta-orange sunset, city silhouette, light poles
    im = sky((230, 80, 150), (255, 190, 100), 1.0); d = Draw(W2, H2); d.dot(1200, 820, 220, (255, 230, 160, 255))
    for k, x in enumerate(range(0, W2, 160)): h_ = 200 + (k * 131) % 300; d.rect(x, 900 - h_, x + 140, 940, (120, 50, 110, 255))
    for x in range(200, W2, 600): d.rect(x, 380, x + 20, 940, (60, 40, 70, 255)); d.rrect(x - 40, 360, x + 60, 400, 14, fill=(255, 240, 180, 255))
    fl(d, (90, 80, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 820, 420, (255, 220, 160, 110), 100); im.convert('RGB').save(path)


def cyanstage(path):                                         # cyan spotlight stage with sparkles
    im = sky((16, 50, 80), (30, 150, 170), 1.0); d = Draw(W2, H2); stars(d, 70, 700, 9)
    for x in (600, 1200, 1800): d.poly([(x - 50, 0), (x + 50, 0), (x + 320, 940), (x - 320, 940)], fill=(200, 255, 250, 45))
    fl(d, (30, 70, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 760, 480, (180, 255, 240, 80), 100); im.convert('RGB').save(path)


def highway(path):                                           # sky-blue highway: green hills, clouds, road
    im = sky((90, 170, 250), (220, 240, 255), 1.0); d = Draw(W2, H2); hills(d, 620, (120, 200, 120, 255), 90, 3); hills(d, 740, (90, 170, 100, 255), 60, 5, 0.7)
    for x, y in ((300, 160), (1500, 220)): [d.dot(x + k * 90, y + (k % 2) * 24, 80, (255, 255, 255, 240)) for k in range(4)]
    d.rect(0, 860, W2, 940, (90, 90, 110, 255)); [d.rect(x, 895, x + 100, 905, WT) for x in range(0, W2, 220)]
    fl(d, (100, 100, 120, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def philly(path):                                            # autumn dusk Philadelphia: brick rows, orange trees, violet sky
    im = sky((110, 70, 150), (255, 160, 100), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 260)): h_ = 380 + (k % 3) * 60; d.rect(x, 940 - h_, x + 240, 940, (170 + (k % 2) * 20, 70, 60, 255)); [win(d, x + 40 + j * 100, 940 - h_ + 60, x + 100 + j * 100, 940 - h_ + 150, (255, 220, 140, 255)) for j in range(2)]
    for x in range(120, W2, 420): ptree(d, x, 940, 1.1, (240, 130, 50, 255), fruit=(255, 200, 80, 255))
    fl(d, (120, 80, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def velvet(path):                                            # red velvet auction house: curtains, gold frames, chandelier
    im = sky((120, 16, 40), (210, 60, 70), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 140): d.rect(x, 0, x + 60, 940, (150, 24, 50, 255))
    for x in (500, 1900): d.rrect(x - 200, 260, x + 200, 600, 10, fill=(60, 30, 60, 255), outline=GOLD, width=26); d.dot(x, 430, 80, (255, 200, 120, 255))
    d.stroke([(1200, 0), (1200, 120)], GOLD, 8); [d.dot(1200 + k * 70, 170 + abs(k) * 10, 26, (255, 240, 180, 255)) for k in range(-3, 4)]
    fl(d, (90, 20, 40, 255)); im.alpha_composite(d.out()); glow(im, 1200, 170, 320, (255, 230, 160, 120), 80); im.convert('RGB').save(path)


def heaven(path):                                            # pink-gold sunset clouds and rays
    im = sky((255, 170, 210), (255, 230, 150), 1.0); d = Draw(W2, H2)
    for k in range(9): a = math.radians(200 + k * 16); d.poly([(1200, 700), (1200 + 2000 * math.cos(a), 700 + 2000 * math.sin(a)), (1200 + 2000 * math.cos(a + 0.12), 700 + 2000 * math.sin(a + 0.12))], fill=(255, 255, 230, 60))
    for x, y in ((200, 820), (700, 860), (1300, 840), (1900, 820), (2300, 870)): [d.dot(x + k * 110, y + (k % 2) * 30, 120, (255, 246, 250, 255)) for k in range(4)]
    fl(d, (255, 236, 240, 255)); im.alpha_composite(d.out()); glow(im, 1200, 700, 400, (255, 250, 210, 120), 100); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast3(('mintw', 'kid', 'auct'))
    multi = dict(penny={k: penny(k) for k in ('default', 'shocked', 'sad', 'crown', 'halo', 'gold')}, press={'default': press(), 'slam': press(True)}, prow={'default': prow()},
                 scale={'default': scale(), 'tip': scale(True)}, mintb={'default': mintb()}, piggy={'default': piggy(), 'leak': piggy(True)}, printer={'default': printer()},
                 pile={'default': pile()}, jar={'default': jar()}, couch={'default': couch(), 'lift': couch(True)}, car={'default': car()},
                 thermo={'default': thermo(1), **{'t%d' % k: thermo(k) for k in range(1, 5)}}, ledger={'default': ledger()}, vantr={'default': vantr()}, hall={'default': hall()},
                 podium={'default': podium()}, cases={'default': cases()}, crowd={'default': crowd()}, qlot={'default': qlot(), 'open': qlot(True)}, throne={'default': throne()})
    multi['penny']['default'] = penny('happy')
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PL, TL, CR = (110, 60, 160, 255), (30, 120, 130, 255), (170, 30, 60, 255)
    cards = dict(hookc=M.bigneon('4¢ TO MAKE', '1 CENT?!', 960, YEL, MAG),
                 every=stamp('EVERY SINGLE TIME!', 980, PL, 110, -3),
                 notonce=stamp('NOT ONCE!', 700, CR, 160, 4),
                 y2024=M.cal('U.S. MINT', '2024', TL),
                 lost85=stamp('-$85 MILLION', 900, CR, 130, -4),
                 literally=M.bigneon('LITERALLY', 'MAKING MONEY', 980, YEL, MINT),
                 b300=M.bigneon('300', 'BILLION', 760, YEL, MAG),
                 onecent=P_('ONE CENT', 'NEVER CHANGED', TL, 980, 150, 130, YEL),
                 make=stamp('MAKE IT', 640, PL, 150, -4), manage=stamp('MANAGE IT', 760, TL, 150, 3), ship=stamp('SHIP IT', 640, CR, 150, -3),
                 nov12=M.cal('NOV 12', '2025', (200, 90, 50, 255)),
                 philly=P_('PHILADELPHIA', 'THE LAST ONE', (150, 60, 50, 255), 1000, 130, 120, YEL),
                 last=M.bigneon('LAST', 'PENNY!', 760, YEL, (255, 170, 80, 255)),
                 strange=stamp('SOMETHING STRANGE...', 1000, PL, 100, -3),
                 sets232=M.bigneon('232', 'SETS', 700, YEL, MINT),
                 k800=stamp('$800,000!', 860, CR, 170, -5),
                 twenty=P_('LOST MONEY', '~20 YEARS', PL, 900, 130, 150, YEL),
                 fortune=M.bigneon('A', 'FORTUNE!', 860, YEL, MAG),
                 bye=P_('GOODBYE,', 'PENNY!', (220, 90, 140, 255), 820, 130, 170, WT))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    CE.tiles(T('steel.jpg'), (130, 110, 170), (116, 98, 154)); CE.tiles(T('marble.jpg'), (230, 226, 214), (214, 210, 198)); CE.tiles(T('plum.jpg'), (110, 50, 100), (96, 42, 88))
    M.sandtex(T('lawn.jpg'), (140, 210, 140), (124, 194, 124)); CE.tiles(T('ktile.jpg'), (250, 236, 200), (236, 220, 184)); B.tex_wood(T('wood.jpg'))
    M.sandtex(T('asphalt.jpg'), (90, 80, 110), (80, 70, 98), seed=3); CE.tiles(T('stage.jpg'), (30, 70, 100), (24, 60, 88)); M.sandtex(T('road.jpg'), (110, 110, 130), (98, 98, 116))
    CE.tiles(T('brick.jpg'), (170, 100, 80), (150, 86, 68)); CE.tiles(T('pave.jpg'), (120, 90, 160), (106, 78, 144)); CE.tiles(T('carpet.jpg'), (220, 96, 110), (204, 82, 96)); M.sandtex(T('cloud.jpg'), (255, 240, 244), (250, 228, 236))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(presshall=presshall, mintsky=mintsky, vault=vault, pastel=pastel, kitchen=kitchen, living=living, parklot=parklot, cyanstage=cyanstage, highway=highway,
                philly=philly, velvet=velvet, heaven=heaven)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
