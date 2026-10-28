#!/usr/bin/env python3
"""Writes the page inputs of the chapter 17 page v9.95.0 (NEW files only; nothing committed is edited; refuses to overwrite):
  08-tooling/ch17-page/stories_img_v9_95_0.json   over stories_img_v1_0_1.json (which recorded no pictures): the five story pictures of the deck 2.0.0 (assets story_images_v2_0_0.json),
                                                  the two portrait-shaped ones (Warnock, the PKZIP floppy) as the landscape crops made by portrait_crop_make_v9_95_0.py, credit = the deck's SlideCredit plus 'cropped' for those two
  08-tooling/ch17-deck/examples_out_v9_95_0.json  the Lab's 'Chapter examples' made FROM THE MANIFEST 03-materials/ch17/page/chapter_code_ch17_v1_0_0.json (same code, same order; one cell per example, no recorded echo)
  08-tooling/ch17-page/limits_v9_95_0.json        over limits_v1_0_0.json: a sentence says where the Chapter examples come from
Usage: page_inputs_make_v9_95_0.py"""
__version__ = "9.95.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); T = os.path.join(R, "08-tooling")
A = os.path.join(R, "03-materials/ch17/assets")
outs = [os.path.join(H, "stories_img_v9_95_0.json"), os.path.join(T, "ch17-deck/examples_out_v9_95_0.json"), os.path.join(H, "limits_v9_95_0.json")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
lic = json.load(open(os.path.join(A, "story_images_v2_0_0.json"), encoding="utf-8"))
MAP = [("WarnockCamelot1991", "image_warnock.jpg", "image_warnock_crop.jpg"), ("ZipFormat1989", "image_pkzip.jpg", "image_pkzip_crop.jpg"),
       ("OoxmlStandard2006", "image_ooxml.jpg", "image_ooxml.jpg"), ("PdfBecomesIso2008", "image_adobe_hq.jpg", "image_adobe_hq.jpg"),
       ("DocxNameTrap2014", "image_pypi.jpg", "image_pypi.jpg")]
si = {"_version": "9.95.0", "_note": "Story pictures for the chapter 17 page's Stories tab (new file; stories_img_v1_0_1.json recorded none): the files are in 03-materials/ch17/assets, the licences in story_images_v2_0_0.json there; the same five stories and pictures as the chapter 17 deck 2.0.0 (08-tooling/ch17-deck/deck_content_v2_0_0.py), credit = the deck's SlideCredit; the two portrait-shaped photographs (Warnock, the PKZIP floppy) are the landscape crops of ASSETS_PROVENANCE_v1_0_1.md so that the story text starts within the first screen. The story PypdfFourNames has no picture, as it has no story in the deck."}
for sid, orig, fn in MAP:
    cr = lic[orig]["SlideCredit"]
    if fn != orig: cr = cr.rstrip(".") + " (cropped)."
    si[sid] = [{"file": fn, "credit": cr}]
json.dump(si, open(outs[0], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
man = json.load(open(os.path.join(R, "03-materials/ch17/page/chapter_code_ch17_v1_0_0.json"), encoding="utf-8"))
ex = {"_version": "9.95.0", "_note": "Made from chapter_code_ch17_v1_0_0.json: the deck's 28 code examples in slide order, the code as the manifest has it."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
assert len(ex) == 30
json.dump(ex, open(outs[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
lm = json.load(open(os.path.join(H, "limits_v1_0_0.json"), encoding="utf-8")); L = list(lm["limits"])
old = "Every example was run in the browser and compared with its stored result."
assert old in L[0]
L[0] = L[0].replace(old, "Every example was run in the browser and compared with its stored result. The page's Chapter examples are the 28 code examples of the deck, taken from the deck's chapter-code manifest (same code, same order); each was run in the browser's Python (Pyodide 0.28.2) and its result compared with the manifest's recorded result before the page was built.")
json.dump({"_version": "9.95.0", "limits": L}, open(outs[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", *[os.path.relpath(o, R) for o in outs])
