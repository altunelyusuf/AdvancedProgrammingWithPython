#!/usr/bin/env python3
"""Compares chapter-code manifests 1.0.0 and 1.1.0 of chapter 3, lists every difference; scans first lines of recorded results;
runs every example of the new manifest under a given python and compares with the recorded result.
Usage: manifest_compare_v5_1_0.py OLD.json NEW.json PYTHON"""
__version__ = "5.1.0"
import json, re, subprocess, sys
old, new = (json.load(open(p, encoding="utf-8")) for p in sys.argv[1:3])
py = sys.argv[3]
diffs = []
for k in sorted(set(old) | set(new)):
    if k != "examples" and old.get(k) != new.get(k):
        diffs.append("top-level %s: %r -> %r" % (k, str(old.get(k))[:70], str(new.get(k))[:70]))
oe, ne = old["examples"], new["examples"]
if len(oe) != len(ne):
    diffs.append("example count %d -> %d" % (len(oe), len(ne)))
for a, b in zip(oe, ne):
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            diffs.append("example %s (%s) field %s differs" % (a["order"], a["name"], k))
print("DIFFERENCES (%d):" % len(diffs))
for d in diffs:
    print(" ", d)
pat = re.compile(r"^(\w*Error|Traceback|Stopped after)")
bad = [e["name"] for e in ne if pat.match(e["expected"].split("\n")[0])]
print("first-line scan ^(\\w*Error|Traceback|Stopped after): %d matches %s" % (len(bad), bad))
fails = 0
for e in ne:
    r = subprocess.run([py, "-I", "-c", e["code"]], capture_output=True, text=True, timeout=60)
    ok = r.returncode == 0 and r.stdout == e["expected"]
    fails += not ok
    print("run %2d %-45s %s" % (e["order"], e["name"], "OK" if ok else "MISMATCH %r" % r.stdout[:80]))
print("RUNS: %d of %d printed the recorded result" % (len(ne) - fails, len(ne)))
