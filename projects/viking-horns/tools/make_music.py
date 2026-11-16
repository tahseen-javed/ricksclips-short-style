#!/usr/bin/env python3
"""Energetic underscore + sound effects for the Viking-horns Short, synthesised in code (no samples).
Full energy from frame 1: kick, snare, taiko hits, hats, driving bass and string stabs in D minor with a
boom on the first frame; a half-time breath on the record scratch; a Wagner-style heroic brass call for
the opera; a mysterious drop for the bog, then the beat returns; stamp, pops, scratch, ding, bonk,
applause, dig and whooshes on their words.   usage: make_music.py out.wav seconds [cues.json]"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100; OUT, LEN = sys.argv[1], float(sys.argv[2])
C = dict(stamp=1.8, pops=[4.0, 4.6, 5.2], scratch=7.0, ding=13.0, bonk=17.0, opera=19.5, applause=30.0, strange=33.0, back=40.0,
         dig=37.5, whoosh=[14.0, 19.5, 33.0, 46.0, 48.5], end=LEN)
if len(sys.argv) > 3: C.update(json.load(open(sys.argv[3])))
N = int(SR * LEN); bed = np.zeros(N); fx = np.zeros(N); R = np.random.RandomState(3); BEAT = 60.0 / 124


def midi(m): return 440.0 * 2 ** ((m - 69) / 12.0)
def put(buf, sig, t, g=1.0):
    s = int(SR * t)
    if 0 <= s < N: e = min(N, s + len(sig)); buf[s:e] += sig[:e - s] * g
def env(n, a, r):
    e = np.ones(n); na, nr = min(n, max(1, int(a * SR))), min(n, max(1, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[n - nr:] *= np.linspace(1, 0, nr) ** 2; return e
def filt(x, kind, f): return sosfilt(butter(2, f, btype=kind, fs=SR, output='sos'), x)
def noise(d): return R.uniform(-1, 1, int(SR * d))
def ts(d): return np.arange(int(SR * d)) / SR
def sweep(f0, f1, d, k): t = ts(d); return np.sin(2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * k)) / SR)
def kick(): t = ts(0.35); return sweep(140, 48, 0.35, 30) * np.exp(-t * 9)
def taiko(): t = ts(0.5); return sweep(170, 95, 0.5, 20) * np.exp(-t * 6) + filt(noise(0.5), 'lowpass', 600) * np.exp(-t * 25) * 0.6
def snare(): t = ts(0.22); return filt(noise(0.22), 'bandpass', [1200, 6000]) * np.exp(-t * 18) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.5
def hat(): t = ts(0.05); return filt(noise(0.05), 'highpass', 7000) * np.exp(-t * 70)
def saw(f, d, cut, a=0.005, r=0.08):
    t = ts(d); return filt(sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9)), 'lowpass', cut) * env(len(t), a, r)


DM = [[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 49, 52]]          # Dm Bb C A


def groove(t0, t1, full=True):
    i, t = 0, t0
    while t < t1 - 0.05:
        b, ch = i % 8, DM[(i // 8) % 4]
        if b in (0, 4) or (not full and b == 0): put(bed, kick(), t, 0.9)
        if full and b in (2, 6): put(bed, snare(), t, 0.45)
        if full and b in (3, 7) and (i // 8) % 2: put(bed, taiko(), t, 0.4)
        put(bed, hat(), t, 0.12 if b % 2 else 0.2)
        put(bed, saw(midi(ch[0] - 24), BEAT * 0.45, 900), t, 0.32)
        if full and b in (1, 5):
            for n in ch: put(bed, saw(midi(n), BEAT * 0.35, 2600), t, 0.07)
        i += 1; t += BEAT / 2


def brass(t0, t1):                                                      # heroic call, Wagner-style dotted rhythm
    mot = [(57, .5), (62, 1.5), (57, .5), (62, .5), (65, 1.5), (62, 1.5), (65, .5), (69, 1.5), (65, .5), (69, .5), (72, 1.5), (69, 1.5)]
    t = t0
    while t < t1 - 0.3:
        for m, l in mot:
            d = l * BEAT / 2
            if t + d > t1: return
            put(bed, saw(midi(m), d * 0.95, 3200, 0.03, 0.06), t, 0.16); t += d


s0 = C['scratch'] + 0.3; half = s0 + BEAT * 4
groove(0.0, C['scratch']); groove(s0, half, full=False); groove(half, C['strange'])
brass(C['opera'] + 0.2, C['strange'] - 0.2)
t = C['strange']                                                       # mysterious drop: low drone, ticks, a high shimmer
put(bed, saw(midi(26), C['back'] - t, 300, 0.8, 0.6), t, 0.5); put(bed, np.sin(2 * np.pi * midi(86) * ts(C['back'] - t)) * env(int(SR * (C['back'] - t)), 1.0, 0.5), t, 0.03)
while t < C['back'] - 0.2: put(bed, hat(), t, 0.15); t += BEAT
groove(C['back'], LEN); brass(C['back'] + BEAT * 8, LEN)

put(fx, sweep(120, 38, 1.4, 4) * np.exp(-ts(1.4) * 2.5) + filt(noise(1.4), 'lowpass', 2500) * np.exp(-ts(1.4) * 4) * 0.5, 0.0)   # boom on frame 1
st = sweep(160, 60, 0.4, 12) * np.exp(-ts(0.4) * 9); k = len(ts(0.12)); st[:k] += filt(R.uniform(-1, 1, k), 'bandpass', [800, 3000]) * np.exp(-ts(0.12) * 30) * 0.7
put(fx, st, C['stamp'])                                                # stamp on "invented"
for p in C['pops']: put(fx, sweep(500, 1400, 0.09, 25) * np.exp(-ts(0.09) * 30), p, 0.6)
t = ts(0.45); put(fx, filt(noise(0.45), 'bandpass', [600, 3000]) * np.sin(2 * np.pi * np.cumsum(500 + 450 * np.sin(2 * np.pi * 7 * t)) / SR) * env(len(t), 0.01, 0.1), C['scratch'], 0.9)
t = ts(1.2); put(fx, sum(a * np.sin(2 * np.pi * 1320 * k * t) for k, a in ((1, 1), (2.76, .5), (5.4, .25))) * np.exp(-t * 4), C['ding'], 0.5)
t = ts(0.3); put(fx, sweep(380, 110, 0.3, 10) * np.exp(-t * 10), C['bonk'], 0.9)
t = ts(1.8); clap = np.zeros(len(t))
for k in R.randint(0, len(t) - 2000, 420): clap[k:k + 1500] += filt(R.uniform(-1, 1, 1500), 'bandpass', [900, 5000]) * np.exp(-np.arange(1500) / 200.0)
put(fx, clap * env(len(t), 0.1, 0.7), C['applause'], 0.35)
t = ts(0.6); put(fx, sweep(110, 45, 0.6, 8) * np.exp(-t * 6) + filt(noise(0.6), 'lowpass', 500) * np.exp(-t * 8), C['dig'], 0.9)
for w in C['whoosh']:
    t = ts(0.5); put(fx, filt(noise(0.5), 'bandpass', [400, 3500]) * np.sin(np.pi * t / 0.5) ** 2, w - 0.25, 0.5)

lo = np.abs(bed) > 1e-4; bed *= 0.1 / max(1e-6, np.sqrt(np.mean(bed[lo] ** 2)))
fx *= 0.85 / max(1e-6, np.abs(fx).max())
mix = np.tanh((bed + fx) * 1.2) / np.tanh(1.2); f = int(SR * 0.12); mix[-f:] *= np.linspace(1, 0, f)
sf.write(OUT, (mix / max(1e-6, np.abs(mix).max()) * 0.95).astype(np.float32), SR)
print("music %s %.1f s" % (OUT, LEN))
