#!/usr/bin/env python3
"""Chapter 15 comparison (new file, TK_Ret_Ch15_Research). Two parts; no file is written.
Part 1: the research set v1_0_2 (committed) against v1_0_4 (rebuilt from the data module v1_0_4): classes, individuals, links (object properties), sources and labels,
        file by file (document, domain TBox, domain ABox, SHACL, research). Every triple of v1_0_2 that is absent in v1_0_4 is listed with its kind;
        version numbers in IRIs/literals (1_0_2 / 1.0.2 -> 1_0_4 / 1.0.4) are normalised first so that only real differences remain.
Part 2: the new page ABox (v9_95_0, describing page 9.96.1) against what the chapter has: the domain classes and individuals, the old page 9.30.0 (menu, tabs, nodes, widgets),
        and the files that must be byte-identical (git status of 03-materials/ch15 apart from the new files).
Usage: sen0414_ch15_compare_v1_0_0.py"""
import os, re, json, subprocess, rdflib
from rdflib import RDF, RDFS, OWL, URIRef, Literal
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials", "ch15"); RD = os.path.join(M, "rdodi")
ln = lambda u: str(u).rsplit("#", 1)[-1]
norm_v = lambda s: str(s).replace("1_0_2", "1_0_4").replace("1.0.2", "1.0.4")
def load(kind, v):
    g = rdflib.Graph().parse(os.path.join(RD, "sen0414_ch15_%s_v%s.ttl" % (kind, v)))
    out = set()
    for s, p, o in g:
        s2 = URIRef(norm_v(s)) if isinstance(s, URIRef) else s
        p2 = URIRef(norm_v(p))
        o2 = URIRef(norm_v(o)) if isinstance(o, URIRef) else (Literal(norm_v(o), lang=o.language, datatype=o.datatype) if isinstance(o, Literal) else o)
        out.add((s2, p2, o2))
    return out
DC = "http://purl.org/dc/terms/"
print("=== Part 1: research set v1_0_2 against v1_0_4 ===")
for kind in ("document", "domain_tbox", "domain_abox", "domain_shacl", "research"):
    O, N = load(kind, "1_0_2"), load(kind, "1_0_4")
    lost, gained = O - N, N - O
    typ = lambda S: {(s, o) for s, p, o in S if p == RDF.type}
    cls = lambda S: {s for s, o in typ(S) if o == OWL.Class}
    ind = lambda S: {s for s, o in typ(S) if o != OWL.Class and o != OWL.Ontology and isinstance(s, URIRef)}
    links = lambda S: {(s, p, o) for s, p, o in S if isinstance(o, URIRef) and p != RDF.type}
    src = lambda S: {(s, p, o) for s, p, o in S if ln(p) in ("source", "citedSource", "hasSource", "references") or str(p).startswith(DC + "source")}
    lab = lambda S: {(s, o) for s, p, o in S if p == RDFS.label}
    print("%-13s triples old %4d new %4d | classes lost %d | individuals lost %d | links lost %d | sources lost %d | labels lost %d | triples lost %d gained %d" % (
        kind, len(O), len(N), len(cls(O) - cls(N)), len(ind(O) - ind(N)), len(links(O) - links(N)), len(src(O) - src(N)), len(lab(O) - lab(N)), len(lost), len(gained)))
    for t in sorted(lost, key=str)[:12]: print("    only in v1_0_2:", tuple(ln(x) if isinstance(x, URIRef) else str(x)[:110] for x in t))
    for t in sorted(gained, key=str)[:12]: print("    only in v1_0_4:", tuple(ln(x) if isinstance(x, URIRef) else str(x)[:110] for x in t))
print()
print("=== Part 2: the new page ABox against the chapter's files ===")
PA = os.path.join(M, "page", "sen0414_ch15_page_abox_v9_95_0.ttl")
P = rdflib.Graph().parse(PA)
IPO = "http://example.org/rdodi/interactive-page-ontology#"
cnt = lambda t: set(P.subjects(RDF.type, URIRef(IPO + t)))
secs = {ln(s) for s in cnt("ChapterSection")}; wids = {ln(s) for s in cnt("InstructionalWidget")}
print("new page ABox: %d triples, %d sections, %d widgets, %d code examples, %d menu items, %d tab rows" % (len(P), len(secs), len(wids), len(cnt("CodeExample")), len(cnt("Menu")), len(cnt("Tabs"))))
T = rdflib.Graph().parse(os.path.join(RD, "sen0414_ch15_domain_tbox_v1_0_4.ttl")); A = rdflib.Graph().parse(os.path.join(RD, "sen0414_ch15_domain_abox_v1_0_4.ttl"))
cls = {ln(s): str(next(T.objects(s, RDFS.label), "")) for s in T.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
ns = {norm(x) for x in secs}
print("domain TBox classes (v1_0_4): %d; with a same-named section in the page ABox: %d" % (len(cls), sum(norm(c) in ns for c in cls)))
for c, l in sorted(cls.items()):
    if norm(c) not in ns: print("   class without a section of its own name:", c, "|", l)
ind = {ln(s) for s in A.subjects(RDF.type, None) if isinstance(s, URIRef)} - {ln(s) for s in A.subjects(RDF.type, OWL.Ontology)}
print("domain ABox individuals (v1_0_4): %d; same-named section in the page ABox: %d" % (len(ind), sum(norm(re.sub(r"^(IO_|X_)", "", i)) in ns for i in ind)))
old = open(os.path.join(M, "page", "sen0414_ch15_page_v9_30_0.html"), encoding="utf-8").read()
m = re.search(r"const VIEWS=\[.*?\];", old)
print("old page 9.30.0 top menu:", re.findall(r"\['(\w+)','[^']*'\]", m.group(0)) if m else "VIEWS not found")
print("new page ABox menu items:", sorted(ln(s) for s in cnt("Menu")))
print("new page ABox tab rows  :", sorted(ln(s) for s in cnt("Tabs")))
st = [str(o) for o in P.objects(None, None) if "static example shown" in str(o)]
print("widgets described as static example (no step control):", len(st))
for v in ("9_30_0", "9_96_1"):
    d = json.load(open(os.path.join(R, "08-tooling", "ch15-page", "page_data_v%s.json" % v), encoding="utf-8"))
    print("page data %s: %d nodes | visuals: %d | chaptercode: %d" % (v, len(d.get("nodes", [])), len(d.get("visuals", {})), len(d.get("chaptercode", []) or [])))
print("committed files unchanged (git status of the chapter's files; only new files may show):")
out = subprocess.run(["git", "-C", R, "status", "--short", "03-materials/ch15", "08-tooling/ch15-deck", "08-tooling/ch15-page"], capture_output=True, text=True).stdout
print(out if out.strip() else "   no change")
print("modified or deleted tracked files:", subprocess.run(["git", "-C", R, "diff", "--name-only", "HEAD"], capture_output=True, text=True).stdout.split() or "none")
