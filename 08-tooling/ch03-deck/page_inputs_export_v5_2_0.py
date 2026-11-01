#!/usr/bin/env python3
"""Exports the finished chapter 3 deck 5.2.0 and its manifest 1.2_0 into the two page inputs (NEW files; the files of deck 5.1.0 stay):
  ../ch03-page/lecture_v2_2_0.json     the Lecture tab: slide titles and speaker notes (teach slides included), each slide tied to the concept it teaches
                                        (the teach slide shares the concept of the code slide after it); every concept id is checked against the ids of the page data v9_91_0
  ./examples_out_v5_2_0.json           the page's Chapter examples pane: each example one cell (the whole listing, no recorded echo), exactly the code of the manifest, in its slide order
The slide-to-concept ties are those of lecture_v2_1_0.json (deck 5.1.0), by example; the story slides of Gauss and of PEP 572 are tied to the concepts they illustrate.
Usage: page_inputs_export_v5_2_0.py <deck.pptx> <manifest.json> <python-version> <page_data.json>   (task TK_MS_Ch03_Build)"""
__version__ = "5.2.0"
import json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
CONCEPT = {"while": "WhileStatement", "accumulator": "Accumulator", "breakloop": "InfiniteLoop", "continue": "ContinueStatement", "walrus": "AssignmentExpressionLoop",
           "forrange": "ForStatement", "rangeargs": "RangeStartStop", "lazyrange": "LazyRange", "listtuple": "ListValue", "dictloop": "DictionaryValue",
           "enumzip": "EnumerateFunction", "zipstrict": "ZipStrict", "iterator": "IteratorObject", "loopelse": "LoopElseClause", "importrandom": "RandomModule",
           "importforms": "ImportStyle", "importerror": "ModuleSearchPath", "sysexit": "ExitFunction", "guess1": "GuessTheNumber", "guess2": "LoopElseClause",
           "rps1": "RockPaperScissors", "rps2": "RockPaperScissors"}
STORY = {"Story: Gauss added 1 to 100 without a loop": "Accumulator", "Story: the walrus operator and PEP 572": "AssignmentExpressionLoop",
         "Story: why range stops before the end": "HalfOpenRange"}
ids = {n["id"] for n in json.load(open(sys.argv[4]))["nodes"]}
bad = [v for v in list(CONCEPT.values()) + list(STORY.values()) if v not in ids]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
man = json.load(open(sys.argv[2], encoding="utf-8"))
code_slide = {e["slide"]: e["id"] for e in man["examples"]}
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.text_frame.text.strip() != ">>>"]
    title = texts[0]
    cid = ""
    if i in code_slide:
        cid = CONCEPT[code_slide[i]]
    elif i + 1 in code_slide:
        cid = CONCEPT[code_slide[i + 1]]
    elif title in STORY:
        cid = STORY[title]
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": cid, "visual": ""})
json.dump({"_version": "2.2.0", "_deck": "5.2.0", "_python": sys.argv[3],
           "_note": "2.2.0 (over 2.1.0, which stays as it is): the slide titles and the speaker notes of the deck 5.2.0 (teach slides included), each slide tied to a concept by its example or its title; %d slides tied." % sum(1 for s in out if s["concept"]),
           "slides": out},
          open(os.path.join(HERE, "..", "ch03-page", "lecture_v2_2_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
ex = {"_version": "5.2.0", "_note": "5.2.0 New file over 3.1.0 (which stays as it is): the worked examples of the chapter 3 deck 5.2.0 for the page-data builder, taken from the deck's chapter-code manifest "
      "03-materials/ch03/page/chapter_code_ch03_v1_2_0.json (indented, no prompt, no lambda). Each example is one cell (the whole listing, no recorded echo), so the page's Chapter examples pane carries exactly the code of the deck 5.2.0, in its slide order. Written by TK_MS_Ch03_Build.",
      "_python": sys.argv[3]}
for e in man["examples"]:
    ex[e["id"]] = [[e["code"], ""]]
json.dump(ex, open(os.path.join(HERE, "examples_out_v5_2_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v2_2_0.json: %d slides, %d tied; examples_out_v5_2_0.json: %d examples" % (len(out), sum(1 for s in out if s["concept"]), len(man["examples"])))
