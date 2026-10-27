#!/usr/bin/env python3
"""Writes the page inputs of the chapter 18 page v9.95.0 that are made from the deck's chapter-code manifest 03-materials/ch18/page/chapter_code_ch18_v1_0_1.json
(the manifest of the delivered deck v2_0_1):
  08-tooling/ch18-deck/examples_out_v2_0_1.json  the Lab / Playground examples pane's examples: one cell per manifest example, same code, same order (a NEW file over examples_out_v1_0_0.json,
                                                 the earlier deck's transcript, which stays; the page-data builder 2.25.0 reads the newest examples_out of the deck folder first)
  08-tooling/ch18-page/stories_img_v9_95_0.json  the six story pictures of the deck 2.0.1 (files and licences in 03-materials/ch18/assets), credit = the deck's SlideCredit
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_95_0.py"""
__version__ = "9.95.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
man = json.load(open(os.path.join(R, "03-materials/ch18/page/chapter_code_ch18_v1_0_1.json"), encoding="utf-8"))
lic = json.load(open(os.path.join(R, "03-materials/ch18/assets/story_images_v2_0_0.json"), encoding="utf-8"))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
ex = {"_version": "2.0.1", "_note": "Made from the chapter-code manifest 03-materials/ch18/page/chapter_code_ch18_v1_0_1.json (same code, same order): one cell per manifest example, name = the example's name. New file over examples_out_v1_0_0.json (the earlier deck's transcript), which stays unchanged; the page-data builder 2.25.0 reads the newest examples_out in the deck folder first."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch18-deck/examples_out_v2_0_1.json"), ex)
MAP = {"CsvFortran1972": "image_ibm.jpg", "Rfc4180In2005": "image_ietf.jpg", "JsonMessage2001": "image_crockford.jpg", "Xml10In1998": "image_bosak.jpg", "PythonLibraries2006": "image_guido.jpg", "BillionLaughs2002": "image_servers.jpg"}
si = {"_version": "9.95.0", "_note": "Story pictures for the chapter 18 page's Stories tab (new file over 1.0.1, which recorded none): files in 03-materials/ch18/assets, licences in story_images_v2_0_0.json there; mapping as in the chapter 18 deck 2.0.1 (08-tooling/ch18-deck/deck_content_v2_0_1.py), credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(R, "08-tooling/ch18-page/stories_img_v9_95_0.json"), si)
