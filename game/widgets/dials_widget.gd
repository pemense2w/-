extends Widget
## A row of symbol dials (shape lock, tide lock ...).  Click the upper half of a column to advance, the lower half to go back.

var cells: Array = []
var symbols: Array = []
var faces: Array = []
var prefix := ""

func _build() -> void:
	cells = args.cells
	symbols = args.symbols
	prefix = "dial_" + str(args.flag) + "_"
	mouse_filter = Control.MOUSE_FILTER_STOP
	var init: Array = args.get("init", [])
	for i in cells.size():
		if not G.s.flags.has(prefix + str(i)):
			G.s.flags[prefix + str(i)] = int(init[i]) if i < init.size() else (i * 2 + 3) % symbols.size()
		var c: Array = cells[i]
		if args.get("digits", false):
			var lb := Label.new()
			lb.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
			lb.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
			lb.position = Vector2(c[0], c[1]) - position
			lb.size = Vector2(c[2], c[3])
			lb.add_theme_font_override("font", Fonts.world())
			lb.add_theme_font_size_override("font_size", 120)
			lb.add_theme_color_override("font_color", Color("#efe5c6"))
			lb.mouse_filter = Control.MOUSE_FILTER_IGNORE
			add_child(lb)
			faces.append(lb)
			continue
		var tr := TextureRect.new()
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
		tr.position = Vector2(c[0] + 14, c[1] + 14) - position
		tr.size = Vector2(c[2] - 28, c[3] - 28)
		tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(tr)
		faces.append(tr)

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	var p: Vector2 = e.position + position
	for i in cells.size():
		var c: Array = cells[i]
		if p.x >= c[0] - 30 and p.x <= c[0] + c[2] + 30:
			var cy: float = c[1] + c[3] / 2.0
			_step(i, 1 if p.y < cy else -1)
			accept_event()
			return

func _step(i: int, d: int) -> void:
	if G.f(args.flag):
		G.say("dials.locked")
		return
	var k: String = prefix + str(i)
	G.setf(k, posmod(G.fi(k) + d, symbols.size()))
	Snd.play("dial")
	event("changed", {"values": values()})
	_check()

func values() -> Array:
	var out := []
	for i in cells.size():
		out.append(symbols[G.fi(prefix + str(i))])
	return out

func _check() -> void:
	if values() == args.solution:
		G.setf(args.flag)
		Snd.play("unlock")
		event("solved", {})

func refresh() -> void:
	for i in faces.size():
		var nm: String = symbols[G.fi(prefix + str(i))]
		if args.get("digits", false):
			faces[i].text = nm
		else:
			faces[i].texture = ViewNode.tex(_glyph_path(nm))

func _glyph_path(nm: String) -> String:
	var v = G.views.get("ui_glyphs", {})
	for s in v.get("sprites", []):
		if s.id == "glyph_" + nm:
			return s.tex
	return ""
