extends Widget
## Knotted rope tiles: rotate until one rope runs from the float (left) to the weight (right).
## Tile kinds: S straight (E-W), C corner (N-E), B blank. Click a tile to turn it a quarter clockwise.

const KINDS := ["S", "C", "B", "C", "C", "C", "S", "S", "C"]
const INIT := [1, 0, 0, 1, 3, 1, 0, 1, 2]
var cell := 240
var texs := {}
var rects: Array = []
var key := "tiles_rot"

func _build() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	cell = int(args.get("cell", 240))
	var v = G.views.get("c2_net_tile", {})
	for s in v.get("sprites", []):
		texs[s.id.substr(5)] = ViewNode.tex(s.tex)       # "tile_s" -> "s"
	if not G.s.flags.has(key):
		G.s.flags[key] = INIT.duplicate()
	for i in 9:
		var tr := TextureRect.new()
		tr.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
		tr.stretch_mode = TextureRect.STRETCH_SCALE
		tr.size = Vector2(cell - 6, cell - 6)
		tr.position = Vector2((i % 3) * cell + 3, (i / 3) * cell + 3)
		tr.pivot_offset = tr.size / 2.0
		tr.mouse_filter = Control.MOUSE_FILTER_IGNORE
		add_child(tr)
		rects.append(tr)

func _gui_input(e: InputEvent) -> void:
	if not (e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT):
		return
	accept_event()
	if G.f(args.flag):
		return
	var col := int(e.position.x / cell)
	var row := int(e.position.y / cell)
	if col < 0 or col > 2 or row < 0 or row > 2:
		return
	turn(row * 3 + col)

func turn(i: int) -> void:
	var r: Array = G.s.flags[key]
	r[i] = (int(r[i]) + 1) % 4
	G.s.flags[key] = r
	Snd.play("rope")
	if connected():
		G.setf(args.flag)
		event("solved", {})
	else:
		G.changed.emit()

## directions: 0 N, 1 E, 2 S, 3 W
func dirs(i: int) -> Array:
	var r: int = int(G.s.flags[key][i])
	match KINDS[i]:
		"S":
			return [(1 + r) % 4, (3 + r) % 4]
		"C":
			return [r % 4, (1 + r) % 4]
	return []

func connected() -> bool:
	# the rope enters at the west edge of the top-left tile and must leave at the east edge of the bottom-right tile
	var cur := 0
	var entering := 3
	var seen := {}
	while true:
		if seen.has(cur * 4 + entering):
			return false
		seen[cur * 4 + entering] = true
		var d := dirs(cur)
		if not (entering in d):
			return false
		var out: int = d[1] if d[0] == entering else d[0]
		var col := cur % 3
		var row := cur / 3
		if cur == 8 and out == 1:
			return true
		match out:
			0:
				row -= 1
			1:
				col += 1
			2:
				row += 1
			3:
				col -= 1
		if col < 0 or col > 2 or row < 0 or row > 2:
			return false
		cur = row * 3 + col
		entering = (out + 2) % 4
	return false

func refresh() -> void:
	var r: Array = G.s.flags.get(key, INIT)
	for i in 9:
		var k: String = KINDS[i].to_lower()
		rects[i].texture = texs.get(k)
		rects[i].rotation_degrees = float(r[i]) * 90.0
	visible = not (G.f(args.flag) and G.f("got_net"))
