extends "res://tests/test_base.gd"
## Chapter 4: both eras, the pocket watch, the logbook, oil, chain, lens, the sleeper and the light.

func _initialize() -> void:
	_run()

func _run() -> void:
	await boot()
	G.new_game()
	await tick()
	G.select_chapter(4)
	await tick()
	var ch = G.chapter
	check(G.s.view == "c4_door", "chapter 4 starts at the lighthouse door")
	# 4.1
	await use("lhkey", "door_lock")
	flag("door_open", "the key opens the door")
	await click("enter")
	check(G.s.view == "c4_store_a", "inside the store room")
	check(not main.time_btn.visible, "no Then/Now button before the watch works")
	# 4.2 stem in the tin, watch in the quarters; the oilcan is only there in Then
	check(not main.click_hotspot("oilcan"), "no oilcan in the present")
	await click("tin")
	await click("stem")
	check(G.has("stem"), "winding stem")
	# F7: the creaking step
	await at("c4_store_b")
	await click("stairs_look")
	await click("step_odd"); await click("step_odd")
	await click("frag7")
	check(7 in G.s.frags, "fragment 7 under the creaking step")
	await at("c4_store_b")
	await click("stairs_up")
	check(G.s.view == "c4_quarters_a", "stairs up to the quarters")
	await click("watch")
	check(G.has("watch"), "the stopped watch")
	G.combine("stem", "watch")
	check(G.has("pocket_watch") and G.f("watch_ok"), "stem + watch = working pocket watch")
	await tick()
	check(main.time_btn.visible, "Then/Now button appears")
	check(G.era() == "now", "start in Now")
	# the present: drawer rusted shut, logbook torn, valve seized
	G.turn(1); await tick()
	check(G.s.view == "c4_quarters_b", "quarters wall B")
	await click("drawer")
	check(not main.click_hotspot("chain"), "chain not visible in Now")
	await click("drawer_now")
	check(not G.has("chain"), "rusted shut in Now")
	await at("c4_watch_a")
	await click("logbook")
	await click("log_torn")
	check(not G.f("log_read"), "the page is torn out in Now")
	await at("c4_valves")
	var vw := wid("valves")
	vw._step(1, -1)
	check(G.fi("valve_1") == 5, "the middle valve is seized in Now")
	# switch to Then
	ch.toggle_era()
	check(G.era() == "then", "Then")
	check(G.f("rule_shown"), "the carry rule is shown once")
	# 4.4 oilcan (store room, Then), 4.5 chain (drawer, Then), F8 calendar, 4.3 logbook, 4.7 sleeper
	await at("c4_store_a")
	await click("oilcan")
	check(G.has("oilcan"), "oilcan in Then")
	await at("c4_quarters_b")
	await click("drawer")
	await click("chain")
	check(G.has("chain"), "spare chain from the drawer in Then")
	await at("c4_calendar")
	await click("cal_page")
	flag("cal_lifted", "calendar page lifted in Then")
	await at("c4_watch_a")
	await click("logbook")
	await click("log_page")
	flag("log_read", "the log is whole in Then")
	check("valves" in G.s.notes, "valve settings sketched")
	await at("c4_watch_a")
	await click("chair")
	check(G.s.view == "c4_sleeper", "the chair close-up")
	await click("sleeper")
	await tick(3)
	flag("sleeper_seen", "the sleeper turns at 4:20")
	await at("c4_valves")
	await use("oilcan", "valve_board")
	flag("valve_oiled", "valve oiled in Then")
	# back to Now: carry crosses, persistence holds
	ch.toggle_era()
	check(G.era() == "now" and G.has("chain") and G.has("pocket_watch"), "carried items cross back to Now")
	await at("c4_valves")
	vw = wid("valves")
	var want := [3, 1, 4]
	for i in 3:
		var guard := 0
		while G.fi("valve_%d" % i) != want[i] and not G.f("valves_ok") and guard < 12:
			guard += 1
			vw._step(i, -1 if posmod(G.fi("valve_%d" % i) - want[i], 10) <= 5 else 1)
	flag("valves_ok", "valves set to 3-1-4 in Now")
	# F8 in Now: pinned behind where the page was
	await at("c4_calendar")
	await click("frag8")
	check(8 in G.s.frags, "fragment 8 behind the lifted calendar page, in Now")
	# 4.5 fit the chain in Now
	await at("c4_lamp_b")
	await click("chain_mech")
	await use("chain", "chain_break")
	flag("chain_fixed", "chain fitted in Now")
	# 4.6 the lens
	await at("c4_lamp_a")
	await click("lens")
	var bw := wid("beam")
	var target := [0, 1, 0, 0, 0, 0, 1, 0, 0]
	var cfg: Array = G.s.flags["lens_cfg"]
	for i in 9:
		if G.f("lens_ok"):
			break
		if int(cfg[i]) != target[i]:
			bw.turn(i)
	flag("lens_ok", "the beam leaves by the sea window")
	# 4.8 the light
	await at("c4_lamp_a")
	await use("lantern_lit", "wick")
	flag("lamp_lit", "the far light is lit")
	await tick(4)
	check(int(G.s.chapter) == 5, "chapter 4 hands over to chapter 5")
	check(G.views.has(G.s.view), "chapter 5 opens in a real view (%s)" % G.s.view)
	var scr = load("res://game/chapters/ch4.gd").new()
	for p in scr.puzzles():
		for t in 3:
			check(L.has_key("hint.%s.%d" % [p.id, t + 1]), "hint text for %s tier %d" % [p.id, t + 1])
	finish()
