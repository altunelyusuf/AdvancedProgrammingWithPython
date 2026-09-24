#!/usr/bin/env python3
"""RDODI Stage 4 for a SEN0414 chapter: the interactive page and its ABox, generated from the chapter's
Stage 2 ontology and Stage 3 document. Every output a widget reveals was produced by executing the
expression under the given Python, never typed. Usage: sen0414_page_build_v1_0_0.py <NN> <python>
Navigation follows BP-D34: 26-50 sections -> grouped permanent top bar with a sub-section sidebar."""
import html, json, os, subprocess, sys
import rdflib
from rdflib import RDF, RDFS, OWL
N, PY = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi"); OUT = os.path.join(REPO, "03-materials", "ch%s" % N, "page"); os.makedirs(OUT, exist_ok=True)
f = lambda p: os.path.join(RD, "sen0414_ch%s_%s_v1_0_0.ttl" % (N, p))
T = rdflib.Graph(); T.parse(f("domain_tbox"), format="turtle")
A = rdflib.Graph(); A.parse(f("domain_abox"), format="turtle")
Dg = rdflib.Graph(); Dg.parse(f("document"), format="turtle")
Rg = rdflib.Graph(); Rg.parse(f("research"), format="turtle")
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#"); SK = rdflib.namespace.SKOS; DC = rdflib.namespace.DCTERMS
RDN = rdflib.Namespace("http://example.org/rdodi/domain-ontology#"); RES = rdflib.Namespace("http://example.org/rdodi/research-ontology#")
BASE = "http://example.org/sen0414/ch%s" % N
CHN = rdflib.Namespace(BASE + "#")
title = str(Dg.value(predicate=RDF.type, object=None) and next(o for s, o in Dg.subject_objects(RDFS.label) if str(s).endswith("#Document")))
secs = sorted(((int(Dg.value(s, DOC.sectionOrder)), int(Dg.value(s, DOC.hierarchyLevel)), str(Dg.value(s, DOC.sectionTitle)),
                str(Dg.value(s, SK.definition)), str(Dg.value(s, DC.source)), str(s), str(Dg.value(s, DOC.hasParentSection) or "")) for s in Dg.subjects(DOC.sectionTitle, None)))

def run(expr):  # execute under the chapter's Python and return exactly what it prints for the expression
    code = "ns={}\ntry:\n    print(repr(eval(%r, ns)))\nexcept Exception as e:\n    print('%%s: %%s' %% (type(e).__name__, e))\n" % expr
    return subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=20).stdout.strip()
pyver = subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip()

widgets = []; body = []; nav = {}; glossary = []
for order, lv, t, text, cls_iri, sec_iri, parent in secs:
    cname = cls_iri.split("#")[-1]; sid = "s-" + cname
    ex = A.value(predicate=RDF.type, object=rdflib.URIRef(cls_iri)) if False else next((s for s in A.subjects(RDF.type, rdflib.URIRef(cls_iri)) if str(s).split("#")[-1].startswith("X_")), None)
    io = A.value(ex, RDN.hasIOExample) if ex is not None else None
    err = A.value(ex, RDN.hasErrorCondition) if ex is not None else None
    kids = [c for c in T.subjects(RDFS.subClassOf, rdflib.URIRef(cls_iri))]
    if lv == 1: nav[sid] = (t, [])
    else:
        top = sec_iri if lv == 1 else None
    w = None
    if io is not None:
        expr = str(A.value(io, CHN.input)); shown = run(expr)
        wid = "w-" + cname
        w = dict(id=wid, cls=cls_iri, prim="Primitive_CoupledVariableExplorer" if cname == "Precedence" else "Primitive_GuidedNarrativeWalkthrough",
                 warrant=("Feature_AsymmetricContrast: the section contrasts what a learner expects with what Python actually does for %s" % expr), kind="predict", expr=expr, out=shown)
        if cname == "Precedence":
            w.update(kind="toggle", alt="(2 + 3) * 6", alt_out=run("(2 + 3) * 6"))
        if err is not None:
            w["err_expr"] = str(A.value(err, RDFS.label)).split(" raises ")[0].replace("\\'", "'"); w["err_out"] = run(w["err_expr"])
    elif lv == 3:
        steps = [str(A.value(ex, RDFS.label)), str(A.value(ex, SK.definition))]
        w = dict(id="w-" + cname, cls=cls_iri, prim="Primitive_GuidedNarrativeWalkthrough",
                 warrant="Feature_OrderedArgument: the section's point is best met as an example followed by its explanation", kind="steps", steps=steps)
    else:
        items = [(str(T.value(k, RDFS.label)), str(Dg.value(rdflib.URIRef(BASE + "/document#S_" + str(k).split("#")[-1]), SK.definition) or
                  next((str(o) for s2, o in Dg.subject_objects(SK.definition) if str(s2).endswith("S_" + str(k).split("#")[-1])), ""))) for k in kids]
        w = dict(id="w-" + cname, cls=cls_iri, prim="Primitive_OverviewDetailBrushing",
                 warrant="Feature_KCategoryEnumeration: the section enumerates %d kinds; choosing one shows its detail" % len(items), kind="map", items=items)
    widgets.append(w)
    if lv == 3: glossary.append((t, str(A.value(ex, SK.definition)) if ex is not None else text))
    body.append((order, lv, t, text, sid, sec_iri, w, parent))

# --- navigation groups (BP-D34: grouped top bar, sub-section sidebar) ---
groups = []; cur = None
for order, lv, t, text, sid, sec_iri, w, parent in body:
    if lv == 1: cur = [t, sid, []]; groups.append(cur)
    else: cur[2].append((lv, t, sid))

E = html.escape
def widget_html(w):
    i = w["id"]
    if w["kind"] in ("predict", "toggle"):
        extra = ""
        if w["kind"] == "toggle":
            extra = '<button class="btn ghost" data-toggle="%s">Try it with parentheses</button>' % i
        if "err_expr" in w:
            extra += '<div class="errline">And <code>%s</code>? <button class="btn ghost" data-err="%s">Show what Python says</button> <output id="%s-err" class="out err" hidden>%s</output></div>' % (E(w["err_expr"]), i, i, E(w["err_out"]))
        return ('<div class="widget" id="%s"><div class="wlabel">Predict, then run</div><div class="shell"><span class="pr">&gt;&gt;&gt;</span> <code id="%s-expr">%s</code></div>'
                '<label class="sr" for="%s-guess">Your prediction</label><input id="%s-guess" class="guess" placeholder="Your prediction" autocomplete="off">'
                '<button class="btn" data-run="%s">Run</button><output id="%s-out" class="out" hidden>%s</output><p id="%s-verdict" class="verdict" aria-live="polite"></p>%s</div>') % (
                i, i, E(w["expr"]), i, i, i, i, E(w["out"]), i, extra)
    if w["kind"] == "steps":
        return ('<div class="widget" id="%s"><div class="wlabel">Walk through it</div><ol class="steps">%s</ol><button class="btn" data-step="%s">Next step</button></div>') % (
                i, "".join('<li%s>%s</li>' % ("" if k == 0 else " hidden", E(s)) for k, s in enumerate(w["steps"])), i)
    return ('<div class="widget" id="%s"><div class="wlabel">Explore the kinds</div><div class="chips">%s</div><p id="%s-detail" class="detail" aria-live="polite">Choose one to see what it is.</p></div>') % (
            i, "".join('<button class="chip" data-detail="%s" data-text="%s">%s</button>' % (i, E(d, quote=True), E(t)) for t, d in w["items"]), i)

refs = sorted((str(Rg.value(p, RDFS.label)), str(Rg.value(p, DC.source))) for p in Rg.subjects(RDF.type, RES.Publication))
quiz = json.load(open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "quiz.json")))
payload = json.dumps({w["id"]: {k: w.get(k) for k in ("kind", "out", "alt", "alt_out", "expr")} for w in widgets})
H = []
H.append('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%s - SEN0414 chapter %d</title><style>
:root{--ink:#1F2933;--mute:#5B6B7B;--navy:#1E2A3A;--blue:#306998;--yellow:#FFD43B;--card:#F1F4F8;--code:#17202B;--ok:#1A7F37;--bad:#B42318;--bg:#FFFFFF;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--ink:#E6EDF3;--mute:#9AA7B4;--card:#1C2531;--bg:#0F151C;--blue:#79B8FF;--ok:#56D364;--bad:#FF7B72}}
*{box-sizing:inherit}html{scroll-padding-top:6.5rem}body{margin:0;font:16px/1.6 Calibri,Arial,sans-serif;color:var(--ink);background:var(--bg)}
header.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--navy);color:#fff;padding:.6rem 1rem}
header.top h1{margin:0;font:600 1.15rem Cambria,Georgia,serif}header.top .sub{font-size:.85rem;color:#C9D4E0}
nav.groups{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.45rem}nav.groups a{background:var(--yellow);color:#1E2A3A;text-decoration:none;font-weight:700;padding:.2rem .7rem;border-radius:999px;font-size:.85rem}
.wrap{display:grid;grid-template-columns:15rem 1fr;gap:2rem;max-width:72rem;margin:0 auto;padding:1rem}
aside.side{position:sticky;top:6.5rem;align-self:start;max-height:calc(100vh - 7rem);overflow:auto;font-size:.9rem}aside.side ul{list-style:none;margin:0;padding-left:.8rem}aside.side a{color:var(--blue);text-decoration:none}
main section{margin-bottom:1.6rem}h2{font:700 1.6rem Cambria,Georgia,serif;color:var(--blue);margin:2rem 0 .4rem}h3{font:700 1.25rem Cambria,Georgia,serif;margin:1.2rem 0 .3rem}h4{font:700 1.05rem Cambria,Georgia,serif;margin:1rem 0 .2rem}
.widget{background:var(--card);border-radius:12px;padding:.8rem 1rem;margin:.6rem 0}.wlabel{font-size:.75rem;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);font-weight:700}
.shell{background:var(--code);color:#E6EDF3;border-radius:8px;padding:.5rem .8rem;margin:.4rem 0;font-family:"Courier New",monospace;overflow-x:auto}.pr{color:var(--yellow);font-weight:700}
.guess{font:15px "Courier New",monospace;padding:.35rem .5rem;border:1px solid #8896A5;border-radius:6px;width:min(22rem,100%%);margin-right:.4rem;background:var(--bg);color:var(--ink)}
.btn{background:var(--blue);color:#fff;border:0;border-radius:6px;padding:.4rem .9rem;font-weight:700;cursor:pointer;margin:.2rem .3rem .2rem 0}.btn.ghost{background:transparent;color:var(--blue);border:1px solid var(--blue)}
.out{display:block;font-family:"Courier New",monospace;background:var(--code);color:#7EE787;border-radius:6px;padding:.3rem .6rem;margin-top:.4rem;overflow-x:auto}.out.err{color:#FF7B72}
.verdict{margin:.3rem 0 0;font-weight:700}.chips{display:flex;flex-wrap:wrap;gap:.4rem;margin:.4rem 0}.chip{border:1px solid var(--blue);background:var(--bg);color:var(--blue);border-radius:999px;padding:.25rem .8rem;cursor:pointer;font-weight:700}
.chip[aria-pressed="true"]{background:var(--blue);color:#fff}.detail{margin:.3rem 0 0}.steps{margin:.4rem 0;padding-left:1.3rem}
.sr{position:absolute;left:-9999px}table{border-collapse:collapse}td,th{padding:.3rem .6rem;border-bottom:1px solid #D0D7DE;text-align:left}
.quiz fieldset{border:0;background:var(--card);border-radius:12px;margin:.6rem 0;padding:.8rem 1rem}.quiz legend{font-weight:700}
.meta{font-size:.85rem;color:var(--mute)}@media (max-width:760px){.wrap{grid-template-columns:1fr}aside.side{display:none}}
</style></head><body>''' % (E(title), int(N)))
H.append('<header class="top"><h1>%s</h1><div class="sub">SEN0414 Advanced Programming &middot; chapter %d &middot; every result below was produced by %s</div><nav class="groups" aria-label="Chapter sections">%s<a href="#quiz">Quiz</a><a href="#glossary">Glossary</a><a href="#references">References</a></nav></header>' % (
    E(title), int(N), E(pyver), "".join('<a href="#%s">%s</a>' % (sid, E(t)) for t, sid, _ in groups)))
H.append('<div class="wrap"><aside class="side" aria-label="All sections"><ul>%s</ul></aside><main>' % "".join(
    '<li><a href="#%s"><b>%s</b></a><ul>%s</ul></li>' % (sid, E(t), "".join('<li style="margin-left:%dpx"><a href="#%s">%s</a></li>' % ((lv - 2) * 10, s2, E(t2)) for lv, t2, s2 in subs)) for t, sid, subs in groups))
H.append('<section id="introduction"><p class="meta">Introduction &middot; chapter %d of <i>Automate the Boring Stuff with Python</i>, 3rd edition (Sweigart, 2025), renewed for an advanced course. Predict each result before you run it: the gap between what you expect and what Python does is where learning happens.</p><p><b>After this chapter you can:</b></p><ul>%s</ul><p class="meta">These chapter objectives serve the course outcomes LO-1 and LO-4.</p></section>' % (int(N), ''.join('<li>%s</li>' % E(v[0]) for v in json.load(open(os.path.join(REPO, '08-tooling', 'ch%s-page' % N, 'objectives.json'))).values())))
for order, lv, t, text, sid, sec_iri, w, parent in body:
    tag = {1: "h2", 2: "h3", 3: "h4"}[lv]
    H.append('<section id="%s" data-source="%s"><%s>%s</%s><p>%s</p>%s</section>' % (sid, E(sec_iri), tag, E(t), tag, E(text), widget_html(w)))
H.append('<section id="quiz" class="quiz"><h2>Quiz</h2>%s</section>' % "".join(
    '<fieldset data-answer="%d"><legend>%d. %s</legend>%s<button class="btn" data-check="q%d">Check</button><p id="q%d-fb" class="verdict" aria-live="polite"></p></fieldset>' % (
        (q["answer"] - k) % len(q["options"]), k + 1, E(q["q"]), "".join('<label style="display:block"><input type="radio" name="q%d" value="%d"> %s</label>' % (k, j, E(o)) for j, o in enumerate(q["options"][k % len(q["options"]):] + q["options"][:k % len(q["options"])])), k, k) for k, q in enumerate(quiz)))
H.append('<section id="glossary"><h2>Glossary</h2><table>%s</table></section>' % "".join('<tr><th>%s</th><td>%s</td></tr>' % (E(t), E(d)) for t, d in glossary))
H.append('<section id="references"><h2>References</h2><ol>%s</ol><p class="meta">Every source above was opened and read on 2026-09-24; the full research record is sen0414_ch%s_research_v1_0_0.ttl.</p></section>' % ("".join('<li>%s &mdash; <a href="%s">%s</a></li>' % (E(l), E(u), E(u)) for l, u in refs), N))
H.append('''</main></div><script>
const W=%s;
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;
 if(b.dataset.run){const i=b.dataset.run,o=document.getElementById(i+'-out'),g=document.getElementById(i+'-guess').value.trim(),v=document.getElementById(i+'-verdict');o.textContent=o.dataset.current||o.textContent;o.hidden=false;
  v.textContent=g===''?'Now compare with what you expected.':(g===o.textContent.trim()?'Your prediction matched.':'Not what you predicted - read the section again, then try the next one.');}
 if(b.dataset.toggle){const i=b.dataset.toggle,x=document.getElementById(i+'-expr'),o=document.getElementById(i+'-out'),alt=x.textContent===W[i].expr;
  x.textContent=alt?W[i].alt:W[i].expr;o.textContent=alt?W[i].alt_out:W[i].out;o.hidden=true;document.getElementById(i+'-verdict').textContent='';b.textContent=alt?'Back to the original':'Try it with parentheses';}
 if(b.dataset.err){document.getElementById(b.dataset.err+'-err').hidden=false;}
 if(b.dataset.step){const h=[...document.querySelectorAll('#'+b.dataset.step+' li[hidden]')];if(h.length){h[0].hidden=false;}if(h.length<=1){b.disabled=true;b.textContent='Done';}}
 if(b.dataset.detail){document.querySelectorAll('#'+b.dataset.detail+' .chip').forEach(c=>c.setAttribute('aria-pressed','false'));b.setAttribute('aria-pressed','true');document.getElementById(b.dataset.detail+'-detail').textContent=b.dataset.text;}
 if(b.dataset.check){const fs=b.closest('fieldset'),c=fs.querySelector('input:checked'),fb=document.getElementById(b.dataset.check+'-fb');fb.textContent=!c?'Choose an answer first.':(c.value===fs.dataset.answer?'Correct.':'Not quite - look back at the section.');}
});
</script></body></html>''' % payload)
open(os.path.join(OUT, "sen0414_ch%s_page_v1_0_0.html" % N), "w").write("".join(H))
json.dump({"widgets": widgets, "sections": [(o, lv, t, sid, s) for o, lv, t, x, sid, s, w, p in body], "python": pyver, "quiz": quiz}, open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "build_record.json"), "w"), indent=1)
print("page: %d sections, %d widgets, %d quiz questions, %d glossary entries - under %s" % (len(body), len(widgets), len(quiz), len(glossary), pyver))
