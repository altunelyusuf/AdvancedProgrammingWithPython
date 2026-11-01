#!/usr/bin/env python3
"""Builds exam_engine_fixtures_v1_1_0.json (task TK4_Engine5). ALL DATA IS SYNTHETIC: every stem, option and bank entry is made of
invented marker words and says Fixture; nothing is taken from a real pool of the course. The only real things the records point to are
files and critical-point entries (the item validator requires that sources exist and course points resolve).
A pool is a list of SETS; a set holds the 18 records (one per sub-question block: 14 single-unit records, one blank with 4 gaps, one cloze with
3 gaps, one match with 5 premises, one order with 4 steps) of exam_design_v1_2_0.json: 30 sub-questions (units) in all.
Usage: exam_engine_fixtures_build_v1_1_0.py OUT.json     (deterministic: the same file every time)"""
import json, random, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
EXD = REPO / "04-assessment/exams"
POINT_FILES = {1: "critical_points_ch01_04_v1_0_0.json", 2: "critical_points_ch01_04_v1_0_0.json", 3: "critical_points_ch01_04_v1_0_0.json",
               4: "critical_points_ch01_04_v1_0_0.json", 5: "critical_points_ch05_v1_0_0.json", 6: "critical_points_ch06_08_v1_0_0.json",
               7: "critical_points_ch06_08_v1_0_0.json", 8: "critical_points_ch06_08_v1_0_0.json"}
SYL = ["qua", "zel", "vor", "dri", "plu", "tex", "mon", "ska", "bru", "yuv", "kep", "nol", "fim", "gar", "wix", "ode", "hap", "lur", "sev", "cov"]
# id: (type, chapters, points, bloom, asks, indirect_form, listing lines, units)
SPEC = [("Q1a", "predict", [1], 4, 3, "effect", "none", 2), ("Q1b", "predict", [2], 4, 3, "effect", "none", 2), ("Q1c", "predict", [3], 4, 3, "effect", "none", 2),
        ("Q1d", "mcq", [4], 4, 4, "effect", "none", 2), ("Q1e", "mcq", [6], 4, 4, "effect", "none", 2), ("Q1f", "mcq", [7, 6], 5, 4, "effect", "none", 2),
        ("Q2a", "blank", [1, 2, 3, 4], 16, 3, "use", "none", 3), ("Q2b", "cloze", [5, 6, 8], 9, 2, "reason", "none", 0),
        ("Q3a", "match", [1, 2, 3, 4, 5], 15, 3, "use", "none", 0), ("Q3b", "mcq", [7, 1], 5, 4, "reason", "none", 0), ("Q3c", "mcq", [8, 2], 5, 4, "reason", "none", 0),
        ("Q4a", "order", [3, 5, 6, 7], 16, 3, "use", "none", 0), ("Q4b", "mcq", [8, 2], 4, 4, "effect", "consequence", 2), ("Q4c", "mcq", [4, 1], 5, 5, "effect", "exception", 0),
        ("Q5a", "mcq", [1, 2], 3, 4, "effect", "consequence", 0), ("Q5b", "mcq", [2, 3], 3, 4, "reason", "reason", 0),
        ("Q5c", "mcq", [6, 5], 2, 5, "effect", "consequence", 2), ("Q5d", "mcq", [7, 8], 2, 4, "reason", "reason", 2)]
TERMS_AT = {"Q1b": ("tuple", "A tuple is a fixed list of values that cannot be changed."),
            "Q4b": ("exception", "An exception is an error that stops the normal run of the code.")}


def points_index():
    out = {}
    for ch, f in POINT_FILES.items():
        arr = json.loads((EXD / f).read_text(encoding="utf-8"))
        for k, e in enumerate(arr):
            if e["chapter"] == ch and e["evidence_kind"] == "slide":
                out[ch] = ("04-assessment/exams/%s#%d" % (f, k), e["point"], e["source_file"]); break
    return out


def make_set(tag, seed):
    rng = random.Random(seed)
    pts = points_index()
    t = tag.lower()
    W = lambda: "".join(rng.choice(SYL) for _ in range(3)) + t
    items = []
    for (iid, ty, chs, points, bloom, asks, ind, lst) in SPEC:
        q, sub = iid[:2], iid[2]
        u = {"mcq": 1, "predict": 1, "match": 5, "order": 4, "blank": 4, "cloze": 3}[ty]
        term, tip = TERMS_AT.get(iid, (None, "none"))
        mid = "keeps %s in a %s beside %s" % (W(), term, W()) if term else "keeps %s beside %s when %s changes" % (W(), W(), W())
        stem = "Fixture %s synthetic record %s: which marker word %s?" % (tag, iid, mid)
        it = {"id": iid, "chapters": chs, "source": [pts[chs[0]][2]], "bloom": bloom, "critical_point": pts[chs[0]][1],
              "course_point": [pts[c][0] for c in dict.fromkeys(chs)], "seed_item": "none", "type": ty, "stem": stem, "listing": [],
              "options_or_blanks": None, "answer": None, "points": points, "reason": "Fixture: synthetic reason %s %s %s." % (tag, iid, W()),
              "indirect_form": ind, "code_width": 45, "bank_id": "none", "question": q, "sub": sub, "tip": tip, "terms": [term] if term else [], "asks": asks}
        if lst:
            it["listing"] = ["fx_%s%d = %d" % (t, k, k + 1) for k in range(lst)]
        if ty in ("mcq", "predict"):
            it["options_or_blanks"] = ["%s %s" % (W(), W()) for _ in range(4)]
            it["answer"] = rng.choice("ABCD")
        elif ty == "match":
            it["options_or_blanks"] = {"premises": ["%s %s %s" % (W(), iid, W()) for _ in range(5)], "answers": ["%s %s" % (W(), W()) for _ in range(7)]}
            it["answer"] = [chr(65 + x) for x in rng.sample(range(7), 5)]
        elif ty == "order":
            it["options_or_blanks"] = ["%s step %s" % (W(), W()) for _ in range(4)]
            a = [1, 2, 3, 4]; rng.shuffle(a); it["answer"] = a
        else:
            g = u
            n = g + (3 if ty == "blank" else 2)
            it["stem"] = "Fixture %s synthetic record %s: fill the numbered gaps %s so that the marker program keeps %s beside %s" % (
                tag, iid, " ".join("[[%d]]" % (j + 1) for j in range(g)), W(), W())
            it["options_or_blanks"] = {"gaps": g, "bank": ["%s%d %s" % (W(), j, W()) for j in range(n)]}
            it["answer"] = rng.sample(range(n), g); it["bank_id"] = "fx-bank-%s-%s" % (t, iid)
        items.append(it)
    return {"name": tag, "items": items}


def synthetic_seeds():
    return [{"id": "FX-SEED-1", "type": "match", "stem": "Fixture seed one: which marker word pairs with the marker word zorp quil mero tavo?",
             "listing": [], "options_or_blanks": {"premises": ["fxa one", "fxa two", "fxa three", "fxa four", "fxa five"],
                                                  "answers": ["fxb one", "fxb two", "fxb three", "fxb four", "fxb five", "fxb six", "fxb seven"]},
             "answer": ["A", "B", "C", "D", "E"]}]


def main(out):
    S1, S2, T1, T2 = make_set("S1", 5101), make_set("S2", 5102), make_set("T1", 6101), make_set("T2", 6102)
    for it in S2["items"]:
        if it["id"] == "Q5d":
            it["bloom"] = 3                                       # the second set differs from the first in one level
    fx = []
    def P(name, what, ops, rules, **kw):
        fx.append(dict({"name": name, "what": what, "level": "pool", "pool": "midterm", "ops": ops, "expected": {"verdict": "refused" if rules else "paper", "rules": rules}}, **kw))
    def A(name, what, ops, rules):
        fx.append({"name": name, "what": what, "level": "paper", "ops": ops, "expected": {"verdict": "refused", "rules": rules}})
    one = [{"op": "keep_sets", "names": ["S1"]}]
    low = lambda ids, v=3: {"op": "set_bloom", "by_id": {i: v for i in ids}}
    # ---- accepted papers
    P("valid_midterm", "two sets of 18 records give a paper of 5 questions and 30 sub-questions; every rule passes", [], [])
    P("valid_makeup", "a second pool gives a make-up paper that repeats no record of the midterm", [], [], pool="makeup", other="midterm")
    P("valid_six_pages", "the same pool with long listings and long options needs 6 pages in total, still accepted",
      one + [{"op": "long_layout", "types": ["mcq", "predict"], "lines": 12}], [])
    P("valid_abbreviation_expanded", "two stems use the short form IDE, both write its full form first: accepted",
      one + [{"op": "stem_add", "ids": ["Q1a", "Q1b"], "text": " Use the integrated development environment (IDE) tool."}], [])
    P("bloom_mix_chosen", "each of the two sets alone has 6 sub-questions at Analyze and above; the choice of records mixes them and meets the rule of 8",
      [{"op": "set_bloom", "sets": ["S1"], "by_id": {i: 3 for i in ["Q1d", "Q1e", "Q1f", "Q3b", "Q3c"]}},
       {"op": "set_bloom", "sets": ["S2"], "by_id": {i: 3 for i in ["Q4b", "Q4c", "Q5a", "Q5b"]}}], [], note="mix")
    P("bloom_exactly_8", "one set; 8 sub-questions at Analyze and above (11 minus the three at Q5b, Q5c and Q5d): accepted",
      one + [low(["Q5b", "Q5c", "Q5d"])], [])
    P("bloom_8_by_units", "one set; only Q1d, Q1e, Q1f at Analyze and above as single sub-questions and the 5-premise match record: 3 + 5 = 8 sub-questions in 4 records, accepted",
      one + [{"op": "set_bloom", "by_id": {"Q1d": 4, "Q1e": 4, "Q1f": 4, "Q3a": 4}, "default": 3}], [])
    # ---- refused papers (pool level)
    P("bloom_seven", "one set; 7 sub-questions at Analyze and above (Q5a to Q5d lowered): refused by E24 only", one + [low(["Q5a", "Q5b", "Q5c", "Q5d"])], ["E24"])
    P("bloom_seven_two_sets", "two sets, in both Q5a to Q5d are lowered: the choice cannot reach 8 and the paper is refused by E24",
      [low(["Q5a", "Q5b", "Q5c", "Q5d"])], ["E24"])
    P("bloom_zero", "one set; no record above Apply: refused by E24 only", one + [{"op": "set_bloom", "by_id": {}, "default": 3}], ["E24"])
    P("E06_apply_not_majority", "one set; 14 of 30 sub-questions at Apply and above (the 10 single records of Q1, Q3, Q4 and the order record), 11 of them at Analyze and above",
      one + [{"op": "set_bloom", "by_id": {"Q1a": 3, "Q1b": 3, "Q1c": 3, "Q1d": 4, "Q1e": 4, "Q1f": 4, "Q3b": 4, "Q3c": 4, "Q4a": 4, "Q4b": 4, "Q4c": 5}, "default": 2}], ["E06"])
    P("E25_points_below_half", "one set; 16 of 30 sub-questions at Apply and above but only 49 of the 100 base points on them",
      one + [{"op": "set_bloom", "by_id": {"Q1a": 3, "Q1b": 3, "Q1d": 4, "Q1e": 4, "Q1f": 4, "Q2b": 3, "Q3b": 4, "Q3c": 4, "Q4b": 4, "Q4c": 5, "Q5a": 4, "Q5b": 4, "Q5c": 5, "Q5d": 4}, "default": 2}], ["E25"])
    P("E01_duplicate_id", "one set holds two records with the id Q1a", one + [{"op": "dup_record", "set": "S1", "id": "Q1a"}], ["E01"])
    P("E02_validator", "the order record has an empty reason: the item validator reports R18", one + [{"op": "set_fields", "ids": ["Q4a"], "set": {"reason": ""}}], ["E02"])
    P("E03_chapter_quota", "one set; the first chapter of Q1a is changed from 1 to 2: chapter 1 has 3 sub-questions, chapter 2 has 5",
      one + [{"op": "set_fields", "ids": ["Q1a"], "set": {"chapters": [2]}}], ["E03"])
    P("E04_E21_E22_E03_missing_match", "one set without the match record: 5 sub-questions and 15 points missing from Q3 (E03 chapters, E04 type, E21 count, E22 points)",
      one + [{"op": "drop_ids", "ids": ["Q3a"]}], ["E03", "E04", "E21", "E22"])
    P("E09_cross", "one set; no one-unit record names two chapters", one + [{"op": "set_fields", "ids": ["Q1f", "Q3b", "Q3c", "Q4b", "Q4c", "Q5a", "Q5b", "Q5c", "Q5d"], "keep_first_chapter": True}], ["E09"])
    P("E10_indirect", "one set; no record is indirect", one + [{"op": "set_fields", "where_type": "any", "set": {"indirect_form": "none"}}], ["E10"])
    P("E11_bank_size", "one set; every bank has as many entries as gaps", one + [{"op": "shrink_bank"}], ["E11"])
    P("E16_near_copy_of_seed", "one set; the match record copies a (synthetic) seed item", one + [{"op": "copy_of_seed", "ids": ["Q3a"]}], ["E16"], seeds="synthetic")
    P("E17_makeup_repeats", "the make-up pool holds only the midterm's records", [], ["E17"], pool="midterm_records", other="midterm")
    P("E22_points", "one set; Q1a carries 5 points instead of 4: Q1 has 26 and the base 101", one + [{"op": "set_fields", "ids": ["Q1a"], "set": {"points": 5}}], ["E22"])
    P("E26_bare_short_form", "one set; the stem of Q1a uses the short form IDE with no full form before it", one + [{"op": "stem_add", "ids": ["Q1a"], "text": " Use the IDE tool."}], ["E26"])
    P("E21_missing_record", "one set without Q5d: Q5 has 3 sub-questions and 8 points (E21, E22) and chapter 7, type mcq, cross-chapter and indirect fall short (E03, E04, E09, E10)",
      one + [{"op": "drop_ids", "ids": ["Q5d"]}], ["E03", "E04", "E09", "E10", "E21", "E22"])
    P("list_like_set_A_incomplete", "one list like the first item set: Q3 holds 6 of 7 sub-questions, Q4 5 of 6, Q5 2 of 4 (Q3c, Q4c, Q5c, Q5d missing): refused with every rule that counts the missing units",
      one + [{"op": "drop_ids", "ids": ["Q3c", "Q4c", "Q5c", "Q5d"]}], ["E03", "E04", "E09", "E10", "E21", "E22", "E24"])
    # ---- refused papers (paper level): rules that the assembler meets by construction or that no valid pool can break
    A("E05_time", "the seconds of every sub-question are doubled", [{"op": "slow", "factor": 2}], ["E05"])
    A("E07_letter_spread", "form A: all 14 lettered records keyed A", [{"op": "all_letters", "form": "A", "letter": "A"}], ["E07", "E08"])
    A("E08_letter_run", "form A: letter counts 4/3/3/4 but D stands four times in a row", [{"op": "letter_run", "form": "A"}], ["E08"])
    A("E12_seed_not_stored", "form A: the seed of the first bank is removed", [{"op": "drop_bank_seed", "form": "A"}], ["E12"])
    A("E12_seed_wrong", "form A: the stored seed does not reproduce the bank", [{"op": "wrong_bank_seed", "form": "A"}], ["E12"])
    A("E13_gap_order", "form A: the keys of the first bank rise with the gap number", [{"op": "keys_rise", "form": "A"}], ["E13"])
    A("E14_same_key", "form A: two gaps of the first bank have the same key", [{"op": "same_keys", "form": "A"}], ["E14"])
    A("E15_three_in_a_row", "form A: bank number 0 is the key of every gap of the first bank (also E13 and E14)", [{"op": "three_in_a_row", "form": "A"}], ["E13", "E14", "E15"])
    A("E18_type_at_position", "form B: the record at position 1 has the other lettered type", [{"op": "retype", "form": "B", "position": 1}], ["E18"])
    A("E19_same_options", "form B: one record has the option order of form A", [{"op": "copy_option_order"}], ["E19"])
    A("E20_wrong_format", "Q5 holds a record of type predict in both forms (Q5 takes mcq only); the type counts change too (E04)",
      [{"op": "retype_question", "question": "Q5", "to": "predict"}], ["E04", "E20"])
    A("E23_question_order", "form B: the first record of Q1 and the first record of Q5 swap places (E18: the type at the position changes; E28: form B's unit order no longer matches the sheet built from form A)",
      [{"op": "swap_positions", "form": "B", "first_question": "Q1", "second_question": "Q5"}], ["E18", "E23", "E28"])
    A("E27_page_budget", "every listing has 40 lines: the layout does not fit in 6 pages", [{"op": "long_entries", "lines": 40}], ["E27"])
    A("E28_sheet_unit_missing", "the sheet specification loses its unit 3c", [{"op": "drop_sheet_unit", "no": "3c"}], ["E28"])
    A("E28_unit_number", "form A: a unit of the question blocks is renumbered", [{"op": "rename_unit", "form": "A", "from": "2c", "to": "2z"}], ["E28"])
    doc = {"note": "SYNTHETIC FixtureS for exam_engine_v1_1_0.py (task TK4_Engine5). Every record is invented marker text that says Fixture; no real pool of the course "
                   "and no personal data is used. Level 'pool': the pool (after the operations) goes to the assembler, which must give a paper or refuse with the rules named. "
                   "Level 'paper': a rule that the assembler meets by construction (letters after shuffling, bank permutation, the order of the forms, the sheet, the question "
                   "format) or that no pool of valid records can break (the time) cannot be broken by a pool, so the built paper of the valid pool is changed by hand and the "
                   "SHACL rules are decided on it.",
           "design": "04-assessment/exams/exam_design_v1_2_0.json", "seed": 20261102, "makeup_seed": 20261103,
           "pools": {"midterm": {"sets": [S1, S2]}, "makeup": {"sets": [T1, T2]}}, "synthetic_seed_items": synthetic_seeds(), "fixtures": fx}
    Path(out).write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
