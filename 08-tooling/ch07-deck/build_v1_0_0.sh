#!/usr/bin/env bash
# Builds the chapter 7 lecture deck 1.0.0 from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14> <out.pptx>
# The renderer, the layout/fit/notes checks and the stamp are the course-wide tools in 08-tooling; the plan builder,
# the example runner and the deck/program checks are this chapter's.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY ../sen0414_ch07_corpus_v1_0_0.py > /dev/null
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
$PY deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node ../deck_render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 7 - Dictionaries and Structuring Data"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY deck_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
$PY program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
# the checks must discriminate: each stale fixture must be refused by the check that owns it
python3 fixtures_make_v1_0_0.py "$OUT" "$T/fx"
for f in expr chart table; do ! $PY deck_check_v1_0_0.py "$T/fx/fixture_stale_${f}_v1_0_0.pptx" examples_out_v1_0_0.json > /dev/null && echo "fixture $f refused by deck_check"; done
! $PY program_check_v1_0_0.py "$T/fx/fixture_stale_program_v1_0_0.pptx" examples_out_v1_0_0.json "$PY" > /dev/null && echo "fixture program refused by program_check"
rm -rf "$T"
