#!/usr/bin/env python3
"""Assets for video 16 (A farm boy found a planet: Clyde Tombaugh, Pluto and New Horizons), drawn in code.
Cute cast: young Clyde (sandy quiff, freckles, straw hat, denim), old Clyde (white hair, round glasses, brown cardigan), Dad
(red farmer cap, moustache), Mom (bob, rose cardigan), the Lowell director (glasses, navy suit), the newsboy (cap), the NASA
engineer (white suit, teal band), two astronomers 2006 (green sweater / plum suit).
Props: the homemade telescope (with a face), crankshaft, cream separator, the 1910 car (with a face), sketch of Jupiter + Mars,
envelope, job-offer letter, mailbox, blink comparator, the two photo plates (dot jumps between faces a/b), Planet X (?), cute
Pluto with the heart (happy / shocked / sad), New Horizons probe, the little capsule, the rocket, the 1930 newspaper, the
textbook with Pluto crossed out, yellow voting cards.
Fourteen sets: FM Kansas farm at night (hook + loop), HL hailstorm field, WB lantern workshop barn, AT attic at night, MB mailbox
at sunset, LO Lowell dome at dusk, PX teal nebula with Planet X, BC red-lamp blink room, NW sunny 1930 news street, LC bright
launch day, CR white clean room, SP icy Pluto flyby, VT blue voting hall, TX cream study desk.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import corrigan_assets as CA
import catseyes_assets as CE
import lordgta_assets as LA
import mco_assets as M
import mono_assets as MA
from assets_base import Draw, LINE, WHITE, H

ROOT = B.ROOT; RED, GOLD, GOLDL = LA.RED, LA.GOLD, M.GOLDL
dk, glow, plaque, stamp, neon, sky, W2, H2, fl, faceon = LA.dk, CE.glow, LA.plaque, LA.stamp, LA.neon, M.sky, M.W2, M.H2, MA.fl, MA.faceon
WT, LIME, PINK, CYAN, YEL, ORNG, TEAL, NAVY = (250, 250, 245, 255), (120, 230, 90, 255), (255, 90, 160, 255), (120, 220, 255, 255), (255, 206, 50, 255), (250, 140, 50, 255), (40, 170, 150, 255), (40, 60, 150, 255)
PLU, PLUD, HEART = (226, 196, 160, 255), (170, 130, 100, 255), (250, 236, 220, 255)
LA.NEW.update({
    'clyde': dict(sk=0, style='quiff', hair=(214, 170, 90, 255), suit=(70, 120, 190, 255), shade=(54, 96, 160, 255), body='denim', freck=1, hat='straw'),
    'clydeo': dict(sk=0, style='part', hair=(238, 238, 242, 255), suit=(160, 116, 80, 255), shade=(130, 92, 60, 255), body='cardigan', glasses=1),
    'dad': dict(sk=0, style='side', hair=(110, 80, 50, 255), suit=(170, 70, 56, 255), shade=(140, 54, 42, 255), body='sweater', stache=(110, 80, 50, 255), hat='cap2'),
    'mom': dict(sk=0, style='bob', hair=(110, 60, 40, 255), suit=(214, 100, 130, 255), shade=(180, 76, 104, 255), body='cardigan', band=YEL),
    'astro': dict(sk=1, style='side', hair=(60, 50, 40, 255), suit=NAVY, shade=(30, 44, 116, 255), body='suit', tie=GOLD, glasses=2, stache=(60, 50, 40, 255)),
    'newsboy': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=(214, 130, 60, 255), shade=(180, 104, 44, 255), body='sweater', hat='cap'),
    'eng': dict(sk=1, style='bob', hair=(40, 30, 40, 255), suit=(236, 240, 246, 255), shade=(200, 206, 220, 255), body='suit', tie=(60, 120, 220, 255), band=CYAN),
    'v1': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=(90, 150, 100, 255), shade=(70, 124, 80, 255), body='sweater', glasses=1),
    'v2': dict(sk=0, style='bob', hair=(200, 80, 50, 255), suit=(130, 90, 180, 255), shade=(104, 70, 150, 255), body='suit', tie=YEL, band=WT),
})


def head(char, expr):
    im = MA.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']
    if c.get('hat') == 'straw':                              # straw hat: wide brim, red band, weave lines
        d.ellipse(cx, cy - R + 60, R + 110, 46, fill=(240, 206, 110, 255), outline=LINE, width=14); d.chord(cx, cy - R + 56, R - 20, R - 10, 180, 360, fill=(240, 206, 110, 255), outline=LINE, width=14)
        d.rect(cx - R + 26, cy - R + 18, cx + R - 26, cy - R + 46, (220, 60, 60, 255))
        for k in range(5): d.stroke([(cx - R + 60 + k * 70, cy - R - 60), (cx - R + 40 + k * 70, cy - R + 10)], (200, 160, 70, 255), 6)
    elif c.get('hat') == 'cap2':                             # red farmer cap with a peak
        d.chord(cx, cy - R + 70, R + 10, R - 40, 180, 360, fill=(220, 60, 60, 255), outline=LINE, width=14); d.ellipse(cx + 130, cy - R + 76, 140, 30, fill=(190, 40, 40, 255), outline=LINE, width=12)
        d.dot(cx, cy - R - 26, 18, (190, 40, 40, 255))
    im.alpha_composite(d.out()); return im


# ------------------------------------------------------------------ props
def star(d, x, y, r, col): d.poly([(x + (r if k % 2 == 0 else r * 0.45) * math.cos(math.radians(k * 36 - 90)), y + (r if k % 2 == 0 else r * 0.45) * math.sin(math.radians(k * 36 - 90))) for k in range(10)], fill=col, outline=LINE, width=6)


def rot(cx, cy, t): r = math.radians(t); return lambda x, y: (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))


def scope():                                                 # homemade telescope: tilted tube with a face, wooden tripod, crank wheel
    d = Draw(900, 1100); P = rot(470, 360, -32)
    for a, b in (((470, 460), (200, 1080)), ((470, 460), (740, 1080)), ((470, 460), (470, 1080))): d.stroke([a, b], LINE, 40); d.stroke([a, b], (170, 110, 60, 255), 24)
    d.poly([P(-360, -90), P(330, -90), P(330, 90), P(-360, 90)], fill=(90, 120, 160, 255), outline=LINE, width=16)
    d.poly([P(300, -120), P(400, -120), P(400, 120), P(300, 120)], fill=(200, 160, 70, 255), outline=LINE, width=14)
    for k in (-200, -40): d.poly([P(k, -100), P(k + 30, -100), P(k + 30, 100), P(k, 100)], fill=(200, 160, 70, 255), outline=LINE, width=8)
    d.dot(470, 470, 70, (130, 130, 140, 255)); d.ellipse(470, 470, 70, 70, outline=LINE, width=12)
    for k in range(6): a = math.radians(k * 60); d.stroke([(470, 470), (470 + 60 * math.cos(a), 470 + 60 * math.sin(a))], LINE, 6)
    cx, cy = P(60, 0); faceon(d, cx, cy, 0.7, 'happy'); return d.out()


def crank():                                                 # crankshaft: steel zig-zag with round journals
    d = Draw(1000, 460); pts = [(60, 230), (200, 230), (240, 110), (380, 110), (420, 230), (580, 230), (620, 350), (760, 350), (800, 230), (940, 230)]
    d.stroke(pts, LINE, 70); d.stroke(pts, (170, 176, 190, 255), 46)
    for x, y in pts[::2] + [pts[-1]]: d.dot(x, y, 44, (210, 214, 226, 255)); d.ellipse(x, y, 44, 44, outline=LINE, width=10)
    d.stroke([(250, 120), (370, 120)], (240, 244, 250, 255), 10); return d.out()


def separator():                                             # cream separator: bowl, spouts, crank handle, pedestal
    d = Draw(760, 1000); d.poly([(300, 980), (460, 980), (420, 560), (340, 560)], fill=(130, 60, 50, 255), outline=LINE, width=14)
    d.ellipse(380, 980, 220, 30, fill=(110, 50, 40, 255), outline=LINE, width=12); d.chord(380, 380, 240, 200, 0, 180, fill=(200, 206, 220, 255), outline=LINE, width=16)
    d.ellipse(380, 380, 240, 50, fill=(240, 244, 250, 255), outline=LINE, width=14)
    for sg in (-1, 1): d.poly([(380 + sg * 150, 480), (380 + sg * 330, 520), (380 + sg * 330, 560), (380 + sg * 150, 540)], fill=(200, 206, 220, 255), outline=LINE, width=10)
    d.stroke([(560, 640), (700, 640), (700, 760)], LINE, 24); d.dot(700, 780, 34, (220, 60, 60, 255)); faceon(d, 380, 440, 0.7, 'happy'); return d.out()


def car():                                                   # 1910 car: boxy red body, spoked wheels, brass lamp, face on the radiator
    d = Draw(1400, 880); d.rrect(160, 300, 1240, 640, 40, fill=(200, 50, 50, 255), outline=LINE, width=16); d.rrect(640, 120, 1100, 330, 30, fill=(60, 50, 60, 255), outline=LINE, width=14)
    d.rrect(160, 280, 420, 640, 30, fill=(230, 190, 80, 255), outline=LINE, width=14)
    for x in (330, 1030):
        d.dot(x, 680, 170, (60, 50, 60, 255)); d.ellipse(x, 680, 170, 170, outline=LINE, width=14); d.dot(x, 680, 110, (240, 220, 190, 255))
        for k in range(8): a = math.radians(k * 45); d.stroke([(x, 680), (x + 105 * math.cos(a), 680 + 105 * math.sin(a))], LINE, 8)
        d.dot(x, 680, 26, (230, 190, 80, 255))
    d.dot(110, 330, 60, (255, 230, 140, 255)); d.ellipse(110, 330, 60, 60, outline=LINE, width=12); faceon(d, 290, 420, 0.75, 'happy'); return d.out()


def sketch():                                                # pencil sketch page: striped Jupiter + red Mars
    d = Draw(900, 700); d.poly([(30, 40), (860, 20), (870, 670), (40, 680)], fill=(252, 248, 236, 255), outline=LINE, width=14)
    d.dot(290, 340, 190, (240, 200, 150, 255)); d.ellipse(290, 340, 190, 190, outline=LINE, width=10)
    for y, c in ((260, (200, 120, 80)), (320, (220, 160, 110)), (390, (190, 110, 70))): d.rect(110, y, 470, y + 30, c + (255,))
    d.ellipse(290, 340, 190, 190, outline=LINE, width=10); d.ellipse(350, 400, 40, 24, fill=(200, 80, 60, 255))
    d.dot(670, 360, 110, (220, 100, 60, 255)); d.ellipse(670, 360, 110, 110, outline=LINE, width=10); d.ellipse(640, 330, 40, 22, fill=(170, 70, 40, 255))
    d.stroke([(640, 560), (820, 620)], (255, 200, 60, 255), 22); return d.out()


def envelope():
    d = Draw(800, 520); d.rrect(20, 20, 780, 500, 20, fill=(250, 240, 220, 255), outline=LINE, width=14); d.stroke([(20, 30), (400, 300), (780, 30)], LINE, 12)
    d.rect(600, 60, 720, 180, (220, 70, 70, 255)); d.dot(660, 120, 36, (255, 230, 140, 255)); return d.out()


def letter():                                                # job offer: gold star seal, header band
    d = Draw(720, 920); d.poly([(40, 40), (680, 40), (680, 880), (40, 880)], fill=WT, outline=LINE, width=14); d.rect(100, 90, 620, 190, (40, 60, 150, 255))
    d.dot(360, 140, 40, (255, 220, 80, 255))
    for y in range(280, 700, 70): d.rect(110, y, 610, y + 16, (170, 176, 196, 255))
    d.dot(540, 770, 80, (255, 200, 60, 255)); d.ellipse(540, 770, 80, 80, outline=LINE, width=10); star(d, 540, 770, 56, (255, 240, 150, 255)); return d.out()


def mailbox():
    d = Draw(700, 1100); d.rect(320, 420, 380, 1090, (130, 90, 60, 255)); d.poly([(320, 420), (380, 420), (380, 1090), (320, 1090)], outline=LINE, width=10)
    d.rrect(90, 160, 610, 460, 120, fill=(110, 150, 200, 255), outline=LINE, width=16); d.rect(90, 300, 610, 460, (110, 150, 200, 255)); d.poly([(90, 300), (610, 300), (610, 460), (90, 460)], outline=LINE, width=16)
    d.stroke([(560, 300), (560, 80)], LINE, 20); d.poly([(560, 80), (680, 110), (560, 150)], fill=(230, 50, 50, 255), outline=LINE, width=8); faceon(d, 300, 330, 0.7, 'happy'); return d.out()


def plates(b=False):                                         # two photo plates of the same sky: the one dot jumps
    d = Draw(1400, 700); r = np.random.RandomState(11)
    for x0 in (40, 740):
        d.rrect(x0, 40, x0 + 620, 660, 20, fill=(20, 26, 44, 255), outline=(200, 200, 210, 255), width=16)
        rr = np.random.RandomState(11)
        for _ in range(70): d.dot(x0 + 40 + rr.randint(540), 80 + rr.randint(540), rr.choice([4, 6, 9]), (240, 244, 255, 255))
    for x0, dx in ((40, 0), (740, 90 if not b else 0)):
        px, py = x0 + 330 + (0 if not b else 90) + (dx if x0 == 740 else 0) * 0, 330
    ax = 370 if not b else 460; bx = 1070 if not b else 1160
    for x in (ax, bx): d.dot(x, 330, 14, (255, 230, 120, 255)); d.ellipse(x, 330, 46, 46, outline=(255, 80, 80, 255), width=8)
    return d.out()


def comparator():                                            # blink comparator: olive desk machine, eyepiece, two plate frames, knobs
    d = Draw(1000, 1100); d.rrect(100, 600, 900, 1080, 30, fill=(110, 130, 100, 255), outline=LINE, width=16)
    d.rrect(150, 240, 850, 620, 30, fill=(140, 160, 120, 255), outline=LINE, width=16)
    for x in (200, 520): d.rrect(x, 300, x + 280, 560, 10, fill=(30, 36, 56, 255), outline=LINE, width=10)
    d.poly([(460, 240), (540, 240), (580, 60), (420, 60)], fill=(60, 60, 70, 255), outline=LINE, width=12); d.ellipse(500, 60, 90, 30, fill=(40, 40, 50, 255), outline=LINE, width=10)
    for x in (260, 500, 740): d.dot(x, 760, 40, (230, 190, 80, 255)); d.ellipse(x, 760, 40, 40, outline=LINE, width=8)
    faceon(d, 500, 900, 0.9, 'happy'); return d.out()


def planetx():
    d = Draw(900, 900); d.dot(450, 450, 400, (110, 70, 170, 255)); d.ellipse(450, 450, 400, 400, outline=LINE, width=16)
    for u, v, s in ((-0.4, -0.3, 0.2), (0.35, 0.3, 0.26), (0.1, -0.5, 0.12)): d.ellipse(450 + u * 400, 450 + v * 400, s * 400, s * 240, fill=(90, 54, 150, 255))
    d.text(450, 470, '?', 520, (255, 230, 120, 255), stroke=14, stroke_fill=LINE); return d.out()


def pluto(face='happy'):                                     # cute Pluto with the big pale heart
    d = Draw(900, 900); d.dot(450, 450, 400, PLU); d.ellipse(450, 450, 400, 400, outline=LINE, width=16)
    for u, v, s in ((-0.55, -0.45, 0.16), (-0.6, 0.2, 0.12), (0.5, -0.55, 0.1)): d.ellipse(450 + u * 400, 450 + v * 400, s * 400, s * 260, fill=PLUD)
    hx, hy = 560, 600; d.poly([(hx, hy + 170)] + [(hx + 160 * math.sin(math.radians(a)) * (1 if a < 180 else 1), hy - 40 - 110 * math.cos(math.radians(a))) for a in range(-150, 151, 15)], fill=HEART)
    d.dot(hx - 75, hy - 40, 85, HEART); d.dot(hx + 75, hy - 40, 85, HEART)
    sh = face == 'shocked'
    for sg in (-1, 1):
        d.ellipse(360 + sg * 110, 380, 58, 74 if sh else 66, fill=WHITE, outline=LINE, width=12); d.dot(360 + sg * 110 + 8, 392, 26 if sh else 32, LINE); d.dot(360 + sg * 110 + 20, 372, 11, WHITE)
        d.ellipse(360 + sg * 200, 470, 46, 26, fill=(255, 130, 130, 190))
        if face == 'sad': d.stroke([(360 + sg * 60, 300), (360 + sg * 150, 320)], LINE, 12)
    if sh: d.ellipse(360, 500, 50, 60, fill=(120, 30, 40, 255), outline=LINE, width=12)
    elif face == 'sad': d.arc(360, 540, 60, 34, 200, 340, LINE, 14)
    else: d.chord(360, 480, 70, 56, 0, 180, fill=(120, 30, 40, 255), outline=LINE, width=12)
    return d.out()


def probe(face='happy'):                                     # New Horizons: gold triangle body, big white dish, RTG arm, thrusters
    d = Draw(1000, 900); d.stroke([(560, 640), (900, 820)], LINE, 34); d.stroke([(560, 640), (900, 820)], (150, 150, 160, 255), 20); d.dot(900, 820, 46, (90, 90, 100, 255))
    d.poly([(200, 460), (800, 460), (660, 760), (340, 760)], fill=(230, 180, 60, 255), outline=LINE, width=16)
    for k in range(4): d.stroke([(260 + k * 140, 480), (360 + k * 90, 740)], (200, 150, 40, 255), 6)
    d.chord(500, 440, 380, 300, 180, 360, fill=WT, outline=LINE, width=16); d.ellipse(500, 440, 380, 60, fill=(230, 234, 244, 255), outline=LINE, width=14); d.dot(500, 300, 30, (200, 200, 210, 255))
    faceon(d, 500, 590, 0.95, face); return d.out()


def capsule():
    d = Draw(500, 700); d.rrect(100, 120, 400, 640, 60, fill=(200, 206, 220, 255), outline=LINE, width=14); d.rrect(130, 60, 370, 150, 30, fill=(170, 176, 190, 255), outline=LINE, width=12)
    star(d, 250, 390, 110, (255, 200, 60, 255)); return d.out()


def rocket2(face='happy'):                                   # white Atlas-style rocket, orange stripe, side boosters, flame when 'fire'
    d = Draw(700, 1500)
    if face == 'fire':
        for k, c in enumerate(((255, 120, 40), (255, 210, 80), (255, 250, 200))): d.poly([(350 - 150 + k * 50, 1250), (350, 1500 - k * 70), (350 + 150 - k * 50, 1250)], fill=c + (255,))
    d.rrect(250, 160, 450, 1260, 40, fill=WT, outline=LINE, width=16); d.poly([(250, 200), (350, 20), (450, 200)], fill=(230, 100, 50, 255), outline=LINE, width=16)
    d.rect(250, 600, 450, 680, (230, 100, 50, 255))
    for sg in (-1, 1): d.rrect(350 + sg * 160 - 50, 760, 350 + sg * 160 + 50, 1240, 40, fill=(236, 236, 240, 255), outline=LINE, width=12)
    faceon(d, 350, 420, 0.75, 'happy'); return d.out()


def paper1930():
    d = Draw(900, 1100); d.poly([(40, 40), (860, 60), (850, 1070), (50, 1060)], fill=(246, 240, 222, 255), outline=LINE, width=14)
    d.rect(90, 90, 810, 220, (40, 40, 50, 255))
    d.dot(450, 520, 200, PLU); d.ellipse(450, 520, 200, 200, outline=LINE, width=10); d.ellipse(500, 580, 70, 56, fill=HEART)
    for y in range(780, 1020, 50): d.rect(100, y, 800, y + 16, (170, 166, 150, 255))
    return d.out()


def textbook():                                              # open textbook: the planet list, Pluto crossed out
    d = Draw(1400, 900); d.poly([(40, 120), (700, 60), (700, 860), (40, 820)], fill=(252, 248, 236, 255), outline=LINE, width=14); d.poly([(700, 60), (1360, 120), (1360, 820), (700, 860)], fill=(248, 244, 230, 255), outline=LINE, width=14)
    cols = [(180, 170, 160), (230, 200, 120), (90, 150, 230), (220, 100, 60), (230, 180, 120), (230, 210, 150), (150, 220, 230), (80, 120, 220), (226, 196, 160)]
    for k, c in enumerate(cols):
        x, y = (180 + (k % 5) * 110, 260 + (k // 5) * 260) if k < 5 else (860 + ((k - 5) % 2) * 220, 260 + ((k - 5) // 2) * 260)
        d.dot(x, y, 46 if k not in (4, 5) else 62, c + (255,)); d.ellipse(x, y, 46 if k not in (4, 5) else 62, 46 if k not in (4, 5) else 62, outline=LINE, width=8)
        if k < 8:
            for yy in (y + 80,): d.rect(x - 40, yy, x + 40, yy + 12, (170, 176, 196, 255))
    x, y = 1080, 520
    for a, b in (((x - 90, y - 90), (x + 90, y + 90)), ((x + 90, y - 90), (x - 90, y + 90))): d.stroke([a, b], LINE, 40); d.stroke([a, b], (230, 50, 50, 255), 24)
    return d.out()


def vcard():
    d = Draw(500, 640); d.rrect(30, 30, 470, 610, 20, fill=(255, 214, 60, 255), outline=LINE, width=14); d.rect(80, 110, 420, 140, (200, 160, 30, 255)); d.rect(80, 190, 340, 216, (200, 160, 30, 255)); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def farm(path):                                              # Kansas night: bright blue sky, Milky Way, a tiny Pluto glint, red barn, windmill, wheat
    im = sky((50, 76, 160), (110, 130, 200), 1.0); d = Draw(W2, H2); r = np.random.RandomState(5)
    for _ in range(260): d.dot(r.randint(0, W2), r.randint(0, 700), r.choice([3, 4, 6]), (255, 252, 230, 230))
    d.ellipse(1700, 200, 90, 90, fill=(250, 246, 220, 255)); d.dot(860, 240, 16, (255, 220, 170, 255))
    d.ellipse(1200, 980, 1500, 200, fill=(70, 120, 80, 255))
    d.poly([(260, 920), (260, 640), (420, 520), (580, 640), (580, 920)], fill=(200, 60, 50, 255), outline=LINE, width=12); d.rect(360, 760, 480, 920, (130, 40, 36, 255)); d.stroke([(360, 760), (480, 920)], WT, 8); d.stroke([(480, 760), (360, 920)], WT, 8)
    d.stroke([(2000, 920), (2040, 520), (2080, 920)], LINE, 14); d.dot(2040, 500, 22, LINE)
    for k in range(4): a = math.radians(k * 90 + 20); d.poly([(2040, 500), (2040 + 170 * math.cos(a) - 20 * math.sin(a), 500 + 170 * math.sin(a) + 20 * math.cos(a)), (2040 + 170 * math.cos(a) + 20 * math.sin(a), 500 + 170 * math.sin(a) - 20 * math.cos(a))], fill=(220, 220, 230, 255), outline=LINE, width=6)
    for x in range(0, W2, 26): d.stroke([(x, 940), (x + 6, 870 - (x * 7) % 40)], (230, 200, 110, 255), 8)
    fl(d, (150, 130, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 380, 700, (160, 180, 255, 60), 100); glow(im, 860, 240, 60, (255, 220, 170, 160), 16); glow(im, 1700, 200, 180, (240, 240, 210, 100), 40)
    im.convert('RGB').save(path)


def hail(path):                                              # hailstorm: grey-green sky, white hail streaks, flattened wheat, farmhouse
    im = sky((120, 140, 130), (170, 186, 170), 1.0); d = Draw(W2, H2); r = np.random.RandomState(3)
    for x in (300, 900, 1500, 2100): d.ellipse(x, 120, 380, 140, fill=(90, 104, 100, 255), outline=LINE, width=10)
    d.poly([(1700, 920), (1700, 620), (1900, 480), (2100, 620), (2100, 920)], fill=(236, 226, 200, 255), outline=LINE, width=12); d.rect(1840, 720, 1960, 920, (120, 90, 70, 255))
    for x in (1760, 2040): d.rect(x - 30, 680, x + 30, 740, (255, 230, 150, 255))
    for x in range(0, W2, 30): d.stroke([(x, 940), (x + 40, 900)], (180, 160, 90, 255), 8)
    for _ in range(240): x, y = r.randint(0, W2), r.randint(160, 930); d.dot(x, y, r.choice([5, 7, 9]), WT)
    fl(d, (130, 140, 100, 255)); im.alpha_composite(d.out()); glow(im, 1900, 700, 200, (255, 230, 160, 90), 40); im.convert('RGB').save(path)


def barn(path):                                              # workshop barn: plank walls, lantern glow, tool pegboard, hay loft, a big wheel
    im = sky((170, 110, 70), (196, 136, 90), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 112, 940, (190, 128, 84, 255)); d.stroke([(x, 0), (x, 940)], (140, 90, 56, 255), 8)
    d.rrect(900, 200, 1500, 600, 16, fill=(150, 104, 70, 255), outline=LINE, width=12)
    for k, (x, y) in enumerate(((980, 300), (1100, 300), (1240, 320), (1380, 300), (1000, 480), (1180, 470), (1360, 480))): d.stroke([(x, y - 60), (x, y + 60)], LINE, 16); d.dot(x, y - 70, 22, (170, 176, 190, 255))
    d.ellipse(400, 560, 200, 200, outline=LINE, width=24); d.ellipse(400, 560, 200, 200, outline=(150, 100, 60, 255), width=12)
    for k in range(8): a = math.radians(k * 45); d.stroke([(400, 560), (400 + 190 * math.cos(a), 560 + 190 * math.sin(a))], (150, 100, 60, 255), 10)
    d.poly([(1700, 0), (2400, 0), (2400, 240), (1700, 240)], fill=(230, 200, 110, 255)); d.stroke([(1700, 240), (2400, 240)], LINE, 10)
    d.stroke([(1950, 300), (1950, 380)], LINE, 8); d.rrect(1900, 380, 2000, 520, 20, fill=(255, 220, 130, 255), outline=LINE, width=10)
    fl(d, (150, 110, 70, 255)); im.alpha_composite(d.out()); glow(im, 1950, 450, 360, (255, 200, 110, 150), 60); im.convert('RGB').save(path)


def attic(path):                                             # attic at night: sloped roof, round window with Jupiter + Mars in the sky, lamp
    im = sky((120, 90, 130), (150, 116, 150), 1.0); d = Draw(W2, H2)
    d.poly([(0, 0), (700, 0), (0, 600)], fill=(110, 76, 90, 255)); d.poly([(2400, 0), (1700, 0), (2400, 600)], fill=(110, 76, 90, 255))
    d.dot(1200, 380, 280, (50, 70, 150, 255)); r = np.random.RandomState(2)
    for _ in range(50): d.dot(1200 + r.randint(-250, 250), 380 + r.randint(-250, 250), 4, WT)
    d.dot(1110, 330, 60, (240, 200, 150, 255)); d.dot(1300, 450, 34, (220, 100, 60, 255)); d.ellipse(1200, 380, 280, 280, outline=(230, 200, 140, 255), width=30)
    d.stroke([(920, 380), (1480, 380)], (230, 200, 140, 255), 14); d.stroke([(1200, 100), (1200, 660)], (230, 200, 140, 255), 14)
    for x, y in ((420, 420), (560, 560), (1900, 450)): d.rrect(x - 80, y - 60, x + 80, y + 60, 6, fill=(252, 248, 236, 255), outline=LINE, width=8); d.dot(x, y, 30, (240, 190, 130, 255))
    fl(d, (150, 110, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 380, 340, (150, 170, 255, 80), 60); im.convert('RGB').save(path)


def mailroad(path):                                          # sunset farm road: pink-gold sky, telephone poles, fence, dirt road
    im = sky((250, 140, 170), (255, 210, 130), 1.0); d = Draw(W2, H2); d.dot(1500, 760, 220, (255, 236, 160, 255))
    d.ellipse(600, 960, 900, 160, fill=(200, 170, 90, 255)); d.ellipse(1900, 970, 800, 150, fill=(180, 160, 90, 255))
    for x in range(100, W2, 500): d.stroke([(x, 940), (x, 300)], LINE, 18); d.stroke([(x - 80, 340), (x + 80, 340)], LINE, 12)
    for x in range(100, W2 - 500, 500): d.stroke([(x, 350), (x + 250, 390), (x + 500, 350)], LINE, 4)
    d.poly([(1100, 940), (1300, 940), (1220, 760), (1180, 760)], fill=(220, 180, 130, 255))
    fl(d, (190, 150, 100, 255)); im.alpha_composite(d.out()); glow(im, 1500, 760, 400, (255, 220, 150, 130), 70); im.convert('RGB').save(path)


def lowell(path):                                            # Arizona dusk: white observatory dome on a pine hill, red mesas, purple-orange sky
    im = sky((110, 80, 170), (255, 170, 110), 1.0); d = Draw(W2, H2)
    for x0, x1, h in ((0, 600, 420), (1800, 2400, 380)): d.poly([(x0, 940), (x0 + 60, 940 - h), (x1 - 60, 940 - h), (x1, 940)], fill=(200, 90, 60, 255), outline=LINE, width=10)
    d.ellipse(1200, 1000, 700, 360, fill=(80, 130, 90, 255), outline=LINE, width=10)
    d.rect(1020, 460, 1380, 700, (240, 240, 236, 255)); d.poly([(1020, 460), (1380, 460), (1380, 700), (1020, 700)], outline=LINE, width=12)
    d.chord(1200, 470, 210, 220, 180, 360, fill=(250, 250, 248, 255), outline=LINE, width=14); d.rect(1170, 260, 1230, 470, (60, 70, 100, 255))
    for x in (760, 880, 1520, 1640): d.poly([(x - 70, 820), (x, 520), (x + 70, 820)], fill=(40, 100, 70, 255), outline=LINE, width=8)
    r = np.random.RandomState(4)
    for _ in range(40): d.dot(r.randint(0, W2), r.randint(0, 300), 4, (255, 250, 230, 220))
    fl(d, (170, 110, 80, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 300, (255, 240, 200, 70), 50); im.convert('RGB').save(path)


def nebula(path):                                            # teal-green nebula, star clusters, a faint ringed giant far away
    im = sky((20, 90, 100), (60, 150, 140), 1.0); d = Draw(W2, H2); r = np.random.RandomState(8)
    for x, y, rr, c in ((500, 300, 380, (60, 200, 180, 90)), (1700, 400, 460, (120, 230, 170, 80)), (1200, 700, 300, (40, 160, 200, 90))): d.dot(x, y, rr, c)
    for _ in range(320): d.dot(r.randint(0, W2), r.randint(0, 940), r.choice([3, 4, 6, 8]), (240, 255, 250, 230))
    d.ellipse(1950, 220, 120, 120, fill=(230, 200, 150, 255), outline=LINE, width=8); d.ellipse(1950, 220, 220, 40, outline=(240, 220, 170, 255), width=10)
    fl(d, (60, 120, 130, 255)); im.alpha_composite(d.out()); glow(im, 1200, 450, 600, (150, 255, 230, 60), 100); im.convert('RGB').save(path)


def blinkroom(path):                                         # observatory plate room: warm red safelight, plate racks, star charts, brass rail
    im = sky((170, 70, 70), (200, 100, 90), 1.0); d = Draw(W2, H2)
    for x0 in (120, 1820):
        d.rrect(x0, 200, x0 + 460, 880, 10, fill=(120, 60, 50, 255), outline=LINE, width=12)
        for y in range(240, 860, 60): d.rect(x0 + 30, y, x0 + 430, y + 36, (40, 36, 50, 255))
    d.rrect(820, 160, 1580, 640, 10, fill=(30, 36, 70, 255), outline=(230, 200, 120, 255), width=16); r = np.random.RandomState(6)
    for _ in range(90): d.dot(r.randint(850, 1550), r.randint(190, 610), r.choice([3, 5]), WT)
    for k in range(5): d.stroke([(880 + k * 150, 600), (930 + k * 150, 220)], (120, 140, 200, 255), 3)
    d.dot(1200, 80, 40, (255, 80, 60, 255)); d.rect(0, 900, W2, 920, (230, 190, 90, 255))
    fl(d, (150, 80, 70, 255)); im.alpha_composite(d.out()); glow(im, 1200, 80, 300, (255, 90, 70, 140), 50); glow(im, 1200, 400, 400, (120, 150, 255, 60), 70); im.convert('RGB').save(path)


def news(path):                                              # sunny 1930 street: sepia-yellow sky, brick shops with awnings, lamp posts, bunting
    im = sky((255, 220, 150), (255, 240, 200), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 400)):
        col = ((200, 90, 70), (110, 140, 190), (220, 170, 90), (140, 170, 110))[k % 4] + (255,); h = 600 + (k % 3) * 80
        d.poly([(x, 940), (x + 390, 940), (x + 390, 940 - h), (x, 940 - h)], fill=col, outline=LINE, width=10)
        for i in range(3): d.rrect(x + 40 + i * 115, 1000 - h, x + 120 + i * 115, 1100 - h, 8, fill=(255, 240, 190, 255), outline=LINE, width=6)
        for i in range(6): d.poly([(x + i * 65, 680), (x + i * 65 + 65, 680), (x + i * 65 + 32, 740)], fill=(WT if i % 2 else (220, 60, 60, 255)))
        d.rect(x + 60, 760, x + 330, 940, (90, 70, 60, 255))
    for k in range(30): d.poly([(k * 80, 120 + 20 * (k % 2)), (k * 80 + 40, 170), (k * 80 + 80, 120 + 20 * ((k + 1) % 2))], fill=[PINK, YEL, CYAN][k % 3])
    fl(d, (190, 170, 140, 255)); im.alpha_composite(d.out()); glow(im, 1200, 200, 500, (255, 250, 220, 80), 80); im.convert('RGB').save(path)


def launchday(path):                                         # bright launch day: deep blue sky, huge white clouds, tower, palms, crowd stand
    im = sky((60, 140, 230), (190, 226, 255), 1.0); d = Draw(W2, H2)
    for x, y, s in ((300, 200, 1.0), (900, 140, 1.3), (1800, 220, 1.1), (2200, 120, 0.8)):
        for dx, dy, rr in ((0, 0, 120), (110, 20, 100), (-110, 30, 90), (40, -60, 90)): d.dot(x + dx * s, y + dy * s, rr * s, WT)
    d.poly([(1500, 940), (1500, 260), (1620, 260), (1620, 940)], outline=(200, 60, 50, 255), width=16)
    for y in range(300, 940, 80): d.stroke([(1500, y), (1620, y + 80)], (200, 60, 50, 255), 8)
    for x in (300, 520, 2050, 2250): M.palm(d, x, 940, 360)
    d.rect(0, 860, W2, 940, (120, 160, 120, 255)); fl(d, (210, 200, 180, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 500, (255, 255, 240, 60), 80); im.convert('RGB').save(path)


def cleanroom(path):                                         # white clean room: teal floor stripe, glass walls, gantry crane, ceiling lights
    im = sky((226, 240, 244), (210, 232, 236), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.rect(x, 0, x + 290, 860, (236, 246, 248, 255)); d.stroke([(x, 0), (x, 860)], (170, 200, 210, 255), 8)
    for x in range(150, W2, 300): d.rrect(x - 100, 30, x + 100, 60, 10, fill=(255, 255, 240, 255))
    d.rect(300, 140, 2100, 180, (240, 190, 60, 255)); d.poly([(300, 140), (2100, 140), (2100, 180), (300, 180)], outline=LINE, width=8); d.stroke([(1200, 180), (1200, 420)], LINE, 8)
    d.rect(0, 860, W2, 900, (60, 180, 170, 255)); fl(d, (220, 236, 236, 255)); im.alpha_composite(d.out())
    for x in range(150, W2, 300): glow(im, x, 45, 120, (255, 255, 230, 100), 30)
    im.convert('RGB').save(path)


def flyby(path):                                             # icy flyby: blue-violet space, distant sun as a bright star, Charon, ice-mountain horizon
    im = sky((60, 70, 150), (150, 140, 190), 1.0); d = Draw(W2, H2); r = np.random.RandomState(12)
    for _ in range(260): d.dot(r.randint(0, W2), r.randint(0, 800), r.choice([3, 4, 6]), (255, 252, 240, 230))
    d.dot(1950, 260, 130, (190, 186, 180, 255)); d.ellipse(1950, 260, 130, 130, outline=LINE, width=10); d.ellipse(1910, 230, 40, 26, fill=(160, 156, 150, 255))
    d.dot(400, 160, 22, (255, 255, 230, 255))
    pts = [(0, 940)] + [(x, 860 - 80 * abs(math.sin(x / 170.0)) - (40 if (x // 300) % 2 else 0)) for x in range(0, W2 + 1, 60)] + [(W2, 940)]
    d.poly(pts, fill=(236, 226, 214, 255), outline=LINE, width=10)
    fl(d, (220, 204, 190, 255)); im.alpha_composite(d.out()); glow(im, 400, 160, 120, (255, 255, 220, 150), 30); im.convert('RGB').save(path)


def hall(path):                                              # 2006 voting hall: blue tiers of seats, big screen with the nine-planet line-up, spotlights
    im = sky((60, 90, 180), (100, 130, 210), 1.0); d = Draw(W2, H2)
    d.rrect(560, 100, 1840, 560, 16, fill=(20, 30, 60, 255), outline=LINE, width=16)
    for k in range(9): s = (14, 18, 20, 16, 50, 44, 30, 30, 12)[k]; d.dot(660 + k * 135, 330, s, ((200, 190, 180), (240, 210, 140), (90, 150, 230), (220, 100, 60), (230, 180, 120), (230, 210, 150), (150, 220, 230), (80, 120, 220), (226, 196, 160))[k] + (255,))
    d.ellipse(1740, 330, 50, 50, outline=(255, 70, 70, 255), width=8)
    for row in range(4):
        y = 640 + row * 75
        for x in range(40 + row * 30, W2, 120): d.rrect(x, y, x + 100, y + 60, 16, fill=(40, 80 + row * 10, 170, 255), outline=LINE, width=6)
    for x0 in (200, 2000): d.poly([(x0, 0), (x0 + 120, 0), (x0 + 300, 940), (x0 - 180, 940)], fill=(255, 255, 230, 50))
    fl(d, (90, 110, 170, 255)); im.alpha_composite(d.out()); glow(im, 1200, 330, 500, (150, 180, 255, 60), 70); im.convert('RGB').save(path)


def study(path):                                             # cream study: window with blue sky, bookshelves, globe, star poster
    im = sky((250, 236, 206), (246, 226, 190), 1.0); d = Draw(W2, H2)
    d.rect(950, 140, 1450, 620, (150, 200, 245, 255)); M.window(d, 950, 140, 1450, 620)
    for x0 in (150, 1700):
        d.rect(x0, 160, x0 + 520, 900, (150, 100, 70, 255))
        for y in range(200, 880, 140):
            d.rect(x0 + 20, y + 110, x0 + 500, y + 126, (110, 70, 50, 255))
            for k in range(9): d.rect(x0 + 30 + k * 52, y + 20 + (k % 3) * 8, x0 + 72 + k * 52, y + 110, ((220, 80, 70), (70, 130, 200), (240, 190, 80), (90, 160, 100))[k % 4] + (255,))
    fl(d, (190, 150, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 380, 360, (255, 250, 220, 90), 60); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, LA.body
    for ch in ('clyde', 'clydeo', 'dad', 'mom', 'astro', 'newsboy', 'eng', 'v1', 'v2'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'smug')]
    multi = dict(scope={'default': scope()}, crank={'default': crank()}, sep={'default': separator()}, car={'default': car()}, sketch={'default': sketch()}, env={'default': envelope()},
                 letter={'default': letter()}, mailbox={'default': mailbox()}, plates={'default': plates(), 'b': plates(True)}, comp={'default': comparator()}, px={'default': planetx()},
                 pluto={'default': pluto(), 'shocked': pluto('shocked'), 'sad': pluto('sad')}, probe={'default': probe()}, capsule={'default': capsule()},
                 rocket2={'default': rocket2(), 'fire': rocket2('fire')}, paper30={'default': paper1930()}, tbook={'default': textbook()}, vcard={'default': vcard()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    GRN, CRIM, SKY = (40, 150, 80, 255), (220, 50, 50, 255), (60, 120, 220, 255)
    cards = dict(farmboy=plaque('A FARM BOY', 'FOUND A PLANET!', SKY, WHITE, 1000, border=GOLDL, bs=150, ss=126, sc=GOLDL),
                 oldcar=plaque('BUILT FROM', 'AN OLD CAR!', (220, 90, 40, 255), WHITE, 960, border=GOLDL, bs=140, ss=140, sc=GOLDL),
                 flew=plaque('85 YEARS LATER', 'HE FLEW THERE!', (110, 70, 170, 255), WHITE, 1000, border=CYAN, bs=120, ss=130, sc=CYAN),
                 kansas=MA.street('KANSAS', (40, 120, 70, 255)),
                 hailst=stamp('HAILSTORM!', 900, (80, 100, 110, 255), 130, -4),
                 crops=plaque("THE FAMILY'S CROPS", 'WIPED OUT!', (120, 100, 60, 255), WHITE, 1000, border=GOLDL, bs=104, ss=150, sc=GOLDL),
                 college=plaque('CLYDE, 22', "CAN'T AFFORD COLLEGE", (70, 120, 190, 255), WHITE, 1000, border=WHITE, bs=150, ss=90, sc=(255, 240, 170, 255)),
                 y1928=M.cal('HE BUILDS', '1928', (200, 110, 50, 255)),
                 ownscope=plaque('HIS OWN', 'TELESCOPE!', (200, 110, 50, 255), WHITE, 940, border=GOLDL, bs=150, ss=150, sc=GOLDL),
                 parts=stamp('THE PARTS?', 820, (110, 70, 170, 255), 130, 3),
                 buick=plaque('CRANKSHAFT OF A', '1910 BUICK', (190, 50, 50, 255), WHITE, 980, border=GOLDL, bs=110, ss=160, sc=GOLDL),
                 cream=plaque('+ PIECES OF A', 'CREAM SEPARATOR', (60, 130, 170, 255), WHITE, 1000, border=WHITE, bs=120, ss=110, sc=(220, 245, 255, 255)),
                 sketches=plaque('HE SKETCHES', 'JUPITER AND MARS', (200, 120, 60, 255), WHITE, 1000, border=GOLDL, bs=130, ss=110, sc=GOLDL),
                 mails=plaque('MAILS THE', 'DRAWINGS!', (220, 90, 120, 255), WHITE, 960, border=GOLDL, bs=140, ss=140, sc=GOLDL),
                 lowell=plaque('LOWELL OBSERVATORY', 'ARIZONA', (180, 80, 60, 255), WHITE, 1040, border=GOLDL, bs=92, ss=150, sc=GOLDL),
                 advice=plaque('HE WANTS', 'ADVICE', (70, 120, 190, 255), WHITE, 960, border=GOLDL, bs=140, ss=140, sc=GOLDL),
                 hunting=plaque('LOWELL WAS', 'HUNTING...', (110, 70, 170, 255), WHITE, 960, border=CYAN, bs=140, ss=140, sc=CYAN),
                 joboffer=M.bigneon('THEY SEND BACK', 'A JOB OFFER!', 1000, YEL, LIME),
                 planetx=M.bigneon('PLANET X', 'A MYSTERY WORLD', 960, CYAN, PINK),
                 tedious=plaque('THE MOST TEDIOUS', 'JOB IN ASTRONOMY', (150, 50, 60, 255), WHITE, 1000, border=GOLDL, bs=110, ss=110, sc=GOLDL),
                 flip=plaque('FLIP BETWEEN', 'TWO PHOTOS', (40, 50, 90, 255), WHITE, 960, border=CYAN, bs=130, ss=150, sc=CYAN),
                 days=plaque('TAKEN', 'DAYS APART', (110, 110, 140, 255), WHITE, 960, border=GOLDL, bs=140, ss=140, sc=GOLDL),
                 onedot=plaque('FIND THE ONE DOT', 'THAT MOVES!', (220, 80, 60, 255), WHITE, 1000, border=GOLDL, bs=110, ss=150, sc=GOLDL),
                 countless=plaque('AMONG', 'COUNTLESS STARS', (30, 120, 120, 255), WHITE, 960, border=GOLDL, bs=150, ss=120, sc=GOLDL),
                 y1930=M.cal('FEB 18', '1930', (60, 120, 220, 255)),
                 finds=stamp('HE FINDS IT!', 880, CRIM, 130, -4),
                 age24=M.bigneon('HE IS', 'ONLY 24!', 820, YEL, LIME),
                 named=plaque('THE WORLD NAMES IT', 'PLUTO!', (60, 120, 220, 255), WHITE, 1000, border=GOLDL, bs=104, ss=190, sc=GOLDL),
                 before=plaque('BEFORE ANYONE', 'CAN VISIT IT', (90, 80, 140, 255), WHITE, 960, border=(220, 210, 255, 255), bs=130, ss=130, sc=(230, 220, 255, 255)),
                 y2006=M.cal('LAUNCH', '2006', (60, 120, 220, 255)),
                 nh=plaque('NASA LAUNCHES', 'NEW HORIZONS', (30, 60, 140, 255), WHITE, 1000, border=(255, 110, 90, 255), bs=120, ss=130, sc=(255, 200, 180, 255)),
                 capsule=plaque('INSIDE A', 'SMALL CAPSULE', (40, 150, 150, 255), WHITE, 960, border=GOLDL, bs=150, ss=124, sc=GOLDL),
                 ashes=plaque('ABOUT AN OUNCE', 'OF HIS ASHES', (110, 90, 70, 255), WHITE, 960, border=GOLDL, bs=130, ss=140, sc=GOLDL),
                 y2015=M.cal('JULY', '2015', (110, 70, 170, 255)),
                 miles=M.bigneon('7,800 MILES', 'FROM PLUTO!', 980, CYAN, YEL),
                 arrives=plaque('CLYDE FINALLY', 'ARRIVES!', (230, 150, 40, 255), WHITE, 940, border=WHITE, bs=130, ss=170, sc=(255, 250, 200, 255)),
                 problem=plaque("THERE'S JUST", 'ONE PROBLEM...', (60, 60, 80, 255), WHITE, 960, border=(255, 120, 120, 255), bs=130, ss=124, sc=(255, 170, 170, 255)),
                 months7=plaque('7 MONTHS', 'AFTER LAUNCH', (80, 100, 180, 255), WHITE, 960, border=GOLDL, bs=140, ss=140, sc=GOLDL),
                 votedout=plaque('PLUTO VOTED OUT', 'OF THE PLANETS!', CRIM, WHITE, 1000, border=GOLDL, bs=120, ss=120, sc=GOLDL),
                 leftearth=plaque('LEFT EARTH', 'FOR A PLANET', (60, 120, 220, 255), WHITE, 960, border=WHITE, bs=150, ss=140, sc=(220, 240, 255, 255)),
                 dwarf=M.bigneon('ARRIVED AT', 'A DWARF!', 900, PINK, YEL),
                 onpaper=plaque('ON PAPER, HE', 'LOST HIS PLANET', (120, 110, 100, 255), WHITE, 980, border=(255, 120, 120, 255), bs=120, ss=124, sc=(255, 170, 170, 255)),
                 inspace=plaque('IN SPACE, HE', 'FINALLY REACHED IT!', (110, 70, 170, 255), WHITE, 1000, border=GOLDL, bs=120, ss=110, sc=GOLDL))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (110, 120, 150), (100, 110, 140))
    M.sandtex(T('wheat.jpg'), (190, 160, 90), (170, 140, 76)); M.sandtex(T('mud.jpg'), (140, 140, 100), (120, 124, 88)); CE.tiles(T('plank.jpg'), (170, 120, 80), (156, 108, 72))
    CE.tiles(T('atticwood.jpg'), (170, 130, 110), (156, 118, 98)); M.sandtex(T('road.jpg'), (210, 170, 120), (190, 150, 104)); M.sandtex(T('redrock.jpg'), (196, 120, 90), (176, 104, 76))
    M.sandtex(T('spacefloor.jpg'), (60, 130, 130), (230, 255, 250), seed=7); CE.tiles(T('redtile.jpg'), (170, 90, 80), (156, 80, 72)); CE.tiles(T('cobble2.jpg'), (196, 180, 150), (180, 164, 136))
    CE.tiles(T('concrete.jpg'), (214, 210, 200), (200, 196, 186)); CE.tiles(T('whitetile.jpg'), (226, 240, 240), (206, 226, 228)); M.sandtex(T('ice.jpg'), (228, 216, 204), (206, 196, 186))
    CE.tiles(T('bluecarpet.jpg'), (100, 120, 190), (90, 108, 176)); CE.tiles(T('studyfloor.jpg'), (200, 160, 116), (186, 146, 104))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(farm=farm, hail=hail, barn=barn, attic=attic, mailroad=mailroad, lowell=lowell, nebula=nebula, blinkroom=blinkroom, news=news, launchday=launchday,
                cleanroom=cleanroom, flyby=flyby, hall=hall, study=study)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
