#!/usr/bin/env python3
"""Assets for video 10 (GTA 6 launch: Nov 19 / Nov 18, two delays, no disc, the midnight wave), drawn in code.
New cute cast: Kiwi gamer (backwards cap + headset, purple hoodie), store clerk (hair bun, red vest), Londoner (bowler hat,
tweed), sleepy New Yorker (nightcap, striped pyjamas).  Hero prop: the GTA 6 game box (closed / opened with no disc).
Props: calendar pages, download-code card, signs.  Sets: NZ gamer room at night (TV, clock at 12, world-map poster),
game store, delay billboard in town, London street at 11 a.m. (clock tower), New York at 6 a.m. dawn.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import viking_assets as V
import vasa_assets as VA
import corrigan_assets as CA
import catseyes_assets as CE
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN, BLUE = G.RED, G.GOLD, G.GREEN, VA.BLUE
dk, SK, eyes2, glow, btag, tiles = VA.dk, VA.SK, CE.eyes2, CE.glow, CE.btag, CE.tiles
PURP, TEAL, PINK, ORNG, NAVY2 = (122, 84, 200, 255), (40, 170, 170, 255), (240, 96, 150, 255), (250, 150, 60, 255), (34, 40, 84, 255)
NEW = {
    'kiwi': dict(sk=1, style='bcap', hair=(70, 46, 36, 255), hc=TEAL, suit=PURP, shade=(96, 64, 168, 255), body='hoodie', freck=1),
    'shopgirl': dict(sk=2, style='bun', hair=(36, 28, 34, 255), suit=(246, 244, 238, 255), shade=(214, 212, 206, 255), body='vest'),
    'londoner': dict(sk=0, style='bowler', hair=(196, 112, 60, 255), hc=(52, 48, 54, 255), suit=(150, 112, 78, 255), shade=(124, 90, 60, 255), body='tweed',
                     stache=(176, 96, 52, 255)),
    'nyer': dict(sk=1, style='nightcap', hair=(150, 104, 70, 255), hc=(80, 130, 210, 255), suit=(150, 190, 236, 255), shade=(120, 160, 210, 255), body='pjs'),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; st, hr = c['style'], c.get('hair')
    skin, sh = SK[c['sk']]; hc = c.get('hc')
    if st == 'bun': d.ellipse(cx, 70, 74, 66, fill=hr, outline=LINE, width=lw); d.rrect(cx - 60, 118, cx + 60, 142, 10, fill=RED, outline=LINE, width=8)
    if st == 'bcap':                                         # headset band behind the head
        d.arc(cx, cy, R + 22, R + 22, 196, 344, LINE, 34); d.arc(cx, cy, R + 22, R + 22, 196, 344, (60, 60, 72, 255), 20)
    d.ellipse(cx, cy, R, R, fill=skin, outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, sh, skin)
    d.chord(cx, cy - 66, R + 8, 132, 180, 360, fill=hr, outline=LINE, width=lw)
    if st == 'bcap':                                         # backwards cap, brim at the back-left, tuft of hair under the strap
        d.chord(cx + 6, 150, R + 4, 140, 180, 360, fill=hc, outline=LINE, width=lw); d.stroke(bez((cx - 30, 16), (cx - 20, 60), (cx - 10, 110), (cx, 150)), dk(hc, 0.8), 8)
        d.poly([(cx + 150, 136), (cx + 228, 104), (cx + 226, 150), (cx + 160, 160)], fill=dk(hc, 0.85), outline=LINE, width=12)
        d.dot(cx, 20, 16, dk(hc, 0.8)); d.rrect(cx - 172, 132, cx - 120, 160, 8, fill=GOLD, outline=LINE, width=6)
        for sg in (-1, 1): d.rrect(cx + sg * 208 - 30, cy - 50, cx + sg * 208 + 30, cy + 70, 26, fill=(60, 60, 72, 255), outline=LINE, width=12)
        d.rrect(cx + 178, cy + 0, cx + 238, cy + 30, 10, fill=PINK)
        d.stroke(bez((cx - 200, cy + 60), (cx - 210, cy + 130), (cx - 150, cy + 150), (cx - 96, cy + 136)), LINE, 12); d.dot(cx - 92, cy + 136, 16, (60, 60, 72, 255))
    elif st == 'bun':
        for sg in (-1, 1): d.ellipse(cx + sg * 160, cy - 40, 50, 70, fill=hr, outline=LINE, width=10)
    elif st == 'bowler':                                     # black bowler hat
        d.ellipse(cx, 128, 236, 38, fill=dk(hc, 0.9), outline=LINE, width=lw); d.chord(cx, 128, 156, 126, 180, 360, fill=hc, outline=LINE, width=lw)
        d.rect(cx - 148, 98, cx + 148, 120, (150, 40, 50, 255)); d.ellipse(cx - 60, 50, 40, 16, fill=(255, 255, 255, 70))
    elif st == 'nightcap':                                   # floppy striped nightcap with a pom-pom
        d.poly(bez((cx - 196, 150), (cx - 170, 10), (cx + 120, -20), (cx + 196, 210)) + [(cx + 170, 220), (cx + 110, 140)], fill=hc, outline=LINE, width=lw)
        for k in range(3): d.stroke(bez((cx - 150 + k * 90, 140), (cx - 120 + k * 90, 80), (cx - 80 + k * 80, 40), (cx - 60 + k * 80, 20)), WHITE, 14)
        d.rrect(cx - 200, 120, cx + 120, 166, 22, fill=WHITE, outline=LINE, width=10); d.dot(cx + 192, 220, 34, WHITE); d.ellipse(cx + 192, 220, 34, 34, outline=LINE, width=8)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 30, 17, fill=BLUSH)
    if c.get('freck'):
        for sg in (-1, 1):
            for dx, dy in ((-14, 0), (8, -10), (10, 12)): d.dot(cx + sg * 108 + dx, cy + 12 + dy, 5, (196, 120, 90, 255))
    B.eyes(d, L, Rr, expr, skin); B.brows(d, L, Rr, expr, ey - 50)
    my = cy + 74
    if c.get('stache'):
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 34, my - 52), (cx + sg * 62, my - 40), (cx + sg * 80, my - 64)), c['stache'], 22)
        my += 12
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']; base = c['suit']; bs = c['body']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=base)
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=base); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if bs == 'hoodie':                                       # hood collar, drawstrings, kangaroo pocket, pixel heart
        t.chord(230, 452, 120, 56, 0, 180, fill=dk(base, 0.8)); t.stroke([(206, 470), (200, 590)], WHITE, 9); t.stroke([(254, 470), (260, 590)], WHITE, 9)
        t.rrect(130, 640, 330, 760, 30, fill=dk(base, 0.88), outline=LINE, width=7)
        for (px, py) in ((-1, 0), (1, 0), (-2, -1), (-1, -1), (1, -1), (2, -1), (-2, 0), (2, 0), (0, 1), (-1, 1), (1, 1), (0, 2), (0, 0)):
            t.rect(230 + px * 14 - 7, 560 + py * 14 - 7, 230 + px * 14 + 7, 560 + py * 14 + 7, PINK)
    elif bs == 'vest':                                       # white shirt, red vest, name badge
        for sg in (-1, 1): t.poly([(230 + sg * 30, 452), (230 + sg * 160, 470), (230 + sg * 160, 800), (230 + sg * 30, 800), (230 + sg * 10, 560)], fill=(206, 50, 60, 255), outline=LINE, width=8)
        t.rrect(276, 560, 350, 600, 8, fill=WHITE, outline=LINE, width=6); t.text(313, 580, 'STAFF', 20, LINE)
        for y in (620, 690, 760): t.dot(230, y, 8, GOLD)
    elif bs == 'tweed':                                      # tweed jacket, white shirt, red tie, pocket square
        t.poly([(176, 452), (284, 452), (230, 600)], fill=WHITE); t.poly([(222, 470), (238, 470), (246, 590), (230, 610), (214, 590)], fill=RED, outline=LINE, width=6)
        for x in range(100, 370, 30): t.stroke([(x, 460), (x, 800)], dk(base, 0.9), 4)
        t.poly([(300, 560), (340, 560), (330, 590), (310, 590)], fill=(240, 220, 120, 255), outline=LINE, width=5)
    elif bs == 'pjs':                                        # striped pyjamas, collar, buttons
        for x in range(100, 370, 44): t.rect(x, 452, x + 16, 800, (255, 255, 255, 170))
        for sg in (-1, 1): t.poly([(230, 470), (230 + sg * 80, 452), (230 + sg * 70, 520)], fill=WHITE, outline=LINE, width=6)
        for y in (560, 630, 700, 770): t.dot(230, y, 9, (60, 90, 160, 255))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


# ------------------------------------------------------------------ hero prop and cards
def coverart(w, h, title=True):                                          # sunset, retro sun, palms, ocean, title
    im = CA.gradient((122, 70, 190), (255, 170, 90), w, h, 1.1).convert('RGBA'); d = Draw(w, h)
    sx, sy, sr = w * 0.5, h * 0.52, w * 0.3; d.dot(sx, sy, sr, (255, 214, 110, 255))
    for k in range(5): y = sy + sr * (0.15 + k * 0.17); d.rect(sx - sr, y, sx + sr, y + 10 + k * 5, (240, 120, 120, 255))
    d.rect(0, h * 0.72, w, h, (60, 70, 150, 255))
    for k in range(6): d.stroke([(w * 0.1 + k * w * 0.15, h * (0.78 + 0.03 * (k % 3))), (w * 0.2 + k * w * 0.15, h * (0.78 + 0.03 * (k % 3)))], (150, 160, 240, 255), 8)
    for px, s in ((0.14, 1.0), (0.86, 0.85)):                # palm silhouettes
        x0, y0 = w * px, h * 0.74; tx, ty = x0 + w * 0.04 * (1 if px < 0.5 else -1), h * (0.36 + 0.08 * (1 - s))
        d.stroke(bez((x0, y0), (x0, y0 - h * 0.15), (tx, ty + h * 0.1), (tx, ty)), (40, 26, 60, 255), int(w * 0.03 * s))
        for a in (-150, -110, -60, -20, 20):
            ex, ey = tx + math.cos(math.radians(a)) * w * 0.17 * s, ty + math.sin(math.radians(a)) * w * 0.17 * s + h * 0.05
            d.stroke(bez((tx, ty), ((tx + ex) / 2, ty - h * 0.04), (ex, ey - h * 0.02), (ex, ey)), (40, 26, 60, 255), int(w * 0.022 * s))
    if title: d.text(w * 0.5, h * 0.24, 'GTA 6', int(w * 0.25), WHITE, stroke=max(6, int(w * 0.014)), stroke_fill=LINE)
    im.alpha_composite(d.out()); return im


def gbox(opened=False):                                      # game case on a 1600x1200 canvas (both faces the same size)
    W_, H_ = 1600, 1200; d = Draw(W_, H_)
    if not opened:
        x0, y0, x1, y1 = 330, 40, 1270, 1160; d.rrect(x0, y0, x1, y1, 40, fill=(30, 36, 70, 255), outline=LINE, width=18)
        d.rrect(x0 + 10, y0 + 14, x1 - 10, y0 + 120, 26, fill=(44, 92, 196, 255)); im = d.out()
        art = coverart(x1 - x0 - 60, y1 - y0 - 190); im.alpha_composite(art, (x0 + 30, y0 + 150))
        g = Draw(W_, H_); g.poly([(x0 + 60, y0 + 150), (x0 + 300, y0 + 150), (x0 + 60, y0 + 560)], fill=(255, 255, 255, 70))
        g.rrect(x0 + 30, y0 + 150, x1 - 30, y1 - 40, 16, outline=LINE, width=10); im.alpha_composite(g.out()); return im
    d.rrect(40, 120, 790, 1120, 36, fill=(30, 36, 70, 255), outline=LINE, width=18); d.rrect(810, 120, 1560, 1120, 36, fill=(30, 36, 70, 255), outline=LINE, width=18)
    d.rrect(860, 170, 1510, 1070, 24, fill=(214, 218, 230, 255), outline=LINE, width=10)
    for k in range(18): a0 = k * 20; d.arc(1185, 560, 260, 260, a0, a0 + 11, (120, 124, 140, 255), 12)      # dashed empty disc ring
    d.dot(1185, 560, 60, (180, 184, 196, 255)); d.ellipse(1185, 560, 60, 60, outline=LINE, width=8)
    d.rrect(940, 860, 1430, 1030, 18, fill=(255, 226, 100, 255), outline=LINE, width=10); d.text(1185, 920, 'DOWNLOAD CODE', 46, LINE); d.text(1185, 985, 'XXXX-XXXX', 46, (150, 60, 70, 255))
    d.rrect(100, 180, 730, 1060, 20, fill=(70, 80, 130, 255), outline=LINE, width=10)
    for k in range(5): d.rrect(160, 260 + k * 150, 670, 300 + k * 150, 12, fill=(110, 120, 170, 255))
    im = d.out(); return im


def code():
    d = Draw(1100, 600); d.rrect(20, 20, 1080, 580, 40, fill=(255, 226, 100, 255), outline=LINE, width=18)
    for x in (20, 1080): d.dot(x, 300, 60, (0, 0, 0, 0))
    d.text(550, 130, 'DOWNLOAD CODE', 92, LINE); d.rrect(120, 220, 980, 380, 24, fill=WHITE, outline=LINE, width=10); d.text(550, 300, 'XXXX-XXXX-XXXX', 84, (150, 60, 70, 255))
    d.poly([(470, 420), (630, 420), (630, 470), (700, 470), (550, 570), (400, 470), (470, 470)], fill=BLUE, outline=LINE, width=10); return d.out()


def cal(n):                                                  # calendar page NOVEMBER n
    d = Draw(720, 800); d.rrect(20, 60, 700, 780, 40, fill=WHITE, outline=LINE, width=18); d.rrect(20, 60, 700, 250, 40, fill=RED, outline=LINE, width=18)
    d.rect(38, 200, 682, 250, RED); d.stroke([(20, 250), (700, 250)], LINE, 14); d.text(360, 160, 'NOVEMBER', 96, WHITE, stroke=5, stroke_fill=LINE)
    for x in (200, 520): d.rrect(x - 22, 20, x + 22, 120, 18, fill=(150, 150, 160, 255), outline=LINE, width=10)
    d.text(360, 520, n, 330, LINE); return d.out()


def alarm():                                                 # cute alarm clock at midnight
    d = Draw(760, 800)
    for x in (180, 580): d.dot(x, 130, 90, GOLD); d.ellipse(x, 130, 90, 90, outline=LINE, width=14)
    for x0, x1 in ((240, 160), (520, 600)): d.stroke([(x0, 700), (x1, 780)], LINE, 22)
    d.ellipse(380, 430, 300, 300, fill=(122, 84, 200, 255), outline=LINE, width=18); d.ellipse(380, 430, 240, 240, fill=WHITE, outline=LINE, width=12)
    for k in range(12): a = math.radians(k * 30); d.dot(380 + 200 * math.sin(a), 430 - 200 * math.cos(a), 12 if k % 3 == 0 else 8, LINE)
    d.stroke([(380, 430), (380, 250)], LINE, 22); d.stroke([(380, 430), (380, 300)], RED, 12); d.dot(380, 430, 22, LINE)
    eyes2(d, [(310, 500), (450, 500)], 30, 'calm'); d.chord(380, 570, 40, 30, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=8)
    for x in (280, 480): d.ellipse(x, 560, 26, 14, fill=BLUSH)
    return d.out()


def card2(big, small, col, w, bs=150, ss=62):                # big_card with a size for long words
    d = G.card(w, 420); d.text(w / 2, 170, big, bs, col, stroke=8, stroke_fill=LINE); d.text(w / 2, 326, small, ss, LINE); return d.out()


# ------------------------------------------------------------------ sets
WMAP = [[(0.08, 0.22), (0.30, 0.16), (0.36, 0.30), (0.26, 0.42), (0.20, 0.40), (0.10, 0.32)], [(0.24, 0.48), (0.32, 0.50), (0.30, 0.78), (0.25, 0.80), (0.22, 0.60)],
        [(0.44, 0.18), (0.56, 0.16), (0.58, 0.30), (0.46, 0.32)], [(0.46, 0.36), (0.58, 0.36), (0.60, 0.50), (0.54, 0.72), (0.48, 0.60), (0.44, 0.46)],
        [(0.58, 0.16), (0.88, 0.14), (0.90, 0.32), (0.76, 0.44), (0.64, 0.40), (0.58, 0.30)], [(0.78, 0.62), (0.88, 0.60), (0.90, 0.72), (0.80, 0.74)]]


def worldmap(d, x0, y0, w, h):                               # cute poster map, New Zealand glowing at the right edge
    d.rrect(x0, y0, x0 + w, y0 + h, 16, fill=(120, 190, 230, 255), outline=(236, 220, 180, 255), width=20); d.rrect(x0, y0, x0 + w, y0 + h, 16, outline=LINE, width=8)
    for poly in WMAP: d.poly([(x0 + u * w, y0 + v * h) for u, v in poly], fill=(244, 222, 170, 255), outline=LINE, width=6)
    for k in range(1, 12): d.stroke([(x0 + k * w / 12, y0 + 14), (x0 + k * w / 12, y0 + h - 14)], (255, 255, 255, 90), 4)
    d.poly([(x0 + 0.935 * w, y0 + 0.78 * h), (x0 + 0.955 * w, y0 + 0.76 * h), (x0 + 0.95 * w, y0 + 0.86 * h), (x0 + 0.93 * w, y0 + 0.86 * h)], fill=(255, 230, 90, 255), outline=LINE, width=6)
    d.ellipse(x0 + 0.945 * w, y0 + 0.81 * h, 30, 30, outline=(255, 120, 150, 255), width=8)


def nzroom(path):                                            # night: window with moon, TV with the cover art, clock at 12, world map poster
    W, Hh = 2400, 1100; im = Image.new('RGBA', (W, Hh), (54, 60, 112, 255)); d = Draw(W, Hh)
    for x in range(0, W, 120): d.stroke([(x, 0), (x, Hh)], (60, 66, 120, 255), 6)
    d.rect(0, 0, W, 40, (150, 110, 230, 255)); d.rect(0, 960, W, Hh, (88, 70, 66, 255)); d.stroke([(0, 960), (W, 960)], LINE, 10)
    d.rrect(100, 150, 500, 650, 20, fill=(24, 30, 70, 255), outline=(236, 228, 210, 255), width=26); d.stroke([(300, 150), (300, 650)], (236, 228, 210, 255), 16); d.stroke([(100, 400), (500, 400)], (236, 228, 210, 255), 16)
    d.dot(200, 270, 50, (255, 246, 200, 255)); d.dot(222, 254, 44, (24, 30, 70, 255))
    R_ = np.random.RandomState(3)
    for k in range(14): d.dot(120 + R_.uniform(0, 360), 170 + R_.uniform(0, 460), R_.uniform(3, 7), (255, 250, 220, 255))
    d.rrect(100, 150, 500, 650, 20, outline=LINE, width=8)
    d.rrect(1020, 760, 1720, 960, 16, fill=(110, 80, 60, 255), outline=LINE, width=12); d.rrect(1080, 800, 1660, 920, 10, outline=(80, 56, 44, 255), width=8)
    d.rrect(1040, 300, 1700, 720, 24, fill=(20, 20, 30, 255), outline=LINE, width=16); d.rect(1350, 720, 1390, 760, (40, 40, 50, 255))
    out = d.out(); im.alpha_composite(out); glow(im, 1370, 510, 420, (180, 140, 255, 120), 80)
    art = coverart(620, 380, False); im.alpha_composite(art, (1060, 320))
    d = Draw(W, Hh); d.rrect(1060, 320, 1680, 700, 12, outline=LINE, width=8)
    d.ellipse(1960, 260, 100, 100, fill=WHITE, outline=LINE, width=14)
    for k in range(12): a = math.radians(k * 30); d.dot(1960 + 78 * math.sin(a), 260 - 78 * math.cos(a), 7, LINE)
    d.stroke([(1960, 260), (1960, 190)], LINE, 14); d.stroke([(1960, 260), (1960, 174)], RED, 7); d.dot(1960, 260, 12, LINE)
    worldmap(d, 560, 330, 440, 300)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def store(path):                                             # game store: sign, three shelves of colourful cases
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (238, 216, 186, 255)); d.rect(0, 960, W, Hh, (150, 110, 74, 255))
    d.rrect(900, 60, 1500, 190, 30, fill=(44, 92, 196, 255), outline=LINE, width=14)
    d.rrect(1110, 88, 1290, 162, 36, fill=(255, 226, 110, 255), outline=LINE, width=8); d.rect(1138, 117, 1170, 133, LINE); d.rect(1146, 109, 1162, 141, LINE)
    for x, y in ((1238, 112), (1258, 126), (1238, 140)): d.dot(x, y, 8, RED)
    for x in (1000, 1400): star = [(x + (34 if k % 2 == 0 else 14) * math.cos(math.radians(k * 36 - 90)), 125 + (34 if k % 2 == 0 else 14) * math.sin(math.radians(k * 36 - 90))) for k in range(10)]; d.poly(star, fill=(255, 226, 110, 255), outline=LINE, width=5)
    R_ = np.random.RandomState(8); cols = [PURP, TEAL, PINK, ORNG, BLUE, GREEN, RED, (90, 90, 110, 255)]
    for y in (420, 650, 880):
        d.rect(120, y, 2280, y + 26, (150, 100, 64, 255)); d.stroke([(120, y + 26), (2280, y + 26)], LINE, 8)
        x = 150
        while x < 2240:
            w = R_.randint(70, 96); h = R_.randint(150, 190); c = cols[R_.randint(len(cols))]
            d.rrect(x, y - h, x + w, y, 8, fill=c, outline=LINE, width=6); d.rect(x + 10, y - h + 16, x + w - 10, y - h + 40, (255, 255, 255, 150)); d.dot(x + w / 2, y - h * 0.45, w * 0.22, (255, 236, 160, 255))
            x += w + R_.randint(6, 18)
    d.out().save(path)


def billboard(path):                                         # release-date board: header + big blank calendar grid
    W, Hh = 1800, 1000; d = Draw(W, Hh); d.rrect(20, 20, W - 20, Hh - 20, 30, fill=(250, 244, 230, 255), outline=LINE, width=20)
    d.rrect(20, 20, W - 20, 230, 30, fill=PURP, outline=LINE, width=20); d.rect(40, 180, W - 40, 230, PURP); d.stroke([(20, 230), (W - 20, 230)], LINE, 14)
    for x in (W * 0.3, W * 0.5, W * 0.7): star = [(x + (70 if k % 2 == 0 else 28) * math.cos(math.radians(k * 36 - 90)), 128 + (70 if k % 2 == 0 else 28) * math.sin(math.radians(k * 36 - 90))) for k in range(10)]; d.poly(star, fill=(255, 226, 110, 255), outline=LINE, width=8)
    for i in range(1, 7): d.stroke([(40 + i * (W - 80) / 7, 250), (40 + i * (W - 80) / 7, Hh - 40)], (220, 210, 190, 255), 6)
    for j in range(1, 4): d.stroke([(40, 250 + j * (Hh - 290) / 4), (W - 40, 250 + j * (Hh - 290) / 4)], (220, 210, 190, 255), 6)
    d.out().save(path)


def london(path):                                            # 11 a.m.: brick terrace, clock tower at 11, red phone box, lamp
    W, Hh = 2400, 1050; im = CA.gradient((120, 176, 236), (250, 232, 200), W, Hh, 1.2).convert('RGBA'); glow(im, 2100, 160, 200, (255, 250, 220, 180), 60); d = Draw(W, Hh)
    for x0, w, h, c in ((60, 440, 520, (176, 84, 64, 255)), (520, 420, 600, (196, 150, 110, 255)), (1500, 420, 560, (186, 96, 70, 255)), (1940, 430, 500, (210, 176, 130, 255))):
        d.rect(x0, Hh - 120 - h, x0 + w, Hh - 120, c); d.poly([(x0, Hh - 120 - h), (x0 + w, Hh - 120 - h), (x0 + w, Hh - 120), (x0, Hh - 120)], outline=LINE, width=8)
        for i in range(3):
            for j in range(int(h / 170)): d.rrect(x0 + 50 + i * (w - 100) / 3, Hh - 120 - h + 60 + j * 160, x0 + 50 + i * (w - 100) / 3 + (w - 100) / 3 - 40, Hh - 120 - h + 160 + j * 160, 8, fill=(220, 236, 246, 255), outline=LINE, width=6)
    tx = 1220; d.rect(tx - 130, 200, tx + 130, Hh - 120, (214, 190, 130, 255)); d.poly([(tx - 130, 200), (tx + 130, 200), (tx + 130, Hh - 120), (tx - 130, Hh - 120)], outline=LINE, width=10)
    d.poly([(tx - 150, 200), (tx, 30), (tx + 150, 200)], fill=(90, 100, 120, 255), outline=LINE, width=10); d.dot(tx, 330, 100, (250, 246, 230, 255)); d.ellipse(tx, 330, 100, 100, outline=LINE, width=12)
    for k in range(12): a = math.radians(k * 30); d.dot(tx + 80 * math.sin(a), 330 - 80 * math.cos(a), 7, LINE)
    d.stroke([(tx, 330), (tx, 250)], LINE, 12); d.stroke([(tx, 330), (tx - 52, 300)], LINE, 14); d.dot(tx, 330, 12, LINE)
    for y in range(470, Hh - 160, 120): d.rrect(tx - 60, y, tx + 60, y + 80, 30, fill=(70, 70, 90, 255), outline=LINE, width=6)
    d.rrect(1700, Hh - 420, 1820, Hh - 120, 14, fill=(206, 40, 46, 255), outline=LINE, width=10)
    for i in range(2):
        for j in range(4): d.rect(1716 + i * 50, Hh - 380 + j * 62, 1756 + i * 50, Hh - 330 + j * 62, (220, 236, 246, 255))
    d.rect(0, Hh - 130, W, Hh, (150, 146, 140, 255)); d.stroke([(0, Hh - 130), (W, Hh - 130)], LINE, 8)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def nyc(path):                                               # 6 a.m. dawn: skyline with a few lit windows, water tower, yellow cab
    W, Hh = 2400, 1050; im = CA.gradient((110, 100, 170), (255, 180, 140), W, Hh, 1.0).convert('RGBA'); glow(im, 1300, Hh - 150, 300, (255, 220, 160, 200), 80); d = Draw(W, Hh)
    R_ = np.random.RandomState(9); x = 0
    while x < W:
        w = R_.randint(150, 260); h = R_.randint(340, 820); c = (int(80 + R_.randint(0, 40)), int(70 + R_.randint(0, 30)), int(120 + R_.randint(0, 40)), 255)
        d.rect(x, Hh - 120 - h, x + w, Hh - 120, c); d.poly([(x, Hh - 120 - h), (x + w, Hh - 120 - h), (x + w, Hh - 120), (x, Hh - 120)], outline=LINE, width=7)
        for i in range(int(w / 50)):
            for j in range(int(h / 70)):
                if R_.rand() < 0.22: d.rect(x + 16 + i * 50, Hh - 100 - h + j * 70, x + 40 + i * 50, Hh - 70 - h + j * 70, (255, 226, 140, 255))
        if R_.rand() < 0.3: d.rect(x + w / 2 - 40, Hh - 200 - h, x + w / 2 + 40, Hh - 120 - h, (140, 90, 70, 255)); d.poly([(x + w / 2 - 50, Hh - 200 - h), (x + w / 2, Hh - 250 - h), (x + w / 2 + 50, Hh - 200 - h)], fill=(110, 70, 56, 255), outline=LINE, width=6)
        x += w + R_.randint(0, 30)
    d.rect(0, Hh - 130, W, Hh, (130, 120, 130, 255)); d.stroke([(0, Hh - 130), (W, Hh - 130)], LINE, 8)
    d.rrect(1700, Hh - 230, 2080, Hh - 110, 30, fill=(250, 200, 50, 255), outline=LINE, width=10); d.rrect(1780, Hh - 290, 1990, Hh - 220, 20, fill=(250, 200, 50, 255), outline=LINE, width=10)
    for i in range(8): d.rect(1710 + i * 46, Hh - 190, 1733 + i * 46, Hh - 170, LINE)
    for x in (1780, 2000): d.dot(x, Hh - 110, 40, (46, 44, 52, 255))
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'shouting')]
    multi = dict(gbox={'default': gbox(), 'open': gbox(True)})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    cards = dict(launch19=card2('GTA 6', 'LAUNCHES NOV 19', PURP, 820, 170), first18=card2('NOV 18', 'FIRST PLAYERS', RED, 760),
                 cal18=cal('18'), cal19=cal('19'), codecard=code(),
                 fall25=V.wtag('FALL 2025', 760, BLUE, 96), may26=V.wtag('MAY 26, 2026', 900, BLUE, 88), nov19=V.wtag('NOV 19', 640, GREEN, 100),
                 delayed=CA.stamp('DELAYED!', 760, 112), delays2=card2('2', 'DELAYS', RED, 600, 190),
                 preord=card2('#1', 'MOST PRE-ORDERED', GOLD, 820, 170), psstore=btag('PLAYSTATION STORE HISTORY', 1400, 70),
                 nodisc=CA.stamp('NO DISC INSIDE!', 1000, 96), gb200=card2('200+', 'GIGABYTES', BLUE, 680, 170),
                 notone=CA.stamp('NOT ONE MOMENT', 1120, 86), midnite=card2('12:00', 'MIDNIGHT LOCAL TIME', BLUE, 860, 170, 56),
                 cbyc=V.wtag('COUNTRY BY COUNTRY', 1240, GREEN, 78), nzfirst=card2('NEW ZEALAND', 'HITS MIDNIGHT FIRST', BLUE, 1120, 108, 58),
                 ldn11=card2('11 A.M.', 'LONDON', RED, 760, 150), nov18=V.wtag('NOV 18', 640, RED, 100), ny6=card2('6 A.M.', 'NEW YORK', ORNG, 720, 150),
                 yrsdelay=CA.stamp('YEARS OF DELAYS', 1040, 90), oneday=CA.stamp("DIDN'T FIT IN ONE DAY", 1240, 82),
                 clock12=alarm(), playing=V.wtag('ALREADY PLAYING!', 1000, GREEN, 84), still18=card2('NOV 18', 'MOST OF THE PLANET', RED, 820, 150))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); tiles(T('pave.jpg'), (206, 200, 190), (176, 170, 162))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg'))
    nzroom(Pp('nzroom.png')); store(Pp('store.png')); billboard(Pp('billboard.png')); london(Pp('london.png')); nyc(Pp('nyc.png'))
    VA.skyplane(Pp('skyday.png'), (92, 150, 226), (236, 240, 248), hills=(150, 170, 120))
    for n in ('nzroom', 'store', 'billboard', 'london', 'nyc'): items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
