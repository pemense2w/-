extends Widget
## A silver shadow passes under the gap; lower the net as it passes.  Wide timing window that widens after each miss;
## the "No timing" setting makes the first try succeed.

var fish_x := 0.0
var dir := 1.0
var decoys: Array = []
var net_y := -1.0
var lowering := false
var t := 0.0

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	fish_x = 40.0
	for i in 2:
		decoys.append({"x": 200.0 + i * 500.0, "d": 1.0 if i == 0 else -1.0, "y": 140.0 + i * 180.0, "sp": 90.0 + i * 40.0})
	set_process(true)

func _window() -> float:
	return minf(1000.0, 190.0 + 90.0 * G.fi("catch_miss"))

func _process(delta: float) -> void:
	if not is_visible_in_tree():
		return
	var speed := 150.0 if not G.settings.reduce_motion else 80.0
	fish_x += dir * speed * delta
	if fish_x > size.x - 80.0:
		dir = -1.0
	elif fish_x < 80.0:
		dir = 1.0
	for d in decoys:
		d.x += d.d * d.sp * delta
		if d.x > size.x - 60.0 or d.x < 60.0:
			d.d *= -1.0
	t += delta
	if lowering:
		net_y += delta * 900.0
		if net_y > size.y * 0.62:
			lowering = false
			_resolve()
	elif net_y > -1.0:
		net_y = maxf(-1.0, net_y - delta * 700.0)
	queue_redraw()

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	accept_event()
	if lowering or G.busy:
		return
	if not G.has("net"):
		G.say("c2.catch_nonet")
		return
	if G.has("small_fish"):
		G.say("c2.catch_have")
		return
	net_y = 0.0
	lowering = true
	Snd.play("splash")

func _resolve() -> void:
	var half := _window() / 2.0
	var ok := absf(fish_x - size.x / 2.0) <= half or bool(G.settings.no_timing)
	if ok:
		if G.give("small_fish"):
			G.setf("got_fish_once")
			G.s.flags["catch_miss"] = 0
			event("caught", {})
	else:
		G.inc("catch_miss")
		G.say("c2.catch_miss")

func _draw() -> void:
	# the lit patch of water under the gap
	var w := _window()
	draw_rect(Rect2(size.x / 2.0 - w / 2.0, 0, w, size.y), Color(0.7, 0.85, 0.9, 0.07), true)
	for d in decoys:
		_fish(Vector2(d.x, d.y), 0.55, Color(0.05, 0.1, 0.13, 0.5), d.d)
	var fp := Vector2(fish_x, size.y * 0.52 + sin(t * 2.0) * 14.0)
	_fish(fp, 1.0, Color(0.78, 0.88, 0.92, 0.5), dir)
	if net_y >= 0.0:
		var c := Vector2(size.x / 2.0, net_y)
		draw_line(Vector2(c.x, 0), c, Color("#b79c68"), 6.0)
		draw_arc(c + Vector2(0, 40), 120, 0, PI, 20, Color("#b79c68"), 8.0)
		for k in range(-3, 4):
			draw_line(c + Vector2(k * 34, 40), c + Vector2(k * 22, 140), Color("#b79c68", 0.8), 3.0)

func _fish(p: Vector2, s: float, col: Color, d: float) -> void:
	var pts := PackedVector2Array()
	for i in 20:
		var a := TAU * i / 20.0
		pts.append(p + Vector2(cos(a) * 70.0 * s * d, sin(a) * 30.0 * s))
	draw_colored_polygon(pts, col)
	var tx := -d * 70.0 * s
	draw_colored_polygon(PackedVector2Array([p + Vector2(tx, 0), p + Vector2(tx - d * 40.0 * s, -26.0 * s), p + Vector2(tx - d * 40.0 * s, 26.0 * s)]), col)
