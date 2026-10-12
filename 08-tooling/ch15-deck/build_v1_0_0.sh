#!/usr/bin/env bash
# Builds the chapter 15 lecture deck 1.0.0 from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14 with ezsheets> <out.pptx>
# Google was never reached: every program that uses EZSheets runs the real library against the stand-in for Google written for this
# study (corpus programs' first 72 lines; progrun_v1_0_0.py sets CH15_FIX to ../ch15-page/fixtures), and the deck says so on each slide.
# The renderer (shared deck_render + this chapter's render_v1_0_0.js), the layout/fit/notes checks and the stamp are the course-wide tools in
# 08-tooling. Python 3.14.x is $PY (it has ezsheets); the plan builder, the diagram check, the lecture export and the links check use the
# system python3 (rdflib, python-pptx, requests). LibreOffice is not needed to build; it was used only to look at the slides.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import ezsheets; print('ezsheets', ezsheets.__version__)"
$PY ../sen0414_ch15_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch15_diagrams_v1_0_0.py | tail -1
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
python3 deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 15 - Google Sheets"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY deck_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
$PY program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
python3 diagram_check_v1_0_0.py "$OUT"
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
python3 honesty_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json deck_plan_v1_0_0.json
python3 links_check_v1_0_0.py
python3 lecture_export_v1_0_0.py "$OUT" "$($PY -c 'import platform;print(platform.python_version())')"
# the checks must discriminate: each stale fixture must be refused by the check that owns it, or this build fails
python3 fixtures_make_v1_0_0.py "$OUT" "$T/fx"
refused() { # <fixture> <check name> <command...>
  local fx="$1" label="$2"; shift 2
  if "$@" > "$T/refusal.txt" 2>&1; then echo "FAIL: fixture $fx was NOT refused by $label"; cat "$T/refusal.txt"; exit 1; fi
  echo "fixture $fx refused by $label: $(grep -m1 REFUSED "$T/refusal.txt" | cut -c1-175)"
}
FX="$T/fx/fixture_stale"
refused expr deck_check $PY deck_check_v1_0_0.py "${FX}_expr_v1_0_0.pptx" examples_out_v1_0_0.json
refused table deck_check $PY deck_check_v1_0_0.py "${FX}_table_v1_0_0.pptx" examples_out_v1_0_0.json
refused chart deck_check $PY deck_check_v1_0_0.py "${FX}_chart_v1_0_0.pptx" examples_out_v1_0_0.json
for f in program code tcap; do refused $f program_check $PY program_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json "$PY"; done
refused diagram diagram_check python3 diagram_check_v1_0_0.py "${FX}_diagram_v1_0_0.pptx"
refused label honesty_check python3 honesty_check_v1_0_0.py "${FX}_label_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
refused notexec honesty_check python3 honesty_check_v1_0_0.py "${FX}_notexec_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
rm -rf "$T"
echo "BUILD OK: $OUT"
