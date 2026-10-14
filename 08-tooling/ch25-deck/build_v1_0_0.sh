#!/usr/bin/env bash
# Builds the chapter 25 lecture deck 1.0.0 (Threads) from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14> <out.pptx>      (the interpreter is /home/claude/venv314_ch25_latest/bin/python, Python 3.14.6, uv)
# The programs of the deck use the standard library only. The table of environments on slide 23 also runs the probe under four more interpreters at check time
# (uv Python 3.11.15, 3.12.13, 3.13.14 and the free-threaded 3.14.6, paths in examples_v1_0_0.py); the standard build of 3.14.6 is $PY. The downloader programs run
# against an HTTP server of the program on 127.0.0.1 (a local stand-in): xkcd.com is never contacted. NO program prints a duration: the research's timings are read from
# ../ch25-page/timing_record_v1_0_0.json by tables and charts and are Recorded, not measured again. The renderer (shared deck_render + this chapter's render_v1_0_0.js),
# the layout/fit/notes checks and the stamp are the course-wide tools in 08-tooling. The plan builder, the diagram check, the honesty check, the lecture export, the links
# check, the program check (it needs Pillow for the pixel comparison; it runs the programs with $PY) and the fixtures use the system python3 (rdflib, python-pptx, requests, Pillow). The stale-fixture refusals run two at a time (xargs -P2). LibreOffice is not
# needed to build. No PowerPoint is available.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import sysconfig; print('GIL build: Py_GIL_DISABLED =', sysconfig.get_config_var('Py_GIL_DISABLED'))"
python3 ../sen0414_ch25_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch25_diagrams_v1_0_0.py | tail -1
$PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
python3 deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 25 - Threads"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY deck_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json
python3 program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
python3 diagram_check_v1_0_0.py "$OUT"
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
python3 honesty_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json deck_plan_v1_0_0.json
python3 links_check_v1_0_0.py
python3 lecture_export_v1_0_0.py "$OUT" "$($PY -c 'import platform;print(platform.python_version())')"
# the checks must discriminate: each stale fixture must be refused by the check that owns it, or this build fails
python3 fixtures_make_v1_0_0.py "$OUT" "$T/fx"
# every refusal is one command line of a task file; two run at a time
FX="$T/fx/fixture"; TASKS="$T/tasks.txt"; : > "$TASKS"
export T
refused_one() { # <fixture> <check name> <command...>
  local fx="$1" label="$2"; shift 2
  if "$@" > "$T/refusal_${fx}_${label}.txt" 2>&1; then echo "FAIL: fixture $fx was NOT refused by $label"; cat "$T/refusal_${fx}_${label}.txt"; return 1; fi
  echo "fixture $fx refused by $label: $(grep -m1 REFUSED "$T/refusal_${fx}_${label}.txt" | cut -c1-175)"
}
export -f refused_one
task() { echo "refused_one $*" >> "$TASKS"; }
for f in stale_expr stale_table stale_chart; do
  task $f deck_check $PY deck_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json
done
for f in stale_program stale_code stale_image_pixel stale_image_swap stale_image_caption stale_image_loose stale_photo_pixel stale_photo_swap stale_photo_caption stale_photo_loose; do
  task $f program_check python3 program_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json "$PY"
done
task stale_diagram diagram_check python3 diagram_check_v1_0_0.py "${FX}_stale_diagram_v1_0_0.pptx"
for f in stale_notexec stale_standin stale_standin_local stale_recorded stale_honest_not stale_title stale_image_caption; do
  task $f honesty_check python3 honesty_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_0.json
done
xargs -P2 -d '\n' -I{} bash -c '{}' < "$TASKS" || { echo "FAIL: a stale fixture was not refused"; exit 1; }
# the controls: a re-encoded picture and a re-encoded photograph (other bytes, the same pixels) must be ACCEPTED, as pixel-identical
for c in ok_image_reencoded ok_photo_reencoded; do
  python3 program_check_v1_0_0.py "${FX}_${c}_v1_0_0.pptx" examples_out_v1_0_0.json "$PY" > "$T/ok_$c.txt" 2>&1 || { echo "FAIL: the control $c was refused"; cat "$T/ok_$c.txt"; exit 1; }
  grep -q "4 byte-identical, 1 pixel-identical" "$T/ok_$c.txt" || { echo "FAIL: the control $c was not accepted as pixel-identical"; cat "$T/ok_$c.txt"; exit 1; }
  echo "control $c accepted by program_check: $(grep -o '5 picture(s).*mismatch(es)' "$T/ok_$c.txt")"
done
rm -rf "$T"
echo "BUILD OK: $OUT"
