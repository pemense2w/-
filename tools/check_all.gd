extends SceneTree
## Loads every GDScript file under res://game so parse errors in lazily loaded scripts show up.
func _initialize() -> void:
	var bad := 0
	var stack := ["res://game"]
	while not stack.is_empty():
		var d: String = stack.pop_back()
		for f in DirAccess.get_files_at(d):
			if f.ends_with(".gd"):
				var s = load(d + "/" + f)
				if s == null:
					bad += 1
					print("LOAD FAILED: ", d, "/", f)
		for sub in DirAccess.get_directories_at(d):
			stack.append(d + "/" + sub)
	print("check_all done, failures: ", bad)
	quit(1 if bad > 0 else 0)
