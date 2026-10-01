extends "res://tests/test_base.gd"
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.new_game()
	G.select_chapter(4)
	await tick(3)
	G.setf("watch_ok"); G.give("pocket_watch", true)
	await at("c4_watch_a"); await tick(4); await shot("c4_watch_now")
	G.setf("era", "then"); await tick(8); await shot("c4_watch_then")
	await at("c4_sleeper"); G.setf("sleeper_turned"); await tick(8); await shot("c4_sleeper")
	await at("c4_valves"); await tick(3); await shot("c4_valves")
	G.setf("era", "now"); await at("c4_lens"); await tick(3); await shot("c4_lens")
	await at("c4_lamp_a"); G.setf("lamp_lit"); G.setf("valves_ok"); await tick(40); await shot("c4_lamp_lit")
	finish()
