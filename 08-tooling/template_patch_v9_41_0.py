#!/usr/bin/env python3
"""Patches course_page_template_v9_40_0.html into course_page_template_v9_41_0.html.

One subject: an individual whose own name is a line of code. The audit rule F-B4 (9.24.0) named worked examples and error
cases by what they show and moved their code to the card; it reached the individuals an owner links to with has...Example
or has...Condition. Measured on the 9.27.0 chapter 4 page: 64 of the chapter's 94 individuals are the concept instances
themselves (X_DefStatement "def hello():", "lambda a, b: a + b", "a def inside a def"), which no such edge reaches, so 17
boxes of the taxonomy's individuals layer read as code. The same rule now applies to them: an individual with no role
whose label reads as code is named by its class ("Def statement (instance)", numbered when a class has several) and its
code goes to the card, where the F-B4 card already shows it.
"""
__version__ = "9.41.0"
SRC, DST = "course_page_template_v9_40_0.html", "course_page_template_v9_41_0.html"
s = open(SRC, encoding="utf-8").read(); n0 = len(s)
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:100])
    s = s.replace(a, b)
rep("  const used=new Map();[...N.values()].forEach(x=>{const k=String(x.label||'').toLowerCase();used.set(k,(used.get(k)||0)+1)});\n",
    "  const used=new Map();[...N.values()].forEach(x=>{const k=String(x.label||'').toLowerCase();used.set(k,(used.get(k)||0)+1)});\n"
    "  // 9.41.0 - a concept instance named by a line of code is named by its class instead, before the examples it owns take their names from it; the code goes to the card\n"
    "  const CODEY=/__import__|lambda |exec\\(|\\bdef |\\(\\)|^[a-z_]+\\.[a-z_]+\\(|=|\\bprint\\(|\\bexcept\\b|\\braise\\b|\\bimport\\b|\\btry\\b|\\breturn\\b|\\bassert\\b|\\bwhile\\b|\\bfor\\b.*\\bin\\b|:$|^Traceback/;\n"
    "  [...N.values()].forEach(x=>{if(x.kind!=='individual'||x.role||!CODEY.test(String(x.label||'')))return;const kcls=N.get(cls.get(x.id));if(!kcls)return;x.code=x.code||x.label;let lab=String(kcls.label||'').trim()+' (instance)';const k=lab.toLowerCase();used.set(k,(used.get(k)||0)+1);if(used.get(k)>1)lab+=' ('+used.get(k)+')';x.label=lab;x.role='instance'});\n", 1)
rep("<!-- course_page_template version 9.40.0:", "<!-- course_page_template version 9.41.0: a concept instance whose own name is a line of code is named by its class in the taxonomy and the code shown in the card (the F-B4 rule reaching the instances no owner edge links). Earlier: --><!-- course_page_template version 9.40.0:", 1)
open(DST, "w", encoding="utf-8").write(s); print("written %s (%d -> %d bytes)" % (DST, n0, len(s)))
