#!/usr/bin/env python3
"""Generate short.json (and the word-cued music) for video 03: the Viking-horns myth.
usage: build_short.py <project folder>
Sets 70 units apart: VK beach (hook, fight, ending), FM Norwegian farm 1943, OP opera stage 1876,
BG Danish bog 1942.  Swaps (horns on/off) use twin puppets; anything that changes sets moves at
least 0.3 s after a dissolve, while the camera is elsewhere.  The last shot repeats the first for the loop."""
import json, os, sys, subprocess
import scene_base as SB
from scene_base import *

SB.X.clear(); SB.X.update(VK=0, FM=70, OP=140, BG=210)
HERE = os.path.dirname(os.path.abspath(__file__))


def put(cid, name, at, h, face="default"):
    chars.append(dict(id=cid, puppet="puppets/" + name, pos=at, height=h, face=face))


def rel(s, phrase):
    return round(say(phrase) - (0.0 if s["start"] == 0 else say(s["_phrase"])), 3)


def swap(s, at, out_id, in_id, p, face=None):
    hide(s, at, out_id); show(s, at, in_id, p, hop=0.1)
    if face: act(s, at, in_id, face=face)


# ================================================================== SETS
box("VK", 0, 0, -2, [40, 0.02, 20], color="#e6cf9c"); box("VK", 0, 0, -21, [60, 0.03, 18], color="#4f86c0")
plane("VK", "ship.png", 4.5, 0.0, -14, 10, 5.4)
box("VK", -4.6, 0, -2.6, [1.2, 0.8, 1.0], color="#8a8e9a"); box("VK", 5.2, 0, -3.6, [1.6, 1.1, 1.2], color="#7b808e")
tree("VK", -9, -6, 1.6, "#3f7a4c"); tree("VK", 10, -7, 1.8, "#356b42"); tree("VK", -13, -9, 1.9, "#356b42")

house("FM", 4.6, -9, [5, 4, 5], "#7a3a30", color="#c9573f")
for x in range(-9, 10, 2): post("FM", x, -5, 1.0, "#8a6a4a")
box("FM", 0.1, 0, 0.9, [2.6, 0.02, 1.8], color="#6b4a32"); tree("FM", -7, -7, 1.6, "#3f7a4c"); tree("FM", 10, -8, 1.7)

box("OP", 0, 0, -1.6, [12, 0.6, 6], texture="wood.jpg", repeat=[4, 2]); wall("OP", 0, 0, -4.7, [32, 7.5, 0.3], "velvet.jpg", [6, 1])
box("OP", 0, 0, 6, [32, 0.02, 12], color="#6a3040"); plane("OP", "prosc.png", 0, 0, 1.6, 9.0, 6.5)
for x in range(-4, 5): box("OP", x, 0.6, 1.25, [0.3, 0.12, 0.12], color="#ffe08a")
box("OP", 8.0, 0, 4.75, [4.6, 0.95, 0.22], color="#8a2a3a")

box("BG", 0, 0, -3, [30, 0.02, 20], texture="peat.jpg", repeat=[6, 4])
for x, z, w in ((-3.4, -2.2, 2.2), (3.6, -3.4, 2.8), (-0.4, -6, 3.2)): box("BG", x, 0.021, z, [w, 0.01, w * 0.5], color="#5c7f9e")
for x, z in ((-5, -1), (-4.4, -1.6), (4.8, -1.2), (5.4, -2), (-2.2, -5), (2.6, -6), (6.5, -4.5), (-6.8, -3.8)): post("BG", x, z, 0.9, "#8a9a3c")
tree("BG", -10, -9, 1.7, "#4f6f3a"); tree("BG", 9, -10, 1.6, "#4f6f3a")

# ================================================================== CHARACTERS
PARK = SB.PARK
human("vik", "vik", pos("VK", -0.3, 0, 0.5), face="shouting"); human("vikr", "vikr", PARK); human("foe", "foe", pos("VK", 7, 0, 0.3))
human("dopK", "dop", PARK, face="smug"); human("singv", "sing", PARK, face="happy"); human("singvh", "singh", PARK, face="happy")
human("farm", "farm", pos("FM", -1.4, 0, 0.6)); human("wag", "wag", pos("OP", -2.9, 0, 2.7), face="happy")
human("sing", "sing", pos("OP", 0.6, 0.6, -1.2), face="happy"); human("singh", "singh", PARK, face="happy"); human("dop", "dop", PARK, face="smug")
for c_, x_ in (("mom", 6.8), ("dad", 8.0), ("tech", 9.2)): human(c_, c_, pos("OP", x_, 0, 4.25), face="happy")
human("cut1", "cut1", pos("BG", -1.4, 0, 0.6)); human("cut2", "cut2", pos("BG", 1.4, 0, 0.5))
put("axe", "axe", pos("VK", 0.12, 1.0, 0.55), 0.9); put("spadeF", "spade", pos("FM", -0.95, 0, 0.7), 1.3)
put("spade1", "spade", pos("BG", -0.95, 0, 0.7), 1.3); put("spade2", "spade", pos("BG", 1.85, 0, 0.6), 1.3)
put("helmr", "helmr", pos("FM", 0.1, -1.2, 1.0), 0.8); put("helmb1", "helmb", pos("BG", -0.45, -1.4, 1.0), 0.8); put("helmb2", "helmb", pos("BG", 0.65, -1.4, 0.9), 0.8)
for cid, name, h in (("excl", "excl", 0.5), ("fake", "fake", 0.45), ("hornsK", "horns", 0.5), ("poofK", "poof", 0.9), ("cal43", "cal43", 1.3), ("only", "only", 0.4),
                     ("round", "round", 0.32), ("iron", "iron", 0.32), ("zero", "zero", 0.4), ("ques", "ques", 0.55), ("grab", "grab", 0.8), ("cal76", "cal76", 1.4),
                     ("notes", "notes", 0.6), ("ring", "ring", 1.0), ("hornsO", "horns", 0.5), ("poofO", "poof", 0.9), ("hearts", "hearts", 0.9), ("y150", "y150", 1.1),
                     ("cal42", "cal42", 1.2), ("poofB", "poof", 0.9), ("y3000", "y3000", 0.55), ("ritual", "ritual", 0.55), ("timeline", "timeline", 0.5),
                     ("hornsV", "horns", 0.5), ("poofV", "poof", 0.9), ("notesV", "notes", 0.55)):
    sticker(cid, name, h)

# ================================================================== SHOTS
HOOK = dict(target="vik", hw=0.34, yaw=10, pitch=4, zoom=12, pan=(-10, 6), fy=0.0)
# ---- 0-5 hook + "picture a Viking" (VK): roaring in frame 1, FAKE? stamp, the designer with the horns
s = shot("0", **HOOK)
act(s, 0.0, "vik", face="shouting", pose=dict(armR=-150), shake=0.6); show(s, 0.12, "excl", pos("VK", 0.55, 1.75, 0.6), hop=0.1)
s = shot("invented", anchor=pos("VK", 0.4, 1.3, 0.6), dist=8, yaw=-10, pitch=3, zoom=8, pan=(12, 0), fy=0.06)
hide(s, 0.0, "excl"); show(s, 0.0, "fake", pos("VK", -0.3, 1.55, 0.75), hop=0.1); act(s, 0.0, "vik", face="shocked", shake=0.8)
o = rel(s, "opera costume"); show(s, o, "dopK", pos("VK", 1.15, 0, 0.6), hop=0.15); act(s, o + 0.05, "dopK", pose=dict(armR=-140))
show(s, o + 0.1, "hornsK", pos("VK", 1.45, 1.55, 0.75), hop=0.1)
s = shot("Picture", anchor=pos("VK", 0.3, 1.5, -1.0), dist=11, yaw=14, pitch=6, zoom=8, pan=(14, 0), fy=0.05)
show(s, 0.0, "poofK", pos("VK", 1.1, 0.4, 0.8), hop=0.1); hide(s, 0.05, "dopK"); hide(s, 0.05, "hornsK"); hide(s, 0.0, "fake")
act(s, 0.1, "vik", face="happy", pose=dict(armR=-150)); hide(s, 0.5, "poofK")
s = shot("Big beard", target="vik", hw=0.5, yaw=6, pitch=2, zoom=10, pan=(0, -8), fy=-0.15)
act(s, 0.0, "vik", face="smug")
s = shot("Big axe", anchor=pos("VK", 0.12, 1.45, 0.55), dist=3.2, yaw=-8, pitch=3, zoom=10, pan=(8, 4), fy=0.0)
act(s, 0.05, "axe", shake=0.6)
s = shot("And two horns", out="dissolve", target="vik", hw=0.42, yaw=8, pitch=6, zoom=10, pan=(-6, -6), fy=-0.25)
act(s, 0.0, "vik", face="happy")

# ---- 6-9 the real thing (FM): 1943 farm, the only complete helmet rises: ROUND, IRON, 0 HORNS
s = shot("Now look", anchor=pos("FM", 0, 1.4, -1.0), dist=11, yaw=-12, pitch=6, zoom=8, pan=(-12, 0), fy=0.05)
show(s, rel(s, "1943"), "cal43", pos("FM", -2.7, 1.5, 0.5), hop=0.15)
s = shot("a farm in Norway", target="farm", hw=0.28, yaw=10, pitch=3, zoom=8, pan=(10, 4), fy=0.1)
for k in range(3): act(s, 0.1 + k * 0.45, "farm", pose=dict(armR=-70 if k % 2 == 0 else -20)); act(s, 0.2 + k * 0.45, "spadeF", shake=0.4)
s = shot("the only complete", anchor=pos("FM", 0.1, 0.6, 1.0), dist=4.2, yaw=-8, pitch=4, zoom=10, pan=(-6, 6), fy=0.0)
hide(s, 0.0, "cal43"); go(s, 0.0, "helmr", pos("FM", 0.1, 0.05, 1.0), 0.5, walk=False, hop=0.2); act(s, 0.2, "farm", face="shocked")
show(s, rel(s, "ever found"), "only", pos("FM", 0.1, 1.2, 1.15), hop=0.12)
s = shot("Round", out="dissolve", anchor=pos("FM", 0.1, 0.55, 1.0), dist=4.4, yaw=10, pitch=3, zoom=10, pan=(8, 0), fy=0.05)
hide(s, 0.0, "only"); show(s, 0.0, "round", pos("FM", -0.4, 1.05, 1.15), hop=0.1); show(s, rel(s, "Iron"), "iron", pos("FM", 0.55, 1.05, 1.15), hop=0.1)
z = rel(s, "Zero horns"); show(s, z, "zero", pos("FM", 0.1, 1.45, 1.2), hop=0.15); act(s, z, "helmr", shake=0.6)

# ---- 10-13 the fight (VK): horns are a handle
s = shot("Think about it", anchor=pos("VK", 0.35, 1.3, 0.5), dist=7, yaw=10, pitch=4, zoom=8, pan=(10, 0), fy=0.08)
act(s, 0.3, "vik", face="neutral", pose=dict(armR=-150)); go(s, 0.3, "foe", pos("VK", 1.0, 0, 0.4), 0.8); show(s, 0.5, "ques", pos("VK", 0.35, 2.0, 0.6), hop=0.1)
s = shot("Horns in a sword", anchor=pos("VK", 0.35, 1.3, 0.5), dist=5.2, yaw=-8, pitch=3, zoom=10, pan=(-8, 4), fy=0.06)
hide(s, 0.0, "ques"); act(s, 0.0, "foe", face="sneaky"); act(s, 0.1, "vik", face="smug")
s = shot("Your enemy", anchor=pos("VK", 0.2, 1.4, 0.5), dist=4.6, yaw=6, pitch=3, zoom=12, pan=(6, -6), fy=0.04)
gr = rel(s, "grabs"); act(s, gr - 0.1, "foe", pose=dict(armL=130)); show(s, gr, "grab", pos("VK", -0.3, 1.7, 0.8), hop=0.15); act(s, gr, "vik", face="shocked", shake=1.0)
s = shot("So where did", out="dissolve", target="vik", hw=0.3, yaw=-10, pitch=3, zoom=8, pan=(-8, 4), fy=0.1)
hide(s, 0.0, "grab"); act(s, 0.0, "foe", pose=dict(armL=0)); act(s, 0.05, "vik", face="confused", pose=dict(head=8)); show(s, 0.2, "ques", pos("VK", 0.25, 1.9, 0.6), hop=0.1)

# ---- 14-20 the opera (OP): 1876, Wagner, the Ring, the designer adds horns, the audience loves it
s = shot("You see", anchor=pos("OP", 0, 2.2, -1.0), dist=13, yaw=12, pitch=4, zoom=8, pan=(12, 0), fy=0.05)
show(s, rel(s, "1876"), "cal76", pos("OP", -2.6, 3.0, 1.0), hop=0.15)
s = shot("Richard Wagner", target="wag", hw=0.28, yaw=-10, pitch=3, zoom=8, pan=(-10, 4), fy=0.1)
for k in range(4): act(s, k * 0.35, "wag", pose=dict(armR=-150 if k % 2 == 0 else -100, armL=60 if k % 2 == 0 else 20))
show(s, 0.2, "notes", pos("OP", -2.3, 1.9, 2.9), hop=0.12)
s = shot("The Ring", anchor=pos("OP", 0.0, 3.3, 1.0), dist=6, yaw=8, pitch=3, zoom=8, pan=(8, 0), fy=0.0)
hide(s, 0.0, "cal76"); show(s, 0.05, "ring", pos("OP", 0.0, 2.9, 1.0), hop=0.15)
s = shot("He needed", target="sing", hw=0.3, yaw=-8, pitch=3, zoom=8, pan=(-8, 4), fy=0.1)
hide(s, 0.0, "ring"); hide(s, 0.0, "notes"); act(s, 0.1, "sing", pose=dict(armR=-120))
s = shot("So his costume", anchor=pos("OP", -0.2, 1.9, -1.1), dist=6.5, yaw=10, pitch=3, zoom=8, pan=(10, 0), fy=0.05)
show(s, 0.1, "dop", pos("OP", -1.0, 0.6, -1.0), hop=0.15); show(s, 0.2, "hornsO", pos("OP", -0.9, 2.45, -0.85), hop=0.1)
g = rel(s, "gave them horns"); show(s, g, "poofO", pos("OP", 0.6, 1.5, -0.9), hop=0.1); swap(s, g + 0.05, "sing", "singh", pos("OP", 0.6, 0.6, -1.2), "happy")
hide(s, g, "hornsO"); act(s, g, "dop", face="happy", pose=dict(armR=-150)); hide(s, g + 0.5, "poofO")
s = shot("Audiences loved", anchor=pos("OP", 8.0, 1.3, 4.3), dist=7, yaw=-10, pitch=4, zoom=8, pan=(-10, 4), fy=0.08)
for c_, t_ in (("mom", 0.1), ("dad", 0.2), ("tech", 0.3)): act(s, t_, c_, pose=dict(armR=-150, armL=150))
show(s, 0.3, "hearts", pos("OP", 8.0, 2.3, 4.6), hop=0.15)
s = shot("And it stuck", out="dissolve", anchor=pos("OP", 1.0, 1.9, -1.1), dist=6.5, yaw=8, pitch=3, zoom=8, pan=(8, 4), fy=0.05)
act(s, 0.1, "singh", pose=dict(armR=-150)); show(s, rel(s, "For"), "y150", pos("OP", 1.9, 2.1, -0.7), hop=0.15)

# ---- 21-26 the bog (BG): 1942, two horned helmets rise, 3,000 years old, rituals, a thousand years before Vikings
s = shot("But here's", anchor=pos("BG", 0, 1.3, -1.0), dist=12, yaw=-14, pitch=6, zoom=6, pan=(-12, 0), fy=0.05)
hide(s, 0.3, "foe"); show(s, 0.3, "singv", pos("VK", 1.2, 0, 0.4), hop=0); act(s, 0.3, "vik", face="happy", pose=dict(armR=-150, head=0)); hide(s, 0.3, "ques")
s = shot("Horned helmets", anchor=pos("BG", 0.2, 1.2, 0.5), dist=6.5, yaw=10, pitch=4, zoom=8, pan=(10, 4), fy=0.06)
for k in range(3):
    for c_, sp_ in (("cut1", "spade1"), ("cut2", "spade2")): act(s, 0.1 + k * 0.4, c_, pose=dict(armR=-70 if k % 2 == 0 else -20)); act(s, 0.15 + k * 0.4, sp_, shake=0.4)
s = shot("In 1942", anchor=pos("BG", 0.1, 0.9, 0.9), dist=5.5, yaw=-8, pitch=4, zoom=10, pan=(-8, 6), fy=0.04)
show(s, 0.05, "cal42", pos("BG", -1.9, 1.4, 0.8), hop=0.15); p2 = rel(s, "pulled two")
go(s, p2, "helmb1", pos("BG", -0.45, 0.05, 1.0), 0.45, walk=False, hop=0.2); go(s, p2 + 0.15, "helmb2", pos("BG", 0.65, 0.05, 0.9), 0.45, walk=False, hop=0.2)
show(s, p2, "poofB", pos("BG", 0.1, 0.0, 1.25), hop=0.1); act(s, p2 + 0.2, "cut1", face="shocked"); act(s, p2 + 0.25, "cut2", face="shocked")
s = shot("They're almost", anchor=pos("BG", 0.1, 0.55, 0.95), dist=4.2, yaw=8, pitch=3, zoom=10, pan=(8, 0), fy=0.0)
hide(s, 0.0, "cal42"); hide(s, 0.0, "poofB"); show(s, 0.1, "y3000", pos("BG", 0.1, 1.2, 1.15), hop=0.12)
s = shot("Built for", anchor=pos("BG", 0.1, 0.8, 0.95), dist=4.4, yaw=-8, pitch=3, zoom=8, pan=(-8, 4), fy=0.02)
hide(s, 0.0, "y3000"); show(s, 0.05, "ritual", pos("BG", 0.1, 1.15, 1.15), hop=0.12)
s = shot("Made more", out="dissolve", anchor=pos("BG", 0.1, 1.1, 1.0), dist=4.8, yaw=10, pitch=3, zoom=8, pan=(10, 0), fy=0.02)
hide(s, 0.0, "ritual"); show(s, 0.05, "timeline", pos("BG", 0.1, 1.2, 1.15), hop=0.12)

# ---- 27-30 wrong people (VK): the horns fly off the Viking onto the opera singer; loop back to the hook
s = shot("So the horns", anchor=pos("VK", 0.45, 1.3, 0.5), dist=7, yaw=-10, pitch=4, zoom=8, pan=(-10, 4), fy=0.08)
l_ = rel(s, "landed"); show(s, l_, "hornsV", pos("VK", -0.3, 1.6, 0.65), hop=0); go(s, l_ + 0.02, "hornsV", pos("VK", 1.2, 1.6, 0.65), 0.5, walk=False, hop=0.3)
swap(s, l_, "vik", "vikr", pos("VK", -0.3, 0, 0.5), "confused"); hide(s, l_, "axe"); show(s, l_, "poofV", pos("VK", -0.3, 1.3, 0.7), hop=0.1)
hide(s, l_ + 0.55, "hornsV"); swap(s, l_ + 0.55, "singv", "singvh", pos("VK", 1.2, 0, 0.4), "happy"); hide(s, l_ + 0.6, "poofV")
s = shot("The Vikings never", target="vikr", hw=0.3, yaw=8, pitch=3, zoom=8, pan=(8, 4), fy=0.1)
act(s, 0.05, "vikr", face="confused", pose=dict(armR=-40, armL=40, head=-8))
s = shot("An opera did", out="dissolve", target="singvh", hw=0.3, yaw=-8, pitch=3, zoom=10, pan=(-8, 4), fy=0.1)
act(s, 0.05, "singvh", pose=dict(armR=-150)); show(s, 0.15, "notesV", pos("VK", 1.75, 2.0, 0.6), hop=0.12)
s = shot("And that's why", **HOOK)
swap(s, 0.0, "vikr", "vik", pos("VK", -0.3, 0, 0.5), "shouting"); act(s, 0.0, "vik", pose=dict(armR=-150))
show(s, 0.0, "axe", pos("VK", 0.12, 1.0, 0.55), hop=0); hide(s, 0.0, "singvh"); hide(s, 0.0, "notesV")

# ================================================================== SPEC
spec = {
    "fps": 30, "audio": {"voice": "audio/voice.mp3", "music": "audio/music.mp3", "musicDb": -11},
    "words": "audio/words.json", "captions": {"wordsPer": 1}, "font": "fonts/Montserrat-ExtraBold.ttf", "contactShadow": 0.6,
    "moods": {"day": {"sun": {"azimuth": 35, "elevation": 50, "color": "#ffe0b5", "intensity": 2.4},
                      "sky": {"top": "#5f86d8", "horizon": "#f2b98a"}, "fill": {"sky": "#8ea2ff", "ground": "#6a3b6e", "intensity": 1.15}}},
    "lighting": [{"t": 0, "mood": "day"}],
    "ground": {"texture": TEX + "grass.jpg", "repeat": [525, 525], "size": 1400},
    "backdrop": {"image": "bg/fjord.jpg", "blur": 5}, "ink": {"set": 4},
    "characters": chars, "props": props, "shots": shots, "end": "audio",
}

# ---- music + effects synthesised to the word timings: full energy from frame 1
cues = dict(stamp=say("invented"), pops=[say("Big beard"), say("Big axe"), say("And two horns")], scratch=say("Now look"), ding=say("Zero horns"),
            bonk=say("grabs"), opera=say("You see"), applause=say("Audiences loved"), strange=say("But here's"), back=say("They're almost"),
            dig=say("pulled two"), whoosh=[say("Think about it"), say("You see"), say("But here's"), say("So the horns"), say("landed")], end=DURATION)
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
