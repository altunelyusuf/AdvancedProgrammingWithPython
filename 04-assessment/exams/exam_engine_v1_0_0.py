#!/usr/bin/env python3
"""exam_engine_v1_0_0: the assembler of the general exam engine for the SEN0414 printed exams (task TK4_Engine_Core).

Input : a pool of item records (the 17-field format of exam_design_v1_1_0.md section 2; a JSON list or {"items": [...]})
        and the design file (exam_design_v1_1_0.json: blueprint, arithmetic rows). Nothing of the blueprint is hard-coded:
        items, minutes, chapters, type counts, cross-chapter minimum, indirect minimum and the seconds per type come from the design.
Output: for one seed, a paper of the blueprint's size in two forms A and B (same item type at every position; the order inside a
        group of equal type and the options differ), a build record (seed, pool file and SHA-256, design file, version and SHA-256,
        the result of every rule E01 to E19), the printed answer-key data (letter, places or bank number, points, reason) and the
        sheet specification in the format of the SEN0401 sheet module (kinds choice, match, order, bank). No printed paper is rendered.
The rules are SHACL (exam_engine_shapes_v1_0_0.ttl); this file writes the description of a pool and a paper (build_graph) and
reads the verdict. Rules E02 and E16 use the item validator (exam_item_check_v1_0_0.py) and the near-copy tool (exam_nocopy_v1_0_0.py).

Assumptions (the Owner has not answered; each is one name here and marked in every build record):
  A1 BLOOM_THRESHOLD = 3 ("Apply and up"); A2 items per paper and A3 items per chapter are read from the design file.

Command line:
  exam_engine_v1_0_0.py build --pool POOL.json --design DESIGN.json --seed N --out DIR [--stem NAME] [--kind midterm|makeup]
                        [--paper-version V] [--midterm BUILD.json] [--root REPO]
  exam_engine_v1_0_0.py verify BUILD.json [--design DESIGN.json]      re-decide the rules of a build record with the SHACL file
  exam_engine_v1_0_0.py rules                                       list the rules
Exit 0 only when the paper was built and every rule passed; 1 when refused (the rules are named); 2 when it cannot run.
"""
import hashlib, importlib.util, json, math, os, random, re, sys
from collections import Counter
from decimal import Decimal, ROUND_FLOOR
from fractions import Fraction
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
import exam_item_check_v1_0_0 as itemcheck           # noqa: E402
import exam_nocopy_v1_0_0 as nocopy                  # noqa: E402

VERSION = "1.0.0"
SHAPES = HERE / "exam_engine_shapes_v1_0_0.ttl"
SHEET_DIR = Path(os.environ.get("SEN0401_EXAM_DIR", "/home/claude/sen0401/08-tooling/exam"))
SHEET_MODULES = ("sen0401_exam_answersheet_v1_0_0.py", "sen0401_exam_answersheet_v1_1_0.py")
EX = "https://example.org/sen0414/exam-engine#"

BLOOM_THRESHOLD = 3                                   # A1, assumption: the Bloom reading "Apply and up"
PART_ORDER = ("mcq", "predict", "blank", "cloze", "match", "order")   # design section 5: choice, trace, bank fill-in, match and order
FORMS = ("A", "B")
LETTERS = "ABCD"
ASSUMPTIONS = {"A1": "Bloom reading Apply and up: level %d" % BLOOM_THRESHOLD,
               "A2": "items per paper, read from the design file (blueprint.items)",
               "A3": "items per chapter, read from the design file (blueprint.chapters)"}


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
    data = load_json(path)
    if isinstance(data, dict):
        data = data.get("items")
    if not isinstance(data, list) or not all(isinstance(x, dict) and "id" in x for x in data):
        raise CannotRun("%s: not a JSON list of item records with an id" % path)
    return data


def design_version(path):
    m = re.search(r"_v(\d+_\d+_\d+)\.json$", str(path))
    return m.group(1).replace("_", ".") if m else "unknown"


def read_blueprint(design):
    """The numbers of the blueprint, all read from the design file."""
    bp = design.get("blueprint")
    try:
        out = {"items": int(bp["items"]), "minutes": int(bp["minutes"]),
               "chapters": {int(k): int(v) for k, v in bp["chapters"].items()},
               "types": {k: int(v) for k, v in bp["types"].items()},
               "cross_min": int(bp["cross_chapter_items"]), "total_points": bp["arithmetic"]["total_points"]}
        seconds = {}
        for r in bp["arithmetic"]["rows"]:
            key = r["type"] + ("+code" if r["type"] == "mcq" and "with code" in r["name"] else "")
            seconds[key] = int(r["seconds_each"])
        out["seconds"] = seconds
    except (KeyError, TypeError, ValueError) as e:
        raise CannotRun("design file: blueprint field missing or malformed: %r" % (e,))
    ind = None
    for d in design.get("decisions", []):
        if "indirect" in d.get("topic", "").lower():
            m = re.search(r"[Ii]ndirect items[^.]*?at least (\d+) per paper", d.get("decision", ""))
            if m:
                ind = int(m.group(1))
    if ind is None:
        raise CannotRun("design file: the number of indirect items per paper was not found in the decisions")
    out["indirect_min"] = ind
    if sum(out["chapters"].values()) != out["items"] or sum(out["types"].values()) != out["items"]:
        raise CannotRun("design file: chapters or types do not add up to the items of the blueprint")
    for t in out["types"]:
        if t not in out["seconds"] and t != "mcq":
            raise CannotRun("design file: no seconds per item for type %s" % t)
    if "mcq" in out["types"] and not ("mcq" in out["seconds"] and "mcq+code" in out["seconds"]):
        raise CannotRun("design file: mcq needs a plain row and a 'with code' row")
    return out


def item_seconds(it, bp):
    t = it["type"]
    if t == "mcq":
        return bp["seconds"]["mcq+code" if it.get("listing") else "mcq"]
    return bp["seconds"][t]


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
        except Exception as e:                       # missing reportlab or font
            raise CannotRun("sheet module cannot be imported: %r" % (e,))
        _sheet["m"] = mod
    return _sheet["m"]


# ------------------------------------------------------------------ near-copy views
def nocopy_view(it):
    """The record the near-copy tool reads: stem, code, flat options, answer."""
    t, o, a = it["type"], it["options_or_blanks"], it["answer"]
    code = "\n".join(it.get("listing") or [])
    if t in ("mcq", "predict"):
        return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o), "answer": a}
    if t == "match":
        flat = list(o["premises"]) + list(o["answers"])
        return {"id": it["id"], "stem": it["stem"], "code": code, "options": flat,
                "answer": [o["answers"][ord(x) - 65] for x in a]}
    if t == "order":
        return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o),
                "answer": [o[a.index(k)] for k in sorted(a)]}
    return {"id": it["id"], "stem": it["stem"], "code": code, "options": list(o["bank"]), "answer": [o["bank"][k] for k in a]}


def dec6(fr):
    return (Decimal(fr.numerator) / Decimal(fr.denominator)).quantize(Decimal("0.000001"), rounding=ROUND_FLOOR)


def measure(items, seeds):
    """Per item: (largest coverage with an equal answer, largest coverage whatever the answer, listing copy)."""
    res = nocopy.measure_all([nocopy_view(i) for i in items], seeds)
    out = {}
    for it, r in zip(items, res):
        same = max([c["c"] for c in r["comparisons"] if c["answers_equal"]] or [Fraction(0)])
        anyc = max([c["c"] for c in r["comparisons"]] or [Fraction(0)])
        lc = any(c["listing_copy"] for c in r["comparisons"])
        out[it["id"]] = (same, anyc, lc)
    return out


# ------------------------------------------------------------------ selection
def first_chapter(it):
    return it["chapters"][0]


def select(pool, bp, flags, rng, restarts=12, iters=6000):
    """Seeded local search for a set of items that satisfies the blueprint. Returns (indexes, cost)."""
    n = bp["items"]
    if len(pool) <= n:
        return list(range(len(pool))), 0
    ch = [first_chapter(i) if i["chapters"] else -1 for i in pool]
    ty = [i["type"] for i in pool]
    sec = [item_seconds(i, bp) for i in pool]
    bl = [1 if i["bloom"] >= BLOOM_THRESHOLD else 0 for i in pool]
    cr = [1 if len(i["chapters"]) >= 2 else 0 for i in pool]
    ind = [1 if i["indirect_form"] != "none" else 0 for i in pool]
    bad = [flags[i["id"]]["bad"] for i in pool]
    rep = [flags[i["id"]]["rep"] for i in pool]
    limit = 90 * bp["minutes"] * 60
    need_bloom = n // 2 + 1

    def cost(S):
        c = Counter(ch[i] for i in S); t = Counter(ty[i] for i in S)
        v = sum(abs(c.get(k, 0) - q) for k, q in bp["chapters"].items()) + sum(x for k, x in c.items() if k not in bp["chapters"])
        v += sum(abs(t.get(k, 0) - q) for k, q in bp["types"].items()) + sum(x for k, x in t.items() if k not in bp["types"])
        v *= 4
        tot = sum(sec[i] for i in S)
        if tot * 100 > limit:
            v += 5 + (tot * 100 - limit) / 100000.0
        v += 2 * max(0, need_bloom - sum(bl[i] for i in S))
        v += 2 * max(0, bp["cross_min"] - sum(cr[i] for i in S))
        v += 2 * max(0, bp["indirect_min"] - sum(ind[i] for i in S))
        v += 3 * sum(bad[i] for i in S) + 3 * sum(rep[i] for i in S)
        return v

    best, bestc = None, None
    idx = list(range(len(pool)))
    for _ in range(restarts):
        S = rng.sample(idx, n)
        cur = cost(S)
        for it in range(iters):
            if cur == 0:
                break
            T = 2.0 * (1 - it / iters) + 0.05
            p = rng.randrange(n)
            old = S[p]
            if rng.random() < 0.5:
                same = [j for j in idx if ch[j] == ch[old] and ty[j] == ty[old] and j not in S]
                if not same:
                    continue
                new = rng.choice(same)
            else:
                new = rng.choice(idx)
                if new in S:
                    continue
            S[p] = new
            c2 = cost(S)
            if c2 <= cur or rng.random() < math.exp((cur - c2) / T):
                cur = c2
            else:
                S[p] = old
        if bestc is None or cur < bestc:
            best, bestc = list(S), cur
        if bestc == 0:
            break
    return best, bestc


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
    for _ in range(200):
        p = list(range(n)); rng.shuffle(p)
        if p not in avoid:
            return p
    return p


def present_item(it, pos, target, rng, avoid_sig, master, form, attempt=0):
    """Returns the presented entry of one item for one form (without bank keys that depend on neighbours)."""
    t, o, a = it["type"], it["options_or_blanks"], it["answer"]
    e = {"position": pos, "id": it["id"], "type": t, "chapters": list(it["chapters"]), "points": it["points"], "reason": it["reason"],
         "stem": it["stem"], "listing": list(it["listing"]), "code_width": it["code_width"]}
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
    else:                                                        # blank, cloze: the bank is chosen in present_banks
        e["authored"] = {"bank": list(o["bank"]), "answer": list(a)}
        e["gaps"] = o["gaps"]; e["bank_id"] = it["bank_id"]
    return e


def bank_perm(seed, n):
    p = list(range(n)); random.Random(seed).shuffle(p); return p


def present_banks(entries, master, form, avoid_sigs):
    """Chooses, for each fill-in item in position order, a seeded bank permutation that satisfies E13, E14, E15."""
    seq = []                                                     # keys of the gaps of the form so far
    for e in sorted(entries, key=lambda x: x["position"]):
        if e["type"] not in ("blank", "cloze"):
            continue
        bank, ans = e["authored"]["bank"], e["authored"]["answer"]
        ok = None
        for attempt in range(400):
            s = seed_int(master, form, e["id"], attempt)
            perm = bank_perm(s, len(bank))
            keys = [perm.index(x) for x in ans]
            sig = "B" + "".join(map(str, perm))
            if sig == avoid_sigs.get(e["id"]):
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
            ok = (s, perm, keys, sig, attempt)                    # kept: the SHACL rules will name the failure
        s, perm, keys, sig, attempt = ok
        e["bank"] = [bank[i] for i in perm]
        e["bank_codes"] = [bank_code(k) for k in range(len(bank))]
        e["key"] = keys
        e["bank_seed"] = s; e["bank_attempt"] = attempt; e["option_order"] = sig
        seq += keys


def build_forms(selected, bp, master):
    groups = {t: [i for i in selected if i["type"] == t] for t in bp["types"]}
    order = [t for t in PART_ORDER if t in groups] + [t for t in groups if t not in PART_ORDER]
    rng = random.Random(seed_int(master, "order"))
    seqA, seqB = [], []
    for t in order:
        g = groups[t][:]
        rng.shuffle(g); seqA += g
        h = g[:]
        for _ in range(500):
            rng.shuffle(h)
            if len(g) < 2 or all(x["id"] != y["id"] for x, y in zip(g, h)):
                break
        seqB += h
    forms, sigs = {}, {}
    for form, seq in (("A", seqA), ("B", seqB)):
        r = random.Random(seed_int(master, "options", form))
        lettered = [i for i in seq if i["type"] in ("mcq", "predict")]
        targets = targets_for_letters(len(lettered), r)
        entries, li = [], 0
        for pos, it in enumerate(seq, 1):
            tgt = None
            if it["type"] in ("mcq", "predict"):
                tgt = targets[li]; li += 1
            entries.append(present_item(it, pos, tgt, r, sigs.get(it["id"]), master, form))
        present_banks(entries, master, form, sigs)
        if form == "A":
            sigs = {e["id"]: e["option_order"] for e in entries}
        forms[form] = entries
    return forms


# ------------------------------------------------------------------ sheet specification and key
def unit_list(e):
    """Units of one presented item: (no, kind, options, answer text, points)."""
    p, t = e["position"], e["type"]
    if t in ("mcq", "predict"):
        return [(str(p), "choice", "ABCD", e["key"], e["points"])]
    if t == "match":
        return [("%d%s" % (p, "abcde"[k]), "match", "ABCDEFG", e["key"][k], 1) for k in range(5)]
    if t == "order":
        return [("%d%s" % (p, "abcd"[k]), "order", "1234", str(e["key"][k]), 1) for k in range(4)]
    return [("%d%s" % (p, "abcdefghij"[k]), "bank", None, bank_code(e["key"][k]), 1) for k in range(e["gaps"])]


def sheet_spec(entries, kind, paper_version):
    mod = sheet_module()
    units = [{"no": "F", "kind": "bank", "digits": 2}]
    for e in sorted(entries, key=lambda x: x["position"]):
        for no, k, opts, _, _ in unit_list(e):
            units.append({"no": no, "kind": k, "digits": 2} if k == "bank" else {"no": no, "kind": k, "opts": opts})
    pk = "Midterm" if kind == "midterm" else "MakeUp"
    return {"paper_kind": pk, "paper_version": paper_version,
            "form_code": mod.make_code(1000 + paper_version * 10 + (0 if kind == "midterm" else 1), 4), "units": units}


def form_mark(kind, form):
    serial = {("midterm", "A"): 0, ("midterm", "B"): 1, ("makeup", "A"): 2, ("makeup", "B"): 3}[(kind, form)]
    return {"serial": serial, "code": bank_code(serial)}


def key_data(entries, kind, form, paper_version):
    items = []
    for e in sorted(entries, key=lambda x: x["position"]):
        us = [{"unit": no, "kind": k, "answer": ans, "points": pts} for no, k, _, ans, pts in unit_list(e)]
        k = {"position": e["position"], "id": e["id"], "type": e["type"], "units": us, "points": sum(u["points"] for u in us), "reason": e["reason"]}
        if e["type"] in ("blank", "cloze"):
            k["bank_numbers"] = e["key"]
        items.append(k)
    body = {"kind": kind, "form": form, "paper_version": paper_version, "form_mark": form_mark(kind, form), "items": items,
            "total_points": sum(i["points"] for i in items)}
    body["content_sha256"] = hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return body


# ------------------------------------------------------------------ SHACL description and verdict
def build_graph(build):
    from rdflib import Graph, Namespace, Literal, RDF, XSD, BNode
    ex = Namespace(EX)
    g = Graph(); g.bind("ex", ex)
    bp = build["blueprint"]
    P = ex["paper"]
    g.add((P, RDF.type, ex.Paper))
    g.add((P, ex.minutes, Literal(bp["minutes"])))
    g.add((P, ex.bloomThreshold, Literal(build["assumptions"]["bloom_threshold"])))
    g.add((P, ex.crossMin, Literal(bp["cross_min"])))
    g.add((P, ex.indirectMin, Literal(bp["indirect_min"])))
    for c, q in bp["chapters"].items():
        b = BNode(); g.add((P, ex.hasChapterQuota, b)); g.add((b, RDF.type, ex.ChapterQuota)); g.add((b, ex.chapter, Literal(int(c)))); g.add((b, ex.quota, Literal(q)))
    for t, q in bp["types"].items():
        b = BNode(); g.add((P, ex.hasTypeQuota, b)); g.add((b, RDF.type, ex.TypeQuota)); g.add((b, ex.itemType, Literal(t))); g.add((b, ex["count"], Literal(q)))
    for k, pid in enumerate(build["pool_ids"]):
        n = ex["pool/%d" % k]; g.add((n, RDF.type, ex.PoolRecord)); g.add((n, ex.poolId, Literal(pid)))
    for l in LETTERS:
        g.add((ex["letter/" + l], RDF.type, ex.Letter))
    forms = build["forms"]
    first = forms[FORMS[0]] if FORMS[0] in forms else []
    for e in first:
        n = ex["item/" + re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"])]
        m = build["measures"][e["id"]]
        g.add((n, RDF.type, ex.PaperItem)); g.add((n, ex.inPaper, P)); g.add((n, ex.itemId, Literal(e["id"])))
        g.add((n, ex.firstChapter, Literal(e["chapters"][0] if e["chapters"] else -1)))
        g.add((n, ex.itemType, Literal(e["type"]))); g.add((n, ex.seconds, Literal(m["seconds"]))); g.add((n, ex.bloom, Literal(m["bloom"])))
        g.add((n, ex.chapterCount, Literal(len(e["chapters"])))); g.add((n, ex.indirect, Literal(bool(m["indirect"]))))
        g.add((n, ex.validatorFailures, Literal(m["validator_failures"])))
        for name, key in (("maxCoverageSame", "max_same"), ("maxCoverageAny", "max_any"), ("otherMaxCoverageSame", "other_max_same"), ("otherMaxCoverageAny", "other_max_any")):
            g.add((n, ex[name], Literal(Decimal(m[key]), datatype=XSD.decimal)))
        g.add((n, ex.listingCopy, Literal(bool(m["listing_copy"])))); g.add((n, ex.otherIdRepeated, Literal(bool(m["other_id_repeated"]))))
        g.add((n, ex.otherListingCopy, Literal(bool(m["other_listing_copy"]))))
    for form, entries in forms.items():
        F = ex["form/" + form]; g.add((F, RDF.type, ex.Form)); g.add((F, ex.formName, Literal(form)))
        sizes = Counter(e["type"] for e in entries)
        rank = 0; seq = 0
        for e in sorted(entries, key=lambda x: x["position"]):
            item = ex["item/" + re.sub(r"[^A-Za-z0-9_.-]", "_", e["id"])]
            pr = ex["presented/%s/%d" % (form, e["position"])]
            g.add((pr, RDF.type, ex.Presented)); g.add((pr, ex.inForm, F)); g.add((pr, ex.forItem, item)); g.add((pr, ex.position, Literal(e["position"])))
            g.add((pr, ex.itemType, Literal(e["type"]))); g.add((pr, ex.groupSize, Literal(sizes[e["type"]])))
            g.add((pr, ex.optionOrder, Literal(e.get("option_order", ""))))
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
    return g


_labels = {}
def shape_labels():
    if not _labels:
        from rdflib import Graph, RDFS, URIRef
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
        parent = sg.value(None, SH.property, src)             # a property shape reports under the rule that owns it
        shape = str(parent if parent is not None else src).split("#")[-1]
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
def assemble(pool, design, seed, kind="midterm", paper_version=1, root=REPO, seeds=None, other_items=None,
             pool_path=None, design_path=None, sheet=True):
    """Builds the paper of a seed. Returns the build record (dict); build["ok"] is true only when every rule passed."""
    bp = read_blueprint(design)
    master = "%s|%s" % (kind, seed)
    ids = [i["id"] for i in pool]
    build = {"engine_version": VERSION, "kind": kind, "paper_version": paper_version, "seed": seed, "blueprint": bp,
             "assumptions": {"bloom_threshold": BLOOM_THRESHOLD, "notes": ASSUMPTIONS}, "pool_ids": ids,
             "pool_file": pool_path, "design_file": design_path,
             "design_version": design_version(design_path) if design_path else "unknown", "forms": {}, "measures": {}}
    if pool_path and Path(pool_path).is_file():
        build["pool_sha256"] = sha256_file(pool_path)
    if design_path and Path(design_path).is_file():
        build["design_sha256"] = sha256_file(design_path)
    if len(set(ids)) != len(ids):                                # E01: the pool is ambiguous; nothing else is decided
        build["rules"] = decide_pool_only(build)
        build["failed_rules"] = failed(build["rules"])
        build["ok"] = False
        return build
    for i in pool:                                               # the validator needs the whole record
        if not isinstance(i, dict):
            raise CannotRun("pool record is not an object")
    fails = {i["id"]: [f for f in itemcheck.check_item(i, str(root))] for i in pool}
    structurally_usable = [i for i in pool if _usable(i)]
    if len(structurally_usable) != len(pool):
        pool = structurally_usable
    if seeds is None:
        seeds, _ = nocopy.load_seeds(str(root))
    m_seed = measure(pool, seeds)
    other_seeds = nocopy.seeds_from_items([nocopy_view(i) for i in other_items], "other") if other_items else []
    m_other = measure(pool, other_seeds) if other_seeds else {i["id"]: (Fraction(0), Fraction(0), False) for i in pool}
    other_ids = {i["id"] for i in (other_items or [])}
    flags = {}
    for i in pool:
        s, a, lc = m_seed[i["id"]]
        os_, oa, olc = m_other[i["id"]]
        copy = (a >= nocopy.ANY_ANSWER_THRESHOLD) or (s >= nocopy.SAME_ANSWER_THRESHOLD) or lc
        rep = i["id"] in other_ids or (oa >= nocopy.ANY_ANSWER_THRESHOLD) or (os_ >= nocopy.SAME_ANSWER_THRESHOLD) or olc
        flags[i["id"]] = {"bad": 1 if (fails[i["id"]] or copy) else 0, "rep": 1 if rep else 0}
    rng = random.Random(seed_int(master, "select"))
    idxs, cost = select(pool, bp, flags, rng)
    selected = [pool[k] for k in sorted(idxs)]
    build["selection_cost"] = cost
    for i in selected:
        s, a, lc = m_seed[i["id"]]
        os_, oa, olc = m_other[i["id"]]
        build["measures"][i["id"]] = {"seconds": item_seconds(i, bp), "bloom": i["bloom"], "indirect": i["indirect_form"] != "none",
                                      "validator_failures": len(fails[i["id"]]), "max_same": str(dec6(s)), "max_any": str(dec6(a)),
                                      "listing_copy": lc, "other_id_repeated": i["id"] in other_ids, "other_max_same": str(dec6(os_)),
                                      "other_max_any": str(dec6(oa)), "other_listing_copy": olc}
    build["forms"] = build_forms(selected, bp, master)
    build["authored_items"] = selected
    build["rules"] = decide(build)
    build["failed_rules"] = failed(build["rules"])
    build["ok"] = not build["failed_rules"]
    if sheet:
        build["sheet_spec"] = sheet_spec(build["forms"]["A"], kind, paper_version)
        build["sheet_modules"] = {n: {"path": str(SHEET_DIR / n), "sha256": sha256_file(SHEET_DIR / n)} for n in SHEET_MODULES if (SHEET_DIR / n).is_file()}
    return build


def _usable(i):
    """The engine can only read a record that has the fields it uses; the validator reports the rest (E02)."""
    try:
        return (isinstance(i["chapters"], list) and i["chapters"] and isinstance(i["bloom"], int) and i["type"] in PART_ORDER
                and isinstance(i["options_or_blanks"], (list, dict)) and isinstance(i["listing"], list) and "indirect_form" in i)
    except KeyError:
        return False


def decide_pool_only(build):
    """Duplicate ids make the pool ambiguous: only E01 is decided, the other rules are marked not_decided."""
    b = dict(build); b["forms"] = {}; b["measures"] = {}
    res = decide(b)
    for r, v in res.items():
        if r != "E01":
            v["status"] = "not_decided"; v["messages"] = []
    return res


def verify(build):
    """Decides the rules again from a build record (the paper-level fixtures change a record and verify it)."""
    res = decide(build)
    return res, failed(res)


def write_outputs(build, outdir, stem):
    out = Path(outdir); out.mkdir(parents=True, exist_ok=True)
    kind, pv = build["kind"], build["paper_version"]
    paper = {"kind": kind, "paper_version": pv, "stem": stem, "forms": {f: [{k: v for k, v in e.items() if k not in ("authored",)} for e in es]
                                                                       for f, es in build["forms"].items()}}
    keys = {f: key_data(es, kind, f, pv) for f, es in build["forms"].items()}
    record = {k: v for k, v in build.items() if k not in ("forms", "authored_items", "sheet_spec")}
    record["forms_summary"] = {f: {"items": len(es), "total_points": keys[f]["total_points"], "form_mark": keys[f]["form_mark"]} for f, es in build["forms"].items()}
    files = {"paper": paper, "key": keys, "sheetspec": build["sheet_spec"], "build": record, "authored": build["authored_items"]}
    paths = {}
    for name, data in files.items():
        p = out / ("%s_%s.json" % (stem, name))
        p.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        paths[name] = str(p)
    # the full record (forms, authored items) is what verify reads
    full = out / ("%s_buildfull.json" % stem)
    full.write_text(json.dumps({k: v for k, v in build.items()}, indent=1, ensure_ascii=False, default=str) + "\n", encoding="utf-8")
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
        opt = {}
        pos = []
        while args:
            a = args.pop(0)
            if a.startswith("--"):
                opt[a[2:]] = args.pop(0)
            else:
                pos.append(a)
        if cmd == "verify":
            build = load_json(pos[0])
            res, bad = verify(build)
            for r, v in res.items():
                print("%s %-4s %s" % (r, v["status"].upper(), v["title"]))
            return 1 if bad else 0
        if cmd != "build":
            print(__doc__); return 2
        root = Path(opt.get("root", REPO))
        design_path = opt.get("design", str(HERE / "exam_design_v1_1_0.json"))
        pool = load_pool(opt["pool"]); design = load_json(design_path)
        other = None
        if "midterm" in opt:
            other = load_json(opt["midterm"]).get("authored_items")
        build = assemble(pool, design, int(opt["seed"]), opt.get("kind", "midterm"), int(opt.get("paper-version", 1)), root,
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
