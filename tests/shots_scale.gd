extends "res://tests/test_base.gd"
## Largest text size with the longest captions: checks nothing spills out of its panel (needs a display / xvfb-run).
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.settings.text_scale = 1.5
	for lang in ["en", "zh", "ja"]:
		L.set_language(lang)
		G.new_game(); await tick(3)
		# longest caption of the English table, in this language
		var best := ""
		var best_len := 0
		for k in L._tables["en"]:
			if k.begins_with("c") and not k.begins_with("cap.") and not k.begins_with("chapter") and not k.begins_with("choice") and not k.begins_with("combine"):
				var t: String = L._tables["en"][k]
				if t.length() > best_len and t.length() < 400:
					best_len = t.length(); best = k
		G.say(best); await tick(3); await shot("scale_%s_caption" % lang)
		G.go("c1_e"); await tick(2)
		main.ask_pell(); await tick(4); await shot("scale_%s_hint" % lang)
		main._close_modal(); await tick(2)
		G.note("clock_fish"); G.note("floats"); G.note("shapes")
		main.open_notebook(); await tick(3); await shot("scale_%s_notebook" % lang)
		main._close_modal(); await tick(2)
		main.open_settings(); await tick(3); await shot("scale_%s_settings" % lang)
		main._close_modal(); await tick(2)
	finish()
