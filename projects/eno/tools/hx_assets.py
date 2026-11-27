"""Shared cast + helpers for videos 20-22 (1904 marathon, Statue of Liberty, teddy bear): new hats (top hat, boater, flat cap, goggles,
campaign hat, slouch hat, paper hat), new bodies (runner tank + bib, apron, khaki jacket, pyjamas, clerical collar, smock, lab coat).
Every character is unique to its video (names never reused as card names)."""
import math
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

GOLDL = M.GOLDL
dk, glow, plaque, stamp, sky, W2, H2, fl = LA.dk, CE.glow, LA.plaque, LA.stamp, M.sky, M.W2, M.H2, MA.fl
eyes, shine, win = PD.eyes, PD.shine, PD.win
WT, PINK, CYAN, YEL, ORNG, TEAL, NAVY, RED, VIO = (250, 250, 245, 255), (255, 110, 170, 255), (80, 230, 255, 255), (255, 214, 60, 255), (255, 140, 40, 255), (30, 150, 150, 255), (30, 40, 100, 255), (220, 40, 60, 255), (150, 100, 220, 255)
LIME, COP, VERD, HONEY, BRN = (182, 255, 60, 255), (214, 120, 70, 255), (90, 200, 170, 255), (236, 170, 80, 255), (120, 80, 50, 255)
LA.NEW.update({
    # video 20 - 1904 marathon
    'lorz': dict(sk=0, style='curly', hair=(90, 60, 40, 255), suit=(250, 250, 240, 255), shade=(214, 214, 204, 255), body='runner', bib='31', bibc=(40, 80, 200, 255), stripe=(40, 80, 200, 255)),
    'hicks': dict(sk=0, style='side', hair=(214, 160, 80, 255), suit=(200, 50, 60, 255), shade=(170, 36, 48, 255), body='runner', bib='20', bibc=RED, stripe=WT, stache=(214, 160, 80, 255)),
    'felix': dict(sk=1, style='spiky', hair=(30, 24, 24, 255), suit=(250, 236, 200, 255), shade=(220, 204, 166, 255), body='runner', bib='3', bibc=(30, 140, 80, 255), stripe=(240, 80, 60, 255), xhat='flatcap'),
    'tau': dict(sk=2, style='curly', hair=(30, 24, 24, 255), suit=(250, 210, 60, 255), shade=(220, 176, 40, 255), body='runner', bib='35', bibc=(30, 120, 60, 255), stripe=(30, 120, 60, 255)),
    'sullivan': dict(sk=0, style='part', hair=(60, 44, 34, 255), suit=(44, 54, 100, 255), shade=(32, 40, 78, 255), body='suit', tie=(240, 180, 60, 255), stache=(60, 44, 34, 255), glasses=1, xhat='tophat'),
    'trainer': dict(sk=2, style='bald', hair=(236, 236, 236, 255), suit=(60, 140, 90, 255), shade=(44, 112, 70, 255), body='sweater', stache=(236, 236, 236, 255), glasses=2),
    'judge': dict(sk=1, style='quiff', hair=(70, 46, 34, 255), suit=(150, 90, 180, 255), shade=(124, 70, 154, 255), body='suit', tie=YEL, xhat='boater'),
    # video 21 - Statue of Liberty
    'bartholdi': dict(sk=0, style='curly', hair=(70, 50, 40, 255), suit=(80, 120, 200, 255), shade=(60, 96, 170, 255), body='smock', stache=(70, 50, 40, 255), beard=(70, 50, 40, 255)),
    'official': dict(sk=1, style='bald', hair=(210, 210, 210, 255), suit=(120, 116, 136, 255), shade=(96, 92, 112, 255), body='suit', tie=RED, glasses=1),
    'senator': dict(sk=0, style='slick', hair=(40, 40, 50, 255), suit=(70, 44, 100, 255), shade=(54, 32, 80, 255), body='suit', tie=(240, 190, 80, 255), stache=(40, 40, 50, 255)),
    'newsboy': dict(sk=2, style='spiky', hair=(30, 24, 24, 255), suit=(230, 130, 60, 255), shade=(200, 104, 40, 255), body='denim', freck=1, hat='cap'),
    'chemist': dict(sk=1, style='bob', hair=(40, 30, 34, 255), suit=(250, 250, 250, 255), shade=(220, 224, 232, 255), body='labcoat', band=VERD, xhat='goggles'),
    # video 22 - teddy bear
    'teddyr': dict(sk=0, style='side', hair=(110, 80, 60, 255), suit=(196, 170, 110, 255), shade=(168, 142, 88, 255), body='khaki', stache=(110, 80, 60, 255), glasses=1, xhat='campaign'),
    'collier': dict(sk=2, style='bald', hair=(236, 236, 236, 255), suit=(110, 90, 140, 255), shade=(88, 70, 116, 255), body='denim', stache=(236, 236, 236, 255), beard=(236, 236, 236, 255), xhat='slouch'),
    'berryman': dict(sk=0, style='part', hair=(150, 110, 70, 255), suit=(50, 70, 120, 255), shade=(38, 54, 96, 255), body='suit', tie=RED, stache=(150, 110, 70, 255), glasses=2),
    'morris': dict(sk=0, style='curly', hair=(34, 28, 30, 255), suit=(220, 70, 90, 255), shade=(190, 50, 70, 255), body='apron', stache=(34, 28, 30, 255), xhat='paperhat'),
    'rose': dict(sk=0, style='side', hair=(120, 60, 40, 255), suit=(250, 150, 180, 255), shade=(224, 120, 152, 255), body='cardigan', bun=1),
    'priest': dict(sk=1, style='part', hair=(170, 170, 176, 255), suit=(50, 46, 60, 255), shade=(36, 32, 44, 255), body='collar', glasses=1),
    'kid': dict(sk=1, style='spiky', hair=(90, 56, 36, 255), suit=(110, 160, 240, 255), shade=(86, 132, 210, 255), body='pjs', freck=1),
    'kid2': dict(sk=2, style='bob', hair=(30, 24, 24, 255), suit=(250, 140, 190, 255), shade=(222, 112, 162, 255), body='pjs', band=YEL),
    'buyer': dict(sk=0, style='quiff', hair=(200, 90, 50, 255), suit=(90, 150, 110, 255), shade=(70, 124, 88, 255), body='suit', tie=YEL, hat='fedora'),
})


def head(char, expr):
    im = MA.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']; x = c.get('xhat')
    if c.get('beard'): d.chord(cx, cy + 150, R - 40, 120, 0, 180, fill=c['beard'], outline=LINE, width=12)
    if x == 'tophat':
        d.rrect(cx - R + 60, cy - R - 230, cx + R - 60, cy - R + 50, 18, fill=(36, 32, 44, 255), outline=LINE, width=14); d.rect(cx - R + 64, cy - R - 10, cx + R - 64, cy - R + 30, RED)
        d.ellipse(cx, cy - R + 52, R + 50, 30, fill=(36, 32, 44, 255), outline=LINE, width=12); d.rect(cx - R + 90, cy - R - 200, cx - R + 110, cy - R - 60, (255, 255, 255, 90))
    elif x == 'boater':
        d.rrect(cx - R + 50, cy - R - 70, cx + R - 50, cy - R + 50, 14, fill=(244, 214, 130, 255), outline=LINE, width=14); d.rect(cx - R + 54, cy - R - 6, cx + R - 54, cy - R + 30, (40, 60, 160, 255))
        d.ellipse(cx, cy - R + 50, R + 70, 30, fill=(244, 214, 130, 255), outline=LINE, width=12)
    elif x == 'flatcap':
        d.chord(cx, cy - R + 84, R + 14, R - 40, 180, 360, fill=(120, 130, 160, 255), outline=LINE, width=14); d.ellipse(cx + 110, cy - R + 84, 130, 28, fill=(100, 110, 140, 255), outline=LINE, width=12)
    elif x == 'goggles':
        d.stroke([(cx - R + 10, cy - R + 90), (cx + R - 10, cy - R + 90)], (60, 60, 70, 255), 20)
        for sg in (-1, 1): d.dot(cx + sg * 64, cy - R + 90, 48, (150, 240, 220, 230)); d.ellipse(cx + sg * 64, cy - R + 90, 48, 48, outline=LINE, width=12); d.dot(cx + sg * 64 - 16, cy - R + 74, 12, WT)
    elif x == 'campaign':
        d.ellipse(cx, cy - R + 56, R + 100, 40, fill=(150, 110, 70, 255), outline=LINE, width=14)
        d.poly([(cx - R + 50, cy - R + 56), (cx - 70, cy - R - 150), (cx, cy - R - 110), (cx + 70, cy - R - 150), (cx + R - 50, cy - R + 56)], fill=(170, 126, 80, 255), outline=LINE, width=14)
        d.rect(cx - R + 56, cy - R + 10, cx + R - 56, cy - R + 46, (90, 60, 40, 255))
    elif x == 'slouch':
        d.chord(cx, cy - R + 70, R - 10, R - 10, 180, 360, fill=(80, 70, 74, 255), outline=LINE, width=14); d.ellipse(cx, cy - R + 70, R + 76, 42, fill=(70, 60, 64, 255), outline=LINE, width=12)
        d.rect(cx - R + 30, cy - R + 30, cx + R - 30, cy - R + 60, (150, 60, 60, 255))
    elif x == 'paperhat':
        d.poly([(cx - R + 30, cy - R + 80), (cx - R + 80, cy - R - 60), (cx + R - 80, cy - R - 60), (cx + R - 30, cy - R + 80)], fill=WT, outline=LINE, width=12); d.rect(cx - R + 50, cy - R + 20, cx + R - 50, cy - R + 50, RED)
    im.alpha_composite(d.out()); return im


NEWB = ('runner', 'apron', 'khaki', 'pjs', 'collar', 'smock', 'labcoat')


def body(char):
    c = LA.NEW[char]; bs = c['body']
    if bs not in NEWB: return LA.body(char)
    LA.NEW['_tmp'] = dict(c, body='plain'); im = LA.body('_tmp'); d = Draw(im.width, im.height); x0, y0, x1, y1, r = 85, 458, 375, 800, 115
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); t = Draw(d.w, d.h); base = c['suit']
    if bs == 'runner':                                       # sleeveless running vest, sash stripe, pinned bib with the race number
        t.stroke([(100, 470), (360, 790)], c['stripe'], 34); t.chord(230, 452, 70, 40, 0, 180, fill=dk(base, 0.8))
        t.rrect(150, 560, 310, 700, 14, fill=WT, outline=LINE, width=8); t.text(230, 632, c['bib'], 90 if len(c['bib']) < 3 else 70, c['bibc'])
        for x in (162, 298): t.dot(x, 572, 6, (150, 150, 160, 255))
    elif bs == 'apron':                                      # white shop apron with a pocket and a candy stripe
        t.rrect(140, 520, 320, 820, 30, fill=WT); t.rect(140, 600, 320, 620, PINK); t.rrect(190, 680, 270, 740, 10, outline=(200, 200, 210, 255), width=6)
        for sg in (-1, 1): t.stroke([(230 + sg * 80, 520), (230 + sg * 50, 455)], WT, 16)
    elif bs == 'khaki':                                      # safari jacket: chest pockets, buttons, belt, neckerchief
        for sg in (-1, 1): t.rrect(230 + sg * 75 - 42, 520, 230 + sg * 75 + 42, 590, 8, outline=dk(base, 0.7), width=6)
        for y in (520, 600, 680): t.dot(230, y, 8, (120, 90, 50, 255))
        t.rect(85, 700, 375, 730, (110, 76, 46, 255)); t.poly([(186, 452), (274, 452), (230, 520)], fill=RED)
    elif bs == 'pjs':                                        # striped pyjamas with a moon pocket
        for x in range(95, 380, 44): t.rect(x, 450, x + 16, 800, (255, 255, 255, 110))
        t.chord(230, 452, 70, 36, 0, 180, fill=dk(base, 0.8)); t.dot(300, 560, 22, YEL); t.dot(310, 552, 18, base)
    elif bs == 'collar':                                     # clerical collar
        t.chord(230, 452, 80, 46, 0, 180, fill=(30, 26, 36, 255)); t.rect(214, 452, 246, 486, WT); t.stroke([(230, 520), (230, 800)], dk(base, 0.6), 6)
    elif bs == 'smock':                                      # sculptor smock with a big floppy bow
        t.poly([(186, 470), (230, 500), (186, 530)], fill=RED, outline=LINE, width=6); t.poly([(274, 470), (230, 500), (274, 530)], fill=RED, outline=LINE, width=6); t.dot(230, 500, 14, RED)
        for y in (600, 680, 760): t.dot(230, y, 9, WT)
        t.rrect(110, 640, 190, 720, 12, outline=dk(base, 0.7), width=6)
    elif bs == 'labcoat':                                    # lab coat: lapels, pocket pens, mint shirt
        t.poly([(186, 452), (274, 452), (230, 560)], fill=(150, 230, 210, 255))
        for sg in (-1, 1): t.stroke([(230 + sg * 44, 456), (230 + sg * 12, 640)], (200, 204, 214, 255), 10)
        t.rrect(270, 600, 330, 650, 6, outline=(200, 204, 214, 255), width=6); t.rect(282, 580, 290, 610, RED); t.rect(300, 584, 308, 610, (60, 120, 220, 255))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=H['lw']); im.alpha_composite(d.out()); return im


def build_cast(names, faces=('happy', 'shocked')):
    B.human_head, B.human_body = head, body; items = []
    for ch in names: layers, fc = B.build_human(ch); items += [(ch + ' ' + e, fc[e]) for e in faces]
    return items


def P_(a, b, bg, w=1000, bs=130, ss=130, bd=GOLDL): return plaque(a, b, bg, WHITE, w, border=bd, bs=bs, ss=ss, sc=bd)


def cards_out(ROOT, cards, multi, items):
    import os, json
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    json.dump({nm: round(im.width / im.height, 3) for nm, im in list(cards.items()) + [(k, v['default']) for k, v in multi.items()]}, open(os.path.join(ROOT, 'aspect.json'), 'w'))


def stars(d, n, ybot, seed=3): r = np.random.RandomState(seed); [d.dot(r.randint(0, W2), r.randint(0, ybot), r.choice([3, 4, 6]), (255, 250, 230, 230)) for _ in range(n)]


def hills(d, y0, col, amp=80, k=3, ph=0.0):
    pts = [(x, y0 - amp * (0.5 + 0.5 * math.sin(x / W2 * math.pi * k + ph))) for x in range(0, W2 + 1, 40)]; d.poly(pts + [(W2, H2), (0, H2)], fill=col)


def ptree(d, x, y, s, leaf, trunk=(120, 80, 50, 255), fruit=None):
    d.rect(x - 14 * s, y - 120 * s, x + 14 * s, y, trunk); d.dot(x, y - 170 * s, 90 * s, leaf); d.ellipse(x, y - 170 * s, 90 * s, 90 * s, outline=LINE, width=6)
    if fruit:
        for a in range(0, 360, 60): d.dot(x + 55 * s * math.cos(math.radians(a)), y - 170 * s + 50 * s * math.sin(math.radians(a)), 14 * s, fruit)
