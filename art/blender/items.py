"""Item icons (384x384, drawn centred) - one View per item, exported to items.json by build.py."""
import math
from pc import *
from reg import view
from kit import *

CH = "items"
ITEM_BUILDERS = {}

def item(id, light=None):
    def deco(fn):
        def build():
            v = View("item_" + id, CH, size=(384, 384), kind="item", has_bg=False, meta={"item": id, "light": light})
            with v.sprite("icon", pad=400):
                fn(v)
            return v
        from reg import VIEWS, ORDER
        VIEWS["item_" + id] = (CH, build)
        ORDER.append("item_" + id)
        return fn
    return deco

C = 192  # centre

@item("key")
def _key(v):
    v.layer(1)
    key(v, C - 30, C + 6, 2.6, ang=-35)

@item("food")
def _food(v):
    v.layer(1)
    v.add(rect(112, 150, 160, 190, 16), "#3e6a74")
    v.add(rect(102, 128, 180, 36, 10), "#c9a24d")
    v.add(rect(132, 190, 120, 100, 8), "#e8dec2")
    v.ink(ellipse(190, 244, 26, 17), GOLDFISH)
    v.ink(poly([(210, 244), (236, 226), (236, 262)]), GOLDFISH)

@item("note")
def _note(v):
    v.layer(1)
    paper_sheet(v, 100, 70, 190, 250, "#e6dcbc", ang=-5, d=1, lines=6)

@item("match")
def _match(v):
    v.layer(1)
    v.add(line([(120, 290), (270, 110)], 14), "#d9c08a")
    v.add(ellipse(276, 100, 20, 20), "#a33a30")
    v.ink(ellipse(271, 94, 8, 8), "#d8584a")

@item("candle_lit", light="#ffb050")
def _candle(v):
    v.layer(1)
    candle_stub(v, C, 330, 2.2)
    flame(v, C, 150, 1.8)

@item("oil")
def _oil(v):
    v.layer(1)
    v.add(rect(112, 150, 160, 180, 22), "#7a8a52")
    v.add(rect(166, 100, 54, 60, 8), "#7a8a52")
    v.add(rect(170, 86, 46, 20, 6), "#3b281d")
    v.ink(rect(128, 200, 128, 80, 8), "#e8dec2")
    v.ink(ellipse(192, 240, 22, 22), "#c0a038")

@item("lantern")
def _lantern(v):
    v.layer(1)
    lantern(v, C, 340, 2.4)

@item("lantern_oil")
def _lantern_oil(v):
    v.layer(1)
    lantern(v, C, 340, 2.4, oil=True)

@item("lantern_lit", light="#ffb860")
def _lantern_lit(v):
    v.layer(1)
    lantern(v, C, 340, 2.4, lit=True)

@item("chart")
def _chart(v):
    v.layer(1)
    paper_sheet(v, 70, 70, 250, 250, "#e1d6b4", ang=-3, d=1)
    for i in range(1, 5):
        v.ink(line([(100 + i * 44, 110), (100 + i * 44, 300)], 3), "#5b4a35")
        v.ink(line([(100, 110 + i * 38), (300, 110 + i * 38)], 3), "#5b4a35")
    v.ink(poly([(105, 290), (150, 262), (200, 270), (230, 220), (295, 232), (295, 296), (105, 296)]), "#8fa59a")
    v.ink(ring(240, 160, 26, 19), "#a33a30")

@item("oar")
def _oar(v):
    v.layer(1)
    v.add(rot(rect(180, 40, 24, 300, 8), 35), "#8a6a46")
    v.add(rot(rect(140, 200, 100, 140, 40), 35, origin=(190, 190)), "#a68359")

@item("ticket")
def _ticket(v):
    v.layer(1)
    paper_sheet(v, 70, 130, 250, 130, "#d9c8a0", ang=8, d=1)
    v.ink(rot(rect(94, 160, 100, 12), 8, origin=(195, 195)), "#7a2a22")
    v.ink(rot(rect(94, 190, 200, 8), 8, origin=(195, 195)), INK)
    v.ink(rot(rect(94, 214, 150, 8), 8, origin=(195, 195)), INK)
