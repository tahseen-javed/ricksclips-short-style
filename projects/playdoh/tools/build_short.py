#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 17: Play-Doh was wallpaper cleaner (Kutol, Kay Zufall, Joe McVicker).
usage: build_short.py <project folder>
Ten candy-clay sets 70 units apart: PR candy playroom (hook + loop, covered "?" trophy = open loop), CN amber 1930s Cincinnati, KF teal-copper
soap works, SO grey sooty coal home, GS mint-coral 1950s atomic home, DR aqua drain, NS crayon-yellow nursery class, DS red-cream 1956 store,
TV purple TV studio, HF gold Hall of Fame.  Shots 1-2 s, every neighbour a different move (push / orbit / crane / whip / tilt / pull / macro)."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(PR=0, CN=70, KF=140, SO=210, GS=280, DR=350, NS=420, DS=490, TV=560, HF=630)
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


yard("PR", "playroom.png", "candy.jpg"); box("PR", -2.9, 0.04, -2.6, [0.6, 0.6, 0.6], color="#ff5a8a"); box("PR", -2.4, 0.04, -3.4, [0.5, 0.9, 0.5], color="#5ab4ff"); box("PR", 3.0, 0.04, -2.4, [0.5, 0.5, 0.5], color="#ffd23c")
yard("CN", "cincy.png", "cobblesep.jpg"); house("CN", -3.4, -4.4, [1.6, 2.6, 1.4], "#6a3a2a", color="#b8704a"); house("CN", 3.4, -4.6, [1.6, 3.2, 1.4], "#5a3a30", color="#a0603e")
for x in (-1.8, 1.8): post("CN", x, -3.0, 2.4, "#3a2a24")
yard("KF", "factory.png", "factile.jpg"); table("KF", 2.2, -2.0, 1.2, 0.8, 0.74, "#c87840"); box("KF", -2.8, 0.04, -2.4, [0.9, 0.9, 0.9], color="#ff8aa8"); box("KF", 3.6, 0.04, -3.8, [1.0, 1.4, 1.0], color="#d08040")
yard("SO", "sooty.png", "oldboard.jpg"); box("SO", -3.2, 0.04, -3.0, [1.0, 0.8, 0.6], color="#6a5a54"); box("SO", 3.2, 0.04, -3.4, [0.8, 1.2, 0.6], color="#5a4a44")
yard("GS", "atomic.png", "atomtile.jpg"); table("GS", -2.9, -2.2, 1.0, 0.7, 0.74, "#ff7a6e"); box("GS", 3.0, 0.04, -3.2, [1.2, 0.8, 0.7], color="#7ad2c0")
yard("DR", "bath.png", "aqua.jpg"); box("DR", -1.4, 0.04, -2.6, [0.5, 1.0, 0.5], color="#f4fbff"); box("DR", 1.4, 0.04, -2.6, [0.5, 1.0, 0.5], color="#f4fbff"); box("DR", -3.2, 0.04, -3.2, [0.9, 0.6, 0.6], color="#8ad8e6")
yard("NS", "school.png", "classfloor.jpg"); table("NS", 0.2, -2.9, 1.2, 0.7, 0.6, "#5ab4ff"); box("NS", 3.0, 0.04, -3.0, [0.8, 0.8, 0.6], color="#ff9a3c")
yard("DS", "store.png", "marble.jpg"); box("DS", -3.0, 0.04, -2.8, [1.0, 1.0, 0.7], color="#f6e0b0"); box("DS", 3.0, 0.04, -3.0, [1.0, 1.4, 0.7], color="#c83040")
yard("TV", "studio.png", "stage.jpg"); box("TV", -3.0, 0.04, -3.0, [0.6, 1.6, 0.6], color="#3a2a5a"); box("TV", 3.0, 0.04, -3.0, [0.6, 1.6, 0.6], color="#3a2a5a")
yard("HF", "fame.png", "redcarpet.jpg"); box("HF", 0.0, 0.04, -2.2, [1.0, 0.86, 0.8], color="#c83040"); box("HF", -3.0, 0.04, -3.0, [0.8, 1.2, 0.8], color="#ffd878")

# ================================================================== CHARACTERS (cards carry "_" in the id: not frame-checked as cast; hero props are)
human("kidaP", "kida", pos("PR", -0.75, 0.04, -1.6), face="shocked", h=1.25); put("canPR", "can", pos("PR", 0.45, 0.04, -1.9), 1.2, face="shocked"); put("pdPR", "pdcan", PARK, 1.2)
put("trophy_PR", "trophy", pos("PR", 1.25, 0.04, -3.4), 0.8, face="q")
human("joeK", "joe", pos("KF", -0.75, 0.04, -1.7), face="happy"); human("kayK", "kay", PARK, face="happy"); put("soapK", "soap", pos("KF", 2.2, 0.78, -2.0), 0.7); put("doughK", "dough", pos("KF", -2.8, 0.94, -2.4), 0.55)
human("momS", "mom", pos("SO", -1.4, 0.04, -1.6), face="nervous"); put("stoveS", "stove", pos("SO", 1.6, 0.04, -2.2), 1.5); put("wall_S", "wallp", pos("SO", 0.0, 0.25, -2.8), 2.4)
human("momG", "mom50", pos("GS", -0.9, 0.04, -1.6), face="happy"); put("furnG", "furnace", pos("GS", 1.0, 0.04, -2.2), 1.5); put("vinylG", "vinyl", pos("GS", -2.9, 0.78, -2.2), 0.55)
put("whirlD", "whirl", pos("DR", 0.0, 0.1, -2.6), 1.1); put("canD", "can", pos("DR", 0.0, 1.3, -2.3), 0.75, face="sad")
human("kayN", "kay", pos("NS", -1.3, 0.04, -1.6), face="happy"); human("kidaN", "kida", pos("NS", 1.1, 0.04, -1.9), face="happy", h=1.25); human("kidbN", "kidb", pos("NS", 1.9, 0.04, -1.7), face="happy", h=1.25)
put("clay_N", "clay", pos("NS", 0.2, 0.64, -2.9), 0.5); put("magN", "mag", PARK, 0.5)
human("kidbD", "kidb", pos("DS", -0.8, 0.04, -1.6), face="shocked", h=1.25); put("canDS", "pdcan", pos("DS", 0.9, 0.04, -2.0), 1.2)
put("tvT", "tv", pos("TV", 0.4, 0.04, -2.2), 1.6); human("kidaT", "kida", pos("TV", -1.1, 0.04, -1.5), face="happy", h=1.25)
put("trophyH", "trophy", pos("HF", 0.0, 0.9, -2.2), 1.1); put("cansH", "cans", pos("HF", 1.6, 0.04, -3.8), 0.9)
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


HOOK = dict(anchor=(-0.12, 0.8, -1.9), dist=6.8, yaw=4, pitch=8)
# ---- Every kid in America has played with wallpaper cleaner. You just called it Play-Doh.
s = S("0", "PR", zoom=14, pan=(-3, 0), **HOOK); ft(s, "kidaP", ["shocked", "happy", "shocked"]); act(s, 0.0, "kidaP", pose=dict(armR=-150)); act(s, 0.1, "canPR", shake=0.4)
tag(s, 0.0, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
s = S("has played with", "PR", (0.45, 0.7, -1.9), 3.4, -14, pitch=4, yawTo=6, type="macro", dof=dict(focus="canPR", blur=0.5)); act(s, 0.1, "canPR", shake=0.3); snap(s, max(0.3, rel(s, "cleaner")), 14)
s = crane("You just called", "PR", (0.0, 0.85, -2.0), 8.2, 20, 2, 34, 6); ft(s, "kidaP", ["happy", "shocked"]); hide(s, rel(s, "Playdoh"), "canPR"); show(s, rel(s, "Playdoh") + 0.02, "pdPR", pos("PR", 0.45, 0.04, -1.9)); act(s, 0.1, "trophy_PR", shake=0.3); T(s, "wait", rel(s, "Playdoh") + 0.15, wf=0.5)
# ---- Cincinnati. Kutol Products, a small soap company. Back then, homes burned coal, and soot turned every wall gray.
s = S("Cincinnati", "CN", (0.0, 1.6, -3.0), 9.6, 0, pitch=6, zoom=4, pan=(36, 0)); c_ = T(s, "cinci", dy=0.32, wf=0.48, hf=0.12); swap(s, c_, rel(s, "Kutol"), "kutol")
s = crane("a small soap", "KF", (0.75, 1.1, -1.9), 10.0, -24, -4, 36, 6); ft(s, "joeK", ["happy", "smug"]); act(s, 0.1, "soapK", shake=0.3); cfx(s, 0.2, "glint", "soapK", 0.7)
s = S("Back then", "SO", (0.1, 1.2, -2.0), 9.6, 10, pitch=6, zoom=-10); ft(s, "momS", ["nervous", "shocked"]); act(s, 0.1, "stoveS", shake=0.4); T(s, "coal")
s = S("and soot turned", "SO", (0.0, 1.3, -2.8), 5.0, -6, pitch=14, pitchTo=2, zoom=4, type="macro"); act(s, 0.1, "wall_S", shake=0.2); T(s, "gray"); snap(s, rel(s, "gray"), 14)
s = S("Kutol's best seller", "KF", (-1.72, 1.1, -2.0), 7.6, 6, pitch=16, pitchTo=4); ft(s, "joeK", ["smug", "happy"]); act(s, 0.1, "doughK", shake=0.3); T(s, "best")
s = S("a soft doughy", "KF", (-2.8, 1.2, -2.4), 3.2, 14, pitch=4, yawTo=-4, type="macro", dof=dict(focus="doughK", blur=0.5)); act(s, 0.05, "doughK", face="shocked", shake=0.3); act(s, 0.6, "doughK", face="default"); cfx(s, 0.3, "glint", "doughK", 0.7)
# ---- You rolled it across the wallpaper, and the dirt came right off.
s = S("You rolled it", "SO", (-1.05, 1.2, -2.0), 5.0, 10, pitch=5, zoom=12); ft(s, "momS", ["happy", "smug"]); act(s, 0.0, "momS", pose=dict(armR=-110)); T(s, "rolled")
s = S("and the dirt", "SO", (0.0, 1.3, -2.8), 5.0, -8, pitch=4, yawTo=6, zoom=4, type="macro"); act(s, 0.05, "wall_S", face="clean", shake=0.3); T(s, "dirt"); snap(s, rel(s, "off"), 12)
# ---- Then, after World War Two, America switched to gas and oil heat. No soot. No dirty walls. Washable vinyl wallpaper finished the job.
s = crane("Then after World", "GS", (0.1, 1.2, -1.9), 8.5, 22, 2, 38, 6); ft(s, "momG", ["happy", "smug"]); T(s, "ww2", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("America switched to", "GS", (1.0, 0.9, -2.2), 3.6, -10, pitch=4, zoom=12, type="macro", dof=dict(focus="furnG", blur=0.5)); act(s, 0.1, "furnG", shake=0.3); T(s, "gasoil")
s = S("No soot", "SO", (1.6, 0.9, -2.2), 4.2, 8, pitch=4, zoom=-12); act(s, 0.0, "stoveS", face="sad", shake=0.3); T(s, "nosoot")
s = S("No dirty walls", "GS", (-0.9, 1.3, -1.6), 4.4, -14, pitch=5, yawTo=4, zoom=4, dof=dict(focus="momG", blur=0.4)); ft(s, "momG", ["smug", "happy"]); T(s, "nowalls"); snap(s, rel(s, "walls"), 12)
s = S("Washable vinyl", "GS", (-2.9, 1.05, -2.2), 3.0, 6, pitch=16, pitchTo=4, type="macro", dof=dict(focus="vinylG", blur=0.5)); act(s, 0.1, "vinylG", shake=0.3); T(s, "vinylc"); cfx(s, 0.4, "glint", "vinylG", 0.7)
# ---- Kutol's biggest hit was going down the drain.
s = crane("Kutol's biggest hit", "DR", (0.0, 1.1, -2.4), 8.0, -20, 0, 50, 10); act(s, 0.1, "canD", shake=0.3); T(s, "drain")
s = S("going down the", "DR", (0.0, 0.85, -2.4), 4.6, 6, pitch=6, zoom=14, type="macro", dof=dict(focus="canD", blur=0.4)); go(s, 0.1, "canD", pos("DR", 0.0, 0.55, -2.3), 1.0, walk=False); act(s, 0.1, "whirlD", shake=0.3); snap(s, rel(s, "drain"), 14)
# ---- You see, the rescue came from the family. Kay Zufall was a nursery school teacher, and Joe McVicker's sister-in-law.
s = crane("You see the", "NS", (0.3, 1.1, -1.9), 10.6, -22, -2, 36, 6); ft(s, "kayN", ["happy", "smug"]); ft(s, "kidaN", ["happy", "shocked"]); T(s, "rescue")
s = S("from the family", "KF", (-0.1, 1.3, -1.6), 6.2, 10, pitch=6, zoom=-10, _dis=1); show(s, 0.0, "kayK", pos("KF", 0.55, 0.04, -1.5), hop=0); ft(s, "kayK", ["happy", "smug"]); ft(s, "joeK", ["happy", "shocked"])
s = S("Kay Zufall was", "NS", (-1.3, 1.35, -1.6), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="kayN", blur=0.4)); ft(s, "kayN", ["happy", "smug"]); T(s, "kayc")
s = S("and Joe McVicker's", "KF", (-0.1, 1.4, -1.6), 6.0, -16, pitch=5, yawTo=2, zoom=4); ft(s, "joeK", ["happy", "smug"]); ft(s, "kayK", ["smug", "happy"]); T(s, "sil"); snap(s, rel(s, "sisterinlaw"), 12)
# ---- She read that the putty could be used for art projects. She tried it with her class. The kids loved it.
s = S("She read that", "NS", (-1.25, 1.15, -1.5), 3.6, -8, pitch=12, pitchTo=2, dof=dict(focus="magN", blur=0.4)); show(s, 0.0, "magN", pos("NS", -0.8, 0.92, -1.3), hop=0.1); ft(s, "kayN", ["confused", "happy"]); cfx(s, 0.2, "question", "kayN", 0.8)
s = S("could be used", "NS", (0.2, 0.92, -2.9), 3.0, 10, pitch=4, zoom=12, type="macro", dof=dict(focus="clay_N", blur=0.5)); act(s, 0.1, "clay_N", shake=0.3); T(s, "art")
s = crane("She tried it", "NS", (0.3, 1.1, -1.9), 10.6, 24, 4, 40, 6); hide(s, 0.0, "magN"); ft(s, "kayN", ["happy", "smug"]); ft(s, "kidaN", ["happy", "shocked"]); ft(s, "kidbN", ["shocked", "happy"]); T(s, "klass")
s = S("The kids loved", "NS", (1.5, 0.95, -1.8), 4.2, -10, pitch=5, zoom=-10); ft(s, "kidaN", ["happy", "shocked"]); ft(s, "kidbN", ["shocked", "happy"]); act(s, 0.0, "kidaN", pose=dict(armR=-150, armL=150)); act(s, 0.0, "kidbN", pose=dict(armR=-150, armL=150)); T(s, "loved"); snap(s, rel(s, "loved"), 12); cfx(s, 0.3, "blush", "kidaN", 0.7)
# ---- So she told Joe: stop selling it for walls. Sell it to kids. She even gave it a new name. Play-Doh.
s = S("So she told", "KF", (-0.1, 1.4, -1.6), 5.6, 14, pitch=5, zoom=12); ft(s, "kayK", ["shouting", "smug"]); ft(s, "joeK", ["shocked", "nervous"]); act(s, 0.0, "kayK", pose=dict(armR=-150)); T(s, "stop")
s = S("Sell it to", "KF", (-0.75, 1.4, -1.7), 3.6, -14, pitch=5, yawTo=4, dof=dict(focus="joeK", blur=0.4)); ft(s, "joeK", ["shocked", "happy"]); T(s, "sellk")
s = S("She even gave", "NS", (-1.3, 1.3, -1.6), 4.4, 8, pitch=16, pitchTo=4); ft(s, "kayN", ["smug", "happy"]); act(s, 0.0, "kayN", pose=dict(armR=-150)); T(s, "newname")
s = S("Playdoh#2", "PR", (0.45, 0.7, -1.9), 3.4, 10, pitch=4, zoom=14, type="macro", dof=dict(focus="pdPR", blur=0.5), _dis=1); act(s, 0.05, "pdPR", shake=0.5); cfx(s, 0.15, "glint", "pdPR", 0.7); snap(s, 0.3, 12)
# ---- In 1956, it hit a department store in Washington. Then Macy's. Then Captain Kangaroo started playing with it on TV.
s = crane("In 1956", "DS", (0.0, 1.2, -1.8), 9.0, -22, -2, 34, 6); ft(s, "kidbD", ["shocked", "happy"]); T(s, "y1956", dy=0.2, dx=0.15, wf=0.32, hf=0.34)
s = S("it hit a", "DS", (0.9, 1.0, -2.0), 4.2, -10, pitch=4, zoom=12, dof=dict(focus="canDS", blur=0.4)); act(s, 0.1, "canDS", shake=0.3); T(s, "dstore")
s = S("Then Macy's", "DS", (0.05, 1.2, -2.0), 8.6, 6, pitch=5, zoom=4, pan=(24, 0)); ft(s, "kidbD", ["happy", "shocked"]); T(s, "macys")
s = crane("Then Captain Kangaroo", "TV", (-0.2, 1.1, -1.9), 8.6, 22, 2, 36, 6); ft(s, "kidaT", ["happy", "shocked"]); act(s, 0.1, "tvT", shake=0.3); T(s, "ontv")
s = S("playing with it", "TV", (0.4, 0.95, -2.2), 5.4, -12, pitch=4, yawTo=4, type="macro", dof=dict(focus="tvT", blur=0.5)); act(s, 0.1, "tvT", shake=0.4)
# ---- More than two billion cans later, it's in the Toy Hall of Fame.
s = S("More than two", "HF", (0.0, 2.0, -2.0), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="CANS SOLD", items=["2,000,000,000"]))
s = crane("it's in the", "HF", (0.6, 1.3, -2.6), 9.0, -20, 0, 30, 6); act(s, 0.1, "trophyH", shake=0.4); act(s, 0.1, "cansH", shake=0.2); T(s, "hof"); snap(s, rel(s, "Fame"), 14); cfx(s, 0.3, "glint", "trophyH", 0.8)
# ---- Not bad for a product that was dying, because nobody needed to clean their walls.
s = S("Not bad for", "DR", (0.0, 1.0, -2.4), 4.2, -8, pitch=5, zoom=-10); act(s, 0.0, "canD", shake=0.3); T(s, "dying")
s = S("because nobody needed", "GS", (0.1, 1.2, -1.9), 7.8, 16, pitch=5, yawTo=-2, zoom=4); ft(s, "momG", ["smug", "happy"]); T(s, "nobody")
# ---- And every kid in America has played with wallpaper cleaner. (kids cheer, then pull-out onto the hook frame)
s = S("And every kid", "NS", (1.5, 0.95, -1.8), 4.6, 12, pitch=5, zoom=12); ft(s, "kidaN", ["happy", "shocked"]); ft(s, "kidbN", ["shocked", "happy"]); act(s, 0.0, "kidbN", pose=dict(armR=-150, armL=150))
s = S("has played with#2", "PR", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); hide(s, 0.0, "pdPR"); show(s, 0.0, "canPR", pos("PR", 0.45, 0.04, -1.9), hop=0); act(s, 0.0, "trophy_PR", face="default", shake=0.4)
ft(s, "kidaP", ["shocked", "happy", "shocked"]); act(s, 0.0, "kidaP", pose=dict(armR=-150)); act(s, 0.1, "canPR", shake=0.4); tag(s, 0.05, "hookc", 0.3, 0.0, wf=0.66, hf=0.24)
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
ATM = dict(PR=dict(dust=D_(22), rays=dict(angle=30, intensity=0.5)), CN=dict(dust=D_(40), rays=dict(angle=24, intensity=0.6)), KF=dict(dust=D_(20)), SO=dict(dust=D_(44)),
           GS=dict(dust=D_(18), rays=dict(angle=34, intensity=0.55)), DR=dict(bokeh=BK(0.4)), NS=dict(dust=D_(22), rays=dict(angle=28, intensity=0.55)), DS=dict(bokeh=BK(0.35)),
           TV=dict(bokeh=BK(0.4)), HF=dict(bokeh=BK(0.4), rays=dict(angle=20, intensity=0.5)))
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
MOOD = dict(PR="candy", CN="sepia", KF="copper", SO="soot", GS="atomic", DR="aqua", NS="sunny", DS="store", TV="studio", HF="gold")
light, cur = [{"t": 0, "mood": "candy"}], "candy"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 17,
    "moods": {"candy": {"sun": {"azimuth": 40, "elevation": 40, "color": "#fff0f6", "intensity": 2.4}, "sky": {"top": "#ff9ad5", "horizon": "#ffe0f0"}, "fill": {"sky": "#ffe0f4", "ground": "#a08090", "intensity": 1.5}},
              "sepia": {"sun": {"azimuth": -40, "elevation": 22, "color": "#ffc880", "intensity": 2.5}, "sky": {"top": "#e8a060", "horizon": "#ffe0a8"}, "fill": {"sky": "#ffd8a0", "ground": "#705040", "intensity": 1.6}},
              "copper": {"sun": {"azimuth": 30, "elevation": 38, "color": "#ffd8a8", "intensity": 2.4}, "sky": {"top": "#3c9a96", "horizon": "#8ad0c4"}, "fill": {"sky": "#c0f0e6", "ground": "#605040", "intensity": 1.7}},
              "soot": {"sun": {"azimuth": -60, "elevation": 30, "color": "#ffb070", "intensity": 2.5}, "sky": {"top": "#8a8486", "horizon": "#b4aca8"}, "fill": {"sky": "#e0d8d4", "ground": "#605048", "intensity": 1.9}},
              "atomic": {"sun": {"azimuth": 50, "elevation": 45, "color": "#fffbe8", "intensity": 2.4}, "sky": {"top": "#7ad8c8", "horizon": "#e0fff4"}, "fill": {"sky": "#f0fff8", "ground": "#907060", "intensity": 1.4}},
              "aqua": {"sun": {"azimuth": 0, "elevation": 50, "color": "#f0ffff", "intensity": 2.4}, "sky": {"top": "#40aac8", "horizon": "#a8ecf4"}, "fill": {"sky": "#d8faff", "ground": "#508090", "intensity": 1.7}},
              "sunny": {"sun": {"azimuth": 40, "elevation": 45, "color": "#fff4d0", "intensity": 2.4}, "sky": {"top": "#ffc840", "horizon": "#fff0a8"}, "fill": {"sky": "#fff4d0", "ground": "#907050", "intensity": 1.4}},
              "store": {"sun": {"azimuth": 20, "elevation": 45, "color": "#fff0d8", "intensity": 2.4}, "sky": {"top": "#c83040", "horizon": "#ff9a80"}, "fill": {"sky": "#ffe0d0", "ground": "#806050", "intensity": 1.6}},
              "studio": {"sun": {"azimuth": 0, "elevation": 50, "color": "#f8e8ff", "intensity": 2.5}, "sky": {"top": "#5a2aa0", "horizon": "#b070e0"}, "fill": {"sky": "#e0c8ff", "ground": "#504070", "intensity": 1.9}},
              "gold": {"sun": {"azimuth": 0, "elevation": 45, "color": "#fff0c8", "intensity": 2.5}, "sky": {"top": "#c08020", "horizon": "#ffd878"}, "fill": {"sky": "#fff0c8", "ground": "#805030", "intensity": 1.7}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff4f8b", "paper": ["#fff0f6", "#ffd8e8"], "dofPx": 8, "particle": "#fff6fa", "bokehColor": "#ffd0f0", "ray": "#fff4e0", "raySide": 1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(cinci="Cincinnati", then="Then after World", yousee="You see the", y1956="In 1956", more="More than two", notbad="Not bad for", every="And every kid",
           cleaner="cleaner", playdoh="Playdoh", gray="gray", off="off", drain="drain", loved="loved", playdoh2="Playdoh#2", tv="TV", fame="Fame", billion="billion")
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
