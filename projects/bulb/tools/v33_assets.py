"""Shared helpers for videos 33-36 (oldest light bulb, stop-sign inventor, chunky ice cream, Streisand Effect): new hats (fire helmet,
bolt cap, sailor cap, flower bonnet hat, riding bowler, 1860s police dome, soda-jerk paper cap, leather aviator cap, round-glasses beanie),
new bodies (fire turnout coat, electrician coverall, sailor suit, bustle dress, red riding coat, 1860s police coat, tie-dye tee, striped
soda apron, flight jacket, three-piece lawyer, blogger zip hoodie) and the reusable StopperText card: glossy extruded 3D letters in the
video's own stopper font on a sticker plate, one image per animation state (off/lit, slap, counter roll, redacted peel)."""
import os
from v29_assets import *
import v29_assets as V29
from PIL import ImageFont

HATS5 = ('firehelm', 'boltcap', 'sailor', 'flowerhat', 'riding', 'bobby', 'sodacap', 'aviator', 'beanie5')
NEWB5 = ('turnout', 'coverall', 'sailorsuit', 'bustle', 'redcoat', 'police67', 'tiedye', 'soda', 'flightjk', 'vest3', 'zip')


def head(char, expr):
    c = LA.NEW[char]; x = c.get('xhat5'); im = V29.head(char, expr); d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']; hc = c.get('hatc', (200, 60, 60, 255))
    if x == 'firehelm':                                      # classic fire helmet: long back brim, ridge comb, front shield with a number
        d.ellipse(cx + 20, cy - R + 112, R + 70, 30, fill=hc, outline=LINE, width=12); d.chord(cx, cy - R + 112, R + 6, R - 10, 180, 360, fill=hc, outline=LINE, width=14)
        d.stroke([(cx - R + 40, cy - R + 60), (cx, cy - R - 2), (cx + R - 40, cy - R + 60)], dk(hc, 0.75), 14)
        d.poly([(cx - 70, cy - R + 20), (cx + 70, cy - R + 20), (cx + 60, cy - R + 110), (cx - 60, cy - R + 110)], fill=YEL, outline=LINE, width=8); d.text(cx, cy - R + 66, c.get('num', '6'), 70, LINE)
    elif x == 'boltcap':                                     # electrician cap with a lightning-bolt badge and a pencil
        d.chord(cx, cy - R + 104, R + 10, R - 30, 180, 360, fill=hc, outline=LINE, width=14); d.chord(cx + 90, cy - R + 104, R - 40, 40, 0, 180, fill=dk(hc, 0.75), outline=LINE, width=10)
        d.poly([(cx - 10, cy - R + 10), (cx - 40, cy - R + 60), (cx - 6, cy - R + 56), (cx - 26, cy - R + 98), (cx + 36, cy - R + 40), (cx + 2, cy - R + 44)], fill=YEL, outline=LINE, width=6)
    elif x == 'sailor':                                      # little sailor cap with a navy band and ribbon
        d.ellipse(cx, cy - R + 70, R - 10, 54, fill=WT, outline=LINE, width=12); d.rect(cx - R + 30, cy - R + 76, cx + R - 30, cy - R + 104, hc); d.stroke([(cx + R - 50, cy - R + 100), (cx + R - 10, cy - R + 170)], hc, 12)
    elif x == 'flowerhat':                                   # wide Victorian hat with ribbon and three flowers
        d.ellipse(cx, cy - R + 84, R + 90, 40, fill=hc, outline=LINE, width=12); d.chord(cx, cy - R + 80, R - 30, R - 40, 180, 360, fill=hc, outline=LINE, width=12)
        d.rect(cx - R + 34, cy - R + 46, cx + R - 34, cy - R + 72, c.get('band2', (250, 240, 250, 255)))
        for k, fc in enumerate(((255, 120, 170, 255), (255, 214, 60, 255), (150, 200, 255, 255))): fx_ = cx - 120 + k * 60; [d.dot(fx_ + 18 * math.cos(a), cy - R + 40 + 18 * math.sin(a), 16, fc) for a in (0, 1.26, 2.5, 3.8, 5.0)]; d.dot(fx_, cy - R + 40, 10, YEL)
    elif x == 'riding':                                      # black riding bowler with a short brim
        d.ellipse(cx, cy - R + 92, R + 30, 26, fill=hc, outline=LINE, width=12); d.chord(cx, cy - R + 92, R - 30, R - 20, 180, 360, fill=hc, outline=LINE, width=12); d.ellipse(cx - 60, cy - R + 30, 40, 16, fill=(255, 255, 255, 70))
    elif x == 'bobby':                                       # tall 1860s police dome helmet with a star badge and a knob
        d.chord(cx, cy - R + 110, R - 10, R + 40, 180, 360, fill=hc, outline=LINE, width=14); d.dot(cx, cy - R - 70, 18, YEL); d.text(cx, cy - R + 40, '*', 110, YEL, stroke=5, stroke_fill=LINE)
        d.ellipse(cx, cy - R + 112, R + 10, 20, fill=dk(hc, 0.7), outline=LINE, width=8)
    elif x == 'sodacap':                                     # white folded soda-jerk paper cap with a red stripe
        d.poly([(cx - R + 30, cy - R + 100), (cx - R + 60, cy - R + 10), (cx + R - 60, cy - R + 10), (cx + R - 30, cy - R + 100)], fill=WT, outline=LINE, width=12); d.rect(cx - R + 50, cy - R + 60, cx + R - 50, cy - R + 80, hc)
    elif x == 'aviator':                                     # leather aviator cap with ear flaps and goggles on the brow
        d.chord(cx, cy - R + 130, R + 14, R + 10, 180, 360, fill=hc, outline=LINE, width=14)
        for sg in (-1, 1): d.rrect(cx + sg * (R - 10) - 40, cy - 40, cx + sg * (R - 10) + 40, cy + 90, 30, fill=hc, outline=LINE, width=10); d.dot(cx + sg * 70, cy - R + 104, 44, (150, 220, 250, 255)); d.ellipse(cx + sg * 70, cy - R + 104, 44, 44, outline=LINE, width=10)
    elif x == 'beanie5':                                     # slouchy knit beanie with a fold and stripes
        d.chord(cx, cy - R + 120, R + 16, R + 20, 180, 360, fill=hc, outline=LINE, width=14); d.rect(cx - R - 10, cy - R + 92, cx + R + 10, cy - R + 124, dk(hc, 0.78)); [d.stroke([(cx + k * 44, cy - R + 20), (cx + k * 44, cy - R + 90)], dk(hc, 0.85), 6) for k in range(-3, 4)]
    im.alpha_composite(d.out()); return im


def body(char):
    c = LA.NEW[char]; bs = c['body']
    if bs not in NEWB5: return V29.body(char)
    LA.NEW['_tmp'] = dict(c, body='plain'); im = LA.body('_tmp'); d = Draw(im.width, im.height); x0, y0, x1, y1, r = 85, 458, 375, 800, 115
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); t = Draw(d.w, d.h); base = c['suit']; ac = c.get('acc', RED)
    if bs == 'turnout':                                      # fire turnout coat: reflective stripes, clasps
        for y in (600, 720): t.rect(85, y, 375, y + 30, YEL); t.rect(85, y + 8, 375, y + 20, (230, 230, 235, 255))
        [t.rrect(214, yy, 246, yy + 20, 6, fill=(60, 60, 70, 255)) for yy in (500, 560, 660)]
    elif bs == 'coverall':                                   # electrician coverall: zip, tool belt with pliers + screwdriver, bolt patch
        t.stroke([(230, 460), (230, 800)], dk(base, 0.7), 8); t.rect(85, 690, 375, 726, (90, 70, 50, 255)); t.rect(120, 700, 140, 780, (230, 60, 60, 255)); t.rect(300, 696, 312, 790, YEL)
        t.poly([(282, 520), (300, 520), (290, 548), (306, 548), (276, 590), (286, 556), (272, 556)], fill=YEL)
    elif bs == 'sailorsuit':                                 # kid sailor suit: square collar with stripes, red neck bow
        t.poly([(120, 452), (340, 452), (300, 560), (160, 560)], fill=ac); t.stroke([(140, 470), (320, 470)], WT, 6); t.poly([(206, 520), (230, 540), (254, 520), (230, 580)], fill=RED)
    elif bs == 'bustle':                                     # Victorian bustle dress: lace collar, buttons, ruffle hem
        t.poly([(180, 452), (280, 452), (230, 510)], fill=WT); [t.dot(230, y, 9, WT) for y in (540, 590, 640)]; [t.dot(x, 790, 22, dk(base, 0.8)) for x in range(95, 380, 36)]
    elif bs == 'redcoat':                                    # red riding coat, cream stock tie, gold buttons
        t.poly([(186, 452), (274, 452), (230, 580)], fill=(250, 240, 220, 255)); [t.dot(x, y, 10, YEL) for x in (200, 260) for y in (600, 680)]
    elif bs == 'police67':                                   # 1860s police frock coat: double buttons, belt, badge
        [t.dot(x, y, 10, YEL) for x in (190, 270) for y in (520, 590, 660)]; t.rect(85, 700, 375, 730, (40, 40, 50, 255)); t.text(320, 520, '*', 80, YEL)
    elif bs == 'tiedye':                                     # tie-dye tee with a peace-like swirl
        for k, col in enumerate(((255, 120, 170, 255), (255, 214, 60, 255), (120, 220, 255, 255), (150, 230, 120, 255))): t.ellipse(230, 640, 150 - k * 34, 130 - k * 30, outline=col, width=26)
    elif bs == 'soda':                                       # white soda-jerk shirt, striped apron, bow tie
        t.rect(120, 560, 340, 800, WT); [t.rect(x, 560, x + 18, 800, ac) for x in range(130, 340, 40)]; t.poly([(206, 470), (230, 482), (206, 494)], fill=ac); t.poly([(254, 470), (230, 482), (254, 494)], fill=ac)
    elif bs == 'flightjk':                                   # brown flight jacket with a fleece collar and a camera strap
        t.poly([(150, 452), (310, 452), (290, 520), (170, 520)], fill=(250, 240, 225, 255)); t.stroke([(120, 470), (330, 780)], (40, 40, 50, 255), 14); t.rrect(270, 690, 360, 770, 10, fill=(60, 60, 70, 255), outline=LINE, width=6); t.dot(315, 730, 22, (150, 210, 250, 255))
    elif bs == 'vest3':                                      # three-piece suit: waistcoat, tie, watch chain
        t.poly([(170, 452), (290, 452), (300, 760), (160, 760)], fill=dk(base, 0.72)); t.poly([(220, 470), (240, 470), (246, 600), (230, 620), (214, 600)], fill=ac); t.arc(230, 680, 60, 30, 0, 180, YEL, 5)
    elif bs == 'zip':                                        # zip hoodie with drawstrings and a laptop sticker
        t.stroke([(230, 470), (230, 800)], dk(base, 0.6), 10); [t.stroke([(x, 470), (x, 560)], WT, 6) for x in (200, 260)]; t.rrect(110, 640, 190, 700, 10, fill=ac)
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=H['lw']); im.alpha_composite(d.out()); return im


def build_cast5(names, faces=('happy', 'shocked')):
    for n in names:
        c = LA.NEW[n]
        if c.get('xhat') in HATS5: c['xhat5'] = c.pop('xhat')
        elif c.get('xhat') in ('stovepipe', 'coonskin', 'kepi', 'straw', 'headphones', 'pilot', 'homburg', 'feather', 'hardhat', 'beret', 'fedora', 'newsboy'): c['xhat2'] = c.pop('xhat')
    B.human_head, B.human_body = head, body; items = []
    for ch in names: layers, fc = B.build_human(ch); items += [(ch + ' ' + e, fc[e]) for e in faces]
    return items


# ------------------------------------------------------------------ StopperText: glossy extruded 3D letters (its own font, not the caption font)
SFONT = os.path.join(B.ROOT, 'fonts', 'stop.ttf')


def fitf(txt, size, maxw, font=None):
    f = font or SFONT
    while size > 24 and ImageFont.truetype(f, size).getlength(txt) > maxw: size -= 3
    return size


def word3d(d, cx, cy, txt, size, face, side, depth=16, glossy=True, font=None):
    """one line of extruded letters: dark side layers stepping down-right, a thick outline, then a glossy top half"""
    f = font or SFONT
    for k in range(depth, 0, -2): d.text(cx + k * 0.5, cy + k, txt, size, side, font=f, stroke=9, stroke_fill=LINE)
    d.text(cx, cy, txt, size, face, font=f, stroke=9, stroke_fill=LINE)
    if glossy:
        hl = Draw(d.w, d.h); hl.text(cx, cy, txt, size, (255, 255, 255, 120), font=f); m = Draw(d.w, d.h); m.rect(0, cy - size * 0.6, d.w, cy - size * 0.08, WHITE); d.clip(hl, m)


def stopper(lines, face, side, plate, rim, w=1000, h=None, tilt=0, lit=True, extra=None):
    """StopperText card: up to 2 lines on a rounded sticker plate with a rim; lit=False = an unlit neon tube look"""
    h = h or (300 if len(lines) == 1 else 470); d = Draw(w, h); d.rrect(14, 24, w - 14, h - 6, 52, fill=dk(plate, 0.6)); d.rrect(10, 10, w - 10, h - 22, 52, fill=plate, outline=LINE, width=16)
    d.rrect(36, 36, w - 36, h - 48, 36, outline=rim, width=8); d.ellipse(w * 0.3, 46, w * 0.22, 12, fill=(255, 255, 255, 70))
    n = len(lines)
    for k, ln in enumerate(lines):
        sz = fitf(ln, 190 if n == 1 else 160, w - 120); cy = (h - 22) * ((k + 1) / (n + 1)) + (8 if n == 2 and k == 0 else -8 if n == 2 else 0)
        if lit: word3d(d, w / 2, cy, ln, sz, face, side)
        else: d.text(w / 2, cy, ln, sz, (120, 112, 132, 255), font=SFONT, stroke=6, stroke_fill=dk(plate, 0.7))
    if extra: extra(d, w, h)
    im = d.out(); return im.rotate(tilt, resample=Image.BICUBIC, expand=True) if tilt else im


def redact(im, frac, label='TOP SECRET'):
    """black redaction bar over the right part of a stopper image; frac = covered share (1 = all covered, 0 = peeled away)"""
    im = im.copy(); w, h = im.size
    if frac <= 0: return im
    d = Draw(w, h); x0 = w * (1 - frac); d.rrect(x0 + 20, 40, w - 20, h - 60, 24, fill=(30, 26, 34, 255), outline=LINE, width=10)
    if frac < 1: d.poly([(x0 + 20, 40), (x0 + 90, 40), (x0 + 20, h - 60)], fill=(80, 76, 90, 255))     # the peeled corner curling back
    if frac > 0.55: d.text(x0 + (w - x0) / 2, h / 2 - 10, label, min(110, int(w * frac / 9)), (230, 50, 60, 255), stroke=5, stroke_fill=LINE)
    im.alpha_composite(d.out()); return im


def eyes5(d, cx, cy, s, face):
    """prop eyes: adds sleepy (closed arcs + soft smile), dizzy (spirals + wobbly mouth) and wink to the shared happy/shocked/sad"""
    if face not in ('sleepy', 'dizzy', 'wink'): return eyes(d, cx, cy, s, face)
    for sg in (-1, 1):
        ex = cx + sg * 62 * s
        if face == 'sleepy' or (face == 'wink' and sg > 0): d.arc(ex, cy + 6 * s, 30 * s, 20 * s, 20, 160, LINE, int(10 * s) + 2)
        elif face == 'dizzy': [d.arc(ex, cy, r * s, r * s, a, a + 250, LINE, int(7 * s) + 2) for r, a in ((34, 0), (22, 120), (10, 240))]
        else: d.ellipse(ex, cy, 34 * s, 40 * s, fill=WHITE, outline=LINE, width=int(9 * s) + 2); d.dot(ex + 6 * s, cy + 8 * s, 21 * s, LINE); d.dot(ex + 14 * s, cy - 6 * s, 8 * s, WHITE)
        d.ellipse(cx + sg * 112 * s, cy + 52 * s, 24 * s, 14 * s, fill=(255, 130, 130, 200))
    if face == 'dizzy': d.stroke([(cx - 40 * s, cy + 70 * s), (cx - 14 * s, cy + 58 * s), (cx + 14 * s, cy + 76 * s), (cx + 40 * s, cy + 62 * s)], LINE, int(9 * s) + 2)
    else: d.chord(cx, cy + 56 * s, 36 * s, 26 * s, 0, 180, fill=(120, 30, 40, 255), outline=LINE, width=int(8 * s) + 2)
