#!/usr/bin/env python3
"""Makes the chapter 18 head-and-shoulders crops of the three portraits (Crockford, Bosak, van Rossum) as NEW asset files (the originals stay), the provenance note
ASSETS_PROVENANCE_v1_0_1.md (a new file over v1_0_0, which stays) and stories_img_v9_96_0.json (a new file over stories_img_v9_95_0.json, which stays).
Why: the originals are portraits (960x1280, 836x1219, 960x1440); the photograph then fills the first screen and the story text begins below it (story-layout probe FAIL on
stories 3, 4, 5 of page v9_95_0). Refuses to overwrite. Usage: portrait_crop_make_v9_96_0.py"""
__version__ = "9.96.0"
import json, os, sys
from PIL import Image
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
A = os.path.join(R, "03-materials/ch18/assets")
BOX = {"image_crockford.jpg": ((0, 150, 960, 790), "image_crockford_crop.jpg"),
       "image_bosak.jpg": ((0, 40, 836, 597), "image_bosak_crop.jpg"),
       "image_guido.jpg": ((0, 20, 960, 740), "image_guido_crop.jpg")}
outs = [os.path.join(A, v[1]) for v in BOX.values()] + [os.path.join(A, "ASSETS_PROVENANCE_v1_0_1.md"), os.path.join(R, "08-tooling/ch18-page/stories_img_v9_96_0.json")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
sizes = {}
for src, (box, dst) in BOX.items():
    im = Image.open(os.path.join(A, src)).convert("RGB"); sizes[src] = im.size
    c = im.crop(box); c.save(os.path.join(A, dst), quality=90); print(dst, c.size)
rows = "".join("| %s | %s (%d x %d), cropped to the box x %d-%d, y %d-%d (%d x %d pixels, head and shoulders, landscape) | %s |\n" % (
    v[1], s, sizes[s][0], sizes[s][1], v[0][0], v[0][2], v[0][1], v[0][3], v[0][2] - v[0][0], v[0][3] - v[0][1], lic) for (s, v), lic in zip(BOX.items(), ["CC BY-SA 2.0", "CC BY-SA 3.0", "CC BY-SA 2.0"]))
open(outs[3], "w", encoding="utf-8").write("# Chapter 18 page assets - crops for the Stories tab (v1.0.1)\n\nThe original photographs stay as they are (ASSETS_PROVENANCE_v1_0_0.md). These three files are made so that the story text starts within the first screen on a phone (390 x 844) and on a laptop (1366 x 768) instead of below a full-height portrait.\n\n| file | made from | licence |\n|---|---|---|\n" + rows + "\nThe credit lines carried on the page are in 08-tooling/ch18-page/stories_img_v9_96_0.json (the original credit plus the word 'cropped').\n")
d = json.load(open(os.path.join(R, "08-tooling/ch18-page/stories_img_v9_95_0.json"), encoding="utf-8"))
d["_version"] = "9.96.0"
d["_note"] = "Story pictures for the chapter 18 page's Stories tab (new file over 9.95.0, which stays): the portraits of Crockford, Bosak and van Rossum are the landscape head-and-shoulders crops (image_*_crop.jpg in 03-materials/ch18/assets, ASSETS_PROVENANCE_v1_0_1.md) so that the story text starts within the first screen; the other three are as in 9.95.0."
for sid, fn in (("JsonMessage2001", "image_crockford.jpg"), ("Xml10In1998", "image_bosak.jpg"), ("PythonLibraries2006", "image_guido.jpg")):
    e = d[sid][0]; assert e["file"] == fn
    e["file"] = BOX[fn][1]; e["credit"] = e["credit"].replace(", as titled on Wikimedia Commons.", ", as titled on Wikimedia Commons (cropped).").replace(" at OSCON 2006:", " at OSCON 2006 (cropped):")
    print(sid, e["credit"])
json.dump(d, open(outs[4], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
