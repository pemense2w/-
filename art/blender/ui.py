"""UI art: glyph sprites, Pell's portrait, the title picture."""
import math
from pc import *
from reg import view
from kit import *

CH = "ui"

@view("ui_glyphs", CH)
def ui_glyphs():
    v = View("ui_glyphs", CH, size=(1200, 400), kind="sheet", has_bg=False)
    for i, nm in enumerate(GLYPHS):
        with v.sprite("glyph_" + nm, pad=6):
            v.layer(1)
            draw_glyph(v, nm, 100 + i * 200, 200, 150, color="#efe5c6", dark="#241a12", d=1)
    return v

@view("ui_icons", CH)
def ui_icons():
    v = View("ui_icons", CH, size=(1000, 500), kind="sheet", has_bg=False)
    with v.sprite("pell_big", pad=8, shadow=True):
        v.layer(1)
        pell_fish(v, 260, 250, 1.5, facing=1)
    return v

@view("ui_title", CH)
def ui_title():
    v = View("ui_title", CH, kind="title")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#0d1c27", grad="#2b5460")
    # stars
    rnd = random.Random(7)
    for _ in range(60):
        v.ink(ellipse(rnd.random() * 1600, rnd.random() * 520, 1.5 + rnd.random() * 2, 1.5 + rnd.random() * 2), "#cfd9cc")
    v.layer(1)
    v.add(ellipse(430, 250, 120), "#dfe5d2")
    v.ink(ellipse(392, 268, 26, 22), "#cbd4bd"); v.ink(ellipse(470, 210, 34, 30), "#cbd4bd"); v.ink(ellipse(455, 300, 18, 15), "#cbd4bd")
    # far shore + lighthouse (right), unlit
    v.layer(1)
    v.add(poly([(900, 560), (1100, 520), (1300, 540), (1600, 500), (1600, 580), (900, 580)]), "#0b161d")
    v.layer(2)
    lx = 1230
    v.add(poly([(lx - 34, 548), (lx - 18, 300), (lx + 18, 300), (lx + 34, 548)]), "#0b161d")
    v.add(rect(lx - 26, 268, 52, 32), "#0b161d")
    v.add(poly([(lx - 34, 268), (lx, 232), (lx + 34, 268)]), "#0b161d")
    v.add(rect(lx - 44, 296, 88, 10), "#0b161d")
    v.ink(rect(lx - 12, 272, 24, 22), "#1c3a46")
    # still lake
    v.layer(1)
    v.rect(0, 560, 1600, 440, "#183846", grad="#07151c")
    for i in range(10):
        v.ink(rect(120 + (i * 173) % 1400, 600 + i * 38, 160 + (i % 3) * 60, 4), "#2d5a68")
    v.ink(poly([(lx - 20, 584), (lx + 20, 584), (lx + 44, 760), (lx - 44, 760)]), "#10262f")
    v.ink(rect(380, 680, 100, 5), "#335a62")
    # a small boat with a lantern (left, near)
    v.layer(3)
    v.add(poly([(220, 820), (580, 820), (520, 880), (290, 880)]), "#3b281d")
    v.ink(rect(250, 826, 300, 6), "#5a3d2c")
    v.add(rect(398, 700, 6, 120), "#1d1713")
    v.add(arc(401, 706, 40, 180, 360, 6), "#1d1713")
    v.layer(4)
    lantern(v, 401, 820, 0.9, lit=True)
    # moths in the light
    for (mx, my, s_) in ((330, 650, 0.9), (470, 690, 0.7), (380, 600, 0.6), (520, 620, 0.8)):
        v.layer(5)
        moth(v, mx, my, s_, glow=0.5)
    v.light(401, 760, 520, "#ffb860", intensity=0.9, flicker=0.05)
    v.dark = "0.0"
    return v
