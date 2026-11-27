#!/usr/bin/env python3
"""Template 9.56.0 = 9.55.0 + the owner's rulings of 2026-11-27 (urgency case on chapter 11, applied to every chapter).
1. The slide source code tab sits under Lab, named Slide source code: large resizable editor, slide number beside each
   example, walk-through block by block on the same code, hidden set-up for each example, recorded results where an example cannot run.
2. A finished exam shows its answers: the button is always Open result and answers; a review rebuilds the questions from the exam
   code when the stored snapshot is gone; corrections are open under each question.
3. Mock exam and quiz questions test course content and code, never book metadata: nodes about the practice section, edition
   changes and errata are left out of every question pool, and so are question-bank items about them.
usage: template_patch_v9_56_0.py IN(9.55.0) OUT(9.56.0)"""
import sys, os, json, re
__version__ = "9.56.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
spec = json.load(open(os.path.join(here, "template_slidecode_ops_v1_0_0.json"), encoding="utf-8"))
# 1 the tab moves from Learn to Lab
g = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"; lab = "lab:[['play','▶ Playground'],"
rep(g, ""); rep(lab, lab + "...(CC.length?[['chaptercode','💻 Slide source code']]:[]),")
rep("</body>", spec["walk_script"] + "</body>")
for op in spec["ops"]:
    rep(op["old"], op["new"])
# 3 the meta nodes and items are left out of every pool
rep("const BANK=(()=>{try{return JSON.parse(document.getElementById('qbank').textContent)||[]}catch(e){return[]}})(),BSEEN=new Set();",
    "const XMETAIDS=new Set(['PracticeWork','PracticeQuestions','PracticePrograms','PracticeProgram','PracticeProgramsAndAnswers','BookAndPractice','WorkingVocabulary','EditionChange','SecondEditionContent','BookCorrections','Questions']),XMETATEXT=/practice|chapter|reader|subject cover|questions answered|vocabulary|textbook|\\bbook\\b|edition|errata/i;\n"
    "const BANK=(()=>{try{return (JSON.parse(document.getElementById('qbank').textContent)||[]).filter(b=>!(XMETAIDS.has(b.concept)&&XMETATEXT.test(String(b.q||'')+' '+(b.options||[]).join(' ')+' '+String(b.why||''))))}catch(e){return[]}})(),BSEEN=new Set();")
a = "qUnder=id=>{const r=[];const w=i=>qKids(i).forEach(k=>{r.push(k.id);w(k.id)});w(id);return r};"
rep(a, a + "\nconst XMETANODES=new Set(D.nodes.filter(n=>XMETAIDS.has(n.id)||((n.label==='Programs'||n.label==='Questions')&&XMETAIDS.has(n.parent))).map(n=>n.id));")
rep("cids:xsh([top.id].concat(qUnder(top.id)),R)", "cids:xsh([top.id].concat(qUnder(top.id)).filter(i=>!XMETANODES.has(i)),R)")
rep("if(!scope||scope==='all')return D.nodes.map(n=>n.id);return [scope].concat(qUnder(scope))",
    "if(!scope||scope==='all')return D.nodes.map(n=>n.id).filter(i=>!XMETANODES.has(i));return [scope].concat(qUnder(scope)).filter(i=>!XMETANODES.has(i))")
rep("const ids=scope&&scope!=='all'?[scope].concat(qUnder(scope)):D.nodes.map(n=>n.id);return xsh(ids,R)",
    "const ids=(scope&&scope!=='all'?[scope].concat(qUnder(scope)):D.nodes.map(n=>n.id)).filter(i=>!XMETANODES.has(i));return xsh(ids,R)")
rep("<!-- course_page_template version 9.55.0", "<!-- course_page_template version 9.56.0 (new file over 9.55.0; Owner's ruling of 2026-11-27, urgency case on chapter 11, for all chapters): the Slide source code tab under Lab with a large resizable editor, slide numbers and walk-through; a finished exam always opens with its answers; no question about book metadata -->\n<!-- course_page_template version 9.55.0")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
