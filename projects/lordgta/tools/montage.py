#!/usr/bin/env python3
"""Contact sheets for review.
  montage.py stills <stills dir> <out dir> [shots per sheet]   3 stills per shot, 2 shots per row
  montage.py frames <frames dir> <out.jpg> <t0> <fps>          every extracted frame, labelled with its time"""
import os, re, sys, glob
from PIL import Image, ImageDraw

mode = sys.argv[1]
if mode == "stills":
    src, out = sys.argv[2], sys.argv[3]; per = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    os.makedirs(out, exist_ok=True); shots = {}
    for f in sorted(glob.glob(os.path.join(src, "shot*_*.jpg"))):
        m = re.match(r"shot(\d+)_([a-c])\.jpg", os.path.basename(f))
        if m: shots.setdefault(int(m.group(1)), {})[m.group(2)] = f
    ids = sorted(shots); CW, CH = 270, 480
    for si in range(0, len(ids), per):
        grp = ids[si:si + per]; rows = (len(grp) + 1) // 2
        im = Image.new("RGB", (6 * CW, rows * (CH + 22)), (24, 22, 30)); d = ImageDraw.Draw(im)
        for gi, sid in enumerate(grp):
            c0, row = (gi % 2) * 3, gi // 2; y0 = row * (CH + 22)
            d.text((c0 * CW + 6, y0 + 5), "S%02d" % sid, fill=(255, 255, 255))
            for ci, k in enumerate("abc"):
                if k in shots[sid]:
                    im.paste(Image.open(shots[sid][k]).convert("RGB").resize((CW, CH), Image.LANCZOS), ((c0 + ci) * CW, y0 + 22))
        im.save(os.path.join(out, "sheet_%02d.jpg" % (si // per + 1)), quality=88)
    print("sheets:", (len(ids) + per - 1) // per, "shots:", len(ids))
else:
    src, out, t0, fps = sys.argv[2], sys.argv[3], float(sys.argv[4]), float(sys.argv[5])
    files = sorted(glob.glob(os.path.join(src, "f*.png"))); cols = 8; CW = 240
    ims = [Image.open(f).convert("RGB") for f in files]
    if not ims: sys.exit("no frames")
    CH = int(ims[0].height * CW / ims[0].width); rows = (len(ims) + cols - 1) // cols
    im = Image.new("RGB", (cols * CW, rows * (CH + 16)), (24, 22, 30)); d = ImageDraw.Draw(im)
    for i, fr in enumerate(ims):
        x, y = (i % cols) * CW, (i // cols) * (CH + 16)
        d.text((x + 4, y + 2), "%.2fs" % (t0 + i / fps), fill=(255, 255, 255)); im.paste(fr.resize((CW, CH), Image.LANCZOS), (x, y + 16))
    im.save(out, quality=88); print("frames:", len(ims))
