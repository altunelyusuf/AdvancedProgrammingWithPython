#!/usr/bin/env python3
"""Exports the finished deck's slide titles and speaker notes to lecture_out_v1_0_0.json beside this file, in the shape of
chapter 13's lecture_v1_0_0.json (the Lecture tab of the chapter page). Each slide is linked to the concept it teaches; every
concept id is checked against the chapter's topics, read from the v1_0_1 RDODI document and ABox. The file is left here and not
written into ch15-page, whose files belong to the page's own build.
Usage: lecture_export_v1_0_0.py <deck.pptx> <python-version>   (needs python-pptx and rdflib)"""
__version__ = "1.0.0"
import importlib.util, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("diagrams15", os.path.join(HERE, "..", "sen0414_ch15_diagrams_v1_0_0.py"))
DG = importlib.util.module_from_spec(spec); spec.loader.exec_module(DG)
IDS = {n["id"] for n in DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))}
CONCEPT = {4: "LibraryContext", 5: "NewSpreadsheet", 6: "CloudProject", 7: "TokenLifetime", 8: "TokenPickle", 9: "SpreadsheetAttributes",
           10: "AddressConversion", 11: "IdFromUrl", 12: "RowsColumns", 13: "SheetIndex", 14: "ValuesAsText", 15: "RequestCost",
           16: "RetryOnQuota", 17: "QuotaRules", 18: "BlockchainLedger", 19: "AuditProgram", 20: "AuditProgram",
           21: "TransactionProgram", 22: "AppendRace", 23: "PracticePrograms"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 15: Google Sheets" if i == 1 else next(t for t in texts if t != ">>>")
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "1.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "lecture_out_v1_0_0.json"), "w"), indent=1)
print("lecture_out_v1_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
