#!/usr/bin/env bash
cd /home/claude/AdvancedProgrammingWithPython/08-tooling
P=../03-materials/ch03/page/sen0414_ch03_page_v9_92_0.html; L=ch03-page/logs_ms
ts(){ echo "$(date -u +%FT%TZ) $*" >> $L/progress_v9_92_0.log; }
ts "lock held; start diag audit"
python3 ch08-page/diag_audit_run_v9_92_0.py $P > $L/diag_audit_v9_92_0.log 2>&1; ts "diag rc=$?"
python3 ch08-page/playground_width_check_v9_92_0.py $P $L/playground_width_v9_92_0.log > $L/playground_width_stdout_v9_92_0.log 2>&1; ts "width rc=$?"
python3 sen0414_story_layout_probe_v1_0_0.py $P $L/story_layout_v9_92_0_run1.log > $L/story_probe_stdout_v9_92_0.log 2>&1; ts "story rc=$?"
PAGE_VER=9_92_0 PAGE_TEST_FILE=sen0414_page_test_v9_38_0.py python3 sen0414_page_test_run_v1_1_0.py 03 9_92_0 > $L/page_test_9_38_0_v9_92_0_run1_full_output.log 2>&1; ts "test 9.38.0 rc=$?"
python3 sen0414_lineage_chapter_check_v1_2_0.py Page/Ch03 > $L/chapter_check_Page_Ch03_v9_92_0_run1.log 2>&1; ts "chapter check (9.37.0) rc=$?"
python3 sen0414_exercise_leak_probe_v1_3_0.py /tmp/claude-0/scratch16/npm/node_modules /tmp/ms03_run/leak course_page_template_v9_53_1.html $P 4 4 1 2 3 > $L/leak_probe_v1_3_0_page_v9_92_0.log 2>&1; ts "leak rc=$?"
ts "chain done"
