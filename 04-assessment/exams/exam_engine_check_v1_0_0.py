#!/usr/bin/env python3
"""exam_engine_check_v1_0_0: runs every fixture of exam_engine_fixtures_v1_0_0.json through exam_engine_v1_0_0.py (task TK4_Engine_Core).
Prints, for each fixture, the expected and the actual verdict and the rules named; prints the rule results of the valid papers; recomputes the
main counts of the valid papers without SHACL (so that a vacuous rule is seen); checks that the same seed gives the same paper, that every rule E01
to E19 has a fixture that is refused with that rule named, and that the sheet specification is accepted by the SEN0401 sheet module's layout
(read-only, in memory, nothing written). Exit 0 only when every fixture is as expected; any other state prints its name and exits 1 or 2.
Usage: exam_engine_check_v1_0_0.py [--quick]   (--quick skips the second run of the determinism check)"""
import copy, json, sys, time
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exam_engine_v1_0_0 as eng          # noqa: E402
import exam_nocopy_v1_0_0 as nocopy       # noqa: E402

FIXTURES = HERE / "exam_engine_fixtures_v1_0_0.json"
ok_all = True
def say(ok, text):
    global ok_all
    ok_all &= bool(ok)
    print(("OK       " if ok else "MISMATCH ") + text)

def apply_pool_ops(pool, ops, syn_seed):
    pool = copy.deepcopy(pool)
    for op in ops:
        k = op["op"]
        if k == "append_copy":
            c = copy.deepcopy(next(i for i in pool if i["id"] == op["of"])); c["id"] = op["id"]; pool.append(c)
        elif k == "drop_where":
            keep = op["keep"]; out = []; n = 0
            for i in pool:
                hit = ("first_chapter" in op and i["chapters"][0] == op["first_chapter"]) or ("type" in op and i["type"] == op["type"])
                if hit:
                    n += 1
                    if n > keep:
                        continue
                out.append(i)
            pool = out
        elif k == "set_where":
            for i in pool:
                if all(i[a] == b for a, b in op["where"].items()):
                    i.update(copy.deepcopy(op["set"]))
        elif k == "single_chapter":
            for i in pool:
                i["chapters"] = [i["chapters"][0]]; i["course_point"] = i["course_point"][:1]
        elif k == "shrink_bank":
            for i in pool:
                if i["type"] in ("blank", "cloze") and i["options_or_blanks"]["gaps"] >= 3:
                    g = i["options_or_blanks"]["gaps"]; i["options_or_blanks"]["bank"] = i["options_or_blanks"]["bank"][:g]; i["answer"] = list(range(g))
        elif k == "copy_of_seed":
            for i in pool:
                if all(i[a] == b for a, b in op["where"].items()):
                    for f in ("stem", "listing", "options_or_blanks", "answer"):
                        i[f] = copy.deepcopy(syn_seed[f])
        else:
            raise ValueError("unknown pool op " + k)
    return pool

def lettered(entries):
    return [e for e in sorted(entries, key=lambda x: x["position"]) if e["type"] in ("mcq", "predict")]

def apply_paper_ops(build, ops):
    b = copy.deepcopy(build)
    for op in ops:
        k = op["op"]; es = b["forms"].get(op.get("form", "A"))
        banks = [e for e in sorted(es or [], key=lambda x: x["position"]) if e["type"] in ("blank", "cloze")]
        if k == "all_letters":
            for e in lettered(es):
                e["key"] = op["letter"]
        elif k == "letter_run":
            L = lettered(es); n = len(L)
            pool = {"A": 6, "B": 5, "C": 5, "D": 1}; seq = ["D"] * 4; i = 0
            while sum(pool.values()):
                for l in "ABCD":
                    if pool[l]:
                        seq.append(l); pool[l] -= 1
            assert n == len(seq) and seq.count("D") == 5, (n, seq)
            for e, l in zip(L, seq):
                e["key"] = l
        elif k == "drop_bank_seed":
            del banks[0]["bank_seed"]
        elif k == "wrong_bank_seed":
            banks[0]["bank_seed"] += 1
        elif k == "keys_rise":
            banks[0]["key"] = sorted(banks[0]["key"])
        elif k == "same_keys":
            n = len(banks[0]["bank"]); banks[0]["key"] = [n - 1, n - 1, 0][:len(banks[0]["key"])]
        elif k == "three_in_a_row":
            banks[0]["key"] = [0] * len(banks[0]["key"])
        elif k == "retype":
            e = next(x for x in es if x["position"] == op["position"]); e["type"] = "predict" if e["type"] == "mcq" else "mcq"
        elif k == "copy_option_order":
            a = {e["id"]: e["option_order"] for e in b["forms"]["A"]}
            e = b["forms"]["B"][0]; e["option_order"] = a[e["id"]]
        else:
            raise ValueError("unknown paper op " + k)
    return b

def independent_recount(build):
    """Counts straight from the build, without SHACL."""
    bp = build["blueprint"]; A = build["forms"]["A"]; msgs = []
    c = Counter(e["chapters"][0] for e in A)
    msgs.append(("chapters %s" % dict(sorted(c.items())), c == Counter({int(k): v for k, v in bp["chapters"].items()})))
    t = Counter(e["type"] for e in A)
    msgs.append(("types %s" % dict(sorted(t.items())), t == Counter(bp["types"])))
    secs = sum(build["measures"][e["id"]]["seconds"] for e in A)
    msgs.append(("answer time %d s of limit %d s" % (secs, 90 * bp["minutes"] * 60 // 100), secs * 100 <= 90 * bp["minutes"] * 60))
    bl = sum(1 for e in A if build["measures"][e["id"]]["bloom"] >= build["assumptions"]["bloom_threshold"])
    msgs.append(("Bloom %d or above: %d of %d" % (build["assumptions"]["bloom_threshold"], bl, len(A)), bl * 2 > len(A)))
    msgs.append(("cross-chapter %d (min %d)" % (sum(len(e["chapters"]) >= 2 for e in A), bp["cross_min"]), sum(len(e["chapters"]) >= 2 for e in A) >= bp["cross_min"]))
    msgs.append(("indirect %d (min %d)" % (sum(build["measures"][e["id"]]["indirect"] for e in A), bp["indirect_min"]), sum(build["measures"][e["id"]]["indirect"] for e in A) >= bp["indirect_min"]))
    for f in "AB":
        L = [e["key"] for e in lettered(build["forms"][f])]; cnt = Counter(L)
        run = max(sum(1 for _ in g) for _, g in __import__("itertools").groupby(L))
        msgs.append(("form %s letters %s longest run %d" % (f, dict(sorted(cnt.items())), run), max(cnt.values()) - min(cnt.get(l, 0) for l in "ABCD") <= 1 and run <= 3))
    msgs.append(("same type at every position in A and B", [e["type"] for e in build["forms"]["A"]] == [e["type"] for e in build["forms"]["B"]]))
    diff = sum(1 for a, b in zip(build["forms"]["A"], build["forms"]["B"]) if a["id"] != b["id"])
    msgs.append(("%d of %d positions hold another item in B" % (diff, len(A)), diff > 0))
    optdiff = {a["id"]: a["option_order"] != b["option_order"] for a in build["forms"]["A"] for b in build["forms"]["B"] if a["id"] == b["id"]}
    msgs.append(("option order differs for %d of %d items" % (sum(optdiff.values()), len(optdiff)), all(optdiff.values())))
    for f in "AB":
        for e in build["forms"][f]:
            if e["type"] in ("blank", "cloze"):
                if not (len(e["bank"]) > len(e["key"]) and len(set(e["key"])) == len(e["key"]) and e["bank"][e["key"][0]] == e["authored"]["bank"][e["authored"]["answer"][0]]):
                    msgs.append(("bank of %s in form %s" % (e["id"], f), False))
    return msgs

def main(argv):
    t0 = time.time()
    try:
        fx = json.loads(FIXTURES.read_text(encoding="utf-8"))
        design_path = eng.REPO / fx["design"]
        design = eng.load_json(design_path)
        print("CHECK exam_engine_check_v1_0_0: %d fixtures, engine %s, design %s (%s)" % (len(fx["fixtures"]), eng.VERSION, design_path.name, eng.design_version(design_path)))
        say(eng.SHAPES.is_file() and len(eng.shape_labels()) == 19, "shapes file parses, rules %s" % sorted(eng.shape_labels()))
        bp = eng.read_blueprint(design)
        print("blueprint read from the design: items %d, minutes %d, chapters %s, types %s, cross-chapter min %d, indirect min %d, seconds %s" %
              (bp["items"], bp["minutes"], bp["chapters"], bp["types"], bp["cross_min"], bp["indirect_min"], bp["seconds"]))
        real_seeds, census = nocopy.load_seeds(str(eng.REPO))
        print("real seeds loaded for the near-copy tool: %d" % len(real_seeds))
        syn = nocopy.seeds_from_items([eng.nocopy_view(i) for i in fx["synthetic_seed_items"]], "synthetic")
        builds = {}
        covered = set()
        for f in fx["fixtures"]:
            exp = f["expected"]
            if f["level"] == "pool":
                pool = fx["pools"][f.get("pool", "midterm")] if f.get("pool") != "midterm_items" else builds["valid_midterm"]["authored_items"]
                pool = apply_pool_ops(pool, f["mutations"], fx["synthetic_seed_items"][0])
                other = builds["valid_midterm"]["authored_items"] if f.get("other") == "midterm" else None
                seeds = syn if f.get("seeds") == "synthetic" else real_seeds
                seed = fx["makeup_seed"] if other else fx["seed"]
                kind = "makeup" if other else "midterm"
                b = eng.assemble(pool, design, seed, kind, 1, eng.REPO, seeds=seeds, other_items=other, pool_path=None, design_path=str(design_path))
                builds[f["name"]] = b
                rules = b["failed_rules"]; verdict = "paper" if b["ok"] else "refused"
            else:
                b0 = builds["valid_midterm"]
                b = eng.apply = None
                b = apply_paper_ops(b0, f["ops"])
                res, rules = eng.verify(b)
                verdict = "refused" if rules else "paper"
            actual = {"verdict": verdict, "rules": rules}
            say(actual == exp, "%-26s [%s] expected=%s actual=%s" % (f["name"], f["level"], json.dumps(exp, sort_keys=True), json.dumps(actual, sort_keys=True)))
            if exp["verdict"] == "refused":
                covered |= set(exp["rules"]) if len(exp["rules"]) == 1 or f["name"][:3] in exp["rules"] else set()
                covered.add(f["name"][:3])
            if f["name"].startswith("valid_"):
                for r, v in b["rules"].items():
                    print("      %s %-4s %s" % (r, v["status"].upper(), v["title"]))
                print("      selection cost %s, items %d, sheet units %d" % (b["selection_cost"], len(b["forms"]["A"]), len(b["sheet_spec"]["units"])))
                for text, good in independent_recount(b):
                    say(good, "recount %-12s %s" % (f["name"], text))
        rules_all = set(eng.shape_labels())
        say(rules_all == covered, "every rule has a fixture refused with that rule named: covered %s of %s" % (sorted(covered), sorted(rules_all)))
        # determinism
        b1 = builds["valid_midterm"]
        pool = fx["pools"]["midterm"]
        b2 = eng.assemble(pool, design, fx["seed"], "midterm", 1, eng.REPO, seeds=real_seeds, design_path=str(design_path))
        say(json.dumps(b1["forms"], sort_keys=True) == json.dumps(b2["forms"], sort_keys=True), "same seed, same pool: the two forms are identical")
        b3 = eng.assemble(pool, design, fx["seed"] + 1, "midterm", 1, eng.REPO, seeds=real_seeds, design_path=str(design_path))
        say(json.dumps(b1["forms"], sort_keys=True) != json.dumps(b3["forms"], sort_keys=True) and b3["ok"], "another seed gives another valid paper")
        # sheet specification against the SEN0401 sheet module (read-only, in memory)
        mod = eng.sheet_module()
        spec = b1["sheet_spec"]; lay = mod.build_layout(spec)
        kinds = Counter(u["kind"] for u in spec["units"])
        say(len(spec["units"]) == 1 + sum(len(eng.unit_list(e)) for e in b1["forms"]["A"]) and lay["pages"] >= 1,
            "sheet specification: %d units %s, module layout %d pages, form code %s, paper_kind %s" % (len(spec["units"]), dict(kinds), lay["pages"], spec["form_code"], spec["paper_kind"]))
        # design arithmetic units
        say(len(spec["units"]) == 54, "units equal the design's total_units 54 (from the blueprint types at 21 choice, 10 match, 8 order, 14 bank, 1 form mark)")
        # key
        ka, kb = (eng.key_data(b1["forms"][f], "midterm", f, 1) for f in "AB")
        say(ka["total_points"] == kb["total_points"] and ka["form_mark"] != kb["form_mark"], "key data: form A %d points, form B %d points, form marks %s and %s (the synthetic pool's own points; the design's real pool must give %s)" %
            (ka["total_points"], kb["total_points"], ka["form_mark"], kb["form_mark"], bp["total_points"]))
        # write/read round trip in a scratch folder outside the repository
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            paths = eng.write_outputs(b1, d, "fx")
            full = json.loads(Path(paths["buildfull"]).read_text(encoding="utf-8"))
            res, bad = eng.verify(full)
            say(not bad, "written build record read back and decided again: failed rules %s" % bad)
            say(all(Path(p).stat().st_size > 0 for p in paths.values()), "files written to a scratch folder: %s" % sorted(paths))
    except eng.CannotRun as e:
        print("CANNOT_RUN:", e); return 2
    print("%d seconds" % (time.time() - t0))
    print("RESULT", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv))
