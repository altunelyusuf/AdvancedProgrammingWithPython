#!/usr/bin/env python3
"""SEN0414, chapter 21 (Making Graphs and Manipulating Images, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case diagram, the life of a thing a state
diagram, an exchange between parties a sequence diagram, a topic and its parts a mind map - and the mapping from narrative pattern to diagram type lives in
the CME ontology (the narrative-to-diagram module of cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts
whose paragraphs it accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts whose explanations
the content draws on), one sentence saying why the pattern fits, and the diagram's content in the element names the renderer of that type expects. Every
element label is made of words that occur in the first paragraph and the definition of the accompanying concepts or their section, which is the text the page
shows; run_checks() measures that (the grounding ratio, required here to be 0.84 or more) besides the structural rules. This module follows the layout of
sen0414_ch20_diagrams_v1_0_0.py (the helper functions below are the same rules, written again because a file of another chapter is not edited); because
chapter 21 has no page data in the new build, nodes_from_ttl() builds the node list from the chapter's RDODI v1_0_2 document and ABox, so the grounding is
measured on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch21_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "AddingALogoToEveryPicture",
        "pattern": "Workflow",
        "title": "Project 16: adding a logo to every picture of a folder",
        "concepts": ["LogoConstants", "LogoFileLoop", "BothSidesTest", "ProportionMath", "CornerPosition", "MaskedPaste", "OutputFolder"],
        "also_from": ["LogoSetup", "LogoResizeLogic", "LogoPlacement", "LogoProject", "ShippedScript"],
        "read_from": "chapter 21, Project 16: Add a Logo: open the logo, loop over the files of the working directory, skip names that are not .png or .jpg and the "
                     "logo, resize only if the width and the height are both larger than 300, paste the logo in the bottom-right corner with itself as the mask and save "
                     "the picture in the folder withLogo",
        "why": "the passage is a numbered sequence of steps with two tests that send the program to the next file, and a loop over the files: a workflow",
        "data": {
            "nodes": [
                {"id": "open", "label": "Open the logo as an Image object"},
                {"id": "loop", "label": "Loop over the names that os.listdir() returns"},
                {"id": "ext", "label": "Does the name end in .png or .jpg and is it not the logo?", "kind": "decision"},
                {"id": "size", "label": "Open the picture and read its width and height"},
                {"id": "big", "label": "Are the width and the height both larger than 300?", "kind": "decision"},
                {"id": "resize", "label": "Calculate the new size and call resize()"},
                {"id": "paste", "label": "Paste the logo in the corner with the logo as the mask"},
                {"id": "save", "label": "Save the picture in the folder withLogo"},
            ],
            "flows": [["start", "open"], ["open", "loop"], ["loop", "ext"], ["ext", "size", "yes"], ["ext", "loop", "no"], ["size", "big"], ["big", "resize", "yes"],
                      ["big", "paste", "no"], ["resize", "paste"], ["paste", "save"], ["save", "loop"], ["loop", "end"]],
        },
    },
    {
        "id": "TilingAPictureWithPaste",
        "pattern": "Workflow",
        "title": "Tiling a face over the whole picture with two loops",
        "concepts": ["CropBox", "PasteInPlace", "TileLoop"],
        "also_from": ["CropAndPaste", "HalfOpenBox", "BoxTuple", "ImageEditing"],
        "read_from": "chapter 21, Pasting Images onto Other Images: crop the face, copy the picture, loop over left in range(0, width, face width) and inside it over top "
                     "in range(0, height, face height), and paste the face at each position",
        "why": "the passage is a sequence of steps with two nested loops that repeat until the grid is full: a workflow",
        "data": {
            "nodes": [
                {"id": "crop", "label": "Crop the face with a box tuple"},
                {"id": "copy", "label": "Copy the picture with copy()"},
                {"id": "left", "label": "Take the next left in range(0, width, face width)"},
                {"id": "top", "label": "Take the next top in range(0, height, face height)"},
                {"id": "paste", "label": "Paste the face at left and top"},
                {"id": "more", "label": "Is there another top or left to paste?", "kind": "decision"},
                {"id": "save", "label": "Save the modified copy"},
            ],
            "flows": [["start", "crop"], ["crop", "copy"], ["copy", "left"], ["left", "top"], ["top", "paste"], ["paste", "more"], ["more", "left", "yes"],
                      ["more", "save", "no"], ["save", "end"]],
        },
    },
    {
        "id": "FromADrawingToAPngFile",
        "pattern": "Workflow",
        "title": "Making a drawing with ImageDraw and saving it as a PNG file",
        "concepts": ["DrawObject", "RectangleEllipse", "DrawingExample", "TrueTypeFont", "TextMeasuring"],
        "also_from": ["ImageDrawShapes", "PointsAndLines", "PolygonDrawing", "TextDrawing", "DefaultFont", "NewImage", "SaveFormats"],
        "read_from": "chapter 21, Drawing on Images: make a white 200 by 200 image with Image.new(), pass it to ImageDraw.Draw(), call the methods for lines, rectangles, "
                     "ellipses and polygons, add text with draw.text() and a font, and save the picture",
        "why": "the passage is a sequence of steps, with a test on the font that sends the program to another font when the file is not found: a workflow",
        "data": {
            "nodes": [
                {"id": "new", "label": "Make an image with Image.new()"},
                {"id": "draw", "label": "Pass the image to ImageDraw.Draw()"},
                {"id": "shapes", "label": "Call line(), rectangle(), ellipse() and polygon()"},
                {"id": "font", "label": "Does ImageFont.truetype() find the font file?", "kind": "decision"},
                {"id": "other", "label": "Load a font by another file name"},
                {"id": "text", "label": "Draw the text with draw.text() and the font"},
                {"id": "save", "label": "Save the picture with save()"},
            ],
            "flows": [["start", "new"], ["new", "draw"], ["draw", "shapes"], ["shapes", "font"], ["font", "text", "yes"], ["font", "other", "no"], ["other", "font"],
                      ["text", "save"], ["save", "end"]],
        },
    },
    {
        "id": "ShowingAGraphInAWindow",
        "pattern": "Interaction",
        "title": "A program showing a graph in a Tk window",
        "concepts": ["ShowLifecycle", "SaveFigure", "PyplotState"],
        "also_from": ["DecorationsAndOutput", "BackendChoice", "FigureModel", "PlotDecorations"],
        "read_from": "chapter 21, Line Graphs and Scatter Plots: save the graph with plt.savefig() before calling plt.show(), the window blocks until the user closes it, "
                     "and closing it resets the graph data",
        "why": "the passage is an exchange between the program and the window in an order that matters - the save comes before the show: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "win", "label": "The Tk window"},
            ],
            "messages": [
                ["prog", "win", "Calls plt.savefig() to write the image"],
                ["prog", "win", "Calls plt.show() to open the window"],
                ["win", "prog", "Blocks until the user closes the window", "reply"],
                ["prog", "win", "Calls plt.show() a second time"],
                ["win", "prog", "Returns at once because no figure is left", "reply"],
                ["prog", "win", "Calls plt.savefig() after the window"],
                ["win", "prog", "Saves a blank image of a new figure", "reply"],
            ],
        },
    },
    {
        "id": "CopyingAnImageToTheClipboard",
        "pattern": "Interaction",
        "title": "A program copying an image to the clipboard and pasting it back",
        "concepts": ["ClipboardCopyPaste", "ClipboardFailures", "ShowViewer"],
        "also_from": ["ClipboardAndViewer", "DrawingAndClipboard"],
        "read_from": "chapter 21, Copying and Pasting Images to the Clipboard: pyperclipimg.copy() puts a Pillow Image on the clipboard of the operating system and "
                     "pyperclipimg.paste() returns the image of the clipboard as an Image object",
        "why": "the passage is an exchange between the program and the clipboard in an order that matters - the copy comes before the paste: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The program"},
                {"id": "clip", "label": "The clipboard"},
            ],
            "messages": [
                ["prog", "clip", "Calls pyperclipimg.copy() with an Image"],
                ["clip", "prog", "Holds the image and copy() returns None", "reply"],
                ["prog", "clip", "Calls pyperclipimg.paste()"],
                ["clip", "prog", "Returns the image as an Image object", "reply"],
                ["prog", "clip", "Calls paste() with text on the clipboard"],
                ["clip", "prog", "Raises UnidentifiedImageError", "reply"],
            ],
        },
    },
    {
        "id": "TheLifeOfAPyplotFigure",
        "pattern": "LifeCycle",
        "title": "A pyplot figure from the first plot to the closed window",
        "concepts": ["PyplotState", "ShowLifecycle", "FigureDefaults"],
        "also_from": ["FigureModel", "BackendChoice", "SaveFigure", "DecorationsAndOutput", "MatplotlibGraphs"],
        "read_from": "chapter 21, Line Graphs and Scatter Plots: plt.plot() draws on the current figure, plt.show() opens a window that blocks, and closing the window "
                     "resets the graph data so a second plt.show() does nothing",
        "why": "the passage follows one figure through the states it can be in and names the call that moves it from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "empty", "label": "A new figure with no lines"},
                {"id": "plotted", "label": "A figure with lines on the current axes"},
                {"id": "shown", "label": "A figure in a window"},
                {"id": "closed", "label": "A closed figure and an empty list of figures"},
            ],
            "initial": "empty",
            "final": ["closed"],
            "transitions": [
                ["empty", "plotted", "plt.plot() draws on the current axes"],
                ["plotted", "plotted", "plt.show() with Agg returns None and keeps the figure"],
                ["plotted", "plotted", "plt.savefig() writes the figure as an image"],
                ["plotted", "shown", "plt.show() with Tk opens a window"],
                ["shown", "closed", "The user closes the window and the figure is gone"],
            ],
        },
    },
    {
        "id": "WhatAProgramCanDoWithAnImage",
        "pattern": "SetOfUses",
        "title": "What a program can do with a Pillow Image object",
        "concepts": ["CropBox", "PasteInPlace", "ResizeInteger", "RotateExpand", "TransposeFlip", "PixelAccess", "SaveFormats", "DrawObject"],
        "also_from": ["ImageEditing", "CropAndPaste", "ResizeAndRotate", "FlipAndPixels", "ImageObject", "ImageDrawShapes", "OpenAndSize"],
        "read_from": "chapter 21, Manipulating Images with Pillow: crop, copy, paste, resize, rotate and transpose an Image, read and set one pixel, draw shapes on it "
                     "and save it to a file",
        "why": "the chapter lists independent things a program can do with the same Image object - crop, paste, resize, rotate, flip, change a pixel, draw, "
               "save - a set of uses of the same object, not a sequence",
        "data": {
            "system": "THE PILLOW IMAGE OBJECT",
            "actors": [{"id": "prog", "label": "A program"}],
            "usecases": [
                {"id": "crop", "label": "Crop a rectangle with a box tuple"},
                {"id": "paste", "label": "Paste one image onto another"},
                {"id": "resize", "label": "Resize to an integer width and height"},
                {"id": "rotate", "label": "Rotate and expand the image"},
                {"id": "flip", "label": "Flip the image with transpose()"},
                {"id": "pixel", "label": "Change one pixel with putpixel()"},
                {"id": "draw", "label": "Draw shapes on the image with ImageDraw"},
                {"id": "save", "label": "Save the image in a format by its extension"},
            ],
            "links": [["prog", "crop"], ["prog", "paste"], ["prog", "resize"], ["prog", "rotate"], ["prog", "flip"], ["prog", "pixel"], ["prog", "draw"], ["prog", "save"]],
        },
    },
    {
        "id": "MakingGraphsAndManipulatingImagesAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Making graphs and manipulating images at a glance: six branches",
        "concepts": ["ImageFundamentals", "ImageEditing", "LogoProject", "DrawingAndClipboard", "MatplotlibGraphs", "BookAndPractice"],
        "also_from": ["ColorRepresentation", "CoordinateSystem", "ImageObject", "CropAndPaste", "ResizeAndRotate", "FlipAndPixels", "LogoSetup", "LogoResizeLogic",
                      "LogoPlacement", "ImageDrawShapes", "TextDrawing", "ClipboardAndViewer", "FigureModel", "LineAndScatter", "BarAndPie", "DecorationsAndOutput",
                      "InstallAndVersions", "BookCorrections", "DeprecatedApis", "PracticePrograms", "RgbaTuple", "ColorNames", "BoxTuple", "HalfOpenBox", "PasteInPlace",
                      "ResizeInteger", "RotateFill", "BothSidesTest", "MaskedPaste", "ShippedScript", "RectangleEllipse", "TextMeasuring", "ClipboardCopyPaste", "ShowLifecycle",
                      "PieChart", "SaveFigure", "GreenTableError", "AppendixPins", "TextsizeGone", "ClipboardFailures", "PixelOrigin", "ImageModes"],
        "read_from": "chapter 21, the opening of each of its main parts: computer image fundamentals, manipulating images with Pillow, Project 16, drawing and the "
                     "clipboard, graphs with Matplotlib, and the book and its practice programs",
        "why": "the chapter classifies one topic, working with images and graphs from a program, by what each part is about and lists examples under each - a topic and "
               "its parts, laid out to remember, with the one idea that holds for every part stated once at the root",
        "data": {
            "root": "A program edits pictures and draws graphs with Pillow and Matplotlib",
            "branches": [
                {"label": "Image fundamentals",
                 "children": ["A colour is four integers from 0 to 255",
                              "The origin is the top left pixel",
                              "A box excludes its right and bottom edge"]},
                {"label": "Image editing",
                 "children": ["paste() changes the image in place",
                              "resize() takes integers only",
                              "rotate() fills the corners by the mode"]},
                {"label": "The logo project",
                 "children": ["Resize only if both sides are larger than 300",
                              "Paste the logo with the logo as the mask",
                              "The page has an en dash and the file has a minus sign"]},
                {"label": "Drawing and the clipboard",
                 "children": ["A rectangle includes its last pixel",
                              "textbbox() replaced textsize()",
                              "copy() needs xclip and a display"]},
                {"label": "Matplotlib graphs",
                 "children": ["Agg returns from show() at once",
                              "pie() returns a PieContainer in 3.11",
                              "savefig() comes before show()"]},
                {"label": "The book and practice",
                 "children": ["Green of Table 21-1 is lime",
                              "matplotlib==3.92 is not a release",
                              "The 2nd edition used textsize"]},
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
    CHX = "http://example.org/sen0414/ch21#"
    d = os.path.join(root, "03-materials", "ch21", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch21_document_v1_0_2.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch21_domain_abox_v1_0_2.ttl"))
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
