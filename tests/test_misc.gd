extends "res://tests/test_base.gd"
## Cross-cutting checks: save/load, settings, hint timing, chapter select, localisation completeness.

func _initialize() -> void:
	_run()

func _run() -> void:
	await boot()
	# ---- localisation completeness: every puzzle in every chapter has three hint tiers in every language
	G.new_game()
	await tick()
	for n in range(1, 6):
		G._load_chapter(n)
		var pz: Array = G.chapter.puzzles()
		check(pz.size() >= 5, "chapter %d lists its puzzles (%d)" % [n, pz.size()])
		for p in pz:
			for lang in L.LANGS:
				L.lang = lang
				for tier in [1, 2, 3]:
					check(L.has_key("hint.%s.%d" % [p.id, tier]), "hint.%s.%d missing (%s)" % [p.id, tier, lang])
					var t: String = L.t("hint.%s.%d" % [p.id, tier])
					check(not t.begins_with("⟦"), "hint.%s.%d unresolved (%s)" % [p.id, tier, lang])
			L.lang = "en"
	# every language table carries every English key, with the same placeholders
	for lang in ["zh", "ja"]:
		var missing := 0
		for k in L._tables["en"]:
			if not L._tables[lang].has(k):
				missing += 1
		check(missing == 0, "%s table is missing %d keys" % [lang, missing])
	# every item has a name and description in every language
	var named := 0
	for it in G.items_meta:
		if L._tables["en"].has("item.%s.name" % it):
			named += 1
			for lang in ["zh", "ja"]:
				check(L._tables[lang].has("item.%s.name" % it) and L._tables[lang].has("item.%s.desc" % it), "item %s named and described in %s" % [it, lang])
	check(named > 20, "items have names (%d)" % named)
	for lang in L.LANGS:
		for f in ["world", "ui", "plain"]:
			var suffix: String = "" if lang == "en" else "_" + lang
			check(ResourceLoader.exists("res://assets/fonts/%s%s.ttf" % [f, suffix]), "font %s%s.ttf present" % [f, suffix])

	# ---- save / load round trip
	G.new_game()
	await tick()
	G.give("candle", true)
	G.setf("clock_set")
	G.inc("counter", 3)
	G.note("clock_fish")
	G.s.stats.play_time = 123.0
	await at("c1_e")
	G.save()
	check(G.has_save(), "a save file exists")
	var saved_view: String = G.s.view
	G.s = {}
	G.in_game = false
	var ok: bool = G.continue_game()
	await tick(2)
	check(ok, "continue_game succeeds")
	check(G.s.view == saved_view, "view restored (%s)" % G.s.view)
	check(G.has("candle"), "satchel restored")
	check(G.f("clock_set") and G.fi("counter") == 3, "flags and counters restored")
	check("clock_fish" in G.s.notes, "notebook restored")
	check(absf(float(G.s.stats.play_time) - 123.0) < 5.0, "play time restored (%s)" % G.s.stats.play_time)
	# an old save without newer keys migrates instead of breaking
	var old := {"v": 0, "chapter": 2, "view": "", "items": ["candle"], "flags": {}}
	var mig: Dictionary = G._migrate(old)
	check(mig.has("hints") and mig.has("stats") and mig.has("notes") and mig.has("frags"), "old saves migrate")
	check(mig.v == G.SAVE_VERSION, "migrated save carries the current version")

	# ---- settings persist and apply
	G.set_setting("purist", true)
	G.set_setting("text_scale", 1.4)
	G.set_setting("lang", "ja")
	check(L.lang == "ja", "language setting switches the string table")
	var again := {}
	again = G._read_json(G._save_dir + "settings.json", {})
	check(again.get("purist", false) == true and is_equal_approx(float(again.get("text_scale", 0)), 1.4), "settings are written to disk")
	check(again.get("lang", "") == "ja", "language persists")
	G.new_game(); await tick(2)
	main.open_notebook()
	check(main.modal == null, "purist mode: notebook does not open")
	G.set_setting("purist", false)
	main.open_notebook()
	check(main.modal != null, "notebook opens when purist mode is off")
	main._close_modal(); await tick(2)
	G.set_setting("text_scale", 1.0)
	G.set_setting("lang", "en")

	# ---- hints: first tier at once, later tiers wait, then give the answer
	G.new_game(); await tick(2)
	G.test_mode = false     # hint timing is real time; everything else stays instant
	var h1: Dictionary = G.request_hint()
	check(h1.tier == 1 and h1.wait == 0.0, "first hint is tier 1 immediately")
	var h2: Dictionary = G.request_hint()
	check(h2.tier == 1 and h2.wait > 0.0, "second hint must wait (%s s left)" % h2.wait)
	check(h2.text.contains("\n\n"), "waiting hint says how long")
	var stats_hints: int = G.s.stats.hints
	check(stats_hints == 1, "hint counter counts a tier once")
	# pretend the wait elapsed
	var pid: String = h1.pid
	G.s.hints[pid].t = float(G.s.hints[pid].t) - 100.0
	var h3: Dictionary = G.request_hint()
	check(h3.tier == 2 and h3.wait == 0.0, "tier 2 after waiting")
	G.s.hints[pid].t = float(G.s.hints[pid].t) - 100.0
	var h4: Dictionary = G.request_hint()
	check(h4.tier == 3, "tier 3 gives the answer")
	var h5: Dictionary = G.request_hint()
	check(h5.tier == 3 and h5.wait == 0.0, "tier 3 is final")
	G.test_mode = true

	# ---- chapter select: each chapter starts in a real view with its carried kit
	for n in range(1, 6):
		G.select_chapter(n)
		await tick(2)
		check(G.views.has(G.s.view), "chapter %d starts in a real view (%s)" % [n, G.s.view])
		check(int(G.s.chapter) == n, "chapter number %d recorded" % n)
		check(int(G.profile.unlocked) >= n, "chapter %d unlocked" % n)
	# ---- hotspots: a small hotspot inside a bigger one is the one that gets the click
	G.select_chapter(1); await tick(2)
	G.setf("clock_set"); await at("c1_clock"); await tick(2)
	var mh = main.view.get_hotspot("match")
	check(mh != null and mh.visible, "the match is offered once the clock is set")
	var centre: Vector2 = mh.position + mh.size / 2.0
	check(main.view.hit_test(centre) == mh, "a click on the match lands on the match, not on the hatch around it")
	check(main.click_hotspot("match"), "the match can be clicked")
	await tick(2)
	check(G.has("match"), "the match goes into the satchel")
	# ---- endings are recorded in the profile
	G.finish_game("B")
	check("B" in G.profile.endings and G.profile.finished, "ending recorded in profile")
	finish()
