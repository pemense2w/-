extends "res://tests/test_base.gd"
## Screenshots of Chapter 1 in the real renderer (run under xvfb-run, without --headless).
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.new_game()
	await tick(3)
	await shot("c1_start")
	await at("c1_e"); await tick(3); await shot("c1_east_dark")
	await at("c1_clock"); await tick(3); await shot("c1_clock")
	G.give("candle_lit", true); G.give("lantern_lit", true)
	G.held = "candle_lit"
	await at("c1_painting"); await tick(3)
	await shot("c1_painting_dark_candle")
	G.setf("painting_lit"); G.held = ""; await tick(3)
	await shot("c1_painting_lit")
	G.setf("lantern_placed"); G.setf("moth_window")
	await at("c1_n"); await tick(5); await shot("c1_north_lit")
	await at("c1_window"); await tick(5); await shot("c1_window_shapes")
	await at("c1_door"); await tick(5); await shot("c1_door")
	G.note("clock_fish"); G.note("floats"); G.note("shapes")
	main.open_notebook(); await tick(3); await shot("notebook")
	finish()
