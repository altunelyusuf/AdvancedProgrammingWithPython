# COMMON text of the SEN0414 v4.0.0 briefs (part of every brief)

## Why (Owner order 2026-11-02 18:20 Istanbul = 15:20Z, urgent, relayed by the coordinator)
Deduction calculations are too complicated, even impossible by hand; each question's deduction differs; it confuses and stresses students. Simplify. The sheet with tips is 3 pages and the exam 6, together 9; the standard is 4, the maximum 6. Shorten the tips and put them on the question. "Remove the deductions and remove the bonus question, but increase the options from 4 to 5, so students get 20 points if they answer totally blindly." Hand-written answers: say how they are graded.

## The seven rulings (design v1_5_0 and everything below it)
1. No deductions of any kind: right = its points, wrong or blank = 0; no floor needed; the design alternatives A1 to A4 and every per-question penalty sentence are removed.
2. No bonus Q5. Total 100 points, equal weight per unit as far as the chapter quotas allow; the design states exactly how the points are distributed.
3. Every closed-answer unit has 5 alternatives: choice 5 options; match 5 responses per premise; order: place 1 to 5 over 5 steps; bank 5 entries. Hand-written units (number, code result) stay hand-written (blind chance about 0). Blind total is therefore slightly under 20; report the exact figure (integer-scaled DP convolution, as in revq5score). The fifth alternative is a NEW item version; every answer is recomputed by running the code; no untaught name (validator scope rule R27).
4. No tips page on the sheet. A short tip (12 words or fewer, or none) is printed on the question under the stem. A NEW validator version checks tips on the question; R20 stays unchanged in its own file.
5. Paper + sheet at most 6 pages, aim 4 or 5 (cover 1, questions 2 or 3, sheet 1). The sheet is one page and holds closed-answer units only. The question pages are the legal copy.
6. The key holds a plain ONE-page grading procedure: closed answers are read from the sheet or the question pages; hand-written results are compared with the key value (exact = full points, otherwise 0, no partial); then add; no other arithmetic.
7. Paper directions and sheet lose the penalty and Q5 sentences; the legal-copy sentence stays.

## Rules of an executor
- You are an EXECUTOR session. You do NOT touch the register (07-lineage); the lineage agent records your start and controls the result by its own re-runs.
- All work is in /home/claude/CME/exams/SEN0414/ as NEW versioned files (generated files in 04-assessment/exams/papers_r20/). No committed file is edited: design v1_3_0 (and v1_4_0 files if any), engine v1_2_1 and older, items v3_0_0 and older, marking tool v1_0_0/v1_1_0, validator v1_2_0, renderers, papers_r15/r18/r19 stay byte for byte. Nothing of the exam goes into the public repository /home/claude/AdvancedProgrammingWithPython.
- No gate is weakened. Where a rule changes (no penalty, 5 alternatives) the old rule is kept for the old files; the change is a stated, tested rule with a fixture of known answer and a fixture that proves the refused case.
- First `git pull --rebase --autostash` in /home/claude/CME. Commit ONLY your own new files; never `git add -A`; the message ends with your task identifier in parentheses; push, no force.
- Shared machine (2 cores): `nice`, no heavy parallel runs, delete your own scratch; STOP and report if free space is under 0.8 GB.
- Report every result exactly as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN; the last two are not passes). A failing result is never worked around. Never invent a term or fact. Wait inside your turn; never schedule a wake-up. Word is never measured here; say so.
- Final report: commit SHAs, new files with SHA-256, verbatim output of every check, achieved / not achieved in plain words.
- Delivery names: sen0414_exam_midterm_v4_0_0_{paper.docx,paper.pdf,key.docx,key.pdf,sheet.pdf} plus SHA256.txt.

## The parts (parallel; 1 and 2 and 3a start at once)
1. TK4_V4_1_Items: items v4_0_0 (five alternatives) and validator v1_3_0 (tips on the question).
2. TK4_V4_2_Design: design v1_5_0, engine v1_4_0 and the real build (uses a synthetic item set until part 1 commits).
3. TK4_V4_3_Score: marking tool v1_2_0, grading procedure text, exact blind figures.
4. TK4_V4_4_Render: paper, key, sheet, delivery set (prepares against a synthetic build; renders the real files when part 2's build is committed).
5. TK4_V4_5_Measure: measurement of the delivery set (starts when part 4 has committed it).
