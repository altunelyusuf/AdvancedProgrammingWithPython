#!/usr/bin/env python3
"""Writes the page inputs of the chapter 18 page v9.96.1 as NEW files (refuses to overwrite; nothing committed is edited):
  03-materials/ch18/assets/image_garrett_crop.jpg      a landscape crop of the portrait of Jesse James Garrett (960 x 1280), so that the story text starts within the first screen
  03-materials/ch18/assets/ASSETS_PROVENANCE_v1_0_2.md the new picture and its crop, with licence (the full record is in story_images_v2_0_2.json)
  08-tooling/ch18-page/stories_img_v9_96_1.json        the pictures of the six stories of sen0414_ch18_stories_v1_1_0.py (AjaxName2005: the Garrett crop; the others as in v9_96_0)
  08-tooling/ch18-page/page_data_v9_96_1.json          written by page_data_make_v9_96_1.py after the page is made
Usage: page_inputs_make_v9_96_1.py"""
__version__ = "9.96.1"
import json, os, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); A = os.path.join(R, "03-materials/ch18/assets")
outs = [os.path.join(A, "image_garrett_crop.jpg"), os.path.join(A, "ASSETS_PROVENANCE_v1_0_2.md"), os.path.join(H, "stories_img_v9_96_1.json")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
rec = json.load(open(os.path.join(A, "story_images_v2_0_2.json"), encoding="utf-8"))
Image.open(os.path.join(A, "image_garrett.jpg")).convert("RGB").crop((0, 120, 960, 760)).save(outs[0], quality=90)
old = json.load(open(os.path.join(H, "stories_img_v9_96_0.json"), encoding="utf-8"))
new = {k: v for k, v in old.items() if k != "JsonMessage2001"}
new["_version"] = "9.96.1"
new["_note"] = "Story pictures for the chapter 18 page's Stories tab, for the stories of sen0414_ch18_stories_v1_1_0.py: as v9_96_0 except AjaxName2005, whose picture is the landscape crop image_garrett_crop.jpg (credit as on the deck 2.0.2 slide, licences in 03-materials/ch18/assets/story_images_v2_0_2.json)."
new["AjaxName2005"] = [{"file": "image_garrett_crop.jpg", "credit": rec["image_garrett.jpg"]["SlideCredit"][:-1] + " (cropped)."}]
json.dump(new, open(outs[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(outs[1], "w", encoding="utf-8").write("""# Chapter 18 assets - the new story picture (v1.0.2)

Made by 08-tooling/ch18-deck/story_images_fetch_v2_0_2.py and 08-tooling/ch18-page/page_inputs_make_v9_96_1.py for the owner-approved draft of 2026-11-11. Full record: story_images_v2_0_2.json.

| file | what it is | licence |
|---|---|---|
| image_garrett.jpg | Jesse James Garrett, 25 April 2007, photograph by Tim 'Avatar' Bartel, Wikimedia Commons file 'Jesse-James-Garrett Web2.0-Kongress 2007.jpg'; the 960 px thumbnail Wikimedia serves was read (full-size downloads answered HTTP 429) | CC BY 2.5 |
| image_garrett_crop.jpg | the same, cropped to the box x 0-960, y 120-760 (960 x 640 pixels, head and shoulders, landscape) for the page | CC BY 2.5 |

image_crockford.jpg and image_crockford_crop.jpg (the replaced JSON-origin story) are no longer used by the deck or the page; they stay in the folder.
""")
print("wrote", [os.path.basename(o) for o in outs])
