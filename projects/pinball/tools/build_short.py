#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 24: pinball was illegal in New York for 34 years; Roger Sharpe ended the ban with one called shot.
usage: build_short.py <project folder>
Eleven steel-blue 1940s -> harvest-gold 1976 sets 70 units apart: HK electric pinball world (hook + loop), PF chrome macro studio (open loop: a "?"
silhouette + a "?" ball, resolved when the ball drops into the center lane), MY olive-cream 1942 radio stage, PR amber-teal bowling alley, SM flashbulb
night, RV teal harbor, SC school-bus yellow lunch room, DM sunset domino table, CB red-lamp back room, QS felt-vs-blueprint split stage, CC 1976 council.
Shots 0.7-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, PF=70, MY=140, PR=210, SM=280, RV=350, SC=420, DM=490, CB=560, QS=630, CC=700)
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


yard("HK", "playworld.png", "field.jpg"); box("HK", -2.8, 0.04, -1.6, [0.6, 0.5, 0.6], color="#ffd23c"); box("HK", 2.8, 0.04, -1.6, [0.6, 0.5, 0.6], color="#50e6ff")
yard("PF", "chrome.png", "steel2.jpg"); box("PF", 3.2, 0.04, -2.4, [1.0, 0.46, 0.8], color="#3a4a8a"); box("PF", 6.0, 0.04, -2.4, [1.2, 0.46, 0.6], color="#3a4a8a")
yard("MY", "radio.png", "wood.jpg")
yard("PR", "bowling.png", "lanes.jpg")
yard("SM", "flashnight.png", "cobble.jpg")
yard("RV", "harbor.png", "dock.jpg")
yard("SC", "school.png", "lino2.jpg"); table("SC", 0.2, -2.1, 1.6, 0.8, 0.74, "#c87840")
yard("DM", "dusktable.png", "tabletop.jpg")
yard("CB", "backroom.png", "brick2.jpg")
yard("QS", "splitstage.png", "felt.jpg")
yard("CC", "chamber.png", "shag.jpg"); box("CC", 0.0, 0.04, -2.45, [4.2, 0.82, 0.5], color="#8a5a30")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
put("machH", "pmach", pos("HK", 0.0, 0.04, -2.3), 1.7, face="tape")
put("qmanP", "qman", pos("PF", -3.2, 0.04, -2.4), 1.3); put("pfieldP", "pfield", pos("PF", 0.0, 0.04, -2.4), 1.9); put("ballP", "pball", pos("PF", 3.2, 0.5, -2.4), 0.9, face="q"); put("plungerP", "plunger", pos("PF", 6.0, 0.5, -2.4), 0.45)
human("mayorM", "fiorello", pos("MY", -0.6, 0.04, -1.8), face="shouting", h=1.6); put("podiumM", "podium", pos("MY", 0.6, 0.04, -2.0), 1.3)
human("copR", "cop40", pos("PR", -1.0, 0.04, -1.8), face="shouting"); put("pinsR", "pins", pos("PR", 1.0, 0.04, -2.4), 0.9); put("pileR", "pile", pos("PR", 4.4, 0.04, -2.6), 1.5)
human("mayorS", "fiorello", pos("SM", -1.4, 0.04, -1.8), face="shouting", h=1.6); put("smashS", "smash", pos("SM", 0.2, 0.04, -2.4), 1.9); put("camS", "newscam", pos("SM", 2.9, 0.04, -2.2), 1.2)
put("bargeV", "barge", pos("RV", 0.0, 0.04, -2.6), 1.4)
human("kidC", "lunchkid", pos("SC", -1.4, 0.04, -1.8), face="sad", h=1.35); put("coinsC", "coins", pos("SC", 0.2, 0.78, -2.1), 0.75)
put("domD", "domino", pos("DM", 0.0, 0.04, -2.4), 1.3)
put("machB", "pmach", pos("CB", 0.0, 0.04, -2.4), 1.7, face="cage")
put("scaleQ", "scale", pos("QS", 0.0, 0.04, -2.4), 1.9)
human("c1C", "cncl1", pos("CC", -1.5, 0.04, -2.95), face="confused"); human("c2C", "cncl2", pos("CC", 0.0, 0.04, -3.0), face="happy"); human("c3C", "cncl3", pos("CC", 1.5, 0.04, -2.95), face="smug")
put("gavelC", "gavel", pos("CC", 0.6, 0.86, -2.45), 0.32); human("sharpeC", "sharpe", pos("CC", 3.6, 0.04, -1.6), face="smug"); put("machC", "pmach", pos("CC", 4.8, 0.04, -1.9), 1.5, face="happy")
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


HOOK = dict(anchor=(0.0, 1.0, -2.3), dist=7.0, yaw=4, pitch=6)
# ---- Pinball was illegal in New York for 34 years, and one man ended the ban with a single ball.
s = S("0", "HK", zoom=14, **HOOK); act(s, 0.0, "machH", face="tape", shake=0.5); tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24); snap(s, rel(s, "York"), 10)
s = S("for 34 years", "HK", (0.0, 1.8, -2.3), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="ILLEGAL FOR", items=["34 YEARS"]))
s = S("and one man", "PF", (-3.2, 0.75, -2.4), 3.6, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="qmanP", blur=0.5)); act(s, 0.05, "qmanP", shake=0.4); T(s, "oneman", at=0.1)
s = S("with a single", "PF", (3.2, 0.95, -2.4), 2.8, 6, pitch=6, zoom=14, type="macro", dof=dict(focus="ballP", blur=0.5)); act(s, 0.05, "ballP", shake=0.5)
# ---- In 1942, Mayor Fiorello La Guardia declared pinball gambling. Police raided bars and bowling alleys and seized thousands of machines.
s = crane("In 1942", "MY", (0.0, 1.1, -1.9), 8.0, 22, 2, 36, 8); ft(s, "mayorM", ["shouting", "smug"]); T(s, "y1942", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("Mayor Fiorello La", "MY", (-0.6, 1.15, -1.8), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="mayorM", blur=0.4)); hide(s, 0.0, "podiumM"); ft(s, "mayorM", ["smug", "shouting"]); act(s, 0.05, "mayorM", pose=dict(armR=-150)); T(s, "mayorc"); snap(s, 0.3, 8)
s = S("declared pinball gambling", "HK", (0.0, 1.0, -2.3), 5.0, -14, pitch=5, yawTo=4); act(s, 0.05, "machH", face="shocked", shake=0.4); T(s, "gamb", at=rel(s, "gambling"))
s = S("Police raided bars", "PR", (-0.1, 1.0, -2.0), 6.4, -6, pitch=5, zoom=4, pan=(8, 0)); go(s, 0.0, "copR", pos("PR", -0.6, 0.04, -1.8), 0.8); ft(s, "copR", ["shouting", "shocked"]); T(s, "raid")
s = S("bowling alleys and", "PR", (1.0, 0.5, -2.4), 2.8, 4, pitch=6, zoom=14, type="macro", dof=dict(focus="pinsR", blur=0.5)); act(s, 0.05, "pinsR", shake=0.7)
s = crane("seized thousands of", "PR", (4.4, 0.85, -2.6), 6.4, -22, -2, 36, 8); act(s, 0.1, "pileR", shake=0.5); T(s, "thous", at=rel(s, "thousands"))
# ---- La Guardia smashed them with a sledgehammer for the cameras, and the pieces were dumped into the city's waters.
s = S("La Guardia smashed", "SM", (-0.4, 1.05, -2.1), 7.4, 8, pitch=5, zoom=-10); act(s, 0.05, "mayorS", pose=dict(armR=-150), shake=0.3); ft(s, "mayorS", ["shouting", "smug"]); act(s, 0.1, "smashS", shake=0.7); snap(s, rel(s, "smashed"), 10); cfx(s, rel(s, "smashed"), "bang", "mayorS", 0.5)
s = S("sledgehammer for the", "SM", (2.9, 0.7, -2.2), 3.0, -16, pitch=6, yawTo=4, type="macro", dof=dict(focus="camS", blur=0.5)); act(s, 0.05, "camS", shake=0.4); act(s, rel(s, "cameras"), "camS", shake=0.6); T(s, "cams", at=rel(s, "cameras"))
s = crane("pieces were dumped", "RV", (0.0, 0.8, -2.6), 7.0, 22, 2, 38, 8); act(s, 0.1, "bargeV", shake=0.4); act(s, rel(s, "dumped"), "bargeV", shake=0.7)
# ---- His reason? He said pinball stole children's nickels and dimes. Their lunch money.
s = S("His reason He", "MY", (0.0, 1.05, -1.9), 6.6, -4, pitch=14, pitchTo=3); show(s, 0.05, "podiumM", pos("MY", 0.6, 0.04, -2.0)); ft(s, "mayorM", ["shouting", "confused"]); act(s, 0.1, "mayorM", pose=dict(armR=-150)); T(s, "reason"); cfx(s, 0.3, "question", "mayorM", 0.7)
s = S("stole children's nickels", "SC", (0.2, 1.1, -2.1), 2.8, 6, pitch=8, zoom=14, type="macro", dof=dict(focus="coinsC", blur=0.5)); act(s, 0.05, "coinsC", shake=0.5)
s = S("Their lunch money", "SC", (-0.5, 0.95, -1.95), 5.6, 12, pitch=5, zoom=-12); act(s, 0.0, "coinsC", face="empty", shake=0.5); ft(s, "kidC", ["sad", "shocked"]); T(s, "lunch", at=0.05); snap(s, rel(s, "lunch"), 8)
# ---- Chicago and other cities banned it too. For three decades, a pinball machine in New York was contraband.
s = S("Chicago and other", "DM", (0.0, 0.8, -2.4), 5.8, 18, pitch=8, yawTo=-2); act(s, 0.35, "domD", face="f1", shake=0.3); act(s, 0.95, "domD", face="f2", shake=0.5)
s = S("For three decades", "CB", (0.0, 1.0, -2.4), 7.2, -6, pitch=5, zoom=12); T(s, "decades")
s = S("a pinball machine", "CB", (0.0, 1.0, -2.4), 5.4, 14, pitch=16, pitchTo=4); act(s, 0.05, "machB", shake=0.3)
s = S("was contraband", "CB", (0.0, 1.0, -2.4), 4.2, -4, pitch=5, zoom=14); act(s, 0.05, "machB", shake=0.6); T(s, "contra", at=rel(s, "contraband")); snap(s, rel(s, "contraband"), 8)
# ---- You see, the whole fight came down to one question. Is pinball luck, or skill? Luck meant gambling. Skill meant a game.
s = crane("You see the", "QS", (0.0, 1.0, -2.4), 8.0, -22, -2, 36, 8); act(s, 0.1, "scaleQ", shake=0.3); T(s, "question", at=rel(s, "question"))
s = S("Is pinball luck", "QS", (0.0, 1.0, -2.4), 6.6, 16, pitch=5, yawTo=-4); act(s, rel(s, "luck"), "scaleQ", face="luck", shake=0.3); act(s, rel(s, "skill"), "scaleQ", face="skill", shake=0.3)
s = S("Luck meant gambling", "QS", (0.0, 1.0, -2.4), 6.6, 0, pitch=5, zoom=12); act(s, 0.0, "scaleQ", face="luck", shake=0.6); T(s, "gamb", at=rel(s, "gambling"))
s = S("Skill meant a", "QS", (0.0, 1.0, -2.4), 6.8, -10, pitch=5, zoom=-10); act(s, 0.0, "scaleQ", face="skill", shake=0.6); T(s, "game", at=rel(s, "game"))
# ---- So in 1976, the industry hired a pinball expert named Roger Sharpe to prove it in front of the City Council. A suspicious councilman made him switch to a backup machine.
s = crane("So in 1976", "CC", (0.0, 1.2, -2.6), 10.0, 22, 2, 36, 8); hide(s, 0.0, "machC"); ft(s, "c2C", ["happy", "smug"]); T(s, "y1976", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("the industry hired", "CC", (3.6, 1.2, -1.6), 5.0, 8, pitch=5, zoom=12, dof=dict(focus="sharpeC", blur=0.4)); ft(s, "sharpeC", ["smug", "happy"]); T(s, "expert", at=rel(s, "expert")); snap(s, rel(s, "expert"), 8)
s = S("named Roger Sharpe", "CC", (3.6, 1.25, -1.6), 4.4, -14, pitch=5, yawTo=4, dof=dict(focus="sharpeC", blur=0.4)); ft(s, "sharpeC", ["happy", "smug"]); act(s, 0.1, "sharpeC", pose=dict(armR=-150)); T(s, "sharpec")
s = S("in front of", "CC", (0.0, 1.2, -2.6), 9.8, 6, pitch=6, zoom=-10); ft(s, "c1C", ["confused", "smug"]); ft(s, "c3C", ["smug", "happy"]); T(s, "councilc")
s = S("A suspicious councilman", "CC", (-1.5, 1.35, -2.95), 4.0, -10, pitch=5, yawTo=6, dof=dict(focus="c1C", blur=0.4)); ft(s, "c1C", ["confused", "smug"]); cfx(s, 0.3, "question", "c1C", 0.6)
s = S("made him switch", "CC", (4.2, 1.1, -1.75), 6.0, 4, pitch=5, zoom=4, pan=(-8, 0)); show(s, rel(s, "switch"), "machC", pos("CC", 4.8, 0.04, -1.9)); ft(s, "sharpeC", ["shocked", "smug"]); T(s, "backup", at=rel(s, "backup"))
s = S("Sharpe pointed at", "CC", (4.2, 1.1, -1.75), 4.8, -12, pitch=5, zoom=12, dof=dict(focus="sharpeC", blur=0.3)); act(s, 0.05, "sharpeC", pose=dict(armR=-150), shake=0.3); ft(s, "sharpeC", ["smug", "happy"]); snap(s, rel(s, "pointed"), 8)
# ---- Sharpe pointed at the center lane and said the ball would go right there. He pulled the plunger. It went exactly there. The council voted unanimously to lift the ban.
s = crane("and said the", "PF", (0.0, 0.95, -2.4), 5.4, 18, 2, 40, 10); act(s, 0.05, "pfieldP", face="call", shake=0.3)
s = S("He pulled the", "PF", (6.0, 0.72, -2.4), 2.4, -4, pitch=6, zoom=14, type="macro", dof=dict(focus="plungerP", blur=0.5)); act(s, rel(s, "pulled"), "plungerP", face="pulled", shake=0.4)
s = S("It went exactly", "PF", (0.0, 0.95, -2.4), 5.0, -14, pitch=6, yawTo=4); act(s, 0.0, "pfieldP", face="hit", shake=0.6); T(s, "exactly", at=rel(s, "exactly")); snap(s, rel(s, "went"), 10)
s = S("The council voted", "CC", (0.0, 1.2, -2.6), 9.6, 4, pitch=6, zoom=-10); hide(s, 0.0, "sharpeC"); hide(s, 0.0, "machC")
for k, w_ in enumerate(("c1C", "c2C", "c3C")): act(s, 0.15 + 0.18 * k, w_, pose=dict(armR=-150), face="happy", shake=0.3)
T(s, "unan", at=rel(s, "unanimously"))
s = S("lift the ban", "HK", (0.0, 1.0, -2.3), 5.2, -6, pitch=5, zoom=14); act(s, 0.0, "machH", face="happy", shake=0.6); T(s, "lifted", at=0.05)
# ---- Which means a city that banned gambling let one man bet pinball's entire future on a single ball.
s = S("Which means a", "RV", (0.0, 0.9, -2.6), 7.4, -16, pitch=6, yawTo=4); act(s, 0.1, "bargeV", shake=0.3)
s = S("let one man", "CC", (3.6, 1.25, -1.6), 4.4, 10, pitch=12, pitchTo=3, dof=dict(focus="sharpeC", blur=0.4)); show(s, 0.0, "sharpeC", pos("CC", 3.6, 0.04, -1.6), hop=0); ft(s, "sharpeC", ["smug", "happy"])
s = S("pinball's entire future", "PF", (3.2, 0.95, -2.4), 3.0, -10, pitch=6, yawTo=6, type="macro", dof=dict(focus="ballP", blur=0.5)); act(s, 0.0, "ballP", face="default", shake=0.4); T(s, "future")
s = S("on a single", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.0, "machH", face="happy", shake=0.3); T(s, "single", at=0.1)
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
ATM = dict(HK=dict(bokeh=BK(0.5)), PF=dict(bokeh=BK(0.45)), MY=dict(dust=D_(24), rays=dict(angle=26, intensity=0.5)), PR=dict(dust=D_(22)), SM=dict(bokeh=BK(0.45)),
           RV=dict(bokeh=BK(0.4)), SC=dict(dust=D_(24), rays=dict(angle=32, intensity=0.5)), DM=dict(dust=D_(22), rays=dict(angle=20, intensity=0.6)), CB=dict(bokeh=BK(0.4)),
           QS=dict(dust=D_(18)), CC=dict(dust=D_(26), rays=dict(angle=28, intensity=0.5)))
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
MOOD = dict(HK="pinworld", PF="chrome", MY="radio42", PR="bowl", SM="flash", RV="harbor", SC="schoolbus", DM="dominodusk", CB="redlamp", QS="split", CC="council76")
light, cur = [{"t": 0, "mood": "pinworld"}], "pinworld"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"pinworld": {"sun": {"azimuth": 20, "elevation": 40, "color": "#f0e8ff", "intensity": 2.6}, "sky": {"top": "#28145a", "horizon": "#6e3cbe"}, "fill": {"sky": "#f0e8ff", "ground": "#4a3a70", "intensity": 2.1}},
              "chrome": {"sun": {"azimuth": -30, "elevation": 40, "color": "#f0f6ff", "intensity": 2.6}, "sky": {"top": "#1e2846", "horizon": "#788cb4"}, "fill": {"sky": "#eef4ff", "ground": "#40485a", "intensity": 2.0}},
              "radio42": {"sun": {"azimuth": 30, "elevation": 40, "color": "#fff4e0", "intensity": 2.4}, "sky": {"top": "#78783c", "horizon": "#e6dcaa"}, "fill": {"sky": "#fffbf0", "ground": "#6a5a40", "intensity": 1.6}},
              "bowl": {"sun": {"azimuth": 200, "elevation": 30, "color": "#ffe0b0", "intensity": 2.5}, "sky": {"top": "#1e6e78", "horizon": "#50aaaa"}, "fill": {"sky": "#f0fff8", "ground": "#6a5040", "intensity": 1.8}},
              "flash": {"sun": {"azimuth": 10, "elevation": 42, "color": "#f8f8ff", "intensity": 2.7}, "sky": {"top": "#28325a", "horizon": "#5a6496"}, "fill": {"sky": "#eef0ff", "ground": "#3a3e5a", "intensity": 2.1}},
              "harbor": {"sun": {"azimuth": 210, "elevation": 30, "color": "#fff0d0", "intensity": 2.5}, "sky": {"top": "#142846", "horizon": "#286478"}, "fill": {"sky": "#e0f4ff", "ground": "#2a4a5a", "intensity": 2.1}},
              "schoolbus": {"sun": {"azimuth": 40, "elevation": 46, "color": "#fffbe8", "intensity": 2.3}, "sky": {"top": "#ffd23c", "horizon": "#ffec96"}, "fill": {"sky": "#fffcf0", "ground": "#8a6a40", "intensity": 1.3}},
              "dominodusk": {"sun": {"azimuth": 230, "elevation": 16, "color": "#ffc896", "intensity": 2.5}, "sky": {"top": "#6e3c96", "horizon": "#ff965a"}, "fill": {"sky": "#ffe8e0", "ground": "#5a3a40", "intensity": 1.9}},
              "redlamp": {"sun": {"azimuth": 160, "elevation": 36, "color": "#ffd0c0", "intensity": 2.7}, "sky": {"top": "#32141e", "horizon": "#6e2832"}, "fill": {"sky": "#ffe8e8", "ground": "#4a2a2a", "intensity": 2.2}},
              "split": {"sun": {"azimuth": 20, "elevation": 44, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#1e8250", "horizon": "#285ac8"}, "fill": {"sky": "#f4fff8", "ground": "#40404a", "intensity": 1.7}},
              "council76": {"sun": {"azimuth": 210, "elevation": 26, "color": "#ffe0a8", "intensity": 2.5}, "sky": {"top": "#966438", "horizon": "#c88c50"}, "fill": {"sky": "#fff4e0", "ground": "#6a4a30", "intensity": 1.7}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#2f7bff", "paper": ["#8aa8e8", "#6a88cc"], "dofPx": 8, "particle": "#fff4d8", "bokehColor": "#a8c8ff", "ray": "#fff1c8", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(y1942="In 1942", yousee="You see the", y1976="So in 1976", went="It went exactly",
           n34="34", ball1="single ball", gambling="declared pinball gambling", raid="Police raided", bowling="bowling alleys", seized="seized thousands", smashed="smashed",
           cams="cameras", dumped="dumped", reason="His reason", nickels="nickels", lunch="lunch money", chicago="Chicago", contra="contraband", question="one question",
           luck="Luck meant", skill="Skill meant", sharpe="Roger Sharpe", susp="suspicious", switch="switch", pointed="pointed", pulled="pulled", exactly="exactly",
           unan="unanimously", lift="lift the ban", future="entire future")
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
