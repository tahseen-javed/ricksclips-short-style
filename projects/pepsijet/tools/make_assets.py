#!/usr/bin/env python3
"""Assets for video 28: Chicago 1861 - the Tremont House rose six feet on jackscrews while its guests stayed inside; George Pullman then put
a hotel on wheels. Gaslight Victorian diorama world: amber gaslight street at dusk (hook + loop), rose-wallpaper hotel room, emerald parlour,
sky-blue brick block, amber crawlspace of jackscrews, cream shop, teal swamp + Lake Michigan cross-section, misty green night, terracotta
street-works cross-section, brass-cream glass workshop, Prussian-blue starry railway. Cute cast (new): George Pullman (derby, frock coat,
watch chain), sleepy guest (striped nightcap, nightshirt), U.S. senator (white quiff, cravat), two crew men (bandanas, suspenders).
Cholera is a cartoon germ cloud + a tiny floating figure with a halo only. usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v26_assets import *

ROOT = B.ROOT
BRICK, CORAL, AMB, PRU, CREAM, SW = (196, 96, 70, 255), (255, 90, 95, 255), (255, 176, 60, 255), (30, 50, 100, 255), (250, 240, 220, 255), (70, 120, 90, 255)
LA.NEW.update({
    'pullman': dict(sk=0, style='side', hair=(90, 60, 40, 255), suit=(70, 60, 90, 255), shade=(54, 46, 72, 255), body='frock', acc=(200, 60, 70, 255), xhat='derby', hatc=(50, 44, 50, 255), stache=(90, 60, 40, 255)),
    'guest': dict(sk=1, style='curly', hair=(60, 40, 30, 255), suit=(150, 200, 250, 255), shade=(120, 170, 224, 255), body='nightie', xhat='nightcap', hatc=(90, 130, 220, 255)),
    'senator': dict(sk=0, style='quiff', hair=(246, 244, 240, 255), suit=(40, 40, 60, 255), shade=(28, 28, 44, 255), body='cravat', acc=(250, 250, 245, 255), glasses=1),
    'crew1': dict(sk=2, style='bald', hair=(30, 24, 24, 255), suit=(240, 200, 150, 255), shade=(214, 174, 124, 255), body='braces2', acc=(60, 90, 160, 255), xhat='bandana', hatc=CORAL),
    'crew2': dict(sk=0, style='spiky', hair=(220, 120, 60, 255), suit=(170, 210, 160, 255), shade=(140, 184, 130, 255), body='braces2', acc=(150, 60, 50, 255), xhat='bandana', hatc=(60, 140, 220, 255)),
})


def hotel(mode='default'):                                   # the Tremont House: 6 storeys, cute face over the door, TREMONT HOUSE sign (wave: guests waving)
    d = Draw(1300, 1700); d.rect(130, 260, 1170, 1660, BRICK); d.rect(100, 200, 1200, 270, (150, 70, 60, 255)); d.stroke([(100, 200), (1200, 200)], LINE, 12)
    d.rrect(260, 90, 1040, 210, 20, fill=CREAM, outline=LINE, width=10); d.text(650, 152, 'TREMONT HOUSE', 60, (120, 40, 40, 255))
    for j in range(6):
        for i in range(5):
            x, y = 210 + i * 200, 300 + j * 205; lit = (i + j) % 3 == 0; win(d, x, y, x + 110, y + 150, (255, 220, 140, 255) if lit else (150, 200, 240, 255))
            if mode == 'wave' and (i, j) in ((0, 1), (3, 2), (1, 4), (4, 0), (2, 3)):
                d.dot(x + 55, y + 95, 40, (255, 220, 190, 255)); d.ellipse(x + 55, y + 95, 40, 40, outline=LINE, width=6); d.stroke([(x + 95, y + 110), (x + 130, y + 40)], (255, 220, 190, 255), 18)
                [d.dot(x + 55 + sg * 14, y + 92, 6, LINE) for sg in (-1, 1)]
    d.rrect(560, 1460, 740, 1660, 70, fill=(90, 60, 50, 255), outline=LINE, width=10); eyes(d, 650, 1390, 0.6, 'shocked' if mode == 'wave' else 'happy')
    d.rect(130, 1640, 1170, 1690, (110, 60, 50, 255)); d.rrect(130, 260, 1170, 1690, 2, outline=LINE, width=12)
    return d.out()


def jacks():                                                 # a row of wooden blocks + jackscrews (what the hotel stands on)
    d = Draw(1800, 500)
    for x in range(110, 1800, 200):
        d.rrect(x - 70, 330, x + 70, 480, 10, fill=(160, 110, 70, 255), outline=LINE, width=8); d.rect(x - 26, 60, x + 26, 340, (180, 180, 196, 255)); [d.stroke([(x - 26, y), (x + 26, y + 16)], LINE, 5) for y in range(70, 330, 30)]
        d.rect(x - 60, 40, x + 60, 70, (120, 120, 136, 255)); d.stroke([(x - 120, 180), (x + 120, 180)], (120, 80, 50, 255), 14)
    return d.out()


def steps(steep=False):                                      # the front steps (steep: more, taller steps, a sweating bead)
    d = Draw(1200, 1100); n = 7 if steep else 3; h_ = 900 / n
    for k in range(n): y = 1080 - (k + 1) * h_; d.rect(150 + k * 50, y, 1050 - k * 50, y + h_, (220, 210, 196, 255)); d.stroke([(150 + k * 50, y), (1050 - k * 50, y)], LINE, 10)
    eyes(d, 600, 1000 - (h_ * 0.4), 0.6, 'shocked' if steep else 'happy')
    if steep: d.ellipse(860, 300, 30, 46, fill=(150, 210, 255, 255), outline=LINE, width=6)
    return d.out()


def winframe():                                              # a hotel window frame (creeps up past eye level)
    d = Draw(900, 1100); d.rrect(60, 60, 840, 1040, 20, fill=(120, 60, 50, 255), outline=LINE, width=14); d.rect(130, 130, 770, 900, (150, 210, 250, 255)); d.stroke([(450, 130), (450, 900)], (250, 250, 245, 255), 22)
    d.stroke([(130, 515), (770, 515)], (250, 250, 245, 255), 22); d.rect(40, 920, 860, 1000, (230, 220, 200, 255)); d.ellipse(300, 300, 70, 30, fill=(255, 255, 255, 150)); return d.out()


def bed():                                                   # sleeping guest tucked in bed with Zs
    d = Draw(1500, 1000); d.rrect(100, 200, 260, 900, 40, fill=(140, 90, 60, 255), outline=LINE, width=12); d.rrect(1240, 400, 1400, 900, 40, fill=(140, 90, 60, 255), outline=LINE, width=12)
    d.rrect(200, 560, 1300, 820, 40, fill=(150, 200, 250, 255), outline=LINE, width=14); d.rrect(260, 480, 520, 620, 50, fill=WT, outline=LINE, width=10); d.dot(420, 470, 110, (255, 220, 190, 255)); d.ellipse(420, 470, 110, 110, outline=LINE, width=10)
    for sg in (-1, 1): d.arc(420 + sg * 40, 470, 22, 14, 20, 160, LINE, 8)
    d.chord(420, 440, 116, 100, 180, 360, fill=(90, 130, 220, 255)); [d.text(640 + k * 110, 300 - k * 90, 'Z', 90 + k * 20, (120, 90, 230, 255), stroke=5, stroke_fill=LINE) for k in range(3)]
    return d.out()


def dinner():                                                # dinner table: roast chicken with a happy face, candles, wobbly tea cup
    d = Draw(1400, 1000); d.rrect(100, 560, 1300, 640, 20, fill=(150, 90, 60, 255), outline=LINE, width=12); [d.rect(x, 640, x + 50, 980, (120, 70, 50, 255)) for x in (180, 1170)]
    d.ellipse(700, 540, 300, 60, fill=WT, outline=LINE, width=10); d.ellipse(700, 440, 220, 140, fill=(220, 140, 60, 255), outline=LINE, width=12); eyes(d, 700, 430, 0.6, 'happy')
    for x in (280, 1120): d.rect(x - 20, 300, x + 20, 540, CREAM); d.poly([(x, 230), (x - 20, 290), (x + 20, 290)], fill=AMB)
    return d.out()


def desk():                                                  # check-in desk: register book, service bell, key board
    d = Draw(1500, 1100); d.rrect(100, 500, 1400, 1060, 30, fill=(130, 70, 50, 255), outline=LINE, width=14); d.rrect(60, 440, 1440, 530, 20, fill=(90, 50, 40, 255), outline=LINE, width=10)
    d.rrect(300, 330, 760, 450, 10, fill=CREAM, outline=LINE, width=8); d.stroke([(530, 330), (530, 450)], LINE, 6); d.chord(1050, 440, 110, 90, 180, 360, fill=(240, 200, 80, 255), outline=LINE, width=10); d.dot(1050, 340, 20, LINE)
    d.rrect(400, 40, 1100, 300, 20, fill=(110, 60, 40, 255), outline=LINE, width=10); [d.dot(480 + k * 90, 140 + (k % 2) * 80, 18, (240, 200, 80, 255)) for k in range(8)]
    eyes(d, 750, 780, 0.7, 'happy'); return d.out()


def block():                                                 # half a city block: five brick shops in a row (on screws), awnings
    d = Draw(2000, 900); cols = [BRICK, (200, 130, 80, 255), (170, 80, 80, 255), (210, 150, 100, 255), (180, 100, 70, 255)]; aw = [CORAL, (90, 170, 140, 255), AMB, (120, 120, 200, 255), CORAL]
    for k in range(5):
        x = 40 + k * 384; d.rect(x, 140 + (k % 2) * 60, x + 380, 760, cols[k]); d.rect(x, 140 + (k % 2) * 60, x + 380, 170 + (k % 2) * 60, (120, 60, 50, 255))
        for i in range(2): win(d, x + 60 + i * 160, 240 + (k % 2) * 60, x + 160 + i * 160, 360 + (k % 2) * 60, (255, 220, 140, 255))
        d.poly([(x + 20, 470), (x + 360, 470), (x + 380, 560), (x, 560)], fill=aw[k], outline=LINE, width=8); d.rect(x + 60, 560, x + 320, 760, (150, 210, 240, 255))
        d.rrect(x, 140 + (k % 2) * 60, x + 380, 760, 2, outline=LINE, width=8)
    for x in range(100, 2000, 160): d.rect(x - 14, 760, x + 14, 880, (180, 180, 196, 255)); d.rrect(x - 40, 850, x + 40, 900, 8, fill=(160, 110, 70, 255))
    return d.out()


def crew():                                                  # a long row of tiny crew men, each with a screw bar
    d = Draw(2000, 700); cols = [CORAL, (60, 140, 220, 255), AMB, (90, 170, 140, 255)]
    for k in range(10):
        x = 100 + k * 200; y = 330
        d.rrect(x - 70, y + 60, x + 70, y + 300, 50, fill=(240, 220, 180, 255), outline=LINE, width=8); d.dot(x, y, 70, (255, 220, 190, 255) if k % 3 else (190, 130, 90, 255)); d.ellipse(x, y, 70, 70, outline=LINE, width=8)
        d.chord(x, y - 4, 74, 66, 180, 360, fill=cols[k % 4]); eyes(d, x, y + 14, 0.3, 'happy'); d.stroke([(x - 100, y + 200), (x + 100, y + 170)], (120, 80, 50, 255), 14)
    return d.out()


def screw(turn=False):                                       # one giant jackscrew with a face (turn: one notch - motion arcs)
    d = Draw(900, 1300); d.rrect(150, 1050, 750, 1280, 20, fill=(160, 110, 70, 255), outline=LINE, width=12); d.rect(380, 250, 520, 1060, (190, 190, 206, 255)); d.rrect(380, 250, 520, 1060, 2, outline=LINE, width=8)
    for y in range(280, 1040, 60): d.stroke([(380, y), (520, y + 30)], LINE, 8)
    d.rrect(230, 170, 670, 280, 20, fill=(140, 140, 156, 255), outline=LINE, width=10); d.stroke([(40 if not turn else 120, 330 if not turn else 120), (860 if not turn else 780, 330 if not turn else 540)], (130, 80, 50, 255), 34)
    eyes(d, 450, 660, 0.6, 'shocked' if turn else 'happy')
    if turn: [d.arc(450, 330, 380 + k * 40, 160 + k * 20, 200, 330, WT, 10) for k in range(2)]; d.text(760, 120, '+1', 110, CORAL, stroke=6, stroke_fill=LINE)
    return d.out()


def bell():                                                  # the foreman's signal bell with ring lines
    d = Draw(1000, 1100); d.rect(470, 60, 530, 200, (120, 80, 50, 255)); d.chord(500, 600, 330, 420, 180, 360, fill=(240, 190, 70, 255), outline=LINE, width=14); d.rect(170, 580, 830, 680, (240, 190, 70, 255))
    d.rrect(150, 600, 850, 690, 2, outline=LINE, width=12); d.dot(500, 760, 70, (200, 150, 50, 255)); eyes(d, 500, 420, 0.8, 'happy')
    for sg in (-1, 1): [d.arc(500 + sg * 380, 450, 60 + k * 50, 120 + k * 60, 270 if sg > 0 else 90, 450 if sg > 0 else 270, LINE, 10) for k in range(2)]
    return d.out()


def shop():                                                  # a shop front that stays OPEN, a cute shopkeeper waving
    d = Draw(1300, 1300); d.rect(100, 200, 1200, 1280, (90, 160, 140, 255)); d.rrect(100, 200, 1200, 1280, 2, outline=LINE, width=12); d.poly([(60, 200), (1240, 200), (1200, 380), (100, 380)], fill=CORAL, outline=LINE, width=10)
    [d.rect(140 + k * 160, 200, 220 + k * 160, 380, (255, 255, 255, 170)) for k in range(7)]; d.rect(200, 480, 1100, 1040, (200, 236, 255, 255)); d.rrect(200, 480, 1100, 1040, 2, outline=LINE, width=10)
    d.dot(650, 760, 120, (255, 220, 190, 255)); d.ellipse(650, 760, 120, 120, outline=LINE, width=10); eyes(d, 650, 770, 0.5, 'happy'); d.chord(650, 750, 124, 110, 180, 360, fill=(90, 60, 40, 255))
    d.rrect(780, 560, 1060, 700, 20, fill=WT, outline=LINE, width=8); d.text(920, 630, 'OPEN', 80, (40, 150, 90, 255)); return d.out()


def xsec(mode='default'):                                    # cross-section: Chicago on swamp mud just above Lake Michigan (pipes: new sewer + fresh dirt + raised city)
    d = Draw(2000, 1300); up = 220 if mode == 'pipes' else 0
    d.rect(40, 900, 1960, 1260, (110, 80, 60, 255)); d.rect(40, 800, 1960, 900, (90, 130, 90, 255)); d.rect(40, 860, 1960, 1260, (60, 140, 190, 180)); d.text(1500, 1120, 'LAKE MICHIGAN', 70, WT, stroke=5, stroke_fill=LINE)
    d.stroke([(40, 860), (1960, 860)], WT, 8)
    if mode == 'pipes': d.rect(40, 800 - up, 1960, 800, (170, 120, 80, 255)); d.dot(700, 700, 90, (150, 150, 166, 255)); d.ellipse(700, 700, 90, 90, outline=LINE, width=10); d.dot(700, 700, 50, (60, 60, 70, 255)); d.stroke([(40, 800 - up), (1960, 800 - up)], LINE, 8)
    for k, x in enumerate(range(120, 1900, 300)): h_ = 260 + (k % 3) * 80; d.rect(x, 800 - up - h_, x + 220, 800 - up, (196 - k * 6, 96 + k * 4, 70, 255)); d.rrect(x, 800 - up - h_, x + 220, 800 - up, 2, outline=LINE, width=8); win(d, x + 60, 800 - up - h_ + 60, x + 160, 800 - up - h_ + 150, (255, 220, 140, 255))
    if mode != 'pipes': [d.ellipse(x, 830, 40, 14, fill=(80, 110, 70, 255)) for x in range(160, 1900, 230)]
    else: d.text(1650, 560 - up, '14 FT', 80, CORAL, stroke=5, stroke_fill=LINE); d.stroke([(1550, 800), (1550, 800 - up)], CORAL, 12)
    return d.out()


def germ():                                                  # cholera as a grumpy cartoon germ cloud over a swampy puddle (no people hurt on screen)
    d = Draw(1300, 1100); d.ellipse(650, 960, 520, 110, fill=(90, 140, 100, 255), outline=LINE, width=12)
    for x, y, r in ((450, 450, 230), (700, 380, 270), (900, 480, 220), (650, 560, 240)): d.dot(x, y, r, (150, 210, 110, 255))
    for a in range(0, 360, 40): r_ = math.radians(a); x, y = 680 + 360 * math.cos(r_), 480 + 300 * math.sin(r_); d.stroke([(680 + 280 * math.cos(r_), 480 + 230 * math.sin(r_)), (x, y)], (120, 180, 90, 255), 20); d.dot(x, y, 34, (150, 210, 110, 255))
    eyes(d, 680, 470, 1.0, 'sad'); d.stroke([(560, 360), (640, 400)], LINE, 14); d.stroke([(800, 360), (720, 400)], LINE, 14); return d.out()


def twenty():                                                # one in twenty: 20 little figures, one floats up with a halo
    d = Draw(1800, 900); cols = [(255, 160, 90, 255), (120, 190, 240, 255), (170, 130, 230, 255), (110, 200, 150, 255)]
    for k in range(20):
        i, j = k % 10, k // 10; x, y = 120 + i * 175, 380 + j * 300
        if k == 13: y -= 260; d.ellipse(x, y - 110, 56, 16, outline=AMB, width=12); [d.ellipse(x + sg * 80, y + 30, 40, 26, fill=WT, outline=LINE, width=6) for sg in (-1, 1)]
        d.rrect(x - 50, y + 40, x + 50, y + 190, 40, fill=(200, 200, 214, 255) if k == 13 else cols[k % 4], outline=LINE, width=8); d.dot(x, y, 55, (255, 220, 190, 255)); d.ellipse(x, y, 55, 55, outline=LINE, width=8)
        [d.dot(x + sg * 18, y + 2, 7, LINE) for sg in (-1, 1)]
    return d.out()


def pipe():                                                  # new sewer pipe on a mound of fresh dirt, shovel stuck in
    d = Draw(1700, 1000); d.chord(850, 960, 800, 420, 180, 360, fill=(170, 120, 80, 255), outline=LINE, width=14)
    d.rrect(300, 380, 1400, 640, 130, fill=(170, 170, 186, 255), outline=LINE, width=14); d.ellipse(1400, 510, 70, 130, fill=(60, 60, 70, 255), outline=LINE, width=12); eyes(d, 800, 500, 0.8, 'happy')
    d.stroke([(1500, 900), (1580, 380)], (120, 80, 50, 255), 22); d.poly([(1460, 880), (1560, 900), (1530, 1000), (1440, 980)], fill=(180, 180, 196, 255), outline=LINE, width=8); return d.out()


def glass(sparkle=True):                                     # a perfect pane of glass in a gilded frame, sparkling, unbroken
    d = Draw(1000, 1200); d.rrect(80, 80, 920, 1120, 30, fill=(200, 150, 60, 255), outline=LINE, width=14); d.rect(160, 160, 840, 1040, (200, 236, 255, 255)); d.rrect(160, 160, 840, 1040, 2, outline=LINE, width=8)
    d.poly([(220, 300), (420, 200), (300, 500)], fill=(255, 255, 255, 170)); d.poly([(560, 800), (780, 640), (700, 900)], fill=(255, 255, 255, 140)); eyes(d, 500, 640, 0.9, 'happy')
    for x, y in ((120, 120), (880, 200), (860, 1080)): d.poly([(x, y - 60), (x + 16, y - 16), (x + 60, y), (x + 16, y + 16), (x, y + 60), (x - 16, y + 16), (x - 60, y), (x - 16, y - 16)], fill=WT, outline=LINE, width=5)
    return d.out()


def car(mode='default'):                                     # Pullman sleeping car (night: lit berths with sleepy faces + Zs; q: dark silhouette with "?")
    d = Draw(2000, 900)
    if mode == 'q':
        d.rrect(60, 200, 1940, 720, 80, fill=(70, 50, 110, 255)); [d.dot(x, 760, 90, (60, 40, 100, 255)) for x in (300, 520, 1480, 1700)]; d.text(1000, 470, '?', 380, AMB, stroke=12, stroke_fill=LINE); return d.out()
    d.rrect(60, 200, 1940, 720, 80, fill=(120, 40, 50, 255), outline=LINE, width=16); d.rect(60, 250, 1940, 300, (240, 190, 70, 255)); d.text(1000, 278, 'PULLMAN', 46, (120, 40, 50, 255))
    d.chord(1000, 220, 960, 120, 180, 360, fill=(90, 30, 40, 255), outline=LINE, width=14)
    for k in range(7):
        x = 220 + k * 250; win(d, x - 80, 360, x + 80, 560, (255, 220, 140, 255) if mode == 'night' else (170, 220, 250, 255))
        if mode == 'night': d.dot(x, 470, 46, (255, 220, 190, 255)); d.ellipse(x, 470, 46, 46, outline=LINE, width=6); [d.arc(x + sg * 16, 470, 10, 6, 20, 160, LINE, 5) for sg in (-1, 1)]; d.chord(x, 456, 48, 40, 180, 360, fill=(90, 130, 220, 255))
    if mode == 'night': [d.text(1700 + k * 90, 160 - k * 70, 'Z', 80 + k * 20, (160, 140, 255, 255), stroke=5, stroke_fill=LINE) for k in range(3)]
    for x in (300, 520, 1480, 1700): d.dot(x, 760, 90, (50, 50, 60, 255)); d.dot(x, 760, 36, (200, 200, 210, 255))
    d.rect(60, 840, 1940, 870, (120, 100, 90, 255)); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def gaslight(path):                                          # amber gaslight 1861 street at dusk: lamps, wooden sidewalks, low skyline
    im = sky((90, 60, 120), (255, 170, 90), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 240)): h_ = 260 + (k * 89) % 220; d.rect(x, 900 - h_, x + 220, 940, (150 + (k % 3) * 20, 80, 70, 255)); win(d, x + 60, 900 - h_ + 50, x + 160, 900 - h_ + 130, (255, 210, 120, 255))
    for x in range(150, W2, 520): d.rect(x - 8, 560, x + 8, 940, LINE); d.rrect(x - 36, 500, x + 36, 570, 12, fill=(255, 220, 140, 255), outline=LINE, width=6)
    fl(d, (120, 90, 70, 255)); im.alpha_composite(d.out()); [glow(im, x, 535, 120, (255, 200, 110, 140), 40) for x in range(150, W2, 520)]; im.convert('RGB').save(path)


def roseroom(path):                                          # cosy hotel room: rose wallpaper, gas sconces, framed picture
    im = sky((200, 110, 130), (240, 160, 160), 1.0); d = Draw(W2, H2)
    for x in range(60, W2, 160):
        for y in range(60, 900, 160): d.dot(x + (y // 160 % 2) * 80, y, 22, (240, 130, 150, 255))
    d.rect(0, 700, W2, 940, (150, 80, 90, 255)); d.rrect(900, 150, 1500, 520, 20, fill=(120, 170, 140, 255), outline=(200, 150, 60, 255), width=24)
    for x in (500, 1900): d.rect(x - 10, 300, x + 10, 400, (200, 150, 60, 255)); d.dot(x, 280, 30, (255, 220, 140, 255))
    fl(d, (120, 70, 60, 255)); im.alpha_composite(d.out()); [glow(im, x, 280, 120, (255, 210, 140, 120), 40) for x in (500, 1900)]; im.convert('RGB').save(path)


def parlour(path):                                           # emerald parlour: gold frames, flag, fireplace glow
    im = sky((20, 90, 70), (50, 150, 110), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 200): d.rect(x, 0, x + 12, 940, (200, 160, 70, 255))
    d.rrect(1600, 520, 2100, 940, 20, fill=(120, 60, 50, 255), outline=LINE, width=12); d.rect(1700, 640, 2000, 940, (40, 20, 20, 255)); d.dot(1850, 860, 70, AMB)
    d.rrect(300, 160, 700, 520, 10, fill=(240, 230, 210, 255), outline=(200, 160, 70, 255), width=24); [d.rect(320, 180 + k * 50, 680, 205 + k * 50, (200, 60, 70, 255)) for k in range(0, 7, 2)]; d.rect(320, 180, 480, 330, (40, 50, 110, 255))
    fl(d, (80, 50, 40, 255)); im.alpha_composite(d.out()); glow(im, 1850, 840, 220, (255, 170, 80, 120), 60); im.convert('RGB').save(path)


def blocksky(path):                                          # sky-blue 1860 day: far brick skyline, church spire, clouds
    im = sky((110, 180, 240), (230, 240, 250), 1.0); d = Draw(W2, H2)
    for x, y in ((300, 160), (1500, 220)): [d.dot(x + k * 90, y + (k % 2) * 24, 80, (255, 255, 255, 240)) for k in range(4)]
    for k, x in enumerate(range(0, W2, 200)): h_ = 180 + (k * 71) % 200; d.rect(x, 900 - h_, x + 180, 940, (200, 150, 130, 255))
    d.rect(1180, 400, 1260, 940, (180, 130, 110, 255)); d.poly([(1160, 400), (1220, 200), (1280, 400)], fill=(150, 100, 90, 255))
    fl(d, (150, 130, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def crawl(path):                                             # amber crawlspace under the building: timber beams, lantern glow
    im = sky((110, 70, 30), (200, 130, 60), 1.0); d = Draw(W2, H2)
    for y in (60, 260): d.rect(0, y, W2, y + 90, (120, 80, 40, 255)); d.stroke([(0, y), (W2, y)], LINE, 6)
    for x in range(100, W2, 400): d.rect(x, 0, x + 60, 940, (130, 90, 50, 255))
    fl(d, (110, 80, 50, 255)); im.alpha_composite(d.out()); [glow(im, x, 500, 200, (255, 200, 120, 110), 60) for x in (600, 1800)]; im.convert('RGB').save(path)


def shopst(path):                                            # cream shopping street, bunting, bright noon
    im = sky((150, 210, 250), (255, 244, 220), 1.0); d = Draw(W2, H2); d.stroke([(0, 120), (800, 200), (1600, 120), (W2, 200)], LINE, 5)
    for x in range(40, W2, 80): y = 160 + 40 * math.sin(x / 130); d.poly([(x, y), (x + 50, y), (x + 25, y + 60)], fill=[CORAL, AMB, (90, 170, 140, 255)][(x // 80) % 3])
    for k, x in enumerate(range(0, W2, 300)): d.rect(x, 380, x + 280, 940, [(240, 220, 190, 255), (220, 190, 160, 255)][k % 2])
    fl(d, (170, 150, 120, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def swamp(path):                                             # teal swamp + lake horizon: reeds, cattails, lily pads, mist
    im = sky((60, 140, 150), (190, 230, 210), 1.0); d = Draw(W2, H2); d.rect(0, 640, W2, 940, (60, 130, 150, 255))
    for x in range(30, W2, 70): d.stroke([(x, 940), (x + 10, 640 - (x % 5) * 30)], (60, 110, 60, 255), 10); d.ellipse(x + 10, 640 - (x % 5) * 30, 12, 30, fill=(120, 80, 50, 255))
    fl(d, (70, 110, 80, 255)); im.alpha_composite(d.out()); glow(im, 1200, 600, 700, (230, 255, 240, 80), 140); im.convert('RGB').save(path)


def mistnight(path):                                         # misty green-blue night, moon, rooftops
    im = sky((30, 60, 70), (70, 120, 110), 1.0); d = Draw(W2, H2); d.dot(1800, 220, 90, (240, 250, 220, 255)); stars(d, 40, 500, 4)
    for k, x in enumerate(range(0, W2, 230)): h_ = 240 + (k % 3) * 70; d.rect(x, 940 - h_, x + 210, 940, (40, 70, 70, 255)); win(d, x + 70, 940 - h_ + 60, x + 140, 940 - h_ + 130, (255, 220, 140, 255))
    fl(d, (50, 70, 60, 255)); im.alpha_composite(d.out()); glow(im, 1800, 220, 220, (240, 255, 220, 90), 60); im.convert('RGB').save(path)


def works(path):                                             # terracotta street works: dirt mounds, cranes, sunset
    im = sky((240, 130, 90), (255, 210, 150), 1.0); d = Draw(W2, H2)
    for x in (300, 1900): d.stroke([(x, 940), (x, 300), (x + 400, 300)], (90, 60, 50, 255), 20); d.stroke([(x + 380, 300), (x + 380, 520)], LINE, 6)
    for x in (900, 1500): d.chord(x, 940, 300, 200, 180, 360, fill=(170, 110, 70, 255), outline=LINE, width=10)
    fl(d, (150, 100, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def workshop(path):                                          # brass-cream glass workshop: big arched windows, shelves of panes
    im = sky((250, 236, 206), (240, 210, 160), 1.0); d = Draw(W2, H2)
    for x in (300, 1000, 1700): d.chord(x + 200, 500, 200, 200, 180, 360, fill=(170, 220, 250, 255), outline=(180, 140, 60, 255), width=20); d.rect(x, 500, x + 400, 860, (170, 220, 250, 255)); d.rrect(x, 500, x + 400, 860, 2, outline=(180, 140, 60, 255), width=20)
    fl(d, (180, 140, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def railnight(path):                                         # Prussian-blue starry night with rail tracks to the horizon and a moon
    im = sky((14, 24, 70), (40, 80, 150), 1.0); d = Draw(W2, H2); stars(d, 120, 700, 8); d.dot(500, 200, 100, (255, 246, 210, 255))
    hills(d, 760, (30, 50, 90, 255), 60, 3); d.poly([(1100, 760), (1300, 760), (2000, 940), (400, 940)], fill=(90, 80, 80, 255)); [d.stroke([(1150 - k * 60, 760 + k * 30), (1250 + k * 60, 760 + k * 30)], (140, 110, 80, 255), 8) for k in range(7)]
    fl(d, (40, 50, 80, 255)); im.alpha_composite(d.out()); glow(im, 500, 200, 260, (255, 240, 200, 100), 60); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast3(('pullman', 'guest', 'senator', 'crew1', 'crew2'))
    multi = dict(hotel={'default': hotel(), 'wave': hotel('wave')}, jacks={'default': jacks()}, steps={'default': steps(), 'steep': steps(True)}, winframe={'default': winframe()},
                 bed={'default': bed()}, dinner={'default': dinner()}, desk={'default': desk()}, block={'default': block()}, crew={'default': crew()},
                 screw={'default': screw(), 'turn': screw(True)}, bell={'default': bell()}, shop={'default': shop()}, xsec={'default': xsec(), 'pipes': xsec('pipes')},
                 germ={'default': germ()}, twenty={'default': twenty()}, pipe={'default': pipe()}, glass={'default': glass()}, car={k: car(k) for k in ('default', 'night', 'q')})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PL, GR, RB = (90, 50, 110, 255), (30, 110, 80, 255), (150, 50, 50, 255)
    cards = dict(hookc=M.bigneon('HOTEL ROSE', '6 FEET!', 860, YEL, CORAL),
                 y1861=M.cal('CHICAGO', '1861', RB),
                 inch=stamp('INCH BY INCH...', 860, PL, 120, -3),
                 senat=P_('A U.S. SENATOR', 'IS STAYING THERE', GR, 980, 130, 110, YEL),
                 steeper=stamp('STEEPER?!', 680, RB, 170, 4),
                 eye=stamp('PAST EYE LEVEL!', 900, PRU, 120, -3),
                 year=stamp('A YEAR EARLIER...', 940, PL, 110, 3),
                 f320=M.bigneon('320 FEET', 'OF SHOPS', 860, YEL, AMB),
                 m600=M.bigneon('600', 'MEN', 640, YEL, CORAL),
                 notch=stamp('ONE NOTCH!', 760, RB, 150, -4),
                 open_=stamp('STORES STAY OPEN!', 960, GR, 110, 3),
                 swampc=P_('BUILT ON', 'A SWAMP', (40, 110, 110, 255), 820, 130, 170, YEL),
                 y1854=M.cal('CHOLERA', '1854', (40, 90, 80, 255)),
                 one20=M.bigneon('1 IN', '20', 560, YEL, (150, 230, 120, 255)),
                 wild=M.bigneon('A WILD', 'FIX!', 700, YEL, CORAL),
                 f14=M.bigneon('UP TO', '14 FEET!', 760, YEL, AMB),
                 pullc=P_('GEORGE', 'PULLMAN', PL, 860, 130, 190, YEL),
                 pane=stamp('NOT ONE PANE BROKEN!', 1000, (40, 120, 170, 255), 100, -3),
                 wheels=M.bigneon('ON', 'WHEELS!', 700, YEL, CORAL),
                 travels=P_('A HOTEL', 'THAT TRAVELS!', RB, 960, 150, 150, YEL))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    CE.tiles(T('boards.jpg'), (150, 110, 80), (136, 98, 70)); CE.tiles(T('rug.jpg'), (170, 70, 80), (154, 60, 70)); CE.tiles(T('green.jpg'), (60, 100, 70), (52, 88, 62)); CE.tiles(T('cobble.jpg'), (170, 150, 130), (156, 136, 118))
    M.sandtex(T('dirt.jpg'), (140, 100, 70), (126, 88, 60)); CE.tiles(T('shopfl.jpg'), (220, 200, 170), (206, 186, 156)); M.sandtex(T('mud.jpg'), (90, 110, 80), (78, 98, 70)); M.sandtex(T('night.jpg'), (50, 70, 60), (42, 60, 52))
    CE.tiles(T('brass.jpg'), (220, 190, 140), (206, 176, 126)); M.sandtex(T('ballast.jpg'), (70, 70, 90), (60, 60, 78)); CE.tiles(T('pave.jpg'), (120, 100, 90), (106, 88, 78))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(gaslight=gaslight, roseroom=roseroom, parlour=parlour, blocksky=blocksky, crawl=crawl, shopst=shopst, swamp=swamp, mistnight=mistnight, works=works, workshop=workshop, railnight=railnight)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
