extends Node
## Still Water - the single state object, save/load, and the glue between scene data and chapter logic.
## All state is one Dictionary (`s`) saved as JSON after every action; settings and profile are separate files.

signal view_changed(id: String)
signal changed
signal said(text: String)
signal sfx_caption(text: String)
signal item_gained(id: String)
signal note_added(id: String)
signal fragment_added(n: int)
signal memory_requested(n: int)
signal memory_done
signal ending_requested(kind: String)
signal chapter_card(n: int)
signal inspect_requested(item: String)
signal hint_shown(text: String, tier: int)
signal settings_changed
signal request_title
signal puzzle_solved(pid: String)
signal fx(name: String, data: Dictionary)

const SAVE_VERSION := 1
const SCENE_W := 1600
const SCENE_H := 1000
const HINT_WAIT := 45.0
const SATCHEL_SLOTS := 8
const CHAPTER_SCRIPTS := [
	"res://game/chapters/ch1.gd", "res://game/chapters/ch2.gd", "res://game/chapters/ch3.gd",
	"res://game/chapters/ch4.gd", "res://game/chapters/ch5.gd",
]

var views: Dictionary = {}
var items_meta: Dictionary = {}
var notebook_defs: Array = []
var s: Dictionary = {}
var settings: Dictionary = {}
var profile: Dictionary = {}
var chapter = null            # Chapter instance
var held: String = ""         # selected satchel item
var busy := false             # input locked during sequences
var in_game := false
var test_mode := false        # headless tests: no waiting, no tweens
var _expr_cache := {}
var _save_dir := "user://"

func _ready() -> void:
	var envdir := OS.get_environment("SW_SAVE_DIR")
	if envdir != "":
		_save_dir = envdir.rstrip("/") + "/"
		DirAccess.make_dir_recursive_absolute(_save_dir)
	test_mode = OS.get_environment("SW_TEST") != ""
	views = _read_json("res://assets/data/views.json", {})
	items_meta = _read_json("res://assets/data/items.json", {})
	notebook_defs = _read_json("res://assets/data/notebook.json", [])
	_load_settings()
	_load_profile()
	L.set_language(settings.lang)

func _process(delta: float) -> void:
	if in_game and not busy and not s.is_empty():
		s.stats.play_time = float(s.stats.play_time) + delta

# ------------------------------------------------------------------ files
func _read_json(path: String, fallback):
	if not FileAccess.file_exists(path):
		return fallback
	var fa := FileAccess.open(path, FileAccess.READ)
	var d = JSON.parse_string(fa.get_as_text())
	return d if d != null else fallback

func _write_json(path: String, data) -> void:
	var fa := FileAccess.open(path, FileAccess.WRITE)
	if fa:
		fa.store_string(JSON.stringify(data))

func _default_settings() -> Dictionary:
	return {
		"lang": L.system_default_language(), "vol_amb": 0.8, "vol_sfx": 0.9, "vol_music": 0.7,
		"text_scale": 1.0, "plain_font": false, "reduce_motion": false, "startle": true,
		"no_timing": false, "purist": false, "captions": true, "telemetry": false,
	}

func _load_settings() -> void:
	settings = _default_settings()
	var d = _read_json(_save_dir + "settings.json", {})
	for k in d:
		settings[k] = d[k]

func save_settings() -> void:
	_write_json(_save_dir + "settings.json", settings)
	settings_changed.emit()

func set_setting(k: String, v) -> void:
	settings[k] = v
	if k == "lang":
		L.set_language(v)
	save_settings()

func _load_profile() -> void:
	profile = {"finished": false, "endings": [], "memories": [], "frags": [], "unlocked": 1}
	var d = _read_json(_save_dir + "profile.json", {})
	for k in d:
		profile[k] = d[k]

func save_profile() -> void:
	_write_json(_save_dir + "profile.json", profile)

func has_save() -> bool:
	return FileAccess.file_exists(_save_dir + "save.json")

func save() -> void:
	if s.is_empty():
		return
	s.v = SAVE_VERSION
	_write_json(_save_dir + "save.json", s)

func _fresh_state() -> Dictionary:
	return {
		"v": SAVE_VERSION, "chapter": 1, "view": "", "items": [], "flags": {}, "notes": [], "frags": [],
		"hints": {}, "stats": {"play_time": 0.0, "hints": 0, "failed": {}, "solved": {}, "chapter_time": {}},
	}

func _migrate(d: Dictionary) -> Dictionary:
	# saves carry a version number so updates never break a run in progress
	var base := _fresh_state()
	for k in base:
		if not d.has(k):
			d[k] = base[k]
	d.v = SAVE_VERSION
	return d

# --------------------------------------------------------------- lifecycle
func new_game() -> void:
	s = _fresh_state()
	in_game = true
	held = ""
	start_chapter(1)

func continue_game() -> bool:
	var d = _read_json(_save_dir + "save.json", null)
	if d == null or not (d is Dictionary):
		return false
	s = _migrate(d)
	in_game = true
	held = ""
	_load_chapter(int(s.chapter))
	if s.view == "" or not views.has(s.view):
		chapter.start()
	else:
		view_changed.emit(s.view)
		chapter.resumed()
	changed.emit()
	return true

var _retired: Array = []

func _load_chapter(n: int) -> void:
	s.chapter = n
	# a chapter may call chapter_done() from inside its own method: keep the old instance alive a while
	if chapter != null:
		_retired.append(chapter)
		if _retired.size() > 4:
			_retired.pop_front()
	var scr = load(CHAPTER_SCRIPTS[n - 1])
	chapter = scr.new()

func start_chapter(n: int, carry: bool = false) -> void:
	_load_chapter(n)
	if carry:
		chapter.carry_in()
	s.stats.chapter_time[str(n)] = s.stats.play_time
	if n > int(profile.unlocked):
		profile.unlocked = n
		save_profile()
	chapter_card.emit(n)
	chapter.start()
	log_event("chapter_start", {"chapter": n})
	save()
	changed.emit()

func select_chapter(n: int) -> void:
	# chapter select (after the first finish): fresh run state for that chapter, keeping nothing else
	s = _fresh_state()
	in_game = true
	held = ""
	start_chapter(n, true)

func quit_to_title() -> void:
	save()
	in_game = false
	request_title.emit()

# ------------------------------------------------------------- expressions
func ev(expr: String):
	if expr == "" or expr == null:
		return true
	var e = _expr_cache.get(expr, null)
	if e == null:
		e = Expression.new()
		if e.parse(expr) != OK:
			push_error("bad expression: %s (%s)" % [expr, e.get_error_text()])
			_expr_cache[expr] = false
			return false
		_expr_cache[expr] = e
	if e is bool:
		return false
	var r = e.execute([], self, false)
	if e.has_execute_failed():
		push_error("expression failed: %s" % expr)
		return false
	return r

func evb(expr) -> bool:
	if expr == null:
		return true
	return bool(ev(str(expr)))

func evf(expr, fallback: float = 0.0) -> float:
	if expr == null:
		return fallback
	var r = ev(str(expr))
	return float(r) if (r is float or r is int) else fallback

# ------------------------------------------------------------------- flags
func f(name: String):
	if s.is_empty():
		return false
	return s.flags.get(name, false)

func fi(name: String) -> int:
	if s.is_empty():
		return 0
	var v = s.flags.get(name, 0)
	return int(v) if (v is float or v is int) else 0

func setf(name: String, v = true) -> void:
	s.flags[name] = v
	changed.emit()

func inc(name: String, by: int = 1) -> int:
	var n := fi(name) + by
	s.flags[name] = n
	changed.emit()
	return n

func has(item: String) -> bool:
	return not s.is_empty() and item in s.items

func era() -> String:
	return str(s.flags.get("era", "now"))

func give(item: String, silent: bool = false) -> bool:
	if item in s.items:
		return true
	if s.items.size() >= SATCHEL_SLOTS:
		say("satchel.full")
		return false
	s.items.append(item)
	if not silent:
		item_gained.emit(item)
		Snd.play("take")
	changed.emit()
	return true

func take(item: String) -> void:
	s.items.erase(item)
	if held == item:
		held = ""
	changed.emit()

func replace_item(old: String, new_item: String) -> void:
	var i: int = s.items.find(old)
	if i >= 0:
		s.items[i] = new_item
	else:
		give(new_item, true)
	if held == old:
		held = ""
	item_gained.emit(new_item)
	changed.emit()

func select_item(item: String) -> void:
	held = "" if held == item else item
	changed.emit()

func item_name(item: String) -> String:
	return L.t("item.%s.name" % item)

# ----------------------------------------------------------------- captions
func say(key: String, args: Array = []) -> void:
	said.emit(L.t(key, args))

func say_text(text: String) -> void:
	said.emit(text)

func sfx_cap(key: String) -> void:
	if settings.captions and L.has_key(key):
		sfx_caption.emit(L.t(key))

# --------------------------------------------------------------- navigation
func go(view_id: String) -> void:
	if not views.has(view_id):
		push_error("unknown view: " + view_id)
		return
	s.view = view_id
	held = held  # selection persists across views (use an item anywhere)
	view_changed.emit(view_id)
	if chapter:
		chapter.view_entered(view_id)
	log_event("view_change", {"view": view_id})
	save()
	changed.emit()

func current_view() -> Dictionary:
	return views.get(s.view, {})

func turn(dir: int) -> void:
	var nav = current_view().get("nav", {})
	var target = nav.get("left" if dir < 0 else "right", null)
	if target:
		Snd.play("turn")
		go(target)

func back() -> void:
	var nav = current_view().get("nav", {})
	var target = nav.get("back", null)
	if target:
		Snd.play("back")
		go(target)

# ------------------------------------------------------------- interaction
func activate(hid: String) -> void:
	if busy or s.is_empty():
		return
	if held != "":
		var it := held
		var ok: bool = chapter.use(hid, it)
		if not ok:
			_failed_use(hid, it)
		else:
			held = ""
	else:
		var handled: bool = chapter.click(hid)
		if not handled:
			_look(hid)
	save()
	changed.emit()

func _look(hid: String) -> void:
	for key in ["look.%s" % hid, "look.generic"]:
		if L.has_key(key):
			if key == "look.generic":
				say_text(L.pick("look.generic"))
			else:
				say(key)
			return

func _failed_use(hid: String, it: String) -> void:
	var k := "%s>%s" % [it, hid]
	s.stats.failed[k] = int(s.stats.failed.get(k, 0)) + 1
	log_event("item_use_failed", {"item": it, "target": hid})
	Snd.play("wrong")
	for key in ["use.%s.%s" % [hid, it], "use.%s" % hid, "use.item.%s" % it]:
		if L.has_key(key):
			say(key)
			return
	say_text(L.pick("use.generic"))

## combine two satchel items (drop one on another)
func combine(a: String, b: String) -> void:
	if busy:
		return
	var ok: bool = chapter.combine(a, b)
	if not ok:
		for key in ["combine.%s.%s" % [a, b], "combine.%s.%s" % [b, a]]:
			if L.has_key(key):
				say(key)
				Snd.play("wrong")
				return
		Snd.play("wrong")
		say_text(L.pick("combine.generic"))
	held = ""
	save()
	changed.emit()

func click_item(item: String) -> void:
	if busy:
		return
	if held != "" and held != item:
		combine(held, item)
	else:
		select_item(item)

func inspect_item(item: String) -> void:
	inspect_requested.emit(item)

func widget_event(wid: String, ev_name: String, data: Dictionary = {}) -> void:
	chapter.widget_event(wid, ev_name, data)
	save()
	changed.emit()

# ---------------------------------------------------------------- progress
func note(id: String) -> void:
	if settings.purist or id in s.notes:
		return
	s.notes.append(id)
	note_added.emit(id)
	changed.emit()

func solve(pid: String) -> void:
	if s.stats.solved.has(pid):
		return
	s.stats.solved[pid] = s.stats.play_time
	Snd.play("solve")
	log_event("puzzle_solve", {"puzzle": pid, "t": s.stats.play_time})
	puzzle_solved.emit(pid)

func add_fragment(n: int) -> void:
	if not (n in s.frags):
		s.frags.append(n)
	if not (n in profile.frags):
		profile.frags.append(n)
		save_profile()
	Snd.play("fragment")
	fragment_added.emit(n)
	say("frag.get", [profile.frags.size()])
	changed.emit()

func fragment_count() -> int:
	return profile.frags.size()

func play_memory(n: int) -> void:
	busy = true
	if not (n in profile.memories):
		profile.memories.append(n)
		save_profile()
	memory_requested.emit(n)
	if test_mode:
		busy = false
		return
	await memory_done
	busy = false

func chapter_done(next: int) -> void:
	log_event("chapter_complete", {"chapter": next - 1, "t": s.stats.play_time})
	start_chapter(next)

func finish_game(kind: String) -> void:
	profile.finished = true
	if not (kind in profile.endings):
		profile.endings.append(kind)
	save_profile()
	ending_requested.emit(kind)

func wait(sec: float) -> void:
	if test_mode:
		return
	await get_tree().create_timer(sec).timeout

# ------------------------------------------------------------------- hints
## Returns {"text", "tier", "wait", "pid", "speaker"}; the chapter's puzzle list decides the current puzzle.
func current_puzzle() -> Dictionary:
	if chapter == null:
		return {}
	var open: Array = []
	for p in chapter.puzzles():
		if evb(p.get("avail", "true")) and not evb(p.get("done", "false")):
			open.append(p)
	if open.is_empty():
		return {}
	# prefer the puzzle whose clue or lock is in the view the player is looking at
	for p in open:
		if s.view in p.get("views", []):
			return p
	return open[0]

func request_hint() -> Dictionary:
	var p := current_puzzle()
	if p.is_empty():
		return {"text": L.t("hint.none"), "tier": 0, "wait": 0.0, "pid": "", "speaker": "pell"}
	var pid: String = p.id
	var h: Dictionary = s.hints.get(pid, {"tier": 0, "t": 0.0})
	var now := Time.get_ticks_msec() / 1000.0
	var wait_left := 0.0
	if int(h.tier) == 0:
		h.tier = 1
		h.t = now
		s.stats.hints = int(s.stats.hints) + 1
		log_event("hint_shown", {"puzzle": pid, "tier": 1})
	elif int(h.tier) < 3:
		wait_left = HINT_WAIT - (now - float(h.t))
		if wait_left <= 0.0 or test_mode:
			h.tier = int(h.tier) + 1
			h.t = now
			wait_left = 0.0
			s.stats.hints = int(s.stats.hints) + 1
			log_event("hint_shown", {"puzzle": pid, "tier": h.tier})
	s.hints[pid] = h
	var tier := int(h.tier)
	var pre: bool = not f("fed")
	var key := "hint.%s.%d" % [pid, tier]
	if pre and L.has_key("hintr.%s.%d" % [pid, tier]):
		key = "hintr.%s.%d" % [pid, tier]
	var text := L.t(key)
	if wait_left > 0.0 and tier < 3:
		text += "\n\n" + L.t("hint.more", [int(ceil(wait_left))])
	save()
	return {"text": text, "tier": tier, "wait": wait_left, "pid": pid, "speaker": "r" if (pre and chapter.id == 1) else "pell"}

# --------------------------------------------------------------- telemetry
func log_event(name: String, data: Dictionary = {}) -> void:
	if not settings.telemetry:
		return
	var fa := FileAccess.open(_save_dir + "telemetry.jsonl", FileAccess.READ_WRITE)
	if fa == null:
		fa = FileAccess.open(_save_dir + "telemetry.jsonl", FileAccess.WRITE)
	fa.seek_end()
	data["e"] = name
	data["t"] = Time.get_unix_time_from_system()
	fa.store_line(JSON.stringify(data))
