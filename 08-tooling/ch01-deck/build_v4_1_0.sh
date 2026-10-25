#!/usr/bin/env bash
# Builds the chapter 1 lecture deck 4.1.0 (error-first repair of example 14) and its chapter-code manifest 1.1.0, then runs the builder's own manifest check.
# Usage: build_v4_1_0.sh
set -euo pipefail
cd "$(dirname "$0")"
python3 deck_build_v4_1_0.py
python3 manifest_selfcheck_v4_1_0.py ../../03-materials/ch01/SEN0414_Ch01_PythonBasics_3e_v4_1_0.pptx ../../03-materials/ch01/page/chapter_code_ch01_v1_1_0.json
