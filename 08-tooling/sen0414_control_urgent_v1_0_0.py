#!/usr/bin/env python3
"""sen0414_control_urgent v1_0_0 - the lineage agent's control verdicts of the urgent Chapter 8 box, run by the evidence bridge as a test command (exit 0 = the controlled facts hold).
It RUNS the quick checks itself (deck) and READS the kept logs of the long page runs (a page run takes 9 minutes under the page-test lock; the log is the witness, and each log is kept).
Usage: sen0414_control_urgent_v1_0_0.py deckcheck | deck | page | ctl91
  deckcheck  the new deck standard check v1_1_0: --selftest exits 0 with 0 mismatches; the check on the Chapter 8 deck v2.1.0 prints SUMMARY PASS=13 FAIL=0 NOT_MEASURED=0; the mutation probes of the controller (kept log) show each
             broken copy failing in the expected element (D5, D2, D12, M1)
  deck       the controller's own deck checks C1-C8 exit 0 on the deck and its manifest, plus deckcheck
  page       page v9_92_1: five direct runs of page test 9.37.0 each 'RESULT: PASS' with 'failed 0'; the controller's run of page test 9.38.0 PASS; the leak probe seeds 1-5 PASS; the Playground width probe PASS at 1366, 1400 and 390;
             the story-layout probe PASS
  ctl91      page v9_91_0: the controller's width probe PASS at the three widths and its fifth run of page test 9.37.0 'RESULT: PASS'
A missing log is a failure (NOT_MEASURED is not a pass). Run from the repository root."""
import glob, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
L = os.path.join(R, "08-tooling/ch08-page/logs_u8"); CL = os.path.join(R, "08-tooling/control-u8-logs")
DECK = "03-materials/ch08/SEN0414_Ch08_Strings_3e_v2_1_0.pptx"; MAN = "03-materials/ch08/page/chapter_code_ch08_v1_1_0.json"
bad = []
def say(ok, what):
    print(("PASS " if ok else "FAIL ") + what)
    if not ok: bad.append(what)
def run(cmd):
    p = subprocess.run(cmd, cwd=R, capture_output=True, text=True); return p.returncode, p.stdout + p.stderr
def rd(path):
    try: return open(path, encoding="utf-8", errors="replace").read()
    except OSError: return None
def deckcheck():
    rc, o = run([sys.executable, "08-tooling/sen0414_deck_standard_check_v1_1_0.py", "--selftest"]); say(rc == 0 and "0 mismatches" in o, "deck check selftest exit %d, 0 mismatches" % rc)
    rc, o = run([sys.executable, "08-tooling/sen0414_deck_standard_check_v1_1_0.py", "8", DECK, MAN]); say(rc == 0 and "SUMMARY PASS=13 FAIL=0 NOT_MEASURED=0" in o, "deck check on the Chapter 8 deck v2.1.0 exit %d, SUMMARY PASS=13 FAIL=0 NOT_MEASURED=0" % rc)
    m = rd(os.path.join(CL, "control_deckcheck_mutations_run1.log")) or ""
    for name, el in (("nopic", "D5 FAIL"), ("longbox", "D2 FAIL"), ("widecode", "D12 FAIL")):
        i = m.find("== " + name); j = m.find("\n== ", i + 1); seg = m[i:j if j > 0 else None]
        say(i >= 0 and el in seg, "mutation probe %s fails in %s" % (name, el))
    i = m.find("== chcode with manifest"); say(i >= 0 and "M1 FAIL" in m[i:], "mutation probe chcode fails in M1")
def deck():
    rc, o = run([sys.executable, "08-tooling/sen0414_control_urgent_deck_v1_0_0.py", DECK, MAN]); say(rc == 0 and "RESULT PASS" in o, "controller's deck checks C1-C8 exit %d" % rc)
    deckcheck()
def pagetest(path, what):
    t = rd(path)
    if t is None: say(False, what + ": log missing " + os.path.basename(path)); return
    say("RESULT: PASS" in t and re.search(r"failed 0,", t) is not None and re.search(r"^exit 0\s*$", t, re.M) is not None, what + " (" + os.path.basename(path) + ")")
def widths(path, what):
    t = rd(path)
    if t is None: say(False, what + ": log missing"); return
    say(all(("PASS at %s" % w) in t for w in ("1366x768", "1400x900", "390x844")) and "FAIL" not in t, what)
def page():
    for i in range(1, 6): pagetest(os.path.join(L, "page_test_9_37_0_v9_92_1_run%d.log" % i), "page test 9.37.0 on v9_92_1 run %d" % i)
    pagetest(os.path.join(L, "page_test_9_38_0_v9_92_1_ctl_run1.log"), "page test 9.38.0 on v9_92_1 (controller)")
    t = rd(os.path.join(L, "leak_probe_v1_3_0_page_v9_92_1_run2.log")) or ""
    say(all(("seed %d " % s) in t for s in range(1, 6)) and "baseline_bad=0 wrong_real_runs=0 state_drifts=0" in t and re.search(r"^exit 0\s*$", t, re.M) is not None, "leak probe v1_3_0 seeds 1-5")
    widths(os.path.join(L, "playground_width_v9_92_1_ctl_run1.log"), "Playground width probe on v9_92_1 at 1366, 1400, 390")
    t = rd(os.path.join(L, "story_layout_v9_92_1_ctl_run1.log")) or ""
    say("RESULT: PASS" in t and "FAIL" not in t, "story-layout probe on v9_92_1")
def ctl91():
    widths(os.path.join(L, "playground_width_v9_91_0_ctl_run1.log"), "Playground width probe on v9_91_0 at 1366, 1400, 390")
    pagetest(os.path.join(L, "page_test_9_37_0_v9_91_0_ctl_run5.log"), "page test 9.37.0 on v9_91_0, fifth run")
if __name__ == "__main__":
    {"deckcheck": deckcheck, "deck": deck, "page": page, "ctl91": ctl91}[sys.argv[1]]()
    print("RESULT " + ("FAIL: " + "; ".join(bad) if bad else "PASS")); sys.exit(1 if bad else 0)
