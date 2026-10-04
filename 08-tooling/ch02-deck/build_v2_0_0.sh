#!/usr/bin/env bash
# Builds the chapter 2 lecture deck version 2.0.0 from executed material and runs every check against the result.
# Usage: build_v2_0_0.sh <python3.14> <out.pptx>
#   1. re-execute the chapter corpus's own claims, under both interpreters it names, so the deck is not built on a
#      corpus that has drifted
#   2. execute every shell session and every program the deck shows
#   3. read the source list out of the chapter's RDODI research record
#   4. build the deck, and stamp the version its file name carries into the file's own properties
#   5. refuse it unless every shown example re-runs to the same value, every program re-runs to the same transcript,
#      every program that is meant to fail still fails with the same message, and nothing overflows its box or page
set -euo pipefail
PY="$1"; OUT="$2"; cd "$(dirname "$0")"
$PY ../sen0414_ch02_corpus_v1_0_0.py "$PY"
$PY ../ch01-deck/examples_run_v2_1_0.py "$PY" examples_v1_1_0.py examples_out_v1_1_0.json
$PY ../ch01-deck/sources_make_v1_0_2.py ../../03-materials/ch02/rdodi/sen0414_ch02_research_v1_1_0.ttl ../sen0414_ch02_corpus_v1_0_0.py sources_out_v1_0_0.json
NODE_PATH=$(npm root -g) node deck_v2_0_0.js "$OUT"
python3 ../office_stamp_v1_0_0.py "$OUT" 2.0.0 "SEN0414 Chapter 2 - Flow Control"
$PY deck_check_v1_0_1.py "$OUT"
$PY ../ch03-deck/program_check_v1_0_0.py "$OUT" examples_out_v1_1_0.json "$PY"
$PY ../ch01-deck/program_fail_check_v1_0_0.py "$OUT" examples_out_v1_1_0.json "$PY"
python3 ../ch01-deck/layout_check_v1_0_0.py "$OUT" 83
