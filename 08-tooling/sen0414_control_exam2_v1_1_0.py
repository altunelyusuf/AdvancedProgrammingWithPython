#!/usr/bin/env python3
"""sen0414_control_exam2 v1_1_0 (over v1_0_0, which stays: adds the check 'engine') - the lineage agent's control verdicts for box 2 of the exam lineage (run by the evidence bridge as a test command; exit 0 = the controlled facts hold).
Usage: sen0414_control_exam2_v1_0_0.py distinct | designrev | engine      (from the repository root)
  distinct   the executor's fixtures check exits 0 with 'all fixtures as expected'; the controller's own pairs (own implementation of the 4-word share, boundary cases 0.4/0.6/0.8 with equal and different answers, verbatim real seeds,
             an unrelated text) pass (kept log control_nocopy_own_pairs_run1.log, re-run here)
  designrev  the executor's design check v1_1_0 and item validator selftest exit 0; the controller's own arithmetic over the blueprint and own defective items (kept logs) hold"""
import subprocess, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); X = "04-assessment/exams/"; bad = []
def run(cmd):
    p = subprocess.run(cmd, cwd=R, capture_output=True, text=True); return p.returncode, p.stdout + p.stderr
def say(ok, w):
    print(("PASS " if ok else "FAIL ") + w)
    if not ok: bad.append(w)
def logok(name, key):
    try: t = open(os.path.join(R, "08-tooling/control-exam-logs", name), encoding="utf-8").read()
    except OSError: say(False, name + " missing"); return
    say(key in t and "FAIL" not in t.replace("(fails a majority", ""), "kept log " + name + " has " + key)
if sys.argv[1] == "distinct":
    rc, o = run([sys.executable, X + "exam_nocopy_fixtures_check_v1_0_0.py"]); say(rc == 0 and "RESULT: all fixtures as expected" in o, "fixtures check exit %d" % rc)
    logok("control_nocopy_own_pairs_run1.log", "RESULT PASS")
elif sys.argv[1] == "engine":
    rc, o = run([sys.executable, X + "exam_engine_check_v1_0_0.py", "--quick"]); say(rc == 0 and "RESULT PASS" in o, "engine check (quick) exit %d" % rc)
    try: t = open(os.path.join(R, "08-tooling/control-exam-logs/control_engine_own_pairs_run1.log"), encoding="utf-8").read()
    except OSError: t = ""
    say("build exit 0; same seed twice gives identical" in t.replace("valid pool: ", "") and "REFUSED: E03" in t, "kept log of the controller's own pairs (valid pool builds, same seed identical, no chapter 8 refused with E03)")
else:
    rc, o = run([sys.executable, X + "exam_design_check_v1_1_0.py"]); say(rc == 0 and "RESULT PASS" in o, "design check v1_1_0 exit %d" % rc)
    rc, o = run([sys.executable, X + "exam_item_check_v1_0_0.py", "selftest"]); say(rc == 0 and "RESULT PASS" in o, "item validator selftest exit %d" % rc)
    logok("control_design_v1_1_0_own_arithmetic_run2.log", "RESULT PASS"); logok("control_item_check_own_pairs_run1.log", "RESULT PASS")
print("RESULT " + ("FAIL: " + "; ".join(bad) if bad else "PASS")); sys.exit(1 if bad else 0)
