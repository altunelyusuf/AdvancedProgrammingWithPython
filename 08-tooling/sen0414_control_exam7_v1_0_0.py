#!/usr/bin/env python3
"""sen0414_control_exam3 v1_0_0 - the lineage agent's own control checks for the exam change of 2026-11-01 (run by the evidence bridge as a test command; exit 0 = the controlled facts hold). Written by the controller; executors never run it.
Usage: sen0414_control_exam4_v1_0_0.py points5 | itemrules2 | itemsa2 | engine5 | itemsb2 | itemsa3 (design2 and cover as in exam3)
  design2  the executor's design check v1_2_0 exits 0 with RESULT PASS; the controller's own recount of design v1_2_0 from its JSON (30 sub-questions, 6/7/7/6/4, points 25/25/25/25/10, no Bloom 1, at least 8 of 30 at Bloom 4 or higher and a majority at 3 or higher,
           every chapter 1-8 present, every sub-question asks use/reason/effect); the task's commit adds only new files under 04-assessment/exams
  cover    the executor's check exits 0 with RESULT: PASS; the controller builds midterm form A and make-up form B itself, converts with LibreOffice (one page each), finds no wording of the template's course, finds the grade-table texts (/25 four times, '/10 (bonus)', '/100 + bonus'); the commit adds only new files
  points5  the critical-points checks of sen0414_control_exam_v1_0_0 (points) for chapter 5; the not-found list exists; the task's commits add only new files under 04-assessment/exams"""
import collections, glob, json, os, subprocess, sys, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); X = os.path.join(R, "04-assessment/exams"); bad = []
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def run(cmd, **k):
    p = subprocess.run(cmd, cwd=R, capture_output=True, text=True, **k); return p.returncode, p.stdout + p.stderr
def say(ok, w):
    print(("PASS " if ok else "FAIL ") + w)
    if not ok: bad.append(w)
def only_new(sha, prefix="04-assessment/exams/"):
    rc, o = run(["git", "show", "--name-status", "--format=", sha]); rows = [l.split("\t") for l in o.strip().splitlines() if l.strip()]
    say(bool(rows) and all(r[0] == "A" and r[1].startswith(prefix) for r in rows), "commit %s adds only new files under %s (%d files)" % (sha, prefix, len(rows)))
m = sys.argv[1]
if m == "design2":
    rc, o = run([sys.executable, "04-assessment/exams/exam_design_check_v1_2_0.py"]); say(rc == 0 and "RESULT PASS" in o, "executor's design check v1_2_0 exit %d" % rc)
    d = json.load(open(os.path.join(X, "exam_design_v1_2_0.json"))); S = d["sub_questions"]
    c = collections.Counter(s["question"] for s in S); pts = collections.Counter()
    for s in S: pts[s["question"]] += s["points"]
    say(len(S) == 30 and [c[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [6, 7, 7, 6, 4], "30 sub-questions, 6/7/7/6/4: %s" % dict(c))
    say([pts[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [25, 25, 25, 25, 10], "points per question 25/25/25/25/10: %s" % dict(pts))
    say(all(s["bloom"] >= 2 for s in S), "no sub-question at Bloom 1")
    a3 = sum(s["bloom"] >= 3 for s in S); a4 = sum(s["bloom"] >= 4 for s in S)
    say(a3 > 15 and a4 >= 8, "Apply and above %d of 30 (majority), Analyze and above %d (at least 8)" % (a3, a4))
    say(set(s["chapter"] for s in S if isinstance(s["chapter"], int)) >= set(range(1, 9)), "chapters 1 to 8 all present")
    say(all(s["asks"] in ("use", "reason", "effect") for s in S), "every sub-question asks use, reason or effect")
    only_new("bc305be")
elif m == "cover":
    rc, o = run([sys.executable, "04-assessment/exams/exam_cover_check_v1_0_0.py"]); say(rc == 0 and "RESULT: PASS" in o, "executor's cover check exit %d" % rc)
    sys.path.insert(0, X); import exam_cover_v1_0_0 as c, docx
    t = tempfile.mkdtemp()
    for kind, form in (("midterm", "A"), ("makeup", "B")):
        f = os.path.join(t, "%s_%s.docx" % (kind, form)); c.cover_sen0414(kind, form).save(f)
        rc, o = run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", t, f], timeout=180)
        pdf = f[:-5] + ".pdf"; pages = None
        if os.path.exists(pdf):
            import re; pages = int(re.search(r"Pages:\s+(\d+)", run(["pdfinfo", pdf])[1]).group(1))
        say(pages == 1, "%s form %s renders to %s page(s) (LibreOffice)" % (kind, form, pages))
        d = docx.Document(f); txt = " ".join(d.element.body.itertext())   # every text node, nested tables included
        say(not any(w in txt for w in ("CSE3003", "Object Oriented", "PATLAR", "Fatma")), "no wording of the template's course")
        say(txt.count("/25") >= 4 and "/10" in txt and "bonus" in txt and "/100" in txt, "grade table: four /25 rows, a /10 bonus row")
        say("SEN0414 Advanced Programming" in txt and "60 Minutes" in txt and "2026-2027" in txt, "course, duration and academic year filled")
    say(not [p for p in glob.glob(os.path.join(R, "**/*.docx"), recursive=True) if "IKU_exam_cover" in p], "the template is not in the repository")
    import shutil; shutil.rmtree(t, ignore_errors=True); only_new("bea6a20")
elif m == "points5":
    import sen0414_control_exam_v1_0_0 as K
    K.points("ch05", [5]); [say(False, w) for w in K.BAD]
    rc, o = run(["git", "log", "--format=%h", "--grep=(TK4_Points5)"]); shas = o.split()
    say(bool(shas), "commits found by the task identifier: %s" % shas)
    for s_ in shas: only_new(s_)
    rc, o = run(["git", "status", "--short", "04-assessment/exams"]); say(not o.strip(), "everything committed under 04-assessment/exams")
elif m == "itemrules2":
    import copy, importlib.util
    for v in ("1_0_0", "1_1_0"):
        rc, o = run([sys.executable, "04-assessment/exams/exam_item_check_v%s.py" % v, "selftest"]); say(rc == 0 and "RESULT PASS" in o, "executor's validator v%s selftest exit %d" % (v, rc))
    sp = importlib.util.spec_from_file_location("iv", os.path.join(X, "exam_item_check_v1_1_0.py")); iv = importlib.util.module_from_spec(sp); sp.loader.exec_module(iv)
    fx = json.load(open(os.path.join(X, "exam_item_check_fixtures_v1_1_0.json")))["fixtures"]; say(len(fx) == 66, "66 fixtures")
    base = copy.deepcopy(fx[0]["items"][0]); say(iv.check_items([base]) == [], "the controller's own base item (valid_mcq) passes")
    def rules(**ch):
        it = copy.deepcopy(base); it.update(ch); return sorted(set(r["rule"] for r in iv.check_items([it])))
    L = "Which keyword defines a function in Python, and what does the word stand for in the language?"; A = "Why does the CPU treat the expression -3 ** 2 as minus nine and not as plus nine here?"
    say("R05" in rules(bloom=1), "bloom 1 is a violation (R05): %s" % rules(bloom=1))
    say("R24" in rules(stem="Why -9?"), "short stem is a violation (R24): %s" % rules(stem="Why -9?"))
    say("R22" in rules(asks="define"), "asks outside use/reason/effect is a violation (R22): %s" % rules(asks="define"))
    say("R23" in rules(points=7, sub="a", question="Q1"), "question/sub/type mismatch is a violation (R23): %s" % rules(points=7, sub="a", question="Q1"))
    say("R19" in rules(stem=L), "memorisation stem is a violation (R19): %s" % rules(stem=L))
    say("R21" in rules(stem=A), "abbreviation not in full is a violation (R21): %s" % rules(stem=A))
    say("R01" in rules(extra_field=1), "unknown field is a violation (R01): %s" % rules(extra_field=1))
    only_new("fe726d3")
    rc, o = run(["git", "status", "--short", "04-assessment/exams"]); say(not o.strip(), "everything committed under 04-assessment/exams")
elif m == "itemsa2":
    import collections as C
    I = os.path.join(X, "items"); rc, o = run([sys.executable, "04-assessment/exams/items/items_a_v2_0_0_check.py"]); say(rc == 0 and "RESULT PASS" in o, "executor's check exit %d" % rc)
    sys.path.insert(0, X); import exam_item_check_v1_1_0 as iv
    L = {n: json.load(open(os.path.join(I, n))) for n in ("items_a_v2_0_0.json", "items_a_v2_0_0_makeup.json")}
    for n, d in L.items():
        say(iv.check_items(d) == [], "%s passes the validator v1_1_0 on the controller's own call (%d records)" % (n, len(d)))
        say(len(d) == 14 and len({i["id"] for i in d}) == 14, "%s: 14 records, 14 different ids" % n)
        say(sum(i["bloom"] >= 3 for i in d) >= 0.4 * len(d) and sum(i["bloom"] >= 4 for i in d) >= 0.3 * len(d), "%s: Apply and above %d, Analyze and above %d of %d" % (n, sum(i["bloom"] >= 3 for i in d), sum(i["bloom"] >= 4 for i in d), len(d)))
        say(all(i["bloom"] >= 2 and i["asks"] in ("use", "reason", "effect") for i in d), "%s: no Bloom 1, every record asks use, reason or effect" % n)
        u = C.Counter()
        for i in d:
            o_ = i["options_or_blanks"]; u[i["question"]] += (o_["gaps"] if i["type"] in ("blank", "cloze") else len(o_["premises"]) if i["type"] == "match" else len(o_) if i["type"] == "order" else 1)
        say(u["Q1"] == 6 and u["Q2"] == 7 and u["Q3"] == 5 + 1 and u["Q4"] == 4 + 1 and u["Q5"] == 2, "%s: units (gaps, premises, steps, choices) per question so far %s" % (n, dict(u)))
        say(set(c for i in d for c in i["chapters"]) >= set(range(1, 9)), "%s: chapters 1 to 8 all covered" % n)
    a, b = L["items_a_v2_0_0.json"], L["items_a_v2_0_0_makeup.json"]
    say(not ({i["stem"] for i in a} & {i["stem"] for i in b}), "no identical stem in the paper list and the make-up list")
    say(all(i["id"] == i["question"] + i["sub"] for i in a + b), "every id is question plus sub")
    sd = json.load(open(os.path.join(I, "items_a_v2_0_0_provisional.json"))); say(len(sd) == 28 or (isinstance(sd, dict) and len(json.dumps(sd)) > 100), "provisional side file present")
    only_new("94e08e1", "04-assessment/exams/items/")
    rc, o = run(["git", "status", "--short", "04-assessment/exams/items"]); say(not o.strip(), "everything committed under 04-assessment/exams/items")
elif m == "engine5":
    import copy, tempfile
    EN = os.path.join(X, "exam_engine_v1_1_0.py"); fx = json.load(open(os.path.join(X, "exam_engine_fixtures_v1_1_0.json"))); base = fx["pools"]["midterm"]
    rc, o = run([sys.executable, os.path.join(X, "exam_engine_check_v1_1_0.py")]); say(rc == 0 and "RESULT" in o and "FAIL" not in o.split("RESULT")[-1], "executor's engine check exit %d" % rc)
    def build(pool):
        with tempfile.TemporaryDirectory() as td:
            p = os.path.join(td, "p.json"); json.dump(pool, open(p, "w"))
            rc, o = run([sys.executable, EN, "build", "--pool", p, "--design", os.path.join(X, "exam_design_v1_2_0.json"), "--seed", "20261102", "--out", os.path.join(td, "o")])
        return rc, sorted(set(l.split()[0] for l in o.splitlines() if len(l.split()) > 1 and l.split()[1] == "FAIL"))
    rc, f = build(base); say(rc == 0 and f == [], "the executor's valid pool builds a paper with every rule passing (exit %d)" % rc)
    def mut(name, fn, want):
        p = copy.deepcopy(base); fn(p); rc, f = build(p); say(rc == 1 and all(w in f for w in want), "controller mutation %s is refused with %s (got exit %d, %s)" % (name, want, rc, f))
    def low(p):
        for s_ in p["sets"]:
            for i in s_["items"]: i["bloom"] = min(i["bloom"], 2)
    def noan(p):
        for s_ in p["sets"]:
            for i in s_["items"]:
                if i["bloom"] >= 4: i["bloom"] = 3
    def dup(p): p["sets"][0]["items"].append(copy.deepcopy(p["sets"][0]["items"][0]))
    def pts(p):
        for s_ in p["sets"]:
            for i in s_["items"]: i["points"] += 1
    def drop(p):
        for s_ in p["sets"]: s_["items"].pop()
    def ch9(p):
        for s_ in p["sets"]:
            for i in s_["items"]: i["chapters"] = [9]
    mut("all Bloom 2", low, ["E06", "E24"]); mut("no Analyze and above", noan, ["E24"]); mut("repeated id", dup, ["E01"]); mut("points plus one", pts, ["E22"]); mut("a record dropped from every set", drop, ["E03", "E22"]); mut("chapter 9", ch9, ["E02", "E03"])
    rc, o = run([sys.executable, os.path.join(X, "exam_item_check_v1_1_0.py"), "selftest"]); say(rc == 0, "item validator selftest still passes")
    only_new("540b51b")
    rc, o = run(["git", "status", "--short", "04-assessment/exams/exam_engine_v1_1_0.py", "04-assessment/exams/exam_engine_check_v1_1_0.py", "04-assessment/exams/exam_engine_shapes_v1_1_0.ttl", "04-assessment/exams/exam_engine_fixtures_v1_1_0.json"]); say(not o.strip(), "engine files committed")
elif m == "itemsb2":
    sys.path.insert(0, X); import exam_item_check_v1_1_0 as iv, exam_engine_v1_1_0 as EN_
    I = os.path.join(X, "items"); only_new("034c4dd", "04-assessment/exams/items/")
    for lst in ("", "_makeup"):
        A = json.load(open(os.path.join(I, "items_a_v2_0_0%s.json" % lst))); Bq = json.load(open(os.path.join(I, "items_b_v2_0_0%s.json" % lst))); M = A + Bq
        say(iv.check_items(Bq) == [] and iv.check_items(M) == [], "list%s: B alone and A plus B pass the validator v1_1_0 (%d records)" % (lst or " paper", len(M)))
        say(len({i["id"] for i in M}) == len(M), "list%s: no repeated id in A plus B" % (lst or " paper"))
        u = collections.Counter(); pts = collections.Counter()
        for i in M: u[i["question"]] += EN_.units_of(i); pts[i["question"]] += i["points"]
        say([u[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [6, 7, 7, 6, 4] and [pts[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [25, 25, 25, 25, 10], "list%s: units 6/7/7/6/4 and points 25/25/25/25/10: %s %s" % (lst or " paper", dict(u), dict(pts)))
        cc = collections.Counter(c for i in M for c in EN_.unit_chapters(i)); xc = sum(1 for i in M if EN_.units_of(i) == 1 and len(i["chapters"]) > 1)
        say(dict(cc) != {1: 4, 2: 4, 3: 4, 4: 4, 5: 3, 6: 4, 7: 4, 8: 3} and xc < 9, "list%s: the executor's report of the shortfall is true: units per chapter %s (quota 4,4,4,4,3,4,4,3), cross-chapter %d (minimum 9)" % (lst or " paper", dict(sorted(cc.items())), xc))
    for lst, nm in (("", "paper"), ("_makeup", "make-up")):
        with tempfile.TemporaryDirectory() as td:
            pool = [json.load(open(os.path.join(I, "items_%s_v2_0_0%s.json" % (k, lst)))) for k in "ab"]; p = os.path.join(td, "p.json"); json.dump(pool[0] + pool[1], open(p, "w"))
            rc, o = run([sys.executable, os.path.join(X, "exam_engine_v1_1_0.py"), "build", "--pool", p, "--design", os.path.join(X, "exam_design_v1_2_0.json"), "--seed", "20261102", "--out", os.path.join(td, "o")])
        refused = sorted(set(l.split()[0] for l in o.splitlines() if len(l.split()) > 1 and l.split()[1] == "FAIL")); say(rc == 1 and "E03" in refused and "E09" in refused, "the engine refuses the merged %s pool on E03 and E09 (got exit %d, %s)" % (nm, rc, refused))
elif m in ("itemsa3", "itemsb2m"):
    import tempfile
    sys.path.insert(0, X); import exam_item_check_v1_1_0 as iv, exam_engine_v1_1_0 as EN_
    I = os.path.join(X, "items"); DES = os.path.join(X, "exam_design_v1_2_0.json")
    rc, o = run([sys.executable, os.path.join(I, "items_a_v2_1_0_check.py")]); say(rc == 0 and "RESULT PASS" in o, "executor's check exit %d" % rc)
    rc, o = run([sys.executable, os.path.join(I, "items_b_v2_0_0_check.py")]); print("executor's set B check exit", rc, "(informational: it reports the merged build with its own set A pairing)")
    only_new("275e1d9", "04-assessment/exams/items/"); only_new("034c4dd", "04-assessment/exams/items/")
    rc, o = run(["git", "status", "--short", "04-assessment/exams/items"]); say(not o.strip(), "everything committed under 04-assessment/exams/items")
    quota = {1: 4, 2: 4, 3: 4, 4: 4, 5: 3, 6: 4, 7: 4, 8: 3}; sets = {}
    for lst, nm in (("", "paper"), ("_makeup", "makeup")):
        A = json.load(open(os.path.join(I, "items_a_v2_1_0%s.json" % lst))); Bq = json.load(open(os.path.join(I, "items_b_v2_0_0%s.json" % lst))); M = A + Bq; sets[nm] = M
        say(len(A) == 14 and iv.check_items(A) == [] and iv.check_items(M) == [] and len({i["id"] for i in M}) == 18, "%s: A 14 records, A and A plus B pass the validator v1_1_0, 18 different ids" % nm)
        u = collections.Counter(); pts = collections.Counter()
        for i in M: u[i["question"]] += EN_.units_of(i); pts[i["question"]] += i["points"]
        say([u[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [6, 7, 7, 6, 4] and [pts[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [25, 25, 25, 25, 10], "%s: units 6/7/7/6/4, points 25/25/25/25/10" % nm)
        cc = collections.Counter(c for i in M for c in EN_.unit_chapters(i)); say(dict(cc) == quota, "%s: units per chapter equal the quota: %s" % (nm, dict(sorted(cc.items()))))
        xc = sum(1 for i in M if EN_.units_of(i) == 1 and len(i["chapters"]) > 1); say(xc == 9, "%s: cross-chapter %d (design 9)" % (nm, xc))
        ap = sum(EN_.units_of(i) for i in M if i["bloom"] >= 3); an = sum(EN_.units_of(i) for i in M if i["bloom"] >= 4); say(ap > 15 and an >= 8, "%s: Apply and above %d of 30 units, Analyze and above %d" % (nm, ap, an)); print("MEASURE", nm, "apply_share_percent", round(100 * ap / 30, 1))
    say(not ({i["stem"] for i in sets["paper"]} & {i["stem"] for i in sets["makeup"]}), "no identical stem between the paper and the make-up list")
    with tempfile.TemporaryDirectory() as td:
        for nm in ("paper", "makeup"): json.dump({"sets": [{"name": nm, "items": sets[nm]}]}, open(os.path.join(td, nm + ".json"), "w"))
        def eng(nm, seed, extra):
            rc, o = run([sys.executable, os.path.join(X, "exam_engine_v1_1_0.py"), "build", "--pool", os.path.join(td, nm + ".json"), "--design", DES, "--seed", str(seed), "--out", os.path.join(td, "o_" + nm + str(seed)), "--kind", "midterm" if nm == "paper" else "makeup"] + extra)
            ps = sum(1 for l in o.splitlines() if len(l.split()) > 1 and l.split()[0].startswith("E") and l.split()[1] == "PASS"); return rc, ps, o
        for sd in (1, 20261101, 20261102):
            rc, ps, o = eng("paper", sd, []); say(rc == 0 and ps == 28, "engine builds the merged paper pool, seed %d: exit %d, %d of 28 rules pass" % (sd, rc, ps))
        rc, ps, o = eng("paper", 20261102, []); b = [f for f in glob.glob(os.path.join(td, "o_paper20261102", "*_build.json"))]
        for sd in (7, 20261102):
            rc, ps, o = eng("makeup", sd, ["--midterm", b[0]]); say(rc == 0 and ps == 28, "engine builds the make-up pool against the midterm build, seed %d: exit %d, %d of 28 rules pass" % (sd, rc, ps))
print("RESULT " + ("FAIL: " + "; ".join(bad) if bad else "PASS")); sys.exit(1 if bad else 0)
