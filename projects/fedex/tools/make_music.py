#!/usr/bin/env python3
"""Music + effects for the FedEx blackjack Short, synthesised in code (no samples).
1973 funk in E minor at 112 bpm from frame 1: tight kick/snare, 16th hats, slap bass with octave pops, a clavinet
comp, wah-guitar scratches and brass stabs, with a brass hit, chips and a "21" bell on the first frame.  When the cash
falls it turns tense (heartbeat kick, low drone, minor stabs); a record scratch drops into a light backstory groove;
casino glitter (slot bells) for Las Vegas, a brass fanfare + ka-ching for the win, stop-time hits for "not a strategy",
jet engines when the jets keep flying, a soft clav breakdown at Yale with a sad trombone for the C, and the full band
plus a crowd and a riser into the loop.
usage: make_music.py out.wav seconds cues.json"""
import sys, json
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

SR = 44100; OUT, LEN = sys.argv[1], float(sys.argv[2])
if len(sys.argv) < 4:                                                   # pre-voice placeholder; build_short.py makes the real cue-timed track
    sf.write(OUT, np.zeros(int(SR * LEN), np.float32), SR); sys.exit(0)
C = json.load(open(sys.argv[3]))
N = int(SR * LEN); bed = np.zeros(N); fx = np.zeros(N); R = np.random.RandomState(6); BT = 60 / 112.0; SX = BT / 4


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
def kick(): t = ts(0.32); return sweep(160, 46, 0.32, 34) * np.exp(-t * 9)
def snare(): t = ts(0.22); return filt(noise(0.22), 'bandpass', [1200, 7000]) * np.exp(-t * 18) + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 24) * 0.6
def hat(o=False): d = 0.22 if o else 0.05; t = ts(d); return filt(noise(d), 'highpass', 7500) * np.exp(-t * (14 if o else 75))
def slap(f, d): t = ts(d); return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 20) + 0.25 * np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t * 40)) * np.exp(-t * 5) * env(len(t), 0.003, 0.03)
def clav(f, d): t = ts(d); x = sum(np.sin(2 * np.pi * f * h * t) / h ** 0.8 * np.exp(-t * (8 + 4 * h)) for h in range(1, 8)); return filt(x, 'highpass', 300) * env(len(t), 0.002, 0.03)
def brass(f, d, cut=3800):
    t = ts(d); ph = 2 * np.pi * f * t * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * t)); x = sum(np.sin(ph * h) / h for h in range(1, 9))
    return filt(x, 'lowpass', cut) * env(len(t), 0.03, 0.08)
def wah(t0, f0, f1):                                                    # wah guitar scratch: muted strum through a sweeping band
    d = 0.12; x = filt(noise(d), 'bandpass', [min(f0, f1), max(f0, f1)]) * np.exp(-ts(d) * 30); put(bed, x, t0, 0.22)
def bell(f, d): t = ts(d); return sum(a * np.sin(2 * np.pi * f * k * t) for k, a in ((1, 1), (2.76, .45), (5.4, .2))) * np.exp(-t * 3)
def stampfx(): t = ts(0.35); return sweep(190, 60, 0.35, 30) * np.exp(-t * 14) + filt(noise(0.35), 'bandpass', [700, 3200]) * np.exp(-t * 30) * 0.8
def whoosh(d=0.8, lo=400, hi=3000): t = ts(d); return filt(noise(d), 'bandpass', [lo, hi]) * np.sin(np.pi * t / d) ** 2
def engine(d, f=70, rise=0.0):
    t = ts(d); fr = f * (1 + rise * t / d); x = np.sin(2 * np.pi * np.cumsum(fr) / SR) + 0.5 * filt(noise(d), 'bandpass', [600, 3800])
    return x * env(len(t), 0.25, 0.4)
def chipsfx(n=7):
    x = np.zeros(int(SR * 0.6))
    for k in range(n):
        t = ts(0.06); c = sum(np.sin(2 * np.pi * f * t) for f in (2400 + 300 * R.rand(), 3900 + 400 * R.rand())) * np.exp(-t * 90); s = int(SR * (k * 0.05 + 0.02 * R.rand()))
        x[s:s + len(c)] += c[:len(x) - s]
    return x * 0.5
def kaching(): t = ts(0.9); c = np.zeros(len(t)); c[:int(SR * 0.6)] = chipsfx(4) * 0.6; return c + (np.sin(2 * np.pi * 2093 * t) + np.sin(2 * np.pi * 2637 * t)) * np.exp(-t * 4) * (t > 0.08) * 0.5
def flip(): t = ts(0.08); return filt(noise(0.08), 'bandpass', [1500, 6000]) * np.exp(-t * 60)
def scratch(): t = ts(0.5); return np.sin(2 * np.pi * np.cumsum(900 + 700 * np.sin(2 * np.pi * 7 * t)) / SR) * filt(noise(0.5), 'bandpass', [500, 3000]) * env(len(t), 0.01, 0.1) * 3
def boing(): t = ts(0.6); return np.sin(2 * np.pi * np.cumsum(220 + 160 * np.sin(2 * np.pi * 9 * t) * np.exp(-t * 4)) / SR) * np.exp(-t * 4)
def beep(f=1320, d=0.12): t = ts(d); return np.sin(2 * np.pi * f * t) * env(len(t), 0.005, 0.03)
def cheer(d):
    t = ts(d); x = filt(noise(d), 'bandpass', [500, 2600]) * (0.7 + 0.3 * np.sin(2 * np.pi * 3.1 * t)) * env(len(t), 0.2, 0.6)
    for k in range(int(d * 5)): put_ = int(R.rand() * (len(t) - SR // 4)); w = sweep(900 + 500 * R.rand(), 600, 0.25, 6) * np.exp(-ts(0.25) * 6) * 0.3; x[put_:put_ + len(w)] += w
    return x
def riser(d): t = ts(d); return (filt(noise(d), 'highpass', 2000) * 0.4 + np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR) * 0.3) * (t / d) ** 2


CH = [(40, (64, 67, 71, 74)), (45, (64, 67, 69, 73)), (40, (64, 67, 71, 74)), (47, (63, 66, 69, 71))]      # Em7 A7 Em7 B7, one bar each
BASS = [(0, 0, .2), (3, 0, .1), (4, 12, .1), (6, 10, .1), (8, 0, .2), (10, 7, .1), (11, 10, .1), (14, 12, .12)]  # (16th, interval, length)


def groove(t0, t1, kind='full'):
    b = int(np.ceil(t0 / (4 * BT) - 1e-6)) if t0 > 0 else 0
    t = t0
    while t < t1 - 1e-3:
        bar = int(round(t / (4 * BT))); root, chord = CH[bar % 4]
        for st in range(16):
            u = bar * 4 * BT + st * SX
            if u < t0 - 1e-3 or u >= t1: continue
            if kind != 'tense':
                if st in (0, 6, 8, 10 if bar % 2 else 99): put(bed, kick(), u, 0.9)
                if st in (4, 12): put(bed, snare(), u, 0.55 if kind == 'lite' else 0.7)
                put(bed, hat(st == 14), u, (0.22 if st % 4 == 2 else 0.13) * (0.7 if kind == 'lite' else 1))
                for s_, iv, ln in BASS:
                    if s_ == st: put(bed, slap(midi(root + iv - 12), ln * 4 * BT), u, 0.55)
                if st in (2, 6, 10, 13): put(bed, sum(clav(midi(m), 0.16) for m in chord), u, 0.07)
                if kind == 'full' and st % 2 == 1: wah(u, 500 + 2200 * (st / 16.0), 900 + 2400 * (st / 16.0))
                if kind == 'full' and st in (0, 7) and bar % 2 == 1: put(bed, sum(brass(midi(m), 0.22) for m in chord), u, 0.05)
            else:
                if st in (0, 3): put(bed, kick(), u, 0.9)                              # heartbeat
                if st == 0: put(bed, sum(brass(midi(m - 12), 0.5, 1600) for m in (64, 67, 70)), u, 0.04)
        t = (bar + 1) * 4 * BT


def section(t0, t1, kind): groove(t0, t1, kind)


def tense(t0, t1):
    section(t0, t1, 'tense'); d = t1 - t0; t = ts(d)
    put(bed, np.sin(2 * np.pi * 41.2 * t) * env(len(t), 0.3, 0.3) * 0.5 + filt(noise(d), 'lowpass', 300) * 0.3, t0)
    for k, m in enumerate((52, 53, 55, 56, 58, 59)):                         # creeping line
        u = t0 + k * d / 6; put(bed, brass(midi(m), d / 6 * 0.9, 2200), u, 0.05)


def stab(t, g=1.0): put(fx, sum(brass(midi(m), 0.3) for m in (64, 67, 71, 76)) + kick() [:int(SR * 0.3)] * 0.0, t, 0.11 * g); put(fx, snare(), t, 0.5 * g)
def fanfare(t):
    for k, (m, d) in enumerate(((71, .14), (74, .14), (76, .14), (79, .6))): put(fx, sum(brass(midi(m + x), d) for x in (0, -5, -12)), t + k * 0.13, 0.09)
def slots(t, n=8):
    for k in range(n): put(fx, bell(midi(84 + (0, 4, 7, 12)[k % 4]), 0.4), t + k * 0.07, 0.07)
def sadbone(t):
    for k, m in enumerate((58, 57, 56, 55)): put(fx, brass(midi(m), 0.32 if k < 3 else 0.8, 1400) * (1 + 0.3 * np.sin(2 * np.pi * 6 * ts(0.32 if k < 3 else 0.8))), t + k * 0.3, 0.12)


# ---------------------------------------------------------------- the score
section(0, C['tense'], 'full')
tense(C['tense'], C['yousee'])
section(C['yousee'] + 0.35, C['flew'], 'lite')
section(C['flew'], C['notstrat'], 'full')
section(C['lifeline'], C['idea'], 'full')
section(C['idea'], C['saved'], 'lite')
section(C['saved'], C['end'], 'full')

# ---------------------------------------------------------------- effects on the beats
stab(0.0, 1.3); put(fx, chipsfx(9), 0.02, 0.5); put(fx, bell(midi(88), 1.2), 0.05, 0.12); put(fx, whoosh(0.5, 1200, 6000), 0.0, 0.25)
put(fx, engine(1.6, 90, 0.8), C['takeoff'] - 0.1, 0.18); put(fx, whoosh(1.2, 300, 2000), C['takeoff'], 0.3)
put(fx, chipsfx(8), C['bet'], 0.5); put(fx, bell(midi(81), 0.8), C['vegas'], 0.1); slots(C['vegas'] + 0.1, 6)
put(fx, flip(), C['april'], 0.5); stab(C['launch'], 0.8); put(fx, engine(2.2, 62), C['launch'], 0.08)
for k in range(6): put(fx, beep(880 + 110 * k, 0.07), C['first'] + 0.25 + 0.2 * k, 0.07)
for k in range(8): put(fx, beep(1200 + 150 * k, 0.06), C['cities'] + 0.05 * k, 0.06)
put(fx, boing(), C['cmp'], 0.12); put(fx, sweep(300, 1400, 1.0, -1.5) * env(SR, 0.05, 0.2), C['fuel'], 0.06)
put(fx, whoosh(0.9, 800, 5000), C['vanish'], 0.3); put(fx, stampfx(), C['fell'], 0.55); sadbone(C['nowhere'] + 0.2)
put(fx, scratch(), C['yousee'] - 0.05, 0.14); stab(C['fred'], 0.8); put(fx, stampfx(), C['teach'], 0.55)
put(fx, engine(1.4, 80, 0.5), C['flew'], 0.12); put(fx, whoosh(1.0), C['flew'] + 0.1, 0.25); slots(C['sat'], 8)
for k in range(2): put(fx, flip(), C['deal'] + 0.15 * k, 0.6)
for k in range(2): put(fx, flip(), C['turned'] + 0.1 + 0.3 * k, 0.6)
fanfare(C['won']); put(fx, kaching(), C['won'], 0.45); put(fx, chipsfx(10), C['won'] + 0.1, 0.5); put(fx, cheer(1.4), C['won'], 0.12)
put(fx, stampfx(), C['paid'], 0.55); put(fx, kaching(), C['paid'] + 0.1, 0.3)
put(fx, stampfx(), C['notstrat'], 0.6); stab(C['notstrat'] + 0.02, 1.0); stab(C['strategy'], 1.0); put(fx, boing(), C['lifeline'], 0.16)
put(fx, engine(2.4, 76, 1.0), C['jets'], 0.16); put(fx, whoosh(1.4, 300, 2500), C['jets'] + 0.2, 0.3); stab(C['inv'], 0.8)
put(fx, kaching(), C['eleven'], 0.4); for_ = [put(fx, beep(1000, 0.1), C['alive'] - 0.5 + 0.45 * k, 0.1) for k in range(3)]
put(fx, bell(midi(76), 1.0), C['idea'] + 0.1, 0.1); put(fx, flip(), C['yale'], 0.4); put(fx, stampfx(), C['grade'], 0.6); sadbone(C['grade'] + 0.15)
put(fx, chipsfx(8), C['saved'], 0.5); stab(C['today'], 1.2); put(fx, cheer(C['end'] - C['today']), C['today'], 0.14)
put(fx, riser(1.2), C['loop'] - 0.9, 0.22); stab(C['loop'], 1.1)

mix = bed * 0.9 + fx
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 1.6) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, funk 112 bpm, E minor" % LEN)
