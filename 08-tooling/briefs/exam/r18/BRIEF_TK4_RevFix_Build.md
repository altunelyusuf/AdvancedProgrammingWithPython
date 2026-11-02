# Brief for the executor session SEN0414-EX-rev-fix1

Task TK4_RevFix_Build (story ST4_RevFix), written by the lineage agent. Executor session name: **SEN0414-EX-rev-fix1**. Estimated 2.0 hours of agent work (an estimate; the real start is the instant the coordinator gives from `date -u`). This is NOT urgent: the Owner chose at 16:50 Istanbul (13:50Z) to print the committed PDF of the first version, and these flaws go into a corrections version.

## Why this work exists
The first printed version (paper PDF SHA-256 ace81060e1dee43102406893ef439080d70e89f5d4b14cfc6f9384f70cd86da8, key, 2-page sheet; CME commits up to 2a62393) was measured by part 4 (`papers_r15/exam_papers_measure_v1_0_0_log.txt`) and controlled by the lineage agent. It is fit to print but has these known flaws:
1. The sheet header says "form code 10100", a five-digit number the student never fills; the paper does not mention it, so a student may try to copy it. The line above row F reads "Give the code of one bank word.", which does not fit the form mark. The paper says "in the row marked F, fill the number 00".
2. The 30 answer labels and answer-format sentences on the question pages are set at 9.5 pt; the rule is 10 pt or larger for all body text (the footer, 8.5 pt, is allowed).
3. The last question page has 11.5 pt of slack (a safe margin is about 40 pt): Word, which was not available to measure, may add a sixth page. Part 4 found that moving sub-question 4f onto page 4 would give the room; 4f is 162.7 pt tall and page 4 has 89.3 pt free, so about 79 pt more room on page 4 is needed.
4. The cover has 3 glyphs of the Owner's template 0.55 pt past the right margin (the grey code-box shading ends 2.4 pt past the margin line).
5. The sheet footer text box ends 0.40 pt below the bottom margin line (no ink does), and sheet page 1 has an orphan "it." alone on a line at the end of the penalty sentence.

## The task
Make a corrections version as NEW files in `/home/claude/CME/exams/SEN0414/` (new version numbers; the files of the first version, design v1_3_0, engine v1_2_1, the validator and the marking tool stay as committed and are not edited); nothing in the public repository; the Owner's cover template is read only and is never copied into any repository.
1. Sheet text: a new wording file `exam_sheet_wording_v1_1_0.json` (the single source, as v1_0_0 was). It fixes the header (no printed five-digit "form code" that looks like something to fill, or the same number explained in plain words on the sheet), and the line above row F (it must say what the student does there: fill the form mark 00 in this row, matching the paper's sentence word for word where the paper states it). These sentences are the lineage agent's default and Owner wording points: implement them as written and say so in your report. Build sheet v2.2.0 from it (new renderer file, new check) with the sheet at 2 pages, 31 places, the glyphs inside the margins, the footer box inside the bottom margin line, and no orphan line (check that no line of the penalty sentence holds a single word).
2. Paper type: answer labels and format sentences at 10 pt or larger (new renderer version).
3. Last page slack of at least 40 pt in LibreOffice: reach it by layout, with 4f moving to page 4 (reduce spacing and the empty room of page 3, which is half empty because Question 3 starts a new page: Question 3 may start on page 3 after Question 2 instead if the layout permits; no sub-question is split across pages; the code lines stay whole). Do not change any question, key letter, point value or the engine's build: the build files must stay byte for byte the same as the first version's (compare SHA-256) unless a wording change forces a new build, and then every engine rule E01 to E34 must pass and the key letters against the printed options must be re-read.
4. Cover: no glyph past the margin by more than 0.1 pt, without editing the template (the renderer sets the table width or the cell margin).
5. Page budget stays 7 (paper 5 or fewer, sheet 2).

## Done means (the controller re-runs all of these itself)
- The measure tool (a new version of `exam_papers_measure_v1_0_0.py` if its limits are re-stated; the old one is not edited) prints no FAIL and no RISK; Word stays NOT_MEASURED and is said so.
- Paper 5 pages or fewer, answer spaces 30, sheet 2 pages and 31 places, sheet and paper agree word for word on every shared sentence, the marking tool gives 110 for all right and 0 for all blank on the real key, the reader still reads every fixture sheet exactly.
- Paper type 10 pt or larger, last-page slack of at least 40 pt, cover overshoot at most 0.1 pt, footer box inside the margin line, no orphan line on the sheet.
- No exam file and no copy of the template in the public repository.
- All files committed to CME (pull --rebase --autostash, push, no force).

## Rules of an executor
- You are an EXECUTOR session. You do NOT touch the register (07-lineage); the lineage agent records your start and controls your result by its own re-runs.
- First `git pull --rebase --autostash` in /home/claude/CME. Commit ONLY your own new files; never `git add -A`; message ends with the task identifier in parentheses.
- The machine is shared (2 cores): no heavy parallel runs; delete your own scratch when done; STOP and report if free space falls under 0.8 GB.
- Report every result exactly as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN; the last two are not passes). A failing result is never worked around.
- Never invent a term or fact. Wait inside your turn for results; never schedule a wake-up.
- Final report to the coordinator: commit SHAs, new files, the verbatim output of every check, achieved / not achieved in plain words.
