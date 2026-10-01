class_name NotebookPanel
extends Control
## The keeper's notebook: sketches clues once seen. It records facts, never answers.

signal closed

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(UI.dim_bg(0.78))
	var pn := UI.panel(1240, 960)
	pn.position = Vector2(180, 90)
	add_child(pn)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 12)
	pn.add_child(vb)
	vb.add_child(UI.label(L.t("notebook.title"), 40, UI.WARM))
	var sc := ScrollContainer.new()
	sc.custom_minimum_size = Vector2(1180, 790)
	sc.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	vb.add_child(sc)
	var list := VBoxContainer.new()
	list.add_theme_constant_override("separation", 18)
	list.custom_minimum_size = Vector2(1150, 0)
	sc.add_child(list)
	var shown := 0
	for d in G.notebook_defs:
		if d.id in G.s.notes:
			shown += 1
			list.add_child(_entry(d))
	if shown == 0:
		var e := UI.label(L.t("notebook.empty"), 28, UI.DIM)
		e.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		e.custom_minimum_size = Vector2(1100, 0)
		list.add_child(e)
	var close := UI.button(L.t("ui.close"), 220, 60)
	close.pressed.connect(close_panel)
	vb.add_child(close)
	close.call_deferred("grab_focus")

func _entry(d: Dictionary) -> Control:
	var row := HBoxContainer.new()
	row.add_theme_constant_override("separation", 24)
	var sk := Sketch.new()
	sk.kind = d.sketch
	sk.custom_minimum_size = Vector2(300, 170)
	row.add_child(sk)
	var col := VBoxContainer.new()
	col.custom_minimum_size = Vector2(820, 0)
	var t := UI.label(L.t(d.title), 30, UI.WARM)
	col.add_child(t)
	var tk: String = d.text
	if d.get("alt", null) != null and G.evb(d.alt.when):
		tk = d.alt.key
	var body := UI.label(L.t(tk), 26, UI.TEXT)
	body.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	body.custom_minimum_size = Vector2(820, 0)
	col.add_child(body)
	row.add_child(col)
	return row

func close_panel() -> void:
	closed.emit()
	queue_free()

func _unhandled_key_input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and (e.keycode == KEY_ESCAPE or e.keycode == KEY_N):
		get_viewport().set_input_as_handled()
		close_panel()
