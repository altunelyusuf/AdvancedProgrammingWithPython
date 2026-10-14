#!/usr/bin/env bash
# Builds the chapter 23 lecture deck 1.0.0 from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14> <out.pptx>      (the interpreter is /home/claude/venv314_ch23_latest/bin/python, Python 3.14.6, uv)
# $PY needs PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, PyTweening 1.2.0, PyGetWindow 0.0.9, MouseInfo 0.1.3, pyperclip 1.11.0, python3-xlib 0.15, Pillow 12.3.0,
# NumPy 2.5.4 and OpenCV (opencv-python-headless 5.0.0.93); the programs need Xvfb, openbox, xdotool, xclip, xterm, xrandr, xprintidle and scrot on the PATH. Four other
# interpreters are run at check time by the table of environments on slide 5: /home/claude/venv314_ch23_nocv (no OpenCV), /home/claude/venv314_ch23_oldscreeze
# (PyScreeze 0.1.28), /home/claude/venv312_ch23_tk86 (Python 3.12.3 with Tk 8.6.14) and /home/claude/venv314_ch23_bare (nothing installed). EVERY program starts its own
# virtual X display (Xvfb) and the build removes DISPLAY from the environment first, so nothing is ever sent to the screen of this machine or to a person. The renderer
# (shared deck_render + this chapter's render_v1_0_0.js), the layout/fit/notes checks and the stamp are the course-wide tools in 08-tooling. The plan builder, the diagram
# check, the honesty check, the lecture export, the links check and the fixtures use the system python3 (rdflib, python-pptx, requests, Pillow). LibreOffice is not
# needed to build. No PowerPoint is available.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import importlib.metadata as m; print('PyAutoGUI', m.version('pyautogui'), '- PyScreeze', m.version('pyscreeze'), '- PyMsgBox', m.version('pymsgbox'), '- Pillow', m.version('pillow'), '- OpenCV', m.version('opencv-python-headless'))"
(Xvfb -help 2>&1 || true) | (head -1; cat >/dev/null) | sed 's/^/Xvfb: /'
/home/claude/venv314_ch23_bare/bin/python -c "import pyautogui" 2>&1 | tail -1 | sed 's/^/empty Python (expected failure): /' || true
python3 ../sen0414_ch23_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch23_diagrams_v1_0_0.py | tail -1
unset DISPLAY
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
python3 deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 23 - Controlling the Keyboard and Mouse"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY deck_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json
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
FX="$T/fx/fixture"
refused stale_expr deck_check $PY deck_check_v1_0_0.py "${FX}_stale_expr_v1_0_0.pptx" examples_out_v1_0_0.json
refused stale_table deck_check $PY deck_check_v1_0_0.py "${FX}_stale_table_v1_0_0.pptx" examples_out_v1_0_0.json
refused stale_chart deck_check $PY deck_check_v1_0_0.py "${FX}_stale_chart_v1_0_0.pptx" examples_out_v1_0_0.json
for f in stale_program stale_code stale_image_pixel stale_image_swap stale_image_caption stale_image_loose; do
  refused $f program_check $PY program_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json "$PY"
done
refused stale_diagram diagram_check python3 diagram_check_v1_0_0.py "${FX}_stale_diagram_v1_0_0.pptx"
for f in stale_notexec stale_standin stale_standin_local stale_recorded stale_honest_not stale_title stale_image_caption; do
  refused $f honesty_check python3 honesty_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
done
# the control: a re-encoded picture (other bytes, the same pixels) must be ACCEPTED, as pixel-identical
$PY program_check_v1_0_0.py "${FX}_ok_image_reencoded_v1_0_0.pptx" examples_out_v1_0_0.json "$PY" > "$T/ok.txt" 2>&1 || { echo "FAIL: the re-encoded control was refused"; cat "$T/ok.txt"; exit 1; }
grep -q "5 byte-identical, 1 pixel-identical" "$T/ok.txt" || { echo "FAIL: the control was not accepted as pixel-identical"; cat "$T/ok.txt"; exit 1; }
echo "control ok_image_reencoded accepted by program_check: $(grep -o '6 picture(s).*mismatch(es)' "$T/ok.txt")"
rm -rf "$T"
echo "BUILD OK: $OUT"
