"""Executes every expression and program of examples_v1_1_0.py under the interpreter given and writes
examples_out_v1_1_0.json. An expression is run in a fresh child process and its repr recorded; a program is run with
input() replaced by a function that echoes the prompt and the typed value, so the transcript is exactly what a
student sees. The deck prints nothing that this file did not record.
Usage: examples_run_v1_1_0.py <python> <out.json>"""
__version__ = "1.1.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_1_0 import EX, PROGRAMS, LEAF_PROGRAM, CONCEPT_EX
PY, OUT = sys.argv[1], sys.argv[2]


def ev(e):
    r = subprocess.run([PY, "-c", "import sys\ntry:\n    print(repr(eval(sys.argv[1])))\nexcept Exception as e:\n    print('%s: %s' % (type(e).__name__, e))", e],
                       capture_output=True, text=True)
    return r.stdout.strip()


PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print('\\x01' + prompt + '\\x02' + v + '\\x03')\n    return v\nbuiltins.input = _input\n"
out = {"_version": __version__,
       "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()}
for k, exprs in EX.items():
    if k.startswith("_"):
        out[k] = exprs
        continue
    out[k] = [[e, ev(e)] for e in exprs]
out["_concepts"] = {cid: [expr, ev(expr)] for cid, expr in sorted(CONCEPT_EX.items())}
out["_leaf_program"] = LEAF_PROGRAM
out["_programs"] = {}
for name, (code, runs) in PROGRAMS.items():
    rec = {"code": code, "runs": []}
    for inputs in runs:
        r = subprocess.run([PY, "-c", PRE % inputs + code], capture_output=True, text=True)
        raw = r.stdout.rstrip("\n")
        plain = raw.replace("\x01", "").replace("\x02", "").replace("\x03", "")
        lines = []
        for ln in raw.split("\n"):
            if "\x01" in ln:
                pr, rest = ln.replace("\x01", "").split("\x02", 1)
                lines.append([[pr, False], [rest.replace("\x03", ""), True]])
            else:
                lines.append([[ln, False]])
        rec["runs"].append({"inputs": inputs, "transcript": plain, "lines": lines, "exit": r.returncode, "stderr": r.stderr.strip()})
    out["_programs"][name] = rec
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", len(out["_concepts"]), "concept examples,", len(out["_programs"]), "programs")
