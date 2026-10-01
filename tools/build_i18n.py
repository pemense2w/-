#!/usr/bin/env python3
"""Merge tools/i18n/<lang>_*.py (each defines S = {...}) into assets/i18n/<lang>.json and report gaps.
   Also scans GDScript and Blender scene files for keys that are used but never defined (English)."""
import glob, importlib.util, json, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
LANGS = ["en", "zh", "ja"]
tables = {}
for lang in LANGS:
    t = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "tools", "i18n", f"{lang}_*.py"))):
        spec = importlib.util.spec_from_file_location("m", f)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
        for k, v in m.S.items():
            if k in t: print(f"duplicate key {k} in {f}")
            t[k] = v
    tables[lang] = t
    os.makedirs(os.path.join(ROOT, "assets", "i18n"), exist_ok=True)
    json.dump(t, open(os.path.join(ROOT, "assets", "i18n", f"{lang}.json"), "w"), ensure_ascii=False, indent=0, sort_keys=True)
en = tables["en"]
print({l: len(t) for l, t in tables.items()})
# notebook entries referenced by json
nb = json.load(open(os.path.join(ROOT, "assets", "data", "notebook.json"))) if os.path.exists(os.path.join(ROOT, "assets", "data", "notebook.json")) else []
used = set()
for e in nb:
    used.add(e["title"]); used.add(e["text"])
    if e.get("alt"): used.add(e["alt"]["key"])
# keys used in code
pat = re.compile(r'''(?:G\.say|G\.sfx_cap|L\.t|L\.has_key|L\.pick|say)\(\s*"([^"%]+)"''')
for f in glob.glob(os.path.join(ROOT, "game", "**", "*.gd"), recursive=True):
    src = open(f).read()
    for k in pat.findall(src): used.add(k)
    for k in re.findall(r'"(c\d\.[a-z0-9_.]+)"', src): used.add(k)
# world text keys in blender scenes
for f in glob.glob(os.path.join(ROOT, "art", "blender", "*.py")):
    for k in re.findall(r'v\.text\([^,]+,\s*"([^"]+)"', open(f).read()): used.add(k)
missing = sorted(k for k in used if k not in en and not any(f"{k}.{n}" in en for n in range(1, 3)) and not k.endswith(".") and not k.endswith("_"))
if missing:
    print("MISSING in en:", len(missing))
    for k in missing: print("  ", k)
for lang in LANGS[1:]:
    gaps = sorted(set(en) - set(tables[lang]))
    print(f"{lang}: {len(gaps)} keys not yet translated")
    if gaps and "--verbose" in sys.argv:
        for k in gaps: print("  ", k)
