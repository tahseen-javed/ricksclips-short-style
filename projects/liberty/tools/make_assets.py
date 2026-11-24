#!/usr/bin/env python3
"""Assets for video 21: the Statue of Liberty was never supposed to be green (copper -> patina = armor).
Copper-penny to verdigris world: harbor-sunrise peach + mint, copper orange, plum velvet, storm slate, olive-gold 1910, navy Congress,
sepia news street, deep-blue lab, violet micro world, night skyline with mint fireworks.
Cute cast: Bartholdi (beard + smock), a nervous official, a senator, a newsboy, a goggles chemist; Lady Liberty as a hero prop in 7 colours.
usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import lordgta_assets as LA
import mco_assets as M
import mono_assets as MA
from hx_assets import *

ROOT = B.ROOT
SCH = dict(copper=((222, 126, 74, 255), (176, 90, 52, 255)), brown=((150, 98, 64, 255), (118, 74, 48, 255)), green=((120, 206, 176, 255), (78, 160, 134, 255)),
           streaky=((150, 98, 64, 255), (118, 74, 48, 255)), half=((214, 120, 70, 255), (170, 86, 50, 255)), armor=((120, 206, 176, 255), (78, 160, 134, 255)))


def statue(sch='copper', face='happy'):                      # cute Lady Liberty: robe, crown of 7 rays, torch held high, tablet, plinth
    W = 900; d = Draw(W, 1700); c, k = SCH.get(sch, SCH['copper']); G2 = (110, 200, 168, 255)
    d.rrect(230, 1560, 670, 1690, 16, fill=(210, 200, 180, 255), outline=LINE, width=14)
    d.poly([(330, 690), (570, 690), (680, 1570), (220, 1570)], fill=c, outline=LINE, width=16)
    for x0, x1 in ((380, 330), (450, 450), (520, 580)): d.stroke([(x0, 720), (x1, 1550)], k, 12)
    d.stroke([(370, 720), (250, 280)], LINE, 96); d.stroke([(370, 720), (250, 280)], c, 70)
    d.rrect(205, 180, 295, 300, 18, fill=c, outline=LINE, width=12); d.poly([(250, 30), (310, 150), (250, 190), (190, 150)], fill=(255, 200, 60, 255), outline=LINE, width=10); d.dot(250, 130, 24, (255, 246, 180, 255))
    d.rrect(520, 760, 650, 950, 14, fill=k, outline=LINE, width=12); d.stroke([(560, 730), (600, 860)], LINE, 70); d.stroke([(560, 730), (600, 860)], c, 50)
    for a in range(-150, -29, 20): r0, r1 = 110, 230; d.poly([(450 + r0 * math.cos(math.radians(a - 7)), 520 + r0 * math.sin(math.radians(a - 7))), (450 + r1 * math.cos(math.radians(a)), 520 + r1 * math.sin(math.radians(a))), (450 + r0 * math.cos(math.radians(a + 7)), 520 + r0 * math.sin(math.radians(a + 7)))], fill=c, outline=LINE, width=10)
    d.dot(450, 540, 130, c); d.ellipse(450, 540, 130, 130, outline=LINE, width=14); d.chord(450, 470, 130, 60, 180, 360, fill=k, outline=LINE, width=10)
    if sch == 'streaky':
        for x in (300, 360, 420, 520, 600): d.stroke([(x, 700), (x + 6, 900 + (x % 7) * 60)], G2, 22)
        for x, y in ((440, 620), (500, 600)): d.stroke([(x, y), (x, y + 60)], G2, 10)
    if sch == 'half':
        r = np.random.RandomState(3)
        for _ in range(90): x, y = 450 + r.randint(0, 260), r.randint(180, 1560); d.dot(x, y, r.randint(20, 60), G2)
        for _ in range(30): x, y = 260 + r.randint(0, 190), r.randint(300, 1560); d.dot(x, y, r.randint(12, 34), G2)
    if sch in ('copper', 'armor'): shine(d, 370, 760, 380, 30); d.dot(400, 480, 30, (255, 255, 255, 150))
    if sch == 'armor':
        for x, y, s in ((680, 600, 60), (200, 900, 44), (620, 1300, 50)): d.poly([(x, y - s), (x + s * 0.25, y - s * 0.25), (x + s, y), (x + s * 0.25, y + s * 0.25), (x, y + s), (x - s * 0.25, y + s * 0.25), (x - s, y), (x - s * 0.25, y - s * 0.25)], fill=(255, 255, 230, 255))
    eyes(d, 450, 560, 0.7, face)
    if sch == 'veiled':
        e = Draw(W, 1700); e.poly([(250, 30), (330, 260), (380, 380), (620, 420), (720, 1570), (180, 1570), (200, 400)], fill=(244, 236, 214, 255), outline=LINE, width=14)
        for x in (320, 460, 600): e.stroke([(x - 40, 450), (x, 1550)], (210, 200, 180, 255), 10)
        e.poly([(450, 700), (330, 640), (330, 760)], fill=RED, outline=LINE, width=8); e.poly([(450, 700), (570, 640), (570, 760)], fill=RED, outline=LINE, width=8); e.dot(450, 700, 26, RED)
        im = d.out(); im.alpha_composite(e.out()); return im
    return d.out()


def penny(face='happy'):                                     # giant brand-new penny: rim, ONE CENT, glints, cute face
    d = Draw(1000, 1000); d.dot(500, 500, 460, (226, 130, 76, 255)); d.ellipse(500, 500, 460, 460, outline=LINE, width=18); d.ellipse(500, 500, 400, 400, outline=(190, 100, 56, 255), width=14)
    d.text(500, 290, 'ONE CENT', 80, (170, 84, 46, 255)); eyes(d, 500, 560, 1.0, face); shine(d, 230, 260, 360, 40)
    for x, y, s in ((800, 220, 70), (200, 780, 50)): d.poly([(x, y - s), (x + s * 0.25, y - s * 0.25), (x + s, y), (x + s * 0.25, y + s * 0.25), (x, y + s), (x - s * 0.25, y + s * 0.25), (x - s, y), (x - s * 0.25, y - s * 0.25)], fill=(255, 255, 230, 255))
    return d.out()


def pennies2():                                              # a copper sheet as thick as two stacked pennies, with a measuring bracket
    d = Draw(1400, 800); d.rrect(60, 420, 820, 520, 10, fill=(222, 126, 74, 255), outline=LINE, width=12); shine(d, 80, 430, 70, 20)
    for y in (420, 470): d.ellipse(1100, y + 25, 200, 26, fill=(226, 130, 76, 255), outline=LINE, width=10)
    d.stroke([(900, 410), (900, 530)], RED, 12); d.stroke([(880, 410), (920, 410)], RED, 12); d.stroke([(880, 530), (920, 530)], RED, 12); d.text(1100, 260, '=', 200, RED, stroke=8, stroke_fill=LINE); return d.out()


def sheets():                                                # stack of hammered copper sheets + a big mallet
    d = Draw(1300, 1000)
    for k in range(7): y = 820 - k * 70; d.rrect(120 + k * 10, y, 1000 + k * 10, y + 60, 10, fill=(222 - k * 6, 126 - k * 4, 74, 255), outline=LINE, width=10); [d.dot(200 + j * 120 + k * 10, y + 30, 10, (180, 90, 50, 255)) for j in range(7)]
    d.stroke([(1180, 900), (980, 330)], (150, 100, 60, 255), 40); d.rrect(880, 220, 1100, 380, 30, fill=(110, 110, 120, 255), outline=LINE, width=14); eyes(d, 560, 470, 0.6, 'happy'); return d.out()


def cloud(face='default'):                                   # angry rain cloud dropping rain and salt cubes
    d = Draw(1300, 1100)
    for x, y, r in ((300, 380, 220), (560, 300, 270), (860, 380, 230), (600, 470, 260)): d.dot(x, y, r, (130, 140, 170, 255))
    d.ellipse(600, 470, 520, 220, outline=LINE, width=0); eyes(d, 600, 430, 1.0, 'shocked')
    for sg in (-1, 1): d.stroke([(600 + sg * 60, 330), (600 + sg * 190, 290)], LINE, 20)
    r = np.random.RandomState(5)
    for _ in range(26): x = r.randint(220, 1000); y = r.randint(700, 1060); d.stroke([(x, y), (x - 20, y + 60)], (120, 200, 255, 255), 12)
    for _ in range(10): x = r.randint(220, 1000); y = r.randint(700, 1040); d.rrect(x, y, x + 34, y + 34, 6, fill=WT, outline=LINE, width=5)
    return d.out()


def sketch():                                                # Bartholdi's easel: a statue drawn in deep red, with an arrow and "?"
    d = Draw(800, 1300); d.stroke([(400, 80), (160, 1280)], (150, 100, 60, 255), 26); d.stroke([(400, 80), (640, 1280)], (150, 100, 60, 255), 26)
    d.rrect(110, 180, 690, 860, 16, fill=(250, 244, 230, 255), outline=LINE, width=14)
    st = statue('brown').resize((300, 566)); im = d.out(); px = np.array(st); px[..., 0] = np.minimum(255, px[..., 0] * 1.25); px[..., 1] = px[..., 1] * 0.45; px[..., 2] = px[..., 2] * 0.45
    im.alpha_composite(Image.fromarray(px.astype(np.uint8)), (250, 240)); e = Draw(800, 1300); e.text(620, 300, '?', 160, RED, stroke=8, stroke_fill=LINE); im.alpha_composite(e.out()); return im


def bucket(face='q'):                                        # copper paint bucket with brush and drips (open loop "?"); sad when the plan dies
    d = Draw(900, 1000); d.poly([(150, 300), (750, 300), (680, 940), (220, 940)], fill=(200, 200, 210, 255), outline=LINE, width=16); d.ellipse(450, 300, 300, 60, fill=(222, 126, 74, 255), outline=LINE, width=14)
    for x in (260, 420, 600): d.rrect(x, 300, x + 50, 420 + (x % 5) * 30, 24, fill=(222, 126, 74, 255))
    d.arc(450, 300, 330, 260, 180, 360, LINE, 16); d.stroke([(620, 280), (800, 40)], (150, 100, 60, 255), 34); d.rrect(570, 230, 680, 330, 14, fill=(222, 126, 74, 255), outline=LINE, width=10)
    if face == 'q': d.text(450, 690, '?', 260, (40, 160, 130, 255), stroke=10, stroke_fill=LINE)
    else: eyes(d, 450, 640, 0.8, 'sad' if face == 'sad' else 'happy')
    return d.out()


def crowd():                                                 # angry public with placards
    d = Draw(1800, 1000); sk = [(246, 214, 190, 255), (218, 172, 134, 255), (176, 122, 90, 255)]; cols = [RED, (60, 120, 220, 255), YEL, (60, 170, 90, 255), PINK, ORNG, VIO]
    for k in range(7):
        x = 150 + k * 250; y = 560 + (k % 2) * 50
        if k % 2 == 0: d.stroke([(x + 60, y + 100), (x + 60, y - 300)], (150, 100, 60, 255), 16); d.rrect(x - 60, y - 440, x + 180, y - 280, 14, fill=WT, outline=LINE, width=8); d.text(x + 60, y - 360, '!!', 100, RED)
        d.rrect(x - 90, y + 80, x + 90, y + 420, 40, fill=cols[k], outline=LINE, width=10); d.dot(x, y, 100, sk[k % 3]); d.ellipse(x, y, 100, 100, outline=LINE, width=10)
        for sg in (-1, 1): d.stroke([(x + sg * 20, y - 40), (x + sg * 60, y - 56)], LINE, 10); d.dot(x + sg * 36, y - 6, 12, LINE)
        d.ellipse(x, y + 50, 30, 22, fill=(150, 40, 50, 255), outline=LINE, width=6)
    return d.out()


def flask():                                                 # round flask of bubbling verdigris liquid, cute face
    d = Draw(700, 1000); d.rrect(280, 60, 420, 400, 20, fill=(220, 240, 250, 200), outline=LINE, width=12); d.dot(350, 640, 300, (220, 240, 250, 200)); d.ellipse(350, 640, 300, 300, outline=LINE, width=14)
    d.chord(350, 640, 290, 290, 0, 180, fill=(110, 210, 180, 255)); d.rect(64, 630, 636, 650, (110, 210, 180, 255))
    for x, y, r in ((300, 560, 26), (420, 500, 18), (360, 420, 14), (340, 300, 20)): d.ellipse(x, y, r, r, outline=(110, 210, 180, 255), width=6)
    eyes(d, 350, 760, 0.7, 'happy'); shine(d, 140, 520, 200, 30); return d.out()


def atoms(face='default'):                                   # micro world: copper atoms under a growing mint crystal skin, air bubbles
    d = Draw(1800, 1100)
    for row in range(3):
        for k in range(9): x = 120 + k * 200 + (row % 2) * 100; y = 1000 - row * 170; d.dot(x, y, 90, (226, 130, 76, 255)); d.ellipse(x, y, 90, 90, outline=LINE, width=10); d.dot(x - 30, y - 30, 22, (255, 220, 190, 255))
    for k in range(10): x = 90 + k * 180; d.poly([(x, 560), (x + 90, 510), (x + 180, 560), (x + 180, 640), (x + 90, 690), (x, 640)], fill=(110, 216, 180, 230), outline=LINE, width=8)
    for x, y in ((300, 200), (800, 120), (1400, 230), (1100, 340)): d.dot(x, y, 70, (150, 210, 255, 200)); d.ellipse(x, y, 70, 70, outline=LINE, width=8); d.text(x, y, 'O', 70, (40, 80, 160, 255))
    for x in (520, 1320): eyes(d, x, 830, 0.5, 'happy')
    return d.out()


def shield():                                                # verdigris shield with a copper rim, proud face, sparkles
    d = Draw(900, 1100); pts = [(450, 60), (820, 180), (790, 620), (450, 1040), (110, 620), (80, 180)]; d.poly(pts, fill=(222, 126, 74, 255), outline=LINE, width=16)
    d.poly([(450, 140), (730, 230), (710, 600), (450, 940), (190, 600), (170, 230)], fill=(110, 206, 176, 255)); eyes(d, 450, 520, 0.9, 'happy'); shine(d, 230, 260, 300, 34); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def skyline(d, y0, col, seed=3, n=16):
    r = np.random.RandomState(seed)
    for k in range(n): x = k * W2 / n; h = 80 + r.randint(0, 220); d.rect(x + 10, y0 - h, x + W2 / n - 10, y0, col)


def water(d, y0, col, col2):
    d.rect(0, y0, W2, 940, col)
    for y in range(y0 + 30, 940, 50): [d.stroke([(x, y), (x + 70, y)], col2, 6) for x in range((y * 7) % 140, W2, 260)]


def harbor(path):                                            # hook harbor: peach-mint sunrise, little Manhattan skyline, mint water, gulls
    im = sky((250, 170, 150), (200, 240, 220), 1.0); d = Draw(W2, H2); d.dot(1900, 420, 150, (255, 236, 200, 255))
    skyline(d, 760, (150, 120, 160, 255)); water(d, 760, (90, 190, 180, 255), (200, 255, 240, 255))
    for x, y in ((500, 260), (700, 200), (1500, 300)): d.stroke([(x - 40, y), (x, y + 18), (x + 40, y)], LINE, 8)
    fl(d, (150, 140, 150, 255)); im.alpha_composite(d.out()); glow(im, 1900, 420, 400, (255, 240, 210, 120), 90); im.convert('RGB').save(path)


def unveil(path):                                            # 1886 unveiling: festive blue-gold sky, flags, steamboats with smoke, bunting
    im = sky((90, 150, 230), (255, 226, 160), 1.0); d = Draw(W2, H2); water(d, 720, (60, 120, 190, 255), (180, 220, 255, 255))
    for x in (300, 1000, 1800): d.rect(x, 640, x + 260, 720, WT); d.rect(x + 40, 560, x + 90, 640, RED); d.dot(x + 65, 500, 50, (230, 230, 240, 200)); d.dot(x + 90, 420, 70, (230, 230, 240, 180))
    for k in range(18): x = k * W2 / 18; d.poly([(x, 80), (x + W2 / 18, 80), (x + W2 / 36, 150)], fill=(RED, WT, (40, 80, 200, 255))[k % 3], outline=LINE, width=4)
    fl(d, (180, 160, 140, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 800, (255, 236, 180, 90), 120); im.convert('RGB').save(path)


def velvet(path):                                            # penny stage: plum velvet drapes, spotlight cone, gold stars
    im = sky((90, 30, 80), (150, 60, 120), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 160): d.rect(x, 0, x + 80, 940, (120, 40, 100, 255))
    d.poly([(1000, 0), (1400, 0), (1700, 940), (700, 940)], fill=(255, 240, 200, 50)); stars(d, 40, 900, 4)
    fl(d, (110, 40, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 600, 500, (255, 220, 180, 80), 100); im.convert('RGB').save(path)


def workshop(path):                                          # Paris copper workshop: brick arches, glowing forge, copper sheets on the walls
    im = sky((170, 80, 50), (230, 140, 80), 1.0); d = Draw(W2, H2)
    for x in range(100, W2, 600): d.chord(x + 200, 500, 220, 300, 180, 360, fill=(90, 50, 40, 255)); d.rect(x - 20, 500, x + 420, 940, (90, 50, 40, 255))
    for x in range(0, W2, 300): d.rrect(x + 40, 180, x + 220, 420, 10, fill=(222, 126, 74, 255), outline=LINE, width=8)
    d.rrect(1050, 620, 1350, 900, 30, fill=(60, 50, 50, 255), outline=LINE, width=10); d.chord(1200, 760, 110, 80, 180, 360, fill=(255, 180, 60, 255))
    fl(d, (120, 80, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 740, 400, (255, 170, 80, 140), 90); im.convert('RGB').save(path)


def storm(path):                                             # salt storm: slate-blue sky, rain streaks, white-capped waves
    im = sky((70, 90, 130), (150, 170, 200), 1.0); d = Draw(W2, H2); water(d, 740, (60, 90, 120, 255), (230, 240, 255, 255))
    r = np.random.RandomState(9)
    for _ in range(160): x, y = r.randint(0, W2), r.randint(0, 760); d.stroke([(x, y), (x - 30, y + 90)], (210, 230, 255, 140), 5)
    for x, y, rr in ((400, 160, 200), (1100, 120, 240), (1900, 170, 210)): d.dot(x, y, rr, (100, 110, 140, 230))
    fl(d, (110, 120, 140, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def olive(path):                                             # 1910 harbor: olive-gold sunset, mint-streaked clouds, ferry, piers
    im = sky((180, 170, 80), (255, 210, 140), 1.0); d = Draw(W2, H2); d.dot(600, 560, 180, (255, 220, 140, 255)); water(d, 740, (120, 150, 110, 255), (230, 240, 200, 255))
    for x, y in ((400, 200), (1500, 160), (1900, 300)): d.ellipse(x, y, 260, 40, fill=(160, 220, 190, 150))
    for x in range(1400, 2300, 120): d.rect(x, 700, x + 30, 800, (110, 80, 50, 255))
    fl(d, (160, 140, 90, 255)); im.alpha_composite(d.out()); glow(im, 600, 560, 400, (255, 230, 160, 110), 90); im.convert('RGB').save(path)


def cityhall(path):                                          # officials' office: mint marble walls, white columns, tall window, brass clock
    im = sky((120, 190, 170), (190, 230, 214), 1.0); d = Draw(W2, H2)
    for x in range(150, W2, 500): d.rect(x, 0, x + 90, 940, (236, 236, 226, 255)); d.rect(x - 20, 0, x + 110, 50, (220, 220, 210, 255))
    d.rect(1000, 150, 1400, 650, (190, 230, 255, 255)); d.chord(1200, 150, 200, 120, 180, 360, fill=(190, 230, 255, 255)); d.stroke([(1200, 30), (1200, 650)], WT, 12)
    d.dot(1900, 260, 90, (240, 200, 90, 255)); d.dot(1900, 260, 70, WT); d.stroke([(1900, 260), (1900, 210)], LINE, 8); d.stroke([(1900, 260), (1940, 270)], LINE, 8)
    d.rect(0, 720, W2, 940, (80, 140, 120, 255)); fl(d, (110, 120, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def studio(path):                                            # Bartholdi's studio: terracotta walls, skylight, plaster model shapes, plans pinned up
    im = sky((210, 120, 90), (240, 180, 140), 1.0); d = Draw(W2, H2)
    d.poly([(800, 0), (1600, 0), (1500, 220), (900, 220)], fill=(200, 236, 255, 255))
    for x in (300, 600, 1800, 2100): d.rrect(x - 110, 260, x + 110, 520, 6, fill=(236, 226, 250, 255), outline=(60, 80, 160, 255), width=8); d.stroke([(x - 60, 480), (x, 320), (x + 60, 480)], (60, 80, 160, 255), 6)
    for x, h in ((1100, 300), (1350, 220)): d.rrect(x - 70, 900 - h, x + 70, 900, 30, fill=(236, 230, 220, 255), outline=LINE, width=8)
    fl(d, (170, 110, 80, 255)); im.alpha_composite(d.out()); glow(im, 1200, 120, 500, (255, 250, 240, 90), 80); im.convert('RGB').save(path)


def congress(path):                                          # Congress 1906: navy walls, cream columns, gold dome window, flags, red carpet
    im = sky((40, 60, 120), (90, 110, 170), 1.0); d = Draw(W2, H2)
    d.chord(1200, 420, 360, 300, 180, 360, fill=(240, 200, 110, 255), outline=(200, 160, 80, 255), width=20)
    for x in range(100, W2, 300): d.rect(x, 200, x + 70, 940, (230, 220, 200, 255))
    for x in (500, 1900): d.stroke([(x, 900), (x, 300)], LINE, 8); [d.rect(x, 300 + i * 30, x + 160, 330 + i * 30, (RED, WT)[i % 2]) for i in range(7)]; d.rect(x, 300, x + 70, 400, (40, 60, 150, 255))
    d.poly([(1000, 940), (1400, 940), (1300, 700), (1100, 700)], fill=(180, 40, 60, 255)); fl(d, (90, 70, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 500, (255, 220, 150, 90), 90); im.convert('RGB').save(path)


def newsstreet(path):                                        # news street: sepia brick, red awnings, gas lamps, paper boys' stand
    im = sky((200, 160, 120), (240, 210, 170), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 600): d.rect(x, 80, x + 560, 900, (170, 90, 70, 255)); [d.rect(x + 40 + c * 170, y, x + 160 + c * 170, y + 120, (255, 226, 160, 255)) for c in range(3) for y in (160, 380)]; d.poly([(x, 600), (x + 560, 600), (x + 520, 680), (x + 40, 680)], fill=(RED, WT)[x // 600 % 2], outline=LINE, width=6)
    for x in (580, 1180, 1780): d.stroke([(x, 900), (x, 450)], LINE, 12); d.dot(x, 440, 36, (255, 236, 160, 255))
    fl(d, (150, 120, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def lab(path):                                               # chemistry lab: deep blue walls, shelves of glowing verdigris flasks, a big window
    im = sky((40, 60, 130), (80, 110, 180), 1.0); d = Draw(W2, H2); r = np.random.RandomState(4)
    for y in (300, 560):
        d.rect(0, y, W2, y + 20, (120, 90, 70, 255))
        for x in range(60, W2, 140): rr = 30 + r.randint(0, 20); d.dot(x + 40, y - rr, rr, [(110, 220, 190, 230), (230, 140, 90, 230), (160, 200, 255, 230)][r.randint(0, 3)]); d.ellipse(x + 40, y - rr, rr, rr, outline=LINE, width=5)
    d.rect(1000, 620, 1400, 900, (60, 80, 150, 255)); fl(d, (70, 80, 120, 255)); im.alpha_composite(d.out()); glow(im, 1200, 420, 900, (120, 255, 220, 50), 140); im.convert('RGB').save(path)


def micro(path):                                             # micro world: violet-teal glow, floating molecules and bubbles, crystal sparkles
    im = sky((60, 40, 120), (40, 140, 150), 1.0); d = Draw(W2, H2); r = np.random.RandomState(6)
    for _ in range(40): x, y, rr = r.randint(0, W2), r.randint(0, 900), r.randint(10, 40); d.ellipse(x, y, rr, rr, outline=(180, 240, 255, 150), width=5)
    for _ in range(18): x, y = r.randint(0, W2), r.randint(0, 900); d.dot(x, y, 22, (226, 130, 76, 200)); d.dot(x + 40, y + 10, 16, (150, 210, 255, 200)); d.stroke([(x, y), (x + 40, y + 10)], WT, 4)
    fl(d, (60, 110, 120, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 900, (150, 255, 230, 60), 160); im.convert('RGB').save(path)


def nightsky(path):                                          # a century on: navy night, lit skyline, mint + gold fireworks, harbor lights
    im = sky((30, 40, 100), (80, 90, 170), 1.0); d = Draw(W2, H2); stars(d, 120, 600, 8)
    for x, y, c in ((400, 250, (120, 240, 200, 255)), (1100, 160, (255, 210, 90, 255)), (1900, 260, (255, 140, 190, 255))):
        for a in range(0, 360, 20): d.stroke([(x + 40 * math.cos(math.radians(a)), y + 40 * math.sin(math.radians(a))), (x + 150 * math.cos(math.radians(a)), y + 150 * math.sin(math.radians(a)))], c, 8)
    skyline(d, 760, (60, 60, 120, 255), 5); r = np.random.RandomState(2)
    for _ in range(140): d.dot(r.randint(0, W2), r.randint(560, 750), 5, (255, 220, 130, 255))
    water(d, 760, (40, 70, 130, 255), (255, 220, 140, 200)); fl(d, (60, 70, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast(('bartholdi', 'official', 'senator', 'newsboy', 'chemist'))
    multi = dict(liberty={'default': statue('green', 'shocked'), 'happy': statue('green', 'happy'), 'veiled': statue('veiled'), 'copper': statue('copper', 'happy'), 'brown': statue('brown', 'sad'),
                          'streaky': statue('streaky', 'shocked'), 'half': statue('half', 'shocked'), 'armor': statue('armor', 'happy'), 'copperx': statue('copper', 'shocked')},
                 penny={'default': penny()}, pennies2={'default': pennies2()}, sheets={'default': sheets()}, cloud={'default': cloud()}, sketch={'default': sketch()},
                 bucket={'default': bucket('q'), 'happy': bucket('happy'), 'sad': bucket('sad')}, moneybag={'default': MA.moneybag()}, paper={'default': LA.paper('SACRILEGE!', 'PAINT PLAN', 900)},
                 crowd={'default': crowd()}, flask={'default': flask()}, atoms={'default': atoms()}, shield={'default': shield()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    MINT, COPC = (40, 170, 140, 255), (200, 100, 56, 255)
    cards = dict(hookc=M.bigneon('NEVER MEANT', 'TO BE GREEN!', 960, (110, 255, 200, 255), YEL),
                 damage=stamp('THAT COLOR = DAMAGE!', 980, RED, 110, -4),
                 harborc=P_('NEW YORK', 'HARBOR', (40, 90, 170, 255), 900, 160, 160, WT),
                 y1886=M.cal('OCT 28', '1886', COPC),
                 unveil=stamp('UNVEILED!', 760, (40, 80, 200, 255), 150, 3),
                 pennyc=M.bigneon('BRAND-NEW', 'PENNY!', 900, ORNG, YEL),
                 copperc=P_('REDDISH-BROWN', 'COPPER', COPC, 1000, 120, 190, YEL),
                 s300=P_('300 HAMMERED', 'SHEETS', (150, 80, 50, 255), 960, 130, 190, YEL),
                 thick=stamp('AS THICK AS 2 PENNIES', 1000, COPC, 100, -3),
                 salt=P_('SALT AIR', '+ RAIN', (70, 90, 130, 255), 860, 160, 170, CYAN),
                 dull=stamp('A DULL BROWN...', 860, (120, 80, 50, 255), 130, 3),
                 streaks=stamp('GREEN STREAKS!', 900, MINT, 140, -3),
                 y1910=M.cal('BY', '1910', MINT),
                 halfc=M.bigneon('HALF COPPER', 'HALF GREEN', 1000, ORNG, (110, 255, 200, 255)),
                 patchy=stamp('PATCHY! BLOTCHY!', 960, (120, 140, 60, 255), 120, 3),
                 eating=P_('IS IT EATING', 'HER ALIVE?!', (110, 120, 110, 255), 960, 130, 170, (110, 255, 200, 255)),
                 bart=P_('FRÉDÉRIC', 'BARTHOLDI', (60, 96, 170, 255), 940, 150, 160, YEL),
                 wrong=stamp('GUESSED WRONG!', 920, RED, 140, -4),
                 redc=P_('HE EXPECTED', 'DARK RED', (150, 40, 50, 255), 900, 140, 180, WT),
                 y1906=M.cal('CONGRESS', '1906', (40, 60, 150, 255)),
                 paintc=M.bigneon('PAINT HER BACK', 'TO COPPER!', 1000, ORNG, YEL),
                 explode=stamp('THE PUBLIC EXPLODES!', 1000, RED, 110, -4),
                 dies=stamp('THE PLAN DIES', 860, (90, 70, 90, 255), 140, 3),
                 notrot=P_('THAT GREEN', "ISN'T ROT", MINT, 920, 150, 170, WT),
                 patina=M.bigneon("IT'S A", 'PATINA!', 860, (110, 255, 200, 255), YEL),
                 react=P_('COPPER', '+ AIR', COPC, 820, 170, 180, CYAN),
                 skin=M.bigneon('ITS OWN', 'THIN SKIN', 900, (110, 255, 200, 255), ORNG),
                 sealc=P_('THE SKIN SEALS', 'THE METAL', MINT, 980, 130, 160, YEL),
                 shieldc=stamp('SHIELDING IT!', 860, (40, 140, 120, 255), 140, -3),
                 armor=M.bigneon('THE DAMAGE', 'IS THE ARMOR!', 1000, (110, 255, 200, 255), YEL),
                 later=stamp('TEN YEARS LATER', 900, (40, 60, 130, 255), 130, 3),
                 crownc=P_('GREEN FROM', 'CROWN TO TOE', MINT, 960, 150, 140, YEL),
                 century=stamp('OVER A CENTURY!', 900, (40, 140, 120, 255), 130, -3),
                 paintjob=stamp('THE PAINT JOB...', 860, COPC, 140, 3),
                 alive=P_('THE ONE THING', 'KEEPING HER ALIVE', (40, 140, 120, 255), 1000, 140, 110, YEL),
                 erased=stamp('NEARLY ERASED!', 900, RED, 140, -4))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (180, 170, 170), (166, 156, 156))
    CE.tiles(T('pier.jpg'), (170, 150, 150), (154, 136, 136)); CE.tiles(T('dock.jpg'), (200, 170, 130), (184, 156, 118)); M.sandtex(T('velfloor.jpg'), (120, 50, 100), (100, 40, 84))
    CE.tiles(T('forge.jpg'), (150, 96, 70), (134, 84, 60)); CE.tiles(T('wetstone.jpg'), (110, 124, 150), (96, 110, 136)); CE.tiles(T('olivestone.jpg'), (180, 170, 120), (164, 154, 106))
    CE.tiles(T('marble.jpg'), (170, 210, 196), (156, 196, 182)); M.sandtex(T('terracotta.jpg'), (200, 130, 100), (180, 112, 86)); CE.tiles(T('navytile.jpg'), (90, 100, 150), (78, 88, 136))
    CE.tiles(T('cobsepia.jpg'), (170, 140, 110), (154, 126, 98)); CE.tiles(T('labtile.jpg'), (90, 110, 160), (78, 96, 146)); M.sandtex(T('microfloor.jpg'), (70, 130, 140), (90, 160, 170), seed=5)
    CE.tiles(T('nightpier.jpg'), (80, 90, 140), (70, 78, 126))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(harbor=harbor, unveil=unveil, velvet=velvet, workshop=workshop, storm=storm, olive=olive, cityhall=cityhall, studio=studio, congress=congress, newsstreet=newsstreet, lab=lab, micro=micro, nightsky=nightsky)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
