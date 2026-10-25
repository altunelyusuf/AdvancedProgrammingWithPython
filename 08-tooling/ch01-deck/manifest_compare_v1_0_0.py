#!/usr/bin/env python3
"""Compares two chapter-code manifests and lists every difference; then runs every example of the second under a given
interpreter and scans the recorded first lines against ^(\\w*Error|Traceback|Stopped after).
Usage: manifest_compare_v1_0_0.py OLD.json NEW.json PYTHON"""
__version__ = "1.0.0"
import json, re, subprocess, sys
old, new = json.load(open(sys.argv[1], encoding="utf-8")), json.load(open(sys.argv[2], encoding="utf-8"))
diffs = []
for k in sorted(set(old) | set(new)):
    if k != "examples" and old.get(k) != new.get(k):
        diffs.append("top-level field %r differs" % k)
oe, ne = old["examples"], new["examples"]
if len(oe) != len(ne):
    diffs.append("example count %d vs %d" % (len(oe), len(ne)))
for a, b in zip(oe, ne):
    for k in sorted(set(a) | set(b)):
        if a.get(k) != b.get(k):
            diffs.append("example %d (%s): field %r differs" % (a["order"], a["name"], k))
print("top-level and example differences:")
for d in diffs:
    print("  ", d)
changed = sorted({d.split(":")[0] for d in diffs if d.startswith("example")})
print("examples with differences:", changed)
bad = 0
pat = re.compile(r"^(\w*Error|Traceback|Stopped after)")
for e in ne:
    r = subprocess.run([sys.argv[3], "-I", "-c", e["code"]], capture_output=True, text=True, timeout=60)
    ok = r.returncode == 0 and r.stdout == e["expected"]
    first = e["expected"].split("\n", 1)[0].strip()
    err = bool(pat.match(first))
    print("example %2d %-28s run=%s first-line-error=%s" % (e["order"], e["name"], "PASS" if ok else "FAIL", "YES" if err else "no"))
    bad += (not ok) + err
print("FAIL" if bad else "PASS: every example printed its recorded result under " + sys.argv[3] + "; no recorded first line matches the error pattern")
sys.exit(1 if bad else 0)
