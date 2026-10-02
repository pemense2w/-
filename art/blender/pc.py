"""
pc.py - the "paper-cut" scene builder for Still Water.

Every picture in the game is built here as stacked flat paper shapes (shapely
geometry, no outlines), lit by one soft key light and rendered by Blender's
Cycles through the `bpy` module.  The same scene scripts that draw a view also
declare its hotspots, lights, text slots and widgets, which are exported as JSON
for the Godot project - so art and interaction can never drift apart.

Coordinates are pixels on a 1600x1000 canvas, y pointing DOWN (like Godot).

Run via build.py, not directly.
"""
import os, sys, json, math, hashlib, random
from contextlib import contextmanager

from shapely.geometry import Polygon, MultiPolygon, Point, LineString, box, GeometryCollection
from shapely import affinity
from shapely.ops import unary_union

PX = 0.01            # blender units per pixel
DZ = 0.1           # paper "depth" per layer index (BU)
INK = 0.0012         # z step between shapes of one layer
ENGINE_VERSION = "pc-7"

OUT_ART = os.environ.get("SW_ART_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "assets", "art"))
OUT_DATA = os.environ.get("SW_DATA_OUT", os.path.join(os.path.dirname(__file__), "..", "..", "assets", "data"))
CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", ".cache.json")

# --------------------------------------------------------------------- colours
def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4))

def rgb2hex(c):
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(v * 255)))) for v in c)

def col(c):
    if isinstance(c, str):
        return hex2rgb(c)
    return tuple(c)

def mix(a, b, t):
    a, b = col(a), col(b)
    return rgb2hex(tuple(a[i] * (1 - t) + b[i] * t for i in range(3)))

def shade(c, f):
    """f<0 darker (toward black), f>0 lighter (toward white)."""
    c = col(c)
    if f < 0:
        return rgb2hex(tuple(v * (1 + f) for v in c))
    return rgb2hex(tuple(v + (1 - v) * f for v in c))

def tint(c, t, amt):
    return mix(c, t, amt)

def _lin(v):
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

# ------------------------------------------------------------------- geometry
def rect(x, y, w, h, r=0):
    if r <= 0:
        return box(x, y, x + w, y + h)
    r = min(r, w / 2, h / 2)
    return box(x + r, y + r, x + w - r, y + h - r).buffer(r, resolution=8)

def ellipse(cx, cy, rx, ry=None):
    ry = rx if ry is None else ry
    return affinity.scale(Point(cx, cy).buffer(1, resolution=20), rx, ry)

def poly(pts, holes=None):
    return Polygon(pts, holes or None).buffer(0)

def ring(cx, cy, r1, r2):
    return Point(cx, cy).buffer(r1, resolution=24).difference(Point(cx, cy).buffer(r2, resolution=24))

def line(pts, w, cap="round"):
    return LineString(pts).buffer(w / 2, resolution=6, cap_style=1 if cap == "round" else 2, join_style=1)

def arc(cx, cy, r, a0, a1, w, n=24):
    """stroke along a circle arc; angles in degrees, 0 = +x (right), 90 = down (screen)"""
    pts = [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return line(pts, w)

def sector(cx, cy, r, a0, a1, n=24):
    pts = [(cx, cy)] + [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                         cy + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return Polygon(pts).buffer(0)

def rot(g, deg, origin=None):
    return affinity.rotate(g, deg, origin=origin or "center")

def move(g, dx, dy):
    return affinity.translate(g, dx, dy)

def scl(g, sx, sy=None, origin=None):
    return affinity.scale(g, sx, sx if sy is None else sy, origin=origin or "center")

def union(*gs):
    return unary_union(list(gs))

def diff(a, b):
    return a.difference(b)

def inter(a, b):
    return a.intersection(b)

def wave(x0, x1, y, amp, period, thick, phase=0.0, n=40):
    pts = [(x0 + (x1 - x0) * i / n, y + amp * math.sin((x0 + (x1 - x0) * i / n) / period * math.tau + phase)) for i in range(n + 1)]
    return line(pts, thick)

def stripes(region, angle, spacing, width, offset=0.0):
    minx, miny, maxx, maxy = region.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    R = math.hypot(maxx - minx, maxy - miny)
    bars = []
    k = -int(R / spacing) - 1
    while k * spacing < R + spacing:
        p = k * spacing + offset
        bars.append(box(cx - R, cy + p - width / 2, cx + R, cy + p + width / 2))
        k += 1
    return inter(rot(unary_union(bars), angle, origin=(cx, cy)), region)

def dots(region, spacing, r, offset=(0, 0)):
    minx, miny, maxx, maxy = region.bounds
    ds = []
    y = miny + spacing / 2 + offset[1]
    row = 0
    while y < maxy:
        x = minx + spacing / 2 + (spacing / 2 if row % 2 else 0) + offset[0]
        while x < maxx:
            ds.append(Point(x, y).buffer(r, resolution=6))
            x += spacing
        y += spacing * 0.87
        row += 1
    return inter(unary_union(ds), region)

def chevrons(region, spacing, thick, depth=None):
    minx, miny, maxx, maxy = region.bounds
    depth = depth or spacing * 0.6
    cx = (minx + maxx) / 2
    shapes = []
    y = miny
    while y < maxy + spacing:
        pts = [(minx - 10, y), (cx, y + depth), (maxx + 10, y)]
        shapes.append(line(pts, thick, cap="flat"))
        y += spacing
    return inter(unary_union(shapes), region)

def bbox(g):
    return g.bounds  # minx, miny, maxx, maxy

# ----------------------------------------------------------------- scene model
class Shape:
    __slots__ = ("geom", "color", "grad", "d", "ink", "glow", "group", "variant", "z", "name", "alpha", "grad_dir")
    def __init__(self, **kw):
        for k in self.__slots__:
            setattr(self, k, kw.get(k))

class View:
    """One picture (background + sprites + metadata)."""

    def __init__(self, id, chapter, size=(1600, 1000), kind="view", back=None, left=None, right=None,
                 bg_color="#000000", has_bg=True, meta=None):
        self.id = id
        self.chapter = chapter
        self.size = size
        self.kind = kind
        self.nav = {"back": back, "left": left, "right": right}
        self.shapes = []
        self.hotspots = []
        self.lights = []
        self.texts = []
        self.widgets = []
        self.sprites = {}            # id -> dict(show, pivot, shadow, group)
        self.refs = []               # placed copies of sprites from another (sheet) view
        self.variants = {}           # name -> when expr
        self.variant_default = None
        self._group = "bg"
        self._variant = None
        self._d = 0
        self.meta = meta or {}
        self.bg_color = bg_color
        self.has_bg = has_bg
        self.dark = None             # expr -> darkness 0..1 (godot)
        self.ambient = None

    # --- drawing ---------------------------------------------------------
    def add(self, geom, color, d=None, grad=None, glow=0.0, ink=False, alpha=1.0, grad_dir="v"):
        if geom is None or geom.is_empty:
            return geom
        geom, color, grad = self._xf(geom, color, grad)
        d = self._d if d is None else d
        self.shapes.append(Shape(geom=geom, color=col(color), grad=(col(grad) if grad else None), d=d, ink=ink,
                                 glow=glow, group=self._group, variant=self._variant, alpha=alpha, grad_dir=grad_dir,
                                 z=len(self.shapes)))
        return geom

    def _xf(self, geom, color, grad):
        """hook for subclasses (mirroring / recolouring)"""
        return geom, color, grad

    def layer(self, d):
        """set the default paper layer for following shapes"""
        self._d = d
        return self

    # convenience wrappers; all return the shapely geometry
    def rect(self, x, y, w, h, color, r=0, **kw):
        return self.add(rect(x, y, w, h, r), color, **kw)

    def ellipse(self, cx, cy, rx, ry, color, **kw):
        return self.add(ellipse(cx, cy, rx, ry), color, **kw)

    def poly(self, pts, color, **kw):
        return self.add(poly(pts), color, **kw)

    def ring(self, cx, cy, r1, r2, color, **kw):
        return self.add(ring(cx, cy, r1, r2), color, **kw)

    def line(self, pts, w, color, **kw):
        return self.add(line(pts, w), color, **kw)

    def ink(self, geom, color, **kw):
        return self.add(geom, color, ink=True, **kw)

    # --- grouping ---------------------------------------------------------
    @contextmanager
    def sprite(self, id, show=None, pivot=None, shadow=True, d=None, pad=0, fx=None, z=0):
        prev = self._group, self._d
        self._group = "spr:" + id
        if d is not None:
            self._d = d
        self.sprites[id] = dict(show=show, pivot=pivot, shadow=shadow, pad=pad, fx=fx, z=z)
        try:
            yield self
        finally:
            self._group, self._d = prev

    @contextmanager
    def variant(self, name):
        prev = self._variant
        self._variant = name
        try:
            yield self
        finally:
            self._variant = prev

    def variants_when(self, mapping, default):
        """mapping: name -> godot expression; default variant name"""
        self.variants = mapping
        self.variant_default = default

    def ref(self, id, sheet, sid, x, y, scale=1.0, show=None, alpha=1.0, anchor="bc", fx=None, tint=None):
        """place a sprite that lives in another view (a sheet), e.g. landmarks reused in four views"""
        self.refs.append(dict(id=id, sheet=sheet, sid=sid, x=x, y=y, scale=scale, show=show, alpha=alpha, anchor=anchor, fx=fx, tint=tint))

    # --- semantic data -----------------------------------------------------
    def hot(self, id, geom, when=None, min_size=88, label=None, kind=None, poly_hit=False):
        if isinstance(geom, (tuple, list)):
            x, y, w, h = geom
            r = [x, y, w, h]
        else:
            minx, miny, maxx, maxy = geom.bounds
            r = [minx, miny, maxx - minx, maxy - miny]
        # enforce comfortable touch size (design rule 4: no pixel hunting)
        if r[2] < min_size:
            r[0] -= (min_size - r[2]) / 2; r[2] = min_size
        if r[3] < min_size:
            r[1] -= (min_size - r[3]) / 2; r[3] = min_size
        self.hotspots.append(dict(id=id, rect=[round(v, 1) for v in r], when=when, kind=kind))

    def light(self, x, y, r, color="#ffb45a", when=None, intensity=1.0, flicker=0.0, hole=1.0):
        self.lights.append(dict(x=x, y=y, r=r, color=rgb2hex(col(color)), when=when, intensity=intensity,
                                flicker=flicker, hole=hole))

    def text(self, id, key, rect_, size=32, color="#e8dcc0", rot=0, font="world", align="center",
             when=None, literal=None, spacing=0, outline=None):
        self.texts.append(dict(id=id, key=key, rect=list(rect_), size=size, color=rgb2hex(col(color)), rot=rot,
                               font=font, align=align, when=when, literal=literal, spacing=spacing, outline=outline))

    def widget(self, id, kind, rect_, when=None, **args):
        self.widgets.append(dict(id=id, kind=kind, rect=list(rect_), when=when, args=args))

    # --- signature for cache ---------------------------------------------
    def signature(self):
        h = hashlib.sha1()
        h.update(ENGINE_VERSION.encode())
        h.update(repr(self.size).encode())
        for s in self.shapes:
            h.update(s.geom.wkb)
            h.update(repr((s.color, s.grad, s.d, s.ink, s.glow, s.group, s.variant, s.alpha, s.grad_dir)).encode())
        h.update(repr(sorted((k, v["pivot"], v["shadow"], v["pad"], v["fx"], v["z"]) for k, v in self.sprites.items())).encode())
        return h.hexdigest()

    # --- export ------------------------------------------------------------
    def _ref_json(self):
        out = []
        for r in self.refs:
            mp = os.path.join(OUT_DATA, "_views", r["sheet"] + ".json")
            if not os.path.exists(mp):
                continue
            sh = json.load(open(mp))
            sd = next((s for s in sh["sprites"] if s["id"] == r["sid"] and "tex" in s), None)
            if sd is None:
                continue
            out.append(dict(id=r["id"], show=r["show"], fx=r["fx"], z=0, tex=sd["tex"], rect=[0, 0, sd["rect"][2], sd["rect"][3]],
                            pivot=None, ref=True, pos=[r["x"], r["y"]], anchor=r["anchor"], scale=r["scale"], alpha=r["alpha"], tint=r["tint"]))
        return out

    def to_json(self, sprite_meta, bg_files):
        return dict(
            id=self.id, chapter=self.chapter, kind=self.kind, size=list(self.size), nav=self.nav,
            bg=bg_files, hotspots=self.hotspots, lights=self.lights, texts=self.texts, widgets=self.widgets,
            sprites=[dict(id=k, show=v["show"], fx=v["fx"], z=v["z"], **sprite_meta.get(k, {})) for k, v in self.sprites.items()
                     if k in sprite_meta] + self._ref_json(),
            meta=self.meta, dark=self.dark, ambient=self.ambient,
        )


# --------------------------------------------------------------- bpy renderer
_bpy = None
_mat_cache = {}

def _init_bpy():
    global _bpy
    if _bpy is not None:
        return _bpy
    import bpy
    _bpy = bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy

def _setup_scene(bpy, size, draft, samples):
    sc = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        bpy.data.meshes.remove(m)
    for c in list(bpy.data.cameras):
        bpy.data.cameras.remove(c)
    for l in list(bpy.data.lights):
        bpy.data.lights.remove(l)
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.use_denoising = True
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
    sc.cycles.max_bounces = 2
    sc.cycles.diffuse_bounces = 1
    sc.cycles.glossy_bounces = 0
    sc.cycles.transmission_bounces = 0
    sc.cycles.transparent_max_bounces = 2
    sc.cycles.use_light_tree = False
    sc.render.resolution_x = size[0]
    sc.render.resolution_y = size[1]
    sc.render.resolution_percentage = 50 if draft else 100
    sc.view_settings.view_transform = "Standard"
    sc.view_settings.look = "None"
    sc.display_settings.display_device = "sRGB"
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.image_settings.color_depth = "8"
    sc.render.film_transparent = False
    sc.render.use_border = False
    sc.render.use_crop_to_border = False
    # camera
    cam = bpy.data.cameras.new("cam")
    cam.type = "ORTHO"
    cam.ortho_scale = max(size) * PX
    co = bpy.data.objects.new("cam", cam)
    sc.collection.objects.link(co)
    co.location = (size[0] * PX / 2, size[1] * PX / 2, 30)
    co.rotation_euler = (0, 0, 0)
    sc.camera = co
    # key light: a soft sun from the top-left, 38 deg off vertical
    ld = bpy.data.lights.new("key", "SUN")
    ld.energy = 1.7
    ld.angle = math.radians(16)
    ld.color = (1.0, 0.97, 0.92)
    lo = bpy.data.objects.new("key", ld)
    sc.collection.objects.link(lo)
    import mathutils
    dvec = mathutils.Vector((0.42, -0.58, -0.80))        # travels right+down => shadows fall to the bottom-right
    lo.rotation_euler = dvec.to_track_quat("-Z", "Y").to_euler()
    # world ambient
    w = bpy.data.worlds.get("W") or bpy.data.worlds.new("W")
    w.use_nodes = True
    bgn = w.node_tree.nodes["Background"]
    bgn.inputs["Color"].default_value = (1, 1, 1, 1)
    bgn.inputs["Strength"].default_value = 0.62
    sc.world = w
    return sc

def _material(bpy, color, grad, glow, grad_dir, alpha):
    key = (tuple(round(v, 4) for v in color), tuple(round(v, 4) for v in grad) if grad else None,
           round(glow, 3), grad_dir, round(alpha, 3))
    m = _mat_cache.get(key)
    if m is not None:
        return m
    m = bpy.data.materials.new("m%d" % len(_mat_cache))
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    lc = tuple(_lin(v) for v in color)
    if grad:
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Generated"], sep.inputs["Vector"])
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].color = (*tuple(_lin(v) for v in color), 1)
        ramp.color_ramp.elements[1].color = (*tuple(_lin(v) for v in grad), 1)
        # generated Y runs bottom(0) -> top(1); "v": color at top, grad at bottom
        axis = {"v": "Y", "h": "X"}[grad_dir]
        if grad_dir == "v":
            inv = nt.nodes.new("ShaderNodeMath"); inv.operation = "SUBTRACT"; inv.inputs[0].default_value = 1.0
            nt.links.new(sep.outputs[axis], inv.inputs[1])
            nt.links.new(inv.outputs[0], ramp.inputs["Fac"])
        else:
            nt.links.new(sep.outputs[axis], ramp.inputs["Fac"])
        colsock = ramp.outputs["Color"]
    else:
        rgb = nt.nodes.new("ShaderNodeRGB")
        rgb.outputs[0].default_value = (*lc, 1)
        colsock = rgb.outputs[0]
    if glow > 0:
        em = nt.nodes.new("ShaderNodeEmission")
        nt.links.new(colsock, em.inputs["Color"])
        em.inputs["Strength"].default_value = glow
        surf = em.outputs[0]
    else:
        # subtle hand-made mottling so large flat areas feel like paper, not vector fill
        tcn = nt.nodes.new("ShaderNodeTexCoord")
        nz = nt.nodes.new("ShaderNodeTexNoise")
        nz.inputs["Scale"].default_value = 1.1
        nz.inputs["Detail"].default_value = 4.0
        nz.inputs["Roughness"].default_value = 0.6
        nt.links.new(tcn.outputs["Object"], nz.inputs["Vector"])
        mr = nt.nodes.new("ShaderNodeMapRange")
        mr.inputs["From Min"].default_value = 0.35
        mr.inputs["From Max"].default_value = 0.65
        mr.inputs["To Min"].default_value = 0.93
        mr.inputs["To Max"].default_value = 1.05
        nt.links.new(nz.outputs["Fac"], mr.inputs["Value"])
        vm = nt.nodes.new("ShaderNodeVectorMath")
        vm.operation = "SCALE"
        nt.links.new(colsock, vm.inputs[0])
        nt.links.new(mr.outputs["Result"], vm.inputs["Scale"])
        df = nt.nodes.new("ShaderNodeBsdfDiffuse")
        nt.links.new(vm.outputs[0], df.inputs["Color"])
        surf = df.outputs[0]
    nt.links.new(surf, out.inputs["Surface"])
    _mat_cache[key] = m
    return m

def _poly_to_mesh(bpy, geom, z, name):
    import mathutils
    from mathutils import Vector
    me = bpy.data.meshes.new(name)
    verts, faces = [], []
    polys = []
    if geom.geom_type == "Polygon":
        polys = [geom]
    elif hasattr(geom, "geoms"):
        for g in geom.geoms:
            if g.geom_type == "Polygon":
                polys.append(g)
            elif hasattr(g, "geoms"):
                polys.extend(p for p in g.geoms if p.geom_type == "Polygon")
    H = None
    for p in polys:
        if p.is_empty or p.area < 0.05:
            continue
        rings = [list(p.exterior.coords)[:-1]] + [list(i.coords)[:-1] for i in p.interiors]
        base = len(verts)
        lines = []
        for r_ in rings:
            lines.append([Vector((x * PX, -y * PX, 0)) for x, y in r_])
        tris = mathutils.geometry.tessellate_polygon(lines)
        flat = [v for ln in lines for v in ln]
        for v in flat:
            verts.append((v.x, v.y, 0.0))
        for t in tris:
            faces.append((base + t[0], base + t[1], base + t[2]))
    me.from_pydata(verts, [], faces)
    me.update()
    return me

def render_view(v, draft=False, samples=10, force=False, only=None, verbose=True):
    """Render a View: background variants + sprite groups.  Returns metadata dict."""
    from PIL import Image, ImageFilter
    bpy = _init_bpy()
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            cache = json.load(open(CACHE_FILE))
        except Exception:
            cache = {}
    sig = v.signature() + ("-draft" if draft else "")
    outdir = os.path.join(OUT_ART, v.chapter)
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(OUT_DATA, exist_ok=True)
    meta_path = os.path.join(OUT_DATA, "_views", v.id + ".json")
    os.makedirs(os.path.dirname(meta_path), exist_ok=True)

    if not force and cache.get(v.id) == sig and os.path.exists(meta_path) and (only is None):
        # art unchanged: only refresh the JSON (hotspots etc. may have changed)
        old = json.load(open(meta_path))
        data = v.to_json({s["id"]: {k: s[k] for k in s if k not in ("id", "show", "fx", "z")} for s in old["sprites"]}, old["bg"])
        json.dump(data, open(meta_path, "w"), indent=1)
        if verbose:
            print(f"  = {v.id} (cached)")
        return data

    sc = _setup_scene(bpy, v.size, draft, samples)
    W, H = v.size
    # build objects, tracking by (group, variant)
    objs = []
    for i, s in enumerate(v.shapes):
        z = s.d * DZ + (s.z * INK)
        me = _poly_to_mesh(bpy, s.geom, 0, f"s{i}")
        if not me.vertices:
            bpy.data.meshes.remove(me)
            continue
        o = bpy.data.objects.new(f"s{i}", me)
        sc.collection.objects.link(o)
        o.location = (0, H * PX, z)
        o.data.materials.append(_material(bpy, s.color, s.grad, s.glow, s.grad_dir, s.alpha))
        if s.ink:
            o.visible_shadow = False
        objs.append((o, s))

    def show(pred):
        for o, s in objs:
            vis = pred(s)
            o.hide_render = not vis
            o.hide_viewport = not vis

    def save_img(path_png, final_path, sprite=False, shadow=True, offset=(0, 0)):
        im = Image.open(path_png).convert("RGBA")
        return im

    # background variants
    names = [None]
    if v.variants:
        names = list(v.variants.keys())
        if v.variant_default not in names:
            names.append(v.variant_default)
    bg_files = []
    tmp = os.path.join(os.path.dirname(__file__), "..", ".tmp")
    os.makedirs(tmp, exist_ok=True)
    sc.render.film_transparent = False
    sc.render.use_border = False
    sc.render.use_crop_to_border = False
    bgcol = tuple(_lin(c) for c in col(v.bg_color))
    if not v.has_bg:
        names = []
    for vn in names:
        if only is not None and vn not in only and ("bg" not in only):
            continue
        show(lambda s, vn=vn: s.group == "bg" and (s.variant is None or s.variant == vn))
        fname = v.id if (vn is None or vn == v.variant_default and len(names) == 1) else f"{v.id}__{vn}"
        tmp_png = os.path.join(tmp, fname + ".png")
        sc.render.filepath = tmp_png
        bpy.ops.render.render(write_still=True)
        im = Image.open(tmp_png).convert("RGB")
        if im.size != tuple(v.size):
            im = im.resize(tuple(v.size), Image.BICUBIC)
        out = os.path.join(outdir, fname + ".webp")
        im.save(out, "WEBP", quality=86, method=4)
        bg_files.append(dict(variant=vn, tex=f"{v.chapter}/{fname}.webp",
                             when=(v.variants.get(vn) if vn != v.variant_default else None)))
        if verbose:
            print(f"  + {fname}.webp")
    # default variant must come last (first match wins)
    if v.variants:
        bg_files.sort(key=lambda b: 1 if b["when"] is None else 0)

    # sprites
    sprite_meta = {}
    sc.render.film_transparent = True
    for sid, sp in v.sprites.items():
        grp = "spr:" + sid
        shapes = [s for s in v.shapes if s.group == grp]
        if not shapes:
            continue
        if only is not None and sid not in only:
            # keep meta from previous
            continue
        geom = unary_union([s.geom for s in shapes])
        minx, miny, maxx, maxy = geom.bounds
        shadow = sp["shadow"]
        pad = sp["pad"]
        padl, padt, padr, padb = (pad + 4, pad + 4, pad + 40, pad + 44) if shadow else (pad + 2,) * 4
        x0 = max(0, int(math.floor(minx - padl)))
        y0 = max(0, int(math.floor(miny - padt)))
        x1 = min(W, int(math.ceil(maxx + padr)))
        y1 = min(H, int(math.ceil(maxy + padb)))
        show(lambda s, grp=grp: s.group == grp)
        sc.render.use_border = True
        sc.render.use_crop_to_border = True
        sc.render.border_min_x = x0 / W
        sc.render.border_max_x = x1 / W
        sc.render.border_min_y = 1 - y1 / H
        sc.render.border_max_y = 1 - y0 / H
        tmp_png = os.path.join(tmp, f"{v.id}__{sid}.png")
        sc.render.filepath = tmp_png
        bpy.ops.render.render(write_still=True)
        im = Image.open(tmp_png).convert("RGBA")
        scale = im.size[0] / (x1 - x0)
        if shadow:
            a = im.split()[3]
            sh = Image.new("RGBA", im.size, (8, 6, 14, 0))
            sa = a.filter(ImageFilter.GaussianBlur(7 * scale)).point(lambda p: int(p * 0.42))
            sh.putalpha(sa)
            offs = (int(7 * scale), int(10 * scale))
            canvas = Image.new("RGBA", im.size, (0, 0, 0, 0))
            canvas.alpha_composite(sh, offs)
            canvas.alpha_composite(im)
            im = canvas
        if scale != 1.0:
            im = im.resize((x1 - x0, y1 - y0), Image.LANCZOS)
        out = os.path.join(outdir, f"{v.id}__{sid}.webp")
        im.save(out, "WEBP", quality=88, method=4, alpha_quality=100)
        piv = sp["pivot"]
        sprite_meta[sid] = dict(tex=f"{v.chapter}/{v.id}__{sid}.webp", rect=[x0, y0, x1 - x0, y1 - y0],
                                pivot=(list(piv) if piv else None))
        if verbose:
            print(f"  + {v.id}__{sid}.webp  {x1 - x0}x{y1 - y0}")
    sc.render.use_border = False
    sc.render.use_crop_to_border = False

    # merge in prior sprite meta when partial render
    if only is not None and os.path.exists(meta_path):
        old = json.load(open(meta_path))
        for s in old["sprites"]:
            if s["id"] not in sprite_meta:
                sprite_meta[s["id"]] = {k: s[k] for k in s if k not in ("id", "show", "fx", "z")}
        if not bg_files:
            bg_files = old["bg"]
    data = v.to_json(sprite_meta, bg_files)
    json.dump(data, open(meta_path, "w"), indent=1)
    cache[v.id] = sig
    json.dump(cache, open(CACHE_FILE, "w"))

    # cleanup
    for o, s in objs:
        bpy.data.objects.remove(o, do_unlink=True)
    for m in list(bpy.data.meshes):
        bpy.data.meshes.remove(m)
    return data
