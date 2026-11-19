#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 10: GTA 6 launches Nov 19, first players got it Nov 18.
usage: build_short.py <project folder>
Five sets 70 units apart: NZ Kiwi gamer room at night (hook + loop), ST game store, BB delay billboard in town, LD London
at 11 a.m., NY New York at 6 a.m.  Every shot moves and dissolves (0.4 s) into the next; snap-ins, atmosphere, depth of
field, comic fx, a macro on the game box and a cutaway timeline for the midnight wave.  Cards are fitted to the safe box
(snap peak included); the frame check prints CUT / SIGNCUT / INSIDE flags.  The last shot pulls out onto the hook frame."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(LO=0, WM=70, SH=140, PR=210, NW=280, MO=350, DU=420, ST=490, BR=560, VC=630)
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
def yard(loc, img, w=15):
    plane(loc, img, 0, -0.2, -6.5, w, round(w * 1100 / 2400, 3))


room("LO", "#5a3420", "lords.png", "red.jpg", rep=(5, 5), sidec="#4a2a18")
box("LO", 0.5, 0.06, -2.0, [1.1, 0.85, 0.6], color="#6a3a22"); box("LO", 0.5, 0.91, -2.0, [1.2, 0.05, 0.7], color="#c8a040")
box("LO", -4.0, 0.06, -2.8, [2.4, 0.55, 2.4], color="#b8283a"); box("LO", 4.0, 0.06, -2.8, [2.4, 0.55, 2.4], color="#b8283a")
for x in (-2.6, 2.9): post("LO", x, -3.9, 2.6, "#c8a040"); box("LO", x, 2.6, -3.9, [0.4, 0.4, 0.4], color="#ffe7a8")
yard("WM", "westminster.png")
for x in range(-6, 7): post("WM", x * 0.75, -4.2, 1.0, "#2e3440")
box("WM", 4.6, 0, -4.9, [2.4, 1.5, 0.9], color="#c8323c"); box("WM", 4.6, 1.5, -4.9, [2.4, 0.06, 0.9], color="#f0e0c0"); tree("WM", -5.0, -4.8, 1.0); tree("WM", 3.0, -5.6, 0.9)
yard("SH", "shop.png", 13)
box("SH", -0.55, 0, -4.4, [1.2, 0.9, 0.8], color="#ff50aa"); box("SH", 3.2, 0, -4.2, [0.6, 0.9, 0.6], color="#2a6a5a")
for x in (-2.4, 1.4): post("SH", x, -3.0, 0.9, "#2e3440")
room("PR", "#343a72", "office.png", "wood.jpg", sidec="#2c3266")
box("PR", -2.5, 0.06, -2.4, [1.4, 0.8, 0.8], color="#4a2e24"); post("PR", -2.9, -2.5, 1.35, "#c8a040"); box("PR", -2.9, 1.35, -2.5, [0.35, 0.25, 0.35], color="#ffe7a8")
yard("NW", "kiosk.png", 13)
box("NW", -2.3, 0, -3.3, [0.8, 0.6, 0.6], color="#e8e0c8"); box("NW", -2.3, 0.6, -3.3, [0.7, 0.4, 0.5], color="#d8d0b8"); box("NW", 2.5, 0, -3.7, [0.9, 0.8, 0.7], color="#e8e0c8")
box("NW", 3.4, 0, -2.2, [1.4, 0.45, 0.45], color="#2e6a4e")
yard("MO", "storm.png", 13)
box("MO", 0, 0, -2.6, [1.5, 0.8, 1.1], color="#4a3a5a"); box("MO", 0, 0.8, -2.6, [1.6, 0.05, 1.2], color="#c8a040")
yard("DU", "dundee.png")
crate("DU", -2.7, 0, -3.0, 0.7); crate("DU", -2.1, 0, -3.5, 0.6); post("DU", 1.9, -3.2, 0.7, "#2e3440"); post("DU", 3.1, -3.9, 2.8, "#2e3440"); box("DU", 3.1, 2.8, -3.9, [0.35, 0.35, 0.35], color="#ffe7a8")
room("ST", "#2e6062", "studio.png", "wood.jpg", sidec="#28585a")
box("ST", -3.2, 0.06, -2.4, [1.6, 0.75, 0.8], color="#8a6248"); box("ST", -3.2, 0.81, -2.5, [0.7, 0.6, 0.6], color="#d6ceb4"); box("ST", 3.0, 0.06, -1.9, [0.6, 0.1, 0.6], color="#e8b060")
room("BR", "#46546e", "boardroom.png", "pave.jpg", sidec="#3e4a62")
box("BR", 0.7, 0.06, -2.1, [2.4, 0.72, 1.0], color="#2a2a34")
for x in (0.1, 1.3): box("BR", x, 0.06, -3.0, [0.5, 0.9, 0.5], color="#c04060")
yard("VC", "vicecity.png"); box("VC", 0, 0, -1, [16, 0.04, 12], texture="sand.jpg", repeat=[8, 8])

# ================================================================== CHARACTERS (cards and palms carry "_" in the id: not frame-checked as cast)
human("lord", "lord", pos("LO", -0.6, 0.06, -2.2), face="shouting"); human("minister", "minister", pos("LO", 2.6, 0.06, -3.0), face="nervous")
GL = pos("LO", 0.5, 0.96, -2.0); put("gboxL", "gbox", GL, 0.6)
human("dad", "dad", pos("WM", -0.9, 0, -2.3), face="shouting"); human("mum", "mum", pos("WM", 0.4, 0, -2.6), face="shouting")
put("gboxS", "gbox", PARK, 0.9); GS = pos("SH", -0.55, 0.9, -4.4)
human("maxc", "maxc", pos("PR", 0.4, 0.06, -2.9), face="sneaky")
put("gboxM", "gbox", pos("MO", 0, 0.85, -2.6), 1.3, face="monster")
human("mike", "mike", pos("ST", -0.8, 0.06, -2.3), face="happy"); human("david", "david", pos("ST", 0.9, 0.06, -2.7), face="happy")
human("exec", "exec", pos("BR", -1.5, 0.06, -2.3), face="smug"); put("gboxB", "gbox", pos("BR", 0.9, 0.78, -2.1), 0.6)
put("palm_1", "palm", pos("VC", -2.6, 0.04, -1.4), 3.4); put("palm_2", "palm", pos("VC", 2.8, 0.04, -2.4), 3.8)

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


def ft(s, who, seq): s["_ft"] = (who, seq)
def snap(s, t, z=25): SNAPC.append((s, t, z))
def cfx(s, t, typ, on, dur=0.9): FXC.append((s, t, typ, on, dur))


HOOK = dict(anchor=(-0.13, 1.45, -2.2), dist=6.6, yaw=-8, pitch=5)
# ---- 0-4 hook: a British lord tried to stop GTA / that was exactly the plan
s = S("0", "LO", zoom=10, pan=(-3, 0), **HOOK); ft(s, "lord", ["shouting", "shocked", "shouting"])
act(s, 0.0, "lord", pose=dict(armR=-150)); act(s, 0.1, "lord", shake=0.3); tag(s, 0.0, "stopgta", 0.3, 0.0, wf=0.56, hf=0.22)
s = S("stop Grand Theft Auto", "LO", (0.5, 1.21, -2.0), 1.9, 10, zoom=8, pan=(3, 0), type="macro", dof=dict(focus="gboxL", blur=0.6)); snap(s, 0.06, 18)
s = S("That was exactly", "PR", (0.5, 1.45, -2.9), 4.6, 14, pitch=5, yawTo=-4); ft(s, "maxc", ["sneaky", "smug", "sneaky"])
tag(s, rel(s, "plan"), "plan", 0.3, tilt=-4, wf=0.52)
# ---- 4-11 May 20th 1997, not in shops, the House of Lords, Lord Campbell asks the government
s = crane("May 20th", "WM", (0, 2.4, -4.0), 10.0, 18, 4, 34, 6); tag(s, 0.05, "date", 0.24, 0.0, wf=0.24, hf=0.24)
s = S("The game isn't", "SH", (-0.4, 2.0, -4.0), 8.0, -12, zoom=10, pan=(3, 0), fgBlur=dict(side="left", blur=0.8)); tag(s, rel(s, "shops"), "notyet", 0.28, tilt=4, wf=0.5)
s = crane("But in the House", "LO", (0.8, 1.6, -2.6), 11.0, -22, -6); ft(s, "lord", ["shouting", "confused"]); tag(s, 0.05, "hol", 0.32, wf=0.56, hf=0.13)
s = S("Lord Campbell", "LO", (-0.8, 1.45, -2.2), 4.0, -12, zoom=10, pan=(3, 0), dof=dict(focus="lord", blur=0.4)); ft(s, "lord", ["shouting", "shocked", "shouting"])
act(s, 0.0, "lord", pose=dict(armR=-110)); tag(s, 0.05, "campbell", 0.3, wf=0.5); snap(s, 0.1, 20)
s = S("asking the government", "LO", (2.6, 1.45, -3.0), 5.4, -14, pitch=6, yawTo=-2); ft(s, "minister", ["nervous", "shocked", "nervous"])
tag(s, rel(s, "government"), "govt", 0.3, wf=0.54); cfx(s, 0.3, "question", "minister")
s = S("what it will do", "LO", (0.8, 1.5, -2.6), 11.0, 30, pitch=14, zoom=10, pan=(-3, 0)); ft(s, "minister", ["nervous", "shocked"])
act(s, 0.0, "lord", face="shouting", pose=dict(armR=-100), shake=0.3); cfx(s, 0.15, "sweat", "minister")
# ---- 11-14 newspapers howl, family groups rage, who made this monster?
s = crane("Newspapers howl", "NW", (0, 2.0, -3.6), 8.0, 16, 2, 36, 8); tag(s, 0.05, "howl", 0.14, wf=0.6, hf=0.3); snap(s, 0.35, 15)
s = S("Family groups", "WM", (-0.25, 1.3, -2.45), 6.6, -12, pitch=10, yawTo=6); ft(s, "dad", ["shouting", "shocked", "shouting"])
act(s, 0.0, "mum", face="shouting", pose=dict(armR=-150), shake=0.3); act(s, 0.0, "dad", pose=dict(armL=150)); tag(s, 0.05, "rage", 0.3, wf=0.3, hf=0.22)
s = S("And who made", "MO", (0, 1.5, -2.6), 4.2, 10, pitch=3, zoom=14, yawTo=-4); act(s, 0.0, "gboxM", shake=0.4)
tag(s, rel(s, "monster"), "monster", 0.33, tilt=-5, wf=0.48, hf=0.13); snap(s, rel(s, "monster"), 15); cfx(s, rel(s, "monster"), "bang", "gboxM", 0.7)
# ---- 14-20 Dundee, Lemmings, the publisher nearly cancelled it, BMG
s = crane("A small studio", "DU", (0, 2.3, -4.0), 10.0, -18, -4, 30, 5); tag(s, rel(s, "Dundee"), "dundee", 0.28, wf=0.44)
s = S("The same people", "ST", (0.05, 1.45, -2.5), 7.2, 10, pitch=5, zoom=10, pan=(-3, 0)); ft(s, "mike", ["happy", "smug", "happy"])
act(s, 0.0, "david", face="happy", pose=dict(armR=-150)); tag(s, rel(s, "Lemmings"), "lemm", 0.3, wf=0.5)
s = crane("Its own publisher", "BR", (-0.4, 1.5, -2.3), 9.0, 20, 6, 26, 6); ft(s, "exec", ["smug", "shouting", "smug"])
act(s, 0.0, "exec", pose=dict(armR=-150))
s = S("nearly cancelled", "BR", (0.9, 1.08, -2.1), 2.2, -10, zoom=10, pan=(3, 0), type="macro", dof=dict(focus="gboxB", blur=0.5))
act(s, 0.0, "gboxB", shake=0.4); tag(s, 0.05, "cancel", 0.3, tilt=-6, wf=0.6, hf=0.15); snap(s, 0.1, 15)
s = S("You see", "BR", (-1.5, 1.45, -2.3), 4.2, 14, zoom=10, pan=(-3, 0), dof=dict(focus="exec", blur=0.4)); ft(s, "exec", ["sneaky", "smug", "happy"])
tag(s, rel(s, "BMG"), "bmg", 0.3, wf=0.36); cfx(s, rel(s, "BMG") + 0.2, "glint", "exec", 0.6)
# ---- 20-27 Max Clifford, Mike Dailly's quote, the plan board
s = S("then hired Max", "PR", (0.4, 1.45, -2.9), 4.2, -10, pitch=3, zoom=12, pan=(-3, 0)); ft(s, "maxc", ["happy", "sneaky", "shouting"])
act(s, 0.0, "maxc", pose=dict(armR=-150), shake=0.3); tag(s, rel(s, "Max"), "maxname", 0.3, wf=0.52); snap(s, rel(s, "Max"), 20)
s = S("a famous British", "PR", (0.9, 1.6, -3.0), 5.4, 8, pitch=8, yawTo=22); ft(s, "maxc", ["smug", "sneaky"])
tag(s, 0.05, "publicist", 0.3, wf=0.5); cfx(s, 0.3, "glint", "maxc", 0.7)
s = S("cocreator Mike", "ST", (-0.8, 1.45, -2.3), 4.2, 14, zoom=10, pan=(-3, 0)); ft(s, "mike", ["happy", "shocked", "happy"]); tag(s, 0.05, "mikecard", 0.3, wf=0.5)
s = S("designed all", "ST", (-1.0, 1.5, -2.3), 4.8, 16, pitch=6, yawTo=4); ft(s, "mike", ["shocked", "shouting", "shocked"])
tag(s, 0.05, "quote", 0.27, wf=0.52, hf=0.24); snap(s, 0.1, 18)
s = S("He told the team", "PR", (0.9, 1.6, -3.0), 5.0, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True,
      diagram=dict(kind="org", title="THE PLAN", items=["WHO HE WOULD TARGET", "WHAT THEY WOULD SAY"]))
s = S("and what they", "PR", (1.0, 2.0, -3.3), 6.6, -18, pitch=6, yawTo=-4); ft(s, "maxc", ["shouting", "smug"]); act(s, 0.0, "maxc", pose=dict(armR=-100))
# ---- 27-33 David Jones, every word came true, the scandal was the advert
s = S("Founder David", "ST", (0.9, 1.45, -2.7), 4.4, -10, zoom=10, pan=(3, 0)); ft(s, "david", ["happy", "shocked", "happy"])
tag(s, 0.05, "davidcard", 0.3, wf=0.5); snap(s, 0.1, 18); cfx(s, 0.5, "blush", "david", 0.8)
s = S("every word came", "NW", (0.2, 1.9, -3.4), 6.6, -14, pitch=8, yawTo=2); tag(s, 0.03, "howl", 0.3, -0.12, wf=0.36, hf=0.2)
tag(s, rel(s, "came"), "cametrue", 0.02, wf=0.56, hf=0.13); snap(s, rel(s, "came"), 15)
s = S("The scandal was", "SH", (-0.55, 1.47, -4.4), 2.6, 8, zoom=10, pan=(3, 0), type="macro", dof=dict(focus="gboxS", blur=0.5))
show(s, 0.0, "gboxS", GS, hop=0.2); tag(s, 0.1, "advert", 0.31, wf=0.56, hf=0.14); cfx(s, 0.4, "glint", "gboxS", 0.8)
# ---- 33-41 twenty-nine years later: Vice City, Rockstar's Miami
s = crane("twentynine years", "VC", (0, 2.4, -3.8), 10.0, 20, 4, 32, 6); tag(s, 0.05, "yrs29", 0.25, wf=0.44)
s = S("GTA 6 takes", "VC", (0.2, 2.0, -3.4), 7.0, -14, pitch=4, zoom=12, pan=(3, 0), fgBlur=dict(side="right", blur=0.8)); tag(s, 0.05, "gta6", 0.22, wf=0.46); snap(s, 0.1, 15)
s = S("Rockstar's version", "VC", (0.5, 1.8, -3.0), 6.4, 8, pitch=6, yawTo=24); tag(s, 0.05, "miami", 0.25, wf=0.5)
# ---- 41-end: and it all began because a British lord tried to stop GTA (pull-out lands on the hook frame)
s = crane("And it all began", "LO", (0.8, 1.6, -2.6), 11.0, 24, 6); ft(s, "lord", ["shouting", "shocked"])
s = S("a British lord#2", "LO", (-0.8, 1.4, -2.2), 4.0, -14, pitch=-3, yawTo=-4, pitchTo=6); ft(s, "lord", ["shouting", "shocked"]); act(s, 0.0, "lord", pose=dict(armR=-110))
s = S("stop Grand Theft Auto#2", "LO", zoom=-5, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "lord", ["shocked", "shouting"])
act(s, 0.0, "lord", pose=dict(armR=-150)); tag(s, 0.05, "stopgta", 0.3, 0.0, wf=0.56, hf=0.22)
for s in shots: s.setdefault("frameY", 0.0)

starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots): s["_dur"] = (starts[k + 1] if k + 1 < len(shots) else DURATION) - starts[k]; s["start"] = round(starts[k], 3)
for k, s in enumerate(shots[:-1]):                          # same set: the camera flies (dolly glide) into the next shot; new set: dissolve
    if LOC[id(s)] == LOC[id(shots[k + 1])] and s.get("type") != "cutaway" and shots[k + 1].get("type") != "cutaway": s["out"] = "glide"; s["outDur"] = 0.5
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
    if "_ft" in s:
        who, seq = s.pop("_ft"); n = max(1, int((s["_dur"] - 0.3) / 0.55) + 1)
        prev, j = None, 0
        for i in range(n):
            while seq[j % len(seq)] == prev: j += 1
            prev = seq[j % len(seq)]; j += 1; act(s, round(i * 0.55, 3), who, face=prev)
# ---- atmosphere by set: dust + rays by day, bokeh by night / dawn
D_ = lambda c=22: dict(count=c, size=1.0, drift=1.0); BK = lambda a=0.3: dict(count=12, size=1.0, alpha=a)
ATM = dict(LO=dict(dust=D_(24), rays=dict(angle=28, intensity=0.5)), WM=dict(dust=D_(20), rays=dict(angle=25, intensity=0.55)), SH=dict(bokeh=BK(0.35)),
           PR=dict(bokeh=BK(0.3)), NW=dict(dust=D_(22), rays=dict(angle=35, intensity=0.45)), MO=dict(bokeh=BK(0.35)), DU=dict(dust=D_(16), rays=dict(angle=30, intensity=0.4)),
           ST=dict(dust=D_(24)), BR=dict(rays=dict(angle=20, intensity=0.5), dust=D_(12)), VC=dict(bokeh=BK(0.3), rays=dict(angle=40, intensity=0.5)))
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
    while shot_cuts(k, s) and s["distance"] < d0 * 1.35: s["distance"] = round(s["distance"] * 1.06, 3)
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
MOOD = dict(LO="lords", WM="day", SH="dusk", PR="night", NW="morning", MO="storm", DU="silver", ST="studio", BR="steel", VC="sunset")
light, cur = [{"t": 0, "mood": "lords"}], "lords"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 11,
    "moods": {"lords": {"sun": {"azimuth": 30, "elevation": 50, "color": "#ffd8a0", "intensity": 2.2}, "sky": {"top": "#6a3020", "horizon": "#f0b070"}, "fill": {"sky": "#ffb880", "ground": "#6a2a2a", "intensity": 1.25}}, "day": {"sun": {"azimuth": 40, "elevation": 46, "color": "#ffe8c8", "intensity": 2.4}, "sky": {"top": "#5b8ee0", "horizon": "#f6d6b0"}, "fill": {"sky": "#a0b4ff", "ground": "#6a4b6e", "intensity": 1.2}}, "dusk": {"sun": {"azimuth": -40, "elevation": 18, "color": "#ff9ab0", "intensity": 2.2}, "sky": {"top": "#36286e", "horizon": "#f07890"}, "fill": {"sky": "#c090ff", "ground": "#5a3050", "intensity": 1.35}}, "night": {"sun": {"azimuth": 200, "elevation": 34, "color": "#b8c4ff", "intensity": 2.0}, "sky": {"top": "#141a40", "horizon": "#3a3a7a"}, "fill": {"sky": "#8a90e0", "ground": "#4a3a5a", "intensity": 1.35}}, "morning": {"sun": {"azimuth": 60, "elevation": 30, "color": "#ffd8b0", "intensity": 2.3}, "sky": {"top": "#8aa8e0", "horizon": "#ffd2a8"}, "fill": {"sky": "#b8c4ff", "ground": "#7a6050", "intensity": 1.2}}, "storm": {"sun": {"azimuth": 0, "elevation": 60, "color": "#e0b0ff", "intensity": 2.0}, "sky": {"top": "#180828", "horizon": "#7a2a70"}, "fill": {"sky": "#a060e0", "ground": "#301838", "intensity": 1.4}}, "silver": {"sun": {"azimuth": 120, "elevation": 30, "color": "#fff4e0", "intensity": 2.3}, "sky": {"top": "#6e96d0", "horizon": "#e6e8ee"}, "fill": {"sky": "#b8c8e8", "ground": "#5a6470", "intensity": 1.25}}, "studio": {"sun": {"azimuth": 30, "elevation": 45, "color": "#ffe0b0", "intensity": 2.1}, "sky": {"top": "#2a5050", "horizon": "#80c0a0"}, "fill": {"sky": "#80ffc0", "ground": "#4a3a30", "intensity": 1.35}}, "steel": {"sun": {"azimuth": -20, "elevation": 40, "color": "#e8f2ff", "intensity": 2.4}, "sky": {"top": "#5a8ad0", "horizon": "#e0ecf8"}, "fill": {"sky": "#b0c8ff", "ground": "#4a5468", "intensity": 1.2}}, "sunset": {"sun": {"azimuth": -60, "elevation": 12, "color": "#ff9a70", "intensity": 2.4}, "sky": {"top": "#5a2090", "horizon": "#ffa070"}, "fill": {"sky": "#ff90c8", "ground": "#704060", "intensity": 1.35}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#e0b43a", "paper": ["#dcc49a", "#c9a878"], "dofPx": 8, "particle": "#ffe6b0", "bokehColor": "#ffb0e0", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(plan="That was exactly", date="May 20th", shops="The game isn't", lords="But in the House", campbell="Lord Campbell", govt="government", news="Newspapers howl",
           family="Family groups", monster="And who made", dundee="Dundee", lemm="Lemmings", publisher="Its own publisher", cancel="cancelled", yousee="You see", bmg="BMG",
           max="then hired Max", famous="a famous British", mike="cocreator Mike", designed="designed all", told="He told the team", say="what they would say", founder="Founder David",
           true="came true", scandal="The scandal", advert="advert", years="twentynine years", gta="GTA 6", miami="Miami", began="And it all began", lord2="a British lord#2")
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
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
