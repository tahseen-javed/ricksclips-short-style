#!/usr/bin/env python3
"""Assets for video 09 (the Great Emu War, 1932), drawn in code with the channel builders.
New cast (all cute, big heads): two Aussie gunners in slouch hats, Major Meredith (peaked cap, binoculars), a veteran wheat
farmer (bush hat, medal) and a farm wife (sun hat), Defence Minister Pearce (walrus moustache), a bounty clerk (green
eyeshade).  Cute props: the emu (smug / happy / shocked / running), an emu in tank armour, an emu herd, a Lewis gun with a
face (idle / firing), an army truck with a face, ammo crates, a wheat sheaf (tall / wrecked), a cash sack, a trophy,
feathers, a map of Australia.  Sets: wheat farm with windmill, red outback, minister's office, army camp, bounty office.
usage: make_assets.py <project folder> [font.ttf]"""
import os, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import assets_base as B
import gimli_assets as G
import viking_assets as V
import vasa_assets as VA
import corrigan_assets as CA
import catseyes_assets as CE
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN, BLUE = G.RED, G.GOLD, G.GREEN, VA.BLUE
dk, SK, eyes2, glow, btag, tiles = VA.dk, VA.SK, CE.eyes2, CE.glow, CE.btag, CE.tiles
KHAKI, KSH, OLIVE, WHEAT, CREAM, GLASS = (196, 170, 112, 255), (164, 138, 86, 255), (110, 120, 76, 255), (240, 196, 92, 255), (250, 238, 206, 255), (170, 222, 244, 255)
EMU, EMUD, NECK, BEAK = (116, 92, 78, 255), (86, 66, 56, 255), (122, 150, 196, 255), (232, 196, 150, 255)
NEW = {
    'gunner': dict(sk=0, style='slouch', hair=(150, 92, 52, 255), hc=(150, 120, 80, 255), suit=KHAKI, shade=KSH, body='army', freck=1),
    'gunner2': dict(sk=2, style='slouch', hair=(44, 32, 36, 255), hc=(128, 102, 70, 255), suit=KHAKI, shade=KSH, body='army'),
    'meredith': dict(sk=1, style='kcap', hair=(110, 70, 44, 255), hc=(176, 150, 96, 255), suit=(180, 156, 102, 255), shade=(150, 126, 80, 255), body='officer',
                     stache=(110, 70, 44, 255)),
    'farmer': dict(sk=1, style='bush', hair=(170, 110, 64, 255), hc=(120, 84, 54, 255), suit=(214, 200, 168, 255), shade=(186, 170, 138, 255), body='veteran'),
    'farmwife': dict(sk=0, style='sunhat', hair=(196, 120, 70, 255), hc=(250, 226, 160, 255), suit=(120, 170, 220, 255), shade=(96, 140, 190, 255), body='apron', freck=1),
    'pearce': dict(sk=0, style='walrus', hair=(214, 214, 222, 255), suit=(60, 64, 84, 255), shade=(44, 46, 64, 255), body='waistcoat', walrus=(214, 214, 222, 255)),
    'clerk': dict(sk=2, style='visor', hair=(40, 30, 34, 255), hc=(60, 170, 110, 255), suit=(246, 246, 240, 255), shade=(214, 214, 210, 255), body='clerk', glasses=1),
}


# ------------------------------------------------------------------ cast
def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']; st, hr = c['style'], c.get('hair')
    skin, sh = SK[c['sk']]
    d.ellipse(cx, cy, R, R, fill=skin, outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, sh, skin)
    if st != 'walrus': d.chord(cx, cy - 66, R + 8, 132, 180, 360, fill=hr, outline=LINE, width=lw)
    hc = c.get('hc')
    if st == 'slouch':                                       # Aussie slouch hat, left brim pinned up, gold badge
        d.ellipse(cx + 20, 150, 250, 40, fill=dk(hc, 0.88), outline=LINE, width=lw)
        d.poly([(cx - 150, 150), (cx - 120, 40), (cx, 60), (cx + 120, 40), (cx + 150, 150)], fill=hc, outline=LINE, width=lw)
        d.rect(cx - 144, 110, cx + 146, 140, (60, 120, 80, 255)); d.poly([(cx - 150, 150), (cx - 236, 40), (cx - 200, 20), (cx - 130, 120)], fill=dk(hc, 0.95), outline=LINE, width=12)
        d.ellipse(cx - 176, 74, 26, 26, fill=GOLD, outline=LINE, width=7); d.dot(cx - 176, 74, 9, (255, 246, 190, 255))
    elif st == 'kcap':                                       # khaki officer's peaked cap, red band
        d.poly([(cx - 180, 140), (cx - 214, 56), (cx, 16), (cx + 214, 56), (cx + 180, 140)], fill=hc, outline=LINE, width=lw)
        d.rrect(cx - 186, 104, cx + 186, 150, 12, fill=(196, 50, 56, 255), outline=LINE, width=10); d.ellipse(cx, 92, 24, 24, fill=GOLD, outline=LINE, width=7)
        d.chord(cx, 150, 166, 44, 0, 180, fill=(70, 50, 36, 255), outline=LINE, width=12)
    elif st == 'bush':                                       # dented bush hat
        d.ellipse(cx, 150, 262, 44, fill=dk(hc, 0.88), outline=LINE, width=lw)
        d.poly([(cx - 150, 150), (cx - 130, 40), (cx - 40, 62), (cx, 40), (cx + 40, 62), (cx + 130, 40), (cx + 150, 150)], fill=hc, outline=LINE, width=lw)
        d.rect(cx - 144, 112, cx + 144, 138, (60, 44, 34, 255)); d.chord(cx, 150, 262, 44, 0, 180, fill=dk(hc, 0.88), outline=LINE, width=lw)
    elif st == 'sunhat':                                     # wide straw sun hat, pink ribbon and flower
        d.ellipse(cx, 140, 270, 56, fill=dk(hc, 0.92), outline=LINE, width=lw); d.chord(cx, 140, 156, 110, 180, 360, fill=hc, outline=LINE, width=lw)
        d.rect(cx - 150, 106, cx + 150, 132, (242, 120, 160, 255)); d.dot(cx + 120, 116, 26, (255, 200, 220, 255)); d.dot(cx + 120, 116, 10, GOLD)
        for sg in (-1, 1): d.ellipse(cx + sg * 196, cy + 10, 34, 56, fill=hr, outline=LINE, width=9)
    elif st == 'walrus':                                     # bald top, grey tufts
        d.ellipse(cx - 60, 120, 60, 26, fill=(255, 255, 255, 110))
        for sg in (-1, 1):
            for dx, dy in ((0, 0), (12, 44)): d.ellipse(cx + sg * (198 + dx), cy - 60 + dy, 36, 32, fill=hr, outline=LINE, width=9)
    elif st == 'visor':                                      # green eyeshade
        d.chord(cx, 150, 236, 70, 0, 180, fill=(60, 170, 110, 200), outline=LINE, width=12); d.rrect(cx - 200, 120, cx + 200, 156, 14, fill=dk(hc, 0.8), outline=LINE, width=10)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    for sg in (-1, 1): d.ellipse(cx + sg * 112, cy + 40, 30, 17, fill=BLUSH)
    if c.get('freck'):
        for sg in (-1, 1):
            for dx, dy in ((-14, 0), (8, -10), (10, 12)): d.dot(cx + sg * 108 + dx, cy + 12 + dy, 5, (196, 120, 90, 255))
    B.eyes(d, L, Rr, expr, skin); B.brows(d, L, Rr, expr, ey - 50)
    if c.get('glasses'):
        for p in (L, Rr): d.ellipse(p[0], p[1], 50, 46, outline=LINE, width=9)
        d.stroke([(L[0] + 50, ey), (Rr[0] - 50, ey)], LINE, 9)
    my = cy + 74
    if c.get('stache'):
        for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 34, my - 52), (cx + sg * 62, my - 40), (cx + sg * 72, my - 58)), c['stache'], 20)
        my += 12
    if c.get('walrus'):                                      # big droopy walrus moustache
        for sg in (-1, 1): d.poly(bez((cx, my - 44), (cx + sg * 70, my - 60), (cx + sg * 110, my - 10), (cx + sg * 96, my + 24)) + [(cx + sg * 30, my - 6)], fill=c['walrus'], outline=LINE, width=8)
        my += 22
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']; base = c['suit']; bs = c['body']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=base)
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=base); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if bs in ('army', 'officer'):                            # khaki tunic, four pockets, belt; gunners wear a bandolier, the Major a Sam Browne + binoculars
        t.poly([(176, 452), (284, 452), (230, 540)], fill=dk(base, 0.8))
        for x in (150, 310): t.rrect(x - 46, 570, x + 46, 640, 10, fill=dk(base, 0.9), outline=LINE, width=6); t.dot(x, 586, 8, (150, 120, 70, 255))
        t.rect(0, 720, 460, 754, (110, 76, 50, 255)); t.rrect(212, 716, 248, 758, 6, fill=GOLD, outline=LINE, width=6)
        if bs == 'army':
            t.stroke([(110, 470), (350, 740)], (120, 84, 54, 255), 30)
            for k in range(6): t.rrect(140 + k * 38, 500 + k * 43, 160 + k * 38, 530 + k * 43, 5, fill=GOLD, outline=LINE, width=4)
        else:
            t.stroke([(330, 470), (130, 724)], (110, 76, 50, 255), 18)
            for x in (196, 264): t.rrect(x - 26, 560, x + 26, 640, 12, fill=(50, 50, 58, 255), outline=LINE, width=6)
            t.stroke([(200, 462), (196, 560)], LINE, 5); t.stroke([(260, 462), (264, 560)], LINE, 5)
    elif bs == 'veteran':                                    # work shirt, braces, a war medal
        for x in (170, 290): t.rect(x - 14, 452, x + 14, 800, (110, 70, 44, 255))
        t.poly([(186, 452), (274, 452), (230, 520)], fill=dk(base, 0.85)); t.rect(300, 540, 320, 590, RED); t.ellipse(310, 610, 22, 22, fill=GOLD, outline=LINE, width=6)
    elif bs == 'apron':                                      # blue dress, white apron
        t.rrect(130, 560, 330, 840, 30, fill=WHITE, outline=LINE, width=8); t.rrect(186, 620, 274, 690, 12, outline=LINE, width=6)
        t.chord(230, 452, 70, 40, 0, 180, fill=WHITE)
    elif bs == 'waistcoat':                                  # suit, waistcoat, gold watch chain
        t.poly([(166, 452), (294, 452), (230, 600)], fill=WHITE); t.rrect(160, 520, 300, 800, 20, fill=(120, 40, 50, 255))
        tt = [(230, 474), (208, 500), (214, 600), (230, 620), (246, 600), (252, 500)]; t.poly(tt, fill=NAVY_ if False else (40, 44, 60, 255)); t.stroke(tt + [tt[0]], LINE, 6)
        t.stroke(bez((180, 660), (210, 700), (250, 700), (280, 660)), GOLD, 7)
        for y in (640, 700, 760): t.dot(230, y, 8, GOLD)
    elif bs == 'clerk':                                      # shirt, sleeve garters, bow tie
        for sg in (-1, 1): t.poly([(230, 478), (230 + sg * 46, 456), (230 + sg * 46, 504)], fill=(60, 170, 110, 255), outline=LINE, width=6)
        t.rrect(290, 560, 340, 620, 6, outline=LINE, width=5); t.rect(300, 540, 308, 580, BLUE)
        for y in (560, 640, 720): t.dot(230, y, 8, (180, 180, 190, 255))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


# ------------------------------------------------------------------ cute props
def emu_draw(d, x, y, mood='smug', run=False, s=1.0, armour=False):   # x, y = feet centre; a cute fluffy emu facing right
    P = lambda a, b: (x + a * s, y + b * s)
    if run:
        for yy, x0 in ((-760, -480), (-660, -520), (-560, -470)): d.stroke([P(x0, yy), P(x0 + 150, yy)], LINE, 22 * s); d.stroke([P(x0 + 4, yy), P(x0 + 146, yy)], WHITE, 9 * s)
        legs = (((-60, -470), (-130, -250), (-230, -60)), ((60, -470), (110, -250), (60, 0)))
    else:
        legs = (((-50, -470), (-80, -240), (-60, 0)), ((50, -470), (80, -240), (70, 0)))
    for (a, b, c) in legs:
        for col, w in ((LINE, 34), ((160, 160, 172, 255), 20)): d.stroke([P(*a), P(*b), P(*c)], col, w * s)
        for ang in (-30, 0, 30): fx, fy = P(*c); d.stroke([(fx, fy), (fx + 60 * s * math.cos(math.radians(ang)), fy + 14 * s * math.sin(math.radians(ang)) - 4 * s)], LINE, 12 * s)
    d.stroke([P(150, -690), P(230, -860), P(250, -1000)], LINE, 100 * s); d.stroke([P(150, -690), P(230, -860), P(250, -1000)], (140, 170, 214, 255), 74 * s)
    d.ellipse(*P(0, -640), 300 * s, 210 * s, fill=EMU, outline=LINE, width=16 * s)
    R_ = np.random.RandomState(3)
    for _ in range(70):
        a = R_.uniform(0, 2 * math.pi); rr = R_.uniform(0.2, 0.9); px, py = P(rr * 260 * math.cos(a), -640 + rr * 180 * math.sin(a))
        d.stroke([(px, py), (px - 30 * s, py + 34 * s)], EMUD if R_.rand() < 0.6 else (150, 124, 104, 255), 8 * s)
    for k in range(7): px, py = P(-300 + k * 20, -700 + k * 30); d.stroke([(px, py), (px - 70 * s, py + 50 * s)], EMUD, 14 * s)
    for k in range(5): px, py = P(150 + k * 14, -740 + k * 26); d.stroke([(px, py), (px + 40 * s, py - 20 * s)], EMUD, 12 * s)
    if armour:                                               # tank armour: plates, rivets, a turret with a little cannon, treads
        d.rrect(*P(-300, -820), *P(300, -480), 40 * s, fill=(110, 130, 80, 255), outline=LINE, width=16 * s)
        for k in range(6): d.dot(*P(-250 + k * 100, -790), 10 * s, (70, 80, 50, 255))
        d.rrect(*P(-120, -960), *P(130, -820), 40 * s, fill=(110, 130, 80, 255), outline=LINE, width=14 * s); d.rrect(*P(120, -910), *P(330, -870), 14 * s, fill=(90, 104, 64, 255), outline=LINE, width=10 * s)
        d.rrect(*P(-340, -120), *P(340, 20), 60 * s, fill=(60, 60, 66, 255), outline=LINE, width=14 * s)
        for k in range(6): d.ellipse(*P(-260 + k * 104, -50), 40 * s, 40 * s, fill=(150, 150, 160, 255), outline=LINE, width=8 * s)
        d.ellipse(*P(-40, -730), 70 * s, 50 * s, fill=(196, 50, 56, 255), outline=LINE, width=8 * s); d.text(*P(-40, -728), 'EMU', int(46 * s), WHITE)
    HD = (132, 126, 158, 255)
    for k in range(7): px, py = P(170 + k * 26, -1222); d.stroke([(px, py), (px + 8 * s, py - 62 * s)], LINE, 12 * s)
    d.ellipse(*P(255, -1085), 168 * s, 156 * s, fill=HD, outline=LINE, width=16 * s); d.ellipse(*P(200, -1150), 60 * s, 30 * s, fill=(255, 255, 255, 70))
    bx, by = P(410, -1060); d.poly([(bx - 10 * s, by - 40 * s), (bx + 100 * s, by - 6 * s), (bx + 96 * s, by + 16 * s), (bx - 10 * s, by + 36 * s)], fill=BEAK, outline=LINE, width=10 * s)
    L, Rr = P(190, -1100), P(320, -1100)
    B.eyes(d, L, Rr, mood, HD, r=int(46 * s)); B.brows(d, L, Rr, mood, P(0, -1185)[1])
    for px in (160, 350): d.ellipse(*P(px, -1010), 34 * s, 18 * s, fill=BLUSH)
    if mood in ('shocked', 'nervous'): G.sweat(d, *P(420, -1200))


def emu(mood='smug', run=False):
    d = Draw(1000, 1420); emu_draw(d, 440, 1380, mood, run); return d.out()


def emutank():
    d = Draw(1100, 1460); emu_draw(d, 520, 1400, 'smug', armour=True); return d.out()


def herd():
    d = Draw(2200, 900)
    for k in range(9): emu_draw(d, 140 + k * 235, 860 - (k % 2) * 60, ('smug', 'happy')[k % 2], run=True, s=0.5)
    return d.out()


def lewis(st='default'):                                     # Lewis gun on a tripod, a face on the cooling shroud
    d = Draw(1200, 760)
    for a, b in (((520, 420), (360, 740)), ((560, 420), (720, 740)), ((540, 420), (560, 740))): d.stroke([a, b], LINE, 22); d.stroke([a, b], (90, 90, 100, 255), 10)
    if st == 'fire':
        star = [(1080 + (110 if k % 2 == 0 else 46) * math.cos(math.radians(k * 30)), 330 + (110 if k % 2 == 0 else 46) * math.sin(math.radians(k * 30))) for k in range(12)]
        d.poly(star, fill=(255, 210, 70, 255), outline=LINE, width=8); d.dot(1080, 330, 36, (255, 250, 210, 255))
        for k in range(4): d.rrect(380 + k * 40, 500 + k * 50, 400 + k * 40, 540 + k * 50, 6, fill=GOLD, outline=LINE, width=5)
    d.rrect(90, 300, 300, 380, 30, fill=(150, 98, 56, 255), outline=LINE, width=14); d.rrect(260, 360, 320, 470, 18, fill=(70, 70, 76, 255), outline=LINE, width=12)
    d.rrect(280, 270, 900, 390, 50, fill=(84, 100, 74, 255), outline=LINE, width=16)
    for x in range(330, 880, 42): d.stroke([(x, 284), (x, 376)], (64, 78, 56, 255), 8)
    d.rrect(880, 310, 1020, 350, 14, fill=(70, 70, 76, 255), outline=LINE, width=10)
    d.ellipse(480, 236, 180, 44, fill=(76, 76, 84, 255), outline=LINE, width=14); d.ellipse(480, 230, 50, 16, fill=(120, 120, 130, 255))
    eyes2(d, [(640, 330), (730, 330)], 30, 'angry' if st == 'fire' else 'calm')
    for x in (600, 770): d.ellipse(x, 368, 20, 10, fill=BLUSH)
    return d.out()


def truck():                                                 # 1930s army truck, nose right, face on the windscreen
    d = Draw(1500, 820); K_ = (150, 140, 96, 255)
    d.rrect(40, 300, 780, 600, 20, fill=K_, outline=LINE, width=16)
    for x in range(100, 760, 80): d.stroke([(x, 320), (x, 580)], dk(K_, 0.85), 8)
    d.rrect(760, 220, 1080, 600, 40, fill=dk(K_, 1.05), outline=LINE, width=16); d.rrect(800, 250, 1040, 400, 24, fill=GLASS, outline=LINE, width=12)
    d.poly(bez((1080, 380), (1250, 360), (1400, 420), (1420, 600)) + [(1080, 600)], fill=K_, outline=LINE, width=16)
    for y in range(440, 590, 30): d.stroke([(1320, y), (1410, y)], LINE, 8)
    eyes2(d, [(880, 326), (980, 326)], 40, 'calm'); d.chord(1240, 520, 56, 40, 0, 180, fill=(124, 40, 62, 255), outline=LINE, width=9)
    for x in (860, 1000): d.ellipse(x, 380, 24, 12, fill=BLUSH)
    for x in (260, 1160): d.ellipse(x, 640, 120, 120, fill=(46, 44, 52, 255), outline=LINE, width=16); d.ellipse(x, 640, 50, 50, fill=(196, 190, 150, 255), outline=LINE, width=8)
    d.dot(1400, 470, 30, (255, 240, 150, 255)); d.ellipse(1400, 470, 30, 30, outline=LINE, width=8); return d.out()


def ammo():
    d = Draw(1000, 760)
    for x, y in ((80, 420), (520, 420), (300, 90)):
        d.rrect(x, y, x + 400, y + 300, 16, fill=OLIVE, outline=LINE, width=14); d.rrect(x + 20, y + 20, x + 380, y + 60, 8, fill=dk(OLIVE, 0.8))
        d.text(x + 200, y + 180, '.303', 90, (250, 236, 170, 255), stroke=5, stroke_fill=LINE)
    for k in range(5): x = 120 + k * 50; d.rrect(x, 640 - 10, x + 30, 740, 10, fill=GOLD, outline=LINE, width=5)
    return d.out()


def wheat(wrecked=False):
    d = Draw(700, 1000); R_ = np.random.RandomState(5)
    for k in range(13):
        x = 120 + k * 36 + R_.uniform(-8, 8); top = 120 + R_.uniform(0, 120); bend = (R_.uniform(-260, 260) if wrecked else R_.uniform(-30, 30))
        tx, ty = x + bend, (top + (520 if wrecked and k % 2 else 0)); d.stroke(bez((350, 980), (x, 700), (tx, ty + 200), (tx, ty)), (200, 160, 70, 255), 12)
        if not (wrecked and k % 3 == 0):
            for j in range(5): d.ellipse(tx + (j % 2) * 18 - 9, ty + j * 26, 16, 22, fill=WHEAT, outline=LINE, width=4)
    d.rrect(240, 760, 460, 820, 20, fill=(150, 98, 56, 255), outline=LINE, width=10)
    if wrecked:
        for x, y in ((120, 900), (560, 880), (360, 930)): d.ellipse(x, y, 30, 18, fill=WHEAT, outline=LINE, width=5)
    return d.out()


def cash():
    d = Draw(800, 820); R_ = np.random.RandomState(4)
    d.poly(bez((180, 300), (60, 500), (100, 760), (400, 780)) + bez((400, 780), (700, 760), (740, 500), (620, 300)), fill=(206, 174, 116, 255), outline=LINE, width=16)
    d.poly([(300, 300), (500, 300), (560, 180), (240, 180)], fill=(206, 174, 116, 255), outline=LINE, width=14); d.rrect(270, 280, 530, 320, 14, fill=(150, 98, 56, 255), outline=LINE, width=10)
    d.text(400, 560, '£', 300, (120, 84, 40, 255), stroke=6, stroke_fill=LINE)
    for k in range(9): d.ellipse(140 + k * 64, 770 + (k % 2) * 20, 40, 18, fill=GOLD, outline=LINE, width=6)
    return d.out()


def trophy():
    d = Draw(600, 760); d.poly([(130, 80), (470, 80), (420, 330), (300, 400), (180, 330)], fill=GOLD, outline=LINE, width=14)
    for sg in (-1, 1): d.arc(300 + sg * 190, 180, 70, 80, 270 if sg < 0 else 90, 450 if sg < 0 else 270, LINE, 14)
    d.rrect(260, 400, 340, 560, 12, fill=GOLD, outline=LINE, width=12); d.rrect(170, 560, 430, 640, 16, fill=(150, 98, 56, 255), outline=LINE, width=12)
    d.text(300, 210, '#1', 120, WHITE, stroke=6, stroke_fill=LINE); d.ellipse(220, 140, 26, 40, fill=(255, 250, 210, 200)); return d.out()


def feathers():
    d = Draw(700, 520)
    for x, y, a in ((150, 260, 30), (330, 160, -20), (520, 280, 40), (300, 400, -50), (560, 110, 10)):
        ux, uy = math.cos(math.radians(a)), math.sin(math.radians(a))
        d.poly([(x - ux * 100, y - uy * 100), (x - uy * 40, y + ux * 40), (x + ux * 100, y + uy * 100), (x + uy * 40, y - ux * 40)], fill=(130, 104, 88, 255), outline=LINE, width=8)
        d.stroke([(x - ux * 120, y - uy * 120), (x + ux * 100, y + uy * 100)], LINE, 6)
    return d.out()


AUS = [(140, 380), (260, 260), (420, 230), (520, 140), (600, 200), (700, 120), (760, 260), (860, 190), (940, 330), (1040, 430), (1080, 560), (1000, 700), (880, 800),
       (740, 790), (620, 700), (520, 660), (400, 700), (260, 720), (150, 640), (110, 500)]


def ozmap():
    d = Draw(1200, 980); d.rrect(10, 10, 1190, 970, 40, fill=(122, 178, 222, 255), outline=LINE, width=18)
    d.poly(AUS, fill=(244, 222, 170, 255), outline=LINE, width=14)
    WA = [p for p in AUS if p[0] <= 520] + [(520, 140)]
    d.poly([(140, 380), (260, 260), (420, 230), (520, 140), (520, 660), (400, 700), (260, 720), (150, 640), (110, 500)], fill=(236, 140, 70, 255), outline=LINE, width=10)
    d.poly(AUS, outline=LINE, width=14); d.dot(250, 470, 26, RED); d.ellipse(250, 470, 26, 26, outline=LINE, width=8)
    d.rrect(150, 520, 350, 580, 14, fill=WHITE, outline=LINE, width=6); d.text(250, 550, 'CAMPION', 34, LINE)
    d.text(600, 880, 'WESTERN AUSTRALIA', 64, WHITE, stroke=5, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ set dressing
def wheatrow(path):
    W, Hh = 2400, 520; d = Draw(W, Hh); R_ = np.random.RandomState(11)
    for k in range(260):
        x = R_.uniform(0, W); top = R_.uniform(40, 200); col = (226 + R_.randint(-20, 20), 180 + R_.randint(-20, 20), 80, 255)
        d.stroke([(x, Hh), (x + R_.uniform(-30, 30), top)], (190, 150, 64, 255), 6)
        for j in range(4): d.ellipse(x + (j % 2) * 10 - 5, top + j * 18, 9, 14, fill=col)
    d.rect(0, Hh - 60, W, Hh, (200, 160, 70, 255)); d.out().save(path)


def windmill(path):
    W, Hh = 700, 1600; d = Draw(W, Hh)
    for a, b in (((350, 330), (180, 1590)), ((350, 330), (520, 1590))): d.stroke([a, b], LINE, 22); d.stroke([a, b], (200, 200, 208, 255), 10)
    for y in range(500, 1590, 220): t = (y - 330) / 1260.0; d.stroke([(350 - 170 * t, y), (350 + 170 * t, y)], (150, 150, 160, 255), 8)
    for k in range(16):
        a = math.radians(k * 22.5); d.poly([(350 + 60 * math.cos(a - 0.12), 300 + 60 * math.sin(a - 0.12)), (350 + 280 * math.cos(a - 0.08), 300 + 280 * math.sin(a - 0.08)),
                                           (350 + 280 * math.cos(a + 0.08), 300 + 280 * math.sin(a + 0.08)), (350 + 60 * math.cos(a + 0.12), 300 + 60 * math.sin(a + 0.12))], fill=(226, 230, 236, 255), outline=LINE, width=5)
    d.dot(350, 300, 40, (196, 50, 56, 255)); d.ellipse(350, 300, 40, 40, outline=LINE, width=8)
    d.poly([(350, 300), (690, 230), (690, 380)], fill=(196, 50, 56, 255), outline=LINE, width=8); d.out().save(path)


def outback(path):                                          # drought: hot orange sky, big sun, red mesas, dead trees
    W, Hh = 2400, 1050; im = CA.gradient((236, 150, 80), (255, 222, 160), W, Hh, 1.2).convert('RGBA'); glow(im, 1700, 260, 260, (255, 250, 200, 200), 60)
    d = Draw(W, Hh); d.ellipse(1700, 260, 130, 130, fill=(255, 244, 180, 255), outline=(240, 170, 80, 255), width=10)
    for x0, w, h in ((100, 600, 300), (900, 400, 220), (1900, 500, 330)): d.poly([(x0, Hh - 120), (x0 + 80, Hh - 120 - h), (x0 + w - 80, Hh - 120 - h), (x0 + w, Hh - 120)], fill=(176, 84, 52, 255), outline=LINE, width=8)
    d.rect(0, Hh - 140, W, Hh, (206, 110, 64, 255))
    for x in (700, 1450):
        d.stroke([(x, Hh - 130), (x + 10, Hh - 420)], (90, 64, 50, 255), 18)
        for a, l in ((-40, 120), (30, 140), (-10, 90)): d.stroke([(x + 8, Hh - 320), (x + 8 + l * math.sin(math.radians(a)), Hh - 320 - l * math.cos(math.radians(a)))], (90, 64, 50, 255), 10)
    im.alpha_composite(d.out()); im.convert('RGB').save(path)


def office(path):                                            # Minister's office: wood panels, window, a map of Australia, portrait, bookshelf
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (170, 120, 80, 255))
    for x in range(0, W, 200): d.rrect(x + 16, 560, x + 184, 1080, 10, outline=(130, 88, 56, 255), width=8)
    d.rect(0, 540, W, 560, (120, 80, 50, 255))
    d.rrect(1000, 230, 1400, 520, 14, fill=(122, 178, 222, 255), outline=(110, 80, 54, 255), width=16)
    d.poly([(1000 + (x - 100) * 0.34 + 30, 230 + (y - 100) * 0.34 + 26) for x, y in AUS], fill=(244, 222, 170, 255), outline=LINE, width=6)
    d.rrect(180, 100, 560, 480, 12, fill=(180, 220, 250, 255), outline=WHITE, width=24); d.rrect(180, 100, 560, 480, 12, outline=LINE, width=8); d.stroke([(370, 100), (370, 480)], WHITE, 14)
    d.rrect(1800, 120, 2140, 480, 10, fill=(236, 220, 180, 255), outline=GOLD, width=24); d.ellipse(1970, 280, 90, 90, fill=SK[0][0], outline=LINE, width=8); d.chord(1970, 240, 96, 70, 180, 360, fill=(120, 90, 60, 255))
    d.out().save(path)


def bountywall(path):                                        # bounty office: pay window with a sign, notice, safe, clock
    W, Hh = 2400, 1100; d = Draw(W, Hh); d.rect(0, 0, W, Hh, (226, 214, 180, 255)); d.rect(0, 700, W, Hh, (150, 110, 70, 255)); d.stroke([(0, 700), (W, 700)], LINE, 10)
    d.rrect(980, 250, 1420, 340, 18, fill=(40, 100, 70, 255), outline=LINE, width=10); d.text(1200, 296, 'BOUNTY OFFICE', 54, (255, 226, 120, 255), stroke=4, stroke_fill=LINE)
    d.rrect(980, 370, 1420, 700, 14, fill=(150, 200, 220, 255), outline=(110, 80, 54, 255), width=18)
    for x in range(1030, 1420, 55): d.stroke([(x, 380), (x, 690)], (110, 80, 54, 255), 6)
    d.rrect(260, 300, 560, 700, 20, fill=(90, 94, 104, 255), outline=LINE, width=14); d.ellipse(410, 470, 60, 60, fill=(196, 200, 210, 255), outline=LINE, width=10)
    d.ellipse(1960, 260, 110, 110, fill=WHITE, outline=LINE, width=14); d.stroke([(1960, 260), (1960, 180)], LINE, 12); d.stroke([(1960, 260), (2020, 300)], LINE, 10)
    d.out().save(path)


def redsand(path, n=512):
    R_ = np.random.RandomState(6); a = np.zeros((n, n, 3)) + np.array([206, 112, 66]); a += R_.normal(0, 9, (n, n, 1)); G.save_tex(a, path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, body
    for ch in NEW: layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked', 'shouting')]
    multi = dict(emu={'default': emu('smug'), 'happy': emu('happy'), 'shocked': emu('shocked'), 'run': emu('happy', run=True)},
                 lewis={'default': lewis(), 'fire': lewis('fire')}, wheat={'default': wheat(), 'wrecked': wheat(True)})
    for nm, faces in multi.items():
        G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    B.sparkle(Pp('sparkle.png'))
    cards = dict(emutank=emutank(), herd=herd(), truck=truck(), ammo=ammo(), cash=cash(), trophy=trophy(), feathers=feathers(), ozmap=ozmap(),
                 atwar=btag('AUSTRALIA GOES TO WAR', 1300, 82), feathert=V.wtag('FEATHERS?!', 760, (126, 70, 140, 255), 96), emuwins=CA.stamp('EMUS WIN!', 760, 116),
                 y1932=V.big_card('1932', 'NOVEMBER', BLUE, 720), drought=CA.stamp('DROUGHT!', 760, 112), e20k=V.wtag('20,000 EMUS!', 900, (150, 98, 56, 255), 92),
                 vets=V.wtag('WWI VETERANS', 900, (60, 120, 80, 255), 86), wrecked=CA.stamp('WRECKED!', 760, 114), help=B.sticker_burst('HELP!'),
                 pearcet=btag('MINISTER PEARCE', 1060, 84), approved=CA.stamp('APPROVED!', 800, 110), soldiers3=V.wtag('3 SOLDIERS', 760, (120, 100, 60, 255), 92),
                 guns2=V.wtag('2 LEWIS GUNS', 840, (84, 100, 74, 255), 88), r10k=V.wtag('10,000 ROUNDS', 940, RED, 84), week=V.big_card('1', 'WEEK LATER', BLUE, 600),
                 r2500=CA.stamp('2,500 GONE!', 860, 104), pulled=CA.stamp('PULLED OUT!', 860, 104), round2=V.wtag('ROUND 2!', 700, RED, 100),
                 same=CA.stamp('SAME RESULT', 860, 100), r9860=V.wtag('9,860 FIRED', 860, RED, 90), b986=V.wtag('986 BIRDS', 760, (150, 98, 56, 255), 94),
                 per10=V.big_card('10', 'BULLETS PER EMU', RED, 760), majort=btag('MAJOR MEREDITH', 1000, 84), tanks=CA.stamp('LIKE TANKS!', 820, 110),
                 nosoldiers=CA.stamp('NO MORE SOLDIERS', 1080, 92), bounty=V.wtag('BOUNTY PER BIRD', 1000, (60, 140, 80, 255), 84), noguns=CA.stamp('NO GUNS. NO ARMY.', 1120, 88),
                 y1934=V.big_card('1934', '6 MONTHS', (60, 140, 80, 255), 720), b57k=V.wtag('57,000 BOUNTIES', 1000, (60, 140, 80, 255), 84),
                 x58=V.big_card('58x', 'MORE THAN GUNS', (60, 140, 80, 255), 760), lost=CA.stamp('BULLETS LOST', 900, 100), won=V.wtag('CASH WON!', 760, (60, 140, 80, 255), 98),
                 boom=B.sticker_burst('RAT-A-TAT!', fill=(255, 190, 70, 255)), qmark=B.sticker_mark('?', GOLD), sparkle=Image.open(Pp('sparkle.png')).convert('RGBA'))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); B.tex_dirt(T('dirt.jpg')); B.tex_grass(T('grass.jpg')); redsand(T('redsand.jpg')); tiles(T('btiles.jpg'), (236, 226, 200), (196, 170, 130))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg'))
    wheatrow(Pp('wheatrow.png')); windmill(Pp('windmill.png')); outback(Pp('outback.png')); office(Pp('office.png')); bountywall(Pp('bountywall.png'))
    VA.skyplane(Pp('skyday.png'), (92, 150, 226), (226, 240, 252), hills=(170, 150, 90))
    for n in ('wheatrow', 'windmill', 'outback', 'office', 'bountywall'): items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
