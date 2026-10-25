#!/usr/bin/env python3
"""Compares the OLD and the NEW files of chapter 5 (individuals, classes, links, sources, labels) and lists every element of the old files that the new files lack.
Usage: sen0414_ch05_subset_proof_v1_0_0.py   (no file is written; exit 0 when nothing of the old files is missing, 1 otherwise)
Pairs: research 1_1_0 -> 1_3_0, domain_tbox 1_1_0 -> 1_3_0, domain_abox 1_1_0 -> 1_3_0, domain_shacl 1_0_0 -> 1_3_0, document 1_2_0 -> 1_3_0 (header triples are not content and are skipped)."""
import hashlib, os, sys, rdflib
from rdflib import RDF, RDFS, OWL, URIRef, Literal
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); RD = os.path.join(REPO, "03-materials", "ch05", "rdodi")
DC = rdflib.Namespace("http://purl.org/dc/terms/")
PAIRS = [("research", "1_1_0"), ("domain_tbox", "1_1_0"), ("domain_abox", "1_1_0"), ("domain_shacl", "1_0_0"), ("document", "1_2_0")]
bad = 0
NS_OLD, NS_NEW = "http://example.org/sen0414/ch05/document#", "http://example.org/sen0414/ch05#"
def norm(g, document):
    """document: the v1_2_0 document names its sections in the namespace .../ch05/document#, the generic builder in .../ch05# (the namespace of every other chapter file); the local names are compared.
    Blank nodes (the SHACL property shapes) are replaced by a name made of their content so that two files with the same shapes compare equal."""
    h = rdflib.Graph(); bn = {}
    def m(x):
        if isinstance(x, URIRef) and document and str(x).startswith(NS_OLD): return URIRef(NS_NEW + str(x)[len(NS_OLD):])
        if isinstance(x, rdflib.BNode):
            return URIRef("urn:bnode:" + hashlib.sha1("|".join(sorted("%s=%s" % (p, o) for p, o in g.predicate_objects(x))).encode()).hexdigest())
        return x
    for s, p, o in g: h.add((m(s), p, m(o)))
    return h
def elements(g):
    hdr = set(g.subjects(RDF.type, OWL.Ontology))
    tr = {t for t in g if t[0] not in hdr}
    individuals = {s for s in g.subjects(RDF.type, None) if s not in hdr and (s, RDF.type, OWL.Class) not in g}
    classes = {s for s in g.subjects(RDF.type, OWL.Class)} | {o for s, o in g.subject_objects(RDF.type) if isinstance(o, URIRef)}
    links = {(s, p, o) for s, p, o in tr if isinstance(o, URIRef) and p != RDF.type}
    sources = {(s, o) for s, o in g.subject_objects(DC.source) if s not in hdr}
    labels = {(s, o) for s, o in g.subject_objects(RDFS.label) if s not in hdr}
    return dict(triples=tr, individuals=individuals, classes=classes, links=links, sources=sources, labels=labels)
for part, ov in PAIRS:
    old = elements(norm(rdflib.Graph().parse(os.path.join(RD, "sen0414_ch05_%s_v%s.ttl" % (part, ov))), part == "document"))
    new = elements(norm(rdflib.Graph().parse(os.path.join(RD, "sen0414_ch05_%s_v1_3_0.ttl" % part)), False))
    print("== %s v%s -> v1_3_0" % (part, ov))
    for k in ("individuals", "classes", "links", "sources", "labels", "triples"):
        miss = old[k] - new[k]
        print("  %-12s old %4d  new %4d  missing in new %d" % (k, len(old[k]), len(new[k]), len(miss)))
        for m in sorted(map(str, miss))[:40]: print("     MISSING", m[:230])
        bad += len(miss)
print("RESULT: %s (%d elements of the old files missing in the new)" % ("NOTHING MISSING" if not bad else "DIFFERENCES", bad))
sys.exit(1 if bad else 0)
