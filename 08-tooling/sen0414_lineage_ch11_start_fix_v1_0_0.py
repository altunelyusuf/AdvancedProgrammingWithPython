#!/usr/bin/env python3
"""sen0414_lineage_ch11_start_fix v1_0_0 - corrects the recorded start of TK_Ret_Ch11_Research from 2026-10-26T06:08:00 to 06:07:00 (the coordinator read the clock at 06:07 UTC just before launching the executor and gave 05:58 and then 06:08 by mistake). The earlier register files stay as committed; this new file carries the corrected instant on the task (startedAt), on its start transition (transitionedAt) and on the brief instance (instantiatedAt), and an audit note that names the correction and its reason."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_lineage_standard_v1_2_0 as W
src = W.newest(); t = open(src, encoding="utf-8").read(); now = W.now()[:19]
OLD, NEW = "2026-10-26T06:08:00", "2026-10-26T06:07:00"
def blk(name):
    i = t.index("\nex:%s a backlog:" % name) + 1; j = t.find("\nex:", i); return i, (len(t) if j < 0 else j)
cnt = 0
for name in ("TK_Ret_Ch11_Research", "Begin2T_TK_Ret_Ch11_Research"):
    i, j = blk(name); b = t[i:j]; nb = b.replace('"%s"^^xsd:dateTime' % OLD, '"%s"^^xsd:dateTime' % NEW); cnt += b.count('"%s"^^xsd:dateTime' % OLD); t = t[:i] + nb + t[j:]
m = re.search(r'(ex:\w+) a backlog:ExecutorBrief[^\n]*\n(?:[^\n]*\n)*?[^\n]*instantiatedAt "%s"\^\^xsd:dateTime' % re.escape(OLD), t)
for mm in re.finditer(r'\n(ex:\w*Ch11_Research\w*) a backlog:[A-Za-z]+ ;', t):
    i = mm.start() + 1; j = t.find("\nex:", i); b = t[i:j]
    if 'instantiatedAt "%s"^^xsd:dateTime' % OLD in b:
        t = t[:i] + b.replace('"%s"^^xsd:dateTime' % OLD, '"%s"^^xsd:dateTime' % NEW) + t[j:]; cnt += 1; break
assert cnt >= 3, cnt
note = ("CORRECTION of the start instant, made on %s UTC: the coordinator gave 2026-10-26T06:08 and had read the clock at 06:07 UTC just before launching the executor (a first instant, 05:58, was also wrong), so the real start is 2026-10-26T06:07:00. The earlier versions 2.260.0 to 2.262.0 stay as committed and carry 06:08; this version carries 06:07 on the task, its start transition and its brief instance. The commit 576b617 of the executor is dated 06:09:29 UTC, 2.5 minutes after the corrected start, which is still short for the work reported (a page ABox of 930 lines, a compare tool and nine chapter-check runs): the controller notes it and does not rule on it; the dates of the commits are the executor's machine clock." % now)
t += "\nex:TK_Ret_Ch11_Research backlog:hasAuditNote %s .\n" % W.lit(note)
print(os.path.basename(W.write_new(src, t, "correction of the start instant of the chapter 11 research from 06:08 to 06:07 (the coordinator's reading of the clock)")))
