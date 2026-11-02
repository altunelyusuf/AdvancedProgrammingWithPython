#!/usr/bin/env python3
"""sen0414_lineage_exam_leak_decision v1_0_0 - records (ONE new register file) the Owner's decision on the exposed exam material: option (a), make the repository private (relayed by the coordinator; the visibility change itself is not yet done - the proxy refuses settings writes - and is asked of the Owner in GitHub settings). The guard stays in force; a history rewrite is NOT decided.
Usage: sen0414_lineage_exam_leak_decision_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
NOTE = ("OWNER DECISION of 2026-11-02 on the exposed exam material (his real answer, relayed by the course coordinator and recorded as relayed): option (a), make the repository private. Not yet done at this recording: the coordinator cannot change the visibility (the proxy refuses settings writes) and has asked the Owner to do it in GitHub settings; the item is closed only when the visibility is private, which the controller checks with the repository API. In force until then and after: the .gitignore guard and the rule that no new exam keys, answer data or final papers are pushed. NOT decided: any rewrite of the history or removal of files already pushed (option b) and the building of new papers (option c); each needs its own Owner decision and then becomes a new task. Copies taken while the repository was public stay taken.")
def main():
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []
    for k in ("ST4_Leak", "TK4_Leak_Guard", "TK4_Leak_Guard_Verify"): add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(NOTE)))
    add.append("ex:Lineage4 backlog:hasAuditNote %s .\n" % W.lit("%s UTC: the Owner chose (a) make the repository private for ST4_Leak (relayed); the visibility change is the Owner's action in GitHub settings; the guard stays in force; history rewrite not decided." % now))
    out = W.write_new(src, t + "\n" + "".join(add), "Exam change: the Owner's decision on ST4_Leak (make the repository private; relayed), guard stays, history rewrite not decided.")
    print(os.path.basename(out))
main()
