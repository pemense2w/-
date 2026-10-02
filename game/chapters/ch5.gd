extends Chapter
## Chapter 5 - Still Water.  The Keeper's Room twice: Above (dusty) and Below (its mirrored reflection under the lake).
## Three things Ruth never did: say sorry, let someone hear it, and let go.  7 puzzles, 2 secrets, Memory 5, three endings.

func _init() -> void:
	id = 5
	for h in ["barometer", "coal", "vase", "oar_stand", "table"]:
		reg(h)
	reg("window", func(): G.say("c5.window"); return true)
	reg("desk", func(): G.say("c5.desk"); return true)
	reg("sill", func(): G.say("c5.sill"); return true)
	reg("drawer", func(): G.say("c5.drawer"); return true)
	reg("candle", func(): G.say("c5.candle"); return true)
	reg("painting", func(): G.say("c5.painting"); return true)
	reg("door", func(): G.say("c5.door"); return true)
	reg("coat", func(): G.say("c5.coat"); return true)
	reg("mat", func(): G.say("c5.mat"); return true)
	reg("cabinet", func(): G.say("c5.cabinet"); return true)
	reg("scrap", func(): G.say("c1.sorry"); return true)
	reg("fish_engraving", func(): G.say("c5.fish_below" if _below() else "c1.fish_engraving"); return true)
	reg("hatch", func(): G.say("c5.hatch_open" if G.f("clock5_done") else "c5.hatch_shut"); return true)
	reg("clock_face", func(): _clock_look(); return true)
	reg("photo_face", func(): G.say("c5.photo_turned" if _below() else "c1.photo"); return true)
	reg("ticket_look", func(): G.say("c5.ticket_look"); return true)
	reg("books_row", func(): _books_look(); return true)
	reg("chair_seat", func(): G.say("c5.chair_seat"); return true)
	# --- walls
	reg("clock", func(): G.go("c5_b_clock" if _below() else "c5_a_clock"); return true)
	reg("grate", func(): G.go("c5_b_grate" if _below() else "c5_a_grate"); return true)
	reg("shelf", func(): G.go("c5_b_books" if _below() else "c5_a_books"); return true)
	reg("mirror", func(): G.go("c5_b_mirror" if _below() else "c5_a_mirror"); return true)
	reg("bowl_w", func():
		if _below():
			G.go("c5_b_bowl")
		else:
			G.say("c5.bowl_dry")
		return true)
	reg("photo", func():
		if _below():
			G.go("c5_b_photo")
		else:
			G.say("c1.photo")
		return true)
	reg("armchair", func():
		if _below():
			G.say("c5.armchair_b")
		elif G.f("ticket_valid"):
			G.go("c5_chair")
		else:
			G.say("look.armchair")
		return true)
	reg("plaque", func():
		if not _below():
			G.say("c1.plaque")
		elif not G.f("plaque_moved"):
			G.setf("plaque_moved")
			Snd.play("rustle")
			G.say("c5.plaque_moved")
		return true)
	reg("frag9", func():
		G.setf("got_frag9")
		G.add_fragment(9)
		return true)
	reg("frag10", func():
		G.setf("got_frag10")
		G.add_fragment(10)
		return true)
	# --- the mirror, both ways
	reg("glass", func(): _cross(true); return true)
	reg("glass_b", func(): _cross(false); return true)
	# --- Above: the grate and the clock's gifts
	reg("ash_pile", func():
		if G.give("ash"):
			G.setf("got_ash")
			G.say("c5.ash_take")
		return true)
	reg("logpage", func():
		if G.give("logpage"):
			G.setf("got_logpage")
			G.say("c5.logpage_take")
			G.inspect_item("logpage")
		return true)
	reg("timetable", func():
		if G.give("timetable"):
			G.setf("got_timetable")
			G.say("c5.timetable_take")
			G.inspect_item("timetable")
		return true)
	# --- Below
	reg("grate_b", func(): G.say("c5.grate_b"); return true, func(item): return _grate_use(item))
	reg("letter", func():
		if G.give("letter"):
			G.setf("got_letter")
			G.setf("said_sorry")
			G.solve("5.3")
			G.say("c5.letter_take")
			G.inspect_item("letter")
		return true)
	reg("punch", func():
		if G.give("punch"):
			G.setf("got_punch")
			G.say("c5.punch_take")
		return true)
	reg("bowl", func(): G.say("c5.bowl_empty" if not G.f("pell_home") else "c5.bowl_pell"); return true, func(item):
		if item == "pell_jar":
			_pour_pell()
			return true
		return false)
	reg("moth5", func(): _last_moth(); return true)

func _below() -> bool:
	return String(G.s.view).begins_with("c5_b")

func start() -> void:
	G.setf("clock_h", 9)
	G.setf("clock_m", 35)
	G.setf("mclock_h", 2)
	G.setf("mclock_m", 25)
	for it in G.s.items.duplicate():
		if not (it in ["lantern_lit", "ticket"]):
			G.take(it)
	for it in ["lantern_lit", "ticket", "pell_jar"]:
		G.give(it, true)
	G.go("c5_a_n")
	G.say("c5.intro")
	Snd.ambience("c5")
	Snd.music("still_water")

func resumed() -> void:
	Snd.ambience("c5")

func carry_in() -> void:
	for it in ["lantern_lit", "ticket"]:
		G.give(it, true)

func puzzles() -> Array:
	return [
		P("5.1", "true", "f('crossed')", ["c5_a_s", "c5_a_mirror"]),
		P("5.2", "f('crossed')", "f('clock5_done')", ["c5_b_e", "c5_b_clock", "c5_a_e", "c5_a_clock"]),
		P("5.3", "f('crossed')", "f('said_sorry')", ["c5_a_grate", "c5_b_grate"]),
		P("5.4", "f('crossed')", "f('books5_done')", ["c5_b_w", "c5_b_books", "c5_a_books"]),
		P("5.5", "f('crossed')", "f('heard')", ["c5_b_w", "c5_b_bowl"]),
		P("5.6", "true", "f('ticket_valid')", ["c5_a_clock", "c5_punch"]),
		P("5.7", "f('said_sorry') and f('heard') and f('ticket_valid')", "f('ending')", ["c5_chair", "c5_a_e"]),
	]

func combine(a: String, b: String) -> bool:
	var pair := [a, b]
	pair.sort()
	if pair == ["punch", "ticket"]:
		G.go("c5_punch")
		G.say("c5.punch_ready")
		return true
	return false

func widget_event(wid: String, ev: String, data: Dictionary) -> void:
	match wid:
		"clock":
			if ev == "set":
				# Below the mechanism is mirrored: the clock Above shows 720 minutes minus what this one shows
				var t: int = (int(data.h) * 60 + int(data.m)) % 720
				var above: int = (720 - t) % 720
				G.setf("clock_h", above / 60)
				G.setf("clock_m", above % 60)
				if above / 60 == 4 and above % 60 == 20 and not G.f("clock5_done"):
					G.setf("clock5_done")
					G.solve("5.2")
					Snd.play("clock_open")
					G.say("c5.clock_done")
				else:
					G.say("c5.clock_set_hint")
		"mirror_books":
			if ev == "solved":
				G.solve("5.4")
				Snd.play("cabinet")
				G.say("c5.books_done")
		"punch":
			if ev == "punched":
				if int(data.h) == 4 and int(data.m) == 30:
					G.setf("ticket_valid")
					G.take("punch")
					G.replace_item("ticket", "ticket_ok")
					G.solve("5.6")
					Snd.play("unlock")
					G.say("c5.ticket_valid")
					G.go("c5_a_e")
				else:
					G.say("c5.ticket_wrong")

func _cross(to_below: bool) -> void:
	if to_below:
		if not G.f("crossed"):
			G.setf("crossed")
			G.solve("5.1")
			G.note("mirror")
			G.say("c5.cross_first")
		else:
			G.say("c5.cross_down")
		Snd.play("cross")
		G.go("c5_b_s")
	else:
		G.say("c5.cross_up")
		Snd.play("cross")
		G.go("c5_a_s")

func _clock_look() -> void:
	var h := G.fi("clock_h")
	var m := G.fi("clock_m")
	G.say_text(L.t("c5.clock_reads", ["%d:%02d" % [h if h != 0 else 12, m]]))

func _books_look() -> void:
	if G.f("books5_done"):
		G.say("c5.books_sorted")
	elif _below():
		G.say("c5.books_below")
	else:
		G.say("c5.books_above")

func _grate_use(item: String) -> bool:
	if item == "ash":
		if G.f("ash_placed"):
			G.say("c5.ash_already")
			return true
		G.take("ash")
		G.setf("ash_placed")
		Snd.play("ash")
		G.say("c5.ash_placed")
		return true
	if item == "lantern_lit":
		if not G.f("ash_placed"):
			G.say("c5.grate_nothing")
			return true
		if G.f("backfire"):
			return true
		_backfire()
		return true
	return false

func _backfire() -> void:
	G.setf("backfire")
	Snd.play("flame_back")
	G.say("c5.backfire")
	await G.wait(3.0)
	G.setf("letter_done")
	G.say("c5.letter_whole")

func _pour_pell() -> void:
	G.take("pell_jar")
	G.setf("pell_home")
	G.setf("heard")
	G.solve("5.5")
	Snd.play("splash")
	G.say("c5.pell_poured")
	await G.wait(2.0)
	G.say("c5.pell_last")

func _last_moth() -> void:
	if not G.f("said_sorry"):
		G.say("c5.moth_unsaid")
		return
	if not G.f("heard"):
		G.say("c5.moth_unheard")
		return
	var opts: Array = [{"key": "release", "label": "choice.release"}, {"key": "keep", "label": "choice.keep"}]
	if G.fragment_count() >= 10:
		opts.append({"key": "bell", "label": "choice.bell"})
	G.say("c5.moth_choice")
	var k: String = await G.ask_choice(opts)
	var kind: String = {"release": "A", "keep": "B", "bell": "C"}.get(k, "A")
	G.setf("ending", kind)
	G.solve("5.7")
	await G.play_memory(5)
	G.finish_game(kind)
