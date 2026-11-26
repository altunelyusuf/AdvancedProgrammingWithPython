#!/usr/bin/env python3
"""Writes the page inputs of the chapter 19 page v9.99.0 (Lineage13; built from the deck 4.0.0 and its chapter-code manifest 03-materials/ch19/page/chapter_code_ch19_v1_2_0.json):
  08-tooling/ch19-deck/examples_out_v9_99_0.json   one Lab / Playground cell per manifest example, same code, same order (new file; the older files stay)
  08-tooling/ch19-page/stories_img_v9_99_0.json    the six story pictures of the deck 4.0.0 (files and licences in 03-materials/ch19/assets/story_images_v1_1_0.json): only the Year 2038 picture differs from 9.97.2
The other inputs (pywheels, standin, limits, resources, quiz, question bank) are unchanged and are read as their newest files. Refuses to overwrite an existing file. Usage: page_inputs_make_v9_99_0.py"""
__version__ = "9.99.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
man = json.load(open(os.path.join(R, "03-materials/ch19/page/chapter_code_ch19_v1_2_0.json"), encoding="utf-8"))
lic = json.load(open(os.path.join(R, "03-materials/ch19/assets/story_images_v1_1_0.json"), encoding="utf-8"))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
ex = {"_version": "9.99.0", "_note": "Made from the chapter-code manifest 03-materials/ch19/page/chapter_code_ch19_v1_2_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch19-deck/examples_out_v9_99_0.json"), ex)
old = json.load(open(os.path.join(H, "stories_img_v9_97_2.json"), encoding="utf-8"))
si = {"_version": "9.99.0", "_note": "Story pictures for the chapter 19 page's Stories tab: files in 03-materials/ch19/assets, licences in story_images_v1_1_0.json there; the same mapping as the chapter 19 deck 4.0.0; credit = the deck's SlideCredit. 9.99.0: the Year 2038 picture is the frame of a public-domain animation (Wikimedia Commons), not a drawing."}
for k, v in old.items():
    if not k.startswith("_"): si[k] = v
si["Year2038Wrap"] = [{"file": "image_y2038_commons.png", "credit": lic["image_y2038_commons.png"]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_99_0.json"), si)
