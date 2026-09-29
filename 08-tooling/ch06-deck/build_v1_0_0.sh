#!/usr/bin/env bash
# Builds the chapter 6 deck version 1.0.0 from executed material and runs every check. Usage: build_v1_0_0.sh <python3.14> <out.pptx> <lecture-out.json>
# Intermediates go to a temporary directory. Reuses the chapter 5 OOXML repair and structure check unchanged.
set -euo pipefail
PY="$1"; OUT="$2"; LEC="$3"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY research_check_v1_0_0.py
$PY taxonomy_make_v1_0_0.py taxonomy_out_v1_0_0.json
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
$PY visuals_make_v1_0_0.py visuals_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v1_0_0.js "$T/raw.pptx" "$LEC"
python3 ../ch03-deck/anim_inject_v1_0_0.py "$T/raw.pptx" "$T/anim.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/anim.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 6 - Lists"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY ../ch03-deck/program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
$PY visual_check_v1_0_0.py "$OUT" visuals_make_v1_0_0.py examples_out_v1_0_0.json "$PY"
rm -rf "$T"
