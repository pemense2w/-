extends Widget
## Bell rhythm.  mode "listen": the bell buoy rings long, short, short, long (with ripples, captions, and a notation);
## mode "answer": hold the boat's bell for long, tap it for short.

const PATTERN := ["L", "S", "S", "L"]
const LONG_MS := 380
var mode := "listen"
var center := Vector2.ZERO
var ripples: Array = []        # {t, long}
var t := 0.0
var cycle := 0.0
var played := 0
var seq: Array = []
var press_ms := 0
var last_ms := 0

func _build() -> void:
	mode = args.mode
	center = Vector2(args.cx, args.cy) - position
	mouse_filter = Control.MOUSE_FILTER_STOP if mode == "answer" else Control.MOUSE_FILTER_IGNORE
	set_process(true)

func _timeline() -> Array:
	return [[0.2, true], [1.6, false], [2.3, false], [3.1, true]]

func _process(delta: float) -> void:
	if not is_visible_in_tree():
		return
	t += delta
	if mode == "listen":
		cycle += delta
		var tl := _timeline()
		if played < tl.size() and cycle >= tl[played][0]:
			_ring(tl[played][1])
			played += 1
		if cycle > 7.0:
			cycle = 0.0
			played = 0
	for r in ripples:
		r.t += delta
	ripples = ripples.filter(func(r): return r.t < 2.4)
	if mode == "answer" and seq.size() > 0 and Time.get_ticks_msec() - last_ms > 2600:
		seq.clear()
	queue_redraw()

func _ring(is_long: bool) -> void:
	ripples.append({"t": 0.0, "long": is_long})
	Snd.play("buoy_long" if is_long else "buoy_short")

func replay() -> void:
	cycle = 0.0
	played = 0

func _gui_input(e: InputEvent) -> void:
	if mode != "answer" or not (e is InputEventMouseButton) or e.button_index != MOUSE_BUTTON_LEFT:
		return
	accept_event()
	if e.pressed:
		press_ms = Time.get_ticks_msec()
	else:
		press(Time.get_ticks_msec() - press_ms >= LONG_MS)

## one ring of the boat's bell (long if held)
func press(is_long: bool) -> void:
	last_ms = Time.get_ticks_msec()
	ripples.append({"t": 0.0, "long": is_long})
	Snd.play("bell_long" if is_long else "bell_short")
	seq.append("L" if is_long else "S")
	for i in seq.size():
		if seq[i] != PATTERN[i]:
			seq.clear()
			event("wrong", {})
			return
	if seq.size() == PATTERN.size():
		seq.clear()
		event("answered", {})

func _draw() -> void:
	for r in ripples:
		var k: float = r.t / 2.4
		var rad: float = (80.0 + 420.0 * k) * (1.25 if r.long else 0.8)
		var a: float = (1.0 - k) * 0.8
		draw_arc(center, rad, 0, TAU, 48, Color(0.75, 0.9, 0.95, a), 10.0 if r.long else 5.0)
	if mode == "answer":
		# the notation of what you've rung so far
		for i in seq.size():
			var p := Vector2(center.x - 120.0 + i * 80.0, size.y - 40.0)
			if seq[i] == "L":
				draw_rect(Rect2(p - Vector2(28, 8), Vector2(56, 16)), Color("#efe5c6"), true)
			else:
				draw_circle(p, 10, Color("#efe5c6"))
