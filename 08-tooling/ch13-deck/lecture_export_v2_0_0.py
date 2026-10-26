#!/usr/bin/env python3
"""Exports the chapter 13 deck 2.0.0 (51 slides) slide titles and speaker notes to ../ch13-page/lecture_v2_0_0.json, the Lecture tab of the
chapter 13 page v9.95.0 (new file over lecture_v1_0_0.json, which describes the earlier deck). Each slide is linked to the concept it teaches;
every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Usage: lecture_export_v2_0_0.py <deck.pptx> <python-version>"""
__version__ = "2.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch13-page", "page_data_v*.json")),
             key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]} if _pf else set()
CONCEPT = {4: "Protocol", 5: "AddressForms", 6: "UrlAnatomy", 7: "PercentEncoding", 8: "StatusCode", 9: "UserAgent", 10: "RobotsTxt",
           11: "RobotsTxt", 12: "PoliteDelay", 13: "CrawlerManners", 14: "Fetching", 15: "BrowserOpening", 16: "PageDownload",
           17: "WebbrowserOpen", 18: "ShowmapProgram", 19: "ResponseBody", 20: "GetRequest", 21: "RaiseForStatus", 22: "ChunkedDownload",
           23: "Services", 24: "ApiCalls", 25: "JsonDecoding", 26: "UnitConversion", 27: "ServiceEndpoint", 28: "Parsing",
           29: "MarkupBasics", 30: "PageInspection", 31: "HtmlElement", 32: "SelectMethod", 33: "SoupObjects", 34: "RegexPitfall",
           35: "LinkVerification", 36: "ComicProgram", 37: "SearchProgram", 38: "Browsers", 39: "SeleniumDriver", 40: "PlaywrightDriver",
           41: "DynamicPages", 42: "SeleniumDriver", 43: "ElementLookup", 44: "SyncPlaywright", 45: "PlaywrightDriver", 46: "AutoWaiting",
           47: "ToolChoice", 48: "AutomationTells", 50: "PracticeQuestions"}
bad = [v for v in CONCEPT.values() if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 13: Web Scraping" if i == 1 else next(t for t in texts if t not in (">>>",))
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(),
                "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "2.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch13-page", "lecture_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v2_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
