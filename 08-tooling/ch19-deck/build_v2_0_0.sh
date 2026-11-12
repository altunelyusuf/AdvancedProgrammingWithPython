#!/usr/bin/env bash
# Builds the chapter 19 lecture deck 2.0.0 and its chapter-code manifest with the generic builder, then runs the builder's own manifest check.
# The independent checks (deck standard check, deck overlap check) are run by their owners' tools; their logs are in logs_v2_0_0/.
# Usage: build_v2_0_0.sh [PYTHON313]    (needs python-pptx 1.0.2, Pillow and the story pictures in 03-materials/ch19/assets/)
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${1:-python3}"
$PY chapter_deck_build_v2_1_0.py ch19-deck/spec
D=../03-materials/ch19/SEN0414_Ch19_TimeScheduling_3e_v2_0_0.pptx; M=../03-materials/ch19/page/chapter_code_ch19_v1_0_0.json
$PY ch18-deck/manifest_selfcheck_v2_0_0.py $D $M
$PY sen0414_deck_standard_check_v1_0_0.py 19 $D $M
$PY sen0414_deck_overlap_check_v1_0_0.py $D
