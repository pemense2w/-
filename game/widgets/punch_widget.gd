extends Widget
## The ferry ticket: pick an hour and a minute (rows of holes), then punch.  The right time makes it valid.

var sel_h := -1
var sel_m := -1
var hole_h: Array = []
var hole_m: Array = []

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	var n_h: int = int(args.hours)
	var n_m: int = int(args.mins)
	for i in n_h:
		hole_h.append(Vector2(60 + i * 80.0, 180))
	for j in n_m:
		hole_m.append(Vector2(60 + j * 80.0, 390))
	var b := UI.button(L.t("ticket.punch"), 260, 66, 28)
	b.position = Vector2(size.x / 2.0 - 130, size.y - 90)
	b.pressed.connect(_punch)
	add_child(b)
	set_process(true)

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	accept_event()
	if G.f(args.flag):
		return
	for i in hole_h.size():
		if e.position.distance_to(hole_h[i]) < 34:
			sel_h = i + 1 if sel_h != i + 1 else -1
			Snd.play("tap")
			queue_redraw()
			return
	for j in hole_m.size():
		if e.position.distance_to(hole_m[j]) < 34:
			sel_m = j * 5 if sel_m != j * 5 else -1
			Snd.play("tap")
			queue_redraw()
			return

func _punch() -> void:
	if G.f(args.flag):
		return
	if sel_h < 0 or sel_m < 0:
		G.say("ticket.pick_both")
		return
	Snd.play("punch")
	event("punched", {"h": sel_h, "m": sel_m})
	sel_h = -1
	sel_m = -1
	queue_redraw()

func _draw() -> void:
	var font := Fonts.world()
	var ink := Color("#3a2418")
	for i in hole_h.size():
		var p: Vector2 = hole_h[i]
		var chosen := (i + 1) == sel_h
		draw_circle(p, 26, Color("#1c1410") if chosen else Color("#e9dfba"))
		draw_arc(p, 26, 0, TAU, 24, ink, 3.0)
		draw_string(font, p + Vector2(-14 if i + 1 >= 10 else -8, 62), str(i + 1), HORIZONTAL_ALIGNMENT_LEFT, -1, 26, ink)
	for j in hole_m.size():
		var p: Vector2 = hole_m[j]
		var chosen := (j * 5) == sel_m
		draw_circle(p, 26, Color("#1c1410") if chosen else Color("#e9dfba"))
		draw_arc(p, 26, 0, TAU, 24, ink, 3.0)
		draw_string(font, p + Vector2(-14, 62), "%02d" % (j * 5), HORIZONTAL_ALIGNMENT_LEFT, -1, 26, ink)
	if G.f(args.flag):
		draw_circle(hole_h[int(args.want_h) - 1], 26, Color("#0a0806"))
		draw_circle(hole_m[int(args.want_m) / 5], 26, Color("#0a0806"))
