#!/usr/bin/env python3
"""Template patch 9.22.0 (over 9.21.0):
1. Code Lab: the "Code patterns" list is gone from every editor (it pasted a pattern into whatever was already typed, which gave the SyntaxErrors); the Playground keeps its one list;
   the Code Lab examples start with ones that need only what the chapter teaches, and the ones that use dictionaries, functions and comprehensions are marked "Advanced";
2. "Enable live LLM" and the model choice are at the top of the Agents view;
3. multiple choice questions in exams and in the practice builder end with the option "None of the above" - and now and then the true statement is left out so that it is the right answer;
4. ordering lines: a drag handle (mouse, finger or Up/Down/Home/End on the keyboard), and holding the arrows keeps the line moving until they are let go;
5. the audit-log / hand-in zip button is at the top of the Exam view.
usage: template_patch_v9_22_0.py IN(9.21.0) OUT(9.22.0)"""
import sys, os
__version__ = "9.22.0"
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)
# 1 editors without the pattern list; Code Lab examples
a = s.index("(ta.id==='pcode'?'':'<select class=\"edsel\" data-edtpl"); e = s.index("</select>')+''", a) + len("</select>')+''")
s = s[:a] + "''" + s[e:]
a = s.index("const CODELAB_SNIPPETS=["); e = s.index("];\n", a) + 2
new = '''const CODELAB_SNIPPETS=[
 ['How many concepts are on this page?',"print(len(PAGE['nodes']), 'concepts')"],
 ['Print the name of every main subject',"for n in PAGE['nodes']:\\n    if n['level'] == 1:\\n        print(n['label'])"],
 ['Quiz answer key',"for q in PAGE['quiz']:\\n    print(q['q'], '->', q['options'][q['answer']])"],
 ['Re-run every example on this page',"for n in PAGE['nodes']:\\n    if n.get('io'):\\n        got = repr(eval(n['io']['code']))\\n        print('same' if got == n['io']['out'] else 'DIFFERENT', '|', n['label'], '|', n['io']['code'], '->', got)"],
 ['Advanced: concepts per subject (dictionary, function, Counter)',"from collections import Counter\\nnodes = {n['id']: n for n in PAGE['nodes']}\\ndef subject(n):\\n    while n['parent']:\\n        n = nodes[n['parent']]\\n    return n['label']\\nCounter(subject(n) for n in PAGE['nodes'] if n['level'] == 3)"],
 ['Advanced: relations by type (Counter)',"from collections import Counter\\nCounter(r['type'] for r in PAGE['relations'])"],
 ['Advanced: concepts that mention a word (list comprehension)',"word = 'string'\\n[n['label'] for n in PAGE['nodes'] if word in (n['body'] + ' ' + (n.get('definition') or '')).lower()]"]];
'''
s = s[:a] + new + s[e:]
rep("<p class=\"note\">Python with this page\\u2019s own data: <code>PAGE</code> holds its concepts, relations, quiz, objectives and references. Runs in the same background Python as the playground.</p>",
    "<p class=\"note\">Python with this page\\u2019s own data: <code>PAGE</code> holds its concepts, relations, quiz, objectives and references. Runs in the same background Python as the playground. The first examples use only what the chapter teaches; those marked <b>Advanced</b> use later material.</p>")
# 2 live LLM bar at the top of the Agents view
a = s.index("+'<div class=\"kit\">"); e = s.index("</button></div></div></div></div>';", a)
kit = s[a + len("+'"):e + len("</button></div>")]
s = s[:a] + "+'" + s[e + len("</button></div>"):]
rep("P+='<div role=\"tabpanel\" data-pane=\"agents\" hidden><div class=\"agentsview\">", "P+='<div role=\"tabpanel\" data-pane=\"agents\" hidden>" + kit + "<div class=\"agentsview\">")
rep(".agentsview{display:grid;grid-template-columns:var(--rw,192px) .5rem 1fr;gap:.3rem;height:calc(100vh - 8.5rem);min-height:26rem}", ".agentsview{display:grid;grid-template-columns:var(--rw,192px) .5rem 1fr;gap:.3rem;height:calc(100vh - 11.5rem);min-height:26rem}")
# 3 "None of the above"
rep("function xMcq(b,R){const idx=xsh(b.options.map((_,i)=>i),R);return {type:'mcq',pts:XT_PTS.mcq,concept:b.concept,level:b.level||'Understand',q:b.q,code:b.code||'',options:idx.map(i=>b.options[i]),answer:idx.indexOf(b.answer),why:b.why}}",
"""const XNONE='None of the above';
function xMcq(b,R){const idx=xsh(b.options.map((_,i)=>i),R);let opts=idx.map(i=>b.options[i]),ans=idx.indexOf(b.answer),why=b.why;
 if(!opts.some(o=>/^(none|all) of the above/i.test(String(o)))){
  if(opts.length>=4&&R()<.25){const right=opts[ans];opts.splice(ans,1);opts.push(XNONE);ans=opts.length-1;why='The true statement was left out of this list, so none of the options is correct. It was: '+right+(b.why?' '+b.why:'')}
  else opts.push(XNONE)}
 return {type:'mcq',pts:XT_PTS.mcq,concept:b.concept,level:b.level||'Understand',q:b.q,code:b.code||'',options:opts,answer:ans,why}}""")
# 4 ordering
rep("<code data-l=\"'+i+'\">", "<span class=\"exgrip\" role=\"button\" tabindex=\"0\" aria-label=\"Drag to move this line, or press Up or Down\" data-tip=\"Drag me\">\\u283F</span><code data-l=\"'+i+'\">", 2)
rep("Move a line with ▲ and ▼ until the program reads correctly.", "Drag a line by its handle \\u283F (or press Up and Down on the handle), or use ▲ and ▼ - hold one to keep the line moving - until the program reads correctly.")
rep("Move a line with the arrows until the program reads correctly.", "Drag a line by its handle \\u283F (or press Up and Down on the handle), or use the arrows - hold one to keep the line moving - until the program reads correctly.")
rep("ol.exlines code{", ".exgrip{cursor:grab;touch-action:none;user-select:none;padding:.3rem .55rem;border-radius:6px;background:var(--card);border:1px solid var(--line);font-size:1.1rem;line-height:1}.exgrip:focus-visible{outline:3px solid var(--blue)}.exgrip:active{cursor:grabbing}ol.exlines li.dragging{background:#FFD43B55;outline:2px solid var(--blue);border-radius:8px}ol.exlines li.dragging code{box-shadow:0 2px 8px #0003}\nol.exlines code{")
js = open(os.path.join(here, "template_order_v9_22_0.js"), encoding="utf-8").read()
marker = "// ---- save the code as a file, open a file into the code ----"
rep(marker, js + "\n" + marker)
# 5 the hand-in zip at the top of the Exam view
rep('<div class="row"><button class="btn g" id="xeauditzip">Download audit log (zip)</button><span class="note">What was done on this page, with your saved result files. Kept in this browser only.</span></div></div>\'}', "</div>'}")
rep('Marking happens when you finish; corrections are folded under each question.</p><div class="xid"', 'Marking happens when you finish; corrections are folded under each question.</p><div class="row xzip"><button class="btn" id="xeauditzip">Download my hand-in and audit log (zip)</button><span class="note">One zip with the result file of each exam you finished and a log of what was done on this page - hand it in, and it is read in one go. Kept in this browser until you ask for it.</span></div><div class="xid"')
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
