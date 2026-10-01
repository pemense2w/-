extends "res://tests/test_base.gd"
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.new_game()
	G.select_chapter(3)
	await tick(3)
	await shot("c3_stern")
	await at("c3_starboard"); await tick(3); await shot("c3_starboard_near_yellow")
	await at("c3_compass"); await tick(3); await shot("c3_compass")
	G.setf("compass_ok"); G.setf("compass_rot", 0)
	var ch = G.chapter
	for d in ["n", "n", "e"]:
		ch.move(d)
	await at("c3_bow"); await tick(3); await shot("c3_bow_here_pale")
	await at("c3_chart"); await tick(3); await shot("c3_chart")
	G.setf("fog_lifted"); G.setf("channel_done")
	ch.move("e"); ch.move("n")
	await at("c3_buoy"); await tick(80); await shot("c3_buoy")
	await at("c3_bow"); await tick(3); await shot("c3_bow_clear")
	await at("c3_deck"); await tick(3); await shot("c3_deck")
	finish()
