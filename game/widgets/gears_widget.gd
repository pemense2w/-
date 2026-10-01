extends Widget
## The winch: three gears sit on three pegs; this widget just draws them (spinning once the winch runs).
## Placement is done by the chapter (use a gear on a peg).

const RADIUS := {"gear_s": 40.0, "gear_m": 80.0, "gear_l": 120.0}
var spin := 0.0

func _build() -> void:
	set_process(true)

func refresh() -> void:
	for sid in args.sprites:
		var n := spr(sid)
		if n == null:
			continue
		n.visible = false
		for k in 3:
			if str(G.s.flags.get("peg_%d" % k, "")) == sid:
				n.visible = true
				var p: Array = args.pegs[k]
				n.position = Vector2(p[0], p[1])

func _process(delta: float) -> void:
	if not G.f("winch_run") or G.settings.reduce_motion:
		return
	spin += delta * 1.2
	for sid in args.sprites:
		var n := spr(sid)
		if n and n.visible:
			var k := -1
			for j in 3:
				if str(G.s.flags.get("peg_%d" % j, "")) == sid:
					k = j
			var ratio: float = 40.0 / RADIUS[sid]
			n.rotation = spin * ratio * (1.0 if k % 2 == 0 else -1.0)
