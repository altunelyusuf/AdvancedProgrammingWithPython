#!/usr/bin/env bash
# Builds the chapter 12 lecture deck 2.0.0 and its chapter-code manifest, then runs the builder's own manifest checks.
# The independent checks (deck standard check, deck overlap check, first-line error scan) are run by their owners' tools and reported separately.
# Usage: build_v2_0_0.sh [NODE_PATH_DIR WORK_DIR]   (with the two arguments the manifest is also run under Pyodide)
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v2_0_0.py
python3 manifest_selfcheck_v2_0_0.py ../../03-materials/ch12/SEN0414_Ch12_CommandLinePrograms_3e_v2_0_0.pptx ../../03-materials/ch12/page/chapter_code_ch12_v1_0_0.json
if [ "$#" -ge 2 ]; then python3 manifest_pyodide_check_v2_0_0.py ../../03-materials/ch12/page/chapter_code_ch12_v1_0_0.json "$1" "$2"; fi
