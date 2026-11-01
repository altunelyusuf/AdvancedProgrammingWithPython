#!/usr/bin/env python3
"""Writes 08-tooling/ch04-deck/examples_out_v3_2_0.json (a NEW file; 3.1.0 and earlier stay as they are) from the deck 3.2.0's chapter-code
manifest 03-materials/ch04/page/chapter_code_ch04_v1_2_0.json, so that the page-data builder carries exactly the code of the deck, in slide order.
Each example is one cell: the whole listing, no recorded echo. Task TK_MS_Ch04_Build. Usage: examples_from_manifest_v1_2_0.py"""
__version__ = "1.2.0"
import json, os
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
m = json.load(open(os.path.join(R, "03-materials/ch04/page/chapter_code_ch04_v1_2_0.json"), encoding="utf-8"))
out = {"_version": "3.2.0",
       "_note": "New file over 3.1.0: the worked examples of the chapter 4 deck 3.2.0 (indented, no prompt, no lambda), taken from the deck's chapter-code manifest 1.2.0. Each example is one cell (the whole listing, no recorded echo), so the page's Chapter examples pane carries exactly the code of the deck, in its slide order.",
       "_python": m["executed_with"]["python"]}
for e in m["examples"]:
    assert e["id"] not in out
    out[e["id"]] = [[e["code"], ""]]
json.dump(out, open(os.path.join(R, "08-tooling/ch04-deck/examples_out_v3_2_0.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("written examples_out_v3_2_0.json:", len(m["examples"]), "examples")
