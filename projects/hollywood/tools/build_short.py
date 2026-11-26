#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 32: the Hollywood sign was never about movies.
usage: build_short.py <project folder>
Seven jazz-age sets 70 units apart: HK peach-magenta sunset hillside with the sign (hook + loop; the "????" tarp over the missing end =
open loop, resolved when L, A, N, D wave goodbye), PR plum-gold premiere night, SG sage-terracotta lots, DC teal-gold art-deco office,
NT navy night with glowing bulbs, RU dusty-rose 1940s ruin, BL mint-cream 1949 office. Shots 0.7-2 s, every neighbour a different move;
the sign, letters and props are the stars, people small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, PR=70, SG=140, DC=210, NT=280, RU=350, BL=420)
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


yard("HK", "sunset.png", "hillfl.jpg"); box("HK", 0.0, 0.04, -3.3, [2.3, 0.9, 0.7], color="#a08a6a"); box("HK", 5.1, 0.04, -2.75, [1.9, 0.94, 0.5], color="#c89a6a"); tree("HK", -2.6, -4.4, 0.8, "#5a7a5a"); tree("HK", 2.8, -4.6, 0.9, "#64845e")
yard("PR", "premiere.png", "carpet.jpg"); box("PR", 0.0, 0.04, -2.8, [1.4, 0.3, 1.0], color="#f0c450")
yard("SG", "sage.png", "sagefl.jpg"); tree("SG", -3.6, -4.2, 0.9, "#7aa070"); tree("SG", 3.4, -4.0, 0.8, "#86aa78")
yard("DC", "deco.png", "decofl.jpg"); box("DC", 1.1, 0.04, -2.8, [1.4, 0.5, 0.8], color="#2a5a64")
yard("NT", "nightglow.png", "nightfl.jpg"); box("NT", 0.0, 0.04, -3.5, [3.0, 0.86, 0.6], color="#3a4a6a")
yard("RU", "ruin.png", "dustfl.jpg"); box("RU", 0.0, 0.04, -3.3, [3.0, 0.76, 0.6], color="#8a7a7a"); barrel("RU", -3.2, -3.6)
yard("BL", "blinds.png", "officefl.jpg"); box("BL", 0.0, 0.04, -2.7, [1.8, 0.3, 0.8], color="#7a5a40")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("signK", "sign", pos("HK", 0.0, 0.94, -3.3), 0.6); human("lineK", "lineman", pos("HK", 0.6, 0.04, -2.3), face="shocked", h=1.05)
for ch_ in "LAND": put("let%sK" % ch_, "let" + ch_, PARK, 0.85)
put("hourK", "hourglass", pos("HK", -4.2, 0.04, -2.4), 1.0); put("sciK", "scissors", pos("HK", -7.6, 0.3, -2.4), 0.7)
put("globeP", "globe", pos("PR", 0.0, 0.34, -2.8), 1.3)
put("houseS", "house", pos("SG", -0.95, 0.04, -3.0), 0.8); put("lotsS", "lots", pos("SG", 0.9, 0.04, -2.4), 0.7); put("giantS", "giant", pos("SG", 5.4, 0.04, -2.6), 1.4)
human("chandD", "chandler", pos("DC", -0.8, 0.04, -2.2), face="happy", h=1.6); put("paperD", "paper", pos("DC", 1.1, 0.54, -2.8), 0.95)
put("signN", "sign", pos("NT", 0.0, 0.9, -3.5), 0.6, face="glow"); put("bulbsN", "bulbs", pos("NT", 3.4, 0.2, -2.4), 0.8); human("lineN", "lineman", pos("NT", -2.6, 0.04, -2.2), face="happy", h=1.5)
put("signR", "sign", pos("RU", 0.0, 0.8, -3.3), 0.6, face="old"); put("bulbsR", "bulbs", pos("RU", 3.2, 0.04, -2.4), 0.7, face="off")
put("dealB", "contract", pos("BL", 0.0, 0.34, -2.7), 1.25)
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


def T(s, name, at=0.05, dy=0.31, wf=0.56, **kw): return tag(s, at, name, dy, wf=wf, **kw)
def swap(s, old, t, name, **kw): hide(s, t - 0.02, old); return T(s, name, t, **kw)
def blink(s, who, t0, t1, step=0.3):
    t, k = t0, 0
    while t < t1: act(s, round(t, 3), who, face="b" if k % 2 == 0 else "default"); t += step; k += 1


HOOK = dict(anchor=(0.0, 1.25, -3.0), dist=6.2, yaw=14, pitch=6)
LAND_P = dict(L=(4.68, 0.98, -2.75), A=(5.52, 0.98, -2.75), N=(4.68, 0.04, -2.2), D=(5.52, 0.04, -2.2))
# ---- The Hollywood sign was never about movies. It's a billboard for houses, and it was built to come down.
s = S("0", "HK", zoom=5, **HOOK); act(s, 0.0, "signK", shake=0.4); tag(s, 0.0, "hookc", 0.31, 0.0, wf=0.6, hf=0.19); ft(s, "lineK", ["shocked", "confused"])
s = S("never about movies", "PR", (0.0, 1.0, -2.8), 4.8, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="globeP", blur=0.5)); act(s, rel(s, "movies"), "globeP", shake=0.5); snap(s, rel(s, "movies"), 10)
s = S("It's a billboard", "SG", (-0.95, 0.5, -3.0), 4.2, 8, pitch=6, zoom=12, dof=dict(focus="houseS", blur=0.4)); act(s, rel(s, "houses"), "houseS", shake=0.5); T(s, "adc", at=rel(s, "billboard"), dy=0.38, wf=0.62)
s = S("and it was", "HK", (-4.2, 0.6, -2.4), 4.2, -10, pitch=14, pitchTo=3, dof=dict(focus="hourK", blur=0.4)); act(s, rel(s, "down"), "hourK", shake=0.5); T(s, "down", at=rel(s, "built"), dy=0.38, wf=0.6)
# ---- Los Angeles, 1923. A group of developers, including the publisher of the Los Angeles Times, is selling hillside lots in a neighborhood called Hollywoodland.
s = crane("Los Angeles 1923", "SG", (0.0, 0.8, -2.7), 7.6, -22, -2, 36, 8); T(s, "y1923", at=rel(s, "1923"), dx=-0.24, dy=0.22, wf=0.26, hf=0.26)
s = crane("A group of", "DC", (0.2, 1.0, -2.4), 7.0, 22, 2, 34, 8); ft(s, "chandD", ["happy", "smug"])
s = S("including the publisher", "DC", (-0.8, 1.05, -2.2), 4.4, -8, pitch=5, zoom=12, dof=dict(focus="chandD", blur=0.4)); ft(s, "chandD", ["smug", "happy"]); cfx(s, 0.2, "glint", "chandD", 0.5)
s = S("Los Angeles Times", "DC", (1.1, 1.0, -2.8), 4.2, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="paperD", blur=0.5)); act(s, 0.05, "paperD", shake=0.5); T(s, "pubc", at=0.05, dy=0.38, wf=0.6); snap(s, 0.15, 8)
s = S("is selling hillside", "SG", (0.9, 0.45, -2.4), 4.6, 6, pitch=8, zoom=4, pan=(-8, 0)); act(s, rel(s, "lots"), "lotsS", shake=0.5)
s = S("a neighborhood called", "SG", (0.0, 0.7, -2.7), 7.6, -10, pitch=5, zoom=-10); T(s, "hlandc", at=rel(s, "Hollywoodland") - 0.2, dy=0.36, wf=0.62)
# ---- So they write its name on the hill. Thirteen letters, each about forty-five feet tall. Four thousand light bulbs. Twenty-one thousand dollars. Planned life: about a year and a half.
s = crane("So they write", "HK", (0.0, 1.25, -3.3), 6.6, -22, 8, 36, 8); hide(s, 0.0, "lineK"); act(s, 0.0, "signK", face="land", shake=0.4)
s = S("Thirteen letters", "HK", (0.0, 1.25, -3.3), 5.4, -12, pitch=5, yawTo=8); act(s, 0.05, "signK", face="land", shake=0.3); T(s, "thirteen", at=0.05, dy=0.36, wf=0.42)
s = S("each about fortyfive", "SG", (5.4, 0.8, -2.6), 4.8, 4, pitch=-2, pitchTo=10, dof=dict(focus="giantS", blur=0.4)); act(s, 0.05, "giantS", shake=0.3); T(s, "ft45", at=0.1, dy=0.38, wf=0.62); snap(s, 0.2, 8)
s = S("Four thousand light", "NT", (3.4, 0.6, -2.4), 4.0, 12, pitch=6, yawTo=-6, type="macro", dof=dict(focus="bulbsN", blur=0.5)); act(s, 0.05, "bulbsN", shake=0.5); T(s, "bulbc", at=0.1, dy=0.38, wf=0.56)
s = S("Twentyone thousand", "NT", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="TWENTY-ONE THOUSAND", items=["DOLLARS"]))
s = S("Planned life about", "HK", (-4.2, 0.55, -2.4), 4.4, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="hourK", blur=0.5)); act(s, 0.05, "hourK", shake=0.4); T(s, "lifec", at=0.1, dy=0.38, wf=0.56); snap(s, rel(s, "year"), 8)
# ---- You see, nobody took it down. It just sat there, falling apart. Then in 1949, a deal saved it, with one condition: cut the last four letters. L. A. N. D.
s = crane("You see nobody", "RU", (0.0, 1.0, -3.0), 6.6, 22, 2, 36, 8); act(s, 0.2, "signR", shake=0.3); T(s, "nobody", at=rel(s, "nobody"), dy=0.35, wf=0.62)
s = S("It just sat", "RU", (0.0, 1.0, -3.3), 6.4, 6, pitch=8, zoom=4, pan=(8, 0)); act(s, rel(s, "falling"), "signR", shake=0.6); T(s, "apart", at=rel(s, "falling"), dy=0.37, wf=0.5); cfx(s, 0.3, "sweat", "bulbsR", 0.6)
s = crane("Then in 1949", "BL", (0.0, 1.0, -2.6), 6.6, -22, -2, 34, 8); T(s, "y1949", at=rel(s, "1949"), dx=-0.2, dy=0.33, wf=0.24, hf=0.24)
s = S("a deal saved", "BL", (0.0, 0.95, -2.7), 4.4, 8, pitch=6, zoom=12, dof=dict(focus="dealB", blur=0.4)); act(s, rel(s, "saved"), "dealB", shake=0.5)
s = S("one condition", "BL", (0.0, 0.95, -2.7), 4.8, -4, pitch=14, pitchTo=3); act(s, 0.05, "dealB", face="cut", shake=0.6); T(s, "cond", at=0.05, dy=0.38, wf=0.5)
s = S("cut the last", "HK", (-7.6, 0.55, -2.4), 4.0, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="sciK", blur=0.5)); act(s, rel(s, "cut"), "sciK", shake=0.7); snap(s, rel(s, "cut") + 0.05, 10)
s = S("L", "HK", (5.1, 0.95, -2.5), 5.2, 6, pitch=6, zoom=6)
for ch_ in "LAND": show(s, rel(s, ch_.lower()), "let%sK" % ch_, pos("HK", *LAND_P[ch_]))
# ---- So the most famous movie sign on Earth is a real estate ad with the ending chopped off. And it was never about movies.
s = S("So the most", "PR", (0.0, 1.0, -2.8), 5.6, 10, pitch=5, zoom=-10); act(s, 0.05, "globeP", shake=0.4); T(s, "famous", at=rel(s, "famous"), dy=0.38, wf=0.5)
s = S("is a real", "HK", (0.0, 1.25, -3.3), 6.0, -10, pitch=6, yawTo=6); act(s, 0.0, "signK", face="cut", shake=0.4); T(s, "realad", at=rel(s, "real"), dy=0.38, wf=0.56); snap(s, rel(s, "estate"), 8)
s = S("ending chopped off", "HK", (5.1, 0.95, -2.5), 5.6, -4, pitch=14, pitchTo=3)
for ch_ in "LAND": act(s, 0.05, "let%sK" % ch_, face="bye", shake=0.6)
s = S("never about#2", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "lineK", pos("HK", 0.6, 0.04, -2.3), hop=0); act(s, 0.0, "signK", face="default", shake=0.4); T(s, "hookc", at=0.05, dy=0.31, wf=0.6, hf=0.19)
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
ATM = dict(HK=dict(dust=D_(22), rays=dict(angle=24, intensity=0.7)), PR=dict(bokeh=BK(0.55)), SG=dict(dust=D_(22), rays=dict(angle=30, intensity=0.6)), DC=dict(dust=D_(20), rays=dict(angle=20, intensity=0.5)),
           NT=dict(bokeh=BK(0.5)), RU=dict(dust=D_(30)), BL=dict(dust=D_(22), rays=dict(angle=26, intensity=0.6)))
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
MOOD = dict(HK="sunset", PR="premiere", SG="sage", DC="deco", NT="night23", RU="ruin", BL="blinds")
light, cur = [{"t": 0, "mood": "sunset"}], "sunset"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"sunset": {"sun": {"azimuth": 230, "elevation": 20, "color": "#ffdcc0", "intensity": 2.6}, "sky": {"top": "#e6468c", "horizon": "#ffc896"}, "fill": {"sky": "#fff0ec", "ground": "#7a5a5a", "intensity": 1.9}},
              "premiere": {"sun": {"azimuth": 160, "elevation": 36, "color": "#fff0e8", "intensity": 2.6}, "sky": {"top": "#461e5a", "horizon": "#c85a8c"}, "fill": {"sky": "#fff0f4", "ground": "#6a3a50", "intensity": 2.3}},
              "sage": {"sun": {"azimuth": 50, "elevation": 40, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#bedcf0", "horizon": "#ffecd2"}, "fill": {"sky": "#fffaf4", "ground": "#7a7a5a", "intensity": 1.5}},
              "deco": {"sun": {"azimuth": 150, "elevation": 38, "color": "#fff8ec", "intensity": 2.5}, "sky": {"top": "#146e78", "horizon": "#3caaaa"}, "fill": {"sky": "#f0fffc", "ground": "#3a5a60", "intensity": 2.2}},
              "night23": {"sun": {"azimuth": 20, "elevation": 40, "color": "#eef2ff", "intensity": 2.7}, "sky": {"top": "#141e5a", "horizon": "#465aaa"}, "fill": {"sky": "#eef2ff", "ground": "#2a3460", "intensity": 2.4}},
              "ruin": {"sun": {"azimuth": 200, "elevation": 30, "color": "#fff0ec", "intensity": 2.4}, "sky": {"top": "#9696aa", "horizon": "#e6b4b4"}, "fill": {"sky": "#fff4f4", "ground": "#7a6a6a", "intensity": 1.8}},
              "blinds": {"sun": {"azimuth": 140, "elevation": 40, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#aae6d2", "horizon": "#faf6e6"}, "fill": {"sky": "#fafffc", "ground": "#7a6a5a", "intensity": 1.6}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#f0c450", "paper": ["#e68cb4", "#d278a0"], "dofPx": 8, "particle": "#fff4ec", "bokehColor": "#ffd8b0", "ray": "#fff4e4", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(la1923="Los Angeles 1923", yousee="You see nobody", then49="Then in 1949", sothe="So the most",
           movies="movies", billboard="billboard", down="come down", y1923="1923", group="group", publisher="publisher", times="Times", lots="lots", hland="Hollywoodland", write="write",
           thirteen="Thirteen", fortyfive="fortyfive", bulbs="light bulbs", dollars="Twentyone", life="Planned", nobody="nobody took", apart="falling", y1949="1949", deal="deal saved",
           condition="condition", cut="cut the last", l_="L", famous="famous", realestate="real estate", chopped="chopped", never2="never about#2")
CUE.update({"s%02d" % k: x["_phrase"] for k, x in enumerate(shots) if x["_phrase"] != "0"})
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
