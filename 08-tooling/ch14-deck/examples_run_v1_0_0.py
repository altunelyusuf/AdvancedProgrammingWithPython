"""Executes every console session, program, chart and table of examples_v1_0_0.py (chapter 14) under the interpreter given and
writes examples_out_v1_0_0.json. A console session runs row by row in one namespace: a row that evaluates records the repr of its
value (nothing for None), one that is a statement records nothing, one that raises records 'Type: message'. A program runs through
progrun_v1_0_0.run_program, so the transcript is what a student sees; its exit code must be 0 or the run is refused. A chart or a
table is the value of its expression after its setup ran; the deck check runs the same pair again.
Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES, PROGRAMS, CHARTS, TABLES
from progrun_v1_0_0 import run_program
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


def sh(code, *args):
    r = subprocess.run([PY, "-c", code, *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("REFUSED: %s" % r.stderr[-400:])
    return r.stdout


out = {"_version": __version__, "_python": sh("import platform;print(platform.python_version())").strip()}
for k, rows in CONSOLES.items():
    out[k] = json.loads(sh(SESSION, json.dumps(rows)))
out["_programs"] = {}
for name, (code, needs, live) in PROGRAMS.items():
    r = run_program(PY, code, (), needs)
    if r.returncode:
        raise SystemExit("REFUSED: program %s exited %d: %s" % (name, r.returncode, r.stderr[-300:]))
    out["_programs"][name] = {"code": code, "inputs": [], "needs": list(needs), "transcript": r.stdout.rstrip("\n"), "live": live, "exit": r.returncode}
    print("  ran %-36s exit %d%s%s" % (name, r.returncode, "  LIVE" if live else "", "  needs " + ",".join(needs) if needs else ""))
out["_charts"], out["_tables"] = {}, {}
for k, c in CHARTS.items():
    pairs = json.loads(sh(DATA, c["setup"], c["expr"]))
    out["_charts"][k] = {"setup": c["setup"], "expr": c["expr"], "labels": [p[0] for p in pairs], "values": [float(p[1]) for p in pairs]}
for k, t in TABLES.items():
    out["_tables"][k] = {"setup": t["setup"], "expr": t["expr"], "rows": json.loads(sh(DATA, t["setup"], t["expr"]))}
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows,",
      len(out["_programs"]), "programs, all exit 0,", len(out["_charts"]), "chart(s),", len(out["_tables"]), "table(s)")
