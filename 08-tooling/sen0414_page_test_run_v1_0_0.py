#!/usr/bin/env python3
"""sen0414_page_test_run v1_0_0 - runs the page test 9.34.0 on a chapter page against a key-substituted copy (see sen0414_page_key_substitute).
Everything it writes goes to a temporary directory outside the repository. Prints the test's tail and one summary line.
Exit 0 only when the test exits 0, reports every widget passed, and prints no [FAIL] line.
The pass proves the page's logic; the release step ran with a TEST key, not the instructor's.

Usage: sen0414_page_test_run_v1_0_0.py NN [PAGEVER]        (PAGEVER default 9_28_0, the version the course repository carries for chapters 7-12)
"""
__version__ = "1.0.0"
import os, re, subprocess, sys, tempfile

TOOL = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOL)
PY = "/home/claude/venv314/bin/python" if os.path.exists("/home/claude/venv314/bin/python") else sys.executable


def main():
    n = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else "9_28_0"
    d = tempfile.mkdtemp(prefix="page_test_")
    r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0414_page_key_substitute_v1_0_0.py"), n, pv, d], capture_output=True, text=True)
    print(r.stdout + r.stderr)
    if r.returncode: print("RESULT: FAIL (key substitution)"); sys.exit(1)
    env = dict(os.environ, PAGE=os.path.join(d, "page.html"), RESULTS=os.path.join(d, "results.json"), PAGE_VER=pv, KEY=os.path.join(d, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, os.path.join(TOOL, "sen0414_page_test_v9_34_0.py"), n], capture_output=True, text=True, env=env, cwd=REPO)
    out = r.stdout + r.stderr
    fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
    m = re.search(r"widgets: (\d+) tested, (\d+) passed", out)
    print("\n".join(out.splitlines()[-12:]))
    ok = r.returncode == 0 and m is not None and m.group(1) == m.group(2) and not fails
    print("page %s: exit %d, widgets %s, features passed %d, failed %d, release step with a TEST key" % (n, r.returncode, m.groups() if m else None, npass, len(fails)))
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
