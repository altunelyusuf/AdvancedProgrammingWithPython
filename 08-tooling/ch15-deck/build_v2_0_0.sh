#!/usr/bin/env bash
# Builds the chapter 15 lecture deck 2.0.0 and its chapter-code manifest, then runs the builder's own manifest checks.
# The independent checks (deck standard check, deck overlap check, first-line error scan) are run by their owners' tools and reported separately.
# Usage: build_v2_0_0.sh PYTHON313_WITH_EZSHEETS    (the examples are run by that interpreter; it needs ezsheets 2026.4.28, google-api-python-client and python-pptx)
set -euo pipefail
cd "$(dirname "$0")"
PY="${1:-python3}"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cp ../../03-materials/ch15/assets/google_standin_v1_0_0.py "$T/google_standin.py"   # the page installs the same file under this name
$PY examples_lint_v2_0_0.py
PYTHONPATH="$T" $PY deck_build_v2_0_0.py
$PY manifest_selfcheck_v2_0_0.py ../../03-materials/ch15/SEN0414_Ch15_GoogleSheets_3e_v2_0_0.pptx ../../03-materials/ch15/page/chapter_code_ch15_v1_0_0.json
