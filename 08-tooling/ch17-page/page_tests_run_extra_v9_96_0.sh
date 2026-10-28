#!/bin/bash
# Extra run 6 of page test 9.37.0 and of Page/Ch17 on page v9_96_0 (run 3 of 9.37.0 ended with a Playwright timeout waiting for #xefinish, no [FAIL] line, no results.json; one more run to have five completed runs). Same method as page_tests_run_v9_96_0.sh.
# Every log is kept; results.json of each page-test folder is copied to test_results_v9_96_0_<name>_runN.json before the folder is removed (only folders this script's TMPDIR holds).
# Usage: TMPDIR=<own folder> page_tests_run_v9_96_0.sh
set -u
R=/home/claude/AdvancedProgrammingWithPython; T=$R/08-tooling; H=$T/ch17-page; L=$H/logs_iter20; cd $R
grab() { # name
  d=$(ls -dt "$TMPDIR"/page_test_* 2>/dev/null | head -1)
  if [ -n "$d" ] && [ -f "$d/results.json" ]; then cp "$d/results.json" "$H/test_results_v9_96_0_$1.json"; fi
  [ -n "$d" ] && rm -rf "$d"
  echo "disk free: $(df -BM --output=avail / | tail -1)" >> "$L/page_tests_progress_v9_96_0_extra.log"
}
free_ok() { a=$(df -BM --output=avail / | tail -1 | tr -dc 0-9); [ "$a" -ge 900 ]; }
P=$L/page_tests_progress_v9_96_0_extra.log
step() { # name, cmd...
  n=$1; shift
  free_ok || { echo "STOP: free disk under 0.9 GB before $n" >> $P; exit 3; }
  echo "$(date -u +%FT%TZ) start $n" >> $P
  ( time flock /tmp/page_test.lock "$@" ) > "$L/$n.log" 2>&1; rc=$?
  echo "$(date -u +%FT%TZ) end $n rc=$rc" >> $P; grab "$n"
}
for i in 6; do
  step page_test_9_37_0_v9_96_0_run${i}_full_output env PAGE_TEST_FILE=sen0414_page_test_v9_37_0.py python3 $T/sen0414_page_test_run_v1_1_0.py 17 9_96_0
  step chapter_check_Page_Ch17_v9_96_0_run${i} python3 $T/sen0414_lineage_chapter_check_v1_2_0.py Page/Ch17
done
echo "$(date -u +%FT%TZ) ALL DONE" >> $P
