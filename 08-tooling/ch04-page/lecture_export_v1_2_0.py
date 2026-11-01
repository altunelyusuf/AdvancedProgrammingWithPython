#!/usr/bin/env python3
"""Exports the chapter 4 deck 3.2.0's slide titles and speaker notes to ch04-page/lecture_v1_2_0.json, the Lecture tab of the chapter page (new file over 1.1.0).
A teaching slide and its code slide are tied to the concept the example teaches; each concept id is checked against the nodes of the page data given.
Usage: lecture_export_v1_2_0.py <deck.pptx> <page_data.json> <python-version>"""
__version__ = "1.2.0"
import json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(os.path.dirname(HERE))
CON = {"hello": "DefStatement", "dedup": "Deduplication", "params": "PositionalArgument", "returns": "ReturnStatement", "none": "ImplicitNone", "named": "NamedParameter",
       "defaults": "KeywordOnlyParameter", "mutable": "DefaultArgument", "stack": "CallStack", "frame": "FrameObject", "localgone": "LocalScope", "walls": "LocalIsolation",
       "samename": "SameNameVariables", "globalstmt": "GlobalStatement", "nonlocal": "NonlocalStatement", "identify": "ScopeIdentification", "unbound": "UnboundLocalError",
       "tryexcept": "TryExcept", "inloop": "TryExcept", "aroundall": "TryExcept", "several": "MultipleExceptTypes", "traceback": "Traceback", "zigzag": "ZigzagProgram",
       "spike": "SpikeProgram", "collatz": "CollatzSequence"}
man = json.load(open(os.path.join(R, "03-materials/ch04/page/chapter_code_ch04_v1_2_0.json"), encoding="utf-8"))
CONCEPT = {}
for e in man["examples"]:
    CONCEPT[e["slide"]] = CON[e["id"]]; CONCEPT[e["slide"] - 1] = CON[e["id"]]       # the code slide and the teach slide before it
IDS = {n["id"] for n in json.load(open(sys.argv[2], encoding="utf-8"))["nodes"]}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.text_frame.text.strip() != ">>>"]
    title = texts[0].split("\n")[0]
    c = CONCEPT.get(i, "")
    if title.startswith("Story: except"): c = "MultipleExceptTypes"
    if title.startswith("Story: an unsolved"): c = "CollatzSequence"
    if title.startswith("Current Python"): c = "ModernPractice"
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": c, "visual": ""})
json.dump({"_version": "1.2.0", "_deck": os.path.basename(sys.argv[1]), "_python": sys.argv[3], "slides": out},
          open(os.path.join(HERE, "lecture_v1_2_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v1_2_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "tied to a concept")
