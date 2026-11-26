#!/usr/bin/env python3
"""Writes the page inputs of the chapter 20 page v9.101.0 (Lineage13; built from the deck 4.0.1 and its chapter-code manifest 03-materials/ch20/page/chapter_code_ch20_v1_2_1.json):
  03-materials/ch20/page/chapter_code_ch20_v1_2_2.json   the manifest 1.2.1 plus, as 1.0.1 did over 1.0.0, "recorded" (the reason) on the 8 examples that a browser cannot run and the note on 'control' (texts copied from 1.0.2)
  08-tooling/ch20-deck/examples_out_v9_101_0.json        one Lab / Playground cell per manifest example, same code, same order
  08-tooling/ch20-page/stories_img_v9_101_0.json         the six story pictures of the deck 4.0.1 (files and licences in 03-materials/ch20/assets/story_images_v1_1_0.json): only the AT&T picture differs from 9.99.1
The other inputs (pywheels 1.0.1, standin 1.0.1, limits, resources, quiz, question bank) are unchanged and are read as their newest files. Refuses to overwrite an existing file. Usage: page_inputs_make_v9_101_0.py"""
__version__ = "9.101.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
def put(path, obj):
    if os.path.exists(path): sys.exit("refusing to overwrite " + path)
    json.dump(obj, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
man = json.load(open(os.path.join(R, "03-materials/ch20/page/chapter_code_ch20_v1_2_1.json"), encoding="utf-8"))
old = json.load(open(os.path.join(R, "03-materials/ch20/page/chapter_code_ch20_v1_0_2.json"), encoding="utf-8"))
lic = json.load(open(os.path.join(R, "03-materials/ch20/assets/story_images_v1_1_0.json"), encoding="utf-8"))
byid = {e["id"]: e for e in old["examples"]}
man["version"] = "1.2.2"
man["_note"] = ("1.2.2 over 1.2.1: the 8 examples that need ezgmail or a local mail server carry \"recorded\" (the page then shows the result recorded on the slide instead of running them), and the example 'control' "
                "carries its note on the subprocess stand-in; the texts are those of 1.0.2. Code and expected results are unchanged (identical to 1.2.1 and to 1.0.2).")
n = 0
for e in man["examples"]:
    o = byid[e["id"]]
    assert o["code"] == e["code"] and o["expected"] == e["expected"], e["id"]
    for k in ("recorded", "note"):
        if k in o: e[k] = o[k]; n += k == "recorded"
assert n == 8
put(os.path.join(R, "03-materials/ch20/page/chapter_code_ch20_v1_2_2.json"), man)
ex = {"_version": "9.101.0", "_note": "Made from the chapter-code manifest 03-materials/ch20/page/chapter_code_ch20_v1_2_2.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
put(os.path.join(R, "08-tooling/ch20-deck/examples_out_v9_101_0.json"), ex)
prev = json.load(open(os.path.join(H, "stories_img_v9_99_1.json"), encoding="utf-8"))
si = {"_version": "9.101.0", "_note": "Story pictures for the chapter 20 page's Stories tab: files in 03-materials/ch20/assets, licences in story_images_v1_1_0.json there; the same mapping as the chapter 20 deck 4.0.1; credit = the deck's SlideCredit. Only the AT&T picture differs from 9.99.1: a sourced photograph replaces the drawing."}
for k, v in prev.items():
    if not k.startswith("_"): si[k] = v
si["Att2025"] = [{"file": "image_att_commons.jpg", "credit": lic["image_att_commons.jpg"]["SlideCredit"]}]
put(os.path.join(H, "stories_img_v9_101_0.json"), si)
