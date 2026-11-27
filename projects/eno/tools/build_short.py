#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 34: the man who invented the stop sign never learned to drive.
usage: build_short.py <project folder>
Eight gilded-traffic sets 70 units apart: HK cobalt-pink dusk crossroads (hook + loop: Eno the horseman, his horse and a giant STOP sign;
StopperText sticker slaps on), NY foggy amber-teal 1867 Broadway (the jam, William age nine, his mother, the policeman), WR mint study,
CH cream-gold marble hall, IN candy-pastel toy roads, FD lilac campus, ST golden-hour stable, SP sky-blue split road (carriage -> car).
Shots 0.7-2 s, every neighbour a different move; the signs and props are the stars. Open loop: HOW?! (a non-driver) -> he was a horseman."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, NY=70, WR=140, CH=210, IN=280, FD=350, ST=420, SP=490)
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


yard("HK", "dusk.png", "asphalt.jpg"); box("HK", 0.0, 0.0, -1.7, [7.0, 0.03, 0.5], color="#f4f0e8"); tree("HK", -3.8, -4.6, 0.8, "#4a6aa0"); tree("HK", 4.4, -4.4, 0.9, "#5a78aa")
yard("NY", "broadway.png", "cobble2.jpg"); post("NY", -1.6, -4.2, 2.4, "#3a2a2a")
yard("WR", "study.png", "mintfl.jpg"); box("WR", 0.0, 0.04, -2.8, [2.0, 0.7, 0.9], color="#8a5a3a")
yard("CH", "marble.png", "marblefl.jpg"); box("CH", 0.0, 0.04, -2.8, [1.3, 0.3, 0.9], color="#c8a050")
yard("IN", "candy.png", "candyfl.jpg"); tree("IN", -4.6, -4.2, 0.8, "#ff8ab0"); tree("IN", 4.8, -4.4, 0.8, "#8ad0ff")
yard("FD", "campus.png", "lilacfl.jpg"); box("FD", -2.2, 0.04, -2.8, [1.0, 0.3, 0.8], color="#7a6aa0")
yard("ST", "stable.png", "hayfl.jpg"); box("ST", 3.4, 0.04, -2.8, [1.0, 0.3, 0.8], color="#a07040"); crate("ST", -3.4, 0.04, -3.6, 0.7)
yard("SP", "splitroad.png", "roadfl.jpg"); box("SP", 0.0, 0.04, -2.8, [0.6, 0.3, 0.6], color="#7a7a90")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("signH", "stopsign", pos("HK", 0.55, 0.04, -2.9), 1.8); human("enoH", "eno", pos("HK", -0.5, 0.04, -2.4), face="happy", h=1.5); put("carH", "car", pos("HK", 3.6, 0.04, -2.8), 0.75)
put("jamN", "jam", pos("NY", 0.0, 0.04, -3.4), 1.5); put("carrN", "carriage", pos("NY", 4.6, 0.04, -3.0), 1.2); human("willy", "willy", pos("NY", 4.0, 0.04, -2.3), face="shocked", h=1.0); human("mom", "mom", pos("NY", 5.1, 0.04, -2.35), face="happy", h=1.5)
human("cop", "cop", pos("NY", -3.6, 0.04, -2.4), face="shocked", h=1.6); put("cal67_", "y1867", pos("NY", -1.6, 2.4, -4.1), 0.8)
put("artW", "article", pos("WR", 0.4, 0.74, -2.8), 1.0); human("enoW", "eno", pos("WR", -0.6, 0.04, -2.3), face="happy", h=1.5)
put("regsC", "regs", pos("CH", 0.0, 0.34, -2.8), 1.4)
put("signI", "stopsign", pos("IN", -2.7, 0.04, -2.8), 1.6); put("owI", "oneway", pos("IN", -0.1, 0.04, -2.8), 1.0); put("circI", "circle", pos("IN", 1.6, 0.04, -3.4), 0.8)
put("trophF", "trophy", pos("FD", -2.2, 0.34, -2.8), 1.15); human("enoF", "eno", pos("FD", -3.3, 0.04, -2.4), face="happy", h=1.5); put("foundF", "found", pos("FD", 1.6, 0.04, -3.4), 1.9)
human("enoS", "eno", pos("ST", 0.2, 0.04, -2.4), face="happy", h=1.5); put("horseS", "horse", pos("ST", -1.0, 0.04, -2.9), 1.2); put("wheelS", "wheel", pos("ST", 3.4, 0.34, -2.8), 1.15)
put("carrP", "carriage", pos("SP", -1.5, 0.04, -2.8), 0.95); put("carP", "car", pos("SP", 1.5, 0.04, -2.8), 0.75); put("regsP", "regs", pos("SP", 0.0, 0.34, -2.8), 0.75)
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
    if not who.startswith("stop"): act(s, at, who, pop=1.25 if (at <= 0.001 and s is shots[0]) else 1)     # every card pops in with an ease-out-back overshoot


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


HOOK = dict(anchor=(0.15, 1.1, -2.9), dist=6.6, yaw=-10, pitch=6)
def STOP(s, face, at=0.0, k=None, shake=None):                 # StopperText: one sticker card, re-placed in every hook shot (no re-pop), escalates by face
    cid = T(s, "stop", at=at, dy=0.31, wf=0.62, hf=0.24); act(s, at, cid, face=face)
    if k: act(s, at, cid, pop=k)
    if shake: act(s, at, cid, shake=shake)
    return cid
# ---- The man who invented the stop sign never learned to drive a car.
s = S("0", "HK", zoom=9, **HOOK); STOP(s, "default", 0.0, k=1.35, shake=0.3); ft(s, "enoH", ["happy", "shocked"]); act(s, 0.0, "signH", shake=0.3); act(s, rel(s, "stop"), "signH", face="wink")
s = S("never learned", "HK", (3.6, 0.5, -2.8), 3.8, 14, pitch=6, yawTo=2, type="macro", dof=dict(focus="carH", blur=0.5)); c = STOP(s, "default"); act(s, 0.8, c, face="esc", pop=1.3, shake=0.3); act(s, rel(s, "car"), "carH", face="x", shake=0.5); snap(s, rel(s, "car"), 9)
s = crane("William Phelps", "ST", (-0.4, 1.0, -2.6), 6.6, -24, -4, 36, 8); STOP(s, "esc"); ft(s, "enoS", ["happy", "smug"])
s = crane("New York 1867", "NY", (0.0, 0.9, -3.2), 7.0, 22, 2, 46, 10); c = STOP(s, "esc"); act(s, 0.4, c, face="wait", pop=1.3, shake=0.4); act(s, rel(s, "1867"), "cal67_", shake=0.4)
s = S("He's nine", "NY", (4.55, 0.85, -2.6), 5.4, -8, pitch=6, zoom=11); c = STOP(s, "wait"); hide(s, 0.6, c); T(s, "age9", at=0.7, dy=0.37, wf=0.4); ft(s, "willy", ["shocked", "nervous"]); ft(s, "mom", ["happy", "nervous"])
s = S("in a traffic", "NY", (0.0, 0.7, -3.4), 5.6, 10, pitch=44, pitchTo=30, type="macro", dof=dict(focus="jamN", blur=0.4)); act(s, rel(s, "jam"), "jamN", shake=0.6); snap(s, rel(s, "jam"), 9)
s = S("Not cars", "HK", (3.6, 0.5, -2.8), 4.2, -6, pitch=5, zoom=-10); act(s, 0.0, "carH", face="x", shake=0.4); T(s, "notcars", at=0.05, dy=0.37, wf=0.5)
s = S("dozen horses", "NY", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="ABOUT A DOZEN", items=["HORSES AND CARRIAGES"]))
# ---- And nobody, not the drivers, not the police, knows how to untangle it. He never forgets it. In 1900, he writes an article demanding real traffic rules.
s = S("And nobody", "NY", (0.0, 0.8, -3.4), 6.0, -14, pitch=12, zoom=5, pan=(8, 0)); act(s, 0.1, "jamN", shake=0.4); cfx(s, 0.3, "question", "jamN", 0.8)
s = S("not the police", "NY", (-3.6, 1.0, -2.4), 4.6, 12, pitch=6, yawTo=-2, dof=dict(focus="cop", blur=0.4)); ft(s, "cop", ["shocked", "confused"]); T(s, "nobody", at=rel(s, "knows"), dy=0.38, wf=0.62); snap(s, rel(s, "police"), 7)
s = S("He never forgets", "NY", (4.0, 0.75, -2.3), 4.0, 6, pitch=14, pitchTo=3, dof=dict(focus="willy", blur=0.4)); hide(s, 0.0, "mom"); hide(s, 0.0, "carrN"); ft(s, "willy", ["nervous", "smug"]); T(s, "y1900", at=rel(s, "1900"), dx=-0.24, dy=0.24, wf=0.26, hf=0.26)
s = crane("he writes an", "WR", (0.0, 1.05, -2.6), 5.8, 22, 4, 34, 8); ft(s, "enoW", ["happy", "smug"])
s = S("real traffic rules", "WR", (0.4, 1.2, -2.8), 3.8, -12, pitch=6, yawTo=4, type="macro", dof=dict(focus="artW", blur=0.5)); act(s, 0.05, "artW", shake=0.4); hide(s, 0.0, "enoW"); T(s, "rulesc", at=rel(s, "rules"), dy=0.38, wf=0.62); snap(s, rel(s, "rules"), 8)
# ---- It leads to New York's first written traffic regulations. Then he keeps going. The stop sign. One-way streets. Traffic circles.
s = crane("It leads to", "CH", (0.0, 1.0, -2.8), 5.4, -22, 2, 36, 8); act(s, rel(s, "leads"), "regsC", shake=0.4)
s = S("written traffic regulations", "CH", (0.0, 1.05, -2.8), 4.2, 8, pitch=6, zoom=12, dof=dict(focus="regsC", blur=0.4)); T(s, "firstc", at=0.05, dy=0.38, wf=0.66)
s = crane("Then he keeps", "IN", (1.75, 0.3, -3.4), 4.4, 20, 2, 56, 22); act(s, 0.2, "circI", shake=0.3)
s = S("The stop sign#2", "IN", (-2.7, 1.0, -2.8), 4.0, -8, pitch=6, zoom=14); act(s, 0.05, "signI", face="wink", shake=0.5); snap(s, 0.15, 8)
s = S("Oneway streets", "IN", (0.75, 0.55, -3.0), 7.8, 8, pitch=26, yawTo=-6, pitchTo=14); act(s, 0.05, "owI", shake=0.5); act(s, rel(s, "circles"), "circI", shake=0.5)
# ---- They call him the father of traffic safety. His foundation, started in 1921, still studies transportation today.
s = S("They call him", "FD", (-2.7, 1.0, -2.6), 4.8, 10, pitch=5, zoom=-9, pan=(-6, 0)); ft(s, "enoF", ["happy", "smug"]); T(s, "father", at=rel(s, "father"), dy=0.37, wf=0.6); act(s, rel(s, "safety"), "trophF", shake=0.4)
s = crane("His foundation", "FD", (1.6, 1.1, -3.4), 6.6, -20, 4, 34, 8); T(s, "y1921", at=rel(s, "1921"), dx=-0.25, dy=0.25, wf=0.26, hf=0.26); act(s, rel(s, "1921"), "foundF", shake=0.4); snap(s, rel(s, "1921"), 8)
s = S("still studies", "FD", (1.6, 1.0, -3.4), 5.6, 6, pitch=14, pitchTo=4); T(s, "today", at=rel(s, "studies"), dy=0.38, wf=0.62)
# ---- You see, Eno didn't need a steering wheel to see the problem. He was a horseman. His rules were written for carriages, and they worked so well that cars simply inherited them.
s = S("You see Eno", "ST", (0.2, 1.1, -2.4), 4.6, -10, pitch=6, zoom=12, dof=dict(focus="enoS", blur=0.4)); ft(s, "enoS", ["smug", "happy"]); hide(s, 0.0, "horseS")
s = S("steering wheel", "ST", (3.4, 0.9, -2.8), 3.8, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="wheelS", blur=0.5)); act(s, rel(s, "wheel") + 0.1, "wheelS", face="x", shake=0.6); snap(s, rel(s, "wheel"), 8)
s = crane("He was a", "ST", (-0.4, 0.9, -2.6), 6.0, 22, -2, 34, 8); T(s, "horsem", at=rel(s, "horseman"), dy=0.37, wf=0.56); show(s, 0.0, "horseS", pos("ST", -1.0, 0.04, -2.9), hop=0); act(s, rel(s, "horseman"), "horseS", shake=0.4); ft(s, "enoS", ["happy", "smug"])
s = S("His rules were", "SP", (-1.5, 0.6, -2.8), 4.4, -8, pitch=6, zoom=11); act(s, 0.1, "carrP", shake=0.3); T(s, "carri", at=rel(s, "carriages"), dy=0.37, wf=0.64)
s = S("and they worked", "SP", (0.0, 0.6, -2.8), 3.0, 4, pitch=6, zoom=12); act(s, 0.1, "regsP", shake=0.4)
s = S("cars simply inherited", "SP", (1.5, 0.5, -2.8), 3.8, -12, pitch=6, yawTo=4, type="macro", dof=dict(focus="carP", blur=0.5)); act(s, rel(s, "inherited"), "carP", shake=0.5); T(s, "inherit", at=0.1, dy=0.38, wf=0.58); snap(s, rel(s, "inherited"), 8)
# ---- So every driver who stops at a stop sign is obeying a man who never drove. A man who started fixing traffic at nine years old, stuck behind a dozen horses.
s = crane("So every driver", "HK", (3.6, 0.5, -2.8), 4.8, 24, 4, 44, 10); act(s, rel(s, "stops"), "carH", face="default", shake=0.3)
s = S("at a stop", "HK", (0.55, 1.5, -2.9), 4.2, 8, pitch=6, zoom=13, dof=dict(focus="signH", blur=0.4)); act(s, 0.1, "signH", face="default", shake=0.4); hide(s, 0.0, "enoH")
s = S("a man who never", "HK", (-0.55, 0.95, -2.4), 4.4, -12, pitch=14, pitchTo=3, dof=dict(focus="enoH", blur=0.4)); show(s, 0.0, "enoH", pos("HK", -0.5, 0.04, -2.4), hop=0); hide(s, 0.0, "signH"); ft(s, "enoH", ["smug", "happy"]); T(s, "neverd", at=rel(s, "drove"), dy=0.38, wf=0.6)
s = S("A man who started", "NY", (4.0, 0.75, -2.3), 4.2, 10, pitch=6, zoom=-9, pan=(6, 0), dof=dict(focus="willy", blur=0.4)); ft(s, "willy", ["smug", "happy"]); T(s, "nineyo", at=rel(s, "nine"), dy=0.38, wf=0.6)
s = crane("nine years old#2", "NY", (0.0, 0.8, -3.4), 6.0, -20, 4, 46, 26); act(s, 0.1, "jamN", shake=0.4)
s = S("dozen horses#2", "HK", zoom=-5, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "signH", pos("HK", 0.55, 0.04, -2.9), hop=0); act(s, 0.0, "signH", face="default"); act(s, 0.6, "signH", face="wink", shake=0.3); ft(s, "enoH", ["happy", "shocked"]); STOP(s, "default", 0.05, k=1)
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
ATM = dict(HK=dict(bokeh=BK(0.5)), NY=dict(dust=D_(28), rays=dict(angle=22, intensity=0.6)), WR=dict(dust=D_(20), rays=dict(angle=26, intensity=0.6)), CH=dict(dust=D_(20), rays=dict(angle=18, intensity=0.7)),
           IN=dict(dust=D_(18), rays=dict(angle=30, intensity=0.5)), FD=dict(dust=D_(20), rays=dict(angle=24, intensity=0.6)), ST=dict(dust=D_(30), rays=dict(angle=16, intensity=0.8)), SP=dict(dust=D_(20), rays=dict(angle=28, intensity=0.5)))
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
MOOD = dict(HK="cobalt", NY="fog67", WR="mint", CH="marble", IN="candy", FD="lilac", ST="golden", SP="split")
light, cur = [{"t": 0, "mood": "cobalt"}], "cobalt"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"cobalt": {"sun": {"azimuth": 220, "elevation": 26, "color": "#ffe0e8", "intensity": 2.7}, "sky": {"top": "#283caa", "horizon": "#ff96be"}, "fill": {"sky": "#f4f2ff", "ground": "#4a4a7a", "intensity": 2.2}},
              "fog67": {"sun": {"azimuth": 120, "elevation": 30, "color": "#ffe6c0", "intensity": 2.5}, "sky": {"top": "#3c7882", "horizon": "#f0be82"}, "fill": {"sky": "#fff6ea", "ground": "#6a5a4a", "intensity": 1.9}},
              "mint": {"sun": {"azimuth": 60, "elevation": 40, "color": "#fffcf4", "intensity": 2.4}, "sky": {"top": "#96dcc8", "horizon": "#f0faf0"}, "fill": {"sky": "#fafffc", "ground": "#6a7a6a", "intensity": 1.6}},
              "marble": {"sun": {"azimuth": 150, "elevation": 42, "color": "#fff8e8", "intensity": 2.4}, "sky": {"top": "#f0dcb4", "horizon": "#fff8e6"}, "fill": {"sky": "#fffaf0", "ground": "#8a7a5a", "intensity": 1.5}},
              "candy": {"sun": {"azimuth": 40, "elevation": 44, "color": "#fffaf8", "intensity": 2.4}, "sky": {"top": "#ffbedc", "horizon": "#bef0ff"}, "fill": {"sky": "#fffaff", "ground": "#8a7a90", "intensity": 1.5}},
              "lilac": {"sun": {"azimuth": 100, "elevation": 38, "color": "#fff6fa", "intensity": 2.4}, "sky": {"top": "#aa96e6", "horizon": "#fae6f5"}, "fill": {"sky": "#fbf8ff", "ground": "#7a6a8a", "intensity": 1.6}},
              "golden": {"sun": {"azimuth": 230, "elevation": 16, "color": "#ffd8a0", "intensity": 2.7}, "sky": {"top": "#ffaa5a", "horizon": "#ffe6aa"}, "fill": {"sky": "#fff4e6", "ground": "#8a6a4a", "intensity": 1.7}},
              "split": {"sun": {"azimuth": 60, "elevation": 40, "color": "#fffcf4", "intensity": 2.4}, "sky": {"top": "#78befa", "horizon": "#e6f6ff"}, "fill": {"sky": "#f8fcff", "ground": "#6a7a7a", "intensity": 1.6}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#e8173c", "paper": ["#f08aa0", "#d86a84"], "dofPx": 8, "particle": "#fff4ec", "bokehColor": "#ffb4c8", "ray": "#fff4e4", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(nobody="And nobody", writes="he writes an", yousee="You see Eno", soevery="So every driver",
           stop1="stop sign", car="car", william="William", y1867="1867", nine="nine", jam="jam", notcars="Not cars", dozen="dozen horses", police="police", forgets="forgets", y1900="1900",
           rules="rules", regs="regulations", keeps="keeps going", stop2="The stop sign#2", oneway="Oneway", circles="circles", father="father", y1921="1921", today="today",
           wheel="wheel", horseman="horseman", carriages="carriages#2", inherited="inherited", stops="stops", stop3="stop sign#3", drove="drove", nine2="nine#2", dozen2="dozen horses#2")
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
