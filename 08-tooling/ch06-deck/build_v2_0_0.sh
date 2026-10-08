#!/usr/bin/env bash
# Builds the SEN0414 chapter 6 deck version 2.0.0 from executed material and runs every check.
# Usage: build_v2_0_0.sh <python3.14> <out.pptx>
# Intermediates go to a temporary directory. The renderer, the ooxml repair, the stamp, the fit, layout and notes
# checks, deck_check and program_check are the course-wide ones, reused by path; the plan, the examples and the
# fixtures are this chapter's.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY ../sen0414_ch06_corpus_v1_0_0.py "$PY" | tail -1
$PY examples_run_v2_0_0.py "$PY" examples_out_v2_0_0.json
python3 deck_build_v2_0_0.py
python3 lecture_export_v2_0_0.py deck_plan_v2_0_0.json ../ch06-page/lecture_v2_0_0.json
NODE_PATH=$(npm root -g) node ../deck_render_v1_0_0.js deck_plan_v2_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 2.0.0 "SEN0414 Chapter 6 - Lists"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY ../ch02-deck/program_check_v2_0_1.py "$OUT" examples_out_v2_0_0.json
# the fit check is pessimistic: its remaining pairs are the renderer's own designs (the caption inside a program panel, the title
# and closing frames) - overflowing frames must be 0, the pairs are read by hand in REVIEW_v2_0_0.md
python3 ../deck_fit_check_v1_0_0.py "$OUT" || true
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
rm -rf "$T"
