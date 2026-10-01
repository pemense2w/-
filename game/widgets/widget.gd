class_name Widget
extends Control
## Base for puzzle widgets that live inside a close-up view. State is kept in G.s.flags so saves restore it.

var view: ViewNode
var def: Dictionary
var args: Dictionary

func setup(v: ViewNode, d: Dictionary) -> void:
	view = v
	def = d
	args = d.get("args", {})
	var r: Array = d.rect
	position = Vector2(r[0], r[1])
	size = Vector2(r[2], r[3])
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	_build()
	refresh()

func _build() -> void:
	pass

func refresh() -> void:
	pass

func event(name: String, data: Dictionary = {}) -> void:
	G.widget_event(def.id, name, data)

func spr(id: String) -> Sprite2D:
	return view.get_sprite(id)

# --- shared tiny control: a pressable arrow
class Arrow extends Control:
	signal pressed
	var dir := Vector2.RIGHT
	var hover := false
	func _ready() -> void:
		mouse_filter = Control.MOUSE_FILTER_STOP
		focus_mode = Control.FOCUS_ALL
		mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
		mouse_entered.connect(func(): hover = true; queue_redraw())
		mouse_exited.connect(func(): hover = false; queue_redraw())
	func _gui_input(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT:
			pressed.emit()
			accept_event()
		elif e is InputEventKey and e.pressed and not e.echo and (e.keycode == KEY_ENTER or e.keycode == KEY_SPACE):
			pressed.emit()
			accept_event()
	func _draw() -> void:
		var c := size / 2.0
		var n := dir.normalized()
		var p := Vector2(-n.y, n.x)
		var s := minf(size.x, size.y) * 0.34
		var pts := PackedVector2Array([c + n * s, c - n * s * 0.8 + p * s, c - n * s * 0.8 - p * s])
		var col := Color(0.98, 0.9, 0.62, 0.95 if (hover or has_focus()) else 0.7)
		draw_circle(c, minf(size.x, size.y) * 0.46, Color(0.08, 0.07, 0.06, 0.55))
		draw_colored_polygon(pts, col)
		if has_focus():
			draw_arc(c, minf(size.x, size.y) * 0.46, 0, TAU, 24, Color(1, 0.95, 0.7), 3.0)
