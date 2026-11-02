# Brief for the executor session SEN0414-EX-rev-sheettext

Task TK4_Rev_SheetText (story ST4_Rev), written by the lineage agent. Executor session name: **SEN0414-EX-rev-sheettext**. Estimated 0.5 hours of agent work (an estimate; the real start is the instant the coordinator gives from `date -u`).

## Why this work exists
The controller's run of the answer sheet v2.0.0 (commit 9f74ac1 in the private CME repository) found one contradiction: the design's legal-copy sentence is printed word for word on page 1 of the answer sheet, and read there it says "Write every answer in the answer space on these pages. These pages are your official answers. The answer sheet is only for faster checking. If the two differ, these pages count." On the sheet, "these pages" means the sheet itself, which is the opposite of what the Owner ordered: the legal copy is the answers on the QUESTION pages, and the answer sheet is only an option. The sentence on the question pages (top of question page 1) is correct and stays.

## The task
Make sheet v2.1.0 as NEW files in `/home/claude/CME/exams/SEN0414/08-tooling/exam/` (and a data file in `/home/claude/CME/exams/SEN0414/04-assessment/exams/`); nothing in the public repository; no committed file is edited (v2.0.0 files, design v1_3_0 and every earlier file stay as committed).
1. New file `exam_sheet_wording_v1_0_0.json` in `04-assessment/exams/` holding the sentence the answer sheet prints, as the single source: "The official answers are the ones you write in the answer spaces on the question pages. This answer sheet is only for faster checking. If the two differ, the question pages count." (three sentences; plain words; no abbreviation; no sheet coordinate), with a note that it replaces the design's sentence ON THE SHEET ONLY (the sentence for the question pages is unchanged). This wording is the lineage agent's default and an Owner wording point: implement it as written and say so in your report.
2. New `sen0414_exam_answersheet_v2_1_0.py` (copy of v2_0_0 that reads the sentence from that file) and a new check `sen0414_exam_answersheet_check_v2_1_0.py` (copy of check v2_0_0) that compares the printed sentence with the file word for word, plus builds of the four fixture sheets as new files in `sheet_v2_1/`.
3. The header must still fit page 1 with the larger sentence: every glyph inside the margins, type 10 point or larger, the grid unchanged (31 places), page 2 unchanged (tips page; no bubbles).
4. Run the new check (all its checks, as before) and the old check v2_0_0 on the new fixtures where it applies; report both outputs verbatim.

## Done means (the controller re-runs all of these itself)
- The check v2_1_0 prints SUMMARY with every check PASS; the four fixture PDFs, layouts and specs exist; the printed sentence on page 1 equals the file's sentence; no glyph outside the margins; 2 pages.
- The reader still reads every fixture exactly (reader checks of v2_0_0 repeated on the new fixtures).
- All files committed to CME (pull --rebase --autostash, push, no force).

## Rules of an executor
- You are an EXECUTOR session. You do NOT touch the register (07-lineage); the lineage agent records your start and controls your result by its own re-runs.
- First `git pull --rebase --autostash` in /home/claude/CME. Commit ONLY your own new files; never `git add -A`; message ends with the task identifier in parentheses.
- The machine is shared (2 cores): no heavy parallel runs; delete your own scratch when done; STOP and report if free space falls under 0.8 GB.
- Report every result exactly as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN; the last two are not passes). A failing result is never worked around.
- Never invent a term or fact. Wait inside your turn for results; never schedule a wake-up.
- Final report to the coordinator: commit SHAs, new files, the verbatim output of every check, achieved / not achieved in plain words.
