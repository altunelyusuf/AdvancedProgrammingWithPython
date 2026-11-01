#!/usr/bin/env python3
"""Exports the chapter 5 deck v3.1.0's slide titles and speaker notes to ../ch05-page/lecture_v2_1_0.json, the Lecture tab of the chapter page (a NEW file;
lecture_v2_0_0.json, made from the deck 3.0.0, stays). Each slide is linked to the corpus concept it teaches (the teach slide shares the concept of the code slide
after it); every concept id is checked against the ids of the page data given. Usage: lecture_export_v3_1_0.py <deck.pptx> <python-version> <page_data.json>  (task TK_MS_Ch05_Build)"""
__version__ = "3.1.0"
import json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CONCEPT = {"boxprint": "RaiseStatement", "exceptionobj": "ExceptionMessage", "unwinding": "TracebackReading", "notes": "ExceptionNotes", "assertfails": "AssertStatement",
           "assertmsg": "AssertVersusRaise", "optimised": "OptimisedMode", "levels": "LoggingLevels", "threshold": "BasicConfig", "format": "LogFormat",
           "tofile": "LogToFile", "disable": "DisablingLogging", "lazy": "LazyFormatting", "factorialbug": "OffByOneRange", "factorialfix": "OffByOneRange",
           "addingbug": "StringConcatenation", "cointossbug": "TypeMismatchComparison", "cointossfix": "TypeMismatchComparison", "stepper": "Debugger",
           "breakpointfn": "BreakpointFunction"}
STORY = {"Story: the bug you can visit in a museum": "BugModel", "Story: the most effective debugging tool": "LoggingVersusPrint",
         "Story: a logging system with a birth certificate": "Logging"}
OTHER = {"The controls of the debugger": "StopControl", "Choose the instrument by the question": "InstrumentChoice", "Current Python adds more": "ModernPractice"}
ids = {n["id"] for n in json.load(open(sys.argv[3]))["nodes"]}
bad = [v for v in list(CONCEPT.values()) + list(STORY.values()) + list(OTHER.values()) if v not in ids]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
man = json.load(open(os.path.join(HERE, "..", "..", "03-materials", "ch05", "page", "chapter_code_ch05_v1_1_0.json"), encoding="utf-8"))
code_slide = {e["slide"]: e["id"] for e in man["examples"]}
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.text_frame.text.strip() != ">>>"]
    title = texts[0]
    cid = ""
    if i in code_slide:
        cid = CONCEPT[code_slide[i]]
    elif i + 1 in code_slide:                 # the teach slide before a code slide
        cid = CONCEPT[code_slide[i + 1]]
    elif title in STORY:
        cid = STORY[title]
    elif title in OTHER:
        cid = OTHER[title]
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": cid, "visual": ""})
json.dump({"_version": "2.1.0", "_deck": "3.1.0", "_python": sys.argv[2],
           "_note": "2.1.0 (over 2.0.0, which stays as it is): the slide titles and the speaker notes of the deck 3.1.0 (teach slides included), each slide tied to a concept by its example or its title; %d slides tied." % sum(1 for s in out if s["concept"]),
           "slides": out},
          open(os.path.join(HERE, "..", "ch05-page", "lecture_v2_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v2_1_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
