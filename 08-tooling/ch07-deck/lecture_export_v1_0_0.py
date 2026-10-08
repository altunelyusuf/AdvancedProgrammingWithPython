#!/usr/bin/env python3
"""Exports the finished deck's slide titles and speaker notes to ../ch07-page/lecture_v1_0_0.json, the Lecture tab of the
chapter page (each slide's notes are reader's prose, so they are the text as they stand). Each slide is linked to the corpus
concept it teaches; every concept id is checked against the chapter corpus.
Usage: lecture_export_v1_0_0.py <deck.pptx> <python-version>"""
__version__ = "1.0.0"
import importlib.util, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c7", os.path.join(HERE, "..", "sen0414_ch07_corpus_v1_0_0.py"))
C = importlib.util.module_from_spec(spec); spec.loader.exec_module(C)
IDS = {n[0] for n in C.NODES}
CONCEPT = {3: "DictionaryModel", 4: "DictionaryType", 5: "ListContrast", 6: "InsertionOrder", 7: "HashableKeys", 8: "GetMethod",
           9: "UpdateAndMerge", 10: "BirthdayLookup", 11: "Views", 12: "CharacterCount", 13: "CounterClass",
           14: "GroupingIntoLists", 15: "DataStructureModel", 16: "ChessboardModel", 17: "ChessboardPrinter",
           18: "ChessboardCommands", 19: "TotalBrought", 20: "CopyingDictionaries", 21: "JsonText", 22: "JsonText",
           23: "FantasyInventory"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = texts[0] if i > 1 else "Chapter 7: Dictionaries"
    if i > 1:
        title = next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "1.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch07-page", "lecture_v1_0_0.json"), "w"), indent=1)
print("lecture_v1_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
