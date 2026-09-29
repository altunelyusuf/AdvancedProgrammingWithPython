#!/usr/bin/env bash
# Builds the chapter 3 deck version 2.0.0 from executed material and runs every check. Usage: build_v2_0_0.sh <python3.14> <out.pptx>
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"
$PY examples_run_v1_1_0.py "$PY" examples_out_v1_1_0.json
$PY visuals_make_v1_0_0.py visuals_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v2_0_0.js /tmp/ch3v2_raw.pptx
python3 anim_inject_v1_0_0.py /tmp/ch3v2_raw.pptx "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 2.0.0 "SEN0414 Chapter 3 - Loops"
python3 ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY program_check_v1_0_0.py "$OUT" examples_out_v1_1_0.json "$PY"
$PY visual_check_v1_0_0.py "$OUT" visuals_make_v1_0_0.py examples_out_v1_1_0.json "$PY"
