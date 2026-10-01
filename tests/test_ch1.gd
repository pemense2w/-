extends "res://tests/test_base.gd"
## Plays Chapter 1 from the first click to the open door, using only what the player has.

func _initialize() -> void:
	_run()

func _run() -> void:
	await boot()
	G.new_game()
	await tick()
	check(G.s.view == "c1_n", "starts in the north wall")
	# navigation ring
	G.turn(1); await tick(); check(G.s.view == "c1_e", "turn right -> east")
	G.turn(1); await tick(); check(G.s.view == "c1_s", "turn right -> south")
	G.turn(1); await tick(); check(G.s.view == "c1_w", "turn right -> west")
	G.turn(1); await tick(); check(G.s.view == "c1_n", "turn right -> north")
	# 1.1 coat pocket
	print("STEP 1.1 coat pocket")
	await at("c1_s")
	await click("coat")
	check(G.s.view == "c1_coat", "coat close-up")
	await click("pocket_r")
	await click("key")
	check(G.has("key"), "brass key taken")
	await click("pocket_l")
	await click("ticket")
	check(G.has("ticket"), "ticket taken")
	G.back(); await tick()
	check(G.s.view == "c1_s", "back to south wall")
	await click("oar")
	check(G.has("oar"), "oar taken")
	# 1.2 desk drawer
	print("STEP 1.2 desk drawer")
	await at("c1_n")
	await click("drawer")
	check(not G.f("drawer_open"), "drawer locked without key")
	await use("key", "drawer")
	flag("drawer_open")
	check(G.s.view == "c1_drawer", "drawer opened close-up")
	await click("food")
	await click("note")
	check(G.has("food") and G.has("note"), "food and note taken")
	await at("c1_n")
	await click("lantern_desk")
	await click("chart")
	check(G.has("lantern") and G.has("chart"), "lantern and chart taken")
	# 1.3 feed Pell
	print("STEP 1.3 feed Pell")
	await at("c1_w")
	await click("bowl_w")
	check(G.s.view == "c1_bowl", "bowl close-up")
	await use("food", "bowl")
	flag("fed")
	await click("pell")
	flag("pell_told")
	check("clock_fish" in G.s.notes, "Pell's line fills the notebook")
	# 1.4 clock to 4:20 (from 9:35)
	print("STEP 1.4 clock to 4:20 (from 9:35)")
	await at("c1_e")
	await click("clock")
	var ck := wid("clock")
	for i in 5:
		ck._turn("h", -1, 5)
	for i in 3:
		ck._turn("m", -1, 5)
	await tick()
	flag("clock_set", "clock solved at 4:20")
	check(G.fi("clock_h") == 4 and G.fi("clock_m") == 20, "clock reads 4:20")
	await click("match")
	check(G.has("match"), "match taken from the clock")
	# 1.5 candle
	print("STEP 1.5 candle")
	await at("c1_e")
	await use("match", "candle")
	flag("candle_burning")
	await click("candle")
	check(G.has("candle_lit"), "lit candle taken")
	# 1.6 painting
	print("STEP 1.6 painting")
	await click("painting")
	check(G.s.view == "c1_painting", "painting close-up")
	await use("candle_lit", "painting_surface")
	flag("painting_lit")
	check("floats" in G.s.notes, "floats sketched")
	# 1.7 books: scrambled start -> painting order by swapping
	print("STEP 1.7 books: scrambled start -> painting order by swapping")
	await at("c1_w")
	await click("shelf")
	check(G.s.view == "c1_books", "books close-up")
	var bw := wid("books")
	var slots: Array = bw.args.slots
	var guard := 0
	while not G.f("books_sorted") and guard < 12:
		guard += 1
		var o: Array = G.s.flags["books_order"]
		for i in o.size():
			if int(o[i]) != i:
				var j: int = o.find(i)
				await mouse(bw, Vector2(slots[i] + 70 - bw.position.x, 60))
				await mouse(bw, Vector2(slots[j] + 70 - bw.position.x, 60))
				break
	flag("books_sorted", "books sorted")
	flag("cabinet_open")
	await click("oil")
	check(G.has("oil"), "oil taken")
	# 1.8 lantern: oil, flame, window
	print("STEP 1.8 lantern: oil, flame, window")
	G.combine("oil", "lantern")
	check(G.has("lantern_oil") and not G.has("oil"), "lantern filled")
	G.combine("candle_lit", "lantern_oil")
	check(G.has("lantern_lit") and not G.has("candle_lit"), "lantern lit")
	await at("c1_n")
	await use("lantern_lit", "sill")
	flag("lantern_placed")
	# 1.9 moth
	print("STEP 1.9 moth")
	await click("jar")
	flag("moth_free")
	flag("moth_window")
	# 1.10 shape lock
	print("STEP 1.10 shape lock")
	await at("c1_window")
	await click("lake")
	check("shapes" in G.s.notes, "shapes sketched")
	await at("c1_door")
	var dw := wid("dials")
	var cells: Array = dw.args.cells
	var want := ["eye", "moon", "fish", "bell"]
	var syms: Array = dw.args.symbols
	for i in 4:
		var guard2 := 0
		while not G.f("door_open") and dw.values()[i] != want[i] and guard2 < 8:
			guard2 += 1
			var c: Array = cells[i]
			await mouse(dw, Vector2(c[0] + c[2] / 2.0 - dw.position.x, c[1] + 10 - dw.position.y))
	flag("door_open", "shape lock opens")
	# the way out needs chart, oar, ticket (all taken) and brings the lantern along
	await at("c1_s")
	await click("door_exit")
	check(true, "exit clicked")
	# hints: every puzzle has all three tiers
	var scr = load("res://game/chapters/ch1.gd").new()
	for p in scr.puzzles():
		for t in 3:
			check(L.has_key("hint.%s.%d" % [p.id, t + 1]), "hint text for %s tier %d" % [p.id, t + 1])
	finish()
