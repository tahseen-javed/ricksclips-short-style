#!/usr/bin/env python3
"""Assets for video 18: a rocket scientist invented the Super Soaker (Lonnie Johnson).  80s neon-splash world: cute cast (Lonnie,
an engineer, the toy exec, two kids), glossy hero props with faces (water blaster, Galileo, Jupiter, nozzle sink), ten painted sets, plaques.
usage: make_assets.py <project> <font>"""
import os, math, json
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import lordgta_assets as LA
import mco_assets as M
import mono_assets as MA
import pd_assets as PD
from assets_base import Draw, LINE, WHITE

ROOT = B.ROOT; GOLDL = M.GOLDL
dk, glow, plaque, stamp, sky, W2, H2, fl = LA.dk, CE.glow, LA.plaque, LA.stamp, M.sky, M.W2, M.H2, MA.fl
eyes, shine, win = PD.eyes, PD.shine, PD.win
WT, LIME, PINK, CYAN, YEL, ORNG, TEAL, NAVY, RED, VIO = (250, 250, 245, 255), (120, 230, 90, 255), (255, 70, 160, 255), (60, 220, 255, 255), (255, 214, 40, 255), (255, 140, 40, 255), (20, 190, 180, 255), (30, 40, 110, 255), (230, 50, 60, 255), (130, 70, 220, 255)
WATER, WATERD = (150, 220, 255, 235), (60, 150, 230, 255)
LA.NEW.update({
    'lonnie': dict(sk=2, style='side', hair=(30, 24, 24, 255), suit=(244, 248, 252, 255), shade=(206, 214, 228, 255), body='suit', tie=(40, 120, 230, 255), stache=(30, 24, 24, 255)),
    'eng': dict(sk=0, style='spiky', hair=(230, 120, 40, 255), suit=(255, 170, 60, 255), shade=(220, 136, 40, 255), body='sweater', freck=1),
    'exec': dict(sk=1, style='slick', hair=(50, 34, 30, 255), suit=PINK, shade=(210, 50, 130, 255), body='suit', tie=YEL),
    'kidc': dict(sk=1, style='bob', hair=(30, 24, 30, 255), suit=TEAL, shade=(16, 150, 144, 255), body='sweater', band=PINK),
    'kidd': dict(sk=0, style='curly', hair=(240, 190, 80, 255), suit=(255, 90, 90, 255), shade=(220, 60, 70, 255), body='denim', freck=1),
})
star = lambda d, cx, cy, R, col, w=8: d.poly([(cx + (R if k % 2 == 0 else R * 0.45) * math.cos(math.radians(k * 36 - 90)), cy + (R if k % 2 == 0 else R * 0.45) * math.sin(math.radians(k * 36 - 90))) for k in range(10)], fill=col, outline=LINE, width=w)


def soaker(face='happy', body=LIME, tank=YEL):               # pump water blaster: big round tank on top, long barrel, pump grip, trigger
    d = Draw(1200, 640)
    d.rrect(140, 280, 1000, 420, 60, fill=body, outline=LINE, width=16); d.rrect(980, 310, 1130, 390, 30, fill=ORNG, outline=LINE, width=14)
    d.rrect(560, 400, 820, 470, 30, fill=ORNG, outline=LINE, width=14); d.poly([(230, 400), (360, 400), (300, 600), (170, 600)], fill=body, outline=LINE, width=16)
    d.ellipse(520, 200, 260, 150, fill=tank, outline=LINE, width=16); d.ellipse(520, 200, 200, 100, fill=(255, 236, 140, 255)); d.rect(500, 40, 540, 70, LINE); d.rrect(470, 20, 570, 60, 14, fill=RED, outline=LINE, width=10)
    shine(d, 360, 120, 120, 30); eyes(d, 520, 200, 0.75, face); return d.out()


def blast(n=7):                                              # a long water jet with droplets
    d = Draw(1600, 360)
    d.poly([(0, 150), (1450, 60), (1600, 180), (1450, 300), (0, 210)], fill=WATER, outline=WATERD, width=10)
    for k in range(n): d.stroke([(80 + k * 200, 180), (240 + k * 200, 170 - (k % 2) * 30)], WT, 12)
    for x, y, r in ((1500, 60, 30), (1560, 300, 26), (1350, 20, 20), (1580, 120, 18), (1400, 330, 22)): d.dot(x, y, r, WATER)
    return d.out()


def sink(on=False):                                          # pedestal sink, homemade brass nozzle + hose on the tap
    d = Draw(900, 1100); d.rrect(330, 520, 570, 1080, 30, fill=(250, 214, 150, 255), outline=LINE, width=16)
    d.chord(450, 420, 400, 180, 0, 180, fill=(255, 226, 170, 255), outline=LINE, width=16); d.rect(52, 400, 848, 440, (255, 226, 170, 255)); d.stroke([(50, 420), (850, 420)], LINE, 14)
    d.rrect(420, 250, 480, 420, 20, fill=(200, 200, 210, 255), outline=LINE, width=12); d.rrect(420, 250, 640, 300, 20, fill=(200, 200, 210, 255), outline=LINE, width=12)
    d.stroke([(630, 276), (760, 180), (820, 240)], (60, 160, 90, 255), 34); d.rrect(780, 210, 880, 270, 18, fill=(230, 170, 60, 255), outline=LINE, width=10)
    if on:
        for k in range(6): d.dot(860 + k * 10, 230 - k * 22, 20 - k * 2, WATER)
    eyes(d, 450, 700, 0.7, 'shocked' if on else 'happy'); return d.out()


def galileo():                                               # Galileo probe: big white umbrella dish, booms, gold body
    d = Draw(1000, 900); d.stroke([(500, 520), (140, 820)], LINE, 22); d.stroke([(500, 520), (860, 820)], LINE, 22); d.dot(140, 820, 46, (200, 200, 210, 255)); d.dot(860, 820, 46, (200, 200, 210, 255))
    d.chord(500, 330, 380, 260, 180, 360, fill=WT, outline=LINE, width=16)
    for a in range(200, 341, 28): d.stroke([(500, 330), (500 + 370 * math.cos(math.radians(a)), 330 + 250 * math.sin(math.radians(a)))], (180, 190, 210, 255), 8)
    d.rrect(380, 330, 620, 600, 30, fill=(240, 190, 60, 255), outline=LINE, width=16); eyes(d, 500, 440, 0.6, 'happy'); return d.out()


def jupiter(face='happy'):                                   # striped Jupiter with the great red spot and a cute face
    d = Draw(1000, 1000); d.dot(500, 500, 470, (236, 196, 150, 255))
    for k, y in enumerate(range(150, 900, 110)): d.ellipse(500, y, 470 - abs(y - 500) * 0.35, 30, fill=((200, 130, 90, 255), (250, 226, 196, 255))[k % 2])
    d.ellipse(700, 650, 110, 60, fill=(210, 80, 60, 255), outline=LINE, width=8); d.ellipse(500, 500, 470, 470, outline=LINE, width=16)
    eyes(d, 470, 430, 1.4, face); return d.out()


def rocket():                                                # small model rocket on a stand
    d = Draw(500, 1200); d.poly([(250, 40), (360, 260), (140, 260)], fill=RED, outline=LINE, width=14); d.rrect(140, 250, 360, 900, 30, fill=WT, outline=LINE, width=14)
    for sg in (-1, 1): d.poly([(250 + sg * 110, 700), (250 + sg * 220, 980), (250 + sg * 110, 900)], fill=RED, outline=LINE, width=14)
    d.dot(250, 420, 60, CYAN); d.ellipse(250, 420, 60, 60, outline=LINE, width=10); d.rrect(150, 1000, 350, 1160, 20, fill=(120, 130, 150, 255), outline=LINE, width=12)
    d.stroke([(250, 900), (250, 1000)], LINE, 20); return d.out()


def cooler():                                                # water cooling rig: chrome box, coils, gauge, snowflake glow
    d = Draw(900, 1100); d.rrect(120, 200, 780, 1060, 50, fill=(200, 230, 250, 255), outline=LINE, width=16)
    for y in range(300, 700, 70): d.arc(450, y, 250, 30, 0, 180, (90, 160, 220, 255), 16)
    d.dot(650, 820, 90, WT); d.ellipse(650, 820, 90, 90, outline=LINE, width=12); d.stroke([(650, 820), (700, 770)], RED, 10)
    for a in range(0, 180, 30): d.stroke([(250 + 90 * math.cos(math.radians(a)), 140 + 90 * math.sin(math.radians(a))), (250 - 90 * math.cos(math.radians(a)), 140 - 90 * math.sin(math.radians(a)))], CYAN, 14)
    shine(d, 160, 260, 600); eyes(d, 400, 860, 0.8, 'happy'); return d.out()


def freon():                                                 # Freon canister crossed out in red
    d = Draw(600, 900); d.rrect(120, 180, 480, 860, 60, fill=(120, 200, 240, 255), outline=LINE, width=16); d.rrect(230, 80, 370, 200, 20, fill=(150, 150, 160, 255), outline=LINE, width=12)
    d.rect(124, 420, 476, 560, WT); shine(d, 150, 230, 560); d.stroke([(60, 160), (540, 880)], RED, 60); d.stroke([(540, 160), (60, 880)], RED, 60); return d.out()


def mop():                                                   # mop + bucket with a sleepy face
    d = Draw(700, 1200); d.stroke([(420, 40), (330, 800)], (200, 150, 90, 255), 36)
    for k in range(9): d.stroke([(330, 790), (230 + k * 25, 980)], (240, 240, 230, 255), 18)
    d.poly([(380, 860), (680, 860), (640, 1180), (420, 1180)], fill=(90, 150, 230, 255), outline=LINE, width=16); d.ellipse(530, 860, 150, 30, fill=WATER, outline=LINE, width=10)
    eyes(d, 530, 1000, 0.55, 'sad'); return d.out()


def protos():                                                # seven years of prototypes: pipes, bottles, pumps on a board
    d = Draw(1300, 700); d.rrect(30, 520, 1270, 680, 30, fill=(110, 80, 70, 255), outline=LINE, width=14)
    cols = (CYAN, PINK, YEL, LIME, ORNG, VIO, (240, 240, 250, 255))
    for k in range(7):
        x = 110 + k * 175; c = cols[k]; h = 200 + (k * 53) % 160
        d.rrect(x - 50, 520 - h, x + 50, 520, 24, fill=c, outline=LINE, width=10); d.stroke([(x, 520 - h), (x + 60, 500 - h)], LINE, 10)
    eyes(d, 650, 420, 0.5, 'happy'); return d.out()


def contract():                                              # licence contract (no words): lines, signature swirl, red wax seal
    d = Draw(760, 980); d.rrect(30, 30, 730, 950, 24, fill=(255, 250, 236, 255), outline=LINE, width=16)
    for y in range(130, 650, 60): d.rect(90, y, 670, y + 16, (190, 186, 176, 255))
    d.arc(280, 760, 160, 50, 180, 360, (40, 60, 160, 255), 12); d.arc(400, 760, 100, 40, 0, 180, (40, 60, 160, 255), 12)
    d.dot(590, 800, 90, RED); star(d, 590, 800, 60, (255, 170, 160, 255), 6); return d.out()


def boxpd(name):                                             # 1990 toy box: window with the blaster, burst + name band
    d = Draw(1000, 1100); d.rrect(40, 40, 960, 1060, 30, fill=(40, 30, 110, 255), outline=LINE, width=18)
    for k in range(9): d.stroke([(80 + k * 110, 60), (40 + k * 110, 1040)], (60, 50, 150, 255), 30)
    d.rrect(120, 330, 880, 820, 30, fill=(200, 240, 255, 255), outline=LINE, width=14); g = soaker('happy').resize((700, 373)); d.out()
    d.rrect(80, 860, 920, 1020, 24, fill=ORNG if name == 'POWER DRENCHER' else LIME, outline=LINE, width=14)
    d.text(500, 940, name, LA.fit(name, 120, 780), WT, stroke=7, stroke_fill=LINE)
    for k in range(10): a = math.radians(k * 36); d.stroke([(500, 190), (500 + 300 * math.cos(a), 190 + 120 * math.sin(a))], YEL, 30)
    d.ellipse(500, 190, 220, 100, fill=PINK, outline=LINE, width=12); im = d.out(); im.alpha_composite(g, (150, 390)); return im


def cash():                                                  # stacks of green bills with a face
    d = Draw(1100, 800)
    for k, (x, y) in enumerate(((300, 560), (560, 600), (820, 560), (430, 380), (690, 380), (560, 200))):
        d.rrect(x - 150, y - 80, x + 150, y + 80, 16, fill=(110, 200, 120, 255), outline=LINE, width=12); d.rect(x - 30, y - 80, x + 30, y + 80, (250, 236, 170, 255)); d.ellipse(x, y, 50, 40, outline=(40, 120, 60, 255), width=8)
    eyes(d, 560, 600, 0.5, 'happy'); return d.out()


def coins():                                                 # a gold mountain of coins
    d = Draw(1300, 900)
    for row in range(7):
        n = 8 - row
        for k in range(n): x, y = 650 + (k - (n - 1) / 2) * 150, 820 - row * 105; d.ellipse(x, y, 78, 40, fill=(255, 200, 50, 255), outline=LINE, width=8); d.ellipse(x, y - 6, 50, 22, fill=(255, 230, 120, 255))
    star(d, 650, 70, 60, WT, 6); return d.out()


def shadowkid():                                             # the open loop: a violet silhouette of a kid holding something, big "?"
    d = Draw(700, 1100); c = (90, 50, 160, 230)
    d.dot(350, 260, 170, c); d.rrect(200, 400, 500, 820, 80, fill=c); d.rect(230, 800, 320, 1080, c); d.rect(380, 800, 470, 1080, c); d.rrect(60, 500, 660, 600, 40, fill=c)
    d.text(350, 270, '?', 260, YEL, stroke=12, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def bath80(path):                                            # 1982 bathroom: orange + teal tiles, round mirror, rocket poster, rubber duck
    im = sky((255, 150, 80), (255, 200, 140), 1.0); d = Draw(W2, H2)
    for y in range(0, 940, 100):
        for x in range((y // 100) % 2 * 100, W2, 200): d.rect(x, y, x + 100, y + 100, (255, 176, 110, 255))
    d.rect(0, 560, W2, 600, TEAL); d.rect(0, 600, W2, 940, (60, 200, 190, 255))
    for x in range(0, W2, 100): d.stroke([(x, 600), (x, 940)], (40, 170, 160, 255), 6)
    d.ellipse(1200, 300, 220, 190, fill=(210, 240, 250, 255), outline=(250, 230, 200, 255), width=24)
    d.rrect(360, 160, 640, 520, 14, fill=NAVY, outline=WT, width=14); d.poly([(500, 200), (560, 330), (440, 330)], fill=RED); d.rect(460, 330, 540, 460, WT); [d.dot(x, y, 6, WT) for x, y in ((400, 220), (600, 260), (420, 470), (590, 480))]
    d.rrect(1850, 140, 2150, 520, 30, fill=(140, 230, 255, 255), outline=WT, width=20)
    fl(d, (70, 180, 200, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 300, (255, 255, 240, 90), 60); im.convert('RGB').save(path)


def jpl(path):                                               # JPL control room at night: navy walls, giant Jupiter screen, cyan consoles
    im = sky((20, 30, 90), (50, 70, 160), 1.0); d = Draw(W2, H2)
    d.rrect(700, 80, 1700, 560, 20, fill=(10, 20, 50, 255), outline=CYAN, width=16); d.dot(1200, 320, 190, (236, 196, 150, 255))
    for k, y in enumerate(range(170, 480, 50)): d.ellipse(1200, y, 190 - abs(y - 320) * 0.5, 14, fill=((200, 130, 90, 255), (250, 226, 196, 255))[k % 2])
    for x in (150, 1850): d.rrect(x, 120, x + 400, 520, 16, fill=(10, 20, 50, 255), outline=(255, 90, 180, 255), width=12); d.stroke([(x + 30, 400), (x + 120, 300), (x + 220, 360), (x + 370, 200)], LIME, 10)
    for x in range(0, W2, 300): d.rrect(x + 20, 640, x + 280, 760, 20, fill=(60, 80, 150, 255), outline=LINE, width=8); [d.dot(x + 60 + k * 50, 690, 12, (CYAN, YEL, PINK, LIME)[k]) for k in range(4)]
    fl(d, (40, 50, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 320, 420, (120, 220, 255, 90), 80); im.convert('RGB').save(path)


def space(path):                                             # deep violet space, star field, nebula swirl, Io + Europa dots
    im = sky((50, 20, 110), (120, 50, 170), 1.0); d = Draw(W2, H2); r = np.random.RandomState(4)
    for _ in range(300): d.dot(r.randint(0, W2), r.randint(0, 940), r.choice([3, 4, 6]), (255, 250, 230, 230))
    for x, y, rr, c in ((400, 300, 40, (250, 220, 120, 255)), (1900, 200, 30, (220, 230, 250, 255)), (2100, 700, 24, (230, 180, 140, 255))): d.dot(x, y, rr, c)
    fl(d, (60, 30, 110, 255)); im.alpha_composite(d.out()); glow(im, 700, 500, 600, (255, 100, 200, 70), 140); glow(im, 1800, 400, 500, (80, 200, 255, 60), 140); im.convert('RGB').save(path)


def homelab(path):                                           # icy home lab: pale-blue walls, frost window, copper pipes, snowflakes
    im = sky((120, 190, 240), (200, 236, 255), 1.0); d = Draw(W2, H2)
    win(d, 1600, 150, 2100, 560, (230, 246, 255, 255)); [d.dot(x, y, 30, WT) for x, y in ((1650, 520), (1750, 540), (2050, 530))]
    for y in (240, 300): d.stroke([(0, y), (1500, y)], (210, 130, 80, 255), 22)
    for k in range(18): x, y = (k * 431) % W2, 80 + (k * 197) % 650; [d.stroke([(x - 30 * math.cos(math.radians(a)), y - 30 * math.sin(math.radians(a))), (x + 30 * math.cos(math.radians(a)), y + 30 * math.sin(math.radians(a)))], WT, 6) for a in (0, 60, 120)]
    d.rrect(200, 420, 800, 620, 20, fill=(240, 250, 255, 255), outline=(150, 190, 220, 255), width=12)
    fl(d, (150, 200, 230, 255)); im.alpha_composite(d.out()); glow(im, 1850, 350, 350, (255, 255, 255, 100), 70); im.convert('RGB').save(path)


def office(path):                                            # 80s engineering office: warm beige, blueprints, green desk lamps, wet-floor shine
    im = sky((230, 200, 150), (250, 226, 180), 1.0); d = Draw(W2, H2)
    for x in (200, 900, 1600): d.rrect(x, 150, x + 500, 500, 10, fill=(60, 110, 200, 255), outline=WT, width=10); [d.stroke([(x + 40, y), (x + 460, y)], (180, 210, 255, 255), 4) for y in range(200, 480, 50)]; d.ellipse(x + 250, 330, 120, 80, outline=WT, width=6)
    for x in (500, 1300, 2100): d.stroke([(x, 600), (x, 720)], LINE, 10); d.chord(x, 600, 90, 60, 180, 360, fill=(40, 150, 90, 255), outline=LINE, width=8)
    d.rect(0, 720, W2, 940, (150, 110, 80, 255)); d.stroke([(0, 720), (W2, 720)], LINE, 10)
    fl(d, (200, 170, 130, 255)); im.alpha_composite(d.out()); glow(im, 1300, 650, 300, (255, 240, 180, 90), 60); im.convert('RGB').save(path)


def garage(path):                                            # neon garage workshop at night: pegboard, magenta + cyan neon tubes, tools
    im = sky((60, 30, 80), (110, 50, 120), 1.0); d = Draw(W2, H2)
    for x in range(40, W2, 60):
        for y in range(40, 700, 60): d.dot(x, y, 6, (90, 60, 110, 255))
    d.rrect(150, 100, 1100, 130, 14, fill=(255, 90, 200, 255)); d.rrect(1300, 160, 2250, 190, 14, fill=CYAN)
    for x, c in ((300, YEL), (500, RED), (700, LIME), (1500, ORNG), (1750, CYAN), (2000, PINK)): d.stroke([(x, 300), (x, 520)], c, 20); d.rrect(x - 40, 250, x + 40, 320, 10, fill=(200, 200, 210, 255), outline=LINE, width=6)
    fl(d, (70, 60, 90, 255)); im.alpha_composite(d.out()); glow(im, 620, 115, 520, (255, 90, 200, 110), 60); glow(im, 1780, 175, 520, (60, 220, 255, 110), 60); im.convert('RGB').save(path)


def memphis(path):                                           # 1989 toy-company office: Memphis squiggles, pink + yellow + teal shapes
    im = sky((255, 190, 220), (255, 230, 240), 1.0); d = Draw(W2, H2); r = np.random.RandomState(2)
    for k in range(40):
        x, y, t = r.randint(0, W2), r.randint(0, 900), k % 4; c = (TEAL, YEL, VIO, CYAN)[k % 4]
        if t == 0: d.poly([(x, y - 40), (x + 40, y + 30), (x - 40, y + 30)], fill=c, outline=LINE, width=6)
        elif t == 1: d.dot(x, y, 30, c)
        elif t == 2: d.stroke([(x - 60 + i * 20, y + (15 if i % 2 else -15)) for i in range(7)], c, 10)
        else: d.rect(x - 30, y - 30, x + 30, y + 30, c)
    win(d, 1700, 150, 2200, 560, (120, 210, 255, 255))
    fl(d, (60, 190, 180, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def toystore(path):                                          # 1990 toy aisle: tall shelves of bright boxes, neon strips, balloons
    im = sky((255, 230, 60), (255, 246, 160), 1.0); d = Draw(W2, H2)
    for sx in (0, 1300):
        for row in range(4):
            y = 120 + row * 190; d.rect(sx, y + 150, sx + 1100, y + 170, (120, 80, 60, 255))
            for k in range(8): d.rrect(sx + 20 + k * 135, y + 10, sx + 130 + k * 135, y + 150, 10, fill=(PINK, CYAN, LIME, ORNG, VIO, RED)[(k + row) % 6], outline=LINE, width=6)
    for x, c in ((1180, RED), (1230, CYAN), (1210, PINK)): d.dot(x, 200, 60, c); d.stroke([(x, 260), (1200, 560)], LINE, 4)
    fl(d, (240, 240, 250, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def vault(path):                                             # money vault: emerald walls, big round vault door, gold glow, falling bills
    im = sky((20, 110, 80), (60, 170, 120), 1.0); d = Draw(W2, H2)
    d.dot(1900, 450, 330, (190, 196, 206, 255)); d.ellipse(1900, 450, 330, 330, outline=LINE, width=16); d.ellipse(1900, 450, 220, 220, outline=(120, 126, 140, 255), width=20)
    for a in range(0, 360, 60): d.stroke([(1900, 450), (1900 + 120 * math.cos(math.radians(a)), 450 + 120 * math.sin(math.radians(a)))], (90, 96, 110, 255), 18)
    r = np.random.RandomState(6)
    for _ in range(30): x, y = r.randint(0, 1500), r.randint(0, 900); d.poly([(x, y), (x + 80, y + 20), (x + 70, y + 60), (x - 10, y + 40)], fill=(130, 220, 140, 255), outline=LINE, width=4)
    fl(d, (30, 90, 70, 255)); im.alpha_composite(d.out()); glow(im, 800, 600, 500, (255, 220, 100, 90), 100); im.convert('RGB').save(path)


def backyard(path):                                          # sunset backyard: hot pink-orange sky, pool, palms, sprinkler arcs, fence
    im = sky((255, 90, 140), (255, 200, 100), 1.0); d = Draw(W2, H2)
    d.dot(1200, 640, 260, (255, 236, 140, 255)); d.rect(0, 640, W2, 940, (255, 160, 120, 255))
    for x in range(0, W2, 70): d.rect(x, 560, x + 50, 760, (255, 250, 236, 255)); d.stroke([(x, 560), (x + 50, 560)], LINE, 4)
    for x in (250, 2150): d.stroke([(x, 900), (x + 40, 300)], (120, 70, 50, 255), 30); [d.ellipse(x + 40 + 150 * math.cos(math.radians(a)), 300 + 60 * math.sin(math.radians(a)), 150, 40, fill=(40, 160, 90, 255), outline=LINE, width=6) for a in (0, 70, 150, 220, 290)]
    d.rrect(700, 800, 1700, 930, 60, fill=(60, 210, 240, 255), outline=WT, width=16)
    for x in (900, 1500): d.arc(x, 800, 260, 300, 200, 340, WATER, 10)
    fl(d, (110, 200, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 640, 500, (255, 230, 160, 110), 100); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = MA.head, LA.body
    for ch in ('lonnie', 'eng', 'exec', 'kidc', 'kidd'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked')]
    multi = dict(soaker={'default': soaker(), 'shocked': soaker('shocked')}, blast={'default': blast()}, sink={'default': sink(), 'on': sink(True)}, galileo={'default': galileo()},
                 jupiter={'default': jupiter(), 'shocked': jupiter('shocked')}, rocket={'default': rocket()}, cooler={'default': cooler()}, freon={'default': freon()}, mop={'default': mop()},
                 protos={'default': protos()}, contract={'default': contract()}, boxpd={'default': boxpd('POWER DRENCHER')}, cash={'default': cash()}, coins={'default': coins()},
                 shadowkid={'default': shadowkid()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    P_ = lambda a, b, bg, w=1000, bs=130, ss=130, bd=GOLDL: plaque(a, b, bg, WHITE, w, border=bd, bs=bs, ss=ss, sc=bd)
    cards = dict(hookc=M.bigneon('ROCKET SCIENTIST', 'MADE SUPER SOAKER!', 1000, YEL, CYAN),
                 accident=stamp('BY ACCIDENT!', 860, RED, 150, -4),
                 wait=stamp('WAIT FOR IT...', 860, VIO, 120, 4),
                 lonniec=P_('LONNIE JOHNSON', 'NASA JPL', (40, 120, 230, 255), 1000, 130, 160, WT),
                 galileoc=M.bigneon('GALILEO', 'PROBE TO JUPITER', 1000, YEL, CYAN),
                 serious=stamp('SERIOUS WORK.', 880, (60, 70, 100, 255), 130, 3),
                 y1982=M.cal('AT HOME', '1982', ORNG),
                 cooling=P_('NEW COOLING SYSTEM', 'RUNS ON WATER', (40, 150, 220, 255), 1000, 110, 140, WT),
                 freonc=stamp('NOT FREON!', 800, RED, 150, -3),
                 nozzlec=P_('HOMEMADE NOZZLE', 'ON THE SINK', TEAL, 1000, 120, 140, WT),
                 turnon=stamp('TURNS IT ON...', 880, ORNG, 130, 3),
                 blastc=M.bigneon('WHOOSH!', 'ACROSS THE ROOM!', 1000, CYAN, PINK),
                 mopc=P_('MOST ENGINEERS:', 'MOP THE FLOOR', (150, 110, 80, 255), 1000, 120, 140),
                 kidslove=M.bigneon('KIDS WOULD', 'LOVE THIS!', 900, YEL, LIME),
                 years7=P_('7 YEARS', 'OF WORK', VIO, 860, 190, 150, PINK),
                 pgun=P_('PRESSURIZED', 'WATER GUN!', (255, 90, 120, 255), 960, 150, 160, YEL),
                 y1989=M.cal('LICENSED', '1989', PINK),
                 larami=P_('LARAMI', 'TOY COMPANY', TEAL, 900, 190, 130, YEL),
                 licensed=stamp('LICENSED!', 800, (40, 160, 90, 255), 150, -4),
                 y1990=M.cal('LAUNCH', '1990', (40, 120, 230, 255)),
                 renamed=stamp('RENAMED!', 780, VIO, 160, 4),
                 soakerc=M.bigneon('SUPER', 'SOAKER!', 860, CYAN, YEL),
                 total=stamp('TOTAL SALES TODAY?', 1000, (40, 120, 80, 255), 110, -3),
                 billion=M.bigneon('CLOSE TO', 'A BILLION!', 920, YEL, LIME),
                 cool=P_('A BETTER WAY TO', 'COOL THINGS DOWN', (60, 170, 230, 255), 1000, 120, 120, WT),
                 nailed=stamp('HE NAILED IT!', 880, PINK, 140, -4),
                 hands=P_('IT FITS IN', "A KID'S HANDS!", ORNG, 940, 150, 140, WT))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (120, 90, 170), (106, 78, 156))
    CE.tiles(T('tile80.jpg'), (60, 200, 190), (255, 170, 110)); CE.tiles(T('navytile.jpg'), (70, 90, 160), (60, 78, 146)); M.sandtex(T('starfloor.jpg'), (80, 50, 140), (230, 220, 255), seed=7)
    CE.tiles(T('icetile.jpg'), (200, 230, 250), (180, 214, 240)); CE.tiles(T('carpet.jpg'), (170, 130, 100), (156, 118, 90)); CE.tiles(T('concrete.jpg'), (110, 100, 130), (96, 88, 116))
    CE.tiles(T('memphis.jpg'), (60, 190, 180), (255, 214, 60)); CE.tiles(T('storefloor.jpg'), (240, 240, 250), (220, 220, 236)); CE.tiles(T('vaultfloor.jpg'), (40, 120, 90), (30, 104, 76))
    M.sandtex(T('lawn.jpg'), (110, 200, 100), (94, 180, 86))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(bath80=bath80, jpl=jpl, space=space, homelab=homelab, office=office, garage=garage, memphis=memphis, toystore=toystore, vault=vault, backyard=backyard)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
