"""Executes every console group and whole program of examples_v2_0_0.py under the interpreter given and writes
examples_out_v2_0_0.json (the schema program_check_v2_0_1.py reads). A console group is run in ONE child process and
namespace, row by row, with the same rule deck_check_v1_0_1.py applies when it re-runs the slide: a row is evaluated
and its repr recorded (an exception as 'Name: message'), or, when it is a statement, executed and recorded with no
output; a value of None shows nothing, as in the interactive prompt. A program is run as a separate process and its
standard output recorded as the transcript. The deck prints nothing that this file did not record.
Usage: examples_run_v2_0_0.py <python> <out.json>"""
__version__ = "2.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v2_0_0 import EX, PROGRAMS
PY, OUT = sys.argv[1], sys.argv[2]
CHILD = r'''
import json, sys
rows, ns, out = json.loads(sys.argv[1]), {}, []
for src in rows:
    try:
        try:
            v = eval(src, ns); got = None if v is None else repr(v)
        except SyntaxError:
            exec(src, ns); got = None
    except Exception as e:
        got = "%s: %s" % (type(e).__name__, e)
    out.append([src, got or ""])
print(json.dumps(out))
'''
out = {"_version": __version__,
       "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()}
for k, rows in EX.items():
    r = subprocess.run([PY, "-c", CHILD, json.dumps(rows)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("group %s failed: %s" % (k, r.stderr[-300:]))
    out[k] = json.loads(r.stdout)
out["_programs"] = {}
for name, (code, runs) in PROGRAMS.items():
    rec = {"code": code, "runs": []}
    for inputs in runs:
        r = subprocess.run([PY, "-c", code], capture_output=True, text=True, input="\n".join(inputs))
        if r.returncode:
            raise SystemExit("program %s failed: %s" % (name, r.stderr[-300:]))
        rec["runs"].append({"inputs": inputs, "transcript": r.stdout.rstrip("\n"), "exit": r.returncode, "stderr": r.stderr.strip()})
    out["_programs"][name] = rec
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", len(EX), "console groups,", sum(len(v) for k, v in out.items() if k in EX), "rows,", len(out["_programs"]), "programs")
