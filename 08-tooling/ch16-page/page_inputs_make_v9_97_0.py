#!/usr/bin/env python3
"""Writes the page inputs of the chapter 16 page v9.97.0 (NEW files only; nothing committed is edited; refuses to overwrite). The page v9.97.0 repairs v9.96.0
(page test 9.37.0 P1 and P9 at 1366 px: the Playground starter had lines up to 180 characters). The starter is the new playground_v1_0_2.json (longest line 74);
the other inputs are the v9.96.0 files with the same content under the v9_97_0 name - the boot program with the garbage-collection hook is UNCHANGED:
  pywheels_v9_97_0.json, standin_v9_97_0.json, stories_img_v9_97_0.json, limits_v9_97_0.json, ch16-deck/examples_out_v9_97_0.json
Usage: page_inputs_make_v9_97_0.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H)
pairs = [(os.path.join(H, "%s_v9_96_0.json" % k), os.path.join(H, "%s_v9_97_0.json" % k)) for k in ("pywheels", "standin", "stories_img", "limits")]
pairs.append((os.path.join(T, "ch16-deck/examples_out_v9_96_0.json"), os.path.join(T, "ch16-deck/examples_out_v9_97_0.json")))
for s, o in pairs:
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
for s, o in pairs:
    d = json.load(open(s, encoding="utf-8")); d["_version"] = "9.97.0"
    json.dump(d, open(o, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", o)
