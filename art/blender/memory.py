"""Shadow-play memories and ending pictures: black paper puppets against a warm, lamp-lit screen."""
import math
from pc import *
from reg import view
from kit import *

CH = "mem"
K = "#16110d"          # puppet ink
SCREEN_T, SCREEN_B = "#f0d6a0", "#d29b52"

@view("mem_wall", CH)
def mem_wall():
    """the lit paper screen with a dark theatre border"""
    v = View("mem_wall", CH)
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#0a0705")
    v.layer(1)
    v.rect(70, 60, 1460, 880, SCREEN_T, grad=SCREEN_B, r=18)
    # warm hot-spot in the middle (the lamp behind the screen) and soft paper fibres
    v.layer(2)
    v.ink(ellipse(800, 480, 520, 330), "#f6e2b4")
    v.ink(ellipse(800, 480, 330, 210), "#fbefc8")
    rnd = random.Random(2)
    for _ in range(70):
        fx, fy = 100 + rnd.random() * 1400, 90 + rnd.random() * 820
        v.ink(line([(fx, fy), (fx + 30 + rnd.random() * 40, fy + rnd.random() * 18 - 9)], 1.4), "#e2bd7e")
    v.layer(3)
    v.rect(40, 30, 1520, 40, "#2a1a10", r=8); v.rect(40, 930, 1520, 40, "#2a1a10", r=8)
    v.rect(40, 30, 50, 940, "#2a1a10", r=8); v.rect(1510, 30, 50, 940, "#2a1a10", r=8)
    v.dark = "0.0"
    return v

def person(v, x, B, h=330, coat_w=70, hat=False, bun=True, bag=False, lantern=False, lean=0, trousers=False):
    """a standing profile silhouette (facing right), feet at (x, B)"""
    top = B - h * 0.64                       # shoulder line
    sw = coat_w * 0.55                       # half shoulder width
    hem = B - (h * 0.36 if trousers else 8)
    hw = coat_w * (0.58 if trousers else 0.88)
    waist = coat_w * 0.44
    # coat: rounded shoulders, a waist, a flared hem
    v.add(poly([(x - hw, hem), (x - waist + lean * 0.35, top + h * 0.2), (x - sw + lean, top + 16), (x - sw + 12 + lean, top + 2),
                (x + sw - 12 + lean, top + 2), (x + sw + lean, top + 16), (x + waist + lean * 0.35, top + h * 0.2), (x + hw, hem)]), K)
    v.add(rect(x - 9 + lean, top - 14, 18, 24, 4), K)                              # neck
    v.add(ellipse(x + lean, top - 38, 26, 31), K)                                   # head
    v.add(poly([(x + lean + 20, top - 48), (x + lean + 38, top - 33), (x + lean + 21, top - 29)]), K)   # nose
    if bun:
        v.add(ellipse(x - 22 + lean, top - 54, 15, 15), K)
        v.add(ellipse(x - 18 + lean, top - 40, 12, 22), K)                          # hair at the nape
    if hat:
        v.add(union(ellipse(x + lean, top - 62, 33, 20), rect(x + lean - 33, top - 62, 66, 14, 4)), K)  # flat cap
        v.add(rect(x + lean + 8, top - 52, 50, 9, 4), K)                            # its peak
    v.add(line([(x + lean + sw - 8, top + 20), (x + lean + sw + 42, top + 98)], 20), K)    # forward arm
    v.add(line([(x + lean - sw + 8, top + 20), (x + lean - sw - 6, top + 116)], 18), K)    # hanging arm
    if trousers:
        v.add(rect(x - 27, hem - 4, 23, B - hem + 4, 4), K)
        v.add(rect(x + 4, hem - 4, 23, B - hem + 4, 4), K)
        v.add(rect(x - 34, B - 15, 32, 15, 5), K)
        v.add(rect(x + 3, B - 15, 36, 15, 5), K)
    else:
        v.add(ellipse(x - 20, B - 4, 17, 7), K)
        v.add(ellipse(x + 22, B - 4, 19, 7), K)
    if bag:
        v.add(rect(x - coat_w * 0.8, top + 104, 54, 62, 8), K)
        v.add(line([(x + lean - 4, top + 8), (x - coat_w * 0.5, top + 110)], 8), K)
    if lantern:
        hx, hy = x + lean + sw + 46, top + 98                                       # held in the forward hand
        v.add(rect(hx - 17, hy, 34, 46, 5), K)
        v.add(arc(hx, hy, 17, 180, 360, 5), K)
        v.add(rect(hx - 7, hy + 10, 14, 26, 3), SCREEN_T, glow=1.2, ink=True)

@view("mem_puppets", CH)
def mem_puppets():
    v = View("mem_puppets", CH, size=(1600, 1000), kind="sheet", has_bg=False)
    def S(id, **kw):
        return v.sprite(id, shadow=False, pad=6, **kw)
    B = 360
    with S("ruth"):
        v.layer(2); person(v, 120, B, 330, 64, bun=True)
    with S("ruth_lantern"):
        v.layer(2); person(v, 330, B, 330, 64, bun=True, lantern=True)
    with S("tomas"):
        v.layer(2); person(v, 560, B, 360, 78, hat=True, bun=False, bag=True, trousers=True)
    with S("tomas_lean"):
        v.layer(2); person(v, 800, B, 360, 78, hat=True, bun=False, lean=26, trousers=True)
    with S("ruth_sit"):
        v.layer(2)
        v.add(rect(960, B - 130, 130, 24, 6), K)                         # seat
        v.add(poly([(990, B - 130), (1000, B - 330), (1070, B - 330), (1086, B - 130)]), K)
        v.add(ellipse(1034, B - 372, 28, 32), K); v.add(ellipse(1014, B - 396, 14, 14), K)
        v.add(line([(1060, B - 290), (1150, B - 200)], 20), K)
        v.add(rect(1086, B - 126, 36, 126, 6), K)
    with S("chair"):
        v.layer(2)
        v.add(rect(1250, B - 130, 140, 24, 6), K); v.add(rect(1250, B - 330, 28, 210, 6), K); v.add(rect(1250, B - 106, 18, 106), K); v.add(rect(1372, B - 106, 18, 106), K)
    with S("door"):
        v.layer(2)
        v.add(rect(1440, B - 520, 150, 520, 6), K)
        v.add(rect(1456, B - 500, 118, 480, 4), "#26150c", ink=True)
        v.add(ellipse(1556, B - 250, 8, 8), SCREEN_T, ink=True)
    with S("door_open"):
        v.layer(2)
        v.add(poly([(1700 - 260 + 0, B), (1700 - 200, B - 520), (1590 - 0, B - 520), (1590, B)]), K) if False else None
    # row 2: boat things
    B2 = 700
    with S("boat"):
        v.layer(2)
        v.add(poly([(60, B2 - 70), (560, B2 - 70), (500, B2), (140, B2)]), K)
        v.add(poly([(560, B2 - 70), (640, B2 - 120), (520, B2 - 70)]), K)
        v.add(rect(300, B2 - 220, 12, 150), K)
        v.add(rect(284, B2 - 250, 44, 40, 5), K)
        v.add(rect(292, B2 - 242, 28, 26, 3), SCREEN_T, glow=1.0, ink=True)
    with S("oar"):
        v.layer(2)
        v.add(line([(700, B2 - 10), (960, B2 - 140)], 14), K)
        v.add(rot(rect(940, B2 - 170, 90, 34, 14), -28, origin=(970, B2 - 150)), K)
    with S("wave"):
        v.layer(2)
        v.add(wave(0, 1500, 880, 22, 190, 20, n=60), K)
        v.add(rect(0, 890, 1500, 80), K)
    with S("wave_big"):
        v.layer(2)
        v.add(wave(0, 1500, 560, 56, 300, 40, n=80), K)
        v.add(rect(0, 570, 1500, 20), K)
    with S("ferry"):
        v.layer(2)
        v.add(poly([(1100, B2), (1560, B2), (1500, B2 - 70), (1160, B2 - 70)]), K)
        v.add(rect(1220, B2 - 150, 240, 82, 8), K)
        for k in range(5):
            v.add(rect(1236 + k * 46, B2 - 136, 30, 36, 4), SCREEN_T, glow=1.6, ink=True)
        v.add(rect(1330, B2 - 220, 20, 70), K)
    # row 3: scenery
    with S("lighthouse"):
        v.layer(2)
        L0 = 960
        v.add(poly([(80, L0), (120, L0 - 520), (200, L0 - 520), (240, L0)]), K)
        v.add(rect(112, L0 - 580, 96, 62, 6), K)
        v.add(poly([(100, L0 - 580), (160, L0 - 640), (220, L0 - 580)]), K)
        v.add(rect(88, L0 - 524, 144, 14), K)
    with S("lamp_lit"):
        v.layer(3)
        v.add(rect(126, 960 - 570, 68, 44, 4), SCREEN_T, glow=1.8, ink=True)
    with S("jetty"):
        v.layer(2)
        v.add(rect(320, 900, 900, 28), K)
        for x in (340, 600, 860, 1160):
            v.add(rect(x, 900, 22, 100), K)
        v.add(rect(1180, 840, 28, 66), K)
    with S("moon"):
        v.layer(2)
        v.add(ellipse(1340, 660, 70), SCREEN_T, glow=0.9, ink=True)
    with S("moon_crescent"):
        v.layer(2)
        v.add(ellipse(1340, 840, 70).difference(ellipse(1368, 826, 62)), SCREEN_T, glow=0.9, ink=True)
    with S("moth"):
        v.layer(2)
        moth(v, 1480, 540, 0.9, color=K)
    with S("cloud"):
        v.layer(2)
        for (cx, cy, rx, ry) in ((500, 140, 190, 70), (380, 170, 130, 60), (640, 170, 150, 56), (520, 200, 250, 50)):
            v.add(ellipse(cx, cy, rx, ry), K)
    with S("bolt"):
        v.layer(3)
        v.add(poly([(900, 40), (850, 170), (890, 170), (840, 310), (930, 150), (890, 150)]), "#fff7d8", glow=2.0, ink=True)
    with S("window"):
        v.layer(2)
        v.add(union(rect(1020, 400, 220, 340), ellipse(1130, 400, 110, 110)), K)
        v.add(union(rect(1036, 416, 188, 324), ellipse(1130, 410, 94, 94)), "#3a2a18", ink=True)
        v.add(rect(1124, 410, 12, 330), K); v.add(rect(1036, 560, 188, 12), K)
    with S("desk"):
        v.layer(2)
        v.add(rect(1260, 640, 280, 30), K)
        v.add(rect(1280, 670, 24, 120), K); v.add(rect(1500, 670, 24, 120), K)
        v.add(rect(1330, 620, 100, 22, 3), K)
    with S("clock_small"):
        v.layer(2)
        v.add(ring(1260, 560, 70, 56), K)
        v.add(line([(1260, 560), (1260, 510)], 8), K)
        v.add(line([(1260, 560), (1290, 580)], 8), K)
    with S("bell"):
        v.layer(2)
        v.add(union(ellipse(900, 600, 90, 80), rect(810, 590, 180, 50, 10)), K)
        v.add(ellipse(900, 650, 14, 14), K)
    with S("hand"):
        v.layer(2)
        v.add(rect(1062, 120, 36, 170, 8), K); v.add(ellipse(1080, 120, 46, 40), K)
        for k in range(5):
            v.add(rot(rect(1068 + (k - 2) * 24 - 4, 40, 14, 100, 7), (k - 2) * 20, origin=(1080, 120)), K)
    with S("rain"):
        v.layer(2)
        rnd = random.Random(8)
        for _ in range(70):
            x = rnd.random() * 1400; y = rnd.random() * 700
            v.add(line([(x, y), (x - 20, y + 70)], 3), K)
    with S("table_lamp"):
        v.layer(2)
        v.add(rect(60, 800, 280, 26), K); v.add(rect(80, 826, 24, 150), K); v.add(rect(296, 826, 24, 150), K)
        v.add(rect(180, 740, 44, 62, 5), K); v.add(poly([(170, 740), (234, 740), (214, 690), (190, 690)]), K)
        v.add(ellipse(202, 722, 14, 18), SCREEN_T, glow=2.0, ink=True)
    return v

@view("end_dawn", CH)
def end_dawn():
    """Ending A: the first morning on the lake"""
    v = View("end_dawn", CH, kind="ending")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#f3b78a", grad="#9fc3d0")
    v.layer(1)
    v.add(ellipse(1100, 560, 140), "#fff0c0", glow=0.8, ink=True)
    v.add(poly([(0, 560), (300, 530), (700, 548), (1000, 520), (1600, 545), (1600, 600), (0, 600)]), "#5d7b86")
    v.layer(2)
    v.rect(0, 600, 1600, 400, "#7fa5b3", grad="#cfa68f")
    for i in range(14):
        v.ink(rect(40 + (i * 117) % 1500, 640 + i * 24, 140 + (i % 3) * 70, 5), "#e8d3c0")
    # the far light, small and pale on its rock
    v.layer(3)
    v.add(poly([(1280, 600), (1296, 440), (1324, 440), (1340, 600)]), "#e7ddcd")
    v.add(rect(1288, 416, 44, 28, 4), "#3a2d24"); v.add(poly([(1282, 416), (1310, 392), (1338, 416)]), "#3a2d24")
    v.ink(rect(1296, 420, 28, 20), "#f9ecb8")
    # the jetty in the foreground
    v.layer(3)
    v.rect(0, 840, 900, 40, "#6b5543", grad="#56432f")
    for x in (60, 360, 700):
        v.rect(x, 880, 34, 120, "#3a2d24")
    v.dark = "0.0"
    return v

@view("end_jetty", CH)
def end_jetty():
    v = View("end_jetty", CH, kind="ending")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#f6c79b", grad="#a9cdd6")
    v.layer(1)
    v.rect(0, 560, 1600, 440, "#86adba", grad="#d6b49d")
    for i in range(16):
        v.ink(rect(30 + (i * 109) % 1500, 600 + i * 22, 140 + (i % 3) * 80, 5), "#f0ddc8")
    v.layer(3)
    v.rect(0, 760, 1180, 46, "#7a624c", grad="#5e4a38")
    for x in range(0, 1180, 100):
        v.ink(rect(x, 760, 3, 46), "#3a2d24")
    for x in (40, 360, 700, 1060):
        v.rect(x, 806, 36, 200, "#3a2d24")
    v.layer(4)
    v.rect(1060, 700, 36, 66, "#3a3d3f", r=6)
    with v.sprite("ferry_end", shadow=False):
        v.layer(5)
        v.add(poly([(940, 760), (1560, 760), (1500, 690), (1000, 690)]), "#2f2a30")
        v.add(rect(1080, 590, 340, 100, 10), "#e8dcc4")
        for k in range(6):
            v.add(rect(1100 + k * 52, 610, 34, 44, 4), "#fdeab8", glow=1.0, ink=True)
        v.add(rect(1230, 520, 22, 70), "#2f2a30")
        v.add(rect(1000, 700, 580, 16), "#8a2f2a")
    v.dark = "0.0"
    return v

@view("end_two_lights", CH)
def end_two_lights():
    v = View("end_two_lights", CH, kind="ending")
    v.layer(0)
    v.rect(0, 0, 1600, 1000, "#0b1b25", grad="#244553")
    rnd = random.Random(12)
    for _ in range(80):
        v.ink(ellipse(rnd.random() * 1600, rnd.random() * 460, 1.7, 1.7), "#d3dccf")
    v.layer(1)
    v.rect(0, 540, 1600, 460, "#16323f", grad="#050d12")
    for i in range(12):
        v.ink(rect(30 + (i * 133) % 1500, 590 + i * 30, 150 + (i % 3) * 70, 4), "#2d5a68")
    # the far light, lit, on its rock (right)
    v.layer(3)
    v.add(poly([(1180, 560), (1200, 360), (1240, 360), (1260, 560)]), "#c9c3ad")
    v.add(rect(1196, 330, 52, 34, 5), "#2b2018"); v.add(poly([(1190, 330), (1222, 300), (1254, 330)]), "#2b2018")
    v.add(rect(1208, 336, 28, 22), "#fff0b8", glow=3.0, ink=True)
    v.layer(4)
    v.add(poly([(1218, 346), (200, 250), (200, 450)]), "#ffe9a8", glow=0.5, ink=True, alpha=1)
    # the jetty (left, near) and the second light, crossing the water
    v.layer(3)
    v.rect(0, 840, 620, 40, "#6b5543")
    for x in (50, 300, 560):
        v.rect(x, 880, 34, 120, "#3a2d24")
    with v.sprite("second_light", shadow=False, fx="pulse"):
        v.layer(5)
        v.add(ellipse(800, 700, 22, 22), "#fff0b8", glow=4.0, ink=True)
        v.add(ellipse(800, 700, 60, 60), "#ffd890", glow=0.5, ink=True)
        v.add(poly([(740, 760), (860, 760), (830, 716), (770, 716)]), "#2f2a30")
    v.dark = "0.0"
    return v

@view("album_photo", CH)
def album_photo():
    """the photograph of Ruth and Tomas on the ferry deck (ten fragments)"""
    v = View("album_photo", CH, size=(1000, 600), kind="photo")
    v.layer(0)
    v.rect(0, 0, 1000, 600, "#b9ae8e", grad="#8e8266")
    v.layer(1)
    v.rect(0, 360, 1000, 240, "#6e7a72", grad="#4d5a54")                 # the lake, grey
    v.ink(rect(0, 356, 1000, 6), "#d6ceb4", d=1)
    for k in range(6):
        v.ink(rect(40 + k * 160, 420 + (k % 3) * 40, 110, 4), "#8f9b92", d=1)
    # the ferry deck: planks, a rail, a lifebelt
    v.layer(2)
    v.add(poly([(0, 600), (0, 430), (1000, 430), (1000, 600)]), "#8a6a46", grad="#664a30")
    for k in range(10):
        v.ink(line([(k * 110 - 20, 600), (k * 70 + 120, 430)], 4), "#4a3420", d=2)
    v.layer(3)
    v.rect(0, 300, 1000, 14, "#2f2a30")
    for x in range(0, 1000, 120):
        v.rect(x, 300, 10, 140, "#2f2a30")
    v.add(ring(880, 400, 44, 26), "#c9453a")
    # two figures, shoulder to shoulder
    def fig(x, h, hat, bun, col):
        v.add(poly([(x - 56, 560), (x - 36, 560 - h * 0.62), (x + 36, 560 - h * 0.62), (x + 56, 560)]), col)
        v.add(ellipse(x, 560 - h * 0.62 - 34, 28, 32), "#d6a98a")
        if hat:
            v.add(poly([(x - 34, 560 - h * 0.62 - 56), (x + 34, 560 - h * 0.62 - 56), (x + 26, 560 - h * 0.62 - 84), (x - 26, 560 - h * 0.62 - 84)]), "#2b2018")
        if bun:
            v.add(ellipse(x - 20, 560 - h * 0.62 - 62, 14, 14), "#2b2018")
            v.add(arc(x, 560 - h * 0.62 - 38, 30, 200, 340, 8), "#2b2018")
        v.ink(ellipse(x - 10, 560 - h * 0.62 - 36, 3.5, 3.5), INK, d=4); v.ink(ellipse(x + 10, 560 - h * 0.62 - 36, 3.5, 3.5), INK, d=4)
        v.ink(arc(x, 560 - h * 0.62 - 26, 10, 20, 160, 3), "#8a4a3a", d=4)
    v.layer(4)
    fig(420, 330, False, True, "#3a4a5a")
    fig(550, 360, True, False, "#6a3a2f")
    v.add(line([(470, 470), (505, 480)], 16), "#3a4a5a")
    v.dark = "0.0"
    return v
