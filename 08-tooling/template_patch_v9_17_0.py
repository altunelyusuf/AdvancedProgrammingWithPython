#!/usr/bin/env python3
"""Template 9.17.0 = 9.16.0 + a working, readable ERD (owner report 2026-10-01: the ERD view did not show its detail).
Cause, found by a real mouse click (the earlier test used a synthetic event): the diagram's own drag takes pointer capture on every press except on a short list of node kinds, and the ERD entities and the graph's syntax and behaviour nodes were not on it, so their click was delivered to the svg.
Fix: those kinds are on the list; the ERD handler also runs in the capture phase; the chosen entity is marked; the layout is narrower (990 wide, not 1180) so its text is larger at the same width.
usage: template_patch_v9_17_0.py IN(9.16.0) OUT(9.17.0)"""
import sys, re
__version__ = "9.17.0"
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b):
    global s
    assert s.count(a) == 1, (s.count(a), a[:70])
    s = s.replace(a, b)
pos = {'subject': (20, 30), 'topic': (280, 30), 'concept': (540, 30), 'behaviour': (800, 30), 'syntax': (280, 250), 'example': (540, 250), 'book': (800, 250)}
for k, (x, y) in pos.items():
    s, n = re.subn(r"(\n " + k + r":\{)x:\d+,y:\d+", r"\g<1>x:%d,y:%d" % (x, y), s); assert n == 1, k
rep("const BW=210,LH=16;const H=520,W=1180;", "const BW=160,LH=16;const H=400,W=990;")
rep("translate(30,470)", "translate(20,385)")
rep("'is written with']", "'written with']")
rep("if(g)oeInfo(g.dataset.ent)});", "if(g){e.stopImmediatePropagation();oeInfo(g.dataset.ent)}},true);")
rep("function oeInfo(k){const e=OE_ENT[k];", "function oeInfo(k){const e=OE_ENT[k];document.querySelectorAll('#oerd .oe-e').forEach(x=>x.classList.toggle('sel',x.dataset.ent===k));")
rep(".onto svg .oe-r line,", ".onto svg .oe-e.sel rect{stroke:var(--blue);stroke-width:3}.onto svg .oe-r line,")
# the cause found by a real click: the diagram's own drag takes pointer capture on every press except on a few marked kinds of node, so the click of an unlisted kind is delivered to the svg, not to the node.
rep("if(e.target.closest('g.n,g.gn,g.on,[data-c],[data-oid]'))return;", "if(e.target.closest('g.n,g.gn,g.on,[data-c],[data-oid],[data-gid],[data-ent]'))return;")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
