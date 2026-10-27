#!/usr/bin/env python3
"""Writes standin_v9_95_0.json (a NEW file over standin_v1_0_0.json, which stays): the same markers, note, recorded-only examples and notice, with example_notes emptied. Why: those three notes
(title, connect, values) belong to the deck's earlier worked examples, whose names the Chapter examples no longer have; the Chapter examples are now the deck 2.0.1 manifest's 25 examples, and each gives the
same result in the browser's Python as recorded (manifest_pyodide_check_v9_95_0.log: PASS), so none needs a note. Refuses to overwrite. Usage: standin_make_v9_95_0.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); o = os.path.join(H, "standin_v9_95_0.json")
if os.path.exists(o): sys.exit("refusing to overwrite " + o)
d = json.load(open(os.path.join(H, "standin_v1_0_0.json"), encoding="utf-8")); d["_version"] = "9.95.0"; d["example_notes"] = {}
d["_note"] = "Read by sen0414_page_data_v2_25_0.py. Version 9.95.0 (over 1.0.0): example_notes emptied, see standin_make_v9_95_0.py."
json.dump(d, open(o, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", o)
