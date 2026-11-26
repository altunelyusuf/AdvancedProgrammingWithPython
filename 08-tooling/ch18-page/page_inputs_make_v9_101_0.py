#!/usr/bin/env python3
"""Writes the page input of the chapter 18 page v9.101.0 (NEW file only; refuses to overwrite; Lineage13, 2026-11-26). The page follows deck 4.0.0 and its manifest
03-materials/ch18/page/chapter_code_ch18_v1_2_0.json. File: ch18-deck/examples_out_v9_101_0.json (one Lab / Playground cell per manifest example, same code, same order, name = the example's name).
The other inputs (pywheels, standin, stories_img, limits) are unchanged and are read as their newest files. Usage: page_inputs_make_v9_101_0.py"""
__version__ = "9.101.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); R = os.path.dirname(T)
man = json.load(open(os.path.join(R, "03-materials/ch18/page/chapter_code_ch18_v1_2_0.json"), encoding="utf-8"))
out = os.path.join(T, "ch18-deck/examples_out_v9_101_0.json")
if os.path.exists(out): sys.exit("refusing to overwrite " + out)
ex = {"_version": "9.101.0", "_note": "Made from the chapter-code manifest 03-materials/ch18/page/chapter_code_ch18_v1_2_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
json.dump(ex, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", out, len(man["examples"]), "examples")
