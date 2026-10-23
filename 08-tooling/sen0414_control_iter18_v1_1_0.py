#!/usr/bin/env python3
"""sen0414_control_iter18 v1_1_0 - the lineage agent's own control checks of the Iter_18 executor results (G136, G137: the controller re-runs, never trusts the executor's log).
Usage: sen0414_control_iter18_v1_1_0.py CHECK      CHECK = template | pagetest | charset | deckcheck | deck06 | deck07 | deck08 | templatefix | runner | regress
v1.1.0 (over 1.0.0, which stays as committed and is imported for its checks): adds templatefix (template 9.52.2 + builder 4.18.1), runner (page-test runner v1_1_0) and regress (the page test 9.34.0 on pages built from 9.52.2).
Live measurements (hashes, comment counts, the builder's guard function run on both templates, the runner's switch) are taken at run time; the page-test runs, which take about 8 minutes each, are read from the
logs the lineage agent kept in 08-tooling/control-iter18-logs/ (run by the lineage agent's own driver or by the runner, with a TEST release key, outside the executors' sessions, serially, one at a time).
Exit 0 only when every assertion holds; the evidence bridge runs this file as the TestEvidence command."""
__version__ = "1.1.0"
import ast, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0414_control_iter18_v1_0_0 as C

REPO, T, LOGS = C.REPO, C.T, C.LOGS
ok, sha, log, off = C.ok, C.sha, C.log, C.off
OLD2 = {"course_page_template_v9_52_1.html": "d8634e55e9e0a0ff9049efbbf800c423fe043a53260dc676d2463fb026738ccf",
        "sen0414_page_build_v4_18_0.py": "ca12152b53a98311662747ce1fe8954a3145187ddb2e760ce53203594d90e3c9",
        "sen0414_page_test_run_v1_0_0.py": "146dd614710cb500c1edb2733ab2518c7b9b3c91b48634d39cae95ab96eba1ae"}


def txt(f):
    return open(os.path.join(T, f), encoding="utf-8").read()


def old2():
    for f, h in OLD2.items():
        ok(sha(os.path.join(T, f)) == h, "%s is byte-identical to the recorded SHA-256 %s" % (f, h[:12]))
    ok(sha(os.path.join(T, "sen0414_page_test_v9_34_0.py")) == C.OLD["sen0414_page_test_v9_34_0.py"], "sen0414_page_test_v9_34_0.py is byte-identical to the recorded SHA-256")


def guard_fn():
    src = txt("sen0414_page_build_v4_18_1.py"); tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_guard")
    ns = {}; exec(compile(ast.Module([fn], []), "guard", "exec"), ns); return ns["_guard"]


def clean_log(name, label, widgets=True):
    t = log(name); fails = [l for l in t.splitlines() if "[FAIL]" in l]
    ok(not fails, "%s: no feature FAILS (%d [FAIL] lines)%s" % (label, len(fails), "" if not fails else ": " + fails[0][:140]))
    ok(re.search(r"^exit 0", t, re.M) is not None, "%s: the test process exited 0" % label)
    if widgets:
        m = re.search(r"widgets: (\d+) tested, (\d+) passed; failing: \[\]", t); ok(bool(m) and m.group(1) == m.group(2), "%s: every widget passes (%s)" % (label, m.group(0) if m else "none"))
    for pat, nm in ((r"\[PASS\] a focused concept starts at the top", "focused concept starts at the top"), (r"\[PASS\] small phone \(360px\)", "small phone 360px")):
        ok(re.search(pat, t) is not None, "%s: %s PASS" % (label, nm))
    return t


def templatefix():
    old_unchanged = C.old_unchanged; old_unchanged(); old2()
    for f in ("course_page_template_v9_52_2.html", "sen0414_page_build_v4_18_1.py"):
        ok(os.path.exists(os.path.join(T, f)), "new file %s exists" % f)
    a, b = txt("course_page_template_v9_52_1.html"), txt("course_page_template_v9_52_2.html")
    ok(a.count("<!--") == 34 and a.count("-->") == 36, "template 9.52.1 (the root cause): %d comment openers against %d closers - a comment closes early and its text shows above the header" % (a.count("<!--"), a.count("-->")))
    ok(b.count("<!--") == b.count("-->") == 34, "template 9.52.2: %d openers, %d closers" % (b.count("<!--"), b.count("-->")))
    o = off(os.path.join(T, "course_page_template_v9_52_2.html")); ok(o is not None and o < 512, "template 9.52.2: first <meta charset> at byte %s (limit: below 512)" % o)
    g = guard_fn()
    try:
        g(a, "the template 9.52.1"); ok(False, "the builder 4.18.1 guard refuses template 9.52.1")
    except SystemExit as e:
        ok("refused" in str(e), "the builder 4.18.1 guard (its own function, run here) refuses template 9.52.1: %s" % str(e)[:110])
    try:
        g(b, "the template 9.52.2"); ok(True, "the builder 4.18.1 guard accepts template 9.52.2")
    except SystemExit as e:
        ok(False, "the builder 4.18.1 guard accepts template 9.52.2: %s" % e)
    for n in ("01", "10"):
        clean_log("r3_t36_ch%s.log" % n, "chapter %s scratch page on 9.52.2, page test 9.36.0" % n)


def runner():
    old2()
    v0, v1 = txt("sen0414_page_test_run_v1_0_0.py"), txt("sen0414_page_test_run_v1_1_0.py")
    ok("sen0414_page_test_v9_34_0.py" in v0 and "9_36_0" not in v0, "runner v1_0_0 (unchanged) still runs only the page test 9.34.0")
    ok('DEFAULT_TEST = "sen0414_page_test_v9_36_0.py"' in v1 or "DEFAULT_TEST" in v1 and "sen0414_page_test_v9_36_0.py" in v1, "runner v1_1_0 runs the page test 9.36.0 by default")
    for env in ("FORCE_STANDARD", "PAGE_FILE", "PAGE_DATA", "PAGE_TEST_FILE"):
        ok(env in v1, "runner v1_1_0 handles the environment variable %s" % env)
    r = subprocess.run([sys.executable, os.path.join(T, "sen0414_page_test_run_v1_1_0.py"), "10", "9_28_0"], capture_output=True, text=True, cwd=REPO, env=dict(os.environ, PAGE_TEST_FILE="nonexistent_x.py"))
    ok("test file not found" in r.stdout and "nonexistent_x.py" in r.stdout and r.returncode != 0, "PAGE_TEST_FILE switches the test file (a missing name is refused naming it, exit %d)" % r.returncode)
    s = log("r3_runner_sh08.log")
    ok(re.search(r"\[FAIL\] P12 .*byte 9293", s) is not None, "runner with FORCE_STANDARD=1 on the shipped chapter 8 page v9_28_0: P12 FAILS naming byte 9293")
    ok(re.search(r"\[FAIL\] P11 ", s) is not None and re.search(r"\[FAIL\] P2 .*chapter-code", s) is not None, "the same run: P11 (no declared standard) and P2 (no chapter-code tab) FAIL")
    ok("RESULT: FAIL" in s and "Traceback" not in s, "the same run ends RESULT: FAIL without a crash (the stored fail verdict)")
    runner_log("r3_runner_scratch10.log", "runner with PAGE_FILE on the scratch chapter 10 page (9.52.2)", "sen0414_page_test_v9_36_0.py")
    runner_log("r3_runner_t34_ch01.log", "runner with PAGE_TEST_FILE=9.34.0 on the scratch chapter 1 page", "sen0414_page_test_v9_34_0.py")


def runner_log(name, label, test):
    t = log(name); m = re.search(r"^page (\d+): exit 0, widgets \('(\d+)', '(\d+)'\), features passed (\d+), failed (\d+),", t, re.M)
    ok(bool(m) and m.group(2) == m.group(3) and m.group(5) == "0", "%s: %s" % (label, m.group(0)[:100] if m else "no result line"))
    ok(("test file: " + test) in t and "page file substituted" in t, "%s: the runner ran %s on the substituted scratch page" % (label, test))
    ok(re.search(r"^RESULT: PASS", t, re.M) is not None, "%s: RESULT: PASS" % label)


def regress():
    old2()
    for n in ("01", "10"):
        runner_log("r3_runner_t34_ch%s.log" % n, "chapter %s scratch page on 9.52.2, old page test 9.34.0 through the runner switch" % n, "sen0414_page_test_v9_34_0.py")
    ok(re.search(r"^page 10: exit 0, widgets \('59', '59'\), features passed \d+, failed 0", log("r3_baseline_t34_shipped10.log"), re.M) is not None, "baseline: the shipped chapter 10 page v9_28_0 (old template) under 9.34.0 in the same setting: failed 0 (the stored result the new template must give)")


def main():
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    extra = {"templatefix": templatefix, "runner": runner, "regress": regress}
    if c in extra:
        extra[c]()
    else:
        {"template": C.template, "pagetest": C.pagetest, "charset": C.charset, "deckcheck": C.deckcheck, "deck06": lambda: C.deck("06"), "deck07": lambda: C.deck("07"), "deck08": lambda: C.deck("08")}[c]()
    print("RESULT %s (%d failed assertion(s))" % ("FAIL" if C.BAD else "PASS", len(C.BAD))); sys.exit(1 if C.BAD else 0)


if __name__ == "__main__":
    main()
