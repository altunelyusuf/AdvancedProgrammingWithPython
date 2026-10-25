"""Chapter 3 deck visuals, version 5.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from the run of the example itself (the namespace `ns` and
the printed text `out` that deck_build_v5_0_0.py passes in) or from a probe of the same Python objects; nothing is typed in by
hand except the plain-language names of columns and boxes.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "5.0.0"
import ast
import math
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v5_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def vis(c):
    return {" ": "·", "\n": "⏎", "\t": "⇥"}.get(c, c)


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO if mono else None, line=C["line"], radius=0.15)


def strip(s, x, y, text, cw, ch, fills=None, fs=12, idx=True, label_fs=8):
    """A row of character cells with the index below; fills maps index -> kind."""
    fills = fills or {}
    for i, c in enumerate(text):
        f, col = {"teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]), "green": (C["greenLight"], C["ink"]),
                  "red": (C["redLight"], C["ink"])}.get(fills.get(i), (C["card"], C["ink"]))
        label_shape(s, x + i * cw, y, cw - 0.025, ch, vis(c), f, col, size=fs, font=MONO, line=C["line"], radius=0.1)
        if idx:
            tb(s, x + i * cw, y + ch, cw - 0.025, 0.18, str(i), label_fs, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def lines(out):
    return [l for l in out.split("\n") if l != ""]


def rh(h, n, top=0.3):
    return min(top, h / n)


# ------------------------------------------------------------------ part 1: while
@need(1.45)
def v_while(s, x, y, w, h, ns, out):
    ls = lines(out)
    rows = [["Test", "spam", "spam < 5", "Block runs?"]]
    cc = {}
    for k, l in enumerate(ls[:-1], 1):
        sp = int(l.split()[1])
        rows.append([str(k), str(sp), l.split()[-1], "yes"])
        cc[(k, 2)] = C["green"]
    rows.append([str(len(ls)), str(ns["spam"]), ls[-1].split()[-1], "no: the loop ends"])
    cc[(len(rows) - 1, 2)] = C["coral"]
    table(s, x, y, w * 0.6, rows, [0.8, 0.8, 1.2, 2.0], rowh=rh(h, len(rows), 0.26), fs=10, mono_cols=(1, 2), cell_color=cc, align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.64, y, w * 0.36, h, ["t%d" % k for k in range(1, len(rows))], [("spam at the test", [int(r[1]) for r in rows[1:]])], fs=9, legend=False, gap=40, vmax=6, major=2)


@need(1.4)
def v_accumulator(s, x, y, w, h, ns, out):
    steps = ns["steps"]
    ns_ = [20 * (i + 1) for i in range(len(steps))]
    rows = [["After n =", "Running total", "n(n+1)/2", "Equal?"]] + [[str(n), str(t), str(n * (n + 1) // 2), str(t == n * (n + 1) // 2)] for n, t in zip(ns_, steps)]
    cc = {(i + 1, 3): C["green"] for i in range(len(steps))}
    table(s, x, y, w * 0.58, rows, [1.2, 1.5, 1.3, 1.0], rowh=rh(h, len(rows), 0.27), fs=10, mono_cols=(0, 1, 2, 3), cell_color=cc, align_cols={j: PP_ALIGN.CENTER for j in range(4)})
    chart(s, "col", x + w * 0.62, y, w * 0.38, h, ["n=%d" % n for n in ns_], [("running total", steps)], fs=9, legend=False, gap=40, vmax=6000, major=2000)


@need(1.3)
def v_breakloop(s, x, y, w, h, ns, out):
    ls = lines(out)
    rows = [["Pass", "Typed", "Is it Alice?", "What the loop does"]]
    cc = {}
    for k, l in enumerate(ls[:-1], 1):
        typed = l[len("typed "):l.index(" - is it")]
        ok = l.endswith("True")
        rows.append([str(k), typed, str(ok), "break: leave the loop" if ok else "go round again"])
        cc[(k, 2)] = C["green"] if ok else C["coral"]
    table(s, x, y, w * 0.72, rows, [0.7, 1.1, 1.4, 2.4], rowh=rh(h, len(rows) + 1, 0.3), fs=10.5, mono_cols=(1, 2), cell_color=cc, align_cols={0: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER})
    chip(s, x + w * 0.75, y, w * 0.25, 0.34, ls[-1], "green", fs=10.5)
    tb(s, x + w * 0.75, y + 0.42, w * 0.25, 0.6, "printed after the loop, once break has left it", 9.5, C["muted"], italic=True)


@need(1.4)
def v_continue(s, x, y, w, h, ns, out):
    shown, skipped = ns["shown"], ns["skipped"]
    allv = sorted(shown + skipped)
    cw = 0.5
    strip(s, x, y + 0.05, "".join(str(v) for v in allv), cw, 0.42, {i: ("teal" if v in shown else "amber") for i, v in enumerate(allv)}, fs=14, idx=False)
    for i, v in enumerate(allv):
        if v in skipped:
            arrow(s, x + i * cw + cw / 2 - 0.01, y + 0.52, x + i * cw + cw / 2 - 0.01, y + 0.88, C["amber"], 1.2)
    chip(s, x, y + 0.92, 4.3, 0.3, "amber: continue sent the loop back to the test", "amber", fs=9.5, mono=False)
    chip(s, x, y + 1.27, 4.3, 0.3, "teal: the number reached shown.append", "teal", fs=9.5, mono=False)
    rows = [["List", "Numbers", "How many"], ["shown", str(shown), str(len(shown))], ["skipped", str(skipped), str(len(skipped))]]
    table(s, x + 4.5, y, w - 4.5, rows, [1.0, 2.2, 0.9], rowh=0.34, fs=10, mono_cols=(0, 1), align_cols={2: PP_ALIGN.CENTER})


@need(1.3)
def v_walrus(s, x, y, w, h, ns, out):
    ls = lines(out)
    chunks = [ast.literal_eval(l) for l in ls[:-1]] + [ast.literal_eval(ls[-1].split(" ")[0])]
    rows = [["Read", "chunk", "Length", "Truth value", "Loop"]]
    cc = {}
    for k, c in enumerate(chunks, 1):
        rows.append([str(k), repr(c), str(len(c)), str(bool(c)), "goes on" if c else "ends"])
        cc[(k, 3)] = C["green"] if c else C["coral"]
    table(s, x, y, w * 0.64, rows, [0.7, 1.1, 0.8, 1.2, 0.9], rowh=rh(h, len(rows), 0.26), fs=10, mono_cols=(1, 3), cell_color=cc, align_cols={0: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.68, y, w * 0.32, h, ["#%d" % k for k in range(1, len(chunks) + 1)], [("characters read", [len(c) for c in chunks])], fs=9, legend=False, gap=40, vmax=6, major=2)


# ------------------------------------------------------------------ part 2: for and range
@need(1.4)
def v_forrange(s, x, y, w, h, ns, out):
    ls = [l.split() for l in lines(out)[:-1]]
    rows = [["Pass", "i", "total"]] + [[str(k), l[2], l[5]] for k, l in enumerate(ls, 1)]
    table(s, x, y, w * 0.5, rows, [0.9, 0.9, 1.2], rowh=rh(h, len(rows), 0.26), fs=10, mono_cols=(1, 2), align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.54, y, w * 0.46, h, ["i=%s" % l[2] for l in ls], [("total after the pass", [int(l[5]) for l in ls])], fs=9, legend=False, gap=40, vmax=12, major=4)


@need(1.4)
def v_rangeargs(s, x, y, w, h, ns, out):
    calls = ["range(5)", "range(2, 8)", "range(0, 10, 3)", "range(5, 0, -2)"]
    rows = [["Call", "Items", "Count"]]
    sets = []
    for c in calls:
        r = eval(c)
        sets.append(set(r))
        rows.append([c, str(list(r)), str(len(r))])
    table(s, x, y, w * 0.6, rows, [1.7, 2.9, 0.7], rowh=rh(h, len(rows), 0.3), fs=10, mono_cols=(0, 1), align_cols={2: PP_ALIGN.CENTER})
    cw = 0.27
    xs = x + w * 0.64
    tb(s, xs, y - 0.02, 3.0, 0.2, "which of 0 to 9 each call gives", 9, C["muted"], italic=True)
    for k, st in enumerate(sets):
        strip(s, xs, y + 0.2 + k * 0.33, "0123456789", cw, 0.27, {i: "teal" for i in st}, fs=9, idx=False)
    arrow(s, xs, y + 0.2 + 4 * 0.33 + 0.1, xs + 10 * cw - 0.03, y + 0.2 + 4 * 0.33 + 0.1, C["muted"], 1.2)


@need(1.4)
def v_lazyrange(s, x, y, w, h, ns, out):
    r = ns["r"]
    rows = [["Expression", "Result", "How Python answers"],
            ["len(r)", str(len(r)), "from start, stop and step"],
            ["r[999999999]", str(r[999999999]), "by arithmetic"],
            ["123456789 in r", str(123456789 in r), "by arithmetic, no search"],
            ["r[:3]", str(r[:3]), "another range, not a list"]]
    table(s, x, y, w * 0.66, rows, [1.7, 1.9, 2.4], rowh=rh(h, len(rows), 0.3), fs=10, mono_cols=(0, 1))
    xs = x + w * 0.7
    chip(s, xs, y, 2.4, 0.3, "start %d  stop 10**9  step %d" % (r.start, r.step), "teal", fs=9)
    arrow(s, xs + 1.2, y + 0.32, xs + 1.2, y + 0.62, C["teal"])
    chip(s, xs, y + 0.65, 2.4, 0.3, "any value, on demand", "amber", fs=10, mono=False)
    tb(s, xs, y + 1.0, 2.5, 0.3, "stored: 3 numbers", 10, C["muted"], italic=True)


# ------------------------------------------------------------------ part 3: what a for loop visits
@need(1.4)
def v_listtuple(s, x, y, w, h, ns, out):
    pets = ns["pets"]
    chart(s, "col", x, y, w * 0.4, h, pets, [("letters in the name", [len(p) for p in pets])], fs=9, legend=False, gap=50, vmax=6, major=2)
    rows = [["", "list", "tuple"],
            ["brackets", "[ ]", "( )"],
            ["has append()", str(hasattr(pets, "append")), str(hasattr(ns["point"], "append"))],
            ["visited by for", "yes", "yes"],
            ["printed by the loop", str(lines(out)[:3]).replace("'", "")[1:-1], str(lines(out)[3:])[1:-1].replace("'", "")]]
    table(s, x + w * 0.44, y, w * 0.56, rows, [1.7, 2.0, 1.2], rowh=rh(h, len(rows), 0.3), fs=10, mono_cols=(1, 2), align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER})


@need(1.4)
def v_dictloop(s, x, y, w, h, ns, out):
    ages = ns["ages"]
    chart(s, "bar", x, y, w * 0.42, h, list(ages)[::-1], [("age", list(ages.values())[::-1])], fs=9, legend=False, gap=40, vmax=9, major=3)
    rows = [["Call", "Gives"], ["ages.items()", str(list(ages.items()))], ["ages.values()", str(list(ages.values()))], ["list(ages)", str(list(ages))], ["sum(ages.values())", str(sum(ages.values()))]]
    table(s, x + w * 0.46, y, w * 0.54, rows, [1.7, 3.3], rowh=rh(h, len(rows), 0.3), fs=9.5, mono_cols=(0, 1))


@need(1.4)
def v_enumzip(s, x, y, w, h, ns, out):
    names, scores = ns["names"], ns["scores"]
    chart(s, "col", x, y, w * 0.36, h, names, [("score", scores)], fs=9, legend=False, gap=50, vmax=100, major=25)
    rows = [["enumerate", "zip"]] + [["%d, %r" % (i, n), "(%r, %d)" % (n, sc)] for i, (n, sc) in enumerate(zip(names, scores), 1)]
    table(s, x + w * 0.4, y, w * 0.6, rows, [2.3, 2.7], rowh=rh(h, len(rows), 0.3), fs=10, mono_cols=(0, 1))


@need(1.5)
def v_zipstrict(s, x, y, w, h, ns, out):
    left, right = [1, 2, 3], ["x", "y"]
    for i, a in enumerate(left):
        chip(s, x, y + i * 0.42, 0.5, 0.32, str(a), "teal", fs=11)
        if i < len(right):
            arrow(s, x + 0.55, y + i * 0.42 + 0.16, x + 1.25, y + i * 0.42 + 0.16, C["teal"])
            chip(s, x + 1.3, y + i * 0.42, 0.5, 0.32, repr(right[i]), "amber", fs=11)
        else:
            arrow(s, x + 0.55, y + i * 0.42 + 0.16, x + 1.25, y + i * 0.42 + 0.16, C["coral"])
            chip(s, x + 1.3, y + i * 0.42, 0.9, 0.32, "no partner", "red", fs=9.5, mono=False)
    ls = lines(out)
    rows = [["Call", "What happens"], ["zip(..., strict=True)", ls[2]], ["zip(...) without strict", ls[3]]]
    table(s, x + 2.6, y, w - 2.6, rows, [2.2, 4.2], rowh=0.42, fs=10, mono_cols=(0, 1))


@need(1.5)
def v_iterator(s, x, y, w, h, ns, out):
    ls = lines(out)
    items = [("['a', 'b']", "teal"), ("iter(...)", "plain"), ("next -> a", "amber"), ("next -> b", "amber"), ("next -> StopIteration", "red")]
    cw = [1.4, 1.2, 1.3, 1.3, 2.1]
    xx = x
    for (t, k), c in zip(items, cw):
        chip(s, xx, y, c, 0.36, t, k, fs=10)
        if (t, k) != items[-1]:
            arrow(s, xx + c + 0.02, y + 0.18, xx + c + 0.22, y + 0.18, C["muted"])
        xx += c + 0.25
    rows = [["Step", "Printed", "Meaning"], ["print(next(it), next(it))", ls[0], "two items, in order"], ["next(it) once more", ls[1], "StopIteration was caught"], ["iter(it) is it, iter([1]) is [1]", ls[2], "iterator: True; list: False"]]
    table(s, x, y + 0.5, w, rows, [3.2, 1.3, 3.2], rowh=0.25, fs=10, mono_cols=(0, 1))


@need(1.3)
def v_loopelse(s, x, y, w, h, ns, out):
    ls = lines(out)
    rows = [["List", "First even number", "break happened?", "else ran?"]]
    cc = {}
    for k, l in enumerate(ls, 1):
        brk = "first even" in l
        lst = l[:l.index("]") + 1]
        rows.append([lst, l.split()[-1] if brk else "none", str(brk), str(not brk)])
        cc[(k, 2)] = C["green"] if brk else C["coral"]
        cc[(k, 3)] = C["coral"] if brk else C["green"]
    table(s, x, y, w * 0.7, rows, [1.6, 2.0, 1.8, 1.4], rowh=0.36, fs=10.5, mono_cols=(0, 1, 2, 3), cell_color=cc, align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER})
    xs = x + w * 0.73
    chip(s, xs, y, w * 0.27, 0.34, "break -> skip else", "amber", fs=10, mono=False)
    chip(s, xs, y + 0.5, w * 0.27, 0.34, "no break -> else runs", "teal", fs=10, mono=False)


# ------------------------------------------------------------------ part 4: modules and leaving early
@need(1.4)
def v_importrandom(s, x, y, w, h, ns, out):
    rolls = ns["rolls"]
    chart(s, "col", x, y, w * 0.45, h, [str(f) for f in range(1, 7)], [("times rolled", [rolls.count(f) for f in range(1, 7)])], fs=9, legend=False, gap=40, vmax=3, major=1)
    rows = [["What", "Value"], ["rolls", str(rolls)], ["random.__name__", repr(ns["random"].__name__)], ["type(random).__name__", repr(type(ns["random"]).__name__)]]
    table(s, x + w * 0.49, y, w * 0.51, rows, [2.2, 2.5], rowh=rh(h, len(rows), 0.32), fs=10, mono_cols=(0, 1))


@need(1.5)
def v_importforms(s, x, y, w, h, ns, out):
    m = ns["math"]
    rect(s, x, y, 3.0, 1.4, C["card"], line=C["line"], radius=0.06, name="card")
    tb(s, x + 0.1, y + 0.02, 2.8, 0.24, "this program", 9.5, C["muted"], italic=True)
    names = [k for k in ns if not k.startswith("__") and k in ("math", "root")]
    for i, n in enumerate(names):
        chip(s, x + 0.3, y + 0.32 + i * 0.5, 1.2, 0.34, n, "teal", fs=11)
    rect(s, x + 4.6, y, 3.0, 1.4, C["card"], line=C["line"], radius=0.06, name="card")
    tb(s, x + 4.7, y + 0.02, 2.8, 0.24, "module math", 9.5, C["muted"], italic=True)
    for i, n in enumerate(["sqrt", "pi", "floor"]):
        assert hasattr(m, n)
        chip(s, x + 4.9 + (i % 2) * 1.3, y + 0.32 + (i // 2) * 0.5, 1.15, 0.34, n, "amber", fs=11)
    arrow(s, x + 1.55, y + 0.49, x + 4.85, y + 0.49, C["teal"])
    arrow(s, x + 1.55, y + 0.99, x + 4.85, y + 0.55, C["teal"])
    chip(s, x + 7.8, y, w - 7.8, 0.34, "sqrt here? %s" % ("sqrt" in ns), "red", fs=9.5)
    tb(s, x + 7.8, y + 0.42, w - 7.8, 0.9, "math and root both lead into math; the bare name sqrt does not exist here", 9.5, C["muted"], italic=True)


@need(1.4)
def v_importerror(s, x, y, w, h, ns, out):
    ls = lines(out)
    items = [("import nosuchmodule", "teal", 2.2), ("folder 1 of sys.path", "plain", 1.9), ("folder 2", "plain", 1.0), ("... folder n", "plain", 1.2), ("not found", "red", 1.2)]
    xx = x
    for t, k, c in items:
        chip(s, xx, y, c, 0.36, t, k, fs=9.5)
        if t != items[-1][0]:
            arrow(s, xx + c + 0.02, y + 0.18, xx + c + 0.17, y + 0.18, C["muted"])
        xx += c + 0.19
    rows = [["Printed", "Meaning"], [ls[0], "the module name is in the error text"], [ls[1], "sys.path is a list of folders"]]
    table(s, x, y + 0.55, w, rows, [5.4, 3.8], rowh=0.3, fs=10, mono_cols=(0,))


@need(1.25)
def v_sysexit(s, x, y, w, h, ns, out):
    ls = lines(out)
    items = [("print('working')", "teal", ls[0]), ("sys.exit(3)", "amber", "SystemExit raised"), ("except SystemExit", "amber", ls[1]), ("finally", "teal", ls[2])]
    xx = x
    for i, (t, k, res) in enumerate(items):
        chip(s, xx, y, 1.45, 0.34, t, k, fs=9.5)
        tb(s, xx, y + 0.37, 1.55, 0.42, res, 8.5, C["muted"], italic=True)
        if i < len(items) - 1:
            arrow(s, xx + 1.47, y + 0.17, xx + 1.65, y + 0.17, C["muted"])
        xx += 1.68
    chip(s, x, y + 0.88, 2.4, 0.3, "print('never printed')", "grey", fs=9)
    rows = [["Exit status", "Usual meaning"], ["0", "the program finished well"], ["1 or more", "something went wrong; 3 is our choice"]]
    table(s, x + 6.9, y, w - 6.9, rows, [0.9, 2.0], rowh=0.34, fs=9, mono_cols=(0,))


# ------------------------------------------------------------------ part 5: two short programs
@need(1.2)
def v_guess1(s, x, y, w, h, ns, out):
    ls = lines(out)
    secret = ns["secret"]
    rows = [["Pass", "Guess", "Hint"]]
    gs = []
    for k, l in enumerate(ls[:-1], 1):
        g, hint = l.split()
        gs.append(int(g))
        rows.append([str(k), g, hint])
    gs.append(ns["guess"])
    rows.append([str(len(gs)), str(ns["guess"]), "right: break"])
    cc = {(len(rows) - 1, 2): C["green"]}
    table(s, x, y, w * 0.45, rows, [0.8, 0.9, 1.6], rowh=rh(h, len(rows), 0.26), fs=10, mono_cols=(1, 2), cell_color=cc, align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.5, y, w * 0.5, h, ["pass %d" % k for k in range(1, len(gs) + 1)], [("guess", gs), ("secret", [secret] * len(gs))], fs=9, legend=True, gap=60, vmax=20, major=5, colors=[C["teal"], C["amber"]])


@need(1.3)
def v_guess2(s, x, y, w, h, ns, out):
    ls = lines(out)
    used = [int(ls[0].split()[-2]), len(ns["guesses"])]
    rows = [["Game", "Guesses", "Printed", "else ran?"], ["1", "10, 15, 12, 11", ls[0], "False"], ["2", "1, 2, 3, 4, 5, 6", ls[1], "True"]]
    cc = {(1, 3): C["coral"], (2, 3): C["green"]}
    table(s, x, y, w * 0.68, rows, [0.6, 1.6, 2.9, 0.9], rowh=0.42, fs=10, mono_cols=(1, 2, 3), cell_color=cc, align_cols={0: PP_ALIGN.CENTER, 3: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.72, y, w * 0.28, h, ["game 1", "game 2"], [("guesses used", used)], fs=9, legend=False, gap=50, vmax=8, major=2)


@need(1.3)
def v_rps1(s, x, y, w, h, ns, out):
    names = {"r": "rock", "p": "paper", "s": "scissors"}
    p, c = ns["player"], ns["computer"]
    chip(s, x, y, 2.2, 0.4, "player: %s (%s)" % (p, names[p]), "teal", fs=10.5, mono=False)
    chip(s, x, y + 0.7, 2.2, 0.4, "computer: %s (%s)" % (c, names[c]), "amber", fs=10.5, mono=False)
    arrow(s, x + 2.25, y + 0.2, x + 3.15, y + 0.55, C["teal"])
    arrow(s, x + 2.25, y + 0.9, x + 3.15, y + 0.6, C["amber"])
    chip(s, x + 3.2, y + 0.38, 1.6, 0.44, "result: %s" % ns["result"], "green", fs=11.5, mono=False)
    rows = [["Move", "beats"]] + [["%s (%s)" % (k, names[k]), "%s (%s)" % (v, names[v])] for k, v in ns["beats"].items()]
    table(s, x + 5.2, y, w - 5.2, rows, [1.8, 2.1], rowh=0.3, fs=10, mono_cols=(0, 1))


@need(1.3)
def v_rps2(s, x, y, w, h, ns, out):
    ls = lines(out)[:-1]
    rows = [["Round", "Player", "Computer", "Result"]]
    cc = {}
    for k, l in enumerate(ls, 1):
        a = l.split()
        rows.append([str(k), a[0], a[2], a[3]])
        cc[(k, 3)] = {"win": C["green"], "lose": C["coral"], "tie": C["greyTxt"]}[a[3]]
    table(s, x, y, w * 0.55, rows, [0.9, 1.0, 1.2, 1.1], rowh=rh(h, len(rows), 0.25), fs=10, mono_cols=(1, 2, 3), cell_color=cc, align_cols={j: PP_ALIGN.CENTER for j in range(4)})
    sc = ns["score"]
    chart(s, "col", x + w * 0.6, y, w * 0.4, h, list(sc), [("rounds", list(sc.values()))], fs=9, legend=False, gap=50, vmax=4, major=1)


VISUALS = {"while": v_while, "accumulator": v_accumulator, "breakloop": v_breakloop, "continue": v_continue, "walrus": v_walrus,
           "forrange": v_forrange, "rangeargs": v_rangeargs, "lazyrange": v_lazyrange,
           "listtuple": v_listtuple, "dictloop": v_dictloop, "enumzip": v_enumzip, "zipstrict": v_zipstrict, "iterator": v_iterator, "loopelse": v_loopelse,
           "importrandom": v_importrandom, "importforms": v_importforms, "importerror": v_importerror, "sysexit": v_sysexit,
           "guess1": v_guess1, "guess2": v_guess2, "rps1": v_rps1, "rps2": v_rps2}
