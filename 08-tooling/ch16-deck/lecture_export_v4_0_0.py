#!/usr/bin/env python3
"""Exports the chapter 16 deck 4.0.0 (54 slides) slide titles and speaker notes to ../ch16-page/lecture_v4_0_0.json, the Lecture tab of the chapter 16 page v9.100.0
(new file over lecture_v1_0_0.json, which describes a 26-slide deck that no longer exists; Lineage13). A code slide is linked to the first concept of its example in the chapter-code
manifest (the manifest names book topics; a topic is linked only when a page concept has the same label) 03-materials/ch16/page/chapter_code_ch16_v1_2_0.json; every concept id is checked against the concept ids of the chapter's page data (the newest page_data json that holds nodes).
Other slides carry no concept. Usage: lecture_export_v4_0_0.py <deck.pptx> <python-version>"""
__version__ = "4.0.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(HERE))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch16-page", "page_data_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
NODES = json.load(open(_pf[-1]))["nodes"] if _pf else []
IDS = {n["id"] for n in NODES}; BYLABEL = {n["label"].lower(): n["id"] for n in NODES}
man = json.load(open(os.path.join(R, "03-materials/ch16/page/chapter_code_ch16_v1_2_0.json"), encoding="utf-8"))
CONCEPT = {}
for e in man["examples"]:
    hit = next((BYLABEL[c.lower()] for c in e.get("concepts", []) if c.lower() in BYLABEL), "")
    if hit: CONCEPT[e["slide"]] = hit
bad = sorted({v for v in CONCEPT.values() if v not in IDS})
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
    title = "Chapter 16: SQLite Databases" if i == 1 else next(t for t in texts if t != ">>>")
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "4.0.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch16-page", "lecture_v4_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v4_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
