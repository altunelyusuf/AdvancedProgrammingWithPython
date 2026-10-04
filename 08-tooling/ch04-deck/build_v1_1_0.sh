#!/usr/bin/env bash
# Builds the chapter 4 lecture deck version 1.1.0 from executed material and runs every check.
# Usage: build_v1_1_0.sh <python3.14> <out.pptx>
# Intermediates go to a temporary directory. Reuses the chapter 3 build animator and the chapter 5 OOXML repair and
# structure check unchanged, and the course-wide lecture renderer, fit check and plan builder in 08-tooling.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
python3 ../sen0414_deck_plan_v1_0_0.py 04 deck_plan_v1_1_0.json
$PY ../sen0414_ch04_corpus_v1_0_0.py "$PY"
$PY examples_run_v1_1_0.py "$PY" examples_out_v1_1_0.json
$PY visuals_make_v1_0_0.py visuals_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v1_1_0.js "$T/raw.pptx" lecture_out_v1_1_0.json
python3 ../ch03-deck/anim_inject_v1_0_0.py "$T/raw.pptx" "$T/anim.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/anim.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.1.0 "SEN0414 Chapter 4 - Functions"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY ../ch03-deck/program_check_v1_0_0.py "$OUT" examples_out_v1_1_0.json "$PY"
$PY visual_check_v1_0_0.py "$OUT" visuals_make_v1_0_0.py "$PY"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
rm -rf "$T"
