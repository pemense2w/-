class_name InspectPanel
extends Control
## Look closely at an item: its picture and, for papers, what is written on it.

signal closed

func setup(item: String) -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(UI.dim_bg(0.8))
	var pn := UI.panel(1000, 780)
	pn.position = Vector2(300, 150)
	add_child(pn)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 14)
	pn.add_child(vb)
	vb.add_child(UI.label(G.item_name(item), 38, UI.WARM))
	var key := "item.%s.text" % item
	var has_text := L.has_key(key)
	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 28)
	vb.add_child(hb)
	var meta: Dictionary = G.items_meta.get(item, {})
	var art_path: String = meta.get("inspect", meta.get("tex", ""))
	if art_path != "":
		var tr := TextureRect.new()
		tr.texture = ViewNode.tex(art_path)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.custom_minimum_size = Vector2(300, 300) if has_text else Vector2(420, 420)
		hb.add_child(tr)
	var col := VBoxContainer.new()
	col.custom_minimum_size = Vector2(560, 0)
	hb.add_child(col)
	var desc := UI.label(L.t("item.%s.desc" % item), 26, UI.TEXT)
	desc.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	desc.custom_minimum_size = Vector2(560, 0)
	col.add_child(desc)
	if has_text:
		var sep := HSeparator.new()
		col.add_child(sep)
		var tx := UI.label(L.t(key), 30, Color("#e8d9a8"))
		tx.add_theme_font_override("font", Fonts.world())
		tx.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		tx.custom_minimum_size = Vector2(560, 0)
		col.add_child(tx)
	var close := UI.button(L.t("ui.close"), 220, 60)
	close.pressed.connect(func(): closed.emit(); queue_free())
	vb.add_child(close)
	close.call_deferred("grab_focus")

func _unhandled_key_input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and e.keycode == KEY_ESCAPE:
		get_viewport().set_input_as_handled()
		closed.emit()
		queue_free()
