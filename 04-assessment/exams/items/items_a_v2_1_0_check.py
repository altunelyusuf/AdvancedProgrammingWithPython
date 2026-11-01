#!/usr/bin/env python3
"""Check of the item set A, version 2.1.0 (task TK4_Items_A3). Prints every result as it is; exit 0 only if every step passes.
For the paper list and the make-up list, each merged with the committed set B by id (B paper with A paper, B make-up with A make-up):
  1. the item validator exam_item_check_v1_1_0.py (R01 to R24): 0 failures on A alone and on the merged list;
  2. units per question 6/7/7/6/4 and points per question 25/25/25/25/10; units per chapter equal to the quota of the design;
     cross-chapter units 9; indirect units 6; Apply and above at least 27 of 30; Analyze and above at least 8 of 30;
     set A holds the five cross-chapter records Q1f, Q3b, Q4b, Q5a, Q5b with the first chapters 7, 7, 8, 1, 2;
     a blank, cloze, match or order record lists exactly one chapter per unit;
  3. the near-copy rule exam_nocopy_v1_0_0.py against the seeds (view with listing as code); paper against make-up and the reverse;
     set A against set B in all four pairings; identical stems;
  4. the provisional side file;
  5. exam_engine_v1_1_0.py build of the merged pool (two seeds): exit 0 and every rule E01 to E28 PASS; for the make-up with
     --kind makeup --midterm (the build record of the paper's build with the same seed). Its verbatim output is printed.
     The make-up pool is written as one NAMED set ("makeup"): the engine names a plain list S0, and a make-up and a paper both named S0
     would make every same id look like a repeated item (rule E17 compares set name plus id). Nothing else differs from the paper pool.
Usage: python3 items_a_v2_1_0_check.py
"""
import json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXAMS = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EXAMS, "..", ".."))
sys.path.insert(0, EXAMS)
import exam_item_check_v1_1_0 as ic        # noqa: E402
import exam_nocopy_v1_0_0 as nc            # noqa: E402
import exam_engine_v1_1_0 as eng           # noqa: E402

A_FILES = {"paper": "items_a_v2_1_0.json", "makeup": "items_a_v2_1_0_makeup.json"}
B_FILES = {"paper": "items_b_v2_0_0.json", "makeup": "items_b_v2_0_0_makeup.json"}
SIDE = "items_a_v2_1_0_provisional.json"
DESIGN = os.path.join(EXAMS, "exam_design_v1_2_0.json")
SEEDS = (1, 20261101)
CROSS_A = {"Q1f": 7, "Q3b": 7, "Q4b": 8, "Q5a": 1, "Q5b": 2}


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def view(it):
    return eng.nocopy_view(it)


def main():
    ok = True
    design = json.load(open(DESIGN, encoding="utf-8"))
    bp = eng.read_blueprint(design)
    quota = [bp["chapters"][c] for c in range(1, 9)]
    A = {k: load(f) for k, f in A_FILES.items()}
    B = {k: load(f) for k, f in B_FILES.items()}
    M = {k: A[k] + B[k] for k in A}
    ids = {k: [r["id"] for r in M[k]] for k in M}
    print("design:", os.path.basename(DESIGN), " quota per chapter 1..8:", quota, " cross-chapter units:", bp["cross_min"], " indirect units:", bp["indirect_min"])
    print("== 1. item validator exam_item_check_v1_1_0.py ==")
    for k in A:
        for label, L in (("set A " + A_FILES[k], A[k]), ("merged A+B (%s)" % k, M[k])):
            res = ic.check_items(L)
            for r in res:
                print("FAIL", label, r["id"], r["rule"], r["message"])
            print("%s: %d records, %s, %d failure(s)" % (label, len(L), "PASS" if not res else "FAIL", len(res)))
            ok &= not res
        dup = [i for i, n in Counter(ids[k]).items() if n > 1]
        print("merged %s: repeated ids %s" % (k, dup or "none")); ok &= not dup
    print("\n== 2. counts against the design ==")
    for k in M:
        L = M[k]
        feats = [eng.features(r, bp) for r in L]
        uq, pq = Counter(), Counter()
        for r, f in zip(L, feats):
            uq[r["question"]] += f["u"]; pq[r["question"]] += r["points"]
        units = [uq["Q%d" % i] for i in range(1, 6)]; pts = [pq["Q%d" % i] for i in range(1, 6)]
        chap = Counter()
        for f in feats:
            chap.update(f["ch"])
        perch = [chap[c] for c in range(1, 9)]
        cross = sum(f["cross"] for f in feats); ind = sum(f["ind"] for f in feats)
        ap = sum(f["apply"] for f in feats); an = sum(f["analyze"] for f in feats)
        print("%s: units per question %s (want [6, 7, 7, 6, 4]); points %s (want [25, 25, 25, 25, 10])" % (k, units, pts))
        print("%s: units per chapter %s (want %s); cross-chapter %d (want %d); indirect %d (want %d); Apply and above %d of 30 (want 27 or more); Analyze and above %d of 30 (want 8 or more)" %
              (k, perch, quota, cross, bp["cross_min"], ind, bp["indirect_min"], ap, an))
        good = units == [6, 7, 7, 6, 4] and pts == [25, 25, 25, 25, 10] and perch == quota and cross == bp["cross_min"] and ind == bp["indirect_min"] and ap >= 27 and an >= 8
        ok &= good
        print("%s: %s" % (k, "PASS" if good else "FAIL"))
        got = {r["id"]: r["chapters"][0] for r in A[k] if len(r["chapters"]) >= 2 and eng.units_of(r) == 1}
        print("%s: cross-chapter records of set A and their first chapter: %s (want %s)" % (k, got, CROSS_A)); ok &= got == CROSS_A
        bad = [r["id"] for r in A[k] if eng.units_of(r) > 1 and len(r["chapters"]) != eng.units_of(r)]
        print("%s: multi-unit records of A with a chapter list not equal to the units: %s" % (k, bad or "none")); ok &= not bad
        badi = [r["id"] for r in A[k] if (r["indirect_form"] != "none") != (r["id"] in ("Q4b", "Q5a", "Q5b"))]
        print("%s: indirect forms only on Q4b, Q5a, Q5b: %s" % (k, "yes" if not badi else "NO " + str(badi))); ok &= not badi
    print("\n== 3. near-copy rule ==")
    seeds, census = nc.load_seeds(ROOT)
    print("seeds: %d (banks %d files, quizzes %d files, manifests %d files)" % (len(seeds), len(census["banks"]), len(census["quizzes"]), len(census["manifests"])))
    for k, L in A.items():
        res = nc.measure_all([view(it) for it in L], seeds)
        bad = [r for r in res if r["is_copy"]]
        print("%s against the seeds: largest C per item: %s; near copies: %d" % (A_FILES[k], " ".join("%s=%.3f" % (r["id"], float(r["max_c"])) for r in res), len(bad)))
        ok &= not bad
    pairs = [(A["paper"], A["makeup"], "A paper", "A make-up"), (A["makeup"], A["paper"], "A make-up", "A paper")]
    for pa, pb in (("paper", "paper"), ("paper", "makeup"), ("makeup", "paper"), ("makeup", "makeup")):
        pairs += [(A[pa], B[pb], "A " + pa, "B " + pb), (B[pb], A[pa], "B " + pb, "A " + pa)]
    for x, y, nx, ny in pairs:
        other = nc.seeds_from_items([view(it) for it in x], nx)
        res = nc.measure_all([view(it) for it in y], other)
        bad = [r["id"] for r in res if r["is_copy"]]
        print("%s against %s: largest C %.3f; near copies %s" % (ny, nx, max(float(r["max_c"]) for r in res), bad or "none"))
        ok &= not bad
    same = [it["id"] for it in A["paper"] if any(it["stem"] == o["stem"] for o in A["makeup"])]
    print("identical stems in both lists of set A:", same or "none"); ok &= not same
    print("\n== 4. provisional side file ==")
    side = load(SIDE)
    have = {(r["file"], r["id"]) for r in side["records"] if r["provisional"] is True}
    need = {(A_FILES[k], it["id"]) for k, L in A.items() for it in L}
    print("side file covers %d of %d records, provisional true: %s" % (len(have & need), len(need), side["provisional"]))
    ok &= have == need and side["provisional"] is True
    print("\n== 5. engine exam_engine_v1_1_0.py build of the merged pools ==")
    tmp = tempfile.mkdtemp(prefix="a3_check_")
    try:
        pools = {"paper": os.path.join(tmp, "pool_paper.json"), "makeup": os.path.join(tmp, "pool_makeup.json")}
        json.dump(M["paper"], open(pools["paper"], "w"), ensure_ascii=False)
        json.dump({"sets": [{"name": "makeup", "items": M["makeup"]}]}, open(pools["makeup"], "w"), ensure_ascii=False)
        for seed in SEEDS:
            out_p = os.path.join(tmp, "p%d" % seed); out_m = os.path.join(tmp, "m%d" % seed)
            cmds = [("paper", ["build", "--pool", pools["paper"], "--design", DESIGN, "--seed", str(seed), "--out", out_p]),
                    ("makeup", ["build", "--pool", pools["makeup"], "--design", DESIGN, "--seed", str(seed), "--kind", "makeup",
                                "--midterm", os.path.join(out_p, "exam_midterm_s%d_buildfull.json" % seed), "--out", out_m])]
            for name, argv in cmds:
                cmd = [sys.executable, "-I", os.path.join(EXAMS, "exam_engine_v1_1_0.py")] + argv
                print("$ exam_engine_v1_1_0.py", " ".join(os.path.basename(a) if os.sep in a else a for a in argv))
                p = subprocess.run(cmd, capture_output=True, text=True)
                print(p.stdout.rstrip()); print(p.stderr.rstrip())
                rules = re.findall(r"^(E\d\d) (PASS|FAIL)", p.stdout, re.M)
                allpass = len(rules) == 28 and all(s == "PASS" for _, s in rules) and [r for r, _ in rules] == ["E%02d" % i for i in range(1, 29)]
                print("-> %s seed %d: exit code %d; rules E01..E28 listed %d, passing %d" % (name, seed, p.returncode, len(rules), sum(1 for _, s in rules if s == "PASS")))
                ok &= p.returncode == 0 and allpass
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\nRESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
