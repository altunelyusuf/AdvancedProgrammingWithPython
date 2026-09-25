#!/usr/bin/env python3
"""RDODI Stage 2 for SEN0414 chapter 1: the domain ontology (TBox, ABox, SHACL).

Every behaviour an individual claims was executed under both installed interpreters - Python 3.12.3
and Python 3.14.4, the current release, installed with uv - and printed identically in both. The
resolution environment says so. The taxonomy is the section structure Stage 3 will use.
"""
import os
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03-materials", "ch01", "rdodi")
CREATED = "2026-09-24"

def header(iri, label, ident):
    return '''<%s> a owl:Ontology ;
    rdfs:label "%s"@en ; owl:versionInfo "1.0.1" ; owl:versionIRI <%s/1.0.1> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%s"^^xsd:date ; dcterms:modified "%s"^^xsd:date ;
    dcterms:identifier "%s" ; prov:wasRevisionOf <%s/1.0.0> ;
    prov:wasGeneratedBy <http://example.org/sen0414/activity/ch01-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
''' % (iri, label, iri, CREATED, CREATED, ident, iri)

PFX = '''@prefix ch01:    <http://example.org/sen0414/ch01#> .
@prefix rd:      <http://example.org/rdodi/domain-ontology#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
'''
RESEARCH = "http://example.org/sen0414/ch01/research"

# (top, mid, leaf, exemplar, definition, io-example or None)
TAX = [
 ("Value", "NumericValue", "Integer", "the integer 2 ** 100", "A whole number. Python integers have unlimited precision, so 2 ** 100 is exact.", ("2 ** 100", "1267650600228229401496703205376")),
 ("Value", "NumericValue", "FloatingPoint", "the float sum 0.1 + 0.2", "A number with a fractional part, stored in binary, so some decimal values cannot be represented exactly.", ("0.1 + 0.2", "0.30000000000000004")),
 ("Value", "TextValue", "String", "the string 'Alice'", "A sequence of characters written between quotes.", ("'Alice' * 3", "'AliceAliceAlice'")),
 ("Operation", "ArithmeticOperation", "Precedence", "2 + 3 * 6 evaluated", "The order in which operators apply: ** first, then *, /, //, %, then + and -; parentheses override it.", ("2 + 3 * 6", "20")),
 ("Operation", "ArithmeticOperation", "IntegerDivision", "23 // 7 and 23 % 7", "Floor division gives the whole-number quotient; the modulus operator gives the remainder.", ("23 // 7", "3")),
 ("Operation", "TextOperation", "Concatenation", "'Alice' + 'Bob'", "Joining two strings with +. Joining a string to a number raises a TypeError.", ("'Alice' + 'Bob'", "'AliceBob'")),
 ("Operation", "TextOperation", "Replication", "'Alice' * 3", "Repeating a string an integer number of times with *.", ("'Alice' * 3", "'AliceAliceAlice'")),
 ("Operation", "BindingOperation", "Assignment", "spam = 42", "Storing a value in a variable with =; the variable names the value, and the name follows PEP 8's lower_case convention.", None),
 ("BuiltInFunction", "IOFunction", "Output", "print('Hello, world!')", "print() writes its arguments as text to the screen.", None),
 ("BuiltInFunction", "IOFunction", "Input", "input() reading a name", "input() waits for the user to type and always returns a string - input as text.", None),
 ("BuiltInFunction", "ConversionFunction", "TypeConversion", "int('42')", "str(), int() and float() convert a value between types; int() refuses a string that is not a whole number.", ("int('42')", "42")),
 ("BuiltInFunction", "MeasurementFunction", "Length", "len('hello')", "len() returns the number of characters in a string.", ("len('hello')", "5")),
 ("ExecutionEnvironment", "InteractiveEnvironment", "InteractiveShell", "the Python 3.13+ interactive interpreter", "The shell that evaluates expressions as they are typed. Python 3.13 replaced it with a better interactive interpreter.", None),
 ("ExecutionEnvironment", "InterpreterBuild", "FreeThreadedBuild", "CPython's experimental free-threaded build", "A build of CPython, experimental since 3.13, that can run threads in parallel - the preview of the course's multithreading outcome.", None),
 ("ModernPractice", "StringFormatting", "FString", "f'{2 ** 8}'", "An f-string evaluates expressions inside braces as it builds the string; PEP 701 gave f-strings a formal grammar.", ("f'{2 ** 8}'", "'256'")),
 ("ModernPractice", "Tooling", "PackageManager", "uv", "A tool that installs Python packages and interpreters. uv, built in Rust, was the most admired technology in the 2025 Stack Overflow survey.", None),
]

# Labels the camel-case rule mangles ("I o function", "F string", "Built in function"), fixed at source
# in v1.0.1 after the owner's review of the page showed them to students.
LABELS = {"BuiltInFunction": "built-in function", "IOFunction": "input-output function", "FString": "f-string",
          "FreeThreadedBuild": "free-threaded build", "IntegerDivision": "integer division"}
VER = "1_0_1"


def tbox():
    L = [PFX, header("http://example.org/sen0414/ch01/tbox", "SEN0414 chapter 1 domain ontology - TBox", "sen0414_ch01_domain_tbox_v%s" % VER)]
    seen = set()
    for top, mid, leaf, *_ in TAX:
        for c, parent in ((top, None), (mid, top), (leaf, mid)):
            if c in seen: continue
            seen.add(c)
            label = LABELS.get(c) or "".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip()
            L.append('ch01:%s a owl:Class ; rdfs:label "%s"@en ;%s rdfs:isDefinedBy <http://example.org/sen0414/ch01/tbox> .' % (
                c, label[0].upper() + label[1:], (" rdfs:subClassOf ch01:%s ;" % parent) if parent else ""))
    tops = sorted({t[0] for t in TAX})
    for i, a in enumerate(tops):
        for b in tops[i + 1:]:
            L.append("ch01:%s owl:disjointWith ch01:%s ." % (a, b))
    L.append('ch01:hasOwner a owl:ObjectProperty ; rdfs:label "owned by"@en ; rdfs:subPropertyOf rd:hasOwningConcept .')
    return "\n".join(L) + "\n"

def abox():
    L = [PFX, header("http://example.org/sen0414/ch01/abox", "SEN0414 chapter 1 domain ontology - ABox", "sen0414_ch01_domain_abox_v%s" % VER)]
    for n, (top, mid, leaf, ex, d, io) in enumerate(TAX, 1):
        L.append('ch01:X_%s a owl:NamedIndividual, ch01:%s ; rdfs:label "%s"@en ; skos:definition "%s"@en ; dcterms:source <%s> .' % (
            leaf, leaf, ex.replace('"', "'"), d.replace('"', "'"), RESEARCH))
        if leaf in ("Concatenation", "Replication"):
            L.append("ch01:X_%s ch01:hasOwner ch01:X_String ." % leaf)
        if io:
            L.append('ch01:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; ch01:input "%s" ; ch01:output "%s" .' % (
                leaf, io[0].replace('"', "'"), io[1].replace('"', "'"), io[0].replace('"', "'"), io[1].replace('"', "'")))
            L.append("ch01:X_%s rd:hasIOExample ch01:IO_%s ." % (leaf, leaf))
    L.append('ch01:Err_Concatenation a owl:NamedIndividual, rd:ErrorCondition ; rdfs:label "\'Alice\' + 42 raises TypeError: can only concatenate str (not int) to str"@en .')
    L.append("ch01:X_Concatenation rd:hasErrorCondition ch01:Err_Concatenation .")
    L.append('ch01:Err_TypeConversion a owl:NamedIndividual, rd:ErrorCondition ; rdfs:label "int(\'4.2\') raises ValueError: invalid literal for int() with base 10"@en .')
    L.append("ch01:X_TypeConversion rd:hasErrorCondition ch01:Err_TypeConversion .")
    L.append('''
ch01:Artifact a owl:NamedIndividual, rd:DomainOntologyArtifact ; rdfs:label "SEN0414 chapter 1 domain ontology"@en ;
    rd:derivedFromResearchSubject <%s> ;
    rd:hasCompetencyQuestion ch01:CQs ; rd:hasSourceProvenance ch01:Provenance ;
    rd:hasReusabilityScope rd:RS_SubjectSpecific ; rd:hasResolutionEnvironment ch01:Env .
ch01:CQs a owl:NamedIndividual, rd:CompetencyQuestionSet ; rdfs:label "Chapter 1 competency questions"@en ;
    rd:containsCompetencyQuestion ch01:CQ1, ch01:CQ2, ch01:CQ3 .
ch01:CQ1 a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "Which operations can raise an error, and which error?"@en .
ch01:CQ2 a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "Which examples show a value the chapter's own arithmetic might surprise a student with?"@en .
ch01:CQ3 a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "Which concepts reach beyond the 3rd edition into current Python, and on what source?"@en .
ch01:Provenance a owl:NamedIndividual, rd:ResearchSubjectInput ; rdfs:label "Derived from the chapter 1 research artefact"@en ;
    skos:definition "Concepts are corpus-derived from the 3rd edition's chapter 1 through the Stage 1 research artefact; the execution-environment and modern-practice branches are drawn from that artefact's secondary sources, not from the book."@en ;
    dcterms:source <%s> .
ch01:Env a owl:NamedIndividual, rd:ResolutionEnvironment ; rdfs:label "CPython 3.12.3 and CPython 3.14.4"@en ;
    skos:definition "Every input-output example and error condition executed under CPython 3.12.3 (system) and CPython 3.14.4 (installed with uv 2026-09-24): identical output in both."@en ;
    dcterms:source "The execution run recorded with this ontology's build, 08-tooling/sen0414_ch01_domain_build_v1_1_0.py" .
''' % (RESEARCH, RESEARCH))
    return "\n".join(L) + "\n"

def shacl():
    L = [PFX, header("http://example.org/sen0414/ch01/shacl", "SEN0414 chapter 1 domain ontology - shapes", "sen0414_ch01_domain_shacl_v%s" % VER)]
    L.append('''ch01:ExemplarShape a sh:NodeShape ; sh:targetClass owl:NamedIndividual ;
    sh:property [ sh:path rdfs:label ; sh:minCount 1 ; sh:severity sh:Violation ; sh:message "Every individual needs a label." ] .
ch01:ExemplarSourcedShape a sh:NodeShape ; sh:targetSubjectsOf skos:definition ;
    sh:property [ sh:path dcterms:source ; sh:minCount 1 ; sh:severity sh:Violation ; sh:message "A defined exemplar must cite its source." ] .
ch01:IOShape a sh:NodeShape ; sh:targetClass rd:IOExample ;
    sh:property [ sh:path ch01:input ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "An I/O example needs exactly one input." ] ;
    sh:property [ sh:path ch01:output ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "An I/O example needs exactly one output." ] .''')
    return "\n".join(L) + "\n"

for name, fn in (("tbox", tbox), ("abox", abox), ("shacl", shacl)):
    open(os.path.join(OUT, "sen0414_ch01_domain_%s_v%s.ttl" % (name, VER)), "w").write(fn())
print("written")
