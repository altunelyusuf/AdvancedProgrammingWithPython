"""Makes course_page_template_v9_16_0.html from v9_15_0. Usage: template_patch_v9_16_0.py <in.html> <out.html>
9.16.0 (the owner's request of 2026-09-30 17:29): (1) the Taxonomy is now the tree with its leaves (classes nested by kind, worked examples and matching book
concepts as leaves); the Ontology graph is a real graph with three kinds of relation - meaning (kind of), syntax (what each example is written with, read by
Python's parser) and behaviour (what each example does, by rule) - and two more forms of the ontology are added: a class diagram and an entity-relationship
diagram; (2) code boxes save to a .py file and open one (button, or drop a file); (3) corrections are folded under the question until asked for;
(4) mock exams: every exam is kept in a list (My exams), can be reviewed with its answers and corrections, retaken, or replaced by an alternative exam;
(5) a new question type: complete the program - a given program with marked parts left to write, tips and notes on request, marked by running it."""
import sys, os, re, json
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)
def between(a, b, new):
    global s
    i = s.index(a); j = s.index(b, i)
    s = s[:i] + new + s[j:]

rep("<!-- course_page_template version 9.15.0:", "<!-- course_page_template version 9.16.0: taxonomy tree with leaves, ontology graph (meaning, syntax, behaviour), class diagram, ERD, save/open code, folded corrections, exam list with review and alternatives, complete-the-program questions. Earlier: --><!-- course_page_template version 9.15.0:")

CSS = r"""/* 9.16.0: ontology views, exam list, folded corrections */
.onto svg .ge{stroke-width:1.2;opacity:.6;fill:none}.onto svg .ge.me{stroke:var(--mute)}.onto svg .ge.sy{stroke:#1A7F37}.onto svg .ge.be{stroke:#B08900;stroke-width:1.6}
.onto svg.has-sel .ge.dim{opacity:.05}.onto svg.has-sel .ge.sel{opacity:1;stroke-width:2.8}.onto svg.has-sel g.dim{opacity:.22}.onto svg g.sel rect{stroke-width:3}
.onto svg .og-c rect{fill:var(--card);stroke:var(--blue);stroke-width:1}.onto svg .og-c.lv1 rect{fill:var(--navy);stroke:var(--navy)}.onto svg .og-c.lv1 text{fill:#fff;font-weight:700}.onto svg .og-c.lv2 rect{fill:var(--yellow);stroke:#B08900}
.onto svg .og-c text,.onto svg .og-k text{font:12px Calibri,Arial,sans-serif;fill:var(--ink);pointer-events:none}.onto svg .og-c.lv1 text{fill:#fff}
.onto svg .og-k rect{fill:var(--panel);stroke-width:1.8}.onto svg .og-k.sy rect{stroke:#1A7F37}.onto svg .og-k.be rect{stroke:#B08900}.onto svg .og-c,.onto svg .og-k,.onto svg .oc-b,.onto svg .oe-e{cursor:pointer}
.onto svg .colh{font:700 12px Calibri,Arial,sans-serif;fill:var(--mute);letter-spacing:.06em;pointer-events:none}
.onto svg g:focus-visible rect{stroke:var(--blue);stroke-width:3}
.onto svg .oc-b rect{fill:var(--panel);stroke:var(--ink);stroke-width:1.2}.onto svg .oc-b.lv1 rect{fill:var(--card)}.onto svg .oc-b text{font:12px Calibri,Arial,sans-serif;fill:var(--ink);pointer-events:none}.onto svg .oc-b .oc-h{font-weight:700;font-size:13px}.onto svg .oc-b .oc-st{fill:var(--mute);font-size:11px}.onto svg .oc-b .oc-k{fill:var(--mute);font-style:italic;font-size:11px}.onto svg .oc-b line{stroke:var(--ink);stroke-width:1}.onto svg .oc-e{stroke:var(--ink);stroke-width:1.2}
.onto svg .oe-e rect{fill:var(--panel);stroke:var(--ink);stroke-width:1.3}.onto svg .oe-e .oe-hd{fill:var(--navy)}.onto svg .oe-e .oe-t{fill:#fff;font-weight:700}.onto svg .oe-e text{font:12px Calibri,Arial,sans-serif;fill:var(--ink);pointer-events:none}.onto svg .oe-e .oe-t{fill:#fff}
.onto svg .oe-r line,.onto svg .oe-r circle{stroke:var(--ink);stroke-width:1.5}.onto svg .oe-r circle{fill:var(--bg)}.onto svg .oe-v{fill:var(--card);stroke:var(--line)}.onto svg .oe-vt{font:italic 12px Calibri,Arial,sans-serif;fill:var(--ink)}.onto svg .oe-key text{font:11px Calibri,Arial,sans-serif;fill:var(--mute)}
.lg-me,.lg-sy,.lg-be{font-weight:700}.lg-sy{color:#1A7F37}.lg-be{color:#7A5F00}
.xfixd{margin:.2rem 0 .4rem}.xfixd summary{cursor:pointer;font-weight:600}.xtips details{margin:.2rem 0}.xtips summary{cursor:pointer}
#oclass,#oerd{min-height:24rem}
"""
rep("</style>", CSS + "</style>")

# question types: the new one, and the final exam gets one
rep("short:'Short answer'};", "short:'Short answer',program:'Complete the program (tips and notes)'};")
rep("write:3,short:3};", "write:3,short:3,program:4};")
rep("write:'C',short:'D'};", "write:'C',short:'D',program:'C'};")
rep("F:{name:'Final-style',minutes:75,", "F:{name:'Final-style',minutes:85,")
rep("['write',2],['short',3]]}}", "['write',2],['program',1],['short',3]]}}")

# the mock exam pane: what it is and where the earlier exams are
between("function examPane(){return '", "function xHistPaint(){", r"""function examPane(){return '<div role="tabpanel" data-pane="exam" hidden><h2>📝 Mock exam</h2><p class="note">A practice exam on this chapter, built on request from its own concepts, question bank and executed examples. Start a new one at any time: every exam is different, and its code names it, so the same code gives the same questions again. Every exam you start is kept under <b>My exams</b> in this browser, so you can come back to it later, review it with your answers and corrections, retake it, or ask for an alternative. Point values and times are this page’s defaults for practice, not the official exam rules. Marking happens when you finish; corrections are folded under each question.</p><div class="row"><label class="note" for="xekind">Exam</label><select id="xekind" aria-label="Kind of exam"><option value="M">Midterm-style: '+XEXAM.M.mix.reduce((a,x)=>a+x[1],0)+' questions, '+XEXAM.M.minutes+' minutes</option><option value="F">Final-style: '+XEXAM.F.mix.reduce((a,x)=>a+x[1],0)+' questions, '+XEXAM.F.minutes+' minutes</option></select><label class="note" for="xecode">Exam code</label><input class="xin" id="xecode" aria-label="Exam code (leave empty for a new exam)" placeholder="new exam" size="10" autocomplete="off"><label class="note"><input type="checkbox" id="xetimeron" checked> Timer</label><button class="btn" id="xestart">Start exam</button><button class="btn g" id="xenew">New exam</button></div><div id="xeout" aria-live="polite"></div><div id="xehist"></div></div>'}
""")

# maps: taxonomy (tree with leaves), ontology graph, class diagram, ERD
rep("['ontograph','🧬 Ontology graph']]", "['ontograph','🧬 Ontology graph'],['ontoclass','🧱 Class diagram'],['ontoerd','🔗 ERD']]")
i = s.index("P+='<div role=\"tabpanel\" data-pane=\"taxonomy\" hidden>"); j = s.index("\n", i)
s = s[:i] + r"""P+='<div role="tabpanel" data-pane="taxonomy" hidden>'+subbar('maps')+'<h2>🌳 Chapter taxonomy</h2><p class="legend"><span>▭ class (blue outline)</span><span><b style="background:var(--yellow);color:#1F2933;padding:0 .3rem;border-radius:4px">▭ individual</b></span><span>┅ concept from the book, matched by name</span></p><p class="note">The chapter\'s taxonomy as one tree, with its leaves. The root is the chapter; a class sits under the class it is a kind of; a worked example (an individual) hangs under the class it belongs to; a concept from the book hangs under the class it matches by name (dashed line). Choose a box to see what it is, where it sits and what it connects to; when the class has a section on this page you can go there or open its card. Use the checkboxes to hide a kind of node (with only the classes shown this is the plain hierarchy of subjects and concepts), and Show all to fit the whole tree; wheel or pinch to zoom, drag to move.</p><div class="row"><label><input type="checkbox" data-okind="class" checked> Classes</label><label><input type="checkbox" data-okind="individual" checked> Individuals</label><label><input type="checkbox" data-okind="book" checked> Book concepts</label><button class="btn g" id="ofit">Show all</button><span class="note" id="ostat" aria-live="polite"></span></div><div class="ontowrap"><div id="taxo" class="onto"></div><aside id="taxoinfo" class="ontoinfo note">Choose a box to see what it is and what it connects to.</aside></div></div>';""" + s[j:]
i = s.index("P+='<div role=\"tabpanel\" data-pane=\"ontograph\" hidden>"); j = s.index("\n", i)
s = s[:i] + r"""P+='<div role="tabpanel" data-pane="ontograph" hidden>'+subbar('maps')+'<h2>🧬 Ontology graph</h2><p class="legend"><span><b class="lg-me">━</b> meaning: is a kind of</span><span><b class="lg-sy">━</b> syntax: what it is written with</span><span><b class="lg-be">━</b> behaviour: what it does</span></p><p class="note">The ontology as a graph of three kinds of relation, one column each. In the middle are the chapter\'s concepts, indented by “is a kind of” (meaning). On the left are the syntax constructs found in each concept\'s example, read by Python\'s own parser (for example indexing, a method call, a comprehension). On the right are the behaviours the example shows, decided by rule from the same syntax tree (for example it changes the list itself, it builds a new value, it repeats). Every line carries its evidence: hover it to read the piece of code it comes from. Choose a concept to light up its relations, or choose a construct or a behaviour to see every concept that has it; the panel on the right lists them in words, with the meaning links the knowledge graph states (kinds, exclusions, the book\'s matching concept).</p><div class="row"><label><input type="checkbox" data-glayer="meaning" checked> Meaning</label><label><input type="checkbox" data-glayer="syntax" checked> Syntax</label><label><input type="checkbox" data-glayer="behaviour" checked> Behaviour</label><button class="btn g" id="gfit">Show all</button><span class="note" id="gstat" aria-live="polite"></span></div><div class="ontowrap"><div id="onto" class="onto"></div><aside id="ontoinfo" class="ontoinfo note">Choose a concept, a way of writing or a behaviour to see how it is connected.</aside></div></div>';
P+='<div role="tabpanel" data-pane="ontoclass" hidden>'+subbar('maps')+'<h2>🧱 Class diagram</h2><p class="legend"><span>◁ is a kind of (hollow arrow)</span><span>each box: name, what it is written with, what it does</span></p><p class="note">The ontology as a UML class diagram, one subject at a time. Each class shows its stereotype (subject, topic or concept), the syntax constructs its examples are written with, and the behaviours they show; a group takes the union of its concepts. The arrow points from a class to the class it is a kind of. Choose a box to open the concept\'s card.</p><div class="row"><label class="note" for="ocsub">Subject</label><select id="ocsub" aria-label="Subject to draw">'+D.nodes.filter(n=>n.level===1).map(n=>'<option value="'+n.id+'">'+esc(n.label)+'</option>').join('')+'</select><span class="note" id="ocstat" aria-live="polite"></span></div><div id="oclass" class="onto"></div></div>';
P+='<div role="tabpanel" data-pane="ontoerd" hidden>'+subbar('maps')+'<h2>🔗 Entity-relationship diagram</h2><p class="legend"><span>| one</span><span>crow\'s foot: many</span><span>○ optional</span></p><p class="note">The schema behind the ontology as an entity-relationship diagram: the kinds of thing it knows about, their attributes, and how they relate, with the number of each in this chapter. Read a line from either end: one subject contains many topics; one concept is shown by zero or more examples; an example is written with many constructs and a construct is used by many examples. Choose an entity to see its attributes, its relationships and some of its members.</p><div class="ontowrap"><div id="oerd" class="onto"></div><aside id="oerdinfo" class="ontoinfo note">Choose an entity to see what it holds.</aside></div></div>';""" + s[j:]
rep("if(k==='taxonomy')drawTaxo();if(k==='ontograph')drawOnto();", "if(k==='taxonomy')drawOnto();if(k==='ontograph')drawOgraph();if(k==='ontoclass')drawOclass();if(k==='ontoerd')drawOerd();")
rep("if(t.id==='ofit'){const z=document.querySelector('#onto [data-z=\"reset\"]');if(z)z.click();return}", "if(t.id==='ofit'){const z=document.querySelector('#taxo [data-z=\"reset\"]');if(z)z.click();return}if(t.id==='gfit'){const z=document.querySelector('#onto [data-z=\"reset\"]');if(z)z.click();return}")
between("// ---- ontology graph: nodes and edges", "// ---- question views ----", open(os.path.join(here, "template_ontology_v9_16_0.js"), encoding="utf-8").read())

# editor: save and open
rep('<button type="button" class="edb" data-edact="help"', '<span class="edgrp"><button type="button" class="edb" data-edact="save" aria-label="Save the code as a .py file" data-tip="Save as a .py file">⤓ Save</button><button type="button" class="edb" data-edact="open" aria-label="Open a .py file into the editor" data-tip="Open a .py file (or drop one on the box)">⤒ Open</button><input type="file" class="edfile" accept=".py,.txt,text/x-python,text/plain" hidden aria-label="Choose a code file"></span><button type="button" class="edb" data-edact="help"')
rep("['Esc then Tab','leave the box with the keyboard']]", "['Esc then Tab','leave the box with the keyboard'],['Save / Open','keep the code as a .py file, or load one (you can also drop a file on the box)']]")


# long unbroken tokens are cut so every label fits its box
rep("function wrapText(t,max){const w=String(t).split(/\\s+/),L=[];", "function wrapText(t,max){const w=[];String(t).split(/\\s+/).forEach(x=>{while(x.length>max){w.push(x.slice(0,max-1)+'\\u2011');x=x.slice(max-1)}w.push(x)});const L=[];")

js = open(os.path.join(here, "template_practice_v9_16_0.js"), encoding="utf-8").read()
assert s.count("</script>__CORPUS__") == 1
s = s.replace("</script>__CORPUS__", js + "</script>__CORPUS__")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
