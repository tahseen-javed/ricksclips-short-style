#!/usr/bin/env python3
"""Assets for video 25: Roy Sullivan, the park ranger lightning hit seven times (and skipped the one time it hit his wife).
Blue Ridge storm world: indigo-teal storm peak (hook + loop), misty sage-blue layered ridges at dawn, pine park gate, sunset lookout peak, purple dusk
mountain road, golden backyard with laundry poles, pine-plank ranger station, teal fishing lake at dusk, emerald fern trail, gold-spotlight record stage.
Cute cast (new): Roy (flat green ranger hat, ranger shirt), his wife (polka headscarf + dress), three hikers, a cute brown bear. Strikes are cartoon
bolts, smoke puffs and dizzy stars only.
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
LEM, PINE, STORM, SMOKE = (255, 240, 60, 255), (60, 120, 80, 255), (60, 70, 120, 255), (200, 200, 214, 255)
LA.NEW.update({
    'roy': dict(sk=0, style='side', hair=(120, 80, 50, 255), suit=(150, 160, 100, 255), shade=(124, 134, 80, 255), body='ranger', stache=(120, 80, 50, 255), xhat='ranger'),
    'wife': dict(sk=0, style='bob', hair=(200, 130, 70, 255), suit=(240, 120, 150, 255), shade=(214, 96, 126, 255), body='polka', band=LEM, xhat='scarf', hatc=(120, 170, 240, 255)),
    'hk1': dict(sk=1, style='curly', hair=(40, 30, 26, 255), suit=(255, 150, 60, 255), shade=(224, 122, 40, 255), body='sweater'),
    'hk2': dict(sk=2, style='bob', hair=(30, 24, 24, 255), suit=(120, 200, 240, 255), shade=(92, 170, 214, 255), body='cardigan', band=PINK),
    'hk3': dict(sk=0, style='spiky', hair=(230, 190, 90, 255), suit=(170, 120, 230, 255), shade=(140, 96, 200, 255), body='denim', glasses=2),
})


def boltp(glow_=True):                                       # big glossy cartoon lightning bolt
    d = Draw(700, 1400)
    if glow_: d.poly([(330, 0), (600, 0), (430, 520), (660, 520), (180, 1400), (300, 760), (60, 760)], fill=(255, 250, 180, 90))
    d.poly([(350, 40), (560, 40), (400, 540), (600, 540), (220, 1320), (320, 740), (110, 740)], fill=LEM, outline=LINE, width=16); d.poly([(380, 80), (460, 80), (340, 500)], fill=(255, 255, 220, 255))
    return d.out()


def qwife():                                                 # open loop: violet silhouette with a "?" under a laundry line
    d = Draw(800, 1300); d.dot(400, 330, 210, (130, 90, 200, 255)); d.chord(400, 360, 230, 210, 180, 360, fill=(110, 76, 180, 255)); d.poly([(170, 580), (630, 580), (720, 1260), (80, 1260)], fill=(130, 90, 200, 255))
    d.text(400, 340, '?', 300, WT, stroke=8, stroke_fill=LINE); return d.out()


def tally(n=0):                                              # strike tally board: 7 bolt slots, n lit
    d = Draw(1400, 800); d.rrect(30, 30, 1370, 770, 50, fill=(40, 46, 90, 255), outline=LINE, width=16); d.text(700, 140, 'STRIKES', 120, LEM, stroke=6, stroke_fill=LINE)
    for k in range(7):
        x = 160 + k * 180; c = LEM if k < n else (80, 86, 130, 255); d.poly([(x + 10, 260), (x + 70, 260), (x + 30, 450), (x + 80, 450), (x - 20, 700), (x + 10, 520), (x - 40, 520)], fill=c, outline=LINE, width=8)
    return d.out()


def gate():                                                  # rustic park sign
    d = Draw(1500, 1100)
    for x in (130, 1370): d.rect(x - 50, 120, x + 50, 1080, (110, 70, 40, 255)); d.rect(x - 50, 120, x - 20, 1080, (140, 96, 60, 255))
    d.rrect(60, 200, 1440, 760, 40, fill=(150, 96, 54, 255), outline=LINE, width=16); d.rrect(100, 240, 1400, 720, 24, outline=(240, 220, 160, 255), width=8)
    d.text(750, 370, 'SHENANDOAH', 170, (250, 236, 200, 255), stroke=7, stroke_fill=LINE); d.text(750, 520, 'NATIONAL PARK', 110, LEM, stroke=5, stroke_fill=LINE); d.text(750, 640, 'VIRGINIA', 80, (250, 236, 200, 255), stroke=4, stroke_fill=LINE)
    for x in (300, 1200): d.poly([(x, 120), (x - 90, 200), (x + 90, 200)], fill=PINE, outline=LINE, width=8)
    return d.out()


def tower(zap=False):                                        # fire lookout tower with a cute cabin face (zap: bolt + glow)
    im = Image.new('RGBA', (1100, 1700)); d = Draw(1100, 1700)
    if zap: d.dot(550, 330, 420, (255, 250, 180, 110))
    for a, b in (((250, 1680), (420, 640)), ((850, 1680), (680, 640)), ((300, 1400), (800, 1100)), ((800, 1400), (300, 1100)), ((350, 1100), (750, 860)), ((750, 1100), (350, 860))): d.stroke([a, b], (120, 80, 50, 255), 30); d.stroke([a, b], LINE, 6)
    d.rrect(300, 380, 800, 660, 30, fill=(200, 80, 60, 255), outline=LINE, width=14); d.poly([(240, 400), (550, 200), (860, 400)], fill=(90, 60, 50, 255), outline=LINE, width=14)
    d.rect(340, 430, 760, 520, (180, 220, 250, 255)); eyes(d, 550, 580, 0.7, 'shocked' if zap else 'happy'); im.alpha_composite(d.out())
    if zap: im.alpha_composite(boltp(False).resize((210, 420)), (600, 0))
    return im


def boot(zap=False):                                         # ranger boot with a cute face and a cartoon smoke puff (+ small bolt)
    d = Draw(1100, 1000); d.rrect(300, 160, 640, 760, 60, fill=(130, 80, 50, 255), outline=LINE, width=16); d.rrect(300, 620, 960, 900, 80, fill=(130, 80, 50, 255), outline=LINE, width=16)
    d.rect(300, 860, 960, 920, (60, 40, 30, 255)); [d.stroke([(330, y), (610, y)], (240, 220, 160, 255), 10) for y in (260, 340, 420)]; eyes(d, 700, 730, 0.6, 'shocked')
    for x, y, r in ((200, 300, 90), (140, 180, 70), (240, 120, 60)): d.dot(x, y, r, SMOKE); d.ellipse(x, y, r, r, outline=LINE, width=8)
    if zap: d.poly([(880, 20), (960, 20), (900, 200), (980, 200), (820, 460), (860, 280), (800, 280)], fill=LEM, outline=LINE, width=10)
    return d.out()


def truck(mode=''):                                          # 1969 pickup with a face; zap: bolt through the window; flee: speed lines
    d = Draw(1600, 1000)
    if mode == 'flee':
        for y in (420, 560, 700): d.stroke([(1300, y), (1580, y)], WT, 18)
    d.rrect(80, 460, 1300, 800, 60, fill=(60, 140, 180, 255), outline=LINE, width=16); d.rrect(260, 220, 760, 480, 50, fill=(60, 140, 180, 255), outline=LINE, width=16)
    d.rrect(310, 260, 710, 450, 30, fill=(200, 236, 255, 255), outline=LINE, width=10); d.rect(80, 600, 1300, 630, WT)
    for x in (330, 1050): d.dot(x, 800, 130, (40, 40, 50, 255)); d.dot(x, 800, 60, (180, 180, 190, 255))
    d.dot(1240, 560, 50, LEM); eyes(d, 1000, 560, 0.8, 'shocked' if mode == 'zap' else 'happy')
    if mode == 'zap':
        d.poly([(560, 0), (680, 0), (560, 260), (660, 260), (420, 560), (480, 360), (380, 360)], fill=LEM, outline=LINE, width=12)
        for x, y, r in ((560, 200, 60), (650, 150, 50)): d.dot(x, y, r, (255, 255, 230, 160))
    return d.out()


def brows():                                                 # two little eyebrows flying away on tiny wings
    d = Draw(1200, 700)
    for x, y in ((330, 400), (850, 280)):
        d.rrect(x - 180, y - 40, x + 180, y + 40, 40, fill=(120, 80, 50, 255), outline=LINE, width=12)
        for sg in (-1, 1): d.ellipse(x + sg * 60, y - 100, 70, 40, fill=WT, outline=LINE, width=8)
        d.stroke([(x - 300, y + 60), (x - 200, y + 60)], WT, 10)
    return d.out()


def towel():                                                 # wet towel with drips + a little steam puff
    d = Draw(1000, 1100); d.rrect(150, 200, 850, 1000, 60, fill=(120, 200, 240, 255), outline=LINE, width=16)
    for y in (330, 870): d.rect(160, y, 840, y + 40, WT)
    for x in (250, 450, 650, 800): d.ellipse(x, 1060, 22, 34, fill=(150, 210, 255, 255), outline=LINE, width=6)
    for x, y, r in ((300, 120, 70), (420, 70, 60), (540, 110, 70)): d.dot(x, y, r, (240, 244, 250, 220))
    eyes(d, 500, 600, 1.0, 'happy'); return d.out()


def puff():                                                  # cute cartoon hair flame -> smoke puff (no injury)
    d = Draw(800, 900); d.poly([(400, 60), (560, 360), (620, 600), (400, 820), (180, 600), (240, 360)], fill=(255, 140, 40, 255), outline=LINE, width=14)
    d.poly([(400, 300), (500, 520), (400, 720), (300, 520)], fill=(255, 230, 80, 255)); eyes(d, 400, 600, 0.55, 'shocked'); return d.out()


def cloud(zap=False):                                        # storm cloud with a cheeky face (+ bolt)
    d = Draw(1500, 1300)
    for x, y, r in ((400, 420, 260), (750, 330, 320), (1100, 430, 260), (580, 560, 250), (930, 560, 250)): d.dot(x, y, r, (90, 96, 140, 255))
    for x, y, r in ((400, 420, 260), (750, 330, 320), (1100, 430, 260)): d.arc(x, y, r, r, 180, 360, LINE, 14)
    d.rect(250, 560, 1250, 700, (90, 96, 140, 255)); d.stroke([(220, 700), (1280, 700)], LINE, 14); eyes(d, 750, 470, 1.1, 'happy')
    for sg in (-1, 1): d.stroke([(750 + sg * 30, 380), (750 + sg * 120, 400)], LINE, 14)
    if zap: d.poly([(700, 700), (840, 700), (740, 960), (860, 960), (560, 1300), (640, 1040), (520, 1040)], fill=LEM, outline=LINE, width=12)
    return d.out()


def rod():                                                   # fishing rod + a jumping cute fish
    d = Draw(1200, 1100); d.stroke([(150, 1050), (950, 120)], (150, 100, 60, 255), 24); d.stroke([(950, 120), (1000, 600)], (240, 240, 240, 255), 4); d.dot(300, 880, 50, (60, 60, 70, 255))
    d.ellipse(1000, 700, 140, 80, fill=(255, 170, 80, 255), outline=LINE, width=12); d.poly([(1130, 700), (1200, 620), (1200, 780)], fill=(255, 170, 80, 255), outline=LINE, width=10); d.dot(940, 680, 16, LINE)
    for x, y in ((900, 860), (1080, 880)): d.ellipse(x, y, 30, 40, fill=(150, 210, 255, 255), outline=LINE, width=6)
    return d.out()


def bear():                                                  # cute brown bear standing and waving
    d = Draw(1000, 1300); BRN_, MZ = (150, 96, 60, 255), (220, 180, 130, 255)
    d.ellipse(500, 900, 300, 340, fill=BRN_, outline=LINE, width=16); d.ellipse(500, 960, 170, 220, fill=MZ)
    for sg in (-1, 1): d.dot(500 + sg * 190, 150, 80, BRN_); d.ellipse(500 + sg * 190, 150, 80, 80, outline=LINE, width=14); d.dot(500 + sg * 190, 150, 40, MZ)
    d.dot(500, 360, 250, BRN_); d.ellipse(500, 360, 250, 250, outline=LINE, width=16); d.ellipse(500, 450, 110, 80, fill=MZ, outline=LINE, width=10); d.ellipse(500, 410, 36, 24, fill=LINE)
    eyes(d, 500, 330, 0.85, 'happy'); d.rrect(760, 520, 880, 820, 60, fill=BRN_, outline=LINE, width=14); d.rrect(120, 700, 240, 980, 60, fill=BRN_, outline=LINE, width=14)
    return d.out()


def book(stamp_=False):                                      # giant gold record book (stamp: VERIFIED 7)
    d = Draw(1300, 1100); d.rrect(100, 120, 1200, 1000, 40, fill=(250, 246, 230, 255), outline=LINE, width=16); d.stroke([(650, 130), (650, 990)], LINE, 10)
    d.rrect(60, 960, 1240, 1060, 30, fill=(214, 160, 40, 255), outline=LINE, width=12)
    d.text(375, 300, 'WORLD', 110, (200, 140, 30, 255), stroke=4, stroke_fill=LINE); d.text(375, 440, 'RECORDS', 90, (200, 140, 30, 255), stroke=4, stroke_fill=LINE)
    for y in (600, 680, 760, 840): d.stroke([(170, y), (580, y)], (180, 180, 190, 255), 10); d.stroke([(720, y - 300), (1130, y - 300)], (180, 180, 190, 255), 10)
    d.poly([(925, 560), (975, 560), (945, 700), (990, 700), (900, 880), (920, 760), (880, 760)], fill=LEM, outline=LINE, width=8)
    if stamp_:
        s_ = Draw(800, 360); s_.rrect(20, 20, 780, 340, 40, outline=RED, width=22); s_.text(400, 130, 'VERIFIED', 120, RED); s_.text(400, 260, '7 STRIKES', 90, RED)
        d_ = d.out(); d_.alpha_composite(s_.out().rotate(-12, expand=True), (420, 560)); return d_
    return d.out()


def trophy():                                                # gold trophy with a bolt and #1
    d = Draw(900, 1200); d.rrect(250, 1000, 650, 1150, 20, fill=(120, 80, 50, 255), outline=LINE, width=12); d.rect(400, 760, 500, 1000, (240, 190, 60, 255))
    d.chord(450, 300, 300, 480, 0, 180, fill=(250, 200, 60, 255), outline=LINE, width=16); d.rect(150, 260, 750, 320, (250, 200, 60, 255))
    for sg in (-1, 1): d.arc(450 + sg * 330, 450, 90, 120, 0, 360, LINE, 14)
    d.text(450, 500, '#1', 170, WT, stroke=8, stroke_fill=LINE); shine(d, 230, 340, 220); return d.out()


def laundry():                                               # laundry line with cute socks, shirt and a sheet
    d = Draw(1600, 1000)
    for x in (60, 1540): d.rect(x - 20, 120, x + 20, 980, (150, 110, 70, 255))
    d.stroke([(60, 160), (800, 220), (1540, 160)], (240, 240, 240, 255), 8)
    for k, (x, w_, h_, c) in enumerate(((220, 160, 300, PINK), (480, 300, 420, (120, 200, 240, 255)), (850, 360, 520, WT), (1250, 160, 300, LEM))):
        y = 180 + (40 if 300 < x < 1300 else 10); d.rrect(x - w_ / 2, y, x + w_ / 2, y + h_, 30, fill=c, outline=LINE, width=12); d.rect(x - 8, y - 20, x + 8, y + 30, (200, 140, 90, 255))
        if k in (0, 3): eyes(d, x, y + 150, 0.5, 'happy')
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def ridges(d, base, cols, amp=80):
    for k, c in enumerate(cols): hills(d, base + k * 90, c, amp - k * 10, 3 + k, ph=k * 1.3)


def stormpeak(path):                                         # hook: indigo-teal storm, rain streaks, layered dark ridges, far bolts
    im = sky((30, 34, 80), (40, 120, 140), 1.0); d = Draw(W2, H2); r = np.random.RandomState(3)
    for _ in range(140): x, y = r.randint(0, W2), r.randint(0, 800); d.stroke([(x, y), (x - 20, y + 60)], (180, 220, 255, 90), 3)
    ridges(d, 560, [(50, 70, 110, 255), (40, 90, 100, 255), (30, 70, 70, 255)]); bolt(d, 400, 60, 1.0); bolt(d, 1900, 120, 0.8)
    fl(d, (40, 70, 70, 255)); im.alpha_composite(d.out()); glow(im, 420, 200, 300, (255, 250, 180, 110), 80); glow(im, 1910, 230, 260, (255, 250, 180, 90), 80); im.convert('RGB').save(path)


def dawn(path):                                              # Blue Ridge dawn: misty sage-blue layered ridges, peach sun
    im = sky((150, 180, 220), (255, 210, 170), 1.0); d = Draw(W2, H2); d.dot(1600, 420, 120, (255, 236, 190, 255))
    ridges(d, 480, [(120, 150, 200, 255), (100, 140, 170, 255), (80, 130, 130, 255), (60, 110, 90, 255)], 70)
    fl(d, (70, 110, 80, 255)); im.alpha_composite(d.out()); glow(im, 1600, 420, 400, (255, 230, 190, 120), 120); im.convert('RGB').save(path)


def pines(path):                                             # pine park gate: green ridges, fir rows, blue sky
    im = sky((90, 170, 230), (210, 240, 230), 1.0); d = Draw(W2, H2); ridges(d, 600, [(100, 160, 140, 255), (70, 130, 100, 255)], 60)
    for k, x in enumerate(range(40, W2, 160)): s_ = 0.9 + (k % 3) * 0.2; d.poly([(x, 900), (x + 70 * s_, 900 - 300 * s_), (x + 140 * s_, 900)], fill=(40 + (k % 3) * 20, 110, 70, 255), outline=LINE, width=8)
    fl(d, (90, 140, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def sunsetpeak(path):                                        # lookout peak: orange-magenta sunset with a dark storm front rolling in
    im = sky((240, 110, 120), (255, 200, 120), 1.0); d = Draw(W2, H2)
    for x, y, r in ((1700, 180, 220), (2000, 240, 260), (2300, 160, 240), (1500, 260, 180)): d.dot(x, y, r, (70, 70, 110, 255))
    ridges(d, 640, [(150, 80, 110, 255), (110, 60, 90, 255)], 90); fl(d, (100, 70, 80, 255)); im.alpha_composite(d.out()); glow(im, 600, 600, 500, (255, 220, 150, 120), 120); im.convert('RGB').save(path)


def duskroad(path):                                          # 1969 dusk road: purple sky, winding road, guard rail, ridges
    im = sky((90, 60, 140), (255, 140, 110), 1.0); d = Draw(W2, H2); ridges(d, 560, [(110, 70, 130, 255), (80, 60, 110, 255)], 80)
    d.poly([(0, 940), (700, 760), (1500, 720), (W2, 780), (W2, 860), (1500, 800), (700, 840), (0, 1000)], fill=(70, 66, 80, 255)); [d.rect(x, 740, x + 16, 790, WT) for x in range(100, W2, 180)]
    fl(d, (80, 60, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def yard(path):                                              # golden backyard: picket fence, little house, apple tree, warm sky
    im = sky((120, 190, 240), (255, 220, 150), 1.0); d = Draw(W2, H2); d.rect(1500, 420, 2200, 860, (240, 230, 210, 255)); d.poly([(1450, 430), (1850, 200), (2250, 430)], fill=(200, 80, 70, 255), outline=LINE, width=12)
    win(d, 1580, 520, 1740, 660, (150, 210, 250, 255)); d.rect(1900, 600, 2020, 860, (120, 80, 60, 255)); ptree(d, 500, 860, 1.4, (90, 170, 90, 255), fruit=RED)
    for x in range(0, W2, 70): d.poly([(x, 900), (x, 780), (x + 25, 750), (x + 50, 780), (x + 50, 900)], fill=WT, outline=LINE, width=6)
    fl(d, (110, 180, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def cabin(path):                                             # ranger station: pine planks, park map, wood stove, rainy window
    im = sky((170, 120, 80), (200, 150, 100), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 112, 940, (190, 140, 90, 255))
    d.rrect(300, 160, 900, 560, 16, fill=(220, 236, 200, 255), outline=LINE, width=14); d.stroke([(340, 400), (500, 300), (700, 420), (860, 260)], (90, 160, 220, 255), 14)
    d.rrect(1500, 160, 2000, 560, 16, fill=(60, 80, 120, 255), outline=WT, width=22); [d.stroke([(x, 200), (x - 20, 260)], (180, 220, 255, 200), 4) for x in range(1540, 1980, 50)]
    d.rrect(1050, 520, 1300, 900, 30, fill=(60, 60, 70, 255), outline=LINE, width=12); d.dot(1175, 720, 60, (255, 140, 60, 255))
    fl(d, (140, 100, 70, 255)); im.alpha_composite(d.out()); glow(im, 1175, 720, 200, (255, 160, 80, 100), 60); im.convert('RGB').save(path)


def lake(path):                                              # teal fishing lake at dusk: pines, dock, moon, ripples
    im = sky((50, 70, 130), (240, 160, 140), 1.0); d = Draw(W2, H2); d.dot(1800, 240, 80, (255, 246, 210, 255)); ridges(d, 560, [(60, 80, 110, 255)], 60)
    for x in range(0, W2, 130): d.poly([(x, 700), (x + 60, 480), (x + 120, 700)], fill=(30, 70, 60, 255))
    d.rect(0, 700, W2, 940, (40, 130, 140, 255)); [d.stroke([(x, 760 + (x % 4) * 40), (x + 120, 760 + (x % 4) * 40)], (150, 220, 220, 180), 6) for x in range(20, W2, 230)]
    fl(d, (110, 80, 60, 255)); im.alpha_composite(d.out()); glow(im, 1800, 240, 260, (255, 240, 200, 100), 60); im.convert('RGB').save(path)


def ferns(path):                                             # emerald fern trail: tall trunks, sun shafts, ferns
    im = sky((40, 110, 70), (150, 210, 130), 1.0); d = Draw(W2, H2)
    for x in range(80, W2, 300): d.rect(x, 0, x + 90, 940, (90, 70, 50, 255))
    for k in range(5): x = 300 + k * 450; d.poly([(x, 0), (x + 120, 0), (x + 420, 940), (x + 260, 940)], fill=(255, 255, 210, 50))
    for x in range(0, W2, 120): [d.ellipse(x + j * 30, 880 - j * 10, 60, 20, fill=(60, 150, 80, 255)) for j in range(3)]
    fl(d, (80, 110, 60, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def recstage(path):                                          # record stage: deep blue with gold spotlights and sparkles
    im = sky((20, 24, 70), (60, 50, 120), 1.0); d = Draw(W2, H2); stars(d, 60, 800, 21)
    for x in (500, 1200, 1900): d.poly([(x - 60, 0), (x + 60, 0), (x + 360, 940), (x - 360, 940)], fill=(255, 220, 120, 45))
    fl(d, (60, 40, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 700, 500, (255, 210, 120, 80), 100); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast2(('roy', 'wife', 'hk1', 'hk2', 'hk3'))
    multi = dict(boltp={'default': boltp()}, qwife={'default': qwife()}, tally={'default': tally(0), **{'t%d' % k: tally(k) for k in range(1, 8)}}, gate={'default': gate()},
                 tower={'default': tower(), 'zap': tower(True)}, boot={'default': boot(), 'zap': boot(True)}, truck={'default': truck(), 'zap': truck('zap'), 'flee': truck('flee')},
                 brows={'default': brows()}, towel={'default': towel()}, puff={'default': puff()}, cloud={'default': cloud(), 'zap': cloud(True)}, rod={'default': rod()},
                 bear={'default': bear()}, book={'default': book(), 'stamp': book(True)}, trophy={'default': trophy()}, laundry={'default': laundry()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    ST_, PN = (50, 60, 120, 255), (50, 110, 70, 255)
    cards = dict(hookc=M.bigneon('NEVER STRIKES', 'TWICE?', 960, YEL, (90, 200, 255, 255)),
                 seven=M.bigneon('STRUCK', '7 TIMES!', 860, YEL, (90, 200, 255, 255)),
                 survived=stamp('SURVIVED EVERY ONE!', 980, (60, 150, 80, 255), 110, -3),
                 rangerc=P_('ROY SULLIVAN', 'PARK RANGER', PN, 980, 140, 140, YEL),
                 y1942=M.cal('#1', '1942', ST_), y1969=M.cal('#2', '1969', (120, 70, 140, 255)), y1970=M.cal('#3', '1970', (200, 80, 70, 255)),
                 y1972=M.cal('#4', '1972', (150, 100, 60, 255)), y1973=M.cal('#5', '1973', (90, 60, 140, 255)), y1976=M.cal('#6', '1976', PN), y1977=M.cal('#7', '1977', (40, 120, 130, 255)),
                 knocked=stamp('KNOCKED OUT COLD!', 960, ST_, 110, 3),
                 brow=M.bigneon('BYE BYE', 'EYEBROWS!', 900, YEL, PINK),
                 shoulder=stamp('HIS SHOULDER!', 820, (200, 80, 70, 255), 130, -3),
                 inside=stamp('INSIDE?!', 640, (150, 100, 60, 255), 170, 4),
                 towels=stamp('WET TOWELS!', 820, (60, 140, 200, 255), 140, -3),
                 caught=stamp('CAUGHT HIM ANYWAY!', 980, (90, 60, 140, 255), 110, 3),
                 ankle=stamp('HIS ANKLE!', 760, PN, 140, -4),
                 bearc=M.bigneon('THEN...', 'A BEAR!', 820, YEL, (255, 160, 80, 255)),
                 once=P_('MOST PEOPLE:', 'NOT EVEN ONCE', ST_, 1000, 130, 140, YEL),
                 outside=stamp('WHOEVER IS OUTSIDE', 980, (40, 120, 130, 255), 110, -3),
                 job=P_("ROY'S JOB:", 'BE OUTSIDE', PN, 960, 140, 160, YEL),
                 decades=stamp('FOR DECADES', 820, (120, 70, 140, 255), 140, 3),
                 nobody=P_('NOBODY HAS', 'SURVIVED MORE', (150, 110, 30, 255), 1000, 130, 140, WT),
                 strange=M.bigneon('THE STRANGEST', 'PART...', 980, YEL, PINK),
                 hither=M.bigneon('IT HIT', 'HER!', 760, YEL, (255, 160, 80, 255)),
                 skipped=P_('IT SKIPPED', 'ROY!', ST_, 860, 150, 200, YEL))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('rock.jpg'), (70, 90, 90), (60, 78, 78), seed=4); M.sandtex(T('meadow.jpg'), (110, 150, 90), (96, 134, 78)); CE.tiles(T('gravel.jpg'), (150, 140, 120), (136, 126, 108))
    M.sandtex(T('peak.jpg'), (130, 90, 90), (116, 78, 78)); CE.tiles(T('asphalt.jpg'), (80, 70, 90), (70, 62, 80)); M.sandtex(T('grass.jpg'), (120, 190, 100), (106, 174, 88))
    B.tex_wood(T('wood.jpg')); CE.tiles(T('dockw.jpg'), (140, 100, 70), (126, 88, 60)); M.sandtex(T('moss2.jpg'), (80, 120, 60), (68, 104, 52)); CE.tiles(T('stage.jpg'), (70, 50, 110), (60, 42, 96))
    CE.tiles(T('pave.jpg'), (60, 80, 80), (52, 70, 70)); G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(stormpeak=stormpeak, dawn=dawn, pines=pines, sunsetpeak=sunsetpeak, duskroad=duskroad, yard=yard, cabin=cabin, lake=lake, ferns=ferns, recstage=recstage)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
