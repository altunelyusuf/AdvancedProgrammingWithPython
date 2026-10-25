#!/usr/bin/env python3
"""Writes 08-tooling/ch04-deck/examples_out_v3_1_0.json (a NEW file; 3.0.0 and 1.2.0 stay as they are) from the deck 3.1.0's chapter-code
manifest 03-materials/ch04/page/chapter_code_ch04_v1_1_0.json, so that the page-data builder 2.25.0 carries exactly the code of the deck, in slide order.
Each example is one cell: the whole listing, no recorded echo. Written by the page task TK_Ret_Ch04_Page_Build (rebuild on the manifest 1.1.0).
Usage: examples_from_manifest_v1_0_0.py"""
__version__ = "1.1.0"
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
m = json.load(open(os.path.join(R, "03-materials/ch04/page/chapter_code_ch04_v1_1_0.json"), encoding="utf-8"))
out = {"_version": "3.1.0",
       "_note": "New file over 3.0.0 (which stays as it is and was made from manifest 1.0.0): the worked examples of the chapter 4 deck 3.1.0 for the page-data builder 2.25.0, taken from the deck's chapter-code manifest 03-materials/ch04/page/chapter_code_ch04_v1_1_0.json. Each example is one cell (the whole listing, no recorded echo), so the page's Chapter examples pane carries exactly the code of the deck 3.1.0, in its slide order. Written by the page task TK_Ret_Ch04_Page_Build (rebuild on the manifest 1.1.0).",
       "_python": m["executed_with"]["python"]}
for e in m["examples"]:
    assert e["id"] not in out
    out[e["id"]] = [[e["code"], ""]]
json.dump(out, open(os.path.join(R, "08-tooling/ch04-deck/examples_out_v3_1_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written examples_out_v3_1_0.json:", len(m["examples"]), "examples")
