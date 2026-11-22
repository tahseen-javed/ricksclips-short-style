#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 15: Monopoly was invented to make people hate monopolies.
usage: build_short.py <project folder>
Fifteen sets 70 units apart: GB giant-board city at golden hour (hook + loop), TY peach typing office, LL landlord split
(gold mansion | grey rain), PT marble patent office, RS split rules (green meadow | red storm), CU crimson parlour, GU purple quiz
stage, LS teal lecture parlour, HC snowy log cabin, SN seaside sunset, DL olive 1930s living room, PB brick HQ in snow, LZ indigo
rainy room, CT 1970s courtroom, FN neon game night.  Every shot moves (crane / push-in / pull-out); same-set shots fly (dolly
glide), new sets dissolve.  Snap-ins, atmosphere, depth of field, comic fx, a timeline cutaway for the court case.
Cards are fitted to the safe box; the frame check prints CUT / SIGNCUT / INSIDE / OVERLAP flags."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(GB=0, TY=70, LL=140, PT=210, RS=280, CU=350, GU=420, LS=490, HC=560, SN=630, DL=700, PB=770, LZ=840, CT=910, FN=980)
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


def table(loc, x, z, w=1.6, d=0.8, h=0.7, col="#8a5a3a", tex=None):
    if tex: box(loc, x, 0.04, z, [w, h, d], texture=tex, repeat=[1, 1])
    else: box(loc, x, 0.04, z, [w, h, d], color=col)


yard("GB", "bigworld.png", "felt.jpg"); box("GB", 0, 0.02, -2.4, [7.6, 0.03, 7.6], texture="boardtex.jpg", repeat=[1, 1])
for x, z, big in ((-3.0, -5.2, 0), (-1.7, -5.6, 0), (1.9, -5.4, 1), (3.3, -4.6, 0), (-3.4, -3.4, 0)):
    house("GB", x, z, [1.8, 1.5, 1.3] if big else [1.0, 0.9, 1.0], "#a02828" if big else "#1f7a40", color="#e04848" if big else "#4cbf70")
box("GB", 2.7, 0.05, -0.9, [0.6, 0.6, 0.6], color="#fafaf5"); box("GB", 3.4, 0.05, -0.4, [0.5, 0.5, 0.5], color="#fafaf5")
yard("TY", "office.png", "wood.jpg"); table("TY", 0.7, -1.95, 1.8, col="#a0683c"); box("TY", -2.9, 0.04, -3.4, [1.0, 1.4, 0.6], color="#6e9682"); box("TY", 3.0, 0.04, -3.0, [0.5, 0.5, 0.5], color="#c86e46")
yard("LL", "landlords.png", "grass.jpg"); house("LL", -3.4, -4.4, [2.0, 1.6, 1.6], "#c84a3a", color="#ffe296"); house("LL", 3.4, -4.2, [1.2, 1.8, 1.2], "#5a5a6a", color="#9a9aaa"); tree("LL", -2.6, -2.9, 0.7)
yard("PT", "patoffice.png", "marble.jpg"); table("PT", 0.9, -2.4, 2.0, 0.7, 1.0, "#2e4690")
for x in (-3.2, 3.2): box("PT", x, 0.04, -3.0, [0.5, 3.6, 0.5], color="#f4ece0")
yard("RS", "splitrules.png", "checker.jpg"); table("RS", 0, -2.0, 1.8, col="#e8d8b0"); tree("RS", -3.6, -3.8, 0.8); post("RS", 3.4, -3.4, 1.6, "#4a2a2a"); post("RS", 2.8, -4.2, 1.2, "#4a2a2a")
yard("CU", "parlour.png", "crimson.jpg"); table("CU", 0, -2.4, 2.0, 1.0, 0.72, "#6a3a2a"); box("CU", -3.0, 0.04, -3.0, [0.8, 0.9, 0.8], color="#8a2a3a"); box("CU", 3.0, 0.04, -3.2, [0.8, 0.9, 0.8], color="#8a2a3a")
yard("GU", "quiz.png", "stage.jpg"); box("GU", -1.2, 0.04, -2.2, [0.9, 1.0, 0.9], color="#3cb464"); box("GU", 1.2, 0.04, -2.2, [0.9, 1.0, 0.9], color="#dc3c3c")
yard("LS", "lecture.png", "wood.jpg"); box("LS", -2.2, 0.04, -2.7, [0.8, 1.1, 0.6], color="#8a5a3a"); box("LS", 3.2, 0.04, -3.2, [0.9, 0.6, 0.9], color="#c08a5a")
yard("HC", "cabin.png", "plank.jpg"); table("HC", 0, -2.4, 1.6, 0.9); crate("HC", -3.0, 0.04, -3.0, 0.6); crate("HC", 3.1, 0.04, -3.2, 0.5)
yard("SN", "seaside.png", "boards.jpg"); post("SN", -2.2, -2.6, 2.2, "#3a5a3a"); post("SN", 2.3, -2.8, 2.2, "#2a3a6a"); box("SN", -3.2, 0.04, -3.2, [1.4, 0.45, 0.5], color="#7a5030"); barrel("SN", 3.2, -3.0)
yard("DL", "living30.png", "olive.jpg"); table("DL", 0.4, -2.4, 1.6, 0.9, 0.7, "#7a4a2a"); box("DL", -3.0, 0.04, -3.0, [1.0, 0.8, 0.9], color="#9a5a3a")
yard("PB", "hq.png", "snow.jpg"); box("PB", -3.0, 0.04, -3.0, [1.6, 0.4, 1.0], color="#f0f4fa"); crate("PB", 2.8, 0.04, -2.6, 0.7); tree("PB", -3.6, -4.4, 0.8, "#2e7a56"); tree("PB", 3.6, -4.6, 0.9, "#2e7a56")
yard("LZ", "rainy.png", "rug.jpg"); table("LZ", 1.4, -2.4, 1.6, 0.8, 0.74, "#8a5a3a")
yard("CT", "court.png", "mustard.jpg"); box("CT", 0, 0.04, -3.6, [3.0, 1.2, 0.8], color="#824628"); table("CT", -2.8, -2.4, 1.4, 0.7, 0.7, "#9a5a30")
yard("FN", "gamenight.png", "purple.jpg"); table("FN", 0, -2.3, 2.0, 1.0, 0.45, tex="boardtex.jpg"); box("FN", -3.2, 0.04, -3.0, [1.2, 0.6, 0.8], color="#f07aa0")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
LG = pos("GB", -0.75, 0.05, -1.4)
human("lizG", "lizzie", LG, face="shouting"); human("fanG", "fan1", pos("GB", 0.8, 0.05, -2.0), face="happy"); put("cashG", "cash", pos("GB", 0.8, 0.72, -1.8), 0.55)
human("lizT", "lizzie", pos("TY", -0.6, 0.04, -1.6), face="happy"); put("typeT", "typew", pos("TY", 0.0, 0.78, -1.85), 0.5); put("boardT", "board", pos("TY", 1.2, 0.78, -1.8), 0.5)
human("lord", "landlord", pos("LL", -1.0, 0.04, -1.8), face="smug"); put("bagL", "mbag", pos("LL", -0.3, 0.04, -1.6), 0.7); human("ten", "tenant", pos("LL", 1.2, 0.04, -1.9), face="nervous")
human("lizP", "lizzie", pos("PT", -0.75, 0.04, -1.6), face="happy"); put("pat", "patent", pos("PT", -0.32, 0.85, -1.45), 0.55); put("boardP", "board", pos("PT", 0.9, 1.04, -2.3), 0.7)
put("bkG", "bookg", pos("RS", -0.5, 0.74, -1.9), 0.55); put("bkR", "bookr", pos("RS", 0.5, 0.74, -1.9), 0.55)
human("fan2R", "fan2", pos("RS", -1.7, 0.04, -1.9), face="happy"); human("tenR", "tenant", pos("RS", -2.4, 0.04, -2.6), face="happy"); put("cashR", "cash", pos("RS", -2.05, 0.04, -1.4), 0.45)
human("fanC", "fan1", pos("CU", -1.2, 0.04, -1.6), face="smug"); human("tenC", "tenant", pos("CU", 1.3, 0.04, -1.6), face="nervous")
put("cashC", "cash", pos("CU", -0.7, 0.76, -2.3), 0.4); put("bagC", "mbag", pos("CU", -0.15, 0.76, -2.3), 0.5)
put("bkG2", "bookg", pos("GU", -1.2, 1.04, -2.1), 0.8); put("bkR2", "bookr", pos("GU", 1.2, 1.04, -2.1), 0.8); human("lizQ", "lizzie", pos("GU", 0, 0.04, -2.9), face="nervous")
human("lizL", "lizzie", pos("LS", -0.7, 0.04, -2.0), face="happy"); put("bkGL", "bookg", pos("LS", -1.2, 0.85, -1.85), 0.45)
human("fan1L", "fan1", pos("LS", 0.8, 0.04, -1.5), face="smug"); put("bkRL", "bookr", pos("LS", 0.6, 0.8, -1.3), 0.42); human("fan2L", "fan2", pos("LS", 1.9, 0.04, -2.2), face="happy"); put("bkGT", "bookg", pos("LS", 1.55, 0.8, -2.05), 0.4)
human("fan2H", "fan2", pos("HC", -1.3, 0.04, -1.5), face="happy"); human("tenH", "tenant", pos("HC", 1.4, 0.04, -1.6), face="happy"); put("oilH", "oil", pos("HC", 0, 0.74, -2.35), 0.8)
human("fan1S", "fan1", pos("SN", -0.7, 0.04, -1.5), face="happy"); human("fan2S", "fan2", pos("SN", 0.8, 0.04, -1.8), face="happy")
human("darD", "darrow", pos("DL", -1.2, 0.04, -1.6), face="happy"); put("boardD", "board", pos("DL", 0.4, 0.74, -2.3), 0.6); human("fan2D", "fan2", pos("DL", 1.6, 0.04, -1.7), face="happy")
human("darP", "darrow", pos("PB", -0.6, 0.04, -1.6), face="happy"); put("bagP", "mbag", pos("PB", 0.15, 0.04, -1.4), 0.8)
human("lizZ", "lizzie", pos("LZ", -0.7, 0.04, -1.6), face="confused"); put("frZ", "frame", pos("LZ", 1.4, 0.78, -2.35), 0.9)
human("profC", "prof", pos("CT", -0.9, 0.04, -1.6), face="shouting"); put("opat", "oldpat", pos("CT", -0.25, 0.95, -1.45), 0.55); put("frC", "frame", pos("CT", 1.6, 1.24, -3.5), 0.9)
human("lizC", "lizzie", PARK, face="happy")
human("palF", "pal", pos("FN", -1.4, 0.04, -1.5), face="happy"); human("youF", "you", pos("FN", 1.4, 0.04, -1.5), face="shocked")
put("hotF", "houses", pos("FN", -0.1, 0.49, -2.3), 0.45); put("cashF", "cash", pos("FN", -0.6, 0.49, -2.0), 0.35); human("lizF", "lizzie", PARK, face="smug")
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


HOOK = dict(anchor=(0.0, 1.3, -1.7), dist=7.6, yaw=4, pitch=8)
# ---- 0-1.2 hook: Monopoly was invented / to make people hate monopolies. It did the exact opposite.
s = S("0", "GB", zoom=7, pan=(-3, 0), **HOOK); ft(s, "lizG", ["shouting", "shocked", "shouting"]); ft(s, "fanG", ["happy", "smug"]); act(s, 0.0, "lizG", pose=dict(armR=-150)); act(s, 0.1, "cashG", shake=0.3)
tag(s, 0.0, "hate", 0.3, 0.0, wf=0.62, hf=0.22); snap(s, max(0.82, rel(s, "invented")), 12)
s = crane("to make", "GB", (0.0, 0.8, -2.4), 9.4, -28, -6, 44, 12); ft(s, "lizG", ["shouting", "nervous"]); ft(s, "fanG", ["happy", "smug"]); act(s, 0.0, "cashG", shake=0.4)
s = S("It did the", "GB", (0.8, 1.25, -2.0), 5.0, 10, pitch=5, zoom=12, yawTo=0, dof=dict(focus="fanG", blur=0.4)); ft(s, "fanG", ["happy", "smug", "happy"]); T(s, "opposite", wf=0.6, hf=0.14); snap(s, rel(s, "opposite"), 14)
# ---- Lizzie Magie is a typist with a grudge.
s = crane("Lizzie Magie", "TY", (0.2, 1.3, -1.8), 8.6, -24, -4, 38, 6); ft(s, "lizT", ["happy", "smug"]); act(s, 0.1, "typeT", shake=0.3); T(s, "nmliz")
s = S("with a grudge", "TY", (-0.6, 1.25, -1.6), 4.8, 10, pitch=5, zoom=12, dof=dict(focus="lizT", blur=0.4)); ft(s, "lizT", ["sneaky", "shouting"]); T(s, "grudge", wf=0.6, hf=0.14); cfx(s, 0.2, "bang", "lizT", 0.6)
# ---- Landlords get rich just by owning land, and their tenants pay for it.
s = crane("Landlords get", "LL", (0.1, 1.3, -1.9), 9.0, 22, 2, 36, 6); ft(s, "lord", ["smug", "happy"]); ft(s, "ten", ["nervous", "confused"]); act(s, 0.1, "bagL", shake=0.3); T(s, "rich")
s = S("just by owning", "LL", (-0.8, 1.25, -1.8), 5.4, -10, pitch=5, zoom=10, yawTo=2, dof=dict(focus="lord", blur=0.4)); ft(s, "lord", ["smug", "sneaky", "smug"]); T(s, "owning"); snap(s, rel(s, "land"), 12)
s = S("and their tenants", "LL", (1.2, 1.25, -1.9), 5.2, 12, pitch=5, zoom=10, pan=(-3, 0), dof=dict(focus="ten", blur=0.4)); ft(s, "ten", ["nervous", "shocked", "nervous"]); T(s, "tenants"); cfx(s, 0.3, "sweat", "ten", 0.8)
# ---- So she designs a board game to prove it.
s = crane("So she designs", "TY", (0.6, 1.2, -1.9), 7.8, 26, 6, 40, 8); ft(s, "lizT", ["happy", "smug"]); T(s, "designs")
s = S("to prove it", "TY", (1.2, 1.03, -1.8), 3.8, -8, pitch=4, yawTo=4, type="macro", dof=dict(focus="boardT", blur=0.5)); T(s, "prove", wf=0.6, hf=0.14); snap(s, 0.3, 12)
# ---- She patents it in 1904. The Landlord's Game.
s = crane("She patents", "PT", (0.1, 1.3, -1.8), 9.0, -22, -2, 34, 6); ft(s, "lizP", ["happy", "smug"]); act(s, 0.1, "pat", shake=0.3); T(s, "y1904", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("The Landlord's", "PT", (0.9, 1.39, -2.3), 4.2, 10, pitch=4, yawTo=-2, type="macro", dof=dict(focus="boardP", blur=0.5)); T(s, "llgame"); snap(s, rel(s, "Game"), 14)
# ---- Here's the strange part. It ships with two rule sets.
s = crane("Here's the strange", "RS", (-0.7, 1.0, -2.1), 11.0, 30, 4, 46, 10); ft(s, "fan2R", ["happy", "confused"]); T(s, "strange")
s = S("It ships", "RS", (0.0, 1.0, -1.9), 4.0, -6, pitch=4, yawTo=6, type="macro", dof=dict(focus="bkR", blur=0.5)); act(s, 0.1, "bkG", shake=0.3); act(s, 0.5, "bkR", shake=0.3); T(s, "tworules", dy=0.3, wf=0.55); snap(s, rel(s, "two"), 14)
# ---- In one, every player gets richer whenever anyone earns.
s = S("In one", "RS", (-2.1, 1.4, -2.1), 5.4, -14, pitch=5, zoom=10, pan=(3, 0)); ft(s, "fan2R", ["happy", "smug"]); ft(s, "tenR", ["happy", "shocked", "happy"]); act(s, 0.1, "cashR", shake=0.3); T(s, "richer"); snap(s, rel(s, "richer"), 12); cfx(s, 0.4, "glint", "fan2R", 0.7)
s = S("whenever anyone", "RS", (-0.5, 1.0, -1.9), 3.0, 10, pitch=4, zoom=12, type="macro", dof=dict(focus="bkG", blur=0.5)); act(s, 0.1, "bkG", shake=0.3); T(s, "earns")
# ---- In the other, you crush your friends with rent until they go broke.
s = crane("In the other", "CU", (0.0, 1.3, -1.9), 9.0, -24, -2, 36, 6); ft(s, "fanC", ["smug", "sneaky"]); ft(s, "tenC", ["nervous", "shocked"]); act(s, 0.1, "bagC", shake=0.3); T(s, "crush")
s = S("until they go", "CU", (1.3, 1.25, -1.6), 4.9, -10, pitch=5, zoom=12, dof=dict(focus="tenC", blur=0.4)); ft(s, "tenC", ["shocked", "nervous", "shocked"]); T(s, "broke"); snap(s, rel(s, "broke"), 14); cfx(s, 0.3, "sweat", "tenC", 0.8)
# ---- Guess which one people loved.
s = crane("Guess which", "GU", (0.0, 1.4, -2.3), 9.4, 20, 0, 30, 6); ft(s, "lizQ", ["nervous", "confused"]); act(s, 0.2, "bkG2", shake=0.3); act(s, 0.6, "bkR2", shake=0.3); T(s, "guess", dy=0.3, wf=0.58)
# ---- You see, Lizzie meant the cruel rules as a warning. Play them, feel how unfair they are, then switch to the fair ones.
s = crane("You see Lizzie", "LS", (0.45, 1.3, -1.9), 10.4, -18, -2, 30, 6); ft(s, "lizL", ["shouting", "happy"]); ft(s, "fan1L", ["smug", "neutral"]); ft(s, "fan2L", ["confused", "happy"]); act(s, 0.0, "lizL", pose=dict(armR=-150))
s = S("as a warning", "LS", (-0.7, 1.25, -2.0), 5.0, 12, pitch=5, zoom=12, dof=dict(focus="lizL", blur=0.4)); ft(s, "lizL", ["shouting", "nervous"]); act(s, 0.1, "bkGL", shake=0.3); T(s, "warning"); snap(s, rel(s, "warning"), 12)
s = S("Play them", "LS", (1.35, 1.25, -1.7), 6.6, 12, pitch=5, zoom=6, yawTo=4); ft(s, "fan1L", ["smug", "happy"]); ft(s, "fan2L", ["nervous", "shocked"]); act(s, 0.1, "bkRL", shake=0.3); c_ = T(s, "play", wf=0.5, hf=0.13)
swap(s, c_, rel(s, "feel"), "unfair", wf=0.58, hf=0.14); snap(s, rel(s, "unfair"), 12); cfx(s, rel(s, "unfair"), "sweat", "fan2L", 0.7)
s = S("then switch", "LS", (-0.7, 1.25, -2.0), 5.0, -10, pitch=5, zoom=12, dof=dict(focus="lizL", blur=0.4)); ft(s, "lizL", ["happy", "smug"]); act(s, 0.1, "bkGL", shake=0.3); T(s, "switch")
# ---- But players skipped the lesson and kept the cruelty.
s = S("But players", "LS", (1.3, 1.25, -1.8), 6.2, -8, pitch=6, zoom=8, yawTo=6); ft(s, "fan1L", ["smug", "sneaky"]); ft(s, "fan2L", ["smug", "happy"]); act(s, 0.1, "bkGT", shake=0.4); hide(s, 0.45, "bkGT"); T(s, "skipped")
s = S("and kept the", "LS", (0.8, 1.25, -1.5), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="fan1L", blur=0.4), _dis=1); hide(s, 0.0, "lizL"); hide(s, 0.0, "fan2L"); hide(s, 0.0, "bkGL"); ft(s, "fan1L", ["sneaky", "smug"]); act(s, 0.1, "bkRL", shake=0.3); T(s, "kept", wf=0.6, hf=0.14); snap(s, rel(s, "cruelty"), 12)
# ---- For years, fans copied the board by hand.
s = crane("For years", "HC", (0.0, 1.3, -1.9), 9.4, 22, 2, 40, 8); ft(s, "fan2H", ["happy", "smug"]); ft(s, "tenH", ["happy", "neutral"]); T(s, "years", wf=0.5, hf=0.13)
s = S("copied the board", "HC", (0.0, 1.15, -2.35), 3.6, -8, pitch=4, yawTo=4, type="macro", dof=dict(focus="oilH", blur=0.5)); act(s, 0.1, "oilH", shake=0.2); T(s, "byhand")
# ---- Players swapped in their own local street names.
s = crane("Players swapped", "SN", (0.0, 1.3, -1.8), 9.0, -20, -2, 30, 6); ft(s, "fan1S", ["happy", "smug"]); ft(s, "fan2S", ["happy", "shocked"]); act(s, 0.0, "fan1S", pose=dict(armR=-150)); T(s, "streets")
s = S("local street", "SN", (0.1, 1.5, -2.0), 6.4, 14, pitch=5, zoom=8, yawTo=4); ft(s, "fan1S", ["smug", "happy"]); ft(s, "fan2S", ["happy", "smug"])
T(s, "st1", dy=0.34, dx=-0.15, wf=0.4, hf=0.11); T(s, "st2", 0.25, dy=0.2, dx=0.12, wf=0.4, hf=0.11); snap(s, rel(s, "names"), 12)
# ---- Then a man named Charles Darrow learned the game from friends, called it his own invention, and sold it to Parker Brothers in 1935.
s = crane("Then a man", "DL", (0.2, 1.3, -1.9), 9.2, 22, 0, 36, 6); ft(s, "darD", ["happy", "smug"]); ft(s, "fan2D", ["happy", "neutral"]); T(s, "nmdarrow")
s = S("learned the game", "DL", (0.4, 1.04, -2.3), 3.4, -12, pitch=5, yawTo=0, type="macro", dof=dict(focus="boardD", blur=0.5)); act(s, 0.1, "boardD", shake=0.2); T(s, "friends")
s = S("called it his", "DL", (-1.2, 1.25, -1.6), 4.8, 10, pitch=5, zoom=12, dof=dict(focus="darD", blur=0.4)); ft(s, "darD", ["sneaky", "smug"]); T(s, "myown"); snap(s, rel(s, "invention"), 14); cfx(s, 0.3, "glint", "darD", 0.7)
s = crane("and sold it", "PB", (0.0, 1.3, -1.8), 8.8, -24, -4, 34, 6); ft(s, "darP", ["happy", "smug"]); act(s, 0.0, "darP", pose=dict(armR=-150, armL=150)); T(s, "parker")
s = S("in 1935", "PB", (-0.2, 1.5, -1.6), 6.0, 12, pitch=5, zoom=10, yawTo=4, pan=(-3, 0)); ft(s, "darP", ["smug", "happy"]); act(s, 0.1, "bagP", shake=0.4); T(s, "y1935", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
# ---- And Lizzie? Parker Brothers bought her patent for 500 dollars. Her name disappeared.
s = crane("And Lizzie", "LZ", (0.2, 1.3, -1.9), 8.8, 20, 2, 34, 6); ft(s, "lizZ", ["confused", "nervous"]); T(s, "andliz", wf=0.52, hf=0.13); cfx(s, 0.3, "question", "lizZ", 0.8)
s = S("Parker Brothers bought", "LZ", (0.35, 1.3, -1.9), 8.0, 14, pitch=14, pitchTo=4, zoom=8); ft(s, "lizZ", ["nervous", "confused"]); act(s, 0.1, "frZ", shake=0.2)
s = S("for 500", "LZ", (-0.7, 1.25, -1.6), 4.8, -10, pitch=5, zoom=12, dof=dict(focus="lizZ", blur=0.4)); ft(s, "lizZ", ["shocked", "nervous"]); T(s, "d500", dy=0.3, wf=0.55); snap(s, rel(s, "500"), 14)
s = S("Her name", "LZ", (1.4, 1.23, -2.35), 3.8, 8, pitch=4, yawTo=-2, type="macro", dof=dict(focus="frZ", blur=0.5)); act(s, rel(s, "disappeared"), "frZ", face="gone"); T(s, "gone")
# ---- Decades later, an economics professor fighting Parker Brothers in court dug up her old patents. The truth came back.
s = crane("Decades later", "CT", (0.0, 1.4, -2.2), 9.6, -22, -2, 36, 8); act(s, 0.0, "frC", face="gone"); ft(s, "profC", ["shouting", "smug"]); T(s, "decades", wf=0.56, hf=0.13)
s = S("an economics", "CT", (-0.9, 1.25, -1.6), 4.8, 10, pitch=5, zoom=12, dof=dict(focus="profC", blur=0.4)); ft(s, "profC", ["shouting", "happy"]); act(s, 0.0, "profC", pose=dict(armR=-150)); T(s, "nmprof"); cfx(s, 0.3, "bang", "profC", 0.6)
s = S("fighting Parker", "CT", (0.0, 2.0, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="timeline", title="IN COURT", items=["1904", "1935", "DECADES LATER"]))
s = S("dug up her", "CT", (-0.65, 1.2, -1.5), 4.6, -8, pitch=5, zoom=12, dof=dict(focus="opat", blur=0.4)); ft(s, "profC", ["happy", "shocked"]); act(s, 0.1, "opat", shake=0.3); T(s, "dug"); snap(s, rel(s, "patents"), 12)
s = S("The truth came", "CT", (1.3, 1.5, -2.6), 6.0, 12, pitch=6, zoom=10, yawTo=2); act(s, 0.0, "frC", face="default"); show(s, 0.05, "lizC", pos("CT", 0.7, 0.04, -2.0)); ft(s, "lizC", ["happy", "smug"]); T(s, "truth"); cfx(s, 0.4, "blush", "lizC", 0.8)
# ---- So the next time a friend bankrupts you on Boardwalk, that sting is the whole point.
s = crane("So the next", "FN", (0.0, 1.3, -1.9), 9.4, 24, 2, 36, 6); ft(s, "palF", ["happy", "smug"]); ft(s, "youF", ["shocked", "nervous"]); act(s, 0.0, "palF", pose=dict(armR=-150)); T(s, "nexttime")
s = S("on Boardwalk", "FN", (1.4, 1.25, -1.5), 4.8, -10, pitch=5, zoom=12, dof=dict(focus="youF", blur=0.4)); ft(s, "youF", ["shocked", "nervous", "shocked"]); c_ = T(s, "bwalk", dy=0.28, wf=0.3, hf=0.3); snap(s, rel(s, "Boardwalk"), 14)
swap(s, c_, rel(s, "that"), "sting", wf=0.5, hf=0.13); cfx(s, rel(s, "sting"), "sweat", "youF", 0.7)
s = S("is the whole", "FN", (0.0, 1.4, -3.4), 5.2, 8, pitch=6, zoom=12, yawTo=-2, _dis=1); show(s, 0.0, "lizF", pos("FN", 0.0, 0.04, -3.6), hop=0.15); [hide(s, 0.0, c) for c in ("palF", "youF", "cashF")]; ft(s, "lizF", ["smug", "happy", "sneaky"]); T(s, "point", dy=0.3, wf=0.55); cfx(s, 0.4, "blush", "lizF", 0.7)
# ---- Because Monopoly was invented / to make people hate monopolies. (pull-out onto the hook frame)
s = crane("Because Monopoly", "GB", (0.0, 0.9, -2.4), 9.4, 26, 6, 44, 10); ft(s, "lizG", ["shouting", "shocked"]); ft(s, "fanG", ["happy", "smug"]); act(s, 0.1, "cashG", shake=0.3)
s = S("to make#2", "GB", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "lizG", ["shouting", "shocked", "shouting"]); ft(s, "fanG", ["happy", "smug"])
act(s, 0.0, "cashG", shake=0.4); act(s, 0.0, "lizG", pose=dict(armR=-150)); tag(s, 0.05, "hate", 0.3, 0.0, wf=0.62, hf=0.22)

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
ATM = dict(GB=dict(dust=D_(24), rays=dict(angle=30, intensity=0.6)), TY=dict(dust=D_(24), rays=dict(angle=32, intensity=0.55)), LL=dict(dust=D_(18), rays=dict(angle=26, intensity=0.5)),
           PT=dict(dust=D_(20), rays=dict(angle=36, intensity=0.5)), RS=dict(dust=D_(20), rays=dict(angle=30, intensity=0.45)), CU=dict(bokeh=BK(0.35)), GU=dict(bokeh=BK(0.4)),
           LS=dict(dust=D_(18), rays=dict(angle=28, intensity=0.45)), HC=dict(dust=D_(22), rays=dict(angle=34, intensity=0.5)), SN=dict(dust=D_(16), rays=dict(angle=20, intensity=0.6)),
           DL=dict(bokeh=BK(0.3)), PB=dict(dust=D_(26), rays=dict(angle=30, intensity=0.4)), LZ=dict(bokeh=BK(0.4)), CT=dict(dust=D_(26), rays=dict(angle=36, intensity=0.7)), FN=dict(bokeh=BK(0.45)))
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
MOOD = dict(GB="gold", TY="peach", LL="lav", PT="marble", RS="split", CU="crimson", GU="quiz", LS="teal", HC="cabin", SN="sunset", DL="olive", PB="snow", LZ="rain", CT="court", FN="neon")
light, cur = [{"t": 0, "mood": "gold"}], "gold"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 15,
    "moods": {"gold": {"sun": {"azimuth": -30, "elevation": 20, "color": "#ffd08a", "intensity": 2.50}, "sky": {"top": "#3aa882", "horizon": "#ffd27a"}, "fill": {"sky": "#ffe0a0", "ground": "#406850", "intensity": 1.60}}, "peach": {"sun": {"azimuth": 50, "elevation": 40, "color": "#fff0dc", "intensity": 2.40}, "sky": {"top": "#ffd8bc", "horizon": "#ffc8a0"}, "fill": {"sky": "#fff0d8", "ground": "#806048", "intensity": 1.35}}, "lav": {"sun": {"azimuth": -40, "elevation": 30, "color": "#ffe6b0", "intensity": 2.40}, "sky": {"top": "#b496e6", "horizon": "#ffd68c"}, "fill": {"sky": "#e0d0ff", "ground": "#5a6a50", "intensity": 1.40}}, "marble": {"sun": {"azimuth": 30, "elevation": 50, "color": "#fffaf0", "intensity": 2.40}, "sky": {"top": "#f6ecdc", "horizon": "#e8dcc8"}, "fill": {"sky": "#ffffff", "ground": "#807060", "intensity": 1.35}}, "split": {"sun": {"azimuth": 0, "elevation": 45, "color": "#fff4e0", "intensity": 2.40}, "sky": {"top": "#78c8fa", "horizon": "#f06a4a"}, "fill": {"sky": "#fff0e0", "ground": "#706050", "intensity": 1.40}}, "crimson": {"sun": {"azimuth": 20, "elevation": 35, "color": "#ffb070", "intensity": 2.50}, "sky": {"top": "#a02838", "horizon": "#e06a50"}, "fill": {"sky": "#ffb0a0", "ground": "#602830", "intensity": 1.85}}, "quiz": {"sun": {"azimuth": 0, "elevation": 50, "color": "#ffe8ff", "intensity": 2.50}, "sky": {"top": "#5a28a0", "horizon": "#dc5ac8"}, "fill": {"sky": "#ffb0ff", "ground": "#5a3080", "intensity": 1.90}}, "teal": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fff4e6", "intensity": 2.40}, "sky": {"top": "#3caaaa", "horizon": "#6ec8be"}, "fill": {"sky": "#e0fff8", "ground": "#605048", "intensity": 1.40}}, "cabin": {"sun": {"azimuth": -30, "elevation": 35, "color": "#ffd8a0", "intensity": 2.40}, "sky": {"top": "#c8e0fa", "horizon": "#ffd0a0"}, "fill": {"sky": "#ffe8c8", "ground": "#705038", "intensity": 1.50}}, "sunset": {"sun": {"azimuth": 200, "elevation": 15, "color": "#ffc890", "intensity": 2.40}, "sky": {"top": "#fa7896", "horizon": "#ffc878"}, "fill": {"sky": "#ffc0c8", "ground": "#705050", "intensity": 1.50}}, "olive": {"sun": {"azimuth": 30, "elevation": 35, "color": "#ffe0a0", "intensity": 2.40}, "sky": {"top": "#789a5a", "horizon": "#a0b070"}, "fill": {"sky": "#f0f0c0", "ground": "#5a5030", "intensity": 1.55}}, "snow": {"sun": {"azimuth": 40, "elevation": 30, "color": "#fff8f0", "intensity": 2.40}, "sky": {"top": "#78aae6", "horizon": "#dcecfa"}, "fill": {"sky": "#e0f0ff", "ground": "#8090a0", "intensity": 1.40}}, "rain": {"sun": {"azimuth": 150, "elevation": 35, "color": "#c8d0ff", "intensity": 2.60}, "sky": {"top": "#4a508c", "horizon": "#7a80b8"}, "fill": {"sky": "#b0b8ff", "ground": "#404060", "intensity": 1.95}}, "court": {"sun": {"azimuth": -20, "elevation": 40, "color": "#ffd89a", "intensity": 2.50}, "sky": {"top": "#c88246", "horizon": "#e6a060"}, "fill": {"sky": "#ffe0b0", "ground": "#704020", "intensity": 1.45}}, "neon": {"sun": {"azimuth": 0, "elevation": 40, "color": "#ffd0f0", "intensity": 2.60}, "sky": {"top": "#783ca0", "horizon": "#e664aa"}, "fill": {"sky": "#ffb0e0", "ground": "#503070", "intensity": 1.95}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ffcf3c", "paper": ["#e8d6a8", "#d4bc86"], "dofPx": 8, "particle": "#fff0c0", "bokehColor": "#ffb0d8", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(hook="Monopoly", tomake="to make", opp="It did the", liz="Lizzie Magie", typ="typist", grudge="with a grudge", lords="Landlords get", owning="just by owning", ten="and their tenants",
           designs="So she designs", prove="to prove it", pat="She patents", llg="The Landlord's", strange="Here's the strange", ships="It ships", one="In one", earns="whenever anyone",
           other="In the other", broke="until they go", guess="Guess which", yousee="You see Lizzie", play="Play them", feel="feel how", switch="then switch", skipped="But players", kept="and kept the",
           years="For years", copied="copied the board", swapped="Players swapped", local="local street", then="Then a man", learned="learned the game", called="called it his", sold="and sold it",
           y35="in 1935", andliz="And Lizzie", bought="Parker Brothers bought", d500="for 500", name="Her name", decades="Decades later", econ="an economics", fight="fighting Parker", dug="dug up her",
           truth="The truth came", sonext="So the next", bwalk="on Boardwalk", sting="that sting", point="is the whole", because="Because Monopoly", tomake2="to make#2")
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
