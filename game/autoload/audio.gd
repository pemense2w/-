extends Node
## Sound: ambience / effects / music buses, sound starts on the first click (browser rule).
## Files are optional: a missing cue is simply silent (and still captioned).

const SFX_DIR := "res://assets/audio/sfx/"
const AMB_DIR := "res://assets/audio/amb/"
const MUS_DIR := "res://assets/audio/music/"

var _sfx_players: Array = []
var _amb: AudioStreamPlayer
var _mus: AudioStreamPlayer
var _cache := {}
var unlocked := false
var current_amb := ""
var current_mus := ""

func _ready() -> void:
	for i in 8:
		var p := AudioStreamPlayer.new()
		add_child(p)
		_sfx_players.append(p)
	_amb = AudioStreamPlayer.new()
	_mus = AudioStreamPlayer.new()
	add_child(_amb)
	add_child(_mus)
	if G.settings.has("vol_sfx"):
		apply_volumes()
	G.settings_changed.connect(apply_volumes)

func _input(e: InputEvent) -> void:
	if not unlocked and (e is InputEventMouseButton or e is InputEventKey or e is InputEventScreenTouch):
		unlocked = true
		if current_amb != "":
			ambience(current_amb, true)
		if current_mus != "":
			music(current_mus, true)

func apply_volumes() -> void:
	_amb.volume_db = linear_to_db(maxf(0.0001, float(G.settings.vol_amb)))
	_mus.volume_db = linear_to_db(maxf(0.0001, float(G.settings.vol_music)))

func _load(path: String) -> AudioStream:
	if _cache.has(path):
		return _cache[path]
	var st: AudioStream = null
	for ext in [".ogg", ".wav"]:
		if ResourceLoader.exists(path + ext):
			st = load(path + ext)
			break
	_cache[path] = st
	return st

func play(name: String, pitch: float = 1.0, vol: float = 1.0) -> void:
	G.sfx_cap("cap." + name)
	if not unlocked and not G.test_mode:
		return
	var st := _load(SFX_DIR + name)
	if st == null:
		return
	for p in _sfx_players:
		if not p.playing:
			p.stream = st
			p.pitch_scale = pitch
			p.volume_db = linear_to_db(maxf(0.0001, float(G.settings.vol_sfx) * vol))
			p.play()
			return

func ambience(name: String, force: bool = false) -> void:
	if name == current_amb and not force:
		return
	current_amb = name
	if not unlocked:
		return
	var st := _load(AMB_DIR + name)
	if st == null:
		_amb.stop()
		return
	if st is AudioStreamOggVorbis:
		st.loop = true
	elif st is AudioStreamWAV:
		st.loop_mode = AudioStreamWAV.LOOP_FORWARD
	_amb.stream = st
	apply_volumes()
	_amb.play()

func music(name: String, force: bool = false) -> void:
	if name == current_mus and not force:
		return
	current_mus = name
	if not unlocked:
		return
	var st := _load(MUS_DIR + name)
	if st == null:
		_mus.stop()
		return
	_mus.stream = st
	apply_volumes()
	_mus.play()

func stop_music() -> void:
	current_mus = ""
	_mus.stop()
