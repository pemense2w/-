"""Chapter 2 - The Boathouse: the jetty, four dark walls (lit one at a time by the lantern) and close-ups."""
import math
from pc import *
from reg import view
from kit import *

CH = "c2"
PLANK = "#4b3a2e"
PLANK_D = "#33271e"
BEAM = "#2b2018"
TAR = "#1d1815"
ROPE = "#b79c68"
WATER_T, WATER_B = "#1c3a46", "#0b1a21"
IRON = "#3a3d3f"
AMBIENT = "#2c3b46"

def wall_dark(hang):
    """darkness of an interior wall: black unless the lantern hangs on it"""
    return f"pick(fs('hung') == '{hang}', 0.14, 0.97)"

def new(id, dark="0.0", **kw):
    v = View(id, CH, **kw)
    v.dark = dark
    v.ambient = AMBIENT
    return v

def planks_wall(v, x0, y0, x1, y1, base=PLANK, dark=PLANK_D, pw=110, d=0, seed=1):
    rnd = random.Random(seed)
    v.layer(d)
    x = x0
    i = 0
    while x < x1:
        w = min(pw + rnd.randint(-14, 14), x1 - x)
        c = mix(base, dark, 0.15 * ((i * 7) % 5) / 4)
        v.rect(x, y0, w, y1 - y0, c, grad=shade(c, -0.08))
        v.ink(rect(x + w - 3, y0, 3, y1 - y0), shade(dark, -0.3))
        for _ in range(2):
            ky = y0 + rnd.random() * (y1 - y0 - 60) + 20
            v.ink(ellipse(x + w * (0.3 + rnd.random() * 0.4), ky, 7, 14), shade(c, -0.22))
        x += w
        i += 1

def beam_h(v, x, y, w, h=44, d=1):
    v.layer(d)
    v.rect(x, y, w, h, BEAM, grad=shade(BEAM, -0.2))
    v.ink(rect(x, y + 6, w, 3), shade(BEAM, 0.14))

def post(v, x, y, w, h, d=1):
    v.layer(d)
    v.rect(x, y, w, h, BEAM, grad=shade(BEAM, -0.15))
    v.ink(rect(x + 5, y, 4, h), shade(BEAM, 0.14))

def hook(v, x, y, d=3):
    v.layer(d)
    v.add(rect(x - 6, y - 40, 12, 40), IRON)
    v.add(arc(x + 22, y, 22, 90, 270, 9) if False else line([(x, y), (x, y + 24), (x + 22, y + 40), (x + 36, y + 24)], 9), IRON)

def rope_coil(v, cx, cy, r=60, d=3):
    v.layer(d)
    for k in range(4):
        v.add(ring(cx, cy, r - k * 12, r - k * 12 - 9), ROPE)
    v.add(line([(cx + r - 20, cy), (cx + r + 40, cy + 30)], 9), ROPE)

def barrel(v, x, y, w, h, d=2):
    v.layer(d)
    v.add(rect(x, y, w, h, 24), "#5d4330")
    for k in (0.18, 0.5, 0.82):
        v.ink(rect(x, y + h * k - 6, w, 12), IRON)
    for k in range(1, 5):
        v.ink(rect(x + w * k / 5 - 2, y + 4, 4, h - 8), shade("#5d4330", -0.25))

def gear_shape(cx, cy, r, teeth, th=14, hole=0.35, spokes=True):
    pts = []
    pitch = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * pitch
        for f, rr in ((0.0, r - th / 2), (0.18, r + th / 2), (0.5, r + th / 2), (0.68, r - th / 2)):
            ang = a + f * pitch
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    g = Polygon(pts).buffer(0)
    g = g.difference(ellipse(cx, cy, r * hole))
    if spokes and r > 50:
        n = 5
        cut = []
        for k in range(n):
            a = k * 2 * math.pi / n + 0.3
            cut.append(sector(cx, cy, r * 0.78, math.degrees(a) + 8, math.degrees(a) + 360 / n - 8).difference(ellipse(cx, cy, r * 0.42)))
        g = g.difference(union(*cut))
    return g

def rope_path(pts, w=26):
    return line(pts, w)

def twist(v, pts, w=26, color="#6f5a38", step=22, d=None):
    """short diagonal marks along a polyline: twisted rope"""
    segs = []
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        ux, uy = (x1 - x0) / L, (y1 - y0) / L
        for k in range(n):
            px, py = x0 + ux * (k + 0.5) * L / n, y0 + uy * (k + 0.5) * L / n
            nx, ny = -uy, ux
            segs.append(line([(px - nx * w * 0.4 - ux * 4, py - ny * w * 0.4 - uy * 4), (px + nx * w * 0.4 + ux * 4, py + ny * w * 0.4 + uy * 4)], 3, cap="flat"))
    v.ink(union(*segs), color, d=d)

def corner_pts(cx, cy, r, a0, a1, n=14):
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]

def gunwale_boat(v, ox=0, oy=0, patch=False, hole=True):
    """the rowing boat Agnes, from the side, bow to the right"""
    top = [(250, 560), (500, 545), (800, 540), (1100, 520), (1360, 470)]
    bot = [(1300, 640), (1100, 750), (800, 790), (500, 780), (300, 740), (240, 640)]
    pts = [(x + ox, y + oy) for x, y in top + bot]
    hull = poly(pts)
    v.add(hull, "#8a5a36", grad="#6a4126")
    for k in range(1, 5):
        yy = [(560 + k * 40), (545 + k * 40)]
        v.ink(line([(262 + ox + k * 14, 566 + oy + k * 38), (500 + ox, 556 + oy + k * 44), (800 + ox, 550 + oy + k * 46), (1100 + ox - k * 24, 530 + oy + k * 36), (1330 + ox - k * 40, 490 + oy + k * 36)], 4), "#5a3820")
    v.ink(rect(250 + ox, 548 + oy, 1110, 16), "#c9a24d")             # gunwale strip
    v.ink(poly([(1360 + ox, 470 + oy), (1380 + ox, 430 + oy), (1330 + ox, 500 + oy)]), "#6a4126")
    if hole:
        h = poly([(600 + ox, 640 + oy), (630 + ox, 612 + oy), (680 + ox, 618 + oy), (712 + ox, 650 + oy), (700 + ox, 698 + oy), (650 + ox, 706 + oy), (610 + ox, 686 + oy)])
        v.add(h, "#0a0706", ink=True)
    return hull

# ======================================================================== JETTY
def fog_bands(v, y0, y1, c="#9fb5b4", n=6, seed=3, alpha=1):
    rnd = random.Random(seed)
    for i in range(n):
        x = rnd.random() * 1600 - 200
        y = y0 + rnd.random() * (y1 - y0)
        v.ink(ellipse(x, y, 260 + rnd.random() * 200, 22 + rnd.random() * 14), shade(c, 0.0))

@view("c2_jetty", CH)
def c2_jetty():
    v = new("c2_jetty", dark="0.18", left="c2_jetty_end", right="c2_jetty_end")
    v.ambient = "#40586a"
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#14303a", grad="#7d9a99")
    for _ in range(40):
        rnd = random
    rnd = random.Random(11)
    for _ in range(26):
        v.ink(ellipse(rnd.random() * 1600, rnd.random() * 260, 1.8, 1.8), "#d3dccf")
    v.layer(1)
    v.add(ellipse(300, 170, 80), "#dfe6d5")
    v.add(poly([(0, 430), (300, 400), (700, 420), (1000, 380), (1600, 410), (1600, 520), (0, 520)]), "#22434d")     # far shore
    v.layer(1)
    v.rect(0, 500, 1600, 500, "#244752", grad=WATER_B)
    for i in range(12):
        v.ink(rect(60 + (i * 141) % 1500, 560 + i * 34, 180 + (i % 3) * 70, 4), "#3d6773")
    fog_bands(v, 470, 560, n=8)
    # the boathouse (right)
    v.layer(2)
    v.rect(900, 240, 700, 520, "#4a392d", grad="#33271e")
    for x in range(900, 1600, 70):
        v.ink(rect(x + 66, 240, 4, 520), "#241a13")
    v.layer(3)
    v.add(poly([(870, 250), (1250, 110), (1630, 250)]), "#2b2018")
    v.add(poly([(870, 250), (1250, 130), (1630, 250), (1630, 262), (870, 262)]), "#3a2b20")
    v.layer(3)
    v.rect(1130, 400, 240, 360, "#241a13", r=4)
    v.layer(4)
    v.rect(1146, 416, 208, 344, "#5a4636", r=3)
    v.ink(rect(1244, 416, 12, 344), "#33271e")
    v.add(ellipse(1260, 600, 12, 12), BRASS)
    v.ink(rect(1170, 560, 8, 150), "#0f0c0a")
    # window with a missing pane
    v.layer(3)
    v.rect(940, 360, 110, 130, "#241a13")
    v.layer(4)
    v.rect(952, 372, 86, 106, "#0f1a20")
    # the jetty
    v.layer(3)
    v.rect(0, 740, 1100, 70, "#6b5543", grad="#56432f")
    for x in range(0, 1100, 90):
        v.ink(rect(x, 740, 3, 70), "#2f241a")
    v.layer(2)
    for x in (80, 330, 760, 1020):
        v.rect(x, 810, 38, 190, "#33271e")
    # the gap in the planks
    v.layer(4)
    v.rect(450, 736, 110, 78, "#07131a", grad="#1b3a47")
    v.layer(3)
    v.rect(0, 806, 1100, 14, "#2f241a")
    # bollard + rope coil + cold lamp-post
    v.layer(4)
    v.rect(680, 690, 44, 54, "#3a3d3f", r=8); v.add(ellipse(702, 690, 30, 12), "#4a4e50")
    rope_coil(v, 190, 730, 52, d=5)
    v.layer(4)
    v.rect(940, 520, 14, 230, "#2b2018")
    v.rect(916, 480, 62, 50, "#1f2a2b", r=6); v.ink(rect(926, 490, 42, 30, 4), "#41605f")
    v.hot("bh_door", (1130, 400, 240, 360))
    v.hot("gap", (440, 726, 130, 98))
    v.hot("bollard", (660, 680, 90, 70))
    v.hot("coil", (130, 680, 130, 100))
    v.hot("jetty_lamp", (900, 470, 100, 280))
    v.hot("jetty_water", (0, 830, 600, 170))
    return v

@view("c2_jetty_end", CH)
def c2_jetty_end():
    v = new("c2_jetty_end", dark="0.18", left="c2_jetty", right="c2_jetty")
    v.ambient = "#40586a"
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#14303a", grad="#86a3a0")
    rnd = random.Random(5)
    for _ in range(30):
        v.ink(ellipse(rnd.random() * 1600, rnd.random() * 280, 1.8, 1.8), "#d3dccf")
    v.layer(1)
    v.rect(0, 520, 1600, 480, "#244752", grad=WATER_B)
    for i in range(12):
        v.ink(rect(40 + (i * 163) % 1500, 580 + i * 32, 160 + (i % 3) * 80, 4), "#3d6773")
    fog_bands(v, 480, 600, n=9, seed=8)
    # the far light, dark, small on the horizon
    v.layer(2)
    v.add(poly([(1180, 520), (1190, 420), (1210, 420), (1220, 520)]), "#0e1c22")
    v.add(rect(1186, 400, 28, 20), "#0e1c22"); v.add(poly([(1182, 400), (1200, 384), (1218, 400)]), "#0e1c22")
    # jetty planks running out to the end
    v.layer(3)
    v.rect(0, 760, 1250, 70, "#6b5543", grad="#56432f")
    for x in range(0, 1250, 90):
        v.ink(rect(x, 760, 3, 70), "#2f241a")
    v.layer(2)
    for x in (140, 520, 900, 1180):
        v.rect(x, 830, 38, 170, "#33271e")
    # big piling at the end, where the second oar leans
    v.layer(4)
    v.rect(860, 380, 92, 440, "#3a2d24", r=14)
    v.ink(rect(870, 380, 10, 440), "#4f3e31")
    v.add(ellipse(906, 380, 48, 14), "#4f3e31")
    v.layer(4)
    v.rect(1090, 520, 70, 300, "#3a2d24", r=12)          # a second piling (the heron steps here)
    v.add(ellipse(1125, 520, 36, 11), "#4f3e31")
    v.layer(4)
    v.rect(480, 600, 64, 220, "#3a2d24", r=12)           # a third (where it waits later)
    v.add(ellipse(512, 600, 32, 10), "#4f3e31")
    with v.sprite("oar2", show="f('heron_aside') and not f('got_oar2')"):
        v.layer(6)
        v.add(rot(rect(786, 330, 20, 480, 6), -6), "#8a6a46")
        v.add(rot(rect(752, 250, 66, 200, 26), -6, origin=(790, 330)), "#a68359")
    with v.sprite("oar2_hidden", show="not f('heron_aside')"):
        v.layer(5)
        v.add(rot(rect(786, 330, 20, 480, 6), -6), "#8a6a46")
        v.add(rot(rect(752, 250, 66, 200, 26), -6, origin=(790, 330)), "#a68359")
    with v.sprite("heron_guard", show="not f('heron_aside')", fx="sway"):
        v.layer(7)
        heron_silhouette(v, 906, 394, 0.8, d=7)
    with v.sprite("heron_aside", show="f('heron_aside') and not f('heron_fed2')", fx="sway"):
        v.layer(7)
        heron_silhouette(v, 1125, 530, 0.8, d=7, flip=True)
    with v.sprite("heron_frag", show="f('heron_fed2') and not f('got_frag4')", fx="sway"):
        v.layer(7)
        heron_silhouette(v, 512, 610, 0.8, d=7)
        v.add(poly([(594, 262), (640, 252), (648, 280), (600, 292)]), "#d1c6a4", d=8)
    with v.sprite("heron_calm", show="f('got_frag4')", fx="sway"):
        v.layer(7)
        heron_silhouette(v, 512, 610, 0.8, d=7)
    v.hot("piling", (850, 370, 120, 460))
    v.hot("heron", (820, 40, 220, 360), when="not f('heron_aside')")
    v.hot("heron", (1060, 160, 200, 380), when="f('heron_aside') and not f('heron_fed2')")
    v.hot("oar2", (740, 230, 100, 560), when="f('heron_aside') and not f('got_oar2')")
    v.hot("heron_back", (440, 160, 200, 460), when="f('heron_fed2') and not f('got_frag4')")
    v.hot("frag4", (580, 240, 90, 70), when="f('heron_fed2') and not f('got_frag4')")
    v.hot("heron_calm", (440, 160, 200, 460), when="f('got_frag4')")
    v.hot("end_water", (1250, 600, 350, 380))
    v.hot("far_light", (1150, 380, 100, 150))
    return v

@view("c2_gap", CH)
def c2_gap():
    v = new("c2_gap", dark="0.1", back="c2_jetty")
    v.ambient = "#40586a"
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#56432f", grad="#3b2d21")
    planks_wall(v, 0, 0, 1600, 1000, base="#6b5543", dark="#4a3828", pw=220, d=0, seed=4)
    v.layer(2)
    v.rect(260, 220, 1080, 560, "#07131a", grad="#27505c", r=16)             # the gap, looking down at the water
    v.layer(3)
    for i in range(8):
        v.ink(rect(300 + (i * 131) % 900, 330 + i * 52, 150 + (i % 3) * 60, 4), "#3d6773")
    v.layer(4)
    v.add(rect(240, 200, 1120, 28, 8), "#2f241a"); v.add(rect(240, 772, 1120, 28, 8), "#2f241a")
    v.widget("catch", "catch", (260, 220, 1080, 560), flag="got_fish_once")
    v.hot("gap_look", (260, 220, 1080, 560))
    return v

# ================================================================ BOATHOUSE WALLS
@view("c2_bh_door", CH)
def c2_bh_door():
    v = new("c2_bh_door", dark="0.5", left="c2_bh_right", right="c2_bh_left")
    planks_wall(v, 0, 0, 1600, 1000, seed=2)
    beam_h(v, 0, 60, 1600, 50, d=1)
    post(v, 120, 0, 60, 1000); post(v, 1420, 0, 60, 1000)
    # the great door, open a slit onto the fog
    v.layer(2)
    v.rect(520, 150, 560, 760, "#241a13", r=4)
    v.layer(3)
    v.rect(546, 176, 508, 734, "#6d8a8b", grad="#cfdcd8")                    # fog light through the gap
    v.layer(4)
    v.add(poly([(546, 176), (760, 176), (760, 910), (546, 910)]), "#4b3a2e", grad="#33271e")
    v.add(poly([(840, 176), (1054, 176), (1054, 910), (840, 910)]), "#4b3a2e", grad="#33271e")
    for x in (600, 690, 890, 980):
        v.ink(rect(x, 176, 4, 734), "#241a13", d=4)
    v.layer(5)
    v.rect(546, 520, 214, 24, IRON); v.rect(840, 520, 214, 24, IRON)
    v.add(ellipse(780, 700, 11, 11), BRASS)
    # barrel, life ring, oar rack
    barrel(v, 1210, 640, 150, 250)
    v.layer(3)
    v.add(ring(260, 400, 90, 52), "#b8453a")
    v.ink(rect(166, 396, 188, 12), "#e6dcc0"); v.ink(rect(254, 308, 12, 188), "#e6dcc0")
    v.layer(3)
    v.rect(1180, 260, 22, 200, IRON); v.rect(1300, 260, 22, 200, IRON)
    v.rect(1160, 300, 180, 16, "#33271e"); v.rect(1160, 400, 180, 16, "#33271e")
    v.hot("door_out", (546, 176, 508, 734))
    v.hot("life_ring", (160, 300, 200, 200))
    v.hot("rack", (1150, 250, 200, 220))
    v.hot("barrel_d", (1200, 630, 170, 270))
    v.light(800, 420, 780, "#a8c4c0", intensity=0.45)
    return v

def hung_lantern(v, x, y, wall):
    with v.sprite("lantern_hung", show=f"fs('hung') == '{wall}'", fx="flicker"):
        v.layer(5)
        lantern(v, x, y + 196, 1.1, lit=True)

@view("c2_bh_left", CH)
def c2_bh_left():
    v = new("c2_bh_left", dark=wall_dark("left"), left="c2_bh_door", right="c2_bh_back")
    planks_wall(v, 0, 0, 1600, 1000, seed=3)
    beam_h(v, 0, 60, 1600, 50); post(v, 80, 0, 60, 1000); post(v, 1460, 0, 60, 1000)
    hook(v, 800, 170)
    hung_lantern(v, 836, 150, "left")
    v.light(836, 330, 1250, "#ffb860", when="fs('hung') == 'left'", intensity=1.1, flicker=0.05)
    # shelf with the ship in a bottle
    v.layer(2)
    v.rect(1060, 300, 360, 24, "#6e4b36")
    v.layer(3)
    v.add(union(ellipse(1210, 262, 70, 40), rect(1280, 238, 90, 28, 8)), "#8fb4b0")
    v.add(rect(1348, 230, 24, 18, 3), "#a8825a")
    v.ink(poly([(1150, 290), (1270, 290), (1250, 262), (1170, 262)]), "#3b281d")
    v.ink(rect(1210, 200, 5, 62), "#c9b88a")
    v.ink(poly([(1215, 205), (1215, 258), (1250, 258)]), "#e6dcc0")
    # pegboard with tools
    v.layer(2)
    v.rect(200, 200, 520, 280, "#3f3026", r=6)
    for (tx, ty, tw, th_) in ((240, 240, 26, 180), (310, 250, 18, 150), (370, 240, 60, 40), (470, 250, 24, 170), (540, 260, 100, 22)):
        v.add(rect(tx, ty, tw, th_, 5), "#6e7274")
    # tangled net on the wall
    with v.sprite("net_tangle", show="not f('got_net')", d=3):
        v.layer(3)
        pts = [(160, 520), (330, 620), (200, 740), (420, 800), (260, 880), (470, 660), (360, 540)]
        v.add(line(pts, 12), ROPE)
        for k in range(8):
            v.add(line([(200 + k * 36, 540 + (k % 3) * 60), (240 + k * 30, 800 - (k % 2) * 40)], 8), shade(ROPE, -0.1))
        v.add(ellipse(210, 520, 28, 28), "#b8453a")          # the float
        v.add(rect(446, 800, 44, 54, 6), IRON)               # the weight
    # workbench
    v.layer(3)
    v.rect(480, 700, 1000, 50, "#6e4b36", r=4)
    v.layer(2)
    v.rect(500, 750, 40, 250, "#33271e"); v.rect(1420, 750, 40, 250, "#33271e")
    v.rect(520, 800, 920, 24, "#33271e")
    # tackle box
    v.layer(4)
    v.rect(640, 612, 230, 100, "#8a3a2c", r=8)
    v.ink(rect(650, 628, 210, 8), "#c9a24d"); v.add(rect(740, 596, 50, 20, 8), IRON)
    # tar pot
    v.layer(4)
    v.add(poly([(950, 712), (1010, 712), (1040, 640), (920, 640)]), IRON)
    v.add(ellipse(980, 640, 62, 18), TAR)
    v.add(arc(980, 640, 62, 180, 360, 8), IRON)
    with v.sprite("tar_shine", show="fs('hung') == 'left'", shadow=False, fx="pulse"):
        v.layer(5)
        v.add(ellipse(970, 636, 28, 6), "#6a5a4a", ink=True)
    # a vise holding the small gear
    v.layer(4)
    v.rect(1190, 640, 120, 72, IRON, r=6); v.rect(1140, 700, 220, 18, IRON)
    with v.sprite("gear_s", show="not f('got_gear_s')"):
        v.layer(6)
        v.add(gear_shape(1250, 604, 40, 8, 13, spokes=False), "#b88a3a")
    # Pell in his pickle jar
    with v.sprite("jar_pell", show="not f('got_jar')", fx="bob"):
        v.layer(5)
        v.add(jar_shape(1340, 560, 130, 152), "#a9c6c6")
        v.ink(jar_shape(1350, 572, 110, 128), "#2f6f80")
        v.add(rect(1350, 546, 110, 18, 4), "#a8825a")
        pell_fish(v, 1405, 650, 0.5, facing=-1)
    # floor and a plank that sounds hollow
    v.layer(3)
    v.rect(0, 950, 1600, 50, "#2a1f18")
    v.ink(rect(300, 958, 170, 36, 3), "#3c2d22")
    with v.sprite("plank_open", show="f('plank_lifted')"):
        v.layer(4)
        v.rect(300, 952, 170, 48, "#0d0907")
        v.add(poly([(470, 954), (520, 930), (560, 940), (500, 975)]), "#3c2d22")
    with v.sprite("frag3", show="f('plank_lifted') and not f('got_frag3')"):
        v.layer(5)
        v.add(poly([(340, 968), (420, 960), (428, 990), (350, 996)]), "#d1c6a4")
        v.ink(rect(358, 972, 40, 14), "#6a6f69", d=5)
    v.hot("hook_left", (740, 110, 150, 120))
    v.hot("net_tangle", (140, 500, 380, 400), when="not f('got_net')")
    v.hot("tackle", (640, 590, 230, 130))
    v.hot("tar_pot", (910, 610, 150, 110))
    v.hot("bottle", (1130, 190, 260, 140))
    v.hot("jar", (1360, 580, 110, 150), when="not f('got_jar')")
    v.hot("gear_s", (1190, 560, 120, 100), when="not f('got_gear_s')")
    v.hot("plank", (280, 940, 210, 60), when="not f('plank_lifted')")
    v.hot("frag3", (320, 950, 130, 60), when="f('plank_lifted') and not f('got_frag3')")
    v.hot("bench", (480, 700, 1000, 60))
    v.hot("pegboard", (200, 200, 520, 280))
    return v

@view("c2_bh_back", CH)
def c2_bh_back():
    v = new("c2_bh_back", dark=wall_dark("back"), left="c2_bh_left", right="c2_bh_right")
    planks_wall(v, 0, 0, 1600, 1000, seed=5)
    beam_h(v, 0, 60, 1600, 50); post(v, 80, 0, 60, 1000); post(v, 1460, 0, 60, 1000)
    hook(v, 800, 170)
    hung_lantern(v, 836, 150, "back")
    v.light(836, 330, 1250, "#ffb860", when="fs('hung') == 'back'", intensity=1.1, flicker=0.05)
    # noticeboard with the tide table
    v.layer(2)
    v.rect(260, 220, 520, 420, "#5a4630", r=8)
    v.layer(3)
    v.rect(280, 240, 480, 380, "#8a6f4a", grad="#6f5a3a", r=4)
    paper_sheet(v, 320, 270, 220, 300, "#e0d6b6", ang=-2, d=4, lines=9, pin=True)
    paper_sheet(v, 580, 300, 150, 190, "#d6caa6", ang=3, d=4, lines=5, pin=True)
    v.add(ellipse(650, 540, 40, 40), "#b8453a", d=4)
    # winch with a big drum and crank
    v.layer(2)
    v.rect(980, 360, 420, 480, "#3b2c20", r=10)
    v.layer(3)
    v.rect(1010, 420, 360, 300, "#6e4b36", r=24)
    for k in range(7):
        v.ink(rect(1022 + k * 50, 424, 6, 292), "#4a3326")
    v.layer(4)
    v.add(ellipse(1190, 570, 100, 100), "#5b4430")
    v.add(ring(1190, 570, 100, 70), ROPE)
    v.add(ellipse(1190, 570, 28, 28), IRON)
    v.layer(3)
    v.rect(1000, 760, 380, 36, "#2f241a")
    # medium gear hanging on a nail
    v.layer(3)
    v.add(ellipse(850, 440, 8, 8), IRON)
    with v.sprite("gear_m", show="not f('got_gear_m')"):
        v.layer(5)
        v.add(gear_shape(850, 520, 70, 14, 14, spokes=False), "#b88a3a")
    # ropes + buoys
    rope_coil(v, 330, 820, 80, d=3)
    v.layer(3)
    v.add(ellipse(480, 780, 44, 44), "#b8453a"); v.add(ellipse(560, 800, 40, 40), "#dcb33c")
    v.layer(3)
    v.rect(0, 950, 1600, 50, "#2a1f18")
    v.hot("hook_back", (740, 110, 150, 120))
    v.hot("tide_board", (260, 220, 520, 420))
    v.hot("winch", (980, 360, 420, 480))
    v.hot("gear_m", (760, 440, 180, 180), when="not f('got_gear_m')")
    v.hot("ropes", (230, 730, 430, 150))
    return v

@view("c2_bh_right", CH)
def c2_bh_right():
    v = new("c2_bh_right", dark=wall_dark("right"), left="c2_bh_back", right="c2_bh_door")
    planks_wall(v, 0, 0, 1600, 1000, seed=6)
    beam_h(v, 0, 60, 1600, 50); post(v, 60, 0, 60, 1000); post(v, 1480, 0, 60, 1000)
    hook(v, 800, 170)
    hung_lantern(v, 836, 150, "right")
    v.light(836, 330, 1250, "#ffb860", when="fs('hung') == 'right'", intensity=1.1, flicker=0.05)
    # the slip: rails running down into the black pool
    v.layer(1)
    v.rect(0, 800, 1600, 200, WATER_T, grad=WATER_B)
    v.layer(2)
    v.rect(140, 760, 1320, 40, "#2f241a")
    v.rect(260, 520, 40, 280, "#3b2c20"); v.rect(1300, 480, 40, 320, "#3b2c20")
    # the boat in its cradle
    with v.sprite("boat", fx="lowerable"):
        v.layer(4)
        gunwale_boat(v)
        v.layer(5)
        v.add(rect(700, 440, 14, 110), "#4a3326")                           # mast stub
    with v.sprite("hull_patch", show="f('hull_ok')", fx="lowerable"):
        v.layer(7)
        v.add(ellipse(655, 658, 70, 56), "#1d1815")
        for k in range(4):
            v.ink(line([(600 + k * 26, 625), (610 + k * 26, 700)], 3), "#38302a", d=7)
    v.text("name", "", (900, 590, 300, 70), size=44, color="#e8d8a8", literal="AGNES", spacing=8, font="world")
    # lowering: water in front of the hull
    with v.sprite("water_front", show="f('boat_lowered')", shadow=False):
        v.layer(8)
        v.rect(120, 810, 1360, 190, "#1c3a46", grad="#0b1a21")
        v.ink(wave(120, 1480, 812, 5, 90, 5), "#3d6773", d=8)
    # chain from the bow ring to the post
    with v.sprite("chain", show="not f('chain_free')"):
        v.layer(6)
        for k in range(9):
            v.add(ring(1380 + k * 12, 560 + k * 10 + (k % 2) * 6, 11, 5), IRON)
        v.add(rect(1356, 640, 70, 60, 8), "#6e7274")
        v.add(ellipse(1391, 690, 22, 22), BRASS)
    with v.sprite("chain_fallen", show="f('chain_free')"):
        v.layer(6)
        for k in range(8):
            v.add(ring(1372 + k * 12, 840 + (k % 2) * 10, 11, 5), IRON, d=6)
    with v.sprite("crate_open", show="f('crate_open')"):
        v.layer(5)
        v.add(poly([(180, 700), (270, 640), (420, 640), (330, 700)]), "#6e4b36")
    # a crate to the left
    v.layer(4)
    v.rect(170, 700, 240, 200, "#6e4b36", r=4)
    for yy in (730, 790, 850):
        v.ink(rect(170, yy, 240, 8), "#4a3326", d=4)
    with v.sprite("gear_l", show="f('crate_open') and not f('got_gear_l')"):
        v.layer(6)
        v.add(gear_shape(290, 760, 100, 20, 14, spokes=False), "#b88a3a")
    v.layer(3)
    v.rect(0, 950, 1600, 50, "#2a1f18")
    v.hot("hook_right", (740, 110, 150, 120))
    v.hot("boat", (300, 440, 1050, 420))
    v.hot("hull_hole", (560, 570, 240, 260))
    v.hot("chain_lock", (1340, 540, 140, 200))
    v.hot("crate", (170, 640, 260, 260), when="not f('got_gear_l')")
    v.hot("gear_l", (190, 660, 200, 200), when="f('crate_open') and not f('got_gear_l')")
    return v

# ======================================================================= CLOSE-UPS
def cu_bg(v, c="#33271e", c2="#241a13"):
    planks_wall(v, 0, 0, 1600, 1000, base=c, dark=c2, pw=160, seed=9)

@view("c2_net", CH)
def c2_net():
    v = new("c2_net", dark="0.1", back="c2_bh_left")
    cu_bg(v)
    v.layer(1)
    v.rect(380, 170, 760, 760, "#2a2019", r=14)
    v.layer(2)
    v.rect(392, 182, 736, 736, "#3b2c20", r=10)
    # float on the left, weight on the right: one rope must run from one to the other
    v.layer(3)
    v.add(ellipse(300, 310, 66, 66), "#b8453a"); v.ink(rect(240, 298, 120, 10), "#f0e4c8", d=3)
    v.add(line([(330, 310), (410, 310)], 28), ROPE, d=3)
    v.add(rect(1180, 730, 120, 120, 14), IRON); v.add(arc(1240, 730, 38, 180, 360, 10), IRON)
    v.add(line([(1110, 790), (1200, 790)], 28), ROPE, d=3)
    v.hot("net_look", (380, 170, 760, 760))
    v.hot("net_item", (520, 330, 480, 340), when="f('net_untangled') and not f('got_net')")
    v.widget("tiles", "tiles", (400, 190, 720, 720), cell=240, origin=[400, 190], flag="net_untangled",
             tex_s="c2/c2_net_tile__tile_s.webp", tex_c="c2/c2_net_tile__tile_c.webp", tex_b="c2/c2_net_tile__tile_b.webp")
    with v.sprite("net_done", show="f('net_untangled') and not f('got_net')"):
        v.layer(6)
        v.add(rect(520, 330, 480, 340, 30), "#2a2019")
        for k in range(8):
            v.add(line([(545 + k * 62, 345), (545 + k * 62, 655)], 8), ROPE)
            v.add(line([(535, 360 + k * 42), (985, 360 + k * 42)], 8), ROPE)
        v.add(ellipse(760, 500, 12, 12), shade(ROPE, -0.2))
    return v

@view("c2_net_tile", CH)
def c2_net_tile():
    """tile art sheet: straight, corner (N-E), blank - rendered as sprites, 240x240 each"""
    v = View("c2_net_tile", CH, size=(1000, 300), kind="sheet", has_bg=False)
    for i, name in enumerate(("tile_s", "tile_c", "tile_b")):
        ox = 30 + i * 320
        with v.sprite(name, pad=2, shadow=False):
            v.layer(1)
            v.rect(ox, 30, 240, 240, "#4a3828", r=14)
            v.ink(rect(ox + 6, 36, 228, 228, 10), "#3b2c20", d=1)
            cx, cy = ox + 120, 150
            if name == "tile_s":
                pts = [(ox + 6, 150), (ox + 234, 150)]
                v.add(line(pts, 34), ROPE, d=2)
                twist(v, [(ox + 6, 150), (ox + 234, 150)], 34, d=2)
                v.add(ellipse(cx, cy, 24, 24), shade(ROPE, -0.18), d=2)
            elif name == "tile_c":
                # rope from the top edge (N) to the right edge (E): arc centred at the NE corner
                arcp = corner_pts(ox + 234, 36, 114, 90, 180)
                v.add(line(arcp, 34), ROPE, d=2)
                twist(v, arcp, 34, d=2)
                v.add(ellipse(arcp[7][0], arcp[7][1], 22, 22), shade(ROPE, -0.18), d=2)
            else:
                # a loose knot, connecting nothing
                v.add(ring(cx, cy, 52, 26), ROPE, d=2)
                v.add(ring(cx + 18, cy - 8, 40, 20), shade(ROPE, -0.12), d=2)
    return v

@view("c2_bottle", CH)
def c2_bottle():
    v = new("c2_bottle", dark="0.08", back="c2_bh_left")
    cu_bg(v, "#2b3a40", "#1a262b")
    v.layer(1)
    v.rect(0, 800, 1600, 200, "#4b3a2e", grad="#33271e")
    v.layer(2)
    v.rect(420, 740, 760, 60, "#6e4b36", r=8)                            # stand
    v.layer(3)
    v.add(union(ellipse(740, 560, 300, 170), rect(900, 500, 320, 110, 30)), "#8fb4b0")     # the bottle
    v.layer(4)
    v.add(union(ellipse(740, 560, 280, 152), rect(900, 516, 300, 78, 24)), "#b7d5d1")
    v.layer(5)
    v.ink(rect(470, 560, 470, 80), "#264a56", d=5)                       # painted sea inside
    v.ink(poly([(520, 640), (950, 640), (900, 590), (560, 590)]), "#3b6f7e", d=5)
    # the tiny ferry
    v.layer(6)
    v.add(poly([(580, 600), (900, 600), (860, 650), (620, 650)]), "#6a2331")
    v.add(rect(690, 540, 90, 60, 4), "#e6dcc0"); v.ink(rect(700, 552, 20, 20), "#264a56", d=6)
    v.add(rect(600, 470, 8, 130), "#2b2018")
    v.add(poly([(608, 480), (608, 590), (700, 590)]), "#e6dcc0")           # the sail
    with v.sprite("moth_bottle", show="not f('bottle_open')", fx="bob"):
        v.layer(8)
        moth(v, 650, 540, 0.75, glow=0.4)
    with v.sprite("cork", show="not f('bottle_open')"):
        v.layer(6)
        v.add(rect(1190, 530, 70, 50, 8), "#a8825a")
    with v.sprite("cork_out", show="f('bottle_open')"):
        v.layer(6)
        v.add(rot(rect(1280, 700, 70, 50, 8), 20), "#a8825a")
    v.hot("bottle_cork", (1170, 500, 120, 110), when="not f('bottle_open')")
    v.hot("ship", (520, 440, 420, 220))
    v.hot("bottle_glass", (460, 400, 780, 340))
    return v

@view("c2_tackle", CH)
def c2_tackle():
    v = new("c2_tackle", dark="0.08", back="c2_bh_left")
    cu_bg(v)
    v.layer(1)
    v.rect(240, 160, 1120, 700, "#8a3a2c", r=24)
    v.layer(2)
    v.rect(280, 200, 1040, 620, "#3b2018", r=16)
    for (tx, ty, tw, th_) in ((300, 220, 480, 280), (800, 220, 500, 280), (300, 520, 480, 280), (800, 520, 500, 280)):
        v.layer(3)
        v.rect(tx, ty, tw, th_, "#522a20", r=10)
    # hooks, lead weights, a spool
    v.layer(4)
    for k in range(5):
        v.add(arc(380 + k * 60, 300, 24, 200, 460, 6), IRON)
    for k in range(4):
        v.add(ellipse(870 + k * 70, 380, 22, 28), "#6e7274")
    v.add(rect(420, 600, 70, 140, 8), "#c9a24d"); v.add(ellipse(455, 670, 20, 20), "#3b2018")
    with v.sprite("rag", show="not f('got_rag')"):
        v.layer(5)
        v.add(poly([(340, 240), (520, 230), (560, 330), (520, 440), (400, 470), (330, 380)]), "#cfc4a3")
        v.ink(poly([(380, 270), (500, 262), (520, 330), (430, 420)]), "#bdb08c", d=5)
        v.ink(line([(360, 330), (480, 300)], 6), "#7a6b4a", d=5)
    with v.sprite("corkscrew", show="not f('got_corkscrew')"):
        v.layer(5)
        pts = [(900, 600 + k * 14) for k in range(1)]
        v.add(line([(900, 560), (900, 700)], 12), IRON)
        for k in range(5):
            v.add(line([(870 + (k % 2) * 60, 600 + k * 18), (930 - (k % 2) * 60, 612 + k * 18)], 9), IRON)
        v.add(rect(850, 530, 100, 22, 8), "#a8825a")
    v.hot("tackle_tray", (280, 200, 1040, 620))
    v.hot("rag", (320, 220, 260, 260), when="not f('got_rag')")
    v.hot("corkscrew", (840, 520, 130, 200), when="not f('got_corkscrew')")
    return v

@view("c2_tide", CH)
def c2_tide():
    v = new("c2_tide", dark="0.05", back="c2_bh_back")
    cu_bg(v)
    v.layer(1)
    v.rect(300, 60, 1000, 880, "#5a4630", r=14)
    v.layer(2)
    v.rect(330, 90, 940, 820, "#e2d8b8", grad="#d3c7a2", r=6)
    v.ink(rect(360, 200, 880, 4), "#5b4a35", d=2)
    v.text("title", "world.tide_title", (360, 110, 880, 80), size=54, color="#2b2118", font="world", spacing=4)
    rows = [("02:00", "131"), ("02:40", "139"), ("03:20", "150"), ("04:00", "165"), ("04:20", "172"), ("04:40", "181"), ("05:20", "196")]
    for i, (t, lv) in enumerate(rows):
        y = 230 + i * 92
        if t == "04:20":
            pass
        v.text(f"t{i}", "", (400, y, 300, 80), size=60, color="#2b2118", font="world", literal=t, align="left")
        v.text(f"l{i}", "", (800, y, 280, 80), size=60, color="#2b2118", font="world", literal=lv + " cm", align="left")
        v.ink(rect(380, y + 82, 840, 3), "#7b6a4a", d=2)
    v.text("foot", "world.tide_foot", (360, 860, 880, 50), size=28, color="#6a5a40", font="world")
    for i in range(7):
        v.hot(f"tide_r{i}", (360, 226 + i * 92, 880, 90))
    return v

@view("c2_winch", CH)
def c2_winch():
    v = new("c2_winch", dark="0.06", back="c2_bh_back")
    cu_bg(v)
    v.layer(1)
    v.rect(100, 180, 1400, 640, "#2f241a", r=14)
    v.layer(2)
    v.rect(130, 210, 1340, 580, "#3f3026", r=10)
    # the drum (right)
    v.layer(3)
    v.rect(1160, 250, 260, 500, "#6e4b36", r=30)
    for k in range(8):
        v.ink(rect(1172 + k * 31, 256, 6, 488), "#4a3326", d=3)
    v.add(line([(1290, 750), (1290, 900)], 18), ROPE, d=3)
    # axle plate and three pegs: crank (P0), middle (P1), drum (P2)
    v.layer(3)
    v.add(line([(330, 500), (1290, 500)], 40), "#2f241a")
    pegs = [(330, 500), (450, 500), (650, 500)]
    for (px, py) in pegs:
        v.layer(4)
        v.add(ellipse(px, py, 20, 20), IRON)
        v.add(ellipse(px, py, 8, 8), "#8a8e90", ink=True)
    # the drum's own peg and shaft
    v.add(line([(650, 500), (1160, 500)], 30), IRON, d=4)
    # crank on the far left
    v.layer(5)
    v.add(line([(330, 500), (230, 380)], 22), "#8a6a46")
    v.add(ellipse(222, 372, 30, 30), "#a68359")
    # gear sprites, placed on pegs by the game
    for nm, (r_, t_) in (("gear_s", (40, 8)), ("gear_m", (80, 16)), ("gear_l", (120, 24))):
        with v.sprite(nm, show="false", pivot=(330, 500), shadow=True):
            v.layer(6)
            v.add(gear_shape(330, 500, r_, t_, 14), "#b88a3a")
            v.ink(ring(330, 500, r_ * 0.35, r_ * 0.22), "#7a5a22", d=6)
    v.widget("gears", "gears", (130, 210, 1340, 580), pegs=pegs, sprites=["gear_s", "gear_m", "gear_l"])
    v.hot("peg_0", (270, 440, 120, 120))
    v.hot("peg_1", (390, 440, 120, 120))
    v.hot("peg_2", (590, 440, 120, 120))
    v.hot("crank", (150, 320, 160, 160))
    v.hot("drum", (1160, 250, 260, 500))
    return v

@view("c2_chain", CH)
def c2_chain():
    v = new("c2_chain", dark="0.06", back="c2_bh_right")
    cu_bg(v, "#2f241a", "#1d150f")
    v.layer(1)
    for k in range(8):
        v.add(ring(120 + k * 70, 150 + (k % 2) * 16, 34, 16), IRON)
    v.layer(2)
    v.rect(420, 240, 760, 600, "#6e7274", grad="#4a4e50", r=70)
    v.layer(3)
    v.rect(450, 270, 700, 540, "#3a3d3f", r=56)
    v.layer(4)
    v.add(arc(800, 240, 200, 180, 360, 54), "#8a8e90")
    cells = []
    for i in range(3):
        cx = 570 + i * 230
        v.layer(4)
        v.add(ellipse(cx, 540, 96), "#1a1a1c")
        v.add(ring(cx, 540, 100, 88), BRASS)
        cells.append([cx - 80, 460, 160, 160])
        v.ink(poly([(cx - 24, 378), (cx, 354), (cx + 24, 378)]), BRASS, d=4)
        v.ink(poly([(cx - 24, 702), (cx, 726), (cx + 24, 702)]), BRASS, d=4)
    v.widget("dials", "dials", (420, 330, 760, 420), cells=cells, digits=True, symbols=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
             solution=["1", "7", "2"], flag="chain_free", init=[4, 0, 8])
    v.hot("lock_body", (420, 240, 760, 600))
    return v

@view("c2_hull", CH)
def c2_hull():
    v = new("c2_hull", dark="0.06", back="c2_bh_right")
    cu_bg(v, "#2f241a", "#1d150f")
    v.layer(1)
    v.rect(200, 120, 1200, 760, "#8a5a36", grad="#6a4126", r=24)
    for k in range(1, 6):
        v.ink(rect(200, 120 + k * 126, 1200, 8), "#5a3820", d=1)
    v.layer(2)
    h = poly([(640, 430), (720, 360), (840, 350), (960, 400), (1000, 500), (960, 600), (860, 640), (740, 620), (660, 560)])
    v.add(h, "#070504")
    for (a, b) in (((640, 430), (610, 400)), ((960, 400), (1000, 360)), ((1000, 500), (1040, 520)), ((740, 620), (730, 670))):
        v.add(line([a, b], 14), "#6a4126", d=2)
    with v.sprite("hull_patch", show="f('hull_ok')"):
        v.layer(5)
        v.add(ellipse(820, 500, 260, 190), "#1d1815")
        for k in range(8):
            v.ink(line([(620 + k * 48, 360), (632 + k * 48, 640)], 4), "#38302a", d=5)
        v.ink(ellipse(820, 500, 250, 180), "#26201c", d=5)
    v.hot("hole", (600, 330, 440, 340))
    return v

@view("c2_boat", CH)
def c2_boat():
    v = new("c2_boat", dark="0.12", back="c2_bh_right")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#0e1f27", grad="#3d5e66")
    v.layer(1)
    v.rect(0, 560, 1600, 440, "#1c3a46", grad=WATER_B)
    # boat interior seen from the stern: two gunwales running ahead, the bow post and lamp
    v.layer(2)
    v.add(poly([(0, 1000), (520, 520), (1080, 520), (1600, 1000)]), "#8a5a36", grad="#5c3a22")
    for k in range(6):
        v.ink(line([(360 + k * 160, 1000), (570 + k * 92, 520)], 5), "#5a3820", d=2)
    v.layer(3)
    v.add(poly([(0, 1000), (0, 700), (520, 520), (560, 540), (150, 1000)]), "#a06a40")
    v.add(poly([(1600, 1000), (1600, 700), (1080, 520), (1040, 540), (1450, 1000)]), "#a06a40")
    v.layer(3)
    v.rect(0, 840, 1600, 70, "#6e4b36", r=4)              # thwart
    v.layer(4)
    v.rect(780, 330, 40, 240, "#4a3326")                  # bow post
    v.add(rect(740, 300, 120, 100, 14), "#1f2a2b")
    v.ink(rect(756, 316, 88, 68, 8), "#3c5a5c", d=4)
    with v.sprite("lamp_lit", show="f('bow_lamp')", shadow=False, fx="flicker"):
        v.layer(5)
        v.add(rect(756, 316, 88, 68, 8), "#f3cf84", glow=2.2)
        flame(v, 800, 372, 0.9, d=5)
    v.light(800, 350, 520, "#ffb860", when="f('bow_lamp')", intensity=1.1, flicker=0.06)
    # oarlocks
    v.layer(4)
    for (ox, nm) in ((200, "l"), (1400, "r")):
        v.add(rect(ox - 20, 720, 40, 70, 6), IRON); v.add(ring(ox, 716, 34, 18), IRON)
    with v.sprite("oar_l", show="f('oar_l')"):
        v.layer(6)
        v.add(line([(200, 716), (760, 640)], 22), "#8a6a46")
        v.add(rot(rect(60, 690, 190, 70, 30), -8), "#a68359")
    with v.sprite("oar_r", show="f('oar_r')"):
        v.layer(6)
        v.add(line([(1400, 716), (840, 640)], 22), "#8a6a46")
        v.add(rot(rect(1350, 690, 190, 70, 30), 8), "#a68359")
    # the boat's brass bell on the stern post
    v.layer(5)
    v.add(rect(60, 560, 18, 130), "#4a3326")
    v.add(union(ellipse(69, 660, 40, 36), rect(29, 650, 80, 30, 6)), BRASS)
    v.add(ellipse(69, 688, 9, 9), BRASS_D)
    v.hot("lock_l", (140, 660, 120, 160))
    v.hot("lock_r", (1340, 660, 120, 160))
    v.hot("bow_lamp", (730, 290, 140, 120))
    v.hot("boat_bell", (20, 590, 110, 120))
    v.hot("push_off", (640, 880, 320, 110))
    v.text("push", "world.push", (640, 892, 320, 90), size=36, color="#e8d8a8", font="world", spacing=4)
    return v
