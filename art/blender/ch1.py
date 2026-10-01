"""Chapter 1 - The Keeper's Room.  Four walls + close-ups.  Expressions are Godot-side (f('flag'), has('item'))."""
import math
from pc import *
from reg import view
from kit import *

CH = "c1"
WALL_T, WALL_B = "#4b6c68", "#3c5855"
DARK = "pick(f('lantern_placed'), 0.2, 0.46)"
AMBIENT = "#3a4d5c"

def new(id, **kw):
    v = View(id, CH, **kw)
    v.dark = DARK
    v.ambient = AMBIENT
    return v

def wallpaper(v, h=720, c=WALL_B):
    v.layer(0)
    for x in range(40, 1600, 90):
        v.ink(rect(x, 0, 18, h), shade(c, -0.07))
    # a faint damp stain
    v.ink(ellipse(260, 160, 150, 70), shade(c, -0.025))
    v.ink(ellipse(1360, 120, 110, 60), shade(c, 0.02))

def curtain(v, x, w, y0, y1, color=OXBLOOD, d=4, side=1):
    v.layer(d)
    v.add(poly([(x, y0), (x + w, y0), (x + w + side * 10, y1), (x - side * 4, y1)]), color)
    for k in range(1, 5):
        fx = x + w * k / 5
        v.ink(poly([(fx - 5, y0 + 10), (fx + 5, y0 + 10), (fx + 8 + side * 3, y1 - 6), (fx - 3, y1 - 6)]), shade(color, -0.3))
    v.add(rect(x - 10, y0 - 14, w + 20, 18, 4), BRASS_D)

# ============================================================== NORTH: window / desk
@view("c1_n", CH)
def c1_n():
    v = new("c1_n", left="c1_w", right="c1_e")
    wall(v, WALL_T, WALL_B, wain_y=730)
    wallpaper(v, 730)
    # window
    frame(v, 560, 100, 480, 470, outer="#2a1d16", d=2)
    hy = lake_window(v, 590, 130, 420, 410, d=3)
    v.layer(4)
    v.rect(792, 130, 16, 410, "#2a1d16")
    v.rect(590, 320, 420, 14, "#2a1d16")
    curtain(v, 470, 110, 80, 560, side=-1)
    curtain(v, 1050, 110, 80, 560, side=1)
    # sill
    v.layer(4)
    v.rect(520, 568, 560, 30, "#4a3326", r=4)
    v.rect(505, 592, 590, 14, "#2f2018", r=3)
    # the far light, dark (and its answer)
    with v.sprite("far_light", show="f('lantern_placed')", shadow=False, fx="pulse"):
        v.layer(4)
        v.add(ellipse(800, 255 + 28, 7, 7), FLAME, glow=4, ink=True)
        v.add(rect(796, 266, 8, 22), FLAME_HOT, glow=3, ink=True)
    # desk
    v.layer(3)
    v.rect(320, 650, 960, 58, "#6e4b36", r=6)
    v.layer(2)
    v.rect(350, 708, 900, 260, WOOD, grad=WOOD_D)
    v.layer(3)
    for (dx, dw) in ((380, 190), (630, 340), (1030, 190)):
        v.rect(dx, 735, dw, 150, "#6d4a37", r=6)
        v.ink(rect(dx + 8, 743, dw - 16, 4), shade("#6d4a37", 0.25))
    v.layer(4)
    v.add(ellipse(475, 810, 14, 14), BRASS); v.add(ellipse(1125, 810, 14, 14), BRASS)
    # drawer keyhole plate
    v.add(ring(800, 800, 26, 15), BRASS)
    v.add(ellipse(800, 800, 15, 15), "#2a1d16")
    v.ink(rect(796, 794, 8, 22), INK)
    v.add(ellipse(800, 800 - 38, 0.1, 0.1), BRASS)
    # desk clutter
    v.layer(4)
    v.rect(1130, 612, 38, 40, "#272a35", r=6); v.add(line([(1160, 612), (1200, 560)], 5), "#d8d0b4")  # inkwell + quill
    paper_sheet(v, 780, 628, 150, 24, "#cfc5a5", d=4)
    paper_sheet(v, 800, 612, 150, 24, "#ddd3b4", ang=-3, d=4)
    # barometer
    v.layer(2)
    v.add(ellipse(1280, 300, 84), "#3a2a20")
    v.layer(3)
    v.add(ellipse(1280, 300, 70), "#d8cfb2")
    for i in range(13):
        a = math.radians(200 + i * 10)
        v.ink(line([(1280 + 56 * math.cos(a), 300 + 56 * math.sin(a)), (1280 + 64 * math.cos(a), 300 + 64 * math.sin(a))], 3), INK)
    v.ink(line([(1280, 300), (1280 + 48 * math.cos(math.radians(250)), 300 + 48 * math.sin(math.radians(250)))], 4), "#7a2a22")
    v.ink(ellipse(1280, 300, 6, 6), INK)
    # lantern on desk (item)
    with v.sprite("lantern_desk", show="not f('got_lantern')"):
        v.layer(5)
        lantern(v, 470, 652, 1.05)
    # chart pinned to the wall by the window
    with v.sprite("chart", show="not f('got_chart')"):
        v.layer(3)
        paper_sheet(v, 175, 190, 220, 250, "#e1d6b4", ang=-2, d=3)
        g = rect(200, 230, 170, 180)
        for i in range(1, 5):
            v.ink(line([(200 + i * 34, 230), (200 + i * 34, 410)], 2), "#5b4a35", d=3)
            v.ink(line([(200, 230 + i * 36), (370, 230 + i * 36)], 2), "#5b4a35", d=3)
        v.ink(poly([(205, 400), (240, 372), (290, 380), (320, 330), (370, 340), (370, 410), (205, 410)]), "#8fa59a", d=3)
        v.ink(ring(318, 276, 22, 16), "#a33a30", d=3)
        v.add(ellipse(285, 207, 7, 7), "#9a2d2d", d=4)
    # hotspots (large things first)
    v.hot("window", (590, 130, 420, 410))
    v.hot("barometer", (1196, 216, 168, 168))
    v.hot("sill", (505, 560, 590, 50))
    v.hot("desk", (320, 650, 960, 58))
    v.hot("drawer", (630, 735, 340, 150))
    v.hot("lantern_desk", (410, 530, 130, 130), when="not f('got_lantern')")
    v.hot("chart", (175, 190, 220, 250), when="not f('got_chart')")
    v.hot("lantern_win", (740, 440, 120, 130), when="f('lantern_placed')")
    # the moth in its jar (desk, right): calms once a light burns; then it flies to the window
    with v.sprite("jar", show="not f('moth_free')", fx="bob"):
        v.layer(5)
        v.add(jar_shape(1018, 545, 86, 106), "#a9c6c6")
        v.ink(jar_shape(1026, 553, 70, 90), "#8aa9ab")
        v.add(rect(1030, 538, 58, 14, 4), "#c9a24d")
        moth(v, 1061, 612, 0.7)
        v.ink(rect(1030, 566, 6, 66), "#e9f4f4")
    with v.sprite("jar_open", show="f('moth_free')"):
        v.layer(5)
        v.add(jar_shape(1018, 545, 86, 106), "#a9c6c6")
        v.ink(jar_shape(1026, 553, 70, 90), "#6d8c90")
        v.add(rect(1070, 520, 58, 14, 4), "#c9a24d")
    with v.sprite("moth_n", show="f('moth_window')", fx="bob"):
        v.layer(6)
        moth(v, 872, 470, 1.0, glow=0.6)
    v.hot("jar", (1010, 530, 110, 130), when="not f('moth_free')")
    v.hot("moth_n", (810, 410, 130, 120), when="f('moth_window')")
    # lantern burning on the sill
    with v.sprite("lantern_win", show="f('lantern_placed')", fx="flicker"):
        v.layer(5)
        lantern(v, 800, 574, 1.0, lit=True)
    v.light(800, 480, 760, "#ffb860", when="f('lantern_placed')", intensity=1.0, flicker=0.06)
    return v

# ============================================================== EAST: fireplace
def clock_face(v, cx, cy, R, d=4, numerals=True, fish=True, face="#e7dcbc", tick="#2a1d16"):
    v.layer(d)
    v.add(ellipse(cx, cy, R), BRASS_D)
    v.add(ellipse(cx, cy, R * 0.94), face)
    # minute ticks
    for i in range(60):
        a = math.radians(i * 6)
        L = R * (0.08 if i % 5 == 0 else 0.04)
        r1 = R * 0.9
        v.ink(line([(cx + r1 * math.sin(a), cy - r1 * math.cos(a)), (cx + (r1 - L) * math.sin(a), cy - (r1 - L) * math.cos(a))], max(2, R * 0.012)), tick, d=d)
    if numerals:
        for hr in range(1, 13):
            a = math.radians(hr * 30)
            rr = R * 0.7
            nx, ny = cx + rr * math.sin(a), cy - rr * math.cos(a)
            txt = {1: "I", 2: "II", 3: "III", 4: "IIII", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X", 11: "XI", 12: "XII"}[hr]
            g = roman(txt, R * 0.15, R * 0.026)
            g = rot(move(g, nx, ny), hr * 30, origin=(nx, ny))
            v.ink(g, tick, d=d)
    if fish:
        # tiny fish engraved beside the IIII
        a = math.radians(120)
        fx, fy = cx + R * 0.47 * math.sin(a), cy - R * 0.47 * math.cos(a)
        f = union(ellipse(fx, fy, R * 0.07, R * 0.035), poly([(fx + R * 0.05, fy), (fx + R * 0.1, fy - R * 0.04), (fx + R * 0.1, fy + R * 0.04)]))
        v.ink(rot(f, -22, origin=(fx, fy)), "#7a5a22", d=d)

def roman(s, h, w):
    parts = []
    x = 0.0
    sp = w * 2.6
    vw = h * 0.7
    for ch in s:
        if ch == "I":
            parts.append(rect(x - w / 2, -h / 2, w, h)); x += sp
        elif ch == "V":
            parts.append(line([(x - vw / 2, -h / 2), (x, h / 2)], w, cap="flat")); parts.append(line([(x + vw / 2, -h / 2), (x, h / 2)], w, cap="flat")); x += vw + sp * 0.4
        elif ch == "X":
            parts.append(line([(x - vw / 2, -h / 2), (x + vw / 2, h / 2)], w, cap="flat")); parts.append(line([(x + vw / 2, -h / 2), (x - vw / 2, h / 2)], w, cap="flat")); x += vw + sp * 0.4
    g = union(*parts)
    minx, miny, maxx, maxy = g.bounds
    return move(g, -(minx + maxx) / 2, 0)

@view("c1_e", CH)
def c1_e():
    v = new("c1_e", left="c1_n", right="c1_s")
    wall(v, WALL_T, WALL_B, wain_y=760)
    wallpaper(v, 760)
    # chimney breast
    v.layer(1)
    v.rect(330, 0, 900, 760, "#527470", grad="#41625e")
    v.layer(2)
    v.rect(310, 0, 24, 760, "#3a5754"); v.rect(1226, 0, 24, 760, "#3a5754")
    # fireplace surround + firebox
    v.layer(2)
    v.rect(500, 520, 600, 440, "#2e2a2c", r=8)
    v.layer(3)
    v.add(poly([(560, 940), (560, 640), (600, 596), (1000, 596), (1040, 640), (1040, 940)]), "#0f0d0e")
    v.layer(4)
    # hearth
    v.rect(470, 930, 660, 36, "#6b6b68", r=4)
    # andirons + ashes + burnt remains
    v.add(rect(590, 880, 14, 52), "#1b1b1c"); v.add(rect(996, 880, 14, 52), "#1b1b1c")
    v.add(rect(580, 878, 440, 10, 3), "#1b1b1c")
    v.add(poly([(620, 930), (700, 892), (800, 884), (900, 890), (990, 930)]), "#4a4545")
    v.ink(poly([(690, 920), (760, 900), (830, 908), (850, 922)]), "#6e6561")
    # mantel shelf
    v.layer(4)
    v.rect(380, 476, 840, 44, "#7a5339", r=5)
    v.layer(3)
    v.rect(420, 520, 760, 18, "#5a3d2c")
    # the armchair, still warm
    v.layer(2)
    v.rect(1290, 560, 270, 400, "#5b1d29", r=24)                       # back
    v.layer(3)
    v.rect(1264, 700, 70, 250, "#6c2431", r=20); v.rect(1516, 700, 70, 250, "#6c2431", r=20)   # arms
    v.rect(1310, 780, 240, 150, "#7a2938", r=16)                      # seat cushion
    v.ink(rect(1330, 800, 200, 6), "#8e3446")
    v.add(rect(1292, 930, 20, 30), WOOD_D); v.add(rect(1528, 930, 20, 30), WOOD_D)
    for i in range(3):
        v.add(ellipse(1370 + i * 70, 640, 8, 8), BRASS_D, ink=True)
    # warm shimmer above the seat (a hint: it is still warm)
    with v.sprite("warm", shadow=False, fx="pulse"):
        v.layer(5)
        v.add(ellipse(1430, 810, 90, 30), "#e8a05a", glow=0.9, alpha=1, ink=True)
    v.light(1430, 790, 220, "#ff9a50", intensity=0.28)
    # coal bucket + logs
    v.layer(3)
    v.rect(200, 800, 140, 150, "#2a2a2c", r=10)
    v.ink(rect(200, 820, 140, 8), "#454548")
    v.add(arc(270, 800, 60, 180, 360, 8), "#2a2a2c")
    # painting above the mantel (item hotspot to the close-up)
    frame(v, 700, 120, 480, 320, outer="#3b281d", inner="#16222a", t=22, d=3)
    v.layer(5)
    v.ink(wave(722, 1158, 330, 4, 70, 5), "#223742")
    v.ink(ellipse(940, 270, 120, 60), "#1b2c35")
    v.ink(poly([(1090, 140), (1106, 250), (1076, 250)]), "#1b2c35")
    # the clock on the mantel (case)
    v.layer(5)
    v.add(poly([(420, 476), (420, 330), (470, 270), (570, 270), (620, 330), (620, 476)]), "#4b3224")
    v.layer(5)
    clock_face(v, 520, 366, 66, d=6, numerals=False, fish=False)
    # hands (sprites, rotated by the game from the clock state)
    with v.sprite("hand_h", pivot=(520, 366), shadow=False, fx="hand_h"):
        v.layer(7); v.add(hand_shape(520, 366, 38, 7), INK)
    with v.sprite("hand_m", pivot=(520, 366), shadow=False, fx="hand_m"):
        v.layer(7); v.add(hand_shape(520, 366, 54, 5), INK)
    v.layer(8)
    v.add(ellipse(520, 366, 5, 5), BRASS)
    # candle stub and flame
    with v.sprite("stub", show="not f('candle_taken')"):
        v.layer(5)
        candle_stub(v, 1090, 478, 1.0)
    with v.sprite("flame", show="f('candle_burning') and not f('candle_taken')", shadow=False, fx="flicker"):
        v.layer(6)
        flame(v, 1090, 400, 1.0)
    v.light(1090, 410, 420, "#ffb050", when="f('candle_burning') and not f('candle_taken')", intensity=1.0, flicker=0.1)
    # small vase
    v.layer(5)
    v.add(poly([(830, 476), (822, 430), (838, 400), (872, 400), (888, 430), (880, 476)]), "#7f9a92")
    v.add(line([(850, 400), (842, 340)], 4), "#4a6a40"); v.add(line([(860, 400), (872, 350)], 4), "#4a6a40")
    # hotspots
    v.hot("grate", (560, 600, 480, 340))
    v.hot("armchair", (1264, 560, 320, 400))
    v.hot("coal", (200, 800, 140, 150))
    v.hot("vase", (810, 330, 90, 150))
    v.hot("painting", (700, 120, 480, 320))
    v.hot("clock", (420, 270, 200, 206))
    v.hot("candle", (1040, 340, 100, 140), when="not f('candle_taken')")
    return v

# ============================================================== SOUTH: door
@view("c1_s", CH)
def c1_s():
    v = new("c1_s", left="c1_e", right="c1_w")
    wall(v, WALL_T, WALL_B, wain_y=730)
    wallpaper(v, 730)
    # door frame + door
    frame(v, 560, 70, 480, 880, outer="#33231a", d=2, r=4)
    v.layer(3)
    v.rect(584, 94, 432, 856, "#5e402e", grad="#4a3224")
    for (px, py, pw, ph) in ((610, 130, 170, 300), (820, 130, 170, 300), (610, 470, 170, 440), (820, 470, 170, 440)):
        v.layer(4); v.rect(px, py, pw, ph, "#70503a", r=6)
        v.layer(5); v.rect(px + 14, py + 14, pw - 28, ph - 28, "#5a3d2c", r=4)
    v.layer(5)
    v.add(ellipse(975, 560, 20, 20), BRASS); v.ink(ellipse(975, 560, 8, 8), BRASS_D)
    # shape lock plate
    v.layer(6)
    v.rect(880, 420, 120, 130, "#2f2a28", r=10)
    for i in range(4):
        v.add(ellipse(900 + (i % 2) * 60 + 0, 445 + (i // 2) * 55, 20, 20), "#1a1614", ink=True)
    # door open => jetty beyond (sprite swap)
    with v.sprite("door_open", show="f('door_open')", shadow=False):
        v.layer(6)
        v.rect(584, 94, 432, 856, "#0f2128", grad="#365867")
        v.layer(7)
        v.rect(584, 600, 432, 350, "#1b3b46", grad="#0d2229")
        v.layer(8)
        v.add(poly([(700, 950), (900, 950), (840, 650), (760, 650)]), "#5c4533")
        v.ink(rect(760, 640, 80, 8), "#3a2a20")
        v.add(ellipse(800, 330, 90, 56), "#b8c9bd", glow=1.1, alpha=1, ink=True)
    v.light(800, 700, 520, "#9ac4c8", when="f('door_open')", intensity=0.5)
    # doormat
    v.layer(2)
    v.rect(580, 940, 440, 52, "#7a5a3a", r=6)
    v.ink(rect(594, 948, 412, 36, 4), "#5d422a")
    v.text("mat", "world.return", (600, 944, 400, 44), size=28, color="#d9c9a0", font="world", spacing=6)
    with v.sprite("mat_lift", show="f('mat_lifted')"):
        v.layer(5)
        v.add(poly([(572, 946), (1030, 946), (1010, 880), (590, 880)]), "#8a6a46")
    with v.sprite("frag2", show="f('mat_lifted') and not f('got_frag2')"):
        v.layer(6)
        v.add(poly([(740, 962), (836, 954), (846, 990), (752, 996)]), "#cfc4a3", d=6)
        v.ink(rect(764, 968, 40, 22), "#6a6f69", d=6)
    # coat on a hook (left)
    v.layer(2)
    v.add(rect(260, 150, 160, 16), "#3b281d")
    v.add(ellipse(300, 150, 12, 12), BRASS); v.add(ellipse(380, 150, 12, 12), BRASS)
    v.layer(3)
    v.add(poly([(250, 164), (430, 164), (460, 700), (230, 700)]), "#3a4a52", grad="#2f3d44")
    v.layer(4)
    v.add(poly([(250, 164), (340, 164), (332, 360), (292, 320)]), "#2c3a41")
    v.add(poly([(430, 164), (340, 164), (332, 360), (372, 320)]), "#4a5d66")
    for i in range(3):
        v.ink(ellipse(340, 400 + i * 80, 7, 7), BRASS)
    v.add(rect(260, 480, 80, 70, 5), "#2c3a41"); v.add(rect(350, 480, 80, 70, 5), "#2c3a41")      # pockets
    v.ink(rect(266, 486, 68, 6), "#1f2b31"); v.ink(rect(356, 486, 68, 6), "#1f2b31")
    # oar in its stand (right of the door)
    v.layer(3)
    v.rect(1110, 840, 120, 120, "#3b281d", r=8)
    v.ink(rect(1120, 870, 100, 8), "#5a3d2c")
    with v.sprite("oar", show="not f('got_oar')"):
        v.layer(5)
        v.add(rect(1160, 330, 20, 560, 6), "#8a6a46")
        v.add(rect(1136, 250, 68, 220, 28), "#a68359")
        v.ink(line([(1170, 262), (1170, 456)], 4), "#7d5f3c")
        v.ink(rect(1160, 700, 20, 8), "#5a3d2c")
    # mirror (far right)
    frame(v, 1280, 190, 220, 340, outer="#c9a24d", inner="#5f7c80", t=14, d=3, inner_grad="#3d5a60", r=30)
    v.layer(5)
    v.ink(poly([(1310, 260), (1350, 232), (1356, 252), (1316, 282)]), "#9ab4b6")
    v.ink(poly([(1330, 460), (1384, 400), (1392, 418), (1346, 474)]), "#8aa6a8")
    # hotspots
    v.hot("door", (584, 94, 432, 856))
    v.hot("lockplate", (880, 420, 120, 130))
    v.hot("coat", (230, 150, 230, 550))
    v.hot("mirror", (1280, 190, 220, 340))
    v.hot("mat", (580, 940, 440, 52))
    v.hot("oar", (1136, 250, 100, 640), when="not f('got_oar')")
    v.hot("oar_stand", (1110, 840, 120, 120))
    v.hot("frag2", (740, 940, 120, 70), when="f('mat_lifted') and not f('got_frag2')")
    v.hot("door_exit", (700, 300, 220, 600), when="f('door_open')")
    return v

# ============================================================== WEST: shelves, bowl, plaque
@view("c1_w", CH)
def c1_w():
    v = new("c1_w", left="c1_s", right="c1_n")
    wall(v, WALL_T, WALL_B, wain_y=730)
    wallpaper(v, 730)
    # bookshelf
    v.layer(2)
    v.rect(560, 120, 480, 520, "#33231a", r=6)
    v.layer(3)
    for sy in (260, 440, 620):
        v.rect(574, sy - 8, 452, 22, "#6e4b36")
    v.rect(574, 134, 452, 18, "#4a3326")
    # books (flat shapes, shuffled colours - the big ones are in the close-up)
    xs = 590
    cols = [(GREEN, "dots"), (RED, "stripes"), (YELLOW, "plain"), (PALE, "chevrons")]
    xx = 600
    for i, (c, pat) in enumerate(cols):
        book(v, xx, 156, 66, 98, c, pat, d=4)
        xx += 74
    xx = 600
    for i, c in enumerate(["#44566a", "#7a5a3a", "#5b3b48", "#3f6a64", "#8a7a50", "#4a4a5a"]):
        book(v, xx, 300, 52 + (i % 3) * 8, 134 - (i % 2) * 14, c, "plain", d=4)
        xx += 68 + (i % 3) * 8
    # cabinet below (lamp oil)
    v.layer(3)
    v.rect(560, 642, 480, 300, "#5a3d2c", r=6)
    v.layer(4)
    v.rect(576, 660, 220, 262, "#6e4b36", r=5); v.rect(804, 660, 220, 262, "#6e4b36", r=5)
    v.add(ellipse(786, 790, 11, 11), BRASS); v.add(ellipse(814, 790, 11, 11), BRASS)
    # pell's side table + bowl (left)
    v.layer(3)
    v.rect(180, 640, 250, 24, "#6e4b36", r=5)
    v.rect(200, 664, 20, 280, "#5a3d2c"); v.rect(390, 664, 20, 280, "#5a3d2c")
    v.layer(4)
    v.add(ellipse(305, 600, 96, 70), "#9fc2c4", alpha=1)
    v.add(ellipse(305, 600, 86, 60), "#3a7a86", grad=None)
    v.add(rect(240, 662, 130, 8), "#7e9fa1")
    with v.sprite("pell", fx="bob"):
        v.layer(5)
        pell_fish(v, 308, 604, 0.62, facing=1)
    v.layer(6)
    v.ink(arc(305, 580, 80, 195, 255, 5), "#e8f4f4")
    # pike plaque (right)
    v.layer(3)
    v.rect(1160, 220, 300, 130, "#2e2018", r=6)
    v.layer(4)
    v.add(union(ellipse(1310, 300, 120, 24), poly([(1428, 300), (1480, 270), (1480, 330)])), "#8da28e")
    v.add(poly([(1220, 300), (1170, 292), (1170, 312)]), "#7a8d7c")
    v.ink(ellipse(1220, 292, 5, 5), INK)
    v.ink(rect(1250, 296, 150, 6), "#6a7f6c")
    v.text("plaque", "world.plaque", (1160, 352, 300, 56), size=20, color="#d9c9a0", font="world", spacing=1)
    v.layer(3)
    v.rect(1180, 346, 260, 56, "#c9a24d", r=3)
    # photograph (left wall)
    frame(v, 180, 180, 170, 220, outer="#2a1d16", inner="#b9b49f", t=12, d=3)
    v.layer(5)
    v.ink(rect(192, 230, 146, 150), "#7b8e8a")
    v.ink(rect(192, 330, 146, 50), "#4a5e5e")
    v.add(poly([(264, 386), (264, 322), (252, 300), (275, 262), (296, 300), (284, 322), (284, 386)]), "#1d1713", ink=True)
    v.add(ellipse(274, 262, 14, 14), "#1d1713", ink=True)
    # rug hint
    v.hot("shelf", (560, 120, 480, 520))
    v.hot("cabinet", (560, 642, 480, 300))
    v.hot("bowl_w", (200, 530, 220, 140))
    v.hot("plaque", (1160, 220, 300, 190))
    v.hot("photo", (180, 180, 170, 220))
    v.hot("table", (180, 640, 250, 300))
    return v


# ======================================================================= CLOSE-UPS
def closeup_bg(v, top="#2c3d3d", bot="#1e2b2b"):
    v.layer(0)
    v.rect(0, 0, 1600, 1000, top, grad=bot)
    for x in range(20, 1600, 110):
        v.ink(rect(x, 0, 24, 1000), shade(top, -0.06))

@view("c1_window", CH)
def c1_window():
    v = new("c1_window", back="c1_n")
    closeup_bg(v, "#2b3c3c", "#1b2828")
    # big window pane
    frame(v, 200, 70, 1200, 860, outer="#2a1d16", d=1, r=6)
    v.variants_when({"shapes": "f('moth_window')"}, "plain")
    hy = lake_window(v, 240, 110, 1120, 780, d=2, horizon=0.5, far_light=False)
    # mullions
    v.layer(3)
    v.rect(792, 110, 16, 780, "#2a1d16"); v.rect(240, 410, 1120, 16, "#2a1d16")
    # the lake shows four shapes, upside-down, once the moth is at the window
    with v.variant("shapes"):
        v.layer(3)
        order = ["eye", "moon", "fish", "bell"]
        for i, nm in enumerate(order):
            shape, details = glyph_geom(nm, 560 + i * 225, 690, 150)
            c = "#9fc2c6"
            v.add(flip_v(shape), c, d=3, ink=True, alpha=1)
            for g, kind in details:
                v.add(flip_v(g), "#27495a" if kind == "dark" else c, d=3, ink=True)
        for i in range(4):
            v.ink(rect(520 + i * 225, 790 + (i % 2) * 14, 80, 4), "#1b3a47")
    # sill + lantern (when it burns here)
    v.layer(4)
    v.rect(170, 905, 1260, 50, "#4a3326", r=5)
    with v.sprite("lantern_w", show="f('lantern_placed')", fx="flicker"):
        v.layer(5)
        lantern(v, 330, 910, 2.2, lit=True)
    with v.sprite("moth_w", show="f('moth_window')", fx="bob"):
        v.layer(6)
        moth(v, 450, 620, 1.5, glow=0.7)
    v.light(330, 700, 900, "#ffb860", when="f('lantern_placed')", intensity=1.0, flicker=0.06)
    v.hot("lake", (450, 500, 910, 390))
    v.hot("moth_w", (370, 540, 160, 160), when="f('moth_window')")
    v.hot("lantern_w", (230, 640, 200, 280), when="f('lantern_placed')")
    return v

@view("c1_drawer", CH)
def c1_drawer():
    v = new("c1_drawer", back="c1_n")
    closeup_bg(v, "#2a2321", "#1b1614")
    v.layer(1)
    v.rect(180, 120, 1240, 760, "#4a3326", grad="#33231a", r=14)           # drawer box seen from above
    v.layer(2)
    v.rect(230, 170, 1140, 660, "#3b281d", grad="#2a1c14", r=8)
    # lining cloth
    v.layer(3)
    v.rect(260, 200, 1080, 600, "#52292f", r=6)
    for x in range(290, 1330, 70):
        v.ink(rect(x, 210, 8, 580), "#5b3037")
    # stray things
    v.layer(4)
    v.add(ellipse(1150, 620, 26, 26), "#8d8d82"); v.ink(ellipse(1150, 620, 16, 16), "#5e5e58")       # button
    v.add(line([(420, 700), (620, 660)], 14), "#c9a24d"); v.add(poly([(620, 654), (650, 658), (620, 668)]), INK)   # pencil
    v.add(ellipse(1010, 360, 20, 20), "#b0a28a"); v.add(ellipse(1060, 390, 14, 14), "#b0a28a")
    with v.sprite("food", show="not f('got_food')"):
        v.layer(5)
        v.add(rect(860, 430, 190, 230, 18), "#3e6a74")
        v.add(rect(850, 410, 210, 40, 10), "#c9a24d")
        v.add(rect(884, 478, 142, 120, 8), "#e8dec2")
        v.ink(ellipse(955, 540, 30, 20), GOLDFISH)
        v.ink(poly([(978, 540), (1008, 520), (1008, 560)]), GOLDFISH)
    with v.sprite("note", show="not f('got_note')"):
        v.layer(5)
        paper_sheet(v, 380, 270, 280, 330, "#e6dcbc", ang=-6, d=5, lines=6)
        v.add(ellipse(520, 285, 0.1, 0.1), INK)
    v.hot("drawer_inner", (180, 120, 1240, 760))
    v.hot("food", (850, 410, 210, 250), when="not f('got_food')")
    v.hot("note", (370, 250, 300, 360), when="not f('got_note')")
    return v

@view("c1_coat", CH)
def c1_coat():
    v = new("c1_coat", back="c1_s")
    closeup_bg(v, "#2b3a3d", "#1d2a2c")
    v.layer(1)
    v.add(poly([(260, 0), (1340, 0), (1420, 1000), (180, 1000)]), "#3a4a52", grad="#2a373d")
    v.layer(2)
    v.add(poly([(260, 0), (640, 0), (600, 420), (420, 300)]), "#2c3a41")
    v.add(poly([(1340, 0), (960, 0), (1000, 420), (1180, 300)]), "#4d6169")
    v.layer(2)
    v.rect(780, 20, 40, 1000, "#2a373d")           # front seam
    for i in range(5):
        v.add(ellipse(800, 220 + i * 140, 24, 24), BRASS, d=3)
        v.ink(ellipse(800, 220 + i * 140, 12, 12), BRASS_D, d=3)
    # two big pockets
    for (px, nm) in ((260, "pl"), (880, "pr")):
        v.layer(3)
        v.rect(px, 560, 400, 300, "#2f3d44", r=10)
        v.layer(4)
        v.rect(px + 14, 580, 372, 40, "#243238", r=6)
        v.ink(rect(px + 30, 640, 340, 6), "#3b4d55")
    with v.sprite("key", show="f('pocket_r') and not f('got_key')"):
        v.layer(6)
        key(v, 1080, 700, 2.2, ang=-18)
    with v.sprite("ticket", show="f('pocket_l') and not f('got_ticket')"):
        v.layer(6)
        paper_sheet(v, 380, 590, 240, 130, "#d9c8a0", ang=4, d=6)
        v.ink(rect(396, 612, 100, 10), "#7a2a22", d=6)
        v.ink(rect(396, 640, 200, 6), INK, d=6, alpha=1)
        v.ink(rect(396, 662, 150, 6), INK, d=6)
    v.hot("pocket_l", (260, 560, 400, 300))
    v.hot("pocket_r", (880, 560, 400, 300))
    v.hot("key", (980, 600, 220, 200), when="f('pocket_r') and not f('got_key')")
    v.hot("ticket", (360, 580, 280, 150), when="f('pocket_l') and not f('got_ticket')")
    return v

@view("c1_clock", CH)
def c1_clock():
    v = new("c1_clock", back="c1_e")
    closeup_bg(v, "#26373a", "#1a2729")
    cx, cy, R = 800, 380, 270
    v.layer(1)
    v.add(poly([(420, 960), (420, 360), (500, 150), (800, 60), (1100, 150), (1180, 360), (1180, 960)]), "#4b3224", grad="#3a251a")
    v.layer(2)
    v.add(poly([(450, 940), (450, 370), (520, 170), (800, 90), (1080, 170), (1150, 370), (1150, 940)]), "#5a3d2c")
    clock_face(v, cx, cy, R, d=3)
    # hatch under the face (the match is kept inside)
    v.layer(3)
    v.rect(690, 690, 220, 120, "#3b281d", r=8)
    v.layer(4)
    v.rect(702, 702, 196, 96, "#6e4b36", r=6)
    v.add(ellipse(800, 750, 10, 10), BRASS)
    # knobs (hour left, minute right) with their marks
    for (kx, ky, long_) in ((620, 880, False), (980, 880, True)):
        v.layer(3)
        v.add(ellipse(kx, ky, 62), BRASS_D)
        v.layer(4)
        v.add(ellipse(kx, ky, 50), BRASS)
        v.ink(rect(kx - 5, ky - 40, 10, 80), BRASS_D)
        v.ink(ellipse(kx, ky, 12, 12), BRASS_D)
        v.ink(rect(kx - 5, ky - 100 - (30 if long_ else 0), 10, 24 + (30 if long_ else 0)), "#2a1d16")
    with v.sprite("hatch_open", show="f('clock_set')"):
        v.layer(5)
        v.rect(690, 690, 220, 120, "#120c09", r=8)
        v.add(poly([(690, 690), (630, 712), (630, 790), (690, 810)]), "#6e4b36")
    with v.sprite("match", show="f('clock_set') and not f('got_match')"):
        v.layer(6)
        v.add(line([(740, 770), (860, 730)], 12), "#d9c08a")
        v.add(ellipse(866, 727, 15, 15), "#a33a30")
        v.ink(ellipse(862, 722, 6, 6), "#d8584a")
    with v.sprite("hand_h", pivot=(cx, cy), shadow=True, fx="hand_h"):
        v.layer(7); v.add(hand_shape(cx, cy, 160, 26), INK)
    with v.sprite("hand_m", pivot=(cx, cy), shadow=True, fx="hand_m"):
        v.layer(8); v.add(hand_shape(cx, cy, 235, 16), INK)
    v.layer(9)
    v.add(ellipse(cx, cy, 20, 20), BRASS)
    v.widget("clock", "clock", (cx - R, cy - R, 2 * R, 2 * R), cx=cx, cy=cy, knob_h=[620, 880], knob_m=[980, 880], step_m=5)
    v.hot("fish_engraving", (cx + 80, cy + 20, 110, 110))
    v.hot("match", (690, 690, 220, 120), when="f('clock_set') and not f('got_match')")
    v.hot("hatch", (690, 690, 220, 120))
    return v

@view("c1_painting", CH)
def c1_painting():
    v = new("c1_painting", back="c1_e")
    closeup_bg(v, "#2a3a3b", "#1c2829")
    frame(v, 150, 90, 1300, 820, outer="#3b281d", t=28, d=1, r=8)
    v.layer(1)
    v.rect(172, 112, 1256, 776, "#2a1d16")
    v.variants_when({"lit": "f('painting_lit')"}, "dark")
    with v.variant("dark"):
        v.layer(2)
        v.rect(178, 118, 1244, 764, "#0f171b", grad="#0b1114")
        # barely-there shapes: nothing can be made out
        v.ink(wave(190, 1410, 600, 6, 140, 6), "#131d22")
        v.ink(ellipse(800, 420, 200, 40), "#111a1e")
        v.ink(rect(1210, 330, 22, 220), "#121b20")
    with v.variant("lit"):
        v.layer(2)
        v.rect(178, 118, 1244, 764, "#234a56", grad="#bcc7a6")           # dusk sky, pale at the horizon
        v.layer(3)
        v.rect(178, 560, 1244, 322, "#2d5764", grad="#13303a")
        v.ink(ellipse(900, 300, 90, 90), "#e8e2c0", d=3)
        # far lighthouse
        v.layer(3)
        v.add(poly([(1180, 560), (1196, 420), (1216, 420), (1232, 560)]), "#162a31")
        v.add(rect(1190, 392, 32, 28), "#162a31")
        v.add(poly([(1186, 392), (1206, 366), (1226, 392)]), "#162a31")
        # the four floats, in a line across the shallows: red, green, pale, yellow
        names = ["red", "green", "pale", "yellow"]
        for i, nm in enumerate(names):
            fx = 330 + i * 230
            fy = 700 + (i % 2) * 30 - (i // 2) * 8
            float_buoy(v, fx, fy, 1.5, FLOAT_COLORS[nm], FLOAT_PATTERN[nm], d=4)
        # ripples (still)
        for i in range(5):
            v.ink(rect(220 + i * 230, 790 + (i % 2) * 18, 150, 4), "#3c7482", d=3)
        # the heron, at the shore
        heron_silhouette(v, 1330, 860, 0.7, d=4, flip=True)
        v.add(poly([(1180, 860), (1422, 840), (1422, 888), (1180, 888)]), "#17302a", d=4)
        for i in range(6):
            v.add(line([(1200 + i * 30, 870), (1196 + i * 30, 790 - (i % 3) * 20)], 5), "#2c4a38", d=4)
    v.hot("painting_surface", (178, 118, 1244, 764))
    return v

@view("c1_books", CH)
def c1_books():
    v = new("c1_books", back="c1_w")
    closeup_bg(v, "#26373a", "#1a2729")
    v.layer(1)
    v.rect(110, 60, 1380, 880, "#33231a", r=10)
    v.layer(2)
    v.rect(140, 90, 1320, 480, "#241912", r=6)                   # shelf interior
    v.layer(3)
    v.rect(130, 560, 1340, 36, "#6e4b36", r=4)
    # filler books at the two ends
    fx = 170
    for i, c in enumerate(["#44566a", "#7a5a3a", "#5b3b48"]):
        book(v, fx, 250 + (i % 2) * 20, 70 + i * 6, 306 - (i % 2) * 20, c, "plain", d=4); fx += 84
    fx = 1230
    for i, c in enumerate(["#3f6a64", "#8a7a50", "#4a4a5a"]):
        book(v, fx, 240 + (i % 2) * 24, 70 + i * 6, 316 - (i % 2) * 24, c, "plain", d=4); fx += 84
    # the four books: art is rendered in the solved order (red, green, pale, yellow)
    slots = [420, 600, 780, 960]
    for i, nm in enumerate(["red", "green", "pale", "yellow"]):
        with v.sprite("book_" + nm):
            v.layer(5)
            book(v, slots[i], 190, 140, 366, FLOAT_COLORS[nm], FLOAT_PATTERN[nm], d=5)
    v.widget("books", "books", (400, 170, 720, 400), sprites=["book_red", "book_green", "book_pale", "book_yellow"], slots=slots)
    # cabinet below
    v.layer(3)
    v.rect(130, 600, 1340, 330, "#4a3326")
    v.layer(4)
    v.rect(160, 620, 650, 290, "#6e4b36", r=8); v.rect(830, 620, 610, 290, "#6e4b36", r=8)
    v.layer(5)
    v.rect(190, 650, 590, 230, "#5a3d2c", r=6); v.rect(860, 650, 550, 230, "#5a3d2c", r=6)
    v.add(ellipse(780, 760, 18, 18), BRASS); v.add(ellipse(850, 760, 18, 18), BRASS)
    with v.sprite("cabinet_open", show="f('cabinet_open')"):
        v.layer(6)
        v.rect(160, 620, 1280, 290, "#0d0a09", r=6)
        v.layer(7)
        v.add(rect(180, 880, 1240, 22), "#4a3326")
        v.add(poly([(160, 620), (90, 650), (90, 880), (160, 910)]), "#6e4b36")
        v.add(poly([(1440, 620), (1510, 650), (1510, 880), (1440, 910)]), "#6e4b36")
    with v.sprite("oil", show="f('cabinet_open') and not f('got_oil')"):
        v.layer(8)
        v.add(rect(690, 700, 220, 190, 22), "#7a8a52")
        v.add(rect(765, 640, 70, 70, 10), "#7a8a52")
        v.add(rect(770, 626, 60, 22, 6), "#3b281d")
        v.ink(rect(710, 760, 180, 90, 8), "#e8dec2")
        v.ink(ellipse(800, 805, 28, 28), "#c0a038")
    v.hot("books_row", (400, 170, 720, 400))
    v.hot("cabinet", (160, 620, 1280, 290))
    v.hot("oil", (680, 620, 240, 280), when="f('cabinet_open') and not f('got_oil')")
    return v

@view("c1_bowl", CH)
def c1_bowl():
    v = new("c1_bowl", back="c1_w")
    closeup_bg(v, "#2b3c3c", "#1a2727")
    v.layer(1)
    v.rect(0, 800, 1600, 200, "#4a3326", grad="#33231a")
    v.layer(2)
    v.add(ellipse(800, 880, 360, 50), "#241912")
    v.layer(3)
    v.add(ellipse(800, 470, 400, 350), "#a7c8c8")
    v.layer(4)
    v.add(ellipse(800, 480, 376, 326), "#2e6f7c", grad=None)
    v.add(ellipse(800, 480, 376, 326), "#3b8a98")
    v.layer(5)
    v.add(poly([(450, 640), (1150, 640), (1100, 760), (500, 760)]), "#c9b48a", ink=True)           # gravel
    for i in range(9):
        v.ink(ellipse(500 + i * 75, 700 + (i % 3) * 14, 22, 12), shade("#c9b48a", -0.2 + 0.1 * (i % 3)))
    for (px, ph) in ((520, 220), (580, 280), (1060, 250)):
        v.add(poly([(px - 14, 690), (px, 690 - ph), (px + 14, 690)]), "#3f7f4a", ink=True)
    v.add(ellipse(800, 480, 376, 326), "#ffffff", alpha=1, ink=True) if False else None
    with v.sprite("pell", fx="bob", shadow=False):
        v.layer(6)
        pell_fish(v, 800, 470, 1.8, facing=1)
    v.layer(7)
    v.ink(arc(800, 450, 340, 200, 262, 10), "#eaf5f5")
    v.ink(arc(800, 450, 340, 296, 330, 8), "#eaf5f5")
    v.hot("bowl", (420, 150, 760, 640))
    v.hot("pell", (680, 380, 330, 200))
    return v

@view("c1_grate", CH)
def c1_grate():
    v = new("c1_grate", back="c1_e")
    closeup_bg(v, "#2a2627", "#1a1718")
    v.layer(1)
    v.rect(0, 0, 1600, 1000, "#2b2728", grad="#171415")
    v.layer(2)
    v.rect(140, 700, 1320, 240, "#2a2829", r=6)                      # hearth stone
    v.layer(3)
    v.add(poly([(260, 880), (420, 760), (800, 720), (1180, 760), (1340, 880)]), "#3b3737")   # ash bed
    v.add(poly([(420, 860), (600, 790), (800, 780), (1000, 790), (1180, 860)]), "#4b4645")
    for i in range(30):
        rnd = random.Random(i)
        v.ink(ellipse(380 + rnd.random() * 840, 800 + rnd.random() * 70, 8 + rnd.random() * 14, 5 + rnd.random() * 5), shade("#4b4645", -0.15 + rnd.random() * 0.3))
    # iron grate bars
    v.layer(4)
    for i in range(8):
        v.add(rect(230 + i * 160, 560, 24, 330, 6), "#1d1d1f")
    v.add(rect(200, 580, 1200, 22, 6), "#1d1d1f"); v.add(rect(200, 840, 1200, 22, 6), "#1d1d1f")
    # a scrap of paper that survived: one word
    v.layer(5)
    scrap = poly([(560, 650), (700, 628), (860, 640), (1020, 622), (1060, 700), (1030, 780), (880, 800), (730, 790), (600, 800), (540, 740)])
    v.add(scrap, "#cdbf99")
    v.ink(poly([(540, 740), (560, 790), (600, 800), (580, 760)]), "#2a2118", d=5)
    v.ink(poly([(1060, 700), (1030, 780), (1000, 760), (1040, 690)]), "#2a2118", d=5)
    for i in range(4):
        v.ink(line([(590 + i * 130, 660 + (i % 2) * 6), (680 + i * 130, 650 + (i % 2) * 6)], 3), "#7c6f58", d=5)
    v.text("sorry", "world.sorry", (560, 680, 480, 90), size=64, color="#3a2418", font="world", spacing=6)
    with v.sprite("ash_pile", show="not f('got_ash')"):
        v.layer(6)
        v.add(poly([(1120, 880), (1180, 800), (1260, 790), (1320, 880)]), "#6b6563")
        v.ink(ellipse(1220, 830, 40, 18), "#807977")
    v.hot("scrap", (540, 620, 540, 190))
    v.hot("ash_pile", (1100, 780, 240, 110))
    return v

@view("c1_mirror", CH)
def c1_mirror():
    v = new("c1_mirror", back="c1_s")
    closeup_bg(v, "#2b3a3d", "#1b282a")
    # frame
    v.layer(1)
    v.rect(380, 40, 840, 920, "#c9a24d", r=60)
    v.layer(2)
    v.rect(410, 70, 780, 860, "#8d6f2c", r=50)
    v.layer(3)
    v.rect(436, 96, 728, 808, "#5f7d82", grad="#3e5a60", r=40)
    # the room, reflected (a little darker, a little wrong)
    v.layer(4)
    v.rect(436, 96, 728, 808, "#3f5f61", grad="#2e4748", r=40)
    v.layer(5)
    v.rect(436, 660, 728, 244, "#33241b", r=0)
    v.ink(rect(640, 240, 320, 460), "#2a1d16", d=5)
    v.ink(rect(660, 260, 280, 420), "#4a3224", d=5)
    # the reflection: a figure that arrives half a second late
    with v.sprite("refl", pivot=(800, 900), fx=None):
        v.layer(6)
        body = poly([(740, 900), (760, 520), (800, 480), (840, 520), (860, 900)])
        v.add(body, "#7e9c98", d=6)
        v.add(ellipse(800, 440, 44, 50), "#7e9c98", d=6)
        v.ink(poly([(760, 540), (840, 540), (856, 900), (744, 900)]), "#6d8b87", d=6)
        v.ink(ellipse(800, 440, 44, 50), "#8aa8a4", d=6)
        v.ink(arc(800, 440, 44, 190, 350, 6), "#6a8884", d=6)
    with v.sprite("frag1", show="f('mirror_gave') and not f('got_frag1')"):
        v.layer(7)
        v.add(poly([(900, 700), (1020, 690), (1030, 760), (908, 772)]), "#d1c6a4", d=7)
        v.ink(rect(918, 712, 70, 40), "#6f7d78", d=7)
    v.hot("mirror_glass", (436, 96, 728, 808))
    v.hot("frag1", (880, 670, 170, 130), when="f('mirror_gave') and not f('got_frag1')")
    return v

@view("c1_door", CH)
def c1_door():
    v = new("c1_door", back="c1_s")
    closeup_bg(v, "#3b2a1f", "#2a1d14")
    v.layer(1)
    v.rect(0, 0, 1600, 1000, "#5e402e", grad="#3e2a1e")
    for i in range(7):
        v.ink(rect(i * 230 + 20, 0, 6, 1000), "#2f2016")
    v.layer(2)
    v.rect(260, 250, 1080, 500, "#2f2a28", r=26)
    v.layer(3)
    v.rect(290, 280, 1020, 440, "#3d3735", r=20)
    for (sx, sy) in ((330, 316), (1270, 316), (330, 684), (1270, 684)):
        v.add(ellipse(sx, sy, 16, 16), BRASS); v.ink(rect(sx - 10, sy - 2, 20, 4), BRASS_D)
    cells = []
    for i in range(4):
        cx = 460 + i * 227
        v.layer(3)
        v.add(ellipse(cx, 500, 98), BRASS_D)
        v.layer(4)
        v.add(ellipse(cx, 500, 86), "#17120f")
        v.add(ring(cx, 500, 98, 86), BRASS)
        cells.append([cx - 80, 420, 160, 160])
        # up / down chevrons
        v.ink(poly([(cx - 24, 340), (cx, 316), (cx + 24, 340)]), BRASS, d=4)
        v.ink(poly([(cx - 24, 660), (cx, 684), (cx + 24, 660)]), BRASS, d=4)
    v.widget("dials", "dials", (360, 300, 900, 400), cells=cells, symbols=GLYPHS, solution=["eye", "moon", "fish", "bell"], flag="door_open", asset="ui/glyphs")
    v.hot("lockbox", (260, 250, 1080, 500))
    return v

@view("c1_photo", CH)
def c1_photo():
    v = new("c1_photo", back="c1_w")
    closeup_bg(v, "#2b3a3d", "#1b282a")
    frame(v, 380, 60, 840, 880, outer="#2a1d16", inner="#c8bda0", t=26, d=1, r=8)
    sep, sep_d = "#8a7a62", "#4f4332"
    v.layer(3)
    v.rect(436, 116, 728, 768, "#9a8a70", grad="#6a5d49")
    # the room from the other side: window and desk, from where you stand
    v.layer(4)
    v.rect(560, 230, 480, 300, "#5a4e3d", r=4)
    v.rect(580, 250, 440, 260, "#a79a80", grad="#7a6c55")
    v.ink(rect(792, 250, 16, 260), "#5a4e3d"); v.ink(rect(580, 370, 440, 14), "#5a4e3d")
    v.ink(ellipse(700, 440, 20, 20), "#d7ccb0")
    v.rect(500, 600, 600, 60, "#52483a", r=4)
    v.rect(520, 660, 560, 224, "#4a4132")
    # the figure standing in the foreground, seen from behind: exactly where you stand
    v.layer(6)
    v.add(poly([(740, 884), (748, 640), (780, 600), (820, 600), (852, 640), (860, 884)]), "#2d261d")
    v.add(ellipse(800, 560, 44, 50), "#2d261d")
    v.ink(arc(800, 560, 44, 195, 345, 6), "#4a4132")
    v.layer(5)
    v.rect(436, 116, 728, 768, "#6a5a40", alpha=1, ink=True) if False else None
    v.hot("photo_face", (436, 116, 728, 768))
    return v
