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


# ================================================================== SETS
# ---- H: hook plaza
house("H", -7.5, -8, [6, 4.4, 5], "#b5553a"); house("H", 1, -9.5, [7, 5, 5], "#a94d36"); house("H", 9, -8, [6, 4.4, 5], "#c0643a")
windows("H", -5.5, [-9, -6], 2.2); windows("H", -7.0, [-1.2, 3.2], 2.5); windows("H", -5.5, [7.5, 10.5], 2.2)
tree("H", -11, -4.5, 1.6); tree("H", 11.5, -5, 1.4, "#4f8f4a")
cart("H", -4.2, 0, -3.4, 25); crate("H", -6.4, 0, -3.8); crate("H", -6.25, 0.75, -3.85, 0.55, 20); barrel("H", 6.8, -2.4)
post("H", -2.6, -1.6); post("H", 3.0, -1.4)

# ---- A: story plaza, sewer, fancy mansion
house("A", -8.5, -8, [6, 4.4, 5], "#b5553a"); house("A", 9, -8, [6, 4.4, 5], "#c0643a"); house("A", 0.5, -8.5, [7, 5, 5], "#d4a53c")
windows("A", -5.5, [-10, -7], 2.2); windows("A", -6.0, [-0.8, 1.8], 2.6); windows("A", -5.5, [7.5, 10.5], 2.2)
box("A", 0.5, 0, -4.6, [1.5, 0.02, 2.0], color="#a8283c")
box("A", 0.5, 0, -5.5, [3.2, 0.2, 0.9], color="#d8d0c4"); box("A", 0.5, 0.2, -5.75, [2.6, 0.2, 0.5], color="#cfc6b8")
tree("A", -1.9, -5.1, 0.7, "#3f8f4a"); tree("A", 2.9, -5.1, 0.7, "#3f8f4a")
post("A", -4.6, -3.1, 6.9, "#5a3a2a"); post("A", 4.6, -3.1, 6.9, "#5a3a2a"); plane("A", "banner.png", 0, 5.2, -3.05, 8.6, 1.62)
wall("A", 3.6, 0, -2.6, [3.4, 2.3, 0.5], "brick.jpg", [3, 2]); plane("A", "sewer.png", 3.6, 0, -2.33, 1.7, 1.7)
for x, y, s_ in ((2.1, 1.7, 0.5), (5.0, 2.0, 0.4), (4.7, 0.4, 0.35), (2.6, 0.5, 0.3)): plane("A", "sparkle.png", x, y, -2.3, s_, s_)
cart("A", -6.4, 0, -3.4, 25); crate("A", -8.2, 0, -3.8); barrel("A", 7.4, -2.2); post("A", -2.4, -1.8); post("A", 6.4, -0.6)
tree("A", -12.5, -4.5, 1.6); tree("A", 12.5, -5, 1.4, "#4f8f4a")

# ---- B: bounty office (square footprint: the roof overhang stays small, so the front wall is lit)
house("B", 0, -13.5, [8, 6, 8], "#8a4a3a"); house("B", -10.5, -10, [5, 4, 5], "#b5553a"); house("B", 10.5, -10, [5, 4, 5], "#c0643a")
windows("B", -9.5, [-3.0, 3.0], 2.8)
post("B", -1.9, -0.6, 2.8); plane("B", "poster.png", -1.9, 1.15, -0.52, 1.0, 1.33)
crate("B", 3.4, 0, -2.0); crate("B", 3.55, 0.75, -2.05, 0.55, 15); barrel("B", 4.4, -1.4); tree("B", -8, -5, 1.5); tree("B", 8.5, -5, 1.4, "#4f8f4a"); post("B", 6.0, -0.8)

# ---- D: tail counter
house("D", 0, -12, [8, 5, 8], "#8a4a3a"); windows("D", -8.0, [-3.0, 3.0], 2.4)
box("D", 0, 0, -2.2, [5.2, 0.75, 0.9], texture="wood.jpg", repeat=[4, 1])
for x in (-1.7, 0, 1.7): plane("D", "tails.png", x, 0.75, -1.6, 1.5, 1.05)
for x in (-0.85, 0.85): plane("D", "tails.png", x, 1.3, -1.62, 1.5, 1.05)
plane("D", "tails.png", 0, 1.85, -1.64, 1.5, 1.05)
plane("D", "sign_count.png", 0, 3.1, -1.7, 2.4, 1.7)
post("D", -3.9, -1.2, 1.7); plane("D", "calendar.png", -3.9, 1.7, -1.12, 1.2, 1.39)
crate("D", -5.5, 0, -2.8); barrel("D", 5.4, -2.0); tree("D", -9, -6, 1.5); tree("D", 9.5, -6, 1.4, "#4f8f4a")

# ---- C: farm (grass yard, dirt pen z -12..-3, red barn)
box("C", 0, 0, -8, [70, 0.06, 56], texture="grass.jpg", repeat=[18, 14])
box("C", 0, 0, -7.5, [16, 0.08, 9], texture="dirt.jpg", repeat=[4, 2])
house("C", 0, -21, [8, 6, 8], "#5a3a3a", color="#b8473a"); windows("C", -17.0, [-2.4, 2.4], 2.6)
wall("C", 0, 0.06, -12, [16, 1.1, 0.25], "wood.jpg", [8, 1]); wall("C", -8, 0.06, -7.5, [0.25, 1.1, 9], "wood.jpg", [4, 1]); wall("C", 8, 0.06, -7.5, [0.25, 1.1, 9], "wood.jpg", [4, 1])
tree("C", -14, -10, 1.9); tree("C", 15, -12, 1.8, "#4f8f4a"); tree("C", -9, -16, 2.0, "#5a944a"); tree("C", 10, -17, 1.5, "#4f8f4a")
cart("C", 5.8, 0.08, -4.8, -40); crate("C", -5, 0.06, -1.4); crate("C", -4.85, 0.81, -1.45, 0.55, 18); barrel("C", 6.9, -1.0, 0.06)

# ---- E: scrapped bounty yard
house("E", 0, -13.5, [8, 6, 8], "#8a4a3a"); windows("E", -9.5, [-3.0, 3.0], 2.8)
post("E", -0.5, -0.6, 2.8); plane("E", "poster_x.png", -0.5, 1.15, -0.52, 1.0, 1.33)
tree("E", -8, -5, 1.5); tree("E", 8.5, -5, 1.4, "#4f8f4a"); crate("E", 4.6, 0, -2.0); barrel("E", 5.6, -1.5); post("E", 7, -0.8)

# ================================================================== CHARACTERS
human("offH", "official", pos("H", 0, 0, 0), face="smug")
human("fr", "official", pos("A", -2.8, 0, 0.6))
human("boss", "official", pos("B", -0.4, 0, 0), face="smug")
human("bossE", "official", pos("E", 0.55, 0, 0), face="nervous")
human("insp", "inspector", pos("A", -12, 0, 1.6))
human("h1", "hunter", pos("B", -9, 0, 1.8), face="happy")
human("h2", "hunter2", pos("B", -10, 0, 0.9), face="happy")
human("h3", "hunter", pos("B", -11, 0, 2.6), face="happy")

# hook rats (H): hk1/hk2 stand beside the official in the first shot, the rest flood in from the sides
HK = [("hk1", "rat", (-1.0, 1.0), True), ("hk2", "rat", (1.0, 1.1), False),
      ("hk3", "ratnt", (-6.5, 1.8), True), ("hk4", "rat", (6.5, 1.9), False), ("hk5", "ratnt", (-6.5, 2.5), True),
      ("hk6", "rat", (6.5, 2.6), False), ("hk7", "ratnt", (-6.5, 0.4), True), ("hk8", "rat", (6.5, 0.5), False),
      ("hk9", "ratnt", (-6.5, 3.1), True), ("hk10", "rat", (6.5, 3.2), False)]
HK_END = {"hk3": -1.6, "hk4": 1.6, "hk5": -0.55, "hk6": 0.65, "hk7": -1.9, "hk8": 1.9, "hk9": -1.25, "hk10": 1.2}
for cid, kind, (x, z), fl in HK: rat(cid, kind, pos("H", x, 0, z), h=0.7, flip=fl)
HK2 = [("hk11", "ratnt", (-7.5, 2.6), True, -2.3), ("hk12", "rat", (7.5, 2.7), False, 2.2), ("hk13", "ratnt", (-8, 3.8), True, -0.1), ("hk14", "rat", (8, 1.5), False, 0.5)]
for cid, kind, (x, z), fl, xe in HK2: rat(cid, kind, pos("H", x, 0, z), h=0.7, flip=fl)

# A rats: r1-r3 hide behind the sewer wall, r4 waits inside the mansion, n1-n5 wait far away, hn is the hero
for cid, x in (("r1", 3.1), ("r2", 3.8), ("r3", 4.4)): rat(cid, "rat", pos("A", x, 0, -3.4))
rat("r4", "rat", pos("A", -0.8, 2.55, -7.0))
for i in range(5): rat("n%d" % (i + 1), "ratnt", pos("A", 60 + i, 0, 2.5), h=0.7)
rat("hn", "ratnt", pos("A", -40, 0, 3.0), h=0.85)
rat("nx", "ratnt", pos("D", 7.0, 0, 0.3), face="sneaky")

# C rats
rat("mom", "ratmom", pos("C", 2.7, 0.06, 0.0), h=0.85)
for cid, x, z in (("ba1", 3.6, 0.9), ("ba2", 4.2, 1.3), ("ba3", 4.8, 0.2)): rat(cid, "rat", pos("C", x, 0.06, z), h=0.32)
rat("cr", "rat", pos("C", 2.9, 0.06, 0.5), h=0.85)
rat("hn2", "ratnt", PARK, h=0.85, face="shocked")
PEN = [("p1", -1.8, -6.5), ("p2", -0.9, -4.8), ("p3", 0.2, -7.2), ("p4", 1.2, -5.2), ("p5", 1.9, -7.0), ("p6", -0.5, -3.6), ("p7", 1.6, -3.8), ("p8", -1.8, -8.2), ("p9", 0.8, -8.4)]
for i, (cid, x, z) in enumerate(PEN):
    left = i % 2 == 0
    rat(cid, "ratnt" if i % 3 else "rat", pos("C", -11 if left else 11, 0.08, z), flip=left)
for i in range(4): rat("s%d" % (i + 1), "ratnt" if i % 2 else "rat", pos("C", 7.5 + i * 1.1, 0.06, -2.4))
# E rats: already standing around the yard, just outside the tight shot of the poster
E_REST = [(-1.3, 3.0), (1.4, 3.2), (-2.0, 2.4), (2.1, 2.6), (-1.1, 4.0), (1.2, 4.2), (-2.8, 1.6), (2.9, 1.8)]
for i, (x, z) in enumerate(E_REST): rat("e%d" % (i + 1), "ratnt" if i % 2 else "rat", pos("E", x, 0, z), flip=(x < 0))

# stickers (parked under the ground until needed)
sticker("excl", "excl", 0.7); sticker("coin", "coin", 0.34); sticker("scis", "scis", 0.4); sticker("snip", "snip", 0.8); sticker("poof", "poof", 0.8)
sticker("ratsign", "ratsign", 1.28)

# ================================================================== SHOTS
# ---- 0-1  hook: the official proudly "wins", then the rats flood in
s = shot("0", target="offH", hw=0.24, yaw=12, pitch=3, zoom=7, pan=(-16, 6), fy=0.1)
act(s, 0.0, "offH", face="smug", pose=dict(armR=-100, armL=8, head=0, body=0))
act(s, 0.7, "offH", pose=dict(armR=-150), hop=0.1)

s = shot("the more rats Hanoi#2", out="dissolve", target="offH", hw=0.16, yaw=-8, pitch=6, zoom=-6, pan=(10, 0), fy=0.2)
act(s, 0.0, "offH", face="shocked", pose=dict(armR=0, armL=0, head=0)); act(s, 0.05, "offH", shake=0.9)
show(s, 0.12, "excl", pos("H", 0.55, 2.0, 0.2), hop=0.1)
for (cid, kind, (x, z), fl), t_, ov in zip(HK[2:], (0.0, 0.0, 0.15, 0.2, 0.3, 0.35, 0.5, 0.55), (0.8, 0.8, 0.9, 0.9, 0.85, 0.85, 0.8, 0.8)):
    go(s, t_, cid, pos("H", HK_END[cid], 0, z), ov)

# ---- 2-3  1902 establishing, shiny new sewer
s = shot("It's 1902", anchor=pos("A", 0.5, 1.9, -2.0), dist=22, yaw=14, pitch=9, zoom=4, pan=(12, 0), fy=0.02)
hide(s, 0.3, "excl"); go(s, 0.3, "fr", pos("A", 1.4, 0, 0.5), 1.6)

s = shot("a shiny new sewer", anchor=pos("A", 2.4, 1.3, -1.2), dist=8.0, yaw=-12, pitch=4, zoom=6, pan=(-12, 4), fy=0.05)
act(s, 0.15, "fr", face="happy", pose=dict(armR=-95, armL=0, head=-4))

# ---- 4  rats love it
s = shot("Rats love it", anchor=pos("A", 3.6, 0.9, -2.1), dist=5.4, yaw=8, pitch=6, zoom=8, pan=(0, -10), fy=0.05)
act(s, 0.0, "fr", face="neutral", pose=dict(armR=0, head=0)); go(s, 0.05, "fr", pos("A", -7, 0, 0.5), 1.3)
go(s, 0.0, "r1", pos("A", 3.0, 0, -1.6), 0.5, hop=0.2)
go(s, 0.15, "r2", pos("A", 3.9, 0, -1.4), 0.5, hop=0.2)
go(s, 0.3, "r3", pos("A", 4.5, 0, -1.5), 0.5, hop=0.2)

# ---- 5  they climb into the fancy homes (front steps, through the door)
s = shot("They climb", out="dissolve", anchor=pos("A", 0.5, 1.3, -5.6), dist=9.0, yaw=-10, pitch=4, zoom=6, pan=(-10, -6), fy=0.0)
go(s, 0.0, "r1", pos("A", 1.0, 0, -4.6), 0.6); go(s, 0.65, "r1", pos("A", 0.9, 0.2, -5.3), 0.28, hop=0.08)
go(s, 0.95, "r1", pos("A", 0.9, 0.4, -5.75), 0.28, hop=0.08); go(s, 1.25, "r1", pos("A", 0.9, 0.4, -6.5), 0.22)
go(s, 0.1, "r2", pos("A", 1.9, 0, -4.5), 0.8); go(s, 0.95, "r2", pos("A", 0.2, 0.2, -5.3), 0.3, hop=0.08)
go(s, 1.28, "r2", pos("A", 0.2, 0.4, -5.75), 0.28, hop=0.08); go(s, 1.58, "r2", pos("A", 0.2, 0.4, -6.5), 0.22)
go(s, 0.2, "r3", pos("A", 2.3, 0, -4.4), 0.9); go(s, 1.15, "r3", pos("A", 1.5, 0.2, -5.3), 0.3, hop=0.08)
go(s, 1.48, "r3", pos("A", 1.5, 0.4, -5.75), 0.28, hop=0.08); go(s, 1.8, "r3", pos("A", 1.5, 0.4, -6.5), 0.22)
show(s, 1.0, "r4", pos("A", -0.8, 2.55, -5.9), hop=0.18)

# ---- 6-9  the offer (B)
s = shot("So the government", anchor=pos("B", -1.15, 1.2, -0.2), dist=8.0, yaw=-8, pitch=4, zoom=5, pan=(10, 4), fy=0.1)
act(s, 0.0, "boss", face="smug", pose=dict(armL=20, armR=0, head=4))
hide(s, 0.0, "fr")                                                  # the French official has left A
for i in range(5): act(s, 0.0, "n%d" % (i + 1), to=pos("A", (-1.5, -1.0, -0.5, -2.0, 0.5)[i], 0, (2.2, 3.0, 2.4, 3.2, 2.8)[i]), over=0.02, walk=False)   # A is off camera now

s = shot("One cent", anchor=pos("B", -1.2, 1.55, -0.5), dist=5.6, yaw=10, pitch=3, zoom=8, pan=(0, -6), fy=0.18)
act(s, 0.0, "boss", face="happy", pose=dict(armL=95, armR=0, head=-3))

s = shot("Just bring us", target="boss", hw=0.34, yaw=-6, pitch=3, zoom=9, pan=(-8, 0), fy=0.1)
act(s, 0.0, "boss", face="smug", pose=dict(armL=0, armR=-70, head=5))

s = shot("Hunters go", out="dissolve", anchor=pos("B", 0.5, 1.0, 0.5), dist=14, yaw=14, pitch=5, zoom=-5, pan=(14, 0), fy=0.05)
act(s, 0.0, "boss", face="shocked", pose=dict(armL=40, armR=-40, head=0))
for cid, t_, z, x1 in (("h1", 0.0, 1.8, 9), ("h2", 0.25, 0.9, 10), ("h3", 0.5, 2.6, 11)):
    act(s, t_, cid, face="shouting", pose=dict(armL=120, armR=-120)); go(s, t_, cid, pos("B", x1, 0, z), 1.0)
    for k in (0.2, 0.5): act(s, t_ + k, cid, hop=0.12)

# ---- 10-13  turn-in day (D)
s = shot("On June", anchor=pos("D", -3.9, 2.4, -1.1), dist=4.4, yaw=6, pitch=2, zoom=10, pan=(0, -6), fy=0.05)
act(s, 0.15, "boss", to=pos("D", 1.7, 0, -0.6), over=0.02, walk=False, face="happy", pose=dict(armL=0, armR=0, head=0))
for cid, z in (("h1", 0.6), ("h2", 1.2), ("h3", 1.9)): act(s, 0.15, cid, to=pos("D", -6.5, 0, z), over=0.02, walk=False, face="happy", pose=dict(armL=0, armR=0))

s = shot("they turn in", anchor=pos("D", 0, 2.5, -1.5), dist=8.5, yaw=8, pitch=2, zoom=7, pan=(0, -8), fy=0.0)

s = shot("In one single day", out="dissolve", anchor=pos("D", 0, 1.5, -1.2), dist=13, yaw=-10, pitch=5, zoom=-4, pan=(12, 0), fy=0.03)
act(s, 0.0, "boss", face="happy", pose=dict(armL=130, armR=-130, head=0))
for cid, t_, x, z in (("h1", 0.0, -2.2, 0.6), ("h2", 0.15, -1.3, 1.2), ("h3", 0.3, -2.7, 1.9)):
    act(s, t_, cid, face="happy", pose=dict(armL=125, armR=-125)); go(s, t_, cid, pos("D", x, 0, z), 0.6)
    for k in (0.7, 1.0): act(s, t_ + k, cid, hop=0.18)
act(s, 0.95, "boss", face="happy", pose=dict(armL=150, armR=-150, head=-5), hop=0.2)          # "Victory?"
go(s, 0.9, "nx", pos("D", 3.6, 0, 0.3), 0.5)

# ---- 14-17  inspectors (A)
s = shot("Then inspectors", target="insp", hw=0.2, yaw=-14, pitch=5, zoom=5, pan=(12, 4), fy=0.12)
go(s, 0.0, "insp", pos("A", -5.6, 0, 1.2), 1.3)
act(s, 1.1, "insp", face="confused", pose=dict(head=8, armR=-40)); show(s, 1.2, "excl", pos("A", -5.6, 2.05, 1.2), hop=0.1)

s = shot("Rats. Alive", anchor=pos("A", -4.5, 0.55, 2.4), dist=6.5, yaw=-6, pitch=6, zoom=6, pan=(-8, 0), fy=0.05)
for cid, t_, xe, z, ov in (("n1", 0.0, -4.6, 2.2, 0.7), ("n2", 0.1, -3.8, 3.0, 0.8), ("n3", 0.2, -3.2, 2.4, 0.8), ("n4", 0.3, -5.1, 3.2, 0.7)):
    act(s, t_, cid, face="happy"); go(s, t_, cid, pos("A", xe, 0, z), ov)
for cid, t_ in (("n1", 0.85), ("n3", 1.0), ("n2", 1.15), ("n4", 1.3)): act(s, t_, cid, hop=0.16)
act(s, 0.0, "insp", face="confused", pose=dict(head=8, armR=-40))

s = shot("Running through", anchor=pos("A", -8.0, 0.4, 3.0), dist=5.0, yaw=-8, pitch=-1.5, zoom=8, pan=(0, 0), fy=0.0)
hide(s, 0.0, "excl")
for cid, t_ in (("n1", 0.0), ("n2", 0.05), ("n3", 0.1), ("n4", 0.15)):          # the pack bolts left, the camera chases it
    z = {"n1": 2.2, "n2": 3.0, "n3": 2.4, "n4": 3.2}[cid]; go(s, t_, cid, pos("A", -13.5, 0, z), 1.1)
act(s, 0.0, "hn", to=pos("A", -1.5, 0, 3.2), over=0.02, walk=False, face="happy")

s = shot("with no tails", out="dissolve", anchor=pos("A", -1.5, 0.55, 3.2), dist=4.6, yaw=-4, pitch=4, zoom=8, pan=(0, -6), fy=0.05)
act(s, 0.2, "hn", hop=0.15); act(s, 0.55, "hn", face="sneaky")
act(s, 0.0, "h1", to=pos("C", 0, 0.06, 0), over=0.02, walk=False, face="sneaky", pose=dict(armR=-130, armL=0, head=5))

# ---- 18-23  the farm (C)
s = shot("You see", target="h1", hw=0.22, yaw=-14, pitch=5, zoom=5, pan=(12, 6), fy=0.12)
show(s, 0.7, "coin", pos("C", 0.62, 1.24, 0.1), hop=0.15)
hide(s, 1.55, "coin"); go(s, 1.5, "h1", pos("C", -2.8, 0.06, -0.2), 0.6)

s = shot("A rat without", anchor=pos("C", 0.3, 0.5, 0.5), dist=6.2, yaw=10, pitch=8, zoom=6, pan=(-8, 0), fy=0.03)
act(s, 0.0, "mom", face="happy"); go(s, 0.0, "mom", pos("C", -0.15, 0.06, 0.0), 0.9)
for cid, t_, x, z in (("ba1", 0.2, 0.85, 0.9), ("ba2", 0.35, 1.3, 0.6), ("ba3", 0.5, 1.05, 1.3)): go(s, t_, cid, pos("C", x, 0.06, z), 0.7)
for cid, t_ in (("ba1", 1.1), ("ba2", 1.3), ("ba3", 1.5)): act(s, t_, cid, hop=0.14)

s = shot("and every baby", anchor=pos("C", 0.95, 0.35, 0.9), dist=3.8, yaw=14, pitch=6, zoom=10, pan=(-6, 0), fy=0.05)
for cid, t_ in (("ba1", 0.0), ("ba2", 0.3), ("ba3", 0.6)): act(s, t_, cid, hop=0.22)
for cid, t_, x in (("ba1", 1.0, 4.5), ("ba3", 1.1, 4.8), ("ba2", 1.25, 4.2)): go(s, t_, cid, pos("C", x, 0.06, 0.9), 0.9, flip=True)
go(s, 0.9, "mom", pos("C", 4.6, 0.06, 0.0), 1.1, flip=True)
go(s, 0.4, "h1", pos("C", -0.4, 0.06, 0.0), 0.8)

s = shot("So hunters cut", anchor=pos("C", 0.4, 0.9, 0.4), dist=7.5, yaw=-10, pitch=5, zoom=5, pan=(6, 0), fy=0.05)
act(s, 0.0, "h1", face="sneaky", pose=dict(armR=-105, armL=0, head=0))
go(s, 0.0, "cr", pos("C", 1.15, 0.06, 0.5), 0.8)
show(s, 0.75, "scis", pos("C", 0.37, 0.92, 0.15), hop=0.06)
show(s, 1.15, "snip", pos("C", 0.55, 1.25, 0.35), hop=0.12); show(s, 1.15, "poof", pos("C", 1.15, 0.1, 0.6), hop=0.05)
act(s, 1.15, "cr", to=PARK, over=0.02, walk=False); act(s, 1.15, "hn2", to=pos("C", 1.15, 0.06, 0.5), over=0.02, walk=False, face="shocked")
hide(s, 1.5, "snip"); hide(s, 1.5, "poof"); hide(s, 1.5, "scis")
act(s, 1.65, "hn2", face="happy", hop=0.25); act(s, 1.65, "h1", face="happy", pose=dict(armR=0))
go(s, 1.9, "hn2", pos("C", 9, 0.06, 1.0), 1.2, flip=True)

s = shot("Outside the city", anchor=pos("C", 0, 0.8, -6.0), dist=10, yaw=10, pitch=6, zoom=4, pan=(8, 0), fy=0.03)
show(s, 0.0, "ratsign", pos("C", 0, 0.08, -8.95), hop=0.25)
act(s, 0.0, "h2", to=pos("C", 6.0, 0.06, -2.4), over=0.02, walk=False, face="sneaky", pose=dict(armL=0, armR=0, head=4))
go(s, 0.0, "h1", pos("C", -3.0, 0.06, -2.0), 0.8); act(s, 0.4, "h1", face="smug", pose=dict(armL=25, armR=-25))
for i, (cid, x, z) in enumerate(PEN):
    t_ = 0.1 + i * 0.1; go(s, t_, cid, pos("C", x, 0.08, z), 1.1)
    act(s, 1.5 + (i % 4) * 0.15, cid, hop=0.14)

s = shot("Others smuggled", out="dissolve", anchor=pos("C", 2.0, 0.8, -2.4), dist=7.5, yaw=-16, pitch=5, zoom=6, pan=(-12, 0), fy=0.03)
go(s, 0.0, "h2", pos("C", 0.9, 0.06, -2.4), 2.0)
for cid, t_, x, ov in (("s1", 0.3, 1.8, 1.9), ("s2", 0.5, 2.6, 1.8), ("s3", 0.7, 3.3, 1.7), ("s4", 0.9, 3.9, 1.5)): go(s, t_, cid, pos("C", x, 0.06, -2.4), ov)

# ---- 24-25  scrapped (E)
s = shot("The bounty", anchor=pos("E", 0.0, 1.5, -0.5), dist=5.0, yaw=-6, pitch=3, zoom=6, pan=(6, 0), fy=0.12)
act(s, 0.0, "bossE", face="nervous", pose=dict(armL=40, armR=-40, head=6))

s = shot("The rats stayed", out="dissolve", anchor=pos("E", 0.3, 0.9, 1.5), dist=11, yaw=6, pitch=6, zoom=-3, pan=(-4, 0), fy=0.03)
act(s, 0.0, "bossE", face="nervous", pose=dict(armL=0, armR=0, head=8)); act(s, 0.1, "bossE", shake=0.8)
for i in range(8): act(s, 0.05 + i * 0.09, "e%d" % (i + 1), hop=0.16)

# ---- 26-27  counted tails (D)
s = shot("Because the city", target="boss", hw=0.2, yaw=-6, pitch=3, zoom=5, pan=(8, 0), fy=0.12)
act(s, 0.0, "boss", face="confused", pose=dict(armL=0, armR=-50, head=-7))

s = shot("It counted tails", out="dissolve", anchor=pos("D", 0, 2.5, -1.5), dist=7.0, yaw=6, pitch=3, zoom=10, pan=(0, -6), fy=0.05)

# ---- 28  the loop: more rats than ever (H)
s = shot("And that's why", target="offH", hw=0.2, yaw=12, pitch=3, zoom=-5, pan=(-16, 6), fy=0.1)
act(s, 0.0, "offH", face="shocked", pose=dict(armR=0, armL=0, head=0)); act(s, 0.1, "offH", shake=1.4)
for i, cid in enumerate(("hk1", "hk2", "hk3", "hk4", "hk5", "hk6", "hk7", "hk8", "hk9", "hk10")): act(s, 0.15 + i * 0.12, cid, hop=0.14)
for (cid, kind, (x, z), fl, xe), t_ in zip(HK2, (0.3, 0.5, 0.7, 0.9)): go(s, t_, cid, pos("H", xe, 0, z), 0.7)

# ================================================================== SPEC
spec = {
    "fps": 30,
    "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -17},
    "words": "audio/words.json",
    "captions": {"wordsPer": 1},
    "font": "fonts/Montserrat-ExtraBold.ttf",
    "contactShadow": 0.6,
    "moods": {
        "day": {"sun": {"azimuth": 35, "elevation": 50, "color": "#ffe0b5", "intensity": 2.4},
                "sky": {"top": "#5f86d8", "horizon": "#f2b98a"},
                "fill": {"sky": "#8ea2ff", "ground": "#6a3b6e", "intensity": 1.1}},
        "night": {"sun": {"azimuth": -40, "elevation": 40, "color": "#a9bcff", "intensity": 2.1},
                  "sky": {"top": "#1d2a6e", "horizon": "#6a63b8"},
                  "fill": {"sky": "#7686ee", "ground": "#503f94", "intensity": 1.7}, "exposure": 1.3},
        "dusk": {"sun": {"azimuth": -20, "elevation": 38, "color": "#ffa66e", "intensity": 2.3},
                 "sky": {"top": "#3f4f9e", "horizon": "#f0926a"},
                 "fill": {"sky": "#7d7ee0", "ground": "#5e3668", "intensity": 1.35}, "exposure": 1.12},
    },
    "lighting": [{"t": 0, "mood": "day"}, {"t": "say:You see", "mood": "night", "fade": 0.8},
                 {"t": "say:Outside the city", "mood": "dusk", "fade": 0.8}, {"t": "say:And that's why", "mood": "day", "fade": 0.6}],
    "ground": {"texture": TEX + "cobble.jpg", "repeat": [525, 525], "size": 1400},
    "backdrop": {"image": "bg/hanoi.jpg", "blur": 5},
    "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- sanity report: shot timing + actions that overrun or overlap
starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
print("shot  start   dur  phrase")
for k, s in enumerate(shots):
    end = starts[k + 1] if k + 1 < len(shots) else DURATION
    s["_dur"] = end - starts[k]
    print("S%02d  %6.2f %5.2f  %s" % (k, starts[k], s["_dur"], s["_phrase"]))
    if s["_dur"] < 0.7: print("   ! very short shot (mostly glide)")
keys = {}
for k, s in enumerate(shots):
    for a in s["actions"]:
        if "to" in a: keys.setdefault(a["who"], []).append((starts[k] + a["at"], a["over"], k, a["to"]))
        if a["at"] > s["_dur"] + 0.25: print("   ! S%02d action at %.2f s runs past the shot (%.2f s): %s %s" % (k, a["at"], s["_dur"], a["who"], list(a)[2:]))
for who, ks in keys.items():
    ks.sort()
    for (t0, ov, k0, _), (t1, ov1, k1, _) in zip(ks, ks[1:]):
        if t0 + ov > t1 + 0.06: print("   ! %s: move from S%02d (%.2f+%.2f s) overlaps next move in S%02d at %.2f s" % (who, k0, t0, ov, k1, t1))
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
