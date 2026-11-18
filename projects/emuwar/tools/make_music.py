#!/usr/bin/env python3
"""Music + effects for the Emu War Short, synthesised in code (no samples).
A Western showdown (120 bpm E minor: twang guitar, whistled melody, whip crack) from frame 1 with a machine-gun burst;
a bush-band country tune (banjo boom-chick, fiddle, washboard, stomp-clap) for the farms and the bounty; a surf-rock chase
(168 bpm, tremolo twang) for the shooting; a tense ticking pulse for the Major; the showdown returns for the loop.
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


WEST = [(40, (64, 67, 71)), (43, (67, 71, 74)), (45, (69, 72, 76)), (47, (66, 71, 75))]       # Em G Am B7, 120 bpm
WMEL = [(0, 76), (0.5, 79), (1, 81), (2, 83), (3, 81)], [(0, 79), (1, 76), (2, 74), (3, 71)], [(0, 76), (0.5, 79), (1, 81), (2, 84), (3, 83)], [(0, 81), (1, 78), (2, 75), (3.5, 71)]
BUSH = [(43, (67, 71, 74)), (48, (67, 72, 76)), (50, (66, 69, 74)), (43, (67, 71, 74))]       # G C D G, 132 bpm
SURF = [(40, (64, 67, 71)), (43, (67, 71, 74)), (45, (69, 72, 76)), (48, (67, 72, 76))]       # Em G Am C, 168 bpm


def section(t0, t1, kind, bpm, full=True):
    bt = 60.0 / bpm; t = t0; prog = dict(west=WEST, bush=BUSH, surf=SURF, tense=WEST)[kind]
    while t < t1 - 1e-3:
        bar = int(np.floor((t - t0) / (4 * bt) + 1e-6)); b0 = t0 + bar * 4 * bt; root, ch = prog[bar % 4]
        for e in range(8):
            u = b0 + e * bt / 2; beat = e // 2; on = e % 2 == 0
            if u < t0 - 1e-3 or u >= t1: continue
            if kind == 'west':
                if on and beat in (0, 2): put(bed, kick(), u, 0.8); put(bed, twang(midi(root), bt * 0.9), u, 0.3)
                if on and beat in (1, 3): put(bed, snare(), u, 0.38); put(bed, clap(), u, 0.25)
                if not on: put(bed, twang(midi(ch[e % 3]), bt * 0.4), u, 0.08)
                put(bed, hat(), u, 0.08)
            elif kind == 'bush':
                if on and beat in (0, 2): put(bed, kick(), u, 0.7); put(bed, pluck(midi(root - (0 if beat == 0 else 5)), bt * 0.8), u, 0.45)
                if on and beat in (1, 3): put(bed, sum(banjo(midi(m)) for m in ch), u, 0.12); put(bed, clap(), u, 0.3)
                put(bed, hat(), u, 0.07); put(bed, hat(), u + bt / 4, 0.05)
                put(bed, banjo(midi(ch[(e + bar) % 3] + 12)), u, 0.08)
            elif kind == 'surf':
                put(bed, kick(), u, 0.6 if on else 0.35)
                if beat in (1, 3) and on: put(bed, snare(), u, 0.45)
                put(bed, hat(), u, 0.09)
                for q in range(2): put(bed, twang(midi(ch[(e + q) % 3] + (12 if full else 0)), bt * 0.22), u + q * bt / 4, 0.07)
                if on: put(bed, pluck(midi(root - 12), bt * 0.45), u, 0.4)
            else:                                                     # tense: low drone, ticking, sparse plucks
                put(bed, tick(), u, 0.3)
                if on: put(bed, kick(), u, 0.55)
                if e == 0: put(bed, sum(strings_(midi(m - 12), 4 * bt) for m in ch), u, 0.05); put(bed, kick(), u, 0.5)
                if e == 4: put(bed, pluck(midi(ch[1]), bt), u, 0.2)
        if kind == 'west' and full:
            for b, m in WMEL[bar % 4]:
                if t0 <= b0 + b * bt < t1: put(bed, whis(midi(m), bt * 0.8), b0 + b * bt, 0.1)
        if kind == 'bush':
            m = ch[bar % 3] + 12
            if t0 <= b0 < t1: put(bed, fiddle(midi(m), 4 * bt * 0.95), b0, 0.05)
        t = b0 + 4 * bt


def strings_(f, d): t = ts(d); x = sum(np.sin(2 * np.pi * f * h * t) / h for h in range(1, 8)); return filt(x, 'lowpass', 1500) * env(len(t), 0.2, 0.3)


# ---------------------------------------------------------------- the score
section(0, C['campion'], 'west', 120)
section(C['campion'], C['pearce'], 'bush', 132)
section(C['pearce'], C['week'], 'west', 120, full=False)
section(C['week'], C['yousee'], 'surf', 168)
section(C['yousee'], C['gov'], 'tense', 120)
section(C['gov'], C['lost'], 'bush', 132)
section(C['lost'], C['end'], 'west', 120)

# ---------------------------------------------------------------- effects on the beats
put(fx, whip(), 0.0, 0.5); stab(0.0, 1.3); put(fx, gunfire(0.6), 0.05, 0.16); put(fx, boom(), C['war'], 0.4)
put(fx, boing(), C['feathers'], 0.2); put(fx, poof(), C['feathers'], 0.3); fanfare(C['won'] - 0.05); put(fx, cheer(1.0), C['won'], 0.1); put(fx, stampfx(), C['won'] + 0.1, 0.4)
put(fx, whoosh(0.9, 300, 2500), C['campion'] - 0.1, 0.25); put(fx, stampfx(), C['y1932'], 0.45)
put(fx, wind(C['farms'] - C['drought']), C['drought'], 0.25); put(fx, stampfx(), C['drought'], 0.45); put(fx, thumps(1.6), C['e20k'], 0.35); put(fx, stampfx(), C['e20k'], 0.35)
put(fx, whoosh(0.8, 400, 3000), C['farms'], 0.25); put(fx, bell(midi(86), 0.8), C['vets'], 0.1)
for k in range(4): put(fx, crunch(), C['wrecked'] - 0.2 + 0.12 * k, 0.4)
put(fx, stampfx(), C['wrecked'], 0.5); sadbone(C['beg'] + 0.1)
stab(C['pearce'], 0.9); put(fx, tick(), C['answer'], 0.8); put(fx, stampfx(), C['answer'] + 0.05, 0.55)
put(fx, drum_roll(0.8), C['army'], 0.25); put(fx, stampfx(), C['three'], 0.4); put(fx, stampfx(), C['guns'], 0.4); put(fx, bell(midi(81), 0.5), C['guns'] + 0.1, 0.08)
put(fx, stampfx(), C['rounds'], 0.4); put(fx, kaching(), C['rounds'] + 0.1, 0.15)
put(fx, whoosh(0.8, 300, 2500), C['week'] - 0.1, 0.2); put(fx, gunfire(1.0), C['week'] + 0.2, 0.14); put(fx, stampfx(), C['gone'], 0.5); put(fx, gunfire(0.5, 14), C['gone'] + 0.2, 0.1)
put(fx, engine(1.2, 70, 0.3), C['pulled'], 0.12); put(fx, scratch(), C['pulled'] - 0.05, 0.1); put(fx, engine(1.0, 80, 0.2), C['back'], 0.12); put(fx, buzzer(), C['same'], 0.4)
put(fx, gunfire(1.4, 13), C['fired'], 0.16); put(fx, stampfx(), C['fired'] + 0.05, 0.4); put(fx, stampfx(), C['birds'], 0.45); put(fx, boing(), C['birds'] + 0.15, 0.15)
put(fx, bell(midi(88), 0.9), C['ten'], 0.12); put(fx, stampfx(), C['ten'], 0.35)
put(fx, scratch(), C['yousee'] - 0.05, 0.14); put(fx, gunfire(1.0), C['emus'], 0.12); put(fx, boing(), C['emus'] + 0.3, 0.12); put(fx, stampfx(), C['tanks'], 0.55); put(fx, boom(), C['tanks'], 0.5)
put(fx, stampfx(), C['gov'] + 0.1, 0.5); put(fx, kaching(), C['paid'] + 0.2, 0.35); put(fx, kaching(), C['bounty'], 0.3); put(fx, stampfx(), C['noguns'], 0.5)
put(fx, whoosh(0.8, 400, 3000), C['six'] - 0.1, 0.2)
for k in range(3): put(fx, kaching(), C['b57'] + 0.18 * k, 0.25)
put(fx, cheer(1.2), C['b57'], 0.1); fanfare(C['x58'] + 0.05, 79)
sadbone(C['lost'] + 0.05); put(fx, stampfx(), C['lost'], 0.5); put(fx, kaching(), C['cash'], 0.45); put(fx, cheer(0.9), C['cash'], 0.12)
put(fx, riser(1.1), C['loop'] - 0.9, 0.22); stab(C['loop'], 1.1); put(fx, whip(), C['loop'] + 0.05, 0.4); put(fx, stampfx(), C['y1932b'], 0.5)

mix = bed * 1.35 + fx * 0.85
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 2.2) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, western showdown 120 bpm E minor + bush-band country + surf-rock chase + tense pulse" % LEN)
