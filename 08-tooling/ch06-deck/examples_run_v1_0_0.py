"""Executes every session and program of examples_v1_0_0.py under the interpreter given and writes examples_out_v1_0_0.json. A session is run the way the
deck check re-runs it: one namespace, each line evaluated (a statement executed, an exception written as 'Name: message'). A program is run with input()
replaced by a function that echoes the prompt and the typed value, so the transcript is exactly what a student sees.
Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import json, subprocess, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from examples_v1_0_0 import EX, PROGRAMS
PY, OUT = sys.argv[1], sys.argv[2]
SESSION = """import contextlib, io, json, sys
ns = {}; out = []
for src in json.loads(sys.argv[1]):
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            try: got = repr(eval(src, ns))
            except SyntaxError: exec(src, ns); got = None
        if got == 'None':                      # the way a console shows it: a value None prints nothing; a print() of it prints the word
            got = None if not buf.getvalue() else buf.getvalue().rstrip('\\n')
            assert got in (None, 'None'), ('a session line printed something other than the value', src, got)
    except Exception as e: got = '%s: %s' % (type(e).__name__, e)
    out.append([src, got])
print(json.dumps(out))
"""
PRE = "import builtins\n_q = iter(%r)\ndef _input(prompt=''):\n    v = next(_q)\n    print('\\x01' + prompt + '\\x02' + v + '\\x03')\n    return v\nbuiltins.input = _input\n"
out = {"_version": __version__, "_python": subprocess.run([PY, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()}
for k, lines in EX.items():
    r = subprocess.run([PY, "-c", SESSION, json.dumps(lines)], capture_output=True, text=True); assert r.returncode == 0, r.stderr
    out[k] = json.loads(r.stdout)
    assert out[k][-1][1] is not None, ("a session must end with an expression", k)
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
        assert r.returncode == 0, (name, r.stderr)
    out["_programs"][name] = rec
json.dump(out, open(OUT, "w"), indent=1, ensure_ascii=False); print("written", OUT, "under Python", out["_python"])
