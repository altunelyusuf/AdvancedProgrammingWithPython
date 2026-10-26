#!/usr/bin/env python3
"""Chapter 13 has NO older page ABox, so the comparison is of the new page ABox (v9_95_0, describing page 9.95.0) with what the chapter already holds:
(1) the concepts of the older research files (domain TBox classes and domain ABox individuals v1_0_3): which have a section in the new page ABox, which do not;
(2) the older page 9.28.2 (menu items, concept count, widgets with a step control) against the new page's menu items, tab rows and widgets. No file is written.
Usage: sen0414_ch13_page_abox_compare_v1_0_0.py"""
import os, re, rdflib
from rdflib import RDF, RDFS, OWL, URIRef
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials", "ch13")
ln = lambda u: str(u).rsplit("#", 1)[-1]
P = rdflib.Graph().parse(os.path.join(M, "page", "sen0414_ch13_page_abox_v9_95_0.ttl"))
IPO = "http://example.org/rdodi/interactive-page-ontology#"
secs = {ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "ChapterSection"))}
wids = {ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "InstructionalWidget"))}
print("new page ABox: %d triples, %d sections, %d widgets, %d code examples, %d menu items, %d tab rows" % (len(P), len(secs), len(wids), len(set(P.subjects(RDF.type, URIRef(IPO + "CodeExample")))), len(set(P.subjects(RDF.type, URIRef(IPO + "Menu")))), len(set(P.subjects(RDF.type, URIRef(IPO + "Tabs"))))))
T = rdflib.Graph().parse(os.path.join(M, "rdodi", "sen0414_ch13_domain_tbox_v1_0_3.ttl"))
A = rdflib.Graph().parse(os.path.join(M, "rdodi", "sen0414_ch13_domain_abox_v1_0_3.ttl"))
cls = {ln(s): str(next(T.objects(s, RDFS.label), "")) for s in T.subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)}
norm = lambda x: re.sub(r"[^a-z0-9]", "", x.lower())
ns = {norm(x) for x in secs}
print("domain TBox classes (v1_0_3): %d; with a same-named section in the page ABox: %d" % (len(cls), sum(norm(c) in ns for c in cls)))
for c, l in sorted(cls.items()):
    if norm(c) not in ns: print("   class without a section of its own name:", c, "|", l)
ind = {ln(s) for s in A.subjects(RDF.type, None) if isinstance(s, URIRef)} - {ln(s) for s in A.subjects(RDF.type, OWL.Ontology)}
print("domain ABox individuals (v1_0_3): %d; same-named section in the page ABox: %d" % (len(ind), sum(norm(re.sub(r"^IO_", "", i)) in ns for i in ind)))
old = open(os.path.join(M, "page", "sen0414_ch13_page_v9_28_2.html"), encoding="utf-8").read()
print("old page 9.28.2 top menu:", re.findall(r"\['(\w+)','[^']*'\]", re.search(r"const VIEWS=\[.*?\];", old).group(0)))
print("new page ABox menu items:", sorted(ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "Menu"))))
print("new page ABox tab rows  :", sorted(ln(s) for s in P.subjects(RDF.type, URIRef(IPO + "Tabs"))))
ex = [m for m in re.findall(r"static example shown", "\n".join(str(o) for o in P.objects(None, None)))]
print("widgets described as static example (no step control):", len(ex))
