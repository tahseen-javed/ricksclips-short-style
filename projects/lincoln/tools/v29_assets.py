"""Shared cast helpers for videos 29-31 (Lincoln the wrestler, the Pepsi jet, Mount Rushmore's name): new hats (stovepipe, coonskin cap,
soldier kepi, straw hat, 90s headphones, jet helmet, homburg, feathered slouch, hard hat with lamp, beret), a chin-curtain beard and
freckles, and new bodies (frontier linen, buckskin fringe, soldier coat, patched shirt, black coat, grunge flannel, flight suit, judge robe,
pinstripe lawyer, tweed historian, dusty sculptor smock, driller shirt). Each video defines its own unique cast in its make_assets.py."""
from v26_assets import *
import v26_assets as V26

NEWB4 = ('linen', 'fringe', 'soldier', 'patched', 'blackcoat', 'grunge', 'flight', 'judge', 'lawyer', 'tweed', 'dusty', 'driller')


def head(char, expr):
    im = V26.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']; x = c.get('xhat2'); hc = c.get('hatc', (200, 60, 60, 255))
    if c.get('beard'):                                       # chin-curtain beard along the jaw, mouth stays free
        bc = c['beard']; d.arc(cx, cy + 6, R - 6, R - 4, 18, 162, bc, 54); d.chord(cx, cy + R - 30, 70, 46, 0, 180, fill=bc)
    if c.get('freckles'):
        for sg in (-1, 1): [d.dot(cx + sg * (96 + k * 22), cy + 64 + (k % 2) * 16, 7, (200, 120, 80, 255)) for k in range(3)]
    if x == 'stovepipe':                                     # tall stovepipe hat with a band (fits the canvas: sits low on the brow)
        d.rrect(cx - R + 50, 8, cx + R - 50, cy - R + 96, 16, fill=(34, 30, 40, 255), outline=LINE, width=14); d.rect(cx - R + 54, cy - R + 50, cx + R - 54, cy - R + 84, c.get('band2', (90, 70, 60, 255)))
        d.ellipse(cx, cy - R + 100, R + 46, 30, fill=(34, 30, 40, 255), outline=LINE, width=12); d.rect(cx - R + 76, 30, cx - R + 96, cy - R + 40, (255, 255, 255, 80))
    elif x == 'coonskin':                                    # fur cap with tufts and a striped tail
        d.chord(cx, cy - R + 110, R + 12, R + 6, 180, 360, fill=hc, outline=LINE, width=14)
        for k in range(-4, 5): d.stroke([(cx + k * 40, cy - R + 96), (cx + k * 40 + 14, cy - R + 128)], dk(hc, 0.7), 10)
        for k in range(5): d.rrect(cx + R - 20 + (k % 2) * 6, cy - R + 110 + k * 50, cx + R + 46, cy - R + 160 + k * 50, 22, fill=dk(hc, 0.55) if k % 2 else (236, 214, 180, 255), outline=LINE, width=8)
    elif x == 'kepi':                                        # blue soldier kepi with a black visor and brass badge
        d.poly([(cx - R + 30, cy - R + 96), (cx - R + 60, cy - R - 20), (cx + R - 40, cy - R - 40), (cx + R - 20, cy - R + 96)], fill=hc, outline=LINE, width=14)
        d.chord(cx - 20, cy - R + 100, R - 10, 46, 0, 180, fill=(30, 30, 40, 255), outline=LINE, width=10); d.dot(cx, cy - R + 30, 22, YEL); d.ellipse(cx, cy - R + 30, 22, 22, outline=LINE, width=6)
    elif x == 'straw':                                       # frayed straw farm hat
        d.ellipse(cx, cy - R + 90, R + 80, 40, fill=hc, outline=LINE, width=12); d.chord(cx, cy - R + 86, R - 40, R - 30, 180, 360, fill=hc, outline=LINE, width=12)
        d.rect(cx - R + 44, cy - R + 50, cx + R - 44, cy - R + 76, (200, 70, 60, 255)); [d.stroke([(cx + k * 36, cy - R + 70), (cx + k * 40, cy - R + 120)], dk(hc, 0.75), 5) for k in range(-6, 7)]
    elif x == 'headphones':                                  # chunky 90s headphones with orange foam
        d.arc(cx, cy - 10, R + 16, R + 16, 200, 340, (60, 60, 70, 255), 22)
        for sg in (-1, 1): d.rrect(cx + sg * (R + 6) - 40, cy - 40, cx + sg * (R + 6) + 40, cy + 70, 30, fill=hc, outline=LINE, width=10)
    elif x == 'pilot':                                       # white jet helmet, visor up, star
        d.chord(cx, cy - R + 150, R + 24, R + 34, 180, 360, fill=WT, outline=LINE, width=14); d.chord(cx, cy - R + 70, R - 20, 60, 180, 360, fill=(255, 190, 60, 220), outline=LINE, width=10)
        d.text(cx - 110, cy - R + 110, '*', 120, hc, stroke=5, stroke_fill=LINE); d.rect(cx - R - 20, cy - R + 140, cx - R + 20, cy + 40, (220, 220, 230, 255))
    elif x == 'homburg':                                     # grey homburg with a centre dent and ribbon
        d.ellipse(cx, cy - R + 74, R + 60, 30, fill=hc, outline=LINE, width=12); d.rrect(cx - R + 40, cy - R - 30, cx + R - 40, cy - R + 76, 40, fill=hc, outline=LINE, width=14)
        d.stroke([(cx, cy - R - 20), (cx, cy - R + 20)], dk(hc, 0.7), 10); d.rect(cx - R + 44, cy - R + 36, cx + R - 44, cy - R + 64, c.get('band2', (40, 40, 50, 255)))
    elif x == 'feather':                                     # floppy slouch hat with a big feather
        d.poly([(cx - R - 60, cy - R + 110), (cx - R + 40, cy - R + 40), (cx + R - 40, cy - R + 40), (cx + R + 70, cy - R + 100)], fill=hc, outline=LINE, width=12)
        d.chord(cx, cy - R + 60, R - 40, R - 40, 180, 360, fill=hc, outline=LINE, width=12)
        d.poly([(cx + 60, cy - R + 50), (cx + 170, cy - R - 60), (cx + 200, cy - R - 40), (cx + 90, cy - R + 60)], fill=c.get('plume', (230, 60, 60, 255)), outline=LINE, width=8)
    elif x == 'hardhat':                                     # yellow hard hat with a ridge and a headlamp
        d.chord(cx, cy - R + 110, R + 10, R, 180, 360, fill=hc, outline=LINE, width=14); d.ellipse(cx, cy - R + 112, R + 46, 24, fill=hc, outline=LINE, width=10)
        d.stroke([(cx, cy - R + 14), (cx, cy - R + 100)], dk(hc, 0.8), 18); d.dot(cx, cy - R + 70, 30, (255, 250, 210, 255)); d.ellipse(cx, cy - R + 70, 30, 30, outline=LINE, width=8)
    elif x == 'beret':                                       # floppy artist beret with a stalk
        d.ellipse(cx - 20, cy - R + 50, R + 30, 70, fill=hc, outline=LINE, width=14); d.rect(cx - 30, cy - R - 40, cx - 10, cy - R - 8, LINE)
    im.alpha_composite(d.out()); return im


def body(char):
    c = LA.NEW[char]; bs = c['body']
    if bs not in NEWB4: return V26.body(char)
    LA.NEW['_tmp'] = dict(c, body='plain'); im = LA.body('_tmp'); d = Draw(im.width, im.height); x0, y0, x1, y1, r = 85, 458, 375, 800, 115
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); t = Draw(d.w, d.h); base = c['suit']; ac = c.get('acc', RED)
    if bs == 'linen':                                        # frontier linen shirt, open collar, rope belt, patch
        t.poly([(190, 452), (270, 452), (230, 530)], fill=dk(base, 0.8)); t.rect(85, 700, 375, 730, ac); [t.stroke([(x, 700), (x + 12, 730)], dk(ac, 0.7), 5) for x in range(95, 375, 24)]
        t.rrect(280, 600, 340, 660, 8, fill=dk(base, 0.88))
    elif bs == 'fringe':                                     # buckskin jacket with fringe and a red neckerchief
        t.rect(85, 450, 375, 800, base); [t.stroke([(x, 600), (x - 6, 660)], dk(base, 0.7), 8) for x in range(100, 380, 26)]; t.poly([(180, 452), (280, 452), (230, 540)], fill=ac)
        t.stroke([(230, 540), (230, 800)], dk(base, 0.75), 8)
    elif bs == 'soldier':                                    # navy soldier coat, white cross belts, brass buttons
        t.stroke([(100, 460), (360, 790)], WT, 24); t.stroke([(360, 460), (100, 790)], WT, 24); [t.dot(230, y, 12, YEL) for y in (520, 640, 760)]; t.rect(85, 450, 375, 480, ac)
    elif bs == 'patched':                                    # patched farm shirt with a blue neckerchief
        t.rrect(110, 620, 180, 690, 6, fill=ac); t.rrect(270, 540, 330, 600, 6, fill=(250, 220, 120, 255)); t.poly([(180, 452), (280, 452), (230, 520)], fill=(70, 120, 210, 255))
    elif bs == 'blackcoat':                                  # black frock coat, white shirt, black bow tie
        t.poly([(170, 452), (290, 452), (230, 680)], fill=WT); t.poly([(200, 466), (230, 482), (200, 498)], fill=LINE); t.poly([(260, 466), (230, 482), (260, 498)], fill=LINE)
        [t.dot(230, y, 8, (60, 60, 70, 255)) for y in (560, 620)]
    elif bs == 'grunge':                                     # open plaid flannel over a smiley tee
        t.rect(170, 450, 290, 800, (250, 250, 245, 255)); t.dot(230, 600, 40, YEL); [t.dot(230 + sg * 14, 590, 5, LINE) for sg in (-1, 1)]; t.arc(230, 606, 20, 12, 20, 160, LINE, 5)
        for y in range(470, 800, 60): [t.rect(x, y, x + 85, y + 16, dk(base, 0.7)) for x in (85, 290)]
        for x in (110, 140, 310, 340): t.rect(x, 450, x + 12, 800, dk(base, 0.7))
    elif bs == 'flight':                                     # green flight suit, zip, wing patch, name tag
        t.stroke([(230, 460), (230, 800)], dk(base, 0.6), 8); t.rrect(120, 520, 210, 570, 8, fill=YEL); t.poly([(260, 530), (340, 520), (320, 560), (270, 556)], fill=ac)
    elif bs == 'judge':                                      # black judge robe with a white jabot
        t.poly([(196, 452), (264, 452), (250, 560), (210, 560)], fill=WT); [t.stroke([(200, y), (260, y)], (220, 220, 230, 255), 4) for y in (480, 510, 540)]
        [t.stroke([(x, 600), (x, 800)], dk(base, 0.7), 6) for x in (140, 320)]
    elif bs == 'lawyer':                                     # pinstripe suit, tie, pocket square
        for x in range(95, 375, 26): t.stroke([(x, 450), (x, 800)], (255, 255, 255, 50), 3)
        t.poly([(186, 452), (274, 452), (230, 560)], fill=WT); t.poly([(220, 470), (240, 470), (246, 600), (230, 620), (214, 600)], fill=ac); t.poly([(290, 520), (340, 520), (330, 550), (300, 550)], fill=WT)
    elif bs == 'tweed':                                      # tweed jacket, round collar, bow tie
        for k in range(40): t.dot(95 + (k * 53) % 280, 460 + (k * 37) % 340, 6, dk(base, 0.82))
        t.poly([(190, 452), (270, 452), (230, 500)], fill=WT); t.poly([(206, 470), (230, 482), (206, 494)], fill=ac); t.poly([(254, 470), (230, 482), (254, 494)], fill=ac)
    elif bs == 'dusty':                                      # sculptor smock with granite dust and a scarf
        for k in range(14): t.dot(110 + (k * 61) % 250, 520 + (k * 43) % 260, 10, (220, 220, 225, 200))
        t.poly([(170, 452), (290, 452), (300, 500), (160, 500)], fill=ac); t.poly([(250, 490), (290, 490), (280, 600), (256, 600)], fill=ac)
    elif bs == 'driller':                                    # work shirt, tool belt with a hammer
        t.rect(85, 700, 375, 740, (120, 80, 50, 255)); t.rect(280, 700, 300, 790, (150, 150, 160, 255)); t.rect(262, 690, 318, 712, (90, 90, 100, 255)); [t.dot(x, 520, 10, WT) for x in (200, 260)]
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=H['lw']); im.alpha_composite(d.out()); return im


def build_cast4(names, faces=('happy', 'shocked')):
    for n in names:                                          # the new hats live in 'xhat2' so the older modules draw no hat of their own
        c = LA.NEW[n]
        if c.get('xhat') in ('stovepipe', 'coonskin', 'kepi', 'straw', 'headphones', 'pilot', 'homburg', 'feather', 'hardhat', 'beret'): c['xhat2'] = c.pop('xhat')
    B.human_head, B.human_body = head, body; items = []
    for ch in names: layers, fc = B.build_human(ch); items += [(ch + ' ' + e, fc[e]) for e in faces]
    return items
