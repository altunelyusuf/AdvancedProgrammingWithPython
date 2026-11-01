#!/usr/bin/env python3
"""sen0414_lineage_brief_exam6 v1_0_0 - executor briefs r11 for TK4_Engine5 and TK4_Items_A2: the r10 brief plus the settled decisions after the controller's verdicts on TK4_Points5 and TK4_ItemRules2 (register 2.357.0). New files in 08-tooling/briefs/exam/r11; r10 stays.
Usage: sen0414_lineage_brief_exam6_v1_0_0.py"""
__version__ = "1.0.0"
import os
here = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(here, "briefs/exam/r10"); out = os.path.join(here, "briefs/exam/r11"); os.makedirs(out, exist_ok=True)
SHAPE = """## Settled by the lineage agent after the controller's verdicts (r11; these replace anything in the brief below that says otherwise)
1. RECORD SHAPE of match and order: ONE record per sub-question, never one per premise. The controlled validator `04-assessment/exams/exam_item_check_v1_1_0.py` already fixes it: R01 counts 22 fields per record, R23 makes `question`, `sub`, `type` and `points` agree, the points belong to the sub-question, and R10 requires for a `match` record `options_or_blanks` as an object with 5 premises and 7 answers and `answer` as a list of 5 different letters A to G, and for an `order` record `options_or_blanks` as a list of four steps and `answer` as a permutation of 1 to 4. The engine and the item sets take and give exactly these records; the points of a match or order sub-question are whole numbers for the whole record. If you find that this cannot work, STOP and report; do not invent a second shape.
2. CHAPTER 5: the critical-points file now exists and is controlled: `04-assessment/exams/critical_points_ch05_v1_0_0.json` (44 points: 22 slide, 1 speaker note, 18 corpus, 3 story) and `critical_points_ch05_not_found_v1_0_0.md`. The validator reads it by itself. The points name deck v3.1.0; a newer chapter 5 deck is being built and is not committed: cite only what the file cites and do not guess slide numbers of the newer deck. Prefer the 23 slide and speaker-note points for chapter 5 items; use a corpus or story point only when the item says so in `source`.
3. ABBREVIATIONS (R21): the 24 short forms of the validator's registry carry standard expansions that were NOT checked against the course. Use a short form only after writing its full form once at first use, in print order over the whole paper; and report in your final report the list of short forms you used, so the Owner can confirm the expansions in one line each.
4. The validator v1_1_0 is controlled by the lineage agent (66 fixtures, self-tests of v1_0_0 and v1_1_0, its own mutations of a valid item). Run `exam_item_check_v1_1_0.py selftest` first and `check` on your records last; a FAIL stays a FAIL.

"""
for k in ("TK4_Engine5", "TK4_Items_A2"):
    t = open(os.path.join(src, "BRIEF_%s.md" % k), encoding="utf-8").read(); head, _, rest = t.partition("\n\n**")
    open(os.path.join(out, "BRIEF_%s.md" % k), "w", encoding="utf-8").write(head + "\n\n" + SHAPE + "**" + rest)
    print("wrote", k)
