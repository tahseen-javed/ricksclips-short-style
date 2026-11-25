#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 26: the penny cost almost 4 cents to make 1 cent - and made a fortune the day it died.
usage: build_short.py <project folder>
Twelve copper-candy sets 70 units apart: HK lilac-pink Mint press hall (hook + loop; a velvet "?" lot = open loop, resolved as the sold penny sets),
MT mint-green Mint facade, PG plum piggy vault, TN pastel penny town diorama, JR buttercup kitchen, CU teal living room, PK magenta sunset parking lot,
SG cyan spotlight stage, RD sky-blue highway, PH autumn Philadelphia, AU red-velvet auction house, HV pink-gold cloud heaven.
Shots 0.7-2 s, every neighbour a different move; the penny is the hero (glossy coin with a face), people are small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, MT=70, PG=140, TN=210, JR=280, CU=350, PK=420, SG=490, RD=560, PH=630, AU=700, HV=770)
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


yard("HK", "presshall.png", "steel.jpg"); box("HK", -1.8, 0.04, -3.4, [0.9, 0.5, 0.8], color="#b48cdc"); box("HK", 2.4, 0.04, -1.2, [0.6, 0.35, 0.6], color="#e2804a"); box("HK", -0.4, 0.04, -2.0, [0.8, 0.36, 0.6], color="#ff3cac")
yard("MT", "mintsky.png", "marble.jpg"); box("MT", 0, 0.04, -2.4, [5.0, 0.12, 1.4], color="#f0ece0")
yard("PG", "vault.png", "plum.jpg"); box("PG", 1.7, 0.04, -3.2, [0.7, 0.9, 0.7], color="#f0c440")
yard("TN", "pastel.png", "lawn.jpg")
for x, z, rf, c in ((-2.6, -3.6, "#ff7aa8", "#fff4e0"), (2.4, -3.8, "#5ec8b0", "#fff0f4"), (-3.2, -1.6, "#ffc23c", "#f4f0ff"), (4.6, -3.4, "#9a78e0", "#fff8e0")): house("TN", x, z, [1.2, 1.0, 1.0], rf, color=c)
for x, z in ((-1.4, -4.2), (1.2, -4.4), (-4.2, -2.8), (4.2, -2.6)): tree("TN", x, z, 0.6, "#78c878")
yard("JR", "kitchen.png", "ktile.jpg"); box("JR", 0, 0.04, -2.2, [2.2, 0.74, 1.0], color="#c88a50")
yard("CU", "living.png", "wood.jpg"); box("CU", 0, 0.01, -2.2, [3.4, 0.03, 2.2], color="#ffd27a")
yard("PK", "parklot.png", "asphalt.jpg")
for x in (-1.6, 0.0, 1.6): box("PK", x, 0.045, -2.4, [0.08, 0.01, 2.6], color="#ffffff")
yard("SG", "cyanstage.png", "stage.jpg"); box("SG", 0, 0.04, -2.4, [1.4, 0.4, 1.0], color="#ff3cac")
yard("RD", "highway.png", "road.jpg"); box("RD", 0, 0.045, -1.6, [12, 0.01, 0.12], color="#ffe060")
yard("PH", "philly.png", "brick.jpg")
yard("AU", "velvet.png", "carpet.jpg"); box("AU", -2.2, 0.04, -3.6, [0.8, 1.1, 0.5], color="#ffce3c")
yard("HV", "heaven.png", "cloud.jpg")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("pennyH", "penny", pos("HK", -0.4, 0.4, -2.0), 0.95, face="shocked"); put("pressH", "press", pos("HK", 0.62, 0.04, -2.6), 1.8); put("qlot_H", "qlot", pos("HK", -1.8, 0.54, -3.4), 0.8)
put("prowH", "prow", pos("HK", -2.9, 0.04, -2.6), 0.6); human("mintwH", "mintw", pos("HK", -4.0, 0.04, -2.2), face="happy", h=1.6); put("pennyG", "penny", PARK, 0.8, face="gold")
put("mintbM", "mintb", pos("MT", 0.0, 0.16, -2.4), 1.8)
put("piggyP", "piggy", pos("PG", 0.0, 0.04, -2.4), 1.2); put("printerP", "printer", pos("PG", 3.4, 0.04, -2.4), 1.4); put("ledgerP", "ledger", pos("PG", -3.4, 0.04, -2.4), 1.2)
put("pileT", "pile", pos("TN", 0.0, 0.04, -2.6), 1.0)
for k, (x, z) in enumerate(((1.6, -1.6), (2.4, -2.4), (3.6, -2.0))): put("penT%d_" % k, "penny", pos("TN", x, 0.04, z), 0.35)
put("jarJ", "jar", pos("JR", 0.0, 0.78, -2.2), 1.0)
put("couchC", "couch", pos("CU", -0.15, 0.04, -2.4), 0.75); human("kidC", "kid", pos("CU", 0.95, 0.04, -2.0), face="happy", h=1.25)
put("pennyK", "penny", pos("PK", -0.4, 0.04, -1.8), 0.45); put("carK", "car", pos("PK", 0.9, 0.04, -2.9), 0.7)
put("pennyS", "penny", pos("SG", 0.0, 0.44, -2.4), 1.0); put("scaleS", "scale", pos("SG", -3.4, 0.04, -2.6), 1.5); put("thermoS", "thermo", pos("SG", 3.0, 0.04, -2.4), 1.8)
put("vanR", "vantr", pos("RD", 0.2, 0.04, -2.4), 1.0)
put("hallH", "hall", pos("PH", 0.0, 0.04, -3.2), 2.4)
put("podiumA", "podium", pos("AU", 0.55, 0.04, -2.4), 1.2); human("auctA", "auct", pos("AU", -0.75, 0.04, -2.1), face="happy"); put("casesA", "cases", pos("AU", 4.0, 0.04, -2.8), 1.0)
put("crowdA", "crowd", pos("AU", -4.2, 0.04, -2.2), 0.8); put("qlotA", "qlot", pos("AU", -2.2, 1.14, -3.6), 0.9)
put("qlotV", "qlot", pos("HV", 0.0, 0.04, -2.2), 1.2); put("throne_V", "throne", pos("HV", 0.0, 0.04, -3.8), 2.0); put("pennyV", "penny", pos("HV", -0.85, 0.04, -2.0), 0.7, face="crown")
put("pennyA", "penny", pos("HV", 2.4, 0.5, -2.2), 0.9, face="halo")
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


HOOK = dict(anchor=(0.2, 1.2, -2.3), dist=6.4, yaw=4, pitch=6)
# ---- It cost America almost four cents to make one cent. Every single time.
s = S("0", "HK", zoom=7, **HOOK); act(s, 0.0, "pennyH", face="shocked", shake=0.4); act(s, 0.0, "pressH", face="slam", shake=0.5); act(s, 0.45, "pressH", face="default"); tag(s, 0.0, "hookc", 0.33, 0.0, wf=0.6, hf=0.2); snap(s, rel(s, "four"), 10)
s = S("to make one", "HK", (0.62, 1.0, -2.6), 4.0, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="pressH", blur=0.5)); hide(s, 0.0, "pennyH"); act(s, rel(s, "one") - 0.1, "pressH", face="slam", shake=0.6)
s = crane("Every single", "HK", (-3.3, 0.8, -2.5), 6.0, 22, 2, 36, 8); act(s, 0.1, "prowH", shake=0.4); ft(s, "mintwH", ["shocked", "happy"]); c_ = T(s, "every", at=0.1, dy=0.36); swap(s, c_, rel(s, "Not"), "notonce", dy=0.36, wf=0.5)
# ---- Not once. For nineteen straight years, the penny cost more than it was worth.
s = S("For nineteen straight", "SG", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="NINETEEN STRAIGHT", items=["19 YEARS"]))
s = S("the penny cost", "SG", (-3.4, 0.95, -2.6), 6.8, -14, pitch=6, yawTo=4, dof=dict(focus="scaleS", blur=0.4)); act(s, rel(s, "more"), "scaleS", face="tip", shake=0.5); snap(s, rel(s, "more"), 8)
# ---- In 2024 alone, the U.S. Mint lost 85 million dollars making money. Literally making money.
s = crane("In 2024 alone", "MT", (0.0, 1.2, -2.6), 9.0, -22, -2, 36, 8); T(s, "y2024", at=rel(s, "2024"), dy=0.28, wf=0.26, hf=0.26)
s = S("Mint lost", "PG", (0.0, 0.85, -2.4), 5.6, 8, pitch=5, zoom=14, dof=dict(focus="piggyP", blur=0.4)); act(s, rel(s, "lost"), "piggyP", face="leak", shake=0.6); T(s, "lost85", at=rel(s, "85"), dy=0.37, wf=0.6); snap(s, rel(s, "85"), 8)
s = S("making money", "PG", (3.4, 1.2, -2.4), 4.2, 12, pitch=5, yawTo=-4, type="macro", dof=dict(focus="printerP", blur=0.5)); act(s, 0.05, "printerP", shake=0.6); T(s, "literally", at=rel(s, "Literally"), dy=0.36, wf=0.6)
# ---- And about 300 billion pennies are still out there. In jars. Under couch cushions. On parking lot floors.
s = crane("And about 300", "TN", (0.0, 0.6, -2.6), 7.0, -22, -2, 40, 10); act(s, rel(s, "300"), "pileT", shake=0.5); T(s, "b300", at=rel(s, "300"), dy=0.34, wf=0.5)
s = S("are still out", "TN", (2.4, 0.7, -2.0), 6.0, 10, pitch=14, zoom=4, pan=(8, 0)); hide(s, 0.0, "pileT")
for k in range(3): act(s, 0.1 + 0.15 * k, "penT%d_" % k, shake=0.4)
s = S("In jars", "JR", (0.0, 1.35, -2.2), 3.8, -14, pitch=6, yawTo=6, type="macro", dof=dict(focus="jarJ", blur=0.5)); act(s, 0.05, "jarJ", shake=0.4)
s = S("couch cushions", "CU", (0.3, 0.85, -2.2), 6.0, 8, pitch=5, zoom=-10); act(s, rel(s, "cushions"), "couchC", face="lift", shake=0.5); ft(s, "kidC", ["happy", "shocked"])
s = S("On parking lot", "PK", (0.2, 0.55, -2.3), 4.6, -6, pitch=18, pitchTo=4, dof=dict(focus="pennyK", blur=0.4)); go(s, 0.1, "carK", pos("PK", 0.3, 0.04, -2.9), 1.2, walk=False); act(s, 0.3, "pennyK", face="shocked", shake=0.4)
# ---- You see, one cent never changed. But the cost to make it, manage it and ship it kept climbing, to 3.69 cents a coin.
s = S("You see one", "SG", (0.0, 1.0, -2.4), 5.0, 14, pitch=5, yawTo=-4); act(s, 0.05, "pennyS", face="default"); T(s, "onecent", at=rel(s, "one"), dy=0.37, wf=0.56)
s = S("But the cost", "HK", (0.62, 1.0, -2.6), 4.2, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="pressH", blur=0.5)); hide(s, 0.0, "pennyH"); act(s, rel(s, "make"), "pressH", face="slam", shake=0.5); c_ = T(s, "make", at=rel(s, "make"), dy=0.38, wf=0.44); swap(s, c_, rel(s, "manage"), "manage", dy=0.38, wf=0.5)
s = S("ship it", "RD", (0.2, 0.75, -2.4), 5.6, 6, pitch=5, zoom=4, pan=(-8, 0)); act(s, 0.05, "vanR", shake=0.3); T(s, "ship", dy=0.37, wf=0.44)
s = S("369", "SG", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="KEPT CLIMBING", items=["3.69 CENTS A COIN"]))
# ---- So on November 12, 2025, in Philadelphia, America struck its last circulating penny.
s = crane("So on November", "PH", (0.0, 1.3, -3.2), 9.0, 22, 2, 36, 8); T(s, "nov12", at=rel(s, "November"), dx=0.2, dy=0.12, wf=0.26, hf=0.26)
s = S("in Philadelphia", "PH", (0.0, 1.4, -3.2), 6.6, -8, pitch=5, zoom=12, dof=dict(focus="hallH", blur=0.4)); T(s, "philly", dy=0.37, wf=0.6)
s = S("struck its last", "HK", (0.3, 1.0, -2.4), 5.0, -6, pitch=6, zoom=10); hide(s, 0.0, "pennyH"); show(s, rel(s, "last"), "pennyG", pos("HK", 0.35, 0.04, -1.6)); act(s, 0.05, "pressH", face="slam", shake=0.6); T(s, "last", at=rel(s, "last"), dy=0.38, wf=0.5); snap(s, rel(s, "struck"), 10)
# ---- Then something strange happened. The final pennies went to auction. 232 sets. They sold for 16.76 million dollars. One set alone went for 800,000 dollars.
s = S("Then something", "AU", (-2.2, 1.6, -3.4), 4.8, 10, pitch=14, pitchTo=3, dof=dict(focus="qlotA", blur=0.4)); act(s, 0.1, "qlotA", shake=0.4); T(s, "strange", dy=0.37, wf=0.62)
s = crane("The final pennies", "AU", (-0.1, 1.0, -2.3), 7.0, -22, -2, 36, 8); ft(s, "auctA", ["happy", "shocked"])
s = S("232 sets", "AU", (4.0, 0.6, -2.8), 5.4, 12, pitch=5, yawTo=-4, dof=dict(focus="casesA", blur=0.4)); T(s, "sets232", dy=0.37, wf=0.44)
s = S("They sold for", "SG", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="THEY SOLD FOR", items=["$16.76 MILLION"]))
s = S("million dollars#2", "AU", (4.0, 0.6, -2.8), 4.6, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="casesA", blur=0.5)); act(s, 0.05, "casesA", shake=0.4)
s = S("One set alone", "AU", (-4.2, 0.6, -2.2), 5.2, 14, pitch=6, yawTo=-4); act(s, 0.1, "crowdA", shake=0.5); act(s, 0.6, "crowdA", shake=0.5)
s = S("for 800000", "AU", (-0.2, 1.0, -2.2), 5.4, -6, pitch=5, zoom=14, dof=dict(focus="auctA", blur=0.4)); hide(s, 0.0, "podiumA"); hide(s, 0.0, "qlotA"); ft(s, "auctA", ["shocked", "happy"]); act(s, 0.1, "auctA", pose=dict(armR=-150)); T(s, "k800", at=rel(s, "800000"), dy=0.38, wf=0.56); snap(s, rel(s, "800000"), 10)
# ---- The coin that lost money for almost twenty years finally made a fortune the day it died.
s = S("The coin that", "PG", (0.0, 0.85, -2.4), 5.2, -14, pitch=6, yawTo=4, dof=dict(focus="piggyP", blur=0.4)); act(s, 0.05, "piggyP", face="leak", shake=0.4)
s = S("for almost twenty", "SG", (3.0, 1.0, -2.4), 5.4, 8, pitch=5, zoom=-10); act(s, 0.0, "thermoS", face="t4", shake=0.5); T(s, "twenty", at=rel(s, "twenty"), dy=0.37, wf=0.5)
s = crane("finally made a", "HV", (-0.1, 1.0, -2.2), 6.6, 22, 2, 36, 8); act(s, rel(s, "fortune"), "qlotV", face="open", shake=0.6); ft(s, "pennyV", ["crown", "gold"]); T(s, "fortune", at=rel(s, "fortune"), dy=0.36, wf=0.5); snap(s, rel(s, "fortune"), 10)
s = S("the day it", "HV", (2.4, 1.2, -2.2), 4.6, -10, pitch=5, zoom=10, dof=dict(focus="pennyA", blur=0.4)); go(s, 0.05, "pennyA", pos("HV", 2.4, 0.75, -2.2), 0.9, walk=False); T(s, "bye", at=rel(s, "died") - 0.1, dy=0.38, wf=0.5)
# ---- All because it cost America almost four cents to make one cent.
s = crane("All because it", "HK", (0.2, 1.2, -2.3), 7.6, -22, -2, 36, 8); show(s, 0.0, "pennyH", pos("HK", -0.4, 0.4, -2.0), hop=0); hide(s, 0.0, "pennyG"); act(s, 0.1, "pennyH", face="default")
s = S("four cents#2", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.05, "pennyH", face="shocked", shake=0.4); act(s, rel(s, "make") - 0.05, "pressH", face="slam", shake=0.5); T(s, "hookc", at=0.05, dy=0.33, wf=0.6, hf=0.2)
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
ATM = dict(HK=dict(dust=D_(24), rays=dict(angle=24, intensity=0.6)), MT=dict(dust=D_(22), rays=dict(angle=30, intensity=0.6)), PG=dict(bokeh=BK(0.5)), TN=dict(dust=D_(22), rays=dict(angle=26, intensity=0.5)),
           JR=dict(dust=D_(26), rays=dict(angle=20, intensity=0.6)), CU=dict(dust=D_(26)), PK=dict(bokeh=BK(0.45)), SG=dict(bokeh=BK(0.5)), RD=dict(dust=D_(20), rays=dict(angle=30, intensity=0.5)),
           PH=dict(bokeh=BK(0.45)), AU=dict(bokeh=BK(0.5)), HV=dict(dust=D_(30), rays=dict(angle=18, intensity=0.7)))
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
MOOD = dict(HK="presspink", MT="mintmorn", PG="plumvault", TN="pasteltown", JR="butter", CU="tealroom", PK="magsunset", SG="cyanspot", RD="skyroad", PH="phillydusk", AU="velvet", HV="heaven")
light, cur = [{"t": 0, "mood": "presspink"}], "presspink"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"presspink": {"sun": {"azimuth": 30, "elevation": 40, "color": "#fff0f4", "intensity": 2.6}, "sky": {"top": "#966edc", "horizon": "#ffaac8"}, "fill": {"sky": "#fff0fa", "ground": "#6a4a8a", "intensity": 1.8}},
              "mintmorn": {"sun": {"azimuth": 40, "elevation": 44, "color": "#fffbe8", "intensity": 2.4}, "sky": {"top": "#6edcbe", "horizon": "#fff6dc"}, "fill": {"sky": "#f4fff8", "ground": "#5a9a7a", "intensity": 1.4}},
              "plumvault": {"sun": {"azimuth": 20, "elevation": 40, "color": "#fff0d8", "intensity": 2.7}, "sky": {"top": "#461e5a", "horizon": "#aa508c"}, "fill": {"sky": "#fff0f8", "ground": "#4a2a5a", "intensity": 2.2}},
              "pasteltown": {"sun": {"azimuth": 210, "elevation": 34, "color": "#fff4e8", "intensity": 2.4}, "sky": {"top": "#82befa", "horizon": "#ffd6be"}, "fill": {"sky": "#fff8f4", "ground": "#6aa070", "intensity": 1.5}},
              "butter": {"sun": {"azimuth": 150, "elevation": 36, "color": "#fff4d0", "intensity": 2.4}, "sky": {"top": "#ffd65a", "horizon": "#fff0b4"}, "fill": {"sky": "#fffbe8", "ground": "#a07a4a", "intensity": 1.5}},
              "tealroom": {"sun": {"azimuth": 200, "elevation": 30, "color": "#ffe8d0", "intensity": 2.5}, "sky": {"top": "#2896a0", "horizon": "#5ac8c8"}, "fill": {"sky": "#f0ffff", "ground": "#7a5a4a", "intensity": 1.8}},
              "magsunset": {"sun": {"azimuth": 230, "elevation": 16, "color": "#ffc8b0", "intensity": 2.6}, "sky": {"top": "#e65096", "horizon": "#ffbe64"}, "fill": {"sky": "#ffe8f0", "ground": "#5a4a6a", "intensity": 2.0}},
              "cyanspot": {"sun": {"azimuth": 10, "elevation": 42, "color": "#f0fffc", "intensity": 2.7}, "sky": {"top": "#103250", "horizon": "#1e96aa"}, "fill": {"sky": "#e8fffc", "ground": "#1e4a64", "intensity": 2.2}},
              "skyroad": {"sun": {"azimuth": 40, "elevation": 46, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#5aaafa", "horizon": "#dcf0ff"}, "fill": {"sky": "#f4faff", "ground": "#6a8a6a", "intensity": 1.4}},
              "phillydusk": {"sun": {"azimuth": 230, "elevation": 18, "color": "#ffc8a0", "intensity": 2.5}, "sky": {"top": "#6e4696", "horizon": "#ffa064"}, "fill": {"sky": "#fff0e8", "ground": "#6a4a4a", "intensity": 1.9}},
              "velvet": {"sun": {"azimuth": 10, "elevation": 46, "color": "#fff4e0", "intensity": 3.1}, "sky": {"top": "#a01e3c", "horizon": "#f05a5a"}, "fill": {"sky": "#fff4f0", "ground": "#a05a64", "intensity": 2.7}},
              "heaven": {"sun": {"azimuth": 200, "elevation": 30, "color": "#fff4e0", "intensity": 2.4}, "sky": {"top": "#ffaad2", "horizon": "#ffe696"}, "fill": {"sky": "#fffaf4", "ground": "#d2aab4", "intensity": 1.6}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff3cac", "paper": ["#6cc8b4", "#4eae9a"], "dofPx": 8, "particle": "#fff4e0", "bokehColor": "#ffd0f0", "ray": "#fff6dc", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(yousee="You see one", nov="So on November", strange="Then something", coin="The coin that", fortune="finally made a",
           four="four cents", one="to make one", every="Every single", notonce="Not once", nineteen="nineteen", more="more than", y2024="2024", lost="Mint lost", b85="85",
           lit="Literally", b300="300", jars="In jars", cush="cushions", park="parking", cost="But the cost", make="make it", manage="manage it", ship="ship it", climb="369",
           philly="Philadelphia", struck="struck", auction="auction", sets="232", sold="They sold", k800="800000", twenty="twenty", died="died", allb="All because")
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
