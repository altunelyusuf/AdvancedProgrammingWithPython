#!/usr/bin/env bash
# Builds the chapter 20 lecture deck 1.0.1 (1.0.0 with the DNS count corrected from 13 of 18 to 12 of 18 gateway domains; every other script is the unchanged 1.0.0 one) from executed material and runs every check.
# Usage: build_v1_0_1.sh <python3.14> <out.pptx>      (the interpreter is /home/claude/venv314_ch20_latest/bin/python, Python 3.14.6, uv)
# $PY needs ezgmail, requests, aiosmtpd, cryptography and google-api-python-client (the programs import them). Two other interpreters record what
# other environments print: /home/claude/venv314_ch20_bare (the standard library only) and /home/claude/venv314_ch20_pins (requests 2.32.3 and
# the pinned versions of Appendix A). The five interpreters of the table on the slide about Python versions are run at check time.
# No real Gmail account, phone, ntfy server or Twilio account is used anywhere: seven programs run against local stand-ins (aiosmtpd, the real
# ezgmail on a stand-in whose replies were written by this study, and a recorder in place of ntfy). The renderer (shared deck_render + this
# chapter's render_v1_0_0.js), the layout/fit/notes checks and the stamp are the course-wide tools in 08-tooling. The plan builder, the diagram
# check, the honesty check, the lecture export and the links check use the system python3 (rdflib, python-pptx, requests).
# LibreOffice is not needed to build. No PowerPoint is available.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d)
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import importlib.metadata as m; print('ezgmail', m.version('ezgmail'), '- requests', m.version('requests'), '- aiosmtpd', m.version('aiosmtpd'))"
/home/claude/venv314_ch20_bare/bin/python -c "import ezgmail" 2>&1 | tail -1 | sed 's/^/standard library only (expected failure): /' || true
$PY ../sen0414_ch20_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch20_diagrams_v1_0_0.py | tail -1
$PY examples_run_v1_0_0.py "$PY" "$T/examples_rerun.json"
python3 - "$T/examples_rerun.json" examples_out_v1_0_0.json <<'PYE'
import json,sys
a=json.load(open(sys.argv[1])); b=json.load(open(sys.argv[2]))
print("examples re-run equals the committed examples_out_v1_0_0.json:", a==b)
PYE
python3 deck_build_v1_0_1.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_1.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.1 "SEN0414 Chapter 20 - Sending Email, Texts, and Push Notifications"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY deck_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json
$PY program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json
python3 diagram_check_v1_0_0.py "$OUT"
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
python3 honesty_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json deck_plan_v1_0_1.json
python3 links_check_v1_0_1.py
python3 lecture_export_v1_0_1.py "$OUT" "$($PY -c 'import platform;print(platform.python_version())')"
# the checks must discriminate: each stale fixture must be refused by the check that owns it, or this build fails
python3 fixtures_make_v1_0_0.py "$OUT" "$T/fx"
# the 13 fixture checks run two at a time (the machine has 2 CPUs and shares them): each job writes its own file, the verdicts are read after the pair finished
JOBS=()
add() { JOBS+=("$*"); }   # <fixture> <check name> <command...>
runjob() { local fx="$1" label="$2"; shift 2; if "$@" > "$T/ref_$fx.txt" 2>&1; then echo "NOT REFUSED" > "$T/ref_$fx.verdict"; else echo REFUSED > "$T/ref_$fx.verdict"; fi; }
FX="$T/fx/fixture_stale"
add expr deck_check $PY deck_check_v1_0_0.py "${FX}_expr_v1_0_0.pptx" examples_out_v1_0_0.json
add table deck_check $PY deck_check_v1_0_0.py "${FX}_table_v1_0_0.pptx" examples_out_v1_0_0.json
add chart deck_check $PY deck_check_v1_0_0.py "${FX}_chart_v1_0_0.pptx" examples_out_v1_0_0.json
for f in program code tcap; do add $f program_check $PY program_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json "$PY"; done
add diagram diagram_check python3 diagram_check_v1_0_0.py "${FX}_diagram_v1_0_0.pptx"
for f in notexec standin_gmail standin_local recorded honest_not title; do
  add $f honesty_check python3 honesty_check_v1_0_0.py "${FX}_${f}_v1_0_0.pptx" examples_out_v1_0_0.json deck_plan_v1_0_1.json
done
n=${#JOBS[@]}; k=0
while [ $k -lt $n ]; do
  for m in $k $((k+1)); do [ $m -lt $n ] && { set -- ${JOBS[$m]}; runjob "$@" & }; done
  wait; k=$((k+2))
done
for job in "${JOBS[@]}"; do
  set -- $job; fx="$1"; label="$2"
  if [ "$(cat "$T/ref_$fx.verdict")" != "REFUSED" ]; then echo "FAIL: fixture $fx was NOT refused by $label"; cat "$T/ref_$fx.txt"; exit 1; fi
  echo "fixture $fx refused by $label: $(grep -m1 REFUSED "$T/ref_$fx.txt" | cut -c1-175)"
done
rm -rf "$T"
echo "BUILD OK: $OUT"
