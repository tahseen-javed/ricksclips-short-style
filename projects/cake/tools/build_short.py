#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 23: German chocolate cake isn't German - named after Sam German, born in Texas.
usage: build_short.py <project folder>
Eleven cocoa-cherry + Texas-turquoise sets 70 units apart: HK Texas sunset (hook + loop; a "HELLO MY NAME IS ?" tag = open loop, resolved
"GERMAN"), FA gaslit 1850s chocolate works, BR cocoa velvet macro studio (3 pedestals), TX 1957 ranch kitchen, NP Dallas press hall,
SU lemon suburb, GF navy-gold boardroom, MP midnight map room, SL emerald sales board, TY plum writer's desk, GE rose-sepia travel poster.
Shots 0.8-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, FA=70, BR=140, TX=210, NP=280, SU=350, GF=420, MP=490, SL=560, TY=630, GE=700)
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


def table(loc, x, z, w=1.6, d=0.8, h=0.7, col="#8a5a3a"): box(loc, x, 0.04, z, [w, h, d], color=col)


yard("HK", "texas.png", "desert.jpg"); table("HK", 0.0, -2.2, 1.6, 0.9, 0.7, "#f0a040"); box("HK", -3.0, 0.04, -1.6, [0.7, 0.5, 0.6], color="#c86a4a")
yard("FA", "works.png", "mahog.jpg"); table("FA", -1.4, -2.1, 0.9, 0.7, 0.74, "#5a3020")
yard("BR", "studio.png", "velvet.jpg"); box("BR", -2.6, 0.04, -2.4, [0.9, 0.6, 0.7], color="#b84050"); box("BR", 0.0, 0.04, -2.2, [1.4, 0.56, 0.8], color="#e8d0a0"); box("BR", 2.8, 0.04, -2.4, [1.3, 0.5, 0.9], color="#40b0b0")
yard("TX", "ranch.png", "lino.jpg"); table("TX", 0.9, -1.9, 1.2, 0.7, 0.74, "#f04050")
yard("NP", "press.png", "steel.jpg"); box("NP", 0.0, 0.04, -2.4, [1.8, 0.4, 0.5], color="#ff9640")
yard("SU", "suburb.png", "lawn.jpg"); box("SU", -3.0, 0.04, -1.6, [0.6, 0.5, 0.6], color="#ffd23c"); box("SU", 3.0, 0.04, -1.6, [0.6, 0.5, 0.6], color="#28c8c8")
yard("GF", "board.png", "carpet.jpg"); table("GF", 0.9, -1.9, 1.2, 0.7, 0.74, "#9a6a48")
yard("MP", "maproom.png", "grid.jpg"); box("MP", 0.0, 0.04, -2.45, [2.6, 0.12, 0.3], color="#2a3a8a")
yard("SL", "sales.png", "emer.jpg"); box("SL", -2.6, 0.04, -2.2, [0.6, 0.6, 0.6], color="#ffd246")
yard("TY", "desk.png", "wood.jpg"); table("TY", 0.0, -2.2, 1.6, 0.8, 0.74, "#6a3a2a")
yard("GE", "poster.png", "sepia.jpg"); box("GE", 0.0, 0.04, -2.4, [0.8, 0.5, 0.6], color="#8a5aa0")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
put("cakeH", "cake", pos("HK", 0.0, 0.74, -2.2), 1.2, face="shocked"); put("ntag_H", "ntag", pos("HK", -0.45, 0.74, -1.85), 0.3); put("starH", "tstar", pos("HK", 1.25, 0.04, -2.6), 0.8)
human("samF", "samg", pos("FA", -0.3, 0.04, -1.8), face="happy"); put("kettleF", "kettle", pos("FA", 1.2, 0.04, -2.6), 1.1); put("barF", "bar", pos("FA", -1.4, 0.78, -2.1), 0.36)
put("tagB", "ntag", pos("BR", -2.6, 0.64, -2.4), 0.6); put("barB", "bar", pos("BR", 0.0, 0.6, -2.2), 0.62); put("cakeB", "cake", pos("BR", 2.8, 0.54, -2.4), 1.1)
human("momT", "texmom", pos("TX", -0.7, 0.04, -1.8), face="happy"); put("recipeT", "recipe", pos("TX", 0.9, 0.78, -1.9), 0.45)
put("newsN", "news", pos("NP", 0.0, 0.44, -2.4), 1.1)
human("r1S", "rdr1", pos("SU", -1.0, 0.04, -1.9), face="happy"); human("r2S", "rdr2", pos("SU", 0.0, 0.04, -2.0), face="happy"); human("r3S", "rdr3", pos("SU", 1.0, 0.04, -1.9), face="happy")
human("execG", "gfexec", pos("GF", -0.6, 0.04, -1.7), face="smug"); put("recipeG", "recipe", pos("GF", 0.9, 0.78, -1.9), 0.42)
put("mapM", "usmap", pos("MP", 0.0, 0.16, -2.4), 1.55)
put("stackS", "stack", pos("SL", 0.0, 0.04, -2.4), 2.0)
put("typerY", "typer", pos("TY", 0.0, 0.78, -2.2), 0.85)
put("globeG", "globe", pos("GE", 0.0, 0.54, -2.4), 1.3)
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


HOOK = dict(anchor=(0.0, 1.2, -2.1), dist=4.6, yaw=4, pitch=6)
# ---- German chocolate cake isn't German. It's named after a man called German, and it was born in Texas.
s = S("0", "HK", zoom=10, **HOOK); act(s, 0.0, "cakeH", face="shocked", shake=0.5); hide(s, 0.0, "starH"); tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24); act(s, 1.0, "cakeH", face="sad", shake=0.3); snap(s, rel(s, "isn't"), 10)
s = S("It's named after", "BR", (-2.6, 0.92, -2.4), 2.9, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="tagB", blur=0.5)); act(s, 0.05, "tagB", shake=0.5); T(s, "manc", at=rel(s, "man"))
s = crane("and it was", "HK", (0.3, 1.1, -2.3), 7.0, 22, 2, 36, 8); act(s, 0.05, "cakeH", face="default"); show(s, rel(s, "Texas"), "starH", pos("HK", 1.25, 0.04, -2.6)); T(s, "texc", at=rel(s, "born"))
# ---- In the 1850s, a chocolate maker named Sam German created a sweet baking bar for the Baker's Chocolate Company. They named it after him: German's Sweet Chocolate.
s = S("In the 1850s", "FA", (-0.1, 1.1, -2.2), 9.4, -6, pitch=6, zoom=4, pan=(8, 0)); act(s, 0.1, "kettleF", shake=0.4); ft(s, "samF", ["happy", "smug"]); T(s, "y1850", dy=0.28)
s = S("named Sam German", "FA", (-0.3, 1.25, -1.8), 4.6, 10, pitch=5, zoom=12, dof=dict(focus="samF", blur=0.4)); hide(s, 0.0, "kettleF"); hide(s, 0.0, "barF"); ft(s, "samF", ["shocked", "happy"]); act(s, 0.05, "samF", pose=dict(armR=-150)); T(s, "samc"); snap(s, rel(s, "Sam"), 8); cfx(s, 0.5, "blush", "samF", 0.6)
s = S("a sweet baking", "BR", (0.0, 0.92, -2.2), 3.6, -16, pitch=6, yawTo=6, type="macro", dof=dict(focus="barB", blur=0.5)); act(s, 0.05, "barB", shake=0.5)
s = S("the Baker's Chocolate", "FA", (-0.1, 1.1, -2.2), 8.6, 6, pitch=5, zoom=-10); show(s, 0.05, "kettleF", pos("FA", 1.2, 0.04, -2.6)); show(s, 0.15, "barF", pos("FA", -1.4, 0.78, -2.1)); ft(s, "samF", ["happy", "smug"]); T(s, "bakers")
s = S("They named it", "FA", (-0.9, 1.0, -1.95), 5.4, -14, pitch=12, pitchTo=3); hide(s, 0.0, "kettleF"); ft(s, "samF", ["smug", "happy"]); act(s, 0.1, "samF", pose=dict(armR=-150)); act(s, 0.2, "barF", shake=0.4); T(s, "named", at=rel(s, "named"))
s = S("German's Sweet Chocolate", "BR", (0.0, 0.92, -2.2), 3.8, 4, pitch=6, zoom=14, type="macro", dof=dict(focus="barB", blur=0.5)); act(s, 0.05, "barB", shake=0.6)
# ---- A century later, in 1957, a Texas homemaker sent her cake recipe, made with that bar, to a Dallas newspaper.
s = crane("A century later", "TX", (0.0, 1.1, -2.0), 8.4, -22, -2, 38, 8); ft(s, "momT", ["happy", "smug"]); act(s, 0.1, "recipeT", shake=0.3)
s = S("in 1957", "TX", (0.1, 1.15, -1.9), 6.4, 12, pitch=5, zoom=12); T(s, "y1957", dy=0.2, dx=0.17, wf=0.32, hf=0.34); ft(s, "momT", ["smug", "happy"])
s = S("a Texas homemaker", "TX", (-0.7, 1.25, -1.8), 4.6, 14, pitch=5, yawTo=-4, dof=dict(focus="momT", blur=0.4)); ft(s, "momT", ["happy", "shocked"]); T(s, "homec"); snap(s, rel(s, "homemaker"), 8); cfx(s, 0.5, "blush", "momT", 0.6)
s = S("recipe made with", "TX", (0.9, 1.0, -1.9), 2.6, -6, pitch=14, pitchTo=2, type="macro", dof=dict(focus="recipeT", blur=0.5)); act(s, 0.05, "recipeT", shake=0.5)
s = S("to a Dallas", "NP", (0.0, 1.2, -2.4), 5.2, 8, pitch=6, zoom=14); act(s, 0.05, "newsN", shake=0.6); T(s, "dallas", at=rel(s, "Dallas"))
# ---- You see, readers went crazy for it. General Foods, which owned Baker's, sent the recipe to newspapers across the country. Sales of German's chocolate jumped 73 percent in one year.
s = S("You see readers", "SU", (0.0, 1.0, -1.95), 7.4, -4, pitch=5, zoom=-12); ft(s, "r1S", ["happy", "shocked"]); ft(s, "r2S", ["shocked", "happy"]); ft(s, "r3S", ["happy", "shouting"])
for k, w_ in enumerate(("r1S", "r2S", "r3S")): act(s, 0.2 + 0.15 * k, w_, pose=dict(armR=-150), shake=0.4)
T(s, "crazy", at=rel(s, "crazy")); snap(s, rel(s, "crazy"), 10); cfx(s, rel(s, "crazy") + 0.1, "bang", "r2S", 0.5)
s = S("General Foods which", "GF", (-0.1, 1.2, -1.8), 6.6, 16, pitch=5, yawTo=-4); ft(s, "execG", ["smug", "happy"]); act(s, 0.2, "recipeG", shake=0.4); T(s, "gfc")
s = crane("sent the recipe", "MP", (0.0, 0.95, -2.4), 7.6, 18, 4, 36, 8); act(s, 0.05, "mapM", shake=0.3)
s = S("newspapers across the", "MP", (0.0, 0.95, -2.4), 7.4, -6, pitch=5, zoom=8); act(s, 0.05, "mapM", face="p1", shake=0.5); T(s, "across", at=rel(s, "across"))
s = S("Sales of German's", "SL", (0.0, 1.2, -2.4), 7.0, -8, pitch=2, pitchTo=12); act(s, 0.05, "stackS", shake=0.5); snap(s, 0.3, 8)
s = S("jumped 73 percent", "SL", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="SALES JUMPED", items=["+73%"]))
# ---- Then the recipes quietly dropped the apostrophe and the "s." German's chocolate cake became German chocolate cake, and America assumed it came from Germany.
s = S("Then the recipes", "TY", (0.0, 1.15, -2.2), 4.2, 6, pitch=6, zoom=12); act(s, 0.05, "typerY", shake=0.4); T(s, "quietly", at=rel(s, "quietly"))
s = S("apostrophe and the", "TY", (0.0, 1.15, -2.2), 3.0, -14, pitch=6, yawTo=6, type="macro", dof=dict(focus="typerY", blur=0.5)); act(s, rel(s, "and") + 0.3, "typerY", face="b", shake=0.6); snap(s, rel(s, "and") + 0.34, 8)
s = S("German's chocolate cake", "BR", (2.8, 1.1, -2.4), 4.6, 4, pitch=6, zoom=-10); act(s, 0.05, "cakeB", shake=0.4); T(s, "gsc")
s = S("became German chocolate", "BR", (2.8, 1.1, -2.4), 3.8, -14, pitch=5, yawTo=4, dof=dict(focus="cakeB", blur=0.4)); act(s, rel(s, "German"), "cakeB", face="shocked", shake=0.6); T(s, "gcc", at=rel(s, "German"))
s = crane("and America assumed", "GE", (0.0, 1.2, -2.4), 7.0, -22, -2, 36, 8); act(s, 0.1, "globeG", shake=0.4); T(s, "fromde", at=rel(s, "came"))
# ---- So the most German-sounding cake in America is pure Texas. And the only German in German chocolate cake is a man's last name.
s = S("So the most", "HK", (0.0, 1.2, -2.2), 5.6, 10, pitch=5, zoom=4, pan=(-6, 0)); hide(s, 0.0, "starH"); act(s, 0.05, "cakeH", face="tex", shake=0.5)
s = S("is pure Texas", "HK", (1.25, 0.5, -2.6), 3.2, -8, pitch=6, zoom=14, type="macro", dof=dict(focus="starH", blur=0.5)); show(s, 0.02, "starH", pos("HK", 1.25, 0.04, -2.6)); act(s, 0.1, "starH", shake=0.6); T(s, "puretx"); snap(s, 0.15, 8)
s = S("And the only", "BR", (-2.6, 0.92, -2.4), 2.9, 12, pitch=6, yawTo=-6, type="macro", dof=dict(focus="tagB", blur=0.5)); act(s, rel(s, "German"), "tagB", face="g", shake=0.6)
s = S("is a man's", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.0, "ntag_H", face="g"); hide(s, 0.0, "starH"); act(s, 0.05, "cakeH", face="shocked", shake=0.3); T(s, "lastn", at=0.1)
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
ATM = dict(HK=dict(dust=D_(26), rays=dict(angle=28, intensity=0.6)), FA=dict(bokeh=BK(0.45)), BR=dict(bokeh=BK(0.5)), TX=dict(dust=D_(24), rays=dict(angle=24, intensity=0.5)),
           NP=dict(dust=D_(30)), SU=dict(dust=D_(20), rays=dict(angle=32, intensity=0.5)), GF=dict(bokeh=BK(0.4)), MP=dict(bokeh=BK(0.45)), SL=dict(dust=D_(24)),
           TY=dict(bokeh=BK(0.4)), GE=dict(dust=D_(22), rays=dict(angle=30, intensity=0.6)))
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
MOOD = dict(HK="sunsettx", FA="gaslit", BR="cocoa", TX="ranch", NP="pressteal", SU="suburb", GF="navygold", MP="midnight", SL="emerald", TY="plum", GE="poster")
light, cur = [{"t": 0, "mood": "sunsettx"}], "sunsettx"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"sunsettx": {"sun": {"azimuth": 220, "elevation": 20, "color": "#ffe0b0", "intensity": 2.6}, "sky": {"top": "#28bec8", "horizon": "#ff9a50"}, "fill": {"sky": "#fff0e0", "ground": "#8a5a40", "intensity": 1.6}},
              "gaslit": {"sun": {"azimuth": 160, "elevation": 32, "color": "#ffd8a8", "intensity": 2.6}, "sky": {"top": "#5a2a50", "horizon": "#b46a50"}, "fill": {"sky": "#f8e0ff", "ground": "#5a3a30", "intensity": 2.0}},
              "cocoa": {"sun": {"azimuth": 30, "elevation": 40, "color": "#fff0e0", "intensity": 2.6}, "sky": {"top": "#4a2a22", "horizon": "#a0624a"}, "fill": {"sky": "#fff0e8", "ground": "#5a3a30", "intensity": 2.0}},
              "ranch": {"sun": {"azimuth": 40, "elevation": 42, "color": "#fff6e0", "intensity": 2.3}, "sky": {"top": "#50d2d2", "horizon": "#b4f0ea"}, "fill": {"sky": "#f0fffc", "ground": "#7a6a60", "intensity": 1.4}},
              "pressteal": {"sun": {"azimuth": -20, "elevation": 38, "color": "#fff0d8", "intensity": 2.5}, "sky": {"top": "#28646e", "horizon": "#5aa0a0"}, "fill": {"sky": "#e8fff8", "ground": "#4a5a5a", "intensity": 1.9}},
              "suburb": {"sun": {"azimuth": 30, "elevation": 48, "color": "#fffbe8", "intensity": 2.3}, "sky": {"top": "#78c8fa", "horizon": "#fff096"}, "fill": {"sky": "#fffcf0", "ground": "#6a8a5a", "intensity": 1.3}},
              "navygold": {"sun": {"azimuth": 200, "elevation": 24, "color": "#ffd890", "intensity": 2.6}, "sky": {"top": "#1e2a5a", "horizon": "#ffb46e"}, "fill": {"sky": "#e8ecff", "ground": "#4a3a40", "intensity": 2.0}},
              "midnight": {"sun": {"azimuth": 10, "elevation": 40, "color": "#e0ecff", "intensity": 2.6}, "sky": {"top": "#0e143c", "horizon": "#283c82"}, "fill": {"sky": "#e0e8ff", "ground": "#30386a", "intensity": 2.1}},
              "emerald": {"sun": {"azimuth": 40, "elevation": 40, "color": "#f8fff0", "intensity": 2.4}, "sky": {"top": "#146e50", "horizon": "#50be82"}, "fill": {"sky": "#f0fff4", "ground": "#3a5a48", "intensity": 1.7}},
              "plum": {"sun": {"azimuth": 150, "elevation": 34, "color": "#ffe0b8", "intensity": 2.6}, "sky": {"top": "#50285a", "horizon": "#8c5082"}, "fill": {"sky": "#fff0f8", "ground": "#5a3a48", "intensity": 2.0}},
              "poster": {"sun": {"azimuth": 210, "elevation": 26, "color": "#fff0e0", "intensity": 2.4}, "sky": {"top": "#f08c96", "horizon": "#ffdcb4"}, "fill": {"sky": "#fff4f0", "ground": "#8a6a7a", "intensity": 1.5}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff3b4e", "paper": ["#d98a6a", "#b86a4e"], "dofPx": 8, "particle": "#fff0d8", "bokehColor": "#ffc8a0", "ray": "#fff1c8", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(y1850="In the 1850s", century="A century later", tick2="Then the recipes", fin="So the most",
           texas="born in Texas", sam="Sam German", bar="sweet baking bar", named="They named it", y1957="1957", recipe="cake recipe", dallas="Dallas newspaper", crazy="crazy",
           gf="General Foods", news="newspapers across", jumped="jumped", quietly="quietly", apos="apostrophe", became="became", germany="from Germany", pure="pure Texas", lastn="last name")
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
