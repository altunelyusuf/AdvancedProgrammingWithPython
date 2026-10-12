#!/usr/bin/env python3
"""SEN0414, chapter 17 (PDF and Word Documents, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
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
sen0414_ch16_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another
chapter is not edited); because chapter 17 has no page data yet, nodes_from_ttl() builds the node list from the chapter's RDODI
document and ABox, so the grounding can be measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch17_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "ReadingAPdfToText",
        "pattern": "Workflow",
        "title": "From an open PDF to a text file, with a fallback reader",
        "concepts": ["PdfReaderPages", "JoinedPagesNoSeparator", "PdfminerAlternative", "DamagedInput"],
        "also_from": ["ReadingPages", "ExtractionQuality", "PdfTextAndImages", "TextPostProcessing", "LayoutMode"],
        "read_from": "chapter 17, Extracting Text: open the file in binary read mode, build a PdfReader, loop over reader.pages, call "
                     "extract_text() and add the strings, fall back on pdfminer.six when PyPDF cannot understand the file, and write the text",
        "why": "the passage is the chapter's own sequence of steps, each depending on the one before it, with one choice "
               "after the file is opened, whether the reader raised an error: a workflow",
        "data": {
            "nodes": [
                {"id": "open", "label": "Open the PDF file with a PdfReader"},
                {"id": "loop", "label": "Loop over the pages of the reader"},
                {"id": "extract", "label": "Extract the text of each page"},
                {"id": "join", "label": "Join the texts of the pages"},
                {"id": "failed", "label": "Did the reader raise an error?", "kind": "decision"},
                {"id": "fallback", "label": "Read the file with the pdfminer.six alternative"},
                {"id": "write", "label": "Write the text to a file"},
            ],
            "flows": [["start", "open"], ["open", "failed"], ["failed", "fallback", "yes"], ["failed", "loop", "no"], ["loop", "extract"],
                      ["extract", "join"], ["join", "write"], ["fallback", "write"], ["write", "end"]],
        },
    },
    {
        "id": "CombiningManyPdfs",
        "pattern": "Workflow",
        "title": "Project 12: combine the pages after the first of many PDFs",
        "concepts": ["CombineAllPdfs", "CaseInsensitiveSort", "AppendRangeTuple", "WalkFindsAllPdfs"],
        "also_from": ["PracticePrograms", "PageSelection", "PdfWriterStartsEmpty", "ToolsAndPractice"],
        "read_from": "chapter 17, Project 12: find all PDF files in the working directory, sort them alphabetically, copy every page "
                     "after the first of each to an output PDF and save the output PDF to a file",
        "why": "the passage is a numbered sequence of steps with a repeated step for each file and one test, whether another "
               "file is left: a workflow",
        "data": {
            "nodes": [
                {"id": "find", "label": "Find all the PDF files of the folder"},
                {"id": "sort", "label": "Sort the filenames without regard to case"},
                {"id": "writer", "label": "Create a PdfWriter that starts with no pages"},
                {"id": "open", "label": "Open the next PDF with a PdfReader"},
                {"id": "copy", "label": "Append every page after the first page"},
                {"id": "more", "label": "Is another file left?", "kind": "decision"},
                {"id": "save", "label": "Write the combined PDF to a file"},
            ],
            "flows": [["start", "find"], ["find", "sort"], ["sort", "writer"], ["writer", "open"], ["open", "copy"], ["copy", "more"],
                      ["more", "open", "yes"], ["more", "save", "no"], ["save", "end"]],
        },
    },
    {
        "id": "ChoosingAStyle",
        "pattern": "Workflow",
        "title": "Choosing the style of a paragraph or a run",
        "concepts": ["StyleKindMismatch", "UnknownStyleKeyError", "StyleKindsOfTemplate", "CustomParagraphStyle"],
        "also_from": ["StyleSystem", "WordDocuments", "StyleIdLookupDeprecated"],
        "read_from": "chapter 17, Styling Paragraph and Run Objects: set the style attribute to the name of a style; a paragraph takes "
                     "a paragraph style, a run takes a character style, and a custom style is made before it is used",
        "why": "the passage walks through the choices that decide whether an assignment of a style works, each answered by yes or no, "
               "with the step that follows: a workflow",
        "data": {
            "nodes": [
                {"id": "name", "label": "Choose the name of a style"},
                {"id": "exists", "label": "Does the template have a style with that exact name?", "kind": "decision"},
                {"id": "make", "label": "Make a paragraph style with add_style()"},
                {"id": "kind", "label": "Is the style for a whole paragraph?", "kind": "decision"},
                {"id": "para", "label": "Assign it to the style of the paragraph"},
                {"id": "run", "label": "Assign it to the style of the run"},
                {"id": "save", "label": "Save the document"},
            ],
            "flows": [["start", "name"], ["name", "exists"], ["exists", "kind", "yes"], ["exists", "make", "no"], ["make", "para"],
                      ["kind", "para", "yes"], ["kind", "run", "no"], ["para", "save"], ["run", "save"], ["save", "end"]],
        },
    },
    {
        "id": "BuildingAWordDocument",
        "pattern": "Interaction",
        "title": "A program building a paragraph with two runs",
        "concepts": ["AddParagraphReturnsParagraph", "AddRunAppends", "TriStateBold", "RunsSplitAtFormatting"],
        "also_from": ["WordWriting", "BuildingContent", "RunFormatting", "ReadingText"],
        "read_from": "chapter 17, Writing Word Documents: add_paragraph() returns a Paragraph, add_run() returns a Run, and the program "
                     "sets the bold attribute of the run before it saves the document",
        "why": "the passage is an exchange between the program and the objects of the document in an order that matters - each "
               "call returns the object the next call needs: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "doc", "label": "The Document object"},
                {"id": "para", "label": "The Paragraph object"},
                {"id": "run", "label": "The Run object"},
            ],
            "messages": [
                ["prog", "doc", "Calls add_paragraph with the text"],
                ["doc", "prog", "Returns the new Paragraph", "reply"],
                ["prog", "para", "Calls add_run with more text"],
                ["para", "prog", "Returns the new Run", "reply"],
                ["prog", "run", "Sets bold to True"],
                ["prog", "doc", "Saves the document to a file"],
            ],
        },
    },
    {
        "id": "AnEncryptedPdfThroughItsLife",
        "pattern": "LifeCycle",
        "title": "A PDF from plain to encrypted to a decrypted copy",
        "concepts": ["EncryptAes256", "DecryptReturnValues", "ReaderRefusesBeforeDecrypt", "EmptyUserPassword"],
        "also_from": ["Protection", "PdfWriting", "EncryptRc4Default"],
        "read_from": "chapter 17, Encrypting and Decrypting PDFs: encrypt() with AES-256 makes the file unreadable without the password, "
                     "a reader cannot give pages until decrypt() matches a password, and a decrypted copy is written",
        "why": "the passage follows one PDF through the states it can be in and names the event that moves it from each "
               "state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "plain", "label": "A plain PDF"},
                {"id": "encrypted", "label": "An encrypted PDF file"},
                {"id": "locked", "label": "A reader that is not decrypted"},
                {"id": "unlocked", "label": "A reader that is decrypted"},
                {"id": "copy", "label": "A decrypted copy"},
            ],
            "initial": "plain",
            "final": ["copy"],
            "transitions": [
                ["plain", "encrypted", "The writer encrypts it with a password and writes the file"],
                ["encrypted", "locked", "A reader opens the encrypted file"],
                ["locked", "locked", "decrypt() returns NOT_DECRYPTED for a wrong password"],
                ["locked", "unlocked", "decrypt() matches the user or owner password"],
                ["unlocked", "copy", "A writer appends the pages and writes a new file"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithPdfs",
        "pattern": "SetOfUses",
        "title": "What a program can do with a PDF through pypdf",
        "concepts": ["PdfReaderPages", "ImageNameAndData", "AppendRangeTuple", "MergeInsertsAtPosition", "RotateMultiplesOf90", "WatermarkUnderlay", "EncryptAes256", "DecryptReturnValues"],
        "also_from": ["PdfTextAndImages", "PdfWriting", "PageSelection", "InsertAndMerge", "PageEditing", "Protection", "ImageExtraction", "ReadingPages"],
        "read_from": "chapter 17, PDF Documents: the package extracts text and images, copies pages into a new file, inserts pages, rotates "
                     "pages, merges a watermark or overlay, and encrypts and decrypts files",
        "why": "the chapter lists independent things a program can do with the same package - read, copy, insert, rotate, stamp, "
               "protect - a set of uses of the same module, not a sequence",
        "data": {
            "system": "A PDF FILE IN PYTHON",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "text", "label": "Extract the text of the pages"},
                {"id": "images", "label": "Extract the images of a page"},
                {"id": "copy", "label": "Copy pages into a new file"},
                {"id": "insert", "label": "Insert pages at a position"},
                {"id": "rotate", "label": "Rotate pages"},
                {"id": "mark", "label": "Merge a watermark under a page"},
                {"id": "encrypt", "label": "Encrypt a file with AES-256"},
                {"id": "decrypt", "label": "Decrypt a file with a password"},
            ],
            "links": [["prog", "text"], ["prog", "images"], ["prog", "copy"], ["prog", "insert"], ["prog", "rotate"], ["prog", "mark"], ["prog", "encrypt"], ["prog", "decrypt"]],
        },
    },
    {
        "id": "WhatAProgramCanDoWithWord",
        "pattern": "SetOfUses",
        "title": "What a program can do with a Word document through python-docx",
        "concepts": ["ParagraphsOfBody", "StyleKindMismatch", "AddHeadingLevels", "TriStateBold", "PageBreakRun", "PictureSizeFromWidth", "CustomParagraphStyle"],
        "also_from": ["WordDocuments", "WordWriting", "ReadingText", "StyleSystem", "BuildingContent", "RunFormatting", "BreaksAndPictures"],
        "read_from": "chapter 17, Word Documents: the package reads paragraphs and runs, styles them, writes paragraphs, headings, "
                     "run attributes, breaks and pictures, and saves the document",
        "why": "the chapter lists independent things a program can do with the same package - read, style, write, format, break, "
               "add a picture - a set of uses of the same module, not a sequence",
        "data": {
            "system": "A WORD DOCUMENT IN PYTHON",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "read", "label": "Read the paragraphs and runs"},
                {"id": "style", "label": "Set the style of a paragraph"},
                {"id": "make", "label": "Make a paragraph style"},
                {"id": "heading", "label": "Add headings of levels 0 to 9"},
                {"id": "bold", "label": "Set the bold attribute of a run"},
                {"id": "brk", "label": "Add a page break"},
                {"id": "pic", "label": "Add a picture with a width"},
            ],
            "links": [["prog", "read"], ["prog", "style"], ["prog", "make"], ["prog", "heading"], ["prog", "bold"], ["prog", "brk"], ["prog", "pic"]],
        },
    },
    {
        "id": "PdfAndWordAtAGlance",
        "pattern": "TopicAndParts",
        "title": "PDF and Word documents at a glance: six branches",
        "concepts": ["PdfFormat", "PdfTextAndImages", "PdfWriting", "WordDocuments", "WordWriting", "ToolsAndPractice"],
        "also_from": ["FileStructure", "TextAndLayout", "ReadingPages", "ExtractionQuality", "PageSelection", "Protection", "DocxPackage", "ReadingText",
                      "StyleSystem", "BuildingContent", "RunFormatting", "BreaksAndPictures", "PracticePrograms", "PackagesAndSetup"],
        "read_from": "chapter 17, the opening of each of its main branches: the PDF format, reading PDFs, writing PDFs, Word documents, "
                     "writing Word documents, and the tools and practice programs",
        "why": "the chapter classifies one topic, working with documents that people read, by what each branch is about and "
               "lists examples under each - a topic and its parts, laid out to remember, with the one idea that holds for "
               "every part stated once at the root",
        "data": {
            "root": "PDF and Word files are made for people; a program reads and writes them",
            "branches": [
                {"label": "The PDF format",
                 "children": ["A header, objects, a table and a trailer",
                              "Text is drawing commands in stream order",
                              "Text is not removed by a box"]},
                {"label": "Reading PDFs",
                 "children": ["The pages of a PdfReader start at index 0",
                              "Layout mode reads the page",
                              "Images are read from a page"]},
                {"label": "Writing PDFs",
                 "children": ["A tuple is a page range",
                              "Rotation adds up",
                              "AES-256 needs a package"]},
                {"label": "Word documents",
                 "children": ["A docx file is a ZIP archive of XML",
                              "A paragraph holds runs",
                              "A style has an exact name"]},
                {"label": "Writing Word documents",
                 "children": ["Headings have levels 0 to 9",
                              "Bold has three states",
                              "A picture is added from a width"]},
                {"label": "Tools and practice",
                 "children": ["Install python-docx and import docx",
                              "Project 12 joins the pages",
                              "A dictionary is tried in both cases"]},
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
    """the chapter's nodes read from the v1_0_1 document and ABox: id = class name, parent by the section tree, body = first paragraph, definition = the ABox individual's definition"""
    import os, re
    from rdflib import Graph, Namespace, RDFS, URIRef
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    DOC = Namespace("http://example.org/rdodi/document-ontology#")
    CHX = "http://example.org/sen0414/ch17#"
    d = os.path.join(root, "03-materials", "ch17", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch17_document_v1_0_1.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch17_domain_abox_v1_0_1.ttl"))
    nodes = {}
    for s in g.subjects(DOC.sectionTitle, None):
        if not str(s).startswith(CHX + "S_"): continue
        cid = str(s)[len(CHX) + 2:]
        body = str(g.value(s, SKOS.definition) or "")
        nodes[cid] = {"id": cid, "label": str(g.value(s, RDFS.label)), "body": body.split("\n\n")[0], "definition": "", "parent": None, "_s": s}
    for cid, n in nodes.items():
        for p in g.subjects(DOC.hasSection, n["_s"]):
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
