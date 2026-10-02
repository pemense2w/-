class_name SettingsPanel
extends Control
## Accessibility and audio settings. Everything here is saved immediately.

signal closed

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(UI.dim_bg(0.85))
	var pn := UI.panel(1100, 980)
	pn.position = Vector2(250, 90)
	add_child(pn)
	var outer := VBoxContainer.new()
	outer.add_theme_constant_override("separation", 10)
	pn.add_child(outer)
	outer.add_child(UI.label(L.t("settings.title"), 40, UI.WARM))
	var sc := ScrollContainer.new()
	sc.size_flags_vertical = Control.SIZE_EXPAND_FILL
	sc.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	outer.add_child(sc)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 10)
	vb.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	sc.add_child(vb)
	# language
	var lr := HBoxContainer.new()
	lr.add_child(_lbl(L.t("settings.language"), 400))
	for l in L.LANGS:
		var b := UI.button(L.NAMES[l], 200, 54, 24)
		b.pressed.connect(func(): G.set_setting("lang", l); _rebuild())
		lr.add_child(b)
	vb.add_child(lr)
	vb.add_child(_slider("settings.amb", "vol_amb", 0.0, 1.0, 0.05))
	vb.add_child(_slider("settings.sfx", "vol_sfx", 0.0, 1.0, 0.05))
	vb.add_child(_slider("settings.music", "vol_music", 0.0, 1.0, 0.05))
	vb.add_child(_slider("settings.text_size", "text_scale", 1.0, 1.5, 0.1))
	for pair in [["settings.plain_font", "plain_font"], ["settings.hotspot_glow", "hotspot_glow"], ["settings.reduce_motion", "reduce_motion"], ["settings.startle", "startle"],
			["settings.no_timing", "no_timing"], ["settings.purist", "purist"], ["settings.captions", "captions"], ["settings.telemetry", "telemetry"]]:
		vb.add_child(_check(pair[0], pair[1]))
	var close := UI.button(L.t("ui.close"), 240, 60)
	close.pressed.connect(func(): closed.emit(); queue_free())
	outer.add_child(close)
	close.call_deferred("grab_focus")

func _rebuild() -> void:
	# re-open to apply language / text size to this panel itself
	for c in get_children():
		c.queue_free()
	await get_tree().process_frame
	_ready()

func _lbl(text: String, w: int) -> Label:
	var l := UI.label(text, 26, UI.TEXT)
	l.custom_minimum_size = Vector2(w, 0)
	return l

func _slider(key: String, setting: String, mn: float, mx: float, step: float) -> Control:
	var r := HBoxContainer.new()
	r.add_child(_lbl(L.t(key), 400))
	var s := HSlider.new()
	s.min_value = mn
	s.max_value = mx
	s.step = step
	s.value = float(G.settings[setting])
	s.custom_minimum_size = Vector2(420, 40)
	s.value_changed.connect(func(v): G.set_setting(setting, v))
	if setting == "text_scale":
		s.drag_ended.connect(func(_c): _rebuild())
	r.add_child(s)
	return r

func _check(key: String, setting: String) -> Control:
	var r := HBoxContainer.new()
	var c := CheckButton.new()
	c.text = L.t(key)
	c.button_pressed = bool(G.settings[setting])
	c.add_theme_font_override("font", Fonts.ui())
	c.add_theme_font_size_override("font_size", UI.fs(26))
	c.add_theme_color_override("font_color", UI.TEXT)
	c.custom_minimum_size = Vector2(900, 46)
	c.toggled.connect(func(v): G.set_setting(setting, v); if setting == "plain_font": _rebuild())
	r.add_child(c)
	return r

func _unhandled_key_input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and e.keycode == KEY_ESCAPE:
		get_viewport().set_input_as_handled()
		closed.emit()
		queue_free()
