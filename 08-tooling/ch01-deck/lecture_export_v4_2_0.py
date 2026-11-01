#!/usr/bin/env python3
"""Exports the finished chapter 1 deck's (4.2.0) slide titles and speaker notes to ../ch01-page/lecture_v1_2_0.json, the Lecture tab of the
chapter page (a NEW file beside lecture_v1_1_0.json, which stays). Each slide is linked to the concept it teaches; every concept id is checked
against the nodes of the chapter's newest page_data json. The slide numbers are those of the 58-slide deck 4.2.0 (a teach slide, then the code slide of each example).
Usage: lecture_export_v4_2_0.py <deck.pptx> <python-version>"""
__version__ = "4.2.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch01-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {5: "DataType", 6: "InteractiveShell", 7: "InteractiveShell", 8: "PythonInterpreter", 9: "DataType", 10: "DataType", 11: "Integer", 12: "Integer",
           13: "FloatingPoint", 14: "FloatingPoint", 15: "String", 16: "String", 18: "Operator", 19: "ArithmeticOperation", 20: "ArithmeticOperation",
           21: "Precedence", 22: "Precedence", 23: "IntegerDivision", 24: "IntegerDivision", 25: "TextOperation", 26: "Concatenation", 27: "Concatenation",
           28: "Replication", 29: "Replication", 31: "Variable", 32: "Variable", 33: "Variable", 34: "Output", 35: "Output", 36: "BuiltInFunction",
           37: "TypeConversion", 38: "TypeConversion", 39: "FunctionCall", 40: "FunctionCall", 41: "Input", 42: "Input", 43: "Package", 44: "Package",
           46: "Value", 47: "Output", 48: "Output", 49: "Output", 50: "FString", 51: "FString", 52: "Integer", 53: "Integer", 54: "Integer", 55: "ModernPractice"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": "1.2.0", "_deck": "4.2.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch01-page", "lecture_v1_2_0.json"), "w"), indent=1)
print("lecture_v1_2_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
