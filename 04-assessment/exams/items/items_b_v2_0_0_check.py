#!/usr/bin/env python3
"""Check of the item set B, version 2.0.0 (task TK4_Items_B2). Prints every result as it is. Steps:
  1. the validator exam_item_check_v1_1_0.py on each merged list (set A plus set B, sorted by question and sub; a repeated id is a failure);
  2. units against the design: units per question (gaps, premises, steps, 1) and points per question, per merged list;
  3. near-copy rule of B against the seeds, of B against A in both directions, of the merged make-up against the merged paper (both directions);
  4. provisional side file of B; Bloom shares of the merged lists;
  5. the engine exam_engine_v1_1_0.py: midterm build on the merged paper list, then make-up build on the merged make-up list (--midterm).
Scratch files go to a temporary folder that is removed at the end. Exit 0 only if every step passes.
Usage: python3 items_b_v2_0_0_check.py
"""
import json, os, shutil, subprocess, sys, tempfile

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXAMS = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EXAMS, "..", ".."))
sys.path.insert(0, EXAMS); sys.path.insert(0, HERE)
import exam_item_check_v1_1_0 as ic        # noqa: E402
import exam_nocopy_v1_0_0 as nc            # noqa: E402
from items_a_v2_0_0_check import view      # noqa: E402

PAIRS = {"paper": ("items_a_v2_0_0.json", "items_b_v2_0_0.json"), "makeup": ("items_a_v2_0_0_makeup.json", "items_b_v2_0_0_makeup.json")}
SIDE = "items_b_v2_0_0_provisional.json"
DESIGN = os.path.join(EXAMS, "exam_design_v1_2_0.json")


def load(n):
    with open(os.path.join(HERE, n), encoding="utf-8") as f:
        return json.load(f)


def units(it):
    o, t = it["options_or_blanks"], it["type"]
    return o["gaps"] if t in ("blank", "cloze") else len(o["premises"]) if t == "match" else len(o) if t == "order" else 1


def merged(kind):
    a, b = (load(f) for f in PAIRS[kind])
    return sorted(a + b, key=lambda it: (it["question"], it["sub"]))


def main():
    ok = True
    design = json.load(open(DESIGN, encoding="utf-8"))
    want_u = design["blueprint"]["sub_questions_per_question"]; want_p = design["blueprint"]["points_per_question"]
    M = {k: merged(k) for k in PAIRS}
    print("== 1. validator exam_item_check_v1_1_0.py on the merged lists ==")
    for k, L in M.items():
        ids = [it["id"] for it in L]
        rep = sorted({i for i in ids if ids.count(i) > 1})
        res = ic.check_items(L)
        for r in res:
            print("FAIL", k, r["id"], r["rule"], r["message"])
        print("%s: %d records, repeated ids: %s, %s, %d failure(s)" % (k, len(L), rep or "none", "PASS" if not res and not rep else "FAIL", len(res)))
        ok &= not res and not rep
    for k, (fa, fb) in PAIRS.items():
        res = ic.check_items(load(fb))
        print("%s set B alone: %d records, %d failure(s)%s" % (k, len(load(fb)), len(res), "" if not res else " " + str([(r["id"], r["rule"]) for r in res])))
    print("\n== 2. units and points against the design ==")
    for k, L in M.items():
        u, p = {}, {}
        for it in L:
            u[it["question"]] = u.get(it["question"], 0) + units(it); p[it["question"]] = p.get(it["question"], 0) + it["points"]
        good = u == want_u and p == want_p
        print("%s: units %s (design %s); points %s (design %s); total units %d: %s" % (k, u, want_u, p, want_p, sum(u.values()), "PASS" if good else "FAIL"))
        ok &= good
    print("\n== 3. near-copy rule ==")
    seeds, census = nc.load_seeds(ROOT)
    print("seeds: %d" % len(seeds))
    for k, (fa, fb) in PAIRS.items():
        B = load(fb)
        res = nc.measure_all([view(it) for it in B], seeds)
        bad = [r for r in res if r["is_copy"]]
        print("%s set B against the seeds: largest C per item: %s; near copies: %d" % (k, " ".join("%s=%.3f" % (r["id"], float(r["max_c"])) for r in res), len(bad)))
        ok &= not bad
        for x, y, lab in ((fa, fb, "B against A"), (fb, fa, "A against B")):
            X, Y = load(x), load(y)
            other = nc.seeds_from_items([view(it) for it in X], "set:" + x)
            res = nc.measure_all([view(it) for it in Y], other)
            bad = [r for r in res if r["is_copy"]]
            print("%s %s (%s items against %s): largest C %.3f; near copies %d" % (k, lab, y, x, max(float(r["max_c"]) for r in res), len(bad)))
            ok &= not bad
    for a, b in (("paper", "makeup"), ("makeup", "paper")):
        other = nc.seeds_from_items([view(it) for it in M[a]], "merged " + a)
        res = nc.measure_all([view(it) for it in M[b]], other)
        bad = [r for r in res if r["is_copy"]]
        print("merged %s against merged %s: largest C %.3f; near copies %d" % (b, a, max(float(r["max_c"]) for r in res), len(bad)))
        ok &= not bad
    same = [it["id"] for it in M["paper"] if any(it["stem"] == o["stem"] for o in M["makeup"])]
    print("identical stems in both merged lists:", same or "none"); ok &= not same
    print("\n== 4. side file and Bloom ==")
    side = load(SIDE)
    have = {(r["file"], r["id"]) for r in side["records"] if r["provisional"] is True}
    need = {(f, it["id"]) for pr in PAIRS.values() for f in pr[1:] for it in load(f)}
    print("side file covers %d of %d records, provisional: %s" % (len(have & need), len(need), side["provisional"]))
    ok &= have == need and side["provisional"] is True
    for k, L in M.items():
        n = sum(units(it) for it in L)
        ap = sum(units(it) for it in L if it["bloom"] >= 3); an = sum(units(it) for it in L if it["bloom"] >= 4)
        print("%s: units %d; Apply and above %d (%.0f%%, need majority); Analyze and above %d (need at least 8); level 1 records: %d" % (k, n, ap, 100 * ap / n, an, sum(1 for it in L if it["bloom"] < 2)))
        ok &= ap * 2 > n and an >= 8
        ch = sorted({c for it in L for c in it["chapters"]})
        print("   chapters covered:", ch, " letters:", {l: sum(1 for it in L if it["answer"] == l) for l in "ABCD"})
    print("\n== 5. engine exam_engine_v1_1_0.py ==")
    tmp = tempfile.mkdtemp(prefix="items_b2_")
    try:
        engine = os.path.join(EXAMS, "exam_engine_v1_1_0.py")
        mids = None
        for k in ("paper", "makeup"):
            pool = os.path.join(tmp, "pool_%s.json" % k)
            json.dump(M[k], open(pool, "w", encoding="utf-8"), ensure_ascii=False)
            cmd = [sys.executable, "-B", engine, "build", "--pool", pool, "--design", DESIGN, "--seed", "1", "--out", os.path.join(tmp, k),
                   "--stem", "b2_" + k, "--kind", "midterm" if k == "paper" else "makeup"]
            mid = os.path.join(tmp, "paper", "b2_paper_buildfull.json")
            if k == "makeup" and os.path.exists(mid):
                cmd += ["--midterm", mid]
            elif k == "makeup":
                print("NOTE: the midterm build was refused, so no build record exists; the make-up runs without --midterm (E17 then compares nothing)")
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
            print("--- engine %s pool (exit %d) ---" % (k, p.returncode)); print(p.stdout.rstrip()); print(p.stderr.rstrip()[-1500:])
            ok &= p.returncode == 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("\nRESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
