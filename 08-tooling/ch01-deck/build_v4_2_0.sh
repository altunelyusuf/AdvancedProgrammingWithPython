#!/usr/bin/env bash
# Builds the chapter 1 lecture deck 4.2.0 and its chapter-code manifest 1.2.0, then runs the builder's own manifest check.
# The independent checks (deck standard, deck overlap, deck teaching) are run by their owners: see the task report.
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v4_2_0.py
python3 manifest_selfcheck_v4_2_0.py ../../03-materials/ch01/SEN0414_Ch01_PythonBasics_3e_v4_2_0.pptx ../../03-materials/ch01/page/chapter_code_ch01_v1_2_0.json
