extends Chapter
## Chapter 1 - The Keeper's Room.  Look, take, use.  10 puzzles, 2 secrets, Memory 1.

func _init() -> void:
	id = 1
	# --- north wall
	var place := func(item):
		if item == "lantern_lit":
			G.take("lantern_lit")
			G.setf("lantern_placed")
			G.solve("1.8")
			Snd.play("lantern_set")
			G.say("c1.lantern_placed")
			return true
		if item == "lantern_oil" or item == "lantern":
			G.say("c1.sill_unlit")
			return true
		return false
	reg("window", func(): G.go("c1_window"); return true, place)
	reg("barometer")
	reg("sill", null, place)
	reg("desk")
	reg("drawer", func():
		if not G.f("drawer_open"):
			Snd.play("locked")
			G.say("c1.drawer_locked")
		else:
			G.go("c1_drawer")
		return true,
	func(item):
		if item == "key" and not G.f("drawer_open"):
			G.take("key")
			G.setf("drawer_open")
			Snd.play("unlock")
			G.say("c1.drawer_open")
			G.go("c1_drawer")
			return true
		return false)
	reg("lantern_desk", func():
		G.setf("got_lantern")
		G.give("lantern")
		G.say("c1.lantern_take")
		return true)
	pickup("chart", "got_chart", "chart", "c1.chart_take")
	reg("lantern_win", func(): G.say("c1.lantern_burning"); return true)
	reg("jar", func():
		if not G.f("lantern_placed"):
			Snd.play("flutter")
			G.say("c1.jar_frantic")
			return true
		_free_moth()
		return true)
	reg("moth_n", func(): G.say("c1.moth_free"); return true)
	# --- east wall
	reg("clock", func(): G.go("c1_clock"); return true)
	reg("painting", func(): G.go("c1_painting"); return true)
	reg("grate", func(): G.go("c1_grate"); return true)
	reg("armchair")
	reg("coal")
	reg("vase")
	reg("candle", func():
		if not G.f("candle_burning"):
			G.say("c1.candle_unlit")
		else:
			G.setf("candle_taken")
			G.give("candle_lit")
			G.say("c1.candle_take")
		return true,
	func(item):
		if item == "match" and not G.f("candle_burning"):
			G.take("match")
			G.setf("candle_burning")
			G.solve("1.5")
			Snd.play("match")
			G.say("c1.candle_lit")
			return true
		if item == "match":
			G.say("c1.candle_already")
			return true
		return false)
	# --- clock close-up
	reg("fish_engraving", func():
		G.note("clock_fish")
		G.say("c1.fish_engraving")
		return true)
	reg("hatch", func():
		G.say("c1.hatch_open" if G.f("clock_set") else "c1.hatch_shut")
		return true)
	pickup("match", "got_match", "match", "c1.match_take")
	# --- painting
	var reveal := func(item):
		if item == "candle_lit" or item == "lantern_lit":
			if not G.f("painting_lit"):
				G.setf("painting_lit")
				G.note("floats")
				G.solve("1.6")
				Snd.play("reveal")
				G.say("c1.painting_lit")
			else:
				G.say("c1.painting_seen")
			return true
		return false
	reg("painting_surface", func():
		G.say("c1.painting_seen" if G.f("painting_lit") else "c1.painting_dark")
		return true, reveal)
	# --- south wall
	reg("coat", func(): G.go("c1_coat"); return true)
	reg("mirror", func(): G.go("c1_mirror"); return true)
	reg("oar_stand")
	pickup("oar", "got_oar", "oar", "c1.oar_take")
	reg("mat", func():
		if not G.f("mat_lifted"):
			G.setf("mat_lifted")
			Snd.play("rustle")
			G.say("c1.mat_lift")
		else:
			G.say("c1.mat_again")
		return true)
	reg("frag2", func():
		G.setf("got_frag2")
		G.add_fragment(2)
		return true)
	reg("door", func():
		if G.f("door_open"):
			_leave()
		else:
			G.go("c1_door")
		return true)
	reg("lockplate", func(): G.go("c1_door"); return true)
	reg("door_exit", func(): _leave(); return true)
	reg("lockbox", func(): G.say("c1.lockbox"); return true)
	# --- west wall
	reg("shelf", func(): G.go("c1_books"); return true)
	reg("cabinet", func():
		if not G.f("cabinet_open") and G.current_view().id == "c1_w":
			G.go("c1_books")
		elif not G.f("cabinet_open"):
			Snd.play("locked")
			G.say("c1.cabinet_shut")
		else:
			G.say("c1.cabinet_open_look")
		return true)
	reg("bowl_w", func(): G.go("c1_bowl"); return true, func(item): return _feed(item))
	reg("bowl", func(): _pell(); return true, func(item): return _feed(item))
	reg("pell", func(): _pell(); return true, func(item): return _feed(item))
	reg("table")
	reg("plaque", func(): G.say("c1.plaque"); return true)
	reg("photo", func(): G.go("c1_photo"); return true)
	reg("photo_face", func(): G.say("c1.photo"); return true)
	# --- books / cabinet
	reg("books_row", func(): G.say("c1.books_look" if not G.f("books_sorted") else "c1.books_sorted"); return true)
	pickup("oil", "got_oil", "oil", "c1.oil_take")
	# --- drawer
	reg("drawer_inner")
	reg("food", func():
		G.setf("got_food")
		G.give("food")
		G.say("c1.food_take")
		return true)
	reg("note", func():
		G.setf("got_note")
		G.give("note")
		G.say("c1.note_take")
		G.solve("1.2")
		G.inspect_item("note")
		return true)
	# --- coat
	reg("pocket_l", func():
		if not G.f("pocket_l"):
			G.setf("pocket_l")
			Snd.play("rustle")
			G.say("c1.pocket_l")
		else:
			G.say("c1.pocket_empty")
		return true)
	reg("pocket_r", func():
		if not G.f("pocket_r"):
			G.setf("pocket_r")
			Snd.play("rustle")
			G.say("c1.pocket_r")
		else:
			G.say("c1.pocket_empty")
		return true)
	reg("key", func():
		G.setf("got_key")
		G.give("key")
		G.solve("1.1")
		G.say("c1.key_take")
		return true)
	pickup("ticket", "got_ticket", "ticket", "c1.ticket_take")
	# --- window / lake
	reg("lake", func():
		if G.f("moth_window"):
			G.note("shapes")
			G.say("c1.lake_shapes")
		else:
			G.say("c1.lake_still")
		return true)
	reg("moth_w", func(): G.say("c1.moth_w"); return true)
	reg("lantern_w", func(): G.say("c1.lantern_burning"); return true)
	# --- grate
	reg("scrap", func(): G.say("c1.sorry"); return true)
	reg("ash_pile", func(): G.say("c1.ash"); return true)
	# --- mirror
	reg("mirror_glass", func(): _mirror(); return true)
	reg("frag1", func():
		G.setf("got_frag1")
		G.add_fragment(1)
		return true)

func start() -> void:
	G.setf("clock_h", 9)
	G.setf("clock_m", 35)
	G.go("c1_n")
	G.say("c1.intro")
	Snd.ambience("c1")

func resumed() -> void:
	Snd.ambience("c1")

func carry_in() -> void:
	pass

func puzzles() -> Array:
	return [
		P("1.1", "true", "f('got_key')", ["c1_s", "c1_coat"]),
		P("1.2", "f('got_key')", "f('got_note')", ["c1_n", "c1_drawer"]),
		P("1.3", "f('got_food')", "f('fed')", ["c1_w", "c1_bowl"]),
		P("1.4", "true", "f('clock_set')", ["c1_e", "c1_clock"]),
		P("1.5", "f('clock_set')", "f('candle_burning')", ["c1_e"]),
		P("1.6", "f('candle_burning')", "f('painting_lit')", ["c1_e", "c1_painting"]),
		P("1.7", "f('painting_lit')", "f('cabinet_open')", ["c1_w", "c1_books"]),
		P("1.8", "f('got_oil')", "f('lantern_placed')", ["c1_n"]),
		P("1.9", "f('lantern_placed')", "f('moth_free')", ["c1_n"]),
		P("1.10", "f('moth_window')", "f('door_open')", ["c1_window", "c1_s", "c1_door"]),
	]

func combine(a: String, b: String) -> bool:
	var pair := [a, b]
	pair.sort()
	if pair == ["lantern", "oil"]:
		G.take("oil")
		G.replace_item("lantern", "lantern_oil")
		G.setf("lantern_oiled")
		Snd.play("pour")
		G.say("c1.lantern_oiled")
		return true
	if pair == ["candle_lit", "lantern_oil"]:
		G.take("candle_lit")
		G.replace_item("lantern_oil", "lantern_lit")
		G.setf("candle_used")
		Snd.play("flame")
		G.say("c1.lantern_lit")
		return true
	return false

func widget_event(wid: String, ev: String, data: Dictionary) -> void:
	match wid:
		"clock":
			if ev == "set" and int(data.h) == 4 and int(data.m) == 20 and not G.f("clock_set"):
				G.setf("clock_set")
				G.note("clock_fish")
				G.solve("1.4")
				Snd.play("clock_open")
				G.say("c1.clock_set")
		"books":
			if ev == "solved":
				G.setf("cabinet_open")
				G.solve("1.7")
				Snd.play("cabinet")
				G.say("c1.books_solved")
		"dials":
			if ev == "solved":
				G.solve("1.10")
				G.say("c1.door_unlocked")
				G.go("c1_s")

# ------------------------------------------------------------------ helpers
func _feed(item: String) -> bool:
	if item != "food":
		return false
	if G.f("fed"):
		G.say("c1.pell_full")
		return true
	G.take("food")
	G.setf("fed")
	G.solve("1.3")
	Snd.play("pell_eat")
	G.say("c1.pell_fed")
	return true

func _pell() -> void:
	if not G.f("fed"):
		G.say("c1.pell_hungry")
		return
	if not G.f("pell_told"):
		G.setf("pell_told")
		G.note("clock_fish")
		Snd.play("pell_talk")
		G.say("c1.pell_clock")
	else:
		Snd.play("pell_talk")
		G.say_text(L.pick("c1.pell_chat"))

func _free_moth() -> void:
	G.setf("moth_free")
	Snd.play("jar_open")
	G.say("c1.jar_open")
	G.solve("1.9")
	await G.play_memory(1)
	G.setf("moth_window")
	G.say("c1.moth_window")

func _mirror() -> void:
	var n := G.inc("mirror_looks")
	Snd.play("mirror")
	G.fx.emit("refl_late", {"n": n})
	if n == 1:
		G.say("c1.mirror.1")
	elif n == 2:
		G.say("c1.mirror.2")
	elif n == 3:
		G.say("c1.mirror.3")
		G.setf("mirror_gave")
	else:
		G.say("c1.mirror.4")

func _leave() -> void:
	var missing: Array[String] = []
	for it in ["chart", "oar", "ticket"]:
		if not G.has(it):
			missing.append(it)
	if not missing.is_empty():
		G.say("c1.leave_missing.%s" % missing[0])
		return
	if G.f("lantern_placed") and not G.has("lantern_lit"):
		G.give("lantern_lit", true)
	G.say("c1.leave")
	await G.wait(0.6)
	G.chapter_done(2)
