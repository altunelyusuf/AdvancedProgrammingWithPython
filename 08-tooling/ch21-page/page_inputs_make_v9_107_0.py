#!/usr/bin/env python3
"""Writes the page inputs of the chapter 21 page v9.107.0 (Lineage14; built from the deck 4.0.0 and its chapter-code manifest 03-materials/ch21/page/chapter_code_ch21_v1_0_0.json):
  08-tooling/ch21-deck/examples_out_v9_107_0.json   one Lab / Playground cell per manifest example, same code, same order (the page builder reads the deck folder's newest file first)
  08-tooling/ch21-page/stories_img_v9_107_0.json    the six story pictures of the deck 4.0.0 (files and licences in 03-materials/ch21/assets/story_images_v1_0_0.json), keyed by the ids of sen0414_ch21_stories_v1_0_1.py
The other inputs (pywheels, standin, limits, resources, quiz, question bank) are unchanged and are read as their newest files. Refuses to overwrite an existing file. Usage: page_inputs_make_v9_107_0.py"""
__version__ = "9.107.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
man = json.load(open(os.path.join(R, "03-materials/ch21/page/chapter_code_ch21_v1_0_0.json"), encoding="utf-8"))
lic = json.load(open(os.path.join(R, "03-materials/ch21/assets/story_images_v1_0_0.json"), encoding="utf-8"))
ex = {"_version": "9.107.0", "_note": "Made from the chapter-code manifest 03-materials/ch21/page/chapter_code_ch21_v1_0_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch21-deck/examples_out_v9_107_0.json"), ex)
MAP = {"Kirsch1957": "image_kirsch.jpg", "Alpha1970s": "image_alpha.jpg", "Png1996": "image_png.jpg", "Jpeg1992": "image_jpeg.jpg", "Matplotlib2003": "image_matplotlib.jpg", "Pil1995": "image_pil.jpg"}
si = {"_version": "9.107.0", "_note": "Story pictures for the chapter 21 page's Stories tab: files in 03-materials/ch21/assets, licences in story_images_v1_0_0.json there; the same mapping as the chapter 21 deck 4.0.0; credit = the deck's SlideCredit."}
for sid, fn in MAP.items(): si[sid] = [{"file": fn, "credit": lic[fn]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_107_0.json"), si)
