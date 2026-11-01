#!/usr/bin/env python3
"""sen0414_lineage_brief_points5 v1_0_0 - executor brief r10 for TK4_Points5 (critical points of chapter 5), made from the Points_B brief r2 (same format, same rules) with the chapter and the Owner's statements adapted. Usage: sen0414_lineage_brief_points5_v1_0_0.py"""
import os, re
here = os.path.dirname(os.path.abspath(__file__)); repo = os.path.dirname(here)
s = open(os.path.join(here, "briefs/exam/r2/BRIEF_TK4_Points_B.md"), encoding="utf-8").read()
import importlib.util
src = open(os.path.join(here, "sen0414_lineage_control_exam3_v1_0_0.py"), encoding="utf-8").read()
m = re.search(r"^SPEC5 = (\(.*?\))\nVER5", src, re.S | re.M); SPEC5 = eval(m.group(1))
head = "# Brief for the executor session SEN0414-EX-points5\n\nTask TK4_Points5 (written by the lineage agent for the exam change of 2026-11-01; the blocker was found by the design executor). Executor session name: **SEN0414-EX-points5**. Estimated 1.0 hours (an estimate, G120).\n\n"
i = s.index("## Rules of an executor"); j = s.index("## The task")
rules = s[i:j]
why = ("## Why this work exists\nThe printed SEN0414 exams (midterm and make-up, 60 minutes, physical paper) are built from the critical points the instructor explained. The Owner's instruction of 2026-11-01 (relayed): chapters 1-4 and 5-8, so chapter 5 (Debugging) is now part of the exams (his statement of 2026-10-29 had excluded it; the coordinator asked him once); the design v1_2_0 gives it 3 sub-questions. "
       "Critical-points files exist for chapters 1-4 and 6-8; none for chapter 5. This task makes it, in the same format and by the same method.\n\n")
task = "## The task\n**%s**\n\n%s\n\nDepends on: nothing\n\nThe format and the method are those of `04-assessment/exams/critical_points_ch06_08_v1_0_0.json` and its not-found list: read them first. The controller's checks (you do not run them) are the ones that checked those files: exact keys, chapter 5 only, at least 4 points, every source file exists, every place exists (slide in range, notes present, quoted fragment of at most 120 characters found), a chapter 5 section in the not-found list, only new files in your commits, everything committed. Commit message ends with `(TK4_Points5)`.\n\n" % (SPEC5[0], SPEC5[2])
os.makedirs(os.path.join(repo, "08-tooling/briefs/exam/r10"), exist_ok=True)
open(os.path.join(repo, "08-tooling/briefs/exam/r10/BRIEF_TK4_Points5.md"), "w", encoding="utf-8").write(head + why + rules + task)
print("written")
