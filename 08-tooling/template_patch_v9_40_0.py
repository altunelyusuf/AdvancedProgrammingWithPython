#!/usr/bin/env python3
"""Patches course_page_template_v9_39_0.html into course_page_template_v9_40_0.html.

One subject: the chosen entity's labels in the ERD. Choosing an entity lifts its relationships and draws their labels
in full even where the fitted view left them out; measured on the 9.27.0 chapter 1 page with the Arithmetic operation
section chosen (14 relationships), 10 of its labels were drawn at their lines' midpoints over one another, because the
search for a free spot stopped two steps from the line. For a label that must be shown the search now goes on - four
and six steps to either side - before the midpoint fallback, and the fallback is marked so a reader sees it is crowded.
"""
__version__ = "9.40.0"
SRC, DST = "course_page_template_v9_39_0.html", "course_page_template_v9_40_0.html"
s = open(SRC, encoding="utf-8").read(); n0 = len(s)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)
rep("if(!pick){if(!full)return;const d=dim(text.length);", "if(!pick&&full){for(const o of [42,-42,56,-56,72,-72]){for(const f of F){pick=spot(f,o,txt.length);if(pick)break}if(pick)break}}if(!pick){if(!full)return;const d=dim(text.length);", 1)
rep("<!-- course_page_template version 9.39.0:", "<!-- course_page_template version 9.40.0: a chosen entity's labels, which must be shown, search further from their lines before falling back to the midpoint. Earlier: --><!-- course_page_template version 9.39.0:", 1)
open(DST, "w", encoding="utf-8").write(s); print("written %s (%d -> %d bytes)" % (DST, n0, len(s)))
