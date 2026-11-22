#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 16: A farm boy found a planet (Clyde Tombaugh, Pluto, New Horizons).
usage: build_short.py <project folder>
Fourteen sets 70 units apart: FM Kansas farm at night (hook + loop), HL hailstorm field, WB lantern workshop barn, AT attic at night,
MB mailbox road at sunset, LO Lowell dome at dusk, PX teal nebula with Planet X, BC red-lamp blink room, NW sunny 1930 news street,
LC bright launch day, CR white clean room, SP icy Pluto flyby, VT blue voting hall, TX cream study desk.  Every shot moves (crane /
push-in / pull-out); same-set shots fly (dolly glide), new sets dissolve.  Snap-ins, atmosphere, depth of field, comic fx, blinking
photo plates.  Cards are fitted to the safe box; the frame check prints CUT / SIGNCUT / INSIDE / OVERLAP flags."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(FM=0, HL=70, WB=140, AT=210, MB=280, LO=350, PX=420, BC=490, NW=560, LC=630, CR=700, SP=770, VT=840, TX=910)
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


def rock(loc, x, y, z, s, col): box(loc, x, y, z, [s, s * 0.7, s * 0.9], color=col)


yard("FM", "farm.png", "wheat.jpg"); house("FM", -3.4, -4.4, [2.0, 1.8, 1.6], "#7a2a24", color="#c84a3a"); box("FM", 2.8, 0.04, -2.6, [0.9, 0.6, 0.6], color="#e6c86a"); box("FM", 3.4, 0.04, -3.4, [0.8, 0.55, 0.6], color="#e6c86a")
for x in (-1.6, -0.6, 0.4, 1.4): post("FM", x, -4.0, 0.8, "#8a6a4a")
yard("HL", "hail.png", "mud.jpg"); house("HL", 3.4, -4.6, [1.8, 1.4, 1.4], "#6a4a3a", color="#ece2c8")
for x in (-3.4, -2.6, -1.8): post("HL", x, -3.6, 0.8, "#6a5a4a")
yard("WB", "barn.png", "plank.jpg"); table("WB", 2.75, -2.2, 1.8, 0.8, 0.7, "#8a5a3a"); crate("WB", -3.6, 0.04, -3.6, 0.6); crate("WB", 3.6, 0.04, -3.6, 0.6)
yard("AT", "attic.png", "atticwood.jpg"); table("AT", 0.5, -2.0, 1.4, 0.7, 0.74, "#9a6a4a"); box("AT", -2.8, 0.04, -3.0, [1.0, 0.6, 0.7], color="#8a5a6a")
yard("MB", "mailroad.png", "road.jpg"); tree("MB", -3.4, -3.8, 0.8)
for x in (1.8, 2.6, 3.4): post("MB", x, -3.4, 0.9, "#7a5a3a")
yard("LO", "lowell.png", "redrock.jpg"); tree("LO", -3.4, -4.0, 0.9, "#2e6a4a"); tree("LO", 3.4, -4.4, 1.0, "#2e6a4a"); rock("LO", -2.6, 0.04, -2.6, 0.6, "#b06040"); rock("LO", 2.8, 0.04, -2.8, 0.5, "#b06040")
yard("PX", "nebula.png", "spacefloor.jpg")
for x, y, z, s in ((-3.0, 1.8, -3.4, 0.5), (3.2, 2.6, -4.0, 0.4), (-2.0, 3.2, -4.6, 0.3), (2.6, 1.0, -2.6, 0.35)): rock("PX", x, y, z, s, "#3a7a7a")
yard("BC", "blinkroom.png", "redtile.jpg"); box("BC", -3.0, 0.04, -2.2, [0.9, 0.8, 0.5], color="#6a3a30"); box("BC", 3.2, 0.04, -3.2, [0.9, 1.0, 0.7], color="#5a3030")
yard("NW", "news.png", "cobble2.jpg"); house("NW", -3.6, -4.6, [1.6, 2.4, 1.4], "#5a3a3a", color="#c8785a"); house("NW", 3.6, -4.8, [1.6, 2.8, 1.4], "#3a4a6a", color="#8aa0c8"); post("NW", -2.6, -2.6, 2.4, "#3a3a40"); post("NW", 2.6, -2.8, 2.4, "#3a3a40")
yard("LC", "launchday.png", "concrete.jpg"); box("LC", 0.9, 0.04, -3.2, [1.6, 0.25, 1.2], color="#9a9aa0"); box("LC", -3.0, 0.04, -3.0, [1.2, 0.5, 0.8], color="#d0d0d8")
yard("CR", "cleanroom.png", "whitetile.jpg"); box("CR", 1.3, 0.04, -2.5, [1.2, 0.6, 1.0], color="#c8d4dc"); box("CR", -3.0, 0.04, -3.0, [1.0, 0.9, 0.6], color="#e0e8ee")
yard("SP", "flyby.png", "ice.jpg")
for x, z, s in ((-3.2, -2.6, 0.6), (3.2, -3.0, 0.5), (2.2, -4.4, 0.4)): rock("SP", x, 0.04, z, s, "#c8bcb0")
yard("VT", "hall.png", "bluecarpet.jpg"); box("VT", 0.0, 0.04, -3.4, [3.0, 0.8, 0.6], color="#3a4a8a")
yard("TX", "study.png", "studyfloor.jpg"); table("TX", 0.3, -2.2, 2.4, 1.0, 0.74, "#a0683c"); box("TX", -3.0, 0.04, -3.0, [0.6, 1.2, 0.6], color="#8a5a3a")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
CF = pos("FM", -0.75, 0.04, -1.5)
human("clydeF", "clyde", CF, face="happy"); put("scopeF", "scope", pos("FM", 0.9, 0.04, -1.9), 1.5)
human("dadH", "dad", pos("HL", -1.5, 0.04, -1.9), face="shocked"); human("momH", "mom", pos("HL", -0.6, 0.04, -2.3), face="shocked"); human("clydeH", "clyde", pos("HL", 1.3, 0.04, -1.6), face="nervous")
human("clydeW", "clyde", pos("WB", -0.9, 0.04, -1.6), face="happy"); put("scopeW", "scope", pos("WB", 0.3, 0.04, -1.9), 1.3); put("carW", "car", pos("WB", -3.0, 0.04, -2.2), 0.7)
put("crankW", "crank", pos("WB", 2.15, 0.74, -2.1), 0.28); put("sepW", "sep", pos("WB", 3.3, 0.74, -2.1), 0.5)
human("clydeA", "clyde", pos("AT", -0.6, 0.04, -1.6), face="happy"); put("sketchA", "sketch", pos("AT", 0.5, 0.78, -1.9), 0.45)
human("clydeM", "clyde", pos("MB", -0.6, 0.04, -1.5), face="happy"); put("mbox", "mailbox", pos("MB", 0.9, 0.04, -1.8), 1.3); put("envM", "env", pos("MB", -0.05, 0.95, -1.4), 0.25); put("letM", "letter", PARK, 0.4)
human("astroL", "astro", pos("LO", 0.8, 0.04, -1.9), face="happy"); human("clydeO", "clydeo", PARK, face="neutral")
put("pxP", "px", pos("PX", 0.0, 1.0, -2.6), 1.6)
human("clydeB", "clyde", pos("BC", -1.2, 0.04, -1.5), face="neutral"); put("compB", "comp", pos("BC", 0.6, 0.04, -1.9), 1.4); put("platesB", "plates", pos("BC", -3.0, 0.84, -2.0), 0.5)
human("newsN", "newsboy", pos("NW", -0.8, 0.04, -1.5), face="shouting"); put("paperN", "paper30", pos("NW", -0.2, 0.9, -1.4), 0.55); put("plutoN", "pluto", pos("NW", 1.0, 1.0, -2.2), 1.0)
put("rocketL", "rocket2", pos("LC", 0.9, 0.29, -3.2), 3.8); human("engL", "eng", pos("LC", -1.0, 0.04, -1.6), face="happy")
human("engC", "eng", pos("CR", -0.9, 0.04, -1.6), face="happy"); put("capC", "capsule", pos("CR", -0.3, 0.95, -1.45), 0.35); put("probeC", "probe", pos("CR", 1.3, 0.64, -2.3), 1.2)
put("plutoS", "pluto", pos("SP", -1.6, 0.4, -4.0), 2.0); put("probeS", "probe", pos("SP", 0.6, 1.2, -2.0), 0.8); human("clydeS", "clyde", PARK, face="happy")
human("v1", "v1", pos("VT", -1.3, 0.04, -1.8), face="smug"); human("v2", "v2", pos("VT", 0.0, 0.04, -2.1), face="smug")
put("vc1", "vcard", pos("VT", -0.85, 1.75, -1.7), 0.4); put("vc2", "vcard", pos("VT", 0.45, 1.75, -2.0), 0.4); put("plutoV", "pluto", pos("VT", 1.9, 1.2, -2.4), 1.1)
put("tbookT", "tbook", pos("TX", 0.0, 0.78, -2.1), 0.8); put("plutoT", "pluto", pos("TX", 0.95, 0.78, -2.0), 0.55, face="sad")
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


HOOK = dict(anchor=(0.1, 1.2, -1.7), dist=9.2, yaw=4, pitch=8)
# ---- 0: A farm boy found a planet with a telescope built from an old car. Eighty-five years later, he flew there.
s = S("0", "FM", zoom=7, pan=(-3, 0), **HOOK); ft(s, "clydeF", ["shocked", "happy", "shocked"]); act(s, 0.0, "clydeF", pose=dict(armR=-150)); act(s, 0.1, "scopeF", shake=0.3)
tag(s, 0.0, "farmboy", 0.3, 0.0, wf=0.62, hf=0.22); snap(s, max(0.82, rel(s, "planet")), 12)
s = S("with a telescope", "FM", (0.9, 0.9, -1.9), 3.6, -10, pitch=4, yawTo=4, type="macro", dof=dict(focus="scopeF", blur=0.5)); act(s, 0.1, "scopeF", shake=0.3)
s = S("built from", "FM", (-0.75, 1.25, -1.5), 4.6, 10, pitch=5, zoom=12, dof=dict(focus="clydeF", blur=0.4)); ft(s, "clydeF", ["smug", "happy"]); T(s, "oldcar")
s = crane("Eightyfive years", "SP", (-0.6, 1.3, -3.2), 10.0, 18, 2, 20, 5); act(s, 0.1, "probeS", shake=0.3); T(s, "flew"); snap(s, rel(s, "flew"), 12)
# ---- Kansas. A hailstorm wipes out the Tombaugh family's crops. Clyde, twenty-two, can't afford college.
s = crane("Kansas", "HL", (-0.1, 1.2, -1.9), 10.0, -24, -4, 36, 6); ft(s, "dadH", ["shocked", "nervous"]); ft(s, "momH", ["nervous", "shocked"]); ft(s, "clydeH", ["nervous", "confused"])
c_ = T(s, "kansas", dy=0.32, wf=0.45, hf=0.12); swap(s, c_, rel(s, "hailstorm"), "hailst", wf=0.55, hf=0.13)
s = S("the Tombaugh", "HL", (-1.05, 1.25, -2.1), 5.6, 10, pitch=5, zoom=10); ft(s, "dadH", ["shocked", "nervous"]); ft(s, "momH", ["nervous", "shocked"]); T(s, "crops"); cfx(s, 0.3, "sweat", "dadH", 0.8)
s = S("Clyde twentytwo", "HL", (1.3, 1.25, -1.6), 4.6, -10, pitch=5, zoom=12, dof=dict(focus="clydeH", blur=0.4)); ft(s, "clydeH", ["nervous", "confused", "nervous"]); T(s, "college"); snap(s, rel(s, "college"), 12)
# ---- So in 1928 he builds his own telescope. The parts? The crankshaft of a 1910 Buick and pieces of a cream separator.
s = crane("So in 1928", "WB", (-0.3, 1.2, -1.8), 8.0, 8, 0, 24, 6); ft(s, "clydeW", ["happy", "smug"]); act(s, 0.1, "scopeW", shake=0.3); T(s, "y1928", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("he builds his", "WB", (-0.3, 1.2, -1.8), 5.4, -12, pitch=5, zoom=10); ft(s, "clydeW", ["smug", "happy"]); act(s, 0.0, "clydeW", pose=dict(armR=-150)); T(s, "ownscope"); snap(s, rel(s, "telescope"), 12)
s = S("The parts", "WB", (-3.0, 0.45, -2.2), 3.4, 10, pitch=4, yawTo=2, type="macro", dof=dict(focus="carW", blur=0.5)); act(s, 0.1, "carW", shake=0.3); T(s, "parts", dy=0.3, wf=0.5, hf=0.14)
s = S("The crankshaft", "WB", (2.3, 0.88, -2.1), 2.6, -8, pitch=4, yawTo=4, type="macro", dof=dict(focus="crankW", blur=0.5)); act(s, 0.1, "crankW", shake=0.2); T(s, "buick"); snap(s, rel(s, "Buick"), 12)
s = S("and pieces of", "WB", (3.3, 1.0, -2.1), 2.8, 8, pitch=4, yawTo=-2, type="macro", dof=dict(focus="sepW", blur=0.5)); act(s, 0.1, "sepW", shake=0.3); T(s, "cream")
# ---- He sketches Jupiter and Mars and mails the drawings to Lowell Observatory in Arizona. He wants advice. They send back a job offer.
s = crane("He sketches", "AT", (0.0, 1.2, -1.8), 8.4, -22, -2, 36, 6); ft(s, "clydeA", ["happy", "smug"]); act(s, 0.1, "sketchA", shake=0.3); T(s, "sketches")
s = crane("and mails the", "MB", (0.15, 1.2, -1.7), 8.6, 22, 2, 30, 6); ft(s, "clydeM", ["happy", "smug"]); act(s, 0.1, "mbox", shake=0.3); T(s, "mails")
s = crane("to Lowell Observatory", "LO", (0.3, 1.3, -2.0), 9.0, -20, -2, 34, 6); ft(s, "astroL", ["happy", "smug"]); T(s, "lowell"); snap(s, rel(s, "Arizona"), 12)
s = S("He wants advice", "MB", (-0.6, 1.25, -1.5), 4.6, 10, pitch=5, zoom=12, dof=dict(focus="clydeM", blur=0.4)); ft(s, "clydeM", ["nervous", "happy"]); T(s, "advice")
s = S("They send back", "MB", (0.15, 1.2, -1.6), 6.2, -12, pitch=5, zoom=8, yawTo=-2); hide(s, 0.05, "envM"); show(s, 0.08, "letM", pos("MB", -0.05, 0.95, -1.4)); ft(s, "clydeM", ["shocked", "happy"])
T(s, "joboffer", dy=0.3, wf=0.56); snap(s, rel(s, "offer"), 14); cfx(s, 0.3, "glint", "clydeM", 0.7)
# ---- You see, Lowell was hunting a mystery world called Planet X.
s = S("You see Lowell", "LO", (0.8, 1.25, -1.9), 5.2, 12, pitch=8, zoom=10); ft(s, "astroL", ["confused", "neutral"]); act(s, 0.0, "astroL", pose=dict(armR=-150)); T(s, "hunting"); cfx(s, 0.3, "question", "astroL", 0.8)
s = crane("a mystery world", "PX", (0.0, 1.4, -2.6), 8.4, 24, 4, 30, 6); act(s, 0.1, "pxP", shake=0.3); T(s, "planetx", dy=0.32, wf=0.56); snap(s, rel(s, "X"), 14)
# ---- They gave the farm boy the most tedious job in astronomy. Flip between two photos of the same sky, taken days apart, and find the one dot that moves. Among countless stars.
s = crane("They gave the", "BC", (-0.3, 1.2, -1.8), 8.4, -22, -2, 34, 6); ft(s, "clydeB", ["neutral", "confused"]); act(s, 0.1, "compB", shake=0.2)
s = S("the most tedious", "BC", (-1.2, 1.25, -1.5), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="clydeB", blur=0.4)); ft(s, "clydeB", ["sneaky", "neutral"]); T(s, "tedious"); cfx(s, 0.3, "z", "clydeB", 0.9)
s = S("Flip between", "BC", (-3.0, 1.09, -2.0), 3.0, -10, pitch=4, yawTo=2, type="macro", dof=dict(focus="platesB", blur=0.5)); blink(s, "platesB", 0.2, 3.0); T(s, "flip"); snap(s, rel(s, "photos"), 10)
s = S("taken days apart", "BC", (-0.3, 1.25, -1.7), 7.6, 12, pitch=6, zoom=8, yawTo=2); ft(s, "clydeB", ["neutral", "confused"]); act(s, 0.1, "compB", shake=0.2); T(s, "days")
s = S("and find the", "BC", (-3.0, 1.09, -2.0), 3.0, 10, pitch=4, yawTo=-2, type="macro", dof=dict(focus="platesB", blur=0.5)); blink(s, "platesB", 0.1, 3.0, 0.25); T(s, "onedot"); snap(s, rel(s, "moves"), 12)
s = crane("Among countless", "PX", (0.0, 1.3, -2.6), 9.0, -26, -4, 40, 8); act(s, 0.1, "pxP", shake=0.2); T(s, "countless")
# ---- February 18th, 1930. He finds it. He is twenty-four. The world names it Pluto.
s = crane("February 18th", "BC", (-0.2, 1.2, -1.8), 8.6, 16, 2, 26, 6); act(s, 0.0, "compB", shake=0.4); ft(s, "clydeB", ["shocked", "happy"]); T(s, "y1930", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("He finds it", "BC", (-1.2, 1.25, -1.5), 4.4, -10, pitch=5, zoom=12, dof=dict(focus="clydeB", blur=0.4)); ft(s, "clydeB", ["shouting", "happy"]); act(s, 0.0, "clydeB", pose=dict(armR=-150, armL=150)); T(s, "finds", wf=0.55, hf=0.14); snap(s, rel(s, "finds"), 14); cfx(s, 0.25, "bang", "clydeB", 0.6)
s = S("He is", "BC", (-0.3, 1.25, -1.7), 7.8, -12, pitch=6, zoom=10); ft(s, "clydeB", ["happy", "smug"]); T(s, "age24", dy=0.3, wf=0.5)
s = crane("The world names", "NW", (0.1, 1.2, -1.8), 8.6, 22, 2, 34, 6); ft(s, "newsN", ["shouting", "happy"]); act(s, 0.0, "newsN", pose=dict(armR=-150)); act(s, 0.2, "plutoN", shake=0.4); T(s, "named"); snap(s, rel(s, "Pluto"), 14)
# ---- Clyde dies before anyone can visit it. But in 2006, NASA launches New Horizons, and inside a small capsule rides about an ounce of his ashes.
s = S("Clyde dies", "LO", (-0.2, 1.25, -1.8), 6.4, -14, pitch=10, pitchTo=4, zoom=6, _dis=1); hide(s, 0.0, "astroL"); show(s, 0.0, "clydeO", pos("LO", -0.6, 0.04, -1.6), hop=0); ft(s, "clydeO", ["neutral", "happy"]); T(s, "before")
s = crane("But in 2006", "LC", (0.0, 1.6, -2.4), 10.0, -22, -2, 30, 6); ft(s, "engL", ["happy", "smug"]); T(s, "y2006", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("NASA launches", "LC", (0.9, 2.2, -3.2), 6.6, 10, pitch=8, pitchTo=14, zoom=8); act(s, 0.0, "rocketL", face="fire", shake=0.4); go(s, 0.2, "rocketL", pos("LC", 0.9, 0.55, -3.2), 1.4, walk=False); T(s, "nh"); snap(s, rel(s, "New"), 14)
s = crane("and inside a", "CR", (0.2, 1.2, -1.9), 9.0, 22, 2, 34, 6); ft(s, "engC", ["happy", "smug"]); act(s, 0.1, "capC", shake=0.3); T(s, "capsule")
s = S("rides about an", "CR", (-0.7, 0.95, -1.5), 4.4, -10, pitch=4, zoom=6, dof=dict(focus="capC", blur=0.4)); ft(s, "engC", ["happy", "neutral"]); act(s, 0.1, "capC", shake=0.2); T(s, "ashes"); snap(s, rel(s, "ashes"), 12)
# ---- July 2015. The spacecraft sweeps within 7,800 miles of Pluto. Clyde finally arrives.
s = crane("July 2015", "SP", (-0.6, 1.3, -3.2), 10.0, -16, -2, 20, 5); act(s, 0.1, "plutoS", shake=0.2); T(s, "y2015", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("The spacecraft sweeps", "SP", (0.6, 1.55, -2.0), 3.2, 12, pitch=4, yawTo=0, type="macro", dof=dict(focus="probeS", blur=0.5), _dis=1); hide(s, 0.0, "plutoS"); act(s, 0.1, "probeS", shake=0.3); snap(s, 0.5, 12)
s = S("within", "SP", (0.0, 2.0, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="MILES OF PLUTO", items=["7,800"]))
s = S("Clyde finally", "SP", (-0.6, 1.3, -3.2), 9.6, 8, pitch=6, zoom=8, yawTo=-2, _dis=1); show(s, 0.0, "plutoS", pos("SP", -1.6, 0.4, -4.0), hop=0); show(s, 0.05, "clydeS", pos("SP", 0.0, 0.3, -2.4)); ft(s, "clydeS", ["happy", "smug"]); act(s, 0.2, "plutoS", face="shocked"); T(s, "arrives"); cfx(s, 0.4, "blush", "clydeS", 0.8); snap(s, rel(s, "arrives"), 12)
# ---- There's just one problem. Seven months after launch, astronomers voted Pluto out of the planets.
s = crane("There's just", "VT", (0.4, 1.3, -2.0), 10.4, 18, 2, 28, 6); ft(s, "v1", ["smug", "neutral"]); ft(s, "v2", ["neutral", "smug"]); act(s, 0.1, "plutoV", shake=0.2); T(s, "problem")
s = S("Seven months after", "VT", (-0.55, 1.25, -1.9), 6.6, -10, pitch=6, zoom=6, yawTo=-2); ft(s, "v1", ["smug", "sneaky"]); ft(s, "v2", ["sneaky", "smug"]); T(s, "months7")
s = S("astronomers voted", "VT", (1.9, 1.75, -2.4), 3.6, 10, pitch=4, zoom=12, dof=dict(focus="plutoV", blur=0.4)); act(s, 0.1, "plutoV", face="shocked", shake=0.4); act(s, 0.7, "plutoV", face="sad"); T(s, "votedout"); snap(s, rel(s, "voted"), 14)
# ---- His ashes left Earth for a planet and arrived at a dwarf. On paper, he lost his planet. In space, he finally reached it.
s = S("His ashes left", "SP", (0.6, 1.55, -2.0), 3.4, -10, pitch=4, yawTo=2, type="macro", dof=dict(focus="probeS", blur=0.5)); hide(s, 0.0, "clydeS"); hide(s, 0.0, "plutoS"); act(s, 0.0, "plutoS", face="default"); T(s, "leftearth")
s = S("and arrived at", "SP", (-1.6, 1.4, -4.0), 6.0, 8, pitch=5, zoom=12, yawTo=0, _dis=1); show(s, 0.0, "plutoS", pos("SP", -1.6, 0.4, -4.0), hop=0); act(s, 0.1, "plutoS", face="sad", shake=0.3); T(s, "dwarf", dy=0.32, wf=0.5); snap(s, rel(s, "dwarf"), 14)
s = crane("On paper", "TX", (0.3, 1.0, -2.1), 5.2, -20, -2, 44, 10); act(s, 0.1, "tbookT", shake=0.2); T(s, "onpaper")
s = S("In space he", "SP", (-0.6, 1.3, -3.2), 9.6, -10, pitch=6, zoom=8, yawTo=2); show(s, 0.0, "clydeS", pos("SP", 0.0, 0.3, -2.4), hop=0); act(s, 0.0, "plutoS", face="default"); ft(s, "clydeS", ["happy", "smug"]); T(s, "inspace"); snap(s, rel(s, "reached"), 12)
# ---- Because a farm boy found a planet. (pull-out onto the hook frame)
s = S("Because a farm", "FM", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "clydeF", ["shocked", "happy", "shocked"])
act(s, 0.0, "scopeF", shake=0.4); act(s, 0.0, "clydeF", pose=dict(armR=-150)); tag(s, 0.05, "farmboy", 0.3, 0.0, wf=0.62, hf=0.22)

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
ATM = dict(FM=dict(bokeh=BK(0.35)), HL=dict(dust=D_(40)), WB=dict(dust=D_(24), rays=dict(angle=30, intensity=0.55)), AT=dict(bokeh=BK(0.35)),
           MB=dict(dust=D_(18), rays=dict(angle=20, intensity=0.6)), LO=dict(dust=D_(16), rays=dict(angle=24, intensity=0.45)), PX=dict(bokeh=BK(0.4)), BC=dict(bokeh=BK(0.35)),
           NW=dict(dust=D_(22), rays=dict(angle=34, intensity=0.55)), LC=dict(dust=D_(18), rays=dict(angle=40, intensity=0.5)), CR=dict(dust=D_(12)), SP=dict(bokeh=BK(0.4)),
           VT=dict(bokeh=BK(0.35)), TX=dict(dust=D_(24), rays=dict(angle=30, intensity=0.55)))
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
MOOD = dict(FM="night", HL="storm", WB="lantern", AT="attic", MB="sunset", LO="dusk", PX="cosmic", BC="safe", NW="news", LC="launch", CR="clean", SP="icy", VT="hall", TX="study")
light, cur = [{"t": 0, "mood": "night"}], "night"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 16,
    "moods": {"night": {"sun": {"azimuth": 150, "elevation": 35, "color": "#c8d4ff", "intensity": 2.60}, "sky": {"top": "#2a3c8c", "horizon": "#6a7cc0"}, "fill": {"sky": "#b0c0ff", "ground": "#504a40", "intensity": 1.95}}, "storm": {"sun": {"azimuth": -30, "elevation": 30, "color": "#e6f0e0", "intensity": 2.30}, "sky": {"top": "#6a7a70", "horizon": "#a6b4a2"}, "fill": {"sky": "#d0e0d0", "ground": "#505a40", "intensity": 1.60}}, "lantern": {"sun": {"azimuth": 40, "elevation": 35, "color": "#ffc080", "intensity": 2.50}, "sky": {"top": "#8a5a3a", "horizon": "#c08a5a"}, "fill": {"sky": "#ffd0a0", "ground": "#604030", "intensity": 1.70}}, "attic": {"sun": {"azimuth": 120, "elevation": 35, "color": "#c0c8ff", "intensity": 2.50}, "sky": {"top": "#4a3a6a", "horizon": "#8a6a9a"}, "fill": {"sky": "#e0c0ff", "ground": "#504040", "intensity": 1.85}}, "sunset": {"sun": {"azimuth": 200, "elevation": 15, "color": "#ffb890", "intensity": 2.40}, "sky": {"top": "#f08cb0", "horizon": "#ffd28a"}, "fill": {"sky": "#ffc8c0", "ground": "#706050", "intensity": 1.50}}, "dusk": {"sun": {"azimuth": -40, "elevation": 20, "color": "#ffc8a0", "intensity": 2.40}, "sky": {"top": "#6a50aa", "horizon": "#ffaa6e"}, "fill": {"sky": "#d0c0ff", "ground": "#604040", "intensity": 1.60}}, "cosmic": {"sun": {"azimuth": 30, "elevation": 30, "color": "#d0fff0", "intensity": 2.50}, "sky": {"top": "#0a3a44", "horizon": "#2a8a8a"}, "fill": {"sky": "#a0fff0", "ground": "#205050", "intensity": 1.90}}, "safe": {"sun": {"azimuth": 0, "elevation": 40, "color": "#ffa090", "intensity": 2.50}, "sky": {"top": "#6a2020", "horizon": "#b05040"}, "fill": {"sky": "#ffb0a0", "ground": "#503030", "intensity": 1.85}}, "news": {"sun": {"azimuth": 50, "elevation": 45, "color": "#fff0c8", "intensity": 2.50}, "sky": {"top": "#ffe0a0", "horizon": "#fff0d0"}, "fill": {"sky": "#fff0d0", "ground": "#806040", "intensity": 1.35}}, "launch": {"sun": {"azimuth": 30, "elevation": 60, "color": "#ffffff", "intensity": 2.50}, "sky": {"top": "#3c8ce6", "horizon": "#bee2ff"}, "fill": {"sky": "#e0f0ff", "ground": "#707060", "intensity": 1.35}}, "clean": {"sun": {"azimuth": 0, "elevation": 60, "color": "#f8ffff", "intensity": 2.30}, "sky": {"top": "#e2f0f4", "horizon": "#d2e8ec"}, "fill": {"sky": "#ffffff", "ground": "#80a0a0", "intensity": 1.40}}, "icy": {"sun": {"azimuth": 60, "elevation": 25, "color": "#fff4e0", "intensity": 2.60}, "sky": {"top": "#2a3070", "horizon": "#8a84c0"}, "fill": {"sky": "#c8c8ff", "ground": "#606070", "intensity": 1.90}}, "hall": {"sun": {"azimuth": 0, "elevation": 45, "color": "#f0f0ff", "intensity": 2.50}, "sky": {"top": "#2a3c90", "horizon": "#6a82d2"}, "fill": {"sky": "#c0d0ff", "ground": "#404870", "intensity": 1.80}}, "study": {"sun": {"azimuth": 50, "elevation": 40, "color": "#fff4e0", "intensity": 2.40}, "sky": {"top": "#faecce", "horizon": "#f6e2be"}, "fill": {"sky": "#fff0d8", "ground": "#806048", "intensity": 1.35}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ffcf3c", "paper": ["#e8d6a8", "#d4bc86"], "dofPx": 8, "particle": "#fff0c0", "bokehColor": "#b0c8ff", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(hook="A farm", planet="planet", tele="with a telescope", flew="Eightyfive years", kansas="Kansas", hail="hailstorm", tomb="the Tombaugh", clyde22="Clyde twentytwo",
           y28="So in 1928", builds="he builds his", parts="The parts", crank="The crankshaft", buick="Buick", pieces="and pieces of", sketch="He sketches", mails="and mails the",
           lowell="to Lowell Observatory", advice="He wants advice", send="They send back", yousee="You see Lowell", mystery="a mystery world", gave="They gave the",
           tedious="the most tedious", flip="Flip between", taken="taken days apart", find="and find the", moves="moves", among="Among countless", feb="February 18th",
           finds="He finds it", heis="He is", world="The world names", pluto1="Pluto", dies="Clyde dies", b2006="But in 2006", nasa="NASA launches", inside="and inside a",
           rides="rides about an", july="July 2015", sweeps="The spacecraft sweeps", arrives="Clyde finally", problem="There's just", seven="Seven months after",
           voted="astronomers voted", left="His ashes left", dwarf="and arrived at", onpaper="On paper", inspace="In space he", because="Because a farm")
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
