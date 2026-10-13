"""Executes every console session, program, chart and table of examples_v1_0_0.py (chapter 19) under the interpreter given and
writes examples_out_v1_0_0.json. A console session runs row by row in one namespace: a row that evaluates records the repr of its
value (nothing for None), one that is a statement records nothing, one that raises records 'Type: message'. A program runs through
progrun_v1_0_0.run_program, so the transcript is what a student sees; its exit code must be 0 or the run is refused. A chart or a
table is the value of its expression after its setup ran; the deck check runs the same pair again. Two more runs are recorded under
the other environments of the research: the bare environment (the standard library only: no schedule package and no tzdata package) and the
environment holding the versions Appendix A of the book pins (playsound3 2.4.0); the deck's cards quote what they printed.
Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES, PROGRAMS, CHARTS, TABLES, KIND, EQUIV, SUBSET, EMUKEY, BARE_CODE, PINS_CODE
from progrun_v1_0_0 import run_program
PY, OUT = sys.argv[1], sys.argv[2]
BARE = os.environ.get("CH19_BARE", "/home/claude/venv314_ch19_bare/bin/python")
PINS = os.environ.get("CH19_PINS", "/home/claude/venv314_ch19_pins/bin/python")

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
ns = {"HERE": sys.argv[3]}; exec(sys.argv[1], ns); print(json.dumps(eval(sys.argv[2], ns)))
'''


def sh(code, *args):
    r = subprocess.run([PY, "-W", "ignore", "-c", code, *args], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("REFUSED: %s" % r.stderr[-400:])
    return r.stdout


def subsequence(small, big):
    it = iter(big)
    return all(any(x == y for y in it) for x in small)


out = {"_version": __version__, "_python": sh("import platform;print(platform.python_version())").strip(),
       "_packages": sh("import importlib.metadata as m;"
                       "print('schedule', m.version('schedule'), '| tzdata', m.version('tzdata'), '| pyperclip', m.version('pyperclip'),"
                       " '| playsound3', m.version('playsound3'))").strip()}
for k, rows in CONSOLES.items():
    out[k] = json.loads(sh(SESSION, json.dumps(rows)))
out["_programs"] = {}
for name, (code, needs, live) in PROGRAMS.items():
    r = run_program(PY, code, (), needs)
    if r.returncode:
        raise SystemExit("REFUSED: program %s exited %d: %s" % (name, r.returncode, r.stderr[-300:]))
    out["_programs"][name] = {"code": code, "inputs": [], "needs": list(needs), "transcript": r.stdout.rstrip("\n"), "live": live,
                              "kind": KIND[name], "exit": r.returncode, "livekey": [], "emukey": list(EMUKEY.get(name, ()))}
    print("  ran %-42s exit %d  %s" % (name, r.returncode, KIND[name]))
for copy, orig in EQUIV.items():
    if out["_programs"][copy]["transcript"] != out["_programs"][orig]["transcript"]:
        raise SystemExit("REFUSED: %s does not print what %s prints" % (copy, orig))
    print("  %s prints exactly what %s prints" % (copy, orig))
for copy, orig in SUBSET.items():
    small = out["_programs"][copy]["transcript"].split("\n"); big = out["_programs"][orig]["transcript"].split("\n")
    if not subsequence(small, big):
        raise SystemExit("REFUSED: %s prints a line that %s does not print, in that order" % (copy, orig))
    print("  every line %s prints is a line %s prints, in the same order (%d of %d)" % (copy, orig, len(small), len(big)))
out["_charts"], out["_tables"] = {}, {}
for k, c in CHARTS.items():
    pairs = json.loads(sh(DATA, c["setup"], c["expr"], os.path.dirname(os.path.abspath(__file__))))
    out["_charts"][k] = {"setup": c["setup"], "expr": c["expr"], "labels": [p[0] for p in pairs], "values": [float(p[1]) for p in pairs]}
for k, t in TABLES.items():
    out["_tables"][k] = {"setup": t["setup"], "expr": t["expr"], "rows": json.loads(sh(DATA, t["setup"], t["expr"], os.path.dirname(os.path.abspath(__file__))))}


def other(py, code, label):
    r = subprocess.run([py, "-W", "ignore", "-c", code], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit("REFUSED: the %s environment run failed: %s" % (label, r.stderr[-300:]))
    ver = subprocess.run([py, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip()
    pk = subprocess.run(["uv", "pip", "list", "--python", py, "--format=freeze"], capture_output=True, text=True).stdout.split()
    return {"python": ver, "packages": pk, "code": code, "transcript": r.stdout.rstrip("\n")}


# the other environments of the research
out["_bare"] = other(BARE, BARE_CODE, "bare")
if "ModuleNotFoundError" not in out["_bare"]["transcript"]:
    raise SystemExit("REFUSED: the bare environment imported a third-party package the research says it lacks")
out["_pins"] = other(PINS, PINS_CODE, "pins")
if "playsound3 2.4.0" not in out["_pins"]["transcript"]:
    raise SystemExit("REFUSED: the pins environment does not hold playsound3 2.4.0")
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows,",
      len(out["_programs"]), "programs, all exit 0,", len(out["_charts"]), "chart(s),", len(out["_tables"]), "table(s); bare:",
      out["_bare"]["transcript"].replace("\n", " / "), "; pins:", out["_pins"]["transcript"].replace("\n", " / ")[:240])
