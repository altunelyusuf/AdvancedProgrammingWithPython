#!/usr/bin/env python3
"""Writes the page inputs that differ for the chapter 15 page v9.96.0 (the repair of the NOT MET page v9.95.0). NEW file only; nothing committed is edited:
  08-tooling/ch15-page/pywheels_v9_95_1.json   over pywheels_v9_95_0.json (which stays): the boot program keeps the library reset (_before_run, now a call of _reset_library) and wraps
                                               the Python worker's restore function ONCE so that the library reset (ezsheets, google_standin, clock, working folder) also runs after EVERY program,
                                               because the leak probe v1_2_0 reads the library's public attributes after each run and the page boot of v9.95.0 restored them only before the next program.
  08-tooling/ch15-page/pyodide_python_v1_0_1.sh the recording interpreter wrapper over pywheels_v9_95_1.json
Refuses to overwrite an existing file. Usage: page_inputs_make_v9_96_0.py"""
__version__ = "9.96.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__))
old = json.load(open(os.path.join(H, "pywheels_v9_95_0.json"), encoding="utf-8"))
b = old["boot_python"]
assert b.count("def _before_run():\n") == 1
b = b.replace("def _before_run():\n", "def _reset_library():\n")
b += ("_before_run = _reset_library\n"
      "_orig_restore = globals().get('_restore')\n"
      "if _orig_restore is not None and not getattr(_orig_restore, '_library_wrapped', False):\n"
      "    def _restore_and_reset(*_a, **_k):\n"
      "        try:\n"
      "            return _orig_restore(*_a, **_k)\n"
      "        finally:\n"
      "            _reset_library()\n"
      "    _restore_and_reset._library_wrapped = True\n"
      "    globals()['_restore'] = _restore_and_reset\n")
pw = dict(old); pw["_version"] = "9.95.1"; pw["boot_python"] = b
pw["_note"] = old["_note"] + " VERSION 9.95.1 (new file over 9.95.0, the repair of the NOT MET page v9.95.0): the library reset is a function _reset_library(), _before_run is that function, and the worker's restore function (_restore, which the template calls after every program) is wrapped once so that _reset_library() runs after EVERY program as well; the changes of a program to ezsheets (ezsheets.time, ezsheets.SCOPES_SHEETS, SCOPES_DRIVE, DEFAULT_NEW_ROW_COUNT) are no longer visible after it. The template is not changed."
for p, c in (("pywheels_v9_95_1.json", None), ("pyodide_python_v1_0_1.sh", None)):
    if os.path.exists(os.path.join(H, p)): sys.exit("refusing to overwrite " + p)
json.dump(pw, open(os.path.join(H, "pywheels_v9_95_1.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
sh = open(os.path.join(H, "pyodide_python_v1_0_0.sh")).read().replace("pywheels_v9_95_0.json", "pywheels_v9_95_1.json")
open(os.path.join(H, "pyodide_python_v1_0_1.sh"), "w").write(sh); os.chmod(os.path.join(H, "pyodide_python_v1_0_1.sh"), 0o755)
print("wrote pywheels_v9_95_1.json, pyodide_python_v1_0_1.sh")
