#!/usr/bin/env python3
"""Assets for video 27: 110 people won the lottery with the same numbers - all from one fortune cookie (one wrong number paid them all in full).
Lucky neon red-jade night world: purple neon draw studio (hook + loop), forest chalkboard classroom, sunny confetti rooftop, olive night office,
teal investigation room, navy glowing map room, golden bakery macro table, orange-brick Queens factory at golden hour, red-steel cookie line,
navy lantern street, crimson-gold jackpot plaza. Cute cast (new): baker (puffy bonnet, baker whites), lottery official (green eyeshade, sweater
vest), three winners (bucket hat + hawaiian shirt, backwards cap + tracksuit, earmuffs + raincoat). usage: make_assets.py <project> <font>"""
import os, math
import numpy as np
from PIL import Image
import assets_base as B
import gimli_assets as G
import catseyes_assets as CE
import mco_assets as M
from v26_assets import *

ROOT = B.ROOT
JADE, CRIM, GOLD, NAVY, CK = (30, 230, 160, 255), (220, 40, 60, 255), (255, 200, 40, 255), (30, 34, 80, 255), (236, 178, 90, 255)
LA.NEW.update({
    'baker': dict(sk=1, style='bob', hair=(40, 30, 30, 255), suit=WT, shade=(220, 220, 226, 255), body='baker', acc=CRIM, band=CRIM, xhat='bonnet', hatc=(255, 236, 240, 255)),
    'offl': dict(sk=0, style='part', hair=(150, 110, 70, 255), suit=(120, 90, 190, 255), shade=(96, 70, 160, 255), body='svest', acc=CRIM, xhat='visor', glasses=1),
    'w1': dict(sk=2, style='curly', hair=(30, 24, 24, 255), suit=(255, 140, 80, 255), shade=(224, 112, 60, 255), body='hawaii', acc=(255, 240, 120, 255), xhat='bucket', hatc=(120, 200, 240, 255)),
    'w2': dict(sk=0, style='spiky', hair=(230, 180, 80, 255), suit=JADE, shade=(20, 190, 130, 255), body='track', acc=CRIM, xhat='backcap', hatc=CRIM),
    'w3': dict(sk=1, style='pony', hair=(120, 60, 40, 255), suit=(255, 214, 60, 255), shade=(224, 182, 40, 255), body='raincoat', xhat='earmuffs', hatc=(255, 130, 180, 255)),
})


def ball(d, x, y, r, n, col=CRIM, face=None):                # glossy lottery ball with a number band
    d.dot(x, y, r, WT); d.chord(x, y, r, r, 200, 340, fill=col); d.chord(x, y, r, r, 20, 160, fill=col); d.dot(x, y, r * 0.55, WT); d.ellipse(x, y, r, r, outline=LINE, width=max(5, int(r * 0.07)))
    d.text(x, y + r * 0.04, str(n), int(r * 0.62), LINE); d.ellipse(x - r * 0.4, y - r * 0.55, r * 0.2, r * 0.1, fill=(255, 255, 255, 200))


def bmach(mode='default'):                                   # ball machine: glass globe, tumbling balls, cute base face (spin / pop42)
    d = Draw(1100, 1500); d.dot(550, 520, 460, (200, 236, 255, 90)); d.ellipse(550, 520, 460, 460, outline=LINE, width=16); d.ellipse(400, 300, 120, 60, fill=(255, 255, 255, 120))
    r = np.random.RandomState(4 if mode == 'default' else 8); cols = [CRIM, JADE, GOLD, (120, 90, 230, 255), (60, 150, 240, 255)]
    for k in range(9): ball(d, r.randint(250, 850), r.randint(420, 860), 80, r.randint(1, 69), cols[k % 5])
    if mode == 'spin': [d.arc(550, 520, 380 - k * 40, 380 - k * 40, 200 + k * 30, 280 + k * 30, WT, 12) for k in range(3)]
    d.rrect(250, 950, 850, 1450, 60, fill=(120, 60, 200, 255), outline=LINE, width=16); d.rect(470, 960, 630, 1010, (90, 40, 160, 255)); eyes(d, 550, 1180, 0.9, 'shocked' if mode != 'default' else 'happy')
    if mode == 'pop42': d.dot(550, 60, 140, (255, 250, 200, 140)); ball(d, 550, 70, 110, 42, GOLD)
    return d.out()


def tix():                                                   # wall of identical tickets
    d = Draw(1600, 1200)
    for j in range(4):
        for i in range(4):
            x, y = 200 + i * 400, 160 + j * 290; d.rrect(x - 180, y - 120, x + 180, y + 120, 20, fill=(255, 250, 236, 255), outline=LINE, width=10); d.rect(x - 180, y - 120, x + 180, y - 70, CRIM)
            d.text(x, y - 95, 'LOTTO', 40, WT); d.text(x, y + 10, '22 28 32', 56, LINE); d.text(x, y + 70, '33 39', 56, LINE)
    return d.out()


def board(x_=False):                                         # chalkboard: EXPECTED 4 OR 5 WINNERS (x_: red X over it)
    d = Draw(1600, 1100); d.rrect(40, 40, 1560, 1000, 30, fill=(150, 100, 60, 255), outline=LINE, width=16); d.rect(100, 100, 1500, 940, (40, 90, 70, 255))
    d.text(800, 250, 'EXPECTED:', 110, (240, 240, 230, 255)); d.text(800, 470, '4 OR 5', 220, YEL); d.text(800, 680, 'WINNERS', 110, (240, 240, 230, 255))
    for k in range(5): d.dot(320 + k * 90, 860, 30, (240, 240, 230, 255))
    d.rect(300, 1000, 1300, 1060, (120, 80, 50, 255)); eyes(d, 1300, 860, 0.5, 'shocked' if x_ else 'happy')
    if x_: d.stroke([(300, 200), (1300, 840)], CRIM, 50); d.stroke([(1300, 200), (300, 840)], CRIM, 50)
    return d.out()


def balls6(wrong=False):                                     # the first five numbers lit + a 6th "?" ball (wrong: 40 with a red X vs 42)
    d = Draw(1800, 700)
    for k, n in enumerate((22, 28, 32, 33, 39)): x = 160 + k * 300; d.dot(x, 330, 150, (255, 250, 180, 110)); ball(d, x, 330, 120, n, JADE); d.text(x, 560, 'OK', 70, JADE, stroke=5, stroke_fill=LINE)
    if wrong: ball(d, 1660, 330, 120, 40, CRIM); d.stroke([(1560, 230), (1760, 430)], CRIM, 26); d.stroke([(1760, 230), (1560, 430)], CRIM, 26); d.text(1660, 560, '42?', 80, CRIM, stroke=5, stroke_fill=LINE)
    else: d.dot(1660, 330, 120, (120, 90, 200, 255)); d.ellipse(1660, 330, 120, 120, outline=LINE, width=10); d.text(1660, 335, '?', 150, GOLD, stroke=6, stroke_fill=LINE)
    return d.out()


def check(amt='$100,000'):                                   # giant novelty check
    d = Draw(1700, 800); d.rrect(30, 30, 1670, 770, 40, fill=(250, 250, 236, 255), outline=LINE, width=16); d.rect(30, 30, 1670, 150, JADE); d.text(850, 92, 'LOTTERY WINNER', 70, WT, stroke=4, stroke_fill=LINE)
    d.text(330, 260, 'PAY TO:', 60, LINE); d.stroke([(500, 290), (1600, 290)], LINE, 6); d.rrect(900, 360, 1600, 560, 20, fill=(255, 250, 200, 255), outline=LINE, width=10); d.text(1250, 462, amt, 120, CRIM)
    d.stroke([(150, 650), (700, 650)], LINE, 6); eyes(d, 450, 470, 0.6, 'happy'); return d.out()


def calc(boom=False):                                        # office calculator (boom: papers fly, steam puff, shocked)
    d = Draw(1000, 1300); d.rrect(150, 300, 850, 1250, 60, fill=(80, 80, 100, 255), outline=LINE, width=16); d.rrect(220, 380, 780, 560, 20, fill=(170, 220, 160, 255), outline=LINE, width=10)
    d.text(500, 472, 'ERR' if boom else '19,000,000', 90 if boom else 60, LINE)
    for j in range(3):
        for i in range(4): d.rrect(240 + i * 135, 640 + j * 170, 350 + i * 135, 760 + j * 170, 20, fill=(240, 240, 246, 255) if i < 3 else CRIM, outline=LINE, width=8)
    eyes(d, 500, 300, 0.7, 'shocked' if boom else 'happy')
    if boom:
        for x, y, a in ((150, 120, -20), (850, 100, 15), (500, 40, 5)): d.poly([(x - 70, y - 50), (x + 70, y - 60), (x + 80, y + 50), (x - 60, y + 60)], fill=WT, outline=LINE, width=8)
        for x, y, r in ((300, 220, 60), (700, 220, 60)): d.dot(x, y, r, (230, 236, 246, 230))
    return d.out()


def hq():                                                    # lottery HQ tower with a neon LOTTERY sign
    d = Draw(1200, 1600); d.rect(250, 300, 950, 1560, (70, 60, 120, 255)); d.stroke([(250, 300), (950, 300)], LINE, 12)
    for j in range(6):
        for i in range(4): d.rect(300 + i * 160, 600 + j * 150, 400 + i * 160, 700 + j * 150, (255, 230, 140, 255) if (i + j) % 3 else (90, 80, 140, 255))
    d.rrect(150, 120, 1050, 460, 40, fill=(40, 20, 60, 255), outline=JADE, width=20); d.text(600, 290, 'LOTTERY', 170, JADE, stroke=8, stroke_fill=LINE); [d.dot(200 + k * 80, 140, 14, GOLD) for k in range(11)]
    return d.out()


def cork():                                                  # suspicion corkboard: photos, red strings, a giant magnifier
    d = Draw(1500, 1200); d.rrect(40, 40, 1460, 1000, 30, fill=(200, 150, 100, 255), outline=LINE, width=16); pts = [(300, 250), (1100, 220), (700, 600), (1200, 750), (300, 780)]
    for a in pts:
        for b in pts: d.stroke([a, b], CRIM, 6)
    for k, (x, y) in enumerate(pts): d.rrect(x - 110, y - 80, x + 110, y + 80, 10, fill=WT, outline=LINE, width=8); d.dot(x, y - 80, 18, CRIM); d.text(x, y, '?', 90, LINE)
    d.ellipse(1150, 1000, 170, 170, fill=(200, 236, 255, 120), outline=LINE, width=24); d.stroke([(1270, 1120), (1420, 1180)], (120, 80, 50, 255), 40); return d.out()


def pc():                                                    # retro computer with a glitching screen
    d = Draw(1300, 1200); d.rrect(150, 100, 1150, 850, 50, fill=(220, 214, 196, 255), outline=LINE, width=16); d.rrect(240, 180, 1060, 700, 20, fill=(20, 30, 60, 255), outline=LINE, width=10)
    for y, c in ((260, (255, 60, 120, 255)), (380, (60, 240, 255, 255)), (500, (255, 240, 80, 255)), (620, (60, 255, 140, 255))): d.rect(260 + (y % 7) * 20, y, 1040 - (y % 5) * 30, y + 40, c)
    d.rrect(380, 380, 920, 520, 10, fill=CRIM, outline=WT, width=8); d.text(650, 452, 'ERROR', 100, WT); d.rrect(350, 850, 950, 1000, 30, fill=(200, 194, 176, 255), outline=LINE, width=12)
    d.rrect(200, 1020, 1100, 1160, 30, fill=(230, 226, 210, 255), outline=LINE, width=12); eyes(d, 650, 780, 0.45, 'shocked'); return d.out()


US = [(80, 210), (320, 170), (700, 180), (1000, 200), (1250, 210), (1400, 150), (1520, 120), (1650, 170), (1610, 270), (1700, 310), (1570, 430), (1510, 560), (1570, 700), (1480, 830), (1380, 800),
      (1300, 760), (1160, 850), (1090, 970), (990, 890), (820, 890), (700, 990), (600, 890), (480, 850), (380, 770), (200, 710), (120, 560), (60, 380)]


def usmap(route=False):                                      # cartoon US map: IDAHO + TENNESSEE pins (route: glowing lines converge on QUEENS)
    d = Draw(1800, 1100); d.poly(US, fill=(60, 120, 110, 255), outline=JADE, width=14)
    for x in range(200, 1700, 250): d.stroke([(x, 160), (x - 40, 980)], (80, 150, 136, 255), 4)
    pins = dict(IDAHO=(380, 330), TENNESSEE=(1180, 640), QUEENS=(1560, 340))
    if route:
        for p in ('IDAHO', 'TENNESSEE'): d.stroke([pins[p], pins['QUEENS']], GOLD, 22); d.stroke([pins[p], pins['QUEENS']], LINE, 4)
        d.dot(1560, 340, 90, (255, 240, 150, 160))
    for nm, (x, y) in pins.items():
        if nm == 'QUEENS' and not route: continue
        d.poly([(x, y + 60), (x - 50, y - 20), (x + 50, y - 20)], fill=CRIM, outline=LINE, width=8); d.dot(x, y - 40, 50, CRIM); d.ellipse(x, y - 40, 50, 50, outline=LINE, width=8); d.dot(x, y - 40, 18, WT)
        d.text(x, y + 120, nm if nm != 'QUEENS' else 'QUEENS, NY', 70, WT, stroke=6, stroke_fill=LINE)
    return d.out()


def cookie(mode='default'):                                  # fortune cookie hero (crack: split with a slip popping out; gold: perfect, glowing)
    d = Draw(1300, 1000)
    if mode == 'gold': d.dot(650, 560, 480, (255, 240, 160, 140))
    c = (250, 200, 80, 255) if mode == 'gold' else CK; dkc = dk(c, 0.8)
    if mode == 'crack':
        d.chord(380, 620, 280, 230, 120, 330, fill=c, outline=LINE, width=14); d.chord(920, 620, 280, 230, 210, 420, fill=c, outline=LINE, width=14)
        d.rrect(420, 330, 900, 450, 10, fill=WT, outline=LINE, width=8); d.text(660, 392, '22 28 32 33 39 40', 46, CRIM); [d.stroke([(650 + sg * 260, 250), (650 + sg * 330, 180)], GOLD, 14) for sg in (-1, 1)]
        eyes(d, 650, 760, 0.7, 'shocked')
    else:
        d.chord(650, 640, 520, 340, 180, 360, fill=c, outline=LINE, width=16); d.chord(650, 640, 520, 160, 0, 180, fill=dkc, outline=LINE, width=16); d.stroke([(650, 330), (650, 640)], dkc, 12)
        d.ellipse(430, 470, 120, 50, fill=(255, 255, 255, 110)); eyes(d, 650, 540, 0.8, 'happy')
        if mode == 'gold': d.ellipse(650, 200, 220, 50, outline=GOLD, width=30); [d.poly([(x, y - 40), (x + 12, y - 12), (x + 40, y), (x + 12, y + 12), (x, y + 40), (x - 12, y + 12), (x - 40, y), (x - 12, y - 12)], fill=WT) for x, y in ((180, 300), (1120, 320), (1000, 880))]
    return d.out()


def factory():                                               # Queens cookie factory facade: brick, water tower, WONTON FOOD sign, chimney puffs
    d = Draw(1600, 1400); d.rect(150, 560, 1450, 1380, (190, 80, 60, 255)); d.stroke([(150, 560), (1450, 560)], LINE, 12)
    for i in range(5): win(d, 220 + i * 250, 900, 380 + i * 250, 1100, (255, 220, 140, 255))
    d.rect(1150, 200, 1260, 560, (150, 70, 60, 255)); [d.dot(1205 + k * 50, 160 - k * 50, 60 + k * 10, (240, 240, 246, 220)) for k in range(3)]
    d.chord(420, 300, 140, 60, 180, 360, fill=(120, 90, 70, 255), outline=LINE, width=10); d.rect(290, 300, 550, 470, (150, 110, 80, 255)); [d.stroke([(x, 470), (x, 560)], LINE, 10) for x in (310, 530)]
    d.rrect(200, 600, 1400, 820, 30, fill=CRIM, outline=GOLD, width=16); d.text(800, 680, 'WONTON FOOD', 120, GOLD, stroke=6, stroke_fill=LINE); d.text(800, 780, 'QUEENS, NEW YORK', 60, WT)
    d.rrect(700, 1180, 900, 1380, 20, fill=(90, 60, 50, 255), outline=LINE, width=10); return d.out()


def belt():                                                  # conveyor of endless cookies, one with a face
    d = Draw(1800, 800); d.rrect(40, 450, 1760, 600, 60, fill=(150, 160, 180, 255), outline=LINE, width=14); [d.dot(x, 525, 40, (110, 120, 140, 255)) for x in range(140, 1700, 180)]
    for k, x in enumerate(range(170, 1700, 200)): d.chord(x, 440, 90, 70, 180, 360, fill=CK, outline=LINE, width=8); d.chord(x, 440, 90, 30, 0, 180, fill=dk(CK, 0.8), outline=LINE, width=8)
    eyes(d, 970, 400, 0.35, 'happy'); return d.out()


def sprint():                                                # slip printer spitting numbered paper slips
    d = Draw(1300, 1300); d.rrect(200, 500, 1100, 1200, 50, fill=(60, 160, 140, 255), outline=LINE, width=16); d.rrect(300, 560, 1000, 640, 20, fill=LINE)
    for k in range(4): x, y = 650 + (k - 1.5) * 160, 400 - k * 90; d.rrect(x - 200, y - 50, x + 200, y + 50, 8, fill=WT, outline=LINE, width=6); d.text(x, y, '22 28 32', 50, CRIM)
    eyes(d, 650, 900, 0.8, 'happy'); [d.dot(x, 1100, 26, c) for x, c in ((350, GOLD), (450, CRIM))]; return d.out()


def slip(n=0, wrong=False):                                  # giant fortune slip: numbers appear one by one (n), wrong: 40 circled vs 42
    d = Draw(1800, 700); d.rrect(40, 120, 1760, 580, 30, fill=(255, 252, 240, 255), outline=LINE, width=14); d.text(900, 200, 'LUCKY NUMBERS', 70, CRIM)
    for k, v in enumerate((22, 28, 32, 33, 39, 40)):
        x = 220 + k * 272
        if k < n or wrong: d.text(x, 400, str(v), 170, LINE if not (wrong and k == 5) else CRIM, stroke=4, stroke_fill=WT)
        else: d.stroke([(x - 90, 480), (x + 90, 480)], (200, 190, 170, 255), 10)
    if wrong: d.ellipse(1580, 400, 150, 120, outline=CRIM, width=18); d.rrect(1300, 600, 1780, 700, 20, fill=GOLD, outline=LINE, width=8); d.text(1540, 650, 'NEEDED 42', 70, LINE)
    return d.out()


def bowl():                                                  # big bowl of numbered balls, one hopping out
    d = Draw(1400, 1100); r = np.random.RandomState(6); cols = [CRIM, JADE, GOLD, (120, 90, 230, 255)]
    for k in range(10): ball(d, r.randint(330, 1070), r.randint(380, 560), 90, r.randint(1, 69), cols[k % 4])
    d.chord(700, 520, 520, 460, 0, 180, fill=(80, 160, 230, 255), outline=LINE, width=16); d.ellipse(700, 520, 520, 60, outline=LINE, width=12); [d.stroke([(300 + k * 200, 640), (330 + k * 190, 900)], (120, 190, 250, 255), 14) for k in range(5)]
    ball(d, 900, 160, 100, 33, GOLD); eyes(d, 700, 760, 0.8, 'happy'); return d.out()


def pie(sliced=False):                                       # one golden JACKPOT pie (sliced: 110 thin slivers)
    d = Draw(1400, 1000); d.ellipse(700, 560, 620, 340, fill=(220, 150, 60, 255), outline=LINE, width=16); d.ellipse(700, 520, 560, 290, fill=(255, 210, 90, 255), outline=LINE, width=10)
    if sliced:
        for k in range(36): a = math.radians(k * 10); d.stroke([(700, 520), (700 + 560 * math.cos(a), 520 + 290 * math.sin(a))], LINE, 5)
        eyes(d, 700, 520, 0.7, 'shocked')
    else: d.rrect(380, 430, 1020, 600, 30, fill=CRIM, outline=LINE, width=10); d.text(700, 518, 'JACKPOT', 110, GOLD); eyes(d, 700, 720, 0.6, 'happy')
    return d.out()


def bags():                                                  # money bags, each full, cheering
    d = Draw(1600, 1000)
    for k, x in enumerate((300, 800, 1300)):
        d.ellipse(x, 640, 250, 300, fill=(200, 170, 110, 255), outline=LINE, width=14); d.poly([(x - 90, 360), (x + 90, 360), (x + 150, 260), (x - 150, 260)], fill=(200, 170, 110, 255), outline=LINE, width=12)
        d.rect(x - 100, 350, x + 100, 390, CRIM); d.text(x, 620, '$', 220, (100, 160, 80, 255), stroke=6, stroke_fill=LINE); eyes(d, x, 800, 0.45, 'happy')
    return d.out()


def crowdt():                                                # tiny chibi extras all holding the same ticket
    d = Draw(1800, 900); cols = [(255, 140, 80, 255), JADE, (120, 90, 230, 255), (255, 214, 60, 255), (255, 120, 170, 255)]
    for k in range(8):
        x = 140 + k * 220; y = 470 + (k % 2) * 70; c = cols[k % 5]
        d.rrect(x - 95, y + 70, x + 95, y + 360, 60, fill=c, outline=LINE, width=10); d.dot(x, y, 95, (255, 220, 190, 255) if k % 3 else (190, 130, 90, 255)); d.ellipse(x, y, 95, 95, outline=LINE, width=10)
        d.chord(x, y - 10, 98, 86, 180, 360, fill=(40 + k * 22, 30, 30, 255)); eyes(d, x, y + 16, 0.4, 'shocked' if k % 2 else 'happy')
        d.rrect(x + 40, y - 240, x + 200, y - 140, 10, fill=WT, outline=LINE, width=6); d.rect(x + 40, y - 240, x + 200, y - 215, CRIM); d.stroke([(x + 70, y + 120), (x + 110, y - 140)], LINE, 10)
    return d.out()


def qball():                                                 # open loop: a spot-lit 6th ball with "?"
    d = Draw(800, 1000); d.poly([(300, 0), (500, 0), (720, 980), (80, 980)], fill=(255, 255, 220, 70)); d.dot(400, 640, 260, (120, 90, 200, 255)); d.ellipse(400, 640, 260, 260, outline=LINE, width=14)
    d.text(400, 650, '?', 320, GOLD, stroke=10, stroke_fill=LINE); return d.out()


# ------------------------------------------------------------------ set pictures (no text on them)
def studio(path):                                            # purple neon draw studio: bulb arches, beams, LED floor glow
    im = sky((40, 10, 70), (150, 40, 160), 1.0); d = Draw(W2, H2)
    for x in (500, 1200, 1900): d.poly([(x - 40, 0), (x + 40, 0), (x + 380, 940), (x - 380, 940)], fill=(255, 120, 230, 40))
    for k in range(3): d.arc(1200, 1000, 700 + k * 260, 700 + k * 200, 180, 360, (255, 60, 200, 255) if k % 2 else JADE, 16)
    for a in range(180, 361, 12): r_ = math.radians(a); d.dot(1200 + 960 * math.cos(r_), 1000 + 800 * math.sin(r_), 14, (255, 240, 180, 255))
    fl(d, (60, 20, 90, 255)); im.alpha_composite(d.out()); glow(im, 1200, 820, 520, (255, 120, 230, 90), 120); im.convert('RGB').save(path)


def classroom(path):                                         # mustard classroom wall, posters, globe, window
    im = sky((230, 170, 60), (250, 210, 120), 1.0); d = Draw(W2, H2); win(d, 1800, 140, 2200, 560, (150, 210, 255, 255))
    for x, c in ((300, CRIM), (560, JADE), (820, (120, 90, 230, 255))): d.rrect(x - 100, 160, x + 100, 420, 10, fill=c, outline=LINE, width=10); d.dot(x, 290, 50, WT)
    d.dot(1500, 760, 110, (80, 160, 230, 255)); d.ellipse(1500, 760, 110, 110, outline=LINE, width=10); d.rect(1490, 870, 1510, 940, LINE)
    fl(d, (170, 120, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def rooftop(path):                                           # sunny rooftop party: teal sky, string lights, confetti, water towers
    im = sky((60, 190, 220), (200, 240, 250), 1.0); d = Draw(W2, H2); r = np.random.RandomState(3)
    for k, x in enumerate(range(0, W2, 180)): h_ = 200 + (k * 113) % 260; d.rect(x, 900 - h_, x + 160, 940, (240, 230, 214, 255) if k % 2 else (220, 200, 190, 255))
    d.stroke([(0, 140), (600, 240), (1200, 160), (1800, 250), (W2, 150)], LINE, 6); [d.dot(x, 200 + 40 * math.sin(x / 200), 16, (255, 240, 120, 255)) for x in range(40, W2, 90)]
    for _ in range(160): x, y = r.randint(0, W2), r.randint(0, 900); d.rect(x, y, x + 18, y + 10, [CRIM, JADE, GOLD, (120, 90, 230, 255)][r.randint(0, 4)])
    fl(d, (180, 160, 150, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def office(path):                                            # olive night office: file cabinets, rainy window, desk lamp glow
    im = sky((90, 100, 50), (150, 150, 80), 1.0); d = Draw(W2, H2); win(d, 900, 120, 1500, 560, (40, 50, 100, 255)); [d.stroke([(x, 160), (x - 20, 220)], (180, 220, 255, 200), 4) for x in range(940, 1480, 50)]
    for x in (200, 420, 1900, 2120): d.rrect(x - 90, 420, x + 90, 940, 10, fill=(130, 140, 110, 255), outline=LINE, width=8); [d.rect(x - 30, y, x + 30, y + 16, LINE) for y in (520, 680, 840)]
    fl(d, (110, 100, 70, 255)); im.alpha_composite(d.out()); glow(im, 1700, 600, 300, (255, 230, 150, 120), 80); im.convert('RGB').save(path)


def invest(path):                                            # teal investigation room with venetian-blind light stripes
    im = sky((20, 80, 90), (40, 140, 140), 1.0); d = Draw(W2, H2)
    for k in range(9): y = 120 + k * 70; d.poly([(1500, y), (2300, y + 80), (2300, y + 110), (1500, y + 30)], fill=(220, 255, 240, 60))
    d.rrect(200, 200, 700, 600, 20, fill=(30, 60, 70, 255), outline=(120, 200, 190, 255), width=10)
    fl(d, (40, 70, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def maproom(path):                                           # navy map room: grid glow, star field
    im = sky((14, 20, 60), (30, 60, 120), 1.0); d = Draw(W2, H2); stars(d, 80, 900, 5)
    for x in range(0, W2, 160): d.stroke([(x, 0), (x, 940)], (60, 120, 200, 70), 3)
    for y in range(0, 940, 160): d.stroke([(0, y), (W2, y)], (60, 120, 200, 70), 3)
    fl(d, (20, 30, 70, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def bakery(path):                                            # golden bakery macro: warm bokeh, shelves of jars
    im = sky((150, 70, 20), (255, 180, 80), 1.0); d = Draw(W2, H2); r = np.random.RandomState(2)
    for _ in range(40): d.dot(r.randint(0, W2), r.randint(0, 800), r.randint(30, 90), (255, 230, 160, 70))
    fl(d, (170, 100, 50, 255)); im.alpha_composite(d.out()); glow(im, 1200, 500, 600, (255, 220, 150, 90), 140); im.convert('RGB').save(path)


def queens(path):                                            # golden-hour Queens: orange sky, brick rows, elevated train
    im = sky((255, 140, 70), (255, 220, 150), 1.0); d = Draw(W2, H2); d.dot(1900, 640, 160, (255, 240, 190, 255))
    for k, x in enumerate(range(0, W2, 220)): h_ = 300 + (k * 97) % 240; d.rect(x, 940 - h_, x + 200, 940, (170 + (k % 3) * 20, 80, 60, 255)); [win(d, x + 30 + j * 80, 940 - h_ + 50, x + 80 + j * 80, 940 - h_ + 120, (255, 220, 140, 255)) for j in range(2)]
    d.rect(0, 560, W2, 600, (70, 60, 70, 255)); [d.rect(x, 600, x + 30, 940, (70, 60, 70, 255)) for x in range(100, W2, 400)]; d.rrect(300, 500, 1100, 566, 16, fill=(200, 210, 220, 255), outline=LINE, width=8)
    fl(d, (120, 90, 80, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


def line(path):                                              # cookie line interior: red steel, oven glows, hanging lamps
    im = sky((150, 30, 40), (220, 80, 70), 1.0); d = Draw(W2, H2)
    for x in (300, 1200, 2100): d.rrect(x - 220, 300, x + 220, 860, 30, fill=(180, 186, 200, 255), outline=LINE, width=12); d.rrect(x - 150, 420, x + 150, 640, 20, fill=(255, 150, 60, 255), outline=LINE, width=10)
    for x in (750, 1650): d.stroke([(x, 0), (x, 140)], LINE, 6); d.chord(x, 180, 100, 70, 180, 360, fill=(60, 60, 70, 255)); d.dot(x, 190, 30, (255, 240, 180, 255))
    fl(d, (110, 40, 40, 255)); im.alpha_composite(d.out()); [glow(im, x, 530, 240, (255, 170, 80, 110), 60) for x in (300, 1200, 2100)]; im.convert('RGB').save(path)


def lanterns(path):                                          # navy lantern street: red lanterns, moon, rooftops
    im = sky((40, 40, 110), (150, 90, 170), 1.0); d = Draw(W2, H2); stars(d, 60, 500, 11); d.dot(1900, 200, 90, (255, 246, 210, 255))
    for k, x in enumerate(range(0, W2, 260)): h_ = 340 + (k % 3) * 70; d.rect(x, 940 - h_, x + 240, 940, (120, 80, 150, 255)); d.poly([(x - 20, 940 - h_), (x + 120, 880 - h_), (x + 260, 940 - h_)], fill=(210, 60, 80, 255)); [win(d, x + 40 + j * 100, 960 - h_ + 40, x + 100 + j * 100, 960 - h_ + 120, (255, 220, 140, 255)) for j in range(2)]
    d.stroke([(0, 260), (W2, 300)], LINE, 5)
    for x in range(120, W2, 220): y = 260 + 40 * x / W2 + 50; d.ellipse(x, y + 60, 50, 64, fill=CRIM, outline=LINE, width=8); d.rect(x - 30, y - 4, x + 30, y + 8, GOLD)
    fl(d, (40, 30, 60, 255)); im.alpha_composite(d.out()); [glow(im, x, 360, 90, (255, 120, 90, 110), 30) for x in range(120, W2, 220)]; glow(im, 1900, 200, 200, (255, 240, 200, 90), 60); im.convert('RGB').save(path)


def plaza(path):                                             # crimson-gold jackpot plaza at sunset with fireworks
    im = sky((180, 30, 70), (255, 190, 80), 1.0); d = Draw(W2, H2)
    for x, y, c in ((500, 260, GOLD), (1300, 180, JADE), (2000, 300, (255, 120, 200, 255))):
        for a in range(0, 360, 30): r_ = math.radians(a); d.stroke([(x + 40 * math.cos(r_), y + 40 * math.sin(r_)), (x + 150 * math.cos(r_), y + 150 * math.sin(r_))], c, 10)
    for x in range(0, W2, 300): d.rect(x + 60, 620, x + 120, 940, (240, 200, 150, 255)); d.rect(x + 40, 600, x + 140, 640, (250, 220, 170, 255))
    fl(d, (160, 60, 60, 255)); im.alpha_composite(d.out()); im.convert('RGB').save(path)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = build_cast3(('baker', 'offl', 'w1', 'w2', 'w3'))
    multi = dict(bmach={k: bmach(k) for k in ('default', 'spin', 'pop42')}, tix={'default': tix()}, board={'default': board(), 'x': board(True)}, balls6={'default': balls6(), 'wrong': balls6(True)},
                 check={'default': check(), 'k500': check('$500,000')}, calc={'default': calc(), 'boom': calc(True)}, hq={'default': hq()}, cork={'default': cork()}, pc={'default': pc()},
                 usmap={'default': usmap(), 'route': usmap(True)}, cookie={k: cookie(k) for k in ('default', 'crack', 'gold')}, factory={'default': factory()}, belt={'default': belt()},
                 sprint={'default': sprint()}, slip={'default': slip(0), **{'n%d' % k: slip(k) for k in range(1, 7)}, 'wrong': slip(6, True)}, bowl={'default': bowl()},
                 pie={'default': pie(), 'sliced': pie(True)}, bags={'default': bags()}, crowdt={'default': crowdt()}, qball={'default': qball()})
    for nm, faces in multi.items(): G.build_card(nm, faces); items += [(nm + ' ' + k, im) for k, im in faces.items()]
    PL, NV, RD_ = (110, 40, 150, 255), (40, 50, 110, 255), (170, 30, 50, 255)
    cards = dict(hookc=M.bigneon('110 WINNERS', 'SAME NUMBERS!', 980, YEL, JADE),
                 night=stamp('SAME NIGHT!', 760, NV, 150, -4),
                 math=stamp("THAT'S JUST MATH", 940, (40, 90, 70, 255), 110, 3),
                 nobody=stamp('NOBODY BUDGETED!', 940, RD_, 110, -3),
                 scam=stamp('SCAM?!', 560, RD_, 190, -5), glitch=stamp('GLITCH?!', 640, PL, 180, 4),
                 oneplace=P_('ONE PLACE', 'TRACED!', NV, 860, 140, 150, YEL),
                 fortune=M.bigneon('FORTUNE', 'COOKIE!', 860, YEL, JADE),
                 m4=M.bigneon('4 MILLION', 'A DAY!', 880, YEL, (255, 150, 80, 255)),
                 years=stamp('<< YEARS EARLIER', 940, PL, 110, -3),
                 standout=stamp('JUST TO STAND OUT!', 980, (200, 90, 40, 255), 104, 3),
                 random=stamp('AT RANDOM!', 760, (40, 120, 190, 255), 150, -4),
                 need42=M.bigneon('NEEDED', '42!', 700, YEL, (255, 120, 120, 255)),
                 twist=M.bigneon("HERE'S THE", 'TWIST...', 900, YEL, JADE),
                 split=P_('PERFECT =', 'SPLIT 110 WAYS', PL, 980, 140, 130, YEL),
                 wrongn=stamp('ONE WRONG NUMBER!', 960, RD_, 110, -3),
                 paid=M.bigneon('PAID IN', 'FULL!', 760, YEL, JADE))
    cards_out(ROOT, cards, multi, items)
    T = lambda n: os.path.join(ROOT, 'textures', n)
    CE.tiles(T('ledfloor.jpg'), (90, 30, 120), (76, 24, 104)); B.tex_wood(T('wood.jpg')); CE.tiles(T('roof.jpg'), (200, 180, 170), (186, 166, 156)); CE.tiles(T('carpet.jpg'), (120, 110, 80), (106, 96, 70))
    CE.tiles(T('lino.jpg'), (50, 90, 100), (42, 78, 88)); CE.tiles(T('navy.jpg'), (30, 40, 90), (24, 34, 78)); M.sandtex(T('table.jpg'), (190, 120, 60), (174, 106, 52)); CE.tiles(T('pave.jpg'), (140, 110, 100), (126, 98, 88))
    CE.tiles(T('steel.jpg'), (150, 150, 166), (136, 136, 150)); CE.tiles(T('cobble.jpg'), (130, 100, 150), (116, 88, 136)); CE.tiles(T('plaza.jpg'), (200, 120, 90), (184, 106, 78))
    G.sky(os.path.join(ROOT, 'bg', 'sky.jpg')); Pp = lambda n: os.path.join(ROOT, 'props', n)
    SETS = dict(studio=studio, classroom=classroom, rooftop=rooftop, office=office, invest=invest, maproom=maproom, bakery=bakery, queens=queens, line=line, lanterns=lanterns, plaza=plaza)
    for n, f in SETS.items(): f(Pp(n + '.png')); items.append((n, Image.open(Pp(n + '.png'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
