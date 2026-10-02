extends "res://tests/test_base.gd"
## Chapter 5: through the mirror, the mirrored clock, the unburned letter, mirror books, Pell, the ticket, and all three endings.

func _initialize() -> void:
	_run()

func _run() -> void:
	await boot()
	G.new_game()
	await tick()
	G.select_chapter(5)
	await tick()
	var ch = G.chapter
	check(G.s.view == "c5_a_n", "chapter 5 starts Above")
	check(G.has("lantern_lit") and G.has("ticket") and G.has("pell_jar"), "ticket, lantern and Pell's jar carry in")
	# 5.1 through the mirror
	await at("c5_a_s")
	await click("mirror")
	check(G.s.view == "c5_a_mirror", "the mirror close-up")
	await click("glass")
	flag("crossed", "crossed through the mirror")
	check(G.s.view == "c5_b_s", "Below, on the door wall")
	G.turn(-1); await tick()
	check(G.s.view == "c5_b_w", "turning left Below goes the other way round")
	# F9: the other plaque; F10: the photograph turns
	await click("plaque")
	await click("frag9")
	check(9 in G.s.frags, "fragment 9 behind the reflected plaque")
	await click("photo")
	check(G.s.view == "c5_b_photo", "photograph close-up")
	await click("frag10")
	check(10 in G.s.frags, "fragment 10 from the turned photograph")
	# 5.2 the mirrored clock: Below 7:40 -> Above 4:20
	await at("c5_b_e")
	await click("clock")
	check(G.s.view == "c5_b_clock", "clock Below")
	var cw := wid("clock")
	for i in 5:
		cw._turn("h", 1, 5)
	check(not G.f("clock5_done"), "7:25 Below does not open the clock")
	for i in 3:
		cw._turn("m", 1, 5)
	flag("clock5_done", "clock opens with 7:40 below")
	check(G.fi("clock_h") == 4 and G.fi("clock_m") == 20, "the clock Above reads 4:20")
	await at("c5_a_clock")
	await click("logpage"); await click("timetable")
	check(G.has("logpage") and G.has("timetable"), "log page and timetable from the clock")
	# 5.3 ash Above, unburned letter Below
	await at("c5_a_grate")
	await click("ash_pile")
	check(G.has("ash"), "ash from the grate Above")
	await at("c5_b_grate")
	await use("lantern_lit", "grate_b")
	check(not G.f("backfire"), "no fire without ash")
	await use("ash", "grate_b")
	flag("ash_placed")
	await use("lantern_lit", "grate_b")
	flag("backfire", "the fire runs backwards")
	flag("letter_done", "the letter comes back whole")
	await click("letter")
	check(G.has("letter") and G.f("said_sorry"), "Ruth's letter")
	# 5.4 mirror books (reading right to left)
	await at("c5_b_books")
	var bw := wid("books")
	var slots: Array = bw.args.slots
	var guard := 0
	while not G.f("books5_done") and guard < 12:
		guard += 1
		var o: Array = G.s.flags["books5_order"]
		for i in o.size():
			if int(o[i]) != i:
				var j: int = o.find(i)
				await mouse(bw, Vector2(slots[i] + 70 - bw.position.x, 60))
				await mouse(bw, Vector2(slots[j] + 70 - bw.position.x, 60))
				break
	flag("books5_done", "mirror books sorted")
	await click("punch")
	check(G.has("punch"), "ticket punch behind the books")
	# 5.5 Pell comes home
	await at("c5_b_bowl")
	await use("pell_jar", "bowl")
	flag("heard", "Pell comes home")
	check(not G.has("pell_jar"), "Pell leaves the jar")
	# 5.6 the ticket
	G.combine("punch", "ticket")
	check(G.s.view == "c5_punch", "punch view")
	var pw := wid("punch")
	pw.sel_h = 5
	pw.sel_m = 15
	pw._punch()
	check(not G.f("ticket_valid"), "a wrong time does not validate the ticket")
	pw.sel_h = 4
	pw.sel_m = 30
	pw._punch()
	flag("ticket_valid", "4:30 validates the ticket")
	check(G.has("ticket_ok") and not G.has("ticket"), "the ticket is now valid")
	# 5.7 the last moth: Ending A
	await at("c5_a_e")
	await click("armchair")
	check(G.s.view == "c5_chair", "the armchair has turned: close-up")
	G.test_choice = "release"
	await click("moth5")
	check(G.f("ending") == "A", "release = Ending A")
	check("A" in G.profile.endings and G.profile.finished, "Ending A recorded; chapter select unlocks")
	# Ending C needs all ten fragments; B keeps the moth
	G.setf("ending", "")
	G.test_choice = "keep"
	await ch._last_moth()
	check(G.f("ending") == "B" and "B" in G.profile.endings, "keep = Ending B")
	G.setf("ending", "")
	G.profile.frags = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	G.test_choice = "bell"
	await ch._last_moth()
	check(G.f("ending") == "C" and "C" in G.profile.endings, "ten fragments + the bell = Ending C")
	var scr = load("res://game/chapters/ch5.gd").new()
	for p in scr.puzzles():
		for t in 3:
			check(L.has_key("hint.%s.%d" % [p.id, t + 1]), "hint text for %s tier %d" % [p.id, t + 1])
	finish()
