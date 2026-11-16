#!/usr/bin/env python3
"""Intelligibility check: transcribe the finished voice with Whisper and compare with the spoken text.
usage: check_voice.py voice.mp3 tts.txt"""
import os, re, sys, difflib
import whisper

audio, ref_path = sys.argv[1], sys.argv[2]
sp = os.path.join(os.path.dirname(ref_path), "script.txt")   # digits on both sides: only real mishearings count
if os.path.exists(sp): ref_path = sp
norm = lambda s: re.sub(r"[^a-z0-9' ]+", " ", s.lower().replace("’", "'")).split()
ref = norm(open(ref_path, encoding="utf-8").read())
r = whisper.load_model(os.environ.get("SHORTKIT_WHISPER_MODEL", "small")).transcribe(audio, language="en")
hyp = norm(r["text"]); sm = difflib.SequenceMatcher(None, ref, hyp, autojunk=False)
print("heard:", r["text"].strip())
print("intelligibility %.3f (1.0 = every word understood)" % sm.ratio())
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != "equal": print("  %s: said %s -> heard %s" % (tag, ref[i1:i2], hyp[j1:j2]))
