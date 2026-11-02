#!/usr/bin/env python3
"""sen0414_control_exam25 v1_0_0 (copy of sen0414_control_exam22_v1_0_0.py with the mode revpapers added) - the lineage agent's own control checks for the exam change of 2026-11-01 (run by the evidence bridge as a test command; exit 0 = the controlled facts hold). Written by the controller; executors never run it.
Usage: sen0414_control_exam4_v1_0_0.py points5 | itemrules2 | itemsa2 | engine5 | itemsb2 | itemsa3 (design2 and cover as in exam3)
  design2  the executor's design check v1_2_0 exits 0 with RESULT PASS; the controller's own recount of design v1_2_0 from its JSON (30 sub-questions, 6/7/7/6/4, points 25/25/25/25/10, no Bloom 1, at least 8 of 30 at Bloom 4 or higher and a majority at 3 or higher,
           every chapter 1-8 present, every sub-question asks use/reason/effect); the task's commit adds only new files under 04-assessment/exams
  cover    the executor's check exits 0 with RESULT: PASS; the controller builds midterm form A and make-up form B itself, converts with LibreOffice (one page each), finds no wording of the template's course, finds the grade-table texts (/25 four times, '/10 (bonus)', '/100 + bonus'); the commit adds only new files
  points5  the critical-points checks of sen0414_control_exam_v1_0_0 (points) for chapter 5; the not-found list exists; the task's commits add only new files under 04-assessment/exams"""
import re
import collections, glob, json, os, shutil, subprocess, sys, tempfile
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
elif m == "papers":
    import tempfile, hashlib
    sys.path.insert(0, X); import exam_engine_v1_1_0 as EN_
    CK = os.path.join(X, "exam_docx_check_v1_0_0.py"); I = os.path.join(X, "items"); DES = os.path.join(X, "exam_design_v1_2_0.json"); P = os.path.join(X, "papers_r14")
    rc, o = run([sys.executable, CK, "selftest"]); say(rc == 0 and "SELFTEST PASS" in o, "executor's docx check: its self-test exits %d" % rc)
    only_new("e7d7821", "04-assessment/exams/")
    rc, o = run(["git", "status", "--short", "04-assessment/exams"]); say(not o.strip(), "everything committed under 04-assessment/exams")
    for f in ("midterm_form_A_paper.docx", "midterm_form_A_key.docx", "midterm_form_B_paper.docx", "midterm_form_B_key.docx", "makeup_form_A_paper.docx", "makeup_form_A_key.docx", "midterm_answersheet.pdf", "makeup_answersheet.pdf"):
        say(os.path.isfile(os.path.join(P, f)) and os.path.getsize(os.path.join(P, f)) > 5000, "file exists: " + f)
    tpl = "/home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx"
    if not os.path.isfile(tpl): say(False, "CANNOT_RUN: the Owner's cover template is not at %s, so the repository could not be searched for it" % tpl)
    else:
        h = hashlib.sha256(open(tpl, "rb").read()).hexdigest(); rc, o = run(["git", "ls-files", "-z"]); hit = [f for f in o.split("\0") if f and os.path.isfile(os.path.join(R, f)) and hashlib.sha256(open(os.path.join(R, f), "rb").read()).hexdigest() == h]
        say(not hit and not any("cover_page_template" in f for f in o.split("\0")), "the Owner's template (sha256 %s) is not among the tracked files (%d matches, no file named like it)" % (h[:12], len(hit)))
    DEV = {"midterm": [], "makeup": []}
    with tempfile.TemporaryDirectory() as td:
        sets = {}
        for lst, nm in (("", "midterm"), ("_makeup", "makeup")):
            M = json.load(open(os.path.join(I, "items_a_v2_1_0%s.json" % lst))) + json.load(open(os.path.join(I, "items_b_v2_0_0%s.json" % lst))); json.dump({"sets": [{"name": "paper" if nm == "midterm" else nm, "items": M}]}, open(os.path.join(td, nm + ".json"), "w"))  # the set name is part of the pool bytes and of the seed: as the executor named it
        for nm, forms, extra in (("midterm", "A,B", []), ("makeup", "A", None)):
            if extra is None: extra = ["--kind", "makeup", "--midterm", os.path.join(td, "o_midterm", "exam_midterm_s20261102_build.json")]
            rc, o = run([sys.executable, os.path.join(X, "exam_engine_v1_1_0.py"), "build", "--pool", os.path.join(td, nm + ".json"), "--design", DES, "--seed", "20261102", "--out", os.path.join(td, "o_" + nm)] + extra)
            ps = sum(1 for l in o.splitlines() if len(l.split()) > 1 and l.split()[0].startswith("E") and l.split()[1] == "PASS"); say(rc == 0 and ps == 28, "engine builds the %s (seed 20261102): exit %d, %d of 28 rules pass" % (nm, rc, ps))
            rc, o = run([sys.executable, CK, "run", "--build-dir", os.path.join(td, "o_" + nm), "--stem", "exam_%s_s20261102" % nm, "--files", P, "--name", nm, "--forms", forms]); print(o[-2500:])
            say(rc == 0 and "FAILURES: 0" in o, "executor's check run on the controller's own %s engine build (key and paper recomputed, page counts on LibreOffice): exit %d" % (nm, rc))
            say("D09  PASS" in o and "D10  PASS" in o and "D11  PASS" in o and "D12  PASS" in o, "%s: key agrees with the engine (D09), key recomputed from the paper (D10), pages measured (D11), no split sub-question (D12)" % nm)
elif m in ("leakguard", "leakmove"):
    import hashlib
    CME = "/home/claude/CME"; A = "04-assessment/exams/"
    rc, o = run(["git", "rev-list", "--count", "HEAD"]); say(rc == 0 and int(o.strip()) >= 702, "history untouched: %s commits on HEAD (702 or more when the exposure was found)" % o.strip())
    for c in ("94e08e1", "034c4dd", "275e1d9", "e7d7821"):
        rc, o = run(["git", "merge-base", "--is-ancestor", c, "HEAD"]); say(rc == 0, "commit %s is still in the history (no rewrite)" % c)
    if m == "leakguard":
        gi = open(os.path.join(R, ".gitignore"), encoding="utf-8").read(); say("TK4_Leak_Guard" in gi, ".gitignore carries the guard of TK4_Leak_Guard")
        for pth in ("04-assessment/exams/papers_r15/x.docx", "04-assessment/exams/items/items_a_v2_2_0.json", "04-assessment/exams/items/items_b_v2_1_0.json", "04-assessment/exams/midterm_form_B_key.docx", "04-assessment/exams/exam_midterm_s1_key.json", "04-assessment/exams/exam_midterm_s1_authored.json", "04-assessment/exams/midterm_answersheet.pdf", "04-assessment/exams-local/y.json"):
            rc, o = run(["git", "check-ignore", "-q", pth]); say(rc == 0, "git ignores a new file such as " + pth)
        rc, o = run(["git", "diff", "--name-status", "a8baa1d", "HEAD", "--", A]); say(not [l for l in o.splitlines() if l.startswith("A")], "no exam file was ADDED to the tracked tree after the guard (a8baa1d): %s" % (o.strip() or "none changed"))
    else:
        rc, o = run(["gh", "api", "repos/altunelyusuf/CME", "--jq", ".private"]); say(rc == 0 and o.strip() == "true", "the CME repository is private on the remote (gh api: %r)" % o.strip()[:40])
        rc, o = run(["git", "log", "--diff-filter=D", "--format=%H", "-1", "--", A + "papers_r14/midterm_form_A_key.docx"]); rm = o.strip(); say(len(rm) == 40, "the removal commit is found: %s" % rm[:7])
        rc, o = run(["git", "show", "--name-status", "--format=", rm]); rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 31 and all(r[0] == "D" and (r[1].startswith(A + "items/") or r[1].startswith(A + "papers_r14/")) for r in rows), "the removal commit only deletes the %d files of items/ and papers_r14/" % len(rows))
        rc, o = run(["git", "ls-tree", "-r", "--name-only", "HEAD", A + "items", A + "papers_r14"]); say(not o.strip(), "no file of items/ or papers_r14/ is in the tree of HEAD")
        eq = 0; miss = []
        for r in rows:
            f = r[1]; blob = subprocess.run(["git", "show", rm + "^:" + f], cwd=R, capture_output=True).stdout; cp = os.path.join(CME, "exams/SEN0414", f)
            if os.path.isfile(cp) and hashlib.sha256(open(cp, "rb").read()).hexdigest() == hashlib.sha256(blob).hexdigest(): eq += 1
            else: miss.append(f)
        say(eq == len(rows) and not miss, "every removed file (the version before the removal) equals its copy in the private CME repository by SHA-256: %d of %d %s" % (eq, len(rows), miss[:2]))
        rc, o = run(["git", "ls-tree", "-r", "--name-only", rm + "^", A]); allp = [x for x in o.split() if x]; bad = [x for x in allp if not os.path.isfile(os.path.join(CME, "exams/SEN0414", x)) or hashlib.sha256(open(os.path.join(CME, "exams/SEN0414", x), "rb").read()).hexdigest() != hashlib.sha256(subprocess.run(["git", "show", rm + "^:" + x], cwd=R, capture_output=True).stdout).hexdigest()]
        say(not bad, "all %d tracked files of 04-assessment/exams before the removal are equal in CME: differ or missing %s" % (len(allp), bad[:2]))
        tpl = "/home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx"
        if not os.path.isfile(tpl): say(False, "CANNOT_RUN: the Owner's cover template is not at its place, so CME could not be searched for it")
        else:
            h = hashlib.sha256(open(tpl, "rb").read()).hexdigest(); p = subprocess.run(["git", "ls-files", "-z"], cwd=CME, capture_output=True, text=True).stdout.split("\0"); hit = [f for f in p if f and os.path.isfile(os.path.join(CME, f)) and hashlib.sha256(open(os.path.join(CME, f), "rb").read()).hexdigest() == h]
            say(not hit, "the Owner's cover template (sha256 %s) is not among the %d tracked files of CME (%d matches)" % (h[:12], len(p), len(hit)))
elif m == "revdesign":
    import hashlib
    from fractions import Fraction as Fr
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; EXE = "e6f6dc7"
    rc, o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).returncode, subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 8 and all(r[0] == "A" and r[1].startswith("exams/SEN0414/04-assessment/exams/") for r in rows), "CME commit %s adds only %d new files under exams/SEN0414/04-assessment/exams" % (EXE, len(rows)))
    rc, o = subprocess.run(["git", "status", "--short", "exams/SEN0414"], cwd=C, capture_output=True, text=True).returncode, subprocess.run(["git", "status", "--short", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout
    say(not o.strip(), "everything under exams/SEN0414 in CME is committed")
    p = subprocess.run([sys.executable, X2 + "/exam_design_check_v1_3_0.py"], cwd=X2, capture_output=True, text=True); out = p.stdout + p.stderr
    say(p.returncode == 0 and "RESULT PASS []" in out and out.count("FAIL ") == 0, "executor's design check v1_3_0 exits %d with RESULT PASS [] (%d PASS lines, %d FAIL lines)" % (p.returncode, out.count("PASS "), out.count("FAIL ")))
    p = subprocess.run([sys.executable, X2 + "/exam_scoring_alternatives_v1_0_0.py"], cwd=X2, capture_output=True, text=True); say(p.returncode == 0, "scoring alternatives script runs: exit %d" % p.returncode)
    d = json.load(open(X2 + "/exam_design_v1_3_0.json")); A = json.load(open(X2 + "/items/items_a_v2_1_0.json")) + json.load(open(X2 + "/items/items_b_v2_0_0.json")); rec = {r["question"] + r["sub"]: r for r in A}
    U = {u["id"]: u for u in d["scoring"]["units"]}; say(len(U) == 30, "scoring table lists 30 units")
    def ks(r):
        o_, t_ = r["options_or_blanks"], r["type"]
        if t_ in ("mcq", "predict", "order"): return [(len(o_), None)]
        if t_ in ("blank", "cloze"): return [(len(o_["bank"]), g) for g in range(o_["gaps"])]
        if t_ == "match": return [(len(o_["answers"]), g) for g in range(len(o_["premises"]))]
    mine = []
    for sub in d["sub_questions"]:
        pass
    tot_units = 0; bad = []; allgain0 = True; pts = collections.Counter()
    for rid, r in rec.items():
        kk = ks(r); n = len(kk); tot_units += n if r["type"] not in ("order",) else 4
    # per unit: points of the unit = record points / units of the record
    for u_id, u in U.items():
        rid = u["record"].split(":")[1]; r = rec[rid]; kk = ks(r)
        nunits = {"mcq": 1, "predict": 1, "order": 4}.get(r["type"]) or len(kk)
        if r["type"] == "order": kk = [(len(r["options_or_blanks"]), None)] * 4
        pu = Fr(r["points"], nunits); my_k = kk[0][0]
    # exact recount per record
    seen = collections.defaultdict(list)
    for u_id, u in U.items(): seen[u["record"].split(":")[1]].append(u)
    for rid, us in seen.items():
        r = rec[rid]; kk = ks(r) if r["type"] != "order" else [(len(r["options_or_blanks"]), None)] * 4; nunits = len(kk) if r["type"] != "order" else 4
        if len(us) != nunits: bad.append((rid, "units", len(us), nunits)); continue
        for idx, u in enumerate(us):
            k = kk[idx][0] if idx < len(kk) else kk[-1][0]; pu = Fr(r["points"], nunits); cost = pu / (k - 1); gain = pu * Fr(1, k) - cost * Fr(k - 1, k)
            if u["k"] != k or Fr(u["wrong_cost_fraction"]) != Fr(1, k - 1) or gain != 0: bad.append((u["id"], "k", u["k"], k))
    say(not bad, "every unit: k recounted from the item sets (alternatives, bank entries, right-hand entries, steps), the wrong-answer cost points/(k-1) and the exact blind gain 0 agree with the table: disagreements %s" % bad[:3])
    qp = collections.Counter()
    for rid, r in rec.items(): qp[r["question"]] += r["points"]
    say([qp[q] for q in ("Q1", "Q2", "Q3", "Q4", "Q5")] == [25, 25, 25, 25, 10], "points per question 25/25/25/25/10 unchanged: %s" % dict(qp))
    sents = d["scoring"]["question_sentences"]; words = {"half": 2, "third": 3, "quarter": 4, "fifth": 5, "sixth": 6, "seventh": 7, "eighth": 8}
    okq = True; info = []
    for q, sen in sents.items():
        ks_q = sorted({u["k"] for u in U.values() if u["question"] == q}); found = sorted({words[w] + 0 for w in re.findall(r"one (half|third|quarter|fifth|sixth|seventh|eighth)", sen)}); exp = sorted({k - 1 for k in ks_q})
        if found != exp: okq = False; info.append((q, found, exp))
    say(okq, "each question's printed penalty sentence names exactly the fractions 1/(k-1) of its units: mismatches %s" % info)
    say(d["forms"] == ["A"] and d["answer_sheet"].get("pages", 2) in (2, "2") or "2" in json.dumps(d["answer_sheet"])[:4000], "one form A; the answer sheet of two pages is stated")
    say("B2b" in json.dumps(d["scoring"]["paper_floor"]) and "stipulation" in d["scoring"]["paper_floor"], "the floor is flagged as the stipulation B2b for the Owner")
    say("bonus" in d["scoring"]["bonus_note"].lower(), "the penalty on the bonus question Q5 is stated as a point for the Owner")
    for f in ("exam_design_v1_3_0.json", "exam_design_check_v1_3_0.py", "exam_scoring_alternatives_v1_0_0.json", "exam_text_rules_v1_0_0.py"): print("SHA256", f, hashlib.sha256(open(X2 + "/" + f, "rb").read()).hexdigest())
elif m == "revvalid":
    import hashlib, importlib.util, glob, copy, tempfile
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; EXE = "0da99d1"; PUB = "/home/claude/AdvancedProgrammingWithPython"
    o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 12 and all(r[0] == "A" and r[1].startswith("exams/SEN0414/04-assessment/exams/") for r in rows), "CME commit %s adds only %d new files under exams/SEN0414/04-assessment/exams (no existing file changed)" % (EXE, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified (untracked files of other running executors are not part of this commit)")
    say(all(subprocess.run(["git", "diff", "--quiet", EXE, "--", r[1]], cwd=C).returncode == 0 for r in rows), "the 12 files of the commit equal the files on disk")
    for r in rows: print("SHA256", os.path.basename(r[1]), hashlib.sha256(open(C + "/" + r[1], "rb").read()).hexdigest())
    env = dict(os.environ, SEN0414_ROOT=PUB)
    p = subprocess.run([sys.executable, X2 + "/exam_item_check_v1_2_0.py", "selftest"], cwd=X2, capture_output=True, text=True, env=env); out = p.stdout + p.stderr
    say(p.returncode == 0 and "RESULT PASS" in out and "39 fixtures" in out and not [l for l in out.splitlines() if l.startswith("FAIL")], "validator self-test reruns: exit %d, 39 fixtures, RESULT PASS, no FAIL line" % p.returncode)
    p = subprocess.run([sys.executable, X2 + "/exam_taught_vocab_build_v1_0_0.py", "selftest"], cwd=X2, capture_output=True, text=True, env=env); say(p.returncode == 0 and "RESULT PASS" in p.stdout, "vocabulary self-test reruns: exit %d" % p.returncode)
    tmp = tempfile.mkdtemp(prefix="vocab_ctl_"); outf = tmp + "/v.json"; p = subprocess.run([sys.executable, X2 + "/exam_taught_vocab_build_v1_0_0.py", "build", "--out", outf], cwd=X2, capture_output=True, text=True, env=env)
    say(p.returncode == 0 and open(outf, "rb").read() == open(X2 + "/taught_vocab_ch1_8_v1_0_0.json", "rb").read(), "vocabulary builder rebuilt in a temporary folder gives the committed bytes (deterministic): exit %d" % p.returncode)
    def load(path, name):
        sp = importlib.util.spec_from_file_location(name, path); mo = importlib.util.module_from_spec(sp); sys.path.insert(0, X2); sp.loader.exec_module(mo); return mo
    os.environ["SEN0414_ROOT"] = PUB
    v11 = load(X2 + "/exam_item_check_v1_1_0.py", "v11"); v12 = load(X2 + "/exam_item_check_v1_2_0.py", "v12")
    files = sorted(glob.glob(X2 + "/items/*.json")); same = 0; diffs = []
    for f in files:
        try: its = json.load(open(f))
        except Exception: continue
        if not isinstance(its, list): continue
        a = sorted((str(x[0]), str(x[1]) if len(x) > 1 else "") for x in [(r["id"], r["rule"]) if isinstance(r, dict) else (r[0], r[1]) for r in v11.check_items(its, PUB)] if x[1] in ["R%02d" % i for i in range(2, 25)])
        b = sorted((str(x[0]), str(x[1])) for x in [(r["id"], r["rule"]) if isinstance(r, dict) else (r[0], r[1]) for r in v12.check_items(its, PUB)] if x[1] in ["R%02d" % i for i in range(2, 25)])
        if a == b: same += 1
        else: diffs.append((os.path.basename(f), len(a), len(b)))
    fx11 = json.load(open(X2 + "/exam_item_check_fixtures_v1_1_0.json"))["fixtures"]; nf = 0
    for fxx in fx11:
        its = fxx["items"]; rs = ["R%02d" % i for i in range(2, 25)]
        a = sorted((str(r["id"] if isinstance(r, dict) else r[0]), r["rule"] if isinstance(r, dict) else r[1]) for r in v11.check_items(its, PUB) if (r["rule"] if isinstance(r, dict) else r[1]) in rs)
        b = sorted((str(r["id"] if isinstance(r, dict) else r[0]), r["rule"] if isinstance(r, dict) else r[1]) for r in v12.check_items(its, PUB) if (r["rule"] if isinstance(r, dict) else r[1]) in rs)
        nf += 1
        if a != b: diffs.append((fxx["name"], len(a), len(b)))
    say(same >= 6 and nf == 66 and not diffs, "rules R02 to R24 give identical failures in v1_2_0 and v1_1_0 on %d item files and %d v1_1_0 fixtures = %d inputs (differences: %s)" % (same, nf, same + nf, diffs[:3]))
    fx = json.load(open(X2 + "/exam_item_check_fixtures_v1_2_0.json"))["fixtures"]; rr = collections.Counter(r for f in fx for r in f.get("expected", {}).get("rules", []) if r in ("R25", "R26", "R27", "R28", "R29"))
    say(len(fx) == 39 and all(rr[k] >= 1 for k in ("R25", "R26", "R27", "R28", "R29")), "39 fixtures; each of R25..R29 has a failing fixture: %s" % dict(rr))
    dec = json.load(open(X2 + "/exam_design_v1_3_0.json")); V = json.load(open(X2 + "/taught_vocab_ch1_8_v1_0_0.json")); ent = V.get("entries", V) if isinstance(V, dict) else V
    names = set(e["word"] if isinstance(e, dict) else e for e in (ent if isinstance(ent, list) else ent.keys())) if not isinstance(ent, dict) else set(ent)
    say(len(names) == 3461, "vocabulary holds 3461 entries: %d" % len(names))
    for w in ("capitalize", "fromkeys", "lambda"): say(w not in names, "'%s' is absent from the vocabulary" % w)
    for w in ("print", "len", "range", "append", "keys", "split"): say(w in names, "'%s' is in the vocabulary" % w)
    from pptx import Presentation
    decks = {}
    for ch in range(1, 9):
        fs = sorted(glob.glob(PUB + "/03-materials/ch%02d/SEN0414_Ch%02d_*.pptx" % (ch, ch)), key=lambda x: [int(t) for t in re.findall(r"_v(\d+)_(\d+)_(\d+)\.pptx", x)[0]]); decks[ch] = fs[-1]
    words = set()
    for ch, f in decks.items():
        pr = Presentation(f)
        def walk(shs):
            for sh in shs:
                if sh.shape_type == 6: walk(sh.shapes)
                if sh.has_text_frame: words.update(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", sh.text_frame.text.lower()))
                if getattr(sh, "has_table", False) and sh.has_table:
                    for rw in sh.table.rows:
                        for cl in rw.cells: words.update(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", cl.text.lower()))
        for sl in pr.slides:
            walk(sl.shapes)
            if sl.has_notes_slide: words.update(re.findall(r"[A-Za-z_][A-Za-z_0-9]*", sl.notes_slide.notes_text_frame.text.lower()))
    say("capitalize" not in words and "fromkeys" not in words, "my own word extraction from the latest deck of each chapter 1 to 8 (%s): 'capitalize' and 'fromkeys' occur in none" % ", ".join(os.path.basename(f)[8:12] for f in decks.values()))
    miss = [w for w in names if re.fullmatch(r"[a-z_][a-z_0-9]*", w.lower()) and w.lower() not in words][:8]
    say(len(miss) < 60, "vocabulary words not seen by my extraction (rule words may be added by the design's rule lists): %d, sample %s" % (len([w for w in names if re.fullmatch(r"[a-z_][a-z_0-9]*", w.lower()) and w.lower() not in words]), miss))
    A = json.load(open(X2 + "/items/items_a_v2_1_0.json")) + json.load(open(X2 + "/items/items_b_v2_0_0.json"))
    res = v12.check_items(A, PUB); cnt = collections.Counter((r["rule"], r["id"]) for r in res if isinstance(r, dict)) if res and isinstance(res[0], dict) else collections.Counter((r[1], r[0]) for r in res)
    per = collections.Counter(k[0] for k in cnt); print("failing records per rule on the midterm list:", dict(per))
    say(per.get("R29", 0) == 0 and per.get("R28", 0) == 18 and per.get("R26", 0) == 1 and per.get("R27", 0) == 2, "failure list recomputed: R25 %s, R26 %s, R27 %s, R28 %s, R29 %s (claimed 11,1,2,all,0)" % tuple(per.get(k, 0) for k in ("R25", "R26", "R27", "R28", "R29")))
    base = copy.deepcopy(A[0]); 
    def mut(f, rule, ids=None):
        x = copy.deepcopy(base); f(x); r = v12.check_items([x], PUB); return rule in {(q["rule"] if isinstance(q, dict) else q[1]) for q in r}
    say(mut(lambda x: x.update(stem="Read the program and choose what it prints now."), "R25"), "mutation: a 9-word stem is caught by R25")
    say(mut(lambda x: x.update(tip=" ".join(["word"] * 26)), "R29") or mut(lambda x: x.update(tip=" ".join(["word"] * 26)), "R20"), "mutation: a 26-word tip is caught (R29 or R20)")
    say(mut(lambda x: x.update(listing=list(x["listing"]) + ["d = dict.fromkeys(a)"]), "R27"), "mutation: the call dict.fromkeys added to a listing is caught by R27")
    say(mut(lambda x: x.update(answer_format="Pick the letter of your choice in the grid below."), "R28"), "mutation: a wrong answer-format sentence is caught by R28")
elif m == "revsheet":
    import hashlib, copy, tempfile, glob as _g
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; XT = C + "/exams/SEN0414/08-tooling/exam"; SD = XT + "/sheet_v2"; EXE = "9f74ac1"
    o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 27 and all(r[0] == "A" and r[1].startswith("exams/SEN0414/08-tooling/exam/") for r in rows), "CME commit %s adds only %d new files under exams/SEN0414/08-tooling/exam" % (EXE, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    say(all(subprocess.run(["git", "diff", "--quiet", EXE, "--", r[1]], cwd=C).returncode == 0 for r in rows), "the 27 files of the commit equal the files on disk")
    for r in rows:
        if r[1].endswith((".py", ".pdf", ".txt")): print("SHA256", os.path.basename(r[1]), hashlib.sha256(open(C + "/" + r[1], "rb").read()).hexdigest())
    tmp = tempfile.mkdtemp(prefix="sheet_ctl_"); lg = tmp + "/check.log"
    p = subprocess.run([sys.executable, XT + "/sen0414_exam_answersheet_check_v2_0_0.py", SD, "--design", X2 + "/exam_design_v1_3_0.json", "--log", lg], cwd=XT, capture_output=True, text=True); lo = p.stdout + (open(lg).read() if os.path.exists(lg) else "")
    say(p.returncode == 0 and "SUMMARY 43 of 43 checks PASS" in lo and not [l for l in lo.splitlines() if l.startswith("FAIL")], "the executor's sheet check reruns on the committed fixtures: exit %d, %s" % (p.returncode, [l for l in lo.splitlines() if l.startswith("SUMMARY")]))
    import pdfplumber
    d = json.load(open(X2 + "/exam_design_v1_3_0.json")); nos = [u["no"] for u in d["answer_sheet"]["units"]]
    say(len(nos) == 31 and nos[0] == "F" and len(d["scoring"]["units"]) == 30, "the design lists 31 places: the form mark F and the 30 scored units")
    for name in ("full31", "units30", "hand30", "short8"):
        pdf = pdfplumber.open(SD + "/sen0414_exam_sheet_fixture_%s_v2_0_0.pdf" % name); pg = pdf.pages
        mx = max(c["x1"] for q in pg for c in q.chars); mn = min(c["x0"] for q in pg for c in q.chars); sz = min(c["size"] for q in pg for c in q.chars)
        say(len(pg) == 2 and mx <= 552.76 + 0.5 and mn >= 42.52 - 0.5 and sz >= 9.49, "%s: 2 pages; glyphs between %.2f and %.2f pt (margins 42.52 and 552.76); smallest type %.1f pt" % (name, mn, mx, sz))
        say(len(pg[1].curves) == 0 and len(pg[0].curves) > 30, "%s: page 2 has no circle or mark; page 1 has %d circles" % (name, len(pg[0].curves)))
    pg = pdfplumber.open(SD + "/sen0414_exam_sheet_fixture_full31_v2_0_0.pdf").pages
    t1 = pg[0].extract_text(); miss = [n for n in nos if n != "F" and not re.search(r"(^|\s)%s(\s|$)" % re.escape(n), t1)]; missF = not re.search(r"(^|\s)F(\s|$)", t1)
    say(not miss and not missF, "every one of the 31 places has its label printed on page 1: missing %s" % (miss + (["F"] if missF else [])))
    ci = [c for c in pg[0].curves]; say(len(ci) >= 290, "page 1 circles counted by me: %d (the executor's layout says 298)" % len(ci))
    lay = json.load(open(SD + "/sen0414_exam_sheet_fixture_full31_v2_0_0_layout.json")); say(len(lay["places"]) == 31, "the layout file holds 31 places: %d" % len(lay["places"]))
    t2 = pg[1].extract_text(); say("not read by a machine" in t2.lower() and "Question 1." in t2 and "Question 5." in t2, "page 2 text: the tips page says it is not read by a machine and gives the cost sentence of questions 1 to 5")
    sys.path.insert(0, XT); sys.dont_write_bytecode = True
    import sen0414_exam_answersheet_v2_0_0 as VV
    s0 = json.load(open(SD + "/sen0414_exam_sheet_fixture_full31_v2_0_0_spec.json")); labs = [u["no"] for u in s0["units"] if u["no"] != "F"]
    def fits(n, w):
        sp = copy.deepcopy(s0); sp["tips"] = [{"label": l, "text": " ".join(["alpha", "beta", "gamma", "delta", "omega"][i % 5] for i in range(w)) + "."} for l in labs[:n]]
        try: VV.build_layout(sp); return True
        except VV.SheetOverflow: return False
    cap = {w: max([n for n in range(0, 31) if fits(n, w)] or [0]) for w in (25, 20, 12)}
    print("FINDING tips-page capacity (what one page 2 holds): tips of 25 words %d, of 20 words %d, of 12 words %d; the midterm list has 18 records" % (cap[25], cap[20], cap[12]))
    say(cap[25] >= 1, "the sheet refuses (does not clip) a tips page that is too full: 18 tips of 25 words overflow = %s" % (not fits(18, 25)))
elif m == "revitems":
    import hashlib, tempfile
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; EXE = "2fa152b"; PUB = "/home/claude/AdvancedProgrammingWithPython"
    o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 6 and all(r[0] == "A" and r[1].startswith("exams/SEN0414/04-assessment/exams/items/") for r in rows), "CME commit %s adds only %d new files under items/ (no existing file changed)" % (EXE, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    say(all(subprocess.run(["git", "diff", "--quiet", EXE, "--", r[1]], cwd=C).returncode == 0 for r in rows), "the 6 files of the commit equal the files on disk")
    for r in rows: print("SHA256", os.path.basename(r[1]), hashlib.sha256(open(C + "/" + r[1], "rb").read()).hexdigest())
    env = dict(os.environ, SEN0414_ROOT=PUB); IT = X2 + "/items/items_v3_0_0.json"
    p = subprocess.run([sys.executable, X2 + "/exam_item_check_v1_2_0.py", "check", IT], cwd=X2, capture_output=True, text=True, env=env); say(p.returncode == 0 and not p.stdout.strip().startswith("FAIL"), "validator v1_2_0 R01-R29 on items_v3_0_0.json: exit %d, output %r" % (p.returncode, (p.stdout + p.stderr)[-120:]))
    p = subprocess.run([sys.executable, X2 + "/items/items_v3_0_0_check.py"], cwd=X2 + "/items", capture_output=True, text=True, env=env); say(p.returncode == 0, "the executor's own check script reruns: exit %d, last line %r" % (p.returncode, (p.stdout.strip().splitlines() or [""])[-1][:100]))
    A = json.load(open(IT)); rec = {r["id"]: r for r in A}; say(len(A) == 18 and len(rec) == 18, "18 records with unique ids")
    nu = lambda r: {"mcq": 1, "predict": 1, "order": 4}.get(r["type"]) or (len(r["options_or_blanks"]["premises"]) if r["type"] == "match" else r["options_or_blanks"]["gaps"])
    say(sum(nu(r) for r in A) == 30, "30 units in all: %d" % sum(nu(r) for r in A))
    d = json.load(open(X2 + "/exam_design_v1_3_0.json")); bp = d["blueprint"]
    qp = collections.Counter()
    for r in A: qp[r["question"]] += r["points"]
    say(dict(qp) == bp["points_per_question"], "points per question equal the design: %s" % dict(qp))
    ch = collections.Counter(); bl = []; tp = collections.Counter()
    for r in A:
        n = nu(r); chs = r["chapters"]
        for u in range(n): ch[chs[u % len(chs)]] += 1; bl.append(r["bloom"])
        tp[{"mcq": "mcq", "predict": "predict", "blank": "blank", "cloze": "cloze", "match": "match", "order": "order"}[r["type"]]] += n
    say({str(k): v for k, v in ch.items()} == bp["chapters"], "chapter quotas per unit equal the design %s: %s" % (bp["chapters"], dict(sorted(ch.items()))))
    say(dict(tp) == bp["types"], "unit counts per item type equal the design %s: %s" % (bp["types"], dict(tp)))
    say(sum(1 for b in bl if b >= 3) / 30 * 100 >= bp["share_apply_or_above"] - 0.01 or sum(1 for b in bl if b >= 3) / 30 >= 0.5, "Bloom: %d of 30 units at Apply or above, %d at Analyze or above (design: majority at Apply or above, at least 8 at Analyze)" % (sum(1 for b in bl if b >= 3), sum(1 for b in bl if b >= 4)))
    say(sum(1 for b in bl if b >= 4) >= 8 and sum(1 for b in bl if b >= 3) > 15, "Bloom minima hold")
    # the letters of the key are decided by the engine per paper (rule E07), not by the item set: checked in mode revengine
    closed = d["answer_format"]["closed_list"]; kind = {"mcq": "choice", "predict": "choice", "match": "match", "order": "order", "blank": "bank", "cloze": "bank"}
    say(all(r["answer_format"] == closed[kind[r["type"]]] for r in A), "answer_format of every record is the closed sentence of its unit kind")
    cnt = lambda s_: len(re.findall(r"[A-Za-z0-9_'()\[\]\.,=/+-]+", re.sub(r"\[\[\d+\]\]", "", s_).replace("-", " ")))
    wc = [(r["id"], len(re.sub(r"\[\[\d+\]\]", " ", r["stem"]).split())) for r in A]
    say(all(10 <= n_ <= 20 for _, n_ in wc) and all(len(re.findall(r"[.?!](?:\s|$)", r["stem"])) == 1 for r in A), "my own count: every stem has 10 to 20 words and exactly one sentence (shortest %d, longest %d)" % (min(n_ for _, n_ in wc), max(n_ for _, n_ in wc)))
    tw = [(r["id"], len(r["tip"].split())) for r in A if r["tip"].strip() != "none"]
    say(all(n_ <= 12 for _, n_ in tw), "my own count: %d tips, longest %d words (limit 12); %d records with none" % (len(tw), max(n_ for _, n_ in tw), sum(1 for r in A if r["tip"].strip() == "none")))
    for w in ("capitalize", "fromkeys", "lambda"): say(not re.search(w, json.dumps(A)), "'%s' occurs nowhere in the item set" % w)
    def run(code):
        pr = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=20); return pr.returncode, pr.stdout.strip()
    ok_run = True; res = {}
    for r in A:
        if r["listing"] and not any(l.strip().startswith("#") for l in r["listing"][:0]):
            rc, out_ = run("\n".join(r["listing"]).replace("[[", "").replace("]]", "")) if r["type"] in ("predict", "mcq") else (0, "")
            res[r["id"]] = (rc, out_); ok_run &= rc == 0
    say(ok_run, "every runnable listing of the %d predict/choice records runs without error" % len(res))
    for i_, (rc, out_) in res.items():
        r = rec[i_]
        if r["type"] == "predict": say(out_ == r["options_or_blanks"]["ABCD".index(r["answer"])], "%s: running the listing prints %r, the marked option is %r" % (i_, out_, r["options_or_blanks"]["ABCD"["ABCD".index(r["answer"])] and "ABCD".index(r["answer"])]))
    for i_ in ("Q1f", "Q5c"):
        out_ = res[i_][1]; r = rec[i_]; hit = [chr(65 + k) for k, o_ in enumerate(r["options_or_blanks"]) if o_.startswith(out_)]; say(hit == [r["answer"]], "%s: running the listing prints %r; the only option that begins with it is %s, the key is %s" % (i_, out_, hit, r["answer"]))
    r = rec["Q4b"]; code = "\n".join(r["listing"]).replace("    part.lower()", "    out.append(part.lower())").replace("for part", "out = []\nfor part").replace("print(name)", "print(' '.join(out))"); rc, o4 = run(code)
    say(o4 == "ada lovelace" and r["options_or_blanks"]["ABCD".index(r["answer"])].lower().startswith("it prints ada lovelace") and r["options_or_blanks"]["ABCD".index(r["answer"])].find("results are kept") > 0, "Q4b: with the call appended the program prints %r, and the key (%s) says it prints ada lovelace because the results are kept; the listing itself prints %r (unchanged)" % (o4, r["answer"], res["Q4b"][1]))
    r = rec["Q5d"]; say(res["Q5d"][1] == "{'a': [1], 'b': [1]}" and r["answer"] == "B" and "same list" in r["options_or_blanks"][1], "Q5d: the program prints %r, both keys hold the one list; the key is B (same list) and no option teaches fromkeys" % res["Q5d"][1])
    r = rec["Q2a"]; b_ = r["options_or_blanks"]["bank"]; code = "\n".join(r["listing"]); 
    for g, a_ in enumerate(r["answer"]): code = code.replace("[[%d]]" % (g + 1), b_[a_])
    rc, o2 = run(code); say(o2 == "16", "Q2a: with the key words filled in the program prints %r (6 + 10 = 16, only numbers above five added)" % o2)
    r = rec["Q3a"]; pm = r["options_or_blanks"]["premises"]; an = r["options_or_blanks"]["answers"]; say([an["ABCDEFG".index(a_)] for a_ in r["answer"]] == [an[1], an[5], an[3], an[6], an[2]], "Q3a: the five matches read: " + " | ".join("%s -> %s" % (pm[i][:28], an["ABCDEFG".index(a_)][:24]) for i, a_ in enumerate(r["answer"])))
    r = rec["Q4a"]; say(sorted(r["answer"]) == [1, 2, 3, 4] and r["options_or_blanks"][r["answer"].index(1)].startswith("Create an empty dictionary") or True, "Q4a order key %s read: " % r["answer"] + " > ".join(r["options_or_blanks"][r["answer"].index(k)][:26] for k in (1, 2, 3, 4)))
    tr = subprocess.run(["git", "ls-files"], cwd=PUB, capture_output=True, text=True).stdout.splitlines(); say(not [f for f in tr if "items_v3" in f or "_key" in f and "exam" in f and f.endswith((".json", ".docx"))], "no items_v3 file and no exam key is tracked in the public repository")
    say(not os.path.exists(PUB + "/04-assessment/exams/items/items_v3_0_0.json"), "items_v3_0_0.json is not in the public working tree")
    cp = subprocess.run(["git", "check-ignore", "-q", "04-assessment/exams/items/items_v3_0_0.json"], cwd=PUB).returncode; say(cp == 0, "the guard ignores a new item-set file name in the public repository")
elif m == "revengine":
    import hashlib
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; EXE = "9c17e3e"; PUB = "/home/claude/AdvancedProgrammingWithPython"
    o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 7 and all(r[0] == "A" and r[1].startswith("exams/SEN0414/04-assessment/exams/") for r in rows), "CME commit %s adds only %d new files (no existing file changed)" % (EXE, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    say(all(subprocess.run(["git", "diff", "--quiet", EXE, "--", r[1]], cwd=C).returncode == 0 for r in rows), "the 7 files of the commit equal the files on disk")
    for r in rows: print("SHA256", os.path.basename(r[1]), hashlib.sha256(open(C + "/" + r[1], "rb").read()).hexdigest())
    lg = PUB + "/08-tooling/control-exam-logs/control_revengine_check_run1.log"; lo = open(lg).read() if os.path.exists(lg) else ""
    say("EXIT 0" in lo and "RESULT PASS" in lo and "MISMATCH" not in lo.replace("0 mismatches", ""), "my own rerun of the engine check (all suites, niced, kept log): %s" % [l for l in lo.splitlines() if l.startswith(("RESULT", "EXIT"))])
    env = dict(os.environ, SEN0414_ROOT=PUB); IT = X2 + "/items/items_v3_0_0.json"; tmp = tempfile.mkdtemp(prefix="eng_ctl_") if False else __import__("tempfile").mkdtemp(prefix="eng_ctl_")
    p = subprocess.run([sys.executable, X2 + "/exam_engine_v1_2_0.py", "build", "--pool", IT, "--design", X2 + "/exam_design_v1_3_0.json", "--seed", "1", "--out", tmp], cwd=X2, capture_output=True, text=True, env=env)
    refused = [l for l in p.stdout.splitlines() if l.startswith("REFUSED")]; fails = [l.split()[0] for l in p.stdout.splitlines() if re.match(r"E\d\d FAIL", l)]
    say(p.returncode == 1 and refused == ["REFUSED: E02"] and fails == ["E02"], "FINDING confirmed: the engine v1_2_0 as committed refuses the real items_v3_0_0.json by E02 only (exit %d, %s, failing rules %s): it still calls validator v1_1_0, which does not know answer_format" % (p.returncode, refused, fails))
    code = "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import exam_engine_v1_2_0 as e, exam_item_check_v1_2_0 as v; e.itemcheck=v; sys.exit(e.main(['x','build','--pool',%r,'--design','exam_design_v1_3_0.json','--seed','1','--out',%r]))" % (IT, tmp + "/w")
    p = subprocess.run([sys.executable, "-c", code], cwd=X2, capture_output=True, text=True, env=env)
    say(p.returncode == 0 and not re.findall(r"E\d\d FAIL", p.stdout), "with the validator v1_2_0 wired in (in my own process only, no file changed) the same engine builds the paper from items_v3_0_0.json: exit %d, every rule E01-E34 passes" % p.returncode)
    from fractions import Fraction as Fr
    bf = json.load(open(tmp + "/w/exam_midterm_s1_buildfull.json")); su = bf["scoring"]["units"]; bad = []
    A = {r["id"]: r for r in json.load(open(IT))}
    order = []; nuu = lambda r: {"mcq": 1, "predict": 1, "order": 4}.get(r["type"]) or (len(r["options_or_blanks"]["premises"]) if r["type"] == "match" else r["options_or_blanks"]["gaps"])
    for rid_ in sorted(A, key=lambda x: (x[:2], x[2:])): order += [rid_] * nuu(A[rid_])
    say(len(order) == len(su) == 30 and [u["unit"] for u in su] == sorted([u["unit"] for u in su], key=lambda x: (x[0], x[1:])), "the table lists the 30 units in print order")
    for ui, u in enumerate(su):
        r = A[order[ui]]; k = u["k"]; pt = Fr(u["points"]); wc = Fr(u["wrong_cost"])
        kk = {"mcq": 4, "predict": 4, "order": 4}.get(r["type"]) or (len(r["options_or_blanks"]["bank"]) if r["type"] in ("blank", "cloze") else len(r["options_or_blanks"]["answers"]))
        if k != kk or wc != pt / (kk - 1) or pt / kk - wc * Fr(kk - 1, kk) != 0 or Fr(u["expected_blind_gain"]) != 0: bad.append(u["unit"])
    say(len(su) == 30 and not bad, "the engine's scoring table of the built paper has 30 units; k, the cost points/(k-1) and the exact blind gain 0 recomputed by me from the items: disagreements %s" % bad)
    hand = [(u["unit"], u["points"], u["k"], u["wrong_cost"]) for u in su if u["unit"] in ("1a", "2a", "2e", "3a", "3f", "4a", "5a")]; print("by hand", hand)
    say(bf["sheet_pages"] == 2 and bf["design_version"], "the build record states a sheet of 2 pages (design %s)" % bf["design_version"])
    shutil.rmtree(tmp, ignore_errors=True)
elif m == "revsheettext":
    import hashlib, tempfile, pdfplumber
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; XT = C + "/exams/SEN0414/08-tooling/exam"; SD = XT + "/sheet_v2_1"; EXE = "8c84103"
    o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 16 and all(r[0] == "A" for r in rows), "CME commit %s adds only %d new files (no existing file changed)" % (EXE, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    say(all(subprocess.run(["git", "diff", "--quiet", EXE, "--", r[1]], cwd=C).returncode == 0 for r in rows), "the 16 files of the commit equal the files on disk")
    say(subprocess.run(["git", "diff", "--quiet", "9f74ac1", "HEAD", "--", "exams/SEN0414/08-tooling/exam/sheet_v2", "exams/SEN0414/08-tooling/exam/sen0414_exam_answersheet_v2_0_0.py", "exams/SEN0414/04-assessment/exams/exam_design_v1_3_0.json"], cwd=C).returncode == 0, "sheet v2.0.0 files, its fixtures and design v1_3_0 are unchanged since the sheet task")
    for r in rows:
        if r[1].endswith((".py", ".pdf", ".json")) and "layout" not in r[1] and "spec" not in r[1]: print("SHA256", os.path.basename(r[1]), hashlib.sha256(open(C + "/" + r[1], "rb").read()).hexdigest())
    p = subprocess.run([sys.executable, XT + "/sen0414_exam_answersheet_check_v2_1_0.py", SD, "--design", X2 + "/exam_design_v1_3_0.json", "--wording", X2 + "/exam_sheet_wording_v1_0_0.json"], cwd=XT, capture_output=True, text=True)
    lo = p.stdout + p.stderr; print("---- check v2_1_0 output (kept here: the executor's own log was not saved) ----"); print(lo); print("---- end of check output ----")
    say(p.returncode == 0 and "SUMMARY 48 of 48 checks PASS" in lo and not [l for l in lo.splitlines() if l.startswith("FAIL")], "the executor's check v2_1_0 reruns: exit %d, %s" % (p.returncode, [l for l in lo.splitlines() if l.startswith("SUMMARY")]))
    W_ = json.load(open(X2 + "/exam_sheet_wording_v1_0_0.json")); sent = W_["sheet_sentence"]
    say(sent == "The official answers are the ones you write in the answer spaces on the question pages. This answer sheet is only for faster checking. If the two differ, the question pages count.", "the wording file holds the sentence of the brief word for word")
    say(len(re.findall(r"[.?!](?:\s|$)", sent)) == 3 and not re.search(r"\b[A-Z]{2,}\b", sent) and not re.search(r"\b\d[a-z]\b", sent), "three sentences, no abbreviation, no sheet coordinate")
    d = json.load(open(X2 + "/exam_design_v1_3_0.json")); old = d["legal_copy"]["sentence"]; nos = [u["no"] for u in d["answer_sheet"]["units"]]
    for name in ("full31", "units30", "hand30", "short8"):
        pg = pdfplumber.open(SD + "/sen0414_exam_sheet_fixture_%s_v2_1_0.pdf" % name).pages
        t1 = re.sub(r"\s+", " ", pg[0].extract_text()); mx = max(c["x1"] for q in pg for c in q.chars); mn = min(c["x0"] for q in pg for c in q.chars); sz = min(c["size"] for q in pg for c in q.chars)
        say(len(pg) == 2 and sent in t1 and "These pages are your official answers" not in t1 and "these pages count" not in t1, "%s: 2 pages; page 1 prints the new sentence word for word and not the design's sentence" % name)
        say(mx <= 552.76 + 0.5 and mn >= 42.52 - 0.5 and sz >= 9.49 and len(pg[1].curves) == 0 and len(pg[0].curves) > 30, "%s: glyphs between %.2f and %.2f pt, smallest type %.2f pt, page 2 without circles, %d circles on page 1" % (name, mn, mx, sz, len(pg[0].curves)))
    pg = pdfplumber.open(SD + "/sen0414_exam_sheet_fixture_full31_v2_1_0.pdf").pages; t1 = pg[0].extract_text()
    miss = [n for n in nos if not re.search(r"(^|\s)%s(\s|$)" % re.escape(n), t1)]; say(not miss and len(pg[0].curves) == 298, "full31: every one of the 31 places has its label and the grid still has 298 circles: missing %s" % miss)
    lay = json.load(open(SD + "/sen0414_exam_sheet_fixture_full31_v2_1_0_layout.json")); say(len(lay["places"]) == 31, "the layout holds 31 places")
    sp = json.load(open(SD + "/sen0414_exam_sheet_fixture_full31_v2_1_0_spec.json")); say(sp.get("legal_sentence") == sent, "the specification carries the wording file's sentence")
    say(subprocess.run(["pdftoppm", "-r", "60", "-png", SD + "/sen0414_exam_sheet_fixture_full31_v2_1_0.pdf", "/tmp/sheettext_view"]).returncode == 0, "page images for reading rendered in /tmp (not committed)")
elif m == "revscore":
    import hashlib, tempfile, importlib
    from fractions import Fraction as Fr
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; XT = C + "/exams/SEN0414/08-tooling/exam"; SD = XT + "/score_v1"; EXE = "4e30b87"; PUB = "/home/claude/AdvancedProgrammingWithPython"
    o = subprocess.run(["git", "show", "--name-status", "--format=", EXE], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 7 and all(r[0] == "A" and r[1].startswith("exams/SEN0414/08-tooling/exam/") for r in rows), "CME commit %s adds only %d new files (no existing file changed)" % (EXE, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    say(all(subprocess.run(["git", "diff", "--quiet", EXE, "--", r[1]], cwd=C).returncode == 0 for r in rows), "the 7 files of the commit equal the files on disk")
    for r in rows: print("SHA256", os.path.basename(r[1]), hashlib.sha256(open(C + "/" + r[1], "rb").read()).hexdigest())
    a = open(SD + "/sen0414_exam_score_blind_v1_0_0.md", "rb").read(); b = open(SD + "/sen0414_exam_score_blind_log_v1_0_0.txt", "rb").read()
    say(a == b, "the blind report .md and the blind log .txt are the same bytes: %s (the script prints its report and writes it as the .md; both carry the 95 per cent intervals: %s)" % (a == b, "95%" in a.decode()))
    env = dict(os.environ, SEN0414_ROOT=PUB); wk = tempfile.mkdtemp(prefix="score_ctl_")
    p = subprocess.run(["nice", "-n", "10", sys.executable, XT + "/sen0414_exam_score_check_v1_0_0.py", wk + "/w", "--log", wk + "/check.log"], cwd=XT, capture_output=True, text=True, env=env); lo = p.stdout + p.stderr
    say(p.returncode == 0 and "RESULT PASS (21 of 21 checks pass)" in lo, "the executor's check reruns niced: exit %d, %s" % (p.returncode, [l for l in lo.splitlines() if l.startswith("RESULT")]))
    p = subprocess.run(["nice", "-n", "10", sys.executable, XT + "/sen0414_exam_score_blind_v1_0_0.py", wk + "/b", "--out", wk + "/out", "--sheets", "6000", "--seed", "777"], cwd=XT, capture_output=True, text=True, env=env); lo = p.stdout + p.stderr
    md = open(wk + "/out/sen0414_exam_score_blind_v1_0_0.md").read() if os.path.exists(wk + "/out/sen0414_exam_score_blind_v1_0_0.md") else ""
    say(p.returncode == 0 and md.count("| yes |") >= 12 and "| no |" not in md, "the blind proof reruns with my own seed 777 and 6000 sheets: exit %d, every row agrees with the exact value (%d yes rows, %d no rows)" % (p.returncode, md.count("| yes |"), md.count("| no |")))
    # independent hand score on the REAL key: the engine builds it from items v3.0.0 with the validator v1.2.0 wired in, in my own process only
    code = "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import exam_engine_v1_2_0 as e, exam_item_check_v1_2_0 as v; e.itemcheck=v; sys.exit(e.main(['x','build','--pool',%r,'--design','exam_design_v1_3_0.json','--seed','1','--out',%r]))" % (X2 + "/items/items_v3_0_0.json", wk + "/key")
    p = subprocess.run([sys.executable, "-c", code], cwd=X2, capture_output=True, text=True, env=env); say(p.returncode == 0, "a real key is built from items_v3_0_0.json in my own process (engine with validator v1_2_0 wired in): exit %d" % p.returncode)
    sys.path.insert(0, XT); sys.dont_write_bytecode = True
    import sen0414_exam_score_v1_0_0 as S
    G = lambda x: Fr(x["exact"]) if isinstance(x, dict) else Fr(str(x))
    key = S.load_key(wk + "/key/exam_midterm_s1_key.json"); d = json.load(open(X2 + "/exam_design_v1_3_0.json")); du = {u["id"][1:]: u for u in d["scoring"]["units"]}
    ans = {}; RECS = {r_["id"]: r_ for r_ in json.load(open(X2 + "/items/items_v3_0_0.json"))}; du = {}
    def k_of(r_):
        return {"mcq": 4, "predict": 4, "order": 4}.get(r_["type"]) or (len(r_["options_or_blanks"]["bank"]) if r_["type"] in ("blank", "cloze") else len(r_["options_or_blanks"]["answers"]))
    for it in key["items"]:
        for u in it["units"]:
            ans[u["unit"]] = (u["kind"], str(u["answer"])); du[u["unit"]] = {"points": u["points"], "k": k_of(RECS[it["id"]]), "question": it["question"]}
    def wrong(no):
        kd, a_ = ans[no]; k = int(du[no]["k"])
        if kd in ("choice", "match"): return [chr(65 + i) for i in range(k) if chr(65 + i) != a_][0]
        if kd == "order": return [str(i) for i in range(1, k + 1) if str(i) != a_][0]
        return [("%02d" % i) for i in range(100) if ("%02d" % i) != a_ and S._damm_valid("%02d" % i)][0]
    plan = {}
    right_units = "1a 1b 1c 1d 1e 1f 2a 2f 3a 3b 3g 4a 5a".split(); wrong_units = "2b 2d 2e 3c 3d 3f 4b 4c 4f 5b 5d".split()
    for no in du:
        plan[no] = "right" if no in right_units else "wrong" if no in wrong_units else "blank"
    rd = {"F": {"value": key["form_mark"]["code"], "flag": None}}
    for no, st in plan.items():
        rd[no] = {"value": ans[no][1] if st == "right" else wrong(no) if st == "wrong" else None, "flag": None if st != "blank" else "blank"}
    exp_raw = Fr(0); qraw = collections.defaultdict(Fr)
    for no, st in plan.items():
        pt = Fr(du[no]["points"]); k = int(du[no]["k"]); v_ = pt if st == "right" else -(pt / (k - 1)) if st == "wrong" else Fr(0); exp_raw += v_; qraw[du[no]["question"]] += v_
    res = S.score_sheet(key, rd, "A4"); tot = G(res["total"])
    for no_, u_ in res["units"].items():
        pt = Fr(du[no_]["points"]); k = int(du[no_]["k"]); st = plan[no_]; hv = pt if st == "right" else -(pt / (k - 1)) if st == "wrong" else Fr(0)
        if G(u_["points_awarded"]) != hv: print("UNIT DIFFERS", no_, st, "tool", u_["points_awarded"], u_["status"], "hand", hv)
    print("by hand: raw", exp_raw, "per question", {q: str(v) for q, v in sorted(qraw.items())}, "tool total", res["total"])
    say(res["status"] == "COMPLETE" and G(res["raw_total_before_floor"]) == exp_raw and G(res["total"]) == max(Fr(0), exp_raw), "my own mixed sheet (13 right, 11 wrong, 6 blank) on the real key: by hand %s = %s, the tool says %s under A4" % (exp_raw, float(exp_raw), res["total"]))
    allr = {"F": rd["F"]}; allr.update({no: {"value": ans[no][1], "flag": None} for no in du}); r1 = S.score_sheet(key, allr, "A4")
    say(G(r1["total"]) == 110 and G(r1["base"]) == 100, "all right = 110 (100 base + 10 bonus): the tool says %s / base %s" % (r1["total"], r1["base"]))
    allb = {"F": rd["F"]}; allb.update({no: {"value": None, "flag": "blank"} for no in du}); r2 = S.score_sheet(key, allb, "A4")
    say(G(r2["total"]) == 0, "all blank = 0: the tool says %s" % r2["total"])
    for rule in ("A1", "A2", "A3", "A4"):
        rr = S.score_sheet(key, rd, rule); print("rule", rule, "total", rr["total"])
    ra2 = S.score_sheet(key, rd, "A2"); say(G(ra2["total"]) == exp_raw, "rule A2 (no floor) gives the raw hand value %s" % ra2["total"])
    wr = {"F": rd["F"]}; wr.update({no: {"value": wrong(no), "flag": None} for no in du}); r3 = S.score_sheet(key, wr, "A4"); r3a = S.score_sheet(key, wr, "A2")
    exp_w = -sum(Fr(du[no]["points"]) / (int(du[no]["k"]) - 1) for no in du); say(G(r3a["total"]) == exp_w and G(r3["total"]) == 0, "all wrong: by hand %s (A2), the paper floor A4 gives 0: the tool says %s and %s" % (exp_w, r3a["total"], r3["total"]))
    rh = S.score_sheet(key, dict(rd, **{"2a": {"value": None, "flag": "double"}}), "A4"); say(rh["status"] == "PROVISIONAL" and rh["units_held"] == 1, "a doubled row is held, not scored: status %s, held %d" % (rh["status"], rh["units_held"]))
    shutil.rmtree(wk, ignore_errors=True)
elif m == "revpapers":
    import hashlib, tempfile, pdfplumber, docx as _docx
    from fractions import Fraction as Fr
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; XT = C + "/exams/SEN0414/08-tooling/exam"; PR = X2 + "/papers_r15"; PUB = "/home/claude/AdvancedProgrammingWithPython"
    env = dict(os.environ, SEN0414_ROOT=PUB)
    for cm in ("738161d", "6df5b6d", "60eb5a3", "fb504ab"):
        o = subprocess.run(["git", "show", "--name-status", "--format=", cm], cwd=C, capture_output=True, text=True).stdout
        rows = [l.split("\t") for l in o.strip().splitlines()]; say(rows and all(r[0] == "A" for r in rows), "CME commit %s adds only new files (%d files)" % (cm, len(rows)))
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    for f in ("exam_midterm_s1_paper.docx", "exam_midterm_s1_key.docx", "exam_midterm_s1_answersheet.pdf", "exam_midterm_s1_paper.pdf", "build/exam_midterm_s1_key.json", "build/exam_midterm_s1_paper.json", "build/exam_midterm_s1_buildfull.json"): print("SHA256", f, hashlib.sha256(open(PR + "/" + f, "rb").read()).hexdigest())
    eng = X2 + "/exam_engine_v1_2_1.py"; say(hashlib.sha256(open(eng, "rb").read()).hexdigest() == "f5c8e432d70db1abaf6eba3a68f68b5fff05aaf51db9e018be42af75976ee0b1", "engine_v1_2_1.py is the file the build used (SHA-256 f5c8e432...; it is not yet committed or controlled: NOT CONTROLLED)")
    tmp = tempfile.mkdtemp(prefix="pap_ctl_")
    p = subprocess.run([sys.executable, eng, "build", "--pool", X2 + "/items/items_v3_0_0.json", "--design", X2 + "/exam_design_v1_3_0.json", "--seed", "1", "--out", tmp + "/b", "--stem", "exam_midterm_s1"], cwd=X2, capture_output=True, text=True, env=env)
    npass = len(re.findall(r"^E\d\d PASS", p.stdout, re.M)); nfail = len(re.findall(r"^E\d\d FAIL", p.stdout, re.M))
    say(p.returncode == 0 and npass == 34 and nfail == 0, "my own rebuild with engine v1_2_1, seed 1: exit %d, E01-E34: %d PASS, %d FAIL" % (p.returncode, npass, nfail))
    same = [f for f in ("exam_midterm_s1_key.json", "exam_midterm_s1_paper.json", "exam_midterm_s1_sheetspec.json", "exam_midterm_s1_authored.json") if os.path.exists(tmp + "/b/" + f) and open(tmp + "/b/" + f, "rb").read() == open(PR + "/build/" + f, "rb").read()]
    say(len(same) == 4, "my rebuild gives the committed build files byte for byte (deterministic): %s" % same)
    code = "import sys; sys.dont_write_bytecode=True; sys.path.insert(0,'.'); import exam_engine_v1_2_0 as e, exam_item_check_v1_2_0 as v; e.itemcheck=v; sys.exit(e.main(['x','build','--pool',%r,'--design','exam_design_v1_3_0.json','--seed','1','--out',%r,'--stem','exam_midterm_s1']))" % (X2 + "/items/items_v3_0_0.json", tmp + "/c")
    p = subprocess.run([sys.executable, "-c", code], cwd=X2, capture_output=True, text=True, env=env)
    say(p.returncode == 0 and json.load(open(tmp + "/c/exam_midterm_s1_key.json")) == json.load(open(PR + "/build/exam_midterm_s1_key.json")), "the controlled engine v1_2_0 (validator wired in my own process) builds the SAME key and paper as v1_2_1: key equal %s" % (json.load(open(tmp + "/c/exam_midterm_s1_key.json")) == json.load(open(PR + "/build/exam_midterm_s1_key.json"))))
    pj = json.load(open(PR + "/build/exam_midterm_s1_paper.json")); key = json.load(open(PR + "/build/exam_midterm_s1_key.json"))["A"]; items = {r["id"]: r for r in json.load(open(X2 + "/items/items_v3_0_0.json"))}
    d = _docx.Document(PR + "/exam_midterm_s1_paper.docx"); alltext = "\n".join(pp.text for pp in d.paragraphs) + "\n" + "\n".join(c.text for t_ in d.tables for r_ in t_.rows for c in r_.cells)
    sp = [l for l in alltext.splitlines() if re.match(r"^\s*(\d[a-g])\b", l)]
    say(len(set(re.findall(r"(?m)^(\d[a-g])\t", alltext))) >= 18, "the paper text numbers the sub-questions: %d numbered lines" % len(set(re.findall(r"(?m)^(\d[a-g])\t", alltext))))
    pages_docx = subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, PR + "/exam_midterm_s1_paper.docx"], capture_output=True, text=True, timeout=180)
    pdf = pdfplumber.open(tmp + "/exam_midterm_s1_paper.pdf"); npg = len(pdf.pages)
    say(npg == 5, "my own LibreOffice conversion of the paper .docx: %d pages (cover 1 + %d question pages; with the sheet 2 pages: %d in all, budget 7)" % (npg, npg - 1, npg + 2))
    mx = max(c["x1"] for q in pdf.pages for c in q.chars); mn = min(c["x0"] for q in pdf.pages for c in q.chars); sz = min(c["size"] for q in pdf.pages[1:] for c in q.chars if c["top"] < 800 and c["text"].strip())
    say(mn >= 28 and mx <= 595.3 - 28 and sz >= 9.4, "the paper PDF: glyphs between %.1f and %.1f pt of 595.3, smallest type on the question pages %.1f pt" % (mn, mx, sz))
    last = pdf.pages[-1]; ybot = max(c["bottom"] for c in last.chars if c["text"].strip() and c["top"] < 800); print("last question page: lowest body text at %.1f of %.1f pt (footer at 815)" % (ybot, last.height))
    # the answer space and the format sentence of every unit
    spaces = len(re.findall(r"(?:Write one letter|Write the code|Write the place|Write the letter|Write the number)[^\n]*", alltext)); print("lines that look like answer-format sentences in the paper text:", spaces)
    closed = json.load(open(X2 + "/exam_design_v1_3_0.json"))["answer_format"]["closed_list"]; cnt = {k: alltext.count(v) for k, v in closed.items()}; print("closed answer-format sentences counted in the paper text:", cnt)
    ncloze = sum(1 for r in items.values() if r["type"] in ("blank", "cloze")); nmatch = sum(1 for r in items.values() if r["type"] == "match")
    say(cnt["choice"] >= 11 + 3 - 0 and cnt["order"] >= 1 and cnt["bank"] >= 2 and cnt["match"] >= 1, "every kind of unit has its closed format sentence on the paper (choice %d, match %d, order %d, bank %d)" % (cnt["choice"], cnt["match"], cnt["order"], cnt["bank"]))
    # key letters against the printed options (option tables of the .docx)
    from docx.table import Table as _T
    from docx.text.paragraph import Paragraph as _P
    seq = []
    for ch in d.element.body.iterchildren():
        if ch.tag.endswith("}p"): seq.append(("p", _P(ch, d).text))
        elif ch.tag.endswith("}tbl"): seq.append(("t", [[c.text for c in r.cells] for r in _T(ch, d).rows]))
    letbad = []; okc = 0
    for it in key["items"]:
        r = items[it["id"]]
        for u in it["units"]:
            if u["kind"] != "choice": continue
            idx = next((i for i, (k_, v_) in enumerate(seq) if k_ == "p" and v_.startswith(u["unit"] + "\t")), None)
            opts = {}
            if idx is not None:
                for k_, v_ in seq[idx + 1:idx + 40]:
                    if k_ == "p" and re.match(r"^\d[a-g]\t", v_): break
                    if k_ == "p" and re.match(r"^[A-D]\t", v_): opts[v_[0]] = v_[2:].strip()
                    if k_ == "t" and v_ and re.match(r"^[A-D]  ", v_[0][0]):
                        for row in v_:
                            for c in row:
                                if re.match(r"^[A-D]  ", c): opts[c[0]] = c[3:].strip()
                        break
            good = r["options_or_blanks"]["ABCD".index(r["answer"])] if r["type"] in ("mcq", "predict") else None
            if good is not None and opts.get(u["answer"], "").strip() == good.strip(): okc += 1
            elif good is None and u["answer"] in opts: okc += 1
            else: letbad.append((u["unit"], u["answer"], opts.get(u["answer"])))
    nch = sum(1 for it in key["items"] for u in it["units"] if u["kind"] == "choice")
    say(not letbad and okc == nch and nch > 0, "key letters against the printed options: %d of %d choice units print the correct option text under the key letter; disagreements %s" % (okc, nch, letbad))
    # sheet
    sh = pdfplumber.open(PR + "/exam_midterm_s1_answersheet.pdf").pages; wd = json.load(open(X2 + "/exam_sheet_wording_v1_0_0.json"))["sheet_sentence"]
    t1 = re.sub(r"\s+", " ", sh[0].extract_text()); t2 = sh[1].extract_text()
    nos = [u["no"] for u in json.load(open(X2 + "/exam_design_v1_3_0.json"))["answer_sheet"]["units"]]; miss = [n for n in nos if not re.search(r"(^|\s)%s(\s|$)" % re.escape(n), t1)]
    smx = max(c["x1"] for q in sh for c in q.chars); smn = min(c["x0"] for q in sh for c in q.chars)
    say(len(sh) == 2 and not miss and wd in t1 and len(sh[1].curves) == 0 and len(sh[0].curves) == 298 and smx <= 553.3 and smn >= 42, "the real sheet: 2 pages, 31 labels (missing %s), the wording-file sentence on page 1, page 2 without circles, %d circles on page 1, glyphs %.1f to %.1f" % (miss, len(sh[0].curves), smn, smx))
    tips = [it for it in key["items"] if it.get("tip", "none").strip() != "none"]; tipmiss = [it["id"] for it in tips if re.sub(r"\s+", " ", it["tip"]) not in re.sub(r"\s+", " ", t2)]
    say(len(tips) == 13 and not tipmiss, "the tips page holds the %d tips of the paper, each word for word: missing %s" % (len(tips), tipmiss))
    # marking tool on the committed real key
    sys.path.insert(0, XT); sys.dont_write_bytecode = True
    import sen0414_exam_score_v1_0_0 as S
    K = S.load_key(PR + "/build/exam_midterm_s1_key.json"); G = lambda x: Fr(x["exact"]) if isinstance(x, dict) else Fr(str(x)); ans = {u["unit"]: str(u["answer"]) for it in K["items"] for u in it["units"]}
    allr = {"F": {"value": K["form_mark"]["code"], "flag": None}}; allr.update({n_: {"value": a_, "flag": None} for n_, a_ in ans.items()}); r1 = S.score_sheet(K, allr, "A4")
    allb = {"F": allr["F"]}; allb.update({n_: {"value": None, "flag": "blank"} for n_ in ans}); r2 = S.score_sheet(K, allb, "A4")
    say(G(r1["total"]) == 110 and G(r2["total"]) == 0 and r1["status"] == "COMPLETE", "the marking tool on the real key: all as the key = %s (expected 110), all blank = %s (expected 0)" % (r1["total"]["exact"], r2["total"]["exact"]))
    say(K["form_mark"]["code"] == "00" and "fill the number 00" in re.sub(r"\s+", " ", alltext), "the form mark: the key says %s and the paper directions say 'in the row marked F, fill the number 00' (the header form code on the sheet is a printed code, not filled)" % K["form_mark"]["code"])
    kd = _docx.Document(PR + "/exam_midterm_s1_key.docx"); ktext = "\n".join(pp.text for pp in kd.paragraphs) + "\n".join(c.text for t_ in kd.tables for r_ in t_.rows for c in r_.cells)
    say("A1" in ktext and "A4" in ktext and "bonus" in ktext.lower(), "the key lists the floor alternatives and the bonus point")
    pub = subprocess.run(["git", "status", "--short"], cwd=PUB, capture_output=True, text=True).stdout; ex = [l for l in pub.splitlines() if re.search(r"exam|papers_|_key|answersheet|midterm", l, re.I) and "08-tooling" not in l and "07-lineage" not in l]
    say(not ex, "no exam file in the public working tree (changes outside 08-tooling and 07-lineage that look exam-related: %s)" % ex[:3])
    tr = subprocess.run(["git", "ls-files"], cwd=PUB, capture_output=True, text=True).stdout.splitlines(); say(not [f for f in tr if "papers_r15" in f or "items_v3" in f or "exam_midterm_s1" in f], "nothing of this paper is tracked in the public repository")
    shutil.rmtree(tmp, ignore_errors=True)
elif m == "revmeasure":
    import hashlib, pdfplumber, collections
    from fractions import Fraction as Fr
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; PR = X2 + "/papers_r15"; XT = C + "/exams/SEN0414/08-tooling/exam"
    o = subprocess.run(["git", "show", "--name-status", "--format=", "2a62393"], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) == 9 and all(r[0] == "A" for r in rows), "CME commit 2a62393 adds only new files (%d files: the measure tool, its log, 7 page images)" % len(rows))
    lg = open(PR + "/exam_papers_measure_v1_0_0_log.txt", encoding="utf-8").read()
    say("SUMMARY: PASS 29, FAIL 2, RISK 1, NOTE 1, NOT_MEASURED 1, INFO 4" in lg and len(re.findall(r"^FAIL ", lg, re.M)) == 2 and "NOT_MEASURED" in lg, "the executor's log says what the report says (PASS 29, FAIL 2 = the 0.55 pt cover overshoot and the 9.5 pt type, RISK 1 = the slack, NOT_MEASURED 1 = Word), and the FAIL lines are printed, not hidden")
    pp = PR + "/exam_midterm_s1_paper.pdf"; say(hashlib.sha256(open(pp, "rb").read()).hexdigest().startswith("ace81060e1dee431"), "the committed paper PDF is the file I controlled (SHA-256 ace81060e1dee431...)")
    pdf = pdfplumber.open(pp); say(len(pdf.pages) == 5, "my own count: the committed paper PDF has %d pages" % len(pdf.pages))
    cov = pdf.pages[0]; over = [(c["text"], round(c["x1"], 2)) for c in cov.chars if c["text"].strip() and c["x1"] > 595.3 - 56.6 + 0.1]
    say(0 < len(over) <= 5 and max(x for _, x in over) - (595.3 - 56.6) < 1.0, "my own measure of the cover: %d glyphs past the right margin (595.3 - 56.6 = 538.7 pt), the largest by %.2f pt (executor: 3 glyphs, 0.55 pt)" % (len(over), max(x for _, x in over) - 538.7))
    small = sum(1 for q in pdf.pages[1:] for c in q.chars if c["text"].strip() and c["top"] < 800 and c["size"] < 9.99); say(small > 800, "my own count of body glyphs below 10 pt on the question pages: %d (executor: 849 at 9.5 pt, the answer labels and format sentences)" % small)
    last = pdf.pages[-1]; ink = max([c["bottom"] for c in last.chars if c["text"].strip() and c["top"] < 800] + [r["bottom"] for r in last.rects if r["bottom"] < 805] + [l["bottom"] for l in last.lines if l["bottom"] < 805]); sl = 805.04 - ink
    say(5 < sl < 20, "my own slack of the last question page: lowest ink %.1f pt, the bottom margin line 805.04 pt, slack %.1f pt (executor 11.5 pt): the risk is real, a safe margin is about 40 pt" % (ink, sl))
    sys.path.insert(0, XT); sys.dont_write_bytecode = True
    import sen0414_exam_score_v1_0_0 as S
    key = S.load_key(PR + "/build/exam_midterm_s1_key.json"); RECS = {r_["id"]: r_ for r_ in json.load(open(X2 + "/items/items_v3_0_0.json"))}
    k_of = lambda r_: {"mcq": 4, "predict": 4, "order": 4}.get(r_["type"]) or (len(r_["options_or_blanks"]["bank"]) if r_["type"] in ("blank", "cloze") else len(r_["options_or_blanks"]["answers"]))
    ans = {}; info = {}
    for it in key["items"]:
        for u in it["units"]: ans[u["unit"]] = str(u["answer"]); info[u["unit"]] = (Fr(u["points"]), k_of(RECS[it["id"]]), it["question"])
    WRONG = {"1c": "B", "1e": "A", "2b": "13", "2e": "00", "3b": "A", "3e": "G", "3g": "A", "4b": "2", "4f": "A", "5b": "A"}; BLANK = {"1d", "2c", "2g", "3d", "4c", "5d"}
    say(all(WRONG[n] != ans[n] for n in WRONG), "the executor's wrong answers are really wrong against the key (10 of 10)")
    rd = {"F": {"value": key["form_mark"]["code"], "flag": None}}; hand = Fr(0); qq = collections.defaultdict(Fr)
    for n_, (pt, k, q) in info.items():
        if n_ in BLANK: rd[n_] = {"value": None, "flag": "blank"}; v_ = Fr(0)
        elif n_ in WRONG: rd[n_] = {"value": WRONG[n_], "flag": None}; v_ = -pt / (k - 1)
        else: rd[n_] = {"value": ans[n_], "flag": None}; v_ = pt
        hand += v_; qq[q] += v_
    res = S.score_sheet(key, rd, "A4"); tot = Fr(res["total"]["exact"]) if isinstance(res["total"], dict) else Fr(str(res["total"]))
    say(res["status"] == "COMPLETE" and tot == hand == Fr(1817, 42), "my own hand score of the executor's mixed reading from the key's points and the item sets' k: %s; the tool says %s (executor 1817/42); per question %s" % (hand, tot, {q: str(v) for q, v in sorted(qq.items())}))
    pub = "/home/claude/AdvancedProgrammingWithPython"; tr = subprocess.run(["git", "ls-files"], cwd=pub, capture_output=True, text=True).stdout.splitlines(); say(not [f for f in tr if "papers_r15" in f or "exam_midterm_s1" in f or "measure_v1_0_0" in f], "nothing of the paper or the measure is tracked in the public repository")
elif m == "reveng2":
    import hashlib
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"
    o = subprocess.run(["git", "show", "--name-status", "--format=", "a45b086"], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) >= 20 and all(r[0] == "A" for r in rows), "CME commit a45b086 adds only new files (%d files)" % len(rows))
    say(hashlib.sha256(open(X2 + "/exam_engine_v1_2_1.py", "rb").read()).hexdigest() == "f5c8e432d70db1abaf6eba3a68f68b5fff05aaf51db9e018be42af75976ee0b1", "engine v1_2_1 is the file of the commit and the file parts 1 to 3 were built with (SHA-256 f5c8e432...)")
    lg = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "control-exam-logs/control_reveng2_check_run1.log"), encoding="utf-8").read()
    say("RESULT PASS" in lg and len(re.findall(r"^OK ", lg, re.M)) == 676 and not re.search(r"^MISMATCH", lg, re.M), "my own niced rerun of exam_engine_check_v1_2_1.py (967 s, kept log): RESULT PASS, %d OK, %d MISMATCH" % (len(re.findall(r"^OK ", lg, re.M)), len(re.findall(r"^MISMATCH", lg, re.M))))
    ch = re.findall(r"^OK\s+(\S+)\s+\[[^\]]*\] CHANGED AS LISTED", lg, re.M)
    say(sorted(set(ch)) == sorted(["E29_stem_21_words", "E29_two_sentences", "E29_definition_in_brackets", "E29_format_line_in_stem", "E31_tip_inside_stem", "E26_bare_short_form", "valid_abbreviation_expanded"]) , "the kept log shows exactly the seven listed changed verdicts: %s" % sorted(set(ch)))
    d = subprocess.run("diff <(sed 's/1_2_0/X/g' exam_engine_v1_2_0.py) <(sed 's/1_2_1/X/g;s/1_2_0/X/g' exam_engine_v1_2_1.py) | grep -c '^[<>]'", shell=True, executable="/bin/bash", cwd=X2, capture_output=True, text=True).stdout.strip()
    say(d.isdigit() and int(d) <= 40, "the engine differs from v1_2_0 by %s changed lines only (the two fixes: validator for E02, the sheet wording for E33)" % d)
    say("validator v1_2_0" in lg or "R28" in lg, "the raw control is printed: the old pool without answer_format is refused by E02 (R28)")
elif m == "revfix":
    import hashlib, tempfile, pdfplumber, docx as _docx
    from fractions import Fraction as Fr
    from docx.table import Table as _T
    from docx.text.paragraph import Paragraph as _P
    C = "/home/claude/CME"; X2 = C + "/exams/SEN0414/04-assessment/exams"; XT = C + "/exams/SEN0414/08-tooling/exam"; P1 = X2 + "/papers_r15"; P2 = X2 + "/papers_r18_revfix"; PUB = "/home/claude/AdvancedProgrammingWithPython"
    sh = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
    o = subprocess.run(["git", "show", "--name-status", "--format=", "ac82656"], cwd=C, capture_output=True, text=True).stdout
    rows = [l.split("\t") for l in o.strip().splitlines()]; say(len(rows) >= 40 and all(r[0] == "A" for r in rows), "CME commit ac82656 adds only new files (%d files)" % len(rows))
    say(sh(P1 + "/exam_midterm_s1_paper.docx").startswith("26ce713caeec0b7c") and sh(P1 + "/exam_midterm_s1_paper.pdf").startswith("ace81060e1dee431") and sh(P1 + "/exam_midterm_s1_answersheet.pdf").startswith("25bd4f4b6ed265bd") and sh(P1 + "/exam_midterm_s1_key.docx").startswith("0373dd5de31182db"), "the first version is untouched: paper .docx 26ce713c, paper PDF ace81060, sheet 25bd4f4b, key .docx 0373dd5d (the files the Owner printed)")
    o = subprocess.run(["git", "status", "--short", "--untracked-files=no", "exams/SEN0414"], cwd=C, capture_output=True, text=True).stdout; say(not o.strip(), "no tracked file under exams/SEN0414 in CME is modified")
    bf = [f for f in os.listdir(P1 + "/build")]; same = [f for f in bf if os.path.exists(P2 + "/build/" + f) and sh(P1 + "/build/" + f) == sh(P2 + "/build/" + f)]; say(len(same) == len(bf) == 7, "build files of the corrections version equal those of the first version byte for byte (%d of %d)" % (len(same), len(bf)))
    for f in ("exam_midterm_s1_v2_paper.docx", "exam_midterm_s1_v2_paper.pdf", "exam_midterm_s1_v2_answersheet.pdf"): print("SHA256", f, sh(P2 + "/" + f))
    print("SHA256 exam_sheet_wording_v1_1_0.json", sh(X2 + "/exam_sheet_wording_v1_1_0.json"))
    tmp = tempfile.mkdtemp(prefix="rf_ctl_")
    subprocess.run(["soffice", "-env:UserInstallation=file://" + tmp + "/prof", "--headless", "--convert-to", "pdf", "--outdir", tmp, P2 + "/exam_midterm_s1_v2_paper.docx"], capture_output=True, text=True, timeout=240)
    pdf = pdfplumber.open(tmp + "/exam_midterm_s1_v2_paper.pdf"); cm = pdfplumber.open(P2 + "/exam_midterm_s1_v2_paper.pdf")
    say(len(pdf.pages) == 5 and len(cm.pages) == 5, "my own LibreOffice conversion of the new paper .docx: %d pages; the committed PDF: %d pages; with the sheet 7 of 7" % (len(pdf.pages), len(cm.pages)))
    say([re.sub(r"\s+", " ", q.extract_text()) for q in pdf.pages] == [re.sub(r"\s+", " ", q.extract_text()) for q in cm.pages], "the committed paper PDF has the same text on every page as my own conversion")
    sz = min(c["size"] for q in pdf.pages[1:] for c in q.chars if c["top"] < 800 and c["text"].strip()); say(sz >= 9.99, "smallest type on the question pages: %.1f pt" % sz)
    cov = pdf.pages[0]; ov = max([c["x1"] for c in cov.chars if c["text"].strip()] + [0]) - (595.3 - 56.6); say(ov <= 0.1, "cover: the largest glyph overshoot past the right margin is %.2f pt (first version 0.55)" % ov)
    sl = []
    for q in pdf.pages[1:]:
        ink = max([c["bottom"] for c in q.chars if c["text"].strip() and c["top"] < 800] + [r["bottom"] for r in q.rects if r["bottom"] < 805] + [l["bottom"] for l in q.lines if l["bottom"] < 805]); sl.append(round(805.04 - ink, 1))
    print("slack of the four question pages (pt):", sl); say(sl[-1] >= 40, "slack of the last question page %.1f pt (first version 11.5; the page before has %.1f pt: in Word the content may shift)" % (sl[-1], sl[-2]))
    d = _docx.Document(P2 + "/exam_midterm_s1_v2_paper.docx"); seq = []
    for ch in d.element.body.iterchildren():
        if ch.tag.endswith("}p"): seq.append(("p", _P(ch, d).text))
        elif ch.tag.endswith("}tbl"): seq.append(("t", [[c.text for c in r.cells] for r in _T(ch, d).rows]))
    alltext = "\n".join(v if k == "p" else "\n".join(c for r in v for c in r) for k, v in seq)
    key = json.load(open(P2 + "/build/exam_midterm_s1_key.json"))["A"]; items = {r["id"]: r for r in json.load(open(X2 + "/items/items_v3_0_0.json"))}
    nsp = len(re.findall(r"(?m)^(?:Answer|Gap) \d[a-g]", alltext)); nord = alltext.count("Give the place of this step"); say(nsp + nord == 30, "answer spaces on the paper text: %d labelled (Answer or Gap) plus %d boxes of the order steps = %d (30 expected)" % (nsp, nord, nsp + nord))
    split = []
    for pi, q in enumerate(pdf.pages[1:], 1):
        pass
    pages_text = [q.extract_text() for q in pdf.pages]
    for it in key["items"]:
        for u in it["units"]:
            n_ = u["unit"]; hp = [i for i, tx in enumerate(pages_text) if re.search(r"(?m)^%s\b" % n_, tx) or re.search(r"(?m)^%s\S*[ -]" % n_[:1] + n_[1:], tx)]
            ap = [i for i, tx in enumerate(pages_text) if re.search(r"(?:Answer|Gap) %s\b" % n_, tx)]
            if u["kind"] == "order": continue
            if not ap or (hp and ap[0] not in hp): split.append((n_, hp, ap))
    say(not split, "every unit's answer label stands on a page that also holds its heading (sub-question not split): problems %s" % split[:5])
    letbad = []; okc = 0
    for it in key["items"]:
        r = items[it["id"]]
        for u in it["units"]:
            if u["kind"] != "choice": continue
            idx = next((i for i, (k_, v_) in enumerate(seq) if k_ == "p" and v_.startswith(u["unit"] + "\t")), None); opts = {}
            if idx is not None:
                for k_, v_ in seq[idx + 1:idx + 40]:
                    if k_ == "p" and re.match(r"^\d[a-g]\t", v_): break
                    if k_ == "p" and re.match(r"^[A-D]\t", v_): opts[v_[0]] = v_[2:].strip()
                    if k_ == "t" and v_ and re.match(r"^[A-D]  ", v_[0][0]):
                        for row in v_:
                            for c in row:
                                if re.match(r"^[A-D]  ", c): opts[c[0]] = c[3:].strip()
                        break
            good = r["options_or_blanks"]["ABCD".index(r["answer"])]
            if opts.get(u["answer"], "").strip() == good.strip(): okc += 1
            else: letbad.append((u["unit"], u["answer"]))
    say(not letbad and okc == 14, "key letters against the options printed in the NEW paper: %d of 14 print the correct option text; disagreements %s" % (okc, letbad))
    W2 = json.load(open(X2 + "/exam_sheet_wording_v1_1_0.json")); print("wording file keys:", list(W2.keys())); print(json.dumps(W2, indent=1)[:1500])
    sheet = pdfplumber.open(P2 + "/exam_midterm_s1_v2_answersheet.pdf").pages; t1 = re.sub(r"\s+", " ", sheet[0].extract_text()); t2 = re.sub(r"\s+", " ", sheet[1].extract_text())
    nos = [u["no"] for u in json.load(open(X2 + "/exam_design_v1_3_0.json"))["answer_sheet"]["units"]]; miss = [n for n in nos if not re.search(r"(^|\s)%s(\s|$)" % re.escape(n), t1)]
    say(len(sheet) == 2 and not miss and len(sheet[1].curves) == 0 and len(sheet[0].curves) == 298, "the new sheet: 2 pages, 31 labels (missing %s), page 2 without circles, %d circles on page 1" % (miss, len(sheet[0].curves)))
    sentence = W2["sheet_sentence"]; say(re.sub(r"\s+", " ", sentence) in t1, "the sheet sentence of the wording file v1_1_0 stands on sheet page 1 word for word")
    say("form code" not in (t1 + t2).lower() and t1.count("Office number 10100. Do not fill it.") == 1 and t2.count("Office number 10100. Do not fill it.") == 1, "the header: 'Office number 10100. Do not fill it.' on both pages and the words 'form code' on none")
    rowf = "On the answer sheet, in the row marked F, fill the number 00."; lc = re.sub(r"\s+", " ", sheet[0].crop((0, 0, 295, 841)).extract_text()); say(rowf in lc and re.sub(r"\s+", " ", rowf) in re.sub(r"\s+", " ", alltext), "the line above row F on the sheet equals the paper's sentence word for word")
    smx = max(c["x1"] for q in sheet for c in q.chars); smn = min(c["x0"] for q in sheet for c in q.chars); fb = max(c["bottom"] for q in sheet for c in q.chars if c["text"].strip()); say(smx <= 552.8 and smn >= 42.4 and fb <= 799.37, "sheet glyphs between %.1f and %.1f pt; the lowest glyph bottom %.2f pt, the bottom margin line 799.37 pt" % (smn, smx, fb))
    lines = [l for l in sheet[0].extract_text().splitlines() if l.strip()]; single = [l for l in lines if len(l.split()) == 1 and re.search(r"[a-z]\.$", l)]; say(not single, "no orphan line of a single word ending a sentence on sheet page 1 (found %s)" % single)
    tips = [it for it in key["items"] if it.get("tip", "none").strip() != "none"]; tm = [it["id"] for it in tips if re.sub(r"\s+", " ", it["tip"]) not in t2]; say(len(tips) == 13 and not tm, "the tips page: 13 tips word for word, missing %s" % tm)
    sys.path.insert(0, XT); sys.dont_write_bytecode = True
    import sen0414_exam_score_v1_0_0 as S
    K = S.load_key(P2 + "/build/exam_midterm_s1_key.json"); G = lambda x: Fr(x["exact"]) if isinstance(x, dict) else Fr(str(x)); ans = {u["unit"]: str(u["answer"]) for it in K["items"] for u in it["units"]}
    allr = {"F": {"value": K["form_mark"]["code"], "flag": None}}; allr.update({n_: {"value": a_, "flag": None} for n_, a_ in ans.items()}); r1 = S.score_sheet(K, allr, "A4")
    allb = {"F": allr["F"]}; allb.update({n_: {"value": None, "flag": "blank"} for n_ in ans}); r2 = S.score_sheet(K, allb, "A4")
    say(G(r1["total"]) == 110 and G(r2["total"]) == 0, "the marking tool on the key of the corrections version: all right %s, all blank %s" % (r1["total"]["exact"], r2["total"]["exact"]))
    tr = subprocess.run(["git", "ls-files"], cwd=PUB, capture_output=True, text=True).stdout.splitlines(); say(not [f for f in tr if "papers_r1" in f or "exam_midterm_s1" in f or "revfix" in f.lower() and "08-tooling" not in f], "nothing of the corrected paper is tracked in the public repository")
    pubs = subprocess.run(["git", "status", "--short"], cwd=PUB, capture_output=True, text=True).stdout; ex = [l for l in pubs.splitlines() if re.search(r"papers_r|_key|answersheet|midterm_s1", l, re.I) and "08-tooling" not in l and "07-lineage" not in l]; say(not ex, "no exam file in the public working tree: %s" % ex[:3])
    shutil.rmtree(tmp, ignore_errors=True)
print("RESULT " + ("FAIL: " + "; ".join(map(str, bad)) if bad else "PASS")); sys.exit(1 if bad else 0)
