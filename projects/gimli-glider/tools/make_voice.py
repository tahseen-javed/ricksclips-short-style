#!/usr/bin/env python3
"""Deep, clear American male voiceover with Kokoro TTS (free, runs on the runner).
Renders the script with several male voices and blends, keeps the deepest one that Whisper still
understands as well as the clearest, then adds weight: a slight pitch drop, warm low end, presence
for clarity, gentle compression. Pauses squeezed to <= 0.16 s, tempo for the target, -15 LUFS.
usage: make_voice.py <audio folder> <target seconds>"""
import os, re, sys, difflib, subprocess
import numpy as np, soundfile as sf, torch, torchaudio, whisper
from kokoro import KPipeline

d = sys.argv[1].rstrip("/") + "/"; target = float(sys.argv[2]); SR = 24000; SPEED = 1.2
text = open(d + "tts.txt", encoding="utf-8").read()
pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
CANDS = ["am_fenrir", "am_michael", "am_fenrir,am_michael", "am_fenrir,am_onyx", "am_michael,am_onyx", "am_fenrir,am_michael,am_onyx"]


def gen(voice, speed):
    parts = []
    for _, _, a in pipe(text, voice=voice, speed=speed, split_pattern=r"\n+"):
        a = np.asarray(a, dtype=np.float32); idx = np.where(np.abs(a) > 0.012)[0]
        if len(idx): a = a[max(0, idx[0] - int(0.03 * SR)): min(len(a), idx[-1] + int(0.12 * SR))]
        parts += [a, np.zeros(int(0.04 * SR), np.float32)]
    return np.concatenate(parts)


def squeeze(a, keep=0.16, thr=0.012):
    hop = int(0.01 * SR); n = len(a) // hop; out = []; i = 0
    env = np.array([np.abs(a[k * hop:(k + 1) * hop]).max() for k in range(n)])
    while i < n:
        if env[i] >= thr: out.append(a[i * hop:(i + 1) * hop]); i += 1; continue
        j = i
        while j < n and env[j] < thr: j += 1
        seg = a[i * hop:i * hop + min((j - i) * hop, int(keep * SR))].copy(); f = min(len(seg), int(0.01 * SR))
        if f: seg[-f:] *= np.linspace(1, 0, f)
        out.append(seg); i = j
    out.append(a[n * hop:]); return np.concatenate(out)


def pitch_hz(a):
    f = torchaudio.functional.detect_pitch_frequency(torch.from_numpy(a).float(), SR, freq_low=60, freq_high=300).numpy()
    f = f[(f > 60) & (f < 300)]
    return float(np.median(f)) if len(f) else 999.0


asr = whisper.load_model("base.en")
norm = lambda s: re.sub(r"[^a-z0-9' ]+", " ", s.lower().replace("’", "'")).split()
ref = norm(text)


def understood(a):
    sf.write(d + "_cand.wav", a, SR)
    hyp = norm(asr.transcribe(d + "_cand.wav", language="en")["text"])
    return difflib.SequenceMatcher(None, ref, hyp, autojunk=False).ratio()


rows = []
for v in CANDS:
    try: a = squeeze(gen(v, SPEED))
    except Exception as e: print("skip %s: %s" % (v, e)); continue
    rows.append((v, a, pitch_hz(a), understood(a)))
    print("%-30s %5.1f s  pitch %5.1f Hz  understood %.3f" % (v, len(a) / SR, rows[-1][2], rows[-1][3]))
if os.path.exists(d + "_cand.wav"): os.remove(d + "_cand.wav")
best = max(r[3] for r in rows)
v, a, hz, sco = min([r for r in rows if r[3] >= best - 0.01], key=lambda r: r[2])   # the deepest of the clearest
p = min(1.0, max(0.93, 98.0 / hz))           # pitch (and formants) down a touch for a bigger voice, at most ~1.3 semitones
dur = len(a) / SR; tempo = min(1.1, max(1.0, dur / target))
print("chose %s (pitch %.0f Hz, understood %.3f): pitch x%.3f, tempo %.3f -> about %.1f s" % (v, hz, sco, p, tempo, dur / tempo))
sf.write(d + "voice_raw.wav", a / max(1e-6, np.abs(a).max()) * 0.9, SR)
af = ("asetrate=%d,aresample=%d,atempo=%.4f,highpass=f=60,bass=g=3.5:f=140:w=0.9,equalizer=f=3000:t=q:w=1.2:g=2,"
      "acompressor=threshold=0.125:ratio=2.5:attack=8:release=120:makeup=1.5,loudnorm=I=-15:TP=-1.5:LRA=9,apad=pad_dur=0.5") % (int(SR * p), SR, tempo / p)
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", d + "voice_raw.wav", "-af", af, "-ar", "44100", "-b:a", "192k", d + "voice.mp3"], check=True)
os.remove(d + "voice_raw.wav")
