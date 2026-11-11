#!/usr/bin/env python3
"""Writes page_data_v9_96_1.json (the standalone data file the page tests read) as a NEW file: page_data_v9_96_0.json with only 'stories', 'chaptercode' and '_version' taken from the data block of
the page sen0414_ch17_page_v9_96_1.html (made by sen0414_page_stories_patch_v1_0_0.py); every other key, including mission, ndiag_abox and index_page, stays as it was. Refuses to overwrite. Usage: page_data_make_v9_96_1.py"""
__version__ = "9.96.1"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H))
dst = os.path.join(H, "page_data_v9_96_1.json")
if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
TAG = '<script type="application/json" id="data">'
h = open(os.path.join(R, "03-materials/ch17/page/sen0414_ch17_page_v9_96_1.html"), encoding="utf-8").read(); a = h.index(TAG) + len(TAG); emb = json.loads(h[a:h.index("</script>", a)])
d = json.load(open(os.path.join(H, "page_data_v9_96_0.json"), encoding="utf-8"))
for k in ("stories", "chaptercode", "_version"): d[k] = emb[k]
json.dump(d, open(dst, "w", encoding="utf-8"), indent=1, ensure_ascii=True); print("wrote", dst)
