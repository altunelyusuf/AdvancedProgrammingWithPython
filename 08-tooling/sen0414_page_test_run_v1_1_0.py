#!/usr/bin/env python3
"""sen0414_page_test_run v1_1_0 - runs the page test 9.36.0 on a chapter page against a key-substituted copy (new file over v1_0_0, which stays unchanged).
By default it runs sen0414_page_test_v9_36_0.py; the environment PAGE_TEST_FILE names another test file (a file name in this folder, or a path),
for example sen0414_page_test_v9_34_0.py. The interface of v1_0_0 is kept: NN and PAGEVER, the key-substituted copy of the page (sen0414_page_key_substitute_v1_0_0.py),
the TEST key, everything written outside the repository, exit 0 only when the test exits 0, every widget passes and no [FAIL] line is printed.

Environment:
  FORCE_STANDARD=1   passed through to the test (applies the page-standard features P1-P12 to any page)
  PAGE_FILE=path     a built page outside the repository; it is key-substituted in a temporary copy (the repository page of NN/PAGEVER is not used)
  PAGE_DATA=path     the chapter's page data (page_data_vPAGEVER.json) for a page that is not in the repository. The test reads it from
                     08-tooling/chNN-page/page_data_vPAGEVER.json under its own repository root; to leave nothing in the repository the runner
                     makes a temporary MIRROR root outside it (symbolic links to every repository entry, the chNN-page folder re-made with
                     links to its files plus the supplied data file) and runs a link to the test file inside the mirror. Without PAGE_DATA the
                     repository's own page data file is read in place.
  PAGE_TEST_FILE     the test file to run (default sen0414_page_test_v9_36_0.py)

Usage: sen0414_page_test_run_v1_1_0.py NN [PAGEVER]        (PAGEVER default 9_28_0)
The pass proves the page's logic; the release step ran with a TEST key, not the instructor's.
"""
__version__ = "1.1.0"
import os, re, shutil, subprocess, sys, tempfile

TOOL = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TOOL)
PY = "/home/claude/venv314/bin/python" if os.path.exists("/home/claude/venv314/bin/python") else sys.executable
DEFAULT_TEST = "sen0414_page_test_v9_36_0.py"


def substitute_file(src, dst):
    """key-substitute an arbitrary page file (same placeholder and TEST key as sen0414_page_key_substitute_v1_0_0.py); returns the key file content"""
    sys.path.insert(0, TOOL)
    import importlib.util, json
    from cryptography.hazmat.primitives.asymmetric import ec
    spec = importlib.util.spec_from_file_location("ks", os.path.join(TOOL, "sen0414_page_key_substitute_v1_0_0.py")); ks = importlib.util.module_from_spec(spec); spec.loader.exec_module(ks)
    key = ec.generate_private_key(ec.SECP256R1()); num = key.private_numbers(); pub = num.public_numbers
    jwk = {"kty": "EC", "crv": "P-256", "d": ks.b64u(num.private_value.to_bytes(32, "big")), "x": ks.b64u(pub.x.to_bytes(32, "big")), "y": ks.b64u(pub.y.to_bytes(32, "big"))}
    s = open(src, encoding="utf-8", newline="").read(); a, b = ks.PLACEHOLDER
    if not (a in s and b in s): raise SystemExit("RESULT: FAIL (the page does not carry the placeholder public key)")
    open(dst, "w", encoding="utf-8", newline="").write(s.replace(a, jwk["x"]).replace(b, jwk["y"]))
    return {"private_jwk": jwk, "note": "TEST-ONLY key made by sen0414_page_test_run v1_1_0; not the instructor's"}


def mirror(d, n, pv, data, test):
    """temporary root outside the repository: links to everything, chNN-page re-made with the supplied page data; returns the linked test path"""
    root = os.path.join(d, "root"); tool = os.path.join(root, "08-tooling"); os.makedirs(tool)
    for e in os.listdir(REPO):
        if e != "08-tooling": os.symlink(os.path.join(REPO, e), os.path.join(root, e))
    cp = "ch%s-page" % n
    for e in os.listdir(TOOL):
        if e != cp: os.symlink(os.path.join(TOOL, e), os.path.join(tool, e))
    pd = os.path.join(tool, cp); os.makedirs(pd)
    src = os.path.join(TOOL, cp)
    if os.path.isdir(src):
        for e in os.listdir(src): os.symlink(os.path.join(src, e), os.path.join(pd, e))
    tgt = os.path.join(pd, "page_data_v%s.json" % pv)
    if os.path.lexists(tgt): os.unlink(tgt)
    os.symlink(os.path.abspath(data), tgt)
    link = os.path.join(tool, os.path.basename(test)); 
    if not os.path.lexists(link): os.symlink(test, link)
    return root, link


def main():
    n = sys.argv[1]; pv = sys.argv[2] if len(sys.argv) > 2 else "9_28_0"
    tf = os.environ.get("PAGE_TEST_FILE", DEFAULT_TEST)
    test = tf if os.path.isabs(tf) else os.path.join(TOOL, tf)
    if not os.path.isfile(test): print("RESULT: FAIL (test file not found: %s)" % test); sys.exit(1)
    page_file, page_data = os.environ.get("PAGE_FILE"), os.environ.get("PAGE_DATA")
    if page_file and os.path.realpath(page_file).startswith(REPO + os.sep): print("RESULT: FAIL (PAGE_FILE must lie outside the repository)"); sys.exit(1)
    d = tempfile.mkdtemp(prefix="page_test_")
    import json
    if page_file:
        key = substitute_file(page_file, os.path.join(d, "page.html")); json.dump(key, open(os.path.join(d, "test_key.json"), "w")); print("page file substituted:", page_file)
    else:
        r = subprocess.run([sys.executable, os.path.join(TOOL, "sen0414_page_key_substitute_v1_0_0.py"), n, pv, d], capture_output=True, text=True)
        print(r.stdout + r.stderr)
        if r.returncode: print("RESULT: FAIL (key substitution)"); sys.exit(1)
    run_test, cwd = test, REPO
    if page_data:
        if not os.path.isfile(page_data): print("RESULT: FAIL (PAGE_DATA not found)"); sys.exit(1)
        cwd, run_test = mirror(d, n, pv, page_data, test)
    env = dict(os.environ, PAGE=os.path.join(d, "page.html"), RESULTS=os.path.join(d, "results.json"), PAGE_VER=pv, KEY=os.path.join(d, "test_key.json"), PYTHONDONTWRITEBYTECODE="1")
    print("test file:", os.path.basename(test), "| FORCE_STANDARD=%s" % os.environ.get("FORCE_STANDARD", ""), "| page data:", page_data or "repository")
    r = subprocess.run([PY, run_test, n], capture_output=True, text=True, env=env, cwd=cwd)
    out = r.stdout + r.stderr
    open(os.path.join(d, "test_output.log"), "w").write(out)
    fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
    m = re.search(r"widgets: (\d+) tested, (\d+) passed", out)
    pf = [l for l in out.splitlines() if re.match(r"\s*\[(PASS|FAIL|SKIP)\] P\d+ ", l)]
    print("\n".join(out.splitlines()[-12:]))
    print("P features printed: %d" % len(pf)); print("\n".join(l[:160] for l in pf))
    ok = r.returncode == 0 and m is not None and m.group(1) == m.group(2) and not fails
    print("page %s: exit %d, widgets %s, features passed %d, failed %d, release step with a TEST key; temporary folder %s" % (n, r.returncode, m.groups() if m else None, npass, len(fails), d))
    print("RESULT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
