class_name Sketch
extends Control
## Little pencil-and-ink drawings for notebook pages. Drawn from primitives plus the shared glyph art.

var kind := ""

func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE

const INK := Color("#2b2118")
const SHEET := Color("#e3d8b8")
const RED := Color("#b8453a")
const GREEN := Color("#4f8a5b")
const PALE := Color("#d9d3b6")
const YELLOW := Color("#dcb33c")

func _draw() -> void:
	draw_rect(Rect2(Vector2.ZERO, size), SHEET, true)
	draw_rect(Rect2(Vector2.ZERO, size), Color(0.45, 0.36, 0.2), false, 2.0)
	var c := size / 2.0
	match kind:
		"clock_fish":
			draw_arc(c, 62, 0, TAU, 40, INK, 3.0)
			for i in 12:
				var a := i * TAU / 12.0
				draw_line(c + Vector2(sin(a), -cos(a)) * 52, c + Vector2(sin(a), -cos(a)) * 60, INK, 2.0)
			# the four, with the fish beside it
			var a4 := deg_to_rad(120)
			draw_rect(Rect2(c + Vector2(sin(a4), -cos(a4)) * 40 - Vector2(10, 4), Vector2(22, 8)), Color(0, 0, 0, 0), false)
			var fp := c + Vector2(sin(a4), -cos(a4)) * 30
			draw_colored_polygon(PackedVector2Array([fp + Vector2(-9, 0), fp + Vector2(0, -5), fp + Vector2(9, 0), fp + Vector2(0, 5)]), Color("#b26a2a"))
			draw_colored_polygon(PackedVector2Array([fp + Vector2(9, 0), fp + Vector2(16, -6), fp + Vector2(16, 6)]), Color("#b26a2a"))
			draw_line(c, c + Vector2(sin(deg_to_rad(130)), -cos(deg_to_rad(130))) * 34, INK, 4.0)
			draw_line(c, c + Vector2(sin(deg_to_rad(120)), -cos(deg_to_rad(120))) * 50, INK, 2.5)
			draw_circle(c, 4, INK)
		"floats":
			var cols := [RED, GREEN, PALE, YELLOW]
			for i in 4:
				var x := 54.0 + i * 64.0
				var base := size.y - 40.0
				var pts := PackedVector2Array([Vector2(x - 20, base), Vector2(x - 15, base - 56), Vector2(x - 5, base - 78), Vector2(x + 5, base - 78), Vector2(x + 15, base - 56), Vector2(x + 20, base)])
				draw_colored_polygon(pts, cols[i])
				match i:
					0:
						for k in 4:
							draw_line(Vector2(x - 16, base - 14 - k * 11), Vector2(x + 16, base - 14 - k * 11), INK, 2.5)
					1:
						for k in 6:
							draw_circle(Vector2(x - 8 + (k % 2) * 16, base - 14 - (k / 2) * 17), 2.8, INK)
					2:
						for k in 3:
							draw_polyline(PackedVector2Array([Vector2(x - 14, base - 16 - k * 17), Vector2(x, base - 9 - k * 17), Vector2(x + 14, base - 16 - k * 17)]), INK, 2.5)
					3:
						draw_line(Vector2(x - 14, base - 24), Vector2(x + 14, base - 24), INK, 2.5)
				draw_line(Vector2(x, base - 78), Vector2(x, base - 96), INK, 3.0)
			draw_string(ThemeDB.fallback_font, Vector2(20, 26), "1  2  3  4", HORIZONTAL_ALIGNMENT_LEFT, -1, 18, INK)
		"shapes":
			var names := ["eye", "moon", "fish", "bell"]
			for i in 4:
				var tx := ViewNode.tex(_glyph_path(names[i]))
				if tx:
					draw_set_transform(Vector2(54 + i * 66, size.y * 0.62), PI, Vector2(0.3, 0.3))
					draw_texture(tx, -tx.get_size() / 2.0, Color(0.25, 0.2, 0.15))
			draw_set_transform(Vector2.ZERO, 0.0, Vector2.ONE)
			draw_line(Vector2(16, size.y * 0.45), Vector2(size.x - 16, size.y * 0.45), INK, 2.0)
		"tide":
			var rows := [["04:00", "160"], ["04:20", "172"], ["04:40", "181"]]
			for i in rows.size():
				var y := 48.0 + i * 38.0
				var col := INK
				if i == 1:
					draw_rect(Rect2(14, y - 24, size.x - 28, 34), Color(0.7, 0.5, 0.2, 0.35), true)
				draw_string(ThemeDB.fallback_font, Vector2(30, y), rows[i][0], HORIZONTAL_ALIGNMENT_LEFT, -1, 26, col)
				draw_string(ThemeDB.fallback_font, Vector2(180, y), rows[i][1], HORIZONTAL_ALIGNMENT_LEFT, -1, 26, col)
		"bell":
			var x := 30.0
			for p in [2, 1, 1, 2]:
				if p == 2:
					draw_rect(Rect2(x, size.y / 2 - 8, 60, 16), INK, true)
					x += 76
				else:
					draw_circle(Vector2(x + 10, size.y / 2), 10, INK)
					x += 38
		"valves":
			for i in 3:
				var cc := Vector2(60 + i * 90, size.y / 2)
				draw_arc(cc, 30, 0, TAU, 28, INK, 3.0)
				draw_line(cc, cc + Vector2(0, -26).rotated(deg_to_rad([90.0, 30.0, 120.0][i])), INK, 3.0)
				draw_string(ThemeDB.fallback_font, cc + Vector2(-8, 62), ["3", "1", "4"][i], HORIZONTAL_ALIGNMENT_LEFT, -1, 26, INK)
		"mirror":
			draw_line(Vector2(size.x / 2, 20), Vector2(size.x / 2, size.y - 20), INK, 3.0)
			draw_line(Vector2(60, 70), Vector2(size.x / 2 - 20, 70), INK, 4.0)
			draw_colored_polygon(PackedVector2Array([Vector2(size.x / 2 - 20, 58), Vector2(size.x / 2 - 4, 70), Vector2(size.x / 2 - 20, 82)]), INK)
			draw_line(Vector2(size.x - 60, 120), Vector2(size.x / 2 + 20, 120), INK, 4.0)
			draw_colored_polygon(PackedVector2Array([Vector2(size.x / 2 + 20, 108), Vector2(size.x / 2 + 4, 120), Vector2(size.x / 2 + 20, 132)]), INK)
		"chart":
			for i in 6:
				draw_line(Vector2(40 + i * 40, 24), Vector2(40 + i * 40, 150), INK, 1.5)
				draw_line(Vector2(40, 24 + i * 25), Vector2(240, 24 + i * 25), INK, 1.5)
			draw_arc(Vector2(160, 74), 14, 0, TAU, 20, RED, 3.0)
		_:
			draw_string(ThemeDB.fallback_font, Vector2(20, 40), "~", HORIZONTAL_ALIGNMENT_LEFT, -1, 28, INK)

func _glyph_path(nm: String) -> String:
	var v = G.views.get("ui_glyphs", {})
	for s in v.get("sprites", []):
		if s.id == "glyph_" + nm:
			return s.tex
	return ""
