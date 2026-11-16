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

## Video 02 — Gimli Glider (Air Canada 143, 1983)  -> projects/gimli-glider
- Reuse without rewriting: copy make_assets.py -> assets_base.py and build_short.py lines 1-130 -> scene_base.py, then import them; swap B.human_head/B.human_body for a new cast drawn by the same builders (style stays consistent). Stickers with extra faces (build_card) give props moods (jet: cruise/eng1/dead/glide/park/slam/saved).
- transformers now needs torch >= 2.6: render.yml installs torch/torchaudio 2.7.1 (forced_align still exists; it goes away in 2.9).
- Voice: render takes at several speeds and keep the fastest one Whisper understands >= 0.965 against script.txt (digits on both sides). At speed 1.36 Whisper misheard real words ("July"->"by"); 172 words need ~49 s to stay clear (~3.5 words/s). A "~" line in tts.txt adds a short dramatic pause.
- Music is synthesised inside build_short.py from word cues (engine spool-downs, true silence, boom, fire, resolve) because the Scene step runs after alignment.
- Interiors in dusk light were TOO_DARK: switch mood per set (cockpit in day).
- Camera-motion check failed (56 % static frames): wide sky/hangar shots with flat textures read as static. Next time: bigger pan/zoom (pan +-14, zoom +-8), more target close-ups, fewer flat walls.

## Video 03 — Viking horns myth -> projects/viking-horns
- Unique sets/shots every video (user rule); only characters may be reused (mom, dad, tech came back identical via gimli_assets.py).
- Retention hook that worked: character already roaring in frame 1 + boom + fast push-in, a "FAKE?" stamp on the reveal word, last shot = first shot for the loop.
- Music must be full energy from frame 1 (user rule): drums/bass from 0 s, Wagner-style brass for the opera, a short mysterious drop, SFX on words (stamp, pops, scratch, ding, bonk, applause, dig, whooshes).
- Voice (am_fenrir, energetic): trimming each TTS line 0.03 s before the first loud sample clipped soft onsets ("made" -> "aid"); use 0.08 s. Proper nouns (Nibelung, Doepler) cap Whisper scores near 0.96, so a 0.965 threshold can fail: the fallback picks the clearest take.
- Red velvet stage + dark carpet were TOO_DARK: keep interior colours light (velvet (224,92,104), floor #b07a66).
- Cards near frame edges got cut: place pop-up cards within +-0.35 x frame width of the anchor; hide a card at the first shot where it would be cut.
