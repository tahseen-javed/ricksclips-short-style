#!/usr/bin/env python3
"""Music + effects for the Vasa Short, synthesised in code (no samples).
A driving 6/8 sea shanty in A minor from frame 1 (kick, snare, hats, oom-pah bass, accordion chops, a big chord
and a splash on the first frame); a timpani roll as the water pours in; the groove muffled underwater on the
seabed with a low drone and bubbles; a dead stop on "How?"; playful pizzicato for the shipworms; icy bells, wind
and a sad trombone in the Baltic; war taiko for the what-if; a fiddle jig for the museum; effects on their words.
usage: make_music.py out.wav seconds cues.json"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100; OUT, LEN = sys.argv[1], float(sys.argv[2])
if len(sys.argv) < 4:                                                   # pre-voice placeholder; build_short.py makes the real cue-timed track
    sf.write(OUT, np.zeros(int(SR * LEN), np.float32), SR); sys.exit(0)
C = json.load(open(sys.argv[3]))
N = int(SR * LEN); bed = np.zeros(N); fx = np.zeros(N); R = np.random.RandomState(4); E8 = 0.19      # eighth note: a 6/8 bar is 1.14 s


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
def kick(): t = ts(0.35); return sweep(150, 46, 0.35, 32) * np.exp(-t * 9)
def taiko(): t = ts(0.5); return sweep(170, 90, 0.5, 20) * np.exp(-t * 6) + filt(noise(0.5), 'lowpass', 600) * np.exp(-t * 25) * 0.6
def snare(): t = ts(0.22); return filt(noise(0.22), 'bandpass', [1200, 6000]) * np.exp(-t * 18) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 25) * 0.5
def hat(): t = ts(0.05); return filt(noise(0.05), 'highpass', 7000) * np.exp(-t * 70)
def pluck(f, d, k=5.0): t = ts(d); return sum(np.sin(2 * np.pi * f * h * t) / h * np.exp(-t * (k + 3 * h)) for h in range(1, 6))
def bell(f, d): t = ts(d); return sum(a * np.sin(2 * np.pi * f * k * t) for k, a in ((1, 1), (2.76, .45), (5.4, .2))) * np.exp(-t * 3)
def acc(f, d):                                                          # accordion-like reed chop, two detuned squares
    t = ts(d); v = 1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)
    return filt(sum(np.sign(np.sin(2 * np.pi * f * dt * np.cumsum(v) / SR)) for dt in (0.997, 1.003)), 'lowpass', 2400) * env(len(t), 0.01, 0.05)
def bowed(f, d, cut=3600, vib=0.006):                                   # fiddle / trombone body
    t = ts(d); ph = 2 * np.pi * np.cumsum(f * (1 + vib * np.sin(2 * np.pi * 6 * t))) / SR
    return filt(sum(np.sin(k * ph) / k for k in range(1, 8)), 'lowpass', cut) * env(len(t), 0.03, 0.06)


AM = [(45, (57, 60, 64)), (41, (57, 60, 65)), (48, (55, 60, 64)), (43, (55, 59, 62))]       # Am F C G


def groove(buf, t0, t1, kind='full'):
    i, t = 0, t0
    while t < t1 - 0.05:
        b, (bs, ch) = i % 6, AM[(i // 6) % 4]
        if b == 0 or (b == 3 and kind in ('full', 'war', 'tri')): put(buf, kick(), t, 0.9)
        if b == 3 and kind != 'thin': put(buf, snare(), t, 0.25 if kind == 'pizz' else 0.42)
        if kind in ('war', 'tri') and b == 5: put(buf, taiko(), t, 0.5)
        if kind == 'war' and b in (1, 2): put(buf, taiko(), t, 0.32)
        put(buf, hat(), t, 0.16 if b in (0, 3) else 0.08)
        if b in (0, 3): put(buf, pluck(midi(bs - 12 + (7 if b == 3 else 0)), 0.32, 6), t, 0.55)
        if kind == 'pizz': put(buf, pluck(midi(ch[(i * 2) % 3] + 12), 0.16, 14), t, 0.2)
        elif kind == 'thin':
            if b == 0: put(buf, bell(midi(ch[0] + 24), 1.4), t, 0.1)
        elif b in (1, 2, 4, 5):
            for n in ch: put(buf, acc(midi(n), E8 * 0.62), t, 0.035)
        i += 1; t += E8


def muffled(t0, t1, kind):
    u = np.zeros(N); groove(u, t0, t1, kind); bed[:] += filt(u, 'lowpass', 420) * 1.5
    t = ts(t1 - t0); put(bed, filt(sum(np.sin(2 * np.pi * midi(33) * k * t) / k for k in range(1, 6)), 'lowpass', 260) * env(len(t), 0.3, 0.4), t0, 0.5)


c = C
for n in (45, 57, 64, 69, 72): put(bed, pluck(midi(n), 1.4, 2.5), 0.0, 0.3)                    # big chord on frame 1
groove(bed, 0.0, c['seabed'])
n_ = max(1, int((c['seabed'] - c['rush']) / 0.07))
for k in range(n_): put(bed, taiko(), c['rush'] + k * 0.07, 0.06 + 0.3 * k / n_)              # timpani roll as she floods
muffled(c['seabed'], c['up'], 'full')
groove(bed, c['up'], c['how'])                                                                   # back up: full again, then a dead stop on How?
groove(bed, c['yousee'], c['baltic'], 'pizz')
groove(bed, c['baltic'], c['s333'], 'thin')
muffled(c['s333'], c['today'], 'pizz')
groove(bed, c['today'], c['war'], 'tri'); groove(bed, c['war'], c['instead'], 'war'); groove(bed, c['instead'], LEN, 'tri')
JIG = [69, 72, 76, 74, 72, 71, 69, 71, 72, 74, 72, 71, 72, 76, 79, 77, 76, 74, 76, 74, 72, 71, 69, 67]
for a, b in ((c['today'], c['war']), (c['instead'], LEN - 0.2)):
    t, k = a, 0
    while t < b - E8: put(bed, bowed(midi(JIG[k % 24]), E8 * 0.95), t, 0.06); t += E8; k += 1
for n in (45, 57, 64, 69, 72): put(bed, pluck(midi(n), 1.4, 2.5), c['splash'][1], 0.3)        # the loop chord again

# ---- effects on their words
def splash_fx(): t = ts(1.2); return filt(noise(1.2), 'lowpass', 3200) * np.exp(-t * 3.5) * 0.8 + sweep(95, 38, 1.2, 5) * np.exp(-t * 4)
def cannon(): t = ts(0.9); return sweep(120, 34, 0.9, 7) * np.exp(-t * 5) + filt(noise(0.9), 'lowpass', 1400) * np.exp(-t * 7) * 0.7
def poof(): t = ts(0.4); return filt(noise(0.4), 'bandpass', [300, 2200]) * np.exp(-t * 9)
def creak():
    t = ts(1.0); ph = np.cumsum(40 + 30 * np.sin(2 * np.pi * 1.1 * t)) / SR
    return filt(((ph % 1) < 0.06).astype(float), 'bandpass', [350, 1800]) * env(len(t), 0.05, 0.3) * 3
def gullc(): t = ts(0.22); return np.sin(2 * np.pi * np.cumsum(1300 + 700 * np.exp(-t * 14) + 60 * np.sin(2 * np.pi * 30 * t)) / SR) * env(len(t), 0.01, 0.08)
def blips(t0, d, n):
    for k in range(n): f, tt = R.uniform(300, 900), ts(0.09); put(fx, np.sin(2 * np.pi * f * (1 + 4 * tt) * tt) * np.exp(-tt * 35), t0 + R.uniform(0, d), 0.25)

for t0 in c['splash']: put(fx, splash_fx(), t0, 1.0)
for k in range(3): put(fx, gullc(), c['gull'] + 0.15 + k * 0.3, 0.22)
put(fx, bell(midi(57), 2.4) + bell(midi(45), 2.4) * 0.6, c['bell'], 0.45)                       # church bell on 1628
for t0 in c['cannon']: put(fx, cannon(), t0, 0.9)
for k in range(22): put(fx, filt(noise(0.06), 'lowpass', 500) * np.exp(-ts(0.06) * 50), c['run'] + k * 0.11, 0.5)     # thirty pairs of feet
t = ts(0.7); put(fx, np.sin(2 * np.pi * np.cumsum(2700 + 180 * np.sign(np.sin(2 * np.pi * 22 * t))) / SR) * env(len(t), 0.01, 0.1), c['whistle'], 0.35)
for t0 in c['creak']: put(fx, creak(), t0, 0.7)
t = ts(1.3); put(fx, filt(noise(1.3), 'bandpass', [250, 1600]) * np.sin(np.pi * t / 1.3) ** 2, c['gust'] - 0.2, 0.8)
t = ts(1.8); put(fx, filt(noise(1.8), 'bandpass', [400, 5000]) * env(len(t), 0.15, 0.6) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t)), c['rush'], 0.6)
t = ts(0.8); put(fx, sweep(80, 30, 0.8, 6) * np.exp(-t * 5) + filt(noise(0.8), 'lowpass', 300) * np.exp(-t * 6), c['seabed'], 1.0)
blips(c['seabed'], 1.6, 14); blips(c['up'], 1.4, 12); blips(c['s333'], 3.0, 10)
t = ts(1.4); put(fx, filt(noise(1.4), 'bandpass', [300, 3000]) * (t / 1.4) ** 2, c['up'] - 0.2, 0.8); put(fx, splash_fx(), c['up'] + 1.1, 0.7)
t = ts(1.2); put(fx, sum(a * np.sin(2 * np.pi * 1320 * k * t) for k, a in ((1, 1), (2.76, .5), (5.4, .25))) * np.exp(-t * 4), c['whole'], 0.45)
t = ts(0.5); put(fx, np.sin(2 * np.pi * 1760 * t) * np.exp(-t * 9), c['how'], 0.4)
for k in range(4): put(fx, filt(noise(0.08), 'bandpass', [1500, 6000]) * np.exp(-ts(0.08) * 40), c['munch'] + k * 0.12, 0.6)
for t0 in c['poof']: put(fx, poof(), t0, 0.8)
t = ts(2.0); put(fx, filt(noise(2.0), 'bandpass', [500, 2500]) * np.sin(np.pi * t / 2) ** 2, c['baltic'], 0.35)
for k, m in enumerate((96, 100, 103, 108)): put(fx, bell(midi(m), 1.2), c['baltic'] + 0.1 + k * 0.12, 0.12)
for k, m in enumerate((58, 57, 56)): put(fx, bowed(midi(m), 0.32, 1300, 0.0), c['sad'] + k * 0.34, 0.5)                 # wah wah wah
put(fx, bowed(midi(55), 0.9, 1300, 0.02), c['sad'] + 1.02, 0.5)                                                          # waaah
for k in range(10): put(fx, filt(noise(0.03), 'highpass', 3000) * np.exp(-ts(0.03) * 120), c['s333'] + 0.2 + k * 0.25, 0.45)
put(fx, bell(midi(84), 1.0), c['untouched'], 0.3); put(fx, bell(midi(88), 1.0), c['untouched'] + 0.1, 0.3)
put(fx, cannon(), c['war'] + 0.1, 0.8)
t = ts(0.7); put(fx, filt(noise(0.7), 'lowpass', 900) * np.exp(-t * 5) * (R.uniform(0, 1, len(t)) > 0.7), c['rot'], 0.8)
t = ts(1.2); put(fx, filt(noise(1.2), 'bandpass', [200, 3000]) * env(len(t), 0.05, 0.5) * (0.6 + 0.4 * (R.uniform(0, 1, len(t)) > 0.97)), c['burn'], 0.6)
put(fx, splash_fx(), c['sunk'] + 0.2, 0.7)
t = ts(2.2); crowd = sum(filt(noise(2.2), 'bandpass', [f, f * 2.2]) * (0.6 + 0.4 * np.sin(2 * np.pi * r * t + p)) for f, r, p in ((500, 3, 0), (800, 4.2, 1), (1200, 2.5, 2)))
put(fx, crowd * env(len(t), 0.15, 0.8), c['cheer'], 0.35)
t = ts(0.7); put(fx, filt(np.sign(np.sin(2 * np.pi * 110 * t)) + np.sign(np.sin(2 * np.pi * 116 * t)), 'lowpass', 1500) * env(len(t), 0.01, 0.1), c['worst'], 0.3)

lo = np.abs(bed) > 1e-4; bed *= 0.1 / max(1e-6, np.sqrt(np.mean(bed[lo] ** 2)))
fx *= 0.85 / max(1e-6, np.abs(fx).max())
mix = np.tanh((bed + fx) * 1.2) / np.tanh(1.2); f = int(SR * 0.12); mix[-f:] *= np.linspace(1, 0, f)
sf.write(OUT, (mix / max(1e-6, np.abs(mix).max()) * 0.95).astype(np.float32), SR)
print("music %s %.1f s" % (OUT, LEN))
