#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 25: lightning hit park ranger Roy Sullivan seven times - and skipped him the one time it hit his wife.
usage: build_short.py <project folder>
Ten Blue Ridge storm sets 70 units apart: HK indigo-teal storm peak (hook + loop; a violet "?" silhouette = open loop, resolved as his wife), BR misty
dawn ridges (boot), GT pine park gate (+ hikers), TW sunset lookout peak, RD purple dusk road (truck, storm cloud, flying eyebrows), YD golden backyard
with laundry, ST pine ranger station, LK teal fishing lake, FR emerald fern trail (bear), RB gold-spotlight record stage (tally, book, trophy).
Shots 0.7-2 s, every neighbour a different move; strikes are cartoon bolts, smoke puffs, dizzy Zs only."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, BR=70, GT=140, TW=210, RD=280, YD=350, ST=420, LK=490, FR=560, RB=630)
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


yard("HK", "stormpeak.png", "rock.jpg"); box("HK", -3.0, 0.04, -1.8, [0.8, 0.4, 0.7], color="#4a5a6a")
yard("BR", "dawn.png", "meadow.jpg")
yard("GT", "pines.png", "gravel.jpg")
yard("TW", "sunsetpeak.png", "peak.jpg")
yard("RD", "duskroad.png", "asphalt.jpg")
yard("YD", "yard.png", "grass.jpg")
yard("ST", "cabin.png", "wood.jpg"); table("ST", 0.9, -1.9, 1.2, 0.7, 0.74, "#8a5a3a")
yard("LK", "lake.png", "dockw.jpg")
yard("FR", "ferns.png", "moss2.jpg")
yard("RB", "recstage.png", "stage.jpg"); box("RB", -3.4, 0.04, -2.4, [1.5, 0.56, 0.6], color="#3a3a7a"); box("RB", 0.0, 0.04, -2.4, [1.3, 0.56, 0.7], color="#d6a028")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
human("royH", "roy", pos("HK", -0.25, 0.04, -1.8), face="shocked"); put("boltH", "boltp", pos("HK", 0.6, 0.04, -2.4), 1.6); put("qwife_H", "qwife", pos("HK", 1.0, 0.04, -3.3), 1.0)
put("bootB", "boot", pos("BR", -2.6, 0.04, -2.2), 0.9)
put("gateG", "gate", pos("GT", 0.0, 0.04, -2.6), 1.6)
human("h1G", "hk1", pos("GT", 4.2, 0.04, -2.0), face="happy"); human("h2G", "hk2", pos("GT", 5.2, 0.04, -2.1), face="happy"); human("h3G", "hk3", pos("GT", 6.2, 0.04, -2.0), face="happy")
put("towerT", "tower", pos("TW", 0.0, 0.04, -2.8), 2.4); human("royT", "roy", pos("TW", -1.5, 0.04, -1.9), face="happy")
put("truckR", "truck", pos("RD", 0.0, 0.04, -2.4), 1.0); put("cloudR", "cloud", pos("RD", -0.9, 2.0, -3.0), 0.9); human("royR", "roy", pos("RD", 3.8, 0.04, -1.8), face="confused"); put("browsR", "brows", pos("RD", -4.0, 1.0, -2.4), 0.6)
human("royY", "roy", pos("YD", -0.6, 0.04, -1.8), face="happy"); human("wifeY", "wife", pos("YD", 0.6, 0.04, -1.9), face="happy"); put("laundryY", "laundry", pos("YD", 0.0, 0.04, -3.4), 1.2); put("boltY", "boltp", pos("YD", 0.6, 1.9, -2.0), 1.0)
human("royS", "roy", pos("ST", -0.5, 0.04, -1.8), face="happy"); put("towelS", "towel", pos("ST", 0.9, 0.78, -1.9), 0.6); put("puffS", "puff", pos("ST", -0.5, 1.72, -1.75), 0.42)
human("royL", "roy", pos("LK", -0.6, 0.04, -1.8), face="happy"); put("rodL", "rod", pos("LK", 0.55, 0.04, -2.0), 1.3); put("boltL", "boltp", pos("LK", -0.6, 1.95, -1.85), 0.8)
human("royF", "roy", pos("FR", -0.7, 0.04, -1.8), face="happy"); put("bearF", "bear", pos("FR", 0.8, 0.04, -2.4), 1.5)
put("tallyR", "tally", pos("RB", -3.4, 0.6, -2.4), 0.8); put("bookR", "book", pos("RB", 0.0, 0.6, -2.4), 1.0); put("trophyR", "trophy", pos("RB", 3.2, 0.04, -2.4), 1.3)
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


HOOK = dict(anchor=(0.2, 1.05, -2.3), dist=5.8, yaw=4, pitch=6)
# ---- Lightning never strikes twice. It hit Roy Sullivan seven times, and he survived every single one.
s = S("0", "HK", zoom=10, **HOOK); act(s, 0.0, "royH", face="shocked", pose=dict(armR=-150), shake=0.4); act(s, 0.0, "boltH", shake=0.6); tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24); snap(s, rel(s, "twice"), 10)
s = S("It hit Roy", "RB", (-3.4, 1.0, -2.4), 3.4, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="tallyR", blur=0.5))
for k in range(1, 8): act(s, 0.1 + 0.09 * k, "tallyR", face="t%d" % k, shake=0.2)
T(s, "seven", at=rel(s, "seven"))
s = S("and he survived", "HK", (-0.25, 1.15, -1.8), 4.6, 8, pitch=14, pitchTo=3); hide(s, 0.0, "boltH"); ft(s, "royH", ["happy", "smug"]); act(s, 0.1, "royH", pose=dict(armR=-150)); T(s, "survived")
# ---- Roy was a park ranger in Shenandoah National Park, Virginia. In 1942, lightning hit him at a fire lookout tower and scorched his leg.
s = crane("Roy was a", "BR", (2.6, 1.2, -2.6), 8.0, 22, 2, 36, 8); T(s, "rangerc", at=rel(s, "ranger"))
s = S("in Shenandoah National", "GT", (0.0, 0.85, -2.6), 7.0, 6, pitch=6, zoom=6, dof=dict(focus="gateG", blur=0.4)); act(s, 0.05, "gateG", shake=0.3)
s = crane("In 1942", "TW", (-0.6, 1.3, -2.4), 8.4, -22, -2, 36, 8); ft(s, "royT", ["happy", "smug"]); T(s, "y1942", dy=0.1, dx=0.18, wf=0.28, hf=0.3)
s = S("lightning hit him", "TW", (0.0, 1.25, -2.8), 4.4, 4, pitch=5, zoom=14); act(s, rel(s, "hit"), "towerT", face="zap", shake=0.7); snap(s, rel(s, "hit"), 10)
s = S("and scorched his", "BR", (-2.6, 0.5, -2.2), 2.8, -14, pitch=6, yawTo=6, type="macro", dof=dict(focus="bootB", blur=0.5)); act(s, 0.05, "bootB", shake=0.5)
# ---- Then nothing for 27 years. Until 1969. A bolt came through his truck window, knocked him out cold, and burned off his eyebrows.
s = S("Then nothing for", "RB", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="THEN NOTHING FOR", items=["27 YEARS"]))
s = crane("Until 1969", "RD", (0.0, 1.0, -2.5), 7.6, 22, 2, 36, 8); act(s, 0.2, "cloudR", shake=0.4); T(s, "y1969", dy=0.1, dx=0.18, wf=0.28, hf=0.3)
s = S("A bolt came", "RD", (0.0, 0.6, -2.4), 5.4, -6, pitch=6, zoom=10, type="macro", dof=dict(focus="truckR", blur=0.5)); hide(s, 0.0, "cloudR"); act(s, 0.05, "truckR", face="zap", shake=0.7); snap(s, rel(s, "bolt"), 10)
s = S("knocked him out", "RD", (3.8, 1.15, -1.8), 4.4, 12, pitch=14, pitchTo=3, dof=dict(focus="royR", blur=0.4)); ft(s, "royR", ["confused", "sad"]); T(s, "knocked"); cfx(s, 0.2, "z", "royR", 0.6)
s = S("and burned off", "RD", (-4.0, 1.3, -2.4), 2.6, -16, pitch=6, yawTo=4, type="macro", dof=dict(focus="browsR", blur=0.5)); act(s, 0.05, "browsR", shake=0.6); T(s, "brow", at=rel(s, "eyebrows"))
# ---- 1970: it found him in his own yard and seared his shoulder. 1972: inside a ranger station. His hair caught fire, and he smothered it with wet towels.
s = crane("1970 it found", "YD", (-0.3, 1.0, -2.3), 7.8, -22, -2, 36, 8); hide(s, 0.0, "wifeY"); hide(s, 0.0, "boltY"); hide(s, 0.0, "laundryY"); ft(s, "royY", ["happy", "smug"]); T(s, "y1970", dy=0.1, dx=0.18, wf=0.28, hf=0.3)
s = S("and seared his", "YD", (-0.6, 1.15, -1.8), 4.4, 8, pitch=5, zoom=14, dof=dict(focus="royY", blur=0.4)); ft(s, "royY", ["shocked", "nervous"]); act(s, 0.05, "royY", shake=0.5); T(s, "shoulder", at=rel(s, "shoulder")); snap(s, rel(s, "seared"), 8); cfx(s, 0.3, "sweat", "royY", 0.6)
s = S("1972", "ST", (0.2, 1.1, -1.9), 6.4, -14, pitch=5, yawTo=4); hide(s, 0.0, "puffS"); ft(s, "royS", ["happy", "smug"]); T(s, "y1972", dy=0.1, dx=0.18, wf=0.28, hf=0.3)
s = S("inside a ranger", "ST", (0.2, 1.1, -1.9), 7.0, 6, pitch=5, zoom=-10); ft(s, "royS", ["smug", "happy"]); T(s, "inside", at=0.05)
s = S("His hair caught", "ST", (-0.5, 1.4, -1.8), 4.0, 10, pitch=5, zoom=14, dof=dict(focus="royS", blur=0.4)); show(s, 0.05, "puffS", pos("ST", -0.5, 1.72, -1.75)); ft(s, "royS", ["shocked", "nervous"]); act(s, 0.1, "puffS", shake=0.5); cfx(s, 0.4, "sweat", "royS", 0.4)
s = S("and he smothered", "ST", (0.9, 1.1, -1.9), 2.6, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="towelS", blur=0.5)); hide(s, 0.0, "puffS"); act(s, 0.05, "towelS", shake=0.5); T(s, "towels", at=rel(s, "towels"))
# ---- 1973: he drove away from a storm cloud. It caught him anyway, and his hair burned again.
s = S("1973", "RD", (0.0, 1.1, -2.5), 7.2, 4, pitch=16, pitchTo=4); show(s, 0.3, "cloudR", pos("RD", -0.9, 2.0, -3.0)); act(s, 0.05, "truckR", face="default"); T(s, "y1973", dy=0.1, dx=0.18, wf=0.28, hf=0.3)
s = S("he drove away", "RD", (-0.4, 1.0, -2.5), 7.0, -6, pitch=5, zoom=4, pan=(8, 0)); act(s, 0.0, "truckR", face="flee"); go(s, 0.1, "cloudR", pos("RD", -0.4, 2.0, -3.0), 1.2, walk=False); act(s, 0.3, "cloudR", shake=0.4)
s = S("It caught him", "RD", (-0.4, 2.45, -3.0), 3.6, 14, pitch=5, yawTo=-4, type="macro", dof=dict(focus="cloudR", blur=0.5)); act(s, rel(s, "caught"), "cloudR", face="zap", shake=0.7); T(s, "caught", at=rel(s, "anyway")); snap(s, rel(s, "caught"), 10)
# ---- 1976: his ankle. And in 1977, while he was fishing, a bolt hit the top of his head and burned his chest and stomach. Then, on the way back, he ran into a bear.
s = S("1976 his ankle", "BR", (-2.6, 0.55, -2.2), 3.4, 8, pitch=6, zoom=12, type="macro", dof=dict(focus="bootB", blur=0.5)); act(s, rel(s, "ankle"), "bootB", face="zap", shake=0.6); c_ = T(s, "y1976", dy=0.1, dx=0.18, wf=0.28, hf=0.3); swap(s, c_, rel(s, "ankle"), "ankle")
s = crane("And in 1977", "LK", (0.0, 1.0, -2.0), 7.0, -22, -2, 38, 8); hide(s, 0.0, "boltL"); ft(s, "royL", ["happy", "smug"]); act(s, 0.2, "rodL", shake=0.4); T(s, "y1977", dy=0.1, dx=0.18, wf=0.28, hf=0.3)
s = S("a bolt hit", "LK", (-0.6, 1.5, -1.85), 4.6, 6, pitch=5, zoom=12, dof=dict(focus="royL", blur=0.4)); hide(s, 0.0, "rodL"); show(s, rel(s, "bolt"), "boltL", pos("LK", -0.6, 1.95, -1.85)); ft(s, "royL", ["shocked", "nervous"]); act(s, rel(s, "hit"), "royL", shake=0.6); snap(s, rel(s, "hit"), 8)
s = S("and burned his", "RB", (-3.4, 1.0, -2.4), 3.4, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="tallyR", blur=0.5)); act(s, 0.0, "tallyR", face="t6"); act(s, 0.4, "tallyR", face="t7", shake=0.6)
s = S("Then on the", "FR", (0.0, 1.05, -2.1), 6.6, -8, pitch=5, zoom=-10); hide(s, 0.0, "bearF"); go(s, 0.0, "royF", pos("FR", -0.4, 0.04, -1.8), 0.9); show(s, rel(s, "bear"), "bearF", pos("FR", 0.8, 0.04, -2.4)); ft(s, "royF", ["happy", "shocked"]); T(s, "bearc", at=rel(s, "bear") - 0.3)
# ---- You see, most people never get struck even once. But lightning hits whoever is outside when the storm arrives, and Roy's whole job was to be outside...
s = S("You see most", "GT", (5.2, 1.0, -2.05), 8.0, 6, pitch=5, zoom=4)
for k, w_ in enumerate(("h1G", "h2G", "h3G")): act(s, 0.2 + 0.15 * k, w_, pose=dict(armR=-150), shake=0.3); ft(s, w_, ["happy", "smug"])
T(s, "once", at=rel(s, "never"))
s = S("But lightning hits", "HK", (0.6, 1.0, -2.4), 4.2, -6, pitch=2, pitchTo=12); hide(s, 0.0, "royH"); show(s, 0.0, "boltH", pos("HK", 0.6, 0.04, -2.4), hop=0); act(s, 0.1, "boltH", shake=0.7); snap(s, rel(s, "hits"), 10)
s = crane("is outside when", "GT", (5.2, 1.0, -2.05), 8.2, 22, 2, 36, 8); ft(s, "h2G", ["shocked", "nervous"]); T(s, "outside", at=0.1)
s = S("and Roy's whole", "TW", (-1.5, 1.15, -1.9), 4.6, 14, pitch=5, yawTo=-4, dof=dict(focus="royT", blur=0.4)); hide(s, 0.0, "towerT"); ft(s, "royT", ["smug", "happy"]); act(s, 0.1, "royT", pose=dict(armR=-150)); T(s, "job", at=rel(s, "job"))
s = S("in the mountains", "BR", (3.0, 1.2, -2.6), 7.6, -4, pitch=5, zoom=4, pan=(-8, 0)); T(s, "decades", at=rel(s, "decades"))
# ---- Guinness World Records verified all seven strikes. Nobody on record has survived more.
s = S("Guinness World Records", "RB", (0.0, 1.1, -2.4), 3.4, 4, pitch=6, zoom=14, type="macro", dof=dict(focus="bookR", blur=0.5)); act(s, 0.05, "bookR", shake=0.4)
s = S("verified all seven", "RB", (0.0, 1.1, -2.4), 3.6, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="bookR", blur=0.5)); act(s, rel(s, "verified"), "bookR", face="stamp", shake=0.7); snap(s, rel(s, "all"), 8)
s = S("Nobody on record", "RB", (3.2, 0.9, -2.4), 4.2, 10, pitch=14, pitchTo=3, dof=dict(focus="trophyR", blur=0.4)); act(s, 0.05, "trophyR", shake=0.5); T(s, "nobody")
# ---- But here's the strangest part. The one time lightning hit his family, Roy was standing right beside his wife, helping her hang laundry. It hit her. And it skipped the one man it never seemed to miss.
s = crane("But here's the", "YD", (0.0, 1.1, -2.5), 7.8, 22, 2, 38, 8); hide(s, 0.0, "royY"); show(s, 0.0, "laundryY", pos("YD", 0.0, 0.04, -3.4), hop=0); T(s, "strange", at=0.05)
s = S("The one time", "YD", (0.0, 1.2, -2.6), 6.4, -6, pitch=5, zoom=12); act(s, 0.1, "laundryY", shake=0.3)
s = S("Roy was standing", "YD", (0.0, 1.05, -2.2), 6.6, 10, pitch=5, zoom=-10); show(s, 0.0, "royY", pos("YD", -0.6, 0.04, -1.8), hop=0); show(s, 0.05, "wifeY", pos("YD", 0.6, 0.04, -1.9)); ft(s, "royY", ["happy", "smug"]); ft(s, "wifeY", ["happy", "smug"]); cfx(s, 0.5, "blush", "wifeY", 0.6)
s = S("helping her hang", "YD", (0.0, 0.8, -3.4), 6.0, -14, pitch=6, yawTo=4, dof=dict(focus="laundryY", blur=0.4)); hide(s, 0.0, "royY"); hide(s, 0.0, "wifeY"); act(s, 0.05, "laundryY", shake=0.4)
s = S("It hit her", "YD", (0.6, 1.4, -1.95), 4.6, 4, pitch=5, zoom=14, dof=dict(focus="wifeY", blur=0.4)); hide(s, 0.0, "laundryY"); show(s, 0.0, "wifeY", pos("YD", 0.6, 0.04, -1.9), hop=0); show(s, 0.05, "boltY", pos("YD", 0.6, 1.9, -2.0)); ft(s, "wifeY", ["shocked", "nervous"]); act(s, 0.1, "wifeY", shake=0.6); T(s, "hither", at=0.05); snap(s, rel(s, "hit"), 10)
s = S("skipped the one", "YD", (-0.6, 1.15, -1.8), 4.4, -12, pitch=5, yawTo=4, dof=dict(focus="royY", blur=0.4)); hide(s, 0.0, "boltY"); hide(s, 0.0, "wifeY"); show(s, 0.0, "royY", pos("YD", -0.6, 0.04, -1.8), hop=0); ft(s, "royY", ["shocked", "confused"]); T(s, "skipped", at=0.05)
s = S("seemed to miss", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "royH", pos("HK", -0.25, 0.04, -1.8), hop=0); act(s, 0.05, "royH", face="shocked", pose=dict(armR=-150)); act(s, 0.1, "boltH", shake=0.5)
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
ATM = dict(HK=dict(bokeh=BK(0.5)), BR=dict(dust=D_(24), rays=dict(angle=26, intensity=0.6)), GT=dict(dust=D_(22), rays=dict(angle=30, intensity=0.5)), TW=dict(dust=D_(20), rays=dict(angle=22, intensity=0.6)),
           RD=dict(bokeh=BK(0.45)), YD=dict(dust=D_(24), rays=dict(angle=28, intensity=0.6)), ST=dict(dust=D_(26)), LK=dict(bokeh=BK(0.45)), FR=dict(dust=D_(30), rays=dict(angle=18, intensity=0.7)),
           RB=dict(bokeh=BK(0.5)))
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
MOOD = dict(HK="stormteal", BR="ridgedawn", GT="pinegate", TW="sunsetpk", RD="duskroad", YD="goldyard", ST="cabin", LK="lakedusk", FR="fern", RB="recgold")
light, cur = [{"t": 0, "mood": "stormteal"}], "stormteal"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"stormteal": {"sun": {"azimuth": 20, "elevation": 42, "color": "#f0f4ff", "intensity": 2.7}, "sky": {"top": "#1e2250", "horizon": "#28788c"}, "fill": {"sky": "#e8f0ff", "ground": "#304a50", "intensity": 2.2}},
              "ridgedawn": {"sun": {"azimuth": 220, "elevation": 22, "color": "#ffe8c8", "intensity": 2.4}, "sky": {"top": "#96b4dc", "horizon": "#ffd2aa"}, "fill": {"sky": "#fff4ec", "ground": "#5a7050", "intensity": 1.5}},
              "pinegate": {"sun": {"azimuth": 40, "elevation": 44, "color": "#fffbe8", "intensity": 2.3}, "sky": {"top": "#5aaae6", "horizon": "#d2f0e6"}, "fill": {"sky": "#f4fff8", "ground": "#5a7a50", "intensity": 1.4}},
              "sunsetpk": {"sun": {"azimuth": 230, "elevation": 16, "color": "#ffc8a0", "intensity": 2.5}, "sky": {"top": "#f06e78", "horizon": "#ffc878"}, "fill": {"sky": "#ffece0", "ground": "#6a4a50", "intensity": 1.8}},
              "duskroad": {"sun": {"azimuth": 220, "elevation": 18, "color": "#ffc8b0", "intensity": 2.5}, "sky": {"top": "#5a3c8c", "horizon": "#ff8c6e"}, "fill": {"sky": "#ffe8f0", "ground": "#4a3a50", "intensity": 2.0}},
              "goldyard": {"sun": {"azimuth": 210, "elevation": 26, "color": "#ffe8b0", "intensity": 2.4}, "sky": {"top": "#78bef0", "horizon": "#ffdc96"}, "fill": {"sky": "#fff8e8", "ground": "#5a7a40", "intensity": 1.5}},
              "cabin": {"sun": {"azimuth": 150, "elevation": 34, "color": "#ffe0b8", "intensity": 2.5}, "sky": {"top": "#aa7850", "horizon": "#c89664"}, "fill": {"sky": "#fff0e0", "ground": "#6a4a30", "intensity": 1.7}},
              "lakedusk": {"sun": {"azimuth": 230, "elevation": 18, "color": "#ffd8c0", "intensity": 2.5}, "sky": {"top": "#324682", "horizon": "#f0a08c"}, "fill": {"sky": "#f0f0ff", "ground": "#3a4a5a", "intensity": 2.0}},
              "fern": {"sun": {"azimuth": 30, "elevation": 46, "color": "#f8ffe0", "intensity": 2.5}, "sky": {"top": "#286e46", "horizon": "#96d282"}, "fill": {"sky": "#f0fff0", "ground": "#3a5a3a", "intensity": 1.8}},
              "recgold": {"sun": {"azimuth": 10, "elevation": 40, "color": "#fff0c8", "intensity": 2.7}, "sky": {"top": "#141846", "horizon": "#3c3278"}, "fill": {"sky": "#f0ecff", "ground": "#3a2a5a", "intensity": 2.2}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#fff03c", "paper": ["#7a9ad8", "#5a7abc"], "dofPx": 8, "particle": "#fffbe0", "bokehColor": "#c8d8ff", "ray": "#fff6c8", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(roywas="Roy was a", y1969="Until 1969", y1973="1973 he drove", yousee="You see most", strange="But here's the",
           twice="twice", seven="seven times", hit1="lightning hit him", leg="scorched", bolt69="A bolt came", knocked="knocked", brows="eyebrows", y1970="1970 it found", seared="seared",
           y1972="1972 inside", fire="caught fire", towels="wet towels", drove="drove away", caught="caught him anyway", ankle="ankle", y1977="And in 1977", top="bolt hit the top",
           seven7="burned his chest", bear="a bear", hits="lightning hits", guinness="Guinness", verified="verified", nobody="Nobody", hither="It hit her", skipped="skipped")
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
