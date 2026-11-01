#!/usr/bin/env python3
"""exam_engine_v1_1_0: the five-question assembler of the SEN0414 printed exams, with the Bloom rule enforced (task TK4_Engine5).

New file over exam_engine_v1_0_0.py, which stays unchanged and keeps its own check.
Input : a pool of item sets. One set is a JSON list of the 22-field records of exam_item_check_v1_1_0.py, ONE RECORD PER SUB-QUESTION
        (a match record holds its 5 premises, an order record its 4 steps, a blank or cloze record its gaps). The pool file is
        a list of records (one set), {"items": [...]} (one set) or {"sets": [{"name": "S1", "items": [...]}, ...]} (several sets).
        The id of a record is question plus sub (rule R23), so the same id stands once in a set (rule E01) and stands in several sets as
        the alternatives of one slot. The design file (exam_design_v1_2_0.json) gives the questions, their formats, points, sub-question
        numbers, chapter weights, cross-chapter and indirect minima, rates in seconds, allowances and page figures.
Counting: a SUB-QUESTION is one answer-sheet unit (a choice row, a match premise, an order step, a gap), as in design v1_2_0. A record
        counts for its units: 1 for mcq and predict, 5 for match, 4 for order, its gaps for blank and cloze. The 30 sub-questions of the
        design are 30 units in 18 records. Bloom, chapter, indirect and time are counted per unit (a record's value counts for each of its
        units). For a record of several units the list `chapters` names the chapter of each unit in order (cycled); a cross-chapter
        sub-question is a record of ONE unit with two or more chapters. Points belong to the record (whole numbers); the partial credit
        of a unit is the record's points divided by its units.
Output: for one seed, a paper of five questions in two forms A and B (same item type at every position; inside a question, the order of
        the records of equal type and the options differ), a build record (seed, pool file and SHA-256, design file and SHA-256, the named
        constants and assumptions, the result of every rule E01 to E28), the per-question block listing for the .docx renderer, the printed
        key data and the sheet specification in the format of the SEN0401 sheet module. No paper is rendered here (task TK4_Papers).
The rules are SHACL (exam_engine_shapes_v1_1_0.ttl). This file writes the description of a pool and a paper (build_graph) and reads the
verdict. Rules E02 and E16 use the item validator (exam_item_check_v1_1_0.py) and the near-copy tool (exam_nocopy_v1_0_0.py).

Named constants and assumptions (each is one name here and marked in every build record):
  BLOOM_THRESHOLD = 3 (Apply and above is the majority: rule E06); ANALYZE_THRESHOLD = 4 and MIN_ANALYZE = 8 (at least 8 of the 30
  sub-questions at Analyze and above: rule E24, the Owner's second Bloom clause); A7 counting in units; A8 layout figures.

Command line:
  exam_engine_v1_1_0.py build --pool POOL.json --design DESIGN.json --seed N --out DIR [--stem NAME] [--kind midterm|makeup]
                        [--paper-version V] [--midterm BUILD.json] [--root REPO]
  exam_engine_v1_1_0.py verify BUILD.json            re-decide the rules of a build record with the SHACL file
  exam_engine_v1_1_0.py rules                        list the rules
Exit 0 only when the paper was built and every rule passed; 1 when refused (the rules are named); 2 when it cannot run.
"""
import hashlib, importlib.util, itertools, json, math, os, random, re, sys
from collections import Counter
from decimal import Decimal, ROUND_FLOOR
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import exam_item_check_v1_1_0 as itemcheck           # noqa: E402
import exam_nocopy_v1_0_0 as nocopy                  # noqa: E402

VERSION = "1.1.0"
SHAPES = HERE / "exam_engine_shapes_v1_1_0.ttl"
SHEET_DIR = Path(os.environ.get("SEN0401_EXAM_DIR", "/home/claude/sen0401/08-tooling/exam"))
SHEET_MODULES = ("sen0401_exam_answersheet_v1_0_0.py", "sen0401_exam_answersheet_v1_1_0.py")
EX = "https://example.org/sen0414/exam-engine#"

# ---- the Bloom rule (the Owner's words of 2026-10-30: 'B and C, but at least 8 work-out-why' per 30 sub-questions)
BLOOM_THRESHOLD = 3          # A1: Apply and above must be the majority of the sub-questions (rule E06) and half of the base points (E25)
ANALYZE_THRESHOLD = 4        # A9: Analyze and above
MIN_ANALYZE = 8              # A10: at least this many sub-questions at Analyze and above (rule E24); the number is not buried in a rule
# ---- layout figures (A8): characters per printed line at 10 point with 12 mm margins, spare share of the last question page
CHARS_PER_LINE = 95
SPARE_SHARE = Fraction(92, 100)
MAX_PAGES = 6
FOUR_PAGES = 4
MULTI_UNIT = ("match", "order", "blank", "cloze")
PART_ORDER = ("mcq", "predict", "blank", "cloze", "match", "order")
FORMS = ("A", "B")
LETTERS = "ABCD"
UNIT_LETTERS = "abcdefghijklmnopqrstuvwxyz"
ASSUMPTIONS = {"A1": "Bloom reading Apply and above: level %d" % BLOOM_THRESHOLD,
               "A9": "Analyze and above: level %d" % ANALYZE_THRESHOLD,
               "A10": "at least %d sub-questions at Analyze and above (MIN_ANALYZE)" % MIN_ANALYZE,
               "A7": "a sub-question is one answer-sheet unit; a record counts for its units; chapters of a multi-unit record are per unit; cross-chapter only for one-unit records",
               "A8": "layout: %d characters per line, spare share %s of the last question page, at most %d pages in total" % (CHARS_PER_LINE, SPARE_SHARE, MAX_PAGES),
               "A2": "all other numbers (questions, units, points, chapters, types, minima, rates, allowances, lines per page) are read from the design file"}


class CannotRun(Exception):
    pass


# ------------------------------------------------------------------ helpers
def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def seed_int(*parts):
    return int(hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:12], 16)


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise CannotRun("%s: %s" % (path, e))


def load_pool(path):
    """-> list of sets [{"name", "items"}]. `path` may name several files separated by commas: each file is one complete list
    (the paper list, the make-up list ...) and becomes one set named after the file; a list with a repeated id is refused by E01."""
    paths = [p for p in str(path).split(",") if p]
    if len(paths) == 1:
        return pool_sets(load_json(paths[0]), paths[0])
    return [pool_sets(load_json(p), p)[0] | {"name": Path(p).stem} for p in paths]


def pool_sets(data, label="pool"):
    if isinstance(data, dict) and "sets" in data:
        sets = data["sets"]
    elif isinstance(data, dict):
        sets = [{"name": "S0", "items": data.get("items")}]
    else:
        sets = [{"name": "S0", "items": data}]
    ok = isinstance(sets, list) and all(isinstance(s, dict) and isinstance(s.get("name"), str) and isinstance(s.get("items"), list) for s in sets)
    if not ok or not all(isinstance(r, dict) and "id" in r for s in sets for r in s["items"]):
        raise CannotRun("%s: not a list of item records with an id, or a list of named sets" % label)
    return sets


def design_version(path):
    m = re.search(r"_v(\d+_\d+_\d+)\.json$", str(path))
    return m.group(1).replace("_", ".") if m else "unknown"


def units_of(it):
    """Sub-questions (sheet units) of one record."""
    t = it["type"]
    if t in ("mcq", "predict"):
        return 1
    if t == "match":
        return 5
    if t == "order":
        return 4
    return int(it["options_or_blanks"]["gaps"])


def unit_chapters(it):
    ch = it["chapters"]
    return [ch[k % len(ch)] for k in range(units_of(it))]


def read_blueprint(design):
    """The numbers of the five-question blueprint, all read from the design file."""
    try:
        bp = design["blueprint"]
        qs = []
        table = design["sub_questions"]
        for q in design["questions"]:
            rows = [r for r in table if r["question"] == q["question"]]
            runs = []
            for r in rows:
                if runs and runs[-1][0] == r["type"]:
                    runs[-1][1] += 1
                else:
                    runs.append([r["type"], 1])
            qs.append({"question": q["question"], "title": q["title"], "format": q["format"], "points": int(q["points"]), "bonus": bool(q["bonus"]),
                       "types": list(q["types"]), "subs": int(q["sub_questions"]), "runs": [(t, n) for t, n in runs]})
        out = {"items": int(bp["items"]), "minutes": int(bp["minutes"]), "chapters": {int(k): int(v) for k, v in bp["chapters"].items()},
               "types": {k: int(v) for k, v in bp["types"].items()}, "cross_min": int(bp["cross_chapter_items"]), "indirect_min": int(bp["indirect_items"]),
               "questions": qs, "base_points": int(bp["base_points"]), "bonus_points": int(bp["bonus_points"]),
               "rates": {k: int(v) for k, v in bp["arithmetic"]["rates_seconds"].items()},
               "allow": {k: int(v) for k, v in bp["arithmetic"]["allowances_seconds"].items()},
               "lines_relaxed": int(design["page_budget"]["lines_per_page_relaxed"]), "lines_dense": int(design["page_budget"]["lines_per_page_dense_v1_1_0"]),
               "cover_pages": int(design["page_budget"]["cover_pages"]), "sheet_pages_design": int(design["page_budget"]["sheet_pages_measured"])}
    except (KeyError, TypeError, ValueError) as e:
        raise CannotRun("design file: field missing or malformed: %r" % (e,))
    if sum(q["subs"] for q in qs) != out["items"] or sum(out["chapters"].values()) != out["items"] or sum(out["types"].values()) != out["items"]:
        raise CannotRun("design file: questions, chapters or types do not add up to the sub-questions of the blueprint")
    if sum(q["points"] for q in qs if not q["bonus"]) != out["base_points"] or sum(q["points"] for q in qs if q["bonus"]) != out["bonus_points"]:
        raise CannotRun("design file: question points do not add up to base and bonus points")
    for q in qs:
        if sum(n for _, n in q["runs"]) != q["subs"]:
            raise CannotRun("design file: sub-question table of %s does not match its count" % q["question"])
    return out


def slot_classes(bp):
    """Classes of records: (question, type, units per record, number of records), in print order."""
    cl = []
    for q in bp["questions"]:
        for t, n in q["runs"]:
            if t in MULTI_UNIT:
                cl.append({"question": q["question"], "type": t, "units": n, "count": 1})
            else:
                cl.append({"question": q["question"], "type": t, "units": 1, "count": n})
    return cl


def unit_seconds(it, bp):
    r, a = bp["rates"], bp["allow"]
    t = it["type"]
    base = {"mcq": r["mcq_code"] if it["listing"] else r["mcq_plain"], "predict": r["predict"], "match": r["match_premise"],
            "order": r["order_step"], "blank": r["blank_gap"], "cloze": r["cloze_gap"]}[t]
    return base + a["tip_reading_per_sub"] + a["sheet_filling_per_unit"]


def fixed_seconds(bp):
    return bp["allow"]["shared_stem_per_question"] * len(bp["questions"]) + bp["allow"]["cover_and_instructions"]


def bank_code(serial):
    """Printed two-digit code of a bank entry: its serial and the Damm check digit (module make_code)."""
    return sheet_module().make_code(serial, 1)


_sheet = {}
def sheet_module():
    if "m" not in _sheet:
        p = SHEET_DIR / SHEET_MODULES[0]
        if not p.is_file():
            raise CannotRun("sheet module not found: %s" % p)
        spec = importlib.util.spec_from_file_location("sen0401_sheet_readonly", str(p))
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            raise CannotRun("sheet module cannot be imported: %r" % (e,))
        _sheet["m"] = mod
    return _sheet["m"]


# ------------------------------------------------------------------ near-copy views
def nocopy_view(it):
    t, o, a = it["type"], it["options_or_blanks"], it["answer"]
    code = "\n".join(it.get("listing") or [])
    if t in ("mcq", "predict"):
        return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o), "answer": a}
    if t == "match":
        return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o["premises"]) + list(o["answers"]),
                "answer": [o["answers"][ord(x) - 65] for x in a]}
    if t == "order":
        return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o), "answer": [o[a.index(k)] for k in sorted(a)]}
    return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o["bank"]), "answer": [o["bank"][k] for k in a]}


def dec6(fr):
    return (Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.000001"), rounding=ROUND_FLOOR)


def measure(items, seeds):
    """Per item (by list index): (largest coverage with an equal answer, largest coverage whatever the answer, listing copy)."""
    views = []
    for k, i in enumerate(items):
        v = nocopy_view(i); v["id"] = "r%d" % k; views.append(v)
    res = nocopy.measure_all(views, seeds)
    out = []
    for r in res:
        same = max([c["c"] for c in r["comparisons"] if c["answers_equal"]] or [Fraction(0)])
        anyc = max([c["c"] for c in r["comparisons"]] or [Fraction(0)])
        out.append((same, anyc, any(c["listing_copy"] for c in r["comparisons"])))
    return out


# ------------------------------------------------------------------ the layout measure (lines are the layout unit)
def wrap_lines(s, width=CHARS_PER_LINE):
    return max(1, math.ceil(len(s) / float(width)))


def entry_lines(e):
    """Layout lines of one presented record: a spacer, the stem, the tip, the listing and the answer options."""
    n = 1 + wrap_lines(re.sub(r"\s+", " ", e["stem"]))
    if e["tip"].strip() not in ("", "none"):
        n += wrap_lines("Tip: " + e["tip"])
    t, ls = e["type"], len(e["listing"])
    if t in ("mcq", "predict"):
        opts = e["options"]
        opt = 2 if all(len(o) <= 30 for o in opts) else sum(wrap_lines(o) for o in opts)
        n += max(ls, opt) if e["code_width"] == 45 else ls + opt
    elif t == "match":
        half = CHARS_PER_LINE // 2
        n += max(sum(wrap_lines(p, half) for p in e["options"]["premises"]), sum(wrap_lines(a, half) for a in e["options"]["answers"]))
    elif t == "order":
        n += ls + sum(wrap_lines(s) for s in e["options"])
    else:
        per = 3 if all(len(b) + 4 <= 28 for b in e["bank"]) else 1
        n += ls + math.ceil(len(e["bank"]) / per)
    return n


def heading_lines(q):
    return 3


def capacities(bp):
    c4 = (FOUR_PAGES - bp["cover_pages"] - 1 - 1) * bp["lines_dense"] + SPARE_SHARE * bp["lines_dense"]       # question pages of a 4-page paper: 2
    c6 = (MAX_PAGES - bp["cover_pages"] - 1 - 1) * bp["lines_relaxed"] + SPARE_SHARE * bp["lines_relaxed"]    # question pages of a 6-page paper: 4
    return float(c4), float(c6)


def page_plan(lines, sheet_pages, bp):
    """(question pages, total pages as printed) for a paper of `lines` layout lines and a sheet of `sheet_pages`; None when over."""
    c4, c6 = capacities(bp)
    qp = 2 if lines <= c4 else (4 if lines <= c6 else None)
    if qp is None:
        return None, None
    total = bp["cover_pages"] + qp + sheet_pages
    return qp, total + (total % 2)


# ------------------------------------------------------------------ selection
def features(it, bp):
    """The numbers of one record that the selection and the rules count, per unit."""
    u = units_of(it)
    ch = Counter(unit_chapters(it))
    b = it["bloom"] if isinstance(it["bloom"], int) else 0
    return {"u": u, "ch": ch, "apply": u if b >= BLOOM_THRESHOLD else 0, "analyze": u if b >= ANALYZE_THRESHOLD else 0,
            "cross": u if (u == 1 and len(it["chapters"]) >= 2) else 0, "ind": u if it["indirect_form"] != "none" else 0,
            "sec": unit_seconds(it, bp) * u, "pts": it["points"], "apts": it["points"] if b >= BLOOM_THRESHOLD else 0}


def select(cands, classes, bp, flags, rng, restarts=14, iters=5000):
    """cands: per class a list of pool indexes. Returns (list of chosen pool indexes, cost). Exhaustive when the space is small, else seeded local search."""
    F = flags
    need_apply = bp["items"] // 2 + 1
    limit = 90 * bp["minutes"] * 60
    fixed = fixed_seconds(bp)
    qpts = {q["question"]: q["points"] for q in bp["questions"]}
    base_half = bp["base_points"]

    def cost(S):
        c = Counter(); ap = an = cr = ind = sec = 0
        qp = Counter(); apts = 0; bad = 0
        for i in S:
            f = F[i]
            c.update(f["ch"]); ap += f["apply"]; an += f["analyze"]; cr += f["cross"]; ind += f["ind"]; sec += f["sec"]
            qp[f["q"]] += f["pts"]
            if not f["bonus"]:
                apts += f["apts"]
            bad += 3 * f["bad"] + 3 * f["rep"]
        v = 4 * (sum(abs(c.get(k, 0) - q) for k, q in bp["chapters"].items()) + sum(x for k, x in c.items() if k not in bp["chapters"]))
        if (sec + fixed) * 100 > limit:
            v += 5
        v += 3 * max(0, need_apply - ap) + 3 * max(0, MIN_ANALYZE - an)
        v += 2 * max(0, bp["cross_min"] - cr) + 2 * max(0, bp["indirect_min"] - ind)
        v += 3 * sum(abs(qp.get(k, 0) - t) for k, t in qpts.items())
        if apts * 2 < base_half:
            v += 3
        return v + bad

    def choices(ci):
        cl = classes[ci]
        pool = cands[ci]
        out = []
        for sub in itertools.combinations(pool, min(cl["count"], len(pool))):
            if len({F[i]["id"] for i in sub}) == len(sub):
                out.append(sub)
        return out or [tuple()]
    options = [choices(ci) for ci in range(len(classes))]
    space = 1
    for o in options:
        space *= len(o)
        if space > 30000:
            break
    if space <= 30000:
        best, bc = None, None
        order = [list(range(len(o))) for o in options]
        for o in order:
            rng.shuffle(o)
        for combo in itertools.product(*order):
            S = [i for ci, k in enumerate(combo) for i in options[ci][k]]
            c = cost(S)
            if bc is None or c < bc:
                best, bc = S, c
                if bc == 0:
                    break
        return best, bc
    best, bc = None, None
    for _ in range(restarts):
        pick = [rng.randrange(len(o)) for o in options]
        S = lambda: [i for ci, k in enumerate(pick) for i in options[ci][k]]
        cur = cost(S())
        for it in range(iters):
            if cur == 0:
                break
            T = 2.0 * (1 - it / iters) + 0.05
            ci = rng.randrange(len(options))
            if len(options[ci]) < 2:
                continue
            old = pick[ci]
            pick[ci] = rng.randrange(len(options[ci]))
            c2 = cost(S())
            if c2 <= cur or rng.random() < math.exp((cur - c2) / T):
                cur = c2
            else:
                pick[ci] = old
        if bc is None or cur < bc:
            best, bc = S(), cur
        if bc == 0:
            break
    return best, bc


# ------------------------------------------------------------------ presenting the forms
def targets_for_letters(n, rng):
    base, extra = divmod(n, 4)
    plus = rng.sample(range(4), extra)
    seq = [LETTERS[k] for k in range(4) for _ in range(base + (1 if k in plus else 0))]
    for _ in range(5000):
        rng.shuffle(seq)
        if not any(len(set(seq[i:i + 4])) == 1 for i in range(len(seq) - 3)):
            return seq
    raise CannotRun("no letter order without a run of four found")


def perm_of(n, rng, avoid=()):
    p = list(range(n))
    for _ in range(200):
        p = list(range(n)); rng.shuffle(p)
        if p not in avoid:
            return p
    return p


def present_item(it, ref, pos, target, rng, avoid_sig):
    t, o, a = it["type"], it["options_or_blanks"], it["answer"]
    e = {"position": pos, "id": it["id"], "ref": ref, "question": it["question"], "sub": it["sub"], "type": t, "units": units_of(it),
         "chapters": list(it["chapters"]), "points": it["points"], "bloom": it["bloom"], "asks": it["asks"], "indirect_form": it["indirect_form"],
         "tip": it["tip"], "terms": list(it["terms"]), "reason": it["reason"], "stem": it["stem"], "listing": list(it["listing"]),
         "code_width": it["code_width"]}
    if t in ("mcq", "predict"):
        ci = ord(a) - 65
        for _ in range(60):
            others = [i for i in range(4) if i != ci]; rng.shuffle(others)
            order = others[:]; order.insert(LETTERS.index(target), ci)
            if "|".join(map(str, order)) != avoid_sig:
                break
        e["options"] = [o[i] for i in order]; e["key"] = target; e["option_order"] = "|".join(map(str, order))
    elif t == "match":
        for _ in range(60):
            pp = perm_of(5, rng); sp = perm_of(7, rng)
            sig = "P%s|A%s" % ("".join(map(str, pp)), "".join(map(str, sp)))
            if sig != avoid_sig:
                break
        e["options"] = {"premises": [o["premises"][i] for i in pp], "answers": [o["answers"][i] for i in sp]}
        e["key"] = [chr(65 + sp.index(ord(a[i]) - 65)) for i in pp]; e["option_order"] = sig
    elif t == "order":
        for _ in range(60):
            pp = perm_of(4, rng)
            sig = "S" + "".join(map(str, pp))
            if sig != avoid_sig and [a[i] for i in pp] != [1, 2, 3, 4]:
                break
        e["options"] = [o[i] for i in pp]; e["key"] = [a[i] for i in pp]; e["option_order"] = sig
    else:
        e["authored"] = {"bank": list(o["bank"]), "answer": list(a)}
        e["gaps"] = o["gaps"]; e["bank_id"] = it["bank_id"]
    return e


def bank_perm(seed, n):
    p = list(range(n)); random.Random(seed).shuffle(p); return p


def present_banks(entries, master, form, avoid_sigs):
    """For each fill-in record in position order a seeded bank permutation that satisfies E13, E14, E15."""
    seq = []
    for e in sorted(entries, key=lambda x: x["position"]):
        if e["type"] not in ("blank", "cloze"):
            continue
        bank, ans = e["authored"]["bank"], e["authored"]["answer"]
        ok = None
        for attempt in range(400):
            s = seed_int(master, form, e["ref"], attempt)
            perm = bank_perm(s, len(bank))
            keys = [perm.index(x) for x in ans]
            sig = "B" + "".join(map(str, perm))
            if sig == avoid_sigs.get(e["ref"]):
                continue
            if len(keys) >= 2 and all(keys[i] < keys[i + 1] for i in range(len(keys) - 1)):
                continue
            if len(set(keys)) != len(keys):
                continue
            cand = seq + keys
            if any(len(set(cand[i:i + 3])) == 1 for i in range(max(0, len(seq) - 2), len(cand) - 2)):
                continue
            ok = (s, perm, keys, sig, attempt); break
        if ok is None:
            ok = (s, perm, keys, sig, attempt)                    # kept: the SHACL rules name the failure
        s, perm, keys, sig, attempt = ok
        e["bank"] = [bank[i] for i in perm]
        e["bank_codes"] = [bank_code(k) for k in range(len(bank))]
        e["key"] = keys
        e["bank_seed"] = s; e["bank_attempt"] = attempt; e["option_order"] = sig
        seq += keys


def number_units(entries):
    """Sheet unit numbers: question digit plus a running letter inside the question, in print order."""
    count = Counter()
    for e in sorted(entries, key=lambda x: x["position"]):
        nums = []
        for _ in range(e["units"]):
            k = count[e["question"]]; count[e["question"]] += 1
            nums.append(e["question"][1:] + UNIT_LETTERS[k])
        e["unit_numbers"] = nums


def build_forms(selected, bp, master):
    """selected: list of (ref, record). Questions in design order; inside a question the types in the design's order of runs;
    inside a group of equal type form A and form B order the records differently."""
    groups = {}
    for ref, it in selected:
        groups.setdefault((it["question"], it["type"]), []).append((ref, it))
    order = []
    for q in bp["questions"]:
        for t, _ in q["runs"]:
            if (q["question"], t) not in order:
                order.append((q["question"], t))
    rng = random.Random(seed_int(master, "order"))
    seqA, seqB = [], []
    for key in order:
        g = sorted(groups.get(key, []), key=lambda x: x[1]["id"])
        rng.shuffle(g); seqA += g
        h = g[:]
        for _ in range(500):
            rng.shuffle(h)
            if len(g) < 2 or all(x[0] != y[0] for x, y in zip(g, h)):
                break
        seqB += h
    forms, sigs = {}, {}
    for form, seq in (("A", seqA), ("B", seqB)):
        r = random.Random(seed_int(master, "options", form))
        lettered = [x for x in seq if x[1]["type"] in ("mcq", "predict")]
        targets = targets_for_letters(len(lettered), r)
        entries, li = [], 0
        for pos, (ref, it) in enumerate(seq, 1):
            tgt = None
            if it["type"] in ("mcq", "predict"):
                tgt = targets[li]; li += 1
            entries.append(present_item(it, ref, pos, tgt, r, sigs.get(ref)))
        present_banks(entries, master, form, sigs)
        number_units(entries)
        if form == "A":
            sigs = {e["ref"]: e["option_order"] for e in entries}
        forms[form] = entries
    return forms


# ------------------------------------------------------------------ blocks, text, layout
def blocks_of(entries, bp):
    """The per-question block listing for the .docx renderer (task TK4_Papers)."""
    out = []
    for q in bp["questions"]:
        es = sorted((e for e in entries if e["question"] == q["question"]), key=lambda x: x["position"])
        lines = heading_lines(q) + sum(entry_lines(e) for e in es)
        out.append({"question": q["question"], "title": q["title"], "instruction": q["format"], "points": q["points"], "bonus": q["bonus"],
                    "sub_questions": sum(e["units"] for e in es), "layout_lines": lines,
                    "items": [{k: v for k, v in e.items() if k != "authored"} for e in es]})
    return out


def entry_text(e):
    parts = [e["stem"]]
    parts += [x.split("#", 1)[1] for x in e["listing"] if isinstance(x, str) and "#" in x]
    t = e["type"]
    if t in ("mcq", "predict", "order"):
        parts += e["options"]
    elif t == "match":
        parts += e["options"]["premises"] + e["options"]["answers"]
    else:
        parts += e["bank"]
    if e["tip"].strip() != "none":
        parts.append(e["tip"])
    return "\n".join(parts)


def form_text(entries, bp):
    """The text of the question blocks in print order: question title, instruction, then every record."""
    out = []
    for q in bp["questions"]:
        out.append(q["title"]); out.append(q["format"])
        for e in sorted((x for x in entries if x["question"] == q["question"]), key=lambda x: x["position"]):
            out.append(entry_text(e))
    return "\n".join(out)


def abbreviation_faults(entries, bp):
    res = []
    for sh in itemcheck.abbreviation_scan(form_text(entries, bp)):
        res.append(sh)
    return res


# ------------------------------------------------------------------ sheet specification and key
def unit_list(e):
    """Units of one presented record: (no, kind, options, answer text, points)."""
    t, nums = e["type"], e["unit_numbers"]
    pts = Fraction(e["points"], e["units"])
    if t in ("mcq", "predict"):
        return [(nums[0], "choice", "ABCD", e["key"], pts)]
    if t == "match":
        return [(nums[k], "match", "ABCDEFG", e["key"][k], pts) for k in range(5)]
    if t == "order":
        return [(nums[k], "order", "1234", str(e["key"][k]), pts) for k in range(4)]
    return [(nums[k], "bank", None, bank_code(e["key"][k]), pts) for k in range(e["gaps"])]


def sheet_spec(entries, kind, paper_version):
    mod = sheet_module()
    units = [{"no": "F", "kind": "bank", "digits": 2}]
    for e in sorted(entries, key=lambda x: x["position"]):
        for no, k, opts, _, _ in unit_list(e):
            units.append({"no": no, "kind": k, "digits": 2} if k == "bank" else {"no": no, "kind": k, "opts": opts})
    pk = "Midterm" if kind == "midterm" else "MakeUp"
    return {"paper_kind": pk, "paper_version": paper_version,
            "form_code": mod.make_code(1000 + paper_version * 10 + (0 if kind == "midterm" else 1), 4), "units": units}


def sheet_pages(spec):
    return int(sheet_module().build_layout(spec)["pages"])


def form_mark(kind, form):
    serial = {("midterm", "A"): 0, ("midterm", "B"): 1, ("makeup", "A"): 2, ("makeup", "B"): 3}[(kind, form)]
    return {"serial": serial, "code": bank_code(serial)}


def key_data(entries, kind, form, paper_version, bp):
    items = []
    for e in sorted(entries, key=lambda x: x["position"]):
        us = [{"unit": no, "kind": k, "answer": ans, "points": str(p)} for no, k, _, ans, p in unit_list(e)]
        k = {"position": e["position"], "id": e["id"], "ref": e["ref"], "question": e["question"], "type": e["type"], "units": us,
             "points": e["points"], "bonus": next(q["bonus"] for q in bp["questions"] if q["question"] == e["question"]),
             "chapters": e["chapters"], "bloom": e["bloom"], "reason": e["reason"], "tip": e["tip"]}
        if e["type"] in ("blank", "cloze"):
            k["bank_numbers"] = e["key"]
        items.append(k)
    body = {"kind": kind, "form": form, "paper_version": paper_version, "form_mark": form_mark(kind, form), "items": items,
            "base_points": sum(i["points"] for i in items if not i["bonus"]), "bonus_points": sum(i["points"] for i in items if i["bonus"])}
    body["content_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return body


def layout_figures(build):
    """Per form: layout lines and, from the sheet, the page plan. Used by build_graph and by the check."""
    bp = build["blueprint"]
    out = {}
    for f, es in build["forms"].items():
        lines = sum(b["layout_lines"] for b in blocks_of(es, bp))
        out[f] = {"lines": lines}
    return out


# ------------------------------------------------------------------ SHACL description and verdict
def _id(s):
    return re.sub(r"[^A-Za-z0-9_.-]", "_", s)


def build_graph(build):
    from rdflib import Graph, Namespace, Literal, RDF, XSD, BNode
    ex = Namespace(EX)
    g = Graph(); g.bind("ex", ex)
    bp = build["blueprint"]; asm = build["assumptions"]
    P = ex["paper"]
    c4, c6 = capacities(bp)
    g.add((P, RDF.type, ex.Paper))
    for name, val in (("minutes", bp["minutes"]), ("bloomThreshold", asm["bloom_threshold"]), ("analyzeThreshold", asm["analyze_threshold"]),
                      ("minAnalyze", asm["min_analyze"]), ("crossMin", bp["cross_min"]), ("indirectMin", bp["indirect_min"]),
                      ("basePoints", bp["base_points"]), ("bonusPoints", bp["bonus_points"]), ("subTotal", bp["items"]),
                      ("fixedSeconds", fixed_seconds(bp)), ("coverPages", bp["cover_pages"]), ("maxPages", MAX_PAGES)):
        g.add((P, ex[name], Literal(val)))
    g.add((P, ex.capacityFour, Literal(c4, datatype=XSD.double))); g.add((P, ex.capacitySix, Literal(c6, datatype=XSD.double)))
    for c, q in bp["chapters"].items():
        b = BNode(); g.add((P, ex.hasChapterQuota, b)); g.add((b, RDF.type, ex.ChapterQuota)); g.add((b, ex.chapter, Literal(int(c)))); g.add((b, ex.quota, Literal(q)))
    for t, q in bp["types"].items():
        b = BNode(); g.add((P, ex.hasTypeQuota, b)); g.add((b, RDF.type, ex.TypeQuota)); g.add((b, ex.itemType, Literal(t))); g.add((b, ex["count"], Literal(q)))
    for q in bp["questions"]:
        b = BNode(); g.add((P, ex.hasQuestionQuota, b)); g.add((b, RDF.type, ex.QuestionQuota)); g.add((b, ex.question, Literal(q["question"])))
        g.add((b, ex.subs, Literal(q["subs"]))); g.add((b, ex.pointsTarget, Literal(q["points"]))); g.add((b, ex.bonus, Literal(q["bonus"])))
        for t in q["types"]:
            a = BNode(); g.add((a, RDF.type, ex.QuestionType)); g.add((a, ex.question, Literal(q["question"]))); g.add((a, ex.itemType, Literal(t)))
    for k, pid in enumerate(build["pool_ids"]):
        n = ex["pool/%d" % k]; g.add((n, RDF.type, ex.PoolRecord)); g.add((n, ex.poolId, Literal(pid)))
    for l in LETTERS:
        g.add((ex["letter/" + l], RDF.type, ex.Letter))
    forms = build["forms"]
    first = forms[FORMS[0]] if FORMS[0] in forms else []
    for e in first:
        n = ex["item/" + _id(e["ref"])]
        m = build["measures"][e["ref"]]
        g.add((n, RDF.type, ex.PaperItem)); g.add((n, ex.inPaper, P)); g.add((n, ex.itemId, Literal(e["ref"])))
        g.add((n, ex.question, Literal(e["question"]))); g.add((n, ex.itemType, Literal(e["type"]))); g.add((n, ex.units, Literal(e["units"])))
        g.add((n, ex.points, Literal(e["points"]))); g.add((n, ex.bloom, Literal(m["bloom"])))
        g.add((n, ex.validatorFailures, Literal(m["validator_failures"])))
        for name, key in (("maxCoverageSame", "max_same"), ("maxCoverageAny", "max_any"), ("otherMaxCoverageSame", "other_max_same"), ("otherMaxCoverageAny", "other_max_any")):
            g.add((n, ex[name], Literal(Decimal(m[key]), datatype=XSD.decimal)))
        g.add((n, ex.listingCopy, Literal(bool(m["listing_copy"])))); g.add((n, ex.otherIdRepeated, Literal(bool(m["other_id_repeated"]))))
        g.add((n, ex.otherListingCopy, Literal(bool(m["other_listing_copy"]))))
        # one SubQuestion per unit: the unit is what the rules count
        chs = [e["chapters"][k % len(e["chapters"])] for k in range(e["units"])]
        for k in range(e["units"]):
            s = ex["sub/%s/%d" % (_id(e["ref"]), k)]
            g.add((s, RDF.type, ex.SubQuestion)); g.add((s, ex.inPaper, P)); g.add((s, ex.ofItem, n)); g.add((s, ex.question, Literal(e["question"])))
            g.add((s, ex.chapter, Literal(chs[k]))); g.add((s, ex.itemType, Literal(e["type"]))); g.add((s, ex.seconds, Literal(m["unit_seconds"])))
            g.add((s, ex.bloom, Literal(m["bloom"]))); g.add((s, ex.cross, Literal(bool(e["units"] == 1 and len(e["chapters"]) >= 2))))
            g.add((s, ex.indirect, Literal(bool(m["indirect"]))))
    lay = layout_figures(build)
    for form, entries in forms.items():
        F = ex["form/" + form]; g.add((F, RDF.type, ex.Form)); g.add((F, ex.formName, Literal(form)))
        g.add((F, ex.layoutLines, Literal(lay[form]["lines"]))); g.add((F, ex.sheetPages, Literal(build["sheet_pages"])))
        for sh in abbreviation_faults(entries, bp):
            a = ex["abbr/%s/%s" % (form, sh)]; g.add((a, RDF.type, ex.AbbrFault)); g.add((a, ex.inForm, F)); g.add((a, ex.short, Literal(sh)))
        sizes = Counter((e["question"], e["type"]) for e in entries)
        rank = 0; seq = 0; useq = 0
        for e in sorted(entries, key=lambda x: x["position"]):
            item = ex["item/" + _id(e["ref"])]
            pr = ex["presented/%s/%d" % (form, e["position"])]
            g.add((pr, RDF.type, ex.Presented)); g.add((pr, ex.inForm, F)); g.add((pr, ex.forItem, item)); g.add((pr, ex.position, Literal(e["position"])))
            g.add((pr, ex.itemType, Literal(e["type"]))); g.add((pr, ex.question, Literal(e["question"])))
            g.add((pr, ex.groupSize, Literal(sizes[(e["question"], e["type"])])))
            g.add((pr, ex.optionOrder, Literal(e.get("option_order", ""))))
            for no in e["unit_numbers"]:
                useq += 1
                kind = {"mcq": "choice", "predict": "choice", "match": "match", "order": "order", "blank": "bank", "cloze": "bank"}[e["type"]]
                u = ex["block/%s/%d" % (form, useq)]
                g.add((u, RDF.type, ex.BlockUnit)); g.add((u, ex.inForm, F)); g.add((u, ex.seq, Literal(useq))); g.add((u, ex.unitNo, Literal(no)))
                g.add((u, ex.kind, Literal(kind))); g.add((u, ex.question, Literal(e["question"])))
                g.add((u, ex.ordinal, Literal(UNIT_LETTERS.index(no[1:]) + 1 if no[1:] in UNIT_LETTERS else 0)))
            if e["type"] in ("mcq", "predict"):
                rank += 1
                k = ex["keyed/%s/%d" % (form, e["position"])]
                g.add((k, RDF.type, ex.Keyed)); g.add((k, ex.inForm, F)); g.add((k, ex.rank, Literal(rank))); g.add((k, ex.keyLetter, ex["letter/" + str(e["key"])]))
            if e["type"] in ("blank", "cloze"):
                B = ex["bank/%s/%d" % (form, e["position"])]
                g.add((B, RDF.type, ex.Bank)); g.add((B, ex.inForm, F)); g.add((B, ex.forItem, item))
                g.add((B, ex.entries, Literal(len(e["bank"])))); g.add((B, ex.gaps, Literal(len(e["key"]))))
                if e.get("bank_seed") is not None:
                    g.add((B, ex.bankSeed, Literal(e["bank_seed"])))
                    perm = bank_perm(e["bank_seed"], len(e["authored"]["bank"]))
                    g.add((B, ex.reproduced, Literal([e["authored"]["bank"][i] for i in perm] == e["bank"])))
                else:
                    g.add((B, ex.reproduced, Literal(False)))
                for gi, key in enumerate(e["key"], 1):
                    seq += 1
                    G = ex["gap/%s/%d/%d" % (form, e["position"], gi)]
                    g.add((G, RDF.type, ex.Gap)); g.add((G, ex.inBank, B)); g.add((G, ex.inForm, F))
                    g.add((G, ex.gapNo, Literal(gi))); g.add((G, ex.seq, Literal(seq))); g.add((G, ex.key, Literal(key)))
    g.add((P, ex.formMarkUnit, Literal(bool(build["sheet_spec"]["units"] and build["sheet_spec"]["units"][0]["no"] == "F"))))
    for k, u in enumerate([u for u in build["sheet_spec"]["units"] if u["no"] != "F"], 1):
        s = ex["sheet/%d" % k]; g.add((s, RDF.type, ex.SheetUnit)); g.add((s, ex.seq, Literal(k))); g.add((s, ex.unitNo, Literal(u["no"]))); g.add((s, ex.kind, Literal(u["kind"])))
    return g


_labels = {}
def shape_labels():
    if not _labels:
        from rdflib import Graph, RDFS
        sg = Graph().parse(str(SHAPES), format="turtle")
        for s, _, o in sg.triples((None, RDFS.label, None)):
            name = str(s).split("#")[-1]
            if re.fullmatch(r"E\d\d", name):
                _labels[name] = str(o)
    return _labels


def decide(build):
    """Runs the SHACL shapes on the description of a build. Returns {rule: {title, status, messages}}."""
    import pyshacl
    from rdflib import Graph, Namespace, RDF
    SH = Namespace("http://www.w3.org/ns/shacl#")
    sg = Graph().parse(str(SHAPES), format="turtle")
    conforms, rg, _ = pyshacl.validate(build_graph(build), shacl_graph=sg, inference="none", advanced=True)
    out = {r: {"title": t, "status": "pass", "messages": []} for r, t in sorted(shape_labels().items())}
    for res in rg.subjects(RDF.type, SH.ValidationResult):
        src = rg.value(res, SH.sourceShape)
        parent = sg.value(None, SH.property, src)
        shape = str(parent if parent is not None else src).split("#")[-1]
        shape = shape[:3] if re.match(r"E\d\d", shape) else shape         # a rule may have helper shapes: E23b and E28b report under E23 and E28
        msg = str(rg.value(res, SH.resultMessage))
        focus = str(rg.value(res, SH.focusNode)).replace(EX, "ex:")
        if shape in out:
            out[shape]["status"] = "fail"
            if (msg, focus) not in [(m["message"], m["focus"]) for m in out[shape]["messages"]]:
                out[shape]["messages"].append({"message": msg, "focus": focus})
    if conforms and any(v["status"] == "fail" for v in out.values()):
        raise CannotRun("internal: SHACL conforms but a rule failed")
    return out


def failed(results):
    return sorted(r for r, v in results.items() if v["status"] == "fail")


# ------------------------------------------------------------------ assemble
def _usable(i):
    """The engine can only read a record that has the fields it uses; the validator reports the rest (E02)."""
    try:
        t = i["type"]
        if not (isinstance(i["chapters"], list) and i["chapters"] and isinstance(i["bloom"], int) and t in PART_ORDER and isinstance(i["listing"], list)
                and "indirect_form" in i and isinstance(i["points"], int) and isinstance(i["question"], str) and isinstance(i["sub"], str)
                and isinstance(i["tip"], str) and isinstance(i["terms"], list) and isinstance(i["asks"], str) and isinstance(i["reason"], str)):
            return False
        o = i["options_or_blanks"]
        if t in ("mcq", "predict", "order"):
            return isinstance(o, list) and len(o) == 4 and i["answer"] is not None
        if t == "match":
            return isinstance(o, dict) and len(o.get("premises", [])) == 5 and len(o.get("answers", [])) == 7 and isinstance(i["answer"], list) and len(i["answer"]) == 5
        return isinstance(o, dict) and isinstance(o.get("gaps"), int) and isinstance(o.get("bank"), list) and isinstance(i["answer"], list) and len(i["answer"]) == o["gaps"]
    except (KeyError, TypeError):
        return False


def assemble(sets, design, seed, kind="midterm", paper_version=1, root=REPO, seeds=None, other_items=None,
             pool_path=None, design_path=None):
    """Builds the paper of a seed. sets: list of {"name","items"}. other_items: [(ref, record)] of the other paper (E17).
    Returns the build record; build["ok"] is true only when every rule passed."""
    bp = read_blueprint(design)
    master = "%s|%s" % (kind, seed)
    refs = ["%s/%s" % (s["name"], r.get("id")) for s in sets for r in s["items"]]
    build = {"engine_version": VERSION, "kind": kind, "paper_version": paper_version, "seed": seed, "blueprint": bp,
             "assumptions": {"bloom_threshold": BLOOM_THRESHOLD, "analyze_threshold": ANALYZE_THRESHOLD, "min_analyze": MIN_ANALYZE, "notes": ASSUMPTIONS},
             "pool_ids": refs, "pool_file": pool_path, "design_file": design_path,
             "design_version": design_version(design_path) if design_path else "unknown", "forms": {}, "measures": {}}
    if pool_path and Path(pool_path).is_file():
        build["pool_sha256"] = sha256_file(pool_path)
    if design_path and Path(design_path).is_file():
        build["design_sha256"] = sha256_file(design_path)
    if len(set(refs)) != len(refs) or len({s["name"] for s in sets}) != len(sets):          # E01: the pool is ambiguous; nothing else is decided
        build["rules"] = decide_pool_only(build)
        build["failed_rules"] = failed(build["rules"])
        build["ok"] = False
        return build
    flat = [(s["name"], r) for s in sets for r in s["items"]]
    for _, r in flat:
        if not isinstance(r, dict):
            raise CannotRun("pool record is not an object")
    fails = {}
    for k, (_, r) in enumerate(flat):
        fails[k] = itemcheck.check_item(r, str(root))
    usable = [k for k, (_, r) in enumerate(flat) if _usable(r)]
    if seeds is None:
        seeds, _ = nocopy.load_seeds(str(root))
    items_u = [flat[k][1] for k in usable]
    m_seed = measure(items_u, seeds) if items_u else []
    other_refs = {ref for ref, _ in (other_items or [])}
    other_seeds = nocopy.seeds_from_items([nocopy_view(r) for _, r in other_items], "other") if other_items else []
    m_other = measure(items_u, other_seeds) if (other_seeds and items_u) else [(Fraction(0), Fraction(0), False)] * len(items_u)
    flags = {}
    for j, k in enumerate(usable):
        name, r = flat[k]
        s, a, lc = m_seed[j]; os_, oa, olc = m_other[j]
        copy = (a >= nocopy.ANY_ANSWER_THRESHOLD) or (s >= nocopy.SAME_ANSWER_THRESHOLD) or lc
        ref = "%s/%s" % (name, r["id"])
        rep = ref in other_refs or (oa >= nocopy.ANY_ANSWER_THRESHOLD) or (os_ >= nocopy.SAME_ANSWER_THRESHOLD) or olc
        f = features(r, bp)
        f.update({"id": r["id"], "q": r["question"], "bonus": any(q["question"] == r["question"] and q["bonus"] for q in bp["questions"]),
                  "bad": 1 if (fails[k] or copy) else 0, "rep": 1 if rep else 0, "ref": ref, "m": (s, a, lc, os_, oa, olc)})
        flags[k] = f
    classes = slot_classes(bp)
    cands = [[k for k in usable if flat[k][1]["question"] == c["question"] and flat[k][1]["type"] == c["type"]
              and (c["units"] == 1 or units_of(flat[k][1]) == c["units"])] for c in classes]
    rng = random.Random(seed_int(master, "select"))
    idxs, cost = select(cands, classes, bp, flags, rng)
    chosen = sorted(idxs, key=lambda k: (flat[k][1]["question"], flat[k][1]["id"], flat[k][0]))
    selected = [(flags[k]["ref"], flat[k][1]) for k in chosen]
    build["selection_cost"] = cost
    for k in chosen:
        f = flags[k]; r = flat[k][1]; s, a, lc, os_, oa, olc = f["m"]
        build["measures"][f["ref"]] = {"unit_seconds": unit_seconds(r, bp), "bloom": r["bloom"], "indirect": r["indirect_form"] != "none",
                                       "validator_failures": len(fails[k]), "max_same": str(dec6(s)), "max_any": str(dec6(a)), "listing_copy": lc,
                                       "other_id_repeated": f["ref"] in other_refs, "other_max_same": str(dec6(os_)), "other_max_any": str(dec6(oa)),
                                       "other_listing_copy": olc}
    build["forms"] = build_forms(selected, bp, master)
    build["authored_items"] = [r for _, r in selected]
    build["authored_refs"] = [ref for ref, _ in selected]
    build["sheet_spec"] = sheet_spec(build["forms"]["A"], kind, paper_version)
    build["sheet_pages"] = sheet_pages(build["sheet_spec"])
    build["sheet_modules"] = {n: {"path": str(SHEET_DIR / n), "sha256": sha256_file(SHEET_DIR / n)} for n in SHEET_MODULES if (SHEET_DIR / n).is_file()}
    build["rules"] = decide(build)
    build["failed_rules"] = failed(build["rules"])
    build["ok"] = not build["failed_rules"]
    build["blocks"] = {f: blocks_of(es, bp) for f, es in build["forms"].items()}
    lay = layout_figures(build)
    build["pages"] = {f: dict(zip(("question_pages", "pages_total"), page_plan(lay[f]["lines"], build["sheet_pages"], bp)), layout_lines=lay[f]["lines"],
                                sheet_pages=build["sheet_pages"]) for f in lay}
    return build


def decide_pool_only(build):
    """Duplicate ids make the pool ambiguous: only E01 is decided (by the SHACL file), the other rules are marked not_decided."""
    b = dict(build); b["forms"] = {}; b["measures"] = {}; b["sheet_spec"] = {"units": []}; b["sheet_pages"] = 0
    res = decide(b)
    for r, v in res.items():
        if r != "E01":
            v["status"] = "not_decided"; v["messages"] = []
    return res


def verify(build):
    res = decide(build)
    return res, failed(res)


def write_outputs(build, outdir, stem):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    kind, pv, bp = build["kind"], build["paper_version"], build["blueprint"]
    paper = {"kind": kind, "paper_version": pv, "stem": stem, "blocks": build["blocks"]}
    keys = {f: key_data(es, kind, f, pv, bp) for f, es in build["forms"].items()}
    record = {k: v for k, v in build.items() if k not in ("forms", "authored_items", "sheet_spec", "blocks")}
    record["forms_summary"] = {f: {"records": len(es), "sub_questions": sum(e["units"] for e in es), "base_points": keys[f]["base_points"],
                                   "bonus_points": keys[f]["bonus_points"], "form_mark": keys[f]["form_mark"]} for f, es in build["forms"].items()}
    files = {"paper": paper, "key": keys, "sheetspec": build["sheet_spec"], "build": record, "authored": build["authored_items"]}
    paths = {}
    for name, data in files.items():
        p = out / ("%s_%s.json" % (stem, name))
        p.write_text(json.dumps(data, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
        paths[name] = str(p)
    full = out / ("%s_buildfull.json" % stem)
    full.write_text(json.dumps(build, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
    paths["buildfull"] = str(full)
    return paths


# ------------------------------------------------------------------ command line
def main(argv):
    args = list(argv[1:])
    if not args:
        print(__doc__); return 2
    cmd = args.pop(0)
    try:
        if cmd == "rules":
            for r, t in shape_labels().items():
                print(r, t)
            return 0
        opt, pos = {}, []
        while args:
            a = args.pop(0)
            if a.startswith("--"):
                opt[a[2:]] = args.pop(0)
            else:
                pos.append(a)
        if cmd == "verify":
            res, bad = verify(load_json(pos[0]))
            for r, v in res.items():
                print("%s %-4s %s" % (r, v["status"].upper(), v["title"]))
            return 1 if bad else 0
        if cmd != "build":
            print(__doc__); return 2
        root = Path(opt.get("root", REPO))
        design_path = opt.get("design", str(HERE / "exam_design_v1_2_0.json"))
        sets = load_pool(opt["pool"]); design = load_json(design_path)
        other = None
        if "midterm" in opt:
            mb = load_json(opt["midterm"])
            other = list(zip(mb.get("authored_refs", []), mb.get("authored_items", [])))
        build = assemble(sets, design, int(opt["seed"]), opt.get("kind", "midterm"), int(opt.get("paper-version", 1)), root,
                         other_items=other, pool_path=opt["pool"], design_path=design_path)
        for r, v in build["rules"].items():
            print("%s %-4s %s" % (r, v["status"].upper(), v["title"]))
            for m in v["messages"][:3]:
                print("      %s [%s]" % (m["message"], m["focus"]))
        if not build["ok"]:
            print("REFUSED: %s" % ", ".join(build["failed_rules"] or ["E01"]))
            return 1
        paths = write_outputs(build, opt["out"], opt.get("stem", "exam_%s_s%s" % (build["kind"], build["seed"])))
        for k, p in paths.items():
            print("wrote", k, p)
        return 0
    except CannotRun as e:
        print("CANNOT_RUN:", e); return 2
    except (KeyError, IndexError) as e:
        print("CANNOT_RUN: missing argument or field %r" % (e,)); return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
