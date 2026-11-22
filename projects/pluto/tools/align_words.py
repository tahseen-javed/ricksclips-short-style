#!/usr/bin/env python3
"""Word timings by CTC forced alignment (wav2vec2): every script word gets its real start and end in the voice
(about 20 ms accurate), unlike Whisper's guesses for short words.
usage: align_words.py voice.mp3 script.txt spoken.json out.json
spoken.json maps script words that are not spelled the way they are said ("1902." -> "nineteen oh two.")."""
import sys, json, os, re, subprocess
import numpy as np, torch, torchaudio

audio, script_path, spoken_path, out = sys.argv[1:5]
SR = 16000
raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", audio, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
wav = torch.from_numpy(np.frombuffer(raw, dtype=np.float32).copy()).unsqueeze(0)
dur = wav.shape[1] / SR
script = open(script_path, encoding="utf-8").read().split()
spoken = json.load(open(spoken_path, encoding="utf-8")) if os.path.exists(spoken_path) else {}

bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval()
dic = {c: i for i, c in enumerate(bundle.get_labels())}
owners, words = [], []
for i, w in enumerate(script):
    toks = re.findall(r"[A-Za-z']+", spoken.get(w, w))
    if not toks: sys.exit("script word %r has nothing to say: add it to spoken.json" % w)
    for t in toks: owners.append(i); words.append(t.upper())
transcript = "|".join(words)
targets = torch.tensor([[dic[c] for c in transcript]], dtype=torch.int32)
with torch.inference_mode():
    emission, _ = model(wav)
    emission = torch.log_softmax(emission, dim=-1)
ali, scores = torchaudio.functional.forced_align(emission, targets, blank=0)
spans = torchaudio.functional.merge_tokens(ali[0], scores[0].exp())
assert len(spans) == targets.shape[1], (len(spans), targets.shape[1])
ratio = dur / emission.shape[1]

wt = [[None, None] for _ in words]; wi = 0; conf = []
for ch, sp in zip(transcript, spans):
    if ch == "|": wi += 1; continue
    s, e = sp.start * ratio, sp.end * ratio; conf.append(float(sp.score))
    if wt[wi][0] is None: wt[wi][0] = s
    wt[wi][1] = e
res = [[None, None] for _ in script]
for o, (s, e) in zip(owners, wt):
    if res[o][0] is None: res[o][0] = s
    res[o][1] = e
prev = 0.0; entries = []
for w, (s, e) in zip(script, res):
    s = max(s, prev); e = max(e, s + 0.04); entries.append({"w": w, "t0": round(s, 2), "t1": round(e, 2)}); prev = e
with open(out, "w", encoding="utf-8") as fh:
    fh.write('{"audio": %s, "duration": %s, "method": "ctc",\n "words": [\n  %s\n ]}\n' % (
        json.dumps(os.path.basename(audio)), round(dur, 2), ",\n  ".join(json.dumps(x, ensure_ascii=False) for x in entries)))
print("aligned %d words over %.2f s, mean confidence %.2f, shortest word %.2f s" % (len(entries), dur, sum(conf) / len(conf), min(x["t1"] - x["t0"] for x in entries)))
