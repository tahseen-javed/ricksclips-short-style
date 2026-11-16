#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 02: the Gimli Glider (Air Canada 143, 1983).
usage: build_short.py <project folder>   (reads audio/words.json, writes short.json + audio/music.mp3)

Five sets 70 units apart: SKY (sea of clouds; hook jet at x -18, story jet at x 0), CK cockpit,
HG hangar (the metric mix-up), LK luck field (glider, old air base), GM Gimli racetrack (the landing).
The jet is four copies of one puppet (jetK, jetA, jetH, jetG) so nothing teleports in view; anything
that changes sets moves at least 0.3 s after a dissolve, while the camera is elsewhere."""
import json, os, sys, subprocess
import scene_base as SB
from scene_base import *

SB.X.clear(); SB.X.update(SKY=0, CK=70, HG=140, LK=210, GM=280)
HERE = os.path.dirname(os.path.abspath(__file__))


def put(cid, name, at, h, face="default", flip=False):
    c = dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face)
    if flip: c["flip"] = True
    chars.append(c)


def rel(s, phrase, tok=False):
    """time of a phrase (or of one script word given as its joined tokens, '177' for 1.77) from the shot start"""
    t = WORDS["words"][WN.index(phrase)]["t0"] if tok else say(phrase)
    return round(t - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


# ================================================================== SETS
# ---- SKY: a sea of clouds (top at 1.5), cloud banks at the far edge, low puffs in front
box("SKY", 0, 0, -10, [68, 1.5, 60], texture="cloud.jpg", repeat=[9, 8])
for x in (-27, -13, 1, 15, 28): plane("SKY", "cloud.png", x, 0.6, -38, 15, 7.7)
for x, y, z, w in ((-24, 2.6, -16, 8), (-9, 5.6, -24, 10), (-30, 8.5, -28, 9), (9, 3.0, -15, 8), (15, 7.8, -27, 11), (1, 10, -32, 12), (-17, 9.5, -22, 7)):
    plane("SKY", "cloud.png", x, y, z, w, w * 0.51)
for x, z, w in ((-22, 5, 5), (-14.5, 6.5, 6), (-3.5, 5.5, 5), (4.5, 7, 6)): plane("SKY", "cloud.png", x, 0.4, z, w, w * 0.51)

# ---- CK: cockpit (dark floor, panel wall with portholes, console whose gauges face the camera)
box("CK", 0, 0, -1, [16, 0.02, 12], color="#5d6482")
wall("CK", 0, 0, -1.6, [16, 4.4, 0.3], "panel.jpg", [6, 2])
for x in (-2.7, 2.7): plane("CK", "porthole.png", x, 1.5, -1.43, 1.0, 1.0)
box("CK", 0, 0, 0.75, [4.4, 0.95, 0.7], color="#66708f"); box("CK", 0, 0.95, 0.75, [4.5, 0.08, 0.78], color="#424a66")
plane("CK", "gauges.png", 0, 0.06, 1.115, 3.2, 0.87)

# ---- HG: hangar apron (square hangar so the roof never shades its front), METRIC poster
box("HG", 0, 0, -3, [34, 0.02, 26], texture="concrete.jpg", repeat=[10, 8])
house("HG", 0, -12, [14, 8, 14], "#7d8799", color="#c9cfda")
plane("HG", "metric.png", -3.6, 1.0, -4.93, 2.4, 3.2)
for x in (-4.5, 0, 4.5): plane("HG", "porthole.png", x, 4.6, -4.93, 1.4, 1.4)
crate("HG", -7.0, 0, -2.6); crate("HG", -6.85, 0.75, -2.65, 0.55, 15); barrel("HG", 7.4, -1.6); barrel("HG", 8.1, -2.3)
tree("HG", -13, -6, 1.5); tree("HG", 13, -6, 1.4, "#4f8f4a")

# ---- LK: sunny field, the old air-base tower, sparkles of luck
house("LK", 4.8, -9, [3.2, 6.5, 3.2], "#56606f", color="#e2d9c6")
tree("LK", -7, -6, 1.4); tree("LK", -11, -9, 1.7, "#4f8f4a"); tree("LK", 10.5, -7, 1.5); post("LK", 8.0, -4.5, 4.2, "#d8d8d8")
for x, y, s_ in ((-2.5, 1.9, 0.45), (-0.2, 2.35, 0.35), (1.1, 1.55, 0.4), (-1.7, 0.6, 0.3), (2.3, 2.6, 0.3)): plane("LK", "sparkle.png", x, y, 0.2, s_, s_)

# ---- GM: Gimli runway turned racetrack (asphalt, centre dashes, kerbs), FAMILY DAY banner, tents
box("GM", 0, 0, -3, [64, 0.03, 9], texture="asphalt.jpg", repeat=[24, 4])
for x in range(-30, 31, 4): box("GM", x, 0.03, -3, [2.0, 0.012, 0.22], color="#f2efe6")
for i, x in enumerate(range(-16, 17)): box("GM", x, 0.03, 1.75, [1.0, 0.14, 0.4], color="#e04848" if i % 2 else "#f4f1ea")
post("GM", -3.6, -8.6, 4.4); post("GM", 3.6, -8.6, 4.4); plane("GM", "famday.png", 0, 2.9, -8.55, 7.0, 1.4)
house("GM", -9, -12, [3.4, 2.6, 3.4], "#d8453c", color="#f4efe6"); house("GM", 9, -12.5, [3.4, 2.6, 3.4], "#e8b23a", color="#f4efe6")
house("GM", 15, -11, [3.4, 2.6, 3.4], "#3f7fd0", color="#f4efe6")
tree("GM", -16, -10, 1.6); tree("GM", -21, -6, 1.4, "#4f8f4a"); tree("GM", 20, -8, 1.5)

# ================================================================== CHARACTERS
put("jetK", "jet", pos("SKY", -18, 4.2, 0), 2.0); put("jetA", "jet", pos("SKY", 0, 4.2, 0), 2.0)
put("jetH", "jet", pos("HG", 2.6, 0, -1.5), 2.0, face="park"); put("jetG", "jet", pos("GM", -16, 7, -3), 2.0, face="glide")
human("cap", "cap", pos("CK", -0.5, 0, 0.1)); human("fo", "fo", pos("CK", 0.5, 0, 0.1)); human("tech", "tech", pos("HG", -2.2, 0, 0.6), face="happy")
human("mom", "mom", pos("GM", -1.5, 0, 2.6), face="happy"); human("dad", "dad", pos("GM", -0.3, 0, 2.8), face="happy")
put("tank", "tank", pos("CK", 4.3, 0, 0.2), 1.5)
put("k1", "kart1", pos("GM", -9, 0, -1.2), 0.9); put("k2", "kart2", pos("GM", 8, 0, -4.6), 0.9, flip=True); put("k3", "kart3", pos("GM", -4, 0, -2.6), 0.9)
for cid, name, h in (("n177big", "n177", 1.4), ("n177", "n177", 0.75), ("n08", "n08", 0.75), ("cmp", "cmp", 1.6), ("crew", "crew", 1.1), ("alt", "alt", 1.3),
                     ("cal83", "cal83", 1.6), ("cal08", "cal08", 1.5), ("flt", "flt", 0.8), ("broken", "broken", 0.45), ("badge", "badge", 0.9),
                     ("gimli", "gimli", 1.7), ("dots", "dots", 1.0), ("flame1", "flame", 1.1), ("flame2", "flame", 0.85), ("hearts", "hearts", 1.1),
                     ("slam", "slam", 1.1), ("poofK1", "poof", 0.9), ("poofK2", "poof", 0.9), ("poof1A", "poof", 0.8), ("poof2A", "poof", 0.8),
                     ("poof3", "poof", 1.2), ("ques", "ques", 0.6), ("glider", "glider", 0.9)):
    sticker(cid, name, h)

# ================================================================== SHOTS
# ---- 0-1 hook (SKY, x -18): the wrong number pops up, both engines die, the jet becomes a glider
s = shot("0", target="jetK", hw=0.78, yaw=10, pitch=4, zoom=7, pan=(-8, 4), fy=0.02)
show(s, 0.25, "n177big", pos("SKY", -17.7, 6.55, 0.4), hop=0.15)
s = shot("turned", out="dissolve", target="jetK", hw=0.62, yaw=-8, pitch=6, zoom=-5, pan=(8, -2), fy=0.04)
act(s, 0.0, "jetK", face="dead", shake=0.7)
show(s, 0.05, "poofK1", pos("SKY", -19.0, 3.95, 0.35)); show(s, 0.15, "poofK2", pos("SKY", -18.0, 4.15, 0.3))
g = rel(s, "into")
act(s, g, "jetK", face="glide", pose=dict(head=6)); go(s, g, "jetK", pos("SKY", -17.2, 3.5, 0), 1.2, walk=False)
hide(s, g + 0.1, "n177big"); hide(s, g + 0.2, "poofK1"); hide(s, g + 0.3, "poofK2")

# ---- 2-5 the story jet (SKY, x 0): date, flight, people, altitude
s = shot("July", target="jetA", hw=0.5, yaw=12, pitch=5, zoom=6, pan=(10, 2), fy=0.06)
show(s, 0.2, "cal83", pos("SKY", 2.7, 6.3, 0.5), hop=0.15)
s = shot("Air Canada", target="jetA", hw=0.95, yaw=-10, pitch=3, zoom=6, pan=(-8, 0), fy=0.02)
hide(s, 0.05, "cal83"); show(s, 0.15, "flt", pos("SKY", -1.0, 6.45, 0.45))
s = shot("Sixtyone", target="jetA", hw=1.5, yaw=8, pitch=2, zoom=5, pan=(-12, 0), fy=0.0)
hide(s, 0.05, "flt"); show(s, 0.12, "crew", pos("SKY", -0.4, 6.3, 0.5))
s = shot("cruising", target="jetA", hw=0.7, yaw=-12, pitch=6, zoom=4, pan=(10, 0), fy=0.04)
hide(s, 0.05, "crew"); show(s, 0.15, "alt", pos("SKY", -2.4, 6.2, 0.5))

# ---- 6-7 the engines quit, then total silence (the music cuts out)
s = shot("One engine", target="jetA", hw=0.85, yaw=6, pitch=4, zoom=7, pan=(0, -6), fy=0.02)
hide(s, 0.0, "alt"); act(s, 0.05, "jetA", face="eng1", shake=0.7); show(s, 0.1, "poof1A", pos("SKY", -1.0, 3.95, 0.4))
o = rel(s, "Then the other"); act(s, o, "jetA", face="dead", shake=0.9); show(s, o + 0.05, "poof2A", pos("SKY", 0.2, 4.2, 0.3))
s = shot("Total silence", out="dissolve", anchor=pos("SKY", 0.4, 5.6, 0), dist=24, yaw=-6, pitch=8, zoom=-3, pan=(4, 0), fy=0.1)
hide(s, 0.2, "poof1A"); hide(s, 0.3, "poof2A"); show(s, 0.25, "dots", pos("SKY", 2.6, 6.3, 0.4))
act(s, 0.1, "jetA", pose=dict(head=4)); go(s, 0.1, "jetA", pos("SKY", 0.8, 3.4, 0), 1.4, walk=False)

# ---- 8-10 cockpit (CK): blank fuel gauges, the nearly empty tank, the big question
s = shot("The fuel gauges", anchor=pos("CK", 0, 1.0, 1.12), dist=4.6, yaw=8, pitch=4, zoom=5, pan=(-6, 0), fy=0.0)
hide(s, 0.3, "dots"); act(s, 0.0, "cap", face="shocked"); act(s, 0.1, "fo", face="nervous")
b = rel(s, "Broken"); show(s, b, "broken", pos("CK", -0.45, 0.28, 1.2), hop=0.12); act(s, b + 0.1, "cap", face="confused", pose=dict(head=6))
s = shot("Nobody knew", target="tank", hw=0.55, yaw=-8, pitch=4, zoom=6, pan=(8, 0), fy=0.05)
act(s, 0.4, "tank", shake=0.5)
s = shot("How does", out="dissolve", target="cap", hw=0.3, yaw=6, pitch=3, zoom=7, pan=(-6, 4), fy=0.1)
act(s, 0.0, "cap", face="confused", pose=dict(head=8)); show(s, 0.25, "ques", pos("CK", 0.0, 1.72, 0.35))

# ---- 11-16 hangar (HG): Canada goes metric, the first metric jet, the wrong number, half the fuel
s = shot("You see", anchor=pos("HG", -1.0, 2.0, -2.0), dist=16, yaw=10, pitch=6, zoom=4, pan=(8, 0), fy=0.04)
show(s, 0.3, "cap", pos("LK", -1.2, 0, 0.5), hop=0); show(s, 0.3, "fo", pos("LK", 1.4, 0, 0.6), hop=0)
act(s, 0.32, "cap", face="happy", pose=dict(head=0)); act(s, 0.32, "fo", face="happy")
hide(s, 0.3, "broken"); hide(s, 0.3, "ques"); act(s, 0.2, "tech", face="happy", pose=dict(armL=110))
s = shot("and the Boeing", target="jetH", hw=0.85, yaw=-10, pitch=4, zoom=6, pan=(-8, 0), fy=0.15)
show(s, rel(s, "first"), "badge", pos("HG", 4.6, 1.5, -1.0), hop=0.15)
s = shot("But the fuel", target="tech", hw=0.26, yaw=8, pitch=3, zoom=6, pan=(-6, 2), fy=0.08)
act(s, 0.0, "tech", face="confused", pose=dict(armL=0, armR=-60))
n = rel(s, "177", tok=True); show(s, n, "n177", pos("HG", -1.55, 0.12, 0.8), hop=0.12); act(s, n, "tech", face="smug")
s = shot("pounds per", target="n177", hw=0.8, yaw=-6, pitch=2, zoom=5, pan=(4, 0), fy=0.0)
s = shot("instead of", anchor=pos("HG", -0.95, 0.55, 0.8), dist=6.4, yaw=6, pitch=3, zoom=4, pan=(-6, 0), fy=0.05)
k = rel(s, "08", tok=True); show(s, k, "n08", pos("HG", -0.35, 0.12, 0.8), hop=0.12)
act(s, k, "n177", face="x", shake=0.6); act(s, k, "tech", face="shocked")
s = shot("So they took", out="dissolve", anchor=pos("HG", 0.4, 1.8, -0.3), dist=11, yaw=-8, pitch=6, zoom=-4, pan=(10, 4), fy=0.05)
hide(s, 0.0, "n177"); hide(s, 0.0, "n08"); hide(s, 0.2, "badge"); show(s, 0.25, "cmp", pos("HG", -0.6, 0.8, 0.9), hop=0.15)
act(s, 0.2, "jetH", face="default", pose=dict(head=-6)); go(s, 0.2, "jetH", pos("HG", 14, 6.5, -1.5), 2.2, walk=False)

# ---- 17-19 luck (LK): the captain's glider, the co-pilot's old air base, Gimli
s = shot("But luck", anchor=pos("LK", 0.1, 1.2, 0.5), dist=8.5, yaw=10, pitch=5, zoom=5, pan=(8, 0), fy=0.1)
hide(s, 0.3, "cmp"); act(s, 0.1, "cap", pose=dict(armR=-30)); act(s, 0.2, "fo", pose=dict(armL=30))
s = shot("The captain", target="cap", hw=0.28, yaw=8, pitch=3, zoom=6, pan=(8, 4), fy=0.1)
show(s, 0.0, "glider", pos("LK", -4.2, 2.0, 0.3), hop=0); go(s, 0.05, "glider", pos("LK", -0.3, 2.25, 0.3), 1.3, walk=False)
act(s, 0.2, "cap", pose=dict(armR=-150))
s = shot("And the copilot", out="dissolve", anchor=pos("LK", 2.2, 2.3, -3.0), dist=12, yaw=12, pitch=4, zoom=4, pan=(-8, 0), fy=0.05)
act(s, 0.0, "cap", pose=dict(armR=0)); go(s, 0.05, "fo", pos("LK", 3.4, 0, -2.0), 1.2)
act(s, 1.3, "fo", face="smug", pose=dict(armR=-135))
gi = rel(s, "Gimli"); show(s, gi, "gimli", pos("LK", 1.6, 0, -1.6), hop=0.15); act(s, gi, "fo", face="happy")

# ---- 20-26 Gimli (GM): racetrack, family day, karts, the silent landing, the slam, fire, everyone lives
s = shot("One problem", anchor=pos("GM", -0.8, 1.5, -2.5), dist=15, yaw=14, pitch=9, zoom=4, pan=(10, 0), fy=0.0)
hide(s, 0.3, "glider"); hide(s, 0.3, "gimli")
go(s, 0.0, "k1", pos("GM", 6, 0, -1.2), 2.3, walk=False); go(s, 0.1, "k2", pos("GM", -7, 0, -4.6), 2.2, walk=False); go(s, 0.2, "k3", pos("GM", 9, 0, -2.6), 2.1, walk=False)
s = shot("And today", anchor=pos("GM", -0.9, 1.8, 1.0), dist=9, yaw=-10, pitch=4, zoom=6, pan=(-8, 2), fy=0.08)
act(s, 0.1, "mom", pose=dict(armR=-150)); act(s, 0.25, "dad", pose=dict(armL=150)); act(s, 0.75, "mom", pose=dict(armR=-115)); act(s, 0.9, "dad", pose=dict(armL=115))
for c_, x_, z_ in (("k1", 22, -1.2), ("k3", 24, -2.6), ("k2", -22, -4.6)): go(s, 0.1, c_, pos("GM", x_, 0, z_), 1.0, walk=False)
s = shot("Gokarts", anchor=pos("GM", 4.0, 0.5, 0.3), dist=6, yaw=0, pitch=2, zoom=8, pan=(-14, 0), fy=0.05)
show(s, 0.0, "k1", pos("GM", -6, 0, 0.6), hop=0); go(s, 0.03, "k1", pos("GM", 5.0, 0, 0.6), 1.0, walk=False)
show(s, 0.0, "k3", pos("GM", -8, 0, -0.4), hop=0); go(s, 0.2, "k3", pos("GM", 7.0, 0, -0.4), 1.2, walk=False)
show(s, 0.0, "k2", pos("GM", 7, 0, -1.4), hop=0); go(s, 0.1, "k2", pos("GM", -6.0, 0, -1.4), 1.1, walk=False)
s = shot("The plane drops", anchor=pos("GM", -3.0, 3.0, -2.0), dist=16, yaw=-12, pitch=3, zoom=3, pan=(-6, 6), fy=0.05)
go(s, 0.0, "jetG", pos("GM", -2.5, 1.4, -3.0), rel(s, "The nose"), walk=False); act(s, 0.0, "jetG", pose=dict(head=6))
act(s, 0.4, "mom", face="shocked", pose=dict(armR=0)); act(s, 0.5, "dad", face="shocked", pose=dict(armL=0))
for c_, t_ in (("k1", 0.3), ("k3", 0.35), ("k2", 0.4)): act(s, t_, c_, face="shocked")
s = shot("The nose", target="jetG", hw=0.6, yaw=8, pitch=5, zoom=8, pan=(0, -8), fy=0.0)
go(s, 0.0, "jetG", pos("GM", 0.5, 0, -3.0), 0.35, walk=False); act(s, 0.35, "jetG", face="slam", pose=dict(head=7), shake=1.0)
show(s, 0.35, "slam", pos("GM", 2.6, 1.4, -2.4), hop=0.15); show(s, 0.38, "poof3", pos("GM", -1.6, 0, -2.6), hop=0.1)
s = shot("Fire bursts", target="jetG", hw=0.75, yaw=-6, pitch=3, zoom=6, pan=(6, 0), fy=0.05)
hide(s, 0.05, "slam"); show(s, 0.1, "flame1", pos("GM", 2.5, 0, -2.5), hop=0.2); show(s, 0.22, "flame2", pos("GM", 3.2, 0, -2.35), hop=0.2)
act(s, 0.2, "jetG", face="dead")
s = shot("And everyone", out="dissolve", anchor=pos("GM", 0.3, 1.6, -1.0), dist=14, yaw=10, pitch=5, zoom=-4, pan=(8, 2), fy=0.08)
hide(s, 0.05, "flame1"); hide(s, 0.1, "flame2"); show(s, 0.05, "poof3", pos("GM", 2.6, 0.1, -2.3), hop=0.1)
act(s, 0.1, "jetG", face="saved", pose=dict(head=4)); show(s, 0.3, "hearts", pos("GM", 0.6, 2.5, -2.2), hop=0.2)
for c_, t_ in (("mom", 0.15), ("dad", 0.2)): act(s, t_, c_, face="happy", pose=dict(armR=-160, armL=160))
for c_ in ("k1", "k2", "k3"): act(s, 0.25, c_, face="default")
show(s, 0.0, "jetA", pos("SKY", -1.0, 4.4, 0), hop=0); act(s, 0.0, "jetA", face="default", pose=dict(head=0))
show(s, 0.0, "jetK", pos("SKY", -18, 4.2, 0), hop=0); act(s, 0.0, "jetK", face="default", pose=dict(head=0))

# ---- 27-28 the jet flies on until 2008; back to the hook for the loop
s = shot("That same jet", out="dissolve", target="jetA", hw=0.7, yaw=10, pitch=4, zoom=5, pan=(-8, 0), fy=0.02)
go(s, 0.0, "jetA", pos("SKY", 0.6, 4.6, 0), 2.0, walk=False); show(s, 0.3, "cal08", pos("SKY", 2.4, 6.5, 0.5), hop=0.15)
s = shot("All because", target="jetK", hw=0.78, yaw=10, pitch=4, zoom=7, pan=(-8, 4), fy=0.02)
show(s, rel(s, "trusted"), "n177big", pos("SKY", -17.7, 6.55, 0.4), hop=0.15)
w = rel(s, "wrong number#2"); act(s, w, "n177big", face="x", shake=0.6); act(s, w, "jetK", face="eng1")

# ================================================================== SPEC
spec = {
    "fps": 30,
    "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json",
    "captions": {"wordsPer": 1},
    "font": "fonts/Montserrat-ExtraBold.ttf",
    "contactShadow": 0.6,
    "moods": {
        "day": {"sun": {"azimuth": 35, "elevation": 50, "color": "#ffe0b5", "intensity": 2.4},
                "sky": {"top": "#5f86d8", "horizon": "#f2b98a"},
                "fill": {"sky": "#8ea2ff", "ground": "#6a3b6e", "intensity": 1.1}},
        "dusk": {"sun": {"azimuth": -20, "elevation": 38, "color": "#ffa66e", "intensity": 2.3},
                 "sky": {"top": "#3f4f9e", "horizon": "#f0926a"},
                 "fill": {"sky": "#7d7ee0", "ground": "#5e3668", "intensity": 1.35}, "exposure": 1.12},
    },
    "lighting": [{"t": 0, "mood": "day"}, {"t": "say:One engine", "mood": "dusk", "fade": 0.6}, {"t": "say:The fuel gauges", "mood": "day", "fade": 0.5}, {"t": "say:You see", "mood": "day", "fade": 0.8},
                 {"t": "say:One problem", "mood": "dusk", "fade": 0.8}, {"t": "say:That same jet", "mood": "day", "fade": 0.6}],
    "ground": {"texture": TEX + "grass.jpg", "repeat": [525, 525], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 5},
    "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music synthesised to the word timings (engine spool-downs, true silence, boom, fire, resolve)
cues = dict(quit1=say("One engine"), quit2=say("Then the other"), sil=say("Total silence"), explain=say("You see"), luck=say("But luck"),
            drop=say("The plane drops"), slam=say("The nose") + 0.35, fire=say("Fire bursts"), lives=say("And everyone"))
cp, wav = os.path.join(P, "audio", "cues.json"), os.path.join(P, "audio", "music.wav")
json.dump(cues, open(cp, "w"))
subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), wav, "%.2f" % (DURATION + 0.6), cp], check=True)
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
