"""Executes every console session, program, chart and table of examples_v1_0_0.py under the interpreter given and writes
examples_out_v1_0_0.json. A console session runs row by row in one namespace: a row that evaluates records the repr of
its value (nothing for None), one that is a statement records nothing, one that raises records 'Type: message'. A
program runs with input() replaced by a function that echoes the typed value on its own line, so the transcript is what a
student sees. Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES, PROGRAMS, CHARTS, TABLES
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
DATA = r'''
import sys, json
ns = {}; exec(sys.argv[1], ns); print(json.dumps(eval(sys.argv[2], ns)))
'''
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print(v)\n    return v\nbuiltins.input = _input\n"


def sh(code, *args, inp=None):
    r = subprocess.run([PY, "-c", code, *args], capture_output=True, text=True, input=inp)
    if r.returncode:
        raise SystemExit("REFUSED: %s" % r.stderr[-400:])
    return r.stdout


out = {"_version": __version__,
       "_python": sh("import platform;print(platform.python_version())").strip()}
for k, rows in CONSOLES.items():
    out[k] = json.loads(sh(SESSION, json.dumps(rows)))
out["_programs"] = {}
for name, (code, stdin) in PROGRAMS.items():
    inputs = stdin.split("\n")[:-1] if stdin is not None else []
    r = subprocess.run([PY, "-c", PRE % inputs + code], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("REFUSED: program %s: %s" % (name, r.stderr[-300:]))
    out["_programs"][name] = {"code": code, "inputs": inputs, "transcript": r.stdout.rstrip("\n")}
out["_charts"] = {}
for k, (setup, expr) in CHARTS.items():
    pairs = json.loads(sh(DATA, setup, expr))
    out["_charts"][k] = {"setup": setup, "expr": expr, "labels": [p[0] for p in pairs], "values": [p[1] for p in pairs]}
out["_tables"] = {}
for k, (setup, expr) in TABLES.items():
    out["_tables"][k] = {"setup": setup, "expr": expr, "rows": json.loads(sh(DATA, setup, expr))}
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows,",
      len(out["_programs"]), "programs,", len(out["_charts"]), "charts,", len(out["_tables"]), "tables")
