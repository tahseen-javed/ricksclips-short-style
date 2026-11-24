#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 20: the 1904 Olympic marathon - the first man across the line rode in a car,
the winner ran on rat poison, and the poison was legal.
usage: build_short.py <project folder>
Twelve sun-scorched 1904 sets 70 units apart: HK turquoise stadium finish (hook + loop, "?" driver = open loop -> Fred Lorz), SL ivory World's
Fair, ST mustard start road, HT blazing heat, SU plum office, WS peach mile-12 water stop, DG lime cornfield chase, OR emerald orchard,
CR violet country road, DQ red-striped judges tent, TR chartreuse poison aid station, RB violet rules archive. Shots 1-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, SL=70, ST=140, HT=210, SU=280, WS=350, DG=420, OR=490, CR=560, DQ=630, TR=700, RB=770)
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


yard("HK", "finish.png", "claytrack.jpg"); post("HK", -2.6, -2.8, 2.4, "#f4f0e8"); post("HK", 2.7, -2.9, 2.4, "#f4f0e8"); box("HK", -3.2, 0.04, -1.2, [0.6, 0.5, 0.6], color="#e07a3a")
yard("SL", "fair.png", "pavefair.jpg"); tree("SL", -3.0, -3.6, 0.9, "#5aa86a"); tree("SL", 3.1, -3.8, 0.9, "#5aa86a"); post("SL", -1.9, -3.0, 2.2, "#e8d8b8")
yard("ST", "road.png", "dirt.jpg"); post("ST", -2.8, -2.6, 1.0, "#9a6a40"); post("ST", 2.9, -2.6, 1.0, "#9a6a40"); box("ST", 3.2, 0.04, -1.4, [0.6, 0.4, 0.5], color="#c89a50")
yard("HT", "heat.png", "cracked.jpg"); box("HT", -3.0, 0.04, -2.6, [0.9, 0.3, 0.7], color="#c8784a"); tree("HT", 3.2, -3.4, 0.7, "#8a8a40")
yard("SU", "office.png", "carpetplum.jpg"); table("SU", 0.8, -1.9, 1.2, 0.7, 0.74, "#7a4a3a"); box("SU", -3.0, 0.04, -3.0, [0.8, 1.2, 0.6], color="#8a5a70")
yard("WS", "waterstop.png", "dirt2.jpg"); box("WS", 2.8, 0.04, -2.8, [0.8, 0.4, 0.6], color="#c88a50"); post("WS", -2.8, -3.0, 1.2, "#9a6a40")
yard("DG", "corn.png", "dirt3.jpg"); post("DG", 2.9, -2.8, 1.1, "#9a6a40"); box("DG", -3.0, 0.04, -2.6, [0.8, 0.6, 0.6], color="#c8a050")
yard("OR", "orchard.png", "grass.jpg"); box("OR", 0.9, 0.04, -2.0, [0.7, 0.6, 0.6], color="#b07840"); tree("OR", -3.2, -3.4, 1.0, "#4a9a5a"); tree("OR", 3.3, -3.6, 1.0, "#4a9a5a")
yard("CR", "carroad.png", "roadtex.jpg"); post("CR", 3.0, -2.8, 2.2, "#4a3a3a"); box("CR", -3.2, 0.04, -1.4, [0.6, 0.4, 0.6], color="#9a8a70")
yard("DQ", "judges.png", "boards.jpg"); table("DQ", 1.9, -2.3, 1.2, 0.7, 0.74, "#8a5a3a"); box("DQ", -3.0, 0.04, -2.8, [0.8, 0.9, 0.6], color="#a83a46")
yard("TR", "aid.png", "aidfloor.jpg"); table("TR", 1.8, -2.2, 1.4, 0.8, 0.74, "#6a5a30"); table("TR", -2.6, -2.2, 1.0, 0.7, 0.74, "#6a5a30")
yard("RB", "archive.png", "library.jpg"); table("RB", -0.2, -2.0, 1.4, 0.8, 0.74, "#5a3a4a"); table("RB", 2.6, -2.3, 1.6, 0.8, 0.74, "#5a3a4a")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
put("tape_H", "ftape", pos("HK", 0.0, 0.04, -2.6), 1.3); put("carH", "car", pos("HK", -0.4, 0.04, -1.8), 1.2, face="mystery"); human("hicksH", "hicks", pos("HK", 1.0, 0.04, -2.0), face="nervous"); human("lorzH", "lorz", PARK, face="happy")
put("pack_L", "pack", pos("SL", 0.0, 0.04, -2.4), 0.9)
put("pack_S", "pack", pos("ST", 0.0, 0.04, -2.2), 1.2)
put("sunT", "sun", pos("HT", 0.0, 1.4, -3.2), 2.4, face="angry"); put("thermoT", "thermo", pos("HT", 1.4, 0.04, -2.0), 1.5); put("pack_T", "pack", PARK, 1.0, face="drop")
human("sullyU", "sullivan", pos("SU", -0.6, 0.04, -1.7), face="smug")
put("barrelW", "barrel", pos("WS", 0.4, 0.04, -2.2), 1.0); put("mile12", "mile12", pos("WS", -0.9, 0.04, -2.0), 1.5)
human("tauD", "tau", pos("DG", 0.3, 0.04, -1.8), face="shocked"); put("dogD", "dog", pos("DG", -1.3, 0.04, -1.9), 0.9)
human("felixO", "felix", pos("OR", -0.5, 0.04, -1.7), face="happy"); put("appleO", "apple", pos("OR", 0.9, 0.64, -2.0), 0.45)
put("carC", "car", pos("CR", 0.2, 0.04, -2.0), 1.3, face="lorz"); put("mile9", "mile9", pos("CR", -2.9, 0.04, -2.4), 1.3); put("dust_C", "dust", PARK, 0.9)
human("judgeQ", "judge", pos("DQ", -0.8, 0.04, -1.7), face="shouting"); human("lorzQ", "lorz", pos("DQ", 0.5, 0.04, -1.9), face="nervous"); put("watchQ", "watch", pos("DQ", 1.9, 0.78, -2.3), 0.6)
human("hicksT", "hicks", pos("TR", -0.9, 0.04, -1.7), face="nervous"); human("trainT", "trainer", pos("TR", 0.5, 0.04, -1.9), face="smug"); put("trioT", "trio", pos("TR", 1.8, 0.78, -2.2), 0.55); put("poisT", "poison", pos("TR", -2.6, 0.78, -2.2), 0.5)
put("bookR", "rulebook", pos("RB", -0.2, 0.78, -2.0), 0.6); put("scaleR", "scale", pos("RB", 2.6, 0.78, -2.3), 0.7)
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


HOOK = dict(anchor=(0.1, 1.0, -2.0), dist=10.0, yaw=4, pitch=6)
# ---- The first man across the Olympic finish line rode in a car. The winner ran on rat poison. And the poison was legal.
s = S("0", "HK", zoom=14, pan=(-3, 0), **HOOK); go(s, 0.0, "carH", pos("HK", -0.25, 0.04, -1.8), 1.0, walk=False); act(s, 0.1, "carH", shake=0.4); act(s, 0.3, "hicksH", face="shocked", shake=0.5)
tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
s = S("Olympic finish line", "HK", (0.0, 0.8, -2.4), 8.4, -14, pitch=2, yawTo=4); act(s, 0.05, "tape_H", shake=0.5); act(s, 0.2, "hicksH", shake=0.4)
s = S("rode in a", "HK", (-0.25, 0.7, -1.8), 6.6, 10, pitch=5, zoom=10, _dis=1, dof=dict(focus="carH", blur=0.4)); hide(s, 0.0, "hicksH"); act(s, 0.05, "carH", shake=0.5); T(s, "carc"); snap(s, rel(s, "car"), 12)
s = S("The winner ran", "TR", (-2.6, 1.05, -2.2), 2.4, -6, pitch=14, pitchTo=2, type="macro", dof=dict(focus="poisT", blur=0.5)); act(s, 0.1, "poisT", shake=0.5); T(s, "ratc")
s = S("And the poison", "TR", (-1.0, 1.2, -1.7), 4.6, 12, pitch=5, zoom=-10); ft(s, "hicksT", ["nervous", "happy"]); T(s, "legal")
# ---- St. Louis. August 30th, 1904. Thirty-two runners start the Olympic marathon in ninety-degree heat, on dirt roads.
s = crane("St Louis", "SL", (0.0, 1.3, -2.4), 9.4, -22, -2, 36, 6); act(s, 0.2, "pack_L", shake=0.3); T(s, "stl")
s = S("30th 1904", "SL", (0.0, 1.6, -2.4), 7.6, 8, pitch=6, zoom=12); act(s, 0.1, "pack_L", shake=0.3); T(s, "y1904", dy=0.2, dx=-0.15, wf=0.32, hf=0.34); snap(s, 0.3, 10)
s = S("Thirtytwo runners start", "ST", (0.0, 0.8, -2.2), 6.4, 16, pitch=5, yawTo=-4); act(s, 0.1, "pack_S", shake=0.4); T(s, "r32")
s = crane("the Olympic marathon", "ST", (0.0, 0.8, -2.2), 8.0, -20, -2, 40, 10); act(s, 0.1, "pack_S", shake=0.3)
s = S("ninetydegree heat", "HT", (0.3, 1.6, -2.8), 8.4, -6, pitch=18, pitchTo=4); act(s, 0.1, "sunT", shake=0.5); act(s, 0.3, "thermoT", shake=0.4); c_ = T(s, "heatc"); snap(s, rel(s, "heat"), 12); swap(s, c_, rel(s, "dirt"), "dirt")
# ---- The organizer, James Sullivan, has an idea. Just one water stop. Mile twelve. He wants to study dehydration. On purpose.
s = crane("The organizer James", "SU", (-0.1, 1.2, -1.8), 7.6, -20, 0, 32, 6); ft(s, "sullyU", ["smug", "happy"]); T(s, "sully")
s = S("Sullivan has an", "SU", (-0.6, 1.25, -1.7), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="sullyU", blur=0.4)); ft(s, "sullyU", ["happy", "smug"]); act(s, 0.05, "sullyU", pose=dict(armR=-150)); T(s, "idea"); cfx(s, 0.3, "glint", "sullyU", 0.5)
s = S("Just one water", "WS", (-0.2, 0.9, -2.1), 6.8, -16, pitch=5, yawTo=4); act(s, 0.1, "barrelW", shake=0.4); c_ = T(s, "onestop"); act(s, rel(s, "Mile"), "mile12", shake=0.6); snap(s, rel(s, "twelve"), 10)
s = S("He wants to", "SU", (-0.3, 1.2, -1.8), 5.6, -14, pitch=5, yawTo=2); ft(s, "sullyU", ["smug", "happy", "shouting"]); c_ = T(s, "dehyd"); swap(s, c_, rel(s, "On purpose"), "purpose"); act(s, rel(s, "On purpose"), "sullyU", shake=0.4)
# ---- Runners drop. A wild dog chases one man a mile off course. Felix Carvajal eats rotten apples from an orchard, takes a nap, and still finishes fourth.
s = crane("Runners drop", "HT", (0.0, 1.1, -2.2), 8.6, 20, 0, 34, 6); show(s, 0.02, "pack_T", pos("HT", -0.2, 0.04, -1.8), hop=0); act(s, 0.2, "sunT", shake=0.4); T(s, "drop")
s = S("chases one man", "DG", (-0.3, 0.9, -1.9), 7.4, 6, pitch=4, zoom=4, pan=(10, 0)); go(s, 0.05, "tauD", pos("DG", 0.45, 0.04, -1.8), 1.2); go(s, 0.05, "dogD", pos("DG", -0.8, 0.04, -1.9), 1.2, walk=False); ft(s, "tauD", ["shocked", "nervous"]); c_ = T(s, "dogc"); swap(s, c_, rel(s, "a mile"), "offc"); snap(s, 0.3, 10)
s = crane("Flix Carvajal eats", "OR", (0.15, 1.1, -1.8), 7.8, -22, -2, 34, 6); ft(s, "felixO", ["happy", "smug"]); T(s, "felixc")
s = S("apples from an", "OR", (0.9, 0.86, -2.0), 2.8, 0, pitch=6, zoom=10, type="macro", dof=dict(focus="appleO", blur=0.5)); act(s, 0.05, "appleO", face="sad", shake=0.5); T(s, "apples"); snap(s, 0.3, 10)
s = S("takes a nap", "OR", (-0.6, 1.15, -1.75), 5.0, -14, pitch=5, yawTo=4); ft(s, "felixO", ["smug", "happy", "shouting"]); c_ = T(s, "nap"); cfx(s, 0.1, "z", "felixO", 0.5); swap(s, c_, rel(s, "still"), "fourth"); act(s, rel(s, "still"), "felixO", pose=dict(armR=-150))
# ---- Then Fred Lorz crosses the line first. But Lorz quit around mile nine and hitched a ride. About ten miles. In a car. Disqualified.
s = crane("Then Fred Lorz", "HK", (0.0, 1.0, -2.1), 8.6, -20, 0, 32, 6, _dis=1); hide(s, 0.0, "carH"); hide(s, 0.0, "hicksH"); show(s, 0.0, "lorzH", pos("HK", -0.9, 0.04, -1.8), hop=0)
go(s, 0.1, "lorzH", pos("HK", 0.5, 0.04, -1.8), 1.3); ft(s, "lorzH", ["happy", "smug"]); T(s, "lorzc")
s = S("But Lorz quit", "CR", (-2.7, 0.85, -2.4), 3.6, 12, pitch=5, zoom=12, dof=dict(focus="mile9", blur=0.4)); act(s, 0.1, "mile9", shake=0.4); T(s, "quit"); snap(s, rel(s, "quit"), 10)
s = S("and hitched a", "CR", (0.5, 0.8, -2.0), 7.6, -6, pitch=4, zoom=4, pan=(18, 0)); go(s, 0.05, "carC", pos("CR", 0.7, 0.04, -2.0), 1.0, walk=False); show(s, 0.1, "dust_C", pos("CR", -1.0, 0.3, -2.3)); T(s, "ride")
s = crane("About ten miles", "CR", (0.8, 0.8, -2.0), 9.4, 24, 4, 42, 12); act(s, 0.1, "carC", shake=0.4); c_ = T(s, "ten"); swap(s, c_, rel(s, "car"), "incar"); act(s, rel(s, "car"), "carC", shake=0.5)
s = S("Disqualified", "DQ", (-0.2, 1.1, -1.8), 6.6, 16, pitch=5, yawTo=-4); ft(s, "judgeQ", ["shouting", "smug"]); ft(s, "lorzQ", ["nervous", "shocked"]); act(s, 0.05, "judgeQ", pose=dict(armR=-150)); T(s, "dq"); cfx(s, 0.3, "bang", "judgeQ", 0.6)
# ---- The real winner is Thomas Hicks. You see, his trainers kept him moving with egg whites, brandy, and strychnine. Rat poison. He staggers over the line barely standing.
s = crane("is Thomas Hicks", "TR", (0.4, 1.1, -1.9), 9.6, -16, 0, 32, 6); ft(s, "hicksT", ["nervous", "happy"]); T(s, "hicksc")
s = S("You see his", "TR", (1.15, 1.0, -2.0), 5.6, 18, pitch=5, yawTo=2); ft(s, "trainT", ["smug", "happy"]); cfx(s, 0.3, "glint", "trainT", 0.5)
s = S("egg whites brandy", "TR", (1.8, 1.05, -2.2), 2.6, -4, pitch=12, pitchTo=2, type="macro", dof=dict(focus="trioT", blur=0.5)); act(s, 0.05, "trioT", shake=0.4); T(s, "recipe")
s = S("and strychnine Rat", "TR", (-2.6, 1.05, -2.2), 2.4, 10, pitch=5, zoom=14, type="macro", dof=dict(focus="poisT", blur=0.5)); act(s, 0.05, "poisT", shake=0.5); T(s, "strych"); snap(s, rel(s, "strychnine"), 12)
s = S("He staggers over", "HK", (0.0, 0.9, -2.0), 7.4, -6, pitch=2, zoom=10, _dis=1); hide(s, 0.0, "lorzH"); show(s, 0.0, "hicksH", pos("HK", -0.7, 0.04, -2.0), hop=0); go(s, 0.1, "hicksH", pos("HK", 0.5, 0.04, -2.0), 1.6)
ft(s, "hicksH", ["nervous", "shocked"]); T(s, "barely"); cfx(s, 0.3, "sweat", "hicksH", 0.8)
# ---- Three hours, twenty-eight minutes. The slowest winning time in Olympic history. Only fourteen of thirty-two finish.
s = S("Three hours twentyeight", "DQ", (1.9, 1.08, -2.3), 2.6, 10, pitch=5, zoom=14, type="macro", dof=dict(focus="watchQ", blur=0.5)); act(s, 0.05, "watchQ", shake=0.5); snap(s, 0.2, 10)
s = crane("The slowest winning", "HK", (0.0, 1.0, -2.2), 9.6, 22, 2, 44, 10); act(s, 0.2, "hicksH", face="nervous", shake=0.3); T(s, "slowest")
s = S("Only fourteen of", "HK", (0.0, 2.0, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="OF 32 FINISH", items=["14"]))
# ---- And Hicks broke no rule. Doping wasn't banned until 1908. The poison was fine. The car was not.
s = S("And Hicks broke", "TR", (-0.9, 1.25, -1.7), 4.6, -10, pitch=5, zoom=12, _dis=1, dof=dict(focus="hicksT", blur=0.4)); hide(s, 0.0, "trainT"); ft(s, "hicksT", ["smug", "happy"]); T(s, "norule"); cfx(s, 0.3, "glint", "hicksT", 0.6); snap(s, rel(s, "rule"), 10)
s = crane("Doping", "RB", (0.0, 1.0, -2.0), 7.6, -20, 0, 36, 8); act(s, 0.2, "bookR", shake=0.4); T(s, "dopingc")
s = S("until 1908", "RB", (-0.2, 1.1, -2.0), 3.2, 8, pitch=6, zoom=14, type="macro", dof=dict(focus="bookR", blur=0.5)); act(s, 0.05, "bookR", shake=0.5); T(s, "y1908", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("The poison was#2", "RB", (2.6, 1.15, -2.3), 3.2, -10, pitch=5, yawTo=6, type="macro", dof=dict(focus="scaleR", blur=0.5)); act(s, 0.1, "scaleR", shake=0.4); T(s, "fine")
s = S("The car was", "HK", (-0.2, 0.8, -1.8), 6.0, 10, pitch=5, zoom=12, _dis=1); hide(s, 0.0, "hicksH"); show(s, 0.0, "carH", pos("HK", -0.25, 0.04, -1.8), hop=0); act(s, 0.0, "carH", face="lorz", shake=0.5); T(s, "carnot"); snap(s, 0.3, 12)
# ---- So the only cheater that day was the first man across the Olympic finish line. (pull-out onto the hook frame)
s = S("So the only", "HK", (0.0, 1.0, -2.0), 7.4, -14, pitch=5, yawTo=2); act(s, 0.1, "carH", shake=0.4); T(s, "cheater")
s = S("first man across#2", "HK", (-0.3, 0.8, -1.8), 6.6, 14, pitch=5, yawTo=-2); act(s, 0.1, "carH", shake=0.4)
s = S("Olympic finish line#2", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "carH", pos("HK", -0.4, 0.04, -1.8), hop=0); act(s, 0.0, "carH", face="mystery")
show(s, 0.0, "hicksH", pos("HK", 1.0, 0.04, -2.0), hop=0); act(s, 0.0, "hicksH", face="nervous"); go(s, 0.2, "carH", pos("HK", -0.25, 0.04, -1.8), 1.0, walk=False); tag(s, 0.05, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
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
ATM = dict(HK=dict(dust=D_(30), rays=dict(angle=30, intensity=0.55)), SL=dict(dust=D_(22), rays=dict(angle=24, intensity=0.5)), ST=dict(dust=D_(48)), HT=dict(dust=D_(40), rays=dict(angle=16, intensity=0.7)),
           SU=dict(dust=D_(20)), WS=dict(dust=D_(36), rays=dict(angle=34, intensity=0.5)), DG=dict(dust=D_(40)), OR=dict(dust=D_(20), rays=dict(angle=28, intensity=0.5)), CR=dict(dust=D_(34)),
           DQ=dict(dust=D_(20)), TR=dict(bokeh=BK(0.45)), RB=dict(bokeh=BK(0.4)))
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
MOOD = dict(HK="stadium", SL="fairday", ST="prairie", HT="scorch", SU="plum", WS="peachnoon", DG="cornday", OR="orchard", CR="violetdusk", DQ="tent", TR="poison", RB="archive")
light, cur = [{"t": 0, "mood": "stadium"}], "stadium"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 20,
    "moods": {"stadium": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fff4d8", "intensity": 2.4}, "sky": {"top": "#3cbed2", "horizon": "#bef0ec"}, "fill": {"sky": "#e8fff8", "ground": "#a0583a", "intensity": 1.4}},
              "fairday": {"sun": {"azimuth": 30, "elevation": 45, "color": "#fffbe8", "intensity": 2.4}, "sky": {"top": "#50c8dc", "horizon": "#d2f4f0"}, "fill": {"sky": "#f0fffa", "ground": "#a08a6a", "intensity": 1.35}},
              "prairie": {"sun": {"azimuth": 60, "elevation": 35, "color": "#fff0c0", "intensity": 2.4}, "sky": {"top": "#5ac8dc", "horizon": "#fae6aa"}, "fill": {"sky": "#fff4d8", "ground": "#a07a46", "intensity": 1.4}},
              "scorch": {"sun": {"azimuth": 20, "elevation": 50, "color": "#ffd8a0", "intensity": 2.6}, "sky": {"top": "#f05a32", "horizon": "#ffc85a"}, "fill": {"sky": "#ffe0b0", "ground": "#a05030", "intensity": 1.5}},
              "plum": {"sun": {"azimuth": -20, "elevation": 40, "color": "#ffe8c8", "intensity": 2.5}, "sky": {"top": "#783c6e", "horizon": "#aa6496"}, "fill": {"sky": "#ffd8f0", "ground": "#5a3a4a", "intensity": 1.85}},
              "peachnoon": {"sun": {"azimuth": 200, "elevation": 30, "color": "#ffd8b0", "intensity": 2.5}, "sky": {"top": "#fa965a", "horizon": "#ffdcaa"}, "fill": {"sky": "#ffe8d0", "ground": "#9a6a4a", "intensity": 1.45}},
              "cornday": {"sun": {"azimuth": 50, "elevation": 45, "color": "#fffbe0", "intensity": 2.4}, "sky": {"top": "#6ec8f0", "horizon": "#dcf6dc"}, "fill": {"sky": "#f0fff0", "ground": "#8a7a4a", "intensity": 1.35}},
              "orchard": {"sun": {"azimuth": 30, "elevation": 40, "color": "#fff8e0", "intensity": 2.4}, "sky": {"top": "#96dcc8", "horizon": "#e6fadc"}, "fill": {"sky": "#f0fff0", "ground": "#5a7a4a", "intensity": 1.4}},
              "violetdusk": {"sun": {"azimuth": 230, "elevation": 18, "color": "#ffc8a8", "intensity": 2.5}, "sky": {"top": "#786ed2", "horizon": "#ffc8aa"}, "fill": {"sky": "#ffe0e8", "ground": "#6a5a6a", "intensity": 1.7}},
              "tent": {"sun": {"azimuth": -30, "elevation": 40, "color": "#fff0e0", "intensity": 2.4}, "sky": {"top": "#dc3c46", "horizon": "#fac8be"}, "fill": {"sky": "#ffe8e0", "ground": "#8a4a40", "intensity": 1.6}},
              "poison": {"sun": {"azimuth": 20, "elevation": 40, "color": "#f0ffc0", "intensity": 2.5}, "sky": {"top": "#78962e", "horizon": "#c8dc6e"}, "fill": {"sky": "#f0ffc8", "ground": "#5a5a2a", "intensity": 1.9}},
              "archive": {"sun": {"azimuth": 30, "elevation": 35, "color": "#f0e0ff", "intensity": 2.6}, "sky": {"top": "#503c96", "horizon": "#966ec8"}, "fill": {"sky": "#e8d8ff", "ground": "#4a3a60", "intensity": 2.0}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#b6ff3c", "paper": ["#f0a860", "#d88840"], "dofPx": 8, "particle": "#fff4d8", "bokehColor": "#d8ff9a", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(stl="St Louis", drop="Runners drop", lorz="Then Fred Lorz", real="The real winner", doping="Doping", car1="car", poison="poison", legal="legal", heat="ninetydegree heat",
           dog="dog", apples="apples", nap="nap", fourth="fourth", dq="Disqualified", incar="In a car", strych="strychnine", staggers="He staggers over", hours="Three hours",
           fourteen="Only fourteen", carnot="The car was", cheater="cheater", purpose="On purpose", twelve="Mile twelve", idea="idea")
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
