# Brief part 3 of 5: TK4_V4_3_Score (executor session SEN0414-EX-v4-3)
Read COMMON_v4_0_0.md first; it is part of this brief.

## Task
1. NEW `exam_scoring_alternatives_v1_2_0` is NOT needed (no alternatives remain). Make a NEW marking tool `exam_marking_tool_v1_2_0.py` (+ fixtures, check, log) copied from v1_1_0: score = sum of points of the units answered exactly right; wrong or blank = 0; no floor; hand-written units exact string/number compare with the key value, no partial. Fixtures of known answer (all right = 100, all blank = 0, all wrong = 0, mixed). The old rules A1 to A4 stay in the old file; the new file refuses to be given a penalty.
2. Exact blind figures: integer-scaled DP convolution over the units of the design (use the unit list from `papers_r20/build` when part 2 has committed it; before that use the points table you derive from design rules in COMMON and mark it provisional). Report mean (just under 20), sd, and the probability of at least 20, 30, 40 points blind; also the figure for a student who guesses only the closed units.
3. The grading procedure text `grading_procedure_v4_0_0.md`: ONE page when printed, plain words, no jargon: (a) closed answers are read from the sheet or, if the sheet is missing, from the question pages; (b) hand-written results are compared with the key value, exact = full points, otherwise 0, no partial; (c) add the points; (d) no other arithmetic. It answers "how are hand-written answers graded?" in the first lines. Part 4 puts it into the key.
4. A check that the tool, the procedure and the design agree (units, points, 100 total).
Commit as soon as it passes.

## Done means
Tool check, fixtures, DP figures reproduced by a second independent method (Monte Carlo of one million draws within 0.05 of the exact mean), committed to CME.
