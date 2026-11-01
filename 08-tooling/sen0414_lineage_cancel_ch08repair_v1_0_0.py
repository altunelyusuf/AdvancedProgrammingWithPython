#!/usr/bin/env python3
"""sen0414_lineage_cancel_ch08repair v1_0_0 - cancels the held page repair of chapter 8 (ST_CI5_Page_Ch08 with TK_CI5_Page_Ch08_Repair and its Verify) as SUPERSEDED by page v9_92_1.
Recorded as a RetrospectiveFinding with the as-is fit-gap and the closure statement, plus the withdraw transitions (timestamps with Z). The coordinator's direction of 2026-11-01 (no owner question)."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
lit = W.lit
WHY = ("SUPERSEDED. AS-IS FIT-GAP (measured 2026-10-30 and 2026-11-01 by the lineage agent): the repair asked for a NEW page of chapter 8 that restores the warnings state after every program (page v9_91_0). ACCOMPLISHED: page v9_91_0 exists (committed), and the urgent Chapter 8 work then produced page v9_92_1 on template 9.53.1 "
       "(page test 9.38.0 run 1 PASS with 418 features passed and 0 failed; diagram audit, Playground width probe and story-layout probe PASS; controlled on the lineage agent's own runs from register 2.337.0 on), which contains the content of v9_91_0 and the warnings repair and adds full screen, a resizable panel, the deck's code as one tab in slide order and no lambda. "
       "FAILED: nothing the repair asked for remains unmet. IN PROGRESS: the repair task was started 2026-10-29T13:02:52, then held by the urgent interruption of 2026-10-30 and left unresumed; no executor works on it. DUE: nothing; what it would still do (a page on template 9.52.4) would produce a page older than v9_92_1 and be thrown away. "
       "CLOSURE STATEMENT: the story and its tasks end CANCELLED (superseded by ex:ST_U8_Page, page v9_92_1); the objective Obj2_StdPages is moved by the urgent story, not by this one. No gate is weakened and nothing is waived: the controls the repair's Verify task would have run (page test 9.37.0, probes, chapter check) are run on v9_92_1 by the urgent story's verification.")
REMEDY = ("The three items are Cancelled with a rationale (transitions ex:Cancel_TK_CI5_Page_Ch08_Repair, ex:Cancel_TK_CI5_Page_Ch08_Repair_Verify, ex:Cancel_ST_CI5_Page_Ch08). Recorded as a finding and not as a ChangeRequest with a ScopeChange: "
          "a ScopeChange must name an item it admits and nothing is admitted here (the replacement ex:ST_U8_Page is an urgent item, and the urgency shape G158 forbids a scope change to admit an urgent item). The as-is fit-gap and the closure statement are in the root cause. "
          "The course coordinator directed this on 2026-11-01: gaps are handled through change management, no owner question.")
def main():
    src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now()
    out = ["\nex:Finding_Ch08RepairSuperseded a backlog:RetrospectiveFinding ;\n    rdfs:label \"The held repair of the Chapter 8 page was superseded by page v9.92.1 and is cancelled\"@en ;\n"
           "    backlog:belongsToLineage ex:Lineage2 ; backlog:relatesToWorkItem ex:ST_CI5_Page_Ch08 ; backlog:relatesToWorkItem ex:TK_CI5_Page_Ch08_Repair ; backlog:relatesToWorkItem ex:TK_CI5_Page_Ch08_Repair_Verify ; backlog:hasFindingScope backlog:Scope_Methodology ;\n"
           "    backlog:hasRootCause %s ;\n    backlog:hasRemedy %s .\n" % (lit(WHY), lit(REMEDY))]
    for k, via, frm in (("TK_CI5_Page_Ch08_Repair", "T_WithdrawInProgress", "InProgress"), ("TK_CI5_Page_Ch08_Repair_Verify", "T_WithdrawReady", "Ready"), ("ST_CI5_Page_Ch08", "T_WithdrawInProgress", "InProgress")):
        i = t.index("\nex:%s a backlog:" % k) + 1; j = t.find("\nex:", i); b = t[i:j]
        assert "backlog:hasState backlog:%s" % frm in b, (k, frm)
        t = t[:i] + b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled ; backlog:hasRationale %s" % lit("Cancelled " + now + " UTC: superseded by page v9_92_1 (see ex:Finding_Ch08RepairSuperseded for the as-is fit-gap and the closure statement)."), 1) + t[j:]
        out.append('ex:Cancel_%s a backlog:TransitionEvent ; rdfs:label "%s cancelled as superseded"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:%s ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n    backlog:hasTransitionNote %s .\n' % (k, k, k, via, now, lit("Cancelled as superseded; see ex:Finding_Ch08RepairSuperseded.")))
    print(os.path.basename(W.write_new(src, t + "\n" + "\n".join(out), "Held Chapter 8 page repair (ST_CI5_Page_Ch08, TK_CI5_Page_Ch08_Repair and its Verify) cancelled as superseded by page v9_92_1; finding ex:Finding_Ch08RepairSuperseded with the as-is fit-gap and closure statement.")))
main()
