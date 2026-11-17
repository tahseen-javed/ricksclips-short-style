#!/usr/bin/env python3
"""Assets for video 06 (FedEx blackjack), drawn in code with the channel builders.
New cast: young Fred Smith (1973 suit; the same head as a Yale student in 1965), a Las Vegas dealer, a Yale professor
and two investors. Cute props: Falcon jets with faces (parked / flying / sad), parcels with faces, playing cards that
flip (back -> face), chips, a money jar (full / empty), dollar bills, a lifebuoy, a money bag, a term paper (blank /
graded C), a neon LAS VEGAS sign, slot machines, a hub-and-spoke wall map, a chalkboard, a Yale pennant, casino carpet.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math
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
PURP, ORNG, SILVER, CREAM, GLASS, FELT = (96, 56, 156, 255), (242, 130, 44, 255), (200, 208, 220, 255), (250, 238, 206, 255), (150, 212, 240, 255), (46, 140, 88, 255)
CARD_BOX, CASH = (204, 150, 92, 255), (120, 186, 100, 255)
NEW = {
    'fred': dict(skin=SK[0][0], sh=SK[0][1], style='part', hair=(118, 76, 44, 255), suit=(66, 78, 140, 255), shade=(50, 58, 108, 255), tie=ORNG),
    'fredc': dict(look='fred', suit=(46, 76, 150, 255), shade=(34, 56, 116, 255), sweater=1),
    'dealer': dict(skin=SK[2][0], sh=SK[2][1], style='visor', hair=(52, 42, 50, 255), suit=(186, 50, 62, 255), shade=(146, 36, 48, 255), bow=(44, 40, 50, 255),
                   vest=1, stache=(52, 42, 50, 255)),
    'prof': dict(skin=SK[1][0], sh=SK[1][1], style='bald', hair=(238, 238, 242, 255), suit=(156, 116, 78, 255), shade=(124, 90, 58, 255), bow=(150, 40, 66, 255),
                 glasses=1, beard=(240, 240, 244, 255), tweed=1),
    'inv1': dict(skin=SK[2][0], sh=SK[2][1], style='fed', hc=(62, 66, 84, 255), suit=(104, 110, 128, 255), shade=(80, 86, 104, 255), tie=(52, 150, 104, 255), glasses=1),
    'inv2': dict(skin=SK[0][0], sh=SK[0][1], style='bob', hair=(156, 66, 50, 255), suit=(44, 150, 150, 255), shade=(32, 116, 116, 255), pearls=1),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[NEW[char].get('look', char)]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; st, hr = c['style'], c.get('hair')
    if st == 'bob': d.ellipse(cx, cy - 6, R + 44, R + 26, fill=hr, outline=LINE, width=lw)       # bob behind the face
    d.ellipse(cx, cy, R, R, fill=c['skin'], outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, c['sh'], c['skin'])
    if st in ('part', 'visor', 'bob'):                       # hair cap
        d.chord(cx, cy - 66, R + 8, 132, 180, 360, fill=hr, outline=LINE, width=lw)
    if st == 'part':                                         # 1970s side-parted swoop and sideburns
        sw = bez((cx - 196, cy - 80), (cx - 90, cy - 20), (cx + 30, cy - 96), (cx + 204, cy - 104))
        d.poly(sw + [(cx + 190, cy - 160), (cx - 180, cy - 150)], fill=hr); d.stroke(sw, LINE, lw)
        d.stroke(bez((cx - 80, cy - 192), (cx - 70, cy - 160), (cx - 56, cy - 136), (cx - 30, cy - 118)), dk(hr, 0.7), 9)
        d.dot(cx + 40, cy - 150, 22, dk(hr, 1.25) if False else (160, 112, 72, 255))
        for sg in (-1, 1): d.rrect(cx + sg * 176 - 20, cy - 96, cx + sg * 176 + 20, cy + 14, 16, fill=hr, outline=LINE, width=8)
    elif st == 'visor':                                      # slick hair, green dealer visor
        d.stroke(bez((cx - 150, cy - 150), (cx - 60, cy - 176), (cx + 60, cy - 176), (cx + 150, cy - 150)), dk(hr, 1.6) if False else (96, 84, 96, 255), 8)
        d.rrect(cx - 206, cy - 150, cx + 206, cy - 112, 16, fill=(60, 60, 70, 255), outline=LINE, width=10)
        d.chord(cx, cy - 112, 236, 52, 0, 180, fill=(84, 196, 126, 210), outline=LINE, width=12)
    elif st == 'bald':                                       # shiny top, white side tufts
        d.ellipse(cx - 64, cy - 146, 46, 20, fill=(255, 255, 255, 150))
        for sg in (-1, 1):
            for dx, dy, r in ((0, -40, 44), (10, 10, 40), (-6, -84, 34)): d.ellipse(cx + sg * (192 + dx), cy + dy, r, r, fill=hr, outline=LINE, width=9)
    elif st == 'bob':                                        # straight fringe
        d.poly([(cx - 186, cy - 70), (cx + 186, cy - 70), (cx + 150, cy - 170), (cx - 150, cy - 170)], fill=hr)
        d.stroke([(cx - 186, cy - 70), (cx + 186, cy - 70)], LINE, 10)
        d.ellipse(cx + 120, cy - 150, 34, 22, fill=(250, 120, 150, 255), outline=LINE, width=7)      # hair clip
    elif st == 'fed':                                        # fedora (same build as video 05)
        hc = c['hc']; d.ellipse(cx, 150, 250, 40, fill=dk(hc, 0.86), outline=LINE, width=lw)
        d.poly([(cx - 150, 150), (cx - 128, 30), (cx - 40, 46), (cx, 64), (cx + 40, 46), (cx + 128, 30), (cx + 150, 150)], fill=hc, outline=LINE, width=lw)
        d.poly([(cx - 141, 104), (cx + 141, 104), (cx + 147, 136), (cx - 147, 136)], fill=(200, 160, 70, 255))
        d.chord(cx, 150, 250, 40, 0, 180, fill=dk(hc, 0.86), outline=LINE, width=lw)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 28, 16, fill=BLUSH)
    B.eyes(d, L, Rr, expr, c['skin']); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses'):
        for p in (L, Rr): d.ellipse(p[0], p[1], 48, 44, outline=LINE, width=9)
        d.stroke([(L[0] + 48, ey), (Rr[0] - 48, ey)], LINE, 9)
    my = cy + 74
    if c.get('beard'): d.chord(cx, cy + 84, 156, 118, 0, 180, fill=c['beard'], outline=LINE, width=lw)
    if c.get('stache'):
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 30, my - 50), (cx + sg * 58, my - 40), (cx + sg * 70, my - 54)), c['stache'], 20)
        my += 12
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def bowtie(t, col):
    for sg in (-1, 1): t.poly([(230, 478), (230 + sg * 46, 456), (230 + sg * 46, 504)], fill=col, outline=LINE, width=6)
    t.ellipse(230, 480, 14, 14, fill=col, outline=LINE, width=6)


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']; base = c['suit']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=base)
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=base); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if c.get('sweater'):                                     # Yale sweater: ribbed collar and hem, a big Y
        t.chord(230, 452, 96, 52, 0, 180, fill=dk(base, 0.7)); t.chord(230, 452, 70, 34, 0, 180, fill=c.get('shirt', WHITE))
        t.text(230, 636, 'Y', 170, WHITE, stroke=7, stroke_fill=LINE); t.rect(0, 762, 460, 800, dk(base, 0.78))
    else:
        t.poly([(166, 452), (294, 452), (230, 600)], fill=CREAM if c.get('pearls') else WHITE)
        if c.get('tie'):
            tie = [(230, 474), (208, 500), (214, 626), (230, 650), (246, 626), (252, 500)]; t.poly(tie, fill=c['tie']); t.stroke(tie + [tie[0]], LINE, 6)
        if c.get('bow'): bowtie(t, c['bow'])
        if c.get('pearls'):
            for k in range(9): a = math.radians(200 + k * 17.5); t.ellipse(230 + 62 * math.cos(a) * 1.0, 470 - 70 * math.sin(a) * 0.9, 11, 11, fill=WHITE, outline=LINE, width=4)
        for sg in (-1, 1):                                   # wide 70s lapels
            lap = [(230 + sg * 64, 452), (230 + sg * 16, 604), (230 + sg * 84, 540), (230 + sg * 108, 456)]
            t.poly(lap, fill=dk(base, 0.88)); t.stroke(lap, LINE, 7)
        if c.get('vest'):
            for y in (640, 690, 740): t.ellipse(230, y, 11, 11, fill=GOLD, outline=LINE, width=5)
        else:
            for y in (668, 736): t.dot(230, y, 10, dk(base, 0.6))
        if c.get('tweed'):
            for k in range(26): t.dot(110 + (k * 53) % 250, 620 + (k * 37) % 170, 5, dk(base, 0.8))
            t.rrect(270, 610, 340, 650, 8, fill=dk(base, 0.86), outline=LINE, width=6); t.stroke([(300, 590), (300, 625)], RED, 9)
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


# ------------------------------------------------------------------ cute props
def eyes2(d, pts, r, mood):
    for x, y in pts:
        d.ellipse(x, y, r, r * 1.12, fill=WHITE, outline=LINE, width=8)
        dy = r * 0.25 if mood == 'sad' else 0
        d.dot(x + r * 0.18, y + dy, r * 0.58, LINE); d.dot(x + r * 0.32, y - r * 0.2 + dy, r * 0.2, WHITE)
        if mood == 'shocked': d.ellipse(x, y, r, r * 1.12, fill=WHITE, outline=LINE, width=8); d.dot(x, y, r * 0.3, LINE)
        if mood == 'sad': d.stroke([(x - r, y - r * 1.5), (x + r, y - r * 1.2 - (r * 0.5 if x == pts[0][0] else 0))], LINE, 8)


def jet(st):                                                 # Falcon 20 freighter, nose right, a face on the nose
    d = Draw(1400, 620)
    if st == 'fly':
        for y, x0 in ((210, 10), (300, 50), (390, 20)): d.stroke([(x0, y), (x0 + 130, y)], LINE, 24); d.stroke([(x0 + 4, y), (x0 + 126, y)], WHITE, 11)
    d.poly([(600, 330), (780, 330), (560, 520), (440, 520)], fill=dk(SILVER, 0.86), outline=LINE, width=14)          # far wing
    if st != 'fly':
        for x in (640, 1180): d.stroke([(x, 360), (x, 520)], LINE, 20); d.ellipse(x, 540, 44, 44, fill=(46, 44, 52, 255), outline=LINE, width=12); d.dot(x, 540, 16, SILVER)
    fus = bez((160, 250), (500, 196), (1000, 190), (1250, 236)) + bez((1250, 236), (1350, 270), (1350, 340), (1250, 366)) + bez((1250, 366), (1000, 400), (500, 392), (160, 328))
    m = Draw(1400, 620); m.poly(fus, fill=WHITE); d.poly(fus, fill=WHITE)
    t = Draw(1400, 620); t.rect(0, 0, 1400, 262, PURP); t.rect(0, 352, 1400, 420, (226, 230, 238, 255)); d.clip(t, m)
    d.poly(fus, outline=LINE, width=16)
    d.poly([(170, 262), (96, 50), (196, 50), (340, 252)], fill=PURP, outline=LINE, width=14); d.poly([(130, 120), (190, 120), (214, 160), (146, 160)], fill=ORNG)
    d.rrect(30, 34, 250, 70, 16, fill=PURP, outline=LINE, width=12)
    d.rrect(250, 232, 450, 316, 40, fill=SILVER, outline=LINE, width=14); d.ellipse(450, 274, 20, 40, fill=(70, 72, 84, 255), outline=LINE, width=8)
    for x in range(560, 961, 80): d.rrect(x - 20, 266, x + 20, 300, 12, fill=GLASS, outline=LINE, width=7)
    d.text(760, 330, 'FEDERAL EXPRESS', 40, PURP)
    d.poly([(1100, 228), (1214, 230), (1262, 262), (1110, 262)], fill=GLASS, outline=LINE, width=10)
    eyes2(d, [(1136, 300), (1232, 300)], 40, st)
    for x in (1110, 1270): d.ellipse(x, 342, 22, 12, fill=BLUSH)
    if st == 'sad': d.arc(1190, 372, 30, 18, 200, 340, LINE, 9); G.sweat(d, 1290, 250)
    else: d.chord(1190, 344, 34, 26, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=8)
    d.poly([(680, 340), (900, 340), (700, 470), (560, 470)], fill=SILVER, outline=LINE, width=14)                   # near wing
    return d.out()


def parcel(st):                                              # cardboard box with a face, tape and a label
    d = Draw(520, 520); top = [(70, 150), (300, 90), (460, 150), (230, 210)]
    d.poly([(70, 150), (230, 210), (230, 480), (70, 410)], fill=dk(CARD_BOX, 0.84), outline=LINE, width=12)
    d.poly([(230, 210), (460, 150), (460, 400), (230, 480)], fill=CARD_BOX, outline=LINE, width=12)
    d.poly(top, fill=(226, 178, 120, 255), outline=LINE, width=12); d.stroke([(185, 120), (345, 180)], (240, 214, 160, 255), 22)
    d.poly([(300, 330), (420, 296), (420, 360), (300, 394)], fill=WHITE, outline=LINE, width=6); d.stroke([(316, 350), (400, 326)], PURP, 8)
    eyes2(d, [(120, 290), (190, 314)], 26, st)
    for x, y in ((100, 350), (210, 386)): d.ellipse(x, y, 18, 10, fill=BLUSH)
    if st == 'shocked': d.ellipse(156, 380, 16, 20, fill=(124, 40, 62, 255), outline=LINE, width=6)
    else: d.chord(156, 362, 26, 22, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=6)
    if st == 'cheer':
        for x0, sg in ((70, -1), (460, 1)): d.stroke([(x0, 260), (x0 + sg * 50, 170)], LINE, 14)
    return d.out()


def suit_mark(d, x, y, s, kind, col):
    if kind == 'heart':
        d.dot(x - 0.5 * s, y - 0.25 * s, 0.55 * s, col); d.dot(x + 0.5 * s, y - 0.25 * s, 0.55 * s, col); d.poly([(x - 1.02 * s, y - 0.05 * s), (x + 1.02 * s, y - 0.05 * s), (x, y + 1.2 * s)], fill=col)
    else:
        d.dot(x - 0.5 * s, y + 0.25 * s, 0.55 * s, col); d.dot(x + 0.5 * s, y + 0.25 * s, 0.55 * s, col); d.poly([(x - 1.02 * s, y + 0.05 * s), (x + 1.02 * s, y + 0.05 * s), (x, y - 1.2 * s)], fill=col)
        d.poly([(x, y + 0.3 * s), (x - 0.4 * s, y + 1.2 * s), (x + 0.4 * s, y + 1.2 * s)], fill=col)


def pcard(rank, kind):
    d = Draw(380, 520); d.rrect(12, 12, 368, 508, 30, fill=WHITE, outline=LINE, width=14)
    if rank is None:                                         # card back
        d.rrect(40, 40, 340, 480, 18, fill=(196, 48, 64, 255)); d.rrect(60, 60, 320, 460, 12, outline=(255, 230, 230, 255), width=6)
        for k in range(-6, 7): d.stroke([(60 + max(0, k) * 40, 60 + max(0, -k) * 40), (320 - max(0, -k) * 40, 460 - max(0, k) * 40)], (230, 110, 120, 255), 5)
        return d.out()
    col = RED if kind == 'heart' else LINE
    d.text(80, 86, rank, 76, col); suit_mark(d, 80, 160, 24, kind, col); suit_mark(d, 190, 280, 74, kind, col)
    if rank == 'K': d.text(190, 410, 'KING', 46, col)
    return d.out()


def chips(big):
    d = Draw(560, 560); cols = (RED, BLUE, GREEN, PURP, GOLD)
    for i, (x, n) in enumerate(((150, 6 if big else 3), (290, 9 if big else 4), (420, 5 if big else 2))):
        for k in range(n):
            y = 480 - k * 34; c = cols[(i + k) % 5]
            d.ellipse(x, y, 92, 36, fill=dk(c, 0.75), outline=LINE, width=8); d.ellipse(x, y - 10, 92, 34, fill=c, outline=LINE, width=8)
            d.ellipse(x, y - 10, 56, 20, outline=WHITE, width=6)
    return d.out()


def jar(full):
    d = Draw(460, 560); d.rrect(70, 120, 390, 530, 70, fill=(214, 236, 246, 160), outline=LINE, width=14)
    if full:
        for k in range(7): d.rrect(100 + (k % 3) * 80, 470 - k * 52, 220 + (k % 3) * 80, 512 - k * 52, 8, fill=CASH, outline=LINE, width=6)
    else: d.rrect(150, 486, 270, 512, 8, fill=CASH, outline=LINE, width=6)
    d.rrect(100, 70, 360, 130, 16, fill=(186, 140, 92, 255), outline=LINE, width=12); d.stroke([(110, 220), (110, 420)], WHITE, 14)
    d.rrect(150, 250, 310, 330, 12, fill=CREAM, outline=LINE, width=8); d.text(230, 292, 'CASH', 46, LINE); return d.out()


def bill():
    d = Draw(420, 220); d.rrect(12, 12, 408, 208, 18, fill=CASH, outline=LINE, width=12); d.rrect(36, 36, 384, 184, 10, outline=(214, 240, 200, 255), width=6)
    d.ellipse(210, 110, 56, 56, fill=(200, 232, 184, 255), outline=LINE, width=7); d.text(210, 112, '$', 70, (40, 110, 60, 255)); return d.out()


def lifebuoy():
    d = Draw(560, 560)
    for k in range(8):
        d.poly([(280, 280)] + [(280 + 240 * math.cos(math.radians(a)), 280 + 240 * math.sin(math.radians(a))) for a in np.linspace(k * 45, k * 45 + 45, 12)], fill=RED if k % 2 == 0 else WHITE)
    d.ellipse(280, 280, 240, 240, outline=LINE, width=16); d.ellipse(280, 280, 112, 112, fill=(0, 0, 0, 0), outline=LINE, width=16)
    m = Draw(560, 560); m.dot(280, 280, 104, WHITE); im = d.out(); hole = m.out().split()[3]; a = im.split()[3]
    a = Image.fromarray(np.where(np.array(hole) > 0, 0, np.array(a)).astype(np.uint8)); im.putalpha(a)
    d2 = Draw(560, 560); d2.ellipse(280, 280, 112, 112, outline=LINE, width=16); im.alpha_composite(d2.out())
    d3 = Draw(560, 560); d3.text(280, 64, 'LIFELINE', 1, LINE); return im


def moneybag():
    d = Draw(560, 600); d.poly(bez((180, 150), (40, 300), (40, 560), (280, 570)) + bez((280, 570), (520, 560), (520, 300), (380, 150)), fill=(196, 160, 104, 255), outline=LINE, width=14)
    d.poly([(200, 150), (360, 150), (420, 60), (140, 60)], fill=(196, 160, 104, 255), outline=LINE, width=14); d.rrect(170, 136, 390, 172, 14, fill=RED, outline=LINE, width=10)
    d.text(280, 380, '$11M', 120, (40, 120, 64, 255), stroke=7, stroke_fill=LINE); return d.out()


def paper(graded):
    d = Draw(640, 800); d.rrect(20, 20, 620, 780, 18, fill=(252, 250, 242, 255), outline=LINE, width=14)
    d.text(320, 100, 'TERM PAPER', 54, LINE); d.text(320, 166, 'Overnight delivery', 34, (90, 90, 110, 255))
    hx, hy = 320, 400                                                    # hub-and-spoke doodle
    for k in range(8): a = k * math.pi / 4; d.stroke([(hx, hy), (hx + 170 * math.cos(a), hy + 120 * math.sin(a))], BLUE, 8); d.dot(hx + 170 * math.cos(a), hy + 120 * math.sin(a), 16, BLUE)
    d.dot(hx, hy, 34, ORNG); d.ellipse(hx, hy, 34, 34, outline=LINE, width=7)
    for y in (580, 630, 680): d.stroke([(80, y), (560, y)], (186, 190, 204, 255), 10)
    d.text(160, 734, 'F. Smith', 40, (60, 60, 90, 255))
    if graded: d.ellipse(486, 640, 116, 116, outline=(214, 40, 48, 255), width=16); d.text(486, 640, 'C', 190, (214, 40, 48, 255))
    return d.out()


def book():
    d = Draw(620, 700); d.rrect(60, 40, 580, 660, 22, fill=(46, 92, 160, 255), outline=LINE, width=14); d.rect(70, 50, 120, 650, (30, 66, 120, 255))
    d.text(345, 210, 'BUSINESS', 66, WHITE, stroke=4, stroke_fill=LINE); d.text(345, 300, 'SCHOOL', 66, WHITE, stroke=4, stroke_fill=LINE)
    d.text(345, 430, '101', 120, GOLD, stroke=6, stroke_fill=LINE); return d.out()


def fuel():
    d = G.card(760, 560); d.text(380, 92, 'FUEL COSTS', 74, LINE)
    pts = [(90, 470), (220, 430), (330, 440), (450, 330), (560, 270), (660, 150)]
    d.stroke([(80, 160), (80, 490), (690, 490)], LINE, 8); d.stroke(pts, RED, 22); d.poly([(700, 110), (612, 136), (672, 196)], fill=RED, outline=LINE, width=6)
    d.text(560, 420, '$$$', 86, (40, 120, 64, 255), stroke=5, stroke_fill=LINE); return d.out()


def cmp_card():
    d = G.card(880, 560)
    for x, big, small, col in ((230, '14', 'JETS', PURP), (650, '186', 'PARCELS', ORNG)):
        d.text(x, 220, big, 190, col, stroke=8, stroke_fill=LINE); d.text(x, 380, small, 64, LINE)
    d.text(440, 220, 'vs', 70, LINE); d.text(440, 490, '= 13 EACH!', 60, RED); return d.out()


def counter(won):
    d = G.card(880, 400); d.text(440, 92, 'BANKROLL', 60, LINE)
    d.text(440, 250, '$27,000' if won else '$5,000', 170, (40, 130, 70, 255) if won else RED, stroke=8, stroke_fill=LINE); return d.out()


def pulse():
    d = Draw(900, 300); d.rrect(14, 14, 886, 286, 30, fill=GREEN, outline=LINE, width=14)
    d.stroke([(50, 190), (180, 190), (220, 110), (260, 250), (300, 150), (330, 190), (380, 190)], WHITE, 14)
    d.text(630, 160, 'ALIVE!', 120, WHITE, stroke=7, stroke_fill=LINE); return d.out()


def crown():
    d = G.card(900, 560); pts = [(250, 300), (230, 120), (340, 210), (450, 80), (560, 210), (670, 120), (650, 300)]
    d.poly(pts, fill=GOLD, outline=LINE, width=14)
    for x, y in ((230, 120), (450, 80), (670, 120)): d.dot(x, y, 22, RED)
    d.text(450, 400, "WORLD'S #1", 96, PURP, stroke=6, stroke_fill=LINE); d.text(450, 492, 'CARGO AIRLINE', 56, LINE); return d.out()


# ------------------------------------------------------------------ set dressing (props/, textures/, bg/)
def neon(path):
    W, Hh = 1600, 640; base = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); d = Draw(W, Hh)
    d.rrect(20, 20, W - 20, Hh - 20, 60, fill=(64, 40, 96, 255), outline=LINE, width=18)
    g = Draw(W, Hh); g.text(W / 2, 230, 'LAS VEGAS', 200, (255, 90, 200, 255)); g.text(W / 2, 470, 'CASINO', 150, (90, 230, 255, 255))
    for k in range(9): g.ellipse(170 + k * 158, 590, 18, 18, outline=(255, 220, 90, 255), width=8)
    glow = g.out().filter(ImageFilter.GaussianBlur(26)); im = d.out(); im.alpha_composite(glow); im.alpha_composite(glow)
    t = Draw(W, Hh); t.text(W / 2, 230, 'LAS VEGAS', 200, (255, 214, 246, 255)); t.text(W / 2, 470, 'CASINO', 150, (214, 250, 255, 255))
    for k in range(9): t.dot(170 + k * 158, 590, 12, (255, 240, 170, 255))
    im.alpha_composite(t.out()); im.save(path)


def slot(path):
    d = Draw(600, 1000); d.rrect(40, 120, 560, 980, 50, fill=(204, 52, 70, 255), outline=LINE, width=16)
    d.chord(300, 140, 260, 120, 180, 360, fill=GOLD, outline=LINE, width=16); d.text(300, 90, 'JACKPOT', 56, RED)
    d.rrect(90, 260, 510, 520, 24, fill=(60, 40, 70, 255), outline=LINE, width=12)
    for k, x in enumerate((160, 300, 440)): d.rrect(x - 60, 290, x + 60, 490, 14, fill=WHITE, outline=LINE, width=8); d.text(x, 392, '7', 120, RED, stroke=5, stroke_fill=LINE)
    d.rrect(110, 600, 490, 700, 16, fill=(250, 224, 120, 255), outline=LINE, width=10); d.rrect(150, 800, 450, 900, 20, fill=(160, 36, 52, 255), outline=LINE, width=10)
    d.stroke([(560, 380), (590, 380), (590, 220)], SILVER, 22); d.dot(590, 200, 34, RED); d.out().save(path)


def mapwall(path):                                           # hub-and-spoke map of 25 US cities, Memphis in the middle
    W, Hh = 1800, 1100; d = Draw(W, Hh); d.rrect(10, 10, W - 10, Hh - 10, 40, fill=(70, 118, 178, 255), outline=LINE, width=20)
    US = [(150, 180), (120, 360), (170, 560), (260, 700), (520, 770), (700, 790), (830, 900), (930, 830), (1100, 800), (1250, 820), (1330, 960), (1400, 950),
          (1380, 800), (1500, 700), (1580, 520), (1660, 340), (1700, 220), (1600, 200), (1480, 300), (1360, 260), (1230, 300), (1150, 220), (980, 200), (600, 180)]
    d.poly(US, fill=(126, 196, 120, 255), outline=LINE, width=14)
    hub = (1060, 560); R_ = np.random.RandomState(4); cities = []
    while len(cities) < 25:
        x, y = R_.uniform(200, 1640), R_.uniform(230, 780)
        if all(math.hypot(x - a, y - b) > 120 for a, b in cities + [hub]): cities.append((x, y))
    cities[0] = (330, 520)                                   # Las Vegas
    for c in cities: d.stroke([hub, c], (255, 214, 120, 255), 6)
    for c in cities: d.dot(c[0], c[1], 20, WHITE); d.ellipse(c[0], c[1], 20, 20, outline=LINE, width=6)
    d.dot(hub[0], hub[1], 44, ORNG); d.ellipse(hub[0], hub[1], 44, 44, outline=LINE, width=10); d.text(hub[0], hub[1] + 86, 'MEMPHIS', 54, WHITE, stroke=5, stroke_fill=LINE)
    d.text(330, 600, 'LAS VEGAS', 46, WHITE, stroke=5, stroke_fill=LINE); d.text(W / 2, 1010, 'FEDERAL EXPRESS NETWORK 1973', 56, WHITE, stroke=5, stroke_fill=LINE)
    d.out().save(path)


def chalk(path):
    d = Draw(1800, 900); d.rrect(10, 10, 1790, 890, 24, fill=(168, 116, 70, 255), outline=LINE, width=16); d.rect(60, 60, 1740, 840, (58, 112, 86, 255))
    C_ = (236, 242, 236, 255); d.text(560, 170, 'HUB & SPOKE', 120, C_); hx, hy = 1340, 470
    for k in range(10): a = k * math.pi / 5; d.stroke([(hx, hy), (hx + 260 * math.cos(a), hy + 220 * math.sin(a))], C_, 9); d.ellipse(hx + 260 * math.cos(a), hy + 220 * math.sin(a), 24, 24, outline=C_, width=7)
    d.ellipse(hx, hy, 52, 52, outline=C_, width=10)
    for y, s in ((360, 'ALL PARCELS FLY TO'), (450, 'ONE HUB AT NIGHT,'), (540, 'THEN OUT AGAIN'), (630, 'BY MORNING.')): d.text(460, y, s, 64, C_)
    d.rect(120, 820, 420, 840, (250, 250, 250, 255)); d.out().save(path)


def pennant(path):
    d = Draw(1000, 440); d.poly([(40, 30), (40, 410), (960, 220)], fill=(20, 60, 140, 255), outline=LINE, width=14)
    d.rect(20, 20, 60, 420, (240, 240, 240, 255)); d.text(370, 220, 'YALE', 150, WHITE, stroke=6, stroke_fill=LINE); d.out().save(path)


def billboard(path):                                         # cork board of unpaid bills
    d = Draw(1200, 800); d.rrect(10, 10, 1190, 790, 24, fill=(196, 150, 100, 255), outline=LINE, width=16)
    R_ = np.random.RandomState(2)
    for k, (x, y) in enumerate(((220, 230), (520, 200), (820, 250), (1010, 210), (300, 540), (620, 560), (900, 560))):
        w, h = 230, 280; d.rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, (250, 248, 238, 255)); d.rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 6, outline=LINE, width=6)
        d.text(x, y - 80, ('FUEL', 'RENT', 'FUEL', 'PARTS', 'FUEL', 'PAYROLL', 'FUEL')[k], 44, LINE)
        for j in range(3): d.stroke([(x - 80, y - 20 + j * 34), (x + 80, y - 20 + j * 34)], (180, 184, 196, 255), 8)
        d.text(x, y + 100, 'DUE', 52, RED); d.dot(x, y - h / 2 + 14, 14, RED)
    d.out().save(path)


def carpet(path, n=512):                                     # casino carpet: deep red with gold diamonds
    im = Image.new('RGB', (n, n), (150, 40, 58)); dr = ImageDraw.Draw(im); s = n // 4
    for i in range(5):
        for j in range(5):
            cx, cy = i * s, j * s; dr.polygon([(cx, cy - 40), (cx + 40, cy), (cx, cy + 40), (cx - 40, cy)], outline=(232, 184, 80), fill=(176, 56, 72))
            dr.ellipse([cx + s / 2 - 10, cy + s / 2 - 10, cx + s / 2 + 10, cy + s / 2 + 10], fill=(232, 184, 80))
    im.save(path, quality=92)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'nervous')]
    multi = dict(jet={s: jet(s) for s in ('default', 'fly', 'sad')}, parcel={s: parcel(s) for s in ('default', 'shocked', 'cheer')},
                 cardA={'default': pcard(None, ''), 'up': pcard('A', 'spade')}, cardK={'default': pcard(None, ''), 'up': pcard('K', 'heart')},
                 jar={'default': jar(True), 'empty': jar(False)}, paper={'default': paper(False), 'graded': paper(True)},
                 money={'default': counter(False), 'won': counter(True)}, chips={'default': chips(False), 'big': chips(True)})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    B.sparkle(Pp('sparkle.png'))
    cards = dict(bill=bill(), buoy=lifebuoy(), bag=moneybag(), book=book(), fuel=fuel(), cmp=cmp_card(), alive=pulse(), crown=crown(),
                 num1=V.wtag("WORLD'S #1 CARGO AIRLINE", 1240, PURP, 70), last=V.wtag('LAST $5,000!', 820, RED, 88), bj=B.sticker_burst('21!'),
                 cal=G.cal_card('APRIL', '1973', ''), jets14=V.wtag('14 FALCON JETS', 960, PURP, 80), mem=V.wtag('MEMPHIS', 640, ORNG, 92),
                 n186=V.big_card('186', 'PACKAGES', ORNG, 700), n25=V.big_card('25', 'CITIES', BLUE, 640), cash5=CA.stamp('$5,000 LEFT', 820, 104),
                 notenough=V.wtag('NOT ENOUGH!', 780, RED, 84), fred=V.wtag('FRED SMITH', 760, BLUE, 84), founder=V.wtag('FOUNDER', 520, ORNG, 70),
                 never=CA.stamp('NEVER TAUGHT!', 900, 96), vegas=V.wtag('LAS VEGAS!', 700, (214, 60, 160, 255), 88), paid=CA.stamp('PAID!', 520, 120),
                 nostrat=CA.stamp('NOT A STRATEGY', 940, 88), flying=V.wtag('JETS FLYING!', 820, GREEN, 82), yale=V.wtag('YALE', 460, (20, 60, 140, 255), 96),
                 avg=V.wtag('AVERAGE!', 640, (130, 136, 150, 255), 92), saved=V.wtag('SAVED BY A CARD GAME', 1180, RED, 72), back=V.wtag('INVESTORS ARE BACK!', 1160, GREEN, 70),
                 ques=B.sticker_mark('?', GOLD), poof=B.sticker_poof(), hearts=G.hearts(), sparkle=Image.open(Pp('sparkle.png')).convert('RGBA'))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); G.tex_asphalt(T('asphalt.jpg')); carpet(T('carpet.jpg'))
    G.sky(os.path.join(ROOT, 'bg', 'sky73.jpg'))
    neon(Pp('neon.png')); slot(Pp('slot.png')); mapwall(Pp('map.png')); chalk(Pp('chalk.png')); pennant(Pp('pennant.png')); billboard(Pp('bills.png'))
    VA.skyplane(Pp('skymem.png'), (88, 70, 150), (252, 168, 112)); VA.skyplane(Pp('skyday.png'), (92, 150, 226), (226, 240, 252))
    B.window(Pp('window.png'))
    for n in ('neon', 'slot', 'map', 'chalk', 'pennant', 'bills', 'skymem', 'skyday'): items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
