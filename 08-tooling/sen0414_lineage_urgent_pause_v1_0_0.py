#!/usr/bin/env python3
"""sen0414_lineage_urgent_pause v1_0_0 - ONE new register file each call, through the existing urgency mechanism (urgent interruptions Urgent_3 for the chapter lineage and Urgent_4 for the exam lineage, framework ruling G158).
  pause  Records the Owner's urgent order of 2026-11-02 15:43 Istanbul (12:43Z): the exam is the urgent work (already named as urgent items of Urgent_4), all other started work is Suspended (not cancelled): the started items of the chapter lineage are held under Urgent_3 with a recorded T_Suspend move each.
  lift   Records the end of the pause: every item held by the pause moves back to In Progress by T_Resume (the Owner's order is over). Called only when the lineage agent has the coordinator's word that the pause is lifted.
Usage: sen0414_lineage_urgent_pause_v1_0_0.py pause | lift"""
__version__ = "1.0.0"
import os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
NS = "http://example.org/sen0414-slides-lineage#"; B = rdflib.Namespace("http://example.org/backlog#")
HELD = ["ST_MS_Ch04", "TK_MS_Ch04_Build", "ST_MS_Ch06", "TK_MS_Ch06_Build"]
ORDER = ("OWNER URGENT ORDER of 2026-11-02 15:43 Istanbul (12:43Z), relayed by the coordinator and recorded as relayed, recorded AFTER the delivery as the Owner ordered: 'stop all work and finish the exams within 1 to 2 hours; the owner must print them today'. The exam work is the urgent work (named as urgent items of Urgent_4); all other started work is Suspended, not cancelled and nothing waived; the page tests of Chapter 6 and every non-exam validation were not run; controls and registrations not on the exam path waited until after the delivery. Owner at 15:44: new agents may run in parallel (the Papers task was split into four parts). The Owner printed the committed PDF at 16:50 Istanbul (13:50Z).")
def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i + 1)
    return i, (len(t) if j < 0 else j)
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []; mode = sys.argv[1]
if mode == "pause":
    n = 0
    for k in HELD:
        i, j = blk(t, k); b = t[i:j]; assert "backlog:hasState backlog:InProgress" in b, k
        t = t[:i] + b.replace("backlog:hasState backlog:InProgress", "backlog:hasState backlog:Suspended", 1) + t[j:]; n += 1
        add.append('<%sUrgent_3_Hold_%d> a backlog:TransitionEvent ; backlog:transitionedItem <%s%s> ; backlog:viaTransition backlog:T_Suspend ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ; backlog:hasTransitionNote %s .\n' % (NS, 10 + n, NS, k, now, W.lit("paused at the Owner's urgent order of 2026-11-02 15:43 Istanbul (12:43Z) and recorded now (%s UTC), after the delivery: the exam is the urgent work. Suspended, not cancelled. The work was stopped in fact at about 12:43Z; a Chapter 2 page test and two Playground fixture scripts that held the page-test lock were killed as processes at about 15:56 Istanbul to free the machine (no file touched); they must be run again after the lift." % now)))
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit("SUSPENDED %s UTC (recorded late, the stop was at 12:43Z) at the Owner's urgent order of 15:43 Istanbul; Suspended, not cancelled; resumes with the lift of the pause (its executor session is stopped; the Chapter 4 lambda repair and the Chapter 6 page tests are still to do)." % now)))
    for u in ("Urgent_3", "Urgent_4"):
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (u, W.lit(ORDER))) if False else add.append("<%s%s> backlog:hasImpactNote %s .\n" % (NS, u, W.lit(ORDER))) if False else None
    for k in ("Mission4", "Lineage4", "Lineage2"):
        add.append("ex:%s backlog:hasAuditNote %s .\n" % (k, W.lit(ORDER + " Recorded through the existing mechanism: Urgent_4 (exam lineage, the exam items are its urgent items) and Urgent_3 (chapter lineage, four started chapter items held Suspended); no new interruption was declared because the tool refuses a second one on a lineage with an open one. The four chapter items are Suspended by recorded moves but are NOT named in holdsItem of Urgent_3, because they are themselves urgent items of Urgent_3: the interruption cannot be resolved while they are open, so a hold list would make the lift impossible (found by the validation, ruling G158); the moves and the lift are recorded on the items.")))
    msg = "Urgent pause recorded (four chapter items Suspended under Urgent_3; the exam items are the urgent items of Urgent_4)."
else:
    n = 0
    for k in HELD:
        i, j = blk(t, k); b = t[i:j]; assert "backlog:hasState backlog:Suspended" in b, k
        t = t[:i] + b.replace("backlog:hasState backlog:Suspended", "backlog:hasState backlog:InProgress", 1) + t[j:]; n += 1
        add.append('<%sUrgent_3_Back_%d> a backlog:TransitionEvent ; backlog:transitionedItem <%s%s> ; backlog:viaTransition backlog:T_Resume ; backlog:transitionedAt "%sZ"^^xsd:dateTime ; backlog:transitionedBy backlog:Owner ; backlog:hasTransitionNote "resumed after the exam pause: the exam is delivered (printed 2026-11-02 16:50 Istanbul) and the pause is lifted" .\n' % (NS, 10 + n, NS, k, now))
    add.append("ex:Lineage2 backlog:hasAuditNote %s .\n" % W.lit("%s UTC: the exam pause is lifted; the four chapter items held since the Owner's order resume (Chapter 4 lambda repair, Chapter 6 page tests, the Chapter 2 page test killed for the lock)." % now))
    msg = "Urgent pause lifted (four chapter items back In Progress)."
add = [a for a in add if a]
out = W.write_new(src, t + "\n" + "".join(add), msg)
print(os.path.basename(out))
