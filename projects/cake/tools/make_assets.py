#!/usr/bin/env python3
"""Assets for video 22: the bear Roosevelt refused to shoot became every kid's teddy bear (a cartoon of a cartoon).
Honey-caramel + bayou-moss world: misty gold-green bayou, amber hunt camp, moss forest, ink-blue newsroom, cream ink cartoon world,
pink-mint Brooklyn candy shop, dusk brick street, sky-blue White House, red-yellow toy factory, snowy Black Forest workshop,
rainbow 1907 craze, violet stained-glass church, indigo starry kid's bedroom.
Cute cast: Teddy Roosevelt (campaign hat), Holt Collier (slouch hat, white beard), Berryman, Morris + Rose Michtom, a priest, two kids, a buyer.
usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import lordgta_assets as LA
import mco_assets as M
import mono_assets as MA
from hx_assets import *

ROOT = B.ROOT
FUR, MUZ = (66, 60, 70, 255), (150, 110, 80, 255)


def realbear(face='default'):                                # the real bear: old, heavy, black, tired but cute; tied with a rope
    d = Draw(1200, 1100); d.ellipse(600, 720, 420, 330, fill=FUR, outline=LINE, width=16)
    for x in (330, 870): d.rrect(x - 80, 880, x + 80, 1080, 60, fill=FUR, outline=LINE, width=14)
    d.dot(600, 380, 260, FUR); d.ellipse(600, 380, 260, 260, outline=LINE, width=16)
    for sg in (-1, 1): d.dot(600 + sg * 200, 170, 80, FUR); d.ellipse(600 + sg * 200, 170, 80, 80, outline=LINE, width=14); d.dot(600 + sg * 200, 170, 40, MUZ)
    d.ellipse(600, 470, 120, 90, fill=MUZ, outline=LINE, width=12); d.ellipse(600, 430, 40, 28, fill=LINE)
    for x, y in ((470, 250), (720, 230)): d.stroke([(x, y), (x + 30, y - 20)], (170, 170, 180, 255), 8)
    eyes(d, 600, 360, 0.9, 'sad' if face in ('default', 'tied', 'sad') else face)
    if face == 'tied':
        for y in (650, 760): d.stroke([(170, y - 40), (1030, y + 40)], (210, 170, 100, 255), 26); d.stroke([(170, y - 40), (1030, y + 40)], LINE, 6)
    return d.out()


def willow():                                                # weeping willow: trunk + drooping green fronds
    d = Draw(1200, 1600); d.poly([(520, 1600), (560, 600), (640, 600), (700, 1600)], fill=(120, 86, 56, 255), outline=LINE, width=14); d.dot(600, 520, 420, (110, 160, 80, 255))
    for k in range(22): x = 220 + k * 36; d.stroke([(x, 400 + (k % 4) * 30), (x - 20 + (k % 3) * 20, 1050 + (k % 5) * 50)], (90, 150, 70, 255), 22)
    d.ellipse(600, 520, 420, 420, outline=LINE, width=12); return d.out()


def hounds():                                                # two eager hounds barking: floppy ears, wagging tails
    d = Draw(1600, 900)
    for x0, c in ((380, (210, 160, 110, 255)), (1180, (240, 220, 200, 255))):
        d.ellipse(x0, 600, 280, 160, fill=c, outline=LINE, width=14)
        for dx in (-180, -80, 100, 200): d.stroke([(x0 + dx, 700), (x0 + dx, 860)], LINE, 44); d.stroke([(x0 + dx, 700), (x0 + dx, 860)], c, 28)
        d.stroke([(x0 - 260, 560), (x0 - 360, 420)], LINE, 30); d.stroke([(x0 - 260, 560), (x0 - 360, 420)], c, 16)
        d.dot(x0 + 230, 380, 170, c); d.ellipse(x0 + 230, 380, 170, 170, outline=LINE, width=14); d.ellipse(x0 + 340, 440, 90, 66, fill=dk(c, 0.9), outline=LINE, width=10); d.dot(x0 + 410, 420, 26, LINE)
        d.ellipse(x0 + 150, 430, 60, 140, fill=(140, 90, 60, 255), outline=LINE, width=10); eyes(d, x0 + 240, 360, 0.6, 'happy')
    return d.out()


def plush(face='default', col=(214, 150, 80, 255)):          # Rose's teddy: honey plush, round ears, muzzle, red bow, shiny eyes
    d = Draw(1000, 1200); m2 = (250, 220, 170, 255)
    d.ellipse(500, 860, 300, 300, fill=col, outline=LINE, width=16); d.ellipse(500, 880, 170, 190, fill=m2)
    for sg in (-1, 1): d.ellipse(500 + sg * 300, 780, 90, 140, fill=col, outline=LINE, width=14); d.ellipse(500 + sg * 180, 1110, 110, 80, fill=col, outline=LINE, width=14)
    d.dot(500, 420, 270, col); d.ellipse(500, 420, 270, 270, outline=LINE, width=16)
    for sg in (-1, 1): d.dot(500 + sg * 210, 200, 90, col); d.ellipse(500 + sg * 210, 200, 90, 90, outline=LINE, width=14); d.dot(500 + sg * 210, 200, 48, m2)
    d.ellipse(500, 500, 120, 90, fill=m2, outline=LINE, width=10); d.ellipse(500, 470, 40, 28, fill=LINE)
    if face == 'steiff': d.dot(500 - 210, 200, 30, (250, 210, 60, 255)); d.rrect(270, 230, 330, 300, 8, fill=(250, 210, 60, 255), outline=LINE, width=6)
    else: d.poly([(500, 690), (380, 630), (380, 750)], fill=RED, outline=LINE, width=8); d.poly([(500, 690), (620, 630), (620, 750)], fill=RED, outline=LINE, width=8); d.dot(500, 690, 30, RED)
    eyes(d, 500, 400, 0.9, 'happy'); shine(d, 300, 280, 200, 30); return d.out()


def qbear():                                                 # open loop: a glowing silhouette of a little bear with a "?"
    d = Draw(800, 1000); c = (40, 50, 80, 235)
    d.ellipse(400, 720, 240, 240, fill=c); d.dot(400, 360, 220, c)
    for sg in (-1, 1): d.dot(400 + sg * 170, 180, 80, c); d.ellipse(400 + sg * 240, 640, 70, 120, fill=c)
    d.text(400, 400, '?', 260, (255, 200, 80, 255), stroke=10, stroke_fill=LINE); return d.out()


def cartoon(stage=1):                                        # Berryman-style ink cartoon on cream paper: the president turning away, the bear (smaller + cuter each stage)
    d = Draw(1400, 1100); d.rrect(30, 30, 1370, 1070, 20, fill=(250, 244, 226, 255), outline=LINE, width=18); ink = (40, 34, 40, 255)
    d.dot(420, 380, 120, (250, 244, 226, 255)); d.ellipse(420, 380, 120, 120, outline=ink, width=10); d.stroke([(370, 400), (470, 400)], ink, 12)
    d.ellipse(380, 370, 26, 26, outline=ink, width=6); d.ellipse(460, 370, 26, 26, outline=ink, width=6); d.ellipse(420, 270, 170, 30, outline=ink, width=10)
    d.rrect(320, 500, 520, 860, 60, outline=ink, width=10); d.stroke([(500, 560), (700, 460)], ink, 14); d.stroke([(700, 460), (720, 400)], ink, 10)
    d.stroke([(360, 860), (340, 1000)], ink, 12); d.stroke([(480, 860), (500, 1000)], ink, 12)
    s = (1.0, 0.72, 0.5)[stage - 1]; bx, by = 1050, 1000 - 380 * s
    d.ellipse(bx, by + 200 * s, 230 * s, 190 * s, outline=ink, width=10); d.dot(bx, by - 60 * s, 160 * s, (250, 244, 226, 255)); d.ellipse(bx, by - 60 * s, 160 * s, 160 * s, outline=ink, width=10)
    for sg in (-1, 1): d.ellipse(bx + sg * 120 * s, by - 190 * s, 50 * s, 50 * s, outline=ink, width=8)
    if stage == 1:
        for k in range(10): a = math.radians(k * 36); d.stroke([(bx + 160 * s * math.cos(a), by - 60 * s + 160 * s * math.sin(a)), (bx + 190 * s * math.cos(a), by - 60 * s + 190 * s * math.sin(a))], ink, 6)
        d.stroke([(bx - 260, by + 160), (bx + 230, by + 230)], ink, 8)
    eyes(d, bx, by - 60 * s, 0.5 * s + 0.1, ('sad', 'happy', 'happy')[stage - 1])
    if stage == 3: d.dot(bx - 80 * s, by - 20 * s, 18, (255, 150, 170, 255)); d.dot(bx + 80 * s, by - 20 * s, 18, (255, 150, 170, 255))
    return d.out()


def inkpen():                                                # big dip pen + ink pot with a face
    d = Draw(800, 1100); d.rrect(150, 640, 650, 1060, 60, fill=(40, 50, 90, 255), outline=LINE, width=16); d.rect(260, 560, 540, 660, (40, 50, 90, 255)); d.ellipse(400, 560, 140, 30, fill=LINE)
    d.stroke([(420, 600), (640, 60)], (150, 100, 60, 255), 34); d.poly([(400, 640), (430, 560), (460, 620)], fill=(200, 200, 210, 255), outline=LINE, width=6)
    eyes(d, 400, 860, 0.8, 'happy'); shine(d, 190, 690, 260, 30); return d.out()


def window(sign=True):                                       # candy-shop window: striped awning, the plush bear inside, the sign
    d = Draw(1400, 1300); d.rrect(60, 200, 1340, 1240, 20, fill=(90, 60, 70, 255), outline=LINE, width=18); d.rect(120, 300, 1280, 1180, (255, 236, 200, 255))
    for k in range(10): d.rect(60 + k * 128, 120, 60 + k * 128 + 64, 260, PINK); d.rect(60 + k * 128 + 64, 120, 60 + k * 128 + 128, 260, WT)
    for x in (200, 1200): d.rrect(x - 60, 860, x + 60, 1160, 20, fill=(200, 240, 230, 200), outline=LINE, width=8); [d.dot(x - 30 + j * 30, 900 + (j % 2) * 60, 18, (RED, YEL, (90, 200, 120, 255))[j]) for j in range(3)]
    im = d.out(); im.alpha_composite(plush().resize((520, 624)), (440, 330))
    if sign: e = Draw(1400, 1300); e.rrect(380, 950, 1020, 1130, 16, fill=WT, outline=LINE, width=10); e.text(700, 1040, "TEDDY'S BEAR", 74, (180, 40, 60, 255)); im.alpha_composite(e.out())
    return im


def letter():                                                # the president's reply: envelope, wax seal, a big YES
    d = Draw(1100, 800); d.rrect(40, 60, 1060, 760, 20, fill=(250, 246, 236, 255), outline=LINE, width=16); d.poly([(40, 60), (550, 420), (1060, 60)], fill=(236, 230, 214, 255), outline=LINE, width=12)
    d.dot(550, 420, 70, RED); d.text(550, 620, 'YES!', 180, (40, 150, 80, 255), stroke=8, stroke_fill=LINE); return d.out()


def crate():                                                 # crate of bears stencilled 3000
    d = Draw(1300, 1000); r = np.random.RandomState(3)
    for k in range(9): x = 150 + k * 125; d.dot(x, 330 - (k % 2) * 30, 90, (214, 150, 80, 255) if k % 3 else (200, 196, 190, 255)); d.ellipse(x, 330 - (k % 2) * 30, 90, 90, outline=LINE, width=8); d.dot(x - 30, 320, 10, LINE); d.dot(x + 30, 320, 10, LINE)
    d.rrect(60, 380, 1240, 980, 20, fill=(200, 150, 90, 255), outline=LINE, width=16)
    for y in (520, 700, 860): d.stroke([(60, y), (1240, y)], (160, 110, 60, 255), 10)
    d.text(650, 680, '3000', 260, (90, 50, 30, 255)); return d.out()


def pillow():                                                # cosy pillow with the teddy tucked in (the payoff)
    d = Draw(1400, 1000); d.rrect(60, 500, 1340, 960, 160, fill=(240, 236, 255, 255), outline=LINE, width=16); [d.dot(200 + k * 160, 700, 20, (200, 190, 240, 255)) for k in range(7)]
    im = d.out(); im.alpha_composite(plush().resize((560, 672)), (420, 160)); return im


def boxes():                                                 # toy-company boxes, each with a bear face, stacked
    d = Draw(1300, 1100)
    for k, (x, y) in enumerate(((150, 700), (550, 700), (950, 700), (350, 320), (750, 320))):
        d.rrect(x, y, x + 360, y + 360, 20, fill=(RED, YEL, (60, 140, 220, 255), PINK, (90, 200, 120, 255))[k], outline=LINE, width=12); d.dot(x + 180, y + 180, 90, (214, 150, 80, 255))
        d.ellipse(x + 180, y + 180, 90, 90, outline=LINE, width=8); d.dot(x + 150, y + 170, 10, LINE); d.dot(x + 210, y + 170, 10, LINE)
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def bayou(path):                                             # hook bayou: misty gold-green dawn, cypress knees, moss curtains, still water
    im = sky((150, 180, 110), (250, 220, 150), 1.0); d = Draw(W2, H2); d.dot(1700, 420, 140, (255, 236, 180, 255))
    for x in range(100, W2, 380): d.rect(x, 200, x + 60, 820, (90, 80, 60, 255)); [d.stroke([(x - 60 + j * 40, 220), (x - 70 + j * 40, 520 + j * 30)], (130, 160, 100, 220), 14) for j in range(5)]
    d.rect(0, 780, W2, 940, (110, 140, 100, 255)); [d.stroke([(x, 820), (x + 120, 820)], (200, 230, 180, 200), 6) for x in range(40, W2, 300)]
    fl(d, (120, 120, 80, 255)); im.alpha_composite(d.out()); glow(im, 1700, 420, 500, (255, 240, 190, 120), 120); im.convert('RGB').save(path)


def camp(path):                                              # hunt camp: amber sky, canvas tents, campfire smoke, pines
    im = sky((240, 150, 80), (255, 220, 160), 1.0); d = Draw(W2, H2); hills(d, 760, (120, 120, 70, 255), 60, 3)
    for x in (300, 900, 1800): d.poly([(x, 880), (x + 200, 600), (x + 400, 880)], fill=(240, 226, 196, 255), outline=LINE, width=10); d.poly([(x + 170, 880), (x + 200, 700), (x + 230, 880)], fill=(90, 70, 50, 255))
    for x in range(0, W2, 260): d.poly([(x, 760), (x + 80, 480), (x + 160, 760)], fill=(60, 100, 70, 255))
    d.dot(1400, 700, 50, (230, 220, 210, 160)); d.dot(1430, 600, 70, (230, 220, 210, 120)); fl(d, (150, 120, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def forest(path):                                            # hound chase forest: deep moss green, sun shafts, ferns
    im = sky((60, 120, 80), (160, 200, 130), 1.0); d = Draw(W2, H2)
    for x in range(60, W2, 230): d.rect(x, 0, x + 70, 900, (80, 60, 50, 255))
    for x in range(0, W2, 120): d.poly([(x, 940), (x + 60, 780), (x + 120, 940)], fill=(70, 140, 70, 255))
    for x in (500, 1300, 2000): d.poly([(x, 0), (x + 160, 0), (x + 360, 900), (x + 160, 900)], fill=(255, 250, 200, 50))
    fl(d, (90, 110, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def newsroom(path):                                          # Washington Post 1902 newsroom: ink-blue walls, cream drafting light, hanging proofs, clock
    im = sky((50, 70, 130), (100, 120, 180), 1.0); d = Draw(W2, H2)
    d.stroke([(0, 180), (W2, 180)], LINE, 4)
    for x in range(80, W2, 260): d.rect(x, 190, x + 160, 420, (250, 244, 226, 255)); d.rect(x + 20, 230, x + 140, 250, (120, 120, 130, 255)); d.rect(x + 20, 280, x + 100, 380, (190, 186, 176, 255))
    d.rect(950, 480, 1450, 820, (200, 230, 255, 255)); d.dot(2000, 560, 90, WT); d.ellipse(2000, 560, 90, 90, outline=LINE, width=10)
    fl(d, (70, 80, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 650, 500, (255, 250, 220, 80), 90); im.convert('RGB').save(path)


def inkworld(path):                                          # inside the cartoon: cream paper world drawn in ink, crosshatch hills, ink clouds
    im = sky((236, 226, 196), (250, 244, 226), 1.0); d = Draw(W2, H2); ink = (60, 50, 60, 255)
    for x in range(0, W2, 300): d.arc(x + 150, 760, 260, 140, 180, 360, ink, 8)
    for x in range(0, W2, 40): d.stroke([(x, 940), (x + 60, 860)], (120, 110, 110, 255), 4)
    for x, y in ((400, 200), (1300, 140), (2000, 240)): d.arc(x, y, 160, 60, 180, 360, ink, 8)
    fl(d, (220, 206, 176, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def candy(path):                                             # Brooklyn candy shop: pink-mint stripes, jar shelves, gingham counter
    im = sky((250, 170, 200), (200, 250, 230), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 160): d.rect(x, 0, x + 80, 940, (255, 220, 236, 255))
    for y in (260, 520):
        d.rect(0, y, W2, y + 20, (150, 100, 70, 255))
        for x in range(60, W2, 150): d.rrect(x, y - 150, x + 100, y, 20, fill=(220, 250, 240, 220), outline=LINE, width=6); [d.dot(x + 25 + j * 25, y - 50 - (j % 2) * 40, 16, (RED, YEL, (90, 200, 120, 255), (120, 120, 240, 255))[j]) for j in range(4)]
    d.rect(0, 700, W2, 940, (230, 90, 110, 255)); [d.rect(x, 700, x + 60, 940, (250, 140, 160, 255)) for x in range(0, W2, 120)]
    fl(d, (170, 110, 120, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def street(path):                                            # Brooklyn street at dusk: brick fronts, gas lamps, purple-orange sky
    im = sky((120, 80, 160), (255, 170, 120), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 500): d.rect(x, 140, x + 470, 900, (170, 80, 70, 255)); [d.rect(x + 40 + c * 140, y, x + 140 + c * 140, y + 110, (255, 220, 140, 255)) for c in range(3) for y in (200, 400)]
    for x in (480, 980, 1480, 1980): d.stroke([(x, 900), (x, 500)], LINE, 12); d.dot(x, 490, 34, (255, 236, 160, 255))
    fl(d, (120, 100, 110, 255)); im.alpha_composite(d.out()); [glow(im, x, 490, 160, (255, 220, 140, 110), 40) for x in (480, 980, 1480, 1980)]; im.convert('RGB').save(path)


def whitehouse(path):                                        # White House: sky blue, white portico with columns, flag, rose garden
    im = sky((90, 160, 230), (200, 230, 250), 1.0); d = Draw(W2, H2)
    d.rect(500, 420, 1900, 860, (236, 236, 230, 255)); d.poly([(900, 420), (1200, 260), (1500, 420)], fill=(230, 230, 224, 255), outline=LINE, width=10)
    for x in range(920, 1500, 100): d.rect(x, 440, x + 40, 860, (250, 250, 246, 255))
    for x in range(560, 1900, 120): d.rect(x, 500, x + 50, 580, (110, 150, 200, 255))
    d.stroke([(1200, 260), (1200, 120)], LINE, 6); d.rect(1200, 120, 1300, 180, RED)
    for x in range(0, W2, 90): d.dot(x, 900, 30, (90, 160, 80, 255)); d.dot(x + 20, 890, 10, PINK)
    fl(d, (140, 150, 140, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def factory(path):                                           # Ideal toy factory: red-yellow walls, conveyor belt, gears, saw-tooth skylights
    im = sky((230, 70, 60), (255, 200, 90), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.poly([(x, 160), (x + 300, 40), (x + 300, 160)], fill=(200, 230, 255, 255), outline=LINE, width=6)
    for x, y, r in ((400, 400, 120), (700, 480, 80), (1900, 420, 110)): d.dot(x, y, r, (250, 210, 60, 255)); d.ellipse(x, y, r, r, outline=LINE, width=8); d.dot(x, y, r // 3, (200, 150, 40, 255))
    d.rect(0, 700, W2, 760, (80, 80, 90, 255)); [d.dot(x, 730, 22, (150, 150, 160, 255)) for x in range(40, W2, 90)]
    fl(d, (160, 90, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def blackforest(path):                                       # Steiff workshop in Germany: snowy blue night-morning, timber frame, fir trees, glowing window
    im = sky((110, 150, 210), (220, 236, 250), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 200): d.poly([(x, 820), (x + 100, 460), (x + 200, 820)], fill=(60, 110, 90, 255)); d.poly([(x + 40, 600), (x + 100, 460), (x + 160, 600)], fill=WT)
    d.rect(800, 360, 1600, 860, (250, 236, 210, 255)); d.poly([(760, 360), (1200, 140), (1640, 360)], fill=(150, 60, 50, 255), outline=LINE, width=10)
    for x in (800, 1000, 1200, 1400, 1600): d.stroke([(x, 360), (x, 860)], (110, 70, 50, 255), 16)
    d.rect(1060, 480, 1340, 680, (255, 210, 120, 255)); r = np.random.RandomState(1)
    for _ in range(90): d.dot(r.randint(0, W2), r.randint(0, 900), 6, WT)
    fl(d, (220, 230, 240, 255)); im.alpha_composite(d.out()); glow(im, 1200, 580, 300, (255, 210, 140, 110), 60); im.convert('RGB').save(path)


def craze(path):                                             # 1907 teddy craze: rainbow bunting, confetti, toy-shop fronts, balloons
    im = sky((120, 200, 250), (255, 230, 250), 1.0); d = Draw(W2, H2); r = np.random.RandomState(5); cols = [RED, ORNG, YEL, (90, 200, 120, 255), (60, 140, 220, 255), VIO]
    for k in range(20): x = k * W2 / 20; d.poly([(x, 100), (x + W2 / 20, 100), (x + W2 / 40, 180)], fill=cols[k % 6], outline=LINE, width=4)
    for x in range(100, W2, 450): d.rect(x, 420, x + 380, 880, cols[(x // 450) % 6]); d.rect(x + 40, 520, x + 340, 760, (255, 246, 220, 255))
    for _ in range(140): d.rect(*(lambda x, y: (x, y, x + 14, y + 22))(r.randint(0, W2), r.randint(0, 900)), cols[r.randint(0, 6)])
    for x, y in ((300, 260), (1250, 220), (2100, 300)): d.dot(x, y, 60, cols[(x // 300) % 6]); d.stroke([(x, y + 60), (x, y + 240)], LINE, 4)
    fl(d, (220, 180, 150, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def church(path):                                            # Michigan church: violet walls, stained-glass windows, wooden pews, candles
    im = sky((90, 60, 140), (150, 110, 190), 1.0); d = Draw(W2, H2)
    for x in (400, 1200, 2000):
        d.chord(x, 300, 160, 160, 180, 360, fill=(250, 220, 120, 255)); d.rect(x - 160, 300, x + 160, 700, (250, 220, 120, 255))
        for k, c in enumerate((RED, (60, 140, 220, 255), (90, 200, 120, 255), PINK)): d.rect(x - 150 + (k % 2) * 150, 310 + (k // 2) * 190, x - 10 + (k % 2) * 150, 490 + (k // 2) * 190, c)
        d.stroke([(x, 150), (x, 700)], LINE, 10); d.stroke([(x - 160, 500), (x + 160, 500)], LINE, 10)
    fl(d, (110, 80, 90, 255)); im.alpha_composite(d.out()); [glow(im, x, 450, 280, (255, 230, 160, 90), 60) for x in (400, 1200, 2000)]; im.convert('RGB').save(path)


def bedroom(path):                                           # kid's bedroom: indigo starry wallpaper, round moon window, nightlight glow, toy shelf
    im = sky((60, 60, 140), (110, 100, 190), 1.0); d = Draw(W2, H2); stars(d, 120, 900, 9)
    d.dot(1200, 330, 220, (40, 40, 100, 255)); d.ellipse(1200, 330, 220, 220, outline=(240, 200, 120, 255), width=22); d.dot(1260, 280, 80, (255, 240, 190, 255))
    d.rect(1700, 520, 2300, 540, (150, 100, 70, 255)); [d.dot(1760 + k * 120, 480, 40, (RED, YEL, PINK, (90, 200, 120, 255), ORNG)[k]) for k in range(5)]
    fl(d, (90, 80, 140, 255)); im.alpha_composite(d.out()); glow(im, 400, 700, 400, (255, 200, 120, 90), 100); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast(('teddyr', 'collier', 'berryman', 'morris', 'rose', 'priest', 'kid', 'kid2', 'buyer'))
    multi = dict(realbear={'default': realbear(), 'tied': realbear('tied'), 'shocked': realbear('shocked')}, willow={'default': willow()}, hounds={'default': hounds()},
                 plush={'default': plush()}, steiff={'default': plush('steiff', (206, 200, 190, 255))}, qbear={'default': qbear()},
                 cartoon={'default': cartoon(1), 'c2': cartoon(2), 'c3': cartoon(3)}, inkpen={'default': inkpen()}, window={'default': window()}, letter={'default': letter()},
                 crate={'default': crate()}, pillow={'default': pillow()}, boxes={'default': boxes()}, papers={'default': LA.paper('THE BEAR HE', 'WOULD NOT SHOOT', 900)})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    HON, MOSS = (200, 120, 50, 255), (80, 120, 70, 255)
    cards = dict(hookc=M.bigneon('HE REFUSED', 'TO SHOOT IT!', 960, YEL, (255, 160, 80, 255)),
                 hunter=stamp("AMERICA'S MOST FAMOUS HUNTER", 1000, MOSS, 90, -3),
                 everykid=P_('EVERY KID', 'SLEEPS WITH ONE', (70, 60, 150, 255), 960, 150, 130, YEL),
                 y1902=M.cal('NOV 14', '1902', MOSS),
                 missi=P_('MISSISSIPPI', 'BEAR HUNT', (110, 90, 50, 255), 960, 140, 150, YEL),
                 tr=P_('THEODORE', 'ROOSEVELT', (150, 110, 70, 255), 940, 150, 170, WT),
                 notwell=stamp('NOT GOING WELL!', 900, RED, 130, -4),
                 holt=P_('HOLT COLLIER', 'HIS GUIDE', (88, 70, 116, 255), 960, 140, 160, YEL),
                 corner=stamp('AN OLD BLACK BEAR!', 960, (60, 56, 70, 255), 120, 3),
                 tied=stamp('TIED TO A WILLOW', 920, MOSS, 130, -3),
                 shot=stamp('TAKE THE SHOT!', 860, RED, 140, 4),
                 refuses=M.bigneon('ROOSEVELT', 'REFUSES!', 900, YEL, PINK),
                 unsport=stamp('UNSPORTSMANLIKE!', 960, (110, 90, 50, 255), 130, -3),
                 twodays=stamp('TWO DAYS LATER', 860, (50, 70, 130, 255), 130, 3),
                 berry=P_('CLIFFORD', 'BERRYMAN', (50, 70, 130, 255), 920, 150, 170, YEL),
                 spreads=stamp('THE CARTOON SPREADS!', 1000, RED, 110, -4),
                 brooklyn=P_('BROOKLYN', 'CANDY SHOP', (230, 90, 110, 255), 920, 160, 140, WT),
                 morrisc=P_('MORRIS', 'MICHTOM', (190, 50, 70, 255), 900, 150, 170, YEL),
                 rosec=P_('HIS WIFE', 'ROSE', (224, 120, 152, 255), 820, 150, 200, WT),
                 plushc=stamp('A LITTLE PLUSH BEAR', 980, HON, 110, 3),
                 sells=stamp('IT SELLS!', 760, (60, 150, 80, 255), 150, -4),
                 soldout=M.bigneon('SOLD', 'OUT!', 760, YEL, PINK),
                 name=P_('USE HIS', 'NAME?', (40, 80, 160, 255), 820, 160, 190, YEL),
                 quit=stamp('THEY QUIT CANDY!', 900, (230, 90, 110, 255), 130, -3),
                 ideal=P_('IDEAL NOVELTY', '& TOY COMPANY', RED, 1000, 130, 140, YEL),
                 germany=P_('MEANWHILE IN', 'GERMANY', (60, 90, 140, 255), 940, 130, 190, WT),
                 steiffc=P_('STEIFF', 'PLUSH BEAR', (120, 110, 100, 255), 860, 170, 150, YEL),
                 buyerc=stamp('ONE AMERICAN BUYER', 960, (70, 124, 88, 255), 110, 3),
                 y1907=M.cal('BY', '1907', VIO),
                 crazec=M.bigneon("IT'S A", 'CRAZE!', 820, PINK, YEL),
                 priestc=P_('A MICHIGAN', 'PRIEST', (90, 60, 140, 255), 900, 150, 190, YEL),
                 attacks=stamp('ATTACKS TEDDY BEARS!', 1000, RED, 110, -4),
                 hugs=stamp('KIDS KEEP HUGGING', 940, (90, 80, 200, 255), 120, 3),
                 kept=P_('BERRYMAN KEPT', 'DRAWING IT', (50, 70, 130, 255), 980, 130, 160, YEL),
                 smaller=stamp('SMALLER...', 760, (60, 50, 60, 255), 150, -3),
                 cuter=M.bigneon('ROUNDER!', 'CUTER!', 860, PINK, YEL),
                 realb=P_('THE REAL BEAR:', 'OLD, HEAVY, BEATEN', (60, 56, 70, 255), 1000, 130, 100, (255, 160, 80, 255)),
                 cuddly=stamp('ON EVERY PILLOW', 900, (70, 60, 150, 255), 130, 3),
                 cofc=M.bigneon('A CARTOON OF', 'A CARTOON!', 1000, YEL, (255, 160, 80, 255)))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (150, 140, 120), (136, 126, 108))
    M.sandtex(T('mud.jpg'), (130, 120, 80), (110, 104, 66), seed=4); M.sandtex(T('campdirt.jpg'), (190, 150, 100), (170, 132, 86)); M.sandtex(T('moss.jpg'), (90, 130, 70), (76, 112, 60))
    CE.tiles(T('boardsb.jpg'), (110, 110, 140), (96, 96, 126)); M.sandtex(T('paperfl.jpg'), (226, 214, 186), (210, 198, 170)); CE.tiles(T('checker.jpg'), (250, 200, 220), (200, 240, 230))
    CE.tiles(T('brickfl.jpg'), (150, 110, 110), (136, 98, 98)); CE.tiles(T('lawn.jpg'), (130, 180, 110), (116, 164, 98)); CE.tiles(T('factfl.jpg'), (170, 120, 90), (154, 106, 80))
    M.sandtex(T('snow.jpg'), (230, 236, 246), (206, 216, 232)); CE.tiles(T('confl.jpg'), (240, 200, 160), (226, 186, 146)); CE.tiles(T('pews.jpg'), (130, 90, 90), (116, 78, 78)); CE.tiles(T('rug.jpg'), (120, 110, 170), (106, 96, 156))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(bayou=bayou, camp=camp, forest=forest, newsroom=newsroom, inkworld=inkworld, candy=candy, street=street, whitehouse=whitehouse, factory=factory, blackforest=blackforest, craze=craze, church=church, bedroom=bedroom)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
