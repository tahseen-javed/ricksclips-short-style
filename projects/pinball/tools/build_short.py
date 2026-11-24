#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 22: the bear Teddy Roosevelt refused to shoot became every kid's teddy bear -
a cartoon of a cartoon of the real, old, beaten bear.
usage: build_short.py <project folder>
Thirteen honey-caramel + bayou-moss sets 70 units apart: HK misty gold bayou with the willow (hook + loop; a "?" bear silhouette = open loop,
resolved on the kid's pillow), KB indigo starry bedroom, MS amber hunt camp, CH moss forest, WP ink-blue newsroom, CT cream ink-cartoon world,
BK pink-mint candy shop, WN dusk Brooklyn street, WH sky-blue White House, FC red-yellow toy factory, GE snowy Black Forest, CZ rainbow
1907 craze, PR violet church. Shots 1-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, KB=70, MS=140, CH=210, WP=280, CT=350, BK=420, WN=490, WH=560, FC=630, GE=700, CZ=770, PR=840)
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


yard("HK", "bayou.png", "mud.jpg"); tree("HK", -3.2, -3.6, 1.0, "#6a9a5a"); box("HK", 3.0, 0.04, -1.4, [0.7, 0.4, 0.6], color="#7a6a4a")
yard("KB", "bedroom.png", "rug.jpg"); box("KB", 0.0, 0.04, -2.2, [2.0, 0.46, 1.0], color="#6a5aaa"); box("KB", -3.0, 0.04, -2.8, [0.8, 1.0, 0.6], color="#c87a5a")
yard("MS", "camp.png", "campdirt.jpg"); box("MS", 2.8, 0.04, -2.4, [0.8, 0.5, 0.6], color="#8a6a40"); tree("MS", -3.2, -3.4, 1.0, "#4a7a5a")
yard("CH", "forest.png", "moss.jpg"); tree("CH", -3.0, -3.0, 1.1, "#3a7a4a"); tree("CH", 3.2, -3.4, 1.1, "#3a7a4a")
yard("WP", "newsroom.png", "boardsb.jpg"); table("WP", 0.9, -1.9, 1.2, 0.7, 0.74, "#5a4a3a"); table("WP", -2.6, -2.2, 1.0, 0.7, 0.74, "#5a4a3a")
yard("CT", "inkworld.png", "paperfl.jpg")
yard("BK", "candy.png", "checker.jpg"); table("BK", 1.8, -2.1, 1.2, 0.7, 0.74, "#e87a96")
yard("WN", "street.png", "brickfl.jpg"); post("WN", -2.4, -2.4, 2.4, "#2a2a30"); post("WN", 2.5, -2.4, 2.4, "#2a2a30")
yard("WH", "whitehouse.png", "lawn.jpg"); table("WH", 0.9, -1.9, 1.2, 0.7, 0.74, "#7a4a3a")
yard("FC", "factory.png", "factfl.jpg"); box("FC", 2.8, 0.04, -2.6, [0.9, 0.6, 0.7], color="#f0c040")
yard("GE", "blackforest.png", "snow.jpg"); table("GE", -0.4, -2.0, 1.0, 0.7, 0.74, "#8a5a3a")
yard("CZ", "craze.png", "confl.jpg"); box("CZ", -3.0, 0.04, -1.6, [0.6, 0.5, 0.6], color="#e05a8a"); box("CZ", 3.0, 0.04, -1.6, [0.6, 0.5, 0.6], color="#5aa0e0")
yard("PR", "church.png", "pews.jpg"); box("PR", 0.7, 0.04, -1.95, [0.6, 1.1, 0.5], color="#8a5a3a")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
human("teddyH", "teddyr", pos("HK", -0.9, 0.04, -1.8), face="shocked"); put("willow_H", "willow", pos("HK", 0.8, 0.04, -3.0), 2.4); put("bearH", "realbear", pos("HK", 0.8, 0.04, -2.6), 1.3, face="tied")
put("qbear_H", "qbear", pos("HK", -1.5, 0.04, -3.6), 0.8)
put("pillowK", "pillow", pos("KB", 0.0, 0.5, -2.2), 0.9); human("kidK", "kid", pos("KB", -1.3, 0.04, -1.8), face="happy"); human("kid2K", "kid2", pos("KB", 1.3, 0.04, -1.9), face="happy")
human("teddyM", "teddyr", pos("MS", -0.7, 0.04, -1.7), face="nervous"); human("collierM", "collier", pos("MS", 0.7, 0.04, -1.8), face="smug")
put("houndsC", "hounds", pos("CH", -0.7, 0.04, -2.0), 0.9); put("bearC", "realbear", pos("CH", 1.2, 0.04, -2.6), 1.2, face="shocked")
human("berryW", "berryman", pos("WP", -0.7, 0.04, -1.7), face="happy"); put("penW", "inkpen", pos("WP", 0.9, 0.78, -1.9), 0.6); put("papersW", "papers", pos("WP", -2.6, 0.78, -2.2), 0.7)
put("cartoonT", "cartoon", pos("CT", 0.0, 0.3, -2.6), 1.8)
human("morrisB", "morris", pos("BK", -0.9, 0.04, -1.7), face="happy"); human("roseB", "rose", pos("BK", 0.4, 0.04, -1.9), face="happy"); put("plushB", "plush", pos("BK", 1.8, 0.78, -2.1), 0.6)
put("windowN", "window", pos("WN", 0.0, 0.04, -2.6), 1.8)
human("teddyW", "teddyr", pos("WH", -0.6, 0.04, -1.7), face="happy"); put("letterW", "letter", pos("WH", 0.9, 0.78, -1.9), 0.5)
put("boxesF", "boxes", pos("FC", 0.9, 0.04, -2.4), 1.4); human("morrisF", "morris", pos("FC", -1.2, 0.04, -1.8), face="happy")
put("steiffG", "steiff", pos("GE", -0.4, 0.78, -2.0), 0.7); human("buyerG", "buyer", pos("GE", 0.9, 0.04, -1.8), face="smug"); put("crateG", "crate", pos("GE", 2.2, 0.04, -2.5), 0.8)
human("kidZ", "kid", pos("CZ", -0.9, 0.04, -1.8), face="happy"); human("kid2Z", "kid2", pos("CZ", 0.6, 0.04, -1.9), face="happy"); put("plushZ", "plush", pos("CZ", -0.15, 0.04, -2.3), 0.8)
human("priestP", "priest", pos("PR", -0.6, 0.04, -1.7), face="shouting"); put("plushP", "plush", pos("PR", 0.7, 1.14, -1.95), 0.5)
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


HOOK = dict(anchor=(0.0, 1.3, -2.3), dist=9.0, yaw=4, pitch=6)
# ---- America's most famous hunter refused to shoot a bear. That's why every kid sleeps with one.
s = S("0", "HK", zoom=14, pan=(-3, 0), **HOOK); act(s, 0.0, "teddyH", pose=dict(armR=-150), shake=0.3); act(s, 0.2, "bearH", shake=0.5); tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
s = S("refused to shoot", "HK", (-0.1, 1.1, -2.2), 7.0, -14, pitch=4, yawTo=4); ft(s, "teddyH", ["shocked", "smug"]); act(s, 0.1, "bearH", shake=0.4); snap(s, rel(s, "shoot"), 8)
s = crane("That's why every", "KB", (0.0, 1.0, -2.0), 8.4, 22, 2, 38, 8); ft(s, "kidK", ["happy", "smug"]); ft(s, "kid2K", ["happy", "smug"]); act(s, 0.2, "pillowK", shake=0.4); T(s, "everykid"); cfx(s, 0.4, "blush", "kidK", 0.6)
# ---- November 14th, 1902. Mississippi. President Theodore Roosevelt is on a bear hunt, and it is not going well.
s = crane("November 14th", "MS", (0.0, 1.2, -1.8), 8.6, -22, -2, 36, 6); ft(s, "collierM", ["smug", "happy"]); T(s, "y1902", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("Mississippi President", "MS", (0.0, 1.2, -1.8), 7.0, 16, pitch=5, yawTo=-4); T(s, "missi")
s = S("Theodore Roosevelt is", "MS", (-0.7, 1.25, -1.7), 4.6, 8, pitch=5, zoom=12, dof=dict(focus="teddyM", blur=0.4)); ft(s, "teddyM", ["happy", "smug"]); T(s, "tr"); snap(s, 0.3, 8)
s = S("and it is", "MS", (-0.3, 1.2, -1.75), 5.6, -6, pitch=5, zoom=-10); ft(s, "teddyM", ["nervous", "confused"]); T(s, "notwell"); cfx(s, 0.3, "sweat", "teddyM", 0.6)
# ---- So his guide, Holt Collier, fixes it. His hounds corner an old black bear.
s = crane("So his guide", "MS", (0.4, 1.2, -1.8), 8.0, 20, 0, 34, 6); ft(s, "collierM", ["smug", "happy"]); act(s, 0.1, "collierM", pose=dict(armR=-150)); T(s, "holt")
s = S("His hounds corner", "CH", (0.35, 0.8, -2.2), 8.2, -6, pitch=4, zoom=4, pan=(8, 0)); go(s, 0.05, "houndsC", pos("CH", -0.3, 0.04, -2.0), 1.0, walk=False); act(s, 0.4, "bearC", shake=0.5); T(s, "corner"); snap(s, rel(s, "bear"), 8)
# ---- The hunters club it, tie it to a willow tree, and invite the president to take the shot.
s = crane("The hunters club", "HK", (0.8, 1.0, -2.6), 8.4, 22, 2, 40, 8, _dis=1); hide(s, 0.0, "teddyH"); act(s, 0.1, "bearH", face="shocked", shake=0.6)
s = S("tie it to", "HK", (0.8, 1.3, -2.8), 5.6, -10, pitch=8, pitchTo=2, dof=dict(focus="bearH", blur=0.4)); act(s, 0.05, "bearH", face="tied", shake=0.4); T(s, "tied")
s = S("and invite the", "HK", (0.0, 1.2, -2.2), 8.4, 16, pitch=5, yawTo=-2, _dis=1); show(s, 0.0, "teddyH", pos("HK", -0.9, 0.04, -1.8), hop=0); ft(s, "teddyH", ["nervous", "confused"]); T(s, "shot")
# ---- Roosevelt refuses. He calls it unsportsmanlike.
s = S("Roosevelt refuses", "HK", (-0.9, 1.25, -1.8), 4.6, -8, pitch=5, zoom=14, _dis=1, dof=dict(focus="teddyH", blur=0.4)); hide(s, 0.0, "bearH"); act(s, 0.05, "teddyH", pose=dict(armR=-150), shake=0.4); ft(s, "teddyH", ["shouting", "smug"]); T(s, "refuses"); cfx(s, 0.3, "bang", "teddyH", 0.5); snap(s, 0.3, 8)
s = S("He calls it", "HK", (0.0, 1.2, -2.2), 8.6, 0, pitch=5, zoom=-10, _dis=1); show(s, 0.0, "bearH", pos("HK", 0.8, 0.04, -2.6), hop=0); ft(s, "teddyH", ["smug", "happy"]); act(s, 0.1, "bearH", face="default"); T(s, "unsport")
# ---- Two days later, Washington Post cartoonist Clifford Berryman draws the scene. The president, turning away from a tied-up bear. The cartoon spreads fast.
s = crane("Two days later", "WP", (0.1, 1.2, -1.8), 8.0, -20, 0, 34, 6); ft(s, "berryW", ["happy", "smug"]); T(s, "twodays")
s = S("cartoonist Clifford Berryman", "WP", (-0.75, 1.25, -1.7), 4.4, 14, pitch=5, yawTo=-2); ft(s, "berryW", ["smug", "happy"]); T(s, "berry")
s = S("draws the scene", "WP", (0.9, 1.05, -1.9), 2.6, 6, pitch=6, zoom=12, type="macro", dof=dict(focus="penW", blur=0.5)); act(s, 0.05, "penW", shake=0.5)
s = crane("The president turning", "CT", (0.0, 1.2, -2.6), 10.6, 22, 2, 30, 6); act(s, 0.1, "cartoonT", shake=0.4)
s = S("away from a", "CT", (0.0, 1.2, -2.6), 7.0, -6, pitch=4, zoom=8, dof=dict(focus="cartoonT", blur=0.3)); act(s, 0.05, "cartoonT", shake=0.3)
s = S("The cartoon spreads", "WP", (-2.6, 1.15, -2.2), 3.4, 10, pitch=12, pitchTo=2, type="macro", dof=dict(focus="papersW", blur=0.5)); act(s, 0.05, "papersW", shake=0.5); T(s, "spreads"); snap(s, rel(s, "spreads"), 8)
# ---- In Brooklyn, a candy shop owner named Morris Michtom sees it. His wife Rose sews a little plush bear. They put it in the window with a sign. Teddy's bear.
s = crane("In Brooklyn a", "WN", (0.0, 1.0, -2.6), 8.4, -22, -2, 36, 6); T(s, "brooklyn")
s = S("named Morris Michtom", "BK", (-0.9, 1.25, -1.7), 4.6, 10, pitch=5, zoom=12, _dis=1, dof=dict(focus="morrisB", blur=0.4)); hide(s, 0.0, "roseB"); ft(s, "morrisB", ["happy", "shocked"]); T(s, "morrisc"); snap(s, 0.4, 8)
s = S("His wife Rose", "BK", (0.9, 1.2, -1.95), 5.6, -14, pitch=5, yawTo=4, _dis=1); hide(s, 0.0, "morrisB"); show(s, 0.0, "roseB", pos("BK", 0.4, 0.04, -1.9), hop=0); ft(s, "roseB", ["happy", "smug"]); T(s, "rosec")
s = S("a little plush", "BK", (1.8, 1.05, -2.1), 2.6, 6, pitch=12, pitchTo=2, type="macro", dof=dict(focus="plushB", blur=0.5)); act(s, 0.05, "plushB", shake=0.5); T(s, "plushc"); snap(s, 0.3, 8); cfx(s, 0.3, "blush", "roseB", 0.5)
s = S("They put it", "WN", (0.0, 1.0, -2.6), 8.6, 4, pitch=6, zoom=12); act(s, 0.1, "windowN", shake=0.4)
s = S("with a sign", "WN", (0.0, 0.95, -2.6), 6.4, -10, pitch=4, yawTo=4, dof=dict(focus="windowN", blur=0.4)); act(s, 0.05, "windowN", shake=0.5)
# ---- It sells. Then it sells out. The Michtoms ask the president to use his name. He says yes. They quit candy and start the Ideal Novelty and Toy Company.
s = crane("It sells", "BK", (-0.2, 1.2, -1.8), 8.0, 20, 0, 34, 6, _dis=1); show(s, 0.0, "morrisB", pos("BK", -0.9, 0.04, -1.7), hop=0); ft(s, "morrisB", ["happy", "shouting"]); ft(s, "roseB", ["happy", "smug"]); c_ = T(s, "sells"); swap(s, c_, rel(s, "out"), "soldout"); act(s, rel(s, "out"), "morrisB", pose=dict(armR=-150))
s = S("The Michtoms ask", "BK", (-0.3, 1.2, -1.8), 5.8, -14, pitch=5, yawTo=2); ft(s, "morrisB", ["smug", "happy"]); ft(s, "roseB", ["happy", "smug"]); T(s, "name")
s = S("to use his", "WH", (-0.6, 1.25, -1.7), 4.6, 8, pitch=5, zoom=12, dof=dict(focus="teddyW", blur=0.4)); ft(s, "teddyW", ["happy", "smug"])
s = S("He says yes", "WH", (0.9, 1.0, -1.9), 2.4, -8, pitch=12, pitchTo=2, type="macro", dof=dict(focus="letterW", blur=0.5)); act(s, 0.05, "letterW", shake=0.5); snap(s, rel(s, "yes"), 8)
s = S("They quit candy", "FC", (-0.15, 1.1, -2.0), 8.2, 14, pitch=5, yawTo=-4); ft(s, "morrisF", ["shouting", "happy"]); act(s, 0.05, "morrisF", pose=dict(armR=-150)); T(s, "quit")
s = crane("and start the", "FC", (0.0, 1.0, -2.2), 8.6, -22, -2, 38, 8); act(s, 0.1, "boxesF", shake=0.4); T(s, "ideal")
# ---- Meanwhile in Germany, Steiff shows its own plush bear. One American buyer orders three thousand.
s = crane("Meanwhile in Germany", "GE", (0.9, 1.0, -2.1), 9.4, 22, 2, 36, 6); act(s, 0.1, "steiffG", shake=0.3); T(s, "germany")
s = S("Steiff shows its", "GE", (-0.4, 1.15, -2.0), 2.8, -8, pitch=6, zoom=12, type="macro", dof=dict(focus="steiffG", blur=0.5)); act(s, 0.05, "steiffG", shake=0.5); T(s, "steiffc"); snap(s, 0.3, 8)
s = S("One American buyer", "GE", (1.5, 1.0, -2.1), 5.8, 16, pitch=5, yawTo=-2); ft(s, "buyerG", ["smug", "happy"]); act(s, 0.2, "crateG", shake=0.4); T(s, "buyerc")
s = S("orders three thousand", "GE", (0.0, 1.8, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="PLUSH BEARS ORDERED", items=["3000"]))
# ---- By 1907, it's a craze. A Michigan priest attacks teddy bears from the pulpit. Kids keep hugging them anyway.
s = crane("By 1907", "CZ", (-0.15, 1.0, -2.0), 8.4, -22, -2, 38, 8); ft(s, "kidZ", ["happy", "shocked"]); act(s, 0.1, "plushZ", shake=0.4); c_ = T(s, "y1907", dy=0.2, dx=-0.15, wf=0.32, hf=0.34); swap(s, c_, rel(s, "craze"), "crazec"); snap(s, rel(s, "craze"), 8)
s = S("A Michigan priest", "PR", (0.0, 1.2, -1.8), 6.4, 14, pitch=5, yawTo=-4); ft(s, "priestP", ["shouting", "confused"]); T(s, "priestc")
s = S("attacks teddy bears", "PR", (-0.6, 1.25, -1.7), 4.4, -6, pitch=5, zoom=14, dof=dict(focus="priestP", blur=0.4)); act(s, 0.05, "priestP", pose=dict(armR=-150), shake=0.4); ft(s, "priestP", ["shouting", "confused"]); T(s, "attacks"); cfx(s, 0.3, "bang", "priestP", 0.5); snap(s, rel(s, "attacks"), 8)
s = S("Kids keep hugging", "CZ", (-0.15, 1.0, -2.0), 6.6, 16, pitch=5, yawTo=-2); ft(s, "kidZ", ["happy", "smug"]); ft(s, "kid2Z", ["happy", "smug"]); act(s, 0.1, "plushZ", shake=0.4); T(s, "hugs"); cfx(s, 0.3, "blush", "kid2Z", 0.6)
# ---- You see, Berryman kept drawing that bear for years. And every time, it got smaller. Rounder. Cuter. The real bear was old, heavy, and beaten.
s = crane("You see Berryman", "WP", (0.1, 1.2, -1.8), 8.0, 20, 0, 34, 6); ft(s, "berryW", ["happy", "smug"]); act(s, 0.2, "penW", shake=0.4); T(s, "kept")
s = S("that bear for", "WP", (0.9, 1.05, -1.9), 2.6, -6, pitch=12, pitchTo=2, type="macro", dof=dict(focus="penW", blur=0.5)); act(s, 0.05, "penW", shake=0.5)
s = S("And every time", "CT", (0.0, 1.2, -2.6), 5.6, -16, pitch=5, yawTo=4); act(s, rel(s, "smaller"), "cartoonT", face="c2", shake=0.5); T(s, "smaller", at=rel(s, "smaller"))
s = S("Rounder Cuter", "CT", (0.0, 1.2, -2.6), 7.2, 6, pitch=4, zoom=10); act(s, 0.05, "cartoonT", face="c3", shake=0.5); T(s, "cuter")
s = crane("The real bear", "HK", (0.8, 1.0, -2.6), 7.6, -22, -2, 36, 6, _dis=1); hide(s, 0.0, "teddyH"); act(s, 0.1, "bearH", face="default", shake=0.3); T(s, "realb")
# ---- So the cuddly bear on every kid's pillow is a cartoon of a cartoon of the one bear America's most famous hunter refused to shoot.
s = S("So the cuddly", "KB", (0.0, 1.0, -2.2), 3.4, 8, pitch=10, pitchTo=2, type="macro", dof=dict(focus="pillowK", blur=0.5)); act(s, 0.05, "pillowK", shake=0.4); T(s, "cuddly")
s = S("is a cartoon", "CT", (0.0, 1.2, -2.6), 6.4, 18, pitch=5, yawTo=-2); act(s, 0.05, "cartoonT", face="c3", shake=0.3); act(s, 0.45, "cartoonT", face="c2", shake=0.3); act(s, 0.85, "cartoonT", face="default", shake=0.3); T(s, "cofc")
s = S("America's most famous#2", "HK", (0.8, 1.2, -2.7), 6.4, -6, pitch=5, zoom=12, _dis=1); hide(s, 0.0, "teddyH"); act(s, 0.1, "bearH", face="tied", shake=0.4)
s = S("refused to shoot#2", "HK", zoom=-4, pan=(0, 0), _dis=1, **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "teddyH", pos("HK", -0.9, 0.04, -1.8), hop=0); act(s, 0.0, "teddyH", face="shocked")
act(s, 0.1, "teddyH", pose=dict(armR=-150), shake=0.3); tag(s, 0.05, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
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
ATM = dict(HK=dict(dust=D_(24), rays=dict(angle=30, intensity=0.6)), KB=dict(bokeh=BK(0.45)), MS=dict(dust=D_(26), rays=dict(angle=24, intensity=0.5)), CH=dict(dust=D_(30), rays=dict(angle=18, intensity=0.6)),
           WP=dict(dust=D_(18)), CT=dict(dust=D_(14)), BK=dict(dust=D_(18)), WN=dict(bokeh=BK(0.4)), WH=dict(dust=D_(18), rays=dict(angle=30, intensity=0.5)), FC=dict(dust=D_(30)),
           GE=dict(dust=D_(50)), CZ=dict(dust=D_(30)), PR=dict(bokeh=BK(0.4)))
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
MOOD = dict(HK="bayou", KB="nightkid", MS="amber", CH="moss", WP="inkblue", CT="cream", BK="candy", WN="dusk", WH="skyblue", FC="toyred", GE="snowy", CZ="rainbow", PR="violet")
light, cur = [{"t": 0, "mood": "bayou"}], "bayou"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"bayou": {"sun": {"azimuth": 210, "elevation": 22, "color": "#fff0c0", "intensity": 2.5}, "sky": {"top": "#96b46e", "horizon": "#fadc96"}, "fill": {"sky": "#fff8e0", "ground": "#6a6a4a", "intensity": 1.5}},
              "nightkid": {"sun": {"azimuth": 150, "elevation": 35, "color": "#ffe0b0", "intensity": 2.6}, "sky": {"top": "#3c3c8c", "horizon": "#6e64be"}, "fill": {"sky": "#e0d8ff", "ground": "#4a4070", "intensity": 2.0}},
              "amber": {"sun": {"azimuth": 220, "elevation": 20, "color": "#ffd8a0", "intensity": 2.5}, "sky": {"top": "#f09650", "horizon": "#ffdca0"}, "fill": {"sky": "#fff0d8", "ground": "#7a6040", "intensity": 1.5}},
              "moss": {"sun": {"azimuth": 30, "elevation": 45, "color": "#f8ffd8", "intensity": 2.5}, "sky": {"top": "#3c7850", "horizon": "#a0c882"}, "fill": {"sky": "#f0ffe0", "ground": "#4a5a3a", "intensity": 1.8}},
              "inkblue": {"sun": {"azimuth": -20, "elevation": 40, "color": "#fff4e0", "intensity": 2.6}, "sky": {"top": "#324682", "horizon": "#6478b4"}, "fill": {"sky": "#e8ecff", "ground": "#4a4a60", "intensity": 2.0}},
              "cream": {"sun": {"azimuth": 20, "elevation": 45, "color": "#fff8e8", "intensity": 2.2}, "sky": {"top": "#dcd0b0", "horizon": "#f0e6cc"}, "fill": {"sky": "#fff8f0", "ground": "#9a8a70", "intensity": 1.2}},
              "candy": {"sun": {"azimuth": 30, "elevation": 40, "color": "#fff4f0", "intensity": 2.4}, "sky": {"top": "#faaac8", "horizon": "#c8fae6"}, "fill": {"sky": "#fff0f8", "ground": "#9a6a7a", "intensity": 1.4}},
              "dusk": {"sun": {"azimuth": 230, "elevation": 16, "color": "#ffc8a0", "intensity": 2.5}, "sky": {"top": "#7850a0", "horizon": "#ffaa78"}, "fill": {"sky": "#ffe0d8", "ground": "#5a4a5a", "intensity": 1.85}},
              "skyblue": {"sun": {"azimuth": 40, "elevation": 45, "color": "#fffbe8", "intensity": 2.3}, "sky": {"top": "#5aa0e6", "horizon": "#c8e6fa"}, "fill": {"sky": "#f0f8ff", "ground": "#6a7a60", "intensity": 1.3}},
              "toyred": {"sun": {"azimuth": -20, "elevation": 40, "color": "#fff0d8", "intensity": 2.4}, "sky": {"top": "#e6463c", "horizon": "#ffc85a"}, "fill": {"sky": "#fff0e0", "ground": "#8a5040", "intensity": 1.6}},
              "snowy": {"sun": {"azimuth": 40, "elevation": 35, "color": "#fff0d8", "intensity": 2.2}, "sky": {"top": "#6e96d2", "horizon": "#dcecfa"}, "fill": {"sky": "#f0f8ff", "ground": "#8a96aa", "intensity": 1.2}},
              "rainbow": {"sun": {"azimuth": 30, "elevation": 45, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#78c8fa", "horizon": "#ffe6fa"}, "fill": {"sky": "#fff8ff", "ground": "#9a7a6a", "intensity": 1.3}},
              "violet": {"sun": {"azimuth": 10, "elevation": 40, "color": "#fff0d0", "intensity": 2.6}, "sky": {"top": "#5a3c8c", "horizon": "#966ebe"}, "fill": {"sky": "#f0e0ff", "ground": "#5a4050", "intensity": 2.0}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ffa040", "paper": ["#e8a868", "#c88848"], "dofPx": 8, "particle": "#fff4d8", "bokehColor": "#ffd8a8", "ray": "#fff1c8", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(nov="November 14th", brook="In Brooklyn a", ideal="and start the", germany="Meanwhile in Germany", craze="By 1907", yousee="You see Berryman", cuddly="So the cuddly",
           refused="refused", sleeps="sleeps", notwell="not going well", hounds="hounds", club="club", tie="tie it", shot="take the shot", refuses="refuses", unsport="unsportsmanlike",
           draws="draws", spreads="spreads", sews="sews", sign="sign", sells="It sells", out="sells out", yes="yes", quit="quit candy", thousand="thousand", attacks="attacks",
           hugging="hugging", smaller="smaller", cuter="Cuter", beaten="beaten", cartoon2="a cartoon of")
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
