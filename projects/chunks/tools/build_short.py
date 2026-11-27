#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 35: five dollars, split two ways, became a 326 million dollar ice cream company.
usage: build_short.py <project folder>
Eight Vermont dairy-pop sets 70 units apart: HK sky-blue cow-spot dairy hills (hook + loop: the pint with a face on a cow-spot pedestal and
the torn $5 bill; the StopperText counter rolls $5 -> $326,000,000), KD peach-lilac playground, PS butter mail room, BK mint vault, GS
orange-teal 1978 roadside gas station, UN navy-gold corporate skyline, NS lavender senses world, TX cocoa fudge macro world. Shots 0.7-2 s,
every neighbour a different move. Open loop: WHAT MADE IT? -> it's the chunks (a man with no sense of smell sold texture)."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, KD=70, PS=140, BK=210, GS=280, UN=350, NS=420, TX=490)
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


yard("HK", "dairy.png", "grassfl.jpg"); box("HK", 0.0, 0.04, -2.8, [1.3, 0.4, 1.0], color="#f8f8f8"); box("HK", 2.7, 0.04, -2.8, [1.0, 0.3, 0.8], color="#ff8ab0"); tree("HK", -3.8, -4.4, 0.9, "#6ab060")
yard("KD", "playground.png", "rubberfl.jpg"); tree("KD", 3.6, -4.2, 0.8, "#8ac890")
yard("PS", "mailroom.png", "butterfl.jpg"); box("PS", 0.0, 0.04, -2.8, [1.3, 0.3, 0.9], color="#b07a40"); box("PS", 2.9, 0.04, -2.8, [1.1, 0.3, 0.8], color="#b07a40")
yard("BK", "vault.png", "vaultfl.jpg")
yard("GS", "road78.png", "dustfl.jpg"); tree("GS", -4.2, -4.2, 0.9, "#5a9070")
yard("UN", "corp.png", "navyfl.jpg"); box("UN", 0.0, 0.04, -2.8, [1.9, 0.36, 0.8], color="#3a4a8a")
yard("NS", "senses.png", "lavfl.jpg"); box("NS", 0.0, 0.04, -2.8, [1.0, 0.3, 0.8], color="#a08ad0"); box("NS", 2.5, 0.04, -2.8, [1.0, 0.3, 0.8], color="#a08ad0"); box("NS", 5.0, 0.04, -2.8, [1.1, 0.3, 0.8], color="#a08ad0")
yard("TX", "fudge.png", "cocoafl.jpg")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("pintH", "pint", pos("HK", 0.0, 0.44, -2.8), 1.35); put("billH", "bill", pos("HK", 2.7, 0.34, -2.8), 0.55)
human("ben", "ben", pos("KD", -0.5, 0.04, -2.4), face="happy", h=1.55); human("jerry", "jerry", pos("KD", 0.5, 0.04, -2.4), face="happy", h=1.5)
put("courseP", "course", pos("PS", 0.0, 0.34, -2.8), 1.2); put("billP", "bill", pos("PS", 2.9, 0.34, -2.8), 0.55)
put("stacksB", "stacks", pos("BK", 0.0, 0.04, -2.8), 1.25)
put("stationG", "station", pos("GS", 0.0, 0.04, -3.2), 1.9); human("benG", "ben", pos("GS", 2.5, 0.04, -2.4), face="happy", h=1.55)
put("checkU", "check", pos("UN", 0.0, 0.4, -2.8), 0.85); put("scaleU", "scale", pos("UN", 3.6, 0.04, -2.8), 1.4)
human("benN", "ben", pos("NS", -2.6, 0.04, -2.4), face="happy", h=1.55); put("noseN", "nose", pos("NS", 0.0, 0.34, -2.8), 1.0); put("tongueN", "tongue", pos("NS", 2.5, 0.34, -2.8), 1.0); put("blurN", "blur", pos("NS", 5.0, 0.34, -2.8), 1.15)
put("spoonT", "spoon", pos("TX", 0.0, 0.04, -2.8), 1.6); put("chunksT", "chunks", pos("TX", 3.0, 0.04, -2.8), 1.0)
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


HOOK = dict(anchor=(0.0, 1.15, -2.8), dist=5.8, yaw=10, pitch=6)
def STOP(s, face, at=0.0, k=None, shake=None):                 # StopperText: one counter card, re-placed in every hook shot (no re-pop), escalates by face
    cid = T(s, "stop", at=at, dy=0.31, wf=0.62, hf=0.24); act(s, at, cid, face=face)
    if k: act(s, at, cid, pop=k)
    if shake: act(s, at, cid, shake=shake)
    return cid
# ---- Five dollars, split two ways, became a 326 million dollar ice cream company.
s = S("0", "HK", zoom=10, **HOOK); c = STOP(s, "default", 0.0, k=1.3, shake=0.2); act(s, 0.0, "pintH", face="shocked", shake=0.3)
for k_, t_ in enumerate((0.25, 0.45, 0.65, 0.85, 1.05, 1.25)): act(s, t_, c, face="r%d" % (k_ + 1))
s = S("became a 326", "HK", (2.7, 0.65, -2.8), 3.6, 14, pitch=6, yawTo=0, type="macro", dof=dict(focus="billH", blur=0.5)); c = STOP(s, "r6"); act(s, 0.1, c, face="r7"); act(s, rel(s, "326"), c, face="r8", pop=1.25, shake=0.3)
act(s, 0.2, "billH", face="split", shake=0.5); snap(s, rel(s, "326"), 9)
s = crane("dollar ice cream", "HK", (0.0, 1.05, -2.8), 5.6, -24, -4, 36, 8); c = STOP(s, "r8"); act(s, 0.15, c, face="esc", pop=1.3, shake=0.3); act(s, rel(s, "company"), "pintH", face="wink", shake=0.4)
s = crane("Ben Cohen and", "KD", (0.0, 0.95, -2.5), 6.0, 22, 2, 34, 8); c = STOP(s, "esc"); act(s, 0.6, c, face="wait", pop=1.3, shake=0.4); ft(s, "ben", ["happy", "shocked"]); ft(s, "jerry", ["shocked", "happy"])
s = S("are childhood friends", "KD", (0.0, 1.0, -2.4), 4.6, -8, pitch=6, zoom=12); STOP(s, "wait"); ft(s, "ben", ["smug", "happy"]); ft(s, "jerry", ["happy", "smug"])
s = S("They decide to", "HK", (0.0, 1.1, -2.8), 4.2, 12, pitch=14, pitchTo=3, dof=dict(focus="pintH", blur=0.4)); act(s, rel(s, "ice"), "pintH", face="default", shake=0.5); T(s, "friends", at=0.05, dy=0.37, wf=0.6)
# ---- Their training? A five-dollar correspondence course from Penn State. They split the cost.
s = crane("Their training", "PS", (0.0, 0.9, -2.8), 5.6, -22, 4, 34, 8); act(s, rel(s, "training"), "courseP", shake=0.4); cfx(s, rel(s, "training"), "question", "courseP", 0.6)
s = S("correspondence course", "PS", (0.0, 1.0, -2.8), 3.8, 10, pitch=6, yawTo=-4, type="macro", dof=dict(focus="courseP", blur=0.5)); act(s, rel(s, "Penn"), "courseP", shake=0.5); snap(s, rel(s, "Penn"), 8)
s = S("They split the", "PS", (2.9, 0.6, -2.8), 3.6, -6, pitch=5, zoom=-10, dof=dict(focus="billP", blur=0.4)); act(s, rel(s, "split"), "billP", face="split", shake=0.6); T(s, "splitc", at=rel(s, "split"), dy=0.37, wf=0.62)
# ---- Then they scrape together twelve thousand dollars. Four thousand each, four thousand from a bank.
s = crane("Then they scrape", "BK", (0.0, 0.9, -2.8), 6.4, 22, -2, 40, 8); T(s, "k12", at=rel(s, "twelve"), dy=0.37, wf=0.56); act(s, rel(s, "twelve"), "stacksB", shake=0.4)
s = S("Four thousand each", "BK", (0.0, 0.8, -2.8), 5.0, -10, pitch=6, zoom=11); act(s, rel(s, "bank"), "stacksB", shake=0.5); snap(s, rel(s, "bank"), 8)
# ---- May 5th, 1978. Burlington, Vermont. Their first shop opens inside a run-down gas station.
s = crane("May 5th", "GS", (0.0, 1.1, -3.2), 7.2, -22, 2, 36, 8); T(s, "y1978", at=rel(s, "1978"), dx=-0.24, dy=0.25, wf=0.26, hf=0.26)
s = S("Burlington Vermont", "GS", (0.0, 1.0, -3.2), 6.6, 8, pitch=6, zoom=3, pan=(14, 0)); T(s, "burl", at=0.05, dy=0.37, wf=0.6)
s = S("Their first shop", "GS", (0.0, 1.0, -3.2), 6.4, -6, pitch=6, zoom=12); act(s, rel(s, "opens"), "stationG", shake=0.4); ft(s, "benG", ["happy", "smug"])
s = S("rundown gas station", "GS", (0.0, 1.05, -3.2), 6.0, 10, pitch=6, zoom=-8, type="macro", dof=dict(focus="stationG", blur=0.4)); hide(s, 0.0, "benG"); act(s, 0.1, "stationG", shake=0.5); T(s, "rundown", at=0.1, dy=0.38, wf=0.64); snap(s, rel(s, "gas"), 8)
# ---- Twenty-two years later, Unilever buys the company for 326 million dollars.
s = crane("Twentytwo years later", "UN", (0.0, 0.9, -2.8), 5.8, 22, 4, 40, 8); T(s, "y22", at=0.05, dy=0.37, wf=0.54); act(s, rel(s, "Unilever"), "checkU", shake=0.5)
s = S("for 326", "UN", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="326 MILLION", items=["DOLLARS"]))
# ---- But the strangest part isn't the money. It's the chunks.
s = S("But the strangest", "UN", (0.0, 0.75, -2.8), 3.8, -10, pitch=14, pitchTo=3, dof=dict(focus="checkU", blur=0.4)); T(s, "notmoney", at=rel(s, "isn't"), dy=0.38, wf=0.56); act(s, rel(s, "money"), "checkU", shake=0.4)
s = S("It's the chunks", "TX", (3.0, 0.55, -2.8), 4.2, 12, pitch=6, yawTo=-2, type="macro", dof=dict(focus="chunksT", blur=0.5)); act(s, rel(s, "chunks"), "chunksT", shake=0.7); snap(s, rel(s, "chunks"), 10)
# ---- You see, Ben Cohen has anosmia. He has no sense of smell, and very little sense of taste. Regular ice cream flavors blur together for him.
s = S("Ben Cohen has", "NS", (-2.6, 1.15, -2.4), 4.4, -8, pitch=6, zoom=12, dof=dict(focus="benN", blur=0.4)); ft(s, "benN", ["happy", "shocked"]); T(s, "anos", at=rel(s, "anosmia"), dy=0.38, wf=0.56)
s = S("He has no", "NS", (0.0, 0.85, -2.8), 3.8, 12, pitch=6, zoom=-9, type="macro", dof=dict(focus="noseN", blur=0.5)); act(s, rel(s, "smell"), "noseN", shake=0.5); T(s, "nosmell", at=rel(s, "smell"), dy=0.38, wf=0.62)
s = S("and very little", "NS", (2.5, 0.85, -2.8), 4.0, -4, pitch=-2, pitchTo=10); act(s, rel(s, "taste"), "tongueN", shake=0.5); T(s, "notaste", at=rel(s, "taste"), dy=0.38, wf=0.62)
s = S("Regular ice cream", "NS", (5.0, 0.9, -2.8), 4.2, 8, pitch=6, zoom=-10, pan=(-6, 0), dof=dict(focus="blurN", blur=0.4)); act(s, rel(s, "blur"), "blurN", shake=0.6); T(s, "blurc", at=rel(s, "blur"), dy=0.38, wf=0.64); cfx(s, rel(s, "blur"), "question", "blurN", 0.7)
# ---- So he judged ice cream by the one thing he could always feel. Texture. Big, heavy chunks, packed in so every spoonful has something to bite.
s = crane("So he judged", "TX", (0.0, 1.0, -2.8), 5.8, -22, 2, 40, 8); act(s, rel(s, "feel"), "spoonT", shake=0.3)
s = S("feel Texture", "TX", (0.0, 1.15, -2.8), 4.0, 6, pitch=6, zoom=12, type="macro", dof=dict(focus="spoonT", blur=0.5)); act(s, rel(s, "Texture"), "spoonT", shake=0.6); T(s, "texture", at=rel(s, "Texture"), dy=0.38, wf=0.56); snap(s, rel(s, "Texture"), 9)
s = crane("Big heavy chunks", "TX", (3.0, 0.6, -2.8), 4.8, 24, 4, 50, 14); act(s, rel(s, "heavy"), "chunksT", hop=0.25, shake=0.4)
s = S("every spoonful", "TX", (0.0, 0.9, -2.8), 4.6, -6, pitch=6, zoom=10, pan=(-6, 0)); T(s, "bite", at=rel(s, "bite"), dy=0.38, wf=0.6); act(s, rel(s, "bite"), "spoonT", shake=0.4)
# ---- Most companies sold flavor. Ben was selling the one thing he could actually feel. In his words: ice cream, to me, is about texture.
s = S("Most companies sold", "UN", (3.6, 0.9, -2.8), 4.4, 12, pitch=14, pitchTo=3, dof=dict(focus="scaleU", blur=0.4)); T(s, "flavorc", at=rel(s, "flavor"), dy=0.38, wf=0.58); act(s, rel(s, "flavor"), "scaleU", shake=0.4)
s = S("Ben was selling", "GS", (2.5, 1.0, -2.4), 4.0, -14, pitch=6, zoom=11); show(s, 0.0, "benG", pos("GS", 2.5, 0.04, -2.4), hop=0); ft(s, "benG", ["smug", "happy"]); act(s, rel(s, "feel"), "stationG", shake=0.3)
s = S("In his words", "NS", (-2.6, 1.15, -2.4), 4.6, 10, pitch=6, zoom=-9, pan=(6, 0), dof=dict(focus="benN", blur=0.4)); ft(s, "benN", ["smug", "happy"]); T(s, "quote", at=rel(s, "ice"), dy=0.38, wf=0.66)
s = S("is about texture", "TX", (0.0, 1.1, -2.8), 4.6, -10, pitch=6, zoom=12); act(s, rel(s, "texture"), "spoonT", shake=0.5)
# ---- So America's most famous chunky ice cream was shaped by a man who can barely taste it. And it all started with five dollars, split two ways.
s = crane("So America's most", "HK", (0.0, 1.1, -2.8), 6.2, 24, 4, 36, 8); act(s, rel(s, "famous"), "pintH", face="crown", shake=0.5); T(s, "famous", at=rel(s, "famous"), dy=0.38, wf=0.66); snap(s, rel(s, "chunky"), 8)
s = S("was shaped by", "NS", (-2.6, 1.15, -2.4), 4.2, -6, pitch=14, pitchTo=3, dof=dict(focus="benN", blur=0.4)); ft(s, "benN", ["happy", "smug"]); T(s, "barely", at=rel(s, "barely"), dy=0.38, wf=0.62)
s = S("And it all", "PS", (2.9, 0.6, -2.8), 3.6, 10, pitch=6, yawTo=-2); act(s, 0.0, "billP", face="default"); act(s, rel(s, "started"), "billP", shake=0.4)
s = S("dollars#4", "HK", zoom=-5, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.0, "pintH", face="default"); act(s, rel(s, "split"), "pintH", face="shocked", shake=0.3); STOP(s, "default", 0.05, k=1)
for s in shots: s.setdefault("frameY", 0.0)

starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots): s["_dur"] = (starts[k + 1] if k + 1 < len(shots) else DURATION) - starts[k]; s["start"] = round(starts[k], 3)
for k, s in enumerate(shots[:-1]):                          # same set: the camera flies (dolly glide) into the next shot; new set: dissolve
    if LOC[id(s)] == LOC[id(shots[k + 1])] and s.get("type") != "cutaway" and shots[k + 1].get("type") != "cutaway" and not shots[k + 1].get("_dis") and math.dist(s["anchor"], shots[k + 1]["anchor"]) < 1.2: s["out"] = "glide"; s["outDur"] = 0.5   # far jumps dissolve: no half-seen props mid-glide
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
ATM = dict(HK=dict(dust=D_(20), rays=dict(angle=26, intensity=0.6)), KD=dict(dust=D_(20), rays=dict(angle=30, intensity=0.6)), PS=dict(dust=D_(24), rays=dict(angle=20, intensity=0.6)), BK=dict(dust=D_(18), rays=dict(angle=24, intensity=0.5)),
           GS=dict(dust=D_(30), rays=dict(angle=14, intensity=0.8)), UN=dict(bokeh=BK(0.5)), NS=dict(bokeh=BK(0.45)), TX=dict(dust=D_(24), rays=dict(angle=22, intensity=0.6)))
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
MOOD = dict(HK="dairy", KD="play", PS="butter", BK="vault", GS="road78", UN="corp", NS="senses", TX="fudge")
light, cur = [{"t": 0, "mood": "dairy"}], "dairy"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"dairy": {"sun": {"azimuth": 60, "elevation": 40, "color": "#fffcf2", "intensity": 2.5}, "sky": {"top": "#78befa", "horizon": "#e6f8ff"}, "fill": {"sky": "#f8fcff", "ground": "#6a8a5a", "intensity": 1.6}},
              "play": {"sun": {"azimuth": 120, "elevation": 38, "color": "#fff4ee", "intensity": 2.4}, "sky": {"top": "#c8aafa", "horizon": "#ffdcc8"}, "fill": {"sky": "#fffaf8", "ground": "#8a7080", "intensity": 1.6}},
              "butter": {"sun": {"azimuth": 150, "elevation": 40, "color": "#fff8e6", "intensity": 2.4}, "sky": {"top": "#ffdc78", "horizon": "#fff6d2"}, "fill": {"sky": "#fffcf0", "ground": "#8a7050", "intensity": 1.5}},
              "vault": {"sun": {"azimuth": 100, "elevation": 40, "color": "#f4fff8", "intensity": 2.4}, "sky": {"top": "#96e6c8", "horizon": "#e6fff0"}, "fill": {"sky": "#f8fffc", "ground": "#5a7a70", "intensity": 1.6}},
              "road78": {"sun": {"azimuth": 240, "elevation": 16, "color": "#ffd8a8", "intensity": 2.7}, "sky": {"top": "#3ca0aa", "horizon": "#ffaa5a"}, "fill": {"sky": "#fff2e6", "ground": "#7a6a5a", "intensity": 1.8}},
              "corp": {"sun": {"azimuth": 160, "elevation": 36, "color": "#fff4e0", "intensity": 2.7}, "sky": {"top": "#1e2864", "horizon": "#786ebe"}, "fill": {"sky": "#f4f2ff", "ground": "#3a3a6a", "intensity": 2.4}},
              "senses": {"sun": {"azimuth": 80, "elevation": 40, "color": "#fff8ff", "intensity": 2.4}, "sky": {"top": "#aa96f0", "horizon": "#fadcfa"}, "fill": {"sky": "#fcf8ff", "ground": "#7a6a90", "intensity": 1.7}},
              "fudge": {"sun": {"azimuth": 200, "elevation": 30, "color": "#ffe8d0", "intensity": 2.6}, "sky": {"top": "#6e3c28", "horizon": "#dc9664"}, "fill": {"sky": "#fff4ec", "ground": "#6a4a3a", "intensity": 2.1}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff3d7f", "paper": ["#7cc8f0", "#58aee0"], "dofPx": 8, "particle": "#fff6ee", "bokehColor": "#ffc8dc", "ray": "#fff6e8", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(training="Their training", may5="May 5th", strange="But the strangest", yousee="You see Ben", sojudged="So he judged", soamerica="So America's most",
           split1="split", c326="326", company="company", ben="Ben Cohen", friends="friends", decide="decide", penn="Penn", split2="split#2", twelve="twelve", bank="bank", y1978="1978",
           burl="Burlington", opens="opens", gas="gas", y22="Twentytwo", unilever="Unilever", c326b="326#2", money="money", chunks="chunks", anosmia="anosmia", smell="smell", taste="taste",
           blur="blur", texture="Texture", heavy="heavy", bite="bite", flavor="flavor", feel2="feel#2", words="words", texture2="texture#2", famous="famous", barely="barely", five2="five dollars#2")
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
