extends Node
## String tables: one JSON per language, flat key -> text. Scenes and puzzles refer to keys, never to text.

signal language_changed

const LANGS := ["en", "zh", "ja"]
const NAMES := {"en": "English", "zh": "简体中文", "ja": "日本語"}
var lang := "en"
var _tables := {}

func _ready() -> void:
	for l in LANGS:
		_load(l)

func _load(l: String) -> void:
	var p := "res://assets/i18n/%s.json" % l
	if not FileAccess.file_exists(p):
		_tables[l] = {}
		return
	var f := FileAccess.open(p, FileAccess.READ)
	var d = JSON.parse_string(f.get_as_text())
	_tables[l] = d if d is Dictionary else {}

func set_language(l: String) -> void:
	if not (l in LANGS):
		l = "en"
	lang = l
	language_changed.emit()

func has_key(key: String) -> bool:
	return _tables.get(lang, {}).has(key) or _tables.get("en", {}).has(key)

func t(key: String, args: Array = []) -> String:
	var s = _tables.get(lang, {}).get(key, null)
	if s == null:
		s = _tables.get("en", {}).get(key, null)
	if s == null:
		return "⟦%s⟧" % key
	var out: String = s
	for i in args.size():
		out = out.replace("{%d}" % i, str(args[i]))
	return out

## pick one of several numbered variants key.1 .. key.n (random)
func pick(key: String) -> String:
	var n := 0
	while has_key("%s.%d" % [key, n + 1]):
		n += 1
	if n == 0:
		return t(key)
	return t("%s.%d" % [key, 1 + randi() % n])

func system_default_language() -> String:
	var loc := OS.get_locale_language()
	if loc == "zh":
		return "zh"
	if loc == "ja":
		return "ja"
	return "en"
