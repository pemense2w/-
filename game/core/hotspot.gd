class_name Hotspot
extends Control
## An interactive area. Reacts on hover, focus (keyboard) and tap; never a dead click.

signal activated(hid: String)

var hid := ""
var hover := false
var flash := 0.0
var show_all := 0.0

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_STOP
	focus_mode = Control.FOCUS_ALL
	mouse_default_cursor_shape = Control.CURSOR_POINTING_HAND
	mouse_entered.connect(func(): hover = true; queue_redraw())
	mouse_exited.connect(func(): hover = false; queue_redraw())
	focus_entered.connect(queue_redraw)
	focus_exited.connect(queue_redraw)

func _gui_input(e: InputEvent) -> void:
	if e is InputEventMouseButton and e.pressed and e.button_index == MOUSE_BUTTON_LEFT:
		_fire()
		accept_event()
	elif e is InputEventKey and e.pressed and not e.echo and (e.keycode == KEY_ENTER or e.keycode == KEY_KP_ENTER or e.keycode == KEY_SPACE):
		_fire()
		accept_event()

func _fire() -> void:
	flash = 1.0
	set_process(true)
	activated.emit(hid)

func ping(sec: float = 1.2) -> void:
	show_all = sec
	set_process(true)
	queue_redraw()

func _process(delta: float) -> void:
	flash = maxf(0.0, flash - delta * 3.0)
	show_all = maxf(0.0, show_all - delta)
	queue_redraw()
	if flash <= 0.0 and show_all <= 0.0:
		set_process(false)

func _draw() -> void:
	var a := 0.0
	if hover:
		a = 0.55
	if has_focus():
		a = 0.9
	a = maxf(a, flash)
	a = maxf(a, clampf(show_all, 0.0, 1.0) * 0.6)
	if a <= 0.0:
		return
	var r := Rect2(Vector2.ZERO, size).grow(-3)
	var col := Color(1.0, 0.93, 0.72, 0.16 * a + 0.2 * flash)
	draw_rect(r, col, true)
	var oc := Color(1.0, 0.94, 0.75, a)
	var w := 3.0 if has_focus() else 2.0
	draw_rect(r, oc, false, w)
