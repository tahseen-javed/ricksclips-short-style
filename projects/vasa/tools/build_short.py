#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 04: the Vasa.
usage: build_short.py <project folder>
Seven sets 70 units apart: HB Stockholm harbour 1628 (the hook ship goes down at x -30, the story ship sails
from the quay), DK the deck (stability test), SB the seabed, WS a warm Mediterranean beach, CB the cold Baltic,
WR the what-if war sea, MU the museum.  Anything that changes sets moves while the camera is elsewhere; cards
leave one frame before a cut; the last shot repeats the first for the loop."""
import json, os, sys, subprocess
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HB=0, DK=70, SB=140, WS=210, CB=280, WR=350, MU=420)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


def cut(s, phrase, *who):                                    # hide just before the next shot starts on `phrase`
    for w in who: hide(s, rel(s, phrase) - 0.04, w)


# ================================================================== SETS
box("HB", 0, 0, -37, [130, 0.5, 12], color="#86986e")
for i, x in enumerate(range(-50, 40, 6)):
    house("HB", x, -32.5, [4.4, 3.0 + (i % 3) * 0.9, 3.6], ["#6b3a32", "#4a4f63"][i % 2], color=["#d9a441", "#b5533c", "#e8c35a", "#d97b3c", "#c9b48a", "#9fbf8f"][i % 6])
post("HB", -9.2, -32.5, 10, "#3d4a52"); post("HB", 21, -32.5, 8, "#3d4a52")
box("HB", -3, 0, 4.6, [15, 0.5, 2.6], texture="wood.jpg", repeat=[7, 1])
for x in (-8, -4, 0): post("HB", x, 3.6, 1.0, "#4a3a3f")
barrel("HB", -6.2, 4.8, y=0.5); barrel("HB", -5.4, 5.2, y=0.5); crate("HB", 2.2, 0.5, 4.9)

box("DK", 0, 0, -2, [9, 0.04, 36], texture="wood.jpg", repeat=[3, 12])
for sg in (-1, 1):
    box("DK", sg * 4.6, 0, -2, [0.35, 0.9, 36], color="#7a4a2e")
    for z in (-12, -7): box("DK", sg * 3.9, 0, z, [0.9, 0.42, 0.42], color="#3c3c46")
post("DK", 0, -5, 12, "#6b4228"); plane("DK", "sail.png", 0, 3.6, -4.85, 7.6, 5.8)
post("DK", 0, -14, 10, "#6b4228"); plane("DK", "sail.png", 0, 3.2, -13.85, 6.6, 5.0)
crate("DK", -3.3, 0, -8.5); barrel("DK", 3.3, -9.5)

box("SB", 0, 0, -4, [46, 0.05, 30], color="#dcc896"); plane("SB", "under.png", 0, -0.5, -15, 50, 25)
for x, z, sz, c in ((-6.5, -6, [2.2, 0.9, 1.6], "#8f8a84"), (6.8, -7, [2.8, 1.2, 1.8], "#7f7a76"), (-3.6, 1.6, [1.0, 0.45, 0.8], "#9a948c"), (4.2, 1.2, [0.8, 0.35, 0.7], "#a39c92")):
    box("SB", x, 0, z, sz, color=c)
for x, z, h in ((-5, -3, 2.2), (-4.4, -3.6, 1.6), (5, -2.5, 2.6), (5.6, -3.4, 1.8), (-7.5, -1, 1.4), (7.4, -1.5, 1.6), (-2.6, -8, 2.4), (2.8, -8.5, 2.0)):
    post("SB", x, z, h, "#4f9a5a")

box("WS", 0, 0, -9, [46, 0.03, 24], color="#46c6cf"); box("WS", 0, 0, 1.5, [46, 0.14, 7], color="#f1dba2")
plane("WS", "palm.png", -2.6, 0.12, -1.5, 3.2, 4.4); plane("WS", "palm.png", 3.4, 0.12, -2.0, 3.5, 4.8); plane("WS", "skyws.png", 0, -1, -26, 96, 42)

box("CB", 0, 0, -8, [46, 0.03, 30], color="#6f95b6"); plane("CB", "skycb.png", 0, -1, -26, 96, 42)
for x, z, w, d in ((0, 0.4, 2.6, 1.8), (-4.5, -3, 3, 2), (4.8, -2.4, 2.4, 1.6), (-2.4, -7, 3.4, 2.2), (6.2, -8, 3, 2), (-7, 0.5, 2, 1.4), (3, 2.6, 1.4, 1)):
    box("CB", x, 0, z, [w, 0.2, d], color="#eef5fb")

plane("WR", "skywr.png", 0, -1, -26, 96, 42)
for x, z, sz in ((-7, -9, [2.4, 1.6, 2]), (8, -10, [3, 2.2, 2.4])): box("WR", x, 0, z, sz, color="#6f6a72")

box("MU", 0, 0, -3, [28, 0.05, 22], color="#c9ae8c"); box("MU", 0, 0, -13, [30, 13, 0.4], color="#dfe4ea")
for sg in (-1, 1): box("MU", sg * 13.5, 0, -3, [0.4, 13, 22], color="#d2d9e1")
box("MU", 0, 0, -5, [7.5, 0.5, 1.4], color="#5d4c44"); box("MU", 0, 0, -1.4, [12, 0.95, 0.12], color="#8b6b4a")
for x in range(-12, 13, 4): box("MU", x, 9.5, -12.7, [1.2, 0.3, 0.3], color="#ffe08a")

# ================================================================== CHARACTERS
put("vasaK", "vasa", pos("HB", -30, -2.6, -4), 6.5, "flood", pose=dict(head=22))
put("splashK", "splash", pos("HB", -27.4, -0.35, -3.4), 1.5); put("bubK", "bubbles", pos("HB", -31.6, -0.15, -3.4), 1.2)
put("vasaH", "vasa", pos("HB", 0, -1.6, -4), 6.5)
put("vasaS", "vasa", pos("SB", 0, 7, -4), 5.5, "wreck", pose=dict(head=-6))
put("vasaW", "vasa", pos("WR", 0, -1.6, -4), 6.5); put("vasaM", "vasa", pos("MU", 0, 0.38, -5), 7.2, "museum")
SAILORS = [("sA", "sailA", -3.0, 0.9), ("sB", "sailB", -2.6, -0.5), ("sC", "sailC", -2.2, 1.2), ("sD", "sailD", -1.8, -0.2), ("sE", "sailE", -1.4, 0.6), ("sF", "sailF", -1.0, -0.9)]
for cid, pp, x, z in SAILORS: human(cid, pp, pos("DK", x, 0.04, z), face="happy")
human("capt", "capt", pos("DK", 0.3, 0.04, -3.0), face="smug"); human("diver", "diver", pos("SB", 5.5, 0.05, 0.6), face="happy")
for c_, x_ in (("mom", -1.5), ("dad", -0.5), ("tech", 0.5), ("vik", 1.5)): human(c_, c_, pos("MU", x_, 0.05, 0.3), face="happy")
put("f1", "fish", pos("SB", -7, 2.6, -1), 0.7); put("f2", "fish", pos("SB", 7, 3.6, -2), 0.6, flip=True)
WORMS = (("w1", -0.9, 0.3), ("w2", 0.6, 0.7), ("w3", 1.8, 0.2))
put("boat", "boat", pos("WS", 0.4, 0.14, -0.2), 1.3); put("sun", "sun", pos("WS", 2.0, 4.0, -1.0), 1.3)
for cid, x, z in WORMS: put(cid, "worm", pos("WS", x, -1.0, z), 0.85)
put("wormC", "worm", pos("CB", 0, 0.2, 0.5), 0.9, "cold")
for cid, name, h in (("sank", "sank", 0.95), ("cal28", "cal28", 2.4), ("vtag", "vtag", 0.9), ("decks", "decks", 1.1), ("one", "one", 0.55), ("smoke1", "poof", 0.8),
                     ("smoke2", "poof", 0.8), ("x30", "x30", 0.9), ("test", "test", 0.5), ("stop", "stop", 0.75), ("anyway", "anyway", 0.8), ("mile", "mile", 0.9),
                     ("gust", "gust", 1.6), ("splash2", "splash", 1.3), ("bub2", "bubbles", 1.2), ("g1", "gull", 0.9), ("g2", "gull", 0.75), ("poofS", "poof", 1.6),
                     ("cal61", "cal61", 1.8), ("splashU", "splash", 1.8), ("whole", "whole", 0.75), ("spark1", "sparkle", 0.7), ("ques", "ques", 1.3), ("warm", "warm", 0.7),
                     ("clams", "clams", 0.42), ("nom", "nom", 0.5), ("med", "med", 0.55), ("poofB", "poof", 1.4), ("y30", "y30", 0.9), ("snow1", "snow", 1.4),
                     ("snow2", "snow", 1.2), ("baltic", "baltic", 0.55), ("coldsalt", "coldsalt", 0.62), ("nope", "nope", 0.6), ("y333", "y333", 1.3),
                     ("untouched", "untouched", 0.65), ("spark2", "sparkle", 0.6), ("p98", "p98", 1.4), ("whatif", "whatif", 0.8), ("poofW", "poof", 2.0),
                     ("million", "million", 0.75), ("hearts", "hearts", 0.8), ("worst", "worst", 0.8), ("hidden", "hidden", 0.7)):
    sticker(cid, name, h)

# ================================================================== SHOTS
HOOK = dict(anchor=pos("HB", -29.5, 1.6, -4), dist=14, yaw=8, pitch=3, zoom=14, pan=(-6, 3), fy=0.0)
# ---- 0-3 hook (the Vasa already going down in frame 1), then launch day in Stockholm, 1628
s = shot("0", **HOOK)
act(s, 0.0, "vasaK", pose=dict(head=28), ease=2.4, shake=0.5); show(s, rel(s, "only reason"), "sank", pos("HB", -29.5, 4.3, -2.6), hop=0.12)
s = shot("Stockholm", anchor=pos("HB", 1.0, 2.4, -4), dist=24, yaw=-10, pitch=4, zoom=6, pan=(10, 0))
hide(s, 0.0, "sank")
for g_, a_, b_ in (("g1", (-5, 6.6, -2), (6, 7.2, -2)), ("g2", (-3, 7.8, -3), (8, 7.2, -3))):
    show(s, 0.0, g_, pos("HB", *a_), hop=0); go(s, 0.05, g_, pos("HB", *b_), 2.1, walk=False)
show(s, rel(s, "1628") - 0.1, "cal28", pos("HB", -2.4, 4.6, -1.5), hop=0.15); cut(s, "The Vasa", "cal28")
s = shot("The Vasa", anchor=pos("HB", 0.6, 2.2, -4), dist=12, yaw=18, pitch=2, zoom=10, pan=(-8, 2))
show(s, 0.1, "vtag", pos("HB", 0.6, 5.0, -2.2), hop=0.12)
s = shot("Two full", anchor=pos("HB", 0.8, 0.9, -4), dist=7, yaw=-14, pitch=3, zoom=10, pan=(8, 0))
hide(s, 0.0, "vtag"); show(s, 0.0, "smoke1", pos("HB", 1.5, 0.45, -3.6), hop=0.1); show(s, rel(s, "gun decks"), "smoke2", pos("HB", 0.1, -0.05, -3.6), hop=0.1)
show(s, 0.15, "decks", pos("HB", 0.8, 1.9, -2.6), hop=0.12); hide(s, rel(s, "when most"), "decks"); show(s, rel(s, "just one"), "one", pos("HB", 0.8, 2.0, -2.6), hop=0.12)

# ---- 4-8 the stability test (DK): thirty sailors run side to side, she rocks, the captain stops it
s = shot("But before launch", anchor=pos("DK", 0, 1.4, -1), dist=16, yaw=12, pitch=9, zoom=6, pan=(-10, 0))
for c_ in ("smoke1", "smoke2", "one", "g1", "g2"): hide(s, 0.3, c_)
s = shot("thirty sailors", anchor=pos("DK", 0, 1.0, 0), dist=13, yaw=-8, pitch=7, zoom=8, pan=(8, 0))
show(s, 0.1, "x30", pos("DK", 0, 2.6, 1.4), hop=0.12); cut(s, "A stability test", "x30")
for t_, dx in ((0.0, 4.0), (0.85, 0.0), (1.7, 4.0)):
    for j, (cid, _, x, z) in enumerate(SAILORS): go(s, t_ + 0.04 * j, cid, pos("DK", x + dx, 0.04, z), 0.75)
s = shot("A stability test", target="capt", hw=0.3, yaw=10, pitch=3, zoom=8, pan=(-6, 2), fy=0.1)
show(s, 0.15, "test", pos("DK", 0.3, 2.35, -2.5), hop=0.12); act(s, 0.4, "capt", face="nervous")
s = shot("She rocked", anchor=pos("HB", 0.4, 2.0, -4), dist=14, yaw=-6, pitch=4, zoom=10, pan=(6, 0))
hide(s, 0.3, "test"); act(s, 0.0, "vasaH", shake=0.4)
for k in range(5): act(s, k * 0.3, "vasaH", pose=dict(head=13 if k % 2 == 0 else -13), ease=0.28)
s = shot("they stopped", target="capt", hw=0.26, yaw=-12, pitch=3, zoom=12, pan=(8, 0), fy=0.12)
act(s, 0.0, "capt", face="shouting", pose=dict(armR=-150)); show(s, 0.05, "stop", pos("DK", 1.0, 1.9, -2.6), hop=0.15)
for cid, *_ in SAILORS: act(s, 0.05, cid, face="shocked")
act(s, 0.8, "vasaH", pose=dict(head=0), ease=0.3)

# ---- 9-14 she sails anyway (HB): under a mile, the gust, the lean, water through the gun ports, down
s = shot("She sailed anyway", anchor=pos("HB", 3.0, 2.2, -5), dist=18, yaw=-10, pitch=4, zoom=6, pan=(12, 0))
hide(s, 0.3, "stop"); go(s, 0.0, "vasaH", pos("HB", 8, -1.6, -6), 2.6, walk=False)
show(s, rel(s, "anyway"), "anyway", pos("HB", 2.0, 5.8, -3), hop=0.12); cut(s, "Less than a mile", "anyway")
s = shot("Less than a mile", anchor=pos("HB", 7, 2.2, -6), dist=22, yaw=22, pitch=5, zoom=6, pan=(-8, 0))
show(s, 0.2, "mile", pos("HB", 7, 6.4, -4), hop=0.12); cut(s, "a gust", "mile")
s = shot("a gust", anchor=pos("HB", 6.6, 3.0, -6), dist=13, yaw=10, pitch=3, zoom=10, pan=(6, 2))
show(s, 0.0, "gust", pos("HB", 3.2, 4.3, -4.4), hop=0); go(s, 0.03, "gust", pos("HB", 5.0, 4.5, -4.4), 0.7, walk=False)
act(s, 0.3, "vasaH", shake=0.6); cut(s, "She leans", "gust")
s = shot("She leans", anchor=pos("HB", 8.4, 2.0, -6), dist=12, yaw=-10, pitch=3, zoom=12, pan=(-6, 0))
act(s, 0.0, "vasaH", pose=dict(head=18), ease=0.45)
s = shot("Water pours", anchor=pos("HB", 8.9, 0.6, -6), dist=7, yaw=10, pitch=3, zoom=10, pan=(4, 2))
act(s, 0.0, "vasaH", face="flood", pose=dict(head=22), ease=1.2); show(s, 0.1, "splash2", pos("HB", 9.2, -0.3, -5.2), hop=0.1); cut(s, "Within minutes", "splash2")
s = shot("Within minutes", out="dissolve", anchor=pos("HB", 8.4, 2.0, -6), dist=18, yaw=-14, pitch=5, zoom=8, pan=(8, -2))
act(s, 0.0, "vasaH", pose=dict(head=32), ease=2.0); go(s, 0.25, "vasaH", pos("HB", 8, -9, -6), 2.4, walk=False)
show(s, 1.3, "bub2", pos("HB", 8.3, -0.2, -5.2), hop=0.1)

# ---- 15-19 the seabed (SB), 1961, she comes back up (HB), almost whole, How?
s = shot("on the seabed", anchor=pos("SB", 0, 2.0, -4), dist=14, yaw=8, pitch=3, zoom=10, pan=(-6, 2))
go(s, 0.0, "vasaS", pos("SB", 0, 0.05, -4), 0.45, walk=False); show(s, 0.42, "poofS", pos("SB", 0, 0.05, -2.4), hop=0.1)
act(s, 0.3, "vasaH", face="raise", pose=dict(head=0), ease=0.2); hide(s, 0.3, "bub2"); cut(s, "Then in 1961", "poofS")
s = shot("Then in 1961", anchor=pos("SB", 1.2, 1.6, -2), dist=11, yaw=-10, pitch=3, zoom=8, pan=(8, 0))
go(s, 0.0, "diver", pos("SB", 2.4, 0.05, 0.6), 0.9); act(s, 1.0, "diver", pose=dict(armR=-150))
show(s, max(0.05, rel(s, "1961") - 0.05), "cal61", pos("SB", 0.1, 2.6, -0.8), hop=0.15)
s = shot("she comes back up", anchor=pos("HB", 8, 2.0, -6), dist=15, yaw=14, pitch=3, zoom=10, pan=(-6, 4))
go(s, 0.0, "vasaH", pos("HB", 8, -1.6, -6), 1.4, walk=False); show(s, 0.45, "splashU", pos("HB", 8.2, -0.35, -4.8), hop=0.1)
hide(s, 0.3, "diver"); hide(s, 0.3, "cal61"); cut(s, "Almost whole", "splashU")
s = shot("Almost whole", anchor=pos("HB", 8, 2.2, -6), dist=10, yaw=-8, pitch=3, zoom=10, pan=(6, 0))
show(s, 0.1, "whole", pos("HB", 8, 4.4, -4.6), hop=0.12); show(s, 0.25, "spark1", pos("HB", 9.5, 3.3, -4.4), hop=0.1); cut(s, "How", "whole", "spark1")
s = shot("How", anchor=pos("HB", 8, 2.6, -6), dist=7.5, yaw=2, pitch=2, zoom=18)
show(s, 0.05, "ques", pos("HB", 8, 3.2, -4.4), hop=0.15)

# ---- 20-26 shipworms: warm salty Mediterranean (WS) vs the cold, barely salty Baltic (CB)
s = shot("You see", anchor=pos("WS", 0.4, 1.4, -0.5), dist=11, yaw=10, pitch=7, zoom=8, pan=(-8, 2))
hide(s, 0.3, "ques"); p_ = rel(s, "full of shipworms")
for k, (cid, x, z) in enumerate(WORMS): go(s, p_ + 0.12 * k, cid, pos("WS", x, 0.14, z), 0.3, walk=False, hop=0.25)
show(s, rel(s, "warm salty"), "warm", pos("WS", 0.4, 3.0, 0.6), hop=0.12)
s = shot("Tiny clams", anchor=pos("WS", 0.6, 0.75, 0.6), dist=4.2, yaw=-10, pitch=4, zoom=10, pan=(6, 2))
hide(s, 0.0, "warm"); act(s, 0.0, "w2", face="munch", shake=0.6); show(s, 0.1, "clams", pos("WS", 0.6, 1.5, 1.0), hop=0.12)
show(s, rel(s, "chew"), "nom", pos("WS", 1.25, 0.9, 1.1), hop=0.12); cut(s, "In the Mediterranean", "clams", "nom")
s = shot("In the Mediterranean", anchor=pos("WS", 0.4, 1.2, -0.3), dist=8, yaw=14, pitch=6, zoom=8, pan=(-10, 0))
act(s, 0.0, "w2", face="default"); show(s, 0.05, "med", pos("WS", 0.4, 2.3, 0.6), hop=0.12); act(s, 0.2, "w1", face="munch"); act(s, 0.3, "w3", face="munch")
cut(s, "would be eaten", "med")
s = shot("would be eaten", anchor=pos("WS", 0.4, 0.8, -0.2), dist=5.5, yaw=-12, pitch=5, zoom=10, pan=(6, 2))
e_ = rel(s, "eaten"); act(s, e_, "boat", face="eaten", shake=0.5); act(s, e_, "w2", face="munch")
y_ = rel(s, "thirty years"); show(s, y_, "poofB", pos("WS", 0.4, 0.1, 0.4), hop=0.1); hide(s, y_ + 0.1, "boat")
for c_ in ("w1", "w2", "w3"): act(s, y_ + 0.1, c_, face="default")
show(s, y_ + 0.15, "y30", pos("WS", 0.4, 1.55, 0.6), hop=0.12)
s = shot("But the Baltic", anchor=pos("CB", 0, 1.2, 0.2), dist=8, yaw=10, pitch=7, zoom=8, pan=(-8, 2))
hide(s, 0.3, "poofB"); hide(s, 0.3, "y30"); act(s, 0.0, "wormC", shake=1.0)
for c_, x_, z_, y0, y1 in (("snow1", -0.6, 1.2, 3.4, 1.8), ("snow2", 1.0, -0.6, 3.8, 2.2)):
    show(s, 0.0, c_, pos("CB", x_, y0, z_), hop=0); go(s, 0.05, c_, pos("CB", x_, y1, z_), 2.6, walk=False)
show(s, 0.15, "baltic", pos("CB", 0, 2.6, 0.9), hop=0.12); cut(s, "cold and barely", "baltic")
s = shot("cold and barely", anchor=pos("CB", 0, 0.9, 0.5), dist=5, yaw=-8, pitch=5, zoom=10, pan=(6, 2))
show(s, 0.05, "coldsalt", pos("CB", 0, 1.6, 0.95), hop=0.12); act(s, 0.1, "wormC", shake=1.0); cut(s, "and shipworms can't", "coldsalt")
s = shot("and shipworms can't", anchor=pos("CB", 0.2, 0.9, 0.4), dist=6, yaw=12, pitch=5, zoom=10, pan=(-6, 0))
act(s, 0.0, "wormC", face="sad"); show(s, rel(s, "can't thrive"), "nope", pos("CB", 0.3, 1.55, 0.95), hop=0.15)
go(s, rel(s, "there"), "wormC", pos("CB", 0, -1.2, 0.5), 0.5, walk=False)

# ---- 27-29 333 years untouched on the seabed (SB), 98 % original in the museum (MU)
s = shot("So for 333", anchor=pos("SB", 0, 2.2, -4), dist=18, yaw=-14, pitch=3, zoom=6, pan=(12, 0))
for c_ in ("nope", "snow1", "snow2"): hide(s, 0.3, c_)
go(s, 0.0, "f1", pos("SB", 7, 2.9, -1), 3.6, walk=False); go(s, 0.0, "f2", pos("SB", -7, 3.2, -2), 4.0, walk=False)
show(s, rel(s, "333"), "y333", pos("SB", 0, 4.6, -2.4), hop=0.15); cut(s, "Untouched", "y333")
s = shot("Untouched", out="dissolve", anchor=pos("SB", 0.4, 1.8, -4), dist=9, yaw=12, pitch=3, zoom=10, pan=(-6, 2))
show(s, 0.05, "untouched", pos("SB", 0.4, 3.6, -2.6), hop=0.12); show(s, 0.25, "spark2", pos("SB", 1.8, 2.5, -2.8), hop=0.1)
s = shot("Today she", anchor=pos("MU", 0, 3.4, -5), dist=17, yaw=-8, pitch=4, zoom=8, pan=(8, 0))
hide(s, 0.6, "untouched"); hide(s, 0.6, "spark2"); show(s, rel(s, "98"), "p98", pos("MU", 0, 6.0, -3), hop=0.15)

# ---- 30-32 what if she had gone to war (WR): rotted, burned, sunk somewhere salty, vanished
s = shot("If she had", anchor=pos("WR", 0.4, 2.2, -4), dist=15, yaw=10, pitch=4, zoom=8, pan=(-8, 0))
hide(s, 0.3, "p98"); show(s, 0.05, "whatif", pos("WR", 0.4, 5.6, -2.5), hop=0.12); act(s, rel(s, "war"), "vasaW", face="war", shake=0.5)
cut(s, "rotted", "whatif")
s = shot("rotted", anchor=pos("WR", 0.4, 1.8, -4), dist=11, yaw=-10, pitch=3, zoom=10, pan=(6, 0))
act(s, 0.0, "vasaW", face="rot", pose=dict(head=-5), ease=0.3); act(s, rel(s, "burned"), "vasaW", face="burn", shake=0.6, pose=dict(head=4))
s = shot("or sunk", anchor=pos("WR", 0.4, 1.6, -4), dist=14, yaw=8, pitch=4, zoom=8, pan=(-6, 2))
act(s, 0.0, "vasaW", face="wreck", pose=dict(head=24), ease=0.8); go(s, 0.05, "vasaW", pos("WR", 0, -9, -4), 1.3, walk=False)
show(s, rel(s, "vanished"), "poofW", pos("WR", 0.3, -0.4, -2.6), hop=0.1)

# ---- 33-36 a million visitors (MU), the worst launch (HB), the perfect hiding place (SB)
s = shot("Instead", anchor=pos("MU", 0, 1.3, 0.3), dist=10.5, yaw=10, pitch=4, zoom=8, pan=(-8, 2))
for k, c_ in enumerate(("mom", "dad", "tech", "vik")): act(s, 0.1 + 0.08 * k, c_, pose=dict(armR=-150, armL=150), face="happy")
show(s, rel(s, "million"), "million", pos("MU", 0, 2.6, 0.8), hop=0.15); cut(s, "visit her every", "million")
s = shot("visit her every", anchor=pos("MU", 0, 3.6, -4), dist=19, yaw=-16, pitch=6, zoom=6, pan=(12, 2))
show(s, 0.2, "hearts", pos("MU", 0, 2.3, 0.8), hop=0.12)
for k, c_ in enumerate(("mom", "dad", "tech", "vik")): act(s, 0.3 + 0.1 * k, c_, pose=dict(armR=-100, armL=100))
s = shot("The worst launch", anchor=pos("HB", -29.6, 1.8, -4), dist=17, yaw=-22, pitch=5, zoom=8, pan=(8, 0))
hide(s, 0.3, "hearts"); hide(s, 0.3, "poofW"); show(s, 0.1, "worst", pos("HB", -29.6, 5.0, -2.6), hop=0.12)
s = shot("gave her a perfect", anchor=pos("SB", 0.2, 1.9, -4), dist=11, yaw=14, pitch=3, zoom=10, pan=(-8, 2))
hide(s, 0.3, "worst"); act(s, 0.3, "vasaK", pose=dict(head=22), ease=0.2); show(s, rel(s, "hiding"), "hidden", pos("SB", 0.2, 3.9, -2.6), hop=0.15)

# ---- 37 loop: the first shot again
s = shot("Sinking#2", **HOOK); s["start"] = round(say("Sinking#2"), 3)
act(s, 0.0, "vasaK", pose=dict(head=28), ease=2.4, shake=0.5); show(s, rel(s, "only reason#2"), "sank", pos("HB", -29.5, 4.3, -2.6), hop=0.12)

# ================================================================== SPEC
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6,
    "moods": {"day": {"sun": {"azimuth": 35, "elevation": 50, "color": "#ffe0b5", "intensity": 2.4},
                      "sky": {"top": "#5f86d8", "horizon": "#f2b98a"}, "fill": {"sky": "#8ea2ff", "ground": "#6a3b6e", "intensity": 1.15}}},
    "lighting": [{"t": 0, "mood": "day"}],
    "ground": {"texture": TEX + "water.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/stockholm.jpg", "blur": 5}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
cues = dict(splash=[0.0, say("Sinking#2")], gull=say("Stockholm"), bell=say("1628"), cannon=[say("Two full"), say("gun decks")], run=say("thirty sailors"),
            creak=[say("She rocked"), say("She leans")], whistle=say("they stopped"), gust=say("a gust"), rush=say("Water pours"), seabed=say("seabed"),
            up=say("comes back up"), whole=say("Almost whole"), how=say("How"), yousee=say("You see"), munch=say("chew"), poof=[say("thirty years"), say("vanished")],
            baltic=say("But the Baltic"), sad=say("can't thrive"), s333=say("So for 333"), untouched=say("Untouched"), today=say("Today she"), war=say("If she had"),
            rot=say("rotted"), burn=say("burned"), sunk=say("or sunk"), instead=say("Instead"), cheer=say("million people"), worst=say("The worst"), end=DURATION)
cp, wav = os.path.join(P, "audio", "cues.json"), os.path.join(P, "audio", "music.wav")
json.dump(cues, open(cp, "w"))
subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), wav, "%.2f" % (DURATION + 0.4), cp], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", os.path.join(P, "audio", "music.mp3")], check=True)
os.remove(wav)

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
