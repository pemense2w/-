#!/usr/bin/env python3
"""Verify zh/ja tables mirror en: same keys, same {n} placeholders, same newline counts."""
import json, re, sys
root = __file__.rsplit("/tools/", 1)[0]
d = {l: json.load(open(f"{root}/assets/i18n/{l}.json", encoding="utf-8")) for l in ("en", "zh", "ja")}
bad = 0
for l in ("zh", "ja"):
    for k, v in d["en"].items():
        t = d[l].get(k)
        if t is None:
            print(l, "missing", k); bad += 1; continue
        if sorted(re.findall(r"\{\d+\}", v)) != sorted(re.findall(r"\{\d+\}", t)):
            print(l, "placeholder mismatch", k); bad += 1
        if v.count("\n") != t.count("\n"):
            print(l, "newline mismatch", k, v.count("\n"), t.count("\n")); bad += 1
    for k in d[l]:
        if k not in d["en"]:
            print(l, "extra", k); bad += 1
print("i18n check:", "OK" if not bad else f"{bad} problems")
sys.exit(1 if bad else 0)
