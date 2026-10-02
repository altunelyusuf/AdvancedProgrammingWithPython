#!/usr/bin/env python3
"""RDODI Stage 2 and Stage 3 for one SEN0414 chapter, from its corpus file (sen0414_chNN_corpus_vX_Y_Z.py, the newest one).
Writes the domain TBox and ABox and the document (one section per concept, paragraphs joined by a blank line) at the version
given, and states the version it revises. The SHACL shapes are not rewritten here.
usage: sen0414_chapter_build_v1_0_0.py NN NEWVERSION PRIORVERSION [DATE]      e.g.  02 1.1.0 1.0.1
The corpus supplies NODES (see ch01), CHAPTER, OWNERS, ERRORS, CQS, PROVENANCE, INTERPRETERS, CHANGE and the CHECKS list."""
__version__ = "1.0.0"
import os, sys, glob, re, importlib.util, rdflib
from rdflib import RDF, RDFS, OWL
NN, NEW, PRIOR = sys.argv[1], sys.argv[2], sys.argv[3]; MODIFIED = sys.argv[4] if len(sys.argv) > 4 else "2026-10-01"
V = NEW.replace(".", "_"); here = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(here)
cands = sorted(glob.glob(os.path.join(here, "sen0414_ch%s_corpus_v*.py" % NN)), key=lambda f: [int(x) for x in re.search(r"_v(\d+_\d+_\d+)\.py", f).group(1).split("_")])
assert cands, "no corpus file for chapter " + NN
_sp = importlib.util.spec_from_file_location("corpus", cands[-1]); CORPUS = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(CORPUS)
OUT = os.path.join(REPO, "03-materials", "ch" + NN, "rdodi"); P = "ch" + NN
BASE = "http://example.org/sen0414/" + P
RESEARCH = BASE + "/research"
CREATED = {}
old = sorted(glob.glob(os.path.join(OUT, "sen0414_%s_domain_tbox_v*.ttl" % P)))
m = re.search(r'dcterms:created "([0-9-]+)"', open(old[0]).read()) if old else None
CREATED = m.group(1) if m else MODIFIED
PFX = '''@prefix %s:    <http://example.org/sen0414/%s#> .
@prefix rd:      <http://example.org/rdodi/domain-ontology#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
''' % (P, P)
q = lambda s: s.replace('"', "'")
def header(iri, label, ident):
    return '''<%s> a owl:Ontology ;
    rdfs:label "%s"@en ; owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; rdfs:comment "%s"@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%s"^^xsd:date ; dcterms:modified "%s"^^xsd:date ;
    dcterms:identifier "%s" ; prov:wasRevisionOf <%s/%s> ;
    prov:wasGeneratedBy <http://example.org/sen0414/activity/%s-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
''' % (iri, label, NEW, iri, NEW, q(CORPUS.CHANGE), CREATED, MODIFIED, ident, iri, PRIOR, P)
byid = {n[0]: n for n in CORPUS.NODES}
def top(i):
    while byid[i][3]: i = byid[i][3]
    return i
TAX = [(top(n[0]), n[3], n[0], n[4][0], n[4][1], n[4][2]) for n in CORPUS.NODES if n[2] == 3]
LABELS = {n[0]: n[1] for n in CORPUS.NODES if n[1]}
def tbox():
    L = [PFX, header(BASE + "/tbox", "SEN0414 chapter %d domain ontology - TBox" % int(NN), "sen0414_%s_domain_tbox_v%s" % (P, V))]
    seen = set()
    for t, mid, leaf, *_ in TAX:
        for c, parent in ((t, None), (mid, t), (leaf, mid)):
            if c in seen: continue
            seen.add(c)
            label = LABELS.get(c) or "".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip()
            L.append('%s:%s a owl:Class ; rdfs:label "%s"@en ;%s rdfs:isDefinedBy <%s/tbox> .' % (P, c, label[0].upper() + label[1:], (" rdfs:subClassOf %s:%s ;" % (P, parent)) if parent else "", BASE))
    tops = sorted({t[0] for t in TAX})
    for i, a in enumerate(tops):
        for b in tops[i + 1:]: L.append("%s:%s owl:disjointWith %s:%s ." % (P, a, P, b))
    L.append('%s:hasOwner a owl:ObjectProperty ; rdfs:label "owned by"@en ; rdfs:subPropertyOf rd:hasOwningConcept .' % P)
    return "\n".join(L) + "\n"
def abox():
    L = [PFX, header(BASE + "/abox", "SEN0414 chapter %d domain ontology - ABox" % int(NN), "sen0414_%s_domain_abox_v%s" % (P, V))]
    for t, mid, leaf, ex, d, io in TAX:
        L.append('%s:X_%s a owl:NamedIndividual, %s:%s ; rdfs:label "%s"@en ; skos:definition "%s"@en ; dcterms:source <%s> .' % (P, leaf, P, leaf, q(ex), q(d), RESEARCH))
        if io:
            L.append('%s:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; %s:input "%s" ; %s:output "%s" .' % (P, leaf, q(io[0]), q(io[1]), P, q(io[0]), P, q(io[1])))
            L.append("%s:X_%s rd:hasIOExample %s:IO_%s ." % (P, leaf, P, leaf))
    for leaf, owner in getattr(CORPUS, "OWNERS", []): L.append("%s:X_%s %s:hasOwner %s:X_%s ." % (P, leaf, P, P, owner))
    for leaf, text in getattr(CORPUS, "ERRORS", []):
        L.append('%s:Err_%s a owl:NamedIndividual, rd:ErrorCondition ; rdfs:label "%s"@en .' % (P, leaf, text.replace('"', "'").replace("\\", "\\\\")))
        L.append("%s:X_%s rd:hasErrorCondition %s:Err_%s ." % (P, leaf, P, leaf))
    cq = ["%s:CQ%d" % (P, i + 1) for i in range(len(CORPUS.CQS))]
    L.append('''
%(p)s:Artifact a owl:NamedIndividual, rd:DomainOntologyArtifact ; rdfs:label "SEN0414 chapter %(n)d domain ontology"@en ;
    rd:derivedFromResearchSubject <%(r)s> ;
    rd:hasCompetencyQuestion %(p)s:CQs ; rd:hasSourceProvenance %(p)s:Provenance ;
    rd:hasReusabilityScope rd:RS_SubjectSpecific ; rd:hasResolutionEnvironment %(p)s:Env .
%(p)s:CQs a owl:NamedIndividual, rd:CompetencyQuestionSet ; rdfs:label "Chapter %(n)d competency questions"@en ;
    rd:containsCompetencyQuestion %(cq)s .''' % dict(p=P, n=int(NN), r=RESEARCH, cq=", ".join(cq)))
    for c, text in zip(cq, CORPUS.CQS): L.append('%s a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "%s"@en .' % (c, q(text)))
    L.append('''%(p)s:Provenance a owl:NamedIndividual, rd:ResearchSubjectInput ; rdfs:label "Derived from the chapter %(n)d research artefact"@en ;
    skos:definition "%(prov)s"@en ;
    dcterms:source <%(r)s> .
%(p)s:Env a owl:NamedIndividual, rd:ResolutionEnvironment ; rdfs:label "%(env)s"@en ;
    skos:definition "Every input-output example and error condition, and every quoted result in the chapter text (%(k)d checks listed in %(cf)s), executed under %(env)s: identical output where more than one was used."@en ;
    dcterms:source "The execution run recorded with this ontology's build, 08-tooling/sen0414_chapter_build_v1_0_0.py, and the claims check in 08-tooling/%(cf)s" .
''' % dict(p=P, n=int(NN), prov=q(CORPUS.PROVENANCE), r=RESEARCH, env=CORPUS.INTERPRETERS, k=len(CORPUS.CHECKS) + len(CORPUS.RAISES), cf=os.path.basename(cands[-1])))
    return "\n".join(L) + "\n"
def document():
    T = rdflib.Graph(); T.parse(os.path.join(OUT, "sen0414_%s_domain_tbox_v%s.ttl" % (P, V)), format="turtle")
    BODY = {n[0]: CORPUS.facet_text(n[5]) for n in CORPUS.NODES}; BO = list(BODY); ORDER = []
    def walk(c, level, parent):
        ORDER.append((c, level, parent))
        for k in sorted(T.subjects(RDFS.subClassOf, c), key=lambda k: BO.index(str(k).split('#')[-1])): walk(k, level + 1, c)
    for t in sorted([c for c in T.subjects(RDF.type, OWL.Class) if not list(T.objects(c, RDFS.subClassOf))], key=lambda c: BO.index(str(c).split('#')[-1])): walk(t, 1, None)
    D = BASE + "/document"
    L = ['@prefix doc:     <http://example.org/rdodi/document-ontology#> .', '@prefix %s:    <http://example.org/sen0414/%s#> .' % (P, P), '@prefix chd:     <%s#> .' % D,
         '@prefix owl:     <http://www.w3.org/2002/07/owl#> .', '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .', '@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .',
         '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .', '@prefix dcterms: <http://purl.org/dc/terms/> .', '@prefix prov:    <http://www.w3.org/ns/prov#> .', '',
         '''<%(d)s> a owl:Ontology ;
    rdfs:label "SEN0414 chapter %(n)d - RDODI Stage 3 document"@en ; owl:versionInfo "%(v)s" ; owl:versionIRI <%(d)s/%(v)s> ; prov:wasRevisionOf <%(d)s/%(pr)s> ;
    rdfs:comment "%(c)s"@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ; dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:created "%(cr)s"^^xsd:date ; dcterms:modified "%(m)s"^^xsd:date ;
    dcterms:identifier "sen0414_%(p)s_document_v%(V)s" ; prov:wasGeneratedBy <http://example.org/sen0414/activity/%(p)s-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .''' % dict(d=D, n=int(NN), v=NEW, pr=PRIOR, c=q(CORPUS.CHANGE), cr=CREATED, m=MODIFIED, p=P, V=V), '',
         'chd:Document a doc:ReportSection ; rdfs:label "%s"@en ; skos:definition "%s" ;' % (q(getattr(CORPUS, "DOC_TITLE", "SEN0414 chapter %d" % int(NN))), q(getattr(CORPUS, "DOC_ABOUT", ""))),
         '    dcterms:source <%s> ;' % RESEARCH, '    doc:hasSection ' + ", ".join("chd:S_%s" % str(c).split('#')[-1] for c, lv, p in ORDER if lv == 1) + ' .', '']
    for n, (c, lv, p) in enumerate(ORDER, 1):
        name = str(c).split('#')[-1]; title = str(T.value(c, RDFS.label)); kind = "doc:TaxonomicSection" if lv < 3 else "doc:ConceptSection"
        L.append('chd:S_%s a %s ; rdfs:label "%s"@en ; doc:sectionTitle "%s" ; doc:hierarchyLevel %d ; doc:sectionOrder %d ;' % (name, kind, title, title, lv, n))
        L.append('    skos:definition "%s" ;' % BODY[name].replace('"', "'").replace("\n", "\\n"))
        if p is not None: L.append('    doc:hasParentSection chd:S_%s ;' % str(p).split('#')[-1])
        L.append('    dcterms:source <http://example.org/sen0414/%s#%s> .' % (P, name))
    open(os.path.join(OUT, "sen0414_%s_document_v%s.ttl" % (P, V)), "w").write("\n".join(L) + "\n"); return len(ORDER)
for name, fn in (("tbox", tbox), ("abox", abox)):
    open(os.path.join(OUT, "sen0414_%s_domain_%s_v%s.ttl" % (P, name, V)), "w").write(fn())
print("chapter", NN, "ontology", NEW, "- sections:", document())
