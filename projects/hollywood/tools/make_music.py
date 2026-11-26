#!/usr/bin/env python3
"""Music + effects for video 16 (Clyde Tombaugh and Pluto), synthesised in code: an epic timpani-and-brass hook and loop,
a country banjo-and-harmonica shuffle for the Kansas farm, a music-box mystery for Lowell and the blink plates, a piano lament,
a soft space drift for the flyby.
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


XPROG = dict(bayou=[(40, (64, 67, 71)), (45, (64, 69, 72)), (40, (64, 67, 71)), (47, (66, 69, 75))],      # Em Am Em B7
             polka=[(41, (65, 69, 72)), (48, (64, 67, 70)), (41, (65, 69, 72)), (48, (64, 67, 72))],      # F C7 F C
             lullaby=[(43, (67, 71, 74)), (40, (67, 71, 76)), (36, (67, 72, 76)), (38, (66, 69, 74))])   # G Em C D
XPROG = dict(bluegrass=[(43, (67, 71, 74)), (48, (64, 67, 72)), (43, (67, 71, 74)), (50, (66, 69, 74))],    # G C G D
             thunder=[(38, (62, 65, 69)), (46, (62, 65, 70)), (48, (64, 67, 72)), (38, (62, 65, 69))],      # Dm Bb C Dm
             lakefolk=[(38, (66, 69, 74)), (43, (67, 71, 74)), (47, (66, 71, 74)), (45, (64, 69, 73))])     # D G Bm A
XPROG = dict(musichall=[(48, (64, 67, 72)), (45, (64, 67, 73)), (38, (65, 69, 74)), (43, (65, 71, 74))],   # C A7 Dm G7
             jig=[(38, (66, 69, 74)), (43, (67, 71, 74)), (38, (66, 69, 74)), (45, (64, 69, 73))],         # D G D A
             swampdrone=[(45, (64, 69, 72)), (45, (64, 69, 72)), (41, (65, 69, 72)), (40, (64, 68, 71))],  # Am Am F E
             steam=[(43, (67, 71, 74)), (40, (64, 67, 71)), (48, (64, 67, 72)), (38, (66, 69, 74))])       # G Em C D
XPROG = dict(charleston=[(36, (64, 67, 72)), (45, (64, 67, 73)), (38, (65, 69, 74)), (43, (65, 71, 74))],    # C A7 Dm G7
             nightjazz=[(38, (65, 69, 72)), (43, (65, 71, 74)), (36, (64, 67, 71)), (45, (64, 67, 72))],    # Dm7 G7 Cmaj7 Am7
             dustwaltz=[(45, (64, 69, 72)), (40, (64, 68, 71)), (45, (64, 69, 72)), (38, (65, 69, 74))],    # Am E Am Dm
             bigband=[(41, (65, 69, 72)), (38, (65, 69, 74)), (36, (64, 67, 72)), (43, (67, 71, 74))])      # F Dm C G
CAJ = [(43, (67, 71, 74)), (48, (67, 72, 76)), (50, (66, 69, 74)), (43, (67, 71, 74))]          # G C D G
STORM = [(38, (62, 65, 69)), (34, (62, 65, 70)), (36, (60, 64, 67)), (33, (61, 64, 69))]        # Dm Bb C A
MINE = [(45, (69, 72, 76)), (41, (69, 72, 77)), (38, (65, 69, 74)), (40, (68, 71, 76))]         # Am F Dm E
def crash(): t = ts(1.2); return filt(noise(1.2), 'highpass', 4000) * np.exp(-t * 3.5)
def rim(): t = ts(0.05); return filt(noise(0.05), 'bandpass', [1500, 5000]) * np.exp(-t * 120) + np.sin(2 * np.pi * 1700 * t) * np.exp(-t * 80) * 0.5
def tom(f=90): t = ts(0.4); return sweep(f * 1.6, f, 0.4, 18) * np.exp(-t * 7)
def accordion(f, d): t = ts(d); x = sum(np.sign(np.sin(2 * np.pi * f * h * t * (1 + 0.004 * j))) / h for h in (1, 2) for j in (-1, 1)); return filt(x, 'lowpass', 2600) * env(len(t), 0.02, 0.05) * 0.4
def gurgle(d): t = ts(d); return filt(noise(d), 'bandpass', [150, 900]) * (0.6 + 0.4 * np.sin(2 * np.pi * 3 * t)) * env(len(t), 0.1, 0.3)
def splash(): t = ts(0.6); return filt(noise(0.6), 'lowpass', 2500) * np.exp(-t * 6)
def groan(d=1.2): t = ts(d); return filt(np.sign(np.sin(2 * np.pi * np.cumsum(70 - 25 * t / d + 4 * np.sin(2 * np.pi * 5 * t)) / SR)), 'lowpass', 600) * env(len(t), 0.05, 0.3)
def gullcry(): t = ts(0.35); return np.sin(2 * np.pi * np.cumsum(2300 - 1500 * t) / SR) * env(len(t), 0.01, 0.1)


def static(d): t = ts(d); return filt(noise(d), 'bandpass', [1500, 6000]) * (0.5 + 0.5 * (R.rand(len(t)) > 0.97)) * env(len(t), 0.01, 0.1)
SPACE = [(45, (69, 72, 76)), (41, (69, 72, 77)), (43, (67, 71, 74)), (40, (68, 71, 76))]       # Am F G E
MARCH = [(48, (67, 72, 76)), (53, (69, 72, 77)), (55, (67, 71, 74)), (48, (67, 72, 76))]       # C F G C
TENSE = [(38, (62, 65, 69)), (38, (62, 65, 70)), (36, (60, 64, 67)), (37, (61, 64, 69))]       # Dm Dm(b6) C A
FUNK = [(40, (64, 67, 71)), (40, (64, 67, 71)), (45, (64, 69, 72)), (43, (62, 67, 71))]        # Em Em Am G


RAG = [(48, (64, 67, 72)), (45, (64, 69, 72)), (50, (65, 69, 74)), (43, (65, 67, 71))]          # C Am Dm G7
TANGO = [(45, (64, 69, 72)), (45, (64, 69, 72)), (40, (64, 68, 71)), (45, (64, 69, 72))]      # Am Am E Am
SAD = [(45, (69, 72, 76)), (41, (69, 72, 77)), (48, (67, 72, 76)), (40, (68, 71, 76))]        # Am F C E
TRAP = [(37, (61, 64, 68)), (42, (61, 66, 69)), (44, (63, 68, 71)), (40, (64, 68, 71))]       # C#m F#m G# E
def section(t0, t1, kind, bpm):
    bt = 60.0 / bpm; t = t0; prog = dict(space=SPACE, march=MARCH, tick=TENSE, crash=TENSE, lonely=SPACE, funk=FUNK, rag=RAG, tango=TANGO, show=MARCH, lament=SAD, trap=TRAP, country=CAJ, musicbox=MINE, epic=MARCH, drift=SPACE, **XPROG)[kind]
    while t < t1 - 1e-3:
        bar = int(np.floor((t - t0) / (4 * bt) + 1e-6)); b0 = t0 + bar * 4 * bt; root, ch = prog[bar % 4]
        for e in range(16):
            u = b0 + e * bt / 4
            if u < t0 - 1e-3 or u >= t1: continue
            if kind == 'space':                               # 90s space synth: square arpeggio, 808 bass, four-on-the-floor, pad
                put(bed, sq(midi(ch[e % 3] + (12 if (e // 4) % 2 else 0)), bt * 0.22), u, 0.07)
                if e % 4 == 0: put(bed, kick(), u, 0.6)
                if e in (4, 12): put(bed, clap(), u, 0.3)
                if e % 4 == 2: put(bed, hat(), u, 0.08)
                if e in (0, 6, 10): put(bed, b808(midi(root - 12), bt * 1.2), u, 0.3)
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.06)
            elif kind == 'march':                             # light adventure march: snare drive, tuba, brass stabs, glockenspiel
                if e in (0, 8): put(bed, kick(), u, 0.65); put(bed, tri(midi(root - 12), bt * 0.8), u, 0.35)
                if e in (4, 12): put(bed, tri(midi(root - 5), bt * 0.8), u, 0.3)
                if e % 2 == 0: put(bed, snare(), u, 0.12 if e % 4 else 0.3)
                if e in (0, 6) and bar % 2 == 0: put(bed, sum(brass(midi(m), bt * 0.5) for m in ch), u, 0.05)
                if e % 4 == 0: put(bed, bell(midi(ch[(e // 4 + bar) % 3] + 12), 0.5), u, 0.05)
            elif kind == 'tick':                              # tension: clock ticks, low pulse, pizzicato, pad
                if e % 4 == 0: put(bed, clock(), u, 0.35)
                if e % 4 == 2: put(bed, tick(), u, 0.2)
                if e in (0, 8): put(bed, tri(midi(root - 12), bt * 1.6), u, 0.35); put(bed, kick(), u, 0.4)
                if e % 2 == 0: put(bed, pluck(midi(ch[(e // 2) % 3]), bt * 0.4), u, 0.08)
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.05)
            elif kind == 'crash':                             # crash: taiko toms, distorted 808, saw 8ths, crash on the bar
                if e in (0, 3, 6, 8, 11, 14): put(bed, tom(70 if e % 8 == 0 else 95), u, 0.6)
                if e in (0, 8): put(bed, kick(), u, 0.75); put(bed, b808(midi(root - 12), bt * 1.5), u, 0.35)
                if e in (4, 12): put(bed, snare(), u, 0.45)
                if e % 2 == 0: put(bed, saw(midi(root + (12 if e % 4 else 0)), bt * 0.45, 1600), u, 0.12)
                if e == 0: put(bed, crash(), u, 0.1)
            elif kind == 'lonely':                            # lonely: pad, radio pings, soft piano
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.08)
                if e in (0, 10): put(bed, beep(1320, 0.1), u, 0.06)
                if e in (0, 6, 12): put(bed, piano(midi(ch[(e // 6) % 3] + 12), bt * 2), u, 0.12)
                if e in (0, 8): put(bed, tri(midi(root - 12), bt * 2), u, 0.25)
            elif kind == 'rag':                               # ragtime stride: oom-pah bass, off-beat chords, syncopated top line, brushes
                if e in (0, 8): put(bed, piano(midi(root - 12), bt * 1.5), u, 0.34); put(bed, kick(), u, 0.45)
                if e in (4, 12): put(bed, sum(piano(midi(m), bt) for m in ch), u, 0.1); put(bed, snare(), u, 0.16)
                if e in (0, 3, 6, 10, 12, 14): put(bed, piano(midi(ch[(e // 3 + bar) % 3] + 12), bt * 0.5), u, 0.15)
                if e % 2 == 0: put(bed, hat(), u, 0.05)
            elif kind == 'tango':                             # sneaky tango: habanera bass, staccato accordion, pizzicato, rim
                if e in (0, 6, 8, 12): put(bed, tri(midi(root - 12 + (7 if e == 12 else 0)), bt * 0.6), u, 0.4)
                if e in (0, 6, 8): put(bed, kick(), u, 0.45)
                if e in (4, 12): put(bed, sum(accordion(midi(m), bt * 0.3) for m in ch), u, 0.14)
                if e in (2, 10, 14): put(bed, pluck(midi(ch[e % 3] + 12), bt * 0.4), u, 0.1)
                if e == 12: put(bed, rim(), u, 0.25)
            elif kind == 'show':                              # game-show swing: walking bass, claps, brass stabs, bells
                if e % 4 == 0: put(bed, tri(midi(root - 12 + (0, 4, 7, 4)[e // 4]), bt * 0.9), u, 0.35); put(bed, kick(), u, 0.5 if e in (0, 8) else 0.25)
                if e in (4, 12): put(bed, clap(), u, 0.35)
                if e % 2 == 0: put(bed, hat(e % 4 == 2), u, 0.07)
                if e in (0, 6): put(bed, sum(brass(midi(m), bt * 0.35) for m in ch), u, 0.06)
                if e % 4 == 2: put(bed, bell(midi(ch[(e // 4) % 3] + 12), 0.4), u, 0.05)
            elif kind == 'lament':                            # lament: pad, slow piano, low tri
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.07)
                if e in (0, 4, 8, 12): put(bed, piano(midi(ch[(e // 4) % 3] + 12), bt * 2), u, 0.13)
                if e in (0, 8): put(bed, tri(midi(root - 12), bt * 2), u, 0.28)
                if e in (6, 14): put(bed, piano(midi(ch[2] + 24), bt), u, 0.06)
            elif kind == 'trap':                              # game night: 808, clap on 3, hat rolls, plucks
                if e in (0, 10): put(bed, b808(midi(root - 12), bt * 1.4), u, 0.4); put(bed, kick(), u, 0.55)
                if e == 8: put(bed, clap(), u, 0.45)
                put(bed, hat(), u, 0.06 if e % 2 else 0.09)
                if e in (14, 15): put(bed, hat(), u + bt / 8, 0.05)
                if e in (0, 3, 6, 9, 12): put(bed, pluck(midi(ch[e % 3] + 12), bt * 0.5), u, 0.1)
            elif kind == 'country':                           # farm shuffle: banjo rolls, harmonica, boom-chick bass, brushes
                if e in (0, 8): put(bed, kick(), u, 0.45); put(bed, tri(midi(root - 12), bt * 0.8), u, 0.35)
                if e in (4, 12): put(bed, tri(midi(root - 5), bt * 0.8), u, 0.3); put(bed, snare(), u, 0.14)
                if e % 2 == 0: put(bed, hat(), u, 0.05)
                if e in (0, 3, 6, 8, 11, 14): put(bed, banjo(midi(ch[(e + bar) % 3] + 12)), u, 0.12)
                if e in (0, 8) and bar % 2 == 0: put(bed, whis(midi(ch[(e // 8 + bar) % 3] + 12), bt * 1.6) * 0.6 + fiddle(midi(ch[(e // 8 + bar) % 3] + 12), bt * 1.6) * 0.5, u, 0.06)
            elif kind == 'musicbox':                          # mystery: music-box arpeggio, low pulse, ticking, pad
                if e % 2 == 0: put(bed, bell(midi(ch[(e // 2) % 3] + 24), 0.5), u, 0.06)
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.06)
                if e in (0, 8): put(bed, tri(midi(root - 12), bt * 1.6), u, 0.32); put(bed, kick(), u, 0.3)
                if e % 4 == 2: put(bed, tick(), u, 0.12)
            elif kind == 'epic':                              # epic: timpani, brass chords, string pad, snare build
                if e in (0, 8): put(bed, tom(65), u, 0.6); put(bed, kick(), u, 0.55)
                if e in (6, 14): put(bed, tom(90), u, 0.35)
                if e in (0, 8): put(bed, sum(brass(midi(m), bt * 1.4) for m in ch), u, 0.06)
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.08); put(bed, saw(midi(root), 4 * bt, 900), u, 0.05)
                if e >= 12: put(bed, snare(), u, 0.08 + 0.03 * (e - 12))
                if e in (4, 12): put(bed, clap(), u, 0.2)
            elif kind == 'drift':                             # space drift: pad, plucked arpeggio, soft kick, 808
                if e == 0: put(bed, sum(pad(midi(m), 4 * bt) for m in ch), u, 0.08)
                if e % 3 == 0: put(bed, pluck(midi(ch[(e // 3) % 3] + 12), bt * 0.6), u, 0.1)
                if e in (0, 8): put(bed, kick(), u, 0.35); put(bed, b808(midi(root - 12), bt * 1.2), u, 0.25)
                if e % 4 == 2: put(bed, hat(), u, 0.05)
            elif kind == 'bayou':                             # swamp-blues shuffle: stomp kick, slide twang riff, washboard hats, harmonica-ish whistle
                if e in (0, 6, 8, 14): put(bed, kick(), u, 0.45)
                if e in (4, 12): put(bed, snare(), u, 0.16); put(bed, clap(), u, 0.15)
                if e % 2 == 1: put(bed, hat(), u, 0.05)
                if e in (0, 3, 8, 11): put(bed, twang(midi(root + (0, 3, 5, 7)[(e // 3 + bar) % 4]), bt * 0.8), u, 0.14)
                if e == 10 and bar % 2: put(bed, whis(midi(ch[2] + 12), bt * 1.2), u, 0.04)
            elif kind == 'polka':                             # toy-shop polka: oom-pah, clarinet-ish whistle tune, glock, snare off-beats
                if e in (0, 8): put(bed, tri(midi(root - 12), bt * 0.5), u, 0.4); put(bed, kick(), u, 0.35)
                if e in (4, 12): put(bed, sum(accordion(midi(m), bt * 0.25) for m in ch), u, 0.05); put(bed, snare(), u, 0.12)
                if e % 2 == 0: put(bed, whis(midi(ch[(e // 2 + bar) % 3] + 12), bt * 0.4), u, 0.035)
                if e in (2, 10): put(bed, bell(midi(ch[(e + bar) % 3] + 24), 0.3), u, 0.04)
            elif kind == 'lullaby':                           # music-box lullaby over a soft heartbeat kick and pad
                if e % 4 == 0: put(bed, bell(midi(ch[(e // 4 + bar) % 3] + 24), 0.6), u, 0.06)
                if e in (2, 6, 10, 14): put(bed, bell(midi(ch[(e // 4) % 3] + 19), 0.4), u, 0.035)
                if e in (0, 8): put(bed, kick(), u, 0.3); put(bed, pluck(midi(root - 12), bt * 1.5), u, 0.2)
                if e == 0: put(bed, pad(midi(ch[0]), bt * 4), u, 0.06)
                if e in (4, 12): put(bed, rim(), u, 0.12)
            elif kind == 'bluegrass':                         # Appalachian bluegrass: banjo-ish forward rolls, boom-chick bass, brush snare, fiddle twang
                put(bed, pluck(midi(ch[e % 3] + 12 + (12 if e % 4 == 3 else 0)), bt * 0.25), u, 0.042)
                if e in (0, 8): put(bed, pluck(midi(root - 12), bt * 0.6), u, 0.3); put(bed, kick(), u, 0.28)
                if e in (4, 12): put(bed, pluck(midi(root - 5), bt * 0.6), u, 0.24); put(bed, snare(), u, 0.09)
                if e in (0, 6, 10) and bar % 2 == 0: put(bed, twang(midi(ch[1] + 12), bt * 0.8), u, 0.06)
            elif kind == 'thunder':                           # storm drums: tom booms, rim ticks, low drone pad, a far bell
                if e in (0, 3, 8, 11): put(bed, kick(), u, 0.42)
                if e == 12: put(bed, snare(), u, 0.14)
                if e % 2 == 1: put(bed, rim(), u, 0.06)
                if e == 0: put(bed, pad(midi(root - 12), bt * 4), u, 0.08)
                if e == 6 and bar % 2: put(bed, bell(midi(ch[2] + 24), 0.5), u, 0.04)
            elif kind == 'lakefolk':                          # gentle lake folk: fingerpicked chord tones, soft bass, bell answers
                if e % 2 == 0: put(bed, pluck(midi(ch[(e // 2) % 3] + 12), bt * 0.5), u, 0.06)
                if e in (0, 8): put(bed, pluck(midi(root - 12), bt * 1.2), u, 0.25)
                if e in (4, 12): put(bed, bell(midi(ch[2] + 24), 0.4), u, 0.035)
                if e == 0: put(bed, kick(), u, 0.22)
                if e % 4 == 2: put(bed, hat(), u, 0.03)
            elif kind == 'musichall':                         # Victorian music-hall stride: bass-chord vamp, glockenspiel tune, brushed snare
                if e in (0, 8): put(bed, pluck(midi(root - 12), bt * 0.8), u, 0.3); put(bed, kick(), u, 0.3)
                if e in (4, 12): [put(bed, pluck(midi(n_), bt * 0.4), u, 0.04) for n_ in ch]; put(bed, snare(), u, 0.07)
                if e in (2, 6, 10, 14): put(bed, bell(midi(ch[(e // 2 + bar) % 3] + 24), 0.3), u, 0.035)
                if e % 2 == 1: put(bed, hat(), u, 0.03)
            elif kind == 'jig':                               # crew jig: rolling triplet-feel plucks, stomping bass, fiddle twang
                if e % 3 == 0: put(bed, pluck(midi(ch[(e // 3) % 3] + 12), bt * 0.3), u, 0.06)
                if e in (0, 6, 12): put(bed, kick(), u, 0.36); put(bed, pluck(midi(root - 12), bt * 0.6), u, 0.26)
                if e in (3, 9, 15): put(bed, clap(), u, 0.06)
                if e in (0, 8) and bar % 2 == 0: put(bed, twang(midi(ch[2] + 12), bt * 0.8), u, 0.06)
            elif kind == 'swampdrone':                        # swamp drone: low pads, croaky rims, slow heartbeat kick
                if e == 0: put(bed, pad(midi(root - 12), bt * 4), u, 0.09); put(bed, pad(midi(ch[1]), bt * 4), u, 0.04)
                if e in (0, 10): put(bed, kick(), u, 0.36)
                if e in (3, 7, 13): put(bed, rim(), u, 0.08)
                if e == 8: put(bed, snare(), u, 0.1)
                if e == 6 and bar % 2: put(bed, bell(midi(ch[2] + 24), 0.6), u, 0.035)
            elif kind == 'steam':                             # steam-train shuffle: chugging 16th hats, kick-snare, whistle bell
                put(bed, hat(), u, 0.05 if e % 4 == 0 else 0.025)
                if e in (0, 8): put(bed, kick(), u, 0.4); put(bed, pluck(midi(root - 12), bt * 0.8), u, 0.26)
                if e in (4, 12): put(bed, snare(), u, 0.12)
                if e in (2, 6, 10, 14): put(bed, pluck(midi(ch[(e // 4) % 3] + 12), bt * 0.3), u, 0.05)
                if e == 0 and bar % 4 == 0: put(bed, bell(midi(ch[2] + 24), 0.9), u, 0.05); put(bed, bell(midi(ch[0] + 24), 0.9), u, 0.04)
            elif kind == 'charleston':                        # 1920s charleston: dotted bass hits, banjo-like plucks, clap on 4, bell riff
                if e in (0, 6): put(bed, kick(), u, 0.42); put(bed, pluck(midi(root - 12), bt * 0.5), u, 0.28)
                if e in (2, 6, 10, 14): [put(bed, pluck(midi(n_ + 12), bt * 0.18), u, 0.035) for n_ in ch]
                if e == 12: put(bed, clap(), u, 0.16); put(bed, snare(), u, 0.08)
                if e in (0, 3, 8, 11) and bar % 2 == 1: put(bed, bell(midi(ch[(e + bar) % 3] + 24), 0.22), u, 0.04)
            elif kind == 'nightjazz':                         # moonlit cool jazz: brushed hats, walking bass, soft chord pads, bells
                if e % 4 == 0: put(bed, pluck(midi(root - 12 + [0, 3, 5, 7][e // 4]), bt * 0.9), u, 0.26)
                if e % 2 == 0: put(bed, hat(), u, 0.02)
                if e == 0: put(bed, pad(midi(ch[0]), bt * 4), u, 0.06)
                if e in (6, 14): put(bed, bell(midi(ch[2] + 12), 0.5), u, 0.04)
            elif kind == 'dustwaltz':                         # dusty music-box waltz (3/4 feel over 16ths): bass, two chord ticks, wind bell
                if e in (0, 6, 12) and e == 0: put(bed, pluck(midi(root - 12), bt), u, 0.26); put(bed, kick(), u, 0.22)
                if e in (5, 10): [put(bed, pluck(midi(n_), bt * 0.2), u, 0.03) for n_ in ch]
                if e in (0, 5, 10): put(bed, bell(midi(ch[(e // 5 + bar) % 3] + 24), 0.6), u, 0.035)
            elif kind == 'bigband':                           # 1949 big-band swing: kick 1/3, snare backbeat, brass-like chord stabs, ride hats
                if e in (0, 8): put(bed, kick(), u, 0.42)
                if e in (4, 12): put(bed, snare(), u, 0.12)
                if e % 2 == 0: put(bed, hat(), u, 0.03)
                if e in (3, 7, 14): [put(bed, pluck(midi(n_ + 12), bt * 0.35), u, 0.05) for n_ in ch]
                if e == 0: put(bed, pluck(midi(root - 12), bt * 1.5), u, 0.3)
            else:                                             # funk reveal: slap bass, clav chords, 16th hats, kick/snare
                if e in (0, 7, 8): put(bed, kick(), u, 0.65)
                if e in (4, 12): put(bed, snare(), u, 0.4)
                put(bed, hat(), u, 0.05 if e % 2 else 0.08)
                if e in (0, 3, 6, 10, 11, 14): put(bed, slap(midi(root - 12 + (12 if e in (3, 11) else 0)), bt * 0.4), u, 0.3)
                if e in (2, 6, 7, 14): put(bed, sum(clav(midi(m), bt * 0.3) for m in ch), u, 0.05)
        t = b0 + 4 * bt


# ---------------------------------------------------------------- the score
section(0, C['la1923'], 'charleston', 126)
section(C['la1923'], C['yousee'], 'nightjazz', 112)
section(C['yousee'], C['then49'], 'dustwaltz', 96)
section(C['then49'], C['end'], 'bigband', 132)

# ---------------------------------------------------------------- effects: a light whoosh on every scene change, hits on the words
for k in sorted(x for x in C if x.startswith('s') and x[1:].isdigit()): put(fx, whoosh(0.45, 500, 3200), C[k] - 0.18, 0.13); put(fx, stampfx(), C[k] + 0.12, 0.16)
put(fx, boom(), 0.0, 0.4); put(fx, crash(), 0.0, 0.25); put(fx, stampfx(), 0.02, 0.3); put(fx, boing(), C['movies'], 0.16); put(fx, kaching(), C['billboard'], 0.16); put(fx, whoosh(0.8, 200, 900), C['down'], 0.16)
put(fx, flip(), C['y1923'], 0.24); put(fx, bell(midi(84), 0.5), C['group'], 0.12); put(fx, bell(midi(88), 0.6), C['publisher'], 0.12); put(fx, flip(), C['times'], 0.22); put(fx, kaching(), C['lots'], 0.16)
put(fx, bell(midi(91), 0.8), C['hland'], 0.14); put(fx, riser(0.7), C['write'], 0.14); put(fx, stampfx(), C['thirteen'], 0.22); put(fx, riser(0.6), C['fortyfive'] - 0.3, 0.14); put(fx, bell(midi(96), 0.6), C['bulbs'], 0.14)
put(fx, kaching(), C['dollars'] + 0.5, 0.18); put(fx, boing(), C['life'], 0.14); put(fx, groan(0.7), C['nobody'], 0.08); put(fx, crash(), C['apart'] + 0.3, 0.16); put(fx, flip(), C['y1949'], 0.24)
put(fx, gavel(), C['deal'] + 0.3, 0.26); put(fx, stampfx(), C['condition'], 0.22); put(fx, crash(), C['cut'], 0.2)
for dt_ in (0.0, 0.14, 0.3, 0.4): put(fx, boing(), C['l_'] + dt_, 0.14)
fanfare(C['famous']); put(fx, kaching(), C['realestate'], 0.16); put(fx, crash(), C['chopped'], 0.2); put(fx, riser(1.0), C['end'] - 1.1, 0.2); put(fx, crash(), C['end'] - 0.15, 0.25)

mix = bed * 1.35 + fx * 0.85
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 2.2) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, 1920s charleston 126 + moonlit cool jazz 112 + dusty music-box waltz 96 + 1949 big-band swing 132" % LEN)
