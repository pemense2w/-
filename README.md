# Still Water

A one-hour narrative point-and-click puzzle game about Ruth Halloran, keeper of a lighthouse on a lake that will not move.

* **Engine:** Godot 4.3 (GL Compatibility renderer, GDScript, no editor-built scenes: the UI is built in code).
* **Art:** flat cut-paper scenes modelled and rendered in **Blender** (driven from Python with `bpy`), exported to WebP sprites plus JSON for hotspots, lights and text.
* **Audio:** generated procedurally by `tools/synth_audio.py` (no voice; ambience, SFX and a music-box theme).
* **Languages:** English, Simplified Chinese (简体中文), Japanese (日本語).

Five chapters (The Keeper's Room, The Boathouse, The Crossing, The Far Light, Still Water), 41 main puzzles, ten photograph fragments, five shadow-play memories and three endings. Pell the goldfish gives three-tier hints; the keeper's notebook records what you have seen.

## Play it

1. Install [Godot 4.3](https://godotengine.org/download).
2. Open this folder as a project (`project.godot`) and press **F5**, or from a terminal: `godot --path .`

Controls: click or tap to look and use; click an item in the satchel to hold it, click it again to inspect it, drop one item on another to combine; arrows (or A/D, swipe) turn; the bottom bar has the notebook, Pell and the menu. Esc pauses.

Accessibility options (Menu → Settings): text size, plainer interface font, reduce motion, startle toggle, no timed sequences, purist mode (no notebook), sound captions.

## Regenerating the art

The checked-in `assets/art` is rendered from the Blender scripts in `art/blender/`. To rebuild it you need Blender's Python module and a few libraries:

```sh
python3 -m venv venv && venv/bin/pip install bpy shapely numpy scipy pillow
venv/bin/python art/blender/build.py --draft          # fast 800x500 upscaled preview
venv/bin/python art/blender/build.py --force          # final quality (about an hour on 4 cores)
venv/bin/python art/blender/build.py --only c1_n,c1_e  # just some views
godot --headless --path . --import                    # let Godot pick up the new images
```

Renders are cached by a signature of each view's code (`art/.cache.json`), so only changed views are re-rendered. `build.py --list` prints every view id.

Other generated assets:

| What | Command |
| --- | --- |
| Audio (`assets/audio`) | `python3 tools/synth_audio.py` (needs numpy, scipy, soundfile) |
| String tables (`assets/i18n/*.json`) | `python3 tools/build_i18n.py` (merges `tools/i18n/<lang>_<part>.py`; add `--verbose` to list untranslated keys) |
| Translation sanity check | `python3 tools/check_i18n.py` (same keys, placeholders and line breaks in every language) |
| Fonts (`assets/fonts`) | `python3 tools/make_fonts.py` (subsets EB Garamond, Liberation Sans and Noto CJK to the glyphs the strings use; needs `fonttools`) |

## Tests

```sh
tools/check.sh          # loads every script, reports parse errors
tests/run_all.sh        # headless playthroughs of all five chapters, the shadow plays, save/load, settings, hints, localisation completeness
```

Single test: `SW_TEST=1 SW_SAVE_DIR=/tmp/sw godot --headless --path . -s tests/test_ch3.gd`.
`SW_TEST=1` turns off waiting and tweens and skips the title; `SW_SAVE_DIR` keeps the test's saves out of your real profile.

Screenshots in the real renderer (needs a display, or `xvfb-run`): `SW_TEST=1 xvfb-run -a godot --path . -s tests/shots_ch1.gd` (also `shots_ch2..4`, `shots_stage`, `shots_loc`). Images land in `tests/out/`.

## Exporting

`export_presets.cfg` has **Web** and **Linux** presets. Install the Godot 4.3 export templates (Editor → Manage Export Templates), then:

```sh
godot --headless --path . --export-release Web export/web/index.html
godot --headless --path . --export-release Linux export/linux/still_water.x86_64
```

The art is sized for a web download (a few tens of MB). Serve the Web build over HTTPS or localhost.

## Project layout

```
game/
  autoload/     G (state, saves, hints, flags), L (strings), Snd (audio)
  chapters/     one script per chapter: puzzle logic, hotspot handlers, hint table, carried items
  core/         view renderer, hotspots, lighting, notebook, inspect panel, title, album, stage player (shadow plays), fonts, UI helpers
  widgets/      puzzle widgets: clock, dials, books, tiles, catch, gears, rowing, compass, rhythm, moor, valves, beam, punch
  fx/           grain, vignette, additive/multiplicative light, ripple shaders
assets/
  art/          rendered backgrounds, sprites and item icons (WebP)
  data/         views.json, items.json, notebook.json (hotspots, lights, texts, widgets, sprites: written by the Blender build)
  audio/        sfx / amb / music (OGG)
  i18n/         en.json, zh.json, ja.json
  fonts/        subset fonts per language
art/blender/    paper-cut library (pc.py) and one module per chapter, plus items, UI and memory art
tools/          audio synthesiser, string-table build and check, font subsetter, load check
tests/          headless playthroughs and screenshot scripts
```

### How scenes work

Every view is data: a background (with variants for lamp/day/era), sprites with optional effects, hotspots with conditions, lights, and widgets. Conditions are Godot `Expression` strings evaluated against `G`, with helpers `f()` (flag), `fi()` (counter), `has()` (item), `era()` (Then/Now), `near()`, `here()`. Chapter scripts only implement what happens when something is used, combined or solved.

Chapter 5 reuses the Chapter 1 room twice, once Above and once Below the mirror: the Below room is the same builders seen through a mirrored wrapper.

### Adding text or a language

Strings live in `tools/i18n/<lang>_<part>.py` as `S = {key: text}`. Add the key to `en_*.py`, run `python3 tools/build_i18n.py`: it lists keys the code uses that English lacks, and keys other languages still need. Missing translations fall back to English. To add a language: add it to `L.LANGS`/`L.NAMES` in `game/autoload/i18n.gd`, add `<lang>_*.py` files, add fonts in `tools/make_fonts.py`.
