extends "res://tests/test_base.gd"
func _initialize() -> void:
	_run()
func _go(kind, at: float, name: String) -> void:
	var p = load("res://game/core/stage_player.gd").new()
	main.overlay.add_child(p)
	p.play(kind)
	p.t = at
	# run the events up to 'at' (tweens play in real time), then give them a moment
	await get_root().get_tree().create_timer(2.2).timeout
	await shot(name)
	p.queue_free()
	await tick(2)
func _run() -> void:
	await boot()
	G.new_game()
	await tick()
	await _go(1, 9.0, "mem1")
	await _go(2, 14.0, "mem2")
	await _go(3, 14.0, "mem3")
	await _go(4, 17.0, "mem4")
	await _go(5, 22.0, "mem5")
	await _go("A", 13.0, "endA1")
	await _go("A", 36.0, "endA2")
	await _go("C", 12.0, "endC1")
	await _go("C", 33.0, "endC2")
	finish()
