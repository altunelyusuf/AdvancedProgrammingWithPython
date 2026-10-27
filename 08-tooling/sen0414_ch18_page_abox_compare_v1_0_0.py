#!/usr/bin/env python3
"""Chapter 18 has NO older page ABox, so the comparison is of the new page ABox (v9_95_0, describing page 9.96.0) with what the chapter already holds:
(1) the classes of the older domain TBox and the individuals of the older domain ABox (v1_0_2): which have a section in the new page ABox, which do not;
(2) the older page 9.33.0 (top menu, tab rows, concept nodes, widgets) against the new page's menu items, tab rows, sections and widgets;
(3) the research set files: byte-identical to the committed ones (git). No file is written.
Usage: sen0414_ch18_page_abox_compare_v1_0_0.py"""
import os, re, json, subprocess, rdflib
from rdflib import RDF, RDFS, OWL, URIRef
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials", "ch18")
ln = lambda u: str(u).rsplit("#", 1)[-1]
P = rdflib.Graph().parse(os.path.join(M, "page", "sen0414_ch18_page_abox_v9_95_0.ttl"))
IPO = "http://example.org/rdodi/interactive-page-ontology#"
cnt = lambda t: set(P.subjects(RDF.type, URIRef(IPO + t)))
secs = {ln(s) for s in cnt("ChapterSection")}; wids = {ln(s) for s in cnt("InstructionalWidget")}
print("new page ABox: %d triples, %d sections, %d widgets, %d code examples, %d menu items, %d tab rows" % (len(P), len(secs), len(wids), len(cnt("CodeExample")), len(cnt("Menu")), len(cnt("Tabs"))))
T = rdflib.Graph().parse(os.path.join(M, "rdodi", "sen0414_ch18_domain_tbox_v1_0_2.ttl"))
A = rdflib.Graph().parse(os.path.join(M, "rdodi", "sen0414_ch18_domain_abox_v1_0_2.ttl"))
cls = {ln(s): str(next(T.objects(s, RDFS.label), "")) for s in T.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
ns = {norm(x) for x in secs}
print("domain TBox classes (v1_0_2): %d; with a same-named section in the page ABox: %d" % (len(cls), sum(norm(c) in ns for c in cls)))
for c, l in sorted(cls.items()):
    if norm(c) not in ns: print("   class without a section of its own name:", c, "|", l)
ind = {ln(s) for s in A.subjects(RDF.type, None) if isinstance(s, URIRef)} - {ln(s) for s in A.subjects(RDF.type, OWL.Ontology)}
print("domain ABox individuals (v1_0_2): %d; same-named section in the page ABox: %d" % (len(ind), sum(norm(re.sub(r"^IO_", "", i)) in ns for i in ind)))
old = open(os.path.join(M, "page", "sen0414_ch18_page_v9_33_0.html"), encoding="utf-8").read()
print("old page 9.33.0 top menu:", re.findall(r"\['(\w+)','[^']*'\]", re.search(r"const VIEWS=\[.*?\];", old).group(0)))
print("new page ABox menu items:", sorted(ln(s) for s in cnt("Menu")))
print("new page ABox tab rows  :", sorted(ln(s) for s in cnt("Tabs")))
st = [str(o) for o in P.objects(None, None) if "static example shown" in str(o)]
print("widgets described as static example (no step control):", len(st))
try:
    od = json.load(open(os.path.join(R, "08-tooling", "ch18-page", "page_data_v9_33_0.json"), encoding="utf-8"))
    print("old page data 9.33.0: %d nodes" % len(od.get("nodes", [])), "| visuals:", len(od.get("visuals", {})))
except Exception as e: print("old page data 9.33.0 not read:", e)
nd = json.load(open(os.path.join(R, "08-tooling", "ch18-page", "page_data_v9_96_0.json"), encoding="utf-8"))
print("new page data 9.96.0: %d nodes" % len(nd["nodes"]), "| visuals:", len(nd.get("visuals", {})))
print("research files unchanged (git diff HEAD on 03-materials/ch18/rdodi and the page file, the manifests, the deck):")
out = subprocess.run(["git", "-C", R, "status", "--short", "03-materials/ch18", "08-tooling/ch18-deck"], capture_output=True, text=True).stdout
print(out if out.strip() else "   no change to any committed file of 03-materials/ch18 or 08-tooling/ch18-deck")
