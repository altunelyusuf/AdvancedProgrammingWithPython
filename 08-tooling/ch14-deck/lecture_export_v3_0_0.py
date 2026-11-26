#!/usr/bin/env python3
"""Exports the chapter 14 deck 3.0.0 (51 slides) slide titles and speaker notes to ../ch14-page/lecture_v3_0_0.json, the Lecture tab of the
chapter 14 page v9.103.0 (new file over lecture_v1_0_0.json, which describes an earlier deck of 26 slides). Each slide is linked to the concept it teaches;
every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Usage: lecture_export_v3_0_0.py <deck.pptx> <python-version>"""
__version__ = "3.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch14-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {4: "Workbooks", 5: "WorkbookObjects", 6: "FileFormats", 7: "FileFormats", 8: "SheetManagement", 9: "OpenpyxlRelease", 10: "Cells", 11: "CellAccess",
           12: "CellByName", 13: "ColumnLetters", 14: "SliceRange", 15: "IterRows", 16: "DataTypes", 17: "DatesAsDatetime", 18: "CellCreation", 19: "ReadOnlyMode",
           20: "Projects", 21: "Projects", 22: "CensusProject", 23: "NestedTally", 24: "ResultFile", 25: "ProduceProject", 26: "Formulas", 27: "FormulaStorage",
           28: "SaveWorkbook", 29: "FormulaString", 30: "FileFormats", 31: "RoundingDiffers", 32: "Formulas", 33: "InsertRowsLimits", 34: "Formatting",
           35: "FontStyle", 36: "MergedCells", 37: "MultiplicationTable", 38: "FontDefaults", 39: "RowsColumnsSize", 40: "MergeCells", 41: "FreezePanes",
           42: "Charts", 43: "ChartBuilding", 44: "ChartBuilding", 45: "ReferenceObject", 46: "ChartFiles", 47: "LibraryEcosystem", 48: "OpenpyxlRelease",
           50: "PracticePrograms"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 14: Excel Spreadsheets" if i == 1 else next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "3.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch14-page", "lecture_v3_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v3_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
