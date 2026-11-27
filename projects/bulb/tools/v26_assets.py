"""Shared cast helpers for videos 26-28 (last penny, fortune-cookie lottery, raised Chicago hotel): new hats (propeller beanie, knit pompom
beanie, auction headset, baker bonnet, green eyeshade visor, bucket hat, backwards cap, earmuffs, derby, striped nightcap, red bandana) and new
bodies (overalls, hoodie, waistcoat, baker whites, sweater vest, hawaiian shirt, tracksuit, raincoat, frock coat, nightshirt, cravat, suspenders).
Each video defines its own unique cast in its make_assets.py."""
from v23_assets import *
import v23_assets as V23

NEWB3 = ('overalls', 'hoodie', 'waistcoat', 'baker', 'svest', 'hawaii', 'track', 'raincoat', 'frock', 'nightie', 'cravat', 'braces2')


def head(char, expr):
    im = V23.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']; x = c.get('xhat'); hc = c.get('hatc', (200, 60, 60, 255))
    if x == 'propeller':                                     # striped kid beanie with a little propeller
        d.chord(cx, cy - R + 90, R + 6, R - 20, 180, 360, fill=hc, outline=LINE, width=14)
        for k in range(-2, 3): d.stroke([(cx + k * 55, cy - R + 90), (cx + k * 40, cy - R - 10)], c.get('hatc2', YEL), 14)
        d.rect(cx - 6, cy - R - 70, cx + 6, cy - R - 10, LINE); d.ellipse(cx - 60, cy - R - 76, 58, 18, fill=RED, outline=LINE, width=8); d.ellipse(cx + 60, cy - R - 76, 58, 18, fill=(60, 150, 240, 255), outline=LINE, width=8)
    elif x == 'beanie':                                      # knit beanie with fold + pompom
        d.chord(cx, cy - R + 100, R + 10, R - 10, 180, 360, fill=hc, outline=LINE, width=14); d.rrect(cx - R - 6, cy - R + 60, cx + R + 6, cy - R + 118, 26, fill=dk(hc, 0.82), outline=LINE, width=12)
        for k in range(-4, 5): d.stroke([(cx + k * 40, cy - R + 66), (cx + k * 40, cy - R + 112)], dk(hc, 0.65), 6)
        d.dot(cx, cy - R - 40, 50, WT); d.ellipse(cx, cy - R - 40, 50, 50, outline=LINE, width=10)
    elif x == 'headset':                                     # auctioneer headset with a mic boom
        d.arc(cx, cy - 20, R + 14, R + 14, 200, 340, LINE, 18); d.rrect(cx + R - 10, cy - 60, cx + R + 40, cy + 40, 20, fill=(40, 40, 50, 255), outline=LINE, width=8)
        d.stroke([(cx + R + 10, cy + 30), (cx + 80, cy + 120)], LINE, 10); d.dot(cx + 76, cy + 124, 22, (40, 40, 50, 255))
    elif x == 'bonnet':                                      # puffy baker bonnet (hair net cap)
        d.chord(cx, cy - R + 110, R + 30, R + 20, 180, 360, fill=hc, outline=LINE, width=14)
        for k in range(-3, 4): d.stroke([(cx + k * 50, cy - R + 100), (cx + k * 38, cy - R - 20)], dk(hc, 0.85), 5)
        d.rrect(cx - R - 20, cy - R + 84, cx + R + 20, cy - R + 124, 20, fill=dk(hc, 0.9), outline=LINE, width=10)
    elif x == 'visor':                                       # green accountant eyeshade
        d.stroke([(cx - R + 10, cy - R + 70), (cx + R - 10, cy - R + 70)], LINE, 12); d.poly([(cx - R + 10, cy - R + 50), (cx + R - 10, cy - R + 50), (cx + R + 40, cy - R + 130), (cx - R - 40, cy - R + 130)], fill=(60, 200, 120, 200), outline=LINE, width=10)
    elif x == 'bucket':                                      # floppy bucket hat with daisy
        d.chord(cx, cy - R + 70, R - 20, R - 10, 180, 360, fill=hc, outline=LINE, width=14); d.poly([(cx - R - 30, cy - R + 110), (cx - R + 30, cy - R + 50), (cx + R - 30, cy - R + 50), (cx + R + 30, cy - R + 110)], fill=hc, outline=LINE, width=12)
        d.dot(cx + 70, cy - R + 10, 26, WT); d.dot(cx + 70, cy - R + 10, 10, YEL)
    elif x == 'backcap':                                     # baseball cap worn backwards
        d.chord(cx, cy - R + 90, R + 4, R - 30, 180, 360, fill=hc, outline=LINE, width=14); d.ellipse(cx - R + 10, cy - R + 84, 90, 26, fill=dk(hc, 0.8), outline=LINE, width=10); d.dot(cx, cy - R - 2, 18, WT)
    elif x == 'earmuffs':                                    # fluffy earmuffs on a band
        d.arc(cx, cy - 10, R + 6, R + 6, 200, 340, (230, 230, 240, 255), 18)
        for sg in (-1, 1): d.dot(cx + sg * (R + 6), cy + 10, 62, hc); d.ellipse(cx + sg * (R + 6), cy + 10, 62, 62, outline=LINE, width=10)
    elif x == 'derby':                                       # 1860s derby / bowler with ribbon
        d.ellipse(cx, cy - R + 66, R + 70, 36, fill=hc, outline=LINE, width=14); d.chord(cx, cy - R + 62, R - 30, R + 10, 180, 360, fill=hc, outline=LINE, width=14)
        d.rect(cx - R + 34, cy - R + 26, cx + R - 34, cy - R + 54, c.get('band2', (150, 40, 50, 255)))
    elif x == 'nightcap':                                    # long striped nightcap with a pompom tail
        d.poly([(cx - R - 10, cy - R + 100), (cx + R + 10, cy - R + 100), (cx + R + 120, cy - R + 40), (cx + R + 170, cy - R + 60)], fill=hc, outline=LINE, width=12)
        d.chord(cx, cy - R + 104, R + 10, R - 20, 180, 360, fill=hc, outline=LINE, width=14)
        for k in range(-3, 4): d.stroke([(cx + k * 50, cy - R + 100), (cx + k * 50 + 20, cy - R - 10)], WT, 12)
        d.dot(cx + R + 170, cy - R + 70, 40, WT); d.ellipse(cx + R + 170, cy - R + 70, 40, 40, outline=LINE, width=8)
    elif x == 'bandana':                                     # red polka bandana tied at the side
        d.chord(cx, cy - R + 100, R + 6, R - 16, 180, 360, fill=hc, outline=LINE, width=14)
        for k in range(6): d.dot(cx - 150 + k * 60, cy - R + 50 - (k % 2) * 40, 10, WT)
        d.poly([(cx + R - 10, cy - R + 80), (cx + R + 70, cy - R + 50), (cx + R + 60, cy - R + 130)], fill=hc, outline=LINE, width=10)
    im.alpha_composite(d.out()); return im


def body(char):
    c = LA.NEW[char]; bs = c['body']
    if bs not in NEWB3: return V23.body(char)
    LA.NEW['_tmp'] = dict(c, body='plain'); im = LA.body('_tmp'); d = Draw(im.width, im.height); x0, y0, x1, y1, r = 85, 458, 375, 800, 115
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); t = Draw(d.w, d.h); base = c['suit']; ac = c.get('acc', RED)
    if bs == 'overalls':                                     # denim overalls over a shirt, two buttons, bib pocket
        t.rect(85, 450, 375, 540, ac); t.rrect(140, 520, 320, 800, 30, fill=base); [t.stroke([(x, 450), (x + (40 if x < 230 else -40), 540)], dk(base, 0.8), 18) for x in (120, 340)]
        [t.dot(x, 545, 14, YEL) for x in (160, 300)]; t.rrect(190, 580, 270, 650, 10, outline=dk(base, 0.7), width=6)
    elif bs == 'hoodie':                                     # hoodie with strings and a front pocket
        t.chord(230, 452, 120, 60, 0, 180, fill=dk(base, 0.82)); [t.stroke([(x, 470), (x, 590)], WT, 7) for x in (200, 260)]; t.rrect(140, 650, 320, 760, 30, outline=dk(base, 0.7), width=8)
    elif bs == 'waistcoat':                                  # white shirt, gold waistcoat, red bow tie, watch chain
        t.rect(85, 450, 375, 800, WT); t.poly([(85, 450), (200, 460), (230, 800), (85, 800)], fill=base); t.poly([(375, 450), (260, 460), (230, 800), (375, 800)], fill=base)
        [t.dot(230, y, 9, dk(base, 0.6)) for y in (600, 660, 720)]; t.poly([(200, 466), (230, 482), (200, 498)], fill=ac); t.poly([(260, 466), (230, 482), (260, 498)], fill=ac); t.arc(290, 660, 50, 30, 0, 180, YEL, 6)
    elif bs == 'baker':                                      # baker whites, flour dust, little fortune-cookie badge
        t.rect(85, 450, 375, 800, WT); [t.dot(130 + (k * 47) % 220, 500 + (k * 71) % 280, 8, (236, 230, 220, 255)) for k in range(12)]
        t.chord(300, 560, 34, 24, 180, 360, fill=(240, 190, 90, 255)); t.stroke([(170, 452), (230, 520), (290, 452)], ac, 12)
    elif bs == 'svest':                                      # sweater vest over a shirt with a tie
        t.rect(85, 450, 375, 800, WT); t.poly([(85, 470), (190, 470), (230, 560), (270, 470), (375, 470), (375, 800), (85, 800)], fill=base)
        for y in range(600, 800, 50): t.stroke([(85, y), (375, y + 30)], dk(base, 0.8), 6)
        t.poly([(220, 470), (240, 470), (246, 600), (230, 620), (214, 600)], fill=ac)
    elif bs == 'hawaii':                                     # hawaiian shirt with hibiscus flowers
        for k in range(8): x, y = 120 + (k * 83) % 230, 500 + (k * 61) % 260; [t.dot(x + 18 * math.cos(a), y + 18 * math.sin(a), 14, ac) for a in (0, 1.26, 2.51, 3.77, 5.03)]; t.dot(x, y, 8, YEL)
        t.poly([(186, 452), (274, 452), (230, 520)], fill=dk(base, 0.8))
    elif bs == 'track':                                      # tracksuit with side stripes and a zip
        for x in (100, 350): t.rect(x, 450, x + 16, 800, WT)
        t.stroke([(230, 460), (230, 800)], dk(base, 0.6), 8); t.rect(85, 450, 375, 490, ac)
    elif bs == 'raincoat':                                   # yellow raincoat with toggles
        [t.rrect(214, y, 246, y + 14, 7, fill=(120, 80, 50, 255)) for y in (540, 620, 700)]; t.stroke([(230, 470), (230, 800)], dk(base, 0.75), 6); t.poly([(150, 452), (230, 500), (310, 452)], fill=dk(base, 0.85))
    elif bs == 'frock':                                      # 1860s frock coat, waistcoat, gold watch chain
        t.rect(160, 450, 300, 800, ac); t.poly([(160, 450), (200, 450), (230, 560), (160, 620)], fill=dk(base, 0.8)); t.poly([(300, 450), (260, 450), (230, 560), (300, 620)], fill=dk(base, 0.8))
        t.arc(230, 640, 60, 40, 0, 180, YEL, 6); t.dot(230, 470, 12, WT)
    elif bs == 'nightie':                                    # striped nightshirt with a moon button
        for x in range(85, 380, 50): t.rect(x, 450, x + 22, 800, (255, 255, 255, 110))
        t.dot(230, 560, 16, YEL); t.chord(230, 452, 70, 34, 0, 180, fill=dk(base, 0.85))
    elif bs == 'cravat':                                     # senator: black coat, white shirt, big cravat
        t.poly([(170, 452), (290, 452), (230, 640)], fill=WT); t.ellipse(230, 490, 46, 30, fill=ac, outline=LINE, width=6); t.poly([(210, 500), (250, 500), (240, 580), (220, 580)], fill=ac)
    elif bs == 'braces2':                                    # rolled-sleeve shirt with suspenders
        for x in (150, 310): t.stroke([(x, 450), (x, 800)], ac, 16); t.dot(x, 700, 10, YEL)
        t.poly([(186, 452), (274, 452), (230, 500)], fill=dk(base, 0.8))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=H['lw']); im.alpha_composite(d.out()); return im


def build_cast3(names, faces=('happy', 'shocked')):
    B.human_head, B.human_body = head, body; items = []
    for ch in names: layers, fc = B.build_human(ch); items += [(ch + ' ' + e, fc[e]) for e in faces]
    return items


def coin(d, x, y, r, face='happy', col=(222, 120, 60, 255), rim=(178, 84, 40, 255)):    # glossy cute coin with a face
    d.dot(x, y, r, rim); d.dot(x, y, r * 0.86, col); d.ellipse(x, y, r * 0.86, r * 0.86, outline=dk(rim, 0.85), width=max(4, int(r * 0.04)))
    d.ellipse(x - r * 0.35, y - r * 0.45, r * 0.22, r * 0.12, fill=(255, 255, 255, 140)); d.ellipse(x, y, r, r, outline=LINE, width=max(5, int(r * 0.06)))
    if face: eyes(d, x, y + r * 0.1, r / 330, face)
