"""Chapter 4 - The Far Light: the lighthouse in two states.  Now: cold, wrecked, raining.  Then: warm, lamp burning low, storm outside.
Every room is drawn twice from the same geometry (two background variants); sprites and hotspots are shared."""
import math
from pc import *
from reg import view
from kit import *

CH = "c4"
FLOOR_Y = 820

def pal(era):
    if era == "now":
        return dict(wall="#5b6a70", wall2="#3f4c52", joint="#2f3a3f", wood="#4d4540", wood2="#332c28", metal="#707577", rust="#8a5a3a",
                    glass_t="#a9bcc0", glass_b="#7f9498", floor="#2d3234", paper="#c9c3ad", cloth="#4e5a63", warm="#8a9ea3", ink="#1f2a2e")
    return dict(wall="#a37c4b", wall2="#7a5632", joint="#5b3e22", wood="#7b4a22", wood2="#4f2e12", metal="#cfa54d", rust="#b0773a",
                glass_t="#1b1a26", glass_b="#3a2f3f", floor="#4a2e16", paper="#e8d9ae", cloth="#7a2f2a", warm="#f3c76a", ink="#2a1a0c")

def new(id, **kw):
    v = View(id, CH, **kw)
    v.variants_when({"then": "era() == 'then'"}, "now")
    v.dark = "pick(era() == 'then', 0.28, 0.22)"
    v.ambient = "#3a4a58"
    return v

def both(v, fn):
    for era in ("now", "then"):
        with v.variant(era):
            fn(v, era, pal(era))

def shell(v, P, e, fy=FLOOR_Y):
    v.layer(0)
    v.rect(0, 0, 1600, 1000, P["wall"], grad=P["wall2"])
    rnd = random.Random(3)
    for k, y in enumerate(range(70, fy, 90)):
        v.ink(rect(0, y, 1600, 3), P["joint"])
        off = 0 if k % 2 == 0 else 70
        for x in range(off, 1600, 140):
            v.ink(rect(x, y, 3, 90), P["joint"])
    v.layer(1)
    v.rect(0, fy, 1600, 1000 - fy, P["floor"], grad=shade(P["floor"], -0.25))
    for k in range(10):
        v.ink(rect(k * 180 + 30, fy + 10, 3, 1000 - fy), shade(P["floor"], -0.3))
    v.layer(2)
    v.rect(0, fy - 26, 1600, 32, P["wood"])
    if e == "now":
        for _ in range(7):                                    # damp stains
            v.ink(ellipse(rnd.random() * 1600, 120 + rnd.random() * 500, 70 + rnd.random() * 120, 40 + rnd.random() * 50), shade(P["wall2"], -0.12))
    else:
        v.ink(rect(0, 0, 1600, 70), shade(P["wall2"], -0.25))

def window_arch(v, P, e, x, y, w, h, d=3):
    v.layer(d)
    v.add(union(rect(x - 20, y + w / 2, w + 40, h - w / 2 + 20), ellipse(x + w / 2, y + w / 2, w / 2 + 20, w / 2 + 20)), P["wood2"])
    v.layer(d + 1)
    g = union(rect(x, y + w / 2, w, h - w / 2), ellipse(x + w / 2, y + w / 2, w / 2, w / 2))
    v.add(g, P["glass_t"], grad=P["glass_b"])
    rnd = random.Random(int(x + y))
    if e == "now":
        for _ in range(14):
            sx = x + rnd.random() * w
            v.ink(line([(sx, y + 40 + rnd.random() * h * 0.5), (sx - 14, y + 110 + rnd.random() * h * 0.5)], 3), "#dfe9ea")
    else:
        for _ in range(16):
            sx = x + rnd.random() * w
            v.ink(line([(sx, y + 30 + rnd.random() * h * 0.6), (sx - 16, y + 100 + rnd.random() * h * 0.6)], 3), "#6c7a9a")
        # a flash of lightning on the far shore
        v.ink(poly([(x + w * 0.55, y + 20), (x + w * 0.4, y + h * 0.35), (x + w * 0.52, y + h * 0.35), (x + w * 0.36, y + h * 0.7), (x + w * 0.6, y + h * 0.3), (x + w * 0.48, y + h * 0.3)]), "#e8e4ff")
    v.ink(rect(x + w / 2 - 6, y + w / 2, 12, h - w / 2), P["wood2"], d=d + 2)
    v.ink(rect(x, y + h * 0.55, w, 12), P["wood2"], d=d + 2)
    v.layer(d + 1)
    v.rect(x - 30, y + h, w + 60, 24, P["wood"])

def stair_arrows(v):
    pass

def table(v, P, x, y, w, h=60, leg=14, d=3):
    v.layer(d)
    v.rect(x, y, w, 26, P["wood"], r=3)
    v.rect(x + 14, y + 26, leg, h, P["wood2"]); v.rect(x + w - 14 - leg, y + 26, leg, h, P["wood2"])

# ================================================================ the door
@view("c4_door", CH)
def c4_door():
    v = View("c4_door", CH)
    v.dark = "0.22"
    v.ambient = "#3a4a58"
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#8fa4a8", grad="#3d555d")
    rnd = random.Random(21)
    for _ in range(20):
        v.ink(ellipse(rnd.random() * 1600, 40 + rnd.random() * 300, 160 + rnd.random() * 200, 30 + rnd.random() * 24), "#a9bcc0")
    v.layer(1)
    v.rect(0, 800, 1600, 200, "#1d3a46", grad="#0b1a21")
    # the tower
    v.layer(2)
    v.add(poly([(480, 900), (580, 40), (1020, 40), (1120, 900)]), "#c9c3ad", grad="#9d9884")
    for k in range(6):
        v.ink(poly([(500 - k * 4, 120 + k * 130), (1100 + k * 4, 120 + k * 130), (1104 + k * 4, 170 + k * 130), (496 - k * 4, 170 + k * 130)]), "#8a3a30")
    v.layer(3)
    v.rect(590, 0, 420, 56, "#2b2018")
    v.layer(3)
    v.rect(660, 520, 280, 380, "#3b2c20", r=130)
    v.layer(4)
    v.rect(684, 548, 232, 352, "#5a4130", r=110)
    v.ink(rect(796, 548, 8, 352), "#33271e")
    v.add(ellipse(870, 720, 16, 16), BRASS)
    v.layer(5)
    v.rect(840, 690, 80, 70, "#2f2a28", r=8)
    v.layer(3)
    v.rect(0, 880, 1600, 120, "#4a4e50", grad="#2b2f31")
    # rain
    for _ in range(80):
        x = rnd.random() * 1600; y = rnd.random() * 880
        v.ink(line([(x, y), (x - 16, y + 60)], 3), "#d0dde0")
    with v.sprite("door_open", show="f('door_open')"):
        v.layer(6)
        v.rect(684, 548, 232, 352, "#120d09", r=110)
        v.add(poly([(684, 560), (630, 600), (630, 880), (684, 900)]), "#5a4130")
    v.hot("door_lock", (800, 660, 140, 140), when="not f('door_open')")
    v.hot("door", (684, 548, 232, 352), when="not f('door_open')")
    v.hot("enter", (684, 548, 232, 352), when="f('door_open')")
    v.hot("tower", (480, 40, 640, 500))
    v.hot("rocks", (0, 860, 500, 140))
    return v

# ================================================================ store room
@view("c4_store_a", CH)
def c4_store_a():
    v = new("c4_store_a", left="c4_store_b", right="c4_store_b")
    def draw(v, e, P):
        shell(v, P, e)
        window_arch(v, P, e, 1180, 150, 200, 380)
        # shelving
        v.layer(2)
        v.rect(180, 140, 760, 680, P["wood2"], r=6)
        for yy in (320, 520, 720):
            v.layer(3)
            v.rect(160, yy, 800, 24, P["wood"])
        # crates, jars, rope
        v.layer(3)
        for (cx, cy, cw, ch_) in ((200, 580, 170, 140), (390, 600, 130, 120), (580, 560, 220, 160)):
            v.rect(cx, cy, cw, ch_, shade(P["wood"], -0.1), r=3)
            v.ink(rect(cx, cy + ch_ * 0.4, cw, 8), P["wood2"], d=3)
        for k in range(5):
            v.add(jar_shape(210 + k * 90, 220, 60, 100), shade(P["glass_t"], 0.3 if e == "now" else 0.1))
        v.layer(3)
        v.rect(700, 740, 200, 80, P["rust"] if e == "now" else P["wood"], r=4)
        # barrel and a coil
        barrel(v, 1010, 600, 150, 220) if False else None
        v.layer(3)
        v.add(rect(1010, 600, 150, 220, 24), P["wood"])
        for k in (0.2, 0.5, 0.8):
            v.ink(rect(1010, 600 + 220 * k - 6, 150, 12), P["metal"])
    both(v, draw)
    # the tin on the top shelf (with the winding stem inside)
    with v.sprite("tin", show="not f('got_stem')"):
        v.layer(5)
        v.add(rect(520, 232, 120, 90, 8), "#8a3a2c")
        v.add(rect(514, 222, 132, 22, 6), "#c9a24d")
        v.ink(rect(536, 258, 88, 36, 4), "#e6dcc0", d=5)
    with v.sprite("tin_open", show="f('got_stem')"):
        v.layer(5)
        v.add(rect(520, 232, 120, 90, 8), "#8a3a2c")
        v.add(rot(rect(540, 190, 132, 22, 6), -28), "#c9a24d")
    with v.sprite("oilcan", show="era() == 'then' and not f('got_oilcan')"):
        v.layer(5)
        v.add(poly([(250, 520), (350, 520), (370, 440), (230, 440)]), "#a8abad")
        v.add(rect(290, 410, 20, 34), "#a8abad")
        v.add(line([(350, 470), (430, 420), (440, 380)], 12), "#a8abad")
        v.add(arc(250, 470, 34, 90, 270, 8), "#a8abad")
    v.hot("tin", (500, 190, 170, 140), when="not f('got_stem')")
    v.hot("shelf", (160, 130, 800, 700))
    v.hot("oilcan", (220, 400, 240, 140), when="era() == 'then' and not f('got_oilcan')")
    v.hot("barrel", (1000, 590, 170, 240))
    v.hot("window_s", (1160, 130, 240, 420))
    return v

@view("c4_store_b", CH)
def c4_store_b():
    v = new("c4_store_b", left="c4_store_a", right="c4_store_a")
    def draw(v, e, P):
        shell(v, P, e)
        # the stair, rising to the right across the wall
        v.layer(2)
        v.add(poly([(260, 820), (1500, 120), (1500, 190), (330, 880)]), P["wood2"])
        for k in range(9):
            sx = 330 + k * 130
            sy = 790 - k * 74
            v.layer(3)
            v.rect(sx, sy, 150, 34, P["wood"], r=3)
            v.ink(rect(sx, sy + 28, 150, 6), shade(P["wood"], -0.3), d=3)
        v.layer(3)
        v.line([(300, 760), (1480, 70)], 16, P["metal"]) if False else None
        window_arch(v, P, e, 240, 120, 170, 300)
    both(v, draw)
    v.hot("stairs_up", (700, 420, 800, 440))
    v.hot("stairs_look", (300, 740, 380, 200))
    v.hot("window_s2", (220, 100, 210, 340))
    return v

@view("c4_stairs", CH)
def c4_stairs():
    v = new("c4_stairs", back="c4_store_b")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        for k in range(6):
            v.layer(2)
            sy = 760 - k * 120
            v.rect(120 + k * 70, sy, 1360 - k * 70, 80, P["wood"], r=4)
            v.ink(rect(120 + k * 70, sy + 70, 1360 - k * 70, 10), shade(P["wood"], -0.35), d=2)
            v.layer(1)
            v.rect(120 + k * 70, sy + 80, 1360 - k * 70, 40, P["wood2"])
        v.layer(3)
        v.ink(rect(300, 640, 520, 8), shade(P["wood"], -0.3), d=3)
    both(v, draw)
    with v.sprite("step_open", show="f('step_lifted')"):
        v.layer(4)
        v.rect(500, 520, 520, 90, "#0d0907", r=4)
        v.add(rot(rect(420, 440, 520, 50, 4), -14), "#7a5a3a")
    with v.sprite("frag7", show="f('step_lifted') and not f('got_frag7')"):
        v.layer(5)
        v.add(poly([(700, 540), (800, 530), (810, 575), (712, 585)]), "#d1c6a4")
        v.ink(rect(722, 548, 54, 18), "#6a6f69", d=5)
    v.hot("step_odd", (440, 500, 640, 140), when="not f('step_lifted')")
    v.hot("frag7", (680, 510, 150, 90), when="f('step_lifted') and not f('got_frag7')")
    v.hot("stair_steps", (120, 200, 1360, 700))
    return v

@view("c4_tin", CH)
def c4_tin():
    v = new("c4_tin", back="c4_store_a")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        v.layer(1)
        v.rect(0, 760, 1600, 240, P["wood"])
    both(v, draw)
    v.layer(2)
    v.rect(420, 360, 760, 420, "#8a3a2c", r=24)
    v.layer(3)
    v.rect(450, 400, 700, 340, "#3b1a14", r=14)
    with v.sprite("tin_lid"):
        v.layer(5)
        v.add(rot(rect(480, 160, 740, 120, 20), -6), "#a8764a")
        v.ink(rot(rect(540, 190, 600, 50, 8), -6), "#e6dcc0", d=5)
    # odds and ends in the tin, and the brass winding stem among them
    v.layer(4)
    v.add(ellipse(560, 560, 30, 30), "#8a8e90"); v.add(ellipse(720, 640, 26, 26), "#8a8e90")
    v.add(line([(900, 480), (1040, 650)], 12), "#8a8e90")
    v.add(rect(590, 450, 100, 40, 4), "#6e7274")
    with v.sprite("stem", show="not f('got_stem')"):
        v.layer(6)
        v.add(rect(760, 520, 160, 22, 8), BRASS)
        v.add(ellipse(930, 531, 26, 26), BRASS)
        v.add(rect(740, 514, 28, 34, 6), BRASS_D)
    v.hot("stem", (720, 480, 260, 110), when="not f('got_stem')")
    v.hot("tin_inside", (420, 360, 760, 420))
    return v

# ================================================================ quarters
@view("c4_quarters_a", CH)
def c4_quarters_a():
    v = new("c4_quarters_a", left="c4_quarters_b", right="c4_quarters_b")
    def draw(v, e, P):
        shell(v, P, e)
        window_arch(v, P, e, 1080, 140, 220, 400)
        # the bed (iron frame, thin blanket)
        v.layer(2)
        v.rect(140, 520, 760, 60, P["metal"] if e == "then" else P["rust"], r=6)
        v.rect(140, 440, 36, 400, P["metal"] if e == "then" else P["rust"]); v.rect(864, 480, 36, 360, P["metal"] if e == "then" else P["rust"])
        v.layer(3)
        v.rect(180, 540, 680, 200, P["cloth"], r=14)
        v.ink(rect(180, 600, 680, 10), shade(P["cloth"], -0.25), d=3)
        v.rect(190, 500, 220, 70, P["paper"], r=18)
        if e == "now":
            v.ink(poly([(260, 560), (340, 640), (420, 590), (500, 700)]), shade(P["cloth"], -0.25), d=3)
        # bedside table
        table(v, P, 960, 620, 260, 190)
        # a trunk
        v.layer(3)
        v.rect(1300, 700, 220, 120, P["wood"], r=6); v.ink(rect(1300, 740, 220, 10), P["metal"], d=3)
    both(v, draw)
    with v.sprite("watch", show="not f('got_watch')"):
        v.layer(5)
        v.add(ellipse(1090, 590, 40, 40), BRASS)
        v.add(ellipse(1090, 590, 31, 31), "#e8dec2")
        v.ink(line([(1090, 590), (1090, 568)], 4), INK, d=5); v.ink(line([(1090, 590), (1106, 598)], 4), INK, d=5)
        v.add(ring(1090, 540, 14, 8), BRASS)
    v.hot("watch", (1030, 520, 120, 120), when="not f('got_watch')")
    v.hot("bed", (140, 430, 780, 400))
    v.hot("bedside", (950, 610, 280, 220))
    v.hot("trunk", (1290, 690, 240, 140))
    v.hot("window_q", (1060, 120, 260, 440))
    return v

@view("c4_quarters_b", CH)
def c4_quarters_b():
    v = new("c4_quarters_b", left="c4_quarters_a", right="c4_quarters_a")
    def draw(v, e, P):
        shell(v, P, e)
        # chest of drawers
        v.layer(2)
        v.rect(160, 440, 520, 380, P["wood"], r=6)
        for k in range(3):
            v.layer(3)
            v.rect(180, 462 + k * 118, 480, 100, shade(P["wood"], 0.08), r=5)
            v.add(ellipse(420, 512 + k * 118, 14, 14), P["metal"] if e == "then" else P["rust"])
        if e == "now":
            for k in range(5):
                v.ink(ellipse(260 + k * 80, 500 + (k % 3) * 100, 20, 14), P["rust"], d=3)
        # calendar on the wall
        v.layer(2)
        v.rect(840, 200, 260, 330, P["paper"], r=3)
        v.layer(3)
        v.rect(840, 200, 260, 70, P["cloth"])
        for r_ in range(5):
            for c_ in range(6):
                v.ink(rect(858 + c_ * 36, 300 + r_ * 38, 24, 4), P["ink"], d=3)
        # wardrobe
        v.layer(2)
        v.rect(1240, 160, 300, 660, P["wood2"], r=6)
        v.layer(3)
        v.rect(1260, 190, 120, 600, P["wood"], r=4); v.rect(1400, 190, 120, 600, P["wood"], r=4)
        v.add(ellipse(1372, 500, 10, 10), P["metal"]); v.add(ellipse(1408, 500, 10, 10), P["metal"])
    both(v, draw)
    with v.sprite("cal_circle", show="era() == 'then'", shadow=False):
        v.layer(4)
        v.ink(ring(990, 470, 20, 15), "#a33a30", d=4)
    v.hot("drawer", (180, 580, 480, 120))
    v.hot("chest", (160, 440, 520, 380))
    v.hot("calendar", (840, 200, 260, 330))
    v.hot("wardrobe", (1240, 160, 300, 660))
    v.hot("stairs_up", (720, 380, 90, 440))
    v.hot("stairs_down", (720, 700, 90, 120))
    return v

@view("c4_drawer", CH)
def c4_drawer():
    v = new("c4_drawer", back="c4_quarters_b")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        v.layer(1)
        v.rect(160, 200, 1280, 600, P["wood"], r=10)
        v.layer(2)
        if e == "now":
            v.rect(200, 240, 1200, 520, P["wood2"], r=6)
            for k in range(9):
                v.ink(ellipse(260 + k * 130, 330 + (k % 4) * 120, 50 + (k % 3) * 14, 22), P["rust"], d=2)
            v.ink(rect(200, 470, 1200, 16), "#4a2a18", d=2)
        else:
            v.rect(200, 240, 1200, 520, shade(P["wood2"], -0.3), r=6)
            v.layer(3)
            v.rect(240, 280, 1120, 440, P["cloth"], r=8)
    both(v, draw)
    with v.sprite("chain", show="era() == 'then' and not f('got_chain')"):
        v.layer(6)
        for k in range(12):
            v.add(ring(560 + k * 40, 500 + math.sin(k * 0.7) * 24, 20, 9), "#8a8e90")
    v.hot("drawer_now", (200, 240, 1200, 520), when="era() == 'now'")
    v.hot("chain", (540, 440, 520, 120), when="era() == 'then' and not f('got_chain')")
    v.hot("drawer_then", (200, 240, 1200, 520), when="era() == 'then' and f('got_chain')")
    return v

@view("c4_calendar", CH)
def c4_calendar():
    v = new("c4_calendar", back="c4_quarters_b")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        v.layer(1)
        v.rect(420, 60, 760, 880, P["paper"], r=6)
        v.layer(2)
        v.rect(420, 60, 760, 160, P["cloth"])
        for r_ in range(5):
            for c_ in range(7):
                v.ink(rect(470 + c_ * 100, 290 + r_ * 110, 64, 8), P["ink"], d=2)
        if e == "now":
            v.ink(poly([(420, 60), (700, 60), (560, 300), (420, 220)]), P["wall2"], d=3)    # a torn corner
            for _ in range(10):
                v.ink(ellipse(430 + random.random() * 700, 100 + random.random() * 800, 40, 24), shade(P["paper"], -0.15), d=2)
    both(v, draw)
    with v.sprite("cal_page", show="era() == 'then' and not f('cal_lifted')"):
        v.layer(4)
        v.rect(450, 330, 700, 560, "#efe2b8", r=4)
        for r_ in range(4):
            for c_ in range(7):
                v.ink(rect(490 + c_ * 96, 380 + r_ * 100, 60, 8), "#2a1a0c", d=4)
        v.ink(ring(682, 574, 42, 32), "#a33a30", d=4)
    with v.sprite("cal_page_up", show="era() == 'then' and f('cal_lifted')"):
        v.layer(4)
        v.add(poly([(450, 330), (1150, 300), (1170, 420), (470, 480)]), "#efe2b8")
    with v.sprite("frag8", show="era() == 'now' and f('cal_lifted') and not f('got_frag8')"):
        v.layer(4)
        v.add(poly([(560, 520), (700, 508), (712, 590), (572, 604)]), "#d1c6a4")
        v.ink(rect(584, 536, 90, 34), "#6a6f69", d=4)
        v.add(ellipse(630, 514, 8, 8), "#9a2d2d")
    v.hot("cal_page", (450, 330, 700, 560), when="era() == 'then' and not f('cal_lifted')")
    v.hot("cal_behind", (450, 300, 700, 580), when="era() == 'then' and f('cal_lifted')")
    v.hot("cal_now", (420, 60, 760, 880), when="era() == 'now' and not f('cal_lifted')")
    v.hot("frag8", (540, 490, 200, 130), when="era() == 'now' and f('cal_lifted') and not f('got_frag8')")
    v.text("cal_title", "world.cal_month", (440, 70, 720, 140), size=70, color="#efe2b8", font="world", spacing=6)
    return v

# ================================================================ watch room
@view("c4_watch_a", CH)
def c4_watch_a():
    v = new("c4_watch_a", left="c4_watch_b", right="c4_watch_b")
    def draw(v, e, P):
        shell(v, P, e)
        window_arch(v, P, e, 1160, 150, 240, 420)
        # the desk and the logbook
        table(v, P, 260, 560, 560, 220, 22)
        v.layer(4)
        v.rect(300, 540, 220, 24, P["paper"], r=3)
        # lamp on the desk
        v.layer(4)
        v.rect(700, 480, 50, 60, P["metal"], r=6)
        v.add(poly([(690, 480), (760, 480), (740, 430), (710, 430)]), P["metal"])
        # the watch-chair, facing the window
        v.layer(3)
        v.rect(900, 520, 150, 20, P["wood"]); v.rect(900, 540, 14, 270, P["wood2"]); v.rect(1036, 540, 14, 270, P["wood2"])
        v.rect(900, 360, 150, 170, P["wood"], r=10)
        v.ink(rect(916, 380, 118, 120, 6), shade(P["wood"], 0.12), d=3)
    both(v, draw)
    with v.sprite("logbook", d=5):
        v.layer(5)
        v.add(rot(rect(310, 516, 200, 40, 3), 0), "#3a4a52")
        v.ink(rect(310, 526, 200, 6), "#c9a24d", d=5)
    with v.sprite("sleeper_a", show="era() == 'then'"):
        v.layer(5)
        v.add(poly([(924, 540), (1030, 540), (1020, 380), (940, 380)]), "#3a4a5a")         # coat, from behind
        v.add(ellipse(982, 360, 46, 52), "#2b2018")
        v.add(ellipse(982, 372, 30, 26), "#d6a98a")
    v.light(725, 450, 380, "#ffb050", when="era() == 'then'", intensity=0.7, flicker=0.08)
    v.hot("logbook", (290, 490, 250, 80))
    v.hot("desk_w", (250, 560, 580, 260))
    v.hot("chair", (890, 340, 180, 480))
    v.hot("window_w", (1130, 130, 300, 460))
    v.hot("lamp_desk", (680, 420, 100, 130))
    return v

@view("c4_logbook", CH)
def c4_logbook():
    v = new("c4_logbook", back="c4_watch_a")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wood"], grad=P["wood2"])
        v.layer(1)
        v.rect(260, 60, 1080, 880, "#2b3a42" if e == "now" else "#4a2a1a", r=14)
        if e == "then":
            v.layer(2)
            v.rect(290, 90, 520, 820, "#e9dcb4", r=6); v.rect(790, 90, 520, 820, "#efe2ba", r=6)
            v.ink(rect(794, 90, 8, 820), "#8a7a5a", d=2)
        else:
            v.layer(2)
            v.rect(290, 90, 520, 820, "#c2bca5", r=6)
            v.rect(790, 90, 520, 820, "#4a5a62", r=6)             # the right page is gone: torn out
            for k in range(14):
                v.ink(poly([(790, 100 + k * 56), (810 + (k % 3) * 10, 112 + k * 56), (790, 130 + k * 56)]), "#c2bca5", d=2)
            for r_ in range(10):
                v.ink(rect(320, 150 + r_ * 70, 440 - (r_ % 4) * 40, 6), "#6a6a5a", d=2)
    both(v, draw)
    v.text("log_h", "world.log_head", (830, 100, 460, 60), size=38, color="#2a1a0c", font="world", spacing=3, when="era() == 'then'")
    v.text("log_1", "world.log_1", (840, 170, 440, 120), size=27, color="#2a1a0c", font="world", align="left", when="era() == 'then'")
    v.text("log_2", "world.log_2", (840, 300, 440, 160), size=27, color="#2a1a0c", font="world", align="left", when="era() == 'then'")
    v.text("log_3", "world.log_3", (840, 560, 440, 120), size=27, color="#2a1a0c", font="world", align="left", when="era() == 'then'")
    v.text("log_4", "world.log_4", (840, 700, 440, 130), size=27, color="#2a1a0c", font="world", align="left", when="era() == 'then'")
    v.text("log_old", "world.log_old", (310, 110, 480, 60), size=34, color="#3a3a30", font="world", spacing=2, when="era() == 'now'")
    v.hot("log_page", (790, 90, 520, 820), when="era() == 'then'")
    v.hot("log_torn", (790, 90, 520, 820), when="era() == 'now'")
    v.hot("log_left", (290, 90, 520, 820))
    return v

@view("c4_sleeper", CH)
def c4_sleeper():
    v = new("c4_sleeper", back="c4_watch_a")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        window_arch(v, P, e, 1050, 100, 340, 560)
        v.layer(2)
        v.rect(0, 760, 1600, 240, P["floor"])
        # the chair seen from behind
        v.layer(3)
        v.rect(420, 280, 480, 560, P["wood"], r=40)
        v.layer(4)
        v.rect(460, 320, 400, 480, shade(P["wood"], 0.1), r=30)
        if e == "now":
            for k in range(6):
                v.ink(line([(480 + k * 60, 340), (500 + k * 60, 790)], 3), shade(P["wood"], -0.3), d=4)
    both(v, draw)
    with v.sprite("sleeper_body", show="era() == 'then'"):
        v.layer(6)
        v.add(poly([(480, 800), (500, 480), (560, 400), (780, 400), (830, 480), (850, 800)]), "#3a4a5a")        # coat, slumped
        v.ink(poly([(520, 520), (800, 520), (780, 800), (540, 800)]), "#2f3d4b", d=6)
        v.add(rect(430, 640, 80, 200, 20), "#3a4a5a")              # arm over the chair
    with v.sprite("sleeper_head", pivot=(660, 370), show="era() == 'then'", fx=None):
        v.layer(7)
        v.add(ellipse(660, 340, 76, 84), "#2b2018")                 # hair, from behind
        v.add(ellipse(660, 292, 36, 36), "#2b2018")                 # a bun
    with v.sprite("sleeper_face", show="era() == 'then' and f('sleeper_turned')"):
        v.layer(8)
        v.add(ellipse(660, 350, 66, 76), "#d6a98a")
        v.ink(ellipse(632, 340, 12, 7), "#ffffff", d=8); v.ink(ellipse(688, 340, 12, 7), "#ffffff", d=8)
        v.ink(ellipse(632, 340, 6, 6), INK, d=8); v.ink(ellipse(688, 340, 6, 6), INK, d=8)
        v.ink(line([(640, 392), (680, 392)], 5), "#8a4a3a", d=8)
        v.ink(arc(660, 300, 70, 190, 350, 12), "#2b2018", d=8)
    v.light(1220, 360, 520, "#ffb050", when="era() == 'then'", intensity=0.6, flicker=0.1)
    v.hot("sleeper", (420, 260, 460, 580), when="era() == 'then'")
    v.hot("chair_empty", (420, 260, 460, 580), when="era() == 'now'")
    v.hot("window_sl", (1020, 80, 400, 600))
    return v

# ================================================================ watch room B: the valves
@view("c4_watch_b", CH)
def c4_watch_b():
    v = new("c4_watch_b", left="c4_watch_a", right="c4_watch_a")
    def draw(v, e, P):
        shell(v, P, e)
        # pipes rising into the lamp room
        v.layer(2)
        for px in (540, 700, 860):
            v.rect(px - 22, 0, 44, 520, P["metal"] if e == "then" else shade(P["metal"], -0.1), r=6)
            v.ink(rect(px - 22, 120, 44, 10), shade(P["metal"], -0.3), d=2)
        v.layer(3)
        v.rect(420, 480, 560, 260, P["wood2"], r=10)             # valve board
        v.layer(4)
        v.rect(436, 496, 528, 228, P["wood"], r=6)
        for k, px in enumerate((540, 700, 860)):
            v.add(ring(px, 610, 54, 14), P["metal"] if (e == "then" or k != 1) else P["rust"])
            for a in range(0, 360, 60):
                v.add(line([(px, 610), (px + 48 * math.cos(math.radians(a)), 610 + 48 * math.sin(math.radians(a)))], 8), P["metal"] if (e == "then" or k != 1) else P["rust"])
        window_arch(v, P, e, 1180, 160, 200, 360)
        v.layer(3)
        v.rect(1100, 620, 380, 200, P["wood2"], r=6)
        v.layer(4)
        v.rect(1130, 660, 120, 120, P["metal"], r=60); v.rect(1280, 660, 160, 120, P["wood"], r=6)
    both(v, draw)
    v.hot("valves", (420, 480, 560, 260))
    v.hot("pipe", (500, 0, 400, 480))
    v.hot("window_wb", (1160, 140, 240, 400))
    v.hot("stairs_up", (1100, 620, 380, 220))
    v.hot("stairs_down", (60, 600, 260, 220))
    return v

@view("c4_valves", CH)
def c4_valves():
    v = new("c4_valves", back="c4_watch_b")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        v.layer(1)
        v.rect(150, 200, 1300, 600, P["wood2"], r=20)
        v.layer(2)
        v.rect(180, 230, 1240, 540, P["wood"], r=14)
        for k, px in enumerate((420, 800, 1180)):
            v.layer(3)
            v.add(ring(px, 500, 150, 100), P["metal"] if (e == "then" or k != 1) else P["rust"])
            v.add(ellipse(px, 500, 100), P["wood2"])
            v.layer(4)
            for a in range(0, 360, 45):
                v.add(line([(px, 500), (px + 138 * math.cos(math.radians(a)), 500 + 138 * math.sin(math.radians(a)))], 12), P["metal"] if (e == "then" or k != 1) else P["rust"])
            v.ink(ellipse(px, 500, 22, 22), shade(P["metal"], -0.3), d=4)
        if e == "now":
            v.ink(ellipse(800, 440, 70, 40), P["rust"], d=5)
    both(v, draw)
    cells = [[420 - 100, 400, 200, 200], [800 - 100, 400, 200, 200], [1180 - 100, 400, 200, 200]]
    v.widget("valves", "valves", (180, 230, 1240, 540), cells=cells, flag="valves_ok", solution=[3, 1, 4], seized=1)
    v.hot("valve_board", (150, 200, 1300, 600))
    return v

# ================================================================ lamp room
@view("c4_lamp_a", CH)
def c4_lamp_a():
    v = new("c4_lamp_a", left="c4_lamp_b", right="c4_lamp_b")
    def draw(v, e, P):
        shell(v, P, e, fy=860)
        # the big seaward window
        window_arch(v, P, e, 1040, 100, 420, 600)
        # the lens: a drum of prisms around the flame
        v.layer(2)
        v.add(ellipse(520, 460, 300), P["metal"] if e == "then" else shade(P["metal"], -0.1))
        v.layer(3)
        v.add(ellipse(520, 460, 270), P["glass_b"] if e == "then" else "#8fa4a8")
        for k in range(12):
            a = math.radians(k * 30)
            v.ink(line([(520 + 90 * math.cos(a), 460 + 90 * math.sin(a)), (520 + 260 * math.cos(a), 460 + 260 * math.sin(a))], 5), P["metal"], d=3)
        for r_ in (110, 180, 245):
            v.ink(ring(520, 460, r_, r_ - 5), P["metal"], d=3)
        v.layer(4)
        v.rect(390, 700, 260, 160, P["wood"], r=8)       # the lamp table
    both(v, draw)
    with v.sprite("wick_flame", show="f('lamp_lit')", fx="flicker", shadow=False):
        v.layer(6)
        flame(v, 520, 480, 2.4, d=6)
    with v.sprite("wick", show="not f('lamp_lit')"):
        v.layer(6)
        v.add(rect(500, 440, 40, 130, 6), "#6e7274")
        v.ink(rect(516, 410, 8, 34), INK, d=6)
    with v.sprite("oil_level", show="f('valves_ok')", shadow=False):
        v.layer(6)
        v.add(rect(430, 560, 180, 30, 8), "#c0a038", ink=True)
    v.light(520, 460, 700, "#ffb860", when="f('lamp_lit')", intensity=1.2, flicker=0.05)
    v.light(520, 480, 420, "#ffb050", when="era() == 'then' and not f('lamp_lit')", intensity=0.5, flicker=0.1)
    v.hot("lens", (240, 200, 560, 520))
    v.hot("wick", (460, 400, 120, 220))
    v.hot("window_sea", (1010, 80, 480, 640))
    v.hot("oil_tank", (400, 690, 240, 180))
    v.hot("stairs_down", (100, 600, 220, 260))
    return v

@view("c4_lamp_b", CH)
def c4_lamp_b():
    v = new("c4_lamp_b", left="c4_lamp_a", right="c4_lamp_a")
    def draw(v, e, P):
        shell(v, P, e, fy=860)
        window_arch(v, P, e, 120, 120, 200, 380)
        # clockwork frame with weights on chains
        v.layer(2)
        v.rect(560, 140, 640, 640, P["wood2"], r=10)
        v.layer(3)
        v.rect(590, 170, 580, 580, P["wood"], r=6)
        for (cx, cy, r_) in ((760, 340, 90), (980, 420, 130), (780, 590, 70)):
            v.layer(4)
            v.add(gear_like(cx, cy, r_), P["metal"] if e == "then" else shade(P["metal"], -0.1))
        for x in (1260, 1360):
            v.layer(3)
            v.rect(x, 80, 8, 620, P["metal"] if e == "then" else shade(P["metal"], -0.2))
        v.layer(4)
        v.rect(1230, 640, 70, 150, "#4a4e50", r=6); v.rect(1330, 640, 70, 150, "#4a4e50", r=6)
        if e == "now":
            v.ink(line([(1360, 90), (1362, 330)], 8), P["metal"], d=3)
    both(v, draw)
    with v.sprite("chain_broken", show="not f('chain_fixed')", shadow=False):
        v.layer(5)
        for k in range(5):
            v.add(ring(1362, 100 + k * 46, 14, 6), "#8a8e90")
        v.add(line([(1362, 300), (1380, 330), (1354, 350)], 8), "#8a8e90")
    with v.sprite("chain_new", show="f('chain_fixed')", shadow=False):
        v.layer(5)
        for k in range(14):
            v.add(ring(1362, 100 + k * 40, 14, 6), "#a8abad")
    v.hot("chain_mech", (1220, 60, 220, 760))
    v.hot("clockwork", (560, 140, 640, 640))
    v.hot("window_lb", (100, 100, 240, 420))
    return v

def gear_like(cx, cy, r, teeth=14):
    pts = []
    pitch = 2 * math.pi / teeth
    for i in range(teeth):
        a = i * pitch
        for f, rr in ((0.0, r - 8), (0.2, r + 8), (0.5, r + 8), (0.7, r - 8)):
            ang = a + f * pitch
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    return Polygon(pts).buffer(0).difference(ellipse(cx, cy, r * 0.3))

@view("c4_chain", CH)
def c4_chain():
    v = new("c4_chain", back="c4_lamp_b")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, P["wall2"], grad=shade(P["wall2"], -0.3))
        v.layer(1)
        v.rect(200, 120, 1200, 760, P["wood2"], r=14)
        v.layer(2)
        v.add(gear_like(560, 400, 220, 18), P["metal"] if e == "then" else shade(P["metal"], -0.1))
        v.add(gear_like(960, 560, 150, 12), P["metal"] if e == "then" else shade(P["rust"], 0.0))
        v.layer(3)
        v.rect(1180, 140, 24, 700, "#3a3d3f")
    both(v, draw)
    with v.sprite("chain_new", show="f('chain_fixed')", shadow=False):
        v.layer(6)
        for k in range(15):
            v.add(ring(1192, 160 + k * 46, 18, 8), "#a8abad")
    with v.sprite("chain_broken", show="not f('chain_fixed')", shadow=False):
        v.layer(6)
        for k in range(5):
            v.add(ring(1192, 160 + k * 46, 18, 8), "#8a8e90")
        v.add(line([(1192, 380), (1230, 420), (1180, 450)], 10), "#8a8e90")
        v.add(ring(1180, 470, 14, 6), "#8a8e90", d=6)
    v.hot("chain_break", (1090, 140, 220, 700))
    v.hot("gears_look", (320, 160, 800, 600))
    return v

@view("c4_lens", CH)
def c4_lens():
    v = new("c4_lens", back="c4_lamp_a")
    def draw(v, e, P):
        v.layer(0)
        v.rect(0, 0, 1600, 1000, "#10181c", grad="#1b262c")
        v.layer(1)
        v.rect(300, 160, 780, 780, P["metal"] if e == "then" else shade(P["metal"], -0.1), r=24)
        v.layer(2)
        v.rect(330, 190, 720, 720, "#0b1013", r=14)
        for i in range(4):
            v.ink(rect(330 + i * 240 - 3, 190, 6, 720), "#2a363c", d=2)
            v.ink(rect(330, 190 + i * 240 - 3, 720, 6), "#2a363c", d=2)
        # the flame at the west edge and the seaward window at the NE
        v.layer(3)
        v.add(rect(210, 520, 100, 140, 8), "#3a3d3f")
        v.add(poly([(1050, 190), (1180, 150), (1180, 420), (1050, 430)]), "#2f4a54")
    both(v, draw)
    v.text("lens_in", "world.lens_flame", (150, 680, 200, 40), size=20, color="#e6dcc0", font="world")
    v.text("lens_out", "world.lens_sea", (1090, 100, 300, 40), size=20, color="#e6dcc0", font="world")
    v.widget("beam", "beam", (330, 190, 720, 720), cell=240, origin=[330, 190], flag="lens_ok", source=[210, 590])
    v.hot("lens_look", (300, 160, 780, 780))
    return v
