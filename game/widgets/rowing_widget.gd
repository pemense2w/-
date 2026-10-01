extends Widget
## The chart as a rowing control: a 5x5 grid, one cell per stroke.  Fog hides everything but what you have seen.
## Tap a visited landmark to row straight back to it ("one tap"); the arrows at the edges row one cell.

const LM_COLORS := {"red": Color("#b8453a"), "green": Color("#4f8a5b"), "pale": Color("#d9d3b6"), "yellow": Color("#dcb33c")}
var origin := Vector2(420, 150)
var cell := 140.0
var arrows := {}

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	origin = Vector2(args.origin[0], args.origin[1]) - position
	cell = float(args.cell)
	var c := origin + Vector2(cell * 2.5, cell * 2.5)
	var span := cell * 2.5 + 64.0
	for d in ["n", "e", "s", "w"]:
		var a := Widget.Arrow.new()
		a.size = Vector2(76, 76)
		var off := Vector2.ZERO
		match d:
			"n":
				off = Vector2(0, -span)
				a.dir = Vector2.UP
			"e":
				off = Vector2(span, 0)
				a.dir = Vector2.RIGHT
			"s":
				off = Vector2(0, span)
				a.dir = Vector2.DOWN
			"w":
				off = Vector2(-span, 0)
				a.dir = Vector2.LEFT
		a.position = c + off - a.size / 2.0
		a.pressed.connect(func(): G.chapter.move(d))
		add_child(a)
		arrows[d] = a
	set_process(true)

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	var p: Vector2 = (e.position - origin) / cell
	if p.x < 0 or p.y < 0 or p.x >= 5 or p.y >= 5:
		return
	accept_event()
	G.chapter.teleport(int(p.x), int(p.y))

func refresh() -> void:
	queue_redraw()

func _process(_d: float) -> void:
	if is_visible_in_tree():
		queue_redraw()

func _draw() -> void:
	var seen: Array = G.s.flags.get("c3_seen", [])
	var px := G.fi("c3_x")
	var py := G.fi("c3_y")
	var ok: bool = G.f("compass_ok")
	var font := Fonts.world()
	for y in 5:
		for x in 5:
			var r := Rect2(origin + Vector2(x, y) * cell, Vector2(cell, cell))
			var known: bool = (y * 5 + x) in seen
			var col := Color(0.30, 0.50, 0.58, 0.45) if known else Color(0.40, 0.45, 0.42, 0.28)
			draw_rect(r, col, true)
			draw_rect(r, Color("#5b4a35"), false, 2.0)
			if known:
				_icon(G.chapter.landmark_at(x, y), r.get_center(), true)
	# the circled spot is on the chart from the start
	var cc := origin + Vector2(3.5, 1.5) * cell
	draw_arc(cc, cell * 0.38, 0, TAU, 28, Color("#a33a30"), 4.0)
	# the cottage, due south, off the chart
	draw_rect(Rect2(origin + Vector2(2.2, 5.2) * cell, Vector2(cell * 0.6, cell * 0.12)), Color("#f3cf84", 0.9), true)
	# the boat
	var bc := origin + Vector2(px + 0.5, py + 0.5) * cell
	draw_colored_polygon(PackedVector2Array([bc + Vector2(0, -30), bc + Vector2(20, 22), bc + Vector2(-20, 22)]), Color("#8a5a36"))
	draw_circle(bc + Vector2(0, -34), 6, Color("#f3cf84"))
	# headings appear once the compass is set
	var labels := {"n": Vector2(0, -1), "e": Vector2(1, 0), "s": Vector2(0, 1), "w": Vector2(-1, 0)}
	for d in labels:
		var a: Widget.Arrow = arrows[d]
		a.modulate = Color(1, 1, 1, 1.0 if ok else 0.45)
		if ok:
			var t: String = {"n": "N", "e": "E", "s": "S", "w": "W"}[d]
			draw_string(font, a.position + Vector2(26, -6) + (Vector2(0, 0)), t, HORIZONTAL_ALIGNMENT_LEFT, -1, 34, Color("#2b2118"))

func _icon(name: String, c: Vector2, known: bool) -> void:
	if name == "":
		return
	if LM_COLORS.has(name):
		draw_circle(c, 22, LM_COLORS[name])
		draw_circle(c, 22, Color(0, 0, 0, 0.35), false, 2.0)
	elif name == "tree":
		draw_line(c + Vector2(0, 26), c + Vector2(0, -20), Color("#2b241f"), 7.0)
		draw_line(c + Vector2(0, -6), c + Vector2(-22, -26), Color("#2b241f"), 5.0)
		draw_line(c + Vector2(0, -6), c + Vector2(22, -26), Color("#2b241f"), 5.0)
	elif name == "buoy":
		draw_colored_polygon(PackedVector2Array([c + Vector2(-18, 24), c + Vector2(-10, -2), c + Vector2(10, -2), c + Vector2(18, 24)]), Color("#b8453a"))
		draw_circle(c + Vector2(0, -14), 10, Color("#c9a24d"))
	elif name == "reeds":
		for k in range(-2, 3):
			draw_line(c + Vector2(k * 9, 24), c + Vector2(k * 9 + 3, -22), Color("#4a6a40"), 4.0)
	elif name == "landing":
		draw_colored_polygon(PackedVector2Array([c + Vector2(-16, 26), c + Vector2(-10, -22), c + Vector2(10, -22), c + Vector2(16, 26)]), Color("#d9d3b6"))
		draw_rect(Rect2(c + Vector2(-8, -34), Vector2(16, 12)), Color("#2b2018"), true)
