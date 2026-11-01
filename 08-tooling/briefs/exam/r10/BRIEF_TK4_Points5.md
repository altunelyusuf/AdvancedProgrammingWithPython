# Brief for the executor session SEN0414-EX-points5

Task TK4_Points5 (written by the lineage agent for the exam change of 2026-11-01; the blocker was found by the design executor). Executor session name: **SEN0414-EX-points5**. Estimated 1.0 hours (an estimate, G120).

## Why this work exists
The printed SEN0414 exams (midterm and make-up, 60 minutes, physical paper) are built from the critical points the instructor explained. The Owner's instruction of 2026-11-01 (relayed): chapters 1-4 and 5-8, so chapter 5 (Debugging) is now part of the exams (his statement of 2026-10-29 had excluded it; the coordinator asked him once); the design v1_2_0 gives it 3 sub-questions. Critical-points files exist for chapters 1-4 and 6-8; none for chapter 5. This task makes it, in the same format and by the same method.

## Rules of an executor
- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The lineage agent writes it, records your start and runs the control after you report.
- A committed file is never edited: every output is a new file with a new version number. No existing tool, test, template, deck, page, research file or bank is edited.
- A FAILING RESULT IS NEVER WORKED AROUND. NOT_MEASURED, CANNOT_RUN and a skip are not passes. Report every result exactly as printed.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- First `git pull --rebase --autostash` in /home/claude/AdvancedProgrammingWithPython. Commit your work to main with a clear message that ENDS with the task identifier in parentheses, for example `(TK4_Points_A)` (the controller finds your commits by it); no force push; pull --rebase before push. Commit and push each verified step at once: the repository (committed and pushed work) is the only record if a container restarts.
- The machine has 2 cores shared with other sessions: do not start heavy parallel runs; delete stale temporary folders of your own older than 60 minutes (the root disk is small).
- Never write or keep personal data of students; any example student, sheet or name is synthetic and says so.
- Never invent a term, a fact or a source: if the course does not say it, you do not write it. Where you cannot find something, say so plainly in the place the task names for it.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed or could not be found, if anything.

## The task
**Collect the critical points of chapter 5 (Debugging) from the deck, speaker notes, corpus and stories, and list what could not be found**

Chapter 5 now belongs to the exams (the coordinator assumed it in and asked the Owner once), and the design v1_2_0 gives it 3 sub-questions, but no critical-points file exists for it: the chapters 1 to 4 and 6 to 8 have theirs (TK4_Points_A and TK4_Points_B). Write 04-assessment/exams/critical_points_ch05_v1_0_0.json (a list of objects with exactly the keys chapter (the integer 5), point, why_critical, source_file, place, evidence_kind, as in critical_points_ch06_08_v1_0_0.json) and 04-assessment/exams/critical_points_ch05_not_found_v1_0_0.md (a plain list of what you looked for and could not find or confirm as the instructor's own emphasis, as questions the Owner can answer in one line each). At least 4 points, 8 or more if the chapter supports them; read the newest committed deck of chapter 5 and its speaker notes (03-materials/ch05/SEN0414_Ch05_Debugging_3e_v*.pptx; the chapter-5 build executor is producing a newer deck: use the newest committed at your start and name its version), the corpus 08-tooling/sen0414_ch05_corpus_v*.py and the stories 08-tooling/sen0414_ch05_stories_v*.py (newest of each; if a file does not exist say so in the not-found list), and the chapter's ontology under 03-materials/ch05/rdodi for what the chapter names as common mistakes. A point is critical when the deck stresses it, the notes explain it at length, or the corpus or a story ties it to a common mistake. Every place must exist (slide number in range; notes present; a quoted fragment of at most 120 characters found in the file). New files only; nothing under 03-materials is changed. Estimated 1.0 hours (an estimate, G120).

Depends on: nothing

The format and the method are those of `04-assessment/exams/critical_points_ch06_08_v1_0_0.json` and its not-found list: read them first. The controller's checks (you do not run them) are the ones that checked those files: exact keys, chapter 5 only, at least 4 points, every source file exists, every place exists (slide in range, notes present, quoted fragment of at most 120 characters found), a chapter 5 section in the not-found list, only new files in your commits, everything committed. Commit message ends with `(TK4_Points5)`.

