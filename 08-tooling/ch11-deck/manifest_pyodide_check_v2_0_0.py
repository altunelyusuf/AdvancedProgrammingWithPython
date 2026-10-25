#!/usr/bin/env python3
"""BUILDER'S OWN CHECK of the page runtime (not the independent page test): runs every example of the chapter 11 chapter-code manifest, in manifest order and in ONE interpreter, under Pyodide 0.28.2
(the Python of the page template 9.52.2) with the page's own _run function (pyodide_probe_v2_0_0.js), and compares each output, white space normalised, with the manifest's expected result.
Needs node and the npm package pyodide@0.28.2 (NODE_PATH). Usage: manifest_pyodide_check_v2_0_0.py MANIFEST.json NODE_PATH_DIR WORK_DIR
Prints one line per example and PASS or FAIL; exit 0 only on PASS."""
__version__ = "2.0.0"
import json, os, subprocess, sys
man = json.load(open(sys.argv[1], encoding="utf-8")); here = os.path.dirname(os.path.abspath(__file__)); work = sys.argv[3]
os.makedirs(work, exist_ok=True)
codes = os.path.join(work, "codes.json"); outp = os.path.join(work, "pyodide_out.json")
json.dump({"codes": [[e["name"], e["code"]] for e in man["examples"]]}, open(codes, "w"))
r = subprocess.run(["node", os.path.join(here, "pyodide_probe_v2_0_0.js"), codes, outp], env=dict(os.environ, NODE_PATH=sys.argv[2]), capture_output=True, text=True, timeout=600)
if r.returncode:
    print("CANNOT_RUN", r.stderr[-300:]); sys.exit(2)
res = json.load(open(outp)); bad = 0
norm = lambda t: " ".join(t.split())
for e in man["examples"]:
    got = res["out"][e["name"]]; ok = norm(got) == norm(e["expected"])
    bad += not ok
    print("%s %2d %s" % ("PASS" if ok else "FAIL", e["order"], e["name"]))
    if not ok:
        print("   page:", repr(got[:300])); print("   manifest:", repr(e["expected"][:300]))
print("Pyodide %s | %d examples | %s" % (res["python"], len(man["examples"]), "FAIL" if bad else "PASS"))
sys.exit(1 if bad else 0)
