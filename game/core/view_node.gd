class_name ViewNode
extends Control
## Builds one picture from Blender-exported data: background (with state variants), sprites, hotspots,
## text slots and puzzle widgets.  Conditions in the data are Godot expressions evaluated by G.

signal hotspot_pressed(hid: String)

const ART := "res://assets/art/"
const WIDGETS := {
	"clock": "res://game/widgets/clock_widget.gd",
	"dials": "res://game/widgets/dials_widget.gd",
	"books": "res://game/widgets/books_widget.gd",
	"tiles": "res://game/widgets/tiles_widget.gd",
	"catch": "res://game/widgets/catch_widget.gd",
	"gears": "res://game/widgets/gears_widget.gd",
	"rowing": "res://game/widgets/rowing_widget.gd",
	"compass": "res://game/widgets/compass_widget.gd",
	"rhythm": "res://game/widgets/rhythm_widget.gd",
	"beam": "res://game/widgets/beam_widget.gd",
	"punch": "res://game/widgets/punch_widget.gd",
	"valves": "res://game/widgets/valves_widget.gd",
	"mirror_books": "res://game/widgets/books_widget.gd",
	"moor": "res://game/widgets/moor_widget.gd",
	"timeswitch": "res://game/widgets/timeswitch_widget.gd",
}
static var _tex_cache := {}

var data: Dictionary = {}
var bg: TextureRect
var spr := {}
var hots: Array = []
var txts: Array = []
var wids: Array = []
var _bg_path := ""
var t := 0.0

static func tex(path: String) -> Texture2D:
	if _tex_cache.has(path):
		return _tex_cache[path]
	var full: String = ART + path
	var tx: Texture2D = null
	if ResourceLoader.exists(full):
		tx = load(full)
	_tex_cache[path] = tx
	return tx

func setup(d: Dictionary) -> void:
	data = d
	size = Vector2(d.size[0], d.size[1])
	custom_minimum_size = size
	clip_contents = true
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	bg = TextureRect.new()
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_SCALE
	bg.size = size
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bg)
	for sd in d.get("sprites", []):
		if not sd.has("tex"):
			continue
		var n := Sprite2D.new()
		n.centered = false
		n.texture = tex(sd.tex)
		var r: Array = sd.rect
		var pv = sd.get("pivot", null)
		if sd.get("ref", false):
			# a copy of a sprite from a sheet view, placed by anchor point and scale
			var p: Array = sd.pos
			n.position = Vector2(p[0], p[1])
			n.scale = Vector2.ONE * float(sd.get("scale", 1.0))
			n.offset = Vector2(-r[2] / 2.0, -r[3] if sd.get("anchor", "bc") == "bc" else -r[3] / 2.0)
			var tcol := Color.WHITE
			if sd.get("tint", null) != null:
				tcol = Color(sd.tint)
			tcol.a = float(sd.get("alpha", 1.0))
			n.modulate = tcol
		elif pv != null:
			n.position = Vector2(pv[0], pv[1])
			n.offset = Vector2(r[0] - pv[0], r[1] - pv[1])
		else:
			n.position = Vector2(r[0], r[1])
		add_child(n)
		spr[sd.id] = {"n": n, "d": sd, "base": n.position, "phase": randf() * TAU, "mod": n.modulate}
	# Overlapping hotspots: the smaller (more specific) one sits on top, so a match inside a hatch, a tin on a shelf,
	# a fragment under a plank are never swallowed by the bigger area behind them.  Equal areas: the one defined first wins.
	var hlist: Array = d.get("hotspots", [])
	var order := range(hlist.size())
	order.sort_custom(func(a, b):
		var ra: Array = hlist[a].rect
		var rb: Array = hlist[b].rect
		var aa := float(ra[2]) * float(ra[3])
		var ab := float(rb[2]) * float(rb[3])
		if aa != ab:
			return aa > ab
		return a > b)
	var made := {}
	for i in order:
		var hd: Dictionary = hlist[i]
		var h := Hotspot.new()
		h.hid = hd.id
		var r: Array = hd.rect
		h.position = Vector2(r[0], r[1])
		h.size = Vector2(r[2], r[3])
		h.activated.connect(func(id): hotspot_pressed.emit(id))
		add_child(h)
		made[i] = h
	for i in hlist.size():
		hots.append({"n": made[i], "d": hlist[i]})
	for td in d.get("texts", []):
		var lb := Label.new()
		lb.mouse_filter = Control.MOUSE_FILTER_IGNORE
		lb.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lb.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		lb.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		var r: Array = td.rect
		lb.position = Vector2(r[0], r[1])
		lb.size = Vector2(r[2], r[3])
		lb.pivot_offset = lb.size / 2.0
		lb.rotation_degrees = float(td.get("rot", 0))
		add_child(lb)
		txts.append({"n": lb, "d": td})
	for wd in d.get("widgets", []):
		var path: String = WIDGETS.get(wd.kind, "")
		if path == "" or not ResourceLoader.exists(path):
			push_warning("widget not available: %s" % wd.kind)
			continue
		var w: Widget = load(path).new()
		add_child(w)
		w.setup(self, wd)
		wids.append({"n": w, "d": wd})
	L.language_changed.connect(_retext)
	G.fx.connect(_on_fx)
	refresh()

func _exit_tree() -> void:
	if L.language_changed.is_connected(_retext):
		L.language_changed.disconnect(_retext)
	if G.fx.is_connected(_on_fx):
		G.fx.disconnect(_on_fx)

func _on_fx(name: String, data: Dictionary) -> void:
	if G.test_mode:
		return
	match name:
		"refl_late":
			# the reflection lags half a second behind you
			var n := get_sprite("refl")
			if n:
				var tw := create_tween()
				n.modulate.a = 0.35
				tw.tween_interval(0.5)
				tw.tween_property(n, "modulate:a", 1.0, 0.25)
		"startle":
			# the one startle moment: a hard cut, a flash and a jolt (see settings: Startle moments)
			var fl := ColorRect.new()
			fl.color = Color(1, 1, 1, 0.8)
			fl.size = size
			fl.mouse_filter = Control.MOUSE_FILTER_IGNORE
			add_child(fl)
			var tw := create_tween()
			tw.tween_property(fl, "color:a", 0.0, 0.5)
			tw.tween_callback(fl.queue_free)
			var tw2 := create_tween()
			for i in 6:
				tw2.tween_property(self, "position", Vector2(randf_range(-14, 14), randf_range(-10, 10)), 0.04)
			tw2.tween_property(self, "position", Vector2.ZERO, 0.05)
		"buoy_again":
			for wi in wids:
				if wi.n.has_method("replay"):
					wi.n.replay()
		"slowfade":
			modulate.a = 0.0
			var tw3 := create_tween()
			tw3.tween_property(self, "modulate:a", 1.0, float(data.get("secs", 4.0)))
		"shake":
			var n := get_sprite(str(data.get("sprite", "")))
			if n:
				var tw := create_tween()
				var p0 := n.position
				for i in 5:
					tw.tween_property(n, "position:x", p0.x + (8 if i % 2 == 0 else -8), 0.04)
				tw.tween_property(n, "position", p0, 0.04)

func _retext() -> void:
	refresh()

func get_sprite(id: String) -> Sprite2D:
	return spr[id].n if spr.has(id) else null

func get_hotspot(id: String) -> Hotspot:
	var first: Hotspot = null
	for h in hots:
		if h.d.id == id:
			if h.n.visible:
				return h.n
			if first == null:
				first = h.n
	return first

## The hotspot a click at this scene position would land on (topmost visible), or null.
func hit_test(p: Vector2) -> Hotspot:
	var kids := get_children()
	for i in range(kids.size() - 1, -1, -1):
		var c = kids[i]
		if c is Hotspot and c.visible and Rect2(c.position, c.size).has_point(p):
			return c
	return null

## True if some point of this hotspot's area really lands on it (i.e. nothing visible sits on top of all of it).
func reachable(id: String) -> bool:
	var h := get_hotspot(id)
	if h == null:
		return false
	for fy in [0.5, 0.25, 0.75, 0.1, 0.9]:
		for fx in [0.5, 0.25, 0.75, 0.1, 0.9]:
			var hit := hit_test(h.position + Vector2(h.size.x * fx, h.size.y * fy))
			if hit == h:
				return true
	return false

func refresh() -> void:
	# background variant: first match wins (default variant last)
	var path := ""
	for b in data.get("bg", []):
		if b.get("when", null) == null or G.evb(b.when):
			path = b.tex
			break
	if path != "" and path != _bg_path:
		_bg_path = path
		bg.texture = tex(path)
	for k in spr:
		var e = spr[k]
		var sh = e.d.get("show", null)
		e.n.visible = sh == null or G.evb(sh)
	for h in hots:
		var w = h.d.get("when", null)
		var on: bool = w == null or G.evb(w)
		h.n.visible = on
		h.n.mouse_filter = Control.MOUSE_FILTER_STOP if on else Control.MOUSE_FILTER_IGNORE
		h.n.focus_mode = Control.FOCUS_ALL if on else Control.FOCUS_NONE
	for tx in txts:
		var d: Dictionary = tx.d
		var w = d.get("when", null)
		var lb: Label = tx.n
		lb.visible = w == null or G.evb(w)
		lb.text = d.literal if d.get("literal", null) != null else L.t(d.key)
		var f := Fonts.world() if d.get("font", "world") == "world" else Fonts.ui()
		var sp := int(d.get("spacing", 0))
		lb.add_theme_font_override("font", Fonts.spaced(f, sp) if sp != 0 else f)
		lb.add_theme_font_size_override("font_size", int(d.size))
		lb.add_theme_color_override("font_color", Color(d.color))
	for wi in wids:
		var w = wi.d.get("when", null)
		wi.n.visible = w == null or G.evb(w)
		wi.n.refresh()

func lighting() -> Dictionary:
	var lights: Array = []
	for l in data.get("lights", []):
		if l.get("when", null) == null or G.evb(l.when):
			lights.append(l)
	var amb := Color("#415464")
	if data.get("ambient", null) != null:
		amb = Color(data.ambient)
	return {"dark": clampf(G.evf(data.get("dark", null), 0.0), 0.0, 1.0), "shade": amb, "lights": lights}

func ping_hotspots() -> void:
	for h in hots:
		if h.n.visible:
			h.n.ping(1.6)

func _process(delta: float) -> void:
	t += delta
	var calm: bool = G.settings.reduce_motion
	for k in spr:
		var e = spr[k]
		var fx = e.d.get("fx", null)
		if fx == null or not e.n.visible:
			continue
		var n: Sprite2D = e.n
		match fx:
			"bob":
				n.position.y = e.base.y + (0.0 if calm else sin(t * 1.5 + e.phase) * 7.0)
			"sway":
				n.rotation = 0.0 if calm else sin(t * 1.1 + e.phase) * 0.04
			"flicker":
				n.modulate.a = 1.0 if calm else 0.9 + 0.1 * sin(t * 13.0 + e.phase) * sin(t * 5.3)
			"pulse":
				n.modulate.a = 1.0 if calm else 0.72 + 0.28 * sin(t * 2.1 + e.phase)
			"hand_h":
				n.rotation_degrees = float(G.fi("clock_h")) * 30.0 + float(G.fi("clock_m")) * 0.5
			"hand_m":
				n.rotation_degrees = float(G.fi("clock_m")) * 6.0
			"lowerable":
				var target := 120.0 if G.f("boat_lowered") else 0.0
				if not e.has("cur"):
					e["cur"] = target
				e.cur = target if (G.test_mode or calm) else move_toward(e.cur, target, delta * 90.0)
				n.position.y = e.base.y + e.cur
			"bhand_h":
				n.rotation_degrees = float(G.fi("mclock_h")) * 30.0 + float(G.fi("mclock_m")) * 0.5
			"bhand_m":
				n.rotation_degrees = float(G.fi("mclock_m")) * 6.0
			"mhand_h":
				n.rotation_degrees = -(float(G.fi("mclock_h")) * 30.0 + float(G.fi("mclock_m")) * 0.5)
			"mhand_m":
				n.rotation_degrees = -(float(G.fi("mclock_m")) * 6.0)
