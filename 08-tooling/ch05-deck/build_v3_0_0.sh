#!/usr/bin/env bash
# Builds the chapter 5 lecture deck 3.0.0 and its chapter-code manifest, then runs the builder's own manifest check.
# The independent checks (deck standard check, deck overlap check) are other sessions' tools and are run by their owners.
# Usage: build_v3_0_0.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v3_0_0.py
python3 manifest_selfcheck_v3_0_0.py ../../03-materials/ch05/SEN0414_Ch05_Debugging_3e_v3_0_0.pptx ../../03-materials/ch05/page/chapter_code_ch05_v1_0_0.json
