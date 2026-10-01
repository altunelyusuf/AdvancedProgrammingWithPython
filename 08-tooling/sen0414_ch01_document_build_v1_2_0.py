#!/usr/bin/env python3
"""RDODI Stage 3 for SEN0414 chapter 1: the document.

Sections are derived mechanically from the Stage 2 TBox - one per class, titled with the class's own
label, in taxonomy order - and each carries a body with in-line (Surname, Year) citations to the Stage 1
sources. Every number quoted was executed (see the Stage 2 resolution environment).

1.2.0 (writes document version 1.1.0): each section is a set of paragraphs that answer what the concept is, why it matters,
where it is met and how it works (and what to watch for), taken from sen0414_ch01_corpus_v1_1_0.py; a paragraph opens with its
facet ('What it is: ...') and paragraphs are separated by a blank line. The sections follow the TBox of ontology version 1.1.0."""
__version__ = "1.2.0"
import os, importlib.util, rdflib
_sp = importlib.util.spec_from_file_location("corpus", os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0414_ch01_corpus_v1_1_0.py")); CORPUS = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(CORPUS)
from rdflib import RDF, RDFS, OWL
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03-materials", "ch01", "rdodi")
T = rdflib.Graph(); T.parse(os.path.join(R, "sen0414_ch01_domain_tbox_v1_1_0.ttl"), format="turtle")
CH = "http://example.org/sen0414/ch01#"

BODY = {n[0]: CORPUS.facet_text(n[5]) for n in CORPUS.NODES}

ORDER = []
def walk(c, level, parent):
    ORDER.append((c, level, parent))
    kids = [k for k in T.subjects(RDFS.subClassOf, c)]
    for k in sorted(kids, key=lambda k: BODY_ORDER.index(str(k).split('#')[-1])):
        walk(k, level + 1, c)
BODY_ORDER = list(BODY)
tops = sorted([c for c in T.subjects(RDF.type, OWL.Class) if not list(T.objects(c, RDFS.subClassOf))], key=lambda c: BODY_ORDER.index(str(c).split('#')[-1]))
for t in tops: walk(t, 1, None)

L = ['@prefix doc:     <http://example.org/rdodi/document-ontology#> .', '@prefix ch01:    <http://example.org/sen0414/ch01#> .',
     '@prefix chd:     <http://example.org/sen0414/ch01/document#> .', '@prefix owl:     <http://www.w3.org/2002/07/owl#> .',
     '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .', '@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .',
     '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .', '@prefix dcterms: <http://purl.org/dc/terms/> .', '@prefix prov:    <http://www.w3.org/ns/prov#> .', '',
     '''<http://example.org/sen0414/ch01/document> a owl:Ontology ;
    rdfs:label "SEN0414 chapter 1 - RDODI Stage 3 document"@en ; owl:versionInfo "1.1.0" ; owl:versionIRI <http://example.org/sen0414/ch01/document/1.1.0> ; prov:wasRevisionOf <http://example.org/sen0414/ch01/document/1.0.1> ;
    rdfs:comment "1.1.0 rewrites every section as paragraphs that say what the concept is, why it matters, where it is met and how it works, and adds the sections for the concepts the chapter used without explaining; additive, so MINOR."@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ; dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:created "2026-09-24"^^xsd:date ; dcterms:modified "2026-10-01"^^xsd:date ;
    dcterms:identifier "sen0414_ch01_document_v1_1_0" ; prov:wasGeneratedBy <http://example.org/sen0414/activity/ch01-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .''', '',
     'chd:Document a doc:ReportSection ; rdfs:label "Python basics for an advanced course"@en ; skos:definition "This document renews chapter 1 of the 3rd edition for an advanced course, pairing the book\'s basics with the Python students now run (Sweigart, 2025)." ;',
     '    dcterms:source <http://example.org/sen0414/ch01/research> ;',
     '    doc:hasSection ' + ", ".join("chd:S_%s" % str(c).split('#')[-1] for c, lv, p in ORDER if lv == 1) + ' .', '']
for n, (c, lv, p) in enumerate(ORDER, 1):
    name = str(c).split('#')[-1]; title = str(T.value(c, RDFS.label))
    kind = "doc:TaxonomicSection" if lv < 3 else "doc:ConceptSection"
    L.append('chd:S_%s a %s ; rdfs:label "%s"@en ; doc:sectionTitle "%s" ; doc:hierarchyLevel %d ; doc:sectionOrder %d ;' % (name, kind, title, title, lv, n))
    L.append('    skos:definition "%s" ;' % BODY[name].replace('"', "'").replace("\n", "\\n"))
    if p is not None: L.append('    doc:hasParentSection chd:S_%s ;' % str(p).split('#')[-1])
    L.append('    dcterms:source <%s%s> .' % (CH, name))
open(os.path.join(R, "sen0414_ch01_document_v1_1_0.ttl"), "w").write("\n".join(L) + "\n")
print("sections:", len(ORDER))
