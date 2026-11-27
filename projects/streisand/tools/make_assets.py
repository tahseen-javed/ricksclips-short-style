#!/usr/bin/env python3
"""Assets for video 36: the Streisand Effect (2003: Kenneth Adelman's 12,000+ aerial cliff-erosion photos, image 3850 shows a Malibu
clifftop mansion; a $50 million privacy lawsuit; the photo had 6 downloads, 2 by her own lawyers; the lawsuit became news, 400,000+
visitors in a month; the case was thrown out and she paid the photographer's legal fees; two years later blogger Mike Masnick named it).
Malibu-sunset + internet-neon world (new palette): coral-teal sunset cliff coast (hook + loop), sky-blue aerial coast, teal photo lab,
burgundy-gold law office, violet pixel computer room, halftone-yellow newsroom, cyan-magenta neon web world, oak courtroom, amber-lilac
night loft. Accent hazard yellow #ffd000 (the warning label). The star is the clifftop mansion with a face; the celebrity herself is never
drawn. Cute cast (new): photographer Kenneth (leather aviator cap with goggles, flight jacket with a camera), two lawyers (three-piece suits:
slick hair + glasses / bald + mustache), the judge (white quiff, robe, glasses), blogger Mike (striped beanie, zip hoodie, glasses).
usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v33_assets import *

ROOT = B.ROOT
HAZ, CORAL, TEALC, BURG, GLD, VIOL, CYN, MAG, OAK, CRM, SEA = (255, 208, 0, 255), (255, 130, 110, 255), (40, 170, 170, 255), (130, 30, 60, 255), (240, 190, 70, 255), (110, 60, 180, 255), (60, 230, 255, 255), (255, 60, 200, 255), (170, 110, 60, 255), (252, 246, 232, 255), (60, 140, 200, 255)
LA.NEW.update({
    'kenneth': dict(sk=0, style='side', hair=(150, 100, 60, 255), suit=(150, 100, 60, 255), shade=(120, 80, 50, 255), body='flightjk', acc=HAZ, xhat='aviator', hatc=(120, 70, 40, 255), freckles=1),
    'lawa': dict(sk=0, style='slick', hair=(40, 30, 40, 255), suit=(60, 60, 80, 255), shade=(46, 46, 64, 255), body='vest3', acc=HAZ, glasses=1),
    'lawb': dict(sk=1, style='bald', hair=(90, 70, 60, 255), suit=(110, 40, 60, 255), shade=(90, 30, 50, 255), body='vest3', acc=CYN, stache=(90, 70, 60, 255)),
    'judge2': dict(sk=2, style='quiff', hair=(240, 240, 245, 255), suit=(40, 34, 50, 255), shade=(30, 26, 40, 255), body='judge', acc=HAZ, glasses=1),
    'mike': dict(sk=1, style='side', hair=(60, 40, 30, 255), suit=(60, 130, 120, 255), shade=(46, 106, 98, 255), body='zip', acc=HAZ, xhat='beanie5', hatc=(255, 120, 60, 255), glasses=1),
})


def mansion(face='nervous'):                                 # the clifftop mansion on a rocky cliff, a face on the facade (hide: curtain over it; famous: flashes)
    d = Draw(1600, 1300); d.poly([(80, 1300), (200, 820), (420, 760), (1180, 760), (1420, 840), (1540, 1300)], fill=(190, 140, 110, 255), outline=LINE, width=14)
    [d.stroke([(x, 860), (x + 40, 1260)], (160, 110, 90, 255), 10) for x in (300, 600, 1000, 1300)]; d.chord(800, 770, 640, 60, 180, 360, fill=(120, 190, 100, 255))
    d.rect(360, 420, 1240, 760, (255, 248, 236, 255)); d.rrect(360, 420, 1240, 760, 2, outline=LINE, width=12); d.poly([(320, 430), (800, 230), (1280, 430)], fill=CORAL, outline=LINE, width=12)
    for x in (430, 1050): d.rrect(x, 480, x + 130, 600, 14, fill=(170, 220, 250, 255), outline=LINE, width=8)
    d.rrect(1260, 600, 1440, 760, 10, fill=(120, 200, 230, 255), outline=LINE, width=8); eyes5(d, 800, 600, 0.95, {'nervous': 'shocked', 'famous': 'happy', 'hide': 'sad'}.get(face, face))
    if face == 'hide': d.poly([(300, 200), (1300, 200), (1340, 780), (260, 780)], fill=(150, 40, 70, 235), outline=LINE, width=12); [d.stroke([(x, 210), (x - 20, 770)], (120, 30, 56, 255), 10) for x in range(380, 1300, 120)]; d.text(800, 480, '?', 260, HAZ, stroke=8, stroke_fill=LINE)
    if face in ('famous', 'shocked'):
        for x, y in ((180, 300), (1420, 280), (260, 620), (1380, 560)): d.text(x, y, '*', 160, HAZ, stroke=6, stroke_fill=LINE)
    return d.out()


def plane():                                                 # cute little prop plane with a big camera lens under the wing
    d = Draw(1500, 900); d.rrect(200, 380, 1300, 600, 110, fill=(250, 250, 255, 255), outline=LINE, width=14); d.poly([(560, 380), (900, 380), (760, 80), (640, 80)], fill=CORAL, outline=LINE, width=12)
    d.poly([(560, 600), (900, 600), (760, 860), (640, 860)], fill=CORAL, outline=LINE, width=12); d.poly([(200, 420), (60, 260), (130, 250), (300, 400)], fill=TEALC, outline=LINE, width=10)
    d.rrect(1260, 400, 1330, 580, 20, fill=(90, 90, 110, 255)); d.ellipse(1340, 490, 30, 150, fill=(200, 210, 230, 160)); d.rrect(1000, 410, 1180, 500, 30, fill=(170, 220, 250, 255), outline=LINE, width=8)
    d.dot(700, 680, 80, (60, 60, 70, 255)); d.dot(700, 680, 40, (120, 200, 250, 255)); eyes(d, 1080, 540, 0.35, 'happy'); return d.out()


def photos():                                                # 12,000 aerial photos: a fanned stack of coast prints with a big "12,000+" tag
    d = Draw(1500, 1100)
    for k in range(7):
        x, y, a = 300 + k * 140, 640 - abs(k - 3) * 30, (k - 3) * 6; p = Draw(500, 380); p.rrect(10, 10, 490, 370, 14, fill=WT, outline=LINE, width=10); p.rect(40, 40, 460, 300, (120, 190, 230, 255)); p.poly([(40, 300), (200, 170), (330, 230), (460, 140), (460, 300)], fill=(190, 140, 110, 255))
        im = p.out().rotate(-a, expand=True, resample=Image.BICUBIC); d.im.alpha_composite(im.resize((im.width * 3, im.height * 3)), (int((x - im.width / 2) * 3), int((y - im.height / 2) * 3)))
    d.rrect(450, 60, 1050, 260, 30, fill=HAZ, outline=LINE, width=12); d.text(750, 160, '12,000+', 130, LINE); eyes(d, 750, 940, 0.5, 'happy'); return d.out()


def photo3850(face='default'):                               # image 3850: framed aerial shot of the cliff with the tiny mansion, a red circle
    d = Draw(1300, 1100); d.rrect(60, 60, 1240, 960, 20, fill=WT, outline=LINE, width=16); d.rect(110, 110, 1190, 820, (110, 180, 230, 255))
    d.poly([(110, 820), (110, 560), (400, 470), (700, 520), (1000, 420), (1190, 470), (1190, 820)], fill=(190, 140, 110, 255)); d.rect(640, 440, 760, 520, CRM); d.poly([(620, 445), (700, 400), (780, 445)], fill=CORAL)
    d.ellipse(700, 470, 150, 100, outline=(230, 40, 60, 255), width=16); d.rrect(420, 860, 880, 1060, 24, fill=HAZ, outline=LINE, width=10); d.text(650, 960, 'IMAGE 3850', 70, LINE)
    eyes(d, 300, 700, 0.45, 'shocked' if face == 'shocked' else 'happy'); return d.out()


def scroll():                                                # the lawsuit scroll: $50,000,000, invasion of privacy
    d = Draw(1100, 1400); d.rrect(140, 120, 960, 1280, 30, fill=(250, 244, 226, 255), outline=LINE, width=14); [d.rrect(100, y, 1000, y + 90, 45, fill=(230, 214, 180, 255), outline=LINE, width=12) for y in (60, 1250)]
    d.text(550, 260, 'LAWSUIT', 120, BURG); d.rrect(200, 360, 900, 560, 20, fill=(230, 250, 230, 255), outline=(60, 140, 80, 255), width=10); d.text(550, 460, '$50,000,000', 110, (40, 120, 60, 255), stroke=4, stroke_fill=LINE)
    d.text(550, 680, 'INVASION', 90, LINE); d.text(550, 790, 'OF PRIVACY', 90, LINE); [d.stroke([(220, y), (880, y)], (210, 200, 180, 255), 12) for y in range(900, 1160, 60)]; eyes(d, 550, 1060, 0.5, 'shocked'); return d.out()


def screen(mode='six'):                                      # retro computer: DOWNLOADS 6 (two of them lawyers) / VISITORS 400,000+ (a flood of tiny people)
    d = Draw(1400, 1200); d.rrect(120, 80, 1280, 900, 50, fill=(220, 214, 200, 255), outline=LINE, width=16); d.rrect(190, 150, 1210, 760, 24, fill=(30, 30, 70, 255))
    d.text(700, 240, 'DOWNLOADS' if mode == 'six' else 'VISITORS', 80, CYN)
    if mode == 'six':
        d.text(700, 420, '6', 240, HAZ, stroke=8, stroke_fill=LINE)
        for k in range(6): x = 330 + k * 150; d.dot(x, 610, 40, (255, 220, 190, 255)); d.rrect(x - 40, 650, x + 40, 720, 20, fill=(BURG if k in (2, 3) else (120, 200, 250, 255))); d.dot(x - 14, 604, 6, LINE); d.dot(x + 14, 604, 6, LINE)
    else:
        d.text(700, 420, '400,000+', 190, HAZ, stroke=8, stroke_fill=LINE)
        r = np.random.RandomState(3); [d.dot(r.randint(230, 1170), r.randint(560, 740), 18, ((255, 220, 190, 255), CYN, MAG, HAZ)[k % 4]) for k in range(70)]
    d.rrect(520, 900, 880, 1000, 20, fill=(200, 194, 180, 255), outline=LINE, width=10); d.rrect(300, 1000, 1100, 1120, 30, fill=(230, 224, 210, 255), outline=LINE, width=12); eyes(d, 700, 830, 0.4, 'shocked'); return d.out()


def paper():                                                 # the news: halftone front page about the superstar suing over a secret photo
    d = Draw(1200, 1400); d.rrect(80, 60, 1120, 1340, 20, fill=(250, 246, 230, 255), outline=LINE, width=14); d.text(600, 170, 'THE NEWS', 120, LINE); d.stroke([(120, 250), (1080, 250)], LINE, 8)
    d.text(600, 360, 'SUPERSTAR SUES', 96, (200, 30, 60, 255)); d.text(600, 480, 'OVER SECRET PHOTO!', 80, LINE); d.rrect(200, 560, 1000, 960, 20, fill=(110, 180, 230, 255), outline=LINE, width=10)
    d.poly([(200, 960), (200, 800), (500, 720), (800, 760), (1000, 680), (1000, 960)], fill=(190, 140, 110, 255)); d.rect(560, 700, 660, 760, CRM)
    for x in range(140, 1080, 40):
        for y in range(1010, 1300, 40): d.dot(x, y, 8, (200, 190, 170, 255))
    eyes(d, 960, 170, 0.35, 'happy'); return d.out()


def crowd(mode='default'):                                   # a wave of tiny chibi readers with phones, rushing in
    d = Draw(1800, 900); r = np.random.RandomState(5)
    for k in range(22):
        x, y = 120 + (k % 11) * 155 + (k // 11) * 70, 420 + (k // 11) * 250 + (k % 3) * 20; col = (CORAL, TEALC, VIOL, HAZ, MAG, SEA)[k % 6]
        d.rrect(x - 48, y + 30, x + 48, y + 180, 34, fill=col, outline=LINE, width=8); d.dot(x, y, 62, (255, 222, 196, 255)); d.ellipse(x, y, 62, 62, outline=LINE, width=8)
        d.dot(x - 20, y + 4, 9, LINE); d.dot(x + 20, y + 4, 9, LINE); d.ellipse(x, y + 32, 12, 9, fill=(120, 30, 40, 255)); d.rrect(x + 40, y + 50, x + 80, y + 110, 10, fill=(40, 40, 60, 255), outline=LINE, width=5)
        d.chord(x, y - 20, 62, 46, 180, 360, fill=((60, 40, 30, 255), (200, 120, 60, 255), (30, 30, 40, 255))[k % 3])
    return d.out()


def casefile():                                              # the case file flying out, stamped THROWN OUT
    d = Draw(1300, 1100); d.rrect(140, 200, 1160, 980, 30, fill=(240, 200, 120, 255), outline=LINE, width=14); d.rrect(140, 120, 560, 240, 20, fill=(240, 200, 120, 255), outline=LINE, width=12)
    d.text(650, 420, 'THE CASE', 120, BURG); s_ = stamp('THROWN OUT!', 860, (220, 40, 60, 255), 120, -8); d.im.alpha_composite(s_.resize((s_.width * 3, s_.height * 3)), (int(220 * 3), int(540 * 3)))
    [d.stroke([(40, y), (120, y - 30)], LINE, 10) for y in (400, 600, 800)]; eyes(d, 980, 300, 0.32, 'shocked'); return d.out()


def fees():                                                  # the legal fees bill: STREISAND PAYS the photographer's legal fees
    d = Draw(1100, 1300); d.rrect(120, 80, 980, 1220, 24, fill=WT, outline=LINE, width=14); d.text(550, 200, 'LEGAL FEES', 110, LINE); d.stroke([(180, 280), (920, 280)], LINE, 8)
    d.text(550, 400, "PHOTOGRAPHER'S", 80, SEA); d.text(550, 500, 'LAWYERS', 80, SEA); d.rrect(200, 600, 900, 800, 20, fill=(255, 236, 236, 255), outline=(220, 40, 60, 255), width=10); d.text(550, 700, 'PAID BY STREISAND', 66, (220, 40, 60, 255))
    for k in range(5): d.dot(260 + k * 150, 1000 + (k % 2) * 40, 50, GLD); d.ellipse(260 + k * 150, 1000 + (k % 2) * 40, 50, 50, outline=LINE, width=6)
    eyes(d, 550, 900, 0.45, 'sad'); return d.out()


def lost():                                                  # she lost all three: LAWSUIT x, PRIVACY x, MONEY x
    d = Draw(1200, 1200); d.rrect(100, 80, 1100, 1120, 40, fill=CRM, outline=LINE, width=14); d.text(600, 200, 'LOST:', 120, BURG)
    for k, w in enumerate(('THE LAWSUIT', 'THE PRIVACY', 'THE MONEY')):
        y = 400 + k * 230; d.rrect(170, y - 80, 1030, y + 80, 30, fill=WT, outline=LINE, width=10); d.text(530, y, w, 84, LINE)
        d.stroke([(880, y - 50), (980, y + 50)], (230, 40, 60, 255), 26); d.stroke([(980, y - 50), (880, y + 50)], (230, 40, 60, 255), 26)
    return d.out()


def laptop(mode='default'):                                  # the blogger's laptop: the name pops up on screen
    d = Draw(1500, 1100); d.rrect(260, 120, 1240, 760, 40, fill=(60, 60, 80, 255), outline=LINE, width=16); d.rrect(310, 170, 1190, 710, 20, fill=(250, 250, 255, 255) if mode == 'name' else (40, 50, 90, 255))
    if mode == 'name': d.text(750, 340, 'THE STREISAND', 100, LINE); d.text(750, 480, 'EFFECT', 140, (230, 40, 60, 255), stroke=6, stroke_fill=LINE); d.stroke([(400, 600), (1100, 600)], HAZ, 16)
    else: [d.stroke([(380, y), (380 + (y * 37) % 600, y)], (120, 200, 250, 255), 14) for y in range(240, 680, 60)]
    d.poly([(160, 760), (1340, 760), (1440, 900), (60, 900)], fill=(170, 170, 190, 255), outline=LINE, width=14); eyes(d, 750, 830, 0.4, 'happy' if mode == 'name' else 'shocked'); return d.out()


def warn():                                                  # the warning label: hazard sign with stripes
    d = Draw(1300, 1100); d.poly([(650, 60), (1240, 1000), (60, 1000)], fill=LINE); d.poly([(650, 150), (1150, 950), (150, 950)], fill=HAZ)
    d.text(650, 520, '!', 380, LINE); d.rrect(120, 900, 1180, 1080, 30, fill=LINE); [d.poly([(x, 920), (x + 60, 920), (x + 10, 1060), (x - 50, 1060)], fill=HAZ) for x in range(170, 1180, 120)]
    eyes(d, 650, 780, 0.45, 'shocked'); return d.out()


def shovel():                                                # trying to bury the photo: a framed photo half in a sand mound, a cute shovel
    d = Draw(1400, 1100); d.chord(700, 1080, 640, 380, 180, 360, fill=(230, 200, 140, 255), outline=LINE, width=14)
    d.rrect(420, 380, 900, 800, 20, fill=WT, outline=LINE, width=12); d.rect(460, 420, 860, 720, (110, 180, 230, 255)); d.poly([(460, 720), (560, 600), (700, 640), (860, 560), (860, 720)], fill=(190, 140, 110, 255))
    d.chord(700, 1080, 560, 300, 180, 360, fill=(230, 200, 140, 255)); d.stroke([(1080, 200), (1000, 760)], (150, 100, 60, 255), 30); d.poly([(940, 740), (1060, 760), (1040, 960), (920, 940)], fill=(190, 196, 210, 255), outline=LINE, width=10)
    eyes(d, 660, 560, 0.4, 'shocked'); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def malibu(path):                                            # coral-teal Malibu sunset: ocean, cliffs, palms, a low sun
    im = M.sky((40, 150, 170), (255, 150, 120), 1.0); d = Draw(W2, H2); d.dot(1700, 620, 150, (255, 220, 160, 255)); d.rect(0, 640, W2, 940, (50, 140, 180, 255))
    [d.stroke([(x, 680 + k * 40), (x + 200, 680 + k * 40)], (200, 240, 250, 180), 6) for k in range(6) for x in range(80 + k * 60, W2, 520)]
    d.poly([(0, 940), (0, 520), (300, 480), (600, 600), (700, 940)], fill=(170, 110, 90, 255)); d.poly([(1900, 940), (2050, 560), (2400, 500), (2400, 940)], fill=(170, 110, 90, 255))
    for x in (200, 2200): d.stroke([(x, 940), (x + 20, 380)], (90, 60, 50, 255), 16); [d.ellipse(x + 20 + 80 * math.cos(a), 380 + 40 * math.sin(a), 70, 18, fill=(50, 110, 80, 255)) for a in np.linspace(0, 6.28, 7)]
    fl(d, (190, 150, 120, 255)); im.alpha_composite(d.out()); CE.glow(im, 1700, 620, 300, (255, 220, 160, 100), 60); im.convert('RGB').save(path)


def aerial(path):                                            # sky-blue aerial coast: clouds below, coastline far down, gulls
    im = M.sky((100, 180, 250), (220, 240, 255), 1.0); d = Draw(W2, H2); d.rect(0, 700, W2, 940, (60, 150, 200, 255)); d.poly([(0, 940), (0, 720), (500, 760), (1000, 700), (1600, 760), (2400, 720), (2400, 940)], fill=(200, 170, 130, 255))
    for x, y in ((300, 300), (1100, 220), (1900, 340), (700, 560), (1700, 600)): [d.dot(x + k * 110, y + (k % 2) * 30, 90, (255, 255, 255, 235)) for k in range(4)]
    for x, y in ((600, 160), (1400, 120)): d.arc(x, y, 30, 16, 200, 340, LINE, 6); d.arc(x + 56, y, 30, 16, 200, 340, LINE, 6)
    fl(d, (150, 170, 190, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def lab(path):                                               # teal photo lab: strings of hanging prints, red safelight glow
    im = M.sky((20, 110, 120), (60, 170, 170), 1.0); d = Draw(W2, H2)
    for y in (180, 420): d.stroke([(0, y), (W2, y + 20)], LINE, 4); [d.rect(x, y + 10, x + 150, y + 130, WT) for x in range(60, W2, 230)]; [d.rect(x + 12, y + 22, x + 138, y + 118, (120, 190, 230, 255)) for x in range(60, W2, 230)]
    fl(d, (40, 90, 100, 255)); im.alpha_composite(d.out()); CE.glow(im, 2100, 150, 220, (255, 80, 80, 90), 60); im.convert('RGB').save(path)


def office(path):                                            # burgundy-gold law office: wood panels, law books, gold sconces
    im = M.sky((120, 30, 60), (200, 90, 100), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 300): d.rrect(x + 20, 140, x + 280, 880, 10, outline=GLD, width=8)
    for x0 in (300, 1600):
        for y in (300, 520): d.rect(x0, y, x0 + 500, y + 14, (90, 50, 40, 255)); [d.rect(x0 + j * 36, y - 120, x0 + j * 36 + 30, y, ((60, 30, 40, 255), (40, 60, 90, 255), (120, 90, 40, 255))[j % 3]) for j in range(13)]
    fl(d, (110, 60, 60, 255)); im.alpha_composite(d.out()); [CE.glow(im, x, 200, 120, (255, 220, 140, 90), 40) for x in (150, 1200, 2250)]; im.convert('RGB').save(path)


def pixel(path):                                             # violet pixel computer room: big pixels, cables, monitor glow
    im = M.sky((70, 40, 140), (150, 90, 210), 1.0); d = Draw(W2, H2); r = np.random.RandomState(8)
    for _ in range(80): x, y = r.randint(0, 60) * 40, r.randint(0, 22) * 40; d.rect(x, y, x + 36, y + 36, (CYN, MAG, HAZ, (140, 110, 230, 255))[r.randint(0, 4)])
    [d.stroke([(x, 940), (x + 100, 700), (x + 300, 760)], (40, 30, 70, 255), 10) for x in range(0, W2, 500)]; fl(d, (80, 60, 120, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def newsroom(path):                                          # halftone-yellow newsroom: press rollers, flying pages, dots
    im = M.sky((255, 210, 60), (255, 240, 170), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 46):
        for y in range(0, 900, 46): d.dot(x, y, 6 + (y // 150), (230, 170, 40, 255))
    for x in (500, 1700): d.dot(x, 760, 140, (90, 90, 110, 255)); d.ellipse(x, 760, 140, 140, outline=LINE, width=10)
    r = np.random.RandomState(2); [d.rrect(x, y, x + 120, y + 160, 6, fill=WT, outline=LINE, width=5) for x, y in zip(r.randint(0, W2, 9), r.randint(80, 500, 9))]
    fl(d, (180, 150, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def web(path):                                               # cyan-magenta neon web world: perspective grid, glowing nodes and links
    im = M.sky((40, 20, 90), (200, 50, 160), 1.0); d = Draw(W2, H2)
    for x in range(-1200, 3600, 160): d.stroke([(1200, 560), (x, 940)], (60, 230, 255, 160), 4)
    for y in (620, 700, 800, 940): d.stroke([(0, y), (W2, y)], (60, 230, 255, 160), 4)
    r = np.random.RandomState(1); pts = [(r.randint(100, 2300), r.randint(80, 500)) for _ in range(14)]
    for i, p in enumerate(pts): d.stroke([p, pts[(i + 3) % 14]], (255, 120, 220, 150), 4); d.dot(p[0], p[1], 14, CYN)
    fl(d, (60, 30, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def court(path):                                             # oak courtroom: tall windows with light beams, seal, railing
    im = M.sky((180, 120, 70), (240, 200, 150), 1.0); d = Draw(W2, H2)
    for x in (300, 1900): d.rrect(x, 120, x + 260, 700, 20, fill=(240, 236, 210, 255), outline=(120, 80, 40, 255), width=16)
    d.dot(1200, 300, 170, GLD); d.ellipse(1200, 300, 170, 170, outline=(150, 100, 40, 255), width=14); d.text(1200, 300, '*', 200, (150, 100, 40, 255))
    for x in range(100, W2, 120): d.rect(x, 760, x + 30, 900, (130, 80, 40, 255))
    d.rect(0, 750, W2, 780, (130, 80, 40, 255)); fl(d, (150, 100, 60, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def loft(path):                                              # amber-lilac night loft: window with city lights, string lights, plants
    im = M.sky((90, 60, 140), (220, 150, 160), 1.0); d = Draw(W2, H2); d.rrect(800, 120, 1700, 640, 20, fill=(40, 40, 90, 255), outline=(240, 200, 150, 255), width=18)
    M.stars(d, 25, 300, 6); [d.rect(x, 500 - (x * 13) % 200, x + 60, 640, (60, 60, 120, 255)) for x in range(820, 1690, 70)]
    d.stroke([(0, 100), (600, 180), (1200, 90), (1800, 170), (W2, 100)], LINE, 4); [d.dot(x, 140 + 40 * math.sin(x / 200), 14, HAZ) for x in range(40, W2, 120)]
    for x in (300, 2050): d.rrect(x - 70, 760, x + 70, 900, 20, fill=(200, 120, 80, 255)); d.ellipse(x, 700, 120, 90, fill=(90, 160, 90, 255))
    fl(d, (120, 90, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast5(('kenneth', 'lawa', 'lawb', 'judge2', 'mike'))
    def red(lines): return stopper(lines, face=HAZ, side=(170, 110, 0, 255), plate=(40, 34, 54, 255), rim=(255, 60, 200, 255), h=470)
    base_ = red(['SHE SUED TO', 'HIDE ONE PHOTO'])
    stop = {'default': base_, 'p0': redact(base_, 1.0), 'p1': redact(base_, 0.66), 'p2': redact(base_, 0.33), 'esc': red(['6 VIEWS BECAME', '400,000+!']), 'wait': red(['WHAT WENT', 'WRONG?!'])}
    multi = dict(stop=stop, mansion={'default': mansion(), 'shocked': mansion('shocked'), 'hide': mansion('hide'), 'famous': mansion('famous')}, plane={'default': plane()}, photos={'default': photos()},
                 p3850={'default': photo3850(), 'shocked': photo3850('shocked')}, scroll={'default': scroll()}, screen={'default': screen(), 'big': screen('big')}, paper={'default': paper()},
                 crowd={'default': crowd()}, casef={'default': casefile()}, fees={'default': fees()}, lost={'default': lost()}, laptop={'default': laptop(), 'name': laptop('name')}, warn={'default': warn()}, shovel={'default': shovel()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ = (100, 50, 150, 255), (20, 130, 140, 255)
    cards = dict(y2003=M.cal('AERIAL', '2003', SEA), kenc=P_('PHOTOGRAPHER', 'KENNETH ADELMAN', TQ, 980, 100, 96, YEL), coast=stamp('THE CALIFORNIA COAST', 960, SEA, 100, -3),
                 malibu=P_('A MALIBU', 'CLIFFTOP MANSION', CORAL, 960, 100, 110, YEL), sue=stamp('HER LAWYERS SUE!', 900, BURG, 112, 3), privacy=stamp('INVASION OF PRIVACY', 960, BURG, 100, -3),
                 absurd=stamp('THE ABSURD PART', 900, PU, 108, 3), six=M.bigneon('DOWNLOADED', '6 TIMES', 760, YEL, CYN), twolaw=P_('2 OF THEM:', 'HER OWN LAWYERS', BURG, 960, 110, 100, YEL),
                 public=stamp('A LAWSUIT IS PUBLIC', 960, TQ, 100, -3), news=stamp("IT'S NEWS!", 760, (220, 40, 60, 255), 130, 3), visits=M.bigneon('400,000+', 'PEOPLE VISITED', 820, YEL, (255, 130, 220, 255)),
                 everyone=stamp('EVERYONE WANTED TO SEE', 1000, PU, 96, 3), thrown=stamp('CASE THROWN OUT', 900, (220, 40, 60, 255), 110, -3), y2later=stamp('TWO YEARS LATER', 880, VIOL, 110, 3),
                 blogger=P_('BLOGGER', 'MIKE MASNICK', TQ, 900, 110, 120, YEL), explode=stamp('HIDE IT = IT EXPLODES', 980, (220, 40, 60, 255), 98, -3), label=M.bigneon('THE WARNING', 'LABEL', 760, YEL, (255, 130, 220, 255)),
                 sixppl=stamp('ONLY 6 PEOPLE HAD SEEN IT', 1000, PU, 92, 3), picture=stamp("NOW YOU'RE PICTURING IT", 1000, TQ, 92, -3))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('sandfl.jpg'), (220, 180, 140), (206, 166, 128)); M.sandtex(T('cloudfl.jpg'), (200, 220, 240), (186, 206, 226)); CE.tiles(T('labfl.jpg'), (50, 110, 120), (44, 98, 108)); CE.tiles(T('burgfl.jpg'), (130, 60, 70), (118, 52, 62))
    CE.tiles(T('pixfl.jpg'), (100, 70, 150), (90, 62, 136)); M.sandtex(T('newsfl.jpg'), (210, 180, 100), (196, 166, 90)); CE.tiles(T('webfl.jpg'), (80, 40, 120), (70, 34, 108)); B.tex_wood(T('wood.jpg')); CE.tiles(T('oakfl.jpg'), (170, 120, 70), (156, 108, 62))
    CE.tiles(T('loftfl.jpg'), (150, 110, 120), (136, 98, 108)); CE.tiles(T('pave.jpg'), (190, 150, 120), (176, 138, 108))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(malibu=malibu, aerial=aerial, lab=lab, office=office, pixel=pixel, newsroom=newsroom, web=web, court=court, loft=loft)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
