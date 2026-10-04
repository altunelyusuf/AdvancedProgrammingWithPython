#!/usr/bin/env bash
# Builds the chapter 1 lecture deck version 2.0.0 from executed material and runs every check against the result.
# Usage: build_v2_0_0.sh <python3.14> <out.pptx>
#   1. re-execute the chapter corpus's own claims, so the deck is not built on a corpus that has drifted
#   2. execute every shell session and program the deck shows
#   3. read the source list out of the chapter's RDODI research record
#   4. build the deck, and stamp the version its file name carries into the file's own properties
#   5. refuse it unless every shown example re-runs to the same value, every program re-runs to the same transcript,
#      and nothing overflows its box or its page
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"
$PY ../sen0414_ch01_corpus_v1_2_0.py "$PY"
$PY examples_run_v2_0_0.py "$PY" examples_v1_1_0.py examples_out_v1_1_0.json
$PY sources_make_v1_0_2.py ../../03-materials/ch01/rdodi/sen0414_ch01_research_v1_1_0.ttl ../sen0414_ch01_corpus_v1_2_0.py sources_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v2_0_0.js "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 2.0.0 "SEN0414 Chapter 1 - Python Basics"
$PY ../ch02-deck/deck_check_v1_0_1.py "$OUT"
$PY ../ch03-deck/program_check_v1_0_0.py "$OUT" examples_out_v1_1_0.json "$PY"
python3 layout_check_v1_0_0.py "$OUT" 59
