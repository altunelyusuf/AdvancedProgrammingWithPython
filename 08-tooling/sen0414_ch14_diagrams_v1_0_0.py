#!/usr/bin/env python3
"""SEN0414, chapter 14 (Excel Spreadsheets, Automate the Boring Stuff with Python, 3rd edition) - the narrative diagrams of the
chapter (version 1.0.0).

A paragraph gets the diagram its narrative calls for - a workflow an activity diagram, the possible usages a use-case
diagram, the life of a thing a state diagram, an exchange between parties a sequence diagram, a topic and its parts a mind
map - and the mapping from narrative pattern to diagram type lives in the CME ontology (the narrative-to-diagram module of
cme_standards_adoption_v1_3_0.ttl) so that it is reused by every course. Each entry names the concepts whose paragraphs it
accompanies, the narrative pattern it was recognised as, the passage it was read from (also_from names further concepts
whose explanations the content draws on), one sentence saying why the pattern fits, and the diagram's content in the
element names the renderer of that type expects. Every element label is made of words that occur in the first paragraph
and the definition of the accompanying concepts or their section, which is the text the page shows; run_checks() measures
that (the grounding ratio, required here to be 0.84 or more, where the shared rule of the earlier chapters asks 0.8)
besides the structural rules. This module follows the layout of sen0414_ch13_diagrams_v1_0_0.py (the helper functions
below are the same rules, written again because a file of another chapter is not edited); because chapter 14 has no page
data yet, nodes_from_ttl() builds the node list from the chapter's RDODI document and ABox, so the grounding can be
measured now, on the section's first paragraph, which is what the page uses as the body.

Usage: python3 sen0414_ch14_diagrams_v1_0_0.py   (measures the grounding on the newest RDODI files of the chapter)
       or import DIAGRAMS; run_checks(nodes, mapping) with the chapter's node list and the CME mapping.
"""
__version__ = "1.0.0"
MIN_GROUNDING = 0.84

DIAGRAMS = [
    {
        "id": "FromFileToCellValue",
        "pattern": "Workflow",
        "title": "From an .xlsx file to the value of a cell",
        "concepts": ["LoadWorkbook", "SheetByName", "ActiveSheet", "CellByName", "CellByNumbers", "DatesAsDatetime"],
        "also_from": ["WorkbookObjects", "CellAccess", "SheetNames", "CellValues", "Workbooks", "Cells"],
        "read_from": "chapter 14, Reading Excel Files: import openpyxl, call load_workbook() to get a Workbook object, use "
                     "the active or sheetnames attribute, get a Worksheet object, use indexing or cell() with row and column "
                     "keyword arguments, get a Cell object and read its value attribute",
        "why": "the passage is the chapter's own review in seven steps, in order, with one choice on the way, how the cell "
               "is named, by its letter and number or by two integers: a workflow",
        "data": {
            "nodes": [
                {"id": "load", "label": "openpyxl.load_workbook() returns a Workbook object"},
                {"id": "sheet", "label": "Get a Worksheet by its name or from the active attribute"},
                {"id": "how", "label": "Is the cell named by letter and row number?", "kind": "decision"},
                {"id": "name", "label": "sheet['A1'] gets the Cell object by its name"},
                {"id": "nums", "label": "sheet.cell(row=1, column=2) gets it by two integers"},
                {"id": "value", "label": "Read the value attribute of the Cell"},
            ],
            "flows": [["start", "load"], ["load", "sheet"], ["sheet", "how"], ["how", "name", "yes"], ["how", "nums", "no, in a loop"],
                      ["name", "value"], ["nums", "value"], ["value", "end"]],
        },
    },
    {
        "id": "ProjectNineTally",
        "pattern": "Workflow",
        "title": "Project 9: the census tally, row by row",
        "concepts": ["NestedTally", "SetdefaultCall", "ResultFile", "ImportResult"],
        "also_from": ["CensusProject", "MaxRowColumn", "PhantomRows", "Projects"],
        "read_from": "chapter 14, Project 9: open censuspopdata.xlsx, loop over the rows from 2 to max_row, make sure the "
                     "state and the county exist with setdefault(), add one to the tracts and the tract's population to pop, "
                     "then write the dictionary with pprint.pformat() into census2010.py and import it",
        "why": "the passage describes what the program does, step by step and in a loop, with one choice on the way, "
               "whether the state and the county exist in the dictionary yet: a workflow",
        "data": {
            "nodes": [
                {"id": "open", "label": "Open the workbook and get the census sheet"},
                {"id": "row", "label": "Read the state, county and population of the next row"},
                {"id": "has", "label": "Do the state and the county exist in county_data yet?", "kind": "decision"},
                {"id": "set", "label": "setdefault() adds the state, the county, tracts and pop"},
                {"id": "add", "label": "Add one tract and the population to the county"},
                {"id": "more", "label": "Is a row left up to max_row?", "kind": "decision"},
                {"id": "write", "label": "pprint.pformat() writes the dictionary into census2010.py"},
                {"id": "imp", "label": "import census2010 reads the result as a module"},
            ],
            "flows": [["start", "open"], ["open", "row"], ["row", "has"], ["has", "set", "no"], ["has", "add", "yes"], ["set", "add"],
                      ["add", "more"], ["more", "row", "yes"], ["more", "write", "no"], ["write", "imp"], ["imp", "end"]],
        },
    },
    {
        "id": "ProjectTenUpdate",
        "pattern": "Workflow",
        "title": "Project 10: correcting prices without touching the original",
        "concepts": ["PriceDictionary", "UpdateLoop", "CachedValueLoss"],
        "also_from": ["ProduceProject", "SaveWorkbook", "DataOnly"],
        "read_from": "chapter 14, Project 10: store the corrected prices in the PRICE_UPDATES dictionary, loop through the "
                     "rows starting at row 2, check whether the produce name is a key, write the new price in column 2, and "
                     "save to updatedProduceSales3.xlsx so that the original spreadsheet is not overwritten",
        "why": "the passage lists what the program does in order, in a loop with one choice, whether the produce is in the "
               "dictionary, and ends by saving under a new name: a workflow",
        "data": {
            "nodes": [
                {"id": "dict", "label": "PRICE_UPDATES holds the corrected prices"},
                {"id": "open", "label": "Load produceSales3.xlsx and get its sheet"},
                {"id": "name", "label": "Read the produce name of the next row from row 2"},
                {"id": "key", "label": "Is the produce name a key of PRICE_UPDATES?", "kind": "decision"},
                {"id": "write", "label": "Write the new price in column 2"},
                {"id": "more", "label": "Is a row left up to max_row + 1?", "kind": "decision"},
                {"id": "save", "label": "Save the workbook as updatedProduceSales3.xlsx"},
                {"id": "lost", "label": "The saved formulas hold no stored results"},
            ],
            "flows": [["start", "dict"], ["dict", "open"], ["open", "name"], ["name", "key"], ["key", "write", "yes"], ["key", "more", "no"],
                      ["write", "more"], ["more", "name", "yes"], ["more", "save", "no"], ["save", "lost"], ["lost", "end"]],
        },
    },
    {
        "id": "AFormulaResult",
        "pattern": "Interaction",
        "title": "A formula written by openpyxl and calculated by a spreadsheet program",
        "concepts": ["FormulaString", "ReadFormulaBack", "DataOnly", "RecalcByOffice"],
        "also_from": ["FormulaStorage", "CachedResults", "CachedValueLoss", "Formulas"],
        "read_from": "chapter 14, Formulas: the program stores =SUM(A1:A2) in A3, openpyxl does not calculate it, Excel "
                     "populates the result when the file is opened and saved, and data_only=True then reads the 500 that "
                     "was stored",
        "why": "the passage is an exchange between the program and a spreadsheet application in an order that matters - "
               "the formula is written, calculated by the application, and only then read back as a value: an interaction",
        "data": {
            "participants": [
                {"id": "prog", "label": "The Python program"},
                {"id": "app", "label": "Excel or LibreOffice"},
            ],
            "messages": [
                ["prog", "prog", "Assigns '=SUM(A1:A2)' to A3 and saves the file"],
                ["prog", "app", "The file is opened and saved by the application"],
                ["app", "app", "Calculates the formula and stores the result 500"],
                ["app", "prog", "The saved file holds the formula and its result", "reply"],
                ["prog", "prog", "load_workbook() without data_only reads the formula"],
                ["prog", "prog", "data_only=True reads the stored result, 500"],
            ],
        },
    },
    {
        "id": "ABarChartInFiveSteps",
        "pattern": "Workflow",
        "title": "Making a bar chart from the cells of a sheet",
        "concepts": ["ReferenceObject", "SeriesObject", "ChartObject", "ChartXml"],
        "also_from": ["ChartBuilding", "Charts", "FourKinds", "ChartFiles"],
        "read_from": "chapter 14, Charts: create a Reference object from a rectangular selection of cells, create a Series "
                     "object by passing in the Reference, create a Chart object, append the Series to the Chart and add the "
                     "Chart to the Worksheet at a cell",
        "why": "the passage is the chapter's own list of five steps, each depending on the one before it, with no choice "
               "on the way: a workflow",
        "data": {
            "nodes": [
                {"id": "ref", "label": "Reference(sheet, min_col, min_row, max_col, max_row)"},
                {"id": "series", "label": "Series(ref_obj, title='First series') from the Reference"},
                {"id": "chart", "label": "BarChart() creates the Chart object; set its title"},
                {"id": "append", "label": "chart_obj.append(series_obj) adds the Series"},
                {"id": "add", "label": "sheet.add_chart(chart_obj, 'C5') adds the Chart to the sheet"},
                {"id": "save", "label": "save() writes the chart into xl/charts/chart1.xml"},
            ],
            "flows": [["start", "ref"], ["ref", "series"], ["series", "chart"], ["chart", "append"], ["append", "add"],
                      ["add", "save"], ["save", "end"]],
        },
    },
    {
        "id": "AMergedRange",
        "pattern": "LifeCycle",
        "title": "A rectangle of cells under merge_cells and unmerge_cells",
        "concepts": ["MergeCells", "MergedValue", "UnmergeCells"],
        "also_from": ["MergedCells", "Formatting", "RowsColumnsSize"],
        "read_from": "chapter 14, merging and unmerging cells: merge_cells('A1:D3') merges 12 cells into a single cell whose "
                     "value is that of the top-left cell, and unmerge_cells() takes the merged cells back to individual cells",
        "why": "the passage follows one rectangle of cells through the states it can be in and names the call that moves it "
               "from each state to the next: a life cycle",
        "data": {
            "states": [
                {"id": "separate", "label": "Individual cells"},
                {"id": "merged", "label": "One merged cell, with the value of the top-left cell"},
            ],
            "initial": "separate",
            "final": [],
            "transitions": [
                ["separate", "merged", "merge_cells('A1:D3') discards the other values"],
                ["merged", "separate", "unmerge_cells('A1:D3') gives individual cells"],
                ["merged", "merged", "Assigning to a MergedCell value raises an error"],
            ],
        },
    },
    {
        "id": "WhatOpenpyxlCanDo",
        "pattern": "SetOfUses",
        "title": "What a program can do with a workbook through openpyxl",
        "concepts": ["LoadWorkbook", "CreateSheet", "FormulaString", "FontObject", "FreezeSetting", "ChartObject"],
        "also_from": ["Workbooks", "Cells", "Formulas", "Formatting", "Charts", "WorkbookObjects", "SheetManagement"],
        "read_from": "chapter 14: the module reads and modifies Excel files, creates and removes sheets, writes values and "
                     "formulas, sets fonts, row heights and column widths, merges cells, freezes panes and draws charts",
        "why": "the chapter lists independent things a program can do with the same workbook - read, write, calculate, "
               "format, freeze, chart - a set of uses of the same module, not a sequence",
        "data": {
            "system": "A WORKBOOK FILE IN OPENPYXL",
            "actors": [{"id": "prog", "label": "A Python program"}],
            "usecases": [
                {"id": "read", "label": "Open a workbook with load_workbook() and read its cells"},
                {"id": "sheets", "label": "Create and remove sheets with create_sheet()"},
                {"id": "write", "label": "Write values and formulas into cells"},
                {"id": "font", "label": "Set the font style of cells with Font()"},
                {"id": "freeze", "label": "Merge cells and freeze panes"},
                {"id": "chart", "label": "Add a chart with add_chart()"},
            ],
            "links": [["prog", "read"], ["prog", "sheets"], ["prog", "write"], ["prog", "font"], ["prog", "freeze"], ["prog", "chart"]],
        },
    },
    {
        "id": "ExcelSpreadsheetsAtAGlance",
        "pattern": "TopicAndParts",
        "title": "Excel spreadsheets at a glance: six branches",
        "concepts": ["Workbooks", "Cells", "Projects", "Formulas", "Formatting", "Charts"],
        "also_from": ["WorkbookObjects", "SheetManagement", "FileHandling", "LibraryEcosystem", "CellAccess", "RangeAccess",
                      "CensusProject", "ProduceProject", "PracticePrograms", "FormulaStorage", "CachedResults", "FontStyle",
                      "RowsColumnsSize", "MergedCells", "FreezePanes", "ChartBuilding", "ChartKinds", "ChartFiles"],
        "read_from": "chapter 14, the opening of each of its main branches: workbooks and sheets, cells and ranges, the two "
                     "projects and the practice programs, formulas, formatting of fonts, sizes, merges and frozen panes, "
                     "and charts",
        "why": "the chapter classifies one topic, working with spreadsheet files, by what each branch is about and lists "
               "examples under each - a topic and its parts, laid out to remember, with the one idea that holds for every "
               "part stated once at the root",
        "data": {
            "root": "Excel spreadsheets: a program reads and writes workbooks",
            "branches": [
                {"label": "Workbooks and sheets",
                 "children": ["load_workbook() returns a Workbook object",
                              "The active sheet is the one on top",
                              "create_sheet() and del add and remove sheets"]},
                {"label": "Cells and ranges",
                 "children": ["A cell is got by its name or by row and column numbers",
                              "max_row and max_column give the size of the sheet",
                              "A slice of two cell names gives a tuple of rows"]},
                {"label": "Projects",
                 "children": ["Project 9 tallies tracts and population by county",
                              "Project 10 corrects prices in the produce sheet",
                              "The practice programs make a table and insert rows"]},
                {"label": "Formulas",
                 "children": ["A formula is text that begins with an equal sign",
                              "openpyxl does not calculate a formula",
                              "data_only=True reads the stored result"]},
                {"label": "Formatting",
                 "children": ["Font() sets the name, size, bold and italic",
                              "Row heights and column widths are set through dimensions",
                              "merge_cells() and freeze_panes change how cells show"]},
                {"label": "Charts",
                 "children": ["A Reference names a rectangle of cells",
                              "A Series is appended to a chart object",
                              "add_chart() anchors the chart to a cell"]},
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
    CHX = "http://example.org/sen0414/ch14#"
    d = os.path.join(root, "03-materials", "ch14", "rdodi")
    g = Graph(); g.parse(os.path.join(d, "sen0414_ch14_document_v1_0_1.ttl"))
    a = Graph(); a.parse(os.path.join(d, "sen0414_ch14_domain_abox_v1_0_1.ttl"))
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
