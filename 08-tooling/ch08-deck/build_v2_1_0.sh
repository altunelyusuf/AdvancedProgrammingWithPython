#!/usr/bin/env bash
# Builds the chapter 8 lecture deck 2.1.0 and its chapter-code manifest 1.1.0, then runs the builder's own manifest check.
# The independent checks (deck standard, deck overlap, deck teaching) are run by their owners: see the task report.
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v2_1_0.py
python3 manifest_selfcheck_v2_1_0.py ../../03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx ../../03-materials/ch08/page/chapter_code_ch08_v1_1_0.json
