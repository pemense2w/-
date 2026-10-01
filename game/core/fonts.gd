class_name Fonts
extends RefCounted
## Fonts: an old print face for in-world lettering, a plainer face for the interface (optional), CJK per language.

static var _cache := {}

static func _load(path: String) -> Font:
	if _cache.has(path):
		return _cache[path]
	var f: Font = null
	if ResourceLoader.exists(path):
		f = load(path)
	_cache[path] = f
	return f

static func lang_suffix() -> String:
	return "" if L.lang == "en" else ("_" + L.lang)

static func world() -> Font:
	var f := _load("res://assets/fonts/world%s.ttf" % lang_suffix())
	if f == null:
		f = _load("res://assets/fonts/world.ttf")
	return f if f else ThemeDB.fallback_font

static func ui() -> Font:
	var plain: bool = G.settings.get("plain_font", false)
	var name := "plain" if plain else "ui"
	var f := _load("res://assets/fonts/%s%s.ttf" % [name, lang_suffix()])
	if f == null:
		f = _load("res://assets/fonts/%s.ttf" % name)
	return f if f else ThemeDB.fallback_font

static func spaced(base: Font, spacing: int) -> Font:
	var fv := FontVariation.new()
	fv.base_font = base
	fv.spacing_glyph = spacing
	return fv
