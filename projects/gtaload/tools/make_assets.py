#!/usr/bin/env python3
"""Assets for video 12 (GTA Online's loading screen beat Rockstar for 7 years - t0st killed it), drawn in code.
New cute cast: the gamer kid (orange hoodie), t0st (beanie, headphones, round glasses, violet hoodie), the Rockstar rep (emerald
suit, bob), the cop (police cap).  Hero props: the LOADING-BAR BOSS (angry / defeated), the checker robot (happy / dizzy), the
hourglass, the giant file, the cheque, the wall clock, the police car.  Ten sets, each its own palette: AR boss arena (violet +
orange), LV lounge (warm amber afternoon), HG hourglass desert (mint + peach), RM t0st's snowy night room (navy + pink LEDs),
CY cyber city inside the code (neon green + cyan), FL file archive (gold + wood), CK checking factory (teal + hazard yellow),
SP sunny finish line (sky blue + grass), HQ award stage (emerald + gold), ST night street (blue + police red).
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

ROOT = B.ROOT; RED, GOLD, BLUE = LA.RED, LA.GOLD, LA.BLUE
dk, glow, plaque, stamp, neon, bubble, fit = LA.dk, CE.glow, LA.plaque, LA.stamp, LA.neon, LA.bubble, LA.fit
ORNG, VIO, EMER, NAVY, PINK, CYAN, GOLDL, LIME = (250, 140, 50, 255), (120, 80, 210, 255), (20, 130, 96, 255), (40, 62, 150, 255), (255, 80, 170, 255), (60, 230, 240, 255), (255, 214, 96, 255), (120, 230, 90, 255)
LA.NEW.update({
    'kid': dict(sk=1, style='curly', hair=(96, 54, 30, 255), suit=ORNG, shade=(214, 110, 36, 255), body='hoodie', freck=1),
    'toast': dict(sk=0, style='side', hair=(60, 40, 30, 255), suit=VIO, shade=(92, 60, 176, 255), body='hoodie', glasses=1, beanie=(40, 170, 160, 255)),
    'rep': dict(sk=2, style='bob', hair=(30, 24, 30, 255), suit=EMER, shade=(14, 100, 74, 255), body='suit', tie=GOLD, band=GOLD),
    'cop': dict(sk=0, style='part', hair=(232, 190, 90, 255), suit=NAVY, shade=(30, 46, 118, 255), body='suit', tie=LINE, cap=1),
})


def head(char, expr):
    im = LA.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx = 230
    if c.get('beanie'):                                      # knitted beanie + pompom + headphones
        col = c['beanie']; d.chord(cx, 196, 214, 168, 180, 360, fill=col, outline=LINE, width=18)
        for k in range(7): d.stroke([(cx - 150 + k * 50, 70 + abs(k - 3) * 14), (cx - 150 + k * 50, 160)], dk(col, 0.8), 8)
        d.rrect(cx - 220, 150, cx + 220, 204, 26, fill=dk(col, 0.82), outline=LINE, width=14); d.ellipse(cx, 36, 40, 36, fill=(250, 250, 240, 255), outline=LINE, width=12)
        d.arc(cx, 250, 228, 226, 200, 340, LINE, 22); d.arc(cx, 250, 228, 226, 200, 340, (255, 90, 160, 255), 12)
        for sg in (-1, 1): d.rrect(cx + sg * 206 - 30, 230, cx + sg * 206 + 30, 340, 24, fill=(255, 90, 160, 255), outline=LINE, width=12)
    if c.get('cap'):                                         # police cap: crown, black visor, gold badge
        d.poly([(cx - 200, 172), (cx + 200, 172), (cx + 236, 62), (cx - 236, 62)], fill=NAVY, outline=LINE, width=16)
        d.rect(cx - 196, 140, cx + 196, 166, (230, 230, 240, 255)); d.chord(cx, 172, 206, 48, 0, 180, fill=(30, 30, 40, 255), outline=LINE, width=12)
        d.poly([(cx, 76), (cx + 30, 100), (cx + 20, 132), (cx - 20, 132), (cx - 30, 100)], fill=GOLDL, outline=LINE, width=8)
    im.alpha_composite(d.out()); return im


def body(char):
    c = LA.NEW[char]
    if c['body'] != 'hoodie': return LA.body(char)
    im = LA.body(char); d = Draw(im.width, im.height); col = c['suit']
    d.chord(230, 462, 136, 62, 180, 360, fill=dk(col, 0.78), outline=LINE, width=12)
    for sg in (-1, 1): d.stroke([(230 + sg * 34, 478), (230 + sg * 40, 570)], (250, 246, 236, 255), 9); d.dot(230 + sg * 40, 574, 11, (250, 246, 236, 255))
    d.rrect(140, 650, 320, 744, 34, fill=dk(col, 0.86), outline=LINE, width=10)
    if char == 'toast':                                      # a tiny toast slice on the hoodie
        d.rrect(196, 590, 264, 646, 22, fill=(232, 170, 90, 255), outline=LINE, width=7); d.rrect(206, 600, 254, 638, 16, fill=(255, 226, 160, 255))
    im.alpha_composite(d.out()); return im


# ------------------------------------------------------------------ hero props
def boss(face='default'):                                    # the LOADING BAR BOSS
    W_, H_ = 1100, 1320; d = Draw(W_, H_); bod = (92, 52, 150, 255) if face == 'default' else (120, 110, 150, 255)
    for sg in (-1, 1): d.poly([(550 + sg * 300, 360), (550 + sg * 380, 150), (550 + sg * 180, 340)], fill=(255, 230, 200, 255), outline=LINE, width=14)
    for sg in (-1, 1): d.ellipse(550 + sg * 430, 820, 80, 120, fill=bod, outline=LINE, width=14)
    for x in (380, 720): d.rrect(x - 110, 1150, x + 110, 1290, 40, fill=dk(bod, 0.7), outline=LINE, width=14)
    d.rrect(150, 320, 950, 1190, 150, fill=bod, outline=LINE, width=18); d.rrect(190, 360, 600, 520, 70, fill=(255, 255, 255, 40))
    for k in range(10):                                      # spinner crown
        a = math.radians(-90 + k * 36); r = 16 + k * 3.4; cl = (255, 160 + k * 8, 60, 255) if face == 'default' else (170, 170, 180, 255)
        d.dot(550 + 150 * math.cos(a), 170 + 150 * math.sin(a), r, cl); d.ellipse(550 + 150 * math.cos(a), 170 + 150 * math.sin(a), r, r, outline=LINE, width=6)
    d.rrect(240, 930, 860, 1060, 46, fill=(28, 18, 44, 255), outline=LINE, width=14)
    full = 0.36 if face == 'default' else 1.0; x1 = 262 + (838 - 262) * full
    d.rrect(262, 952, x1, 1038, 34, fill=ORNG if face == 'default' else LIME)
    for x in range(290, int(x1) - 20, 64): d.poly([(x, 1038), (x + 30, 1038), (x + 60, 952), (x + 30, 952)], fill=(255, 255, 255, 70))
    if face == 'default':
        for x in (400, 700): d.ellipse(x, 600, 112, 120, fill=WHITE, outline=LINE, width=16); d.dot(x + (18 if x < 550 else -18), 630, 56, LINE); d.dot(x + (36 if x < 550 else 0), 600, 18, WHITE)
        for sg in (-1, 1): d.stroke([(550 + sg * 280, 440), (550 + sg * 60, 500)], LINE, 40)
        d.chord(550, 760, 250, 150, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=16)
        for k in range(6): x = 330 + k * 75; d.poly([(x, 760), (x + 36, 830), (x + 72, 760)], fill=WHITE, outline=LINE, width=6)
        for sg in (-1, 1): d.ellipse(550 + sg * 270, 730, 46, 26, fill=(255, 120, 150, 140))
    else:                                                    # defeated: X eyes, wobbly mouth, sweat
        for x in (400, 700):
            for s2 in (-1, 1): d.stroke([(x - 70, 540), (x + 70, 660)][::s2] if s2 > 0 else [(x - 70, 660), (x + 70, 540)], LINE, 28)
        d.stroke([(400 + k * 30, 800 + (14 if k % 2 else -14)) for k in range(11)], LINE, 18)
        d.ellipse(900, 450, 34, 50, fill=(150, 210, 255, 255), outline=LINE, width=8)
    return d.out()


def robot(face='default'):                                   # cute checker robot with a clipboard
    d = Draw(900, 1200); d.stroke([(450, 130), (450, 50)], LINE, 14); d.dot(450, 46, 34, RED); d.ellipse(450, 46, 34, 34, outline=LINE, width=10)
    d.rrect(300, 990, 600, 1110, 40, fill=(70, 74, 90, 255), outline=LINE, width=14)
    for x in (350, 450, 550): d.dot(x, 1110, 40, (40, 40, 50, 255)); d.ellipse(x, 1110, 40, 40, outline=LINE, width=10)
    d.rrect(250, 550, 650, 1000, 90, fill=ORNG, outline=LINE, width=16); d.rrect(330, 640, 570, 820, 30, fill=(255, 220, 160, 255), outline=LINE, width=10)
    for k, c in enumerate((RED, LIME, BLUE)): d.dot(380 + k * 70, 890, 26, c); d.ellipse(380 + k * 70, 890, 26, 26, outline=LINE, width=7)
    d.ellipse(190, 760, 60, 110, fill=(200, 210, 230, 255), outline=LINE, width=12)
    d.rrect(560, 620, 820, 960, 20, fill=(240, 220, 170, 255), outline=LINE, width=12); d.rect(640, 600, 740, 650, (170, 170, 180, 255))
    for j in range(5): y = 690 + j * 52; d.stroke([(640, y), (790, y)], (150, 140, 120, 255), 10); d.stroke([(586, y - 4), (600, y + 10), (624, y - 16)], (40, 160, 70, 255), 8)
    d.ellipse(760, 800, 60, 100, fill=(200, 210, 230, 255), outline=LINE, width=12)
    d.rrect(200, 120, 700, 540, 100, fill=(196, 214, 236, 255), outline=LINE, width=16); d.rrect(250, 180, 650, 470, 70, fill=(24, 36, 70, 255), outline=LINE, width=10)
    for sg in (-1, 1): d.ellipse(450 + sg * 140, 410, 34, 20, fill=(255, 120, 160, 160))
    if face == 'default':
        for x in (365, 535): d.ellipse(x, 300, 42, 52, fill=CYAN); d.dot(x + 12, 284, 13, WHITE)
        d.arc(450, 370, 70, 44, 20, 160, CYAN, 14)
    else:
        for x in (365, 535):
            pts = [(x + math.cos(a) * a * 6, 310 + math.sin(a) * a * 6) for a in np.linspace(0, 4 * math.pi, 40)]; d.stroke(pts, CYAN, 9)
        d.stroke([(390 + k * 20, 400 + (10 if k % 2 else -10)) for k in range(7)], CYAN, 10)
    return d.out()


def hourglass():
    d = Draw(800, 1300); WD = (150, 96, 56, 255)
    for x in (150, 650): d.rrect(x - 26, 120, x + 26, 1180, 14, fill=WD, outline=LINE, width=10)
    gl = bez((190, 150), (180, 520), (390, 560), (390, 650)) + bez((390, 650), (390, 740), (180, 780), (190, 1150))
    gr = [(800 - x, y) for x, y in gl[::-1]]; d.poly(gl + gr, fill=(200, 236, 255, 140), outline=LINE, width=12)
    sand = (240, 190, 90, 255); d.poly(bez((230, 420), (300, 540), (400, 600), (400, 640)) + bez((400, 640), (400, 600), (500, 540), (570, 420)), fill=sand)
    d.stroke([(400, 640), (400, 1060)], sand, 12); d.chord(400, 1150, 200, 120, 180, 360, fill=sand, outline=dk(sand, 0.8), width=6)
    for y in (60, 1180): d.rrect(80, y, 720, y + 80, 30, fill=WD, outline=LINE, width=14); d.rect(110, y + 14, 690, y + 24, (200, 140, 90, 255))
    d.stroke(bez((250, 200), (230, 320), (250, 400), (290, 440)), (255, 255, 255, 170), 14); return d.out()


def bigfile():
    d = Draw(900, 1150); pg = (252, 248, 236, 255)
    d.poly([(80, 40), (620, 40), (820, 240), (820, 1110), (80, 1110)], fill=pg, outline=LINE, width=16)
    d.poly([(620, 40), (620, 240), (820, 240)], fill=(214, 206, 186, 255), outline=LINE, width=12)
    d.rrect(140, 110, 480, 230, 30, fill=VIO, outline=LINE, width=10); d.text(310, 170, '{ }', 92, WHITE, stroke=5, stroke_fill=LINE)
    R_ = np.random.RandomState(3); cols = [(255, 120, 160, 255), (80, 170, 255, 255), (240, 170, 50, 255), (90, 190, 120, 255)]
    for j in range(15):
        y = 300 + j * 52; x = 150 + (j % 3) * 40; w = R_.randint(160, 480)
        d.rrect(x, y, x + w, y + 24, 12, fill=cols[j % 4]); d.rrect(x + w + 20, y, x + w + 20 + R_.randint(60, 160), y + 24, 12, fill=(180, 176, 190, 255))
    return d.out()


def cheque():
    d = Draw(1300, 640); d.rrect(16, 16, 1284, 624, 30, fill=(214, 240, 210, 255), outline=LINE, width=16); d.rrect(46, 46, 1254, 594, 18, outline=EMER, width=8)
    for k in range(9): d.stroke([(60 + k * 140, 540), (130 + k * 140, 500)], (180, 220, 180, 255), 6)
    d.text(330, 120, 'PAY: t0st', 66, LINE); d.text(1000, 120, 'ROCKSTAR', 56, EMER)
    d.rrect(200, 210, 1100, 420, 26, fill=WHITE, outline=LINE, width=10); d.text(650, 318, '$10,000', fit('$10,000', 190, 860), (20, 120, 60, 255), stroke=6, stroke_fill=LINE)
    d.stroke(bez((800, 520), (860, 440), (900, 560), (1000, 470)) + bez((1000, 470), (1040, 450), (1080, 520), (1160, 480)), LINE, 8); return d.out()


def wallclock():
    d = Draw(760, 760); d.ellipse(380, 380, 340, 340, fill=RED, outline=LINE, width=18); d.ellipse(380, 380, 280, 280, fill=(255, 250, 236, 255), outline=LINE, width=12)
    for k in range(12): a = math.radians(k * 30); d.stroke([(380 + 230 * math.cos(a), 380 + 230 * math.sin(a)), (380 + 262 * math.cos(a), 380 + 262 * math.sin(a))], LINE, 14 if k % 3 == 0 else 8)
    d.stroke([(380, 380), (380, 170)], LINE, 18); d.stroke([(380, 380), (520, 470)], LINE, 22); d.dot(380, 380, 26, GOLDL); d.ellipse(380, 380, 26, 26, outline=LINE, width=8)
    for x in (280, 480): d.dot(x, 300, 22, LINE)
    d.arc(380, 520, 70, 30, 200, 340, LINE, 12); return d.out()


def copcar():
    d = Draw(1400, 760); d.rrect(60, 300, 1340, 600, 110, fill=WHITE, outline=LINE, width=18); d.rect(80, 430, 1320, 520, NAVY)
    d.rrect(300, 120, 1060, 340, 90, fill=WHITE, outline=LINE, width=18)
    for x0, x1 in ((360, 660), (700, 1000)): d.rrect(x0, 160, x1, 320, 50, fill=(150, 210, 245, 255), outline=LINE, width=10)
    d.rrect(560, 60, 680, 130, 20, fill=RED, outline=LINE, width=10); d.rrect(680, 60, 800, 130, 20, fill=(60, 120, 255, 255), outline=LINE, width=10)
    d.poly([(680, 360), (720, 400), (700, 460), (660, 460), (640, 400)], fill=GOLDL, outline=LINE, width=8)
    for x in (330, 1070): d.dot(x, 610, 120, (40, 40, 50, 255)); d.ellipse(x, 610, 120, 120, outline=LINE, width=14); d.dot(x, 610, 50, (190, 190, 200, 255))
    d.dot(1300, 380, 30, (255, 240, 160, 255)); return d.out()


def calendar21():
    d = Draw(720, 800); d.rrect(20, 60, 700, 780, 40, fill=(255, 246, 236, 255), outline=LINE, width=18); d.rrect(20, 60, 700, 270, 40, fill=(40, 170, 160, 255), outline=LINE, width=18)
    d.rect(38, 220, 682, 270, (40, 170, 160, 255)); d.stroke([(20, 270), (700, 270)], LINE, 14); d.text(360, 168, 'EARLY', 120, WHITE, stroke=6, stroke_fill=LINE)
    for x in (200, 520): d.rrect(x - 22, 20, x + 22, 120, 18, fill=(150, 150, 160, 255), outline=LINE, width=10)
    d.text(360, 520, '2021', 230, (255, 80, 150, 255), stroke=10, stroke_fill=LINE)
    for x, y in ((90, 700), (630, 700), (630, 340)):
        for a in range(3): r = math.radians(a * 60); d.stroke([(x - 26 * math.cos(r), y - 26 * math.sin(r)), (x + 26 * math.cos(r), y + 26 * math.sin(r))], (120, 190, 230, 255), 7)
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
W2, H2 = 2400, 1100


def spinner(d, x, y, r, col, n=10, s=1.0):
    for k in range(n): a = math.radians(-90 + k * 360 / n); d.dot(x + r * math.cos(a), y + r * math.sin(a), (10 + k * 3) * s, col)


def arena(path):                                             # boss arena at violet dusk: tiers of glowing arches, floodlights, a huge spinner in the sky
    im = CA.gradient((40, 14, 80), (255, 130, 70), W2, H2, 1.2).convert('RGBA'); d = Draw(W2, H2)
    spinner(d, 1200, 260, 170, (255, 214, 140, 255), 12, 1.6)
    for row, (y0, h, c) in enumerate(((430, 260, (70, 30, 90, 255)), (640, 240, (54, 22, 74, 255)))):
        d.rect(0, y0, W2, y0 + h, c); d.stroke([(0, y0), (W2, y0)], LINE, 10)
        for x in range(30 + row * 70, W2, 160): LA.arch(d, x, x + 100, y0 + 40, y0 + h - 20, (255, 150, 70, 255) if (x // 160 + row) % 3 else (255, 210, 110, 255), width=8)
    for x in (140, 2260): d.rect(x - 24, 240, x + 24, 880, (40, 20, 50, 255)); d.rrect(x - 90, 200, x + 90, 270, 20, fill=(255, 240, 200, 255), outline=LINE, width=10)
    d.rect(0, 880, W2, H2, (60, 26, 84, 255)); d.stroke([(0, 880), (W2, 880)], LINE, 8)
    for k in range(-8, 9): d.stroke([(1200 + k * 60, 880), (1200 + k * 260, H2)], (110, 60, 150, 255), 6)
    im.alpha_composite(d.out()); glow(im, 1200, 260, 260, (255, 200, 120, 120), 60)
    for x in (140, 2260): glow(im, x, 235, 200, (255, 240, 200, 150), 50)
    im.convert('RGB').save(path)


def lounge(path):                                            # warm afternoon lounge: sunny window, TV with a spinner, plants, shelves
    im = Image.new('RGBA', (W2, H2), (238, 178, 120, 255)); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 40, 900, (246, 194, 140, 255))
    d.rrect(120, 140, 700, 640, 16, fill=(130, 200, 255, 255), outline=(255, 246, 230, 255), width=26); d.dot(560, 270, 70, (255, 240, 170, 255))
    d.ellipse(330, 560, 200, 150, fill=(110, 180, 90, 255)); d.stroke([(410, 140), (410, 640)], (255, 246, 230, 255), 16)
    d.rrect(880, 220, 1640, 680, 30, fill=(40, 34, 44, 255), outline=LINE, width=16); d.rrect(920, 256, 1600, 644, 20, fill=(60, 40, 100, 255))
    spinner(d, 1260, 450, 90, (255, 214, 140, 255), 10, 1.2); d.rect(1180, 680, 1340, 720, (40, 34, 44, 255))
    d.rect(1800, 300, 2300, 330, (150, 96, 60, 255)); d.rect(1800, 520, 2300, 550, (150, 96, 60, 255))
    for k, x in enumerate((1850, 1960, 2080, 2200)):
        d.rrect(x - 40, 230, x + 40, 300, 12, fill=[RED, BLUE, ORNG, EMER][k], outline=LINE, width=6); d.ellipse(x, 470, 46, 50, fill=(90, 170, 90, 255), outline=LINE, width=6); d.rect(x - 30, 480, x + 30, 520, (200, 110, 70, 255))
    d.rect(0, 900, W2, H2, (170, 110, 70, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1260, 450, 300, (160, 120, 255, 90), 70); glow(im, 410, 390, 360, (255, 240, 200, 110), 80); im.convert('RGB').save(path)


def desert(path):                                            # surreal golden desert: mint sky, floating clocks, pink dunes, cacti
    im = CA.gradient((150, 226, 214), (255, 206, 160), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2); d.dot(1700, 330, 170, (255, 246, 210, 255))
    for x, y, r in ((400, 240, 70), (900, 160, 50), (2100, 200, 60), (1300, 420, 40)):
        d.ellipse(x, y, r, r, fill=(255, 250, 236, 255), outline=LINE, width=8); d.stroke([(x, y), (x, y - r * 0.7)], LINE, 7); d.stroke([(x, y), (x + r * 0.5, y + r * 0.2)], LINE, 7)
    for y0, c in ((640, (246, 160, 150, 255)), (740, (240, 180, 130, 255)), (850, (230, 150, 110, 255))):
        d.poly([(0, H2), (0, y0)] + [(x, y0 + 50 * math.sin(x / 260.0 + y0)) for x in range(0, W2 + 1, 60)] + [(W2, H2)], fill=c, outline=LINE, width=8)
    for x, s in ((300, 1.0), (2050, 1.2), (1500, 0.7)):
        d.rrect(x - 36 * s, 860 - 300 * s, x + 36 * s, 870, 30 * s, fill=(70, 160, 100, 255), outline=LINE, width=8)
        for sg in (-1, 1): d.rrect(x + sg * 60 * s - 22 * s, 860 - 220 * s, x + sg * 60 * s + 22 * s, 860 - 110 * s, 18 * s, fill=(70, 160, 100, 255), outline=LINE, width=7)
    im.alpha_composite(d.out()); glow(im, 1700, 330, 260, (255, 250, 220, 140), 60); im.convert('RGB').save(path)


def winter(path):                                            # t0st's room on a snowy night: big window, moon, roofs, pink LED strip, shelf
    im = Image.new('RGBA', (W2, H2), (34, 38, 84, 255)); d = Draw(W2, H2)
    d.rrect(260, 130, 1260, 700, 16, fill=(24, 40, 100, 255), outline=(200, 200, 230, 255), width=24); d.dot(1060, 260, 60, (255, 250, 220, 255))
    for k in range(5): x = 300 + k * 200; d.poly([(x, 700), (x, 560), (x + 90, 480), (x + 180, 560), (x + 180, 700)], fill=(60, 50, 90, 255), outline=LINE, width=6); d.chord(x + 90, 520, 96, 30, 180, 360, fill=WHITE)
    R_ = np.random.RandomState(9)
    for _ in range(60): d.dot(280 + R_.rand() * 960, 150 + R_.rand() * 540, 4 + R_.rand() * 5, WHITE)
    d.stroke([(760, 130), (760, 700)], (200, 200, 230, 255), 14)
    for x, c in ((1420, (255, 120, 180, 255)), (1700, (120, 200, 255, 255))): d.rrect(x, 180, x + 220, 480, 10, fill=c, outline=LINE, width=8); d.dot(x + 110, 300, 60, dk(c, 0.7))
    d.rect(1980, 520, 2350, 550, (110, 80, 120, 255))
    for k, x in enumerate((2020, 2110, 2200, 2290)): d.ellipse(x, 470, 34, 46, fill=[ORNG, LIME, PINK, CYAN][k], outline=LINE, width=6)
    d.rect(0, 40, W2, 60, (255, 120, 200, 255)); d.rect(0, 920, W2, H2, (50, 40, 70, 255)); d.stroke([(0, 920), (W2, 920)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1200, 50, 1300, (255, 100, 200, 90), 40); glow(im, 1060, 260, 140, (255, 250, 220, 120), 40); im.convert('RGB').save(path)


def cyber(path):                                             # inside the code: neon data towers, circuit traces, grid floor
    im = CA.gradient((6, 10, 30), (20, 40, 80), W2, H2, 1.0).convert('RGBA'); g = Draw(W2, H2); R_ = np.random.RandomState(5); x = 20
    while x < W2:
        w, h = R_.randint(110, 220), R_.randint(260, 640); c = [CYAN, LIME, (190, 120, 255, 255)][R_.randint(3)]
        g.rrect(x, 880 - h, x + w, 880, 10, fill=(14, 24, 50, 255), outline=c, width=6)
        for j in range(int(h / 50)): g.rect(x + 16, 900 - h + j * 50, x + 16 + R_.randint(20, w - 30), 912 - h + j * 50, c)
        x += w + R_.randint(30, 90)
    for k in range(9):
        y = 120 + k * 30; x0 = R_.randint(0, 1800); g.stroke([(x0, y), (x0 + 300, y), (x0 + 360, y + 60)], CYAN, 5); g.dot(x0 + 360, y + 60, 10, LIME)
    g.rect(0, 880, W2, H2, (10, 16, 36, 255))
    for k in range(-10, 11): g.stroke([(1200 + k * 50, 880), (1200 + k * 300, H2)], CYAN, 4)
    for y in (910, 960, 1030): g.stroke([(0, y), (W2, y)], CYAN, 4)
    im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(8))); im.alpha_composite(g.out()); glow(im, 1200, 600, 700, (60, 200, 255, 60), 80); im.convert('RGB').save(path)


def archive(path):                                           # the giant file archive: towering shelves of folders, warm lamps, ladder
    im = Image.new('RGBA', (W2, H2), (110, 66, 40, 255)); d = Draw(W2, H2); R_ = np.random.RandomState(7)
    cols = [(220, 80, 70, 255), (240, 180, 60, 255), (90, 150, 210, 255), (110, 170, 100, 255), (230, 140, 170, 255), (250, 230, 200, 255)]
    for b in range(5):
        x0 = 30 + b * 475; d.rect(x0, 60, x0 + 440, 900, (80, 46, 28, 255)); d.poly([(x0, 60), (x0 + 440, 60), (x0 + 440, 900), (x0, 900)], outline=LINE, width=10)
        for r in range(6):
            y1 = 200 + r * 130; d.rect(x0 + 10, y1, x0 + 430, y1 + 16, (160, 104, 60, 255)); x = x0 + 18
            while x < x0 + 410: w = R_.randint(18, 34); h = R_.randint(80, 116); d.rect(x, y1 - h, x + w, y1, cols[R_.randint(6)]); x += w + 3
    for x in (520, 1420): d.stroke([(x, 900), (x + 90, 120)], (190, 130, 70, 255), 16); d.stroke([(x + 100, 900), (x + 190, 120)], (190, 130, 70, 255), 16)
    for x in (520, 1420):
        for k in range(8): y = 860 - k * 95; d.stroke([(x + k * 11, y), (x + 100 + k * 11, y)], (190, 130, 70, 255), 12)
    for x in (420, 1200, 1980): d.stroke([(x, 0), (x, 70)], LINE, 6); d.chord(x, 110, 70, 50, 180, 360, fill=(240, 190, 60, 255), outline=LINE, width=8)
    d.rect(0, 900, W2, H2, (150, 96, 60, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    im.alpha_composite(d.out())
    for x in (420, 1200, 1980): glow(im, x, 140, 220, (255, 220, 140, 120), 50)
    im.convert('RGB').save(path)


def gear(d, x, y, r, col, n=10):
    pts = []
    for k in range(n * 2): a = math.radians(k * 180 / n); rr = r if k % 2 else r * 0.82; pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d.poly(pts, fill=col, outline=LINE, width=8); d.dot(x, y, r * 0.3, dk(col, 0.7)); d.ellipse(x, y, r * 0.3, r * 0.3, outline=LINE, width=6)


def factory(path):                                           # checking factory: teal steel, gears, pipes, hazard stripes, warning lamps
    im = CA.gradient((40, 100, 110), (90, 150, 150), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.rect(x, 0, x + 12, 880, (30, 80, 90, 255))
    gear(d, 300, 300, 200, (240, 190, 50, 255), 12); gear(d, 560, 470, 120, (250, 140, 60, 255), 9); gear(d, 2050, 330, 230, (240, 190, 50, 255), 14)
    for y, c in ((160, (200, 80, 70, 255)), (210, (170, 180, 190, 255))): d.rect(800, y, 1700, y + 34, c); d.poly([(800, y), (1700, y), (1700, y + 34), (800, y + 34)], outline=LINE, width=6)
    d.rect(700, 520, 1800, 640, (60, 64, 76, 255)); d.poly([(700, 520), (1800, 520), (1800, 640), (700, 640)], outline=LINE, width=8)
    for x in range(720, 1780, 140): d.rrect(x, 440, x + 100, 520, 10, fill=[(240, 230, 210, 255), (255, 200, 120, 255), (170, 220, 255, 255)][(x // 140) % 3], outline=LINE, width=6)
    for x in range(0, W2, 80): d.poly([(x, 820), (x + 40, 820), (x + 80, 880), (x + 40, 880)], fill=(250, 210, 40, 255))
    d.rect(0, 880, W2, H2, (70, 84, 90, 255)); d.stroke([(0, 880), (W2, 880)], LINE, 8)
    for x in (700, 1800): d.dot(x, 380, 40, (255, 120, 40, 255)); d.ellipse(x, 380, 40, 40, outline=LINE, width=8)
    im.alpha_composite(d.out())
    for x in (700, 1800): glow(im, x, 380, 160, (255, 140, 40, 130), 40)
    im.convert('RGB').save(path)


def finish(path):                                            # sunny finish line: blue sky, clouds, green hills, checkered arch, flags
    im = CA.gradient((70, 150, 250), (200, 236, 255), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2); d.dot(2100, 170, 90, (255, 246, 190, 255))
    for x, y, s in ((300, 200, 1.0), (1100, 130, 0.8), (1700, 260, 1.1)):
        for dx, r in ((-90, 70), (0, 100), (100, 75)): d.dot(x + dx * s, y, r * s, WHITE)
    for y0, c in ((640, (120, 200, 90, 255)), (740, (90, 180, 80, 255))):
        d.poly([(0, H2), (0, y0)] + [(x, y0 - 70 * math.sin(x / 400.0 + y0)) for x in range(0, W2 + 1, 60)] + [(W2, H2)], fill=c, outline=LINE, width=8)
    d.poly([(0, 900), (W2, 900), (W2, H2), (0, H2)], fill=(120, 120, 136, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    for x in (700, 1700): d.rect(x - 22, 260, x + 22, 900, (230, 230, 240, 255)); d.poly([(x - 22, 260), (x + 22, 260), (x + 22, 900), (x - 22, 900)], outline=LINE, width=6)
    for i in range(20):
        for j in range(2): d.rect(700 + i * 50, 240 + j * 50, 750 + i * 50, 290 + j * 50, LINE if (i + j) % 2 else WHITE)
    R_ = np.random.RandomState(2)
    for _ in range(70): d.rect(*(lambda x, y: (x, y, x + 18, y + 10))(R_.randint(0, W2), R_.randint(0, 700)), [PINK, GOLDL, CYAN, LIME, ORNG][R_.randint(5)])
    for x in (200, 2200): d.stroke([(x, 900), (x, 500)], LINE, 10); d.poly([(x, 500), (x + 150, 540), (x, 580)], fill=RED, outline=LINE, width=6)
    im.alpha_composite(d.out()); glow(im, 2100, 170, 160, (255, 250, 220, 140), 50); im.convert('RGB').save(path)


def gala(path):                                              # award stage: emerald backdrop, gold curtains, starburst, confetti
    im = CA.gradient((10, 70, 56), (30, 140, 100), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2)
    for k in range(18): a = math.radians(k * 20); d.poly([(1200, 460), (1200 + 1400 * math.cos(a), 460 + 1400 * math.sin(a)), (1200 + 1400 * math.cos(a + 0.17), 460 + 1400 * math.sin(a + 0.17))], fill=(60, 180, 130, 90))
    for sg in (-1, 1):
        for k in range(6): x = 1200 + sg * (1250 - k * 90); d.rrect(x - 50, -20, x + 50, 900, 40, fill=(230, 170, 50, 255) if k % 2 else (200, 140, 30, 255), outline=LINE, width=6)
    d.chord(1200, 0, 1100, 120, 0, 180, fill=(210, 40, 60, 255), outline=LINE, width=10)
    for k in range(12): d.chord(1200 - 1000 + k * 180, 110, 90, 50, 0, 180, fill=(190, 30, 50, 255), outline=LINE, width=6)
    R_ = np.random.RandomState(8)
    for _ in range(80): d.dot(R_.randint(0, W2), R_.randint(150, 850), R_.randint(5, 12), [GOLDL, WHITE, PINK][R_.randint(3)])
    d.rect(0, 880, W2, H2, (60, 30, 40, 255)); d.stroke([(0, 880), (W2, 880)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1200, 460, 420, (255, 240, 180, 110), 80); im.convert('RGB').save(path)


def street(path):                                            # night street: deep blue city, lit windows, neon shapes, wet road, police glow
    im = CA.gradient((40, 52, 120), (110, 100, 180), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2); R_ = np.random.RandomState(12); x = 0
    while x < W2:
        w, h = R_.randint(160, 300), R_.randint(380, 760); d.rect(x, 900 - h, x + w, 900, (62, 70, 136, 255)); d.poly([(x, 900 - h), (x + w, 900 - h), (x + w, 900), (x, 900)], outline=LINE, width=6)
        for i in range(int(w / 50)):
            for j in range(int(h / 70)):
                if R_.rand() < 0.4: d.rect(x + 14 + i * 50, 930 - h + j * 70, x + 40 + i * 50, 966 - h + j * 70, (255, 214, 120, 255))
        x += w + 10
    g = Draw(W2, H2)
    for x0, y0, c in ((300, 420, PINK), (1500, 360, CYAN), (2000, 500, (255, 170, 60, 255))): g.rrect(x0, y0, x0 + 220, y0 + 90, 40, outline=c, width=12); g.dot(x0 + 110, y0 + 45, 18, c)
    d.rect(0, 900, W2, H2, (70, 70, 110, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    for x in range(60, W2, 260): d.rect(x, 990, x + 140, 1004, (230, 220, 160, 255))
    im.alpha_composite(d.out()); im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(g.out())
    glow(im, 500, 960, 300, (255, 40, 60, 120), 60); glow(im, 1900, 960, 300, (40, 100, 255, 120), 60); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in ('kid', 'toast', 'rep', 'cop'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'shouting')]
    multi = dict(boss={'default': boss(), 'defeated': boss('defeated')}, robot={'default': robot(), 'dizzy': robot('dizzy')}, hglass={'default': hourglass()},
                 jfile={'default': bigfile()}, cheque={'default': cheque()}, wclock={'default': wallclock()}, copcar={'default': copcar()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    cards = dict(gtaon=neon('GTA ONLINE', 'LOADING SCREEN', 900, (255, 170, 60, 255), (170, 130, 255, 255)),
                 yrs7=plaque('7 YEARS', 'BEAT ROCKSTAR', (150, 30, 60, 255), (255, 214, 96, 255), 920, bs=190, ss=74, sc=WHITE),
                 oneplayer=plaque('ONE PLAYER', 'KILLED IT!', VIO, WHITE, 980, border=GOLDL, bs=140, ss=84, sc=GOLDL),
                 min6=stamp('6 MINUTES', 900, (230, 70, 60, 255), 120, -4), everytime=plaque('EVERY TIME', 'YOU JOINED', (40, 110, 170, 255), WHITE, 900, border=GOLDL, bs=130, ss=80, sc=GOLDL),
                 y2021=calendar21(), tname=plaque('t0st', 'PROGRAMMER', (40, 170, 160, 255), WHITE, 860, border=(255, 120, 200, 255), bs=200, ss=78, sc=(255, 236, 160, 255)),
                 waitq=bubble('WHAT THE GAME DOES', 'DURING THAT WAIT?'), startup=stamp('AT STARTUP', 900, (50, 140, 230, 255), 110, 3),
                 onefile=plaque('ONE FILE', '', (190, 120, 40, 255), WHITE, 860, border=GOLDL, bs=150, h=300), mb10=plaque('10 MB', 'TEN MEGABYTES', (90, 50, 30, 255), GOLDL, 880, bs=200, ss=70, sc=WHITE),
                 items63=plaque('63,000', 'ITEMS', (200, 70, 50, 255), WHITE, 900, border=GOLDL, bs=200, ss=90, sc=GOLDL),
                 again=plaque('CHECKS THE WHOLE', 'LIST AGAIN!', (230, 120, 20, 255), WHITE, 1040, border=(255, 240, 160, 255), bs=110, ss=96, sc=(60, 20, 10, 255)), billion=plaque('2 BILLION', 'POINTLESS CHECKS!', (30, 40, 60, 255), (255, 210, 60, 255), 1000, border=(255, 210, 60, 255), bs=170, ss=78, sc=WHITE),
                 fix=stamp('HIS OWN SMALL FIX', 1040, (40, 160, 90, 255), 90, -4), gone=neon('-70%', 'OF THE WAIT: GONE!', 900, LIME, (255, 214, 96, 255)),
                 promise=plaque('PROMISES', 'TO USE HIS FIX', EMER, GOLDL, 960, border=GOLDL, bs=150, ss=84, sc=WHITE), toughest=plaque('TOUGHEST BOSS', 'IN GTA ONLINE', (30, 30, 70, 255), (255, 90, 90, 255), 1000, border=(90, 140, 255, 255), bs=130, ss=78, sc=WHITE),
                 notcops=stamp('NEVER THE COPS!', 960, (40, 80, 200, 255), 104, -5), loadscr=neon('THE LOADING', 'SCREEN!', 900, (255, 120, 60, 255), (255, 214, 96, 255)))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (150, 146, 150), (128, 124, 132)); CE.tiles(T('violet.jpg'), (84, 44, 120), (70, 36, 104)); CE.tiles(T('sand.jpg'), (240, 196, 160), (226, 180, 146))
    CE.tiles(T('navy.jpg'), (60, 56, 100), (50, 46, 88)); CE.tiles(T('grid.jpg'), (16, 30, 60), (24, 60, 90)); CE.tiles(T('steel.jpg'), (110, 124, 130), (94, 108, 116))
    CE.tiles(T('check.jpg'), (245, 245, 245), (40, 40, 48)); CE.tiles(T('emer.jpg'), (120, 40, 50), (100, 30, 42)); CE.tiles(T('asphalt.jpg'), (92, 92, 122), (80, 80, 108))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(arena=arena, lounge=lounge, desert=desert, winter=winter, cyber=cyber, archive=archive, factory=factory, finish=finish, gala=gala, street=street)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
