#!/usr/bin/env python3
"""Subset system fonts into assets/fonts/ using only the glyphs the string tables need.

Sources (all SIL OFL): EB Garamond, Liberation Sans, Noto Serif/Sans CJK.
Install on Debian/Ubuntu: apt install fonts-ebgaramond fonts-liberation fonts-noto-cjk
Run after editing tools/i18n/* and tools/build_i18n.py.
"""
import json, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont, TTCollection

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "fonts")
OT = "/usr/share/fonts/opentype"
TT = "/usr/share/fonts/truetype"

def chars_for(lang):
    s = set(chr(c) for c in range(0x20, 0x7F))
    s.update(chr(c) for c in range(0xA0, 0x100))
    s.update("‘’“”–—…•·←↑→↓●○✓×")
    for l in {"en", lang}:
        with open(os.path.join(ROOT, "assets", "i18n", l + ".json"), encoding="utf-8") as f:
            for k, v in json.load(f).items():
                s.update(v)
                s.update(k)
    s.discard("\n")
    return "".join(sorted(s))

def open_font(path, index_hint=None):
    if path.endswith(".ttc"):
        col = TTCollection(path)
        for f in col.fonts:
            n = f["name"].getDebugName(1) or ""
            if index_hint and index_hint in n:
                return f
        raise SystemExit(f"{path}: no face matching {index_hint}")
    return TTFont(path)

def make(out_name, src, lang, hint=None):
    font = open_font(src, hint)
    opts = subset.Options()
    opts.layout_features = ["kern", "liga", "locl", "vert", "vrt2", "palt"]
    opts.name_IDs = [0, 1, 2, 3, 4, 6, 13, 14]
    opts.notdef_outline = True
    opts.glyph_names = False
    opts.hinting = False
    opts.legacy_kern = True
    sub = subset.Subsetter(opts)
    sub.populate(text=chars_for(lang))
    sub.subset(font)
    path = os.path.join(OUT, out_name)
    font.flavor = None
    font.save(path)
    print(f"{out_name:16s} {os.path.getsize(path)//1024:5d} KB  <- {os.path.basename(src)} {hint or ''}")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    garamond = OT + "/ebgaramond/EBGaramond12-Regular.otf"
    garamond_small = OT + "/ebgaramond/EBGaramond08-Regular.otf"
    sans = TT + "/liberation/LiberationSans-Regular.ttf"
    serif_cjk = OT + "/noto/NotoSerifCJK-Regular.ttc"
    sans_cjk = OT + "/noto/NotoSansCJK-Regular.ttc"
    make("world.ttf", garamond, "en")
    make("ui.ttf", garamond_small, "en")
    make("plain.ttf", sans, "en")
    make("world_zh.ttf", serif_cjk, "zh", "SC")
    make("ui_zh.ttf", serif_cjk, "zh", "SC")
    make("plain_zh.ttf", sans_cjk, "zh", "SC")
    make("world_ja.ttf", serif_cjk, "ja", "JP")
    make("ui_ja.ttf", serif_cjk, "ja", "JP")
    make("plain_ja.ttf", sans_cjk, "ja", "JP")
