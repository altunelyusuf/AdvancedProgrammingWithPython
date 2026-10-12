"""Executes every console session of examples_v1_0_0.py (chapter 13) under the interpreter given and writes examples_out_v1_0_0.json,
in the shape the page-data builder reads (the same shape as ch12-deck/examples_out_v1_0_0.json). A session runs row by row in one
namespace: a row that evaluates records the repr of its value (nothing for None), one that is a statement records nothing, one that
raises records 'Type: message'. Usage: examples_run_v1_0_0.py <python> <out.json>   (the interpreter must not have requests,
beautifulsoup4, selenium or playwright installed: the last session records that Selenium is absent)"""
__version__ = "1.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES
PY, OUT = sys.argv[1], sys.argv[2]
SESSION = r'''
import sys, json
rows = json.loads(sys.argv[1]); ns = {}; out = []
for src in rows:
    try:
        try:
            v = eval(src, ns); got = "" if v is None else repr(v)
        except SyntaxError:
            exec(src, ns); got = ""
    except Exception as e:
        got = "%s: %s" % (type(e).__name__, e)
    out.append([src, got])
print(json.dumps(out))
'''
def sh(code, *args):
    r = subprocess.run([PY, "-c", code, *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("REFUSED: %s" % r.stderr[-400:])
    return r.stdout
out = {"_version": __version__, "_python": sh("import platform;print(platform.python_version())").strip()}
for k, rows in CONSOLES.items():
    out[k] = json.loads(sh(SESSION, json.dumps(rows)))
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows")
