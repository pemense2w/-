extends Widget
## Swap the standing books until they stand in the painting's order.  Click one, then another, to swap them.
## args.sprites: sprite ids in solved order; args.slots: x position of each slot.

var order: Array = []
var picked := -1
var key := "books_order"

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	key = args.get("key", "books_order")
	if not G.s.flags.has(key):
		G.s.flags[key] = args.get("init", [2, 0, 3, 1])
	for sid in args.sprites:
		pass

func _slot_at(x: float) -> int:
	var slots: Array = args.slots
	var best := 0
	var bd := 1e9
	for i in slots.size():
		var d := absf(x - (slots[i] + 70))
		if d < bd:
			bd = d
			best = i
	return best

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	if G.f(args.get("solved_flag", "books_sorted")):
		G.say("books.locked")
		return
	var slot := _slot_at(e.position.x + position.x)
	accept_event()
	if picked < 0:
		picked = slot
		Snd.play("tap")
	elif picked == slot:
		picked = -1
	else:
		var o: Array = G.s.flags[key]
		var tmp = o[picked]
		o[picked] = o[slot]
		o[slot] = tmp
		G.s.flags[key] = o
		picked = -1
		Snd.play("book")
		event("changed", {"order": o})
		if _solved():
			G.setf(args.get("solved_flag", "books_sorted"))
			event("solved", {})
	refresh()

func _solved() -> bool:
	var o: Array = G.s.flags[key]
	for i in o.size():
		if int(o[i]) != i:
			return false
	return true

func refresh() -> void:
	var o: Array = G.s.flags.get(key, [])
	var slots: Array = args.slots
	var ids: Array = args.sprites
	if o.size() != ids.size():
		return
	# o[slot] = which book (home index) stands in that slot
	for slot in o.size():
		var home: int = int(o[slot])
		var n: Sprite2D = spr(ids[home])
		if n == null:
			continue
		var base: Vector2 = view.spr[ids[home]].base
		n.position.x = base.x + (slots[slot] - slots[home])
		n.position.y = base.y - (26 if picked == slot else 0)
