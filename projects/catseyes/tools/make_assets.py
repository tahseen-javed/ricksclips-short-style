#!/usr/bin/env python3
"""Assets for video 08 (Cat's Eyes Cunningham and the carrot lie), drawn in code with the channel builders.
New cast (all cute, big heads): John the night pilot (leather helmet, green goggles, sheepskin jacket), Jimmy the radar
operator (side cap + headphones), a newsboy, a 1940s lady reader, an RAF mess cook, a bowler-hat ministry man, a farmer,
an optician, a historian, a German commander (grey, monocle, no insignia), and a mum + kid of today.  Cute props: the
Beaufighter night fighter with a face (parked / x-ray / flying), grumpy bombers, a radar set with a glowing scope face, a
medal-wearing carrot, Doctor Carrot, carrot fudge, a carrot mountain, a newspaper, three wartime posters.  Sets: night
airfield + hangar, Blitz London at night, a sandbagged street with a newsagent, the RAF mess, the radar fuselage, a
poster wall, a farm, an optician, a library, a German HQ, a kitchen of today.
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
NAVY, ORANGE, CREAM, GLASS, SILVER = (40, 58, 120, 255), (246, 132, 40, 255), (250, 238, 206, 255), (170, 222, 244, 255), (206, 212, 224, 255)
LEAF, OLIVE, SCOPE, PURPLE = (92, 176, 74, 255), (118, 132, 92, 255), (140, 255, 176, 255), (126, 70, 140, 255)
FLEECE = (244, 230, 200, 255)
NEW = {
    'john': dict(sk=0, style='flyhelm', hair=(64, 42, 36, 255), hc=(98, 62, 44, 255), suit=(132, 84, 54, 255), shade=(104, 62, 40, 255), body='irvin'),
    'jimmy': dict(sk=1, style='phones', hair=(176, 112, 62, 255), hc=(78, 98, 138, 255), suit=(100, 122, 160, 255), shade=(78, 96, 132, 255), body='tunic', freck=1),
    'newsboy': dict(sk=0, style='flat', hair=(214, 120, 56, 255), hc=(150, 128, 100, 255), suit=(246, 238, 216, 255), shade=(216, 206, 184, 255), body='braces', freck=1),
    'reader': dict(sk=2, style='scarf', hair=(66, 42, 40, 255), hc=(222, 56, 66, 255), suit=(82, 156, 114, 255), shade=(60, 124, 90, 255), body='coat40'),
    'cook': dict(sk=1, style='chef', hair=(120, 80, 50, 255), suit=(250, 250, 246, 255), shade=(214, 214, 222, 255), body='chef', stache=(120, 80, 50, 255)),
    'minister': dict(sk=0, style='bowler', hair=(150, 150, 158, 255), hc=(52, 50, 62, 255), suit=(88, 92, 110, 255), shade=(66, 68, 86, 255), body='pin', glasses=1,
                     stache=(150, 150, 158, 255)),
    'farmer': dict(sk=1, style='straw', hair=(150, 96, 56, 255), hc=(238, 206, 122, 255), suit=(214, 72, 72, 255), shade=(180, 52, 58, 255), body='dung'),
    'doctor': dict(sk=2, style='mirror', hair=(44, 36, 42, 255), suit=(248, 250, 252, 255), shade=(214, 220, 232, 255), body='whitecoat', glasses=1),
    'historian': dict(sk=0, style='bald', hair=(236, 236, 242, 255), suit=(156, 108, 72, 255), shade=(126, 84, 56, 255), body='tweed', glasses=1,
                      stache=(236, 236, 242, 255)),
    'german': dict(sk=0, style='peak', hair=(204, 172, 112, 255), hc=(112, 124, 106, 255), suit=(122, 132, 116, 255), shade=(94, 104, 90, 255), body='grey', mono=1,
                   handle=(204, 172, 112, 255)),
    'mom': dict(sk=1, style='pony', hair=(116, 62, 42, 255), suit=(246, 124, 112, 255), shade=(216, 94, 88, 255), body='cardi'),
    'max': dict(sk=2, style='spiky', hair=(44, 32, 36, 255), suit=(252, 212, 72, 255), shade=(222, 178, 42, 255), body='stripes', freck=1),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; st, hr = c['style'], c.get('hair')
    skin, sh = SK[c['sk']]
    if st == 'pony':                                         # ponytail behind the head
        d.poly(bez((cx + 150, cy - 120), (cx + 290, cy - 160), (cx + 250, cy + 60), (cx + 200, cy + 130)) + [(cx + 120, cy - 60)], fill=hr, outline=LINE, width=lw)
    if st == 'scarf': d.ellipse(cx, cy - 20, R + 26, R + 10, fill=c['hc'], outline=LINE, width=lw)
    d.ellipse(cx, cy, R, R, fill=skin, outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, sh, skin)
    if st in ('phones', 'flat', 'chef', 'bowler', 'mirror', 'peak', 'pony', 'straw'):
        d.chord(cx, cy - 66, R + 8, 132, 180, 360, fill=hr, outline=LINE, width=lw)
    if st == 'flyhelm':                                      # leather flying helmet, green goggles up, side-swept fringe
        hc = c['hc']
        d.poly([(cx - 176, 176), (cx + 160, 150), (cx + 130, 200), (cx + 50, 182), (cx - 20, 222), (cx - 90, 192), (cx - 160, 224)], fill=hr, outline=LINE, width=9)
        for sg in (-1, 1): d.rrect(cx + sg * 192 - 36, cy - 84, cx + sg * 192 + 36, cy + 90, 32, fill=hc, outline=LINE, width=lw)
        d.chord(cx, 172, 218, 154, 180, 360, fill=hc, outline=LINE, width=lw); d.arc(cx, 172, 196, 132, 200, 340, (150, 104, 76, 255), 8)
        d.stroke(bez((cx, 22), (cx + 6, 70), (cx + 4, 120), (cx, 168)), dk(hc, 0.7), 10)
        d.rrect(cx - 216, 96, cx + 216, 130, 16, fill=(58, 44, 40, 255), outline=LINE, width=10)
        for sg in (-1, 1):
            d.rrect(cx + sg * 82 - 66, 74, cx + sg * 82 + 66, 150, 30, fill=SILVER, outline=LINE, width=12)
            d.rrect(cx + sg * 82 - 48, 88, cx + sg * 82 + 48, 136, 22, fill=(130, 222, 186, 255), outline=LINE, width=6); d.dot(cx + sg * 82 - 22, 100, 9, WHITE)
    elif st == 'phones':                                     # RAF side cap + radio headphones
        d.arc(cx, cy - 10, R + 18, R + 6, 200, 340, (60, 60, 70, 255), 22)
        for sg in (-1, 1): d.rrect(cx + sg * 204 - 34, cy - 50, cx + sg * 204 + 34, cy + 56, 26, fill=(70, 70, 82, 255), outline=LINE, width=12)
        d.poly([(cx - 150, 112), (cx + 110, 70), (cx + 170, 96), (cx + 120, 134), (cx - 140, 150)], fill=c['hc'], outline=LINE, width=12)
        d.dot(cx - 100, 128, 13, GOLD)
    elif st == 'flat':                                       # tweed flat cap
        hc = c['hc']; d.chord(cx, 150, 214, 120, 180, 360, fill=hc, outline=LINE, width=lw)
        d.poly([(cx - 40, 140), (cx + 230, 132), (cx + 216, 172), (cx - 20, 170)], fill=dk(hc, 0.8), outline=LINE, width=12)
        for x in range(-150, 160, 50): d.stroke([(cx + x, 60), (cx + x + 10, 140)], dk(hc, 0.85), 6)
        for sg in (-1, 1): d.ellipse(cx + sg * 190, cy - 20, 30, 40, fill=hr, outline=LINE, width=9)
    elif st == 'scarf':                                      # polka-dot headscarf, knot on top, victory-roll fringe
        hc = c['hc']; d.chord(cx, 160, 214, 140, 180, 360, fill=hc, outline=LINE, width=lw)
        for x, y in ((-120, 110), (-40, 70), (50, 76), (130, 110), (-80, 140), (90, 140), (0, 120)): d.dot(cx + x, y, 14, WHITE)
        for sg in (-1, 1): d.ellipse(cx + sg * 44, 18, 46, 30, fill=hc, outline=LINE, width=10)
        d.dot(cx, 26, 20, dk(hc, 0.8))
        for x in (-90, 0, 90): d.ellipse(cx + x, 172, 52, 34, fill=hr, outline=LINE, width=9)
    elif st == 'chef':                                       # puffy chef's toque
        for x, y, r in ((-90, 40, 70), (0, 10, 84), (90, 40, 70), (-40, 60, 70), (50, 60, 70)): d.ellipse(cx + x, y, r, r, fill=WHITE, outline=LINE, width=12)
        for x, y, r in ((-90, 40, 58), (0, 10, 72), (90, 40, 58), (-40, 60, 60), (50, 60, 60)): d.ellipse(cx + x, y, r, r, fill=WHITE)
        d.rrect(cx - 150, 96, cx + 150, 156, 18, fill=WHITE, outline=LINE, width=12)
    elif st == 'bowler':
        hc = c['hc']; d.ellipse(cx, 150, 232, 38, fill=dk(hc, 0.9), outline=LINE, width=lw); d.chord(cx, 142, 150, 130, 180, 360, fill=hc, outline=LINE, width=lw)
        d.rect(cx - 140, 112, cx + 140, 136, (120, 40, 50, 255)); d.arc(cx - 40, 80, 60, 40, 200, 260, (110, 110, 124, 255), 10)
    elif st == 'straw':                                      # floppy wide straw hat with a green band
        hc = c['hc']; d.ellipse(cx, 150, 262, 50, fill=dk(hc, 0.9), outline=LINE, width=lw); d.chord(cx, 150, 160, 120, 180, 360, fill=hc, outline=LINE, width=lw)
        d.rect(cx - 152, 118, cx + 152, 146, (70, 140, 70, 255))
        for x in range(-140, 150, 36): d.stroke([(cx + x, 40), (cx + x + 6, 118)], dk(hc, 0.85), 5)
    elif st == 'mirror':                                     # optician's head mirror
        d.rrect(cx - 206, 112, cx + 206, 140, 12, fill=(60, 60, 72, 255), outline=LINE, width=8)
        d.ellipse(cx + 60, 104, 62, 62, fill=SILVER, outline=LINE, width=12); d.ellipse(cx + 60, 104, 22, 22, fill=(90, 96, 110, 255)); d.dot(cx + 40, 84, 12, WHITE)
    elif st == 'bald':                                       # bald dome, cloud tufts
        d.ellipse(cx - 60, 120, 60, 26, fill=(255, 255, 255, 110))
        for sg in (-1, 1):
            for dx, dy in ((0, 0), (14, 44), (-6, 86)): d.ellipse(cx + sg * (200 + dx), cy - 70 + dy, 36, 32, fill=hr, outline=LINE, width=9)
    elif st == 'peak':                                       # grey peaked cap, silver cord, plain round cockade
        hc = c['hc']; d.poly([(cx - 190, 140), (cx - 230, 50), (cx, 6), (cx + 230, 50), (cx + 190, 140)], fill=hc, outline=LINE, width=lw)
        d.rrect(cx - 196, 110, cx + 196, 160, 14, fill=dk(hc, 0.7), outline=LINE, width=12); d.stroke([(cx - 180, 128), (cx + 180, 128)], SILVER, 8)
        d.chord(cx, 160, 170, 46, 0, 180, fill=(34, 34, 40, 255), outline=LINE, width=12); d.ellipse(cx, 136, 20, 20, fill=SILVER, outline=LINE, width=6)
    elif st == 'pony':
        d.poly([(cx - 190, 200), (cx - 150, 120), (cx - 60, 196), (cx - 20, 120), (cx + 60, 190), (cx + 120, 130), (cx + 200, 210), (cx + 170, 110), (cx - 170, 110)], fill=hr)
        d.dot(cx + 170, cy - 130, 22, (250, 210, 80, 255))
    elif st == 'spiky':
        d.poly([(cx - 200, 220)] + [(cx - 200 + k * 50 + 25, 40 if k % 2 == 0 else 110) for k in range(8)] + [(cx + 200, 220), (cx + 140, 150), (cx - 140, 150)], fill=hr, outline=LINE, width=10)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 30, 17, fill=BLUSH)
    if c.get('freck'):
        for sg in (-1, 1):
            for dx, dy in ((-14, 0), (8, -10), (10, 12)): d.dot(cx + sg * 108 + dx, cy + 12 + dy, 5, (196, 120, 90, 255))
    B.eyes(d, L, Rr, expr, skin); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses'):
        for p in (L, Rr): d.ellipse(p[0], p[1], 50, 46, outline=LINE, width=9)
        d.stroke([(L[0] + 50, ey), (Rr[0] - 50, ey)], LINE, 9)
    if c.get('mono'):
        d.ellipse(Rr[0], Rr[1], 52, 52, outline=(220, 200, 120, 255), width=10); d.ellipse(Rr[0], Rr[1], 58, 58, outline=LINE, width=5)
        d.stroke(bez((Rr[0] + 50, ey + 20), (Rr[0] + 80, ey + 90), (Rr[0] + 60, ey + 160), (Rr[0] + 30, ey + 210)), (220, 200, 120, 255), 5)
    my = cy + 74
    if c.get('stache'):
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 34, my - 52), (cx + sg * 62, my - 40), (cx + sg * 72, my - 58)), c['stache'], 20)
        my += 12
    if c.get('handle'):                                      # curly handlebar moustache
        for sg in (-1, 1): d.stroke(bez((cx, my - 30), (cx + sg * 60, my - 50), (cx + sg * 100, my - 30), (cx + sg * 96, my - 66)), c['handle'], 18); d.ellipse(cx + sg * 90, my - 70, 12, 12, outline=c['handle'], width=8)
        my += 12
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']; base = c['suit']; bs = c['body']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=base)
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=base); d.clip(sh, mask)
    t = Draw(d.w, d.h)

    def lapels(col):
        for sg in (-1, 1):
            lap = [(230 + sg * 64, 452), (230 + sg * 16, 604), (230 + sg * 84, 540), (230 + sg * 108, 456)]; t.poly(lap, fill=col); t.stroke(lap, LINE, 7)

    def tie(col, shirt=WHITE):
        t.poly([(166, 452), (294, 452), (230, 600)], fill=shirt); tt = [(230, 474), (208, 500), (214, 626), (230, 650), (246, 626), (252, 500)]; t.poly(tt, fill=col); t.stroke(tt + [tt[0]], LINE, 6)

    if bs == 'irvin':                                        # sheepskin flying jacket, zip, pilot wings
        t.stroke([(230, 470), (230, 800)], dk(base, 0.65), 9)
        for x in (150, 310): t.rrect(x - 44, 640, x + 44, 716, 12, fill=dk(base, 0.9), outline=LINE, width=6)
        t.rect(0, 760, 460, 800, FLEECE); t.stroke([(0, 760), (460, 760)], LINE, 7)
        t.poly([(110, 560), (150, 548), (190, 560), (150, 572)], fill=GOLD, outline=LINE, width=5); t.dot(150, 560, 12, WHITE)
    elif bs == 'tunic':                                      # RAF blue tunic, tie, pockets, belt, brass buttons
        tie((40, 44, 60, 255), (190, 214, 240, 255)); lapels(dk(base, 0.88))
        for x in (150, 310): t.rrect(x - 46, 610, x + 46, 680, 10, fill=dk(base, 0.9), outline=LINE, width=6); t.dot(x, 626, 8, GOLD)
        t.rect(0, 728, 460, 760, dk(base, 0.75)); t.rrect(212, 724, 248, 764, 6, fill=GOLD, outline=LINE, width=6)
    elif bs == 'braces':                                     # newsboy: shirt, braces, satchel strap
        for x in (170, 290): t.rect(x - 14, 452, x + 14, 800, (120, 70, 44, 255))
        t.stroke([(110, 480), (360, 760)], (150, 104, 60, 255), 26); t.stroke([(110, 480), (360, 760)], LINE, 4)
        t.rrect(196, 452, 264, 488, 14, fill=(214, 60, 70, 255), outline=LINE, width=6)
    elif bs == 'coat40':                                     # belted 1940s coat
        lapels(dk(base, 0.86)); t.poly([(166, 452), (294, 452), (230, 560)], fill=CREAM)
        t.rect(0, 680, 460, 716, dk(base, 0.7)); t.rrect(206, 674, 254, 722, 8, outline=GOLD, width=8)
        for y in (620, 760): t.ellipse(262, y, 13, 13, fill=dk(base, 0.6), outline=LINE, width=5)
    elif bs == 'chef':                                       # double-breasted whites, red neckerchief, apron
        t.poly([(176, 452), (284, 452), (230, 540)], fill=(220, 50, 56, 255), outline=LINE, width=6)
        for x in (180, 280):
            for y in (560, 620): t.dot(x, y, 9, (150, 150, 160, 255))
        t.rrect(130, 660, 330, 840, 24, fill=(236, 236, 230, 255), outline=LINE, width=7)
    elif bs == 'pin':                                        # pinstripe suit, red tie, pocket square
        for x in range(60, 420, 30): t.stroke([(x, 452), (x, 800)], dk(base, 1.25), 3)
        tie((200, 40, 50, 255)); lapels(dk(base, 0.86)); t.poly([(296, 560), (336, 552), (330, 580)], fill=WHITE, outline=LINE, width=5)
    elif bs == 'dung':                                       # check shirt + denim dungarees
        for x in range(70, 420, 44): t.stroke([(x, 452), (x, 800)], (250, 230, 220, 255), 6)
        for y in range(470, 800, 44): t.stroke([(60, y), (400, y)], (250, 230, 220, 255), 6)
        DEN = (70, 112, 180, 255)
        for sg in (-1, 1): t.stroke([(230 + sg * 70, 452), (230 + sg * 64, 600)], DEN, 26)
        t.rrect(140, 590, 320, 840, 22, fill=DEN, outline=LINE, width=7); t.rrect(190, 630, 270, 690, 10, outline=LINE, width=5)
        for x in (160, 300): t.dot(x, 606, 10, GOLD)
    elif bs == 'whitecoat':                                  # optician's coat, tie, stethoscope
        tie(NAVY, (190, 214, 240, 255)); lapels(dk(base, 0.92))
        t.stroke(bez((170, 456), (150, 560), (200, 640), (230, 640)), (90, 96, 110, 255), 10); t.stroke(bez((290, 456), (310, 560), (260, 640), (230, 640)), (90, 96, 110, 255), 10)
        t.ellipse(230, 650, 22, 22, fill=SILVER, outline=LINE, width=6); t.rrect(290, 560, 340, 620, 6, outline=LINE, width=5); t.rect(300, 540, 308, 580, BLUE)
    elif bs == 'tweed':                                      # tweed jacket, red bow tie
        R_ = np.random.RandomState(4)
        for _ in range(140): t.dot(R_.uniform(60, 400), R_.uniform(452, 800), 4, dk(base, 0.75))
        t.poly([(166, 452), (294, 452), (230, 600)], fill=CREAM); lapels(dk(base, 0.86))
        for sg in (-1, 1): t.poly([(230, 478), (230 + sg * 46, 456), (230 + sg * 46, 504)], fill=RED, outline=LINE, width=6)
        t.ellipse(230, 480, 14, 14, fill=RED, outline=LINE, width=6)
    elif bs == 'grey':                                       # plain field-grey tunic, silver buttons, black belt (no insignia)
        t.rect(0, 452, 460, 486, dk(base, 0.7))
        for y in (540, 600, 660): t.dot(230, y, 10, SILVER)
        for x in (150, 310): t.rrect(x - 46, 560, x + 46, 626, 10, fill=dk(base, 0.9), outline=LINE, width=6)
        t.rect(0, 712, 460, 746, (36, 36, 42, 255)); t.rrect(208, 706, 252, 752, 6, fill=SILVER, outline=LINE, width=6)
    elif bs == 'cardi':                                      # open cardigan over a white tee
        t.rect(176, 452, 284, 800, WHITE); t.chord(230, 452, 54, 30, 0, 180, fill=dk(base, 1.0))
        for sg in (-1, 1): t.stroke([(230 + sg * 54, 452), (230 + sg * 54, 800)], LINE, 7)
        for y in (560, 640, 720): t.dot(296, y, 9, CREAM)
    elif bs == 'stripes':                                    # striped tee with a star
        for y in range(478, 800, 64): t.rect(0, y, 460, y + 28, (70, 140, 230, 255))
        star = [(230 + 50 * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45), 620 + 50 * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45)) for k in range(10)]
        t.poly(star, fill=WHITE, outline=LINE, width=6)
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    if bs == 'irvin':                                        # big fleece collar + white silk scarf
        for sg in (-1, 1): d.poly([(230, 476), (230 + sg * 128, 446), (230 + sg * 150, 520), (230 + sg * 40, 590)], fill=FLEECE, outline=LINE, width=10)
        d.ellipse(230, 476, 64, 30, fill=WHITE, outline=LINE, width=8); d.poly([(240, 490), (300, 500), (286, 620), (250, 600)], fill=WHITE, outline=LINE, width=8)
    return d.out()


# ------------------------------------------------------------------ cute props
def eyes2(d, pts, r, mood):
    for i, (x, y) in enumerate(pts):
        d.ellipse(x, y, r, r * 1.12, fill=WHITE, outline=LINE, width=8)
        if mood == 'angry':
            d.dot(x, y + r * 0.2, r * 0.5, LINE); d.dot(x + r * 0.15, y, r * 0.18, WHITE)
            d.stroke([(x - r * 1.1, y - r * (1.45 if i == 0 else 0.75)), (x + r * 1.1, y - r * (0.75 if i == 0 else 1.45))], LINE, 12)
        elif mood == 'shock':
            d.dot(x, y, r * 0.3, LINE); d.dot(x + r * 0.1, y - r * 0.1, r * 0.1, WHITE)
        else:
            d.dot(x + r * 0.18, y, r * 0.58, LINE); d.dot(x + r * 0.32, y - r * 0.2, r * 0.2, WHITE)


def roundel(d, x, y, s=1.0):
    for r_, col in ((58, (250, 210, 60, 255)), (50, (40, 70, 150, 255)), (32, WHITE), (16, (210, 40, 50, 255))): d.ellipse(x, y, r_ * s, r_ * s, fill=col, outline=LINE, width=6)


def glow(im, x, y, r, col, blur=30):
    g = Draw(im.width, im.height); g.ellipse(x, y, r, r, fill=col); im.alpha_composite(g.out().filter(ImageFilter.GaussianBlur(blur))); return im


def radar_box(d, x, y, s, face='happy'):                    # the AI radar set: olive box, a round green scope as its face
    d.rrect(x - 240 * s, y - 230 * s, x + 240 * s, y + 250 * s, 50 * s, fill=OLIVE, outline=LINE, width=16 * s)
    d.rrect(x - 210 * s, y - 200 * s, x + 210 * s, y + 220 * s, 36 * s, outline=dk(OLIVE, 1.25), width=8 * s)
    d.ellipse(x, y - 10 * s, 168 * s, 168 * s, fill=SILVER, outline=LINE, width=14 * s); d.ellipse(x, y - 10 * s, 140 * s, 140 * s, fill=(26, 84, 56, 255), outline=LINE, width=8 * s)
    for rr in (100, 60): d.ellipse(x, y - 10 * s, rr * s, rr * s, outline=(60, 140, 96, 255), width=4 * s)
    if face == 'wow':
        for sg in (-1, 1): d.ellipse(x + sg * 46 * s, y - 40 * s, 26 * s, 30 * s, fill=SCOPE)
        d.ellipse(x, y + 46 * s, 22 * s, 26 * s, fill=SCOPE)
    else:
        for sg in (-1, 1): d.ellipse(x + sg * 46 * s, y - 40 * s, 22 * s, 26 * s, fill=SCOPE); d.dot(x + sg * 46 * s + 8 * s, y - 50 * s, 7 * s, WHITE)
        d.arc(x, y + 20 * s, 44 * s, 30 * s, 20, 160, SCOPE, 9 * s)
    for k, (bx, by) in enumerate(((-96, 40), (90, -84), (70, 70))): d.dot(x + bx * s, y + by * s, 9 * s, SCOPE)
    for k in range(3): d.ellipse(x - 120 * s + k * 120 * s, y + 196 * s, 22 * s, 22 * s, fill=SILVER, outline=LINE, width=7 * s)


def radar(face='happy'):
    d = Draw(760, 860); d.stroke([(380, 60), (380, 300)], LINE, 14)
    for y in (70, 120): d.stroke([(310, y), (450, y)], LINE, 12)
    d.stroke([(340, 40), (380, 70), (420, 40)], LINE, 10); radar_box(d, 380, 520, 1.0, face)
    for x in (260, 500): d.rrect(x - 50, 770, x + 50, 820, 18, fill=dk(OLIVE, 0.7), outline=LINE, width=10)
    return glow(d.out(), 380, 510, 150, (120, 255, 170, 150), 26)


def beau(st='default'):                                      # Bristol Beaufighter night fighter, nose right, a face on the nose
    d = Draw(1640, 760); BODY, HI = (78, 88, 120, 255), (118, 130, 168, 255); fly = st == 'fly'
    if fly:
        for y, x0 in ((300, 0), (380, 40), (460, 10)): d.stroke([(x0, y), (x0 + 150, y)], LINE, 24); d.stroke([(x0 + 4, y), (x0 + 146, y)], WHITE, 10)
    d.poly([(170, 330), (120, 110), (250, 100), (350, 320)], fill=BODY, outline=LINE, width=14)
    for k, col in enumerate(((210, 40, 50, 255), WHITE, (40, 70, 150, 255))): d.poly([(150 + k * 34, 150), (184 + k * 34, 150), (196 + k * 34, 230), (162 + k * 34, 230)], fill=col)
    d.poly([(110, 320), (420, 316), (420, 352), (100, 350)], fill=dk(BODY, 0.85), outline=LINE, width=10)
    d.poly(bez((150, 300), (500, 250), (1000, 236), (1300, 250)) + [(1390, 300), (1410, 360), (1390, 420)] + bez((1300, 450), (900, 474), (500, 464), (150, 360)), fill=BODY, outline=LINE, width=16)
    d.stroke(bez((320, 292), (700, 264), (1000, 260), (1260, 268)), HI, 14)
    d.chord(1060, 254, 136, 76, 180, 360, fill=GLASS, outline=LINE, width=12)
    for x in (1010, 1100): d.stroke([(x, 182), (x + 14, 254)], LINE, 8)
    d.stroke([(980, 196), (1010, 236)], WHITE, 9)
    roundel(d, 640, 362, 1.1)
    if st == 'xray':                                         # cut-away: the secret radar glowing inside
        d.rrect(380, 286, 900, 448, 40, fill=(24, 30, 52, 255), outline=(255, 230, 90, 255), width=12)
        for x in (440, 840): d.stroke(bez((x, 300), (x + 10, 360), (x - 10, 400), (x, 440)), (90, 100, 130, 255), 8)
        radar_box(d, 640, 368, 0.3, 'happy'); d.stroke(bez((710, 360), (900, 330), (1200, 340), (1420, 360)), (120, 255, 170, 255), 7)
    d.poly([(640, 404), (1060, 392), (1110, 424), (620, 446)], fill=dk(BODY, 0.8), outline=LINE, width=12)
    d.rrect(860, 430, 1190, 530, 50, fill=BODY, outline=LINE, width=14); d.stroke([(900, 452), (1150, 452)], HI, 10)
    d.ellipse(1222, 480, 28, 150, fill=(230, 236, 250, 110), outline=(60, 60, 80, 150), width=6); d.dot(1206, 480, 26, (210, 40, 50, 255)); d.ellipse(1206, 480, 26, 26, outline=LINE, width=8)
    d.stroke([(1410, 360), (1490, 360)], LINE, 10); d.stroke([(1458, 318), (1494, 360), (1458, 402)], LINE, 10); d.stroke([(1440, 340), (1440, 380)], LINE, 8)
    eyes2(d, [(1240, 316), (1338, 316)], 44, 'calm'); d.chord(1292, 396, 36, 26, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=8)
    for x in (1196, 1386): d.ellipse(x, 384, 24, 13, fill=BLUSH)
    if not fly:
        d.stroke([(1020, 520), (1020, 640)], LINE, 22); d.ellipse(1020, 660, 76, 76, fill=(46, 44, 52, 255), outline=LINE, width=14); d.ellipse(1020, 660, 30, 30, fill=SILVER, outline=LINE, width=8)
        d.stroke([(220, 350), (210, 420)], LINE, 16); d.dot(210, 432, 26, (46, 44, 52, 255))
    if st == 'tally':                                        # kill marks painted under the cockpit
        for k in range(20): x = 760 + (k % 10) * 40; y = 300 + (k // 10) * 50; d.stroke([(x, y), (x + 10, y + 34)], WHITE, 9)
    return d.out()


def bomber(st='default'):                                    # grumpy grey bomber, big glass nose, nose right, no markings
    d = Draw(1500, 640); BODY = (140, 150, 132, 255)
    d.poly([(130, 300), (90, 120), (200, 110), (300, 296)], fill=BODY, outline=LINE, width=14); d.rrect(116, 140, 214, 170, 8, fill=(250, 210, 60, 255), outline=LINE, width=6)
    d.poly([(80, 300), (380, 296), (380, 330), (70, 330)], fill=dk(BODY, 0.85), outline=LINE, width=10)
    d.poly(bez((120, 290), (500, 240), (900, 226), (1180, 250)) + bez((1180, 450), (900, 470), (500, 460), (120, 340)), fill=BODY, outline=LINE, width=16)
    d.stroke(bez((300, 282), (600, 256), (900, 250), (1150, 262)), dk(BODY, 1.18), 12)
    d.poly([(560, 390), (980, 380), (1030, 410), (540, 432)], fill=dk(BODY, 0.8), outline=LINE, width=12)
    d.rrect(820, 420, 1070, 500, 40, fill=BODY, outline=LINE, width=12)
    d.ellipse(1096, 460, 24, 120, fill=(230, 236, 250, 110), outline=(60, 60, 80, 150), width=6); d.dot(1082, 460, 22, (250, 210, 60, 255)); d.ellipse(1082, 460, 22, 22, outline=LINE, width=7)
    d.ellipse(1290, 350, 150, 130, fill=GLASS, outline=LINE, width=16)
    for x in (1210, 1290, 1370): d.stroke([(x, 228), (x + 10, 474)], (120, 150, 170, 255), 6)
    eyes2(d, [(1250, 330), (1340, 330)], 38, 'angry' if st == 'default' else 'shock')
    if st == 'default': d.arc(1296, 420, 40, 22, 200, 340, LINE, 10)
    else: d.ellipse(1296, 410, 22, 28, fill=(124, 40, 62, 255), outline=LINE, width=8); G.sweat(d, 1420, 280)
    return d.out()


def carrot_body(d, x, y, s, expr, medal=False, hat=False):   # cute carrot: leafy top, big human-style eyes, blush
    for ang, L in ((-30, 170), (0, 210), (30, 170)):
        a = math.radians(ang - 90); tx, ty = x + L * s * math.cos(a), y - 230 * s + L * s * math.sin(a); nx, ny = -math.sin(a) * 34 * s, math.cos(a) * 34 * s
        if not hat or ang == 0: d.poly([(x, y - 220 * s), (x + (tx - x) * 0.5 + nx, y - 220 * s + (ty - y + 220 * s) * 0.5 + ny), (tx, ty), (x + (tx - x) * 0.5 - nx, y - 220 * s + (ty - y + 220 * s) * 0.5 - ny)], fill=LEAF, outline=LINE, width=10 * s)
    pts = bez((x - 150 * s, y - 200 * s), (x - 230 * s, y), (x - 70 * s, y + 380 * s), (x, y + 520 * s)) + bez((x, y + 520 * s), (x + 70 * s, y + 380 * s), (x + 230 * s, y), (x + 150 * s, y - 200 * s)) + bez((x + 150 * s, y - 200 * s), (x + 100 * s, y - 250 * s), (x - 100 * s, y - 250 * s), (x - 150 * s, y - 200 * s))
    d.poly(pts, fill=ORANGE, outline=LINE, width=14 * s)
    for k, (dx, dy) in enumerate(((-110, 140), (100, 200), (-70, 300), (60, 360))): d.stroke([(x + dx * s, y + dy * s), (x + (dx + (40 if dx < 0 else -40)) * s, y + (dy + 6) * s)], dk(ORANGE, 0.75), 8 * s)
    if hat:
        d.ellipse(x, y - 196 * s, 170 * s, 34 * s, fill=(54, 50, 64, 255), outline=LINE, width=12 * s); d.rrect(x - 110 * s, y - 420 * s, x + 110 * s, y - 196 * s, 18 * s, fill=(54, 50, 64, 255), outline=LINE, width=12 * s)
        d.rect(x - 104 * s, y - 260 * s, x + 104 * s, y - 226 * s, RED)
    L, Rr = (x - 58 * s, y - 70 * s), (x + 58 * s, y - 70 * s)
    B.eyes(d, L, Rr, expr, ORANGE, r=int(20 * s)) if s != 1 else B.eyes(d, L, Rr, expr, ORANGE)
    B.brows(d, L, Rr, expr, y - 122 * s)
    for sg in (-1, 1): d.ellipse(x + sg * 100 * s, y - 20 * s, 28 * s, 15 * s, fill=BLUSH)
    B.mouth(d, x, y + 10 * s, expr)
    if expr in ('shocked', 'nervous'): G.sweat(d, x + 130 * s, y - 130 * s)
    if medal:
        for sg, col in ((-1, (210, 40, 50, 255)), (1, (40, 70, 150, 255))): d.poly([(x + sg * 70 * s, y + 40 * s), (x + sg * 30 * s, y + 40 * s), (x, y + 140 * s), (x + sg * 20 * s, y + 150 * s)], fill=col, outline=LINE, width=7 * s)
        d.ellipse(x, y + 190 * s, 60 * s, 60 * s, fill=GOLD, outline=LINE, width=10 * s)
        star = [(x + 34 * s * math.cos(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45), y + 190 * s + 34 * s * math.sin(math.radians(-90 + k * 36)) * (1 if k % 2 == 0 else 0.45)) for k in range(10)]
        d.poly(star, fill=(255, 246, 190, 255))


def carrot(expr):
    d = Draw(620, 1000); d.stroke([(150, 520), (60, 420)], LINE, 14); d.dot(56, 414, 22, LINE); d.stroke([(470, 520), (560, 440)], LINE, 14); d.dot(564, 436, 22, LINE)
    carrot_body(d, 310, 420, 1.0, expr, medal=True); return d.out()


def drcarrot():
    d = Draw(760, 1100); d.stroke([(230, 640), (130, 560)], LINE, 14); d.dot(126, 554, 22, LINE)
    d.stroke([(500, 660), (560, 760)], LINE, 14); d.rrect(470, 760, 720, 940, 30, fill=(140, 84, 50, 255), outline=LINE, width=12)
    d.rrect(560, 730, 630, 770, 14, outline=LINE, width=10); d.text(595, 850, 'Dr.', 70, CREAM)
    carrot_body(d, 360, 560, 1.0, 'happy', hat=True); return d.out()


def fudge():
    d = Draw(1000, 640); d.ellipse(500, 400, 470, 200, fill=SILVER, outline=LINE, width=14); d.ellipse(500, 390, 420, 166, fill=(230, 234, 242, 255), outline=LINE, width=8)
    for k in range(7):
        x, y = 290 + (k % 4) * 140 + (70 if k >= 4 else 0), 330 + (k // 4) * 110; d.rrect(x - 60, y - 50, x + 60, y + 50, 16, fill=(232, 140, 56, 255), outline=LINE, width=10)
        d.rrect(x - 44, y - 40, x + 10, y - 22, 8, fill=(250, 196, 120, 255))
    eyes2(d, [(456, 372), (526, 372)], 18, 'calm'); d.chord(492, 400, 20, 14, 0, 180, fill=(124, 40, 62, 255))
    d.text(860, 120, '*', 160, GOLD, stroke=6, stroke_fill=LINE); return d.out()


def mini(d, x, y, ang, L, face=False):
    a = math.radians(ang); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux; w = L * 0.22
    d.poly([(x + nx * w, y + ny * w), (x + ux * L, y + uy * L), (x - nx * w, y - ny * w)], fill=ORANGE, outline=LINE, width=8)
    for k in (-1, 1): d.poly([(x, y), (x - ux * L * 0.35 + nx * k * w, y - uy * L * 0.35 + ny * k * w), (x - ux * L * 0.3, y - uy * L * 0.3)], fill=LEAF, outline=LINE, width=6)
    if face: eyes2(d, [(x + ux * L * 0.28 - nx * 14, y + uy * L * 0.28 - ny * 14), (x + ux * L * 0.28 + nx * 14, y + uy * L * 0.28 + ny * 14)], 11, 'calm')


def pile():
    d = Draw(1800, 1000); R_ = np.random.RandomState(9)
    d.poly(bez((60, 960), (300, 300), (1500, 300), (1740, 960)), fill=(150, 98, 64, 255), outline=LINE, width=16)
    for k in range(150):
        u = R_.uniform(0, 1); x = 160 + u * 1480; top = 960 - 640 * math.sin(math.pi * u) ** 0.8; y = R_.uniform(top + 40, 940)
        mini(d, x, y, R_.uniform(0, 360), R_.uniform(90, 140))
    for x, y in ((600, 760), (900, 560), (1200, 760)): mini(d, x, y, 90, 190, True)
    return d.out()


def paper():
    d = Draw(900, 1080); d.rect(30, 30, 870, 1050, (246, 242, 226, 255)); d.rrect(30, 30, 870, 1050, 10, outline=LINE, width=12)
    d.text(450, 100, 'THE DAILY GAZETTE', 60, LINE); d.stroke([(60, 146), (840, 146)], LINE, 8); d.text(450, 172, 'LONDON  1941', 34, (90, 90, 100, 255))
    d.text(450, 300, "CAT'S", 170, (34, 32, 40, 255)); d.text(450, 460, 'EYES!', 170, (34, 32, 40, 255))
    d.rrect(70, 560, 440, 1000, 10, fill=(214, 212, 220, 255), outline=LINE, width=8); d.ellipse(255, 780, 110, 110, fill=SK[0][0], outline=LINE, width=8)
    d.chord(255, 760, 116, 96, 180, 360, fill=(98, 62, 44, 255), outline=LINE, width=8)
    for sg in (-1, 1): d.rrect(255 + sg * 46 - 34, 700, 255 + sg * 46 + 34, 738, 14, fill=(130, 222, 186, 255), outline=LINE, width=6); d.dot(255 + sg * 40, 790, 10, LINE)
    d.arc(255, 820, 30, 20, 20, 160, LINE, 8)
    d.text(650, 600, 'NIGHT ACE', 48, RED)
    for k in range(9): d.stroke([(470, 660 + k * 38), (830, 660 + k * 38)], (150, 150, 160, 255), 10)
    return d.out()


def poster_a():                                              # the Ministry carrot poster
    d = Draw(900, 1200); d.rect(0, 0, 900, 1200, (248, 236, 200, 255)); d.rrect(6, 6, 894, 1194, 10, outline=LINE, width=14)
    d.rrect(50, 50, 850, 260, 20, fill=ORANGE, outline=LINE, width=10); d.text(450, 156, 'CARROTS', 150, WHITE, stroke=8, stroke_fill=LINE)
    d.text(450, 330, 'keep you healthy', 66, NAVY); d.text(450, 410, 'and help you', 66, NAVY)
    for k, x in enumerate((250, 450, 650)): mini(d, x, 620, 90, 220, k == 1)
    d.rrect(60, 880, 840, 1140, 20, fill=NAVY, outline=LINE, width=10); d.text(450, 960, 'SEE IN THE', 84, (255, 236, 120, 255)); d.text(450, 1070, 'BLACKOUT', 100, WHITE)
    return d.out()


def poster_b():
    d = Draw(900, 1200); d.rect(0, 0, 900, 1200, (96, 160, 90, 255)); d.rrect(6, 6, 894, 1194, 10, outline=LINE, width=14)
    d.text(450, 170, 'DIG FOR', 130, WHITE, stroke=7, stroke_fill=LINE); d.text(450, 330, 'VICTORY', 140, (255, 236, 120, 255), stroke=7, stroke_fill=LINE)
    d.stroke([(450, 460), (450, 900)], (150, 100, 60, 255), 34); d.poly([(370, 900), (530, 900), (510, 1080), (390, 1080)], fill=SILVER, outline=LINE, width=12)
    d.rrect(380, 430, 520, 480, 16, fill=(150, 100, 60, 255), outline=LINE, width=10); return d.out()


def poster_c(dr):
    d = Draw(900, 1200); d.rect(0, 0, 900, 1200, (252, 220, 90, 255)); d.rrect(6, 6, 894, 1194, 10, outline=LINE, width=14)
    d.text(450, 140, 'DR. CARROT', 120, RED, stroke=7, stroke_fill=LINE); im = d.out(); sm = dr.resize((int(dr.width * 0.8), int(dr.height * 0.8)), Image.LANCZOS)
    im.alpha_composite(sm, (450 - sm.width // 2, 220)); t = Draw(900, 1200); t.text(450, 1130, "the children's best friend", 50, NAVY); im.alpha_composite(t.out()); return im


def btag(txt, w, size):                                      # navy-and-gold sign
    d = Draw(w, 230); d.rrect(14, 14, w - 14, 216, 30, fill=NAVY, outline=LINE, width=14); d.rrect(38, 38, w - 38, 192, 18, outline=GOLD, width=7)
    d.text(w / 2, 118, txt, size, GOLD, stroke=5, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ set dressing (props/, textures/, bg/)
def skynight(path):                                          # Blitz London at night: moon, searchlights, fire glow, blacked-out skyline
    W, Hh = 2400, 1050; im = CA.gradient((44, 56, 128), (128, 116, 196), W, Hh, 1.2).convert('RGBA'); R_ = np.random.RandomState(2)
    s = Draw(W, Hh)
    for _ in range(160): s.dot(R_.uniform(0, W), R_.uniform(0, 600), R_.uniform(2, 5), (255, 255, 240, 220))
    im.alpha_composite(s.out()); glow(im, 1900, 230, 190, (255, 250, 220, 150), 50)
    m = Draw(W, Hh); m.ellipse(1900, 230, 110, 110, fill=(252, 248, 226, 255), outline=LINE, width=10)
    for x, y, r in ((1870, 200, 20), (1940, 260, 14), (1890, 280, 10)): m.dot(x, y, r, (226, 222, 200, 255))
    im.alpha_composite(m.out())
    bm = Draw(W, Hh)
    for x0, top in ((420, 160), (1180, -120), (1640, 420)): bm.poly([(x0 - 22, Hh), (x0 + 22, Hh), (top + 110, 0), (top - 110, 0)], fill=(255, 250, 210, 70))
    im.alpha_composite(bm.out().filter(ImageFilter.GaussianBlur(10)))
    for x in (300, 1000, 1700, 2200): glow(im, x, 960, 160, (255, 140, 60, 170), 60)
    sk = Draw(W, Hh); col = (62, 64, 120, 255); x = 0
    while x < W:
        w = R_.randint(90, 200); h = R_.randint(120, 300); sk.rect(x, Hh - h, x + w, Hh, col)
        if R_.rand() < 0.5: sk.rect(x + 20, Hh - h - 40, x + 44, Hh - h, col)
        x += w
    sk.rect(1060, 640, 1340, 1050, col); sk.chord(1200, 640, 130, 140, 180, 360, fill=col); sk.rect(1186, 460, 1214, 520, col); sk.dot(1200, 450, 18, col)
    im.alpha_composite(sk.out()); im.convert('RGB').save(path)


def hangar(path):
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (186, 190, 176, 255))
    for x in range(0, W, 40): d.stroke([(x, 260), (x, Hh)], (160, 166, 152, 255), 8)
    for x in (380, 900, 1500, 2020): roundel(d, x, 116, 1.4)
    d.rect(300, 260, 2100, Hh, (150, 156, 142, 255)); d.stroke([(1200, 260), (1200, Hh)], LINE, 12); d.rrect(300, 260, 2100, Hh, 6, outline=LINE, width=14)
    for k in range(6): d.rrect(380 + k * 290, 300, 560 + k * 290, 420, 10, fill=(255, 226, 140, 255), outline=LINE, width=8)
    for k in range(18): d.rect(300 + k * 100, Hh - 60, 350 + k * 100, Hh, (250, 210, 60, 255))
    d.out().save(path)


def street40(path):                                          # sandbagged London street: brick, taped windows, a newsagent
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (178, 92, 72, 255))
    for y in range(0, Hh, 44):
        d.stroke([(0, y), (W, y)], (214, 190, 170, 255), 4)
        for x in range(((y // 44) % 2) * 60, W, 120): d.stroke([(x, y), (x, y + 44)], (214, 190, 170, 255), 4)
    for x in (140, 1640, 2040):
        d.rrect(x, 200, x + 260, 560, 8, fill=GLASS, outline=LINE, width=12); d.stroke([(x + 10, 210), (x + 250, 550)], WHITE, 14); d.stroke([(x + 250, 210), (x + 10, 550)], WHITE, 14)
    d.rrect(560, 120, 1480, 290, 20, fill=(40, 100, 70, 255), outline=LINE, width=12); d.text(1020, 206, 'NEWSAGENT', 110, (255, 226, 120, 255), stroke=5, stroke_fill=LINE)
    d.rect(600, 330, 1440, 1000, (52, 84, 62, 255)); d.rrect(600, 330, 1440, 1000, 6, outline=LINE, width=12)
    for k, (txt, col) in enumerate((('EXTRA!', RED), ("CAT'S EYES", NAVY))):
        x = 960 + k * 260; d.rect(x, 470, x + 220, 720, (246, 242, 226, 255)); d.rrect(x, 470, x + 220, 720, 4, outline=LINE, width=6); d.text(x + 110, 540, txt.split()[0], 46, col)
        if ' ' in txt: d.text(x + 110, 610, txt.split()[1], 46, col)
    for k in range(26): d.rrect(k * 94, Hh - 120 - (k % 2) * 30, k * 94 + 110, Hh - 40 - (k % 2) * 30, 30, fill=(214, 196, 150, 255), outline=LINE, width=8)
    d.out().save(path)


def messwall(path):                                          # RAF mess: two-tone wall, menu board, bunting, hatch
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (244, 234, 206, 255)); d.rect(0, 640, W, Hh, (124, 166, 124, 255)); d.stroke([(0, 640), (W, 640)], LINE, 10)
    for k in range(24): x = k * 100; d.poly([(x, 30), (x + 100, 30), (x + 50, 120)], fill=((210, 40, 50, 255), WHITE, (40, 70, 150, 255))[k % 3], outline=LINE, width=6)
    d.rrect(900, 320, 1500, 840, 20, fill=(54, 70, 60, 255), outline=(150, 104, 64, 255), width=26); d.text(1200, 395, 'MENU', 80, WHITE)
    for k, t in enumerate(('carrot soup', 'carrot pie', 'carrot jam', 'CARROTS!')): d.text(1200, 500 + k * 82, t, 60, (255, 236, 140, 255) if k == 3 else (236, 240, 236, 255))
    d.rrect(1720, 260, 2340, 700, 16, fill=(70, 56, 50, 255), outline=LINE, width=14); d.rrect(1690, 690, 2390, 760, 10, fill=(160, 110, 70, 255), outline=LINE, width=12)
    roundel(d, 2030, 150, 1.4); roundel(d, 370, 150, 1.4); d.out().save(path)


def radarwall(path):                                         # inside the night fighter: ribs, portholes, cables
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (158, 196, 178, 255))
    for x in range(100, W, 300):
        d.rect(x - 26, 0, x + 26, Hh, (120, 156, 140, 255)); d.stroke([(x - 26, 0), (x - 26, Hh)], LINE, 6); d.stroke([(x + 26, 0), (x + 26, Hh)], LINE, 6)
        for y in range(60, Hh, 140): d.dot(x, y, 8, (210, 220, 214, 255))
    for x in (250, 850, 1450, 2050):
        d.ellipse(x, 320, 100, 100, fill=(40, 50, 110, 255), outline=SILVER, width=20); d.ellipse(x, 320, 100, 100, outline=LINE, width=6)
        for dx, dy in ((-30, -20), (30, 10), (0, 40)): d.dot(x + dx, 320 + dy, 5, WHITE)
    for k, col in enumerate(((210, 40, 50, 255), (250, 210, 60, 255), (40, 70, 150, 255))): d.stroke(bez((0, 600 + k * 30), (800, 520 + k * 30), (1600, 700 + k * 30), (W, 600 + k * 30)), col, 12)
    for k in range(24): d.poly([(k * 100, Hh - 70), (k * 100 + 50, Hh - 70), (k * 100 + 100, Hh), (k * 100 + 50, Hh)], fill=(250, 210, 60, 255))
    d.out().save(path)


def posterwall(path, pa, pb, pc):
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (196, 108, 84, 255))
    for y in range(0, Hh, 50):
        d.stroke([(0, y), (W, y)], (226, 200, 180, 255), 5)
        for x in range(((y // 50) % 2) * 70, W, 140): d.stroke([(x, y), (x, y + 50)], (226, 200, 180, 255), 5)
    im = d.out()
    for p, x, a in ((pb, 40, -3), (pa, 900, 2), (pc, 1760, -2)):
        q = p.resize((600, 800), Image.LANCZOS).rotate(a, expand=True, resample=Image.BICUBIC); im.alpha_composite(q, (x, 150))
    im.save(path)


def eyewall(path):                                           # optician: eye chart, diploma, glasses shelf
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (196, 222, 238, 255))
    d.rrect(1000, 300, 1400, 860, 16, fill=WHITE, outline=LINE, width=12)
    for k, (row, size) in enumerate((('E', 110), ('F P', 70), ('T O Z', 52), ('L P E D', 40), ('P E C F D', 32))):
        d.text(1200, 380 + sum((110, 70, 52, 40, 32)[:k]) * 1.25 + k * 18, row, size, LINE)
    d.rrect(180, 220, 600, 520, 12, fill=(250, 246, 230, 255), outline=(150, 104, 64, 255), width=20); d.text(390, 320, 'DIPLOMA', 56, NAVY); d.ellipse(390, 430, 44, 44, fill=RED, outline=LINE, width=6)
    d.rect(1700, 520, 2260, 556, (150, 104, 64, 255))
    for k in range(4):
        x = 1770 + k * 140
        for sg in (-1, 1): d.ellipse(x + sg * 30, 490, 26, 22, outline=LINE, width=8)
    d.out().save(path)


def libwall(path):                                           # historian's library: full bookshelves
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (120, 78, 50, 255)); R_ = np.random.RandomState(7)
    cols = [RED, NAVY, (60, 130, 80, 255), GOLD, PURPLE, (230, 120, 60, 255), (60, 150, 160, 255)]
    for y in (60, 320, 580, 840):
        x = 40
        while x < W - 60:
            w = R_.randint(34, 70); h = R_.randint(150, 220); col = cols[R_.randint(len(cols))]
            d.rrect(x, y + 230 - h, x + w, y + 230, 6, fill=col, outline=LINE, width=5); d.stroke([(x + 6, y + 260 - h), (x + w - 6, y + 260 - h)], GOLD, 4); x += w + 4
        d.rect(0, y + 230, W, y + 258, (90, 56, 36, 255)); d.stroke([(0, y + 258), (W, y + 258)], LINE, 6)
    d.out().save(path)


def gerwall(path):                                           # German HQ: map of Britain, radio set, clock (no insignia)
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (158, 166, 150, 255)); d.rect(0, 820, W, Hh, (128, 136, 122, 255))
    d.rrect(900, 200, 1500, 680, 16, fill=(130, 180, 220, 255), outline=(110, 80, 54, 255), width=18)
    GB = [(1180, 140), (1260, 200), (1240, 300), (1300, 420), (1380, 560), (1420, 700), (1300, 760), (1120, 780), (1000, 740), (1080, 640), (1040, 520), (1100, 420), (1060, 300), (1100, 200)]
    GB = [(1200 + (x - 1210) * 0.62, 440 + (y - 460) * 0.62) for x, y in GB]
    d.poly(GB, fill=(160, 200, 130, 255), outline=LINE, width=8)
    for x, y in ((1225, 560), (1213, 480), (1170, 440)): d.dot(x, y, 10, RED)
    d.rrect(140, 380, 560, 760, 20, fill=(90, 84, 72, 255), outline=LINE, width=12)
    for x in (240, 460): d.ellipse(x, 480, 56, 56, fill=(230, 220, 180, 255), outline=LINE, width=8)
    for k in range(5): d.stroke([(200, 600 + k * 30), (500, 600 + k * 30)], (60, 56, 50, 255), 8)
    d.ellipse(2000, 300, 120, 120, fill=WHITE, outline=LINE, width=14); d.stroke([(2000, 300), (2000, 210)], LINE, 12); d.stroke([(2000, 300), (2060, 340)], LINE, 10)
    d.out().save(path)


def kitchen(path):                                           # a kitchen of today: pastel cabinets, fridge, window, a 2026 calendar
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (250, 244, 232, 255))
    for x in range(0, W, 60): d.stroke([(x, 420), (x, 760)], (222, 226, 234, 255), 4)
    for y in range(420, 760, 60): d.stroke([(0, y), (W, y)], (222, 226, 234, 255), 4)
    for k in range(5): d.rrect(80 + k * 260, 40, 320 + k * 260, 380, 18, fill=(150, 214, 196, 255), outline=LINE, width=10); d.dot(300 + k * 260 - 40, 330, 10, SILVER)
    d.rrect(1440, 80, 1900, 520, 20, fill=(180, 220, 250, 255), outline=WHITE, width=30); d.rrect(1440, 80, 1900, 520, 20, outline=LINE, width=8); d.stroke([(1670, 80), (1670, 520)], WHITE, 18)
    d.rrect(2000, 80, 2340, 1100, 30, fill=(240, 242, 246, 255), outline=LINE, width=12); d.stroke([(2000, 480), (2340, 480)], LINE, 8)
    d.rrect(2060, 560, 2200, 700, 6, fill=WHITE, outline=LINE, width=5); d.ellipse(2130, 620, 34, 34, fill=(250, 210, 60, 255))
    d.rrect(1020, 440, 1340, 720, 10, fill=WHITE, outline=LINE, width=8); d.rect(1020, 440, 1340, 520, RED); d.text(1180, 482, '2026', 64, WHITE)
    for k in range(12): d.rect(1050 + (k % 4) * 72, 550 + (k // 4) * 54, 1090 + (k % 4) * 72, 586 + (k // 4) * 54, (210, 214, 224, 255))
    d.rect(0, 760, 1960, 800, (214, 190, 160, 255)); d.rect(0, 800, 1960, Hh, (150, 214, 196, 255)); d.stroke([(0, 800), (1960, 800)], LINE, 8)
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
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'confused')]
    dr = drcarrot(); pa, pb, pc = poster_a(), poster_b(), poster_c(dr)
    multi = dict(beau={'default': beau(), 'xray': beau('xray'), 'tally': beau('tally')}, beauf={'default': beau('fly')},
                 bomber={'default': bomber(), 'shock': bomber('shock')}, radar={'default': radar(), 'wow': radar('wow')},
                 carrot={'default': carrot('smug'), 'happy': carrot('happy'), 'shocked': carrot('shocked')})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    B.sparkle(Pp('sparkle.png'))
    cards = dict(drcarrot=dr, fudge=fudge(), pile=pile(), paper=paper(), postera=pa,
                 bestpilot=btag('BEST NIGHT PILOT', 1100, 96), cantsee=CA.stamp("CAN'T SEE!", 760, 112), credit=V.wtag('TOOK THE CREDIT!', 1060, ORANGE, 78),
                 machine=V.wtag('A MACHINE COULD!', 1060, (40, 150, 100, 255), 76), y1940=V.big_card('1940', 'BRITAIN', BLUE, 720), blitz=CA.stamp('THE BLITZ!', 820, 110),
                 boom=B.sticker_burst('BOOM!', fill=(255, 170, 60, 255)), everynight=V.wtag('EVERY NIGHT!', 840, RED, 88), found=CA.stamp('FOUND YOU!', 800, 108),
                 name=btag('JOHN CUNNINGHAM', 1180, 84), k20=V.big_card('20', 'KILLS', RED, 600), k19=V.big_card('19', 'IN PITCH BLACK', NAVY, 760),
                 catseyes=V.wtag("CAT'S EYES", 820, (240, 170, 40, 255), 96), secret=V.wtag('HIS SECRET?', 820, PURPLE, 92), carrots=CA.stamp('CARROTS!', 760, 118),
                 lots=V.wtag('LOTS OF CARROTS!', 1060, ORANGE, 78), realsecret=btag('THE REAL SECRET', 1060, 84), radart=V.wtag('RADAR!', 620, (40, 150, 100, 255), 104),
                 topsecret=CA.stamp('TOP SECRET', 860, 108), shh=B.sticker_burst('SHHH!'), story=V.wtag('THE CARROT STORY', 1060, ORANGE, 78),
                 everywhere=CA.stamp('EVERYWHERE!', 900, 104), posters=V.wtag('POSTERS!', 720, RED, 98), drname=V.wtag('DOCTOR CARROT', 960, ORANGE, 84),
                 fudget=V.wtag('CARROT FUDGE!', 960, (170, 96, 50, 255), 84), y1942=V.big_card('1942', 'BRITAIN', GREEN, 720),
                 tons=V.wtag('100,000 TONS!', 960, ORANGE, 92), nonv=CA.stamp('NO NIGHT VISION!', 1100, 92), historians=V.wtag('HISTORIANS SAY...', 1040, NAVY, 80),
                 never=CA.stamp('NEVER FELL FOR IT!', 1160, 88), fooled=V.wtag('IT FOOLED US!', 900, RED, 92), y80=V.big_card('80+', 'YEARS LATER', BLUE, 720),
                 believe=CA.stamp('WE STILL BELIEVE IT!', 1220, 84), qmark=B.sticker_mark('?', GOLD), bang=B.sticker_mark('!', RED),
                 sparkle=Image.open(Pp('sparkle.png')).convert('RGBA'))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); G.tex_asphalt(T('asphalt.jpg')); B.tex_grass(T('grass.jpg')); G.tex_concrete(T('concrete.jpg'))
    tiles(T('tiles.jpg'), (236, 230, 214), (120, 150, 120)); tiles(T('kfloor.jpg'), (240, 236, 230), (214, 206, 196)); tiles(T('ofloor.jpg'), (226, 236, 244), (186, 206, 222))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); B.window(Pp('window.png'))
    skynight(Pp('skynight.png')); hangar(Pp('hangar.png')); street40(Pp('street40.png')); messwall(Pp('messwall.png')); radarwall(Pp('radarwall.png'))
    posterwall(Pp('posterwall.png'), pa, pb, pc); eyewall(Pp('eyewall.png')); libwall(Pp('libwall.png')); gerwall(Pp('gerwall.png')); kitchen(Pp('kitchen.png'))
    VA.skyplane(Pp('skyday.png'), (92, 150, 226), (226, 240, 252), hills=(120, 170, 100))
    for n in ('skynight', 'hangar', 'street40', 'messwall', 'radarwall', 'posterwall', 'eyewall', 'libwall', 'gerwall', 'kitchen'): items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
