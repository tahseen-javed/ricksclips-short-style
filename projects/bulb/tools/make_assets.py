#!/usr/bin/env python3
"""Assets for video 32: the Hollywood sign was never about movies - a 1923 billboard for the Hollywoodland housing tract (13 letters ~45 ft
tall, 4,000 bulbs, $21,000, planned life ~1.5 years); nobody took it down, it fell apart, and a 1949 deal saved it on one condition: cut the
last four letters, L-A-N-D. Jazz-age hillside world (new palette): peach-magenta sunset hillside with the sign (hook + loop; a "????" tarp over
the last four letters = open loop, resolved as L-A-N-D), teal-gold art-deco developers' office, sage-terracotta morning lots, navy night with
glowing bulbs, dusty-rose slate 1940s ruin, mint-cream 1949 office with blinds, plum-gold premiere night. Cute cast (new): the publisher
(fedora, navy art-deco suit, mustache, glasses) and a 1923 bulb lineman (plaid newsboy cap, striped knit sweater). The letters L, A, N, D
are cute characters of their own. usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v29_assets import *

ROOT = B.ROOT
TEAL, GOLDC, PEACH, MAG, SAGE, TERRA, CRM, NAVY, PLUM = (30, 150, 150, 255), (240, 196, 80, 255), (255, 190, 150, 255), (230, 70, 140, 255), (150, 190, 140, 255), (210, 110, 80, 255), (252, 246, 232, 255), (30, 40, 90, 255), (90, 40, 100, 255)
LA.NEW.update({
    'chandler': dict(sk=0, style='slick', hair=(120, 110, 110, 255), suit=(40, 50, 100, 255), shade=(30, 38, 80, 255), body='deco', acc=(230, 70, 140, 255), xhat='fedora', hatc=(150, 120, 90, 255), stache=(120, 110, 110, 255), glasses=1),
    'lineman': dict(sk=1, style='spiky', hair=(60, 40, 30, 255), suit=(240, 236, 220, 255), shade=(214, 208, 190, 255), body='knit49', acc=(30, 150, 150, 255), xhat='newsboy', hatc=(200, 120, 80, 255), freckles=1),
})
LET = 'HOLLYWOODLAND'


def gloss(d, x, y, w, h): d.ellipse(x, y, w, h, fill=(255, 255, 255, 120))


def neon3(a, b, c, w=900, h=560):
    d = Draw(w, h); d.rrect(10, 10, w - 10, h - 10, 44, fill=(40, 20, 60, 255), outline=LINE, width=16); d.rrect(34, 34, w - 34, h - 34, 30, outline=GOLDC, width=8)
    d.text(w / 2, h * 0.2, a, LA.fit(a, 96, w - 160), (120, 230, 220, 255), stroke=6, stroke_fill=LINE)
    for k, (t, col) in enumerate(((b, YEL), (c, (255, 130, 180, 255)))): d.text(w / 2, h * (0.47 + 0.27 * k), t, LA.fit(t, 140, w - 110), col, stroke=7, stroke_fill=LINE)
    return d.out()


def sign(mode='land'):                                       # the hillside sign (hook: LAND under a ???? tarp; glow: bulbs lit; old: crooked, H fallen; cut: LAND gone)
    d = Draw(2400, 760); d.chord(1200, 760, 1250, 380, 180, 360, fill=(150, 130, 90, 255) if mode != 'glow' else (60, 70, 90, 255), outline=LINE, width=12)
    for k, ch in enumerate(LET):
        x = 110 + k * 168; gone = mode == 'cut' and k >= 9
        if gone: d.stroke([(x - 40, 560), (x + 40, 560)], (120, 100, 70, 255), 10); continue
        if mode == 'hook' and k >= 9: continue
        tilt = (k * 37 % 5 - 2) * 12 if mode == 'old' else 0; y = 200 + (90 if (mode == 'old' and k == 0) else 0)
        col = (255, 250, 236, 255) if mode != 'old' else (226, 214, 196, 255)
        d.rect(x - 4, y + 180, x + 4, 600, (120, 100, 80, 255)); d.text(x + tilt * 0.3, y + 80, ch, 220, col, stroke=10, stroke_fill=LINE)
        if mode == 'glow': [d.dot(x - 40 + i * 26, y - 20, 9, (255, 240, 150, 255)) for i in range(4)]
    if mode == 'hook': d.rrect(1590, 110, 2340, 470, 40, fill=(120, 80, 200, 255), outline=LINE, width=14); d.text(1965, 290, '????', 200, YEL, stroke=10, stroke_fill=LINE)
    if mode == 'old': [d.arc(300 + k * 520, 120, 60, 40, 200, 340, (200, 200, 210, 255), 6) for k in range(4)]
    return d.out()


def letter(ch, face='happy'):                                # one cute giant letter with a face (L, A, N or D)
    d = Draw(900, 1100); d.text(450, 520, ch, 900, (255, 250, 236, 255), stroke=26, stroke_fill=LINE); gloss(d, 300, 200, 70, 30)
    eyes(d, 450 if ch != 'L' else 320, 560, 0.8, face); d.rect(300, 1040, 600, 1090, (150, 120, 90, 255)); return d.out()


def house():                                                 # Spanish-style hillside cottage with a red tile roof and a happy door face
    d = Draw(1300, 1100); d.rect(160, 420, 1140, 1060, (250, 236, 210, 255)); d.rrect(160, 420, 1140, 1060, 2, outline=LINE, width=12)
    d.poly([(100, 440), (650, 160), (1200, 440)], fill=TERRA, outline=LINE, width=12); [d.arc(200 + k * 120, 440, 60, 40, 180, 360, (170, 80, 60, 255), 6) for k in range(9)]
    d.chord(650, 1060, 140, 240, 180, 360, fill=(120, 80, 60, 255), outline=LINE, width=10); [win(d, x, 560, x + 170, 760, (170, 220, 250, 255)) for x in (260, 870)]; eyes(d, 650, 720, 0.6, 'happy'); return d.out()


def lots():                                                  # hillside lots: stakes, LOTS FOR SALE sign, SOLD flags
    d = Draw(1800, 1000); d.chord(900, 1000, 900, 560, 180, 360, fill=SAGE, outline=LINE, width=12)
    for k in range(5): x, y = 300 + k * 300, 700 - (2 - abs(k - 2)) * 90; d.stroke([(x - 120, y + 60), (x + 120, y + 60)], WT, 6); d.rect(x - 6, y - 60, x + 6, y + 60, (140, 100, 60, 255)); d.poly([(x + 6, y - 60), (x + 90, y - 40), (x + 6, y - 20)], fill=MAG if k % 2 else GOLDC)
    d.rrect(600, 160, 1200, 380, 20, fill=CRM, outline=LINE, width=10); d.text(900, 230, 'LOTS', 90, TERRA); d.text(900, 320, 'FOR SALE', 70, TEAL); d.rect(890, 380, 910, 560, (140, 100, 60, 255)); return d.out()


def paper():                                                 # 1923 newspaper: big ad for hillside lots, a happy face in the masthead
    d = Draw(1100, 1300); d.rrect(80, 60, 1020, 1240, 20, fill=(246, 240, 226, 255), outline=LINE, width=14); d.text(550, 170, 'THE TIMES', 120, LINE); d.stroke([(120, 250), (980, 250)], LINE, 8)
    d.rrect(140, 300, 960, 760, 20, fill=PEACH, outline=LINE, width=10); d.text(550, 420, 'HOLLYWOODLAND', 90, NAVY); d.text(550, 560, 'LOTS FOR SALE!', 80, MAG); d.chord(550, 740, 300, 90, 180, 360, fill=SAGE)
    [d.stroke([(140, y), (960, y)], (200, 190, 170, 255), 12) for y in range(830, 1180, 60)]; eyes(d, 860, 170, 0.35, 'happy'); return d.out()


def giant():                                                 # one 45-ft letter H with a tiny worker on a ladder and a 45 FT arrow
    d = Draw(1300, 1300); d.text(560, 640, 'H', 1200, (255, 250, 236, 255), stroke=26, stroke_fill=LINE); eyes(d, 560, 640, 0.7, 'happy')
    d.stroke([(1120, 120), (1120, 1220)], MAG, 14); d.poly([(1090, 140), (1150, 140), (1120, 80)], fill=MAG); d.poly([(1090, 1200), (1150, 1200), (1120, 1260)], fill=MAG); d.text(1200, 660, '45', 90, MAG, stroke=5, stroke_fill=LINE)
    d.stroke([(880, 1250), (960, 900)], (150, 100, 60, 255), 10); d.dot(940, 880, 36, (255, 222, 196, 255)); d.ellipse(940, 880, 36, 36, outline=LINE, width=6); d.chord(940, 868, 40, 30, 180, 360, fill=(200, 120, 80, 255)); return d.out()


def bulbs(mode='on'):                                        # cluster of light bulbs with faces (on: glowing)
    d = Draw(1400, 1000)
    for k, (x, y) in enumerate(((300, 400), (700, 300), (1100, 400), (500, 680), (900, 680))):
        on = mode == 'on'; d.dot(x, y, 150, (255, 246, 170, 255) if on else (220, 230, 240, 255)); d.ellipse(x, y, 150, 150, outline=LINE, width=12); d.rrect(x - 60, y + 140, x + 60, y + 230, 14, fill=(170, 170, 186, 255), outline=LINE, width=8)
        eyes(d, x, y, 0.5, 'happy' if on else 'sad'); gloss(d, x - 60, y - 70, 40, 20)
        if on: [d.stroke([(x + 170 * math.cos(a), y + 170 * math.sin(a)), (x + 220 * math.cos(a), y + 220 * math.sin(a))], YEL, 10) for a in (3.6, 4.7, 5.8)]
    return d.out()


def hourglass():                                             # planned life: hourglass with 1.5 YEARS, a worried face
    d = Draw(900, 1200); d.rrect(140, 60, 760, 140, 20, fill=(150, 100, 60, 255), outline=LINE, width=10); d.rrect(140, 1060, 760, 1140, 20, fill=(150, 100, 60, 255), outline=LINE, width=10)
    d.poly([(200, 140), (700, 140), (470, 600), (700, 1060), (200, 1060), (430, 600)], fill=(220, 240, 250, 255), outline=LINE, width=12); d.poly([(300, 240), (600, 240), (450, 520)], fill=GOLDC); d.poly([(450, 760), (620, 1050), (280, 1050)], fill=GOLDC)
    eyes(d, 450, 360, 0.45, 'shocked'); return d.out()


def contract(mode='default'):                                # 1949 deal: contract with handshake seal (cut: big red scissors line through LAND)
    d = Draw(1200, 1300); d.rrect(120, 60, 1080, 1240, 20, fill=CRM, outline=LINE, width=14); d.text(600, 180, 'THE DEAL', 110, NAVY); [d.stroke([(200, y), (1000, y)], (210, 200, 180, 255), 10) for y in range(300, 560, 60)]
    d.rrect(200, 620, 1000, 860, 20, fill=(255, 236, 236, 255), outline=MAG, width=10); d.text(600, 690, 'CONDITION:', 60, MAG); d.text(600, 790, 'CUT "LAND"', 90, (200, 40, 70, 255))
    d.dot(850, 1060, 110, GOLDC); d.ellipse(850, 1060, 110, 110, outline=LINE, width=10); eyes(d, 400, 1060, 0.6, 'happy')
    if mode == 'cut': d.stroke([(160, 900), (1040, 560)], (230, 50, 80, 255), 30)
    return d.out()


def scissors():                                              # giant scissors with a face chopping a LAND ribbon
    d = Draw(1500, 900); d.rrect(60, 600, 1440, 760, 40, fill=MAG, outline=LINE, width=12); d.text(1100, 680, 'LAND', 100, WT, stroke=5, stroke_fill=LINE)
    d.poly([(400, 420), (1000, 640), (980, 690), (380, 480)], fill=(200, 204, 214, 255), outline=LINE, width=10); d.poly([(400, 520), (1000, 650), (980, 610), (380, 460)], fill=(220, 224, 234, 255), outline=LINE, width=10)
    for y in (380, 580): d.ellipse(260, y, 120, 80, outline=TERRA, width=34)
    eyes(d, 700, 520, 0.5, 'happy'); return d.out()


def globe():                                                 # Earth with the HOLLYWOOD sign on top and orbiting stars + a film reel
    d = Draw(1300, 1300); d.dot(650, 700, 480, (90, 170, 240, 255)); [d.ellipse(650 + dx, 700 + dy, rx, ry, fill=(120, 200, 120, 255)) for dx, dy, rx, ry in ((-160, -120, 150, 110), (180, 60, 130, 160), (-60, 240, 120, 70))]
    d.ellipse(650, 700, 480, 480, outline=LINE, width=14); gloss(d, 480, 420, 120, 50); eyes(d, 650, 760, 0.9, 'happy')
    d.rrect(330, 140, 970, 290, 20, fill=CRM, outline=LINE, width=10); d.text(650, 215, 'HOLLYWOOD', 100, NAVY); [d.text(x, y, '*', 120, YEL, stroke=5, stroke_fill=LINE) for x, y in ((150, 300), (1150, 380), (1120, 1100), (180, 1080))]
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def sunset(path):                                            # peach-magenta sunset over the Hollywood hills, palms, searchlight beams
    im = sky((230, 90, 150), (255, 200, 150), 1.0); d = Draw(W2, H2); [d.poly([(x, 940), (x + 60, 0), (x + 140, 0)], fill=(255, 240, 210, 50)) for x in (300, 1900)]
    hills(d, 620, (170, 100, 130, 255), 120, 2); hills(d, 760, (120, 90, 110, 255), 70, 3, 0.8)
    for x in (200, 700, 1800, 2250): d.stroke([(x, 940), (x + 20, 560)], (90, 60, 50, 255), 16); [d.ellipse(x + 20 + 80 * math.cos(a), 560 + 40 * math.sin(a), 70, 18, fill=(60, 110, 70, 255)) for a in np.linspace(0, 6.28, 7)]
    fl(d, (150, 110, 100, 255)); im.alpha_composite(d.out()); glow(im, 1200, 640, 600, (255, 200, 150, 110), 140); im.convert('RGB').save(path)


def deco(path):                                              # teal-gold art-deco office: sunburst panels, tall windows, gold trim
    im = sky((20, 110, 120), (60, 170, 170), 1.0); d = Draw(W2, H2)
    for x in range(200, W2, 500): [d.poly([(x, 900), (x - 180 + k * 60, 200), (x - 150 + k * 60, 200)], fill=(240, 196, 80, 120)) for k in range(7)]
    for x in (700, 1700): d.rrect(x - 150, 150, x + 150, 700, 20, fill=(200, 236, 236, 255), outline=GOLDC, width=16)
    d.rect(0, 860, W2, 900, GOLDC); fl(d, (60, 80, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def sage(path):                                              # sage-terracotta morning hills: tiny houses, winding road, eucalyptus
    im = sky((190, 220, 240), (255, 236, 210), 1.0); d = Draw(W2, H2); hills(d, 600, (170, 200, 150, 255), 110, 2); hills(d, 760, (150, 180, 130, 255), 60, 3, 1.1)
    for k in range(9): x, y = 150 + k * 260, 640 + (k % 3) * 60; d.rect(x, y, x + 90, y + 60, CRM); d.poly([(x - 10, y), (x + 45, y - 40), (x + 100, y)], fill=TERRA)
    d.stroke([(0, 900), (600, 820), (1200, 880), (1800, 800), (W2, 860)], (230, 210, 180, 255), 24); fl(d, (170, 150, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def nightglow(path):                                         # navy 1923 night: stars, moon, twinkling city lights below the hill
    im = sky((20, 30, 90), (70, 90, 170), 1.0); d = Draw(W2, H2); stars(d, 120, 600, 13); d.dot(2000, 200, 80, (255, 246, 210, 255))
    hills(d, 760, (40, 50, 100, 255), 70, 3); r = np.random.RandomState(2); [d.dot(r.randint(0, W2), r.randint(800, 930), 6, (255, 220, 140, 255)) for _ in range(120)]
    fl(d, (60, 70, 110, 255)); im.alpha_composite(d.out()); glow(im, 2000, 200, 200, (255, 240, 200, 100), 60); im.convert('RGB').save(path)


def ruin(path):                                              # dusty-rose slate 1940s: overcast, dry brush, tumbleweeds, broken fence
    im = sky((150, 150, 170), (230, 180, 180), 1.0); d = Draw(W2, H2); hills(d, 680, (170, 140, 140, 255), 90, 2)
    for x, y in ((300, 160), (1400, 120), (2000, 200)): [d.dot(x + k * 120, y + (k % 2) * 30, 100, (200, 196, 210, 240)) for k in range(4)]
    for x in (400, 1500, 2100): d.ellipse(x, 880, 70, 60, outline=(150, 110, 80, 255), width=10)
    for x in range(100, W2, 260): d.rect(x, 780, x + 12, 900, (120, 100, 90, 255))
    fl(d, (170, 140, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def blinds(path):                                            # mint-cream 1949 office: venetian blind light stripes, desk lamp, filing cabinets
    im = sky((170, 230, 210), (250, 246, 230), 1.0); d = Draw(W2, H2); d.rrect(800, 120, 1600, 620, 20, fill=(255, 250, 230, 255), outline=(120, 150, 140, 255), width=20)
    [d.rect(820, y, 1580, y + 18, (150, 180, 170, 255)) for y in range(150, 610, 50)]; [d.rect(x, 560, x + 220, 940, (120, 160, 150, 255)) for x in (150, 2000)]
    fl(d, (140, 120, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def premiere(path):                                          # plum-gold premiere night: crossing searchlights, star sparkles, velvet ropes
    im = sky((70, 30, 90), (200, 90, 140), 1.0); d = Draw(W2, H2)
    for x0, x1 in ((300, 900), (2100, 1400), (900, 300), (1500, 2200)): d.poly([(x0, 940), (x1 - 80, 0), (x1 + 80, 0)], fill=(255, 240, 200, 60))
    r = np.random.RandomState(6); [d.text(r.randint(0, W2), r.randint(40, 700), '*', 60, (255, 230, 150, 255)) for _ in range(26)]
    for x in range(100, W2, 300): d.rect(x, 760, x + 16, 900, GOLDC); d.dot(x + 8, 750, 18, GOLDC)
    d.stroke([(100, 790), (400, 840), (700, 790), (1000, 840), (1300, 790), (1600, 840), (1900, 790), (2200, 840)], (200, 40, 70, 255), 14)
    fl(d, (160, 50, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast4(('chandler', 'lineman'))
    multi = dict(sign={'default': sign('hook'), 'land': sign('land'), 'glow': sign('glow'), 'old': sign('old'), 'cut': sign('cut')},
                 letL={'default': letter('L'), 'bye': letter('L', 'shocked')}, letA={'default': letter('A'), 'bye': letter('A', 'shocked')}, letN={'default': letter('N'), 'bye': letter('N', 'shocked')}, letD={'default': letter('D'), 'bye': letter('D', 'shocked')},
                 house={'default': house()}, lots={'default': lots()}, paper={'default': paper()}, giant={'default': giant()}, bulbs={'default': bulbs(), 'off': bulbs('off')},
                 hourglass={'default': hourglass()}, contract={'default': contract(), 'cut': contract('cut')}, scissors={'default': scissors()}, globe={'default': globe()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ, RB = (100, 40, 120, 255), (20, 120, 120, 255), (190, 50, 80, 255)
    cards = dict(hookc=neon3('THE HOLLYWOOD SIGN', 'WAS NEVER ABOUT', 'MOVIES!'),
                 adc=stamp('A BILLBOARD FOR HOUSES!', 1000, RB, 100, -3),
                 down=stamp('BUILT TO COME DOWN', 960, PU, 110, 3),
                 y1923=M.cal('L.A.', '1923', TQ),
                 pubc=P_('PUBLISHER OF THE', 'L.A. TIMES', NAVY, 900, 100, 150, YEL),
                 hlandc=P_('A NEIGHBORHOOD', 'HOLLYWOODLAND', TQ, 960, 100, 130, YEL),
                 thirteen=M.bigneon('13', 'LETTERS', 640, YEL, (120, 230, 220, 255)),
                 ft45=M.bigneon('EACH ABOUT', '45 FEET TALL', 860, YEL, (255, 130, 180, 255)),
                 bulbc=M.bigneon('4,000', 'LIGHT BULBS', 760, YEL, GOLDC),
                 lifec=P_('PLANNED LIFE', '1.5 YEARS', RB, 820, 120, 170, YEL),
                 nobody=stamp('NOBODY TOOK IT DOWN', 980, PU, 105, -3),
                 apart=stamp('FALLING APART...', 820, (120, 110, 130, 255), 120, 3),
                 y1949=M.cal('THE DEAL', '1949', RB),
                 cond=stamp('ONE CONDITION', 820, MAG, 125, -3),
                 famous=P_('MOST FAMOUS', 'MOVIE SIGN', PU, 820, 130, 160, YEL),
                 realad=M.bigneon('A REAL', 'ESTATE AD!', 760, YEL, (255, 130, 180, 255)))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('hillfl.jpg'), (170, 130, 110), (156, 118, 100)); CE.tiles(T('decofl.jpg'), (40, 90, 100), (34, 80, 90)); M.sandtex(T('sagefl.jpg'), (170, 170, 120), (156, 156, 108)); M.sandtex(T('nightfl.jpg'), (70, 80, 120), (62, 72, 110))
    M.sandtex(T('dustfl.jpg'), (180, 150, 140), (166, 138, 128)); CE.tiles(T('officefl.jpg'), (160, 140, 110), (146, 128, 100)); CE.tiles(T('carpet.jpg'), (190, 60, 90), (176, 52, 80)); CE.tiles(T('pave.jpg'), (120, 100, 90), (106, 88, 78)); B.tex_wood(T('wood.jpg'))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(sunset=sunset, deco=deco, sage=sage, nightglow=nightglow, ruin=ruin, blinds=blinds, premiere=premiere)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
