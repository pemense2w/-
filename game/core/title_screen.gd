extends Control
## Title screen: new game, continue, chapter select (after the first finish), album, settings.

signal start_new
signal start_continue
signal start_chapter(n: int)
signal open_settings
signal open_album

var menu: VBoxContainer
var confirm: Control = null

func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_STOP
	var bgc := ColorRect.new()
	bgc.color = Color("#070b0d")
	bgc.size = Vector2(1600, 1200)
	add_child(bgc)
	var v: Dictionary = G.views.get("ui_title", {})
	if not v.is_empty():
		var tr := TextureRect.new()
		tr.texture = ViewNode.tex(v.bg[0].tex)
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_SCALE
		tr.size = Vector2(1600, 1000)
		tr.position = Vector2(0, 80)
		tr.size = Vector2(1600, 1000)
		add_child(tr)
	var shade := ColorRect.new()
	shade.color = Color(0, 0, 0, 0.18)
	shade.size = Vector2(1600, 1200)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(shade)
	var t := UI.label(L.t("game.title"), 124, Color("#f4e2b4"), HORIZONTAL_ALIGNMENT_CENTER, false)
	t.add_theme_font_override("font", Fonts.world())
	t.add_theme_font_size_override("font_size", 128)
	t.add_theme_color_override("font_outline_color", Color(0.03, 0.05, 0.07, 0.85))
	t.add_theme_constant_override("outline_size", 10)
	t.position = Vector2(0, 90)
	t.size = Vector2(1600, 160)
	add_child(t)
	var sub := UI.label(L.t("game.tagline"), 28, Color("#cbbf9f"), HORIZONTAL_ALIGNMENT_CENTER, false)
	sub.add_theme_font_override("font", Fonts.world())
	sub.add_theme_color_override("font_outline_color", Color(0.03, 0.05, 0.07, 0.9))
	sub.add_theme_constant_override("outline_size", 8)
	sub.position = Vector2(200, 250)
	sub.size = Vector2(1200, 40)
	add_child(sub)
	_build_menu()
	# quick language switch (the first screen must be readable)
	var lang := HBoxContainer.new()
	lang.position = Vector2(1100, 30)
	for l in L.LANGS:
		var b := UI.button(L.NAMES[l], 150, 48, 22)
		b.pressed.connect(func(): G.set_setting("lang", l); _rebuild())
		lang.add_child(b)
	add_child(lang)

func _rebuild() -> void:
	for c in get_children():
		c.queue_free()
	await get_tree().process_frame
	_ready()

func _build_menu() -> void:
	menu = VBoxContainer.new()
	menu.position = Vector2(560, 560)
	menu.add_theme_constant_override("separation", 14)
	add_child(menu)
	var first: Button = null
	if G.has_save():
		first = _item("title.continue", func(): start_continue.emit())
	var nb := _item("title.new", func(): _new_game())
	if first == null:
		first = nb
	if G.profile.finished or int(G.profile.unlocked) > 1:
		_item("title.chapters", func(): _chapters())
	_item("title.album", func(): open_album.emit())
	_item("title.settings", func(): open_settings.emit())
	if not OS.has_feature("web"):
		_item("title.quit", func(): get_tree().quit())
	first.call_deferred("grab_focus")

func _item(key: String, cb: Callable) -> Button:
	var b := UI.button(L.t(key), 480, 70, 30)
	b.pressed.connect(cb)
	menu.add_child(b)
	return b

func _new_game() -> void:
	if not G.has_save():
		start_new.emit()
		return
	confirm = UI.panel(760, 260)
	confirm.position = Vector2(420, 380)
	add_child(confirm)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 20)
	confirm.add_child(vb)
	var l := UI.label(L.t("title.confirm_new"), 28, UI.TEXT, HORIZONTAL_ALIGNMENT_CENTER)
	l.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	l.custom_minimum_size = Vector2(700, 0)
	vb.add_child(l)
	var hb := HBoxContainer.new()
	hb.alignment = BoxContainer.ALIGNMENT_CENTER
	hb.add_theme_constant_override("separation", 24)
	vb.add_child(hb)
	var y := UI.button(L.t("ui.yes"), 220, 60)
	y.pressed.connect(func(): start_new.emit())
	hb.add_child(y)
	var n := UI.button(L.t("ui.no"), 220, 60)
	n.pressed.connect(func(): confirm.queue_free(); confirm = null)
	hb.add_child(n)
	n.call_deferred("grab_focus")

func _chapters() -> void:
	var pn := UI.panel(760, 560)
	pn.position = Vector2(420, 300)
	add_child(pn)
	var vb := VBoxContainer.new()
	vb.add_theme_constant_override("separation", 10)
	pn.add_child(vb)
	vb.add_child(UI.label(L.t("title.chapters"), 36, UI.WARM, HORIZONTAL_ALIGNMENT_CENTER))
	for n in range(1, 6):
		var b := UI.button("%d · %s" % [n, L.t("chapter.%d.title" % n)], 700, 60, 26)
		b.disabled = n > int(G.profile.unlocked) and not G.profile.finished
		b.pressed.connect(func(): start_chapter.emit(n))
		vb.add_child(b)
	var close := UI.button(L.t("ui.close"), 220, 56, 24)
	close.pressed.connect(pn.queue_free)
	vb.add_child(close)
