#!/usr/bin/env python3
"""RDODI Stage 3 for SEN0414 chapter 1: the document.

Sections are derived mechanically from the Stage 2 TBox - one per class, titled with the class's own
label, in taxonomy order - and each carries a body with in-line (Surname, Year) citations to the Stage 1
sources. Every number quoted was executed (see the Stage 2 resolution environment)."""
__version__ = "1.1.1"
import os, rdflib
from rdflib import RDF, RDFS, OWL
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "03-materials", "ch01", "rdodi")
T = rdflib.Graph(); T.parse(os.path.join(R, "sen0414_ch01_domain_tbox_v1_0_1.ttl"), format="turtle")
CH = "http://example.org/sen0414/ch01#"

BODY = {
 "Value": "Every Python expression reduces to a value, and every value has a data type that decides what can be done with it (Sweigart, 2025). Chapter 1 works with three, in its section The Integer, Floating-Point, and String Data Types: integers, floating-point numbers and strings (Python Software Foundation, 2026).",
 "NumericValue": "Integers and floating-point numbers look alike in the shell but are stored differently: integers exactly, floats in binary with a fixed precision (Python Software Foundation, 2026).",
 "Integer": "A Python integer has unlimited precision, so 2 ** 100 evaluates exactly to 1267650600228229401496703205376 rather than overflowing as in many languages (Python Software Foundation, 2026).",
 "FloatingPoint": "Floats are stored in binary, so some decimal fractions cannot be represented exactly: 0.1 + 0.2 evaluates to 0.30000000000000004, and round(0.1 + 0.2, 2) gives 0.3 - the reason behind the chapter's closing section, How Computers Store Data with Binary Numbers (Python Software Foundation, 2026).",
 "TextValue": "Text is a value like any other, and the chapter treats strings with the same expression rules it uses for numbers (Sweigart, 2025).",
 "String": "A string is a sequence of characters between quotes, and the same operators that act on numbers act on strings with a different meaning (Sweigart, 2025).",
 "Operation": "Operators combine values into new values, and the rules for which operator applies first are fixed by the language, not by the reader (Python Software Foundation, 2026).",
 "ArithmeticOperation": "The chapter introduces seven arithmetic operators - +, -, *, /, //, % and ** - evaluated in a documented order (Sweigart, 2025).",
 "Precedence": "Operator precedence decides the result: 2 + 3 * 6 evaluates to 20, while (2 + 3) * 6 evaluates to 30, because ** binds first, then *, /, // and %, then + and -, and parentheses override the order (Python Software Foundation, 2026).",
 "IntegerDivision": "Floor division and the modulus operator split a division into its whole part and its remainder: 23 // 7 is 3 and 23 % 7 is 2, while 23 / 7 gives the float 3.2857142857142856 (Sweigart, 2025).",
 "TextOperation": "Two operators work on strings: + joins them and * repeats them, which the chapter calls string concatenation and replication (Sweigart, 2025).",
 "Concatenation": "String concatenation joins two strings with +, so 'Alice' + 'Bob' gives 'AliceBob'; joining a string to a number raises a TypeError, because Python does not convert types silently (Sweigart, 2025).",
 "Replication": "String replication repeats a string with an integer, so 'Alice' * 3 gives 'AliceAliceAlice' (Sweigart, 2025).",
 "BindingOperation": "Assignment is the operation that gives a value a name, so later expressions can use it (Sweigart, 2025).",
 "Assignment": "An assignment statement stores a value in a variable with the = operator, as the chapter's section Storing Values in Variables shows; PEP 8 recommends lower_case names with underscores for variables (Van Rossum et al., 2001).",
 "BuiltInFunction": "Chapter 1's first program uses six built-in functions - print, input, len, str, int and float - which are always available without importing anything; the sections Your First Program and Dissecting the Program walk through them line by line (Python Software Foundation, 2026).",
 "IOFunction": "Two built-in functions connect a program to its user: print sends text out, and input reads text in (Sweigart, 2025).",
 "Output": "The print function writes its arguments to the screen as text, which is how the first program says hello (Sweigart, 2025).",
 "Input": "The input function waits for the user to type and always returns a string, so a number typed at the keyboard arrives as text - the chapter's point about input as text (Sweigart, 2025).",
 "ConversionFunction": "Because input returns text, programs convert values between types with str, int and float (Python Software Foundation, 2026).",
 "TypeConversion": "The conversion functions change a value's type, so int('42') gives 42 and str(29) gives '29'; int('4.2') raises a ValueError because the text is not a whole number (Python Software Foundation, 2026).",
 "MeasurementFunction": "Some built-in functions measure a value rather than convert it, and len is the first the chapter uses (Sweigart, 2025).",
 "Length": "The len function returns the number of characters in a string, so len('hello') is 5 (Python Software Foundation, 2026).",
 "ExecutionEnvironment": "Where code runs matters as much as what it says, and the Python students run in 2026 is newer than the one the chapter describes: 3.14 is the current release and 3.15 arrives on 1 October 2026 (Python Software Foundation, 2026).",
 "InteractiveEnvironment": "The chapter starts with Entering Expressions into the Interactive Shell, where each expression is evaluated as soon as it is entered (Sweigart, 2025).",
 "InteractiveShell": "Python 3.13 replaced the interactive shell with a better interactive interpreter and improved its error messages, which changes what students see from their first expression (Python Software Foundation, 2026).",
 "InterpreterBuild": "CPython is built in more than one way, and the build decides how programs can use the machine (Python Software Foundation, 2026).",
 "FreeThreadedBuild": "Python 3.13 introduced an experimental free-threaded build of CPython and an experimental just-in-time compiler, which previews the course's multithreading outcome (Python Software Foundation, 2026).",
 "ModernPractice": "An advanced course teaches the current idiom alongside the book's basics, so the chapter's string building and first program are paired with today's tools (Galindo Salgado et al., 2022).",
 "StringFormatting": "Building strings by concatenation works, but formatted string literals are the idiomatic way to mix text and values (Galindo Salgado et al., 2022).",
 "FString": "An f-string evaluates expressions inside braces as it builds the string, so f'{2 ** 8}' gives '256'; PEP 701 gave f-strings a formal grammar for Python 3.12 (Galindo Salgado et al., 2022).",
 "Tooling": "A Python programmer works through tools as much as through the language, starting with how packages and interpreters are installed (Stack Overflow, 2025).",
 "PackageManager": "uv installs Python packages and interpreters; built in Rust, it was the most admired technology in the 2025 Stack Overflow survey at 74 per cent, and it installed the Python 3.14.4 used to check this chapter's examples (Stack Overflow, 2025).",
}

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
    rdfs:label "SEN0414 chapter 1 - RDODI Stage 3 document"@en ; owl:versionInfo "1.0.1" ; prov:wasRevisionOf <http://example.org/sen0414/ch01/document/1.0.0> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ; dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:created "2026-09-24"^^xsd:date ; dcterms:modified "2026-09-24"^^xsd:date ;
    dcterms:identifier "sen0414_ch01_document_v1_0_1" ; prov:wasGeneratedBy <http://example.org/sen0414/activity/ch01-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .''', '',
     'chd:Document a doc:ReportSection ; rdfs:label "Python basics for an advanced course"@en ; skos:definition "This document renews chapter 1 of the 3rd edition for an advanced course, pairing the book\'s basics with the Python students now run (Sweigart, 2025)." ;',
     '    dcterms:source <http://example.org/sen0414/ch01/research> ;',
     '    doc:hasSection ' + ", ".join("chd:S_%s" % str(c).split('#')[-1] for c, lv, p in ORDER if lv == 1) + ' .', '']
for n, (c, lv, p) in enumerate(ORDER, 1):
    name = str(c).split('#')[-1]; title = str(T.value(c, RDFS.label))
    kind = "doc:TaxonomicSection" if lv < 3 else "doc:ConceptSection"
    L.append('chd:S_%s a %s ; rdfs:label "%s"@en ; doc:sectionTitle "%s" ; doc:hierarchyLevel %d ; doc:sectionOrder %d ;' % (name, kind, title, title, lv, n))
    L.append('    skos:definition "%s" ;' % BODY[name].replace('"', "'"))
    if p is not None: L.append('    doc:hasParentSection chd:S_%s ;' % str(p).split('#')[-1])
    L.append('    dcterms:source <%s%s> .' % (CH, name))
open(os.path.join(R, "sen0414_ch01_document_v1_0_1.ttl"), "w").write("\n".join(L) + "\n")
print("sections:", len(ORDER))
