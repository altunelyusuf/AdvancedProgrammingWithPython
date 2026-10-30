#!/usr/bin/env python3
"""Item validator for the SEN0414 printed exams, version 1.0.0 (task TK4_DesignRev).

Checks a JSON list of item records against the item model of section 2 of exam_design_v1_1_0.md.
Library:   from exam_item_check_v1_0_0 import check_items   ->  list of {"id", "rule", "message"}; an empty list is a pass.
Command line:
    exam_item_check_v1_0_0.py check ITEMS.json     prints one line per failure, exits 0 only if there is none
    exam_item_check_v1_0_0.py selftest             runs the fixtures of exam_item_check_fixtures_v1_0_0.json, prints
                                                   expected and actual for each, exits 0 only if every fixture is as expected
The validator does not judge option length or whether one answer is defensible; a person does (design section 8).
"""
import json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIXTURES = os.path.join(HERE, "exam_item_check_fixtures_v1_0_0.json")
POINTS_FILES = ("04-assessment/exams/critical_points_ch01_04_v1_0_0.json", "04-assessment/exams/critical_points_ch06_08_v1_0_0.json")

KEPT_TYPES = ("mcq", "predict", "match", "order", "blank", "cloze")
CHAPTERS = (1, 2, 3, 4, 6, 7, 8)
FIELDS = {"id": str, "chapters": list, "source": list, "bloom": int, "critical_point": str, "course_point": list, "seed_item": str,
          "type": str, "stem": str, "listing": list, "options_or_blanks": (list, dict), "answer": (str, list), "points": int,
          "reason": str, "indirect_form": str, "code_width": int, "bank_id": str}
INDIRECT = ("consequence", "exception", "reason", "none")
POINTS = {"mcq": 3, "predict": 4, "match": 5, "order": 4}      # blank and cloze: one point per gap
MAX_LISTING_LINES = 12
WIDTHS = (45, 90)
MAX_BANK = 10                                                  # the sheet's bank unit has two digit rows: serial 0 to 9
RULES = {
    "R01": "all 17 fields present, no other field, each of the right JSON type",
    "R02": "id unique in the list",
    "R03": "chapters a non-empty list among 1, 2, 3, 4, 6, 7, 8",
    "R04": "every source names a file that exists (path or path#place)",
    "R05": "bloom an integer 1 to 6",
    "R06": "every course_point resolves to an entry of the two critical-points files",
    "R07": "critical_point equals the text of the point of a resolved course_point entry",
    "R08": "seed_item is none or <bank file>#<position> inside that file",
    "R09": "type is one of the kept types",
    "R10": "answer is inside the options and in the form of the type",
    "R11": "no overlapping options",
    "R12": "no 'all of the above' or 'none of the above'",
    "R13": "listing has at most 12 lines",
    "R14": "code_width is 45 or 90 and no listing line is wider or holds a line break",
    "R15": "points equal the value fixed by the type",
    "R16": "blank and cloze: gap markers, gap count, bank size and bank_id agree",
    "R17": "indirect_form is consequence, exception, reason or none",
    "R18": "reason is a non-empty text",
}

_cache = {}
def _json(path):
    if path not in _cache:
        with open(path, encoding="utf-8") as f:
            _cache[path] = json.load(f)
    return _cache[path]

def _norm(s, kind):
    s = str(s)
    return re.sub(r"\s+", "", s) if kind == "predict" else re.sub(r"\s+", " ", s.strip().lower())

def _words(s):
    return re.findall(r"\w+", s.lower())

def _contains(shorter, longer):
    a, b = _words(shorter), _words(longer)
    if len(a) < 3 or len(a) >= len(b):
        return False
    return any(b[i:i + len(a)] == a for i in range(len(b) - len(a) + 1))

def _link(link):
    """'<path>#<n>' -> (path, n) or None."""
    m = re.fullmatch(r"(.+)#(\d+)", link) if isinstance(link, str) else None
    return (m.group(1), int(m.group(2))) if m else None

def _option_texts(it):
    t, o = it.get("type"), it.get("options_or_blanks")
    if t in ("mcq", "predict", "order") and isinstance(o, list):
        return [o]
    if t == "match" and isinstance(o, dict):
        return [o.get("premises", []), o.get("answers", [])]
    if t in ("blank", "cloze") and isinstance(o, dict):
        return [o.get("bank", [])]
    return []

def check_item(it, root=ROOT):
    """Returns a list of (rule, message) for one item record."""
    out = []
    def bad(rule, msg): out.append((rule, msg))
    if not isinstance(it, dict):
        return [("R01", "record is not an object")]
    # R01
    miss = [k for k in FIELDS if k not in it]; extra = [k for k in it if k not in FIELDS]
    wrong = [k for k, ty in FIELDS.items() if k in it and (not isinstance(it[k], ty) or (ty is int and isinstance(it[k], bool)))]
    if miss or extra or wrong:
        bad("R01", "missing %s, unknown %s, wrong type %s" % (miss, extra, wrong))
        return out                                              # the other rules need the fields
    t = it["type"]
    # R03
    ch = it["chapters"]
    if not ch or not all(isinstance(c, int) and not isinstance(c, bool) and c in CHAPTERS for c in ch):
        bad("R03", "chapters %r not a non-empty list among %s" % (ch, list(CHAPTERS)))
    # R04
    if not it["source"]:
        bad("R04", "source is empty")
    for s in it["source"]:
        p = s.split("#", 1)[0] if isinstance(s, str) else ""
        if not p or not os.path.isfile(os.path.join(root, p)):
            bad("R04", "source %r does not exist" % (s,))
    # R05
    if not (1 <= it["bloom"] <= 6):
        bad("R05", "bloom %r outside 1 to 6" % it["bloom"])
    # R06, R07
    texts = []
    if not it["course_point"]:
        bad("R06", "course_point is empty")
    for cp in it["course_point"]:
        ln = _link(cp); ok = False
        if ln:
            path, n = ln
            for pf in POINTS_FILES:
                if path in (pf, os.path.basename(pf)):
                    arr = _json(os.path.join(root, pf))
                    if 0 <= n < len(arr):
                        ok = True; texts.append(arr[n]["point"])
        if not ok:
            bad("R06", "course_point %r does not resolve" % (cp,))
    if texts and it["critical_point"] not in texts:
        bad("R07", "critical_point is not the point of any linked entry")
    # R08
    sd = it["seed_item"]
    if sd != "none":
        ln = _link(sd); ok = False
        if ln and os.path.isfile(os.path.join(root, ln[0])):
            try:
                arr = _json(os.path.join(root, ln[0])); ok = isinstance(arr, list) and 0 <= ln[1] < len(arr)
            except ValueError:
                ok = False
        if not ok:
            bad("R08", "seed_item %r does not resolve" % sd)
    # R09
    if t not in KEPT_TYPES:
        bad("R09", "type %r is not a kept type" % t)
    # R13, R14
    ls = it["listing"]
    if len(ls) > MAX_LISTING_LINES:
        bad("R13", "listing has %d lines, limit %d" % (len(ls), MAX_LISTING_LINES))
    cw = it["code_width"]
    if cw not in WIDTHS:
        bad("R14", "code_width %r is not 45 or 90" % cw)
    for i, line in enumerate(ls, 1):
        if not isinstance(line, str) or "\n" in line or (cw in WIDTHS and len(line) > cw):
            bad("R14", "listing line %d is wider than %s or holds a line break" % (i, cw))
    # R17, R18
    if it["indirect_form"] not in INDIRECT:
        bad("R17", "indirect_form %r" % it["indirect_form"])
    if not it["reason"].strip():
        bad("R18", "reason is empty")
    if t not in KEPT_TYPES:
        return out
    # type-specific shape, R10, R11, R12, R15, R16
    o, a = it["options_or_blanks"], it["answer"]
    shape = True
    if t in ("mcq", "predict"):
        shape = isinstance(o, list) and len(o) == 4 and all(isinstance(x, str) for x in o)
        if not shape: bad("R10", "%s needs a list of four option texts" % t)
        elif a not in ("A", "B", "C", "D"): bad("R10", "answer %r is not one of A, B, C, D" % (a,))
    elif t == "match":
        shape = isinstance(o, dict) and set(o) == {"premises", "answers"} and isinstance(o["premises"], list) and isinstance(o["answers"], list) and len(o["premises"]) == 5 and len(o["answers"]) == 7
        if not shape: bad("R10", "match needs 5 premises and 7 answers")
        elif not (isinstance(a, list) and len(a) == 5 and all(x in list("ABCDEFG") for x in a) and len(set(a)) == 5):
            bad("R10", "match answer must be 5 different letters among A to G")
    elif t == "order":
        shape = isinstance(o, list) and len(o) == 4 and all(isinstance(x, str) for x in o)
        if not shape: bad("R10", "order needs a list of four steps")
        elif not (isinstance(a, list) and sorted(a) == [1, 2, 3, 4]):
            bad("R10", "order answer must be a permutation of 1 to 4")
    else:                                                       # blank, cloze
        shape = isinstance(o, dict) and set(o) == {"gaps", "bank"} and isinstance(o["gaps"], int) and isinstance(o["bank"], list) and all(isinstance(x, str) for x in o["bank"])
        if not shape:
            bad("R10", "%s needs {gaps, bank}" % t)
        else:
            g, bank = o["gaps"], o["bank"]
            if not (isinstance(a, list) and len(a) == g and all(isinstance(x, int) and not isinstance(x, bool) and 0 <= x < len(bank) for x in a) and len(set(a)) == g):
                bad("R10", "answer must be %d different serials inside the bank" % g)
            marks = re.findall(r"\[\[(\d+)\]\]", it["stem"] + "\n" + "\n".join(x for x in ls if isinstance(x, str)))
            if sorted(int(m) for m in marks) != list(range(1, g + 1)):
                bad("R16", "gap markers %s do not run 1 to %d once each" % (marks, g))
            if not (1 <= len(bank) <= MAX_BANK) or len(bank) < g:
                bad("R16", "bank has %d entries for %d gaps (1 to %d, at least the gaps)" % (len(bank), g, MAX_BANK))
            if not it["bank_id"].strip() or it["bank_id"] == "none":
                bad("R16", "bank_id missing")
    if t in ("mcq", "predict", "match", "order") and it["bank_id"] != "none":
        bad("R16", "bank_id must be 'none' for type %s" % t)
    # R15
    want = POINTS.get(t, o.get("gaps") if isinstance(o, dict) and t in ("blank", "cloze") else None)
    if want is not None and it["points"] != want:
        bad("R15", "points %r, the type fixes %r" % (it["points"], want))
    # R11, R12 on every option list
    for lst in _option_texts(it):
        if not all(isinstance(x, str) for x in lst):
            continue
        keys = [_norm(x, t) for x in lst]
        if len(set(keys)) != len(keys):
            bad("R11", "two options are equal after normalising: %s" % lst)
        elif t != "predict" and any(_contains(x, y) for i, x in enumerate(lst) for j, y in enumerate(lst) if i != j):
            bad("R11", "one option is inside another: %s" % lst)
        for x in lst:
            if re.search(r"\b(all|none) of (the above|these|them)\b", x, re.I):
                bad("R12", "option %r" % x)
    return out

def check_items(items, root=ROOT):
    """items: a list of records. Returns a list of {"id", "rule", "message"}; empty means every item passes."""
    res = []
    if not isinstance(items, list):
        return [{"id": None, "rule": "R01", "message": "input is not a list of records"}]
    seen = set()
    for it in items:
        iid = it.get("id") if isinstance(it, dict) else None
        if isinstance(iid, str):
            if iid in seen or not iid.strip():
                res.append({"id": iid, "rule": "R02", "message": "id %r repeated or empty" % iid})
            seen.add(iid)
        for rule, msg in check_item(it, root):
            res.append({"id": iid, "rule": rule, "message": msg})
    return res

def selftest(path=FIXTURES):
    fx = _json(path)
    names = [f["name"] for f in fx["fixtures"]]
    allok = True
    print("SELFTEST %s: %d fixtures" % (os.path.basename(path), len(fx["fixtures"])))
    for f in fx["fixtures"]:
        got = check_items(f["items"])
        actual = {"verdict": "pass" if not got else "fail", "rules": sorted({g["rule"] for g in got})}
        ok = actual == f["expected"]
        allok &= ok
        print("%s %-28s expected=%s actual=%s" % ("OK      " if ok else "MISMATCH", f["name"], json.dumps(f["expected"], sort_keys=True), json.dumps(actual, sort_keys=True)))
    types_cov = {it["type"] for f in fx["fixtures"] if f["expected"]["verdict"] == "pass" for it in f["items"]}
    rules_cov = {r for f in fx["fixtures"] for r in f["expected"]["rules"]}
    cov_ok = types_cov == set(KEPT_TYPES) and rules_cov == set(RULES)
    print("%s coverage: valid fixture types %s of %s; defect fixtures for rules %d of %d" % ("OK      " if cov_ok else "MISMATCH", sorted(types_cov), list(KEPT_TYPES), len(rules_cov & set(RULES)), len(RULES)))
    allok &= cov_ok
    print("RESULT", "PASS" if allok else "FAIL")
    return 0 if allok else 1

def main(argv):
    if len(argv) >= 2 and argv[1] == "selftest":
        return selftest()
    if len(argv) == 3 and argv[1] == "check":
        res = check_items(_json(argv[2]))
        for r in res:
            print("FAIL %s %s %s" % (r["id"], r["rule"], r["message"]))
        print("RESULT", "FAIL" if res else "PASS", "%d failure(s)" % len(res))
        return 1 if res else 0
    print(__doc__)
    return 2

if __name__ == "__main__":
    sys.exit(main(sys.argv))
