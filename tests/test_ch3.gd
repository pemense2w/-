extends "res://tests/test_base.gd"
## Chapter 3: compass, rowing with fog, the coloured channel, the tree, the bell buoy, Pell's dive, look down, mooring.

func _initialize() -> void:
	_run()

func _run() -> void:
	await boot()
	G.new_game()
	await tick()
	G.select_chapter(3)
	await tick()
	var ch = G.chapter
	check(G.s.view == "c3_stern", "chapter 3 starts astern")
	check(G.has("lantern_lit") and G.has("chart") and G.has("net"), "carried-in items")
	# fog: from the start only the neighbouring cell shows
	check(G.near("yellow", "e") and not G.near("yellow", "n"), "yellow float is one cell east in the fog")
	check(not G.near("pale", "n"), "pale is hidden by the fog")
	# 3.1 no heading without the compass
	await click("row_s")
	check(G.fi("c3_y") == 4, "cannot row without the compass")
	await click("to_deck")
	await click("compass")
	check(G.s.view == "c3_compass", "compass close-up")
	var cw := wid("compass")
	cw._turn(1)
	cw._turn(-1)
	for i in 3:
		cw._turn(-1)
	flag("compass_ok", "compass set with S toward the stern")
	# rowing: stern view row_s works; rows south off the chart are refused
	await at("c3_stern")
	await click("row_s")
	check(G.fi("c3_y") == 4, "the chart's southern edge is a fog wall")
	# 3.2 wrong order first: pale before red resets and drifts back
	for d in ["n", "n", "e"]:
		ch.move(d)
	check(ch.pos() == Vector2i(3, 2), "rowed to the pale float's cell (3,2)")
	await at("c3_bow")
	await click("look_here")
	check(G.s.view == "c3_float", "float close-up")
	await click("float")
	check(G.fi("channel_prog") == 0 and ch.pos() != Vector2i(3, 2), "wrong float: progress resets and the boat drifts back one cell")
	# right order: red (0,3), green (1,2), pale (3,2), yellow (3,4)
	var route := {"red": ["w", "w", "n"], "green": [], "pale": [], "yellow": []}
	# go to red from wherever we drifted: use teleport only for visited landmark cells, so row by hand from (3,3)
	var cur: Vector2i = ch.pos()
	check(cur == Vector2i(2, 2), "drifted back to the cell we came from, (2,2)")
	for d in ["w", "w", "s"]:
		ch.move(d)
	check(ch.pos() == Vector2i(0, 3), "at the red float")
	await at("c3_bow"); await click("look_here"); await click("float")
	check(G.fi("channel_prog") == 1, "red accepted")
	for d in ["n", "e"]:
		ch.move(d)
	await at("c3_bow"); await click("look_here"); await click("float")
	check(G.fi("channel_prog") == 2, "green accepted")
	for d in ["e", "e"]:
		ch.move(d)
	await at("c3_bow"); await click("look_here"); await click("float")
	check(G.fi("channel_prog") == 3, "pale accepted")
	for d in ["s", "s"]:
		ch.move(d)
	await at("c3_bow"); await click("look_here"); await click("float")
	flag("channel_done", "the colored channel opens")
	# shoals are blocked before the channel and open after it
	# 3.3 the drowned tree (4,3): bottle needs the net
	ch.move("n"); ch.move("e")
	check(ch.pos() == Vector2i(4, 3), "at the drowned tree")
	await at("c3_bow"); await click("look_here")
	check(G.s.view == "c3_tree", "tree close-up")
	await use("net", "bottle")
	check(G.has("tomas_note") and G.f("got_tomas_note"), "Tomas's note from the bottle")
	# F5: reeds (4,4)
	ch.move("s")
	await at("c3_bow"); await click("look_here")
	await click("reed_bottle")
	check(5 in G.s.frags, "fragment 5 in the reeds")
	# 3.4 the bell buoy (4,1): fog beyond the shallows is open now
	ch.move("n"); ch.move("n"); ch.move("n")
	check(ch.pos() == Vector2i(4, 1), "at the bell buoy")
	await at("c3_bow"); await click("look_here")
	check(G.s.view == "c3_buoy", "buoy close-up")
	check("bell" in G.s.notes, "bell rhythm sketched")
	await at("c3_stern"); await click("boat_bell")
	check(G.s.view == "c3_bell", "boat's bell close-up")
	var rw := wid("rhythm")
	rw.press(true); rw.press(false); rw.press(true)          # wrong: long short LONG
	check(not G.f("bell_ok"), "a wrong rhythm does not answer the buoy")
	rw.press(true); rw.press(false); rw.press(false); rw.press(true)
	flag("bell_ok", "buoy answered")
	flag("fog_lifted")
	check(G.near("deep", "w"), "the deep is visible from the buoy")
	# 3.5 Pell's dive
	await at("c3_deck")
	await click("pell")
	await click("pell")
	flag("got_lhkey", "Pell fetches the key")
	check(G.has("lhkey"), "lighthouse key in the satchel")
	# 3.6 circled spot: the boat will not move until you look down
	await at("c3_stern")
	ch.move("w")
	check(ch.pos() == Vector2i(3, 1), "at the circled spot")
	ch.move("w")
	check(ch.pos() == Vector2i(3, 1), "the boat will not move at the circled spot")
	await at("c3_bow"); await click("look_here")
	check(G.s.view == "c3_deep", "the deep close-up")
	await click("heron_mast"); await click("frag6")
	check(6 in G.s.frags, "fragment 6 from the heron on the mast")
	await at("c3_bow")
	await click("look_down")
	await tick(3)
	flag("moth3", "look down releases the memory and the moth")
	flag("lookdown_done")
	# 3.7 moor at the landing (2,0)
	ch.move("w")
	check(ch.pos() == Vector2i(2, 1), "free again")
	ch.move("n")
	check(ch.pos() == Vector2i(2, 0), "at the landing")
	await at("c3_bow"); await click("look_here")
	check(G.s.view == "c3_landing", "landing view")
	var mw := wid("moor")
	mw.marker = float(mw.args.target[0]) - mw.position.x + 800.0
	await mouse(mw, Vector2(100, 100))
	check(not G.f("moored"), "a wild throw misses")
	mw.marker = float(mw.args.target[0]) - mw.position.x
	await mouse(mw, Vector2(100, 100))
	flag("moored", "the line catches the post")
	var scr = load("res://game/chapters/ch3.gd").new()
	for p in scr.puzzles():
		for t in 3:
			check(L.has_key("hint.%s.%d" % [p.id, t + 1]), "hint text for %s tier %d" % [p.id, t + 1])
	finish()
