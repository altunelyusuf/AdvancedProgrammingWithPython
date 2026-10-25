#!/usr/bin/env python3
"""Writes 08-tooling/ch10-deck/examples_out_v2_0_0.json (the Lab examples pane of the chapter 10 page) FROM the chapter-code
manifest: one entry per manifest example, in manifest order, under the manifest NAME, the code unchanged (one cell with no
recorded output, which the page-data builder keeps as the plain code). Usage: examples_from_manifest_v1_0_0.py"""
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
m = json.load(open(os.path.join(R, "03-materials/ch10/page/chapter_code_ch10_v1_0_0.json"), encoding="utf-8"))
out = {"_version": "2.0.0", "_from": "03-materials/ch10/page/chapter_code_ch10_v1_0_0.json"}
for e in m["examples"]:
    out[e["name"]] = [[e["code"], ""]]
json.dump(out, open(os.path.join(R, "08-tooling/ch10-deck/examples_out_v2_0_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote %d examples" % (len(out) - 2))
