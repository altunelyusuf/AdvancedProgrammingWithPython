#!/usr/bin/env bash
# Builds the chapter 17 lecture deck 2.0.0 and its chapter-code manifest, then runs the builder's own manifest checks.
# The independent checks (deck standard check, deck overlap check, first-line error scan) are run by their owners' tools and reported separately.
# Usage: build_v2_0_0.sh [PYTHON313]    (the examples are run by that interpreter; it needs python-pptx 1.0.2, Pillow, pypdf and python-docx)
# The temporary folders the examples make are put under $TMPDIR; set it to a folder of your own and remove that folder afterwards.
set -euo pipefail
cd "$(dirname "$0")"
PY="${1:-python3}"
$PY examples_lint_v2_0_0.py
$PY deck_build_v2_0_0.py
$PY manifest_selfcheck_v2_0_0.py ../../03-materials/ch17/SEN0414_Ch17_PDFAndWordDocuments_3e_v2_0_0.pptx ../../03-materials/ch17/page/chapter_code_ch17_v1_0_0.json
