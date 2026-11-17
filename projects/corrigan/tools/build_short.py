#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 05: Wrong Way Corrigan.
usage: build_short.py <project folder>
Six sets 70 units apart: AF the New York airfield at dawn, SK the open sky over the Atlantic (the hook), HG the
hangar where inspectors turn him down, CK the cockpit (fuel tank in front, gasoline on the floor), DB a field near
Dublin, NY the pier and the ticker-tape parade street.  Set changes are cuts or dissolves; cards leave one frame
before a cut; the last shot repeats the first for the loop."""
import json, os, sys, subprocess
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(AF=0, SK=70, HG=140, CK=210, DB=280, NY=350)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


def cut(s, phrase, *who):                                    # hide just before the next shot starts on `phrase`
    for w in who: hide(s, rel(s, phrase) - 0.04, w)


# ================================================================== SETS
box("AF", 0, 0, -6, [70, 0.06, 44], texture="grass.jpg", repeat=[18, 12]); box("AF", 0, 0.06, 1.0, [60, 0.03, 4.2], color="#6e7078")
for x in range(-26, 27, 4): box("AF", x, 0.09, 1.0, [1.6, 0.02, 0.22], color="#f4f1e6")
house("AF", -11, -9, [10, 5.2, 8], "#5f6f6a", color="#c9c2b4"); house("AF", 12, -11, [8, 4.4, 7], "#7a5f52", color="#d8cfc0")
box("AF", 6, 0, -8, [1.6, 4.2, 1.6], color="#d8d2c4"); box("AF", 6, 4.2, -8, [2.4, 1.1, 2.4], color="#8fb3cc"); box("AF", 6, 5.3, -8, [2.8, 0.2, 2.8], color="#5f6f6a")
barrel("AF", -5, -3); barrel("AF", -4.3, -3.5); plane("AF", "skyny.png", 0, -1, -26, 96, 42)

box("HG", 0, 0, -2, [26, 0.06, 20], color="#9c9a96"); box("HG", 0, 0, -10, [26, 9, 0.4], color="#7d8794")
for x in (-6, -2, 2, 6): box("HG", x, 0.06, -9.75, [3.7, 7.2, 0.12], color="#94a0ad")
for sg in (-1, 1): box("HG", sg * 12.8, 0, -2, [0.4, 9, 20], color="#76808c")
for z in (-8, -4, 0): box("HG", 0, 8.0, z, [26, 0.35, 0.35], color="#5a6370")
for x in (-5, 0, 5): box("HG", x, 6.4, -3, [0.9, 0.35, 0.9], color="#ffe08a")
box("HG", -7, 0, -8.8, [4, 1.0, 1.2], texture="wood.jpg", repeat=[2, 1]); crate("HG", -9.5, 0, -6.5); crate("HG", -8.8, 0.75, -6.8, 0.6)
barrel("HG", 8, -6.5); barrel("HG", 8.9, -5.8)

box("CK", 0, 0, 0, [4.4, 0.06, 5], color="#4a3c36"); box("CK", 0, 0, -1.6, [4.4, 3.0, 0.15], color="#7a4e34")
box("CK", 0, 1.5, -1.52, [1.2, 0.8, 0.04], color="#9fd3f0"); box("CK", 2.2, 0, 0, [0.15, 3.0, 5], color="#8a5a3c")
box("CK", 0, 0, -0.75, [1.0, 0.7, 0.5], color="#3d2e28"); box("CK", 0, 0, 1.0, [2.0, 1.0, 0.35], color="#5c3d2a"); plane("CK", "dash.png", 0, 0.14, 1.19, 1.8, 0.63)

box("DB", 0, 0, -6, [70, 0.06, 44], texture="grass.jpg", repeat=[18, 12])
for x, z, sz in ((-8, -6, [10, 0.7, 0.45]), (7, -9, [12, 0.7, 0.45]), (-13, -1.5, [0.45, 0.7, 9])): box("DB", x, 0.06, z, sz, color="#9a958c")
house("DB", -9, -13, [4.6, 2.6, 3.4], "#c9a35a", color="#f3efe4"); house("DB", 6, -16, [4.2, 2.4, 3.2], "#b8924c", color="#efe9dc")
tree("DB", -15, -10, 1.3); tree("DB", 12, -12, 1.5, "#4f8f45"); tree("DB", 16, -5, 1.1); plane("DB", "skyie.png", 0, -1, -26, 96, 42)

box("NY", 2, 0, -1, [32, 0.06, 16], color="#7b7d84"); box("NY", 2, 0.06, -5.6, [32, 0.16, 2.8], color="#bdb7ab")
for x, h in ((-11, 9), (-6, 12), (-1, 10), (4, 14), (9, 8.5), (14, 11)):
    box("NY", x, 0, -9.4, [4.8, h, 4.4], texture="facade.jpg", repeat=[2, round(h / 2.4)]); box("NY", x, h, -9.4, [5.0, 0.4, 4.6], color="#d8cfc0")
for x in (-9, -3, 3, 9): post("NY", x, -4.4, 3.2, "#2f3440")
plane("NY", "skyst.png", 2, -1, -30, 110, 48)
box("NY", -24, 0, 1.5, [9, 0.45, 5], texture="wood.jpg", repeat=[4, 2]); crate("NY", -26, 0.45, 2.2); barrel("NY", -22, 2.8, y=0.45)
for x in (-28, -20):
    for z in (-0.8, 3.8): post("NY", x, z, 1.1, "#5a4636")

# ================================================================== CHARACTERS
put("sock", "windsock", pos("AF", 3.2, 0.06, -3.5), 2.4); put("sign", "signpost", pos("AF", -1.6, 0.06, 3.6), 2.3)
put("robinA", "robin", pos("AF", -6, 0.09, 1.0), 2.0, "fly"); put("sun", "sun", pos("AF", 7, 0.5, -16), 3.2)
human("dougA", "doug", PARK, face="happy"); human("insp1A", "insp1", PARK, face="neutral")
put("robinS", "robin", pos("SK", 0, 6.0, 0), 2.2, "fly")
CLOUDS = (("cl1", -5.5, 5.0, -3, 2.0), ("cl2", 4.5, 8.4, -6, 2.8), ("cl3", 8.5, 4.2, -1.5, 1.6), ("cl4", -9, 8.6, -9, 3.4), ("cl5", 1.5, 3.4, 2.6, 1.3), ("cl6", -2.5, 9.6, -2, 1.5))
for cid, x, y, z, h in CLOUDS: put(cid, "cloud", pos("SK", x, y, z), h)
put("robinH", "robin", pos("HG", 0.6, 0.06, -4.2), 2.6)
human("dougH", "doug", pos("HG", -2.4, 0.06, -1.0), face="happy")
human("insp1", "insp1", pos("HG", -10, 0.06, 0.2), face="neutral"); human("insp2", "insp2", pos("HG", 10, 0.06, 0.6), face="neutral")
put("tank", "tank", pos("CK", 0, 1.0, 1.05), 1.25); human("dougC", "doug", pos("CK", 0, 0.06, 0), face="happy"); put("gas", "gasoline", pos("CK", 0, -0.75, 0.5), 0.7)
put("robinD", "robin", pos("DB", -7.5, 2.8, 0), 2.0, "fly"); human("dougD", "doug", PARK, face="happy")
for cid, x, z, h, kw in (("sh1", 1.6, 1.8, 0.9, {}), ("sh2", 4.0, -0.6, 0.8, dict(flip=True)), ("sh3", -2.6, 2.0, 0.85, dict(flip=True))): put(cid, "sheep", pos("DB", x, 0.06, z), h, **kw)
put("cf1", "cloud", PARK, 1.0, "face"); put("cf2", "cloud", PARK, 0.85, "face")
put("ship", "liner", pos("NY", -48, -0.54, -4.2), 3.6); put("car", "car", pos("NY", -10, 0.06, 0.8), 1.3)
human("dougP", "doug", pos("NY", -10.3, 0.06, 0.4), face="happy")
CROWD = (("mom", "mom"), ("dad", "dad"), ("tech", "tech"), ("vik", "vik"), ("sA", "sailA"), ("sC", "sailC"), ("sD", "sailD"), ("capt", "capt"))
for k, (cid, pp) in enumerate(CROWD): human(cid, pp, pos("NY", -6.5 + k * 1.5, 0.22, -4.9 + (k % 2) * 0.5), face="happy")
TAPES = ("t1", "t2", "t3", "t4", "t5", "t6")
for cid in TAPES: sticker(cid, "tape", 1.1)
for cid, name, h in (("banned", "banned", 1.0), ("robtag", "robtag", 1.6), ("price", "price", 0.85), ("unsound", "unsound", 0.85), ("noview", "noview", 0.32),
                     ("gasb", "gas", 0.6), ("punch", "punch", 0.5), ("screw", "screwdriver", 0.9), ("kept", "kept", 0.75), ("name", "name", 1.0), ("cal38", "cal38", 1.4),
                     ("plan", "plan", 1.3), ("clock", "clock", 1.8), ("dublin", "dublin", 0.8), ("compass", "compass", 1.0), ("needle", "needle", 0.49),
                     ("wrong", "wrong", 0.5), ("badvis", "badvis", 0.55), ("licence", "licence", 0.95), ("parade", "parade", 1.2), ("lindy", "lindy", 1.4),
                     ("wwc", "wwc", 0.95), ("purpose", "purpose", 0.38), ("plan2", "plan", 1.05), ("hearts", "hearts", 0.8), ("spark", "sparkle", 0.6)):
    sticker(cid, name, h)
for cid, name, h, tilt in (("d1", "denied", 0.6, -10), ("d2", "denied", 0.6, 8), ("d3", "denied", 0.6, -4), ("susp", "susp", 0.5, -12), ("official", "official", 0.42, -10)):
    put(cid, name, PARK, h, pose=dict(head=tilt))
next(c for c in chars if c["id"] == "banned")["pose"] = dict(head=-8)

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):               # a card at a safe spot of the frame, never near an edge
    (ax, ay, az), d = s["anchor"], s["distance"]
    show(s, at, who, [round(ax + dx * 0.41 * d, 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az + dz, 3)], hop=0.12)


def drift(s, end, speed=1.0):                                # clouds stream past the plane for the whole shot
    dur = rel(s, end) if end else DURATION - say(s["_phrase"])
    for cid, x, y, z, h in CLOUDS:
        show(s, 0.0, cid, pos("SK", x + 6, y, z), hop=0); go(s, 0.02, cid, pos("SK", x + 6 - 12 * speed, y, z), max(0.3, dur - 0.08), walk=False)


def confetti(s, x0, end):
    dur = rel(s, end)
    for k, cid in enumerate(TAPES):
        show(s, 0.0, cid, pos("NY", x0 - 5 + 2 * k, 7.5 + (k % 3) * 1.2, -2.6 + (k % 2) * 2.4), hop=0)
        go(s, 0.02, cid, pos("NY", x0 - 4.4 + 2 * k, -0.6, -2.6 + (k % 2) * 2.4), max(0.3, dur - 0.08), walk=False)


HOOK = dict(anchor=pos("SK", 0.3, 6.9, 0), dist=12, yaw=-12, pitch=5, zoom=10, pan=(6, 0), fy=0.0)
# ---- 0-2 hook: the plane already over the ocean with BANNED! slammed on frame 1; takes off "for California"; lands in Dublin
s = shot("0", out="cut", **HOOK)
drift(s, "So he took off"); card(s, 0.0, "banned", 0.25); hide(s, rel(s, "So he took off") - 0.04, "banned")
s = shot("So he took off", out="cut", anchor=pos("AF", 0, 1.6, 1.0), dist=14, yaw=18, pitch=-2, zoom=8, pan=(-6, 0))
go(s, 0.0, "robinA", pos("AF", 3, 0.09, 1.0), 0.8, walk=False); go(s, 0.82, "robinA", pos("AF", 13, 4.6, 1.0), 1.0, walk=False)
act(s, rel(s, "California"), "sign", shake=0.5)
s = shot("and landed in Dublin", out="cut", anchor=pos("DB", -1.2, 1.5, 0), dist=13, yaw=-14, pitch=4, zoom=8, pan=(6, 0))
go(s, 0.0, "robinD", pos("DB", 0.2, 0.06, -0.4), 1.0, walk=False); act(s, 1.0, "robinD", face="default", shake=0.4)
for c_ in ("sh1", "sh3"): act(s, 1.0, c_, face="shocked", shake=0.4)
card(s, rel(s, "Dublin"), "dublin", 0.27)

# ---- 3-6 the hangar: a used 1929 Curtiss Robin for $900, inspectors say too unsound, DENIED x3
s = shot("His plane was", anchor=pos("HG", -0.6, 2.0, -2.6), dist=15, yaw=10, pitch=6, zoom=6, pan=(-8, 0))
hide(s, 0.3, "dublin"); card(s, max(0.05, rel(s, "1929") - 0.1), "robtag", 0.27); cut(s, "that cost", "robtag")
s = shot("that cost him", anchor=pos("HG", -2.4, 1.45, -1.0), dist=5.5, yaw=-18, pitch=3, zoom=10, pan=(6, 2))
act(s, 0.0, "dougH", face="smug"); card(s, rel(s, "900"), "price", 0.22, 0.12); cut(s, "Inspectors", "price")
s = shot("Inspectors called it", out="whip", anchor=pos("HG", 0.2, 1.7, -1.4), dist=11, yaw=16, pitch=5, zoom=8, pan=(-6, 0))
go(s, 0.0, "insp1", pos("HG", -0.6, 0.06, 0.2), 1.0); go(s, 0.1, "insp2", pos("HG", 2.4, 0.06, 0.6), 1.0)
u_ = rel(s, "unsound"); act(s, u_, "insp1", face="shocked"); act(s, u_, "insp2", face="confused"); act(s, u_, "robinH", shake=0.6)
act(s, 0.0, "dougH", face="happy"); card(s, u_, "unsound", 0.27); cut(s, "and turned", "unsound")
s = shot("and turned him", out="cut", anchor=pos("HG", -1.0, 1.4, -0.3), dist=7.5, yaw=-10, pitch=4, zoom=10, pan=(8, 0))
for k, (w_, dx, dy) in enumerate((("turned", -0.22, 0.27), ("again", 0.2, 0.12), ("again#2", -0.04, 0.0))):
    card(s, rel(s, w_), "d%d" % (k + 1), dy, dx, 0.6 + 0.05 * k); act(s, rel(s, w_), "insp1", face="shouting", pose=dict(armR=-150 if k % 2 == 0 else -40))
act(s, rel(s, "turned"), "dougH", face="nervous"); cut(s, "Extra fuel", "d1", "d2", "d3")

# ---- 7-11 the cockpit: tank blocks the view; over the open sea the floor floods; screwdriver; kept flying
s = shot("Extra fuel tanks", anchor=pos("CK", 0, 1.45, 0.6), dist=4.4, yaw=6, pitch=4, zoom=10, pan=(-4, 0))
go(s, rel(s, "blocked"), "dougC", pos("CK", -0.62, 0.06, 0), 0.35); act(s, rel(s, "blocked"), "dougC", face="confused")
card(s, rel(s, "whole view"), "noview", 0.3); cut(s, "Over the open", "noview")
s = shot("Over the open sea", out="cut", anchor=pos("SK", 0, 5.0, 0), dist=22, yaw=24, pitch=14, zoom=6, pan=(-8, 0))
drift(s, "the cockpit floor", 1.3); act(s, 0.0, "robinS", face="fly")
s = shot("the cockpit floor", anchor=pos("CK", 0, 0.75, 0.2), dist=4.5, yaw=-60, pitch=14, zoom=10, pan=(6, 2))
f_ = rel(s, "flooded"); go(s, max(0.0, f_ - 0.1), "gas", pos("CK", 0, -0.32, 0.5), 1.2, walk=False); act(s, f_, "dougC", face="shocked", shake=0.4)
card(s, rel(s, "gasoline"), "gasb", 0.24, 0.15)
s = shot("He punched a hole", out="cut", anchor=pos("CK", -0.3, 0.6, 0.3), dist=3.6, yaw=-32, pitch=20, zoom=10, pan=(6, 2))
hide(s, 0.3, "gasb"); p_ = rel(s, "punched"); show(s, 0.0, "screw", pos("CK", 0.1, 0.75, 0.6), hop=0.1)
go(s, p_ + 0.05, "screw", pos("CK", 0.1, -0.1, 0.6), 0.12, walk=False); card(s, p_ + 0.17, "punch", 0.02, 0.2, 0.5)
act(s, p_ + 0.17, "dougC", face="nervous"); go(s, rel(s, "screwdriver"), "gas", pos("CK", 0, -0.95, 0.5), 0.9, walk=False)
act(s, rel(s, "screwdriver") + 0.4, "dougC", face="smug"); cut(s, "and kept", "punch", "screw")
s = shot("and kept flying", out="cut", anchor=pos("SK", 0.8, 6.6, 0), dist=9, yaw=-24, pitch=-4, zoom=12, pan=(10, 0))
act(s, 0.0, "robinS", face="drip"); drift(s, "You see", 1.6); card(s, 0.15, "kept", 0.26); cut(s, "You see", "kept")

# ---- 12-15 the real story: New York, dawn, July 17 1938; flight plan Long Beach; 28 h 13 min
s = shot("You see", anchor=pos("AF", 0, 2.0, 0), dist=20, yaw=-20, pitch=10, zoom=6, pan=(12, 0))
act(s, 0.0, "robinS", face="fly"); show(s, 0.0, "robinA", pos("AF", 1.5, 0.09, -0.6), hop=0); act(s, 0.0, "robinA", face="default")
show(s, 0.0, "dougA", pos("AF", -3.5, 0.06, 1.6), hop=0); go(s, 0.1, "dougA", pos("AF", -0.8, 0.06, 1.2), 1.4)
card(s, rel(s, "Douglas"), "name", 0.27); cut(s, "left New York", "name")
s = shot("left New York", anchor=pos("AF", 0.4, 1.4, 0.4), dist=9, yaw=16, pitch=-3, zoom=10, pan=(-8, 2))
go(s, 0.0, "sun", pos("AF", 7, 4.2, -16), 3.0, walk=False); act(s, 0.1, "dougA", pose=dict(armR=-150), face="happy")
d_ = rel(s, "dawn"); hide(s, d_ + 0.3, "dougA"); act(s, d_ + 0.3, "robinA", face="fly", shake=0.3)
card(s, rel(s, "July"), "cal38", 0.22, -0.18); cut(s, "His flight plan", "cal38")
s = shot("His flight plan", out="cut", anchor=pos("AF", -1.0, 1.5, 0.6), dist=7, yaw=-12, pitch=3, zoom=10, pan=(6, 0))
show(s, 0.0, "insp1A", pos("AF", -2.0, 0.06, 1.2), hop=0); act(s, 0.2, "insp1A", pose=dict(armR=-120))
card(s, rel(s, "flight plan"), "plan", 0.2, 0.14); act(s, rel(s, "Long Beach"), "plan", shake=0.4)
s = shot("twentyeight", out="dissolve", anchor=pos("SK", 0, 6.6, 0), dist=14, yaw=30, pitch=4, zoom=8, pan=(-10, 0))
hide(s, 0.3, "plan"); drift(s, "he climbed out", 2.2); card(s, 0.1, "clock", 0.25); cut(s, "he climbed out", "clock")

# ---- 16-19 Dublin: climbs out, the wrong end of the compass needle, clouds, licence suspended
s = shot("he climbed out", anchor=pos("DB", 1.2, 1.3, 0.4), dist=9, yaw=20, pitch=4, zoom=8, pan=(-6, 0))
for c_ in ("sh1", "sh3"): act(s, 0.0, c_, face="default")
show(s, 0.05, "dougD", pos("DB", 1.4, 0.06, 0.0), hop=0.25); go(s, 0.45, "dougD", pos("DB", 2.2, 0.06, 1.1), 0.6)
s = shot("and said he had", anchor=pos("DB", 2.6, 1.4, 1.1), dist=6, yaw=-8, pitch=3, zoom=10, pan=(6, 2))
card(s, 0.1, "compass", 0.1, 0.2); card(s, 0.1, "needle", 0.1, 0.2, 0.36); w_ = rel(s, "wrong end")
act(s, 0.4, "needle", pose=dict(head=-25), ease=0.3); act(s, w_, "needle", pose=dict(head=180), ease=0.55)
act(s, w_, "dougD", face="sneaky"); card(s, w_ + 0.35, "wrong", 0.3, -0.05); cut(s, "Clouds", "compass", "needle", "wrong")
s = shot("Clouds", anchor=pos("DB", 2.4, 1.5, 1.1), dist=7.5, yaw=14, pitch=4, zoom=8, pan=(-6, 0))
o_ = max(0.4, min(1.6, rel(s, "Officials suspended") - 0.35))
show(s, 0.0, "cf1", pos("DB", 0.2, 1.5, 2.0), hop=0.15); go(s, 0.1, "cf1", pos("DB", 1.4, 1.6, 2.0), o_, walk=False)
show(s, 0.1, "cf2", pos("DB", 4.8, 2.3, 1.6), hop=0.15); go(s, 0.2, "cf2", pos("DB", 3.5, 2.2, 1.6), o_ - 0.1, walk=False)
act(s, 0.1, "dougD", pose=dict(armR=-150)); card(s, rel(s, "Bad visibility"), "badvis", 0.28); cut(s, "Officials suspended", "cf1", "cf2", "badvis")
s = shot("Officials suspended", out="cut", anchor=pos("DB", 2.2, 1.5, 1.1), dist=6.5, yaw=-16, pitch=2, zoom=10, pan=(6, 0))
act(s, 0.0, "dougD", pose=dict(armR=0), face="happy"); card(s, 0.05, "licence", 0.17, 0.18)
x_ = rel(s, "suspended"); card(s, x_, "susp", 0.17, 0.18, 0.45); act(s, x_, "dougD", face="shocked", shake=0.4)

# ---- 20-25 home: the ship docks, the ticker-tape parade, bigger than Lindbergh's, Wrong Way Corrigan, never admitted
s = shot("but only until", anchor=pos("NY", -25, 2.0, -1), dist=22, yaw=24, pitch=6, zoom=8, pan=(-10, 0))
hide(s, 0.3, "licence"); hide(s, 0.3, "susp"); go(s, 0.0, "ship", pos("NY", -27, -0.54, -4.2), max(0.6, rel(s, "Then New York") - 0.2), walk=False)
s = shot("Then New York", anchor=pos("NY", -3, 3.0, -1.5), dist=20, yaw=-18, pitch=10, zoom=6, pan=(12, 2))
e_ = rel(s, "bigger than"); go(s, 0.0, "car", pos("NY", -2.5, 0.06, 0.8), e_ - 0.1, walk=False); go(s, 0.0, "dougP", pos("NY", -2.8, 0.06, 0.4), e_ - 0.1, walk=False)
act(s, 0.0, "dougP", pose=dict(armR=-150)); confetti(s, -3, "bigger than")
for k, (cid, _) in enumerate(CROWD): act(s, 0.1 + 0.07 * k, cid, pose=dict(armR=-150, armL=150))
card(s, rel(s, "parade"), "parade", 0.28); cut(s, "bigger than", "parade")
s = shot("bigger than", out="whip", anchor=pos("NY", -1.0, 1.7, -3.6), dist=9, yaw=12, pitch=5, zoom=8, pan=(-8, 0))
confetti(s, -1, "They called"); card(s, 0.1, "lindy", 0.24); show(s, 0.3, "hearts", pos("NY", -1.2, 2.3, -3.2), hop=0.12)
for k, (cid, _) in enumerate(CROWD): act(s, 0.15 + 0.06 * k, cid, pose=dict(armR=-100, armL=100))
cut(s, "They called", "lindy", "hearts")
s = shot("They called him", anchor=pos("NY", -2.8, 1.8, 0.4), dist=7, yaw=-10, pitch=-8, zoom=10, pan=(6, 2))
act(s, 0.0, "dougP", pose=dict(armR=-150, armL=150), face="happy"); card(s, rel(s, "Wrong Way") - 0.05, "wwc", 0.27)
show(s, rel(s, "Corrigan#2"), "spark", pos("NY", -1.7, 2.9, 1.0), hop=0.1); cut(s, "He never once", "wwc", "spark")
s = shot("He never once", anchor=pos("NY", -2.8, 1.5, 0.4), dist=4.6, yaw=16, pitch=2, zoom=12, pan=(-6, 0))
act(s, 0.0, "dougP", pose=dict(armR=0, armL=0), face="sneaky"); p_ = rel(s, "purpose")
act(s, p_, "dougP", pose=dict(armR=-100, armL=100)); card(s, p_, "purpose", 0.27); cut(s, "Because officially", "purpose")
s = shot("Because officially", out="cut", anchor=pos("NY", -2.8, 1.5, 0.4), dist=6.2, yaw=-18, pitch=3, zoom=8, pan=(8, 0))
act(s, 0.0, "dougP", pose=dict(armR=0, armL=0), face="smug"); card(s, 0.05, "plan2", 0.16, 0.18)
card(s, rel(s, "officially"), "official", 0.16, 0.18, 0.45)

# ---- 26 loop: the first shot again
s = shot("never flying", **HOOK); s["start"] = round(say("never flying"), 3)
act(s, 0.0, "robinS", face="fly"); drift(s, None)
for s in shots:
    if "anchor" in s: s.setdefault("frameY", 0.0)                # anchor at the frame centre (the stage default puts it 12 % high)

# ================================================================== SPEC
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6,
    "moods": {"day": {"sun": {"azimuth": 40, "elevation": 46, "color": "#ffe4c0", "intensity": 2.4},
                      "sky": {"top": "#5b8ee0", "horizon": "#f6c79a"}, "fill": {"sky": "#9aaeff", "ground": "#6a4b6e", "intensity": 1.15}}},
    "lighting": [{"t": 0, "mood": "day"}],
    "ground": {"texture": TEX + "water.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky38.jpg", "blur": 4}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
cues = dict(took=say("So he took off"), land=say("landed in Dublin"), denied=[say("turned"), say("again"), say("again#2")], tanks=say("Extra fuel"),
            sea=say("Over the open sea"), flood=say("flooded"), punch=say("punched"), kept=say("kept flying"), yousee=say("You see"), leftny=say("left New York"),
            plan=say("flight plan"), hours=say("twentyeight"), climbed=say("he climbed out"), wrong=say("wrong end"), clouds=say("Clouds"), susp=say("suspended"),
            ship=say("ship docked"), parade=say("Then New York"), lindy=say("bigger than"), wwc=say("Wrong Way"), never=say("He never once"),
            purpose=say("on purpose"), because=say("Because officially"), loop=say("never flying"), end=DURATION)
cp, wav = os.path.join(P, "audio", "cues.json"), os.path.join(P, "audio", "music.wav")
json.dump(cues, open(cp, "w"))
subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), wav, "%.2f" % (DURATION + 0.4), cp], check=True)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", os.path.join(P, "audio", "music.mp3")], check=True)
os.remove(wav)

# ---- sanity report: shot timing + actions that overrun or overlap
starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
print("shot  start   dur  phrase")
for k, s in enumerate(shots):
    end = starts[k + 1] if k + 1 < len(shots) else DURATION
    s["_dur"] = end - starts[k]
    print("S%02d  %6.2f %5.2f  %s" % (k, starts[k], s["_dur"], s["_phrase"]))
    if s["_dur"] < 0.7: print("   ! very short shot (mostly glide)")
keys = {}
for k, s in enumerate(shots):
    for a in s["actions"]:
        if "to" in a: keys.setdefault(a["who"], []).append((starts[k] + a["at"], a["over"], k, a["to"]))
        if a["at"] > s["_dur"] + 0.25: print("   ! S%02d action at %.2f s runs past the shot (%.2f s): %s %s" % (k, a["at"], s["_dur"], a["who"], list(a)[2:]))
for who, ks in keys.items():
    ks.sort()
    for (t0, ov, k0, _), (t1, ov1, k1, _) in zip(ks, ks[1:]):
        if t0 + ov > t1 + 0.06: print("   ! %s: move from S%02d (%.2f+%.2f s) overlaps next move in S%02d at %.2f s" % (who, k0, t0, ov, k1, t1))
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
