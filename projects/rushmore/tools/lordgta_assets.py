#!/usr/bin/env python3
"""Assets for video 11 (a British lord tried to stop GTA in 1997 - the outcry was the plan), drawn in code.
New cute cast: the Lord (scarlet robe, ermine collar, white moustache), the minister (round glasses), a mum and a dad
(family group), the publicist (silver slick hair), the co-creator (ginger spikes, square glasses), the founder (quiff),
the publisher exec.  Hero prop: the 1997 GTA big box (default + monster face).  Ten sets, each with its own palette:
LO House of Lords (red + gold), WM Westminster (blue day), SH high street shop (neon dusk), PR publicist office
(navy night), NW news kiosk (warm morning), MO storm stage (purple), DU Dundee waterfront (cool silver), ST 90s studio
(teal + CRT glow), BR publisher boardroom (steel blue), VC Vice City sunset (pink + cyan neon).
Signs are coloured plaques, stamps, newsprint and neon - never plain white cards.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image, ImageFont, ImageFilter
import assets_base as B
import gimli_assets as G
import vasa_assets as VA
import corrigan_assets as CA
import catseyes_assets as CE
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN, BLUE = G.RED, G.GOLD, G.GREEN, VA.BLUE
dk, SK, glow = VA.dk, VA.SK, CE.glow
SCAR, ERM, NAVY, TEAL, PINK, CYAN, ORNG = (196, 34, 52, 255), (250, 248, 240, 255), (36, 46, 96, 255), (30, 150, 150, 255), (255, 80, 170, 255), (60, 230, 240, 255), (250, 150, 60, 255)
SALT, LEAF, PLUM, GOLDL = (0, 94, 184, 255), (60, 150, 80, 255), (90, 40, 110, 255), (255, 214, 96, 255)
NEW = {
    'lord': dict(sk=0, style='bald', hair=(242, 240, 236, 255), suit=SCAR, shade=(160, 24, 40, 255), body='robe', stache=(246, 244, 240, 255)),
    'minister': dict(sk=0, style='part', hair=(130, 128, 136, 255), suit=NAVY, shade=(26, 34, 76, 255), body='suit', tie=RED, glasses=1),
    'mum': dict(sk=1, style='bob', hair=(120, 66, 40, 255), suit=LEAF, shade=(44, 120, 62, 255), body='cardigan', band=RED),
    'dad': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=(232, 170, 50, 255), shade=(200, 140, 36, 255), body='sweater', stubble=1),
    'maxc': dict(sk=0, style='slick', hair=(150, 152, 164, 255), suit=(40, 36, 48, 255), shade=(28, 24, 36, 255), body='suit', tie=PLUM, stache=(170, 170, 178, 255)),
    'mike': dict(sk=0, style='spiky', hair=(226, 110, 40, 255), suit=TEAL, shade=(22, 120, 120, 255), body='tshirt', glasses=2, freck=1),
    'david': dict(sk=1, style='quiff', hair=(70, 44, 30, 255), suit=(90, 130, 200, 255), shade=(70, 106, 170, 255), body='denim', stubble=1),
    'exec': dict(sk=0, style='side', hair=(30, 28, 36, 255), suit=(120, 128, 146, 255), shade=(96, 104, 122, 255), body='suit', tie=GOLD),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; st, hr = c['style'], c['hair']
    skin, sh = SK[c['sk']]
    if st == 'bob':                                          # hair falls behind the face to the chin
        d.chord(cx, cy + 10, R + 34, R + 40, 180, 360, fill=hr, outline=LINE, width=lw); d.rrect(cx - R - 34, cy, cx + R + 34, cy + 130, 40, fill=hr, outline=LINE, width=lw)
    d.ellipse(cx, cy, R, R, fill=skin, outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, sh, skin)
    if st == 'bald':                                         # shiny dome, fluffy white side tufts
        d.ellipse(cx - 70, cy - 150, 46, 22, fill=(255, 255, 255, 110))
        for sg in (-1, 1):
            for dy in (-30, 20): d.ellipse(cx + sg * (R - 6), cy + dy, 48, 44, fill=hr, outline=LINE, width=10)
    elif st == 'spiky':
        d.poly([(cx - R - 10, cy - 40)] + [(cx - R + k * (2 * R + 20) / 7, cy - R - (80 if k % 2 else 0) + 10) for k in range(8)] + [(cx + R + 10, cy - 40), (cx, cy - 110)], fill=hr, outline=LINE, width=lw)
    else:
        d.chord(cx, cy - 66, R + 8, 132, 180, 360, fill=hr, outline=LINE, width=lw)
        if st == 'part': d.stroke(bez((cx - 60, cy - 196), (cx - 70, cy - 150), (cx - 90, cy - 110), (cx - 120, cy - 80)), dk(hr, 0.7), 9)
        if st == 'curly':
            for k in range(9): a = math.radians(190 + k * 20); d.dot(cx + (R + 4) * math.cos(a), cy - 66 + 132 * math.sin(a) * 0.95, 38, hr)
        if st == 'slick':
            for k in range(4): d.stroke(bez((cx - 140 + k * 60, cy - 120), (cx - 100 + k * 60, cy - 170), (cx - 40 + k * 60, cy - 180), (cx + 20 + k * 60, cy - 160)), (255, 255, 255, 140), 7)
        if st == 'quiff': d.poly(bez((cx - 150, cy - 140), (cx - 120, cy - 260), (cx + 60, cy - 260), (cx + 150, cy - 150)) + [(cx, cy - 150)], fill=hr, outline=LINE, width=lw)
        if st == 'side': d.poly([(cx + 40, cy - 196), (cx + R + 10, cy - 60), (cx + R + 10, cy - 120)], fill=hr, outline=LINE, width=8)
        if st == 'bob': d.stroke(bez((cx - R, cy - 70), (cx - 80, cy - 200), (cx + 80, cy - 200), (cx + R, cy - 70)), c['band'], 22)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 30, 17, fill=BLUSH)
    if c.get('freck'):
        for sg in (-1, 1):
            for dx, dy in ((-14, 0), (8, -10), (10, 12)): d.dot(cx + sg * 108 + dx, cy + 12 + dy, 5, (196, 120, 90, 255))
    B.eyes(d, L, Rr, expr, skin); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses') == 1:
        for p in (L, Rr): d.ellipse(p[0], p[1], 54, 54, outline=LINE, width=10)
        d.stroke([(cx - 10, ey - 6), (cx + 10, ey - 6)], LINE, 9)
    elif c.get('glasses') == 2:
        for p in (L, Rr): d.rrect(p[0] - 56, p[1] - 46, p[0] + 56, p[1] + 46, 16, outline=LINE, width=11)
        d.stroke([(cx - 8, ey - 6), (cx + 8, ey - 6)], LINE, 10)
    my = cy + 74
    if c.get('stubble'):
        for k in range(14): d.dot(cx - 90 + (k % 7) * 30, cy + 110 + (k // 7) * 22, 4, dk(skin, 0.75))
    if c.get('stache'):
        big = 32 if st == 'bald' else 16
        for col, ww in ((LINE, big + 14), (c['stache'], big)):
            for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 34, my - 52), (cx + sg * 62, my - 40), (cx + sg * 84, my - 64)), col, ww)
        my += 14
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']; base = c['suit']; bs = c['body']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=base)
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=base); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if bs == 'robe':                                         # ermine collar with black tails, gold chain, white front
        t.rect(206, 452, 254, 800, ERM); t.chord(230, 452, 170, 120, 0, 180, fill=ERM, outline=LINE, width=8)
        for x, y in ((140, 480), (190, 520), (270, 520), (320, 480), (230, 540)): t.poly([(x - 8, y - 14), (x + 8, y - 14), (x, y + 18)], fill=LINE)
        t.stroke(bez((120, 520), (170, 640), (290, 640), (340, 520)), GOLD, 14); t.dot(230, 640, 26, GOLD); t.ellipse(230, 640, 26, 26, outline=LINE, width=6)
    elif bs == 'suit':                                       # shirt V, tie, lapels, pocket square
        t.poly([(180, 452), (280, 452), (230, 600)], fill=WHITE); t.poly([(222, 470), (238, 470), (248, 600), (230, 625), (212, 600)], fill=c['tie'], outline=LINE, width=6)
        for sg in (-1, 1): t.stroke([(230 + sg * 52, 456), (230 + sg * 30, 610)], dk(base, 0.7), 8)
        t.poly([(300, 560), (340, 560), (330, 590), (310, 590)], fill=c['tie'], outline=LINE, width=5)
    elif bs == 'cardigan':
        t.poly([(186, 452), (274, 452), (230, 560)], fill=(250, 236, 220, 255)); t.stroke([(230, 560), (230, 800)], dk(base, 0.7), 8)
        for y in (600, 670, 740): t.dot(214, y, 10, GOLD)
        for sg in (-1, 1): t.rrect(230 + sg * 90 - 40, 680, 230 + sg * 90 + 40, 740, 10, outline=dk(base, 0.7), width=6)
    elif bs == 'sweater':                                    # diamond pattern band
        for k in range(5): x = 120 + k * 56; t.poly([(x, 600), (x + 28, 570), (x + 56, 600), (x + 28, 630)], fill=(170, 60, 50, 255), outline=LINE, width=5)
        t.chord(230, 452, 80, 40, 0, 180, fill=dk(base, 0.8))
    elif bs == 'tshirt':                                     # pixel car on the shirt
        t.chord(230, 452, 70, 36, 0, 180, fill=dk(base, 0.8))
        for (px, py) in [(i, 0) for i in range(-3, 4)] + [(i, -1) for i in range(-1, 2)] + [(-2, 1), (2, 1)]:
            t.rect(230 + px * 16 - 8, 600 + py * 16 - 8, 230 + px * 16 + 8, 600 + py * 16 + 8, (255, 214, 64, 255) if py >= 0 else (255, 120, 90, 255))
    elif bs == 'denim':
        t.poly([(186, 452), (274, 452), (230, 540)], fill=(250, 246, 236, 255)); t.stroke([(230, 540), (230, 800)], dk(base, 0.7), 6)
        for sg in (-1, 1): t.rrect(230 + sg * 80 - 36, 540, 230 + sg * 80 + 36, 600, 8, outline=dk(base, 0.65), width=6)
        for y in (580, 650, 720): t.dot(230, y, 7, (240, 240, 240, 255))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


# ------------------------------------------------------------------ text fit + signs
def fit(txt, size, maxw):
    while size > 20 and ImageFont.truetype(B.FONT, size).getlength(txt) > maxw: size -= 2
    return size


def plaque(big, small, bg, fg, w, border=GOLDL, bs=150, ss=62, h=420, sc=None):
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 34, fill=bg, outline=LINE, width=16); d.rrect(36, 36, w - 36, h - 36, 22, outline=border, width=7)
    if small:
        d.text(w / 2, h * 0.40, big, fit(big, bs, w - 110), fg, stroke=8, stroke_fill=LINE); d.text(w / 2, h * 0.77, small, fit(small, ss, w - 110), sc or border, stroke=5, stroke_fill=LINE)
    else: d.text(w / 2, h / 2, big, fit(big, bs, w - 110), fg, stroke=8, stroke_fill=LINE)
    return d.out()


def stamp(txt, w, col=RED, size=96, tilt=-5):
    d = Draw(w, 250); d.rrect(14, 14, w - 14, 236, 26, fill=col, outline=LINE, width=16)
    for x in range(50, w - 50, 46): d.rect(x, 40, x + 24, 48, (255, 255, 255, 200)); d.rect(x, 202, x + 24, 210, (255, 255, 255, 200))
    d.text(w / 2, 126, txt, fit(txt, size, w - 90), WHITE, stroke=6, stroke_fill=LINE); return d.out().rotate(tilt, resample=Image.BICUBIC, expand=True)


def paper(headl, sub, w=900):                                # tabloid front page
    d = Draw(w, 600); d.rect(20, 20, w - 20, 580, (238, 230, 208, 255)); d.poly([(20, 20), (w - 20, 20), (w - 20, 580), (20, 580)], outline=LINE, width=14)
    d.rect(44, 44, w - 44, 120, RED); d.text(w / 2, 82, 'THE DAILY', 54, WHITE, stroke=4, stroke_fill=LINE)
    d.text(w / 2, 245, headl, fit(headl, 190, w - 100), LINE); d.text(w / 2, 375, sub, fit(sub, 64, w - 120), RED, stroke=3, stroke_fill=LINE)
    for k in range(3):
        x = 60 + k * (w - 100) / 3
        for j in range(4): d.rect(x, 440 + j * 30, x + (w - 100) / 3 - 30, 452 + j * 30, (150, 146, 136, 255))
    return d.out()


def neon(big, small, w, col=PINK, col2=CYAN, h=420):
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 40, fill=(34, 14, 58, 255), outline=LINE, width=16); d.rrect(34, 34, w - 34, h - 34, 28, outline=col2, width=8)
    im = d.out(); g = Draw(w, h); bsz = fit(big, 160, w - 120); g.text(w / 2, h * (0.40 if small else 0.5), big, bsz, col)
    if small: g.text(w / 2, h * 0.77, small, fit(small, 62, w - 120), col2)
    im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(14))); t = Draw(w, h)
    t.text(w / 2, h * (0.40 if small else 0.5), big, bsz, (255, 236, 250, 255), stroke=7, stroke_fill=col)
    if small: t.text(w / 2, h * 0.77, small, fit(small, 62, w - 120), (230, 255, 255, 255), stroke=4, stroke_fill=dk(col2, 0.6))
    im.alpha_composite(t.out()); return im


def bubble(txt1, txt2, w=1100):                              # quote bubble
    d = Draw(w, 560); d.rrect(20, 20, w - 20, 430, 120, fill=(255, 226, 90, 255), outline=LINE, width=16)
    d.poly([(w * 0.22, 420), (w * 0.16, 540), (w * 0.36, 420)], fill=(255, 226, 90, 255), outline=LINE, width=16); d.rect(w * 0.22, 400, w * 0.36, 426, (255, 226, 90, 255))
    for t, y in ((txt1, 150), (txt2, 300)): d.text(w / 2, y, t, fit(t, 120, w - 160), LINE)
    d.text(80, 90, '“', 140, RED); return d.out()


def calpage():                                               # MAY 1997 / 20
    d = Draw(720, 800); d.rrect(20, 60, 700, 780, 40, fill=(255, 244, 214, 255), outline=LINE, width=18); d.rrect(20, 60, 700, 260, 40, fill=SALT, outline=LINE, width=18)
    d.rect(38, 210, 682, 260, SALT); d.stroke([(20, 260), (700, 260)], LINE, 14); d.text(360, 165, 'MAY 1997', 110, WHITE, stroke=6, stroke_fill=LINE)
    for x in (200, 520): d.rrect(x - 22, 20, x + 22, 120, 18, fill=(150, 150, 160, 255), outline=LINE, width=10)
    d.text(360, 530, '20', 360, RED, stroke=10, stroke_fill=LINE); return d.out()


def placard(txt, col=RED):                                   # protest placard on a stick
    d = Draw(900, 760); d.rect(420, 380, 480, 760, (160, 110, 64, 255)); d.poly([(420, 380), (480, 380), (480, 760), (420, 760)], outline=LINE, width=10)
    d.rrect(20, 20, 880, 420, 20, fill=(255, 236, 120, 255), outline=LINE, width=16); d.text(450, 220, txt, fit(txt, 170, 760), col, stroke=8, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ hero prop: the 1997 big box
def gbox(monster=False):
    W_, H_ = 1100, 1300; d = Draw(W_, H_); d.rrect(60, 40, 1040, 1260, 30, fill=(24, 24, 34, 255), outline=LINE, width=18)
    d.rect(80, 60, 1020, 300, (250, 200, 40, 255)); d.text(550, 130, 'GRAND THEFT', 120, LINE); d.text(550, 240, 'AUTO', 130, RED, stroke=7, stroke_fill=LINE)
    d.rect(110, 340, 990, 1150, (90, 110, 130, 255))           # top-down city: blocks, roads, a red car and a police car
    for i in range(4):
        for j in range(4): d.rrect(130 + i * 220, 360 + j * 200, 300 + i * 220, 520 + j * 200, 14, fill=((120, 170, 110, 255) if (i + j) % 3 == 0 else (200, 170, 140, 255)), outline=LINE, width=6)
    def car(x, y, col, cop=False):
        d.rrect(x - 50, y - 90, x + 50, y + 90, 26, fill=col, outline=LINE, width=8); d.rrect(x - 34, y - 40, x + 34, y + 30, 12, fill=(150, 210, 240, 255), outline=LINE, width=6)
        if cop: d.rect(x - 34, y - 12, x, y + 4, RED); d.rect(x, y - 12, x + 34, y + 4, BLUE)
    car(540, 640, RED); car(760, 1010, WHITE, True)
    if not monster:
        d.text(900, 1210, '1997', 64, GOLDL, stroke=4, stroke_fill=LINE); g = Draw(W_, H_); g.poly([(110, 340), (330, 340), (110, 700)], fill=(255, 255, 255, 60)); return Image.alpha_composite(d.out(), g.out())
    m = Draw(W_, H_)                                          # monster: angry eyes and a toothy grin over the art
    for x in (380, 720):
        m.ellipse(x, 600, 130, 140, fill=WHITE, outline=LINE, width=16); m.dot(x + 20, 630, 62, LINE); m.dot(x + 44, 596, 20, WHITE)
        m.stroke([(x - 140, 440 + (0 if x < 550 else 60)), (x + 140, 440 + (60 if x < 550 else 0))], LINE, 34)
    m.chord(550, 880, 300, 210, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=16)
    for k in range(7): x = 290 + k * 87; m.poly([(x, 880), (x + 40, 960), (x + 80, 880)], fill=WHITE, outline=LINE, width=6)
    return Image.alpha_composite(d.out(), m.out())


# ------------------------------------------------------------------ set pictures (no text on them)
W2, H2 = 2400, 1100


def arch(d, x0, x1, y0, y1, fill, outline=LINE, width=8):
    m = (x0 + x1) / 2; d.poly([(x0, y1), (x0, y0 + (x1 - x0) * 0.5)] + bez((x0, y0 + (x1 - x0) * 0.5), (x0, y0 + 20), (m - 10, y0), (m, y0)) + bez((m, y0), (m + 10, y0), (x1, y0 + 20), (x1, y0 + (x1 - x0) * 0.5)) + [(x1, y1)], fill=fill, outline=outline, width=width)


def lords(path):                                             # oak panels, gold canopy, glowing stained glass, scarlet benches
    im = Image.new('RGBA', (W2, H2), (96, 54, 34, 255)); d = Draw(W2, H2)
    for x in range(0, W2, 100): d.stroke([(x, 0), (x, H2)], (78, 42, 26, 255), 8)
    for x in (110, 420, 1820, 2130):
        arch(d, x, x + 170, 70, 560, (40, 30, 60, 255), width=12)
        for i in range(3):
            for j in range(5): d.rect(x + 14 + i * 50, 200 + j * 70, x + 54 + i * 50, 256 + j * 70, [(220, 60, 60, 255), (60, 120, 220, 255), (240, 200, 60, 255), (80, 170, 90, 255)][(i + j + x // 100) % 4])
    im.alpha_composite(d.out())
    for x in (195, 505, 1905, 2215): glow(im, x, 330, 160, (255, 220, 150, 110), 60)
    d = Draw(W2, H2); arch(d, 900, 1500, 60, 820, (214, 170, 70, 255), width=14); arch(d, 990, 1410, 180, 820, (176, 130, 44, 255), width=10)
    for x in range(940, 1480, 60): d.stroke([(x, 300), (x, 820)], (240, 206, 110, 255), 6)
    d.rrect(1080, 470, 1320, 820, 30, fill=SCAR, outline=LINE, width=12); d.rrect(1110, 380, 1290, 520, 40, fill=SCAR, outline=LINE, width=12); d.dot(1200, 440, 34, GOLD)
    for side in (0, 1):
        for k in range(3):
            y = 760 + k * 110; xa, xb = (0, 820 - k * 60) if side == 0 else (1580 + k * 60, W2)
            d.rect(xa, y, xb, y + 110, (186, 36, 50, 255)); d.rect(xa, y, xb, y + 30, (150, 26, 40, 255)); d.poly([(xa, y), (xb, y), (xb, y + 110), (xa, y + 110)], outline=LINE, width=8)
    for x in (300, 700, 1700, 2100): d.stroke([(x, 0), (x, 90)], LINE, 6); d.dot(x, 110, 28, GOLDL); d.ellipse(x, 110, 28, 28, outline=LINE, width=6)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def westminster(path):                                       # sunny Thames front: gothic facade, clock tower, river
    im = CA.gradient((76, 140, 230), (250, 226, 196), W2, H2, 1.1).convert('RGBA'); glow(im, 300, 160, 140, (255, 250, 220, 200), 50); d = Draw(W2, H2)
    for cx_, cy_ in ((700, 170), (1400, 120), (2200, 220)):
        for dx, r in ((-70, 50), (0, 70), (70, 50)): d.dot(cx_ + dx, cy_, r, (255, 255, 255, 220))
    d.rect(0, 430, 1760, 900, (226, 192, 128, 255)); d.poly([(0, 430), (1760, 430), (1760, 900), (0, 900)], outline=LINE, width=10)
    for x in range(30, 1760, 70): d.stroke([(x, 430), (x, 900)], (196, 160, 100, 255), 6)
    for x in range(60, 1700, 140):
        for y in (500, 650, 790): arch(d, x, x + 50, y, y + 80, (60, 70, 100, 255), width=5)
        d.poly([(x - 10, 430), (x + 25, 360), (x + 60, 430)], fill=(206, 170, 110, 255), outline=LINE, width=6)
    tx = 1980; d.rect(tx - 110, 170, tx + 110, 900, (222, 188, 120, 255)); d.poly([(tx - 110, 170), (tx + 110, 170), (tx + 110, 900), (tx - 110, 900)], outline=LINE, width=10)
    for y in range(420, 880, 90): arch(d, tx - 50, tx + 50, y, y + 60, (60, 70, 100, 255), width=5)
    d.poly([(tx - 130, 170), (tx, 10), (tx + 130, 170)], fill=(70, 100, 96, 255), outline=LINE, width=10); d.dot(tx, 290, 86, (250, 246, 230, 255)); d.ellipse(tx, 290, 86, 86, outline=LINE, width=10)
    d.stroke([(tx, 290), (tx, 225)], LINE, 10); d.stroke([(tx, 290), (tx + 45, 290)], LINE, 12)
    d.rect(0, 900, W2, H2, (70, 126, 176, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    for k in range(18): x = (k * 173) % W2; d.stroke([(x, 950 + (k % 4) * 35), (x + 90, 950 + (k % 4) * 35)], (160, 200, 236, 255), 7)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def shop(path):                                              # neon dusk high street: empty game shop window, phone box, wet street
    im = CA.gradient((54, 40, 110), (236, 120, 130), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2)
    d.rect(300, 120, 2100, 940, (120, 60, 70, 255))
    for y in range(140, 940, 44): d.stroke([(300, y), (2100, y)], (100, 48, 58, 255), 5)
    d.rect(300, 120, 2100, 250, (24, 120, 120, 255))
    for x in range(300, 2100, 120): d.poly([(x, 250), (x + 120, 250), (x + 60, 300)], fill=(24, 120, 120, 255) if (x // 120) % 2 else (240, 230, 220, 255), outline=LINE, width=5)
    d.rrect(480, 330, 1720, 860, 18, fill=(20, 50, 64, 255), outline=LINE, width=14)
    for y in (480, 640, 800): d.rect(520, y, 1680, y + 18, (150, 110, 70, 255))
    for x, y, c in ((560, 480, ORNG), (640, 480, BLUE), (1500, 640, GREEN)): d.rrect(x, y - 120, x + 70, y, 6, fill=c, outline=LINE, width=5)
    d.rrect(1780, 380, 2000, 940, 12, fill=(60, 30, 40, 255), outline=LINE, width=10)
    d.rrect(2160, 500, 2290, 940, 14, fill=(206, 40, 46, 255), outline=LINE, width=10)
    d.rect(0, 940, W2, H2, (50, 40, 70, 255)); d.stroke([(0, 940), (W2, 940)], LINE, 8)
    im.alpha_composite(d.out()); g = Draw(W2, H2); g.rrect(480, 330, 1720, 860, 18, outline=PINK, width=16); g.rrect(1780, 380, 2000, 940, 12, outline=CYAN, width=10)
    im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(10))); im.alpha_composite(g.out())
    r = Draw(W2, H2)
    for x, c in ((1100, (255, 80, 170, 90)), (1890, (60, 230, 240, 90)), (2225, (255, 70, 70, 80))): r.rect(x - 60, 960, x + 60, H2, c)
    im.alpha_composite(r.out().filter(ImageFilter.GaussianBlur(18))); im.convert('RGB').save(path)


def office(path):                                            # publicist's night office: city window, lamp glow, plan board with red strings
    im = Image.new('RGBA', (W2, H2), (30, 34, 74, 255)); d = Draw(W2, H2)
    d.rrect(100, 140, 900, 760, 12, fill=(16, 20, 50, 255), outline=LINE, width=14); R_ = np.random.RandomState(4); x = 110
    while x < 890:
        w, h = R_.randint(60, 120), R_.randint(150, 450); d.rect(x, 760 - h, x + w, 760, (40, 48, 90, 255))
        for i in range(int(w / 30)):
            for j in range(int(h / 40)):
                if R_.rand() < 0.35: d.rect(x + 8 + i * 30, 770 - h + j * 40, x + 22 + i * 30, 786 - h + j * 40, (255, 220, 120, 255))
        x += w + 6
    d.stroke([(500, 140), (500, 760)], LINE, 12); d.dot(760, 240, 40, (255, 246, 210, 255))
    d.rrect(1240, 170, 2240, 760, 16, fill=(196, 146, 92, 255), outline=(110, 70, 40, 255), width=26); d.rrect(1240, 170, 2240, 760, 16, outline=LINE, width=8)
    PIN = [(1400, 300), (1740, 260), (2080, 320), (1500, 600), (1960, 610)]
    for a, b in ((0, 1), (1, 2), (0, 3), (2, 4), (3, 4), (1, 4)): d.stroke([PIN[a], PIN[b]], (220, 40, 50, 255), 7)
    for k, (x, y) in enumerate(PIN):
        d.rect(x - 80, y - 60, x + 80, y + 70, [(250, 246, 230, 255), (255, 226, 110, 255), (180, 220, 250, 255)][k % 3]); d.poly([(x - 80, y - 60), (x + 80, y - 60), (x + 80, y + 70), (x - 80, y + 70)], outline=LINE, width=6)
        d.dot(x, y - 10, 30, (150, 120, 110, 255)); d.dot(x, y - 60, 14, RED)
    d.rect(0, 940, W2, H2, (60, 40, 50, 255)); d.stroke([(0, 940), (W2, 940)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 1080, 560, 260, (255, 200, 120, 110), 70); im.convert('RGB').save(path)


def kiosk(path):                                             # warm morning: green news kiosk, racks of front pages, brick terrace
    im = CA.gradient((170, 190, 226), (255, 214, 170), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2)
    for x0, w, c in ((0, 600, (170, 90, 70, 255)), (1800, 600, (150, 100, 80, 255))):
        d.rect(x0, 150, x0 + w, 940, c)
        for i in range(4):
            for j in range(4): d.rrect(x0 + 50 + i * 140, 210 + j * 180, x0 + 140 + i * 140, 330 + j * 180, 8, fill=(220, 236, 246, 255), outline=LINE, width=6)
    d.rect(620, 240, 1780, 940, (40, 110, 80, 255)); d.poly([(560, 240), (1840, 240), (1780, 320), (620, 320)], fill=(30, 90, 64, 255), outline=LINE, width=10)
    for i in range(6):
        for j in range(3):
            x, y = 680 + i * 180, 380 + j * 180; d.rect(x, y, x + 150, y + 150, (238, 230, 208, 255)); d.rect(x + 10, y + 12, x + 140, y + 40, [RED, LINE, BLUE][(i + j) % 3])
            d.rect(x + 14, y + 56, x + 136, y + 76, LINE); d.rect(x + 14, y + 90, x + 100, y + 100, (140, 140, 140, 255)); d.poly([(x, y), (x + 150, y), (x + 150, y + 150), (x, y + 150)], outline=LINE, width=5)
    d.rect(0, 940, W2, H2, (150, 140, 130, 255)); d.stroke([(0, 940), (W2, 940)], LINE, 8)
    im.alpha_composite(d.out()); glow(im, 2100, 120, 160, (255, 240, 200, 160), 60); im.convert('RGB').save(path)


def storm(path):                                             # purple storm: lightning, spotlight cones
    im = CA.gradient((24, 8, 44), (130, 44, 120), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2)
    for cx_, cy_ in ((400, 200), (1200, 140), (2000, 220)):
        for dx, r in ((-120, 90), (0, 130), (120, 90)): d.dot(cx_ + dx, cy_, r, (60, 30, 80, 255))
    for x0 in (520, 1880): d.poly([(x0, 260), (x0 + 60, 260), (x0 - 10, 470), (x0 + 50, 470), (x0 - 70, 760), (x0 - 10, 520), (x0 - 70, 520)], fill=(255, 236, 120, 255), outline=LINE, width=8)
    d.rect(0, 960, W2, H2, (40, 20, 50, 255)); im.alpha_composite(d.out())
    g = Draw(W2, H2)
    for x in (900, 1500): g.poly([(x, 0), (x + 80, 0), (1200 + (x - 1200) * 0.2 + 260, 1000), (1200 + (x - 1200) * 0.2 - 260, 1000)], fill=(255, 240, 200, 60))
    im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(30))); im.convert('RGB').save(path)


def dundee(path):                                            # silver-blue Tay: hills, long rail bridge, stone tenements, little studio
    im = CA.gradient((110, 150, 206), (232, 232, 238), W2, H2, 1.0).convert('RGBA'); glow(im, 1700, 200, 200, (255, 246, 210, 170), 70); d = Draw(W2, H2)
    d.poly([(0, 640)] + bez((0, 640), (500, 380), (900, 420), (1300, 600)) + [(1300, 700), (0, 700)], fill=(110, 140, 120, 255), outline=LINE, width=8)
    d.poly([(1000, 700)] + bez((1000, 650), (1600, 460), (2000, 520), (2400, 600)) + [(2400, 700)], fill=(90, 124, 110, 255), outline=LINE, width=8)
    d.rect(0, 700, W2, 960, (84, 124, 168, 255)); d.stroke([(0, 700), (W2, 700)], LINE, 8)
    for k in range(20): x = (k * 211) % W2; d.stroke([(x, 760 + (k % 4) * 45), (x + 110, 760 + (k % 4) * 45)], (190, 214, 236, 255), 6)
    d.rect(0, 600, W2, 630, (120, 70, 60, 255)); d.poly([(0, 600), (W2, 600), (W2, 630), (0, 630)], outline=LINE, width=6)
    for x in range(40, W2, 120): d.rect(x, 630, x + 26, 720, (120, 70, 60, 255)); d.poly([(x, 630), (x + 26, 630), (x + 26, 720), (x, 720)], outline=LINE, width=5)
    for x0, h in ((40, 340), (300, 300), (540, 360)):
        d.rect(x0, 940 - h, x0 + 240, 960, (196, 180, 156, 255)); d.poly([(x0, 940 - h), (x0 + 240, 940 - h), (x0 + 240, 960), (x0, 960)], outline=LINE, width=8)
        for i in range(3):
            for j in range(int(h / 90)): d.rrect(x0 + 24 + i * 72, 970 - h + j * 90, x0 + 70 + i * 72, 1030 - h + j * 90, 6, fill=(250, 226, 150, 255), outline=LINE, width=5)
    d.rect(1700, 740, 2200, 960, (70, 90, 140, 255)); d.poly([(1680, 740), (1950, 640), (2220, 740)], fill=(60, 60, 80, 255), outline=LINE, width=8); d.poly([(1700, 740), (2200, 740), (2200, 960), (1700, 960)], outline=LINE, width=8)
    for i in range(4): d.rrect(1730 + i * 118, 790, 1810 + i * 118, 860, 6, fill=(255, 220, 110, 255), outline=LINE, width=5)
    for x, y in ((900, 250), (980, 210), (1100, 280)): d.stroke(bez((x - 30, y), (x - 15, y - 18), (x - 5, y - 10), (x, y)) + bez((x, y), (x + 5, y - 10), (x + 15, y - 18), (x + 30, y)), LINE, 6)
    d.rect(0, 960, W2, H2, (120, 120, 126, 255)); d.stroke([(0, 960), (W2, 960)], LINE, 8)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def studio(path):                                            # 90s dev room: CRT glow, posters, grey Dundee window
    im = Image.new('RGBA', (W2, H2), (36, 74, 76, 255)); d = Draw(W2, H2)
    d.rrect(1700, 150, 2250, 560, 12, fill=(170, 186, 200, 255), outline=(220, 210, 190, 255), width=22); d.stroke([(1975, 150), (1975, 560)], (220, 210, 190, 255), 14)
    for x, c in ((180, ORNG), (520, PINK), (860, (255, 214, 64, 255)), (1200, (120, 200, 255, 255))):
        d.rect(x, 170, x + 260, 520, c); d.poly([(x, 170), (x + 260, 170), (x + 260, 520), (x, 520)], outline=LINE, width=8); d.dot(x + 130, 300, 70, dk(c, 0.75)); d.rect(x + 40, 420, x + 220, 460, dk(c, 0.7))
    d.rect(0, 720, W2, 760, (150, 104, 70, 255)); d.stroke([(0, 760), (W2, 760)], LINE, 8)
    for x in (300, 900, 1500, 2100):
        d.rrect(x - 170, 470, x + 170, 720, 26, fill=(214, 206, 180, 255), outline=LINE, width=10); d.rrect(x - 130, 500, x + 130, 680, 30, fill=(20, 60, 50, 255), outline=LINE, width=8)
    im.alpha_composite(d.out())
    for x in (300, 900, 1500, 2100): glow(im, x, 590, 160, (90, 255, 170, 90), 40)
    d = Draw(W2, H2)
    for x in (300, 900, 1500, 2100):
        for j in range(4): d.rect(x - 100, 520 + j * 36, x - 100 + (60 + (j * 53 + x) % 150), 536 + j * 36, (120, 255, 180, 255))
    d.rect(0, 760, W2, H2, (60, 50, 50, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def boardroom(path):                                         # steel-blue glass wall over a city skyline
    im = CA.gradient((120, 170, 226), (226, 236, 248), W2, H2, 1.0).convert('RGBA'); d = Draw(W2, H2); R_ = np.random.RandomState(6); x = 0
    while x < W2:
        w, h = R_.randint(120, 240), R_.randint(260, 640); c = (int(R_.randint(90, 130)), int(R_.randint(110, 150)), int(R_.randint(150, 190)), 255)
        d.rect(x, 900 - h, x + w, 900, c); d.poly([(x, 900 - h), (x + w, 900 - h), (x + w, 900), (x, 900)], outline=LINE, width=6)
        for j in range(int(h / 60)): d.rect(x + 16, 920 - h + j * 60, x + w - 16, 932 - h + j * 60, (210, 230, 250, 255))
        x += w + R_.randint(10, 60)
    for x in range(0, W2 + 1, 400): d.rect(x - 14, 0, x + 14, 900, (50, 60, 80, 255))
    d.rect(0, 0, W2, 60, (50, 60, 80, 255)); d.rect(0, 900, W2, H2, (70, 80, 100, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    im.alpha_composite(d.out()); g = Draw(W2, H2)
    for x in range(100, W2, 400): g.poly([(x, 60), (x + 120, 60), (x - 80, 900), (x - 200, 900)], fill=(255, 255, 255, 50))
    im.alpha_composite(g.out()); im.convert('RGB').save(path)


def palms(d, x0, y0, s, col=(40, 20, 60, 255)):
    tx, ty = x0 + 60 * s, y0 - 520 * s
    d.stroke(bez((x0, y0), (x0, y0 - 250 * s), (tx, ty + 150 * s), (tx, ty)), col, int(34 * s))
    for a in (-170, -130, -90, -50, -10, 30):
        ex, ey = tx + math.cos(math.radians(a)) * 260 * s, ty + math.sin(math.radians(a)) * 200 * s + 90 * s
        d.stroke(bez((tx, ty), ((tx + ex) / 2, ty - 70 * s), (ex, ey - 30 * s), (ex, ey)), col, int(26 * s))


def vicecity(path):                                          # sunset ocean drive: striped sun, deco hotels with neon, palms
    im = CA.gradient((90, 30, 130), (255, 150, 100), W2, H2, 1.1).convert('RGBA'); d = Draw(W2, H2)
    d.dot(1200, 560, 300, (255, 210, 110, 255))
    for k in range(5): y = 600 + k * 50; d.rect(900, y, 1500, y + 14 + k * 5, (250, 120, 140, 255))
    d.rect(0, 760, W2, 900, (60, 70, 160, 255))
    for k in range(14): x = (k * 197) % W2; d.stroke([(x, 790 + (k % 3) * 35), (x + 100, 790 + (k % 3) * 35)], (160, 170, 250, 255), 7)
    d.rect(0, 900, W2, H2, (250, 210, 160, 255)); d.stroke([(0, 900), (W2, 900)], LINE, 8)
    H_ = [(60, 380, (255, 170, 200, 255)), (500, 300, (150, 240, 220, 255)), (1700, 340, (200, 170, 255, 255)), (2080, 280, (255, 220, 150, 255))]
    for x0, w, c in H_:
        d.rrect(x0, 360, x0 + w, 910, 30, fill=c, outline=LINE, width=10); d.rrect(x0 + w * 0.3, 260, x0 + w * 0.7, 380, 20, fill=c, outline=LINE, width=8)
        for j in range(5): d.rect(x0 + 30, 420 + j * 95, x0 + w - 30, 450 + j * 95, (90, 160, 220, 255))
    im.alpha_composite(d.out()); g = Draw(W2, H2)
    for x0, w, c in H_: g.rrect(x0 + 12, 372, x0 + w - 12, 898, 24, outline=PINK if c[1] < 200 else CYAN, width=12)
    im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(9))); im.alpha_composite(g.out())
    d = Draw(W2, H2)
    for x, s in ((420, 1.0), (1540, 0.9), (2000, 1.1)): palms(d, x, 930, s)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def palm(path):                                              # foreground palm sticker (depth layer)
    d = Draw(900, 1200); palms(d, 420, 1180, 2.0, (50, 26, 66, 255)); d.out().save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'shouting')]
    multi = dict(gbox={'default': gbox(), 'monster': gbox(True)})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    LEA = (120, 22, 36, 255)
    cards = dict(stopgta=plaque('STOP', 'GRAND THEFT AUTO!', LEA, (255, 90, 90, 255), 980, bs=190, ss=72), plan=stamp('THAT WAS THE PLAN', 1060, PLUM, 84),
                 date=calpage(), notyet=stamp('NOT IN SHOPS YET', 1000, (230, 70, 120, 255), 88, 4), hol=plaque('HOUSE OF LORDS', '', LEA, GOLDL, 1100, bs=110, h=260),
                 campbell=plaque('LORD CAMPBELL', 'OF CROY', (24, 70, 60, 255), GOLDL, 1000, bs=120, ss=80), govt=plaque('THE GOVERNMENT', 'WHAT WILL IT DO?', NAVY, WHITE, 1080, border=(140, 180, 255, 255), bs=110, ss=66),
                 howl=paper('OUTRAGE!', 'NEWSPAPERS HOWL', 900), rage=placard('BAN IT!'), monster=stamp('THIS MONSTER?', 900, (110, 30, 140, 255), 92),
                 dundee=plaque('DUNDEE', 'SCOTLAND', SALT, WHITE, 900, border=WHITE, bs=170, ss=78), lemm=plaque('LEMMINGS', 'SAME PEOPLE MADE', LEAF, (255, 250, 200, 255), 980, border=(255, 250, 200, 255), bs=150, ss=66),
                 cancel=stamp('NEARLY CANCELLED!', 1040, RED, 90, -6), bmg=plaque('BMG', 'THE PUBLISHER', (60, 70, 96, 255), GOLDL, 760, bs=230, ss=70),
                 maxname=plaque('MAX CLIFFORD', 'HIRED!', PLUM, GOLDL, 1000, bs=120, ss=86), publicist=plaque('FAMOUS', 'BRITISH PUBLICIST', (230, 140, 30, 255), WHITE, 940, border=WHITE, bs=170, ss=66),
                 mikecard=plaque('MIKE DAILLY', 'CO-CREATOR', TEAL, WHITE, 960, border=(255, 230, 120, 255), bs=120, ss=76, sc=(255, 230, 120, 255)),
                 quote=bubble('DESIGNED ALL', 'THE OUTCRY'), target=plaque('WHO HE WOULD TARGET', 'WHAT THEY WOULD SAY', (196, 146, 92, 255), WHITE, 1200, border=RED, bs=86, ss=70, sc=(255, 236, 120, 255)),
                 davidcard=plaque('DAVID JONES', 'FOUNDER', (40, 90, 170, 255), WHITE, 940, border=GOLDL, bs=120, ss=80, sc=GOLDL), cametrue=stamp('EVERY WORD CAME TRUE', 1120, (30, 140, 80, 255), 80, -4),
                 advert=plaque('THE SCANDAL', 'WAS THE ADVERT!', (230, 50, 110, 255), (255, 240, 120, 255), 1040, border=(255, 240, 120, 255), bs=140, ss=80, sc=WHITE),
                 yrs29=neon('29 YEARS', 'LATER', 860), gta6=neon('GTA 6', 'VICE CITY', 820, PINK, CYAN), miami=neon('MIAMI', "ROCKSTAR'S VERSION", 920, CYAN, PINK))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    palm(Pp('palm.png')); G.build_card('palm', {'default': Image.open(Pp('palm.png'))})
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()] + [('palm', Image.open(Pp('palm.png')))]},
              open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (150, 146, 150), (128, 124, 132)); CE.tiles(T('red.jpg'), (150, 30, 44), (132, 24, 38)); CE.tiles(T('sand.jpg'), (240, 206, 160), (226, 190, 146))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg'))
    SETS = dict(lords=lords, westminster=westminster, shop=shop, office=office, kiosk=kiosk, storm=storm, dundee=dundee, studio=studio, boardroom=boardroom, vicecity=vicecity)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
