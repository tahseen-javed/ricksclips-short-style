#!/usr/bin/env python3
"""Assets for video 07 (who named Black Friday), drawn in code with the channel builders.
New cast (all cute, big heads): a furious Philadelphia traffic cop, a desk sergeant, a straw-hat shopkeeper, 1961 shoppers
(a lady with a pillbox hat, a dad in a fedora, a little girl, a granny), two Army-Navy football fans, a 1980s retail exec
with big hair and shoulder pads, and a store clerk + a teen shopper of today.  Cute props: 1960s cars with faces (calm /
honking), a football with a face, steam puffs, a light bulb, a cricket, map pins, a duty board (roster / BLACK FRIDAY),
a BIG FRIDAY banner, a ledger (red / black), shopping bags, a newspaper.  Sets: Philadelphia shopfronts and skyline, stadium
stands, a police station wall, a 1961 department store, a US map, a 1980s Memphis-style office, a mall of today.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import assets_base as B
import gimli_assets as G
import viking_assets as V
import vasa_assets as VA
import corrigan_assets as CA
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN, BLUE = G.RED, G.GOLD, G.GREEN, VA.BLUE
dk, SK = VA.dk, VA.SK
NAVY, PINK, TEAL, STRAW, CREAM, GLASS = (40, 58, 120, 255), (236, 72, 150, 255), (40, 190, 186, 255), (236, 204, 132, 255), (250, 238, 206, 255), (170, 222, 244, 255)
BLK, MOUTHC = (34, 32, 40, 255), (124, 40, 62, 255)
NEW = {
    'cop': dict(skin=SK[1][0], sh=SK[1][1], style='cap', hair=(70, 48, 36, 255), suit=NAVY, shade=(28, 40, 88, 255), tie=(26, 30, 50, 255), uniform=1, stache=(70, 48, 36, 255)),
    'sarge': dict(skin=SK[2][0], sh=SK[2][1], style='cap', hair=(200, 200, 206, 255), suit=(52, 66, 112, 255), shade=(36, 48, 86, 255), tie=(26, 30, 50, 255), uniform=1,
                  glasses=1, stache=(220, 220, 226, 255)),
    'shopk': dict(skin=SK[0][0], sh=SK[0][1], style='boater', hair=(150, 92, 52, 255), suit=(206, 84, 70, 255), shade=(170, 62, 54, 255), bow=(40, 58, 120, 255), apron=1,
                  stache=(150, 92, 52, 255)),
    'lady': dict(skin=SK[0][0], sh=SK[0][1], style='pillbox', hair=(232, 176, 80, 255), hat=(116, 196, 220, 255), suit=(244, 140, 172, 255), shade=(214, 108, 144, 255), coat=1, pearls=1),
    'dad': dict(skin=SK[1][0], sh=SK[1][1], style='fed', hc=(120, 90, 60, 255), suit=(150, 160, 176, 255), shade=(118, 128, 146, 255), tie=(220, 60, 70, 255)),
    'kid': dict(skin=SK[2][0], sh=SK[2][1], style='bob', hair=(40, 30, 34, 255), suit=(240, 196, 60, 255), shade=(214, 164, 40, 255), coat=1),
    'granny': dict(skin=SK[0][0], sh=SK[0][1], style='bun', hair=(222, 222, 230, 255), suit=(150, 96, 180, 255), shade=(120, 72, 150, 255), coat=1, glasses=1, pearls=1),
    'fan': dict(skin=SK[2][0], sh=SK[2][1], style='beanie', hc=NAVY, stripe=GOLD, suit=NAVY, shade=(28, 40, 88, 255), neck='scarf', letter='N', lc=GOLD),
    'fan2': dict(skin=SK[0][0], sh=SK[0][1], style='beanie', hc=BLK, stripe=GOLD, suit=(60, 60, 66, 255), shade=(40, 40, 46, 255), neck='scarf', letter='A', lc=GOLD),
    'exec': dict(skin=SK[1][0], sh=SK[1][1], style='big80', hair=(150, 56, 50, 255), suit=PINK, shade=(196, 50, 120, 255), pads=1, pearls=1),
    'clerk': dict(skin=SK[2][0], sh=SK[2][1], style='ball', hc=(214, 40, 48, 255), hair=(40, 30, 34, 255), suit=(244, 244, 248, 255), shade=(214, 214, 224, 255), vest=(214, 40, 48, 255)),
    'teen': dict(skin=SK[1][0], sh=SK[1][1], style='bun', hair=(52, 40, 46, 255), suit=TEAL, shade=(26, 150, 148, 255), neck='hoodie'),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; st, hr = c['style'], c.get('hair')
    if st == 'bob': d.ellipse(cx, cy - 6, R + 40, R + 24, fill=hr, outline=LINE, width=lw)
    if st == 'pillbox': d.ellipse(cx, cy - 44, R + 30, R + 6, fill=hr, outline=LINE, width=lw)
    if st == 'big80':
        for k in range(11):
            a = math.radians(160 + k * 22); d.ellipse(cx + 192 * math.cos(a), cy - 20 + 196 * math.sin(a), 46, 46, fill=hr, outline=LINE, width=10)
    if st == 'bun': d.ellipse(cx, 44, 56, 46, fill=hr, outline=LINE, width=lw)
    d.ellipse(cx, cy, R, R, fill=c['skin'], outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, c['sh'], c['skin'])
    if st in ('bob', 'pillbox', 'bun', 'big80', 'boater', 'cap'):
        d.chord(cx, cy - 66, R + 8, 132, 180, 360, fill=hr, outline=LINE, width=lw)
    if st == 'cap':                                          # police peaked cap with a gold badge
        for sg in (-1, 1): d.rrect(cx + sg * 178 - 18, cy - 90, cx + sg * 178 + 18, cy + 4, 14, fill=hr, outline=LINE, width=8)
        d.ellipse(cx, 66, 216, 50, fill=NAVY, outline=LINE, width=lw); d.rrect(cx - 168, 98, cx + 168, 158, 16, fill=(26, 32, 60, 255), outline=LINE, width=12)
        d.stroke([(cx - 150, 112), (cx + 150, 112)], GOLD, 7)
        d.poly([(cx - 30, 52), (cx + 30, 52), (cx + 34, 92), (cx, 120), (cx - 34, 92)], fill=GOLD, outline=LINE, width=8); d.dot(cx, 84, 10, (255, 246, 190, 255))
        d.chord(cx, 156, 178, 44, 0, 180, fill=(22, 22, 30, 255), outline=LINE, width=12)
    elif st == 'boater':                                     # straw boater with a red ribbon
        d.ellipse(cx, 138, 246, 38, fill=dk(STRAW, 0.88), outline=LINE, width=lw); d.rrect(cx - 150, 40, cx + 150, 140, 22, fill=STRAW, outline=LINE, width=lw)
        d.rect(cx - 141, 96, cx + 141, 128, RED); d.stroke([(cx - 141, 96), (cx + 141, 96)], LINE, 7); d.stroke([(cx - 141, 128), (cx + 141, 128)], LINE, 7)
        d.chord(cx, 138, 246, 38, 0, 180, fill=dk(STRAW, 0.88), outline=LINE, width=lw)
        for sg in (-1, 1): d.ellipse(cx + sg * 186, cy - 30, 30, 46, fill=hr, outline=LINE, width=9)
    elif st == 'pillbox':                                    # 1961 flip hairdo + a little pillbox hat
        for sg in (-1, 1): d.ellipse(cx + sg * 206, cy + 52, 40, 30, fill=hr, outline=LINE, width=10)
        d.rrect(cx - 92, 16, cx + 92, 84, 22, fill=c['hat'], outline=LINE, width=12); d.dot(cx + 70, 60, 20, (250, 120, 150, 255))
    elif st == 'bob':
        d.poly([(cx - 186, cy - 70), (cx + 186, cy - 70), (cx + 150, cy - 170), (cx - 150, cy - 170)], fill=hr); d.stroke([(cx - 186, cy - 70), (cx + 186, cy - 70)], LINE, 10)
        d.ellipse(cx - 120, cy - 150, 36, 24, fill=(250, 120, 150, 255), outline=LINE, width=7)
    elif st == 'bun':
        d.stroke(bez((cx - 120, cy - 170), (cx - 60, cy - 120), (cx + 40, cy - 130), (cx + 110, cy - 170)), dk(hr, 0.8), 8)
    elif st == 'big80':                                      # 80s volume curls + gold hoops
        for x in (-130, -50, 40, 120): d.ellipse(cx + x, 96, 52, 46, fill=hr, outline=LINE, width=10)
        for sg in (-1, 1): d.ellipse(cx + sg * 196, cy + 86, 22, 28, outline=GOLD, width=9)
    elif st == 'beanie':                                     # bobble hat in team colours
        hc = c['hc']; d.chord(cx, cy - 80, R + 14, 172, 180, 360, fill=hc, outline=LINE, width=lw)
        d.rrect(cx - 168, 92, cx + 168, 118, 10, fill=c['stripe']); d.rrect(cx - 218, cy - 112, cx + 218, cy - 62, 22, fill=dk(hc, 0.8), outline=LINE, width=12)
        for x in range(-190, 200, 34): d.stroke([(cx + x, cy - 106), (cx + x, cy - 68)], dk(hc, 0.6), 6)
        d.ellipse(cx, 22, 38, 30, fill=c['stripe'], outline=LINE, width=10)
    elif st == 'ball':                                       # store cap
        hc = c['hc']; d.chord(cx, cy - 92, R + 10, 168, 180, 360, fill=hc, outline=LINE, width=lw); d.ellipse(cx, 110, 44, 44, fill=WHITE, outline=LINE, width=8)
        d.text(cx, 112, 'S', 56, hc); d.chord(cx, cy - 94, 236, 36, 0, 180, fill=dk(hc, 0.78), outline=LINE, width=12)
    elif st == 'fed':
        hc = c['hc']; d.ellipse(cx, 150, 250, 40, fill=dk(hc, 0.86), outline=LINE, width=lw)
        d.poly([(cx - 150, 150), (cx - 128, 30), (cx - 40, 46), (cx, 64), (cx + 40, 46), (cx + 128, 30), (cx + 150, 150)], fill=hc, outline=LINE, width=lw)
        d.poly([(cx - 141, 104), (cx + 141, 104), (cx + 147, 136), (cx - 147, 136)], fill=(40, 40, 50, 255)); d.chord(cx, 150, 250, 40, 0, 180, fill=dk(hc, 0.86), outline=LINE, width=lw)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 30, 17, fill=BLUSH)
    B.eyes(d, L, Rr, expr, c['skin']); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses'):
        for p in (L, Rr): d.ellipse(p[0], p[1], 48, 44, outline=LINE, width=9)
        d.stroke([(L[0] + 48, ey), (Rr[0] - 48, ey)], LINE, 9)
    my = cy + 74
    if c.get('stache'):
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 34, my - 52), (cx + sg * 62, my - 40), (cx + sg * 72, my - 58)), c['stache'], 20)
        my += 12
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']; base = c['suit']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=base)
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=base); d.clip(sh, mask)
    t = Draw(d.w, d.h); nk = c.get('neck')
    if nk == 'scarf':                                        # team sweater, big letter, striped scarf
        t.text(230, 650, c['letter'], 160, c['lc'], stroke=7, stroke_fill=LINE); t.rect(0, 762, 460, 800, dk(base, 0.78))
        t.rrect(120, 440, 340, 506, 28, fill=c['lc'], outline=LINE, width=8)
        for x in (170, 230, 290): t.rect(x - 12, 444, x + 12, 502, dk(base, 1.0))
        t.rrect(262, 480, 316, 660, 14, fill=c['lc'], outline=LINE, width=8); t.rect(266, 560, 312, 590, base)
    elif nk == 'hoodie':
        t.chord(230, 452, 132, 64, 0, 180, fill=dk(base, 0.78)); t.chord(230, 452, 82, 34, 0, 180, fill=dk(base, 0.55))
        for x in (204, 256): t.stroke([(x, 476), (x - 4, 580)], WHITE, 9); t.dot(x - 4, 584, 9, WHITE)
        t.rrect(150, 676, 310, 760, 24, fill=dk(base, 0.9), outline=LINE, width=6)
    else:
        t.poly([(166, 452), (294, 452), (230, 600)], fill=CREAM if c.get('pearls') else WHITE)
        if c.get('tie'):
            tie = [(230, 474), (208, 500), (214, 626), (230, 650), (246, 626), (252, 500)]; t.poly(tie, fill=c['tie']); t.stroke(tie + [tie[0]], LINE, 6)
        if c.get('bow'):
            for sg in (-1, 1): t.poly([(230, 478), (230 + sg * 46, 456), (230 + sg * 46, 504)], fill=c['bow'], outline=LINE, width=6)
            t.ellipse(230, 480, 14, 14, fill=c['bow'], outline=LINE, width=6)
        if c.get('pearls'):
            for k in range(9): a = math.radians(200 + k * 17.5); t.ellipse(230 + 62 * math.cos(a), 470 - 63 * math.sin(a), 11, 11, fill=WHITE, outline=LINE, width=4)
        if c.get('vest'):                                    # store vest + name tag
            for sg in (-1, 1): t.poly([(230 + sg * 150, 452), (230 + sg * 52, 452), (230 + sg * 8, 620), (230 + sg * 8, 800), (230 + sg * 150, 800)], fill=c['vest'], outline=LINE, width=7)
            t.rrect(266, 552, 352, 600, 10, fill=WHITE, outline=LINE, width=6); t.text(309, 577, 'STAFF', 22, LINE)
        else:
            for sg in (-1, 1):
                lap = [(230 + sg * 64, 452), (230 + sg * 16, 604), (230 + sg * 84, 540), (230 + sg * 108, 456)]; t.poly(lap, fill=dk(base, 0.88)); t.stroke(lap, LINE, 7)
        if c.get('uniform'):                                 # badge, pocket flaps, belt
            t.poly([(140, 532), (182, 532), (186, 566), (161, 592), (136, 566)], fill=GOLD, outline=LINE, width=7); t.dot(161, 560, 9, (255, 246, 190, 255))
            t.rrect(268, 540, 330, 566, 8, fill=dk(base, 0.8), outline=LINE, width=6)
            t.rect(0, 726, 460, 760, (30, 30, 38, 255)); t.rrect(210, 722, 250, 764, 6, fill=GOLD, outline=LINE, width=6)
        elif c.get('apron'):
            t.rrect(132, 566, 328, 840, 30, fill=WHITE, outline=LINE, width=8); t.rrect(186, 640, 274, 706, 12, outline=LINE, width=6)
            t.stroke([(132, 590), (90, 584)], WHITE, 12)
        elif c.get('coat'):
            for y in (626, 700): t.ellipse(258, y, 15, 15, fill=dk(base, 0.7), outline=LINE, width=6)
            t.rect(0, 770, 460, 800, dk(base, 0.82))
        else:
            for y in (668, 736): t.dot(230, y, 10, dk(base, 0.6))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    if c.get('pads'):                                        # 80s shoulder pads
        for sg in (-1, 1): d.ellipse(230 + sg * 128, 486, 62, 38, fill=base, outline=LINE, width=12)
    return d.out()


# ------------------------------------------------------------------ cute props
def eyes2(d, pts, r, mood):
    for i, (x, y) in enumerate(pts):
        d.ellipse(x, y, r, r * 1.12, fill=WHITE, outline=LINE, width=8)
        if mood == 'angry':
            d.dot(x, y + r * 0.2, r * 0.5, LINE); d.dot(x + r * 0.15, y, r * 0.18, WHITE)
            d.stroke([(x - r * 1.1, y - r * (1.45 if i == 0 else 0.75)), (x + r * 1.1, y - r * (0.75 if i == 0 else 1.45))], LINE, 12)
        else:
            d.dot(x + r * 0.18, y, r * 0.58, LINE); d.dot(x + r * 0.32, y - r * 0.2, r * 0.2, WHITE)


def car(col, st, taxi=False):                                # rounded 1960s car, nose right, face on the windshield
    d = Draw(1320, 660); dc = dk(col, 0.82)
    if st == 'honk':
        for a in (-28, 0, 28): x, y = 1200 + 40 * math.cos(math.radians(a)), 380 + 40 * math.sin(math.radians(a)); d.stroke([(x, y), (x + 80 * math.cos(math.radians(a)), y + 80 * math.sin(math.radians(a)))], LINE, 16)
    d.poly(bez((300, 320), (360, 160), (460, 140), (560, 140)) + [(800, 140)] + bez((800, 140), (900, 140), (950, 220), (1000, 320)), fill=col, outline=LINE, width=16)
    d.rrect(40, 300, 1190, 530, 96, fill=col, outline=LINE, width=16); d.rrect(40, 460, 1190, 530, 40, fill=dc)
    d.stroke([(110, 404), (1120, 404)], (244, 244, 250, 255), 14)
    d.rrect(400, 186, 620, 306, 26, fill=GLASS, outline=LINE, width=10); d.rrect(650, 186, 930, 306, 30, fill=GLASS, outline=LINE, width=10)
    if taxi:
        d.rrect(560, 70, 760, 146, 16, fill=(250, 240, 200, 255), outline=LINE, width=10); d.text(660, 108, 'TAXI', 50, LINE)
        for k in range(12): d.rect(150 + k * 80, 430 + (k % 2) * 22, 190 + k * 80, 452 + (k % 2) * 22, BLK)
    eyes2(d, [(725, 248), (848, 248)], 44, 'angry' if st == 'honk' else 'calm')
    for x in (690, 880): d.ellipse(x, 340, 30, 15, fill=BLUSH)
    d.dot(1160, 360, 34, (255, 240, 150, 255)); d.ellipse(1160, 360, 34, 34, outline=LINE, width=9); d.rrect(48, 340, 86, 400, 10, fill=RED, outline=LINE, width=8)
    if st == 'honk': d.ellipse(1080, 450, 46, 40, fill=MOUTHC, outline=LINE, width=9)
    else: d.chord(1080, 432, 54, 40, 0, 180, fill=MOUTHC, outline=LINE, width=9)
    for x in (1170, 60): d.rrect(x - 30, 470, x + 30, 520, 14, fill=(230, 232, 240, 255), outline=LINE, width=9)
    for x in (290, 960): d.ellipse(x, 540, 92, 92, fill=(44, 42, 52, 255), outline=LINE, width=14); d.ellipse(x, 540, 42, 42, fill=(222, 224, 232, 255), outline=LINE, width=8)
    return d.out()


def football():
    d = Draw(760, 520); d.ellipse(380, 260, 330, 210, fill=(162, 92, 48, 255), outline=LINE, width=16)
    for sg in (-1, 1): d.stroke(bez((380 + sg * 230, 110), (380 + sg * 200, 200), (380 + sg * 200, 320), (380 + sg * 230, 410)), WHITE, 18)
    d.stroke([(290, 110), (470, 110)], WHITE, 14)
    for x in range(310, 461, 30): d.stroke([(x, 92), (x, 128)], WHITE, 10)
    eyes2(d, [(320, 250), (440, 250)], 40, 'calm'); d.chord(380, 330, 40, 30, 0, 180, fill=MOUTHC, outline=LINE, width=8)
    for x in (270, 490): d.ellipse(x, 320, 26, 14, fill=BLUSH)
    return d.out()


def steam():
    d = Draw(620, 380)
    for cx, cy in ((150, 230), (470, 230)):
        blobs = ((cx - 60, cy, 64), (cx, cy - 50, 76), (cx + 60, cy, 64), (cx, cy + 20, 60))
        for x, y, r in blobs: d.ellipse(x, y, r, r, fill=WHITE, outline=LINE, width=12)
        for x, y, r in blobs: d.ellipse(x, y, r - 8, r - 8, fill=WHITE)
    for a in (45, 135, 225, 315):                            # red anger mark
        x, y = 310 + 40 * math.cos(math.radians(a)), 90 + 40 * math.sin(math.radians(a)); d.arc(x, y, 34, 34, a + 100, a + 260, RED, 16)
    return d.out()


def bulb():
    d = Draw(480, 600)
    for k in range(8): a = math.radians(180 + k * 25.7); d.stroke([(240 + 190 * math.cos(a), 230 + 190 * math.sin(a)), (240 + 236 * math.cos(a), 230 + 236 * math.sin(a))], GOLD, 18)
    d.ellipse(240, 230, 150, 150, fill=(255, 236, 110, 255), outline=LINE, width=14); d.ellipse(190, 180, 36, 50, fill=(255, 250, 220, 255))
    d.rrect(170, 370, 310, 470, 16, fill=(196, 200, 212, 255), outline=LINE, width=12)
    for y in (402, 438): d.stroke([(176, y), (304, y)], LINE, 7)
    d.chord(240, 470, 56, 50, 0, 180, fill=(110, 110, 124, 255), outline=LINE, width=10); return d.out()


def cricket():
    d = Draw(560, 420); G_ = (110, 190, 80, 255)
    for x, y in ((180, 300), (300, 310), (400, 300)): d.stroke([(x, 250), (x - 30, y + 60), (x - 70, y + 70)], LINE, 12)
    d.ellipse(250, 240, 170, 90, fill=G_, outline=LINE, width=14); d.ellipse(420, 200, 92, 88, fill=G_, outline=LINE, width=14)
    for sg in (-1, 1): d.stroke(bez((420 + sg * 30, 120), (420 + sg * 60, 40), (420 + sg * 110, 20), (420 + sg * 130, 50)), LINE, 10)
    eyes2(d, [(390, 190), (460, 190)], 30, 'calm'); d.arc(425, 250, 22, 14, 20, 160, LINE, 8)
    d.text(130, 90, '...', 120, LINE); return d.out()


def pin():
    d = Draw(240, 360); d.poly([(70, 170), (170, 170), (120, 350)], fill=BLK, outline=LINE, width=10)
    d.ellipse(120, 120, 104, 104, fill=BLK, outline=LINE, width=12); d.ellipse(84, 84, 22, 18, fill=(120, 120, 140, 255))
    d.text(120, 126, 'BF', 64, WHITE); return d.out()


def board(named):                                            # police duty board: roster -> BLACK FRIDAY
    d = Draw(1200, 860); d.rrect(10, 10, 1190, 850, 30, fill=(150, 104, 64, 255), outline=LINE, width=18); d.rect(60, 60, 1140, 800, (50, 92, 74, 255))
    C_ = (236, 242, 236, 255); d.text(600, 130, 'DUTY ROSTER', 84, C_)
    for k, (a, b) in enumerate((('FRI', 'ALL COPS'), ('SAT', 'ALL COPS'), ('SHIFT', '12 HOURS'))):
        d.text(260, 280 + k * 130, a, 66, C_); d.text(760, 280 + k * 130, b, 66, C_); d.stroke([(110, 330 + k * 130), (1090, 330 + k * 130)], (150, 180, 160, 255), 5)
    if named:
        d.rrect(120, 260, 1080, 700, 40, fill=(40, 80, 64, 255)); d.text(600, 400, 'BLACK', 190, WHITE, stroke=6, stroke_fill=(20, 20, 24, 255))
        d.text(600, 590, 'FRIDAY', 190, WHITE, stroke=6, stroke_fill=(20, 20, 24, 255)); d.stroke([(200, 690), (1000, 680)], (255, 120, 120, 255), 14)
    d.rect(150, 806, 450, 830, (250, 250, 250, 255)); return d.out()


def banner():
    d = Draw(1700, 480); pts = [(30, 40), (1670, 40), (1670, 360)] + [(1670 - k * 82 - (41 if j else 0), 360 + (40 if j else 0)) for k in range(20) for j in (0, 1)] + [(30, 360)]
    d.poly(pts, fill=(222, 50, 64, 255), outline=LINE, width=14); d.rect(30, 30, 1670, 70, GOLD)
    for x in (130, 1570): d.text(x, 210, '*', 200, GOLD)
    d.text(850, 210, 'BIG FRIDAY!', 190, WHITE, stroke=9, stroke_fill=LINE); return d.out()


def ledger(red):
    d = Draw(1200, 800); d.rrect(20, 40, 1180, 780, 30, fill=(70, 50, 40, 255), outline=LINE, width=14)
    for x0 in (50, 610): d.rrect(x0, 60, x0 + 540, 750, 18, fill=(252, 248, 232, 255), outline=LINE, width=10)
    d.stroke([(600, 60), (600, 750)], LINE, 10); d.text(320, 120, 'LEDGER', 70, LINE); d.text(880, 120, '1985', 70, LINE)
    for k in range(5):
        y = 220 + k * 92; d.stroke([(90, y + 40), (560, y + 40)], (190, 196, 210, 255), 5)
        d.text(320, y, ('-$900', '-$700', '-$800', '-$600', '-$900')[k] if red else ('+$900', '+$700', '+$8,000', '+$9,000', '+$9,900')[k], 64, RED if red else BLK)
    if red: d.poly([(820, 260), (940, 260), (940, 520), (1010, 520), (880, 680), (750, 520), (820, 520)], fill=RED, outline=LINE, width=12)
    else: d.poly([(820, 680), (940, 680), (940, 420), (1010, 420), (880, 260), (750, 420), (820, 420)], fill=(40, 170, 90, 255), outline=LINE, width=12)
    return d.out()


def bags():
    d = Draw(700, 560)
    for x, w, h, col, t in ((170, 130, 300, PINK, 'SALE'), (380, 150, 360, GOLD, ''), (560, 110, 260, TEAL, '')):
        d.stroke(bez((x - w * 0.5, 540 - h), (x - w * 0.5, 540 - h - 110), (x + w * 0.5, 540 - h - 110), (x + w * 0.5, 540 - h)), LINE, 12)
        d.poly([(x - w, 540 - h), (x + w, 540 - h), (x + w + 14, 540), (x - w - 14, 540)], fill=col, outline=LINE, width=12)
        if t: d.text(x, 540 - h / 2, t, 56, WHITE, stroke=4, stroke_fill=LINE)
    d.ellipse(380, 360, 40, 40, fill=WHITE, outline=LINE, width=8); d.text(380, 362, '$', 50, LINE); return d.out()


def news():
    d = Draw(860, 960); d.rect(30, 30, 830, 930, (246, 242, 228, 255)); d.rrect(30, 30, 830, 930, 10, outline=LINE, width=12)
    d.text(430, 100, 'THE DAILY NEWS', 64, LINE); d.stroke([(60, 150), (800, 150)], LINE, 8)
    d.text(430, 250, 'BLACK', 150, BLK); d.text(430, 400, 'FRIDAY!', 150, BLK)
    d.rrect(70, 500, 420, 860, 10, fill=(206, 206, 214, 255), outline=LINE, width=8); d.ellipse(245, 640, 80, 80, fill=SK[1][0], outline=LINE, width=8)
    d.ellipse(245, 560, 96, 30, fill=NAVY, outline=LINE, width=8); d.chord(245, 690, 30, 24, 0, 180, fill=LINE)
    for k in range(9): d.stroke([(460, 520 + k * 38), (790, 520 + k * 38)], (150, 150, 160, 255), 10)
    return d.out()


def btag(txt, w, size):                                      # black-and-gold sign
    d = Draw(w, 230); d.rrect(14, 14, w - 14, 216, 30, fill=BLK, outline=LINE, width=14); d.rrect(38, 38, w - 38, 192, 18, outline=GOLD, width=7)
    d.text(w / 2, 118, txt, size, GOLD, stroke=5, stroke_fill=LINE); return d.out()


def h12():
    d = G.card(880, 520); d.ellipse(250, 260, 180, 180, fill=WHITE, outline=LINE, width=16)
    for k in range(12): a = math.radians(k * 30); d.stroke([(250 + 150 * math.cos(a), 260 + 150 * math.sin(a)), (250 + 170 * math.cos(a), 260 + 170 * math.sin(a))], LINE, 10)
    d.stroke([(250, 260), (250, 130)], LINE, 16); d.stroke([(250, 260), (350, 260)], RED, 12); d.dot(250, 260, 18, LINE)
    d.text(640, 220, '12', 220, RED, stroke=9, stroke_fill=LINE); d.text(640, 410, 'HOURS', 82, LINE); return d.out()


def armynavy():
    d = G.card(1000, 460); d.text(250, 190, 'ARMY', 130, BLK, stroke=6, stroke_fill=GOLD); d.text(500, 190, 'vs', 70, LINE)
    d.text(750, 190, 'NAVY', 130, NAVY, stroke=6, stroke_fill=GOLD); d.text(500, 360, 'FOOTBALL GAME', 70, RED); return d.out()


def turkey():
    d = Draw(760, 680)
    for k in range(9):
        a = math.radians(180 + k * 22.5); d.ellipse(380 + 230 * math.cos(a), 360 + 230 * math.sin(a), 70, 70, fill=(RED, (242, 130, 44, 255), GOLD)[k % 3], outline=LINE, width=12)
    d.ellipse(380, 420, 170, 160, fill=(150, 96, 60, 255), outline=LINE, width=14); d.ellipse(380, 300, 96, 92, fill=(186, 128, 84, 255), outline=LINE, width=14)
    eyes2(d, [(346, 290), (414, 290)], 26, 'calm'); d.poly([(360, 330), (400, 330), (380, 366)], fill=(242, 170, 40, 255), outline=LINE, width=7)
    d.ellipse(406, 380, 16, 26, fill=RED, outline=LINE, width=6)
    for x in (300, 460): d.ellipse(x, 340, 20, 12, fill=BLUSH)
    for x in (320, 440): d.stroke([(x, 570), (x, 640)], (242, 170, 40, 255), 14)
    return d.out()


# ------------------------------------------------------------------ set dressing (props/, textures/, bg/)
def shopfront(path, sign, wall, a1, a2, kind):
    W, Hh = 1200, 1300; d = Draw(W, Hh); d.rect(0, 0, W, Hh, wall); d.rrect(4, 4, W - 4, Hh - 4, 8, outline=LINE, width=14)
    d.rrect(90, 50, 1110, 220, 24, fill=(46, 44, 70, 255), outline=LINE, width=12); d.text(600, 138, sign, 110, (255, 226, 120, 255), stroke=5, stroke_fill=LINE)
    for k in range(10): d.poly([(60 + k * 108, 260), (168 + k * 108, 260), (168 + k * 108, 400), (60 + k * 108, 400)], fill=a1 if k % 2 == 0 else a2)
    for k in range(10): d.chord(114 + k * 108, 400, 54, 40, 0, 180, fill=a1 if k % 2 == 0 else a2, outline=LINE, width=8)
    d.rrect(60, 252, 1140, 404, 6, outline=LINE, width=10)
    d.rrect(80, 470, 760, 1100, 20, fill=GLASS, outline=LINE, width=14); d.stroke([(120, 520), (240, 640)], WHITE, 18)
    if kind == 'toys':
        d.ellipse(300, 860, 110, 120, fill=(196, 140, 90, 255), outline=LINE, width=10); d.ellipse(300, 700, 90, 84, fill=(196, 140, 90, 255), outline=LINE, width=10)
        for sg in (-1, 1): d.ellipse(300 + sg * 70, 630, 34, 34, fill=(196, 140, 90, 255), outline=LINE, width=8)
        d.dot(270, 690, 10, LINE); d.dot(330, 690, 10, LINE); d.ellipse(560, 900, 110, 110, fill=RED, outline=LINE, width=10); d.stroke([(460, 900), (660, 900)], WHITE, 22)
    elif kind == 'shoes':
        for x, y, col in ((260, 760, RED), (520, 760, NAVY), (390, 960, (242, 130, 44, 255))):
            d.poly([(x - 110, y), (x - 110, y - 90), (x - 30, y - 90), (x + 10, y - 40), (x + 110, y - 20), (x + 110, y)], fill=col, outline=LINE, width=10)
    else:
        d.poly([(300, 640), (200, 1040), (400, 1040)], fill=PINK, outline=LINE, width=10); d.ellipse(300, 600, 46, 46, fill=CREAM, outline=LINE, width=8)
        d.poly([(560, 640), (460, 1040), (660, 1040)], fill=TEAL, outline=LINE, width=10); d.ellipse(560, 600, 46, 46, fill=CREAM, outline=LINE, width=8)
    d.rrect(180, 1000, 420, 1080, 12, fill=RED, outline=LINE, width=8); d.text(300, 1042, 'SALE!', 60, WHITE)
    d.rrect(820, 470, 1110, 1300, 16, fill=(130, 84, 60, 255), outline=LINE, width=14); d.rrect(870, 520, 1060, 860, 12, fill=GLASS, outline=LINE, width=10)
    d.dot(1070, 960, 18, GOLD); d.rect(0, 1250, 800, 1300, dk(wall, 0.7)); d.out().save(path)


def skyline(path):
    im = CA.gradient((110, 170, 236), (236, 242, 250)); dr = ImageDraw.Draw(im); CA.towers(dr, 800, (160, 172, 200), None, 1800, 11, 160, 420)
    c = (130, 140, 172); dr.rectangle([840, 300, 960, 800], fill=c); dr.rectangle([860, 200, 940, 300], fill=c); dr.polygon([(870, 200), (900, 90), (930, 200)], fill=c)
    dr.ellipse([880, 240, 920, 280], fill=(240, 240, 220)); im.save(path)


def stands(path):
    W, Hh = 3400, 1000; d = Draw(W, Hh); R_ = np.random.RandomState(5)
    for k in range(8):
        y = 300 + k * 88; d.rect(0, y, W, y + 88, (150, 156, 172, 255) if k % 2 else (176, 182, 196, 255)); d.stroke([(0, y), (W, y)], LINE, 6)
        for x in range(30 + (k % 2) * 25, W, 56):
            col = [SK[0][0], SK[1][0], SK[2][0]][R_.randint(3)]; hat = [NAVY, BLK, GOLD, RED, None][R_.randint(5)]
            d.ellipse(x, y + 30, 22, 22, fill=col, outline=LINE, width=4); d.dot(x - 7, y + 30, 3, LINE); d.dot(x + 7, y + 30, 3, LINE)
            if hat: d.chord(x, y + 22, 23, 18, 180, 360, fill=hat)
    for x0, txt, col, tc in ((300, 'GO ARMY!', BLK, GOLD), (1950, 'GO NAVY!', NAVY, GOLD)):
        d.rrect(x0, 150, x0 + 1150, 290, 20, fill=col, outline=LINE, width=12); d.text(x0 + 575, 222, txt, 110, tc, stroke=5, stroke_fill=LINE)
    d.rect(0, 290, W, 306, (230, 230, 236, 255)); d.out().save(path)


def pdwall(path):
    W, Hh = 2400, 1100; d = Draw(W, Hh)
    d.rrect(560, 20, 1840, 170, 20, fill=NAVY, outline=LINE, width=12); d.text(1200, 98, 'POLICE  DEPT.  PHILADELPHIA', 72, GOLD, stroke=4, stroke_fill=LINE)
    for k in range(6):
        x = 40 + k * 150; d.rrect(x, 330, x + 140, 1090, 10, fill=(96, 128, 150, 255), outline=LINE, width=10)
        for j in range(4): d.stroke([(x + 40, 400 + j * 22), (x + 100, 400 + j * 22)], LINE, 6)
        d.rrect(x + 104, 640, x + 120, 720, 4, fill=(200, 200, 210, 255))
    d.ellipse(1220, 470, 150, 150, fill=WHITE, outline=LINE, width=14)
    for k in range(12): a = math.radians(k * 30); d.stroke([(1220 + 120 * math.cos(a), 470 + 120 * math.sin(a)), (1220 + 138 * math.cos(a), 470 + 138 * math.sin(a))], LINE, 8)
    d.stroke([(1220, 470), (1220, 365)], LINE, 14); d.stroke([(1220, 470), (1300, 520)], LINE, 12)
    for x in (2000, 2230):
        d.rect(x - 90, 260, x + 90, 500, (250, 246, 230, 255)); d.rrect(x - 90, 260, x + 90, 500, 6, outline=LINE, width=6); d.text(x, 300, 'WANTED', 40, RED)
        d.ellipse(x, 400, 50, 54, fill=SK[1][0], outline=LINE, width=6); d.stroke([(x - 30, 380), (x + 30, 380)], LINE, 18)
    d.out().save(path)


def storewall(path):
    W, Hh = 2400, 1100; d = Draw(W, Hh)
    d.rrect(500, 10, 1900, 170, 26, fill=(120, 40, 60, 255), outline=LINE, width=12); d.text(1200, 92, 'GRAND DEPARTMENT STORE', 76, (255, 226, 120, 255), stroke=4, stroke_fill=LINE)
    for k in range(18): d.ellipse(80 + k * 132, 220, 60, 30, fill=(70, 150, 80, 255), outline=LINE, width=6); d.dot(80 + k * 132, 240, 14, RED if k % 2 else GOLD)
    R_ = np.random.RandomState(8)
    for row, y in enumerate((440, 700)):
        d.rect(40, y + 120, W - 40, y + 146, (150, 104, 64, 255)); d.stroke([(40, y + 146), (W - 40, y + 146)], LINE, 8)
        for k in range(14):
            x = 110 + k * 165; col = [RED, GOLD, TEAL, PINK, NAVY, (242, 130, 44, 255)][R_.randint(6)]
            if row == 0: d.rrect(x - 60, y, x + 60, y + 118, 10, fill=col, outline=LINE, width=7); d.stroke([(x, y), (x, y + 118)], WHITE, 10)
            else: d.chord(x, y + 112, 64, 74, 180, 360, fill=col, outline=LINE, width=7); d.ellipse(x, y + 114, 78, 14, fill=dk(col, 0.8), outline=LINE, width=6)
    d.out().save(path)


def usmap(path):
    W, Hh = 1800, 1100; d = Draw(W, Hh); d.rrect(10, 10, W - 10, Hh - 10, 40, fill=(122, 178, 222, 255), outline=LINE, width=20)
    US = [(150, 180), (120, 360), (170, 560), (260, 700), (520, 770), (700, 790), (830, 900), (930, 830), (1100, 800), (1250, 820), (1330, 960), (1400, 950),
          (1380, 800), (1500, 700), (1580, 520), (1660, 340), (1700, 220), (1600, 200), (1480, 300), (1360, 260), (1230, 300), (1150, 220), (980, 200), (600, 180)]
    d.poly(US, fill=(244, 228, 186, 255), outline=LINE, width=14)
    for x in (420, 700, 980, 1240): d.stroke([(x, 200), (x + 20, 760)], (214, 196, 156, 255), 6)
    d.stroke([(160, 460), (1600, 440)], (214, 196, 156, 255), 6)
    d.text(900, 1010, 'U . S . A .', 70, WHITE, stroke=5, stroke_fill=LINE); d.out().save(path)


def eighties(path):                                          # Memphis-pattern 1980s wall with a neon sign
    W, Hh = 2400, 1100; im = Image.new('RGBA', (W, Hh), (250, 214, 226, 255)); d = Draw(W, Hh); R_ = np.random.RandomState(3)
    for k in range(60):
        x, y, t = R_.uniform(0, W), R_.uniform(300, Hh), R_.randint(3); col = [TEAL, GOLD, (110, 90, 220, 255)][R_.randint(3)]
        if t == 0: d.poly([(x, y - 40), (x + 44, y + 34), (x - 44, y + 34)], fill=col, outline=LINE, width=6)
        elif t == 1: d.stroke([(x - 60 + j * 20, y + (16 if j % 2 else -16)) for j in range(7)], col, 12)
        else: d.dot(x, y, 16, LINE)
    d.rrect(560, 30, 1840, 260, 40, fill=(40, 30, 70, 255), outline=LINE, width=14)
    g = Draw(W, Hh); g.text(1200, 146, 'SALES  H.Q.', 150, (255, 80, 200, 255)); glow = g.out().filter(ImageFilter.GaussianBlur(22))
    im.alpha_composite(d.out()); im.alpha_composite(glow); im.alpha_composite(glow)
    t = Draw(W, Hh); t.text(1200, 146, 'SALES  H.Q.', 150, (255, 220, 246, 255)); im.alpha_composite(t.out()); im.save(path)


def mall(path):
    W, Hh = 2400, 1300; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (236, 236, 244, 255)); d.rrect(4, 4, W - 4, Hh - 4, 8, outline=LINE, width=14)
    d.rrect(700, 30, 1700, 200, 30, fill=(214, 40, 48, 255), outline=LINE, width=12); d.text(1200, 118, 'MEGA STORE', 110, WHITE, stroke=5, stroke_fill=LINE)
    for x0 in (60, 1640):
        d.rrect(x0, 260, x0 + 700, 1180, 24, fill=BLK, outline=LINE, width=14); d.rrect(x0 + 30, 290, x0 + 670, 1150, 16, outline=GOLD, width=8)
        d.text(x0 + 350, 470, 'BLACK', 150, GOLD, stroke=5, stroke_fill=LINE); d.text(x0 + 350, 630, 'FRIDAY', 150, GOLD, stroke=5, stroke_fill=LINE)
        d.text(x0 + 350, 860, 'SALE', 190, WHITE, stroke=6, stroke_fill=LINE); d.text(x0 + 350, 1040, 'UP TO 70% OFF', 64, (255, 120, 120, 255))
    d.rrect(820, 300, 1580, 1300, 20, fill=GLASS, outline=LINE, width=14); d.stroke([(1200, 300), (1200, 1300)], LINE, 12)
    for x in (900, 1280): d.stroke([(x, 380), (x + 120, 520)], WHITE, 20)
    for x in (1160, 1240): d.rrect(x - 10, 700, x + 10, 860, 6, fill=(200, 204, 214, 255), outline=LINE, width=5)
    d.out().save(path)


def tiles(path, c1, c2, n=512):
    im = Image.new('RGB', (n, n), c1); dr = ImageDraw.Draw(im); s = n // 4
    for i in range(4):
        for j in range(4):
            if (i + j) % 2: dr.rectangle([i * s, j * s, i * s + s, j * s + s], fill=c2)
    im.save(path, quality=92)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shouting', 'sneaky')]
    multi = dict(carA={s: car((90, 196, 190, 255), s) for s in ('default', 'honk')}, carB={s: car((226, 76, 86, 255), s) for s in ('default', 'honk')},
                 carC={s: car((250, 204, 64, 255), s, True) for s in ('default', 'honk')}, board={'default': board(False), 'named': board(True)},
                 ledger={'default': ledger(True), 'black': ledger(False)})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    B.sparkle(Pp('sparkle.png'))
    cards = dict(football=football(), steam=steam(), bulb=bulb(), cricket=cricket(), pin=pin(), bigfri=banner(), bags=bags(), news=news(), h12=h12(),
                 armynavy=armynavy(), turkey=turkey(), bfsign=btag('BLACK FRIDAY', 1000, 108), notthem=CA.stamp('NOT THEM!', 760, 110),
                 cops=V.wtag('NAMED BY COPS!', 1080, BLUE, 82), philly=V.big_card('1961', 'PHILADELPHIA', BLUE, 800),
                 thx=V.wtag('DAY AFTER THANKSGIVING', 1380, (242, 130, 44, 255), 64), flood=V.wtag('SHOPPERS FLOOD IN!', 1200, (126, 70, 140, 255), 72),
                 tourists=V.wtag('+ TOURISTS!', 820, GREEN, 84), gridlock=CA.stamp('GRIDLOCK!', 820, 104), crowds=CA.stamp('CROWDS!', 720, 110),
                 chaos=CA.stamp('CHAOS!', 660, 116), nodayoff=V.wtag('NO DAY OFF!', 820, RED, 88), dark=V.wtag('A DARK NAME...', 940, (60, 56, 70, 255), 80),
                 hate=V.wtag('STORES HATE IT!', 1020, RED, 80), rebrand=V.wtag('REBRAND IT!', 760, GREEN, 90), nobody=CA.stamp('NOBODY SAYS IT', 1000, 92),
                 wontdie=V.wtag("IT WON'T DIE!", 900, (60, 56, 70, 255), 84), coast=V.wtag('COAST TO COAST!', 1020, BLUE, 80),
                 tactic=V.wtag('NEW PLAN!', 700, (126, 70, 140, 255), 92), change=V.wtag('CHANGE WHAT IT MEANS!', 1320, (242, 130, 44, 255), 66),
                 y1980=V.big_card('1980s', 'A NEW STORY', PINK, 780), inred=V.wtag('IN THE RED', 820, RED, 88), inblack=btag('IN THE BLACK', 860, 88),
                 perfect=V.wtag('SOUNDS PERFECT!', 1020, GREEN, 78), myth=CA.stamp('NOT TRUE!', 760, 116), today=V.wtag('TODAY', 540, BLUE, 100),
                 salebig=btag('BLACK FRIDAY SALE', 1260, 84), insult=V.wtag("THE COPS' INSULT!", 1120, RED, 74), why=B.sticker_mark('?', GOLD),
                 shh=B.sticker_burst('SHHH!'), sparkle=Image.open(Pp('sparkle.png')).convert('RGBA'))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in cards.items()}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); G.tex_asphalt(T('asphalt.jpg')); B.tex_grass(T('grass.jpg'))
    tiles(T('tiles.jpg'), (238, 226, 200), (196, 72, 80)); tiles(T('tiles80.jpg'), (60, 200, 196), (250, 236, 244)); tiles(T('mallfloor.jpg'), (232, 232, 240), (206, 208, 222))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg'))
    shopfront(Pp('shop_toys.png'), 'TOYS', (232, 180, 186, 255), RED, WHITE, 'toys'); shopfront(Pp('shop_dept.png'), 'DEPT STORE', (244, 222, 176, 255), (40, 150, 110, 255), WHITE, 'dept')
    shopfront(Pp('shop_shoes.png'), 'SHOES', (184, 216, 226, 255), NAVY, GOLD, 'shoes')
    skyline(Pp('skyphl.png')); stands(Pp('stands.png')); pdwall(Pp('pdwall.png')); storewall(Pp('storewall.png')); usmap(Pp('usmap.png')); eighties(Pp('eighties.png')); mall(Pp('mall.png'))
    VA.skyplane(Pp('skyday.png'), (92, 150, 226), (226, 240, 252)); B.window(Pp('window.png'))
    for n in ('shop_toys', 'shop_dept', 'shop_shoes', 'skyphl', 'stands', 'pdwall', 'storewall', 'usmap', 'eighties', 'mall'): items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
