extends Widget
## Three brass valves, each set 0-9 (upper half of a wheel: +1, lower half: -1).  One valve is seized in Now until it has been oiled.

var cells: Array = []
var labels: Array = []

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	cells = args.cells
	for i in cells.size():
		if not G.s.flags.has("valve_%d" % i):
			G.s.flags["valve_%d" % i] = [7, 5, 2][i]
		var c: Array = cells[i]
		var lb := Label.new()
		lb.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		lb.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
		lb.position = Vector2(c[0], c[1]) - position
		lb.size = Vector2(c[2], c[3])
		lb.add_theme_font_override("font", Fonts.world())
		lb.add_theme_font_size_override("font_size", 120)
		lb.add_theme_color_override("font_color", Color("#efe5c6"))
		lb.add_theme_color_override("font_outline_color", Color("#1a120c"))
		lb.add_theme_constant_override("outline_size", 10)
		lb.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(lb)
		labels.append(lb)

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	accept_event()
	if G.held != "":
		G.activate("valve_board")
		return
	var p: Vector2 = e.position + position
	for i in cells.size():
		var c: Array = cells[i]
		if p.x >= c[0] - 40 and p.x <= c[0] + c[2] + 40:
			_step(i, 1 if p.y < c[1] + c[3] / 2.0 else -1)
			return

func is_seized(i: int) -> bool:
	return i == int(args.seized) and G.era() == "now" and not G.f("valve_oiled")

func _step(i: int, d: int) -> void:
	if G.f(args.flag):
		G.say("c4.valves_locked")
		return
	if is_seized(i):
		Snd.play("seized")
		G.say("c4.valve_seized")
		return
	var k := "valve_%d" % i
	G.setf(k, posmod(G.fi(k) + d, 10))
	Snd.play("valve")
	event("changed", {})
	var right := true
	for j in cells.size():
		if G.fi("valve_%d" % j) != int(args.solution[j]):
			right = false
	if right and G.f("valve_oiled"):
		G.setf(args.flag)
		event("solved", {})
	elif right:
		G.say("c4.valves_right_dry")

func refresh() -> void:
	for i in labels.size():
		labels[i].text = str(G.fi("valve_%d" % i))
		labels[i].modulate = Color(0.75, 0.55, 0.45) if is_seized(i) else Color.WHITE
