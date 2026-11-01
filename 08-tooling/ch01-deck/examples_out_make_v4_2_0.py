#!/usr/bin/env python3
"""Writes examples_out_v4_2_0.json (a NEW file beside examples_out_v4_1_0.json): the Chapter examples pane's worked examples of chapter 1, made from the
chapter-code manifest 1.2_0 (the deck 4.2.0's code boxes, 19 examples, deck order): every example is one cell [code, ""], so that the page-data builder emits
the code exactly as the deck shows it. Usage: examples_out_make_v4_2_0.py <python-version>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
man = json.load(open(os.path.join(HERE, "..", "..", "03-materials", "ch01", "page", "chapter_code_ch01_v1_2_0.json"), encoding="utf-8"))
out = {"_version": "4.2.0", "_python": sys.argv[1], "_examples": "chapter_code_ch01_v1_2_0.json (the deck 4.2.0's code boxes)"}
for e in man["examples"]:
    out[e["id"]] = [[e["code"], ""]]
json.dump(out, open(os.path.join(HERE, "examples_out_v4_2_0.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("examples_out_v4_2_0.json:", len(man["examples"]), "examples")
