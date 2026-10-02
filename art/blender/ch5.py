"""Chapter 5 - Still Water.  The Keeper's Room from Chapter 1, twice:
   Above: dusty and familiar.   Below: its reflection under the lake - mirrored, aqueous, lit from above by the far light.
The room geometry is not redrawn: the Chapter 1 scene builders are run through a mirroring / recolouring wrapper, so every
puzzle really does reuse something from Chapter 1, turned inside out."""
import math
from contextlib import contextmanager
from pc import *
from reg import view
from kit import *
import ch1

CH = "c5"

def _gray(c):
    return sum(c) / 3.0

def dust(c):
    c = col(c)
    g = _gray(c)
    c = tuple(v * 0.62 + g * 0.38 for v in c)
    c = tuple(v * 0.80 + o * 0.20 for v, o in zip(c, hex2rgb("#b9b39f")))
    return tuple(min(1.0, v + 0.04) for v in c)

def aqua(c):
    c = col(c)
    g = _gray(c)
    c = tuple(v * 0.55 + g * 0.45 for v in c)
    c = tuple(v * 0.48 + o * 0.52 for v, o in zip(c, hex2rgb("#2f8a82")))
    return tuple(min(1.0, v * 1.04 + 0.03) for v in c)

class V5(View):
    def __init__(self, *a, mirror=False, cmap=None, **kw):
        super().__init__(*a, **kw)
        self.mirror = mirror
        self.cmap = cmap

    def _xf(self, geom, color, grad):
        if self.mirror:
            geom = affinity.scale(geom, -1, 1, origin=(800, 0))
        if self.cmap:
            color = self.cmap(col(color))
            grad = self.cmap(col(grad)) if grad else grad
        return geom, color, grad

    def mx(self, x, w=0):
        return 1600 - x - w if self.mirror else x

    def hotm(self, id, rect_, **kw):
        x, y, w, h = rect_
        self.hot(id, (self.mx(x, w), y, w, h), **kw)

    def lightm(self, x, y, r, *a, **kw):
        self.light(self.mx(x), y, r, *a, **kw)

    def textm(self, id, key, rect_, **kw):
        x, y, w, h = rect_
        self.text(id, key, (self.mx(x, w), y, w, h), **kw)

    @contextmanager
    def sprite(self, id, show=None, pivot=None, **kw):
        if pivot is not None and self.mirror:
            pivot = (1600 - pivot[0], pivot[1])
        with View.sprite(self, id, show=show, pivot=pivot, **kw):
            yield self

def derive(fn, new_id, mirror, cmap, nav=None, dark="0.22", ambient="#3a4d5c"):
    """run a Chapter 1 scene builder through the wrapper; keep only its background picture"""
    orig = ch1.new

    def fake_new(id, **kw):
        v = V5(new_id, CH, mirror=mirror, cmap=cmap)
        return v
    ch1.new = fake_new
    try:
        v = fn()
    finally:
        ch1.new = orig
    v.shapes = [s for s in v.shapes if s.group == "bg"]
    v.sprites, v.hotspots, v.lights, v.texts, v.widgets, v.refs = {}, [], [], [], [], []
    v.nav = {"back": None, "left": None, "right": None}
    if nav:
        v.nav.update(nav)
    v.dark = dark
    v.ambient = ambient
    return v

def above(fn, new_id, nav=None):
    return derive(fn, new_id, False, dust, nav, dark="pick(f('clock5_done'), 0.2, 0.24)", ambient="#47545e")

def below(fn, new_id, nav=None, mirror=True):
    v = derive(fn, new_id, mirror, aqua, nav, dark="0.12", ambient="#2f6a6c")
    # a shaft of light falling from the far light above, and caustics on the walls
    v.layer(1)
    for k in range(6):
        v.ink(wave(0, 1600, 150 + k * 110, 22, 260 + k * 40, 5, phase=k * 1.3), "#8fe0d2")
    v.lightm(800, -80, 1500, "#aef2e6", intensity=0.55, hole=0.45)
    return v

# --------------------------------------------------------------------------- walls
def ring_nav(a, left, right):
    return dict(left=left, right=right)

def clock_hands_e(v, prefix_fx):
    with v.sprite("hand_h", pivot=(520, 366), shadow=False, fx=prefix_fx[0]):
        v.layer(7); v.add(hand_shape(520, 366, 38, 7), INK)
    with v.sprite("hand_m", pivot=(520, 366), shadow=False, fx=prefix_fx[1]):
        v.layer(7); v.add(hand_shape(520, 366, 54, 5), INK)

@view("c5_a_n", CH)
def c5_a_n():
    v = above(ch1.c1_n, "c5_a_n", dict(left="c5_a_w", right="c5_a_e"))
    with v.sprite("far_light5", shadow=False, fx="pulse"):
        v.layer(4)
        v.add(ellipse(800, 283, 9, 9), FLAME, glow=4, ink=True)
        v.add(rect(796, 266, 8, 22), FLAME_HOT, glow=3, ink=True)
    v.light(800, 280, 520, "#ffd890", intensity=0.5, flicker=0.05)
    v.hot("window", (590, 130, 420, 410)); v.hot("desk", (320, 650, 960, 58)); v.hot("barometer", (1196, 216, 168, 168))
    v.hot("sill", (505, 560, 590, 50)); v.hot("drawer", (630, 735, 340, 150))
    return v

@view("c5_a_e", CH)
def c5_a_e():
    v = above(ch1.c1_e, "c5_a_e", dict(left="c5_a_n", right="c5_a_s"))
    clock_hands_e(v, ("hand_h", "hand_m"))
    with v.sprite("armchair_front", show="f('ticket_valid')", fx=None):
        v.layer(6)
        # the armchair has turned to face the room
        v.rect(1250, 540, 330, 430, "#b9b39f") if False else None
        v.add(rect(1262, 560, 306, 400, 30), dust("#5b1d29"))
        v.add(rect(1236, 700, 70, 260, 22), dust("#6c2431")); v.add(rect(1524, 700, 70, 260, 22), dust("#6c2431"))
        v.add(rect(1290, 790, 250, 160, 18), dust("#7a2938"))
        v.ink(rect(1310, 810, 210, 6), dust("#8e3446"), d=6)
        for i in range(3):
            v.ink(ellipse(1340 + i * 70, 640, 8, 8), dust(BRASS_D), d=6)
    with v.sprite("moth5", show="f('ticket_valid')", fx="bob", shadow=False):
        v.layer(8)
        moth(v, 1415, 770, 1.1, glow=1.0)
    v.light(1415, 770, 420, "#ffe0a0", when="f('ticket_valid')", intensity=0.8, flicker=0.06)
    v.hot("grate", (560, 600, 480, 340)); v.hot("armchair", (1264, 540, 320, 430)); v.hot("coal", (200, 800, 140, 150))
    v.hot("vase", (810, 330, 90, 150)); v.hot("painting", (700, 120, 480, 320)); v.hot("clock", (420, 270, 200, 206))
    v.hot("candle", (1040, 340, 100, 140))
    return v

@view("c5_a_s", CH)
def c5_a_s():
    v = above(ch1.c1_s, "c5_a_s", dict(left="c5_a_e", right="c5_a_w"))
    v.hot("mirror", (1280, 190, 220, 340)); v.hot("door", (584, 94, 432, 856)); v.hot("coat", (230, 150, 230, 550))
    v.hot("oar_stand", (1110, 840, 120, 120)); v.hot("mat", (580, 940, 440, 52))
    v.text("mat", "world.return", (600, 944, 400, 44), size=28, color="#d9c9a0", font="world", spacing=6)
    return v

@view("c5_a_w", CH)
def c5_a_w():
    v = above(ch1.c1_w, "c5_a_w", dict(left="c5_a_s", right="c5_a_n"))
    v.text("plaque", "world.plaque", (1160, 352, 300, 56), size=20, color="#d9c9a0", font="world", spacing=1)
    v.hot("shelf", (560, 120, 480, 520)); v.hot("cabinet", (560, 642, 480, 300)); v.hot("bowl_w", (200, 530, 220, 140))
    v.hot("plaque", (1160, 220, 300, 190)); v.hot("photo", (180, 180, 170, 220)); v.hot("table", (180, 640, 250, 300))
    return v

def below_walls(fn, new_id, nav):
    return below(fn, new_id, nav)

@view("c5_b_n", CH)
def c5_b_n():
    v = below(ch1.c1_n, "c5_b_n", dict(left="c5_b_e", right="c5_b_w"))
    v.hotm("window", (590, 130, 420, 410)); v.hotm("desk", (320, 650, 960, 58)); v.hotm("barometer", (1196, 216, 168, 168))
    v.hotm("drawer", (630, 735, 340, 150))
    return v

@view("c5_b_e", CH)
def c5_b_e():
    v = below(ch1.c1_e, "c5_b_e", dict(left="c5_b_s", right="c5_b_n"))
    with v.sprite("hand_h", pivot=(520, 366), shadow=False, fx="bhand_h"):
        v.layer(7); v.add(hand_shape(520, 366, 38, 7), INK)
    with v.sprite("hand_m", pivot=(520, 366), shadow=False, fx="bhand_m"):
        v.layer(7); v.add(hand_shape(520, 366, 54, 5), INK)
    v.hotm("grate", (560, 600, 480, 340)); v.hotm("armchair", (1264, 540, 320, 430)); v.hotm("coal", (200, 800, 140, 150))
    v.hotm("vase", (810, 330, 90, 150)); v.hotm("painting", (700, 120, 480, 320)); v.hotm("clock", (420, 270, 200, 206))
    v.hotm("candle", (1040, 340, 100, 140))
    return v

@view("c5_b_s", CH)
def c5_b_s():
    v = below(ch1.c1_s, "c5_b_s", dict(left="c5_b_w", right="c5_b_e"))
    v.hotm("mirror", (1280, 190, 220, 340)); v.hotm("door", (584, 94, 432, 856)); v.hotm("coat", (230, 150, 230, 550))
    v.hotm("oar_stand", (1110, 840, 120, 120)); v.hotm("mat", (580, 940, 440, 52))
    v.textm("mat", "world.return", (600, 944, 400, 44), size=28, color="#d9c9a0", font="world", spacing=6)
    return v

@view("c5_b_w", CH)
def c5_b_w():
    v = below(ch1.c1_w, "c5_b_w", dict(left="c5_b_n", right="c5_b_s"))
    # the pike's plaque, reflected: it now says something else
    v.textm("plaque", "world.plaque_b", (1160, 352, 300, 56), size=22, color="#d9c9a0", font="world", spacing=2)
    with v.sprite("plaque_gap", show="f('plaque_moved')"):
        v.layer(6)
        v.add(rect(1180, 346, 260, 56, 3), "#0b1a1a")
    with v.sprite("frag9", show="f('plaque_moved') and not f('got_frag9')"):
        v.layer(7)
        v.add(poly([(1250, 360), (1160, 354), (1154, 388), (1244, 394)]), "#cfe0cc")
        v.ink(rect(1180, 366, 44, 16), "#5a6f6a", d=7)
    v.hotm("shelf", (560, 120, 480, 520)); v.hotm("cabinet", (560, 642, 480, 300)); v.hotm("bowl_w", (200, 530, 220, 140))
    v.hotm("plaque", (1160, 220, 300, 190), when="not f('plaque_moved')")
    v.hotm("frag9", (1160, 330, 200, 90), when="f('plaque_moved') and not f('got_frag9')")
    v.hotm("photo", (180, 180, 170, 220)); v.hotm("table", (180, 640, 250, 300))
    return v

# --------------------------------------------------------------------- Above close-ups
@view("c5_a_mirror", CH)
def c5_a_mirror():
    v = derive(ch1.c1_mirror, "c5_a_mirror", False, dust, dict(back="c5_a_s"))
    with v.sprite("refl5", fx="bob"):
        v.layer(6)
        v.add(poly([(740, 900), (760, 520), (800, 480), (840, 520), (860, 900)]), "#9ab7b2", d=6)
        v.add(ellipse(800, 440, 44, 50), "#9ab7b2", d=6)
        v.add(line([(840, 560), (900, 600), (930, 520)], 26), "#9ab7b2", d=6)            # a hand raised to the glass
        v.add(ellipse(934, 506, 24, 28), "#aecbc6", d=6)
        v.ink(arc(800, 440, 44, 190, 350, 6), "#7f9d98", d=6)
    v.hot("glass", (436, 96, 728, 808))
    return v

@view("c5_a_grate", CH)
def c5_a_grate():
    v = derive(ch1.c1_grate, "c5_a_grate", False, dust, dict(back="c5_a_e"))
    v.text("sorry", "world.sorry", (560, 680, 480, 90), size=64, color="#3a2418", font="world", spacing=6)
    with v.sprite("ash_pile", show="not f('got_ash')"):
        v.layer(6)
        v.add(poly([(1120, 880), (1180, 800), (1260, 790), (1320, 880)]), "#9a9490")
        v.ink(ellipse(1220, 830, 40, 18), "#aaa5a1", d=6)
    v.hot("scrap", (540, 620, 540, 190)); v.hot("ash_pile", (1100, 780, 240, 110), when="not f('got_ash')")
    return v

@view("c5_a_clock", CH)
def c5_a_clock():
    v = derive(ch1.c1_clock, "c5_a_clock", False, dust, dict(back="c5_a_e"))
    cx, cy = 800, 380
    with v.sprite("hatch_open5", show="f('clock5_done')"):
        v.layer(5)
        v.rect(690, 690, 220, 120, "#120c09", r=8)
        v.add(poly([(690, 690), (630, 712), (630, 790), (690, 810)]), dust("#6e4b36"))
    with v.sprite("logpage5", show="f('clock5_done') and not f('got_logpage')"):
        v.layer(6)
        paper_sheet(v, 720, 706, 80, 92, "#d9cfae", ang=-6, d=6, lines=3)
    with v.sprite("timetable5", show="f('clock5_done') and not f('got_timetable')"):
        v.layer(6)
        paper_sheet(v, 806, 712, 84, 82, "#cfc4a3", ang=5, d=6, lines=3)
    with v.sprite("hand_h", pivot=(cx, cy), fx="hand_h"):
        v.layer(7); v.add(hand_shape(cx, cy, 160, 26), INK)
    with v.sprite("hand_m", pivot=(cx, cy), fx="hand_m"):
        v.layer(8); v.add(hand_shape(cx, cy, 235, 16), INK)
    v.layer(9); v.add(ellipse(cx, cy, 20, 20), BRASS)
    v.hot("fish_engraving", (cx + 80, cy + 20, 110, 110)); v.hot("hatch", (690, 690, 220, 120))
    v.hot("logpage", (710, 696, 100, 110), when="f('clock5_done') and not f('got_logpage')")
    v.hot("timetable", (800, 700, 100, 100), when="f('clock5_done') and not f('got_timetable')")
    v.hot("clock_face", (cx - 270, cy - 270, 540, 540))
    return v

def book_row(v, slots, filler=True):
    for i, nm in enumerate(["red", "green", "pale", "yellow"]):
        with v.sprite("book_" + nm):
            v.layer(5)
            book(v, slots[i], 190, 140, 366, FLOAT_COLORS[nm], FLOAT_PATTERN[nm], d=5)

@view("c5_a_books", CH)
def c5_a_books():
    v = derive(ch1.c1_books, "c5_a_books", False, dust, dict(back="c5_a_w"))
    slots = [420, 600, 780, 960]
    book_row(v, slots)
    v.widget("books", "books", (400, 170, 720, 400), sprites=["book_red", "book_green", "book_pale", "book_yellow"], slots=slots, key="books5_order", readonly=True)
    v.hot("books_row", (400, 170, 720, 400)); v.hot("cabinet", (160, 620, 1280, 290))
    return v

@view("c5_chair", CH)
def c5_chair():
    v = View("c5_chair", CH)
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#566267", grad="#2e393e")
    v.layer(1)
    v.rect(0, 800, 1600, 200, "#3a302a")
    # the armchair, turned to face you; the last moth rests in its warmth
    v.layer(2)
    v.rect(450, 140, 700, 700, "#5b1d29", r=70)
    v.layer(3)
    v.rect(380, 480, 170, 360, "#6c2431", r=50); v.rect(1050, 480, 170, 360, "#6c2431", r=50)
    v.layer(4)
    v.rect(520, 580, 560, 260, "#7a2938", r=40)
    v.ink(rect(560, 620, 480, 10), "#8e3446", d=4)
    for i in range(4):
        v.add(ellipse(580 + i * 140, 250, 14, 14), BRASS_D, d=4, ink=True)
    v.add(rect(430, 840, 40, 50), "#3b281d"); v.add(rect(1130, 840, 40, 50), "#3b281d")
    with v.sprite("moth_last", fx="bob", shadow=False):
        v.layer(6)
        moth(v, 800, 560, 2.2, glow=1.4)
    v.light(800, 560, 640, "#ffe0a0", intensity=0.9, flicker=0.06)
    v.dark = "0.35"
    v.ambient = "#3a4d5c"
    v.nav["back"] = "c5_a_e"
    v.hot("moth5", (620, 380, 360, 360))
    v.hot("chair_seat", (450, 140, 700, 700))
    return v

# --------------------------------------------------------------------- Below close-ups
@view("c5_b_mirror", CH)
def c5_b_mirror():
    v = derive(ch1.c1_mirror, "c5_b_mirror", True, aqua, dict(back="c5_b_s"), dark="0.1", ambient="#2f6a6c")
    with v.sprite("refl5b", fx="bob"):
        v.layer(6)
        v.add(poly([(740, 900), (760, 520), (800, 480), (840, 520), (860, 900)]), "#a9d6cc", d=6)
        v.add(ellipse(800, 440, 44, 50), "#a9d6cc", d=6)
        v.add(line([(840, 560), (900, 600), (930, 520)], 26), "#a9d6cc", d=6)
        v.add(ellipse(934, 506, 24, 28), "#bfe6dc", d=6)
    v.hot("glass_b", (436, 96, 728, 808))
    return v

@view("c5_b_clock", CH)
def c5_b_clock():
    # the face is drawn the right way round: only its mechanism is mirrored
    v = derive(ch1.c1_clock, "c5_b_clock", False, aqua, dict(back="c5_b_e"), dark="0.1", ambient="#2f6a6c")
    cx, cy = 800, 380
    with v.sprite("hand_h", pivot=(cx, cy), fx="bhand_h"):
        v.layer(7); v.add(hand_shape(cx, cy, 160, 26), INK)
    with v.sprite("hand_m", pivot=(cx, cy), fx="bhand_m"):
        v.layer(8); v.add(hand_shape(cx, cy, 235, 16), INK)
    v.layer(9); v.add(ellipse(cx, cy, 20, 20), BRASS)
    v.widget("clock", "clock", (cx - 270, cy - 270, 540, 540), cx=cx, cy=cy, knob_h=[620, 880], knob_m=[980, 880], step_m=5, prefix="mclock", lock_flag="clock5_done")
    v.hot("fish_engraving", (cx + 80, cy + 20, 110, 110)); v.hot("hatch", (690, 690, 220, 120))
    return v

@view("c5_b_grate", CH)
def c5_b_grate():
    v = derive(ch1.c1_grate, "c5_b_grate", True, aqua, dict(back="c5_b_e"), dark="0.1", ambient="#2f6a6c")
    # the scrap that survived Above is not here: only a clean hearth
    v.layer(6)
    v.add(poly([(260, 880), (420, 760), (800, 720), (1180, 760), (1340, 880)]), aqua("#3b3737"))
    v.add(poly([(420, 860), (600, 790), (800, 780), (1000, 790), (1180, 860)]), aqua("#4b4645"))
    v.add(rect(520, 600, 600, 200), aqua("#2b2728"))
    v.layer(7)
    for i in range(8):
        v.add(rect(230 + i * 160, 560, 24, 330, 6), aqua("#1d1d1f"))
    v.add(rect(200, 580, 1200, 22, 6), aqua("#1d1d1f")); v.add(rect(200, 840, 1200, 22, 6), aqua("#1d1d1f"))
    with v.sprite("ash_in", show="f('ash_placed')"):
        v.layer(8)
        v.add(poly([(560, 790), (680, 730), (940, 726), (1060, 790)]), "#7e8a86")
    with v.sprite("flames_back", show="f('backfire') and not f('letter_done')", fx="flicker", shadow=False):
        v.layer(9)
        for k in range(5):
            flame(v, 640 + k * 95, 760 - (k % 2) * 30, 1.8, d=9)
    with v.sprite("letter_whole", show="f('letter_done') and not f('got_letter')"):
        v.layer(9)
        paper_sheet(v, 640, 640, 320, 210, "#e8e0c4", ang=-3, d=9, lines=6)
    v.light(800, 760, 520, "#ffb860", when="f('backfire') and not f('letter_done')", intensity=1.0, flicker=0.1)
    v.hot("grate_b", (200, 560, 1200, 340))
    v.hot("letter", (620, 620, 360, 240), when="f('letter_done') and not f('got_letter')")
    return v

@view("c5_b_books", CH)
def c5_b_books():
    v = derive(ch1.c1_books, "c5_b_books", True, aqua, dict(back="c5_b_w"), dark="0.1", ambient="#2f6a6c")
    slots_orig = [420, 600, 780, 960]
    book_row(v, slots_orig)
    mslots = [1600 - x - 140 for x in slots_orig]
    v.widget("books", "mirror_books", (v.mx(400, 720), 170, 720, 400), sprites=["book_red", "book_green", "book_pale", "book_yellow"], slots=mslots, key="books5_order", solved_flag="books5_done", init=[3, 1, 0, 2])
    with v.sprite("cabinet_open5", show="f('books5_done')"):
        v.layer(6)
        v.rect(160, 620, 1280, 290, "#0d0a09", r=6)
    with v.sprite("punch5", show="f('books5_done') and not f('got_punch')"):
        v.layer(8)
        v.add(rect(730, 760, 140, 60, 10), "#3a3d3f"); v.add(rect(790, 700, 20, 70, 6), "#3a3d3f")
        v.add(ellipse(800, 700, 36, 14), "#c9a24d"); v.add(rect(740, 820, 120, 24, 4), "#6e7274")
    v.hot("books_row", (v.mx(400, 720), 170, 720, 400)); v.hot("cabinet", (160, 620, 1280, 290))
    v.hot("punch", (700, 690, 200, 160), when="f('books5_done') and not f('got_punch')")
    return v

@view("c5_b_bowl", CH)
def c5_b_bowl():
    v = derive(ch1.c1_bowl, "c5_b_bowl", True, aqua, dict(back="c5_b_w"), dark="0.1", ambient="#2f6a6c")
    with v.sprite("pell_b", show="f('pell_home')", fx="bob", shadow=False):
        v.layer(6)
        pell_fish(v, 800, 470, 1.8, facing=-1)
    v.hotm("bowl", (420, 150, 760, 640))
    return v

@view("c5_b_photo", CH)
def c5_b_photo():
    v = derive(ch1.c1_photo, "c5_b_photo", True, aqua, dict(back="c5_b_w"), dark="0.1", ambient="#2f6a6c")
    # in the reflection the figure has turned around
    with v.sprite("turned_fig"):
        v.layer(7)
        v.add(poly([(740, 884), (748, 640), (780, 600), (820, 600), (852, 640), (860, 884)]), "#2d3f3e")
        v.add(ellipse(800, 560, 46, 52), "#8fb8ae")
        v.ink(ellipse(784, 556, 7, 5), INK, d=7); v.ink(ellipse(816, 556, 7, 5), INK, d=7)
        v.ink(line([(788, 584), (812, 584)], 4), "#4a6a64", d=7)
    with v.sprite("frag10", show="not f('got_frag10')"):
        v.layer(8)
        v.add(poly([(1010, 800), (1100, 790), (1106, 850), (1018, 860)]), "#cfe0cc")
        v.ink(rect(1030, 812, 50, 26), "#5a6f6a", d=8)
    v.hotm("frag10", (990, 780, 130, 90), when="not f('got_frag10')")
    v.hot("photo_face", (436, 116, 728, 768))
    return v

@view("c5_punch", CH)
def c5_punch():
    v = View("c5_punch", CH)
    v.dark = "0.12"
    v.ambient = "#3a4d5c"
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#2d3f44", grad="#18262a")
    v.layer(1)
    v.rect(260, 150, 1080, 700, "#e0d3ae", grad="#cfc29b", r=18)
    v.layer(2)
    v.rect(290, 180, 1020, 640, "#d4c89f", r=10)
    v.ink(rect(290, 300, 1020, 6), "#7a2a22", d=2)
    v.nav["back"] = "c5_a_e"
    v.widget("punch", "punch", (260, 150, 1080, 700), hours=12, mins=12, flag="ticket_valid", want_h=4, want_m=30)
    v.text("ptitle", "world.ticket_head", (300, 190, 1000, 90), size=48, color="#3a2418", font="world", spacing=4)
    v.text("phours", "world.ticket_hour", (300, 330, 300, 40), size=26, color="#3a2418", font="world", align="left")
    v.text("pmins", "world.ticket_min", (300, 560, 400, 40), size=26, color="#3a2418", font="world", align="left")
    v.hot("ticket_look", (260, 150, 1080, 700))
    return v
