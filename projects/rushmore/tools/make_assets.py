#!/usr/bin/env python3
"""Assets for video 31: Mount Rushmore's name was a joke - New York lawyer Charles Rushmore asked his guide what a Black Hills peak was called
(1885), "it never had a name, we'll call it Rushmore"; Doane Robinson wanted tourists, the sculptor went bigger (four presidents, 400+ workers,
14 years, just under $1 million, 60-ft faces, nobody died), work stopped at the heads in 1941, and the lawyer gave $5,000. Black Hills granite
world (new palette): rose-gold dawn mountain (hook + loop; a "?" speech bubble = open loop, resolved as WHAT'S IT CALLED?), lavender gaslit New
York brownstones, mint-pine Black Hills claims, violet-teal granite peak, cherry-cream 1920s historian office, butter sketch studio, cyan sky
worksite with scaffolds, apricot-indigo 1941 dusk. Cute cast (new): Charles Rushmore (grey homburg, pinstripes, mustache), the guide (feather
slouch hat, green buckskin, beard), Doane Robinson (tweed, bow tie, round glasses), the sculptor (beret, dusty smock), two drillers (hard
hats with lamps). The sculptor's death is a resting beret and chisel by a candle. usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v29_assets import *

ROOT = B.ROOT
GRAN, VIO, ROSE, PINE, GOLD, CRM, NAVY, MINT = (196, 190, 200, 255), (138, 92, 255, 255), (255, 170, 150, 255), (50, 120, 90, 255), (250, 200, 70, 255), (252, 246, 232, 255), (40, 50, 110, 255), (150, 230, 200, 255)
LA.NEW.update({
    'rush': dict(sk=0, style='slick', hair=(60, 50, 50, 255), suit=(80, 86, 110, 255), shade=(62, 66, 88, 255), body='lawyer', acc=(150, 60, 200, 255), xhat='homburg', hatc=(150, 150, 166, 255), stache=(60, 50, 50, 255)),
    'guide': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=(110, 150, 90, 255), shade=(88, 124, 70, 255), body='fringe', acc=(240, 180, 60, 255), xhat='feather', hatc=(150, 110, 80, 255), plume=(80, 160, 230, 255), beard=(40, 30, 30, 255)),
    'doane': dict(sk=0, style='bald', hair=(230, 230, 236, 255), suit=(170, 120, 90, 255), shade=(146, 100, 72, 255), body='tweed', acc=(60, 130, 200, 255), glasses=1, stache=(236, 236, 240, 255)),
    'sculptor': dict(sk=0, style='side', hair=(200, 200, 206, 255), suit=(236, 226, 206, 255), shade=(210, 198, 176, 255), body='dusty', acc=(220, 70, 90, 255), xhat='beret', hatc=(60, 50, 120, 255), stache=(200, 200, 206, 255)),
    'drill1': dict(sk=1, style='spiky', hair=(50, 40, 30, 255), suit=(90, 140, 220, 255), shade=(70, 114, 190, 255), body='driller', xhat='hardhat', hatc=(255, 210, 50, 255)),
    'drill2': dict(sk=0, style='curly', hair=(220, 120, 60, 255), suit=(230, 120, 100, 255), shade=(200, 96, 80, 255), body='driller', xhat='hardhat', hatc=(255, 150, 50, 255), freckles=1),
})


def gloss(d, x, y, w, h): d.ellipse(x, y, w, h, fill=(255, 255, 255, 120))


def neon3(a, b, c, w=900, h=560):
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 44, fill=(50, 30, 90, 255), outline=LINE, width=16); d.rrect(34, 34, w - 34, h - 34, 30, outline=VIO, width=8)
    d.text(w / 2, h * 0.2, a, LA.fit(a, 96, w - 160), MINT, stroke=6, stroke_fill=LINE)
    for k, (t, col) in enumerate(((b, YEL), (c, ROSE))): d.text(w / 2, h * (0.47 + 0.27 * k), t, LA.fit(t, 140, w - 110), col, stroke=7, stroke_fill=LINE)
    return d.out()


def stoneface(d, x, y, r, kind, face='happy'):              # one cute carved granite head (beard / glasses / wig / plain)
    d.dot(x, y, r, (214, 208, 216, 255)); d.ellipse(x, y, r, r, outline=LINE, width=10); d.chord(x - r * 0.3, y - r * 0.3, r * 0.5, r * 0.4, 200, 340, fill=(232, 228, 236, 255))
    if kind == 'wig': [d.dot(x + sg * r * 0.95, y - r * 0.2 + k * r * 0.3, r * 0.22, (200, 194, 204, 255)) for sg in (-1, 1) for k in range(3)]
    if kind == 'beard': d.chord(x, y + r * 0.35, r * 0.85, r * 0.62, 0, 180, fill=(180, 174, 186, 255))
    if kind == 'specs': [d.ellipse(x + sg * r * 0.33, y - r * 0.05, r * 0.26, r * 0.22, outline=LINE, width=8) for sg in (-1, 1)]; d.chord(x, y + r * 0.3, r * 0.5, r * 0.2, 0, 180, fill=(180, 174, 186, 255))
    eyes(d, x, y - r * 0.05, r / 230, face)


def rushmore(mode='default'):                                # the mountain: pine-dotted granite with 4 cute carved heads (plan: dotted bodies to the waist)
    d = Draw(2000, 1300); d.poly([(0, 1300), (120, 700), (360, 380), (700, 220), (1100, 180), (1500, 260), (1800, 520), (2000, 900), (2000, 1300)], fill=GRAN, outline=LINE, width=16)
    for k, (x, kind) in enumerate(((560, 'wig'), (880, 'plain'), (1150, 'specs'), (1450, 'beard'))): stoneface(d, x, 560 + (k % 2) * 40, 160, kind, 'shocked' if mode == 'gasp' else 'happy')
    for x in range(60, 2000, 90): y = 1150 + (x * 37) % 120; d.poly([(x, y), (x + 40, y - 120), (x + 80, y)], fill=PINE)
    if mode == 'plan':
        for x in (560, 880, 1150, 1450): d.rrect(x - 190, 760, x + 190, 1180, 80, outline=VIO, width=14); [d.dot(x + sg * 230, 900, 50, (180, 150, 255, 160)) for sg in (-1, 1)]
    gloss(d, 900, 260, 160, 40); return d.out()


def bubble(mode='default'):                                  # speech bubble (default: big "?" - open loop; ask: WHAT'S IT CALLED?)
    d = Draw(1200, 900); d.rrect(60, 60, 1140, 640, 120, fill=WT, outline=LINE, width=16); d.poly([(300, 620), (380, 860), (520, 630)], fill=WT, outline=LINE, width=14); d.rect(320, 600, 520, 640, WT)
    if mode == 'ask': d.text(600, 260, "WHAT'S IT", 140, VIO, stroke=6, stroke_fill=LINE); d.text(600, 440, 'CALLED?', 160, (230, 80, 110, 255), stroke=6, stroke_fill=LINE)
    else: d.text(600, 350, '?', 420, VIO, stroke=12, stroke_fill=LINE)
    return d.out()


def peak(mode='default'):                                    # the unnamed granite peak with a shy face (named: RUSHMORE flag planted)
    d = Draw(1400, 1300); d.poly([(60, 1280), (420, 420), (640, 140), (860, 380), (1340, 1280)], fill=(180, 176, 196, 255), outline=LINE, width=16); d.poly([(560, 260), (640, 140), (720, 250), (660, 230)], fill=WT)
    for x in range(80, 1340, 110): d.poly([(x, 1280), (x + 45, 1150), (x + 90, 1280)], fill=PINE)
    eyes(d, 680, 760, 1.2, 'happy' if mode == 'named' else 'shocked'); d.stroke([(900, 520), (900, 160)], (120, 80, 50, 255), 16)
    if mode == 'named': d.poly([(900, 160), (1330, 200), (900, 330)], fill=VIO, outline=LINE, width=10); d.text(1060, 236, 'RUSHMORE', 50, WT)
    else: d.poly([(900, 160), (1200, 200), (900, 330)], fill=WT, outline=LINE, width=10); d.text(1010, 240, '?', 120, VIO)
    gloss(d, 520, 400, 80, 30); return d.out()


def claims():                                                # mining claims: stake signs, pickaxe, pan with gold nuggets
    d = Draw(1600, 1000); d.ellipse(800, 900, 700, 80, fill=(170, 140, 100, 255))
    for x in (260, 1340): d.rect(x - 16, 300, x + 16, 900, (140, 100, 60, 255)); d.rrect(x - 160, 220, x + 160, 420, 16, fill=CRM, outline=LINE, width=10); d.text(x, 320, 'CLAIM', 80, (180, 60, 60, 255))
    d.ellipse(800, 720, 300, 120, fill=(150, 150, 166, 255), outline=LINE, width=12); [d.dot(700 + k * 60, 690 + (k % 2) * 30, 34, GOLD) for k in range(4)]; eyes(d, 800, 760, 0.6, 'happy')
    d.stroke([(1000, 560), (1200, 860)], (140, 100, 60, 255), 22); d.chord(1000, 560, 140, 60, 180, 360, fill=(170, 170, 186, 255), outline=LINE, width=10); return d.out()


def sdmap():                                                 # South Dakota map card: state shape, Black Hills pin, glowing route
    d = Draw(1600, 1100); d.rrect(40, 40, 1560, 1060, 40, fill=(240, 230, 200, 255), outline=LINE, width=16)
    d.poly([(160, 220), (1440, 220), (1460, 300), (1420, 880), (1200, 860), (1140, 900), (160, 900)], fill=(170, 220, 170, 255), outline=LINE, width=12)
    d.stroke([(1300, 300), (900, 450), (600, 560), (330, 720)], (250, 120, 90, 255), 16); [d.dot(260 + k * 40, 740 + (k % 2) * 20, 40, (60, 90, 70, 255)) for k in range(5)]
    d.dot(330, 640, 60, VIO); d.poly([(290, 660), (370, 660), (330, 760)], fill=VIO); d.dot(330, 640, 24, WT); d.text(1000, 980, 'SOUTH DAKOTA', 80, NAVY); return d.out()


def tourists():                                              # row of tiny tourists with cameras, sun hats, ice creams
    d = Draw(2000, 800); cols = [(255, 150, 160, 255), (120, 200, 240, 255), (250, 210, 90, 255), (160, 130, 230, 255), (120, 210, 150, 255)]
    for k in range(9):
        x = 120 + k * 220; y = 360 + (k % 2) * 40
        d.rrect(x - 70, y + 70, x + 70, y + 320, 50, fill=cols[k % 5], outline=LINE, width=8); d.dot(x, y, 76, (255, 222, 196, 255) if k % 3 else (196, 136, 96, 255)); d.ellipse(x, y, 76, 76, outline=LINE, width=8)
        d.ellipse(x, y - 60, 110, 26, fill=cols[(k + 2) % 5], outline=LINE, width=6); eyes(d, x, y + 10, 0.34, 'happy'); d.rrect(x - 50, y + 110, x + 50, y + 180, 12, fill=(60, 60, 70, 255), outline=LINE, width=6); d.dot(x, y + 145, 22, (150, 210, 255, 255))
    return d.out()


def legends():                                               # three cute legend busts with name tags: Red Cloud, Lewis and Clark, Buffalo Bill
    d = Draw(2000, 1000)
    for k, (x, nm, hatc) in enumerate(((360, 'RED CLOUD', None), (1000, 'LEWIS & CLARK', (120, 90, 60, 255)), (1640, 'BUFFALO BILL', (200, 160, 110, 255)))):
        d.rrect(x - 200, 560, x + 200, 800, 60, fill=(200, 194, 206, 255), outline=LINE, width=10); d.dot(x, 420, 170, (214, 208, 216, 255)); d.ellipse(x, 420, 170, 170, outline=LINE, width=10); eyes(d, x, 430, 0.6, 'happy')
        if hatc is None: d.chord(x, 330, 175, 120, 180, 360, fill=(60, 50, 50, 255)); d.poly([(x + 120, 300), (x + 160, 100), (x + 200, 300)], fill=(250, 240, 220, 255), outline=LINE, width=6)
        else: d.ellipse(x, 280, 250, 50, fill=hatc, outline=LINE, width=8); d.chord(x, 280, 150, 120, 180, 360, fill=hatc, outline=LINE, width=8)
        if k == 2: d.poly([(x - 30, 560), (x + 30, 560), (x, 640)], fill=(240, 236, 230, 255))
        d.rrect(x - 260, 840, x + 260, 960, 20, fill=GOLD, outline=LINE, width=8); d.text(x, 900, nm, LA.fit(nm, 70, 480), NAVY)
    return d.out()


def blueprint():                                             # the sculptor's bigger plan: four heads carved to the waist on blue paper
    d = Draw(1800, 1100); d.rrect(40, 40, 1760, 1060, 30, fill=(60, 110, 200, 255), outline=LINE, width=16); [d.stroke([(60, y), (1740, y)], (100, 150, 230, 255), 4) for y in range(100, 1060, 80)]
    for x in (360, 720, 1080, 1440): d.ellipse(x, 340, 130, 150, outline=WT, width=10); d.rrect(x - 190, 500, x + 190, 940, 90, outline=WT, width=10); [d.dot(x + sg * 60, 330, 16, WT) for sg in (-1, 1)]
    d.stroke([(100, 960), (1700, 960)], YEL, 10); d.text(900, 1010, 'TO THE WAIST', 60, YEL); eyes(d, 1640, 160, 0.5, 'happy'); return d.out()


def crew():                                                  # 400+ workers: tiny hard-hat drillers dangling on ropes along the cliff
    d = Draw(2000, 1100); d.rect(0, 0, 2000, 120, (150, 146, 160, 255))
    for k in range(12):
        x = 100 + k * 165; y = 300 + (k % 3) * 220; d.stroke([(x, 0), (x, y - 70)], (120, 90, 60, 255), 6)
        d.rrect(x - 50, y + 40, x + 50, y + 180, 36, fill=[(90, 140, 220, 255), (230, 120, 100, 255), (120, 200, 150, 255)][k % 3], outline=LINE, width=6); d.dot(x, y, 54, (255, 222, 196, 255) if k % 2 else (196, 136, 96, 255)); d.ellipse(x, y, 54, 54, outline=LINE, width=6)
        d.chord(x, y - 10, 60, 50, 180, 360, fill=YEL); eyes(d, x, y + 10, 0.25, 'happy'); d.rect(x - 70, y + 170, x + 70, y + 190, (140, 100, 60, 255))
    return d.out()


def scale():                                                 # faces 60 feet tall: one giant stone eye + nose, a tiny worker for scale
    d = Draw(1400, 1300); d.rrect(60, 60, 1340, 1260, 80, fill=(214, 208, 216, 255), outline=LINE, width=16); d.ellipse(480, 420, 230, 170, fill=WT, outline=LINE, width=14); d.dot(500, 440, 90, LINE); d.dot(530, 400, 34, WT)
    d.poly([(860, 300), (1000, 900), (760, 920)], fill=(196, 190, 200, 255), outline=LINE, width=12); d.stroke([(1180, 120), (1180, 760)], (120, 90, 60, 255), 6)
    d.rrect(1140, 840, 1220, 960, 30, fill=(90, 140, 220, 255), outline=LINE, width=6); d.dot(1180, 790, 44, (255, 222, 196, 255)); d.ellipse(1180, 790, 44, 44, outline=LINE, width=6); d.chord(1180, 780, 48, 40, 180, 360, fill=YEL)
    d.stroke([(1290, 140), (1290, 1180)], VIO, 12); d.text(1290, 640, '60', 90, VIO, stroke=5, stroke_fill=LINE); return d.out()


def safety():                                                # nobody died: happy safety board with a big green check and a smiling hard hat
    d = Draw(1300, 1100); d.rrect(80, 80, 1220, 860, 40, fill=(120, 210, 150, 255), outline=LINE, width=16); d.text(650, 220, 'NOBODY HURT', 110, WT, stroke=6, stroke_fill=LINE)
    d.stroke([(430, 520), (580, 680), (880, 360)], WT, 60); d.rect(300, 860, 360, 1080, (120, 90, 60, 255)); d.rect(940, 860, 1000, 1080, (120, 90, 60, 255))
    d.chord(1100, 900, 140, 110, 180, 360, fill=YEL, outline=LINE, width=10); eyes(d, 1100, 860, 0.4, 'happy'); return d.out()


def rest():                                                  # 1941: the sculptor's beret and chisel resting on a stool by a candle (gentle)
    d = Draw(1300, 1100); d.rrect(300, 560, 1000, 640, 20, fill=(150, 100, 60, 255), outline=LINE, width=10); [d.rect(x, 640, x + 40, 1060, (120, 80, 50, 255)) for x in (360, 900)]
    d.ellipse(560, 520, 210, 60, fill=(60, 50, 120, 255), outline=LINE, width=10); d.rect(550, 440, 570, 470, LINE); d.stroke([(700, 540), (930, 470)], (170, 170, 186, 255), 22)
    d.rect(1080, 420, 1160, 900, CRM); d.rrect(1080, 420, 1160, 900, 6, outline=LINE, width=6); d.poly([(1120, 300), (1090, 400), (1150, 400)], fill=(255, 190, 60, 255)); d.dot(1120, 380, 24, YEL)
    return d.out()


def emptybag():                                              # the money ran thin: a flat money bag with a moth and a sad face
    d = Draw(1100, 1000); d.chord(550, 860, 400, 260, 180, 360, fill=(200, 170, 120, 255), outline=LINE, width=14); d.poly([(470, 600), (630, 600), (600, 660), (500, 660)], fill=(170, 140, 90, 255), outline=LINE, width=8)
    d.text(550, 800, '$', 140, (120, 150, 110, 255)); eyes(d, 550, 720, 0.6, 'sad')
    for sg in (-1, 1): d.ellipse(820 + sg * 50, 360, 50, 30, fill=(230, 220, 240, 255), outline=LINE, width=6)
    d.dot(820, 360, 16, LINE); return d.out()


def check():                                                 # the lawyer's $5,000 gift check
    d = Draw(1800, 900); d.rrect(60, 100, 1740, 840, 30, fill=(230, 220, 255, 255), outline=LINE, width=16); [d.stroke([(100, y), (1700, y)], (210, 200, 240, 255), 6) for y in range(160, 820, 60)]
    d.text(560, 230, 'FOR: THE CARVING', 80, NAVY); d.rrect(980, 300, 1680, 470, 20, fill=WT, outline=LINE, width=10); d.text(1330, 385, '$5,000', 130, (40, 120, 70, 255))
    d.stroke([(1050, 700), (1650, 700)], LINE, 6); d.text(1350, 650, 'C. Rushmore', 80, (60, 40, 150, 255)); eyes(d, 450, 560, 0.8, 'happy'); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def dawn(path):                                              # rose-gold dawn over the Black Hills: layered pine ridges, sun glow
    im = sky((255, 150, 140), (255, 220, 170), 1.0); d = Draw(W2, H2); d.dot(1900, 520, 160, (255, 246, 210, 255))
    hills(d, 640, (200, 140, 160, 255), 90, 3); hills(d, 740, (120, 120, 140, 255), 70, 4, 1.2)
    for x in range(0, W2, 70): y = 820 + (x * 53) % 60; d.poly([(x, y + 120), (x + 35, y - 60), (x + 70, y + 120)], fill=(50, 100, 80, 255))
    fl(d, (110, 120, 100, 255)); im.alpha_composite(d.out()); glow(im, 1900, 520, 500, (255, 230, 180, 120), 100); im.convert('RGB').save(path)


def brownstone(path):                                        # lavender gaslit 1885 New York brownstones, stoops, lamps
    im = sky((150, 120, 200), (230, 190, 220), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 400)): d.rect(x + 10, 200, x + 390, 940, (170, 100, 80, 255)); [win(d, x + 60 + i * 150, 280 + j * 200, x + 140 + i * 150, 400 + j * 200, (255, 220, 150, 255)) for i in range(2) for j in range(2)]; d.rect(x + 120, 760, x + 280, 940, (130, 80, 60, 255))
    for x in range(200, W2, 400): d.rect(x - 8, 560, x + 8, 940, LINE); d.rrect(x - 30, 500, x + 30, 570, 10, fill=(255, 220, 140, 255), outline=LINE, width=6)
    fl(d, (120, 100, 120, 255)); im.alpha_composite(d.out()); [glow(im, x, 535, 110, (255, 210, 130, 130), 40) for x in range(200, W2, 400)]; im.convert('RGB').save(path)


def pines(path):                                             # mint-pine Black Hills morning: granite spires, pines, creek
    im = sky((150, 220, 210), (240, 250, 235), 1.0); d = Draw(W2, H2)
    for x, h_ in ((300, 380), (700, 460), (1700, 420), (2100, 360)): d.poly([(x - 120, 900), (x - 40, 900 - h_), (x + 30, 900 - h_ + 40), (x + 120, 900)], fill=(190, 186, 200, 255), outline=LINE, width=8)
    for x in range(0, W2, 90): y = 760 + (x * 31) % 80; d.poly([(x, y + 180), (x + 45, y - 40), (x + 90, y + 180)], fill=(60, 140, 100, 255))
    d.rect(0, 900, W2, 940, (120, 190, 230, 255)); fl(d, (120, 150, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 700, (255, 255, 240, 80), 140); im.convert('RGB').save(path)


def granite(path):                                           # violet-teal granite cliffs at golden hour
    im = sky((90, 70, 170), (90, 200, 200), 1.0); d = Draw(W2, H2)
    for k in range(6): x = k * 450; d.poly([(x - 100, 940), (x + 60, 300 + (k % 2) * 120), (x + 200, 260 + (k % 3) * 60), (x + 400, 940)], fill=(150 + k * 6, 140 + k * 6, 180, 255), outline=LINE, width=8)
    fl(d, (110, 110, 130, 255)); im.alpha_composite(d.out()); glow(im, 600, 200, 400, (255, 220, 180, 110), 90); im.convert('RGB').save(path)


def office(path):                                            # cherry-cream 1920s historian office: wallpaper stripes, map frame, radio
    im = sky((200, 80, 90), (250, 220, 200), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 60, 940, (240, 200, 190, 120))
    d.rrect(800, 160, 1600, 560, 20, fill=(200, 230, 200, 255), outline=(170, 120, 60, 255), width=24); d.poly([(900, 260), (1500, 260), (1480, 480), (920, 480)], fill=(150, 210, 150, 255))
    d.rrect(1900, 600, 2200, 900, 30, fill=(150, 90, 60, 255), outline=LINE, width=8); d.dot(2050, 720, 70, (240, 200, 140, 255))
    fl(d, (150, 90, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def studio(path):                                            # butter sketch studio: skylights, plaster busts, easels
    im = sky((255, 230, 140), (255, 246, 210), 1.0); d = Draw(W2, H2)
    for x in (400, 1200, 2000): d.poly([(x - 250, 80), (x + 250, 80), (x + 200, 300), (x - 200, 300)], fill=(190, 230, 250, 255), outline=(200, 170, 100, 255), width=14)
    for x in (300, 2100): d.rect(x - 60, 700, x + 60, 940, (220, 210, 200, 255)); d.dot(x, 620, 90, (236, 232, 228, 255))
    fl(d, (190, 160, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def worksite(path):                                          # cyan-sky worksite: cliff face, wooden scaffolds, ladders, compressor shed
    im = sky((80, 190, 240), (210, 240, 255), 1.0); d = Draw(W2, H2); d.poly([(0, 940), (100, 200), (2300, 160), (2400, 940)], fill=(190, 184, 196, 255), outline=LINE, width=10)
    for y in (380, 600): d.rect(200, y, 2200, y + 24, (170, 120, 70, 255))
    for x in range(260, 2200, 320): d.rect(x, 200, x + 16, 940, (150, 100, 60, 255))
    fl(d, (160, 150, 140, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def dusk(path):                                              # apricot-indigo 1941 dusk: quiet mountain silhouette, first stars
    im = sky((70, 60, 140), (255, 180, 130), 1.0); d = Draw(W2, H2); stars(d, 50, 300, 7)
    hills(d, 700, (110, 90, 140, 255), 120, 2); hills(d, 820, (70, 70, 110, 255), 60, 4, 0.5)
    fl(d, (120, 100, 120, 255)); im.alpha_composite(d.out()); glow(im, 1200, 760, 700, (255, 190, 140, 110), 140); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast4(('rush', 'guide', 'doane', 'sculptor', 'drill1', 'drill2'))
    multi = dict(rushmore={k: rushmore(k) for k in ('default', 'gasp', 'plan')}, bubble={'default': bubble(), 'ask': bubble('ask')}, peak={'default': peak(), 'named': peak('named')},
                 claims={'default': claims()}, sdmap={'default': sdmap()}, tourists={'default': tourists()}, legends={'default': legends()}, blueprint={'default': blueprint()},
                 crew={'default': crew()}, scale={'default': scale()}, safety={'default': safety()}, rest={'default': rest()}, emptybag={'default': emptybag()}, check={'default': check()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ, RB = (100, 60, 180, 255), (30, 130, 130, 255), (180, 60, 80, 255)
    cards = dict(hookc=neon3("MOUNT RUSHMORE'S", 'NAME WAS', 'A JOKE!'),
                 nylaw=P_('A NEW YORK', 'LAWYER', PU, 820, 130, 170, YEL),
                 y1885=M.cal('DAKOTA', '1885', TQ),
                 charles=P_('CHARLES', 'RUSHMORE', (80, 86, 110, 255), 860, 130, 180, YEL),
                 noname=stamp('IT NEVER HAD A NAME!', 1000, RB, 100, -3),
                 callit=M.bigneon("WE'LL CALL IT", 'RUSHMORE', 900, YEL, VIO),
                 stuck=stamp('AND IT STUCK!', 760, TQ, 140, 4),
                 doanec=P_('DOANE', 'ROBINSON', (170, 100, 70, 255), 800, 130, 180, YEL),
                 want=stamp('WANTS TOURISTS!', 820, (230, 90, 120, 255), 130, 3),
                 bigger=M.bigneon('WENT', 'BIGGER!', 720, YEL, VIO),
                 four=P_('FOUR', 'PRESIDENTS', PU, 800, 140, 170, YEL),
                 workers=M.bigneon('400+', 'WORKERS', 680, YEL, MINT),
                 y14=M.cal('YEARS', '14', (60, 110, 200, 255)),
                 sixty=M.bigneon('FACES', '60 FEET TALL', 860, YEL, ROSE),
                 nodied=stamp('NOBODY DIED!', 720, (50, 150, 90, 255), 150, -3),
                 y1941=M.cal('STOPPED', '1941', RB),
                 heads=stamp('JUST THE HEADS', 860, PU, 120, 3),
                 gave=M.bigneon('LAWYER GAVE', '$5,000', 860, YEL, MINT),
                 kept=P_('THE NAME', 'STAYED', TQ, 800, 130, 170, YEL))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('granfl.jpg'), (150, 140, 130), (138, 128, 118)); CE.tiles(T('cobble.jpg'), (150, 130, 140), (136, 118, 128)); M.sandtex(T('needles.jpg'), (110, 140, 90), (98, 128, 80)); M.sandtex(T('gravel.jpg'), (150, 146, 160), (138, 134, 148))
    CE.tiles(T('officefl.jpg'), (170, 110, 90), (156, 100, 82)); CE.tiles(T('studiofl.jpg'), (210, 180, 130), (196, 166, 118)); M.sandtex(T('rubble.jpg'), (170, 164, 160), (156, 150, 146)); M.sandtex(T('duskfl.jpg'), (110, 100, 120), (98, 90, 110))
    CE.tiles(T('pave.jpg'), (120, 100, 90), (106, 88, 78)); B.tex_wood(T('wood.jpg'))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(dawn=dawn, brownstone=brownstone, pines=pines, granite=granite, office=office, studio=studio, worksite=worksite, dusk=dusk)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
