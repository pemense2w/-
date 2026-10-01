extends Widget
## The loose compass card: turn it (45 degrees a step) until S faces the lit cottage window, behind the stern.

var pivot_c := Vector2.ZERO

func _build() -> void:
	pivot_c = Vector2(args.cx, args.cy)
	if not G.s.flags.has("compass_rot"):
		G.s.flags["compass_rot"] = 135
	for d in [-1, 1]:
		var a := Widget.Arrow.new()
		a.size = Vector2(110, 110)
		a.dir = Vector2(d, 0)
		a.position = Vector2(args.cx + d * 520 - 55, args.cy - 55) - position
		a.pressed.connect(_turn.bind(d))
		add_child(a)

func _turn(d: int) -> void:
	if G.f(args.flag):
		G.say("c3.compass_locked")
		return
	G.s.flags["compass_rot"] = posmod(G.fi("compass_rot") + d * 45, 360)
	Snd.play("compass")
	if G.fi("compass_rot") == 0:
		G.setf(args.flag)
		event("solved", {})
	else:
		G.changed.emit()

func refresh() -> void:
	var n := spr(str(args.sprite))
	if n:
		n.rotation_degrees = float(G.fi("compass_rot"))
