#!/usr/bin/env python3
"""Patches course_page_template_v9_38_0.html into course_page_template_v9_39_0.html.

One subject: the CME standard is in the corpus for provenance and SPARQL, not for answering students. Measured on the
9.27.0 chapter 1 trial page: the page-wide passage search ranked "standard: learning outcomes (course part)" and
"standard: part of a course repository" - individuals of the embedded standards-adoption ontology, which carries the
narrative-to-diagram mapping - above the course's own outcome for every wording of a course question, so the guide
cited the standard instead of the outcome. The agents' and the guide's chunks now skip blocks of kind "standard": the
blocks stay embedded (the corpus list, the SPARQL console and the diagrams' typing read them), the knowledge graph
the agents search is the book, the course, the chapter, the research record and this page, as the About pane says.
"""
__version__ = "9.39.0"
SRC, DST = "course_page_template_v9_38_0.html", "course_page_template_v9_39_0.html"
s = open(SRC, encoding="utf-8").read(); n0 = len(s)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)
rep("(await sparql(Q_TEXT)).forEach(r=>{const kind=r.g.split(':')[2];const kindOf=", "(await sparql(Q_TEXT)).forEach(r=>{const kind=r.g.split(':')[2];if(kind==='standard')return;const kindOf=", 1)
rep("<!-- course_page_template version 9.38.0:", "<!-- course_page_template version 9.39.0: the agents' knowledge graph skips the embedded CME standard (kind standard), which is in the corpus for provenance, the SPARQL console and the diagrams' typing, not for answering a student's question - it had outranked the course's own outcomes. Earlier: --><!-- course_page_template version 9.38.0:", 1)
open(DST, "w", encoding="utf-8").write(s); print("written %s (%d -> %d bytes)" % (DST, n0, len(s)))
