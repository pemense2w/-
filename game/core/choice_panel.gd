class_name ChoicePanel
extends Control
## A quiet choice: a few lines of text, a few buttons.

signal chosen(key: String)

func setup(options: Array) -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(UI.dim_bg(0.7))
	var pn := UI.panel(900, 140 + 90 * options.size())
	pn.position = Vector2(350, 300)
	add_child(pn)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 16)
	pn.add_child(vb)
	vb.add_child(UI.label(L.t("choice.title"), 34, UI.WARM, HORIZONTAL_ALIGNMENT_CENTER))
	var first: Button = null
	for o in options:
		var b := UI.button(L.t(o.label), 820, 70, 28)
		b.pressed.connect(func(): chosen.emit(o.key); queue_free())
		vb.add_child(b)
		if first == null:
			first = b
	first.call_deferred("grab_focus")
