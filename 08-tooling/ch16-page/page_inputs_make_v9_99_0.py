#!/usr/bin/env python3
"""Writes the page inputs of the chapter 16 page v9.99.0 (NEW files only; refuses to overwrite). The page follows deck 4.0.0 and its manifest 03-materials/ch16/page/chapter_code_ch16_v1_2_0.json
(no lambda in the examples). Files: ch16-deck/examples_out_v9_99_0.json (one Lab / Playground cell per manifest example, same code, same order, name = the example's name) and the v9.98.0
inputs pywheels, standin, stories_img, limits under the v9_99_0 name with the same content. The domain ABox is sen0414_ch16_domain_abox_v1_0_4.ttl (abox_lambda_free_make_v1_0_0.py).
Usage: page_inputs_make_v9_99_0.py"""
__version__ = "9.99.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); R = os.path.dirname(T)
man = json.load(open(os.path.join(R, "03-materials/ch16/page/chapter_code_ch16_v1_2_0.json"), encoding="utf-8"))
outs = [os.path.join(T, "ch16-deck/examples_out_v9_99_0.json")] + [os.path.join(H, "%s_v9_99_0.json" % k) for k in ("pywheels", "standin", "stories_img", "limits")]
for o in outs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
ex = {"_version": "9.99.0", "_note": "Made from the chapter-code manifest 03-materials/ch16/page/chapter_code_ch16_v1_2_0.json (same code, same order): one cell per manifest example, name = the example's name."}
for e in man["examples"]: ex[e["name"]] = [[e["code"], ""]]
json.dump(ex, open(outs[0], "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", outs[0])
for k, o in zip(("pywheels", "standin", "stories_img", "limits"), outs[1:]):
    src = os.path.join(H, "%s_v9_97_0.json" % k)
    if not os.path.exists(src): src = os.path.join(H, "%s_v9_98_0.json" % k)
    d = json.load(open(src, encoding="utf-8")); d["_version"] = "9.99.0"
    json.dump(d, open(o, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", o, "from", os.path.basename(src))
