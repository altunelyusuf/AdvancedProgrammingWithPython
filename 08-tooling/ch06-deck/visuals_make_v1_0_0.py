"""Builds the chapter 6 visual specifications by EXECUTING code under the interpreter it is run with. A specification is data: the same file is drawn
as native shapes by the deck and can be drawn as SVG or HTML by the page, so a slide and the page can never show different values. Nothing in the
output is typed by hand except the labels that name a thing: a lane records what a real operation did to a real list (the list before, the list after,
what the call returned, whether the same object is still bound); a slice records the indexes range(*slice.indices(len)) selected; the reference graphs are
snapshots of the objects reachable from the names of a real run (a statement at a time, or the line events of a traced program); the sort records are
the keys the key function really returned; the mutation record is a line trace of the registered program; the matrix frames are rows a real run of the
chapter's program printed, with time.sleep replaced. The list of visuals and their kinds is in the record's _kinds.
Usage: visuals_make_v1_0_0.py <out.json>   (run under the Python the course teaches)"""
__version__ = "1.0.0"
import contextlib, copy, difflib, io, json, os, platform, random, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, ".."))
from examples_v1_0_0 import PROGRAMS, MATRIX, EIGHT
import sen0414_ch06_rdodi_data_v1_0_0 as R
PY = sys.executable
rp = repr
def ev(expr, ns):
    try: return rp(eval(expr, ns))
    except Exception as e: return "%s: %s" % (type(e).__name__, e)

# ---- lanes: what an operation did to a list ---------------------------------------------------------------------------------
def marks(b, a):
    sm = difflib.SequenceMatcher(None, [rp(x) for x in b], [rp(x) for x in a], autojunk=False); bm, am = [], []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag in ("replace", "delete"): bm += list(range(i1, i2))
        if tag in ("replace", "insert"): am += list(range(j1, j2))
    return bm, am
def lane(setup, name, op, mark=True):
    ns = {"random": random, "copy": copy}; exec(setup, ns); obj = ns[name]; before = list(obj); oid = id(obj)
    try: val = eval(op, ns); is_expr = True
    except SyntaxError: exec(op, ns); val = None; is_expr = False
    now = ns[name]; same = id(now) == oid
    if is_expr and isinstance(val, list) and val is not obj:
        assert list(now) == before, ("a new-list operation changed its operand", op)
        cat, cl, after = "new list", "makes a new list; the original is unchanged", list(val); ret = "returns a new list"; same = False
    else:
        assert list(now) != before and same, ("an in-place operation left the list as it was", op)
        cat, cl, after = "in place", "changes the same list in place", list(now)
        ret = ("returns %s" % rp(val)) if is_expr else "a statement: no value"
    bm, am = marks(before, after) if mark else ([], [])
    return {"op": op, "name": name, "before": [rp(x) for x in before], "after": [rp(x) for x in after], "returns": rp(val) if is_expr else None, "ret_label": ret,
            "category": cat, "cat_label": cl, "same_object": same, "before_marks": bm, "after_marks": am}
def errors(setup, exprs):
    ns = {"random": random}; exec(setup, ns); return [{"expr": e, "message": ev(e, ns)} for e in exprs]

# ---- reference graphs -----------------------------------------------------------------------------------------------------
class Graph:
    def __init__(self): self.ids = {}; self.keep = []
    def lab(self, o):
        k = id(o)
        if k not in self.ids: self.ids[k] = "o%d" % (len(self.ids) + 1); self.keep.append(o)
        return self.ids[k]
    def snap(self, scopes):
        objects = {}
        def walk(o):
            oid = self.lab(o)
            if oid in objects: return oid
            if isinstance(o, list):
                objects[oid] = {"type": "list", "items": []}
                for it in o: objects[oid]["items"].append({"ref": walk(it)} if isinstance(it, list) else {"v": rp(it)})
            else: objects[oid] = {"type": "value", "v": rp(o)}
            return oid
        return {"scopes": [{"scope": lab, "names": [[n, walk(v)] for n, v in names.items()]} for lab, names in scopes], "objects": objects}
def renumber(steps):
    m = {}
    def f(o):
        if o not in m: m[o] = "o%d" % (len(m) + 1)
        return m[o]
    for st in steps:
        for sc in st["scopes"]:
            for nm in sc["names"]: nm[1] = f(nm[1])
        new = {}
        for oid, ob in st["objects"].items():
            if ob["type"] == "list": ob = {"type": "list", "items": [{"ref": f(i["ref"])} if "ref" in i else i for i in ob["items"]]}
            new[f(oid)] = ob
        st["objects"] = new
    return steps
def scenario(title, stmts, names, pre=""):
    g = Graph(); ns = {"copy": copy}; exec(pre, ns); steps = []
    for st in stmts:
        exec(st, ns); step = g.snap([("module", {n: ns[n] for n in names if n in ns})]); step["code"] = st; steps.append(step)
    return {"title": title, "steps": renumber(steps)}
def traced(code, pick):
    """Runs the program with a line tracer; every line and return event of the program's own frames is a candidate frame; `pick` chooses the ones to keep."""
    g = Graph(); rec = []; lines = code.split("\n")
    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<prog>": return None
        if event in ("line", "return"):
            sc = [("module", {k: v for k, v in frame.f_globals.items() if isinstance(v, list)})]
            if frame.f_code.co_name != "<module>": sc.append((frame.f_code.co_name + "()", {k: v for k, v in frame.f_locals.items() if isinstance(v, list)}))
            rec.append({"event": event, "func": frame.f_code.co_name, "line": frame.f_lineno, "text": lines[frame.f_lineno - 1].strip(), "snap": g.snap(sc)})
        return tracer
    try:
        sys.settrace(tracer)
        with contextlib.redirect_stdout(io.StringIO()): exec(compile(code, "<prog>", "exec"), {"__name__": "__main__"})
    finally: sys.settrace(None)
    return rec

V = {}
# ---- the three questions ---------------------------------------------------------------------------------------------------
def observe(kind, setup, code, shown, ev_share=""):
    ns = {"random": random}; exec(setup, ns); a = ns["a"]; before = list(a)
    if kind == "change":
        val = eval(code, ns); ok = val is None and list(ns["a"]) != before
        return ok, "returns None; the list itself changed", shown
    if kind == "new":
        val = eval(code, ns); ok = isinstance(val, list) and val is not ns["a"] and list(ns["a"]) == before
        return ok, "returns a new list; the original is unchanged", shown
    ok = bool(eval(code, ns)); return ok, ev_share, shown
CL = [("change", "Did the list itself change?", "It changes in place", [
         ("a = [3, 1]", "a.append(4)", "a.append(4)"), ("a = [3, 1, 2]", "a.sort()", "a.sort()"), ("random.seed(1); a = [1, 2, 3]", "random.shuffle(a)", "random.shuffle(a)")]),
      ("new", "Did it give back a new list?", "It returns a new list", [
         ("a = [3, 1, 2]", "sorted(a)", "sorted(a)"), ("a = [3, 1, 2]", "a[1:]", "a[1:]"), ("a = [3, 1, 2]", "a + [9]", "a + [9]"), ("a = [3, 1, 2]", "[x for x in a]", "[x for x in a]")]),
      ("share", "Do two names reach one list?", "It only shares the list", [
         ("a = [3, 1, 2]", "(lambda b: b is a)(a)", "b = a", "both names reach one list"), ("a = [3, 1, 2]", "(lambda p: p is a)(a)", "f(a)", "the parameter reaches the caller's list"), ("a = [[]]", "all(x is a[0] for x in a * 3)", "[[]] * 3", "three items, one inner list")])]
cols = []
for kind, q, head, items in CL:
    chips = []
    for it in items:
        ok, ev_, sh = observe(kind, *it); assert ok, (kind, it[1]); chips.append({"expr": sh, "evidence": ev_})
    cols.append({"kind": kind, "question": q, "head": head, "chips": chips})
V["ThreeQuestions"] = {"kind": "classify", "caption": "Each operation was run on a real list and put in the column its evidence names.", "columns": cols}

# ---- indexing, slicing ---------------------------------------------------------------------------------------------------
spam = ["cat", "bat", "rat", "elephant"]; ns = {"spam": spam}
V["Indexing"] = {"kind": "boxes", "name": "spam", "list": [rp(x) for x in spam], "len": len(spam),
                 "picks": [{"expr": e, "result": ev(e, ns), "at": [eval(e[5:-1]) % len(spam)]} for e in ("spam[0]", "spam[-1]", "spam[-3]")],
                 "error": {"expr": "spam[10000]", "message": ev("spam[10000]", ns)}, "caption": "Every item has an index counted from the front and one counted from the back."}
class _S:
    def __getitem__(self, k): return k
rows = []
for e in ("spam[1:3]", "spam[:2]", "spam[1:]", "spam[1:10]", "spam[::2]", "spam[::-1]"):
    sl = eval("_S()" + e[4:], {"_S": _S}); picked = list(range(*sl.indices(len(spam))))
    res = eval(e, {"spam": spam}); assert [spam[i] for i in picked] == res
    rows.append({"expr": e, "result": rp(res), "picked": picked, "picked_label": ("from indexes " + ", ".join(map(str, picked))) if picked else "no indexes"})
V["Slicing"] = {"kind": "slices", "name": "spam", "list": [rp(x) for x in spam], "rows": rows, "caption": "A slice is a new list of the items whose indexes it selects; an end outside the list is clipped, not an error."}

# ---- adding, replacing, removing ---------------------------------------------------------------------------------------------
L3 = "spam = ['cat', 'dog', 'bat']"; L4 = "spam = ['cat', 'bat', 'rat', 'elephant']"; LET = "letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']"
V["AddingAndReplacing"] = {"kind": "lanes", "lanes": [lane(L3, "spam", "spam.append('moose')"), lane(L3, "spam", "spam.insert(1, 'chicken')"),
                           lane(L4, "spam", "spam[1] = 'aardvark'"), lane(LET, "letters", "letters[2:5] = ['C', 'D', 'E']")], "errors": [],
                           "caption": "Green boxes are new or replaced; red boxes are the ones that were replaced."}
V["Removing"] = {"kind": "lanes", "lanes": [lane("spam = ['cat', 'bat', 'rat', 'cat', 'hat', 'cat']", "spam", "spam.remove('cat')"), lane("stack = [3, 4, 5, 6, 7]", "stack", "stack.pop()"),
                 lane(L4, "spam", "del spam[2]")],
                 "errors": errors("spam = ['cat', 'bat']", ["spam.remove('chicken')", "[].pop()"]), "caption": "Red boxes are the items that leave the list."}
V["Combining"] = {"kind": "lanes", "lanes": [lane("a = [1, 2, 3]", "a", "a + ['A', 'B', 'C']"), lane("a = ['X', 'Y']", "a", "a * 3")], "errors": [],
                  "caption": "+ and * leave both operands alone and make new lists."}
V["AugmentedAssignment"] = {"kind": "refgraph", "caption": "After b = a, += changes the list both names reach; a = a + other builds a new list and only rebinds a.",
                            "scenarios": [scenario("+= versus +", ["a = [1]", "b = a", "a += [2]", "a = a + [3]"], ["a", "b"])]}
# ---- searching, ordering ----------------------------------------------------------------------------------------------------
pk = ["Zophie", "Pooka", "Fat-tail", "Pooka"]; ns = {"spam": pk}
V["IndexMethod"] = {"kind": "boxes", "name": "spam", "list": [rp(x) for x in pk], "len": len(pk),
                    "picks": [{"expr": "spam.index('Pooka')", "result": ev("spam.index('Pooka')", ns), "at": [pk.index("Pooka")]}, {"expr": "spam.index('Pooka', 2)", "result": ev("spam.index('Pooka', 2)", ns), "at": [pk.index("Pooka", 2)]}],
                    "error": {"expr": "spam.index('howdy howdy howdy')", "message": ev("spam.index('howdy howdy howdy')", ns)}, "caption": "index answers with a position, and raises ValueError when there is no such item."}
def facts(items):
    out = []
    for label, setup, expr in items:
        ns = {}; exec(setup, ns); out.append({"label": label, "expr": expr, "result": ev(expr, ns)})
    return out
V["MembershipOperators"] = {"kind": "facts", "facts": facts([("On a string: is it inside?", "", "'gg' in 'eggs'"), ("On a list: is it an item?", "", "'gg' in ['eggs']"),
                           ("and stops at the left operand", "", "[] and 'not evaluated'"), ("so a length test guards an index", "spam = []", "len(spam) > 0 and spam[0] == 'cat'")]), "caption": "in tests substrings of a string but only whole items of a list."}
V["Ordering"] = {"kind": "lanes", "lanes": [lane("spam = [2, 5, 3.14, 1, -7]", "spam", "spam.sort()", mark=False), lane("spam = ['cat', 'dog', 'moose']", "spam", "spam.reverse()", mark=False),
                 lane("nums = [3, 1, 2]", "nums", "sorted(nums)", mark=False), lane("spam = ['Alice', 'ants', 'Bob', 'badgers', 'Carol', 'cats']", "spam", "spam.sort()", mark=False)],
                 "errors": errors("spam = [1, 3, 2, 4, 'Alice', 'Bob']", ["spam.sort()"]), "caption": "sort() and reverse() return None; sorted() returns a new list. Strings sort with uppercase before lowercase."}
def ksort(title, items, key_src, reverse=False):
    keyf = eval(key_src) if key_src else None
    order = sorted(range(len(items)), key=(lambda i: keyf(items[i])) if keyf else (lambda i: items[i]), reverse=reverse)
    expected = sorted(items, key=keyf, reverse=reverse); assert [items[i] for i in order] == expected
    return {"title": title, "expr": "sorted(%s%s%s)" % (rp(items), (", key=" + key_src) if key_src else "", ", reverse=True" if reverse else ""),
            "items": [rp(x) for x in items], "keys": [rp(keyf(x)) for x in items] if keyf else None, "order": order, "result": [rp(x) for x in expected]}
V["SortKeyAndReverse"] = {"kind": "keysort", "examples": [ksort("key=str.lower", ["a", "z", "A", "Z"], "str.lower"),
                          ksort("reverse=True", ["Ants", "Badgers", "Cats", "Dogs", "Elephants"], None, True),
                          ksort("equal keys stay in order", [("red", 1), ("blue", 1), ("red", 2), ("blue", 2)], "lambda t: t[0]")],
                          "caption": "The key function is called once for each item; the sort is stable, so items with equal keys keep the order they had."}
# ---- loops -------------------------------------------------------------------------------------------------------------------
sup = ["pens", "staplers", "flamethrowers", "binders"]
def passes(title, header, code, cols):
    got, printed = [], []
    def emit(*a): got.append([str(x) if isinstance(x, str) else rp(x) for x in a[:-1]]); printed.append(a[-1])
    exec(code, {"supplies": sup, "emit": emit}); return {"title": title, "header": header, "cols": cols, "rows": got}, printed
t1, p1 = passes("range(len(supplies))", "for i in range(len(supplies)):", "for i in range(len(supplies)):\n    emit(i, supplies[i], 'Index ' + str(i) + ' in supplies is: ' + supplies[i])", ["i", "supplies[i]"])
t2, p2 = passes("enumerate(supplies)", "for index, item in enumerate(supplies):", "for index, item in enumerate(supplies):\n    emit(index, item, 'Index ' + str(index) + ' in supplies is: ' + item)", ["index", "item"])
assert p1 == p2
V["Looping"] = {"kind": "passes", "tables": [t1, t2], "printed_label": "both loops printed", "printed": p1,
    "start": {"expr": "list(enumerate(supplies, start=1))[0]", "result": ev("list(enumerate(supplies, start=1))[0]", {"supplies": sup})},
    "caption": "Both loops visit indexes 0 to 3 and print the same four lines; enumerate needs neither len nor range."}
# ---- mutation while iterating ---------------------------------------------------------------------------------------------------
code = PROGRAMS["mutation_bug_v1_0_0.py"][0]; lines = code.split("\n")
def find(sub): return next(i + 1 for i, l in enumerate(lines) if sub in l)
lfor, lif, lrem, lpr = find("for x in items"), find("if x < 3"), find("items.remove"), find("print(items)")
passes_, cur, k = [], [None], [0]; g = {"__name__": "__main__"}; buf = io.StringIO()
def tr(frame, event, arg):
    if frame.f_code.co_filename != "<prog>": return None
    if event == "line":
        L = frame.f_lineno; it = frame.f_locals.get("items")
        if L in (lfor, lpr) and cur[0] is not None: cur[0]["after"] = list(it); cur[0] = None
        if L == lif: cur[0] = {"pos": k[0], "x": frame.f_locals["x"], "before": list(it), "removed": False, "after": None}; passes_.append(cur[0]); k[0] += 1
        if L == lrem and cur[0] is not None: cur[0]["removed"] = True
    return tr
try:
    sys.settrace(tr)
    with contextlib.redirect_stdout(buf): exec(compile(code, "<prog>", "exec"), g)
finally: sys.settrace(None)
orig = [1, 2, 3, 4]; visited = [p["x"] for p in passes_]
V["MutationWhileIterating"] = {"kind": "mutation", "code": code, "original": [rp(x) for x in orig], "final": [rp(x) for x in g["items"]], "printed": buf.getvalue().strip(),
    "passes": [{"n": p["pos"] + 1, "pos": p["pos"], "x": rp(p["x"]), "before": [rp(v) for v in p["before"]], "after": [rp(v) for v in p["after"]], "head": "pass %d · position %d · x = %s" % (p["pos"] + 1, p["pos"], rp(p["x"])), "action": ("removes %s" % rp(p["x"])) if p["removed"] else "keeps %s" % rp(p["x"])} for p in passes_],
    "skipped": [rp(v) for v in orig if v < 3 and v not in visited], "skip_label": " and ".join(rp(v) for v in orig if v < 3 and v not in visited) + " was never visited", "final_label": "after the loop: " + rp(g["items"]),
    "caption": "The loop counts positions. After 1 is removed, 2 moves into position 0, which the loop has already passed."}
# ---- unpacking ---------------------------------------------------------------------------------------------------------------
def unpack(stmt_targets, src, items_src):
    ns = {}; exec("items = " + items_src, ns); items = list(ns["items"]); n = len(items)
    if src == "cat": ns["cat"] = list(items)
    stmt = "%s = %s" % (", ".join(("*" if t[0] else "") + t[1] for t in stmt_targets), src); exec(stmt, ns)
    star = [i for i, t in enumerate(stmt_targets) if t[0]]; spans = []; pos = 0
    for i, (st, nm) in enumerate(stmt_targets):
        if st: cnt = n - (len(stmt_targets) - 1); spans.append((pos, pos + cnt)); pos += cnt
        else: spans.append((pos, pos + 1)); pos += 1
    vals = []
    for (a, b), (st, nm) in zip(spans, stmt_targets):
        want = items[a:b] if st else items[a]; assert ns[nm] == want, (nm, ns[nm], want); vals.append(rp(ns[nm]))
    return {"stmt": stmt, "items": [rp(x) for x in items], "targets": [{"name": ("*" if st else "") + nm, "from": a, "to": b, "value": v} for (a, b), (st, nm), v in zip(spans, stmt_targets, vals)]}
V["Unpacking"] = {"kind": "unpack", "cases": [unpack([(0, "size"), (0, "color"), (0, "disposition")], "cat", "['fat', 'gray', 'loud']"), unpack([(0, "first"), (1, "rest")], "cat", "['fat', 'gray', 'loud']"),
                  unpack([(0, "head"), (1, "middle"), (0, "last")], "range(5)", "range(5)")],
                  "caption": "Names take items left to right; one starred name takes whatever is left over."}
_ns = {"cat": ["fat", "gray", "loud"]}
try: exec("size, color, disposition, name = cat", _ns)
except ValueError as e: V["Unpacking"]["error"] = {"expr": "size, color, disposition, name = cat", "message": "%s: %s" % (type(e).__name__, e)}
V["ListComprehension"] = {"kind": "facts", "facts": facts([("Build a list from a rule", "", "[x**2 for x in range(10)]"), ("Keep only some items", "vec = [-4, -2, 0, 2, 4]", "[x for x in vec if x >= 0]"),
                          ("A star splices a list into a list", "", "[*[1, 2], *[3]]")]), "caption": "A comprehension builds a new list; its loop variable does not stay behind."}
# ---- sequence types ------------------------------------------------------------------------------------------------------------
from collections.abc import MutableSequence
types_ = []
for nm, sample, assign in (("list", "['A', 'B', 'C']", "x[1] = 'X'"), ("str", "'Zophie a cat'", "x[7] = 'the'"), ("tuple", "('hello', 42, 0.5)", "x[1] = 99"), ("range", "range(3)", "x[1] = 5")):
    ns = {"x": eval(sample)}
    try: exec(assign, ns); res = "ok: " + rp(ns["x"])
    except TypeError as e: res = "%s: %s" % (type(e).__name__, e)
    types_.append({"type": nm, "sample": sample, "mutable": isinstance(eval(sample), MutableSequence), "mutable_label": "mutable" if isinstance(eval(sample), MutableSequence) else "immutable", "assign": assign, "result": res})
V["MutableVersusImmutable"] = {"kind": "seqtypes", "types": types_, "caption": "Among list, str, tuple and range only the list is a mutable sequence."}
V["TupleType"] = {"kind": "facts", "facts": facts([("A comma makes the tuple", "", "type(('hello',))"), ("Parentheses alone do not", "", "type(('hello'))"),
                  ("A changed string is rebuilt from slices", "name = 'Zophie a cat'", "name[0:7] + 'the' + name[8:12]")]), "caption": "A one-item tuple needs its comma."}
# ---- references ----------------------------------------------------------------------------------------------------------------
V["ReferencesAndAliasing"] = {"kind": "refgraph", "caption": "Assignment binds a name to an object and copies nothing. A number is replaced; a list is shared.",
    "scenarios": [scenario("a list is shared", ["spam = [0, 1, 2, 3]", "eggs = spam", "eggs[1] = 'Hello!'"], ["spam", "eggs"]), scenario("a number is only rebound", ["spam = 42", "eggs = spam", "spam = 99"], ["spam", "eggs"])]}
rec = traced(PROGRAMS["passing_v1_0_0.py"][0], None)
def pickf(func, event, prefix, nth=0):
    hits = [r for r in rec if r["func"] == func and r["event"] == event and r["text"].startswith(prefix)]; return hits[nth]
def steps_of(frames):
    return renumber([dict(f["snap"], code=lab) for f, lab in frames])
A1 = pickf("eggs", "line", "some_parameter.append"); A2 = pickf("<module>", "line", "print(spam)", 0); B1 = pickf("reassign", "return", "some_parameter = some_parameter + "); B2 = pickf("<module>", "line", "print(spam)", 1)
# keep the caller's frame in the graph while inside the call: the snapshot of a function frame already holds module and function scopes
V["ListArguments"] = {"kind": "refgraph", "code": PROGRAMS["passing_v1_0_0.py"][0], "caption": "The function receives a reference. A method call changes the caller's list; assigning to the parameter only rebinds the local name.",
    "scenarios": [{"title": "the function calls append", "steps": steps_of([(A1, "inside the function, before append"), (A2, "back in the caller")])},
                  {"title": "the function assigns a new list", "steps": steps_of([(B1, "inside the function, after the assignment"), (B2, "back in the caller")])}]}
V["Copying"] = {"kind": "refgraph", "caption": "copy.copy makes a new outer list holding the same inner lists; copy.deepcopy copies the inner lists too.",
    "scenarios": [scenario("a flat list: the copy is independent", ["spam = ['A', 'B', 'C']", "cheese = copy.copy(spam)", "cheese[1] = 42"], ["spam", "cheese"]),
                  scenario("a nested list", ["nested = [[1, 2], [3]]", "shallow = copy.copy(nested)", "deep = copy.deepcopy(nested)", "nested[0].append('changed')"], ["nested", "shallow", "deep"])]}
V["ReplicationAliasing"] = {"kind": "refgraph", "caption": "* repeats references: [[]] * 3 holds one inner list three times.",
    "scenarios": [scenario("[[]] * 3", ["lists = [[]] * 3", "lists[0].append(3)"], ["lists"]), scenario("[[] for i in range(3)]", ["lists = [[] for i in range(3)]", "lists[0].append(3)"], ["lists"])]}
# ---- random and the programs -------------------------------------------------------------------------------------------------
ns = {}; exec(EIGHT.split("print(")[0], ns); msgs = ns["messages"]; random.seed(8); cnt = [0] * len(msgs)
for _ in range(2000): cnt[random.randint(0, len(msgs) - 1)] += 1
assert all(cnt)
V["MagicEightBall"] = {"kind": "hist", "draws": 2000, "seed": 8, "bars": [{"index": i, "label": m, "text": "%d  %s" % (i, m), "count": c} for i, (m, c) in enumerate(zip(msgs, cnt))],
                       "caption": "randint includes both ends, so every index from 0 to 8, and every answer, can appear."}
V["RandomShuffle"] = {"kind": "facts", "facts": facts([("choice returns one item and leaves the list alone", "import random; random.seed(3)", "random.choice(['Dog', 'Cat', 'Moose'])"),
                          ("shuffle reorders the list itself and returns None", "import random; random.seed(3); people = ['Alice', 'Bob', 'Carol', 'David']", "(random.shuffle(people), people)"),
                          ("sample with k = len returns a new shuffled list", "import random; random.seed(3); people = ['Alice', 'Bob', 'Carol', 'David']", "random.sample(people, k=len(people))")]),
                      "caption": "choice picks an item; shuffle reorders a list in place; sample gives a shuffled new list."}
# matrix: run the chapter's program with time.sleep replaced, capturing the columns after every printed row
import time
def matrix_run(source, rows_wanted, seed=5):
    calls = []; states = []; gl = {}
    def fake_sleep(s):
        calls.append(s); states.append(list(gl["columns"]))
        if len(calls) == rows_wanted: raise KeyboardInterrupt
    real = time.sleep; time.sleep = fake_sleep; random.seed(seed); buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try: exec(source, gl)
            except SystemExit: pass
    finally: time.sleep = real
    return buf.getvalue().split("\n")[:-1], states
mrows, mstates = matrix_run(MATRIX, 300)
W = 70; assert len(mrows) == 300 and all(len(r) == W for r in mrows)
def stream(col):
    """A column's first complete stream: the row where its counter is set, and the rows through the space after it."""
    r = 1
    while r < 299:
        if mrows[r][col] != " " and mrows[r - 1][col] == " ":
            e = r
            while e < 300 and mrows[e][col] != " ": e += 1
            if e < 300: return r - 1, e
        r += 1
    return None
best = None
for col in range(W):
    s_ = stream(col)
    if s_ and (s_[1] - s_[0]) <= 7 and (best is None or s_[0] < best[1][0]): best = (col, s_)
col, (a, b) = best
life = [{"row": t + 1, "char": mrows[t][col] if mrows[t][col] != " " else "space", "counter": mstates[t][col]} for t in range(a, b + 1)]
life_cols = ["row", "printed", "counter after the row"]
bad_src = MATRIX.replace("                print(random.choice([0, 1]), end='')\n                columns[i] -= 1\n", "                print(random.choice([0, 1]), end='')\n").replace("        print()\n", "            columns[i] -= 1\n        print()\n")
assert bad_src != MATRIX
brows, _ = matrix_run(bad_src, 300)
V["MatrixScreensaver"] = {"kind": "matrix", "width": W, "seed": 5, "code": MATRIX, "frames": [{"label": "rows 1 to 6: streams begin", "first": 1, "rows": mrows[0:6]}, {"label": "rows 295 to 300", "first": 295, "rows": mrows[294:300]}],
    "column": col, "life_cols": life_cols, "life": life, "hazard": [{"label": "counter decremented only for a column above zero (the chapter)", "row": mrows[-1], "spaces": mrows[-1].count(" "), "spaces_label": "%d spaces" % mrows[-1].count(" ")},
                                             {"label": "counter decremented for every column", "row": brows[-1], "spaces": brows[-1].count(" "), "spaces_label": "%d spaces" % brows[-1].count(" ")}],
    "caption": "Each column keeps a counter: above zero it prints a random 0 or 1 and counts down; at zero it prints a space."}
# practice: the research programs, executed
pp = [c for t, c, w in R.BEH if t.startswith("practice program")][0]
head = pp[:pp.index("print(repr")]; dp = pp[pp.index("P = {1: 1.0}"):pp.index("print(round(hit, 3))")]
ns = {}; exec(head, ns); ns2 = {}; exec(dp, ns2); ns3 = {"spam": ["a", "b", "c", "d"]}
V["PracticePrograms"] = {"kind": "facts", "facts": [
    {"label": "Practice program 1: comma code", "expr": "comma_code(['apples', 'bananas', 'tofu', 'cats'])", "result": rp(ns["comma_code"](["apples", "bananas", "tofu", "cats"]))},
    {"label": "Practice program 2: a streak of six in 100 flips", "expr": "exact chance, by counting run lengths", "result": rp(round(ns2["hit"], 3))},
    {"label": "Question 3 of the chapter", "expr": "spam[int(int('3' * 2) // 11)]", "result": ev("spam[int(int('3' * 2) // 11)]", ns3)}], "caption": "Two practice programs and 17 practice questions close the chapter."}
V["_kinds"] = {"classify": "columns of chips: operations grouped by what they do to a list",
               "boxes": "a row of boxes with positive and negative indexes, picks and an error", "slices": "rows of slices with the indexes they select",
               "lanes": "an operation with the list before and after, what it returned and whether it is the same object", "refgraph": "snapshots of names and the objects they reach",
               "facts": "an executed expression and its result", "keysort": "input row, keys, and output row of a sort", "passes": "one row per pass of a loop",
               "mutation": "a line-traced loop that changes the list it walks", "unpack": "names taking items of a list", "seqtypes": "sequence types with mutability and the result of item assignment",
               "hist": "counts of 2000 seeded draws", "matrix": "rows printed by the chapter's program, one column's counter life, and a misplaced-decrement variant"}
V["_meta"] = {"version": __version__, "python": platform.python_version(), "note": "Executed specifications; drawn by the deck and by the page."}
json.dump(V, open(sys.argv[1], "w"), indent=1, ensure_ascii=False)
print("written", sys.argv[1], "under Python", platform.python_version(), "-", len([k for k in V if not k.startswith("_")]), "visuals")
