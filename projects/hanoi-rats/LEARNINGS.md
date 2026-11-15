# LEARNINGS — read before every build, append after every render

Rules that hold for this channel (from the skill): plum-black lines, warm sun vs cool tinted shadow,
camera moves in every shot and glides between shots, captions 1-2 words at 70 % height, head ~20 % of
frame width in close-ups, cute characters (big round heads, shiny eyes, blush).

## Video 01 — Hanoi rats (1902 rat bounty)
- Assets: drawn in code (PIL) — official / hunter / inspector puppets + rat / tailless rat, 8 faces each.
- Voice: Kokoro af_heart, speed tuned to ~36 s. Music: synthesised pizzicato underscore.
- Findings and fixes (read before video 02):
  - Whisper word times are wrong for short words at sentence ends ("Victory?" got 0.16 s): use CTC forced alignment (tools/align_words.py), accurate to ~20 ms.
  - CAMERA_INSIDE_PROP can be a false alarm: the roof cone's axis-aligned box is huge. Keep the camera z beyond house z + 1.1 x max(w, d), and use square footprints (w = d) so the roof overhang does not shade the front wall.
  - Never let an actor stand in the frame of a shot it does not belong to: teleport actors while the camera is in another set, keep one set per location (70 units apart) and use dissolves between sets, glides inside a set.
  - Timed overlays (SNIP!, poof, scissors, coin, sign) are "sticker" puppets parked at y=-60 and moved in with a 0.02 s move.
  - A rat cannot climb a wall (legs do not lean with the body): use steps and a door.
  - Shots under 0.7 s are all glide: merge them into the neighbour.
- Upgrade for next time: more rats and bigger rats in the beats about numbers (0.7 m reads better than 0.55 m); plan every shot's framing with frame width = 0.41 x distance before writing it; keep the first frame busy (character plus the paradox).
