#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 10: GTA 6 launches Nov 19, first players got it Nov 18.
usage: build_short.py <project folder>
Five sets 70 units apart: NZ Kiwi gamer room at night (hook + loop), ST game store, BB delay billboard in town, LD London
at 11 a.m., NY New York at 6 a.m.  Every shot moves and dissolves (0.4 s) into the next; snap-ins, atmosphere, depth of
field, comic fx, a macro on the game box and a cutaway timeline for the midnight wave.  Cards are fitted to the safe box
(snap peak included); the frame check prints CUT / SIGNCUT / INSIDE flags.  The last shot pulls out onto the hook frame."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(NZ=0, ST=70, BB=140, LD=210, NY=280)
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
ROOMP = (0, 0.06, -4.82, 11, 5.04)
room("NZ", "#363c70", "nzroom.png", "wood.jpg", sidec="#2e3462")
box("NZ", -0.6, 0.06, -2.3, [3.2, 0.02, 2.2], color="#6a5ab0")
box("NZ", -4.2, 0, -3.9, [2.0, 0.55, 1.0], color="#c0506a"); box("NZ", -4.2, 0.55, -4.3, [2.0, 0.75, 0.25], color="#a84058")
box("NZ", 2.4, 0, -1.2, [1.2, 0.45, 0.7], color="#8a6248"); post("NZ", 3.6, -3.8, 1.9, "#d8c8a0"); box("NZ", 3.6, 1.9, -3.8, [0.5, 0.35, 0.5], color="#ffe7a8")
room("ST", "#eedab8", "store.png", "wood.jpg", sidec="#e0c8a0")
box("ST", 1.8, 0, -3.4, [1.6, 1.0, 0.8], color="#3a5cb0"); box("ST", 1.8, 1.0, -3.4, [1.7, 0.06, 0.9], color="#e8e0d0")
box("ST", -2.6, 0, -1.0, [0.9, 1.1, 0.9], color="#c04060")
plane("BB", "skyday.png", 0, -1, -30, 96, 42)
for x, z, sz, rf, wc in ((-7, -11, [4, 3.2, 4], "#c05a4a", "#f0e0c0"), (-2, -12.5, [3.5, 2.8, 3.5], "#5a7ac0", "#f4d8b0"),
                         (3.5, -11, [4, 3.6, 4], "#6aa060", "#ecdcc4"), (8.5, -12.5, [3.6, 3.0, 3.6], "#c08a40", "#f0e4d0")): house("BB", x, z, sz, rf, color=wc)
BBP = (0.3, 1.9, -3.5, 3.0, 1.67)
plane("BB", "billboard.png", *BBP); post("BB", -0.9, -3.55, 1.95, "#5a4a40"); post("BB", 1.5, -3.55, 1.95, "#5a4a40")
tree("BB", -3.4, -5.5, 0.9); tree("BB", 4.2, -6.0, 1.0); box("BB", 2.6, 0, -0.6, [1.4, 0.45, 0.45], color="#9a6a44")
plane("LD", "london.png", 0, -0.2, -6, 14, 6.13)
post("LD", -2.0, -2.4, 2.8, "#2e3440"); box("LD", -2.0, 2.8, -2.4, [0.4, 0.4, 0.4], color="#ffe7a8"); box("LD", -1.5, 0, -0.7, [0.45, 1.1, 0.45], color="#c8323c")
plane("NY", "nyc.png", 0, -0.2, -6, 14, 6.13)
box("NY", 1.7, 0, -2.9, [1.6, 0.35, 1.4], color="#8a5a44"); box("NY", 1.7, 0.35, -3.2, [1.6, 0.35, 0.8], color="#8a5a44")
post("NY", 0.85, -2.3, 1.0, "#2e3440"); box("NY", -1.9, 0, -0.8, [0.35, 0.7, 0.35], color="#d23c3c")

# ================================================================== CHARACTERS
K0 = pos("NZ", -1.2, 0.06, -2.4)
human("kiwiN", "kiwi", K0, face="shouting"); G0 = pos("NZ", -1.62, 0.72, -2.15); put("gboxN", "gbox", G0, 0.45)
human("shopgirl", "shopgirl", pos("ST", 0.5, 0.06, -2.7), face="happy"); human("kiwiS", "kiwi", pos("ST", -0.9, 0.06, -2.2), face="happy")
put("gboxS", "gbox", pos("ST", 1.8, 1.06, -3.3), 0.6)
human("kiwiB", "kiwi", pos("BB", -0.9, 0.06, -1.6), face="happy")
human("londoner", "londoner", pos("LD", 0.9, 0.06, -2.0), face="confused")
human("nyer", "nyer", pos("NY", -0.4, 0.06, -1.8), face="sneaky")

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}
N_ = [0]; REQ = []; SNAPC = []; FXC = []; LOC = {}


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):
    (ax, ay, az), d = s["anchor"], s["distance"]; y = math.radians(s["yaw"]); w = dx * 0.41 * d
    show(s, at, who, [round(ax + w * math.cos(y) + dz * math.sin(y), 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az - w * math.sin(y) + dz * math.cos(y), 3)], hop=0.12)


def tag(s, at, name, dy=0.25, dx=0.0, dz=0.3, wf=0.24, hf=0.17, tilt=0):
    N_[0] += 1; cid = "%s_%d" % (name, N_[0]); c = dict(id=cid, puppet="puppets/" + name, pos=PARK, height=0.1, face="default")
    if tilt: c["pose"] = dict(head=tilt)
    chars.append(c); s["_tags"].append(cid); REQ.append((s, at, cid, name, dy, dx, dz, wf, hf, c)); return cid


def S(start, loc, anchor, dist, yaw, pitch=4, zoom=8, pan=(0, 0), **kw):
    s = shot(start, anchor=pos(loc, *anchor), dist=dist, yaw=yaw, pitch=pitch, zoom=zoom, pan=pan)
    s["_tags"] = []; s["pan"] = [v * 5 for v in s["pan"]]; s["out"] = "dissolve"; s["outDur"] = 0.4; s.update(kw); LOC[id(s)] = loc; return s


def ft(s, who, seq): s["_ft"] = (who, seq)                    # face track, laid out once the shot length is known
def snap(s, t, z=25): SNAPC.append((s, t, z))
def cfx(s, t, typ, on, dur=0.9): FXC.append((s, t, typ, on, dur))


HOOK = dict(anchor=(-1.45, 1.4, -2.4), dist=5.6, yaw=-8, pitch=4)
# ---- 0-4 hook: GTA 6 launches on November 19th / the first players got it on November 18th
s = S("0", "NZ", zoom=8, pan=(-3, 0), **HOOK); ft(s, "kiwiN", ["shouting", "happy", "shocked"])
act(s, 0.0, "kiwiN", pose=dict(armR=-60)); act(s, 0.1, "kiwiN", shake=0.3); tag(s, 0.0, "launch19", 0.31, 0.04, wf=0.5, hf=0.2)
s = S("November 19th", "NZ", (-1.45, 1.45, -2.4), 3.9, 10, zoom=8, pan=(4, 0)); ft(s, "kiwiN", ["shocked", "happy"])
tag(s, 0.02, "cal19", 0.2, 0.24, wf=0.24, hf=0.22); snap(s, 0.05)
s = S("The first players", "NZ", (-1.3, 1.5, -2.6), 4.8, 12, zoom=8, pan=(-4, 0)); ft(s, "kiwiN", ["happy", "smug", "shouting"])
act(s, 0.0, "kiwiN", pose=dict(armL=40, armR=-40)); tag(s, rel(s, "November"), "first18", 0.31, wf=0.42); tag(s, rel(s, "18th"), "cal18", 0.05, 0.25, wf=0.2, hf=0.2)
# ---- 4-9 the delays on the town billboard
s = S("It was promised", "BB", (0.0, 2.0, -2.6), 9.0, -10, pitch=3, zoom=6, pan=(-4, 0), fgBlur=dict(side="left", blur=0.8))
ft(s, "kiwiB", ["happy", "smug", "happy"]); act(s, 0.0, "kiwiB", pose=dict(armR=-150)); tag(s, rel(s, "fall"), "fall25", 0.12, 0.05, wf=0.36)
s = S("Then May", "BB", (-0.3, 2.4, -3.0), 9.0, 10, pitch=2, zoom=8, pan=(3, 0)); ft(s, "kiwiB", ["shocked", "nervous"])
tag(s, 0.03, "delayed", 0.3, tilt=-8, wf=0.36); tag(s, rel(s, "May"), "may26", 0.1, wf=0.42); snap(s, rel(s, "May"))
s = S("Then November", "BB", (-0.9, 1.45, -1.6), 4.6, -12, zoom=8, pan=(-4, 0), dof=dict(focus="kiwiB", blur=0.4)); ft(s, "kiwiB", ["nervous", "shocked", "shouting", "nervous"])
d1 = tag(s, 0.03, "delayed", 0.3, tilt=7, wf=0.36); n1 = tag(s, rel(s, "November"), "nov19", 0.1, wf=0.3); td = rel(s, "Two delays")
hide(s, td - 0.02, d1); hide(s, td - 0.02, n1); act(s, td, "kiwiB", shake=0.4, pose=dict(armR=-150, armL=150)); tag(s, td, "delays2", 0.24, wf=0.3); cfx(s, td + 0.1, "sweat", "kiwiB")
# ---- 9-19 the store: most pre-ordered, the box with no disc, a download code, 200 GB
s = S("It still became", "ST", (0.3, 2.3, -2.8), 8.6, 8, zoom=6, pan=(-4, 0)); ft(s, "shopgirl", ["happy", "smug", "happy"])
act(s, 0.0, "kiwiS", face="happy"); tag(s, rel(s, "most"), "preord", 0.3, wf=0.44)
s = S("in PlayStation Store", "ST", (1.1, 1.4, -2.9), 5.0, -12, zoom=8, pan=(-3, 0)); ft(s, "shopgirl", ["shouting", "happy"])
act(s, 0.0, "shopgirl", pose=dict(armR=-150, armL=150), shake=0.3); tag(s, 0.05, "psstore", 0.31, wf=0.72, hf=0.14); snap(s, 0.05)
s = S("And the box", "ST", (1.8, 1.34, -3.3), 1.75, 6, zoom=7, pan=(2, 0), type="macro", dof=dict(focus="gboxS", blur=0.6))
s = S("No disc inside", "ST", (1.8, 1.36, -3.3), 2.6, -8, zoom=8, pan=(-3, 0), dof=dict(focus="gboxS", blur=0.5))
act(s, 0.0, "gboxS", face="open", shake=0.3); tag(s, rel(s, "No disc"), "nodisc", 0.3, tilt=-6, wf=0.5); snap(s, 0.08, 20)
s = S("Just a download code", "ST", (-0.2, 1.45, -2.5), 5.4, 10, zoom=8, pan=(3, 0)); ft(s, "kiwiS", ["shocked", "confused"])
act(s, 0.0, "shopgirl", face="nervous"); tag(s, rel(s, "download"), "codecard", 0.27, wf=0.36)
s = S("for a game over", "ST", (-0.9, 1.25, -2.2), 4.4, -14, zoom=8, pan=(-4, 0), dof=dict(focus="kiwiS", blur=0.5)); ft(s, "kiwiS", ["shocked", "shouting"])
show(s, 0.0, "shopgirl", PARK, hop=0); g2 = rel(s, "200"); act(s, g2, "kiwiS", shake=0.4); tag(s, g2, "gb200", 0.26, 0.18, wf=0.3); snap(s, g2, 20); cfx(s, g2, "speed", "kiwiS", 0.7)
# ---- 19-26 the pivot: not one moment, midnight local time, country by country, New Zealand first
s = S("You see", "NZ", (-1.0, 1.55, -2.6), 5.2, 10, zoom=8, pan=(4, 0)); ft(s, "kiwiN", ["confused", "nervous", "confused"]); show(s, 0.0, "gboxN", PARK, hop=0)
tag(s, rel(s, "one moment"), "notone", 0.3, tilt=-6, wf=0.5); cfx(s, 0.5, "question", "kiwiN")
s = S("It unlocks at midnight", "NZ", (-0.95, 1.6, -2.6), 5.6, -10, zoom=8, pan=(3, 0)); ft(s, "kiwiN", ["shocked", "happy", "shocked"])
tag(s, 0.05, "clock12", 0.0, 0.25, wf=0.2, hf=0.17); tag(s, rel(s, "midnight"), "midnite", 0.3, 0.0, wf=0.42); snap(s, rel(s, "midnight"), 20)
s = S("country by country", "NZ", (-1.6, 1.9, -3.0), 5.6, 12, pitch=2, zoom=8, pan=(-3, 0)); ft(s, "kiwiN", ["happy", "smug"])
act(s, 0.0, "kiwiN", pose=dict(armR=-150)); tag(s, 0.05, "cbyc", 0.32, wf=0.56)
s = S("New Zealand hits", "NZ", (-0.6, 1.6, -2.6), 5.0, -14, zoom=8, pan=(4, 0)); ft(s, "kiwiN", ["shouting", "happy", "shouting"])
act(s, 0.05, "kiwiN", pose=dict(armR=-150, armL=150), shake=0.4); tag(s, 0.05, "nzfirst", 0.3, wf=0.56); snap(s, 0.1); cfx(s, 0.25, "bang", "kiwiN")
# ---- 26-33 London 11 a.m. on November 18th, New York 6 a.m., the wave rolls west
s = S("In London", "LD", (-0.2, 2.2, -2.6), 8.6, 8, pitch=-2, zoom=6, pan=(-3, 0), fgBlur=dict(side="right", blur=0.8)); ft(s, "londoner", ["confused", "shocked", "confused"])
tag(s, rel(s, "11"), "ldn11", 0.06, -0.18, wf=0.3); tag(s, rel(s, "November"), "nov18", -0.1, -0.18, wf=0.26); cfx(s, rel(s, "11") + 0.2, "question", "londoner")
s = S("In New York", "NY", (-0.3, 1.6, -2.0), 5.2, -10, zoom=8, pan=(3, 0)); ft(s, "nyer", ["sneaky", "neutral", "sneaky"])
tag(s, rel(s, "6 am"), "ny6", 0.28, 0.12, wf=0.34); snap(s, 0.08); cfx(s, 0.3, "z", "nyer", 1.2)
s = S("Then the wave", "NY", (0.0, 1.6, -2.0), 6.0, 6, zoom=6, pan=(-3, 0), type="cutaway",
      long=True, diagram=dict(kind="timeline", title="THE WAVE ROLLS WEST", items=["NEW ZEALAND: MIDNIGHT", "LONDON: 11 A.M.", "NEW YORK: 6 A.M."]))
# ---- 33-43 years of delays, launch day didn't fit inside one day, NZ already playing, the planet still on the 18th
s = S("So after years", "BB", (0.0, 2.4, -2.8), 8.2, 12, zoom=8, pan=(3, 0)); ft(s, "kiwiB", ["nervous", "shocked"])
tag(s, rel(s, "years"), "yrsdelay", 0.3, tilt=-6, wf=0.5); cfx(s, 0.3, "sweat", "kiwiB"); snap(s, rel(s, "years"), 20)
s = S("launch day didn't", "ST", (0.4, 2.35, -2.8), 8.8, -10, zoom=8, pan=(-3, 0)); ft(s, "shopgirl", ["confused", "shocked", "confused"]); show(s, 0.0, "shopgirl", pos("ST", 0.5, 0.06, -2.7), hop=0)
tag(s, 0.05, "cal18", 0.02, -0.25, wf=0.2, hf=0.18); tag(s, 0.25, "cal19", 0.02, 0.25, wf=0.2, hf=0.18); tag(s, rel(s, "fit"), "oneday", 0.31, wf=0.6)
s = S("Players in New Zealand", "NZ", (-0.9, 1.5, -2.6), 4.4, 14, zoom=8, pan=(-4, 0), dof=dict(focus="kiwiN", blur=0.4)); ft(s, "kiwiN", ["happy", "smug", "happy"])
act(s, 0.0, "kiwiN", pose=dict(armL=40, armR=-40)); al = rel(s, "already"); tag(s, al, "playing", 0.3, wf=0.5); snap(s, al); cfx(s, al + 0.2, "blush", "kiwiN")
s = S("while most of the planet", "NZ", (-1.6, 1.9, -3.0), 5.6, -12, pitch=2, zoom=8, pan=(3, 0)); ft(s, "kiwiN", ["happy", "smug"])
act(s, 0.0, "kiwiN", pose=dict(armR=-150))
s = S("was still living", "NZ", zoom=-7, pan=(3, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "kiwiN", ["smug", "happy", "shouting"])
show(s, 0.0, "gboxN", G0, hop=0); act(s, 0.0, "kiwiN", pose=dict(armR=-60)); tag(s, 0.05, "still18", 0.31, 0.04, wf=0.46, hf=0.2)
for s in shots: s.setdefault("frameY", 0.0)

starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots): s["_dur"] = (starts[k + 1] if k + 1 < len(shots) else DURATION) - starts[k]
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
ATM = dict(NZ=dict(bokeh=dict(count=12, size=1.0, alpha=0.3)), ST=dict(dust=dict(count=22, size=1.0, drift=1.0)),
           BB=dict(dust=dict(count=26, size=1.0, drift=1.0), rays=dict(angle=25, intensity=0.55)), LD=dict(dust=dict(count=22, size=1.0, drift=0.8), rays=dict(angle=30, intensity=0.5)),
           NY=dict(bokeh=dict(count=10, size=1.0, alpha=0.25), rays=dict(angle=35, intensity=0.35)))
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
    te = drift_t(s["_dur"], tl); y, p = math.radians(s["yaw"]), math.radians(s["pitch"]); dr = [math.sin(y) * math.cos(p), math.sin(p), math.cos(y) * math.cos(p)]
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
KOPEN = next(i for i, x in enumerate(shots) if x["_phrase"] == "No disc inside")
def shot_cuts(k, s, report=False):
    n = 0
    if s.get("type") == "cutaway": return 0
    for tl in moments(s):
        c = cam(s, tl); T = starts[k] + tl
        for cid, tr in track.items():
            if "_" in cid: continue                           # cards are fitted separately
            p0 = [e for e in tr if e[0] <= T][-1][1]
            if p0[1] < -50: continue
            h, w = SH[cid], (SH[cid] * 0.8 if cid.startswith("gbox") and (cid == "gboxN" or k < KOPEN) else WID[cid]); pts = [proj(c, [p0[0] + sx * w / 2, p0[1] + sy * h, p0[2]]) for sx in (-1, 1) for sy in (0, 1)]
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
MOOD = dict(NZ="night", ST="store", BB="day", LD="ldn", NY="dawn")
light, cur = [{"t": 0, "mood": "night"}], "night"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 10,
    "moods": {"night": {"sun": {"azimuth": 200, "elevation": 34, "color": "#b8c4ff", "intensity": 1.9}, "sky": {"top": "#141a40", "horizon": "#3a3a7a"},
                        "fill": {"sky": "#8a90e0", "ground": "#4a3a5a", "intensity": 1.25}},
              "store": {"sun": {"azimuth": 30, "elevation": 50, "color": "#ffe2b8", "intensity": 2.3}, "sky": {"top": "#6a9ae0", "horizon": "#f6dcb8"}, "fill": {"sky": "#b0c0ff", "ground": "#7a5a50", "intensity": 1.2}},
              "day": {"sun": {"azimuth": 40, "elevation": 46, "color": "#ffe8c8", "intensity": 2.4}, "sky": {"top": "#5b8ee0", "horizon": "#f6d6b0"}, "fill": {"sky": "#a0b4ff", "ground": "#6a4b6e", "intensity": 1.2}},
              "ldn": {"sun": {"azimuth": -30, "elevation": 52, "color": "#fff0d8", "intensity": 2.4}, "sky": {"top": "#78aee8", "horizon": "#f6e6c8"}, "fill": {"sky": "#b0c4ff", "ground": "#6a5a60", "intensity": 1.2}},
              "dawn": {"sun": {"azimuth": -60, "elevation": 14, "color": "#ffb08a", "intensity": 2.3}, "sky": {"top": "#6a5aa8", "horizon": "#ffc49a"}, "fill": {"sky": "#c0a0ff", "ground": "#6a4a5e", "intensity": 1.25}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#e0b43a", "paper": ["#dcc49a", "#c9a878"], "dofPx": 8, "particle": "#ffe6b0", "bokehColor": "#c8b4ff", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(nov19="November 19th", first="The first players", cal18="18th", promised="It was promised", fall="fall", may="Then May", nov19b="Then November",
           two="Two delays", most="most", ps="PlayStation", box="And the box", nodisc="No disc", code="download", gb="200", yousee="You see", moment="one moment",
           midnight="midnight", country="country by country", nz="New Zealand hits", london="In London", eleven="11", ny="In New York", six="6 am",
           wave="Then the wave", sofar="So after years", years="years", launch="launch day", fit="fit", already="already", still="was still living")
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
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
