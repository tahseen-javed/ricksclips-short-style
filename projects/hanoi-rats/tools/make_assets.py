#!/usr/bin/env python3
"""Draw every asset for the Hanoi rats Short in code (PIL, no generator):
cute doodle puppets + rig.json (references/formats.md), emotion faces,
seamless textures, a painted backdrop and flat prop cards.
usage: make_assets.py <project folder> [font.ttf]"""
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

ROOT = sys.argv[1]
FONT = sys.argv[2] if len(sys.argv) > 2 else None
S = 3                                   # supersample for clean anti-aliasing
LINE = (39, 25, 37, 255)                # plum-black #271925, never pure black
CREAM = (246, 241, 227, 255)
SHADE = (214, 205, 190, 255)
BLUSH = (242, 140, 140, 120)
WHITE = (255, 255, 255, 255)
MOUTH = (124, 40, 62, 255)
TONGUE = (238, 120, 132, 255)
GREY = (168, 164, 182, 255)
GREY_SHADE = (138, 132, 156, 255)
PINK = (242, 172, 184, 255)

def sc(v): return int(round(v * S))
def hexc(c): return '#%02x%02x%02x' % c[:3]
def bez(p0, p1, p2, p3, n=30):
    pts = []
    for i in range(n):
        t = i / (n - 1); u = 1 - t
        pts.append((u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
                    u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1]))
    return pts

class Draw:
    def __init__(self, w, h, bg=(0, 0, 0, 0)):
        self.w, self.h = w, h
        self.im = Image.new("RGBA", (sc(w), sc(h)), bg)
        self.d = ImageDraw.Draw(self.im)
    def box(self, cx, cy, rx, ry): return [sc(cx - rx), sc(cy - ry), sc(cx + rx), sc(cy + ry)]
    def ellipse(self, cx, cy, rx, ry, fill=None, outline=None, width=0):
        self.d.ellipse(self.box(cx, cy, rx, ry), fill=fill, outline=outline, width=sc(width))
    def dot(self, cx, cy, r, fill): self.ellipse(cx, cy, r, r, fill=fill)
    def stroke(self, pts, fill, width, closed=False):
        pts = list(pts) + ([pts[0]] if closed else [])
        self.d.line([(sc(x), sc(y)) for x, y in pts], fill=fill, width=sc(width), joint="curve")
        for x, y in pts: self.dot(x, y, width / 2, fill)
    def poly(self, pts, fill=None, outline=None, width=0):
        if fill: self.d.polygon([(sc(x), sc(y)) for x, y in pts], fill=fill)
        if outline: self.stroke(pts, outline, width, closed=True)
    def rect(self, x0, y0, x1, y1, fill): self.d.rectangle([sc(x0), sc(y0), sc(x1), sc(y1)], fill=fill)
    def rrect(self, x0, y0, x1, y1, r, fill=None, outline=None, width=0):
        self.d.rounded_rectangle([sc(x0), sc(y0), sc(x1), sc(y1)], radius=sc(r), fill=fill, outline=outline, width=sc(width))
    def arc(self, cx, cy, rx, ry, a0, a1, fill, width):
        self.d.arc(self.box(cx, cy, rx, ry), a0, a1, fill=fill, width=sc(width))
    def chord(self, cx, cy, rx, ry, a0, a1, fill, outline=None, width=0):
        self.d.chord(self.box(cx, cy, rx, ry), a0, a1, fill=fill, outline=outline, width=sc(width))
    def clip(self, layer, mask):
        """composite `layer` onto self where `mask` is opaque"""
        a = ImageChops.multiply(layer.im.getchannel('A'), mask.im.getchannel('A'))
        src = layer.im.copy(); src.putalpha(a); self.im.alpha_composite(src); self.d = ImageDraw.Draw(self.im)
    def text(self, cx, cy, s, size, fill, font=None, stroke=0, stroke_fill=None):
        f = ImageFont.truetype(font or FONT, sc(size)) if (font or FONT) else ImageFont.load_default()
        self.d.text((sc(cx), sc(cy)), s, fill=fill, font=f, anchor="mm", stroke_width=sc(stroke), stroke_fill=stroke_fill)
    def out(self): return self.im.resize((self.w, self.h), Image.LANCZOS)

# ------------------------------------------------------------------ humans
H = dict(W=460, H=1000, cx=230, hcy=270, R=200, neck=(230, 468), hip=(230, 800), lw=18, feetY=994,
         shoulders=((92, 512), (368, 512)), hands=((42, 772), (418, 772)),
         hips=((190, 796), (270, 796)), feet=((176, 986), (284, 986)), headbox=(0, 0, 460, 480))
HUMANS = {
    'official':  dict(base=(244, 240, 230, 255), shade=(214, 208, 196, 255), sash=(74, 104, 196, 255)),
    'hunter':    dict(base=(140, 92, 60, 255), shade=(108, 68, 44, 255), belt=(92, 58, 36, 255)),
    'inspector': dict(base=(66, 76, 146, 255), shade=(48, 56, 114, 255)),
    'hunter2':   dict(base=(86, 140, 98, 255), shade=(60, 104, 72, 255), belt=(92, 58, 36, 255)),
}

def cel_shadow(d, cx, cy, r, shade, skin, off=(-48, -26)):
    sh = Draw(d.w, d.h); sh.ellipse(cx, cy, r, r, fill=shade); sh.ellipse(cx + off[0], cy + off[1], r, r, fill=skin)
    m = Draw(d.w, d.h); m.ellipse(cx, cy, r, r, fill=WHITE); d.clip(sh, m)

def hat(d, char):
    cx, cy, lw = H['cx'], H['hcy'], H['lw']
    if char == 'official':                                   # pith helmet
        dome = Draw(d.w, d.h); dome.ellipse(cx, cy - 170, 166, 100, fill=(242, 236, 220, 255))
        band = Draw(d.w, d.h); band.ellipse(cx, cy - 170, 166, 100, fill=(217, 164, 65, 255)); band.ellipse(cx, cy - 200, 166, 100, fill=(242, 236, 220, 255))
        d.ellipse(cx, cy - 170, 166, 100, fill=(242, 236, 220, 255)); d.clip(band, dome)
        d.ellipse(cx, cy - 170, 166, 100, outline=LINE, width=lw)
        d.ellipse(cx, cy - 132, 226, 38, fill=(242, 236, 220, 255), outline=LINE, width=lw)
    elif char.startswith('hunter'):                          # conical straw hat
        tan, dark = (226, 188, 118, 255), (178, 138, 72, 255)
        apex, bl, br = (cx, 10), (cx - 222, 150), (cx + 222, 150)
        d.poly([apex, bl, br], fill=tan); d.chord(cx, 150, 222, 32, 0, 180, fill=tan)
        for k in range(1, 6):
            t = k / 6; d.stroke([apex, (bl[0] + (br[0] - bl[0]) * t, 150 + 30 * math.sin(math.pi * t))], dark, 5)
        d.stroke([bl, apex, br], LINE, lw); d.arc(cx, 150, 222, 32, 0, 180, LINE, lw)
        d.dot(bl[0], bl[1], lw / 2, LINE); d.dot(br[0], br[1], lw / 2, LINE)
    elif char == 'inspector':                                # kepi
        d.rrect(cx - 128, 26, cx + 128, 154, 28, fill=(60, 70, 140, 255))
        d.rect(cx - 128, 116, cx + 128, 142, (217, 164, 65, 255))
        d.rrect(cx - 128, 26, cx + 128, 154, 28, outline=LINE, width=lw)
        d.chord(cx, 152, 150, 40, 0, 180, fill=(44, 34, 56, 255), outline=LINE, width=lw)

def eyes(d, L, R, expr, skin, r=20):
    if expr == 'happy':
        for x, y in (L, R): d.arc(x, y + 8, 26, 22, 200, 340, LINE, 10); d.dot(x - 26, y + 8, 5, LINE); d.dot(x + 26, y + 8, 5, LINE)
    elif expr == 'shocked':
        for x, y in (L, R):
            d.ellipse(x, y, 34, 37, fill=WHITE, outline=LINE, width=8); d.dot(x, y + 5, 11, LINE); d.dot(x - 5, y - 2, 4, WHITE)
    elif expr in ('smug', 'sneaky'):
        for x, y in (L, R):
            d.dot(x, y, r, LINE); d.dot(x - 7, y - 7, 7, WHITE)
            lid = y - 2 if expr == 'smug' else y + 3
            d.rect(x - r - 2, y - r - 2, x + r + 2, lid, skin); d.stroke([(x - r - 2, lid), (x + r + 2, lid)], LINE, 9)
    else:
        for x, y in (L, R): d.dot(x, y, r, LINE); d.dot(x - 7, y - 7, 7, WHITE)

def brows(d, L, R, expr, by):
    ex = 24
    shapes = {
        'neutral':  ([(L[0]-ex, by+2), (L[0]+ex, by-2)], [(R[0]-ex, by-2), (R[0]+ex, by+2)]),
        'happy':    ([(L[0]-ex, by-6), (L[0], by-16), (L[0]+ex, by-8)], [(R[0]-ex, by-8), (R[0], by-16), (R[0]+ex, by-6)]),
        'shocked':  ([(L[0]-ex, by-18), (L[0], by-30), (L[0]+ex, by-20)], [(R[0]-ex, by-20), (R[0], by-30), (R[0]+ex, by-18)]),
        'confused': ([(L[0]-ex, by-4), (L[0]+ex, by-26)], [(R[0]-ex, by-2), (R[0]+ex, by+4)]),
        'shouting': ([(L[0]-ex, by-14), (L[0]+ex, by+12)], [(R[0]-ex, by+12), (R[0]+ex, by-14)]),
        'nervous':  ([(L[0]-ex, by+10), (L[0]+ex, by-12)], [(R[0]-ex, by-12), (R[0]+ex, by+10)]),
        'smug':     ([(L[0]-ex, by+8), (L[0]+ex, by+4)], [(R[0]-ex, by+4), (R[0]+ex, by+8)]),
        'sneaky':   ([(L[0]-ex, by-2), (L[0]+ex, by+12)], [(R[0]-ex, by+12), (R[0]+ex, by-2)]),
    }[expr]
    for pts in shapes: d.stroke(pts, LINE, 12)

def mouth(d, cx, my, expr):
    if expr == 'neutral': d.arc(cx, my - 14, 34, 26, 25, 155, LINE, 9)
    elif expr == 'happy':
        d.chord(cx, my - 6, 62, 54, 0, 180, fill=LINE); d.chord(cx, my - 6, 50, 42, 0, 180, fill=MOUTH)
        d.chord(cx + 8, my + 20, 24, 16, 180, 360, fill=TONGUE)
    elif expr == 'shocked': d.ellipse(cx, my, 24, 32, fill=LINE); d.ellipse(cx, my + 3, 14, 20, fill=MOUTH)
    elif expr == 'confused': d.stroke([(cx-34, my), (cx-14, my-10), (cx+6, my+6), (cx+30, my-6)], LINE, 9)
    elif expr == 'shouting':
        d.ellipse(cx, my, 50, 58, fill=LINE); d.ellipse(cx, my + 6, 36, 42, fill=MOUTH)
        d.chord(cx, my - 24, 32, 14, 0, 180, fill=WHITE)
    elif expr == 'nervous': d.stroke([(cx-36, my), (cx-22, my+8), (cx-8, my-6), (cx+6, my+8), (cx+20, my-6), (cx+34, my+2)], LINE, 9)
    elif expr == 'smug': d.arc(cx + 12, my - 12, 30, 22, 20, 150, LINE, 9)
    elif expr == 'sneaky':
        d.chord(cx, my - 26, 60, 44, 15, 165, fill=LINE); d.chord(cx, my - 26, 50, 34, 15, 165, fill=WHITE)
        for k in (-24, -8, 8, 24): d.stroke([(cx + k, my - 20), (cx + k, my + 2)], LINE, 5)

def human_head(char, expr):
    d = Draw(H['W'], H['H']); cx, cy, R, lw = H['cx'], H['hcy'], H['R'], H['lw']
    d.ellipse(cx, cy, R, R, fill=CREAM, outline=LINE, width=lw)
    cel_shadow(d, cx, cy, R - 9, SHADE, CREAM)
    hat(d, char)
    ey = cy - 6; L, Rr = (cx - 62, ey), (cx + 62, ey)
    d.ellipse(cx - 122, cy + 40, 30, 17, fill=BLUSH); d.ellipse(cx + 122, cy + 40, 30, 17, fill=BLUSH)
    eyes(d, L, Rr, expr, CREAM); brows(d, L, Rr, expr, ey - 50)
    my = cy + 74
    if char in ('official', 'inspector'):                    # moustache
        if char == 'official':
            d.stroke(bez((cx - 8, my - 30), (cx - 40, my - 44), (cx - 62, my - 40), (cx - 70, my - 64)), LINE, 11)
            d.stroke(bez((cx + 8, my - 30), (cx + 40, my - 44), (cx + 62, my - 40), (cx + 70, my - 64)), LINE, 11)
        else:
            d.rrect(cx - 54, my - 44, cx + 54, my - 22, 11, fill=LINE)
        my += 10
    mouth(d, cx, my, expr)
    if expr == 'nervous':                                    # sweat drop
        sx, sy = cx + 150, cy - 30
        d.poly([(sx, sy - 34), (sx - 16, sy + 4), (sx + 16, sy + 4)], fill=(150, 200, 240, 255))
        d.dot(sx, sy + 4, 16, (150, 200, 240, 255))
        d.stroke([(sx, sy - 34), (sx - 16, sy + 2)], LINE, 6); d.stroke([(sx, sy - 34), (sx + 16, sy + 2)], LINE, 6)
        d.arc(sx, sy + 4, 16, 16, 0, 180, LINE, 6)
    return d.out()

def human_body(char):
    d = Draw(H['W'], H['H']); c = HUMANS[char]; x0, y0, x1, y1, r, lw = 85, 458, 375, 800, 115, H['lw']
    mask = Draw(d.w, d.h); mask.rrect(x0, y0, x1, y1, r, fill=WHITE)
    d.rrect(x0, y0, x1, y1, r, fill=c['base'])
    sh = Draw(d.w, d.h); sh.rrect(x0, y0, x1, y1, r, fill=c['shade']); sh.rrect(x0 - 42, y0 - 20, x1 - 42, y1 - 20, r, fill=c['base']); d.clip(sh, mask)
    det = Draw(d.w, d.h)
    if char == 'official':
        det.stroke([(x0 + 36, y0 + 24), (x1 - 30, y1 - 40)], c['sash'], 46)
        for y in (560, 640, 720): det.dot(230, y, 11, (217, 164, 65, 255)); det.ellipse(230, y, 11, 11, outline=LINE, width=4)
        det.dot(x0 + 70, 600, 16, (217, 164, 65, 255)); det.ellipse(x0 + 70, 600, 16, 16, outline=LINE, width=4)
        det.stroke([(x0 + 70, 570), (x0 + 70, 586)], (196, 60, 70, 255), 12)
    elif char.startswith('hunter'):
        det.rect(x0, 696, x1, 724, c['belt']); det.stroke([(x0, 696), (x1, 696)], LINE, 5); det.stroke([(x0, 724), (x1, 724)], LINE, 5)
        det.stroke([(230, 480), (230, 690)], c['shade'], 8)
    else:
        for y in (560, 640, 720):
            for x in (200, 260): det.dot(x, y, 10, (217, 164, 65, 255)); det.ellipse(x, y, 10, 10, outline=LINE, width=4)
        det.stroke([(230, 470), (230, 540)], (217, 164, 65, 255), 8)
    d.clip(det, mask)
    d.rrect(x0, y0, x1, y1, r, outline=LINE, width=lw)
    return d.out()

def limb(p0, p1, width, hand):
    d = Draw(H['W'], H['H']); d.stroke([p0, p1], LINE, width)
    if hand: d.dot(p1[0], p1[1], hand, LINE)
    return d.out()

def write_rig(folder, name, size, feetY, head, skin, layers, pivots, eyes, faces, headbox, order=None):
    os.makedirs(os.path.join(folder, 'faces'), exist_ok=True)
    rig = {"version": 2, "name": name, "size": list(size), "feetY": feetY,
           "head": {"center": list(head[0]), "diameter": head[1]}, "skin": skin, "layers": {},
           "order": order or ["legL", "legR", "armL", "armR", "body", "head"], "eyes": eyes, "faces": {}}
    for k, img in layers.items():
        bb = headbox if k == 'head' else img.getbbox()
        x0, y0, x1, y1 = bb; img.crop(bb).save(os.path.join(folder, k + '.png'))
        rig["layers"][k] = {"file": k + ".png", "box": [x0, y0, x1 - x0, y1 - y0], "pivot": list(pivots[k])}
    hx, hy = headbox[0], headbox[1]
    for fname, img in faces.items():
        img.crop(headbox).save(os.path.join(folder, 'faces', fname + '.png'))
        rig["faces"][fname] = {"file": "faces/%s.png" % fname, "size": [headbox[2] - hx, headbox[3] - hy],
                               "pivot": [pivots['head'][0] - hx, pivots['head'][1] - hy],
                               "center": [head[0][0] - hx, head[0][1] - hy], "diameter": head[1]}
    with open(os.path.join(folder, 'rig.json'), 'w') as fh: json.dump(rig, fh, indent=1)
    return rig

EXPRS = ['neutral', 'happy', 'shocked', 'confused', 'shouting', 'nervous', 'smug', 'sneaky']

def build_human(char):
    folder = os.path.join(ROOT, 'puppets', char); lw = H['lw']
    layers = {'head': human_head(char, 'neutral'), 'body': human_body(char),
              'armL': limb(H['shoulders'][0], H['hands'][0], lw, 20), 'armR': limb(H['shoulders'][1], H['hands'][1], lw, 20),
              'legL': limb(H['hips'][0], H['feet'][0], lw, 0), 'legR': limb(H['hips'][1], H['feet'][1], lw, 0)}
    pivots = {'head': H['neck'], 'body': H['hip'], 'armL': H['shoulders'][0], 'armR': H['shoulders'][1], 'legL': H['hips'][0], 'legR': H['hips'][1]}
    ey = H['hcy'] - 6
    eyes_ = [{"c": [H['cx'] - 62, ey], "r": 36}, {"c": [H['cx'] + 62, ey], "r": 36}]
    faces = {e: human_head(char, e) for e in EXPRS}
    write_rig(folder, char, (H['W'], H['H']), H['feetY'], ((H['cx'], H['hcy']), 2 * H['R']), hexc(CREAM), layers, pivots, eyes_, faces, H['headbox'])
    return layers, faces

# ------------------------------------------------------------------ rats
RW, RH = 520, 300
R_HEAD = ((150, 160), 150); R_NECK = (205, 200); R_HEADBOX = (55, 45, 245, 245); R_LW = 9

def rat_head(expr, bow=False):
    d = Draw(RW, RH); (cx, cy), D = R_HEAD; R = D / 2
    for ex in (105, 195):
        d.ellipse(ex, 95, 38, 38, fill=GREY, outline=LINE, width=R_LW); d.ellipse(ex, 97, 22, 22, fill=PINK)
    d.ellipse(cx, cy, R, R, fill=GREY, outline=LINE, width=R_LW)
    cel_shadow(d, cx, cy, R - 4, GREY_SHADE, GREY, off=(-22, -12))
    L, Rr = (125, 158), (175, 158)
    d.ellipse(cx - 44, cy + 20, 14, 8, fill=BLUSH); d.ellipse(cx + 44, cy + 20, 14, 8, fill=BLUSH)
    if expr == 'happy':
        for x, y in (L, Rr): d.arc(x, y + 4, 13, 11, 200, 340, LINE, 6)
    elif expr == 'shocked':
        for x, y in (L, Rr): d.ellipse(x, y, 17, 18, fill=WHITE, outline=LINE, width=4); d.dot(x, y + 3, 6, LINE)
    elif expr == 'sneaky':
        for x, y in (L, Rr): d.dot(x, y, 12, LINE); d.dot(x - 4, y - 4, 4, WHITE); d.rect(x - 14, y - 14, x + 14, y + 1, GREY); d.stroke([(x - 13, y + 1), (x + 13, y + 1)], LINE, 5)
    elif expr == 'dead':
        for x, y in (L, Rr): d.stroke([(x - 11, y - 11), (x + 11, y + 11)], LINE, 6); d.stroke([(x - 11, y + 11), (x + 11, y - 11)], LINE, 6)
    else:
        for x, y in (L, Rr): d.dot(x, y, 12, LINE); d.dot(x - 4, y - 4, 4, WHITE)
    d.dot(86, 188, 10, PINK); d.ellipse(86, 188, 10, 10, outline=LINE, width=4)
    for y1 in (176, 194, 212): d.stroke([(96, 192), (58, y1)], LINE, 3)
    if expr == 'shocked': d.ellipse(118, 208, 9, 12, fill=LINE)
    elif expr == 'happy': d.chord(118, 204, 16, 13, 0, 180, fill=LINE); d.chord(118, 204, 11, 8, 0, 180, fill=MOUTH)
    elif expr == 'dead': d.arc(118, 202, 14, 9, 20, 160, LINE, 5); d.chord(124, 212, 8, 10, 0, 180, fill=TONGUE); d.arc(124, 212, 8, 10, 0, 180, LINE, 3)
    else: d.arc(118, 198, 14, 10, 20, 160, LINE, 5)
    if bow:
        for sx in (-1, 1): d.poly([(150, 74), (150 + sx * 44, 52), (150 + sx * 44, 96)], fill=(240, 110, 150, 255), outline=LINE, width=5)
        d.dot(150, 74, 11, (240, 110, 150, 255)); d.ellipse(150, 74, 11, 11, outline=LINE, width=5)
    return d.out()

def rat_body(tail):
    d = Draw(RW, RH); cx, cy, rx, ry = 290, 195, 140, 85
    if tail:
        pts = bez((425, 185), (480, 165), (505, 100), (470, 30))
        d.stroke(pts, LINE, 20); d.stroke(pts, PINK, 10)
    d.ellipse(cx, cy, rx, ry, fill=GREY, outline=LINE, width=R_LW)
    mask = Draw(RW, RH); mask.ellipse(cx, cy, rx - 4, ry - 4, fill=WHITE)
    belly = Draw(RW, RH); belly.ellipse(cx, cy + 36, 118, 52, fill=(216, 211, 224, 255)); d.clip(belly, mask)
    sh = Draw(RW, RH); sh.ellipse(cx, cy, rx - 4, ry - 4, fill=GREY_SHADE); sh.ellipse(cx - 26, cy - 16, rx - 4, ry - 4, fill=(0, 0, 0, 0))
    top = Draw(RW, RH); top.ellipse(cx - 26, cy - 16, rx - 4, ry - 4, fill=WHITE); shm = Draw(RW, RH); shm.ellipse(cx, cy, rx - 4, ry - 4, fill=WHITE)
    crescent = Draw(RW, RH); crescent.ellipse(cx, cy, rx - 4, ry - 4, fill=GREY_SHADE)
    cut = ImageChops.subtract(shm.im.getchannel('A'), top.im.getchannel('A')); src = crescent.im.copy(); src.putalpha(cut); d.im.alpha_composite(src); d.d = ImageDraw.Draw(d.im)
    d.ellipse(cx, cy, rx, ry, outline=LINE, width=R_LW)
    if not tail:                                             # a tiny plaster where the tail was
        for a, b in (((404, 174), (438, 204)), ((404, 204), (438, 174))): d.stroke([a, b], LINE, 16); d.stroke([a, b], (250, 206, 212, 255), 9)
    return d.out()

def rat_limb(p0, p1):
    d = Draw(RW, RH); d.stroke([p0, p1], LINE, 11); d.dot(p1[0], p1[1], 9, LINE); return d.out()

def build_rat(name, tail, bow=False):
    folder = os.path.join(ROOT, 'puppets', name)
    piv = {'head': R_NECK, 'body': (300, 280), 'armL': (170, 262), 'armR': (215, 268), 'legL': (335, 270), 'legR': (385, 266)}
    layers = {'head': rat_head('neutral', bow), 'body': rat_body(tail),
              'armL': rat_limb(piv['armL'], (164, 290)), 'armR': rat_limb(piv['armR'], (216, 292)),
              'legL': rat_limb(piv['legL'], (330, 292)), 'legR': rat_limb(piv['legR'], (392, 292))}
    eyes_ = [{"c": [125, 158], "r": 20}, {"c": [175, 158], "r": 20}]
    faces = {e: rat_head(e, bow) for e in ('neutral', 'happy', 'shocked', 'sneaky', 'dead')}
    write_rig(folder, name, (RW, RH), 296, R_HEAD, hexc(GREY), layers, piv, eyes_, faces, R_HEADBOX)
    return layers, faces

# ------------------------------------------------------------------ textures (seamless)
def tex_brick(path, n=512):
    d = Draw(n, n, (92, 60, 70, 255)); random.seed(3); rows, bw = 8, 128; bh = n // rows
    for r in range(rows):
        off = (bw // 2) if r % 2 else 0
        for c in range(-1, n // bw + 1):
            x0 = c * bw + off; v = random.randint(-14, 14)
            col = (126 + v, 76 + v // 2, 68 + v // 2, 255)
            d.rrect(x0 + 5, r * bh + 5, x0 + bw - 5, (r + 1) * bh - 5, 8, fill=col, outline=LINE, width=4)
            d.rrect(x0 + 12, r * bh + 10, x0 + bw - 12, r * bh + 22, 5, fill=(150 + v, 98 + v // 2, 88, 255))
    d.out().convert('RGB').save(path, quality=92)

def tex_wood(path, n=512):
    d = Draw(n, n, (168, 122, 74, 255)); random.seed(5); pw = n // 4
    for p in range(4):
        v = random.randint(-16, 16); x0 = p * pw
        d.rect(x0, 0, x0 + pw, n, (170 + v, 124 + v, 76 + v // 2, 255))
        for k in range(7):
            y = random.randint(0, n); amp = random.randint(6, 18)
            pts = [(x0 + 8 + i * (pw - 16) / 12, y + amp * math.sin(i / 2.0 + k)) for i in range(13)]
            d.stroke(pts, (138 + v, 96 + v, 56, 255), 4)
        d.stroke([(x0 + 2, 0), (x0 + 2, n)], LINE, 5)
        for y in (60, 300): d.dot(x0 + pw // 2, y + p * 37 % 120, 6, (90, 62, 44, 255))
    d.out().convert('RGB').save(path, quality=92)

def tex_dirt(path, n=512):
    d = Draw(n, n, (186, 136, 92, 255)); random.seed(7)
    for _ in range(260):
        x, y, r = random.randint(0, n), random.randint(0, n), random.randint(4, 22); v = random.randint(-22, 18)
        col = (186 + v, 136 + v, 92 + v, 255)
        for dx in (-n, 0, n):
            for dy in (-n, 0, n): d.ellipse(x + dx, y + dy, r, r * 0.7, fill=col)
    for _ in range(90):
        x, y = random.randint(0, n), random.randint(0, n)
        for dx in (-n, 0, n):
            for dy in (-n, 0, n): d.dot(x + dx, y + dy, random.randint(2, 4), (120, 84, 66, 255))
    d.out().convert('RGB').save(path, quality=92)

def tex_grass(path, n=512):
    d = Draw(n, n, (116, 172, 88, 255)); random.seed(9)
    for _ in range(200):
        x, y, r = random.randint(0, n), random.randint(0, n), random.randint(10, 34); v = random.randint(-16, 14)
        for dx in (-n, 0, n):
            for dy in (-n, 0, n): d.ellipse(x + dx, y + dy, r, r * 0.7, fill=(116 + v, 172 + v, 88 + v // 2, 255))
    for _ in range(320):
        x, y = random.randint(0, n), random.randint(0, n); c = random.choice([(70, 128, 74, 255), (58, 112, 66, 255), (150, 200, 100, 255)])
        for dx in (-n, 0, n):
            for dy in (-n, 0, n): d.stroke([(x + dx - 7, y + dy), (x + dx, y + dy - 14), (x + dx + 7, y + dy)], c, 3)
    d.out().convert('RGB').save(path, quality=92)

# ------------------------------------------------------------------ backdrop
def backdrop(path, W=2520, Hh=1080):
    im = Image.new('RGB', (W, Hh)); px = im.load()
    top, mid, hor = (95, 134, 216), (236, 178, 140), (247, 206, 160)
    for y in range(Hh):
        t = y / 830 if y < 830 else 1.0
        if t < 0.72: a = t / 0.72; c = tuple(int(top[i] + (mid[i] - top[i]) * a) for i in range(3))
        else: a = (t - 0.72) / 0.28; c = tuple(int(mid[i] + (hor[i] - mid[i]) * a) for i in range(3))
        for x in range(W): px[x, y] = c
    glow = Image.new('RGB', (W, Hh), (0, 0, 0)); g = ImageDraw.Draw(glow)
    for r, a in ((520, 40), (380, 60), (240, 90)): g.ellipse([1700 - r, 760 - r * 0.6, 1700 + r, 760 + r * 0.6], fill=(a, int(a * 0.8), int(a * 0.5)))
    im = ImageChops.add(im, glow.filter(ImageFilter.GaussianBlur(90)))
    d = ImageDraw.Draw(im, 'RGBA')
    for ridge, col, base, amp in (((150, 140, 185, 255), None, 800, 60), ((122, 110, 162, 255), None, 850, 40)):
        pts = [(x, base - amp * (0.6 * math.sin(2 * math.pi * 3 * x / W) + 0.4 * math.sin(2 * math.pi * 7 * x / W + 1.3))) for x in range(0, W + 1, 8)]
        d.polygon(pts + [(W, Hh), (0, Hh)], fill=ridge)
    random.seed(11); bcol, rcol, wcol = (104, 92, 140, 255), (118, 78, 92, 255), (242, 204, 140, 255)
    def building(x, w, h, roof):
        for dx in (-W, 0, W):
            d.rectangle([x + dx, 1000 - h, x + dx + w, 1010], fill=bcol)
            if roof == 'tile': d.polygon([(x + dx - 8, 1000 - h), (x + dx + w / 2, 1000 - h - 40), (x + dx + w + 8, 1000 - h)], fill=rcol)
            else: d.rectangle([x + dx - 6, 1000 - h - 14, x + dx + w + 6, 1000 - h], fill=rcol)
            for wy in range(1000 - h + 30, 995, 34):
                for wx in range(x + 14, x + w - 14, 30):
                    if random.random() < 0.5: d.rectangle([wx + dx, wy, wx + dx + 10, wy + 14], fill=wcol)
    x = 0
    while x < W:
        w, h = random.randint(70, 190), random.randint(50, 150); building(x, w, h, random.choice(['tile', 'flat'])); x += w + random.randint(10, 60)
    for tx in (560, 1900):                                   # twin-tower cathedral
        for dx in (-W, 0, W):
            d.rectangle([tx + dx, 820, tx + dx + 60, 1010], fill=bcol); d.rectangle([tx + dx + 100, 820, tx + dx + 160, 1010], fill=bcol)
            d.rectangle([tx + dx + 60, 880, tx + dx + 100, 1010], fill=bcol); d.polygon([(tx + dx, 820), (tx + dx + 30, 780), (tx + dx + 60, 820)], fill=rcol)
            d.polygon([(tx + dx + 100, 820), (tx + dx + 130, 780), (tx + dx + 160, 820)], fill=rcol)
    for px_ in (300, 1150, 1400, 2200):                      # palms
        for dx in (-W, 0, W):
            d.line([(px_ + dx, 1010), (px_ + dx + 10, 880)], fill=(86, 100, 92, 255), width=8)
            for a in range(0, 360, 45): d.line([(px_ + dx + 10, 880), (px_ + dx + 10 + 70 * math.cos(math.radians(a)), 880 + 40 * math.sin(math.radians(a)) - 10)], fill=(86, 110, 92, 255), width=10)
    d.rectangle([0, 1005, W, Hh], fill=(206, 154, 112, 255))
    haze = Image.new('RGBA', (W, Hh), (0, 0, 0, 0)); hd = ImageDraw.Draw(haze); hd.rectangle([0, 760, W, 1010], fill=(247, 206, 170, 90))
    im = Image.alpha_composite(im.convert('RGBA'), haze.filter(ImageFilter.GaussianBlur(40))).convert('RGB')
    im.save(path, quality=92)

# ------------------------------------------------------------------ flat props
def poster(path):
    d = Draw(600, 800); d.rrect(10, 10, 590, 790, 26, fill=(241, 230, 200, 255), outline=LINE, width=14)
    d.rrect(34, 34, 566, 766, 16, outline=(190, 150, 110, 255), width=4)
    for x, y in ((60, 60), (540, 60), (60, 740), (540, 740)): d.dot(x, y, 12, (190, 60, 60, 255)); d.ellipse(x, y, 12, 12, outline=LINE, width=4)
    d.text(300, 190, "1¢", 250, LINE); d.text(300, 350, "PER RAT", 88, (190, 60, 60, 255), stroke=4, stroke_fill=LINE)
    d.ellipse(300, 520, 110, 62, fill=LINE); d.ellipse(190, 500, 56, 56, fill=LINE); d.dot(160, 456, 22, LINE); d.dot(212, 450, 22, LINE)
    d.stroke(bez((405, 520), (470, 520), (500, 470), (470, 420)), LINE, 14); d.dot(176, 500, 7, WHITE); d.dot(206, 500, 7, WHITE)
    d.text(300, 690, "BRING THE TAIL", 62, LINE)
    d.out().save(path)

def tails(path):
    d = Draw(600, 420); random.seed(21)
    d.rrect(50, 180, 550, 405, 40, fill=(150, 100, 60, 255))
    for y in range(206, 400, 32): d.stroke([(62, y), (538, y)], (112, 72, 42, 255), 6)
    for x in range(90, 540, 56): d.stroke([(x, 186), (x, 400)], (112, 72, 42, 255), 5)
    for _ in range(46):
        x, y = random.randint(90, 510), random.randint(120, 240); a = random.uniform(0, 6.28)
        pts = bez((x, y), (x + 60 * math.cos(a), y + 40 * math.sin(a)), (x + 40 * math.cos(a + 2), y - 50 * math.sin(a + 1)), (x + 90 * math.cos(a + 1), y - 70))
        d.stroke(pts, LINE, 18); d.stroke(pts, PINK, 9)
    d.rrect(50, 180, 550, 405, 40, outline=LINE, width=12)
    d.rrect(40, 160, 560, 210, 24, fill=(168, 116, 70, 255), outline=LINE, width=10)
    d.out().save(path)

def sewer(path):
    d = Draw(600, 600); cx = cy = 300
    d.ellipse(cx, cy, 290, 290, fill=(122, 74, 68, 255), outline=LINE, width=12)
    for k in range(14):
        a = math.radians(k * 360 / 14)
        d.stroke([(cx + 210 * math.cos(a), cy + 210 * math.sin(a)), (cx + 284 * math.cos(a), cy + 284 * math.sin(a))], LINE, 8)
    d.ellipse(cx, cy, 212, 212, fill=(43, 33, 64, 255), outline=LINE, width=12)
    d.ellipse(cx, cy + 10, 150, 150, fill=(56, 44, 86, 255)); d.ellipse(cx, cy + 20, 90, 90, fill=(66, 52, 100, 255))
    for ex in (262, 338): d.dot(ex, 330, 12, (250, 220, 90, 255)); d.dot(ex + 3, 330, 5, LINE)
    for x in (230, 300, 370): d.stroke(bez((x, 500), (x - 5, 540), (x + 5, 560), (x, 585)), (120, 148, 100, 255), 10)
    d.out().save(path)

# ------------------------------------------------------------------ cards and stickers
GOLD = (236, 184, 64, 255)
RED = (212, 62, 70, 255)
WOOD = (176, 124, 76, 255)
WOOD_D = (128, 86, 52, 255)

def tail_bunting(d, y0, x0, x1, n):
    cols = [(212, 62, 70, 255), (74, 104, 196, 255), GOLD, (96, 170, 110, 255)]
    step = (x1 - x0) / n
    for i in range(n):
        xa = x0 + i * step; d.poly([(xa + 8, y0), (xa + step - 8, y0), (xa + step / 2, y0 + 70)], fill=cols[i % 4], outline=LINE, width=6)

def banner(path):
    d = Draw(1800, 340); d.stroke([(20, 40), (1780, 40)], LINE, 8)
    pts = [(60, 40), (1740, 40), (1700, 140), (1740, 240), (60, 240), (100, 140)]
    d.poly(pts, fill=(246, 238, 214, 255), outline=LINE, width=14)
    d.rrect(130, 62, 1670, 218, 18, outline=(190, 150, 110, 255), width=5)
    d.text(900, 146, "HANOI  ·  1902", 150, LINE)
    tail_bunting(d, 246, 90, 1710, 14)
    d.out().save(path)

def window(path):
    d = Draw(380, 560)
    for x0 in (10, 300):                                       # shutters
        d.rrect(x0, 120, x0 + 70, 440, 10, fill=(70, 150, 150, 255), outline=LINE, width=7)
        for y in range(150, 430, 36): d.stroke([(x0 + 12, y), (x0 + 58, y)], (44, 112, 118, 255), 5)
    d.rect(78, 150, 302, 440, (252, 244, 226, 255)); d.chord(190, 150, 112, 96, 180, 360, fill=(252, 244, 226, 255))
    d.rect(100, 160, 280, 430, (150, 196, 232, 255)); d.chord(190, 160, 90, 80, 180, 360, fill=(150, 196, 232, 255))
    d.stroke([(190, 78), (190, 430)], (252, 244, 226, 255), 12); d.stroke([(100, 270), (280, 270)], (252, 244, 226, 255), 12)
    d.stroke([(100, 430), (100, 160), (110, 130), (190, 78), (270, 130), (280, 160), (280, 430)], LINE, 8)
    d.stroke([(78, 440), (78, 150)], LINE, 7); d.stroke([(302, 440), (302, 150)], LINE, 7)
    d.poly([(100, 160), (182, 160), (150, 270), (100, 250)], fill=(222, 80, 96, 255), outline=LINE, width=6)   # curtains
    d.poly([(280, 160), (198, 160), (230, 270), (280, 250)], fill=(222, 80, 96, 255), outline=LINE, width=6)
    d.rrect(56, 440, 324, 508, 12, fill=(168, 112, 70, 255), outline=LINE, width=8)                            # flower box
    for i, x in enumerate(range(84, 310, 36)):
        d.dot(x, 428 - (i % 2) * 12, 17, ((240, 110, 150, 255), (250, 214, 90, 255))[i % 2]); d.ellipse(x, 428 - (i % 2) * 12, 17, 17, outline=LINE, width=4)
        d.stroke([(x, 440), (x, 452)], (84, 150, 90, 255), 6)
    d.out().save(path)

def sign_ratfarm(path):
    d = Draw(1100, 440)
    for x in (170, 930): d.rrect(x - 26, 220, x + 26, 436, 10, fill=WOOD_D, outline=LINE, width=8)
    d.rrect(30, 40, 1070, 300, 34, fill=WOOD, outline=LINE, width=14)
    for y in (120, 200): d.stroke([(50, y), (1050, y)], WOOD_D, 6)
    for x, y in ((80, 80), (1020, 80), (80, 260), (1020, 260)): d.dot(x, y, 12, (120, 84, 60, 255)); d.ellipse(x, y, 12, 12, outline=LINE, width=4)
    d.text(550, 170, "RAT FARM", 170, (252, 240, 214, 255), stroke=12, stroke_fill=LINE)
    d.out().save(path)

def sign_count(path):
    d = Draw(900, 640)
    for x in (200, 700): d.rrect(x - 24, 440, x + 24, 636, 10, fill=WOOD_D, outline=LINE, width=8)
    d.rrect(20, 20, 880, 480, 42, fill=WOOD, outline=LINE, width=14)
    d.rrect(48, 48, 852, 452, 28, outline=WOOD_D, width=6)
    d.text(450, 112, "TAILS TURNED IN", 66, (252, 240, 214, 255), stroke=6, stroke_fill=LINE)
    d.text(450, 270, "20,112", 230, GOLD, stroke=14, stroke_fill=LINE)
    d.text(450, 406, "IN ONE DAY", 70, (252, 240, 214, 255), stroke=6, stroke_fill=LINE)
    d.out().save(path)

def calendar(path):
    d = Draw(500, 580)
    d.rrect(20, 40, 480, 560, 34, fill=(252, 248, 238, 255), outline=LINE, width=14)
    d.rrect(20, 40, 480, 190, 34, fill=RED, outline=LINE, width=14); d.rect(34, 120, 466, 190, RED)
    d.stroke([(20, 190), (480, 190)], LINE, 10)
    for x in (130, 370): d.rrect(x - 18, 4, x + 18, 84, 16, fill=(220, 220, 230, 255), outline=LINE, width=7)
    d.text(250, 118, "JUNE", 100, WHITE, stroke=8, stroke_fill=LINE)
    d.text(250, 360, "21", 250, LINE)
    d.text(250, 504, "1902", 64, (130, 110, 120, 255))
    d.out().save(path)

def poster_stamped(path):
    base = Image.open(os.path.join(ROOT, 'props', 'poster.png')).convert('RGBA')
    t = Draw(600, 800); t.rrect(30, 280, 570, 520, 22, fill=(248, 238, 218, 244), outline=RED, width=16); t.text(300, 400, "SCRAPPED", 112, RED)
    rot = t.out().rotate(-18, resample=Image.BICUBIC); base.alpha_composite(rot); base.save(path)

def sparkle(path):
    d = Draw(256, 256)
    pts = [(128, 8), (152, 104), (248, 128), (152, 152), (128, 248), (104, 152), (8, 128), (104, 104)]
    d.poly(pts, fill=(255, 246, 176, 255), outline=LINE, width=7); d.dot(128, 128, 14, WHITE)
    d.out().save(path)

def sticker_burst(txt, fill=(255, 214, 64, 255), tc=RED):
    d = Draw(460, 360); cx, cy = 230, 180; pts = []
    for k in range(28):
        a = math.pi * 2 * k / 28; r = 172 if k % 2 == 0 else 112; pts.append((cx + r * math.cos(a) * 1.18, cy + r * math.sin(a) * 0.9))
    d.poly(pts, fill=fill, outline=LINE, width=10); d.text(cx, cy + 4, txt, 112, tc, stroke=10, stroke_fill=LINE)
    return d.out()

def sticker_poof():
    d = Draw(420, 340)
    for x, y, r in ((120, 210, 82), (210, 150, 104), (306, 206, 86), (210, 240, 96), (150, 130, 62), (280, 120, 56)):
        d.dot(x, y, r, LINE)
    for x, y, r in ((120, 210, 72), (210, 150, 94), (306, 206, 76), (210, 240, 86), (150, 130, 52), (280, 120, 46)):
        d.dot(x, y, r, (250, 248, 255, 255))
    d.dot(190, 120, 20, (226, 226, 242, 255)); d.dot(300, 200, 26, (226, 226, 242, 255))
    return d.out()

def sticker_mark(ch, col):
    d = Draw(230, 320); d.text(115, 170, ch, 300, col, stroke=16, stroke_fill=LINE); return d.out()

def sticker_scissors():
    d = Draw(420, 300)
    d.poly([(130, 150), (370, 70), (380, 100), (150, 170)], fill=(214, 220, 232, 255), outline=LINE, width=7)
    d.poly([(130, 150), (370, 230), (380, 200), (150, 130)], fill=(190, 198, 214, 255), outline=LINE, width=7)
    for cy in (96, 204): d.ellipse(84, cy, 46, 40, outline=LINE, width=26); d.ellipse(84, cy, 46, 40, outline=RED, width=14)
    d.dot(146, 150, 12, GOLD); d.ellipse(146, 150, 12, 12, outline=LINE, width=4)
    return d.out()

def sticker_coin():
    d = Draw(240, 240); d.dot(120, 120, 108, LINE); d.dot(120, 120, 98, GOLD); d.ellipse(120, 120, 78, 78, outline=(204, 148, 40, 255), width=8)
    d.text(120, 124, "1¢", 100, LINE); d.dot(80, 70, 14, (255, 238, 170, 255))
    return d.out()

def build_sticker(name, img):
    folder = os.path.join(ROOT, 'puppets', name); os.makedirs(folder, exist_ok=True)
    w, h = img.size; Image.new('RGBA', (4, 4), (0, 0, 0, 0)).save(os.path.join(folder, 'body.png')); img.save(os.path.join(folder, 'head.png'))
    rig = {"version": 2, "name": name, "size": [w, h], "feetY": h, "head": {"center": [w / 2, h / 2], "diameter": w}, "skin": "#ffffff",
           "layers": {"body": {"file": "body.png", "box": [w // 2 - 2, h - 4, 4, 4], "pivot": [w / 2, h - 2]},
                      "head": {"file": "head.png", "box": [0, 0, w, h], "pivot": [w / 2, h / 2]}},
           "order": ["body", "head"], "eyes": [], "faces": {}}
    with open(os.path.join(folder, 'rig.json'), 'w') as fh: json.dump(rig, fh, indent=1)

# ------------------------------------------------------------------ run
def sheet(items, path, cell=(300, 330)):
    cols = 6; rows = (len(items) + cols - 1) // cols
    im = Image.new('RGB', (cols * cell[0], rows * cell[1]), (120, 150, 190)); dr = ImageDraw.Draw(im)
    for i, (name, img) in enumerate(items):
        x, y = (i % cols) * cell[0], (i // cols) * cell[1]
        th = img.copy(); th.thumbnail((cell[0] - 20, cell[1] - 40)); im.paste(th, (x + 10, y + 10), th if th.mode == 'RGBA' else None)
        dr.text((x + 10, y + cell[1] - 26), name, fill=(255, 255, 255))
    im.save(path, quality=88)

if __name__ == '__main__':
    for sub in ('puppets', 'textures', 'bg', 'props', 'models', 'audio'): os.makedirs(os.path.join(ROOT, sub), exist_ok=True)
    items = []
    for char in HUMANS:
        layers, faces = build_human(char); items += [(char + ' ' + e, f) for e, f in faces.items()]
    layers, faces = build_human('hunter2'); items += [('hunter2 ' + e, f) for e, f in faces.items()]
    for name, tail, bow in (('rat', True, False), ('ratnt', False, False), ('ratmom', False, True)):
        layers, faces = build_rat(name, tail, bow); items += [(name + ' ' + e, f) for e, f in faces.items()]; items.append((name + ' body', layers['body']))
    tex_brick(os.path.join(ROOT, 'textures', 'brick.jpg')); tex_wood(os.path.join(ROOT, 'textures', 'wood.jpg')); tex_dirt(os.path.join(ROOT, 'textures', 'dirt.jpg')); tex_grass(os.path.join(ROOT, 'textures', 'grass.jpg'))
    backdrop(os.path.join(ROOT, 'bg', 'hanoi.jpg'))
    poster(os.path.join(ROOT, 'props', 'poster.png')); tails(os.path.join(ROOT, 'props', 'tails.png')); sewer(os.path.join(ROOT, 'props', 'sewer.png'))
    banner(os.path.join(ROOT, 'props', 'banner.png')); window(os.path.join(ROOT, 'props', 'window.png')); sign_ratfarm(os.path.join(ROOT, 'props', 'sign_ratfarm.png'))
    sign_count(os.path.join(ROOT, 'props', 'sign_count.png')); calendar(os.path.join(ROOT, 'props', 'calendar.png')); poster_stamped(os.path.join(ROOT, 'props', 'poster_x.png')); sparkle(os.path.join(ROOT, 'props', 'sparkle.png'))
    for nm, im in (('snip', sticker_burst('SNIP!')), ('poof', sticker_poof()), ('excl', sticker_mark('!', RED)), ('ques', sticker_mark('?', GOLD)), ('scis', sticker_scissors()), ('coin', sticker_coin()), ('ratsign', Image.open(os.path.join(ROOT, 'props', 'sign_ratfarm.png')).convert('RGBA'))):
        build_sticker(nm, im); items.append(('sticker ' + nm, im))
    for n in ('poster', 'tails', 'sewer', 'banner', 'window', 'sign_ratfarm', 'sign_count', 'calendar', 'poster_x', 'sparkle'): items.append((n, Image.open(os.path.join(ROOT, 'props', n + '.png'))))
    for n in ('brick', 'wood', 'dirt'): items.append((n, Image.open(os.path.join(ROOT, 'textures', n + '.jpg'))))
    items.append(('backdrop', Image.open(os.path.join(ROOT, 'bg', 'hanoi.jpg'))))
    sheet(items, os.path.join(ROOT, 'assets_preview.jpg'))
    print('assets written to', ROOT)
