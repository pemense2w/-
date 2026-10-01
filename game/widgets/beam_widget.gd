extends Widget
## The lens: a 3x3 grid of prism panels (mirrors) around the flame.  Click a panel to turn it a quarter; make the beam
## leave through the seaward window at the east edge of the top row.

const INIT := [1, 0, 1, 1, 1, 1, 0, 1, 1]      # 0 = '/', 1 = '\'
var cell := 240.0
var origin := Vector2.ZERO
var path: Array = []
var exit_cell := Vector2i(-9, -9)

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	cell = float(args.cell)
	origin = Vector2(args.origin[0], args.origin[1]) - position
	if not G.s.flags.has("lens_cfg"):
		G.s.flags["lens_cfg"] = INIT.duplicate()
	set_process(true)

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	accept_event()
	if G.f(args.flag):
		return
	var col := int((e.position.x - origin.x) / cell)
	var row := int((e.position.y - origin.y) / cell)
	if col < 0 or col > 2 or row < 0 or row > 2:
		return
	turn(row * 3 + col)

func turn(i: int) -> void:
	var cfg: Array = G.s.flags["lens_cfg"]
	cfg[i] = 1 - int(cfg[i])
	G.s.flags["lens_cfg"] = cfg
	Snd.play("prism")
	_trace()
	if exit_cell == Vector2i(0, 3):
		G.setf(args.flag)
		event("solved", {})
	else:
		G.changed.emit()

## follows the beam: enters row 1 from the west heading east; returns the cells visited
func _trace() -> void:
	var cfg: Array = G.s.flags["lens_cfg"]
	var r := 1
	var c := 0
	var d := Vector2i(0, 1)
	path = []
	var seen := {}
	while r >= 0 and r < 3 and c >= 0 and c < 3:
		var key := "%d,%d,%d,%d" % [r, c, d.x, d.y]
		if seen.has(key):
			exit_cell = Vector2i(-9, -9)
			return
		seen[key] = true
		path.append(Vector2i(r, c))
		if int(cfg[r * 3 + c]) == 0:
			d = Vector2i(-d.y, -d.x)      # '/'
		else:
			d = Vector2i(d.y, d.x)        # '\'
		r += d.x
		c += d.y
	exit_cell = Vector2i(r, c)

func refresh() -> void:
	_trace()
	queue_redraw()

func _process(_dt: float) -> void:
	if is_visible_in_tree():
		queue_redraw()

func _draw() -> void:
	var cfg: Array = G.s.flags.get("lens_cfg", INIT)
	var lit: bool = G.f(args.flag)
	# the beam
	var pts := PackedVector2Array()
	pts.append(origin + Vector2(-60, cell * 1.5))
	for p in path:
		pts.append(origin + Vector2((p.y + 0.5) * cell, (p.x + 0.5) * cell))
	if exit_cell.x != -9:
		var last: Vector2i = path[path.size() - 1]
		var out := origin + Vector2((exit_cell.y + 0.5) * cell, (exit_cell.x + 0.5) * cell)
		pts.append(out)
	draw_polyline(pts, Color(1.0, 0.85, 0.45, 0.22), 26.0)
	draw_polyline(pts, Color(1.0, 0.93, 0.62, 0.95 if lit else 0.7), 7.0)
	# the prism panels
	for i in 9:
		var cc := origin + Vector2((i % 3 + 0.5) * cell, (i / 3 + 0.5) * cell)
		var a := Vector2(-1, 1) if int(cfg[i]) == 0 else Vector2(-1, -1)
		var h := cell * 0.34
		draw_line(cc - a * h, cc + a * h, Color("#6c8d96", 0.95), 18.0)
		draw_line(cc - a * h, cc + a * h, Color("#c9e4ea", 0.9), 8.0)
