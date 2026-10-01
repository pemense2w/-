class_name Chapter
extends RefCounted
## Base class for a chapter's logic. Scene art, hotspots, sprites and lights come from Blender-exported JSON;
## a chapter only decides what happens when things are clicked, used and combined.

var id := 0
var A: Dictionary = {}          # hotspot id -> {"click": Callable, "use": Callable}

func start() -> void:
	pass

func resumed() -> void:
	pass

func carry_in() -> void:
	## items the player would have carried into this chapter (used by chapter select)
	pass

func puzzles() -> Array:
	return []

func view_entered(_view: String) -> void:
	pass

func click(h: String) -> bool:
	var a = A.get(h, null)
	if a and a.has("click"):
		return a.click.call()
	return false

func use(h: String, item: String) -> bool:
	var a = A.get(h, null)
	if a and a.has("use"):
		return a.use.call(item)
	return false

func combine(_a: String, _b: String) -> bool:
	return false

## chapter-specific helpers that scene expressions may call through G (Chapter 3 uses them for fog and position)
func near(_what: String, _dir: String) -> bool:
	return false

func here(_what: String) -> bool:
	return false

func here_any() -> bool:
	return false

func widget_event(_wid: String, _ev: String, _data: Dictionary) -> void:
	pass

# ---- small helpers shared by chapter scripts
func reg(h: String, click = null, use_ = null) -> void:
	var d := {}
	if click != null:
		d["click"] = click
	if use_ != null:
		d["use"] = use_
	A[h] = d

func pickup(h: String, flag: String, item: String, text_key: String = "") -> void:
	## click to take an item lying in the world
	reg(h, func():
		if G.f(flag):
			return false
		if not G.give(item):
			return true        # satchel full: it stays where it is (G.give says so)
		G.setf(flag)
		if text_key != "":
			G.say(text_key)
		return true)

func P(id: String, avail: String, done: String, views: Array = []) -> Dictionary:
	return {"id": id, "avail": avail, "done": done, "views": views}
