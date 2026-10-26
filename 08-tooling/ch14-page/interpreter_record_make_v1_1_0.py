#!/usr/bin/env python3
"""Writes interpreter_record_v1_1_0.json: the record of v1_0_0 (the openpyxl program under the seven 3.14 releases, 3.13 and 3.12, recorded 2026-10-12 with uv)
plus one row for the page's own runtime, Pyodide 0.28.2 (CPython 3.13.2) with the page's openpyxl 3.1.5 and et_xmlfile 2.0.0 wheels, run by the wrapper
pyodide_python_v1_0_0.sh. The rows of v1_0_0 are copied unchanged.
Usage (env PYODIDE_NODE_PATH = the folder holding node_modules/pyodide 0.28.2): interpreter_record_make_v1_1_0.py"""
__version__ = "1.1.0"
import datetime, json, os, subprocess
H = os.path.dirname(os.path.abspath(__file__))
old = json.load(open(os.path.join(H, "interpreter_record_v1_0_0.json")))
r = subprocess.run([os.path.join(H, "pyodide_python_v1_0_0.sh"), "-c", old["program"]], capture_output=True, text=True, timeout=600)
if r.returncode: raise SystemExit("the program failed under Pyodide: " + r.stderr[-400:])
ver = subprocess.run([os.path.join(H, "pyodide_python_v1_0_0.sh"), "--version"], capture_output=True, text=True).stdout.strip()
first = ver.split()[1] + " (Pyodide " + ver.split("Pyodide ")[1].rstrip(")") + ")"
row = "%s | %s" % (first, r.stdout.strip().replace("\n", " / "))
body = lambda s: s.split(" | ", 1)[1].split(" / ", 1)[1].rsplit(" / ", 1)[0]
rows = old["rows"] + [row]
equal = len({body(x) for x in rows}) == 1
json.dump({"_version": __version__, "program": old["program"], "rows": rows, "all_bodies_equal": equal, "pyodide_row": row,
           "_note": old["_note"] + " Version 1.1.0 adds the row of the page's own runtime, %s, run on %s with openpyxl 3.1.5 and every warning an error; the last line of that row is 'older interpreter' because it is not one of the seven 3.14 releases, and the other lines are compared with those of the other rows (bodies equal: %s)." % (first, datetime.date.today().isoformat(), equal)},
          open(os.path.join(H, "interpreter_record_v1_1_0.json"), "w"), indent=1)
print(row); print("all bodies equal:", equal)
