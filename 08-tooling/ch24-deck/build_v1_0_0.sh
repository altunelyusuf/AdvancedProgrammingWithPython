#!/usr/bin/env bash
# Builds the chapter 24 lecture deck 1.0.0 from executed material and runs every check.
# Usage: build_v1_0_0.sh <python3.14> <out.pptx>      (the interpreter is /home/claude/venv314_ch24_latest/bin/python, Python 3.14.6, uv)
# $PY needs pyttsx3 2.99, openai-whisper 20250625, yt-dlp 2026.8.19, torch 2.14.1+cpu and NumPy 2.5.4; eSpeak NG 1.51 (espeak-ng), ffmpeg/ffprobe 6.1.1 and aplay must be on the PATH.
# Three other interpreters are run at check time by the table of environments on slide 5: /home/claude/venv312_ch24_pins (Python 3.12.3, pyttsx3 2.98, openai-whisper 20231117,
# NumPy 1.26.4), /home/claude/venv314_ch24_bare (nothing installed) and $PY itself with ffmpeg taken off the PATH. NOTHING IS HEARD: the machine has no sound card, so every program writes
# WAV files; no program uses a microphone, a GPU, Windows, macOS, a cloud key or YouTube (the four programs that need audio read public-domain LibriVox readings from archive.org,
# which STAND IN FOR YouTube, fetched once into /home/claude/ch24_cache and checked against a SHA-256). The renderer (shared deck_render + this chapter's render_v1_0_0.js), the
# layout/fit/notes checks and the stamp are the course-wide tools in 08-tooling. The plan builder, the diagram check, the program check (it compares pictures with Pillow), the honesty
# check, the lecture export, the links check and the fixtures use the system python3 (rdflib, python-pptx, requests, Pillow); the deck check runs under $PY so that the console rows are
# Python 3.14.6's. LibreOffice is not needed to build. No PowerPoint is available.
# Speed options that do not weaken a gate: REUSE_RECORDING=1 keeps the programs of an existing examples_out_v1_0_0.json (each program was recorded, twice, by an earlier run of
# examples_run_v1_0_0.py) and only recomputes the console rows, charts and tables; the program check runs every program again once and the 17 stale-fixture checks read that run
# (CH24_RUN_CACHE); the 17 refusals run two at a time.
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"; T=$(mktemp -d); export CH24_RUN_CACHE="$T/runs"
phase() { echo "[phase $1: $((SECONDS - ${T0:-0})) s]"; T0=$SECONDS; }
T0=$SECONDS
$PY -c "import sys; assert sys.version_info[:2] == (3, 14), sys.version; print('interpreter', sys.version.split()[0])"
$PY -c "import importlib.metadata as m; print('pyttsx3', m.version('pyttsx3'), '- openai-whisper', m.version('openai-whisper'), '- yt-dlp', m.version('yt-dlp'), '- torch', m.version('torch'), '- NumPy', m.version('numpy'))"
espeak-ng --version | head -1
ffmpeg -version | head -1
test -e /dev/snd && echo "a sound card exists here; the programs still write WAV files" || echo "no sound card (/dev/snd is absent): nothing is heard"
/home/claude/venv314_ch24_bare/bin/python -c "import pyttsx3" 2>&1 | tail -1 | sed 's/^/empty Python (expected failure): /' || true
python3 ../sen0414_ch24_stories_v1_0_0.py | tail -1
python3 ../sen0414_ch24_diagrams_v1_0_0.py | tail -1
unset DISPLAY
phase preflight
if [ "${REUSE_RECORDING:-}" = 1 ] && [ -f examples_out_v1_0_0.json ]; then
  RESUME_CHARTS=1 $PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
else
  $PY examples_run_v1_0_0.py "$PY" examples_out_v1_0_0.json
fi
phase examples
python3 deck_build_v1_0_0.py
NODE_PATH=$(npm root -g) node render_v1_0_0.js deck_plan_v1_0_0.json "$T/raw.pptx"
python3 ../ch05-deck/ooxml_fix_v1_0_0.py "$T/raw.pptx" "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 1.0.0 "SEN0414 Chapter 24 - Text-to-Speech and Speech Recognition Engines"
phase "plan and render"
python3 ../ch05-deck/structure_check_v1_0_0.py "$OUT"
$PY deck_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json
phase "structure and deck_check"
python3 program_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json "$PY"
phase program_check
python3 diagram_check_v1_0_0.py "$OUT"
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
python3 honesty_check_v1_0_0.py "$OUT" examples_out_v1_0_0.json deck_plan_v1_0_0.json
python3 links_check_v1_0_0.py
python3 lecture_export_v1_0_0.py "$OUT" "$($PY -c 'import platform;print(platform.python_version())')"
phase "other checks and export"
# the checks must discriminate: each stale fixture must be refused by the check that owns it, or this build fails
python3 fixtures_make_v1_0_0.py "$OUT" "$T/fx"
refused() { # <fixture> <check name> <command...>
  local fx="$1" label="$2"; shift 2
  if "$@" > "$T/refusal_$fx.txt" 2>&1; then echo "FAIL: fixture ${fx%_h} was NOT refused by $label"; cat "$T/refusal_$fx.txt"; return 1; fi
  echo "fixture ${fx%_h} refused by $label: $(grep -m1 REFUSED "$T/refusal_$fx.txt" | cut -c1-175)"
}
export -f refused; export T
FX="$T/fx/fixture"
{
  echo "stale_expr deck_check $PY deck_check_v1_0_0.py ${FX}_stale_expr_v1_0_0.pptx examples_out_v1_0_0.json"
  echo "stale_table deck_check $PY deck_check_v1_0_0.py ${FX}_stale_table_v1_0_0.pptx examples_out_v1_0_0.json"
  echo "stale_chart deck_check $PY deck_check_v1_0_0.py ${FX}_stale_chart_v1_0_0.pptx examples_out_v1_0_0.json"
  for f in stale_program stale_code stale_image_pixel stale_image_swap stale_image_caption stale_image_loose; do
    echo "$f program_check python3 program_check_v1_0_0.py ${FX}_${f}_v1_0_0.pptx examples_out_v1_0_0.json $PY"
  done
  echo "stale_diagram diagram_check python3 diagram_check_v1_0_0.py ${FX}_stale_diagram_v1_0_0.pptx"
  for f in stale_notexec stale_standin stale_standin_local stale_standin_remote stale_recorded stale_honest_not stale_title stale_image_caption; do
    echo "${f}_h honesty_check python3 honesty_check_v1_0_0.py ${FX}_${f}_v1_0_0.pptx examples_out_v1_0_0.json deck_plan_v1_0_0.json"
  done
} > "$T/jobs.txt"
# xargs runs the 22 refusals (17 fixtures, stale_image_caption twice: program_check and honesty_check) two at a time
xargs -L1 -P2 bash -c 'refused "$@"' _ < "$T/jobs.txt" | sort
phase "refusals"
# the control: a re-encoded picture (other bytes, the same pixels) must be ACCEPTED, as pixel-identical
python3 program_check_v1_0_0.py "${FX}_ok_image_reencoded_v1_0_0.pptx" examples_out_v1_0_0.json "$PY" > "$T/ok.txt" 2>&1 || { echo "FAIL: the re-encoded control was refused"; cat "$T/ok.txt"; exit 1; }
grep -q "4 byte-identical, 1 pixel-identical" "$T/ok.txt" || { echo "FAIL: the control was not accepted as pixel-identical"; cat "$T/ok.txt"; exit 1; }
echo "control ok_image_reencoded accepted by program_check: $(grep -o '5 picture(s).*mismatch(es)' "$T/ok.txt")"
rm -rf "$T"
echo "BUILD OK: $OUT"
