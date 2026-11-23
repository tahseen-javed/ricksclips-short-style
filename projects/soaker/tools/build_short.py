#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 18: a rocket scientist invented the Super Soaker (Lonnie Johnson).
usage: build_short.py <project folder>
Ten 80s neon-splash sets 70 units apart: BT orange-teal 1982 bathroom (hook + loop, violet "?" kid silhouette = open loop), JP navy JPL
control room, SP violet space with Jupiter, HM ice-blue home lab, MP beige engineering office, GR magenta-cyan neon garage, LR pink Memphis
toy office, TS yellow toy aisle, MN emerald money vault, YD pink-orange sunset backyard.  Shots 1-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(BT=0, JP=70, SP=140, HM=210, MP=280, GR=350, LR=420, TS=490, MN=560, YD=630)
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


yard("BT", "bath80.png", "tile80.jpg"); box("BT", 2.7, 0.04, -3.2, [1.4, 0.6, 0.8], color="#f8f4ec"); box("BT", -3.0, 0.04, -2.8, [0.6, 0.9, 0.6], color="#ff9a50")
yard("JP", "jpl.png", "navytile.jpg"); box("JP", -2.8, 0.04, -2.4, [1.2, 0.8, 0.6], color="#3c50a0"); box("JP", 2.8, 0.04, -2.6, [1.2, 0.8, 0.6], color="#3c50a0")
yard("SP", "space.png", "starfloor.jpg")
for x, y, z, sz in ((-3.2, 0.6, -2.6, 0.4), (3.0, 2.2, -3.4, 0.3), (2.6, 0.5, -2.2, 0.35)): box("SP", x, y, z, [sz, sz * 0.8, sz], color="#8a6ad0")
yard("HM", "homelab.png", "icetile.jpg"); table("HM", -2.8, -2.3, 1.0, 0.7, 0.74, "#9ab8d8"); box("HM", 2.9, 0.04, -3.0, [0.9, 1.3, 0.6], color="#c8e4f8")
yard("MP", "office.png", "carpet.jpg"); box("MP", 0.2, 0.04, -1.5, [1.6, 0.02, 0.8], color="#8ad4ff"); table("MP", -2.8, -2.4, 1.4, 0.8, 0.74, "#a07050"); box("MP", 2.8, 0.04, -2.8, [0.9, 1.2, 0.6], color="#7a8a9a")
yard("GR", "garage.png", "concrete.jpg"); table("GR", 1.3, -2.2, 1.6, 0.8, 0.74, "#6a4a5a"); box("GR", -3.0, 0.04, -3.0, [1.0, 0.7, 0.7], color="#ff5ac8")
yard("LR", "memphis.png", "memphis.jpg"); table("LR", -2.7, -2.2, 1.0, 0.7, 0.74, "#ffd23c"); box("LR", 2.8, 0.04, -2.8, [0.8, 0.8, 0.8], color="#8a4ae0")
yard("TS", "toystore.png", "storefloor.jpg"); box("TS", 2.8, 0.04, -2.4, [0.8, 0.8, 0.8], color="#3cdcff"); box("TS", -3.0, 0.04, -3.0, [1.0, 1.2, 0.6], color="#ff46a0")
yard("MN", "vault.png", "vaultfloor.jpg"); box("MN", -2.9, 0.04, -3.0, [1.0, 0.6, 0.7], color="#ffc83c")
yard("YD", "backyard.png", "lawn.jpg"); box("YD", 2.9, 0.04, -3.0, [1.2, 0.3, 0.9], color="#3cd2f0")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
human("lonB", "lonnie", pos("BT", -0.8, 0.04, -1.6), face="shocked"); put("soakB", "soaker", pos("BT", -0.35, 0.95, -1.35), 0.42); put("blast_B", "blast", pos("BT", 0.62, 1.02, -1.35), 0.26)
put("sinkB", "sink", pos("BT", 2.4, 0.04, -3.4), 1.1); put("blastS", "blast", PARK, 0.4, flip=True); put("shadow_B", "shadowkid", pos("BT", -1.6, 0.04, -4.0), 1.1)
human("lonJ", "lonnie", pos("JP", -0.8, 0.04, -1.6), face="happy"); put("rocketJ", "rocket", pos("JP", 0.7, 0.04, -2.2), 1.5)
put("galS", "galileo", pos("SP", 0.5, 1.2, -2.2), 1.0); put("jupS", "jupiter", pos("SP", -1.2, 0.8, -4.4), 2.0)
human("lonH", "lonnie", pos("HM", -1.0, 0.04, -1.6), face="happy"); put("coolH", "cooler", pos("HM", 0.6, 0.04, -2.2), 1.4); put("freonH", "freon", pos("HM", -2.8, 0.78, -2.3), 0.55)
human("engM", "eng", pos("MP", -0.6, 0.04, -1.6), face="nervous"); put("mopM", "mop", pos("MP", 0.5, 0.04, -1.8), 1.4)
human("lonG", "lonnie", pos("GR", -0.9, 0.04, -1.6), face="happy"); put("protoG", "protos", pos("GR", 1.3, 0.78, -2.2), 0.6); put("soakG", "soaker", PARK, 0.42)
human("lonL", "lonnie", pos("LR", -0.8, 0.04, -1.6), face="happy"); human("execL", "exec", pos("LR", 0.6, 0.04, -1.7), face="happy"); put("contractL", "contract", pos("LR", -2.7, 0.78, -2.2), 0.6)
put("boxT", "boxpd", pos("TS", 0.4, 0.04, -2.2), 1.5); human("kidcT", "kidc", pos("TS", -1.2, 0.04, -1.6), face="shocked", h=1.25); put("soakT", "soaker", pos("TS", 2.8, 0.84, -2.4), 0.45)
put("cashM", "cash", pos("MN", -0.3, 0.04, -2.0), 0.9); put("coinsM", "coins", pos("MN", 1.8, 0.04, -3.4), 1.2)
human("kiddY", "kidd", pos("YD", -0.7, 0.04, -1.6), face="happy", h=1.25); put("soakY", "soaker", pos("YD", -0.3, 0.62, -1.4), 0.32); put("blast_Y", "blast", pos("YD", 0.45, 0.7, -1.4), 0.18)
human("kidcY", "kidc", pos("YD", 1.2, 0.04, -1.9), face="shocked", h=1.25)
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


HOOK = dict(anchor=(0.0, 1.0, -1.5), dist=7.0, yaw=4, pitch=8)
# ---- A rocket scientist invented the Super Soaker. By accident. In his bathroom.
s = S("0", "BT", zoom=14, pan=(-3, 0), **HOOK); ft(s, "lonB", ["shocked", "happy", "shocked"]); act(s, 0.1, "soakB", shake=0.4); act(s, 0.0, "blast_B", shake=0.3)
tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
s = S("invented the", "BT", (-0.55, 1.1, -1.5), 3.6, -14, pitch=4, yawTo=6, dof=dict(focus="soakB", blur=0.4)); ft(s, "lonB", ["happy", "shocked"]); act(s, 0.1, "soakB", face="shocked", shake=0.3); snap(s, max(0.3, rel(s, "Soaker")), 14)
s = S("By accident", "BT", (2.4, 1.0, -3.4), 2.8, -6, pitch=14, pitchTo=2, type="macro", dof=dict(focus="sinkB", blur=0.5), _dis=1); hide(s, 0.0, "blast_B"); act(s, 0.1, "sinkB", face="on", shake=0.4); T(s, "accident")
s = S("In his bathroom", "BT", (0.7, 1.2, -2.4), 10.4, 10, pitch=6, zoom=-10); ft(s, "lonB", ["shocked", "happy"]); act(s, 0.1, "shadow_B", shake=0.3); T(s, "wait", 0.15, wf=0.5)
# ---- Lonnie Johnson worked at NASA's Jet Propulsion Laboratory. He worked on Galileo, the probe sent to Jupiter. Serious work.
s = crane("Lonnie Johnson worked", "JP", (0.0, 1.2, -1.9), 9.0, 22, 2, 36, 6); ft(s, "lonJ", ["happy", "smug"]); T(s, "lonniec")
s = S("Jet Propulsion", "JP", (0.3, 1.2, -2.0), 6.5, -6, pitch=5, zoom=4, pan=(34, 0)); act(s, 0.05, "rocketJ", shake=0.5); ft(s, "lonJ", ["shocked", "happy"])
s = crane("He worked on", "SP", (-0.6, 1.5, -3.0), 11.0, -18, -2, 24, 6); act(s, 0.1, "galS", shake=0.3); T(s, "galileoc")
s = S("the probe sent", "SP", (-0.4, 1.5, -3.2), 10.0, 8, pitch=5, yawTo=-4); go(s, 0.1, "galS", pos("SP", 0.1, 1.3, -2.6), 1.2, walk=False); act(s, 0.3, "jupS", face="shocked", shake=0.3); snap(s, rel(s, "Jupiter"), 12)
s = S("Serious work", "JP", (-0.8, 1.45, -1.6), 4.0, 10, pitch=5, zoom=12, dof=dict(focus="lonJ", blur=0.4)); ft(s, "lonJ", ["neutral", "smug"]); T(s, "serious")
# ---- 1982. At home, he's building a new cooling system that runs on water instead of Freon.
s = crane("1982", "HM", (-0.2, 1.2, -1.9), 9.0, -22, -2, 36, 6); ft(s, "lonH", ["happy", "smug"]); T(s, "y1982", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("a new cooling", "HM", (0.6, 0.85, -2.2), 3.4, -8, pitch=4, zoom=12, type="macro", dof=dict(focus="coolH", blur=0.5)); act(s, 0.1, "coolH", shake=0.3); T(s, "cooling")
s = S("instead of Freon", "HM", (-2.8, 1.05, -2.3), 2.6, 8, pitch=14, pitchTo=2, type="macro", dof=dict(focus="freonH", blur=0.5)); act(s, 0.1, "freonH", shake=0.4); T(s, "freonc")
# ---- He hooks a homemade nozzle to his bathroom sink. Turns it on. A blast of water shoots clean across the room.
s = crane("He hooks a", "BT", (0.7, 1.2, -2.4), 10.4, 20, 2, 38, 6, _dis=1); hide(s, 0.0, "soakB"); hide(s, 0.0, "blast_B"); ft(s, "lonB", ["happy", "smug"]); T(s, "nozzlec")
s = S("to his bathroom", "BT", (0.7, 1.2, -2.4), 9.4, -10, pitch=5, zoom=-10); ft(s, "lonB", ["smug", "happy"]); act(s, 0.1, "sinkB", shake=0.3)
s = S("Turns it on", "BT", (2.4, 1.0, -3.4), 3.0, 6, pitch=4, zoom=14, type="macro", dof=dict(focus="sinkB", blur=0.5)); act(s, 0.25, "sinkB", face="on", shake=0.5); T(s, "turnon")
s = S("A blast of", "BT", (0.7, 1.2, -2.5), 10.0, -4, pitch=5, zoom=4, pan=(24, 0)); show(s, 0.08, "blastS", pos("BT", 0.9, 1.1, -2.8)); act(s, 0.1, "lonB", face="shocked"); T(s, "blastc"); snap(s, 0.3, 14)
s = S("shoots clean across", "BT", (0.7, 1.2, -2.4), 9.6, 12, pitch=6, zoom=-12); ft(s, "lonB", ["shocked", "shouting"]); act(s, 0.0, "lonB", pose=dict(armR=-150, armL=150)); act(s, 0.1, "blastS", shake=0.4); cfx(s, 0.2, "bang", "lonB", 0.6)
# ---- You see, most engineers would just mop the floor. Lonnie thought: kids would love this.
s = crane("You see most", "MP", (0.0, 1.1, -1.8), 8.0, -22, -2, 36, 6); ft(s, "engM", ["nervous", "neutral"]); T(s, "mopc")
s = S("just mop the", "MP", (0.5, 0.9, -1.8), 3.0, 12, pitch=4, yawTo=-4, type="macro", dof=dict(focus="mopM", blur=0.5)); act(s, 0.1, "mopM", shake=0.4); cfx(s, 0.2, "z", "mopM", 0.8)
s = S("Lonnie thought", "BT", (-0.8, 1.45, -1.6), 4.0, 10, pitch=5, zoom=12, dof=dict(focus="lonB", blur=0.4)); hide(s, 0.0, "blastS"); ft(s, "lonB", ["smug", "happy"]); act(s, 0.0, "lonB", pose=dict(armR=-150)); T(s, "kidslove"); cfx(s, 0.3, "glint", "lonB", 0.7)
# ---- He spent seven years turning that blast into a pressurized water gun.
s = crane("He spent seven", "GR", (0.2, 1.2, -1.9), 9.5, 22, 2, 38, 6); ft(s, "lonG", ["happy", "smug"]); T(s, "years7")
s = S("turning that blast", "GR", (1.3, 1.0, -2.2), 3.0, -12, pitch=4, yawTo=6, type="macro", dof=dict(focus="protoG", blur=0.5)); act(s, 0.1, "protoG", shake=0.3)
s = S("into a pressurized", "GR", (-0.65, 1.2, -1.5), 3.8, 10, pitch=5, zoom=12, dof=dict(focus="soakG", blur=0.4)); show(s, 0.05, "soakG", pos("GR", -0.45, 0.95, -1.35)); ft(s, "lonG", ["shocked", "happy"]); T(s, "pgun"); snap(s, rel(s, "pressurized"), 12)
# ---- In 1989, a toy company called Larami finally licensed it.
s = crane("In 1989", "LR", (-0.1, 1.2, -1.8), 8.6, -22, -2, 34, 6); ft(s, "execL", ["happy", "smug"]); ft(s, "lonL", ["happy", "smug"]); T(s, "y1989", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("a toy company", "LR", (0.6, 1.45, -1.7), 4.0, -10, pitch=5, zoom=12, dof=dict(focus="execL", blur=0.4)); ft(s, "execL", ["smug", "happy"]); T(s, "larami")
s = S("finally licensed it", "LR", (-2.7, 1.05, -2.2), 2.6, 8, pitch=14, pitchTo=2, type="macro", dof=dict(focus="contractL", blur=0.5)); act(s, 0.1, "contractL", shake=0.4); T(s, "licensed")
# ---- It launched in 1990 as the Power Drencher. They renamed it. Super Soaker.
s = crane("It launched in", "TS", (-0.3, 1.1, -1.9), 8.6, 22, 2, 36, 6); ft(s, "kidcT", ["shocked", "happy"]); T(s, "y1990", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("as the Power", "TS", (0.4, 0.8, -2.2), 3.8, -8, pitch=4, zoom=12, type="macro", dof=dict(focus="boxT", blur=0.5)); act(s, 0.1, "boxT", shake=0.3)
s = S("They renamed it", "TS", (-0.4, 1.1, -1.9), 6.8, -16, pitch=5, yawTo=4); ft(s, "kidcT", ["shocked", "happy"]); T(s, "renamed")
s = S("Super Soaker#2", "TS", (2.8, 1.05, -2.4), 2.8, 8, pitch=4, zoom=14, type="macro", dof=dict(focus="soakT", blur=0.5)); act(s, 0.05, "soakT", shake=0.5); T(s, "soakerc"); snap(s, 0.3, 12); cfx(s, 0.3, "glint", "soakT", 0.7)
# ---- In about two years, it made 200 million dollars. Total sales today? Close to a billion.
s = crane("In about two", "MN", (0.7, 1.0, -2.6), 9.4, -20, 0, 40, 8); act(s, 0.1, "cashM", shake=0.3); act(s, 0.1, "coinsM", shake=0.2)
s = S("it made 200", "MN", (0.0, 2.0, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="IN ABOUT TWO YEARS", items=["$200,000,000"]))
s = S("Total sales today", "MN", (-0.3, 0.6, -2.0), 4.0, 8, pitch=4, zoom=12, type="macro", dof=dict(focus="cashM", blur=0.5)); act(s, 0.1, "cashM", shake=0.3); T(s, "total")
s = S("Close to a", "MN", (1.8, 0.8, -3.4), 5.0, -8, pitch=5, zoom=-10); act(s, 0.1, "coinsM", shake=0.4); T(s, "billion"); snap(s, rel(s, "billion"), 14); cfx(s, 0.3, "glint", "coinsM", 0.7)
# ---- He set out to build a better way to cool things down. He nailed it. It just fits in a kid's hands.
s = crane("He set out", "HM", (-0.2, 1.2, -1.9), 9.0, 20, 0, 34, 6); ft(s, "lonH", ["happy", "smug"]); T(s, "cool")
s = S("to cool things", "HM", (0.6, 0.9, -2.2), 3.4, 6, pitch=14, pitchTo=2, type="macro", dof=dict(focus="coolH", blur=0.5)); act(s, 0.1, "coolH", shake=0.3)
s = S("He nailed it", "YD", (0.2, 1.0, -1.8), 8.0, 6, pitch=5, zoom=4, pan=(26, 0)); ft(s, "kiddY", ["happy", "shouting"]); ft(s, "kidcY", ["shocked", "happy"]); act(s, 0.1, "blast_Y", shake=0.4); T(s, "nailed")
s = S("It just fits", "YD", (-0.55, 0.85, -1.5), 3.4, -10, pitch=5, zoom=12, dof=dict(focus="soakY", blur=0.4)); ft(s, "kiddY", ["happy", "smug"]); T(s, "hands"); snap(s, rel(s, "hands"), 12); cfx(s, 0.3, "blush", "kiddY", 0.7)
# ---- Because a rocket scientist invented the Super Soaker. (pull-out onto the hook frame)
s = S("Because a rocket", "JP", (-0.1, 1.2, -1.9), 6.8, 16, pitch=5, yawTo=-2); ft(s, "lonJ", ["smug", "happy"]); act(s, 0.1, "rocketJ", shake=0.3)
s = S("invented the#2", "BT", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "soakB", pos("BT", -0.35, 0.95, -1.35), hop=0); show(s, 0.0, "blast_B", pos("BT", 0.62, 1.02, -1.35), hop=0)
ft(s, "lonB", ["shocked", "happy", "shocked"]); act(s, 0.1, "soakB", shake=0.4); tag(s, 0.05, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
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
ATM = dict(BT=dict(dust=D_(20), rays=dict(angle=30, intensity=0.5)), JP=dict(bokeh=BK(0.4)), SP=dict(bokeh=BK(0.45)), HM=dict(dust=D_(30)), MP=dict(dust=D_(24), rays=dict(angle=26, intensity=0.5)),
           GR=dict(bokeh=BK(0.4)), LR=dict(dust=D_(18)), TS=dict(dust=D_(20), rays=dict(angle=36, intensity=0.5)), MN=dict(bokeh=BK(0.4)), YD=dict(dust=D_(30), rays=dict(angle=18, intensity=0.65)))
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
MOOD = dict(BT="retro", JP="mission", SP="cosmos", HM="frost", MP="beige", GR="neon", LR="memphis", TS="aisle", MN="emerald", YD="sunsetpink")
light, cur = [{"t": 0, "mood": "retro"}], "retro"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 18,
    "moods": {"retro": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fff0dc", "intensity": 2.4}, "sky": {"top": "#ff9650", "horizon": "#ffd8a0"}, "fill": {"sky": "#ffe8d0", "ground": "#407a78", "intensity": 1.5}},
              "mission": {"sun": {"azimuth": 20, "elevation": 40, "color": "#c8e8ff", "intensity": 2.6}, "sky": {"top": "#18286a", "horizon": "#3c58b0"}, "fill": {"sky": "#b0d8ff", "ground": "#404a80", "intensity": 2.0}},
              "cosmos": {"sun": {"azimuth": 50, "elevation": 30, "color": "#fff0e0", "intensity": 2.6}, "sky": {"top": "#3a1470", "horizon": "#8a46c0"}, "fill": {"sky": "#e0c8ff", "ground": "#503878", "intensity": 2.0}},
              "frost": {"sun": {"azimuth": -30, "elevation": 45, "color": "#f4fbff", "intensity": 2.3}, "sky": {"top": "#78bef0", "horizon": "#d8f0ff"}, "fill": {"sky": "#e8f6ff", "ground": "#6a8aa8", "intensity": 1.5}},
              "beige": {"sun": {"azimuth": 30, "elevation": 40, "color": "#fff0d0", "intensity": 2.4}, "sky": {"top": "#e6c896", "horizon": "#faebc8"}, "fill": {"sky": "#fff0d8", "ground": "#806048", "intensity": 1.45}},
              "neon": {"sun": {"azimuth": -20, "elevation": 40, "color": "#ffd0f4", "intensity": 2.6}, "sky": {"top": "#3c1e50", "horizon": "#7a3488"}, "fill": {"sky": "#f0c8ff", "ground": "#503860", "intensity": 2.1}},
              "memphis": {"sun": {"azimuth": 40, "elevation": 45, "color": "#fff4f8", "intensity": 2.4}, "sky": {"top": "#ffb4d8", "horizon": "#ffe6f0"}, "fill": {"sky": "#fff0f8", "ground": "#508a88", "intensity": 1.45}},
              "aisle": {"sun": {"azimuth": 0, "elevation": 55, "color": "#fffbe8", "intensity": 2.3}, "sky": {"top": "#ffd83c", "horizon": "#fff4b0"}, "fill": {"sky": "#fffbe8", "ground": "#8a8070", "intensity": 1.4}},
              "emerald": {"sun": {"azimuth": 20, "elevation": 40, "color": "#fff0b0", "intensity": 2.5}, "sky": {"top": "#146e50", "horizon": "#3caa78"}, "fill": {"sky": "#d8ffe0", "ground": "#305a48", "intensity": 1.95}},
              "sunsetpink": {"sun": {"azimuth": 200, "elevation": 14, "color": "#ffc090", "intensity": 2.5}, "sky": {"top": "#ff5a8c", "horizon": "#ffc864"}, "fill": {"sky": "#ffd0c0", "ground": "#6a7050", "intensity": 1.6}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#3cdcff", "paper": ["#e8f8ff", "#c8ecff"], "dofPx": 8, "particle": "#e8faff", "bokehColor": "#ff8ad8", "ray": "#fff0e0", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(lonnie="Lonnie Johnson worked", y1982="1982", yousee="You see most", y1989="In 1989", inabout="In about two", heset="He set out", soaker="Soaker", jet="Jet Propulsion",
           jupiter="Jupiter", blast="A blast of", mop="mop", thought="Lonnie thought", press="pressurized", licensed="licensed", renamed="They renamed it", soaker2="Super Soaker#2",
           m200="200", billion="billion", nailed="He nailed it", hands="hands", turns="Turns it on")
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
