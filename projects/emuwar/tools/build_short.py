#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 09: the Great Emu War (1932).
usage: build_short.py <project folder>
Five sets 70 units apart: WF wheat farm (war area x 0, farm area x 8; hook + loop), OB red outback, PH the Defence Minister's
office, AC army camp, BO bounty office.  Every shot moves (dolly + orbit); cards are fitted to the safe box; the frame check
prints CUT / SIGNCUT / INSIDE flags.  The last line "And that is how, in 1932," ends on the hook frame so the video loops."""
import json, os, sys, subprocess, math
import scene_base as base
from scene_base import *

base.X.clear(); base.X.update(WF=0, OB=70, PH=140, AC=210, BO=280)
HERE = os.path.dirname(os.path.abspath(__file__)); PARK = base.PARK
ASP = json.load(open(os.path.join(P, "aspect.json")))


def put(cid, name, at, h, face="default", **kw):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face, **kw))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


def room(loc, wallc, img, floor, rep=(4, 4), sidec=None):     # interior: floor, back wall + picture, two side walls
    box(loc, 0, 0, -1, [12, 0.06, 10], texture=floor, repeat=list(rep)); box(loc, 0, 0, -5, [12, 6.2, 0.3], color=wallc)
    for sg in (-1, 1): box(loc, sg * 5.85, 0, -1, [0.3, 6.2, 10], color=sidec or wallc)
    plane(loc, img, 0, 0.06, -4.82, 11, 5.04)


# ================================================================== SETS
# WF wheat farm: red dirt, rows of golden wheat, windmill, farmhouse with a tin roof, fence; war area at x 0, farm area at x 8
plane("WF", "skyday.png", 0, -1, -30, 96, 42); box("WF", 0, 0, -4, [44, 0.05, 26], texture="dirt.jpg", repeat=[11, 7])
for z, off in ((-6.5, 0.0), (-9.0, 3.7)):
    for k in range(-3, 4): plane("WF", "wheatrow.png", k * 7.4 + off, 0.05, z, 7.5, 1.63)
plane("WF", "windmill.png", -7.5, 0.05, -12, 2.6, 5.94); house("WF", 10, -14, [6, 3.6, 5], "#b8bcc4", color="#f0e0c0")
for x in range(-16, 17, 2): post("WF", x, -5.2, 1.0, "#a07050")
box("WF", 0, 0.6, -5.2, [32, 0.1, 0.08], color="#c09060")
# OB red outback in drought
plane("OB", "outback.png", 0, -0.5, -20, 34, 14.9); box("OB", 0, 0, -4, [44, 0.05, 26], texture="redsand.jpg", repeat=[11, 7])
# PH the Defence Minister's office; AC the army camp; BO the bounty office
room("PH", "#aa7850", "office.png", "wood.jpg", sidec="#9a6a44")
box("PH", 0.6, 0, -3.9, [2.6, 0.78, 1.0], color="#7a4a2c"); box("PH", 0.6, 0.78, -3.9, [2.7, 0.06, 1.1], color="#a06a40")
plane("AC", "skyday.png", 0, -1, -30, 96, 42); box("AC", 0, 0, -4, [44, 0.05, 26], texture="dirt.jpg", repeat=[11, 7])
for x, z in ((-6, -9), (-1.5, -10.5), (3.5, -9.5), (8, -11)): house("AC", x, z, [3.2, 2.2, 3.2], "#a89a6a", color="#c8b88a")
for x, z in ((-4.2, -6.0), (-3.4, -6.4), (5.0, -6.2)): props.append(dict(type="crate", pos=pos("AC", x, 0, z), size=0.8, color="#6e784c"))
post("AC", 6.5, -7.5, 5.0, "#e8e0d0")
room("BO", "#e2d6b4", "bountywall.png", "btiles.jpg", sidec="#d4c6a0")
plane("BO", "skyday.png", 0, -1, -30, 96, 42)

SIGNS = []                                                   # (name, world corners) of text painted on set pictures


def sign(nm, loc, plane_, rect, W=2400, Hh=1100):
    (x, y, z, pw, ph), (a, b, c, d) = plane_, rect; X0 = base.X[loc] + x
    SIGNS.append((nm, [[X0 + (u / W - 0.5) * pw, y + ph * (1 - v / Hh), z + 0.02] for u in (a, c) for v in (b, d)]))


ROOMP = (0, 0.06, -4.82, 11, 5.04)
sign("bountysign", "BO", ROOMP, (980, 250, 1420, 340)); sign("paywindow", "BO", ROOMP, (980, 370, 1420, 700)); sign("ozwall", "PH", ROOMP, (1000, 230, 1400, 520))

# ================================================================== CHARACTERS
G0, LG0 = pos("WF", -0.45, 0.06, 0.0), pos("WF", 0.5, 0.06, 0.35)
human("gunW", "gunner", G0, face="shouting"); put("lewisH", "lewis", LG0, 0.85)
put("emuH", "emu", PARK, 1.9, flip=True); put("truck", "truck", PARK, 1.1); put("emutank", "emutank", PARK, 2.0, flip=True)
for k in (4, 5): put("e%d" % k, "emu", PARK, 1.6, face="run", flip=True)
human("farmer", "farmer", pos("WF", 7.5, 0.06, -1.6), face="happy"); human("farmwife", "farmwife", pos("WF", 8.6, 0.06, -1.8), face="happy", h=1.7)
put("wheat1", "wheat", PARK, 1.4)
for k in (1, 2): put("e%d" % k, "emu", PARK, 1.7, face="run")
put("cashW", "cash", PARK, 0.8)
put("herd", "herd", pos("OB", -0.5, 0.05, -4.0), 1.1); put("e6", "emu", pos("OB", 1.2, 0.05, -1.8), 1.6, face="run"); put("e7", "emu", pos("OB", -1.5, 0.05, -1.4), 1.5, face="run")
human("pearce", "pearce", pos("PH", -0.4, 0.06, -2.6), face="neutral")
human("merA", "meredith", pos("AC", -0.95, 0.06, -2.4), face="happy"); human("gunA", "gunner", pos("AC", 0.0, 0.06, -2.6), face="happy")
human("gun2A", "gunner2", pos("AC", 0.95, 0.06, -2.4), face="happy")
for cid in ("lewisA1", "lewisA2"): put(cid, "lewis", PARK, 0.85)
put("ammoA", "ammo", PARK, 1.0)
human("clerk", "clerk", pos("BO", 0.55, 0.06, -3.0), face="happy"); human("farmB", "farmer", pos("BO", -0.6, 0.06, -2.6), face="happy")
for k in range(3): put("cashB%d" % k, "cash", PARK, 0.75)

# ================================================================== SHOTS
SH = {c["id"]: c["height"] for c in chars}
N_ = [0]


def card(s, at, who, dy=0.25, dx=0.0, dz=0.3):               # a card at a safe spot of the frame, never near an edge
    (ax, ay, az), d = s["anchor"], s["distance"]; y = math.radians(s["yaw"]); w = dx * 0.41 * d
    show(s, at, who, [round(ax + w * math.cos(y) + dz * math.sin(y), 3), round(ay + dy * 0.728 * d - SH[who] / 2, 3), round(az - w * math.sin(y) + dz * math.cos(y), 3)], hop=0.12)


REQ = []


def tag(s, at, name, dy=0.25, dx=0.0, dz=0.3, wf=0.24, hf=0.17, tilt=0, face="default"):   # placed later by the card fit
    N_[0] += 1; cid = "%s_%d" % (name, N_[0]); c = dict(id=cid, puppet="puppets/" + name, pos=PARK, height=0.1, face=face)
    if tilt: c["pose"] = dict(head=tilt)
    chars.append(c); s["_tags"].append(cid); REQ.append((s, at, cid, name, dy, dx, dz, wf, hf, c)); return cid


def temp(s, *who): s["_tags"].extend(who)


def S(start, **kw):
    s = shot(start, **kw); s["_tags"] = []; s["glide"] = "dolly"; s["pan"] = [v * 5 for v in s["pan"]]; return s


def hook_state(s):
    show(s, 0.0, "gunW", G0, hop=0); show(s, 0.0, "lewisH", LG0, hop=0); act(s, 0.0, "lewisH", face="default")
    act(s, 0.0, "gunW", face="shouting", pose=dict(armR=-70, armL=0)); show(s, 0.0, "emuH", PARK, hop=0)
    return tag(s, 0.0, "atwar", 0.31, 0.0, 0.4, wf=0.3)


HOOK = dict(anchor=pos("WF", 0.15, 1.35, 0.1), dist=6.8, yaw=-8, pitch=6, zoom=-5, pan=(3, 0))
EH = pos("WF", 1.45, 0.06, 0.25)
# ---- 0-2 hook: Australia goes to war -> the enemy had feathers -> and the enemy won
s = S("0", out="cut", **HOOK); hook_state(s); act(s, rel(s, "war"), "gunW", shake=0.3)
s = S("The enemy had feathers", out="cut", anchor=pos("WF", 0.6, 1.3, 0.2), dist=6.6, yaw=10, pitch=4, zoom=8, pan=(-4, 0))
show(s, 0.0, "emuH", EH); act(s, 0.0, "emuH", face="default"); act(s, 0.0, "gunW", face="shocked", shake=0.3)
fe = rel(s, "feathers"); tag(s, fe, "feathers", 0.1, 0.2, 0.6, wf=0.12); tag(s, fe, "feathert", 0.32)
s = S("And the enemy won", out="cut", anchor=pos("WF", 0.65, 1.3, 0.25), dist=6.8, yaw=-12, pitch=6, zoom=8, pan=(4, 0))
wn = rel(s, "won"); act(s, 0.0, "emuH", face="happy", shake=0.3); act(s, 0.0, "gunW", face="nervous")
tag(s, wn, "trophy", 0.12, 0.12, 0.6, wf=0.1); tag(s, wn, "emuwins", 0.32, tilt=-7); act(s, wn, "emuH", face="happy", shake=0.4)

# ---- 3-7 Campion 1932: drought, 20,000 emus onto veterans' wheat farms, wheat wrecked, farmers beg for help
s = S("Campion", out="cut", anchor=pos("WF", 8.0, 1.8, -2.6), dist=10.5, yaw=6, pitch=8, zoom=7, pan=(-8, 0))
act(s, 0.0, "farmer", face="happy", pose=dict(armR=-150)); tag(s, 0.05, "ozmap", 0.24, -0.08, wf=0.3, hf=0.3); tag(s, rel(s, "November"), "y1932", 0.3, 0.2, 0.5, wf=0.16)
s = S("A drought pushes", out="cut", anchor=pos("OB", 0.0, 1.6, -2.6), dist=9.5, yaw=-10, pitch=6, zoom=7, pan=(-6, 0))
dr_ = rel(s, "onto wheat farms") - 0.1; go(s, 0.02, "herd", pos("OB", 0.3, 0.05, -4.0), dr_, walk=False)
go(s, 0.02, "e6", pos("OB", 1.4, 0.05, -1.8), dr_, walk=False); go(s, 0.02, "e7", pos("OB", -1.0, 0.05, -1.4), dr_, walk=False)
tag(s, 0.05, "drought", 0.33, tilt=-6); tag(s, rel(s, "twenty thousand"), "e20k", 0.18)
s = S("onto wheat farms", out="cut", anchor=pos("WF", 8.3, 1.4, -2.0), dist=8.0, yaw=12, pitch=6, zoom=8, pan=(-9, 0))
show(s, 0.0, "wheat1", pos("WF", 9.3, 0.06, -2.5)); show(s, 0.0, "e1", pos("WF", 9.7, 0.06, -1.2), hop=0); go(s, 0.02, "e1", pos("WF", 9.0, 0.06, -1.3), 0.8, walk=False)
act(s, 0.0, "farmer", face="shocked", pose=dict(armR=-150, armL=150), shake=0.3); act(s, 0.0, "farmwife", face="shocked")
tag(s, rel(s, "veterans"), "vets", 0.32)
s = S("The wheat gets wrecked", out="cut", anchor=pos("WF", 9.4, 1.2, -2.0), dist=5.4, yaw=-12, pitch=6, zoom=9, pan=(4, 0))
show(s, 0.0, "e1", pos("WF", 8.7, 0.06, -1.5), hop=0); act(s, 0.0, "e1", face="happy")
for cid in ("farmer", "farmwife"): show(s, 0.0, cid, PARK, hop=0); wr = rel(s, "wrecked")
act(s, wr, "wheat1", face="wrecked", shake=0.5); act(s, wr, "e1", shake=0.4); tag(s, wr, "wrecked", 0.32, tilt=-8); temp(s, "wheat1")
s = S("The farmers beg", out="cut", anchor=pos("WF", 8.0, 1.4, -1.7), dist=6.4, yaw=10, pitch=4, zoom=8, pan=(-5, 0))
show(s, 0.0, "e1", PARK, hop=0); show(s, 0.0, "farmer", pos("WF", 7.5, 0.06, -1.6), hop=0); show(s, 0.0, "farmwife", pos("WF", 8.6, 0.06, -1.8), hop=0)
for cid in ("farmer", "farmwife"): act(s, 0.0, cid, face="shouting", pose=dict(armR=-150, armL=150), shake=0.4)
tag(s, 0.1, "help", 0.32, wf=0.2)

# ---- 8-11 Minister Pearce approves; the army sends 3 soldiers, 2 Lewis guns, 10,000 rounds
s = S("Defence Minister Pearce", out="cut", anchor=pos("PH", -0.1, 1.8, -2.8), dist=6.0, yaw=0, pitch=4, zoom=8, pan=(-6, 0))
act(s, 0.0, "pearce", face="smug", pose=dict(armR=-80)); tag(s, 0.05, "pearcet", 0.33, wf=0.27); ma = rel(s, "military answer")
act(s, ma, "pearce", face="shouting", pose=dict(armR=-150), shake=0.4); tag(s, ma, "approved", 0.12, 0.0, 0.5, tilt=-8)
s = S("The army sends", out="cut", anchor=pos("AC", 0.0, 1.5, -2.5), dist=7.6, yaw=-10, pitch=6, zoom=8, pan=(6, 0))
for k, cid in enumerate(("merA", "gunA", "gun2A")): act(s, 0.1 * k, cid, face="happy", pose=dict(armR=-150), shake=0.3)
tag(s, rel(s, "three soldiers"), "soldiers3", 0.33)
s = S("Two Lewis", out="cut", anchor=pos("AC", 0.0, 1.2, -2.0), dist=6.6, yaw=10, pitch=6, zoom=8, pan=(-6, 0))
show(s, 0.0, "lewisA1", pos("AC", -0.65, 0.06, -1.5)); show(s, 0.12, "lewisA2", pos("AC", 0.75, 0.06, -1.5))
for cid in ("gunA", "gun2A"): act(s, 0.0, cid, face="shocked")
tag(s, 0.1, "guns2", 0.34)
s = S("Ten thousand rounds", out="cut", anchor=pos("AC", -0.5, 1.2, -2.2), dist=6.4, yaw=-12, pitch=6, zoom=8, pan=(0, 0))
for cid in ("gunA", "gun2A", "lewisA1", "lewisA2"): show(s, 0.0, cid, PARK, hop=0)
show(s, 0.0, "ammoA", pos("AC", 0.05, 0.06, -2.0)); act(s, 0.0, "merA", face="happy", pose=dict(armR=-120)); tag(s, 0.1, "r10k", 0.34)

# ---- 12-16 a week of firing: 2,500 rounds gone, pulled out; back again: 9,860 rounds, 986 birds, 10 bullets per emu
s = S("One week later", out="cut", anchor=pos("WF", 0.5, 1.3, 0.0), dist=8.4, yaw=10, pitch=6, zoom=6, pan=(0, 0))
act(s, 0.0, "lewisH", face="fire", shake=0.5); act(s, 0.0, "gunW", face="shouting", pose=dict(armR=-70)); show(s, 0.0, "emuH", PARK, hop=0)
dr_ = rel(s, "The soldiers are") - 0.1
show(s, 0.0, "e4", pos("WF", 1.7, 0.06, -0.8), hop=0); go(s, 0.02, "e4", pos("WF", 1.4, 0.06, -0.8), dr_, walk=False)
tag(s, 0.05, "week", 0.32, -0.15, wf=0.14); g_ = rel(s, "2500 rounds"); tag(s, g_, "r2500", 0.32, 0.12, 0.5, tilt=-6, wf=0.22); act(s, g_, "e4", face="happy", shake=0.4)
s = S("The soldiers are", out="cut", anchor=pos("WF", 0.0, 1.1, -1.6), dist=8.5, yaw=-10, pitch=6, zoom=6, pan=(0, 0))
show(s, 0.0, "gunW", PARK, hop=0); show(s, 0.0, "lewisH", PARK, hop=0); show(s, 0.0, "e4", PARK, hop=0)
show(s, 0.0, "truck", pos("WF", 0.35, 0.06, -1.6), hop=0); go(s, 0.05, "truck", pos("WF", -0.35, 0.06, -1.6), rel(s, "They come back") - 0.2, walk=False)
tag(s, rel(s, "pulled"), "pulled", 0.3, tilt=-7)
s = S("They come back", out="cut", anchor=pos("WF", 0.0, 1.1, -1.6), dist=8.5, yaw=8, pitch=6, zoom=7, pan=(0, 0))
show(s, 0.0, "truck", pos("WF", -0.35, 0.06, -1.6), hop=0); go(s, 0.02, "truck", pos("WF", 0.35, 0.06, -1.6), 0.7, walk=False)
tag(s, 0.05, "round2", 0.34); tag(s, rel(s, "Same result"), "same", 0.15, tilt=7)
s = S("9860 rounds", out="cut", anchor=pos("WF", 0.5, 1.3, 0.0), dist=9.2, yaw=-8, pitch=4, zoom=6, pan=(0, 0))
show(s, 0.0, "truck", PARK, hop=0); show(s, 0.0, "gunW", G0, hop=0); show(s, 0.0, "lewisH", LG0, hop=0); act(s, 0.0, "lewisH", face="fire", shake=0.6)
act(s, 0.0, "gunW", face="shouting", pose=dict(armR=-70)); show(s, 0.0, "e5", pos("WF", 1.55, 0.06, -0.6), hop=0); act(s, 0.0, "e5", face="run")
tag(s, 0.05, "r9860", 0.34); tag(s, 0.1, "boom", 0.12, 0.05, 0.6, wf=0.14); b9 = rel(s, "986 birds"); tag(s, b9, "b986", 0.2, 0.0, 0.5)
s = S("Ten bullets", out="cut", anchor=pos("WF", 1.5, 1.1, -0.6), dist=5.4, yaw=12, pitch=4, zoom=9, pan=(-5, 0))
act(s, 0.0, "e5", face="default", shake=0.3); show(s, 0.0, "lewisH", PARK, hop=0); show(s, 0.0, "gunW", PARK, hop=0); tag(s, 0.05, "per10", 0.31, wf=0.18)

# ---- 17-18 Major Meredith admits it: emus face machine guns like tanks
s = S("You see", out="cut", anchor=pos("AC", -1.0, 1.5, -2.4), dist=5.6, yaw=-12, pitch=4, zoom=9, pan=(5, 0))
show(s, 0.0, "ammoA", PARK, hop=0)
act(s, 0.0, "merA", face="nervous", pose=dict(armR=-100)); tag(s, 0.05, "majort", 0.33, wf=0.26)
s = S("Emus could face", out="cut", anchor=pos("WF", 0.55, 1.4, 0.1), dist=9.4, yaw=12, pitch=6, zoom=6, pan=(0, 0))
show(s, 0.0, "e5", PARK, hop=0); show(s, 0.0, "gunW", G0, hop=0); show(s, 0.0, "lewisH", LG0, hop=0); show(s, 0.0, "emutank", pos("WF", 1.45, 0.06, 0.0)); act(s, 0.0, "lewisH", face="fire", shake=0.5)
act(s, 0.0, "gunW", face="shocked", shake=0.3); tag(s, rel(s, "tanks"), "tanks", 0.32, tilt=-7); temp(s, "emutank")

# ---- 19-22 no more soldiers: a bounty per bird instead; 1934: 57,000 bounties, 58 times the machine guns
s = S("So the government", out="cut", anchor=pos("PH", -0.2, 1.8, -2.8), dist=5.8, yaw=-4, pitch=4, zoom=9, pan=(5, 0))
act(s, 0.0, "pearce", face="shouting", pose=dict(armR=-150, armL=150), shake=0.3); tag(s, 0.1, "nosoldiers", 0.32, tilt=-6)
s = S("It paid farmers", out="cut", anchor=pos("BO", 0.0, 1.7, -2.8), dist=6.8, yaw=10, pitch=4, zoom=6, pan=(3, 0))
act(s, 0.0, "clerk", face="happy", pose=dict(armR=-90)); act(s, 0.0, "farmB", face="happy", pose=dict(armR=-150))
tag(s, 0.2, "cash", 0.05, 0.0, 0.6, wf=0.12, hf=0.12); tag(s, rel(s, "bounty"), "bounty", 0.34); tag(s, rel(s, "No machine guns"), "noguns", 0.17, tilt=-6)
s = S("Six months", out="cut", anchor=pos("BO", 0.0, 1.9, -2.6), dist=7.6, yaw=-6, pitch=6, zoom=6, pan=(0, 0))
for k, x in enumerate((-0.9, -0.15, 1.1)): show(s, 0.1 + 0.15 * k, "cashB%d" % k, pos("BO", x, 0.06, -2.0))
act(s, 0.0, "farmB", face="happy", pose=dict(armR=-150, armL=150), shake=0.3); tag(s, 0.05, "y1934", 0.31, -0.14, wf=0.15); tag(s, rel(s, "57000"), "b57k", 0.31, 0.1, 0.5, wf=0.24)
s = S("Almost fiftyeight", out="cut", anchor=pos("WF", 8.0, 1.4, -1.7), dist=6.6, yaw=-10, pitch=6, zoom=8, pan=(5, 0))
show(s, 0.0, "cashW", pos("WF", 8.05, 0.06, -1.2))
for cid in ("farmer", "farmwife"): act(s, 0.0, cid, face="happy", pose=dict(armR=-150, armL=150), shake=0.3)
tag(s, 0.05, "x58", 0.31, wf=0.18); temp(s, "cashW")

# ---- 23-24 bullets lost, cash won ... and that is how, in 1932, (loops into the hook)
s = S("Bullets lost", out="cut", anchor=pos("WF", 0.15, 1.3, 0.1), dist=7.2, yaw=10, pitch=4, zoom=8, pan=(-5, 0))
show(s, 0.0, "gunW", G0, hop=0); show(s, 0.0, "lewisH", LG0, hop=0); act(s, 0.0, "lewisH", face="default"); act(s, 0.0, "gunW", face="nervous", pose=dict(armR=0))
tag(s, 0.05, "lost", 0.33, tilt=-6, wf=0.24); cw = rel(s, "Cash won"); tag(s, cw, "won", 0.17, wf=0.22); tag(s, cw, "cash", 0.02, 0.24, 0.6, wf=0.1, hf=0.1)
s = S("And that is how", **HOOK); hook_state(s); tag(s, rel(s, "1932#2"), "y1932", 0.12, 0.2, 0.6, wf=0.14)
for cid in ("truck", "e4", "e5"): show(s, 0.0, cid, PARK, hop=0)
for s in shots:
    if "anchor" in s: s.setdefault("frameY", 0.0)

starts = [0.0 if s["start"] == 0 else say(s["_phrase"]) for s in shots]
for k, s in enumerate(shots): s["_dur"] = (starts[k + 1] if k + 1 < len(shots) else DURATION) - starts[k]


def drift_t(dur, tl):                                        # stage.js driftTable: the camera arrives fast, then settles
    n = max(2, int(round(dur * 30))); acc = 0.0; f = tl * 30
    for i in range(1, n):
        if i > f: break
        u = (i + 0.5) / n; ss = min(1, max(0, (u - 0.15) / 0.25)); ss = ss * ss * (3 - 2 * ss); acc += (1 + 0.7 * (1 - ss)) / 30
    return acc


# ---- every card / temporary character leaves one frame before the next shot
for k, s in enumerate(shots):
    if k + 1 < len(shots):
        for cid in s["_tags"]: hide(s, round(starts[k + 1] - starts[k] - 0.04, 3), cid)
    s.pop("_tags")

# ---- camera auto-fit: widen a shot (distance x1.06 per step, at most x1.7) until no character, prop card or set sign is cut
W_, H_, T0, ASPH = 1080, 1920, math.tan(math.radians(20)), 0.46
def norm(v): l = math.sqrt(sum(c * c for c in v)); return [c / l for c in v]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cam(s, tl):
    te = drift_t(s["_dur"], tl); y, p = math.radians(s["yaw"]), math.radians(s["pitch"]); dr = [math.sin(y) * math.cos(p), math.sin(p), math.cos(y) * math.cos(p)]
    fwd = [-c for c in dr]; right = norm(cross(fwd, [0, 1, 0])); up = cross(right, fwd)
    sc = math.exp(math.log1p(s["zoom"] / 100) * te); d = s["distance"] / sc; wpp = 2 * d * T0 / H_
    dx, dy = s["pan"][0] * te, s["pan"][1] * te
    look = [a - r * dx * wpp + u_ * dy * wpp for a, r, u_ in zip(s["anchor"], right, up)]
    return [l + c * d for l, c in zip(look, dr)], fwd, right, up
def proj(c, P_):
    pos_, f, r, u = c; v = [a - b for a, b in zip(P_, pos_)]; z = dot(v, f)
    if z <= 0.1: return None
    return 0.5 + dot(v, r) / (z * T0 * W_ / H_) / 2, 0.5 - dot(v, u) / (z * T0) / 2
def partial(pts, lo=0.03, hi=0.97, bot=0.985):
    if any(q is None for q in pts): return False
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    return max(xs) > 0.01 and min(xs) < 0.99 and max(ys) > 0.01 and min(ys) < 0.99 and (min(xs) < lo or max(xs) > hi or min(ys) < lo or max(ys) > bot)
def shot_cuts(k, s):
    n = 0
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        c = cam(s, tl); T = starts[k] + tl
        for cid, tr in track.items():
            p0 = [e for e in tr if e[0] <= T][-1][1]
            if p0[1] < -50: continue
            h, w = SH[cid], WID[cid]
            if partial([proj(c, [p0[0] + sx * w / 2, p0[1] + sy * h, p0[2]]) for sx in (-1, 1) for sy in (0, 1)]): n += 1
        for nm, corners in SIGNS:
            if partial([proj(c, q) for q in corners], 0.01, 0.99, 0.99): n += 1
    return n
track = {c["id"]: [(-1.0, c["pos"])] for c in chars}
for k, s in enumerate(shots):
    for a_ in s["actions"]:
        if "to" in a_: track[a_["who"]].append((starts[k] + a_["at"] + a_.get("over", 0) * 0.5, a_["to"]))
for v in track.values(): v.sort(key=lambda e: e[0])
WID = {c["id"]: c["height"] * (ASP.get(c["puppet"].split("/")[1], ASPH)) for c in chars}
for k, s in enumerate(shots):
    d0 = s["distance"]
    while shot_cuts(k, s) and s["distance"] < d0 * 1.35: s["distance"] = round(s["distance"] * 1.06, 3)
    if s["distance"] != d0: print("   autofit S%02d distance %.1f -> %.1f" % (k, d0, s["distance"]))

# ---- fit every card into the safe box (x 7-87 %, y 7-64 %, above the captions) for its whole time on screen, zoom + pan included
for (s, at, cid, name, dy, dx, dz, wf, hf, c) in REQ:
    d = s["distance"]; h = min(wf * d / ASP[name], hf * 0.728 * d); samples = [at + (s["_dur"] - at) * u for u in (0, 0.25, 0.5, 0.75, 1.0)]
    for it in range(60):
        hfr, wfr, ok = h / (0.728 * d), h * ASP[name] / (0.41 * d), True
        for tl in samples:
            te = drift_t(s["_dur"], tl); sc = math.exp(math.log1p(s["zoom"] / 100) * te); px, py = s["pan"][0] * te / 1080, s["pan"][1] * te / 1920
            xc, yc = 0.5 + dx * sc + px, 0.5 - dy * sc + py
            if xc - wfr * sc / 2 < 0.10 or xc + wfr * sc / 2 > 0.85 or yc - hfr * sc / 2 < 0.08 or yc + hfr * sc / 2 > 0.63: ok = False; break
        if ok: break
        dx += (-0.03 - dx) * 0.15; dy += (0.15 - dy) * 0.15; h *= 0.97
    c["height"] = round(h, 3); SH[cid] = c["height"]; card(s, at, cid, dy, dx, dz)


# ================================================================== SPEC
mood = lambda m, ph: {"t": round(say(ph), 3), "mood": m, "fade": 0.02}
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6,
    "moods": {"day": {"sun": {"azimuth": 40, "elevation": 46, "color": "#ffe8c8", "intensity": 2.4},
                      "sky": {"top": "#5b8ee0", "horizon": "#f6d6b0"}, "fill": {"sky": "#a0b4ff", "ground": "#6a4b6e", "intensity": 1.2}},
              "hot": {"sun": {"azimuth": 60, "elevation": 40, "color": "#ffcf9a", "intensity": 2.5}, "sky": {"top": "#e89a5a", "horizon": "#ffd9a0"}, "fill": {"sky": "#ffc8a0", "ground": "#8a4a3e", "intensity": 1.2}}},
    "lighting": [{"t": 0, "mood": "day"}, mood("hot", "A drought pushes"), mood("day", "onto wheat farms")],
    "ground": {"texture": TEX + "asphalt.jpg", "repeat": [175, 175], "size": 1400},
    "backdrop": {"image": "bg/sky.jpg", "blur": 4}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
CUE = dict(war="war", feathers="feathers", won="won", campion="Campion", y1932="November", drought="A drought pushes", e20k="twenty thousand",
           farms="onto wheat farms", vets="veterans", wrecked="wrecked", beg="The farmers beg", pearce="Defence Minister Pearce", answer="military answer",
           army="The army sends", three="three soldiers", guns="Two Lewis", rounds="Ten thousand rounds", week="One week later", gone="2500 rounds",
           pulled="The soldiers are", back="They come back", same="Same result", fired="9860 rounds", birds="986 birds", ten="Ten bullets", yousee="You see",
           emus="Emus could face", tanks="tanks", gov="So the government", paid="It paid farmers", bounty="bounty", noguns="No machine guns", six="Six months",
           b57="57000", x58="Almost fiftyeight", lost="Bullets lost", cash="Cash won", loop="And that is how", y1932b="1932#2")
cues = {k: say(v) for k, v in CUE.items()}; cues["end"] = DURATION
cp, wav = os.path.join(P, "audio", "cues.json"), os.path.join(P, "audio", "music.wav")
json.dump(cues, open(cp, "w"))
if os.environ.get("NO_MUSIC") != "1":
    subprocess.run([sys.executable, os.path.join(HERE, "make_music.py"), wav, "%.2f" % (DURATION + 0.4), cp], check=True)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-b:a", "192k", os.path.join(P, "audio", "music.mp3")], check=True)
    os.remove(wav)

# ---- sanity report: shot timing + actions that overrun or overlap
print("shot  start   dur  phrase")
for k, s in enumerate(shots):
    print("S%02d  %6.2f %5.2f  %s" % (k, starts[k], s["_dur"], s["_phrase"]))
    if s["_dur"] < 0.7: print("   ! very short shot")
keys = {}
for k, s in enumerate(shots):
    for a in s["actions"]:
        if a["at"] < 0: print("   ! S%02d negative action time %.2f: %s" % (k, a["at"], a["who"]))
        if "to" in a: keys.setdefault(a["who"], []).append((starts[k] + a["at"], a["over"], k, a["to"]))
        if a["at"] > s["_dur"] + 0.25: print("   ! S%02d action at %.2f s runs past the shot (%.2f s): %s %s" % (k, a["at"], s["_dur"], a["who"], list(a)[2:]))
for who, ks in keys.items():
    ks.sort()
    for (t0, ov, k0, _), (t1, ov1, k1, _) in zip(ks, ks[1:]):
        if t0 + ov > t1 + 0.06: print("   ! %s: move from S%02d (%.2f+%.2f s) overlaps next move in S%02d at %.2f s" % (who, k0, t0, ov, k1, t1))

# ---- frame check: project every visible character / card (engine camera maths, dolly glide) at 3 moments per shot
W_, H_, T0 = 1080, 1920, math.tan(math.radians(20))
ASPH = 0.46
def norm(v): l = math.sqrt(sum(c * c for c in v)); return [c / l for c in v]
def cross(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cam(s, tl):
    te = drift_t(s["_dur"], tl); y, p = math.radians(s["yaw"]), math.radians(s["pitch"]); dr = [math.sin(y) * math.cos(p), math.sin(p), math.cos(y) * math.cos(p)]
    fwd = [-c for c in dr]; right = norm(cross(fwd, [0, 1, 0])); up = cross(right, fwd)
    sc = math.exp(math.log1p(s["zoom"] / 100) * te); d = s["distance"] / sc; wpp = 2 * d * T0 / H_
    dx, dy = s["pan"][0] * te, s["pan"][1] * te
    look = [a - r * dx * wpp + u_ * dy * wpp for a, r, u_ in zip(s["anchor"], right, up)]
    return [l + c * d for l, c in zip(look, dr)], fwd, right, up
def proj(c, P_):
    pos_, f, r, u = c; v = [a - b for a, b in zip(P_, pos_)]; z = dot(v, f)
    if z <= 0.1: return None
    return 0.5 + dot(v, r) / (z * T0 * W_ / H_) / 2, 0.5 - dot(v, u) / (z * T0) / 2
track = {c["id"]: [(-1.0, c["pos"])] for c in chars}
for k, s in enumerate(shots):
    for a in s["actions"]:
        if "to" in a: track[a["who"]].append((starts[k] + a["at"] + a.get("over", 0) * 0.5, a["to"]))
for v in track.values(): v.sort(key=lambda e: e[0])
WID = {c["id"]: c["height"] * (ASP.get(c["puppet"].split("/")[1], ASPH)) for c in chars}
flags = 0
for k, s in enumerate(shots):
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        c = cam(s, tl); T = starts[k] + tl
        for cid, tr in track.items():
            p0 = [e for e in tr if e[0] <= T][-1][1]
            if p0[1] < -50: continue
            h, w = SH[cid], WID[cid]; pts = [proj(c, [p0[0] + sx * w / 2, p0[1] + sy * h, p0[2]]) for sx in (-1, 1) for sy in (0, 1)]
            if any(q is None for q in pts): continue
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            inside = max(xs) > 0 and min(xs) < 1 and max(ys) > 0 and min(ys) < 1
            if inside and (min(xs) < 0.03 or max(xs) > 0.97 or min(ys) < 0.03 or max(ys) > 0.985):
                flags += 1; print("   CUT S%02d t=%.2f %-14s x %.2f..%.2f y %.2f..%.2f" % (k, tl, cid, min(xs), max(xs), min(ys), max(ys)))
for k, s in enumerate(shots):
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        c = cam(s, tl)
        for nm, corners in SIGNS:
            pts = [proj(c, q) for q in corners]
            if any(q is None for q in pts): continue
            xs, ys = [q[0] for q in pts], [q[1] for q in pts]
            if max(xs) > 0.01 and min(xs) < 0.99 and max(ys) > 0.01 and min(ys) < 0.99 and (min(xs) < 0.01 or max(xs) > 0.99 or min(ys) < 0.01 or max(ys) > 0.99):
                flags += 1; print("   SIGNCUT S%02d t=%.2f %-10s x %.2f..%.2f y %.2f..%.2f" % (k, tl, nm, min(xs), max(xs), min(ys), max(ys)))
BOXES = []                                                   # engine CAMERA_INSIDE_PROP: AABB (+0.12) of every house (with its rotated cone roof) / box
for pr in props:
    if pr["type"] not in ("house", "box", "crate", "wall"): continue
    (x, y, z), sz = pr["pos"], pr["size"]; w, h, d = sz if isinstance(sz, list) else (sz, sz, sz)
    if pr["type"] == "house": r = max(w, d) * 0.78 * 1.4143; BOXES.append((pr, x - max(w / 2, r), y, z - max(d / 2, r), x + max(w / 2, r), y + h * 1.6, z + max(d / 2, r)))
    else: BOXES.append((pr, x - w / 2, y, z - d / 2, x + w / 2, y + h, z + d / 2))
for k, s in enumerate(shots):
    for tl in (0.05, s["_dur"] * 0.5, s["_dur"] - 0.05):
        cp = cam(s, tl)[0]
        for pr, x0, y0, z0, x1, y1, z1 in BOXES:
            if x0 - 0.12 <= cp[0] <= x1 + 0.12 and y0 - 0.12 <= cp[1] <= y1 + 0.12 and z0 - 0.12 <= cp[2] <= z1 + 0.12:
                flags += 1; print("   INSIDE S%02d t=%.2f %s@%s" % (k, tl, pr["type"], pr["pos"]))
print("frame check: %d CUT flags" % flags)
for s in shots: s.pop("_phrase"); s.pop("_dur", None)
json.dump(spec, open(os.path.join(P, "short.json"), "w"), indent=1)
print("wrote short.json: %d shots, %d characters, %d props, voice %.2f s" % (len(shots), len(chars), len(props), DURATION))
