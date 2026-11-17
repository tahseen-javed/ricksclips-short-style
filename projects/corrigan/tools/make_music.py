#!/usr/bin/env python3
"""Music + effects for the Wrong Way Corrigan Short, synthesised in code (no samples).
1930s big-band swing in B-flat at 160 bpm from frame 1: swung ride and brushes, a walking bass, a stride-piano
comp, brass stabs and a muted-trumpet riff, with a brass hit, a stamp and a prop engine on the first frame.  Over
the open sea it turns tense (minor string tremolo, heartbeat kick, rising notes, the engine drone); a record
scratch drops into a light stride-piano backstory; a tin whistle plays in Dublin; tiptoe pizzicato under the
"clouds" excuse; the full band plus a crowd for the parade; finger snaps for the sly ending; a riser into the loop.
usage: make_music.py out.wav seconds cues.json"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100; OUT, LEN = sys.argv[1], float(sys.argv[2])
if len(sys.argv) < 4:                                                   # pre-voice placeholder; build_short.py makes the real cue-timed track
    sf.write(OUT, np.zeros(int(SR * LEN), np.float32), SR); sys.exit(0)
C = json.load(open(sys.argv[3]))
N = int(SR * LEN); bed = np.zeros(N); fx = np.zeros(N); R = np.random.RandomState(5); BT = 60 / 160.0; SW = BT * 2 / 3


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
def kick(): t = ts(0.3); return sweep(140, 48, 0.3, 30) * np.exp(-t * 10)
def brush(): t = ts(0.2); return filt(noise(0.2), 'bandpass', [1800, 8000]) * np.exp(-t * 16)
def hat(): t = ts(0.05); return filt(noise(0.05), 'highpass', 7000) * np.exp(-t * 70)
def ride(): t = ts(0.5); return filt(noise(0.5), 'highpass', 5000) * np.exp(-t * 9) * 0.6 + sum(np.sin(2 * np.pi * f * t) for f in (3150, 4720, 6010)) * np.exp(-t * 7) * 0.05
def bass(f, d): t = ts(d); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(4 * np.pi * f * t) + 0.18 * np.sin(6 * np.pi * f * t)) * np.exp(-t * 3) * env(len(t), 0.005, 0.04)
def piano(f, d): t = ts(d); return sum(np.sin(2 * np.pi * f * h * t) / h ** 1.3 * np.exp(-t * (3 + 2 * h)) for h in range(1, 7)) * env(len(t), 0.003, 0.05)
def bell(f, d): t = ts(d); return sum(a * np.sin(2 * np.pi * f * k * t) for k, a in ((1, 1), (2.76, .45), (5.4, .2))) * np.exp(-t * 3)
def bowed(f, d, cut=3600, vib=0.006, n=8):                             # brass / muted trumpet / strings body
    t = ts(d); ph = 2 * np.pi * np.cumsum(f * (1 + vib * np.sin(2 * np.pi * 5.5 * t))) / SR
    return filt(sum(np.sin(k * ph) / k for k in range(1, n)), 'lowpass', cut) * env(len(t), 0.02, 0.07)
def whistle(f, d): t = ts(d); return (np.sin(2 * np.pi * f * t * (1 + 0.004 * np.sin(2 * np.pi * 6 * t))) + filt(noise(d), 'bandpass', [f * 0.9, f * 1.1]) * 0.12) * env(len(t), 0.02, 0.05)
def snap(): t = ts(0.06); return filt(noise(0.06), 'bandpass', [1800, 4200]) * np.exp(-t * 80)


CH = [(46, (58, 62, 65, 67)), (43, (59, 62, 65, 67)), (48, (58, 60, 63, 67)), (41, (57, 60, 63, 65))]      # Bb6 G7 Cm7 F7
WALK = {46: (46, 50, 53, 44), 43: (43, 47, 50, 47), 48: (48, 51, 55, 42), 41: (41, 45, 48, 45)}           # root, 3rd, 5th, approach
RIFF = [(0, 74, .5), (.67, 77, .3), (1, 79, .5), (2, 77, .5), (2.67, 74, .3), (3, 70, .9), (4.67, 71, .3), (5, 74, .5), (6, 77, .5), (7, 74, .9),
        (8, 75, .5), (8.67, 79, .3), (9, 82, .5), (10, 79, .5), (11, 75, .9), (12, 77, .5), (13, 75, .5), (14, 72, .5), (14.67, 69, .3), (15, 70, .9)]


def groove(t0, t1, kind='full'):
    i, t = 0, t0
    while t < t1 - 0.05:
        b, (rt, ch) = i % 4, CH[(i // 4) % 4]; big = kind in ('full', 'parade')
        if kind != 'sneak':
            put(bed, ride(), t, 0.10)
            if b in (1, 3): put(bed, ride(), t + SW, 0.06); put(bed, brush(), t, 0.24); put(bed, hat(), t, 0.1)
        if big and b in (0, 2): put(bed, kick(), t, 0.6)
        elif kind in ('light', 'snap') and b == 0: put(bed, kick(), t, 0.35)
        if kind in ('sneak', 'snap'):
            if b in (0, 2): put(bed, bass(midi(WALK[rt][b]), 0.16), t, 0.55)
            if b in (1, 3): put(bed, snap(), t, 0.5)
            if kind == 'sneak': put(bed, bass(midi(ch[b % 4] + 12), 0.1), t + SW, 0.18)            # tiptoe pizzicato
        else:
            put(bed, bass(midi(WALK[rt][b]), BT * 0.95), t, 0.55)
            if b in (0, 1):                                                                    # Charleston piano comp
                for n in ch: put(bed, piano(midi(n), 0.32), t if b == 0 else t + SW, 0.07)
        if big and b == 3 and (i // 4) % 2 == 1:                                               # brass stab on the and-of-4
            for n in ch: put(bed, bowed(midi(n), 0.2, 2600, 0.0, 12), t + SW, 0.05)
        if kind == 'parade' and b == 0:
            for n in ch: put(bed, bowed(midi(n + 12), BT * 1.6, 3000, 0.004, 12), t, 0.035)
        i += 1; t += BT


def riff(t0, t1, g=0.09):
    t = t0
    while t < t1 - 0.3:
        for off, m, du in RIFF:
            if t + off * BT < t1 - 0.15: put(bed, bowed(midi(m), du * BT * 1.1, 2300, 0.01), t + off * BT, g)
        t += 16 * BT


def tense(t0, t1):                                                    # over the open sea: G-minor tremolo, heartbeat, creeping line
    d = t1 - t0; t = ts(d); trem = 0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)
    for m in (43, 50, 55, 58): put(bed, bowed(midi(m), d, 1800, 0.003) * trem, t0, 0.06)
    k, tt = 0, t0
    while tt < t1 - 0.1:
        put(bed, kick(), tt, 0.55); put(bed, kick(), tt + 0.22, 0.3)
        if k % 2 == 0: put(bed, bowed(midi(67 + k // 2), BT * 1.9, 2600, 0.01), tt, 0.06)
        tt += BT * 2; k += 1


c = C
def stab(t0, g=1.0):
    for n in (46, 58, 62, 65, 67, 70): put(bed, bowed(midi(n), 0.7, 3200, 0.0, 12), t0, 0.06 * g)
    put(bed, kick(), t0, 0.9 * g)
stab(0.0)
groove(0.0, c['sea']); riff(0.0, c['sea'])
tense(c['sea'], c['punch'])
groove(c['punch'], c['yousee']); riff(c['punch'], c['yousee'], 0.1); stab(c['punch'] + 0.05, 0.8)
groove(c['yousee'], c['clouds'], 'light')
REEL = [70, 72, 74, 70, 67, 70, 65, 67, 70, 72, 74, 77, 74, 72, 70, 67]
t, k = c['climbed'], 0
while t < c['clouds'] - BT / 2: put(bed, whistle(midi(REEL[k % 16] + 12), BT * 0.48), t, 0.05); t += BT / 2; k += 1
groove(c['clouds'], c['susp'], 'sneak')
groove(c['susp'], c['parade'], 'light')
groove(c['parade'], c['never'], 'parade'); riff(c['parade'], c['never'], 0.11); stab(c['parade'])
groove(c['never'], c['because'], 'snap')
groove(c['because'], LEN, 'full'); riff(c['because'], LEN, 0.08)

# ---- effects on their words
def stampfx(): t = ts(0.35); return sweep(190, 60, 0.35, 30) * np.exp(-t * 14) + filt(noise(0.35), 'bandpass', [700, 3200]) * np.exp(-t * 30) * 0.8
def engine(d, f=62, rise=0.0):
    t = ts(d); f_ = f * (1 + rise * t / d); ph = np.cumsum(f_) / SR
    saw = 2 * (ph % 1) - 1; am = 0.65 + 0.35 * np.sign(np.sin(2 * np.pi * np.cumsum(f_ * 0.3) / SR))
    return filt(saw * am, 'lowpass', 900) * env(len(t), 0.2, 0.5) + filt(noise(d), 'lowpass', 400) * 0.3
def whoosh(d=0.8): t = ts(d); return filt(noise(d), 'bandpass', [400, 3000]) * np.sin(np.pi * t / d) ** 2
def clank(): t = ts(0.6); return sum(a * np.sin(2 * np.pi * f * t) for f, a in ((520, 1), (1340, .6), (2210, .4))) * np.exp(-t * 12)
def blips(t0, d, n, lo=300, hi=900, g=0.25):
    for k in range(n): f, tt = R.uniform(lo, hi), ts(0.09); put(fx, np.sin(2 * np.pi * f * (1 + 4 * tt) * tt) * np.exp(-tt * 35), t0 + R.uniform(0, d), g)

put(fx, stampfx(), 0.02, 1.0); put(fx, engine(2.6), 0.0, 0.5); put(fx, whoosh(1.0), 0.0, 0.5)              # frame 1: stamp, engine, whoosh
put(fx, engine(2.2, 55, 0.9), c['took'] - 0.3, 0.55); put(fx, whoosh(1.2), c['took'] + 0.8, 0.5)
for k in range(2): t = ts(0.12); put(fx, np.sin(2 * np.pi * 900 * t) * np.exp(-t * 30) + filt(noise(0.12), 'bandpass', [1500, 5000]) * np.exp(-t * 30), c['land'] + 0.35 + k * 0.22, 0.4)
put(fx, kick(), c['land'] + 0.35, 0.8)
for t0 in c['denied']: put(fx, stampfx(), t0, 1.0)
put(fx, clank(), c['tanks'], 0.5); put(fx, clank(), c['tanks'] + 0.3, 0.35)
put(fx, engine(c['punch'] - c['sea'] + 0.3, 66), c['sea'], 0.45)
t = ts(2.0); put(fx, filt(noise(2.0), 'lowpass', 700) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)) * env(len(t), 0.2, 0.5), c['flood'], 0.6); blips(c['flood'], 1.8, 12, 200, 600)
put(fx, clank(), c['punch'] + 0.05, 0.9); put(fx, stampfx(), c['punch'] + 0.05, 0.6)
for k in range(10): put(fx, np.sin(2 * np.pi * (700 - 50 * k) * ts(0.08)) * np.exp(-ts(0.08) * 30), c['punch'] + 0.4 + k * 0.08, 0.3)   # gurgle drain
t = ts(0.45); f_ = 300 + 900 * np.abs(np.sin(2 * np.pi * 2.2 * t)); put(fx, filt(noise(0.45), 'bandpass', [500, 3500]) * 0.6 + np.sin(2 * np.pi * np.cumsum(f_) / SR) * 0.5, c['yousee'] - 0.1, 0.7)  # record scratch
for k in range(3): put(fx, filt(noise(0.12), 'lowpass', 600) * np.exp(-ts(0.12) * 20), c['leftny'] + 0.1 + k * 0.28, 0.7)   # engine coughs
put(fx, engine(2.0, 60, 0.4), c['leftny'] + 0.9, 0.45)
for k in range(6): put(fx, filt(noise(0.03), 'highpass', 2500) * np.exp(-ts(0.03) * 120), c['plan'] + k * 0.11, 0.6)
put(fx, bell(midi(96), 0.9), c['plan'] + 0.75, 0.25)
for k in range(14): put(fx, filt(noise(0.03), 'highpass', 3000) * np.exp(-ts(0.03) * 120), c['hours'] + 1.6 * (1 - (1 - k / 14.0) ** 1.6), 0.45)
t = ts(1.6); put(fx, np.sin(2 * np.pi * np.cumsum(300 + 600 * (t / 1.6) ** 2) / SR) * env(len(t), 0.3, 0.1), c['hours'], 0.12)
put(fx, kick(), c['climbed'], 0.7)
t = ts(0.9); put(fx, np.sin(2 * np.pi * np.cumsum(330 * (1 + 0.35 * np.sin(2 * np.pi * 11 * t) * np.exp(-t * 3))) / SR) * np.exp(-t * 3), c['wrong'], 0.45)   # boing
put(fx, whoosh(1.4), c['clouds'] - 0.1, 0.5)
t = ts(0.5); put(fx, np.sin(2 * np.pi * np.cumsum(600 + 900 * t / 0.5) / SR) * env(len(t), 0.05, 0.1), c['clouds'] + 1.0, 0.18)      # innocent slide whistle
put(fx, stampfx(), c['susp'], 1.0)
t = ts(1.5)
for f in (110, 165): put(fx, filt(2 * ((np.cumsum(np.full(len(t), f)) / SR) % 1) - 1, 'lowpass', 700) * env(len(t), 0.08, 0.4), c['ship'], 0.35)   # ship horn
t = ts(3.0); crowd = sum(filt(noise(3.0), 'bandpass', [f, f * 2.2]) * (0.6 + 0.4 * np.sin(2 * np.pi * r * t + p)) for f, r, p in ((500, 3, 0), (800, 4.2, 1), (1200, 2.5, 2)))
put(fx, crowd * env(len(t), 0.2, 1.0), c['parade'], 0.35); put(fx, crowd * env(len(t), 0.2, 1.0), c['wwc'], 0.3)
blips(c['parade'], 2.5, 16, 1500, 3000, 0.12)
for k in range(2): put(fx, bell(midi(88), 0.8), c['lindy'] + 0.2 + k * 0.18, 0.3)
for k, m in enumerate((70, 74, 77, 82)): put(fx, bowed(midi(m), 0.16 if k < 3 else 0.7, 3200, 0.0, 12), c['wwc'] + k * 0.13, 0.25)
put(fx, bell(midi(96), 0.7), c['purpose'], 0.25)
t = ts(LEN - c['because']); put(fx, filt(noise(LEN - c['because']), 'bandpass', [600, 5000]) * (t / t[-1]) ** 2, c['because'], 0.35)        # riser into the loop
put(fx, engine(LEN - c['loop'], 62), c['loop'], 0.45)

lo = np.abs(bed) > 1e-4; bed *= 0.1 / max(1e-6, np.sqrt(np.mean(bed[lo] ** 2)))
fx *= 0.85 / max(1e-6, np.abs(fx).max())
mix = np.tanh((bed + fx) * 1.2) / np.tanh(1.2); f = int(SR * 0.12); mix[-f:] *= np.linspace(1, 0, f)
sf.write(OUT, (mix / max(1e-6, np.abs(mix).max()) * 0.95).astype(np.float32), SR)
print("music %s %.1f s" % (OUT, LEN))
