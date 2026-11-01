#!/usr/bin/env bash
# Builds the chapter 6 lecture deck 3.1.1 and its chapter-code manifest 1.1.1, then runs the builder's own manifest check.
# The independent checks (deck standard, deck teaching, deck overlap) are run by their owners: see the task report.
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v3_1_1.py
python3 manifest_selfcheck_v3_1_0.py ../../03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_1_1.pptx ../../03-materials/ch06/page/chapter_code_ch06_v1_1_1.json
