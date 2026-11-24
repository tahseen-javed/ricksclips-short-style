#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 19: the Eiffel Tower was built to be torn down; one wire on top saved it;
then it caught a spy (Mata Hari).
usage: build_short.py <project folder>
Twelve Paris sets 70 units apart: HK indigo night Paris with a wrecking ball (hook + loop), TP navy tower-top with the antenna wire, SY teal
spy-noir alley (trench-coat "?" silhouette = open loop, resolved as Mata Hari), PA champagne 1889 fair, PM sage permit office, AR wine-red
artists' cafe, CL slate demolition yard, PN peach dawn Pantheon, AY blue-morning army camp, RS amber radio room, WR blood-red war night,
EA teal "big ear".  Shots 1-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, TP=70, SY=140, PA=210, PM=280, AR=350, CL=420, PN=490, AY=560, RS=630, WR=700, EA=770)
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


def wcrane(loc, x, z, arm_to): post(loc, x, z, 3.0, "#d8a030"); box(loc, (x + arm_to) / 2, 2.95, z, [abs(arm_to - x) + 0.3, 0.14, 0.14], color="#d8a030")


yard("HK", "nightparis.png", "cobnight.jpg"); wcrane("HK", -2.2, -2.4, -1.2); box("HK", 2.8, 0.04, -2.6, [0.8, 0.5, 0.6], color="#6a5aa0")
yard("TP", "topnight.png", "ironfloor.jpg")
yard("SY", "alley.png", "wetcob.jpg"); post("SY", -1.2, -2.6, 2.6, "#1a2a30"); box("SY", 2.6, 0.04, -2.8, [0.8, 0.9, 0.6], color="#2a4a50")
yard("PA", "fair.png", "fairsand.jpg"); box("PA", -2.8, 0.04, -2.8, [0.9, 0.6, 0.6], color="#e8c070"); tree("PA", -3.4, -4.2, 0.8, "#5a9a5a")
yard("PM", "bureau.png", "parquet.jpg"); table("PM", 0.6, -1.9, 1.2, 0.7, 0.74, "#7a5040"); box("PM", -3.0, 0.04, -3.0, [0.8, 1.2, 0.6], color="#5a7a64")
yard("AR", "cafe.png", "cafefloor.jpg"); box("AR", -2.8, 0.04, -2.6, [0.8, 0.7, 0.8], color="#8a2a3a")
yard("CL", "demolish.png", "rubble.jpg"); wcrane("CL", -2.4, -2.4, -0.6); box("CL", 2.9, 0.04, -2.6, [0.9, 0.4, 0.7], color="#8a8a90")
yard("PN", "dawn.png", "stone.jpg"); tree("PN", -3.2, -3.6, 0.8, "#6aaa6a")
yard("AY", "camp.png", "grass2.jpg"); box("AY", 3.0, 0.04, -3.0, [1.0, 0.6, 0.8], color="#7a7a50")
yard("RS", "valves.png", "walnut.jpg"); table("RS", 0.9, -2.0, 1.4, 0.8, 0.74, "#6a4630"); table("RS", -2.7, -2.2, 1.2, 0.7, 0.74, "#6a4630")
yard("WR", "warnight.png", "redcob.jpg"); box("WR", 2.8, 0.04, -2.8, [0.9, 0.5, 0.7], color="#5a2a3a")
yard("EA", "bigear.png", "tealcob.jpg"); box("EA", -2.9, 0.04, -2.8, [0.8, 0.6, 0.6], color="#2a6a70")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
put("towerH", "tower", pos("HK", 0.4, 0.04, -2.8), 3.2, face="nervous"); put("ballH", "ball", pos("HK", -1.2, 1.5, -2.4), 1.4)
put("t_top", "towertop", pos("TP", 0.0, 0.3, -2.6), 2.8); put("wavesT", "waves", PARK, 0.7)
put("spyS", "spy", pos("SY", 0.5, 0.04, -2.0), 1.8); human("mataS", "mata", PARK, face="smug")
human("eiffelP", "eiffel", pos("PA", -0.8, 0.04, -1.6), face="happy"); put("towerP", "tower", pos("PA", 1.4, 0.04, -3.4), 3.0)
human("eiffelM", "eiffel", pos("PM", -1.0, 0.04, -1.6), face="nervous"); put("permitM", "permit", pos("PM", 0.6, 0.78, -1.9), 0.75)
human("art1", "artist", pos("AR", -0.9, 0.04, -1.6), face="shouting"); human("art2", "artist2", pos("AR", 0.4, 0.04, -1.8), face="shocked"); put("easelA", "easel", pos("AR", 1.5, 0.04, -2.7), 1.4)
put("towerC", "tower", pos("CL", 0.9, 0.04, -3.2), 3.0, face="nervous"); put("ballC", "ball", pos("CL", -0.45, 1.6, -2.4), 1.1); human("bossC", "boss", pos("CL", -1.3, 0.04, -1.8), face="shouting")
put("pantN", "pantheon", pos("PN", 0.5, 0.04, -3.2), 2.4); put("wavesN", "waves", PARK, 0.8)
human("sold1", "soldier", pos("AY", -1.2, 0.04, -1.6), face="happy"); human("sold2", "soldier", pos("AY", 0.0, 0.04, -1.9), face="smug"); human("sold3", "soldier", pos("AY", 1.2, 0.04, -1.7), face="happy")
human("radman", "radioman", pos("RS", -0.8, 0.04, -1.6), face="happy"); put("radioR", "radio", pos("RS", 0.9, 0.78, -2.0), 0.75); put("tapeR", "tape", pos("RS", -2.7, 0.78, -2.2), 0.5)
put("towerW", "tower", pos("WR", 0.3, 0.04, -3.2), 3.0, face="shocked"); human("sold4", "soldier", pos("WR", -1.3, 0.04, -1.8), face="shocked")
put("towerE", "tower", pos("EA", 0.0, 0.04, -2.8), 3.2, face="ear"); put("wavesE", "waves", PARK, 0.7)
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


HOOK = dict(anchor=(0.0, 1.7, -2.6), dist=9.4, yaw=4, pitch=6)
# ---- The Eiffel Tower was built to be torn down. One wire on top saved it. Then it caught a spy.
s = S("0", "HK", zoom=14, pan=(-3, 0), **HOOK); act(s, 0.0, "towerH", shake=0.4); go(s, 0.15, "ballH", pos("HK", -0.75, 1.6, -2.4), 0.6, walk=False); act(s, 0.7, "towerH", face="shocked", shake=0.5)
tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
s = S("built to be", "HK", (0.16, 1.8, -2.6), 9.4, -12, pitch=5, yawTo=6, dof=dict(focus="towerH", blur=0.3)); act(s, 0.05, "towerH", face="shocked", shake=0.6); act(s, 0.1, "ballH", shake=0.4); snap(s, rel(s, "torn"), 8)
s = S("One wire on", "TP", (0.0, 1.6, -2.6), 6.4, 4, pitch=2, pitchTo=16); act(s, 0.1, "t_top", shake=0.4); T(s, "wire"); snap(s, rel(s, "saved"), 12)
s = S("Then it caught", "SY", (0.5, 1.1, -2.0), 5.6, -6, pitch=5, zoom=4, pan=(26, 0)); act(s, 0.1, "spyS", shake=0.4); T(s, "spyc")
# ---- Paris, 1889. Gustave Eiffel gets a permit for just twenty years.
s = crane("Paris 1889", "PA", (0.3, 1.5, -2.4), 9.6, -22, -2, 36, 6); ft(s, "eiffelP", ["happy", "smug"]); T(s, "y1889", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("Gustave Eiffel gets", "PA", (-0.8, 1.2, -1.6), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="eiffelP", blur=0.4)); ft(s, "eiffelP", ["smug", "happy"]); T(s, "eiffelc")
s = S("permit for just", "PM", (0.6, 1.15, -1.9), 2.6, -6, pitch=14, pitchTo=2, type="macro", dof=dict(focus="permitM", blur=0.5)); act(s, 0.1, "permitM", shake=0.4); snap(s, rel(s, "twenty"), 10)
# ---- Famous artists already call his tower "useless and monstrous." After twenty years, the city can take it, and tear it down.
s = crane("Famous artists already", "AR", (0.2, 1.2, -1.9), 9.2, 22, 2, 34, 6); ft(s, "art1", ["shouting", "smug"]); ft(s, "art2", ["shocked", "shouting"]); act(s, 0.1, "easelA", shake=0.3); T(s, "artists")
s = S("his tower useless", "AR", (-0.9, 1.2, -1.6), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="art1", blur=0.4)); ft(s, "art1", ["shouting", "smug"]); act(s, 0.0, "art1", pose=dict(armR=-150)); T(s, "useless"); snap(s, rel(s, "monstrous"), 12); cfx(s, 0.3, "bang", "art1", 0.6)
s = S("After twenty years", "CL", (0.0, 1.5, -2.6), 9.0, -16, pitch=6, yawTo=4); ft(s, "bossC", ["shouting", "smug"]); act(s, 0.1, "ballC", shake=0.3); T(s, "after20")
s = S("and tear it", "CL", (0.5, 1.6, -2.8), 7.4, 8, pitch=6, zoom=-12, _dis=1); hide(s, 0.0, "bossC"); go(s, 0.05, "ballC", pos("CL", 0.1, 1.6, -2.5), 0.5, walk=False); act(s, 0.5, "towerC", face="shocked", shake=0.6); T(s, "tear")
# ---- Eiffel needs a reason. A big one.
s = crane("Eiffel needs a", "PM", (-0.2, 1.2, -1.8), 7.6, -20, 0, 32, 6); ft(s, "eiffelM", ["nervous", "confused"]); c_ = T(s, "reason"); cfx(s, 0.3, "question", "eiffelM", 0.7); swap(s, c_, rel(s, "A big one"), "bigone"); act(s, rel(s, "A big one"), "eiffelM", pose=dict(armR=-150))
# ---- You see, Eiffel turns his tower into a giant antenna. In 1898, a radio signal flies from the top to the Pantheon, four kilometers away.
s = crane("You see Eiffel", "TP", (0.0, 1.6, -2.6), 7.0, 20, 0, 34, 6); act(s, 0.1, "t_top", shake=0.4)
s = S("into a giant", "TP", (0.0, 2.6, -2.6), 4.2, -6, pitch=4, zoom=12, type="macro", dof=dict(focus="t_top", blur=0.4)); act(s, 0.1, "t_top", shake=0.4); T(s, "antenna"); snap(s, rel(s, "antenna"), 12)
s = S("In 1898", "TP", (0.2, 1.8, -2.6), 7.6, -14, pitch=5, yawTo=4); show(s, 0.1, "wavesT", pos("TP", 0.5, 2.6, -2.2)); T(s, "y1898", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("a radio signal", "TP", (0.2, 2.0, -2.6), 7.4, 6, pitch=5, zoom=4, pan=(20, 0)); go(s, 0.05, "wavesT", pos("TP", 0.8, 2.9, -2.2), 0.8, walk=False); act(s, 0.1, "t_top", shake=0.3)
s = crane("to the Panthon", "PN", (0.3, 1.3, -3.0), 9.0, 22, 2, 30, 6); show(s, 0.1, "wavesN", pos("PN", -1.4, 2.3, -2.6)); act(s, 0.3, "pantN", shake=0.4); T(s, "pantc")
s = S("four kilometers away", "PN", (0.0, 2.0, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="KILOMETERS AWAY", items=["4"]))
# ---- The army moves in. A permanent radio station follows. And Paris renews his permit for seventy more years.
s = crane("The army moves", "AY", (0.0, 1.2, -1.8), 9.0, -22, -2, 36, 6); ft(s, "sold1", ["happy", "smug"]); ft(s, "sold2", ["smug", "happy"]); ft(s, "sold3", ["happy", "shouting"]); T(s, "army"); snap(s, 0.3, 12)
s = S("A permanent radio", "RS", (0.9, 1.05, -2.0), 3.6, 10, pitch=4, zoom=12, type="macro", dof=dict(focus="radioR", blur=0.5)); act(s, 0.1, "radioR", shake=0.3); T(s, "station")
s = S("And Paris renews", "PM", (-0.2, 1.2, -1.8), 6.6, 16, pitch=5, yawTo=-2); act(s, 0.2, "permitM", shake=0.4); ft(s, "eiffelM", ["happy", "smug"]); cfx(s, 0.4, "blush", "eiffelM", 0.7)
s = S("for seventy more", "PM", (0.6, 1.15, -1.9), 2.8, 8, pitch=4, zoom=14, type="macro", dof=dict(focus="permitM", blur=0.5)); act(s, 0.1, "permitM", face="renewed", shake=0.5); T(s, "plus70"); snap(s, rel(s, "seventy"), 12)
# ---- Then war comes. The tower listens to enemy radio. They call it "the big ear." It intercepts messages about a secret agent, code name H-21.
s = crane("Then war comes", "WR", (-0.4, 1.5, -2.6), 9.0, 20, 0, 30, 6); act(s, 0.1, "towerW", shake=0.4); ft(s, "sold4", ["shocked", "nervous"]); T(s, "war")
s = S("The tower listens", "EA", (0.0, 1.7, -2.8), 7.6, -8, pitch=5, zoom=12); show(s, 0.1, "wavesE", pos("EA", -0.9, 2.6, -2.4)); T(s, "listens")
s = S("They call it", "EA", (0.0, 1.6, -2.8), 8.2, -16, pitch=5, yawTo=4); act(s, 0.1, "towerE", shake=0.4); T(s, "bigear"); snap(s, rel(s, "ear"), 12)
s = S("It intercepts messages", "RS", (-2.7, 1.0, -2.2), 2.8, 8, pitch=14, pitchTo=2, type="macro", dof=dict(focus="tapeR", blur=0.5)); act(s, 0.1, "tapeR", shake=0.4); T(s, "intercept")
s = crane("a secret agent", "SY", (0.3, 1.1, -2.0), 7.6, -20, 0, 32, 6); act(s, 0.1, "spyS", shake=0.3); T(s, "h21")
s = S("code name", "SY", (0.5, 1.0, -2.0), 5.6, -14, pitch=5, yawTo=4); act(s, 0.1, "spyS", shake=0.4); cfx(s, 0.2, "question", "spyS", 0.7)
# ---- Her real name? Mata Hari.
s = S("Her real name", "SY", (0.5, 1.0, -2.0), 4.6, 10, pitch=5, zoom=12, dof=dict(focus="spyS", blur=0.4)); act(s, 0.1, "spyS", shake=0.4); T(s, "realname")
s = S("Mata Hari", "SY", (0.5, 1.0, -2.0), 4.2, -8, pitch=5, zoom=-10); hide(s, 0.0, "spyS"); show(s, 0.02, "mataS", pos("SY", 0.5, 0.04, -2.0)); ft(s, "mataS", ["smug", "happy"]); T(s, "matac"); snap(s, 0.3, 12); cfx(s, 0.3, "glint", "mataS", 0.7)
# ---- Not bad for a tower that was built to be torn down. (pull-out onto the hook frame)
s = S("Not bad for", "PA", (0.3, 1.5, -2.4), 9.6, 16, pitch=6, yawTo=-2); ft(s, "eiffelP", ["smug", "happy"]); act(s, 0.1, "towerP", shake=0.3); T(s, "notbad")
s = S("built to be#2", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "ballH", pos("HK", -1.0, 1.6, -2.4), hop=0); act(s, 0.0, "towerH", face="nervous", shake=0.4)
go(s, 0.2, "ballH", pos("HK", -0.75, 1.6, -2.4), 0.6, walk=False); tag(s, 0.05, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
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
ATM = dict(HK=dict(bokeh=BK(0.4)), TP=dict(bokeh=BK(0.45)), SY=dict(bokeh=BK(0.4)), PA=dict(dust=D_(24), rays=dict(angle=30, intensity=0.55)), PM=dict(dust=D_(20), rays=dict(angle=24, intensity=0.5)),
           AR=dict(dust=D_(20)), CL=dict(dust=D_(44)), PN=dict(dust=D_(18), rays=dict(angle=16, intensity=0.6)), AY=dict(dust=D_(22), rays=dict(angle=34, intensity=0.5)), RS=dict(dust=D_(24)),
           WR=dict(bokeh=BK(0.4)), EA=dict(bokeh=BK(0.45)))
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
MOOD = dict(HK="parisnight", TP="topnight", SY="noir", PA="champagne", PM="sage", AR="wine", CL="slate", PN="peach", AY="bluemorning", RS="amber", WR="warred", EA="tealear")
light, cur = [{"t": 0, "mood": "parisnight"}], "parisnight"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 19,
    "moods": {"parisnight": {"sun": {"azimuth": 150, "elevation": 35, "color": "#d8d0ff", "intensity": 2.6}, "sky": {"top": "#28287a", "horizon": "#6e5ab4"}, "fill": {"sky": "#c8c0ff", "ground": "#504870", "intensity": 2.0}},
              "topnight": {"sun": {"azimuth": 30, "elevation": 30, "color": "#c8f0ff", "intensity": 2.6}, "sky": {"top": "#141e5a", "horizon": "#3c46a0"}, "fill": {"sky": "#a8e0ff", "ground": "#3c4070", "intensity": 2.1}},
              "noir": {"sun": {"azimuth": -40, "elevation": 35, "color": "#ffe0c0", "intensity": 2.5}, "sky": {"top": "#145a64", "horizon": "#3c8c8c"}, "fill": {"sky": "#c0fff0", "ground": "#304a50", "intensity": 2.0}},
              "champagne": {"sun": {"azimuth": 40, "elevation": 35, "color": "#fff0c8", "intensity": 2.4}, "sky": {"top": "#f0c070", "horizon": "#fff0c0"}, "fill": {"sky": "#fff0d0", "ground": "#907050", "intensity": 1.45}},
              "sage": {"sun": {"azimuth": 20, "elevation": 40, "color": "#fff8e0", "intensity": 2.4}, "sky": {"top": "#78aa8c", "horizon": "#b4d6ba"}, "fill": {"sky": "#e8fff0", "ground": "#6a5040", "intensity": 1.6}},
              "wine": {"sun": {"azimuth": -20, "elevation": 40, "color": "#ffd8b0", "intensity": 2.5}, "sky": {"top": "#962a3c", "horizon": "#c85a5a"}, "fill": {"sky": "#ffd0c0", "ground": "#5a2a30", "intensity": 1.85}},
              "slate": {"sun": {"azimuth": 30, "elevation": 35, "color": "#ffe0c0", "intensity": 2.4}, "sky": {"top": "#5a6482", "horizon": "#9aa0b4"}, "fill": {"sky": "#e0e4f0", "ground": "#605a5a", "intensity": 1.8}},
              "peach": {"sun": {"azimuth": 200, "elevation": 14, "color": "#ffc8a0", "intensity": 2.5}, "sky": {"top": "#ffa090", "horizon": "#ffe0c8"}, "fill": {"sky": "#ffe0d0", "ground": "#806a5a", "intensity": 1.5}},
              "bluemorning": {"sun": {"azimuth": 50, "elevation": 45, "color": "#fffbe8", "intensity": 2.4}, "sky": {"top": "#5aa0e6", "horizon": "#c8e2fa"}, "fill": {"sky": "#e8f4ff", "ground": "#6a7050", "intensity": 1.4}},
              "amber": {"sun": {"azimuth": 20, "elevation": 40, "color": "#ffc888", "intensity": 2.5}, "sky": {"top": "#5a3c28", "horizon": "#966440"}, "fill": {"sky": "#ffd8a8", "ground": "#503828", "intensity": 2.0}},
              "warred": {"sun": {"azimuth": -30, "elevation": 30, "color": "#ffc0a0", "intensity": 2.6}, "sky": {"top": "#781e32", "horizon": "#c85046"}, "fill": {"sky": "#ffc8c0", "ground": "#502830", "intensity": 2.0}},
              "tealear": {"sun": {"azimuth": 40, "elevation": 35, "color": "#e8fff8", "intensity": 2.5}, "sky": {"top": "#14646e", "horizon": "#46aaaa"}, "fill": {"sky": "#d0fff8", "ground": "#305a60", "intensity": 1.95}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ffcf3c", "paper": ["#b89ae0", "#9a78cc"], "dofPx": 8, "particle": "#fff4d8", "bokehColor": "#c8b8ff", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(paris="Paris 1889", yousee="You see Eiffel", war="Then war comes", notbad="Not bad for", tear="and tear it", monst="monstrous", signal="a radio signal", army="The army moves",
           seventy="seventy", listens="The tower listens", ear="ear", intercepts="It intercepts", mata="Mata Hari", wire="One wire on", spy="spy", reason="Eiffel needs a", bigone="A big one",
           saved="saved", antenna="antenna", y1898="In 1898", pant="to the Panthon")
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
