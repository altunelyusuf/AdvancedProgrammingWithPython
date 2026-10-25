#!/usr/bin/env python3
"""Builds the chapter 5 RDODI files v1_3_0 (08-tooling/sen0414_ch05_rdodi_data_v1_3_0.py) and restores what the generic builder cannot write.
Usage: sen0414_ch05_restore_v1_3_0.py   (runs the generic builder 1.2.0, then adds to the TBox, ABox and document every triple of v1_1_0 / v1_2_0 that the build lacks).
Not added: the triples of the ontology header (version, identifier, dates, revision comment), which describe the file and not its content; in the document only the labels.
In the research file the per-source verification times, the methodology text and the two scorecard texts of v1_1_0 replace the generic ones of the build, so that nothing the earlier file says is lost."""
import os, subprocess, sys, rdflib
from rdflib import RDF, RDFS, OWL, SKOS
TOOL = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(TOOL)
RD = os.path.join(REPO, "03-materials", "ch05", "rdodi")
r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0414_rdodi_build_v1_2_0.py"), "sen0414_ch05_rdodi_data_v1_3_0", "2026-10-01T20:00:44"], cwd=TOOL, env=dict(os.environ, PYTHONPATH=TOOL, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()); r.check_returncode()
def load(p): return rdflib.Graph().parse(p)
def f(part, v): return os.path.join(RD, "sen0414_ch05_%s_v%s.ttl" % (part, v))
SEN = rdflib.Namespace("http://example.org/sen0414#"); VA = SEN.verifiedAt
for part, oldv, mode in (("domain_tbox", "1_1_0", "all"), ("domain_abox", "1_1_0", "all"), ("document", "1_2_0", "labels"), ("research", "1_1_0", "verified")):
    new = load(f(part, "1_3_0")); old = load(f(part, oldv)); added = 0
    header = {s for s in old.subjects(RDF.type, OWL.Ontology)}
    if mode == "verified":
        for P in (VA, SEN.methodology, SEN.topicCoverage, SEN.citationStrength):
            for s, o in list(old.subject_objects(P)):
                if (s, P, o) not in new: new.remove((s, P, None)); new.add((s, P, o)); added += 1
        print("%s: %d values (verification times, methodology, scorecard texts) of %s restored" % (part, added, oldv))
    else:
        if mode == "labels":
            # the old document names its sections in .../ch05/document#, the generic builder in .../ch05# : the old labels and titles go to the new names; the
            # generated label and title of a section are replaced by the curated ones of v1_2_0, and the old description of the document replaces the generated one
            DOC = rdflib.Namespace("http://example.org/sen0414/ch05/document#"); CHN = rdflib.Namespace("http://example.org/sen0414/ch05#")
            DT = rdflib.URIRef("http://example.org/rdodi/document-ontology#sectionTitle")
            for s, p, o in list(old):
                if s in header or not str(s).startswith(str(DOC)): continue
                s2 = CHN[str(s)[len(str(DOC)):]]
                if p in (RDFS.label, DT) or (p == SKOS.definition and str(s2).endswith("#Document")):
                    new.remove((s2, p, None)); new.add((s2, p, o)); added += 1
            old = rdflib.Graph()
        for s, p, o in old:
            if s in header: continue
            if mode == "labels" and p != RDFS.label: continue
            if (s, p, o) not in new: new.add((s, p, o)); added += 1
        print("%s: %d triples of %s added" % (part, added, oldv))
    new.serialize(f(part, "1_3_0"), format="turtle")
