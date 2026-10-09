#!/usr/bin/env python3
"""Data for a SEN0414 chapter page, version 2: everything the page shows, extracted from the chapter's
Stage 2 ontology and Stage 3 document, with every example executed and every code diagram built from
Python's own ast module under the given interpreter. Nothing is typed by hand except the agent names.
Usage: sen0414_page_data_v2_7_0.py <NN> <python>  ->  08-tooling/chNN-page/page_data_v2.json"""
__version__ = "2.7.0"
# 2.7.0 (over 2.6.0), the owner's report of 2026-10-09 that the page's own worked examples never matched the slide
#   deck's code: the page's per-concept io examples are a separate, hand-curated set and always were, and the Lab
#   tab's Code Lab pane was entirely generic (meta-queries over the page's own data, not chapter content). This
#   version reads the chapter's own newest chNN-deck/examples_out_v*.json (the deck build's real executed REPL
#   transcript, the true source of the slide code) and flattens every named example's [code, out] cells into one
#   runnable script under data["examples"]: a cell whose out is falsy (None or "") is emitted verbatim (a statement,
#   assignment or void call); a cell whose out matches "<ExceptionName>: ..." is also emitted verbatim, so the
#   script genuinely raises the same error the slide shows (several chapters teach from a deliberate mistake, e.g.
#   chapter 3's randint used before its import - that is the point, not a bug to paper over); any other cell is
#   wrapped as print(repr(<code>)) to reproduce the interactive shell's auto-echo the deck's transcript captured.
#   No chapter without an examples_out file (none among 01-07; 08-24 are a different template generation) gets the
#   key at all, so the page build and the template degrade exactly as they already do for other optional sections.
# 2.6.0 (over 2.5.0), the owner's two-fold rule (2026-10-06) and the review of 2026-10-07 14:46, taken from the sibling
#   course's proven data builder: (a) reads course_page_config_v1_4_0.json (materials 1.37.0, the re-provisioned public
#   key, corpus.standards naming the two CME files with digests); (b) the chapter's 5N1K story companion
#   (sen0414_chNN_stories_v*.py, its own run_checks must pass) joins the page data under data["stories"], photographs
#   from 03-materials/chNN/assets through chNN-page/stories_img_v*.json, downscaled and embedded as data URIs;
#   (c) the CME narrative-to-diagram mapping is parsed from the CME checkout (CME_REPO, default /home/claude/cme) and
#   refused if a file's bytes differ from the recorded digest -> data["diagram_map"]; the newest
#   sen0414_chNN_diagrams_v*.py is imported, its run_checks(nodes, mapping) must pass, the type is ASSIGNED from the
#   mapping -> data["ndiag"], and the diagrams as cme:NarrativeDiagram individuals go into a Turtle block
#   (data["ndiag_abox"]) the page build embeds - never a file of the package (BP-D54 ceilings).
# 2.5.0: a document section may be several paragraphs, each opening with the question it answers ('What it is: ...'); the node keeps them as `paras` ([{facet, text}]) and its `body` is the first paragraph without the facet, so every consumer that wants one short statement still gets one; the co-mention relations read all the paragraphs.
# 2.4.0: reads course_page_config_v1_3_4.json, which adds the instructor's public key for exam release codes (the key pair is made outside the repository; only the public half is here).
# 2.3.0: reads course_page_config_v1_3_4.json (register 1.22.0, which lists the chapter 5 deck and page); a chapter may carry resources_v*.json (links, each opened and its title read on the date the file states) and lecture_v*.json (the deck's talk track), which become D.resources, D.resources_checked and D.lecture; the agents of chapter 5 are named.
# 2.2.2: reads course_page_config_v1_3_2.json (the course materials register of version 1.21.0, which lists the chapter 3 deck version 2.0.0 and page 9.6).
# 2.2.1: reads course_page_config_v1_3_1.json (the course materials register of version 1.20.0, which lists the chapter 4 deck, document and page).
# 2.2.0: the visuals file is the newest visuals_v*.json of the chapter (none is allowed), a chapter may replace the course's
# playground program with playground_v*.json, and the agents of chapters 3 and 4 are named. Chapters 1 and 2 build as before.
import json, os, re, subprocess, sys
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the page version they were produced for
import rdflib
from rdflib import RDF, RDFS, OWL
N, PY = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi"); import glob
f = lambda p: sorted(glob.glob(os.path.join(RD, "sen0414_ch%s_%s_v*.ttl" % (N, p))), key=lambda x: [int(v) for v in x.rsplit("_v",1)[1][:-4].split("_")])[-1]
T = rdflib.Graph(); T.parse(f("domain_tbox"), format="turtle"); A = rdflib.Graph(); A.parse(f("domain_abox"), format="turtle")
D = rdflib.Graph(); D.parse(f("document"), format="turtle"); R = rdflib.Graph(); R.parse(f("research"), format="turtle")
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#"); SK = rdflib.namespace.SKOS; DC = rdflib.namespace.DCTERMS
RDN = rdflib.Namespace("http://example.org/rdodi/domain-ontology#"); RES = rdflib.Namespace("http://example.org/rdodi/research-ontology#")
BASE = "http://example.org/sen0414/ch%s" % N; CH = rdflib.Namespace(BASE + "#")
pyver = subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip()

EXEC = r'''
import ast, json, sys
expr = sys.argv[1]
def tree(n):
    kids = [tree(c) for c in ast.iter_child_nodes(n) if not isinstance(c, (ast.Load, ast.Store, ast.operator, ast.unaryop, ast.cmpop, ast.boolop))]
    if isinstance(n, ast.BinOp): lab = {ast.Add:"+",ast.Sub:"-",ast.Mult:"*",ast.Div:"/",ast.FloorDiv:"//",ast.Mod:"%",ast.Pow:"**"}.get(type(n.op), type(n.op).__name__)
    elif isinstance(n, ast.Constant): lab = repr(n.value)
    elif isinstance(n, ast.Name): lab = n.id
    elif isinstance(n, ast.Call): lab = "call"
    elif isinstance(n, ast.JoinedStr): lab = "f-string"
    elif isinstance(n, ast.FormattedValue): lab = "{ }"
    else: lab = type(n).__name__
    return {"label": lab, "kind": type(n).__name__, "children": kids}
t = ast.parse(expr, mode="eval").body
try: out = repr(eval(expr, {}))
except Exception as e: out = "%s: %s" % (type(e).__name__, e)
# evaluation steps: the innermost operation whose operands are already values is evaluated and replaced, until one value
# remains - every step computed by this interpreter, not written by hand
SAFE = {"int", "str", "float", "len", "round", "bool", "abs", "repr", "type", "min", "max"}
def reducible(n):
    if isinstance(n, ast.Call):
        return isinstance(n.func, ast.Name) and n.func.id in SAFE and not n.keywords and all(isinstance(a, ast.Constant) for a in n.args)
    if isinstance(n, ast.BoolOp) and isinstance(n.values[0], ast.Constant):
        # short-circuit: "and" stops at a false value, "or" at a true one, without evaluating the rest
        v = n.values[0].value
        if (isinstance(n.op, ast.And) and not v) or (isinstance(n.op, ast.Or) and v): return True
    if isinstance(n, (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp)):
        return all(isinstance(c, ast.Constant) for c in ast.iter_child_nodes(n) if isinstance(c, ast.expr))
    if isinstance(n, ast.IfExp):
        return isinstance(n.test, ast.Constant) and isinstance(n.body, ast.Constant) and isinstance(n.orelse, ast.Constant)
    if isinstance(n, ast.JoinedStr):
        return all(isinstance(v, ast.Constant) or (isinstance(v, ast.FormattedValue) and isinstance(v.value, ast.Constant) and v.format_spec is None) for v in n.values)
    return False
steps = []
try:
    whole = ast.parse(expr, mode="eval")
    for _ in range(40):
        # Python evaluates operands left to right, innermost first: post-order, and the first reducible node wins
        def post(n):
            if isinstance(n, ast.BoolOp):
                # operands left to right, stopping as soon as the operation can short-circuit
                for c in n.values:
                    yield from post(c)
                    if reducible(n): break
                yield n; return
            for c in ast.iter_child_nodes(n): yield from post(c)
            yield n
        cand = [n for n in post(whole.body) if reducible(n)]
        if not cand: break
        node = cand[0]
        before, focus = ast.unparse(whole.body), ast.unparse(node)
        try: val = eval(compile(ast.Expression(node), "<step>", "eval"), {})
        except Exception as e:
            steps.append({"expr": before, "focus": focus, "value": "%s: %s" % (type(e).__name__, e), "error": True}); break
        if not isinstance(val, (int, float, str, bool, type(None))): break
        steps.append({"expr": before, "focus": focus, "value": repr(val)})
        new = ast.Constant(val)
        for parent in ast.walk(whole):
            for f, v in ast.iter_fields(parent):
                if v is node: setattr(parent, f, new)
                elif isinstance(v, list): parent.__dict__[f] = [new if x is node else x for x in v]
        ast.fix_missing_locations(whole)
        if isinstance(whole.body, ast.Constant): break
except SyntaxError:
    steps = []
print(json.dumps({"out": out, "tree": tree(t), "steps": steps}))
'''
def ex(expr):
    r = subprocess.run([PY, "-c", EXEC, expr], capture_output=True, text=True, timeout=20)
    return json.loads(r.stdout)

label = lambda c: str(T.value(c, RDFS.label))
classes = list(T.subjects(RDF.type, OWL.Class))
parent = {str(c): str(T.value(c, RDFS.subClassOf)) if T.value(c, RDFS.subClassOf) else None for c in classes}
secs = {str(D.value(s, DC.source)): s for s in D.subjects(DOC.sectionTitle, None)}
order = sorted(classes, key=lambda c: int(D.value(secs[str(c)], DOC.sectionOrder)))
FACETS = ("What it is", "Why it matters", "Where you meet it", "How it works", "What changed", "Watch out")
def PARAS(t):
    out = []
    for p in t.split("\n\n"):
        m = re.match(r"^(%s): (.*)$" % "|".join(FACETS), p, re.S)
        out.append({"facet": m.group(1), "text": m.group(2)} if m else {"facet": "", "text": p})
    return out
nodes = []
for c in order:
    s = secs[str(c)]; cid = str(c).split("#")[-1]
    X = next((x for x in A.subjects(RDF.type, c) if str(x).split("#")[-1].startswith("X_")), None)
    node = {"id": cid, "label": label(c), "level": int(D.value(s, DOC.hierarchyLevel)), "parent": parent[str(c)].split("#")[-1] if parent[str(c)] else None,
            "body": PARAS(str(D.value(s, SK.definition)))[0]["text"], "paras": PARAS(str(D.value(s, SK.definition))) if "\n\n" in str(D.value(s, SK.definition)) else [], "section_iri": str(s), "class_iri": str(c)}
    if X is not None:
        node["example"] = str(A.value(X, RDFS.label)); node["definition"] = str(A.value(X, SK.definition))
        io = A.value(X, RDN.hasIOExample)
        if io is not None:
            e = str(A.value(io, CH.input)); r = ex(e); node["io"] = {"code": e, "out": r["out"], "tree": r["tree"], "steps": r.get("steps", [])}
        er = A.value(X, RDN.hasErrorCondition)
        if er is not None:
            e = str(A.value(er, RDFS.label)).split(" raises ")[0]; node["error"] = {"code": e, "out": ex(e)["out"]}
        own = A.value(X, CH.hasOwner)
        if own is not None: node["owner"] = str(own).split("#")[-1].replace("X_", "")
    nodes.append(node)
ids = {n["id"] for n in nodes}; bylabel = {n["label"].lower(): n["id"] for n in nodes}
# Relations, each with its evidence: stated in the ontology, or a co-mention the document itself makes.
rels = []
for n in nodes:
    if n["parent"]: rels.append({"source": n["id"], "target": n["parent"], "type": "is a kind of", "evidence": "rdfs:subClassOf in the chapter's domain TBox"})
    if n.get("owner"): rels.append({"source": n["id"], "target": n["owner"], "type": "operates on", "evidence": "hasOwner (a subproperty of RDODI's hasOwningConcept) in the chapter's domain ABox"})
for n in nodes:
    if n["level"] < 3: continue
    for m in nodes:
        if m is n or m["level"] < 3 or m["parent"] == n["parent"]: continue
        if re.search(r"\b%s\b" % re.escape(m["label"].lower()), " ".join([p["text"] for p in n["paras"]] if n["paras"] else [n["body"]]).lower()):
            rels.append({"source": n["id"], "target": m["id"], "type": "mentions", "evidence": "the document's section on %s names %s" % (n["label"], m["label"])})
# Subjects and their agents: one per second-level subject, named for what it covers.
AGENT = {"NumericValue": "Numbers agent", "TextValue": "Text agent", "ArithmeticOperation": "Arithmetic agent", "TextOperation": "String agent",
         "BindingOperation": "Variables agent", "IOFunction": "Input-output agent", "ConversionFunction": "Conversion agent", "MeasurementFunction": "Measurement agent",
         "InteractiveEnvironment": "Shell agent", "InterpreterBuild": "Interpreter agent", "StringFormatting": "Formatting agent", "Tooling": "Tooling agent",
         "TruthValue": "Truth agent", "EqualityComparison": "Equality agent", "OrderingComparison": "Ordering agent", "LogicalOperator": "Logic agent",
         "Evaluation": "Evaluation agent", "ControlStructure": "Structure agent", "Branching": "Branching agent", "ExpressionForm": "Expression agent",
         "PatternMatching": "Matching agent", "Style": "Style agent",
         "ConditionLoop": "Condition loops agent", "CountedLoop": "Counted loops agent", "RangeSequence": "Range agent", "IterationHelper": "Iteration agent",
         "EarlyExit": "Early exit agent", "Skipping": "Skipping agent", "LoopCompletion": "Loop ending agent", "ImportForm": "Imports agent", "ExpressionStyle": "Expression style agent", "Hazard": "Hazards agent",
         "Raising": "Raising agent", "Tracebacks": "Traceback agent", "Assert": "Assertion agent", "Setup": "Logging setup agent", "Levels": "Logging levels agent", "Practice": "Logging practice agent", "Controls": "Debugger controls agent", "PythonDebugger": "Python debugger agent", "WorkedCases": "Worked cases agent"}
agents = [{"id": "agent-" + n["id"], "name": AGENT.get(n["id"], n["label"] + " agent"), "subject": n["id"],
           "covers": [m["id"] for m in nodes if m["parent"] == n["id"]] + [n["id"]]} for n in nodes if n["level"] == 2]
refs = sorted((str(R.value(p, RDFS.label)), str(R.value(p, DC.source))) for p in R.subjects(RDF.type, RES.Publication))
title = next(str(o) for s, o in D.subject_objects(RDFS.label) if str(s).endswith("#Document"))
SEN = rdflib.Namespace("http://example.org/sen0414#")
findings = sorted(((str(R.value(x, RDFS.label)), str(R.value(x, SEN.findingText))) for x in R.subjects(RDF.type, SEN.Finding)), key=lambda x: x[0])
COURSE = json.load(open(os.path.join(REPO, "08-tooling", "course_page_config_v1_4_0.json")))
DISC = os.path.join(REPO, "08-tooling", "ch%s-page" % N, "discussion_v1_0_0.json")
_vf = sorted(glob.glob(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "visuals_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
VIS = _vf[-1] if _vf else ""
_pf = sorted(glob.glob(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "playground_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
if _pf: COURSE["playground"] = {k: v for k, v in json.load(open(_pf[-1])).items() if not k.startswith("_")}
def newest(pat):
    fs = sorted(glob.glob(os.path.join(REPO, "08-tooling", "ch%s-page" % N, pat)), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
    return json.load(open(fs[-1])) if fs else None
_res = newest("resources_v*.json"); _lec = newest("lecture_v*.json")
# ---- 2.7.0: the chapter's own deck examples, flattened into runnable scripts that match the slide transcript ----
_ef = sorted(glob.glob(os.path.join(REPO, "08-tooling", "ch%s-deck" % N, "examples_out_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
EXAMPLES = None
if _ef:
    _ERR = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*(Error|Exception|Warning):")
    def _flatten(cells):
        lines = []
        for code, out in cells:
            if not out or (isinstance(out, str) and _ERR.match(out.strip())):
                lines.append(code)
            else:
                lines.append("print(repr(%s))" % code)
        return "\n".join(lines)
    _deck = json.load(open(_ef[-1]))
    EXAMPLES = [{"name": k, "code": _flatten(v)} for k, v in _deck.items() if not k.startswith("_")]
    print("examples: %d from %s (the deck's own worked examples, this chapter)" % (len(EXAMPLES), os.path.basename(_ef[-1])))
# ---- 2.7.0: the chapter's 5N1K stories, checked by their own module, photos from the deck's assets --------------
STORIES = None
if True:
    _sf = sorted(glob.glob(os.path.join(REPO, "08-tooling", "sen0414_ch%s_stories_v*.py" % N)),
                 key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-3].split("_")])
    if _sf:
        import base64, io, importlib.util
        from PIL import Image
        spec = importlib.util.spec_from_file_location("stories_mod", _sf[-1]); _sm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_sm)
        _bad = _sm.run_checks()
        if _bad: raise SystemExit("story companion %s fails its own checks: %s" % (os.path.basename(_sf[-1]), _bad))
        _imap = {}
        _if = sorted(glob.glob(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "stories_img_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
        if _if: _imap = {k: v for k, v in json.load(open(_if[-1])).items() if not k.startswith("_")}
        ADIR = os.path.join(REPO, "03-materials", "ch%s" % N, "assets")
        def _embed(fn, maxw):
            fp = os.path.join(ADIR, fn)
            if not os.path.exists(fp): raise SystemExit("stories_img maps %s, which is not in %s" % (fn, ADIR))
            im = Image.open(fp); im.load()
            if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
            buf = io.BytesIO()
            if fn.lower().endswith(".png"): im.save(buf, "PNG", optimize=True); mime = "image/png"
            else: im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True); mime = "image/jpeg"
            return {"data": "data:%s;base64,%s" % (mime, base64.b64encode(buf.getvalue()).decode()), "w": im.width, "h": im.height}
        STORIES = []
        for s in _sm.STORIES:
            e = {k: s[k] for k in ("id", "title", "when", "who", "where", "link", "story", "lesson", "source")}
            e["concepts"] = list(s.get("concepts", []))
            pics = _imap.get(s["id"], [])
            e["imgs"] = [dict(_embed(p["file"], 640 if len(pics) == 1 else 420), credit=p["credit"], file=p["file"]) for p in pics]
            STORIES.append(e)
        print("stories: %d from %s (%d with photographs, %d photographs embedded)" % (
            len(STORIES), os.path.basename(_sf[-1]), sum(1 for e in STORIES if e["imgs"]), sum(len(e["imgs"]) for e in STORIES)))
# ---- 2.11.0: the CME narrative-to-diagram mapping, and the chapter's authored diagrams typed by it ----------------
import hashlib
CME_REPO = os.environ.get("CME_REPO", "/home/claude/cme")
CMEN = rdflib.Namespace("http://example.org/cme#")
MAPG = rdflib.Graph()
for st in COURSE["corpus"].get("standards", []):
    fp = os.path.join(CME_REPO, st["folder"], st["path"]); b = open(fp, "rb").read()
    if hashlib.sha256(b).hexdigest() != st["sha256"]:
        raise SystemExit("the CME standard %s at %s does not match the digest recorded in the configuration; re-run course_page_config_build" % (st["path"], fp))
    MAPG.parse(data=b.decode(), format="turtle")
def _lab(s): return str(MAPG.value(s, RDFS.label) or "")
DMAP = {}
for p in MAPG.subjects(RDF.type, CMEN.NarrativePattern):
    types = [str(t).split("#")[1] for t in MAPG.objects(p, CMEN.suggestsDiagram)]
    DMAP[str(p).split("#")[1]] = {"label": _lab(p), "question": str(MAPG.value(p, CMEN.answersQuestion) or ""), "cues": sorted(str(c) for c in MAPG.objects(p, CMEN.cuePhrase)),
                                   "types": types, "notation": str(MAPG.value(CMEN[types[0]], CMEN.notation) or "") if types else "", "renderer": str(MAPG.value(CMEN[types[0]], CMEN.renderer) or "") if types else ""}
NDIAG = None; NDIAG_ABOX = None
if True:
    _df = sorted(glob.glob(os.path.join(REPO, "08-tooling", "sen0414_ch%s_diagrams_v*.py" % N)), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-3].split("_")])
    if _df:
        import importlib.util
        spec = importlib.util.spec_from_file_location("diagrams_mod", _df[-1]); _dm = importlib.util.module_from_spec(spec); spec.loader.exec_module(_dm)
        _bad = _dm.run_checks(nodes, DMAP)
        if _bad: raise SystemExit("diagram companion %s fails its checks: %s" % (os.path.basename(_df[-1]), _bad))
        NDIAG = [{k: d[k] for k in ("id", "pattern", "type", "title", "concepts", "read_from", "why", "data", "grounding")} for d in _dm.DIAGRAMS]
        # the diagrams as individuals of the CME vocabulary, beside the page
        def _tl(s): return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'
        ab = ["@prefix cme: <http://example.org/cme#> .", "@prefix chx: <http://example.org/sen0414/ch%s#> .", "@prefix owl: <http://www.w3.org/2002/07/owl#> .", "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .", "@prefix dcterms: <http://purl.org/dc/terms/> .", "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .", "",
              "<http://example.org/sen0414/ch%s/diagrams> a owl:Ontology ; rdfs:label \"SEN0414 ch%s narrative diagrams - ABox\"@en ; owl:versionInfo \"%s\" ; dcterms:identifier \"sen0414_ch%s_diagrams_abox_v%s\" ;" % (N, N, _dm.__version__, N, _dm.__version__.replace(".", "_")),
              "    rdfs:comment \"The chapter's authored diagrams as cme:NarrativeDiagram individuals: generated by sen0414_page_data_v2_6_0.py from sen0414_ch%s_diagrams_v%s.py, typed by the CME narrative-to-diagram mapping (a module of cme_standards_adoption_v1_3_0.ttl, CME 0.16.0).\"@en ; owl:imports <http://example.org/cme/narrative-diagram> ." % (N, _dm.__version__.replace(".", "_")), ""]
        ab[1] = ab[1] % N
        for d in NDIAG:
            ab.append("chx:Diagram_%s a cme:NarrativeDiagram ; rdfs:label %s@en ; cme:hasPattern cme:%s ; cme:hasDiagramType cme:%s ; cme:readFrom %s ; cme:elementCount %d ;" % (d["id"], _tl(d["title"]), d["pattern"], d["type"], _tl(d["read_from"]), len(_dm._labels(d))))
            ab.append("    " + " ; ".join("cme:accompanies %s" % _tl(c) for c in d["concepts"]) + " ; rdfs:comment %s@en ." % _tl(d["why"]))
        _abn = "sen0414_ch%s_diagrams_abox_v%s.ttl" % (N, _dm.__version__.replace(".", "_"))
        _abt = "\n".join(ab) + "\n"
        rdflib.Graph().parse(data=_abt, format="turtle")
        NDIAG_ABOX = {"name": _abn, "text": _abt}
        print("diagrams: %d from %s (%s), grounding %s; ABox block %s (embedded in the page, not a file: BP-D54 counts every Turtle file of the package, and the course's A-file ceiling is 34)" % (len(NDIAG), os.path.basename(_df[-1]), ", ".join("%s->%s" % (d["pattern"], d["type"]) for d in NDIAG), " ".join("%d/%d" % tuple(d["grounding"]) for d in NDIAG), _abn))
data = {"_version": PV.replace("_", "."), "visuals": {k: v for k, v in (json.load(open(VIS)) if os.path.exists(VIS) else {}).items() if not k.startswith("_")}, "course": COURSE, "discussion": json.load(open(DISC)) if os.path.exists(DISC) else [], "findings": findings, "unit": None,
        "research_file": os.path.basename(f("research")), "chapter": int(N), "title": title, "python": pyver, "nodes": nodes, "relations": rels, "agents": agents, "refs": refs}
if _res: data["resources"] = _res["links"]; data["resources_checked"] = _res["checked"]
if _lec: data["lecture"] = _lec["slides"]
if EXAMPLES is not None: data["examples"] = EXAMPLES
if STORIES is not None: data["stories"] = STORIES
data["diagram_map"] = DMAP
if NDIAG is not None: data["ndiag"] = NDIAG; data["ndiag_abox"] = NDIAG_ABOX
out = os.path.join(REPO, "08-tooling", "ch%s-page" % N); os.makedirs(out, exist_ok=True)
json.dump(data, open(os.path.join(out, "page_data_v%s.json" % PV), "w"), indent=1)
print("chapter %s: %d concepts, %d relations (%d stated, %d co-mentions), %d agents, %d executed examples with ast trees, under %s" % (
    N, len(nodes), len(rels), sum(1 for r in rels if r["type"] != "mentions"), sum(1 for r in rels if r["type"] == "mentions"),
    len(agents), sum(1 for n in nodes if "io" in n), pyver))
