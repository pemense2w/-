extends Chapter
## Chapter 3 - The Crossing.  Rowing by the chart; rhythm.  7 puzzles, 2 secrets, Memory 3.
##
## The lake is a 5x5 grid (col, row); the boat starts at (2,4) with the cottage window due south.
## Fog hides everything but the next cell (two cells once the fog has lifted).
## Rowing rules: at most six moves between landmarks; a wrong turn drifts back one cell; visited landmarks are one tap away.

const LM := {
	"red": [0, 3], "green": [1, 2], "pale": [3, 2], "yellow": [3, 4],
	"tree": [4, 3], "reeds": [4, 4], "buoy": [4, 1], "deep": [3, 1], "landing": [2, 0],
}
const FLOATS := ["red", "green", "pale", "yellow"]
const DIRS := {"n": Vector2i(0, -1), "e": Vector2i(1, 0), "s": Vector2i(0, 1), "w": Vector2i(-1, 0)}
const DEEP := Vector2i(3, 1)

func _init() -> void:
	id = 3
	for d in ["n", "e", "s", "w"]:
		reg("row_" + d, func(): move(d); return true)
	reg("look_here", func(): _look_here(); return true)
	reg("look_down", func(): _look_down(); return true)
	reg("to_deck", func(): G.go("c3_deck"); return true)
	reg("to_chart", func(): _open_chart(); return true)
	reg("chart_table", func(): _open_chart(); return true)
	reg("compass", func(): G.go("c3_compass"); return true)
	reg("compass_card", func(): G.say("c3.compass_look"); return true)
	reg("chart_paper", func(): G.say("c3.chart_look"); return true)
	reg("lantern_deck", func(): G.say("c3.lantern_look"); return true)
	reg("line_coil", func(): G.say("c3.line_look"); return true)
	reg("pell", func(): _pell(); return true)
	reg("float", func(): _float_touch(); return true)
	reg("tree", func(): G.say("c3.tree_look"); return true)
	reg("bottle", func():
		G.say("c3.bottle_high")
		return true,
	func(item):
		if item == "net":
			_take_bottle()
			return true
		return false)
	reg("reeds", func(): G.say("c3.reeds_look"); return true)
	reg("reed_bottle", func():
		G.setf("got_frag5")
		G.add_fragment(5)
		return true)
	reg("buoy_body", func():
		G.say("c3.buoy_again")
		G.fx.emit("buoy_again", {})
		return true)
	reg("bell_body", func(): G.say("c3.bell_hint"); return true)
	reg("boat_bell", func(): G.go("c3_bell"); return true)
	reg("deep_water", func(): G.say("c3.deep_look"); return true)
	reg("heron_mast", func():
		if not G.f("heron_gave"):
			G.setf("heron_gave")
			Snd.play("heron")
			G.say("c3.heron_gives")
		return true)
	reg("frag6", func():
		G.setf("got_frag6")
		G.add_fragment(6)
		return true)
	reg("down_look", func(): G.say("c3.down_see"); return true)
	reg("post_hit", func(): G.say("c3.post_look"); return true)

func start() -> void:
	G.setf("c3_x", 2)
	G.setf("c3_y", 4)
	G.setf("c3_px", 2)
	G.setf("c3_py", 4)
	G.s.flags["c3_seen"] = [4 * 5 + 2]
	G.setf("channel_prog", 0)
	G.go("c3_stern")
	G.say("c3.intro")
	Snd.ambience("c3")

func resumed() -> void:
	Snd.ambience("c3")

func carry_in() -> void:
	for it in ["lantern_lit", "chart", "net"]:
		G.give(it, true)
	G.setf("got_jar")
	G.setf("bow_lamp")

func puzzles() -> Array:
	return [
		P("3.1", "true", "f('compass_ok')", ["c3_deck", "c3_compass", "c3_chart"]),
		P("3.2", "f('compass_ok')", "f('channel_done')", ["c3_chart", "c3_float", "c3_bow", "c3_starboard", "c3_stern", "c3_port"]),
		P("3.3", "f('compass_ok')", "f('got_tomas_note')", ["c3_tree", "c3_starboard", "c3_bow"]),
		P("3.4", "f('channel_done')", "f('bell_ok')", ["c3_buoy", "c3_bell", "c3_stern"]),
		P("3.5", "f('bell_ok')", "f('got_lhkey')", ["c3_deck"]),
		P("3.6", "f('bell_ok')", "f('moth3')", ["c3_deep", "c3_bow"]),
		P("3.7", "f('moth3')", "f('moored')", ["c3_landing", "c3_chart"]),
	]

# --------------------------------------------------------- position & fog
func pos() -> Vector2i:
	return Vector2i(G.fi("c3_x"), G.fi("c3_y"))

func landmark_at(x: int, y: int) -> String:
	for k in LM:
		if LM[k][0] == x and LM[k][1] == y:
			return k
	return ""

func here(what: String) -> bool:
	return LM.has(what) and pos() == Vector2i(LM[what][0], LM[what][1])

func here_any() -> bool:
	return landmark_at(pos().x, pos().y) != ""

func near(what: String, dir: String) -> bool:
	if not LM.has(what) or not DIRS.has(dir):
		return false
	var target := Vector2i(LM[what][0], LM[what][1])
	var steps := 2 if G.f("fog_lifted") else 1
	for k in range(1, steps + 1):
		if pos() + DIRS[dir] * k == target:
			return true
	return false

func move(dir: String) -> void:
	if not G.f("compass_ok"):
		G.say("c3.no_heading")
		Snd.play("oar_idle")
		return
	var p := pos()
	if p == DEEP and not G.f("lookdown_done"):
		G.say("c3.boat_wont_move")
		Snd.play("oar_stuck")
		return
	var np: Vector2i = p + DIRS[dir]
	if np.x < 0 or np.x > 4 or np.y < 0 or np.y > 4:
		G.say("c3.chart_edge")
		return
	if np.y <= 1 and not G.f("channel_done") and p.y >= 2:
		G.say("c3.shoal")
		Snd.play("scrape")
		return
	if np.y == 0 and not G.f("moth3"):
		G.say("c3.fog_wall")
		return
	_enter(np)

func _enter(np: Vector2i) -> void:
	G.setf("c3_px", pos().x)
	G.setf("c3_py", pos().y)
	G.setf("c3_x", np.x)
	G.setf("c3_y", np.y)
	var seen: Array = G.s.flags.get("c3_seen", [])
	var idx := np.y * 5 + np.x
	if not (idx in seen):
		seen.append(idx)
	G.s.flags["c3_seen"] = seen
	Snd.play("oar")
	var lm := landmark_at(np.x, np.y)
	if lm != "":
		G.say("c3.arrive." + lm)
	else:
		G.say_text(L.pick("c3.row"))
	G.changed.emit()

func teleport(x: int, y: int) -> void:
	var seen: Array = G.s.flags.get("c3_seen", [])
	if not ((y * 5 + x) in seen) or landmark_at(x, y) == "":
		G.say("c3.chart_tap")
		return
	if not G.f("compass_ok"):
		G.say("c3.no_heading")
		return
	if pos() == DEEP and not G.f("lookdown_done"):
		G.say("c3.boat_wont_move")
		return
	if Vector2i(x, y) == pos():
		return
	if y <= 1 and not G.f("channel_done") and pos().y >= 2:
		G.say("c3.shoal")
		return
	_enter(Vector2i(x, y))
	G.say("c3.teleport")

func _look_here() -> void:
	match landmark_at(pos().x, pos().y):
		"red", "green", "pale", "yellow":
			G.go("c3_float")
		"tree":
			G.go("c3_tree")
		"reeds":
			G.go("c3_reeds")
		"buoy":
			G.go("c3_buoy")
		"deep":
			G.go("c3_deep")
		"landing":
			G.go("c3_landing")

func _open_chart() -> void:
	if G.has("chart"):
		G.go("c3_chart")
	else:
		G.say("c3.no_chart")

# ------------------------------------------------------------ puzzles
func _float_touch() -> void:
	var c := landmark_at(pos().x, pos().y)
	if not (c in FLOATS):
		return
	if G.f("channel_done"):
		G.say("c3.float_done")
		return
	var prog := G.fi("channel_prog")
	if c == FLOATS[prog]:
		prog += 1
		G.s.flags["channel_prog"] = prog
		Snd.play("float_chime", 1.0 + 0.12 * prog)
		if prog == 4:
			G.setf("channel_done")
			G.solve("3.2")
			G.say("c3.channel_open")
		else:
			G.say("c3.float_ok.%d" % prog)
		G.go("c3_bow")
	elif prog > 0 and c == FLOATS[prog - 1]:
		G.say("c3.float_again")
	else:
		# a wrong turn: the channel closes behind you and the current drifts the boat back one cell
		G.s.flags["channel_prog"] = 0
		var px := G.fi("c3_px")
		var py := G.fi("c3_py")
		G.setf("c3_x", px)
		G.setf("c3_y", py)
		Snd.play("scrape")
		G.say("c3.float_wrong")
		G.go("c3_bow")

func _take_bottle() -> void:
	if G.f("got_tomas_note"):
		return
	if G.give("tomas_note"):
		G.setf("got_tomas_note")
		G.solve("3.3")
		Snd.play("splash")
		G.say("c3.bottle_net")
		G.inspect_item("tomas_note")

func _pell() -> void:
	if not G.f("pell_asks") or G.f("got_lhkey"):
		Snd.play("pell_talk")
		G.say_text(L.pick("c3.pell_chat"))
		return
	if not G.f("pell_confirm"):
		G.setf("pell_confirm")
		Snd.play("pell_talk")
		G.say("c3.pell_asks")
		return
	if G.s.items.size() >= G.SATCHEL_SLOTS:
		G.say("satchel.full")
		return
	G.busy = true
	Snd.play("splash")
	G.say("c3.pell_dives")
	await G.wait(1.8)
	G.give("lhkey")
	G.setf("got_lhkey")
	G.solve("3.5")
	G.say("c3.pell_returns")
	G.busy = false

func _look_down() -> void:
	if pos() == DEEP:
		if G.f("lookdown_done"):
			G.say("c3.down_done")
		else:
			G.go("c3_down")
	else:
		G.say("c3.down_nothing")

func view_entered(view: String) -> void:
	match view:
		"c3_buoy":
			G.note("bell")
			G.say("c3.buoy_rings")
		"c3_down":
			_down_scene()
		"c3_deep":
			if not G.f("deep_seen"):
				G.setf("deep_seen")
				G.say("c3.deep_arrive")
		"c3_landing":
			G.say("c3.landing_arrive")

func _down_scene() -> void:
	if G.f("lookdown_done"):
		return
	G.busy = true
	await G.wait(0.5)
	if G.settings.startle:
		Snd.play("sting")
		G.fx.emit("startle", {})
	else:
		G.fx.emit("slowfade", {"secs": 4.0})
	G.say("c3.down_see")
	await G.wait(3.6 if G.settings.startle else 5.0)
	G.setf("lookdown_done")
	G.busy = false
	await G.play_memory(3)
	G.setf("moth3")
	G.solve("3.6")
	G.say("c3.down_after")
	G.go("c3_deep")

func widget_event(wid: String, ev: String, data: Dictionary) -> void:
	match wid:
		"compass":
			if ev == "solved":
				G.solve("3.1")
				G.say("c3.compass_set")
		"rhythm":
			if ev == "wrong":
				G.say("c3.bell_wrong")
			elif ev == "answered":
				if here("buoy"):
					if not G.f("bell_ok"):
						G.setf("bell_ok")
						G.setf("fog_lifted")
						G.setf("pell_asks")
						G.solve("3.4")
						Snd.play("buoy_answer")
						G.say("c3.bell_answered")
						G.go("c3_stern")
				else:
					G.say("c3.bell_nothing")
		"moor":
			if ev == "moored":
				G.solve("3.7")
				G.say("c3.moored")
				await G.wait(1.4)
				G.chapter_done(4)
