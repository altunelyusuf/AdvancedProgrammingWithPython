#!/usr/bin/env python3
"""exam_engine_check_v1_1_0: runs every fixture of exam_engine_fixtures_v1_1_0.json through exam_engine_v1_1_0.py (task TK4_Engine5).
Prints, for each fixture, the expected and the actual verdict and the rules named; prints the rule results and the independent recount
(without SHACL) of every accepted paper, among them the counts of sub-questions at Apply and above and at Analyze and above; checks that every
rule E01 to E28 has a fixture refused with that rule named, that the same seed gives the same paper, and that the sheet specification is
accepted by the SEN0401 sheet module (read-only, in memory). Exit 0 only when every fixture is as expected; any other state prints its name
and exits 1 or 2.  Usage: exam_engine_check_v1_1_0.py"""
import copy, itertools, json, sys, tempfile, time
from collections import Counter
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import exam_engine_v1_1_0 as eng          # noqa: E402
import exam_nocopy_v1_0_0 as nocopy       # noqa: E402

FIXTURES = HERE / "exam_engine_fixtures_v1_1_0.json"
ok_all = True
def say(ok, text):
    global ok_all
    ok_all &= bool(ok)
    print(("OK       " if ok else "MISMATCH ") + text)

def apply_pool_ops(sets, ops, syn_seed):
    sets = copy.deepcopy(sets)
    for op in ops:
        k = op["op"]
        names = op.get("sets")
        tgt = [s for s in sets if names is None or s["name"] in names]
        if k == "keep_sets":
            sets = [s for s in sets if s["name"] in op["names"]]
        elif k == "dup_record":
            s = next(x for x in sets if x["name"] == op["set"]); s["items"].append(copy.deepcopy(next(i for i in s["items"] if i["id"] == op["id"])))
        elif k == "drop_ids":
            for s in tgt:
                s["items"] = [i for i in s["items"] if i["id"] not in op["ids"]]
        elif k == "set_fields":
            for s in tgt:
                for i in s["items"]:
                    if op.get("where_type") == "any" or i["id"] in op.get("ids", []):
                        if "set" in op:
                            i.update(copy.deepcopy(op["set"]))
                        if op.get("keep_first_chapter"):
                            i["chapters"] = [i["chapters"][0]]
        elif k == "set_bloom":
            for s in tgt:
                for i in s["items"]:
                    if i["id"] in op["by_id"]:
                        i["bloom"] = op["by_id"][i["id"]]
                    elif "default" in op:
                        i["bloom"] = op["default"]
        elif k == "stem_add":
            for s in tgt:
                for i in s["items"]:
                    if i["id"] in op["ids"]:
                        i["stem"] += op["text"]
        elif k == "shrink_bank":
            for s in tgt:
                for i in s["items"]:
                    if i["type"] in ("blank", "cloze"):
                        g = i["options_or_blanks"]["gaps"]; i["options_or_blanks"]["bank"] = i["options_or_blanks"]["bank"][:g]; i["answer"] = list(range(g))
        elif k == "copy_of_seed":
            for s in tgt:
                for i in s["items"]:
                    if i["id"] in op["ids"]:
                        for f in ("stem", "listing", "options_or_blanks", "answer"):
                            i[f] = copy.deepcopy(syn_seed[f])
        elif k == "long_layout":
            for s in tgt:
                for i in s["items"]:
                    if i["type"] in op["types"]:
                        i["listing"] = ["fx_long_line_number_%02d = %d  # a long listing line of the layout fixture" % (n, n) for n in range(op["lines"])]
                        i["code_width"] = 90
                        i["options_or_blanks"] = [o + " " + "pad" * 12 + "%d" % j for j, o in enumerate(i["options_or_blanks"])]
        else:
            raise ValueError("unknown pool op " + k)
    return sets

def lettered(entries):
    return [e for e in sorted(entries, key=lambda x: x["position"]) if e["type"] in ("mcq", "predict")]

def apply_paper_ops(build, ops):
    b = copy.deepcopy(build)
    for op in ops:
        k = op["op"]; es = b["forms"].get(op.get("form", "A"))
        banks = [e for e in sorted(es or [], key=lambda x: x["position"]) if e["type"] in ("blank", "cloze")]
        if k == "slow":
            for m in b["measures"].values():
                m["unit_seconds"] *= op["factor"]
        elif k == "all_letters":
            for e in lettered(es):
                e["key"] = op["letter"]
        elif k == "letter_run":
            seq = ["D"] * 4 + list("ABCABCABCA")
            L = lettered(es); assert len(L) == len(seq) == 14 and Counter(seq) == {"A": 4, "B": 3, "C": 3, "D": 4}
            for e, l in zip(L, seq):
                e["key"] = l
        elif k == "drop_bank_seed":
            del banks[0]["bank_seed"]
        elif k == "wrong_bank_seed":
            banks[0]["bank_seed"] += 1
        elif k == "keys_rise":
            banks[0]["key"] = sorted(banks[0]["key"])
        elif k == "same_keys":
            n = len(banks[0]["bank"]); banks[0]["key"] = [n - 1, n - 1, 0, 1][:len(banks[0]["key"])]
        elif k == "three_in_a_row":
            banks[0]["key"] = [0] * len(banks[0]["key"])
        elif k == "retype":
            e = next(x for x in es if x["position"] == op["position"]); e["type"] = "predict" if e["type"] == "mcq" else "mcq"
        elif k == "copy_option_order":
            a = {e["ref"]: e["option_order"] for e in b["forms"]["A"]}
            e = b["forms"]["B"][0]; e["option_order"] = a[e["ref"]]
        elif k == "retype_question":
            for f in b["forms"].values():
                e = next(x for x in f if x["question"] == op["question"]); e["type"] = op["to"]
        elif k == "swap_positions":
            e1 = next(x for x in es if x["question"] == op["first_question"]); e2 = next(x for x in es if x["question"] == op["second_question"])
            e1["position"], e2["position"] = e2["position"], e1["position"]
        elif k == "long_entries":
            for f in b["forms"].values():
                for e in f:
                    e["listing"] = ["fx_line = 1"] * op["lines"]
        elif k == "drop_sheet_unit":
            b["sheet_spec"]["units"] = [u for u in b["sheet_spec"]["units"] if u["no"] != op["no"]]
        elif k == "rename_unit":
            for e in es:
                e["unit_numbers"] = [op["to"] if n == op["from"] else n for n in e["unit_numbers"]]
        else:
            raise ValueError("unknown paper op " + k)
    return b

def recount(build):
    """Counts straight from the build, without SHACL."""
    bp = build["blueprint"]; A = build["forms"]["A"]; msgs = []
    units = [(e, k) for e in A for k in range(e["units"])]
    qs = {q["question"]: q for q in bp["questions"]}
    per_q = Counter(e["question"] for e, _ in units)
    msgs.append(("sub-questions per question %s, total %d" % (dict(sorted(per_q.items())), len(units)), all(per_q[q] == qs[q]["subs"] for q in qs) and len(units) == bp["items"]))
    pts = Counter()
    for e in A:
        pts[e["question"]] += e["points"]
    msgs.append(("points per question %s, base %d, bonus %d" % (dict(sorted(pts.items())), sum(v for q, v in pts.items() if not qs[q]["bonus"]), sum(v for q, v in pts.items() if qs[q]["bonus"])),
                 all(pts[q] == qs[q]["points"] for q in qs)))
    ch = Counter(e["chapters"][k % len(e["chapters"])] for e, k in units)
    msgs.append(("sub-questions per chapter %s" % dict(sorted(ch.items())), ch == Counter({int(c): v for c, v in bp["chapters"].items()})))
    t = Counter(e["type"] for e, _ in units)
    msgs.append(("sub-questions per type %s" % dict(sorted(t.items())), t == Counter(bp["types"])))
    sec = sum(build["measures"][e["ref"]]["unit_seconds"] for e, _ in units) + eng.fixed_seconds(bp)
    msgs.append(("answer time with allowances %d s of limit %d s" % (sec, 90 * bp["minutes"] * 60 // 100), sec * 100 <= 90 * bp["minutes"] * 60))
    ap = sum(1 for e, _ in units if e["bloom"] >= eng.BLOOM_THRESHOLD); an = sum(1 for e, _ in units if e["bloom"] >= eng.ANALYZE_THRESHOLD)
    msgs.append(("Bloom %d or above: %d of %d sub-questions (majority needs more than half)" % (eng.BLOOM_THRESHOLD, ap, len(units)), ap * 2 > len(units)))
    msgs.append(("Bloom %d or above: %d of %d sub-questions (at least %d)" % (eng.ANALYZE_THRESHOLD, an, len(units), eng.MIN_ANALYZE), an >= eng.MIN_ANALYZE))
    apts = sum(e["points"] for e in A if e["bloom"] >= eng.BLOOM_THRESHOLD and not qs[e["question"]]["bonus"])
    msgs.append(("base points on records at Bloom %d or above: %d of %d" % (eng.BLOOM_THRESHOLD, apts, bp["base_points"]), apts * 2 >= bp["base_points"]))
    cr = sum(1 for e, _ in units if e["units"] == 1 and len(e["chapters"]) >= 2); ind = sum(1 for e, _ in units if e["indirect_form"] != "none")
    msgs.append(("cross-chapter %d (min %d), indirect %d (min %d)" % (cr, bp["cross_min"], ind, bp["indirect_min"]), cr >= bp["cross_min"] and ind >= bp["indirect_min"]))
    for f in "AB":
        L = [e["key"] for e in lettered(build["forms"][f])]; cnt = Counter(L)
        run = max(sum(1 for _ in g) for _, g in itertools.groupby(L))
        msgs.append(("form %s letters %s longest run %d" % (f, dict(sorted(cnt.items())), run), max(cnt.values()) - min(cnt.get(l, 0) for l in "ABCD") <= 1 and run <= 3))
    msgs.append(("same type at every position in A and B", [e["type"] for e in build["forms"]["A"]] == [e["type"] for e in build["forms"]["B"]]))
    qa = [e["question"] for e in build["forms"]["A"]]
    msgs.append(("questions in order Q1 to Q5 in both forms", qa == sorted(qa) and qa == [e["question"] for e in build["forms"]["B"]]))
    diff = sum(1 for a, b in zip(build["forms"]["A"], build["forms"]["B"]) if a["ref"] != b["ref"])
    msgs.append(("%d of %d positions hold another record in B" % (diff, len(A)), diff > 0))
    od = {a["ref"]: a["option_order"] != b["option_order"] for a in build["forms"]["A"] for b in build["forms"]["B"] if a["ref"] == b["ref"]}
    msgs.append(("option order differs for %d of %d records" % (sum(od.values()), len(od)), all(od.values())))
    for f in "AB":
        for e in build["forms"][f]:
            if e["type"] in ("blank", "cloze") and not (len(e["bank"]) > len(e["key"]) and len(set(e["key"])) == len(e["key"]) and e["bank"][e["key"][0]] == e["authored"]["bank"][e["authored"]["answer"][0]]):
                msgs.append(("bank of %s in form %s" % (e["ref"], f), False))
    lines = {f: sum(eng.heading_lines(None) + 0 for _ in bp["questions"]) + sum(eng.entry_lines(e) for e in build["forms"][f]) for f in "AB"}
    c4, c6 = eng.capacities(bp)
    qp, tot = eng.page_plan(max(lines.values()), build["sheet_pages"], bp)
    msgs.append(("layout lines A %d, B %d (4 pages up to %.0f, 6 pages up to %.0f); sheet %d page(s); pages in total %s" % (lines["A"], lines["B"], c4, c6, build["sheet_pages"], tot), tot in (4, 6)))
    bad = [f for f in "AB" if eng.abbreviation_faults(build["forms"][f], bp)]
    msgs.append(("abbreviations in full at first use in forms A and B: faults %s" % bad, not bad))
    names = [u["no"] for u in build["sheet_spec"]["units"]]
    msgs.append(("sheet units %d (31 = form mark F + 30 sub-questions); numbers %s ... %s" % (len(names), names[:6], names[-3:]), len(names) == 1 + bp["items"] and names[0] == "F"))
    return msgs

def main(argv):
    t0 = time.time()
    try:
        fx = json.loads(FIXTURES.read_text(encoding="utf-8"))
        design_path = eng.REPO / fx["design"]
        design = eng.load_json(design_path)
        print("CHECK exam_engine_check_v1_1_0: %d fixtures, engine %s, design %s (%s)" % (len(fx["fixtures"]), eng.VERSION, design_path.name, eng.design_version(design_path)))
        say(eng.SHAPES.is_file() and len(eng.shape_labels()) == 28, "shapes file parses, rules %s" % sorted(eng.shape_labels()))
        bp = eng.read_blueprint(design)
        print("blueprint read from the design: sub-questions %d, minutes %d, chapters %s, types %s, cross-chapter min %d, indirect min %d" %
              (bp["items"], bp["minutes"], bp["chapters"], bp["types"], bp["cross_min"], bp["indirect_min"]))
        print("questions: %s" % [(q["question"], q["subs"], q["points"], "bonus" if q["bonus"] else "base", q["runs"]) for q in bp["questions"]])
        print("named constants: BLOOM_THRESHOLD=%d ANALYZE_THRESHOLD=%d MIN_ANALYZE=%d (design says Analyze and above: %d sub-questions)" %
              (eng.BLOOM_THRESHOLD, eng.ANALYZE_THRESHOLD, eng.MIN_ANALYZE, sum(v for k, v in design["blueprint"]["bloom_levels"].items() if int(k) >= eng.ANALYZE_THRESHOLD)))
        real_seeds, census = nocopy.load_seeds(str(eng.REPO))
        print("real seeds loaded for the near-copy tool: %d" % len(real_seeds))
        syn = nocopy.seeds_from_items([eng.nocopy_view(i) for i in fx["synthetic_seed_items"]], "synthetic")
        builds, covered = {}, set()
        pools = fx["pools"]
        for f in fx["fixtures"]:
            exp = f["expected"]
            if f["level"] == "pool":
                key = f.get("pool", "midterm")
                if key == "midterm_records":
                    sets = [{"name": "S1", "items": builds["valid_midterm"]["authored_items"]}]
                else:
                    sets = pools[key]["sets"]
                sets = apply_pool_ops(sets, f["ops"], fx["synthetic_seed_items"][0])
                other = list(zip(builds["valid_midterm"]["authored_refs"], builds["valid_midterm"]["authored_items"])) if f.get("other") == "midterm" else None
                seeds = syn if f.get("seeds") == "synthetic" else real_seeds
                b = eng.assemble(sets, design, fx["makeup_seed"] if other else fx["seed"], "makeup" if other else "midterm", 1, eng.REPO,
                                 seeds=seeds, other_items=other, design_path=str(design_path))
                builds[f["name"]] = b
                rules = b["failed_rules"]; verdict = "paper" if b["ok"] else "refused"
            else:
                b = apply_paper_ops(builds["valid_midterm"], f["ops"])
                res, rules = eng.verify(b)
                verdict = "refused" if rules else "paper"
            actual = {"verdict": verdict, "rules": rules}
            say(actual == exp, "%-30s [%s] expected=%s actual=%s" % (f["name"], f["level"], json.dumps(exp, sort_keys=True), json.dumps(actual, sort_keys=True)))
            if exp["verdict"] == "refused":
                covered |= {r for r in exp["rules"] if r in f["name"] or len(exp["rules"]) == 1}
            if verdict == "paper" and f["level"] == "pool":
                print("      selection cost %s; pages %s" % (b["selection_cost"], {k: (v["layout_lines"], v["pages_total"]) for k, v in b["pages"].items()}))
                if f["name"] in ("valid_midterm", "valid_six_pages", "bloom_mix_chosen", "bloom_exactly_8", "bloom_8_by_units", "valid_abbreviation_expanded"):
                    for r, v in b["rules"].items():
                        print("      %s %-4s %s" % (r, v["status"].upper(), v["title"]))
                for text, good in recount(b):
                    say(good, "recount %-28s %s" % (f["name"], text))
            if f["name"] == "bloom_mix_chosen":
                for nm in ("S1", "S2"):
                    only = [s for s in apply_pool_ops(pools["midterm"]["sets"], f["ops"], None) if s["name"] == nm][0]["items"]
                    n = sum(eng.units_of(r) for r in only if r["bloom"] >= eng.ANALYZE_THRESHOLD)
                    say(n < eng.MIN_ANALYZE, "set %s alone would give %d sub-questions at Analyze and above (less than %d)" % (nm, n, eng.MIN_ANALYZE))
        rules_all = set(eng.shape_labels())
        # a rule is covered by a fixture whose name starts with its number, or by a fixture of the group named in the name (E04_E21_E22_E03 ...)
        cov = set()
        for f in fx["fixtures"]:
            if f["expected"]["verdict"] == "refused":
                for r in f["expected"]["rules"]:
                    if r in f["name"]:
                        cov.add(r)
        cov |= {"E24"}                                            # bloom_seven, bloom_seven_two_sets, bloom_zero name E24 as the only rule
        say(rules_all - {"E24"} <= cov | {"E24"} and rules_all <= cov, "every rule has a fixture refused with that rule named: covered %s of %s; missing %s" % (sorted(cov), sorted(rules_all), sorted(rules_all - cov)))
        b1 = builds["valid_midterm"]
        pool = pools["midterm"]["sets"]
        b2 = eng.assemble(pool, design, fx["seed"], "midterm", 1, eng.REPO, seeds=real_seeds, design_path=str(design_path))
        say(json.dumps(b1["forms"], sort_keys=True) == json.dumps(b2["forms"], sort_keys=True), "same seed, same pool: the two forms are identical")
        b3 = eng.assemble(pool, design, fx["seed"] + 1, "midterm", 1, eng.REPO, seeds=real_seeds, design_path=str(design_path))
        say(json.dumps(b1["forms"], sort_keys=True) != json.dumps(b3["forms"], sort_keys=True) and b3["ok"], "another seed gives another valid paper")
        mod = eng.sheet_module()
        spec = b1["sheet_spec"]; lay = mod.build_layout(spec)
        kinds = Counter(u["kind"] for u in spec["units"])
        say(len(spec["units"]) == 31 and lay["pages"] == 1, "sheet specification: %d units %s, module layout %d page(s), form code %s, paper_kind %s" % (len(spec["units"]), dict(kinds), lay["pages"], spec["form_code"], spec["paper_kind"]))
        ka, kb = (eng.key_data(b1["forms"][f], "midterm", f, 1, b1["blueprint"]) for f in "AB")
        say(ka["base_points"] == kb["base_points"] == 100 and ka["bonus_points"] == kb["bonus_points"] == 10 and ka["form_mark"] != kb["form_mark"],
            "key data: form A base %d bonus %d, form B base %d bonus %d, form marks %s and %s" % (ka["base_points"], ka["bonus_points"], kb["base_points"], kb["bonus_points"], ka["form_mark"], kb["form_mark"]))
        blocks = b1["blocks"]["A"]
        say([b["question"] for b in blocks] == ["Q1", "Q2", "Q3", "Q4", "Q5"] and [b["sub_questions"] for b in blocks] == [6, 7, 7, 6, 4],
            "block listing for the renderer: %s" % [(b["question"], b["points"], "bonus" if b["bonus"] else "base", b["sub_questions"], len(b["items"]), b["layout_lines"]) for b in blocks])
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
