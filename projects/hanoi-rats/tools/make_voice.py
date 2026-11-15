#!/usr/bin/env python3
"""Voiceover with Kokoro TTS (free, runs on the runner): fast and punchy, pauses squeezed to <= 0.16 s,
a touch of tempo if the target length needs it, loudness normalised, 0.5 s tail.
usage: make_voice.py <audio folder> <target seconds>"""
import os, sys, subprocess
import numpy as np, soundfile as sf
from kokoro import KPipeline

d = sys.argv[1].rstrip("/") + "/"; target = float(sys.argv[2]); SR = 24000
text = open(d + "tts.txt", encoding="utf-8").read()
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")


def gen(speed):
    parts = []
    for _, _, a in pipe(text, voice="af_heart", speed=speed, split_pattern=r"\n+"):
        a = np.asarray(a, dtype=np.float32); idx = np.where(np.abs(a) > 0.012)[0]
        if len(idx): a = a[max(0, idx[0] - int(0.03 * SR)): min(len(a), idx[-1] + int(0.12 * SR))]
        parts += [a, np.zeros(int(0.04 * SR), np.float32)]
    return np.concatenate(parts)


def squeeze(a, keep=0.16, thr=0.012):
    hop = int(0.01 * SR); n = len(a) // hop; out = []; i = 0
    env = np.array([np.abs(a[k * hop:(k + 1) * hop]).max() for k in range(n)])
    while i < n:
        if env[i] >= thr: out.append(a[i * hop:(i + 1) * hop]); i += 1; continue
        j = i
        while j < n and env[j] < thr: j += 1
        seg = a[i * hop:i * hop + min((j - i) * hop, int(keep * SR))].copy(); f = min(len(seg), int(0.01 * SR))
        if f: seg[-f:] *= np.linspace(1, 0, f)
        out.append(seg); i = j
    out.append(a[n * hop:]); return np.concatenate(out)


raw = gen(1.0); print("natural speed: %.1f s" % (len(raw) / SR))
a = squeeze(gen(1.3)); dur = len(a) / SR
tempo = min(1.12, max(1.0, dur / target))
print("speed 1.3, pauses squeezed: %.1f s -> tempo %.3f -> about %.1f s" % (dur, tempo, dur / tempo))
sf.write(d + "voice_raw.wav", a / max(1e-6, np.abs(a).max()) * 0.9, SR)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", d + "voice_raw.wav", "-af",
                "atempo=%.4f,loudnorm=I=-15:TP=-1.5:LRA=9,apad=pad_dur=0.5" % tempo, "-ar", "44100", "-b:a", "192k", d + "voice.mp3"], check=True)
os.remove(d + "voice_raw.wav")
