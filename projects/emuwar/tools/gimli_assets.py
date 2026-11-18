#!/usr/bin/env python3
"""Draw every asset for the Gimli Glider Short in code (PIL), in the same style and with the same
builders as video 01 (assets_base.py): a cute new cast (two pilots, a technician, a family), a jet
with seven moods, a glider, a fuel tank, go-karts, cards, textures and a sky backdrop.
usage: make_assets.py <project folder> [font.ttf]"""
import os, json, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import assets_base as B
from assets_base import Draw, LINE, WHITE, BLUSH, MOUTH, H, bez

ROOT = B.ROOT
RED, GOLD, GREEN = (212, 62, 70, 255), (236, 184, 64, 255), (64, 160, 96, 255)
NAVY, SKYB, STEEL, DROP = (40, 50, 96, 255), (186, 218, 246, 255), (196, 200, 214, 255), (150, 200, 240, 255)


def sweat(d, sx, sy):
    d.poly([(sx, sy - 34), (sx - 16, sy + 4), (sx + 16, sy + 4)], fill=DROP); d.dot(sx, sy + 4, 16, DROP)
    d.stroke([(sx, sy - 34), (sx - 16, sy + 2)], LINE, 6); d.stroke([(sx, sy - 34), (sx + 16, sy + 2)], LINE, 6); d.arc(sx, sy + 4, 16, 16, 0, 180, LINE, 6)


# ------------------------------------------------------------------ cast (same head/body builders as video 01)
CAST = {
    'cap':  dict(skin=(246, 222, 200, 255), sh=(222, 190, 166, 255), hat='pilot', base=(44, 56, 104, 255), shade=(32, 40, 80, 255), tie=(196, 52, 64, 255), stache=(150, 150, 162, 255)),
    'fo':   dict(skin=(232, 190, 150, 255), sh=(206, 160, 120, 255), hat='pilot', base=(44, 56, 104, 255), shade=(32, 40, 80, 255), tie=(52, 132, 150, 255), glasses=True),
    'tech': dict(skin=(196, 140, 104, 255), sh=(166, 112, 80, 255), hat='hard', base=(240, 128, 40, 255), shade=(206, 98, 30, 255)),
    'mom':  dict(skin=(244, 214, 192, 255), sh=(220, 184, 160, 255), hat='sun', base=(236, 112, 120, 255), shade=(204, 84, 98, 255), hair=(120, 70, 50, 255)),
    'dad':  dict(skin=(160, 106, 78, 255), sh=(132, 84, 60, 255), hat='cap', base=(62, 160, 160, 255), shade=(42, 124, 128, 255)),
}


def hat(d, char):
    cx, lw, k = H['cx'], H['lw'], CAST[char]['hat']
    if k == 'pilot':
        crown = [(cx - 168, 36), (cx + 168, 36), (cx + 142, 148), (cx - 142, 148)]
        d.poly(crown, fill=NAVY); d.rect(cx - 140, 112, cx + 140, 146, (26, 28, 44, 255)); d.poly(crown, outline=LINE, width=lw)
        d.chord(cx, 148, 158, 46, 0, 180, fill=(26, 28, 44, 255), outline=LINE, width=lw)
        d.stroke([(cx - 74, 76), (cx - 30, 86)], GOLD, 12); d.stroke([(cx + 30, 86), (cx + 74, 76)], GOLD, 12)
        d.dot(cx, 82, 24, GOLD); d.ellipse(cx, 82, 24, 24, outline=LINE, width=6)
    elif k == 'hard':
        yel = (250, 204, 60, 255)
        d.chord(cx, 152, 190, 136, 180, 360, fill=yel, outline=LINE, width=lw)
        d.stroke([(cx, 26), (cx, 150)], (222, 172, 40, 255), 16)
        d.rrect(cx - 224, 138, cx + 224, 166, 14, fill=yel, outline=LINE, width=lw)
    elif k == 'sun':
        pink = (246, 170, 190, 255)
        d.ellipse(cx, 132, 262, 54, fill=pink, outline=LINE, width=lw)
        d.chord(cx, 132, 150, 112, 180, 360, fill=pink, outline=LINE, width=lw)
        d.stroke([(cx - 146, 116), (cx + 146, 116)], RED, 22)
        d.dot(cx + 104, 104, 24, (255, 236, 120, 255)); d.ellipse(cx + 104, 104, 24, 24, outline=LINE, width=6)
    else:                                                    # baseball cap
        blue = (58, 96, 196, 255)
        d.ellipse(cx + 150, 146, 124, 30, fill=(40, 70, 160, 255), outline=LINE, width=lw)
        d.chord(cx, 154, 184, 140, 180, 360, fill=blue, outline=LINE, width=lw)
        d.dot(cx, 16, 16, blue); d.ellipse(cx, 16, 16, 16, outline=LINE, width=6)


def head(char, expr):
    c = CAST[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']
    if 'hair' in c: d.ellipse(cx, cy + 20, R + 42, 186, fill=c['hair'], outline=LINE, width=lw)
    d.ellipse(cx, cy, R, R, fill=c['skin'], outline=LINE, width=lw)
    B.cel_shadow(d, cx, cy, R - 9, c['sh'], c['skin'])
    hat(d, char)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    d.ellipse(cx - 122, cy + 40, 30, 17, fill=BLUSH); d.ellipse(cx + 122, cy + 40, 30, 17, fill=BLUSH)
    B.eyes(d, L, Rr, expr, c['skin']); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses'):
        for x, y in (L, Rr): d.ellipse(x, y, 48, 46, outline=LINE, width=8)
        d.stroke([(L[0] + 48, ey - 4), (Rr[0] - 48, ey - 4)], LINE, 8)
    my = cy + 74
    if 'stache' in c:
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 30, my - 50), (cx + sg * 58, my - 40), (cx + sg * 66, my - 22)), c['stache'], 22)
        my += 10
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = CAST[char]; k = c['hat']; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE)
    d.rrect(x0, y0, x1, y1, r, fill=c['base'])
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=c['base']); d.clip(sh, mask)
    det = Draw(d.w, d.h)
    if k == 'pilot':                                         # white shirt, tie, gold buttons, wings badge
        det.poly([(178, 450), (282, 450), (230, 570)], fill=WHITE)
        det.poly([(217, 466), (243, 466), (240, 556), (230, 582), (220, 556)], fill=c['tie'])
        for y in (630, 700):
            for x in (196, 264): det.dot(x, y, 11, GOLD); det.ellipse(x, y, 11, 11, outline=LINE, width=4)
        det.stroke([(292, 528), (336, 520)], GOLD, 10); det.stroke([(292, 528), (314, 542)], GOLD, 8)
    elif k == 'hard':                                        # hi-vis vest over a blue shirt
        det.poly([(186, 450), (274, 450), (230, 520)], fill=(70, 110, 190, 255))
        for y in (606, 688):
            det.rect(x0, y, x1, y + 24, (226, 230, 240, 255)); det.stroke([(x0, y), (x1, y)], LINE, 4); det.stroke([(x0, y + 24), (x1, y + 24)], LINE, 4)
    elif k == 'sun':                                         # polka-dot dress
        for y in range(500, 800, 64):
            for x in range(110 + (32 if (y // 64) % 2 else 0), 380, 64): det.dot(x, y, 12, (255, 236, 236, 255))
    else:                                                    # striped polo
        for y in range(486, 800, 58): det.rect(x0, y, x1, y + 22, (236, 246, 240, 255))
    d.clip(det, mask)
    d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


B.human_head, B.human_body = head, body                     # build_human() now draws this cast

# ------------------------------------------------------------------ the jet (one puppet, seven moods)
JW, JH = 1200, 520
SKINS = [(246, 222, 200, 255), (196, 140, 104, 255), (232, 190, 150, 255), (160, 106, 78, 255)]
HAIRS = [(90, 60, 40, 255), (44, 36, 44, 255), (206, 154, 64, 255), (120, 70, 50, 255)]
LEAF = [(0, -44), (9, -22), (24, -28), (18, -8), (38, -12), (28, 4), (34, 10), (6, 8), (6, 30), (-6, 30), (-6, 8), (-34, 10), (-28, 4), (-38, -12), (-18, -8), (-24, -28), (-9, -22)]


def leaf(d, cx, cy, s, col=WHITE): d.poly([(cx + x * s, cy + y * s) for x, y in LEAF], fill=col)


def engine(d, x, y, w, h, dead):
    d.rrect(x, y, x + w, y + h, h / 2, fill=(150, 150, 164, 255) if dead else STEEL, outline=LINE, width=10)
    d.ellipse(x + w - 8, y + h / 2, h * 0.24, h / 2 - 5, fill=(96, 96, 110, 255) if dead else (64, 70, 96, 255), outline=LINE, width=6)
    cx, cy = x + w * 0.45, y + h / 2
    if dead:
        d.stroke([(cx - 12, cy - 10), (cx + 12, cy + 10)], LINE, 7); d.stroke([(cx - 12, cy + 10), (cx + 12, cy - 10)], LINE, 7)
    else:
        for k in range(3): d.stroke([(x - 70 + 22 * k, cy - 12 + 12 * k), (x - 40 + 22 * k, cy - 12 + 12 * k)], (150, 200, 250, 255), 7)


def passenger(d, x, y, var, i):
    d.ellipse(x, y, 34, 38, fill=SKYB, outline=LINE, width=7)
    m = Draw(d.w, d.h); m.ellipse(x, y, 30, 34, fill=WHITE)
    p = Draw(d.w, d.h); fy = y + 10
    p.dot(x, fy, 24, SKINS[i % 4]); p.chord(x, fy - 4, 25, 22, 180, 360, fill=HAIRS[i % 4])
    if var == 'saved':
        for ex in (-9, 9): p.arc(x + ex, fy + 2, 5, 5, 200, 340, LINE, 3)
        p.chord(x, fy + 8, 9, 9, 0, 180, fill=MOUTH)
    elif var in ('dead', 'slam'):
        for ex in (-9, 9): p.dot(x + ex, fy, 4.5, LINE)
        p.ellipse(x, fy + 13, 4, 6, fill=LINE)
    else:
        for ex in (-9, 9): p.dot(x + ex, fy, 4, LINE)
        if var in ('cruise', 'park'): p.arc(x, fy + 6, 8, 6, 20, 160, LINE, 3)
        else: p.stroke([(x - 6, fy + 12), (x + 6, fy + 12)], LINE, 3)
    d.clip(p, m)


def nose_face(d, var):
    L, R = (1000, 266), (1076, 268)
    d.ellipse(1022, 326, 22, 12, fill=BLUSH); d.ellipse(1118, 318, 16, 10, fill=BLUSH)
    if var == 'saved':
        for x, y in (L, R): d.arc(x, y + 6, 24, 20, 200, 340, LINE, 10)
    elif var == 'dead':
        for x, y in (L, R): d.ellipse(x, y, 28, 31, fill=WHITE, outline=LINE, width=8); d.dot(x, y + 4, 9, LINE)
    elif var == 'slam':
        for (x, y), sg in ((L, 1), (R, -1)): d.stroke([(x - 16 * sg, y - 14), (x + 12 * sg, y), (x - 16 * sg, y + 14)], LINE, 9)
    else:
        for x, y in (L, R): d.dot(x, y, 23, LINE); d.dot(x - 8, y - 8, 8, WHITE)
    if var == 'eng1':                                        # worried brows
        for (x, y), sg in ((L, 1), (R, -1)): d.stroke([(x - 20 * sg, y - 30), (x + 18 * sg, y - 42)], LINE, 9)
    if var == 'glide':                                       # determined brows
        for (x, y), sg in ((L, 1), (R, -1)): d.stroke([(x - 20 * sg, y - 44), (x + 18 * sg, y - 32)], LINE, 9)
    mx, my = 1092, 336
    if var in ('cruise', 'park'): d.arc(mx, my - 10, 26, 20, 20, 160, LINE, 8)
    elif var == 'eng1': d.stroke([(mx - 22, my), (mx - 11, my - 6), (mx, my + 2), (mx + 11, my - 6), (mx + 22, my)], LINE, 7)
    elif var == 'dead': d.ellipse(mx, my + 2, 11, 15, fill=LINE)
    elif var == 'glide': d.arc(mx, my - 6, 20, 12, 30, 150, LINE, 8)
    elif var == 'slam':
        d.rrect(mx - 24, my - 10, mx + 24, my + 12, 8, fill=WHITE, outline=LINE, width=7); d.stroke([(mx, my - 10), (mx, my + 12)], LINE, 5)
    else:
        d.chord(mx, my - 10, 28, 26, 0, 180, fill=LINE); d.chord(mx, my - 10, 22, 20, 0, 180, fill=MOUTH)
    if var in ('eng1', 'dead'): sweat(d, 958, 226)


def jet(var):
    d = Draw(JW, JH)
    if var in ('cruise', 'eng1', 'glide'):
        for y in (246, 296, 346): d.stroke([(6, y), (60, y)], (255, 255, 255, 220), 9)
    engine(d, 592, 396, 130, 42, var not in ('cruise', 'eng1'))                     # far engine, behind the wing
    d.poly([(118, 228), (44, 40), (158, 40), (302, 228)], fill=RED, outline=LINE, width=12); leaf(d, 140, 126, 1.15)
    pts = ([(150, 222), (1000, 214)] + bez((1000, 214), (1112, 212), (1170, 292), (1142, 340)) +
           bez((1142, 340), (1122, 374), (1062, 378), (992, 378)) + [(300, 378)] + bez((300, 378), (196, 378), (112, 330), (62, 240)))
    d.poly(pts, fill=(248, 249, 253, 255))
    m = Draw(JW, JH); m.poly(pts, fill=WHITE)
    sh = Draw(JW, JH); sh.rect(0, 340, JW, JH, (218, 222, 236, 255)); sh.rect(0, 316, JW, 332, RED); d.clip(sh, m)
    for i, x in enumerate(range(380, 940, 88)): passenger(d, x, 266, var, i)
    nose_face(d, var)
    d.stroke(pts, LINE, 12, closed=True)
    d.poly([(70, 262), (232, 256), (198, 292), (38, 292)], fill=(232, 234, 244, 255), outline=LINE, width=10)
    d.poly([(500, 348), (722, 348), (592, 466), (440, 466)], fill=(228, 232, 242, 255), outline=LINE, width=12)
    engine(d, 470, 418, 170, 58, var != 'cruise')                                      # near engine
    if var in ('park', 'slam', 'saved'):
        for x in (540, 584):
            d.stroke([(562, 470), (x, 494)], LINE, 10); d.dot(x, 500, 19, (64, 64, 78, 255)); d.dot(x, 500, 7, STEEL)
        if var == 'park':
            d.stroke([(1010, 376), (1010, 494)], LINE, 10); d.dot(1010, 500, 18, (64, 64, 78, 255)); d.dot(1010, 500, 7, STEEL)
    if var == 'slam':
        for sx, sy, r in ((1120, 410, 26), (1170, 440, 18), (1080, 450, 16)):
            d.poly([(sx, sy - r), (sx + r * 0.3, sy - r * 0.3), (sx + r, sy), (sx + r * 0.3, sy + r * 0.3), (sx, sy + r),
                    (sx - r * 0.3, sy + r * 0.3), (sx - r, sy), (sx - r * 0.3, sy - r * 0.3)], fill=(255, 220, 80, 255), outline=LINE, width=5)
    return d.out()


def glider():
    d = Draw(900, 300)
    d.poly([(60, 182), (842, 126), (850, 146), (70, 204)], fill=(238, 240, 248, 255), outline=LINE, width=9)
    body_ = bez((120, 150), (320, 118), (680, 116), (806, 150)) + bez((806, 150), (770, 184), (420, 188), (120, 164))
    d.poly(body_, fill=WHITE, outline=LINE, width=9)
    d.poly([(104, 156), (92, 66), (152, 66), (196, 152)], fill=(240, 128, 90, 255), outline=LINE, width=9)
    d.ellipse(640, 136, 58, 22, fill=SKYB, outline=LINE, width=7)
    d.dot(748, 146, 7, LINE); d.dot(774, 148, 6, LINE); d.arc(764, 158, 12, 8, 20, 160, LINE, 4)
    return d.out()


def tank():
    d = Draw(420, 470)
    d.rrect(150, 24, 270, 84, 16, fill=STEEL, outline=LINE, width=10)
    d.rrect(30, 70, 390, 452, 70, fill=(214, 218, 230, 255), outline=LINE, width=14)
    for x in (70, 350):
        for y in (114, 410): d.dot(x, y, 9, (160, 164, 180, 255))
    d.text(190, 126, "FUEL", 56, RED, stroke=4, stroke_fill=LINE)
    d.rrect(302, 164, 352, 404, 22, fill=(246, 248, 252, 255), outline=LINE, width=8)
    m = Draw(420, 470); m.rrect(306, 168, 348, 400, 18, fill=WHITE); f = Draw(420, 470); f.rect(300, 372, 356, 404, (244, 176, 60, 255)); d.clip(f, m)
    for x in (128, 220): d.dot(x, 252, 21, LINE); d.dot(x - 7, 245, 7, WHITE)
    d.stroke([(100, 214), (146, 202)], LINE, 10); d.stroke([(202, 202), (248, 214)], LINE, 10)
    d.stroke([(124, 324), (144, 314), (164, 326), (184, 314), (204, 326), (224, 316)], LINE, 9)
    d.ellipse(88, 292, 24, 13, fill=BLUSH); d.ellipse(260, 292, 24, 13, fill=BLUSH)
    sweat(d, 268, 190)
    return d.out()


def kart(col, helmet, face):
    d = Draw(560, 380)
    d.rrect(206, 196, 316, 290, 40, fill=(250, 250, 250, 255), outline=LINE, width=10)
    d.dot(262, 128, 100, LINE); d.dot(262, 128, 90, helmet)
    d.ellipse(286, 142, 60, 50, fill=(246, 222, 200, 255), outline=LINE, width=8)
    d.ellipse(252, 160, 12, 7, fill=BLUSH)
    if face == 'shocked':
        for x in (268, 306): d.ellipse(x, 136, 13, 15, fill=WHITE, outline=LINE, width=5); d.dot(x, 138, 5, LINE)
        d.ellipse(288, 170, 8, 10, fill=LINE)
    else:
        for x in (268, 306): d.dot(x, 136, 9, LINE); d.dot(x - 3, 132, 3, WHITE)
        d.chord(288, 160, 17, 16, 0, 180, fill=LINE); d.chord(288, 160, 13, 12, 0, 180, fill=MOUTH)
    d.stroke([(316, 236), (356, 206)], LINE, 10); d.ellipse(360, 202, 16, 24, outline=LINE, width=8)
    d.poly([(40, 272), (470, 262), (532, 290), (522, 322), (40, 322)], fill=col, outline=LINE, width=12)
    d.dot(176, 296, 22, WHITE); d.ellipse(176, 296, 22, 22, outline=LINE, width=5)
    for x in (112, 440): d.dot(x, 322, 50, LINE); d.dot(x, 322, 40, (60, 60, 72, 255)); d.dot(x, 322, 16, STEEL)
    return d.out()


# ------------------------------------------------------------------ cards and stickers
def card(w, h, bg=(246, 238, 214, 255)):
    d = Draw(w, h); d.rrect(8, 8, w - 8, h - 8, 30, fill=bg, outline=LINE, width=14); return d


def num_card(big, small, col, mark=None):
    d = card(640, 420); d.text(320, 172, big, 200, col, stroke=8, stroke_fill=LINE); d.text(320, 330, small, 66, LINE)
    if mark == 'x':
        for a, b in (((130, 80), (510, 340)), ((510, 80), (130, 340))): d.stroke([a, b], LINE, 60); d.stroke([a, b], RED, 38)
    if mark == 'ok':
        d.dot(560, 84, 48, GREEN); d.ellipse(560, 84, 48, 48, outline=LINE, width=8); d.stroke([(536, 84), (554, 104), (586, 64)], WHITE, 14)
    return d.out()


def cmp_card():
    d = card(720, 520); d.text(360, 84, "FUEL", 84, LINE)
    for i, (lab, frac, col) in enumerate((("NEEDED", 1.0, GREEN), ("LOADED", 0.45, RED))):
        y = 176 + i * 170
        d.text(360, y, lab, 50, LINE)
        d.rrect(70, y + 40, 650, y + 112, 24, fill=(232, 228, 216, 255), outline=LINE, width=10)
        m = Draw(720, 520); m.rrect(80, y + 50, 640, y + 102, 16, fill=WHITE)
        f = Draw(720, 520); f.rect(70, y + 40, 80 + 560 * frac, y + 112, col); d.clip(f, m)
    return d.out()


def cal_card(top, big, bottom):
    d = Draw(480, 520); d.rrect(10, 30, 470, 510, 30, fill=(250, 246, 236, 255))
    m = Draw(480, 520); m.rrect(10, 30, 470, 510, 30, fill=WHITE); hd = Draw(480, 520); hd.rect(0, 0, 480, 150, RED); d.clip(hd, m)
    d.rrect(10, 30, 470, 510, 30, outline=LINE, width=14); d.stroke([(10, 150), (470, 150)], LINE, 10)
    for x in (130, 350): d.rrect(x - 14, 6, x + 14, 70, 10, fill=(150, 150, 164, 255), outline=LINE, width=6)
    d.text(240, 92, top, 64, WHITE, stroke=4, stroke_fill=LINE)
    d.text(240, 300 if bottom else 330, big, 170 if len(big) <= 2 else 136, LINE)
    if bottom: d.text(240, 448, bottom, 66, RED, stroke=3, stroke_fill=LINE)
    return d.out()


def flight_card():
    d = card(760, 300, (250, 246, 236, 255))
    for y in range(36, 270, 26): d.stroke([(560, y), (560, y + 12)], (180, 170, 150, 255), 6)
    leaf(d, 110, 154, 1.9, RED)
    d.text(350, 104, "FLIGHT", 62, LINE); d.text(350, 196, "143", 120, RED, stroke=6, stroke_fill=LINE)
    d.poly([(610, 150), (708, 138), (722, 150), (708, 162)], fill=LINE)
    d.poly([(660, 148), (636, 108), (656, 108), (690, 146)], fill=LINE); d.poly([(660, 152), (636, 192), (656, 192), (690, 154)], fill=LINE)
    return d.out()


def crew_card():
    d = card(640, 440); d.text(320, 118, "61", 150, LINE); d.text(320, 234, "PASSENGERS", 56, RED); d.text(320, 340, "+ 8 CREW", 76, LINE)
    return d.out()


def alt_card():
    d = Draw(480, 480); d.dot(240, 240, 228, LINE); d.dot(240, 240, 214, (250, 250, 246, 255))
    for k in range(10):
        a = 2 * math.pi * k / 10 - math.pi / 2
        d.stroke([(240 + 176 * math.cos(a), 240 + 176 * math.sin(a)), (240 + 204 * math.cos(a), 240 + 204 * math.sin(a))], LINE, 9)
    a = math.radians(-50); d.stroke([(240, 240), (240 + 150 * math.cos(a), 240 + 150 * math.sin(a))], RED, 14); d.dot(240, 240, 16, LINE)
    d.text(240, 318, "41,000", 78, LINE); d.text(240, 386, "FEET", 46, RED)
    return d.out()


def tag(txt):
    d = Draw(480, 220); d.rrect(14, 14, 466, 206, 30, fill=RED, outline=LINE, width=14); d.rrect(38, 38, 442, 182, 18, outline=(255, 236, 236, 255), width=6)
    d.text(240, 114, txt, 84, WHITE, stroke=6, stroke_fill=LINE); return d.out()


def badge():
    d = Draw(380, 470); blue = (70, 110, 200, 255)
    d.poly([(140, 250), (92, 452), (152, 414), (184, 462), (196, 270)], fill=blue, outline=LINE, width=8)
    d.poly([(240, 250), (288, 452), (228, 414), (196, 462), (184, 270)], fill=blue, outline=LINE, width=8)
    pts = [(190 + (152 if k % 2 == 0 else 130) * math.cos(math.pi * k / 18), 182 + (152 if k % 2 == 0 else 130) * math.sin(math.pi * k / 18)) for k in range(36)]
    d.poly(pts, fill=GOLD, outline=LINE, width=8); d.dot(190, 182, 112, (255, 226, 120, 255)); d.ellipse(190, 182, 112, 112, outline=LINE, width=6)
    d.text(190, 150, "1st", 96, RED, stroke=4, stroke_fill=LINE); d.text(190, 232, "METRIC", 42, LINE)
    return d.out()


def gimli_sign():
    d = Draw(680, 480)
    for x in (170, 510): d.rrect(x - 16, 250, x + 16, 472, 8, fill=(150, 100, 60, 255), outline=LINE, width=8)
    d.rrect(20, 20, 660, 290, 30, fill=(56, 128, 88, 255), outline=LINE, width=14); d.rrect(42, 42, 638, 268, 20, outline=WHITE, width=8)
    d.text(340, 132, "GIMLI", 132, WHITE, stroke=6, stroke_fill=LINE); d.text(340, 226, "AIR BASE", 52, (255, 236, 160, 255))
    return d.out()


def dots():
    d = Draw(440, 320)
    d.poly([(120, 214), (70, 300), (196, 238)], fill=WHITE, outline=LINE, width=10)
    d.ellipse(220, 140, 200, 118, fill=WHITE, outline=LINE, width=12)
    d.poly([(128, 220), (96, 276), (184, 236)], fill=WHITE)
    for x in (148, 220, 292): d.dot(x, 140, 22, LINE)
    return d.out()


def flame():
    d = Draw(320, 440)
    for w, h, col, ol in ((120, 420, (238, 84, 52, 255), True), (84, 300, (250, 150, 50, 255), False), (46, 180, (255, 226, 96, 255), False)):
        cx, by = 160, 430
        pts = bez((cx, by), (cx - 1.3 * w, by), (cx - 0.3 * w, by - 0.6 * h), (cx, by - h)) + bez((cx, by - h), (cx + 0.3 * w, by - 0.6 * h), (cx + 1.3 * w, by), (cx, by))
        d.poly(pts, fill=col, outline=LINE if ol else None, width=10 if ol else 0)
    return d.out()


def hearts():
    d = Draw(440, 320)
    for cx, cy, s in ((100, 190, 1.0), (230, 130, 1.35), (350, 200, 0.9)):
        pts = bez((cx, cy + 50 * s), (cx - 90 * s, cy - 10 * s), (cx - 40 * s, cy - 80 * s), (cx, cy - 30 * s)) + bez((cx, cy - 30 * s), (cx + 40 * s, cy - 80 * s), (cx + 90 * s, cy - 10 * s), (cx, cy + 50 * s))
        d.poly(pts, fill=(242, 110, 140, 255), outline=LINE, width=9); d.dot(cx - 24 * s, cy - 32 * s, 8 * s, (255, 220, 230, 255))
    return d.out()


def build_card(name, imgs):
    """one-layer sticker puppet; extra images become faces (same size, same pivot) so `face` can swap them"""
    B.build_sticker(name, imgs['default'])
    folder = os.path.join(ROOT, 'puppets', name); rp = os.path.join(folder, 'rig.json'); rig = json.load(open(rp))
    w, h = imgs['default'].size; os.makedirs(os.path.join(folder, 'faces'), exist_ok=True)
    for k, im in imgs.items():
        if k == 'default': continue
        im.save(os.path.join(folder, 'faces', k + '.png'))
        rig['faces'][k] = {"file": "faces/%s.png" % k, "size": [w, h], "pivot": [w / 2, h / 2], "center": [w / 2, h / 2], "diameter": w}
    with open(rp, 'w') as fh: json.dump(rig, fh, indent=1)


# ------------------------------------------------------------------ props, textures, backdrop
def cloud(path):
    d = Draw(900, 460); blobs = [(170, 340, 120), (320, 260, 160), (510, 236, 180), (690, 300, 150), (430, 340, 150), (800, 370, 90), (90, 390, 80)]
    for x, y, r in blobs: d.dot(x, y, r + 10, LINE)
    for x, y, r in blobs: d.dot(x, y, r, (252, 253, 255, 255))
    m = Draw(900, 460)
    for x, y, r in blobs: m.dot(x, y, r, WHITE)
    s = Draw(900, 460); s.rect(0, 360, 900, 460, (220, 230, 248, 255)); d.clip(s, m)
    d.out().save(path)


def porthole(path):
    d = Draw(400, 400); d.dot(200, 200, 192, LINE); d.dot(200, 200, 180, (176, 182, 202, 255)); d.dot(200, 200, 140, LINE)
    d.dot(200, 200, 130, (126, 176, 236, 255))
    for x, y, r in ((150, 236, 40), (200, 222, 52), (252, 240, 38)): d.dot(x, y, r, WHITE)
    d.arc(200, 200, 100, 100, 200, 250, (255, 255, 255, 200), 14)
    d.out().save(path)


def gauges(path):
    d = Draw(1400, 380); d.rrect(10, 10, 1390, 370, 40, fill=(58, 64, 86, 255), outline=LINE, width=14)
    def dial(cx, kind, label):
        cy, r = 168, 110
        d.dot(cx, cy, r + 12, LINE); d.dot(cx, cy, r, (30, 34, 46, 255))
        if kind == 'att':
            m = Draw(1400, 380); m.dot(cx, cy, r, WHITE); a = Draw(1400, 380)
            a.rect(cx - r, cy - r, cx + r, cy, (90, 150, 220, 255)); a.rect(cx - r, cy, cx + r, cy + r, (150, 104, 70, 255)); d.clip(a, m)
            d.stroke([(cx - 60, cy), (cx + 60, cy)], (255, 220, 80, 255), 10)
        elif kind == 'fuel':                               # blank, broken display
            d.rrect(cx - 70, cy - 36, cx + 70, cy + 36, 10, fill=(18, 24, 20, 255), outline=(92, 98, 112, 255), width=6)
            d.text(cx, cy + 2, "- - -", 40, (86, 108, 92, 255))
        else:
            for k in range(9):
                a_ = math.radians(-220 + k * 32.5)
                d.stroke([(cx + 78 * math.cos(a_), cy + 78 * math.sin(a_)), (cx + 96 * math.cos(a_), cy + 96 * math.sin(a_))], WHITE, 6)
            d.stroke([(cx, cy), (cx + 70 * math.cos(-0.7), cy + 70 * math.sin(-0.7))], (255, 120, 90, 255), 9); d.dot(cx, cy, 10, WHITE)
        d.text(cx, 332, label, 44, (236, 238, 246, 255))
    dial(210, 'att', "ATTITUDE"); dial(530, 'fuel', "FUEL"); dial(870, 'fuel', "FUEL"); dial(1190, 'needle', "SPEED")
    for y, col in ((96, (90, 220, 120, 255)), (168, (250, 180, 60, 255)), (240, (230, 70, 70, 255))): d.dot(700, y, 18, LINE); d.dot(700, y, 13, col)
    d.out().save(path)


def metric(path):
    d = Draw(600, 800); d.rrect(10, 10, 590, 790, 26, fill=(246, 240, 226, 255))
    m = Draw(600, 800); m.rrect(10, 10, 590, 790, 26, fill=WHITE); hd = Draw(600, 800); hd.rect(0, 0, 600, 200, RED); d.clip(hd, m)
    d.rrect(10, 10, 590, 790, 26, outline=LINE, width=14); d.stroke([(10, 200), (590, 200)], LINE, 10)
    d.text(300, 106, "CANADA", 100, WHITE, stroke=5, stroke_fill=LINE)
    d.text(300, 290, "GOES", 84, LINE); d.text(300, 398, "METRIC", 110, RED, stroke=5, stroke_fill=LINE)
    d.rrect(70, 476, 530, 548, 10, fill=(250, 210, 80, 255), outline=LINE, width=8)
    for i, x in enumerate(range(92, 520, 22)): d.stroke([(x, 478), (x, 512 if i % 5 == 0 else 498)], LINE, 4)
    d.text(180, 672, "kg", 120, LINE); d.text(430, 672, "L", 130, (60, 120, 200, 255), stroke=4, stroke_fill=LINE)
    d.out().save(path)


def famday(path):
    d = Draw(1500, 300); d.rrect(10, 40, 1490, 290, 30, fill=(255, 214, 92, 255), outline=LINE, width=14)
    cols = [RED, (70, 140, 220, 255), GREEN, (250, 150, 60, 255)]
    for k in range(14):
        x = 40 + k * 104; d.poly([(x, 30), (x + 90, 30), (x + 45, 100)], fill=cols[k % 4], outline=LINE, width=6)
    d.text(750, 190, "FAMILY DAY", 150, RED, stroke=8, stroke_fill=LINE)
    d.out().save(path)


def periodic(n, seed, freqs):
    rng = np.random.RandomState(seed); y, x = np.mgrid[0:n, 0:n] / n; v = np.zeros((n, n))
    for kx in range(-freqs, freqs + 1):
        for ky in range(0, freqs + 1):
            if kx == 0 and ky == 0: continue
            v += rng.uniform(0.5, 1) / math.hypot(kx, ky) * np.sin(2 * np.pi * (kx * x + ky * y) + rng.uniform(0, 6.3))
    return (v - v.min()) / (v.max() - v.min())


def save_tex(a, path): Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path, quality=92)


def tex_cloud(path, n=512):
    t = np.clip((periodic(n, 4, 6)[..., None] - 0.35) / 0.4, 0, 1)
    save_tex(np.array([196, 212, 240]) + np.array([59, 43, 15]) * t, path)


def tex_asphalt(path, n=512):
    rng = np.random.RandomState(2); a = np.zeros((n, n, 3)) + [82, 84, 96]
    a += (periodic(n, 9, 5)[..., None] - 0.5) * 16 + rng.normal(0, 7, (n, n, 1)); a[rng.rand(n, n) < 0.006] += 40
    save_tex(a, path)


def tex_concrete(path, n=512):
    rng = np.random.RandomState(3); a = np.zeros((n, n, 3)) + [200, 202, 208]
    a += (periodic(n, 5, 4)[..., None] - 0.5) * 18 + rng.normal(0, 4, (n, n, 1))
    for k in (0, 256): a[k:k + 3, :] -= 46; a[:, k:k + 3] -= 46
    save_tex(a, path)


def tex_panel(path, n=512):
    a = np.zeros((n, n, 3)) + [128, 136, 168]; a += (periodic(n, 6, 3)[..., None] - 0.5) * 10
    for k in (0, 128, 256, 384): a[k:k + 4, :] = [84, 90, 116]; a[:, k:k + 4] = [84, 90, 116]
    im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); dr = ImageDraw.Draw(im)
    for cx in range(0, n, 128):
        for cy in range(0, n, 128):
            for dx, dy in ((14, 14), (114, 14), (14, 114), (114, 114)): dr.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4], fill=(150, 156, 180))
    random.seed(8)
    for _ in range(14):
        x, y = random.randrange(20, n - 60, 4), random.randrange(20, n - 40, 4)
        dr.rectangle([x, y, x + 34, y + 18], fill=(40, 44, 60))
        dr.rectangle([x + 4, y + 4, x + 14, y + 14], fill=random.choice([(90, 220, 120), (250, 180, 60), (230, 80, 80), (200, 210, 230)]))
    im.save(path, quality=92)


def sky(path, W=2520, Hh=1080):
    y = np.linspace(0, 1, Hh)[:, None, None]; t = np.clip(y / 0.9, 0, 1) ** 1.25
    a = np.broadcast_to(np.array([88, 136, 222]) * (1 - t) + np.array([248, 216, 184]) * t, (Hh, W, 3)).copy()
    im = Image.fromarray(a.astype(np.uint8)).convert('RGBA')
    cl = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); dr = ImageDraw.Draw(cl); random.seed(12)
    for _ in range(26):
        x, yy, r = random.randrange(0, W), random.randrange(560, 930), random.randrange(40, 120)
        for _k in range(5):
            ox, oy, rr = x + random.randint(-2 * r, 2 * r), yy + random.randint(-r // 3, r // 3), int(r * random.uniform(0.6, 1.1))
            for dx in (-W, 0, W): dr.ellipse([ox + dx - rr * 1.6, oy - rr, ox + dx + rr * 1.6, oy + rr * 0.7], fill=(255, 255, 255, 170))
    im = Image.alpha_composite(im, cl.filter(ImageFilter.GaussianBlur(8)))
    dr = ImageDraw.Draw(im)
    pts = [(x, 1000 - 16 * math.sin(2 * math.pi * 5 * x / W) - 10 * math.sin(2 * math.pi * 13 * x / W + 1)) for x in range(0, W + 1, 12)]
    dr.polygon(pts + [(W, Hh), (0, Hh)], fill=(104, 140, 112, 255)); dr.rectangle([0, 1030, W, Hh], fill=(150, 182, 120, 255))
    haze = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); ImageDraw.Draw(haze).rectangle([0, 800, W, 1030], fill=(250, 222, 196, 80))
    Image.alpha_composite(im, haze.filter(ImageFilter.GaussianBlur(40))).convert('RGB').save(path, quality=92)


# ------------------------------------------------------------------ run
if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    for ch in CAST:
        layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked')]
    cards = {'jet': {('default' if v == 'cruise' else v): jet(v) for v in ('cruise', 'eng1', 'dead', 'glide', 'park', 'slam', 'saved')},
             'n177': {'default': num_card("1.77", "lb per L", RED), 'x': num_card("1.77", "lb per L", RED, 'x')}}
    for i, (col, hel) in enumerate((((226, 70, 70, 255), (250, 210, 70, 255)), ((70, 130, 220, 255), (240, 120, 160, 255)), ((250, 200, 60, 255), (90, 180, 120, 255)))):
        cards['kart%d' % (i + 1)] = {'default': kart(col, hel, 'happy'), 'shocked': kart(col, hel, 'shocked')}
    singles = dict(glider=glider(), tank=tank(), n08=num_card("0.8", "kg per L", GREEN, 'ok'), cmp=cmp_card(), crew=crew_card(), alt=alt_card(),
                   cal83=cal_card("JULY", "23", "1983"), cal08=cal_card("UNTIL", "2008", ""), flt=flight_card(), broken=tag("BROKEN"),
                   badge=badge(), gimli=gimli_sign(), dots=dots(), flame=flame(), hearts=hearts(), slam=B.sticker_burst('SLAM!'),
                   poof=B.sticker_poof(), ques=B.sticker_mark('?', GOLD))
    for nm, im in singles.items(): cards[nm] = {'default': im}
    for nm, imgs in cards.items():
        build_card(nm, imgs); items += [(nm + ' ' + k, im) for k, im in imgs.items()]
    T = lambda n: os.path.join(ROOT, 'textures', n)
    tex_cloud(T('cloud.jpg')); tex_asphalt(T('asphalt.jpg')); tex_concrete(T('concrete.jpg')); tex_panel(T('panel.jpg'))
    B.tex_grass(T('grass.jpg')); B.tex_wood(T('wood.jpg'))
    sky(os.path.join(ROOT, 'bg', 'sky.jpg'))
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    cloud(Pp('cloud.png')); porthole(Pp('porthole.png')); gauges(Pp('gauges.png')); metric(Pp('metric.png')); famday(Pp('famday.png')); B.sparkle(Pp('sparkle.png'))
    for n in ('cloud', 'porthole', 'gauges', 'metric', 'famday'): items.append((n, Image.open(Pp(n + '.png'))))
    for n in ('cloud', 'asphalt', 'concrete', 'panel'): items.append((n, Image.open(T(n + '.jpg'))))
    items.append(('backdrop', Image.open(os.path.join(ROOT, 'bg', 'sky.jpg'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
