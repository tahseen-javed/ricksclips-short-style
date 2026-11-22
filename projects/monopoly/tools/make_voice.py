#!/usr/bin/env python3
"""Normal, clear American male voiceover with Kokoro TTS (free, runs on the runner).
Renders every line with am_michael and am_fenrir at three speeds, scores each take with Whisper
against the script (numbers stay digits on both sides, so only real mishearings count) and keeps the
fastest take that is still understood almost perfectly (>= 0.965). Pauses inside a line are squeezed
to <= 0.16 s; a line starting with "~" is followed by a short dramatic pause (0.45 s in total).
Light presence EQ, gentle compression, -15 LUFS.
usage: make_voice.py <audio folder> <target seconds>"""
import os, re, sys, difflib, subprocess
import numpy as np, soundfile as sf, whisper
from kokoro import KPipeline

d = sys.argv[1].rstrip("/") + "/"; target = float(sys.argv[2]); SR = 24000
LINES = [l.strip() for l in open(d + "tts.txt", encoding="utf-8") if l.strip()]
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
VOICES, SPEEDS = ["am_fenrir"], [1.28, 1.32, 1.36]       # the channel voice, energetic


def squeeze(a, keep=0.14, thr=0.012):
    hop = int(0.01 * SR); n = len(a) // hop; out = []; i = 0
    env = np.array([np.abs(a[k * hop:(k + 1) * hop]).max() for k in range(n)])
    while i < n:
        if env[i] >= thr: out.append(a[i * hop:(i + 1) * hop]); i += 1; continue
        j = i
        while j < n and env[j] < thr: j += 1
        seg = a[i * hop:j * hop].copy(); h, tl, f = int(0.04 * SR), int((keep - 0.04) * SR), int(0.01 * SR)
        if i > 0 and len(seg) > h + tl:                       # never the line onset (already trimmed); keep the tail of the last sound AND the soft onset of the next word
            s1, s2 = seg[:h].copy(), seg[-tl:].copy(); s1[-f:] *= np.linspace(1, 0, f); s2[:f] *= np.linspace(0, 1, f); seg = np.concatenate([s1, s2])
        out.append(seg); i = j
    out.append(a[n * hop:]); return np.concatenate(out)


def gen(voice, speed):
    parts = []
    for line in LINES:
        a = np.concatenate([np.asarray(x, dtype=np.float32) for _, _, x in pipe(line.lstrip("~").strip(), voice=voice, speed=speed)])
        idx, on = np.where(np.abs(a) > 0.012)[0], np.where(np.abs(a) > 0.004)[0]      # low threshold finds the start of a soft s/t/th
        if len(idx): a = a[max(0, on[0] - int(0.06 * SR)): min(len(a), idx[-1] + int(0.12 * SR))]
        parts += [squeeze(a), np.zeros(int((0.33 if line.startswith("~") else 0.04) * SR), np.float32)]
    return np.concatenate(parts)


asr = whisper.load_model("base.en")
norm = lambda s: re.sub(r"[^a-z0-9' ]+", " ", s.lower().replace("’", "'")).split()
ref = norm(open(d + "script.txt", encoding="utf-8").read())


def understood(a):
    sf.write(d + "_cand.wav", a, SR)
    hyp = norm(asr.transcribe(d + "_cand.wav", language="en")["text"])
    return difflib.SequenceMatcher(None, ref, hyp, autojunk=False).ratio()


rows = []
for v in VOICES:
    for sp in SPEEDS:
        try: a = gen(v, sp)
        except Exception as e: print("skip %s: %s" % (v, e)); break
        rows.append(("%s @%.2f" % (v, sp), a, understood(a)))
        print("%-18s %5.1f s  understood %.3f" % (rows[-1][0], len(a) / SR, rows[-1][2]))
if os.path.exists(d + "_cand.wav"): os.remove(d + "_cand.wav")
good = [r for r in rows if r[2] >= 0.975]
name, a, sco = min(good, key=lambda r: len(r[1])) if good else max(rows, key=lambda r: r[2])
dur = len(a) / SR; tempo = min(1.05, max(1.0, dur / target))
print("chose %s (understood %.3f): tempo %.3f -> about %.1f s" % (name, sco, tempo, dur / tempo))
sf.write(d + "voice_raw.wav", a / max(1e-6, np.abs(a).max()) * 0.9, SR)
af = ("atempo=%.4f,highpass=f=70,equalizer=f=3200:t=q:w=1.2:g=3,treble=g=2:f=8000,"
      "acompressor=threshold=0.1:ratio=3:attack=5:release=90:makeup=1.6,loudnorm=I=-15:TP=-1.5:LRA=9,apad=pad_dur=0.5") % tempo
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", d + "voice_raw.wav", "-af", af, "-ar", "44100", "-b:a", "192k", d + "voice.mp3"], check=True)
os.remove(d + "voice_raw.wav")
