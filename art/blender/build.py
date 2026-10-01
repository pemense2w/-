#!/usr/bin/env python3
"""
Build all Still Water art with Blender (bpy) and export view JSON for Godot.

  /opt/tools/venv/bin/python art/blender/build.py [--chapter c1] [--only c1_n,c1_e]
                                                   [--draft] [--force] [--list] [--samples 10]

Outputs  assets/art/<chapter>/*.webp   and   assets/data/views.json (merged from _views/*.json)
"""
import os, sys, json, glob, argparse, time, importlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pc, reg

MODULES = ["ch1", "ch2", "ch3", "ch4", "ch5", "ui", "items"]

def load_modules():
    for m in MODULES:
        if os.path.exists(os.path.join(HERE, m + ".py")):
            importlib.import_module(m)

def merge_json():
    views = {}
    for f in sorted(glob.glob(os.path.join(pc.OUT_DATA, "_views", "*.json"))):
        d = json.load(open(f))
        views[d["id"]] = d
    # item icons -> items.json
    items = {}
    for vid, d in views.items():
        if vid.startswith("item_") and d["sprites"]:
            m = d["meta"]
            e = {"tex": d["sprites"][0]["tex"]}
            if m.get("light"): e["light"] = m["light"]
            items[m["item"]] = e
    items = json.load(open(os.path.join(pc.OUT_DATA, "items_extra.json"))) | items if os.path.exists(os.path.join(pc.OUT_DATA, "items_extra.json")) else items
    json.dump(items, open(os.path.join(pc.OUT_DATA, "items.json"), "w"), separators=(",", ":"))
    json.dump({k: v for k, v in views.items() if not k.startswith("item_")}, open(os.path.join(pc.OUT_DATA, "views.json"), "w"), separators=(",", ":"))
    return len(views)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter"); ap.add_argument("--only"); ap.add_argument("--draft", action="store_true")
    ap.add_argument("--force", action="store_true"); ap.add_argument("--list", action="store_true")
    ap.add_argument("--samples", type=int, default=10); ap.add_argument("--merge-only", action="store_true")
    ap.add_argument("--sprite", help="only (re)render this sprite id (with --only view)")
    a = ap.parse_args()
    load_modules()
    ids = list(reg.ORDER)
    if a.chapter:
        ids = [i for i in ids if reg.VIEWS[i][0] == a.chapter]
    if a.only:
        want = a.only.split(",")
        ids = [i for i in ids if i in want or any(i.startswith(w.rstrip("*")) for w in want if w.endswith("*"))]
    if a.list:
        for i in ids: print(i)
        return
    if a.merge_only:
        print("views:", merge_json()); return
    t0 = time.time()
    for n, i in enumerate(ids):
        ch, fn = reg.VIEWS[i]
        t = time.time()
        v = fn()
        pc.render_view(v, draft=a.draft, samples=a.samples, force=a.force, only=([a.sprite] if a.sprite else None))
        print(f"[{n + 1}/{len(ids)}] {i}  {time.time() - t:.1f}s", flush=True)
    print("views in views.json:", merge_json(), f"  total {time.time() - t0:.0f}s")

if __name__ == "__main__":
    main()
