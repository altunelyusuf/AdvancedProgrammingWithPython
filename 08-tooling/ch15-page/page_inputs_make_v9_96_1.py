#!/usr/bin/env python3
"""Writes the page inputs that differ for the chapter 15 page v9.96.1 (the SECOND repair of the NOT MET pages v9.95.0 and v9.96.0). NEW files only; nothing committed is edited:
  08-tooling/ch15-page/pywheels_v9_95_2.json   over pywheels_v9_95_1.json (which stays): the boot program no longer tries to wrap the worker's restore function itself (the template runs
                                               py_boot BEFORE it defines _run and _restore, so at that time there is nothing to wrap); _before_run (the hook the template calls at the start of every program,
                                               when _restore exists) resets the library and wraps _restore ONCE, lazily, so that the library reset also runs after EVERY program.
  08-tooling/ch15-page/pyodide_python_v1_0_2.sh the recording interpreter wrapper over pywheels_v9_95_2.json
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_96_1.py"""
__version__ = "9.96.1"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
old = json.load(open(os.path.join(H, "pywheels_v9_95_1.json"), encoding="utf-8"))
b = old["boot_python"]
tail = "_before_run = _reset_library\n"
i = b.index(tail); assert b.count(tail) == 1
b = b[:i] + (
    "def _before_run():\n"
    "    _reset_library()\n"
    "    _o = globals().get('_restore')\n"
    "    if _o is not None and not getattr(_o, '_library_wrapped', False):\n"
    "        def _restore_and_reset(*_a, **_k):\n"
    "            try:\n"
    "                return _o(*_a, **_k)\n"
    "            finally:\n"
    "                _reset_library()\n"
    "        _restore_and_reset._library_wrapped = True\n"
    "        globals()['_restore'] = _restore_and_reset\n")
assert "_orig_restore" not in b
pw = dict(old); pw["_version"] = "9.95.2"; pw["boot_python"] = b
pw["_note"] = old["_note"] + " VERSION 9.95.2 (new file over 9.95.1, the second repair): the template starts the boot program before it defines the worker's _run and _restore, so the wrap of 9.95.1 found no _restore and changed nothing; now _before_run (called by the template at the start of every program, when _restore exists) resets the library and wraps _restore once, lazily, so that the library reset runs after EVERY program as well. The template is not changed."
for p in ("pywheels_v9_95_2.json", "pyodide_python_v1_0_2.sh"):
    if os.path.exists(os.path.join(H, p)): sys.exit("refusing to overwrite " + p)
json.dump(pw, open(os.path.join(H, "pywheels_v9_95_2.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
sh = open(os.path.join(H, "pyodide_python_v1_0_1.sh")).read().replace("pywheels_v9_95_1.json", "pywheels_v9_95_2.json")
open(os.path.join(H, "pyodide_python_v1_0_2.sh"), "w").write(sh); os.chmod(os.path.join(H, "pyodide_python_v1_0_2.sh"), 0o755)
print("wrote pywheels_v9_95_2.json, pyodide_python_v1_0_2.sh")
