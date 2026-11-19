#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 12: GTA Online's loading screen beat Rockstar for 7 years; t0st killed it.
usage: build_short.py <project folder>
Ten sets 70 units apart: AR boss arena (hook + loop), LV lounge, HG hourglass desert, RM t0st's snowy room, CY cyber city inside the
code, FL file archive, CK checking factory, SP sunny finish line, HQ award stage, ST night street.  Every shot moves (crane / orbit /
push-in / pull-out); same-set shots fly (dolly glide), new sets dissolve.  Snap-ins, atmosphere, depth of field, comic fx, a cutaway
bar chart for the fix.  Cards are fitted to the safe box; the frame check prints CUT / SIGNCUT / INSIDE / OVERLAP flags."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(AR=0, LV=70, HG=140, RM=210, CY=280, FL=350, CK=420, SP=490, HQ=560, ST=630)
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


def lamp(loc, x, z, h, col, cap):
    post(loc, x, z, h, col); box(loc, x, h, z, [0.36, 0.36, 0.36], color=cap)


yard("AR", "arena.png", "violet.jpg")
for x, z in ((-3.4, -4.4), (3.6, -4.2)): lamp("AR", x, z, 2.4, "#3a2050", "#ffd890")
box("AR", -2.6, 0.04, -0.4, [0.9, 0.4, 0.7], color="#6a2a8a"); box("AR", 2.5, 0.04, -0.2, [0.7, 0.3, 0.6], color="#8a3a6a")
room("LV", "#c87a48", "lounge.png", "wood.jpg", sidec="#b06a3c")
box("LV", 0.4, 0.06, -3.4, [2.8, 0.55, 0.9], color="#2f7f8f"); box("LV", 0.4, 0.06, -3.9, [2.8, 1.1, 0.3], color="#287080")
box("LV", 1.7, 0.06, -1.5, [0.9, 0.4, 0.6], color="#8a5a3a"); lamp("LV", -3.4, -3.8, 1.7, "#5a3a2a", "#fff0c0")
yard("HG", "desert.png", "sand.jpg")
for x, z, s in ((-3.2, -4.2, 0.8), (3.4, -3.6, 0.7)): tree("HG", x, z, s, "#4aa070")
box("HG", -1.9, 0.04, -1.6, [0.7, 0.35, 0.7], color="#e0a070"); box("HG", 2.2, 0.04, -2.0, [0.5, 0.25, 0.5], color="#f0b8a0")
room("RM", "#262a5c", "winter.png", "navy.jpg", sidec="#20244e")
box("RM", 1.3, 0.06, -3.4, [2.2, 0.75, 0.8], color="#5a4070"); box("RM", 0.85, 0.81, -3.6, [0.75, 0.48, 0.08], color="#30e8d8"); box("RM", 1.75, 0.81, -3.6, [0.75, 0.48, 0.08], color="#ff70c0")
lamp("RM", -3.2, -3.6, 1.6, "#3a3060", "#ff80c8")
yard("CY", "cyber.png", "grid.jpg")
for x, z, h in ((-3.4, -4.0, 2.6), (-1.9, -4.8, 1.8), (2.1, -4.6, 2.2), (3.5, -3.8, 1.4)): lamp("CY", x, z, h, "#1a3a6a", "#80ffe0")
yard("FL", "archive.png", "wood.jpg")
for x, z, s in ((-3.3, -2.2, 0.7), (-2.6, -2.8, 0.6), (3.1, -1.9, 0.6), (3.3, -2.9, 0.7)): crate("FL", x, 0.04, z, s)
lamp("FL", -1.9, -4.6, 2.4, "#4a2a18", "#ffd070")
yard("CK", "factory.png", "steel.jpg")
box("CK", 0, 0.04, -3.6, [6.4, 0.7, 0.9], color="#3c4250"); box("CK", 0, 0.74, -3.6, [6.4, 0.04, 0.8], color="#22262e")
for x in (-2.6, -1.7, -0.8, 0.9, 1.8, 2.7): crate("CK", x, 0.78, -3.6, 0.42)
lamp("CK", -3.6, -2.4, 2.0, "#2e3440", "#ff9040")
yard("SP", "finish.png", "asphalt.jpg")
for x, z in ((-3.3, -3.0), (3.4, -3.4)): post("SP", x, z, 2.2, "#f0f0f0"); box("SP", x + 0.3, 1.8, z, [0.6, 0.4, 0.04], color="#e83050")
yard("HQ", "gala.png", "emer.jpg")
box("HQ", 0, 0.04, -4.2, [3.4, 0.3, 1.2], color="#d8a830"); lamp("HQ", -3.4, -3.4, 2.0, "#c89020", "#fff4c0"); lamp("HQ", 3.4, -3.4, 2.0, "#c89020", "#fff4c0")
yard("ST", "street.png", "asphalt.jpg")
lamp("ST", -3.4, -4.6, 3.0, "#2e3440", "#ffe7a8")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
KP = pos("AR", -0.6, 0.04, -1.4)
human("kid", "kid", KP, face="shocked"); put("boss", "boss", pos("AR", 0.3, 0.04, -4.6), 2.7); human("toastA", "toast", PARK, face="smug")
human("kidL", "kid", pos("LV", -0.5, 0.06, -2.4), face="nervous"); put("wclock", "wclock", pos("LV", -1.6, 2.4, -4.75), 0.85)
put("hglass", "hglass", pos("HG", 0.0, 0.04, -3.2), 2.4)
human("toast", "toast", pos("RM", 0.0, 0.06, -2.5), face="happy")
human("toastC", "toast", pos("CY", 0.0, 0.04, -2.4), face="shocked")
put("jfile", "jfile", pos("FL", 0.8, 0.04, -3.4), 1.9); put("robotF", "robot", pos("FL", -0.9, 0.04, -2.6), 1.4)
put("robotC", "robot", pos("CK", 0.0, 0.04, -2.5), 1.5)
human("toastS", "toast", pos("SP", -0.6, 0.04, -2.1), face="happy"); put("bossS", "boss", pos("SP", 0.75, 0.04, -3.2), 1.7, face="defeated")
human("rep", "rep", pos("HQ", 1.0, 0.04, -2.6), face="happy"); human("toastH", "toast", pos("HQ", -0.9, 0.04, -2.3), face="happy")
human("cop", "cop", pos("ST", -1.0, 0.04, -2.2), face="smug"); put("copcar", "copcar", pos("ST", 1.2, 0.04, -4.2), 1.0)

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


HOOK = dict(anchor=(-0.05, 1.6, -2.7), dist=7.4, yaw=-5, pitch=12)
# ---- 0-3.5 hook: GTA Online's loading screen beat Rockstar for seven years. One player killed it.
s = S("0", "AR", zoom=8, pan=(-3, 0), **HOOK); ft(s, "kid", ["shocked", "shouting", "shocked"]); act(s, 0.0, "kid", pose=dict(armR=-150)); act(s, 0.1, "boss", shake=0.3)
tag(s, 0.0, "gtaon", 0.3, 0.0, wf=0.56, hf=0.2)
s = S("beat Rockstar", "AR", (0.3, 1.5, -4.6), 8.4, 12, pitch=-2, zoom=8, yawTo=0, pitchTo=4, _dis=1); hide(s, 0.0, "kid"); act(s, 0.0, "boss", shake=0.4)
tag(s, 0.05, "yrs7", 0.3, wf=0.52, hf=0.2); snap(s, 0.25, 16)
s = crane("One player", "AR", (-0.05, 1.5, -3.0), 9.0, -22, -6, 32, 12, _dis=1); show(s, 0.0, "toastA", KP, hop=0); s["_tags"].append("toastA")
ft(s, "toastA", ["smug", "shouting", "happy"]); act(s, 0.0, "toastA", pose=dict(armR=-150)); tag(s, 0.05, "oneplayer", 0.3, wf=0.52)
act(s, rel(s, "killed"), "boss", face="defeated", shake=0.4); cfx(s, rel(s, "killed"), "bang", "toastA", 0.7)
# ---- 3.5-6 every time you joined, you waited. Six minutes.
s = crane("Every time you", "LV", (-0.5, 1.5, -2.5), 6.2, 24, -4, 34, 6, fgBlur=dict(side="left", blur=0.8)); ft(s, "kidL", ["nervous", "confused", "nervous"]); cfx(s, rel(s, "waited"), "z", "kidL")
tag(s, 0.05, "everytime", 0.31, wf=0.5)
s = crane("Six minutes", "HG", (0.0, 1.5, -3.2), 8.0, -18, 2, 36, 5); tag(s, 0.05, "min6", 0.33, wf=0.5); snap(s, 0.5, 14)
# ---- 6-12 Early 2021. A programmer who calls himself t0st gets curious. He digs in...
s = crane("Early 2021", "RM", (0.5, 1.7, -3.0), 9.0, 22, 6, 32, 6); tag(s, 0.05, "y2021", 0.25, -0.12, wf=0.3, hf=0.3)
s = S("A programmer", "RM", (0.3, 1.4, -2.7), 5.6, -12, pitch=4, zoom=10, pan=(3, 0)); ft(s, "toast", ["happy", "smug", "happy"]); tag(s, rel(s, "t0st"), "tname", 0.31, wf=0.46)
s = S("gets curious", "RM", (0.0, 1.45, -2.5), 4.4, 16, pitch=6, yawTo=4, dof=dict(focus="toast", blur=0.4)); ft(s, "toast", ["confused", "sneaky", "confused"])
cfx(s, 0.15, "question", "toast"); snap(s, 0.2, 14)
s = crane("He digs in", "CY", (0.0, 1.9, -3.4), 9.4, -24, -4, 38, 6); ft(s, "toastC", ["shocked", "confused"])
s = S("what the game does", "CY", (0.0, 1.5, -2.4), 5.0, 10, pitch=8, zoom=10, pan=(-3, 0)); ft(s, "toastC", ["confused", "shocked", "confused"]); tag(s, 0.05, "waitq", 0.29, wf=0.6, hf=0.26)
# ---- 12-21 You see, at startup the game reads one file... two billion pointless checks
s = crane("You see", "FL", (0.0, 1.6, -3.0), 9.2, 20, 2, 30, 6); act(s, 0.0, "robotF", shake=0.2); tag(s, rel(s, "startup"), "startup", 0.32, wf=0.48)
s = S("reads one file", "FL", (0.8, 1.0, -3.4), 4.6, -10, zoom=10, pan=(3, 0), type="macro", dof=dict(focus="jfile", blur=0.6)); tag(s, 0.05, "onefile", 0.33, wf=0.44, hf=0.15); snap(s, 0.1, 14)
s = S("Ten megabytes", "FL", (0.8, 1.1, -3.4), 5.2, 14, pitch=6, yawTo=-6); tag(s, 0.05, "mb10", 0.32, wf=0.5)
s = S("Nearly sixtythree", "FL", (0.0, 1.8, -3.2), 7.6, -6, pitch=8, zoom=-7, pan=(0, 0)); tag(s, 0.05, "items63", 0.3, wf=0.5); act(s, 0.0, "robotF", shake=0.3)
s = crane("And for every", "CK", (0.0, 1.4, -3.0), 8.0, -20, 4, 34, 6, fgBlur=dict(side="right", blur=0.8)); act(s, 0.0, "robotC", shake=0.2)
s = S("it checks the", "CK", (0.0, 1.25, -2.5), 4.6, 12, pitch=4, zoom=12, pan=(-3, 0)); tag(s, 0.05, "again", 0.32, wf=0.6, hf=0.14); act(s, 0.5, "robotC", face="dizzy", shake=0.3)
s = S("Almost two billion", "CK", (0.0, 1.15, -2.5), 4.0, -12, pitch=3, zoom=10, pan=(3, 0), type="macro", dof=dict(focus="robotC", blur=0.5)); act(s, 0.0, "robotC", face="dizzy", shake=0.5)
tag(s, 0.05, "billion", 0.32, wf=0.52); snap(s, 0.15, 14); cfx(s, 0.4, "sweat", "robotC")
# ---- 21-27 So t0st writes his own small fix. Six minutes become under two. Seventy percent of the wait, gone.
s = S("So t0st writes", "RM", (0.6, 1.5, -2.9), 6.0, -16, pitch=7, yawTo=2); ft(s, "toast", ["happy", "smug", "happy"]); act(s, 0.0, "toast", pose=dict(armR=-120))
tag(s, 0.05, "fix", 0.32, wf=0.5); cfx(s, 0.5, "glint", "toast", 0.7)
s = S("Six minutes become", "RM", (0.6, 2.0, -3.3), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="bars", title="THE WAIT", items=["6 MINUTES", "UNDER 2"]))
s = crane("Seventy percent", "SP", (0.0, 1.4, -2.7), 8.0, 22, 2, 30, 5); ft(s, "toastS", ["happy", "shouting", "happy"]); act(s, 0.0, "toastS", pose=dict(armR=-150, armL=150))
act(s, 0.0, "bossS", shake=0.4); tag(s, 0.05, "gone", 0.3, wf=0.5); snap(s, 0.6, 14)
# ---- 27-31 Rockstar pays him ten thousand dollars and promises to use his fix
s = crane("Rockstar pays", "HQ", (0.05, 1.5, -2.6), 9.0, -20, -2, 32, 6); ft(s, "rep", ["happy", "smug"]); act(s, 0.0, "rep", pose=dict(armR=-120))
s = S("ten thousand dollars", "HQ", (-0.9, 1.45, -2.3), 4.4, 12, pitch=5, zoom=12, pan=(0, 0)); ft(s, "toastH", ["shocked", "happy", "shouting"]); tag(s, 0.05, "cheque", 0.31, wf=0.6, hf=0.2)
cfx(s, 0.5, "blush", "toastH", 0.8); snap(s, 0.15, 14)
s = S("and promises", "HQ", (1.0, 1.45, -2.6), 4.2, 10, pitch=4, yawTo=-4, dof=dict(focus="rep", blur=0.4)); ft(s, "rep", ["smug", "happy", "smug"]); tag(s, 0.05, "promise", 0.32, wf=0.6, hf=0.14)
# ---- 31-end For seven years, the toughest boss in GTA Online was never the cops. It was the loading screen. (pull-out onto the hook frame)
s = crane("For seven years#2", "ST", (0.1, 1.6, -3.2), 10.0, 18, 0, 34, 6); ft(s, "cop", ["smug", "neutral"]); tag(s, 0.05, "yrs7", 0.3, wf=0.5, hf=0.2)
s = S("boss in", "ST", (-1.0, 1.4, -2.2), 3.6, 12, pitch=4, zoom=12, pan=(0, 0)); ft(s, "cop", ["neutral", "confused", "smug"]); tag(s, 0.05, "toughest", 0.31, wf=0.52); snap(s, 0.2, 14)
s = S("was never the", "ST", (0.35, 1.3, -3.2), 9.0, 6, pitch=6, yawTo=-4); ft(s, "cop", ["confused", "nervous"]); tag(s, 0.05, "notcops", 0.31, wf=0.52); cfx(s, 0.3, "z", "cop")
s = S("It was the", "AR", zoom=-5, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); ft(s, "kid", ["shocked", "shouting", "shocked"]); show(s, 0.0, "kid", KP, hop=0)
act(s, 0.0, "boss", face="default", shake=0.4); act(s, 0.0, "kid", pose=dict(armR=-150))
tag(s, 0.05, "gtaon", 0.3, 0.0, wf=0.56, hf=0.2)

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
    if "_ft" in s:
        who, seq = s.pop("_ft"); n = max(1, int((s["_dur"] - 0.3) / 0.55) + 1)
        prev, j = None, 0
        for i in range(n):
            while seq[j % len(seq)] == prev: j += 1
            prev = seq[j % len(seq)]; j += 1; act(s, round(i * 0.55, 3), who, face=prev)
# ---- atmosphere by set: dust + rays by day, bokeh by night / dawn
D_ = lambda c=22: dict(count=c, size=1.0, drift=1.0); BK = lambda a=0.3: dict(count=12, size=1.0, alpha=a)
ATM = dict(AR=dict(bokeh=BK(0.35), rays=dict(angle=30, intensity=0.45)), LV=dict(dust=D_(24), rays=dict(angle=28, intensity=0.55)), HG=dict(dust=D_(20), rays=dict(angle=35, intensity=0.5)),
           RM=dict(bokeh=BK(0.35)), CY=dict(bokeh=BK(0.4)), FL=dict(dust=D_(26), rays=dict(angle=25, intensity=0.45)), CK=dict(dust=D_(18), rays=dict(angle=20, intensity=0.4)),
           SP=dict(dust=D_(16), rays=dict(angle=40, intensity=0.55)), HQ=dict(bokeh=BK(0.35), rays=dict(angle=22, intensity=0.5)), ST=dict(bokeh=BK(0.4)))
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
MOOD = dict(AR="arena", LV="lounge", HG="desert", RM="winter", CY="cyber", FL="archive", CK="factory", SP="noon", HQ="gala", ST="street")
light, cur = [{"t": 0, "mood": "arena"}], "arena"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 12,
    "moods": {"arena": {"sun": {"azimuth": -30, "elevation": 22, "color": "#ffb878", "intensity": 2.3}, "sky": {"top": "#2a1050", "horizon": "#ff9050"}, "fill": {"sky": "#c080ff", "ground": "#4a2050", "intensity": 1.35}}, "lounge": {"sun": {"azimuth": 50, "elevation": 35, "color": "#ffd8a0", "intensity": 2.3}, "sky": {"top": "#e09060", "horizon": "#ffe0b0"}, "fill": {"sky": "#ffd0a0", "ground": "#7a4a30", "intensity": 1.30}}, "desert": {"sun": {"azimuth": -50, "elevation": 26, "color": "#fff0c0", "intensity": 2.4}, "sky": {"top": "#80d8c8", "horizon": "#ffd0a0"}, "fill": {"sky": "#b0f0e0", "ground": "#c08060", "intensity": 1.30}}, "winter": {"sun": {"azimuth": 160, "elevation": 40, "color": "#b8c8ff", "intensity": 2.0}, "sky": {"top": "#0c1030", "horizon": "#303a80"}, "fill": {"sky": "#a0a0ff", "ground": "#503060", "intensity": 1.40}}, "cyber": {"sun": {"azimuth": 0, "elevation": 50, "color": "#b0fff0", "intensity": 1.9}, "sky": {"top": "#040818", "horizon": "#103050"}, "fill": {"sky": "#40e0ff", "ground": "#102040", "intensity": 1.45}}, "archive": {"sun": {"azimuth": 30, "elevation": 45, "color": "#ffd890", "intensity": 2.2}, "sky": {"top": "#5a3018", "horizon": "#e0a060"}, "fill": {"sky": "#ffc080", "ground": "#5a3020", "intensity": 1.30}}, "factory": {"sun": {"azimuth": -20, "elevation": 50, "color": "#f0fff8", "intensity": 2.3}, "sky": {"top": "#2a6070", "horizon": "#a0d0d0"}, "fill": {"sky": "#a0f0f0", "ground": "#405058", "intensity": 1.25}}, "noon": {"sun": {"azimuth": 40, "elevation": 60, "color": "#fffaf0", "intensity": 2.5}, "sky": {"top": "#3a8af0", "horizon": "#d0f0ff"}, "fill": {"sky": "#b0d8ff", "ground": "#508040", "intensity": 1.20}}, "gala": {"sun": {"azimuth": 20, "elevation": 40, "color": "#ffe8a0", "intensity": 2.3}, "sky": {"top": "#0a4030", "horizon": "#40c090"}, "fill": {"sky": "#a0ffd0", "ground": "#503020", "intensity": 1.35}}, "street": {"sun": {"azimuth": 200, "elevation": 58, "color": "#c8d4ff", "intensity": 2.6}, "sky": {"top": "#1a2460", "horizon": "#5a5aa0"}, "fill": {"sky": "#ff90b0", "ground": "#40407a", "intensity": 1.85}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff9a3c", "paper": ["#dcc49a", "#c9a878"], "dofPx": 8, "particle": "#ffe6b0", "bokehColor": "#a0c8ff", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(player="One player", killed="killed", every="Every time you", waited="you waited", six="Six minutes", early="Early 2021", toast="A programmer", curious="gets curious",
           digs="He digs in", wait="what the game does", yousee="You see", file="reads one file", mb="Ten megabytes", items="Nearly sixtythree", every2="And for every",
           checks="it checks the", billion="Almost two billion", fix="So t0st writes", become="Six minutes become", seventy="Seventy percent", gone="gone", pays="Rockstar pays",
           dollars="ten thousand dollars", promises="and promises", seven2="For seven years#2", boss="boss in", cops="was never the", was="It was the", loading2="loading screen#2")
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
