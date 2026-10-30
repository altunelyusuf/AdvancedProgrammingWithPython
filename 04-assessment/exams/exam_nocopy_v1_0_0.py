#!/usr/bin/env python3
"""exam_nocopy_v1_0_0: the near-copy rule for SEN0414 exam items (task TK4_Distinct_Build).

Rule (Owner's ruling of 2026-10-30, design section 2.1 of exam_design_v1_0_0.md):
  * normalise: lower case; a word is a run of letters, digits and underscore;
  * the text of an item is its stem, its code listing and its options joined;
  * C(new, seed) = share of the new item's distinct 4-word sequences that also occur in the seed;
  * near copy of a seed: C >= 0.50 and the correct answers are equal as normalised text,
    or C >= 0.80 whatever the answer;
  * a listing that equals a seed listing after whitespace is a copy, unless a change of case
    alters what it prints (decided by running both listings);
  * the same rule applies between two papers (--other).
Seeds (what a student can open before the sitting): every item of the newest question_bank_v*.json
and of the newest quiz_v*.json in 08-tooling/chNN-page for chapters 1 to 8 (chapter 5 too), and every
listing of the newest 03-materials/chNN/page/chapter_code_chNN_v*.json.

Usage: python3 exam_nocopy_v1_0_0.py ITEMS.json [--other PAPER.json ...] [--root REPO] [--shacl]
Exit 0 only when no item is a near copy (and every input could be read); 2 on unreadable input.
"""
import json, re, subprocess, sys, tempfile, os
from decimal import Decimal, ROUND_FLOOR
from fractions import Fraction
from pathlib import Path

VERSION = "1.0.0"
CHAPTERS = (1, 2, 3, 4, 5, 6, 7, 8)
SAME_ANSWER_THRESHOLD = Fraction(1, 2)   # 0.50
ANY_ANSWER_THRESHOLD = Fraction(4, 5)    # 0.80
NC = "https://example.org/sen0414/nocopy#"

def words(text):
    """Lower-case runs of letters, digits and underscore (Unicode letters count as letters)."""
    return re.findall(r"[^\W]+", str(text).lower())


def grams(ws, n=4):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def norm(text):
    return " ".join(words(text))


def _options_list(opts):
    if opts is None:
        return []
    if isinstance(opts, dict):
        return [str(v) for v in opts.values()]
    return [str(o) for o in opts]


def item_text(stem, code, options):
    return " ".join([str(stem or ""), str(code or "")] + _options_list(options))


def resolve_answer(item):
    """Correct answer as normalised text: a letter or index is mapped to the option text;
    a list is mapped entry by entry; anything else is normalised as it stands."""
    opts = item.get("options", item.get("options_or_blanks"))
    ans = item.get("answer")
    if isinstance(opts, dict):
        keys = list(opts.keys()); vals = list(opts.values())
    else:
        vals = _options_list(opts); keys = [chr(65 + i) for i in range(len(vals))]

    def one(a):
        if isinstance(a, bool):
            return str(a)
        if isinstance(a, int) and 0 <= a < len(vals) and not isinstance(opts, dict):
            return str(vals[a])
        s = str(a).strip()
        if s in keys:
            return str(vals[keys.index(s)])
        if len(s) == 1 and s.upper() in keys:
            return str(vals[keys.index(s.upper())])
        return s
    if isinstance(ans, (list, tuple)):
        return norm(" ".join(one(a) for a in ans))
    return norm(one(ans)) if ans is not None else ""


# ---------------------------------------------------------------- seeds
def _newest(paths):
    def key(p):
        m = re.search(r"_v(\d+)_(\d+)_(\d+)\.json$", p.name)
        return tuple(int(x) for x in m.groups()) if m else (-1,)
    paths = sorted(paths, key=key)
    return paths[-1] if paths else None


def load_seeds(root):
    """Returns (seeds, census). A seed is a dict: id, kind (item|listing), source, text, code, answer."""
    root = Path(root)
    seeds, census = [], {"banks": [], "quizzes": [], "manifests": []}
    for ch in CHAPTERS:
        page = root / "08-tooling" / f"ch{ch:02d}-page"
        bank = _newest(list(page.glob("question_bank_v*.json")))
        quiz = _newest(list(page.glob("quiz_v*.json")))
        for kind, path in (("banks", bank), ("quizzes", quiz)):
            if path is None:
                raise FileNotFoundError(f"no {kind[:-1]} file in {page}")
            data = json.loads(path.read_text(encoding="utf-8"))
            lst = data["items"] if isinstance(data, dict) else data
            rel = path.relative_to(root).as_posix()
            census[kind].append((rel, len(lst)))
            for pos, it in enumerate(lst):
                opts = it.get("options", [])
                ans = it["answer"]
                ans_text = norm(opts[ans]) if isinstance(ans, int) and 0 <= ans < len(opts) else norm(ans)
                code = it.get("code", "") or ""
                seeds.append({"id": f"{rel}#{pos}", "kind": "item", "source": rel,
                              "text": item_text(it["q"], code, opts), "code": code, "answer": ans_text})
        man = _newest(list((root / "03-materials" / f"ch{ch:02d}" / "page").glob(f"chapter_code_ch{ch:02d}_v*.json")))
        if man is None:
            raise FileNotFoundError(f"no chapter-code manifest for chapter {ch}")
        data = json.loads(man.read_text(encoding="utf-8"))
        rel = man.relative_to(root).as_posix()
        census["manifests"].append((rel, len(data["examples"])))
        for ex in data["examples"]:
            seeds.append({"id": f"{rel}#{ex['id']}", "kind": "listing", "source": rel,
                          "text": ex["code"], "code": ex["code"], "answer": norm(ex.get("expected", ""))})
    return seeds, census


def seeds_from_items(items, label):
    out = []
    for it in items:
        code = it.get("code", "") or ""
        out.append({"id": f"{label}:{it['id']}", "kind": "item", "source": label,
                    "text": item_text(it.get("stem"), code, it.get("options", it.get("options_or_blanks"))),
                    "code": code, "answer": resolve_answer(it)})
    return out


# ---------------------------------------------------------------- listings
def _squash(code):
    return re.sub(r"\s+", "", code)


def run_listing(code, timeout=5):
    """Run a listing with the current Python in isolated mode; return (returncode, stdout, last stderr line)."""
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "listing.py")
        with open(f, "w", encoding="utf-8") as h:
            h.write(code)
        try:
            p = subprocess.run([sys.executable, "-I", f], cwd=d, capture_output=True, text=True,
                               timeout=timeout, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return (-9, "", "timeout")
        err = p.stderr.strip().splitlines()
        return (p.returncode, p.stdout, err[-1] if err else "")


def listing_relation(new_code, seed_code):
    """'copy' (equal after whitespace), 'case_same_output' (copy), 'case_differs' (not a copy), or None."""
    a, b = _squash(new_code), _squash(seed_code)
    if not a or not b:
        return None
    if a == b:
        return "copy"
    if a.lower() == b.lower():
        return "case_same_output" if run_listing(new_code) == run_listing(seed_code) else "case_differs"
    return None


# ---------------------------------------------------------------- measure
def _pct(fr):
    return float(fr)


def measure_item(item, seeds, seed_grams=None):
    """Compare one item with every seed. Returns a result dict."""
    code = item.get("code", "") or ""
    text = item_text(item.get("stem"), code, item.get("options", item.get("options_or_blanks")))
    ng = grams(words(text))
    ans = resolve_answer(item)
    comps = []
    for i, s in enumerate(seeds):
        sg = seed_grams[i] if seed_grams is not None else grams(words(s["text"]))
        c = Fraction(len(ng & sg), len(ng)) if ng else Fraction(0)
        eq = bool(ans) and ans == s["answer"]
        lrel = listing_relation(code, s["code"]) if code and s["code"] else None
        text_copy = (c >= ANY_ANSWER_THRESHOLD) or (c >= SAME_ANSWER_THRESHOLD and eq)
        list_copy = lrel in ("copy", "case_same_output")
        comps.append({"seed": s["id"], "c": c, "answers_equal": eq, "listing": lrel,
                      "text_copy": text_copy, "listing_copy": list_copy})
    best = max(comps, key=lambda x: (x["c"], x["answers_equal"])) if comps else None
    flagged = [x for x in comps if x["text_copy"] or x["listing_copy"]]
    show = max(flagged, key=lambda x: (x["c"], x["listing_copy"])) if flagged else best
    if flagged:
        if show["listing_copy"] and not show["text_copy"]:
            why = "near copy (listing)"
        elif show["c"] >= ANY_ANSWER_THRESHOLD:
            why = "near copy (C>=0.80)"
        else:
            why = "near copy (C>=0.50, same answer)"
        verdict = why
    else:
        verdict = "not a copy"
    return {"id": item["id"], "max_c": best["c"] if best else Fraction(0), "best_seed": best["seed"] if best else "-",
            "shown": show, "verdict": verdict, "is_copy": bool(flagged), "comparisons": comps,
            "case_differs": [x["seed"] for x in comps if x["listing"] == "case_differs"]}


def measure_all(items, seeds):
    sg = [grams(words(s["text"])) for s in seeds]
    return [measure_item(it, seeds, sg) for it in items]


# ---------------------------------------------------------------- RDF / SHACL
def to_graph(results):
    from rdflib import Graph, Namespace, Literal, BNode, RDF, XSD
    ns = Namespace(NC)
    g = Graph(); g.bind("nc", ns)
    for r in results:
        item = ns["item/" + re.sub(r"[^A-Za-z0-9_.-]", "_", r["id"])]
        g.add((item, RDF.type, ns.MeasuredItem))
        g.add((item, ns.itemId, Literal(r["id"])))
        for c in r["comparisons"]:
            if c["c"] == 0 and not c["listing"]:
                continue
            b = BNode()
            g.add((item, ns.comparedWith, b))
            g.add((b, RDF.type, ns.Comparison))
            g.add((b, ns.seedId, Literal(c["seed"])))
            dec = (Decimal(c["c"].numerator) / Decimal(c["c"].denominator)).quantize(Decimal("0.000001"), rounding=ROUND_FLOOR)
            g.add((b, ns.coverage, Literal(dec, datatype=XSD.decimal)))
            g.add((b, ns.answersEqual, Literal(bool(c["answers_equal"]))))
            g.add((b, ns.listingCopy, Literal(bool(c["listing_copy"]))))
    return g


# ---------------------------------------------------------------- CLI
def load_items(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("items", data.get("records"))
    if not isinstance(data, list):
        raise ValueError(f"{path}: not a JSON list of item records")
    for it in data:
        if "id" not in it:
            raise ValueError(f"{path}: an item has no id")
    return data


def main(argv):
    args = list(argv[1:]); root = Path(__file__).resolve().parents[2]; others = []; shacl = False
    items_path = None
    while args:
        a = args.pop(0)
        if a == "--root":
            root = Path(args.pop(0))
        elif a == "--other":
            others.append(args.pop(0))
        elif a == "--shacl":
            shacl = True
        elif items_path is None:
            items_path = a
        else:
            print("unexpected argument:", a); return 2
    if items_path is None:
        print(__doc__); return 2
    try:
        items = load_items(items_path)
        seeds, census = load_seeds(root)
        for o in others:
            seeds += seeds_from_items(load_items(o), "paper:" + Path(o).name)
    except (OSError, ValueError, KeyError) as e:
        print("CANNOT_RUN:", e); return 2
    n_list = sum(1 for s in seeds if s["kind"] == "listing")
    print(f"seeds: {len(seeds)} ({sum(n for _, n in census['banks'])} bank items, {sum(n for _, n in census['quizzes'])} quiz items, "
          f"{n_list} manifest listings, {len(seeds) - sum(n for _, n in census['banks']) - sum(n for _, n in census['quizzes']) - n_list} other-paper items)")
    for k in ("banks", "quizzes", "manifests"):
        for rel, n in census[k]:
            print(f"  seed file {rel} ({n})")
    results = measure_all(items, seeds)
    print("id | largest C | seed | answers equal | verdict")
    for r in results:
        s = r["shown"]
        print(f"{r['id']} | {float(r['max_c']):.3f} | {r['best_seed'] if s is None or not r['is_copy'] else s['seed']} | "
              f"{'yes' if (s and s['answers_equal']) else 'no'} | {r['verdict']}")
        for sid in r["case_differs"]:
            print(f"    note: listing equals {sid} apart from case but prints differently (not a copy)")
    bad = [r for r in results if r["is_copy"]]
    if shacl:
        import pyshacl
        from rdflib import Graph
        sg = Graph().parse(str(Path(__file__).with_name("exam_nocopy_shapes_v1_0_0.ttl")), format="turtle")
        conforms, _, text = pyshacl.validate(to_graph(results), shacl_graph=sg, inference="none", advanced=True)
        print("SHACL:", "conforms" if conforms else "violation")
        if not conforms:
            print(text)
        if conforms == bool(bad):
            print("MISMATCH between library verdict and SHACL"); return 1
    print(f"{len(bad)} of {len(results)} items are near copies")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
