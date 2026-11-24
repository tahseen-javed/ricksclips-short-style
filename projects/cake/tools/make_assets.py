#!/usr/bin/env python3
"""Assets for video 23: German chocolate cake isn't German - it is named after Sam German and was born in Texas.
Cocoa-cherry + Texas-turquoise world: turquoise-orange Texas sunset with windmill + mesas (hook + loop), gaslit 1850s chocolate works,
cocoa-velvet macro studio, turquoise-tile 1957 ranch kitchen, steel-teal Dallas press hall, lemon 1950s suburb, navy-gold boardroom,
midnight map room, emerald sales board, plum writer's desk, rose-sepia travel-poster sky.
Cute cast (new): Sam German (chef toque), a Texas homemaker (red stetson, gingham), a General Foods exec (bow tie), three readers.
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
CH1, CH2, COCO, PEC, CHER, TURQ = (92, 52, 40, 255), (70, 38, 30, 255), (236, 196, 130, 255), (170, 110, 60, 255), (240, 50, 70, 255), (40, 200, 200, 255)
LA.NEW.update({
    'samg': dict(sk=0, style='curly', hair=(110, 66, 40, 255), suit=(250, 250, 246, 255), shade=(220, 220, 214, 255), body='chef', acc=CHER, stache=(110, 66, 40, 255), xhat='toque'),
    'texmom': dict(sk=0, style='bob', hair=(190, 80, 40, 255), suit=(60, 190, 190, 255), shade=(40, 160, 164, 255), body='gingham', freck=1, band=YEL, xhat='stetson', hatc=CHER, band2=WT),
    'gfexec': dict(sk=1, style='bald', hair=(230, 230, 230, 255), suit=(40, 50, 110, 255), shade=(30, 38, 86, 255), body='bowtie', acc=(250, 200, 60, 255), stache=(230, 230, 230, 255), glasses=1),
    'rdr1': dict(sk=2, style='spiky', hair=(30, 24, 24, 255), suit=(250, 200, 60, 255), shade=(220, 170, 40, 255), body='sweater'),
    'rdr2': dict(sk=0, style='bob', hair=(240, 200, 110, 255), suit=(150, 220, 170, 255), shade=(120, 196, 146, 255), body='polka', band=PINK),
    'rdr3': dict(sk=1, style='quiff', hair=(60, 40, 30, 255), suit=(250, 120, 90, 255), shade=(220, 96, 70, 255), body='denim', glasses=2),
})


def cake(face='default', hat=False):                         # glossy 3-layer chocolate cake, coconut-pecan frosting, turquoise cake stand, face
    d = Draw(1200, 1300); d.rrect(420, 1080, 780, 1140, 20, fill=TURQ, outline=LINE, width=12); d.poly([(520, 1080), (680, 1080), (640, 980), (560, 980)], fill=TURQ, outline=LINE, width=12)
    d.ellipse(600, 970, 470, 60, fill=(120, 230, 230, 255), outline=LINE, width=14)
    for k, y in enumerate((780, 600, 420)):
        d.rrect(170, y - 20, 1030, y + 170, 50, fill=(CH1, CH2, CH1)[k], outline=LINE, width=14); d.rect(190, y - 30, 1010, y + 10, COCO)
        for j in range(16): d.dot(210 + j * 52, y - 14 + (j % 3) * 8, 12, PEC)
    d.ellipse(600, 405, 440, 70, fill=COCO, outline=LINE, width=14)
    for j in range(26): d.dot(260 + (j * 97) % 690, 380 + (j * 31) % 50, 14, PEC); d.dot(240 + (j * 61) % 720, 394 + (j * 17) % 40, 8, WT)
    for x in (220, 1000): d.stroke([(x, 420), (x + 10, 520)], (110, 64, 46, 255), 18)
    shine(d, 230, 640, 120); shine(d, 230, 820, 110); eyes(d, 600, 680, 1.25, face)
    if hat:
        d.chord(600, 330, 300, 60, 180, 360, fill=CHER, outline=LINE, width=14); d.ellipse(600, 330, 300, 26, fill=CHER, outline=LINE, width=12)
        d.rrect(470, 190, 730, 340, 50, fill=CHER, outline=LINE, width=14); d.rect(474, 300, 726, 328, WT)
    return d.out()


def bar(n=1):                                                # German's Sweet Chocolate bar: torn wrapper, glossy squares
    d = Draw(1300, 700); d.rrect(40, 60, 1260, 640, 40, fill=CH1, outline=LINE, width=16)
    for x in range(80, 1240, 140):
        for y in (100, 360): d.rrect(x, y, x + 120, y + 230, 18, fill=CH2, outline=LINE, width=6); d.rect(x + 14, y + 14, x + 34, y + 120, (150, 100, 80, 200))
    d.rrect(380, 40, 1280, 660, 30, fill=(250, 236, 200, 255), outline=LINE, width=16); d.rect(380, 120, 1280, 170, CHER); d.rect(380, 530, 1280, 580, CHER)
    d.text(830, 290, "GERMAN'S", 160, CH2, stroke=6, stroke_fill=WT); d.text(830, 440, 'SWEET CHOCOLATE', 84, CHER, stroke=4, stroke_fill=LINE)
    d.poly([(380, 40), (430, 120), (390, 200), (440, 300), (390, 400), (440, 500), (380, 660)], fill=(250, 236, 200, 255), outline=LINE, width=10)
    return d.out()


def kettle():                                                # copper chocolate kettle with a paddle + face
    d = Draw(1100, 1100); d.chord(550, 500, 420, 480, 0, 180, fill=(214, 120, 70, 255), outline=LINE, width=16); d.ellipse(550, 500, 420, 70, fill=CH1, outline=LINE, width=14)
    d.ellipse(480, 490, 120, 24, fill=(140, 90, 70, 255)); d.stroke([(700, 120), (620, 520)], (170, 120, 70, 255), 40); d.stroke([(700, 120), (620, 520)], LINE, 8)
    for x in (300, 800): d.rect(x - 20, 920, x + 20, 1060, (90, 60, 50, 255))
    shine(d, 220, 600, 160); eyes(d, 550, 720, 1.1, 'happy'); return d.out()


def recipe():                                                # recipe card with a cake doodle
    d = Draw(1100, 800); d.rrect(40, 40, 1060, 760, 30, fill=(255, 250, 236, 255), outline=LINE, width=16)
    for y in range(260, 740, 70): d.stroke([(80, y), (1020, y)], (150, 200, 230, 255), 5)
    d.rect(40, 200, 1060, 210, CHER); d.text(550, 130, 'RECIPE', 110, CHER, stroke=5, stroke_fill=LINE)
    for k, w in enumerate((600, 520, 640, 480)): d.stroke([(110, 300 + k * 90), (110 + w, 300 + k * 90)], (90, 80, 120, 255), 12)
    d.rrect(780, 300, 1000, 520, 30, fill=CH1, outline=LINE, width=10); d.rect(790, 290, 990, 320, COCO); d.rect(790, 400, 990, 420, COCO)
    return d.out()


def usmap(stage=0):                                          # stylised USA, Texas lit, routes to newspapers (stage 1)
    d = Draw(1500, 1000)
    US = [(60, 220), (330, 170), (700, 190), (900, 150), (1060, 220), (1250, 130), (1320, 200), (1190, 350), (1160, 470), (1090, 570), (1160, 800), (1110, 820), (1020, 640),
          (900, 660), (770, 670), (710, 790), (630, 720), (540, 590), (430, 600), (240, 560), (90, 440)]
    d.poly([(x + 6, y + 14) for x, y in US], fill=(10, 20, 50, 160)); d.poly(US, fill=(110, 160, 230, 255), outline=LINE, width=14)
    TX = [(520, 470), (610, 470), (620, 530), (760, 560), (770, 670), (710, 790), (630, 720), (560, 610), (470, 590)]
    d.poly(TX, fill=CHER, outline=LINE, width=12); d.dot(640, 600, 26, YEL); d.ellipse(640, 600, 26, 26, outline=LINE, width=8)
    if stage:
        for x, y in ((200, 300), (380, 260), (900, 260), (1180, 230), (1060, 420), (1000, 560), (820, 380), (300, 470), (1110, 700), (620, 300)):
            d.stroke([(640, 600), ((640 + x) / 2, min(600, y) - 120), (x, y)], (255, 236, 120, 255), 12); d.dot(x, y - 30, 26, YEL); d.poly([(x - 20, y - 26), (x + 20, y - 26), (x, y + 10)], fill=YEL, outline=LINE, width=6)
            d.ellipse(x, y - 30, 26, 26, outline=LINE, width=8)
    return d.out()


def stack():                                                 # a tower of chocolate bars shooting up + arrow
    d = Draw(900, 1300)
    for k in range(9): y = 1180 - k * 120; d.rrect(180 + (k % 2) * 30, y, 660 + (k % 2) * 30, y + 100, 20, fill=CH1, outline=LINE, width=12); d.rect(380 + (k % 2) * 30, y, 470 + (k % 2) * 30, y + 100, CHER)
    d.poly([(720, 120), (860, 340), (800, 340), (800, 600), (640, 600), (640, 340), (580, 340)], fill=(80, 230, 120, 255), outline=LINE, width=12); return d.out()


def typer(stage=0):                                          # cute typewriter; stage 0 paper says GERMAN'S, stage 1 the 'S flies off
    d = Draw(1450, 1200); d.rrect(260, 140, 1040, 600, 20, fill=(255, 252, 240, 255), outline=LINE, width=14)
    d.text(650, 360, 'GERMAN' if stage else "GERMAN'S", 150, CH2, stroke=4, stroke_fill=WT)
    d.rrect(160, 560, 1140, 640, 40, fill=(60, 60, 70, 255), outline=LINE, width=14); d.rrect(120, 620, 1180, 1120, 80, fill=(240, 90, 110, 255), outline=LINE, width=16)
    for r_ in range(3):
        for k in range(9 - r_): d.dot(260 + r_ * 50 + k * 100, 960 + r_ * 50 - 120, 34, WT); d.ellipse(260 + r_ * 50 + k * 100, 840 + r_ * 50, 34, 34, outline=LINE, width=7)
    eyes(d, 650, 740, 0.8, 'shocked' if stage else 'happy'); shine(d, 170, 700, 200)
    if stage:
        for k, (x, y, s) in enumerate(((1130, 200, "'"), (1260, 330, 'S'))): d.text(x, y, s, 190, CHER, stroke=8, stroke_fill=LINE); [d.stroke([(x - 160 - j * 30, y - 40 + j * 40), (x - 90 - j * 30, y - 40 + j * 40)], WT, 8) for j in range(3)]
    return d.out()


def globe():                                                 # globe: USA + Europe, dotted arc Texas -> Germany, "?" bubble
    d = Draw(1200, 1200); d.dot(600, 600, 500, (70, 150, 230, 255)); d.ellipse(600, 600, 500, 500, outline=LINE, width=16)
    d.poly([(170, 380), (420, 330), (470, 450), (400, 560), (330, 640), (240, 560)], fill=(120, 210, 120, 255), outline=LINE, width=10); d.dot(330, 560, 26, CHER)
    d.poly([(820, 300), (960, 280), (1010, 380), (930, 470), (840, 440)], fill=(120, 210, 120, 255), outline=LINE, width=10); d.dot(900, 380, 26, YEL)
    for k in range(13): t = k / 12; x, y = 330 + (900 - 330) * t, 560 + (380 - 560) * t - 260 * math.sin(math.pi * t); d.dot(x, y, 12, WT)
    d.dot(960, 170, 110, WT); d.ellipse(960, 170, 110, 110, outline=LINE, width=12); d.text(960, 170, '?', 150, CHER, stroke=4, stroke_fill=LINE); shine(d, 300, 300, 200, 40)
    return d.out()


def nametag(nm='?'):                                         # HELLO MY NAME IS tag (open loop "?", resolved "GERMAN")
    d = Draw(1200, 800); d.rrect(30, 30, 1170, 770, 60, fill=CHER, outline=LINE, width=16); d.text(600, 120, 'HELLO', 110, WT, stroke=5, stroke_fill=LINE)
    d.text(600, 220, 'MY NAME IS', 70, WT, stroke=4, stroke_fill=LINE); d.rrect(80, 290, 1120, 700, 30, fill=WT, outline=LINE, width=10)
    d.text(600, 500, nm, 220 if nm == '?' else 190, CH2 if nm != '?' else CHER, stroke=4, stroke_fill=LINE); return d.out()


def star():                                                  # glossy Texas lone star badge
    d = Draw(1000, 1000); pts = [(500 + (440 if k % 2 == 0 else 190) * math.sin(k * math.pi / 5), 520 - (440 if k % 2 == 0 else 190) * math.cos(k * math.pi / 5)) for k in range(10)]
    d.poly(pts, fill=(255, 210, 70, 255), outline=LINE, width=18); d.poly([(500, 120), (560, 420), (500, 520)], fill=(255, 240, 160, 255)); eyes(d, 500, 560, 0.9, 'happy'); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def texas(path):                                             # Texas sunset: turquoise sky -> orange, mesas, windmill, prickly pears
    im = sky((40, 190, 200), (255, 150, 70), 1.1); d = Draw(W2, H2); d.dot(1500, 640, 210, (255, 220, 120, 255))
    for x, w, h in ((100, 500, 260), (900, 380, 200), (1800, 520, 300)): d.poly([(x, 800), (x + 60, 800 - h), (x + w - 60, 800 - h), (x + w, 800)], fill=(200, 90, 70, 255), outline=LINE, width=10)
    d.rect(560, 380, 580, 860, (90, 60, 50, 255)); [d.stroke([(570, 380), (570 + 120 * math.cos(a), 380 + 120 * math.sin(a))], (240, 236, 220, 255), 26) for a in np.linspace(0, 2 * math.pi, 9)[:-1]]
    d.dot(570, 380, 24, LINE); hills(d, 820, (220, 130, 70, 255), 40, 2)
    for x in (300, 1300, 2150): [d.ellipse(x + dx, 860 - dy, 50, 70, fill=(80, 170, 100, 255), outline=LINE, width=8) for dx, dy in ((0, 0), (-50, 70), (50, 80))]
    fl(d, (200, 120, 70, 255)); im.alpha_composite(d.out()); glow(im, 1500, 640, 500, (255, 220, 140, 120), 120); im.convert('RGB').save(path)


def works(path):                                             # 1850s chocolate works: mahogany walls, gaslight, copper vats, pipes
    im = sky((70, 36, 60), (160, 80, 60), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.rect(x, 0, x + 18, 940, (60, 30, 30, 255))
    for x in (300, 1100, 1900): d.chord(x, 760, 240, 260, 0, 180, fill=(214, 120, 70, 255), outline=LINE, width=12); d.ellipse(x, 760, 240, 40, fill=CH1, outline=LINE, width=10)
    d.stroke([(0, 200), (W2, 200)], (180, 110, 70, 255), 40); d.stroke([(0, 200), (W2, 200)], LINE, 6)
    for x in (700, 1500, 2300): d.stroke([(x, 200), (x, 320)], (60, 40, 40, 255), 10); d.dot(x, 350, 40, (255, 200, 120, 255))
    fl(d, (90, 50, 40, 255)); im.alpha_composite(d.out())
    for x in (700, 1500, 2300): glow(im, x, 350, 260, (200, 140, 255, 90), 80)
    im.convert('RGB').save(path)


def studio(path):                                            # cocoa-velvet macro studio with cream + cherry bokeh
    im = sky((50, 26, 22), (120, 66, 50), 1.0); d = Draw(W2, H2); r = np.random.RandomState(5)
    for _ in range(40): d.dot(r.randint(0, W2), r.randint(0, 800), r.randint(30, 90), ((255, 230, 190, 70), (255, 80, 100, 60), (255, 200, 120, 60))[r.randint(3)])
    fl(d, (70, 36, 30, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 600, (255, 200, 150, 60), 120); im.convert('RGB').save(path)


def ranch(path):                                             # 1957 Texas ranch kitchen: turquoise tiles, cherry cabinets, sunset window with cactus, star clock
    im = sky((90, 210, 210), (170, 236, 230), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 80):
        for y in range(420, 940, 80): d.rect(x + 3, y + 3, x + 77, y + 77, (120, 220, 216, 255))
    d.rrect(900, 160, 1500, 560, 20, fill=(255, 160, 80, 255), outline=WT, width=26); d.dot(1200, 470, 90, (255, 230, 120, 255)); d.rect(900, 520, 1500, 560, (200, 110, 70, 255))
    d.rrect(1300, 360, 1350, 540, 24, fill=(80, 170, 100, 255), outline=LINE, width=8)
    for x in (100, 1700): d.rrect(x, 100, x + 600, 360, 16, fill=CHER, outline=LINE, width=12); d.dot(x + 300, 230, 14, WT)
    d.dot(700, 260, 70, WT); d.ellipse(700, 260, 70, 70, outline=LINE, width=10); fl(d, (240, 236, 220, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def press(path):                                             # Dallas press hall: steel teal, tangerine rollers, paper ribbons zigzag overhead
    im = sky((40, 100, 110), (90, 160, 160), 1.0); d = Draw(W2, H2)
    for k in range(4): y = 130 + k * 110; d.stroke([(0, y), (W2, y + 60)], (250, 246, 230, 255), 34); d.stroke([(0, y), (W2, y + 60)], LINE, 4)
    for x in (300, 1000, 1700): d.rrect(x, 560, x + 500, 900, 30, fill=(70, 80, 90, 255), outline=LINE, width=12); [d.dot(x + 120 + j * 260, 640, 80, (255, 150, 50, 255)) for j in range(2)]
    fl(d, (80, 96, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def suburb(path):                                            # 1950s suburb at noon: lemon sky, ranch houses with candy roofs, lollipop trees
    im = sky((120, 200, 250), (255, 240, 150), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(80, W2, 460)):
        d.rect(x, 600, x + 360, 860, (250, 246, 236, 255)); d.poly([(x - 30, 600), (x + 180, 470), (x + 390, 600)], fill=(CHER, TURQ, YEL, PINK, (150, 110, 230, 255), ORNG)[k % 6], outline=LINE, width=10)
        win(d, x + 50, 660, x + 150, 760, (150, 210, 250, 255)); d.rect(x + 220, 700, x + 300, 860, (150, 90, 60, 255)); ptree(d, x + 420, 860, 0.8, (90, 200, 110, 255))
    fl(d, (120, 200, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def board(path):                                             # General Foods boardroom: navy panels, gold-framed window on a golden skyline
    im = sky((30, 40, 90), (60, 70, 130), 1.0); d = Draw(W2, H2); d.rrect(700, 120, 1700, 700, 10, fill=(255, 190, 110, 255), outline=(240, 200, 90, 255), width=30)
    for k, x in enumerate(range(720, 1690, 90)): h = 160 + (k * 73) % 300; d.rect(x, 700 - h, x + 80, 700, (110, 70, 90, 255)); [d.rect(x + 16, 700 - h + 20 + j * 50, x + 30, 700 - h + 34 + j * 50, YEL) for j in range(h // 60)]
    for x in (100, 400, 1900, 2200): d.rect(x, 80, x + 200, 860, (40, 52, 110, 255)); d.rect(x, 80, x + 200, 100, (240, 200, 90, 255))
    fl(d, (60, 40, 50, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def maproom(path):                                           # midnight map room: navy, glowing grid, small stars
    im = sky((14, 20, 60), (40, 60, 130), 1.0); d = Draw(W2, H2); stars(d, 90, 700, 11)
    for x in range(0, W2, 160): d.stroke([(x, 0), (x, 940)], (80, 130, 230, 90), 4)
    for y in range(0, 940, 160): d.stroke([(0, y), (W2, y)], (80, 130, 230, 90), 4)
    fl(d, (30, 40, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 600, 700, (90, 160, 255, 70), 120); im.convert('RGB').save(path)


def sales(path):                                             # emerald sales board: ticker strips, arrows up, gold coins
    im = sky((20, 110, 80), (80, 190, 130), 1.0); d = Draw(W2, H2)
    for y in (140, 300): d.rect(0, y, W2, y + 90, (14, 60, 44, 255)); [d.poly([(x, y + 70), (x + 30, y + 20), (x + 60, y + 70)], fill=(120, 255, 150, 255)) for x in range(60, W2, 220)]
    for x in range(100, W2, 300): d.dot(x, 700, 60, (255, 210, 70, 255)); d.ellipse(x, 700, 60, 60, outline=LINE, width=8)
    fl(d, (30, 90, 64, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def desk(path):                                              # plum writer's room: dotted wallpaper, shelves, warm lamp pool
    im = sky((80, 40, 90), (140, 80, 130), 1.0); d = Draw(W2, H2)
    for x in range(40, W2, 90):
        for y in range(40, 900, 90): d.dot(x + (y // 90 % 2) * 45, y, 8, (200, 140, 200, 120))
    for x in (100, 1800): d.rect(x, 200, x + 500, 220, (110, 70, 50, 255)); [d.rect(x + 20 + j * 60, 90, x + 64 + j * 60, 200, (CHER, YEL, TURQ, PINK, WT, ORNG, VIO, CHER)[j]) for j in range(8)]
    fl(d, (90, 50, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 640, 600, (255, 210, 140, 110), 120); im.convert('RGB').save(path)


def poster(path):                                            # rose-sepia travel-poster sky: big sun rays, clouds, faraway hills, a plane trail
    im = sky((240, 140, 150), (255, 220, 180), 1.0); d = Draw(W2, H2)
    for k in range(12): a = k * math.pi / 12; d.poly([(1200, 900), (1200 + 1800 * math.cos(a - 0.05), 900 - 1800 * math.sin(a - 0.05)), (1200 + 1800 * math.cos(a + 0.05), 900 - 1800 * math.sin(a + 0.05))], fill=(255, 255, 255, 40))
    for x, y in ((300, 200), (1800, 260), (1000, 120)): [d.dot(x + j * 70, y + (j % 2) * 20, 70, (255, 250, 245, 230)) for j in range(4)]
    d.stroke([(200, 600), (800, 380), (1400, 330), (2000, 420)], (255, 255, 255, 200), 12); hills(d, 820, (150, 110, 160, 255), 60, 3)
    fl(d, (170, 120, 150, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast2(('samg', 'texmom', 'gfexec', 'rdr1', 'rdr2', 'rdr3'))
    multi = dict(cake={'default': cake(), 'shocked': cake('shocked'), 'sad': cake('sad'), 'tex': cake('default', True)}, bar={'default': bar()}, kettle={'default': kettle()},
                 recipe={'default': recipe()}, usmap={'default': usmap(0), 'p1': usmap(1)}, stack={'default': stack()}, typer={'default': typer(0), 'b': typer(1)},
                 globe={'default': globe()}, ntag={'default': nametag('?'), 'g': nametag('GERMAN')}, tstar={'default': star()},
                 news={'default': LA.paper("GERMAN'S CHOCOLATE CAKE", 'A TEXAS RECIPE!', 900)})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    COC, TQ = (110, 60, 46, 255), (30, 150, 150, 255)
    cards = dict(hookc=M.bigneon("IT'S NOT", 'GERMAN!', 900, YEL, (255, 90, 110, 255)),
                 manc=P_('A MAN CALLED', 'GERMAN', COC, 960, 120, 170, YEL),
                 texc=stamp('BORN IN TEXAS!', 900, CHER, 130, -4),
                 y1850=P_('1850s', 'A CHOCOLATE MAKER', COC, 900, 220, 110, YEL),
                 samc=P_('SAM', 'GERMAN', (200, 60, 70, 255), 860, 170, 170, WT),
                 sweetc=stamp('A SWEET BAKING BAR', 960, COC, 110, 3),
                 bakers=P_("BAKER'S", 'CHOCOLATE CO.', (150, 40, 50, 255), 960, 160, 120, YEL),
                 named=stamp('NAMED AFTER HIM!', 900, (90, 60, 160, 255), 120, -3),
                 y1957=M.cal('IN', '1957', TQ),
                 homec=P_('A TEXAS', 'HOMEMAKER', TQ, 920, 150, 160, YEL),
                 dallas=stamp('A DALLAS NEWSPAPER', 960, (240, 120, 40, 255), 110, 3),
                 crazy=M.bigneon('READERS WENT', 'CRAZY!', 960, YEL, PINK),
                 gfc=P_('GENERAL FOODS', "OWNED BAKER'S", (40, 50, 110, 255), 1000, 130, 120, YEL),
                 across=stamp('ACROSS THE COUNTRY!', 980, (40, 90, 200, 255), 110, -3),
                 oneyear=stamp('IN ONE YEAR!', 820, (40, 150, 90, 255), 140, 3),
                 quietly=stamp('QUIETLY DROPPED...', 900, (120, 60, 130, 255), 120, -4),
                 gsc=P_("GERMAN'S", 'CHOCOLATE CAKE', COC, 1000, 170, 120, YEL),
                 gcc=P_('GERMAN', 'CHOCOLATE CAKE', CHER, 1000, 170, 120, YEL),
                 fromde=stamp('FROM GERMANY?', 860, (60, 60, 70, 255), 140, 3),
                 puretx=M.bigneon('PURE', 'TEXAS!', 760, YEL, (255, 90, 110, 255)),
                 lastn=P_("A MAN'S", 'LAST NAME', (200, 60, 70, 255), 920, 170, 150, YEL))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('desert.jpg'), (220, 150, 90), (200, 132, 76), seed=4); CE.tiles(T('mahog.jpg'), (110, 60, 50), (96, 50, 42)); M.sandtex(T('velvet.jpg'), (90, 46, 38), (76, 38, 30))
    CE.tiles(T('lino.jpg'), (250, 246, 236), (240, 90, 100)); CE.tiles(T('steel.jpg'), (110, 126, 130), (96, 112, 116)); CE.tiles(T('lawn.jpg'), (130, 210, 110), (116, 194, 98))
    CE.tiles(T('carpet.jpg'), (120, 40, 60), (106, 34, 52)); CE.tiles(T('grid.jpg'), (40, 50, 110), (30, 40, 96)); CE.tiles(T('emer.jpg'), (40, 120, 90), (30, 104, 76))
    B.tex_wood(T('wood.jpg')); M.sandtex(T('sepia.jpg'), (200, 150, 160), (186, 136, 146))
    CE.tiles(T('pave.jpg'), (200, 130, 80), (186, 118, 70)); G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(texas=texas, works=works, studio=studio, ranch=ranch, press=press, suburb=suburb, board=board, maproom=maproom, sales=sales, desk=desk, poster=poster)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
