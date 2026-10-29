#!/usr/bin/env python3
"""Exam briefs, version 1.2.0: runs sen0414_lineage_brief_exam_v1_1_0.py (unchanged) into 08-tooling/briefs/exam/r3 and appends the Owner's ruling of 2026-10-30 on the interactive pages' questions to every brief."""
import os, sys, subprocess
here = os.path.dirname(os.path.abspath(__file__)); tgt = sys.argv[1] if len(sys.argv) > 1 else "ALL"
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "briefs", "exam", "r3")
subprocess.run([sys.executable, os.path.join(here, "sen0414_lineage_brief_exam_v1_1_0.py"), tgt, out], check=True)
R = ("\n## Ruling of 2026-10-30 on the interactive pages' questions (the Owner's, relayed)\n"
     "'Interactive page questions are accessible by the students before the exam. They are chapter subject specific questions, rarely cross-section. It is not wise to use them directly, but they can be a seed for better questions and enhancement iterations.' "
     "So: no exam item is a page item or a near copy of one; page items are seeds for new, better items, each linked to its seed and to the course points it tests; cross-chapter, synthesis and reasoning items are authored. "
     "In your task: where you cite or list bank items, mark them as seeds, never as exam items. ")
R_DESIGN = ("In the design you state: (a) the item model's seed link (field seed_item, the page item it grew from, or none) and course-point link; (b) the similarity method that decides 'near copy' (name the measure, the threshold and why, for example shared word sequences of the stem and the options and the same answer; it must be computable by a tool and checkable on a fixture whose answer is known); (c) what an enhancement iteration changes in a seed (a new angle, a cross-chapter link, a reasoning step, a changed code case) so the result tests the critical point and not memory of the page. "
            "A rule in SHACL and its fixture are built later from your design.\n")
for t in os.listdir(out):
    if not t.startswith("BRIEF_"): continue
    p = os.path.join(out, t); s = open(p, encoding="utf-8").read(); i = s.find("\n## Order of work")
    add = R + (R_DESIGN if "Design" in t else "\n")
    open(p, "w", encoding="utf-8").write(s[:i] + add + s[i:] if i > 0 else s + add)
print("briefs in", out)
