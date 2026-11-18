#!/usr/bin/env python3
"""Music + effects for the Cat's Eyes Short, synthesised in code (no samples).
A war-movie march (132 bpm D minor: snare roll, timpani, low brass, string ostinato) from frame 1 with an air-raid siren hit,
bombs and a bomber drone for the Blitz; an oompah music-hall tune (tuba, brass pahs, glockenspiel, woodblock) for the carrot
propaganda; a spy pulse with radar pings for the secret; a modern trap beat for today; the march returns for the loop.
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




# ---------------------------------------------------------------- video 08 instruments
def timp(f=73.4, d=0.9): t = ts(d); return (np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 6)) * np.exp(-t * 4) * env(len(t), 0.004, 0.1) + filt(noise(d), 'lowpass', 400) * np.exp(-t * 20) * 0.6
def roll(d, g=1.0):                                                     # military snare roll, crescendo
    x = np.zeros(int(SR * d) + SR // 4)
    for k in range(int(d / 0.045)):
        s = snare() * (0.35 + 0.65 * k * 0.045 / d); i = int(SR * k * 0.045); x[i:i + len(s)] += s[:len(x) - i]
    return x * g
def strings(f, d, cut=2600): t = ts(d); ph = 2 * np.pi * f * t; x = sum(np.sin(ph * h + 0.3 * h) / h for h in range(1, 10)) + sum(np.sin(ph * 1.006 * h) / h for h in range(1, 10)); return filt(x, 'lowpass', cut) * env(len(t), 0.03, 0.06) * 0.5
def tuba(f, d): t = ts(d); return filt(sum(np.sin(2 * np.pi * f * h * t) / h ** 1.2 for h in range(1, 7)), 'lowpass', 900) * env(len(t), 0.02, 0.06)
def glock(f, d=0.5): t = ts(d); return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 10)) * np.exp(-t * 6)
def wblock(): t = ts(0.06); return filt(np.sin(2 * np.pi * 900 * t) * np.exp(-t * 90) + noise(0.06) * np.exp(-t * 120) * 0.3, 'bandpass', [500, 2500])
def ping(f=1250, d=1.1): t = ts(d); return np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) * (1 + 0.3 * np.sin(2 * np.pi * 7 * t))
def sub808(f, d): t = ts(d); return np.sin(2 * np.pi * np.cumsum(f * (1 + 1.2 * np.exp(-t * 30))) / SR) * np.exp(-t * 2.2) * env(len(t), 0.002, 0.05)
def meow(): t = ts(0.55); fr = 520 + 380 * np.sin(np.pi * np.clip(t / 0.55, 0, 1)) ** 1.5; x = sum(np.sin(2 * np.pi * np.cumsum(fr * h) / SR) / h for h in (1, 2, 3)); return filt(x, 'bandpass', [400, 3500]) * env(len(t), 0.03, 0.15)
def crunch(): t = ts(0.22); return filt(noise(0.22), 'bandpass', [1500, 6500]) * (np.abs(np.sin(2 * np.pi * 34 * t)) ** 3) * np.exp(-t * 6)
def drone(d): t = ts(d); x = np.sin(2 * np.pi * 62 * t) + 0.8 * np.sin(2 * np.pi * 64.5 * t) + 0.3 * filt(noise(d), 'bandpass', [200, 900]); return x * env(len(t), 0.4, 0.4)
def raid(d=2.0): t = ts(d); return np.sin(2 * np.pi * np.cumsum(300 + 420 * np.clip(t / 0.7, 0, 1) - 120 * np.clip((t - 1.2) / 0.8, 0, 1)) / SR) * env(len(t), 0.2, 0.4)
def chuckle(t0):
    for k in range(4): put(fx, sweep(420 - 30 * k, 300, 0.12, 8) * env(int(SR * 0.12), 0.01, 0.04), t0 + k * 0.13, 0.12)


# ---------------------------------------------------------------- the four styles
MARCH = [(38, (62, 65, 69)), (34, (58, 62, 65)), (31, (55, 58, 62)), (33, (57, 61, 64))]   # Dm Bb Gm A, 132 bpm
OOM = [(41, (65, 69, 72)), (36, (64, 67, 70)), (34, (62, 65, 70)), (36, (64, 67, 72))]     # F C7 Bb C, 126 bpm
TUNE = [((0, 77), (1, 81), (2, 84), (3, 81)), ((0, 79), (1, 76), (2, 72), (3.5, 76)), ((0, 74), (1, 77), (2, 82), (3, 81)), ((0, 79), (1.5, 84), (2, 84))]
SPY = [(45, (57, 60, 64)), (41, (57, 60, 65)), (43, (55, 59, 62)), (40, (56, 59, 64))]      # Am F G E, 128 bpm
TRAP = [(45, (69, 72, 76)), (41, (69, 72, 77)), (48, (67, 72, 76)), (43, (67, 71, 74))]     # Am F C G, 140 bpm half-time


def section(t0, t1, kind, bpm, full=True):
    bt = 60.0 / bpm; t = t0
    prog = dict(march=MARCH, oom=OOM, spy=SPY, trap=TRAP)[kind]
    while t < t1 - 1e-3:
        bar = int(np.floor((t - t0) / (4 * bt) + 1e-6)); b0 = t0 + bar * 4 * bt; root, ch = prog[bar % 4]
        for e in range(8):                                            # eighth notes
            u = b0 + e * bt / 2; beat = e // 2; on = e % 2 == 0
            if u < t0 - 1e-3 or u >= t1: continue
            if kind == 'march':
                if on and beat in (0, 2): put(bed, kick(), u, 0.8)
                if on and beat in (1, 3): put(bed, snare(), u, 0.42)
                put(bed, filt(snare(), 'highpass', 2000), u + bt / 4, 0.09); put(bed, hat(), u, 0.07)
                if e == 0: put(bed, timp(midi(root + 12)), u, 0.5); put(bed, sum(brass(midi(m - 12), 4 * bt * 0.95, 2200) for m in ch), u, 0.05 if full else 0.03)
                put(bed, strings(midi(ch[(e + bar) % 3] + 12), bt * 0.42, 3200), u, 0.07)
                if on: put(bed, tuba(midi(root), bt * 0.8), u, 0.3)
            elif kind == 'oom':
                if on and beat in (0, 2): put(bed, tuba(midi(root - (0 if beat == 0 else 5)), bt * 0.7), u, 0.55); put(bed, kick(), u, 0.55)
                if on and beat in (1, 3): put(bed, sum(brass(midi(m), bt * 0.35, 3000) for m in ch), u, 0.06); put(bed, clap(), u, 0.25)
                if not on: put(bed, wblock(), u, 0.16)
                put(bed, hat(), u, 0.06)
            elif kind == 'spy':
                put(bed, saw(midi(root - 12), bt * 0.42, 700), u, 0.32 if full else 0.22)
                if on and beat in (0, 2) and full: put(bed, kick(), u, 0.7)
                if on and beat == 3: put(bed, filt(snare(), 'bandpass', [1500, 5000]), u, 0.25)
                put(bed, hat(), u, 0.05); put(bed, hat(), u + bt / 4, 0.035)
                if e == 0: put(bed, sum(strings(midi(m), 4 * bt, 1800) for m in ch), u, 0.03); put(bed, ping(midi(88)), u, 0.05)
            else:                                                     # trap
                if e in (0, 5): put(bed, kick(), u, 0.85); put(bed, sub808(midi(root - 12), bt * 1.6), u, 0.5)
                if e == 4: put(bed, clap(), u, 0.55); put(bed, snare(), u, 0.3)
                put(bed, hat(), u, 0.1)
                if e == 7:
                    for r in range(3): put(bed, hat(), u + r * bt / 6, 0.08)
                put(bed, pluck(midi(ch[(e * 2 + bar) % 3]), bt * 0.4), u, 0.12)
        if kind == 'oom':
            for b, m in TUNE[bar % 4]:
                if t0 <= b0 + b * bt < t1: put(bed, glock(midi(m)), b0 + b * bt, 0.16 if full else 0.1)
        if kind == 'march' and bar % 2 == 1 and full:
            for k, m in enumerate((74, 77, 76, 73)):
                if t0 <= b0 + k * bt < t1: put(bed, brass(midi(m), bt * 0.9, 2600), b0 + k * bt, 0.05)
        t = b0 + 4 * bt


def stab(t, g=1.0): put(fx, sum(brass(midi(m), 0.35) for m in (62, 65, 69, 74)), t, 0.1 * g); put(fx, timp(), t, 0.5 * g); put(fx, kick(), t, 0.6 * g)
def fanfare(t, base=72):
    for k, (m, d) in enumerate(((0, .14), (4, .14), (7, .14), (12, .6))): put(fx, sum(brass(midi(base + m + x), d) for x in (0, -5, -12)), t + k * 0.13, 0.085)


# ---------------------------------------------------------------- the score
section(0, C['papers'], 'march', 132)
section(C['papers'], C['yousee'], 'oom', 126)
section(C['yousee'], C['story'], 'spy', 128)
section(C['story'], C['but'], 'oom', 126)
section(C['but'], C['only'], 'spy', 128, full=False)
section(C['only'], C['loop'], 'trap', 140)
section(C['loop'], C['end'], 'march', 132)

# ---------------------------------------------------------------- effects on the beats
put(fx, raid(2.2), 0.0, 0.07); stab(0.0, 1.3); put(fx, roll(0.5, 0.5), 0.0); put(fx, stampfx(), C['couldnt'], 0.5); put(fx, boing(), C['couldnt'] + 0.15, 0.1)
for k in range(3): put(fx, ping(1250 + 250 * k, 0.5), C['machine'] + 0.12 * k, 0.12)
put(fx, boing(), C['carrot'], 0.18); fanfare(C['credit'] - 0.05); put(fx, cheer(1.0), C['credit'], 0.1)
stab(C['y1940'], 1.1); put(fx, raid(1.8), C['y1940'], 0.08); put(fx, boom(), C['blitz'], 0.7); put(fx, boom(), C['blitz'] + 0.25, 0.5)
put(fx, drone(C['john'] - C['bombers']), C['bombers'], 0.12); put(fx, boom(), C['night'], 0.6); put(fx, boom(), C['night'] + 0.3, 0.4)
put(fx, whoosh(1.0, 300, 3000), C['pilot'], 0.3); put(fx, engine(1.2, 90, 0.5), C['pilot'] + 0.1, 0.1); stab(C['anyway'], 0.9); put(fx, stampfx(), C['anyway'], 0.4)
fanfare(C['john'], 74); put(fx, cheer(0.9), C['john'], 0.08)
for k in range(10): put(fx, tick(), C['kills'] + 0.06 * k, 0.5)
put(fx, stampfx(), C['kills'], 0.45); put(fx, stampfx(), C['nineteen'], 0.45); put(fx, bell(midi(86), 0.8), C['nineteen'], 0.08)
put(fx, scratch(), C['papers'] - 0.05, 0.1); put(fx, flip(), C['papers'] + 0.1, 0.4); put(fx, meow(), C['cats'] + 0.1, 0.3); put(fx, stampfx(), C['cats'], 0.35)
put(fx, filt(noise(0.4), 'highpass', 3000) * env(int(SR * 0.4), 0.1, 0.2), C['secret'], 0.1); put(fx, crunch(), C['carrots'], 0.5); put(fx, stampfx(), C['carrots'], 0.45)
for k in range(6): put(fx, boing(), C['lots'] + 0.11 * k, 0.07); put(fx, crunch(), C['lots'] + 0.13 * k, 0.2)
put(fx, scratch(), C['yousee'] - 0.05, 0.1); put(fx, ping(1500), C['radar'], 0.3); put(fx, ping(1500), C['radar'] + 0.4, 0.15); stab(C['radar'], 0.7)
put(fx, whoosh(0.9, 400, 2500), C['hidden'] - 0.1, 0.25); put(fx, bell(midi(88), 0.9), C['hidden'] + 0.1, 0.08)
put(fx, filt(noise(0.6), 'highpass', 3500) * env(int(SR * 0.6), 0.05, 0.3), C['britain'] + 0.1, 0.12); put(fx, stampfx(), C['enemy'], 0.55); put(fx, boom(), C['enemy'], 0.3)
stab(C['story'], 1.0); put(fx, stampfx(), C['everywhere'], 0.5); put(fx, flip(), C['posters'], 0.5); put(fx, flip(), C['posters'] + 0.08, 0.4)
fanfare(C['doctor'] - 0.05, 77); put(fx, kaching(), C['fudge'], 0.3)
for k in range(5): put(fx, glock(midi(84 + (0, 4, 7, 12, 16)[k]), 0.3), C['fudge'] + 0.07 * k, 0.1)
stab(C['y1942'], 1.0); put(fx, boom(), C['tons'], 0.6); put(fx, cheer(1.0), C['tons'], 0.08)
put(fx, scratch(), C['but'] - 0.05, 0.14); put(fx, buzzer(), C['vision'], 0.45); put(fx, stampfx(), C['vision'], 0.5)
put(fx, flip(), C['hist'], 0.4); put(fx, flip(), C['hist'] + 0.1, 0.3); put(fx, stampfx(), C['never'], 0.5); chuckle(C['never'] + 0.2)
stab(C['only'], 0.9); put(fx, stampfx(), C['us'], 0.55); put(fx, whoosh(1.0, 300, 2500), C['eighty'] - 0.1, 0.25); put(fx, crunch(), C['eighty'] + 0.3, 0.4)
put(fx, stampfx(), C['believe'], 0.5); put(fx, riser(1.2), C['loop'] - 1.0, 0.22); stab(C['loop'], 1.2); put(fx, raid(2.0), C['loop'], 0.06)
put(fx, stampfx(), C['dark'], 0.4)

mix = bed * 0.9 + fx
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 1.6) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, war march 132 bpm D minor + oompah F major + spy pulse + trap" % LEN)
