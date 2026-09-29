"""Executes every expression and program of examples_v1_1_0.py under the interpreter given and writes
examples_out_v1_1_0.json. A program is run with input() replaced by a function that echoes the prompt and the typed
value, so the transcript is exactly what a student sees. Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.1.0"
import json, subprocess, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from examples_v1_1_0 import EX, PROGRAMS
PY, OUT = sys.argv[1], sys.argv[2]
def ev(e):
    r = subprocess.run([PY, "-c", "import sys\ntry:\n    print(repr(eval(sys.argv[1])))\nexcept Exception as e:\n    print('%s: %s' % (type(e).__name__, e))", e], capture_output=True, text=True)
    return r.stdout.strip()
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print('\\x01' + prompt + '\\x02' + v + '\\x03')\n    return v\nbuiltins.input = _input\n"
out = {"_version": __version__, "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()}
for k, exprs in EX.items(): out[k] = [[e, ev(e)] for e in exprs]
out["_programs"] = {}
for name, (code, runs) in PROGRAMS.items():
    rec = {"code": code, "runs": []}
    for inputs in runs:
        r = subprocess.run([PY, "-c", PRE % inputs + code], capture_output=True, text=True)
        raw = r.stdout.rstrip("\n"); plain = raw.replace("\x01", "").replace("\x02", "").replace("\x03", "")
        lines = []
        for ln in raw.split("\n"):
            if "\x01" in ln:
                pr, rest = ln.replace("\x01", "").split("\x02", 1); lines.append([[pr, False], [rest.replace("\x03", ""), True]])
            else: lines.append([[ln, False]])
        rec["runs"].append({"inputs": inputs, "transcript": plain, "lines": lines, "exit": r.returncode, "stderr": r.stderr.strip()})
    out["_programs"][name] = rec
json.dump(out, open(OUT, "w"), indent=1); print("written", OUT, "under Python", out["_python"])
