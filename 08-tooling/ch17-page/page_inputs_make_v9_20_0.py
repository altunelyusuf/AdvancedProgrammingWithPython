#!/usr/bin/env python3
"""Writes the one page input of the chapter 17 page v9.20.0 that is made from the deck's chapter-code manifest 03-materials/ch17/page/chapter_code_ch17_v1_1_0.json (deck 3.0.0):
  08-tooling/ch17-deck/examples_out_v3_0_0.json   one Lab / Playground cell per manifest example, same code, same order
The other inputs of the page (limits, pywheels, standin, stories_img, corpus_manifest, all _v9_20_0) are the newest ones of the chapter, renamed to the page version; the domain ABox is
sen0414_ch17_domain_abox_v1_0_4.ttl (abox_lambda_free_make_v1_0_0.py). Refuses to overwrite an existing file. Usage: page_inputs_make_v9_20_0.py"""
__version__ = "9.20.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.normpath(os.path.join(H, "..", ".."))
man = json.load(open(os.path.join(R, "03-materials/ch17/page/chapter_code_ch17_v1_1_0.json"), encoding="utf-8"))
path = os.path.join(R, "08-tooling/ch17-deck/examples_out_v3_0_0.json")
if os.path.exists(path): sys.exit("refusing to overwrite " + path)
ex = {"_version": "3.0.0", "_note": "Made from the chapter-code manifest 03-materials/ch17/page/chapter_code_ch17_v1_1_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
json.dump(ex, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", os.path.relpath(path, R))
