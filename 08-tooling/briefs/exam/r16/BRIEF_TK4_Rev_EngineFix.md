# Brief for the executor session SEN0414-EX-rev-enginefix

Task TK4_Rev_EngineFix (story ST4_Rev), written by the lineage agent. Executor session name: **SEN0414-EX-rev-enginefix**. Estimated 0.7 hours of agent work (an estimate; the real start is the instant the coordinator gives from `date -u`). Do not start until TK4_Rev_SheetText_Verify is Done in the register (the lineage agent tells the coordinator): you need the sheet wording file `exam_sheet_wording_v1_0_0.json` that task writes.

## Why this work exists
The controller ran the engine v1.2.0 (commit 9c17e3e, private CME repository) on the real single-form item set `items/items_v3_0_0.json` (commit 2fa152b) and found two defects, both in the engine and not in the items:
1. The engine still imports the item validator v1_1_0 for rule E02 (and the abbreviation scan), which does not know the new field `answer_format`. The real item set is refused by E02 alone; with the validator v1_2_0 wired in (in the controller's own process only) the same engine builds the paper from the same items with every rule E01 to E34 passing, seed 1.
2. Rule E33 requires that the answer sheet carries the SAME legal-copy sentence as the directions. The task TK4_Rev_SheetText gives the sheet its own sentence (file `exam_sheet_wording_v1_0_0.json`: the official answers are those on the question pages; the sheet is only for faster checking), because the design's sentence read on the sheet contradicts itself. As written, E33 would refuse the first correct paper.

## The task
New files only, in `/home/claude/CME/exams/SEN0414/04-assessment/exams/` (nothing in the public repository; no committed file is edited; engine v1_2_0, its shapes, fixtures and check stay as committed):
1. `exam_engine_v1_2_1.py`: a copy of v1_2_0 in which (a) the item validator is `exam_item_check_v1_2_0.py` (R01 to R29, which needs `SEN0414_ROOT=/home/claude/AdvancedProgrammingWithPython`; the engine passes the root through as it already does for `--root`), and (b) rule E33 checks that the directions hold the design's legal-copy sentence word for word, that the sheet specification carries the sentence of `exam_sheet_wording_v1_0_0.json` word for word, and that every question has its one penalty sentence in the directions. No other rule changes; no rule is weakened (E02 must still refuse an unknown extra field and a missing answer_format; add a fixture for each).
2. New shapes file only if the SHACL text of E33 has to change (`exam_engine_shapes_v1_2_1.ttl`), new fixtures `exam_engine_fixtures_v1_2_1.json` and its build script, and `exam_engine_check_v1_2_1.py` (a copy of check v1_2_0 that runs the new fixtures, the v1_2_0 fixtures again and the v1_1_0 fixtures again; nothing that passed may change its verdict except the two rules above, and each such change is listed with the reason).
3. Prove with the real items: build from `items/items_v3_0_0.json`, design `exam_design_v1_3_0.json`, seeds 1, 2 and 3, with `SEN0414_ROOT` set: every rule E01 to E34 passes; report the verbatim output of each build and the build record's scoring table (30 units, exact blind gain 0).
4. Run the new check completely (it is long: run it niced, never beside page tests, and wait inside your turn); report every line as printed.

## Done means (the controller re-runs all of these itself)
- The check v1_2_1 prints RESULT PASS with no MISMATCH; the three real builds are accepted; a pool with a record that has an unknown extra field is refused by E02; a sheet carrying the design's sentence instead of the wording file's is refused by E33; the v1_1_0 and v1_2_0 fixtures behave as before except the two named rules.
- All files committed to CME (pull --rebase --autostash, push, no force).

## Rules of an executor
- You are an EXECUTOR session. You do NOT touch the register (07-lineage); the lineage agent records your start and controls your result by its own re-runs.
- First `git pull --rebase --autostash` in /home/claude/CME. Commit ONLY your own new files; never `git add -A`; message ends with the task identifier in parentheses.
- The machine is shared (2 cores): no heavy parallel runs; delete your own scratch when done; STOP and report if free space falls under 0.8 GB.
- Report every result exactly as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN; the last two are not passes). A failing result is never worked around.
- Never invent a term or fact. Wait inside your turn for results; never schedule a wake-up.
- Final report to the coordinator: commit SHAs, new files, the verbatim output of every check, achieved / not achieved in plain words.
