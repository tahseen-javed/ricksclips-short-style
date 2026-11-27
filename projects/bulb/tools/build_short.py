#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 33: the world's oldest light bulb, glowing since 1901.
usage: build_short.py <project folder>
Eight firehouse-nocturne sets 70 units apart: HK midnight-teal Fire Station 6 night (hook + loop: the glowing bulb on a pedestal, the
StopperText neon sign flickers on), OH amber 1890s glassworks, WW olive-khaki war-years sky, TW mint-lilac toy town, WC violet 2013 webcam
room, EL cyan x-ray blueprint (power supply + electrician), CL coral dawn clock, WS lemon-mint watt workshop. Shots 0.7-2 s, every neighbour a
different move; the bulb and props are the stars, people small companions. Open loop: WHAT'S ITS SECRET? -> it barely tries; the machine fails
first, the bulb glows on and the last shot lands on the hook frame."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, OH=70, WW=140, TW=210, WC=280, EL=350, CL=420, WS=490)
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


yard("HK", "night6.png", "nightfl.jpg"); box("HK", 0.0, 0.04, -2.8, [1.1, 0.5, 0.9], color="#c8463c"); tree("HK", -3.6, -4.6, 0.8, "#2f6a5a"); tree("HK", 3.8, -4.4, 0.9, "#36705e")
yard("OH", "glassw.png", "brickfl.jpg"); box("OH", 3.2, 0.04, -3.6, [1.2, 0.8, 0.8], color="#8a4a30")
yard("WW", "warsky.png", "khakifl.jpg"); box("WW", 0.0, 0.04, -2.8, [1.4, 0.3, 1.0], color="#8a8a50"); tree("WW", -3.4, -4.4, 0.8, "#6a7a40")
yard("TW", "town.png", "townfl.jpg"); tree("TW", -3.2, -4.0, 0.8, "#7ac0a0"); tree("TW", 3.4, -4.2, 0.9, "#9ad0b0"); box("TW", 0.0, 0.0, -1.6, [6.0, 0.03, 0.9], color="#f0e8f8")
yard("WC", "room13.png", "violetfl.jpg"); box("WC", 0.0, 0.04, -2.8, [2.0, 0.66, 0.9], color="#5a3a8a")
yard("EL", "xray.png", "bluefl.jpg"); box("EL", 3.0, 0.04, -3.6, [1.0, 0.6, 0.8], color="#2a7a9a")
yard("CL", "dawn.png", "coralfl.jpg"); box("CL", 0.7, 0.04, -2.8, [0.9, 0.4, 0.8], color="#e0806a")
yard("WS", "workshop.png", "lemonfl.jpg"); box("WS", 5.6, 0.04, -2.8, [1.0, 0.4, 0.8], color="#8ab090"); box("WS", -5.4, 0.04, -3.6, [1.0, 0.9, 0.7], color="#c8b070")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("bulbH", "bulb", pos("HK", 0.0, 0.54, -2.8), 1.2); put("fireh", "fireh", pos("HK", -3.7, 0.04, -4.4), 1.8); human("rosa", "rosa", PARK, face="happy", h=1.1)
put("kilnO", "kiln", pos("OH", 0.0, 0.04, -3.0), 1.9)
put("warsW", "wars", pos("WW", 0.0, 0.34, -2.8), 1.5)
put("truckT", "truck", pos("TW", 0.0, 0.04, -2.6), 1.15)
put("camW", "cam", pos("WC", 0.0, 0.7, -2.8), 1.25)
put("psuE", "psu", pos("EL", 0.7, 0.04, -2.8), 1.3); human("dev", "dev", pos("EL", -0.9, 0.04, -2.4), face="happy", h=1.45)
put("clockC", "clock", pos("CL", -0.6, 0.04, -2.8), 1.2); put("bulbC", "bulb", pos("CL", 0.7, 0.44, -2.8), 1.0, face="bright")
put("meterS", "meter", pos("WS", -2.8, 0.04, -2.8), 1.15); put("filS", "fil", pos("WS", 0.0, 0.04, -2.8), 1.45); put("switchS", "switch", pos("WS", 2.8, 0.04, -2.8), 1.45); put("bulbS", "bulb", pos("WS", 5.6, 0.44, -2.8), 1.0, face="sleepy")
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


HOOK = dict(anchor=(0.0, 1.2, -2.8), dist=6.2, yaw=12, pitch=6)
def STOP(s, face, at=0.0, k=None, shake=None):                 # StopperText: one neon sign card, re-placed in every hook shot (no re-pop), escalates by face
    cid = T(s, "stop", at=at, dy=0.31, wf=0.62, hf=0.22); act(s, at, cid, face=face)
    if k: act(s, at, cid, pop=k)
    if shake: act(s, at, cid, shake=shake)
    return cid
# ---- A light bulb has been glowing since 1901. It's still on right now.
s = S("0", "HK", zoom=9, **HOOK); c = STOP(s, "default", 0.0, k=1.25); act(s, 0.0, "bulbH", face="shocked", shake=0.3)
for t_, f_ in ((0.08, "off"), (0.14, "default"), (0.22, "off"), (0.28, "default")): act(s, t_, c, face=f_)
s = S("since 1901", "HK", (0.0, 1.15, -2.8), 4.4, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="bulbH", blur=0.5)); STOP(s, "default"); act(s, rel(s, "1901"), "bulbH", face="default", shake=0.4); snap(s, rel(s, "1901"), 10)
s = S("It's still on", "WC", (0.0, 1.3, -2.8), 4.6, 6, pitch=14, pitchTo=3); c = STOP(s, "default"); act(s, 0.1, c, face="esc", pop=1.3, shake=0.3)
s = crane("Livermore", "HK", (0.0, 1.1, -3.2), 7.4, -24, -4, 38, 8); c = STOP(s, "esc"); act(s, 0.9, c, face="wait", pop=1.3, shake=0.4); show(s, 0.0, "rosa", pos("HK", -0.95, 0.04, -2.3), hop=0); ft(s, "rosa", ["happy", "shocked"])
s = S("Fire Station", "HK", (-3.7, 0.95, -4.4), 7.2, 8, pitch=6, zoom=6); STOP(s, "wait"); hide(s, 0.0, "rosa"); act(s, rel(s, "6"), "fireh", shake=0.4); snap(s, rel(s, "6"), 8)
# ---- A handmade carbon bulb, made in Ohio in the 1890s. It has burned through two world wars and a move across town.
s = crane("A handmade", "OH", (0.0, 0.95, -3.0), 5.6, 22, 4, 34, 8); T(s, "handc", at=rel(s, "handmade"), dy=0.37, wf=0.62)
s = S("Ohio", "OH", (0.2, 1.0, -3.0), 5.9, -10, pitch=5, zoom=-9, pan=(-6, 0), dof=dict(focus="kilnO", blur=0.4)); T(s, "y1890", at=rel(s, "1890s"), dx=-0.24, dy=0.24, wf=0.26, hf=0.26); act(s, rel(s, "1890s"), "kilnO", shake=0.3)
s = S("It has burned", "WW", (0.0, 1.1, -2.8), 5.0, -16, pitch=6, yawTo=10); act(s, rel(s, "wars"), "warsW", shake=0.5); T(s, "warsc", at=rel(s, "two"), dy=0.37, wf=0.52); snap(s, rel(s, "wars"), 9)
s = crane("and a move", "TW", (0.0, 0.6, -2.6), 6.0, -20, 6, 46, 10, pan=(-8, 0)); act(s, 0.1, "truckT", to=pos("TW", 0.5, 0.04, -2.6), over=1.0); T(s, "movec", at=rel(s, "move"), dy=0.36, wf=0.6)
# ---- Then, May 2013. Its live webcam shows darkness. After more than a century, the world's oldest bulb is dead.
s = crane("Then May 2013", "WC", (0.0, 1.1, -2.8), 6.2, 22, 2, 34, 8); T(s, "y2013", at=rel(s, "2013"), dx=-0.24, dy=0.25, wf=0.26, hf=0.26)
s = S("Its live webcam", "WC", (0.0, 1.1, -2.8), 4.4, -8, pitch=5, zoom=12, type="macro", dof=dict(focus="camW", blur=0.5)); act(s, rel(s, "darkness"), "camW", face="dark", shake=0.5); snap(s, rel(s, "darkness"), 9); cfx(s, rel(s, "darkness") + 0.1, "question", "camW", 0.7)
s = S("After more than", "HK", (0.0, 1.1, -3.0), 5.8, 10, pitch=8, zoom=4, pan=(8, 0)); act(s, 0.0, "bulbH", face="dark"); show(s, 0.0, "rosa", pos("HK", -0.95, 0.04, -2.3), hop=0); ft(s, "rosa", ["shocked", "happy"])
s = S("the world's oldest", "HK", (0.0, 1.15, -2.8), 4.0, -4, pitch=14, pitchTo=3, dof=dict(focus="bulbH", blur=0.5)); act(s, 0.0, "bulbH", face="dark"); hide(s, 0.0, "rosa"); T(s, "deadc", at=rel(s, "dead"), dy=0.37, wf=0.62); snap(s, rel(s, "dead"), 10)
# ---- You see, it wasn't. An electrician traced the problem to a faulty power supply. The bulb was fine. About ten hours later, it was glowing again.
s = S("You see it", "HK", (0.0, 1.15, -2.8), 4.6, 14, pitch=5, zoom=-10); act(s, rel(s, "wasn't"), "bulbH", face="wink", shake=0.4); T(s, "wasnt", at=rel(s, "wasn't"), dy=0.37, wf=0.5)
s = crane("An electrician", "EL", (0.0, 1.0, -2.6), 5.8, -22, -2, 34, 8); ft(s, "dev", ["happy", "shocked"]); act(s, rel(s, "traced"), "dev", to=pos("EL", -0.6, 0.04, -2.4), over=0.6, walk=True)
s = S("a faulty power", "EL", (0.7, 0.85, -2.8), 4.0, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="psuE", blur=0.5)); act(s, 0.05, "psuE", face="broken", shake=0.6); T(s, "psuc", at=0.1, dy=0.38, wf=0.56); snap(s, 0.2, 8); cfx(s, 0.3, "bang", "psuE", 0.6)
s = S("The bulb was", "HK", (0.0, 1.15, -2.8), 4.8, -12, pitch=6, zoom=12); act(s, 0.0, "bulbH", face="default", shake=0.3); T(s, "finec", at=rel(s, "fine"), dy=0.37, wf=0.6)
s = S("About ten hours", "CL", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="ABOUT TEN HOURS", items=["LATER"]))
s = S("it was glowing", "CL", (0.05, 0.85, -2.8), 6.3, 8, pitch=-2, pitchTo=10, dof=dict(focus="bulbC", blur=0.4)); act(s, rel(s, "again"), "bulbC", shake=0.5); cfx(s, rel(s, "again"), "glint", "bulbC", 0.6)
# ---- Its secret is that it barely tries. Built for sixty watts, it now gives the light of about four. A thick filament, a dim glow, almost never switched off.
s = crane("Its secret", "WS", (5.6, 0.95, -2.8), 5.0, 22, 4, 34, 8); T(s, "triesc", at=rel(s, "barely"), dy=0.37, wf=0.56); cfx(s, rel(s, "barely"), "z", "bulbS", 0.9)
s = S("Built for sixty", "WS", (-2.8, 0.65, -2.8), 3.9, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="meterS", blur=0.5)); act(s, rel(s, "sixty"), "meterS", shake=0.5); snap(s, rel(s, "sixty"), 8)
s = S("it now gives", "WS", (-2.8, 0.7, -2.8), 4.6, 6, pitch=6, zoom=-9, pan=(6, 0)); act(s, rel(s, "four"), "meterS", face="four", shake=0.5); T(s, "wattc", at=rel(s, "light"), dy=0.37, wf=0.56)
s = S("A thick filament", "WS", (0.0, 0.85, -2.8), 3.9, 10, pitch=6, yawTo=-6, type="macro", dof=dict(focus="filS", blur=0.5)); T(s, "filc", at=rel(s, "thick"), dy=0.38, wf=0.5); act(s, rel(s, "dim"), "filS", shake=0.3)
s = S("almost never switched", "WS", (2.8, 0.85, -2.8), 4.8, -6, pitch=6, zoom=12); T(s, "offc", at=0.1, dy=0.37, wf=0.58); act(s, rel(s, "off"), "switchS", shake=0.5)
# ---- The machine built to keep it alive failed first. The bulb didn't. And tonight, it's still glowing, like it has since 1901.
s = crane("machine built", "EL", (0.3, 0.9, -2.8), 5.8, 20, 2, 32, 8); act(s, 0.0, "psuE", face="broken"); ft(s, "dev", ["shocked", "happy"])
s = S("failed first", "EL", (0.7, 0.85, -2.8), 4.2, -10, pitch=14, pitchTo=4, dof=dict(focus="psuE", blur=0.4)); act(s, 0.05, "psuE", face="broken", shake=0.7); T(s, "failc", at=0.05, dy=0.38, wf=0.62); snap(s, 0.1, 8)
s = S("The bulb didn't", "HK", (0.0, 1.15, -2.8), 4.4, 6, pitch=6, zoom=13); act(s, 0.0, "bulbH", face="bright", shake=0.4); T(s, "didnt", at=0.05, dy=0.37, wf=0.56)
s = crane("And tonight", "HK", (0.0, 1.1, -2.8), 5.2, 24, 6, 40, 8); act(s, 0.0, "bulbH", face="bright"); ft(s, "rosa", ["happy", "shocked"])
s = S("it has since", "HK", zoom=-5, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.0, "bulbH", face="default"); act(s, 0.8, "bulbH", face="shocked", shake=0.3); STOP(s, "default", 0.05, k=1)
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
ATM = dict(HK=dict(bokeh=BK(0.55)), OH=dict(dust=D_(26), rays=dict(angle=24, intensity=0.6)), WW=dict(dust=D_(22), rays=dict(angle=30, intensity=0.6)), TW=dict(dust=D_(20), rays=dict(angle=26, intensity=0.6)),
           WC=dict(bokeh=BK(0.5)), EL=dict(bokeh=BK(0.4)), CL=dict(dust=D_(22), rays=dict(angle=20, intensity=0.8)), WS=dict(dust=D_(22), rays=dict(angle=28, intensity=0.5)))
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
MOOD = dict(HK="nite", OH="glass", WW="khaki", TW="toytown", WC="room", EL="xray", CL="dawn", WS="shop")
light, cur = [{"t": 0, "mood": "nite"}], "nite"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"nite": {"sun": {"azimuth": 210, "elevation": 34, "color": "#ffe6c0", "intensity": 2.7}, "sky": {"top": "#145a6e", "horizon": "#3c9aa0"}, "fill": {"sky": "#eefaff", "ground": "#2a5060", "intensity": 2.3}},
              "glass": {"sun": {"azimuth": 120, "elevation": 30, "color": "#ffd8a0", "intensity": 2.6}, "sky": {"top": "#963c28", "horizon": "#ffb45a"}, "fill": {"sky": "#fff2e6", "ground": "#7a4a3a", "intensity": 2.0}},
              "khaki": {"sun": {"azimuth": 60, "elevation": 38, "color": "#fff6e0", "intensity": 2.4}, "sky": {"top": "#96a06e", "horizon": "#f0dcaa"}, "fill": {"sky": "#fffaf0", "ground": "#7a7050", "intensity": 1.6}},
              "toytown": {"sun": {"azimuth": 40, "elevation": 44, "color": "#fffaf4", "intensity": 2.4}, "sky": {"top": "#c8b4fa", "horizon": "#dcfaeb"}, "fill": {"sky": "#fafaff", "ground": "#7a8a80", "intensity": 1.5}},
              "room": {"sun": {"azimuth": 160, "elevation": 36, "color": "#f4eaff", "intensity": 2.6}, "sky": {"top": "#5a3296", "horizon": "#aa6ed2"}, "fill": {"sky": "#f6f0ff", "ground": "#4a3a6a", "intensity": 2.3}},
              "xray": {"sun": {"azimuth": 140, "elevation": 40, "color": "#eefcff", "intensity": 2.5}, "sky": {"top": "#146e96", "horizon": "#3cbed2"}, "fill": {"sky": "#f0fcff", "ground": "#2a5a70", "intensity": 2.2}},
              "dawn": {"sun": {"azimuth": 200, "elevation": 18, "color": "#ffe0c8", "intensity": 2.6}, "sky": {"top": "#ff8278", "horizon": "#ffdcaa"}, "fill": {"sky": "#fff4f0", "ground": "#8a5a50", "intensity": 1.8}},
              "shop": {"sun": {"azimuth": 70, "elevation": 40, "color": "#fffcec", "intensity": 2.4}, "sky": {"top": "#e6f08c", "horizon": "#b4f0d2"}, "fill": {"sky": "#fbfff4", "ground": "#7a8a6a", "intensity": 1.6}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff8c1a", "paper": ["#5ab4c8", "#3c96aa"], "dofPx": 8, "particle": "#fff2dc", "bokehColor": "#ffc878", "ray": "#fff4dc", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(thenmay="Then May 2013", yousee="You see it", tonight="And tonight",
           y1901="1901", still="still on", liv="Livermore", station="Station", hand="handmade", ohio="Ohio", y1890="1890s", wars="wars", move="move", y2013="2013", dark="darkness",
           dead="dead", wasnt="wasn't", elec="electrician", faulty="faulty", fine="fine", ten="ten hours", again="again", secret="secret", sixty="sixty", four="four", thick="thick",
           never="never switched", machine="machine", failed="failed", didnt="didn't", y1901b="1901#2")
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
