class_name StagePlayer
extends Control
## Plays a short scripted scene: paper-cut puppets and pictures on a lit screen, with captions and sound.
## Used for the five shadow-play memories and the three ending sequences.  Any click, key or the Skip button ends it.

signal finished

const W := 1600
const H := 1200
const SH := 1000

var events: Array = []
var idx := 0
var t := 0.0
var done := false
var stage: Control
var bg: TextureRect
var bg2: TextureRect
var layer: Control
var caption: Label
var title_lbl: Label
var skip: Button
var tint_rect: ColorRect
var puppets := {}
var _pending: Array = []
var _time_scale := 1.0

## sc: a memory number (1-5), an ending key ("A", "B", "C") or a ready-made script array
func play(sc, bg_view: String = "mem_wall") -> void:
	var music := ""
	if typeof(sc) == TYPE_INT:
		music = "memory"
		sc = StageScripts.memory(int(sc))
	elif typeof(sc) == TYPE_STRING:
		bg_view = StageScripts.ending_bg(str(sc))
		music = "ending_" + str(sc)
		sc = StageScripts.ending(str(sc))
	events = sc
	events.sort_custom(func(a, b): return float(a.t) < float(b.t))
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var black := ColorRect.new()
	black.color = Color.BLACK
	black.size = Vector2(W, H)
	add_child(black)
	stage = Control.new()
	stage.size = Vector2(W, SH)
	stage.clip_contents = true
	add_child(stage)
	bg = TextureRect.new()
	bg.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg.stretch_mode = TextureRect.STRETCH_SCALE
	bg.size = Vector2(W, SH)
	stage.add_child(bg)
	bg2 = TextureRect.new()
	bg2.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	bg2.stretch_mode = TextureRect.STRETCH_SCALE
	bg2.size = Vector2(W, SH)
	bg2.modulate.a = 0.0
	stage.add_child(bg2)
	_set_bg(bg, bg_view)
	layer = Control.new()
	layer.size = Vector2(W, SH)
	stage.add_child(layer)
	tint_rect = ColorRect.new()
	tint_rect.color = Color(1, 1, 1, 0)
	tint_rect.size = Vector2(W, SH)
	tint_rect.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(tint_rect)
	var vig := ColorRect.new()
	vig.size = Vector2(W, SH)
	var m := ShaderMaterial.new()
	m.shader = load("res://game/fx/vignette.gdshader")
	vig.material = m
	vig.mouse_filter = Control.MOUSE_FILTER_IGNORE
	stage.add_child(vig)
	caption = UI.label("", 34, Color("#f3e6c4"), HORIZONTAL_ALIGNMENT_CENTER)
	caption.position = Vector2(120, SH + 20)
	caption.size = Vector2(W - 240, 150)
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.add_theme_font_override("font", Fonts.world())
	add_child(caption)
	title_lbl = UI.label("", 96, Color("#f4e2b4"), HORIZONTAL_ALIGNMENT_CENTER, false)
	title_lbl.add_theme_font_override("font", Fonts.world())
	title_lbl.add_theme_font_size_override("font_size", 110)
	title_lbl.position = Vector2(0, 400)
	title_lbl.size = Vector2(W, 160)
	title_lbl.modulate.a = 0.0
	add_child(title_lbl)
	skip = UI.button(L.t("ui.skip"), 180, 54, 24)
	skip.position = Vector2(W - 220, SH + 130)
	skip.pressed.connect(_finish)
	add_child(skip)
	set_process(true)
	if music != "":
		Snd.music(music)
	modulate.a = 0.0
	create_tween().tween_property(self, "modulate:a", 1.0, 0.6)

func _set_bg(rect: TextureRect, view: String) -> void:
	var v: Dictionary = G.views.get(view, {})
	if v.is_empty() or v.bg.is_empty():
		rect.texture = null
		return
	rect.texture = ViewNode.tex(v.bg[v.bg.size() - 1].tex)

func _process(delta: float) -> void:
	if done:
		return
	t += delta
	while idx < events.size() and float(events[idx].t) <= t:
		_run(events[idx])
		idx += 1
		if done:
			return
	if bg.material:
		(bg.material as ShaderMaterial).set_shader_parameter("t", t)
	for k in puppets:
		var p = puppets[k]
		if p.bob != null:
			var b: Dictionary = p.bob
			var off: float = sin((t - b.t0) * b.speed + b.ph) * b.amp
			var cur: Vector2 = p.n.position
			p.n.position = Vector2(cur.x, p.base_y + off)
	

func _input(e: InputEvent) -> void:
	if done:
		return
	if e is InputEventKey and e.pressed and not e.echo and (e.keycode == KEY_ESCAPE or e.keycode == KEY_SPACE or e.keycode == KEY_ENTER):
		get_viewport().set_input_as_handled()
		_finish()

func _finish() -> void:
	if done:
		return
	done = true
	var tw := create_tween()
	tw.tween_property(self, "modulate:a", 0.0, 0.4)
	tw.tween_callback(func(): finished.emit())

func _tex_for(d: Dictionary) -> Array:
	## returns [texture, size, anchor-offset]
	if d.has("img"):
		var tx := ViewNode.tex(str(d.img))
		return [tx, tx.get_size() if tx else Vector2(64, 64), true]
	var sheet := str(d.get("sheet", "mem_puppets"))
	var v: Dictionary = G.views.get(sheet, {})
	for s in v.get("sprites", []):
		if s.id == d.spr:
			var tx := ViewNode.tex(s.tex)
			return [tx, Vector2(s.rect[2], s.rect[3]), false]
	return [null, Vector2.ZERO, false]

func _run(e: Dictionary) -> void:
	var a: String = e.a
	match a:
		"put":
			var info := _tex_for(e)
			if info[0] == null:
				push_warning("stage: unknown sprite %s" % str(e))
				return
			var n := Sprite2D.new()
			n.centered = false
			n.texture = info[0]
			var sz: Vector2 = info[1]
			var s := float(e.get("s", 1.0))
			n.scale = Vector2(s * (-1.0 if e.get("flip", false) else 1.0), s)
			n.offset = Vector2(-sz.x / 2.0, -sz.y)
			n.position = Vector2(float(e.x), float(e.y))
			n.modulate = Color(1, 1, 1, float(e.get("alpha", 1.0)))
			layer.add_child(n)
			puppets[e.id] = {"n": n, "bob": null, "base_y": n.position.y}
			if e.has("bob"):
				var b: Dictionary = e.bob
				puppets[e.id].bob = {"amp": float(b.amp), "speed": float(b.speed), "ph": float(b.get("ph", 0.0)), "t0": t}
				set_process(true)
		"move":
			var p = puppets.get(e.id)
			if p:
				var tw := create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_IN_OUT)
				tw.tween_property(p.n, "position", Vector2(float(e.x), float(e.y)), float(e.get("dur", 1.0)))
				p.base_y = float(e.y)
		"scale":
			var p = puppets.get(e.id)
			if p:
				var sg: float = signf(p.n.scale.x)
				create_tween().tween_property(p.n, "scale", Vector2(float(e.s) * sg, float(e.s)), float(e.get("dur", 1.0)))
		"rot":
			var p = puppets.get(e.id)
			if p:
				create_tween().tween_property(p.n, "rotation_degrees", float(e.deg), float(e.get("dur", 1.0)))
		"sway":
			var p = puppets.get(e.id)
			if p:
				var tw := create_tween().set_loops(int(e.get("loops", 8)))
				var amp := float(e.deg)
				var d := float(e.get("dur", 1.5))
				tw.tween_property(p.n, "rotation_degrees", amp, d).set_trans(Tween.TRANS_SINE)
				tw.tween_property(p.n, "rotation_degrees", -amp, d).set_trans(Tween.TRANS_SINE)
		"fade":
			var p = puppets.get(e.id)
			if p:
				create_tween().tween_property(p.n, "modulate:a", float(e.alpha), float(e.get("dur", 1.0)))
		"nobob":
			var p = puppets.get(e.id)
			if p:
				p.bob = null
		"flip":
			var p = puppets.get(e.id)
			if p:
				p.n.scale.x = -p.n.scale.x
		"del":
			var p = puppets.get(e.id)
			if p:
				p.n.queue_free()
				puppets.erase(e.id)
		"tint":
			var tw2 := create_tween()
			tw2.tween_property(tint_rect, "color", Color(e.color), float(e.get("dur", 1.0)))
		"flash":
			var fl := ColorRect.new()
			fl.color = Color(1, 0.98, 0.9, 0.9)
			fl.size = Vector2(W, SH)
			fl.mouse_filter = Control.MOUSE_FILTER_IGNORE
			stage.add_child(fl)
			var tw3 := create_tween()
			tw3.tween_property(fl, "color:a", 0.0, float(e.get("dur", 0.4)))
			tw3.tween_callback(fl.queue_free)
		"shake":
			var tw4 := create_tween()
			for i in 6:
				tw4.tween_property(layer, "position", Vector2(randf_range(-10, 10), randf_range(-8, 8)), 0.04)
			tw4.tween_property(layer, "position", Vector2.ZERO, 0.05)
		"cap":
			caption.text = L.t(str(e.key))
			caption.modulate.a = 0.0
			var tw5 := create_tween()
			tw5.tween_property(caption, "modulate:a", 1.0, 0.5)
			tw5.tween_interval(float(e.get("dur", 4.0)) - 1.0)
			tw5.tween_property(caption, "modulate:a", 0.0, 0.5)
		"title":
			title_lbl.text = L.t(str(e.key))
			var tw6 := create_tween()
			tw6.tween_property(title_lbl, "modulate:a", 1.0, 1.2)
			tw6.tween_interval(float(e.get("dur", 4.0)))
			tw6.tween_property(title_lbl, "modulate:a", 0.0, 1.0)
		"bg":
			_set_bg(bg2, str(e.view))
			bg2.modulate.a = 0.0
			var tw7 := create_tween()
			tw7.tween_property(bg2, "modulate:a", 1.0, float(e.get("dur", 1.5)))
			tw7.tween_callback(func():
				bg.texture = bg2.texture
				bg2.modulate.a = 0.0)
		"ripple":
			if bg.material == null:
				var m := ShaderMaterial.new()
				m.shader = load("res://game/fx/ripple.gdshader")
				bg.material = m
			var mm: ShaderMaterial = bg.material
			create_tween().tween_method(func(v): mm.set_shader_parameter("amp", v), 0.0, float(e.amp), float(e.get("dur", 3.0)))
		"snd":
			Snd.play(str(e.name))
		"music":
			Snd.music(str(e.name))
		"photo":
			_photo(e)
		"photo_clear":
			for k in puppets.keys():
				if str(k).begins_with("photo"):
					var pn: Sprite2D = puppets[k].n
					create_tween().tween_property(pn, "modulate:a", 0.0, 1.5)
		"end":
			_finish()

func _photo(e: Dictionary) -> void:
	var v: Dictionary = G.views.get("album_photo", {})
	if v.is_empty():
		return
	var tx := ViewNode.tex(v.bg[v.bg.size() - 1].tex)
	var sz := tx.get_size()
	var cell := Vector2(sz.x / 5.0, sz.y / 2.0)
	var sc := 1.25
	var origin := Vector2((W - sz.x * sc) / 2.0, 190.0)
	var dur := float(e.get("dur", 6.0))
	for i in 10:
		var at := AtlasTexture.new()
		at.atlas = tx
		at.region = Rect2(Vector2(i % 5, i / 5) * cell, cell)
		var n := Sprite2D.new()
		n.centered = false
		n.texture = at
		n.scale = Vector2(sc, sc)
		n.position = Vector2(randf_range(-300, W + 100), randf_range(-400, -100) if i % 2 == 0 else randf_range(SH + 50, SH + 300))
		n.rotation_degrees = randf_range(-70, 70)
		n.modulate.a = 0.0
		layer.add_child(n)
		puppets["photo%d" % i] = {"n": n, "bob": null, "base_y": 0.0}
		var tw := create_tween().set_parallel(true)
		var target := origin + Vector2(i % 5, i / 5) * cell * sc
		var delay := 0.25 * i
		tw.tween_property(n, "modulate:a", 1.0, 0.3).set_delay(delay)
		tw.tween_property(n, "position", target, dur * 0.6).set_delay(delay).set_trans(Tween.TRANS_QUINT).set_ease(Tween.EASE_OUT)
		tw.tween_property(n, "rotation_degrees", 0.0, dur * 0.6).set_delay(delay).set_trans(Tween.TRANS_QUINT).set_ease(Tween.EASE_OUT)
