extends SceneTree
## Shared helpers for headless playthrough tests.  Run:
##   SW_TEST=1 SW_SAVE_DIR=/tmp/sw godot --headless --path . -s tests/test_ch1.gd

var main: Node
var fails := 0
var checks := 0
# autoloads are not compile-time globals for -s scripts: bind them at runtime
var G: Node
var L: Node
var Snd: Node

func boot() -> void:
	G = root.get_node("G")
	L = root.get_node("L")
	Snd = root.get_node("Snd")
	create_timer(90.0).timeout.connect(func(): print("TIMEOUT - test did not finish"); quit(3))
	main = load("res://game/main.tscn").instantiate()
	root.add_child(main)
	await process_frame
	await process_frame

func tick(n: int = 1) -> void:
	for i in n:
		await process_frame

func check(cond: bool, msg: String) -> void:
	checks += 1
	if not cond:
		fails += 1
		print("FAIL: ", msg)

func click(h: String) -> void:
	var ok: bool = main.click_hotspot(h)
	check(ok, "hotspot '%s' not clickable in view %s" % [h, G.s.view])
	await process_frame

func use(item: String, h: String) -> void:
	check(G.has(item), "cannot use '%s' on '%s': item not in satchel" % [item, h])
	G.held = item
	var ok: bool = main.click_hotspot(h)
	check(ok, "hotspot '%s' not clickable in view %s" % [h, G.s.view])
	await process_frame

func at(view_id: String) -> void:
	G.go(view_id)
	await process_frame

func flag(name: String, msg: String = "") -> void:
	check(G.f(name), msg if msg != "" else "flag '%s' should be set (view %s)" % [name, G.s.view])

func wid(id: String) -> Control:
	var w: Control = main.widget(id)
	check(w != null, "widget '%s' missing in view %s" % [id, G.s.view])
	return w

func mouse(w: Control, local: Vector2) -> void:
	var e := InputEventMouseButton.new()
	e.button_index = MOUSE_BUTTON_LEFT
	e.pressed = true
	e.position = local
	w._gui_input(e)
	await process_frame

func shot(name: String) -> void:
	await process_frame
	await RenderingServer.frame_post_draw
	var img := root.get_viewport().get_texture().get_image()
	DirAccess.make_dir_recursive_absolute("res://tests/out")
	img.save_png("res://tests/out/%s.png" % name)

func finish() -> void:
	print("RESULT checks=%d fails=%d" % [checks, fails])
	quit(1 if fails > 0 else 0)
