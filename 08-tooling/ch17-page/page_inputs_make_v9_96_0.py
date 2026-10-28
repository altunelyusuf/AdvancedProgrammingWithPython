#!/usr/bin/env python3
"""Writes the page inputs of the chapter 17 page v9.96.0 as NEW files over those of v9.95.0 (same content, version 9.96.0; refuses to overwrite; nothing committed is edited):
stories_img_v9_96_0.json, limits_v9_96_0.json (08-tooling/ch17-page) and examples_out_v9_96_0.json (08-tooling/ch17-deck). The portraits, pictures, Playground starter and the examples
from the manifest are those of v9.95.0, accepted by the controller. Usage: page_inputs_make_v9_96_0.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H)
for src, dst in ((os.path.join(H, "stories_img_v9_95_0.json"), os.path.join(H, "stories_img_v9_96_0.json")), (os.path.join(H, "limits_v9_95_0.json"), os.path.join(H, "limits_v9_96_0.json")),
                 (os.path.join(T, "ch17-deck/examples_out_v9_95_0.json"), os.path.join(T, "ch17-deck/examples_out_v9_96_0.json"))):
    if os.path.exists(dst): sys.exit("refusing to overwrite " + dst)
    d = json.load(open(src, encoding="utf-8")); d["_version"] = "9.96.0"
    json.dump(d, open(dst, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", dst)
