#!/usr/bin/env python3
"""Generate short.json for video 01 (Hanoi rats bounty).
usage: build_short.py <project folder>   (reads audio/words.json, writes short.json)

Six sets 70 units apart in one world: H hook plaza, A story plaza (sewer + mansion),
B bounty office, D tail counter, C farm, E scrapped-bounty yard.  Every rat lives in one
set; only the few humans that change sets are moved while the camera is elsewhere.
"""
import json, os, sys, re

P = sys.argv[1]
X = dict(H=-70, A=0, B=70, D=140, C=210, E=280)
PARK = [0, -60, 0]
TEX = "textures/"
chars, props, shots = [], [], []


def pos(loc, x=0.0, y=0.0, z=0.0):
    return [round(X[loc] + x, 3), round(y, 3), round(z, 3)]


# ------------------------------------------------------------------ characters
def human(cid, puppet, at, face="neutral", h=1.8):
    chars.append(dict(id=cid, puppet="puppets/" + puppet, pos=at, height=h, face=face))


def rat(cid, kind, at, face="happy", h=0.55, flip=False):
    c = dict(id=cid, puppet="puppets/" + kind, pos=at, height=h, face=face)
    if flip: c["flip"] = True
    chars.append(c)


def sticker(cid, name, h):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=PARK, height=h, face="default"))


# ------------------------------------------------------------------ props
def house(loc, x, z, size, roof, wall="plaster.jpg", color=None):
    p = dict(type="house", pos=pos(loc, x, 0, z), size=size, roof=roof, door="#7a5890")
    if color: p["color"] = color
    else: p["wall"] = TEX + wall
    props.append(p)


def plane(loc, img, x, y, z, w, h):
    props.append(dict(type="plane", image="props/" + img, pos=pos(loc, x, y, z), size=[w, h]))


def windows(loc, front_z, xs, y):
    for x in xs: plane(loc, "window.png", x, y, front_z + 0.04, 1.1, 1.62)


def tree(loc, x, z, scale, color="#5f9a4c"):
    props.append(dict(type="tree", pos=pos(loc, x, 0, z), scale=scale, color=color))


def crate(loc, x, y, z, size=0.75, rot=0):
    props.append(dict(type="crate", pos=pos(loc, x, y, z), size=size, rotY=rot, texture=TEX + "wood.jpg"))


def barrel(loc, x, z, y=0):
    props.append(dict(type="barrel", pos=pos(loc, x, y, z)))


def post(loc, x, z, h=2.6, color="#4a3a3f"):
    props.append(dict(type="post", pos=pos(loc, x, 0, z), h=h, color=color))


def box(loc, x, y, z, size, color=None, texture=None, repeat=None):
    p = dict(type="box", pos=pos(loc, x, y, z), size=size)
    if color: p["color"] = color
    if texture: p["texture"] = TEX + texture
    if repeat: p["repeat"] = repeat
    props.append(p)


def wall(loc, x, y, z, size, texture, repeat):
    props.append(dict(type="wall", pos=pos(loc, x, y, z), size=size, texture=TEX + texture, repeat=repeat))


def cart(loc, x, y, z, rot):
    props.append(dict(type="model", file="models/cart.glb", pos=pos(loc, x, y, z), height=1.25, rotY=rot))


# ------------------------------------------------------------------ timing (same tokenising as render.mjs)
WORDS = json.load(open(os.path.join(P, "audio", "words.json"), encoding="utf-8"))
TOK = lambda s: re.sub(r"[^a-z0-9' ]+", " ", s.lower().replace("‘", "'").replace("’", "'")).split()
WN = ["".join(TOK(w["w"])) for w in WORDS["words"]]
DURATION = WORDS["duration"]


def say(phrase):
    m = re.match(r"^(.+?)(?:#(\d+))?$", phrase); want = TOK(m.group(1)); nth = int(m.group(2) or 1); seen = 0
    for i in range(len(WN) - len(want) + 1):
        if all(WN[i + j] == t for j, t in enumerate(want)):
            seen += 1
            if seen == nth: return WORDS["words"][i]["t0"]
    sys.exit('phrase not found: "%s"' % phrase)


# ------------------------------------------------------------------ shot helpers
def shot(start, out=None, target=None, anchor=None, hw=None, dist=None, yaw=0, pitch=6, zoom=6, pan=(0, 0), fy=None, fx=None):
    s = {"start": "say:" + start if start != "0" else 0}
    if target: s["target"] = target
    if anchor: s["anchor"] = anchor
    if hw: s["headWidth"] = hw
    if dist: s["distance"] = dist
    s.update(yaw=yaw, pitch=pitch, zoom=zoom, pan=list(pan))
    if fy is not None: s["frameY"] = fy
    if fx is not None: s["frameX"] = fx
    if out: s["out"] = out
    s["actions"] = []; s["_phrase"] = start
    shots.append(s); return s


def act(s, at, who, **kw):
    s["actions"].append(dict(at=round(at, 3), who=who, **kw))


def go(s, at, who, p, over, walk=True, **kw):
    act(s, at, who, to=p, over=over, walk=walk, **kw)


def show(s, at, who, p, hop=0.12):
    act(s, at, who, to=p, over=0.02, walk=False, hop=hop)


def hide(s, at, who):
    act(s, at, who, to=PARK, over=0.02, walk=False)

