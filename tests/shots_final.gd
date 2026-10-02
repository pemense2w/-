extends "res://tests/test_base.gd"
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.new_game(); await tick(2)
	G.select_chapter(3); await tick(2)
	G.setf("bow_lamp")
	await at("c3_bell"); await tick(4); await shot("final_c3_bell")
	await at("c3_bow"); await tick(4); await shot("final_c3_bow_lamp")
	await at("c3_stern"); await tick(4); await shot("final_c3_stern")
	var sp: Control = load("res://game/core/stage_player.gd").new()
	main.overlay.add_child(sp); sp.play(1)
	await tick(150); await shot("final_mem1")
	sp.queue_free(); await tick(2)
	var sp2: Control = load("res://game/core/stage_player.gd").new()
	main.overlay.add_child(sp2); sp2.play(2)
	await tick(150); await shot("final_mem2")
	finish()
