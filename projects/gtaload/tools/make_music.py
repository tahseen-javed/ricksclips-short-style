#!/usr/bin/env python3
"""Music + effects for video 12 (GTA Online loading screen boss), synthesised in code (no samples).
Boss-battle rock 150/160 bpm (Em power chords, double kick) from frame 1; bossa-nova waiting music 118 bpm with a ticking clock;
mysterious electro arp 112 bpm inside the code; bright piano house 124 bpm for the fix and payout; rock again for the loop.
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
BT = 60 / 124.0; SW = BT * 2 / 3                                        # swung off-beat


def pluck(f, d): t = ts(d); return (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 12)) * np.exp(-t * 5) * env(len(t), 0.004, 0.04)
def piano(f, d): t = ts(d); return sum(np.sin(2 * np.pi * f * h * t) / h ** 1.3 * np.exp(-t * (3 + 2.5 * h)) for h in range(1, 6)) * env(len(t), 0.002, 0.05)
def clap(): t = ts(0.2); x = filt(noise(0.2), 'bandpass', [900, 5000]); e = sum(np.exp(-np.clip(t - o, 0, None) * 60) * (t >= o) for o in (0, 0.012, 0.024)); return x * e * 0.8
def jingle(): t = ts(0.14); return filt(noise(0.14), 'highpass', 6500) * (np.exp(-t * 40) + 0.5 * np.exp(-np.abs(t - 0.03) * 80)) * (1 + 0.5 * np.sin(2 * np.pi * 70 * t))
def saw(f, d, cut=1800): t = ts(d); return filt(sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 12)), 'lowpass', cut) * env(len(t), 0.005, 0.04)
def sq(f, d): t = ts(d); return filt(np.sign(np.sin(2 * np.pi * f * t)), 'lowpass', 4000) * env(len(t), 0.004, 0.03) * 0.5
def gated():                                                            # 80s gated-reverb snare
    t = ts(0.32); x = np.zeros(len(t)); s = snare(); x[:len(s)] += s; return x + filt(noise(0.32), 'bandpass', [800, 6000]) * (t < 0.26) * 0.35
def whistle(d=0.6): t = ts(d); return np.sin(2 * np.pi * np.cumsum(2900 + 260 * np.sign(np.sin(2 * np.pi * 26 * t))) / SR) * env(len(t), 0.01, 0.06)
def siren(d=1.2): t = ts(d); return np.sin(2 * np.pi * np.cumsum(780 + 420 * np.sin(2 * np.pi * t / 0.6)) / SR) * env(len(t), 0.05, 0.15)
def horn(f=330): t = ts(0.32); return filt(np.sign(np.sin(2 * np.pi * f * t)) + np.sign(np.sin(2 * np.pi * f * 1.26 * t)), 'lowpass', 2200) * env(len(t), 0.01, 0.05) * 0.4
def gobble(): t = ts(0.5); return np.sin(2 * np.pi * np.cumsum(420 + 260 * np.sin(2 * np.pi * 22 * t)) / SR) * env(len(t), 0.01, 0.08)
def tick(): t = ts(0.03); return filt(noise(0.03), 'highpass', 3000) * np.exp(-t * 200)
def buzzer(): t = ts(0.6); return filt(np.sign(np.sin(2 * np.pi * 116 * t)) + np.sign(np.sin(2 * np.pi * 121 * t)), 'lowpass', 2500) * env(len(t), 0.005, 0.05) * 0.5
def crickets(d):
    x = np.zeros(int(SR * d))
    for k in range(int(d * 3)):
        for j in range(3):
            t = ts(0.03); c = np.sin(2 * np.pi * 4700 * t) * np.sin(np.pi * t / 0.03); s = int(SR * (k / 3.0 + j * 0.05))
            if s + len(c) <= len(x): x[s:s + len(c)] += c
    return x
def boom(): t = ts(1.2); return sweep(110, 32, 1.2, 4) * np.exp(-t * 2.5) + filt(noise(1.2), 'lowpass', 200) * np.exp(-t * 5) * 0.5




# ---------------------------------------------------------------- video 09 instruments
def twang(f, d): t = ts(d); fr = f * (1 - 0.03 * np.exp(-t * 30)); x = sum(np.sin(2 * np.pi * np.cumsum(fr * h) / SR) / h ** 0.9 for h in range(1, 8)); return np.tanh(x * 1.5) * np.exp(-t * 4) * env(len(t), 0.002, 0.04)
def whis(f, d): t = ts(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 0.012 * np.sin(2 * np.pi * 6 * t))) / SR) * env(len(t), 0.03, 0.08)
def whip(): t = ts(0.25); return filt(noise(0.25), 'highpass', 2500) * np.exp(-t * 40) + np.sin(2 * np.pi * np.cumsum(3000 - 2500 * t / 0.25) / SR) * np.exp(-t * 30) * 0.4
def banjo(f): t = ts(0.3); return sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 7)) * np.exp(-t * 14) * env(len(t), 0.001, 0.02)
def fiddle(f, d): t = ts(d); return filt(sum(np.sin(2 * np.pi * np.cumsum(f * h * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t))) / SR) / h for h in range(1, 9)), 'bandpass', [300, 3500]) * env(len(t), 0.06, 0.08)
def gunfire(d, rate=11):
    x = np.zeros(int(SR * d) + SR // 5)
    for k in range(int(d * rate)):
        i = int(SR * k / rate); g = filt(noise(0.07), 'bandpass', [300, 4500]) * np.exp(-ts(0.07) * 55) + sweep(240, 70, 0.07, 40) * np.exp(-ts(0.07) * 45) * 0.8; x[i:i + len(g)] += g
    return x
def thumps(d):
    x = np.zeros(int(SR * d) + SR // 4)
    for k in range(int(d * 9)): i = int(SR * (k / 9.0 + 0.03 * R.rand())); g = sweep(120, 50, 0.18, 20) * np.exp(-ts(0.18) * 18); x[i:i + len(g)] += g * (0.6 + 0.4 * R.rand())
    return x
def crunch(): t = ts(0.22); return filt(noise(0.22), 'bandpass', [1500, 6500]) * (np.abs(np.sin(2 * np.pi * 34 * t)) ** 3) * np.exp(-t * 6)
def poof(): t = ts(0.4); return filt(noise(0.4), 'bandpass', [800, 3000]) * np.sin(np.pi * t / 0.4) ** 2
def wind(d): t = ts(d); return filt(noise(d), 'bandpass', [200, 900]) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.4 * t)) * env(len(t), 0.3, 0.4)
def drum_roll(d):
    x = np.zeros(int(SR * d) + SR // 4)
    for k in range(int(d / 0.045)): s = snare() * (0.35 + 0.65 * k * 0.045 / d); i = int(SR * k * 0.045); x[i:i + len(s)] += s[:len(x) - i]
    return x
def sadbone(t):
    for k, m in enumerate((62, 61, 60, 59)): d = 0.28 if k < 3 else 0.8; put(fx, brass(midi(m), d, 1400) * (1 + 0.3 * np.sin(2 * np.pi * 6 * ts(d))), t + k * 0.26, 0.11)
def fanfare(t, base=76):
    for k, (m, d) in enumerate(((0, .14), (4, .14), (7, .14), (12, .6))): put(fx, sum(brass(midi(base + m + x), d) for x in (0, -5, -12)), t + k * 0.13, 0.085)
def stab(t, g=1.0): put(fx, sum(twang(midi(m), 0.5) for m in (52, 59, 64)), t, 0.12 * g); put(fx, boom(), t, 0.35 * g); put(fx, kick(), t, 0.6 * g)



def b808(f, d): t = ts(d); fr = f * (1 + 0.6 * np.exp(-t * 30)); return np.tanh(np.sin(2 * np.pi * np.cumsum(fr) / SR) * 2.2) * np.exp(-t * 2.2) * env(len(t), 0.003, 0.06)
def chip(f, d, duty=0.25): t = ts(d); ph = (f * t) % 1.0; return ((ph < duty) * 2.0 - 1.0) * env(len(t), 0.002, 0.02) * 0.5
def tri(f, d): t = ts(d); ph = (f * t) % 1.0; return (4 * np.abs(ph - 0.5) - 1) * env(len(t), 0.003, 0.03)
def pad(f, d): t = ts(d); x = sum(np.sin(2 * np.pi * f * k * t * (1 + 0.003 * j)) / k for k in (1, 2, 3) for j in (-1, 1)); return filt(x, 'lowpass', 1600) * env(len(t), 0.25, 0.4)
def clock(): t = ts(0.06); return filt(noise(0.06), 'bandpass', [2500, 7000]) * np.exp(-t * 120) + np.sin(2 * np.pi * 3100 * t) * np.exp(-t * 90) * 0.3


def gavel(): t = ts(0.25); return (filt(noise(0.25), 'bandpass', [400, 2500]) * np.exp(-t * 60) + np.sin(2 * np.pi * 520 * t) * np.exp(-t * 35)) * 1.2
def pipes(t0, d=1.1):                                                   # Scottish pipes sting: drone + chanter run
    t = ts(d); dr = filt(sum(np.sign(np.sin(2 * np.pi * midi(m) * t)) for m in (45, 57)), 'lowpass', 1800) * env(len(t), 0.05, 0.2) * 0.25; put(fx, dr, t0, 0.22)
    for k, m in enumerate((69, 71, 73, 76, 74, 73)): put(fx, saw(midi(m), 0.17, 3200) * (1 + 0.2 * np.sin(2 * np.pi * 6 * ts(0.17))), t0 + k * 0.16, 0.12)
def ring(t0):
    for k in range(4): put(fx, beep(1300 if k % 2 == 0 else 1650, 0.07), t0 + k * 0.08, 0.13)


ROCK = [(40, (52, 59, 64)), (36, (48, 55, 60)), (38, (50, 57, 62)), (35, (47, 54, 59))]          # Em C D B
BOSSA = [(50, (65, 69, 72, 76)), (43, (65, 71, 74, 77)), (48, (64, 67, 71, 76)), (45, (61, 67, 69, 76))]  # Dm7 G7 Cmaj7 A7
ELEC = [(45, (69, 72, 76)), (41, (69, 72, 77)), (48, (67, 72, 76)), (43, (67, 71, 74))]              # Am F C G
HOUSE = [(48, (64, 67, 72)), (45, (64, 69, 72)), (41, (65, 69, 72)), (43, (62, 67, 71))]             # C Am F G
def power(f, d): t = ts(d); x = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 9)) + sum(np.sin(2 * np.pi * f * 1.5 * k * t) / k for k in range(1, 6)) * 0.8; return np.tanh(filt(x, 'lowpass', 2600) * 3.5) * env(len(t), 0.004, 0.03)
def crash(): t = ts(1.2); return filt(noise(1.2), 'highpass', 4000) * np.exp(-t * 3.5)
def rim(): t = ts(0.05); return filt(noise(0.05), 'bandpass', [1500, 5000]) * np.exp(-t * 120) + np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 80) * 0.5


def section(t0, t1, kind, bpm):
    bt = 60.0 / bpm; t = t0; prog = dict(rock=ROCK, bossa=BOSSA, elec=ELEC, house=HOUSE)[kind]
    while t < t1 - 1e-3:
        bar = int(np.floor((t - t0) / (4 * bt) + 1e-6)); b0 = t0 + bar * 4 * bt; root, ch = prog[bar % 4]
        for e in range(16):
            u = b0 + e * bt / 4
            if u < t0 - 1e-3 or u >= t1: continue
            if kind == 'rock':                                # double kick, backbeat, palm-muted 8ths, crash on the bar
                if e in (0, 2, 8, 10, 11): put(bed, kick(), u, 0.75)
                if e in (4, 12): put(bed, snare(), u, 0.5)
                if e == 0: put(bed, crash(), u, 0.12)
                if e % 2 == 0: put(bed, hat(), u, 0.07); put(bed, power(midi(root), bt * (0.9 if e in (0, 8) else 0.4)), u, 0.11)
                if e in (6, 14) and bar % 2: put(bed, chip(midi(ch[2] + 12), bt * 0.4), u, 0.05)
            elif kind == 'bossa':                             # clave rim, nylon plucks, soft bass, maj7 piano, ticking clock
                if e in (0, 3, 6, 10, 12): put(bed, rim(), u, 0.22)
                if e in (0, 8): put(bed, kick(), u, 0.35); put(bed, pluck(midi(root - 12), bt * 1.5), u, 0.32)
                if e in (2, 5, 7, 10, 13): put(bed, sum(pluck(midi(m), bt * 0.6) for m in ch[:3]), u, 0.07)
                if e == 0: put(bed, sum(piano(midi(m), 4 * bt) for m in ch), u, 0.06)
                if e % 4 == 0: put(bed, clock(), u, 0.25)
            elif kind == 'elec':                              # 16th square arp, four on the floor, tri bass
                if e % 4 == 0: put(bed, kick(), u, 0.65)
                if e in (4, 12): put(bed, clap(), u, 0.3)
                put(bed, sq(midi(ch[e % 3] + (12 if e % 8 >= 4 else 0)), bt * 0.22), u, 0.08)
                if e % 4 == 2: put(bed, tri(midi(root - 12), bt * 0.5), u, 0.32); put(bed, hat(), u, 0.06)
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.05)
            else:                                             # piano house: kick 4/4, open hats off-beat, piano stabs, offbeat bass
                if e % 4 == 0: put(bed, kick(), u, 0.8)
                if e in (4, 12): put(bed, clap(), u, 0.32)
                if e % 4 == 2: put(bed, hat(True), u, 0.07); put(bed, saw(midi(root - 12), bt * 0.4, 700), u, 0.22)
                if e in (0, 3, 6, 10, 14): put(bed, sum(piano(midi(m + 12), bt * 0.8) for m in ch), u, 0.07)
        t = b0 + 4 * bt


# ---------------------------------------------------------------- the score
section(0, C['every'], 'rock', 150)
section(C['every'], C['early'], 'bossa', 118)
section(C['early'], C['yousee'], 'elec', 112)
section(C['yousee'], C['fix'], 'rock', 160)
section(C['fix'], C['seven2'], 'house', 124)
section(C['seven2'], C['end'], 'rock', 150)

# ---------------------------------------------------------------- effects on the words
put(fx, boom(), 0.0, 0.5); put(fx, kick(), 0.0, 0.7); put(fx, crash(), 0.0, 0.3); put(fx, whoosh(0.5, 600, 4000), 0.0, 0.2); put(fx, buzzer(), 0.25, 0.12)
put(fx, whoosh(0.7, 400, 3000), C['player'] - 0.25, 0.25); put(fx, boom(), C['killed'], 0.45); put(fx, stampfx(), C['killed'] + 0.05, 0.4)
put(fx, whoosh(0.8, 300, 2600), C['every'] - 0.15, 0.22)
for k in range(6): put(fx, tick(), C['waited'] + 0.25 * k, 0.4)
put(fx, bell(midi(84), 0.9), C['six'] + 0.1, 0.14); put(fx, stampfx(), C['six'] + 0.15, 0.4)
put(fx, whoosh(1.0, 300, 2600), C['early'] - 0.1, 0.25); put(fx, bell(midi(88), 0.6), C['early'] + 0.2, 0.1)
put(fx, beep(1320, 0.08), C['toast'] + 0.3, 0.12); put(fx, boing(), C['curious'] + 0.1, 0.1)
put(fx, riser(0.6), C['digs'] - 0.5, 0.15); put(fx, whoosh(1.2, 200, 3000), C['digs'] - 0.05, 0.3)
for k in range(4): put(fx, beep(880 + 220 * k, 0.06), C['wait'] + 0.1 * k, 0.08)
put(fx, scratch(), C['yousee'] - 0.05, 0.14); put(fx, flip(), C['file'], 0.4); put(fx, stampfx(), C['file'] + 0.1, 0.35)
put(fx, stampfx(), C['mb'] + 0.05, 0.35); put(fx, whoosh(0.8, 300, 2600), C['items'] - 0.1, 0.2)
for k in range(5): put(fx, flip(), C['items'] + 0.08 * k, 0.4)
for k in range(14): put(fx, beep(1400 + 60 * (k % 4), 0.04), C['checks'] + 0.11 * k, 0.07)
put(fx, buzzer(), C['billion'] + 0.1, 0.25); put(fx, boom(), C['billion'] + 0.1, 0.4)
put(fx, scratch(), C['fix'] - 0.05, 0.12); put(fx, kaching(), C['fix'] + 0.9, 0.18)
put(fx, whoosh(0.9, 300, 2600), C['become'] - 0.1, 0.22); put(fx, riser(0.8), C['seventy'] - 0.8, 0.18); put(fx, boom(), C['seventy'], 0.35)
put(fx, cheer(1.2), C['seventy'] + 0.1, 0.12); put(fx, poof(), C['gone'], 0.3)
put(fx, whoosh(1.0, 300, 2600), C['pays'] - 0.1, 0.22); put(fx, kaching(), C['dollars'] + 0.1, 0.3); fanfare(C['dollars'] + 0.1, 76); put(fx, stampfx(), C['promises'] + 0.1, 0.35)
put(fx, whoosh(1.2, 200, 2400), C['seven2'] - 0.15, 0.28); put(fx, siren(1.2), C['boss'] + 0.1, 0.06); put(fx, stampfx(), C['cops'] + 0.1, 0.4)
put(fx, whoosh(1.0, 300, 2600), C['was'] - 0.1, 0.25); put(fx, boom(), C['loading2'], 0.45)
put(fx, riser(1.0), C['end'] - 1.1, 0.2); put(fx, crash(), C['end'] - 0.15, 0.25)

mix = bed * 1.35 + fx * 0.85
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 2.2) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, boss rock 150/160 bpm + bossa waiting 118 bpm + electro arp 112 bpm + piano house 124 bpm" % LEN)
