#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 12: GTA Online's loading screen beat Rockstar for 7 years; t0st killed it.
usage: build_short.py <project folder>
Ten sets 70 units apart: AR boss arena (hook + loop), LV lounge, HG hourglass desert, RM t0st's snowy room, CY cyber city inside the
code, FL file archive, CK checking factory, SP sunny finish line, HQ award stage, ST night street.  Every shot moves (crane / orbit /
push-in / pull-out); same-set shots fly (dolly glide), new sets dissolve.  Snap-ins, atmosphere, depth of field, comic fx, a cutaway
bar chart for the fix.  Cards are fitted to the safe box; the frame check prints CUT / SIGNCUT / INSIDE / OVERLAP flags."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(WH=0, BY=70, RG=140, DK=210, SK=280, WF=350, SM=420, TN=490, EX=560, GF=630, NL=700)
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


def dock(loc, x, z, w=2.2, d=1.6):
    box(loc, x, 0.04, z, [w, 0.3, d], texture="wood.jpg", repeat=[2, 2])
    for sx in (-1, 1): post(loc, x + sx * (w / 2 - 0.1), z - d / 2 + 0.1, 0.75, "#5a3a2a")


yard("WH", "whirlbg.png", "lake.jpg"); box("WH", 0.3, 0.04, -3.6, [5.2, 0.03, 4.0], texture="swirl.jpg", repeat=[1, 1]); dock("WH", -1.5, -1.3)
for x, z, s in ((-4.0, -4.6, 0.9), (4.2, -4.4, 0.8)): tree("WH", x, z, s, "#3f7a5a")
yard("BY", "bayou.png", "lily.jpg")
for x, z, s in ((-3.6, -3.8, 1.0), (3.8, -4.2, 0.9), (-2.2, -5.0, 0.7)): tree("BY", x, z, s, "#4f8a5a")
for x, z in ((-1.4, -1.8), (0.9, -2.6), (2.2, -1.6), (-2.6, -2.8)): box("BY", x, 0.04, z, [0.6, 0.02, 0.4], color="#5aa060")
post("BY", 1.7, -3.2, 1.2, "#5a3a2a")
yard("RG", "lakenoon.png", "noon.jpg")
for x, z in ((-2.8, -2.6), (2.9, -2.2)): box("RG", x, 0.04, z, [0.3, 0.3, 0.3], color="#ff8a30")
yard("DK", "deck.png", "steel.jpg"); box("DK", -3.0, 0.04, -3.6, [1.6, 0.5, 0.8], color="#8a96a8"); crate("DK", 2.9, 0.04, -2.4, 0.6); crate("DK", 3.3, 0.04, -3.2, 0.5)
lamp("DK", 3.5, -4.0, 2.2, "#3a3f4a", "#fff0c0")
yard("SK", "storm.png", "stormw.jpg"); box("SK", 0, 0.04, -3.2, [6.0, 0.03, 4.4], texture="swirl2.jpg", repeat=[1, 1])
for x, z, s in ((-4.0, -4.6, 0.9), (4.1, -4.8, 0.8)): tree("SK", x, z, s, "#4a7a50")
yard("WF", "falls.png", "canal.jpg")
for x, z, s in ((-2.9, -3.4, 0.9), (3.0, -3.0, 0.8)): tree("WF", x, z, s, "#4f9a5a")
for x, z in ((-2.2, -1.8), (2.4, -2.2)): barrel("WF", x, z)
yard("SM", "saltmine.png", "salt.jpg")
for x, z in ((-3.0, -3.0), (3.1, -3.4)): box("SM", x, 0.04, z, [0.8, 2.6, 0.8], color="#f4e6ee")
lamp("SM", -1.9, -4.2, 2.2, "#7a5a70", "#fff0a0")
yard("TN", "tunnel.png", "flood.jpg")
for x, z in ((-3.2, -3.4), (3.3, -3.0)): box("TN", x, 0.04, z, [0.8, 2.8, 0.8], color="#f6e8f0")
yard("EX", "escape.png", "grass.jpg")
for x, z, s in ((-3.6, -3.6, 0.9), (3.7, -4.0, 1.0)): tree("EX", x, z, s, "#5aa050")
yard("GF", "gulf.png", "sea.jpg")
for x, z in ((-2.6, -2.4), (2.7, -2.0)): box("GF", x, 0.04, z, [0.3, 0.3, 0.3], color="#ff5a50")
yard("NL", "newlake.png", "dusk.jpg"); dock("NL", -0.6, -1.5)
for x, z, s in ((-3.8, -4.2, 0.9), (3.9, -4.6, 0.8)): tree("NL", x, z, s, "#3f6a5a")
lamp("NL", 1.6, -2.6, 1.7, "#4a3a5a", "#fff0c0")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
FP = pos("WH", -0.85, 0.34, -1.25)
human("fisher", "fisher", FP, face="shocked"); put("pizza", "pizza", pos("WH", 0.5, 0.06, -1.6), 1.1, face="shocked")
put("gullB", "gull", pos("BY", 1.7, 1.2, -3.2), 0.5)
put("rig", "rig", pos("RG", 0.8, 0.04, -3.6), 3.6); put("pole", "pole", pos("RG", -1.2, 0.04, -1.6), 1.7)
human("driller", "driller", pos("DK", -0.6, 0.04, -2.0), face="nervous"); put("bit", "bit", pos("DK", 0.8, 0.04, -2.6), 2.2)
put("rigS", "rig", pos("SK", 0.0, 0.04, -4.2), 2.8); put("barge1", "barge", pos("SK", -0.8, 0.04, -2.3), 0.6); put("barge2", "barge", pos("SK", 0.9, 0.04, -3.0), 0.55)
put("gullW", "gull", pos("WF", -1.3, 2.6, -3.5), 0.55)
human("minerS", "miner", pos("SM", -0.6, 0.04, -2.2), face="happy"); put("bitS", "bit", PARK, 1.8)
human("m1", "miner", pos("TN", -1.2, 0.04, -2.6), face="shocked"); human("m2", "miner", pos("TN", -0.4, 0.04, -3.1), face="shocked"); human("m3", "miner", pos("TN", 0.4, 0.04, -2.7), face="shocked")
human("e1", "miner", pos("EX", -0.9, 0.04, -2.4), face="happy"); human("e2", "miner", pos("EX", 0.0, 0.04, -2.9), face="shouting"); human("e3", "miner", pos("EX", 0.9, 0.04, -2.4), face="happy")
put("g1", "gull", pos("GF", -1.3, 2.2, -3.0), 0.6); put("g2", "gull", pos("GF", 1.1, 2.7, -3.6), 0.5)
human("fisherN", "fisher", pos("NL", -0.6, 0.34, -1.5), face="happy")

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


def ft(s, who, seq): s["_ft"] = (who, seq)
def snap(s, t, z=25): SNAPC.append((s, t, z))
def cfx(s, t, typ, on, dur=0.9): FXC.append((s, t, typ, on, dur))


HOOK = dict(anchor=(-0.12, 1.3, -1.45), dist=8.6, yaw=-6, pitch=10)
# ---- 0-2.6 hook: A hole the size of a pizza swallowed an entire lake.
s = S("0", "WH", zoom=7, pan=(-3, 0), **HOOK); ft(s, "fisher", ["shocked", "shouting", "shocked"]); act(s, 0.0, "fisher", pose=dict(armR=-150)); act(s, 0.1, "pizza", shake=0.3)
tag(s, 0.0, "pizzahole", 0.3, 0.0, wf=0.6, hf=0.2); snap(s, rel(s, "pizza"), 12)
s = crane("swallowed an", "WH", (0.0, 0.8, -2.6), 9.5, 26, 6, 46, 18); ft(s, "fisher", ["shouting", "shocked"]); act(s, 0.0, "pizza", shake=0.4); tag(s, 0.05, "entire", 0.33, wf=0.5)
# ---- November 20, 1980. Texaco was drilling in Louisiana's Lake Peigneur, just 10 feet deep.
s = crane("November", "BY", (0.4, 1.8, -3.0), 8.0, -24, -2, 36, 6); tag(s, 0.05, "date", 0.2, -0.1, wf=0.34, hf=0.36)
s = crane("Texaco was", "RG", (0.6, 1.9, -3.4), 9.0, 22, 4, 34, 8); tag(s, 0.05, "texaco", 0.31, wf=0.5)
s = S("in Louisiana's", "RG", (0.8, 2.0, -3.6), 6.8, -14, pitch=6, zoom=10, pan=(3, 0)); tag(s, 0.05, "lakename", 0.31, wf=0.56)
s = S("just 10", "RG", (-1.2, 0.95, -1.6), 4.4, -14, pitch=5, yawTo=-2, type="macro", dof=dict(focus="pole", blur=0.5), _dis=1); hide(s, 0.0, "rig"); tag(s, 0.05, "ft10", 0.3, wf=0.46)
# ---- Then the 14-inch drill got stuck.
s = crane("Then the", "DK", (0.1, 1.35, -2.3), 6.4, 18, -4, 30, 6); ft(s, "driller", ["nervous", "shocked", "shouting"]); act(s, rel(s, "stuck"), "bit", shake=0.5)
tag(s, 0.05, "inch14", 0.31, wf=0.54); snap(s, rel(s, "stuck"), 14); cfx(s, rel(s, "stuck") + 0.1, "sweat", "driller", 0.8)
# ---- The water started to spin. A whirlpool swallowed the rig, 11 barges, and 65 acres of land.
s = crane("The water", "SK", (0.0, 0.5, -3.0), 9.0, -28, 8, 48, 26); tag(s, 0.05, "spin", 0.32, wf=0.54)
s = S("A whirlpool", "SK", (0.0, 1.4, -3.4), 8.2, 14, pitch=12, yawTo=-4, pitchTo=6); act(s, 0.0, "rigS", shake=0.4); go(s, 0.15, "rigS", pos("SK", 0.0, -1.1, -4.2), 1.2, walk=False)
act(s, 0.3, "barge1", shake=0.4); go(s, 0.5, "barge1", pos("SK", -0.5, -0.35, -2.7), 1.0, walk=False); tag(s, rel(s, "the rig"), "rigsw", 0.31, wf=0.5)
s = S("11 barges", "SK", (0.0, 2.0, -3.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="timeline", title="SWALLOWED", items=["THE RIG", "11 BARGES", "65 ACRES OF LAND"]))
# ---- A canal flowed backward into a 150-foot waterfall.
s = crane("A canal flowed", "WF", (0.0, 1.8, -4.0), 9.0, -22, 0, 34, 8); tag(s, 0.05, "backward", 0.32, wf=0.6, hf=0.14); go(s, 0.0, "gullW", pos("WF", -0.4, 2.9, -3.5), 1.6, walk=False)
s = S("into a", "WF", (0.0, 1.6, -4.6), 6.4, 8, pitch=4, zoom=12, pan=(0, 0)); tag(s, 0.05, "falls150", 0.31, wf=0.5); snap(s, 0.3, 14)
# ---- You see, right under the lake sat a salt mine. The drill punched straight into its tunnels, and the whole lake drained down.
s = crane("You see", "SM", (0.0, 2.2, -3.6), 10.0, 20, 0, 36, 6); ft(s, "minerS", ["happy", "smug"])
s = S("sat a salt", "SM", (-0.3, 1.4, -2.4), 5.4, -12, pitch=6, zoom=10, pan=(3, 0)); ft(s, "minerS", ["happy", "confused"]); tag(s, 0.05, "saltmine", 0.31, wf=0.56)
s = S("The drill punched", "SM", (0.1, 1.5, -2.6), 6.6, 12, pitch=8, yawTo=-2); show(s, 0.15, "bitS", pos("SM", 0.8, 1.3, -2.8), hop=0); go(s, 0.2, "bitS", pos("SM", 0.8, 0.5, -2.8), 0.35, walk=False)
act(s, 0.55, "bitS", shake=0.5); ft(s, "minerS", ["confused", "shocked", "shouting"]); tag(s, rel(s, "straight"), "tunnels", 0.32, wf=0.62, hf=0.13); snap(s, 0.6, 14); cfx(s, 0.7, "bang", "minerS", 0.6)
s = crane("and the whole", "TN", (0.0, 1.8, -3.0), 9.0, -20, 2, 34, 6); tag(s, 0.05, "drained", 0.32, wf=0.56)
for m in ("m1", "m2", "m3"): ft(s, m, ["shocked", "shouting"])
# ---- All 55 miners ran, and every one escaped.
s = S("All 55", "TN", (0.1, 1.3, -2.8), 8.4, 10, pitch=5, zoom=10, pan=(-3, 0)); tag(s, 0.05, "miners55", 0.31, wf=0.5)
for m, x, z in (("m1", -0.6, -2.6), ("m2", 0.2, -3.1), ("m3", 1.0, -2.7)): go(s, 0.0, m, pos("TN", x, 0.04, z), 1.2); ft(s, m, ["shouting", "shocked"])
cfx(s, 0.3, "speed", "m2", 0.8)
s = crane("and every one", "EX", (0.0, 1.5, -2.6), 7.4, 18, -2, 30, 8); tag(s, 0.05, "escaped", 0.31, wf=0.5); snap(s, 0.3, 14)
for m in ("e1", "e2", "e3"): act(s, 0.0, m, pose=dict(armR=-150, armL=150)); ft(s, m, ["happy", "shouting"])
# ---- The canal refilled it with salt water from the Gulf.
s = crane("The canal refilled", "GF", (0.0, 1.8, -3.4), 9.0, -18, 4, 36, 8); go(s, 0.0, "g1", pos("GF", -0.5, 2.4, -3.0), 1.4, walk=False); go(s, 0.0, "g2", pos("GF", 0.4, 2.9, -3.6), 1.4, walk=False)
s = S("salt water", "GF", (0.0, 1.9, -3.4), 6.6, 10, pitch=6, zoom=10, pan=(3, 0)); tag(s, 0.05, "gulf", 0.31, wf=0.52)
# ---- Lake Peigneur is still there. It's just not the same lake.
s = crane("Peigneur is", "NL", (0.0, 1.7, -2.6), 9.0, 20, 2, 32, 6); ft(s, "fisherN", ["happy", "smug"]); tag(s, 0.05, "still", 0.31, wf=0.56)
s = S("It's just", "NL", (-0.6, 1.55, -1.5), 4.4, -10, pitch=5, zoom=12, pan=(0, 0), dof=dict(focus="fisherN", blur=0.4)); ft(s, "fisherN", ["confused", "happy", "confused"])
tag(s, 0.05, "notsame", 0.32, wf=0.6, hf=0.14); snap(s, 0.2, 14); cfx(s, 0.4, "question", "fisherN")
# ---- All because of a hole the size of a pizza. (pull-out onto the hook frame)
s = S("All because", "WH", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "fisher", ["shocked", "shouting", "shocked"]); show(s, 0.0, "fisher", FP, hop=0)
act(s, 0.0, "pizza", shake=0.4); act(s, 0.0, "fisher", pose=dict(armR=-150)); tag(s, 0.05, "pizzahole", 0.3, 0.0, wf=0.6, hf=0.2)

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
    if "_ft" in s:
        who, seq = s.pop("_ft"); n = max(1, int((s["_dur"] - 0.3) / 0.55) + 1)
        prev, j = None, 0
        for i in range(n):
            while seq[j % len(seq)] == prev: j += 1
            prev = seq[j % len(seq)]; j += 1; act(s, round(i * 0.55, 3), who, face=prev)
# ---- atmosphere by set: dust + rays by day, bokeh by night / dawn
D_ = lambda c=22: dict(count=c, size=1.0, drift=1.0); BK = lambda a=0.3: dict(count=12, size=1.0, alpha=a)
ATM = dict(WH=dict(bokeh=BK(0.35), rays=dict(angle=30, intensity=0.45)), BY=dict(dust=D_(22), rays=dict(angle=28, intensity=0.55)), RG=dict(dust=D_(18), rays=dict(angle=35, intensity=0.5)),
           DK=dict(dust=D_(24), rays=dict(angle=22, intensity=0.5)), SK=dict(bokeh=BK(0.4)), WF=dict(dust=D_(20), rays=dict(angle=38, intensity=0.6)), SM=dict(dust=D_(26)),
           TN=dict(bokeh=BK(0.4)), EX=dict(dust=D_(18), rays=dict(angle=30, intensity=0.6)), GF=dict(dust=D_(14), rays=dict(angle=40, intensity=0.5)), NL=dict(bokeh=BK(0.35)))
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
    while shot_cuts(k, s) and s["distance"] < d0 * 1.35: s["distance"] = round(s["distance"] * 1.06, 3)
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
MOOD = dict(WH="whirl", BY="bayou", RG="noon", DK="deck", SK="storm", WF="falls", SM="salt", TN="flood", EX="escape", GF="gulf", NL="dusk")
light, cur = [{"t": 0, "mood": "whirl"}], "whirl"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 13,
    "moods": {"whirl": {"sun": {"azimuth": -30, "elevation": 22, "color": "#ffb070", "intensity": 2.3}, "sky": {"top": "#18465a", "horizon": "#ff9a50"}, "fill": {"sky": "#80e0e0", "ground": "#305050", "intensity": 1.4}}, "bayou": {"sun": {"azimuth": 40, "elevation": 15, "color": "#ffd0b0", "intensity": 2.3}, "sky": {"top": "#f08cb0", "horizon": "#ffe0a0"}, "fill": {"sky": "#ffc0d0", "ground": "#507060", "intensity": 1.35}}, "noon": {"sun": {"azimuth": 40, "elevation": 60, "color": "#fffaf0", "intensity": 2.5}, "sky": {"top": "#3a8af0", "horizon": "#d0f0ff"}, "fill": {"sky": "#b0d8ff", "ground": "#508040", "intensity": 1.2}}, "deck": {"sun": {"azimuth": -60, "elevation": 14, "color": "#ffb060", "intensity": 2.4}, "sky": {"top": "#784090", "horizon": "#ffa050"}, "fill": {"sky": "#ffb090", "ground": "#404050", "intensity": 1.35}}, "storm": {"sun": {"azimuth": 160, "elevation": 40, "color": "#c0f0d0", "intensity": 2.2}, "sky": {"top": "#3c1e5a", "horizon": "#6eaa78"}, "fill": {"sky": "#b0a0ff", "ground": "#305040", "intensity": 1.5}}, "falls": {"sun": {"azimuth": 0, "elevation": 30, "color": "#ffe8b0", "intensity": 2.4}, "sky": {"top": "#ffc070", "horizon": "#ffecbe"}, "fill": {"sky": "#fff0c0", "ground": "#607040", "intensity": 1.3}}, "salt": {"sun": {"azimuth": 30, "elevation": 50, "color": "#fff0f4", "intensity": 2.3}, "sky": {"top": "#f0c8dc", "horizon": "#ffe8f0"}, "fill": {"sky": "#ffd0e8", "ground": "#a07090", "intensity": 1.4}}, "flood": {"sun": {"azimuth": 0, "elevation": 50, "color": "#c0f0ff", "intensity": 2.4}, "sky": {"top": "#286e82", "horizon": "#96d2dc"}, "fill": {"sky": "#80e0ff", "ground": "#305a70", "intensity": 1.6}}, "escape": {"sun": {"azimuth": -40, "elevation": 18, "color": "#ffe0a0", "intensity": 2.4}, "sky": {"top": "#ffaa5a", "horizon": "#ffeca0"}, "fill": {"sky": "#fff0b0", "ground": "#608040", "intensity": 1.3}}, "gulf": {"sun": {"azimuth": 40, "elevation": 60, "color": "#fffaf0", "intensity": 2.5}, "sky": {"top": "#3caae6", "horizon": "#dcfaff"}, "fill": {"sky": "#b0f0ff", "ground": "#408080", "intensity": 1.2}}, "dusk": {"sun": {"azimuth": 200, "elevation": 20, "color": "#ffc890", "intensity": 2.3}, "sky": {"top": "#463282", "horizon": "#ffaa6e"}, "fill": {"sky": "#c0a0ff", "ground": "#504070", "intensity": 1.5}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff9a3c", "paper": ["#dcc49a", "#c9a878"], "dofPx": 8, "particle": "#ffe6b0", "bokehColor": "#a0c8ff", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(swallowed="swallowed an", nov="November", texaco="Texaco was", lake="in Louisiana's", feet="just 10", then="Then the", stuck="stuck", spin="The water", whirl="A whirlpool",
           barges="11 barges", acres="65 acres", canal="A canal flowed", falls="into a", yousee="You see", salt="sat a salt", drill="The drill punched", tunnels="tunnels",
           drained="drained", miners="All 55", escaped="escaped", refill="The canal refilled", gulf="salt water", still="Peigneur is", notsame="It's just", because="All because", pizza2="pizza#2")
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
