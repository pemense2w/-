extends Widget
## Throw the mooring line over the landing post.  A relaxed aim: the target window widens after each miss.

var marker := 0.0
var dir := 1.0
var throwing := 0.0
var t := 0.0

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	set_process(true)

func _window() -> float:
	return minf(520.0, 150.0 + 70.0 * G.fi("moor_miss"))

func _process(delta: float) -> void:
	if not is_visible_in_tree() or G.f(args.flag):
		return
	t += delta
	var speed := 380.0 if not G.settings.reduce_motion else 200.0
	marker += dir * speed * delta
	if marker > size.x - 40.0:
		dir = -1.0
	elif marker < 40.0:
		dir = 1.0
	throwing = maxf(0.0, throwing - delta * 2.5)
	queue_redraw()

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	accept_event()
	if G.f(args.flag) or G.busy:
		return
	if not G.f("got_lhkey"):
		G.say("c3.moor_pell")
		return
	throwing = 1.0
	Snd.play("throw")
	var target_x: float = float(args.target[0]) - position.x
	var ok := absf(marker - target_x) <= _window() / 2.0 or bool(G.settings.no_timing)
	if ok:
		G.setf(args.flag)
		event("moored", {})
	else:
		G.inc("moor_miss")
		G.say("c3.moor_miss")

func _draw() -> void:
	if G.f(args.flag):
		return
	var target_x: float = float(args.target[0]) - position.x
	var w := _window()
	draw_rect(Rect2(target_x - w / 2.0, size.y - 120.0, w, 12.0), Color(1, 0.93, 0.7, 0.25), true)
	draw_circle(Vector2(marker, size.y - 114.0), 14, Color(1, 0.9, 0.6, 0.9))
	draw_line(Vector2(marker, size.y - 140.0), Vector2(marker, size.y - 90.0), Color(1, 0.9, 0.6, 0.9), 3.0)
