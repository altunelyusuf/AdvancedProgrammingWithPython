#!/usr/bin/env bash
# Builds the chapter 4 lecture deck 3.1.0 and its chapter-code manifest, then runs the builder's own manifest check.
# The independent checks (deck standard check, deck overlap check) are other sessions' tools and are run by their owners.
# Usage: build_v3_1_0.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v3_1_0.py
python3 manifest_selfcheck_v3_1_0.py ../../03-materials/ch04/SEN0414_Ch04_Functions_3e_v3_1_0.pptx ../../03-materials/ch04/page/chapter_code_ch04_v1_1_0.json
