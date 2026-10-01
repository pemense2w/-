extends Chapter
## Chapter 2 - The Boathouse.  Combining items; darkness.  9 puzzles, 2 secrets, Memory 2.

const TIDE_TIMES := ["02:00", "02:40", "03:20", "04:00", "04:20", "04:40", "05:20"]
const TIDE_LEVELS := [131, 139, 150, 165, 172, 181, 196]
const GEAR_R := {"gear_s": 1, "gear_m": 2, "gear_l": 3}
const PEG_D := [3, 5]       # spacings between pegs 0-1 and 1-2, in gear units

func _init() -> void:
	id = 2
	# --- jetty
	reg("bh_door", func(): G.go("c2_bh_door"); return true)
	reg("gap", func(): G.go("c2_gap"); return true)
	for h in ["bollard", "coil", "jetty_lamp", "jetty_water", "piling", "end_water", "far_light", "heron_calm"]:
		reg(h)
	reg("heron", func(): G.say("c2.heron_look" if not G.f("heron_aside") else "c2.heron_aside_look"); return true, func(item): return _feed_heron(item))
	pickup("oar2", "got_oar2", "oar2", "c2.oar2_take")
	reg("frag4", func():
		if G.f("got_frag4"):
			return false
		G.setf("got_frag4")
		G.add_fragment(4)
		return true)
	reg("heron_back", func(): G.say("c2.heron_frag_look"); return true)
	reg("gap_look", func(): G.say("c2.gap_look"); return true)
	# --- door wall
	reg("door_out", func(): G.go("c2_jetty"); return true)
	for h in ["life_ring", "rack", "barrel_d", "bench", "pegboard", "ropes"]:
		reg(h)
	# --- hooks: hang the lantern where you want to see
	for w in ["left", "back", "right"]:
		reg("hook_" + w, func(): return _hook(w), func(item): return _hang(w, item))
	# --- left wall
	reg("net_tangle", func(): G.go("c2_net"); return true)
	reg("tackle", func(): G.go("c2_tackle"); return true)
	reg("tar_pot", func(): return _tar(), func(item):
		if item == "lantern_lit":
			return _tar(true)
		return false)
	reg("bottle", func(): G.go("c2_bottle"); return true)
	reg("jar", func():
		# Pell travels with you (the Ask Pell button); the jar does not use a satchel slot
		G.setf("got_jar")
		Snd.play("pell_talk")
		G.say("c2.jar_take")
		return true)
	pickup("gear_s", "got_gear_s", "gear_s", "c2.gear_take")
	reg("plank", func():
		if G.f("got_frag3"):
			G.say("c2.plank_after")
		elif not G.f("plank_tapped"):
			G.setf("plank_tapped")
			Snd.play("hollow")
			G.say("c2.plank_hollow")
		elif not G.f("plank_lifted"):
			G.setf("plank_lifted")
			Snd.play("rustle")
			G.say("c2.plank_lift")
		return true)
	reg("frag3", func():
		G.setf("got_frag3")
		G.add_fragment(3)
		return true)
	# --- back wall
	reg("tide_board", func(): G.go("c2_tide"); return true)
	reg("winch", func(): G.go("c2_winch"); return true)
	pickup("gear_m", "got_gear_m", "gear_m", "c2.gear_take")
	# --- right wall
	reg("boat", func():
		G.go("c2_boat")
		return true)
	reg("hull_hole", func(): G.go("c2_hull"); return true)
	reg("chain_lock", func():
		if G.f("chain_free"):
			G.say("c2.chain_slack")
		else:
			G.go("c2_chain")
		return true)
	reg("crate", func():
		if not G.f("crate_open"):
			G.setf("crate_open")
			Snd.play("crate")
			G.say("c2.crate_open")
		return true)
	pickup("gear_l", "got_gear_l", "gear_l", "c2.gear_take")
	# --- net / bottle / tackle / tide / winch / chain / hull / boat close-ups
	reg("net_look", func(): G.say("c2.net_look_done" if G.f("net_untangled") else "c2.net_look"); return true)
	reg("net_item", func():
		if G.give("net"):
			G.setf("got_net")
			G.say("c2.net_take")
		return true)
	reg("bottle_glass", func(): G.say("c2.bottle_look"); return true)
	reg("ship", func(): G.say("c2.bottle_look"); return true)
	reg("bottle_cork", func():
		G.say("c2.cork_stuck")
		return true,
	func(item):
		if item == "corkscrew":
			_open_bottle()
			return true
		return false)
	reg("tackle_tray", func(): G.say("c2.tackle_look"); return true)
	pickup("rag", "got_rag", "rag", "c2.rag_take")
	pickup("corkscrew", "got_corkscrew", "corkscrew", "c2.corkscrew_take")
	for i in 7:
		reg("tide_r%d" % i, func(): _tide_row(i); return true)
	for k in 3:
		reg("peg_%d" % k, func(): return _peg_click(k), func(item): return _peg_use(k, item))
	reg("crank", func(): _crank(); return true)
	reg("drum", func(): G.say("c2.drum_look"); return true)
	reg("lock_body", func(): G.say("c2.lock_look"); return true)
	reg("hole", func(): G.say("c2.hole_look" if not G.f("hull_ok") else "c2.hull_ok"); return true,
		func(item):
			if item == "patch":
				G.take("patch")
				G.setf("hull_ok")
				G.solve("2.3")
				Snd.play("patch")
				G.say("c2.hull_patched")
				return true
			if item == "tar" or item == "rag":
				G.say("c2.patch_first")
				return true
			return false)
	reg("lock_l", func(): G.say("c2.oarlock_look"); return true, func(item): return _oarlock("l", item))
	reg("lock_r", func(): G.say("c2.oarlock_look"); return true, func(item): return _oarlock("r", item))
	reg("bow_lamp", func(): G.say("c2.lamp_lit" if G.f("bow_lamp") else "c2.lamp_cold"); return true)
	reg("boat_bell", func():
		Snd.play("bell")
		G.say("c2.bell_ring")
		return true)
	reg("push_off", func(): _push_off(); return true)

func start() -> void:
	G.go("c2_jetty")
	G.say("c2.intro")
	Snd.ambience("c2")

func resumed() -> void:
	Snd.ambience("c2")

func carry_in() -> void:
	for it in ["lantern_lit", "oar", "chart", "ticket"]:
		G.give(it, true)

func puzzles() -> Array:
	return [
		P("2.1", "true", "f('hung_once')", ["c2_bh_door", "c2_bh_left", "c2_bh_back", "c2_bh_right"]),
		P("2.2", "f('hung_once')", "f('chain_free')", ["c2_bh_back", "c2_tide", "c2_bh_right", "c2_chain"]),
		P("2.3", "f('hung_once')", "f('hull_ok')", ["c2_bh_left", "c2_tackle", "c2_bh_right", "c2_hull"]),
		P("2.4", "f('hung_once')", "f('got_net')", ["c2_bh_left", "c2_net"]),
		P("2.5", "f('got_net')", "f('got_fish_once')", ["c2_jetty", "c2_gap"]),
		P("2.6", "f('got_fish_once')", "f('got_oar2')", ["c2_jetty_end"]),
		P("2.7", "f('hung_once')", "f('boat_lowered')", ["c2_bh_back", "c2_winch"]),
		P("2.8", "f('got_corkscrew')", "f('bottle_open')", ["c2_bh_left", "c2_bottle"]),
		P("2.9", "true", "f('launched')", ["c2_bh_right", "c2_boat"]),
	]

func combine(a: String, b: String) -> bool:
	var pair := [a, b]
	pair.sort()
	if pair == ["rag", "tar"]:
		G.take("rag")
		G.replace_item("tar", "patch")
		Snd.play("patch")
		G.say("c2.patch_made")
		return true
	if pair == ["lantern_lit", "rag"]:
		G.say("c2.rag_burn")
		return true
	return false

func widget_event(wid: String, ev: String, data: Dictionary) -> void:
	match wid:
		"dials":
			if ev == "solved":
				G.solve("2.2")
				G.say("c2.chain_open")
				Snd.play("chain")
		"tiles":
			if ev == "solved":
				G.solve("2.4")
				G.say("c2.net_untangled")
		"catch":
			if ev == "caught":
				G.solve("2.5")
				G.say("c2.fish_caught")

# ------------------------------------------------------------------ helpers
func _hook(wall: String) -> bool:
	if G.fs("hung") == wall:
		if G.give("lantern_lit", true):
			G.setf("hung", "")
			Snd.play("lantern_set")
			G.say("c2.lantern_take")
		return true
	G.say("c2.hook_bare")
	return true

func _hang(wall: String, item: String) -> bool:
	if item != "lantern_lit":
		return false
	G.take("lantern_lit")
	G.setf("hung", wall)
	if not G.f("hung_once"):
		G.setf("hung_once")
		G.solve("2.1")
	Snd.play("lantern_set")
	G.say("c2.lantern_hung.%s" % wall)
	return true

func _tar(with_lantern: bool = false) -> bool:
	if G.f("got_tar"):
		G.say("c2.tar_empty")
		return true
	if G.fs("hung") == "left" or with_lantern:
		if G.give("tar"):
			G.setf("got_tar")
			Snd.play("tar")
			G.say("c2.tar_soft")
		return true
	G.say("c2.tar_cold")
	return true

func _feed_heron(item: String) -> bool:
	if item != "small_fish":
		return false
	G.take("small_fish")
	if not G.f("heron_aside"):
		G.setf("heron_aside")
		G.solve("2.6")
		Snd.play("heron")
		G.say("c2.heron_fed1")
	elif not G.f("heron_fed2"):
		G.setf("heron_fed2")
		Snd.play("heron")
		G.say("c2.heron_fed2")
	else:
		G.give("small_fish", true)
		G.say("c2.heron_full")
	return true

func _open_bottle() -> void:
	if G.f("bottle_open"):
		return
	G.take("corkscrew")
	G.setf("bottle_open")
	G.solve("2.8")
	Snd.play("cork")
	G.say("c2.bottle_open")
	await G.play_memory(2)
	G.setf("bow_lamp")
	G.say("c2.bow_lamp_lit")

func _tide_row(i: int) -> void:
	if i == 4:
		G.note("tide")
		G.say("c2.tide_420")
	else:
		G.say_text(L.t("c2.tide_other", [TIDE_TIMES[i], TIDE_LEVELS[i]]))

func _peg_click(k: int) -> bool:
	var g: String = str(G.s.flags.get("peg_%d" % k, ""))
	if g == "":
		G.say("c2.peg_bare")
		return true
	if G.give(g):
		G.setf("peg_%d" % k, "")
		Snd.play("gear_off")
		G.say("c2.gear_removed")
	return true

func _peg_use(k: int, item: String) -> bool:
	if not GEAR_R.has(item):
		return false
	if str(G.s.flags.get("peg_%d" % k, "")) != "":
		G.say("c2.peg_taken")
		return true
	G.take(item)
	G.setf("peg_%d" % k, item)
	Snd.play("gear_on")
	G.say("c2.gear_placed")
	return true

func _crank() -> void:
	if G.f("boat_lowered"):
		G.say("c2.crank_done")
		return
	var g: Array = [str(G.s.flags.get("peg_0", "")), str(G.s.flags.get("peg_1", "")), str(G.s.flags.get("peg_2", ""))]
	if g[0] == "" or g[1] == "" or g[2] == "":
		G.say("c2.crank_spins")
		return
	# each neighbouring pair must mesh: radii add up to the peg spacing
	for pair in 2:
		var need: int = PEG_D[pair]
		var have: int = int(GEAR_R[g[pair]]) + int(GEAR_R[g[pair + 1]])
		if have < need:
			G.say("c2.gears_gap")
			Snd.play("grind")
			return
		if have > need:
			G.say("c2.gears_jam")
			Snd.play("grind")
			return
	G.setf("winch_run")
	G.setf("boat_lowered")
	G.solve("2.7")
	Snd.play("winch")
	G.say("c2.winch_turns")

func _oarlock(side: String, item: String) -> bool:
	if item != "oar" and item != "oar2":
		return false
	if G.f("oar_" + side):
		G.say("c2.oarlock_full")
		return true
	G.take(item)
	G.setf("oar_" + side, item)
	Snd.play("oarlock")
	G.say("c2.oar_placed")
	return true

func _push_off() -> void:
	var miss := ""
	if not G.f("boat_lowered"):
		miss = "cradle"
	elif not G.f("hull_ok"):
		miss = "hull"
	elif not G.f("chain_free"):
		miss = "chain"
	elif not (G.f("oar_l") and G.f("oar_r")):
		miss = "oars"
	elif not G.f("bow_lamp"):
		miss = "lamp"
	elif not G.f("got_jar"):
		miss = "jar"
	elif not G.f("got_net"):
		miss = "net"
	if miss != "":
		G.say("c2.launch_" + miss)
		return
	if G.fs("hung") != "":
		G.setf("hung", "")
		G.give("lantern_lit", true)
	G.setf("launched")
	G.solve("2.9")
	Snd.play("pushoff")
	G.say("c2.launch")
	await G.wait(0.8)
	G.chapter_done(3)
