#!/usr/bin/env python3
"""Writes the page inputs of the chapter 17 page v9.96.1 as NEW files (refuses to overwrite; nothing committed is edited):
  03-materials/ch17/assets/image_simonyi_crop.jpg   a landscape crop of the portrait of Charles Simonyi (960 x 1446), so that the story text starts within the first screen
  03-materials/ch17/assets/ASSETS_PROVENANCE_v1_0_3.md   the two new pictures and the crop, with their licences (the full records are in story_images_v2_1_0.json)
  08-tooling/ch17-page/stories_img_v9_96_1.json      the pictures of the six stories of sen0414_ch17_stories_v1_1_0.py (WordDocBinary2008: the Office 2007 boxes; WordSourceCode2014: the Simonyi crop;
                                                      PypdfFourNames: the Python logo, as the deck's new story slide)
Usage: page_inputs_make_v9_96_1.py"""
__version__ = "9.96.1"
import json, os, sys
from PIL import Image
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); A = os.path.join(R, "03-materials/ch17/assets")
outs = [os.path.join(A, "image_simonyi_crop.jpg"), os.path.join(A, "ASSETS_PROVENANCE_v1_0_3.md"), os.path.join(H, "stories_img_v9_96_1.json")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
rec = json.load(open(os.path.join(A, "story_images_v2_1_0.json"), encoding="utf-8"))
im = Image.open(os.path.join(A, "image_simonyi.jpg")).convert("RGB"); box = (0, 170, 960, 810)
im.crop(box).save(outs[0], quality=90)
old = json.load(open(os.path.join(H, "stories_img_v9_96_0.json"), encoding="utf-8"))
new = {"_version": "9.96.1",
       "_note": "Story pictures for the chapter 17 page's Stories tab, for the stories of sen0414_ch17_stories_v1_1_0.py: the same pictures and credits as the deck 2.1.0 (08-tooling/ch17-deck/deck_content_v2_1_0.py; licences in 03-materials/ch17/assets/story_images_v2_1_0.json); the portrait of Simonyi is the landscape crop image_simonyi_crop.jpg.",
       "WarnockCamelot1991": old["WarnockCamelot1991"],
       "WordDocBinary2008": [{"file": "image_ooxml.jpg", "credit": rec["image_ooxml.jpg"]["SlideCredit"]}],
       "WordSourceCode2014": [{"file": "image_simonyi_crop.jpg", "credit": rec["image_simonyi.jpg"]["SlideCredit"][:-1] + " (cropped)."}],
       "PdfBecomesIso2008": old["PdfBecomesIso2008"],
       "PypdfFourNames": [{"file": "image_python1990s.jpg", "credit": rec["image_python1990s.jpg"]["SlideCredit"]}],
       "DocxNameTrap2014": old["DocxNameTrap2014"]}
json.dump(new, open(outs[2], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
open(outs[1], "w", encoding="utf-8").write("""# Chapter 17 assets - the new story pictures (v1.0.3)

Made by 08-tooling/ch17-deck/story_images_fetch_v2_1_0.py and 08-tooling/ch17-page/page_inputs_make_v9_96_1.py for the owner-approved drafts of 2026-11-11. Full records: story_images_v2_1_0.json.

| file | what it is | licence |
|---|---|---|
| image_simonyi.jpg | Charles Simonyi, 13 December 2006, NASA photograph, Wikimedia Commons file 'Charles simonyi.jpg'; the 960 px thumbnail Wikimedia serves was read (full-size downloads answered HTTP 429) | Public domain (NASA) |
| image_simonyi_crop.jpg | the same, cropped to the box x 0-960, y 170-810 (960 x 640 pixels, face and shoulders, landscape) for the page | Public domain (NASA) |
| image_python1990s.jpg | the Python logo used between the 1990s and 2006, drawn by Just van Rossum, Wikimedia Commons file 'Python logo 1990s.svg'; the 500 px PNG rendering flattened on white | Public domain |
| image_ooxml.jpg | already in 03-materials/ch17/assets (ASSETS_PROVENANCE_v1_0_2 and story_images_v2_0_0.json), now the picture of the 2008 .doc story, disclosed in the speaker notes: it shows Office 2007 boxes, not the announcement | CC BY-SA 2.0 |

image_pkzip.jpg and image_pkzip_crop.jpg (the ZIP story) are no longer used by the deck or the page; they stay in the folder.
""")
print("wrote", [os.path.basename(o) for o in outs])
