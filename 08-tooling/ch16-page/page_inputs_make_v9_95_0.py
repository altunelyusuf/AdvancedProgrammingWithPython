#!/usr/bin/env python3
"""Writes the page inputs of the chapter 16 page v9.95.0 (NEW files only; nothing committed is edited; refuses to overwrite):
  08-tooling/ch16-page/stories_img_v9_95_0.json   over stories_img_v1_0_0.json (which recorded no pictures): the six story pictures of the deck 2.0.1 (assets story_images_v2_0_1.json), the three portraits as the landscape crops
                                                  made by portrait_crop_make_v9_95_0.py, credit = the deck's SlideCredit plus 'cropped' for those three
  08-tooling/ch16-deck/examples_out_v9_95_0.json  the Lab's 'Chapter examples' made FROM THE MANIFEST 03-materials/ch16/page/chapter_code_ch16_v1_0_1.json (same code, same order; one cell per example, no recorded echo, so the code runs as it is)
  08-tooling/ch16-page/limits_v9_95_0.json        over limits_v1_0_0.json: the sentence about the deck's worked examples now says where the Chapter examples come from
Usage: page_inputs_make_v9_95_0.py"""
__version__ = "9.95.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); T = os.path.join(R, "08-tooling")
A = os.path.join(R, "03-materials/ch16/assets")
outs = [os.path.join(H, "stories_img_v9_95_0.json"), os.path.join(T, "ch16-deck/examples_out_v9_95_0.json"), os.path.join(H, "limits_v9_95_0.json")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
lic = json.load(open(os.path.join(A, "story_images_v2_0_1.json"), encoding="utf-8"))
MAP = [("SqliteBegins2000", "image_hipp_sqlite.jpg", "image_hipp_sqlite.jpg"), ("CoddRelationalModel1970", "image_codd.jpg", "image_codd_crop.jpg"),
       ("PythonGainsSqlite2006", "image_guido_python.jpg", "image_guido_python.jpg"), ("StrictTables2021", "image_sqlite_banner.png", "image_sqlite_banner.png"),
       ("BobbyTables2007", "image_munroe_portrait.jpg", "image_munroe_crop.jpg"), ("AcidNamed1983", "image_jim_gray.jpg", "image_jim_gray_crop.jpg")]
si = {"_version": "9.95.0", "_note": "Story pictures for the chapter 16 page's Stories tab (new file; stories_img_v1_0_0.json recorded none): the files are in 03-materials/ch16/assets, the licences in story_images_v2_0_1.json there; the same six stories and pictures as the chapter 16 deck 2.0.1 (08-tooling/ch16-deck/deck_content_v2_0_1.py), credit = the deck's SlideCredit; the three portraits (Codd, Gray, Munroe) are the landscape crops of ASSETS_PROVENANCE_v1_0_1.md so that the story text starts within the first screen."}
for sid, orig, fn in MAP:
    cr = lic[orig]["SlideCredit"]
    if fn != orig: cr = cr.rstrip(".") + " (cropped)."
    si[sid] = [{"file": fn, "credit": cr}]
json.dump(si, open(outs[0], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
man = json.load(open(os.path.join(R, "03-materials/ch16/page/chapter_code_ch16_v1_0_1.json"), encoding="utf-8"))
ex = {"_version": "9.95.0", "_note": "Made from chapter_code_ch16_v1_0_1.json: the deck's 25 code examples in slide order, the code as the manifest has it."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
assert len(ex) == 27
json.dump(ex, open(outs[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
lm = json.load(open(os.path.join(H, "limits_v1_0_0.json"), encoding="utf-8")); L = list(lm["limits"])
old = "The deck's worked examples are used as the deck has them, so three of them print something different here (title, connect and values) and say so under the example list of Chapter examples."
assert old in L[0]
L[0] = L[0].replace(old, "The page's Chapter examples are the 25 code examples of the deck, taken from the deck's chapter-code manifest (same code, same order); each was run in the browser's Python (Pyodide 0.28.2) and its result compared with the manifest's recorded result before the page was built.")
json.dump({"_version": "9.95.0", "limits": L}, open(outs[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", *[os.path.relpath(o, R) for o in outs])
