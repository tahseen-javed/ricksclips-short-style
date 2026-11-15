#!/usr/bin/env python3
"""Playful pizzicato underscore synthesised in code (Karplus-Strong plucks):
sneaky and curious, soft plucked bass, builds a little tension, no drums.
usage: make_music.py out.wav [seconds]"""
import sys, math, random
import numpy as np, soundfile as sf

SR = 44100
OUT = sys.argv[1]; LEN = float(sys.argv[2]) if len(sys.argv) > 2 else 42.0
BPM = 118; BEAT = 60.0 / BPM; BAR = 4 * BEAT
random.seed(42); rng = np.random.RandomState(42)

def pluck(freq, dur, decay=0.996, bright=0.5, vol=1.0):
    n = max(2, int(SR / freq)); buf = rng.uniform(-1, 1, n) * vol
    buf -= buf.mean(); out = np.empty(int(SR * dur), np.float32); i = 0
    while i < len(out):
        k = min(n, len(out) - i); out[i:i + k] = buf[:k]
        buf = decay * (bright * buf + (1 - bright) * np.roll(buf, 1)); i += k
    env = np.minimum(1.0, np.arange(len(out)) / (SR * 0.004))
    return out * env

def midi(m): return 440.0 * 2 ** ((m - 69) / 12.0)

total = int(SR * (LEN + 2)); mix = np.zeros(total, np.float32)
def put(sig, t, gain):
    s = int(SR * t)
    if s >= total: return
    e = min(total, s + len(sig)); mix[s:e] += sig[:e - s] * gain

# A minor, sneaky: Am | F | Dm | E7  (bass roots 45 41 38 40)
prog = [([57, 60, 64], 45), ([53, 57, 60], 41), ([50, 53, 57], 38), ([52, 56, 59], 40)]
scale = [57, 59, 60, 62, 64, 65, 67, 68, 69, 71, 72, 74, 76]
bars = int(math.ceil(LEN / BAR)) + 1
mel = 69
for b in range(bars):
    chord, root = prog[b % 4]; t0 = b * BAR
    # soft plucked bass: root on 1 and 3, fifth on the "and" of 2 (sneaky bounce)
    put(pluck(midi(root), 1.1, 0.994, 0.35), t0, 0.55)
    put(pluck(midi(root + 7), 0.5, 0.992, 0.35), t0 + 1.5 * BEAT, 0.32)
    put(pluck(midi(root), 1.1, 0.994, 0.35), t0 + 2 * BEAT, 0.5)
    put(pluck(midi(root + 3 if b % 4 != 3 else root + 4), 0.5, 0.992, 0.35), t0 + 3.5 * BEAT, 0.3)
    # pizzicato chord stabs on the off-beats
    for beat in (1, 3):
        for k, n in enumerate(chord): put(pluck(midi(n), 0.35, 0.985, 0.6), t0 + beat * BEAT + 0.012 * k, 0.17)
    # curious melody: staccato 8ths with rests; only notes that agree with the chord (no clashes)
    allowed = {0: [67, 69, 71, 72, 74, 76], 1: [65, 67, 69, 72, 74], 2: [62, 65, 67, 69, 72, 74], 3: [64, 68, 71, 74, 76]}[b % 4]
    for e in range(8):
        if random.random() < 0.38: continue
        near = sorted(allowed, key=lambda n: abs(n - mel) + random.random() * 2.5)
        mel = near[0]
        lift = 12 if (b >= 8 and random.random() < 0.5) else 0
        put(pluck(midi(mel + lift), 0.28, 0.986, 0.7), t0 + e * BEAT / 2, 0.22 + 0.02 * min(b, 10))
    # tension: a quiet tremolo string note from bar 10 on
    if b >= 10:
        dur = BAR; t = np.arange(int(SR * dur)) / SR
        trem = (0.5 + 0.5 * np.sin(2 * np.pi * 7 * t)) * np.sin(2 * np.pi * midi(chord[0] + 12) * t) * np.exp(-t * 0.6)
        put(trem.astype(np.float32), t0, 0.05 + 0.005 * (b - 10))
# warm low pad under everything
t = np.arange(total) / SR
pad = np.zeros(total, np.float32)
for b in range(bars):
    chord, root = prog[b % 4]; s, e = int(b * BAR * SR), min(total, int((b + 1) * BAR * SR))
    if s >= total: break
    tt = t[s:e] - b * BAR; env = np.minimum(1, tt / 0.4) * np.minimum(1, (BAR - tt) / 0.4)
    pad[s:e] = env * (np.sin(2 * np.pi * midi(root + 12) * tt) + 0.5 * np.sin(2 * np.pi * midi(root + 19) * tt))
mix += pad * 0.05
# gentle fade out and normalise
fade = int(SR * 2.5); mix[-fade:] *= np.linspace(1, 0, fade)
mix = mix[:int(SR * LEN)]
mix = np.tanh(mix * 1.4) / np.max(np.abs(np.tanh(mix * 1.4))) * 0.7
sf.write(OUT, mix, SR)
print('music', OUT, '%.1f s' % (len(mix) / SR))
