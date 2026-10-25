#!/usr/bin/env python3
"""sen0414_control_iter19_compare v1_0_0 - the lineage agent's own comparison of the OLD and NEW files of a retrofitted chapter (the lesson of chapter 6: a session dropped seven individuals and said nothing was removed).
Usage: sen0414_control_iter19_compare_v1_0_0.py NN OLD_FILE[,OLD_FILE...] NEW_FILE[,NEW_FILE...] [--map PREFIXOLD=PREFIXNEW]
Compares by LOCAL NAME (the part after # or the last /), so a changed namespace or ontology version does not count as a difference: the typed individuals, the classes, the predicates used, the links between named things (subject, predicate, object), the source values and the labels.
Prints every element of the old set missing from the new set, and the new elements; exit 0 always (the caller reads the lists)."""
__version__ = "1.0.0"
import re, sys
import rdflib
from rdflib import RDF, RDFS, OWL, Literal, URIRef


def ln(x, mp):
    s = str(x); s = re.split(r"[#/]", s)[-1]
    for a, b in mp:
        if s.startswith(a): s = b + s[len(a):]
    return s


def load(files):
    g = rdflib.Graph()
    for f in files.split(","):
        g.parse(f, format="turtle")
    return g


def sets(g, mp):
    out = {k: set() for k in ("individuals", "classes", "predicates", "links", "sources", "labels")}
    for s, p, o in g:
        if p == RDF.type and isinstance(s, URIRef):
            if o in (OWL.Class, RDFS.Class): out["classes"].add(ln(s, mp))
            elif o not in (OWL.Ontology, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty, RDF.Property, OWL.NamedIndividual): out["individuals"].add(ln(s, mp))
        if isinstance(s, URIRef): out["predicates"].add(ln(p, mp))
        if isinstance(s, URIRef) and isinstance(o, URIRef) and p != RDF.type: out["links"].add((ln(s, mp), ln(p, mp), ln(o, mp)))
        if re.search(r"source", str(p), re.I) and isinstance(o, Literal): out["sources"].add(" ".join(str(o).split()))
        if p == RDFS.label and isinstance(o, Literal) and isinstance(s, URIRef): out["labels"].add((ln(s, mp), " ".join(str(o).split())))
    return out


def main():
    n, old, new = sys.argv[1], sys.argv[2], sys.argv[3]; mp = []
    if "--map" in sys.argv:
        for m in sys.argv[sys.argv.index("--map") + 1:]:
            a, b = m.split("="); mp.append((a, b))
    so, sn = sets(load(old), mp), sets(load(new), mp)
    print("chapter", n, "old files:", old, "new files:", new, "map:", mp)
    for k in so:
        miss = sorted(so[k] - sn[k], key=str); add = sn[k] - so[k]
        print("%-11s old %5d  new %5d  missing from new %4d  new-only %4d" % (k, len(so[k]), len(sn[k]), len(miss), len(add)))
        for x in miss[:60]:
            print("   MISSING %s: %s" % (k, str(x)[:200]))


if __name__ == "__main__":
    main()
