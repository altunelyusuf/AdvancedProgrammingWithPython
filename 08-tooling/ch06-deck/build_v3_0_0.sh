#!/usr/bin/env bash
# Builds the SEN0414 chapter 6 deck v3.0.0 and its chapter-code manifest, then runs the builder's own consistency checks and the existing layout, notes and fit checks.
# Usage: build_v3_0_0.sh [python3.14]      (python-pptx 1.0.2 in the system python3). The independent deck standard check and the overlap check are run by their own sessions.
set -euo pipefail
PY="${1:-/root/.local/bin/python3.14}"; cd "$(dirname "$0")"
OUT=../../03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_0_0.pptx
python3 deck_build_v3_0_0.py "$PY"
python3 manifest_verify_v1_0_0.py
python3 ../deck_layout_check_v1_0_0.py "$OUT"
python3 ../deck_notes_check_v1_0_0.py "$OUT"
python3 ../deck_fit_check_v1_0_0.py "$OUT"
