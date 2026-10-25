#!/usr/bin/env python3
"""Exports the finished chapter 1 deck's (4.1.0) slide titles and speaker notes to ../ch01-page/lecture_v1_1_0.json, the Lecture tab of the
chapter page (new file; chapter 1 had none). Each slide is linked to the concept it teaches; every concept id is checked against the
nodes of the chapter's newest page_data json.
Usage: lecture_export_v4_1_0.py <deck.pptx> <python-version>"""
__version__ = "4.1.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch01-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {4: "Value", 5: "DataType", 6: "InteractiveShell", 7: "PythonInterpreter", 8: "DataType", 9: "Integer", 10: "FloatingPoint",
           11: "String", 12: "Operation", 13: "Operator", 14: "Operator", 15: "Precedence", 16: "IntegerDivision", 17: "TextOperation",
           18: "Concatenation", 19: "Replication", 20: "BindingOperation", 21: "Variable", 22: "Assignment", 23: "Output",
           24: "BuiltInFunction", 25: "TypeConversion", 26: "FunctionCall", 27: "Input", 28: "Package", 31: "Output",
           32: "FunctionCall", 33: "FString", 34: "Integer", 35: "Integer", 36: "ModernPractice"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": "1.1.0", "_deck": "4.1.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch01-page", "lecture_v1_1_0.json"), "w"), indent=1)
print("lecture_v1_1_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
