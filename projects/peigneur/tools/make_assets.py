#!/usr/bin/env python3
"""Assets for video 13 (Lake Peigneur, 1980: a hole the size of a pizza swallowed a lake), drawn in code.
New cute cast: the fisherman (straw hat, teal hoodie), the driller (yellow hard hat, moustache, orange hoodie), the miner
(white hard hat with a lamp, blue hoodie, reflective stripe).  Hero props: the cute PIZZA (happy / shocked), the oil rig,
the barge, the drill bit, the depth pole, the seagull.  Eleven sets, each its own palette: WH whirlpool lake at a storm dusk
(teal + orange), BY bayou dawn (pink + gold), RG lake at noon (sky blue), DK drill deck at sunset (orange + steel),
SK storm swallow (violet + green), WF waterfall with a rainbow (gold + emerald), SM salt-mine cross-section (pink + lilac),
TN flooding tunnel (teal + salt white), EX escape at sunrise (gold), GF the Gulf (turquoise), NL the new lake at dusk (purple + gold).
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image, ImageFilter
import assets_base as B
import gimli_assets as G
import corrigan_assets as CA
import catseyes_assets as CE
import lordgta_assets as LA
from assets_base import Draw, LINE, WHITE, bez

ROOT = B.ROOT; RED, GOLD = LA.RED, LA.GOLD
dk, glow, plaque, stamp, neon, fit = LA.dk, CE.glow, LA.plaque, LA.stamp, LA.neon, LA.fit
ORNG, TEAL, YEL, SKYB, GOLDL, LIME, PINK = (250, 140, 50, 255), (40, 170, 150, 255), (255, 206, 50, 255), (70, 150, 230, 255), (255, 214, 96, 255), (120, 230, 90, 255), (255, 90, 160, 255)
WT = (250, 250, 245, 255)
LA.NEW.update({
    'fisher': dict(sk=2, style='curly', hair=(40, 28, 24, 255), suit=TEAL, shade=(30, 136, 120, 255), body='hoodie', freck=1, straw=1),
    'driller': dict(sk=0, style='side', hair=(170, 80, 40, 255), suit=ORNG, shade=(214, 110, 36, 255), body='hoodie', freck=1, hardhat=YEL),
    'miner': dict(sk=1, style='part', hair=(50, 34, 28, 255), suit=SKYB, shade=(50, 110, 190, 255), body='hoodie', hardhat=WT, lamp=1),
})


def head(char, expr):
    im = LA.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx = 230
    if c.get('hardhat'):                                     # hard hat: dome, brim, ridge or a head lamp
        col = c['hardhat']; d.chord(cx, 186, 218, 172, 180, 360, fill=col, outline=LINE, width=16)
        d.rrect(cx - 224, 168, cx + 224, 206, 18, fill=dk(col, 0.85), outline=LINE, width=12)
        if c.get('lamp'): d.ellipse(cx, 110, 54, 46, fill=(255, 250, 200, 255), outline=LINE, width=12); d.ellipse(cx, 110, 28, 24, fill=(255, 226, 80, 255))
        else: d.rrect(cx - 24, 22, cx + 24, 172, 14, fill=dk(col, 0.9), outline=LINE, width=8)
    if c.get('straw'):                                       # straw hat with a red band
        S = (236, 200, 120, 255); d.ellipse(cx, 178, 224, 48, fill=S, outline=LINE, width=12); d.chord(cx, 170, 158, 140, 180, 360, fill=S, outline=LINE, width=14)
        d.rect(cx - 150, 128, cx + 150, 156, (220, 60, 60, 255))
        for k in range(5): d.stroke([(cx - 120 + k * 60, 70), (cx - 110 + k * 55, 120)], dk(S, 0.85), 6)
    im.alpha_composite(d.out()); return im


def body(char):
    c = LA.NEW[char]; im = LA.body(char); d = Draw(im.width, im.height); col = c['suit']
    d.chord(230, 462, 136, 62, 180, 360, fill=dk(col, 0.78), outline=LINE, width=12)
    d.rrect(140, 650, 320, 744, 34, fill=dk(col, 0.86), outline=LINE, width=10)
    if char == 'miner': d.rect(96, 600, 364, 626, (255, 226, 70, 255))
    if char == 'driller':
        for sg in (-1, 1): d.stroke([(230 + sg * 70, 476), (230 + sg * 58, 650)], (60, 84, 150, 255), 22)
    if char == 'fisher': d.ellipse(230, 600, 40, 22, fill=(255, 150, 80, 255), outline=LINE, width=6); d.poly([(268, 600), (296, 582), (296, 618)], fill=(255, 150, 80, 255), outline=LINE, width=6)
    im.alpha_composite(d.out()); return im


# ------------------------------------------------------------------ hero props
def pizza(face='default'):                                  # the cute pizza: crust, cheese, pepperoni, big eyes
    d = Draw(900, 900); cx, cy = 450, 450
    d.ellipse(cx, cy, 420, 420, fill=(214, 140, 60, 255), outline=LINE, width=18); d.ellipse(cx, cy, 352, 352, fill=(255, 206, 90, 255), outline=LINE, width=10)
    for a in range(30, 390, 60): r = math.radians(a); d.stroke([(cx + 60 * math.cos(r), cy + 60 * math.sin(r)), (cx + 350 * math.cos(r), cy + 350 * math.sin(r))], (226, 168, 60, 255), 8)
    for x, y in ((250, 250), (650, 270), (450, 190), (170, 480), (730, 480), (270, 700), (630, 700)): d.ellipse(x, y, 50, 50, fill=(214, 60, 50, 255), outline=LINE, width=8); d.dot(x - 14, y - 12, 9, (240, 120, 100, 255))
    for sg in (-1, 1): d.ellipse(cx + sg * 110, 420, 48, 62 if face == 'shocked' else 56, fill=WHITE, outline=LINE, width=10); d.dot(cx + sg * 110 + 6, 432, 22, LINE); d.dot(cx + sg * 110 + 14, 418, 7, WHITE)
    for sg in (-1, 1): d.ellipse(cx + sg * 200, 530, 44, 26, fill=(255, 130, 130, 190))
    if face == 'shocked': d.ellipse(cx, 590, 58, 70, fill=(120, 30, 40, 255), outline=LINE, width=10); d.ellipse(cx, 620, 34, 22, fill=(255, 120, 130, 255))
    else: d.chord(cx, 540, 104, 80, 0, 180, fill=(120, 30, 40, 255), outline=LINE, width=12)
    return d.out()


def rig():                                                   # red-and-white derrick on a steel deck, yellow cabin, flag
    d = Draw(800, 1500); R_ = (220, 70, 50, 255)
    for x in (130, 670): d.rect(x - 22, 1350, x + 22, 1490, (70, 70, 84, 255))
    d.rrect(40, 1250, 760, 1360, 20, fill=(96, 104, 120, 255), outline=LINE, width=14); d.rect(70, 1300, 730, 1316, YEL)
    for a, b in (((170, 1250), (400, 100)), ((630, 1250), (400, 100))): d.stroke([a, b], LINE, 30); d.stroke([a, b], R_, 16)
    for k in range(1, 8):
        y0, y1 = 100 + k * 144, 100 + (k + 1) * 144; w0, w1 = (y0 - 100) / 1150 * 230, min(230, (y1 - 100) / 1150 * 230)
        d.stroke([(400 - w0, y0), (400 + w0, y0)], LINE, 16); d.stroke([(400 - w0, y0), (400 + w0, y0)], WT if k % 2 else R_, 8)
        if k < 7: d.stroke([(400 - w0, y0), (400 + w1, y1)], R_, 6); d.stroke([(400 + w0, y0), (400 - w1, y1)], R_, 6)
    d.rrect(560, 1100, 740, 1250, 14, fill=YEL, outline=LINE, width=12); d.rrect(590, 1130, 660, 1186, 8, fill=(170, 220, 255, 255), outline=LINE, width=6)
    d.stroke([(400, 100), (400, 10)], LINE, 10); d.poly([(404, 12), (500, 40), (404, 70)], fill=R_, outline=LINE, width=8); return d.out()


def barge():
    d = Draw(1200, 520); d.poly([(20, 300), (1180, 300), (1100, 490), (100, 490)], fill=(180, 70, 50, 255), outline=LINE, width=16); d.rect(44, 330, 1156, 352, YEL)
    for k, x in enumerate((170, 410, 650, 890)): d.rrect(x, 110 + (k % 2) * 60, x + 200, 300, 14, fill=[(70, 140, 200, 255), ORNG, (90, 170, 110, 255), (230, 90, 90, 255)][k], outline=LINE, width=12)
    for x in (150, 1050): d.dot(x, 420, 26, (240, 240, 240, 255))
    return d.out()


def drillbit():                                              # steel pipe + three-cone bit with gold teeth
    d = Draw(420, 1300); d.rrect(150, 0, 270, 900, 20, fill=(150, 160, 176, 255), outline=LINE, width=14); d.rect(176, 20, 196, 880, (210, 220, 232, 255))
    for y in (220, 560): d.rrect(130, y, 290, y + 70, 16, fill=(110, 118, 134, 255), outline=LINE, width=12)
    for cx_ in (130, 210, 290): d.ellipse(cx_, 1040, 92, 170, fill=(120, 126, 140, 255), outline=LINE, width=14)
    for cx_ in (130, 210, 290):
        for y in (930, 1010, 1090, 1170): d.poly([(cx_ - 26, y), (cx_ + 26, y), (cx_, y + 40)], fill=GOLDL, outline=LINE, width=6)
    return d.out()


def pole():                                                  # red/white depth pole with a buoy
    d = Draw(260, 1300)
    for k in range(10): d.rect(90, 40 + k * 120, 170, 160 + k * 120, (230, 60, 60, 255) if k % 2 else WT)
    d.poly([(90, 40), (170, 40), (170, 1240), (90, 1240)], outline=LINE, width=12); d.ellipse(130, 1150, 120, 70, fill=ORNG, outline=LINE, width=12); return d.out()


def gull():
    d = Draw(700, 420); W_ = (250, 250, 252, 255)
    d.poly(bez((330, 220), (220, 40), (90, 60), (20, 120)) + [(200, 200)], fill=(220, 226, 236, 255), outline=LINE, width=12)
    d.poly(bez((370, 220), (480, 40), (610, 60), (680, 120)) + [(500, 200)], fill=(220, 226, 236, 255), outline=LINE, width=12)
    d.ellipse(350, 250, 150, 92, fill=W_, outline=LINE, width=12); d.ellipse(470, 210, 70, 64, fill=W_, outline=LINE, width=12)
    d.poly([(530, 205), (600, 220), (530, 236)], fill=YEL, outline=LINE, width=8); d.dot(486, 196, 14, LINE); d.dot(490, 190, 5, WHITE); d.ellipse(458, 232, 16, 10, fill=(255, 150, 150, 200))
    return d.out()


def calendar():
    d = Draw(720, 800); d.rrect(20, 60, 700, 780, 40, fill=(255, 246, 236, 255), outline=LINE, width=18); d.rrect(20, 60, 700, 270, 40, fill=(230, 80, 60, 255), outline=LINE, width=18)
    d.rect(38, 220, 682, 270, (230, 80, 60, 255)); d.stroke([(20, 270), (700, 270)], LINE, 14); d.text(360, 168, 'NOV 20', 120, WHITE, stroke=6, stroke_fill=LINE)
    for x in (200, 520): d.rrect(x - 22, 20, x + 22, 120, 18, fill=(150, 150, 160, 255), outline=LINE, width=10)
    d.text(360, 520, '1980', 230, (40, 150, 200, 255), stroke=10, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
W2, H2 = 2400, 1100
def sky(top, bot, k=1.2): return CA.gradient(top, bot, W2, H2, k).convert('RGBA')
def cypress(d, x, base, h, col, moss=(150, 176, 130, 255)):
    d.poly([(x - 46, base), (x - 14, base - h), (x + 14, base - h), (x + 46, base)], fill=dk(col, 0.55), outline=LINE, width=8)
    for k in range(3): d.ellipse(x + (k - 1) * 44, base - h + k * h * 0.2, 150 - k * 12, 58, fill=col, outline=LINE, width=8)
    for k in range(4): xx = x - 90 + k * 60; d.stroke([(xx, base - h + 30), (xx + 8, base - h + 140 + k * 18)], moss, 10)
def clouds(d, pts, col=(255, 255, 255, 235)):
    for x, y, s in pts:
        for dx, dy, r in ((-90, 10, 70), (0, -20, 95), (95, 8, 72), (40, 30, 70), (-40, 30, 70)): d.ellipse(x + dx * s, y + dy * s, r * s * 1.3, r * s, fill=col)
def whirlpool(d, cx, cy, rx, ry, c1, c2, n=9):
    for k in range(n):
        f = 1 - k / n; c = tuple(int(a + (b - a) * k / n) for a, b in zip(c1, c2)) + (255,)
        d.ellipse(cx, cy + k * ry * 0.06, rx * f + 20, ry * f + 8, fill=c, outline=LINE if k == 0 else None, width=10 if k == 0 else 0)
    for k in range(n - 1): f = 1 - k / n; d.arc(cx, cy + k * ry * 0.06, rx * f * 0.94, ry * f * 0.9, 190 + k * 40, 320 + k * 40, (236, 255, 255, 235), max(4, 14 - k))
    d.ellipse(cx, cy + n * ry * 0.06, rx * 0.08, ry * 0.08, fill=(8, 24, 40, 255))
def derrick(d, x, y, h, tilt, col=(220, 70, 50, 255)):
    t = math.radians(tilt); P_ = lambda u, v: (x + u * math.cos(t) - v * math.sin(t), y + u * math.sin(t) + v * math.cos(t))
    d.stroke([P_(-h * 0.22, 0), P_(0, -h)], LINE, 14); d.stroke([P_(h * 0.22, 0), P_(0, -h)], LINE, 14); d.stroke([P_(-h * 0.22, 0), P_(0, -h)], col, 7); d.stroke([P_(h * 0.22, 0), P_(0, -h)], col, 7)
    for k in range(1, 5): v = -h * k / 5; w = h * 0.22 * (1 - k / 5); d.stroke([P_(-w, v), P_(w, v)], col, 6)


def whirlbg(path):                                           # hook lake at storm dusk: orange break in the clouds, a giant whirlpool, a rig tipping in
    im = sky((24, 70, 90), (255, 150, 70), 1.4); d = Draw(W2, H2)
    clouds(d, [(300, 160, 1.6), (900, 110, 1.3), (1600, 150, 1.7), (2200, 120, 1.4)], (60, 80, 110, 230)); d.poly([(1720, 80), (1660, 260), (1720, 250), (1650, 430), (1800, 220), (1730, 230), (1800, 80)], fill=(255, 250, 200, 255))
    for x in range(-40, W2 + 80, 170): cypress(d, x, 600, 170 + (x * 37) % 90, (40, 80, 70, 255), (90, 120, 100, 255))
    d.rect(0, 580, W2, H2, (40, 140, 150, 255)); d.stroke([(0, 580), (W2, 580)], LINE, 8)
    whirlpool(d, 1200, 800, 1000, 260, (60, 180, 180), (10, 60, 80)); derrick(d, 1500, 760, 260, 28)
    im.alpha_composite(d.out()); glow(im, 1720, 250, 220, (255, 250, 200, 120), 50); glow(im, 1200, 470, 600, (255, 170, 90, 90), 90); im.convert('RGB').save(path)


def bayou(path):                                             # pink-gold dawn, low sun, cypress with moss, lily pads, mist
    im = sky((250, 140, 170), (255, 224, 150), 1.1); d = Draw(W2, H2)
    d.ellipse(1450, 560, 170, 170, fill=(255, 246, 200, 255)); clouds(d, [(500, 220, 1.0), (1000, 160, 0.8), (1900, 230, 1.1)], (255, 200, 210, 220))
    d.rect(0, 600, W2, H2, (120, 170, 190, 255)); d.stroke([(0, 600), (W2, 600)], LINE, 8)
    for k in range(6): d.stroke([(1450 - 140 + k * 20, 640 + k * 50), (1450 + 140 - k * 20, 640 + k * 50)], (255, 240, 200, 255), 10)
    for x, h in ((140, 520), (460, 400), (1950, 470), (2280, 560), (780, 300)): cypress(d, x, 640, h, (70, 130, 80, 255))
    for x, y in ((300, 900), (700, 1000), (1100, 860), (1800, 960), (2150, 880)): d.ellipse(x, y, 80, 26, fill=(80, 170, 90, 255), outline=LINE, width=6); d.dot(x + 20, y - 10, 16, (255, 140, 190, 255))
    im.alpha_composite(d.out()); glow(im, 1450, 560, 300, (255, 250, 220, 150), 60); glow(im, 1200, 640, 900, (255, 255, 255, 60), 100); im.convert('RGB').save(path)


def lakenoon(path):                                          # bright noon: blue sky, puffy clouds, salt-dome hill with a white house, flat lake
    im = sky((60, 140, 240), (200, 236, 255), 1.0); d = Draw(W2, H2)
    clouds(d, [(400, 200, 1.3), (1200, 140, 1.0), (2000, 220, 1.4)])
    d.chord(600, 620, 700, 200, 180, 360, fill=(110, 180, 90, 255), outline=LINE, width=8); d.chord(1900, 620, 600, 120, 180, 360, fill=(90, 160, 80, 255), outline=LINE, width=8)
    d.rect(520, 380, 700, 470, WT); d.poly([(500, 384), (610, 320), (720, 384)], fill=(200, 80, 70, 255), outline=LINE, width=8); d.poly([(520, 380), (700, 380), (700, 470), (520, 470)], outline=LINE, width=8)
    for x in (550, 610, 670): d.rect(x - 8, 400, x + 8, 460, (120, 170, 210, 255))
    d.rect(0, 610, W2, H2, (70, 160, 220, 255)); d.stroke([(0, 610), (W2, 610)], LINE, 8)
    for k in range(40): x, y = (k * 383) % W2, 660 + (k * 137) % 420; d.stroke([(x, y), (x + 70, y)], (230, 248, 255, 255), 6)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def deck(path):                                              # sunset deck: big sun, derrick legs, pipe racks, hazard stripes, floodlights
    im = sky((120, 60, 140), (255, 160, 70), 1.0); d = Draw(W2, H2)
    d.ellipse(1250, 600, 260, 260, fill=(255, 220, 130, 255))
    for x, sg in ((260, 1), (2140, -1)):
        d.stroke([(x, H2), (x + sg * 300, 0)], LINE, 40); d.stroke([(x, H2), (x + sg * 300, 0)], (200, 80, 60, 255), 22)
        for k in range(6): y = 100 + k * 160; d.stroke([(x + sg * 300 * (1 - y / H2), y), (x + sg * 300 * (1 - y / H2) + sg * 200, y + 80)], (200, 80, 60, 255), 12)
    d.rect(0, 700, W2, H2, (70, 76, 92, 255)); d.stroke([(0, 700), (W2, 700)], LINE, 10)
    for j in range(3):
        for k in range(5): d.rrect(700 + k * 200 + j * 100, 620 - j * 60, 880 + k * 200 + j * 100, 670 - j * 60, 24, fill=(150, 160, 176, 255), outline=LINE, width=8)
    for x in range(0, W2, 120): d.poly([(x, 1040), (x + 60, 1040), (x + 120, 1100), (x + 60, 1100)], fill=YEL)
    for x in (520, 1880): d.rrect(x - 90, 120, x + 90, 200, 20, fill=(255, 250, 220, 255), outline=LINE, width=10)
    im.alpha_composite(d.out()); glow(im, 1250, 600, 420, (255, 230, 150, 130), 80)
    for x in (520, 1880): glow(im, x, 160, 200, (255, 250, 220, 140), 50)
    im.convert('RGB').save(path)


def storm(path):                                             # violet-green storm: spiral clouds, trees tipping, barges pulled into a huge whirlpool
    im = sky((60, 30, 90), (110, 170, 120), 1.2); d = Draw(W2, H2)
    for k in range(6): d.arc(1200, 260, 300 + k * 160, 90 + k * 40, 180 + k * 20, 330 + k * 20, (170, 140, 210, 200), 18)
    d.rect(0, 560, W2, H2, (50, 120, 110, 255)); d.stroke([(0, 560), (W2, 560)], LINE, 8)
    for x, t in ((150, -14), (420, -8), (1980, 10), (2260, 18)):
        tt = math.radians(t); d.stroke([(x, 600), (x + 260 * math.sin(tt), 600 - 260 * math.cos(tt))], dk((60, 110, 70, 255), 0.6), 30); d.ellipse(x + 270 * math.sin(tt), 600 - 270 * math.cos(tt), 130, 70, fill=(60, 110, 70, 255), outline=LINE, width=8)
    whirlpool(d, 1200, 790, 1080, 280, (90, 190, 160), (10, 50, 60))
    for x, y, a in ((700, 760, 16), (1720, 740, -20)):
        r = math.radians(a); pts = [(-140, -30), (140, -30), (110, 40), (-110, 40)]; d.poly([(x + u * math.cos(r) - v * math.sin(r), y + u * math.sin(r) + v * math.cos(r)) for u, v in pts], fill=(180, 70, 50, 255), outline=LINE, width=8)
    im.alpha_composite(d.out()); glow(im, 1200, 820, 300, (20, 40, 60, 90), 80); im.convert('RGB').save(path)


def falls(path):                                             # golden backlight: the canal pours over a cliff into the hole, spray and a rainbow
    im = sky((255, 200, 110), (255, 236, 190), 1.0); d = Draw(W2, H2)
    for k, c in enumerate(((240, 80, 80), (250, 160, 60), (250, 230, 80), (100, 200, 110), (80, 150, 230), (150, 100, 210))): d.arc(1200, 760, 900 - k * 34, 620 - k * 34, 180, 360, c + (200,), 34)
    d.poly([(0, 520), (2400, 520), (2400, 600), (1500, 640), (900, 640), (0, 600)], fill=(80, 150, 80, 255), outline=LINE, width=8)
    d.poly([(1020, 600), (1380, 600), (1340, 1100), (1060, 1100)], fill=(120, 200, 230, 255), outline=LINE, width=8)
    for k in range(9): x = 1050 + k * 37; d.stroke([(x, 610), (x - 10 + k * 3, 1090)], (240, 252, 255, 255), 8)
    d.rect(0, 640, 1020, H2, (110, 84, 60, 255)); d.rect(1380, 640, W2, H2, (110, 84, 60, 255)); d.stroke([(0, 640), (1020, 640)], LINE, 8); d.stroke([(1380, 640), (W2, 640)], LINE, 8)
    for x, y in ((1200, 1060), (1080, 1000), (1320, 1010)): d.ellipse(x, y, 200, 70, fill=(255, 255, 255, 220))
    im.alpha_composite(d.out()); glow(im, 1200, 300, 600, (255, 250, 220, 120), 90); glow(im, 1200, 1040, 360, (255, 255, 255, 150), 50); im.convert('RGB').save(path)


def saltmine(path):                                          # cross-section: lake + rig on top, layered pink salt below, lit tunnel rooms
    im = sky((120, 200, 255), (200, 236, 255), 1.0); d = Draw(W2, H2)
    d.rect(0, 150, W2, 260, (60, 150, 210, 255)); d.stroke([(0, 150), (W2, 150)], LINE, 8); derrick(d, 1400, 160, 130, 0)
    for k, c in enumerate(((246, 200, 214), (252, 232, 238), (226, 196, 236), (250, 220, 230))): d.rect(0, 260 + k * 210, W2, 470 + k * 210, c + (255,))
    for k in range(4): d.stroke([(x, 262 + k * 210 + 20 * math.sin(x / 140)) for x in range(0, W2 + 60, 60)], (255, 255, 255, 200), 6)
    for row, y in enumerate((440, 700, 940)):
        for x in range(120 + row * 90, W2 - 100, 300): d.rrect(x, y, x + 200, y + 120, 30, fill=(110, 70, 120, 255), outline=LINE, width=8); d.dot(x + 100, y + 30, 14, (255, 230, 120, 255))
    for y in range(270, 440, 40): d.stroke([(1400, y), (1400, y + 20)], (230, 60, 60, 255), 10)
    im.alpha_composite(d.out())
    for row, y in enumerate((440, 700, 940)):
        for x in range(120 + row * 90, W2 - 100, 600): glow(im, x + 100, y + 40, 80, (255, 230, 140, 110), 30)
    im.convert('RGB').save(path)


def tunnel(path):                                            # flooding salt tunnel: one-point perspective, lamps, a torrent from the roof
    im = sky((40, 110, 130), (150, 210, 220), 1.0); d = Draw(W2, H2); vx, vy = 1200, 520
    d.poly([(0, 0), (W2, 0), (vx + 260, vy - 160), (vx - 260, vy - 160)], fill=(236, 220, 230, 255), outline=LINE, width=8)
    for sg in (-1, 1): d.poly([(1200 + sg * 1200, 0), (1200 + sg * 1200, H2), (vx + sg * 260, vy + 160), (vx + sg * 260, vy - 160)], fill=(250, 236, 242, 255), outline=LINE, width=8)
    d.rrect(vx - 260, vy - 160, vx + 260, vy + 160, 10, fill=(30, 60, 80, 255), outline=LINE, width=8)
    for k in range(1, 5):
        f = k / 5; x0, x1 = 1200 - 1200 * (1 - f) - 260 * f, 1200 + 1200 * (1 - f) + 260 * f; y0, y1 = 0 + (vy - 160) * f, H2 - (H2 - vy - 160) * f
        d.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], outline=(200, 170, 190, 255), width=10); d.dot(1200, y0 + 30, 22, (255, 230, 120, 255))
    d.poly([(1040, 0), (1360, 0), (1520, 820), (880, 820)], fill=(70, 170, 220, 255), outline=LINE, width=8)
    for k in range(10): x = 1060 + k * 32; d.stroke([(x, 0), (x + (k - 4.5) * 50, 820)], (230, 250, 255, 255), 8)
    d.poly([(0, 820), (W2, 820), (W2, H2), (0, H2)], fill=(60, 150, 200, 255)); d.ellipse(1200, 830, 520, 90, fill=(240, 252, 255, 255))
    im.alpha_composite(d.out())
    for k in range(1, 5): glow(im, 1200, int((vy - 160) * k / 5 + 30), 90, (255, 230, 140, 120), 30)
    im.convert('RGB').save(path)


def escape(path):                                            # sunrise: rays, the mine headframe, trucks, a happy sky
    im = sky((255, 170, 90), (255, 236, 160), 1.0); d = Draw(W2, H2)
    for k in range(14): a = math.radians(180 + k * 13); d.poly([(1500, 640), (1500 + 1800 * math.cos(a - 0.04), 640 + 1800 * math.sin(a - 0.04)), (1500 + 1800 * math.cos(a + 0.04), 640 + 1800 * math.sin(a + 0.04))], fill=(255, 250, 210, 90))
    d.ellipse(1500, 640, 170, 170, fill=(255, 246, 200, 255))
    x0 = 620; d.stroke([(x0 - 160, 660), (x0, 160)], LINE, 26); d.stroke([(x0 + 160, 660), (x0, 160)], LINE, 26); d.stroke([(x0 - 160, 660), (x0, 160)], (90, 90, 110, 255), 14); d.stroke([(x0 + 160, 660), (x0, 160)], (90, 90, 110, 255), 14)
    d.ellipse(x0, 170, 70, 70, fill=(200, 80, 60, 255), outline=LINE, width=10); d.dot(x0, 170, 18, LINE)
    d.rect(0, 640, W2, H2, (120, 180, 80, 255)); d.stroke([(0, 640), (W2, 640)], LINE, 8)
    for x, c in ((1800, (230, 80, 60)), (2100, (60, 130, 210))): d.rrect(x, 560, x + 220, 650, 16, fill=c + (255,), outline=LINE, width=8); d.dot(x + 50, 660, 26, LINE); d.dot(x + 170, 660, 26, LINE)
    im.alpha_composite(d.out()); glow(im, 1500, 640, 360, (255, 250, 220, 150), 70); im.convert('RGB').save(path)


def gulf(path):                                              # turquoise Gulf: rows of waves, lighthouse, gulls, the canal mouth
    im = sky((60, 170, 230), (220, 250, 255), 1.0); d = Draw(W2, H2)
    clouds(d, [(500, 180, 1.0), (1500, 130, 0.8)])
    d.rect(0, 520, W2, H2, (30, 170, 190, 255)); d.stroke([(0, 520), (W2, 520)], LINE, 8)
    for j in range(7):
        y = 560 + j * 80
        for x in range(-60 + (j % 2) * 90, W2, 180): d.arc(x, y, 80, 22, 200, 340, (230, 255, 255, 255), 8)
    d.poly([(2000, 520), (2060, 200), (2120, 200), (2180, 520)], fill=WT, outline=LINE, width=8)
    for y in (280, 400): d.poly([(2000 + (520 - y) * 0.19, y), (2180 - (520 - y) * 0.19, y), (2180 - (560 - y) * 0.19, y + 40), (2000 + (560 - y) * 0.19, y + 40)], fill=(220, 60, 60, 255))
    d.rrect(2040, 150, 2140, 210, 12, fill=(255, 240, 150, 255), outline=LINE, width=8)
    for x, y in ((700, 300), (900, 250), (1200, 330)): d.stroke(bez((x - 50, y), (x - 25, y - 30), (x, y - 20), (x, y)) + bez((x, y), (x, y - 20), (x + 25, y - 30), (x + 50, y)), LINE, 8)
    d.poly([(700, H2), (1700, H2), (1350, 700), (1050, 700)], fill=(80, 200, 220, 255), outline=LINE, width=8)
    for k in range(6): d.stroke([(1100 + k * 40, 760 + k * 50), (1150 + k * 40, 700 + k * 50)], (240, 255, 255, 255), 8)
    im.alpha_composite(d.out()); glow(im, 2090, 180, 160, (255, 250, 200, 140), 40); im.convert('RGB').save(path)


def newlake(path):                                           # purple-gold dusk over the refilled lake: mirror water, sun column, island, first stars
    im = sky((70, 50, 130), (255, 170, 110), 1.1); d = Draw(W2, H2)
    for k in range(30): d.dot((k * 571) % W2, (k * 97) % 300 + 20, 4 + k % 3, (255, 250, 230, 230))
    d.ellipse(1000, 590, 150, 150, fill=(255, 220, 140, 255)); d.rect(0, 590, W2, H2, (110, 90, 160, 255)); d.stroke([(0, 590), (W2, 590)], LINE, 8)
    for k in range(9): w = 150 - k * 12; d.stroke([(1000 - w, 630 + k * 50), (1000 + w, 630 + k * 50)], (255, 210, 140, 255), 10)
    d.chord(1800, 600, 380, 90, 180, 360, fill=(70, 100, 80, 255), outline=LINE, width=8); cypress(d, 1720, 560, 260, (60, 110, 80, 255)); cypress(d, 1900, 560, 200, (60, 110, 80, 255))
    d.rect(330, 470, 470, 540, WT); d.poly([(310, 474), (400, 420), (490, 474)], fill=(200, 80, 70, 255), outline=LINE, width=8)
    im.alpha_composite(d.out()); glow(im, 1000, 590, 320, (255, 220, 160, 140), 70); im.convert('RGB').save(path)


def water(path, c1, c2, n=512):                              # flat water texture: base + ripple lines
    d = Draw(n, n, c1 + (255,))
    for k in range(18): x, y = (k * 197) % n, (k * 89) % n; d.stroke([(x, y), (x + 60, y)], c2 + (255,), 6)
    d.out().convert('RGB').save(path, quality=92)


def swirltex(path, c1, c2, n=1024):                          # the whirlpool seen from above: spiral foam arms into a dark eye
    im = Image.new('RGBA', (n, n), c1 + (255,)); g = np.mgrid[0:n, 0:n]; r = np.hypot(g[0] - n / 2, g[1] - n / 2) / (n / 2)
    col = np.array(c1)[None, None] * np.clip(r, 0, 1)[..., None] + np.array(c2)[None, None] * (1 - np.clip(r, 0, 1))[..., None]
    im = Image.fromarray(np.dstack([col.astype(np.uint8), np.full((n, n), 255, np.uint8)])); d = Draw(n, n)
    for arm in range(5):
        pts = [(n / 2 + (n * 0.48) * (1 - u) * math.cos(arm * 1.2566 + u * 7), n / 2 + (n * 0.48) * (1 - u) * math.sin(arm * 1.2566 + u * 7)) for u in np.linspace(0, 0.93, 80)]
        d.stroke(pts, (236, 255, 255, 230), 22)
    d.dot(n / 2, n / 2, n * 0.05, (8, 20, 36, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path, quality=92)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in ('fisher', 'driller', 'miner'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'shouting')]
    multi = dict(pizza={'default': pizza(), 'shocked': pizza('shocked')}, rig={'default': rig()}, barge={'default': barge()}, bit={'default': drillbit()},
                 pole={'default': pole()}, gull={'default': gull()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    BLUE2, DEEP = (40, 110, 190, 255), (20, 60, 90, 255)
    cards = dict(pizzahole=plaque('PIZZA-SIZED HOLE', 'SWALLOWED A LAKE!', (210, 60, 40, 255), WHITE, 1000, border=GOLDL, bs=120, ss=86, sc=GOLDL),
                 entire=stamp('AN ENTIRE LAKE!', 960, BLUE2, 110, -4), date=calendar(),
                 texaco=plaque('TEXACO', 'WAS DRILLING', (200, 40, 40, 255), WHITE, 860, border=GOLDL, bs=190, ss=84, sc=GOLDL),
                 lakename=plaque('LAKE PEIGNEUR', 'LOUISIANA', (30, 120, 170, 255), WHITE, 980, border=GOLDL, bs=130, ss=84, sc=GOLDL),
                 ft10=plaque('10 FEET', 'DEEP', (40, 150, 200, 255), WHITE, 820, border=WHITE, bs=200, ss=90, sc=GOLDL),
                 inch14=plaque('14-INCH DRILL', 'GOT STUCK!', (60, 66, 84, 255), YEL, 980, border=YEL, bs=130, ss=96, sc=WHITE),
                 spin=stamp('IT STARTED TO SPIN!', 1040, (110, 60, 170, 255), 96, 4),
                 rigsw=plaque('THE RIG', 'SWALLOWED!', (200, 60, 50, 255), WHITE, 860, border=GOLDL, bs=180, ss=90, sc=GOLDL),
                 backward=stamp('CANAL FLOWED BACKWARD!', 1080, (40, 140, 90, 255), 86, -4),
                 falls150=neon('150-FOOT', 'WATERFALL!', 920, (120, 220, 255, 255), GOLDL),
                 saltmine=plaque('SALT MINE', 'RIGHT UNDER THE LAKE', (220, 110, 160, 255), WHITE, 980, border=WHITE, bs=170, ss=74, sc=(255, 240, 160, 255)),
                 tunnels=stamp('STRAIGHT INTO ITS TUNNELS!', 1100, (220, 60, 60, 255), 80, 3),
                 drained=plaque('THE WHOLE LAKE', 'DRAINED DOWN', DEEP, (120, 220, 255, 255), 980, border=(120, 220, 255, 255), bs=120, ss=96, sc=WHITE),
                 miners55=plaque('55 MINERS', 'RAN!', (40, 90, 180, 255), WHITE, 900, border=YEL, bs=170, ss=100, sc=YEL),
                 escaped=neon('ALL 55', 'ESCAPED!', 900, LIME, GOLDL),
                 gulf=plaque('SALT WATER', 'FROM THE GULF', (20, 150, 170, 255), WHITE, 960, border=WHITE, bs=160, ss=84, sc=(255, 240, 160, 255)),
                 still=plaque('LAKE PEIGNEUR', 'IS STILL THERE', (90, 60, 150, 255), WHITE, 980, border=GOLDL, bs=130, ss=84, sc=GOLDL),
                 notsame=stamp('NOT THE SAME LAKE', 1000, (230, 110, 40, 255), 100, -4))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (120, 150, 140), (104, 134, 126))
    water(T('lake.jpg'), (50, 150, 160), (120, 210, 210)); water(T('lily.jpg'), (110, 160, 170), (180, 220, 220)); water(T('noon.jpg'), (80, 170, 225), (200, 240, 255))
    water(T('stormw.jpg'), (60, 120, 110), (140, 200, 180)); water(T('canal.jpg'), (90, 180, 200), (220, 250, 255)); water(T('flood.jpg'), (60, 150, 200), (200, 240, 255))
    water(T('sea.jpg'), (40, 180, 200), (210, 255, 255)); water(T('dusk.jpg'), (120, 100, 170), (255, 200, 150))
    CE.tiles(T('steel.jpg'), (110, 120, 136), (96, 106, 122)); CE.tiles(T('salt.jpg'), (246, 220, 230), (232, 204, 220)); B.tex_grass(T('grass.jpg'))
    swirltex(T('swirl.jpg'), (60, 170, 170), (8, 40, 60)); swirltex(T('swirl2.jpg'), (80, 170, 140), (10, 40, 50))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(whirlbg=whirlbg, bayou=bayou, lakenoon=lakenoon, deck=deck, storm=storm, falls=falls, saltmine=saltmine, tunnel=tunnel, escape=escape, gulf=gulf, newlake=newlake)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
