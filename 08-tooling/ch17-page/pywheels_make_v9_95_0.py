#!/usr/bin/env python3
"""Writes pywheels_v9_95_0.json (a NEW file over pywheels_v1_0_0.json, which stays; refuses to overwrite): the same wheels and Pyodide packages, and a new boot program:
(1) the garbage-collection guard of the controller's brief (_gc_clean, _before_run, and the worker's _restore wrapped once, lazily from inside _before_run, so that the collection also
runs after every program); (2) the working folder put back before every program (as in 1.0.0); (3) the module attributes of pypdf and docx (every module of those two packages loaded at boot)
put back after EVERY program (the same lazy wrap). Usage: pywheels_make_v9_95_0.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(H, "pywheels_v9_95_0.json")
if os.path.exists(out): sys.exit("refusing to overwrite " + out)
d = json.load(open(os.path.join(H, "pywheels_v1_0_0.json"), encoding="utf-8"))
BOOT = '''import os, sys, gc, warnings
import pypdf, docx, docx.document
_cwd0 = os.getcwd()
_LIBS = {}
for _n, _m in list(sys.modules.items()):
    if _m is not None and (_n.split('.')[0] in ('pypdf', 'docx')):
        _LIBS[_n] = (_m, dict(vars(_m)))
def _gc_clean():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        gc.collect(); gc.collect()
def _reset_library():
    # one Python serves many programs in the browser; put the folder and the attributes of pypdf and python-docx back as they were at start
    os.chdir(_cwd0)
    for _n, (_m, _v) in _LIBS.items():
        sys.modules[_n] = _m
        for _k in [_k for _k in vars(_m) if _k not in _v]:
            delattr(_m, _k)
        vars(_m).update(_v)
def _before_run():
    _gc_clean()
    _reset_library()
    _o = globals().get('_restore')
    if _o is not None and not getattr(_o, '_gc_wrapped', False):
        def _restore_and_gc(*_a, **_k):
            try:
                return _o(*_a, **_k)
            finally:
                _reset_library()
                _gc_clean()
        _restore_and_gc._gc_wrapped = True
        globals()['_restore'] = _restore_and_gc
'''
d["boot_python"] = BOOT; d["_version"] = "9.95.0"
d["_note"] += " VERSION 9.95.0 (new file over 1.0.0; the wheels and Pyodide packages are those of 1.0.0, unchanged): boot_python imports pypdf and docx at start, and _before_run (called by the template at the start of every program) collects garbage with warnings ignored, puts the working folder and the module attributes of pypdf and python-docx back as they were at start, and wraps the worker's _restore once, lazily, so that the same happens after EVERY program (the template starts the boot program before it defines _restore, so the wrap is made from inside _before_run). The chapter's programs build PDF and Word files in memory or in a temporary folder and may leave file objects in reference cycles; the collection closes them before the next program."
json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", out)
