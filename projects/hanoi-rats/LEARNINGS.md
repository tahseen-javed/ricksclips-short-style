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

## Video 04 (Vasa warship) - what changed and what to keep
- Every set change needs out="cut" (or "dissolve"). The default out is "glide", which flies the camera across the whole world between sets and gives empty, broken frames.
- The stage puts an anchor 12 % above frame centre by default (frameY 0.12). Set frameY 0 for anchor shots and place cards with a card() helper: y = anchor + dy * 0.728 * dist, x = anchor + dx * 0.41 * dist, dy about 0.22-0.25. No more cards cut at the top.
- make_voice squeeze kept the START of every quiet gap and cut the soft onset of the next word (s, t, th, b): "Sinking" was heard as "thinking". Now it keeps 0.04 s of the gap head plus 0.08 s of its tail, and the line trim starts at a 0.004 threshold. Intelligibility 0.954 -> 0.980.
- make_music.py is also called once before the voice exists (placeholder step) with no cues file: handle that case.
- Ground texture can be water: sea sets come for free, anything below y 0 is hidden under the surface (sinking and rising ships are just moves in y).
- Sticker pose head rotates the whole card around its centre, positive is clockwise.
- Bash tool: an unbalanced apostrophe inside a heredoc breaks the command. Write such files with the Write tool.
- Tokens: about 589K new tokens, far over the cap. The cause was very long planning in my reasoning plus two extra render rounds. Next time: reuse projects/vasa/tools/build_short.py structure (card, cut helpers, cuts at set changes), plan briefly, one render.

## Video 05 (Wrong Way Corrigan) -> projects/corrigan
- Kokoro under-articulates the FIRST word of every separately generated line: So, Clouds, Then, They were heard as nothing or as "louds". Merging tts lines so those words fall mid-line fixed all of them (0.938 -> 0.962). But a longer line 1 made the very first word ("Officials") soft. Keep line 1 short (hook sentence only) and merge only the later lines.
- Stop-frame PURE_BLACK = more than 3% of pixels with RGB under 10. Dark boxes close to the camera trigger it. In close interiors use mid-tone colours (#9a6a48 or lighter), a wood texture floor and a window.
- A card must be narrower than 0.41 x camera distance (frame height is 0.728 x distance) or it is cut at the frame edge.
- Props box, plane, crate and wall are placed by their BOTTOM.
- Hyphenated script words become one token: "Twenty-eight" is say("twentyeight").
- Motion check: static_frames 70% and pan_speed_ok false (vasa 53%). Too many held shots. Next video: every shot gets a visible camera move (dolly in or out, or an orbit of 8 degrees or more), target static under 55%.
- The same cloud render took 37 min once and about 60 min the next time: runner speed varies.
- Tokens: about 490K new tokens against a 200K cap. Causes: three cloud render rounds (stills flags, then a voice fix), 70 hand-drawn assets, context compactions. Next time: copy projects/corrigan/tools, write tts.txt with merged lines from the start, keep line 1 short, check stills locally before the first cloud run, one render.

## Video 06 (FedEx blackjack) -> projects/fedex
- `pan` is px/s (not degrees). Videos 01-05 used 6-12 px/s = a held frame (static 70%). Now every shot uses glide "dolly" (parallax) and pan x5 (about 45 px/s) with zoom 7-14 %/s: static frames 1.6%, pan_speed_ok and zoom_ok true. The S() helper in fedex/build_short.py does this for every shot.
- Puppet folder names are global: a card named "fred" overwrote the human puppet "fred" (every Fred became a giant sign). Card names must never equal a cast name.
- rel(s, word) takes the FIRST match in the whole script. A word that also appears earlier ("founder" in line 1) puts the action at a negative time, so the card shows up in earlier shots. Use "word#2" and check that no action time is negative (dry run below).
- Cards placed toward the camera (dz) drift sideways when the shot has yaw. card() now places along the camera's right/forward axes (cos/sin yaw). Size each card from the shot distance: tag() keeps width <= 24% of distance (about 58% of the frame); tilted stamps 20%; zoom <= 10 when a wide card shows.
- A shot without out="cut" glides into the next one for 0.8 s. A shot under 1 s that follows a glide never settles, and its card gets cut. Cut into short shots, and always cut between sets.
- At dusk (sun azimuth 250) a hangar front faces away from the sun: TOO_DARK. Use light walls (#ddd6ee) and frame some sky.
- Wood texture on small boxes (desks, tables) reads as crates. Use solid colours plus a lighter top slab.
- Whisper writes numbers as digits, so the "understood" score drops (0.92) even when every word is right. Read the replace lines, not the score.
- Local dry run before any cloud run (python only, no install): make_assets into D:/Claude projects/_tmp/fx with the Montserrat font, then build_short with a fake words.json (NO_MUSIC=1). It caught two crashes for free.
- Funk score (112 bpm E minor) synth: fedex/tools/make_music.py. Next video: change the style again.
