#!/usr/bin/env python3
"""Exports the finished deck's slide titles and speaker notes to lecture_out_v1_0_0.json beside this file, in the shape of
chapter 12's lecture_v1_0_0.json (the Lecture tab of the chapter page). Each slide is linked to the concept it teaches; every
concept id is checked against the chapter's topics, read from the v1_0_2 RDODI document and ABox. The file is left here and not
written into ch13-page, whose files belong to the page's own build.
Usage: lecture_export_v1_0_0.py <deck.pptx> <python-version>   (needs python-pptx and rdflib)"""
__version__ = "1.0.0"
import importlib.util, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("diagrams13", os.path.join(HERE, "..", "sen0414_ch13_diagrams_v1_0_0.py"))
DG = importlib.util.module_from_spec(spec); spec.loader.exec_module(DG)
IDS = {n["id"] for n in DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))}
CONCEPT = {4: "UrlAnatomy", 5: "RobotsTxt", 6: "PoliteDelay", 7: "ShowmapProgram", 8: "RaiseForStatus", 9: "RequestTimeout",
           10: "GetRequest", 11: "AccessKey", 12: "JsonDecoding", 13: "SelectMethod", 14: "RegexPitfall", 15: "ChallengePage",
           16: "ComicCrawler", 17: "PoliteCrawler", 18: "DynamicPages", 19: "WebDriverStart", 20: "ClickAndSubmit",
           21: "CheckBoxes", 22: "AutoWaiting", 23: "ToolChoice"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 13: Web Scraping" if i == 1 else next(t for t in texts if t != ">>>")
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "1.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "lecture_out_v1_0_0.json"), "w"), indent=1)
print("lecture_out_v1_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
