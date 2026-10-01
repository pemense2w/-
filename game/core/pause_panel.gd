class_name PausePanel
extends Control

signal resume
signal open_settings
signal open_notebook
signal open_album
signal quit_title

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(UI.dim_bg(0.82))
	var pn := UI.panel(520, 560)
	pn.position = Vector2(540, 250)
	add_child(pn)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 14)
	pn.add_child(vb)
	vb.add_child(UI.label(L.t("pause.title"), 40, UI.WARM, HORIZONTAL_ALIGNMENT_CENTER))
	var items := [
		["pause.resume", func(): resume.emit(); queue_free()],
		["pause.notebook", func(): open_notebook.emit()],
		["pause.album", func(): open_album.emit()],
		["pause.settings", func(): open_settings.emit()],
		["pause.title_screen", func(): quit_title.emit()],
	]
	var first: Button = null
	for it in items:
		var b := UI.button(L.t(it[0]), 480, 68)
		b.pressed.connect(it[1])
		vb.add_child(b)
		if first == null:
			first = b
	first.call_deferred("grab_focus")

func _unhandled_key_input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and e.keycode == KEY_ESCAPE:
		get_viewport().set_input_as_handled()
		resume.emit()
		queue_free()
