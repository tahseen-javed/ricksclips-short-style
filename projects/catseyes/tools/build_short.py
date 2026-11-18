#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 08: Cat's Eyes Cunningham and the carrot lie.
usage: build_short.py <project folder>
Eleven sets 70 units apart: AF night airfield (hook + loop), SK Blitz London at night, NS sandbagged newsagent street,
KT RAF mess, RD radar fuselage, PR poster wall, FM carrot farm, OP optician, LB library, GR German HQ, TD kitchen of today.
Every shot has a camera move (dolly + orbit); the hook frame keeps John head-to-feet and every card inside the frame (pull-out).
Cards are sized from the shot distance and leave one frame before the next shot.  A frame check projects every visible
character and card at the start, middle and end of each shot and prints CUT lines for anything crossing the frame edge."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(AF=0, SK=70, NS=140, KT=210, RD=280, PR=350, FM=420, OP=490, LB=560, GR=630, TD=700)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK
ASP = json.load(open(os.path.join(P, "aspect.json")))


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


def room(loc, wallc, img, floor, rep=(4, 4), sidec=None):     # interior: floor, back wall + picture, two side walls
    box(loc, 0, 0, -1, [12, 0.06, 10], texture=floor, repeat=list(rep)); box(loc, 0, 0, -5, [12, 6.2, 0.3], color=wallc)
    for sg in (-1, 1): box(loc, sg * 5.85, 0, -1, [0.3, 6.2, 10], color=sidec or wallc)
    plane(loc, img, 0, 0.06, -4.82, 11, 5.04)


# ================================================================== SETS
# AF night airfield: concrete apron, 604 Squadron hangar, runway lights, sandbags, windsock post
plane("AF", "skynight.png", 0, -1, -30, 96, 42); box("AF", 0, 0, -4, [40, 0.05, 26], texture="concrete.jpg", repeat=[10, 7])
box("AF", 0, 0, -14, [16, 7.5, 6], color="#b8bcaa"); box("AF", 0, 7.5, -14, [16.4, 0.5, 6.4], color="#5a6070"); plane("AF", "hangar.png", 0, 0.05, -10.94, 14, 6.42)
for x in range(-15, 16, 3): box("AF", x, 0.05, 3.4, [0.3, 0.22, 0.3], color="#ffe27a")
for x in (-8.5, 8.5): box("AF", x, 0, -6.0, [3.0, 0.9, 1.2], color="#d6c496")
post("AF", 10.5, -7, 4.0, "#e8e0d0")
# SK Blitz London: street, terraced houses with taped windows, lamp posts, sandbags, night skyline
plane("SK", "skynight.png", 0, -1, -30, 96, 42); box("SK", 0, 0, -3, [40, 0.05, 24], texture="asphalt.jpg", repeat=[8, 6])
for k, x in enumerate(range(-15, 16, 5)):
    house("SK", x, -11, [4.8, 4.4 + (k % 3) * 0.8, 5], ("#5a4a6a", "#6a4a3a", "#3a4a5a")[k % 3], color=("#c9a0a0", "#d8c0a0", "#a8b8c8")[k % 3])
    windows("SK", -8.5, (x - 1.2, x + 1.2), 1.2)
for x in (-6, 0, 6): post("SK", x, -6.5, 3.2, "#33405a")
box("SK", -3, 0, -7, [3, 0.8, 1], color="#d6c496"); box("SK", 4, 0, -7, [3, 0.8, 1], color="#d6c496")
# NS newsagent street (day): pavement, brick shopfront with taped windows, lamp posts
plane("NS", "skyday.png", 0, -1, -30, 96, 42); box("NS", 0, 0, -5.25, [34, 0.15, 2.6], color="#d4ccbe")
box("NS", 0, 0, -9, [14, 6.4, 5], color="#b25c48"); box("NS", 0, 6.4, -9, [14.4, 0.4, 5.4], color="#6a4a3a"); plane("NS", "street40.png", 0, 0.15, -6.44, 13, 5.96)
for x in (-9, 9): house("NS", x, -9.5, [4.6, 5.0, 5], "#5a4a5a", color="#c8b090")
for x in (-6.6, 6.6): post("NS", x, -4.4, 3.4, "#33405a")
# KT RAF mess: green tiles, two-tone wall with menu + bunting, a long table at the back
room("KT", "#f4eace", "messwall.png", "tiles.jpg", sidec="#e8dcc0")
box("KT", 0, 0, -3.3, [3.2, 0.75, 1.0], color="#a0644a"); box("KT", 0, 0.75, -3.3, [3.3, 0.06, 1.1], color="#e8d6b0")
# RD inside the night fighter: ribs, portholes, an olive console for the radar set
room("RD", "#9ec4b2", "radarwall.png", "wood.jpg", sidec="#8fb6a4"); box("RD", 0.7, 0, -4.0, [2.4, 0.8, 0.9], color="#5c6a4c")
# PR poster wall street (day)
plane("PR", "skyday.png", 0, -1, -30, 96, 42); box("PR", 0, 0, -4.5, [34, 0.15, 3.0], color="#d4ccbe")
box("PR", 0, 0, -6.2, [15, 6.2, 0.4], color="#c46c54"); plane("PR", "posterwall.png", 0, 0.15, -5.98, 13, 5.96)
for x in (-8.5, 8.5): house("PR", x, -9, [4.8, 5.4, 5], "#3a4a5a", color="#d8c0a0")
# FM carrot farm: grass, red barn, fence
plane("FM", "skyday.png", 0, -1, -30, 96, 42); box("FM", 0, 0, -3, [40, 0.05, 24], texture="grass.jpg", repeat=[8, 6])
house("FM", -8, -12, [6, 5, 5], "#7a3a30", color="#c8483c"); house("FM", 8, -13, [5, 4, 5], "#5a4a3a", color="#e8d0a0")
for x in range(-12, 13, 2): post("FM", x, -7.5, 1.0, "#a07050")
box("FM", 0, 0.6, -7.5, [24, 0.12, 0.08], color="#c09060")
room("OP", "#c4deee", "eyewall.png", "ofloor.jpg")
room("LB", "#8a5a3a", "libwall.png", "wood.jpg", sidec="#7a4e32")
room("GR", "#9ea696", "gerwall.png", "concrete.jpg", sidec="#8e9686")
room("TD", "#faf4e8", "kitchen.png", "kfloor.jpg", sidec="#eee6d6")

SIGNS = []                                                   # (name, world corners) of text painted on set pictures


def sign(nm, loc, plane_, rect, W=2400, Hh=1100):
    (x, y, z, pw, ph), (a, b, c, d) = plane_, rect; X0 = base.X[loc] + x
    SIGNS.append((nm, [[X0 + (u / W - 0.5) * pw, y + ph * (1 - v / Hh), z + 0.02] for u in (a, c) for v in (b, d)]))


NSP, KTP, PRP, ROOMP = (0, 0.15, -6.44, 13, 5.96), (0, 0.06, -4.82, 11, 5.04), (0, 0.15, -5.98, 13, 5.96), (0, 0.06, -4.82, 11, 5.04)
sign("newsagent", "NS", NSP, (560, 120, 1480, 290)); sign("bill1", "NS", NSP, (960, 470, 1180, 720)); sign("bill2", "NS", NSP, (1220, 470, 1440, 720))
sign("menu", "KT", KTP, (900, 320, 1500, 840))
for k, x0 in enumerate((40, 900, 1760)): sign("poster%d" % k, "PR", PRP, (x0, 140, x0 + 610, 960))
sign("chart", "OP", ROOMP, (1000, 300, 1400, 860)); sign("diploma", "OP", ROOMP, (180, 220, 600, 520))
sign("calendar", "TD", ROOMP, (1020, 440, 1340, 720)); sign("map", "GR", ROOMP, (900, 200, 1500, 680))

# ================================================================== CHARACTERS
JOHN0 = pos("AF", -0.9, 0.06, 0.0)
human("john", "john", JOHN0, face="confused"); put("beauP", "beau", pos("AF", -2.4, 0.05, -9.6), 2.0)
put("radarA", "radar", PARK, 1.0); put("carrotA", "carrot", PARK, 1.1)
for k in range(2): put("b%d" % k, "bomber", PARK, 1.0)
put("beauF", "beauf", PARK, 1.0)
human("newsboy", "newsboy", pos("NS", -0.5, 0.15, -4.6), face="shouting", h=1.3); human("reader", "reader", pos("NS", 0.95, 0.15, -4.9), face="happy", h=1.75)
human("johnK", "john", pos("KT", -0.3, 0.06, -1.6), face="sneaky"); COOK0 = pos("KT", 1.3, 0.06, -2.0); human("cook", "cook", COOK0, face="happy")
put("carrotK", "carrot", PARK, 1.0); put("pileK", "pile", PARK, 0.9)
human("jimmy", "jimmy", pos("RD", -0.5, 0.06, -2.8), face="happy"); put("radarR", "radar", pos("RD", 0.7, 0.86, -4.1), 1.1)
human("minR", "minister", PARK, face="sneaky")
human("minP", "minister", pos("PR", -0.6, 0.15, -4.4), face="happy"); put("drC", "drcarrot", PARK, 1.5); human("minN", "minister", PARK, face="happy")
put("pileF", "pile", pos("FM", 0.6, 0.05, -5.2), 2.0); human("farmer", "farmer", pos("FM", -1.5, 0.06, -3.6), face="happy")
human("doctor", "doctor", pos("OP", -0.6, 0.06, -2.4), face="neutral"); put("carrotO", "carrot", pos("OP", 0.45, 0.06, -2.2), 1.0, face="happy")
human("historian", "historian", pos("LB", 0.0, 0.06, -2.6), face="happy")
human("german", "german", pos("GR", -0.5, 0.06, -2.6), face="smug")
human("mom", "mom", pos("TD", -0.6, 0.06, -2.4), face="happy"); human("max", "max", pos("TD", 0.35, 0.06, -2.1), face="happy", h=1.25)
put("carrotT", "carrot", PARK, 0.95)

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}
N_ = [0]


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):               # a card at a safe spot of the frame, never near an edge
    (ax, ay, az), d = s["anchor"], s["distance"]; y = math.radians(s["yaw"]); w = dx * 0.41 * d
    show(s, at, who, [round(ax + w * math.cos(y) + dz * math.sin(y), 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az - w * math.sin(y) + dz * math.cos(y), 3)], hop=0.12)


REQ = []


def tag(s, at, name, dy=0.25, dx=0.0, dz=0.3, wf=0.24, hf=0.17, tilt=0, face="default"):   # placed later by the card fit
    N_[0] += 1; cid = "%s_%d" % (name, N_[0]); c = dict(id=cid, puppet="puppets/" + name, pos=PARK, height=0.1, face=face)
    if tilt: c["pose"] = dict(head=tilt)
    chars.append(c); s["_tags"].append(cid); REQ.append((s, at, cid, name, dy, dx, dz, wf, hf, c)); return cid


def temp(s, *who): s["_tags"].extend(who)


def S(start, **kw):
    s = shot(start, **kw); s["_tags"] = []; s["glide"] = "dolly"; s["pan"] = [v * 5 for v in s["pan"]]; return s


def hook_state(s):
    show(s, 0.0, "john", JOHN0, hop=0); act(s, 0.0, "john", face="confused", pose=dict(armR=-80, armL=80))
    tag(s, 0.0, "qmark", 0.1, 0.24, 0.5, wf=0.07); return tag(s, 0.0, "bestpilot", 0.31, 0.0, 0.4, wf=0.3)


HOOK = dict(anchor=pos("AF", -0.9, 1.5, 0.0), dist=6.6, yaw=8, pitch=6, zoom=-5, pan=(6, 0))
# ---- 0-2 hook: the best night pilot can't see in the dark -> a machine could -> the carrot takes the credit
s = S("0", out="cut", **HOOK); hook_state(s); c_ = rel(s, "couldn't")
act(s, c_, "john", face="shocked", pose=dict(armR=-150, armL=150), shake=0.35); tag(s, c_, "cantsee", 0.18, -0.02, 0.55, wf=0.2, tilt=-9)
s = S("A machine could", out="cut", anchor=pos("AF", -0.3, 1.3, 0.2), dist=6.8, yaw=-24, pitch=4, zoom=8, pan=(-2, 0))
show(s, 0.0, "radarA", pos("AF", 0.4, 0.06, 0.35)); act(s, 0.0, "radarA", face="wow", shake=0.3); temp(s, "radarA")
act(s, 0.0, "john", face="shocked", pose=dict(armR=-95, armL=0)); tag(s, 0.05, "machine", 0.32); tag(s, 0.2, "sparkle", 0.1, 0.22, 0.6, wf=0.08)
s = S("and a carrot", out="cut", anchor=pos("AF", -1.5, 1.25, 0.3), dist=6.8, yaw=7, pitch=6, zoom=8, pan=(2, 0))
show(s, 0.0, "carrotA", pos("AF", -2.1, 0.06, 0.55)); act(s, 0.0, "john", face="confused", pose=dict(armR=0, armL=0)); temp(s, "carrotA")
cr = rel(s, "credit"); act(s, cr, "carrotA", face="happy", shake=0.35); act(s, cr, "john", face="shocked", shake=0.3); tag(s, cr, "credit", 0.32)
tag(s, cr, "sparkle", 0.1, -0.24, 0.6, wf=0.08)

# ---- 3-5 1940, the Blitz: bombers every night, one pilot keeps finding them
s = S("It's 1940", out="cut", anchor=pos("SK", 0, 3.9, -4.5), dist=15, yaw=-8, pitch=-4, zoom=7, pan=(-10, 0))
dur = rel(s, "German bombers")
show(s, 0.0, "b0", pos("SK", -1.6, 5.3, -7.5), hop=0); go(s, 0.02, "b0", pos("SK", 0.0, 5.6, -7.5), dur - 0.1, walk=False)
show(s, 0.0, "b1", pos("SK", 0.6, 6.9, -9.5), hop=0); go(s, 0.02, "b1", pos("SK", 2.2, 7.1, -9.5), dur - 0.1, walk=False)
tag(s, 0.05, "y1940", 0.3, wf=0.2); bl = rel(s, "Blitz"); tag(s, bl, "blitz", 0.08, 0.0, 0.5, wf=0.22, tilt=-8)
for dx in (-0.26, 0.26): tag(s, bl, "boom", -0.1, dx, 0.6, wf=0.1)
s = S("German bombers", out="cut", anchor=pos("SK", 0.4, 5.4, -7.5), dist=10, yaw=12, pitch=-8, zoom=8, pan=(-9, 0))
show(s, 0.0, "b0", pos("SK", -0.1, 4.9, -7.5), hop=0); go(s, 0.02, "b0", pos("SK", 0.7, 5.1, -7.5), rel(s, "One pilot keeps") - 0.1, walk=False)
show(s, 0.0, "b1", PARK, hop=0); en = rel(s, "every night"); tag(s, en, "everynight", 0.33); tag(s, en, "boom", -0.12, -0.25, 0.6, wf=0.1)
s = S("One pilot keeps", out="cut", anchor=pos("SK", 0.0, 5.5, -7.5), dist=13, yaw=-10, pitch=-6, zoom=5, pan=(-5, 0))
show(s, 0.0, "beauF", pos("SK", -1.0, 5.2, -7.0), hop=0); go(s, 0.02, "beauF", pos("SK", -0.25, 5.4, -7.0), rel(s, "John Cunningham") - 0.1, walk=False)
show(s, 0.0, "b0", pos("SK", 1.2, 5.9, -8.5), hop=0); temp(s, "beauF", "b0"); an = rel(s, "anyway")
act(s, an, "b0", face="shock", shake=0.4); tag(s, an, "found", 0.32, tilt=-6)

# ---- 6-7 John Cunningham, twenty kills, nineteen in pitch black
s = S("John Cunningham", out="cut", anchor=pos("AF", -0.9, 1.5, 0.0), dist=5.6, yaw=9, pitch=4, zoom=10, pan=(-9, 0))
act(s, 0.0, "john", face="happy", pose=dict(armR=-150, armL=150), shake=0.3); nm = tag(s, 0.05, "name", 0.31, wf=0.26); tag(s, 0.3, "sparkle", 0.12, 0.24, 0.6, wf=0.08)
tw = rel(s, "Twenty kills"); hide(s, tw - 0.03, nm); s["_tags"].remove(nm); tag(s, tw, "k20", 0.3, wf=0.15); act(s, tw, "john", face="smug", pose=dict(armR=-120, armL=0), shake=0.3)
act(s, tw, "beauP", face="tally")
s = S("nineteen", out="cut", anchor=pos("AF", -1.5, 1.6, -2.0), dist=9, yaw=10, pitch=6, zoom=8, pan=(-9, 0))
act(s, 0.0, "john", face="smug", pose=dict(armR=-120, armL=0)); tag(s, 0.0, "k20", 0.3, -0.12, wf=0.15); tag(s, 0.05, "k19", 0.12, 0.1, 0.5, wf=0.2)

# ---- 8-11 the papers: CAT'S EYES; his secret? carrots, lots of carrots
s = S("The papers call", out="cut", anchor=pos("NS", 0.2, 1.45, -4.7), dist=7.2, yaw=10, pitch=6, zoom=8, pan=(-9, 0))
act(s, 0.0, "newsboy", face="shouting", pose=dict(armR=-150, armL=0), shake=0.3); ce = rel(s, "Cat's")
tag(s, ce, "paper", 0.17, 0.0, 0.5, wf=0.2, hf=0.3); tag(s, ce, "catseyes", 0.38, wf=0.22); act(s, ce, "reader", face="shocked", pose=dict(armR=-150), shake=0.3)
s = S("His secret", out="cut", anchor=pos("KT", -0.2, 1.4, -1.6), dist=5.6, yaw=-4, pitch=4, zoom=9, pan=(0, 0))
act(s, 0.0, "johnK", face="sneaky", pose=dict(armR=-120, armL=0)); tag(s, 0.05, "secret", 0.31); tag(s, 0.1, "qmark", 0.1, 0.24, 0.5, wf=0.07)
show(s, 0.0, "cook", PARK, hop=0); cz = rel(s, "Carrots"); show(s, cz, "carrotK", pos("KT", 0.3, 0.06, -1.4)); act(s, cz, "carrotK", face="happy", shake=0.3)
act(s, cz, "johnK", face="happy", pose=dict(armR=-150, armL=150)); cs = tag(s, cz, "carrots", 0.12, 0.0, 0.5, tilt=8, wf=0.2)
lo = rel(s, "Lots of carrots"); hide(s, lo - 0.03, cs); s["_tags"].remove(cs); tag(s, lo, "lots", 0.12, 0.0, 0.5, wf=0.26)
show(s, lo, "pileK", pos("KT", 0.0, 0.81, -3.3)); act(s, lo, "johnK", face="shocked", shake=0.4); temp(s, "carrotK")

# ---- 12-14 the real secret: a radar hidden inside his plane; the enemy must not learn
s = S("You see", out="cut", anchor=pos("RD", 0.1, 1.5, -3.1), dist=6.8, yaw=-12, pitch=6, zoom=7, pan=(9, 0))
act(s, 0.0, "jimmy", face="happy", pose=dict(armR=-95)); tag(s, 0.05, "realsecret", 0.34, wf=0.26); ra = rel(s, "radar")
act(s, ra, "radarR", face="wow", shake=0.4); act(s, ra, "jimmy", face="shocked"); tag(s, ra, "radart", 0.19, 0.0, 0.6, wf=0.18)
s = S("hidden inside", out="cut", anchor=pos("AF", -2.4, 1.3, -9.6), dist=14, yaw=6, pitch=4, zoom=7, pan=(-3, 0))
show(s, 0.0, "john", PARK, hop=0); act(s, 0.0, "beauP", face="xray", shake=0.3); tag(s, 0.15, "sparkle", 0.12, 0.0, 0.5, wf=0.07)
s = S("Britain could not", out="cut", anchor=pos("RD", -1.15, 1.5, -2.6), dist=7.6, yaw=14, pitch=4, zoom=7, pan=(3, 0))
show(s, 0.0, "radarR", PARK, hop=0); show(s, 0.0, "minR", pos("RD", -1.8, 0.06, -2.4)); act(s, 0.0, "minR", face="sneaky", pose=dict(armR=-60)); act(s, 0.0, "jimmy", face="nervous")
tag(s, 0.1, "shh", 0.12, -0.24, 0.6, wf=0.11); temp(s, "minR"); tag(s, rel(s, "enemy"), "topsecret", 0.32, tilt=-8)

# ---- 15-19 the carrot story everywhere: posters, Doctor Carrot, carrot fudge, 100,000 tons
s = S("So the carrot story", out="cut", anchor=pos("PR", 0.0, 2.4, -4.6), dist=9, yaw=-6, pitch=6, zoom=7, pan=(4, 0))
act(s, 0.0, "minP", face="happy", pose=dict(armR=-150, armL=150), shake=0.3); st_ = tag(s, 0.05, "story", 0.37); tag(s, rel(s, "everywhere"), "everywhere", 0.13, tilt=-6, wf=0.22)
po = rel(s, "Posters"); hide(s, po - 0.03, st_); s["_tags"].remove(st_); tag(s, po, "posters", 0.37, wf=0.2); act(s, po, "minP", face="smug", pose=dict(armR=-95, armL=0))
s = S("A mascot called", out="cut", anchor=pos("NS", -0.05, 1.35, -4.6), dist=7.2, yaw=0, pitch=4, zoom=7, pan=(0, 0))
for cid in ("newsboy", "reader"): show(s, 0.0, cid, PARK, hop=0)
show(s, 0.0, "minN", pos("NS", -0.6, 0.15, -4.6), hop=0); show(s, 0.0, "drC", pos("NS", 0.45, 0.15, -4.5)); temp(s, "drC", "minN")
act(s, 0.0, "minN", face="happy", pose=dict(armR=-95, armL=0))
dc = rel(s, "Doctor"); act(s, dc, "drC", shake=0.4); dn = tag(s, dc, "drname", 0.33)
fz = rel(s, "Carrot fudge"); hide(s, fz - 0.03, dn); s["_tags"].remove(dn); tag(s, fz, "fudget", 0.33); tag(s, fz, "fudge", 0.04, -0.2, 0.6, wf=0.2, hf=0.13)
act(s, fz, "minN", face="shocked", shake=0.3)
s = S("By 1942", out="cut", anchor=pos("FM", 0.3, 2.0, -4.0), dist=12, yaw=8, pitch=6, zoom=-5, pan=(6, 0))
act(s, 0.05, "pileF", shake=0.4); tag(s, 0.05, "y1942", 0.31, wf=0.18); ht = rel(s, "hundred thousand")
act(s, ht, "farmer", face="shocked", pose=dict(armR=-150, armL=150), shake=0.4); tag(s, ht, "tons", 0.15, wf=0.24)

# ---- 20-22 the truth: no night vision; historians: the Germans never fell for it
s = S("But carrots don't", out="cut", anchor=pos("OP", -0.1, 1.4, -2.3), dist=6.8, yaw=-12, pitch=4, zoom=10, pan=(3, 0))
act(s, 0.0, "doctor", face="smug", pose=dict(armR=-120, armL=0)); nv = rel(s, "night vision")
act(s, nv, "carrotO", face="shocked", shake=0.4); act(s, nv, "doctor", face="shouting", shake=0.3); tag(s, nv, "nonv", 0.32, tilt=-6)
s = S("And historians say", out="cut", anchor=pos("LB", 0.0, 1.45, -2.6), dist=5.2, yaw=12, pitch=4, zoom=10, pan=(-9, 0))
act(s, 0.0, "historian", face="happy", pose=dict(armR=-150, armL=0)); tag(s, 0.05, "historians", 0.33)
s = S("the Germans probably", out="cut", anchor=pos("GR", -0.4, 1.95, -2.6), dist=6.8, yaw=-12, pitch=4, zoom=8, pan=(5, 0))
act(s, 0.0, "german", face="smug", pose=dict(armR=-80)); tag(s, 0.05, "paper", -0.02, 0.21, 0.6, wf=0.12, hf=0.14); nf = rel(s, "never")
act(s, nf, "german", face="happy", pose=dict(armR=-150, armL=150), shake=0.4); tag(s, nf, "never", 0.33, tilt=-7, wf=0.26)

# ---- 23-25 today: it fooled us; 80+ years later we still believe it
s = S("The only people", out="cut", anchor=pos("TD", 0.2, 1.3, -2.3), dist=7.4, yaw=12, pitch=6, zoom=8, pan=(2, 0))
act(s, 0.0, "mom", face="happy", pose=dict(armR=-95)); act(s, 0.0, "max", face="happy"); show(s, 0.0, "carrotT", pos("TD", 0.8, 0.06, -2.2))
us = rel(s, "us"); tag(s, us, "fooled", 0.33); act(s, us, "mom", face="shocked", shake=0.3)
s = S("More than eighty", out="cut", anchor=pos("TD", 0.2, 1.15, -2.2), dist=5.8, yaw=8, pitch=6, zoom=8, pan=(0, 0))
act(s, 0.0, "max", face="happy", pose=dict(armR=-150), shake=0.3); show(s, 0.0, "mom", PARK, hop=0); act(s, 0.0, "carrotT", face="default", shake=0.3); tag(s, 0.05, "y80", 0.33, wf=0.17)
s = S("we still believe", out="cut", anchor=pos("TD", 0.15, 1.3, -2.3), dist=7.2, yaw=10, pitch=6, zoom=-6, pan=(-8, 0))
show(s, 0.0, "mom", pos("TD", -0.6, 0.06, -2.4), hop=0)
for cid in ("mom", "max", "carrotT"): act(s, 0.0, cid, shake=0.35)
act(s, 0.0, "mom", face="happy", pose=dict(armR=-150, armL=150)); act(s, 0.0, "max", face="happy", pose=dict(armR=-150, armL=150))
tag(s, 0.05, "believe", 0.33, tilt=-5, wf=0.26)
s = S("Because Britain's", **HOOK); hook_state(s); act(s, 0.0, "beauP", face="default")
for cid in ("radarA", "carrotA"): show(s, 0.0, cid, PARK, hop=0)
for s in shots:
    if "anchor" in s: s.setdefault("frameY", 0.0)

starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots): s["_dur"] = (starts[k + 1] if k + 1 < len(shots) else DURATION) - starts[k]


def drift_t(dur, tl):                                        # stage.js driftTable: the camera arrives fast, then settles
    n = max(2, int(round(dur * 30))); acc = 0.0; f = tl * 30
    for i in range(1, n):
        if i > f: break
        u = (i + 0.5) / n; ss = min(1, max(0, (u - 0.15) / 0.25)); ss = ss * ss * (3 - 2 * ss); acc += (1 + 0.7 * (1 - ss)) / 30
    return acc


# ---- fit every card into the safe box (x 7-87 %, y 7-64 %, above the captions) for its whole time on screen, zoom + pan included
for (s, at, cid, name, dy, dx, dz, wf, hf, c) in REQ:
    d = s["distance"]; h = min(wf * d / ASP[name], hf * 0.728 * d); samples = [at + (s["_dur"] - at) * u for u in (0, 0.25, 0.5, 0.75, 1.0)]
    for it in range(60):
        hfr, wfr, ok = h / (0.728 * d), h * ASP[name] / (0.41 * d), True
        for tl in samples:
            te = drift_t(s["_dur"], tl); sc = math.exp(math.log1p(s["zoom"] / 100) * te); px, py = s["pan"][0] * te / 1080, s["pan"][1] * te / 1920
            xc, yc = 0.5 + dx * sc + px, 0.5 - dy * sc + py
            if xc - wfr * sc / 2 < 0.10 or xc + wfr * sc / 2 > 0.85 or yc - hfr * sc / 2 < 0.08 or yc + hfr * sc / 2 > 0.63: ok = False; break
        if ok: break
        dx += (-0.03 - dx) * 0.15; dy += (0.15 - dy) * 0.15; h *= 0.97
    c["height"] = round(h, 3); SH[cid] = c["height"]; card(s, at, cid, dy, dx, dz)

# ---- every card / temporary character leaves one frame before the next shot
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
              "night": {"sun": {"azimuth": 220, "elevation": 42, "color": "#d4dcff", "intensity": 2.1},
                        "sky": {"top": "#2c3a80", "horizon": "#8a7ad0"}, "fill": {"sky": "#a4b0ff", "ground": "#5a4a7e", "intensity": 1.3}}},
    "lighting": [{"t": 0, "mood": "night"}, mood("day", "The papers call"), mood("night", "You see"), mood("day", "So the carrot story"), mood("night", "Because Britain's")],
    "ground": {"texture": TEX + "asphalt.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(couldnt="couldn't", machine="A machine could", carrot="and a carrot", credit="credit", y1940="It's 1940", blitz="Blitz", bombers="German bombers",
           night="every night", pilot="One pilot keeps", anyway="anyway", john="John Cunningham", kills="Twenty kills", nineteen="nineteen", papers="The papers call",
           cats="Cat's", secret="His secret", carrots="Carrots", lots="Lots of carrots", yousee="You see", radar="radar", hidden="hidden inside",
           britain="Britain could not", enemy="enemy", story="So the carrot story", everywhere="everywhere", posters="Posters", mascot="A mascot called",
           doctor="Doctor", fudge="Carrot fudge", y1942="By 1942", tons="hundred thousand", but="But carrots don't", vision="night vision",
           hist="And historians say", germans="the Germans probably", never="never", only="The only people", us="us", eighty="More than eighty",
           believe="we still believe", loop="Because Britain's", dark="dark#2")
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

# ---- frame check: project every visible character / card (engine camera maths, dolly glide) at 3 moments per shot
W_, H_, T0 = 1080, 1920, math.tan(math.radians(20))
ASPH = 0.46
def norm(v): l = math.sqrt(sum(c * c for c in v)); return [c / l for c in v]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cam(s, tl):
    te = drift_t(s["_dur"], tl); y, p = math.radians(s["yaw"]), math.radians(s["pitch"]); dr = [math.sin(y) * math.cos(p), math.sin(p), math.cos(y) * math.cos(p)]
    fwd = [-c for c in dr]; right = norm(cross(fwd, [0, 1, 0])); up = cross(right, fwd)
    sc = math.exp(math.log1p(s["zoom"] / 100) * te); d = s["distance"] / sc; wpp = 2 * d * T0 / H_
    dx, dy = s["pan"][0] * te, s["pan"][1] * te
    look = [a - r * dx * wpp + u_ * dy * wpp for a, r, u_ in zip(s["anchor"], right, up)]
    return [l + c * d for l, c in zip(look, dr)], fwd, right, up
def proj(c, P_):
    pos_, f, r, u = c; v = [a - b for a, b in zip(P_, pos_)]; z = dot(v, f)
    if z <= 0.1: return None
    return 0.5 + dot(v, r) / (z * T0 * W_ / H_) / 2, 0.5 - dot(v, u) / (z * T0) / 2
track = {c["id"]: [(-1.0, c["pos"])] for c in chars}
for k, s in enumerate(shots):
    for a in s["actions"]:
        if "to" in a: track[a["who"]].append((starts[k] + a["at"] + a.get("over", 0) * 0.5, a["to"]))
for v in track.values(): v.sort(key=lambda e: e[0])
WID = {c["id"]: c["height"] * (ASP.get(c["puppet"].split("/")[1], ASPH)) for c in chars}
flags = 0
for k, s in enumerate(shots):
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        c = cam(s, tl); T = starts[k] + tl
        for cid, tr in track.items():
            p0 = [e for e in tr if e[0] <= T][-1][1]
            if p0[1] < -50: continue
            h, w = SH[cid], WID[cid]; pts = [proj(c, [p0[0] + sx * w / 2, p0[1] + sy * h, p0[2]]) for sx in (-1, 1) for sy in (0, 1)]
            if any(q is None for q in pts): continue
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            inside = max(xs) > 0 and min(xs) < 1 and max(ys) > 0 and min(ys) < 1
            if inside and (min(xs) < 0.03 or max(xs) > 0.97 or min(ys) < 0.03 or max(ys) > 0.985):
                flags += 1; print("   CUT S%02d t=%.2f %-14s x %.2f..%.2f y %.2f..%.2f" % (k, tl, cid, min(xs), max(xs), min(ys), max(ys)))
for k, s in enumerate(shots):
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        c = cam(s, tl)
        for nm, corners in SIGNS:
            pts = [proj(c, q) for q in corners]
            if any(q is None for q in pts): continue
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            if max(xs) > 0.01 and min(xs) < 0.99 and max(ys) > 0.01 and min(ys) < 0.99 and (min(xs) < 0.01 or max(xs) > 0.99 or min(ys) < 0.01 or max(ys) > 0.99):
                flags += 1; print("   SIGNCUT S%02d t=%.2f %-10s x %.2f..%.2f y %.2f..%.2f" % (k, tl, nm, min(xs), max(xs), min(ys), max(ys)))
BOXES = []                                                   # engine CAMERA_INSIDE_PROP: AABB (+0.12) of every house (with its rotated cone roof) / box
for pr in props:
    if pr["type"] not in ("house", "box", "crate", "wall"): continue
    (x, y, z), (w, h, d) = pr["pos"], pr["size"]
    if pr["type"] == "house": r = max(w, d) * 0.78 * 1.4143; BOXES.append((pr, x - max(w / 2, r), y, z - max(d / 2, r), x + max(w / 2, r), y + h * 1.6, z + max(d / 2, r)))
    else: BOXES.append((pr, x - w / 2, y, z - d / 2, x + w / 2, y + h, z + d / 2))
for k, s in enumerate(shots):
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        cp = cam(s, tl)[0]
        for pr, x0, y0, z0, x1, y1, z1 in BOXES:
            if x0 - 0.12 <= cp[0] <= x1 + 0.12 and y0 - 0.12 <= cp[1] <= y1 + 0.12 and z0 - 0.12 <= cp[2] <= z1 + 0.12:
                flags += 1; print("   INSIDE S%02d t=%.2f %s@%s" % (k, tl, pr["type"], pr["pos"]))
print("frame check: %d CUT flags" % flags)
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
