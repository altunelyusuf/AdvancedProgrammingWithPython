#!/usr/bin/env python3
"""Builds exam_engine_fixtures_v1_0_0.json (task TK4_Engine_Core). ALL DATA IS SYNTHETIC: every stem, option and bank entry is made of
invented marker words and says FIXTURE; nothing is taken from a real pool of the course. The only real things the items point to are
files and critical-point entries (the item validator requires that sources exist and course points resolve).
Usage: exam_engine_fixtures_build_v1_0_0.py OUT.json     (deterministic: the same file every time)"""
import json, random, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CH = [1, 2, 3, 4, 6, 7, 8]
POINT_FILES = {1: "critical_points_ch01_04_v1_0_0.json", 2: "critical_points_ch01_04_v1_0_0.json", 3: "critical_points_ch01_04_v1_0_0.json",
               4: "critical_points_ch01_04_v1_0_0.json", 6: "critical_points_ch06_08_v1_0_0.json", 7: "critical_points_ch06_08_v1_0_0.json",
               8: "critical_points_ch06_08_v1_0_0.json"}
SYL = ["qua", "zel", "vor", "dri", "plu", "tex", "mon", "ska", "bru", "yuv", "kep", "nol", "fim", "gar", "wix", "ode", "hap", "lur", "sev", "cov"]


def word(rng, tag):
    return "".join(rng.choice(SYL) for _ in range(3)) + tag


def points_index():
    out = {}
    for ch, f in POINT_FILES.items():
        arr = json.loads((REPO / "04-assessment/exams" / f).read_text(encoding="utf-8"))
        for k, e in enumerate(arr):
            if e["chapter"] == ch:
                out[ch] = ("04-assessment/exams/%s#%d" % (f, k), e["point"], e["source_file"]); break
    return out


def make_pool(tag, seed):
    rng = random.Random(seed)
    pts = points_index()
    plan = [("mcq", False)] * 13 + [("mcq", True)] * 13 + [("predict", True)] * 8 + [("match", False)] * 4 + [("order", False)] * 4 + \
           [("blank", True)] * 5 + [("cloze", False)] * 4
    forms = ["consequence", "exception", "reason", "none", "none"]
    blooms = [2, 3, 3, 4, 4, 5, 1, 3]
    items = []
    for k, (t, code) in enumerate(plan):
        c = CH[k % 7]; c2 = CH[(k + 1) % 7]
        chapters = [c, c2] if k % 2 == 0 else [c]
        iid = "FX-%s-%02d" % (tag, k)
        w = lambda: word(rng, tag.lower())
        cps = [pts[x][0] for x in chapters]
        it = {"id": iid, "chapters": chapters, "source": [pts[c][2]], "bloom": blooms[k % 8], "critical_point": pts[c][1], "course_point": cps,
              "seed_item": "none", "type": t, "stem": "FIXTURE %s synthetic item %s: which marker belongs to %s and %s?" % (tag, iid, w(), w()),
              "listing": [], "options_or_blanks": None, "answer": None, "points": 0, "reason": "FIXTURE: synthetic reason %s %s." % (iid, w()),
              "indirect_form": forms[k % 5], "code_width": 45, "bank_id": "none"}
        if code:
            it["listing"] = ["fx_%s = %d" % (w(), k), "fx_%s = %d" % (w(), k + 1)]
        if t in ("mcq", "predict"):
            it["options_or_blanks"] = ["%s %s" % (w(), w()) for _ in range(4)]
            it["answer"] = rng.choice("ABCD"); it["points"] = 3 if t == "mcq" else 4
        elif t == "match":
            it["options_or_blanks"] = {"premises": ["%s %s" % (w(), iid) for _ in range(5)], "answers": ["%s %s" % (w(), w()) for _ in range(7)]}
            it["answer"] = [chr(65 + x) for x in rng.sample(range(7), 5)]; it["points"] = 5
        elif t == "order":
            it["options_or_blanks"] = ["%s step %s" % (w(), iid) for _ in range(4)]
            a = [1, 2, 3, 4]; rng.shuffle(a); it["answer"] = a; it["points"] = 4
        else:
            g = 3 if (t == "blank" or k % 2 == 0) else 2
            n = rng.randint(g + 1, 9)
            it["stem"] = "FIXTURE %s synthetic item %s: " % (tag, iid) + " ".join("%s [[%d]]" % (w(), j + 1) for j in range(g))
            it["options_or_blanks"] = {"gaps": g, "bank": ["%s%d" % (w(), j) for j in range(n)]}
            it["answer"] = rng.sample(range(n), g); it["points"] = g; it["bank_id"] = "fx-bank-" + iid
        items.append(it)
    return items


def synthetic_seeds():
    return [{"id": "FX-SEED-1", "type": "match", "stem": "FIXTURE seed one: which marker word pairs with the marker word zorp quil mero tavo?",
             "listing": [], "options_or_blanks": {"premises": ["fxa one", "fxa two", "fxa three", "fxa four", "fxa five"],
                                                  "answers": ["fxb one", "fxb two", "fxb three", "fxb four", "fxb five", "fxb six", "fxb seven"]},
             "answer": ["A", "B", "C", "D", "E"]}]


def main(out):
    base, other = make_pool("M", 4101), make_pool("U", 7202)
    fx = []
    P = lambda name, what, muts, rules, **kw: fx.append(dict({"name": name, "what": what, "level": "pool", "mutations": muts,
                                                                "expected": {"verdict": "refused" if rules else "paper", "rules": rules}}, **kw))
    P("valid_midterm", "the synthetic pool gives a paper; every rule passes", [], [])
    P("valid_makeup", "a second synthetic pool gives a make-up paper that repeats no item of the midterm", [], [], pool="makeup", other="midterm")
    P("E01_duplicate_id", "two records share an id", [{"op": "append_copy", "of": "FX-M-00", "id": "FX-M-00"}], ["E01"])
    P("E02_validator", "all four order items fail the item validator (empty reason)", [{"op": "set_where", "where": {"type": "order"}, "set": {"reason": ""}}], ["E02"])
    P("E03_chapter_quota", "only three items start in chapter 1, the quota is 4", [{"op": "drop_where", "first_chapter": 1, "keep": 3}], ["E03"])
    P("E04_type_count", "only one match item, the blueprint asks for two", [{"op": "drop_where", "type": "match", "keep": 1}], ["E04"])
    P("E05_time", "every mcq has a listing, so the answer time passes 90 per cent of the sitting",
      [{"op": "set_where", "where": {"type": "mcq"}, "set": {"listing": ["fx_zzz = 1", "fx_yyy = 2"]}}], ["E05"])
    P("E06_bloom", "every item at Bloom level 2", [{"op": "set_where", "where": {}, "set": {"bloom": 2}}], ["E06"])
    P("E09_cross", "no item names two chapters", [{"op": "single_chapter"}], ["E09"])
    P("E10_indirect", "no item is indirect", [{"op": "set_where", "where": {}, "set": {"indirect_form": "none"}}], ["E10"])
    P("E11_bank_size", "every bank of three gaps has three entries", [{"op": "shrink_bank"}], ["E11"])
    P("E16_near_copy_of_seed", "all match items copy a (synthetic) seed item", [{"op": "copy_of_seed", "where": {"type": "match"}}], ["E16"], seeds="synthetic")
    P("E17_makeup_repeats", "the make-up pool holds only the midterm's items", [], ["E17"], pool="midterm_items", other="midterm")
    paper = lambda name, what, ops, rules: fx.append({"name": name, "what": what, "level": "paper", "ops": ops, "expected": {"verdict": "refused", "rules": rules}})
    paper("E07_letter_spread", "form A: all 21 lettered items keyed A", [{"op": "all_letters", "form": "A", "letter": "A"}], ["E07", "E08"])
    paper("E08_letter_run", "form A: letters keep counts 6/5/5/5 but D stands four times in a row", [{"op": "letter_run", "form": "A"}], ["E08"])
    paper("E12_seed_not_stored", "form A: the seed of the first bank is removed", [{"op": "drop_bank_seed", "form": "A"}], ["E12"])
    paper("E12_seed_wrong", "form A: the stored seed does not reproduce the bank", [{"op": "wrong_bank_seed", "form": "A"}], ["E12"])
    paper("E13_gap_order", "form A: the keys of the first bank rise with the gap number", [{"op": "keys_rise", "form": "A"}], ["E13"])
    paper("E14_same_key", "form A: two gaps of one item have the same key", [{"op": "same_keys", "form": "A"}], ["E14"])
    paper("E15_three_in_a_row", "form A: bank number 0 is the key of the three gaps of the first bank (a triple in a row inside one bank also breaks E13 and E14)", [{"op": "three_in_a_row", "form": "A"}], ["E13", "E14", "E15"])
    paper("E18_type_at_position", "form B: the item at position 1 has the other lettered type", [{"op": "retype", "form": "B", "position": 1}], ["E18"])
    paper("E19_same_options", "form B: one item has the option order of form A", [{"op": "copy_option_order"}], ["E19"])
    doc = {"note": "SYNTHETIC FIXTURES for exam_engine_v1_0_0.py (task TK4_Engine_Core). Every item is invented marker text that says FIXTURE; no real pool of the course "
                   "and no personal data is used. Level 'pool': the pool (after the mutations) goes to the assembler, which must give a paper or refuse with the rules named. "
                   "Level 'paper': a rule that the assembler fulfils by construction (letters after shuffling, bank permutation, forms) cannot be broken by any pool, so the "
                   "built paper of the valid pool is changed by hand and the SHACL rules are decided on it.",
           "design": "04-assessment/exams/exam_design_v1_1_0.json", "seed": 20261102, "makeup_seed": 20261103,
           "pools": {"midterm": base, "makeup": other}, "synthetic_seed_items": synthetic_seeds(), "fixtures": fx}
    Path(out).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
