"""Shared cast helpers for videos 23-25 (German chocolate cake, pinball ban, Roy Sullivan): new hats (chef toque, stetson, police cap,
flat ranger hat, headscarf, aviator shades, wide mayor hat) and new bodies (chef jacket, gingham dress, police tunic, ranger shirt,
70s plaid jacket, bow-tie suit, polka-dot dress). Each video defines its own unique cast in its make_assets.py."""
from hx_assets import *
import hx_assets as HX

NEWH = ('toque', 'stetson', 'police', 'ranger', 'scarf', 'shades', 'mayor')
NEWB2 = ('chef', 'gingham', 'police', 'ranger', 'plaid', 'bowtie', 'polka')


def head(char, expr):
    im = HX.head(char, expr); c = LA.NEW[char]; d = Draw(im.width, im.height); cx, cy, R = H['cx'], H['hcy'], H['R']; x = c.get('xhat'); hc = c.get('hatc', (200, 60, 60, 255))
    if x == 'toque':                                         # puffy white chef hat (fits the 70 px above the head)
        for dx in (-110, 0, 110): d.dot(cx + dx, cy - R - 6, 72, WT); d.ellipse(cx + dx, cy - R - 6, 72, 72, outline=LINE, width=12)
        d.rrect(cx - R + 30, cy - R - 10, cx + R - 30, cy - R + 64, 20, fill=WT, outline=LINE, width=14); d.stroke([(cx - 60, cy - R + 4), (cx - 60, cy - R + 50)], (220, 220, 226, 255), 8); d.stroke([(cx + 60, cy - R + 4), (cx + 60, cy - R + 50)], (220, 220, 226, 255), 8)
    elif x == 'stetson':                                     # cowboy hat with curled brim + band
        d.chord(cx, cy - R + 60, R + 110, 70, 180, 360, fill=hc, outline=LINE, width=14); d.ellipse(cx, cy - R + 60, R + 110, 34, fill=hc, outline=LINE, width=12)
        d.rrect(cx - R + 50, cy - R - 120, cx + R - 50, cy - R + 50, 60, fill=hc, outline=LINE, width=14); d.stroke([(cx - 40, cy - R - 110), (cx, cy - R - 70), (cx + 40, cy - R - 110)], LINE, 10)
        d.rect(cx - R + 54, cy - R + 4, cx + R - 54, cy - R + 36, c.get('band2', (250, 250, 245, 255)))
    elif x == 'police':                                      # 1940s peaked police cap with a gold badge
        d.ellipse(cx, cy - R + 10, R + 20, 70, fill=(40, 50, 100, 255), outline=LINE, width=14); d.rect(cx - R + 30, cy - R + 20, cx + R - 30, cy - R + 70, (30, 36, 70, 255))
        d.ellipse(cx + 20, cy - R + 84, R - 20, 26, fill=(20, 20, 28, 255), outline=LINE, width=10); d.dot(cx, cy - R + 10, 30, YEL); d.ellipse(cx, cy - R + 10, 30, 30, outline=LINE, width=8)
    elif x == 'ranger':                                      # flat-brim park ranger hat, green band + pine badge
        d.ellipse(cx, cy - R + 60, R + 120, 44, fill=(120, 150, 90, 255), outline=LINE, width=14); d.rrect(cx - R + 70, cy - R - 110, cx + R - 70, cy - R + 54, 40, fill=(120, 150, 90, 255), outline=LINE, width=14)
        d.rect(cx - R + 74, cy - R + 6, cx + R - 74, cy - R + 40, (60, 90, 50, 255)); d.poly([(cx, cy - R - 40), (cx - 30, cy - R + 10), (cx + 30, cy - R + 10)], fill=(240, 200, 80, 255), outline=LINE, width=6)
    elif x == 'scarf':                                       # polka headscarf knotted on top
        d.chord(cx, cy - R + 110, R + 10, R - 10, 180, 360, fill=hc, outline=LINE, width=14)
        for k in range(5): d.dot(cx - 140 + k * 70, cy - R + 20 - (k % 2) * 50, 14, WT)
        for sg in (-1, 1): d.ellipse(cx + sg * 50, cy - R - 60, 50, 30, fill=hc, outline=LINE, width=10)
    elif x == 'shades':                                      # big 70s aviator shades pushed up on the head
        for sg in (-1, 1): d.ellipse(cx + sg * 70, cy - R + 60, 56, 44, fill=(110, 80, 50, 230), outline=(200, 170, 80, 255), width=10); d.dot(cx + sg * 70 - 18, cy - R + 46, 10, WT)
        d.stroke([(cx - 18, cy - R + 50), (cx + 18, cy - R + 50)], (200, 170, 80, 255), 8)
    elif x == 'mayor':                                       # wide black hat
        d.ellipse(cx, cy - R + 56, R + 90, 40, fill=(30, 28, 34, 255), outline=LINE, width=14); d.chord(cx, cy - R + 54, R - 30, R - 20, 180, 360, fill=(30, 28, 34, 255), outline=LINE, width=14)
        d.rect(cx - R + 36, cy - R + 16, cx + R - 36, cy - R + 46, (90, 80, 90, 255))
    im.alpha_composite(d.out()); return im


def body(char):
    c = LA.NEW[char]; bs = c['body']
    if bs not in NEWB2: return HX.body(char)
    LA.NEW['_tmp'] = dict(c, body='plain'); im = LA.body('_tmp'); d = Draw(im.width, im.height); x0, y0, x1, y1, r = 85, 458, 375, 800, 115
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); t = Draw(d.w, d.h); base = c['suit']; ac = c.get('acc', RED)
    if bs == 'chef':                                         # double-breasted chef jacket + neckerchief
        for x in (190, 270):
            for y in (540, 620, 700): t.dot(x, y, 10, dk(base, 0.7))
        t.poly([(186, 452), (274, 452), (230, 510)], fill=ac); t.stroke([(230, 470), (300, 800)], dk(base, 0.85), 6)
    elif bs == 'gingham':                                    # check dress with a white ruffle collar
        for x in range(85, 380, 40): t.rect(x, 450, x + 20, 800, (255, 255, 255, 90))
        for y in range(450, 800, 40): t.rect(85, y, 380, y + 20, (255, 255, 255, 90))
        for k in range(5): t.dot(170 + k * 30, 470, 20, WT)
    elif bs == 'police':                                     # navy tunic, gold buttons, badge, belt
        for y in (520, 600, 680): t.dot(230, y, 9, YEL)
        t.poly([(130, 520), (166, 520), (166, 560), (148, 574), (130, 560)], fill=YEL, outline=LINE, width=5); t.rect(85, 700, 375, 732, (30, 28, 34, 255)); t.rect(214, 704, 246, 728, YEL)
    elif bs == 'ranger':                                     # ranger shirt: pockets, arm patch, badge
        for sg in (-1, 1): t.rrect(230 + sg * 72 - 40, 520, 230 + sg * 72 + 40, 590, 8, outline=dk(base, 0.7), width=6)
        t.poly([(300, 500), (330, 500), (330, 530), (315, 540), (300, 530)], fill=YEL, outline=LINE, width=5); t.dot(110, 520, 26, (110, 80, 50, 255)); t.dot(110, 520, 12, (120, 170, 90, 255))
        t.poly([(186, 452), (274, 452), (230, 500)], fill=(240, 230, 200, 255))
    elif bs == 'plaid':                                      # 70s plaid jacket, wide collar, turtleneck
        for x in range(85, 380, 60): t.rect(x, 450, x + 14, 800, (255, 230, 160, 120))
        for y in range(450, 800, 60): t.rect(85, y, 380, y + 14, (90, 40, 20, 110))
        t.rect(196, 452, 264, 800, ac); for_ = [t.poly([(196, 452), (150, 470), (196, 600)], fill=dk(base, 0.8), outline=LINE, width=6), t.poly([(264, 452), (310, 470), (264, 600)], fill=dk(base, 0.8), outline=LINE, width=6)]
    elif bs == 'bowtie':                                     # suit with a big bow tie
        t.poly([(186, 452), (274, 452), (230, 560)], fill=WT); t.poly([(194, 470), (230, 488), (194, 506)], fill=ac, outline=LINE, width=6); t.poly([(266, 470), (230, 488), (266, 506)], fill=ac, outline=LINE, width=6)
        t.dot(230, 488, 12, ac)
        for sg in (-1, 1): t.stroke([(230 + sg * 44, 456), (230 + sg * 14, 640)], dk(base, 0.7), 10)
    elif bs == 'polka':                                      # polka-dot dress
        for k in range(30): t.dot(100 + (k * 53) % 270, 470 + (k * 37) % 320, 14, (255, 255, 255, 200))
        t.chord(230, 452, 70, 36, 0, 180, fill=dk(base, 0.8))
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=H['lw']); im.alpha_composite(d.out()); return im


def build_cast2(names, faces=('happy', 'shocked')):
    B.human_head, B.human_body = head, body; items = []
    for ch in names: layers, fc = B.build_human(ch); items += [(ch + ' ' + e, fc[e]) for e in faces]
    return items


def bolt(d, x, y, s, col=(255, 236, 90, 255)):               # chunky cartoon lightning bolt
    pts = [(x, y), (x + 60 * s, y), (x + 20 * s, y + 110 * s), (x + 80 * s, y + 110 * s), (x - 30 * s, y + 300 * s), (x + 5 * s, y + 160 * s), (x - 50 * s, y + 160 * s)]
    d.poly(pts, fill=col, outline=LINE, width=max(4, int(10 * s)))
