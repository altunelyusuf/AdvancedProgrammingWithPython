#!/usr/bin/env python3
"""sen0414_lineage_box2_run v1_0_0 - runs the box-2 plan of the exam lineage on a newest register whose header still names the previous version (register 2.340.0 was made by a plain copy through the framework's urgency tool,
which does not move the header: its owl:versionInfo says 2.339.0). The committed 2.340.0 stays as it is; this run writes 2.341.0 with a correct header (versionInfo 2.341.0, priorVersion 2.340.0) and says so in its comment.
Usage: sen0414_lineage_box2_run_v1_0_0.py"""
import importlib.util, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
sp = importlib.util.spec_from_file_location("b2", os.path.join(here, "sen0414_lineage_exam_box2_v1_0_0.py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
W = m.W
src = W.newest(); t = open(src, encoding="utf-8").read(); cur = "%d.%d.%d" % tuple(W.ver(src))
hm = re.search(r'owl:versionInfo "([\d.]+)" ; owl:versionIRI <([^>]*)> ; owl:priorVersion <([^>]*)> ;', t)
if hm.group(1) != cur:
    base = hm.group(2).rsplit("/", 1)[0]
    t = t.replace(hm.group(0), 'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (cur, base, cur, base, hm.group(1)), 1)
nt, comment = m.plan(t)
comment += " (The register 2.340.0 kept the header of 2.339.0 because the urgency tool copies without moving it; this version's header is correct.)"
print(os.path.basename(W.write_new(src, nt, comment)))
