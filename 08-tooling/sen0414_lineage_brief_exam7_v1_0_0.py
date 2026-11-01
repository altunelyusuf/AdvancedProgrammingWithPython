#!/usr/bin/env python3
"""sen0414_lineage_brief_exam7 v1_0_0 - briefs r12: the r11 brief of TK4_Engine5 plus an addendum, and the r10 brief of TK4_Items_B2 plus the settled decisions, after the controller's verdict on TK4_Items_A2 (commit 94e08e1). New files in 08-tooling/briefs/exam/r12; r10 and r11 stay."""
__version__ = "1.0.0"
import os
here = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(here, "briefs/exam/r12"); os.makedirs(out, exist_ok=True)
SET = """## Settled by the lineage agent after the controller's verdict on set A (r12; these correct the wording of r11 where they differ)
1. UNITS AND RECORDS. The design's 30 sub-questions are UNITS: one gap of a blank or cloze bank, one premise of a match, one step of an order, one choice (mcq or predict). An item RECORD is the printed item: one bank, one match set (5 premises, 7 answers), one order set (4 steps), or one choice. Its `points` are the sum of the points of its units; its `id` is question plus the record letter (not the design's unit letter). The units per question must add to the design counts: Q1 6, Q2 7, Q3 7, Q4 6, Q5 4, and the points per question to 25, 25, 25, 25 and 10. Set A holds, per list, Q1 6 units, Q2 7 (a bank of 4 gaps and a cloze of 3), Q3 6 (a match of 5 and one choice), Q4 5 (an order of 4 and one choice), Q5 2 of 4: so 1 unit of Q3 (one choice, 5 points), 1 unit of Q4 (one choice, 5 points) and 2 units of Q5 (2 points each, 4 in all) are still to write. The design JSON and its check do not change: they plan the units; the engine counts units from the records (`gaps`, number of `premises`, number of `steps`, 1) and compares them with the design.
2. LISTS. One list holds one record per id (R02) and ids follow question plus sub (R23); neither rule changes. A form therefore reads its own list: the engine takes one list per form (the paper list, the make-up list), each complete and valid on its own; it may take several files and refuses a list with a repeated id. Set A has `items_a_v2_0_0.json` (paper) and `items_a_v2_0_0_makeup.json` (make-up).
3. SET A is controlled (14 records per list, validator 0 failures on the controller's own call, Apply and above 13 of 14, Analyze and above 7 of 14, chapters 1 to 8, no identical stems). Its answer keys of blank and cloze are 0-based positions in the bank; match answers are letters; order answers give the place of each printed step. Choice letters are uneven (A 3, B 5, C 8, D 4); the engine permutes options per form. The near-copy tool reads only the old fields, so the check runs it on a built view; `seed_item` is `none` everywhere because set A was not copied from a page item.
4. ABBREVIATIONS to confirm with the Owner in one line each: JSON = JavaScript Object Notation, IDE = integrated development environment (and the earlier 24 of the registry).

"""
ENG = SET.split("3. SET A")[0] + "(Points 3 and 4 concern the item sets.)\n\n"
def mk(src, name, add):
    t = open(os.path.join(here, "briefs/exam", src, "BRIEF_%s.md" % name), encoding="utf-8").read(); head, _, rest = t.partition("\n\n")[0], None, t.partition("\n\n")
    head = t.split("\n\n")[0]; body = t[len(head) + 2:]
    open(os.path.join(out, "BRIEF_%s.md" % name), "w", encoding="utf-8").write(head + "\n\n" + add + body); print("wrote", name)
mk("r11", "TK4_Engine5", ENG)
mk("r10", "TK4_Items_B2", SET.replace("(r12; these correct the wording of r11 where they differ)", "(r12)") + """5. YOUR SCOPE: write `items_b_v2_0_0.json` (paper list) and `items_b_v2_0_0_makeup.json` (make-up list), each holding only the records still missing from set A: Q3 one choice (record Q3c, 5 points), Q4 one choice (Q4c, 5 points) and Q5 two further choices (Q5c and Q5d, 2 points each; the design JSON gives their chapters, 6 and 7, and the chapters of the open units of Q3 and Q4, which you must read there), so that set A plus set B in each list make 30 units with the right points. Then check the merged list (A plus B, by id) with the validator v1_1_0, check the units against the design, and the near-copy rule of B against A in both directions and of the make-up against the paper. The merged list must have no repeated id.

""")
