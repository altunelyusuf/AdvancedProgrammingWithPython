"""Executes every console session, program, chart and table of examples_v1_0_0.py (chapter 22) under the interpreter given and
writes examples_out_v1_0_0.json. A console session runs row by row in one namespace: a row that evaluates records the repr of its
value (nothing for None), one that is a statement records nothing, one that raises records 'Type: message'. A program runs through
progrun_v1_0_0.run_program, so the transcript is what a student sees; its exit code must be 0 and its transcript must not say NOT EXECUTED
(the programs that fetch the publisher's zip print that and stop when the zip is missing or differs: such a recording is refused; the one line of the corpus program hyphensAndDigits that says the language model step was NOT EXECUTED is the chapter's honest statement and is allowed). The pictures
that programs save with keep() are written to images/ beside this file, and each is listed in the recording with its SHA-256. A chart or a table is the
value of its expression after its setup ran; the deck check runs the same pair again (the table of environments runs four interpreters every time).
Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import hashlib, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES, PROGRAMS, CHARTS, TABLES, KIND, EQUIV, SUBSET, STANDKEY, IMAGES
from progrun_v1_0_0 import run_program
PY, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "images")

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


out = {"_version": __version__, "_python": sh("import platform;print(platform.python_version())").strip(),
       "_packages": sh("import importlib.metadata as m;print('pytesseract', m.version('pytesseract'), '| Pillow', m.version('pillow'), '| NumPy', m.version('numpy'), '| OpenCV', m.version('opencv-python-headless'), '| PyAutoGUI', m.version('pyautogui'))").strip(),
       "_tesseract": subprocess.run(["tesseract", "--version"], capture_output=True, text=True).stdout.splitlines()[0]}
for k, rows in CONSOLES.items():
    out[k] = json.loads(sh(SESSION, json.dumps(rows)))
os.makedirs(IMG, exist_ok=True)
for f in os.listdir(IMG):
    os.remove(os.path.join(IMG, f))
out["_programs"] = {}
for name, (code, needs, live) in PROGRAMS.items():
    r = run_program(PY, code, (), needs, keep=IMG)
    if r.returncode:
        raise SystemExit("REFUSED: program %s exited %d: %s" % (name, r.returncode, (r.stderr or r.stdout)[-400:]))
    bad = [l for l in r.stdout.splitlines() if l.startswith("NOT EXECUTED") and "large language model" not in l]
    if bad:
        raise SystemExit("REFUSED: program %s printed NOT EXECUTED: %s" % (name, bad[0][:300]))
    out["_programs"][name] = {"code": code, "inputs": [], "needs": list(needs), "transcript": r.stdout.rstrip("\n"), "live": live,
                              "kind": KIND[name], "exit": r.returncode, "standkey": list(STANDKEY.get(name, ())), "corpus": name in __import__("examples_v1_0_0").B.PROGRAMS}
    print("  ran %-34s exit %d  %s" % (name, r.returncode, KIND[name]))
out["_images"] = {}
for fn, prog in IMAGES.items():
    p = os.path.join(IMG, fn)
    if not os.path.exists(p):
        raise SystemExit("REFUSED: program %s did not save %s" % (prog, fn))
    b = open(p, "rb").read()
    out["_images"][fn] = {"program": prog, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}
    if hashlib.sha256(b).hexdigest()[:12] not in out["_programs"][prog]["transcript"]:
        raise SystemExit("REFUSED: the transcript of %s does not print the hash of %s" % (prog, fn))
extra = sorted(set(os.listdir(IMG)) - set(IMAGES))
if extra:
    raise SystemExit("REFUSED: pictures saved but not placed: %r" % extra)
out["_charts"], out["_tables"] = {}, {}
for k, c in CHARTS.items():
    pairs = json.loads(sh(DATA, c["setup"], c["expr"], HERE))
    out["_charts"][k] = {"setup": c["setup"], "expr": c["expr"], "labels": [p[0] for p in pairs], "values": [float(p[1]) for p in pairs]}
for k, t in TABLES.items():
    out["_tables"][k] = {"setup": t["setup"], "expr": t["expr"], "rows": json.loads(sh(DATA, t["setup"], t["expr"], HERE))}
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows,",
      len(out["_programs"]), "programs, all exit 0,", len(out["_images"]), "pictures,", len(out["_charts"]), "chart(s),", len(out["_tables"]), "table(s)")
