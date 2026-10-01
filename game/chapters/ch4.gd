extends Chapter
## Chapter 4 - The Far Light.  Then and Now.  8 puzzles, 2 secrets, Memory 4.
##
## A pocket watch switches between Now (cold, wrecked, raining) and Then (4:19 on the night: warm, lamp burning low, storm).
## Two rules, shown once and never broken: what you carry crosses with you; anything you move in Then stays moved in Now.

func _init() -> void:
	id = 4
	# --- the door
	reg("door_lock", func(): G.say("c4.door_locked"); return true, func(item):
		if item == "lhkey":
			G.take("lhkey")
			G.setf("door_open")
			G.solve("4.1")
			Snd.play("unlock")
			G.say("c4.door_unlocked")
			return true
		return false)
	reg("door", func(): G.say("c4.door_locked"); return true, func(item):
		if item == "lhkey":
			return A["door_lock"].use.call(item)
		return false)
	reg("enter", func(): G.go("c4_store_a"); G.say("c4.enter"); return true)
	for h in ["tower", "rocks", "barrel", "window_s", "window_s2", "stair_steps", "tin_inside", "bed", "bedside", "trunk", "window_q",
			"wardrobe", "chest", "desk_w", "window_w", "lamp_desk", "window_sl", "pipe", "window_wb", "window_sea", "oil_tank", "clockwork",
			"window_lb", "gears_look", "lens_look", "valve_board", "log_left", "cal_behind", "drawer_then"]:
		reg(h)
	# --- store room
	reg("tin", func(): G.go("c4_tin"); return true)
	reg("shelf", func():
		if G.era() == "now" and not G.f("got_oilcan"):
			G.say("c4.shelf_ring")
		else:
			G.say("c4.shelf_look")
		return true)
	reg("oilcan", func():
		if G.give("oilcan"):
			G.setf("got_oilcan")
			G.say("c4.oilcan_take")
		return true)
	reg("stairs_up", func(): _stairs(1); return true)
	reg("stairs_down", func(): _stairs(-1); return true)
	reg("stairs_look", func(): G.go("c4_stairs"); return true)
	reg("step_odd", func():
		if not G.f("step_tapped"):
			G.setf("step_tapped")
			Snd.play("hollow")
			G.say("c4.step_hollow")
		else:
			G.setf("step_lifted")
			Snd.play("crate")
			G.say("c4.step_lift")
		return true)
	reg("frag7", func():
		G.setf("got_frag7")
		G.add_fragment(7)
		return true)
	reg("stem", func():
		if G.give("stem"):
			G.setf("got_stem")
			G.say("c4.stem_take")
		return true)
	# --- quarters
	reg("watch", func():
		if G.give("watch"):
			G.setf("got_watch")
			G.say("c4.watch_take")
		return true)
	reg("drawer", func(): G.go("c4_drawer"); return true)
	reg("calendar", func(): G.go("c4_calendar"); return true)
	reg("drawer_now", func(): G.say("c4.drawer_rust"); Snd.play("seized"); return true)
	reg("chain", func():
		if G.give("chain"):
			G.setf("got_chain")
			G.say("c4.chain_take")
		return true)
	reg("cal_page", func():
		if not G.f("cal_lifted"):
			G.setf("cal_lifted")
			Snd.play("rustle")
			G.say("c4.cal_lift")
			_rule_persist()
		return true)
	reg("cal_now", func(): G.say("c4.cal_now"); return true)
	reg("frag8", func():
		G.setf("got_frag8")
		G.add_fragment(8)
		return true)
	# --- watch room
	reg("logbook", func(): G.go("c4_logbook"); return true)
	reg("chair", func(): G.go("c4_sleeper"); return true)
	reg("log_page", func():
		if not G.f("log_read"):
			G.setf("log_read")
			G.note("valves")
			G.solve("4.3")
			G.say("c4.log_read")
		else:
			G.say("c4.log_again")
		return true)
	reg("log_torn", func(): G.say("c4.log_torn"); return true)
	reg("sleeper", func(): _sleeper_scene(); return true)
	reg("chair_empty", func(): G.say("c4.chair_empty"); return true)
	reg("valves", func(): G.go("c4_valves"); return true)
	reg("valve_board", func(): G.say("c4.valve_board"); return true, func(item):
		if item == "oilcan":
			if G.f("valve_oiled"):
				G.say("c4.valve_oiled_already")
				return true
			G.take("oilcan")
			G.setf("valve_oiled")
			Snd.play("pour")
			G.say("c4.valve_oiled")
			if G.era() == "then":
				_rule_persist()
			return true
		return false)
	# --- lamp room
	reg("lens", func(): G.go("c4_lens"); return true)
	reg("wick", func(): G.say("c4.wick_look"); return true, func(item):
		if item == "lantern_lit":
			_light_lamp()
			return true
		return false)
	reg("chain_mech", func(): G.go("c4_chain"); return true)
	reg("chain_break", func(): G.say("c4.chain_break" if not G.f("chain_fixed") else "c4.chain_fixed"); return true, func(item):
		if item == "chain":
			if G.era() == "then":
				G.say("c4.chain_then")
				return true
			G.take("chain")
			G.setf("chain_fixed")
			G.solve("4.5")
			Snd.play("chain")
			G.say("c4.chain_fit")
			return true
		return false)

func start() -> void:
	G.setf("era", "now")
	G.go("c4_door")
	G.say("c4.intro")
	Snd.ambience("c4_now")

func resumed() -> void:
	Snd.ambience("c4_then" if G.era() == "then" else "c4_now")

func carry_in() -> void:
	G.give("lantern_lit", true)
	G.give("lhkey", true)
	G.setf("got_jar")

func puzzles() -> Array:
	return [
		P("4.1", "true", "f('door_open')", ["c4_door"]),
		P("4.2", "f('door_open')", "f('watch_ok')", ["c4_quarters_a", "c4_store_a", "c4_tin", "c4_store_b"]),
		P("4.3", "f('watch_ok')", "f('log_read')", ["c4_watch_a", "c4_logbook"]),
		P("4.4", "f('log_read')", "f('valves_ok')", ["c4_watch_b", "c4_valves", "c4_store_a"]),
		P("4.5", "f('watch_ok')", "f('chain_fixed')", ["c4_quarters_b", "c4_drawer", "c4_lamp_b", "c4_chain"]),
		P("4.6", "f('door_open')", "f('lens_ok')", ["c4_lamp_a", "c4_lens"]),
		P("4.7", "f('watch_ok')", "f('sleeper_seen')", ["c4_watch_a", "c4_sleeper"]),
		P("4.8", "f('valves_ok') and f('chain_fixed') and f('lens_ok') and f('sleeper_seen')", "f('lamp_lit')", ["c4_lamp_a"]),
	]

func combine(a: String, b: String) -> bool:
	var pair := [a, b]
	pair.sort()
	if pair == ["stem", "watch"]:
		G.take("stem")
		G.replace_item("watch", "pocket_watch")
		G.setf("watch_ok")
		G.solve("4.2")
		Snd.play("watch_wind")
		G.say("c4.watch_fixed")
		return true
	return false

func widget_event(wid: String, ev: String, _data: Dictionary) -> void:
	match wid:
		"valves":
			if ev == "solved":
				G.solve("4.4")
				Snd.play("oil_flow")
				G.say("c4.oil_flows")
		"beam":
			if ev == "solved":
				G.solve("4.6")
				Snd.play("prism_ok")
				G.say("c4.lens_aligned")

# --------------------------------------------------------------- Then and Now
func toggle_era() -> void:
	if not G.f("watch_ok"):
		return
	var now_era := G.era()
	G.setf("era", "then" if now_era == "now" else "now")
	Snd.play("watch_tick")
	Snd.ambience("c4_then" if G.era() == "then" else "c4_now")
	G.fx.emit("era_flip", {})
	if not G.f("rule_shown"):
		G.setf("rule_shown")
		G.say("c4.era_rules")
	else:
		G.say("c4.era_then" if G.era() == "then" else "c4.era_now")

func _rule_persist() -> void:
	if not G.f("rule_persist_shown"):
		G.setf("rule_persist_shown")
		G.say("c4.rule_persist")

func _stairs(dir: int) -> void:
	var cur: String = G.s.view
	var floor_ := 0
	if cur.begins_with("c4_quarters"):
		floor_ = 1
	elif cur.begins_with("c4_watch"):
		floor_ = 2
	elif cur.begins_with("c4_lamp"):
		floor_ = 3
	var nf := clampi(floor_ + dir, 0, 3)
	if nf == floor_:
		return
	Snd.play("steps")
	if dir > 0:
		G.go(["c4_quarters_a", "c4_watch_a", "c4_lamp_a"][floor_])
	else:
		G.go(["c4_store_b", "c4_quarters_b", "c4_watch_b"][nf])

func _sleeper_scene() -> void:
	if G.f("sleeper_seen"):
		G.say("c4.sleeper_again")
		return
	if not G.f("watch_ok"):
		return
	G.busy = true
	G.say("c4.sleeper_watch")
	await G.wait(2.6)
	Snd.play("watch_tick")
	G.say("c4.sleeper_420")
	await G.wait(2.2)
	G.setf("sleeper_turned")
	G.say("c4.sleeper_face")
	await G.wait(3.0)
	G.busy = false
	G.setf("sleeper_seen")
	G.solve("4.7")
	await G.play_memory(4)
	G.say("c4.sleeper_after")

func _light_lamp() -> void:
	if G.era() == "then":
		G.say("c4.lamp_then")
		return
	if not G.f("valves_ok"):
		G.say("c4.lamp_need_oil")
		return
	if not G.f("chain_fixed"):
		G.say("c4.lamp_need_chain")
		return
	if not G.f("lens_ok"):
		G.say("c4.lamp_need_lens")
		return
	if not G.f("sleeper_seen"):
		G.say("c4.lamp_need_past")
		return
	G.setf("lamp_lit")
	G.solve("4.8")
	Snd.play("lamp_light")
	G.say("c4.lamp_lit")
	await G.wait(3.5)
	G.say("c4.lake_still")
	await G.wait(2.5)
	G.chapter_done(5)
