#!/usr/bin/env python3
"""Exam lineage 4, event 'close_backlog COMMIT': fills the Backlog stage output's closedAtCommit and records the Owner's decision of 2026-10-30 on the chapter lists as an audit note on the lineage.
Builds on sen0414_lineage_exam_v1_1_0.py (unchanged)."""
import sys, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("ex11", os.path.join(here, "sen0414_lineage_exam_v1_1_0.py")); X = importlib.util.module_from_spec(sp); sp.loader.exec_module(X)
W = X.W
NOTE = ("OWNER DECISION 2026-10-30 (relayed by the course coordinator): the chapter lists keep their defaults. SEN0414 is examined over chapters 1 to 8 without chapter 5 (Debugging), "
        "and the SEN0401 exam work uses chapters 1 to 6. This fixes the chapter list that the mission leaves to the instructor; the mission wording is unchanged. "
        "Chapter 5 stays complete as chapter material and receives no further work.")
def main():
    commit = sys.argv[1]; src = W.newest(); t = open(src, encoding="utf-8").read()
    t = X.fill_prev(t, "Backlog", commit)
    t += "\nex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit(NOTE)
    print(os.path.basename(W.write_new(src, t, "closedAtCommit of the Backlog stage output of the exam lineage set (%s); the Owner's decision of 2026-10-30 on the chapter lists recorded." % commit)))
main()
