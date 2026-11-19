#!/usr/bin/env python3
"""Music + effects for the GTA 6 launch Short, synthesised in code (no samples).
A trap launch-hype beat (140 bpm F minor: 808 slides, hat rolls, saw arp) from frame 1; an 8-bit chiptune run (150 bpm)
for the delays, the pre-orders and the empty box; a ticking clock pulse with bells for the midnight wave; the trap beat
returns for the loop.
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


TRAP = [(41, (65, 68, 72)), (37, (61, 65, 68)), (44, (63, 68, 72)), (39, (63, 67, 70))]          # Fm Db Ab Eb, 140 bpm
CHIP = [(53, (65, 69, 72)), (50, (62, 65, 69)), (46, (62, 65, 70)), (48, (64, 67, 72))]          # F Dm Bb C, 150 bpm
CMEL = [(0, 77), (0.5, 81), (1, 84), (1.5, 81), (2, 79), (3, 77)], [(0, 74), (0.5, 77), (1, 81), (2, 79), (3, 74)], [(0, 74), (0.5, 77), (1, 82), (1.5, 81), (2, 77), (3, 74)], [(0, 76), (0.5, 79), (1, 84), (2, 82), (2.5, 81), (3, 79)]


def section(t0, t1, kind, bpm, full=True):
    bt = 60.0 / bpm; t = t0; prog = dict(trap=TRAP, chip=CHIP, clock=TRAP)[kind]
    while t < t1 - 1e-3:
        bar = int(np.floor((t - t0) / (4 * bt) + 1e-6)); b0 = t0 + bar * 4 * bt; root, ch = prog[bar % 4]
        for e in range(16):                                   # sixteenth notes
            u = b0 + e * bt / 4; beat = e // 4
            if u < t0 - 1e-3 or u >= t1: continue
            if kind == 'trap':
                if e in (0, 10): put(bed, kick(), u, 0.85); put(bed, b808(midi(root - 12), bt * (2.4 if e == 0 else 1.4)), u, 0.42)
                if e in (8,): put(bed, clap(), u, 0.5); put(bed, snare(), u, 0.3)
                if e % 2 == 0 or (bar % 2 == 1 and e >= 12): put(bed, hat(), u, 0.09 if e % 4 else 0.12)
                if full and e % 2 == 0: put(bed, saw(midi(ch[(e // 2) % 3] + 12), bt * 0.4, 2600), u, 0.05)
            elif kind == 'chip':
                if e % 4 == 0: put(bed, kick(), u, 0.6)
                if e in (4, 12): put(bed, snare(), u, 0.32)
                if e % 2 == 1: put(bed, hat(), u, 0.06)
                put(bed, chip(midi(ch[e % 3] + 12), bt * 0.22, 0.125), u, 0.05)
                if e % 4 == 0: put(bed, tri(midi(root - 12 + (7 if e == 8 else 0)), bt * 0.9), u, 0.32)
            else:                                             # clock: ticking pulse, low pad, bell on each bar
                if e % 4 == 0: put(bed, clock(), u, 0.35 if e % 8 == 0 else 0.22); put(bed, kick(), u, 0.5 if e in (0, 8) else 0.3)
                if e == 0: put(bed, sum(pad(midi(m - 12), 4 * bt) for m in ch), u, 0.06); put(bed, bell(midi(ch[0] + 12), 1.2), u, 0.07)
                if e in (6, 14): put(bed, pluck(midi(ch[(bar + e) % 3]), bt), u, 0.18)
                if e % 2 == 1: put(bed, hat(), u, 0.04)
        if kind == 'chip':
            for b, m in CMEL[bar % 4]:
                if t0 <= b0 + b * bt < t1: put(bed, chip(midi(m), bt * 0.45, 0.5), b0 + b * bt, 0.06)
        t = b0 + 4 * bt


# ---------------------------------------------------------------- the score
section(0, C['promised'], 'trap', 140)
section(C['promised'], C['yousee'], 'chip', 150)
section(C['yousee'], C['sofar'], 'clock', 120)
section(C['sofar'], C['end'], 'trap', 140)

# ---------------------------------------------------------------- effects on the beats
put(fx, boom(), 0.0, 0.45); put(fx, kick(), 0.0, 0.7); put(fx, stampfx(), 0.03, 0.4); put(fx, whoosh(0.5, 600, 4000), 0.0, 0.2)
for k in ('nov19', 'first', 'cal18'): put(fx, bell(midi(84), 0.6), C[k], 0.1)
put(fx, stampfx(), C['first'] + 0.05, 0.35)
put(fx, whoosh(0.7, 400, 3000), C['promised'] - 0.2, 0.22); put(fx, beep(1320, 0.1), C['fall'], 0.2)
for k in ('may', 'nov19b'): put(fx, stampfx(), C[k] - 0.3, 0.5); put(fx, buzzer(), C[k] - 0.25, 0.18); put(fx, beep(1568, 0.1), C[k], 0.2)
put(fx, buzzer(), C['two'], 0.35); put(fx, stampfx(), C['two'], 0.4)
put(fx, kaching(), C['most'], 0.3); put(fx, cheer(1.0), C['most'], 0.1); fanfare(C['ps'] + 0.05, 77)
put(fx, whoosh(0.8, 300, 2500), C['box'] - 0.1, 0.25); put(fx, riser(0.9), C['box'] + 0.2, 0.15)
put(fx, flip(), C['nodisc'] - 0.05, 0.6); put(fx, stampfx(), C['nodisc'], 0.55); put(fx, boing(), C['nodisc'] + 0.2, 0.15)
for k in range(3): put(fx, beep(1760, 0.07), C['code'] + 0.12 * k, 0.15)
put(fx, boom(), C['gb'], 0.4); put(fx, stampfx(), C['gb'], 0.35)
put(fx, scratch(), C['yousee'] - 0.05, 0.14); put(fx, stampfx(), C['moment'], 0.45)
put(fx, bell(midi(72), 1.4), C['midnight'], 0.16); put(fx, bell(midi(79), 1.0), C['midnight'] + 0.2, 0.1)
put(fx, whoosh(0.6, 500, 3500), C['country'], 0.2)
put(fx, boom(), C['nz'], 0.35); put(fx, cheer(1.2), C['nz'] + 0.1, 0.12); fanfare(C['nz'] + 0.05, 79)
put(fx, whoosh(0.8, 300, 2500), C['london'] - 0.1, 0.25); put(fx, bell(midi(76), 1.0), C['eleven'], 0.12)
put(fx, whoosh(0.8, 300, 2500), C['ny'] - 0.1, 0.25); put(fx, beep(1046, 0.25), C['six'], 0.15)
put(fx, whoosh(1.2, 200, 2000), C['wave'], 0.3)
for k in range(3): put(fx, beep(1175 + 220 * k, 0.09), C['wave'] + 0.45 + 0.35 * k, 0.15)
put(fx, stampfx(), C['years'], 0.5); sadbone(C['years'] + 0.1)
put(fx, bell(midi(84), 0.5), C['launch'], 0.1); put(fx, stampfx(), C['fit'], 0.55)
put(fx, cheer(1.0), C['already'], 0.12); put(fx, stampfx(), C['already'] + 0.05, 0.3)
put(fx, riser(1.4), C['end'] - 1.5, 0.22); put(fx, stampfx(), C['still'], 0.4)

mix = bed * 1.35 + fx * 0.85
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 2.2) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, trap launch beat 140 bpm F minor + 8-bit chiptune 150 bpm + ticking clock pulse" % LEN)
