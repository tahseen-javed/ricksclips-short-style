#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 07: who named Black Friday.
usage: build_short.py <project folder>
Seven sets 70 units apart: DT Philadelphia downtown 1961 (the hook, the gridlock), ST the Army-Navy stadium, PD the police
station, MR the department store, US the map room, EI the 1980s sales office, TD the mall of today.  Every shot has a camera
move (dolly + orbit); the hook frame keeps the whole character and every card inside the frame (pull-out, never a push-in).
Cards are sized from the shot distance and leave one frame before the next shot; the last shot repeats the first for the loop."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(DT=0, ST=70, PD=140, MR=210, US=280, EI=350, TD=420)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK
ASP = json.load(open(os.path.join(P, "aspect.json")))


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


# ================================================================== SETS
# DT Philadelphia 1961: sidewalk, three shopfronts, lamps, a traffic podium, crosswalk, lane line, skyline
plane("DT", "skyphl.png", 0, -1, -30, 96, 42)
box("DT", 0, 0, -5.25, [34, 0.15, 2.6], color="#d4ccbe"); box("DT", 0, 0, -3.98, [34, 0.17, 0.12], color="#b8b0a2")
for x, w, h, roof, wall, img in ((-7, 5.2, 6.2, "#8a4a6a", "#e8b4ba", "shop_toys"), (0, 6.4, 7.6, "#3a6a58", "#f4deb0", "shop_dept"), (7, 5.2, 6.0, "#3a4a7a", "#b8d8e2", "shop_shoes")):
    house("DT", x, -9, [w, h, 5], roof, color=wall); fw = w - 0.8; plane("DT", img + ".png", x, 0.15, -6.44, fw, fw * 1300 / 1200)
for x, col in ((-13.2, "#c9a0d8"), (13.2, "#f2c48a")): house("DT", x, -9.5, [6.6, 5.2, 5], "#6a5a7a", color=col)
for x in (-10.2, -3.6, 3.6, 10.2): post("DT", x, -4.3, 3.4, "#33405a")
box("DT", 0, 0, 0.5, [1.1, 0.35, 1.1], color="#f2c230"); box("DT", 0, 0.35, 0.5, [1.2, 0.05, 1.2], color="#e04a50")
for k in range(7): box("DT", -3 + k, 0.07, 3.0, [0.55, 0.02, 2.0], color="#f4f4f4")
for x in range(-18, 19, 3): box("DT", x, 0.07, -1.0, [1.4, 0.02, 0.14], color="#f2c230")
# ST the stadium: grass field, yard lines, goalposts, packed stands
plane("ST", "skyday.png", 0, -1, -30, 96, 42)
box("ST", 0, 0, -3, [34, 0.05, 22], texture="grass.jpg", repeat=[8, 6])
for x in range(-15, 16, 3): box("ST", x, 0.06, -3, [0.14, 0.02, 20], color="#ffffff")
box("ST", 0, 0, -12.9, [34, 7.0, 0.4], color="#8e94a6"); plane("ST", "stands.png", 0, 0, -12.6, 34, 10)
for x in (-1.6, 1.6): post("ST", x, -8, 4.2, "#f2d230")
box("ST", 0, 1.9, -8, [3.4, 0.16, 0.16], color="#f2d230"); post("ST", 0, -8.2, 1.9, "#f2d230")
# PD the police station: wood floor, blue walls, lockers / clock / sign wall, desk
box("PD", 0, 0, -1, [12, 0.06, 9], texture="wood.jpg", repeat=[3, 3]); box("PD", 0, 0, -5, [12, 5.6, 0.3], color="#86a2bc")
for sg in (-1, 1): box("PD", sg * 5.85, 0, -1, [0.3, 5.6, 9], color="#7894ae")
plane("PD", "pdwall.png", 0, 0.06, -4.82, 11, 5.04)
# MR the 1961 department store: checker floor, shelves wall, glass counters
box("MR", 0, 0, -1, [12, 0.06, 10], texture="tiles.jpg", repeat=[4, 4]); box("MR", 0, 0, -5, [12, 7, 0.3], color="#f4d9a8")
for sg in (-1, 1): box("MR", sg * 5.85, 0, -1, [0.3, 7, 10], color="#ead0a0")
plane("MR", "storewall.png", 0, 0.06, -4.82, 11, 5.04)
for x in (-3.6, 3.6): box("MR", x, 0, -2.6, [2.0, 0.9, 0.8], color="#a0644a"); box("MR", x, 0.9, -2.6, [2.1, 0.08, 0.9], color="#cdeaf5")
# US the map room: tall navy wall, the map
box("US", 0, 0, -1, [14, 0.06, 9], color="#3a4660"); box("US", 0, 0, -5, [14, 12, 0.3], color="#2f4a6e")
for sg in (-1, 1): box("US", sg * 6.85, 0, -1, [0.3, 12, 9], color="#2a4262")
plane("US", "usmap.png", 0, 3.2, -4.82, 6.4, 3.91)
# EI the 1980s sales office: teal/pink checker floor, Memphis wall, desk + computer, an easel for the ledger
box("EI", 0, 0, -1, [12, 0.06, 10], texture="tiles80.jpg", repeat=[4, 4]); box("EI", 0, 0, -5, [12, 6, 0.3], color="#fad6e2")
for sg in (-1, 1): box("EI", sg * 5.85, 0, -1, [0.3, 6, 10], color="#7ad8d4")
plane("EI", "eighties.png", 0, 0.06, -4.82, 11, 5.04)
box("EI", -2.8, 0, -2.8, [2.0, 0.74, 0.9], color="#2b2b3a"); box("EI", -2.8, 0.74, -2.8, [2.1, 0.06, 1.0], color="#ff70c0"); box("EI", -2.9, 0.8, -3.0, [0.7, 0.6, 0.6], color="#e8e0cc")
for x in (0.75, 1.85): box("EI", x, 0, -3.45, [0.08, 1.4, 0.08], color="#8a5a3a")
# TD the mall today: glossy floor, MEGA STORE front, ceiling lights
box("TD", 0, 0, -1, [14, 0.06, 10], texture="mallfloor.jpg", repeat=[5, 4]); box("TD", 0, 0, -5, [14, 7, 0.3], color="#ececf4")
for sg in (-1, 1): box("TD", sg * 6.85, 0, -1, [0.3, 7, 10], color="#d8d8e6")
plane("TD", "mall.png", 0, 0.06, -4.82, 11.5, 6.23)
for x in (-4, 0, 4): box("TD", x, 6.6, -2, [2.4, 0.12, 0.6], color="#fff6c0")

# ================================================================== CHARACTERS
SHOP0 = pos("DT", -7, 0.15, -5.0)
human("shopD", "shopk", SHOP0, face="happy"); put("bagsD", "bags", pos("DT", -6.05, 0.15, -4.75), 0.5)
human("copD", "cop", pos("DT", 0, 0.4, 0.5), face="shouting")
CARS = [("c%d" % k, ("carB", "carA", "carC")[k % 3], x) for k, x in enumerate((-12.6, -3.6, -0.6, 2.4, 5.4, 8.4, 11.4))]
for cid, nm, x in CARS: put(cid, nm, pos("DT", x, 0.06, -2.4), 1.25)
human("lady", "lady", pos("DT", -1.6, 0.06, 3.0), face="happy"); human("dad", "dad", pos("DT", -4.6, 0.06, 2.9), face="happy")
human("kid", "kid", pos("DT", -5.4, 0.06, 3.3), face="happy", h=1.25); human("granny", "granny", pos("DT", 4.6, 0.06, 2.8), face="happy", h=1.6)
human("fan", "fan", pos("ST", 4.6, 0.06, 0.6), face="happy"); human("fan2", "fan2", pos("ST", -4.6, 0.06, 0.4), face="happy"); put("ball", "football", PARK, 0.5)
human("copP", "cop", pos("PD", -2.0, 0.06, -3.4), face="nervous"); human("sarge", "sarge", pos("PD", 0.75, 0.06, -3.2), face="neutral")
put("board", "board", pos("PD", 1.8, 1.2, -4.62), 1.45)
human("shopM", "shopk", pos("MR", -0.8, 0.06, -1.8), face="neutral"); put("bigfri", "bigfri", PARK, 1.0)
human("ladyM", "lady", pos("MR", 3.2, 0.06, -1.2), face="neutral"); human("kidM", "kid", pos("MR", 4.0, 0.06, -1.0), face="neutral", h=1.25)
PINS = [(1560, 400), (1450, 330), (1380, 540), (1250, 410), (1120, 600), (980, 330), (860, 520), (700, 420), (560, 620), (420, 330), (300, 500), (220, 300)]
for k in range(len(PINS)): put("p%d" % k, "pin", PARK, 0.42)
for k in range(3): put("n%d" % k, "news", PARK, 2.2)
human("exec", "exec", pos("EI", -0.3, 0.06, -2.4), face="happy"); put("ledger", "ledger", pos("EI", 1.3, 0.9, -3.35), 1.0)
human("clerk", "clerk", pos("TD", 0.2, 0.06, -3.6), face="happy")
human("teen", "teen", pos("TD", -4.2, 0.06, -1.8), face="happy"); human("kidT", "kid", pos("TD", 4.2, 0.06, -1.6), face="happy", h=1.25)
human("dadT", "dad", pos("TD", 5.0, 0.06, -2.8), face="happy")
put("bagsT", "bags", pos("TD", -0.35, 0.06, -1.4), 0.5); put("bagsT2", "bags", pos("TD", 0.35, 0.06, -1.35), 0.5)
for cid in ("steamD", "steamM"): put(cid, "steam", PARK, 0.42)

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}
N_ = [0]


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):               # a card at a safe spot of the frame, never near an edge
    (ax, ay, az), d = s["anchor"], s["distance"]; y = math.radians(s["yaw"]); w = dx * 0.41 * d
    show(s, at, who, [round(ax + w * math.cos(y) + dz * math.sin(y), 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az - w * math.sin(y) + dz * math.cos(y), 3)], hop=0.12)


def tag(s, at, name, dy=0.25, dx=0.0, dz=0.3, wf=0.24, hf=0.2, tilt=0, face="default"):
    d = s["distance"]; h = round(min(wf * d / ASP[name], hf * 0.728 * d), 3); N_[0] += 1; cid = "%s_%d" % (name, N_[0])
    c = dict(id=cid, puppet="puppets/" + name, pos=PARK, height=h, face=face)
    if tilt: c["pose"] = dict(head=tilt)
    chars.append(c); SH[cid] = h; card(s, at, cid, dy, dx, dz); s["_tags"].append(cid); return cid


def temp(s, *who): s["_tags"].extend(who)


def S(start, **kw):
    s = shot(start, **kw); s["_tags"] = []; s["glide"] = "dolly"; s["pan"] = [v * 5 for v in s["pan"]]; return s


def honk(s, at, cids=None, face="honk"):
    for k, (cid, _, _) in enumerate(CARS):
        if cids is None or cid in cids: act(s, at + 0.06 * k, cid, face=face, shake=0.35 if face == "honk" else 0)


def hook_state(s):
    show(s, 0.0, "shopD", SHOP0, hop=0); act(s, 0.0, "shopD", face="happy", pose=dict(armR=-150, armL=150)); return tag(s, 0.0, "bfsign", 0.3, 0.0, 0.4)


HOOK = dict(anchor=pos("DT", -7, 1.45, -5.0), dist=6.0, yaw=8, pitch=6, zoom=-5, pan=(6, 0))
# ---- 0-1 hook: a happy shopkeeper under the BLACK FRIDAY sign -> NOT THEM!  -> the furious traffic cop
s = S("0", out="cut", **HOOK); hook_state(s); w_ = rel(s, "wasn't")
tag(s, w_, "notthem", 0.19, 0.05, 0.5, wf=0.2, tilt=-10); act(s, w_, "shopD", face="shocked", pose=dict(armR=0, armL=0), shake=0.3)
s = S("It was named", out="cut", anchor=pos("DT", 0, 1.5, 0.5), dist=5.6, yaw=16, pitch=-4, zoom=10, pan=(-9, 0))
act(s, 0.0, "copD", face="shouting", pose=dict(armR=-150, armL=0)); f_ = rel(s, "furious"); honk(s, f_)
show(s, f_, "steamD", pos("DT", 0.0, 2.25, 0.55)); act(s, f_, "copD", shake=0.4); temp(s, "steamD"); tag(s, rel(s, "cops"), "cops", 0.36)

# ---- 2-6 Philadelphia 1961: the day after Thanksgiving, shoppers flood downtown; Saturday the Army-Navy game, tourists
s = S("Philadelphia", out="cut", anchor=pos("DT", 0, 2.6, -2), dist=17, yaw=-8, pitch=10, zoom=7, pan=(10, 0))
honk(s, 0.0, face="default"); act(s, 0.0, "copD", face="happy", pose=dict(armR=-150, armL=150)); tag(s, 0.05, "philly", 0.28)
s = S("The day after", out="cut", anchor=pos("DT", -1.6, 1.3, 3.0), dist=5.8, yaw=-14, pitch=6, zoom=10, pan=(9, 0))
act(s, 0.0, "lady", face="happy", pose=dict(armR=-60)); tag(s, 0.05, "thx", 0.3, wf=0.3); t_ = rel(s, "Thanksgiving"); tag(s, t_, "turkey", 0.05, -0.3, 0.5, wf=0.2, hf=0.16)
act(s, t_, "lady", face="shocked", pose=dict(armR=-150))
s = S("suburban shoppers", out="cut", anchor=pos("DT", -0.6, 1.3, 3.0), dist=9.5, yaw=10, pitch=8, zoom=8, pan=(-9, 0))
act(s, 0.0, "lady", face="happy", pose=dict(armR=0)); go(s, 0.0, "kid", pos("DT", -0.9, 0.06, 3.3), 1.2); go(s, 0.05, "dad", pos("DT", -0.15, 0.06, 2.9), 1.2)
go(s, 0.1, "granny", pos("DT", 0.4, 0.06, 2.6), 1.2); tag(s, rel(s, "flood"), "flood", 0.3, wf=0.3)
s = S("Then on Saturday", out="cut", anchor=pos("ST", 0, 3.2, -6), dist=19, yaw=12, pitch=8, zoom=7, pan=(10, 0))
tag(s, rel(s, "armynavy"), "armynavy", 0.3); k_ = rel(s, "football")
show(s, k_ - 0.2, "ball", pos("ST", 0, 0.1, -1.0), hop=0); go(s, k_, "ball", pos("ST", 0, 3.4, -8.3), max(0.3, min(0.8, rel(s, "and the tourists") - k_ - 0.12)), walk=False); temp(s, "ball")
s = S("and the tourists", out="cut", anchor=pos("ST", 0, 1.35, 0.5), dist=7.2, yaw=-14, pitch=6, zoom=8, pan=(9, 0))
go(s, 0.0, "fan", pos("ST", 0.5, 0.06, 0.6), 0.9); go(s, 0.06, "fan2", pos("ST", -0.45, 0.06, 0.4), 0.9)
for cid in ("fan", "fan2"): act(s, 0.95, cid, pose=dict(armR=-150, armL=150), shake=0.3)
tag(s, rel(s, "tourists"), "tourists", 0.3)

# ---- 7-9 Gridlock. Crowds. Chaos.
s = S("Gridlock", out="cut", anchor=pos("DT", -2.0, 0.9, -2.4), dist=7.5, yaw=-24, pitch=8, zoom=12, pan=(9, 0))
honk(s, 0.0); tag(s, 0.05, "gridlock", 0.3, tilt=-8, wf=0.22)
s = S("Crowds", out="cut", anchor=pos("DT", -0.5, 1.25, 3.0), dist=8.6, yaw=16, pitch=4, zoom=8, pan=(-9, 0))
for k, cid in enumerate(("kid", "dad", "granny", "lady")): act(s, 0.04 * k, cid, face=("shocked", "nervous")[k % 2], shake=0.4)
tag(s, 0.05, "crowds", 0.32, tilt=8, wf=0.2)
s = S("Chaos", out="cut", anchor=pos("DT", 0, 1.45, 0.5), dist=5.2, yaw=-26, pitch=12, zoom=14, pan=(-8, 2))
act(s, 0.0, "copD", face="shouting", pose=dict(armR=-150, armL=150), shake=0.6); show(s, 0.0, "steamD", pos("DT", 0.0, 2.3, 0.55), hop=0); temp(s, "steamD")
honk(s, 0.0); tag(s, 0.05, "chaos", 0.33, tilt=10, wf=0.2)
for cid, x in (("kid", -5.6), ("lady", -4.8), ("dad", 4.8), ("granny", 5.6)): show(s, 0.0, cid, pos("DT", x, 0.06, 3.0), hop=0)

# ---- 10-13 the police station: no day off, twelve-hour shifts, a dark name: BLACK FRIDAY
s = S("No traffic cop", out="cut", anchor=pos("PD", -1.2, 1.35, -3.0), dist=7, yaw=12, pitch=6, zoom=10, pan=(-9, 0))
act(s, 0.0, "copP", face="nervous"); tag(s, rel(s, "day off"), "nodayoff", 0.3)
s = S("They work", out="cut", anchor=pos("PD", -2.0, 1.4, -3.4), dist=5, yaw=-16, pitch=4, zoom=12, pan=(9, 0))
tw = rel(s, "twelvehour"); act(s, tw, "copP", face="shocked", shake=0.4); tag(s, tw, "h12", 0.27); act(s, tw + 0.6, "copP", face="nervous")
s = S("So the police", out="cut", anchor=pos("PD", 1.2, 1.7, -3.9), dist=8, yaw=-10, pitch=4, zoom=-6, pan=(9, 0))
dk_ = rel(s, "dark name"); act(s, 0.0, "sarge", face="shouting", pose=dict(armR=-110)); act(s, dk_, "sarge", pose=dict(armR=-150), shake=0.3); tag(s, dk_, "dark", 0.34)
s = S("Black Friday#2", out="cut", anchor=pos("PD", 1.8, 1.95, -4.3), dist=4.4, yaw=8, pitch=2, zoom=10, pan=(-8, 0))
act(s, 0.05, "board", face="named", shake=0.5); show(s, 0.0, "sarge", pos("PD", -0.8, 0.06, -3.2), hop=0)

# ---- 14-20 stores hate it: BIG FRIDAY flops, the name won't die, spreads coast to coast, a new plan
s = S("Stores hate it", out="cut", anchor=pos("MR", -0.8, 1.45, -1.8), dist=5.6, yaw=14, pitch=4, zoom=10, pan=(-9, 0))
act(s, 0.0, "shopM", face="shouting", pose=dict(armR=-150, armL=150), shake=0.4); show(s, 0.1, "steamM", pos("MR", -0.8, 1.95, -1.75)); temp(s, "steamM")
tag(s, rel(s, "hate"), "hate", 0.33)
s = S("That same year", out="cut", anchor=pos("MR", 0, 2.2, -3.0), dist=10, yaw=-10, pitch=6, zoom=7, pan=(9, 0))
b_ = rel(s, "Big Friday"); act(s, 0.0, "shopM", face="sneaky", pose=dict(armR=0, armL=0)); tag(s, rel(s, "rebrand"), "rebrand", -0.05, 0.12, wf=0.14)
show(s, b_ - 0.3, "bigfri", pos("MR", 0, 5.0, -4.4), hop=0); go(s, b_ - 0.25, "bigfri", pos("MR", 0, 3.4, -4.4), 0.3, walk=False)
act(s, b_ + 0.05, "shopM", face="happy", pose=dict(armR=-150, armL=150), shake=0.3)
s = S("Nobody says", out="cut", anchor=pos("MR", -0.35, 1.9, -2.4), dist=8.4, yaw=14, pitch=6, zoom=8, pan=(-9, 0))
act(s, 0.0, "shopM", face="nervous", pose=dict(armR=0, armL=0)); go(s, 0.0, "ladyM", pos("MR", -2.2, 0.06, -1.2), 1.4); go(s, 0.1, "kidM", pos("MR", -1.4, 0.06, -1.0), 1.4)
for cid in ("ladyM", "kidM"): act(s, 0.0, cid, face="confused")
tag(s, 0.05, "nobody", 0.2, wf=0.24, tilt=-6); tag(s, rel(s, "Big Friday#2"), "cricket", 0.02, 0.28, 0.6, wf=0.12); act(s, rel(s, "Big Friday#2"), "bigfri", shake=0.3)
s = S("You see", out="cut", anchor=pos("MR", -0.8, 1.5, -1.8), dist=5.4, yaw=-16, pitch=6, zoom=10, pan=(9, 0))
show(s, 0.0, "ladyM", pos("MR", 4.4, 0.06, -1.2), hop=0); show(s, 0.0, "kidM", pos("MR", 5.0, 0.06, -1.0), hop=0)
sg_ = tag(s, 0.05, "bfsign", 0.3); r_ = rel(s, "refuses"); act(s, r_, "shopM", face="shouting", pose=dict(armR=-150), shake=0.3)
act(s, r_ + 0.15, sg_, shake=0.5); d_ = rel(s, "die"); act(s, d_, sg_, shake=0.5); tag(s, d_, "wontdie", 0.17)
s = S("Slowly", out="cut", anchor=pos("US", 0, 3.9, -4.6), dist=16.5, yaw=6, pitch=0, zoom=-5, pan=(-10, 0))
for k in range(3): show(s, 0.05 + 0.25 * k, "n%d" % k, pos("US", -2.15 + 2.15 * k, 0.3, -4.6))
sp, ct = rel(s, "spreads"), rel(s, "whole country")
for k, (px, py) in enumerate(PINS): show(s, sp + (ct - sp + 0.2) * k / len(PINS), "p%d" % k, pos("US", (px / 1800 - 0.5) * 6.4, 3.2 + (1 - py / 1100) * 3.91 - 0.05, -4.7))
tag(s, ct, "coast", 0.37)
s = S("So retailers", out="cut", anchor=pos("MR", -0.8, 1.5, -1.8), dist=5.2, yaw=18, pitch=4, zoom=10, pan=(-9, 0))
act(s, 0.0, "shopM", face="sneaky", pose=dict(armR=-120)); sw = rel(s, "switch"); tag(s, sw, "bulb", 0.12, -0.27, 0.4, wf=0.12); tag(s, rel(s, "tactics"), "tactic", 0.33)
s = S("If you can't", out="cut", anchor=pos("MR", -0.8, 1.45, -1.8), dist=4.6, yaw=-10, pitch=8, zoom=6, pan=(8, 2))
act(s, 0.0, "shopM", face="smug", pose=dict(armR=0)); sg_ = tag(s, 0.05, "bfsign", 0.22); c_ = rel(s, "change")
act(s, c_, sg_, shake=0.5); act(s, c_, "shopM", face="sneaky", pose=dict(armR=-150)); tag(s, c_, "change", 0.38, wf=0.32)

# ---- 21-25 the 1980s: the red-to-black story ... it just isn't true
s = S("In the 1980s", out="cut", anchor=pos("EI", -0.3, 1.9, -2.6), dist=8, yaw=-12, pitch=6, zoom=8, pan=(9, 0))
act(s, 0.0, "exec", face="happy", pose=dict(armR=-150, armL=150), shake=0.3); tag(s, 0.1, "y1980", 0.28)
s = S("Stores lose money", out="cut", anchor=pos("EI", 0.7, 1.4, -2.8), dist=7.8, yaw=14, pitch=4, zoom=-6, pan=(-9, 0))
act(s, 0.0, "exec", face="nervous", pose=dict(armR=-80, armL=0)); act(s, rel(s, "red"), "ledger", shake=0.4); tag(s, rel(s, "red"), "inred", 0.31)
s = S("and this is the day", out="cut", anchor=pos("EI", 1.35, 1.45, -3.2), dist=4.6, yaw=-10, pitch=6, zoom=5, pan=(9, 0))
bl = rel(s, "into the black"); act(s, bl, "ledger", face="black", shake=0.5); tag(s, bl, "inblack", 0.33); act(s, bl, "exec", face="happy", pose=dict(armR=-150, armL=150))
s = S("Sounds perfect", out="cut", anchor=pos("EI", -0.3, 1.45, -2.4), dist=5, yaw=16, pitch=6, zoom=10, pan=(-9, 0))
act(s, 0.0, "exec", face="smug", pose=dict(armR=-150, armL=150)); tag(s, 0.05, "perfect", 0.32); tag(s, 0.2, "sparkle", 0.12, 0.27, 0.5, wf=0.1)
s = S("It just isn't", out="cut", anchor=pos("EI", 0.4, 1.6, -2.8), dist=6.4, yaw=-14, pitch=4, zoom=12, pan=(8, 2))
n_ = rel(s, "isn't"); act(s, 0.0, "exec", face="smug"); act(s, n_, "exec", face="shocked", pose=dict(armR=0, armL=0), shake=0.5); act(s, n_, "ledger", shake=0.5)
tag(s, n_, "myth", 0.13, -0.04, 0.6, wf=0.24, tilt=-12)

# ---- 26-28 today: the cops' insult on every sale sign ... and nobody tells you why
s = S("Today", out="cut", anchor=pos("TD", 0.1, 1.6, -2.6), dist=8.6, yaw=12, pitch=6, zoom=8, pan=(-10, 0))
for cid, x, z in (("teen", -0.55, -1.9), ("kidT", 0.75, -1.7), ("dadT", 1.15, -3.2)): show(s, 0.0, cid, pos("TD", x, 0.06, z), hop=0); act(s, 0.0, cid, pose=dict(armR=-150, armL=150), shake=0.3)
act(s, 0.0, "clerk", face="happy", pose=dict(armR=-150, armL=150)); tag(s, 0.05, "today", 0.3)
s = S("print the", out="cut", anchor=pos("TD", 0.2, 1.5, -3.4), dist=5.6, yaw=-14, pitch=6, zoom=10, pan=(9, 0))
for cid, x in (("teen", -4.6), ("kidT", 4.4), ("dadT", 5.2), ("bagsT", -5.2), ("bagsT2", 5.8)): show(s, 0.0, cid, pos("TD", x, 0.06, -1.5), hop=0)
act(s, 0.0, "clerk", face="happy", pose=dict(armR=-150, armL=0)); tag(s, 0.05, "salebig", 0.3, wf=0.28); tag(s, rel(s, "insult"), "insult", 0.15, tilt=-6)
s = S("And not one", out="cut", anchor=pos("TD", 0.2, 1.4, -3.6), dist=4.8, yaw=14, pitch=4, zoom=12, pan=(-8, 2))
act(s, 0.0, "clerk", face="sneaky", pose=dict(armR=-60, armL=0)); tag(s, rel(s, "tell"), "shh", 0.12, 0.25, 0.5, wf=0.13); tag(s, rel(s, "will"), "why", 0.12, -0.26, 0.5, wf=0.1)
s = S("why", **HOOK); hook_state(s)
for s in shots:
    if "anchor" in s: s.setdefault("frameY", 0.0)

# ---- every card / temporary character leaves one frame before the next shot
starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots):
    if k + 1 < len(shots):
        for cid in s["_tags"]: hide(s, round(starts[k + 1] - starts[k] - 0.04, 3), cid)
    s.pop("_tags")

# ================================================================== SPEC
mood = lambda m, ph: {"t": round(say(ph), 3), "mood": m, "fade": 0.02}
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6,
    "moods": {"day": {"sun": {"azimuth": 40, "elevation": 46, "color": "#ffe8c8", "intensity": 2.4},
                      "sky": {"top": "#5b8ee0", "horizon": "#f6d6b0"}, "fill": {"sky": "#a0b4ff", "ground": "#6a4b6e", "intensity": 1.2}},
              "neon": {"sun": {"azimuth": 30, "elevation": 50, "color": "#ffd6f0", "intensity": 2.3},
                       "sky": {"top": "#5a3aa0", "horizon": "#ff8ad0"}, "fill": {"sky": "#b8a8ff", "ground": "#8a4a8e", "intensity": 1.3}}},
    "lighting": [{"t": 0, "mood": "day"}, mood("neon", "In the 1980s"), mood("day", "Today")],
    "ground": {"texture": TEX + "asphalt.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(named="It was named", furious="furious", philly="Philadelphia", thx="Thanksgiving", flood="flood", sat="Then on Saturday", army="armynavy",
           ball="football", tour="tourists", grid="Gridlock", crowds="Crowds", chaos="Chaos", nocop="No traffic cop", twelve="twelvehour", police="So the police",
           dark="dark name", bf2="Black Friday#2", hate="Stores hate it", same="That same year", big="Big Friday", nobody="Nobody says", yousee="You see",
           refuse="refuses", slowly="Slowly", spreads="spreads", country="whole country", retail="So retailers", switch="switch", cant="If you can't",
           change="change", e80="In the 1980s", red="red", day80="and this is the day", black="into the black", perfect="Sounds perfect", isnt="isn't",
           today="Today", insult="insult", notone="And not one", tell="tell", loop="why")
cues = {k: say(v) for k, v in CUE.items()}; cues["end"] = DURATION
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
    if s["_dur"] < 0.7: print("   ! very short shot")
keys = {}
for k, s in enumerate(shots):
    for a in s["actions"]:
        if a["at"] < 0: print("   ! S%02d negative action time %.2f: %s" % (k, a["at"], a["who"]))
        if "to" in a: keys.setdefault(a["who"], []).append((starts[k] + a["at"], a["over"], k, a["to"]))
        if a["at"] > s["_dur"] + 0.25: print("   ! S%02d action at %.2f s runs past the shot (%.2f s): %s %s" % (k, a["at"], s["_dur"], a["who"], list(a)[2:]))
for who, ks in keys.items():
    ks.sort()
    for (t0, ov, k0, _), (t1, ov1, k1, _) in zip(ks, ks[1:]):
        if t0 + ov > t1 + 0.06: print("   ! %s: move from S%02d (%.2f+%.2f s) overlaps next move in S%02d at %.2f s" % (who, k0, t0, ov, k1, t1))
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
