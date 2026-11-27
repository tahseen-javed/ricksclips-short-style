#!/usr/bin/env python3
"""Assets for video 34: the man who invented the stop sign never learned to drive (William Phelps Eno: New York 1867, age nine, stuck in
a jam of about a dozen horses and carriages; 1900 article -> New York's first written traffic regulations; stop sign, one-way streets,
traffic circles; father of traffic safety; foundation 1921; a horseman whose carriage rules cars inherited). Gilded-traffic world (new
palette): cobalt-pink dusk crossroads (hook + loop), foggy amber-teal 1867 Broadway, mint study, cream-gold marble hall, candy-pastel toy
roads, lilac campus, golden-hour stable, sky-blue split road. Accent ruby #e8173c. Cute cast (new): young William (sailor cap + sailor suit,
ginger hair, freckles), his mother (flower hat, lilac bustle dress), adult Eno the horseman (black riding bowler, red riding coat, mustache),
1867 policeman (navy dome helmet, frock coat). usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v33_assets import *

ROOT = B.ROOT
RUBY, COB, MNT, CRM, GLD, LIL, BRN, SKY, PNK = (232, 23, 60, 255), (40, 70, 170, 255), (150, 230, 200, 255), (252, 246, 232, 255), (240, 190, 70, 255), (200, 170, 240, 255), (150, 100, 60, 255), (150, 210, 250, 255), (255, 150, 190, 255)
LA.NEW.update({
    'willy': dict(sk=0, style='spiky', hair=(220, 110, 50, 255), suit=(240, 244, 250, 255), shade=(210, 216, 230, 255), body='sailorsuit', acc=COB, xhat='sailor', hatc=COB, freckles=1),
    'mom': dict(sk=0, style='bob', hair=(120, 70, 40, 255), band=PNK, suit=(190, 160, 230, 255), shade=(160, 130, 200, 255), body='bustle', acc=PNK, xhat='flowerhat', hatc=(250, 220, 200, 255)),
    'eno': dict(sk=0, style='part', hair=(140, 130, 120, 255), suit=(210, 40, 50, 255), shade=(170, 30, 40, 255), body='redcoat', acc=GLD, xhat='riding', hatc=(40, 36, 44, 255), stache=(140, 130, 120, 255)),
    'cop': dict(sk=2, style='flat', hair=(40, 30, 30, 255), suit=(40, 50, 110, 255), shade=(30, 40, 90, 255), body='police67', acc=GLD, xhat='bobby', hatc=(40, 50, 110, 255)),
})


def octo(d, cx, cy, r, fill, rim=WT):
    pts = [(cx + r * math.cos(math.radians(22.5 + k * 45)), cy + r * math.sin(math.radians(22.5 + k * 45))) for k in range(8)]
    d.poly(pts, fill=LINE); d.poly([(cx + (r - 14) * math.cos(math.radians(22.5 + k * 45)), cy + (r - 14) * math.sin(math.radians(22.5 + k * 45))) for k in range(8)], fill=rim)
    d.poly([(cx + (r - 34) * math.cos(math.radians(22.5 + k * 45)), cy + (r - 34) * math.sin(math.radians(22.5 + k * 45))) for k in range(8)], fill=fill)


def stopsign(face='happy'):                                  # glossy octagon STOP sign on a pole, a cute face under the word
    d = Draw(1000, 1500); d.rect(470, 800, 530, 1490, (170, 176, 190, 255)); d.rrect(470, 800, 530, 1490, 8, outline=LINE, width=8); octo(d, 500, 460, 430, RUBY)
    d.text(500, 330, 'STOP', 210, WT, stroke=8, stroke_fill=LINE); eyes5(d, 500, 570, 1.1, face); d.ellipse(330, 180, 90, 30, fill=(255, 255, 255, 90)); return d.out()


def car(mode='default'):                                     # cute modern bubble car (x: big red X for "not cars")
    d = Draw(1400, 900); d.rrect(100, 380, 1300, 760, 120, fill=SKY, outline=LINE, width=14); d.chord(700, 400, 420, 300, 180, 360, fill=SKY, outline=LINE, width=14)
    d.chord(700, 400, 340, 230, 180, 360, fill=(220, 244, 255, 255)); d.rect(690, 170, 710, 400, SKY); [d.dot(x, 770, 120, (50, 50, 60, 255)) for x in (360, 1040)]; [d.dot(x, 770, 52, (210, 210, 220, 255)) for x in (360, 1040)]
    d.dot(1250, 520, 40, YEL); eyes(d, 700, 560, 0.7, 'shocked' if mode == 'x' else 'happy')
    if mode == 'x': d.stroke([(160, 140), (1240, 860)], RUBY, 70); d.stroke([(1240, 140), (160, 860)], RUBY, 70)
    return d.out()


def horse(face='happy', w=1200):                             # chibi horse: round body, big head, mane, little hooves
    d = Draw(1200, 1100); bc = (190, 130, 80, 255); mn = (90, 50, 40, 255)
    for x in (330, 480, 760, 900): d.rrect(x - 40, 640, x + 40, 1000, 30, fill=bc, outline=LINE, width=10); d.rrect(x - 44, 960, x + 44, 1040, 20, fill=mn)
    d.ellipse(600, 600, 380, 220, fill=bc, outline=LINE, width=14); d.stroke([(230, 560), (130, 760)], mn, 50)
    d.ellipse(930, 360, 210, 190, fill=bc, outline=LINE, width=14); d.ellipse(1040, 450, 120, 90, fill=(230, 180, 140, 255), outline=LINE, width=10)
    [d.poly([(x, 200), (x + 40, 120), (x + 70, 210)], fill=bc, outline=LINE, width=8) for x in (820, 930)]; [d.dot(780 + k * 50, 230 + k * 40, 50, mn) for k in range(4)]
    eyes(d, 930, 340, 0.55, face); return d.out()


def carriage(face='happy'):                                  # horse-drawn carriage with a cute face and big spoked wheels
    d = Draw(1400, 1000); d.rrect(300, 260, 1100, 720, 80, fill=(120, 40, 70, 255), outline=LINE, width=14); d.rrect(380, 320, 640, 520, 30, fill=(240, 220, 180, 255), outline=LINE, width=10)
    d.rect(250, 230, 1150, 270, GLD); for_w = [(420, 780, 170), (980, 780, 200)]
    for x, y, r in for_w: d.dot(x, y, r, (240, 210, 120, 255)); d.ellipse(x, y, r, r, outline=LINE, width=12); [d.stroke([(x, y), (x + r * math.cos(a), y + r * math.sin(a))], LINE, 6) for a in np.linspace(0, 6.28, 9)]; d.dot(x, y, 30, LINE)
    d.stroke([(1100, 560), (1360, 520)], (120, 80, 50, 255), 18); eyes(d, 870, 440, 0.6, face); return d.out()


def jam():                                                   # 1867 traffic knot: carriages and horses tangled in a circle, "?" bubbles
    d = Draw(1600, 1100); d.ellipse(800, 600, 700, 380, fill=(200, 180, 150, 255))
    for k in range(7):
        a = k * 0.9; x, y = 800 + 450 * math.cos(a), 600 + 250 * math.sin(a); col = ((120, 40, 70, 255), (60, 100, 160, 255), (60, 130, 90, 255))[k % 3]
        d.rrect(x - 150, y - 90, x + 150, y + 90, 40, fill=col, outline=LINE, width=10); d.ellipse(x + 160 * math.cos(a + 1.6), y + 100 * math.sin(a + 1.6), 80, 60, fill=(190, 130, 80, 255), outline=LINE, width=8)
        eyes(d, x, y, 0.3, 'shocked')
    for x, y in ((420, 160), (800, 110), (1180, 170)): d.dot(x, y, 70, WT); d.ellipse(x, y, 70, 70, outline=LINE, width=8); d.text(x, y, '?', 90, RUBY)
    return d.out()


def article():                                               # the 1900 article: newspaper with a big headline and a little stop hand
    d = Draw(1100, 1300); d.rrect(80, 60, 1020, 1240, 20, fill=(246, 240, 226, 255), outline=LINE, width=14); d.text(550, 170, 'THE DAILY', 110, LINE); d.stroke([(120, 250), (980, 250)], LINE, 8)
    d.rrect(140, 300, 960, 720, 20, fill=(255, 230, 230, 255), outline=RUBY, width=10); d.text(550, 420, 'REAL', 120, RUBY); d.text(550, 580, 'TRAFFIC RULES!', 100, COB)
    [d.stroke([(140, y), (960, y)], (200, 190, 170, 255), 12) for y in range(800, 1180, 60)]; eyes(d, 860, 170, 0.35, 'happy'); return d.out()


def regs():                                                  # New York's first written traffic regulations: a fat rule book with a ribbon
    d = Draw(1100, 1300); d.rrect(140, 120, 1000, 1220, 40, fill=dk(COB, 0.7), outline=LINE, width=14); d.rrect(110, 80, 960, 1180, 40, fill=COB, outline=LINE, width=14)
    d.rrect(200, 220, 870, 560, 24, fill=CRM, outline=GLD, width=10); d.text(535, 320, 'TRAFFIC', 110, RUBY); d.text(535, 460, 'REGULATIONS', 84, COB)
    d.text(535, 660, 'NEW YORK', 80, GLD, stroke=5, stroke_fill=LINE); d.rect(760, 1100, 820, 1290, RUBY); eyes(d, 535, 880, 0.6, 'happy'); return d.out()


def oneway():                                                # ONE WAY arrow sign with a face
    d = Draw(1400, 1200); d.rect(670, 600, 730, 1190, (170, 176, 190, 255)); d.rrect(100, 200, 1300, 620, 40, fill=LINE); d.rrect(120, 220, 1280, 600, 30, fill=WT)
    d.poly([(180, 340), (980, 340), (980, 260), (1240, 410), (980, 560), (980, 480), (180, 480)], fill=LINE); d.text(560, 410, 'ONE WAY', 110, WT); eyes(d, 700, 820, 0.5, 'happy'); return d.out()


def circle():                                                # traffic circle model: round island with a tree, three little cars driving round
    d = Draw(1500, 1100); d.ellipse(750, 600, 700, 440, fill=(110, 110, 130, 255), outline=LINE, width=14); d.ellipse(750, 600, 300, 190, fill=(150, 220, 140, 255), outline=LINE, width=12)
    d.ellipse(750, 600, 500, 315, outline=WT, width=10); d.dot(750, 520, 110, (90, 170, 90, 255)); d.rect(735, 540, 765, 640, BRN); eyes(d, 750, 660, 0.4, 'happy')
    for k, c in enumerate((RUBY, YEL, SKY)): a = 0.6 + k * 2.1; x, y = 750 + 500 * math.cos(a), 600 + 315 * math.sin(a); d.rrect(x - 70, y - 40, x + 70, y + 40, 24, fill=c, outline=LINE, width=8)
    d.poly([(1220, 300), (1300, 260), (1280, 340)], fill=WT); return d.out()


def trophy():                                                # golden trophy for the father of traffic safety, a tiny stop sign on top
    d = Draw(1000, 1300); d.rrect(260, 1060, 740, 1200, 20, fill=BRN, outline=LINE, width=12); d.rect(440, 820, 560, 1060, GLD); d.chord(500, 420, 330, 420, 0, 180, fill=GLD, outline=LINE, width=14)
    [d.arc(x, 560, 110, 150, a0, a1, GLD, 30) for x, a0, a1 in ((170, 90, 270), (830, 270, 450))]; octo(d, 500, 280, 130, RUBY); d.text(500, 280, 'STOP', 60, WT)
    d.ellipse(380, 520, 50, 120, fill=(255, 255, 255, 110)); eyes(d, 500, 640, 0.6, 'happy'); return d.out()


def foundation():                                            # the foundation house: columns, pediment, a 1921 stone, a happy door
    d = Draw(1600, 1200); d.rect(200, 440, 1400, 1160, CRM); d.rrect(200, 440, 1400, 1160, 2, outline=LINE, width=14); d.poly([(140, 450), (800, 150), (1460, 450)], fill=(230, 220, 200, 255), outline=LINE, width=14)
    for x in range(300, 1400, 220): d.rect(x, 480, x + 70, 1060, (240, 236, 226, 255)); d.rrect(x, 480, x + 70, 1060, 4, outline=LINE, width=8)
    d.rrect(560, 230, 1040, 420, 20, fill=COB, outline=LINE, width=10); d.text(800, 325, '1921', 130, GLD, stroke=6, stroke_fill=LINE); d.chord(800, 1160, 120, 200, 180, 360, fill=(120, 60, 50, 255), outline=LINE, width=10)
    eyes(d, 800, 820, 0.5, 'happy'); return d.out()


def wheel(mode='default'):                                   # a steering wheel he never needed (x: big ruby no-sign over it)
    d = Draw(1200, 1200); d.ellipse(600, 600, 440, 440, outline=LINE, width=110); d.ellipse(600, 600, 440, 440, outline=(80, 80, 100, 255), width=80)
    for a in (90, 210, 330): d.stroke([(600, 600), (600 + 400 * math.cos(math.radians(a)), 600 + 400 * math.sin(math.radians(a)))], (80, 80, 100, 255), 60)
    d.dot(600, 600, 150, (110, 110, 130, 255)); d.ellipse(600, 600, 150, 150, outline=LINE, width=12); eyes(d, 600, 590, 0.55, 'shocked' if mode == 'x' else 'happy')
    if mode == 'x': d.ellipse(600, 600, 560, 560, outline=RUBY, width=70); d.stroke([(200, 1000), (1000, 200)], RUBY, 70)
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def dusk(path):                                              # cobalt-pink dusk crossroads: skyline with glowing windows, traffic lights, stars
    im = M.sky((40, 60, 170), (255, 150, 190), 1.0); d = Draw(W2, H2); M.stars(d, 50, 300, 4)
    for k in range(13): x = k * 190; h = 260 + (k * 71) % 280; d.rect(x, 900 - h, x + 160, 940, (50, 50, 120, 255)); [d.rect(x + 24 + j * 50, 900 - h + 40 + i * 70, x + 50 + j * 50, 900 - h + 80 + i * 70, (255, 220, 140, 255)) for j in range(2) for i in range(2)]
    for x in (500, 1900): d.rect(x, 560, x + 20, 940, (40, 40, 60, 255)); d.rrect(x - 40, 440, x + 60, 600, 20, fill=(40, 40, 60, 255)); [d.dot(x + 10, 470 + i * 45, 18, c) for i, c in enumerate((RUBY, YEL, (60, 230, 120, 255)))]
    fl(d, (90, 80, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def broadway(path):                                          # foggy amber-teal 1867 Broadway: shop fronts with awnings, telegraph wires, gas lamps
    im = M.sky((60, 120, 130), (240, 190, 130), 1.0); d = Draw(W2, H2)
    for k in range(9): x = k * 270; d.rect(x, 380, x + 250, 940, ((170, 110, 90, 255), (140, 120, 100, 255), (180, 140, 110, 255))[k % 3]); [d.rect(x + 30 + j * 80, 450, x + 80 + j * 80, 560, (255, 220, 150, 255)) for j in range(3)]; d.poly([(x, 640), (x + 250, 640), (x + 230, 700), (x + 20, 700)], fill=(RUBY, (60, 140, 140, 255), GLD)[k % 3])
    for y in (220, 260): d.stroke([(0, y), (W2, y + 30)], LINE, 4)
    for x in (300, 1300, 2100): d.rect(x, 600, x + 14, 940, LINE); d.dot(x + 7, 590, 30, (255, 220, 140, 255))
    fl(d, (150, 120, 100, 255)); im.alpha_composite(d.out()); CE.glow(im, 1200, 500, 900, (255, 230, 200, 60), 120); im.convert('RGB').save(path)


def study(path):                                             # mint study: tall bookshelves, arched window, green lamp glow
    im = M.sky((150, 220, 200), (240, 250, 240), 1.0); d = Draw(W2, H2); d.chord(1200, 700, 260, 520, 180, 360, fill=(200, 236, 250, 255), outline=(90, 140, 120, 255), width=16)
    for x0 in (150, 1650):
        for y in range(200, 880, 140): d.rect(x0, y, x0 + 600, y + 16, (120, 90, 60, 255)); [d.rect(x0 + 10 + j * 40, y - 100 + (j % 3) * 10, x0 + 42 + j * 40, y, (RUBY, COB, GLD, (60, 140, 100, 255))[j % 4]) for j in range(14)]
    fl(d, (120, 150, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def marble(path):                                            # cream-gold marble hall: columns, gold trim, a big round window
    im = M.sky((240, 220, 180), (255, 248, 230), 1.0); d = Draw(W2, H2); d.dot(1200, 380, 220, (220, 236, 250, 255)); d.ellipse(1200, 380, 220, 220, outline=GLD, width=20)
    for x in range(100, W2, 330): d.rect(x, 140, x + 110, 900, (250, 246, 236, 255)); d.rect(x - 20, 120, x + 130, 160, GLD); [d.rect(x + 16 + j * 26, 170, x + 24 + j * 26, 880, (230, 224, 210, 255)) for j in range(4)]
    fl(d, (200, 180, 150, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def candy(path):                                             # candy-pastel toy-road world: puffy clouds, lollipop trees, rainbow hills
    im = M.sky((255, 190, 220), (190, 240, 255), 1.0); d = Draw(W2, H2)
    for x, y in ((300, 200), (1300, 140), (2000, 260)): [d.dot(x + k * 110, y + (k % 2) * 30, 90, (255, 255, 255, 230)) for k in range(4)]
    hills(d, 700, (200, 240, 180, 255), 90, 2); hills(d, 800, (255, 210, 160, 255), 50, 4, 0.7)
    for x in range(150, W2, 300): d.rect(x, 640, x + 14, 860, WT); d.dot(x + 7, 620, 50, (RUBY, (150, 120, 240, 255), (60, 200, 160, 255))[x // 300 % 3])
    fl(d, (180, 180, 200, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def campus(path):                                            # lilac campus: round trees, paths, brick wall, morning glow
    im = M.sky((170, 150, 230), (250, 230, 245), 1.0); d = Draw(W2, H2); hills(d, 720, (160, 200, 170, 255), 60, 3)
    for x in range(100, W2, 260): ptree(d, x, 860, 0.9, (120, 180, 130, 255))
    d.rect(0, 860, W2, 900, (190, 120, 100, 255)); fl(d, (170, 160, 180, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def stable(path):                                            # golden-hour stable: red barn, hay bales, paddock fence, low sun
    im = M.sky((255, 170, 90), (255, 230, 170), 1.0); d = Draw(W2, H2); d.dot(1700, 600, 160, (255, 240, 190, 255)); hills(d, 760, (210, 170, 90, 255), 50, 2)
    d.rect(300, 420, 900, 900, (190, 60, 50, 255)); d.poly([(260, 440), (600, 220), (940, 440)], fill=(120, 40, 40, 255)); d.rect(520, 640, 680, 900, (250, 230, 200, 255)); d.stroke([(520, 640), (680, 900)], (190, 60, 50, 255), 12)
    for x in range(1000, W2, 180): d.rect(x, 760, x + 18, 920, (140, 90, 50, 255))
    d.stroke([(1000, 790), (W2, 790)], (140, 90, 50, 255), 12); d.stroke([(1000, 860), (W2, 860)], (140, 90, 50, 255), 12); [d.ellipse(x, 880, 90, 50, fill=(240, 200, 100, 255)) for x in (1200, 2100)]
    fl(d, (190, 150, 90, 255)); im.alpha_composite(d.out()); CE.glow(im, 1700, 600, 300, (255, 230, 160, 100), 60); im.convert('RGB').save(path)


def splitroad(path):                                         # sky-blue split road: left sepia past, right bright present, a road to the horizon
    im = M.sky((120, 190, 250), (230, 246, 255), 1.0); d = Draw(W2, H2); d.rect(0, 0, 1200, H2, (240, 210, 160, 120))
    hills(d, 760, (150, 200, 140, 255), 50, 2); d.poly([(1100, 760), (1300, 760), (1700, 940), (700, 940)], fill=(90, 90, 110, 255)); d.stroke([(1200, 770), (1200, 940)], WT, 10)
    fl(d, (160, 170, 160, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast5(('willy', 'mom', 'eno', 'cop'))
    def slap(lines, tilt): return stopper(lines, face=RUBY, side=(130, 10, 30, 255), plate=(255, 250, 236, 255), rim=(255, 196, 40, 255), h=470, tilt=tilt)
    multi = dict(stop={'default': slap(['STOP SIGN', 'INVENTOR'], -4), 'esc': slap(['NEVER DROVE', 'A CAR?!'], -4), 'wait': slap(['HOW?!', 'WAIT FOR IT'], -4)},
                 stopsign={'default': stopsign(), 'shocked': stopsign('shocked'), 'wink': stopsign('wink')}, car={'default': car(), 'x': car('x')},
                 horse={'default': horse(), 'shocked': horse('shocked')}, carriage={'default': carriage(), 'shocked': carriage('shocked')}, jam={'default': jam()}, article={'default': article()},
                 regs={'default': regs()}, oneway={'default': oneway()}, circle={'default': circle()}, trophy={'default': trophy()}, found={'default': foundation()}, wheel={'default': wheel(), 'x': wheel('x')})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ = (100, 50, 150, 255), (20, 120, 130, 255)
    cards = dict(y1867=M.cal('NEW YORK', '1867', COB), age9=stamp('AGE 9', 620, COB, 140, -3), notcars=stamp('NOT CARS!', 760, RUBY, 130, 3), nobody=stamp('NOBODY KNOWS HOW', 920, PU, 106, -3),
                 y1900=M.cal('ARTICLE', '1900', RUBY), rulesc=stamp('REAL TRAFFIC RULES!', 960, RUBY, 100, 3), firstc=P_("NEW YORK'S FIRST", 'WRITTEN REGULATIONS', COB, 980, 96, 96, YEL),
                 father=P_('FATHER OF', 'TRAFFIC SAFETY', RUBY, 900, 120, 110, YEL), y1921=M.cal('FOUNDED', '1921', TQ), today=stamp('STILL STUDYING TODAY', 960, TQ, 100, -3),
                 horsem=stamp('A HORSEMAN!', 780, (150, 90, 40, 255), 124, 3), carri=stamp('WRITTEN FOR CARRIAGES', 980, PU, 96, -3), inherit=M.bigneon('CARS SIMPLY', 'INHERITED THEM', 860, YEL, (255, 130, 160, 255)),
                 neverd=stamp('HE NEVER DROVE', 900, RUBY, 110, 3), nineyo=stamp('NINE YEARS OLD', 880, COB, 110, -3))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    CE.tiles(T('asphalt.jpg'), (100, 96, 120), (90, 86, 110)); CE.tiles(T('cobble2.jpg'), (160, 130, 110), (146, 118, 100)); CE.tiles(T('mintfl.jpg'), (140, 170, 150), (128, 156, 138)); CE.tiles(T('marblefl.jpg'), (230, 220, 200), (216, 206, 186))
    CE.tiles(T('candyfl.jpg'), (220, 200, 230), (206, 186, 216)); M.sandtex(T('lilacfl.jpg'), (180, 170, 200), (166, 156, 186)); M.sandtex(T('hayfl.jpg'), (220, 180, 110), (206, 166, 98)); CE.tiles(T('roadfl.jpg'), (150, 160, 170), (136, 146, 156))
    CE.tiles(T('pave.jpg'), (110, 100, 130), (98, 88, 118)); B.tex_wood(T('wood.jpg'))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(dusk=dusk, broadway=broadway, study=study, marble=marble, candy=candy, campus=campus, stable=stable, splitroad=splitroad)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
