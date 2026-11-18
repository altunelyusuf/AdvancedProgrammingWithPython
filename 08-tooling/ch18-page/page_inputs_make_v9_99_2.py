#!/usr/bin/env python3
"""Writes the page inputs of the chapter 18 page v9.99.2 (the first page of the chapter built from the deck 3.0.0 and its chapter-code manifest 03-materials/ch18/page/chapter_code_ch18_v1_1_0.json):
  08-tooling/ch18-deck/examples_out_v3_0_0.json   one Lab / Playground cell per manifest example, same code, same order (new file over examples_out_v2_0_1.json, which stays)
  08-tooling/ch18-page/stories_img_v9_99_2.json   the six story pictures, the mapping of stories_img_v9_96_2.json (same stories, same pictures, same credits); a new file because the page has a new version
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_99_2.py"""
__version__ = "9.99.2"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
man = json.load(open(os.path.join(R, "03-materials/ch18/page/chapter_code_ch18_v1_1_0.json"), encoding="utf-8"))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
ex = {"_version": "3.0.0", "_note": "Made from the chapter-code manifest 03-materials/ch18/page/chapter_code_ch18_v1_1_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch18-deck/examples_out_v3_0_0.json"), ex)
si = json.load(open(os.path.join(H, "stories_img_v9_96_2.json"), encoding="utf-8"))
si["_version"] = "9.99.2"
si["_note"] = "Story pictures for the chapter 18 page's Stories tab: the mapping of stories_img_v9_96_2.json, unchanged (same stories, same pictures, same credits), written again because the page has a new version."
put(os.path.join(H, "stories_img_v9_99_2.json"), si)
