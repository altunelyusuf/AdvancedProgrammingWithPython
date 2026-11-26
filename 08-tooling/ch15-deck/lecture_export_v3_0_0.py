#!/usr/bin/env python3
"""Exports the chapter 15 deck 3.0.0 (53 slides) slide titles and speaker notes to ../ch15-page/lecture_v3_0_0.json, the Lecture tab of the
chapter 15 page v9.105.0 (new file over lecture_v1_0_0.json, which describes a 23-slide deck that no longer exists). Each slide is linked to the concept it teaches;
every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Usage: lecture_export_v3_0_0.py <deck.pptx> <python-version>"""
__version__ = "3.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch15-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {4: "GoogleAccess", 5: "CloudProject", 6: "SignInFlow", 7: "ScopesChosen", 8: "TokenFiles", 9: "SignInFlow", 10: "LocalServerFlow", 11: "ClientLibraries",
           12: "SignInFlow", 13: "TokenPickle", 14: "TokenLifetime", 15: "SpreadsheetObjects", 16: "SpreadsheetObjects", 17: "NewSpreadsheet", 18: "OpeningSpreadsheets",
           19: "SpreadsheetAttributes", 20: "LibraryContext", 21: "FileTransfer", 22: "DownloadFormats", 23: "TrashAndDelete", 24: "SheetObjects", 25: "CellAccess",
           26: "CellByAddress", 27: "AddressConversion", 28: "RowsColumns", 29: "GetRowColumn", 30: "BatchedUpdate", 31: "LibraryStatus", 32: "SheetLifecycle",
           33: "CreateSheet", 34: "CopySheet", 35: "SheetQuirks", 36: "RequestsAndQuotas", 37: "FormsResponses", 38: "FormsResponses", 39: "FormsResponses",
           40: "RetryOnQuota", 41: "LedgerProjects", 42: "BlockchainLedger", 43: "AuditProgram", 44: "BlankRowError", 45: "TransactionProgram", 46: "AppendRace",
           47: "BlockchainLedger", 48: "BeanCountCheck", 49: "RequestCost", 50: "ReleaseState", 52: "PracticePrograms"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 15: Google Sheets" if i == 1 else next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "3.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch15-page", "lecture_v3_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v3_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
