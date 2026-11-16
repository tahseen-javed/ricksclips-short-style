#!/usr/bin/env python3
"""Assets for video 03 (the Viking-horns myth), drawn in code with the channel builders.
Reuses video 02's cast code (gimli_assets.py) so mom, dad and tech look identical, and adds Vikings,
Wagner, the costume designer, an opera singer, a farmer, peat cutters, the real helmets, an opera
stage, a longship and cards.   usage: make_assets.py <project folder> [font.ttf]"""
import os, math
import numpy as np
from PIL import Image, ImageDraw
import assets_base as B
import gimli_assets as G
from assets_base import Draw, LINE, WHITE, BLUSH, H, bez

ROOT = B.ROOT; RED, GOLD, GREEN = G.RED, G.GOLD, G.GREEN
IRON, IRON_D, BRONZE, HORN = (156, 162, 178, 255), (112, 118, 136, 255), (214, 156, 72, 255), (246, 236, 214, 255)
VS = dict(skin=(246, 214, 190, 255), sh=(222, 184, 160, 255), base=(150, 96, 60, 255), shade=(118, 72, 44, 255), beard=(214, 110, 52, 255), belt=1)
NEW = {
    'vik':   dict(VS, hat='horned'), 'vikr': dict(VS, hat='round'),
    'foe':   dict(skin=(214, 168, 130, 255), sh=(186, 140, 104, 255), hat='round', base=(70, 120, 90, 255), shade=(50, 92, 68, 255), beard=(70, 52, 46, 255), belt=1),
    'wag':   dict(skin=(244, 220, 200, 255), sh=(220, 190, 168, 255), hat='beret', base=(52, 48, 70, 255), shade=(36, 32, 52, 255), cravat=1),
    'dop':   dict(skin=(232, 196, 160, 255), sh=(206, 166, 130, 255), hat='tophat', base=(126, 70, 140, 255), shade=(98, 50, 112, 255), tape=1, stache=(90, 60, 40, 255)),
    'sing':  dict(skin=(248, 220, 200, 255), sh=(226, 190, 170, 255), hat='round', base=(190, 196, 214, 255), shade=(150, 156, 178, 255), hair=(242, 196, 80, 255), gown=1),
    'farm':  dict(skin=(236, 200, 170, 255), sh=(210, 170, 140, 255), hat='flat', base=(70, 100, 170, 255), shade=(52, 76, 136, 255), straps=1),
    'cut1':  dict(skin=(226, 186, 150, 255), sh=(198, 156, 120, 255), hat='flat', base=(150, 124, 96, 255), shade=(118, 96, 72, 255), straps=1),
    'cut2':  dict(skin=(180, 126, 92, 255), sh=(150, 100, 70, 255), hat='flat2', base=(120, 132, 146, 255), shade=(92, 102, 114, 255), straps=1),
}
NEW['singh'] = dict(NEW['sing'], hat='horned')


def horns_on(d, cx, y0, s=1.0):
    for sg in (-1, 1):
        pts = (bez((cx + sg * 110 * s, y0 + 30 * s), (cx + sg * 250 * s, y0 + 30 * s), (cx + sg * 268 * s, y0 - 70 * s), (cx + sg * 212 * s, y0 - 116 * s)) +
               bez((cx + sg * 212 * s, y0 - 116 * s), (cx + sg * 226 * s, y0 - 50 * s), (cx + sg * 196 * s, y0 - 6 * s), (cx + sg * 112 * s, y0 - 4 * s)))
        d.poly(pts, fill=HORN, outline=LINE, width=H['lw'])
        d.stroke([(cx + sg * 200 * s, y0 + 6 * s), (cx + sg * 238 * s, y0 - 40 * s)], (222, 206, 176, 255), 10)


def hat(d, char):
    cx, lw, k = H['cx'], H['lw'], NEW[char]['hat']
    if k in ('horned', 'round'):
        if k == 'horned': horns_on(d, cx, 126)
        d.chord(cx, 152, 196, 136, 180, 360, fill=IRON, outline=LINE, width=lw)
        d.rect(cx - 190, 126, cx + 190, 150, IRON_D); d.stroke([(cx, 20), (cx, 150)], IRON_D, 14)
        for x in range(cx - 160, cx + 170, 54): d.dot(x, 138, 7, (210, 214, 226, 255))
        d.stroke([(cx - 196, 152), (cx + 196, 152)], LINE, lw)
        if k == 'round':                                     # Gjermundbu "spectacle" guard
            for sg in (-1, 1): d.arc(cx + sg * 62, 264, 50, 48, 180, 360, IRON_D, 14)
            d.stroke([(cx, 152), (cx, 230)], IRON_D, 16)
    elif k == 'beret':
        d.ellipse(cx + 24, 104, 196, 74, fill=(40, 36, 56, 255), outline=LINE, width=lw); d.dot(cx + 40, 34, 14, LINE)
    elif k == 'tophat':
        d.rrect(cx - 108, 4, cx + 108, 146, 16, fill=(44, 40, 60, 255), outline=LINE, width=lw)
        d.rect(cx - 104, 104, cx + 104, 130, RED); d.ellipse(cx, 148, 186, 30, fill=(44, 40, 60, 255), outline=LINE, width=lw)
    else:                                                    # flat cap
        col = (120, 90, 64, 255) if k == 'flat' else (96, 100, 110, 255)
        d.chord(cx, 150, 190, 110, 180, 360, fill=col, outline=LINE, width=lw); d.ellipse(cx + 70, 150, 150, 26, fill=col, outline=LINE, width=lw)


def head(char, expr):
    c = NEW[char]; d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']
    if 'hair' in c:                                          # long braids behind the head
        for sg in (-1, 1): d.rrect(cx + sg * 170 - 44, cy - 20, cx + sg * 170 + 44, 470, 44, fill=c['hair'], outline=LINE, width=lw)
    d.ellipse(cx, cy, R, R, fill=c['skin'], outline=LINE, width=lw); B.cel_shadow(d, cx, cy, R - 9, c['sh'], c['skin'])
    if 'beard' in c: d.chord(cx, cy + 36, R - 4, 168, 0, 180, fill=c['beard'], outline=LINE, width=lw)
    hat(d, char)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    d.ellipse(cx - 122, cy + 40, 30, 17, fill=BLUSH); d.ellipse(cx + 122, cy + 40, 30, 17, fill=BLUSH)
    B.eyes(d, L, Rr, expr, c['skin']); B.brows(d, L, Rr, expr, ey - 50)
    my = cy + 74
    for key in ('stache', 'beard'):
        if key in c:
            for sg in (-1, 1): d.stroke(bez((cx, my - 34), (cx + sg * 30, my - 50), (cx + sg * 58, my - 40), (cx + sg * 66, my - 22)), c[key], 24)
            my += 12
    B.mouth(d, cx, my, expr)
    if expr == 'nervous': G.sweat(d, cx + 150, cy - 30)
    return d.out()


def body(char):
    c = NEW[char]; d = Draw(H['W'], H['H']); x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE); d.rrect(x0, y0, x1, y1, r, fill=c['base'])
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=c['base']); d.clip(sh, mask)
    t = Draw(d.w, d.h)
    if c.get('belt'):
        t.poly([(196, 450), (264, 450), (230, 530)], fill=c['shade']); t.rect(x0, 684, x1, 718, (92, 58, 36, 255)); t.rrect(212, 680, 248, 722, 6, fill=GOLD)
    if c.get('cravat'): t.poly([(186, 452), (274, 452), (230, 540)], fill=WHITE); t.dot(230, 560, 12, GOLD)
    if c.get('tape'):
        for x in (176, 284): t.stroke([(x, 456), (x + (6 if x > 230 else -6), 790)], (250, 214, 70, 255), 22)
    if c.get('gown'):
        for x in (190, 270): t.dot(x, 540, 38, (226, 230, 242, 255)); t.ellipse(x, 540, 38, 38, outline=LINE, width=5)
        t.rect(x0, 640, x1, 664, GOLD)
    if c.get('straps'):
        for x in (176, 284): t.stroke([(x, 452), (x, 800)], (60, 44, 40, 255), 14); t.dot(x, 600, 9, GOLD)
    d.clip(t, mask); d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()


# ------------------------------------------------------------------ stickers, cards, props
def helm_real():
    d = Draw(520, 460)
    d.chord(260, 300, 220, 230, 180, 360, fill=IRON, outline=LINE, width=14); d.stroke([(260, 74), (260, 300)], IRON_D, 22)
    d.stroke([(44, 300), (476, 300)], IRON_D, 24); d.stroke([(40, 300), (480, 300)], LINE, 8)
    for sg in (-1, 1): d.ellipse(260 + sg * 70, 352, 58, 50, outline=IRON_D, width=22); d.ellipse(260 + sg * 70, 352, 70, 62, outline=LINE, width=6)
    d.stroke([(260, 300), (260, 420)], IRON_D, 24)
    for x in range(70, 460, 50): d.dot(x, 300, 8, (214, 218, 230, 255))
    d.arc(200, 190, 90, 80, 200, 260, (236, 240, 248, 220), 14)
    return d.out()


def helm_bronze():
    d = Draw(600, 560); horns_on(d, 300, 300, 1.25)
    d.chord(300, 380, 190, 190, 180, 360, fill=BRONZE, outline=LINE, width=14)
    d.stroke([(110, 380), (490, 380)], LINE, 10)
    for sg in (-1, 1): d.dot(300 + sg * 70, 300, 34, (238, 196, 110, 255)); d.ellipse(300 + sg * 70, 300, 34, 34, outline=LINE, width=7)
    d.poly([(300, 250), (322, 300), (300, 340), (278, 300)], fill=(238, 196, 110, 255), outline=LINE, width=6)
    for k in range(5): d.dot(170 + k * 65, 360, 7, (246, 214, 140, 255))
    return d.out()


def horns_card():
    d = Draw(620, 300); horns_on(d, 310, 210, 1.1); return d.out()


def axe():
    d = Draw(260, 460); d.rrect(116, 40, 144, 450, 12, fill=(150, 100, 60, 255), outline=LINE, width=8)
    d.poly([(140, 60)] + bez((140, 60), (250, 20), (260, 160), (240, 200)) + [(140, 170)], fill=IRON, outline=LINE, width=10)
    d.stroke([(236, 70), (252, 170)], (226, 230, 240, 255), 8); return d.out()


def spade():
    d = Draw(180, 470); d.rrect(78, 10, 102, 330, 10, fill=(150, 100, 60, 255), outline=LINE, width=7); d.rrect(50, 6, 130, 34, 12, fill=(150, 100, 60, 255), outline=LINE, width=7)
    d.poly([(40, 320), (140, 320), (134, 430), (90, 462), (46, 430)], fill=IRON, outline=LINE, width=9); return d.out()


def notes():
    d = Draw(320, 320)
    for x, y in ((90, 250), (230, 210)): d.ellipse(x, y, 44, 34, fill=GOLD, outline=LINE, width=9); d.stroke([(x + 38, y - 6), (x + 38, y - 180)], LINE, 12)
    d.poly([(128, 70), (268, 30), (268, 74), (128, 114)], fill=LINE); return d.out()


def wtag(txt, w, col=RED, size=84):
    d = Draw(w, 220); d.rrect(14, 14, w - 14, 206, 30, fill=col, outline=LINE, width=14); d.rrect(38, 38, w - 38, 182, 18, outline=(255, 240, 240, 255), width=6)
    d.text(w / 2, 114, txt, size, WHITE, stroke=6, stroke_fill=LINE); return d.out()


def big_card(big, small, col, w=680):
    d = G.card(w, 420); d.text(w / 2, 170, big, 150, col, stroke=8, stroke_fill=LINE); d.text(w / 2, 326, small, 62, LINE); return d.out()


def tick(d, x, y, ok):
    d.dot(x, y, 40, GREEN if ok else RED); d.ellipse(x, y, 40, 40, outline=LINE, width=7)
    if ok: d.stroke([(x - 20, y), (x - 4, y + 18), (x + 22, y - 16)], WHITE, 12)
    else: d.stroke([(x - 16, y - 16), (x + 16, y + 16)], WHITE, 12); d.stroke([(x - 16, y + 16), (x + 16, y - 16)], WHITE, 12)


def ritual_card():
    d = G.card(680, 400); d.text(300, 130, "RITUALS", 96, LINE); tick(d, 590, 130, True); d.text(300, 280, "BATTLE", 96, LINE); tick(d, 590, 280, False); return d.out()


def timeline_card():
    d = G.card(960, 400); d.stroke([(110, 250), (850, 250)], LINE, 14); d.poly([(850, 226), (900, 250), (850, 274)], fill=LINE)
    for x, lab, col in ((140, "HORNS", BRONZE), (820, "VIKINGS", RED)): d.dot(x, 250, 34, col); d.ellipse(x, 250, 34, 34, outline=LINE, width=8); d.text(x, 330, lab, 52, LINE)
    d.text(480, 150, "1,000+ YEARS", 84, RED, stroke=5, stroke_fill=LINE); return d.out()


def ring_card():
    d = G.card(780, 380, (250, 240, 214, 255)); d.ellipse(130, 190, 80, 80, outline=LINE, width=38); d.ellipse(130, 190, 80, 80, outline=GOLD, width=24)
    d.text(470, 140, "THE RING OF THE", 54, LINE); d.text(470, 232, "NIBELUNG", 92, RED, stroke=5, stroke_fill=LINE); return d.out()


def prosc(path):                                             # red curtains + gold valance, open in the middle
    d = Draw(1800, 1300)
    for x0 in (0, 1500):
        d.rect(x0, 0, x0 + 300, 1300, (168, 34, 52, 255))
        for k in range(5): d.stroke([(x0 + 30 + k * 60, 160), (x0 + 30 + k * 60, 1300)], (120, 22, 40, 255), 10)
        d.stroke([(x0 + (300 if x0 == 0 else 0), 160), (x0 + (300 if x0 == 0 else 0), 1300)], LINE, 12)
    d.rect(0, 0, 1800, 200, (168, 34, 52, 255))
    for k in range(18): d.chord(50 + k * 100, 200, 50, 40, 0, 180, fill=(168, 34, 52, 255), outline=LINE, width=8)
    d.rect(0, 150, 1800, 176, GOLD); d.stroke([(0, 150), (1800, 150)], LINE, 8)
    d.out().save(path)


def ship(path):
    d = Draw(1300, 700)
    d.rect(560, 60, 590, 470, (120, 80, 50, 255)); sail = [(380, 110), (770, 110), (790, 400), (360, 400)]
    d.poly(sail, fill=(246, 240, 226, 255))
    m = Draw(1300, 700); m.poly(sail, fill=WHITE); s = Draw(1300, 700)
    for k in range(0, 9, 2): s.rect(360 + k * 48, 100, 408 + k * 48, 410, RED)
    d.clip(s, m); d.poly(sail, outline=LINE, width=10)
    hull = bez((80, 420), (300, 640), (1000, 640), (1220, 420)) + [(1220, 420), (80, 420)]
    d.poly(hull, fill=(150, 96, 60, 255), outline=LINE, width=12)
    for k in range(9): x = 250 + k * 100; d.dot(x, 470, 36, [RED, GOLD, (70, 120, 200, 255)][k % 3]); d.ellipse(x, 470, 36, 36, outline=LINE, width=6)
    d.stroke(bez((1180, 440), (1260, 300), (1200, 180), (1150, 200)), LINE, 30); d.stroke(bez((1180, 440), (1260, 300), (1200, 180), (1150, 200)), (150, 96, 60, 255), 18)
    d.out().save(path)


def tex_stripes(path, base, dark, period, n=512):
    x = np.arange(n) / n; v = (0.5 + 0.5 * np.sin(2 * np.pi * period * x)) ** 2
    a = np.array(dark) + (np.array(base) - np.array(dark)) * v[None, :, None] * np.ones((n, 1, 1))
    G.save_tex(a, path)


def tex_peat(path, n=512):
    rng = np.random.RandomState(5); a = np.zeros((n, n, 3)) + [96, 70, 50]
    a += (G.periodic(n, 7, 5)[..., None] - 0.5) * 30 + rng.normal(0, 6, (n, n, 1)); G.save_tex(a, path)


def fjord(path):
    G.sky(path); im = Image.open(path).convert('RGB'); dr = ImageDraw.Draw(im); W = im.size[0]
    for base, amp, col in ((960, 230, (122, 136, 170)), (1000, 150, (92, 108, 140))):
        pts = [(x, base - amp * abs(math.sin(math.pi * 3 * x / W + base)) ** 1.5) for x in range(0, W + 1, 10)]
        dr.polygon(pts + [(W, 1080), (0, 1080)], fill=col)
    dr.rectangle([0, 1000, W, 1080], fill=(84, 130, 176)); im.save(path, quality=92)


if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    for ch in ('mom', 'dad', 'tech'):                        # the same faces as video 02
        layers, faces = B.build_human(ch); items.append((ch, faces['happy']))
    B.human_head, B.human_body = head, body
    for ch in NEW:
        layers, faces = B.build_human(ch); items += [(ch + ' happy', faces['happy']), (ch + ' shocked', faces['shocked'])]
    cards = dict(helmr=helm_real(), helmb=helm_bronze(), horns=horns_card(), axe=axe(), spade=spade(), notes=notes(),
                 fake=wtag("FAKE?", 480), only=wtag("ONLY ONE!", 640), round=wtag("ROUND", 480, (70, 120, 200, 255)), iron=wtag("IRON", 420, (110, 116, 136, 255)),
                 zero=wtag("0 HORNS", 560), cal43=G.cal_card("NORWAY", "1943", ""), cal76=G.cal_card("OPERA", "1876", ""), cal42=G.cal_card("DENMARK", "1942", ""),
                 y150=big_card("150", "YEARS", RED, 560), y3000=big_card("3,000", "YEARS OLD", BRONZE), ritual=ritual_card(), timeline=timeline_card(),
                 ring=ring_card(), grab=B.sticker_burst('GRAB!'), poof=B.sticker_poof(), excl=B.sticker_mark('!', RED), ques=B.sticker_mark('?', GOLD), hearts=G.hearts())
    for nm, im in cards.items(): G.build_card(nm, {'default': im}); items.append((nm, im))
    T = lambda n: os.path.join(ROOT, 'textures', n)
    B.tex_grass(T('grass.jpg')); B.tex_wood(T('wood.jpg')); tex_peat(T('peat.jpg')); tex_stripes(T('velvet.jpg'), (176, 40, 58), (96, 16, 34), 8)
    fjord(os.path.join(ROOT, 'bg', 'fjord.jpg'))
    Pp = lambda n: os.path.join(ROOT, 'props', n)
    prosc(Pp('prosc.png')); ship(Pp('ship.png')); B.sparkle(Pp('sparkle.png'))
    for n in ('prosc', 'ship'): items.append((n, Image.open(Pp(n + '.png'))))
    items.append(('backdrop', Image.open(os.path.join(ROOT, 'bg', 'fjord.jpg'))))
    B.sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT, '-', len(items), 'items')
