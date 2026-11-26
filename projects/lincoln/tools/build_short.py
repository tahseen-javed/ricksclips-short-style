#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 29: Abraham Lincoln is in the Wrestling Hall of Fame.
usage: build_short.py <project folder>
Eleven wrestling-poster sets 70 units apart: RG tangerine starburst arena with a turquoise ring (hook + loop; a "?" moon = open loop, resolved
when the almanac moon sets), HF turquoise trophy hall, PR butter prairie, CP peach-teal 1832 camp, NS mint New Salem, FT coral fight circle,
FR honey firefly dusk, CT oxblood courtroom, JL lilac jail, MN navy moon meadow, AL amber candlelit study. Shots 0.7-2 s, every neighbour a
different move; props and places are the stars, people mostly small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(RG=0, HF=70, PR=140, CP=210, NS=280, FT=350, FR=420, CT=490, JL=560, MN=630, AL=700)
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


yard("RG", "arena.png", "pave.jpg"); box("RG", 0, 0.04, -2.6, [5.0, 0.46, 4.0], texture="mat.jpg", repeat=[3, 3])
for sx in (-2.4, 2.4):
    for sz in (-0.8, -4.4): box("RG", sx, 0.5, sz, [0.18, 1.4, 0.18], color="#ffc83c")
    for hy in (0.95, 1.35, 1.75): box("RG", sx, hy, -2.6, [0.05, 0.05, 3.6], color="#ff5a8a")
for hy in (0.95, 1.35, 1.75): box("RG", 0, hy, -4.4, [4.8, 0.05, 0.05], color="#ff5a8a")
box("RG", 0.85, 0.5, -2.3, [0.5, 0.45, 0.5], color="#ffc83c")
yard("HF", "trophyhall.png", "marble.jpg"); box("HF", 3.5, 0.04, -2.6, [1.0, 0.6, 0.8], color="#f5c842"); box("HF", -3.0, 0.04, -3.6, [0.7, 1.0, 0.7], color="#e8f4f0")
yard("PR", "prairie.png", "prairie.jpg"); tree("PR", -3.4, -4.4, 0.9, "#7fae4a"); tree("PR", 4.8, -4.2, 1.0, "#8ab84e"); barrel("PR", -1.6, -3.6)
yard("CP", "camp.png", "campdirt.jpg"); crate("CP", -3.0, 0, -3.6); barrel("CP", 2.5, -3.8); box("CP", 6.0, 0.04, -3.4, [0.6, 0.3, 0.6], color="#a86a40")
yard("NS", "salem.png", "grass.jpg"); tree("NS", -3.2, -4.0, 1.0, "#5faa6e"); tree("NS", 3.4, -4.4, 1.1, "#6ab878"); crate("NS", 2.0, 0, -3.6)
yard("FT", "duskring.png", "dust.jpg"); barrel("FT", -3.4, -3.4); crate("FT", 3.6, 0, -3.8)
yard("FR", "fireflies.png", "meadow.jpg"); tree("FR", -3.4, -4.2, 1.0, "#9aa84a"); post("FR", 2.4, -3.6, 1.2, "#8a6a40"); post("FR", 4.6, -3.6, 1.2, "#8a6a40")
yard("CT", "court.png", "courtfl.jpg")
yard("JL", "jail.png", "stone.jpg"); box("JL", 1.2, 0.04, -3.0, [0.5, 0.45, 0.5], color="#8a7aa0")
yard("MN", "moonfield.png", "nightgr.jpg"); tree("MN", 3.6, -4.6, 1.0, "#3a7a6a")
yard("AL", "study.png", "studyfl.jpg"); box("AL", 0.6, 0.04, -2.6, [1.8, 0.8, 1.0], color="#8a5a3a")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
human("abeR", "abe", pos("RG", -0.35, 0.5, -2.5), face="happy", h=1.75); put("belt_R", "belt", pos("RG", 0.85, 0.95, -2.3), 0.38); put("moonq_R", "moon", pos("RG", 1.05, 1.3, -4.4), 0.6, face="q")
put("maskH", "masked", pos("HF", 0.0, 0.04, -2.6), 1.3); human("abeH", "abe", pos("HF", 3.5, 0.64, -2.6), face="happy", h=1.6)
human("abeyP", "abey", pos("PR", 1.4, 0.04, -2.2), face="happy", h=1.8); put("ruler_P", "ruler", pos("PR", 2.3, 0.04, -2.4), 2.0)
human("abeyC", "abey", pos("CP", -0.9, 0.04, -2.2), face="happy", h=1.8); human("thompsonC", "thompson", pos("CP", 0.9, 0.04, -2.2), face="happy", h=1.8); put("flopC", "flop", pos("CP", 4.2, 0.04, -2.4), 0.9)
human("jackN", "jack", pos("NS", 0.0, 0.04, -2.2), face="happy", h=1.85)
put("brawlF", "brawl", pos("FT", 0.0, 0.04, -2.8), 1.3); put("crowd_F", "crowd", pos("FT", 0.0, 0.04, -4.4), 0.9); put("betsF", "bets", PARK, 0.8)
human("abeyF", "abey", pos("FR", -0.55, 0.04, -2.2), face="happy", h=1.8); human("jackF", "jack", pos("FR", 0.55, 0.04, -2.2), face="happy", h=1.85); put("palsF", "pals", pos("FR", 3.4, 0.9, -2.4), 0.8)
put("benchT", "bench", pos("CT", 0.0, 0.04, -3.4), 1.4); human("duffT", "duff", pos("CT", -1.0, 0.04, -2.4), face="happy", h=1.6); human("abe58T", "abe58", pos("CT", 1.0, 0.04, -2.4), face="happy", h=1.75)
human("duffJ", "duff", pos("JL", 0.0, 0.04, -2.2), face="happy", h=1.6)
put("moonM", "moon", pos("MN", 0.0, 1.6, -4.4), 2.0); human("witnessM", "witness", pos("MN", -1.2, 0.04, -2.2), face="happy", h=1.7)
put("almA", "almanac", pos("AL", 0.6, 0.84, -2.6), 0.75); human("abe58A", "abe58", pos("AL", -1.3, 0.04, -2.3), face="happy", h=1.75); put("tagA", "tag", PARK, 0.42)
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


HOOK = dict(anchor=(0.0, 1.3, -2.5), dist=6.4, yaw=4, pitch=6)
# ---- A president is in the Wrestling Hall of Fame. Not a pro wrestler. Abraham Lincoln.
s = S("0", "RG", zoom=8, **HOOK); act(s, 0.0, "abeR", face="smug", pose=dict(armR=-150), shake=0.4); tag(s, 0.0, "hookc", 0.34, 0.0, wf=0.62, hf=0.2); act(s, 0.3, "moonq_R", shake=0.4); act(s, 0.5, "belt_R", shake=0.4)
ft(s, "abeR", ["smug", "shocked"]); snap(s, rel(s, "Fame"), 10)
s = S("Not a pro", "HF", (0.0, 0.75, -2.6), 4.6, -12, pitch=6, yawTo=4, type="macro", dof=dict(focus="maskH", blur=0.5)); act(s, rel(s, "pro"), "maskH", face="no", shake=0.7); T(s, "notpro", at=rel(s, "pro"), dy=0.38, wf=0.5)
s = S("Abraham Lincoln", "HF", (3.5, 1.45, -2.6), 5.0, 8, pitch=5, zoom=-10, dof=dict(focus="abeH", blur=0.4)); ft(s, "abeH", ["smug", "happy"]); T(s, "abec", at=0.05, dy=0.37, wf=0.5)
# ---- Before the beard and top hat, Lincoln was a six-foot-four frontier wrestler. Legend says about 300 matches.
s = S("Before the beard", "RG", (-0.35, 1.6, -2.5), 4.6, 12, pitch=5, yawTo=-4, dof=dict(focus="abeR", blur=0.4)); act(s, 0.0, "abeR", pose=dict(armR=0)); ft(s, "abeR", ["confused", "happy"])
s = S("Lincoln was a", "PR", (1.85, 1.1, -2.3), 5.6, 0, pitch=16, pitchTo=2); ft(s, "abeyP", ["happy", "smug"]); T(s, "ft64", at=rel(s, "was") + 0.2, dy=0.36, wf=0.6); snap(s, rel(s, "was") + 0.25, 8)
s = S("frontier wrestler", "PR", (1.4, 1.0, -2.2), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="abeyP", blur=0.4)); act(s, 0.05, "abeyP", pose=dict(armR=-150), shake=0.3); ft(s, "abeyP", ["smug", "happy"]); cfx(s, 0.2, "glint", "abeyP", 0.6)
s = S("Legend says", "PR", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="LEGEND SAYS", items=["300 MATCHES"]))
# ---- The only recorded loss came in 1832, to a soldier named Thompson.
s = crane("The only recorded", "CP", (0.0, 1.0, -2.2), 7.0, 22, 2, 36, 8); ft(s, "thompsonC", ["smug", "happy"]); ft(s, "abeyC", ["happy", "nervous"])
s = S("1832", "CP", (4.2, 0.55, -2.4), 4.6, -12, pitch=8, yawTo=4, type="macro", dof=dict(focus="flopC", blur=0.5)); act(s, 0.05, "flopC", shake=0.5); T(s, "y1832", at=0.05, dx=-0.24, dy=0.22, wf=0.26, hf=0.26); snap(s, 0.15, 8)
s = S("to a soldier", "CP", (0.9, 1.1, -2.2), 4.8, 10, pitch=5, zoom=12, dof=dict(focus="thompsonC", blur=0.4)); ft(s, "thompsonC", ["smug", "happy"]); T(s, "thomp", at=rel(s, "soldier"), dy=0.37, wf=0.6)
# ---- His most famous fight was in New Salem, against the town tough, Jack Armstrong. Crowds bet money. Armstrong walked away his friend.
s = crane("His most famous", "NS", (0.0, 1.0, -2.4), 8.0, -22, -2, 38, 8); T(s, "salemc", at=rel(s, "New"), dy=0.34, wf=0.5); ft(s, "jackN", ["smug", "happy"])
s = S("against the town", "FT", (0.0, 0.75, -2.8), 5.0, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="brawlF", blur=0.5)); act(s, 0.05, "brawlF", shake=0.7)
s = S("Jack Armstrong", "NS", (0.0, 1.1, -2.2), 4.6, 6, pitch=5, zoom=14, dof=dict(focus="jackN", blur=0.4)); ft(s, "jackN", ["smug", "shocked"]); T(s, "jackc", at=0.05, dy=0.37, wf=0.5); snap(s, 0.15, 10)
s = S("Crowds bet money", "FT", (0.3, 0.8, -3.2), 7.4, 8, pitch=10, zoom=4, pan=(8, 0)); hide(s, 0.0, "brawlF"); act(s, 0.0, "crowd_F", face="cheer", shake=0.3); show(s, rel(s, "bet"), "betsF", pos("FT", 1.0, 0.04, -2.2)); T(s, "betc", at=0.05, dy=0.36, wf=0.56)
s = S("Armstrong walked away", "FR", (0.0, 1.0, -2.2), 6.4, -10, pitch=6, zoom=-10); ft(s, "abeyF", ["happy", "smug"]); ft(s, "jackF", ["happy", "smug"]); T(s, "friendc", at=rel(s, "friend"), dy=0.36, wf=0.5); cfx(s, rel(s, "friend"), "blush", "jackF", 0.8)
# ---- You see, that friendship mattered. In 1858, Jack's son Duff was charged with murder. Lincoln defended him for free.
s = S("You see that", "FR", (3.4, 1.3, -2.4), 4.4, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="palsF", blur=0.5)); act(s, 0.05, "palsF", shake=0.4)
s = crane("In 1858", "CT", (0.0, 1.2, -3.0), 8.0, 22, 2, 36, 8); hide(s, 0.0, "duffT"); hide(s, 0.0, "abe58T"); T(s, "y1858", at=rel(s, "1858"), dx=-0.24, dy=0.22, wf=0.26, hf=0.26)
s = S("Jack's son Duff", "JL", (0.0, 1.0, -2.2), 4.4, -8, pitch=5, zoom=12, dof=dict(focus="duffJ", blur=0.4)); ft(s, "duffJ", ["nervous", "shocked"]); T(s, "duffc", at=0.05, dy=0.37, wf=0.5); cfx(s, 0.3, "sweat", "duffJ", 0.6)
s = S("charged with murder", "CT", (0.0, 0.9, -3.4), 5.6, 12, pitch=14, pitchTo=4, dof=dict(focus="benchT", blur=0.4)); act(s, rel(s, "charged"), "benchT", face="bang", shake=0.7); snap(s, rel(s, "charged") + 0.05, 10)
s = S("Lincoln defended him", "AL", (-0.9, 1.15, -2.3), 5.0, -12, pitch=6, yawTo=4); hide(s, 0.0, "almA"); ft(s, "abe58A", ["smug", "happy"]); show(s, rel(s, "free") - 0.1, "tagA", pos("AL", -0.5, 1.4, -2.2)); T(s, "freec", at=rel(s, "free"), dy=0.37, wf=0.4)
# ---- A witness swore he saw everything by moonlight. Lincoln opened an almanac. The moon had almost set. Not guilty.
s = S("A witness swore", "MN", (-0.5, 1.6, -2.6), 6.6, 8, pitch=5, zoom=8); act(s, 0.05, "witnessM", pose=dict(armR=-150)); ft(s, "witnessM", ["smug", "shocked"]); cfx(s, 0.3, "question", "witnessM", 0.6)
s = S("everything by moonlight", "MN", (0.0, 2.6, -4.4), 5.8, -10, pitch=4, yawTo=6, type="macro", dof=dict(focus="moonM", blur=0.4)); hide(s, 0.0, "witnessM"); act(s, 0.05, "moonM", shake=0.3); T(s, "moonc", at=rel(s, "moonlight"), dy=0.36, wf=0.5)
s = S("Lincoln opened an", "AL", (0.6, 1.2, -2.6), 4.4, 8, pitch=10, zoom=12, dof=dict(focus="almA", blur=0.4)); hide(s, 0.0, "tagA"); show(s, 0.0, "almA", pos("AL", 0.6, 0.84, -2.6), hop=0); act(s, rel(s, "almanac"), "almA", face="open", shake=0.5); snap(s, rel(s, "almanac") + 0.05, 8)
s = S("The moon had", "MN", (0.0, 2.3, -4.4), 6.4, 4, pitch=8, zoom=4, pan=(-8, 0)); act(s, 0.0, "moonM", face="set"); go(s, 0.1, "moonM", pos("MN", 0.0, 1.3, -4.4), 1.0, walk=False); T(s, "setc", at=rel(s, "almost"), dy=0.36, wf=0.5)
s = S("Not guilty", "CT", (0.0, 1.1, -2.8), 8.0, -8, pitch=5, zoom=-10); act(s, 0.0, "benchT", face="default"); show(s, 0.0, "duffT", pos("CT", -1.0, 0.04, -2.4), hop=0.3); show(s, 0.0, "abe58T", pos("CT", 1.0, 0.04, -2.4), hop=0)
ft(s, "duffT", ["happy", "smug"]); ft(s, "abe58T", ["smug", "happy"]); T(s, "notg", at=0.05, dy=0.35, wf=0.5)
# ---- One wrestling match won a friend and saved his son. That is the man in the Wrestling Hall of Fame.
s = S("won a friend", "FR", (0.0, 1.0, -2.2), 5.6, 12, pitch=5, yawTo=-4); ft(s, "abeyF", ["happy", "smug"]); ft(s, "jackF", ["smug", "happy"]); T(s, "savedc", at=0.05, dy=0.37, wf=0.62)
s = S("That is the", "HF", (3.5, 1.45, -2.6), 5.4, -6, pitch=14, pitchTo=4); ft(s, "abeH", ["happy", "smug"])
s = S("Wrestling Hall#2", "RG", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.05, "abeR", face="smug", pose=dict(armR=-150), shake=0.4); T(s, "hookc", at=0.05, dy=0.34, wf=0.62, hf=0.2)
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
ATM = dict(RG=dict(bokeh=BK(0.5)), HF=dict(dust=D_(24), rays=dict(angle=26, intensity=0.6)), PR=dict(dust=D_(26), rays=dict(angle=30, intensity=0.7)), CP=dict(dust=D_(24)), NS=dict(dust=D_(22), rays=dict(angle=24, intensity=0.6)),
           FT=dict(dust=D_(32)), FR=dict(bokeh=BK(0.55)), CT=dict(dust=D_(22), rays=dict(angle=20, intensity=0.6)), JL=dict(dust=D_(20), rays=dict(angle=28, intensity=0.6)), MN=dict(bokeh=BK(0.45)), AL=dict(bokeh=BK(0.5)))
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
MOOD = dict(RG="arena", HF="hall", PR="prairie", CP="camp", NS="salem", FT="duskring", FR="firefly", CT="court", JL="jail", MN="moon", AL="study")
light, cur = [{"t": 0, "mood": "arena"}], "arena"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"arena": {"sun": {"azimuth": 200, "elevation": 40, "color": "#fff0e0", "intensity": 2.6}, "sky": {"top": "#ff7846", "horizon": "#ff5a96"}, "fill": {"sky": "#fff4ec", "ground": "#6a3a5a", "intensity": 2.1}},
              "hall": {"sun": {"azimuth": 30, "elevation": 44, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#1e8c96", "horizon": "#78dcd2"}, "fill": {"sky": "#f0fffc", "ground": "#8a5a5a", "intensity": 1.6}},
              "prairie": {"sun": {"azimuth": 230, "elevation": 26, "color": "#fff0c8", "intensity": 2.5}, "sky": {"top": "#ffc86e", "horizon": "#fff0be"}, "fill": {"sky": "#fffaf0", "ground": "#8a7a40", "intensity": 1.5}},
              "camp": {"sun": {"azimuth": 220, "elevation": 22, "color": "#ffd8b8", "intensity": 2.5}, "sky": {"top": "#3c8ca0", "horizon": "#ffbe96"}, "fill": {"sky": "#fff4ec", "ground": "#6a5a50", "intensity": 1.9}},
              "salem": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#96dcc8", "horizon": "#f0fae6"}, "fill": {"sky": "#f4fff8", "ground": "#5a7a5a", "intensity": 1.5}},
              "duskring": {"sun": {"azimuth": 230, "elevation": 18, "color": "#ffd0a8", "intensity": 2.5}, "sky": {"top": "#ff6e5a", "horizon": "#ffc878"}, "fill": {"sky": "#fff0e8", "ground": "#7a5040", "intensity": 1.8}},
              "firefly": {"sun": {"azimuth": 220, "elevation": 20, "color": "#ffe0b0", "intensity": 2.5}, "sky": {"top": "#f09650", "horizon": "#ffdc8c"}, "fill": {"sky": "#fff4e0", "ground": "#6a5a30", "intensity": 1.8}},
              "court": {"sun": {"azimuth": 150, "elevation": 36, "color": "#fff0e0", "intensity": 2.6}, "sky": {"top": "#782832", "horizon": "#be5a50"}, "fill": {"sky": "#fff0e8", "ground": "#6a3a30", "intensity": 2.3}},
              "jail": {"sun": {"azimuth": 160, "elevation": 40, "color": "#f4f0ff", "intensity": 2.4}, "sky": {"top": "#8c82b4", "horizon": "#c8bee6"}, "fill": {"sky": "#f8f4ff", "ground": "#5a5070", "intensity": 1.9}},
              "moon": {"sun": {"azimuth": 20, "elevation": 40, "color": "#eef4ff", "intensity": 2.7}, "sky": {"top": "#284696", "horizon": "#6e96d2"}, "fill": {"sky": "#eef4ff", "ground": "#2a4a5a", "intensity": 2.4}},
              "study": {"sun": {"azimuth": 150, "elevation": 34, "color": "#fff0d8", "intensity": 2.5}, "sky": {"top": "#c87832", "horizon": "#ffc878"}, "fill": {"sky": "#fff4e8", "ground": "#6a4a30", "intensity": 2.0}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#22e0ff", "paper": ["#f0a050", "#dc8c3c"], "dofPx": 8, "particle": "#fff0d8", "bokehColor": "#ffd8a0", "ray": "#fff4dc", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(his="His most famous", yousee="You see that", witness="A witness swore", notg="Not guilty",
           fame="Fame", pro="pro", abraham="Abraham", beard="beard", six="was a", frontier="frontier", legend="Legend", k300="300", y1832="1832", thompson="Thompson",
           salem="New Salem", against="against", jack="Jack Armstrong", bet="bet", friend="friend", y1858="1858", duff="Duff", charged="charged", free="free",
           moonlight="moonlight", almanac="almanac", almost="almost", won="won a friend", saved="saved", man="That is the")
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
