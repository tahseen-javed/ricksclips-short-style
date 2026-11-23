#!/usr/bin/env python3
"""Assets for video 19: the Eiffel Tower was built to be torn down; a wire on top saved it; then it caught a spy.
Paris lavender-dusk + champagne-gold + spy-noir world: cute cast (Eiffel with beard + bowler, two beret artists, a demolition boss,
a soldier, a radio man with headphones, Mata Hari), the tower as a hero with faces, twelve painted sets, plaques.
usage: make_assets.py <project> <font>"""
import os, math, json
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import lordgta_assets as LA
import mco_assets as M
import mono_assets as MA
import pd_assets as PD
from assets_base import Draw, LINE, WHITE, H

ROOT = B.ROOT; GOLDL = M.GOLDL
dk, glow, plaque, stamp, sky, W2, H2, fl = LA.dk, CE.glow, LA.plaque, LA.stamp, M.sky, M.W2, M.H2, MA.fl
eyes, shine, win = PD.eyes, PD.shine, PD.win
WT, PINK, CYAN, YEL, ORNG, TEAL, NAVY, RED, VIO = (250, 250, 245, 255), (255, 110, 170, 255), (80, 230, 255, 255), (255, 214, 60, 255), (255, 140, 40, 255), (30, 150, 150, 255), (30, 40, 100, 255), (220, 40, 60, 255), (150, 100, 220, 255)
IRON, IRONL, GOLD2, LAV = (150, 90, 70, 255), (190, 120, 90, 255), (240, 190, 90, 255), (190, 160, 230, 255)
LA.NEW.update({
    'eiffel': dict(sk=0, style='side', hair=(120, 90, 70, 255), suit=(60, 50, 80, 255), shade=(44, 36, 62, 255), body='suit', tie=RED, stache=(120, 90, 70, 255), hat='bowler', beard=(120, 90, 70, 255)),
    'artist': dict(sk=0, style='curly', hair=(60, 40, 30, 255), suit=(200, 60, 70, 255), shade=(170, 44, 56, 255), body='sweater', stache=(60, 40, 30, 255), xhat='beret'),
    'artist2': dict(sk=1, style='bob', hair=(200, 120, 60, 255), suit=(90, 70, 160, 255), shade=(70, 52, 136, 255), body='cardigan', band=YEL, xhat='beret2'),
    'boss': dict(sk=2, style='curly', hair=(30, 24, 24, 255), suit=ORNG, shade=(220, 110, 30, 255), body='denim', xhat='hard'),
    'soldier': dict(sk=0, style='side', hair=(90, 60, 40, 255), suit=(110, 140, 200, 255), shade=(86, 114, 170, 255), body='suit', tie=RED, xhat='kepi'),
    'radioman': dict(sk=1, style='spiky', hair=(40, 30, 30, 255), suit=(170, 130, 80, 255), shade=(140, 104, 60, 255), body='sweater', freck=1, xhat='phones'),
    'mata': dict(sk=1, style='bob', hair=(30, 22, 30, 255), suit=(120, 30, 60, 255), shade=(96, 20, 46, 255), body='cardigan', band=GOLD2, xhat='feather'),
})


def head(char, expr):
    im = MA.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']; x = c.get('xhat')
    if c.get('beard'): d.chord(cx, cy + 150, R - 40, 120, 0, 180, fill=c['beard'], outline=LINE, width=12)
    if x in ('beret', 'beret2'):
        col = (40, 40, 60, 255) if x == 'beret' else (220, 60, 90, 255); d.ellipse(cx - 20, cy - R + 40, R + 30, 70, fill=col, outline=LINE, width=14); d.dot(cx - 20, cy - R - 30, 16, col)
    elif x == 'hard':
        d.chord(cx, cy - R + 90, R + 10, R - 20, 180, 360, fill=YEL, outline=LINE, width=14); d.ellipse(cx, cy - R + 90, R + 50, 26, fill=YEL, outline=LINE, width=12); d.rect(cx - 16, cy - R - 10, cx + 16, cy - R + 80, (255, 236, 140, 255))
    elif x == 'kepi':
        d.rrect(cx - R + 40, cy - R - 60, cx + R - 40, cy - R + 70, 20, fill=RED, outline=LINE, width=14); d.rect(cx - R + 44, cy - R + 30, cx + R - 44, cy - R + 66, NAVY); d.ellipse(cx + 40, cy - R + 74, R - 40, 22, fill=LINE)
    elif x == 'phones':
        d.arc(cx, cy - 20, R + 20, R + 10, 180, 360, LINE, 22)
        for sg in (-1, 1): d.rrect(cx + sg * (R + 10) - 40, cy - 70, cx + sg * (R + 10) + 40, cy + 50, 26, fill=(80, 80, 90, 255), outline=LINE, width=12)
    elif x == 'feather':
        d.ellipse(cx + 10, cy - R + 50, R + 50, 40, fill=(40, 30, 50, 255), outline=LINE, width=14); d.chord(cx + 10, cy - R + 46, R - 40, R - 30, 180, 360, fill=(40, 30, 50, 255), outline=LINE, width=14)
        d.poly([(cx + 90, cy - R - 10), (cx + 260, cy - R - 200), (cx + 200, cy - R - 20)], fill=(255, 120, 170, 255), outline=LINE, width=10)
    im.alpha_composite(d.out()); return im


def tower(face='default', h=1600):                           # cute Eiffel Tower: iron lattice, three decks, gold lights, a face on the first deck
    W = 900; d = Draw(W, h); cx = W / 2
    leg = lambda y: 70 + 370 * (y / h) ** 2.2
    d.poly([(cx, 60), (cx + leg(h * 0.4) * 0.5, h * 0.4), (cx + leg(h) * 1.0, h - 20), (cx + 140, h - 20), (cx + 40, h * 0.66), (cx - 40, h * 0.66), (cx - 140, h - 20), (cx - leg(h) * 1.0, h - 20), (cx - leg(h * 0.4) * 0.5, h * 0.4)], fill=IRON, outline=LINE, width=16)
    d.chord(cx, h - 20, 150, 200, 180, 360, fill=(70, 50, 80, 255))
    for k in range(14):
        y = 160 + k * (h - 260) / 14; w = leg(y) * 0.8; d.stroke([(cx - w, y), (cx + w * 0.7, y + 60)], IRONL, 8); d.stroke([(cx + w, y), (cx - w * 0.7, y + 60)], IRONL, 8)
    for y in (h * 0.4, h * 0.66): w = leg(y) * 0.6 + 40; d.rrect(cx - w, y - 26, cx + w, y + 26, 10, fill=(120, 70, 60, 255), outline=LINE, width=12); [d.dot(cx - w + 30 + i * (2 * w - 60) / 6, y, 9, YEL) for i in range(7)]
    d.stroke([(cx, 60), (cx, 0)], LINE, 14)
    if face == 'wire': [d.arc(cx, 20, 60 + 50 * i, 40 + 30 * i, 200, 340, CYAN, 10) for i in range(3)]
    if face == 'ear': d.ellipse(cx + 170, h * 0.52, 120, 170, fill=(255, 190, 170, 255), outline=LINE, width=14); d.arc(cx + 170, h * 0.52, 60, 100, 100, 300, (200, 120, 110, 255), 14)
    eyes(d, cx, h * 0.52, 0.85, {'default': 'happy', 'wire': 'happy', 'ear': 'happy'}.get(face, face)); return d.out()


def towertop():                                              # the very top: little iron cap, flag pole, the antenna wire singing radio rings
    d = Draw(1000, 1300); cx = 500
    d.poly([(cx - 60, 200), (cx + 60, 200), (cx + 260, 1280), (cx - 260, 1280)], fill=IRON, outline=LINE, width=16)
    for y in range(300, 1280, 120): d.stroke([(cx - 60 - (y - 200) * 0.18, y), (cx + 60 + (y - 260) * 0.18, y + 80)], IRONL, 8)
    d.rrect(cx - 130, 180, cx + 130, 260, 16, fill=(120, 70, 60, 255), outline=LINE, width=12); d.stroke([(cx, 180), (cx, 40)], LINE, 16)
    d.stroke([(cx, 50), (cx + 380, 160)], (60, 60, 70, 255), 8); d.stroke([(cx, 50), (cx - 380, 160)], (60, 60, 70, 255), 8)
    for i in range(3): d.arc(cx, 50, 90 + 70 * i, 60 + 46 * i, 200, 340, CYAN, 12)
    d.dot(cx, 40, 26, YEL); eyes(d, cx, 700, 0.8, 'happy'); return d.out()


def ball():                                                  # wrecking ball on a chain, angry brows
    d = Draw(600, 900); d.stroke([(300, 0), (300, 420)], (90, 90, 100, 255), 24)
    for y in range(20, 420, 50): d.ellipse(300, y, 16, 26, outline=LINE, width=8)
    d.dot(300, 640, 240, (80, 80, 96, 255)); d.ellipse(300, 640, 240, 240, outline=LINE, width=16); d.ellipse(220, 560, 60, 40, fill=(140, 140, 160, 255))
    for sg in (-1, 1): d.stroke([(300 + sg * 40, 600), (300 + sg * 120, 580)], LINE, 14)
    d.arc(300, 720, 50, 26, 200, 340, LINE, 12); return d.out()


def permit(renewed=False):                                   # the permit: parchment, wax seal, a giant "20" (or "20" crossed + "+70")
    d = Draw(760, 980); d.rrect(30, 30, 730, 950, 24, fill=(250, 240, 210, 255), outline=LINE, width=16)
    for y in range(110, 300, 50): d.rect(90, y, 670, y + 14, (190, 176, 150, 255))
    d.text(380, 560, '20', 300, (120, 60, 50, 255), stroke=10, stroke_fill=LINE)
    if renewed: d.stroke([(150, 440), (610, 680)], RED, 30); d.rrect(300, 680, 720, 900, 30, fill=(60, 170, 100, 255), outline=LINE, width=14); d.text(510, 790, '+70', 160, WT, stroke=8, stroke_fill=LINE)
    else: d.dot(590, 820, 80, RED)
    return d.out()


def easel():                                                 # easel with an angry painting of the tower crossed out
    d = Draw(800, 1200); d.stroke([(400, 80), (160, 1180)], (150, 100, 60, 255), 26); d.stroke([(400, 80), (640, 1180)], (150, 100, 60, 255), 26)
    d.rrect(120, 200, 680, 760, 16, fill=(250, 246, 236, 255), outline=LINE, width=14); d.poly([(400, 260), (520, 720), (280, 720)], fill=IRON, outline=LINE, width=8)
    d.stroke([(170, 250), (630, 710)], RED, 30); d.stroke([(630, 250), (170, 710)], RED, 30); return d.out()


def pantheon():                                              # the Panthéon: columned portico, big dome, cute face on the pediment
    d = Draw(1200, 1100); d.rect(160, 600, 1040, 1080, (240, 226, 200, 255)); d.poly([(130, 600), (600, 420), (1070, 600)], fill=(250, 236, 210, 255), outline=LINE, width=14)
    for x in range(220, 1000, 110): d.rect(x, 640, x + 50, 1060, (226, 210, 186, 255)); d.stroke([(x, 640), (x, 1060)], LINE, 6)
    d.rect(450, 200, 750, 430, (236, 220, 196, 255)); d.chord(600, 210, 230, 200, 180, 360, fill=(170, 200, 210, 255), outline=LINE, width=14); d.stroke([(600, 10), (600, 60)], LINE, 12); d.dot(600, 60, 18, YEL)
    d.rect(160, 1040, 1040, 1080, LINE); eyes(d, 600, 520, 0.5, 'happy'); return d.out()


def waves():                                                 # a flying radio signal: cyan rings + a bolt
    d = Draw(900, 600)
    for i in range(4): d.arc(120, 300, 120 + 150 * i, 100 + 110 * i, 300, 60, CYAN, 22 - 3 * i)
    d.poly([(560, 120), (660, 280), (600, 290), (700, 480), (540, 300), (600, 290), (500, 130)], fill=YEL, outline=LINE, width=10); return d.out()


def radio():                                                 # radio station set: wooden cabinet, glowing valves, dials, morse key
    d = Draw(1100, 800); d.rrect(40, 120, 1060, 780, 30, fill=(150, 100, 60, 255), outline=LINE, width=16)
    for x in (200, 360, 520): d.ellipse(x, 120, 50, 90, fill=(255, 210, 120, 220), outline=LINE, width=10); d.dot(x, 140, 22, ORNG)
    for x in (720, 900): d.dot(x, 330, 70, WT); d.ellipse(x, 330, 70, 70, outline=LINE, width=10); d.stroke([(x, 330), (x + 40, 290)], RED, 8)
    d.rrect(120, 560, 980, 720, 20, fill=(60, 40, 30, 255), outline=LINE, width=10); eyes(d, 360, 380, 0.6, 'happy'); return d.out()


def tape():                                                  # intercepted messages: a curling paper tape of dots and dashes
    d = Draw(1200, 600); pts = [(40 + k * 28, 300 + 120 * math.sin(k * 0.22)) for k in range(41)]
    for k in range(40): d.stroke([pts[k], pts[k + 1]], (250, 244, 220, 255), 90)
    for k in range(2, 39, 2): x, y = pts[k]; (d.dot(x, y, 12, LINE) if k % 6 else d.rrect(x - 20, y - 8, x + 20, y + 8, 6, fill=LINE))
    return d.out()


def spy():                                                   # the open loop: trench-coat silhouette with a wide hat, smoke, "?"
    d = Draw(700, 1200); c = (40, 50, 70, 240)
    d.dot(350, 300, 140, c); d.ellipse(350, 190, 250, 50, fill=c); d.chord(350, 190, 130, 120, 180, 360, fill=c)
    d.poly([(170, 440), (530, 440), (620, 1100), (80, 1100)], fill=c); d.rect(160, 1080, 300, 1190, c); d.rect(400, 1080, 540, 1190, c)
    d.text(350, 320, '?', 220, (255, 80, 110, 255), stroke=10, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def roofs(d, y0, col, n=12, seed=3):
    r = np.random.RandomState(seed)
    for k in range(n):
        x = k * W2 / n; h = 160 + r.randint(0, 180); d.rect(x, y0 - h, x + W2 / n - 10, y0 + 40, col); d.poly([(x - 10, y0 - h), (x + W2 / n, y0 - h), (x + W2 / n - 30, y0 - h - 70), (x + 20, y0 - h - 70)], fill=dk(col, 0.8))
        for c in range(2): d.rect(x + 30 + c * 80, y0 - h - 110, x + 60 + c * 80, y0 - h - 60, dk(col, 0.7))
        for wy in range(int(y0 - h) + 40, int(y0), 70): d.rect(x + 30, wy, x + 60, wy + 36, (255, 220, 130, 255)); d.rect(x + W2 / n - 70, wy, x + W2 / n - 40, wy + 36, (255, 220, 130, 255))


def stars(d, n, ybot, seed=3): r = np.random.RandomState(seed); [d.dot(r.randint(0, W2), r.randint(0, ybot), r.choice([3, 4, 6]), (255, 250, 230, 230)) for _ in range(n)]


def nightparis(path):                                        # hook: indigo night, gold-lit Paris roofs, searchlight beams, big moon
    im = sky((40, 40, 120), (110, 90, 180), 1.0); d = Draw(W2, H2); stars(d, 160, 500); d.dot(1900, 220, 110, (255, 246, 210, 255))
    for x, a in ((400, -20), (2000, 20)): d.poly([(x, 900), (x + a * 30 - 120, 0), (x + a * 30 + 120, 0)], fill=(255, 250, 200, 50))
    roofs(d, 860, (80, 70, 130, 255)); fl(d, (70, 60, 110, 255)); im.alpha_composite(d.out()); glow(im, 1900, 220, 260, (255, 240, 200, 90), 60); glow(im, 1200, 820, 900, (255, 200, 120, 60), 120); im.convert('RGB').save(path)


def topnight(path):                                          # tower top at night: deep navy, the city lights far below, stars, cyan glow
    im = sky((20, 30, 90), (60, 70, 160), 1.0); d = Draw(W2, H2); stars(d, 260, 700, 5)
    r = np.random.RandomState(8)
    for _ in range(260): d.dot(r.randint(0, W2), 760 + r.randint(0, 170), 5, (255, 210, 120, 255))
    fl(d, (40, 40, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 700, (80, 220, 255, 60), 140); im.convert('RGB').save(path)


def alley(path):                                             # spy-noir alley: teal fog, wet cobbles, a red lamp-lit window, poster shapes
    im = sky((20, 80, 90), (60, 140, 140), 1.0); d = Draw(W2, H2)
    for x in (0, 1700): d.rect(x, 0, x + 700, 940, (30, 60, 70, 255)); [d.rect(x + 80 + c * 200, y, x + 200 + c * 200, y + 140, (255, 90, 100, 255) if (c + y) % 3 == 0 else (40, 80, 90, 255)) for c in range(3) for y in (120, 380)]
    d.stroke([(1200, 940), (1200, 300)], LINE, 18); d.dot(1200, 290, 50, (255, 236, 160, 255))
    for x, y in ((850, 400), (1450, 500)): d.rrect(x, y, x + 160, y + 220, 10, fill=(200, 60, 80, 255), outline=LINE, width=8)
    fl(d, (40, 70, 80, 255)); im.alpha_composite(d.out()); glow(im, 1200, 290, 300, (255, 230, 160, 120), 60); glow(im, 1200, 700, 900, (180, 255, 240, 50), 140); im.convert('RGB').save(path)


def fair(path):                                              # Paris 1889 world fair: champagne-gold sky, pavilions with domes, flags, balloons
    im = sky((250, 200, 120), (255, 236, 190), 1.0); d = Draw(W2, H2)
    for x in (300, 1100, 1900): d.rect(x - 220, 520, x + 220, 860, (250, 236, 210, 255)); d.chord(x, 520, 150, 160, 180, 360, fill=(110, 170, 200, 255), outline=LINE, width=10); [d.rect(x - 200 + k * 80, 600, x - 170 + k * 80, 840, (226, 206, 176, 255)) for k in range(6)]
    for k in range(14): x = 100 + k * 170; d.stroke([(x, 300), (x, 420)], LINE, 4); d.poly([(x, 300), (x + 70, 330), (x, 360)], fill=(RED, (40, 80, 200, 255), WT)[k % 3], outline=LINE, width=4)
    for x, y, c in ((700, 200, RED), (1600, 150, (60, 140, 220, 255))): d.dot(x, y, 70, c); d.ellipse(x, y, 70, 70, outline=LINE, width=6); d.rect(x - 20, y + 90, x + 20, y + 120, (150, 100, 60, 255))
    fl(d, (220, 190, 140, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 800, (255, 240, 200, 70), 120); im.convert('RGB').save(path)


def bureau(path):                                            # permit office: sage-green panels, brass lamps, tall arched window, filing drawers
    im = sky((120, 170, 140), (180, 214, 186), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 240): d.rrect(x + 20, 520, x + 220, 900, 10, outline=(90, 140, 110, 255), width=10)
    d.rect(950, 120, 1450, 600, (180, 220, 255, 255)); d.chord(1200, 120, 250, 160, 180, 360, fill=(180, 220, 255, 255)); d.stroke([(1200, 0), (1200, 600)], WT, 14); d.stroke([(950, 360), (1450, 360)], WT, 14)
    for x in (300, 2000): d.stroke([(x, 0), (x, 160)], LINE, 6); d.chord(x, 200, 90, 50, 180, 360, fill=GOLD2, outline=LINE, width=8)
    for k in range(4): d.rrect(1700 + k * 150, 400, 1830 + k * 150, 880, 8, fill=(140, 100, 70, 255), outline=LINE, width=6)
    fl(d, (110, 80, 60, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 400, (255, 255, 240, 80), 80); im.convert('RGB').save(path)


def cafe(path):                                              # artists' café: wine-red walls, gold mirrors, framed paintings, round tables
    im = sky((150, 40, 60), (200, 80, 90), 1.0); d = Draw(W2, H2)
    for x in (300, 1100, 1900): d.ellipse(x, 360, 200, 250, fill=(250, 220, 170, 255), outline=GOLD2, width=24)
    for x, y, c in ((700, 250, (90, 140, 220, 255)), (1500, 300, (250, 180, 80, 255)), (2250, 260, (120, 200, 140, 255))): d.rect(x - 110, y - 80, x + 110, y + 80, c); d.rrect(x - 120, y - 90, x + 120, y + 90, 6, outline=GOLD2, width=16)
    d.rect(0, 680, W2, 940, (110, 30, 46, 255)); d.stroke([(0, 680), (W2, 680)], GOLD2, 12)
    fl(d, (90, 30, 40, 255)); im.alpha_composite(d.out()); glow(im, 1200, 300, 600, (255, 200, 140, 70), 100); im.convert('RGB').save(path)


def demolish(path):                                          # demolition day: stormy slate sky, hazard stripes, rubble, orange cones
    im = sky((90, 100, 130), (150, 160, 180), 1.0); d = Draw(W2, H2)
    for x, y, r in ((400, 200, 160), (700, 160, 200), (1700, 180, 180), (2000, 220, 150)): d.dot(x, y, r, (110, 116, 140, 220))
    for x in range(0, W2, 160): d.poly([(x, 760), (x + 80, 760), (x + 40, 860), (x - 40, 860)], fill=YEL); d.poly([(x + 80, 760), (x + 160, 760), (x + 120, 860), (x + 40, 860)], fill=LINE)
    for x in (300, 900, 1500, 2100): d.poly([(x - 50, 940), (x, 760), (x + 50, 940)], fill=ORNG, outline=LINE, width=8); d.rect(x - 30, 860, x + 30, 880, WT)
    fl(d, (130, 126, 130, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def dawn(path):                                              # Latin Quarter at dawn: peach-pink sky, cream stone streets, trees, pigeons
    im = sky((255, 170, 150), (255, 226, 200), 1.0); d = Draw(W2, H2); d.dot(400, 600, 160, (255, 240, 190, 255))
    roofs(d, 880, (236, 210, 190, 255), 10, 7)
    for x in (200, 2200): d.dot(x, 600, 160, (110, 170, 110, 255)); d.rect(x - 20, 700, x + 20, 900, (120, 80, 60, 255))
    fl(d, (226, 200, 176, 255)); im.alpha_composite(d.out()); glow(im, 400, 600, 400, (255, 240, 200, 110), 80); im.convert('RGB').save(path)


def camp(path):                                              # army camp on the Champ de Mars: olive tents, tricolour flags, blue morning sky
    im = sky((110, 170, 230), (200, 226, 250), 1.0); d = Draw(W2, H2)
    for x in range(100, W2, 380): d.poly([(x, 880), (x + 160, 640), (x + 320, 880)], fill=(120, 130, 80, 255), outline=LINE, width=10); d.poly([(x + 130, 880), (x + 160, 720), (x + 190, 880)], fill=(60, 60, 40, 255))
    for x in (500, 1300, 2100): d.stroke([(x, 640), (x, 380)], LINE, 8); d.rect(x, 380, x + 60, 440, (40, 70, 180, 255)); d.rect(x + 60, 380, x + 120, 440, WT); d.rect(x + 120, 380, x + 180, 440, RED)
    fl(d, (150, 150, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def valves(path):                                            # radio station room: dark walnut walls, amber valve racks, wires, a round window on the city
    im = sky((90, 60, 40), (150, 100, 60), 1.0); d = Draw(W2, H2)
    for x in range(100, W2, 420):
        d.rrect(x, 180, x + 300, 860, 14, fill=(70, 46, 34, 255), outline=LINE, width=10)
        for y in range(240, 820, 110): [d.ellipse(x + 60 + c * 90, y, 26, 40, fill=(255, 200, 110, 230), outline=LINE, width=6) for c in range(3)]
    d.dot(1200, 300, 130, (60, 70, 140, 255)); d.ellipse(1200, 300, 130, 130, outline=GOLD2, width=20)
    fl(d, (80, 56, 40, 255)); im.alpha_composite(d.out()); [glow(im, x + 150, 520, 260, (255, 180, 90, 70), 60) for x in range(100, W2, 420)]; im.convert('RGB').save(path)


def warnight(path):                                          # war: blood-red night sky, crossing searchlights, smoke, dark rooftops
    im = sky((120, 30, 50), (200, 80, 70), 1.0); d = Draw(W2, H2)
    for x, a in ((300, 30), (900, -25), (1600, 20), (2200, -30)): d.poly([(x, 900), (x + a * 25 - 90, 0), (x + a * 25 + 90, 0)], fill=(255, 240, 200, 60))
    for x, y, r in ((500, 300, 130), (1800, 250, 160)): d.dot(x, y, r, (90, 50, 60, 160))
    roofs(d, 880, (70, 40, 60, 255), 12, 9); fl(d, (60, 36, 50, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 900, (255, 120, 80, 60), 140); im.convert('RGB').save(path)


def bigear(path):                                            # the big ear: teal noir sky full of floating sound waves and morse dots
    im = sky((20, 100, 110), (70, 170, 170), 1.0); d = Draw(W2, H2)
    for i in range(7): d.arc(1200, 500, 250 + 160 * i, 160 + 100 * i, 200, 340, (120, 240, 240, 140), 10)
    for k in range(30): x, y = (k * 389) % W2, 100 + (k * 173) % 600; (d.dot(x, y, 12, WT) if k % 3 else d.rrect(x - 26, y - 8, x + 26, y + 8, 6, fill=WT))
    roofs(d, 900, (30, 70, 80, 255), 12, 4); fl(d, (30, 80, 90, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    B.human_head, B.human_body = head, LA.body
    for ch in ('eiffel', 'artist', 'artist2', 'boss', 'soldier', 'radioman', 'mata'): layers, faces = B.build_human(ch); items += [(ch + ' ' + e, faces[e]) for e in ('happy', 'shocked')]
    multi = dict(tower={'default': tower(), 'shocked': tower('shocked'), 'nervous': tower('sad'), 'wire': tower('wire'), 'ear': tower('ear')}, towertop={'default': towertop()},
                 ball={'default': ball()}, permit={'default': permit(), 'renewed': permit(True)}, easel={'default': easel()}, pantheon={'default': pantheon()}, waves={'default': waves()},
                 radio={'default': radio()}, tape={'default': tape()}, spy={'default': spy()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    P_ = lambda a, b, bg, w=1000, bs=130, ss=130, bd=GOLDL: plaque(a, b, bg, WHITE, w, border=bd, bs=bs, ss=ss, sc=bd)
    cards = dict(hookc=M.bigneon('BUILT TO BE', 'TORN DOWN!', 1000, YEL, PINK),
                 wire=P_('ONE WIRE', 'SAVED IT!', TEAL, 900, 170, 170, CYAN),
                 spyc=stamp('IT CAUGHT A SPY?!', 960, RED, 120, -4),
                 y1889=M.cal('PARIS', '1889', (60, 80, 200, 255)),
                 eiffelc=P_('GUSTAVE', 'EIFFEL', (60, 50, 80, 255), 900, 150, 190, GOLD2),
                 permitc=P_('PERMIT:', 'JUST 20 YEARS', (110, 150, 120, 255), 960, 150, 140, WT),
                 artists=P_('FAMOUS ARTISTS', 'HATE IT!', (150, 40, 60, 255), 1000, 120, 170),
                 useless=M.bigneon('"USELESS AND', 'MONSTROUS!"', 1000, PINK, YEL),
                 after20=P_('AFTER 20 YEARS:', 'TEAR IT DOWN', (90, 100, 130, 255), 1000, 120, 140, ORNG),
                 tear=stamp('TEAR IT DOWN!', 900, ORNG, 140, -3),
                 reason=P_('EIFFEL NEEDS', 'A REASON', (60, 50, 80, 255), 940, 140, 160, GOLD2),
                 bigone=stamp('A BIG ONE!', 760, VIO, 150, 4),
                 antenna=M.bigneon('A GIANT', 'ANTENNA!', 900, CYAN, YEL),
                 y1898=M.cal('SIGNAL', '1898', TEAL),
                 pantc=P_('THE PANTHEON', '4 KM AWAY!', (230, 140, 120, 255), 960, 140, 170, WT),
                 army=stamp('THE ARMY MOVES IN!', 1000, (80, 100, 60, 255), 110, -3),
                 station=P_('PERMANENT', 'RADIO STATION', (150, 100, 60, 255), 960, 150, 130),
                 plus70=M.bigneon('+70 MORE', 'YEARS!', 860, (120, 240, 140, 255), YEL),
                 war=stamp('THEN WAR COMES', 940, RED, 130, -4),
                 listens=P_('IT LISTENS TO', 'ENEMY RADIO', TEAL, 980, 130, 150, CYAN),
                 bigear=M.bigneon('"THE', 'BIG EAR"', 820, CYAN, PINK),
                 intercept=stamp('INTERCEPTED!', 880, (40, 120, 130, 255), 140, 3),
                 h21=P_('SECRET AGENT', 'CODE NAME H-21', (40, 50, 70, 255), 1000, 130, 140, (255, 120, 140, 255)),
                 realname=stamp('HER REAL NAME?', 900, (120, 30, 60, 255), 130, -3),
                 matac=M.bigneon('MATA', 'HARI!', 760, PINK, YEL),
                 notbad=P_('NOT BAD', 'FOR A TOWER!', (60, 50, 80, 255), 980, 140, 130, GOLD2))
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_wood(T('wood.jpg')); CE.tiles(T('pave.jpg'), (120, 110, 150), (106, 96, 136))
    CE.tiles(T('cobnight.jpg'), (90, 84, 130), (78, 72, 116)); M.sandtex(T('ironfloor.jpg'), (60, 60, 110), (200, 200, 255), seed=5); CE.tiles(T('wetcob.jpg'), (50, 90, 100), (40, 76, 86))
    M.sandtex(T('fairsand.jpg'), (226, 196, 150), (206, 176, 132)); CE.tiles(T('parquet.jpg'), (150, 100, 70), (134, 88, 60)); CE.tiles(T('cafefloor.jpg'), (240, 230, 210), (60, 50, 50))
    M.sandtex(T('rubble.jpg'), (150, 146, 150), (120, 116, 122)); CE.tiles(T('stone.jpg'), (236, 216, 196), (220, 200, 180)); M.sandtex(T('grass2.jpg'), (130, 160, 90), (110, 140, 76))
    CE.tiles(T('walnut.jpg'), (110, 76, 54), (96, 66, 46)); CE.tiles(T('redcob.jpg'), (110, 50, 60), (96, 40, 50)); CE.tiles(T('tealcob.jpg'), (50, 110, 116), (40, 96, 100))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(nightparis=nightparis, topnight=topnight, alley=alley, fair=fair, bureau=bureau, cafe=cafe, demolish=demolish, dawn=dawn, camp=camp, valves=valves, warnight=warnight, bigear=bigear)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
