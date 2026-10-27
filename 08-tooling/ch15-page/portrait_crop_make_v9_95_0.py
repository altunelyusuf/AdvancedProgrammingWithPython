#!/usr/bin/env python3
"""Makes the landscape head-and-shoulders crop of the one portrait among the chapter 15 story pictures (Jonathan Rochelle, 768 x 1024) as a NEW asset file
(the original stays), and the provenance note ASSETS_PROVENANCE_v1_0_1.md (a new file over v1_0_0, which stays). Why: a portrait photograph fills the first
screen on a phone and pushes the story text below it (the lesson of the chapter 18 page). Run BEFORE the first build. Refuses to overwrite. Usage: portrait_crop_make_v9_95_0.py"""
__version__ = "9.95.0"
import os, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(R, "03-materials/ch15/assets")
BOX = {"image_rochelle_google.jpg": ((0, 190, 768, 622), "image_rochelle_crop.jpg", "CC BY 2.0")}
outs = [os.path.join(A, v[1]) for v in BOX.values()] + [os.path.join(A, "ASSETS_PROVENANCE_v1_0_1.md")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
rows = ""
for src, (box, dst, lic) in BOX.items():
    im = Image.open(os.path.join(A, src)).convert("RGB"); w, h = im.size
    c = im.crop(box); c.save(os.path.join(A, dst), quality=90); print(dst, c.size)
    rows += "| %s | %s (%d x %d), cropped to the box x %d-%d, y %d-%d (%d x %d pixels, head and torso, landscape) | %s |\n" % (dst, src, w, h, box[0], box[2], box[1], box[3], box[2] - box[0], box[3] - box[1], lic)
open(outs[1], "w", encoding="utf-8").write("# Chapter 15 page assets - crop for the Stories tab (v1.0.1)\n\nThe original photograph stays as it is (ASSETS_PROVENANCE_v1_0_0.md and story_images_v2_0_0.json). The file below is made so that the story text starts within the first screen on a phone (390 x 844) and on a laptop (1366 x 768) instead of below a full-height portrait.\n\n| file | made from | licence |\n|---|---|---|\n" + rows + "\nThe credit line carried on the page is in 08-tooling/ch15-page/stories_img_v9_95_0.json (the deck's credit plus the word 'cropped').\n")
