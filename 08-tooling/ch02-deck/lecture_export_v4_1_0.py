#!/usr/bin/env python3
"""Exports the finished chapter 2 deck 4.1.0 (slide titles and speaker notes) to ../ch02-page/lecture_v1_0_0.json, the Lecture tab of the chapter page.
Each code slide and its teach slide, and the story slides, are linked to the concept they teach; every concept id is checked against the concept ids of the
chapter page data (the page the chapter's ontology files of v9_91_0 give). Usage: lecture_export_v4_1_0.py <deck.pptx> <manifest.json> <python-version>"""
__version__ = "4.1.0"
import glob, json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
_pf = sorted(glob.glob(os.path.join(HERE, "..", "ch02-page", "page_data_v*.json")), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
IDS = {n["id"] for n in json.load(open(_pf[0 if "--oldest" in sys.argv else -1]))["nodes"]}
OF = {"booleans": "BooleanValue", "comparison": "Comparison", "equality": "EqualityComparison", "chained": "ChainedComparison", "truthtable": "TruthTable",
      "notprec": "BooleanPrecedence", "mixing": "BooleanExpression", "shortcircuit": "ShortCircuit", "truthiness": "Truthiness", "block": "Block",
      "indent": "Indentation", "password": "IfStatement", "elif": "ElifClause", "elifOrder": "BranchChain", "oppositeday": "Toggle", "capacity": "DecisionPattern",
      "condexpr": "ConditionalExpression", "match": "MatchStatement", "matchseq": "SequencePattern", "matchguard": "Guard", "walrus": "AssignmentExpression"}
STORY = {"Story: the man inside the bool type": "BooleanValue", "Story: the whitespace that is the syntax": "Indentation",
         "Story: a thirty-year-old wish, granted in 3.10": "PatternMatching", "Story: the walrus that changed who leads Python": "AssignmentExpression"}
bad = [v for v in list(OF.values()) + list(STORY.values()) if v not in IDS]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
man = json.load(open(sys.argv[2], encoding="utf-8"))
CONCEPT = {}
for e in man["examples"]:
    CONCEPT[e["slide"]] = OF[e["id"]]
    CONCEPT[e["slide"] - 1] = OF[e["id"]]       # the teach slide stands right before its code slide
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.text_frame.text.strip() != ">>>"]
    title = texts[0]
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": CONCEPT.get(i) or STORY.get(title, ""), "visual": ""})
json.dump({"_version": __version__, "_deck": "4.1.0", "_python": sys.argv[3], "slides": out}, open(os.path.join(HERE, "..", "ch02-page", "lecture_v1_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v1_0_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
