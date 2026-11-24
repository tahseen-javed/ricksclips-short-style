#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 21: the Statue of Liberty was never supposed to be green - the green is a patina
that became her armor, and America nearly painted it over.
usage: build_short.py <project folder>
Thirteen copper-to-verdigris sets 70 units apart: HK peach-mint harbor sunrise (hook + loop, a copper paint bucket "?" hangs over her = open
loop, resolved: the paint job would have covered her armor), UN festive 1886 unveiling, PN plum velvet penny stage, SH orange Paris workshop,
ST slate salt storm, GR olive-gold 1910, OF mint city hall, BA terracotta studio, CG navy Congress, NP sepia news street, CH deep-blue lab,
MI violet micro world, CE night skyline with fireworks. Shots 1-2 s, every neighbour a different move."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, UN=70, PN=140, SH=210, ST=280, GR=350, OF=420, BA=490, CG=560, NP=630, CH=700, MI=770, CE=840)
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


yard("HK", "harbor.png", "pier.jpg"); post("HK", 2.2, -3.4, 4.2, "#d8a030"); box("HK", 1.55, 4.1, -3.3, [1.6, 0.14, 0.14], color="#d8a030"); box("HK", -3.0, 0.04, -1.4, [0.6, 0.6, 0.6], color="#e0704a")
yard("UN", "unveil.png", "dock.jpg"); post("UN", -2.4, -2.6, 2.4, "#f4f0e8"); post("UN", 2.5, -2.7, 2.4, "#f4f0e8"); box("UN", 3.0, 0.04, -1.4, [0.6, 0.4, 0.6], color="#3a6ad0")
yard("PN", "velvet.png", "velfloor.jpg"); box("PN", 0.0, 0.04, -2.2, [1.4, 0.6, 0.7], color="#7a3a6a"); table("PN", 2.2, -2.3, 1.2, 0.7, 0.74, "#5a2a4a")
yard("SH", "workshop.png", "forge.jpg"); box("SH", -2.0, 0.04, -2.2, [0.7, 0.7, 0.6], color="#5a4a4a"); box("SH", 2.6, 0.04, -2.6, [0.9, 0.5, 0.7], color="#c87a4a")
yard("ST", "storm.png", "wetstone.jpg"); box("ST", -3.0, 0.04, -1.6, [0.6, 0.5, 0.6], color="#5a6a8a")
yard("GR", "olive.png", "olivestone.jpg"); post("GR", 2.4, -2.6, 1.4, "#7a5a3a"); box("GR", -2.8, 0.04, -1.6, [0.6, 0.4, 0.6], color="#a89a5a")
yard("OF", "cityhall.png", "marble.jpg"); table("OF", 0.9, -1.9, 1.2, 0.7, 0.74, "#7a5a40"); box("OF", -3.0, 0.04, -3.0, [0.8, 1.2, 0.6], color="#5a8a7a")
yard("BA", "studio.png", "terracotta.jpg"); box("BA", -2.8, 0.04, -2.6, [0.8, 0.9, 0.7], color="#e8e0d4")
yard("CG", "congress.png", "navytile.jpg"); table("CG", 0.9, -1.9, 1.2, 0.7, 0.74, "#6a4a3a"); box("CG", -3.0, 0.04, -2.8, [0.8, 1.0, 0.6], color="#e8dcc0")
yard("NP", "newsstreet.png", "cobsepia.jpg"); box("NP", -0.8, 0.04, -1.9, [0.8, 0.8, 0.5], color="#2a6a4a"); post("NP", 2.6, -2.4, 2.4, "#2a2a30")
yard("CH", "lab.png", "labtile.jpg"); table("CH", 0.9, -1.9, 1.2, 0.7, 0.74, "#e8ecf4"); box("CH", -3.0, 0.04, -2.8, [0.8, 1.0, 0.6], color="#4a5a9a")
yard("MI", "micro.png", "microfloor.jpg")
yard("CE", "nightsky.png", "nightpier.jpg"); box("CE", -2.8, 0.04, -1.6, [0.6, 0.5, 0.6], color="#4a5a9a"); post("CE", 2.6, -2.4, 1.6, "#ffd870")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
put("statueH", "liberty", pos("HK", -0.3, 0.04, -3.0), 3.2); put("bucketH", "bucket", pos("HK", 1.0, 2.7, -3.3), 0.7)
put("statueU", "liberty", pos("UN", 0.0, 0.04, -3.0), 3.0, face="veiled")
put("pennyP", "penny", pos("PN", 0.0, 0.64, -2.2), 1.3); put("pen2P", "pennies2", pos("PN", 2.2, 0.78, -2.3), 0.5)
put("sheetsS", "sheets", pos("SH", 0.4, 0.04, -2.2), 1.0)
put("statueS", "liberty", pos("ST", 1.0, 0.04, -3.2), 3.0, face="copper"); put("cloudS", "cloud", pos("ST", -1.3, 2.3, -2.6), 1.3)
put("statueG", "liberty", pos("GR", 0.0, 0.04, -3.0), 3.0, face="half")
human("officialO", "official", pos("OF", -0.6, 0.04, -1.7), face="nervous"); put("miniO", "liberty", pos("OF", 0.9, 0.78, -1.9), 0.9, face="streaky")
human("bartB", "bartholdi", pos("BA", -0.7, 0.04, -1.7), face="happy"); put("sketchB", "sketch", pos("BA", 0.9, 0.04, -2.2), 1.7)
human("senatorC", "senator", pos("CG", -0.6, 0.04, -1.7), face="shouting"); put("bagC", "moneybag", pos("CG", 0.9, 0.78, -1.9), 0.7); put("bucketC", "bucket", pos("CG", 2.0, 0.04, -2.3), 0.8, face="happy")
put("crowd_N", "crowd", pos("NP", 0.0, 0.04, -3.0), 1.6); human("newsN", "newsboy", pos("NP", 0.7, 0.04, -1.8), face="shouting"); put("paperN", "paper", pos("NP", -0.8, 0.84, -1.9), 0.9)
human("chemC", "chemist", pos("CH", -0.6, 0.04, -1.7), face="happy"); put("flaskC", "flask", pos("CH", 0.9, 0.78, -1.9), 0.6)
put("atoms_M", "atoms", pos("MI", 0.0, 0.2, -2.6), 1.6); put("shieldM", "shield", PARK, 1.1)
put("statueE", "liberty", pos("CE", 0.0, 0.04, -3.0), 3.2, face="happy")
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


HOOK = dict(anchor=(0.1, 1.8, -2.8), dist=9.8, yaw=4, pitch=6)
# ---- The Statue of Liberty was never supposed to be green. That famous color is damage.
s = S("0", "HK", zoom=14, pan=(-3, 0), **HOOK); act(s, 0.0, "statueH", shake=0.4); go(s, 0.1, "bucketH", pos("HK", 0.8, 2.75, -3.3), 0.8, walk=False); act(s, 0.5, "bucketH", shake=0.4)
tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
s = S("supposed to be", "HK", (0.0, 1.8, -2.9), 9.4, -12, pitch=16, pitchTo=3); act(s, 0.05, "statueH", shake=0.5); snap(s, rel(s, "green"), 8)
s = S("That famous color", "HK", (0.15, 1.75, -2.9), 7.8, 8, pitch=4, zoom=6, dof=dict(focus="statueH", blur=0.4)); act(s, 0.05, "statueH", shake=0.4); T(s, "damage"); snap(s, rel(s, "damage"), 10)
# ---- New York Harbor. October 28th, 1886. Lady Liberty is unveiled, and she shines like a brand-new penny. Reddish-brown copper, gleaming in the sun.
s = crane("New York Harbor", "UN", (0.0, 1.6, -2.8), 9.6, -22, -2, 36, 6); act(s, 0.2, "statueU", shake=0.3); T(s, "harborc")
s = S("October 28th", "UN", (0.0, 1.8, -2.8), 8.0, 10, pitch=6, zoom=12); T(s, "y1886", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("Lady Liberty is", "UN", (0.0, 1.6, -2.8), 7.6, -16, pitch=5, yawTo=4); act(s, rel(s, "unveiled"), "statueU", face="copper", shake=0.6); T(s, "unveil", at=rel(s, "unveiled"))
s = S("and she shines", "PN", (0.0, 1.3, -2.2), 3.4, 6, pitch=6, zoom=14, type="macro", dof=dict(focus="pennyP", blur=0.5)); act(s, 0.05, "pennyP", shake=0.5); T(s, "pennyc"); snap(s, rel(s, "penny"), 10)
s = S("Reddishbrown copper gleaming", "UN", (0.0, 1.8, -2.8), 7.4, 6, pitch=18, pitchTo=3); act(s, 0.1, "statueU", face="copper", shake=0.3); T(s, "copperc")
# ---- Three hundred hammered sheets, each about as thick as two pennies.
s = crane("Three hundred hammered", "SH", (0.3, 0.9, -2.2), 7.6, 22, 2, 40, 8); act(s, 0.1, "sheetsS", shake=0.5); T(s, "s300")
s = S("each about as", "PN", (2.2, 1.0, -2.3), 2.6, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="pen2P", blur=0.5)); act(s, 0.1, "pen2P", shake=0.4); T(s, "thick")
# ---- But salt air and rain get to work. The shine fades to a dull brown. Then green streaks creep in.
s = crane("But salt air", "ST", (0.0, 1.6, -2.8), 9.2, 20, 0, 34, 6); act(s, 0.1, "cloudS", shake=0.5); T(s, "salt")
s = S("rain get to", "ST", (-1.4, 2.9, -2.6), 5.0, -6, pitch=4, zoom=14, dof=dict(focus="cloudS", blur=0.4)); act(s, 0.05, "cloudS", shake=0.6)
s = S("The shine fades", "ST", (1.0, 1.6, -3.2), 6.6, -16, pitch=5, yawTo=4); act(s, rel(s, "fades"), "statueS", face="brown", shake=0.4); T(s, "dull")
s = S("Then green streaks", "ST", (1.0, 1.7, -3.2), 6.4, 6, pitch=4, zoom=10, dof=dict(focus="statueS", blur=0.4)); act(s, 0.05, "statueS", face="streaky", shake=0.5); T(s, "streaks"); snap(s, rel(s, "streaks"), 10)
# ---- By 1910, she's half copper, half blue-green. Patchy, blotchy, and spreading. Officials fear the green is eating her alive.
s = crane("By 1910", "GR", (0.0, 1.6, -2.8), 9.4, -22, -2, 36, 6); act(s, 0.1, "statueG", shake=0.3); T(s, "y1910", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("half copper half", "GR", (0.0, 1.7, -3.0), 6.8, 8, pitch=5, zoom=12); act(s, 0.1, "statueG", shake=0.4); T(s, "halfc"); snap(s, 0.6, 8)
s = S("Patchy blotchy and", "GR", (0.0, 1.6, -3.0), 6.4, -6, pitch=4, zoom=4, pan=(24, 0), dof=dict(focus="statueG", blur=0.4)); act(s, 0.1, "statueG", shake=0.3); T(s, "patchy")
s = crane("Officials fear the", "OF", (0.0, 1.2, -1.8), 7.6, 20, 0, 34, 6); ft(s, "officialO", ["nervous", "shocked"]); cfx(s, 0.3, "sweat", "officialO", 0.7)
s = S("is eating her", "OF", (0.9, 1.25, -1.9), 2.8, -8, pitch=6, zoom=14, type="macro", dof=dict(focus="miniO", blur=0.5)); act(s, 0.05, "miniO", shake=0.5); T(s, "eating")
# ---- Even her designer, Frederic Bartholdi, guessed wrong. He expected her to darken to red.
s = crane("Even her designer", "BA", (0.0, 1.2, -1.9), 8.0, -20, 0, 32, 6); ft(s, "bartB", ["happy", "smug"]); T(s, "bart")
s = S("guessed wrong He", "BA", (-0.7, 1.25, -1.7), 4.6, 14, pitch=5, yawTo=-2); ft(s, "bartB", ["shocked", "nervous"]); T(s, "wrong"); cfx(s, 0.3, "sweat", "bartB", 0.6); snap(s, rel(s, "wrong"), 10)
s = S("to darken to", "BA", (0.9, 1.0, -2.2), 3.4, -8, pitch=12, pitchTo=2, type="macro", dof=dict(focus="sketchB", blur=0.5)); act(s, 0.05, "sketchB", shake=0.4); T(s, "redc")
# ---- So in 1906, Congress sets aside sixty-two thousand dollars to paint her back to copper.
s = crane("So in 1906", "CG", (0.7, 1.2, -1.9), 9.0, -22, -2, 34, 6); ft(s, "senatorC", ["shouting", "smug"]); T(s, "y1906", dy=0.2, dx=-0.15, wf=0.32, hf=0.34)
s = S("aside sixtytwo", "CG", (0.0, 1.8, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="SIXTY-TWO THOUSAND DOLLARS", items=["62000"]))
s = S("to paint her", "CG", (1.45, 1.0, -2.1), 5.8, -10, pitch=5, zoom=8, dof=dict(focus="bucketC", blur=0.4)); act(s, 0.05, "bucketC", shake=0.5); act(s, 0.2, "bagC", shake=0.4); T(s, "paintc"); snap(s, rel(s, "copper"), 8)
# ---- And the public explodes. Newspapers call it sacrilege. The plan quietly dies.
s = crane("And the public", "NP", (0.0, 1.2, -2.2), 8.6, -22, -2, 34, 6); ft(s, "newsN", ["shouting", "shocked"]); act(s, 0.1, "crowd_N", shake=0.5); T(s, "explode"); snap(s, rel(s, "explodes"), 10)
s = S("Newspapers call it", "NP", (-0.8, 1.3, -1.9), 3.6, 10, pitch=8, pitchTo=2, type="macro", dof=dict(focus="paperN", blur=0.5)); act(s, 0.05, "paperN", shake=0.5)
s = S("The plan quietly", "CG", (0.6, 1.1, -2.0), 8.8, 12, pitch=5, zoom=-8); act(s, 0.05, "bucketC", face="sad", shake=0.3); ft(s, "senatorC", ["nervous", "confused"]); T(s, "dies")
# ---- You see, that green isn't rot. It's a patina. Copper reacts with the air and grows its own thin skin.
s = crane("You see that", "CH", (0.1, 1.2, -1.8), 7.8, 20, 0, 32, 6); ft(s, "chemC", ["happy", "smug"]); c_ = T(s, "notrot"); swap(s, c_, rel(s, "patina"), "patina"); act(s, rel(s, "patina"), "flaskC", shake=0.5); act(s, rel(s, "patina"), "chemC", pose=dict(armR=-150)); cfx(s, rel(s, "patina"), "glint", "chemC", 0.4)
s = S("Copper reacts with", "MI", (0.0, 1.1, -2.6), 7.4, -4, pitch=10, zoom=14); act(s, 0.1, "atoms_M", shake=0.4); T(s, "react")
s = S("and grows its", "MI", (0.0, 1.0, -2.6), 6.0, 18, pitch=5, yawTo=-2); act(s, 0.1, "atoms_M", shake=0.3); T(s, "skin"); snap(s, rel(s, "skin"), 10)
# ---- And that skin seals the metal underneath, shielding it from more corrosion. The damage is the armor.
s = crane("And that skin", "MI", (0.0, 1.1, -2.4), 9.2, -20, 0, 30, 6); show(s, 0.05, "shieldM", pos("MI", 0.0, 0.7, -2.2)); T(s, "sealc")
s = S("shielding it from", "MI", (0.0, 1.25, -2.2), 3.4, 8, pitch=4, zoom=12, type="macro", dof=dict(focus="shieldM", blur=0.4)); act(s, 0.05, "shieldM", shake=0.5); T(s, "shieldc")
s = S("The damage is", "CE", (0.0, 1.7, -3.0), 6.4, -8, pitch=4, zoom=10, dof=dict(focus="statueE", blur=0.4)); act(s, 0.05, "statueE", face="armor", shake=0.5); T(s, "armor"); snap(s, rel(s, "armor"), 10)
# ---- About ten years later, she's green from crown to toe. She's stayed that way for over a century.
s = crane("About ten years", "CE", (0.0, 1.6, -2.8), 9.6, 22, 2, 36, 6); act(s, 0.1, "statueE", face="happy", shake=0.3); T(s, "later")
s = S("green from crown", "CE", (0.0, 1.7, -3.0), 7.4, -8, pitch=20, pitchTo=2); act(s, 0.1, "statueE", shake=0.3); T(s, "crownc")
s = S("stayed that way", "CE", (0.0, 1.6, -3.0), 8.2, 18, pitch=5, yawTo=-2); act(s, 0.1, "statueE", face="armor", shake=0.3); T(s, "century")
# ---- So the paint job would have covered the one thing keeping her alive. America nearly erased its most famous color,
s = S("So the paint", "HK", (0.3, 2.2, -2.8), 6.6, 10, pitch=5, zoom=12); go(s, 0.05, "bucketH", pos("HK", 0.6, 2.95, -3.3), 0.9, walk=False); act(s, 0.4, "statueH", shake=0.4); T(s, "paintjob")
s = S("the one thing", "HK", (-0.1, 1.85, -2.9), 7.0, -10, pitch=4, yawTo=4, dof=dict(focus="statueH", blur=0.4)); act(s, 0.05, "statueH", shake=0.5); T(s, "alive"); snap(s, rel(s, "alive"), 10)
s = crane("America nearly erased", "HK", (0.1, 1.6, -2.8), 10.0, -22, -2, 36, 6); act(s, 0.2, "bucketH", shake=0.4); T(s, "erased")
s = S("its most famous", "HK", (0.1, 1.8, -2.8), 8.6, -6, pitch=6, zoom=10); act(s, 0.1, "statueH", shake=0.4)
# ---- because the Statue of Liberty was never supposed to be green. (pull-out onto the hook frame)
s = S("because the Statue", "HK", (0.2, 1.8, -2.8), 8.0, 16, pitch=5, yawTo=2); act(s, 0.1, "statueH", shake=0.3)
s = S("was never supposed#2", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "bucketH", pos("HK", 1.0, 2.7, -3.3), hop=0); act(s, 0.0, "statueH", shake=0.3)
go(s, 0.2, "bucketH", pos("HK", 0.8, 2.75, -3.3), 0.8, walk=False); tag(s, 0.05, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
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
ATM = dict(HK=dict(dust=D_(20), rays=dict(angle=30, intensity=0.55)), UN=dict(dust=D_(24), rays=dict(angle=24, intensity=0.55)), PN=dict(bokeh=BK(0.45)), SH=dict(dust=D_(44)), ST=dict(bokeh=BK(0.4)),
           GR=dict(dust=D_(22), rays=dict(angle=20, intensity=0.6)), OF=dict(dust=D_(18)), BA=dict(dust=D_(24), rays=dict(angle=28, intensity=0.5)), CG=dict(dust=D_(18)), NP=dict(dust=D_(30)),
           CH=dict(bokeh=BK(0.45)), MI=dict(bokeh=BK(0.5)), CE=dict(bokeh=BK(0.45)))
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
MOOD = dict(HK="sunrise", UN="festive", PN="velvet", SH="forge", ST="storm", GR="olive", OF="mintoffice", BA="terracotta", CG="navyhall", NP="sepia", CH="lab", MI="micro", CE="night")
light, cur = [{"t": 0, "mood": "sunrise"}], "sunrise"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 21,
    "moods": {"sunrise": {"sun": {"azimuth": 200, "elevation": 22, "color": "#ffe0c0", "intensity": 2.5}, "sky": {"top": "#faa896", "horizon": "#c8f0dc"}, "fill": {"sky": "#fff0e8", "ground": "#8a7a8a", "intensity": 1.5}},
              "festive": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fff4d8", "intensity": 2.4}, "sky": {"top": "#5a96e6", "horizon": "#ffe2a0"}, "fill": {"sky": "#f0f4ff", "ground": "#8a7a6a", "intensity": 1.4}},
              "velvet": {"sun": {"azimuth": 10, "elevation": 50, "color": "#fff0d8", "intensity": 2.6}, "sky": {"top": "#5a1e50", "horizon": "#963c78"}, "fill": {"sky": "#ffd8f0", "ground": "#5a2a4a", "intensity": 2.0}},
              "forge": {"sun": {"azimuth": -20, "elevation": 35, "color": "#ffc890", "intensity": 2.5}, "sky": {"top": "#aa5032", "horizon": "#e68c50"}, "fill": {"sky": "#ffd8b0", "ground": "#6a4030", "intensity": 1.85}},
              "storm": {"sun": {"azimuth": 30, "elevation": 40, "color": "#e0ecff", "intensity": 2.5}, "sky": {"top": "#465a82", "horizon": "#96aac8"}, "fill": {"sky": "#e0ecff", "ground": "#4a5a6a", "intensity": 1.9}},
              "olive": {"sun": {"azimuth": 210, "elevation": 18, "color": "#ffe0a8", "intensity": 2.5}, "sky": {"top": "#b4aa50", "horizon": "#ffd28c"}, "fill": {"sky": "#fff0d0", "ground": "#7a6a4a", "intensity": 1.5}},
              "mintoffice": {"sun": {"azimuth": 20, "elevation": 40, "color": "#fffbe8", "intensity": 2.4}, "sky": {"top": "#78beaa", "horizon": "#bee6d6"}, "fill": {"sky": "#f0fff8", "ground": "#5a6a60", "intensity": 1.5}},
              "terracotta": {"sun": {"azimuth": 30, "elevation": 45, "color": "#fff0e0", "intensity": 2.4}, "sky": {"top": "#d2785a", "horizon": "#f0b48c"}, "fill": {"sky": "#fff0e0", "ground": "#8a5a40", "intensity": 1.5}},
              "navyhall": {"sun": {"azimuth": 0, "elevation": 45, "color": "#fff0d0", "intensity": 2.6}, "sky": {"top": "#283c78", "horizon": "#5a6eaa"}, "fill": {"sky": "#e0e8ff", "ground": "#4a3a5a", "intensity": 2.0}},
              "sepia": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fff0d0", "intensity": 2.4}, "sky": {"top": "#c8a078", "horizon": "#f0d2aa"}, "fill": {"sky": "#fff0e0", "ground": "#7a6050", "intensity": 1.5}},
              "lab": {"sun": {"azimuth": 20, "elevation": 40, "color": "#e8f4ff", "intensity": 2.6}, "sky": {"top": "#283c82", "horizon": "#506eb4"}, "fill": {"sky": "#d8fff0", "ground": "#3a4a70", "intensity": 2.0}},
              "micro": {"sun": {"azimuth": 30, "elevation": 40, "color": "#e0fff8", "intensity": 2.6}, "sky": {"top": "#3c2878", "horizon": "#288c96"}, "fill": {"sky": "#d0fff0", "ground": "#3a5a70", "intensity": 2.0}},
              "night": {"sun": {"azimuth": 150, "elevation": 35, "color": "#d8e8ff", "intensity": 2.6}, "sky": {"top": "#1e2864", "horizon": "#505aaa"}, "fill": {"sky": "#c8f0ff", "ground": "#3a4070", "intensity": 2.0}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#3fe0b0", "paper": ["#7cc8b0", "#5aa890"], "dofPx": 8, "particle": "#fff4d8", "bokehColor": "#a8ffe0", "ray": "#fff1c8", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(harbor="New York Harbor", salt="But salt air", congress="So in 1906", yousee="You see that", later="About ten years", damage="damage", unveiled="unveiled", penny="penny",
           hammered="hammered", rain="rain get", fades="fades", streaks="streaks", y1910="By 1910", eating="eating", wrong="guessed wrong", explodes="explodes", sacrilege="sacrilege",
           dies="dies", patina="patina", skin="thin skin", armor="armor", century="century", erased="erased", paintjob="So the paint", alive="alive", dollars="dollars")
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
