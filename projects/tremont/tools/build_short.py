#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 28: Chicago 1861 - the Tremont House rose six feet while its guests stayed inside.
usage: build_short.py <project folder>
Eleven gaslight-Victorian sets 70 units apart: HK amber gaslight street with the hotel on jackscrews (hook + loop; a violet "?" rail-car silhouette =
open loop, resolved as the Pullman sleeping car), RM rose hotel room, PL emerald parlour, BL sky-blue brick block, CR amber crawlspace of jackscrews,
SH cream shop street, SW teal swamp + lake cross-section, MN misty green night, WK terracotta street works, WS brass-cream glass workshop, RN
Prussian-blue starry railway. Shots 0.7-2 s, every neighbour a different move; buildings and props are the stars, people small companions."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(HK=0, RM=70, PL=140, BL=210, CR=280, SH=350, SW=420, MN=490, WK=560, WS=630, RN=700)
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


yard("HK", "gaslight.png", "cobble.jpg"); box("HK", 2.6, 0.04, -1.2, [0.5, 0.4, 0.5], color="#a86a40")
yard("RM", "roseroom.png", "rug.jpg"); box("RM", 1.5, 0.04, -3.6, [0.8, 1.2, 0.5], color="#8a5040")
yard("PL", "parlour.png", "green.jpg"); box("PL", 1.3, 0.04, -2.8, [0.7, 0.9, 0.6], color="#c8a050")
yard("BL", "blocksky.png", "boards.jpg")
yard("CR", "crawl.png", "dirt.jpg")
yard("SH", "shopst.png", "shopfl.jpg"); box("SH", 1.4, 0.04, -1.6, [0.6, 0.5, 0.6], color="#ff5a5f")
yard("SW", "swamp.png", "mud.jpg")
yard("MN", "mistnight.png", "night.jpg")
yard("WK", "works.png", "dirt.jpg")
yard("WS", "workshop.png", "brass.jpg"); box("WS", 2.6, 0.04, -3.0, [1.0, 0.8, 0.6], color="#b48c50")
yard("RN", "railnight.png", "ballast.jpg"); box("RN", 0, 0.045, -2.6, [14, 0.06, 0.12], color="#8a7a6a"); box("RN", 0, 0.045, -2.1, [14, 0.06, 0.12], color="#8a7a6a")

# ================================================================== CHARACTERS (cards + background decor carry "_" in the id: not frame-checked; hero props are)
put("jacksH", "jacks", pos("HK", 0.0, 0.04, -2.6), 0.4); put("hotelH", "hotel", pos("HK", 0.0, 0.44, -2.6), 2.0, face="wave"); put("carq_H", "car", pos("HK", 1.15, 0.04, -4.4), 0.36, face="q")
put("stepsH", "steps", pos("HK", -3.3, 0.04, -2.2), 1.0); human("guestH", "guest", pos("HK", -2.1, 0.04, -2.0), face="happy", h=1.6)
put("bedR", "bed", pos("RM", 0.0, 0.04, -2.6), 1.0); put("dinnerR", "dinner", pos("RM", 3.0, 0.04, -2.4), 0.9); put("deskR", "desk", pos("RM", 4.6, 0.04, -2.4), 1.0)
human("guestR", "guest", pos("RM", -3.4, 0.04, -2.0), face="happy", h=1.6); put("winR", "winframe", pos("RM", -2.45, 0.6, -2.2), 1.0)
human("senatorP", "senator", pos("PL", 0.0, 0.04, -2.2), face="happy")
put("blockB", "block", pos("BL", 0.0, 0.04, -3.0), 1.0)
put("bellC", "bell", pos("CR", -3.4, 1.2, -2.6), 0.9); put("crewC", "crew", pos("CR", 0.0, 0.04, -2.6), 0.6); put("screwC", "screw", pos("CR", 3.4, 0.04, -2.4), 1.3)
human("crew1C", "crew1", pos("CR", 5.6, 0.04, -2.1), face="happy", h=1.6); human("crew2C", "crew2", pos("CR", 6.6, 0.04, -2.2), face="happy", h=1.6)
put("shopS", "shop", pos("SH", 0.0, 0.04, -2.6), 1.5)
put("xsecW", "xsec", pos("SW", 0.0, 0.04, -2.6), 1.2)
put("germM", "germ", pos("MN", 0.0, 0.5, -2.6), 1.2); put("twentyM", "twenty", pos("MN", 4.0, 0.04, -2.4), 0.9)
put("pipeK", "pipe", pos("WK", 0.0, 0.04, -2.4), 1.0)
human("pullmanS", "pullman", pos("WS", -1.0, 0.04, -2.0), face="happy"); put("glassS", "glass", pos("WS", 1.0, 0.04, -2.4), 1.2)
put("carN", "car", pos("RN", 0.0, 0.04, -2.4), 0.9, face="q")
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


HOOK = dict(anchor=(0.0, 1.45, -2.4), dist=6.8, yaw=4, pitch=6)
# ---- A six-story hotel rose six feet into the air while its guests stayed inside.
s = S("0", "HK", zoom=7, **HOOK); act(s, 0.0, "hotelH", face="wave", shake=0.4); tag(s, 0.0, "hookc", 0.33, 0.0, wf=0.6, hf=0.18); act(s, 0.3, "carq_H", shake=0.3); snap(s, rel(s, "rose"), 10)
s = S("into the air", "HK", (0.0, 1.3, -2.6), 6.6, -6, pitch=2, pitchTo=14); act(s, 0.0, "hotelH", face="default"); go(s, 0.05, "hotelH", pos("HK", 0.0, 0.6, -2.6), 0.8, walk=False)
s = S("while its guests", "RM", (0.0, 0.75, -2.6), 4.6, 12, pitch=6, zoom=12, dof=dict(focus="bedR", blur=0.4)); act(s, 0.1, "bedR", shake=0.3)
# ---- Chicago, 1861. The Tremont House. Inch by inch, for days, the whole hotel climbs.
s = crane("Chicago 1861", "HK", (0.0, 1.4, -2.5), 7.8, -22, -2, 36, 8); show(s, 0.0, "hotelH", pos("HK", 0.0, 0.44, -2.6), hop=0); hide(s, 0.0, "guestH"); hide(s, 0.0, "stepsH"); T(s, "y1861", at=rel(s, "1861"), dx=-0.26, dy=0.2, wf=0.24, hf=0.24)
s = S("The Tremont House", "HK", (0.0, 1.9, -2.6), 6.0, 6, pitch=5, zoom=8, dof=dict(focus="hotelH", blur=0.4))
s = S("Inch by inch", "CR", (3.4, 0.9, -2.4), 4.4, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="screwC", blur=0.5)); act(s, 0.1, "screwC", face="turn", shake=0.4); act(s, 0.6, "screwC", face="default"); T(s, "inch", at=0.05, dy=0.38, wf=0.56)
s = S("the whole hotel", "HK", (0.0, 1.45, -2.5), 6.2, 10, pitch=5, zoom=-10); show(s, 0.0, "hotelH", pos("HK", 0.0, 0.44, -2.6), hop=0); go(s, 0.1, "hotelH", pos("HK", 0.0, 0.62, -2.6), 1.0, walk=False)
# ---- Guests keep sleeping, eating, checking in. A U.S. senator is staying there.
s = S("Guests keep sleeping", "RM", (0.0, 0.8, -2.6), 4.4, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="bedR", blur=0.5)); act(s, 0.05, "bedR", shake=0.3)
s = S("eating checking", "RM", (3.8, 0.75, -2.4), 8.6, -10, pitch=6, yawTo=4); act(s, 0.05, "dinnerR", shake=0.4); act(s, rel(s, "checking"), "deskR", shake=0.4)
s = S("senator is staying", "PL", (0.0, 1.05, -2.2), 4.8, 10, pitch=5, zoom=12, dof=dict(focus="senatorP", blur=0.4)); ft(s, "senatorP", ["happy", "smug"]); T(s, "senat", at=0.05, dy=0.37, wf=0.62)
# ---- One guest notices the front steps getting steeper. Then the windows creep up past eye level.
s = crane("One guest notices", "HK", (-2.7, 1.0, -2.1), 6.2, -22, -2, 34, 8); ft(s, "guestH", ["happy", "confused"])
s = S("getting steeper", "HK", (-3.3, 0.75, -2.2), 3.8, 12, pitch=6, yawTo=-4, type="macro", dof=dict(focus="stepsH", blur=0.5)); hide(s, 0.0, "guestH"); act(s, 0.05, "stepsH", face="steep", shake=0.5); T(s, "steeper", at=rel(s, "steeper"), dy=0.38, wf=0.48); snap(s, rel(s, "steeper"), 8)
s = S("Then the windows", "RM", (-2.9, 1.15, -2.1), 5.0, -10, pitch=5, zoom=10, dof=dict(focus="guestR", blur=0.4)); ft(s, "guestR", ["confused", "shocked"]); go(s, 0.1, "winR", pos("RM", -2.45, 1.0, -2.2), 1.0, walk=False)
s = S("past eye level", "RM", (-2.9, 1.3, -2.1), 4.4, 12, pitch=4, pitchTo=12); show(s, 0.0, "winR", pos("RM", -2.45, 1.0, -2.2), hop=0); go(s, 0.05, "winR", pos("RM", -2.45, 1.35, -2.2), 0.8, walk=False); ft(s, "guestR", ["shocked", "nervous"]); T(s, "eye", at=0.1, dy=0.38, wf=0.58)
# ---- A year earlier, crews did it to half a city block. 320 feet of brick shops. 600 men. 6,000 jackscrews.
s = crane("A year earlier", "BL", (0.0, 1.2, -3.0), 8.6, 22, 2, 38, 8); T(s, "year", at=0.05, dy=0.34, wf=0.6)
s = S("half a city", "BL", (0.0, 0.8, -3.0), 8.0, 4, pitch=8, zoom=4, pan=(-8, 0)); act(s, 0.1, "blockB", shake=0.3)
s = S("320 feet", "BL", (0.0, 0.7, -3.0), 8.2, -12, pitch=6, yawTo=4, dof=dict(focus="blockB", blur=0.4)); T(s, "f320", at=0.05, dy=0.3, wf=0.6)
s = S("600 men", "CR", (0.0, 0.6, -2.6), 6.4, 8, pitch=5, zoom=12); act(s, 0.05, "crewC", shake=0.4); T(s, "m600", at=0.05, dy=0.32, wf=0.4)
s = S("6000 jackscrews", "BL", (0.0, 1.8, -2.4), 6.6, 0, zoom=6, pan=(-3, 0), type="cutaway", long=True, diagram=dict(kind="counter", title="600 MEN", items=["6,000 JACKSCREWS"]))
# ---- On a signal, every man turns his screws one notch. Stores stay open the whole time.
s = S("On a signal", "CR", (-3.4, 1.6, -2.6), 4.4, 12, pitch=6, yawTo=-6, type="macro", dof=dict(focus="bellC", blur=0.5)); act(s, 0.05, "bellC", shake=0.7)
s = S("every man turns", "CR", (6.1, 1.0, -2.15), 5.6, -8, pitch=5, zoom=12, dof=dict(focus="crew1C", blur=0.4))
for w_ in ("crew1C", "crew2C"): act(s, 0.1, w_, pose=dict(armR=-150), shake=0.3); ft(s, w_, ["happy", "smug"])
s = S("one notch", "CR", (3.4, 0.9, -2.4), 4.2, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="screwC", blur=0.5)); act(s, rel(s, "notch"), "screwC", face="turn", shake=0.6); T(s, "notch", at=rel(s, "notch"), dy=0.38, wf=0.5); snap(s, rel(s, "notch"), 10)
s = S("Stores stay open", "SH", (0.0, 0.95, -2.6), 5.6, -8, pitch=5, zoom=12, dof=dict(focus="shopS", blur=0.4)); act(s, 0.1, "shopS", shake=0.4); T(s, "open_", at=rel(s, "open"), dy=0.37, wf=0.62)
# ---- You see, Chicago was built on a swamp, barely above Lake Michigan. In 1854, cholera killed about one in twenty people.
s = crane("You see Chicago", "SW", (0.0, 0.9, -2.6), 7.4, -22, -2, 38, 8); act(s, 0.3, "xsecW", shake=0.3)
s = S("on a swamp", "SW", (0.0, 0.8, -2.6), 6.2, 8, pitch=5, zoom=10, dof=dict(focus="xsecW", blur=0.4)); T(s, "swampc", at=rel(s, "swamp"), dy=0.36, wf=0.5)
s = S("barely above Lake", "SW", (0.0, 0.6, -2.6), 5.4, -14, pitch=6, yawTo=4, type="macro", dof=dict(focus="xsecW", blur=0.5)); act(s, rel(s, "Lake"), "xsecW", shake=0.3)
s = S("In 1854", "MN", (0.0, 1.2, -2.6), 6.0, 6, pitch=14, pitchTo=3, dof=dict(focus="germM", blur=0.4)); act(s, 0.1, "germM", shake=0.4); T(s, "y1854", at=rel(s, "1854"), dx=-0.24, dy=0.24, wf=0.24, hf=0.24)
s = S("killed about one", "MN", (4.0, 0.8, -2.4), 6.0, -10, pitch=5, zoom=10, dof=dict(focus="twentyM", blur=0.4)); act(s, 0.1, "twentyM", shake=0.3); T(s, "one20", at=rel(s, "one"), dy=0.36, wf=0.4)
# ---- So the city picked a wild fix. Lay new sewer pipes along the streets, bury them under fresh dirt, and lift downtown to match. Some buildings went up as much as fourteen feet.
s = crane("So the city", "WK", (0.0, 1.0, -2.4), 7.0, 22, 2, 36, 8); T(s, "wild", at=rel(s, "wild"), dy=0.34, wf=0.5)
s = S("Lay new sewer", "WK", (0.0, 0.75, -2.4), 5.0, -10, pitch=5, zoom=12, dof=dict(focus="pipeK", blur=0.4)); act(s, 0.1, "pipeK", shake=0.4)
s = S("bury them under", "WK", (0.0, 0.7, -2.4), 5.6, 12, pitch=18, pitchTo=6); act(s, 0.1, "pipeK", shake=0.3)
s = S("and lift downtown", "SW", (0.0, 0.8, -2.6), 6.2, 12, pitch=5, yawTo=-4, dof=dict(focus="xsecW", blur=0.4)); act(s, rel(s, "lift"), "xsecW", face="pipes", shake=0.6); snap(s, rel(s, "lift"), 10)
s = S("Some buildings went", "BL", (0.0, 1.0, -3.0), 8.4, -8, pitch=5, zoom=-10); go(s, 0.1, "blockB", pos("BL", 0.0, 0.3, -3.0), 1.0, walk=False); T(s, "f14", at=rel(s, "fourteen"), dy=0.32, wf=0.5)
# ---- The young man behind some of the biggest lifts was George Pullman. His crews raised hotels and a whole city block, without breaking a single pane of glass.
s = crane("The young man", "WS", (-0.15, 1.0, -2.2), 7.0, -22, -2, 36, 8); show(s, 0.0, "blockB", pos("BL", 0.0, 0.04, -3.0), hop=0); ft(s, "pullmanS", ["happy", "smug"])
s = S("was George Pullman", "WS", (-1.0, 1.1, -2.0), 4.6, 10, pitch=5, zoom=12, dof=dict(focus="pullmanS", blur=0.4)); ft(s, "pullmanS", ["smug", "happy"]); T(s, "pullc", at=rel(s, "George"), dy=0.37, wf=0.5)
s = S("His crews raised", "HK", (0.0, 1.45, -2.5), 7.0, -14, pitch=6, yawTo=4); show(s, 0.0, "hotelH", pos("HK", 0.0, 0.44, -2.6), hop=0); act(s, 0.05, "hotelH", face="wave")
s = S("and a whole", "BL", (0.0, 0.9, -3.0), 8.0, 6, pitch=8, zoom=4, pan=(8, 0))
s = S("without breaking a", "WS", (1.0, 0.85, -2.4), 4.2, -12, pitch=6, yawTo=6, type="macro", dof=dict(focus="glassS", blur=0.5)); act(s, 0.1, "glassS", shake=0.3); T(s, "pane", at=rel(s, "pane") - 0.2, dy=0.38, wf=0.62); snap(s, rel(s, "pane"), 8)
# ---- Then he took that skill, moving heavy buildings full of sleeping people, and put it on wheels. The Pullman sleeping car. A hotel that travels.
s = S("Then he took", "WS", (-1.0, 1.1, -2.0), 5.2, -10, pitch=14, pitchTo=4); ft(s, "pullmanS", ["confused", "smug"])
s = S("moving heavy buildings", "HK", (0.0, 1.45, -2.5), 6.6, 8, pitch=5, zoom=-10); act(s, 0.05, "hotelH", face="default"); go(s, 0.1, "hotelH", pos("HK", 0.0, 0.58, -2.6), 0.9, walk=False)
s = S("full of sleeping", "RM", (0.0, 0.8, -2.6), 4.4, 14, pitch=6, yawTo=-4, type="macro", dof=dict(focus="bedR", blur=0.5)); act(s, 0.05, "bedR", shake=0.3)
s = crane("and put it", "RN", (0.0, 0.8, -2.4), 7.4, 22, 2, 36, 8); act(s, rel(s, "wheels") - 0.1, "carN", face="default", shake=0.6); T(s, "wheels", at=rel(s, "wheels"), dy=0.34, wf=0.46); snap(s, rel(s, "wheels"), 10)
s = S("The Pullman sleeping", "RN", (0.0, 0.7, -2.4), 6.0, -8, pitch=5, zoom=12, dof=dict(focus="carN", blur=0.4)); act(s, 0.05, "carN", face="night", shake=0.3)
s = S("A hotel that", "RN", (0.0, 0.75, -2.4), 6.4, 6, pitch=8, zoom=4, pan=(-8, 0)); act(s, 0.0, "carN", face="night"); T(s, "travels", at=0.1, dy=0.35, wf=0.6)
# ---- All from a man who made a six-story hotel rise six feet while its guests stayed inside.
s = S("All from a", "WS", (-1.0, 1.1, -2.0), 4.8, 12, pitch=5, yawTo=-4, dof=dict(focus="pullmanS", blur=0.4)); ft(s, "pullmanS", ["smug", "happy"])
s = crane("who made a", "HK", (0.0, 1.45, -2.4), 8.0, -22, -2, 36, 8); show(s, 0.0, "hotelH", pos("HK", 0.0, 0.44, -2.6), hop=0); act(s, 0.05, "hotelH", face="default")
s = S("rise six", "HK", zoom=-4, pan=(0, 0), **HOOK); s.pop("out"); s.pop("outDur"); act(s, 0.05, "hotelH", face="wave", shake=0.4); T(s, "hookc", at=0.05, dy=0.33, wf=0.6, hf=0.18)
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
ATM = dict(HK=dict(bokeh=BK(0.5)), RM=dict(dust=D_(24)), PL=dict(bokeh=BK(0.45)), BL=dict(dust=D_(22), rays=dict(angle=28, intensity=0.6)), CR=dict(dust=D_(30), rays=dict(angle=18, intensity=0.6)),
           SH=dict(dust=D_(22), rays=dict(angle=30, intensity=0.5)), SW=dict(dust=D_(20), rays=dict(angle=24, intensity=0.5)), MN=dict(bokeh=BK(0.45)), WK=dict(dust=D_(28), rays=dict(angle=22, intensity=0.6)),
           WS=dict(dust=D_(24), rays=dict(angle=20, intensity=0.7)), RN=dict(bokeh=BK(0.5)))
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
MOOD = dict(HK="gaslight", RM="roseroom", PL="emerald", BL="blockday", CR="crawl", SH="shopnoon", SW="swamp", MN="mistnight", WK="works", WS="workshop", RN="railnight")
light, cur = [{"t": 0, "mood": "gaslight"}], "gaslight"
for k, s in enumerate(shots):
    m = MOOD[LOC[id(s)]]
    if m != cur and s.get("type") != "cutaway": light.append({"t": round(max(0.0, starts[k] - 0.2), 3), "mood": m, "fade": 0.4}); cur = m
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6, "seed": 22,
    "moods": {"gaslight": {"sun": {"azimuth": 220, "elevation": 26, "color": "#ffd8a8", "intensity": 2.7}, "sky": {"top": "#5a3c78", "horizon": "#ffaa5a"}, "fill": {"sky": "#fff0e0", "ground": "#6a4a3a", "intensity": 2.1}},
              "roseroom": {"sun": {"azimuth": 150, "elevation": 34, "color": "#ffe8d8", "intensity": 2.5}, "sky": {"top": "#c86e82", "horizon": "#f0a0a0"}, "fill": {"sky": "#fff0f0", "ground": "#7a4a4a", "intensity": 1.8}},
              "emerald": {"sun": {"azimuth": 20, "elevation": 40, "color": "#fff4d8", "intensity": 2.7}, "sky": {"top": "#145a46", "horizon": "#32966e"}, "fill": {"sky": "#f0fff4", "ground": "#3a4a30", "intensity": 2.2}},
              "blockday": {"sun": {"azimuth": 40, "elevation": 46, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#6eb4f0", "horizon": "#e6f0fa"}, "fill": {"sky": "#f4faff", "ground": "#8a7a6a", "intensity": 1.4}},
              "crawl": {"sun": {"azimuth": 200, "elevation": 32, "color": "#ffe0b0", "intensity": 2.6}, "sky": {"top": "#6e461e", "horizon": "#c8823c"}, "fill": {"sky": "#fff0e0", "ground": "#5a3a20", "intensity": 2.0}},
              "shopnoon": {"sun": {"azimuth": 40, "elevation": 48, "color": "#fffbf0", "intensity": 2.3}, "sky": {"top": "#96d2fa", "horizon": "#fff4dc"}, "fill": {"sky": "#fffaf0", "ground": "#9a8a70", "intensity": 1.4}},
              "swamp": {"sun": {"azimuth": 210, "elevation": 30, "color": "#f0fff0", "intensity": 2.5}, "sky": {"top": "#3c8c96", "horizon": "#bee6d2"}, "fill": {"sky": "#f0fff8", "ground": "#4a6a50", "intensity": 1.7}},
              "mistnight": {"sun": {"azimuth": 230, "elevation": 30, "color": "#f0fff0", "intensity": 2.7}, "sky": {"top": "#1e3c46", "horizon": "#46786e"}, "fill": {"sky": "#f0fff8", "ground": "#2a3a34", "intensity": 2.3}},
              "works": {"sun": {"azimuth": 230, "elevation": 18, "color": "#ffd0a8", "intensity": 2.5}, "sky": {"top": "#f0825a", "horizon": "#ffd296"}, "fill": {"sky": "#fff0e8", "ground": "#6a4a3a", "intensity": 1.8}},
              "workshop": {"sun": {"azimuth": 150, "elevation": 36, "color": "#fff4e0", "intensity": 2.3}, "sky": {"top": "#faecce", "horizon": "#f0d2a0"}, "fill": {"sky": "#fffaf0", "ground": "#9a7a50", "intensity": 1.4}},
              "railnight": {"sun": {"azimuth": 20, "elevation": 40, "color": "#f0f4ff", "intensity": 2.7}, "sky": {"top": "#0e1846", "horizon": "#285096"}, "fill": {"sky": "#e8f0ff", "ground": "#1e2a50", "intensity": 2.3}}},
    "lighting": light, "ground": {"texture": TEX + "pave.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "fxLook": {"ink": "#271925", "accent": "#ff5a5f", "paper": ["#c8a06a", "#ae8650"], "dofPx": 8, "particle": "#fff0d8", "bokehColor": "#ffd8a0", "ray": "#fff4dc", "raySide": -1},
    "fx": FX, "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(year="A year earlier", yousee="You see Chicago", sothecity="So the city", young="The young man",
           rose="rose six", air="into the air", y1861="1861", tremont="Tremont", inch="Inch by", climbs="climbs", sleeping="sleeping", checking="checking", senator="senator",
           steeper="steeper", windows="the windows", eye="eye level", half="half a city", f320="320", m600="600 men", k6000="6000", signal="signal", notch="notch", open="open",
           swamp="swamp", lake="Lake", y1854="1854", twenty="twenty", wild="wild", pipes="sewer", bury="bury", lift="lift downtown", fourteen="fourteen", pullman="George",
           pane="pane", took="Then he took", wheels="wheels", car="The Pullman", travels="travels", allfrom="All from")
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
