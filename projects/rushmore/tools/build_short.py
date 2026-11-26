#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 31: Mount Rushmore's name was a joke.
usage: build_short.py <project folder>
Eight Black Hills sets 70 units apart: HK rose-gold dawn mountain (hook + loop; the "?" speech bubble = open loop, revealed as WHAT'S IT
CALLED?), NY lavender gaslit brownstones, PN mint-pine claims, GR violet-teal granite peak + legends, OF cherry-cream historian office,
ST butter sketch studio, WK cyan-sky worksite, DK apricot-indigo 1941 dusk. Shots 0.7-2 s, every neighbour a different move; the mountain,
peak, maps and props are the stars, people small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, NY=70, PN=140, GR=210, OF=280, ST=350, WK=420, DK=490)
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


yard("HK", "dawn.png", "granfl.jpg"); tree("HK", -3.0, -3.8, 0.8, "#3c7a5a"); tree("HK", 3.2, -4.0, 0.9, "#468a64")
yard("NY", "brownstone.png", "cobble.jpg"); post("NY", 2.4, -3.2, 2.4, "#2a2a3a"); box("NY", -2.6, 0.04, -3.4, [0.8, 0.4, 0.6], color="#8a5a4a")
yard("PN", "pines.png", "needles.jpg"); tree("PN", -3.4, -4.0, 1.0, "#3c8a64"); tree("PN", 3.6, -4.2, 1.1, "#4a9a6e"); cart("PN", 3.0, 0.04, -3.6, 30)
yard("GR", "granite.png", "gravel.jpg"); tree("GR", -4.0, -4.6, 0.9, "#3c7a6a"); box("GR", 4.4, 0.04, -3.6, [0.7, 0.5, 0.7], color="#a8a4b8")
yard("OF", "office.png", "officefl.jpg"); box("OF", 1.4, 0.04, -2.8, [1.4, 0.75, 0.8], color="#8a4a3a")
yard("ST", "studio.png", "studiofl.jpg"); box("ST", 0.75, 0.04, -2.7, [1.4, 0.46, 0.6], color="#b48c5a")
yard("WK", "worksite.png", "rubble.jpg"); crate("WK", -2.4, 0, -3.8); barrel("WK", 2.4, -3.8)
yard("DK", "dusk.png", "duskfl.jpg"); tree("DK", -4.0, -4.2, 0.9, "#4a4a70")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("rushK", "rushmore", pos("HK", 0.0, 0.04, -4.6), 1.6); human("lawK", "rush", pos("HK", -0.7, 0.04, -2.2), face="happy", h=1.3); put("bubbleK", "bubble", pos("HK", 0.0, 1.4, -2.2), 0.5)
put("checkK", "check", pos("HK", -4.4, 0.9, -2.4), 0.7)
human("lawN", "rush", pos("NY", 0.0, 0.04, -2.2), face="happy", h=1.6); put("bubbleN", "bubble", pos("NY", 3.0, 1.0, -2.4), 0.7)
human("lawP", "rush", pos("PN", -0.7, 0.04, -2.2), face="happy", h=1.6); put("claimsP", "claims", pos("PN", 1.0, 0.04, -2.6), 0.8); put("touristsP", "tourists", pos("PN", 6.0, 0.04, -2.6), 0.8); put("mapP", "sdmap", pos("PN", -6.0, 0.4, -2.6), 1.1)
put("peakG", "peak", pos("GR", 0.0, 0.04, -3.6), 1.6); human("lawG", "rush", pos("GR", -1.05, 0.04, -2.2), face="happy", h=1.5); human("guideG", "guide", pos("GR", 1.05, 0.04, -2.2), face="happy", h=1.6)
put("legendsG", "legends", pos("GR", 7.0, 0.04, -2.6), 0.9)
human("doaneO", "doane", pos("OF", -0.6, 0.04, -2.2), face="happy", h=1.6)
human("sculptS", "sculptor", pos("ST", -0.85, 0.04, -2.2), face="happy", h=1.6); put("blueS", "blueprint", pos("ST", 0.75, 0.5, -2.6), 0.75)
put("crewW", "crew", pos("WK", 0.0, 0.6, -3.8), 1.1); human("drill1W", "drill1", pos("WK", -0.6, 0.04, -2.2), face="happy", h=1.6); human("drill2W", "drill2", pos("WK", 0.6, 0.04, -2.2), face="happy", h=1.6)
put("scaleW", "scale", pos("WK", 4.2, 0.04, -2.6), 1.3); put("safetyW", "safety", pos("WK", -4.2, 0.04, -2.6), 1.2)
put("rushD", "rushmore", pos("DK", 0.0, 0.04, -4.4), 1.6); put("restD", "rest", pos("DK", 2.8, 0.04, -2.4), 0.9); put("bagD", "emptybag", pos("DK", -2.8, 0.04, -2.4), 0.8)
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


HOOK = dict(anchor=(0.0, 1.3, -2.6), dist=6.4, yaw=4, pitch=6)
# ---- Mount Rushmore's name was a joke. A New York lawyer asked one question, and a mountain got his name.
s = S("0", "HK", zoom=8, **HOOK); act(s, 0.0, "rushK", face="gasp", shake=0.4); tag(s, 0.0, "hookc", 0.31, 0.0, wf=0.6, hf=0.19); act(s, 0.2, "bubbleK", shake=0.5); ft(s, "lawK", ["shocked", "smug"]); snap(s, rel(s, "joke"), 10)
s = S("A New York", "NY", (0.0, 1.05, -2.2), 4.6, -10, pitch=5, zoom=12, dof=dict(focus="lawN", blur=0.4)); ft(s, "lawN", ["smug", "happy"]); T(s, "nylaw", at=0.05, dy=0.37, wf=0.5)
s = S("asked one question", "NY", (3.0, 1.35, -2.4), 4.0, 12, pitch=5, yawTo=-4, type="macro", dof=dict(focus="bubbleN", blur=0.5)); act(s, rel(s, "question"), "bubbleN", shake=0.6)
s = crane("and a mountain", "HK", (0.0, 1.0, -4.0), 6.8, -22, -2, 36, 8); act(s, 0.0, "rushK", face="default"); act(s, rel(s, "name"), "rushK", shake=0.4)
# ---- 1885. The Black Hills of South Dakota. Charles Rushmore is checking mining claims.
s = crane("1885", "PN", (0.3, 1.0, -2.4), 7.4, 22, 2, 36, 8); T(s, "y1885", at=0.05, dx=-0.24, dy=0.22, wf=0.26, hf=0.26); ft(s, "lawP", ["happy", "smug"])
s = S("The Black Hills", "PN", (-6.0, 0.95, -2.6), 4.6, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="mapP", blur=0.5)); act(s, rel(s, "Dakota"), "mapP", shake=0.5); snap(s, rel(s, "Black"), 8)
s = S("Charles Rushmore is", "PN", (0.15, 1.0, -2.4), 7.4, 8, pitch=5, zoom=8); ft(s, "lawP", ["smug", "happy"]); T(s, "charles", at=0.05, dy=0.37, wf=0.5); act(s, rel(s, "claims"), "claimsP", shake=0.5)
# ---- He points at a granite peak and asks his guide what it's called. The answer, reportedly: it never had a name. We'll call it Rushmore. And it stuck.
s = crane("He points at", "GR", (0.0, 1.2, -2.8), 7.6, 22, 2, 34, 8); act(s, 0.1, "lawG", pose=dict(armR=-150)); ft(s, "lawG", ["happy", "confused"])
s = S("asks his guide", "GR", (1.05, 1.0, -2.2), 4.6, -8, pitch=5, zoom=12, dof=dict(focus="guideG", blur=0.4)); hide(s, 0.0, "peakG"); hide(s, 0.0, "lawG"); ft(s, "guideG", ["confused", "happy"]); cfx(s, 0.2, "question", "guideG", 0.7)
s = S("The answer reportedly", "GR", (0.0, 0.95, -3.6), 5.0, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="peakG", blur=0.5)); show(s, 0.0, "peakG", pos("GR", 0.0, 0.04, -3.6), hop=0); hide(s, 0.0, "guideG"); act(s, 0.05, "peakG", shake=0.4)
s = S("it never had", "GR", (1.05, 1.0, -2.2), 5.0, 6, pitch=14, pitchTo=3); hide(s, 0.0, "peakG"); show(s, 0.0, "guideG", pos("GR", 1.05, 0.04, -2.2), hop=0); ft(s, "guideG", ["smug", "happy"]); T(s, "noname", at=0.05, dy=0.38, wf=0.62)
s = S("We'll call it", "GR", (0.0, 1.0, -3.6), 5.6, 10, pitch=5, zoom=-10); show(s, 0.0, "peakG", pos("GR", 0.0, 0.04, -3.6), hop=0); hide(s, 0.0, "guideG"); act(s, 0.0, "peakG", face="named", shake=0.6); c_ = T(s, "callit", at=0.05, dy=0.36, wf=0.6); swap(s, c_, rel(s, "stuck"), "stuck", dy=0.36, wf=0.5); snap(s, 0.15, 10)
# ---- Almost forty years later, a state historian named Doane Robinson wants tourists. His first idea? Carve Western legends into the rock. Red Cloud. Lewis and Clark. Buffalo Bill.
s = S("Almost forty years", "GR", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="ALMOST", items=["FORTY YEARS LATER"]))
s = crane("a state historian", "OF", (0.0, 1.0, -2.4), 7.0, -22, -2, 34, 8); ft(s, "doaneO", ["happy", "smug"]); T(s, "doanec", at=rel(s, "Doane"), dy=0.36, wf=0.5)
s = S("wants tourists", "PN", (6.0, 0.6, -2.6), 6.0, 6, pitch=8, zoom=4, pan=(-8, 0)); act(s, 0.05, "touristsP", shake=0.5); T(s, "want", at=0.05, dy=0.36, wf=0.56)
s = S("His first idea", "OF", (-0.6, 1.05, -2.2), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="doaneO", blur=0.4)); ft(s, "doaneO", ["smug", "confused"]); cfx(s, 0.2, "glint", "doaneO", 0.5)
s = S("Carve Western legends", "GR", (7.0, 0.75, -2.6), 5.0, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="legendsG", blur=0.4)); act(s, rel(s, "rock"), "legendsG", shake=0.4)
s = S("Red Cloud", "GR", (7.0, 0.7, -2.6), 5.6, 4, pitch=8, zoom=4, pan=(8, 0)); act(s, rel(s, "Clark"), "legendsG", shake=0.3)
s = S("Buffalo Bill", "GR", (7.0, 0.7, -2.6), 4.8, 2, pitch=14, pitchTo=4); act(s, 0.05, "legendsG", shake=0.4)
# ---- You see, the sculptor went bigger. Four presidents, carved down to the waist. More than four hundred workers. Fourteen years. Just under one million dollars.
s = crane("You see the", "ST", (0.0, 1.0, -2.4), 7.0, 22, 2, 34, 8); ft(s, "sculptS", ["smug", "happy"]); T(s, "bigger", at=rel(s, "bigger"), dy=0.35, wf=0.5); snap(s, rel(s, "bigger"), 10)
s = S("Four presidents carved", "ST", (0.75, 0.95, -2.6), 5.2, 6, pitch=14, pitchTo=4, dof=dict(focus="blueS", blur=0.4)); act(s, rel(s, "waist"), "blueS", shake=0.4); T(s, "four", at=0.05, dy=0.38, wf=0.5)
s = crane("More than four", "WK", (0.0, 1.2, -3.2), 8.0, -22, -2, 34, 8); act(s, rel(s, "workers"), "crewW", shake=0.4); T(s, "workers", at=rel(s, "four"), dy=0.36, wf=0.46)
s = S("Fourteen years", "WK", (0.0, 1.0, -2.2), 5.0, -8, pitch=5, zoom=12); hide(s, 0.0, "crewW"); ft(s, "drill1W", ["happy", "smug"]); ft(s, "drill2W", ["smug", "happy"]); T(s, "y14", at=0.05, dx=-0.24, dy=0.24, wf=0.26, hf=0.26)
s = S("Just under one", "WK", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="JUST UNDER", items=["ONE MILLION DOLLARS"]))
# ---- Faces sixty feet tall. And remarkably, nobody died.
s = S("Faces sixty feet", "WK", (4.2, 0.75, -2.6), 4.4, 12, pitch=6, yawTo=-6, type="macro", dof=dict(focus="scaleW", blur=0.5)); act(s, rel(s, "sixty"), "scaleW", shake=0.5); T(s, "sixty", at=rel(s, "sixty"), dy=0.38, wf=0.6); snap(s, rel(s, "sixty"), 8)
s = S("And remarkably nobody", "WK", (-4.2, 0.7, -2.6), 5.0, 8, pitch=5, zoom=-10); act(s, rel(s, "nobody"), "safetyW", shake=0.5); T(s, "nodied", at=rel(s, "died"), dy=0.37, wf=0.5)
# ---- Then in 1941 the sculptor died, the money ran thin, and the work stopped at the heads.
s = crane("Then in 1941", "DK", (0.0, 1.1, -4.0), 7.0, 22, 2, 34, 8); T(s, "y1941", at=rel(s, "1941"), dx=-0.24, dy=0.22, wf=0.26, hf=0.26)
s = S("the sculptor died", "DK", (2.8, 0.5, -2.4), 3.8, -12, pitch=8, yawTo=4, type="macro", dof=dict(focus="restD", blur=0.5))
s = S("the money ran", "DK", (-2.8, 0.45, -2.4), 3.8, 6, pitch=6, zoom=12, dof=dict(focus="bagD", blur=0.5)); act(s, rel(s, "thin"), "bagD", shake=0.4)
s = S("and the work", "HK", (0.0, 1.0, -4.6), 5.6, -6, pitch=5, zoom=-10); hide(s, 0.0, "lawK"); hide(s, 0.0, "bubbleK"); act(s, 0.0, "rushK", face="default"); T(s, "heads", at=rel(s, "stopped"), dy=0.36, wf=0.56)
# ---- The lawyer even gave five thousand dollars toward the carving. So the presidents never got their bodies.
s = S("The lawyer even", "NY", (0.0, 1.05, -2.2), 5.0, 12, pitch=6, yawTo=-4); ft(s, "lawN", ["smug", "happy"])
s = S("five thousand dollars", "HK", (-4.4, 1.15, -2.4), 4.2, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="checkK", blur=0.5)); act(s, 0.05, "checkK", shake=0.5); T(s, "gave", at=0.05, dy=0.38, wf=0.56); snap(s, 0.2, 8)
s = S("So the presidents", "HK", (0.0, 1.0, -4.6), 5.6, 4, pitch=16, pitchTo=4); act(s, 0.0, "rushK", face="plan", shake=0.3)
# ---- But the mountain kept its name, all because one New York lawyer asked one simple question.
s = crane("But the mountain", "HK", (0.0, 1.0, -4.4), 6.6, -22, -2, 36, 8); act(s, 0.0, "rushK", face="default"); T(s, "kept", at=rel(s, "kept"), dy=0.34, wf=0.5)
s = S("all because one", "NY", (0.0, 1.05, -2.2), 4.4, -8, pitch=5, zoom=12, dof=dict(focus="lawN", blur=0.4)); ft(s, "lawN", ["happy", "smug"])
s = S("asked one simple", "NY", (3.0, 1.35, -2.4), 4.0, -12, pitch=5, yawTo=4, type="macro", dof=dict(focus="bubbleN", blur=0.5)); act(s, 0.0, "bubbleN", face="ask", shake=0.6); snap(s, 0.15, 8)
s = S("question#2", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "lawK", pos("HK", -0.7, 0.04, -2.2), hop=0); show(s, 0.0, "bubbleK", pos("HK", 0.0, 1.4, -2.2), hop=0); act(s, 0.05, "rushK", face="gasp", shake=0.4); T(s, "hookc", at=0.05, dy=0.31, wf=0.6, hf=0.19)
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
ATM = dict(HK=dict(dust=D_(22), rays=dict(angle=26, intensity=0.7)), NY=dict(bokeh=BK(0.5)), PN=dict(dust=D_(24), rays=dict(angle=30, intensity=0.6)), GR=dict(dust=D_(22), rays=dict(angle=22, intensity=0.6)),
           OF=dict(dust=D_(24), rays=dict(angle=20, intensity=0.5)), ST=dict(dust=D_(26), rays=dict(angle=28, intensity=0.7)), WK=dict(dust=D_(34), rays=dict(angle=24, intensity=0.6)), DK=dict(bokeh=BK(0.45)))
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
MOOD = dict(HK="dawn", NY="gaslit", PN="pines", GR="granite", OF="office", ST="studio", WK="worksite", DK="dusk41")
light, cur = [{"t": 0, "mood": "dawn"}], "dawn"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"dawn": {"sun": {"azimuth": 60, "elevation": 22, "color": "#ffe0c8", "intensity": 2.6}, "sky": {"top": "#ff968c", "horizon": "#ffdcaa"}, "fill": {"sky": "#fff4ec", "ground": "#6a6a5a", "intensity": 1.8}},
              "gaslit": {"sun": {"azimuth": 210, "elevation": 30, "color": "#ffe4c8", "intensity": 2.6}, "sky": {"top": "#9678c8", "horizon": "#e6bedc"}, "fill": {"sky": "#fbf0ff", "ground": "#6a5a6a", "intensity": 2.1}},
              "pines": {"sun": {"azimuth": 40, "elevation": 42, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#96dcd2", "horizon": "#f0faeb"}, "fill": {"sky": "#f4fff8", "ground": "#5a7a5a", "intensity": 1.6}},
              "granite": {"sun": {"azimuth": 230, "elevation": 22, "color": "#ffe8d0", "intensity": 2.6}, "sky": {"top": "#5a46aa", "horizon": "#5ac8c8"}, "fill": {"sky": "#f4f4ff", "ground": "#5a5a6a", "intensity": 2.0}},
              "office": {"sun": {"azimuth": 150, "elevation": 36, "color": "#fff4ec", "intensity": 2.4}, "sky": {"top": "#c8505a", "horizon": "#fadcc8"}, "fill": {"sky": "#fff4f0", "ground": "#7a4a40", "intensity": 1.9}},
              "studio": {"sun": {"azimuth": 30, "elevation": 50, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#ffe68c", "horizon": "#fff6d2"}, "fill": {"sky": "#fffcf4", "ground": "#8a7a5a", "intensity": 1.5}},
              "worksite": {"sun": {"azimuth": 40, "elevation": 46, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#50bef0", "horizon": "#d2f0ff"}, "fill": {"sky": "#f4faff", "ground": "#7a7470", "intensity": 1.5}},
              "dusk41": {"sun": {"azimuth": 240, "elevation": 16, "color": "#ffd0b0", "intensity": 2.6}, "sky": {"top": "#463c8c", "horizon": "#ffb482"}, "fill": {"sky": "#fff0ec", "ground": "#5a4a6a", "intensity": 2.3}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#8a5cff", "paper": ["#8adcb4", "#78c8a0"], "dofPx": 8, "particle": "#fff4ec", "bokehColor": "#ffd8c0", "ray": "#fff4e0", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(almost="Almost forty", yousee="You see the", then41="Then in 1941", lawyer2="The lawyer even",
           joke="joke", newyork="New York lawyer", question="asked one question", mountain="and a mountain", y1885="1885", hills="Black Hills", charles="Charles", claims="claims",
           points="points", guide="guide", answer="answer", never="never had", callit="call it", stuck="stuck", doane="Doane", tourists="tourists", idea="idea", carve="Carve",
           red="Red Cloud", lewis="Lewis", buffalo="Buffalo", bigger="bigger", four="Four presidents", waist="waist", workers="workers", fourteen="Fourteen", million="million",
           sixty="sixty", died1="nobody died", died2="sculptor died", thin="thin", heads="heads", five="five thousand", bodies="bodies", kept="kept", simple="simple")
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
