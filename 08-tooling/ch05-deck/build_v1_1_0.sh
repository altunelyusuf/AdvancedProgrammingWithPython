#!/usr/bin/env bash
# Builds the chapter 5 lecture deck version 1.1.0 from executed material and runs every check.
# Usage: build_v1_1_0.sh <python3.14> <out.pptx>
# Intermediates go to a temporary directory. The executed visual specifications and their check are those of deck
# version 1.0.0, unchanged; the lecture renderer, fit check and plan builder are the course-wide ones in 08-tooling.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
python3 ../sen0414_deck_plan_v1_0_0.py 05 deck_plan_v1_1_0.json
$PY ../sen0414_ch05_corpus_v1_0_0.py "$PY"
$PY examples_run_v1_1_0.py "$PY" examples_out_v1_1_0.json
$PY visuals_make_v1_0_0.py visuals_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v1_1_0.js "$T/raw.pptx" lecture_out_v1_1_0.json
python3 ../ch03-deck/anim_inject_v1_0_0.py "$T/raw.pptx" "$T/anim.pptx"
python3 ooxml_fix_v1_0_0.py "$T/anim.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.1.0 "SEN0414 Chapter 5 - Debugging"
python3 structure_check_v1_0_0.py "$OUT"
$PY ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY ../ch03-deck/program_check_v1_0_0.py "$OUT" examples_out_v1_1_0.json "$PY"
$PY visual_check_v1_1_0.py "$OUT" visuals_make_v1_0_0.py examples_out_v1_1_0.json "$PY"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
rm -rf "$T"
