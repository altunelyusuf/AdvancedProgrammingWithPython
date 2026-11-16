#!/usr/bin/env bash
# Builds the chapter 20 lecture deck 2.0.0 and its chapter-code manifest with the generic builder 2.3.0, then runs the builder's own manifest check.
# The independent checks (material check, deck overlap check, story prose check) are run by their owners' tools; their logs are in logs_v2_0_0/.
# Usage: build_v2_0_0.sh [PYTHON]    (needs python-pptx 1.0.2, Pillow, ezgmail, requests, aiosmtpd and the story pictures in 03-materials/ch20/assets/)
set -euo pipefail
cd "$(dirname "$0")/.."
PY="${1:-python3}"
$PY chapter_deck_build_v2_3_0.py ch20-deck/spec
D=../03-materials/ch20/SEN0414_Ch20_EmailTextsPushNotifications_3e_v2_0_0.pptx; M=../03-materials/ch20/page/chapter_code_ch20_v1_0_0.json
$PY manifest_selfcheck_v2_1_0.py $D $M
$PY cme_material_check_v1_0_0.py $D
$PY sen0414_deck_overlap_check_v1_0_0.py $D
