#!/usr/bin/env python3
"""Underscore + sound effects for the Gimli Glider Short, synthesised in code (no samples):
a tense pulse while the jet cruises, two engine spool-downs, true silence on "Total silence", a low
heartbeat, a curious pluck theme for the explanation, a hopeful lift when luck arrives, a near-silent
glide, a boom on the nose slam, crackling fire, and a warm resolve when everyone lives.
usage: make_music.py out.wav seconds [cues.json]   (build_short.py passes the word-timed cues)"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100; OUT, LEN = sys.argv[1], float(sys.argv[2])
C = dict(quit1=8.5, quit2=9.5, sil=10.3, explain=15.0, luck=26.0, drop=35.0, slam=36.8, fire=37.8, lives=38.8)
if len(sys.argv) > 3: C.update(json.load(open(sys.argv[3])))
N = int(SR * LEN); bed = np.zeros(N); fx = np.zeros(N); R = np.random.RandomState(7); BEAT = 0.6


def midi(m): return 440.0 * 2 ** ((m - 69) / 12.0)


def put(buf, sig, t, g=1.0):
    s = int(SR * t)
    if 0 <= s < N: e = min(N, s + len(sig)); buf[s:e] += sig[:e - s] * g


def env(n, a, r):
    e = np.ones(n); na, nr = min(n, max(1, int(a * SR))), min(n, max(1, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[n - nr:] *= np.linspace(1, 0, nr) ** 2; return e


def tone(f, dur, a=0.01, r=0.3, harm=(1.0, 0.35, 0.12)):
    n = max(64, int(SR * dur)); t = np.arange(n) / SR
    return sum(h * np.sin(2 * np.pi * f * (k + 1) * t) for k, h in enumerate(harm)) * env(n, a, r)


def pluck(f, dur, decay=0.995, bright=0.5):
    n = max(2, int(SR / f)); buf = R.uniform(-1, 1, n); buf -= buf.mean(); out = np.empty(max(64, int(SR * dur))); i = 0
    while i < len(out):
        k = min(n, len(out) - i); out[i:i + k] = buf[:k]; buf = decay * (bright * buf + (1 - bright) * np.roll(buf, 1)); i += k
    return out * env(len(out), 0.003, 0.05)


def filt(x, kind, f): return sosfilt(butter(2, f, btype=kind, fs=SR, output='sos'), x)
def noise(dur): return R.uniform(-1, 1, int(SR * dur))
def tick(dur, hp): return filt(noise(dur), 'highpass', hp) * env(int(SR * dur), 0.001, dur * 0.85)


def eighths(t0, t1):
    t = t0
    while t < t1 - 0.05: yield t; t += BEAT / 2


DM = [[50, 53, 57], [46, 50, 53], [48, 52, 55], [45, 49, 52]]          # Dm Bb C A  (tense)
FM = [[53, 57, 60], [48, 52, 55], [50, 53, 57], [46, 50, 53]]          # F C Dm Bb  (hopeful)
DMAJ = [50, 54, 57, 62]

for i, t in enumerate(eighths(0.0, C['sil'])):                         # 1 tense pulse
    ch = DM[(i // 8) % 4]; lift = min(1.0, t / max(1.0, C['sil']))
    put(bed, tone(midi(ch[0] - 12), 0.26, 0.005, 0.2), t, 0.5 + 0.3 * lift)
    if i % 2 == 1: put(bed, tick(0.04, 6000), t, 0.10)
    if i % 8 == 0:
        for n in ch: put(bed, tone(midi(n), BEAT * 4, 0.3, 0.6, (1, 0.2)), t, 0.06)
    if i % 16 == 0: put(bed, tone(midi(81), 0.9, 0.002, 0.85, (1,)), t, 0.07)
t = C['sil'] + 1.25                                                    # 2 low drone + heartbeat
put(bed, tone(midi(26), C['explain'] - t + 0.6, 1.0, 1.0, (1, 0.5)), t, 0.16)
put(bed, tone(midi(33), C['explain'] - t + 0.6, 1.2, 1.0, (1,)), t, 0.08)
while t < C['explain'] - 0.3:
    put(bed, tone(55, 0.18, 0.004, 0.16, (1, 0.3)), t, 0.45); put(bed, tone(55, 0.18, 0.004, 0.16, (1, 0.3)), t + 0.22, 0.3); t += 0.9
for i, t in enumerate(eighths(C['explain'], C['luck'])):               # 3 curious plucks
    ch = DM[(i // 8) % 4]
    if i % 4 == 0: put(bed, pluck(midi(ch[0] - 12), 0.9, 0.994, 0.35), t, 0.5)
    put(bed, pluck(midi(ch[i % 3] + 12), 0.3, 0.986, 0.6), t, 0.22)
    if i % 2 == 0: put(bed, tick(0.03, 5000), t, 0.07)
for i, t in enumerate(eighths(C['luck'], C['drop'])):                  # 4 hopeful lift
    ch = FM[(i // 8) % 4]; up = 1 + 0.4 * (t - C['luck']) / max(1.0, C['drop'] - C['luck'])
    if i % 4 == 0: put(bed, pluck(midi(ch[0] - 12), 1.0, 0.995, 0.35), t, 0.55)
    if i % 8 == 0:
        for n in ch: put(bed, tone(midi(n), BEAT * 4, 0.25, 0.6, (1, 0.25)), t, 0.07 * up)
    put(bed, pluck(midi([ch[0], ch[1], ch[2], ch[1]][i % 4] + 12), 0.35, 0.988, 0.7), t, 0.24 * up)
gl = max(0.3, C['slam'] - C['drop'])                                   # 5 near-silent glide
put(bed, filt(noise(gl + 0.3), 'bandpass', [500, 1800]) * env(int(SR * (gl + 0.3)), gl * 0.6, 0.25), C['drop'], 0.25)
put(bed, tone(midi(81), gl + 0.2, 0.3, 0.3, (1,)), C['drop'], 0.05)
for n in DMAJ: put(bed, tone(midi(n), LEN - C['lives'], 0.6, 1.5, (1, 0.3, 0.1)), C['lives'], 0.08)   # 6 warm resolve
put(bed, tone(midi(38), LEN - C['lives'], 0.3, 1.5, (1, 0.5)), C['lives'], 0.25)
for i, t in enumerate(eighths(C['lives'] + 0.3, LEN - 1.0)): put(bed, pluck(midi(DMAJ[i % 4] + 12), 0.5, 0.99, 0.6), t, 0.2)

for q in (C['quit1'], C['quit2']):                                     # turbine spool-downs
    tt = np.arange(int(SR * 2.0)) / SR; f = 180 + 1200 * np.exp(-tt * 2.2)
    put(fx, np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 1.6) * 0.6 + filt(noise(2.0), 'bandpass', [800, 4000]) * np.exp(-tt * 2.5) * 0.5, q)
tt = np.arange(int(SR * 1.2)) / SR                                     # boom on the nose slam
put(fx, np.sin(2 * np.pi * np.cumsum(35 + 45 * np.exp(-tt * 6)) / SR) * np.exp(-tt * 3.5) + filt(noise(1.2), 'lowpass', 400) * np.exp(-tt * 9), C['slam'])
tt = np.arange(int(SR * 1.4)) / SR; crack = np.zeros(len(tt)); idx = R.randint(0, len(tt), 160); crack[idx] = R.uniform(-1, 1, 160)
put(fx, filt(noise(1.4), 'lowpass', 900) * np.minimum(1, tt / 0.15) * np.exp(-tt * 1.6) + filt(crack, 'highpass', 1500) * 3 * np.exp(-tt * 1.2), C['fire'], 0.8)

s0, s1 = int(SR * (C['sil'] - 0.06)), int(SR * (C['sil'] + 1.25))     # true silence for "Total silence"
fd = int(SR * 0.08); bed[max(0, s0 - fd):s0] *= np.linspace(1, 0, s0 - max(0, s0 - fd)); bed[s0:s1] = 0
f0 = int(SR * (C['sil'] + 0.3)); fx[f0:s1] *= np.linspace(1, 0, s1 - f0) ** 2
lo = np.abs(bed) > 1e-4; bed *= 0.08 / max(1e-6, np.sqrt(np.mean(bed[lo] ** 2)))
fx *= 0.85 / max(1e-6, np.abs(fx).max())
mix = np.tanh((bed + fx) * 1.2) / np.tanh(1.2)
fo = int(SR * 1.5); mix[-fo:] *= np.linspace(1, 0, fo)
mix = mix / max(1e-6, np.abs(mix).max()) * 0.95
sf.write(OUT, mix.astype(np.float32), SR)
print("music %s %.1f s, cues %s" % (OUT, LEN, {k: round(v, 2) for k, v in C.items()}))
