#!/usr/bin/env python3
"""Assets for video 05 (Wrong Way Corrigan), drawn in code with the channel builders.
Reuses the cast code of videos 02-04 so mom, dad, tech, the Viking, the Vasa sailors and the captain look identical,
and adds Doug Corrigan, two inspectors, the Curtiss Robin (Doug in its window; parked / flying / dripping), puffy
clouds (with and without faces), sheep, a compass with a separate needle (it spins with the pose), a fuel tank,
gasoline, a screwdriver, an ocean liner, a parade car, ticker tape, a signpost, a windsock, stamps, cards and skies.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math
import numpy as np
from PIL import Image, ImageDraw
import assets_base as B
import gimli_assets as G
import viking_assets as V
import vasa_assets as VA
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN, BLUE, PURP, GREY = G.RED, G.GOLD, G.GREEN, VA.BLUE, (126, 70, 140, 255), (110, 116, 136, 255)
dk, SK = VA.dk, VA.SK
LEATHER, SILVER, CREAM, BRASS, GLASS = (150, 92, 54, 255), (200, 208, 220, 255), (250, 238, 206, 255), (222, 172, 70, 255), (150, 212, 240, 255)
GAS, STAMP, TYRE = (186, 222, 78, 215), (214, 40, 48, 255), (46, 44, 52, 255)
NEW = {
    'doug': dict(skin=SK[0][0], sh=SK[0][1], hat='avi', hc=LEATHER, hair=(206, 112, 58, 255), base=(140, 88, 52, 255), shade=(110, 66, 38, 255), scarf=1, freck=1),
    'insp1': dict(skin=SK[1][0], sh=SK[1][1], hat='fed', hc=(78, 84, 102, 255), base=(112, 118, 136, 255), shade=(86, 92, 110, 255), tie=RED, stache=(66, 50, 40, 255), glasses=1),
    'insp2': dict(skin=SK[2][0], sh=SK[2][1], hat='fed', hc=(126, 90, 62, 255), base=(156, 126, 96, 255), shade=(126, 98, 72, 255), tie=BLUE),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; hc = c['hc']
    d.ellipse(cx, cy, R, R, fill=c['skin'], outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, c['sh'], c['skin'])
    if c['hat'] == 'avi':                                    # leather flying cap with ear flaps, goggles pushed up, a ginger fringe
        for x in range(cx - 120, cx + 121, 40): d.poly([(x - 30, 140), (x + 4, 198), (x + 30, 140)], fill=c['hair'], outline=LINE, width=8)
        for sg in (-1, 1): d.rrect(cx + sg * 190 - 34, cy - 90, cx + sg * 190 + 34, cy + 96, 32, fill=hc, outline=LINE, width=lw)
        d.chord(cx, 158, 214, 162, 180, 360, fill=hc, outline=LINE, width=lw)
        d.stroke(bez((cx, 2), (cx + 6, 50), (cx + 4, 110), (cx, 156)), dk(hc), 10)
        d.rrect(cx - 214, 92, cx + 214, 132, 18, fill=(70, 46, 34, 255), outline=LINE, width=10)
        for sg in (-1, 1):
            d.ellipse(cx + sg * 80, 104, 62, 56, fill=BRASS, outline=LINE, width=12); d.ellipse(cx + sg * 80, 104, 42, 37, fill=GLASS, outline=LINE, width=6)
            d.dot(cx + sg * 80 - 14, 90, 10, WHITE)
    else:                                                    # fedora
        d.ellipse(cx, 150, 250, 40, fill=dk(hc, 0.86), outline=LINE, width=lw)
        d.poly([(cx - 150, 150), (cx - 128, 30), (cx - 40, 46), (cx, 64), (cx + 40, 46), (cx + 128, 30), (cx + 150, 150)], fill=hc, outline=LINE, width=lw)
        d.poly([(cx - 141, 104), (cx + 141, 104), (cx + 147, 136), (cx - 147, 136)], fill=(40, 36, 44, 255))
        d.chord(cx, 150, 250, 40, 0, 180, fill=dk(hc, 0.86), outline=LINE, width=lw)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 28, 16, fill=BLUSH)
    if c.get('freck'):
        for sg in (-1, 1):
            for dx, dy in ((-14, 0), (8, -10), (10, 12)): d.dot(cx + sg * 108 + dx, cy + 12 + dy, 5, (196, 120, 90, 255))
    B.eyes(d, L, Rr, expr, c['skin']); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses'):
        for p in (L, Rr): d.ellipse(p[0], p[1], 48, 44, outline=LINE, width=9)
        d.stroke([(L[0] + 48, ey), (Rr[0] - 48, ey)], LINE, 9)
    my = cy + 74
    if 'stache' in c:
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 30, my - 50), (cx + sg * 58, my - 40), (cx + sg * 66, my - 22)), c['stache'], 24)
        my += 12
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=c['base'])
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=c['base']); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if c.get('scarf'):                                       # flight jacket: fleece collar, zip, pockets, white scarf
        t.stroke([(230, 500), (230, 800)], dk(c['base'], 0.6), 10)
        for x in (150, 310): t.rrect(x - 40, 640, x + 40, 700, 10, fill=dk(c['base'], 0.86), outline=LINE, width=6)
        t.poly([(110, 452), (350, 452), (334, 548), (230, 506), (126, 548)], fill=CREAM); t.stroke([(126, 548), (230, 506), (334, 548)], LINE, 7)
        t.rrect(150, 446, 310, 500, 22, fill=WHITE, outline=LINE, width=7)
    else:                                                    # suit: shirt, tie, lapels
        t.poly([(170, 452), (290, 452), (230, 590)], fill=WHITE)
        tie = [(230, 474), (212, 500), (220, 610), (230, 628), (240, 610), (248, 500)]; t.poly(tie, fill=c['tie']); t.stroke(tie + [tie[0]], LINE, 6)
        for sg in (-1, 1): t.stroke([(230 + sg * 64, 452), (230 + sg * 20, 600)], LINE, 7)
        for y in (660, 730): t.dot(230, y, 10, dk(c['base'], 0.6))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    if c.get('scarf'): d.poly([(296, 476), (404, 520), (420, 610), (368, 566), (322, 530)], fill=WHITE, outline=LINE, width=10)
    else:                                                    # clipboard
        d.rrect(110, 560, 250, 740, 14, fill=(160, 112, 66, 255), outline=LINE, width=9); d.rect(126, 588, 234, 724, WHITE)
        for y in (614, 646, 678): d.stroke([(140, y), (220, y)], (150, 156, 170, 255), 7)
        d.rrect(156, 546, 204, 580, 8, fill=SILVER, outline=LINE, width=6)
    return d.out()


def framed_face(im, box, r=18, expr='happy', zoom=1.25, fy=0.6):
    """Doug's own head, clipped into a window / photo box of a sticker (so the pilot is always the same Doug)."""
    x0, y0, x1, y1 = box; w, h = x1 - x0, y1 - y0; s = w * zoom / 460.0
    hd = head('doug', expr).crop((0, 0, 460, 480)).resize((int(460 * s), int(480 * s)), Image.LANCZOS)
    win = Image.new('RGBA', (w, h), GLASS); win.alpha_composite(hd, (int(w / 2 - 230 * s), int(h * fy - 270 * s)))
    m = Draw(w, h); m.rrect(0, 0, w, h, r, fill=WHITE); im.paste(win, (x0, y0), m.out())
    o = Draw(im.size[0], im.size[1]); o.rrect(x0, y0, x1, y1, r, outline=LINE, width=12); im.alpha_composite(o.out()); return im


# ------------------------------------------------------------------ stickers
def robin(st):                                              # the Curtiss Robin, nose to the right
    d = Draw(1400, 720)
    if st != 'default':
        for y, x0 in ((250, 20), (340, 60), (430, 30)): d.stroke([(x0, y), (x0 + 120, y)], LINE, 26); d.stroke([(x0 + 4, y), (x0 + 116, y)], WHITE, 12)
    d.stroke([(700, 450), (770, 600)], LINE, 24); d.stroke([(860, 450), (774, 600)], LINE, 24)
    d.ellipse(772, 612, 76, 76, fill=TYRE, outline=LINE, width=14); d.ellipse(772, 612, 30, 30, fill=SILVER, outline=LINE, width=8)
    d.stroke([(250, 330), (236, 392)], LINE, 18); d.dot(236, 402, 24, TYRE)
    d.poly([(170, 290), (118, 110), (214, 92), (340, 280)], fill=RED, outline=LINE, width=14)
    d.poly(bez((150, 300), (420, 200), (700, 170), (1150, 228)) + [(1180, 262), (1180, 420)] + bez((1150, 440), (900, 482), (500, 470), (150, 332)), fill=SILVER, outline=LINE, width=16)
    d.poly(bez((196, 318), (500, 382), (900, 392), (1166, 352)) + bez((1166, 384), (900, 424), (500, 414), (196, 334)), fill=RED)
    d.rrect(84, 298, 330, 330, 14, fill=RED, outline=LINE, width=10)
    d.rrect(560, 206, 700, 300, 18, fill=GLASS, outline=LINE, width=12); d.stroke([(586, 222), (620, 280)], WHITE, 8)
    d.ellipse(1176, 338, 46, 122, fill=dk(SILVER, 0.7), outline=LINE, width=14)
    for k in range(5): d.dot(1180, 258 + k * 40, 12, (70, 72, 84, 255))
    if st == 'default': d.rrect(1222, 146, 1252, 530, 14, fill=(150, 98, 56, 255), outline=LINE, width=10)
    else: d.ellipse(1238, 338, 24, 204, fill=(232, 238, 248, 120), outline=(60, 60, 70, 150), width=6)
    d.dot(1238, 338, 26, RED); d.ellipse(1238, 338, 26, 26, outline=LINE, width=8)
    d.poly(bez((330, 152), (500, 110), (900, 104), (1090, 142)) + bez((1090, 142), (1070, 184), (600, 186), (330, 178)), fill=CREAM, outline=LINE, width=14)
    d.stroke([(1000, 180), (880, 440)], LINE, 16); d.stroke([(1000, 180), (880, 440)], SILVER, 6)
    if st == 'drip':
        for x, y, r in ((640, 520, 20), (622, 590, 15), (650, 650, 12)): d.poly([(x, y - r * 2.2), (x + r, y), (x - r, y)], fill=GAS); d.ellipse(x, y + 2, r, r, fill=GAS, outline=LINE, width=6)
    return framed_face(d.out(), (720, 206, 860, 300))


def cloud(face):
    d = Draw(900, 560); P_ = ((250, 330, 150), (440, 250, 190), (640, 310, 160), (770, 390, 110), (140, 400, 100), (450, 400, 150))
    for x, y, r in P_: d.dot(x, y, r + 14, LINE)
    for x, y, r in P_: d.dot(x, y, r, (222, 232, 248, 255))
    for x, y, r in P_: d.dot(x - r * 0.12, y - r * 0.18, r * 0.8, WHITE)
    if face:                                                 # shifty "who, us?" eyes
        for x in (390, 520):
            d.ellipse(x, 330, 30, 36, fill=WHITE, outline=LINE, width=8); d.dot(x - 12, 336, 16, LINE)
        for x in (330, 580): d.ellipse(x, 390, 34, 16, fill=BLUSH)
        d.ellipse(455, 410, 16, 18, fill=LINE)
    return d.out()


def sheep(shock):
    d = Draw(640, 520)
    for x in (200, 290, 390, 450): d.rrect(x - 18, 360, x + 18, 500, 14, fill=TYRE, outline=LINE, width=6)
    P_ = ((200, 290, 92), (300, 236, 100), (400, 276, 96), (330, 336, 108), (220, 350, 80), (440, 344, 80))
    for x, y, r in P_: d.dot(x, y, r + 12, LINE)
    for x, y, r in P_: d.dot(x, y, r, (250, 248, 240, 255))
    for sg in (-1, 1): d.ellipse(520 + sg * 80, 196, 44, 20, fill=(56, 50, 58, 255), outline=LINE, width=8)
    d.ellipse(520, 230, 72, 88, fill=(56, 50, 58, 255), outline=LINE, width=12)
    for x, y in ((496, 150), (530, 142), (556, 156)): d.dot(x, y, 24, (250, 248, 240, 255))
    r_ = 24 if shock else 18
    for x in (494, 546):
        d.ellipse(x, 222, r_, r_ + 4, fill=WHITE, outline=LINE, width=5); d.dot(x + 2, 226, r_ * 0.5, LINE)
    if shock: d.ellipse(520, 284, 14, 18, fill=(230, 120, 140, 255), outline=WHITE, width=4)
    else: d.arc(520, 270, 18, 12, 20, 160, WHITE, 6)
    return d.out()


def compass():
    d = Draw(700, 700); d.dot(350, 350, 336, LINE); d.dot(350, 350, 320, BRASS); d.dot(350, 350, 272, LINE); d.dot(350, 350, 262, CREAM)
    for a in range(0, 360, 15):
        r0, ra = (196 if a % 90 == 0 else 226), math.radians(a)
        d.stroke([(350 + r0 * math.sin(ra), 350 - r0 * math.cos(ra)), (350 + 250 * math.sin(ra), 350 - 250 * math.cos(ra))], LINE, 10 if a % 45 == 0 else 5)
    for t, x, y in (('N', 350, 152), ('E', 548, 350), ('S', 350, 548), ('W', 152, 350)): d.text(x, y, t, 76, RED if t == 'N' else LINE)
    return d.out()


def needle():
    d = Draw(700, 700); d.poly([(350, 196), (390, 350), (310, 350)], fill=RED, outline=LINE, width=10)
    d.poly([(350, 504), (390, 350), (310, 350)], fill=WHITE, outline=LINE, width=10); d.dot(350, 350, 30, LINE); d.dot(350, 350, 18, BRASS); return d.out()


def tank():
    d = Draw(640, 820); d.rrect(70, 90, 570, 770, 120, fill=SILVER, outline=LINE, width=16); d.rrect(122, 160, 200, 700, 36, fill=(238, 242, 248, 255))
    for y in (230, 680):
        d.stroke([(80, y), (560, y)], dk(SILVER, 0.75), 10)
        for x in range(150, 520, 60): d.dot(x, y, 8, dk(SILVER, 0.6))
    d.rrect(176, 350, 480, 530, 24, fill=RED, outline=LINE, width=10); d.text(328, 440, 'GAS', 110, WHITE, stroke=6, stroke_fill=LINE)
    d.rrect(272, 40, 372, 100, 12, fill=BRASS, outline=LINE, width=10); return d.out()


def gasoline():
    d = Draw(1400, 420); wave = [(x, 120 + 22 * math.sin(x / 70.0)) for x in range(0, 1401, 20)]
    d.poly(wave + [(1400, 420), (0, 420)], fill=GAS); d.stroke(wave, LINE, 12)
    for k, col in enumerate(((255, 120, 200, 160), (120, 200, 255, 160))): d.stroke([(x, y + 36 + 18 * k) for x, y in wave[8:42]], col, 10)
    for x, y, r in ((300, 240, 24), (520, 300, 16), (900, 260, 20), (1150, 320, 14)): d.ellipse(x, y, r, r, outline=(255, 255, 255, 220), width=6)
    return d.out()


def screwdriver():
    d = Draw(300, 900); d.rrect(130, 360, 170, 830, 10, fill=SILVER, outline=LINE, width=8)
    d.poly([(130, 822), (170, 822), (158, 884), (142, 884)], fill=dk(SILVER), outline=LINE, width=8)
    d.rrect(80, 30, 220, 380, 60, fill=GOLD, outline=LINE, width=14)
    for x in (122, 150, 178): d.stroke([(x, 80), (x, 330)], dk(GOLD, 0.8), 10)
    return d.out()


def liner():                                                # ocean liner, bow right, waterline at y 640 of 760
    d = Draw(1700, 760)
    for x in (640, 900): d.rrect(x - 60, 70, x + 60, 262, 16, fill=RED, outline=LINE, width=14); d.rect(x - 50, 80, x + 50, 122, (40, 36, 44, 255))
    d.rrect(380, 240, 1180, 330, 16, fill=WHITE, outline=LINE, width=14); d.rrect(280, 320, 1340, 420, 16, fill=WHITE, outline=LINE, width=14)
    for x in range(330, 1300, 50): d.dot(x, 370, 13, GLASS)
    for x in range(440, 1140, 60): d.rect(x, 268, x + 34, 302, GLASS)
    d.poly([(60, 400), (1640, 380), (1500, 740), (170, 740)], fill=(44, 46, 60, 255), outline=LINE, width=16)
    d.poly([(138, 640), (1539, 640), (1500, 740), (170, 740)], fill=(196, 56, 52, 255)); d.stroke([(66, 432), (1628, 414)], WHITE, 10)
    for x in range(260, 1500, 90): d.dot(x, 520, 14, (240, 230, 200, 255))
    return d.out()


def car():                                                  # 1930s open parade car, nose right
    d = Draw(1400, 600); BODY = (200, 44, 56, 255)
    for x in (330, 1060): d.ellipse(x, 470, 112, 112, fill=TYRE, outline=LINE, width=14); d.ellipse(x, 470, 70, 70, fill=WHITE, outline=LINE, width=8); d.dot(x, 470, 30, SILVER)
    d.rrect(200, 180, 470, 290, 40, fill=(70, 40, 40, 255), outline=LINE, width=12)
    d.poly([(820, 262), (760, 110), (790, 104), (860, 262)], fill=(200, 230, 250, 150), outline=LINE, width=10)
    d.rrect(80, 260, 1300, 420, 60, fill=BODY, outline=LINE, width=16); d.rrect(840, 226, 1320, 330, 40, fill=BODY, outline=LINE, width=14)
    for x in (330, 1060): d.chord(x, 420, 160, 120, 180, 360, fill=dk(BODY), outline=LINE, width=14)
    d.rrect(1296, 236, 1340, 410, 14, fill=SILVER, outline=LINE, width=10); d.dot(1290, 236, 30, GOLD); d.ellipse(1290, 236, 30, 30, outline=LINE, width=8)
    d.stroke([(120, 300), (1260, 300)], (255, 236, 200, 255), 8); d.rect(470, 420, 900, 446, (60, 56, 64, 255)); return d.out()


def tape():
    d = Draw(700, 900); R_ = np.random.RandomState(7); cols = (WHITE, (255, 240, 150, 255), (255, 182, 200, 255), (170, 214, 255, 255), (190, 240, 190, 255))
    for k in range(34):
        x, y, a, L_ = R_.uniform(50, 650), R_.uniform(50, 850), R_.uniform(0, math.pi), R_.uniform(26, 60); dx, dy = L_ * math.cos(a), L_ * math.sin(a)
        d.stroke([(x - dx, y - dy), (x + dx, y + dy)], LINE, 24); d.stroke([(x - dx, y - dy), (x + dx, y + dy)], cols[k % 5], 14)
    for k, x0 in enumerate((140, 330, 520)):
        pts = [(x0 + 34 * math.sin(t * 0.45), 60 + t * 19) for t in range(40)]; d.stroke(pts, LINE, 18); d.stroke(pts, cols[(k + 1) % 5], 10)
    return d.out()


def signpost():
    d = Draw(1000, 1200); d.rrect(470, 120, 530, 1180, 18, fill=(150, 104, 62, 255), outline=LINE, width=12)
    for y, txt, col, tc, pts in ((280, 'IRELAND', GREEN, WHITE, [(110, 200), (840, 200), (960, 280), (840, 360), (110, 360)]),
                                 (540, 'CALIFORNIA', GOLD, LINE, [(890, 460), (160, 460), (40, 540), (160, 620), (890, 620)])):
        d.poly(pts, fill=col, outline=LINE, width=14); d.text(510 if col == GREEN else 490, y, txt, 92, tc, stroke=5 if tc == WHITE else 0, stroke_fill=LINE)
    return d.out()


def windsock():
    d = Draw(700, 1000); d.rrect(80, 100, 112, 994, 12, fill=SILVER, outline=LINE, width=8)
    for k in range(5):
        xa, ha, hb = 112 + k * 112, 100 - k * 10, 90 - k * 10
        d.poly([(xa, 200 - ha), (xa + 112, 216 - hb), (xa + 112, 216 + hb), (xa, 200 + ha)], fill=(244, 120, 44, 255) if k % 2 == 0 else WHITE, outline=LINE, width=8)
    return d.out()


def stamp(txt, w, size=100):
    d = Draw(w, 250); d.rrect(14, 14, w - 14, 236, 26, fill=(255, 250, 244, 225), outline=STAMP, width=20); d.rrect(42, 42, w - 42, 208, 14, outline=STAMP, width=6)
    d.text(w / 2, 126, txt, size, STAMP); return d.out()


def price():
    d = Draw(760, 440); d.poly([(150, 40), (720, 40), (720, 400), (150, 400), (30, 220)], fill=CREAM, outline=LINE, width=16)
    d.ellipse(118, 220, 28, 28, fill=WHITE, outline=LINE, width=8); d.text(440, 186, '$900', 150, (36, 130, 70, 255), stroke=8, stroke_fill=LINE)
    d.text(440, 330, 'USED', 62, LINE); return d.out()


def plan():
    d = G.card(800, 560); d.text(400, 100, 'FLIGHT PLAN', 74, LINE); d.stroke([(90, 160), (710, 160)], LINE, 8)
    d.text(400, 250, 'FROM: NEW YORK', 54, GREY); d.text(400, 330, 'TO:', 54, GREY); d.text(400, 432, 'LONG BEACH', 100, BLUE, stroke=6, stroke_fill=LINE)
    return d.out()


def licence():
    d = G.card(860, 520); d.text(590, 120, 'PILOT', 80, LINE); d.text(590, 210, 'LICENSE', 80, LINE)
    for y in (310, 370, 430): d.stroke([(440, y), (760, y)], (176, 182, 196, 255), 14)
    return framed_face(d.out(), (90, 90, 370, 440), 20, 'happy', 1.15, 0.55)


def lindy():
    d = G.card(900, 520); d.text(450, 96, 'PARADE CROWD', 64, LINE)
    for y, nm, w_, col in ((240, 'LINDBERGH', 430, (150, 156, 170, 255)), (390, 'CORRIGAN', 740, GOLD)):
        d.rrect(80, y - 56, 80 + w_, y + 56, 26, fill=col, outline=LINE, width=10); d.text(80 + w_ / 2, y, nm, 54, WHITE, stroke=5, stroke_fill=LINE)
    return d.out()


def wwc():
    d = G.card(1000, 440); d.text(500, 140, 'WRONG WAY', 128, RED, stroke=8, stroke_fill=LINE); d.text(500, 310, 'CORRIGAN', 128, BLUE, stroke=8, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ skies, textures, panels
def gradient(top, bot, W=1800, Hh=800, k=1.4):
    y = np.linspace(0, 1, Hh)[:, None, None]; top, bot = np.array(top), np.array(bot)
    return Image.fromarray((top + (bot - top) * y ** k * np.ones((1, W, 1))).astype(np.uint8))


def towers(dr, base, col, lit, W, seed, hmin=120, hmax=420):
    R_, x = np.random.RandomState(seed), 0
    while x < W:
        w, h = int(R_.uniform(50, 120)), int(R_.uniform(hmin, hmax)); dr.rectangle([x, base - h, x + w, base], fill=col)
        if R_.rand() < 0.3:                                 # setback tower with a spire
            dr.rectangle([x + w * 0.2, base - h - 70, x + w * 0.8, base - h], fill=col); dr.polygon([(x + w * 0.4, base - h - 70), (x + w * 0.5, base - h - 190), (x + w * 0.6, base - h - 70)], fill=col)
        if lit:
            for yy in range(base - h + 16, base - 10, 26):
                for xx in range(x + 10, x + w - 10, 20):
                    if R_.rand() < 0.35: dr.rectangle([xx, yy, xx + 7, yy + 10], fill=lit)
        x += w + int(R_.uniform(2, 14))


def skyny(path):                                            # New York at dawn
    im = gradient((84, 92, 170), (255, 178, 116)); dr = ImageDraw.Draw(im); dr.ellipse([1020, 540, 1300, 820], fill=(255, 224, 140))
    towers(dr, 800, (78, 64, 108), (255, 214, 130), 1800, 3); im.save(path)


def skyst(path):                                            # far end of the parade street
    im = gradient((126, 176, 236), (232, 238, 248)); dr = ImageDraw.Draw(im); towers(dr, 800, (150, 160, 190), None, 1800, 9, 200, 560); im.save(path)


def backdrop(path):                                         # open sky over the Atlantic, puffy clouds, sea horizon
    W, Hh = 2520, 1080; im = gradient((70, 132, 222), (214, 232, 250), W, Hh, 1.2); dr = ImageDraw.Draw(im, 'RGBA'); R_ = np.random.RandomState(5)
    for k in range(16):
        cx, cy, s = R_.uniform(0, W), R_.uniform(260, 900), R_.uniform(0.5, 1.2)
        for j in range(7):
            x, y, r = cx + R_.uniform(-150, 150) * s, cy + R_.uniform(-40, 30) * s, R_.uniform(50, 100) * s
            dr.ellipse([x - r, y - r, x + r, y + r * 0.8], fill=(255, 255, 255, 170))
    dr.rectangle([0, 990, W, Hh], fill=(52, 104, 168, 255)); im.save(path, quality=92)


def facade(path, n=256):
    im = Image.new('RGB', (n, n), (184, 122, 96)); dr = ImageDraw.Draw(im)
    for y in range(0, n, 16): dr.line([(0, y), (n, y)], fill=(166, 106, 82), width=2)
    dr.rectangle([56, 44, 200, 212], fill=(236, 226, 206)); dr.rectangle([68, 56, 188, 196], fill=(66, 92, 138))
    dr.polygon([(68, 196), (188, 80), (188, 120), (108, 196)], fill=(98, 130, 176)); dr.line([(128, 56), (128, 196)], fill=(236, 226, 206), width=8)
    dr.rectangle([48, 212, 208, 224], fill=(220, 210, 190)); im.save(path, quality=92)


def dash(path):
    d = Draw(1200, 420); d.rrect(10, 10, 1190, 410, 40, fill=(92, 60, 40, 255), outline=LINE, width=14)
    for k, x in enumerate((170, 430, 690, 950)):
        d.ellipse(x + 60, 210, 110, 110, fill=(30, 28, 34, 255), outline=SILVER, width=12); d.ellipse(x + 60, 210, 84, 84, fill=CREAM)
        a = math.radians(-60 + k * 50); d.stroke([(x + 60, 210), (x + 60 + 70 * math.sin(a), 210 - 70 * math.cos(a))], RED, 10); d.dot(x + 60, 210, 10, LINE)
    d.out().save(path)


def tex_ocean(path, n=512):
    p, q = G.periodic(n, 9, 7), G.periodic(n, 3, 13); a = np.zeros((n, n, 3)) + [44, 112, 182]
    a += (p[..., None] - 0.5) * 34 + (q[..., None] - 0.5) * 20 + (np.clip(p - 0.76, 0, 1) * 4)[..., None] * [120, 130, 120]
    G.save_tex(a, path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = G.head, G.body              # the same faces as videos 02-04
    for ch in ('mom', 'dad', 'tech'): layers, faces = B.build_human(ch); items.append((ch, faces['happy']))
    B.human_head, B.human_body = V.head, V.body
    layers, faces = B.build_human('vik'); items.append(('vik', faces['happy']))
    B.human_head, B.human_body = VA.head, VA.body
    for ch in ('sailA', 'sailC', 'sailD', 'capt'): layers, faces = B.build_human(ch); items.append((ch, faces['happy']))
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'sneaky', 'confused')]
    multi = dict(robin={s: robin(s) for s in ('default', 'fly', 'drip')}, cloud={'default': cloud(False), 'face': cloud(True)},
                 sheep={'default': sheep(False), 'shocked': sheep(True)})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    B.sparkle(Pp('sparkle.png'))
    cards = dict(compass=compass(), needle=needle(), tank=tank(), gasoline=gasoline(), screwdriver=screwdriver(), liner=liner(), car=car(), tape=tape(),
                 signpost=signpost(), windsock=windsock(), price=price(), plan=plan(), licence=licence(), lindy=lindy(), sun=VA.sun(),
                 banned=stamp('BANNED!', 660, 112), unsound=stamp('TOO UNSOUND!', 900, 96), denied=stamp('DENIED', 580, 112),
                 susp=stamp('SUSPENDED', 800, 104), official=stamp('OFFICIAL', 680, 108),
                 dublin=V.wtag('DUBLIN?!', 560, GREEN), robtag=V.big_card('1929', 'CURTISS ROBIN', BLUE, 760), noview=V.wtag('NO FRONT VIEW!', 900, PURP, 72),
                 gas=B.sticker_burst('GAS!', (196, 230, 84, 255)), punch=B.sticker_burst('PUNCH!'), kept=V.wtag('KEPT FLYING!', 780, GREEN, 76),
                 name=V.wtag('DOUGLAS CORRIGAN', 1040, BLUE, 72), cal38=G.cal_card('JULY 17', '1938', ''), clock=V.big_card('28:13', 'HOURS : MINUTES', PURP, 760),
                 wrong=V.wtag('WRONG END!', 740, RED), badvis=V.wtag('BAD VISIBILITY', 880, GREY, 70), parade=V.wtag('TICKER-TAPE PARADE!', 1120, RED, 74),
                 wwc=wwc(), purpose=V.wtag('ON PURPOSE?', 800, PURP), ques=B.sticker_mark('?', GOLD),
                 poof=B.sticker_poof(), hearts=G.hearts(), sparkle=Image.open(Pp('sparkle.png')).convert('RGBA'))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); B.tex_grass(T('grass.jpg')); tex_ocean(T('water.jpg')); facade(T('facade.jpg'))
    backdrop(os.path.join(ROOT, 'bg', 'sky38.jpg'))
    skyny(Pp('skyny.png')); skyst(Pp('skyst.png')); VA.skyplane(Pp('skyie.png'), (104, 166, 232), (222, 238, 250), (104, 170, 92)); dash(Pp('dash.png'))
    for n in ('skyny', 'skyst', 'skyie', 'dash'): items.append((n, Image.open(Pp(n + '.png'))))
    items.append(('backdrop', Image.open(os.path.join(ROOT, 'bg', 'sky38.jpg'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
