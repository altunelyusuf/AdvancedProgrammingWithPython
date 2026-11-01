#!/usr/bin/env python3
"""Item validator for the SEN0414 printed exams, version 1.1.0 (task TK4_ItemRules2).

Checks a JSON list of item records (one record per sub-question, in print order) against the item model of
exam_design_v1_2_0.md section 3 (the 17 fields of v1_1_0 plus question, sub, tip, terms, asks) and the new item rules N1 to N5.
Library:   from exam_item_check_v1_1_0 import check_items   ->  list of {"id", "rule", "message"}; an empty list is a pass.
Command line:
    exam_item_check_v1_1_0.py check ITEMS.json     prints one line per failure, exits 0 only if there is none
    exam_item_check_v1_1_0.py selftest             runs the fixtures of exam_item_check_fixtures_v1_1_0.json, prints
                                                   expected and actual for each, exits 0 only if every fixture is as expected
exam_item_check_v1_0_0.py is NOT replaced: it stays and checks the 17-field records of the v1_1_0 design.
Differences from v1_0_0: R01 counts 22 fields; R03 allows chapter 5; R05 is 2 to 6 (level 1 is a violation, N1); R15 (points fixed by
the type) is retired because the design v1_2_0 gives each sub-question its own whole-number points: R23 checks them instead.
New: R19 no memorisation item (N1), R20 tip for every course term (N2), R21 abbreviations in full at first use over the paper (N3),
R22 asks is use, reason or effect (N4), R23 question, sub, type and points agree, R24 stem of 10 to 30 words (N5).
The validator does not judge option length or whether one answer is defensible; a person does (design section 8).
"""
import json, os, re, sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
FIXTURES = os.path.join(HERE, "exam_item_check_fixtures_v1_1_0.json")
POINTS_FILES = ("04-assessment/exams/critical_points_ch01_04_v1_0_0.json", "04-assessment/exams/critical_points_ch06_08_v1_0_0.json")

def _points_files(root=ROOT):
    """The two committed files plus the newest critical_points_ch05_v*.json when the chapter 5 task has made it."""
    extra = sorted(f for f in os.listdir(os.path.join(root, "04-assessment/exams")) if re.fullmatch(r"critical_points_ch05_v\d+_\d+_\d+\.json", f)) if os.path.isdir(os.path.join(root, "04-assessment/exams")) else []
    return POINTS_FILES + tuple("04-assessment/exams/" + f for f in extra)

KEPT_TYPES = ("mcq", "predict", "match", "order", "blank", "cloze")
CHAPTERS = (1, 2, 3, 4, 5, 6, 7, 8)
FIELDS = {"id": str, "chapters": list, "source": list, "bloom": int, "critical_point": str, "course_point": list, "seed_item": str,
          "type": str, "stem": str, "listing": list, "options_or_blanks": (list, dict), "answer": (str, list), "points": (int, float),
          "reason": str, "indirect_form": str, "code_width": int, "bank_id": str,
          "question": str, "sub": str, "tip": str, "terms": list, "asks": str}
INDIRECT = ("consequence", "exception", "reason", "none")
QUESTIONS = {"Q1": ("predict", "mcq"), "Q2": ("blank", "cloze"), "Q3": ("match", "mcq"), "Q4": ("order", "mcq"), "Q5": KEPT_TYPES}
ASKS = ("use", "reason", "effect")
STEM_WORDS = (10, 30)
TIP_WORDS = 20
MAX_LISTING_LINES = 12
WIDTHS = (45, 90)
MAX_BANK = 10                                                  # the sheet's bank unit has two digit rows: serial 0 to 9
RULES = {
    "R01": "all 22 fields present, no other field, each of the right JSON type",
    "R02": "id unique in the list",
    "R03": "chapters a non-empty list among 1 to 8 (chapter 5 is in)",
    "R04": "every source names a file that exists (path or path#place)",
    "R05": "bloom an integer 2 to 6 (level 1 is a memorisation level and is not allowed)",
    "R06": "every course_point resolves to an entry of the two critical-points files",
    "R07": "critical_point equals the text of the point of a resolved course_point entry",
    "R08": "seed_item is none or <bank file>#<position> inside that file",
    "R09": "type is one of the kept types",
    "R10": "answer is inside the options and in the form of the type",
    "R11": "no overlapping options",
    "R12": "no 'all of the above' or 'none of the above'",
    "R13": "listing has at most 12 lines",
    "R14": "code_width is 45 or 90 and no listing line is wider or holds a line break",
    "R16": "blank and cloze: gap markers, gap count, bank size and bank_id agree",
    "R17": "indirect_form is consequence, exception, reason or none",
    "R18": "reason is a non-empty text",
    "R19": "no memorisation item: the stem does not ask for a name, keyword, definition, signature or syntax detail from memory (patterns below)",
    "R20": "tip rules: every course term of the term list found in stem or options is in terms and has a tip; tip at most 20 words, not an option, not 'none' when terms is not empty; no term is the answer",
    "R21": "abbreviations: over the whole list in print order, the first use of each short form is 'full form (SHORT)'",
    "R22": "asks is use, reason or effect",
    "R23": "question is Q1 to Q5, sub a to g, id equals question plus sub (unique pair), type allowed in the question, points a whole number of at least 1",
    "R24": "stem has 10 to 30 words (gap markers [[n]] not counted)",
}

# ---- R19: stems that ask for something to be remembered. Each pattern with the reason it is a memorisation question.
R19_PATTERNS = [
    (r"\bwhat\s+is\s+the\s+(name|term|keyword)\b", "asks for a name or term"),
    (r"\b(what|how)\s+(is|are)\s+.{0,80}\bcalled\b|\bis\s+called\b|\bwhat\s+do\s+we\s+call\b|\bknown\s+as\b", "asks for the name of a thing"),
    (r"\bwhich\s+(reserved\s+word|keyword|function\s+name|method\s+name|module\s+name|built-in\s+name|command\s+name)\b", "asks to pick a name or keyword"),
    (r"\bdefin(e|ition|es|ed)\b", "asks for a definition"),
    (r"\bstands?\s+for\b|\bshort\s+for\b|\babbreviation\s+of\b", "asks what a short form means"),
    (r"\b(syntax|signature)\b|\bcorrect\s+way\s+to\s+(write|spell|type)\b|\bhow\s+is\s+.{0,40}\b(written|spelled)\b|\bexact\s+(spelling|form|wording)\b", "asks for a syntax or signature detail"),
    (r"\b(remember|recall|memori[sz]e|from\s+memory|by\s+heart)\b", "asks outright to recall"),
]
# a call asked about without a shown listing is a question about the function's remembered behaviour
R19_NOLISTING = [
    (r"\bwhat\s+does\s+(the\s+)?(built-in\s+)?(function|method|operator)\b.{0,60}\b(return|do|mean)\b", "what does the function ... return, with no listing shown"),
    (r"\bwhat\s+does\s+[\w.]+\(.*\)\s+(return|do|mean)\b", "what does f(...) return, with no listing shown"),
    (r"\bwhat\s+(is|are)\s+the\s+(return\s+value|default\s+value|parameters?)\s+of\b", "asks for a remembered return value, default or parameter list, with no listing shown"),
]

# ---- R20: the stated term list: specific terms the course uses. Each term is checked at selftest to occur in the course files below.
TERM_SOURCES = ("04-assessment/exams/critical_points_ch01_04_v1_0_0.json", "04-assessment/exams/critical_points_ch06_08_v1_0_0.json",
                "03-materials/ch05/page/chapter_code_ch05_v1_1_0.json")
TERMS = ["floor division", "slice", "IndexError", "TypeError", "ValueError", "NameError", "KeyError", "exception", "traceback",
         "tuple", "dictionary", "mutable", "f-string", "iterator", "alias", "deepcopy", "setdefault", "enumerate",
         "return value", "encoding", "breakpoint", "debugger", "assertion", "logging"]

# ---- R21: short forms the course uses, with their full forms; exceptions are not abbreviations of a phrase
ABBREVIATIONS = {"IDE": "integrated development environment", "CSV": "comma-separated values", "JSON": "JavaScript Object Notation",
                 "ASCII": "American Standard Code for Information Interchange", "UTF": "Unicode Transformation Format",
                 "API": "application programming interface", "URL": "uniform resource locator", "HTML": "hypertext markup language",
                 "XML": "extensible markup language", "PDF": "portable document format", "CPU": "central processing unit",
                 "RAM": "random-access memory", "OS": "operating system", "CLI": "command-line interface",
                 "GUI": "graphical user interface", "REPL": "read-evaluate-print loop", "PEP": "Python Enhancement Proposal",
                 "SQL": "structured query language", "HTTP": "hypertext transfer protocol", "ID": "identity number",
                 "EOF": "end of file", "GB": "gigabyte", "LIFO": "last in, first out", "FIFO": "first in, first out"}
ABBR_EXCEPTIONS = {"A", "B", "C", "D", "E", "F", "G", "FM", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET", "NAME", "PASS", "FAIL"}   # option letters, form mark, logging level names (words in Python, printed in capitals)

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

def _flat_options(it):
    out = []
    for lst in _option_texts(it):
        out += [x for x in lst if isinstance(x, str)]
    return out

def _term_hits(text, terms=TERMS):
    return [t for t in terms if re.search(r"(?<![\w-])" + re.escape(t) + r"(s|es)?(?![\w-])", text, re.I)]

def _stem_words(stem):
    return len(re.sub(r"\[\[\d+\]\]", " ", stem).split())

def new_rules(it, bad):
    """R19 to R24 on one record whose 22 fields are present and of the right type."""
    stem, t, tip, terms = it["stem"], it["type"], it["tip"], it["terms"]
    # R19
    low = stem.lower()
    for pat, why in R19_PATTERNS:
        if re.search(pat, low):
            bad("R19", "stem matches a memorisation pattern (%s): %r" % (why, stem))
    if not it["listing"]:
        for pat, why in R19_NOLISTING:
            if re.search(pat, low):
                bad("R19", "stem matches a memorisation pattern (%s): %r" % (why, stem))
    # R20
    opts = _flat_options(it)
    hits = _term_hits(stem + "\n" + "\n".join(opts))
    has_tip = isinstance(tip, str) and tip.strip() not in ("", "none")
    for h in hits:
        if not has_tip:
            bad("R20", "term %r is used and there is no tip" % h)
        if not any(h.lower() == str(x).lower() for x in terms):
            bad("R20", "term %r is used but not listed in terms" % h)
    if not all(isinstance(x, str) and x.strip() for x in terms):
        bad("R20", "terms must be non-empty texts")
    elif len(terms) > 2:
        bad("R20", "terms has %d entries, at most two" % len(terms))
    if terms and not has_tip:
        bad("R20", "terms is not empty and tip is missing or 'none'")
    if has_tip:
        if len(tip.split()) > TIP_WORDS:
            bad("R20", "tip has %d words, at most %d" % (len(tip.split()), TIP_WORDS))
        if any(tip.strip().lower() == o.strip().lower() for o in opts):
            bad("R20", "tip equals an option")
    ans = it["answer"]
    texts = []
    if t in ("mcq", "predict") and isinstance(it["options_or_blanks"], list) and ans in ("A", "B", "C", "D") and len(it["options_or_blanks"]) == 4:
        texts = [it["options_or_blanks"][("A", "B", "C", "D").index(ans)]]
    elif t in ("blank", "cloze") and isinstance(it["options_or_blanks"], dict) and isinstance(ans, list):
        bank = it["options_or_blanks"].get("bank", [])
        texts = [bank[i] for i in ans if isinstance(i, int) and 0 <= i < len(bank)]
    elif t == "match" and isinstance(it["options_or_blanks"], dict) and isinstance(ans, list):
        al = it["options_or_blanks"].get("answers", [])
        texts = [al[ "ABCDEFG".index(x)] for x in ans if x in list("ABCDEFG") and "ABCDEFG".index(x) < len(al)]
    for x in texts:
        if isinstance(x, str) and any(x.strip().lower() == tm.lower() for tm in terms):
            bad("R20", "answer %r is a listed term: the answer would depend on knowing the term" % x)
    # R22
    if it["asks"] not in ASKS:
        bad("R22", "asks %r is not one of %s" % (it["asks"], list(ASKS)))
    # R23
    q, sb = it["question"], it["sub"]
    if q not in QUESTIONS:
        bad("R23", "question %r is not Q1 to Q5" % q)
    elif t in KEPT_TYPES and t not in QUESTIONS[q]:
        bad("R23", "type %r is not allowed in %s (allowed %s)" % (t, q, list(QUESTIONS[q])))
    if sb not in list("abcdefg"):
        bad("R23", "sub %r is not a letter a to g" % sb)
    if q in QUESTIONS and sb in list("abcdefg") and it["id"] != q + sb:
        bad("R23", "id %r is not question plus sub (%s)" % (it["id"], q + sb))
    pts = it["points"]
    if not (isinstance(pts, int) and not isinstance(pts, bool) and pts >= 1):
        bad("R23", "points %r is not a whole number of at least 1" % (pts,))
    # R24
    n = _stem_words(stem)
    if not (STEM_WORDS[0] <= n <= STEM_WORDS[1]):
        bad("R24", "stem has %d words, the rule is %d to %d" % (n, STEM_WORDS[0], STEM_WORDS[1]))

def abbreviation_scan(text, registry=ABBREVIATIONS, exceptions=ABBR_EXCEPTIONS):
    """text in print order. Returns the short forms (two or more capitals) whose first use is not 'full form (SHORT)' or is not in the registry."""
    bad_, seen = [], set()
    for m in re.finditer(r"(?<![\w-])[A-Z]{2,}(?![\w-])", text):
        sh = m.group(0)
        if sh in exceptions or sh in seen:
            continue
        seen.add(sh)
        full = registry.get(sh)
        if full is None or text[max(0, m.start() - len(full) - 2):m.start()].lower() != (full + " (").lower():
            bad_.append(sh)
    return bad_

def item_text(it):
    """The printed text of one record in print order: stem, listing comments, options or bank, tip."""
    parts = [it["stem"]]
    parts += [x.split("#", 1)[1] for x in it["listing"] if isinstance(x, str) and "#" in x]
    parts += _flat_options(it)
    if isinstance(it["tip"], str) and it["tip"].strip() != "none":
        parts.append(it["tip"])
    return "\n".join(parts)

def check_item(it, root=ROOT):
    """Returns a list of (rule, message) for one item record."""
    out = []
    def bad(rule, msg): out.append((rule, msg))
    if not isinstance(it, dict):
        return [("R01", "record is not an object")]
    # R01
    miss = [k for k in FIELDS if k not in it]; extra = [k for k in it if k not in FIELDS]
    wrong = [k for k, ty in FIELDS.items() if k in it and (not isinstance(it[k], ty) or isinstance(it[k], bool))]
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
    if not (2 <= it["bloom"] <= 6):
        bad("R05", "bloom %r outside 2 to 6 (level 1 is not allowed)" % it["bloom"])
    # R06, R07
    texts = []
    if not it["course_point"]:
        bad("R06", "course_point is empty")
    for cp in it["course_point"]:
        ln = _link(cp); ok = False
        if ln:
            path, n = ln
            for pf in _points_files(root):
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
    new_rules(it, bad)
    if t not in KEPT_TYPES:
        return out
    # type-specific shape, R10, R11, R12, R16
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
    seen, texts, owner = set(), [], []
    for it in items:
        iid = it.get("id") if isinstance(it, dict) else None
        if isinstance(iid, str):
            if iid in seen or not iid.strip():
                res.append({"id": iid, "rule": "R02", "message": "id %r repeated or empty" % iid})
            seen.add(iid)
        for rule, msg in check_item(it, root):
            res.append({"id": iid, "rule": rule, "message": msg})
        if isinstance(it, dict) and all(k in it for k in FIELDS) and not any(r == "R01" for r, _ in check_item(it, root)):
            texts.append((iid, item_text(it)))
    # R21 over the whole list, in print order: a short form first used before (or without) its full form
    pos, whole = [], ""
    for iid, tx in texts:
        pos.append((len(whole), iid)); whole += tx + "\n"
    for sh in abbreviation_scan(whole):
        m = re.search(r"(?<![\w-])" + sh + r"(?![\w-])", whole)
        who = [i for st, i in pos if st <= m.start()][-1]
        res.append({"id": who, "rule": "R21", "message": "short form %s is not in the form 'full form (%s)' at its first use%s" % (sh, sh, "" if sh in ABBREVIATIONS else " (and is not in the registry)")})
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
    # provenance of the stated term list: every term must occur in the course files it is taken from
    corpus = ""
    for tf in TERM_SOURCES:
        with open(os.path.join(ROOT, tf), encoding="utf-8") as f:
            corpus += f.read().lower() + "\n"
    absent = [t for t in TERMS if t.lower() not in corpus]
    print("%s term list: %d terms, each found in the course files %s; not found: %s" % ("OK      " if not absent else "MISMATCH", len(TERMS), [os.path.basename(x) for x in TERM_SOURCES], absent))
    allok &= not absent
    # the registry: no short form maps to an empty full form, and the scan itself on known texts
    scan = [("Open the integrated development environment (IDE), then run the IDE.", []), ("Open the IDE first.", ["IDE"]),
            ("The IDE, the integrated development environment (IDE).", ["IDE"]), ("Choose A or B, form mark FM.", [])]
    sc_ok = all(abbreviation_scan(t) == w for t, w in scan) and all(v.strip() for v in ABBREVIATIONS.values())
    print("%s abbreviation scan: %d known texts and a registry of %d short forms" % ("OK      " if sc_ok else "MISMATCH", len(scan), len(ABBREVIATIONS)))
    allok &= sc_ok
    # every R19 pattern is hit by at least one defect fixture stem
    stems = [it["stem"].lower() for f in fx["fixtures"] if f["name"].startswith("defect_R19") for it in f["items"]]
    unhit = [w for p_, w in R19_PATTERNS + R19_NOLISTING if not any(re.search(p_, s_) for s_ in stems)]
    print("%s R19 patterns: %d patterns, each hit by a defect fixture; not hit: %s" % ("OK      " if not unhit else "MISMATCH", len(R19_PATTERNS) + len(R19_NOLISTING), unhit))
    allok &= not unhit
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
