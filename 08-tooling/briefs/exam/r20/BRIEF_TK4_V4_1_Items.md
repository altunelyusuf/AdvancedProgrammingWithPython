# Brief part 1 of 5: TK4_V4_1_Items (executor session SEN0414-EX-v4-1)
Read COMMON_v4_0_0.md in this folder first; it is part of this brief.

## Task
1. `items/items_v4_0_0.json` (+ `items_v4_0_0_make.py`, `items_v4_0_0_check.py`, `items_v4_0_0_changes.md`, `items_v4_0_0_check_run1.log`), a NEW version made from `items/items_v3_0_0.json`:
   - Remove all Q5 (bonus) items from the exam set (keep them in v3_0_0 as history). Report which units exist and their kinds.
   - Choice and predict items: add a fifth option (a plausible distractor from taught material only; same length style; no option is "none of the above" or "all of the above"); the right letter may move; the item text names no untaught name.
   - Match: 5 responses per premise (add a fifth response); order: 5 steps (place 1 to 5); bank/cloze: 5 entries.
   - Number and code-result (hand-written) items stay hand-written; do not add alternatives.
   - Every answer is recomputed by RUNNING the code in the listing (not by reading); the check prints each recomputed answer next to the stored one.
   - The tip of each item is 12 words or fewer or empty, and sits as its own field; no tip repeats the stem.
2. `exam_item_check_v1_3_0.py`, `exam_item_check_fixtures_v1_3_0.json`, selftest log: a NEW validator copied from v1_2_0 where R01 to R19, R21 to R28 keep their rule, R20 is untouched in v1_2_0; the new file adds R30 (tip printed on the question: tip field present or empty, at most 12 words, one line, not inside the stem, no abbreviation or sheet coordinate), R31 (five alternatives per closed unit by kind) and R32 (no deduction wording anywhere in an item). Each new rule has a fixture that passes and a fixture that is refused. Run it over items_v4_0_0.json and print the failures (an empty list is the goal).
3. Taught-vocabulary scope (R27) over the new alternatives is mandatory.
Commit items first as soon as they pass.

## Done means
Items check (recomputed answers all equal), validator selftest and run over the items all PASS, committed to CME; the report lists each added alternative item by item.
