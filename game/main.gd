extends Control
## The one screen: scene (1600x1000) with the caption line, satchel and buttons underneath.
## Interface stays out of the picture: two turn arrows, a back arrow, the satchel, the notebook and Pell.

const W := 1600
const H := 1200
const SH := 1000

var scene_area: Control
var view: ViewNode = null
var mul: ColorRect
var addl: ColorRect
var vig: ColorRect
var grain: ColorRect
var fade: ColorRect
var caption: Label
var sfx_label: Label
var hover_label: Label
var slots: Array = []
var arrow_l: Widget.Arrow
var arrow_r: Widget.Arrow
var arrow_b: Widget.Arrow
var btn_nb: Button
var btn_pell: Button
var btn_menu: Button
var time_btn: Control
var held_icon: TextureRect
var overlay: Control
var modal: Control = null
var title: Control = null
var _dark := 0.0
var _cap_t := 0.0
var _sfx_t := 0.0
var _swapping := false
var _light_cache := {}
var _touch_start := Vector2.ZERO
var _slot_flash := {}
var _nb_pulse := 0.0
var _gt := 0.0

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	_build_ui()
	G.view_changed.connect(_on_view_changed)
	G.changed.connect(_on_changed)
	G.said.connect(_on_said)
	G.sfx_caption.connect(_on_sfx_caption)
	G.item_gained.connect(_on_item_gained)
	G.note_added.connect(_on_note_added)
	G.memory_requested.connect(_on_memory)
	G.ending_requested.connect(_on_ending)
	G.chapter_card.connect(_on_chapter_card)
	G.fx.connect(_on_fx)
	G.choice_requested.connect(_on_choice)
	G.request_title.connect(show_title)
	G.settings_changed.connect(_apply_settings)
	L.language_changed.connect(_relabel)
	_apply_settings()
	_relabel()
	if not G.test_mode:
		show_title()

# ------------------------------------------------------------------ layout
func _build_ui() -> void:
	var bgc := ColorRect.new()
	bgc.color = Color("#0a0f11")
	bgc.size = Vector2(W, H)
	bgc.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(bgc)
	scene_area = Control.new()
	scene_area.size = Vector2(W, SH)
	scene_area.clip_contents = true
	scene_area.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(scene_area)
	# lighting: darkness with pools of light, warm additive glow, vignette, grain
	mul = _fx_rect("res://game/fx/light_mul.gdshader")
	addl = _fx_rect("res://game/fx/light_add.gdshader")
	vig = _fx_rect("res://game/fx/vignette.gdshader")
	grain = _fx_rect("res://game/fx/grain.gdshader")
	fade = ColorRect.new()
	fade.color = Color(0, 0, 0, 0)
	fade.size = Vector2(W, SH)
	fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	scene_area.add_child(fade)
	# navigation arrows (turn left / right, step back from a close-up)
	arrow_l = _arrow(Vector2.LEFT, Vector2(18, 440), func(): G.turn(-1))
	arrow_r = _arrow(Vector2.RIGHT, Vector2(W - 114, 440), func(): G.turn(1))
	arrow_b = _arrow(Vector2.DOWN, Vector2(W / 2.0 - 48, SH - 118), func(): G.back())
	# bottom panel
	var pnl := ColorRect.new()
	pnl.color = Color("#10181b")
	pnl.position = Vector2(0, SH)
	pnl.size = Vector2(W, H - SH)
	pnl.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(pnl)
	var edge := ColorRect.new()
	edge.color = Color(UI.EDGE, 0.55)
	edge.position = Vector2(0, SH)
	edge.size = Vector2(W, 3)
	edge.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(edge)
	caption = UI.label("", 30, UI.TEXT, HORIZONTAL_ALIGNMENT_CENTER)
	caption.position = Vector2(60, SH + 6)
	caption.size = Vector2(W - 120, 88)
	caption.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	caption.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	add_child(caption)
	sfx_label = UI.label("", 22, UI.DIM, HORIZONTAL_ALIGNMENT_LEFT)
	sfx_label.position = Vector2(868, SH + 150)
	sfx_label.size = Vector2(300, 36)
	sfx_label.clip_text = true
	add_child(sfx_label)
	hover_label = UI.label("", 22, UI.WARM, HORIZONTAL_ALIGNMENT_LEFT)
	hover_label.position = Vector2(868, SH + 108)
	hover_label.size = Vector2(300, 36)
	hover_label.clip_text = true
	add_child(hover_label)
	for i in G.SATCHEL_SLOTS:
		var b := Button.new()
		b.position = Vector2(40 + i * 102, SH + 104)
		b.size = Vector2(94, 90)
		b.custom_minimum_size = b.size
		b.expand_icon = true
		b.icon_alignment = HORIZONTAL_ALIGNMENT_CENTER
		b.add_theme_constant_override("icon_max_width", 80)
		b.focus_mode = Control.FOCUS_ALL
		b.gui_input.connect(_slot_input.bind(i))
		b.mouse_entered.connect(_slot_hover.bind(i, true))
		b.mouse_exited.connect(_slot_hover.bind(i, false))
		add_child(b)
		slots.append(b)
	btn_nb = _bar_button(Vector2(1180, SH + 110), 122, func(): open_notebook())
	btn_pell = _bar_button(Vector2(1312, SH + 110), 122, func(): ask_pell())
	btn_menu = _bar_button(Vector2(1444, SH + 110), 116, func(): open_pause())
	time_btn = TimeButton.new()
	time_btn.position = Vector2(24, 24)
	time_btn.size = Vector2(96, 96)
	time_btn.visible = false
	time_btn.pressed.connect(func(): if not G.busy: G.chapter.toggle_era())
	add_child(time_btn)
	held_icon = TextureRect.new()
	held_icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	held_icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	held_icon.size = Vector2(76, 76)
	held_icon.mouse_filter = Control.MOUSE_FILTER_IGNORE
	held_icon.visible = false
	add_child(held_icon)
	overlay = Control.new()
	overlay.size = Vector2(W, H)
	overlay.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(overlay)

func _fx_rect(shader_path: String) -> ColorRect:
	var c := ColorRect.new()
	c.size = Vector2(W, SH)
	c.mouse_filter = Control.MOUSE_FILTER_IGNORE
	var m := ShaderMaterial.new()
	m.shader = load(shader_path)
	c.material = m
	scene_area.add_child(c)
	return c

func _arrow(dir: Vector2, pos: Vector2, cb: Callable) -> Widget.Arrow:
	var a := Widget.Arrow.new()
	a.dir = dir
	a.position = pos
	a.size = Vector2(96, 96)
	a.pressed.connect(cb)
	scene_area.add_child(a)
	return a

func _bar_button(pos: Vector2, w: int, cb: Callable) -> Button:
	var b := UI.button("", w, 78, 22)
	b.position = pos
	b.pressed.connect(cb)
	add_child(b)
	return b

func _relabel() -> void:
	btn_nb.text = L.t("ui.notebook")
	btn_pell.text = L.t("ui.ask_pell")
	btn_menu.text = L.t("ui.menu")
	for b in [btn_nb, btn_pell, btn_menu]:
		b.add_theme_font_override("font", Fonts.ui())
		b.add_theme_font_size_override("font_size", mini(UI.fs(22), 26))
	caption.add_theme_font_override("font", Fonts.ui())
	caption.add_theme_font_size_override("font_size", UI.fs(30))
	_on_changed()

func _apply_settings() -> void:
	caption.add_theme_font_size_override("font_size", UI.fs(30))
	caption.add_theme_font_override("font", Fonts.ui())
	btn_nb.visible = not G.settings.purist
	grain.visible = true

# -------------------------------------------------------------- view logic
func _on_view_changed(id: String) -> void:
	if G.test_mode or G.settings.reduce_motion or view == null:
		_swap(id)
		return
	if _swapping:
		return
	_swapping = true
	var tw := create_tween()
	tw.tween_property(fade, "color:a", 1.0, 0.14)
	tw.tween_callback(func(): _swap(id))
	tw.tween_property(fade, "color:a", 0.0, 0.2)
	tw.tween_callback(func(): _swapping = false)

func _swap(id: String) -> void:
	if view:
		view.queue_free()
		view = null
	var d: Dictionary = G.views.get(id, {})
	if d.is_empty():
		return
	view = ViewNode.new()
	scene_area.add_child(view)
	scene_area.move_child(view, 0)
	view.setup(d)
	view.hotspot_pressed.connect(func(h): G.activate(h))
	_on_changed()
	if G.test_mode:
		_dark = view.lighting().dark

func _on_changed() -> void:
	if view != null and is_instance_valid(view):
		view.refresh()
		_light_cache = view.lighting()
		var nav: Dictionary = view.data.get("nav", {})
		arrow_l.visible = nav.get("left", null) != null
		arrow_r.visible = nav.get("right", null) != null
		arrow_b.visible = nav.get("back", null) != null
	_update_satchel()
	time_btn.visible = G.in_game and not G.s.is_empty() and G.f("watch_ok") and int(G.s.chapter) == 4
	time_btn.queue_redraw()
	btn_nb.visible = not G.settings.purist
	btn_nb.text = L.t("ui.notebook") + ("  •" if _nb_pulse > 0.0 else "")

func _update_satchel() -> void:
	if G.s.is_empty():
		for b in slots:
			b.icon = null
			b.visible = false
		return
	for i in slots.size():
		var b: Button = slots[i]
		b.visible = true
		var item: String = G.s.items[i] if i < G.s.items.size() else ""
		var sel := item != "" and item == G.held
		var edge := UI.WARM if sel else Color(UI.EDGE, 0.35)
		b.add_theme_stylebox_override("normal", UI.box(Color("#1c262a") if item != "" else Color("#141b1e"), edge, 3 if sel else 2, 12))
		b.add_theme_stylebox_override("hover", UI.box(Color("#2a3a40"), UI.WARM, 3, 12))
		b.add_theme_stylebox_override("pressed", UI.box(Color("#3a4a50"), UI.WARM, 3, 12))
		b.add_theme_stylebox_override("focus", UI.box(Color("#2a3a40"), UI.WARM, 3, 12))
		if item == "":
			b.icon = null
			b.tooltip_text = ""
			b.disabled = false
			continue
		var meta: Dictionary = G.items_meta.get(item, {})
		b.icon = ViewNode.tex(meta.get("tex", "")) if meta.has("tex") else null
		b.text = "" if b.icon != null else G.item_name(item).substr(0, 6)
		b.tooltip_text = G.item_name(item)
	if G.held != "":
		var m: Dictionary = G.items_meta.get(G.held, {})
		held_icon.texture = ViewNode.tex(m.get("tex", "")) if m.has("tex") else null
	held_icon.visible = G.held != "" and held_icon.texture != null

func _slot_input(e: InputEvent, i: int) -> void:
	if i >= G.s.items.size():
		return
	var item: String = G.s.items[i]
	if e is InputEventKey and e.pressed and not e.echo and (e.keycode == KEY_ENTER or e.keycode == KEY_SPACE):
		_slot_click(i)
		get_viewport().set_input_as_handled()
		return
	if not (e is InputEventMouseButton and e.pressed):
		return
	if e.button_index == MOUSE_BUTTON_RIGHT or (e.button_index == MOUSE_BUTTON_LEFT and e.double_click):
		if not G.busy:
			G.inspect_item(item)
			open_inspect(item)
	elif e.button_index == MOUSE_BUTTON_LEFT:
		_slot_click(i)
	get_viewport().set_input_as_handled()

func _slot_hover(i: int, on: bool) -> void:
	if not on or i >= G.s.items.size():
		hover_label.text = ""
		return
	hover_label.text = "%s  ·  %s" % [G.item_name(G.s.items[i]), L.t("ui.examine_hint")]

func _slot_click(i: int) -> void:
	if i < G.s.items.size():
		G.click_item(G.s.items[i])

func _on_said(text: String) -> void:
	caption.text = text
	caption.modulate.a = 1.0
	_cap_t = 9.0

func _on_sfx_caption(text: String) -> void:
	if not G.settings.captions:
		return
	sfx_label.text = "[%s]" % text
	sfx_label.modulate.a = 1.0
	_sfx_t = 2.4

func _on_item_gained(item: String) -> void:
	var i: int = G.s.items.find(item)
	if i >= 0:
		_slot_flash[i] = 1.0

func _on_note_added(_id: String) -> void:
	_nb_pulse = 6.0
	G.say("notebook.updated")

func _process(delta: float) -> void:
	_gt += delta
	if _cap_t > 0.0:
		_cap_t -= delta
		if _cap_t < 1.5:
			caption.modulate.a = maxf(0.0, _cap_t / 1.5)
	if _sfx_t > 0.0:
		_sfx_t -= delta
		sfx_label.modulate.a = clampf(_sfx_t / 0.8, 0.0, 1.0)
	if _nb_pulse > 0.0:
		_nb_pulse -= delta
		var pulse := 0.5 + 0.5 * sin(_gt * 7.0)
		btn_nb.add_theme_color_override("font_color", UI.TEXT.lerp(UI.WARM, pulse))
		if _nb_pulse <= 0.0:
			btn_nb.add_theme_color_override("font_color", UI.TEXT)
			_on_changed()
	for k in _slot_flash.keys():
		_slot_flash[k] -= delta * 1.6
		if _slot_flash[k] <= 0.0:
			_slot_flash.erase(k)
			slots[k].modulate = Color.WHITE
		else:
			slots[k].modulate = Color.WHITE.lerp(Color(1.6, 1.4, 0.9), _slot_flash[k])
	if held_icon.visible:
		held_icon.position = get_local_mouse_position() + Vector2(18, 12)
	_update_lighting(delta)

func _update_lighting(delta: float) -> void:
	if _light_cache.is_empty():
		return
	var target: float = _light_cache.dark
	_dark = target if (G.test_mode or G.settings.reduce_motion) else lerpf(_dark, target, 1.0 - exp(-delta * 3.0))
	var lights: Array = _light_cache.lights.duplicate()
	if G.held != "" and G.items_meta.get(G.held, {}).has("light"):
		var mp := scene_area.get_local_mouse_position()
		if Rect2(Vector2.ZERO, scene_area.size).has_point(mp):
			lights.append({"x": mp.x, "y": mp.y, "r": 360.0, "color": G.items_meta[G.held].light, "intensity": 0.9, "flicker": 0.08, "hole": 1.0})
	var lm := PackedVector4Array()
	var la := PackedVector4Array()
	var lc := PackedVector4Array()
	for i in 8:
		if i < lights.size():
			var l: Dictionary = lights[i]
			var col := Color(l.color)
			lm.append(Vector4(l.x, l.y, l.r, float(l.get("hole", 1.0))))
			la.append(Vector4(l.x, l.y, l.r, float(l.get("intensity", 1.0))))
			lc.append(Vector4(col.r, col.g, col.b, 0.0 if G.settings.reduce_motion else float(l.get("flicker", 0.0))))
		else:
			lm.append(Vector4(0, 0, 1, 0))
			la.append(Vector4(0, 0, 1, 0))
			lc.append(Vector4(0, 0, 0, 0))
	var n := mini(lights.size(), 8)
	var mm: ShaderMaterial = mul.material
	mm.set_shader_parameter("dark", _dark)
	mm.set_shader_parameter("shade_color", _light_cache.shade)
	mm.set_shader_parameter("n_lights", n)
	mm.set_shader_parameter("lights", lm)
	var am: ShaderMaterial = addl.material
	am.set_shader_parameter("n_lights", n)
	am.set_shader_parameter("lights", la)
	am.set_shader_parameter("colors", lc)
	am.set_shader_parameter("t", 0.0 if G.settings.reduce_motion else _gt)
	var gm: ShaderMaterial = grain.material
	gm.set_shader_parameter("t", 0.0 if G.settings.reduce_motion else _gt)

# ------------------------------------------------------------------- input
func _unhandled_key_input(e: InputEvent) -> void:
	if not (e is InputEventKey and e.pressed and not e.echo):
		return
	if modal != null or G.busy or not G.in_game:
		return
	match e.keycode:
		KEY_LEFT:
			G.turn(-1)
		KEY_RIGHT:
			G.turn(1)
		KEY_DOWN:
			G.back()
		KEY_ESCAPE:
			if G.held != "":
				G.select_item(G.held)
			elif view and view.data.get("nav", {}).get("back", null) != null:
				G.back()
			else:
				open_pause()
		KEY_N:
			open_notebook()
		KEY_H:
			ask_pell()
		KEY_E:
			if G.held != "":
				open_inspect(G.held)
		KEY_T:
			if time_btn.visible:
				G.chapter.toggle_era()
		KEY_F:
			if view:
				view.ping_hotspots()
		KEY_1, KEY_2, KEY_3, KEY_4, KEY_5, KEY_6, KEY_7, KEY_8:
			_slot_click(e.keycode - KEY_1)
		_:
			return
	get_viewport().set_input_as_handled()

func _input(e: InputEvent) -> void:
	# swipe: left / right turns, down steps back (touch)
	if e is InputEventScreenTouch:
		if e.pressed:
			_touch_start = e.position
		elif modal == null and G.in_game and not G.busy:
			var d: Vector2 = e.position - _touch_start
			if absf(d.x) > 160 and absf(d.y) < 110:
				G.turn(1 if d.x < 0 else -1)
			elif d.y > 170 and absf(d.x) < 110:
				G.back()
	elif e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_RIGHT and modal == null and G.held != "":
		G.select_item(G.held)   # right click puts the item away

# ---------------------------------------------------------------- overlays
func _open_modal(n: Control) -> void:
	if modal != null:
		return
	modal = n
	overlay.add_child(n)
	Snd.play("ui_open")
	n.tree_exited.connect(func(): modal = null; Snd.play("ui_close"))

func open_notebook() -> void:
	if G.settings.purist or modal != null or not G.in_game:
		return
	_nb_pulse = 0.0
	btn_nb.add_theme_color_override("font_color", UI.TEXT)
	var p := NotebookPanel.new()
	_open_modal(p)

func open_inspect(item: String) -> void:
	if modal != null:
		return
	var p := InspectPanel.new()
	_open_modal(p)
	p.setup(item)

func open_settings() -> void:
	var p := SettingsPanel.new()
	_close_modal()
	_open_modal(p)

func open_album() -> void:
	if not ResourceLoader.exists("res://game/core/album_panel.gd"):
		return
	var p: Control = load("res://game/core/album_panel.gd").new()
	_close_modal()
	_open_modal(p)

func open_pause() -> void:
	if modal != null or not G.in_game:
		return
	var p := PausePanel.new()
	p.open_settings.connect(open_settings)
	p.open_notebook.connect(func(): _close_modal(); open_notebook())
	p.open_album.connect(open_album)
	p.quit_title.connect(func(): _close_modal(); G.quit_to_title())
	_open_modal(p)

func _close_modal() -> void:
	if modal != null:
		modal.queue_free()
		modal = null

func ask_pell() -> void:
	if modal != null or not G.in_game or G.busy:
		return
	var h := G.request_hint()
	var p := HintPanel.new()
	_open_modal(p)
	p.setup(h)

func show_title() -> void:
	_close_modal()
	if title != null and is_instance_valid(title):
		title.queue_free()
	var t = load("res://game/core/title_screen.gd").new()
	title = t
	overlay.add_child(t)
	modal = t
	t.tree_exited.connect(func(): modal = null)
	t.start_new.connect(func(): _begin(func(): G.new_game()))
	t.start_continue.connect(func(): _begin(func(): G.continue_game()))
	t.start_chapter.connect(func(n): _begin(func(): G.select_chapter(n)))
	t.open_settings.connect(func(): var p := SettingsPanel.new(); overlay.add_child(p); p.closed.connect(func(): pass))
	t.open_album.connect(func(): if ResourceLoader.exists("res://game/core/album_panel.gd"): overlay.add_child(load("res://game/core/album_panel.gd").new()))
	Snd.ambience("title")
	Snd.music("still_water")

func _begin(fn: Callable) -> void:
	if title != null and is_instance_valid(title):
		title.queue_free()
		title = null
	modal = null
	fn.call()

func _on_choice(options: Array) -> void:
	var p := ChoicePanel.new()
	overlay.add_child(p)
	p.setup(options)
	p.chosen.connect(func(k): G.choice_made.emit(k))

func _on_fx(name: String, _data: Dictionary) -> void:
	if name == "era_flip" and not G.test_mode:
		var fl := ColorRect.new()
		fl.color = Color(1, 0.96, 0.85, 0.9) if G.era() == "then" else Color(0.75, 0.85, 0.95, 0.9)
		fl.size = Vector2(W, SH)
		fl.mouse_filter = Control.MOUSE_FILTER_IGNORE
		scene_area.add_child(fl)
		var tw := create_tween()
		tw.tween_property(fl, "color:a", 0.0, 0.55)
		tw.tween_callback(fl.queue_free)

func _on_chapter_card(n: int) -> void:
	if G.test_mode:
		return
	var card := ColorRect.new()
	card.color = Color(0.02, 0.03, 0.035, 1.0)
	card.size = Vector2(W, H)
	card.mouse_filter = Control.MOUSE_FILTER_STOP
	var l1 := UI.label(L.t("chapter.n", [n]), 30, UI.DIM, HORIZONTAL_ALIGNMENT_CENTER)
	l1.size = Vector2(W, 50)
	l1.position = Vector2(0, 440)
	var l2 := UI.label(L.t("chapter.%d.title" % n), 72, UI.WARM, HORIZONTAL_ALIGNMENT_CENTER)
	l2.add_theme_font_override("font", Fonts.world())
	l2.size = Vector2(W, 100)
	l2.position = Vector2(0, 490)
	card.add_child(l1)
	card.add_child(l2)
	overlay.add_child(card)
	G.busy = true
	card.modulate.a = 0.0
	var tw := create_tween()
	tw.tween_property(card, "modulate:a", 1.0, 0.5)
	tw.tween_interval(1.6)
	tw.tween_property(card, "modulate:a", 0.0, 0.7)
	tw.tween_callback(func(): card.queue_free(); G.busy = false)

func _on_memory(n: int) -> void:
	if G.test_mode:
		G.memory_done.emit()
		return
	var p := StagePlayer.new()
	overlay.add_child(p)
	p.play(n)
	p.finished.connect(func():
		p.queue_free()
		Snd.stop_music()
		Snd.ambience(Snd.current_amb, true)
		G.memory_done.emit())

func _on_ending(kind: String) -> void:
	if G.test_mode:
		return
	G.busy = true
	var p := StagePlayer.new()
	overlay.add_child(p)
	p.play(kind)
	p.finished.connect(func():
		p.queue_free()
		G.busy = false
		Snd.stop_music()
		var es = load("res://game/core/end_screen.gd").new()
		overlay.add_child(es)
		es.setup(kind)
		es.back_to_title.connect(func(): es.queue_free(); G.quit_to_title())
		es.start_over.connect(func(): es.queue_free(); G.new_game())
		es.open_album.connect(func(): open_album()))

# --------------------------------------------------------------- test hooks
func click_hotspot(id: String) -> bool:
	## Press a hotspot exactly as a click would - fails if the art has no such visible hotspot.
	if view == null:
		return false
	var h := view.get_hotspot(id)
	if h == null or not h.visible:
		return false
	G.activate(id)
	return true

func widget(id: String) -> Widget:
	if view == null:
		return null
	for w in view.wids:
		if w.d.id == id:
			return w.n
	return null


class TimeButton extends Control:
	signal pressed
	var hover := false
	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		focus_mode = Control.FOCUS_ALL
		mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		mouse_entered.connect(func(): hover = true; queue_redraw())
		mouse_exited.connect(func(): hover = false; queue_redraw())
		tooltip_text = "Then / Now  (T)"
	func _gui_input(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT:
			pressed.emit()
			accept_event()
		elif e is InputEventKey and e.pressed and not e.echo and (e.keycode == KEY_ENTER or e.keycode == KEY_SPACE):
			pressed.emit()
			accept_event()
	func _draw() -> void:
		var c := size / 2.0
		var then := G.era() == "then"
		draw_circle(c, 46, Color("#c9a24d") if not hover else Color("#f0cf7a"))
		draw_circle(c, 38, Color("#f3e3b8") if then else Color("#b9c8cc"))
		for i in 12:
			var a := TAU * i / 12.0
			draw_line(c + Vector2(sin(a), -cos(a)) * 31, c + Vector2(sin(a), -cos(a)) * 36, Color("#3a2a18"), 2.0)
		draw_line(c, c + Vector2(sin(deg_to_rad(130)), -cos(deg_to_rad(130))) * 20, Color("#2a1a0c"), 4.0)
		draw_line(c, c + Vector2(sin(deg_to_rad(120)), -cos(deg_to_rad(120))) * 30, Color("#2a1a0c"), 3.0)
		draw_circle(c + Vector2(0, -52), 7, Color("#c9a24d"))
		if has_focus():
			draw_arc(c, 50, 0, TAU, 32, Color.WHITE, 3.0)

class HintPanel extends Control:
	var again: Button
	var txt: Label
	func setup(h: Dictionary) -> void:
		set_anchors_preset(Control.PRESET_FULL_RECT)
		add_child(UI.dim_bg(0.55))
		var pn := UI.panel(1180, 330)
		pn.position = Vector2(210, 420)
		add_child(pn)
		var hb := HBoxContainer.new()
		hb.add_theme_constant_override("separation", 26)
		pn.add_child(hb)
		var tr := TextureRect.new()
		var icon_path := "ui/ui_icons__pell_big.webp"
		tr.texture = ViewNode.tex(icon_path)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.custom_minimum_size = Vector2(190, 190)
		hb.add_child(tr)
		var col := VBoxContainer.new()
		col.add_theme_constant_override("separation", 12)
		hb.add_child(col)
		var who: String = "hint.speaker.r" if h.get("speaker", "pell") == "r" else "hint.speaker.pell"
		col.add_child(UI.label("%s · %s" % [L.t(who), L.t("hint.tier.%d" % int(h.get("tier", 0)))], 26, UI.WARM))
		txt = UI.label(h.get("text", ""), 28, UI.TEXT)
		txt.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		txt.custom_minimum_size = Vector2(880, 0)
		col.add_child(txt)
		var row := HBoxContainer.new()
		row.add_theme_constant_override("separation", 18)
		col.add_child(row)
		again = UI.button(L.t("hint.again"), 300, 56, 24)
		again.pressed.connect(func(): setup_refresh())
		row.add_child(again)
		var close := UI.button(L.t("ui.close"), 220, 56, 24)
		close.pressed.connect(queue_free)
		row.add_child(close)
		close.call_deferred("grab_focus")
	func setup_refresh() -> void:
		var h := G.request_hint()
		txt.text = h.text
	func _unhandled_key_input(e: InputEvent) -> void:
		if e is InputEventKey and e.pressed and (e.keycode == KEY_ESCAPE or e.keycode == KEY_H):
			get_viewport().set_input_as_handled()
			queue_free()
