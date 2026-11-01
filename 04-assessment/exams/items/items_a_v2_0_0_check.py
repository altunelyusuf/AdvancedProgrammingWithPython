#!/usr/bin/env python3
"""Check of the item set A, version 2.0.0 (task TK4_Items_A2). Runs, in this order, and prints every result as it is:
  1. the item validator exam_item_check_v1_1_0.py (all rules R01 to R24) on each of the two lists;
  2. the near-copy rule exam_nocopy_v1_0_0.py against the seed pages' banks, quizzes and chapter listings, in two views:
     (a) the records as they are (the tool reads the fields 'code' and 'options', which a 22-field record does not have, so the
         listing is NOT compared in this view: printed as a limit of the tool, not hidden);
     (b) a view built from each record: stem, listing joined as code, every option text, the answer as text; this one compares the listing;
  3. the make-up against the paper (and the paper against the make-up): no item shared, by the same near-copy rule (--other);
  4. the provisional side file: every record of both lists is in it with provisional true;
  5. the shares of Bloom levels and the spread over chapters, types, asks and letters, with the thresholds of the brief.
Exit 0 only if every step passes. Usage: python3 items_a_v2_0_0_check.py
"""
import json, os, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXAMS = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(EXAMS, "..", ".."))
sys.path.insert(0, EXAMS)
import exam_item_check_v1_1_0 as ic        # noqa: E402
import exam_nocopy_v1_0_0 as nc            # noqa: E402

FILES = ("items_a_v2_0_0.json", "items_a_v2_0_0_makeup.json")
SIDE = "items_a_v2_0_0_provisional.json"


def load(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return json.load(f)


def view(it):
    """The record as the near-copy tool reads it: code, options (flat), answer as text."""
    o, a, t = it["options_or_blanks"], it["answer"], it["type"]
    if t in ("mcq", "predict"):
        opts = list(o); ans = o["ABCD".index(a)]
    elif t == "order":
        opts = list(o); ans = " ".join(o[i] for i in sorted(range(4), key=lambda k: a[k]))
    elif t == "match":
        opts = list(o["premises"]) + list(o["answers"]); ans = " ".join(o["premises"][i] + " = " + o["answers"]["ABCDEFG".index(x)] for i, x in enumerate(a))
    else:
        opts = list(o["bank"]); ans = " ".join(o["bank"][i] for i in a)
    return {"id": it["id"], "stem": it["stem"], "code": "\n".join(it["listing"]), "options": opts, "answer": ans}


def main():
    ok = True
    lists = {f: load(f) for f in FILES}
    print("== 1. item validator exam_item_check_v1_1_0.py ==")
    for f, L in lists.items():
        res = ic.check_items(L)
        for r in res:
            print("FAIL", f, r["id"], r["rule"], r["message"])
        print("%s: %d records, %s, %d failure(s)" % (f, len(L), "PASS" if not res else "FAIL", len(res)))
        ok &= not res
    print("\n== 2. near-copy rule exam_nocopy_v1_0_0.py against the seeds ==")
    seeds, census = nc.load_seeds(ROOT)
    print("seeds: %d (banks %d files, quizzes %d files, manifests %d files)" % (len(seeds), len(census["banks"]), len(census["quizzes"]), len(census["manifests"])))
    for f, L in lists.items():
        for label, items in (("(a) records as they are, listing not read by the tool", [dict(it, id=it["id"], options=it["options_or_blanks"]) for it in L]),
                             ("(b) view with listing as code", [view(it) for it in L])):
            res = nc.measure_all(items, seeds)
            bad = [r for r in res if r["is_copy"]]
            print("%s %s: largest C per item: %s; near copies: %d" % (f, label, " ".join("%s=%.3f" % (r["id"], float(r["max_c"])) for r in res), len(bad)))
            for r in bad:
                print("   NEAR COPY", r["id"], r["verdict"], r["shown"]["seed"])
            ok &= not bad
    print("\n== 3. make-up against paper (no item in both) ==")
    for a, b in ((FILES[0], FILES[1]), (FILES[1], FILES[0])):
        other = nc.seeds_from_items([view(it) for it in lists[a]], "paper:" + a)
        res = nc.measure_all([view(it) for it in lists[b]], other)
        bad = [r for r in res if r["is_copy"]]
        print("%s against %s: largest C %.3f; near copies %d" % (b, a, max(float(r["max_c"]) for r in res), len(bad)))
        ok &= not bad
    same = [it["id"] for it in lists[FILES[0]] if any(it["stem"] == o["stem"] for o in lists[FILES[1]])]
    print("identical stems in both lists:", same or "none"); ok &= not same
    print("\n== 4. provisional side file ==")
    side = load(SIDE)
    have = {(r["file"], r["id"]) for r in side["records"] if r["provisional"] is True}
    need = {(f, it["id"]) for f, L in lists.items() for it in L}
    print("side file covers %d of %d records, provisional true: %s" % (len(have & need), len(need), side["provisional"]))
    ok &= have == need and side["provisional"] is True
    print("\n== 5. shares and spread ==")
    allit = [it for L in lists.values() for it in L]
    for f, L in lists.items():
        n = len(L)
        ap = sum(1 for it in L if it["bloom"] >= 3); an = sum(1 for it in L if it["bloom"] >= 4)
        pts = {}
        for it in L:
            pts[it["question"]] = pts.get(it["question"], 0) + it["points"]
        print("%s: %d records; Apply and above %d (%.0f%%, need at least 40%%); Analyze and above %d (%.0f%%, need at least 30%%); points per question %s" %
              (f, n, ap, 100 * ap / n, an, 100 * an / n, pts))
        ok &= ap / n >= 0.40 and an / n >= 0.30 and all(it["bloom"] >= 2 for it in L)
    cnt = lambda key: {k: sum(1 for it in allit if (k in it[key] if isinstance(it[key], list) else it[key] == k)) for k in sorted({x for it in allit for x in (it[key] if isinstance(it[key], list) else [it[key]])})}
    print("chapters (a record may cover two):", cnt("chapters"))
    print("types:", cnt("type"), " asks:", cnt("asks"), " bloom:", cnt("bloom"))
    print("letters of choice answers:", {l: sum(1 for it in allit if it["answer"] == l) for l in "ABCD"})
    missing = sorted(set(range(1, 9)) - {c for it in allit for c in it["chapters"]})
    print("chapters with no record:", missing or "none"); ok &= not missing
    print("\nRESULT", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
