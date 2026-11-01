#!/usr/bin/env bash
# Builds the chapter 3 lecture deck 5.2.0 and its chapter-code manifest 1.2.0, then runs the builder's own manifest check.
# The independent checks (deck standard, deck overlap, deck teaching) are run by their owners: see the task report.
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v5_2_0.py
python3 manifest_selfcheck_v5_2_0.py ../../03-materials/ch03/SEN0414_Ch03_Loops_3e_v5_2_0.pptx ../../03-materials/ch03/page/chapter_code_ch03_v1_2_0.json
