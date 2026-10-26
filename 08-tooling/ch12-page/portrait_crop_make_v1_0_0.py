#!/usr/bin/env python3
"""Makes the chapter 12 McIlroy and Ritchie head-and-shoulders crops (NEW assets; photo_doug_mcilroy.jpg and photo_dennis_ritchie_2011.jpg stay),
their provenance note v1.0.0 and the story-pictures file stories_img_v2_1_0.json (a new file over 2.0.0, which stays). Usage: portrait_crop_make_v1_0_0.py"""
import json, os
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(R, "03-materials/ch12/assets")
Image.open(os.path.join(A, "photo_doug_mcilroy.jpg")).convert("RGB").crop((0, 10, 407, 320)).save(os.path.join(A, "photo_doug_mcilroy_crop.jpg"), quality=90)
Image.open(os.path.join(A, "photo_dennis_ritchie_2011.jpg")).convert("RGB").crop((0, 50, 558, 468)).save(os.path.join(A, "photo_dennis_ritchie_2011_crop.jpg"), quality=90)
open(os.path.join(A, "ASSETS_PROVENANCE_v1_0_0.md"), "w", encoding="utf-8").write(
"""# Chapter 12 page assets - crops for the Stories tab (v1.0.0)

The original photographs stay as they are. These two files are made so that the story text starts within the first screen on a phone (390 x 844) and on a laptop (1366 x 768) instead of below a full-height portrait.

| file | made from | licence | credit carried on the page |
|---|---|---|---|
| photo_doug_mcilroy_crop.jpg | photo_doug_mcilroy.jpg (407 x 564), cropped to the box x 0-407, y 10-320 (407 x 310 pixels, head and shoulders, landscape) | CC BY 2.0 | Douglas McIlroy in 2011 (cropped). Photo: Denise Panyik-Dale, CC BY 2.0, Wikimedia Commons. |
| photo_dennis_ritchie_2011_crop.jpg | photo_dennis_ritchie_2011.jpg (558 x 717), cropped to the box x 0-558, y 50-468 (558 x 418 pixels, head and shoulders, landscape) | CC BY 2.0 | Dennis Ritchie at the Japan Prize ceremony, May 2011 (cropped). Photo: Denise Panyik-Dale, CC BY 2.0, Wikimedia Commons. |
""")
d = json.load(open(os.path.join(R, "08-tooling/ch12-page/stories_img_v2_0_0.json"), encoding="utf-8"))
d["_version"] = "2.1.0"
d["_note"] = ("Story photographs for the chapter 12 page's Stories tab (new file over 2.0.0, which stays unchanged): the McIlroy and Ritchie portraits are cropped to landscape head-and-shoulders "
              "pictures (photo_doug_mcilroy_crop.jpg and photo_dennis_ritchie_2011_crop.jpg in 03-materials/ch12/assets, ASSETS_PROVENANCE_v1_0_0.md) so that the story text starts within the first screen; the other two are as in 2.0.0.")
d["McIlroyPipes1973"] = [{"file": "photo_doug_mcilroy_crop.jpg", "credit": "Douglas McIlroy in 2011 (cropped). Photo: Denise Panyik-Dale, CC BY 2.0, Wikimedia Commons."}]
d["RitchieShebang1980"] = [{"file": "photo_dennis_ritchie_2011_crop.jpg", "credit": "Dennis Ritchie at the Japan Prize ceremony, May 2011 (cropped). Photo: Denise Panyik-Dale, CC BY 2.0, Wikimedia Commons."}]
json.dump(d, open(os.path.join(R, "08-tooling/ch12-page/stories_img_v2_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote the two crops, ASSETS_PROVENANCE_v1_0_0.md, stories_img_v2_1_0.json")
