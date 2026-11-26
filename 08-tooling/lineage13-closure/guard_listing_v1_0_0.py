#!/usr/bin/env python3
"""Lineage13 guard listing (2026-11-26), story ST13_Guards: lists the files changed by the lineage's commits since the objective stage (git diff --name-status from the objective-stage commit eb2d646 to HEAD) and sorts them against the allowed folders
(03-materials/ch16..ch20 except existing rdodi files, 08-tooling, 07-lineage) and the guarded areas (exam work, chapters 1 to 15 and 21 to 25, lab materials, existing rdodi files). Prints counts and the files outside the allowed folders; exit 0 when no guarded file and no outside file changed. Usage: guard_listing_v1_0_0.py"""
__version__ = "1.0.0"
import re, subprocess, sys
BASE = "eb2d646"
out = subprocess.run(["git", "diff", "--name-status", BASE, "HEAD"], capture_output=True, text=True, check=True).stdout.splitlines()
rows = [l.split("\t") for l in out if l.strip()]
files = [(r[0], r[-1]) for r in rows]
def allowed(p):
    if p.startswith("08-tooling/") or p.startswith("07-lineage/"): return True
    m = re.match(r"03-materials/ch(\d\d)/", p)
    return bool(m and 16 <= int(m.group(1)) <= 20)
outside = [(s, p) for s, p in files if not allowed(p)]
early = [(s, p) for s, p in files if re.match(r"03-materials/ch(0[1-9]|1[0-5]|2[1-5])/", p)]
exam = [(s, p) for s, p in files if re.search(r"(^|/)(04-assessment|05-projects)/", p) or (re.search(r"exam", p, re.I) and not re.search(r"/examples_|examples_out|examples_v|examples_run|chapter_code", p, re.I))]
lab = [(s, p) for s, p in files if re.search(r"lab[_-]?(lib|session|handout)", p, re.I)]
rd = [(s, p) for s, p in files if "/rdodi/" in p]
rd_old = [(s, p) for s, p in rd if s[0] != "A"]
print("Guard listing, Lineage13 (2026-11-26): git diff --name-status from the objective-stage commit %s to HEAD (%s)" % (BASE, subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()))
print("Files changed in all: %d (added %d, modified %d, deleted %d, renamed %d)" % (len(files), *(sum(1 for s, _ in files if s[0] == c) for c in "AMDR")))
print("Files outside the allowed folders (03-materials/ch16..ch20, 08-tooling, 07-lineage): %d" % len(outside))
for s, p in outside: print("  %s\t%s" % (s, p))
print("Files of chapters 1 to 15 and 21 to 25 changed: %d" % len(early))
print("Exam or mock-exam files changed: %d (04-assessment, 05-projects, any file named exam; the files named examples_* are example code and are not counted)" % len(exam))
for s, p in exam: print("  %s\t%s" % (s, p))
print("Lab library, session or handout files changed: %d" % len(lab))
print("Files under rdodi folders changed: %d, of which existing files modified, renamed or deleted: %d" % (len(rd), len(rd_old)))
for s, p in rd: print("  %s\t%s" % (s, p))
guard = len(outside) + len(early) + len(exam) + len(lab) + len(rd_old)
print("Guarded files or files outside the allowed folders: %d" % guard)
sys.exit(0 if guard == 0 else 1)
