#!/usr/bin/env python3
"""Assets for video 24: pinball was illegal in New York for 34 years; Roger Sharpe ended the ban with one called shot.
Steel-blue 1940s -> harvest-gold 1976 world: electric pinball playfield world (hook + loop), olive-cream 1942 radio stage, amber-teal bowling alley,
flashbulb night, deep-teal harbor, school-bus yellow lunch desk, sunset domino table, red-lamp back room, felt-green vs blueprint split stage,
70s wood-panel council chamber (avocado, harvest gold, burnt orange), chrome macro studio.
Cute cast (new): Mayor La Guardia (wide black hat, bow tie), a 1940s cop, a lunch-money kid, Roger Sharpe (70s plaid, aviators), three councilmen.
usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v23_assets import *

ROOT = B.ROOT
EB, CHR, GLD, AVO, ORG = (47, 123, 255, 255), (214, 222, 236, 255), (240, 190, 60, 255), (140, 150, 60, 255), (230, 110, 40, 255)
LA.NEW.update({
    'fiorello': dict(sk=0, style='slick', hair=(30, 28, 34, 255), suit=(60, 66, 90, 255), shade=(46, 50, 72, 255), body='bowtie', acc=(230, 40, 60, 255), xhat='mayor'),
    'cop40': dict(sk=1, style='part', hair=(90, 60, 40, 255), suit=(40, 50, 100, 255), shade=(30, 38, 80, 255), body='police', stache=(90, 60, 40, 255), xhat='police'),
    'lunchkid': dict(sk=2, style='spiky', hair=(40, 30, 26, 255), suit=(250, 200, 50, 255), shade=(224, 170, 30, 255), body='denim', freck=1, hat='cap'),
    'sharpe': dict(sk=0, style='curly', hair=(110, 70, 40, 255), suit=(200, 120, 50, 255), shade=(170, 96, 36, 255), body='plaid', acc=(250, 236, 200, 255), stache=(110, 70, 40, 255), xhat='shades'),
    'cncl1': dict(sk=0, style='bald', hair=(200, 190, 180, 255), suit=(130, 90, 50, 255), shade=(108, 72, 38, 255), body='suit', tie=AVO, glasses=1),
    'cncl2': dict(sk=1, style='bob', hair=(60, 40, 34, 255), suit=(140, 150, 60, 255), shade=(116, 124, 46, 255), body='cardigan', band=ORG),
    'cncl3': dict(sk=2, style='quiff', hair=(30, 26, 26, 255), suit=(230, 110, 40, 255), shade=(200, 90, 30, 255), body='suit', tie=GLD, stache=(30, 26, 26, 255)),
})


def machine(face='default', tape=False, cage=False):         # cute pinball machine: glowing backglass, bumpers, legs, face on the cabinet
    d = Draw(1100, 1500); d.rrect(150, 60, 950, 560, 40, fill=(60, 40, 120, 255), outline=LINE, width=16)
    for k, (x, y, c) in enumerate(((330, 220, YEL), (550, 180, PINK), (770, 220, CYAN), (440, 400, ORG), (660, 400, (120, 255, 140, 255)))): d.dot(x, y, 70, c); d.ellipse(x, y, 70, 70, outline=LINE, width=10); d.dot(x - 20, y - 22, 18, WT)
    d.rrect(120, 560, 980, 1080, 50, fill=EB, outline=LINE, width=16); d.poly([(160, 600), (940, 600), (900, 700), (200, 700)], fill=CHR, outline=LINE, width=10)
    for x in (230, 870): d.rect(x - 26, 1080, x + 26, 1440, (60, 60, 70, 255)); d.ellipse(x, 1440, 60, 22, fill=(60, 60, 70, 255), outline=LINE, width=8)
    shine(d, 150, 600, 300); eyes(d, 550, 850, 1.3, 'shocked' if face in ('shocked', 'dizzy') else ('sad' if face == 'sad' else 'happy'))
    if face == 'dizzy':
        for k in range(5): a = k * 2 * math.pi / 5; x, y = 550 + 260 * math.cos(a), 640 + 70 * math.sin(a); d.poly([(x + 40 * math.sin(j * math.pi / 5) * (1 if j % 2 == 0 else 0.45), y - 40 * math.cos(j * math.pi / 5) * (1 if j % 2 == 0 else 0.45)) for j in range(10)], fill=YEL, outline=LINE, width=6)
    if tape:
        for a, b in (((80, 700), (1020, 1020)), ((80, 1020), (1020, 700))): d.stroke([a, b], (255, 220, 40, 255), 90); d.stroke([a, b], LINE, 8)
    if cage:
        for x in range(120, 1000, 110): d.stroke([(x, 20), (x, 1460)], (90, 90, 100, 255), 26); d.stroke([(x, 20), (x, 1460)], LINE, 6)
        d.stroke([(100, 40), (1000, 40)], (90, 90, 100, 255), 30)
    return d.out()


def ball(q=False):                                           # glossy chrome pinball with a city reflection (q: "?" glow open loop)
    d = Draw(1000, 1000)
    if q: d.dot(500, 500, 480, (120, 170, 255, 90))
    d.dot(500, 500, 400, CHR); d.ellipse(500, 500, 400, 400, outline=LINE, width=16); d.chord(500, 560, 360, 300, 0, 180, fill=(150, 160, 190, 255))
    for k in range(6): d.rect(260 + k * 80, 520 - (k % 3) * 60, 310 + k * 80, 600, (110, 120, 150, 255))
    d.ellipse(380, 330, 130, 80, fill=(255, 255, 255, 230)); d.dot(640, 300, 30, WT)
    if q: d.text(500, 480, '?', 380, EB, stroke=10, stroke_fill=WT)
    return d.out()


def qman():                                                  # open loop: a blue silhouette with a "?"
    d = Draw(700, 1300); d.dot(350, 330, 220, (40, 60, 140, 255)); d.rrect(130, 560, 570, 1260, 160, fill=(40, 60, 140, 255))
    d.text(350, 330, '?', 300, WT, stroke=8, stroke_fill=LINE); return d.out()


def podium():                                                # 1942 radio podium with two big microphones
    d = Draw(900, 1100); d.poly([(150, 500), (750, 500), (700, 1080), (200, 1080)], fill=(200, 60, 60, 255), outline=LINE, width=14); d.rect(160, 620, 740, 680, WT)
    for x in (330, 570): d.stroke([(x, 500), (x, 260)], (60, 60, 70, 255), 20); d.rrect(x - 60, 120, x + 60, 300, 50, fill=CHR, outline=LINE, width=12); [d.stroke([(x - 50, y), (x + 50, y)], (140, 150, 170, 255), 6) for y in (170, 210, 250)]
    return d.out()


def pins():                                                  # cute bowling pins + black ball (strike!)
    d = Draw(1200, 1000)
    for k, (x, y) in enumerate(((300, 560), (500, 520), (700, 520), (900, 560), (400, 420), (600, 400), (800, 420))):
        d.ellipse(x, y + 200, 80, 200, fill=WT, outline=LINE, width=12); d.dot(x, y, 60, WT); d.ellipse(x, y, 60, 60, outline=LINE, width=12); d.rect(x - 60, y + 70, x + 60, y + 96, RED)
        d.dot(x - 20, y, 9, LINE); d.dot(x + 20, y, 9, LINE)
    d.dot(160, 820, 140, (40, 40, 60, 255)); d.ellipse(160, 820, 140, 140, outline=LINE, width=12); [d.dot(130 + j * 40, 770, 14, (90, 90, 110, 255)) for j in range(2)]
    return d.out()


def pile():                                                  # heap of seized mini machines with red tags
    d = Draw(1400, 1100); im = d.out()
    for k, (x, y, s) in enumerate(((100, 500, 0.4), (500, 470, 0.4), (900, 500, 0.4), (300, 120, 0.38), (720, 110, 0.38))):
        m = machine(('sad', 'shocked', 'sad', 'shocked', 'sad')[k]).resize((int(1100 * s), int(1500 * s))); im.alpha_composite(m, (x, y))
    d = Draw(1400, 1100)
    for x, y in ((240, 760), (640, 730), (1040, 760), (440, 380), (860, 370)): d.rrect(x, y, x + 150, y + 90, 12, fill=RED, outline=LINE, width=8); d.dot(x + 20, y + 45, 10, WT)
    im.alpha_composite(d.out()); return im


def smash():                                                 # sledgehammer bonk: dizzy machine, POW burst, flying springs + balls (cartoon, safe)
    im = Image.new('RGBA', (1400, 1500)); d = Draw(1400, 1500)
    pts = [(700 + (560 if k % 2 == 0 else 330) * math.cos(k * math.pi / 8), 520 + (420 if k % 2 == 0 else 250) * math.sin(k * math.pi / 8)) for k in range(16)]
    d.poly(pts, fill=(255, 230, 60, 255), outline=LINE, width=14); im.alpha_composite(d.out())
    im.alpha_composite(machine('dizzy').resize((770, 1050)), (315, 430)); d = Draw(1400, 1500)
    d.stroke([(1120, 120), (820, 420)], (150, 100, 60, 255), 44); d.stroke([(1120, 120), (820, 420)], LINE, 8); d.rrect(700, 300, 960, 520, 30, fill=(110, 110, 120, 255), outline=LINE, width=14)
    for x, y in ((180, 300), (1220, 640), (150, 900), (1250, 1000)): d.dot(x, y, 50, CHR); d.ellipse(x, y, 50, 50, outline=LINE, width=8)
    for x, y in ((300, 160), (1150, 860)): d.stroke([(x + j * 18, y + (j % 2) * 40) for j in range(8)], (200, 200, 210, 255), 12)
    im.alpha_composite(d.out()); return im


def newscam():                                               # newsreel camera with a flash bulb, cute face
    d = Draw(1000, 1100); d.rrect(200, 300, 800, 700, 40, fill=(60, 60, 70, 255), outline=LINE, width=14)
    for x in (330, 650): d.dot(x, 220, 130, (60, 60, 70, 255)); d.ellipse(x, 220, 130, 130, outline=LINE, width=12); d.dot(x, 220, 40, CHR)
    d.dot(500, 500, 110, (90, 160, 255, 255)); d.ellipse(500, 500, 110, 110, outline=LINE, width=12); d.dot(470, 470, 30, WT)
    d.dot(860, 330, 90, (255, 250, 200, 255)); d.ellipse(860, 330, 90, 90, outline=LINE, width=10)
    for x in (300, 500, 700): d.stroke([(500, 700), (x, 1080)], (90, 80, 70, 255), 18)
    return d.out()


def barge():                                                 # harbor barge tipping cartoon pieces into the water with a big splash
    d = Draw(1500, 1000); d.poly([(150, 600), (1250, 600), (1150, 820), (250, 820)], fill=(160, 60, 50, 255), outline=LINE, width=14); d.rect(260, 640, 1140, 680, (240, 200, 80, 255))
    for k in range(10): x = 1250 + (k % 3) * 60; y = 420 + k * 40; d.dot(x, y, 30, CHR if k % 2 else YEL); d.ellipse(x, y, 30, 30, outline=LINE, width=6)
    for k in range(7): a = math.pi * (0.1 + k * 0.13); d.ellipse(1320 + 160 * math.cos(a), 880 - 160 * math.sin(a), 30, 60, fill=(200, 240, 255, 255), outline=LINE, width=6)
    d.rect(0, 840, 1500, 1000, (40, 120, 140, 200)); eyes(d, 700, 720, 0.7, 'shocked'); return d.out()


def coins(empty=False):                                      # lunchbox + a nickel and a dime with faces (empty: sad open lunchbox)
    d = Draw(1300, 1000); d.rrect(150, 480, 1150, 960, 50, fill=(240, 60, 60, 255), outline=LINE, width=16); d.rect(150, 600, 1150, 640, WT)
    d.stroke([(500, 480), (500, 380), (800, 380), (800, 480)], (60, 60, 70, 255), 24)
    if not empty:
        for x, y, r, c in ((420, 300, 170, (200, 200, 210, 255)), (850, 260, 130, (220, 220, 230, 255))): d.dot(x, y, r, c); d.ellipse(x, y, r, r, outline=LINE, width=12); eyes(d, x, y - 10, r / 240, 'happy')
    else: eyes(d, 650, 780, 1.0, 'sad'); d.ellipse(650, 520, 360, 40, fill=(60, 30, 30, 255))
    return d.out()


def dominoes(stage=0):                                       # domino city tiles: CHICAGO first, other skylines behind, falling in a chain
    d = Draw(1600, 1000)
    for k in range(5):
        x = 140 + k * 300; lean = min(1.0, max(0.0, stage - k * 0.5)) if stage else 0.0; a = lean * 1.1
        w, h = 200, 640; cx, by = x + 100, 940
        P = [(-w / 2, 0), (w / 2, 0), (w / 2, -h), (-w / 2, -h)]; P = [(cx + px * math.cos(a) - py * math.sin(a), by + px * math.sin(a) + py * math.cos(a)) for px, py in P]
        d.poly(P, fill=((70, 60, 110, 255), (60, 90, 140, 255), (110, 70, 120, 255), (60, 110, 110, 255), (120, 90, 60, 255))[k], outline=LINE, width=12)
        if lean < 0.3:
            for j in range(4): d.rect(x + 30 + j * 40, by - 200 - (j % 2) * 120, x + 60 + j * 40, by - 40, (255, 220, 120, 255))
            if k == 0: d.text(cx, by - h + 80, 'CHICAGO', 54, WT, stroke=5, stroke_fill=LINE)
    return d.out()


def scale(stage=0):                                          # balance scale: LUCK (dice) vs SKILL (target); stage 1 tips to luck, 2 to skill
    d = Draw(1500, 1200); t = (0, -0.22, 0.22)[stage]; d.rect(720, 300, 780, 1100, GLD); d.rrect(500, 1080, 1000, 1160, 20, fill=GLD, outline=LINE, width=12)
    L, R = (750 - 520 * math.cos(t), 300 - 520 * math.sin(t)), (750 + 520 * math.cos(t), 300 + 520 * math.sin(t)); d.stroke([L, R], GLD, 30); d.stroke([L, R], LINE, 6)
    for (x, y), lab, c in ((L, 'LUCK', (40, 150, 90, 255)), (R, 'SKILL', EB)):
        d.stroke([(x, y), (x - 150, y + 330)], LINE, 8); d.stroke([(x, y), (x + 150, y + 330)], LINE, 8); d.chord(x, y + 330, 200, 70, 0, 180, fill=c, outline=LINE, width=12)
        d.text(x, y + 470, lab, 110, c, stroke=7, stroke_fill=WT)
        if lab == 'LUCK':
            for j, (dx, dy) in enumerate(((-60, 250), (60, 260))): d.rrect(x + dx - 50, y + dy - 50, x + dx + 50, y + dy + 50, 16, fill=WT, outline=LINE, width=10); d.dot(x + dx, y + dy, 12, RED)
        else:
            for r_, c2 in ((90, RED), (60, WT), (30, RED)): d.dot(x, y + 240, r_, c2)
            d.ellipse(x, y + 240, 90, 90, outline=LINE, width=10)
    d.dot(750, 300, 50, GLD); d.ellipse(750, 300, 50, 50, outline=LINE, width=10); return d.out()


def playfield(stage=0):                                      # top view of the playfield: plunger lane, bumpers, CENTER LANE; stage 1 dotted call, 2 ball in the lane + flash
    d = Draw(1000, 1500); d.rrect(40, 40, 960, 1460, 60, fill=(40, 30, 90, 255), outline=LINE, width=18); d.rect(860, 300, 900, 1420, (90, 80, 140, 255))
    for x, y, c in ((300, 420, YEL), (500, 340, PINK), (700, 420, CYAN)): d.dot(x, y, 80, c); d.ellipse(x, y, 80, 80, outline=LINE, width=10)
    for x in (380, 620): d.rect(x - 14, 120, x + 14, 300, CHR)
    d.rrect(440, 110, 560, 290, 20, fill=(255, 240, 120, 255) if stage == 2 else (90, 80, 150, 255), outline=LINE, width=10)
    for sg in (-1, 1): d.poly([(500 + sg * 60, 1240), (500 + sg * 300, 1140), (500 + sg * 290, 1110)], fill=WT, outline=LINE, width=10)
    if stage == 0: d.dot(880, 1340, 40, CHR); d.ellipse(880, 1340, 40, 40, outline=LINE, width=8)
    if stage == 1:
        for k in range(14): t = k / 13; d.dot(880 - 380 * t, 1300 - 1080 * t + 300 * math.sin(math.pi * t), 16, (255, 240, 120, 255))
        d.poly([(500, 300), (450, 380), (550, 380)], fill=(255, 240, 120, 255), outline=LINE, width=6)
    if stage == 2:
        for k in range(12): a = k * math.pi / 6; d.stroke([(500 + 90 * math.cos(a), 200 + 90 * math.sin(a)), (500 + 220 * math.cos(a), 200 + 220 * math.sin(a))], (255, 250, 180, 255), 16)
        d.dot(500, 200, 46, CHR); d.ellipse(500, 200, 46, 46, outline=LINE, width=8)
    return d.out()


def plunger(pulled=False):                                   # macro: chrome plunger knob + spring
    d = Draw(1400, 700); off = 220 if pulled else 0; d.rect(100, 300, 1300, 400, (60, 50, 110, 255))
    for k in range(9): x = 400 + k * (40 + off / 9); d.stroke([(x, 270), (x + 20, 430)], CHR, 14)
    d.rect(300 + off, 320, 1000, 380, CHR); d.rrect(60 + off, 220, 320 + off, 480, 80, fill=(240, 60, 60, 255), outline=LINE, width=14); d.dot(140 + off, 300, 30, WT)
    d.dot(1180, 350, 70, CHR); d.ellipse(1180, 350, 70, 70, outline=LINE, width=10); return d.out()


def gavel():                                                 # council gavel on its block
    d = Draw(1000, 800); d.rrect(250, 600, 750, 720, 30, fill=(150, 90, 50, 255), outline=LINE, width=12)
    d.stroke([(700, 100), (420, 520)], (150, 90, 50, 255), 40); d.stroke([(700, 100), (420, 520)], LINE, 8); d.rrect(260, 380, 560, 560, 40, fill=(130, 76, 40, 255), outline=LINE, width=14)
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def playworld(path):                                         # inside a giant pinball world: violet field, glowing bumpers, chrome rails, lane lights
    im = sky((40, 20, 90), (110, 60, 190), 1.0); d = Draw(W2, H2)
    for k, (x, y, c) in enumerate(((300, 300, YEL), (800, 220, PINK), (1300, 320, CYAN), (1800, 240, ORG), (2200, 340, (120, 255, 140, 255)))): d.dot(x, y, 130, c); d.ellipse(x, y, 130, 130, outline=LINE, width=14); d.dot(x - 40, y - 40, 30, WT)
    for x in range(100, W2, 200): d.dot(x, 620, 20, (255, 240, 150, 255))
    d.stroke([(0, 760), (W2, 700)], CHR, 30); d.stroke([(0, 760), (W2, 700)], LINE, 6); fl(d, (70, 40, 130, 255)); im.alpha_composite(d.out())
    for x, c in ((300, (255, 220, 60, 90)), (1300, (80, 230, 255, 90)), (2200, (120, 255, 140, 90))): glow(im, x, 300, 300, c, 80)
    im.convert('RGB').save(path)


def radio(path):                                             # 1942 radio stage: olive curtains, cream arch, red stripes, ON AIR-style lamp (no text)
    im = sky((120, 120, 60), (230, 220, 170), 1.0); d = Draw(W2, H2); d.chord(1200, 900, 800, 700, 180, 360, fill=(250, 240, 210, 255), outline=LINE, width=14)
    for x in (0, 2000): [d.rect(x + j * 80, 0, x + j * 80 + 60, 940, (110, 120, 50, 255)) for j in range(5)]
    for k in range(5): d.rect(400 + k * 340, 300, 520 + k * 340, 330, (220, 50, 60, 255))
    d.dot(1200, 260, 60, (255, 80, 80, 255)); fl(d, (120, 90, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 260, 200, (255, 120, 100, 100), 60); im.convert('RGB').save(path)


def bowling(path):                                           # 1940s bowling alley: amber lanes to the horizon, teal walls, neon rings
    im = sky((30, 110, 120), (80, 170, 170), 1.0); d = Draw(W2, H2)
    for k in range(6): x = 200 + k * 380; d.poly([(x, 940), (x + 260, 940), (1200 + (x - 1200) * 0.3 + 60, 420), (1200 + (x - 1200) * 0.3, 420)], fill=(230, 170, 90, 255), outline=LINE, width=6)
    for x in range(300, W2, 500): d.ellipse(x, 220, 120, 60, outline=(255, 120, 200, 255), width=14)
    fl(d, (180, 120, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def flashnight(path):                                        # flashbulb night: slate blue street, white flash bursts, crowd silhouettes
    im = sky((40, 50, 90), (90, 100, 150), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 140): d.dot(x + 70, 860, 80, (30, 34, 60, 255)); d.rrect(x + 20, 900, x + 120, 1100, 30, fill=(30, 34, 60, 255))
    fl(d, (60, 64, 100, 255), 1000); im.alpha_composite(d.out())
    for x, y in ((400, 300), (1100, 200), (1800, 320), (2200, 180)): glow(im, x, y, 220, (255, 255, 230, 150), 50)
    im.convert('RGB').save(path)


def harbor(path):                                            # night harbor: deep teal water, bridge silhouette, warm windows, moon
    im = sky((20, 40, 70), (40, 100, 120), 1.0); d = Draw(W2, H2); stars(d, 80, 500, 13); d.dot(1900, 200, 90, (250, 240, 200, 255))
    for x in (500, 1300): d.rect(x, 200, x + 70, 760, (30, 40, 60, 255))
    d.stroke([(0, 600), (500, 240), (900, 560), (1300, 240), (1800, 600)], (30, 40, 60, 255), 16)
    for k, x in enumerate(range(1700, W2, 120)): d.rect(x, 760 - 100 - (k % 3) * 80, x + 100, 780, (30, 40, 60, 255)); d.rect(x + 30, 700 - (k % 3) * 80, x + 50, 720 - (k % 3) * 80, YEL)
    d.rect(0, 780, W2, 940, (20, 90, 110, 255)); [d.stroke([(x, 820 + (x % 3) * 30), (x + 140, 820 + (x % 3) * 30)], (120, 200, 210, 200), 6) for x in range(40, W2, 260)]
    fl(d, (30, 70, 90, 255)); im.alpha_composite(d.out()); glow(im, 1900, 200, 260, (255, 240, 200, 90), 60); im.convert('RGB').save(path)


def school(path):                                            # school-bus yellow lunch room: red apple wallpaper, big clock, window
    im = sky((255, 210, 60), (255, 236, 150), 1.0); d = Draw(W2, H2)
    for x in range(60, W2, 220):
        for y in (120, 380): d.dot(x + (y // 380) * 110, y, 34, (230, 60, 60, 255)); d.stroke([(x + (y // 380) * 110, y - 34), (x + (y // 380) * 110 + 10, y - 60)], (90, 150, 60, 255), 8)
    d.dot(1200, 300, 130, WT); d.ellipse(1200, 300, 130, 130, outline=LINE, width=14); d.stroke([(1200, 300), (1200, 210)], LINE, 12); d.stroke([(1200, 300), (1270, 300)], LINE, 12)
    fl(d, (200, 150, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def dusktable(path):                                         # sunset domino table: purple-orange sky, far skyline, long table edge
    im = sky((110, 60, 150), (255, 150, 90), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 110)): h = 120 + (k * 53) % 260; d.rect(x, 760 - h, x + 96, 760, (80, 50, 110, 255))
    fl(d, (120, 70, 60, 255), 760); im.alpha_composite(d.out()); glow(im, 1200, 760, 600, (255, 190, 120, 110), 120); im.convert('RGB').save(path)


def backroom(path):                                          # contraband back room: red lamp, brick, crates, shadows
    im = sky((50, 20, 30), (110, 40, 50), 1.0); d = Draw(W2, H2)
    for y in range(0, 940, 70):
        for x in range(-((y // 70) % 2) * 80, W2, 160): d.rrect(x + 4, y + 4, x + 152, y + 64, 8, fill=(120, 50, 50, 255))
    for x in (200, 1900): d.rect(x, 560, x + 320, 900, (140, 100, 60, 255)); d.stroke([(x, 560), (x + 320, 900)], (90, 60, 40, 255), 10)
    d.stroke([(1200, 0), (1200, 200)], LINE, 8); d.chord(1200, 240, 120, 60, 180, 360, fill=(240, 50, 50, 255), outline=LINE, width=10)
    fl(d, (60, 30, 34, 255)); im.alpha_composite(d.out()); glow(im, 1200, 260, 500, (255, 60, 60, 120), 100); im.convert('RGB').save(path)


def splitstage(path):                                        # split stage: casino-felt green left with dice, blueprint blue right with grid
    im = sky((30, 130, 80), (30, 130, 80), 1.0); d = Draw(W2, H2); d.rect(1200, 0, W2, H2, (40, 90, 200, 255))
    for x in range(1240, W2, 80): d.stroke([(x, 0), (x, 940)], (120, 170, 255, 160), 4)
    for y in range(40, 940, 80): d.stroke([(1200, y), (W2, y)], (120, 170, 255, 160), 4)
    for x, y in ((200, 200), (600, 500), (900, 220)): d.rrect(x - 60, y - 60, x + 60, y + 60, 16, fill=(255, 255, 255, 120))
    d.rect(1190, 0, 1210, 940, WT); fl(d, (60, 50, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def chamber(path):                                           # 1976 council chamber: wood panels, harvest gold + avocado + orange stripes, round seal (no text)
    im = sky((150, 100, 60), (200, 140, 80), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 160): d.rect(x, 0, x + 150, 940, (170, 110, 60, 255))
    for k, c in enumerate((GLD, AVO, ORG)): d.rect(0, 560 + k * 40, W2, 590 + k * 40, c)
    d.dot(1200, 300, 190, (240, 200, 90, 255)); d.ellipse(1200, 300, 190, 190, outline=LINE, width=14); d.dot(1200, 300, 120, (60, 110, 160, 255))
    fl(d, (110, 70, 40, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def chrome(path):                                            # chrome macro studio: steel gradient, blue light bars, sparkle bokeh
    im = sky((30, 40, 70), (120, 140, 180), 1.0); d = Draw(W2, H2); r = np.random.RandomState(7)
    for x in range(150, W2, 450): d.rrect(x, 80, x + 60, 860, 30, fill=(120, 180, 255, 120))
    for _ in range(30): d.dot(r.randint(0, W2), r.randint(0, 800), r.randint(20, 60), (220, 235, 255, 70))
    fl(d, (50, 60, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast2(('fiorello', 'cop40', 'lunchkid', 'sharpe', 'cncl1', 'cncl2', 'cncl3'))
    multi = dict(pmach={'default': machine(), 'shocked': machine('shocked'), 'tape': machine('shocked', tape=True), 'happy': machine('default'), 'cage': machine('sad', cage=True), 'sad': machine('sad')},
                 pball={'default': ball(), 'q': ball(True)}, qman={'default': qman()}, podium={'default': podium()}, pins={'default': pins()}, pile={'default': pile()},
                 smash={'default': smash()}, newscam={'default': newscam()}, barge={'default': barge()}, coins={'default': coins(), 'empty': coins(True)},
                 domino={'default': dominoes(0), 'f1': dominoes(1.2), 'f2': dominoes(3.2)}, scale={'default': scale(0), 'luck': scale(1), 'skill': scale(2)},
                 pfield={'default': playfield(0), 'call': playfield(1), 'hit': playfield(2)}, plunger={'default': plunger(), 'pulled': plunger(True)}, gavel={'default': gavel()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    NV, BR_ = (40, 60, 140, 255), (150, 90, 50, 255)
    cards = dict(hookc=M.bigneon('BANNED FOR', '34 YEARS!', 920, YEL, (90, 160, 255, 255)),
                 oneman=stamp('ONE MAN. ONE BALL.', 960, NV, 120, -3),
                 y1942=M.cal('IN', '1942', (110, 120, 50, 255)),
                 mayorc=P_('MAYOR', 'LA GUARDIA', (200, 50, 60, 255), 920, 150, 160, YEL),
                 gamb=stamp('GAMBLING!', 800, RED, 160, -4),
                 raid=stamp('POLICE RAID!', 860, NV, 140, 3),
                 thous=stamp('THOUSANDS SEIZED!', 960, RED, 110, -3),
                 cams=P_('FOR THE', 'CAMERAS!', (60, 64, 110, 255), 860, 130, 180, YEL),
                 reason=stamp('HIS REASON?', 820, (110, 120, 50, 255), 140, 3),
                 lunch=M.bigneon('THEIR LUNCH', 'MONEY!', 920, YEL, PINK),
                 decades=P_('THREE', 'DECADES', (80, 50, 110, 255), 860, 170, 160, YEL),
                 contra=stamp('CONTRABAND!', 880, (200, 40, 50, 255), 150, -4),
                 question=P_('ONE', 'QUESTION', (40, 90, 200, 255), 820, 170, 170, YEL),
                 game=stamp('A GAME!', 700, (40, 90, 200, 255), 160, 3),
                 y1976=M.cal('IN', '1976', ORG),
                 expert=P_('PINBALL', 'EXPERT', BR_, 900, 160, 170, YEL),
                 sharpec=P_('ROGER', 'SHARPE', ORG, 860, 160, 180, WT),
                 councilc=P_('CITY', 'COUNCIL', AVO, 820, 170, 170, WT),
                 backup=stamp('BACKUP MACHINE!', 900, (110, 70, 40, 255), 120, -3),
                 exactly=M.bigneon('EXACTLY', 'THERE!', 860, YEL, (90, 160, 255, 255)),
                 unan=stamp('UNANIMOUS!', 860, (60, 140, 80, 255), 140, 3),
                 lifted=M.bigneon('BAN', 'LIFTED!', 760, YEL, (120, 255, 140, 255)),
                 future=stamp("PINBALL'S ENTIRE FUTURE", 1000, NV, 100, -3),
                 single=P_('ON A', 'SINGLE BALL', EB, 900, 150, 170, YEL))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    CE.tiles(T('field.jpg'), (80, 50, 150), (66, 40, 130)); B.tex_wood(T('wood.jpg')); CE.tiles(T('lanes.jpg'), (230, 180, 110), (214, 164, 96)); CE.tiles(T('cobble.jpg'), (80, 84, 110), (66, 70, 96))
    CE.tiles(T('dock.jpg'), (110, 80, 60), (96, 68, 50)); CE.tiles(T('lino2.jpg'), (240, 230, 200), (200, 60, 60)); M.sandtex(T('tabletop.jpg'), (150, 90, 70), (134, 78, 60))
    CE.tiles(T('brick2.jpg'), (90, 40, 40), (76, 32, 32)); CE.tiles(T('felt.jpg'), (40, 140, 90), (40, 90, 200)); CE.tiles(T('shag.jpg'), (200, 140, 60), (150, 160, 70)); M.sandtex(T('steel2.jpg'), (90, 100, 130), (76, 86, 116))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(playworld=playworld, radio=radio, bowling=bowling, flashnight=flashnight, harbor=harbor, school=school, dusktable=dusktable, backroom=backroom, splitstage=splitstage, chamber=chamber, chrome=chrome)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
