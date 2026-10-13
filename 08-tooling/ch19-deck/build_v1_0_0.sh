#!/usr/bin/env bash
# Builds the chapter 19 lecture deck 1.0.0 from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14> <out.pptx>      (the interpreter is /home/claude/venv314_ch19_latest/bin/python, Python 3.14.6, uv)
# $PY needs schedule, tzdata, pyperclip and playsound3 (the programs import them; time, datetime, zoneinfo, subprocess, sched and threading are the standard library). Two other
# interpreters are used only to record what other environments print: /home/claude/venv314_ch19_bare (the standard library only: schedule and tzdata do not
# import) and /home/claude/venv314_ch19_pins (playsound3 2.4.0, the version Appendix A pins). No program of
# this chapter is claimed to read the network by this deck; see the notes of the slides.
# The renderer (shared deck_render + this chapter's render_v1_0_0.js), the layout/fit/notes checks and the stamp are the course-wide tools
# in 08-tooling. The plan builder, the diagram check, the honesty check, the lecture export and the links check use the system python3
# (rdflib, python-pptx, requests). LibreOffice is not needed to build; it is not used. No PowerPoint is available.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import importlib.metadata as m; print('schedule', m.version('schedule'), '- tzdata', m.version('tzdata'))"
/home/claude/venv314_ch19_bare/bin/python -c "import schedule" 2>&1 | tail -1 | sed 's/^/standard library only (expected failure): /' || true
$PY ../sen0414_ch19_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch19_diagrams_v1_0_0.py | tail -1
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
python3 deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 19 - Keeping Time, Scheduling Tasks, and Launching Programs"
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
refused notexec honesty_check python3 honesty_check_v1_0_0.py "${FX}_notexec_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
refused once honesty_check python3 honesty_check_v1_0_0.py "${FX}_once_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
refused emulated honesty_check python3 honesty_check_v1_0_0.py "${FX}_emulated_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
refused honest_not honesty_check python3 honesty_check_v1_0_0.py "${FX}_honest_not_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
rm -rf "$T"
echo "BUILD OK: $OUT"
