#!/usr/bin/env python3
"""Check of the near-copy rule against fixtures of known answer (task TK4_Distinct_Build).
Prints expected and actual for every fixture; runs the SHACL on conforming and violating graphs;
exits 0 only when every one is as expected."""
import importlib.util, json, re, sys
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location("nc", HERE / "exam_nocopy_v1_0_0.py")
nc = importlib.util.module_from_spec(spec); spec.loader.exec_module(nc)

fails = []
def line(ok, name, expected, actual):
    print(f"{'PASS' if ok else 'FAIL'} {name} | expected {expected} | actual {actual}")
    if not ok:
        fails.append(name)

fx = json.loads((HERE / "exam_nocopy_fixtures_v1_0_0.json").read_text(encoding="utf-8"))
seeds_by_id = {s["id"]: s for s in fx["seeds"]}

def seed_records(ids):
    out = []
    for sid in ids:
        s = seeds_by_id[sid]
        if s.get("kind") == "listing":
            out.append({"id": "f:" + sid, "kind": "listing", "source": "f", "text": s["code"], "code": s["code"],
                        "answer": nc.norm(s["expected"])})
        else:
            out += nc.seeds_from_items([s], "f")
    return out

# 0. constants: fixtures, library and the SHACL file agree
from rdflib import Graph, Namespace, Literal, BNode, RDF, XSD
sg = Graph().parse(str(HERE / "exam_nocopy_shapes_v1_0_0.ttl"), format="turtle")
NC = Namespace(nc.NC)
ruling = NC.TheRuling
ttl_same = Fraction(str(sg.value(ruling, NC.sameAnswerThreshold).toPython()))
ttl_any = Fraction(str(sg.value(ruling, NC.anyAnswerThreshold).toPython()))
ttl_len = int(sg.value(ruling, NC.wordLength))
q = str(sg.value(NC.NearCopyRefusal, URIRef := __import__("rdflib").URIRef("http://www.w3.org/ns/shacl#select")))
line(ttl_same == nc.SAME_ANSWER_THRESHOLD == Fraction(str(fx["thresholds"]["same_answer"])), "threshold same answer", "0.50 in ttl, library, fixtures", f"{float(ttl_same)} / {float(nc.SAME_ANSWER_THRESHOLD)} / {fx['thresholds']['same_answer']}")
line(ttl_any == nc.ANY_ANSWER_THRESHOLD == Fraction(str(fx["thresholds"]["any_answer"])), "threshold any answer", "0.80 in ttl, library, fixtures", f"{float(ttl_any)} / {float(nc.ANY_ANSWER_THRESHOLD)} / {fx['thresholds']['any_answer']}")
line(ttl_len == 4 == fx["thresholds"]["word_length"], "sequence length", 4, ttl_len)
line("0.50" in q and "0.80" in q, "numbers inside the SPARQL constraint", "0.50 and 0.80", re.findall(r"\?c >= (0\.\d+)", q))

# 1. the fixture seed equals the bank item it names
path, pos = fx["seeds"][0]["origin"].split("#")
b = json.loads((ROOT / path).read_text(encoding="utf-8"))[int(pos)]
s0 = fx["seeds"][0]
line(b["q"] == s0["stem"] and b["options"] == s0["options"] and "ABCD"[b["answer"]] == s0["answer"], "S_values equals bank item", f"{path}#{pos}", "equal" if b["q"] == s0["stem"] and b["options"] == s0["options"] else "different")

# 2. cases
graph_of = {}
for c in fx["cases"]:
    if c["kind"] == "between_papers":
        ss = nc.seeds_from_items(fx["papers"][c["against_paper"]], "paper:" + c["against_paper"])
    else:
        ss = seed_records(c["against"])
    res = nc.measure_all([c["item"]], ss)[0]
    e = c["expected"]
    exp_c = Fraction(e["grams_shared"], e["grams_total"])
    best = max(res["comparisons"], key=lambda x: x["c"])
    sh = res["shown"]
    # actual shared / total from the measured fraction
    act = (best["c"].numerator, best["c"].denominator)
    ok_c = best["c"] == exp_c
    ok_d = True
    if "design_c" in e:
        ok_d = f"{float(best['c']):.3f}" == e["design_c"]
    ok_all = ok_c and ok_d and sh["answers_equal"] == e["answers_equal"] and sh["listing"] == e["listing"] and res["is_copy"] == e["is_copy"]
    exp_txt = f"C {float(exp_c):.3f} ({e['grams_shared']}/{e['grams_total']})" + (f" design {e['design_c']}" if "design_c" in e else "") + f", answers_equal {e['answers_equal']}, listing {e['listing']}, near copy {e['is_copy']}"
    act_txt = f"C {float(best['c']):.3f}, answers_equal {sh['answers_equal']}, listing {sh['listing']}, near copy {res['is_copy']} ({res['verdict']})"
    line(ok_all, c["id"], exp_txt, act_txt)
    graph_of[c["id"]] = (nc.to_graph([res]), res)

# 2b. the five variants again against every real seed (largest C over all seeds)
real, census = nc.load_seeds(ROOT)
print(f"real seeds: {len(real)} ({sum(n for _, n in census['banks'])} bank, {sum(n for _, n in census['quizzes'])} quiz, {sum(n for _, n in census['manifests'])} listings)")
sgm = [nc.grams(nc.words(s["text"])) for s in real]
for c in fx["cases"]:
    if c["id"].startswith("V"):
        r = nc.measure_item(c["item"], real, sgm)
        exp_copy = c["expected"]["is_copy"]
        line(r["is_copy"] == exp_copy, c["id"] + " against all real seeds", f"near copy {exp_copy}", f"near copy {r['is_copy']}, largest C {float(r['max_c']):.3f} ({r['best_seed']})")

# 3. SHACL on graphs built from the fixtures (conforming and violating)
import pyshacl
def validate(g):
    return pyshacl.validate(g, shacl_graph=sg, inference="none", advanced=True)[0]
for name, spec_g in fx["shacl_graphs"].items():
    g = Graph(); g.bind("nc", NC)
    it = NC["item/" + name]
    g.add((it, RDF.type, NC.MeasuredItem)); g.add((it, NC.itemId, Literal(name)))
    for cmp_ in spec_g["comparisons"]:
        bn = BNode()
        g.add((it, NC.comparedWith, bn)); g.add((bn, RDF.type, NC.Comparison))
        g.add((bn, NC.seedId, Literal(cmp_["seed"])))
        g.add((bn, NC.coverage, Literal(Decimal(cmp_["coverage"]), datatype=XSD.decimal)))
        g.add((bn, NC.answersEqual, Literal(cmp_["answers_equal"])))
        g.add((bn, NC.listingCopy, Literal(cmp_["listing_copy"])))
    got = validate(g)
    line(got == spec_g["expected_conforms"], "SHACL " + name, f"conforms {spec_g['expected_conforms']}", f"conforms {got}")
# a malformed graph (coverage above 1) is refused too
g = Graph(); it = NC["item/bad"]
g.add((it, RDF.type, NC.MeasuredItem)); g.add((it, NC.itemId, Literal("bad"))); bn = BNode()
g.add((it, NC.comparedWith, bn)); g.add((bn, NC.seedId, Literal("x"))); g.add((bn, NC.coverage, Literal(Decimal("1.5"), datatype=XSD.decimal)))
g.add((bn, NC.answersEqual, Literal(False))); g.add((bn, NC.listingCopy, Literal(False)))
line(validate(g) is False, "SHACL malformed (coverage 1.5)", "conforms False", f"conforms {validate(g)}")

# 4. library verdict and SHACL agree on every case
for cid, (g, res) in graph_of.items():
    got = validate(g)
    line(got == (not res["is_copy"]), "SHACL agrees with library " + cid, f"conforms {not res['is_copy']}", f"conforms {got}")

print("RESULT:", "all fixtures as expected" if not fails else f"{len(fails)} FAILED: " + ", ".join(fails))
sys.exit(0 if not fails else 1)
