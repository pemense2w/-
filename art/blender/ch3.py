"""Chapter 3 - The Crossing: open water in fog; four views around the boat, and the fifth you were told not to use."""
import math
from pc import *
from reg import view
from kit import *

CH = "c3"
FOG_T, FOG_B = "#7f9a9c", "#2d4a54"
SEA_T, SEA_B = "#1f4350", "#0a1a21"
WOOD_B = "#8a5a36"
IRON = "#3a3d3f"
AMBIENT = "#334756"

def new(id, dark="0.12", **kw):
    v = View(id, CH, **kw)
    v.dark = dark
    v.ambient = AMBIENT
    return v

# ---------------------------------------------------------------- landmark sheet
@view("c3_lm", CH)
def c3_lm():
    """Landmark sprites, drawn once and placed (small & faded when seen through fog, large when alongside)."""
    v = View("c3_lm", CH, size=(1600, 1000), kind="sheet", has_bg=False)
    # four floats (colour + pattern)
    for i, nm in enumerate(["red", "green", "pale", "yellow"]):
        with v.sprite("float_" + nm, pad=10):
            v.layer(2)
            float_buoy(v, 160 + i * 300, 330, 2.0, FLOAT_COLORS[nm], FLOAT_PATTERN[nm], d=2)
    # the drowned tree: bare trunk and branches coming out of the water, a bottle wedged in the fork
    with v.sprite("tree", pad=10):
        v.layer(2)
        v.add(poly([(1330, 340), (1352, 120), (1384, 120), (1410, 340)]), "#2b241f")
        for (a, b) in (((1368, 160), (1250, 60)), ((1368, 190), (1500, 80)), ((1360, 240), (1260, 190)), ((1260, 60), (1200, 20)), ((1500, 80), (1560, 30)), ((1250, 60), (1280, 10))):
            v.add(line([a, b], 14), "#2b241f")
        v.add(ellipse(1368, 345, 90, 14), "#0b1a21", ink=True)
    with v.sprite("bottle_tree", pad=10):
        v.layer(3)
        v.add(union(ellipse(1330, 200, 22, 34), rect(1320, 150, 20, 40, 4)), "#a9c6c6")
        v.ink(rot(rect(1322, 190, 16, 28), 8), "#e6dcc0")
    # bell buoy
    with v.sprite("buoy", pad=10):
        v.layer(2)
        v.add(poly([(140, 880), (170, 760), (230, 760), (260, 880)]), "#b8453a")
        v.ink(rect(150, 800, 100, 18), "#f0e4c8")
        v.add(rect(192, 640, 16, 120), IRON if False else "#3a3d3f")
        v.add(poly([(150, 640), (250, 640), (230, 590), (170, 590)]), "#3a3d3f")
        v.add(union(ellipse(200, 650, 44, 36), rect(156, 640, 88, 20, 4)), BRASS)
        v.add(ellipse(200, 676, 9, 9), BRASS_D)
        v.add(ellipse(200, 885, 80, 12), "#0b1a21", ink=True)
    # reeds, with a bottle caught low among them
    with v.sprite("reeds", pad=10):
        v.layer(2)
        rnd = random.Random(4)
        for k in range(16):
            x0 = 520 + k * 22 + rnd.random() * 8
            h = 150 + rnd.random() * 150
            v.add(line([(x0, 890), (x0 + (rnd.random() - 0.5) * 50, 890 - h)], 8), "#4a6a40")
            v.add(ellipse(x0 + (rnd.random() - 0.5) * 50, 890 - h, 7, 22), "#6a4a30")
        v.add(ellipse(690, 893, 190, 16), "#0b1a21", ink=True)
    with v.sprite("bottle_reeds", pad=10):
        v.layer(3)
        v.add(rot(union(ellipse(700, 850, 30, 46), rect(688, 788, 24, 56, 4)), 70, origin=(700, 850)), "#a9c6c6")
        v.ink(rot(rect(688, 830, 22, 34), 70, origin=(700, 850)), "#e6dcc0")
    # the circled spot: slow rings on the water; the sunken ferry's mast with the heron
    with v.sprite("deep", pad=10):
        v.layer(2)
        for k, r_ in enumerate((190, 140, 90)):
            v.add(ring(1030, 880, r_, r_ - 8), "#2c5260")
            pass
        v.add(ellipse(1030, 880, 60, 10), "#05090c")
    with v.sprite("mast", pad=10):
        v.layer(3)
        v.add(rect(1022, 560, 14, 330), "#3b2c20")
        v.add(rect(960, 600, 140, 12), "#3b2c20")
        v.add(rect(996, 640, 64, 8), "#3b2c20")
    with v.sprite("heron_mast", pad=10):
        v.layer(4)
        heron_silhouette(v, 1030, 600, 0.75, d=4)
    with v.sprite("heron_frag", pad=10):
        v.layer(4)
        heron_silhouette(v, 1030, 600, 0.75, d=4)
        v.add(poly([(1110, 222), (1156, 214), (1162, 240), (1116, 250)]), "#d1c6a4", d=5)
    # the far light's landing: the lighthouse base, a stage, and the post
    with v.sprite("landing", pad=10):
        v.layer(2)
        v.add(poly([(1280, 900), (1300, 600), (1500, 600), (1520, 900)]), "#d9d3b6", grad="#b9b394")
        for k in range(5):
            v.ink(rect(1290 + k * 4, 650 + k * 52, 220 - k * 8, 16), "#7a2f2a")
        v.add(rect(1340, 560, 120, 50, 6), "#2b2018")
        v.add(rect(1360, 500, 80, 70, 4), "#2f4a54")
        v.add(poly([(1340, 500), (1400, 450), (1460, 500)]), "#2b2018")
        v.add(rect(1180, 840, 140, 30, 4), "#6b5543")
    with v.sprite("post", pad=10):
        v.layer(4)
        v.add(rect(1190, 760, 30, 110), "#3a2d24")
        v.add(ellipse(1205, 760, 22, 8), "#4f3e31")
    return v

# ------------------------------------------------------------------ directional views
def sea(v, clear=False, horizon=420):
    v.layer(0)
    if clear:
        v.rect(0, 0, 1600, 1000, "#0f2a36", grad="#3f6670")
        rnd = random.Random(5)
        for _ in range(60):
            v.ink(ellipse(rnd.random() * 1600, rnd.random() * 330, 1.6, 1.6), "#d3dccf")
    else:
        v.rect(0, 0, 1600, 1000, FOG_T, grad=FOG_B)
    v.layer(1)
    v.rect(0, horizon, 1600, 1000 - horizon, SEA_T, grad=SEA_B)
    for i in range(10):
        v.ink(rect(40 + (i * 177) % 1500, horizon + 40 + i * 44, 160 + (i % 3) * 80, 4), "#3d6773")
    if not clear:
        rnd = random.Random(9)
        for k in range(9):
            v.ink(ellipse(rnd.random() * 1600, horizon - 20 + rnd.random() * 90, 200 + rnd.random() * 220, 26 + rnd.random() * 24), "#b4c5c4")
    else:
        for k in range(5):
            v.ink(ellipse(200 + k * 330, horizon + 4, 190, 14), "#2a4a56")

def hull_foreground(v, kind):
    """the boat around you, looking along each side"""
    if kind in ("bow", "stern"):
        # floor planks converging toward the far end, low side-walls, the thwart you sit on
        v.layer(3)
        v.add(poly([(0, 1000), (1600, 1000), (1120, 730), (480, 730)]), WOOD_B, grad="#6a4126")
        for k in range(9):
            v.ink(line([(k * 200, 1000), (480 + k * 80, 730)], 5), "#5a3820")
        v.layer(4)
        v.add(poly([(0, 1000), (0, 700), (440, 640), (480, 730)]), "#7a4e2c")
        v.add(poly([(1600, 1000), (1600, 700), (1160, 640), (1120, 730)]), "#7a4e2c")
        v.ink(line([(0, 700), (440, 640)], 12), "#c9a24d")
        v.ink(line([(1600, 700), (1160, 640)], 12), "#c9a24d")
        v.layer(4)
        v.rect(0, 930, 1600, 70, "#6e4a2c")
        v.ink(rect(0, 934, 1600, 10), "#a8764a")
        v.layer(5)
        v.rect(776, 600, 48, 140, "#4a3326", r=6)                  # bow post / stern post
        if kind == "bow":
            with v.sprite("lamp_dir", show="f('bow_lamp')", fx="flicker"):
                v.layer(6)
                v.add(rect(740, 520, 120, 100, 14), "#c8963f", glow=0.6)
                v.add(rect(752, 532, 96, 76, 8), "#e3b866", glow=0.8)
                flame(v, 800, 604, 1.5, d=6, glow=2.2)
            v.layer(5)
            v.add(rect(730, 510, 140, 16, 4), "#1f2a2b"); v.add(rect(730, 616, 140, 14, 4), "#1f2a2b")
        else:
            v.layer(6)
            v.add(rect(784, 560, 32, 20, 4), IRON)
            v.add(union(ellipse(800, 600, 36, 32), rect(764, 592, 72, 24, 5)), BRASS)
            v.add(ellipse(800, 622, 8, 8), BRASS_D)
    else:
        v.layer(3)
        v.add(poly([(0, 1000), (0, 760), (1600, 700), (1600, 1000)]), WOOD_B, grad="#6a4126")
        v.layer(4)
        v.ink(rect(0, 770, 1600, 14), "#c9a24d")
        for k in range(9):
            v.ink(line([(k * 200, 1000), (k * 200 + 60, 790)], 5), "#5a3820")
        # oar resting in its lock
        v.layer(5)
        sx = 1 if kind == "port" else -1
        v.add(rect(740, 735, 60, 70, 6), IRON); v.add(ring(770, 730, 30, 15), IRON)
        v.add(line([(770, 730), (770 + sx * 640, 700)], 20), "#8a6a46")
        v.add(rot(rect(770 + sx * 560, 660, 200, 70, 30), sx * -6), "#a68359")

def landmark_refs(v, d):
    """near (seen through the fog, small and pale) and here (alongside, large) copies of every landmark"""
    names = [("float_red", "red"), ("float_green", "green"), ("float_pale", "pale"), ("float_yellow", "yellow"),
             ("tree", "tree"), ("buoy", "buoy"), ("reeds", "reeds"), ("deep", "deep"), ("landing", "landing")]
    near_dist = {"red": 0.95, "green": 0.95, "pale": 0.95, "yellow": 0.95, "tree": 1.0, "buoy": 1.0, "reeds": 1.0, "deep": 1.2, "landing": 0.8}
    for sid, key in names:
        sc_near = 0.45 * near_dist[key]
        v.ref(f"{sid}_near", "c3_lm", sid, 800, 560, scale=sc_near, show=f"near('{key}', '{d}') and not here('{key}')", alpha=0.38, tint="#c9d8da")
        v.ref(f"{sid}_here", "c3_lm", sid, 620 if key not in ("landing", "deep") else 560, 760, scale=1.0 if key != "landing" else 0.9, show=f"here('{key}')")
    # tree / reeds bottles ride on top of their parents
    v.ref("bottle_tree_here", "c3_lm", "bottle_tree", 620, 760, scale=1.0, show="here('tree') and not f('got_tomas_note')")
    v.ref("bottle_reeds_here", "c3_lm", "bottle_reeds", 620, 760, scale=1.0, show="here('reeds') and not f('got_frag5')")
    v.ref("mast_here", "c3_lm", "mast", 560, 760, scale=1.0, show="here('deep')")
    v.ref("heron_mast_here", "c3_lm", "heron_mast", 560, 760, scale=1.0, show="here('deep') and not f('got_frag6')", fx="sway")
    v.ref("heron_frag_here", "c3_lm", "heron_frag", 560, 760, scale=1.0, show="here('deep') and f('heron_gave') and not f('got_frag6')", fx="sway")
    v.ref("post_here", "c3_lm", "post", 620, 760, scale=0.9, show="here('landing')")

def dir_hotspots(v, d, nm):
    v.hot("row_" + d, (360, 340, 880, 340))
    v.hot("look_here", (300, 420, 760, 400), when="here_any()")
    v.hot("look_down", (520, 840, 560, 150))
    v.hot("to_deck", (20, 640, 300, 340))
    v.hot("to_chart", (1280, 640, 300, 340))

def direction_view(vid, kind, d, left, right, extra=None):
    def build():
        v = new(vid, left=left, right=right)
        v.variants_when({"clear": "f('fog_lifted')"}, "fog")
        for vn in ("fog", "clear"):
            with v.variant(vn):
                sea(v, clear=(vn == "clear"), horizon=430)
                if extra:
                    extra(v, vn)
        hull_foreground(v, kind)
        landmark_refs(v, d)
        # a bow lamp / lantern throws a little warm light onto the water around you
        v.light(800, 760, 520, "#ffb860", intensity=0.5, flicker=0.05, when="f('bow_lamp')")
        dir_hotspots(v, d, kind)
        if kind == "stern":
            v.hot("boat_bell", (720, 540, 160, 120))
        return v
    return build

def extra_bow(v, vn):
    v.layer(2)
    # the far light, far off: a pinprick that seems to answer your lantern (it is only its reflection)
    v.add(ellipse(800, 400, 6, 6), FLAME, glow=4, ink=True)
    if vn == "clear":
        v.add(poly([(790, 430), (794, 330), (806, 330), (810, 430)]), "#0b161d")
        v.add(rect(790, 316, 20, 14), "#0b161d")

def extra_stern(v, vn):
    v.layer(2)
    # the cottage window you lit in Chapter 1: the one fixed point
    v.add(poly([(0, 438), (500, 430), (900, 436), (1600, 428), (1600, 470), (0, 470)]), "#12242c")
    v.add(rect(1020, 392, 44, 40), FLAME, glow=2.4, ink=True)
    v.ink(rect(1040, 392, 4, 40), "#7a4a20")

view("c3_bow", CH)(direction_view("c3_bow", "bow", "n", "c3_port", "c3_starboard", extra_bow))
view("c3_starboard", CH)(direction_view("c3_starboard", "starboard", "e", "c3_bow", "c3_stern"))
view("c3_stern", CH)(direction_view("c3_stern", "stern", "s", "c3_starboard", "c3_port", extra_stern))
view("c3_port", CH)(direction_view("c3_port", "port", "w", "c3_stern", "c3_bow"))

# ===================================================================== close-ups
def cu(v, top="#26414a", bot="#0f242c"):
    v.layer(0)
    v.rect(0, 0, 1600, 1000, top, grad=bot)

@view("c3_deck", CH)
def c3_deck():
    v = new("c3_deck", dark="0.1", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#6e4a2c", grad="#4a2f1a")
    for k in range(9):
        v.ink(rect(k * 180 + 10, 0, 6, 1000), "#3b2414")
    v.layer(1)
    v.rect(0, 700, 1600, 80, "#8a5a36", r=4)                        # thwart
    v.ink(rect(0, 706, 1600, 10), "#a8764a")
    # the chart spread on the thwart
    v.layer(2)
    paper_sheet(v, 220, 560, 360, 230, "#e1d6b4", ang=-4, d=2)
    for k in range(1, 5):
        v.ink(line([(250 + k * 64, 590), (250 + k * 64, 760)], 2), "#5b4a35", d=2)
        v.ink(line([(250, 590 + k * 34), (560, 590 + k * 34)], 2), "#5b4a35", d=2)
    v.ink(ring(470, 640, 18, 13), "#a33a30", d=2)
    # the compass in its brass bowl
    v.layer(2)
    v.add(ellipse(1180, 650, 130), BRASS_D)
    v.layer(3)
    v.add(ellipse(1180, 650, 112), "#e8dec2")
    v.ink(line([(1180, 560), (1180, 740)], 4), INK, d=3); v.ink(line([(1090, 650), (1270, 650)], 4), INK, d=3)
    v.ink(ellipse(1180, 650, 10, 10), BRASS, d=3)
    # the lantern, Pell's jar, the mooring line
    v.layer(3)
    lantern(v, 800, 700, 1.3, lit=True)
    rope_coil2(v, 520, 880)
    with v.sprite("pell_jar", fx="bob"):
        v.layer(5)
        v.add(jar_shape(940, 470, 160, 220), "#a9c6c6")
        v.ink(jar_shape(950, 484, 140, 192), "#2f6f80")
        v.add(rect(950, 456, 140, 24, 6), "#a8825a")
        pell_fish(v, 1020, 590, 0.55, facing=1)
    v.light(800, 600, 700, "#ffb860", intensity=0.8, flicker=0.05)
    v.hot("chart_table", (200, 540, 400, 270))
    v.hot("compass", (1050, 520, 260, 260))
    v.hot("pell", (930, 440, 180, 260))
    v.hot("lantern_deck", (690, 480, 220, 240))
    v.hot("line_coil", (440, 800, 180, 160))
    return v

def rope_coil2(v, cx, cy, r=70):
    v.layer(3)
    for k in range(4):
        v.add(ring(cx, cy, r - k * 14, r - k * 14 - 10), "#b79c68")

@view("c3_chart", CH)
def c3_chart():
    v = new("c3_chart", dark="0.06", back="c3_deck")
    cu(v, "#3a2c20", "#2a1d14")
    v.layer(1)
    v.rect(140, 40, 1320, 920, "#e1d6b4", grad="#cfc29b", r=10)
    # the coast: low land in the bottom-left corner, like the chart in the cottage
    v.layer(2)
    v.add(poly([(140, 620), (360, 560), (520, 600), (600, 760), (560, 960), (140, 960)]), "#8fa59a", grad="#7a9086")
    v.add(poly([(140, 700), (300, 660), (420, 720), (480, 860), (140, 900)]), "#a9bdb2")
    v.text("warn", "world.chart_warn", (880, 70, 540, 50), size=26, color="#7a2a22", font="world", spacing=3)
    v.text("stern", "world.chart_stern", (170, 70, 540, 50), size=26, color="#3a2d1f", font="world", spacing=3)
    v.widget("rowing", "rowing", (130, 40, 920, 920), grid=5, origin=[240, 150], cell=140)
    # land to the left edge is only decoration; the grid is drawn by the widget
    v.hot("chart_paper", (140, 40, 1320, 920))
    return v

@view("c3_compass", CH)
def c3_compass():
    v = new("c3_compass", dark="0.06", back="c3_deck")
    cu(v, "#2a3a40", "#141f24")
    cx, cy = 800, 500
    v.layer(1)
    v.add(ellipse(cx, cy, 430), BRASS_D)
    v.layer(2)
    v.add(ellipse(cx, cy, 400), BRASS)
    v.layer(3)
    v.add(ellipse(cx, cy, 372), "#1a2428")
    # the loose card: N E S W and a ring of ticks (rotates; pivot at the centre)
    with v.sprite("card", pivot=(cx, cy), shadow=False):
        v.layer(4)
        v.add(ellipse(cx, cy, 350), "#e8dec2")
        for i in range(72):
            a = math.radians(i * 5)
            L = 28 if i % 18 == 0 else (18 if i % 9 == 0 else 10)
            v.ink(line([(cx + 330 * math.sin(a), cy - 330 * math.cos(a)), (cx + (330 - L) * math.sin(a), cy - (330 - L) * math.cos(a))], 4), INK, d=4)
        # N: a spear point + 'N'; E, S, W as simple stroked letters
        v.add(poly([(cx, cy - 300), (cx - 40, cy - 90), (cx, cy - 130), (cx + 40, cy - 90)]), "#b8453a", d=4)
        v.add(poly([(cx, cy + 300), (cx - 40, cy + 90), (cx, cy + 130), (cx + 40, cy + 90)]), INK, d=4)
        v.add(poly([(cx + 300, cy), (cx + 90, cy - 40), (cx + 130, cy), (cx + 90, cy + 40)]), "#7a6b4a", d=4)
        v.add(poly([(cx - 300, cy), (cx - 90, cy - 40), (cx - 130, cy), (cx - 90, cy + 40)]), "#7a6b4a", d=4)
        # letters (drawn from strokes, so they need no font)
        def L_(x, y, strokes):
            for (a, b) in strokes:
                v.add(line([(x + a[0], y + a[1]), (x + b[0], y + b[1])], 14, ), INK, d=5)
        L_(cx, cy - 230, [((-18, 26), (-18, -26)), ((-18, -26), (18, 26)), ((18, 26), (18, -26))])                     # N
        L_(cx + 230, cy, [((-18, -26), (-18, 26)), ((-18, -26), (18, -26)), ((-18, 0), (12, 0)), ((-18, 26), (18, 26))])    # E
        L_(cx, cy + 230, [((16, -22), (-16, -22)), ((-16, -22), (-16, 0)), ((-16, 0), (16, 0)), ((16, 0), (16, 22)), ((16, 22), (-16, 22))])   # S
        L_(cx - 230, cy, [((-24, -24), (-12, 24)), ((-12, 24), (0, -10)), ((0, -10), (12, 24)), ((12, 24), (24, -24))])      # W
    v.layer(6)
    v.add(ellipse(cx, cy, 22, 22), BRASS)
    # the fixed lubber line: the boat's bow is up, its stern is down
    v.add(poly([(cx - 14, cy - 400), (cx + 14, cy - 400), (cx, cy - 340)]), "#b8453a", d=7)
    v.add(poly([(cx - 14, cy + 400), (cx + 14, cy + 400), (cx, cy + 340)]), "#3a4a52", d=7)
    v.widget("compass", "compass", (cx - 430, cy - 430, 860, 860), cx=cx, cy=cy, sprite="card", flag="compass_ok")
    v.hot("compass_card", (cx - 350, cy - 350, 700, 700))
    return v

@view("c3_float", CH)
def c3_float():
    v = new("c3_float", dark="0.1", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, FOG_T, grad="#2c4852")
    v.layer(1)
    v.rect(0, 560, 1600, 440, SEA_T, grad=SEA_B)
    for i in range(7):
        v.ink(rect(60 + i * 230, 650 + (i % 3) * 60, 200, 4), "#3d6773")
    for i, nm in enumerate(["red", "green", "pale", "yellow"]):
        v.ref("f_" + nm, "c3_lm", "float_" + nm, 800, 800, scale=2.0, show=f"here('{nm}')")
    v.hot("float", (560, 140, 480, 700))
    return v

@view("c3_tree", CH)
def c3_tree():
    v = new("c3_tree", dark="0.1", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#5f797b", grad="#243e48")
    v.layer(1)
    v.rect(0, 700, 1600, 300, SEA_T, grad=SEA_B)
    v.ref("tree_big", "c3_lm", "tree", 800, 840, scale=2.1)
    v.ref("bottle_big", "c3_lm", "bottle_tree", 800, 840, scale=2.1, show="not f('got_tomas_note')")
    v.hot("tree", (300, 40, 1000, 800))
    v.hot("bottle", (610, 280, 260, 320), when="not f('got_tomas_note')")
    return v

@view("c3_buoy", CH)
def c3_buoy():
    v = new("c3_buoy", dark="0.12", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#566f72", grad="#1d3640")
    v.layer(1)
    v.rect(0, 640, 1600, 360, SEA_T, grad=SEA_B)
    v.ref("buoy_big", "c3_lm", "buoy", 800, 860, scale=1.9, fx="sway")
    v.widget("rhythm", "rhythm", (200, 560, 1200, 420), mode="listen", cx=800, cy=800)
    v.hot("buoy_body", (560, 200, 480, 620))
    return v

@view("c3_bell", CH)
def c3_bell():
    v = new("c3_bell", dark="0.1", back="c3_stern")
    cu(v, "#2a3a40", "#141f24")
    v.layer(1)
    v.rect(740, 40, 120, 420, "#4a3326", r=8)
    v.layer(2)
    # a real bell profile: round shoulders, a slight waist, a flared mouth
    import math as _m
    def _hw(t):
        if t < 0.35:
            return 46 + 130 * _m.sin(t / 0.35 * _m.pi / 2)
        if t < 0.78:
            return 176 + 34 * ((t - 0.35) / 0.43)
        return 210 + 110 * ((t - 0.78) / 0.22) ** 2
    prof = [(_hw(i / 40.0), 250 + 500 * i / 40.0) for i in range(41)]
    body = poly([(800 - w, y) for w, y in prof] + [(800 + w, y) for w, y in reversed(prof)])
    v.add(body, BRASS, grad=BRASS_D)
    v.add(ellipse(800, 756, 336, 34), BRASS_D)                                   # the lip
    v.add(rect(466, 742, 668, 22, 8), BRASS)
    _ts = [0.14 + 0.5 * i / 12.0 for i in range(13)]
    v.add(poly([(800 - _hw(t) + 26, 250 + 500 * t) for t in _ts] + [(800 - _hw(t) + 58, 250 + 500 * t) for t in reversed(_ts)]), "#e0c987")   # a highlight
    for ty in (0.42, 0.52):
        yy = 250 + 500 * ty
        v.ink(line([(800 - _hw(ty) + 6, yy), (800 + _hw(ty) - 6, yy)], 6), BRASS_D, d=2)
    v.add(ellipse(800, 244, 44, 34), BRASS_D)                                    # the crown
    v.ink(ring(800, 238, 28, 18), "#2a1c10", d=2)                                # the loop it hangs from
    v.layer(3)
    v.add(ellipse(800, 780, 34, 34), BRASS_D)
    v.add(line([(800, 780), (800, 930)], 14), "#b79c68")
    v.add(ellipse(800, 944, 22, 22), "#b79c68")
    v.widget("rhythm", "rhythm", (300, 300, 1000, 650), mode="answer", cx=800, cy=640)
    v.hot("bell_body", (480, 380, 640, 420))
    return v

@view("c3_deep", CH)
def c3_deep():
    v = new("c3_deep", dark="0.2", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#243e48", grad="#0b1a21")
    v.layer(1)
    v.rect(0, 540, 1600, 460, "#0f2a35", grad="#04090c")
    for k, r_ in enumerate((420, 320, 220, 120)):
        v.ink(ring(800, 780, r_, r_ - 8), "#2c5260")
    v.ref("mast_c", "c3_lm", "mast", 800, 790, scale=1.6)
    v.ref("heron_c", "c3_lm", "heron_mast", 800, 790, scale=1.6, show="not f('got_frag6') and not f('heron_gave')", fx="sway")
    v.ref("heron_cf", "c3_lm", "heron_frag", 800, 790, scale=1.6, show="f('heron_gave') and not f('got_frag6')", fx="sway")
    v.hot("heron_mast", (580, 160, 440, 520), when="not f('got_frag6')")
    v.hot("frag6", (880, 150, 240, 160), when="f('heron_gave') and not f('got_frag6')")
    v.hot("deep_water", (200, 640, 1200, 340))
    v.hot("look_down", (300, 800, 1000, 190))
    return v

@view("c3_reeds", CH)
def c3_reeds():
    v = new("c3_reeds", dark="0.1", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#5f797b", grad="#243e48")
    v.layer(1)
    v.rect(0, 720, 1600, 280, SEA_T, grad=SEA_B)
    v.ref("reeds_big", "c3_lm", "reeds", 800, 870, scale=1.9)
    v.ref("bottle_reeds_big", "c3_lm", "bottle_reeds", 800, 870, scale=1.9, show="not f('got_frag5')")
    v.hot("reeds", (300, 120, 1000, 800))
    v.hot("reed_bottle", (800, 560, 320, 300), when="not f('got_frag5')")
    return v

@view("c3_landing", CH)
def c3_landing():
    v = new("c3_landing", dark="0.12", back="c3_bow")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#0f2a36", grad="#4a7076")
    rnd = random.Random(8)
    for _ in range(40):
        v.ink(ellipse(rnd.random() * 1600, rnd.random() * 300, 1.7, 1.7), "#d3dccf")
    v.layer(1)
    v.rect(0, 600, 1600, 400, SEA_T, grad=SEA_B)
    v.ref("landing_big", "c3_lm", "landing", 1000, 860, scale=1.5)
    v.ref("post_big", "c3_lm", "post", 1000, 860, scale=1.5)
    with v.sprite("rope_line", show="f('moored')"):
        v.layer(6)
        v.add(line([(320, 840), (520, 760), (760, 800), (1000, 770), (1160, 810)], 10), "#b79c68")
    # the bow of the boat, with its mooring line
    v.layer(4)
    v.add(poly([(0, 1000), (0, 760), (400, 700), (560, 780), (300, 1000)]), WOOD_B)
    v.layer(5)
    v.ink(rect(0, 850, 400, 10), "#c9a24d")
    v.widget("moor", "moor", (300, 300, 1200, 560), target=[1205, 800], flag="moored")
    v.hot("post_hit", (1130, 700, 140, 200))
    return v

@view("c3_down", CH)
def c3_down():
    v = new("c3_down", dark="0.0", back="c3_deep")
    v.nav["back"] = None
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#06141b", grad="#010304")
    # the ferry, sunk, its lights still burning; a hand opens to release a moth
    v.layer(1)
    v.add(poly([(260, 640), (1340, 640), (1260, 800), (400, 800)]), "#1a2b33")
    v.add(rect(420, 520, 760, 130, 14), "#22363f")
    for k in range(7):
        v.add(rect(450 + k * 100, 548, 70, 70, 8), "#f3cf84", glow=1.8)
    v.add(rect(780, 400, 40, 130), "#22363f")
    v.add(rect(700, 380, 200, 24, 6), "#22363f")
    v.layer(2)
    v.add(poly([(220, 700), (1380, 700), (1300, 760), (300, 760)]), "#10202a")
    with v.sprite("hand", fx="pulse", shadow=False):
        v.layer(3)
        v.add(rect(782, 340, 36, 190, 8), "#9bb2b4")
        v.add(ellipse(800, 330, 52, 46), "#9bb2b4")
        for k in range(5):
            v.add(rot(rect(790 + (k - 2) * 26 - 4, 220, 16, 120, 8), (k - 2) * 20, origin=(800, 330)), "#9bb2b4")
    with v.sprite("moth_down", fx="bob", shadow=False):
        v.layer(4)
        moth(v, 800, 250, 1.3, glow=1.0)
    v.light(800, 300, 700, "#ffd890", intensity=0.5)
    v.hot("down_look", (200, 160, 1200, 700))
    return v
