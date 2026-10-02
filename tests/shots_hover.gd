extends "res://tests/test_base.gd"
## Hover over a hotspot with the glow off and on (needs a display / xvfb-run).
func _initialize() -> void:
	_run()
func _run() -> void:
	await boot()
	G.new_game(); await tick(3)
	await at("c1_drawer"); await tick(3)
	var h = main.view.get_hotspot("drawer_inner")
	for glow in [false, true]:
		G.settings.hotspot_glow = glow
		var e := InputEventMouseMotion.new()
		e.position = h.position + h.size / 2.0
		e.global_position = e.position
		root.get_viewport().push_input(e)
		h.hover = true; h.queue_redraw()
		await tick(3)
		await shot("hover_glow_%s" % str(glow))
	await at("c1_n"); await tick(2)
	G.settings.text_scale = 1.5
	main.open_settings(); await tick(3); await shot("settings_scroll")
	finish()
