#!/usr/bin/env python3
"""Assets for video 15 (Monopoly was invented to make people hate monopolies), drawn in code.
Cute cast: Lizzie (hair bun + pink bow, plum blouse), the landlord (bowler hat, green waistcoat suit, moustache), the tenant
(flat cap, brown sweater), fan1 (quiff, mustard sweater), fan2 (red bob, green cardigan), Charles Darrow (fedora, tan suit),
the professor (grey curls, round glasses, plum suit), pal (spiky, pink tee) and you (blond bob, denim).
Props: the board (top view), the hand-drawn oilcloth board, typewriter, cash fan, money bag, the fair (green, happy) and cruel
(red, horned) rule books, the 1904 patent, the old yellowed patent, Lizzie's portrait (and the empty frame), dice, houses + hotel.
Fifteen sets, each its own palette: GB board city at golden hour, TY peach typing office, LL landlord split (gold mansion | grey
rain), PT cream marble patent office, RS split rules (green meadow | red storm), CU crimson parlour, GU purple quiz stage, LS teal
lecture parlour, HC snowy log cabin, SN seaside sunset, DL olive 1930s living room, PB brick HQ in snow, LZ indigo rainy room,
CT 1970s courtroom, FN neon game night.
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
from assets_base import Draw, LINE, WHITE, H

ROOT = B.ROOT; RED, GOLD, GOLDL = LA.RED, LA.GOLD, M.GOLDL
dk, glow, plaque, stamp, neon, sky, W2, H2 = LA.dk, CE.glow, LA.plaque, LA.stamp, LA.neon, M.sky, M.W2, M.H2
WT, GRN, LIME, PINK, CYAN, YEL, ORNG = (250, 250, 245, 255), (50, 160, 90, 255), (120, 230, 90, 255), (255, 90, 160, 255), (120, 220, 255, 255), (255, 206, 50, 255), (250, 140, 50, 255)
PLUM, TEAL, NAVY = (150, 80, 170, 255), (40, 170, 150, 255), (40, 60, 150, 255)
LA.NEW.update({
    'lizzie': dict(sk=1, style='part', hair=(120, 64, 40, 255), suit=PLUM, shade=(118, 58, 140, 255), body='cardigan', freck=1, bun=1),
    'landlord': dict(sk=0, style='slick', hair=(60, 40, 34, 255), suit=(50, 130, 80, 255), shade=(36, 104, 62, 255), body='suit', tie=GOLD, stache=(70, 46, 36, 255), hat='bowler'),
    'tenant': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=(160, 110, 76, 255), shade=(130, 86, 58, 255), body='sweater', hat='cap'),
    'fan1': dict(sk=0, style='quiff', hair=(200, 120, 50, 255), suit=(232, 170, 50, 255), shade=(200, 140, 36, 255), body='sweater', freck=1),
    'fan2': dict(sk=1, style='bob', hair=(190, 70, 40, 255), suit=(60, 150, 80, 255), shade=(44, 120, 62, 255), body='cardigan', band=YEL),
    'darrow': dict(sk=0, style='side', hair=(80, 56, 40, 255), suit=(196, 150, 96, 255), shade=(166, 120, 72, 255), body='suit', tie=RED, hat='fedora'),
    'prof': dict(sk=1, style='curly', hair=(170, 170, 180, 255), suit=(110, 80, 150, 255), shade=(86, 60, 124, 255), body='suit', tie=TEAL, glasses=1, stubble=1),
    'pal': dict(sk=2, style='spiky', hair=(40, 30, 40, 255), suit=(240, 100, 140, 255), shade=(210, 70, 110, 255), body='tshirt'),
    'you': dict(sk=0, style='bob', hair=(236, 190, 90, 255), suit=(90, 130, 200, 255), shade=(70, 106, 170, 255), body='denim', band=TEAL),
})


def head(char, expr):
    im = LA.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']
    if c.get('bun'):                                         # hair bun on top + pink bow
        d.ellipse(cx + 20, cy - R - 30, 74, 62, fill=c['hair'], outline=LINE, width=14)
        for sg in (-1, 1): d.poly([(cx + 20, cy - R + 20), (cx + 20 + sg * 80, cy - R - 10), (cx + 20 + sg * 80, cy - R + 50)], fill=(255, 120, 170, 255), outline=LINE, width=10)
        d.dot(cx + 20, cy - R + 20, 18, (255, 120, 170, 255))
    h = c.get('hat')
    if h == 'bowler':
        d.ellipse(cx, cy - R + 50, R + 60, 34, fill=(40, 36, 44, 255), outline=LINE, width=14); d.chord(cx, cy - R + 46, R - 30, R - 10, 180, 360, fill=(40, 36, 44, 255), outline=LINE, width=14)
        d.rect(cx - R + 40, cy - R + 14, cx + R - 40, cy - R + 40, GOLD)
    elif h == 'cap':
        d.chord(cx, cy - R + 70, R + 10, R - 40, 180, 360, fill=(120, 124, 136, 255), outline=LINE, width=14); d.ellipse(cx + 120, cy - R + 74, 130, 30, fill=(100, 104, 116, 255), outline=LINE, width=12)
        d.dot(cx, cy - R - 26, 18, (100, 104, 116, 255))
    elif h == 'fedora':
        d.ellipse(cx, cy - R + 46, R + 80, 40, fill=(120, 84, 54, 255), outline=LINE, width=14); d.poly([(cx - R + 30, cy - R + 44), (cx - R + 56, cy - R - 110), (cx, cy - R - 80), (cx + R - 56, cy - R - 110), (cx + R - 30, cy - R + 44)], fill=(120, 84, 54, 255), outline=LINE, width=14)
        d.rect(cx - R + 34, cy - R, cx + R - 34, cy - R + 34, (60, 40, 30, 255))
    im.alpha_composite(d.out()); return im


# ------------------------------------------------------------------ props
PC = [(150, 84, 54), (130, 200, 240), (220, 80, 160), (250, 150, 50), (230, 56, 56), (250, 220, 60), (60, 170, 90), (50, 80, 190)]


def board(S=1000, hand=False):                               # top view: 9 squares a side, colour strips, corners, gold coin in the middle
    bg = (240, 226, 196, 255) if hand else (206, 232, 206, 255); d = Draw(S, S); c = S / 12.0; cs = 1.5 * c; r = np.random.RandomState(3)
    j = (lambda: r.uniform(-6, 6)) if hand else (lambda: 0)
    d.rrect(8, 8, S - 8, S - 8, 24, fill=bg, outline=LINE, width=16)
    for side in range(4):
        for k in range(9):
            a, b = cs + k * c, cs + (k + 1) * c; col = PC[(side * 2 + k // 5) % 8] + (255,)
            (x0, y0), (x1, y1), (u0, v0), (u1, v1) = dict(top=((a, 8), (b, cs), (a, cs - 0.4 * c), (b, cs)), bot=((a, S - cs), (b, S - 8), (a, S - cs), (b, S - cs + 0.4 * c)),
                                                          lef=((8, a), (cs, b), (cs - 0.4 * c, a), (cs, b)), rig=((S - cs, a), (S - 8, b), (S - cs, a), (S - cs + 0.4 * c, b)))[('top', 'bot', 'lef', 'rig')[side]]
            if k not in (2, 5, 7): d.poly([(u0 + j(), v0 + j()), (u1 + j(), v0 + j()), (u1 + j(), v1 + j()), (u0 + j(), v1 + j())], fill=(col if not hand else dk(col, 1.0)))
            else: d.dot((x0 + x1) / 2, (y0 + y1) / 2, c * 0.22, (255, 150, 60, 255) if k == 2 else (90, 90, 110, 255))
            d.poly([(x0 + j(), y0 + j()), (x1 + j(), y0 + j()), (x1 + j(), y1 + j()), (x0 + j(), y1 + j())], outline=(80, 80, 90, 255) if hand else LINE, width=6)
    for (x, y), k in zip(((cs / 2, cs / 2), (S - cs / 2, cs / 2), (S - cs / 2, S - cs / 2), (cs / 2, S - cs / 2)), range(4)):
        if k == 0:
            for q in range(4): d.stroke([(x - cs * 0.3 + q * cs * 0.2, y - cs * 0.3), (x - cs * 0.3 + q * cs * 0.2, y + cs * 0.3)], LINE, 10)
        elif k == 2: d.poly([(x - cs * 0.3, y - cs * 0.12), (x + 0.05 * cs, y - cs * 0.12), (x + 0.05 * cs, y - cs * 0.3), (x + cs * 0.35, y), (x + 0.05 * cs, y + cs * 0.3), (x + 0.05 * cs, y + cs * 0.12), (x - cs * 0.3, y + cs * 0.12)], fill=(230, 56, 56, 255), outline=LINE, width=6)
        else: d.dot(x, y, cs * 0.28, (60, 170, 90, 255) if k == 1 else (70, 130, 220, 255))
    d.dot(S / 2, S / 2, S * 0.2, (255, 200, 60, 255)); d.ellipse(S / 2, S / 2, S * 0.2, S * 0.2, outline=LINE, width=14); d.text(S / 2, S / 2, '$', int(S * 0.26), (200, 120, 20, 255), stroke=6, stroke_fill=LINE)
    if hand:
        d.stroke([(S * 0.66, S * 0.72), (S * 0.86, S * 0.52)], (255, 206, 50, 255), 26); d.poly([(S * 0.66, S * 0.72), (S * 0.62, S * 0.78), (S * 0.69, S * 0.75)], fill=LINE)
    return d.out()


def faceon(d, cx, cy, s, mood):                              # cute face on a prop
    for sg in (-1, 1):
        d.ellipse(cx + sg * 60 * s, cy, 26 * s, 34 * s, fill=WHITE, outline=LINE, width=8); d.dot(cx + sg * 60 * s + 4, cy + 8 * s, 13 * s, LINE); d.dot(cx + sg * 60 * s + 10, cy - 2 * s, 5 * s, WHITE)
        d.ellipse(cx + sg * 104 * s, cy + 50 * s, 22 * s, 13 * s, fill=(255, 130, 130, 190))
        if mood == 'angry': d.stroke([(cx + sg * 30 * s, cy - 40 * s), (cx + sg * 92 * s, cy - 62 * s)], LINE, 12)
    if mood == 'angry': d.arc(cx, cy + 80 * s, 40 * s, 22 * s, 200, 340, LINE, 12)
    else: d.chord(cx, cy + 48 * s, 44 * s, 36 * s, 0, 180, fill=(120, 30, 40, 255), outline=LINE, width=10)


def book(col, mood):
    d = Draw(700, 860); d.rrect(40, 60, 660, 820, 40, fill=dk(col, 0.7), outline=LINE, width=16); d.rrect(70, 40, 650, 800, 36, fill=col, outline=LINE, width=16)
    d.rect(100, 60, 140, 780, dk(col, 0.8)); d.rrect(200, 120, 600, 260, 24, fill=WT, outline=LINE, width=10)
    for k in range(3): d.rect(240, 150 + k * 34, 560, 166 + k * 34, (150, 150, 160, 255))
    faceon(d, 380, 470, 1.5, mood)
    if mood == 'angry':
        for sg in (-1, 1): d.poly([(380 + sg * 150, 70), (380 + sg * 250, -10 + 40), (380 + sg * 210, 90)], fill=(255, 220, 60, 255), outline=LINE, width=10)
    else: d.ellipse(380, 30 + 10, 150, 26, outline=(255, 220, 60, 255), width=14)
    return d.out()


def typewriter():
    d = Draw(900, 760); d.rrect(260, 30, 640, 300, 10, fill=WT, outline=LINE, width=12)
    for k in range(4): d.rect(300, 80 + k * 46, 600, 94 + k * 46, (160, 160, 170, 255))
    d.rrect(120, 260, 780, 360, 40, fill=(60, 60, 70, 255), outline=LINE, width=14); d.rrect(70, 330, 830, 700, 70, fill=(40, 150, 140, 255), outline=LINE, width=16)
    for row in range(3):
        for k in range(9 - row): d.dot(200 + row * 30 + k * 64, 560 + row * 50, 22, (250, 246, 230, 255)); d.ellipse(200 + row * 30 + k * 64, 560 + row * 50, 22, 22, outline=LINE, width=6)
    faceon(d, 450, 430, 0.9, 'happy'); return d.out()


def cash():
    d = Draw(900, 640)
    for k, a in enumerate((-18, -6, 6, 18)):
        cx, cy, t = 450 + k * 30 - 45, 360, math.radians(a); pts = [(cx + x * math.cos(t) - y * math.sin(t), cy + x * math.sin(t) + y * math.cos(t)) for x, y in ((-320, -170), (320, -170), (320, 170), (-320, 170))]
        d.poly(pts, fill=(150, 214, 140, 255), outline=LINE, width=12)
    d.rrect(160, 220, 740, 500, 20, outline=(60, 130, 70, 255), width=10); d.dot(450, 360, 100, (110, 190, 110, 255)); d.text(450, 362, '$', 150, (30, 100, 50, 255), stroke=5, stroke_fill=LINE); return d.out()


def moneybag():
    d = Draw(700, 820); d.ellipse(350, 520, 300, 280, fill=(200, 170, 110, 255), outline=LINE, width=16); d.poly([(240, 250), (460, 250), (420, 160), (480, 70), (220, 70), (280, 160)], fill=(200, 170, 110, 255), outline=LINE, width=14)
    d.stroke([(250, 250), (450, 250)], (180, 60, 50, 255), 26); d.text(350, 540, '$', 300, (60, 140, 70, 255), stroke=10, stroke_fill=LINE); return d.out()


def patent(old=False):
    pc = (232, 206, 150, 255) if old else WT; d = Draw(720, 920)
    pts = [(40, 40), (680, 40), (680, 880), (40, 880)] if not old else [(40, 50), (300, 30), (460, 60), (680, 40), (660, 400), (690, 620), (670, 880), (380, 860), (200, 890), (40, 870), (60, 500)]
    d.poly(pts, fill=pc, outline=LINE, width=14)
    for y in range(300, 760, 70): d.rect(110, y, 610, y + 16, (180, 160, 130, 255) if old else (170, 176, 196, 255))
    d.rect(140, 120, 580, 200, (60, 90, 170, 255) if not old else (150, 120, 90, 255))
    for sg in (-1, 1): d.poly([(560, 720), (560 + sg * 60, 880), (560 + sg * 10, 850)], fill=(220, 50, 50, 255), outline=LINE, width=8)
    d.dot(560, 720, 80, (255, 200, 60, 255) if not old else (200, 150, 70, 255)); d.ellipse(560, 720, 80, 80, outline=LINE, width=10); d.ellipse(560, 720, 52, 52, outline=dk((255, 200, 60, 255), 0.7), width=8)
    if old:
        for x, y in ((200, 400), (480, 560), (300, 650)): d.dot(x, y, 26, (200, 170, 120, 160))
    return d.out()


def frame(gone=False):
    d = Draw(760, 920); d.rrect(20, 20, 740, 900, 60, fill=(230, 170, 60, 255), outline=LINE, width=16); d.rrect(80, 80, 680, 840, 40, fill=(250, 236, 214, 255) if gone else (130, 200, 220, 255), outline=LINE, width=12)
    for x, y in ((50, 50), (710, 50), (50, 870), (710, 870)): d.dot(x, y, 34, (255, 214, 96, 255))
    im = d.out()
    if gone:
        g = Draw(760, 920); g.ellipse(380, 360, 170, 170, outline=(180, 170, 160, 255), width=10); g.chord(380, 760, 220, 200, 180, 360, None, outline=(180, 170, 160, 255), width=10)
        g.text(380, 380, '?', 220, (170, 160, 150, 255)); im.alpha_composite(g.out())
    else:
        hd = head('lizzie', 'happy').crop((0, 0, 460, 520)).resize((414, 468)); bd = LA.body('lizzie').crop((60, 440, 400, 800)).resize((360, 360))
        im.alpha_composite(bd, (200, 470)); im.alpha_composite(hd, (173, 120))
    return im


def dice():
    d = Draw(900, 520)
    for cx, cy, n, t in ((280, 280, 5, -12), (640, 250, 6, 10)):
        r = math.radians(t); P = lambda x, y: (cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r))
        d.poly([P(-200, -200), P(200, -200), P(200, 200), P(-200, 200)], fill=WT, outline=LINE, width=16)
        for x, y in {5: ((-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)), 6: ((-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1))}[n]: d.dot(*P(x * 110, y * 110), 34, (220, 50, 50, 255))
    return d.out()


def houses():
    d = Draw(1000, 640)
    def hut(x, y, w, h, col):
        d.poly([(x, y), (x + w, y), (x + w, y - h), (x + w / 2, y - h - w * 0.5), (x, y - h)], fill=col, outline=LINE, width=14); d.rect(x + w * 0.38, y - h * 0.5, x + w * 0.62, y - 8, dk(col, 0.6))
    hut(40, 600, 220, 180, (60, 170, 90, 255)); hut(740, 600, 220, 180, (60, 170, 90, 255)); hut(300, 600, 400, 340, (220, 50, 50, 255))
    for x in (360, 470, 580): d.rect(x, 330, x + 60, 390, (255, 236, 160, 255))
    return d.out()


def oilpencil():                                             # hand-drawn board on oilcloth with a pencil
    im = board(1000, hand=True); return im


# ------------------------------------------------------------------ cards
def street(txt, col=(30, 120, 70, 255)):
    d = Draw(1000, 300); d.rrect(10, 10, 990, 290, 30, fill=col, outline=LINE, width=16); d.rrect(40, 40, 960, 260, 20, outline=WT, width=10)
    d.text(500, 152, txt, LA.fit(txt, 150, 860), WT, stroke=6, stroke_fill=LINE); return d.out()


def deed(name, col=(40, 60, 170, 255)):
    d = Draw(760, 960); d.rrect(20, 20, 740, 940, 30, fill=WT, outline=LINE, width=16); d.rrect(70, 70, 690, 330, 16, fill=col, outline=LINE, width=10)
    d.text(380, 200, name, LA.fit(name, 120, 580), WT, stroke=6, stroke_fill=LINE)
    for y in range(420, 860, 80): d.rect(130, y, 630, y + 18, (170, 176, 196, 255))
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def fl(d, col, y=940): d.rect(0, y, W2, H2, col); d.stroke([(0, y), (W2, y)], LINE, 8)


def bigworld(path):                                          # golden-hour city of board houses + hotels, confetti, a huge sun
    im = sky((50, 160, 130), (255, 214, 120), 1.0); d = Draw(W2, H2); r = np.random.RandomState(7); d.dot(1200, 600, 250, (255, 240, 180, 255))
    for x in range(-60, W2, 140):
        h, hot = r.randint(150, 400), r.rand() < 0.35; col, w = ((220, 54, 54, 255), 130) if hot else ((60, 170, 90, 255), 110)
        d.poly([(x, 940 - h), (x + w, 940 - h), (x + w, 940), (x, 940)], fill=col, outline=LINE, width=8); d.poly([(x - 12, 940 - h), (x + w / 2, 940 - h - 70), (x + w + 12, 940 - h)], fill=dk(col, 0.72), outline=LINE, width=8)
        for wy in range(940 - h + 30, 900, 70): d.rect(x + 24, wy, x + w - 24, wy + 28, (255, 240, 170, 255))
    for _ in range(140): d.dot(r.randint(0, W2), r.randint(0, 700), r.choice([6, 9, 12]), [PINK, YEL, CYAN, LIME, WT][r.randint(5)])
    fl(d, (40, 130, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 600, 420, (255, 240, 180, 110), 80); im.convert('RGB').save(path)


def office(path):                                            # peach typing office 1904: striped wallpaper, tall sunny window, cabinets, clock, fern
    im = sky((255, 214, 186), (250, 196, 160), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 54, 940, (255, 200, 172, 255))
    d.rect(860, 110, 1540, 860, (150, 210, 240, 255)); d.dot(1380, 320, 90, (255, 244, 190, 255))
    for x, h in ((880, 300), (990, 430), (1110, 250), (1230, 380), (1370, 290)): d.rect(x, 860 - h, x + 100, 860, (120, 150, 196, 255))
    M.window(d, 860, 110, 1540, 860)
    for k in range(3): d.rrect(160, 500 + k * 145, 540, 635 + k * 145, 12, fill=(110, 150, 130, 255), outline=LINE, width=10); d.rrect(310, 550 + k * 145, 390, 574 + k * 145, 8, fill=GOLDL)
    d.ellipse(1900, 300, 120, 120, fill=WT, outline=LINE, width=14); d.stroke([(1900, 300), (1900, 210)], LINE, 12); d.stroke([(1900, 300), (1960, 330)], LINE, 12)
    d.rrect(2080, 760, 2260, 930, 20, fill=(200, 110, 70, 255), outline=LINE, width=10)
    for a in range(200, 345, 24): t = math.radians(a); d.ellipse(2170 + 150 * math.cos(t), 740 + 130 * math.sin(t), 90, 30, fill=(70, 160, 90, 255), outline=LINE, width=8)
    fl(d, (170, 110, 80, 255)); im.alpha_composite(d.out()); glow(im, 1200, 480, 520, (255, 246, 210, 90), 90); im.convert('RGB').save(path)


def landlords(path):                                         # left: gold mansion on a sunny hill | right: grey tenements in the rain
    im = sky((180, 150, 230), (255, 214, 140), 1.0); im.paste(CA.gradient((96, 104, 130), (150, 156, 176), W2 // 2, H2, 1.0).convert('RGBA'), (W2 // 2, 0)); d = Draw(W2, H2)
    d.dot(330, 230, 110, (255, 236, 150, 255)); d.ellipse(600, 1000, 760, 300, fill=(110, 190, 100, 255), outline=LINE, width=10)
    d.poly([(330, 760), (870, 760), (870, 500), (330, 500)], fill=(255, 226, 150, 255), outline=LINE, width=12); d.poly([(290, 500), (600, 330), (910, 500)], fill=(220, 70, 60, 255), outline=LINE, width=12)
    for x in (380, 500, 700, 820): d.rect(x - 16, 560, x + 16, 760, WT)
    for x in (440, 760): d.rrect(x - 40, 560, x + 40, 650, 8, fill=(255, 220, 90, 255), outline=LINE, width=8)
    d.rrect(560, 620, 640, 760, 30, fill=(120, 70, 50, 255), outline=LINE, width=8)
    for k, x in enumerate(range(1240, W2, 190)): h = 480 + 60 * (k % 3); d.poly([(x, 940), (x + 170, 940), (x + 170, 940 - h), (x, 940 - h)], fill=(130, 130, 150, 255), outline=LINE, width=10); [d.rect(x + 30 + i * 70, 940 - h + 40 + j * 110, x + 70 + i * 70, 940 - h + 100 + j * 110, (90, 96, 120, 255)) for i in range(2) for j in range(h // 110 - 1)]
    for x in (1350, 1700, 2100): d.ellipse(x, 140, 260, 90, fill=(90, 96, 116, 255), outline=LINE, width=10)
    r = np.random.RandomState(2)
    for _ in range(120): x, y = r.randint(1210, W2), r.randint(220, 930); d.stroke([(x, y), (x - 14, y + 50)], (200, 214, 240, 255), 5)
    d.rect(1196, 0, 1204, H2, LINE); fl(d, (120, 170, 90, 255)); im.alpha_composite(d.out()); glow(im, 330, 230, 300, (255, 240, 170, 110), 60); im.convert('RGB').save(path)


def patoffice(path):                                         # cream marble hall: columns, navy drapes, gold seal window, red carpet
    im = sky((250, 240, 222), (236, 222, 200), 1.0); d = Draw(W2, H2)
    d.ellipse(1200, 400, 300, 300, fill=(140, 200, 240, 255), outline=LINE, width=16); d.ellipse(1200, 400, 330, 330, outline=(230, 180, 60, 255), width=26)
    pts = [(1200 + (150 if k % 2 == 0 else 60) * math.cos(math.radians(k * 36 - 90)), 400 + (150 if k % 2 == 0 else 60) * math.sin(math.radians(k * 36 - 90))) for k in range(10)]; d.poly(pts, fill=(255, 220, 80, 255), outline=LINE, width=10)
    for x in (200, 520, 1780, 2100): d.rect(x, 60, x + 130, 940, (244, 236, 224, 255)); d.poly([(x, 60), (x + 130, 60), (x + 130, 940), (x, 940)], outline=LINE, width=10); d.rect(x - 20, 40, x + 150, 90, (220, 210, 196, 255)); [d.stroke([(x + 30 + i * 35, 100), (x + 30 + i * 35, 920)], (214, 204, 190, 255), 6) for i in range(3)]
    for x0, x1 in ((700, 860), (1540, 1700)): d.poly([(x0, 0), (x1, 0), (x1 - 30, 940), (x0 + 30, 940)], fill=(40, 60, 140, 255), outline=LINE, width=10)
    d.rect(0, 0, W2, 40, (40, 60, 140, 255)); d.poly([(900, 940), (1500, 940), (1700, H2), (700, H2)], fill=(200, 50, 60, 255))
    fl(d, (224, 214, 200, 255)); d.poly([(950, 940), (1450, 940), (1650, H2), (750, H2)], fill=(200, 50, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 400, 360, (200, 230, 255, 90), 60); im.convert('RGB').save(path)


def splitrules(path):                                        # left: green meadow, sun + rainbow | right: red storm, lightning
    im = sky((120, 200, 250), (210, 240, 255), 1.0); im.paste(CA.gradient((150, 30, 40), (240, 110, 70), W2 // 2, H2, 1.0).convert('RGBA'), (W2 // 2, 0)); d = Draw(W2, H2)
    for k, c in enumerate(((230, 60, 60), (250, 150, 50), (250, 220, 60), (80, 190, 90), (70, 130, 230))): d.arc(600, 940, 560 - k * 40, 520 - k * 40, 180, 360, c + (255,), 40)
    d.dot(220, 200, 100, (255, 236, 120, 255)); d.ellipse(600, 1000, 800, 200, fill=(110, 200, 100, 255), outline=LINE, width=10)
    r = np.random.RandomState(4)
    for _ in range(40): d.dot(r.randint(40, 1160), r.randint(840, 930), 12, [PINK, YEL, WT][r.randint(3)])
    for x in (1400, 1800, 2200): d.ellipse(x, 160, 280, 100, fill=(90, 20, 40, 255), outline=LINE, width=10)
    d.poly([(1760, 240), (1660, 520), (1760, 520), (1680, 800), (1900, 440), (1790, 440), (1880, 240)], fill=(255, 230, 80, 255), outline=LINE, width=10)
    d.ellipse(1800, 1000, 800, 200, fill=(120, 50, 50, 255), outline=LINE, width=10); d.rect(1196, 0, 1204, H2, (255, 250, 220, 255))
    fl(d, (230, 220, 200, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 300, (255, 250, 220, 120), 50); glow(im, 1780, 520, 260, (255, 230, 120, 110), 50); im.convert('RGB').save(path)


def parlour(path):                                           # crimson parlour: gold damask, fireplace, chandelier, smug portraits
    im = sky((180, 50, 70), (210, 80, 90), 1.0); d = Draw(W2, H2)
    for x in range(60, W2, 160):
        for y in range(60, 900, 160): d.poly([(x, y - 26), (x + 20, y), (x, y + 26), (x - 20, y)], fill=(240, 170, 80, 255))
    d.rrect(900, 520, 1500, 940, 20, fill=(240, 226, 210, 255), outline=LINE, width=14); d.rrect(1000, 620, 1400, 940, 160, fill=(60, 30, 30, 255), outline=LINE, width=12)
    for k, c in enumerate(((255, 120, 40), (255, 200, 60))): d.poly([(1080 + k * 40, 930), (1200, 700 + k * 60), (1320 - k * 40, 930)], fill=c + (255,))
    for x in (380, 2020): d.rrect(x - 170, 260, x + 170, 620, 20, fill=(230, 180, 60, 255), outline=LINE, width=14); d.rect(x - 130, 300, x + 130, 580, (90, 130, 90, 255)); d.dot(x, 400, 60, (240, 200, 170, 255)); d.chord(x, 330, 64, 50, 180, 360, fill=(40, 36, 44, 255))
    d.stroke([(1200, 0), (1200, 120)], LINE, 8); d.ellipse(1200, 160, 190, 50, fill=(255, 214, 96, 255), outline=LINE, width=10)
    for x in range(1040, 1380, 60): d.dot(x, 200, 16, (255, 250, 210, 255))
    fl(d, (150, 60, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 820, 300, (255, 160, 60, 140), 60); glow(im, 1200, 180, 300, (255, 240, 180, 110), 50); im.convert('RGB').save(path)


def quiz(path):                                              # purple quiz stage: bulb arch, spotlight cones, giant glowing ?
    im = sky((90, 40, 160), (220, 90, 200), 1.0); d = Draw(W2, H2)
    for x0 in (300, 1700): d.poly([(x0, 0), (x0 + 400, 0), (x0 + 700, 940), (x0 - 300, 940)], fill=(255, 250, 220, 60))
    d.arc(1200, 940, 900, 820, 180, 360, (255, 120, 200, 255), 60)
    for k in range(34): a = math.radians(180 + k * 180 / 33); d.dot(1200 + 900 * math.cos(a), 940 + 820 * math.sin(a), 16, (255, 246, 190, 255))
    d.text(1200, 520, '?', 520, (255, 220, 80, 255), stroke=14, stroke_fill=LINE)
    for x in range(0, W2, 200): d.rrect(x + 20, 880, x + 180, 940, 10, fill=(70, 30, 120, 255), outline=LINE, width=8)
    fl(d, (120, 60, 170, 255)); im.alpha_composite(d.out()); glow(im, 1200, 520, 360, (255, 220, 120, 120), 70); im.convert('RGB').save(path)


def lecture(path):                                           # teal parlour: coral curtains, chalkboard with a board sketch, picture rail
    im = sky((60, 170, 170), (110, 200, 190), 1.0); d = Draw(W2, H2)
    d.rrect(640, 180, 1760, 800, 20, fill=(40, 80, 70, 255), outline=(150, 100, 60, 255), width=30)
    d.poly([(900, 300), (1300, 300), (1300, 700), (900, 700)], outline=(240, 240, 230, 255), width=12); d.poly([(980, 380), (1220, 380), (1220, 620), (980, 620)], outline=(240, 240, 230, 255), width=8)
    d.stroke([(1360, 500), (1600, 500)], (255, 140, 120, 255), 14); d.poly([(1600, 470), (1650, 500), (1600, 530)], fill=(255, 140, 120, 255))
    d.ellipse(1540, 650, 70, 60, outline=(255, 230, 120, 255), width=10)
    for x0, x1 in ((0, 420), (1980, W2)): d.poly([(x0, 0), (x1, 0), (x1 - 60, 940), (x0 + 60, 940)], fill=(250, 130, 110, 255), outline=LINE, width=12)
    d.rect(0, 100, W2, 120, (230, 190, 110, 255)); fl(d, (170, 120, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 480, 500, (255, 250, 220, 60), 80); im.convert('RGB').save(path)


def cabin(path):                                             # log cabin: snowy window, fireplace glow, hand-drawn boards pinned up
    im = sky((180, 120, 80), (200, 140, 90), 1.0); d = Draw(W2, H2)
    for y in range(0, 940, 90): d.rrect(-20, y, W2 + 20, y + 84, 40, fill=(196, 136, 90, 255), outline=dk((196, 136, 90, 255), 0.6), width=6)
    d.rect(900, 180, 1500, 700, (190, 220, 250, 255)); d.ellipse(1200, 760, 420, 120, fill=WT)
    r = np.random.RandomState(9)
    for _ in range(70): d.dot(r.randint(910, 1490), r.randint(190, 690), r.choice([5, 8]), WT)
    for x in (1000, 1120, 1300, 1420): d.poly([(x, 690), (x + 50, 540), (x + 100, 690)], fill=(60, 120, 90, 255), outline=LINE, width=6)
    M.window(d, 900, 180, 1500, 700)
    for x, y in ((360, 300), (560, 420), (1820, 330), (2040, 440)): d.rrect(x - 90, y - 90, x + 90, y + 90, 8, fill=(240, 226, 196, 255), outline=LINE, width=8); d.poly([(x - 60, y - 60), (x + 60, y - 60), (x + 60, y + 60), (x - 60, y + 60)], outline=(200, 80, 60, 255), width=8); d.dot(x, y - 96, 10, (220, 50, 50, 255))
    fl(d, (150, 100, 70, 255)); im.alpha_composite(d.out()); glow(im, 1200, 440, 360, (230, 245, 255, 90), 60); im.convert('RGB').save(path)


def seaside(path):                                           # boardwalk at sunset: pink-orange sky, sea, pier + Ferris wheel, hotels, gulls
    im = sky((250, 120, 150), (255, 200, 120), 1.0); d = Draw(W2, H2); d.dot(1200, 700, 200, (255, 236, 150, 255))
    d.rect(0, 700, W2, 940, (70, 140, 200, 255))
    for y in range(730, 930, 40): d.stroke([(0, y), (W2, y)], (150, 200, 240, 255), 4)
    d.rect(1600, 620, 2400, 650, (120, 80, 60, 255)); d.ellipse(2000, 400, 230, 230, outline=LINE, width=14)
    for k in range(12): a = math.radians(k * 30); d.stroke([(2000, 400), (2000 + 230 * math.cos(a), 400 + 230 * math.sin(a))], (255, 250, 240, 255), 6); d.dot(2000 + 230 * math.cos(a), 400 + 230 * math.sin(a), 22, [PINK, YEL, CYAN][k % 3])
    for x, h, c in ((60, 420, (250, 230, 200)), (300, 520, (255, 200, 170)), (560, 380, (230, 240, 250))): d.poly([(x, 940), (x + 220, 940), (x + 220, 940 - h), (x, 940 - h)], fill=c + (255,), outline=LINE, width=10); [d.rect(x + 30 + i * 60, 960 - h + j * 80, x + 70 + i * 60, 1000 - h + j * 80, (255, 220, 120, 255)) for i in range(3) for j in range(h // 80 - 1)]
    for x, y in ((900, 260), (1000, 200), (1450, 300)): d.stroke([(x - 40, y), (x, y + 20), (x + 40, y)], LINE, 8)
    fl(d, (200, 150, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 700, 360, (255, 220, 150, 130), 70); im.convert('RGB').save(path)


def living30(path):                                          # olive 1930s living room: pinstripes, deco radio, lamp glow, rainy window
    im = sky((120, 150, 90), (150, 176, 110), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 90): d.rect(x, 0, x + 10, 940, (100, 130, 74, 255))
    d.rect(1400, 180, 1900, 680, (150, 170, 200, 255))
    for x, h in ((1420, 250), (1540, 340), (1680, 220), (1780, 300)): d.rect(x, 680 - h, x + 100, 680, (110, 120, 150, 255))
    M.window(d, 1400, 180, 1900, 680)
    d.rrect(500, 520, 820, 900, 140, fill=(160, 100, 60, 255), outline=LINE, width=14); d.rrect(560, 600, 760, 760, 60, fill=(240, 210, 150, 255), outline=LINE, width=8)
    for y in range(620, 760, 30): d.stroke([(570, y), (750, y)], (160, 100, 60, 255), 5)
    d.stroke([(2160, 940), (2160, 360)], LINE, 18); d.poly([(2060, 360), (2260, 360), (2220, 240), (2100, 240)], fill=(255, 220, 140, 255), outline=LINE, width=10)
    d.rrect(160, 260, 380, 440, 10, fill=(230, 190, 110, 255), outline=LINE, width=10); d.rect(190, 290, 350, 410, (180, 200, 220, 255))
    fl(d, (140, 100, 70, 255)); im.alpha_composite(d.out()); glow(im, 2160, 330, 260, (255, 230, 150, 130), 60); glow(im, 660, 680, 200, (255, 220, 140, 90), 40); im.convert('RGB').save(path)


def hq(path):                                                # red-brick company building in snow, chimney smoke, icy sky, snowy pines
    im = sky((120, 170, 230), (220, 236, 250), 1.0); d = Draw(W2, H2)
    d.poly([(500, 940), (1900, 940), (1900, 300), (500, 300)], fill=(190, 80, 60, 255), outline=LINE, width=14)
    for y in range(330, 940, 50): d.stroke([(500, y), (1900, y)], (160, 64, 50, 255), 4)
    for i in range(7):
        for j in range(3): d.rrect(570 + i * 190, 360 + j * 170, 690 + i * 190, 470 + j * 170, 10, fill=(255, 226, 150, 255), outline=LINE, width=8)
    d.rect(480, 270, 1920, 310, WT); d.rrect(1080, 760, 1320, 940, 20, fill=(90, 60, 50, 255), outline=LINE, width=10)
    for x in (700, 1700): d.rect(x, 120, x + 90, 300, (170, 70, 56, 255)); d.poly([(x, 120), (x + 90, 120), (x + 90, 300), (x, 300)], outline=LINE, width=10); [d.ellipse(x + 45 + k * 40, 90 - k * 40, 60 + k * 14, 40 + k * 10, fill=(240, 244, 250, 255)) for k in range(3)]
    for x in (150, 300, 2100, 2260): d.poly([(x - 110, 900), (x, 560), (x + 110, 900)], fill=(50, 120, 90, 255), outline=LINE, width=8); d.poly([(x - 50, 720), (x, 560), (x + 50, 720)], fill=WT)
    r = np.random.RandomState(5)
    for _ in range(90): d.dot(r.randint(0, W2), r.randint(0, 900), r.choice([5, 8]), WT)
    fl(d, (236, 242, 250, 255)); im.alpha_composite(d.out()); glow(im, 1200, 560, 600, (255, 230, 170, 60), 80); im.convert('RGB').save(path)


def rainy(path):                                             # Lizzie's room: indigo flower wallpaper, rain on a big window, warm lamp
    im = sky((110, 116, 180), (130, 136, 196), 1.0); d = Draw(W2, H2); r = np.random.RandomState(8)
    for x in range(60, W2, 150):
        for y in range(60, 900, 150): d.dot(x + (y // 150 % 2) * 75, y, 10, (170, 176, 230, 255))
    d.rect(800, 160, 1600, 760, (70, 90, 140, 255))
    for x, h in ((820, 260), (960, 360), (1120, 220), (1280, 330), (1440, 280)): d.rect(x, 760 - h, x + 130, 760, (50, 64, 104, 255)); [d.rect(x + 20, 780 - h + j * 60, x + 50, 800 - h + j * 60, (255, 220, 140, 255)) for j in range(h // 60 - 1)]
    for _ in range(90): x, y = r.randint(810, 1590), r.randint(170, 740); d.stroke([(x, y), (x - 8, y + 40)], (200, 220, 255, 255), 4)
    M.window(d, 800, 160, 1600, 760); d.rrect(1900, 620, 2160, 940, 16, fill=(150, 100, 70, 255), outline=LINE, width=10)
    d.stroke([(2030, 620), (2030, 440)], LINE, 12); d.poly([(1940, 440), (2120, 440), (2080, 320), (1980, 320)], fill=(255, 210, 120, 255), outline=LINE, width=10)
    fl(d, (100, 90, 130, 255)); im.alpha_composite(d.out()); glow(im, 2030, 420, 300, (255, 210, 130, 150), 60); im.convert('RGB').save(path)


def court(path):                                             # 1970s courtroom: orange wood panels, judge bench + gold seal, tall windows, rays
    im = sky((200, 130, 70), (220, 150, 90), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 110): d.stroke([(x, 0), (x, 940)], (170, 104, 54, 255), 8)
    for x in (140, 1960): d.rrect(x, 120, x + 300, 700, 140, fill=(255, 236, 180, 255), outline=LINE, width=14); M.window(d, x + 30, 260, x + 270, 680, (200, 140, 80, 255))
    d.rrect(700, 520, 1700, 940, 20, fill=(130, 70, 40, 255), outline=LINE, width=14); d.rect(700, 520, 1700, 580, (230, 170, 60, 255))
    d.dot(1200, 300, 150, (240, 190, 70, 255)); d.ellipse(1200, 300, 150, 150, outline=LINE, width=14); d.ellipse(1200, 300, 110, 110, outline=(180, 120, 40, 255), width=10)
    d.stroke([(1130, 330), (1270, 330)], LINE, 12); d.stroke([(1200, 230), (1200, 330)], LINE, 12); d.arc(1150, 330, 40, 30, 0, 180, LINE, 8); d.arc(1250, 330, 40, 30, 0, 180, LINE, 8)
    d.rect(0, 860, W2, 940, (110, 64, 40, 255)); fl(d, (200, 160, 80, 255)); im.alpha_composite(d.out())
    for x in (290, 2110): glow(im, x, 450, 250, (255, 240, 190, 120), 50)
    im.convert('RGB').save(path)


def gamenight(path):                                         # neon game night: purple room, LED strip, string lights, big TV, sofa, city window
    im = sky((120, 60, 170), (230, 100, 170), 1.0); d = Draw(W2, H2)
    d.rect(1500, 160, 2200, 640, (60, 50, 120, 255))
    for x, h in ((1520, 300), (1640, 400), (1800, 260), (1950, 360), (2080, 300)): d.rect(x, 640 - h, x + 110, 640, (40, 30, 90, 255)); [d.rect(x + 20, 660 - h + j * 50, x + 40, 676 - h + j * 50, (255, 230, 120, 255)) for j in range(h // 50 - 1)]
    M.window(d, 1500, 160, 2200, 640, (255, 200, 240, 255)); d.rrect(260, 260, 1000, 680, 20, fill=(30, 30, 50, 255), outline=LINE, width=16); d.rect(300, 300, 960, 640, (80, 200, 230, 255))
    d.dot(630, 470, 110, (255, 220, 80, 255)); d.stroke([(0, 90), (W2, 90)], (80, 255, 230, 255), 16)
    for k in range(40): x = k * 62; d.dot(x, 150 + 30 * math.sin(k * 0.7), 12, [PINK, YEL, CYAN][k % 3])
    d.rrect(200, 720, 1200, 940, 60, fill=(250, 120, 160, 255), outline=LINE, width=14); d.rrect(260, 660, 1140, 780, 50, fill=(255, 150, 180, 255), outline=LINE, width=12)
    fl(d, (150, 90, 170, 255)); im.alpha_composite(d.out()); glow(im, 630, 470, 400, (120, 230, 255, 80), 70)
    for k in range(0, 40, 3): glow(im, k * 62, 150 + 30 * math.sin(k * 0.7), 40, (255, 230, 160, 110), 14)
    im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, LA.body
    for ch in ('lizzie', 'landlord', 'tenant', 'fan1', 'fan2', 'darrow', 'prof', 'pal', 'you'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'smug')]
    multi = dict(board={'default': board()}, oil={'default': board(1000, True)}, typew={'default': typewriter()}, cash={'default': cash()}, mbag={'default': moneybag()},
                 bookg={'default': book((70, 180, 100, 255), 'happy')}, bookr={'default': book((220, 60, 60, 255), 'angry')}, patent={'default': patent()}, oldpat={'default': patent(True)},
                 frame={'default': frame(), 'gone': frame(True)}, dice={'default': dice()}, houses={'default': houses()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    GRD, CRIM = (40, 150, 80, 255), (220, 50, 50, 255)
    cards = dict(hate=plaque('INVENTED TO MAKE PEOPLE', 'HATE MONOPOLIES!', GRD, WHITE, 1040, border=GOLDL, bs=96, ss=120, sc=GOLDL),
                 opposite=stamp('THE EXACT OPPOSITE!', 1000, CRIM, 110, -4),
                 nmliz=plaque('LIZZIE MAGIE', 'A TYPIST', PLUM, WHITE, 960, border=(255, 190, 220, 255), bs=150, ss=100, sc=(255, 210, 230, 255)),
                 grudge=stamp('WITH A GRUDGE!', 940, (230, 110, 30, 255), 116, 3),
                 rich=neon('LANDLORDS', 'GET RICH', 940, GOLDL, LIME),
                 owning=plaque('JUST BY', 'OWNING LAND!', (60, 130, 70, 255), WHITE, 960, border=GOLDL, bs=130, ss=130, sc=GOLDL),
                 tenants=plaque('THEIR TENANTS', 'PAY FOR IT', (100, 104, 130, 255), WHITE, 960, border=(200, 214, 240, 255), bs=140, ss=110, sc=(220, 230, 255, 255)),
                 designs=plaque('SHE DESIGNS', 'A BOARD GAME', (40, 140, 130, 255), WHITE, 980, border=GOLDL, bs=140, ss=110, sc=GOLDL),
                 prove=stamp('TO PROVE IT!', 900, (220, 60, 120, 255), 120, -4),
                 y1904=M.cal('PATENT', '1904', (60, 90, 170, 255)),
                 llgame=plaque("THE LANDLORD'S", 'GAME', (200, 50, 60, 255), WHITE, 980, border=GOLDL, bs=130, ss=150, sc=GOLDL),
                 strange=plaque("HERE'S THE", 'STRANGE PART', (110, 60, 170, 255), WHITE, 960, border=(220, 190, 255, 255), bs=130, ss=130, sc=(230, 210, 255, 255)),
                 tworules=M.bigneon('TWO', 'RULE SETS!', 900, LIME, (255, 110, 110, 255)),
                 richer=plaque('EVERY PLAYER', 'GETS RICHER', GRD, WHITE, 980, border=GOLDL, bs=140, ss=120, sc=GOLDL),
                 earns=plaque('WHENEVER', 'ANYONE EARNS!', (50, 150, 90, 255), WHITE, 960, border=WHITE, bs=130, ss=124, sc=(255, 250, 180, 255)),
                 crush=plaque('CRUSH YOUR FRIENDS', 'WITH RENT', CRIM, WHITE, 1000, border=GOLDL, bs=110, ss=130, sc=GOLDL),
                 broke=plaque('UNTIL THEY', 'GO BROKE!', (60, 50, 70, 255), WHITE, 940, border=(255, 110, 110, 255), bs=130, ss=150, sc=(255, 130, 130, 255)),
                 guess=M.bigneon('GUESS WHICH ONE', 'PEOPLE LOVED?', 1000, YEL, PINK),
                 warning=plaque('THE CRUEL RULES', 'WERE A WARNING', (40, 140, 140, 255), WHITE, 1000, border=(255, 150, 130, 255), bs=120, ss=106, sc=(255, 190, 170, 255)),
                 play=stamp('PLAY THEM...', 820, CRIM, 120, -3),
                 unfair=stamp('FEEL HOW UNFAIR!', 980, (230, 110, 30, 255), 110, 3),
                 switch=plaque('THEN SWITCH TO', 'THE FAIR ONES', GRD, WHITE, 980, border=GOLDL, bs=120, ss=116, sc=GOLDL),
                 skipped=plaque('THEY SKIPPED', 'THE LESSON!', (110, 110, 130, 255), WHITE, 960, border=WHITE, bs=130, ss=140, sc=(220, 230, 255, 255)),
                 kept=stamp('KEPT THE CRUELTY!', 980, CRIM, 112, 4),
                 years=stamp('FOR YEARS...', 860, (150, 90, 50, 255), 120, -3),
                 byhand=plaque('FANS COPIED', 'THE BOARD BY HAND', (150, 90, 50, 255), WHITE, 1000, border=GOLDL, bs=140, ss=96, sc=GOLDL),
                 streets=plaque('THEIR OWN LOCAL', 'STREET NAMES!', (240, 120, 80, 255), WHITE, 1000, border=WHITE, bs=120, ss=120, sc=(255, 240, 170, 255)),
                 st1=street('OCEAN AVE'), st2=street('MAIN STREET', (40, 90, 170, 255)),
                 nmdarrow=plaque('A MAN NAMED', 'CHARLES DARROW', (170, 120, 60, 255), WHITE, 1000, border=GOLDL, bs=110, ss=116, sc=GOLDL),
                 friends=plaque('LEARNED IT', 'FROM FRIENDS', (100, 130, 70, 255), WHITE, 960, border=GOLDL, bs=130, ss=130, sc=GOLDL),
                 myown=plaque('"MY OWN', 'INVENTION!"', (200, 120, 30, 255), WHITE, 940, border=WHITE, bs=140, ss=140, sc=(255, 250, 190, 255)),
                 parker=plaque('SOLD TO', 'PARKER BROTHERS', (190, 70, 50, 255), WHITE, 1000, border=GOLDL, bs=130, ss=112, sc=GOLDL),
                 y1935=M.cal('SOLD', '1935', (190, 70, 50, 255)),
                 andliz=stamp('AND LIZZIE?', 880, PLUM, 120, -3),
                 d500=M.bigneon('$500', 'FOR HER PATENT', 960, LIME, GOLDL),
                 gone=plaque('HER NAME', 'DISAPPEARED', (90, 90, 130, 255), WHITE, 960, border=(200, 200, 230, 255), bs=140, ss=130, sc=(220, 220, 250, 255)),
                 decades=stamp('DECADES LATER...', 960, (200, 110, 40, 255), 112, -3),
                 nmprof=plaque('AN ECONOMICS', 'PROFESSOR', (110, 80, 150, 255), WHITE, 960, border=GOLDL, bs=130, ss=140, sc=GOLDL),
                 dug=plaque('DUG UP HER', 'OLD PATENTS!', (150, 100, 40, 255), WHITE, 960, border=GOLDL, bs=130, ss=130, sc=GOLDL),
                 truth=plaque('THE TRUTH', 'CAME BACK!', (230, 160, 40, 255), WHITE, 960, border=WHITE, bs=150, ss=150, sc=(255, 250, 200, 255)),
                 nexttime=plaque('NEXT TIME A FRIEND', 'BANKRUPTS YOU', (120, 60, 170, 255), WHITE, 1000, border=PINK, bs=110, ss=120, sc=(255, 200, 230, 255)),
                 bwalk=deed('BOARDWALK'),
                 sting=stamp('THAT STING...', 860, (230, 70, 120, 255), 120, -3),
                 point=M.bigneon('IS THE', 'WHOLE POINT!', 940, CYAN, YEL))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (90, 110, 96), (80, 100, 86)); board(1024).convert('RGB').save(T('boardtex.jpg'), quality=92)
    M.sandtex(T('felt.jpg'), (50, 140, 96), (40, 120, 80)); M.sandtex(T('grass.jpg'), (120, 180, 90), (100, 160, 76)); CE.tiles(T('marble.jpg'), (236, 230, 220), (220, 214, 204))
    CE.tiles(T('checker.jpg'), (236, 232, 210), (200, 220, 190)); M.sandtex(T('crimson.jpg'), (170, 66, 70), (150, 54, 60)); CE.tiles(T('stage.jpg'), (150, 80, 190), (130, 64, 170))
    CE.tiles(T('plank.jpg'), (180, 130, 90), (166, 118, 80)); CE.tiles(T('boards.jpg'), (210, 170, 120), (196, 156, 108)); M.sandtex(T('olive.jpg'), (150, 130, 90), (134, 116, 80))
    M.sandtex(T('snow.jpg'), (240, 244, 252), (220, 228, 244)); M.sandtex(T('rug.jpg'), (120, 110, 170), (106, 96, 156)); CE.tiles(T('mustard.jpg'), (210, 170, 90), (194, 154, 78))
    M.sandtex(T('purple.jpg'), (160, 100, 190), (144, 86, 176))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(bigworld=bigworld, office=office, landlords=landlords, patoffice=patoffice, splitrules=splitrules, parlour=parlour, quiz=quiz, lecture=lecture,
                cabin=cabin, seaside=seaside, living30=living30, hq=hq, rainy=rainy, court=court, gamenight=gamenight)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
