#!/usr/bin/env python3
"""Exports the chapter 17 deck 4.0.0 (59 slides, plain wording instead of everyday analogies; Lineage10) slide titles and speaker notes to ../ch17-page/lecture_v2_0_0.json, the Lecture tab of the
chapter 17 page (new file over lecture_v1_0_0.json, which holds the notes of deck 2.1.0). Each slide is linked to the concept it teaches (the code slides and the story and practice slides that
name one); every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Usage: lecture_export_v2_0_0.py <deck.pptx> <python-version>"""
__version__ = "2.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch17-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {5: "PdfReaderPages", 7: "HeaderAndTrailer", 8: "PdfReaderPages", 9: "TextOrderIsStreamOrder", 10: "ContentStreamText",
           11: "TextPostProcessing", 12: "ScannedPageNoText", 16: "PdfWriterStartsEmpty", 17: "AppendRangeTuple", 18: "MergePositionalTupleTrap",
           19: "RotationAccumulates", 21: "WatermarkUnderlay", 22: "ReaderRefusesBeforeDecrypt", 24: "DecryptReturnValues", 25: "EncryptRc4Default",
           27: "CaseInsensitiveSort", 28: "CombineAllPdfs", 32: "DocxIsZipOfXml", 33: "ParagraphsOfBody", 34: "TablesAndHeadersApart",
           36: "StyleKindsOfTemplate", 37: "UnknownStyleKeyError", 39: "TriStateBold", 43: "AddParagraphReturnsParagraph", 44: "AddHeadingLevels",
           45: "PageBreakRun", 47: "PictureSizeFromWidth", 48: "PackageNameTrap", 51: "WalkFindsAllPdfs", 53: "InvitationPageBreaks",
           54: "DictionaryAttackBothCases", 56: "RemovedNames", 58: "PracticeAnswersChecked"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 17: PDF and Word Documents" if i == 1 else next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "4.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch17-page", "lecture_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v2_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
