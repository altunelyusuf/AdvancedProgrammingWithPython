#!/usr/bin/env python3
"""Makes the chapter 11 Adler head-and-shoulders crop (a NEW asset; photo_adler.jpg stays), its provenance note v1.1.0 and
the story-pictures file stories_img_v2_1_0.json (a new file over 2.0.0, which stays). Usage: adler_crop_make_v1_0_0.py"""
import json, os
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(R, "03-materials/ch11/assets")
Image.open(os.path.join(A, "photo_adler.jpg")).convert("RGB").crop((50, 180, 450, 480)).save(os.path.join(A, "photo_adler_crop.jpg"), quality=90)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_1_0.md"), "w", encoding="utf-8").write(
"""# Chapter 11 deck and page assets - provenance and licences (v1.1.0)

Version 1.0.0 stays as it is (every file it lists is unchanged). This version adds one file for the page's Stories tab, so that the story text starts within the first screen on a phone (390 x 844) instead of below a full-height portrait.

| file | made from | licence | credit carried on the page |
|---|---|---|---|
| photo_adler_crop.jpg | photo_adler.jpg (500 x 667), cropped to the box x 50-450, y 180-480 (400 x 300 pixels, head and shoulders, landscape) | Public domain (NASA) | Mark Adler (cropped). Photo: NASA, public domain, Wikimedia Commons. |
""")
d = json.load(open(os.path.join(R, "08-tooling/ch11-page/stories_img_v2_0_0.json"), encoding="utf-8"))
d["_version"] = "2.1.0"
d["_note"] = ("Story photographs for the chapter 11 page's Stories tab (new file over 2.0.0, which stays unchanged): the Adler portrait is cropped to a landscape head-and-shoulders "
              "picture (photo_adler_crop.jpg in 03-materials/ch11/assets, licence in ASSETS_PROVENANCE_v1_1_0.md) so that the story text starts within the first screen on a phone; the other three are as in 2.0.0.")
d["GaillyAdlerZlib1995"] = [{"file": "photo_adler_crop.jpg", "credit": "Mark Adler (cropped). Photo: NASA, public domain, Wikimedia Commons."}]
json.dump(d, open(os.path.join(R, "08-tooling/ch11-page/stories_img_v2_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote photo_adler_crop.jpg, ASSETS_PROVENANCE_v1_1_0.md, stories_img_v2_1_0.json")
