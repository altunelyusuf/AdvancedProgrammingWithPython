#!/usr/bin/env python3
"""Compares the OLD page ABox of chapter 1 (v9_4_2) with the NEW one (v9_92_0, which describes the page 9.92.0): the individuals, classes, links, sources and
labels of the old file that the new file lacks, grouped by the kind of individual. No file is written. Usage: sen0414_ch01_page_abox_compare_v1_0_0.py"""
import collections, os, rdflib
from rdflib import RDF, RDFS, OWL, URIRef
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PD = os.path.join(REPO, "03-materials", "ch01", "page")
DC = rdflib.Namespace("http://purl.org/dc/terms/")
def load(v): return rdflib.Graph().parse(os.path.join(PD, "sen0414_ch01_page_abox_v%s.ttl" % v))
def els(g):
    hdr = set(g.subjects(RDF.type, OWL.Ontology))
    ind = {s for s in g.subjects(RDF.type, None) if s not in hdr}
    cls = {o for o in g.objects(None, RDF.type) if isinstance(o, URIRef)}
    links = {(s, p, o) for s, p, o in g if isinstance(o, URIRef) and p != RDF.type and s not in hdr}
    src = {(s, o) for s, o in g.subject_objects(DC.source) if s not in hdr}
    lab = {(s, str(o)) for s, o in g.subject_objects(RDFS.label) if s not in hdr}
    return dict(individuals=ind, classes=cls, links=links, sources=src, labels=lab)
def mapped(g):
    """the old page ABox names the sections of the old taxonomy pg:s_<Id>; the new one names a section pg:<Id> (the id of the concept in the page data); the old name is mapped to the new one"""
    h = rdflib.Graph()
    m = lambda x: URIRef(str(x).replace("/page#s_", "/page#")) if isinstance(x, URIRef) else x
    for s, p, o in g: h.add((m(s), p, m(o)))
    return h
import sys
MAP = "--mapped" in sys.argv
o, n = els(mapped(load("9_4_2")) if MAP else load("9_4_2")), els(load("9_92_0"))
ln = lambda u: str(u).rsplit("#", 1)[-1]
for k in o:
    miss = o[k] - n[k]; print("%-12s old %4d new %4d missing in new %4d" % (k, len(o[k]), len(n[k]), len(miss)))
kind = lambda name: ("widget-" + name.split("_")[0]) if name.startswith(("w_", "wv_")) else ("question-option" if name.startswith("Q") and "_O" in name else "question" if name.startswith("Q") else "objective" if name.startswith("CO") else "other")
g = collections.defaultdict(list)
for s in sorted(o["individuals"] - n["individuals"], key=ln): g[kind(ln(s))].append(ln(s))
for k, v in g.items(): print("missing individuals, kind %s: %d  %s" % (k, len(v), ", ".join(v[:60])))
print("missing classes:", sorted(map(ln, o["classes"] - n["classes"])))
print("labels missing (subject, text):")
for s, l in sorted(o["labels"] - n["labels"], key=lambda x: (ln(x[0]), x[1])): print("   ", ln(s), "|", l, "| new label:", [x for x in n["labels"] if x[0] == s][:1])
print("sources missing (subject -> source), first 40:")
for s, l in sorted(o["sources"] - n["sources"], key=lambda x: (ln(x[0]), str(x[1])))[:40]: print("   ", ln(s), "->", l)
print("links missing (first 40):")
for s, p, x in sorted(o["links"] - n["links"], key=lambda x: tuple(map(str, x)))[:40]: print("   ", ln(s), ln(p), ln(x))
