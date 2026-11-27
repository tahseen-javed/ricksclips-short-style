#!/usr/bin/env python3
"""Assets for video 33: the world's oldest light bulb (Livermore Fire Station 6, glowing since 1901, handmade carbon bulb from Ohio in the
1890s, two world wars and a move across town; May 2013 the webcam went dark, but a faulty power supply was to blame; ten hours later it
glowed again; built for 60 W, now gives about 4; the machine failed first). Firehouse-nocturne world (new palette): midnight-teal fire
station night (hook + loop), amber 1890s Ohio glassworks, olive-khaki war-years sky, mint-lilac toy town, violet 2013 webcam room, cyan
x-ray blueprint, coral ten-hours dawn, lemon-mint watt workshop. Accent filament orange #ff8c1a. Cute cast (new, companions only): Fire
Captain Rosa (red fire helmet with a 6 shield, tan turnout coat) and electrician Dev (orange bolt cap, teal coverall, tool belt). The bulb
with a face is the star. usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v33_assets import *

ROOT = B.ROOT
TEALN, AMB, OLV, MNT, LIL, VIO, CYN, CORL, LEM, FRED, CRM, ORG = (20, 90, 110, 255), (255, 170, 60, 255), (150, 150, 80, 255), (150, 230, 200, 255), (200, 170, 240, 255), (110, 60, 170, 255), (60, 200, 230, 255), (255, 120, 110, 255), (250, 240, 110, 255), (220, 50, 50, 255), (252, 246, 232, 255), (255, 140, 26, 255)
LA.NEW.update({
    'rosa': dict(sk=2, style='curly', hair=(60, 30, 30, 255), suit=(214, 170, 90, 255), shade=(186, 142, 70, 255), body='turnout', acc=FRED, xhat='firehelm', hatc=FRED, num='6'),
    'dev': dict(sk=1, style='side', hair=(30, 30, 40, 255), suit=(40, 150, 160, 255), shade=(30, 120, 130, 255), body='coverall', acc=ORG, xhat='boltcap', hatc=ORG, freckles=1),
})


def bulb(face='default'):                                    # the Centennial bulb: pear glass, thick looped filament, brass base, a face
    lit = face not in ('dark',); W_, H_ = 1000, 1300; im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    if lit: CE.glow(im, 500, 520, 470 if face == 'bright' else 400, (255, 190, 80, 170 if face != 'sleepy' else 110), 70)
    d = Draw(W_, H_); glass = (255, 236, 170, 235) if lit else (190, 196, 210, 235)
    d.dot(500, 500, 330, glass); d.poly([(260, 700), (740, 700), (640, 960), (360, 960)], fill=glass); d.ellipse(500, 500, 330, 330, outline=LINE, width=16)
    d.stroke([(250, 720), (360, 960)], LINE, 16); d.stroke([(750, 720), (640, 960)], LINE, 16)
    fc = (255, 120, 30, 255) if lit else (110, 100, 100, 255); d.stroke([(440, 960), (440, 760), (400, 690), (500, 640), (600, 690), (560, 760), (560, 960)], fc, 24)
    for y in (980, 1050, 1120): d.rrect(350, y, 650, y + 64, 26, fill=(210, 170, 90, 255), outline=LINE, width=10)
    d.chord(500, 1190, 90, 70, 0, 180, fill=(80, 60, 50, 255), outline=LINE, width=10); d.ellipse(380, 360, 60, 110, fill=(255, 255, 255, 150))
    eyes5(d, 500, 430, 1.35, {'default': 'happy', 'bright': 'happy', 'dark': 'sad'}.get(face, face))
    if face == 'bright': [d.stroke([(500 + 380 * math.cos(a), 500 + 380 * math.sin(a)), (500 + 460 * math.cos(a), 500 + 460 * math.sin(a))], YEL, 16) for a in np.linspace(3.4, 6.0, 5)]
    if face == 'sleepy': [d.text(780 + k * 70, 200 - k * 70, 'z', 70 + k * 20, WT, stroke=5, stroke_fill=LINE) for k in range(3)]
    im.alpha_composite(d.out()); return im


def firehouse():                                             # Fire Station 6: red brick, arched doors, a glowing bulb in the window, cute face
    d = Draw(1500, 1200); d.rect(150, 330, 1350, 1160, (200, 70, 60, 255)); d.rrect(150, 330, 1350, 1160, 2, outline=LINE, width=14)
    for y in range(380, 1150, 70): d.stroke([(150, y), (1350, y)], (170, 56, 50, 255), 5)
    d.poly([(110, 340), (750, 120), (1390, 340)], fill=(90, 60, 70, 255), outline=LINE, width=14); d.rrect(380, 190, 1120, 330, 26, fill=CRM, outline=LINE, width=12); d.text(750, 262, 'FIRE STATION 6', 66, FRED)
    for x in (260, 800): d.chord(x + 220, 1160, 200, 300, 180, 360, fill=(240, 226, 200, 255), outline=LINE, width=12); [d.stroke([(x + 40 + k * 90, 900), (x + 40 + k * 90, 1160)], (200, 186, 160, 255), 6) for k in range(5)]
    d.dot(750, 560, 120, (255, 200, 90, 255)); d.ellipse(750, 560, 120, 120, outline=LINE, width=10); d.dot(750, 560, 40, (255, 250, 200, 255)); eyes(d, 750, 760, 0.6, 'happy'); return d.out()


def kiln():                                                  # 1890s Ohio glassworks: brick furnace with an orange mouth, a blowpipe with a baby bulb
    im = Image.new('RGBA', (1400, 1200), (0, 0, 0, 0)); CE.glow(im, 600, 760, 260, (255, 150, 40, 170), 50); d = Draw(1400, 1200)
    d.chord(600, 1150, 460, 720, 180, 360, fill=(170, 90, 60, 255), outline=LINE, width=14); d.rect(560, 120, 640, 450, (140, 80, 60, 255)); d.chord(600, 900, 180, 160, 180, 360, fill=(255, 170, 50, 255), outline=LINE, width=12)
    d.stroke([(700, 820), (1280, 560)], (120, 120, 130, 255), 18); d.dot(1240, 560, 90, (255, 236, 170, 230)); d.ellipse(1240, 560, 90, 90, outline=LINE, width=10); eyes(d, 1240, 560, 0.35, 'happy')
    eyes(d, 600, 640, 0.6, 'happy'); im.alpha_composite(d.out()); return im


def wars():                                                  # two world wars, cute: a brave globe in a tin helmet, two toy biplanes circling, x2 medal
    d = Draw(1300, 1200); d.dot(650, 680, 420, (90, 170, 240, 255)); [d.ellipse(650 + dx, 680 + dy, rx, ry, fill=(130, 190, 110, 255)) for dx, dy, rx, ry in ((-140, -100, 140, 100), (160, 60, 120, 150), (-40, 220, 110, 60))]
    d.ellipse(650, 680, 420, 420, outline=LINE, width=14); d.chord(650, 330, 300, 120, 180, 360, fill=OLV, outline=LINE, width=12); eyes(d, 650, 700, 0.8, 'shocked')
    for x, y, c in ((180, 230, CORL), (1080, 300, YEL)): d.rrect(x - 110, y - 22, x + 110, y + 22, 18, fill=c, outline=LINE, width=8); d.rrect(x - 30, y - 70, x + 30, y + 70, 12, fill=c, outline=LINE, width=8); d.dot(x + 120, y, 16, LINE)
    d.dot(1100, 1000, 120, AMB); d.ellipse(1100, 1000, 120, 120, outline=LINE, width=10); d.text(1100, 1000, 'x2', 110, WT, stroke=6, stroke_fill=LINE); return d.out()


def truck():                                                 # the move across town: a cute fire truck carrying the bulb on a velvet cushion
    im = Image.new('RGBA', (1600, 1000), (0, 0, 0, 0)); CE.glow(im, 820, 300, 200, (255, 200, 90, 150), 40); d = Draw(1600, 1000)
    d.rrect(120, 420, 1480, 820, 60, fill=FRED, outline=LINE, width=14); d.rrect(1080, 300, 1440, 600, 40, fill=FRED, outline=LINE, width=14); d.rrect(1140, 340, 1400, 500, 20, fill=(170, 220, 250, 255), outline=LINE, width=10)
    d.stroke([(160, 400), (1000, 360)], (230, 230, 230, 255), 16); [d.stroke([(160 + k * 120, 400 - k * 5), (160 + k * 120, 440)], (230, 230, 230, 255), 10) for k in range(8)]
    d.rrect(620, 340, 1020, 440, 40, fill=(150, 40, 90, 255), outline=LINE, width=10); d.dot(820, 250, 110, (255, 236, 170, 240)); d.ellipse(820, 250, 110, 110, outline=LINE, width=10); d.rrect(780, 350, 860, 380, 8, fill=(210, 170, 90, 255))
    eyes(d, 820, 250, 0.4, 'happy'); [d.dot(x, 840, 110, (50, 50, 60, 255)) for x in (380, 1220)]; [d.dot(x, 840, 50, (200, 200, 210, 255)) for x in (380, 1220)]; eyes(d, 600, 620, 0.6, 'happy'); return d.out()


def cam(mode='live'):                                        # the 2013 live webcam and its monitor (live: the glowing bulb; dark: black screen and a "?")
    d = Draw(1400, 1200); d.rrect(100, 120, 1300, 860, 40, fill=(60, 60, 80, 255), outline=LINE, width=16); d.rrect(150, 170, 1250, 810, 24, fill=(20, 22, 34, 255) if mode == 'dark' else (40, 60, 90, 255))
    if mode == 'live': d.dot(700, 450, 170, (255, 220, 120, 255)); d.dot(700, 450, 70, (255, 250, 220, 255))
    else: d.text(700, 490, '?', 300, (120, 110, 150, 255), stroke=8, stroke_fill=LINE)
    d.rrect(190, 210, 420, 290, 20, fill=(230, 40, 60, 255) if mode == 'live' else (80, 80, 90, 255)); d.text(305, 252, 'LIVE', 60, WT); d.rect(620, 860, 780, 1000, (60, 60, 80, 255)); d.rrect(460, 990, 940, 1060, 20, fill=(60, 60, 80, 255), outline=LINE, width=10)
    d.dot(1180, 1000, 90, (230, 230, 240, 255)); d.ellipse(1180, 1000, 90, 90, outline=LINE, width=10); d.dot(1180, 1000, 40, (40, 60, 120, 255)); eyes(d, 700, 940, 0.35, 'happy' if mode == 'live' else 'shocked'); return d.out()


def psu(mode='ok'):                                          # the power supply box (broken: dizzy eyes, smoke puff, sparks - cute, no damage)
    d = Draw(1200, 1100); d.rrect(200, 320, 1000, 980, 50, fill=(150, 160, 180, 255), outline=LINE, width=16); [d.rect(280, y, 520, y + 20, (110, 120, 140, 255)) for y in range(420, 640, 50)]
    d.stroke([(1000, 700), (1120, 700), (1140, 900)], LINE, 18); d.rrect(640, 400, 920, 520, 20, fill=(40, 40, 60, 255)); d.text(780, 460, '~', 90, (120, 255, 160, 255) if mode == 'ok' else (255, 90, 90, 255))
    eyes5(d, 600, 760, 0.8, 'happy' if mode == 'ok' else 'dizzy')
    if mode == 'broken':
        for x, y, r in ((420, 220, 90), (560, 160, 110), (720, 220, 90)): d.dot(x, y, r, (200, 200, 210, 230))
        for x, y in ((180, 300), (1040, 280), (1080, 520)): d.text(x, y, '*', 120, YEL, stroke=5, stroke_fill=LINE)
    return d.out()


def clock():                                                 # alarm clock with a glowing 10-hour arc
    d = Draw(1100, 1200); [d.dot(x, 200, 110, (255, 214, 60, 255)) for x in (270, 830)]; [d.ellipse(x, 200, 110, 110, outline=LINE, width=12) for x in (270, 830)]
    d.dot(550, 640, 420, (255, 250, 240, 255)); d.ellipse(550, 640, 420, 420, outline=CORL, width=40); d.ellipse(550, 640, 440, 440, outline=LINE, width=12)
    d.arc(550, 640, 330, 330, -90, 210, (255, 140, 26, 230), 60); d.stroke([(550, 640), (550, 380)], LINE, 22); d.stroke([(550, 640), (380, 700)], LINE, 26); d.dot(550, 640, 26, LINE)
    eyes(d, 550, 820, 0.55, 'happy'); [d.dot(x, 1100, 50, LINE) for x in (300, 800)]; return d.out()


def meter(mode='60'):                                        # watt gauge: needle at 60 (built for) or near 4 (now), cute face
    d = Draw(1300, 1000); d.chord(650, 760, 560, 560, 180, 360, fill=CRM, outline=LINE, width=16); d.rect(90, 760, 1210, 900, (60, 70, 90, 255)); d.rrect(90, 740, 1210, 920, 30, outline=LINE, width=14)
    for k in range(7): a = math.radians(180 + k * 30); d.stroke([(650 + 470 * math.cos(a), 760 + 470 * math.sin(a)), (650 + 530 * math.cos(a), 760 + 530 * math.sin(a))], LINE, 12); d.text(650 + 400 * math.cos(a), 760 + 400 * math.sin(a), str(k * 10), 60, LINE)
    a = math.radians(180 + (180 if mode == '60' else 12)); col = FRED if mode == '60' else (40, 170, 110, 255); d.stroke([(650, 760), (650 + 440 * math.cos(a), 760 + 440 * math.sin(a))], col, 26); d.dot(650, 760, 44, LINE)
    d.text(650, 600, '60 W' if mode == '60' else '4 W', 130, col, stroke=7, stroke_fill=LINE); eyes(d, 650, 830, 0.4, 'shocked' if mode == '60' else 'happy'); return d.out()


def fil():                                                   # macro: the thick carbon filament glowing inside the glass
    im = Image.new('RGBA', (1300, 1300), (0, 0, 0, 0)); CE.glow(im, 650, 650, 560, (255, 170, 60, 160), 90); d = Draw(1300, 1300)
    d.dot(650, 650, 600, (255, 230, 170, 120)); d.ellipse(650, 650, 600, 600, outline=(255, 250, 230, 200), width=20)
    pts = [(420, 1250), (420, 760)] + [(650 + 260 * math.cos(t), 540 + 200 * math.sin(t)) for t in np.linspace(math.pi * 0.9, math.pi * 2.1, 18)] + [(880, 760), (880, 1250)]
    d.stroke(pts, (255, 120, 30, 255), 70); d.stroke(pts, (255, 220, 120, 255), 26); eyes5(d, 650, 860, 0.7, 'sleepy'); return d.out()


def switch():                                                # giant wall switch stuck on ON with crossed tape
    d = Draw(900, 1300); d.rrect(100, 80, 800, 1220, 60, fill=CRM, outline=LINE, width=16); d.rrect(330, 300, 570, 1000, 50, fill=(220, 214, 200, 255), outline=LINE, width=12)
    d.rrect(350, 320, 550, 640, 40, fill=(255, 140, 26, 255), outline=LINE, width=10); d.text(450, 480, 'ON', 110, WT, stroke=6, stroke_fill=LINE)
    for y in (290, 690): d.stroke([(200, y), (700, y + 20)], (240, 220, 160, 235), 70)
    eyes(d, 450, 840, 0.5, 'happy'); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def night6(path):                                            # midnight-teal night over Livermore: stars, moon, rooftops with warm windows, a hose tower
    im = M.sky((20, 70, 100), (60, 150, 160), 1.0); d = Draw(W2, H2); M.stars(d, 120, 560, 7); d.dot(1950, 190, 90, (255, 246, 210, 255))
    for k in range(12): x = k * 210; h = 180 + (k * 53) % 140; d.rect(x, 900 - h, x + 180, 940, (30, 60, 80, 255)); [d.rect(x + 30 + j * 60, 900 - h + 40, x + 60 + j * 60, 900 - h + 80, (255, 200, 110, 255)) for j in range(2)]
    d.rect(300, 300, 400, 940, (150, 50, 50, 255)); fl(d, (40, 80, 90, 255)); im.alpha_composite(d.out()); CE.glow(im, 1950, 190, 220, (255, 240, 200, 90), 60); im.convert('RGB').save(path)


def glassw(path):                                            # amber 1890s glassworks: brick arches, glowing furnace mouths, chimneys
    im = M.sky((150, 70, 40), (255, 180, 90), 1.0); d = Draw(W2, H2); [d.rect(x, 100, x + 90, 600, (120, 60, 40, 255)) for x in (300, 1900)]
    for x in range(0, W2, 480): d.chord(x + 240, 940, 200, 380, 180, 360, fill=(110, 50, 40, 255)); d.chord(x + 240, 940, 100, 140, 180, 360, fill=(255, 170, 60, 255))
    fl(d, (130, 70, 50, 255)); im.alpha_composite(d.out()); [CE.glow(im, x + 240, 880, 160, (255, 170, 60, 110), 40) for x in range(0, W2, 480)]; im.convert('RGB').save(path)


def warsky(path):                                            # olive-khaki war-years sky: puffy sepia clouds, bunting, far hills
    im = M.sky((150, 160, 110), (240, 220, 170), 1.0); d = Draw(W2, H2)
    for x, y in ((300, 200), (1200, 140), (2000, 240)): [d.dot(x + k * 110, y + (k % 2) * 30, 90, (250, 240, 220, 230)) for k in range(4)]
    hills(d, 760, (120, 130, 80, 255), 70, 3); d.stroke([(0, 360), (600, 420), (1200, 360), (1800, 420), (W2, 360)], LINE, 6)
    for k in range(24): x = k * 100 + 20; y = 380 + 30 * math.sin(k * 0.52); d.poly([(x, y), (x + 60, y), (x + 30, y + 60)], fill=(CORL, YEL, (120, 200, 230, 255))[k % 3])
    fl(d, (150, 140, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def town(path):                                              # mint-lilac toy town: pastel hills, little houses, a winding road
    im = M.sky((200, 180, 250), (220, 250, 235), 1.0); d = Draw(W2, H2); hills(d, 600, (170, 230, 200, 255), 100, 2); hills(d, 760, (150, 210, 180, 255), 60, 3, 1.1)
    for k in range(10): x, y = 120 + k * 230, 660 + (k % 3) * 50; d.rect(x, y, x + 100, y + 70, (255, 246, 236, 255)); d.poly([(x - 10, y), (x + 50, y - 50), (x + 110, y)], fill=(LIL, CORL, (120, 200, 230, 255))[k % 3])
    d.stroke([(0, 900), (700, 820), (1400, 900), (W2, 820)], (240, 230, 250, 255), 26); fl(d, (170, 190, 170, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def room13(path):                                            # violet 2013 room: shelves, a window with the city, a blue screen glow
    im = M.sky((90, 50, 150), (170, 110, 210), 1.0); d = Draw(W2, H2); d.rrect(1500, 150, 2150, 650, 20, fill=(40, 40, 110, 255), outline=(220, 190, 250, 255), width=16)
    M.stars(d, 30, 600, 5); [d.rect(x, 260, x + 300, 280, (200, 160, 230, 255)) for x in (200, 650)]; [d.rect(x + 20 * k, 200, x + 20 * k + 14, 260, (CORL, YEL, CYN)[k % 3]) for x in (220, 680) for k in range(8)]
    fl(d, (90, 70, 130, 255)); im.alpha_composite(d.out()); CE.glow(im, 1200, 600, 400, (120, 160, 255, 70), 80); im.convert('RGB').save(path)


def xray(path):                                              # cyan x-ray blueprint: grid, circuit traces with dots
    im = M.sky((20, 110, 150), (60, 190, 210), 1.0); d = Draw(W2, H2); [d.stroke([(x, 0), (x, H2)], (150, 230, 250, 90), 3) for x in range(0, W2, 80)]; [d.stroke([(0, y), (W2, y)], (150, 230, 250, 90), 3) for y in range(0, H2, 80)]
    for k in range(9): y = 120 + k * 90; d.stroke([(0, y), (500 + k * 60, y), (560 + k * 60, y + 60), (W2, y + 60)], (200, 250, 255, 150), 6); d.dot(500 + k * 60, y, 12, YEL)
    fl(d, (30, 100, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def dawn(path):                                              # coral ten-hours dawn: sun rising behind soft hills, pink clouds
    im = M.sky((255, 130, 120), (255, 220, 170), 1.0); d = Draw(W2, H2); d.dot(1200, 700, 240, (255, 240, 180, 255))
    for x, y in ((400, 220), (1700, 180)): [d.dot(x + k * 110, y + (k % 2) * 30, 80, (255, 200, 210, 230)) for k in range(4)]
    hills(d, 700, (240, 140, 130, 255), 80, 2); fl(d, (200, 120, 110, 255)); im.alpha_composite(d.out()); CE.glow(im, 1200, 700, 400, (255, 230, 160, 110), 80); im.convert('RGB').save(path)


def workshop(path):                                          # lemon-mint watt workshop: pegboard, tool shapes, shelf with jars
    im = M.sky((230, 240, 140), (180, 240, 210), 1.0); d = Draw(W2, H2); d.rrect(300, 120, 2100, 760, 20, fill=(220, 200, 150, 255), outline=(150, 130, 90, 255), width=14)
    for x in range(360, 2080, 70):
        for y in range(170, 740, 70): d.dot(x, y, 8, (170, 150, 100, 255))
    for x, c in ((600, CORL), (1000, (120, 200, 230, 255)), (1500, VIO), (1850, ORG)): d.rrect(x - 40, 260, x + 40, 560, 20, fill=c, outline=LINE, width=8)
    fl(d, (150, 170, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast5(('rosa', 'dev'))
    SP = dict(face=ORG, side=(170, 70, 10, 255), plate=(20, 40, 60, 255), rim=(60, 220, 230, 255), h=470)
    multi = dict(bulb={'default': bulb(), 'dark': bulb('dark'), 'shocked': bulb('shocked'), 'sleepy': bulb('sleepy'), 'bright': bulb('bright'), 'wink': bulb('wink')},
                 stop={'default': stopper(['ON SINCE 1901'], **SP), 'off': stopper(['ON SINCE 1901'], lit=False, **SP), 'esc': stopper(['ON SINCE 1901', 'NEVER DIED?!'], **SP),
                       'wait': stopper(["WHAT'S ITS", 'SECRET?'], **SP)},
                 fireh={'default': firehouse()}, kiln={'default': kiln()}, wars={'default': wars()}, truck={'default': truck()}, cam={'default': cam(), 'dark': cam('dark')},
                 psu={'default': psu(), 'broken': psu('broken')}, clock={'default': clock()}, meter={'default': meter(), 'four': meter('4')}, fil={'default': fil()}, switch={'default': switch()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    TQ, RB, PU = (20, 120, 130, 255), (200, 40, 50, 255), (100, 50, 150, 255)
    cards = dict(livc=P_('LIVERMORE,', 'CALIFORNIA', TQ, 900, 110, 120, YEL), y1890=M.cal('OHIO', '1890s', (210, 110, 40, 255)), handc=stamp('HANDMADE CARBON BULB', 980, (180, 80, 40, 255), 96, -3),
                 warsc=M.bigneon('TWO WORLD', 'WARS', 760, YEL, CORL), movec=stamp('A MOVE ACROSS TOWN', 960, PU, 100, 3), y2013=M.cal('MAY', '2013', VIO),
                 deadc=stamp('OLDEST BULB: DEAD?!', 960, RB, 104, -3), wasnt=stamp("IT WASN'T!", 760, (30, 150, 110, 255), 130, 3), psuc=P_('FAULTY', 'POWER SUPPLY', RB, 900, 110, 120, YEL),
                 finec=stamp('THE BULB WAS FINE', 940, (30, 150, 110, 255), 104, -3), triesc=stamp('IT BARELY TRIES', 900, ORG, 110, 3), wattc=M.bigneon('BUILT: 60 W', 'NOW: ABOUT 4', 820, YEL, (120, 255, 160, 255)),
                 filc=P_('THICK', 'FILAMENT', (180, 80, 30, 255), 760, 120, 130, YEL), offc=stamp('ALMOST NEVER OFF', 900, TQ, 108, -3), failc=stamp('THE MACHINE FAILED FIRST', 1000, RB, 96, 3),
                 didnt=stamp("THE BULB DIDN'T!", 900, (30, 150, 110, 255), 112, -3))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('nightfl.jpg'), (50, 90, 100), (44, 80, 90)); CE.tiles(T('brickfl.jpg'), (150, 80, 60), (136, 70, 52)); M.sandtex(T('khakifl.jpg'), (160, 150, 110), (146, 136, 98)); M.sandtex(T('townfl.jpg'), (180, 210, 190), (166, 196, 176))
    CE.tiles(T('violetfl.jpg'), (120, 90, 160), (108, 80, 146)); CE.tiles(T('bluefl.jpg'), (50, 130, 160), (44, 118, 146)); M.sandtex(T('coralfl.jpg'), (220, 140, 120), (206, 128, 110)); CE.tiles(T('lemonfl.jpg'), (190, 200, 140), (176, 186, 128))
    CE.tiles(T('pave.jpg'), (60, 90, 100), (52, 80, 90)); B.tex_wood(T('wood.jpg'))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(night6=night6, glassw=glassw, warsky=warsky, town=town, room13=room13, xray=xray, dawn=dawn, workshop=workshop)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
