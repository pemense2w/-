extends Widget
## Two knobs set the hands.  Hour knob: whole hours; minute knob: steps of args.step_m minutes.
## The hands themselves are sprites animated by ViewNode (fx hand_h / hand_m).

func _build() -> void:
	var step: int = int(args.get("step_m", 5))
	for which in ["h", "m"]:
		var kp: Array = args.knob_h if which == "h" else args.knob_m
		for d in [-1, 1]:
			var a := Widget.Arrow.new()
			a.dir = Vector2(d, 0)
			a.size = Vector2(64, 64)
			a.position = Vector2(kp[0] + d * 92 - 32, kp[1] - 32) - position
			a.pressed.connect(_turn.bind(which, d, step))
			add_child(a)

func _turn(which: String, d: int, step: int) -> void:
	var pre: String = args.get("prefix", "clock")
	if G.f(args.get("lock_flag", "clock_set")):
		G.say("clock.locked")
		return
	if which == "h":
		G.setf(pre + "_h", posmod(G.fi(pre + "_h") + d, 12))
	else:
		G.setf(pre + "_m", posmod(G.fi(pre + "_m") + d * step, 60))
	Snd.play("tick")
	event("set", {"h": G.fi(pre + "_h"), "m": G.fi(pre + "_m")})
