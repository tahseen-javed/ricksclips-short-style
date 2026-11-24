#!/usr/bin/env python3
"""Assets for video 20: the 1904 Olympic marathon (car, rat poison, a legal win).
Sun-scorched 1904 Midwest world: turquoise sky, terracotta + mustard dust, ivory fair palace, chartreuse poison accent, violet dusk archive.
Cute cast: Fred Lorz, Thomas Hicks, Felix Carvajal, Len Tau, James Sullivan (top hat), a trainer, a boater judge; hero props with faces.
usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
import mono_assets as MA
import hx_assets as X
from hx_assets import *

ROOT = B.ROOT


def car(face='default'):                                     # 1904 runabout: red body, brass lamps with eyes, spoked wheels, a driver
    im = Image.new('RGBA', (1500, 1000), (0, 0, 0, 0)); d = Draw(1500, 1000)
    if face == 'mystery': d.dot(820, 330, 150, (40, 40, 56, 245)); d.rrect(690, 440, 950, 640, 60, fill=(40, 40, 56, 245)); d.text(820, 340, '?', 200, LIME, stroke=10, stroke_fill=LINE)
    if face == 'lorz': d.rrect(700, 450, 940, 640, 60, fill=(250, 250, 240, 255), outline=LINE, width=12)
    im.alpha_composite(d.out())
    if face == 'lorz':
        hd = MA.head('lorz', 'happy'); k = 420 / hd.width; hd = hd.resize((420, int(hd.height * k))); im.alpha_composite(hd, (int(820 - H['cx'] * k), int(330 - H['hcy'] * k)))
    base = im
    e = Draw(1500, 1000)
    e.rrect(160, 560, 1340, 800, 70, fill=(220, 50, 60, 255), outline=LINE, width=16); e.rrect(240, 470, 640, 600, 40, fill=(190, 36, 50, 255), outline=LINE, width=14)
    e.stroke([(980, 560), (1040, 380)], LINE, 18); e.dot(1040, 372, 40, (60, 60, 70, 255)); e.rect(200, 600, 1300, 620, (255, 214, 120, 255))
    for x in (340, 1160): e.dot(x, 820, 150, (60, 50, 50, 255)); e.ellipse(x, 820, 150, 150, outline=LINE, width=14); e.dot(x, 820, 110, (250, 230, 190, 255)); [e.stroke([(x, 820), (x + 105 * math.cos(math.radians(a)), 820 + 105 * math.sin(math.radians(a)))], (150, 90, 60, 255), 10) for a in range(0, 360, 30)]; e.dot(x, 820, 26, YEL)
    e.dot(1360, 620, 60, (255, 214, 90, 255)); e.ellipse(1360, 620, 60, 60, outline=LINE, width=10); shine(e, 230, 580, 140)
    eyes(e, 760, 690, 0.55, 'happy' if face != 'sad' else 'sad')
    base.alpha_composite(e.out()); return base


def sun(face='default'):                                     # giant scorching sun: rays, sweat drops, angry brows
    d = Draw(1200, 1200); c = 600
    for a in range(0, 360, 20): r0, r1 = 400, 560 + (40 if a % 40 else 0); d.poly([(c + r0 * math.cos(math.radians(a - 6)), c + r0 * math.sin(math.radians(a - 6))), (c + r1 * math.cos(math.radians(a)), c + r1 * math.sin(math.radians(a))), (c + r0 * math.cos(math.radians(a + 6)), c + r0 * math.sin(math.radians(a + 6)))], fill=ORNG, outline=LINE, width=8)
    d.dot(c, c, 400, (255, 200, 60, 255)); d.ellipse(c, c, 400, 400, outline=LINE, width=16); d.dot(c - 120, c - 140, 90, (255, 240, 170, 200))
    if face == 'angry':
        for sg in (-1, 1): d.stroke([(c + sg * 60, c - 110), (c + sg * 210, c - 170)], LINE, 22)
    eyes(d, c, c, 1.4, 'shocked' if face == 'angry' else 'happy'); G.sweat(d, c + 330, c - 160); return d.out()


def thermo():                                                # thermometer bursting to 90 degrees
    d = Draw(420, 1300); d.rrect(130, 60, 290, 1060, 80, fill=WT, outline=LINE, width=16); d.rrect(170, 200, 250, 1080, 40, fill=RED); d.dot(210, 1130, 140, RED); d.ellipse(210, 1130, 140, 140, outline=LINE, width=16)
    for y in range(160, 1000, 80): d.stroke([(290, y), (340, y)], LINE, 8)
    d.text(210, 110, '90', 90, RED, stroke=6, stroke_fill=LINE); shine(d, 150, 260, 600); return d.out()


def barrel(face='default'):                                  # the one water barrel: wooden staves, tap, a single tin cup
    d = Draw(900, 1000); d.ellipse(450, 200, 300, 70, fill=(150, 200, 240, 255), outline=LINE, width=14); d.rrect(150, 200, 750, 900, 60, fill=(170, 110, 60, 255), outline=LINE, width=16)
    for y in (330, 760): d.rect(150, y, 750, y + 34, (90, 90, 100, 255))
    for x in range(230, 700, 90): d.stroke([(x, 240), (x, 880)], (140, 86, 46, 255), 8)
    d.rect(740, 600, 840, 640, (150, 150, 160, 255)); d.rrect(780, 700, 880, 800, 14, fill=(190, 190, 200, 255), outline=LINE, width=10); eyes(d, 450, 520, 0.8, face if face != 'default' else 'nervous'); return d.out()


def milepost(num):                                           # wooden mile post with a big painted number
    d = Draw(700, 1300); d.rect(300, 500, 400, 1290, (150, 100, 60, 255)); d.rrect(60, 80, 640, 560, 30, fill=(250, 236, 200, 255), outline=LINE, width=16)
    d.text(350, 250, 'MILE', 110, (120, 70, 40, 255)); d.text(350, 420, num, 200, RED, stroke=8, stroke_fill=LINE); return d.out()


def dog(face='default'):                                     # scruffy wild dog mid-chase: fluffy, big eyes, angry brows, tongue
    d = Draw(1200, 900); c = (170, 120, 80, 255)
    d.ellipse(560, 520, 360, 200, fill=c, outline=LINE, width=16)
    for x, a in ((300, -30), (420, 20), (700, -20), (820, 30)): d.stroke([(x, 640), (x + a * 3, 840)], LINE, 52); d.stroke([(x, 640), (x + a * 3, 840)], c, 34)
    d.poly([(200, 470), (40, 380), (120, 520)], fill=c, outline=LINE, width=12)
    d.dot(900, 380, 210, c); d.ellipse(900, 380, 210, 210, outline=LINE, width=16); d.ellipse(1040, 460, 110, 80, fill=(230, 200, 170, 255), outline=LINE, width=12); d.dot(1120, 430, 30, LINE)
    for sg in (-1, 1): d.poly([(900 + sg * 120, 230), (900 + sg * 200, 110), (900 + sg * 40, 190)], fill=dk(c, 0.8), outline=LINE, width=12)
    eyes(d, 900, 360, 0.75, 'shocked' if face == 'default' else face); d.stroke([(830, 280), (880, 300)], LINE, 14); d.stroke([(970, 300), (1020, 280)], LINE, 14)
    d.rrect(1050, 500, 1100, 600, 24, fill=PINK, outline=LINE, width=8); return d.out()


def apple(face='default'):                                   # rotten apple: brown spots, bite, a cute worm waving
    d = Draw(900, 900); d.dot(450, 500, 330, (150, 170, 60, 255)); d.ellipse(450, 500, 330, 330, outline=LINE, width=16)
    for x, y, r in ((300, 380, 70), (580, 640, 90), (620, 360, 50)): d.dot(x, y, r, (120, 90, 50, 255))
    d.dot(760, 560, 110, (0, 0, 0, 0)); d.stroke([(450, 180), (480, 60)], BRN, 22); d.ellipse(560, 110, 90, 40, fill=(90, 170, 70, 255), outline=LINE, width=10)
    d.ellipse(700, 330, 70, 40, fill=PINK, outline=LINE, width=10); d.dot(740, 300, 12, LINE); eyes(d, 420, 520, 0.9, 'happy' if face == 'default' else face); return d.out()


def bottle(kind='poison'):                                   # glossy bottles: green glowing poison (cute rat label), amber brandy, egg-white glass
    d = Draw(600, 1100)
    if kind == 'egg':
        d.poly([(140, 400), (460, 400), (420, 1040), (180, 1040)], fill=(230, 240, 250, 200), outline=LINE, width=14); d.poly([(160, 600), (440, 600), (420, 1020), (180, 1020)], fill=(250, 250, 236, 255))
        d.ellipse(300, 330, 110, 140, fill=(250, 246, 230, 255), outline=LINE, width=12); d.dot(300, 760, 70, (255, 200, 60, 255)); return d.out()
    col = LIME if kind == 'poison' else (190, 110, 40, 255)
    d.rrect(230, 60, 370, 360, 30, fill=dk(col, 0.8), outline=LINE, width=14); d.rect(220, 40, 380, 110, BRN); d.rrect(80, 330, 520, 1060, 110, fill=col, outline=LINE, width=16)
    d.rrect(130, 560, 470, 900, 30, fill=(250, 244, 220, 255), outline=LINE, width=10); shine(d, 120, 400, 520, 36)
    if kind == 'poison':                                     # cute rat face on the label
        d.dot(300, 740, 90, (170, 170, 186, 255)); [d.dot(300 + sg * 80, 660, 44, (200, 170, 186, 255)) for sg in (-1, 1)]; d.dot(300, 790, 14, PINK); eyes(d, 300, 730, 0.35, 'shocked')
    else: d.dot(300, 730, 80, (220, 150, 70, 255))
    return d.out()


def trio():                                                  # the trainers' recipe: egg-white glass, brandy, poison
    im = Image.new('RGBA', (1500, 1100), (0, 0, 0, 0))
    for k, kd in enumerate(('egg', 'brandy', 'poison')): im.alpha_composite(bottle(kd), (k * 450, 0))
    return im


def pack(face='default'):                                    # 8 tiny chibi runners (or collapsed ones for "runners drop")
    d = Draw(1600, 800); cols = [RED, (40, 80, 200, 255), YEL, (60, 170, 90, 255), PINK, ORNG, VIO, WT]; sk = [(246, 214, 190, 255), (218, 172, 134, 255), (176, 122, 90, 255)]
    for k in range(8):
        x = 110 + k * 190; y = 360 + (k % 2) * 60
        if face == 'drop':
            d.rrect(x - 80, y + 230, x + 90, y + 300, 30, fill=cols[k], outline=LINE, width=8); d.dot(x - 110, y + 250, 50, sk[k % 3]); d.ellipse(x - 110, y + 250, 50, 50, outline=LINE, width=8); d.stroke([(x - 130, y + 240), (x - 100, y + 260)], LINE, 6)
            continue
        d.stroke([(x - 20, y + 200), (x - 50, y + 330)], LINE, 18); d.stroke([(x + 20, y + 200), (x + 60, y + 320)], LINE, 18)
        d.rrect(x - 55, y + 60, x + 55, y + 210, 30, fill=cols[k], outline=LINE, width=8); d.rect(x - 28, y + 110, x + 28, y + 150, WT)
        d.dot(x, y, 70, sk[k % 3]); d.ellipse(x, y, 70, 70, outline=LINE, width=8); d.dot(x - 24, y - 4, 12, LINE); d.dot(x + 24, y - 4, 12, LINE); d.dot(x - 20, y - 8, 4, WT); d.dot(x + 28, y - 8, 4, WT)
    return d.out()


def ftape():                                                 # finish line: two striped posts and a red-white tape
    d = Draw(1800, 1000)
    for x in (100, 1700): d.rect(x - 30, 100, x + 30, 990, WT); [d.rect(x - 30, y, x + 30, y + 60, RED) for y in range(100, 990, 120)]; d.dot(x, 90, 44, YEL)
    for k in range(16): d.rect(130 + k * 98, 470, 130 + k * 98 + 98, 520, RED if k % 2 else WT)
    return d.out()


def watch():                                                 # big brass stopwatch reading 3:28
    d = Draw(900, 1000); d.rrect(400, 20, 500, 140, 20, fill=(220, 170, 60, 255), outline=LINE, width=12); d.dot(450, 560, 420, (220, 170, 60, 255)); d.ellipse(450, 560, 420, 420, outline=LINE, width=16)
    d.dot(450, 560, 350, WT); d.text(450, 560, '3:28', 220, LINE); d.stroke([(450, 560), (450, 260)], RED, 14); shine(d, 180, 380, 200, 30); return d.out()


def rulebook():                                              # thick old rulebook with gold corners and a ribbon
    d = Draw(1100, 900); d.rrect(80, 120, 1020, 840, 30, fill=(200, 56, 60, 255), outline=LINE, width=16); d.rect(100, 780, 1000, 830, (250, 240, 210, 255))
    for x, y in ((80, 120), (1020, 120)): d.dot(x, y, 50, (240, 190, 80, 255))
    d.rrect(300, 260, 800, 520, 20, outline=(240, 190, 80, 255), width=12); d.stroke([(840, 120), (840, 880)], RED, 26); eyes(d, 550, 390, 0.6, 'happy'); return d.out()


def scale():                                                 # balance: poison bottle with a green tick vs car with a red cross
    d = Draw(1600, 1100); d.rect(770, 300, 830, 1000, (200, 160, 70, 255)); d.rrect(600, 1000, 1000, 1060, 20, fill=(200, 160, 70, 255), outline=LINE, width=10)
    d.stroke([(200, 330), (1400, 270)], (200, 160, 70, 255), 30); d.dot(800, 300, 40, YEL)
    for x, y in ((200, 330), (1400, 270)): d.stroke([(x, y), (x - 150, y + 300)], LINE, 6); d.stroke([(x, y), (x + 150, y + 300)], LINE, 6); d.chord(x, y + 300, 190, 70, 0, 180, fill=(220, 180, 90, 255), outline=LINE, width=10)
    pb = bottle('poison').resize((180, 330)); cr = car('default').resize((420, 280)); im = d.out(); im.alpha_composite(pb, (110, 300)); im.alpha_composite(cr, (1190, 300))
    e = Draw(1600, 1100); e.stroke([(130, 180), (190, 250), (300, 100)], (60, 200, 90, 255), 40); e.stroke([(1310, 80), (1500, 250)], RED, 40); e.stroke([(1500, 80), (1310, 250)], RED, 40); im.alpha_composite(e.out()); return im


def dust():                                                  # dust cloud puff
    d = Draw(1000, 600)
    for x, y, r in ((200, 380, 160), (420, 300, 200), (680, 360, 180), (850, 420, 120)): d.dot(x, y, r, (230, 200, 150, 200))
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def bunting(d, y, n=18):
    for k in range(n): x = k * W2 / n; d.poly([(x, y), (x + W2 / n, y), (x + W2 / n / 2, y + 70)], fill=(RED, WT, (40, 80, 200, 255), YEL)[k % 4], outline=LINE, width=4)


def finish(path):                                            # stadium finish: turquoise sky, terracotta stands with a colourful crowd, bunting, flags
    im = sky((60, 190, 210), (190, 240, 236), 1.0); d = Draw(W2, H2); r = np.random.RandomState(4)
    d.poly([(0, 560), (W2, 560), (W2, 900), (0, 900)], fill=(200, 110, 70, 255)); [d.rect(0, y, W2, y + 10, (170, 86, 56, 255)) for y in range(600, 900, 60)]
    for _ in range(420): d.dot(r.randint(0, W2), r.randint(580, 880), 14, [(250, 220, 90, 255), WT, RED, (60, 120, 220, 255), PINK][r.randint(0, 5)])
    for x in range(100, W2, 300): d.stroke([(x, 560), (x, 300)], LINE, 8); d.poly([(x, 300), (x + 100, 330), (x, 360)], fill=(RED, YEL, (40, 80, 200, 255))[x // 300 % 3], outline=LINE, width=4)
    bunting(d, 540); fl(d, (200, 120, 80, 255)); im.alpha_composite(d.out()); glow(im, 1900, 160, 500, (255, 250, 200, 90), 100); im.convert('RGB').save(path)


def fair(path):                                              # 1904 World's Fair: ivory palace with a big dome, cascades, turquoise lagoon
    im = sky((80, 200, 220), (210, 244, 240), 1.0); d = Draw(W2, H2)
    d.rect(500, 380, 1900, 820, (250, 240, 220, 255)); d.chord(1200, 380, 280, 260, 180, 360, fill=(230, 200, 140, 255), outline=LINE, width=12); d.dot(1200, 110, 30, YEL)
    for x in range(560, 1880, 110): d.rect(x, 460, x + 50, 800, (236, 220, 196, 255))
    for x in (300, 2100): d.rect(x - 120, 500, x + 120, 820, (250, 236, 214, 255)); d.chord(x, 500, 120, 120, 180, 360, fill=(200, 160, 110, 255), outline=LINE, width=8)
    d.rect(0, 820, W2, 940, (60, 190, 210, 255)); [d.stroke([(x, 860), (x + 80, 860)], WT, 6) for x in range(40, W2, 200)]
    fl(d, (230, 210, 180, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 700, (255, 250, 220, 80), 100); im.convert('RGB').save(path)


def road(path):                                              # start road: mustard prairie, fence, dust clouds, heat shimmer
    im = sky((90, 200, 220), (250, 230, 170), 1.0); d = Draw(W2, H2); hills(d, 760, (220, 180, 80, 255), 60, 2); hills(d, 840, (200, 150, 60, 255), 40, 3, 1.0)
    for x in range(0, W2, 140): d.rect(x, 780, x + 16, 900, (150, 100, 60, 255))
    d.rect(0, 810, W2, 822, (150, 100, 60, 255)); [d.stroke([(x, 400 + (x % 3) * 30), (x + 200, 380 + (x % 3) * 30)], (255, 250, 230, 120), 6) for x in range(0, W2, 320)]
    for x, y, r in ((300, 820, 120), (2000, 830, 140)): d.dot(x, y, r, (240, 210, 160, 180))
    fl(d, (210, 170, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def heat(path):                                              # heat: blazing orange-red sky, white-hot glow, cracked earth, heat waves
    im = sky((240, 90, 50), (255, 200, 90), 1.0); d = Draw(W2, H2); hills(d, 800, (200, 90, 50, 255), 50, 2)
    for y in range(300, 760, 90): d.stroke([(x, y + 20 * math.sin(x / 60)) for x in range(0, W2, 40)], (255, 240, 200, 90), 8)
    fl(d, (220, 140, 80, 255)); [d.stroke([(x, 960), (x + 60, 1040), (x + 20, 1100)], (170, 90, 50, 255), 6) for x in range(80, W2, 260)]
    im.alpha_composite(d.out()); glow(im, 1200, 300, 900, (255, 250, 210, 110), 150); im.convert('RGB').save(path)


def office(path):                                            # Sullivan's office: plum wallpaper with gold stripes, tall window, map frame, brass lamp
    im = sky((120, 60, 110), (170, 100, 150), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 12, 940, (210, 160, 90, 255))
    d.rect(900, 140, 1500, 640, (150, 220, 240, 255)); d.stroke([(1200, 140), (1200, 640)], WT, 16); d.stroke([(900, 390), (1500, 390)], WT, 16); d.rrect(890, 130, 1510, 650, 8, outline=(110, 70, 50, 255), width=24)
    d.rrect(1700, 200, 2200, 560, 10, fill=(240, 220, 170, 255), outline=(200, 160, 80, 255), width=20); d.stroke([(1760, 480), (1880, 300), (2000, 420), (2140, 260)], RED, 10)
    d.rect(0, 700, W2, 940, (90, 50, 80, 255)); fl(d, (110, 70, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 390, 500, (255, 250, 230, 90), 80); im.convert('RGB').save(path)


def waterstop(path):                                         # mile 12: lonely peach-orange roadside, one striped tent, dry grass, buzzards
    im = sky((250, 150, 90), (255, 220, 170), 1.0); d = Draw(W2, H2); hills(d, 820, (220, 170, 100, 255), 50, 2, 2.0)
    d.poly([(1500, 860), (1700, 620), (1900, 860)], fill=WT, outline=LINE, width=10); [d.poly([(1500 + k * 80, 860), (1700, 620), (1540 + k * 80, 860)], fill=RED) for k in range(0, 5, 2)]
    for x, y in ((600, 220), (800, 280)): d.stroke([(x - 50, y), (x, y + 20), (x + 50, y)], LINE, 8)
    for x in range(0, W2, 60): d.stroke([(x, 940), (x + 10, 900)], (200, 160, 80, 255), 6)
    fl(d, (220, 170, 110, 255)); im.alpha_composite(d.out()); glow(im, 400, 200, 400, (255, 250, 210, 120), 80); im.convert('RGB').save(path)


def corn(path):                                              # cornfield chase: lime corn rows, red farmhouse, windmill, sunny sky
    im = sky((110, 200, 240), (220, 246, 220), 1.0); d = Draw(W2, H2); hills(d, 700, (140, 200, 90, 255), 50, 2)
    d.rect(1700, 520, 2000, 720, (200, 60, 60, 255)); d.poly([(1680, 520), (1850, 400), (2020, 520)], fill=(120, 40, 40, 255), outline=LINE, width=8)
    d.stroke([(500, 720), (500, 360)], LINE, 10); [d.stroke([(500, 360), (500 + 160 * math.cos(math.radians(a)), 360 + 160 * math.sin(math.radians(a)))], (230, 230, 240, 255), 26) for a in (20, 110, 200, 290)]
    for x in range(0, W2, 70): d.stroke([(x, 940), (x + 10, 700)], (120, 180, 60, 255), 16); d.ellipse(x + 10, 760, 14, 36, fill=YEL)
    fl(d, (190, 160, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def orchard(path):                                           # orchard: emerald apple trees, mint sky, picket fence, ladder
    im = sky((150, 220, 200), (230, 250, 220), 1.0); d = Draw(W2, H2); hills(d, 760, (90, 170, 90, 255), 40, 3)
    for k, x in enumerate(range(150, W2, 330)): ptree(d, x, 900, 2.0 + 0.3 * (k % 2), (60, 150, 70, 255), fruit=(230, 50, 60, 255))
    for x in range(0, W2, 90): d.rect(x, 860, x + 30, 940, WT)
    fl(d, (120, 170, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def carroad(path):                                           # country road at late afternoon: violet-blue sky, telegraph poles, rolling hills
    im = sky((120, 110, 210), (255, 200, 170), 1.0); d = Draw(W2, H2); hills(d, 720, (110, 150, 120, 255), 90, 2); hills(d, 820, (150, 180, 110, 255), 60, 3, 1.5)
    for x in range(100, W2, 400): d.stroke([(x, 860), (x, 420)], LINE, 10); d.stroke([(x - 60, 450), (x + 60, 450)], LINE, 8)
    d.stroke([(x, 455) for x in range(100, W2, 40)], (60, 50, 70, 255), 4); fl(d, (200, 170, 130, 255)); im.alpha_composite(d.out()); glow(im, 2000, 640, 400, (255, 220, 180, 100), 80); im.convert('RGB').save(path)


def judges(path):                                            # judges' tent: red-white striped canvas, lanterns, flags, a desk banner shape
    im = sky((220, 60, 70), (250, 200, 190), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 200): d.rect(x, 0, x + 100, 940, (250, 244, 236, 255))
    for x in (500, 1200, 1900): d.stroke([(x, 0), (x, 120)], LINE, 6); d.dot(x, 160, 50, (255, 220, 120, 255)); d.ellipse(x, 160, 50, 50, outline=LINE, width=8)
    bunting(d, 260, 14); d.rect(0, 720, W2, 940, (150, 40, 50, 255)); fl(d, (170, 120, 90, 255)); im.alpha_composite(d.out()); [glow(im, x, 160, 160, (255, 230, 150, 100), 40) for x in (500, 1200, 1900)]; im.convert('RGB').save(path)


def aid(path):                                               # trainers' aid station: sickly chartreuse gloom, bottle shelves, lantern glow
    im = sky((120, 150, 50), (200, 220, 110), 1.0); d = Draw(W2, H2)
    for y in (300, 560): d.rect(0, y, W2, y + 24, (110, 80, 50, 255))
    r = np.random.RandomState(2)
    for y in (300, 560):
        for x in range(60, W2, 110): h = 90 + r.randint(0, 80); d.rrect(x, y - h, x + 60, y, 14, fill=[(182, 255, 60, 230), (190, 110, 40, 230), (240, 240, 230, 230)][r.randint(0, 3)], outline=LINE, width=5)
    d.dot(1200, 160, 60, (255, 240, 150, 255)); fl(d, (120, 120, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 160, 500, (220, 255, 120, 90), 100); im.convert('RGB').save(path)


def archive(path):                                           # rules archive at dusk: violet bookshelves, round window with stars, lamp glow
    im = sky((80, 60, 150), (150, 110, 200), 1.0); d = Draw(W2, H2); r = np.random.RandomState(7)
    for x0 in (0, 1600):
        for y in range(120, 900, 160):
            d.rect(x0, y + 130, x0 + 800, y + 150, (90, 60, 50, 255)); xx = x0 + 20
            while xx < x0 + 780: w = 30 + r.randint(0, 30); d.rect(xx, y + 130 - 90 - r.randint(0, 30), xx + w, y + 130, [(220, 90, 90, 255), (90, 160, 220, 255), (240, 200, 90, 255), (120, 200, 140, 255)][r.randint(0, 4)]); xx += w + 6
    d.dot(1200, 360, 230, (40, 40, 110, 255)); d.ellipse(1200, 360, 230, 230, outline=(240, 190, 80, 255), width=24); stars(d, 0, 10)
    for k in range(30): d.dot(1200 + r.randint(-180, 180), 360 + r.randint(-180, 180), 5, WT)
    fl(d, (90, 70, 120, 255)); im.alpha_composite(d.out()); glow(im, 1200, 360, 400, (200, 180, 255, 80), 80); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast(('lorz', 'hicks', 'felix', 'tau', 'sullivan', 'trainer', 'judge'))
    multi = dict(car={'default': car(), 'mystery': car('mystery'), 'lorz': car('lorz')}, sun={'default': sun(), 'angry': sun('angry')}, thermo={'default': thermo()},
                 barrel={'default': barrel()}, mile12={'default': milepost('12')}, mile9={'default': milepost('9')}, dog={'default': dog()}, apple={'default': apple(), 'sad': apple('sad')},
                 poison={'default': bottle('poison')}, trio={'default': trio()}, pack={'default': pack(), 'drop': pack('drop')}, ftape={'default': ftape()}, watch={'default': watch()},
                 rulebook={'default': rulebook()}, scale={'default': scale()}, dust={'default': dust()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    GRN = (60, 150, 60, 255)
    cards = dict(hookc=M.bigneon('WINNER RAN ON', 'RAT POISON!', 1000, LIME, YEL),
                 carc=stamp('HE RODE IN A CAR?!', 960, RED, 120, -4),
                 ratc=stamp('RAT POISON!', 820, GRN, 150, 3),
                 legal=P_('AND IT WAS', 'LEGAL!', (60, 120, 60, 255), 900, 140, 190, LIME),
                 stl=P_('ST. LOUIS', 'OLYMPICS', (40, 140, 170, 255), 900, 160, 140, WT),
                 y1904=M.cal('AUGUST 30', '1904', (200, 90, 60, 255)),
                 r32=P_('32 RUNNERS', 'START!', (200, 110, 60, 255), 960, 150, 150, YEL),
                 heatc=M.bigneon('90 DEGREE', 'HEAT!', 900, ORNG, YEL),
                 dirt=stamp('DIRT ROADS!', 820, BRN, 150, -3),
                 sully=P_('JAMES', 'SULLIVAN', (44, 54, 100, 255), 900, 150, 190, (240, 180, 60, 255)),
                 idea=stamp('AN IDEA...', 700, VIO, 150, 4),
                 onestop=P_('JUST ONE', 'WATER STOP', (40, 120, 190, 255), 940, 140, 160, CYAN),
                 dehyd=M.bigneon('STUDY', 'DEHYDRATION', 1000, CYAN, ORNG),
                 purpose=stamp('ON PURPOSE!', 860, RED, 150, -4),
                 drop=stamp('RUNNERS DROP!', 900, (200, 90, 50, 255), 140, 3),
                 dogc=P_('A WILD DOG!', 'CHASE!', (150, 100, 60, 255), 900, 150, 150, YEL),
                 offc=P_('ONE MILE', 'OFF COURSE', (110, 150, 60, 255), 920, 150, 150, WT),
                 felixc=P_('FELIX', 'CARVAJAL', (30, 140, 80, 255), 900, 150, 180, YEL),
                 apples=stamp('ROTTEN APPLES!', 940, (120, 90, 40, 255), 130, -3),
                 nap=stamp('TAKES A NAP!', 860, VIO, 140, 3),
                 fourth=M.bigneon('STILL', '4TH!', 760, LIME, YEL),
                 lorzc=P_('FRED LORZ', 'CROSSES FIRST', (40, 80, 200, 255), 960, 150, 130, YEL),
                 quit=P_('QUIT AT', 'MILE 9', (150, 60, 160, 255), 860, 150, 190, WT),
                 ride=stamp('HITCHED A RIDE!', 940, RED, 130, -3),
                 ten=M.bigneon('ABOUT', '10 MILES!', 880, PINK, YEL),
                 incar=stamp('IN A CAR!', 760, RED, 150, 4),
                 dq=stamp('DISQUALIFIED!', 960, RED, 150, -5),
                 hicksc=P_('THOMAS HICKS', 'REAL WINNER', (200, 50, 60, 255), 1000, 130, 150, YEL),
                 recipe=P_('EGG WHITES', '+ BRANDY', (190, 110, 40, 255), 900, 150, 150, WT),
                 strych=M.bigneon('STRYCHNINE', '= RAT POISON', 1000, LIME, PINK),
                 barely=stamp('BARELY STANDING!', 980, (200, 90, 50, 255), 120, 3),
                 t328=M.bigneon('3 HOURS', '28 MINUTES', 960, YEL, ORNG),
                 slowest=P_('SLOWEST WIN', 'IN OLYMPIC HISTORY', (90, 60, 150, 255), 1000, 140, 100, YEL),
                 norule=stamp('NO RULE BROKEN!', 960, (60, 120, 60, 255), 130, -3),
                 dopingc=stamp("DOPING WASN'T BANNED", 1000, (90, 60, 150, 255), 110, -3),
                 y1908=M.cal('BANNED IN', '1908', (90, 60, 150, 255)),
                 fine=stamp('THE POISON WAS FINE', 1000, (60, 150, 60, 255), 110, 3),
                 carnot=stamp('THE CAR WAS NOT!', 960, RED, 130, -4),
                 cheater=M.bigneon('THE ONLY', 'CHEATER!', 860, PINK, LIME))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (200, 120, 80), (186, 106, 70))
    M.sandtex(T('claytrack.jpg'), (206, 112, 74), (184, 96, 62)); CE.tiles(T('pavefair.jpg'), (236, 220, 196), (220, 204, 180)); M.sandtex(T('dirt.jpg'), (214, 176, 116), (190, 150, 96), seed=6)
    M.sandtex(T('cracked.jpg'), (226, 146, 86), (200, 120, 70), seed=8); CE.tiles(T('carpetplum.jpg'), (130, 70, 100), (116, 60, 90)); M.sandtex(T('dirt2.jpg'), (226, 180, 120), (204, 156, 100), seed=9)
    M.sandtex(T('dirt3.jpg'), (196, 166, 106), (176, 146, 90), seed=3); M.sandtex(T('grass.jpg'), (120, 180, 90), (100, 160, 76)); M.sandtex(T('roadtex.jpg'), (206, 176, 136), (186, 156, 120), seed=2)
    CE.tiles(T('boards.jpg'), (180, 130, 90), (164, 116, 80)); CE.tiles(T('aidfloor.jpg'), (140, 140, 70), (124, 124, 60)); CE.tiles(T('library.jpg'), (110, 86, 140), (96, 74, 124))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(finish=finish, fair=fair, road=road, heat=heat, office=office, waterstop=waterstop, corn=corn, orchard=orchard, carroad=carroad, judges=judges, aid=aid, archive=archive)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
