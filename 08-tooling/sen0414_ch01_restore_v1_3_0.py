#!/usr/bin/env python3
"""Builds the chapter 1 RDODI files v1_3_0 (08-tooling/sen0414_ch01_rdodi_data_v1_3_0.py) and restores what the generic builder cannot write.
Usage: sen0414_ch01_restore_v1_3_0.py   (runs the generic builder 1.2.0, then adds to the five files every triple of the committed files that the build lacks).
Old files: research v1_1_0, domain_tbox v1_1_1, domain_abox v1_1_1, domain_shacl v1_0_1, document v1_2_0 (all committed, none edited).
Not added: the triples of the ontology header (version, identifier, dates, revision comment), which describe the file and not its content.
Research: the research file v1_1_0 names its individuals in the namespace http://example.org/sen0414# (Ch01Research, Ch01Scope, P01..P25, C01_01..C01_27, F1..F5, Scorecard);
the generic builder writes them in the chapter namespace as Research, Scope and C_01..C_27. The old local names are kept (the generated Research, Scope, C_nn and Scorecard are
replaced by the old individuals with all their triples, written in the chapter namespace), so that no individual name of the old file is lost; the research content is that of v1_1_0.
Domain ABox: the individuals Artifact, CQs, CQ1..CQ3, Provenance and Env are described by the old file; where the build wrote a different label, definition or source for one of them, the old one replaces it.
SHACL: the old shapes (with their messages) replace the generated ones. Document: the old section labels and titles replace the generated ones (as in chapter 4)."""
import os, re, subprocess, sys, rdflib
from rdflib import RDF, RDFS, OWL, SKOS
TOOL = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(TOOL)
RD = os.path.join(REPO, "03-materials", "ch01", "rdodi")
r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0414_rdodi_build_v1_2_0.py"), "sen0414_ch01_rdodi_data_v1_3_0", "2026-10-25T12:00:00"], cwd=TOOL, env=dict(os.environ, PYTHONPATH=TOOL, PYTHONDONTWRITEBYTECODE="1"), capture_output=True, text=True)
print(r.stdout.strip(), r.stderr.strip()); r.check_returncode()
def load(p): return rdflib.Graph().parse(p)
def f(part, v): return os.path.join(RD, "sen0414_ch01_%s_v%s.ttl" % (part, v))
SEN = rdflib.Namespace("http://example.org/sen0414#"); CHN = rdflib.Namespace("http://example.org/sen0414/ch01#")
DCS = rdflib.URIRef("http://purl.org/dc/terms/source")
INDIV = re.compile(r"^(Ch01Research|Ch01Scope|P\d+|C01_\d+|F\d+|Scorecard)$")
def to_chx(x):
    if isinstance(x, rdflib.URIRef) and str(x).startswith(str(SEN)) and INDIV.match(str(x)[len(str(SEN)):]): return CHN[str(x)[len(str(SEN)):]]
    return x
for part, oldv, mode in (("domain_tbox", "1_1_1", "all"), ("domain_abox", "1_1_1", "abox"), ("domain_shacl", "1_0_1", "replace"), ("document", "1_2_0", "labels"), ("research", "1_1_0", "research")):
    new = load(f(part, "1_3_0")); old = load(f(part, oldv)); added = 0
    header = {s for s in old.subjects(RDF.type, OWL.Ontology)}
    if mode == "research":
        # drop the generated Research, Scope, C_nn and Scorecard; take every old individual (with all its triples) under the old local name in the chapter namespace
        gen = [CHN.Research, CHN.Scope, CHN.Scorecard] + [s for s in set(new.subjects()) if re.match(r"^C_\d+$", str(s).rsplit("#", 1)[-1])]
        for s in gen: new.remove((s, None, None))
        for s, p, o in old:
            if s in header: continue
            s2 = to_chx(s)
            if s2 == s: continue            # not one of the research individuals
            if re.match(r"^(P\d+|F\d+)$", str(s2).rsplit("#", 1)[-1]): new.remove((s2, p, None))
        for s, p, o in old:
            if s in header: continue
            s2 = to_chx(s)
            if s2 == s: continue
            new.add((s2, p, to_chx(o))); added += 1
        print("%s: %d triples of the individuals Ch01Research, Ch01Scope, P01-P25, C01_01-C01_27, F1-F5 and Scorecard of %s written under their old names" % (part, added, oldv))
    elif mode == "replace":
        for s, p, o in list(new):
            if s not in set(new.subjects(RDF.type, OWL.Ontology)): new.remove((s, p, o))
        for s, p, o in old:
            if s not in header: new.add((s, p, o)); added += 1
        print("%s: %d triples of %s replace the generated shapes" % (part, added, oldv))
    else:
        if mode == "labels":
            DOC = rdflib.Namespace("http://example.org/sen0414/ch01/document#")
            DT = rdflib.URIRef("http://example.org/rdodi/document-ontology#sectionTitle")
            for s, p, o in list(old):
                if s in header or not str(s).startswith(str(DOC)): continue
                s2 = CHN[str(s)[len(str(DOC)):]]
                if p in (RDFS.label, DT) or (p == SKOS.definition and str(s2).endswith("#Document")):
                    new.remove((s2, p, None)); new.add((s2, p, o)); added += 1
            old = rdflib.Graph()
        if mode == "abox":
            for s in (CHN.Artifact, CHN.CQs, CHN.CQ1, CHN.CQ2, CHN.CQ3, CHN.Provenance, CHN.Env):
                for p in (RDFS.label, SKOS.definition, DCS):
                    ov = set(old.objects(s, p))
                    if ov and set(new.objects(s, p)) != ov: new.remove((s, p, None))
        for s, p, o in old:
            if s in header: continue
            if mode == "labels" and p != RDFS.label: continue
            if (s, p, o) not in new: new.add((s, p, o)); added += 1
        print("%s: %d triples of %s added" % (part, added, oldv))
    new.serialize(f(part, "1_3_0"), format="turtle")
