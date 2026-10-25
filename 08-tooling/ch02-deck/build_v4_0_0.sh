#!/usr/bin/env bash
# Builds the chapter 2 lecture deck 4.0.0 and its chapter-code manifest, then runs the builder's own manifest check.
# The independent checks (deck standard check, deck overlap check) are other sessions' tools and are run by their owners.
# Usage: build_v4_0_0.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v4_0_0.py
python3 manifest_selfcheck_v4_0_0.py ../../03-materials/ch02/SEN0414_Ch02_FlowControl_3e_v4_0_0.pptx ../../03-materials/ch02/page/chapter_code_ch02_v1_0_0.json
