"""Makes course_page_template_v9_15_0.html from v9_14_0. Usage: template_patch_v9_15_0.py <in.html> <out.html>
9.15.0 (the owner's request of 2026-09-30 16:15): (1) the Agents list is short (icon and name), its width is adjustable (drag, keys, double-click for icons only)
and what each agent knows is a tip; (2) the Playground starts with its own default program; (3) every code box is a small Python editor: colouring, font family and
size, line numbers, hover help, suggestions, indentation helpers, auto-closing brackets and quotes, code templates; (4) the right-hand card closes when the main
area changes context; (5) the ontology graph is a rooted tree like the taxonomy, with a legend and a fuller narrative; (6) Back, Forward and a list of places
visited in the header. Editor help data: python_docs_v1_0_0.json (built by python_docs_build_v1_0_0.py from the interpreter)."""
import sys, os, re
here = os.path.dirname(os.path.abspath(__file__))
s = open(sys.argv[1], encoding="utf-8").read()
def rep(old, new, count=1):
    global s
    assert s.count(old) == count, (s.count(old), old[:90])
    s = s.replace(old, new)

rep("<!-- course_page_template version 9.14.0:", "<!-- course_page_template version 9.15.0: code editor, adjustable short agent list with tips, playground default, card closes on context change, ontology tree, Back/Forward trail. Earlier: --><!-- course_page_template version 9.14.0:")

CSS = r"""/* 9.15.0: editor, agent list, navigation trail, ontology tree */
.ed{margin:.3rem 0;--edgw:0px}
.edtools{display:flex;flex-wrap:wrap;gap:.35rem .7rem;align-items:center;background:#0F1720;border:1px solid #2B3A4B;border-bottom:0;border-radius:8px 8px 0 0;padding:.3rem .5rem;font-size:.8rem;color:#DCE6F0}
.edtools select{font:inherit;background:#1B2836;color:#E6EDF3;border:1px solid #3B4D61;border-radius:6px;padding:.15rem .3rem;max-width:11rem}
.edgrp{display:inline-flex;gap:.2rem;align-items:center}.edfs{min-width:3.2rem;text-align:center}
.edb{font:inherit;font-weight:700;min-width:1.9rem;min-height:1.9rem;background:var(--yellow);color:#1F2933;border:0;border-radius:6px;cursor:pointer;padding:0 .4rem}.edb:hover{filter:brightness(.93)}
.edln{display:inline-flex;gap:.25rem;align-items:center}
.edhelp{background:#0F1720;color:#DCE6F0;border:1px solid #2B3A4B;border-top:0;padding:.3rem .6rem;font-size:.8rem}.edhelp[hidden]{display:none}.edhelp table{border-collapse:collapse}.edhelp th{text-align:left;font-family:ui-monospace,monospace;padding:.1rem .9rem .1rem 0;color:#FFD43B;font-weight:600;white-space:nowrap}.edhelp td{padding:.1rem 0}
.edbox{position:relative;background:var(--code);border:1px solid #2B3A4B;border-radius:8px;overflow:hidden}.ed.hastools .edbox{border-radius:0 0 8px 8px}.edbox:focus-within{outline:2px solid var(--yellow);outline-offset:1px}
.edhl,.edgut,textarea.edta{font-family:var(--edff,"Courier New",monospace)!important;font-size:calc(var(--edfs,14)*.0625rem)!important;line-height:1.5!important;tab-size:4;letter-spacing:normal;margin:0;box-sizing:border-box;white-space:pre;border:0;padding-top:.6rem;padding-bottom:.6rem;padding-right:.7rem;padding-left:calc(var(--edgw) + 1.2rem)}
.ed.noln .edhl,.ed.noln textarea.edta{padding-left:.7rem}
.edhl{position:absolute;inset:0;overflow:hidden;color:#E6EDF3;padding-bottom:calc(.6rem + 20px);pointer-events:none;background:none}
.edgut{position:absolute;left:0;top:0;bottom:0;width:calc(var(--edgw) + .7rem);overflow:hidden;color:#93A6B9;text-align:right;padding-left:0;padding-right:.35rem;pointer-events:none;background:#121B26;border-right:1px solid #2B3A4B;padding-bottom:calc(.6rem + 20px)}.ed.noln .edgut{display:none}
textarea.edta{position:relative;display:block;width:100%;background:transparent!important;color:#E6EDF3!important;-webkit-text-fill-color:transparent;caret-color:#FFD43B;resize:none;overflow:auto;outline:none;border-radius:0;min-height:0}
textarea.edta::selection{background:rgba(88,146,224,.5);-webkit-text-fill-color:transparent}
.edhl i{font-style:normal}.edhl .hk{color:#FF8B84}.edhl .hb{color:#7CC4FF}.edhl .hs{color:#A8DDA8}.edhl .hn{color:#FFD07A}.edhl .hc{color:#93A6B9;font-style:italic}.edhl .hf{color:#D9B4FF}.edhl .hd{color:#FFB070}.edhl .hv{color:#FFB070;font-style:italic}
#edac{position:fixed;z-index:23;background:#0F1720;color:#E6EDF3;border:1px solid #3B4D61;border-radius:8px;box-shadow:0 6px 20px #0006;min-width:12rem;max-width:26rem;font:.85rem ui-monospace,monospace;padding:.2rem}#edac[hidden]{display:none}
#edac [role=option]{padding:.15rem .5rem;border-radius:5px;cursor:pointer;display:flex;gap:.6rem;align-items:baseline}#edac [role=option][aria-selected=true]{background:#2A4A73}
#edac small{color:#B7C6D6;font-size:.72rem;font-family:system-ui,sans-serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.edsr{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
#tip{white-space:pre-line}
.agentsview{--rw:192px}
.rsplit{cursor:col-resize;width:.5rem;border-radius:4px;background:var(--line);touch-action:none;align-self:stretch}.rsplit:hover,.rsplit:focus-visible{background:var(--blue)}
.persona .pn{min-width:0;overflow:hidden}.persona .pn b{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.agentsview.icons .pn{display:none}.agentsview.icons .persona{justify-content:center;padding:.4rem .15rem}
@media (max-width:900px){.rsplit{display:none}.agentsview.icons .pn{display:block}.agentsview.icons .persona{justify-content:flex-start;padding:.45rem .6rem}}
.navgrp{display:inline-flex;gap:.25rem;position:relative;align-items:center}
.navgrp>button{background:var(--yellow);color:#1F2933;border:0;border-radius:8px;font-weight:700;min-width:36px;min-height:36px;cursor:pointer;font-size:1rem}.navgrp>button:disabled{opacity:.4;cursor:default}
#navMenu{position:absolute;top:calc(100% + 4px);left:0;z-index:30;background:var(--panel);color:var(--ink);border:1px solid var(--line);border-radius:10px;box-shadow:0 8px 24px #0004;min-width:14rem;max-width:80vw;max-height:60vh;overflow:auto;padding:.25rem;flex-direction:column;display:flex}#navMenu[hidden]{display:none}
#navMenu button{background:transparent;color:var(--ink);text-align:left;border:0;font-size:.9rem;min-height:36px;padding:.25rem .6rem;border-radius:6px;width:100%;cursor:pointer}#navMenu button:hover,#navMenu button:focus-visible{background:var(--card)}#navMenu button[aria-current]{font-weight:700}
.onto svg .on{cursor:pointer}.onto svg .on rect{fill:var(--card);stroke:var(--blue);stroke-width:1.4}.onto svg .on.k-individual rect{fill:var(--yellow);stroke:#B08900}.onto svg .on.k-book rect{fill:var(--panel);stroke:#7A5F00;stroke-dasharray:5 3}
.onto svg .on:focus rect,.onto svg .on:hover rect{stroke-width:3}.onto svg text{font:12px "Courier New",monospace;fill:var(--ink);pointer-events:none}
"""
rep("</style>", CSS + "</style>")
rep("grid-template-columns:17rem 1fr;gap:.8rem", "grid-template-columns:var(--rw,192px) .5rem 1fr;gap:.3rem")
rep("@media print{header.top,", "@media print{.navgrp,.ed .edtools,#edac,header.top,")

# header: Back, Forward and the places visited
rep('<button class="btn g" id="srchBtn"', '<span class="navgrp" role="group" aria-label="Where you have been"><button type="button" id="navBack" aria-label="Back" data-tip="Nothing to go back to" disabled>◀</button><button type="button" id="navFwd" aria-label="Forward" data-tip="Nothing to go forward to" disabled>▶</button><button type="button" id="navTrail" aria-haspopup="menu" aria-expanded="false" aria-label="Places you have visited" data-tip="Places you have visited">🕘</button><div id="navMenu" role="menu" aria-label="Places you have visited" hidden></div></span><button class="btn g" id="srchBtn"')

# playground: its own default program first and shown
rep(r'''<select id="pex" aria-label="Examples">'+D.nodes.filter(n=>n.io).map(n=>'<option value="'+n.id+'">'+esc(n.label)+': '+esc(n.io.code)+'</option>').join('')+'<option value="first">'+esc(D.course.playground.label)+'</option></select>''',
    r'''<select id="pex" aria-label="Examples"><option value="first">'+esc(D.course.playground.label)+'</option>'+D.nodes.filter(n=>n.io).map(n=>'<option value="'+n.id+'">'+esc(n.label)+': '+esc(n.io.code)+'</option>').join('')+'</select>''')
rep(r'''aria-label="Playground code">print(\'Hello, world!\')</textarea>''', r'''aria-label="Playground code">'+esc(D.course.playground.code)+'</textarea>''')

# agents: short names, the sentence is a tip, adjustable width
rep(r'''<button role="tab" class="persona" data-agenttab="guide" aria-selected="true"><span class="av">🧭</span><span><b>Guide</b><small>Not sure who to ask? I\u2019ll introduce you</small></span></button>''',
    r'''<button role="tab" class="persona" data-agenttab="guide" aria-selected="true" aria-label="Guide. Not sure who to ask? I\u2019ll introduce you" data-tip="Not sure who to ask? I\u2019ll introduce you"><span class="av">🧭</span><span class="pn"><b>Guide</b></span></button>''')
rep(r'''aria-selected="false"><span class="av">'+agentIcon(a)+'</span><span><b>'+esc(a.name)+'</b><small>'+esc(agentRole(a))+'</small></span></button>''',
    r'''aria-selected="false" aria-label="'+esc(a.name+'. '+agentRole(a))+'" data-tip="'+esc(agentRole(a))+'"><span class="av">'+agentIcon(a)+'</span><span class="pn"><b>'+esc(a.name)+'</b></span></button>''')
rep('''</div><div class="chatpane">''', '''</div><div class="rsplit" role="separator" aria-orientation="vertical" tabindex="0" aria-label="Resize the agent list" aria-valuemin="56" aria-valuemax="360" aria-valuenow="192" data-tip="Drag to resize. Double-click for icons only."></div><div class="chatpane">''')

# ontology graph pane: legend and a fuller narrative, like the concept map and the taxonomy
i = s.index("<h2>🧬 Ontology graph</h2>"); j = s.index('<div class="ontowrap">', i)
s = s[:i] + r'''<h2>🧬 Ontology graph</h2><p class="legend"><span>▭ class (blue outline)</span><span><b style="background:var(--yellow);color:#1F2933;padding:0 .3rem;border-radius:4px">▭ individual</b></span><span style="color:#7A5F00">┅ concept from the book, matched by name</span></p><p class="note">This is the chapter\'s knowledge graph drawn as a tree, like the taxonomy. The root is the chapter; a class sits under the class it is a kind of; an individual (a worked example) hangs under the class it belongs to; a concept from the book hangs under the class it matches by name (dashed line). Links that are neither kinds nor examples appear in the side panel when you choose a box. Choose a box to see what it is, where it sits and what it connects to; when the class has a section on this page you can go there or open its card. Use the checkboxes to hide a kind of node, and Show all to fit the whole tree; wheel or pinch to zoom, drag to move.</p><div class="row"><label><input type="checkbox" data-okind="class" checked> Classes</label><label><input type="checkbox" data-okind="individual" checked> Individuals</label><label><input type="checkbox" data-okind="book" checked> Book concepts</label><button class="btn g" id="ofit">Show all</button><span class="note" id="ostat" aria-live="polite"></span></div>''' + "'+'" .replace("'+'", "") + s[j:]
rep("if(t.id==='orelayout'){if(ONTO)layoutOnto();return}", "")
rep("if(t.id==='ofit'){renderOnto();return}", "if(t.id==='ofit'){const z=document.querySelector('#onto [data-z=\"reset\"]');if(z)z.click();return}")
rep("seed:1};st.textContent=ONTO.nodes.length+' nodes, '+E.length+' edges';layoutOnto()}", "seed:1};renderOnto()}")
a = s.index("function layoutOnto(){"); b = s.index("// ---- question views ----")
s = s[:a] + open(os.path.join(here, "template_onto_v9_15_0.js"), encoding="utf-8").read() + s[b:]

# tips on elements that carry one
rep("document.addEventListener('mouseover',e=>{const c=e.target.closest('[data-c]');if(!c){tip.hidden=true;return}",
    "document.addEventListener('mouseover',e=>{const d=e.target.closest&&e.target.closest('[data-tip]');if(d){tip.textContent=d.dataset.tip;tip.hidden=false;return}const c=e.target.closest('[data-c]');if(!c){tip.hidden=true;return}")
# the copy button must not be added to the editor's colour layer
rep("p.closest('#srch,.cheat,.widget,.vis')", "p.closest('#srch,.cheat,.widget,.vis,.edbox')")

import json
pydoc = json.dumps(json.load(open(os.path.join(here, "python_docs_v1_0_0.json"), encoding="utf-8")), ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
js = open(os.path.join(here, "template_editor_v9_15_0.js"), encoding="utf-8").read().replace("__PYDOC__", pydoc)
assert s.count("</script>__CORPUS__") == 1
s = s.replace("</script>__CORPUS__", js + "</script>__CORPUS__")
open(sys.argv[2], "w", encoding="utf-8").write(s)
print("wrote", sys.argv[2], len(s))
