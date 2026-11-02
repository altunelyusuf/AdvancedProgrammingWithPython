#!/usr/bin/env python3
"""sen0414_lineage_exam_fixlinks v1_0_0 - ONE new register file: repairs the two violations that the validation of 2.388.0 found beyond the 26 of the baseline: (1) G148 on ST4_Rev (all its tasks are Done, but the repair of the print flaws is still to come: the repair task TK4_RevFix_Build is added as a child that is still to come); (2) G158 on Urgent_4 (the repair work was started by the coordinator while the interruption is still open: it is named as urgent exam work of Urgent_4, said openly)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
NS = "http://example.org/sen0414-slides-lineage#"
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now(); add = []
i = t.index("\nex:ST4_Rev a backlog:Story") + 1; j = t.find("\nex:", i + 1); b = t[i:j]
a = "backlog:decomposesInto ex:TK4_Rev_Design,"; assert a in b
t = t[:i] + b.replace(a, "backlog:decomposesInto ex:TK4_RevFix_Build, ex:TK4_Rev_Design,", 1) + t[j:]
add.append("ex:ST4_Rev backlog:hasAuditNote %s .\n" % W.lit("%s UTC: the repair task TK4_RevFix_Build of the story ST4_RevFix is named as the child that is still to come (framework ruling G148: a story whose children are all Done is Done unless a child is still to come); the story is closed after the corrections version is controlled. The task belongs to ST4_RevFix, which carries its own objective." % now))
add.append("".join("<%sUrgent_4> backlog:urgentItem <%s%s> .\n" % (NS, NS, k) for k in ("ST4_RevFix", "TK4_RevFix_Build", "TK4_RevFix_Verify")))
add.append("ex:ST4_RevFix backlog:hasAuditNote %s .\n" % W.lit("%s UTC: the Owner printed the first version at 16:50 Istanbul and the coordinator launched the corrections version at 13:58:09Z while the urgent interruption Urgent_4 was still open (the lift waits for the registration of the SEN0401 exam); as exam work it is named as an urgent item of Urgent_4 (framework ruling G158), which the lineage agent says openly: the corrections are not urgent for the sitting, and the work files are new versions that never touch the printed files." % now))
print(os.path.basename(W.write_new(src, t + "\n" + "".join(add), "Exam: the repair story linked as the child still to come of ST4_Rev and named as exam work of Urgent_4.")))
