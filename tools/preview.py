#!/usr/bin/env python3
"""Composite a view (bg + all sprites, optional hotspot outlines) to a PNG for quick review.
   preview.py c1_n [c1_e ...] [--hot] [--sprites] [--variant name] [--out path]"""
import sys, json, os
from PIL import Image, ImageDraw
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ART = os.path.join(ROOT, "assets", "art")
views = json.load(open(os.path.join(ROOT, "assets", "data", "views.json")))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
hot = "--hot" in sys.argv
nosp = "--nosprites" in sys.argv
variant = None
out = "/tmp/claude-0/scratch/preview.png"
if "--variant" in sys.argv: variant = sys.argv[sys.argv.index("--variant") + 1]; args.remove(variant)
if "--out" in sys.argv: out = sys.argv[sys.argv.index("--out") + 1]; args.remove(out)
sheets = []
for vid in args:
    v = views[vid]
    bg = None
    for b in v["bg"]:
        if variant is None or b["variant"] == variant:
            bg = b; break
    if bg is None and v["bg"]: bg = v["bg"][-1]
    im = Image.open(os.path.join(ART, bg["tex"])).convert("RGBA") if bg else Image.new("RGBA", tuple(v["size"]), (60, 70, 70, 255))
    if not nosp:
        for s in v["sprites"]:
            if "tex" not in s: continue
            sp = Image.open(os.path.join(ART, s["tex"])).convert("RGBA")
            if s.get("ref"):
                sc = s.get("scale", 1.0)
                if sc != 1.0: sp = sp.resize((int(sp.size[0] * sc), int(sp.size[1] * sc)))
                px, py = s["pos"]
                x0 = int(px - sp.size[0] / 2); y0 = int(py - (sp.size[1] if s.get("anchor", "bc") == "bc" else sp.size[1] / 2))
                if s.get("alpha", 1.0) < 1.0:
                    a = sp.split()[3].point(lambda p: int(p * s["alpha"])); sp.putalpha(a)
                if "--here" in sys.argv and "_near" in s["id"]: continue
                if "--near" in sys.argv and "_here" in s["id"]: continue
                tmp = Image.new("RGBA", im.size, (0,0,0,0)); tmp.paste(sp, (x0, y0)); im = Image.alpha_composite(im, tmp)
            else:
                im.alpha_composite(sp, (int(s["rect"][0]), int(s["rect"][1])))
    if hot:
        d = ImageDraw.Draw(im, "RGBA")
        for h in v["hotspots"]:
            x, y, w, hh = h["rect"]
            d.rectangle([x, y, x + w, y + hh], outline=(255, 80, 80, 230), width=3, fill=(255, 80, 80, 28))
            d.text((x + 4, y + 2), h["id"], fill=(255, 255, 255, 255))
    sheets.append(im)
if len(sheets) == 1:
    sheets[0].convert("RGB").save(out)
else:
    cols = 2 if len(sheets) > 1 else 1
    rows = (len(sheets) + cols - 1) // cols
    W, H = sheets[0].size
    sc = 0.5
    sheet = Image.new("RGB", (int(W * sc) * cols, int(H * sc) * rows), (0, 0, 0))
    for i, s in enumerate(sheets):
        sheet.paste(s.convert("RGB").resize((int(W * sc), int(H * sc))), ((i % cols) * int(W * sc), (i // cols) * int(H * sc)))
    sheet.save(out)
print(out)
