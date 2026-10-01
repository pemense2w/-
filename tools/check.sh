#!/bin/bash
# compile-check every script: loads the project headless and prints script errors
cd "$(dirname "$0")/.."
godot --headless --path . --quit 2>&1 | grep -E "ERROR|SCRIPT|Parse|Compile|at: " | grep -v "ALSA\|audio" | sort -u | head -${1:-40}
