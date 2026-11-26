#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 30: Pepsi's 1996 Harrier jet ad and the student who tried to buy it.
usage: build_short.py <project folder>
Ten 90s Memphis-pop sets 70 units apart: HK sky-blue schoolyard (hook + loop; the covered "?" price tag = open loop, revealed as 700,000,000
POINTS + JUST KIDDING), TV cobalt-bubblegum Memphis studio, DR grape-lime dorm, HG steel-teal hangar, RT peach-lilac rooftop, PO red-white-blue
post street, HQ mirror-glass plaza, FC cool marble federal court, FN pastel rainbow fantasy, LV dusk-lilac living room. Shots 0.7-2 s, every
neighbour a different move; the jet, cans, tags and checks are the stars, people small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, TV=70, DR=140, HG=210, RT=280, PO=350, HQ=420, FC=490, FN=560, LV=630)
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


yard("HK", "schoolyard.png", "lawn.jpg"); box("HK", 0.45, 0.04, -2.4, [0.5, 0.5, 0.5], color="#ff78be"); box("HK", -4.0, 0.04, -2.4, [0.6, 0.5, 0.5], color="#aaf03c"); tree("HK", -2.8, -4.2, 0.9, "#5aaa5a"); tree("HK", 3.2, -4.4, 1.0, "#64b464")
yard("TV", "memphis.png", "studio.jpg"); box("TV", -1.2, 0.04, -4.0, [0.6, 0.6, 0.6], color="#aaf03c"); box("TV", 1.4, 0.04, -4.2, [0.5, 0.9, 0.5], color="#ffe650")
yard("DR", "dorm.png", "dormfl.jpg"); box("DR", 1.6, 0.04, -2.6, [1.3, 0.7, 0.8], color="#7a5a8a"); box("DR", -3.6, 0.04, -3.6, [1.4, 0.5, 0.8], color="#aaf03c")
yard("HG", "hangar.png", "hangfl.jpg"); crate("HG", -3.4, 0, -3.8); barrel("HG", 3.2, -3.6)
yard("RT", "rooftop.png", "roof.jpg"); box("RT", 3.2, 0.04, -3.6, [0.8, 1.0, 0.8], color="#b48ca0")
yard("PO", "poststreet.png", "sidewalk.jpg"); post("PO", -2.6, -3.4, 2.2, "#3a3a50")
yard("HQ", "glassplaza.png", "plaza.jpg"); box("HQ", -3.6, 0.04, -3.8, [1.2, 0.4, 1.2], color="#9ad2f0")
yard("FC", "fedcourt.png", "marblefl.jpg")
yard("FN", "fantasy.png", "cloudfl.jpg"); box("FN", -1.7, 0.04, -2.4, [1.0, 0.46, 0.8], color="#ffffff"); box("FN", 2.6, 0.04, -3.6, [1.0, 0.7, 0.8], color="#fff0fa")
yard("LV", "livingroom.png", "rug.jpg"); box("LV", -2.7, 0.04, -2.4, [1.6, 0.5, 0.8], color="#b48cdc"); box("LV", 0, 0.04, -3.2, [2.2, 0.3, 0.7], color="#5a4a7a")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("school_K", "school", pos("HK", 0.0, 0.04, -5.6), 2.6); put("jetK", "jet", pos("HK", 0.0, 1.35, -2.7), 0.8, face="hover"); human("johnK", "john", pos("HK", -0.6, 0.04, -2.3), face="happy", h=1.4)
put("tagqK", "pricetag", pos("HK", 0.45, 0.54, -2.4), 0.55); put("tag7K", "pricetag", pos("HK", -4.0, 0.54, -2.4), 0.7, face="7m")
put("jetL", "jet", pos("HK", 4.5, 1.5, -2.7), 0.9, face="hover"); human("pilotK", "pilot", pos("HK", 6.0, 0.04, -2.2), face="happy", h=1.6)
put("stuffT", "stuff", pos("TV", 0.0, 0.04, -2.8), 1.4); put("canT", "can", pos("TV", 2.6, 0.04, -2.4), 1.1); put("tvT", "tvset", pos("TV", -2.8, 0.04, -2.6), 1.4)
human("johnD", "john", pos("DR", 0.0, 0.04, -2.2), face="happy", h=1.6); put("calcD", "calc", pos("DR", 1.6, 0.74, -2.6), 0.6); put("dimeD", "dime", pos("DR", -2.6, 0.04, -2.4), 0.8)
put("jetG", "jet", pos("HG", 0.0, 0.04, -2.8), 1.3); human("johnG", "john", pos("HG", -2.4, 0.04, -2.2), face="sad", h=1.6)
put("investR", "investors", pos("RT", 0.0, 0.04, -2.6), 0.95)
put("mailP", "mailbox", pos("PO", 0.0, 0.04, -2.6), 1.3); put("checkP", "check", pos("PO", 2.8, 0.6, -2.4), 0.8)
put("suitH", "suit", pos("HQ", 0.0, 0.04, -2.6), 1.3); put("canH", "can", pos("HQ", 2.4, 0.04, -2.4), 1.1); put("checkH", "check", pos("HQ", -2.6, 0.7, -2.4), 0.7)
put("benchF", "bench", pos("FC", 0.0, 0.04, -3.4), 1.4); human("judgeF", "judge", pos("FC", 2.0, 0.04, -2.4), face="happy", h=1.7); human("johnF", "john", pos("FC", -2.0, 0.04, -2.4), face="happy", h=1.6); put("stampF", "stampd", pos("FC", 4.6, 0.04, -2.4), 1.0)
put("jetN", "jet", pos("FN", 0.6, 1.0, -3.0), 0.9); human("pilotN", "pilot", pos("FN", -1.7, 0.5, -2.4), face="happy", h=1.5)
put("tvL", "tvset", pos("LV", 0.0, 0.34, -3.2), 1.4, face="series"); human("johnL", "john", pos("LV", -1.4, 0.04, -2.2), face="happy", h=1.6)
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


HOOK = dict(anchor=(0.0, 1.3, -2.5), dist=6.4, yaw=4, pitch=6)
# ---- Pepsi put a fighter jet in an ad as a joke. A college student tried to buy it.
s = S("0", "HK", zoom=8, **HOOK); act(s, 0.0, "jetK", face="hover", shake=0.4); tag(s, 0.0, "hookc", 0.31, 0.0, wf=0.6, hf=0.19); act(s, 0.3, "tagqK", shake=0.4); act(s, 0.1, "johnK", pose=dict(armR=-150))
ft(s, "johnK", ["shocked", "happy"]); snap(s, rel(s, "joke"), 10)
s = S("A college student", "DR", (0.0, 1.0, -2.2), 4.4, -10, pitch=5, zoom=12, dof=dict(focus="johnD", blur=0.4)); ft(s, "johnD", ["smug", "happy"]); T(s, "tryc", at=rel(s, "tried"), dy=0.37, wf=0.62)
# ---- 1996. Pepsi Stuff. Drink Pepsi, collect points, trade them for T-shirts and leather jackets. Then the final shot.
s = crane("1996", "TV", (0.0, 1.0, -2.8), 7.6, -22, -2, 36, 8); T(s, "y1996", at=0.05, dx=-0.24, dy=0.22, wf=0.26, hf=0.26); snap(s, rel(s, "Stuff"), 10)
s = S("Drink Pepsi collect", "TV", (2.6, 0.6, -2.4), 4.2, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="canT", blur=0.5)); act(s, 0.05, "canT", shake=0.5); act(s, rel(s, "collect"), "canT", shake=0.5)
s = S("trade them for", "TV", (0.0, 0.8, -2.8), 6.4, 6, pitch=8, zoom=4, pan=(-8, 0)); act(s, 0.4, "stuffT", shake=0.4)
s = S("Then the final", "TV", (-2.8, 0.75, -2.6), 4.8, -8, pitch=5, zoom=12, dof=dict(focus="tvT", blur=0.4)); act(s, 0.05, "tvT", shake=0.4); T(s, "shotc", at=0.1, dy=0.37, wf=0.56)
# ---- A teenager lands a Harrier jump jet at his high school. Price: seven million Pepsi Points.
s = crane("A teenager lands", "HK", (5.2, 1.0, -2.5), 6.6, 22, 2, 34, 8); go(s, 0.05, "jetL", pos("HK", 4.5, 0.06, -2.7), 0.7, walk=False); ft(s, "pilotK", ["happy", "smug"])
s = S("Harrier jump jet", "HK", (4.5, 0.5, -2.7), 4.4, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="jetL", blur=0.5)); show(s, 0.0, "jetL", pos("HK", 4.5, 0.06, -2.7), hop=0); act(s, 0.05, "jetL", face="default", shake=0.4); T(s, "harrier", at=0.1, dy=0.37, wf=0.5); snap(s, 0.2, 8)
s = S("Price seven million", "HK", (-4.0, 0.85, -2.4), 4.6, 8, pitch=12, pitchTo=3, dof=dict(focus="tag7K", blur=0.4)); act(s, rel(s, "seven"), "tag7K", shake=0.6)
s = S("Pepsi Points", "TV", (2.6, 0.6, -2.4), 5.0, -6, pitch=5, zoom=-10); act(s, 0.0, "canT", face="shocked", shake=0.5)
# ---- Nobody can drink that much Pepsi. But John Leonard, a business student, found the loophole. You could buy extra points. Ten cents each.
s = S("Nobody can drink", "HQ", (2.4, 0.7, -2.4), 4.4, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="canH", blur=0.5)); act(s, 0.05, "canH", face="shocked", shake=0.4); T(s, "nobody", at=0.1, dy=0.38, wf=0.62)
s = S("But John Leonard", "DR", (0.0, 1.05, -2.2), 4.6, 8, pitch=5, zoom=12, dof=dict(focus="johnD", blur=0.4)); ft(s, "johnD", ["happy", "smug"]); T(s, "johnc", at=0.05, dy=0.37, wf=0.6)
s = S("found the loophole", "DR", (1.6, 1.0, -2.6), 4.0, -10, pitch=14, pitchTo=4, dof=dict(focus="calcD", blur=0.4)); act(s, 0.05, "calcD", shake=0.4); T(s, "loop", at=rel(s, "loophole"), dy=0.38, wf=0.5)
s = crane("You could buy", "DR", (0.6, 1.0, -2.4), 7.0, 22, 2, 34, 8); ft(s, "johnD", ["smug", "happy"])
s = S("Ten cents each", "DR", (-2.6, 0.45, -2.4), 4.2, 12, pitch=6, yawTo=-6, type="macro", dof=dict(focus="dimeD", blur=0.5)); act(s, 0.05, "dimeD", shake=0.6); T(s, "tenc", at=0.1, dy=0.36, wf=0.5); snap(s, 0.15, 8)
# ---- Seven million points? Seven hundred thousand dollars. For a military jet worth over thirty million.
s = S("Seven million points", "DR", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="SEVEN MILLION POINTS?", items=["SEVEN HUNDRED THOUSAND DOLLARS"]))
s = S("Seven hundred thousand", "DR", (1.6, 0.95, -2.6), 4.2, 8, pitch=8, zoom=12, dof=dict(focus="calcD", blur=0.4)); act(s, 0.0, "calcD", face="sum", shake=0.5)
s = crane("For a military", "HG", (0.0, 0.9, -2.8), 7.6, -22, -2, 36, 8); hide(s, 0.0, "johnG")
s = S("worth over thirty", "HG", (0.0, 0.65, -2.8), 5.2, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="jetG", blur=0.4)); act(s, 0.05, "jetG", shake=0.3); T(s, "worth", at=rel(s, "thirty") - 0.1, dy=0.36, wf=0.56); snap(s, rel(s, "thirty"), 8); cfx(s, 0.2, "glint", "jetG", 0.6)
# ---- So he found five investors. He mailed Pepsi fifteen labels and a check for seven hundred thousand dollars and eight dollars fifty. Some of that was shipping and handling.
s = crane("So he found", "RT", (0.0, 0.8, -2.6), 7.0, 22, 2, 34, 8); act(s, rel(s, "five"), "investR", shake=0.5); T(s, "five", at=rel(s, "five"), dy=0.34, wf=0.46)
s = S("He mailed Pepsi", "PO", (0.0, 0.8, -2.6), 4.8, -8, pitch=5, zoom=12, dof=dict(focus="mailP", blur=0.4)); act(s, 0.05, "mailP", face="sent", shake=0.4)
s = S("and a check", "PO", (2.8, 1.0, -2.4), 4.4, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="checkP", blur=0.5)); act(s, 0.05, "checkP", shake=0.4); snap(s, 0.2, 8)
s = S("and eight dollars", "PO", (2.8, 1.0, -2.4), 5.6, 6, pitch=5, zoom=-8); act(s, rel(s, "fifty"), "checkP", shake=0.5)
s = crane("Some of that", "HQ", (-2.6, 1.05, -2.4), 5.0, -22, -2, 34, 8); act(s, 0.3, "checkH", shake=0.4)
# ---- Pepsi sent the check back. He sued.
s = S("Pepsi sent the", "PO", (0.0, 0.8, -2.6), 5.0, 8, pitch=5, zoom=-10); act(s, 0.0, "mailP", face="back", shake=0.5)
s = S("He sued", "HQ", (0.0, 0.8, -2.6), 4.6, -6, pitch=12, pitchTo=3, dof=dict(focus="suitH", blur=0.4)); act(s, 0.05, "suitH", shake=0.7); T(s, "suedc", at=0.1, dy=0.38, wf=0.46); snap(s, 0.2, 10)
# ---- You see, Pepsi said it was obviously a joke, and in 1999 a federal judge agreed.
s = S("Pepsi said it", "HQ", (2.4, 0.7, -2.4), 4.4, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="canH", blur=0.5)); show(s, 0.0, "canH", pos("HQ", 2.4, 0.04, -2.4), hop=0); act(s, 0.0, "canH", face="default", shake=0.4); cfx(s, rel(s, "obviously"), "glint", "canH", 0.6)
s = crane("and in 1999", "FC", (0.0, 1.1, -3.0), 7.8, 22, 2, 36, 8); hide(s, 0.0, "judgeF"); hide(s, 0.0, "johnF"); T(s, "y1999", at=rel(s, "1999"), dx=-0.24, dy=0.22, wf=0.26, hf=0.26)
s = S("a federal judge", "FC", (0.0, 0.9, -3.4), 5.6, -10, pitch=14, pitchTo=4, dof=dict(focus="benchF", blur=0.4)); act(s, rel(s, "agreed"), "benchF", face="bang", shake=0.7); snap(s, rel(s, "agreed"), 10)
# ---- Judge Kimba Wood called flying a jet to school an exaggerated adolescent fantasy.
s = S("Judge Kimba Wood", "FC", (2.0, 1.05, -2.4), 4.6, -8, pitch=5, zoom=12, dof=dict(focus="judgeF", blur=0.4)); show(s, 0.0, "judgeF", pos("FC", 2.0, 0.04, -2.4), hop=0); act(s, 0.0, "benchF", face="default"); ft(s, "judgeF", ["smug", "happy"]); T(s, "kimba", at=0.05, dy=0.37, wf=0.5)
s = crane("flying a jet", "FN", (0.3, 1.2, -2.8), 7.0, -22, -2, 34, 8); hide(s, 0.0, "pilotN"); go(s, 0.05, "jetN", pos("FN", 0.0, 1.4, -3.0), 0.9, walk=False); cfx(s, 0.2, "speed", "jetN", 0.6)
s = S("an exaggerated adolescent", "FN", (-0.6, 1.2, -2.6), 7.4, 8, pitch=5, zoom=-10); show(s, 0.0, "pilotN", pos("FN", -1.7, 0.5, -2.4), hop=0.2); ft(s, "pilotN", ["happy", "smug"]); T(s, "fant", at=rel(s, "adolescent"), dy=0.36, wf=0.62); snap(s, rel(s, "adolescent"), 10)
# ---- No objective person, the court said, could see a real offer. Leonard lost. The appeal failed too.
s = S("No objective person", "FC", (0.0, 1.0, -2.8), 7.6, 6, pitch=8, zoom=4, pan=(-8, 0)); show(s, 0.0, "johnF", pos("FC", -2.0, 0.04, -2.4), hop=0); ft(s, "judgeF", ["smug", "happy"]); ft(s, "johnF", ["nervous", "confused"])
s = S("could see a", "HK", (-4.0, 0.85, -2.4), 4.4, -12, pitch=6, yawTo=4, type="macro", dof=dict(focus="tag7K", blur=0.5)); act(s, rel(s, "offer"), "tag7K", shake=0.6)
s = S("Leonard lost", "FC", (-2.0, 1.0, -2.4), 4.4, 10, pitch=5, zoom=12, dof=dict(focus="johnF", blur=0.4)); ft(s, "johnF", ["sad", "shocked"]); T(s, "lost", at=0.05, dy=0.37, wf=0.5); cfx(s, 0.2, "sweat", "johnF", 0.5)
s = S("The appeal failed", "FC", (4.6, 0.6, -2.4), 4.4, -12, pitch=6, yawTo=4, type="macro", dof=dict(focus="stampF", blur=0.5)); act(s, rel(s, "failed"), "stampF", shake=0.7); T(s, "appealc", at=rel(s, "failed"), dy=0.38, wf=0.62)
# ---- But Pepsi still changed the ad. The jet now cost seven hundred million points. And two new words appeared under the price: just kidding.
s = crane("But Pepsi still", "TV", (-2.8, 0.9, -2.6), 6.0, 22, 2, 34, 8); act(s, rel(s, "changed"), "tvT", shake=0.5); T(s, "newad", at=rel(s, "changed"), dy=0.34, wf=0.62)
s = S("The jet now", "HG", (0.0, 0.65, -2.8), 5.0, -12, pitch=6, yawTo=4, type="macro", dof=dict(focus="jetG", blur=0.4)); show(s, 0.0, "jetG", pos("HG", 0.0, 0.04, -2.8), hop=0); act(s, 0.05, "jetG", shake=0.4)
s = S("seven hundred million", "HK", (0.45, 0.85, -2.4), 4.2, -6, pitch=6, zoom=12, dof=dict(focus="tagqK", blur=0.4)); hide(s, 0.0, "johnK"); hide(s, 0.0, "jetK"); act(s, 0.0, "tagqK", face="700m", shake=0.7); snap(s, 0.15, 8)
s = S("And two new", "HK", (0.45, 0.85, -2.4), 4.8, 4, pitch=14, pitchTo=3); act(s, rel(s, "appeared"), "tagqK", shake=0.4)
s = S("just kidding", "TV", (2.6, 0.6, -2.4), 4.6, 12, pitch=6, yawTo=-4, dof=dict(focus="canT", blur=0.4)); act(s, 0.0, "canT", face="default", shake=0.5)
# ---- Leonard never got his jet. He got a Netflix series instead, in 2022.
s = S("Leonard never got", "HG", (-1.2, 1.0, -2.4), 6.4, -8, pitch=5, zoom=-10); hide(s, 0.02, "jetG"); show(s, 0.0, "johnG", pos("HG", -2.4, 0.04, -2.2), hop=0); ft(s, "johnG", ["sad", "confused"]); T(s, "nojet", at=0.1, dy=0.36, wf=0.46)
s = crane("He got a", "LV", (-0.6, 1.0, -2.6), 7.0, -22, -2, 34, 8); ft(s, "johnL", ["happy", "smug"]); snap(s, rel(s, "Netflix"), 10)
s = S("in 2022", "LV", (0.0, 1.05, -3.2), 4.6, 8, pitch=6, zoom=12, dof=dict(focus="tvL", blur=0.4)); act(s, 0.05, "tvL", shake=0.4); T(s, "netc", at=0.05, dy=0.38, wf=0.56)
# ---- Because nobody told a college student that Pepsi's fighter jet was a joke.
s = S("Because nobody told", "DR", (0.0, 1.05, -2.2), 5.0, -12, pitch=6, yawTo=4); ft(s, "johnD", ["smug", "happy"])
s = S("that Pepsi's fighter", "HK", (0.0, 1.85, -2.7), 4.6, -10, pitch=5, yawTo=6, type="macro", dof=dict(focus="jetK", blur=0.4)); act(s, 0.0, "tagqK", face="default"); hide(s, 0.0, "tagqK"); show(s, 0.0, "jetK", pos("HK", 0.0, 1.35, -2.7), hop=0); act(s, 0.05, "jetK", face="hover", shake=0.3); T(s, "jokec", at=0.05, dy=0.38, wf=0.5)
s = S("was a joke", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); show(s, 0.0, "johnK", pos("HK", -0.6, 0.04, -2.3), hop=0); show(s, 0.0, "tagqK", pos("HK", 0.45, 0.54, -2.4), hop=0); act(s, 0.05, "jetK", face="hover", shake=0.4); act(s, 0.05, "johnK", pose=dict(armR=-150)); T(s, "hookc", at=0.05, dy=0.31, wf=0.6, hf=0.19)
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
ATM = dict(HK=dict(dust=D_(20), rays=dict(angle=28, intensity=0.6)), TV=dict(bokeh=BK(0.5)), DR=dict(bokeh=BK(0.45)), HG=dict(dust=D_(26), rays=dict(angle=22, intensity=0.7)), RT=dict(dust=D_(20), rays=dict(angle=18, intensity=0.6)),
           PO=dict(dust=D_(20), rays=dict(angle=30, intensity=0.5)), HQ=dict(dust=D_(18), rays=dict(angle=26, intensity=0.6)), FC=dict(dust=D_(22), rays=dict(angle=24, intensity=0.6)), FN=dict(bokeh=BK(0.5)), LV=dict(bokeh=BK(0.5)))
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
MOOD = dict(HK="school", TV="memphis", DR="dorm", HG="hangar", RT="rooftop", PO="post", HQ="plaza", FC="fedcourt", FN="fantasy", LV="living")
light, cur = [{"t": 0, "mood": "school"}], "school"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"school": {"sun": {"azimuth": 40, "elevation": 46, "color": "#fffbf0", "intensity": 2.4}, "sky": {"top": "#5ab4ff", "horizon": "#dcf0ff"}, "fill": {"sky": "#f4faff", "ground": "#5a8a5a", "intensity": 1.5}},
              "memphis": {"sun": {"azimuth": 160, "elevation": 40, "color": "#fff4fa", "intensity": 2.5}, "sky": {"top": "#285ae6", "horizon": "#ff82c8"}, "fill": {"sky": "#fff4fa", "ground": "#8a4a7a", "intensity": 2.0}},
              "dorm": {"sun": {"azimuth": 150, "elevation": 36, "color": "#fff0e8", "intensity": 2.5}, "sky": {"top": "#7846aa", "horizon": "#be8cdc"}, "fill": {"sky": "#fbf4ff", "ground": "#5a4a6a", "intensity": 2.1}},
              "hangar": {"sun": {"azimuth": 30, "elevation": 44, "color": "#f4ffff", "intensity": 2.5}, "sky": {"top": "#286478", "horizon": "#82c8c8"}, "fill": {"sky": "#f0ffff", "ground": "#5a6a70", "intensity": 1.9}},
              "rooftop": {"sun": {"azimuth": 230, "elevation": 20, "color": "#ffe0c8", "intensity": 2.5}, "sky": {"top": "#c896e6", "horizon": "#ffbe96"}, "fill": {"sky": "#fff4f0", "ground": "#7a5a6a", "intensity": 1.8}},
              "post": {"sun": {"azimuth": 40, "elevation": 50, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#96d2ff", "horizon": "#f0f8ff"}, "fill": {"sky": "#f8fbff", "ground": "#8a8a90", "intensity": 1.4}},
              "plaza": {"sun": {"azimuth": 50, "elevation": 46, "color": "#f8fcff", "intensity": 2.4}, "sky": {"top": "#3c96f0", "horizon": "#c8ebff"}, "fill": {"sky": "#f4faff", "ground": "#8a8a96", "intensity": 1.5}},
              "fedcourt": {"sun": {"azimuth": 150, "elevation": 40, "color": "#f4f8ff", "intensity": 2.5}, "sky": {"top": "#5a78aa", "horizon": "#b4c8e6"}, "fill": {"sky": "#f4f8ff", "ground": "#6a7080", "intensity": 1.9}},
              "fantasy": {"sun": {"azimuth": 160, "elevation": 44, "color": "#fff8fc", "intensity": 2.3}, "sky": {"top": "#ffbee6", "horizon": "#bee6ff"}, "fill": {"sky": "#fffaff", "ground": "#a08aa0", "intensity": 1.5}},
              "living": {"sun": {"azimuth": 150, "elevation": 34, "color": "#f8f0ff", "intensity": 2.6}, "sky": {"top": "#6e5aa0", "horizon": "#be96c8"}, "fill": {"sky": "#f4f8ff", "ground": "#4a4060", "intensity": 2.3}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff2d55", "paper": ["#8cb4ff", "#7aa0eb"], "dofPx": 8, "particle": "#fff8ff", "bokehColor": "#ffb4dc", "ray": "#fff8f0", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(nobody="Nobody can drink", yousee="You see Pepsi", butpepsi="But Pepsi still",
           joke="as a joke", tried="tried", y1996="1996", stuff="Stuff", drink="Drink", trade="trade", final="final shot", lands="lands", harrier="Harrier", price="Price", seven="seven million",
           john="John Leonard", loophole="loophole", ten="Ten cents", sevenh="Seven hundred", military="military", thirty="thirty", five="five", mailed="mailed", check="and a check", fifty="fifty",
           shipping="shipping", back="sent the check", sued="sued", y1999="1999", agreed="agreed", kimba="Kimba", flying="flying", fantasy="fantasy", objective="objective", offer="offer",
           lost="Leonard lost", appeal="appeal", changed="changed", sevenm="seven hundred million", kidding="kidding", never="Leonard never", netflix="Netflix", y2022="2022", because="Because nobody")
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
