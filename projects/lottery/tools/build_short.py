#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 27: 110 people won the lottery with the same numbers - all from one fortune cookie.
usage: build_short.py <project folder>
Eleven lucky neon red-jade sets 70 units apart: HK purple neon draw studio (hook + loop; a spot-lit "?" 6th ball = open loop, resolved as the one
wrong number 40), CB mustard classroom chalkboard, RF sunny confetti rooftop, OF olive night office, IV teal investigation room, MP navy map room,
BK golden bakery macro table, FC golden-hour Queens factory, LN red-steel cookie line, LS navy lantern street, JP crimson-gold jackpot plaza.
Shots 0.7-2 s, every neighbour a different move; props and the cookie are the stars, people are small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, CB=70, RF=140, OF=210, IV=280, MP=350, BK=420, FC=490, LN=560, LS=630, JP=700)
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


def table(loc, x, z, w=1.4, d=0.8, h=0.74, col="#8a5a3a"): box(loc, x, 0.04, z, [w, h, d], color=col)


yard("HK", "studio.png", "ledfloor.jpg"); box("HK", -3.4, 0.04, -2.6, [1.0, 0.95, 0.6], color="#7840c8"); box("HK", 1.9, 0.04, -1.0, [0.5, 0.3, 0.5], color="#1ee6a0")
yard("CB", "classroom.png", "wood.jpg"); box("CB", 1.0, 0.04, -1.4, [0.9, 0.5, 0.6], color="#c88a50")
yard("RF", "rooftop.png", "roof.jpg"); box("RF", 1.7, 0.04, -3.2, [0.8, 0.8, 0.8], color="#e83c50")
yard("OF", "office.png", "carpet.jpg"); table("OF", 0.6, -2.2, 1.4, 0.8, 0.76, "#6a5a40")
yard("IV", "invest.png", "lino.jpg"); table("IV", 2.0, -2.4, 1.4, 0.8, 0.76, "#4a6a6a")
yard("MP", "maproom.png", "navy.jpg"); box("MP", 0, 0.04, -2.5, [2.6, 0.18, 0.5], color="#1ee6a0")
yard("BK", "bakery.png", "table.jpg"); table("BK", 0, -2.2, 2.4, 1.0, 0.74, "#a8643a")
yard("FC", "queens.png", "pave.jpg")
yard("LN", "line.png", "steel.jpg"); table("LN", -3.6, -2.2, 1.2, 0.8, 0.6, "#b4b4c8")
yard("LS", "lanterns.png", "cobble.jpg")
yard("JP", "plaza.png", "plaza.jpg")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
human("w1H", "w1", pos("HK", -0.7, 0.04, -2.0), face="shocked", h=1.5); human("w2H", "w2", pos("HK", 0.05, 0.04, -2.1), face="shocked", h=1.5); human("w3H", "w3", pos("HK", 0.8, 0.04, -2.0), face="shocked", h=1.5)
put("qball_H", "qball", pos("HK", 0.45, 1.45, -3.8), 0.7); put("bmachH", "bmach", pos("HK", 3.1, 0.04, -3.4), 2.0); put("balls6H", "balls6", pos("HK", -3.4, 0.99, -2.6), 0.7)
put("boardC", "board", pos("CB", 0.0, 0.5, -3.0), 1.6); human("offlC", "offl", pos("CB", 2.4, 0.04, -2.4), face="happy")
put("checkR", "check", pos("RF", 0.0, 0.04, -2.4), 0.9); put("tixR", "tix", pos("RF", -4.0, 0.3, -3.0), 1.2)
human("w1R", "w1", pos("RF", 3.3, 0.04, -2.0), face="happy", h=1.5); human("w2R", "w2", pos("RF", 4.1, 0.04, -2.1), face="happy", h=1.5); human("w3R", "w3", pos("RF", 4.9, 0.04, -2.0), face="happy", h=1.5)
human("offlO", "offl", pos("OF", -0.8, 0.04, -2.0), face="shocked"); put("calcO", "calc", pos("OF", 0.6, 0.8, -2.2), 0.9)
put("corkI", "cork", pos("IV", -1.6, 0.5, -3.0), 1.4); put("pcI", "pc", pos("IV", 2.0, 0.8, -2.4), 0.9)
put("usmapM", "usmap", pos("MP", 0.0, 0.22, -2.6), 1.4)
put("cookieB", "cookie", pos("BK", 0.0, 0.78, -2.2), 0.8)
put("factoryF", "factory", pos("FC", 0.0, 0.04, -3.0), 2.2)
put("beltL", "belt", pos("LN", 0.0, 0.04, -2.6), 0.8); human("bakerL", "baker", pos("LN", -1.3, 0.04, -1.9), face="happy", h=1.7); put("sprintL", "sprint", pos("LN", 3.4, 0.04, -2.4), 1.3)
put("bowlL", "bowl", pos("LN", -3.6, 0.64, -2.2), 0.8)
put("slipS", "slip", PARK, 0.7); put("hqS", "hq", pos("LS", -4.0, 0.04, -3.2), 2.6)
put("pieJ", "pie", pos("JP", 0.0, 0.04, -2.4), 1.0); put("crowdJ", "crowdt", pos("JP", -4.0, 0.04, -2.4), 0.9); put("bagsJ", "bags", pos("JP", 4.0, 0.04, -2.4), 0.9)
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


HOOK = dict(anchor=(0.05, 1.2, -2.2), dist=6.6, yaw=4, pitch=6)
# ---- 110 people won the lottery with the exact same numbers. On the same night.
s = S("0", "HK", zoom=7, **HOOK)
for k, w_ in enumerate(("w1H", "w2H", "w3H")): act(s, 0.0, w_, face="shocked", pose=dict(armR=-150), shake=0.3); ft(s, w_, ["shocked", "happy"])
tag(s, 0.0, "hookc", 0.33, 0.0, wf=0.6, hf=0.2); act(s, 0.2, "qball_H", shake=0.3); snap(s, rel(s, "same"), 10)
s = S("won the lottery", "HK", (3.1, 1.0, -3.4), 5.0, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="bmachH", blur=0.5)); act(s, 0.05, "bmachH", face="spin", shake=0.5)
s = S("with the exact", "RF", (-4.0, 0.9, -3.0), 5.6, 14, pitch=16, pitchTo=4, dof=dict(focus="tixR", blur=0.4)); act(s, 0.1, "tixR", shake=0.3)
s = S("On the same", "LS", (0.0, 1.3, -2.6), 6.4, -6, pitch=5, zoom=10); hide(s, 0.0, "hqS"); T(s, "night", at=rel(s, "night"), dy=0.3, wf=0.5)
# ---- Powerball expected four or five second-prize winners. That's just math. Instead, 110 tickets matched the first five numbers.
s = crane("Powerball expected", "CB", (0.0, 1.3, -2.9), 7.6, 22, 2, 36, 8); hide(s, 0.0, "offlC"); act(s, rel(s, "four"), "boardC", shake=0.4)
s = S("That's just math", "CB", (2.4, 1.0, -2.4), 4.8, -10, pitch=5, zoom=12, dof=dict(focus="offlC", blur=0.4)); ft(s, "offlC", ["happy", "smug"]); act(s, 0.1, "offlC", pose=dict(armR=-150)); T(s, "math", dy=0.38, wf=0.6)
s = S("Instead 110 tickets", "CB", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="INSTEAD", items=["110 TICKETS"]))
s = S("matched the first", "HK", (-3.4, 1.35, -2.6), 5.4, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="balls6H", blur=0.5)); act(s, 0.1, "balls6H", shake=0.4)
# ---- Each one won between 100,000 and 500,000 dollars. Almost 19 million dollars nobody had budgeted for.
s = S("Each one won", "RF", (0.0, 0.75, -2.4), 5.4, 6, pitch=5, zoom=12, dof=dict(focus="checkR", blur=0.4)); act(s, rel(s, "100000"), "checkR", shake=0.5)
s = S("and 500000", "RF", (0.0, 0.75, -2.4), 5.0, -12, pitch=6, yawTo=4); act(s, 0.05, "checkR", face="k500", shake=0.6); snap(s, rel(s, "500000"), 8)
s = S("Almost 19 million", "CB", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="ALMOST", items=["$19 MILLION"]))
s = S("nobody had budgeted", "OF", (-0.1, 1.0, -2.1), 5.6, 10, pitch=5, zoom=-10); ft(s, "offlO", ["shocked", "nervous"]); act(s, 0.1, "calcO", face="boom", shake=0.6); T(s, "nobody", dy=0.38, wf=0.6); cfx(s, 0.3, "sweat", "offlO", 0.7)
# ---- So officials did what any lottery would do. They suspected a scam. Or a computer glitch.
s = crane("So officials did", "LS", (-4.0, 1.4, -3.2), 8.6, -22, -2, 36, 8)
s = S("They suspected a", "IV", (-1.6, 1.2, -3.0), 5.4, 8, pitch=5, zoom=14, dof=dict(focus="corkI", blur=0.4)); act(s, rel(s, "scam"), "corkI", shake=0.5); T(s, "scam", at=rel(s, "scam"), dy=0.37, wf=0.4); snap(s, rel(s, "scam"), 8)
s = S("Or a computer", "IV", (2.0, 1.25, -2.4), 3.8, -14, pitch=6, yawTo=6, type="macro", dof=dict(focus="pcI", blur=0.5)); act(s, 0.05, "pcI", shake=0.6); T(s, "glitch", at=rel(s, "glitch"), dy=0.38, wf=0.44)
# ---- Then lottery officials in Tennessee and Idaho traced the tickets back to one place.
s = crane("Then lottery officials", "MP", (0.0, 0.9, -2.6), 7.0, 22, 2, 40, 8); act(s, rel(s, "Tennessee"), "usmapM", shake=0.4)
s = S("and Idaho traced", "MP", (-0.4, 0.9, -2.6), 6.4, -6, pitch=10, zoom=6, pan=(-8, 0)); act(s, rel(s, "Idaho"), "usmapM", shake=0.3)
s = S("back to one", "MP", (0.0, 0.95, -2.6), 6.8, 12, pitch=5, yawTo=-2); act(s, 0.05, "usmapM", face="route", shake=0.5); T(s, "oneplace", at=rel(s, "place") - 0.2, dy=0.37, wf=0.5)
# ---- You see, every one of those winners had cracked open a fortune cookie.
s = S("You see every", "JP", (-4.0, 0.7, -2.4), 5.6, -8, pitch=5, zoom=10); act(s, 0.1, "crowdJ", shake=0.4); act(s, 0.6, "crowdJ", shake=0.4)
s = S("cracked open a", "BK", (0.0, 1.2, -2.2), 3.6, 12, pitch=6, yawTo=-6, type="macro", dof=dict(focus="cookieB", blur=0.5)); act(s, rel(s, "open"), "cookieB", face="crack", shake=0.7); T(s, "fortune", at=rel(s, "fortune"), dy=0.38, wf=0.5); snap(s, rel(s, "open"), 10)
# ---- The cookies came from Wonton Food, a factory in Queens, New York, that bakes 4 million a day.
s = crane("The cookies came", "FC", (0.0, 1.3, -3.0), 8.8, -22, -2, 36, 8)
s = S("a factory in", "FC", (0.0, 1.5, -3.0), 7.4, 4, pitch=5, zoom=12, dof=dict(focus="factoryF", blur=0.4)); act(s, 0.1, "factoryF", shake=0.3)
s = S("that bakes 4", "LN", (-0.5, 0.9, -2.3), 6.0, -10, pitch=5, yawTo=6); ft(s, "bakerL", ["happy", "smug"]); act(s, 0.1, "beltL", shake=0.3); T(s, "m4", at=rel(s, "4"), dy=0.37, wf=0.56); snap(s, rel(s, "4"), 8)
# ---- Years earlier, it started printing lottery numbers on the back, just to stand out. The numbers? Drawn at random from a bowl.
s = S("Years earlier it", "LN", (-0.5, 0.9, -2.3), 6.2, 8, pitch=5, zoom=-10); ft(s, "bakerL", ["smug", "happy"]); T(s, "years", at=0.05, dy=0.37, wf=0.6)
s = S("started printing lottery", "LN", (3.4, 1.1, -2.4), 4.6, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="sprintL", blur=0.5)); act(s, 0.05, "sprintL", shake=0.5)
s = S("just to stand", "BK", (0.0, 1.2, -2.2), 4.4, -8, pitch=14, pitchTo=3); act(s, 0.05, "cookieB", face="default", shake=0.4); T(s, "standout", at=0.05, dy=0.37, wf=0.62)
s = S("The numbers Drawn", "LN", (-3.6, 1.1, -2.2), 4.4, 12, pitch=5, zoom=12, dof=dict(focus="bowlL", blur=0.4)); act(s, 0.05, "bowlL", shake=0.5)
s = S("at random from", "LN", (-3.6, 1.1, -2.2), 3.8, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="bowlL", blur=0.5)); T(s, "random", at=0.05, dy=0.38, wf=0.5)
# ---- That night, the cookie said 22, 28, 32, 33, 39 and 40. The jackpot needed 42.
s = crane("That night the", "LS", (0.0, 1.3, -2.4), 6.8, 22, 2, 36, 8); hide(s, 0.0, "hqS"); show(s, 0.1, "slipS", pos("LS", 0.0, 0.9, -2.4)); act(s, 0.2, "slipS", face="default")
s = S("22", "LS", (0.0, 1.25, -2.4), 5.2, 6, pitch=5, zoom=10, dof=dict(focus="slipS", blur=0.4))
for k, n_ in enumerate(("22", "28", "32")): act(s, rel(s, n_), "slipS", face="n%d" % (k + 1), shake=0.3)
s = S("33", "LS", (0.0, 1.25, -2.4), 5.0, -14, pitch=6, yawTo=4, dof=dict(focus="slipS", blur=0.4)); act(s, 0.0, "slipS", face="n3")
for k, n_ in enumerate(("33", "39", "40")): act(s, rel(s, n_), "slipS", face="n%d" % (k + 4), shake=0.3)
s = S("The jackpot needed", "HK", (3.1, 1.2, -3.4), 5.6, -6, pitch=5, zoom=14, dof=dict(focus="bmachH", blur=0.4)); act(s, rel(s, "42"), "bmachH", face="pop42", shake=0.6); T(s, "need42", at=rel(s, "42"), dx=-0.2, dy=0.1, wf=0.34, hf=0.24); snap(s, rel(s, "42"), 10)
# ---- And here's the twist. A perfect cookie would have meant 110 people splitting one jackpot.
s = crane("And here's the", "JP", (0.0, 1.0, -2.4), 7.0, -22, -2, 36, 8); T(s, "twist", at=rel(s, "twist"), dy=0.36, wf=0.6)
s = S("A perfect cookie", "BK", (0.0, 1.25, -2.2), 4.0, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="cookieB", blur=0.5)); act(s, 0.05, "cookieB", face="gold", shake=0.5)
s = S("would have meant", "JP", (-4.0, 0.7, -2.4), 5.2, 8, pitch=5, zoom=-10); act(s, 0.1, "crowdJ", shake=0.5); T(s, "split", at=rel(s, "110"), dy=0.36, wf=0.6)
s = S("splitting one jackpot", "JP", (0.0, 0.8, -2.4), 4.8, -10, pitch=16, pitchTo=4, dof=dict(focus="pieJ", blur=0.4)); act(s, rel(s, "splitting"), "pieJ", face="sliced", shake=0.5)
# ---- The cookie's one wrong number made the lottery pay every single one of them in full.
s = S("The cookie's one", "HK", (-3.4, 1.35, -2.6), 5.4, -12, pitch=6, yawTo=6, dof=dict(focus="balls6H", blur=0.4)); act(s, rel(s, "wrong"), "balls6H", face="wrong", shake=0.6); T(s, "wrongn", at=rel(s, "wrong"), dy=0.36, wf=0.62); snap(s, rel(s, "wrong"), 10)
s = S("made the lottery", "JP", (4.0, 0.75, -2.4), 5.0, 10, pitch=5, zoom=12, dof=dict(focus="bagsJ", blur=0.4)); act(s, 0.1, "bagsJ", shake=0.5)
s = S("every single one", "RF", (4.1, 1.05, -2.0), 6.2, -8, pitch=5, zoom=8)
for k, w_ in enumerate(("w1R", "w2R", "w3R")): act(s, 0.1 + 0.1 * k, w_, pose=dict(armR=-150), shake=0.3); ft(s, w_, ["happy", "smug"])
T(s, "paid", at=rel(s, "full") - 0.3, dy=0.36, wf=0.5)
# ---- Because 110 people won the lottery with the exact same numbers.
s = crane("Because 110", "HK", (0.05, 1.2, -2.2), 7.8, 22, 2, 36, 8)
for w_ in ("w1H", "w2H", "w3H"): act(s, 0.0, w_, face="happy", pose=dict(armR=0))
s = S("won the lottery#2", "HK", zoom=-2, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); T(s, "hookc", at=0.05, dy=0.33, wf=0.6, hf=0.2)
for k, w_ in enumerate(("w1H", "w2H", "w3H")): act(s, 0.1 + 0.1 * k, w_, face="shocked", pose=dict(armR=-150), shake=0.3)
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
ATM = dict(HK=dict(bokeh=BK(0.5)), CB=dict(dust=D_(24), rays=dict(angle=24, intensity=0.6)), RF=dict(dust=D_(22), rays=dict(angle=30, intensity=0.5)), OF=dict(bokeh=BK(0.4)),
           IV=dict(dust=D_(26), rays=dict(angle=16, intensity=0.6)), MP=dict(bokeh=BK(0.5)), BK=dict(bokeh=BK(0.55)), FC=dict(dust=D_(22), rays=dict(angle=22, intensity=0.6)),
           LN=dict(dust=D_(28)), LS=dict(bokeh=BK(0.5)), JP=dict(bokeh=BK(0.45)))
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
MOOD = dict(HK="neonstudio", CB="mustard", RF="rooftop", OF="olive", IV="tealinv", MP="mapnavy", BK="bakegold", FC="queensgold", LN="redline", LS="lantern", JP="jackpot")
light, cur = [{"t": 0, "mood": "neonstudio"}], "neonstudio"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"neonstudio": {"sun": {"azimuth": 20, "elevation": 42, "color": "#fff0ff", "intensity": 2.8}, "sky": {"top": "#280a46", "horizon": "#9628a0"}, "fill": {"sky": "#fff0ff", "ground": "#4a2a6a", "intensity": 2.3}},
              "mustard": {"sun": {"azimuth": 150, "elevation": 38, "color": "#fff4d8", "intensity": 2.4}, "sky": {"top": "#e6aa3c", "horizon": "#fad278"}, "fill": {"sky": "#fffbe8", "ground": "#8a6a4a", "intensity": 1.5}},
              "rooftop": {"sun": {"azimuth": 40, "elevation": 46, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#3cbedc", "horizon": "#c8f0fa"}, "fill": {"sky": "#f4ffff", "ground": "#8a7a70", "intensity": 1.4}},
              "olive": {"sun": {"azimuth": 200, "elevation": 34, "color": "#fff0c8", "intensity": 2.6}, "sky": {"top": "#5a6432", "horizon": "#969650"}, "fill": {"sky": "#fffbe8", "ground": "#5a5030", "intensity": 2.0}},
              "tealinv": {"sun": {"azimuth": 230, "elevation": 30, "color": "#f0fff8", "intensity": 2.6}, "sky": {"top": "#14505a", "horizon": "#288c8c"}, "fill": {"sky": "#f0fffc", "ground": "#2a4a50", "intensity": 2.1}},
              "mapnavy": {"sun": {"azimuth": 10, "elevation": 44, "color": "#f0f8ff", "intensity": 2.7}, "sky": {"top": "#0e143c", "horizon": "#1e3c78"}, "fill": {"sky": "#e8f0ff", "ground": "#1e2a5a", "intensity": 2.3}},
              "bakegold": {"sun": {"azimuth": 150, "elevation": 32, "color": "#ffe8c0", "intensity": 2.5}, "sky": {"top": "#964614", "horizon": "#ffb450"}, "fill": {"sky": "#fff0e0", "ground": "#7a4a2a", "intensity": 1.9}},
              "queensgold": {"sun": {"azimuth": 230, "elevation": 18, "color": "#ffd0a0", "intensity": 2.5}, "sky": {"top": "#ff8c46", "horizon": "#ffdc96"}, "fill": {"sky": "#fff0e0", "ground": "#6a4a40", "intensity": 1.7}},
              "redline": {"sun": {"azimuth": 20, "elevation": 40, "color": "#fff0e8", "intensity": 2.6}, "sky": {"top": "#961e28", "horizon": "#dc5046"}, "fill": {"sky": "#fff0f0", "ground": "#6a2a2a", "intensity": 2.1}},
              "lantern": {"sun": {"azimuth": 220, "elevation": 30, "color": "#ffe0d0", "intensity": 2.7}, "sky": {"top": "#141846", "horizon": "#3c3278"}, "fill": {"sky": "#fff0f0", "ground": "#3a2a4a", "intensity": 2.3}},
              "jackpot": {"sun": {"azimuth": 230, "elevation": 20, "color": "#ffd8b0", "intensity": 2.6}, "sky": {"top": "#b41e46", "horizon": "#ffbe50"}, "fill": {"sky": "#fff0e8", "ground": "#6a3a3a", "intensity": 2.0}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#1ee6a0", "paper": ["#e87878", "#cc5a5a"], "dofPx": 8, "particle": "#fff0d0", "bokehColor": "#ffb0e0", "ray": "#fff6dc", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(officials="So officials did", yousee="You see every", night="That night the", twist="And here's the",
           same="same numbers", won="won the lottery", exact="with the exact", samen="same night", four="four or five", math="That's just math", instead="Instead",
           k100="100000", k500="500000", m19="19", nobody="nobody had", scam="scam", glitch="glitch", tenn="Tennessee", idaho="Idaho", place="one place", cracked="cracked open",
           wonton="Wonton", queens="Queens", m4="4 million", years="Years earlier", printing="printing", stand="stand out", random="random", bowl="bowl",
           n22="22", n28="28", n32="32", n33="33", n39="39", n40="40", n42="42", perfect="A perfect", split="splitting", wrong="wrong", full="in full", because="Because 110")
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
