#!/usr/bin/env python3
"""sen0414_lineage_chapter_check v1_0_0 - ONE rerunnable command per story of chapters 7 to 12, for backlog_evidence_bridge to run as the
test of a TestEvidence (the bridge verifies a TestEvidence only if its spec file exists in the workspace and the command exits 0).
It runs the checks that already belong to the chapter and changes nothing in the repository (outputs go to a temporary directory).

Usage: sen0414_lineage_chapter_check_v1_0_0.py KIND/ChNN        e.g. Deck/Ch07, Research/Ch09, Page/Ch12
  Deck      the checks of 08-tooling/chNN-deck/build_v1_0_0.sh that follow the build (structure, deck_check, program_check, layout, fit, notes, and the
            stale fixtures that each must refuse), run against the committed deck under Python 3.14 (the interpreter the examples were recorded under)
  Research  RDODI's own pipeline validator over Stages 1-3 (sen0414_rdodi_gates) and the chapter's execution checks (sen0414_rdodi_checks)
  Page      the browser test of the page (sen0414_page_test, headless Chromium), failing on any FAIL line or failing widget
Exit 0 only when every part passed.
"""
__version__ = "1.0.0"
import glob, os, re, shutil, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "08-tooling")
ECO = os.environ.get("RDODI_ECOSYSTEM", "/home/claude/eco_pin/rdodi-ecosystem")  # the pinned ecosystem the course's own gates ran against (validator 1_6_0 and later)
PY = shutil.which("python3.14") or sys.executable


def newest(pattern):
    fs = glob.glob(pattern)
    return sorted(fs, key=lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()])[-1]


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def deck(n):
    d = os.path.join(TOOL, "ch%02d-deck" % n)
    pptx = glob.glob(os.path.join(d, "sen0414_ch%02d_deck_v1_0_0.pptx" % n)) or glob.glob(os.path.join(REPO, "03-materials", "ch%02d" % n, "SEN0414_Ch%02d_*_3e_v1_0_0.pptx" % n))
    assert len(pptx) == 1, pptx
    lines = open(os.path.join(d, "build_v1_0_0.sh"), encoding="utf-8").read().splitlines()
    i = next(k for k, l in enumerate(lines) if "structure_check" in l)
    body = [l for l in lines[i:] if l.strip() and not l.startswith("#") and "rm -rf" not in l]
    script = "set -euo pipefail\nPY=%s\nOUT=%s\nT=$(mktemp -d)\ncd %s\n%s\n" % (PY, pptx[0], d, "\n".join(body))
    f = tempfile.NamedTemporaryFile("w", suffix=".sh", delete=False); f.write(script); f.close()
    rc, out = run(["bash", f.name]); os.unlink(f.name)
    # every kind of stale fixture the build makes (named in its for-loop or in a line that expects a refusal) must be refused by the check that owns it
    named = set()
    for l in body:
        m = re.match(r"for f in ([\w ]+); do", l)
        if m: named |= set(m.group(1).split())
        for x in re.findall(r"fixture_stale_(\w+?)_v", l): named.add(x)
    refused = set(re.findall(r"^fixture (\w+) refused by", out, re.M))
    print(out[-3000:])
    ok = rc == 0 and bool(named) and named <= refused
    print("deck %02d: exit %d, stale fixture kinds named %s, refused %s" % (n, rc, sorted(named), sorted(refused)))
    return ok


def data_module(n):
    """The newest data module whose own version has its TBox and ABox in the chapter's rdodi folder (a chapter whose data module was
    revised without its ontology files being rebuilt is checked on the version that exists)."""
    rd = os.path.join(REPO, "03-materials", "ch%02d" % n, "rdodi")
    mods = sorted(glob.glob(os.path.join(TOOL, "sen0414_ch%02d_rdodi_data_v*.py" % n)), key=lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()], reverse=True)
    for m in mods:
        v = re.search(r'__version__\s*=\s*"([\d.]+)"', open(m, encoding="utf-8").read())
        v = (v.group(1) if v else "1.0.0").replace(".", "_")
        if all(os.path.exists(os.path.join(rd, "sen0414_ch%02d_%s_v%s.ttl" % (n, k, v))) for k in ("domain_tbox", "domain_abox")):
            return os.path.basename(m)[:-3]
    raise SystemExit("no data module of chapter %d has its ontology files" % n)


def research(n):
    rc1, o1 = run(["python3", os.path.join(TOOL, "sen0414_rdodi_gates_v1_1_1.py"), "%02d" % n, ECO])
    print(o1[-2500:])
    ok = rc1 == 0 and "OVERALL: PASS" in o1
    mod = data_module(n)
    rc2, o2 = run(["python3", os.path.join(TOOL, "sen0414_rdodi_checks_v1_2_0.py"), mod, PY], cwd=TOOL, env=dict(os.environ, PYTHONPATH=TOOL, PYTHONDONTWRITEBYTECODE="1"))
    print(o2[-1500:])
    print("research %02d: gates exit %d (%s); execution checks (%s) exit %d" % (n, rc1, "PASS" if ok else "not PASS", mod, rc2))
    return ok and rc2 == 0


def page(n):
    key = os.environ.get("KEY", "/home/claude/instructor_keys/sen0414_instructor_key_v1_0_0.json")
    if not os.path.exists(key):
        # the page test ends with the mock-exam release, which unlocks with the instructor's private key; without it the test cannot complete
        print("page %02d: the instructor key %s is absent on this machine, so the page test cannot run to its end; nothing is claimed" % (n, key))
        return False
    res = os.path.join(tempfile.mkdtemp(), "results.json")
    rc, out = run(["python3", os.path.join(TOOL, "sen0414_page_test_v9_34_0.py"), "%02d" % n], env=dict(os.environ, PAGE_VER="9_28_0", RESULTS=res, PYTHONDONTWRITEBYTECODE="1"))
    fails = [l for l in out.splitlines() if l.strip().startswith("[FAIL]")]
    m = re.search(r"widgets: (\d+) tested, (\d+) passed", out)
    npass = sum(1 for l in out.splitlines() if l.strip().startswith("[PASS]"))
    print("\n".join(out.splitlines()[-12:]))
    print("page %02d: exit %d, widgets %s, features passed %d, failed %d" % (n, rc, m.groups() if m else None, npass, len(fails)))
    return rc == 0 and m is not None and m.group(1) == m.group(2) and not fails


def main():
    kind, ch = sys.argv[1].split("/")
    n = int(ch[2:])
    ok = {"Deck": deck, "Research": research, "Page": page}[kind](n)
    print("RESULT %s: %s" % (sys.argv[1], "PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
