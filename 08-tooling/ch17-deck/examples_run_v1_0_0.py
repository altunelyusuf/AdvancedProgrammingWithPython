"""Executes every console session, program, chart and table of examples_v1_0_0.py (chapter 17) under the interpreter given and
writes examples_out_v1_0_0.json. A console session runs row by row in one namespace: a row that evaluates records the repr of its
value (nothing for None), one that is a statement records nothing, one that raises records 'Type: message'. A program runs through
progrun_v1_0_0.run_program, so the transcript is what a student sees; its exit code must be 0 or the run is refused. A chart or a
table is the value of its expression after its setup ran; the deck check runs the same pair again. Two more runs are recorded under
other environments of the research: the bare environment (pypdf alone, no Pillow and no cryptography) and the environment holding the
package docx 0.2.4 that the chapter says not to install; the deck's cards quote what they printed.
Usage: examples_run_v1_0_0.py <python> <out.json>"""
__version__ = "1.0.0"
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from examples_v1_0_0 import CONSOLES, PROGRAMS, CHARTS, TABLES, KIND, EQUIV, SUBSET, LIVEKEY, BARE_CODE, BARE_MAKE, DOCX02_CODE
from progrun_v1_0_0 import run_program
PY, OUT = sys.argv[1], sys.argv[2]
BARE = os.environ.get("CH17_BARE", "/home/claude/venv314_ch17_bare/bin/python")
DOCX02 = os.environ.get("CH17_DOCX02", "/home/claude/venv314_ch17_docx02/bin/python")

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
       "_packages": sh("import pypdf, docx, pdfminer, PIL, cryptography, importlib.metadata as m;"
                       "print('pypdf', pypdf.__version__, '| python-docx', docx.__version__, '| pdfminer.six', m.version('pdfminer.six'),"
                       " '| Pillow', PIL.__version__, '| cryptography', cryptography.__version__)").strip()}
for k, rows in CONSOLES.items():
    out[k] = json.loads(sh(SESSION, json.dumps(rows)))
out["_programs"] = {}
for name, (code, needs, live) in PROGRAMS.items():
    r = run_program(PY, code, (), needs)
    if r.returncode:
        raise SystemExit("REFUSED: program %s exited %d: %s" % (name, r.returncode, r.stderr[-300:]))
    out["_programs"][name] = {"code": code, "inputs": [], "needs": list(needs), "transcript": r.stdout.rstrip("\n"), "live": live,
                              "kind": KIND[name], "exit": r.returncode, "livekey": list(LIVEKEY.get(name, ()))}
    print("  ran %-42s exit %d%s  %s" % (name, r.returncode, "  LIVE" if live else "", "  " + KIND[name]))
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
# the other environments of the research
import tempfile
_scan = os.path.join(tempfile.mkdtemp(), "scan.pdf")
sh(BARE_MAKE, _scan)                                # a one-image PDF made with Pillow under the interpreter of the build
r = subprocess.run([BARE, "-W", "ignore", "-c", BARE_CODE, _scan], capture_output=True, text=True)
if r.returncode:
    raise SystemExit("REFUSED: the bare environment run failed: %s" % r.stderr[-300:])
out["_bare"] = {"python": subprocess.run([BARE, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip(),
                "packages": subprocess.run(["uv", "pip", "list", "--python", BARE, "--format=freeze"], capture_output=True, text=True).stdout.split(),
                "code": BARE_CODE, "transcript": r.stdout.rstrip("\n")}
r = subprocess.run([DOCX02, "-c", DOCX02_CODE], capture_output=True, text=True)
if r.returncode == 0:
    raise SystemExit("REFUSED: import docx succeeded in the environment of the package docx 0.2.4, the research says it fails")
out["_docx02"] = {"python": subprocess.run([DOCX02, "-c", "import platform;print(platform.python_version())"], capture_output=True, text=True).stdout.strip(),
                  "last_line": r.stderr.strip().split("\n")[-1],
                  "package": subprocess.run(["uv", "pip", "list", "--python", DOCX02, "--format=freeze"], capture_output=True, text=True).stdout.split()}
json.dump(out, open(OUT, "w"), indent=1)
print("written", OUT, "under Python", out["_python"], "-", sum(len(v) for k, v in out.items() if k in CONSOLES), "console rows,",
      len(out["_programs"]), "programs, all exit 0,", len(out["_charts"]), "chart(s),", len(out["_tables"]), "table(s); bare:",
      out["_bare"]["transcript"].replace("\n", " / "), "; docx 0.2.4:", out["_docx02"]["last_line"])
