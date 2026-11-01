#!/usr/bin/env python3
"""sen0414_lineage_owner_note v1_0_0 - records an Owner statement as relayed, as audit notes on named items (a NEW file; ONE new register version).
Usage: sen0414_lineage_owner_note_v1_0_0.py docx      (the Owner's statement of 2026-10-30 13:15 Istanbul: papers also as editable MS Word)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
assert sys.argv[1:2] == ["docx"], __doc__
WORD = ("OWNER STATEMENT of 2026-10-30 at 13:15 Istanbul (10:15 UTC), relayed by the course coordinator and recorded as relayed: 'Not PDF, MS Explorer for edit option.' Read, and confirmed by the coordinator, as: the SEN0414 exam papers are also delivered as editable MS Word documents (.docx), not only as PDF. "
        "Scope recorded: the paper and its printed key are rendered as .docx from the same data as the PDF (the assembler's build record, forms A and B, key data); the answer sheet stays position-exact and its format is a decision pending with the Owner (a bubble grid read by the SEN0401 reader cannot be edited freely without losing its geometry). "
        "Effect on the work in the box: none on the item pools or the near-copy rule or the design (items are data records); it adds to the scope of the paper-rendering story, whose tasks are made at the planning of the box after box 2, and to the checks of that story (the .docx opens and its text equals the build record).")
src = W.newest(); t = open(src, encoding="utf-8").read(); L = []
for k in ("Mission4", "Scope4", "ST4_Papers"):
    assert "\nex:%s a backlog:" % k in t, k
    L.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(WORD)))
print(os.path.basename(W.write_new(src, t + "\n" + "".join(L), "The Owner's statement of 13:15 Istanbul recorded: the exam papers also as editable MS Word (.docx); the answer sheet's format pending with the Owner.")))
