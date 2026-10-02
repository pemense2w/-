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

@item("pell_jar")
def _pell_jar(v):
    v.layer(1)
    v.add(jar_shape(110, 70, 170, 230), "#a9c6c6")
    v.ink(jar_shape(124, 86, 142, 198), "#2f6f80")
    v.add(rect(124, 56, 142, 26, 6), "#a8825a")
    pell_fish(v, 196, 200, 0.62, facing=1)

@item("rag")
def _rag(v):
    v.layer(1)
    v.add(poly([(110, 140), (270, 110), (300, 210), (260, 290), (150, 300), (100, 230)]), "#cfc4a3")
    v.ink(poly([(140, 170), (250, 150), (270, 220), (190, 270)]), "#bdb08c")
    v.ink(line([(130, 220), (240, 190)], 7), "#7a6b4a")

@item("tar")
def _tar(v):
    v.layer(1)
    v.add(poly([(110, 270), (280, 270), (300, 170), (90, 170)]), IRON)
    v.add(ellipse(195, 170, 105, 30), "#1d1815")
    v.ink(ellipse(180, 164, 45, 8), "#6a5a4a")
    v.add(arc(195, 170, 105, 180, 360, 12), IRON)

@item("patch")
def _patch(v):
    v.layer(1)
    v.add(ellipse(192, 192, 110, 86), "#1d1815")
    for k in range(5):
        v.ink(line([(110 + k * 40, 130), (118 + k * 40, 256)], 5), "#38302a")
    v.ink(ellipse(192, 192, 100, 76), "#26201c")

@item("corkscrew")
def _corkscrew(v):
    v.layer(1)
    v.add(line([(192, 130), (192, 310)], 16), IRON)
    for k in range(6):
        v.add(line([(150 + (k % 2) * 84, 170 + k * 22), (234 - (k % 2) * 84, 186 + k * 22)], 12), IRON)
    v.add(rect(130, 90, 124, 30, 10), "#a8825a")

@item("net")
def _net(v):
    v.layer(1)
    v.add(arc(192, 130, 110, 180, 360, 12), ROPE)
    for k in range(-4, 5):
        v.add(line([(192 + k * 24, 130), (192 + k * 14, 290)], 6), ROPE)
    for k in range(4):
        v.add(arc(192, 140 + k * 40, 100 - k * 22, 0, 180, 6), ROPE)
    v.add(line([(192, 130), (192, 50)], 12), "#8a6a46")

@item("small_fish")
def _fish(v):
    v.layer(1)
    v.add(ellipse(180, 192, 100, 48), "#c3d3d6")
    v.add(poly([(260, 192), (330, 140), (330, 244)]), "#a9bcc0")
    v.ink(ellipse(120, 182, 9, 9), INK)
    v.ink(line([(130, 214), (240, 206)], 5), "#8fa6ab")

@item("oar2")
def _oar2(v):
    v.layer(1)
    v.add(rot(rect(180, 40, 24, 300, 8), -35), "#8a6a46")
    v.add(rot(rect(140, 200, 100, 140, 40), -35, origin=(190, 190)), "#a68359")

def _gear_item(v, r, t):
    v.layer(1)
    v.add(gear_shape(192, 192, r, t, r * 0.2), "#b88a3a")
    v.ink(ring(192, 192, r * 0.34, r * 0.2), "#7a5a22")

from ch2 import gear_shape, IRON, ROPE
@item("gear_s")
def _g1(v):
    _gear_item(v, 62, 9)

@item("gear_m")
def _g2(v):
    _gear_item(v, 98, 14)

@item("gear_l")
def _g3(v):
    _gear_item(v, 140, 20)

@item("lhkey")
def _lhkey(v):
    v.layer(1)
    key(v, 150, 200, 2.6, ang=-35, color="#9aa4a6")
    v.add(poly([(250, 270), (320, 250), (330, 300), (262, 320)]), "#c9a24d")

@item("tomas_note")
def _tnote(v):
    v.layer(1)
    paper_sheet(v, 100, 70, 190, 250, "#d9cfae", ang=6, d=1, lines=5)
    v.ink(ellipse(150, 280, 40, 26), "#b8aa88")
    v.ink(ellipse(250, 120, 26, 18), "#b8aa88")

def _watch(v, working):
    v.layer(1)
    v.add(ring(192, 120, 40, 22), BRASS)
    v.add(ellipse(192, 215, 120), BRASS_D)
    v.add(ellipse(192, 215, 106), BRASS)
    v.add(ellipse(192, 215, 92), "#e8dec2")
    for i in range(12):
        a = math.radians(i * 30)
        v.ink(line([(192 + 80 * math.sin(a), 215 - 80 * math.cos(a)), (192 + 70 * math.sin(a), 215 - 70 * math.cos(a))], 4), INK)
    # hands: both pointing near 4:19
    v.ink(line([(192, 215), (192 + 38 * math.sin(math.radians(130)), 215 - 38 * math.cos(math.radians(130)))], 7), INK)
    v.ink(line([(192, 215), (192 + 66 * math.sin(math.radians(114)), 215 - 66 * math.cos(math.radians(114)))], 5), INK)
    v.ink(ellipse(192, 215, 7, 7), BRASS_D)
    if not working:
        v.ink(poly([(204, 130), (292, 215), (270, 240), (180, 150)]), "#00000000" if False else shade("#e8dec2", -0.2))
        v.ink(line([(120, 150), (160, 190)], 5), "#6a5a3a")
        v.ink(line([(260, 160), (230, 200)], 5), "#6a5a3a")
        v.ink(line([(170, 160), (215, 280)], 4), "#6a5a3a")

@item("watch")
def _w1(v):
    _watch(v, False)

@item("pocket_watch")
def _w2(v):
    _watch(v, True)

@item("stem")
def _stem(v):
    v.layer(1)
    v.add(rect(110, 182, 170, 24, 8), BRASS)
    v.add(ellipse(290, 194, 30, 30), BRASS)
    v.add(rect(88, 174, 34, 40, 6), BRASS_D)
    v.ink(rect(130, 186, 100, 4), BRASS_D)

@item("oilcan")
def _oilcan(v):
    v.layer(1)
    v.add(poly([(100, 290), (240, 290), (264, 180), (76, 180)]), "#a8abad")
    v.add(rect(150, 140, 30, 44), "#a8abad")
    v.add(line([(240, 220), (320, 160), (336, 110)], 16), "#a8abad")
    v.add(arc(100, 235, 44, 90, 270, 10), "#a8abad")
    v.ink(rect(110, 225, 120, 10), "#7a7e80")

@item("chain")
def _chain(v):
    v.layer(1)
    for k in range(9):
        v.add(ring(110 + k * 22, 190 + math.sin(k * 0.7) * 40, 26, 11), "#8a8e90")

@item("ash")
def _ash(v):
    v.layer(1)
    v.add(poly([(80, 300), (150, 200), (240, 190), (320, 300)]), "#8a8480")
    v.ink(ellipse(200, 250, 70, 26), "#a09a96")
    v.ink(ellipse(150, 280, 30, 12), "#6f6a66")

@item("letter")
def _letter(v):
    v.layer(1)
    paper_sheet(v, 90, 80, 210, 240, "#ece4c8", ang=-4, d=1, lines=7)
    v.ink(rect(120, 110, 100, 10), "#7a2a22")

@item("logpage")
def _logpage(v):
    v.layer(1)
    v.add(poly([(100, 70), (290, 60), (300, 330), (110, 340)]), "#d9cfae")
    v.ink(poly([(100, 70), (150, 80), (120, 140), (100, 120)]), "#bdb08c")
    for k in range(6):
        v.ink(line([(130, 120 + k * 36), (270 - (k % 3) * 24, 116 + k * 36)], 4), INK)

@item("timetable")
def _timetable(v):
    v.layer(1)
    paper_sheet(v, 100, 90, 190, 220, "#cfc4a3", ang=5, d=1, lines=5)
    v.ink(rect(130, 120, 100, 12), "#7a2a22")

@item("punch")
def _punch(v):
    v.layer(1)
    v.add(rect(120, 200, 160, 70, 12), "#3a3d3f")
    v.add(rect(180, 120, 24, 90, 8), "#3a3d3f")
    v.add(ellipse(192, 118, 44, 16), "#c9a24d")
    v.add(rect(130, 270, 140, 26, 4), "#6e7274")

@item("ticket_ok")
def _ticket_ok(v):
    v.layer(1)
    paper_sheet(v, 70, 130, 250, 130, "#e0d3ae", ang=8, d=1)
    v.ink(rot(rect(94, 160, 100, 12), 8, origin=(195, 195)), "#2a6a3a")
    v.add(rot(ellipse(150, 230, 12, 12), 8, origin=(195, 195)), "#10181a")
    v.add(rot(ellipse(250, 218, 12, 12), 8, origin=(195, 195)), "#10181a")
