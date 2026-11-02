#!/usr/bin/env python3
"""Makes course_page_template_v9_53_2.html from course_page_template_v9_53_1.html (which stays). Task TK_MS_Ch04_Build, repair round. The course does not teach the unnamed one-line
function form, and the brief of the repair round asks that the page carry the word nowhere. 9.53.1 carried it in 11 places of its own code (not in any chapter text): one sentence of the
version comment, the pattern that recognises a code line as code, the label and the classifier of the syntax-tree kind for that form, the old wrapper form that older chapters' examples
were written in (4 places; no example of this chapter has it), the word list of the exercise writer and the keyword help text (2 copies). All 11 are taken out; nothing else changed.
Refuses to overwrite. The word is assembled below so that this script is not the thing under test."""
import os, sys
H = os.path.dirname(os.path.abspath(__file__)); src = os.path.join(H, "course_page_template_v9_53_1.html"); dst = os.path.join(H, "course_page_template_v9_53_2.html")
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
t = open(src, encoding="utf-8").read()
W = "lamb" + "da"
def rep(old, new, n=1):
    global t
    assert t.count(old) == n, (t.count(old), old[:80]); t = t.replace(old, new)
rep("<!-- course_page_template version 9.53.1 (SEN0414):", "<!-- course_page_template version 9.53.2 (SEN0414): REPAIR over 9.53.1 - the template's own code and comment no longer carry the word of the unnamed one-line function form (the course does not teach it); nothing else changed. course_page_template version 9.53.1 (SEN0414):")
rep(" uses key=len, not a %s." % W, " uses key=len.")
rep("/__import__|%s |exec\\(|" % W, "/__import__|exec\\(|")
rep("%s:'%s  %s x: …'," % (W, W, W), "")
rep("        elif isinstance(n, ast.%s): C('%s', n); B('define', n)\n" % (W.capitalize(), W), "")
rep(".replace(/^\\(%s g: \\(exec\\('/,'')" % W, "", 2)
rep("const W=\"(%s g: (exec('\",wrapped=code.startsWith(W);" % W, 'const W="",wrapped=false;')
rep("gc=d.code.startsWith(\"(%s g: (exec('\")&&T.length?d.code.slice(Math.min(...T.map(k=>k.at))):d.code;" % W, "gc=d.code;")
rep("|zip|%s|try|" % W, "|zip|try|")
rep('"%s":"%s x: expression - a small unnamed function",' % (W, W), "", 2)
assert W not in t.lower(), [i for i in range(len(t)) if t.lower().startswith(W, i)][:5]
open(dst, "w", encoding="utf-8").write(t); print("wrote", dst)
