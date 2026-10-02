extends Control
## The album: the five memories (replayable) and the photograph of Ruth and Tomas, which the ten fragments assemble.

signal closed

var photo_box: Control
var count_label: Label

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(UI.dim_bg(0.88))
	var pn := UI.panel(1420, 1020)
	pn.position = Vector2(90, 70)
	add_child(pn)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 12)
	pn.add_child(vb)
	vb.add_child(UI.label(L.t("album.title"), 40, UI.WARM))
	var hb := HBoxContainer.new()
	hb.add_theme_constant_override("separation", 40)
	vb.add_child(hb)
	# memories
	var left := VBoxContainer.new()
	left.custom_minimum_size = Vector2(520, 0)
	left.add_theme_constant_override("separation", 10)
	hb.add_child(left)
	left.add_child(UI.label(L.t("album.memories"), 30, UI.TEXT))
	for n in range(1, 6):
		var have: bool = n in G.profile.memories
		var b := UI.button("%d · %s" % [n, L.t("mem.%d.title" % n) if have else "???"], 500, 62, 26)
		b.disabled = not have
		b.pressed.connect(func(): _replay(n))
		left.add_child(b)
	left.add_child(UI.label(L.t("album.endings"), 30, UI.TEXT))
	for k in ["A", "B", "C"]:
		var have2: bool = k in G.profile.endings
		var l := UI.label("%s · %s" % [k, L.t("end.%s.title" % k) if have2 else ("???" if k != "C" else L.t("album.ending_c_hint"))], 26, UI.TEXT if have2 else UI.DIM)
		l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		l.custom_minimum_size = Vector2(500, 0)
		left.add_child(l)
	# photograph
	var right := VBoxContainer.new()
	hb.add_child(right)
	right.add_child(UI.label(L.t("album.photo"), 30, UI.TEXT))
	photo_box = Control.new()
	photo_box.custom_minimum_size = Vector2(800, 520)
	right.add_child(photo_box)
	count_label = UI.label(L.t("album.fragments", [G.fragment_count()]), 28, UI.WARM)
	right.add_child(count_label)
	_build_photo()
	var close := UI.button(L.t("ui.close"), 240, 60)
	close.pressed.connect(func(): closed.emit(); queue_free())
	vb.add_child(close)
	close.call_deferred("grab_focus")

func _build_photo() -> void:
	var v: Dictionary = G.views.get("album_photo", {})
	var back := ColorRect.new()
	back.color = Color("#1a1612")
	back.size = Vector2(800, 520)
	photo_box.add_child(back)
	if v.is_empty():
		return
	var tx := ViewNode.tex(v.bg[v.bg.size() - 1].tex)
	var cell := Vector2(tx.get_size().x / 5.0, tx.get_size().y / 2.0)
	var sc := 780.0 / tx.get_size().x
	for i in 10:
		var n := TextureRect.new()
		var at := AtlasTexture.new()
		at.atlas = tx
		at.region = Rect2(Vector2(i % 5, i / 5) * cell, cell)
		n.texture = at
		n.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		n.stretch_mode = TextureRect.STRETCH_SCALE
		n.size = cell * sc
		n.position = Vector2(10, 10) + Vector2(i % 5, i / 5) * cell * sc
		var have: bool = (i + 1) in G.profile.frags
		n.modulate = Color.WHITE if have else Color(0.05, 0.05, 0.06, 1.0)
		photo_box.add_child(n)
		if not have:
			var q := UI.label(str(i + 1), 26, UI.DIM, HORIZONTAL_ALIGNMENT_CENTER)
			q.position = n.position + n.size / 2.0 - Vector2(40, 18)
			q.size = Vector2(80, 36)
			photo_box.add_child(q)

func _replay(n: int) -> void:
	var p := StagePlayer.new()
	add_child(p)
	p.play(n)
	p.finished.connect(func():
		p.queue_free()
		Snd.stop_music())

func _unhandled_key_input(e: InputEvent) -> void:
	if e is InputEventKey and e.pressed and e.keycode == KEY_ESCAPE:
		get_viewport().set_input_as_handled()
		closed.emit()
		queue_free()
