#!/usr/bin/env python3
"""Makes landscape crops of the two portrait-shaped photographs among the chapter 17 story pictures (John Warnock 434 x 509, the PKZIP floppy 768 x 1024) as NEW asset files
(the originals stay) and the provenance note ASSETS_PROVENANCE_v1_0_1.md (a new file). Why: a portrait fills the first screen on a phone and pushes the story text below it
(the lesson of the chapter 18 page). Run BEFORE the first build. Refuses to overwrite. Usage: portrait_crop_make_v9_95_0.py"""
__version__ = "9.95.0"
import os, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(R, "03-materials/ch17/assets")
BOX = {"image_warnock.jpg": ((0, 40, 434, 330), "image_warnock_crop.jpg", "CC BY-SA 3.0", "head, beard and collar"),
       "image_pkzip.jpg": ((0, 330, 768, 800), "image_pkzip_crop.jpg", "CC BY 2.0", "the whole floppy disk with the sock drawer around it")}
outs = [os.path.join(A, v[1]) for v in BOX.values()] + [os.path.join(A, "ASSETS_PROVENANCE_v1_0_1.md")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
rows = ""
for src, (box, dst, lic, what) in BOX.items():
    im = Image.open(os.path.join(A, src)).convert("RGB"); w, h = im.size
    c = im.crop(box); c.save(os.path.join(A, dst), quality=90); print(dst, c.size)
    rows += "| %s | %s (%d x %d), cropped to the box x %d-%d, y %d-%d (%d x %d pixels, %s, landscape) | %s |\n" % (dst, src, w, h, box[0], box[2], box[1], box[3], box[2] - box[0], box[3] - box[1], what, lic)
open(outs[-1], "w", encoding="utf-8").write("# Chapter 17 page assets - crops for the Stories tab (v1.0.1)\n\nThe original photographs stay as they are (story_images_v2_0_0.json carries their licences). The files below are made so that the story text starts within the first screen on a phone (390 x 844) and on a laptop (1366 x 768) instead of below a full-height portrait. The licence of a crop is the licence of its original; the page's credit line says 'cropped'.\n\n| file | made from | licence |\n|---|---|---|\n" + rows + "\nThe credit lines carried on the page are in 08-tooling/ch17-page/stories_img_v9_95_0.json (the deck's credit plus the word 'cropped' for these two).\n")
