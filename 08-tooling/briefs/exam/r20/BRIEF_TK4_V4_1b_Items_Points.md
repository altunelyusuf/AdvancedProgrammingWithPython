# Brief part 1b of 5: TK4_V4_1b_Items_Points (executor session SEN0414-EX-v4-1b)
Read COMMON_v4_0_0.md and ADDENDUM_1.md in this folder first; they are part of this brief.

## Task
1. NEW `items/items_v4_0_1.json` (+ `items_v4_0_1_make.py`, `items_v4_0_1_check.py` as copies of the v4_0_0 files changed only for the version, `items_v4_0_1_changes.md`, `items_v4_0_1_check_run1.log`), made from `items/items_v4_0_0.json`. The ONLY change: Q4a points 16 -> 15 (3 per place) and Q4b points 4 -> 5. Every other field of every record is byte for byte equal; print a field-by-field comparison with v4_0_0 that shows exactly these two differences.
2. Rerun the items check (all answers recomputed by running the code) and the validator `exam_item_check_v1_3_0.py check items/items_v4_0_1.json`; print the results as they are. Total must be 100, each question 25, and every scoring unit (one per gap, premise, place, or choice or number item) must carry whole points: print the table.
3. Commit as soon as it passes; new files only; v4_0_0 and the validator stay unchanged. Estimated 0.2 hours.

## Done means
Check and validator PASS on items_v4_0_1.json, comparison with v4_0_0 shows two differences, committed to CME.
