#!/bin/bash
# Runs every headless playthrough test; exits non-zero if any fails.
cd "$(dirname "$0")/.."
fail=0
for t in tests/test_ch*.gd tests/test_misc.gd tests/test_stage.gd; do
  name=$(basename "$t" .gd)
  out=$(SW_TEST=1 SW_SAVE_DIR=/tmp/sw_$name timeout 150 godot --headless --path . -s "$t" 2>&1)
  res=$(echo "$out" | grep -E "RESULT|TIMEOUT" | tail -1)
  echo "$name: $res"
  echo "$out" | grep -E "^FAIL|SCRIPT ERROR" | head -20
  echo "$out" | grep -q "fails=0" || fail=1
done
exit $fail
