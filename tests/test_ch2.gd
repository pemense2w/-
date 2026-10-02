extends "res://tests/test_base.gd"
## Chapter 2 from the jetty to the launch, including both secrets.

func _initialize() -> void:
	_run()

func _run() -> void:
	await boot()
	G.new_game()
	await tick()
	G.select_chapter(2)
	await tick()
	check(G.s.view == "c2_jetty", "chapter 2 starts on the jetty")
	check(G.has("lantern_lit") and G.has("oar") and G.has("chart") and G.has("ticket"), "carried-in items")
	# 2.1 the walls are dark until the lantern hangs on one
	await at("c2_bh_door"); await click("door_out"); check(G.s.view == "c2_jetty", "door leads back out")
	await click("bh_door")
	G.turn(1); await tick()
	check(G.s.view == "c2_bh_left", "turn right -> workbench wall")
	check(G.evf(G.current_view().get("dark")) > 0.9, "left wall is dark without the lantern")
	await use("lantern_lit", "hook_left")
	flag("hung_once")
	check(G.fs("hung") == "left" and not G.has("lantern_lit"), "lantern hangs on the left wall")
	check(G.evf(G.current_view().get("dark")) < 0.3, "left wall is lit by the lantern")
	G.turn(1); await tick()
	check(G.evf(G.current_view().get("dark")) > 0.9, "back wall stays dark")
	G.turn(-1); await tick()
	# 2.3 tar, rag, patch
	await click("tar_pot")
	check(G.has("tar"), "tar softened by the hung lantern")
	await click("tackle")
	await click("rag"); await click("corkscrew")
	check(G.has("rag") and G.has("corkscrew"), "rag and corkscrew from the tackle box")
	G.back(); await tick()
	G.combine("rag", "tar")
	check(G.has("patch") and not G.has("rag") and not G.has("tar"), "rag + tar = patch")
	# Pell's jar, small gear, hollow plank (secret F3)
	await click("jar"); check(G.f("got_jar"), "Pell's jar")
	await click("gear_s"); check(G.has("gear_s"), "small gear")
	await click("plank"); await click("plank")
	await click("frag3")
	check(3 in G.s.frags, "fragment 3 under the hollow plank")
	# 2.4 net tiles
	await click("net_tangle")
	check(G.s.view == "c2_net", "net close-up")
	var tw := wid("tiles")
	check(not tw.connected(), "net starts tangled")
	var want := {0: 0, 1: 2, 4: 0, 5: 2, 8: 0}
	for i in want:
		var guard := 0
		while int(G.s.flags["tiles_rot"][i]) != int(want[i]) and guard < 5:
			guard += 1
			tw.turn(i)
	flag("net_untangled", "net untangled")
	await tick()
	await click("net_item")
	check(G.has("net"), "net taken")
	# 2.8 ship in a bottle
	await at("c2_bh_left"); await click("bottle")
	await use("corkscrew", "bottle_cork")
	flag("bottle_open"); flag("bow_lamp")
	# 2.1 move the lantern to the back wall: gear + tide table
	await at("c2_bh_left")
	await click("hook_left")
	check(G.has("lantern_lit"), "lantern taken off its hook")
	G.turn(1); await tick()
	await use("lantern_lit", "hook_back")
	await click("gear_m"); check(G.has("gear_m"), "middle gear")
	await click("tide_board")
	await click("tide_r0")
	check(not ("tide" in G.s.notes), "wrong row does not fill the notebook")
	await click("tide_r4")
	check("tide" in G.s.notes, "04:20 row sketched")
	# 2.7 right wall: gear in a crate, then the winch
	await at("c2_bh_back")
	await click("hook_back")
	G.turn(1); await tick()
	await use("lantern_lit", "hook_right")
	await click("crate"); await click("gear_l")
	check(G.has("gear_l"), "large gear from the crate")
	# 2.3 patch the hull
	await click("hull_hole")
	await use("patch", "hole")
	flag("hull_ok", "hull patched")
	# 2.2 chain lock: 1-7-2
	await at("c2_bh_right")
	await click("chain_lock")
	var dw := wid("dials")
	var cells: Array = dw.args.cells
	var target := [1, 7, 2]
	for i in 3:
		var guard2 := 0
		while G.fi("dial_chain_free_%d" % i) != target[i] and not G.f("chain_free") and guard2 < 12:
			guard2 += 1
			var c: Array = cells[i]
			var cur: int = G.fi("dial_chain_free_%d" % i)
			var up: bool = posmod(target[i] - cur, 10) <= 5
			await mouse(dw, Vector2(c[0] + c[2] / 2.0 - dw.position.x, (c[1] + 10 if up else c[1] + c[3] - 10) - dw.position.y))
	flag("chain_free", "chain lock opens on 172")
	# winch: wrong arrangement first
	await at("c2_winch")
	await use("gear_l", "peg_0"); await use("gear_m", "peg_1"); await use("gear_s", "peg_2")
	await click("crank")
	check(not G.f("boat_lowered"), "wrong gears do not lower the boat")
	await click("peg_0"); await click("peg_1"); await click("peg_2")
	check(G.has("gear_s") and G.has("gear_m") and G.has("gear_l"), "gears return to the satchel")
	await use("gear_s", "peg_0"); await use("gear_m", "peg_1"); await use("gear_l", "peg_2")
	await click("crank")
	flag("boat_lowered", "boat lowered by the winch")
	# 2.5 fish at the gap (miss first, then success), 2.6 heron
	await at("c2_jetty"); await click("gap")
	var cw := wid("catch")
	cw.fish_x = 80.0
	cw._resolve()
	check(G.fi("catch_miss") == 1, "a miss widens the window")
	cw.fish_x = cw.size.x / 2.0
	cw._resolve()
	check(G.has("small_fish"), "fish caught")
	G.back(); await tick()
	G.turn(1); await tick()
	check(G.s.view == "c2_jetty_end", "jetty end")
	await use("small_fish", "heron")
	flag("heron_aside")
	await click("oar2"); check(G.has("oar2"), "second oar from behind the heron")
	# F4: a second fish
	G.back() if false else null
	G.turn(-1); await tick(); await click("gap")
	cw = wid("catch")
	cw.fish_x = cw.size.x / 2.0
	cw._resolve()
	check(G.has("small_fish"), "second fish caught")
	G.back(); await tick(); G.turn(1); await tick()
	await use("small_fish", "heron")
	flag("heron_fed2")
	await click("frag4")
	check(4 in G.s.frags, "fragment 4 from the heron")
	# 2.9 launch: oars into the oarlocks, push off
	await at("c2_bh_right")
	await click("boat")
	check(G.s.view == "c2_boat", "boat deck")
	await click("push_off")
	check(not G.f("launched"), "cannot launch without oars")
	await use("oar", "lock_l"); await use("oar2", "lock_r")
	check(G.f("oar_l") and G.f("oar_r"), "both oars in place")
	await click("push_off")
	flag("launched")
	await tick(4)
	check(int(G.s.chapter) == 3, "chapter 2 hands over to chapter 3")
	check(G.views.has(G.s.view), "chapter 3 opens in a real view (%s)" % G.s.view)
	# hints
	var scr = load("res://game/chapters/ch2.gd").new()
	for p in scr.puzzles():
		for t in 3:
			check(L.has_key("hint.%s.%d" % [p.id, t + 1]), "hint text for %s tier %d" % [p.id, t + 1])
	finish()
