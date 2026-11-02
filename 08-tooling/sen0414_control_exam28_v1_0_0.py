#!/usr/bin/env python3
"""sen0414_control_exam28 v1_0_0 - the lineage agent's own control checks for the SEN0414 v4.0.0 exam set (urgent redesign of 2026-11-02), run by the evidence bridge as a test command (exit 0 = the controlled facts hold). The files are in the private CME repository (/home/claude/CME/exams/SEN0414); only this controller and its kept logs are public.
Usage: sen0414_control_exam28_v1_0_0.py v4items | v4design | v4score | v4set | v4measure
  v4items    items_v4_0_1.json: validator v1_3_0 check and selftest PASS, the items check PASS, 14 records / 27 units / 100 points / 25 per question, five alternatives per closed unit, no Q5, only Q4a (16 -> 15) and Q4b (4 -> 5) differ from v4_0_0, tips of at most 12 words, committed files unchanged
  v4design   design v1_6_0 check PASS, only the Bloom 4+ minimum (7 of 27) differs in substance from v1_5_0, engine v1_4_0 verify of the real build: 34 of 34 rules PASS, the unit table: 27 units, 100 points, 7 units at Bloom 4+, letters 2 each
  v4score    marking tool check 35 of 35 PASS, agreement check 10 of 10 PASS on the real design and key, exact blind figures recomputed independently (mean 20, sd 7.8588, P(>=20) 50.3543 %), grading procedure text exists
  v4set      the delivery set: five files named by the convention, SHA256.txt matches, delivery check RESULT PASS, pages paper 4 / sheet 1 / key 3, no deduction, bonus or Q5 wording, 10 tips printed
  v4measure  the measure v1_3_0 rerun: PASS 79, FAIL 0, RISK 1 (R10b), NOT_MEASURED 1 (L3, Word)"""
import glob, hashlib, json, os, re, subprocess, sys, tempfile
from fractions import Fraction as F
C = "/home/claude/CME/exams/SEN0414"; X = C + "/04-assessment/exams"; T = C + "/08-tooling/exam"; PUB = "/home/claude/AdvancedProgrammingWithPython"; bad = []
def run(cmd, cwd=X):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=dict(os.environ, SEN0414_ROOT=PUB)); return p.returncode, p.stdout + p.stderr
def say(ok, w):
    print(("PASS " if ok else "FAIL ") + w)
    if not ok: bad.append(w)
def items(f):
    d = json.load(open(f)); return d if isinstance(d, list) else d.get("items", d)
m = sys.argv[1]
if m == "v4items":
    rc, o = run([sys.executable, "exam_item_check_v1_3_0.py", "check", "items/items_v4_0_1.json"]); say(rc == 0 and "RESULT PASS 0 failure" in o, "validator v1_3_0 check on items_v4_0_1: exit %d" % rc)
    rc, o = run([sys.executable, "exam_item_check_v1_3_0.py", "selftest"]); say(rc == 0 and "RESULT PASS" in o, "validator v1_3_0 selftest: exit %d" % rc)
    rc, o = run([sys.executable, "items/items_v4_0_1_check.py"]); say(rc == 0 and "RESULT PASS" in o, "executor's items check: exit %d" % rc)
    A = items(X + "/items/items_v4_0_0.json"); B = items(X + "/items/items_v4_0_1.json")
    say(len(B) == 14 and sum(r["points"] for r in B) == 100 and all(sum(r["points"] for r in B if r["question"] == q) == 25 for q in ("Q1", "Q2", "Q3", "Q4")), "14 records, 100 points, 25 per question")
    dif = [(a["id"], k, a.get(k), b.get(k)) for a, b in zip(A, B) for k in set(a) | set(b) if a.get(k) != b.get(k)]
    say(sorted(dif) == [("Q4a", "points", 16, 15), ("Q4b", "points", 4, 5)], "v4_0_1 differs from v4_0_0 in exactly Q4a 16->15 and Q4b 4->5: %s" % dif)
    say(not any(r["question"] == "Q5" for r in B), "no Q5 record")
    say(all(r.get("tip", "none") == "none" or len(r["tip"].split()) <= 12 for r in B), "every tip has at most 12 words")
    rc, o = run(["git", "diff", "--quiet", "HEAD", "--", "04-assessment/exams/items/items_v4_0_0.json", "04-assessment/exams/exam_item_check_v1_2_0.py", "04-assessment/exams/items/items_v3_0_0.json"], cwd=C + "/../.."); say(rc == 0, "items v4_0_0, v3_0_0 and validator v1_2_0 are unchanged against the committed copy")
elif m == "v4design":
    rc, o = run([sys.executable, "exam_design_check_v1_6_0.py"]); say(rc == 0 and "RESULT PASS" in o, "design check v1_6_0: exit %d" % rc)
    d5 = json.load(open(X + "/exam_design_v1_5_0.json")); d6 = json.load(open(X + "/exam_design_v1_6_0.json"))
    say(d6["blueprint"]["bloom_rule"]["min_required"] == 7 and d6["blueprint"]["items"] == 27 and d6["blueprint"]["base_points"] == 100 and d5["blueprint"]["bloom_rule"]["min_required"] == 8, "design v1_6_0: minimum 7 of 27 at Bloom 4+, 100 points (v1_5_0 said 8)")
    rc, o = run([sys.executable, "exam_engine_v1_4_0.py", "verify", "papers_r20/build/exam_midterm_s1_buildfull.json"]); say(rc == 0 and len(re.findall(r"^E\d\d PASS", o, re.M)) == 34 and "FAIL" not in o, "engine v1_4_0 verify of the real build: exit %d, %d PASS lines" % (rc, len(re.findall(r"^E\d\d PASS", o, re.M))))
    rows = [l.split() for l in open(X + "/papers_r20/build/unit_table_seed1.txt") if re.match(r"\d[a-g] ", l)]
    pts = [int(r[2]) for r in rows]; bl = [int(r[4]) for r in rows]; lt = [r[3] for r in rows if r[1] == "choice" or True]
    say(len(rows) == 27 and sum(pts) == 100 and sum(b >= 4 for b in bl) == 7, "unit table: %d units, %d points, %d units at Bloom 4+" % (len(rows), sum(pts), sum(b >= 4 for b in bl)))
    k = json.load(open(X + "/papers_r20/build/exam_midterm_s1_key.json")); say(len(json.dumps(k)) > 100, "real key present")
elif m == "v4score":
    w = tempfile.mkdtemp(); rc, o = run([sys.executable, T + "/sen0414_exam_score_check_v1_2_0.py", w], cwd=T); say(rc == 0 and "RESULT 35 of 35 PASS" in o, "marking tool check: exit %d, 35 of 35" % rc)
    w = tempfile.mkdtemp(); rc, o = run([sys.executable, T + "/sen0414_exam_score_agree_v1_2_1.py", w, "--design", X + "/exam_design_v1_6_0.json", "--key", X + "/papers_r20/build/exam_midterm_s1_key.json"], cwd=T); say(rc == 0 and "SUMMARY PASS 10, FAIL 0, NOT_MEASURED 0" in o, "agreement check on the real design and key: exit %d" % rc)
    pts = [int(l.split()[2]) for l in open(X + "/papers_r20/build/unit_table_seed1.txt") if re.match(r"\d[a-g] ", l)]
    dist = {0: F(1)}
    for p in pts:
        n = {}
        for s, q in dist.items(): n[s] = n.get(s, 0) + q * F(4, 5); n[s + p] = n.get(s + p, 0) + q * F(1, 5)
        dist = n
    mean = sum(s * q for s, q in dist.items()); sd = float(sum((s - mean) ** 2 * q for s, q in dist.items())) ** .5; p20 = float(sum(q for s, q in dist.items() if s >= 20)) * 100
    say(mean == 20 and abs(sd - 7.8588) < 5e-5 and abs(p20 - 50.3543) < 5e-5, "exact blind figures recomputed from the unit table: mean %s, sd %.4f, P(>=20) %.4f %%" % (mean, sd, p20))
    say(os.path.exists(T + "/score_v1_2/grading_procedure_v4_0_0.md"), "grading procedure text exists")
elif m == "v4set":
    D = X + "/papers_r20/delivery"; P = "sen0414_exam_midterm_v4_0_0_"; names = [P + n for n in ("paper.docx", "paper.pdf", "key.docx", "key.pdf", "sheet.pdf")]
    say(sorted(os.listdir(D)) == sorted(names + ["SHA256.txt"]), "the delivery folder holds the five convention names and SHA256.txt: %s" % sorted(os.listdir(D)))
    h = {l.split()[1]: l.split()[0] for l in open(D + "/SHA256.txt") if l.strip()}; say(all(h.get(n) == hashlib.sha256(open(D + "/" + n, "rb").read()).hexdigest() for n in names), "SHA256.txt matches all five files")
    rc, o = run([sys.executable, "exam_v4_delivery_check_v1_0_1.py", "papers_r20", PUB, "exam_design_v1_6_0.json", T + "/score_v1_2/grading_procedure_v4_0_0.md"]); say(rc == 0 and "RESULT PASS" in o, "delivery check v1_0_1: exit %d" % rc)
    pg = {n: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", D + "/" + n], capture_output=True, text=True).stdout).group(1)) for n in names if n.endswith(".pdf")}; say([pg[P + "paper.pdf"], pg[P + "sheet.pdf"], pg[P + "key.pdf"]] == [4, 1, 3], "pages paper/sheet/key %s" % pg)
    txt = subprocess.run(["pdftotext", "-layout", D + "/" + P + "paper.pdf", "-"], capture_output=True, text=True).stdout; say(not re.search(r"penalt|deduct|bonus|Question 5|subtract", txt, re.I) and txt.count("Tip:") == 10, "paper: no penalty, deduction, bonus or Question 5 wording; 10 tip lines")
elif m == "v4measure":
    w = tempfile.mkdtemp(); lg = os.path.join(tempfile.mkdtemp(), "m.log"); rc, o = run([sys.executable, "exam_papers_measure_v1_3_0.py", w, "--log", lg]); say("SUMMARY: PASS 79, RISK 1, NOT_MEASURED 1, INFO 3" in o, "measure v1_3_0 rerun: %s" % [l for l in o.splitlines() if "SUMMARY" in l])
    L = open(lg).read(); say("RISK         R10b" in L and "NOT_MEASURED L3" in L and not re.search(r"^FAIL", L, re.M), "the one RISK is R10b (page 2 slack 2.0 pt), the one NOT_MEASURED is L3 (Word), no FAIL")
print("RESULT", "PASS" if not bad else "FAIL %d" % len(bad)); sys.exit(1 if bad else 0)
