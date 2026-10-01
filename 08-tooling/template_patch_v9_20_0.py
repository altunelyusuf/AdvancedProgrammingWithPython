#!/usr/bin/env python3
"""Template 9.20.0 = 9.19.0 + the owner's review of chapter 1 (2026-10-01):
1. a link "All chapters" to index.html in the header (the chapter pages and the index sit in one folder);
2. the Playground has ONE list: this chapter's examples and the code patterns; every pattern is complete and runs as it is (the old toolbar
   "Templates" list inserted fragments with an empty slot, such as "while :", which returned errors); the toolbar list stays in the Code Lab and the exercise editors, now with runnable patterns too;
3. on a phone the header wraps instead of pushing the text-size buttons off the screen (the page was 472 px wide on a 390 px screen);
4. an audit log (page opened, exams started and finished, result files saved, release codes tried, data cleared) that can be downloaded as a .zip with the saved results;
5. light theme only: the dark-mode block is gone;
6. a clear option that asks first, offers the audit zip before anything is removed, and records that it was used.
usage: template_patch_v9_20_0.py IN(9.19.0) OUT(9.20.0)"""
import sys, os, re
__version__ = "9.20.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
# 1 index link
rep("<h1>__TITLE__</h1>", '<h1>__TITLE__</h1><a class="idxlink" href="index.html" title="Back to the list of chapters (index.html in the same folder)">⌂ All chapters</a>')
# 2 patterns that run
a = s.index("const ED_TPL=["); b = s.index("\n", a)
tpl = [("For loop over numbers", 'for i in range(5):\n    print(i)'), ("For loop over a list", 'for item in ["a", "b", "c"]:\n    print(item)'),
 ("While loop", 'n = 3\nwhile n > 0:\n    print(n)\n    n -= 1'), ("If, elif, else", 'x = 5\nif x > 10:\n    print("big")\nelif x > 3:\n    print("medium")\nelse:\n    print("small")'),
 ("Function with a docstring", 'def double(x):\n    """Return x doubled."""\n    return x * 2\n\nprint(double(4))'), ("Class with __init__", 'class Dog:\n    def __init__(self, name):\n        self.name = name\n\nprint(Dog("Rex").name)'),
 ("Try and except", 'try:\n    int("abc")\nexcept ValueError as e:\n    print("Problem:", e)'), ("Write a file, then read it line by line", 'with open("data.txt", "w") as f:\n    f.write("one\\ntwo\\n")\nwith open("data.txt") as f:\n    for line in f:\n        print(line.rstrip())'),
 ("List comprehension", 'result = [x for x in range(10) if x % 2 == 0]\nprint(result)'), ("Dictionary comprehension", 'result = {k: v for k, v in {"a": 1, "b": 2}.items()}\nprint(result)'),
 ("Count words with a dictionary", 'counts = {}\nfor word in "to be or not to be".split():\n    counts[word] = counts.get(word, 0) + 1\nprint(counts)'), ("Ask for a number (7 if left empty)", 'n = int(input("Enter a number: ") or 7)\nprint(n * 2)'),
 ("Print with an f-string", 'name = "Ada"\nprint(f"Hello, {name}!")'), ("Sort with a key", 'result = sorted(["pear", "fig", "apple"], key=lambda x: len(x))\nprint(result)'),
 ("Check with assert", 'x = 3\nassert x > 0, "x must be positive"\nprint("ok")'), ("Main guard", 'def main():\n    print("hello")\n\nif __name__ == "__main__":\n    main()')]
import json
s = s[:a] + "const ED_TPL=" + json.dumps([list(t) for t in tpl], ensure_ascii=False) + ";" + s[b:]
old = "<select class=\"edsel\" data-edtpl aria-label=\"Insert a code template\"><option value=\"\">Templates</option>'+ED_TPL.map((t,i)=>'<option value=\"'+i+'\">'+esc(t[0])+'</option>').join('')+'</select>'"
rep(old, "'+(ta.id==='pcode'?'':'<select class=\"edsel\" data-edtpl aria-label=\"Insert a code template\"><option value=\"\">Code patterns</option>'+ED_TPL.map((t,i)=>'<option value=\"'+i+'\">'+esc(t[0])+'</option>').join('')+'</select>')+''")
rep("if(id==='pex'){const v=e.target.value;document.getElementById('pcode').value=v==='first'?D.course.playground.code:byId[v].io.code;fitViews()}",
    "if(id==='pex'){const v=e.target.value;document.getElementById('pcode').value=v==='first'?D.course.playground.code:v.slice(0,4)==='tpl:'?ED_TPL[+v.slice(4)][1]:byId[v].io.code;fitViews()}")
rep("if(t.id==='pload'){const v=document.getElementById('pex').value;document.getElementById('pcode').value=v==='first'?D.course.playground.code:byId[v].io.code;return}",
    "if(t.id==='pload'){const v=document.getElementById('pex').value;document.getElementById('pcode').value=v==='first'?D.course.playground.code:v.slice(0,4)==='tpl:'?ED_TPL[+v.slice(4)][1]:byId[v].io.code;return}")
# 3 css
rep(".fsctl{margin-left:auto;", ".idxlink{color:#fff;border:1px solid #ffffff66;border-radius:8px;padding:.25rem .6rem;font-size:.85rem;font-weight:600;text-decoration:none;white-space:nowrap}.idxlink:hover,.idxlink:focus-visible{background:#ffffff22}\n.xid{margin:.5rem 0}\n.fsctl{margin-left:auto;")
rep("@media (max-width:700px){.fsctl button{min-width:2.2rem}}",
    "@media (max-width:700px){.fsctl button{min-width:2rem}#fsReset{display:none}.titlebar{flex-wrap:wrap;gap:.2rem;row-gap:.25rem}.titlebar{flex-wrap:nowrap;gap:.1rem}header.top{padding:.35rem .4rem}.titlebar button,.titlebar .idxlink{min-width:30px}.fsctl{gap:.1rem}.fsctl button{padding:.2rem .35rem;min-width:30px}.navgrp button{padding:.2rem .3rem;min-width:30px}.titlebar h1{flex:1 1 0;min-width:0;order:-3;font-size:.9rem;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.titlebar .explore{order:-4;min-width:36px;min-height:36px}#srchBtn{font-size:0;padding:.2rem .5rem}#srchBtn::before{content:'\\1F50D';font-size:1rem}.idxlink{font-size:0;padding:.2rem .5rem;min-height:2rem;display:inline-flex;align-items:center}.idxlink::before{content:'\\2302';font-size:1.15rem}.navgrp button{min-width:2rem}#progBadge{font-size:.8rem}}\n@media (max-width:340px){#progBadge{display:none}}\n@media (max-width:520px){.titlebar h1{display:none}.titlebar .navgrp{margin-left:auto}}\n@media (min-width:701px) and (max-width:1000px){.titlebar{flex-wrap:wrap;row-gap:.25rem}}")
# light theme only (owner rule): the dark-mode block is removed
m = re.search(r"@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme=\"light\"\]\)\{[^\n]*\}\}\n", s)
assert m, "dark block"
s = s[:m.start()] + s[m.end():]
rep(":root{--ink:#1F2933;", ":root{color-scheme:light;--ink:#1F2933;")
# 4/5 audit, clear
js = open(os.path.join(here, "template_audit_v9_20_0.js"), encoding="utf-8").read()
marker = "// ---- save the code as a file, open a file into the code ----"
rep(marker, js + "\n" + marker)
rep("if(t.id==='xeclear'){e.stopImmediatePropagation();XS.recs=[];XS.items={};xSave();xHistPaint();return}", "if(t.id==='xeclear'){e.stopImmediatePropagation();xClearAsk();return}")
rep('id="xeclear">Clear my list</button>', 'id="xeclear">Clear my exam data…</button>')
rep('<div id="xehist"></div></div>', '<div id="xehist"></div><div id="xeclearbox"></div><div class="row"><button class="btn g" id="xeauditzip">Download audit log (zip)</button><span class="note">What was done on this page, with your saved result files. Kept in this browser only.</span></div></div>')
rep("items:items,answers:rec.ans||[],answered:", "items:items,labels:xLabels(items,rec.ans||[]),answers:rec.ans||[],answered:")
# 7 the Code pipeline view is removed: it did not suit every program, and it made a second, different list of examples next to the Playground's
rep("['pipeline','\U0001F3ED Code pipeline'],", "")
a = s.index("P+='<div role=\"tabpanel\" data-pane=\"pipeline\" hidden>"); e = s.index("</div></div>';\n", a) + len("</div></div>';\n")
assert "ppnext" in s[a:e] and s[a:e].count("data-pane=") == 1, "pipeline pane bounds"
s = s[:a] + s[e:]
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
