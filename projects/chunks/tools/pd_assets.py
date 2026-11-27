#!/usr/bin/env python3
"""Assets for video 17: Play-Doh was wallpaper cleaner.  Candy-clay world: cute cast (kids, Kay, Joe, two homemakers),
glossy hero props with faces (cleaner can, Play-Doh can, dough blob), ten painted sets, plaques.
usage: make_assets.py <project> <font>"""
import os, math, json
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import corrigan_assets as CA
import catseyes_assets as CE
import lordgta_assets as LA
import mco_assets as M
import mono_assets as MA
from assets_base import Draw, LINE, WHITE, H

ROOT = B.ROOT; GOLD, GOLDL = LA.GOLD, M.GOLDL
dk, glow, plaque, stamp, sky, W2, H2, fl, faceon = LA.dk, CE.glow, LA.plaque, LA.stamp, M.sky, M.W2, M.H2, MA.fl, MA.faceon
WT, LIME, PINK, CYAN, YEL, ORNG, TEAL, NAVY, RED = (250, 250, 245, 255), (120, 230, 90, 255), (255, 90, 160, 255), (120, 220, 255, 255), (255, 206, 50, 255), (250, 140, 50, 255), (40, 170, 150, 255), (40, 60, 150, 255), (226, 52, 52, 255)
LIL, MINT, PEACH, CORAL, SEP = (190, 150, 240, 255), (150, 230, 200, 255), (255, 200, 160, 255), (255, 120, 110, 255), (200, 150, 90, 255)
LA.NEW.update({
    'kida': dict(sk=1, style='bob', hair=(120, 70, 40, 255), suit=(255, 110, 170, 255), shade=(220, 80, 140, 255), body='sweater', band=YEL),
    'kidb': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=(255, 200, 40, 255), shade=(220, 166, 30, 255), body='denim', freck=1),
    'kay': dict(sk=0, style='bob', bun=1, hair=(196, 100, 56, 255), suit=TEAL, shade=(30, 136, 120, 255), body='cardigan', glasses=1, band=PINK),
    'joe': dict(sk=0, style='side', hair=(60, 44, 34, 255), suit=NAVY, shade=(30, 44, 116, 255), body='suit', tie=RED, hat='fedora'),
    'mom': dict(sk=1, style='bob', hair=(90, 60, 50, 255), suit=(150, 120, 200, 255), shade=(120, 94, 170, 255), body='cardigan', band=(250, 240, 220, 255)),
    'mom50': dict(sk=2, style='curly', hair=(40, 30, 30, 255), suit=CORAL, shade=(220, 90, 84, 255), body='sweater', band=MINT),
})


def eyes(d, cx, cy, s, face):                               # big shiny cute eyes + mouth for props
    sh, sad = face == 'shocked', face == 'sad'
    for sg in (-1, 1):
        d.ellipse(cx + sg * 62 * s, cy, 34 * s, (46 if sh else 40) * s, fill=WHITE, outline=LINE, width=int(9 * s) + 2)
        d.dot(cx + sg * 62 * s + 6 * s, cy + 8 * s, (16 if sh else 21) * s, LINE); d.dot(cx + sg * 62 * s + 14 * s, cy - 6 * s, 8 * s, WHITE)
        d.ellipse(cx + sg * 112 * s, cy + 52 * s, 24 * s, 14 * s, fill=(255, 130, 130, 200))
        if sad: d.stroke([(cx + sg * 34 * s, cy - 58 * s), (cx + sg * 92 * s, cy - 44 * s)], LINE, int(10 * s) + 2)
    if sh: d.ellipse(cx, cy + 74 * s, 26 * s, 32 * s, fill=(120, 30, 40, 255), outline=LINE, width=int(8 * s) + 2)
    elif sad: d.arc(cx, cy + 92 * s, 34 * s, 20 * s, 200, 340, LINE, int(10 * s) + 2)
    else: d.chord(cx, cy + 56 * s, 42 * s, 36 * s, 0, 180, fill=(120, 30, 40, 255), outline=LINE, width=int(8 * s) + 2)


def shine(d, x, y, h, w=26): d.rrect(x, y, x + w, y + h, w / 2, fill=(255, 255, 255, 150))


def can(kind, face='default'):                               # glossy tin can, lid on top, big label + face
    d = Draw(760, 980); body, lid = ((200, 206, 214, 255), (170, 176, 186, 255)) if kind == 'old' else ((255, 210, 50, 255), (250, 190, 30, 255))
    d.rrect(90, 150, 670, 930, 60, fill=body, outline=LINE, width=16); d.ellipse(380, 930, 290, 46, fill=dk(body, 0.85), outline=LINE, width=14); d.rrect(90, 150, 670, 860, 60, fill=body)
    d.ellipse(380, 150, 300, 70, fill=lid, outline=LINE, width=16); d.ellipse(380, 150, 230, 42, outline=dk(lid, 0.8), width=10)
    lab = (226, 60, 50, 255) if kind == 'old' else (230, 56, 70, 255)
    d.rect(92, 300, 668, 560, lab); d.stroke([(92, 300), (668, 300)], LINE, 12); d.stroke([(92, 560), (668, 560)], LINE, 12)
    if kind == 'old': d.text(380, 380, 'WALLPAPER', LA.fit('WALLPAPER', 104, 440), WT, stroke=6, stroke_fill=LINE); d.text(380, 490, 'CLEANER', LA.fit('CLEANER', 104, 440), YEL, stroke=6, stroke_fill=LINE)
    else: d.text(380, 430, 'PLAY-DOH', LA.fit('PLAY-DOH', 140, 460), WT, stroke=8, stroke_fill=LINE)
    shine(d, 130, 200, 600); eyes(d, 380, 690, 1.15, face); return d.out()


def dough(face='default', col=(246, 236, 214, 255)):        # soft putty blob with a face
    d = Draw(900, 760); r = np.random.RandomState(4)
    pts = [(450 + (380 + 30 * math.sin(a * 5)) * math.cos(math.radians(a * 30 / 3.14159 * 3.14159)), 430 + (300 + 26 * math.cos(a * 4)) * math.sin(math.radians(a * 30 / 3.14159 * 3.14159))) for a in range(0, 12)]
    d.ellipse(450, 440, 390, 290, fill=col, outline=LINE, width=16); d.ellipse(330, 300, 120, 60, fill=(255, 255, 255, 150))
    for _ in range(14): d.dot(160 + r.randint(0, 580), 260 + r.randint(0, 340), 8, dk(col, 0.9))
    eyes(d, 450, 450, 1.2, face); return d.out()


def wallp(clean=False):                                      # wallpaper panel: grey soot, or one bright clean stripe + dough roll
    d = Draw(1000, 1200); base = (150, 144, 136, 255); d.rect(20, 20, 980, 1180, base)
    for y in range(80, 1180, 180):
        for x in range(90 if (y // 180) % 2 else 180, 980, 180): d.dot(x, y, 38, (126, 120, 112, 255)); d.dot(x, y, 14, (110, 104, 98, 255))
    r = np.random.RandomState(2)
    for _ in range(40): d.dot(r.randint(40, 960), r.randint(40, 1160), r.randint(20, 70), (90, 86, 82, 120))
    if clean:
        d.rect(380, 20, 640, 1180, (255, 236, 214, 255))
        for y in range(80, 1180, 180): d.dot(510, y, 38, (255, 160, 190, 255)); d.dot(510, y, 14, (120, 200, 150, 255))
        d.ellipse(510, 900, 190, 130, fill=(70, 66, 62, 255), outline=LINE, width=14); d.ellipse(470, 870, 60, 30, fill=(110, 106, 100, 255))
        for k in range(5): d.stroke([(400 + k * 50, 300), (420 + k * 50, 360)], (255, 255, 255, 230), 10)
    d.poly([(20, 20), (980, 20), (980, 1180), (20, 1180)], outline=LINE, width=16); return d.out()


def stove(face='default'):                                   # pot-belly coal stove, glowing window, soot cloud
    d = Draw(800, 1100); hot = face != 'sad'
    if hot:
        for x, y, rr in ((300, 170, 110), (420, 120, 130), (540, 190, 100), (400, 230, 90)): d.dot(x, y, rr, (96, 92, 98, 235))
    d.rect(370, 240, 430, 420, (90, 90, 100, 255)); d.stroke([(370, 240), (370, 420)], LINE, 10); d.stroke([(430, 240), (430, 420)], LINE, 10)
    d.ellipse(400, 690, 270, 300, fill=(110, 108, 124, 255), outline=LINE, width=16); d.ellipse(400, 440, 220, 50, fill=(130, 128, 144, 255), outline=LINE, width=14)
    d.rrect(290, 700, 510, 860, 30, fill=(255, 150, 50, 255) if hot else (70, 66, 72, 255), outline=LINE, width=12)
    if hot: d.poly([(330, 850), (360, 760), (400, 820), (440, 740), (470, 850)], fill=(255, 230, 90, 255))
    for x in (230, 570): d.stroke([(x, 940), (x - 20 * (1 if x < 400 else -1), 1060)], LINE, 26)
    eyes(d, 400, 590, 0.9, 'happy' if hot else 'sad'); return d.out()


def furnace():                                               # 1950s gas furnace: cream cabinet, blue flame window
    d = Draw(760, 1100); d.rrect(100, 160, 660, 1060, 50, fill=(250, 244, 226, 255), outline=LINE, width=16); d.rect(100, 160, 660, 260, (120, 210, 200, 255)); d.stroke([(100, 260), (660, 260)], LINE, 12)
    d.rrect(240, 760, 520, 960, 30, fill=(30, 40, 90, 255), outline=LINE, width=12)
    for k in range(6): d.poly([(270 + k * 42, 940), (290 + k * 42, 830 - (k % 2) * 30), (310 + k * 42, 940)], fill=(80, 170, 255, 255)); d.poly([(282 + k * 42, 940), (290 + k * 42, 880), (298 + k * 42, 940)], fill=(200, 240, 255, 255))
    shine(d, 130, 300, 600); eyes(d, 380, 480, 1.1, 'happy'); return d.out()


def vinyl():                                                 # roll of washable vinyl wallpaper + sponge + sparkles
    d = Draw(1000, 800); d.rrect(80, 180, 760, 620, 40, fill=(160, 230, 210, 255), outline=LINE, width=16)
    for x in range(140, 740, 90): d.rect(x, 184, x + 40, 616, (255, 170, 190, 255))
    d.ellipse(760, 400, 110, 220, fill=(130, 210, 190, 255), outline=LINE, width=16); d.ellipse(760, 400, 40, 90, fill=(250, 250, 240, 255), outline=LINE, width=10)
    d.rrect(720, 560, 960, 700, 30, fill=(255, 220, 60, 255), outline=LINE, width=12)
    for x, y, s in ((200, 120, 60), (600, 110, 44), (900, 300, 50)): d.poly([(x, y - s), (x + s * 0.25, y - s * 0.25), (x + s, y), (x + s * 0.25, y + s * 0.25), (x, y + s), (x - s * 0.25, y + s * 0.25), (x - s, y), (x - s * 0.25, y - s * 0.25)], fill=WT, outline=LINE, width=6)
    eyes(d, 420, 400, 0.9, 'happy'); return d.out()


def clay():                                                  # kids' clay art on a board: snail, snake, star, flower
    d = Draw(1200, 760); d.rrect(40, 520, 1160, 700, 40, fill=(200, 150, 100, 255), outline=LINE, width=14)
    d.ellipse(260, 420, 150, 130, fill=(255, 120, 170, 255), outline=LINE, width=14); d.arc(260, 420, 90, 80, 0, 300, LINE, 12); d.rrect(120, 470, 470, 540, 30, fill=(150, 220, 120, 255), outline=LINE, width=12)
    for k in range(7): d.dot(560 + k * 50, 500 - 30 * math.sin(k), 36, (90, 170, 255, 255))
    d.ellipse(560, 500, 36, 36, outline=LINE, width=8); d.dot(890, 480, 30, LINE)
    cx, cy, R = 960, 330, 130; d.poly([(cx + (R if k % 2 == 0 else R * 0.45) * math.cos(math.radians(k * 36 - 90)), cy + (R if k % 2 == 0 else R * 0.45) * math.sin(math.radians(k * 36 - 90))) for k in range(10)], fill=YEL, outline=LINE, width=12)
    for k in range(6): a = math.radians(k * 60); d.dot(700 + 70 * math.cos(a), 250 + 70 * math.sin(a), 46, ORNG)
    d.dot(700, 250, 40, (255, 240, 120, 255)); eyes(d, 260, 400, 0.45, 'happy'); eyes(d, 960, 330, 0.45, 'happy'); return d.out()


def magazine():                                              # craft magazine: picture of putty art (no words)
    d = Draw(780, 1000); d.rrect(20, 20, 760, 980, 24, fill=(255, 246, 230, 255), outline=LINE, width=16); d.rect(60, 60, 720, 180, (110, 70, 200, 255))
    for x in range(100, 700, 120): d.dot(x, 120, 30, YEL)
    d.rrect(80, 230, 700, 760, 20, fill=(150, 230, 210, 255), outline=LINE, width=10)
    for k, c in enumerate(((255, 120, 170, 255), YEL, (90, 170, 255, 255))): d.ellipse(200 + k * 190, 560 - (k % 2) * 80, 90, 80, fill=c, outline=LINE, width=10)
    for y in range(820, 950, 40): d.rect(90, y, 690, y + 16, (180, 170, 160, 255))
    return d.out()


def tv():                                                    # 1950s wooden TV, rabbit ears, clay shapes on the screen
    d = Draw(1000, 1000); d.stroke([(500, 220), (330, 40)], LINE, 14); d.stroke([(500, 220), (680, 40)], LINE, 14); d.dot(330, 40, 20, RED); d.dot(680, 40, 20, RED)
    d.rrect(60, 200, 940, 860, 60, fill=(190, 120, 70, 255), outline=LINE, width=18); d.rrect(120, 260, 700, 800, 70, fill=(110, 210, 230, 255), outline=LINE, width=14)
    d.ellipse(300, 600, 90, 80, fill=(255, 120, 170, 255), outline=LINE, width=10); d.ellipse(500, 560, 80, 110, fill=YEL, outline=LINE, width=10); d.ellipse(410, 420, 60, 60, fill=(120, 230, 90, 255), outline=LINE, width=10)
    shine(d, 150, 300, 300, 30)
    for y in (380, 520): d.dot(820, y, 50, (240, 200, 120, 255)); d.ellipse(820, y, 50, 50, outline=LINE, width=10)
    for x in (160, 840): d.stroke([(x, 860), (x, 960)], LINE, 26)
    return d.out()


def trophy(hidden=False):                                    # gold cup + star, or a covered "?" silhouette (the open loop)
    d = Draw(800, 1000)
    if hidden:
        d.poly([(400, 80), (680, 900), (120, 900)], fill=(110, 70, 170, 255), outline=LINE, width=16); d.ellipse(400, 900, 280, 50, fill=(90, 56, 140, 255), outline=LINE, width=14)
        d.text(400, 560, '?', 420, YEL, stroke=14, stroke_fill=LINE); return d.out()
    d.chord(400, 300, 260, 300, 0, 180, fill=(255, 200, 60, 255), outline=LINE, width=16); d.rect(150, 280, 650, 310, (255, 200, 60, 255)); d.stroke([(140, 300), (660, 300)], LINE, 14)
    for sg in (-1, 1): d.arc(400 + sg * 270, 380, 80, 100, 90 if sg > 0 else -90, 270 if sg > 0 else 90, LINE, 22)
    d.rect(360, 600, 440, 760, (240, 180, 40, 255)); d.rrect(220, 760, 580, 900, 20, fill=(150, 90, 60, 255), outline=LINE, width=14)
    cx, cy, R = 400, 140, 110; d.poly([(cx + (R if k % 2 == 0 else R * 0.45) * math.cos(math.radians(k * 36 - 90)), cy + (R if k % 2 == 0 else R * 0.45) * math.sin(math.radians(k * 36 - 90))) for k in range(10)], fill=(255, 240, 120, 255), outline=LINE, width=10)
    shine(d, 230, 330, 160); eyes(d, 400, 420, 0.8, 'happy'); return d.out()


def cans():                                                  # a mountain of little yellow cans
    d = Draw(1400, 900)
    for row in range(6):
        n = 7 - row
        for k in range(n):
            x, y = 700 + (k - (n - 1) / 2) * 180, 790 - row * 130; c = (RED, YEL, (90, 170, 255, 255), (120, 230, 90, 255), PINK)[(k + row) % 5]
            d.rrect(x - 80, y - 110, x + 80, y + 40, 20, fill=(255, 210, 50, 255), outline=LINE, width=10); d.ellipse(x, y - 110, 82, 22, fill=c, outline=LINE, width=8); d.rect(x - 78, y - 60, x + 78, y - 10, (230, 56, 70, 255))
    return d.out()


def whirl():                                                 # the drain: a blue whirlpool funnel
    d = Draw(1200, 900)
    for k in range(9):
        w = 560 - k * 58; y = 220 + k * 70; c = (60 + k * 8, 150 + k * 6, 230 - k * 6, 255); d.ellipse(600 + 20 * math.sin(k), y, w, 70, fill=c, outline=LINE, width=8)
    d.ellipse(600, 860, 60, 30, fill=(30, 40, 70, 255), outline=LINE, width=8)
    for k in range(6): d.arc(600, 380 + k * 60, 400 - k * 50, 50, 200, 340, (230, 250, 255, 255), 8)
    return d.out()


def soap():                                                  # a stack of soap bars with bubbles
    d = Draw(1000, 800)
    for k, c in enumerate(((150, 230, 200, 255), (255, 190, 210, 255), (255, 236, 150, 255))): d.rrect(200 + k * 30, 560 - k * 170, 800 - k * 30, 720 - k * 170, 50, fill=c, outline=LINE, width=14); shine(d, 260 + k * 30, 590 - k * 170, 30, 200)
    for x, y, rr in ((150, 200, 60), (860, 160, 80), (780, 320, 40), (240, 90, 40), (520, 80, 50)): d.ellipse(x, y, rr, rr, fill=(220, 250, 255, 120), outline=(90, 160, 220, 255), width=6); d.dot(x - rr * 0.3, y - rr * 0.3, rr * 0.2, WT)
    eyes(d, 500, 300, 0.7, 'happy'); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def dots(d, col, step=150, r=22, y1=940):
    for y in range(60, y1, step):
        for x in range(60 if (y // step) % 2 else 135, W2, step): d.dot(x, y, r, col)


def win(d, x0, y0, x1, y1, skyc, frame=WT):
    d.rect(x0, y0, x1, y1, skyc); d.rrect(x0, y0, x1, y1, 16, outline=frame, width=26); d.stroke([((x0 + x1) / 2, y0), ((x0 + x1) / 2, y1)], frame, 18); d.stroke([(x0, (y0 + y1) / 2), (x1, (y0 + y1) / 2)], frame, 18)


def playroom(path):                                          # candy playroom: lilac wall, mint polka dots, cotton-candy window, toy shelf
    im = sky((236, 170, 230), (255, 214, 236), 1.0); d = Draw(W2, H2); dots(d, (170, 240, 210, 255))
    win(d, 1500, 160, 2000, 620, (150, 210, 255, 255)); [d.dot(x, y, r, WT) for x, y, r in ((1600, 300, 50), (1660, 290, 60), (1720, 310, 46), (1850, 480, 44), (1900, 470, 54))]
    d.rrect(200, 420, 900, 450, 10, fill=(255, 180, 90, 255), outline=LINE, width=8)
    for k, c in enumerate((RED, YEL, (90, 170, 255, 255), (120, 230, 90, 255))): d.rrect(240 + k * 150, 300, 360 + k * 150, 420, 14, fill=c, outline=LINE, width=8)
    for k in range(13): x = 100 + k * 180; d.poly([(x, 40), (x + 160, 40), (x + 80, 130)], fill=(PINK, YEL, CYAN, LIME)[k % 4], outline=LINE, width=6)
    d.rect(0, 760, W2, 940, (150, 230, 210, 255)); d.stroke([(0, 760), (W2, 760)], LINE, 10)
    fl(d, (255, 190, 220, 255)); im.alpha_composite(d.out()); glow(im, 1750, 390, 400, (255, 255, 230, 90), 80); im.convert('RGB').save(path)


def cincy(path):                                             # 1930s Cincinnati: amber smoky sky, brick skyline, stacks, river + suspension bridge
    im = sky((240, 170, 90), (255, 226, 160), 1.0); d = Draw(W2, H2); r = np.random.RandomState(8)
    for x, y, rr in ((300, 200, 120), (500, 160, 150), (1500, 140, 140), (1800, 220, 110), (2100, 150, 130)): d.dot(x, y, rr, (190, 150, 120, 140))
    for k in range(18):
        x = k * 140; h = 260 + r.randint(0, 300); d.rect(x, 760 - h, x + 120, 780, (150 - k % 3 * 15, 90, 60, 255))
        for wy in range(800 - h, 760, 50): d.rect(x + 20, wy, x + 40, wy + 22, (255, 220, 120, 255)); d.rect(x + 70, wy, x + 90, wy + 22, (255, 220, 120, 255))
    for x in (420, 1240, 1960): d.rect(x, 280, x + 50, 600, (120, 70, 50, 255)); d.dot(x + 25, 250, 60, (120, 110, 110, 200)); d.dot(x + 60, 190, 80, (140, 130, 130, 170))
    d.rect(0, 780, W2, 940, (90, 140, 150, 255))
    for x in (700, 1700): d.rect(x - 40, 520, x + 40, 900, (130, 80, 60, 255)); d.rect(x - 60, 520, x + 60, 560, (110, 66, 50, 255))
    d.arc(1200, 520, 500, 220, 0, 180, LINE, 10); d.stroke([(0, 800), (W2, 800)], (110, 70, 50, 255), 24)
    fl(d, (200, 150, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 600, (255, 200, 120, 80), 100); im.convert('RGB').save(path)


def factory(path):                                           # Kutol soap works: teal tile wall, copper vats, pipes, bubbles, warm windows
    im = sky((60, 150, 150), (110, 200, 190), 1.0); d = Draw(W2, H2)
    for y in range(0, 940, 90): d.stroke([(0, y), (W2, y)], (80, 170, 160, 255), 6)
    for x in (300, 1900): win(d, x, 120, x + 300, 460, (255, 220, 140, 255), (90, 70, 60, 255))
    for x in (800, 1300): d.ellipse(x, 640, 220, 260, fill=(210, 120, 60, 255), outline=LINE, width=14); d.ellipse(x, 400, 220, 50, fill=(240, 160, 90, 255), outline=LINE, width=12); d.rect(x - 160, 520, x - 120, 760, (255, 190, 120, 140))
    d.stroke([(0, 200), (W2, 200)], (200, 110, 60, 255), 30); d.stroke([(1050, 200), (1050, 380)], (200, 110, 60, 255), 26)
    for x, y, rr in ((600, 300, 40), (1050, 120, 60), (1550, 260, 46), (2200, 600, 50)): d.ellipse(x, y, rr, rr, fill=(230, 250, 255, 110), outline=(255, 255, 255, 220), width=6)
    fl(d, (90, 120, 110, 255)); im.alpha_composite(d.out()); glow(im, 450, 290, 300, (255, 220, 140, 80), 60); glow(im, 2050, 290, 300, (255, 220, 140, 80), 60); im.convert('RGB').save(path)


def sooty(path):                                             # coal-heated home: grey flower wallpaper with soot, smoky window, ember glow
    im = sky((150, 140, 136), (176, 166, 160), 1.0); d = Draw(W2, H2)
    for y in range(60, 940, 150):
        for x in range(60 if (y // 150) % 2 else 135, W2, 150): d.dot(x, y, 30, (130, 120, 116, 255)); d.dot(x, y, 10, (120, 100, 100, 255))
    r = np.random.RandomState(5)
    for _ in range(60): d.dot(r.randint(0, W2), r.randint(0, 900), r.randint(30, 110), (100, 94, 92, 90))
    win(d, 1700, 180, 2100, 560, (170, 170, 176, 255), (120, 90, 70, 255)); d.dot(1850, 300, 90, (120, 120, 126, 255))
    for x, y in ((500, 300), (900, 260)): d.rrect(x, y, x + 200, y + 150, 10, fill=(200, 170, 120, 255), outline=(110, 80, 50, 255), width=16)
    fl(d, (120, 90, 70, 255)); im.alpha_composite(d.out()); glow(im, 300, 800, 500, (255, 140, 60, 110), 120); im.convert('RGB').save(path)


def atomic(path):                                            # 1950s atomic home: mint wall, coral boomerangs, starburst clock, sunny suburb window
    im = sky((150, 226, 210), (210, 250, 236), 1.0); d = Draw(W2, H2)
    for k in range(16): x, y = 120 + (k * 330) % 2300, 100 + (k * 170) % 700; d.arc(x, y, 70, 30, 200, 340, (255, 120, 110, 255), 14)
    win(d, 1500, 140, 2200, 620, (120, 200, 255, 255)); d.ellipse(1850, 560, 400, 70, fill=(110, 200, 110, 255))
    for x in (1620, 1800, 2000): d.poly([(x - 60, 560), (x, 480), (x + 60, 560)], fill=(255, 140, 120, 255), outline=LINE, width=6); d.rect(x - 50, 560, x + 50, 600, WT)
    cx, cy = 600, 300; [d.stroke([(cx, cy), (cx + 170 * math.cos(math.radians(a)), cy + 170 * math.sin(math.radians(a)))], (240, 180, 60, 255), 10) for a in range(0, 360, 30)]
    d.dot(cx, cy, 80, WT); d.ellipse(cx, cy, 80, 80, outline=LINE, width=10); d.stroke([(cx, cy), (cx, cy - 55)], LINE, 10); d.stroke([(cx, cy), (cx + 40, cy)], LINE, 10)
    d.rect(0, 760, W2, 940, (255, 150, 140, 255)); d.stroke([(0, 760), (W2, 760)], LINE, 10)
    fl(d, (250, 236, 200, 255)); im.alpha_composite(d.out()); glow(im, 1850, 380, 420, (255, 255, 220, 90), 80); im.convert('RGB').save(path)


def bath(path):                                              # aqua tiled bathroom, round mirror, bubbles everywhere
    im = sky((80, 190, 210), (150, 230, 236), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.stroke([(x, 0), (x, 940)], (120, 220, 230, 255), 6)
    for y in range(0, 940, 120): d.stroke([(0, y), (W2, y)], (120, 220, 230, 255), 6)
    d.ellipse(1200, 330, 260, 230, fill=(200, 240, 250, 255), outline=(250, 250, 255, 255), width=24)
    r = np.random.RandomState(9)
    for _ in range(26): x, y, rr = r.randint(0, W2), r.randint(0, 900), r.randint(20, 70); d.ellipse(x, y, rr, rr, fill=(230, 250, 255, 100), outline=WT, width=5)
    fl(d, (230, 246, 250, 255)); im.alpha_composite(d.out()); glow(im, 1200, 330, 300, (255, 255, 255, 90), 60); im.convert('RGB').save(path)


def school(path):                                            # nursery class: sunny yellow wall, rainbow, kid drawings on a string, chalkboard
    im = sky((255, 220, 90), (255, 240, 170), 1.0); d = Draw(W2, H2)
    for k, c in enumerate((RED, ORNG, YEL, LIME, (90, 170, 255, 255), LIL)): d.arc(1800, 520, 400 - k * 40, 330 - k * 40, 180, 360, c, 40)
    d.rrect(240, 200, 1000, 620, 20, fill=(50, 110, 80, 255), outline=(170, 110, 60, 255), width=26)
    for k, (x, y) in enumerate(((400, 330), (600, 420), (800, 300))): d.ellipse(x, y, 70, 50, outline=WT, width=8)
    d.arc(1200, 60, 1200, 60, 0, 180, LINE, 6)
    for k in range(9): x = 120 + k * 260; d.rect(x, 80, x + 160, 220, (255, 255, 250, 255)); d.dot(x + 80, 150, 40, (PINK, CYAN, LIME, ORNG)[k % 4])
    d.rect(0, 760, W2, 940, (110, 190, 255, 255)); d.stroke([(0, 760), (W2, 760)], LINE, 10)
    fl(d, (240, 180, 110, 255)); im.alpha_composite(d.out()); glow(im, 1800, 400, 500, (255, 255, 220, 80), 80); im.convert('RGB').save(path)


def store(path):                                             # 1956 department store: red + cream columns, garlands, big display windows, chandeliers
    im = sky((200, 50, 60), (250, 130, 110), 1.0); d = Draw(W2, H2)
    for x in range(100, W2, 400): d.rect(x, 0, x + 90, 940, (250, 236, 206, 255)); d.rect(x - 15, 0, x + 105, 60, (240, 200, 120, 255))
    for x in range(260, W2, 400): win(d, x, 280, x + 220, 640, (255, 236, 180, 255), (240, 200, 120, 255))
    for x in range(0, W2, 200): d.arc(x + 100, 130, 100, 60, 0, 180, (60, 160, 90, 255), 20); d.dot(x + 100, 190, 18, YEL)
    for x in (700, 1500): d.stroke([(x, 0), (x, 120)], LINE, 6); d.ellipse(x, 150, 90, 40, fill=(255, 236, 160, 255), outline=LINE, width=8)
    fl(d, (240, 220, 190, 255)); im.alpha_composite(d.out()); glow(im, 700, 160, 200, (255, 240, 180, 120), 50); glow(im, 1500, 160, 200, (255, 240, 180, 120), 50); im.convert('RGB').save(path)


def studio(path):                                            # 1950s TV studio: purple velvet curtain, spotlight cones, stars, camera silhouettes
    im = sky((90, 50, 160), (170, 110, 220), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 120): d.rect(x, 0, x + 60, 940, (120, 70, 190, 255))
    for x in (400, 1200, 2000): d.poly([(x, 0), (x - 260, 940), (x + 260, 940)], fill=(255, 250, 210, 60))
    for k in range(20): x, y = (k * 523) % W2, (k * 211) % 700; d.poly([(x, y - 30), (x + 8, y - 8), (x + 30, y), (x + 8, y + 8), (x, y + 30), (x - 8, y + 8), (x - 30, y), (x - 8, y - 8)], fill=(255, 240, 160, 255))
    fl(d, (70, 40, 110, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 500, (255, 240, 200, 70), 90); im.convert('RGB').save(path)


def fame(path):                                              # Hall of Fame: gold columns, red velvet, spotlights, gold confetti
    im = sky((180, 120, 30), (250, 210, 110), 1.0); d = Draw(W2, H2)
    for x in (0, 2100): d.rect(x, 0, x + 300, 940, (190, 40, 60, 255))
    for x in range(400, 2100, 340): d.rect(x, 80, x + 110, 940, (255, 220, 120, 255)); d.rect(x - 20, 60, x + 130, 110, (240, 190, 80, 255)); d.stroke([(x + 30, 120), (x + 30, 920)], (220, 170, 70, 255), 10)
    r = np.random.RandomState(11)
    for _ in range(90): x, y = r.randint(0, W2), r.randint(0, 900); d.rect(x, y, x + 18, y + 10, (RED, YEL, PINK, CYAN, WT)[r.randint(0, 5)])
    fl(d, (170, 40, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 400, 600, (255, 240, 190, 90), 100); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = MA.head, LA.body
    for ch in ('kida', 'kidb', 'kay', 'joe', 'mom', 'mom50'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked')]
    multi = dict(can={'default': can('old'), 'shocked': can('old', 'shocked'), 'sad': can('old', 'sad')}, pdcan={'default': can('new'), 'shocked': can('new', 'shocked')},
                 dough={'default': dough(), 'shocked': dough('shocked')}, wallp={'default': wallp(), 'clean': wallp(True)}, stove={'default': stove(), 'sad': stove('sad')},
                 furnace={'default': furnace()}, vinyl={'default': vinyl()}, clay={'default': clay()}, mag={'default': magazine()}, tv={'default': tv()},
                 trophy={'default': trophy(), 'q': trophy(True)}, cans={'default': cans()}, whirl={'default': whirl()}, soap={'default': soap()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    P_ = lambda a, b, bg, w=1000, bs=130, ss=130, bd=GOLDL: plaque(a, b, bg, WHITE, w, border=bd, bs=bs, ss=ss, sc=bd)
    cards = dict(hookc=P_('WALLPAPER', 'CLEANER!', RED, 1000, 190, 190),
                 wait=stamp('WAIT FOR IT...', 860, (110, 70, 200, 255), 120, 4),
                 cinci=MA.street('CINCINNATI', (40, 110, 140, 255)),
                 kutol=P_('KUTOL PRODUCTS', 'A SMALL SOAP COMPANY', TEAL, 1000, 120, 96),
                 coal=P_('HOMES', 'BURNED COAL', (90, 80, 80, 255), 900, 150, 150, ORNG),
                 gray=stamp('EVERY WALL GRAY!', 940, (110, 106, 110, 255), 120, -4),
                 best=M.bigneon('BEST SELLER:', 'DOUGHY PUTTY!', 980, YEL, PINK),
                 rolled=P_('ROLL IT ACROSS', 'THE WALLPAPER', (170, 110, 200, 255), 980, 120, 120, WT),
                 dirt=stamp('DIRT GONE!', 820, (60, 170, 110, 255), 140, 3),
                 ww2=M.cal('AFTER', 'WW2', (60, 90, 170, 255)),
                 gasoil=P_('GAS + OIL', 'HEAT!', (40, 120, 220, 255), 900, 160, 170, CYAN),
                 nosoot=stamp('NO SOOT!', 760, (240, 120, 40, 255), 150, -4),
                 nowalls=M.bigneon('NO DIRTY', 'WALLS!', 880, CYAN, LIME),
                 vinylc=P_('WASHABLE VINYL', 'WALLPAPER', (230, 100, 120, 255), 980, 120, 150),
                 drain=M.bigneon('BIGGEST HIT...', 'DOWN THE DRAIN!', 1000, PINK, CYAN),
                 rescue=P_('THE RESCUE CAME', 'FROM THE FAMILY!', (240, 140, 40, 255), 1000, 116, 116, WT),
                 kayc=P_('KAY ZUFALL', 'NURSERY SCHOOL TEACHER', TEAL, 1000, 170, 90),
                 sil=P_("JOE McVICKER'S", 'SISTER-IN-LAW', NAVY, 1000, 130, 140),
                 art=M.bigneon('FOR ART', 'PROJECTS!', 860, YEL, PINK),
                 klass=P_('SHE TRIED IT', 'WITH HER CLASS', (90, 170, 255, 255), 960, 140, 130, WT),
                 loved=stamp('THE KIDS LOVED IT!', 1000, (255, 90, 160, 255), 120, -3),
                 stop=P_('STOP SELLING IT', 'FOR WALLS!', RED, 980, 120, 160),
                 sellk=M.bigneon('SELL IT', 'TO KIDS!', 820, YEL, LIME),
                 newname=P_('A NEW NAME:', 'PLAY-DOH!', (255, 170, 40, 255), 960, 130, 190, WT),
                 y1956=M.cal('IN', '1956', (230, 56, 70, 255)),
                 dstore=P_('DEPARTMENT STORE', 'IN WASHINGTON', (200, 50, 60, 255), 1000, 110, 140),
                 macys=stamp("THEN MACY'S!", 860, (200, 30, 50, 255), 140, 3),
                 ontv=P_('CAPTAIN KANGAROO', 'PLAYS ON TV!', (110, 70, 200, 255), 1000, 110, 150, YEL),
                 hof=P_('TOY HALL', 'OF FAME!', (190, 40, 60, 255), 900, 170, 170),
                 dying=P_('A PRODUCT', 'THAT WAS DYING', (100, 96, 110, 255), 960, 150, 120, (255, 170, 170, 255)),
                 nobody=P_('NOBODY NEEDED TO', 'CLEAN THEIR WALLS', (60, 150, 140, 255), 1000, 110, 110, WT))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (200, 170, 220), (186, 156, 206))
    CE.tiles(T('candy.jpg'), (255, 190, 220), (170, 236, 210)); M.sandtex(T('cobblesep.jpg'), (196, 150, 104), (176, 132, 90)); CE.tiles(T('factile.jpg'), (120, 150, 140), (104, 136, 126))
    CE.tiles(T('oldboard.jpg'), (140, 104, 80), (124, 92, 70)); CE.tiles(T('atomtile.jpg'), (255, 236, 200), (120, 210, 200)); CE.tiles(T('aqua.jpg'), (220, 246, 250), (150, 226, 236))
    CE.tiles(T('classfloor.jpg'), (236, 176, 110), (220, 160, 96)); CE.tiles(T('marble.jpg'), (246, 232, 206), (226, 210, 186)); CE.tiles(T('stage.jpg'), (90, 56, 140), (76, 46, 120))
    CE.tiles(T('redcarpet.jpg'), (200, 50, 70), (180, 40, 60))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(playroom=playroom, cincy=cincy, factory=factory, sooty=sooty, atomic=atomic, bath=bath, school=school, store=store, studio=studio, fame=fame)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
