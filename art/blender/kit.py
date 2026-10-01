"""Shared prop kit: reusable paper-cut things (they appear in several chapters)."""
import math
from pc import *

# ---------------------------------------------------------------- palette
INK = "#1d1713"
CREAM = "#e8dec2"
PAPER = "#d9cfae"
BRASS = "#c9a24d"
BRASS_D = "#8d6f2c"
WOOD = "#5a3d2c"
WOOD_D = "#3b281d"
WOOD_L = "#7b5339"
OXBLOOD = "#6a2331"
FLAME = "#f7c46a"
FLAME_HOT = "#fff0b8"
MOTH = "#efe7cb"
LAKE = "#1f4150"
LAKE_D = "#112a34"
GOLDFISH = "#e2742f"
GOLDFISH_D = "#b4501e"
# the four floats / books: colour AND pattern (design rule 8)
RED = "#b8453a"
GREEN = "#4f8a5b"
PALE = "#d9d3b6"
YELLOW = "#dcb33c"
FLOAT_COLORS = {"red": RED, "green": GREEN, "pale": PALE, "yellow": YELLOW}
FLOAT_PATTERN = {"red": "stripes", "green": "dots", "pale": "chevrons", "yellow": "plain"}

# ------------------------------------------------------------------ glyphs
GLYPHS = ["eye", "moon", "fish", "bell", "moth", "wave"]

def glyph_geom(name, cx, cy, s):
    """Return (shape, details) geometry for a symbol of size s (about s wide)."""
    r = s / 2
    if name == "eye":
        a = poly([(cx - r, cy)] + [(cx + r * math.cos(t), cy - r * 0.55 * math.sin(t) * 1.0) for t in [math.pi - i * math.pi / 16 for i in range(17)]][::-1] + [(cx + r, cy)])
        top = [(cx + (-r) * math.cos(t), cy - r * 0.62 * math.sin(t)) for t in [i * math.pi / 20 for i in range(21)]]
        bot = [(cx + (-r) * math.cos(t), cy + r * 0.62 * math.sin(t)) for t in [i * math.pi / 20 for i in range(21)]][::-1]
        body = poly(top + bot)
        iris = ellipse(cx, cy, r * 0.36, r * 0.36)
        return body, [(iris, "dark"), (ellipse(cx, cy, r * 0.15, r * 0.15), "light")]
    if name == "moon":
        m = ellipse(cx, cy, r * 0.85).difference(ellipse(cx + r * 0.42, cy - r * 0.12, r * 0.72))
        return m, []
    if name == "fish":
        body = ellipse(cx - r * 0.12, cy, r * 0.72, r * 0.38)
        tail = poly([(cx + r * 0.45, cy), (cx + r * 0.98, cy - r * 0.42), (cx + r * 0.98, cy + r * 0.42)])
        return union(body, tail), [(ellipse(cx - r * 0.52, cy - r * 0.07, r * 0.07, r * 0.07), "dark")]
    if name == "bell":
        dome = ellipse(cx, cy - r * 0.1, r * 0.55, r * 0.62)
        flare = poly([(cx - r * 0.58, cy + r * 0.12), (cx + r * 0.58, cy + r * 0.12), (cx + r * 0.78, cy + r * 0.52), (cx - r * 0.78, cy + r * 0.52)])
        top = rect(cx - r * 0.1, cy - r * 0.82, r * 0.2, r * 0.22, 2)
        return union(dome, flare, top), [(ellipse(cx, cy + r * 0.66, r * 0.14, r * 0.14), "dark")]
    if name == "moth":
        w1 = rot(ellipse(cx - r * 0.42, cy - r * 0.22, r * 0.5, r * 0.27), -28, origin=(cx - r * 0.42, cy - r * 0.22))
        w2 = rot(ellipse(cx + r * 0.42, cy - r * 0.22, r * 0.5, r * 0.27), 28, origin=(cx + r * 0.42, cy - r * 0.22))
        w3 = rot(ellipse(cx - r * 0.34, cy + r * 0.22, r * 0.38, r * 0.2), 24, origin=(cx - r * 0.34, cy + r * 0.22))
        w4 = rot(ellipse(cx + r * 0.34, cy + r * 0.22, r * 0.38, r * 0.2), -24, origin=(cx + r * 0.34, cy + r * 0.22))
        body = ellipse(cx, cy, r * 0.11, r * 0.5)
        return union(w1, w2, w3, w4, body), [(body, "dark")]
    if name == "wave":
        ws = [wave(cx - r * 0.85, cx + r * 0.85, cy + k * r * 0.4, r * 0.14, r * 0.9, r * 0.14, n=24) for k in (-1, 0, 1)]
        return union(*ws), []
    raise ValueError(name)

def draw_glyph(v, name, cx, cy, s, color=CREAM, dark=INK, d=None, **kw):
    shape, details = glyph_geom(name, cx, cy, s)
    v.add(shape, color, d=d, **kw)
    for g, kind in details:
        v.add(g, dark if kind == "dark" else color, d=d, ink=True)
    return shape

# --------------------------------------------------------------- furniture
def wall(v, top, bottom, wain_y=700, wain_top=WOOD, wain_bottom=WOOD_D, floor_y=950, floor=None, planks=True):
    v.layer(0)
    v.rect(0, 0, 1600, 1000, top, grad=bottom)
    v.layer(1)
    v.rect(0, wain_y, 1600, 1000 - wain_y, wain_top, grad=wain_bottom)
    v.layer(2)
    v.rect(0, wain_y - 14, 1600, 22, shade(wain_top, 0.12))
    if planks:
        x = 0
        while x < 1600:
            v.ink(rect(x + 197, wain_y + 20, 3, floor_y - wain_y - 20), shade(wain_top, -0.35), alpha=1)
            x += 200
    v.layer(2)
    v.rect(0, floor_y, 1600, 1000 - floor_y, floor or shade(wain_bottom, -0.4))
    v.rect(0, floor_y - 18, 1600, 22, shade(wain_top, -0.1))

def frame(v, x, y, w, h, outer=WOOD_D, inner=None, t=18, d=3, inner_grad=None, r=6):
    v.layer(d)
    v.rect(x, y, w, h, outer, r=r)
    if inner is not None:
        v.layer(d + 1)
        v.rect(x + t, y + t, w - 2 * t, h - 2 * t, inner, grad=inner_grad)

def key_shape(cx, cy, s=1.0, ang=0):
    bow = ring(cx - 26 * s, cy, 20 * s, 9 * s)
    shaft = rect(cx - 8 * s, cy - 4 * s, 62 * s, 8 * s, 2)
    t1 = rect(cx + 34 * s, cy, 8 * s, 18 * s)
    t2 = rect(cx + 46 * s, cy, 8 * s, 14 * s)
    return rot(union(bow, shaft, t1, t2), ang, origin=(cx, cy))

def key(v, cx, cy, s=1.0, ang=0, color=BRASS, d=None):
    v.add(key_shape(cx, cy, s, ang), color, d=d)

def book_shape(x, y, w, h, tilt=0):
    return rot(rect(x, y, w, h, 4), tilt, origin=(x + w / 2, y + h))

def book(v, x, y, w, h, color, pattern="plain", d=None, spine=True, tilt=0, trim=BRASS):
    """a standing book seen from the spine: colour + pattern"""
    b = rect(x, y, w, h, 5)
    v.add(rot(b, tilt, origin=(x + w / 2, y + h)) if tilt else b, color, d=d)
    inner = rect(x + 6, y + 14, w - 12, h - 28)
    if pattern == "stripes":
        p = stripes(inner, 0, 22, 8, 0)
        v.ink(rot(p, tilt, origin=(x + w / 2, y + h)), shade(color, -0.42), d=d)
    elif pattern == "dots":
        p = dots(inner, 20, 5)
        v.ink(rot(p, tilt, origin=(x + w / 2, y + h)), shade(color, -0.4), d=d)
    elif pattern == "chevrons":
        p = chevrons(inner, 24, 7, 16)
        v.ink(rot(p, tilt, origin=(x + w / 2, y + h)), shade(color, -0.42), d=d)
    elif pattern == "plain":
        v.ink(rot(rect(x + 6, y + 14, w - 12, 5), tilt, origin=(x + w / 2, y + h)), shade(color, -0.3), d=d)
    for yy in (y + 8, y + h - 12):
        v.ink(rot(rect(x, yy, w, 4), tilt, origin=(x + w / 2, y + h)), trim, d=d)

def candle_stub(v, cx, base_y, s=1.0, d=None, color="#d9cdb0"):
    v.add(rect(cx - 26 * s, base_y - 14 * s, 52 * s, 14 * s, 4), BRASS_D, d=d)       # saucer
    v.add(rect(cx - 15 * s, base_y - 60 * s, 30 * s, 48 * s, 3), color, d=d)
    v.ink(poly([(cx - 15 * s, base_y - 60 * s), (cx + 15 * s, base_y - 60 * s), (cx + 10 * s, base_y - 48 * s), (cx - 6 * s, base_y - 52 * s)]), shade(color, -0.12), d=d)
    v.ink(rect(cx - 1.5 * s, base_y - 70 * s, 3 * s, 12 * s), INK, d=d)               # wick

def flame(v, cx, cy, s=1.0, d=None, glow=3.0):
    f = poly([(cx, cy - 46 * s), (cx + 14 * s, cy - 14 * s), (cx + 10 * s, cy + 6 * s), (cx - 10 * s, cy + 6 * s), (cx - 14 * s, cy - 14 * s)])
    f = union(f, ellipse(cx, cy - 6 * s, 14 * s, 15 * s))
    v.add(f, FLAME, d=d, glow=glow, ink=True)
    v.add(ellipse(cx, cy - 2 * s, 6 * s, 12 * s), FLAME_HOT, d=d, glow=4.5, ink=True)

def lantern(v, cx, base_y, s=1.0, lit=False, oil=False, d=None):
    """paper lantern with cut glass; origin at base centre"""
    w, h = 84 * s, 118 * s
    x0 = cx - w / 2
    v.add(rect(x0 - 5 * s, base_y - 14 * s, w + 10 * s, 14 * s, 3), "#1f2a2b", d=d)                 # base
    v.add(rect(x0, base_y - h, w, h - 12 * s, 6 * s), "#2f4144", d=d)                                # frame
    glass = rect(x0 + 10 * s, base_y - h + 22 * s, w - 20 * s, h - 54 * s, 5 * s)
    gc = "#f3cf84" if lit else ("#3c5a5c" if oil else "#41605f")
    v.add(glass, gc, d=d, glow=(2.2 if lit else 0.0), ink=True)
    if oil and not lit:
        v.ink(rect(x0 + 12 * s, base_y - 56 * s, w - 24 * s, 28 * s, 4), "#b79338", d=d)
    v.add(rect(x0 - 6 * s, base_y - h - 4 * s, w + 12 * s, 16 * s, 4), "#1f2a2b", d=d)             # cap
    v.add(arc(cx, base_y - h - 2 * s, 30 * s, 180, 360, 6 * s), "#1f2a2b", d=d)                     # handle
    v.ink(rect(cx - 3 * s, base_y - h + 22 * s, 6 * s, h - 54 * s), "#2f4144", d=d)
    if lit:
        flame(v, cx, base_y - 70 * s, 0.85 * s, d=d, glow=3.2)

def jar_shape(x, y, w, h):
    body = rect(x, y + h * 0.14, w, h * 0.86, 12)
    neck = rect(x + w * 0.1, y, w * 0.8, h * 0.2, 6)
    return union(body, neck)

def pell_fish(v, cx, cy, s=1.0, facing=1, d=None, eye_open=True):
    """Pell: a goldfish with one oddly human eye."""
    f = facing
    body = ellipse(cx, cy, 58 * s, 38 * s)
    tail = poly([(cx - f * 44 * s, cy), (cx - f * 108 * s, cy - 44 * s), (cx - f * 92 * s, cy), (cx - f * 108 * s, cy + 44 * s)])
    fin_t = poly([(cx - f * 8 * s, cy - 34 * s), (cx + f * 26 * s, cy - 62 * s), (cx + f * 32 * s, cy - 30 * s)])
    fin_b = poly([(cx - f * 4 * s, cy + 34 * s), (cx - f * 24 * s, cy + 58 * s), (cx + f * 12 * s, cy + 36 * s)])
    v.add(union(tail), GOLDFISH_D, d=d)
    v.add(union(fin_t, fin_b), GOLDFISH_D, d=d)
    v.add(body, GOLDFISH, d=d)
    # scales
    for i in range(3):
        v.ink(arc(cx - f * (6 + i * 18) * s, cy + 4 * s, 20 * s, 90 + (0 if f > 0 else 0), 270, 3 * s) if f < 0 else arc(cx - f * (6 + i * 18) * s, cy + 4 * s, 20 * s, -90, 90, 3 * s), GOLDFISH_D, d=d)
    # the human eye: white, iris with a lid
    ex, ey = cx + f * 28 * s, cy - 8 * s
    v.add(ellipse(ex, ey, 17 * s, 14 * s), "#f4efe4", d=d)
    v.ink(ellipse(ex + f * 2 * s, ey + 1 * s, 9 * s, 9 * s), "#4a3a2a", d=d)
    v.ink(ellipse(ex + f * 2 * s, ey + 1 * s, 4.5 * s, 4.5 * s), INK, d=d)
    v.ink(ellipse(ex + f * 5 * s, ey - 2 * s, 2 * s, 2 * s), "#ffffff", d=d)
    if eye_open:
        v.ink(poly([(ex - 18 * s, ey - 2 * s), (ex, ey - 17 * s), (ex + 18 * s, ey - 2 * s), (ex + 18 * s, ey - 6 * s), (ex, ey - 20 * s), (ex - 18 * s, ey - 6 * s)]), GOLDFISH_D, d=d)
    # mouth
    v.ink(arc(cx + f * 56 * s, cy + 10 * s, 8 * s, 80 if f > 0 else 100, 260 if f > 0 else 280, 3 * s) if False else line([(cx + f * 56 * s, cy + 9 * s), (cx + f * 46 * s, cy + 12 * s)], 3 * s), INK, d=d)

def moth(v, cx, cy, s=1.0, d=None, glow=0.0, color=MOTH, rot_=0, wings=1.0):
    w = 46 * s * wings
    parts = [
        rot(ellipse(cx - w * 0.62, cy - 10 * s, w * 0.7, 20 * s), -22, origin=(cx, cy)),
        rot(ellipse(cx + w * 0.62, cy - 10 * s, w * 0.7, 20 * s), 22, origin=(cx, cy)),
        rot(ellipse(cx - w * 0.5, cy + 14 * s, w * 0.5, 13 * s), 20, origin=(cx, cy)),
        rot(ellipse(cx + w * 0.5, cy + 14 * s, w * 0.5, 13 * s), -20, origin=(cx, cy)),
    ]
    g = union(*parts)
    if rot_:
        g = rot(g, rot_, origin=(cx, cy))
    v.add(g, color, d=d, glow=glow)
    v.ink(ellipse(cx, cy, 5 * s, 22 * s), "#5b4a3a", d=d)
    v.ink(line([(cx - 2 * s, cy - 20 * s), (cx - 16 * s, cy - 38 * s)], 2.5 * s), "#5b4a3a", d=d)
    v.ink(line([(cx + 2 * s, cy - 20 * s), (cx + 16 * s, cy - 38 * s)], 2.5 * s), "#5b4a3a", d=d)
    # wing eyes
    v.ink(ellipse(cx - w * 0.7, cy - 12 * s, 6 * s, 6 * s), "#a89870", d=d)
    v.ink(ellipse(cx + w * 0.7, cy - 12 * s, 6 * s, 6 * s), "#a89870", d=d)

def paper_sheet(v, x, y, w, h, color=PAPER, ang=0, d=None, lines=0, ink=INK, margin=16, pin=False):
    g = rect(x, y, w, h, 3)
    if ang:
        g = rot(g, ang)
    v.add(g, color, d=d)
    cx, cy = x + w / 2, y + h / 2
    for i in range(lines):
        ly = y + margin + 10 + i * ((h - 2 * margin - 10) / max(1, lines))
        l = line([(x + margin, ly), (x + w - margin - (i % 3) * 14, ly)], 3)
        v.ink(rot(l, ang, origin=(cx, cy)) if ang else l, ink, alpha=0.7, d=d)
    if pin:
        v.add(ellipse(x + w / 2, y + 10, 8, 8), "#9a2d2d", d=d)
    return g

def moon(v, cx, cy, r, color="#d8dfcf", d=None):
    v.add(ellipse(cx, cy, r), color, d=d)

def lake_window(v, x, y, w, h, far_light=None, d=3, sky_top="#16303a", sky_bot="#2c5864", water_top="#1b3c48", water_bot="#0d222b",
                horizon=0.55, moon_pos=(0.78, 0.2), stars=True, lighthouse=True):
    """A window pane looking out over the still lake at night; returns geometry of horizon, lighthouse base."""
    v.layer(d)
    v.rect(x, y, w, h, sky_top, grad=sky_bot)
    hy = y + h * horizon
    v.rect(x, hy, w, y + h - hy, water_top, grad=water_bot)
    if moon_pos:
        v.add(ellipse(x + w * moon_pos[0], y + h * moon_pos[1], w * 0.045), "#d6dccb", d=d, glow=0.0)
    if stars:
        rnd = random.Random(int(x + y + w))
        for _ in range(14):
            sx, sy = x + rnd.random() * w, y + rnd.random() * (hy - y) * 0.8
            v.ink(ellipse(sx, sy, 2.2, 2.2), "#cfd8c8")
    # still, unmoving reflection lines
    for i in range(4):
        v.ink(rect(x + w * (0.18 + 0.18 * i), hy + 14 + i * 22, w * 0.2, 3), "#2d5a68", alpha=1)
    if lighthouse:
        lx = x + w * 0.5
        v.ink(poly([(lx - 9, hy), (lx - 5, hy - 46), (lx + 5, hy - 46), (lx + 9, hy)]), "#0b1a21")
        v.ink(rect(lx - 7, hy - 56, 14, 10), "#0b1a21")
        v.ink(poly([(lx - 9, hy - 56), (lx, hy - 66), (lx + 9, hy - 56)]), "#0b1a21")
        if far_light:
            v.add(ellipse(lx, hy - 52, 5, 5), FLAME, glow=4, ink=True)
    return hy

def hand_shape(cx, cy, length, width, tail=0.18):
    """a clock hand pointing straight UP from pivot (cx,cy); rotate later."""
    L = length
    pts = [(cx - width * 0.5, cy + L * tail), (cx - width * 0.5, cy - L * 0.78), (cx, cy - L), (cx + width * 0.5, cy - L * 0.78), (cx + width * 0.5, cy + L * tail)]
    return poly(pts)

def heron_silhouette(v, cx, base_y, s=1.0, color="#8ea0a4", d=None, flip=False):
    f = -1 if flip else 1
    body = ellipse(cx, base_y - 170 * s, 36 * s, 62 * s)
    body = rot(body, 14 * f, origin=(cx, base_y - 170 * s))
    neck = line([(cx + f * 14 * s, base_y - 220 * s), (cx + f * 30 * s, base_y - 270 * s), (cx + f * 18 * s, base_y - 316 * s), (cx + f * 30 * s, base_y - 350 * s)], 12 * s)
    head = ellipse(cx + f * 34 * s, base_y - 356 * s, 17 * s, 11 * s)
    beak = poly([(cx + f * 46 * s, base_y - 362 * s), (cx + f * 108 * s, base_y - 348 * s), (cx + f * 46 * s, base_y - 350 * s)])
    legs = union(line([(cx, base_y - 112 * s), (cx - f * 4 * s, base_y)], 6 * s), line([(cx + f * 14 * s, base_y - 112 * s), (cx + f * 22 * s, base_y)], 6 * s))
    wing = rot(ellipse(cx - f * 10 * s, base_y - 170 * s, 24 * s, 50 * s), 14 * f, origin=(cx, base_y - 170 * s))
    v.add(legs, shade(color, -0.45), d=d)
    v.add(union(body, neck, head), color, d=d)
    v.add(beak, "#c99b3f", d=d)
    v.ink(wing, shade(color, -0.2), d=d)
    v.ink(ellipse(cx + f * 38 * s, base_y - 358 * s, 3 * s, 3 * s), INK, d=d)
    v.ink(rect(cx - 8 * s, base_y - 255 * s, 16 * s, 4 * s), shade(color, 0.35), d=d)

def sparkle(v, cx, cy, s=1.0, color="#fff4c8", d=None):
    v.add(union(rect(cx - 2 * s, cy - 14 * s, 4 * s, 28 * s), rect(cx - 14 * s, cy - 2 * s, 28 * s, 4 * s)), color, d=d, glow=2.5, ink=True)

def float_buoy(v, cx, cy, s, color, pattern, d=None, flag_color=None):
    """A channel float: coloured body with a pattern (colour + pattern, design rule 8). cy = waterline."""
    body = poly([(cx - 34 * s, cy), (cx - 26 * s, cy - 60 * s), (cx - 10 * s, cy - 96 * s), (cx + 10 * s, cy - 96 * s), (cx + 26 * s, cy - 60 * s), (cx + 34 * s, cy)])
    v.add(body, color, d=d)
    inner = inter(body, rect(cx - 40 * s, cy - 88 * s, 80 * s, 80 * s))
    dark = shade(color, -0.42)
    if pattern == "stripes":
        v.ink(stripes(inner, 0, 18 * s, 7 * s), dark, d=d)
    elif pattern == "dots":
        v.ink(dots(inner, 17 * s, 4.5 * s), dark, d=d)
    elif pattern == "chevrons":
        v.ink(chevrons(inner, 21 * s, 6 * s, 13 * s), dark, d=d)
    else:
        v.ink(rect(cx - 30 * s, cy - 16 * s, 60 * s, 5 * s), dark, d=d)
    v.add(rect(cx - 3 * s, cy - 130 * s, 6 * s, 40 * s), "#2a2a2c", d=d)
    v.add(ellipse(cx, cy - 134 * s, 8 * s, 8 * s), color, d=d)
    v.add(ellipse(cx, cy + 6 * s, 44 * s, 8 * s), "#0e2029", d=d, alpha=1)      # waterline shadow

def flip_v(g):
    return affinity.scale(g, 1, -1, origin="center")
