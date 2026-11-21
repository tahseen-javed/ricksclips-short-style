#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 14: Mars Climate Orbiter - NASA's math was perfect, the units were not.
usage: build_short.py <project folder>
Thirteen sets 70 units apart: CR night control room (hook + loop), SP deep space + giant Mars, LP launch pad at dawn, TR the cruise,
CB chalkboard office, NV amber navigation room, MT dusk meeting, MA Mars arrival, BN the burn, DS dish at night, UN split room
(Lockheed orange | NASA blue), LB desk with the missing label, QN sunny classroom.  Every shot moves (crane / push-in / pull-out);
same-set shots fly (dolly glide), new sets dissolve.  Snap-ins, atmosphere, depth of field, comic fx, a counter cutaway for 4.45.
Cards are fitted to the safe box; the frame check prints CUT / SIGNCUT / INSIDE / OVERLAP flags."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(CR=0, SP=70, LP=140, TR=210, CB=280, NV=350, MT=420, MA=490, BN=560, DS=630, UN=700, LB=770, QN=840)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK
ASP = json.load(open(os.path.join(P, "aspect.json")))


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):                                          # the first match at or after the shot start (repeated words!)
    t0 = 0.0 if s["start"] == 0 else say(s["_phrase"]); k = 1
    while True:
        t = say("%s#%d" % (phrase, k))
        if t >= t0 - 0.01: return round(t - t0, 3)
        k += 1


def room(loc, wallc, img, floor, rep=(4, 4), sidec=None):
    box(loc, 0, 0, -1, [12, 0.06, 10], texture=floor, repeat=list(rep)); box(loc, 0, 0, -5, [12, 6.2, 0.3], color=wallc)
    for sg in (-1, 1): box(loc, sg * 5.85, 0, -1, [0.3, 6.2, 10], color=sidec or wallc)
    plane(loc, img, 0, 0.06, -4.82, 11, 5.04)


SIGNS = []


def sign(nm, loc, plane_, rect, W=2400, Hh=1100):
    (x, y, z, pw, ph), (a, b, c, d) = plane_, rect; X0 = base.X[loc] + x
    SIGNS.append((nm, [[X0 + (u / W - 0.5) * pw, y + ph * (1 - v / Hh), z + 0.02] for u in (a, c) for v in (b, d)]))


# ================================================================== SETS
def yard(loc, img, floor, w=16, rep=(8, 8)):
    plane(loc, img, 0, -0.2, -6.5, w, round(w * 1100 / 2400, 3)); box(loc, 0, 0, -1, [w, 0.04, 12], texture=floor, repeat=list(rep))


def lamp(loc, x, z, h, col, cap):
    post(loc, x, z, h, col); box(loc, x, h, z, [0.36, 0.36, 0.36], color=cap)


def desk(loc, x, z, w=1.6, col="#3a4660", mon=None):
    box(loc, x, 0.04, z, [w, 0.74, 0.7], color=col)
    if mon: box(loc, x, 0.78, z - 0.12, [0.62, 0.44, 0.08], color=mon)


def rock(loc, x, y, z, s, col): box(loc, x, y, z, [s, s * 0.7, s * 0.9], color=col)


yard("CR", "ctrl.png", "navtile.jpg"); desk("CR", -3.2, -2.6, mon="#1a2a48"); desk("CR", 3.2, -2.8, mon="#1a2a48"); desk("CR", 0.45, -1.7, 1.0); lamp("CR", 2.4, -3.8, 1.6, "#2a3040", "#ffb050")
yard("SP", "space.png", "starfloor.jpg")
for x, y, z, s in ((-3.2, 1.6, -3.4, 0.5), (3.4, 2.4, -4.0, 0.4), (-2.0, 3.0, -4.6, 0.3), (2.6, 0.9, -2.4, 0.35)): rock("SP", x, y, z, s, "#6a5a7a")
yard("LP", "launch.png", "pad.jpg"); crate("LP", -3.0, 0.04, -2.6, 0.6); crate("LP", -3.4, 0.04, -3.3, 0.5); barrel("LP", 3.0, -2.4); barrel("LP", 3.4, -3.0)
yard("TR", "trip.png", "starfloor2.jpg")
for x, y, z, s in ((-3.0, 2.2, -3.6, 0.4), (3.2, 1.4, -3.0, 0.5), (2.2, 3.2, -4.4, 0.3)): rock("TR", x, y, z, s, "#4a7a8a")
yard("CB", "board.png", "wood.jpg"); desk("CB", 1.1, -1.7, 1.6, "#a87050")
yard("NV", "radarbg.png", "darktile.jpg"); desk("NV", 1.2, -1.9, 1.4, "#4a4038"); desk("NV", -3.0, -3.0, 1.4, "#4a4038", "#2a2018")
yard("MT", "meet.png", "carpet.jpg"); box("MT", 0.0, 0.04, -3.6, [3.2, 0.72, 1.0], color="#8a6a5a")
yard("MA", "arrive.png", "redsand.jpg")
for x, z, s in ((-3.0, -2.6, 0.6), (3.2, -3.2, 0.5), (-1.6, -4.0, 0.4), (2.0, -1.8, 0.3)): rock("MA", x, 0.04, z, s, "#b05a3a")
yard("BN", "burn.png", "redsand2.jpg")
for x, z, s in ((-3.0, -2.4, 0.6), (3.0, -2.8, 0.7), (1.8, -4.0, 0.4)): rock("BN", x, 0.04, z, s, "#7a3020")
yard("DS", "dishes.png", "nightsand.jpg")
for x in (-3.4, -2.6, -1.8): post("DS", x, -3.6, 0.8, "#4a3a50")
yard("UN", "units.png", "checker.jpg"); desk("UN", -2.4, -2.6, 1.6, "#c07030", "#3a2a20"); desk("UN", 2.4, -2.6, 1.6, "#3060b0", "#1a2a48")
yard("LB", "deskbg.png", "deskwood.jpg"); box("LB", 0.0, 0.04, -2.1, [2.6, 0.8, 1.0], color="#8a5a3a"); box("LB", -0.9, 0.84, -2.2, [0.36, 0.4, 0.36], color="#e05a4a")
yard("QN", "school.png", "schoolwood.jpg")
for x, z in ((-3.0, -3.0), (3.0, -3.2), (-2.0, -4.2), (2.2, -4.4)): box("QN", x, 0.04, z, [1.0, 0.7, 0.6], color="#e0a060")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
NP = pos("CR", -0.75, 0.04, -1.3)
human("nav", "nav", NP, face="shocked"); put("clip", "clip", pos("CR", 0.45, 0.78, -1.6), 0.8)
put("orbS", "orbiter", pos("SP", 0.2, 0.9, -2.6), 1.3, face="shocked")
put("rocket", "rocket", pos("LP", 0.8, 0.04, -3.0), 3.4); human("bossL", "boss", pos("LP", -0.7, 0.04, -2.8), face="happy")
put("orbT", "orbiter", pos("TR", -0.4, 1.4, -2.8), 1.1)
human("navB", "nav", pos("CB", -0.6, 0.04, -2.0), face="happy"); put("orbM", "orbiter", pos("CB", 0.75, 0.78, -1.75), 0.55); put("calc", "calc", pos("CB", 1.5, 0.78, -1.6), 0.55)
human("navN", "nav", pos("NV", -1.15, 0.04, -2.0), face="nervous"); human("nav2N", "nav2", pos("NV", -0.65, 0.04, -2.5), face="confused"); put("radar", "radar", pos("NV", 1.0, 0.78, -1.9), 0.95)
human("navM", "nav", pos("MT", -0.8, 0.04, -2.0), face="shouting"); human("bossM", "boss", pos("MT", 0.7, 0.04, -2.4), face="smug")
put("orbA", "orbiter", pos("MA", -0.8, 1.1, -3.0), 1.1)
put("orbB", "orbiter", pos("BN", 0.2, 1.7, -3.0), 1.4, face="burn")
put("dish", "dish", pos("DS", 0.6, 0.04, -3.2), 2.0); human("navD", "nav2", pos("DS", -0.8, 0.04, -1.8), face="nervous")
human("lockU", "lock", pos("UN", -1.1, 0.04, -1.8), face="happy"); human("navU", "nav", pos("UN", 1.1, 0.04, -1.8), face="happy")
put("sheet", "sheet", pos("LB", 0.25, 0.84, -2.0), 1.0); human("navL", "nav", pos("LB", 1.55, 0.04, -1.5), face="neutral")
human("bossQ", "boss", pos("QN", 1.0, 0.04, -2.0), face="smug"); put("paper", "test100", pos("QN", 0.45, 1.0, -1.9), 0.6); human("navQ", "nav", pos("QN", -0.8, 0.04, -1.6), face="confused")

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}
N_ = [0]; REQ = []; SNAPC = []; FXC = []; LOC = {}


def ease(s, tl): u = min(1.0, max(0.0, tl / s["_dur"])); return 1 - (1 - u) ** 2      # stage.js arc easing
def yaw_at(s, tl): return s["yaw"] + (s.get("yawTo", s["yaw"]) - s["yaw"]) * ease(s, tl)
def pitch_at(s, tl): return s["pitch"] + (s.get("pitchTo", s["pitch"]) - s["pitch"]) * ease(s, tl)


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):
    (ax, ay, az), d = s["anchor"], s["distance"]; y = math.radians(yaw_at(s, at)); w = dx * 0.41 * d
    p_ = [round(ax + w * math.cos(y) + dz * math.sin(y), 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az - w * math.sin(y) + dz * math.cos(y), 3)]
    if at <= 0.001 and s is shots[0]: next(c for c in chars if c["id"] == who)["pos"] = p_    # HOOK LAW: the hook sign is already up at frame 0
    show(s, at, who, p_, hop=0 if (at <= 0.001 and s is shots[0]) else 0.12)


def tag(s, at, name, dy=0.25, dx=0.0, dz=0.3, wf=0.24, hf=0.17, tilt=0):
    N_[0] += 1; cid = "%s_%d" % (name, N_[0]); c = dict(id=cid, puppet="puppets/" + name, pos=PARK, height=0.1, face="default")
    if tilt: c["pose"] = dict(head=tilt)
    chars.append(c); s["_tags"].append(cid); REQ.append((s, at, cid, name, dy, dx, dz, wf, hf, c)); return cid


def S(start, loc, anchor, dist, yaw, pitch=4, zoom=8, pan=(0, 0), **kw):
    s = shot(start, anchor=pos(loc, *anchor), dist=dist, yaw=yaw, pitch=pitch, zoom=zoom, pan=pan)
    s["_tags"] = []; s["pan"] = [v * 5 for v in s["pan"]]; s["out"] = "dissolve"; s["outDur"] = 0.4; s["glide"] = "dolly"; s.update(kw); LOC[id(s)] = loc; return s


def crane(start, loc, anchor, dist, yaw0, yaw1, p0=30, p1=6, **kw):        # 3D crane: from high above, swinging round and down to eye level
    return S(start, loc, anchor, dist, yaw0, pitch=p0, zoom=8, yawTo=yaw1, pitchTo=p1, **kw)


def ft(s, who, seq): s.setdefault("_ft", []).append((who, seq))
def snap(s, t, z=25): SNAPC.append((s, t, z))
def cfx(s, t, typ, on, dur=0.9): FXC.append((s, t, typ, on, dur))


HOOK = dict(anchor=(-0.2, 1.3, -1.4), dist=8.0, yaw=-6, pitch=8)
# ---- 0-2 hook: NASA's math was perfect.
s = S("0", "CR", zoom=7, pan=(-3, 0), **HOOK); ft(s, "nav", ["shocked", "shouting", "shocked"]); act(s, 0.0, "nav", pose=dict(armR=-150)); act(s, 0.1, "clip", shake=0.3)
tag(s, 0.0, "perfect", 0.3, 0.0, wf=0.6, hf=0.2); snap(s, max(0.82, rel(s, "perfect")), 12)
# ---- That's exactly how they lost a 125 million dollar spacecraft at Mars.
s = crane("That's exactly", "SP", (0.2, 1.7, -2.6), 9.0, 24, 4, 26, 8); act(s, 0.0, "orbS", shake=0.4); tag(s, rel(s, "lost"), "lost", 0.31, wf=0.52)
s = S("125", "SP", (0.2, 1.95, -2.6), 6.4, -10, pitch=4, yawTo=2, type="macro", dof=dict(focus="orbS", blur=0.5)); act(s, 0.0, "orbS", shake=0.3); tag(s, 0.05, "m125", 0.3, wf=0.5)
# ---- December 11, 1998. Mars Climate Orbiter launches on a nine-month trip.
s = crane("December", "LP", (0.2, 2.0, -3.0), 10.0, -24, -2, 36, 6); tag(s, 0.05, "date1", 0.2, -0.12, wf=0.32, hf=0.34); ft(s, "bossL", ["happy", "smug"])
s = S("Mars Climate", "LP", (0.4, 2.0, -3.0), 9.6, 12, pitch=4, zoom=3, yawTo=4); act(s, 0.0, "rocket", face="fire", shake=0.4); go(s, 0.2, "rocket", pos("LP", 0.8, 0.29, -3.0), 1.4, walk=False)
act(s, 0.0, "bossL", pose=dict(armR=-150, armL=150)); ft(s, "bossL", ["shouting", "happy"]); tag(s, 0.05, "mco", 0.35, wf=0.6, hf=0.13); snap(s, rel(s, "launches"), 14)
s = crane("on a", "TR", (0.0, 1.95, -2.8), 6.8, 20, 0, 24, 6); go(s, 0.0, "orbT", pos("TR", 0.15, 1.4, -2.8), 1.6, walk=False); tag(s, 0.05, "trip", 0.32, wf=0.55)
# ---- Every engine burn is calculated to the decimal.
s = crane("Every engine", "CB", (0.2, 1.4, -1.9), 8.0, -20, 2, 34, 6); ft(s, "navB", ["happy", "smug"]); tag(s, 0.05, "burnc", 0.31, wf=0.56)
s = S("calculated", "CB", (1.05, 1.3, -1.65), 4.4, -8, pitch=6, yawTo=4, type="macro", dof=dict(focus="calc", blur=0.5)); tag(s, 0.05, "decimal", 0.3, wf=0.6)
# ---- But the navigators keep seeing its path drift lower.
s = crane("But the navigators", "NV", (0.2, 1.5, -2.1), 9.4, 22, 2, 36, 6); ft(s, "navN", ["nervous", "confused"]); ft(s, "nav2N", ["confused", "nervous"]); cfx(s, 0.5, "sweat", "navN", 0.8)
s = S("its path", "NV", (1.0, 1.6, -1.9), 4.2, -10, pitch=4, yawTo=2, type="macro", dof=dict(focus="radar", blur=0.5)); tag(s, 0.05, "drift", 0.3, wf=0.6); snap(s, rel(s, "drift"), 12)
# ---- They raise concerns. Nobody fixes it.
s = crane("They raise", "MT", (0.0, 1.4, -2.2), 8.0, -18, 2, 32, 6); act(s, 0.0, "navM", pose=dict(armR=-150)); ft(s, "navM", ["shouting", "nervous"]); ft(s, "bossM", ["smug", "sneaky"]); tag(s, 0.05, "concerns", 0.32, wf=0.58)
s = S("Nobody fixes", "MT", (0.7, 1.55, -2.4), 4.9, 12, pitch=5, zoom=12, dof=dict(focus="bossM", blur=0.4)); ft(s, "bossM", ["smug", "happy", "smug"]); tag(s, 0.05, "nobody", 0.32, wf=0.6, hf=0.14)
# ---- September 23, 1999. The orbiter should pass high above the Martian air.
s = crane("September", "MA", (0.0, 2.0, -3.0), 9.5, 22, 0, 40, 8); tag(s, 0.05, "date2", 0.2, 0.15, wf=0.32, hf=0.34); go(s, 0.0, "orbA", pos("MA", -0.3, 1.2, -3.0), 1.4, walk=False)
s = S("The orbiter should", "MA", (-0.2, 1.9, -3.0), 6.8, -12, pitch=6, zoom=10, pan=(3, 0)); tag(s, 0.05, "high", 0.31, wf=0.56)
# ---- Instead, it drops to under 40 miles. Contact is lost. It never calls home again.
s = S("Instead", "BN", (0.15, 1.9, -3.0), 9.0, 10, pitch=10, yawTo=-6, pitchTo=4); act(s, 0.0, "orbB", shake=0.5); go(s, 0.1, "orbB", pos("BN", 0.0, 0.7, -3.0), 1.3, walk=False)
tag(s, 0.05, "miles40", 0.32, wf=0.5); snap(s, rel(s, "40"), 14); cfx(s, rel(s, "drops"), "speed", "orbB", 0.8)
s = crane("Contact is", "DS", (0.0, 1.6, -2.5), 9.5, -20, 2, 34, 6); tag(s, 0.05, "contact", 0.32, wf=0.55); ft(s, "navD", ["nervous", "shocked"]); act(s, 0.2, "dish", face="sad")
s = S("It never", "DS", (-0.8, 1.55, -1.8), 5.0, 10, pitch=5, zoom=12, dof=dict(focus="navD", blur=0.4), _dis=1); hide(s, 0.0, "dish"); ft(s, "navD", ["nervous", "confused", "nervous"])
tag(s, 0.05, "never", 0.32, wf=0.6, hf=0.14); cfx(s, 0.3, "sweat", "navD", 0.8)
# ---- You see, the numbers were never wrong. The units were.
s = crane("You see the", "UN", (0.0, 1.5, -1.9), 9.5, 18, 0, 38, 6, _dis=1); show(s, 0.0, "dish", pos("DS", 0.6, 0.04, -3.2), hop=0); ft(s, "lockU", ["happy", "smug"]); ft(s, "navU", ["smug", "happy"]); tag(s, 0.05, "numbers", 0.32, wf=0.58)
s = S("The units", "UN", (1.1, 1.55, -1.8), 5.0, -8, pitch=5, zoom=12, dof=dict(focus="navU", blur=0.4)); ft(s, "navU", ["shocked", "shouting"]); tag(s, 0.05, "units", 0.32, wf=0.6, hf=0.14); snap(s, 0.3, 12); cfx(s, 0.4, "bang", "navU", 0.6)
# ---- Lockheed Martin's software reported thrust in pounds. NASA's software read it as newtons.
s = S("Lockheed Martin's", "UN", (-1.1, 1.5, -1.9), 5.6, -14, pitch=5, zoom=10, pan=(3, 0)); ft(s, "lockU", ["happy", "smug"]); tag(s, 0.05, "pounds", 0.31, wf=0.58)
s = S("NASA's software", "UN", (1.1, 1.5, -1.9), 5.6, 14, pitch=5, zoom=10, pan=(-3, 0)); ft(s, "navU", ["happy", "confused"]); tag(s, 0.05, "newtons", 0.31, wf=0.58)
# ---- Every push was off by a factor of 4.45.
s = S("Every push", "UN", (0.0, 2.0, -1.9), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="OFF BY A FACTOR OF", items=["4.45"]))
# ---- One missing label, unnoticed for nine months.
s = S("One missing", "LB", (0.25, 1.38, -2.0), 4.0, -10, pitch=4, yawTo=2, type="macro", dof=dict(focus="sheet", blur=0.5)); tag(s, 0.05, "label", 0.3, wf=0.6); snap(s, rel(s, "label"), 12)
s = crane("unnoticed", "LB", (0.55, 1.4, -1.9), 8.6, 20, 0, 36, 6); ft(s, "navL", ["neutral", "sneaky"]); cfx(s, 0.3, "z", "navL", 1.0); tag(s, 0.05, "months9", 0.32, wf=0.56)
# ---- So when someone tells you their math is perfect, ask one question. Perfect in what units?
s = crane("So when", "QN", (0.1, 1.5, -1.8), 9.0, -20, 2, 34, 6); ft(s, "bossQ", ["smug", "happy"]); ft(s, "navQ", ["confused", "neutral"]); act(s, 0.1, "paper", shake=0.3); tag(s, 0.05, "mathperf", 0.32, wf=0.6)
s = S("ask one", "QN", (-0.8, 1.55, -1.6), 4.9, 10, pitch=5, zoom=12, dof=dict(focus="navQ", blur=0.4)); ft(s, "navQ", ["confused", "smug"]); tag(s, 0.05, "askone", 0.32, wf=0.6, hf=0.14)
s = S("Perfect in", "QN", (0.1, 1.5, -1.8), 8.6, -6, pitch=5, zoom=12); ft(s, "navQ", ["smug", "happy"]); ft(s, "bossQ", ["shocked", "nervous"]); tag(s, 0.05, "whatunits", 0.31, wf=0.55); snap(s, 0.25, 14); cfx(s, 0.5, "blush", "bossQ")
# ---- Because NASA's math was perfect. (pull-out onto the hook frame)
s = S("Because NASA's", "CR", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "nav", ["shocked", "shouting", "shocked"]); show(s, 0.0, "nav", NP, hop=0)
act(s, 0.0, "clip", shake=0.4); act(s, 0.0, "nav", pose=dict(armR=-150)); tag(s, 0.05, "perfect", 0.3, 0.0, wf=0.6, hf=0.2)

for s in shots: s.setdefault("frameY", 0.0)

starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots): s["_dur"] = (starts[k + 1] if k + 1 < len(shots) else DURATION) - starts[k]; s["start"] = round(starts[k], 3)
for k, s in enumerate(shots[:-1]):                          # same set: the camera flies (dolly glide) into the next shot; new set: dissolve
    if LOC[id(s)] == LOC[id(shots[k + 1])] and s.get("type") != "cutaway" and shots[k + 1].get("type") != "cutaway" and not shots[k + 1].get("_dis"): s["out"] = "glide"; s["outDur"] = 0.5
for s in shots:                                              # short shots: enough pan that the move is clearly visible (>= 3.6 % of the width)
    if abs(s["zoom"]) * s["_dur"] < 8.5 and abs(s["pan"][0]) * s["_dur"] < 39: s["pan"][0] = round(math.copysign(39 / s["_dur"], s["pan"][0] or 1), 1)


def drift_t(dur, tl):                                        # stage.js driftTable: the camera arrives fast, then settles
    n = max(2, int(round(dur * 30))); acc = 0.0; f = tl * 30
    for i in range(1, n):
        if i > f: break
        u = (i + 0.5) / n; ss = min(1, max(0, (u - 0.15) / 0.25)); ss = ss * ss * (3 - 2 * ss); acc += (1 + 0.7 * (1 - ss)) / 30
    return acc


# ---- the last shot pulls out and lands exactly on the hook frame
L = shots[-1]; L["distance"] = round(HOOK["dist"] * math.exp(math.log1p(L["zoom"] / 100) * drift_t(L["_dur"], L["_dur"])), 3)

# ---- snap-ins: 3-9 s apart, the first one inside 0.8-2.5 s, none in the last shot
last = -9.0
for s, t, z in SNAPC:
    T = starts[shots.index(s)] + t
    if T - last >= 3.0 and s is not L: s["snap"] = dict(t=round(t, 3), zoom=z, dur=0.28); last = T
SN = [x for x in shots if x.get("snap")]; T_ = lambda x: starts[shots.index(x)] + x["snap"]["t"]
while len(SN) > max(1, round(12 * DURATION / 60)):            # at most 12 per 60 s: drop the snap whose neighbours stay closest (gap <= 9 s)
    best = min(range(1, len(SN) - 1), key=lambda i: T_(SN[i + 1]) - T_(SN[i - 1])); SN.pop(best)["snap"] = None
for x in shots:
    if "snap" in x and not x["snap"]: x.pop("snap")
# ---- comic fx: one at a time, at least 3 s apart, none before 2 s
FX, last = [], -9.0
for s, t, typ, on, dur in FXC:
    T = starts[shots.index(s)] + t
    end_ = starts[shots.index(s)] + s["_dur"] - 0.1
    if T >= 2.0 and T - last >= 3.0 and end_ - T >= 0.4: FX.append(dict(type=typ, on=on, t=round(T, 3), dur=round(min(dur, end_ - T), 2))); last = T
# ---- face tracks: a new face every 0.55 s, never the same twice in a row
for s in shots:
    for who, seq in s.pop("_ft", []):
        n = max(1, int((s["_dur"] - 0.3) / 0.55) + 1)
        prev, j = None, 0
        for i in range(n):
            while seq[j % len(seq)] == prev: j += 1
            prev = seq[j % len(seq)]; j += 1; act(s, round(i * 0.55, 3), who, face=prev)
# ---- atmosphere by set: dust + rays by day, bokeh by night / dawn
D_ = lambda c=22: dict(count=c, size=1.0, drift=1.0); BK = lambda a=0.3: dict(count=12, size=1.0, alpha=a)
ATM = dict(CR=dict(bokeh=BK(0.35)), SP=dict(bokeh=BK(0.4)), LP=dict(dust=D_(20), rays=dict(angle=28, intensity=0.55)), TR=dict(bokeh=BK(0.35)),
           CB=dict(dust=D_(24), rays=dict(angle=32, intensity=0.55)), NV=dict(bokeh=BK(0.3)), MT=dict(dust=D_(16), rays=dict(angle=24, intensity=0.4)), MA=dict(bokeh=BK(0.3)),
           BN=dict(dust=D_(30), rays=dict(angle=40, intensity=0.5)), DS=dict(bokeh=BK(0.4)), UN=dict(dust=D_(18)), LB=dict(dust=D_(24), rays=dict(angle=30, intensity=0.5)),
           QN=dict(dust=D_(22), rays=dict(angle=35, intensity=0.6)))
for s in shots:
    if s.get("type") != "cutaway": s["atmos"] = ATM[LOC[id(s)]]

# ---- every card / temporary character leaves one frame before the next shot
for k, s in enumerate(shots):
    if k + 1 < len(shots):
        for cid in s["_tags"]: hide(s, round(starts[k + 1] - starts[k] - 0.04, 3), cid)
    s.pop("_tags")

# ---- camera maths (engine): drift + snap punch
W_, H_, T0, ASPH = 1080, 1920, math.tan(math.radians(20)), 0.46
def snapf(s, tl):
    v = s.get("snap"); u = tl - v["t"] if v else -1
    if not v or not (0 < u < v["dur"]): return 1.0
    r = min(0.12, v["dur"] * 0.45); e = 1 - (1 - u / r) ** 3 if u < r else 0.5 * (1 + math.cos(math.pi * (u - r) / (v["dur"] - r)))
    return 1 + min(v["zoom"], 35) / 100 * e
def scale(s, tl): return math.exp(math.log1p(s["zoom"] / 100) * drift_t(s["_dur"], tl)) * snapf(s, tl)
def norm(v): l = math.sqrt(sum(c * c for c in v)); return [c / l for c in v]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cam(s, tl):
    te = drift_t(s["_dur"], tl); y, p = math.radians(yaw_at(s, tl)), math.radians(pitch_at(s, tl)); dr = [math.sin(y) * math.cos(p), math.sin(p), math.cos(y) * math.cos(p)]
    fwd = [-c for c in dr]; right = norm(cross(fwd, [0, 1, 0])); up = cross(right, fwd)
    d = s["distance"] / scale(s, tl); wpp = 2 * d * T0 / H_; dx, dy = s["pan"][0] * te, s["pan"][1] * te
    look = [a - r * dx * wpp + u_ * dy * wpp for a, r, u_ in zip(s["anchor"], right, up)]
    return [l + c * d for l, c in zip(look, dr)], fwd, right, up
def proj(c, P_):
    pos_, f, r, u = c; v = [a - b for a, b in zip(P_, pos_)]; z = dot(v, f)
    if z <= 0.1: return None
    return 0.5 + dot(v, r) / (z * T0 * W_ / H_) / 2, 0.5 - dot(v, u) / (z * T0) / 2
def moments(s):
    m = [0.05, s["_dur"] * 0.25, s["_dur"] * 0.5, s["_dur"] * 0.75, s["_dur"] - 0.05]
    if s.get("snap"): m.append(s["snap"]["t"] + 0.12)
    return m
def partial(pts, lo=0.03, hi=0.97, bot=0.985):
    if any(q is None for q in pts): return False
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return max(xs) > 0.01 and min(xs) < 0.99 and max(ys) > 0.01 and min(ys) < 0.99 and (min(xs) < lo or max(xs) > hi or min(ys) < lo or max(ys) > bot)
track = {c["id"]: [(-1.0, c["pos"])] for c in chars}
for k, s in enumerate(shots):
    for a_ in s["actions"]:
        if "to" in a_: track[a_["who"]].append((starts[k] + a_["at"] + a_.get("over", 0) * 0.5, a_["to"]))
for v in track.values(): v.sort(key=lambda e: e[0])
WID = {c["id"]: c["height"] * (ASP.get(c["puppet"].split("/")[1], ASPH)) for c in chars}
def shot_cuts(k, s, report=False):
    n = 0
    if s.get("type") == "cutaway": return 0
    for tl in moments(s):
        c = cam(s, tl); T = starts[k] + tl
        for cid, tr in track.items():
            if "_" in cid: continue                           # cards are fitted separately
            p0 = [e for e in tr if e[0] <= T][-1][1]
            if p0[1] < -50: continue
            h, w = SH[cid], WID[cid]; pts = [proj(c, [p0[0] + sx * w / 2, p0[1] + sy * h, p0[2]]) for sx in (-1, 1) for sy in (0, 1)]
            if partial(pts):
                n += 1
                if report: print("   CUT S%02d t=%.2f %-10s x %.2f..%.2f y %.2f..%.2f" % (k, tl, cid, min(q[0] for q in pts), max(q[0] for q in pts), min(q[1] for q in pts), max(q[1] for q in pts)))
        for nm, corners in SIGNS:
            pts = [proj(c, q) for q in corners]
            if partial(pts, 0.01, 0.99, 0.99):
                n += 1
                if report: print("   SIGNCUT S%02d t=%.2f %s" % (k, tl, nm))
    return n
# ---- camera auto-fit: widen a shot (x1.06 per step, at most x1.35) until nothing is cut
for k, s in enumerate(shots[:-1]):
    d0 = s["distance"]
    while os.environ.get("NOFIT") != "1" and shot_cuts(k, s) and s["distance"] < d0 * 1.35: s["distance"] = round(s["distance"] * 1.06, 3)
    if s["distance"] != d0: print("   autofit S%02d distance %.1f -> %.1f" % (k, d0, s["distance"]))

# ---- fit every card into the safe box (x 10-85 %, y 8-63 %) for its whole time on screen, drift + pan + snap peak included
RECT = {}
for (s, at, cid, name, dy, dx, dz, wf, hf, c) in REQ:
    d = s["distance"]; h = min(wf * d / ASP[name], hf * 0.728 * d); samples = [at + (s["_dur"] - at) * u for u in (0, 0.25, 0.5, 0.75, 1.0)]
    if s.get("snap") and s["snap"]["t"] + 0.12 > at: samples.append(s["snap"]["t"] + 0.12)
    for it in range(60):
        hfr, wfr, ok = h / (0.728 * d), h * ASP[name] / (0.41 * d), True
        for tl in samples:
            te = drift_t(s["_dur"], tl); sc = scale(s, tl); px, py = s["pan"][0] * te / 1080, s["pan"][1] * te / 1920
            xc, yc = 0.5 + dx * sc + px, 0.5 - dy * sc + py
            if xc - wfr * sc / 2 < 0.10 or xc + wfr * sc / 2 > 0.85 or yc - hfr * sc / 2 < 0.08 or yc + hfr * sc / 2 > 0.63: ok = False; break
        if ok: break
        dx *= 0.97; dy *= 0.97; h *= 0.97                  # shrink the whole card layout towards the centre: cards never slide onto each other
    c["height"] = round(h, 3); SH[cid] = c["height"]; card(s, at, cid, dy, dx, dz); RECT[cid] = (s, at, 0.5 + dx - wfr / 2, 0.5 - dy - hfr / 2, 0.5 + dx + wfr / 2, 0.5 - dy + hfr / 2)

# ================================================================== SPEC
MOOD = dict(CR="ctrl", SP="space", LP="dawn", TR="cruise", CB="office", NV="amber", MT="dusk", MA="arrive", BN="burn", DS="moon", UN="split", LB="sepia", QN="sunny")
light, cur = [{"t": 0, "mood": "ctrl"}], "ctrl"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 14,
    "moods": {"ctrl": {"sun": {"azimuth": -30, "elevation": 25, "color": "#ffc890", "intensity": 1.9}, "sky": {"top": "#0a1430", "horizon": "#2a4070"}, "fill": {"sky": "#6080d0", "ground": "#202840", "intensity": 1.6}}, "space": {"sun": {"azimuth": 60, "elevation": 30, "color": "#ffe0c0", "intensity": 2.6}, "sky": {"top": "#2a1450", "horizon": "#8a3a9a"}, "fill": {"sky": "#c090ff", "ground": "#604060", "intensity": 1.9}}, "dawn": {"sun": {"azimuth": 40, "elevation": 15, "color": "#ffd0b0", "intensity": 2.3}, "sky": {"top": "#f08cb0", "horizon": "#ffe0a0"}, "fill": {"sky": "#ffc0d0", "ground": "#706060", "intensity": 1.35}}, "cruise": {"sun": {"azimuth": -40, "elevation": 35, "color": "#e0fff8", "intensity": 2.2}, "sky": {"top": "#08303e", "horizon": "#20808a"}, "fill": {"sky": "#80e0e0", "ground": "#205050", "intensity": 1.5}}, "office": {"sun": {"azimuth": 50, "elevation": 45, "color": "#fff4e0", "intensity": 2.4}, "sky": {"top": "#fff0d0", "horizon": "#ffe6b8"}, "fill": {"sky": "#fff0d0", "ground": "#806040", "intensity": 1.3}}, "amber": {"sun": {"azimuth": 0, "elevation": 40, "color": "#ffc070", "intensity": 2.6}, "sky": {"top": "#2a1a0c", "horizon": "#704424"}, "fill": {"sky": "#ffc080", "ground": "#504030", "intensity": 1.9}}, "dusk": {"sun": {"azimuth": 200, "elevation": 20, "color": "#ffc890", "intensity": 2.2}, "sky": {"top": "#463282", "horizon": "#ffaa6e"}, "fill": {"sky": "#c0a0ff", "ground": "#504070", "intensity": 1.5}}, "arrive": {"sun": {"azimuth": 30, "elevation": 30, "color": "#ffd0a0", "intensity": 2.3}, "sky": {"top": "#08041e", "horizon": "#2e164c"}, "fill": {"sky": "#90c0ff", "ground": "#603020", "intensity": 1.5}}, "burn": {"sun": {"azimuth": -20, "elevation": 30, "color": "#ff9050", "intensity": 2.5}, "sky": {"top": "#460a0e", "horizon": "#ff7832"}, "fill": {"sky": "#ff9060", "ground": "#502010", "intensity": 1.4}}, "moon": {"sun": {"azimuth": 150, "elevation": 35, "color": "#c0d0ff", "intensity": 2.0}, "sky": {"top": "#081036", "horizon": "#32508c"}, "fill": {"sky": "#8090ff", "ground": "#303050", "intensity": 1.6}}, "split": {"sun": {"azimuth": 0, "elevation": 50, "color": "#fff8f0", "intensity": 2.4}, "sky": {"top": "#ffd0a0", "horizon": "#a0c8ff"}, "fill": {"sky": "#ffffff", "ground": "#606070", "intensity": 1.3}}, "sepia": {"sun": {"azimuth": 60, "elevation": 35, "color": "#ffe0b0", "intensity": 2.3}, "sky": {"top": "#ecd8b2", "horizon": "#d6b88c"}, "fill": {"sky": "#ffe0c0", "ground": "#806050", "intensity": 1.3}}, "sunny": {"sun": {"azimuth": 40, "elevation": 50, "color": "#fffae0", "intensity": 2.5}, "sky": {"top": "#ffe0a0", "horizon": "#fff4d0"}, "fill": {"sky": "#fff4c0", "ground": "#a08050", "intensity": 1.3}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff9a3c", "paper": ["#dcc49a", "#c9a878"], "dofPx": 8, "particle": "#ffe6b0", "bokehColor": "#a0c8ff", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(perf1="perfect", lost="That's exactly", m125="125", dec="December", launch="launches", trip="on a", every="Every engine", decimal="decimal", nav="But the navigators",
           drift="drift", concerns="They raise", nobody="Nobody fixes", sep="September", should="The orbiter should", instead="Instead", miles="40", contact="Contact is",
           never="It never", yousee="You see the", units="The units", lock="Lockheed Martin's", nasa="NASA's software", push="Every push", label="One missing",
           unnoticed="unnoticed", sowhen="So when", ask="ask one", perfin="Perfect in", because="Because NASA's", perfect2="perfect#4")
cues = {k: say(v) for k, v in CUE.items()}; cues["end"] = DURATION
cp, wav = os.path.join(P, "audio", "cues.json"), os.path.join(P, "audio", "music.wav")
json.dump(cues, open(cp, "w"))
if os.environ.get("NO_MUSIC") != "1":
    subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), wav, "%.2f" % (DURATION + 0.4), cp], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", os.path.join(P, "audio", "music.mp3")], check=True)
    os.remove(wav)

# ---- report: shot timing, snaps, overruns, frame check
print("shot  start   dur  phrase")
for k, s in enumerate(shots):
    print("S%02d  %6.2f %5.2f  %-26s d %.1f%s" % (k, starts[k], s["_dur"], s["_phrase"], s["distance"], "  snap" if s.get("snap") else ""))
    if s["_dur"] < 0.7: print("   ! very short shot")
    for a in s["actions"]:
        if a["at"] > s["_dur"] + 0.25: print("   ! S%02d action at %.2f s runs past the shot (%.2f s): %s" % (k, a["at"], s["_dur"], a["who"]))
print("snaps %d, comic fx %d" % (sum(1 for s in shots if s.get("snap")), len(FX)))
flags = sum(shot_cuts(k, s, True) for k, s in enumerate(shots))
BOXES = []
for pr in props:
    if pr["type"] not in ("house", "box", "crate", "wall"): continue
    (x, y, z), sz = pr["pos"], pr["size"]; w, h, d = sz if isinstance(sz, list) else (sz, sz, sz)
    if pr["type"] == "house": r = max(w, d) * 0.78 * 1.4143; BOXES.append((pr, x - max(w / 2, r), y, z - max(d / 2, r), x + max(w / 2, r), y + h * 1.6, z + max(d / 2, r)))
    else: BOXES.append((pr, x - w / 2, y, z - d / 2, x + w / 2, y + h, z + d / 2))
for k, s in enumerate(shots):
    for tl in moments(s):
        cp_ = cam(s, tl)[0]
        for pr, x0, y0, z0, x1, y1, z1 in BOXES:
            if x0 - 0.12 <= cp_[0] <= x1 + 0.12 and y0 - 0.12 <= cp_[1] <= y1 + 0.12 and z0 - 0.12 <= cp_[2] <= z1 + 0.12:
                flags += 1; print("   INSIDE S%02d t=%.2f %s@%s" % (k, tl, pr["type"], pr["pos"]))
for a_, b_ in [(x, y) for x in RECT for y in RECT if x < y and RECT[x][0] is RECT[y][0]]:   # cards on screen together must not overlap
    s, A, B_ = RECT[a_][0], RECT[a_], RECT[b_]
    off = lambda cid, at: min([x["at"] for x in s["actions"] if x["who"] == cid and x.get("to") == PARK and x["at"] > at] + [99])
    if max(A[1], B_[1]) < min(off(a_, A[1]), off(b_, B_[1])) and A[2] < B_[4] and B_[2] < A[4] and A[3] < B_[5] and B_[3] < A[5]:
        flags += 1; print("   OVERLAP S%02d %s / %s" % (shots.index(s), a_, b_))
print("frame check: %d CUT flags" % flags)
for s in shots: s.pop("_phrase"); s.pop("_dur", None); s.pop("_dis", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
