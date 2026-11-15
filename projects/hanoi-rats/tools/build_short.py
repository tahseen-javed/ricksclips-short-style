#!/usr/bin/env python3
"""Generate short.json for video 01 (Hanoi rats bounty).
usage: build_short.py <project folder>   (reads audio/words.json, writes short.json)

Six sets 70 units apart in one world: H hook plaza, A story plaza (sewer + mansion),
B bounty office, D tail counter, C farm, E scrapped-bounty yard.  Every rat lives in one
set; only the few humans that change sets are teleported while the camera is elsewhere.
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
def house(loc, x, z, size, roof, wall="plaster.jpg"):
    props.append(dict(type="house", pos=pos(loc, x, 0, z), size=size, wall=TEX + wall, roof=roof))


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
    s = {"start": "say:" + start if isinstance(start, str) and start != "0" else 0}
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
windows("A", -5.5, [-10, -7], 2.2); windows("A", -6.0, [-1.0, 2.0], 2.6); windows("A", -5.5, [7.5, 10.5], 2.2)
box("A", 0.5, 0, -4.6, [1.5, 0.02, 2.0], color="#a8283c")
box("A", 0.5, 0, -5.5, [3.2, 0.2, 0.9], color="#d8d0c4"); box("A", 0.5, 0.2, -5.75, [2.6, 0.2, 0.5], color="#cfc6b8")
tree("A", -1.9, -5.1, 0.7, "#3f8f4a"); tree("A", 2.9, -5.1, 0.7, "#3f8f4a")
post("A", -4.6, -3.1, 4.6, "#5a3a2a"); post("A", 4.6, -3.1, 4.6, "#5a3a2a"); plane("A", "banner.png", 0, 3.0, -3.05, 8.6, 1.62)
wall("A", 3.6, 0, -2.6, [3.4, 2.3, 0.5], "brick.jpg", [3, 2]); plane("A", "sewer.png", 3.6, 0, -2.33, 1.7, 1.7)
for x, y, s_ in ((2.1, 1.7, 0.5), (5.0, 2.0, 0.4), (4.7, 0.4, 0.35), (2.6, 0.5, 0.3)): plane("A", "sparkle.png", x, y, -2.3, s_, s_)
cart("A", -6.4, 0, -3.4, 25); crate("A", -8.2, 0, -3.8); barrel("A", 7.4, -2.2); post("A", -2.4, -1.8); post("A", 6.4, -0.6)
tree("A", -12.5, -4.5, 1.6); tree("A", 12.5, -5, 1.4, "#4f8f4a")

# ---- B: bounty office
house("B", 0, -12.5, [9, 6, 6], "#8a4a3a"); house("B", -10.5, -10, [5, 4, 5], "#b5553a"); house("B", 10.5, -10, [5, 4, 5], "#c0643a")
windows("B", -9.5, [-3.2, 3.2], 2.8)
post("B", -1.9, -0.6, 2.8); plane("B", "poster.png", -1.9, 1.15, -0.52, 1.0, 1.33)
crate("B", 3.4, 0, -2.0); crate("B", 3.55, 0.75, -2.05, 0.55, 15); barrel("B", 4.4, -1.4); tree("B", -8, -5, 1.5); tree("B", 8.5, -5, 1.4, "#4f8f4a"); post("B", 6.0, -0.8)

# ---- D: tail counter
house("D", 0, -11, [9, 5, 5], "#8a4a3a")
box("D", 0, 0, -2.2, [5.2, 0.75, 0.9], texture="wood.jpg", repeat=[4, 1])
for x in (-1.7, 0, 1.7): plane("D", "tails.png", x, 0.75, -1.6, 1.5, 1.05)
for x in (-0.85, 0.85): plane("D", "tails.png", x, 1.3, -1.62, 1.5, 1.05)
plane("D", "tails.png", 0, 1.85, -1.64, 1.5, 1.05)
plane("D", "sign_count.png", 0, 3.1, -1.7, 2.4, 1.7)
post("D", -3.9, -1.2, 1.7); plane("D", "calendar.png", -3.9, 1.7, -1.12, 1.2, 1.39)
crate("D", -5.5, 0, -2.8); barrel("D", 5.4, -2.0); tree("D", -9, -6, 1.5); tree("D", 9.5, -6, 1.4, "#4f8f4a")

# ---- C: farm
box("C", 0, 0, -6, [44, 0.06, 36], texture="dirt.jpg", repeat=[11, 9])
house("C", 0, -20, [10, 6, 6], "#8a4a3a", wall="wood.jpg")
wall("C", 0, 0.06, -12, [16, 1.1, 0.25], "wood.jpg", [8, 1]); wall("C", -8, 0.06, -6.5, [0.25, 1.1, 11], "wood.jpg", [5, 1]); wall("C", 8, 0.06, -6.5, [0.25, 1.1, 11], "wood.jpg", [5, 1])
tree("C", -14, -10, 1.9); tree("C", 15, -12, 1.8, "#4f8f4a"); tree("C", -9, -16, 2.0, "#5a944a"); tree("C", 10, -17, 1.5, "#4f8f4a")
cart("C", 5.8, 0.06, -4.2, -40); crate("C", -5, 0.06, -2.4); crate("C", -4.85, 0.81, -2.45, 0.55, 18); barrel("C", 6.9, -1.6, 0.06)

# ---- E: scrapped bounty yard
house("E", 0, -13, [9, 6, 6], "#8a4a3a"); windows("E", -10, [-3.2, 3.2], 2.8)
post("E", -0.5, -0.6, 2.8); plane("E", "poster_x.png", -0.5, 1.15, -0.52, 1.0, 1.33)
tree("E", -8, -5, 1.5); tree("E", 8.5, -5, 1.4, "#4f8f4a"); crate("E", 3.6, 0, -2.0); barrel("E", 4.6, -1.5); post("E", 6, -0.8)

# ================================================================== CHARACTERS
human("offH", "official", pos("H", 0, 0, 0), face="smug")
human("fr", "official", pos("A", -2.8, 0, 0.6))
human("boss", "official", pos("B", -0.4, 0, 0), face="smug")
human("bossE", "official", pos("E", 0.9, 0, 0), face="nervous")
human("insp", "inspector", pos("A", -12, 0, 1.6))
human("h1", "hunter", pos("B", -9, 0, 1.8), face="happy")
human("h2", "hunter2", pos("B", -10, 0, 0.9), face="happy")
human("h3", "hunter", pos("B", -11, 0, 2.6), face="happy")

# hook rats (H): hk1/hk2 stand at the edges in the first shot, the rest flood in
HK = [("hk1", "rat", (-1.25, 0.7), False), ("hk2", "rat", (1.3, 0.9), True),
      ("hk3", "ratnt", (-6.5, 1.6), True), ("hk4", "rat", (6.5, 1.8), False), ("hk5", "ratnt", (-6.5, 2.0), True),
      ("hk6", "rat", (6.5, 2.3), False), ("hk7", "ratnt", (-6.5, 0.2), True), ("hk8", "rat", (6.5, 0.3), False),
      ("hk9", "ratnt", (-6.5, 2.6), True), ("hk10", "rat", (6.5, 2.7), False)]
for cid, kind, (x, z), fl in HK: rat(cid, kind, pos("H", x, 0, z), flip=fl)
for cid, kind, (x, z), fl in (("hk11", "ratnt", (-7.5, 2.2), True), ("hk12", "rat", (7.5, 2.4), False), ("hk13", "ratnt", (-8, 1.0), True), ("hk14", "rat", (8, 1.1), False)):
    rat(cid, kind, pos("H", x, 0, z), flip=fl)

# A rats: r1-r3 hide behind the sewer wall, r4 waits inside the mansion, n1-n5 wait far away, hn is the hero
for cid, x in (("r1", 3.1), ("r2", 3.8), ("r3", 4.4)): rat(cid, "rat", pos("A", x, 0, -3.4))
rat("r4", "rat", pos("A", -1.0, 2.55, -7.0))
for i in range(5): rat("n%d" % (i + 1), "ratnt", pos("A", 60 + i, 0, 2.5))
rat("hn", "ratnt", pos("A", -40, 0, 3.0), h=0.85)
rat("nx", "ratnt", pos("D", 7.0, 0, 0.3), face="sneaky")

# C rats
rat("mom", "ratmom", pos("C", 2.7, 0.06, 0.0), h=0.95)
for cid, x, z in (("ba1", 3.6, 0.9), ("ba2", 4.2, 1.3), ("ba3", 4.8, 0.2)): rat(cid, "rat", pos("C", x, 0.06, z), h=0.32)
rat("cr", "rat", pos("C", 3.6, 0.06, 0.5), h=0.85)
rat("hn2", "ratnt", PARK, h=0.85, face="shocked")
PEN = [("p1", -2.4, -6.5), ("p2", -1.2, -4.8), ("p3", 0.2, -7.2), ("p4", 1.4, -5.2), ("p5", 2.5, -7.0), ("p6", -0.6, -3.4), ("p7", 1.9, -3.6), ("p8", -2.2, -8.2), ("p9", 0.9, -8.4)]
for i, (cid, x, z) in enumerate(PEN):
    left = i % 2 == 0
    rat(cid, "ratnt" if i % 3 else "rat", pos("C", -11 if left else 11, 0.06, z), flip=left)
for i in range(4): rat("s%d" % (i + 1), "ratnt" if i % 2 else "rat", pos("C", 7.5 + i * 1.1, 0.06, -3.0))
# E rats
E_REST = [(-1.2, 1.0), (2.8, 1.1), (0.3, 1.8), (1.9, 2.0), (-0.4, 0.4), (3.2, 0.2), (-1.8, 2.2), (2.4, 2.7)]
for i in range(8): rat("e%d" % (i + 1), "ratnt" if i % 2 else "rat", pos("E", (-8 - i) if i % 2 == 0 else (8 + i), 0, E_REST[i][1]), flip=(i % 2 == 0))

# stickers (parked under the ground until needed)
sticker("excl", "excl", 0.7); sticker("coin", "coin", 0.34); sticker("scis", "scis", 0.4); sticker("snip", "snip", 0.8); sticker("poof", "poof", 0.8)
sticker("ratsign", "ratsign", 1.28)

# ================================================================== SHOTS
# ---- 0  hook
s = shot("0", target="offH", hw=0.27, yaw=12, pitch=3, zoom=7, pan=(-16, 6), fy=0.1)
act(s, 0.0, "offH", face="smug", pose=dict(armR=-100, armL=8, head=0, body=0))
act(s, 0.8, "offH", pose=dict(armR=-150), hop=0.1)

s = shot("the more rats Hanoi#2", out="dissolve", target="offH", hw=0.12, yaw=-8, pitch=6, zoom=-6, pan=(10, 0), fy=0.05)
act(s, 0.0, "offH", face="shocked", pose=dict(armR=0, armL=0, head=0)); act(s, 0.05, "offH", shake=0.9)
show(s, 0.12, "excl", pos("H", 0.55, 2.0, 0.2), hop=0.1)
for (cid, kind, (x, z), fl), t_, ov in zip(HK[2:], (0.0, 0.0, 0.15, 0.2, 0.3, 0.35, 0.5, 0.55), (0.8, 0.8, 0.9, 0.9, 0.85, 0.85, 0.8, 0.8)):
    fx = {"hk3": -2.2, "hk4": 2.3, "hk5": -0.5, "hk6": 0.9, "hk7": -2.6, "hk8": 2.7, "hk9": -1.6, "hk10": 1.9}[cid]
    go(s, t_, cid, pos("H", fx, 0, z), ov)

# ---- 2  1902 establishing, 3 shiny sewer
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
s = shot("They climb", out="dissolve", anchor=pos("A", 0.5, 1.5, -5.6), dist=10, yaw=-10, pitch=4, zoom=6, pan=(-10, -6), fy=0.0)
go(s, 0.0, "r1", pos("A", 1.0, 0, -4.6), 0.6); go(s, 0.65, "r1", pos("A", 0.9, 0.2, -5.3), 0.28, hop=0.08)
go(s, 0.95, "r1", pos("A", 0.9, 0.4, -5.75), 0.28, hop=0.08); go(s, 1.25, "r1", pos("A", 0.9, 0.4, -6.5), 0.22)
go(s, 0.1, "r2", pos("A", 1.9, 0, -4.5), 0.8); go(s, 0.95, "r2", pos("A", 0.2, 0.2, -5.3), 0.3, hop=0.08)
go(s, 1.28, "r2", pos("A", 0.2, 0.4, -5.75), 0.28, hop=0.08); go(s, 1.58, "r2", pos("A", 0.2, 0.4, -6.5), 0.22)
go(s, 0.2, "r3", pos("A", 2.3, 0, -4.4), 0.9); go(s, 1.15, "r3", pos("A", 1.5, 0.2, -5.3), 0.3, hop=0.08)
go(s, 1.48, "r3", pos("A", 1.5, 0.4, -5.75), 0.28, hop=0.08); go(s, 1.8, "r3", pos("A", 1.5, 0.4, -6.5), 0.22)
show(s, 1.1, "r4", pos("A", -1.0, 2.55, -5.9), hop=0.18)

# ---- 6-9  the offer (B)
s = shot("So the government", target="boss", hw=0.22, yaw=-12, pitch=4, zoom=5, pan=(14, 6), fy=0.12)
act(s, 0.0, "boss", face="smug", pose=dict(armL=20, armR=0, head=4))
for i in range(5): act(s, 0.0, "n%d" % (i + 1), to=pos("A", (-0.5, 0.4, 1.4, 2.2, 3.0)[i], 0, (2.5, 2.9, 2.2, 3.1, 2.6)[i]), over=0.02, walk=False)   # A is off camera now

s = shot("One cent", anchor=pos("B", -1.2, 1.55, -0.5), dist=5.6, yaw=10, pitch=3, zoom=8, pan=(0, -6), fy=0.18)
act(s, 0.0, "boss", face="happy", pose=dict(armL=95, armR=0, head=-3))

s = shot("Just bring us", target="boss", hw=0.34, yaw=-6, pitch=3, zoom=9, pan=(-8, 0), fy=0.1)
act(s, 0.0, "boss", face="smug", pose=dict(armL=0, armR=-70, head=5))

s = shot("Hunters go", out="dissolve", anchor=pos("B", 0.5, 1.0, 0.5), dist=14, yaw=14, pitch=5, zoom=-5, pan=(14, 0), fy=0.05)
act(s, 0.0, "boss", face="shocked", pose=dict(armL=40, armR=-40, head=0))
for cid, t_, z, x0, x1 in (("h1", 0.0, 1.8, -9, 9), ("h2", 0.25, 0.9, -10, 10), ("h3", 0.5, 2.6, -11, 11)):
    act(s, t_, cid, face="shouting", pose=dict(armL=120, armR=-120)); go(s, t_, cid, pos("B", x1, 0, z), 1.4)
    for k in (0.25, 0.65, 1.05): act(s, t_ + k, cid, hop=0.12)

# ---- 10-13  turn-in day (D)
s = shot("On June", anchor=pos("D", -3.9, 2.4, -1.1), dist=4.4, yaw=6, pitch=2, zoom=10, pan=(0, -6), fy=0.05)
act(s, 0.15, "boss", to=pos("D", 2.6, 0, -0.8), over=0.02, walk=False, face="happy", pose=dict(armL=0, armR=0, head=0))
for cid, z in (("h1", 0.6), ("h2", 1.2), ("h3", 1.9)): act(s, 0.15, cid, to=pos("D", -6.5, 0, z), over=0.02, walk=False, face="happy", pose=dict(armL=0, armR=0))
act(s, 0.15, "nx", to=pos("D", 7.0, 0, 0.3), over=0.02, walk=False)

s = shot("they turn in", anchor=pos("D", 0, 2.5, -1.5), dist=8.5, yaw=8, pitch=2, zoom=7, pan=(0, -8), fy=0.0)

s = shot("In one single day", anchor=pos("D", 0, 1.5, -1.2), dist=15, yaw=-10, pitch=5, zoom=-4, pan=(12, 0), fy=0.03)
act(s, 0.0, "boss", face="happy", pose=dict(armL=130, armR=-130, head=0))
for cid, t_, x, z in (("h1", 0.0, -2.4, 0.6), ("h2", 0.2, -1.4, 1.2), ("h3", 0.4, -2.9, 1.9)):
    act(s, t_, cid, face="happy", pose=dict(armL=125, armR=-125)); go(s, t_, cid, pos("D", x, 0, z), 0.7)
    for k in (0.8, 1.15): act(s, t_ + k, cid, hop=0.18)

s = shot("Victory", out="dissolve", target="boss", hw=0.27, yaw=6, pitch=3, zoom=6, pan=(-6, 4), fy=0.1)
act(s, 0.0, "boss", face="happy", pose=dict(armL=150, armR=-150, head=-5)); act(s, 0.12, "boss", hop=0.2)
go(s, 0.2, "nx", pos("D", 3.5, 0, 0.3), 0.6, flip=False)

# ---- 14-17  inspectors (A)
s = shot("Then inspectors", target="insp", hw=0.2, yaw=-14, pitch=5, zoom=5, pan=(12, 4), fy=0.12)
go(s, 0.0, "insp", pos("A", -5.4, 0, 1.2), 1.3)
act(s, 1.1, "insp", face="confused", pose=dict(head=8, armR=-40)); show(s, 1.2, "excl", pos("A", -5.4, 2.05, 1.2), hop=0.1)

s = shot("Rats. Alive", anchor=pos("A", -4.4, 0.7, 1.5), dist=10, yaw=-6, pitch=8, zoom=6, pan=(-10, 0), fy=0.05)
for cid, t_, xe, z in (("n1", 0.0, -9, 2.5), ("n2", 0.2, -9.5, 2.9), ("n3", 0.4, -8.5, 2.2), ("n4", 0.55, -9, 3.1)):
    act(s, t_, cid, face="happy"); go(s, t_, cid, pos("A", xe, 0, z), 1.9)
act(s, 0.0, "insp", face="confused", pose=dict(head=8, armR=-40))

s = shot("Running through", anchor=pos("A", -3.0, 0.35, 2.4), dist=6.0, yaw=-8, pitch=-1.5, zoom=8, pan=(0, 0), fy=0.0)
hide(s, 0.0, "excl")
for cid, t_, x0, z in (("n1", 0.0, -8.0, 2.0), ("n2", 0.15, -8.5, 2.6), ("n3", 0.3, -9.0, 1.6), ("n4", 0.45, -8.0, 3.0)):
    act(s, t_, cid, to=pos("A", x0, 0, z), over=0.02, walk=False, flip=True); go(s, t_ + 0.05, cid, pos("A", 2.0, 0, z), 1.3)
act(s, 0.0, "hn", to=pos("A", -8.5, 0, 3.0), over=0.02, walk=False, face="happy")

s = shot("with no tails", out="dissolve", anchor=pos("A", -8.5, 0.55, 3.0), dist=4.6, yaw=-4, pitch=4, zoom=8, pan=(0, -6), fy=0.05)
act(s, 0.2, "hn", hop=0.15); act(s, 0.55, "hn", face="sneaky")
act(s, 0.0, "h1", to=pos("C", 0, 0.06, 0), over=0.02, walk=False, face="sneaky", pose=dict(armR=-130, armL=0, head=5))

# ---- 18-23  the farm (C)
s = shot("You see", target="h1", hw=0.22, yaw=-14, pitch=5, zoom=5, pan=(12, 6), fy=0.12)
show(s, 0.7, "coin", pos("C", 0.62, 1.24, 0.1), hop=0.15)
hide(s, 1.55, "coin"); go(s, 1.5, "h1", pos("C", -2.8, 0.06, -0.2), 0.6)

s = shot("A rat without", anchor=pos("C", 0.2, 0.55, 0.4), dist=7.5, yaw=10, pitch=8, zoom=6, pan=(-10, 0), fy=0.03)
act(s, 0.0, "mom", face="happy"); go(s, 0.0, "mom", pos("C", 0.3, 0.06, 0.0), 0.9)
for cid, t_, x, z in (("ba1", 0.2, 1.3, 0.9), ("ba2", 0.35, 0.7, 1.3), ("ba3", 0.5, 1.5, 0.2)): go(s, t_, cid, pos("C", x, 0.06, z), 0.8)
for cid, t_ in (("ba1", 1.2), ("ba2", 1.45), ("ba3", 1.7)): act(s, t_, cid, hop=0.14)

s = shot("and every baby", anchor=pos("C", 0.95, 0.35, 0.8), dist=3.8, yaw=14, pitch=6, zoom=10, pan=(-6, 0), fy=0.05)
for cid, t_ in (("ba1", 0.0), ("ba2", 0.3), ("ba3", 0.6)): act(s, t_, cid, hop=0.22)
for cid, t_, x in (("ba1", 1.0, 4.5), ("ba3", 1.1, 4.8), ("ba2", 1.25, 4.2)): go(s, t_, cid, pos("C", x, 0.06, 0.8), 0.9, flip=True)
go(s, 0.9, "mom", pos("C", 4.6, 0.06, 0.0), 1.1, flip=True)

s = shot("So hunters cut", anchor=pos("C", 0.4, 0.9, 0.4), dist=7.5, yaw=-10, pitch=5, zoom=5, pan=(6, 0), fy=0.05)
go(s, 0.0, "h1", pos("C", -0.4, 0.06, 0.0), 0.6); act(s, 0.5, "h1", face="sneaky", pose=dict(armR=-105, armL=0, head=0))
go(s, 0.1, "cr", pos("C", 1.15, 0.06, 0.5), 0.7)
show(s, 0.75, "scis", pos("C", 0.37, 0.92, 0.15), hop=0.06)
show(s, 1.15, "snip", pos("C", 0.55, 1.25, 0.35), hop=0.12); show(s, 1.15, "poof", pos("C", 1.15, 0.1, 0.6), hop=0.05)
act(s, 1.15, "cr", to=PARK, over=0.02, walk=False); act(s, 1.15, "hn2", to=pos("C", 1.15, 0.06, 0.5), over=0.02, walk=False, face="shocked")
hide(s, 1.5, "snip"); hide(s, 1.5, "poof"); hide(s, 1.5, "scis")
act(s, 1.65, "hn2", face="happy", hop=0.25); act(s, 1.65, "h1", face="happy", pose=dict(armR=0))
go(s, 2.0, "hn2", pos("C", 9, 0.06, 1.0), 1.2, flip=True)

s = shot("Outside the city", anchor=pos("C", 0, 1.0, -6.0), dist=15, yaw=10, pitch=6, zoom=4, pan=(8, 0), fy=0.03)
show(s, 0.0, "ratsign", pos("C", 0, 0.06, -8.95), hop=0.25)
act(s, 0.0, "h2", to=pos("C", 6.0, 0.06, -3.0), over=0.02, walk=False, face="sneaky", pose=dict(armL=0, armR=0, head=4))
go(s, 0.0, "h1", pos("C", -2.8, 0.06, -2.4), 0.8); act(s, 0.4, "h1", face="smug", pose=dict(armL=25, armR=-25))
for i, (cid, x, z) in enumerate(PEN):
    t_ = 0.1 + i * 0.1; go(s, t_, cid, pos("C", x, 0.06, z), 1.1)
    act(s, 1.5 + (i % 4) * 0.15, cid, hop=0.14)

s = shot("Others smuggled", out="dissolve", anchor=pos("C", 2.0, 0.9, -3.2), dist=10.5, yaw=-16, pitch=5, zoom=6, pan=(-12, 0), fy=0.03)
go(s, 0.0, "h2", pos("C", 0.6, 0.06, -3.0), 2.0)
for cid, t_, x, ov in (("s1", 0.3, 1.6, 1.9), ("s2", 0.5, 2.5, 1.8), ("s3", 0.7, 3.4, 1.7), ("s4", 0.9, 4.0, 1.5)): go(s, t_, cid, pos("C", x, 0.06, -3.0), ov)

# ---- 24-25  scrapped (E)
s = shot("The bounty", anchor=pos("E", -0.1, 1.5, -0.5), dist=5.8, yaw=-8, pitch=3, zoom=7, pan=(8, 0), fy=0.12)
act(s, 0.0, "bossE", face="nervous", pose=dict(armL=40, armR=-40, head=6))
for i in range(8):
    act(s, 0.0, "e%d" % (i + 1), to=pos("E", (-7 - i * 0.4) if i % 2 == 0 else (7 + i * 0.4), 0, E_REST[i][1]), over=0.02, walk=False)

s = shot("The rats stayed", out="dissolve", anchor=pos("E", 0.8, 0.8, 0.6), dist=12, yaw=12, pitch=6, zoom=4, pan=(-6, 0), fy=0.03)
act(s, 0.0, "bossE", face="nervous", pose=dict(armL=0, armR=0, head=8)); act(s, 0.1, "bossE", shake=0.8)
for i in range(8):
    go(s, 0.05 + i * 0.1, "e%d" % (i + 1), pos("E", E_REST[i][0], 0, E_REST[i][1]), 0.7)
    act(s, 0.9 + (i % 3) * 0.12, "e%d" % (i + 1), hop=0.14)

# ---- 26-27  counted tails (D)
s = shot("Because the city", target="boss", hw=0.2, yaw=-6, pitch=3, zoom=5, pan=(8, 0), fy=0.12)
act(s, 0.0, "boss", face="confused", pose=dict(armL=0, armR=-50, head=-7))
act(s, 0.0, "nx", to=pos("D", 7.0, 0, 0.3), over=0.02, walk=False)

s = shot("It counted tails", out="dissolve", anchor=pos("D", 0, 2.5, -1.5), dist=7.0, yaw=6, pitch=3, zoom=10, pan=(0, -6), fy=0.05)

# ---- 28  the loop: more rats than ever (H)
s = shot("And that's why", target="offH", hw=0.16, yaw=12, pitch=3, zoom=-5, pan=(-16, 6), fy=0.1)
act(s, 0.0, "offH", face="shocked", pose=dict(armR=0, armL=0, head=0)); act(s, 0.1, "offH", shake=1.4)
for i, cid in enumerate(("hk1", "hk2", "hk3", "hk4", "hk5", "hk6", "hk7", "hk8", "hk9", "hk10")): act(s, 0.15 + i * 0.12, cid, hop=0.14)
for cid, t_, x, z in (("hk11", 0.3, -3.0, 2.2), ("hk12", 0.5, 3.0, 2.4), ("hk13", 0.7, -3.4, 1.0), ("hk14", 0.9, 3.4, 1.1)): go(s, t_, cid, pos("H", x, 0, z), 0.7)

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
