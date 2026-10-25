#!/usr/bin/env bash
# Builds the chapter 10 lecture deck 2.0.0 and its chapter-code manifest, then runs the builder's own manifest check.
# The independent checks (deck standard check, deck overlap check) are other sessions' tools and are run by their owners.
# Usage: build_v2_0_0.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v2_0_0.py
python3 manifest_selfcheck_v2_0_0.py ../../03-materials/ch10/SEN0414_Ch10_ReadingWritingFiles_3e_v2_0_0.pptx ../../03-materials/ch10/page/chapter_code_ch10_v1_0_0.json
