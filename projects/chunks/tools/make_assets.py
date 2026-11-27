#!/usr/bin/env python3
"""Assets for video 35: five dollars, split two ways, became a 326 million dollar ice cream company - and it was shaped by a man who can
barely taste it (Ben Cohen's anosmia -> texture -> big heavy chunks). Vermont dairy-pop world (new palette): sky-blue cow-spot dairy hills
(hook + loop), peach-lilac playground, butter-yellow mail room, mint bank vault, orange-teal 1978 roadside gas station, navy-gold corporate
skyline, lavender senses cloud world, cocoa fudge macro world. Accent strawberry #ff3d7f. Cute cast (new): Ben (curly dark hair, beard,
tie-dye tee), Jerry (soda-jerk paper cap, striped soda apron, glasses, mustache). The pint with a face is the star.
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
STRW, FUDGE, MINTC, BUT, SKYB, GRN, NAVY2, GLD, LAV, CRM, MONEY = (255, 61, 127, 255), (120, 70, 40, 255), (160, 236, 200, 255), (255, 226, 120, 255), (140, 200, 250, 255), (110, 190, 90, 255), (30, 40, 90, 255), (240, 190, 70, 255), (190, 170, 240, 255), (255, 248, 236, 255), (140, 200, 120, 255)
LA.NEW.update({
    'ben': dict(sk=1, style='curly', hair=(50, 34, 30, 255), suit=(240, 240, 250, 255), shade=(214, 214, 226, 255), body='tiedye', acc=STRW, beard=(50, 34, 30, 255)),
    'jerry': dict(sk=0, style='side', hair=(90, 60, 40, 255), suit=(240, 244, 250, 255), shade=(214, 218, 230, 255), body='soda', acc=STRW, xhat='sodacap', hatc=STRW, glasses=1, stache=(90, 60, 40, 255)),
})


def chunk(d, x, y, r, kind, face=None):                     # one glossy chunk: fudge cube, cookie-dough ball or nut
    if kind == 0: d.rrect(x - r, y - r, x + r, y + r, r * 0.3, fill=FUDGE, outline=LINE, width=8); d.rrect(x - r * 0.7, y - r * 0.8, x - r * 0.2, y - r * 0.55, 6, fill=(255, 255, 255, 90))
    elif kind == 1: d.dot(x, y, r, (230, 190, 130, 255)); d.ellipse(x, y, r, r, outline=LINE, width=8); [d.dot(x + r * 0.4 * math.cos(a), y + r * 0.4 * math.sin(a), r * 0.16, FUDGE) for a in (0.5, 2.4, 4.2)]
    else: d.ellipse(x, y, r * 1.1, r * 0.75, fill=(200, 140, 70, 255), outline=LINE, width=8); d.arc(x, y, r * 0.6, r * 0.3, 200, 340, (150, 100, 50, 255), 6)
    if face: eyes(d, x, y + r * 0.05, r / 170, face)


def pint(face='happy'):                                      # the hero pint: striped cup, overflowing scoop, chunks poking out, a face
    d = Draw(1100, 1400); d.poly([(180, 560), (920, 560), (840, 1340), (260, 1340)], fill=CRM, outline=LINE, width=16)
    for k in range(5): x = 260 + k * 150; d.poly([(x, 580), (x + 60, 580), (x + 46, 1320), (x - 4, 1320)], fill=(255, 200, 220, 255))
    d.rrect(150, 520, 950, 600, 30, fill=STRW, outline=LINE, width=12)
    for x, y, r in ((300, 420, 190), (550, 330, 230), (800, 420, 190)): d.dot(x, y, r, (255, 236, 214, 255))
    d.chord(550, 520, 420, 300, 180, 360, fill=(255, 236, 214, 255)); [d.arc(x, y, r, r, 200, 340, LINE, 12) for x, y, r in ((300, 420, 190), (550, 330, 230), (800, 420, 190))]
    for k, (x, y) in enumerate(((330, 330), (560, 200), (760, 330), (450, 460), (680, 470), (220, 480), (880, 470))): chunk(d, x, y, 52, k % 3)
    d.ellipse(420, 250, 60, 26, fill=(255, 255, 255, 140)); eyes5(d, 550, 900, 1.25, face)
    if face == 'crown': d.poly([(400, 120), (450, 20), (510, 90), (550, -10), (590, 90), (650, 20), (700, 120)], fill=GLD, outline=LINE, width=10)
    return d.out()


def bill(mode='whole'):                                      # a five-dollar bill with a cute face (split: torn in two halves, pulled apart)
    from PIL import ImageDraw
    W_, H_ = 1500, 760; h = Draw(W_, H_); h.rrect(100, 140, 1400, 640, 30, fill=MONEY, outline=LINE, width=14); h.rrect(140, 180, 1360, 600, 20, outline=(70, 130, 70, 255), width=8)
    for x, y in ((230, 250), (1270, 250), (230, 540), (1270, 540)): h.text(x, y, '5', 90, (40, 100, 50, 255))
    h.dot(900, 390, 150, (200, 236, 190, 255)); h.ellipse(900, 390, 150, 150, outline=(70, 130, 70, 255), width=8); eyes(h, 900, 380, 0.55, 'happy' if mode == 'whole' else 'shocked'); h.text(520, 390, '$5', 170, (40, 100, 50, 255), stroke=5, stroke_fill=LINE)
    whole = h.out()
    if mode == 'whole': return whole
    m = Image.new('L', (W_, H_), 0); ImageDraw.Draw(m).polygon([(0, 0), (770, 0), (720, 260), (800, 400), (730, H_), (0, H_)], fill=255)
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); im.paste(whole, (-80, 24), m); R_ = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); R_.paste(whole, (0, 0), Image.eval(m, lambda v: 255 - v))
    im.alpha_composite(R_.rotate(-5, resample=Image.BICUBIC, center=(1100, 400)).transform((W_, H_), Image.AFFINE, (1, 0, -70, 0, 1, 20))); return im


def course():                                                # the five-dollar correspondence course: certificate + envelope + $5 stamp
    d = Draw(1200, 1200); d.rrect(120, 560, 1080, 1120, 30, fill=(250, 240, 210, 255), outline=LINE, width=14); d.poly([(120, 580), (600, 880), (1080, 580)], outline=LINE, width=12)
    d.rrect(200, 80, 1000, 700, 30, fill=CRM, outline=(90, 120, 200, 255), width=16); d.text(600, 200, 'ICE CREAM', 110, NAVY2); d.text(600, 320, 'COURSE', 110, STRW); d.text(600, 450, 'PENN STATE', 80, (90, 120, 200, 255))
    d.dot(880, 600, 110, GLD); d.ellipse(880, 600, 110, 110, outline=LINE, width=10); d.text(880, 600, '$5', 100, WT, stroke=6, stroke_fill=LINE); eyes(d, 600, 960, 0.6, 'happy'); return d.out()


def stacks():                                                # $12,000: three equal money stacks (Ben, Jerry, the bank), 4,000 tags
    d = Draw(1800, 1200)
    for k, (x, tag) in enumerate(((330, 'BEN'), (900, 'JERRY'), (1470, 'BANK'))):
        for j in range(7): d.rrect(x - 220, 1060 - j * 90, x + 220, 1140 - j * 90, 16, fill=MONEY, outline=LINE, width=8); d.rect(x - 40, 1060 - j * 90, x + 40, 1140 - j * 90, (220, 236, 200, 255))
        d.rrect(x - 230, 180, x + 230, 380, 24, fill=CRM, outline=LINE, width=10); d.text(x, 240, '4,000', 96, (40, 120, 60, 255)); d.text(x, 330, tag, 64, STRW); eyes(d, x, 640, 0.5, 'happy')
    return d.out()


def station(mode='default'):                                 # the run-down 1978 gas station turned ice cream shop: peeling paint, old pumps, banner
    d = Draw(1700, 1300); d.rect(250, 420, 1450, 1260, (240, 230, 200, 255)); d.rrect(250, 420, 1450, 1260, 2, outline=LINE, width=14)
    for x, y in ((330, 520), (1300, 600), (420, 1100), (1200, 1150)): d.ellipse(x, y, 60, 30, fill=(200, 186, 150, 255))
    d.rect(180, 300, 1520, 430, (60, 150, 150, 255)); d.rrect(180, 300, 1520, 430, 6, outline=LINE, width=12); d.rrect(420, 140, 1280, 300, 30, fill=STRW, outline=LINE, width=12); d.text(850, 220, 'ICE CREAM!', 110, WT, stroke=6, stroke_fill=LINE)
    d.rrect(650, 760, 1050, 1260, 20, fill=(150, 210, 230, 255), outline=LINE, width=12); [d.rrect(x, 600, x + 220, 880, 20, fill=(170, 220, 240, 255), outline=LINE, width=10) for x in (330, 1150)]
    for x in (60, 1560): d.rrect(x - 60, 900, x + 60, 1260, 20, fill=(240, 140, 60, 255), outline=LINE, width=10); d.dot(x, 980, 36, WT); d.stroke([(x + 60, 1000), (x + 90, 1100)], LINE, 10)
    eyes(d, 850, 590, 0.6, 'happy'); d.stroke([(1000, 500), (1120, 560), (1060, 640)], (150, 130, 100, 255), 6); return d.out()


def check():                                                 # the giant $326,000,000 check from Unilever
    d = Draw(1800, 900); d.rrect(60, 80, 1740, 820, 40, fill=(236, 250, 240, 255), outline=LINE, width=16); d.rrect(100, 120, 1700, 780, 28, outline=(90, 170, 120, 255), width=8)
    d.text(380, 200, 'UNILEVER', 80, NAVY2); d.text(1380, 200, 'PAY', 70, (90, 170, 120, 255)); d.rrect(220, 300, 1580, 500, 24, fill=WT, outline=LINE, width=10); d.text(900, 400, '$326,000,000', 170, (40, 120, 60, 255), stroke=6, stroke_fill=LINE)
    d.stroke([(1100, 680), (1600, 680)], LINE, 6); d.stroke([(1150, 660), (1250, 600), (1330, 670), (1440, 610)], NAVY2, 8); eyes(d, 450, 640, 0.6, 'shocked'); return d.out()


def scale(mode='default'):                                   # balance: light FLAVOR scoop up, heavy TEXTURE chunk down
    d = Draw(1500, 1300); d.rect(720, 300, 780, 1180, (180, 150, 100, 255)); d.rrect(500, 1160, 1000, 1260, 20, fill=(150, 110, 70, 255), outline=LINE, width=10)
    d.stroke([(250, 280), (1250, 520)], (180, 150, 100, 255), 30); d.dot(750, 400, 40, GLD)
    for x, y, lab, col in ((250, 280, 'FLAVOR', (255, 200, 220, 255)), (1250, 520, 'TEXTURE', (210, 170, 120, 255))):
        d.stroke([(x, y), (x - 160, y + 330)], LINE, 6); d.stroke([(x, y), (x + 160, y + 330)], LINE, 6); d.chord(x, y + 330, 220, 90, 0, 180, fill=(200, 200, 210, 255), outline=LINE, width=10)
        d.rrect(x - 200, y + 380, x + 200, y + 470, 20, fill=col, outline=LINE, width=8); d.text(x, y + 425, lab, 64, LINE)
    d.dot(250, 560, 90, (255, 200, 220, 255)); d.ellipse(250, 560, 90, 90, outline=LINE, width=8); chunk(d, 1250, 770, 110, 0, 'happy'); return d.out()


def nose():                                                  # cute nose with smell waves crossed out
    d = Draw(1200, 1100); [d.arc(600 + k * 10, 360 - k * 90, 200 + k * 60, 60, 200, 340, (200, 160, 240, 255), 16) for k in range(3)]
    d.stroke([(300, 80), (900, 420)], STRW, 50); d.stroke([(900, 80), (300, 420)], STRW, 50)
    d.poly([(600, 480), (760, 860), (440, 860)], fill=(255, 210, 180, 255), outline=LINE, width=14); d.dot(470, 880, 90, (255, 210, 180, 255)); d.dot(730, 880, 90, (255, 210, 180, 255)); d.rrect(470, 840, 730, 960, 60, fill=(255, 210, 180, 255))
    d.ellipse(530, 900, 30, 20, fill=LINE); d.ellipse(670, 900, 30, 20, fill=LINE); d.text(900, 640, '?', 200, STRW, stroke=8, stroke_fill=LINE); eyes(d, 600, 680, 0.4, 'shocked'); return d.out()


def tongue():                                                # cute tongue with a nearly empty TASTE meter
    d = Draw(1200, 1100); d.chord(600, 300, 360, 200, 0, 180, fill=(200, 60, 80, 255), outline=LINE, width=14); d.rrect(330, 340, 870, 900, 260, fill=(255, 130, 150, 255), outline=LINE, width=14)
    d.stroke([(600, 420), (600, 720)], (220, 90, 110, 255), 12); eyes(d, 600, 560, 0.6, 'sad')
    d.rrect(200, 940, 1000, 1060, 30, fill=WT, outline=LINE, width=10); d.rrect(220, 960, 330, 1040, 20, fill=STRW); d.text(700, 1000, 'TASTE', 70, LINE); return d.out()


def blur():                                                  # regular flavors blurring together: three scoops smeared into one dizzy swirl
    im = Image.new('RGBA', (1300, 1200), (0, 0, 0, 0)); d = Draw(1300, 1200)
    for x, c in ((380, (255, 180, 200, 255)), (650, (170, 240, 200, 255)), (920, (150, 100, 70, 255))): d.dot(x, 480, 230, c)
    sm = d.out().filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(40)); im.alpha_composite(sm); d = Draw(1300, 1200)
    d.poly([(380, 680), (920, 680), (760, 1160), (540, 1160)], fill=(230, 190, 130, 255), outline=LINE, width=14); [d.stroke([(420 + k * 60, 700), (560 + k * 30, 1140)], (200, 160, 100, 255), 6) for k in range(8)]
    eyes5(d, 650, 480, 0.9, 'dizzy'); im.alpha_composite(d.out()); return im


def spoon():                                                 # giant spoon scooping chunky ice cream
    d = Draw(1100, 1500); d.rrect(500, 700, 600, 1480, 40, fill=(210, 214, 226, 255), outline=LINE, width=12); d.ellipse(550, 480, 330, 400, fill=(220, 224, 236, 255), outline=LINE, width=14)
    d.chord(550, 420, 300, 300, 180, 360, fill=(255, 236, 214, 255), outline=LINE, width=10)
    for k, (x, y) in enumerate(((420, 260), (600, 180), (700, 320), (500, 380), (360, 380))): chunk(d, x, y, 58, k % 3)
    d.ellipse(400, 560, 70, 30, fill=(255, 255, 255, 140)); eyes(d, 550, 640, 0.7, 'happy'); return d.out()


def chunks():                                                # big heavy chunks with faces, dropping in with a thud
    d = Draw(1800, 1100); d.ellipse(900, 1000, 820, 90, fill=(90, 50, 30, 120))
    for k, (x, y, r, f) in enumerate(((330, 700, 230, 'happy'), (900, 620, 290, 'shocked'), (1470, 720, 220, 'wink'))): chunk(d, x, y, r, k, f if f != 'wink' else 'happy')
    for x in (600, 1200): d.text(x, 300, '!', 160, STRW, stroke=8, stroke_fill=LINE)
    return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def dairy(path):                                             # sky-blue dairy hills: cow-spot cows, a silo, puffy clouds
    im = M.sky((120, 190, 250), (230, 248, 255), 1.0); d = Draw(W2, H2)
    for x, y in ((300, 180), (1300, 120), (2000, 220)): [d.dot(x + k * 110, y + (k % 2) * 30, 90, (255, 255, 255, 235)) for k in range(4)]
    hills(d, 640, (130, 210, 100, 255), 100, 2); hills(d, 780, (110, 190, 90, 255), 60, 3, 1.2); d.rect(1800, 420, 1900, 760, (230, 230, 240, 255)); d.chord(1850, 420, 50, 50, 180, 360, fill=(200, 80, 80, 255))
    for x, y in ((400, 760), (900, 720), (1500, 770)): d.ellipse(x, y, 80, 46, fill=WT, outline=LINE, width=6); d.dot(x - 20, y - 10, 18, LINE); d.dot(x + 30, y + 10, 14, LINE); d.ellipse(x + 80, y - 20, 34, 26, fill=WT, outline=LINE, width=6)
    fl(d, (120, 180, 100, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def playground(path):                                        # peach-lilac playground: swings, slide, round trees
    im = M.sky((200, 170, 250), (255, 220, 200), 1.0); d = Draw(W2, H2); hills(d, 760, (180, 220, 170, 255), 40, 2)
    d.stroke([(300, 400), (350, 900)], (240, 120, 120, 255), 18); d.stroke([(800, 400), (750, 900)], (240, 120, 120, 255), 18); d.stroke([(300, 400), (800, 400)], (240, 120, 120, 255), 18)
    for x in (440, 640): d.stroke([(x, 400), (x, 700)], LINE, 4); d.rect(x - 40, 700, x + 40, 716, (90, 150, 230, 255))
    d.poly([(1500, 500), (1560, 500), (1900, 900), (1820, 900)], fill=(255, 200, 80, 255)); d.rect(1460, 480, 1580, 900, (90, 150, 230, 255))
    for x in (1100, 2200): ptree(d, x, 900, 1.0, (130, 200, 140, 255))
    fl(d, (200, 170, 160, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def mailroom(path):                                          # butter-yellow mail room: pigeon-hole wall with envelopes
    im = M.sky((255, 220, 120), (255, 246, 210), 1.0); d = Draw(W2, H2); d.rect(200, 120, 2200, 860, (200, 150, 90, 255))
    for x in range(230, 2180, 150):
        for y in range(150, 840, 110): d.rect(x, y, x + 130, y + 90, (150, 100, 60, 255)); (x + y) % 3 == 0 and d.rect(x + 20, y + 30, x + 110, y + 80, (255, 250, 236, 255))
    fl(d, (190, 160, 110, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def vault(path):                                             # mint bank vault: big round door, gold bars, lamp glow
    im = M.sky((150, 230, 200), (230, 255, 240), 1.0); d = Draw(W2, H2); d.dot(1200, 480, 380, (170, 190, 190, 255)); d.ellipse(1200, 480, 380, 380, outline=(110, 130, 130, 255), width=30)
    for a in range(0, 360, 45): d.stroke([(1200, 480), (1200 + 300 * math.cos(math.radians(a)), 480 + 300 * math.sin(math.radians(a)))], (130, 150, 150, 255), 16)
    for x in (300, 1900): [d.rrect(x + j * 70, 820 - k * 40, x + j * 70 + 60, 850 - k * 40, 6, fill=GLD) for k in range(4) for j in range(4 - k)]
    fl(d, (130, 170, 160, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def road78(path):                                            # orange-teal 1978 roadside: sunset, green mountains, telephone poles
    im = M.sky((60, 160, 170), (255, 170, 90), 1.0); d = Draw(W2, H2); d.dot(1700, 640, 170, (255, 220, 140, 255)); hills(d, 680, (80, 140, 110, 255), 140, 2); hills(d, 800, (110, 160, 110, 255), 60, 3, 0.4)
    for x in range(100, W2, 400): d.rect(x, 560, x + 16, 900, (110, 80, 60, 255)); d.rect(x - 40, 580, x + 56, 592, (110, 80, 60, 255))
    d.stroke([(0, 600), (W2, 620)], LINE, 3); fl(d, (170, 150, 120, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def corp(path):                                              # navy-gold corporate skyline: glass towers, gold-lit windows
    im = M.sky((30, 40, 100), (120, 110, 190), 1.0); d = Draw(W2, H2); M.stars(d, 50, 300, 8)
    for k in range(10): x = k * 250; h = 400 + (k * 89) % 400; d.rect(x, 940 - h, x + 210, 940, (50, 60, 130, 255)); [d.rect(x + 20 + j * 46, 940 - h + 30 + i * 60, x + 50 + j * 46, 940 - h + 60 + i * 60, GLD) for j in range(4) for i in range(0, h // 60 - 1, 2)]
    fl(d, (70, 70, 120, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def senses(path):                                            # lavender senses world: soft clouds, floating sparkles, pastel rings
    im = M.sky((170, 150, 240), (250, 220, 250), 1.0); d = Draw(W2, H2)
    for x, y in ((300, 260), (1100, 160), (1900, 300)): [d.dot(x + k * 120, y + (k % 2) * 40, 100, (255, 255, 255, 200)) for k in range(4)]
    r = np.random.RandomState(9); [d.text(r.randint(0, W2), r.randint(60, 800), '*', 50, (255, 240, 255, 255)) for _ in range(30)]
    for x in (600, 1800): [d.ellipse(x, 700, 80 + k * 70, 30 + k * 26, outline=(220, 200, 255, 200), width=8) for k in range(3)]
    fl(d, (170, 150, 200, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def fudge(path):                                             # cocoa fudge macro world: caramel drips, sprinkles, wafer hills
    im = M.sky((110, 60, 40), (220, 150, 100), 1.0); d = Draw(W2, H2)
    for x in range(0, W2, 160): d.rrect(x, -40, x + 120, 140 + (x * 37) % 220, 60, fill=(240, 180, 80, 255))
    r = np.random.RandomState(4); [d.rrect(x, y, x + 50, y + 16, 8, fill=(STRW, MINTC, BUT, SKYB)[k % 4]) for k, (x, y) in enumerate(zip(r.randint(0, W2, 60), r.randint(300, 820, 60)))]
    hills(d, 780, (200, 140, 80, 255), 60, 4); fl(d, (150, 90, 60, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast5(('ben', 'jerry'))
    def spots(d, w, h): [d.dot(x, y, r, LINE) for x, y, r in ((60, 70, 26), (w - 80, h - 90, 30), (w - 60, 60, 18), (90, h - 70, 20))]
    def cnt(lines): return stopper(lines, face=STRW, side=(140, 20, 60, 255), plate=(255, 252, 244, 255), rim=(110, 200, 250, 255), h=470, extra=spots)
    roll = ['$5', '$50', '$500', '$5,000', '$50,000', '$500,000', '$5,000,000', '$50,000,000', '$326,000,000']
    stop = {('default' if k == 0 else 'r%d' % k): cnt([v]) for k, v in enumerate(roll)}; stop.update(esc=cnt(['FROM $5 TO', '$326 MILLION?!']), wait=cnt(['WHAT MADE IT?', 'WAIT FOR IT']))
    multi = dict(stop=stop, pint={'default': pint(), 'shocked': pint('shocked'), 'wink': pint('wink'), 'crown': pint('crown')}, bill={'default': bill(), 'split': bill('split')},
                 course={'default': course()}, stacks={'default': stacks()}, station={'default': station()}, check={'default': check()}, scale={'default': scale()},
                 nose={'default': nose()}, tongue={'default': tongue()}, blur={'default': blur()}, spoon={'default': spoon()}, chunks={'default': chunks()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PU, TQ, FD = (110, 60, 170, 255), (20, 130, 140, 255), (120, 70, 40, 255)
    cards = dict(friends=stamp('CHILDHOOD FRIENDS', 940, PU, 104, -3), splitc=stamp('THEY SPLIT THE COST', 960, STRW, 100, 3), k12=M.bigneon('$12,000', 'SCRAPED TOGETHER', 820, YEL, MINTC),
                 y1978=M.cal('MAY 5TH', '1978', STRW), burl=P_('BURLINGTON,', 'VERMONT', TQ, 900, 110, 120, YEL), rundown=stamp('A RUN-DOWN GAS STATION', 1000, (200, 110, 40, 255), 96, -3),
                 y22=stamp('22 YEARS LATER', 860, NAVY2, 110, 3), notmoney=stamp("ISN'T THE MONEY", 900, PU, 106, -3), anos=P_('BEN HAS', 'ANOSMIA', STRW, 860, 110, 140, YEL),
                 nosmell=stamp('NO SENSE OF SMELL', 960, PU, 102, 3), notaste=stamp('VERY LITTLE TASTE', 940, (200, 60, 90, 255), 102, -3), blurc=stamp('FLAVORS BLUR TOGETHER', 980, TQ, 96, 3),
                 texture=M.bigneon('TEXTURE', 'HE COULD FEEL IT', 820, YEL, (255, 150, 190, 255)), bite=stamp('SOMETHING TO BITE', 920, FD, 104, -3), flavorc=stamp('THEY SOLD FLAVOR', 900, (90, 120, 200, 255), 106, 3),
                 quote=P_('"ICE CREAM, TO ME,', 'IS ABOUT TEXTURE."', PU, 1000, 92, 92, YEL), famous=P_("AMERICA'S MOST FAMOUS", 'CHUNKY ICE CREAM', STRW, 1000, 84, 96, YEL), barely=stamp('CAN BARELY TASTE IT', 960, PU, 100, 3))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    M.sandtex(T('grassfl.jpg'), (120, 190, 100), (108, 176, 90)); CE.tiles(T('rubberfl.jpg'), (220, 170, 170), (206, 156, 156)); CE.tiles(T('butterfl.jpg'), (220, 190, 120), (206, 176, 108)); CE.tiles(T('vaultfl.jpg'), (140, 180, 170), (126, 166, 156))
    M.sandtex(T('dustfl.jpg'), (190, 160, 120), (176, 146, 108)); CE.tiles(T('navyfl.jpg'), (70, 70, 120), (60, 60, 108)); M.sandtex(T('lavfl.jpg'), (180, 160, 210), (166, 146, 196)); M.sandtex(T('cocoafl.jpg'), (150, 96, 64), (136, 86, 56))
    CE.tiles(T('pave.jpg'), (120, 170, 110), (108, 156, 98)); B.tex_wood(T('wood.jpg'))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(dairy=dairy, playground=playground, mailroom=mailroom, vault=vault, road78=road78, corp=corp, senses=senses, fudge=fudge)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
