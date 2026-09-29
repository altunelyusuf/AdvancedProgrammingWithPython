#!/usr/bin/env bash
# Builds the chapter 5 deck version 1.0.1 from executed material and runs every check. Usage: build_v1_0_1.sh <python3.14> <out.pptx> <lecture-out.json>
set -euo pipefail
PY="$1"; OUT="$2"; LEC="$3"; cd "$(dirname "$0")"
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
$PY visuals_make_v1_0_0.py visuals_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v1_0_0.js /tmp/ch5_raw.pptx "$LEC"
python3 ../ch03-deck/anim_inject_v1_0_0.py /tmp/ch5_raw.pptx /tmp/ch5_anim.pptx
python3 ooxml_fix_v1_0_0.py /tmp/ch5_anim.pptx "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.1 "SEN0414 Chapter 5 - Debugging"
python3 structure_check_v1_0_0.py "$OUT"
$PY ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY ../ch03-deck/program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
$PY visual_check_v1_1_0.py "$OUT" visuals_make_v1_0_0.py examples_out_v1_0_0.json "$PY"
