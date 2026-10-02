class_name StageScripts
extends RefCounted
## The five memories and three endings as short scripts for StagePlayer.  Coordinates are in the 1600x1000 stage;
## sprites are anchored at their feet (bottom centre).  Captions are string keys.

static func _p(t: float, id: String, spr: String, x: float, y: float, s: float = 1.0, extra: Dictionary = {}) -> Dictionary:
	var d := {"t": t, "a": "put", "id": id, "spr": spr, "x": x, "y": y, "s": s}
	d.merge(extra, true)
	return d

static func _mv(t: float, id: String, x: float, y: float, dur: float) -> Dictionary:
	return {"t": t, "a": "move", "id": id, "x": x, "y": y, "dur": dur}

static func _cap(t: float, key: String, dur: float = 4.5) -> Dictionary:
	return {"t": t, "a": "cap", "key": key, "dur": dur}

static func _do(t: float, a: String, extra: Dictionary = {}) -> Dictionary:
	var d := {"t": t, "a": a}
	d.merge(extra, true)
	return d

static func total_time(sc: Array) -> float:
	var m := 0.0
	for e in sc:
		m = maxf(m, float(e.t))
	return m

static func memory(n: int) -> Array:
	match n:
		1: return _m1()
		2: return _m2()
		3: return _m3()
		4: return _m4()
		5: return _m5()
	return []

static func ending_bg(kind: String) -> String:
	match kind:
		"A":
			return "end_dawn"
		"B":
			return "end_two_lights"
		"C":
			return "end_two_lights"
	return "mem_wall"

# ---------------------------------------------------------------- memories
static func _m1() -> Array:
	## 1 - The Quarrel: Tomas says he is leaving the lake for good and asks Ruth to come.  She refuses.
	return [
		_p(0.0, "table", "table_lamp", 430, 905, 1.0),
		_p(0.0, "ruth", "ruth_sit", 560, 905, 0.9, {"alpha": 1.0}),
		_p(0.0, "door", "door", 1430, 905, 0.95),
		_p(0.0, "tomas", "tomas", 1180, 905, 1.0, {"flip": true}),
		_do(0.0, "tint", {"color": "#00000000", "dur": 0.1}),
		_cap(0.8, "mem1.1", 5.0),
		_mv(5.0, "tomas", 900, 905, 3.0),
		_cap(7.5, "mem1.2", 5.0),
		_do(13.0, "rot", {"id": "ruth", "deg": -3.0, "dur": 0.5}),
		_do(13.6, "rot", {"id": "ruth", "deg": 1.0, "dur": 0.8}),
		_cap(13.0, "mem1.3", 5.0),
		_cap(18.5, "mem1.4", 4.5),
		_do(20.0, "shake", {}),
		_cap(23.5, "mem1.5", 5.0),
		_do(29.0, "flip", {"id": "tomas"}),
		_mv(29.5, "tomas", 1430, 905, 3.5),
		_do(33.0, "fade", {"id": "tomas", "alpha": 0.0, "dur": 1.2}),
		_do(33.2, "tint", {"color": "#20120a88", "dur": 1.0}),
		_cap(34.0, "mem1.6", 5.0),
		_do(40.0, "end"),
	]

static func _m2() -> Array:
	## 2 - Lessons: Tomas teaching Ruth to row, on a golden afternoon.
	var bob := {"bob": {"amp": 7.0, "speed": 1.5}}
	return [
		_p(0.0, "wave", "wave", 800, 945, 1.0),
		_p(0.0, "boat", "boat", 520, 835, 0.9, bob),
		_p(0.0, "ruth", "ruth", 470, 770, 0.5, bob),
		_p(0.0, "tomas", "tomas", 600, 770, 0.62, bob),
		_p(0.0, "oar_l", "oar", 380, 790, 0.9, bob),
		_p(0.0, "oar_r", "oar", 700, 790, 0.9, {"flip": true, "bob": {"amp": 7.0, "speed": 1.5}}),
		_do(0.5, "sway", {"id": "oar_l", "deg": 8.0, "dur": 1.4, "loops": 14}),
		_do(0.5, "sway", {"id": "oar_r", "deg": 8.0, "dur": 1.4, "loops": 14}),
		_mv(0.0, "boat", 1050, 835, 30.0),
		_mv(0.0, "ruth", 1000, 770, 30.0),
		_mv(0.0, "tomas", 1130, 770, 30.0),
		_mv(0.0, "oar_l", 910, 790, 30.0),
		_mv(0.0, "oar_r", 1230, 790, 30.0),
		_cap(0.8, "mem2.1", 5.0),
		_cap(6.0, "mem2.2", 4.5),
		_cap(11.0, "mem2.3", 4.5),
		_cap(16.5, "mem2.4", 5.0),
		_cap(22.5, "mem2.5", 5.0),
		_cap(28.0, "mem2.6", 5.0),
		_do(35.0, "end"),
	]

static func _m3() -> Array:
	## 3 - The Storm: Tomas steering for a light that isn't there.
	return [
		_do(0.0, "tint", {"color": "#0a1830aa", "dur": 0.1}),
		_p(0.0, "lh", "lighthouse", 1390, 960, 0.9),
		_p(0.0, "cloud", "cloud", 600, 360, 1.5),
		_p(0.0, "rain", "rain", 800, 960, 1.0),
		_p(0.0, "wave", "wave_big", 800, 975, 1.05),
		_p(0.0, "boat", "boat", 600, 830, 0.9, {"bob": {"amp": 12.0, "speed": 1.8}}),
		_p(0.0, "tomas", "tomas_lean", 520, 740, 0.7, {"bob": {"amp": 12.0, "speed": 1.8}}),
		_do(0.5, "sway", {"id": "boat", "deg": 7.0, "dur": 1.8, "loops": 20}),
		_cap(0.8, "mem3.1", 5.5),
		_do(4.0, "flash", {}),
		_p(4.0, "bolt1", "bolt", 880, 300, 1.4),
		_do(4.5, "del", {"id": "bolt1"}),
		_cap(7.0, "mem3.2", 4.5),
		_mv(0.0, "boat", 1000, 830, 24.0),
		_mv(0.0, "tomas", 920, 740, 24.0),
		_do(12.0, "flash", {}),
		_p(12.0, "bolt2", "bolt", 1230, 340, 1.2),
		_do(12.5, "del", {"id": "bolt2"}),
		_cap(12.0, "mem3.3", 5.0),
		_cap(17.5, "mem3.4", 5.0),
		_do(22.0, "shake", {}),
		_do(24.0, "nobob", {"id": "boat"}),
		_do(24.0, "nobob", {"id": "tomas"}),
		_do(24.0, "rot", {"id": "boat", "deg": 36.0, "dur": 3.0}),
		_mv(24.0, "boat", 1050, 1100, 4.0),
		_mv(24.0, "tomas", 960, 1010, 4.0),
		_do(24.0, "flash", {}),
		_cap(26.0, "mem3.5", 5.0),
		_do(33.0, "end"),
	]

static func _m4() -> Array:
	## 4 - Half Past Four: Ruth waking to see the ferry go under.
	return [
		_do(0.0, "tint", {"color": "#2a180c33", "dur": 0.1}),
		_p(0.0, "window", "window", 1130, 860, 1.4),
		_p(0.0, "rain", "rain", 800, 960, 1.0),
		_p(0.0, "ferry", "ferry", 1260, 640, 0.35),
		_p(0.0, "desk", "desk", 480, 905, 1.2),
		_p(0.0, "lamp", "table_lamp", 420, 800, 0.7),
		_p(0.0, "ruth", "ruth_sit", 620, 905, 1.0),
		_p(0.0, "clock", "clock_small", 260, 540, 1.0),
		_cap(0.8, "mem4.1", 5.0),
		_do(6.0, "rot", {"id": "ruth", "deg": 7.0, "dur": 3.0}),
		_cap(6.0, "mem4.2", 4.5),
		_do(11.0, "tint", {"color": "#050302dd", "dur": 0.4}),
		_do(11.0, "snd", {"name": "watch_tick"}),
		_cap(11.0, "mem4.3", 5.0),
		_do(16.5, "tint", {"color": "#2a180c44", "dur": 1.2}),
		_do(16.5, "rot", {"id": "ruth", "deg": 0.0, "dur": 1.2}),
		_cap(17.0, "mem4.4", 5.5),
		_mv(18.0, "ferry", 1280, 700, 5.0),
		_do(18.0, "rot", {"id": "ferry", "deg": 22.0, "dur": 5.0}),
		_do(23.0, "fade", {"id": "ferry", "alpha": 0.0, "dur": 2.5}),
		_cap(24.0, "mem4.5", 5.0),
		_do(31.0, "end"),
	]

static func _m5() -> Array:
	## 5 - Still Water: Ruth at the jetty, every night since.
	return [
		_do(0.0, "tint", {"color": "#0a1a3a77", "dur": 0.1}),
		_p(0.0, "wave", "wave", 800, 960, 1.0),
		_p(0.0, "jetty", "jetty", 800, 1000, 1.0),
		_p(0.0, "moon", "moon", 1300, 330, 1.0),
		_p(0.0, "ruth", "ruth_lantern", 1060, 905, 1.0),
		_cap(0.8, "mem5.1", 5.0),
		_do(6.0, "fade", {"id": "moon", "alpha": 0.0, "dur": 1.2}),
		_p(7.0, "moon2", "moon_crescent", 1300, 400, 1.0, {"alpha": 0.0}),
		_do(7.2, "fade", {"id": "moon2", "alpha": 1.0, "dur": 1.2}),
		_cap(7.0, "mem5.2", 5.0),
		_do(13.0, "fade", {"id": "moon2", "alpha": 0.0, "dur": 1.0}),
		_p(14.0, "moon3", "moon", 1300, 330, 1.0, {"alpha": 0.0}),
		_do(14.2, "fade", {"id": "moon3", "alpha": 1.0, "dur": 1.0}),
		_cap(14.0, "mem5.3", 5.0),
		_do(20.0, "fade", {"id": "moon3", "alpha": 0.0, "dur": 1.0}),
		_p(20.0, "moth", "moth", 1080, 740, 0.9, {"bob": {"amp": 14.0, "speed": 2.2}}),
		_cap(21.0, "mem5.4", 5.0),
		_cap(27.0, "mem5.5", 5.0),
		_do(33.0, "end"),
	]

# ------------------------------------------------------------------ endings
static func ending(kind: String) -> Array:
	match kind:
		"A":
			return [
				_do(0.0, "tint", {"color": "#0a1424cc", "dur": 0.1}),
				_p(0.0, "moth", "moth_last", 520, 880, 1.2, {"sheet": "c5_chair", "alpha": 1.0}),
				_cap(0.8, "end.A.1", 5.0),
				_mv(3.0, "moth", 1310, 470, 9.0),
				_do(11.5, "fade", {"id": "moth", "alpha": 0.0, "dur": 1.5}),
				_do(11.0, "tint", {"color": "#0a142400", "dur": 7.0}),
				_cap(10.0, "end.A.2", 5.0),
				_do(14.0, "ripple", {"amp": 1.0, "dur": 6.0}),
				_do(14.0, "snd", {"name": "ripple"}),
				_cap(15.0, "end.A.3", 5.5),
				_do(23.0, "bg", {"view": "end_jetty", "dur": 2.5}),
				_p(24.0, "ferry", "ferry_end", 2200, 770, 1.0, {"sheet": "end_jetty"}),
				_mv(24.5, "ferry", 1200, 770, 8.0),
				_do(25.0, "snd", {"name": "ferry_horn"}),
				_cap(25.0, "end.A.4", 5.5),
				_p(34.0, "ticket", "ticket_ok", 800, 700, 1.4, {"img": "items/item_ticket_ok__icon.webp", "alpha": 0.0}),
				_do(34.0, "fade", {"id": "ticket", "alpha": 1.0, "dur": 1.5}),
				_cap(34.5, "end.A.5", 5.0),
				_do(41.0, "title", {"key": "end.A.title", "dur": 3.5}),
				_do(48.0, "end"),
			]
		"B":
			return [
				_do(0.0, "tint", {"color": "#050a14e8", "dur": 0.1}),
				_p(0.0, "moth", "moth_last", 800, 640, 1.4, {"sheet": "c5_chair", "alpha": 0.0}),
				_do(0.5, "fade", {"id": "moth", "alpha": 1.0, "dur": 2.0}),
				_cap(1.0, "end.B.1", 5.0),
				_do(8.0, "fade", {"id": "moth", "alpha": 0.0, "dur": 1.5}),
				_do(9.0, "bg", {"view": "c1_n", "dur": 2.5}),
				_do(9.0, "tint", {"color": "#0a141ca0", "dur": 3.0}),
				_cap(10.0, "end.B.2", 5.0),
				_do(17.0, "bg", {"view": "c1_mirror", "dur": 2.0}),
				_cap(18.0, "end.B.3", 5.5),
				_p(21.0, "refl", "refl", 800, 900, 1.0, {"sheet": "c1_mirror", "alpha": 0.0}),
				_do(22.5, "fade", {"id": "refl", "alpha": 1.0, "dur": 1.2}),
				_cap(24.5, "end.B.4", 5.0),
				_do(31.0, "title", {"key": "end.B.title", "dur": 3.0}),
				_do(37.0, "end"),
			]
		"C":
			return [
				_do(0.0, "tint", {"color": "#050a14aa", "dur": 0.1}),
				_cap(0.8, "end.C.1", 5.0),
				_do(1.0, "snd", {"name": "bell"}),
				_do(5.0, "photo", {"dur": 7.0}),
				_cap(6.0, "end.C.2", 6.0),
				_do(15.0, "snd", {"name": "bell_far"}),
				_cap(15.0, "end.C.3", 5.0),
				_do(19.0, "tint", {"color": "#050a1400", "dur": 4.0}),
				_p(20.0, "light", "second_light", 1000, 760, 1.0, {"sheet": "end_two_lights", "alpha": 0.0}),
				_do(20.0, "fade", {"id": "light", "alpha": 1.0, "dur": 2.0}),
				_do(20.0, "photo_clear", {}),
				_mv(21.0, "light", 440, 840, 17.0),
				_cap(22.0, "end.C.4", 6.0),
				_cap(30.0, "end.C.5", 6.0),
				_do(39.0, "title", {"key": "end.C.title", "dur": 3.5}),
				_do(46.0, "end"),
			]
	return []
