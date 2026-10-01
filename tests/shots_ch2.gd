extends "res://tests/test_base.gd"
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.new_game()
	G.select_chapter(2)
	await tick(3)
	await shot("c2_jetty")
	await at("c2_bh_left"); await tick(3); await shot("c2_left_dark")
	G.take("lantern_lit"); G.setf("hung", "left"); G.setf("hung_once"); await tick(8)
	await shot("c2_left_lit")
	await at("c2_net"); await tick(3); await shot("c2_net_tiles")
	await at("c2_gap"); await tick(3); G.give("net", true); await tick(30); await shot("c2_gap")
	await at("c2_winch"); G.setf("peg_0", "gear_s"); G.setf("peg_1", "gear_m"); G.setf("peg_2", "gear_l"); await tick(3); await shot("c2_winch_gears")
	await at("c2_chain"); await tick(3); await shot("c2_chain")
	await at("c2_tide"); await tick(3); await shot("c2_tide")
	await at("c2_bh_right"); G.setf("hung", "right"); G.setf("boat_lowered"); G.setf("hull_ok"); await tick(40); await shot("c2_right_lowered")
	finish()
