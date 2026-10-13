#!/usr/bin/env python3
"""SEN0414, chapter 22 (Recognizing Text in Images, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case diagram, the life of a thing a state
diagram, an exchange between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to diagram type lives in
the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts
whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations
the content draws on), one sentence saying why the pattern fits, and the diagram's content in the element names the renderer of that type expects. Every
element label is made of words that occur in the first paragraph and the definition of the accompanying concepts or their section, which is the text the page
shows; run_checks() measures that (the grounding ratio, required here to be 0.84 or more) besides the structural rules. This module follows the layout of
sen0414_ch21_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another chapter is not edited); nodes_from_ttl()
builds the node list from the chapter's RDODI v1_0_2 document and ABox, so the grounding is measured on the section's first paragraph, which is what the page
uses as the body.

Usage: python3 sen0414_ch22_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "ReadingAnImageInFourLines",
        "pattern": "Workflow",
        "title": "Reading the text of an image file with four lines of Python",
        "concepts": ["OpenImage", "ImageToString", "ReturnType", "PillowCoupling"],
        "also_from": ["TheFourLines", "PathLookup", "FrankensteinOutput", "ReadingAnImage"],
        "read_from": "chapter 22, Reading Text from Images: import pytesseract and Pillow, open the image with Image.open(), pass it to image_to_string() and print the "
                     "string that comes back",
        "why": "the passage is a short sequence of steps, each of which uses the result of the one before it: a workflow",
        "data": {
            "nodes": [
                {"id": "imp", "label": "Import pytesseract and Pillow"},
                {"id": "open", "label": "Open the image file with Image.open()"},
                {"id": "read", "label": "Pass the image to image_to_string()"},
                {"id": "str", "label": "Receive a str that ends with a newline"},
                {"id": "show", "label": "Print the string"},
            ],
            "flows": [["start", "imp"], ["imp", "open"], ["open", "read"], ["read", "str"], ["str", "show"], ["show", "end"]],
        },
    },
    {
        "id": "CleaningAPageBeforeReadingIt",
        "pattern": "Workflow",
        "title": "Cleaning a page before Tesseract reads it",
        "concepts": ["GrayscaleConversion", "Upscaling", "WhiteBorder", "Deskew", "Binarization"],
        "also_from": ["WhatHelps", "AccuracyAndPreprocessing", "SmallText", "Skew", "NoiseLevel", "WhiteOnBlack"],
        "read_from": "chapter 22, the advice on preprocessing: convert the picture to grey, enlarge small text, add a white border, turn a skewed page back and "
                     "binarise it when that helps, then call image_to_string()",
        "why": "the passage is a sequence of steps with a test after each of them that sends the program to the next step or back to the reading: a workflow",
        "data": {
            "nodes": [
                {"id": "grey", "label": "Convert the picture to grey with convert('L')"},
                {"id": "small", "label": "Is the text smaller than about 10 pixels?", "kind": "decision"},
                {"id": "up", "label": "Enlarge the image with resize()"},
                {"id": "skew", "label": "Is the page turned by a few degrees?", "kind": "decision"},
                {"id": "turn", "label": "Estimate the angle and turn the image back"},
                {"id": "border", "label": "Add a white border around the text"},
                {"id": "read", "label": "Call image_to_string() and measure the error rate"},
            ],
            "flows": [["start", "grey"], ["grey", "small"], ["small", "up", "yes"], ["small", "skew", "no"], ["up", "skew"], ["skew", "turn", "yes"], ["skew", "border", "no"],
                      ["turn", "border"], ["border", "read"], ["read", "end"]],
        },
    },
    {
        "id": "MakingASearchablePdfWithNaps2",
        "pattern": "Workflow",
        "title": "Making a searchable PDF with NAPS2 from a program",
        "concepts": ["NapsCommand", "NapsOverwrite", "NapsInputLanguage", "SubprocessRun", "ProgramNotFound"],
        "also_from": ["Naps2", "NapsPackage", "SearchablePdfs", "OtherPdfRoutes"],
        "read_from": "chapter 22, the section on NAPS2: run naps2 console with subprocess.run(), name the input image, the output PDF and the language, give -f to "
                     "overwrite and read the PDF text back",
        "why": "the passage is a sequence of steps with a test on whether the program is found and one on whether the output file already exists: a workflow",
        "data": {
            "nodes": [
                {"id": "build", "label": "Name the input image, the output PDF and the language"},
                {"id": "run", "label": "Call subprocess.run() with naps2 console"},
                {"id": "found", "label": "Is the program found?", "kind": "decision"},
                {"id": "fail", "label": "subprocess.run() raises FileNotFoundError"},
                {"id": "exists", "label": "Does the output file already exist and is -f missing?", "kind": "decision"},
                {"id": "refuse", "label": "Add -f to overwrite the file"},
                {"id": "pdf", "label": "Read the text of the PDF"},
            ],
            "flows": [["start", "build"], ["build", "run"], ["run", "found"], ["found", "fail", "no"], ["found", "exists", "yes"], ["fail", "end"], ["exists", "refuse", "yes"],
                      ["exists", "pdf", "no"], ["refuse", "run"], ["pdf", "end"]],
        },
    },
    {
        "id": "ProgramTalkingToTesseract",
        "pattern": "Interaction",
        "title": "A program asking Tesseract to read an image through pytesseract",
        "concepts": ["PathLookup", "ImageToString", "TimeoutArgument", "MissingLanguage"],
        "also_from": ["TheEngine", "EngineVersion", "LanguageFolder", "TheWrapper", "WrongLanguage"],
        "read_from": "chapter 22, Installing Tesseract and PyTesseract and Reading Text from Images: pytesseract starts the tesseract program, hands it the image and the "
                     "language, and returns what the program prints",
        "why": "the passage is an exchange between the program, the wrapper and the engine in an order that matters - the call goes out before the text comes back: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The Python program"},
                {"id": "wrap", "label": "pytesseract"},
                {"id": "eng", "label": "The tesseract program"},
            ],
            "messages": [
                ["prog", "wrap", "Calls image_to_string() with an image"],
                ["wrap", "eng", "Starts tesseract and hands it the image"],
                ["eng", "wrap", "Prints the text it recognised", "reply"],
                ["wrap", "prog", "Returns the text as a string", "reply"],
                ["prog", "wrap", "Calls image_to_string() with a language it does not have"],
                ["eng", "wrap", "Reports an error opening the data file", "reply"],
                ["wrap", "prog", "Raises TesseractError", "reply"],
            ],
        },
    },
    {
        "id": "AskingNaps2ToOverwriteAFile",
        "pattern": "Interaction",
        "title": "A program running NAPS2 twice on the same output file",
        "concepts": ["NapsOverwrite", "NapsCommand", "SubprocessRun"],
        "also_from": ["Naps2", "NapsPackage", "ProgramNotFound"],
        "read_from": "chapter 22, the section on NAPS2: the first run writes output.pdf, a second run without -f finds the file and refuses, and the run with -f writes it again",
        "why": "the passage is an exchange between the program and NAPS2 in an order that matters - the second run meets the file the first run wrote: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The Python program"},
                {"id": "naps", "label": "NAPS2"},
            ],
            "messages": [
                ["prog", "naps", "Runs naps2 console with -f"],
                ["naps", "prog", "Writes output.pdf and returns 0", "reply"],
                ["prog", "naps", "Runs naps2 console without -f"],
                ["naps", "prog", "Prints File already exists and still returns 0", "reply"],
                ["prog", "naps", "Runs naps2 console with -f again"],
                ["naps", "prog", "Writes the file again and returns 0", "reply"],
            ],
        },
    },
    {
        "id": "TheLifeOfAScannedPage",
        "pattern": "LifeCycle",
        "title": "A scanned page from a file on disk to corrected text",
        "concepts": ["OpenImage", "ImageToString", "RealWordErrors", "LowConfidenceWords", "SearchableOutputs"],
        "also_from": ["TheFourLines", "LlmCorrection", "OtherOutputs", "WhatHelps", "FrankensteinOutput"],
        "read_from": "chapter 22: an image file is opened, cleaned, read by Tesseract into a string, checked for the mistakes it makes and written out as text or as a "
                     "searchable PDF",
        "why": "the passage follows one page through the states it can be in and names the call that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "file", "label": "An image file"},
                {"id": "opened", "label": "An Image object"},
                {"id": "cleaned", "label": "A preprocessed image"},
                {"id": "read", "label": "A string"},
                {"id": "fixed", "label": "Text without the mistakes"},
                {"id": "pdf", "label": "A searchable PDF"},
            ],
            "initial": "file",
            "final": ["fixed", "pdf"],
            "transitions": [
                ["file", "opened", "Image.open() reads the file"],
                ["opened", "cleaned", "Convert to grey, resize and deskew"],
                ["opened", "read", "image_to_string() reads the image"],
                ["cleaned", "read", "image_to_string() reads the image"],
                ["read", "fixed", "A language model fixes the mistakes"],
                ["cleaned", "pdf", "image_to_pdf_or_hocr() makes the PDF"],
            ],
        },
    },
    {
        "id": "WhatPytesseractCanReturn",
        "pattern": "SetOfUses",
        "title": "What a program can ask pytesseract to return for an image",
        "concepts": ["ImageToString", "ImageToData", "SearchableOutputs", "OsdOrientation", "GetLanguages", "EngineVersion"],
        "also_from": ["OtherOutputs", "ConfidenceScale", "ReturnType", "PytesseractReleases", "LanguagePacks", "TheWrapper"],
        "read_from": "chapter 22 and the pytesseract documentation: the text of an image, the words with their boxes and confidence, a searchable PDF or hOCR page, "
                     "the orientation of a page, the languages installed and the version of the engine",
        "why": "the chapter lists independent things a program can ask for with the same wrapper - text, data, a PDF, an orientation, languages, a version - a set of uses, not a sequence",
        "data": {
            "system": "THE PYTESSERACT WRAPPER",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "text", "label": "Read the text with image_to_string()"},
                {"id": "data", "label": "Get words, boxes and confidence with image_to_data()"},
                {"id": "pdf", "label": "Make a searchable PDF with image_to_pdf_or_hocr()"},
                {"id": "osd", "label": "Find the orientation of a page with image_to_osd()"},
                {"id": "langs", "label": "List the languages with get_languages()"},
                {"id": "ver", "label": "Read the engine version with get_tesseract_version()"},
            ],
            "links": [["prog", "text"], ["prog", "data"], ["prog", "pdf"], ["prog", "osd"], ["prog", "langs"], ["prog", "ver"]],
        },
    },
    {
        "id": "RecognizingTextInImagesAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Recognizing text in images at a glance: six branches",
        "concepts": ["InstallingTheTools", "ReadingAnImage", "AccuracyAndPreprocessing", "LanguagesAndData", "SearchablePdfs", "BookAndPractice"],
        "also_from": ["TheEngine", "TheWrapper", "InstallerPlatforms", "TheFourLines", "WhatComesBack", "OtherOutputs", "MeasuringAccuracy", "WhatHurts", "WhatHelps",
                      "Segmentation", "ConfigStrings", "LanguagePacks", "ChoosingLanguage", "ModelKinds", "Naps2", "OtherPdfRoutes", "SubprocessAndInput", "LlmCorrection",
                      "ScreenScraper", "BookCorrections", "Interpreters", "FindLoaderBreak", "ExactResultsVary", "SmallText", "Skew", "Upscaling", "PsmModes", "AllLanguagesSize",
                      "IsoCodes", "FastBestLegacy", "NapsOverwrite", "OcrmypdfRoute", "RealWordErrors", "NoDisplay", "InversionAdvice", "PlaceholderLink", "ShippedScriptNames",
                      "PytesseractReleases", "WhiteOnBlack", "EngineVersion"],
        "read_from": "chapter 22, the opening of each of its main parts: installing Tesseract and PyTesseract, reading text from images, preprocessing, other languages, "
                     "searchable PDFs with NAPS2, and the book and its practice program",
        "why": "the chapter classifies one topic, reading text from pictures with a program, by what each part is about and lists examples under each - a topic and "
               "its parts, laid out to remember, with the one idea that holds for every part stated once at the root",
        "data": {
            "root": "A program reads the text of a picture with Tesseract and pytesseract",
            "branches": [
                {"label": "Installing the tools",
                 "children": ["pytesseract 0.3.10 stops on Python 3.14",
                              "The engine is a separate program",
                              "The data folder holds the languages"]},
                {"label": "Reading an image",
                 "children": ["image_to_string() returns a str",
                              "The first word varies with the engine",
                              "Hyphens at line ends stay in the text"]},
                {"label": "Accuracy and preprocessing",
                 "children": ["Small text and skew raise the error rate",
                              "Enlarging helps nine pixel text",
                              "psm 7 reads a single line"]},
                {"label": "Languages and data",
                 "children": ["The code is the data file name",
                              "The fast set holds 126 languages",
                              "Best data is larger than fast data"]},
                {"label": "Searchable PDFs",
                 "children": ["NAPS2 refuses to overwrite without -f",
                              "OCRmyPDF needs a dpi for an image",
                              "Pillow makes a PDF with no text"]},
                {"label": "The book and practice",
                 "children": ["The shipped script calls undefined names",
                              "The preprocessing link is a placeholder",
                              "The screen scraper needs a display"]},
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
    CHX = "http://example.org/sen0414/ch22#"
    d = os.path.join(root, "03-materials", "ch22", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch22_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch22_domain_abox_v1_0_2.ttl"))
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
