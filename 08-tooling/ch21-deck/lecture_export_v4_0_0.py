#!/usr/bin/env python3
"""Exports the chapter 21 deck 4.0.0 (40 slides) slide titles and speaker notes to ../ch21-page/lecture_v4_0_0.json, the Lecture tab of the chapter 21 page v9.108.0
(new file over lecture_v1_0_0.json, which describes the first-version deck that no longer matches; Lineage14). A code slide is linked to a page concept by hand (the chapter-code
manifest 03-materials/ch21/page/chapter_code_ch21_v1_0_0.json names book topics, whose labels differ from the page concepts); every concept id is checked against the concept ids of the
chapter's page data (the newest page_data json that holds nodes). Other slides carry no concept. Usage: lecture_export_v4_0_0.py <deck.pptx> <python-version>"""
__version__ = "4.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch21-page", "page_data_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[-1]))["nodes"]}
# each code slide is linked by hand to the page concept that its example shows (slide of the code slide: concept id)
CONCEPT = {8: "ColorNames", 10: "BoxTuple", 11: "CropBox", 12: "TileLoop", 16: "PasteMask", 17: "RotateExpand", 20: "SaveFormats", 25: "LogoFileLoop", 26: "RectangleEllipse",
           27: "TextMeasuring", 31: "ClipboardCopyPaste", 32: "LinePlot", 33: "BarChart", 36: "TileMaker", 37: "SeatingCards"}
bad = sorted({v for v in CONCEPT.values() if v not in IDS})
if bad: raise SystemExit("REFUSED: unknown concept ids %r" % bad)
dst = os.path.join(HERE, "..", "ch21-page", "lecture_v4_0_0.json")
if os.path.exists(dst): raise SystemExit("refusing to overwrite " + dst)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = sl.shapes.title.text_frame.text if sl.shapes.title is not None and sl.shapes.title.has_text_frame and sl.shapes.title.text_frame.text.strip() else texts[0]
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "4.0.0", "_python": sys.argv[2], "slides": out}, open(dst, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v4_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
