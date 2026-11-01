#!/usr/bin/env python3
"""Exports the chapter 7 deck v2.1.0's slide titles and speaker notes to ../ch07-page/lecture_v1_1_0.json, the Lecture tab of the chapter page (a NEW file;
lecture_v1_0_0.json, made from the deck 1.0.0, stays). Each slide is linked to the corpus concept it teaches; every concept id is checked against the ids of the
newest page data. Usage: lecture_export_v1_1_0.py <deck.pptx> <python-version> <page_data.json>  (task TK_MS_Ch07_Build)"""
__version__ = "1.1.0"
import json, os, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import examples_v2_1_0 as X
CONCEPT = {"dict_basics": "DictionaryType", "dict_vs_list": "ListContrast", "insertion_order": "InsertionOrder", "hashable_keys": "HashableKeys",
           "keys_values_items": "KeysValuesItems", "key_exists": "GetMethod", "setdefault": "SetdefaultMethod", "change_pairs": "UpdateAndMerge",
           "views_follow": "LiveAndSetLikeViews", "birthdays": "BirthdayLookup", "char_count": "CharacterCount", "counter": "CounterClass",
           "grouping": "GroupingIntoLists", "board_model": "ChessboardModel", "board_print": "ChessboardPrinter", "chess_moves": "ChessboardCommands",
           "validator": "ChessValidator", "picnic_nested": "TotalBrought", "inventory": "FantasyInventory", "loot": "LootConversion", "copies": "CopyingDictionaries",
           "json_pprint": "JsonText", "typed_records": "TypedModels", "match_dict": "MappingPattern"}
ids = {n["id"] for n in json.load(open(sys.argv[3]))["nodes"]}
bad = [v for v in CONCEPT.values() if v not in ids]
if bad:
    raise SystemExit("REFUSED: unknown concept ids %r" % bad)
man = json.load(open(os.path.join(HERE, "..", "..", "03-materials", "ch07", "page", "chapter_code_ch07_v1_1_0.json"), encoding="utf-8"))
code_slide = {e["slide"]: e["id"] for e in man["examples"]}
story_concept = {"Story: one short reply gave dictionaries an order": "InsertionOrder", "Story: the sentence the character counter counts": "CharacterCount",
                 "Story: where the squares a1 to h8 come from": "ChessboardModel", "Story: the notation that carries dictionaries": "JsonText"}
prs = Presentation(sys.argv[1]); out = []
for i, sl in enumerate(prs.slides, 1):
    texts = [sh.text_frame.text for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip() and sh.text_frame.text.strip() != ">>>"]
    title = texts[0]
    cid = ""
    if i in code_slide:
        cid = CONCEPT[code_slide[i]]
    elif i + 1 in code_slide:                 # the teach slide before a code slide
        cid = CONCEPT[code_slide[i + 1]]
    elif title in story_concept:
        cid = story_concept[title]
    out.append({"n": i, "title": title, "say": sl.notes_slide.notes_text_frame.text.strip(), "concept": cid, "visual": ""})
json.dump({"_version": __version__, "_deck": "2.1.0", "_python": sys.argv[2], "slides": out},
          open(os.path.join(HERE, "..", "ch07-page", "lecture_v1_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("lecture_v1_1_0.json:", len(out), "slides,", sum(1 for s in out if s["concept"]), "linked to a concept")
