#!/usr/bin/env python3
"""Exports the finished deck's slide titles and speaker notes to lecture_out_v1_0_0.json beside this file, in the shape of
chapter 13's lecture_v1_0_0.json (the Lecture tab of the chapter page). Each slide is linked to the concept it teaches; every
concept id is checked against the chapter's topics, read from the v1_0_2 RDODI document and ABox. The file is written here and a copy
as a new versioned file into ch17-page (lecture_v1_0_0.json), which is not an existing file.
Usage: lecture_export_v1_0_0.py <deck.pptx> <python-version>   (needs python-pptx and rdflib)"""
__version__ = "1.0.0"
import importlib.util, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("diagrams17", os.path.join(HERE, "..", "sen0414_ch17_diagrams_v1_0_0.py"))
DG = importlib.util.module_from_spec(spec); spec.loader.exec_module(DG)
IDS = {n["id"] for n in DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))}
CONCEPT = {4: "RemovedNames", 5: "ContentStreamText", 6: "HeaderAndTrailer", 7: "JoinedPagesNoSeparator", 8: "TextPostProcessing",
           9: "ImageNameAndData", 10: "MergePositionalTupleTrap", 11: "RotationAccumulates", 12: "EncryptRc4Default",
           13: "DecryptReturnValues", 14: "CombineAllPdfs", 15: "WalkFindsAllPdfs", 16: "DictionaryAttackBothCases",
           17: "DocxIsZipOfXml", 18: "HyperlinkTextAndRuns", 19: "RunsSplitAtFormatting", 20: "UnknownStyleKeyError",
           21: "RunVersusFontAttributes", 22: "AddHeadingLevels", 23: "InvitationPageBreaks"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 17: PDF and Word Documents" if i == 1 else next(t for t in texts if t != ">>>")
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i, ""), "visual": ""})
for dst in (os.path.join(HERE, "lecture_out_v1_0_0.json"), os.path.join(HERE, "..", "ch17-page", "lecture_v1_0_0.json")):
    json.dump({"_version": __version__, "_deck": "1.0.0", "_python": sys.argv[2], "slides": out}, open(dst, "w"), indent=1)
print("lecture_out_v1_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
