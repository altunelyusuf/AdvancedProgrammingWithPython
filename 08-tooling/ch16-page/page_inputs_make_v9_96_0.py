#!/usr/bin/env python3
"""Writes the page inputs of the chapter 16 page v9.96.0 (NEW files only; nothing committed is edited; refuses to overwrite). The page v9.96.0 repairs the page v9.95.0 (leak probe v1_2_0 FAIL):
  pywheels_v9_96_0.json   over pywheels_v1_0_0.json: the boot program gets the garbage-collection hook of the controller's repair (a collection before every program and, wrapped lazily from _before_run, after every program)
  standin_v9_96_0.json, stories_img_v9_96_0.json, limits_v9_96_0.json, ch16-deck/examples_out_v9_96_0.json: the v9_95_0 files with the same content under the v9_96_0 name
Usage: page_inputs_make_v9_96_0.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H)
outs = {"pywheels": os.path.join(H, "pywheels_v9_96_0.json"), "standin": os.path.join(H, "standin_v9_96_0.json"), "stories": os.path.join(H, "stories_img_v9_96_0.json"),
        "limits": os.path.join(H, "limits_v9_96_0.json"), "examples": os.path.join(T, "ch16-deck/examples_out_v9_96_0.json")}
for o in outs.values():
    if os.path.exists(o): sys.exit("refusing to overwrite " + o)
pw = json.load(open(os.path.join(H, "pywheels_v1_0_0.json"), encoding="utf-8"))
old = "def _before_run():\n    os.chdir(_cwd0); _put()\n"
assert pw["boot_python"].endswith(old)
new = '''import gc, warnings
def _gc_clean():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        gc.collect(); gc.collect()
def _before_run():
    _gc_clean()
    os.chdir(_cwd0); _put()
    _o = globals().get('_restore')
    if _o is not None and not getattr(_o, '_gc_wrapped', False):
        def _restore_and_gc(*_a, **_k):
            try: return _o(*_a, **_k)
            finally: _gc_clean()
        _restore_and_gc._gc_wrapped = True
        globals()['_restore'] = _restore_and_gc
'''
pw["boot_python"] = pw["boot_python"][:-len(old)] + new
pw["_version"] = "9.96.0"
pw["_note"] += " Version 9.96.0 (over 1.0.0): the boot program also collects garbage before every program and, through _restore wrapped once from _before_run, after every program, so that sqlite3 connections left alive in reference cycles by one program neither keep the shared in-memory database alive nor emit a ResourceWarning into the next program."
json.dump(pw, open(outs["pywheels"], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
src = {"standin": "standin_v9_95_0.json", "stories": "stories_img_v9_95_0.json", "limits": "limits_v9_95_0.json"}
for k, f in src.items():
    d = json.load(open(os.path.join(H, f), encoding="utf-8")); d["_version"] = "9.96.0"
    json.dump(d, open(outs[k], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
d = json.load(open(os.path.join(T, "ch16-deck/examples_out_v9_95_0.json"), encoding="utf-8")); d["_version"] = "9.96.0"
json.dump(d, open(outs["examples"], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote", *[os.path.relpath(o, os.path.dirname(T)) for o in outs.values()])
