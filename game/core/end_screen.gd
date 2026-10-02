extends Control
## After an ending: how long it took, how many hints were used, what has been found.

signal back_to_title
signal start_over
signal open_album

func setup(kind: String) -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bgc := ColorRect.new()
	bgc.color = Color("#070b0d")
	bgc.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(bgc)
	var vb := VBoxContainer.new()
	vb.position = Vector2(400, 150)
	vb.size = Vector2(800, 900)
	vb.add_theme_constant_override("separation", 18)
	add_child(vb)
	var t := UI.label(L.t("end.%s.title" % kind), 84, Color("#f4e2b4"), HORIZONTAL_ALIGNMENT_CENTER, false)
	t.add_theme_font_override("font", Fonts.world())
	t.add_theme_font_size_override("font_size", 96)
	vb.add_child(t)
	var sub := UI.label(L.t("end.%s.sub" % kind), 28, UI.DIM, HORIZONTAL_ALIGNMENT_CENTER)
	sub.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	vb.add_child(sub)
	vb.add_child(HSeparator.new())
	var secs := int(float(G.s.stats.play_time)) if not G.s.is_empty() else 0
	var lines := [
		L.t("end.time", ["%d:%02d" % [secs / 3600 * 60 + (secs % 3600) / 60, secs % 60]]),
		L.t("end.hints", [int(G.s.stats.hints) if not G.s.is_empty() else 0]),
		L.t("end.fragments", [G.fragment_count()]),
		L.t("end.endings", [G.profile.endings.size()]),
	]
	for l in lines:
		vb.add_child(UI.label(l, 32, UI.TEXT, HORIZONTAL_ALIGNMENT_CENTER))
	vb.add_child(HSeparator.new())
	var first: Button = null
	if kind == "B":
		first = UI.button(L.t("end.begin_again"), 600, 70, 28)
		first.pressed.connect(func(): start_over.emit())
		vb.add_child(first)
	var ab := UI.button(L.t("title.album"), 600, 70, 28)
	ab.pressed.connect(func(): open_album.emit())
	vb.add_child(ab)
	var tb := UI.button(L.t("pause.title_screen"), 600, 70, 28)
	tb.pressed.connect(func(): back_to_title.emit())
	vb.add_child(tb)
	if first == null:
		first = tb
	first.call_deferred("grab_focus")
