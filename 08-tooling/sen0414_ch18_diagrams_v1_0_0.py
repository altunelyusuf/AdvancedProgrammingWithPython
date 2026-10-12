#!/usr/bin/env python3
"""SEN0414, chapter 18 (CSV, JSON, and XML Files, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case
diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and its parts a mind
map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of
cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts
whose explanations the content draws on), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects. Every element label is made of words that occur in the first paragraph
and the definition of the accompanying concepts or their section, which is the text the page shows; run_checks() measures
that (the grounding ratio, required here to be 0.84 or more) besides the structural rules. This module follows the layout of
sen0414_ch17_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another
chapter is not edited); because chapter 18 has no page data yet, nodes_from_ttl() builds the node list from the chapter's RDODI v1_0_2
document and ABox, so the grounding can be measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch18_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "ReadingACsvFile",
        "pattern": "Workflow",
        "title": "Reading a CSV file with a reader and a for loop",
        "concepts": ["ReaderObjects", "ReaderUsedOnce", "LoopSavesMemory", "ReaderEveryValueString"],
        "also_from": ["CsvModule", "CsvEncoding", "DefaultEncodingIsLocale", "LineNumVsRecords"],
        "read_from": "chapter 18, Reading Data from Reader Objects in a for Loop: pass the file object that open() returns to csv.reader(), "
                     "loop over the reader once, and read each row as a list of strings",
        "why": "the passage is the chapter's own sequence of steps for reading a file, each depending on the one before it, with one "
               "choice, whether another row is left in the reader: a workflow",
        "data": {
            "nodes": [
                {"id": "open", "label": "Open the file with open()"},
                {"id": "reader", "label": "Pass the file object to csv.reader()"},
                {"id": "loop", "label": "Loop over the reader in a for loop"},
                {"id": "row", "label": "Read a row as a list of strings"},
                {"id": "more", "label": "Is another row left?", "kind": "decision"},
                {"id": "again", "label": "Call open() and csv.reader() again to read the file again"},
            ],
            "flows": [["start", "open"], ["open", "reader"], ["reader", "loop"], ["loop", "row"], ["row", "more"],
                      ["more", "row", "yes"], ["more", "again", "no"], ["again", "end"]],
        },
    },
    {
        "id": "RemovingCsvHeaders",
        "pattern": "Workflow",
        "title": "Project 13: remove the header row from every CSV file",
        "concepts": ["Project13", "SkipHeaderWithNext", "EmptyAndHeaderOnly", "WriterDoubleSpacing"],
        "also_from": ["BookAndPractice", "LineNumVsRecords", "WriterObjects", "ReaderObjects"],
        "read_from": "chapter 18, Project 13: loop through the files that end in .csv, read each with csv.reader() and skip the first row, "
                     "and write the other rows to a new file in a folder called headerRemoved",
        "why": "the passage is a numbered sequence of steps with a repeated step for each file and one test, whether another "
               "file is left: a workflow",
        "data": {
            "nodes": [
                {"id": "find", "label": "Loop through the files that end in .csv"},
                {"id": "reader", "label": "Read the file with csv.reader()"},
                {"id": "skip", "label": "Skip the first row"},
                {"id": "write", "label": "Write the other rows to a new file"},
                {"id": "more", "label": "Is another file left?", "kind": "decision"},
            ],
            "flows": [["start", "find"], ["find", "reader"], ["reader", "skip"], ["skip", "write"], ["write", "more"],
                      ["more", "reader", "yes"], ["more", "end", "no"]],
        },
    },
    {
        "id": "ParsingUntrustedXml",
        "pattern": "Workflow",
        "title": "Parsing XML text that someone else wrote",
        "concepts": ["XmlSecurity", "DefusedxmlForbids", "BillionLaughsLimit", "ExternalEntityNotFetched"],
        "also_from": ["XmlFormat", "XmltodictEntitiesDisabled", "ElementTreeReading", "XmlLibraries"],
        "read_from": "chapter 18, XML: the chapter parses text with ET.fromstring() and gives no warning about untrusted input; the "
                     "Python documentation and defusedxml describe what to do with it",
        "why": "the passage walks through the choices that decide whether parsing text is safe, each answered by yes or no, "
               "with the step that follows: a workflow",
        "data": {
            "nodes": [
                {"id": "text", "label": "Receive XML text"},
                {"id": "trust", "label": "Did a source you trust write the text?", "kind": "decision"},
                {"id": "parse", "label": "Parse the text with ET.fromstring()"},
                {"id": "defused", "label": "Parse the text with defusedxml"},
                {"id": "forbid", "label": "Does the document have an entity?", "kind": "decision"},
                {"id": "error", "label": "Catch the exception that forbids the entity"},
                {"id": "use", "label": "Use the elements"},
            ],
            "flows": [["start", "text"], ["text", "trust"], ["trust", "parse", "yes"], ["trust", "defused", "no"], ["defused", "forbid"],
                      ["forbid", "error", "yes"], ["forbid", "use", "no"], ["parse", "use"], ["error", "end"], ["use", "end"]],
        },
    },
    {
        "id": "WritingACsvFileOnWindows",
        "pattern": "Interaction",
        "title": "A program writing rows with a writer and a file object",
        "concepts": ["WriterObjects", "WriterReturnsLength", "WriterTypes", "WriterDoubleSpacing"],
        "also_from": ["CsvModule", "CsvDialects", "ExcelDialect", "EmbeddedLineBreak"],
        "read_from": "chapter 18, Writer Objects: open() with newline='' returns a file object, csv.writer() returns a writer, "
                     "and writerow() writes a row to the file",
        "why": "the passage is an exchange between the program and the objects it uses in an order that matters - each "
               "call returns the object the next call needs: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "file", "label": "The file object"},
                {"id": "writer", "label": "The writer object"},
            ],
            "messages": [
                ["prog", "file", "Calls open() with newline=''"],
                ["file", "prog", "Returns the file object", "reply"],
                ["prog", "writer", "Calls csv.writer() with the file object"],
                ["writer", "prog", "Returns the writer object", "reply"],
                ["prog", "writer", "Calls writerow() with a list"],
                ["writer", "file", "Writes the row to the file"],
                ["writer", "prog", "Returns the length", "reply"],
            ],
        },
    },
    {
        "id": "AValueThroughJson",
        "pattern": "LifeCycle",
        "title": "A Python value through dumps, a file and loads",
        "concepts": ["TupleBecomesList", "KeysBecomeStrings", "FileRoundTrip", "UnsupportedTypesRaise"],
        "also_from": ["JsonTypes", "JsonFiles", "EnsureAscii", "IndentAndSeparators", "BomHandling"],
        "read_from": "chapter 18, JSON: json.dumps() turns a Python value into text, the text can be written to a file, and "
                     "json.loads() turns the text into a Python value again, with the changes the format makes",
        "why": "the passage follows one value through the states it can be in and names the event that moves it from each "
               "state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "py", "label": "A Python value"},
                {"id": "text", "label": "JSON text"},
                {"id": "file", "label": "A file of JSON"},
                {"id": "back", "label": "A Python value again"},
            ],
            "initial": "py",
            "final": ["back"],
            "transitions": [
                ["py", "text", "json.dumps() turns the value into text"],
                ["py", "py", "dumps() raises an error for a type it does not support"],
                ["text", "file", "The program writes the text to a file"],
                ["file", "back", "json.loads() turns the text into a value"],
                ["text", "back", "json.loads() turns the text into a value"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithCsv",
        "pattern": "SetOfUses",
        "title": "What a program can do with a CSV file through the csv module",
        "concepts": ["ReaderObjects", "WriterObjects", "DictReaderFirstRowKeys", "DictWriterExtraKey", "QuotingConstants", "TabDelimited", "FieldSizeLimit"],
        "also_from": ["CsvModule", "DictReadersWriters", "CsvDialects", "CsvLimits", "RestkeyRestval", "ExcelDialect"],
        "read_from": "chapter 18, the csv module: the module reads rows with a reader, writes rows with a writer, uses the first row "
                     "as keys with DictReader, and the chapter adds a different delimiter",
        "why": "the chapter lists independent things a program can do with the same module - read, write, key, quote, "
               "change the delimiter - a set of uses of the same module, not a sequence",
        "data": {
            "system": "A CSV FILE IN PYTHON",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "read", "label": "Read the rows of a file"},
                {"id": "write", "label": "Write rows to a file"},
                {"id": "dictread", "label": "Read rows as dictionaries"},
                {"id": "dictwrite", "label": "Write dictionaries as rows"},
                {"id": "tab", "label": "Change the delimiter to a tab"},
                {"id": "limit", "label": "Read a field above the size limit"},
            ],
            "links": [["prog", "read"], ["prog", "write"], ["prog", "dictread"], ["prog", "dictwrite"], ["prog", "tab"], ["prog", "limit"]],
        },
    },
    {
        "id": "WhatAProgramCanDoWithElementTree",
        "pattern": "SetOfUses",
        "title": "What a program can do with XML through xml.etree.ElementTree",
        "concepts": ["RootTagAndChildren", "TextNoneOrString", "IterDocumentOrder", "FindAndXPathSubset", "SubElementAndSet", "IndentPrettyPrint", "IterparseClear"],
        "also_from": ["ElementTreeReading", "ElementTreeWriting", "TostringSpaceBeforeSlash", "OtherParsers", "XmlLibraries"],
        "read_from": "chapter 18, xml.etree.ElementTree: the module reads the root and its children, the text of an element, "
                     "finds elements, builds elements and sets attributes, and turns the tree into text",
        "why": "the chapter lists independent things a program can do with the same module - read, find, build, print - "
               "a set of uses of the same module, not a sequence",
        "data": {
            "system": "AN XML DOCUMENT IN PYTHON",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "root", "label": "Read the root and its children"},
                {"id": "text", "label": "Read the text of an element"},
                {"id": "iter", "label": "Iterate over the elements in document order"},
                {"id": "find", "label": "Find elements with find() and findall()"},
                {"id": "sub", "label": "Add a SubElement and set an attribute"},
                {"id": "indent", "label": "Indent the tree to print it"},
                {"id": "iterparse", "label": "Clear elements while iterparse reads a large file"},
            ],
            "links": [["prog", "root"], ["prog", "text"], ["prog", "iter"], ["prog", "find"], ["prog", "sub"], ["prog", "indent"], ["prog", "iterparse"]],
        },
    },
    {
        "id": "CsvJsonAndXmlAtAGlance",
        "pattern": "TopicAndParts",
        "title": "CSV, JSON, and XML files at a glance: six branches",
        "concepts": ["CsvFormat", "CsvModule", "JsonFormat", "XmlFormat", "XmlLibraries", "BookAndPractice"],
        "also_from": ["CsvRules", "CsvEncoding", "ReaderObjects", "WriterObjects", "JsonSyntax", "JsonTypes", "JsonFiles", "XmlSyntax", "XmlNamespaces",
                      "XmlSecurity", "ElementTreeReading", "XmltodictLibrary", "FormatChoice", "ChapterAccuracy", "Project13"],
        "read_from": "chapter 18, the opening of each of its main branches: the CSV format, the csv module, JSON, XML, the XML libraries, "
                     "and the book and its practice programs",
        "why": "the chapter classifies one topic, plaintext data files, by what each branch is about and "
               "lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for "
               "every part stated once at the root",
        "data": {
            "root": "CSV, JSON, and XML are plaintext formats; a module reads and writes them",
            "branches": [
                {"label": "The CSV format",
                 "children": ["A field in quotes holds a comma",
                              "A doubled quote is an escape",
                              "The encoding is not named"]},
                {"label": "The csv module",
                 "children": ["A reader gives rows of strings",
                              "A reader can be looped over once",
                              "A writer needs newline=''"]},
                {"label": "JSON",
                 "children": ["A trailing comma is refused",
                              "A tuple becomes a list",
                              "Keys become strings"]},
                {"label": "XML",
                 "children": ["Tags are case sensitive",
                              "A namespace is part of a name",
                              "xsi:nil is not understood"]},
                {"label": "XML libraries",
                 "children": ["The text of an element is None or a string",
                              "xmltodict gives strings",
                              "iterparse clears elements"]},
                {"label": "The book and practice",
                 "children": ["Project 13 removes headers",
                              "next() skips the header",
                              "The chapter has a curly quote"]},
            ],
        },
    },
]
STOP = set("a an the of to in on and or is are be by it its for from with as at that this not yet no yes one every then".split())


def _labels(d):
    """every element label of a diagram, whatever its type"""
    x = d["data"]; out = []
    for n in x.get("nodes", []) + x.get("states", []) + x.get("actors", []) + x.get("usecases", []) + x.get("participants", []):
        out.append(n["label"] if isinstance(n, dict) else n)
    out += [f[2] for f in x.get("flows", []) + x.get("transitions", []) if len(f) > 2 and f[2]]
    out += [m[2] for m in x.get("messages", [])]
    for b in x.get("branches", []):
        out.append(b["label"]); out += b.get("children", [])
    if x.get("root"): out.append(x["root"])
    if x.get("system"): out.append(x["system"])
    return out


def grounding(d, nodes):
    """share of a diagram's content words that occur in the explanations of its concepts (and their section and subject)"""
    import re
    by = {n["id"]: n for n in nodes}
    ids = set(d["concepts"]) | set(d.get("also_from", []))
    for c in list(ids):
        n = by.get(c)
        while n and n.get("parent"):
            ids.add(n["parent"]); n = by.get(n["parent"])
    text = " ".join((by[c].get("body") or "") + " " + (by[c].get("definition") or "") + " " + by[c]["label"] for c in ids if c in by).lower()
    words = [w for w in re.findall(r"[a-z0-9][a-z0-9'-]*", " ".join(_labels(d)).lower()) if w not in STOP and len(w) > 1]
    hit = [w for w in words if w in text or w.rstrip("s") in text or (w + "s") in text]
    return len(hit), len(words), sorted(set(w for w in words if w not in hit))


def run_checks(nodes=None, mapping=None):
    """structural rules and, with the chapter's nodes, the grounding ratio; with the CME mapping, the pattern is known and its type is assigned"""
    bad = []
    ids = [d["id"] for d in DIAGRAMS]
    if len(ids) != len(set(ids)): bad.append("duplicate diagram ids")
    by = {n["id"]: n for n in nodes} if nodes else None
    for d in DIAGRAMS:
        for f in ("pattern", "title", "concepts", "read_from", "why", "data"):
            if not d.get(f): bad.append("%s: missing %s" % (d["id"], f))
        if by:
            for c in d["concepts"] + d.get("also_from", []):
                if c not in by: bad.append("%s: unknown concept %s" % (d["id"], c))
        if mapping:
            m = mapping.get(d["pattern"])
            if not m: bad.append("%s: pattern %s is not in the CME mapping" % (d["id"], d["pattern"]))
            else:
                d["type"] = m["types"][0]
        x = d["data"]
        if "flows" in x:
            nid = set(n["id"] for n in x["nodes"]) | {"start", "end"}
            for f in x["flows"]:
                if f[0] not in nid or f[1] not in nid: bad.append("%s: flow names an unknown node %r" % (d["id"], f))
            if not any(f[0] == "start" for f in x["flows"]) or not any(f[1] == "end" for f in x["flows"]): bad.append("%s: no start or no end" % d["id"])
            for n in x["nodes"]:
                if n.get("kind") == "decision" and len([f for f in x["flows"] if f[0] == n["id"]]) < 2: bad.append("%s: decision %s has fewer than two outgoing flows" % (d["id"], n["id"]))
        if "transitions" in x:
            sid = set(s["id"] if isinstance(s, dict) else s for s in x["states"])
            if x["initial"] not in sid: bad.append("%s: initial state unknown" % d["id"])
            for f in x.get("final", []):
                if f not in sid: bad.append("%s: final state unknown" % d["id"])
            for tr in x["transitions"]:
                if tr[0] not in sid or tr[1] not in sid or not tr[2]: bad.append("%s: transition %r unknown state or unlabelled" % (d["id"], tr))
        if "usecases" in x:
            aid = set(a["id"] for a in x["actors"]); uid = set(u["id"] for u in x["usecases"])
            for a, u in x["links"]:
                if a not in aid or u not in uid: bad.append("%s: link %r names an unknown actor or use case" % (d["id"], (a, u)))
            if uid - set(u for _, u in x["links"]): bad.append("%s: a use case has no actor" % d["id"])
        if "messages" in x:
            pid = set(p["id"] for p in x["participants"])
            for m in x["messages"]:
                if m[0] not in pid or m[1] not in pid or not m[2]: bad.append("%s: message %r unknown participant or empty" % (d["id"], m))
        if "branches" in x:
            if len(x["branches"]) < 2: bad.append("%s: a mind map needs at least two branches" % d["id"])
        for lab in _labels(d):
            if len(lab) > 72: bad.append("%s: label over 72 characters: %r" % (d["id"], lab))
        if nodes:
            h, n, miss = grounding(d, nodes)
            d["grounding"] = [h, n]
            if n and h / n < MIN_GROUNDING: bad.append("%s: grounding %d/%d below %.2f; words not in the concepts' explanations: %s" % (d["id"], h, n, MIN_GROUNDING, ", ".join(miss)))
    return bad


def nodes_from_ttl(root):
    """the chapter's nodes read from the v1_0_2 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch18#"
    d = os.path.join(root, "03-materials", "ch18", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch18_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch18_domain_abox_v1_0_2.ttl"))
    nodes = {}
    for s in g.subjects(DOC.sectionTitle, None):
        if not str(s).startswith(CHX + "S_"): continue
        cid = str(s)[len(CHX) + 2:]
        body = str(g.value(s, SKOS.definition) or "")
        nodes[cid] = {"id": cid, "label": str(g.value(s, RDFS.label)), "body": body.split("\n\n")[0], "definition": "", "parent": None, "_s": s}
    for cid, n in nodes.items():
        for p in list(g.subjects(DOC.hasSection, n["_s"])) + list(g.objects(n["_s"], DOC.hasParentSection)):
            q = str(p)[len(CHX) + 2:]
            if q in nodes: n["parent"] = q
        x = a.value(URIRef(CHX + "X_" + cid), SKOS.definition)
        if x: n["definition"] = str(x)
        del n["_s"]
    return list(nodes.values())


if __name__ == "__main__":
    import sys, os
    here = os.path.dirname(os.path.abspath(__file__))
    nodes = nodes_from_ttl(os.path.dirname(here))
    bad = run_checks(nodes)
    for d in DIAGRAMS: print("%-26s %-12s grounding %s" % (d["id"], d["pattern"], d.get("grounding")))
    print("\n".join(bad) or "all checks pass: %d diagrams, nodes %d" % (len(DIAGRAMS), len(nodes))); sys.exit(1 if bad else 0)
