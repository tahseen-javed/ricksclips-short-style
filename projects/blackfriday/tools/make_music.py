#!/usr/bin/env python3
"""Music + effects for the Black Friday Short, synthesised in code (no samples).
Electro-swing in A minor at 124 bpm from frame 1: four-on-the-floor kick, clap, swung hats, sleigh bells, a walking upright
bass, off-beat swing piano and muted-trumpet riffs, with a police whistle + brass hit on the first frame.  Sirens and car horns
for the gridlock, a noir cop groove (minor walking bass, vibes, brushed snare) in the police station, a cheesy fanfare and
crickets for BIG FRIDAY, map-pin pops, a 1980s synthwave section (gated snare, saw bass, square arpeggio) for the red-to-black
story, a buzzer + record scratch for NOT TRUE, then the full swing band, cash registers and a riser into the loop.
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


SWG = [(45, (57, 60, 64)), (50, (57, 62, 65)), (52, (56, 59, 62, 64)), (45, (57, 60, 64))]        # Am Dm E7 Am, one bar each
WALK = [(0, 7, 12, 10), (0, 3, 7, 6), (0, 4, 7, 10), (0, 7, 5, 4)]
NOIR = [(45, (57, 60, 64, 67)), (41, (57, 60, 64, 65)), (44, (56, 59, 62, 65)), (45, (57, 60, 64, 67))]
WAVE = [(45, (57, 60, 64)), (41, (57, 60, 65)), (48, (55, 60, 64)), (43, (55, 59, 62))]          # Am F C G
RIFF = [(0, 76, .2), (1, 74, .2), (1.5, 72, .2), (2, 69, .45), (3.5, 72, .25)]                   # muted trumpet answer (beat, midi, len)


def band(t0, t1, kind='full'):
    t = t0
    while t < t1 - 1e-3:
        bar = int(np.floor(t / (4 * BT) + 1e-6)); b0 = bar * 4 * BT
        prog = WAVE if kind == 'wave' else NOIR if kind == 'noir' else SWG; root, chord = prog[bar % 4]
        for bt in range(4):
            for sub, off in ((0, 0.0), (1, SW)):
                u = b0 + bt * BT + off
                if u < t0 - 1e-3 or u >= t1: continue
                if kind in ('full', 'lite'):
                    if sub == 0: put(bed, kick(), u, 0.85 if kind == 'full' else 0.55)
                    if sub == 0 and bt % 2 == 1: put(bed, clap(), u, 0.5 if kind == 'full' else 0.3)
                    put(bed, hat(sub == 1 and bt == 3), u, 0.16 if sub else 0.1)
                    if kind == 'full': put(bed, jingle(), u, 0.09 if sub else 0.06)
                    if sub == 0: put(bed, pluck(midi(root + WALK[bar % 4][bt] - 12), BT * 0.9), u, 0.55)
                    if sub == 1: put(bed, sum(piano(midi(m), 0.25) for m in chord), u, 0.075)
                elif kind == 'noir':
                    if sub == 0 and bt == 0: put(bed, kick(), u, 0.7)
                    if sub == 0 and bt == 2: put(bed, filt(snare(), 'lowpass', 3000), u, 0.25)
                    put(bed, hat(), u, 0.08 if sub else 0.05)
                    if sub == 0: put(bed, pluck(midi(root + (0, 3, 7, 6)[bt] - 12), BT * 0.9), u, 0.6)
                    if sub == 0 and bt in (0, 2): put(bed, sum(bell(midi(m), 0.9) for m in chord), u, 0.03)
                elif kind == 'wave' and sub == 0:
                    put(bed, kick(), u, 0.85)
                    if bt % 2 == 1: put(bed, gated(), u, 0.5)
                    for e in (0, 0.5): put(bed, saw(midi(root - 12), BT * 0.45, 900), u + e * BT, 0.3); put(bed, hat(), u + e * BT, 0.08)
                    for q in range(4): put(bed, sq(midi(chord[q % len(chord)] + 12), BT / 4 * 0.9), u + q * BT / 4, 0.07)
                    if bt == 0: put(bed, sum(saw(midi(m), 4 * BT, 2400) for m in chord), u, 0.035)
        if kind == 'full' and bar % 2 == 1:
            for b, m, ln in RIFF:
                if t0 <= b0 + b * BT < t1: put(bed, brass(midi(m), ln, 2400), b0 + b * BT, 0.06)
        t = b0 + 4 * BT


def stab(t, g=1.0): put(fx, sum(brass(midi(m), 0.3) for m in (69, 72, 76, 81)), t, 0.1 * g); put(fx, clap(), t, 0.5 * g); put(fx, kick(), t, 0.6 * g)
def fanfare(t):
    for k, (m, d) in enumerate(((72, .14), (76, .14), (79, .14), (84, .6))): put(fx, sum(brass(midi(m + x), d) for x in (0, -5, -12)), t + k * 0.13, 0.085)
def sadbone(t):
    for k, m in enumerate((62, 61, 60, 59)): d = 0.3 if k < 3 else 0.8; put(fx, brass(midi(m), d, 1400) * (1 + 0.3 * np.sin(2 * np.pi * 6 * ts(d))), t + k * 0.28, 0.11)


# ---------------------------------------------------------------- the score
band(0, C['nocop'], 'full')
band(C['nocop'], C['hate'], 'noir')
band(C['hate'], C['nobody'], 'full')
band(C['nobody'], C['yousee'], 'lite')
band(C['yousee'], C['e80'], 'full')
band(C['e80'], C['isnt'] + 0.1, 'wave')
band(C['today'], C['end'], 'full')

# ---------------------------------------------------------------- effects on the beats
put(fx, whistle(0.55), 0.0, 0.16); stab(0.0, 1.3); put(fx, kaching(), 0.05, 0.25); put(fx, stampfx(), max(0.3, C['named'] - 1.0), 0.5)
put(fx, siren(1.3), C['named'], 0.1); put(fx, whistle(0.4), C['furious'], 0.14)
for k in range(3): put(fx, horn(300 + 40 * k), C['furious'] + 0.12 * k, 0.12)
stab(C['philly'], 0.8); put(fx, cheer(1.6), C['philly'], 0.05); put(fx, gobble(), C['thx'] + 0.1, 0.12); put(fx, whoosh(1.0, 300, 2500), C['flood'] - 0.1, 0.25)
put(fx, cheer(2.4), C['sat'], 0.12); fanfare(C['army']); put(fx, kick(), C['ball'], 0.8); put(fx, whoosh(0.8, 800, 4000), C['ball'] + 0.05, 0.3); put(fx, cheer(1.4), C['tour'], 0.16)
for k in range(5): put(fx, horn(260 + 37 * k), C['grid'] + 0.1 * k, 0.13)
put(fx, stampfx(), C['grid'], 0.5); put(fx, cheer(0.8), C['crowds'], 0.14); put(fx, stampfx(), C['crowds'], 0.5)
put(fx, stampfx(), C['chaos'], 0.55); put(fx, whistle(0.5), C['chaos'], 0.16); put(fx, siren(1.0), C['chaos'] + 0.1, 0.08); put(fx, horn(310), C['chaos'] + 0.3, 0.12)
put(fx, scratch(), C['nocop'] - 0.05, 0.12); put(fx, siren(0.9), C['nocop'] + 0.1, 0.05)
for k in range(8): put(fx, tick(), C['twelve'] - 0.4 + 0.25 * k, 0.4)
put(fx, bell(midi(81), 1.0), C['twelve'], 0.1); put(fx, boom(), C['dark'], 0.4); put(fx, stampfx(), C['bf2'], 0.6); put(fx, boom(), C['bf2'], 0.5)
put(fx, scratch(), C['hate'] - 0.05, 0.12); put(fx, stampfx(), C['hate'] + 0.3, 0.45); fanfare(C['big'] - 0.1); put(fx, kaching(), C['big'], 0.2)
put(fx, crickets(max(0.5, C['yousee'] - C['nobody'])), C['nobody'] + 0.1, 0.06); sadbone(C['nobody'] + 0.2)
stab(C['yousee'], 0.9); put(fx, boing(), C['refuse'], 0.14)
for k in range(12): put(fx, beep(700 + 90 * k, 0.07), C['spreads'] + (C['country'] - C['spreads'] + 0.2) * k / 12, 0.08)
put(fx, whoosh(1.2, 300, 2500), C['slowly'], 0.25); stab(C['country'], 1.0)
put(fx, bell(midi(88), 0.9), C['switch'], 0.12); put(fx, riser(0.9), C['change'] - 0.6, 0.18); stab(C['change'], 1.0)
put(fx, scratch(), C['e80'] - 0.05, 0.12); put(fx, sweep(200, 1600, 0.8, -2) * env(int(SR * 0.8), 0.05, 0.2), C['e80'], 0.05)
put(fx, sweep(900, 120, 0.7, 3) * env(int(SR * 0.7), 0.02, 0.2), C['red'], 0.08); put(fx, kaching(), C['black'], 0.4); fanfare(C['black'] + 0.05)
for k in range(6): put(fx, bell(midi(88 + (0, 4, 7)[k % 3]), 0.4), C['perfect'] + 0.08 * k, 0.06)
put(fx, buzzer(), C['isnt'], 0.5); put(fx, scratch(), C['isnt'] + 0.05, 0.16); put(fx, stampfx(), C['isnt'], 0.55)
stab(C['today'], 1.2); put(fx, cheer(C['notone'] - C['today']), C['today'], 0.1); put(fx, kaching(), C['today'] + 0.1, 0.3)
put(fx, stampfx(), C['insult'], 0.55); put(fx, whistle(0.35), C['insult'] + 0.1, 0.1)
put(fx, filt(noise(0.5), 'highpass', 3000) * env(int(SR * 0.5), 0.1, 0.2), C['tell'], 0.12)
put(fx, riser(1.2), C['loop'] - 1.0, 0.22); stab(C['loop'], 1.1); put(fx, whistle(0.4), C['loop'] + 0.05, 0.12)

mix = bed * 0.9 + fx
mix = np.tanh(mix / max(1e-6, np.abs(mix).max()) * 1.6) * 0.89
st = np.stack([mix, np.roll(mix, int(SR * 0.008)) * 0.96], 1)
sf.write(OUT, st.astype(np.float32), SR)
print("music: %.1f s, electro-swing 124 bpm A minor + noir + synthwave" % LEN)
