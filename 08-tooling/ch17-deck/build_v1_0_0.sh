#!/usr/bin/env bash
# Builds the chapter 17 lecture deck 1.0.0 from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14> <out.pptx>      (the interpreter is /home/claude/venv314_ch17_latest/bin/python, Python 3.14.6, uv)
# $PY needs pypdf, python-docx, pdfminer.six, Pillow and cryptography (the programs import them). Two other interpreters are used only to
# record failures: /home/claude/venv314_ch17_bare (pypdf only) and /home/claude/venv314_ch17_docx02 (python-docx 0.2.4). Two programs are
# LIVE: they fetch Recursion_Chapter1.pdf and demo.docx from nostarch.com on their first run (kept in the system temp folder) and check the
# sha256 (d943896e0bd2 and b43b21137d7d), so the build needs the network once.
# The renderer (shared deck_render + this chapter's render_v1_0_0.js), the layout/fit/notes checks and the stamp are the course-wide tools
# in 08-tooling. The plan builder, the diagram check, the honesty check, the lecture export and the links check use the system python3
# (rdflib, python-pptx, requests). LibreOffice is not needed to build; it is not used. No PowerPoint is available.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import pypdf, docx; print('pypdf', pypdf.__version__, '- python-docx', docx.__version__ if hasattr(docx, '__version__') else 'imported')"
/home/claude/venv314_ch17_docx02/bin/python -c "import docx" 2>&1 | tail -1 | sed 's/^/python-docx 0.2.4 (expected failure): /' || true
$PY ../sen0414_ch17_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch17_diagrams_v1_0_0.py | tail -1
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
python3 deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 17 - PDF and Word Documents"
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
refused once honesty_check python3 honesty_check_v1_0_0.py "${FX}_once_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
rm -rf "$T"
echo "BUILD OK: $OUT"
