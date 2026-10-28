#!/usr/bin/env python3
"""Writes pywheels_v9_96_0.json (a NEW file over pywheels_v9_95_1.json, which stays; refuses to overwrite) - the REPAIR of the sys.modules leak of page v9_95_0
(the concept example ImagesNeedPillow sets sys.modules['PIL'] = None; a blanked variant raises before its finally block and PIL stays None for every later program).
The same wheels and Pyodide packages. The boot program now:
(1) imports pypdf, docx, PIL, lxml and cryptography (the submodules the chapter uses) so that they are in the snapshot;
(2) _reset_library puts back, BEFORE and AFTER every program (the worker's _restore is wrapped once, lazily, from _before_run), the working folder, every module of those packages
    in sys.modules (a None entry becomes the real module again) and their module attributes;
(3) general guard: every sys.modules entry whose value is None and which was not None at boot is deleted (a name that was a real module at boot is put back);
(4) the garbage-collection hook of the controller's brief (gc.collect twice, warnings ignored) before and after every program;
(5) none of the worker's own names (_LIBS, _restore, _run, _run_inner, _inlib, _state_x, _CWD0) is used as a module-level name.
Usage: pywheels_make_v9_96_0.py"""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); out = os.path.join(H, "pywheels_v9_96_0.json")
if os.path.exists(out): sys.exit("refusing to overwrite " + out)
d = json.load(open(os.path.join(H, "pywheels_v9_95_1.json"), encoding="utf-8"))
BOOT = '''import os, sys, gc, warnings
import pypdf, docx, docx.document, lxml, lxml.etree, PIL, PIL.Image, cryptography
import cryptography.hazmat.primitives.ciphers, cryptography.hazmat.primitives.ciphers.algorithms, cryptography.hazmat.primitives.ciphers.modes
try:
    import pypdf.generic._image_xobject
except Exception:
    pass
_cwd0 = os.getcwd()
_PKGS = ('pypdf', 'docx', 'PIL', 'lxml', 'cryptography')
def _snapshot_libraries():
    snap = {}
    for name, mod in list(sys.modules.items()):
        if mod is not None and name.split('.')[0] in _PKGS:
            snap[name] = (mod, dict(vars(mod)))
    return snap
_lib_snap = _snapshot_libraries()
_boot_real = {name: mod for name, mod in list(sys.modules.items()) if mod is not None}
def _gc_clean():
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        gc.collect(); gc.collect()
def _reset_library():
    # one Python serves many programs in the browser; put the folder, the library modules and their attributes back as they were at start
    os.chdir(_cwd0)
    # general guard: a sys.modules entry left at None by a program (sys.modules['PIL'] = None) is a state; a name that was a real module at boot gets it back, any other is deleted
    for name in [n for n, m in list(sys.modules.items()) if m is None]:
        if name in _boot_real:
            sys.modules[name] = _boot_real[name]
        else:
            del sys.modules[name]
    for name, (mod, saved) in _lib_snap.items():
        sys.modules[name] = mod
        for key in [k for k in vars(mod) if k not in saved]:
            try:
                delattr(mod, key)
            except Exception:
                pass
        vars(mod).update(saved)
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
d["boot_python"] = BOOT; d["_version"] = "9.96.0"
d["_note"] += " VERSION 9.96.0 (new file over 9.95.1; the repair of the sys.modules leak): the boot program imports pypdf, python-docx, Pillow, lxml and cryptography and snapshots every module of them; before AND after every program (the worker's _restore wrapped once, lazily, from _before_run) it puts the working folder, those modules in sys.modules (a None entry becomes the real module again) and their module attributes back, and as a general guard deletes every sys.modules entry that is None and was not None at start (the name of a real module of the start is put back). The cause: the example ImagesNeedPillow sets sys.modules['PIL'] = None and restores it in a finally block; a variant of it with one token blanked raised before that block and left PIL at None for every later program that imports PIL."
json.dump(d, open(out, "w", encoding="utf-8"), indent=1, ensure_ascii=False); print("wrote", out)
