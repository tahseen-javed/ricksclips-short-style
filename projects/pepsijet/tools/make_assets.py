#!/usr/bin/env python3
"""Assets for video 30: Pepsi put a Harrier jet in a 1996 ad as a joke (7,000,000 Pepsi Points) and business student John Leonard tried to buy
it with a $700,008.50 check; a federal judge (1999) called it an adolescent fantasy, Pepsi raised the price to 700,000,000 points and added
"just kidding". 90s Memphis-pop world (new palette): sky-blue schoolyard with a red-brick high school (hook + loop; a covered "?" price tag =
open loop, resolved as JUST KIDDING), cobalt-bubblegum-lime Memphis TV studio, grape-lime 90s dorm, steel-teal hangar, peach-lilac rooftop,
red-white-blue noon post street, mirror-glass HQ plaza, cool marble federal court, pastel rainbow fantasy clouds, dusk-lilac living room with
a cyan TV glow. Cute cast (new): John Leonard (90s headphones, open flannel), the ad's teen pilot (jet helmet, flight suit), Judge Kimba Wood
(bob, judge robe), five tiny investors. usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v29_assets import *

ROOT = B.ROOT
COB, PINK, LIME, RD, SKY, STEEL, CRM, NAVY = (40, 90, 230, 255), (255, 120, 190, 255), (170, 240, 60, 255), (240, 40, 70, 255), (120, 200, 255, 255), (60, 130, 150, 255), (252, 246, 236, 255), (30, 50, 120, 255)
LA.NEW.update({
    'john': dict(sk=0, style='side', hair=(110, 70, 40, 255), suit=(60, 140, 90, 255), shade=(46, 112, 70, 255), body='grunge', xhat='headphones', hatc=(255, 140, 40, 255)),
    'pilot': dict(sk=1, style='spiky', hair=(40, 30, 30, 255), suit=(110, 140, 80, 255), shade=(88, 114, 62, 255), body='flight', acc=RD, xhat='pilot', hatc=RD),
    'judge': dict(sk=0, style='bob', hair=(150, 90, 50, 255), suit=(40, 36, 50, 255), shade=(28, 26, 36, 255), body='judge', band=(200, 170, 90, 255), glasses=1),
})


def gloss(d, x, y, w, h): d.ellipse(x, y, w, h, fill=(255, 255, 255, 120))


def neon3(a, b, c, w=900, h=560, col=(20, 40, 110, 255), edge=PINK):
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 44, fill=col, outline=LINE, width=16); d.rrect(34, 34, w - 34, h - 34, 30, outline=edge, width=8)
    d.text(w / 2, h * 0.2, a, LA.fit(a, 96, w - 160), LIME, stroke=6, stroke_fill=LINE)
    for k, (t, cc) in enumerate(((b, YEL), (c, PINK))): d.text(w / 2, h * (0.47 + 0.27 * k), t, LA.fit(t, 140, w - 110), cc, stroke=7, stroke_fill=LINE)
    return d.out()


def jet(mode='default'):                                     # chibi Harrier jump jet with big eyes on the canopy (hover: thrust puffs below)
    d = Draw(1800, 1100); g = (150, 170, 180, 255)
    d.poly([(200, 560), (1500, 470), (1700, 560), (1500, 650)], fill=g, outline=LINE, width=14); d.poly([(700, 560), (1100, 300), (1250, 320), (1050, 560)], fill=dk(g, 0.85), outline=LINE, width=12)
    d.poly([(700, 600), (1100, 840), (1250, 820), (1050, 600)], fill=dk(g, 0.8), outline=LINE, width=12); d.poly([(220, 560), (120, 360), (260, 360), (420, 540)], fill=dk(g, 0.85), outline=LINE, width=12)
    d.ellipse(1350, 500, 200, 90, fill=(120, 200, 255, 255), outline=LINE, width=12); gloss(d, 1300, 470, 70, 24); eyes(d, 1360, 520, 0.7, 'shocked' if mode == 'hover' else 'happy')
    d.ellipse(900, 600, 130, 60, fill=dk(g, 0.7), outline=LINE, width=10); d.text(900, 470, '*', 120, RD, stroke=5, stroke_fill=LINE); d.rect(1200, 540, 1240, 640, RD)
    if mode == 'hover':
        for x in (760, 1040): [d.dot(x + k * 30 * (1 if k % 2 else -1), 760 + k * 90, 70 + k * 14, (255, 255, 255, 220)) for k in range(4)]
    return d.out()


def can(mode='default'):                                     # glossy blue cola can with a red-white wave, PEPSI label, face
    d = Draw(800, 1200); d.rrect(130, 140, 670, 1120, 70, fill=COB, outline=LINE, width=16); d.ellipse(400, 140, 270, 60, fill=(200, 206, 214, 255), outline=LINE, width=14)
    d.ellipse(400, 1120, 270, 50, fill=dk(COB, 0.8), outline=LINE, width=12); d.poly([(132, 520), (400, 440), (668, 520), (668, 640), (400, 560), (132, 640)], fill=WT); d.poly([(132, 640), (400, 560), (668, 640), (668, 700), (400, 620), (132, 700)], fill=RD)
    d.text(400, 330, 'PEPSI', 120, WT, stroke=8, stroke_fill=LINE); d.rrect(170, 180, 210, 1060, 20, fill=(255, 255, 255, 110)); eyes(d, 400, 860, 1.0, 'shocked' if mode == 'shocked' else 'happy')
    return d.out()


def pricetag(mode='default'):                                      # the giant price tag (q: covered "?" - open loop; 7m; 700m + JUST KIDDING)
    d = Draw(1400, 900); d.poly([(300, 80), (1340, 80), (1340, 820), (300, 820), (60, 450)], fill=(255, 236, 120, 255) if mode != 'default' else (150, 80, 200, 255), outline=LINE, width=16)
    d.dot(220, 450, 50, WT); d.ellipse(220, 450, 50, 50, outline=LINE, width=10); gloss(d, 600, 150, 160, 36)
    if mode == 'default': d.text(820, 450, '?', 520, YEL, stroke=14, stroke_fill=LINE); return d.out()
    big = '7,000,000' if mode == '7m' else '700,000,000'
    d.text(820, 300 if mode == '7m' else 250, big, LA.fit(big, 200, 940), RD, stroke=8, stroke_fill=LINE); d.text(820, 500 if mode == '7m' else 430, 'PEPSI POINTS', 100, NAVY)
    if mode == '700m': d.rrect(430, 540, 1220, 740, 30, fill=PINK, outline=LINE, width=10); d.text(825, 640, 'JUST KIDDING', 96, WT, stroke=6, stroke_fill=LINE)
    else: eyes(d, 820, 680, 0.8, 'happy')
    return d.out()


def stuff():                                                 # Pepsi Stuff catalog rack: T-shirt + leather jacket on hangers with point tags
    d = Draw(1800, 1100); d.stroke([(100, 140), (1700, 140)], (200, 200, 210, 255), 24)
    for x, col, nm in ((520, (255, 255, 255, 255), 'T'), (1260, (90, 60, 50, 255), 'J')):
        d.arc(x, 200, 50, 50, 180, 360, LINE, 10); d.poly([(x - 260, 280), (x - 120, 220), (x + 120, 220), (x + 260, 280), (x + 300, 480), (x + 200, 500), (x + 190, 900), (x - 190, 900), (x - 200, 500), (x - 300, 480)], fill=col, outline=LINE, width=14)
        if nm == 'T': d.dot(x, 520, 110, COB); d.poly([(x - 110, 520), (x + 110, 500), (x + 110, 540), (x - 110, 560)], fill=RD); eyes(d, x, 700, 0.6, 'happy')
        else: d.stroke([(x, 230), (x, 900)], (200, 200, 210, 255), 10); [d.dot(x + sg * 90, 420, 16, (200, 200, 210, 255)) for sg in (-1, 1)]; eyes(d, x, 640, 0.6, 'happy')
        d.rrect(x + 150, 760, x + 380, 880, 20, fill=LIME, outline=LINE, width=8); d.text(x + 265, 820, 'PTS', 56, NAVY)
    return d.out()


def school():                                                # red-brick 90s high school with a clock, HIGH SCHOOL sign, cute door face
    d = Draw(2000, 1100); d.rect(100, 300, 1900, 1080, (200, 80, 70, 255)); d.rrect(100, 300, 1900, 1080, 2, outline=LINE, width=14)
    for k in range(6):
        for j in range(2): x, y = 220 + k * 290, 420 + j * 260; win(d, x, y, x + 160, y + 160, (170, 220, 255, 255))
    d.rrect(700, 150, 1300, 300, 20, fill=CRM, outline=LINE, width=10); d.text(1000, 226, 'HIGH SCHOOL', 80, NAVY); d.dot(1000, 70, 60, WT); d.ellipse(1000, 70, 60, 60, outline=LINE, width=8)
    d.rrect(880, 880, 1120, 1080, 30, fill=(80, 120, 200, 255), outline=LINE, width=10); eyes(d, 1000, 820, 0.5, 'happy'); return d.out()


def calc(mode='default'):                                    # chunky calculator with a face; screen shows 0.10 (sum: 700,000)
    d = Draw(900, 1200); d.rrect(100, 60, 800, 1140, 70, fill=(250, 200, 80, 255), outline=LINE, width=16); d.rrect(170, 140, 730, 380, 20, fill=(180, 230, 190, 255), outline=LINE, width=10)
    d.text(450, 260, '$700,000' if mode == 'sum' else '$0.10', 120 if mode == 'sum' else 150, (30, 80, 50, 255))
    for j in range(3):
        for i in range(4): d.rrect(180 + i * 140, 700 + j * 140, 290 + i * 140, 810 + j * 140, 24, fill=[WT, PINK, (120, 200, 255, 255)][(i + j) % 3], outline=LINE, width=8)
    eyes(d, 450, 520, 0.8, 'shocked' if mode == 'sum' else 'happy'); gloss(d, 300, 120, 100, 30); return d.out()


def dime():                                                  # shiny 10-cent coin with a face
    d = Draw(900, 900); d.dot(450, 450, 400, (210, 214, 222, 255)); d.ellipse(450, 450, 400, 400, outline=LINE, width=16); d.ellipse(450, 450, 330, 330, outline=(170, 174, 186, 255), width=12)
    d.text(450, 300, '10', 200, (110, 116, 130, 255), stroke=6, stroke_fill=LINE); eyes(d, 450, 560, 1.0, 'happy'); gloss(d, 300, 200, 110, 46); return d.out()


def check():                                                 # the giant check: $700,008.50 to PEPSI, with 15 can labels clipped on
    d = Draw(1800, 900); d.rrect(60, 100, 1740, 840, 30, fill=(200, 240, 210, 255), outline=LINE, width=16); [d.stroke([(100, y), (1700, y)], (170, 220, 185, 255), 6) for y in range(160, 820, 60)]
    d.text(500, 220, 'PAY TO: PEPSI', 80, NAVY); d.rrect(980, 290, 1680, 460, 20, fill=WT, outline=LINE, width=10); d.text(1330, 375, '$700,008.50', 110, (30, 110, 60, 255)); d.stroke([(1050, 700), (1650, 700)], LINE, 6)
    d.text(1350, 650, 'J. Leonard', 80, (40, 60, 160, 255))
    for k in range(5): d.rrect(120 + k * 50, 420 + k * 40, 520 + k * 50, 620 + k * 40, 20, fill=[COB, RD, WT, COB, RD][k], outline=LINE, width=8)
    d.text(330, 800, '15 LABELS', 70, NAVY); return d.out()


def investors():                                             # five tiny investors in suits with briefcases, cheering
    d = Draw(2000, 800); cols = [(90, 110, 200, 255), (200, 90, 120, 255), (90, 170, 130, 255), (220, 160, 60, 255), (150, 100, 200, 255)]
    for k in range(5):
        x = 220 + k * 390; y = 330
        d.rrect(x - 90, y + 80, x + 90, y + 380, 60, fill=cols[k], outline=LINE, width=10); d.poly([(x - 30, y + 90), (x + 30, y + 90), (x, y + 200)], fill=WT); d.dot(x, y, 100, (255, 222, 196, 255) if k % 2 == 0 else (196, 136, 96, 255))
        d.ellipse(x, y, 100, 100, outline=LINE, width=10); d.chord(x, y - 20, 104, 80, 180, 360, fill=[(60, 40, 30, 255), (230, 200, 120, 255), (30, 30, 40, 255)][k % 3]); eyes(d, x, y + 20, 0.42, 'happy')
        d.rrect(x + 80, y + 300, x + 200, y + 390, 14, fill=(120, 80, 50, 255), outline=LINE, width=8); d.text(x, y - 160, '$', 90, (60, 170, 90, 255), stroke=5, stroke_fill=LINE)
    return d.out()


def mailbox(mode='default'):                                 # blue US mailbox with a face (sent: envelope flying in; back: envelope bouncing out, sad)
    d = Draw(1200, 1300); d.rrect(260, 300, 940, 1100, 40, fill=(40, 80, 180, 255), outline=LINE, width=16); d.chord(600, 320, 340, 220, 180, 360, fill=(40, 80, 180, 255), outline=LINE, width=16)
    d.rect(330, 420, 870, 470, (20, 40, 100, 255)); d.rect(300, 1100, 380, 1280, LINE); d.rect(820, 1100, 900, 1280, LINE); d.text(600, 620, 'US MAIL', 80, WT); eyes(d, 600, 820, 0.9, 'sad' if mode == 'back' else 'happy')
    if mode != 'default':
        y = 200 if mode == 'sent' else 80; d.rrect(620 if mode == 'back' else 380, y, 1080 if mode == 'back' else 840, y + 260, 20, fill=CRM, outline=LINE, width=10); d.poly([(400 if mode != 'back' else 640, y + 10), (600 if mode != 'back' else 850, y + 140), (820 if mode != 'back' else 1060, y + 10)], outline=LINE, width=8)
        if mode == 'back': d.text(860, y + 330, 'RETURN', 60, RD, stroke=4, stroke_fill=LINE)
    return d.out()


def suit():                                                  # the lawsuit: scroll with a seal and a little gavel
    d = Draw(1100, 1300); d.rrect(200, 120, 900, 1180, 30, fill=CRM, outline=LINE, width=14); d.ellipse(550, 120, 360, 60, fill=(240, 230, 210, 255), outline=LINE, width=12); d.ellipse(550, 1180, 360, 60, fill=(240, 230, 210, 255), outline=LINE, width=12)
    d.text(550, 300, 'LAWSUIT', 120, RD, stroke=5, stroke_fill=LINE); [d.stroke([(290, y), (810, y)], (200, 190, 170, 255), 10) for y in range(420, 900, 70)]
    d.dot(780, 1000, 90, RD); d.text(780, 1000, '*', 110, YEL); eyes(d, 470, 990, 0.6, 'happy'); return d.out()


def bench(bang=False):                                       # marble federal bench with a gold eagle seal and a gavel (bang: down + lines)
    d = Draw(1600, 1100); d.rrect(120, 420, 1480, 1080, 30, fill=(225, 228, 236, 255), outline=LINE, width=14); d.rrect(80, 360, 1520, 450, 20, fill=(180, 186, 200, 255), outline=LINE, width=12)
    for x in (300, 1300): d.rect(x - 50, 470, x + 50, 1060, (205, 210, 222, 255)); d.stroke([(x - 20, 480), (x - 20, 1050)], (180, 186, 200, 255), 8)
    d.dot(800, 640, 140, (240, 200, 90, 255)); d.ellipse(800, 640, 140, 140, outline=LINE, width=12); d.text(800, 646, '*', 160, NAVY); eyes(d, 800, 900, 0.7, 'shocked' if bang else 'happy')
    if bang: d.rrect(1060, 300, 1300, 360, 20, fill=(120, 70, 40, 255), outline=LINE, width=10); d.stroke([(1180, 300), (1320, 120)], (120, 70, 40, 255), 26); [d.stroke([(1180 + 160 * math.cos(a), 330 + 90 * math.sin(a)), (1180 + 240 * math.cos(a), 330 + 130 * math.sin(a))], YEL, 14) for a in (3.6, 4.2, 5.2, 5.8)]
    else: d.rrect(1080, 220, 1320, 280, 20, fill=(120, 70, 40, 255), outline=LINE, width=10); d.stroke([(1200, 280), (1200, 360)], (120, 70, 40, 255), 26)
    return d.out()


def stampd():                                                # appeal: big red DENIED stamp on a folder
    d = Draw(1300, 1000); d.rrect(100, 200, 1200, 960, 30, fill=(250, 210, 120, 255), outline=LINE, width=14); d.rrect(100, 120, 520, 240, 20, fill=(250, 210, 120, 255), outline=LINE, width=12)
    d.rrect(240, 400, 1060, 700, 30, outline=RD, width=24); d.text(650, 550, 'DENIED', 200, RD); eyes(d, 650, 820, 0.6, 'sad'); return d.out()


def tvset(mode='ad'):                                        # chunky 90s TV with a face (ad: jet + school on screen; series: clapper + 2022)
    d = Draw(1500, 1300); d.rrect(100, 100, 1400, 1100, 90, fill=(120, 100, 200, 255), outline=LINE, width=16); d.rrect(200, 180, 1150, 900, 60, fill=(170, 236, 255, 255), outline=LINE, width=12)
    for y in (300, 500, 700): d.dot(1270, y, 50, PINK); d.ellipse(1270, y, 50, 50, outline=LINE, width=8)
    if mode == 'ad': d.rect(260, 650, 1090, 850, (200, 80, 70, 255)); d.poly([(420, 480), (900, 440), (980, 480), (900, 520)], fill=(150, 170, 180, 255), outline=LINE, width=8); d.ellipse(880, 470, 50, 24, fill=(120, 200, 255, 255), outline=LINE, width=6)
    else: d.rrect(400, 380, 950, 700, 20, fill=LINE); [d.poly([(400 + k * 110, 380), (460 + k * 110, 380), (420 + k * 110, 300), (360 + k * 110, 300)], fill=WT if k % 2 else LINE) for k in range(5)]; d.text(675, 560, '2022', 150, YEL)
    d.rect(300, 1100, 380, 1240, LINE); d.rect(1120, 1100, 1200, 1240, LINE); eyes(d, 675, 990, 0.6, 'happy'); gloss(d, 380, 260, 120, 40); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def squig(d, x, y, col, n=4, s=40):
    d.stroke([(x + k * s, y + (s * 0.6 if k % 2 else 0)) for k in range(n)], col, 14)


def schoolyard(path):                                        # bright sky-blue schoolyard: clouds, sun rays, bleachers, trees
    im = sky((90, 180, 255), (220, 240, 255), 1.0); d = Draw(W2, H2)
    for x, y in ((300, 180), (1700, 140), (1100, 260)): [d.dot(x + k * 90, y + (k % 2) * 30, 80, (255, 255, 255, 240)) for k in range(4)]
    for x in (200, 2200): ptree(d, x, 900, 1.3, (90, 180, 90, 255))
    for k in range(4): d.rect(500 + k * 40, 700 + k * 50, 1900 - k * 40, 730 + k * 50, (230, 230, 240, 255))
    fl(d, (90, 170, 90, 255)); im.alpha_composite(d.out()); glow(im, 2100, 120, 400, (255, 250, 200, 110), 80); im.convert('RGB').save(path)


def memphis(path):                                           # cobalt-bubblegum-lime 90s Memphis TV studio: squiggles, dots, triangles, light bars
    im = sky((40, 90, 230), (255, 130, 200), 1.1); d = Draw(W2, H2); r = np.random.RandomState(5)
    for _ in range(40):
        x, y, k = r.randint(0, W2), r.randint(0, 850), r.randint(0, 3); col = [LIME, YEL, WT, (60, 230, 230, 255)][r.randint(0, 4)]
        if k == 0: squig(d, x, y, col)
        elif k == 1: d.poly([(x, y), (x + 70, y + 20), (x + 20, y + 80)], fill=col, outline=LINE, width=6)
        else: d.dot(x, y, 22, col)
    for x in range(150, W2, 450): d.rect(x, 0, x + 40, 60, (255, 250, 220, 255))
    fl(d, (230, 90, 160, 255)); im.alpha_composite(d.out()); [glow(im, x + 20, 40, 160, (255, 250, 220, 100), 50) for x in range(150, W2, 450)]; im.convert('RGB').save(path)


def dorm(path):                                              # grape-lime 90s dorm: posters, lava lamp, string lights, desk
    im = sky((120, 70, 170), (190, 140, 220), 1.0); d = Draw(W2, H2)
    for x, col in ((300, LIME), (700, (60, 230, 230, 255)), (1700, YEL), (2100, PINK)): d.rrect(x - 140, 150, x + 140, 520, 10, fill=col, outline=LINE, width=8); d.dot(x, 300, 70, WT)
    d.stroke([(0, 90), (600, 140), (1200, 90), (1800, 140), (W2, 90)], LINE, 5); [d.dot(x, 100 + 30 * math.sin(x / 190), 14, [YEL, PINK, LIME][(x // 120) % 3]) for x in range(40, W2, 120)]
    d.rrect(1050, 520, 1150, 840, 50, fill=(255, 120, 60, 255), outline=LINE, width=8); [d.dot(1100, y, 26, (255, 220, 80, 255)) for y in (600, 700, 780)]
    fl(d, (90, 60, 120, 255)); im.alpha_composite(d.out()); glow(im, 1100, 680, 200, (255, 180, 100, 120), 50); im.convert('RGB').save(path)


def hangar(path):                                            # steel-teal military hangar: arched roof ribs, spotlights, hazard stripes
    im = sky((40, 100, 120), (130, 200, 200), 1.0); d = Draw(W2, H2)
    for k in range(7): d.arc(1200, 1100, 1300 - k * 30, 1000 - k * 90, 180, 360, (30, 70, 90, 255), 14)
    for x in range(0, W2, 120): d.poly([(x, 880), (x + 60, 880), (x + 20, 940), (x - 40, 940)], fill=YEL)
    fl(d, (110, 130, 140, 255)); im.alpha_composite(d.out()); [glow(im, x, 160, 240, (230, 255, 255, 110), 60) for x in (500, 1200, 1900)]; im.convert('RGB').save(path)


def rooftop(path):                                           # peach-lilac sunset rooftop: skyline, water tower, balloons
    im = sky((200, 150, 230), (255, 190, 150), 1.0); d = Draw(W2, H2)
    for k, x in enumerate(range(0, W2, 170)): h_ = 200 + (k * 97) % 300; d.rect(x, 900 - h_, x + 150, 940, (150, 110, 170, 255)); [win(d, x + 30, 900 - h_ + 40 + j * 90, x + 70, 900 - h_ + 90 + j * 90, (255, 220, 160, 255)) for j in range(h_ // 120)]
    d.rect(1800, 420, 2000, 600, (170, 110, 80, 255)); d.poly([(1780, 420), (1900, 340), (2020, 420)], fill=(140, 90, 70, 255))
    fl(d, (170, 130, 150, 255)); im.alpha_composite(d.out()); glow(im, 1200, 900, 700, (255, 200, 150, 90), 140); im.convert('RGB').save(path)


def poststreet(path):                                        # red-white-blue noon post street: bunting, flag, brick post office
    im = sky((150, 210, 255), (240, 248, 255), 1.0); d = Draw(W2, H2); d.rect(700, 300, 1700, 940, (200, 90, 80, 255)); d.poly([(650, 300), (1200, 160), (1750, 300)], fill=(240, 240, 245, 255), outline=LINE, width=8)
    for x in range(780, 1700, 160): d.rect(x, 380, x + 60, 900, (240, 240, 245, 255))
    d.stroke([(0, 120), (600, 200), (1200, 120), (1800, 200), (W2, 120)], LINE, 5)
    for x in range(30, W2, 90): y = 130 + 60 * math.sin(x / 300); d.poly([(x, y), (x + 60, y), (x + 30, y + 70)], fill=[RD, WT, COB][(x // 90) % 3])
    fl(d, (190, 190, 200, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def glassplaza(path):                                        # mirror-glass HQ plaza: blue glass tower grid, fountain, flags
    im = sky((60, 150, 240), (200, 235, 255), 1.0); d = Draw(W2, H2); d.rect(600, 60, 1800, 940, (80, 150, 220, 255))
    for x in range(620, 1800, 100):
        for y in range(80, 920, 100): d.rect(x, y, x + 86, y + 86, (140, 200, 250, 255) if (x + y) % 300 else (210, 240, 255, 255))
    for x in (300, 2100): d.rect(x, 300, x + 12, 940, LINE); d.rect(x + 12, 300, x + 160, 400, [RD, COB][x > 1000])
    fl(d, (200, 205, 215, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def fedcourt(path):                                          # cool marble federal court: steel-blue walls, white columns, gold eagle crest
    im = sky((90, 120, 170), (180, 200, 230), 1.0); d = Draw(W2, H2)
    for x in range(150, W2, 330): d.rect(x - 60, 120, x + 60, 940, (240, 242, 248, 255)); [d.stroke([(x + k, 130), (x + k, 930)], (210, 214, 226, 255), 6) for k in (-30, 0, 30)]
    d.dot(1200, 200, 110, (240, 200, 90, 255)); d.ellipse(1200, 200, 110, 110, outline=LINE, width=10); d.poly([(1040, 190), (1200, 150), (1360, 190), (1200, 240)], fill=(200, 150, 60, 255))
    fl(d, (150, 160, 180, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def fantasy(path):                                           # pastel rainbow fantasy sky: rainbow arcs, candy clouds, sparkles
    im = sky((255, 190, 230), (190, 230, 255), 1.0); d = Draw(W2, H2)
    for k, col in enumerate([(255, 120, 120, 255), (255, 190, 100, 255), (255, 240, 120, 255), (140, 230, 140, 255), (120, 190, 255, 255), (190, 140, 255, 255)]): d.arc(1200, 1000, 1000 - k * 60, 760 - k * 60, 180, 360, col, 60)
    for x, y in ((300, 700), (1000, 820), (1800, 720), (2200, 860)): [d.dot(x + k * 110, y + (k % 2) * 30, 110, (255, 255, 255, 250)) for k in range(4)]
    r = np.random.RandomState(4); [d.text(r.randint(0, W2), r.randint(50, 600), '*', 60, (255, 250, 200, 255)) for _ in range(20)]
    fl(d, (240, 220, 250, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def livingroom(path):                                        # dusk-lilac living room: window city lights, plant, lamp, cyan TV glow
    im = sky((110, 90, 160), (190, 150, 200), 1.0); d = Draw(W2, H2); d.rrect(200, 140, 800, 560, 20, fill=(40, 50, 110, 255), outline=(240, 220, 200, 255), width=20); stars(d, 0, 0)
    [d.dot(260 + k * 50, 480 - (k % 3) * 40, 10, YEL) for k in range(11)]; ptree(d, 2100, 900, 0.8, (90, 170, 110, 255))
    d.rect(1700, 300, 1716, 900, LINE); d.chord(1708, 300, 100, 80, 180, 360, fill=(255, 220, 140, 255), outline=LINE, width=8)
    fl(d, (120, 100, 140, 255)); im.alpha_composite(d.out()); glow(im, 1200, 600, 600, (120, 255, 255, 80), 120); glow(im, 1708, 280, 200, (255, 220, 150, 110), 50); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast4(('john', 'pilot', 'judge'))
    multi = dict(jet={'default': jet(), 'hover': jet('hover')}, can={'default': can(), 'shocked': can('shocked')}, pricetag={k: pricetag(k) for k in ('default', '7m', '700m')},
                 stuff={'default': stuff()}, school={'default': school()}, calc={'default': calc(), 'sum': calc('sum')}, dime={'default': dime()}, check={'default': check()},
                 investors={'default': investors()}, mailbox={k: mailbox(k) for k in ('default', 'sent', 'back')}, suit={'default': suit()}, bench={'default': bench(), 'bang': bench(True)},
                 stampd={'default': stampd()}, tvset={'default': tvset(), 'series': tvset('series')})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ = (110, 50, 160, 255), (30, 130, 140, 255)
    cards = dict(hookc=neon3('PEPSI PUT A', 'FIGHTER JET', 'IN AN AD!'),
                 tryc=stamp('HE TRIED TO BUY IT!', 960, RD, 110, -3),
                 y1996=M.cal('PEPSI', '1996', COB),
                 shotc=stamp('THE FINAL SHOT...', 900, PU, 120, 3),
                 harrier=P_('HARRIER', 'JUMP JET', NAVY, 860, 130, 170, YEL),
                 nobody=stamp('NOBODY CAN DRINK THAT!', 1000, RD, 100, -3),
                 johnc=P_('JOHN LEONARD', 'BUSINESS STUDENT', (40, 120, 80, 255), 960, 120, 100, YEL),
                 loop=stamp('THE LOOPHOLE!', 760, PU, 140, 4),
                 tenc=M.bigneon('10 CENTS', 'EACH!', 760, YEL, LIME),
                 worth=M.bigneon('WORTH OVER', '$30 MILLION', 860, YEL, PINK),
                 five=P_('FIVE', 'INVESTORS', PU, 760, 130, 170, YEL),
                 suedc=stamp('HE SUED!', 680, RD, 160, -4),
                 y1999=M.cal('COURT', '1999', NAVY),
                 kimba=P_('JUDGE', 'KIMBA WOOD', (40, 40, 60, 255), 820, 130, 160, YEL),
                 fant=stamp('ADOLESCENT FANTASY', 1000, PINK, 110, 3),
                 lost=M.bigneon('LEONARD', 'LOST', 760, YEL, RD),
                 appealc=stamp('APPEAL FAILED TOO', 960, NAVY, 110, -3),
                 newad=stamp('PEPSI CHANGED THE AD', 1000, COB, 100, 3),
                 nojet=stamp('NO JET...', 640, PU, 150, -4),
                 netc=P_('A NETFLIX SERIES', '2022', RD, 880, 110, 190, YEL),
                 jokec=M.bigneon('IT WAS', 'A JOKE!', 760, YEL, PINK))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('lawn.jpg'), (110, 190, 100), (98, 176, 90)); CE.tiles(T('studio.jpg'), (240, 110, 180), (226, 98, 166)); CE.tiles(T('dormfl.jpg'), (150, 110, 80), (136, 98, 70)); CE.tiles(T('hangfl.jpg'), (140, 150, 160), (128, 138, 148))
    CE.tiles(T('roof.jpg'), (180, 150, 160), (166, 138, 148)); CE.tiles(T('sidewalk.jpg'), (210, 210, 215), (196, 196, 202)); CE.tiles(T('plaza.jpg'), (220, 222, 230), (206, 208, 218)); CE.tiles(T('marblefl.jpg'), (200, 206, 220), (186, 192, 208))
    M.sandtex(T('cloudfl.jpg'), (245, 230, 250), (236, 220, 244)); CE.tiles(T('rug.jpg'), (150, 120, 170), (138, 108, 158)); CE.tiles(T('pave.jpg'), (120, 100, 90), (106, 88, 78))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(schoolyard=schoolyard, memphis=memphis, dorm=dorm, hangar=hangar, rooftop=rooftop, poststreet=poststreet, glassplaza=glassplaza, fedcourt=fedcourt, fantasy=fantasy, livingroom=livingroom)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
