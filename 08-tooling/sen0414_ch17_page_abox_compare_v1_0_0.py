#!/usr/bin/env python3
"""Chapter 17 comparison (new tool, TK_Ret_Ch17_Research). No file is written.
(A) the research files 1.0.2 (committed) against 1.0.3 (new): individuals, classes, properties, links (triples between named things), literal labels and definitions, sources;
    the set of the old files must be a subset of the new files', each missing item is listed with its kind.
(B) the first page ABox (v9_95_0, describing page 9.96.0) against what the chapter already holds: the concepts of the research files (domain TBox classes and ABox individuals)
    that have a section in the page ABox, the older page 9.32.0 (top menu, concept nodes) against the new page's menu items, tab rows and widgets, widgets without a step control,
    and the page version stated inside the file.
Usage: sen0414_ch17_page_abox_compare_v1_0_0.py"""
import ast, json, os, re, rdflib
from rdflib import RDF, RDFS, OWL, URIRef, Literal
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials", "ch17")
ln = lambda u: str(u).rsplit("#", 1)[-1].rsplit("/", 1)[-1]
G = lambda kind, v: rdflib.Graph().parse(os.path.join(M, "rdodi", "sen0414_ch17_%s_v%s.ttl" % (kind, v)))
allok = True
reasons = {}
def newlabel(g, name):
    for s_, p_, o_ in g:
        if isinstance(s_, URIRef) and ln(s_) == name and ln(p_) == "label": return str(o_)
    return ""
def code_of(expr):
    t = ast.parse(expr, mode="eval").body
    if isinstance(t, ast.Call) and isinstance(t.func, ast.Lambda):      # (lambda g: (exec(<code>, g), g['out'])[1])({})
        return ast.literal_eval(t.func.body.value.elts[0].args[0])
    return ast.literal_eval(t.args[0])                                  # __import__('env').out(<code>)
def split_label(t):
    """a label is an expression followed by the text of the result; returns (code string, rest)"""
    m = re.match(r"^(\(lambda g: .*?\)\[1\]\)\(\{\}\))(.*)$", t, re.S) or re.match(r"^(__import__\('[^']+'\)\.out\('(?:[^'\\]|\\.)*'\))(.*)$", t, re.S)
    return (code_of(m.group(1)), m.group(2)) if m else None
def code_equal(old, new):
    try:
        a, b = split_label(old), split_label(new)
        return a is not None and a == b
    except Exception: return False
print("(A) research files 1_0_2 against 1_0_3")
for kind in ("domain_tbox", "domain_abox", "domain_shacl", "research", "document"):
    o, n = G(kind, "1_0_2"), G(kind, "1_0_3")
    subj = lambda g: {ln(s) for s in g.subjects() if isinstance(s, URIRef)}
    typed = lambda g: {(ln(s), ln(t)) for s, t in g.subject_objects(RDF.type) if isinstance(s, URIRef)}
    links = lambda g: {(ln(s), ln(p), ln(x)) for s, p, x in g if isinstance(s, URIRef) and isinstance(x, URIRef)}
    lits = lambda g: {(ln(s), ln(p), str(x)) for s, p, x in g if isinstance(s, URIRef) and isinstance(x, Literal) and ln(p) in ("label", "definition", "source", "comment", "verifiedAt", "title", "description", "sourceRole")}
    srcs = lambda g: {str(x) for s, p, x in g if ln(p) in ("source",)}
    res = {}
    for name, f in (("individuals/classes", subj), ("type statements", typed), ("links", links), ("labels/definitions/sources", lits), ("source URLs", srcs)):
        a, b = f(o), f(n); miss = sorted(a - b, key=str); add = len(b - a)
        # the two differences that have a stated reason: the version of the file (versionIRI) and the label of an input-output individual, which carries the example's expression: the new
        # expression is the same program (its code string) run in the isolated environment
        keep = []
        for x in miss:
            if x[1] == "versionIRI":
                reasons["versionIRI"] = reasons.get("versionIRI", 0) + 1
            elif x[1] == "label" and x[0].startswith("IO_") and code_equal(x[2], newlabel(n, x[0])):
                reasons["label of an input-output individual: expression wrapped to run in the isolated environment, same code string"] = reasons.get("label of an input-output individual: expression wrapped to run in the isolated environment, same code string", 0) + 1
            else:
                keep.append(x)
        miss = keep
        res[name] = (len(a), len(b), len(miss), add)
        if miss:
            allok = False
            for x in miss[:12]: print("      missing in 1_0_3 [%s %s]: %s" % (kind, name, str(x)[:200]))
    print("  %-12s triples %5d -> %5d | " % (kind, len(o), len(n)) + "; ".join("%s old %d new %d missing %d added %d" % ((k,) + v) for k, v in res.items()))
print("  differences with a stated reason:", reasons)
print("  every item of the 1_0_2 files is in the 1_0_3 files, apart from the stated differences:", allok)
print("(B) page ABox")
P = rdflib.Graph().parse(os.path.join(M, "page", "sen0414_ch17_page_abox_v9_95_0.ttl"))
IPO = "http://example.org/rdodi/interactive-page-ontology#"
secs = {ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "ChapterSection"))}
wids = {ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "InstructionalWidget"))}
print("new page ABox: %d triples, %d sections, %d widgets, %d code examples, %d menu items, %d tab rows" % (len(P), len(secs), len(wids), len(set(P.subjects(RDF.type, URIRef(IPO + "CodeExample")))), len(set(P.subjects(RDF.type, URIRef(IPO + "Menu")))), len(set(P.subjects(RDF.type, URIRef(IPO + "Tabs"))))))
T, A = G("domain_tbox", "1_0_3"), G("domain_abox", "1_0_3")
cls = {ln(s): str(next(T.objects(s, RDFS.label), "")) for s in T.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower()); ns = {norm(x) for x in secs}
print("domain TBox classes (v1_0_3): %d; with a same-named section in the page ABox: %d" % (len(cls), sum(norm(c) in ns for c in cls)))
for c, l in sorted(cls.items()):
    if norm(c) not in ns: print("   class without a section of its own name:", c, "|", l)
ind = {ln(s) for s in A.subjects(RDF.type, None) if isinstance(s, URIRef)} - {ln(s) for s in A.subjects(RDF.type, OWL.Ontology)}
print("domain ABox individuals (v1_0_3): %d; same-named section in the page ABox: %d" % (len(ind), sum(norm(re.sub(r"^IO_", "", i)) in ns for i in ind)))
old = open(os.path.join(M, "page", "sen0414_ch17_page_v9_32_0.html"), encoding="utf-8").read()
print("old page 9.32.0 top menu:", re.findall(r"\['(\w+)','[^']*'\]", re.search(r"const VIEWS=\[.*?\];", old).group(0)))
print("new page ABox menu items:", sorted(ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "Menu"))))
print("new page ABox tab rows  :", sorted(ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "Tabs"))))
print("widgets described as static example (no step control):", len(re.findall(r"static example shown", "\n".join(str(o) for o in P.objects(None, None)))))
PD = os.path.join(R, "08-tooling", "ch17-page")
on = {n["id"]: n["label"] for n in json.load(open(os.path.join(PD, "page_data_v9_32_0.json"), encoding="utf-8"))["nodes"]}
nn = {n["id"]: n["label"] for n in json.load(open(os.path.join(PD, "page_data_v9_96_0.json"), encoding="utf-8"))["nodes"]}
print("page data nodes: old 9.32.0 %d, new 9.96.0 %d; only in old: %d; only in new: %d; label changed: %d" % (len(on), len(nn), len(set(on) - set(nn)), len(set(nn) - set(on)), sum(on[i] != nn[i] for i in set(on) & set(nn))))
for i in sorted(set(on) - set(nn)): print("   only in old:", i, "|", on[i])
for i in sorted(set(nn) - set(on)): print("   only in new:", i, "|", nn[i])
for i in sorted(set(on) & set(nn)):
    if on[i] != nn[i]: print("   label changed:", i, "|", on[i], "->", nn[i])
txt = open(os.path.join(M, "page", "sen0414_ch17_page_abox_v9_95_0.ttl"), encoding="utf-8").read()
print("page file named in the ABox:", sorted(set(re.findall(r"sen0414_ch17_page_v[\d_]+\.html", txt))))
print("page version stated inside the file (statements naming the page file):", len(re.findall(r"sen0414_ch17_page_v9_96_0\.html", txt)), "of which the page individual's pageFile:", len(re.findall(r'sen0414:pageFile "03-materials/ch17/page/sen0414_ch17_page_v9_96_0\.html"', txt)))
