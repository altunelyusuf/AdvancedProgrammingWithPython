#!/usr/bin/env bash
# Builds the chapter 16 lecture deck 2.0.0 and its chapter-code manifest, then runs the builder's own manifest checks.
# The independent checks (deck standard check, deck overlap check, first-line error scan) are run by their owners' tools and reported separately.
# Usage: build_v2_0_0.sh [PYTHON313]    (the examples are run by that interpreter; it needs python-pptx 1.0.2 and Pillow; the examples use the standard library only)
set -euo pipefail
cd "$(dirname "$0")"
PY="${1:-python3}"
$PY examples_lint_v2_0_0.py
$PY deck_build_v2_0_0.py
$PY manifest_selfcheck_v2_0_0.py ../../03-materials/ch16/SEN0414_Ch16_SQLiteDatabases_3e_v2_0_0.pptx ../../03-materials/ch16/page/chapter_code_ch16_v1_0_0.json
