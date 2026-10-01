class_name UI
extends RefCounted
## Tiny UI toolkit: paper-and-ink styling shared by every panel.

const INK := Color("#12181a")
const PANEL := Color("#1a2326")
const PANEL_HI := Color("#26343a")
const EDGE := Color("#c9a24d")
const TEXT := Color("#eadfc4")
const DIM := Color("#9b9481")
const WARM := Color("#f4b95e")
const RED := Color("#c9553f")

static func fs(base: int) -> int:
	return int(round(base * float(G.settings.get("text_scale", 1.0))))

static func box(bg: Color, edge: Color = Color(0, 0, 0, 0), bw: int = 0, radius: int = 10, pad: int = 0) -> StyleBoxFlat:
	var sb := StyleBoxFlat.new()
	sb.bg_color = bg
	sb.border_color = edge
	sb.set_border_width_all(bw)
	sb.set_corner_radius_all(radius)
	sb.content_margin_left = pad
	sb.content_margin_right = pad
	sb.content_margin_top = pad
	sb.content_margin_bottom = pad
	return sb

static func label(text: String, size: int = 28, color: Color = TEXT, align: int = HORIZONTAL_ALIGNMENT_LEFT, scaled: bool = true) -> Label:
	var l := Label.new()
	l.text = text
	l.horizontal_alignment = align
	l.add_theme_font_override("font", Fonts.ui())
	l.add_theme_font_size_override("font_size", fs(size) if scaled else size)
	l.add_theme_color_override("font_color", color)
	l.mouse_filter = Control.MOUSE_FILTER_IGNORE
	return l

static func button(text: String, w: int = 260, h: int = 64, size: int = 28) -> Button:
	var b := Button.new()
	b.text = text
	b.custom_minimum_size = Vector2(w, h)
	b.size = Vector2(w, h)
	b.add_theme_font_override("font", Fonts.ui())
	b.add_theme_font_size_override("font_size", fs(size))
	b.add_theme_color_override("font_color", TEXT)
	b.add_theme_color_override("font_hover_color", Color.WHITE)
	b.add_theme_color_override("font_focus_color", Color.WHITE)
	b.add_theme_stylebox_override("normal", box(PANEL, Color(EDGE, 0.6), 2, 12, 10))
	b.add_theme_stylebox_override("hover", box(PANEL_HI, EDGE, 2, 12, 10))
	b.add_theme_stylebox_override("pressed", box(Color("#3a4a50"), WARM, 2, 12, 10))
	b.add_theme_stylebox_override("focus", box(PANEL_HI, WARM, 3, 12, 10))
	b.focus_mode = Control.FOCUS_ALL
	return b

static func panel(w: float, h: float, bg: Color = Color(PANEL, 0.97)) -> PanelContainer:
	var p := PanelContainer.new()
	p.custom_minimum_size = Vector2(w, h)
	p.size = Vector2(w, h)
	p.add_theme_stylebox_override("panel", box(bg, Color(EDGE, 0.8), 2, 14, 18))
	return p

static func dim_bg(alpha: float = 0.72) -> ColorRect:
	var c := ColorRect.new()
	c.color = Color(0.02, 0.03, 0.035, alpha)
	c.mouse_filter = Control.MOUSE_FILTER_STOP
	c.set_anchors_preset(Control.PRESET_FULL_RECT)
	return c

static func shape_tex(path: String) -> Texture2D:
	return ViewNode.tex(path)
