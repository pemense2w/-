extends "res://tests/test_base.gd"
## The memories and endings: every sprite exists, every caption has text, and the running times are in range.

var SS = load("res://game/core/stage_scripts.gd")

func _initialize() -> void:
	_run()

func _check_script(name: String, sc: Array, lo: float, hi: float) -> void:
	var total: float = SS.total_time(sc)
	check(total >= lo and total <= hi, "%s runs %.0f s (want %.0f-%.0f)" % [name, total, lo, hi])
	var p = load("res://game/core/stage_player.gd").new()
	for e in sc:
		if e.a == "put":
			var info: Array = p._tex_for(e)
			check(info[0] != null, "%s: sprite '%s' exists" % [name, str(e.get("spr", e.get("img", "?")))])
		if e.a == "cap" or e.a == "title":
			check(L.has_key(str(e.key)), "%s: caption '%s' has text" % [name, str(e.key)])
		if e.a == "bg":
			check(G.views.has(str(e.view)), "%s: bg view '%s' exists" % [name, str(e.view)])
	var ids := {}
	for e in sc:
		if e.a == "put":
			ids[e.id] = true
		elif e.has("id") and e.a != "put" and not e.a.begins_with("photo"):
			check(ids.has(e.id), "%s: '%s' used before it is put on stage" % [name, str(e.id)])
	p.free()

func _run() -> void:
	await boot()
	for n in range(1, 6):
		_check_script("memory %d" % n, SS.memory(n), 25.0, 42.0)
	for k in ["A", "B", "C"]:
		_check_script("ending %s" % k, SS.ending(k), 30.0, 60.0)
		check(G.views.has(SS.ending_bg(k)), "ending %s background exists" % k)
	finish()
