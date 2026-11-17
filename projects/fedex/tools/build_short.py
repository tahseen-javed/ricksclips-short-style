#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 06: FedEx saved by blackjack.
usage: build_short.py <project folder>
Six sets 70 units apart: VG the Las Vegas casino (the hook), MP Memphis airport at dusk 1973 (fourteen Falcon jets),
OF the Federal Express office, OP the operations room with the hub-and-spoke wall map, YL a Yale classroom, TD the
giant cargo hub of today.  Every shot has a camera move (dolly + orbit).  Cards are sized from the shot distance and
leave one frame before the next shot; the last shot repeats the first for the loop."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(VG=0, MP=70, OF=140, OP=210, YL=280, TD=350)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


# ================================================================== SETS
# VG casino: carpet, purple walls, neon sign, slot machines, gold pillars, the blackjack table
box("VG", 0, 0, -3, [22, 0.06, 16], texture="carpet.jpg", repeat=[5, 4]); box("VG", 0, 0, -9, [22, 7.5, 0.4], color="#8a5a9e")
for sg in (-1, 1): box("VG", sg * 10.8, 0, -3, [0.4, 7.5, 16], color="#9a6a7e"); box("VG", sg * 4.6, 0, -6, [0.7, 7.5, 0.7], color="#d9a441")
plane("VG", "neon.png", 0, 3.4, -8.75, 6.4, 2.56)
for x in (-8.6, -6.8, 6.8, 8.6): plane("VG", "slot.png", x, 0.06, -8.7, 1.5, 2.5)
for x in (-5, 0, 5): box("VG", x, 6.6, -4, [1.0, 0.3, 1.0], color="#ffe08a")
box("VG", 0, 0, -1.6, [4.2, 0.86, 1.9], color="#8a3e2e"); box("VG", 0, 0.7, -0.62, [4.2, 0.08, 0.06], color="#e0b050"); box("VG", 0, 0.86, -1.6, [3.9, 0.05, 1.6], color="#2e8c58")
box("VG", -6, 0, -5, [3, 0.86, 1.5], color="#8a3e2e"); box("VG", -6, 0.86, -5, [2.7, 0.05, 1.2], color="#2e8c58")
box("VG", 6, 0, -5, [3, 0.86, 1.5], color="#8a3e2e"); box("VG", 6, 0.86, -5, [2.7, 0.05, 1.2], color="#a23a4a")
# MP Memphis 1973 at dusk: taxi line, runway lights, hangar, tower, crates
plane("MP", "skymem.png", 0, -1, -26, 96, 42)
for x in range(-20, 21, 4): box("MP", x, 0.07, 1.6, [1.4, 0.02, 0.16], color="#f2c230")
for x in range(-18, 19, 3): post("MP", x, 2.6, 0.35, "#ffd166")
house("MP", -10, -12, [12, 6.5, 9], "#8a76b8", color="#ddd6ee"); house("MP", 11, -14, [8, 4.6, 7], "#7a5f52", color="#d8cfc0")
box("MP", 9, 0, -10, [1.6, 5, 1.6], color="#d8d2c4"); box("MP", 9, 5, -10, [2.6, 1.2, 2.6], color="#8fb3cc"); box("MP", 9, 6.2, -10, [3, 0.2, 3], color="#5e4f86")
crate("MP", -4.5, 0, -7.5); crate("MP", -3.8, 0.75, -7.7, 0.6); barrel("MP", 5.5, -8); barrel("MP", 6.2, -8.4)
# OF office: wood floor, warm walls, bills board, window, desk, cabinet
box("OF", 0, 0, -1, [10, 0.06, 9], texture="wood.jpg", repeat=[3, 3]); box("OF", 0, 0, -4.5, [10, 4.2, 0.3], color="#d8b48a")
for sg in (-1, 1): box("OF", sg * 4.85, 0, -1, [0.3, 4.2, 9], color="#c9a27a")
plane("OF", "bills.png", -1.7, 1.3, -4.32, 2.4, 1.6); plane("OF", "window.png", 2.4, 0.9, -4.32, 1.4, 2.06)
box("OF", -0.4, 0, -1.6, [2.6, 0.74, 1.1], color="#a8724a"); box("OF", -0.4, 0.74, -1.6, [2.7, 0.06, 1.2], color="#c98f5e"); box("OF", -3.6, 0, -3.7, [0.9, 1.4, 0.7], color="#9aa6b6")
box("OF", 3.6, 0, -3.8, [1.2, 2.2, 0.5], color="#b07a4e")
# OP operations room: the hub-and-spoke wall map
box("OP", 0, 0, -1, [14, 0.06, 10], color="#8a93a3"); box("OP", 0, 0, -5, [14, 6.4, 0.3], color="#6f7d96")
for sg in (-1, 1): box("OP", sg * 6.85, 0, -1, [0.3, 6.4, 10], color="#7d8aa2"); box("OP", sg * 5.0, 0, -3.6, [1.6, 0.9, 0.7], color="#5a6478")
plane("OP", "map.png", 0, 0.7, -4.82, 8.4, 5.13)
# YL Yale classroom: chalkboard, pennant, window, desks
box("YL", 0, 0, -1, [12, 0.06, 10], texture="wood.jpg", repeat=[3, 3]); box("YL", 0, 0, -5, [12, 5, 0.3], color="#b8c6dc")
for sg in (-1, 1): box("YL", sg * 5.85, 0, -1, [0.3, 5, 10], color="#a8b8d0")
plane("YL", "chalk.png", 0.8, 1.0, -4.82, 5.0, 2.5); plane("YL", "pennant.png", -3.4, 2.6, -4.82, 2.0, 0.88); plane("YL", "window.png", 4.4, 0.9, -4.82, 1.3, 1.9)
box("YL", -0.6, 0, -0.6, [1.3, 0.69, 0.75], color="#b07a4e"); box("YL", -0.6, 0.69, -0.6, [1.4, 0.06, 0.85], color="#d09a64")
for x, z in ((-3.0, -1.6), (2.6, -0.4), (-3.4, 1.2), (3.2, 1.4)): box("YL", x, 0, z, [1.2, 0.75, 0.7], color="#b07a4e")
box("YL", 2.2, 0, -3.4, [1.8, 0.95, 0.8], color="#9a6a48")
# TD the cargo hub today: day sky, giant hangars, tower
plane("TD", "skyday.png", 0, -1, -26, 96, 42)
for x in range(-20, 21, 4): box("TD", x, 0.07, 1.6, [1.4, 0.02, 0.16], color="#f2c230")
house("TD", -12, -13, [14, 7.5, 9], "#6a4aa0", color="#e8e6f0"); house("TD", 9, -15, [16, 8.5, 9], "#e07a2c", color="#ecebf2")
box("TD", 1, 0, -12, [1.8, 7, 1.8], color="#e4e0d8"); box("TD", 1, 7, -12, [3, 1.4, 3], color="#8fb3cc"); box("TD", 1, 8.4, -12, [3.4, 0.2, 3.4], color="#6a4aa0")

# ================================================================== CHARACTERS
human("fredV", "fred", pos("VG", -1.25, 0.06, -0.45), face="shocked"); human("dealer", "dealer", pos("VG", 0.3, 0.06, -3.0), face="shocked")
CARDS = dict(cardA=pos("VG", -0.05, 0.91, -1.15), cardK=pos("VG", 0.42, 0.91, -1.05))
for cid, p in CARDS.items(): put(cid, cid, p, 0.42, "up")
put("chips", "chips", pos("VG", -0.78, 0.91, -1.0), 0.5, "big")
JETS = []
for k in range(14):
    row = k % 2; x = -10 + (k // 2) * 3.1 + row * 1.5; z = -3.2 - row * 3.2; JETS.append(("J%d" % k, x, z, row))
    put("J%d" % k, "jet", pos("MP", x, 0.06, z), 1.15)
human("fredM", "fred", pos("MP", -3.2, 0.06, 0.5), face="happy")
put("jetH", "jet", PARK, 1.2)
PK = ["pk%d" % k for k in range(6)]
for k, cid in enumerate(PK): put(cid, "parcel", PARK, 0.44)
human("fredO", "fred", pos("OF", -0.4, 0.06, -2.5), face="neutral"); put("jar", "jar", pos("OF", 0.6, 0.8, -1.3), 0.6)
human("inv1", "inv1", PARK, face="happy"); human("inv2", "inv2", PARK, face="happy")
BILLS = ["b%d" % k for k in range(5)]
for cid in BILLS: put(cid, "bill", PARK, 0.32)
put("buoy", "buoy", PARK, 0.95)
put("jetm", "jet", PARK, 0.55, "fly", flip=True)
human("fredc", "fredc", pos("YL", -0.6, 0.06, -1.3), face="happy"); human("prof", "prof", pos("YL", 1.6, 0.06, -1.9), face="neutral")
put("paper", "paper", pos("YL", -0.25, 0.75, -0.2), 0.5)
TDJ = ((-13, -5, 1.6), (-9, -7.5, 1.4), (-5, -5, 1.6), (5, -5.5, 1.6), (9, -8, 1.4), (13, -5, 1.6), (-1, -9, 1.3), (16, -9, 1.3))
for k, (x, z, h) in enumerate(TDJ): put("T%d" % k, "jet", pos("TD", x, 0.06, z), h, flip=bool(k % 2))
put("jetT", "jet", PARK, 1.6, "fly")
PC = ["pc%d" % k for k in range(5)]
for k, cid in enumerate(PC): put(cid, "parcel", pos("TD", -2.6 + k * 1.3, 0.06, 1.4 + (k % 2) * 0.5), 0.6, "cheer", **({"flip": True} if k % 2 else {}))
human("fredT", "fred", pos("TD", 0.0, 0.06, 0.6), face="happy")

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}
ASP = dict(num1=5.64, last=3.73, bj=1.1, cal=0.92, jets14=4.36, mem=2.9, n186=1.67, n25=1.52, cash5=3.28, notenough=3.55, fredtag=3.45, founder=2.36,
           never=3.6, vegas=3.18, paid=2.08, nostrat=3.76, flying=3.73, yale=2.09, avg=2.9, saved=5.36, back=5.27, ques=1.0, bag=0.93, book=0.89,
           fuel=1.36, cmp=1.57, alive=3.0, crown=1.6, money=2.2, hearts=1.3, sparkle=1.0, poof=1.0)
N_ = [0]


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):               # a card at a safe spot of the frame, never near an edge
    (ax, ay, az), d = s["anchor"], s["distance"]; y = math.radians(s["yaw"]); w = dx * 0.41 * d    # along the camera's own right / forward axes
    show(s, at, who, [round(ax + w * math.cos(y) + dz * math.sin(y), 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az - w * math.sin(y) + dz * math.cos(y), 3)], hop=0.12)


def tag(s, at, name, dy=0.25, dx=0.0, dz=0.3, wf=0.24, hf=0.2, tilt=0, face="default"):
    """a fresh card sized for this shot (<= 30 % of the frame width, so a dolly-in never cuts it), hidden at the cut"""
    d = s["distance"]; h = round(min(wf * d / ASP[name], hf * 0.728 * d), 3); N_[0] += 1; cid = "%s_%d" % (name, N_[0])
    c = dict(id=cid, puppet="puppets/" + name, pos=PARK, height=h, face=face)
    if tilt: c["pose"] = dict(head=tilt)
    chars.append(c); SH[cid] = h; card(s, at, cid, dy, dx, dz); s["_tags"].append(cid); return cid


def temp(s, *who): s["_tags"].extend(who)                     # characters that leave with the cut


def S(start, **kw):
    s = shot(start, **kw); s["_tags"] = []; s["glide"] = "dolly"; s["pan"] = [v * 5 for v in s["pan"]]; return s


def hook_state(s):
    for cid, p in CARDS.items(): show(s, 0.0, cid, p, hop=0); act(s, 0.0, cid, face="up")
    show(s, 0.0, "chips", pos("VG", -0.78, 0.91, -1.0), hop=0); act(s, 0.0, "chips", face="big")
    show(s, 0.0, "fredV", pos("VG", -1.25, 0.06, -0.45), hop=0); act(s, 0.0, "fredV", face="shocked", pose=dict(armR=-150, armL=150))
    show(s, 0.0, "dealer", pos("VG", 0.3, 0.06, -3.0), hop=0); act(s, 0.0, "dealer", face="shocked"); tag(s, 0.0, "bj", 0.02, 0.24, 0.5); tag(s, 0.0, "num1", 0.29, 0.0, 0.4, wf=0.22)


HOOK = dict(anchor=pos("VG", -0.3, 1.3, -1.1), dist=4.6, yaw=-16, pitch=8, zoom=8, pan=(9, 0))
# ---- 0-3 hook: blackjack already won on frame 1; a FedEx jet takes off; the last $5,000 pushed in; the Las Vegas casino
s = S("0", out="cut", **HOOK); hook_state(s)
s = S("survived because", out="cut", anchor=pos("TD", 0, 3.0, -2), dist=16, yaw=10, pitch=-4, zoom=10, pan=(-9, 0))
show(s, 0.0, "jetT", pos("TD", -6, 0.6, -0.5), hop=0); go(s, 0.02, "jetT", pos("TD", 6, 4.8, -0.5), max(0.6, rel(s, "bet the") - 0.06), walk=False); temp(s, "jetT")
s = S("bet the company's", out="cut", anchor=pos("VG", -0.8, 1.2, -0.8), dist=3.8, yaw=18, pitch=6, zoom=10, pan=(-9, 0))
act(s, 0.0, "fredV", face="nervous", pose=dict(armR=0, armL=0)); act(s, 0.0, "dealer", face="neutral"); act(s, 0.0, "chips", face="default")
for cid in CARDS: hide(s, 0.0, cid)
show(s, 0.0, "chips", pos("VG", -1.0, 0.91, -0.7), hop=0); l_ = rel(s, "last five")
act(s, l_ - 0.25, "fredV", pose=dict(armR=-70)); go(s, l_ - 0.2, "chips", pos("VG", -0.25, 0.91, -1.25), 0.45, walk=False); tag(s, l_, "last", 0.27, 0.05)
s = S("on blackjack", out="cut", anchor=pos("VG", 0, 2.5, -3.5), dist=11, yaw=-12, pitch=4, zoom=-7, pan=(10, 0))
act(s, 0.0, "fredV", face="happy", pose=dict(armR=0)); act(s, rel(s, "blackjack"), "dealer", face="happy", shake=0.4)

# ---- 4-9 Memphis, April 1973: fourteen Falcon jets, the first night, 186 packages, 25 cities
s = S("In April", anchor=pos("MP", -3.0, 1.5, 0.4), dist=6.5, yaw=14, pitch=4, zoom=10, pan=(-9, 0))
act(s, 0.1, "fredM", pose=dict(armR=-150), face="happy"); tag(s, rel(s, "April"), "cal", 0.18, 0.2)
s = S("Federal Express launched", out="cut", anchor=pos("MP", 0, 1.6, -4.6), dist=15, yaw=-20, pitch=12, zoom=7, pan=(10, 0))
act(s, 0.0, "fredM", pose=dict(armR=0)); tag(s, rel(s, "fourteen small"), "jets14", 0.28)
s = S("out of Memphis", out="cut", anchor=pos("MP", -8, 4.2, -6), dist=13, yaw=26, pitch=-5, zoom=10, pan=(-9, 2)); tag(s, rel(s, "Memphis"), "mem", 0.26)
s = S("On that first night", out="cut", anchor=pos("MP", 2.4, 0.9, 1.0), dist=6, yaw=-10, pitch=6, zoom=10, pan=(9, 0))
show(s, 0.0, "jetH", pos("MP", 3.6, 0.06, 0.6), hop=0); act(s, 0.0, "jetH", face="default"); temp(s, "jetH", *PK)
n_ = rel(s, "186")
for k, cid in enumerate(PK):
    show(s, 0.0, cid, pos("MP", 0.2 + k * 0.42, 0.06, 1.7 + (k % 2) * 0.25), hop=0); act(s, 0.0, cid, face="default")
    go(s, 0.25 + 0.22 * k, cid, pos("MP", 2.9, 0.5, 1.0), 0.3, walk=False); hide(s, 0.57 + 0.22 * k, cid)
tag(s, n_, "n186", 0.26, -0.15)
s = S("to 25 cities", out="cut", anchor=pos("OP", 0.6, 3.2, -4.8), dist=9, yaw=8, pitch=2, zoom=9, pan=(-10, 0)); tag(s, rel(s, "25"), "n25", 0.27, -0.2)
s = S("Fourteen jets for", out="cut", anchor=pos("MP", 0, 1.3, -2.4), dist=12, yaw=6, pitch=10, zoom=-8, pan=(-10, 0))
show(s, 0.0, "fredM", pos("MP", -1.9, 0.06, 0.8), hop=0); act(s, 0.0, "fredM", face="confused")
for k, cid in enumerate(PK[:3]): show(s, 0.0, cid, pos("MP", 0.0 + k * 0.6, 0.06, 1.0), hop=0); act(s, 0.0, cid, face="shocked")
temp(s, *PK[:3]); tag(s, 0.1, "cmp", 0.24, 0.1)

# ---- 10-13 money trouble: fuel costs, the vanishing cash, $5,000 left, the jets can't fly
s = S("Fuel costs", out="cut", anchor=pos("OF", -0.4, 1.6, -2.2), dist=5.5, yaw=-14, pitch=4, zoom=12, pan=(9, 0))
tag(s, rel(s, "Fuel"), "fuel", 0.2, 0.08); act(s, rel(s, "climbing"), "fredO", face="nervous")
s = S("and the money", anchor=pos("OF", 0.4, 1.25, -1.4), dist=3.6, yaw=16, pitch=10, zoom=10, pan=(-9, 0))
v_ = rel(s, "vanishing"); act(s, 0.0, "jar", face="default"); act(s, v_, "jar", face="empty", shake=0.4); temp(s, *BILLS)
for k, cid in enumerate(BILLS):
    show(s, v_ - 0.1, cid, pos("OF", 0.6, 1.1, -1.25), hop=0); go(s, v_ - 0.05 + 0.05 * k, cid, pos("OF", 0.6 + (k - 2) * 0.45, 2.7 + 0.15 * k, -1.2), 0.5, walk=False)
s = S("Then the company's", out="cut", anchor=pos("OF", -0.4, 1.5, -2.3), dist=4.2, yaw=-6, pitch=2, zoom=9, pan=(7, 2))
f_ = rel(s, "fell"); act(s, f_, "fredO", face="shocked", shake=0.4); tag(s, f_, "cash5", 0.27, 0.0, wf=0.2, tilt=-8)
s = S("Nowhere near", out="cut", anchor=pos("MP", -2, 1.0, -3.2), dist=7, yaw=-24, pitch=6, zoom=9, pan=(10, 0))
for cid, *_ in JETS: act(s, 0.0, cid, face="sad")
tag(s, 0.15, "notenough", 0.27)

# ---- 14-19 Fred Smith goes to Las Vegas: $5,000 becomes $27,000
s = S("You see", out="cut", anchor=pos("OF", -0.4, 1.4, -2.3), dist=5, yaw=20, pitch=0, zoom=10, pan=(-10, 0))
act(s, 0.0, "fredO", face="smug", pose=dict(armR=-150)); tag(s, rel(s, "founder#2"), "founder", 0.29); tag(s, rel(s, "Fred"), "fredtag", 0.17)
s = S("did something", out="cut", anchor=pos("OF", -0.4, 1.6, -2.0), dist=5, yaw=-18, pitch=6, zoom=-8, pan=(9, 0))
act(s, 0.0, "fredO", face="sneaky", pose=dict(armR=0)); tag(s, 0.05, "book", 0.1, 0.2); tag(s, rel(s, "teach"), "never", 0.08, 0.18, 0.5, tilt=-10)
s = S("He flew to", out="cut", anchor=pos("OP", -1.0, 3.3, -4.8), dist=7.5, yaw=-10, pitch=0, zoom=10, pan=(9, 0))
show(s, 0.0, "jetm", pos("OP", 0.75, 2.95, -4.55), hop=0); go(s, 0.05, "jetm", pos("OP", -2.66, 3.15, -4.55), max(0.6, rel(s, "sat down") - 0.15), walk=False)
temp(s, "jetm"); tag(s, rel(s, "Las Vegas#2"), "vegas", 0.27, 0.05)
s = S("sat down", out="cut", anchor=pos("VG", -0.6, 1.3, -1.4), dist=6, yaw=10, pitch=8, zoom=8, pan=(-10, 0))
show(s, 0.0, "fredV", pos("VG", -4.2, 0.06, -0.4), hop=0); go(s, 0.05, "fredV", pos("VG", -1.25, 0.06, -0.45), 0.85); act(s, 0.0, "fredV", face="happy")
act(s, 0.0, "chips", face="default"); show(s, 0.0, "chips", pos("VG", -0.78, 0.91, -1.0), hop=0)
dl = max(0.5, rel(s, "blackjack table") - 0.1)
for k, (cid, p) in enumerate(CARDS.items()):
    act(s, 0.0, cid, face="default"); show(s, dl + 0.15 * k, cid, pos("VG", 0.3, 0.91, -2.2), hop=0); go(s, dl + 0.02 + 0.15 * k, cid, p, 0.3, walk=False)
act(s, dl, "dealer", pose=dict(armR=-70), face="happy")
s = S("and turned that", anchor=pos("VG", 0.15, 1.15, -1.1), dist=3.0, yaw=-8, pitch=18, zoom=10, pan=(9, 0))
t_ = rel(s, "turned"); act(s, 0.0, "dealer", pose=dict(armR=0), face="neutral"); show(s, 0.0, "dealer", pos("VG", 1.0, 0.06, -3.0), hop=0)
act(s, t_ + 0.1, "cardA", face="up", shake=0.3); act(s, t_ + 0.4, "cardK", face="up", shake=0.3); tag(s, rel(s, "five thousand#3"), "money", 0.28)
s = S("twentyseven", out="cut", anchor=pos("VG", -0.6, 1.3, -1.0), dist=4.4, yaw=20, pitch=6, zoom=14, pan=(-8, 2))
act(s, 0.0, "chips", face="big", shake=0.5); act(s, 0.0, "fredV", face="shocked", pose=dict(armR=-150, armL=150)); act(s, 0.5, "fredV", face="happy")
act(s, 0.0, "dealer", face="shocked"); tag(s, 0.0, "money", 0.28, face="won"); tag(s, 0.15, "bj", 0.0, 0.25, 0.5)

# ---- 20-25 paid, a lifeline, the jets fly again, investors, $11 million, alive
s = S("One card table", out="cut", anchor=pos("OF", -1.0, 1.7, -3.0), dist=6, yaw=10, pitch=4, zoom=10, pan=(-9, 0))
act(s, 0.0, "jar", face="default"); act(s, 0.0, "fredO", face="happy", pose=dict(armR=0)); tag(s, rel(s, "paid"), "paid", 0.12, -0.12, 0.6, wf=0.2, tilt=-10)
s = S("Not a strategy", out="cut", anchor=pos("OF", -0.4, 1.5, -2.2), dist=4.6, yaw=-20, pitch=4, zoom=12, pan=(10, 0))
act(s, 0.0, "fredO", face="nervous"); tag(s, rel(s, "Not"), "nostrat", 0.27, tilt=-8); li = rel(s, "lifeline")
show(s, li - 0.05, "buoy", pos("OF", -0.4, 3.4, -1.9), hop=0); go(s, li, "buoy", pos("OF", -0.4, 0.95, -1.9), 0.3, walk=False); temp(s, "buoy")
act(s, li + 0.3, "fredO", face="happy", shake=0.3); tag(s, li + 0.35, "hearts", 0.2, 0.22)
s = S("The jets kept", out="cut", anchor=pos("MP", 0, 2.4, -4.4), dist=14, yaw=16, pitch=-2, zoom=8, pan=(-10, 0))
d_ = rel(s, "investors came")
for cid, x, z, row in JETS:
    act(s, 0.0, cid, face="fly")
    if row == 0: go(s, 0.05 + 0.04 * (x + 10), cid, pos("MP", x + 5, 3.5 + 0.25 * (x + 10), z), max(0.5, d_ - 0.1), walk=False)
tag(s, 0.1, "flying", 0.29)
s = S("investors came", out="cut", anchor=pos("OF", -0.4, 1.4, -1.8), dist=7, yaw=-8, pitch=4, zoom=-8, pan=(9, 0))
show(s, 0.0, "inv1", pos("OF", -4.0, 0.06, -1.0), hop=0); go(s, 0.02, "inv1", pos("OF", -2.1, 0.06, -1.1), 0.8)
show(s, 0.0, "inv2", pos("OF", 3.4, 0.06, -1.0), hop=0); go(s, 0.08, "inv2", pos("OF", 1.4, 0.06, -1.1), 0.8)
act(s, 0.0, "fredO", face="happy"); tag(s, 0.3, "back", 0.29)
s = S("and Smith raised", out="cut", anchor=pos("OF", -0.4, 1.4, -2.0), dist=4.4, yaw=14, pitch=2, zoom=12, pan=(-7, 2))
e_ = rel(s, "eleven"); act(s, e_, "fredO", face="happy", pose=dict(armR=-150, armL=150), shake=0.3); tag(s, e_, "bag", 0.08, 0.2)
act(s, e_, "inv1", face="smug"); act(s, e_, "inv2", face="happy"); tag(s, rel(s, "more"), "sparkle", 0.26, -0.2)
s = S("The tiny overnight", out="cut", anchor=pos("MP", 0.8, 3.3, 0.2), dist=8, yaw=-12, pitch=-6, zoom=10, pan=(10, 0))
show(s, 0.0, "jetH", pos("MP", -0.6, 2.7, 0.0), hop=0); act(s, 0.0, "jetH", face="fly"); go(s, 0.02, "jetH", pos("MP", 1.6, 3.3, 0.0), max(0.6, rel(s, "And the idea") - 0.06), walk=False)
temp(s, "jetH"); tag(s, rel(s, "alive"), "alive", 0.28)

# ---- 26-30 the idea: a Yale term paper, graded C; saved by a card game
s = S("And the idea", anchor=pos("YL", 0, 1.9, -2.5), dist=9.5, yaw=-14, pitch=8, zoom=8, pan=(10, 0)); tag(s, 0.1, "ques", 0.2, 0.25)
s = S("It started", out="cut", anchor=pos("YL", -0.5, 1.2, -0.9), dist=4.2, yaw=16, pitch=8, zoom=10, pan=(-9, 0))
act(s, 0.0, "fredc", face="happy", pose=dict(armR=-60)); tag(s, rel(s, "Yale"), "yale", 0.28, 0.1)
s = S("His grade", out="cut", anchor=pos("YL", 0.2, 1.3, -0.9), dist=5, yaw=-18, pitch=4, zoom=12, pan=(9, 0))
go(s, 0.0, "prof", pos("YL", 0.75, 0.06, -1.0), 0.6); c_ = rel(s, "C")
act(s, c_, "paper", face="graded", shake=0.5); act(s, c_, "prof", face="smug", pose=dict(armR=-120)); act(s, c_ + 0.1, "fredc", face="shocked", pose=dict(armR=0))
s = S("Graded average", out="cut", anchor=pos("YL", -0.6, 1.4, -1.0), dist=3.6, yaw=6, pitch=2, zoom=14, pan=(-7, 0))
act(s, 0.0, "fredc", face="nervous"); act(s, 0.0, "prof", pose=dict(armR=0)); tag(s, 0.05, "avg", 0.28)
s = S("saved by", out="cut", anchor=pos("VG", 0.15, 1.2, -1.1), dist=3.4, yaw=22, pitch=14, zoom=10, pan=(-10, 0))
for cid, p in CARDS.items(): act(s, 0.0, cid, face="up")
act(s, 0.0, "chips", face="big"); tag(s, 0.05, "saved", 0.28)

# ---- 31 today: the world's biggest cargo airline; 32 loop: the first shot again
s = S("and today", out="cut", anchor=pos("TD", 0, 2.6, -3), dist=15, yaw=-14, pitch=10, zoom=-7, pan=(10, 0))
show(s, 0.0, "jetT", pos("TD", -7, 4.6, -6), hop=0); go(s, 0.02, "jetT", pos("TD", 7, 6.2, -6), max(0.6, rel(s, "cargo airline#2") - 0.06), walk=False); temp(s, "jetT")
act(s, 0.0, "fredT", pose=dict(armR=-150, armL=150))
for k, cid in enumerate(PC): act(s, 0.05 * k, cid, shake=0.4)
tag(s, rel(s, "today"), "crown", 0.2)
s = S("cargo airline#2", **HOOK); s["start"] = round(say("cargo airline#2"), 3); hook_state(s)
for s in shots:
    if "anchor" in s: s.setdefault("frameY", 0.0)                # anchor at the frame centre (the stage default puts it 12 % high)

# ---- every card / temporary character leaves one frame before the next shot
starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots):
    if k + 1 < len(shots):
        for cid in s["_tags"]: hide(s, round(starts[k + 1] - starts[k] - 0.04, 3), cid)
    s.pop("_tags")

# ================================================================== SPEC
dusk = lambda ph: {"t": round(say(ph), 3), "mood": "dusk", "fade": 0.02}
day = lambda ph: {"t": round(say(ph), 3), "mood": "day", "fade": 0.02}
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6,
    "moods": {"day": {"sun": {"azimuth": 40, "elevation": 46, "color": "#ffe8c8", "intensity": 2.4},
                      "sky": {"top": "#5b8ee0", "horizon": "#f6d6b0"}, "fill": {"sky": "#a0b4ff", "ground": "#6a4b6e", "intensity": 1.2}},
              "dusk": {"sun": {"azimuth": 250, "elevation": 16, "color": "#ffb47a", "intensity": 2.1},
                       "sky": {"top": "#4a3c8a", "horizon": "#f59a6a"}, "fill": {"sky": "#9a8ae0", "ground": "#6a4a6e", "intensity": 1.15}}},
    "lighting": [{"t": 0, "mood": "day"}, dusk("In April"), day("Fuel costs"), dusk("Nowhere near"), day("You see"), dusk("The jets kept"), day("investors came"),
                 dusk("The tiny overnight"), day("And the idea")],
    "ground": {"texture": TEX + "asphalt.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky73.jpg", "blur": 4}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
cues = dict(takeoff=say("survived because"), bet=say("last five"), vegas=say("Las Vegas"), april=say("April"), launch=say("Federal Express launched"),
            first=say("On that first night"), cities=say("25"), cmp=say("Fourteen jets for"), fuel=say("Fuel costs"), vanish=say("vanishing"),
            tense=say("Then the company's"), fell=say("fell"), nowhere=say("Nowhere near"), yousee=say("You see"), fred=say("Fred"), teach=say("teach"),
            flew=say("He flew to"), sat=say("sat down"), deal=say("blackjack table"), turned=say("turned"), won=say("twentyseven"), paid=say("paid"),
            notstrat=say("Not a strategy"), strategy=say("strategy"), lifeline=say("lifeline"), jets=say("The jets kept"), inv=say("investors came"),
            eleven=say("eleven"), alive=say("alive"), idea=say("And the idea"), yale=say("Yale"), grade=say("C"), saved=say("saved by"),
            today=say("and today"), loop=say("cargo airline#2"), end=DURATION)
cp, wav = os.path.join(P, "audio", "cues.json"), os.path.join(P, "audio", "music.wav")
json.dump(cues, open(cp, "w"))
if os.environ.get("NO_MUSIC") != "1":
    subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), wav, "%.2f" % (DURATION + 0.4), cp], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", os.path.join(P, "audio", "music.mp3")], check=True)
    os.remove(wav)

# ---- sanity report: shot timing + actions that overrun or overlap
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
