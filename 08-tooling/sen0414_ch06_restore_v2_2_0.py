#!/usr/bin/env python3
"""Builds the chapter 6 RDODI files v2_2_0 (08-tooling/sen0414_ch06_rdodi_data_v2_2_0.py) and restores what v2_1_0 dropped.
Usage: sen0414_ch06_restore_v2_2_0.py   (runs the generic builder 1.2.0, then adds to the TBox, ABox and document every triple of v2_0_0 that the build lacks).
Not added: the triples of the ontology header (version, identifier, dates, revision comment), which describe the file and not its content; in the document only the labels."""
import os, subprocess, sys, rdflib
from rdflib import RDF, RDFS, OWL
TOOL = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(TOOL)
RD = os.path.join(REPO, "03-materials", "ch06", "rdodi")
r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0414_rdodi_build_v1_2_0.py"), "sen0414_ch06_rdodi_data_v2_2_0", "2026-10-08"], cwd=TOOL, env=dict(os.environ, PYTHONPATH=TOOL, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()); r.check_returncode()
B = "http://example.org/sen0414/ch06"; CH = rdflib.Namespace(B + "#"); RDm = rdflib.Namespace("http://example.org/rdodi/domain-ontology#")
def load(p): return rdflib.Graph().parse(p)
def f(part, v): return os.path.join(RD, "sen0414_ch06_%s_v%s.ttl" % (part, v))
for part, labels_only in (("domain_tbox", False), ("domain_abox", False), ("document", True)):
    new = load(f(part, "2_2_0")); old = load(f(part, "2_0_0")); added = 0
    header = {s for s in old.subjects(RDF.type, OWL.Ontology)}
    for s, p, o in old:
        if s in header: continue
        if labels_only and p != RDFS.label: continue
        if (s, p, o) not in new: new.add((s, p, o)); added += 1
    new.serialize(f(part, "2_2_0"), format="turtle")
    print("%s: %d triples of v2_0_0 added" % (part, added))
