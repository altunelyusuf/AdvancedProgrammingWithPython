"""Chapter 6 deck visuals, version 3.1.1 (over 3.1.0, which stays as committed: the tuple row of the sequences visual shows the tuple the code builds, (3, 4), not a longer one): the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from a run of the example's own code (the namespace `ns`
and the printed text `out` that deck_build_v3_1_0.py passes in, or the same operations re-run here on the same values); nothing is
typed in by hand except the plain-language names of columns and rows.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "3.1.1"
import ast
import copy
import random
from collections import Counter
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v3_1_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg


def table(s, x, y, w, rows, colw, fs=10, **kw):
    """the kit table with the visuals' default font size (10 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=False):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=None, line=C["line"], radius=0.15)


def lines_of(out):
    return [l for l in out.split("\n") if l != ""]


def strip(s, x, y, items, cw, ch, fills=None, fs=11, idx=True, neg=True, label_fs=9.5, mono=False):
    """A row of cells holding the items, with the index above and the negative index below; fills maps index -> kind."""
    fills = fills or {}
    n = len(items)
    for i, it in enumerate(items):
        label_shape(s, x + i * cw, y, cw - 0.04, ch, str(it), {"teal": C["tealLight"], "amber": C["amberLight"], "green": C["greenLight"], "red": C["redLight"]}.get(fills.get(i), C["card"]),
                    C["ink"], size=fs, line=C["line"], radius=0.1)
        if idx:
            tb(s, x + i * cw, y - 0.22, cw - 0.04, 0.2, str(i), label_fs, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
        if neg:
            tb(s, x + i * cw, y + ch + 0.01, cw - 0.04, 0.2, str(i - n), label_fs, C["coral"], align=PP_ALIGN.CENTER, margin=(0, 0))


def label(s, x, y, w, text, fs=10, color=None, bold=False):
    return tb(s, x, y, w, 0.24, text, fs, color or C["muted"], bold=bold, italic=not bold, margin=(0, 0))


# ------------------------------------------------------------------ part 1
@need(1.55)
def v_indexes(s, x, y, w, h, ns, out):
    spam = ns["spam"]
    strip(s, x, y + 0.5, spam, 1.12, 0.46, {0: "teal", 3: "teal"}, fs=11)
    label(s, x, y, 4.4, "index above (from the left), minus index below (from the right)", 9.5)
    ls = lines_of(out)
    rows = [["Expression", "Printed"], ["spam[0], spam[3]", ls[0]], ["spam[-1], spam[-3]", ls[1]], ["len(spam)", ls[2]]]
    table(s, x + 4.75, y + 0.05, w - 4.75, rows, [2.2, 2.2], rowh=0.34, mono_cols=(0, 1))


@need(1.5)
def v_nested(s, x, y, w, h, ns, out):
    grid = ns["grid"]
    for r, row in enumerate(grid):
        tb(s, x, y + 0.1 + r * 0.55, 1.0, 0.4, "grid[%d]" % r, 10.5, C["muted"], anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))
        for c, it in enumerate(row):
            hit = (r, c) == (1, 2)
            label_shape(s, x + 1.0 + c * 0.7, y + 0.1 + r * 0.55, 0.64, 0.42, repr(it), C["amberLight"] if hit else C["card"], C["ink"], size=11, line=C["line"], radius=0.1)
    tb(s, x + 3.2, y + 0.65, 1.7, 0.4, "grid[1][2]", 10.5, C["coral"], bold=True, anchor=MSO_ANCHOR.MIDDLE)
    arrow(s, x + 3.2, y + 0.85, x + 2.45, y + 0.62, C["coral"], 1.6)
    ls = lines_of(out)
    chip(s, x + 5.0, y + 0.1, w - 5.0, 0.4, ls[0], "green", fs=10.5, mono=True)
    chip(s, x + 5.0, y + 0.65, w - 5.0, 0.4, ls[1], "red", fs=10.5, mono=True)
    tb(s, x + 5.0, y + 1.1, w - 5.0, 0.24, "the second print is the caught error", 9.5, C["muted"], italic=True, margin=(0, 0))


@need(1.75)
def v_slices(s, x, y, w, h, ns, out):
    spam = ns["spam"]
    strip(s, x, y + 0.5, spam, 1.12, 0.46, {1: "teal", 2: "teal"}, fs=11)
    label(s, x, y, 4.5, "spam[1:3] takes the two highlighted cells", 9.5)
    exprs = ["spam[1:3]", "spam[:2]", "spam[2:]", "spam[::2]", "spam[::-1]", "spam[:] == spam", "spam[:] is spam"]
    rows = [["Expression", "Result"]] + [[e, repr(eval(e, {"spam": spam}))] for e in exprs]
    table(s, x + 4.7, y, w - 4.7, rows, [1.8, 2.7], rowh=0.215, fs=9, mono_cols=(0, 1))


@need(1.5)
def v_dijkstra(s, x, y, w, h, ns, out):
    sl = ns["s"]
    strip(s, x, y + 0.24, sl, 0.52, 0.4, {2: "teal", 3: "teal", 4: "teal"}, fs=11, neg=False)
    for i, (a, b, kind) in enumerate([(0, 3, "amber"), (3, 10, "green")]):
        label_shape(s, x + a * 0.52, y + 0.78 + i * 0.36, (b - a) * 0.52 - 0.04, 0.3, "s[%d:%d]  %d items" % (a, b, len(sl[a:b])), C["amberLight"] if kind == "amber" else C["greenLight"], C["ink"], size=10, line=C["line"], radius=0.1)
    ls = lines_of(out)
    rows = [["Check", "Printed"], ["s[2:5], len(s[2:5])", ls[0]], ["s[0:3] + s[3:10] == s", ls[1]], ["three lengths", ls[2]]]
    table(s, x + 5.5, y, w - 5.5, rows, [1.9, 1.8], rowh=0.34, fs=9.5, mono_cols=(0, 1))


@need(1.75)
def v_sequences(s, x, y, w, h, ns, out):
    vals = [("str", ns["name"]), ("list", list(ns["name"])), ("tuple", ns["point"])]
    rows = [["Type", "Value", "[0]", "[1:3]", "len", "Item assignment?"]]
    for nm, v in vals:
        try:
            t = v[:] if not isinstance(v, str) else v
            if isinstance(t, tuple):
                t[0] = 0
            elif isinstance(t, str):
                t[0] = "x"
            else:
                t[0] = "x"
            ok = "works"
        except TypeError:
            ok = "TypeError"
        rows.append([nm, repr(v) if nm != "list" else "['Z', 'o', ...]", repr(v[0]), repr(v[1:3]), str(len(v)), ok])
    cf = {(i, 5): (C["greenLight"] if r[5] == "works" else C["redLight"]) for i, r in enumerate(rows) if i}
    table(s, x, y, w * 0.78, rows, [0.8, 2.2, 0.7, 1.7, 0.6, 1.5], rowh=0.34, mono_cols=(1, 2, 3), cell_fill=cf, align_cols={4: PP_ALIGN.CENTER})
    ls = lines_of(out)
    chip(s, x, y + 1.45, w * 0.78, 0.3, "last print: " + ls[-1], "amber", fs=10, mono=True)


# ------------------------------------------------------------------ part 2
def replay(code, var, skip=("print",)):
    """Run the statements of a code text one by one in a fresh namespace; give (source, repr of var) after each statement that is not a print."""
    tree = ast.parse(code)
    ns = {}
    rows = []
    for st in tree.body:
        seg = ast.get_source_segment(code, st)
        if isinstance(st, ast.Expr) and isinstance(st.value, ast.Call) and getattr(st.value.func, "id", "") in skip:
            continue
        exec(compile(ast.Module([st], []), "<replay>", "exec"), ns)
        rows.append((seg, repr(ns[var])))
    return rows


@need(3.5)
def v_change(s, x, y, w, h, ns, out):
    code = CODE["change"]
    chip(s, x, y, w, 0.3, "pop() handed back: " + lines_of(out)[1].split()[0], "amber", fs=9.5)
    rows = [["Statement", "spam afterwards"]]
    for seg, val in replay(code, "spam"):
        rows.append([seg, val])
    table(s, x, y + 0.38, w, rows, [1.55, 2.25], rowh=0.4, fs=9, mono_cols=(0, 1))


@need(3.4)
def v_augmented(s, x, y, w, h, ns, out):
    a = [1, 2, 3]
    steps = []
    b = a + ["A", "B"]
    steps.append(("spam + ['A', 'B']", b is a))
    c = ["X", "Y"] * 3
    steps.append(("['X', 'Y'] * 3", c is a))
    i0 = id(a)
    a += [4]
    steps.append(("spam += [4]", id(a) == i0))
    a *= 2
    steps.append(("spam *= 2", id(a) == i0))
    a.extend(["A", "B"])
    steps.append(("spam.extend(['A', 'B'])", id(a) == i0))
    rows = [["Statement", "Same list as spam?"]] + [[t, "yes, spam changed" if same else "no, a new list"] for t, same in steps]
    cf = {(i + 1, 1): (C["amberLight"] if same else C["greenLight"]) for i, (t, same) in enumerate(steps)}
    table(s, x, y, w, rows, [2.2, 1.6], rowh=0.42, fs=9.5, mono_cols=(0,), cell_fill=cf)
    ls = lines_of(out)
    tb(s, x, y + 0.42 * len(rows) + 0.08, w, 0.4, "spam after += and *=: " + ls[2], 9.5, C["ink"], margin=(0, 0))
    tb(s, x, y + 0.42 * len(rows) + 0.5, w, 0.5, "after extend: " + ls[3], 9.5, C["ink"], margin=(0, 0))


@need(3.4)
def v_searching(s, x, y, w, h, ns, out):
    pets = ns["pets"]
    cw = min(0.95, w / len(pets))
    hits = {i: "teal" for i, p in enumerate(pets) if p == "Pooka"}
    strip(s, x, y + 0.5, pets, cw, 0.46, hits, fs=9.5, neg=False)
    label(s, x, y, w, "the two Pooka cells are highlighted", 9.5)
    ls = lines_of(out)
    rows = [["Question", "Printed"], ["in, not in", ls[0]], ["index('Pooka')", ls[1]], ["index('Cat')", ls[2]], ["count('Pooka')", ls[3]]]
    table(s, x, y + 1.05, w, rows, [1.5, 2.3], rowh=0.42, fs=9.5, mono_cols=(0, 1))


@need(1.55)
def v_shortcircuit(s, x, y, w, h, ns, out):
    env = {"spam": []}
    items = [("spam and spam[0] == 'cat'", "spam is empty, so false: spam[0] is never tried"), ("bool(spam)", "an empty list counts as false"),
             ("'' or 'Guest'", "or returns the first true value"), ("0 or [] or 'last'", "no true value, so the last operand"), ("1 and 2 and 3", "all true, so the last operand")]
    rows = [["Expression", "Result", "Why"]] + [[e, repr(eval(e, env)), why] for e, why in items]
    table(s, x, y, w, rows, [2.5, 1.0, 4.6], rowh=0.25, fs=9.5, mono_cols=(0, 1))


@need(3.5)
def v_sort(s, x, y, w, h, ns, out):
    nums = [2, 5, 3.14, 1, -7]
    letters = ["a", "z", "A", "Z"]
    rows = [["Call", "Result"], ["nums at the start", repr(nums)]]
    n2 = list(nums)
    n2.sort()
    rows.append(["nums.sort()", repr(n2)])
    n2.sort(reverse=True)
    rows.append(["nums.sort(reverse=True)", repr(n2)])
    rows.append(["sorted(letters)", repr(sorted(letters))])
    rows.append(["sorted(letters, key=str.lower)", repr(sorted(letters, key=str.lower))])
    rows.append(["print(nums.sort())", repr(n2.sort())])
    cf = {(6, 1): C["redLight"], (2, 1): C["greenLight"], (3, 1): C["greenLight"]}
    table(s, x, y, w, rows, [1.7, 2.1], rowh=0.42, fs=9, mono_cols=(0, 1), cell_fill=cf)
    tb(s, x, y + 0.42 * len(rows) + 0.08, w, 0.3, "green: the list itself changed", 9.5, C["muted"], italic=True, margin=(0, 0))


@need(1.7)
def v_magic8(s, x, y, w, h, ns, out):
    msgs = ns["messages"]
    random.seed(1946)
    picks = [random.randint(0, len(msgs) - 1) for _ in range(3)]
    ls = lines_of(out)
    assert [msgs[p] for p in picks] == ls
    rows = [["Round", "random index", "messages[index]"]] + [[str(i + 1), str(p), msgs[p]] for i, p in enumerate(picks)]
    table(s, x, y, w * 0.5, rows, [0.7, 1.2, 2.6], rowh=0.36, mono_cols=(1,), align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})
    strip(s, x + w * 0.52, y + 0.5, [m.split()[0] + "..." for m in msgs], 1.0, 0.46, {p: "amber" for p in picks}, fs=9.5, neg=False)
    label(s, x + w * 0.52, y + 0.05, 4.2, "the list; highlighted cells were picked", 9.5)


# ------------------------------------------------------------------ part 3
@need(1.6)
def v_loops(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    a = [l.split(" ", 1) for l in ls[:4]]
    b = [l.split(" ") for l in ls[4:]]
    table(s, x, y, w * 0.4, [["i", "supplies[i]"]] + a, [0.6, 2.3], rowh=0.3, mono_cols=(0, 1), align_cols={0: PP_ALIGN.CENTER})
    table(s, x + w * 0.45, y, w * 0.55, [["n", "s", "len(s)"]] + b, [0.6, 2.3, 1.0], rowh=0.3, mono_cols=(0, 1, 2), align_cols={0: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER})
    tb(s, x, y + 1.55, w * 0.4, 0.24, "range(len(...)): positions from 0", 9.5, C["muted"], italic=True, margin=(0, 0))
    tb(s, x + w * 0.45, y + 1.55, w * 0.55, 0.24, "enumerate(..., 1): numbers from 1", 9.5, C["muted"], italic=True, margin=(0, 0))


@need(3.5)
def v_removal(s, x, y, w, h, ns, out):
    items = ["a", "b", "c", "d"]
    rows = [["Pass", "x", "List after remove(x)"]]
    i = 0
    cf = {}
    while i < len(items):
        xx = items[i]
        items.remove(xx)
        rows.append([str(i + 1), xx, repr(items)])
        i += 1
    rows.append(["", "", ""])
    rows[-1] = ["end", "-", "%s left behind" % repr(items)]
    cf[(len(rows) - 1, 2)] = C["redLight"]
    table(s, x, y, w, rows, [0.7, 0.5, 2.6], rowh=0.34, fs=10, mono_cols=(1, 2), cell_fill=cf, align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})
    ls = lines_of(out)
    label(s, x, y + 0.34 * len(rows) + 0.1, w, "the safe ways, as printed:", 9.5)
    chip(s, x, y + 0.34 * len(rows) + 0.38, w * 0.48, 0.34, "new list: " + ls[1], "green", fs=10, mono=True)
    chip(s, x + w * 0.52, y + 0.34 * len(rows) + 0.38, w * 0.48, 0.34, "clear(): " + ls[2], "green", fs=10, mono=True)


@need(1.5)
def v_unpack(s, x, y, w, h, ns, out):
    groups = [("size, color, mood", [("size", ns["size"]), ("color", ns["color"]), ("mood", ns["mood"])]),
              ("first, *rest", [("first", ns["first"]), ("rest", ns["rest"])]),
              ("a, b = b, a", [("a", ns["a"]), ("b", ns["b"])])]
    gw = w / 3.0
    for g, (head, pairs) in enumerate(groups):
        gx = x + g * gw
        tb(s, gx, y, gw - 0.2, 0.24, head, 10, C["teal"], bold=True, margin=(0, 0))
        for r, (nm, val) in enumerate(pairs):
            yy = y + 0.3 + r * 0.42
            chip(s, gx, yy, 0.85, 0.32, nm, "teal", fs=10, mono=True)
            arrow(s, gx + 0.88, yy + 0.16, gx + 1.2, yy + 0.16, C["teal"], 1.5)
            chip(s, gx + 1.22, yy, gw - 1.5, 0.32, repr(val), "amber", fs=10, mono=True)


@need(1.7)
def v_comprehension(s, x, y, w, h, ns, out):
    sq = ns["squares"]
    chart(s, "col", x, y - 0.05, w * 0.5, max(h, 1.7), ["x=%d" % (i + 1) for i in range(len(sq))], [("x squared", sq)], fs=9, legend=False, gap=40, vmax=40, major=10)
    ls = lines_of(out)
    rows = [["Line", "Printed"], ["squares", ls[0]], ["evens", ls[1]], ["sum(squares)", ls[2]]]
    table(s, x + w * 0.54, y + 0.1, w * 0.46, rows, [1.3, 3.2], rowh=0.36, fs=10, mono_cols=(0, 1))


@need(1.55)
def v_input(s, x, y, w, h, ns, out):
    words = ns["line"].split()
    nums = ns["nums"]
    n = len(words)
    cw = 0.95
    tb(s, x, y, 1.3, 0.3, "the text", 10, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))
    chip(s, x + 1.35, y, cw * n - 0.1, 0.3, repr(ns["line"]), "amber", fs=10.5, mono=True)
    tb(s, x, y + 0.5, 1.3, 0.3, "line.split()", 10, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))
    tb(s, x, y + 1.0, 1.3, 0.3, "int(w) each", 10, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))
    for i, (wd, nm) in enumerate(zip(words, nums)):
        chip(s, x + 1.35 + i * cw, y + 0.5, cw - 0.1, 0.3, repr(wd), "amber", fs=10, mono=True)
        chip(s, x + 1.35 + i * cw, y + 1.0, cw - 0.1, 0.3, repr(nm).replace("'", ""), "green", fs=10, mono=True)
        arrow(s, x + 1.35 + i * cw + (cw - 0.1) / 2, y + 0.81, x + 1.35 + i * cw + (cw - 0.1) / 2, y + 0.99, C["teal"], 1.2)
    ls = lines_of(out)
    chip(s, x + 1.35 + n * cw + 0.1, y + 0.0, w - (1.35 + n * cw + 0.1), 0.3, "sum, max, len: " + ls[1], "teal", fs=9.5, mono=True)
    chip(s, x + 1.35 + n * cw + 0.1, y + 0.5, w - (1.35 + n * cw + 0.1), 0.3, "type of line: " + ls[2], "red", fs=9.5, mono=True)


# ------------------------------------------------------------------ part 4
def listbox(s, x, y, w, items, kind="teal"):
    bw = (w - 0.1) / len(items)
    rect(s, x, y, w, 0.5, C["card"], line=C["teal"], radius=0.1)
    for i, it in enumerate(items):
        label_shape(s, x + 0.07 + i * bw, y + 0.07, bw - 0.06, 0.36, repr(it), C["tealLight"] if kind == "teal" else C["amberLight"], C["ink"], size=10.5, line=C["line"], radius=0.1)


@need(1.55)
def v_alias(s, x, y, w, h, ns, out):
    lst = ns["spam"]
    listbox(s, x + 3.0, y + 0.45, 4.0, lst)
    chip(s, x, y + 0.2, 1.2, 0.36, "spam", "amber", fs=11, mono=True)
    chip(s, x, y + 0.75, 1.2, 0.36, "eggs", "amber", fs=11, mono=True)
    arrow(s, x + 1.25, y + 0.38, x + 2.95, y + 0.62, C["teal"], 1.8)
    arrow(s, x + 1.25, y + 0.93, x + 2.95, y + 0.82, C["teal"], 1.8)
    tb(s, x + 3.0, y + 1.05, 4.0, 0.24, "one list in memory; two name tags", 9.5, C["muted"], italic=True, margin=(0, 0))
    ls = lines_of(out)
    chip(s, x + 7.2, y + 0.45, w - 7.2, 0.5, "eggs is spam: " + ls[1].split()[0], "green", fs=10, mono=True)


@need(1.55)
def v_argument(s, x, y, w, h, ns, out):
    lst = ns["nums"]
    listbox(s, x + 3.4, y + 0.45, 3.6, lst)
    for i, nm in enumerate(["nums (caller)", "items (parameter)", "result"]):
        chip(s, x, y + i * 0.5, 1.9, 0.36, nm, "amber", fs=10, mono=True)
        arrow(s, x + 1.95, y + 0.18 + i * 0.5, x + 3.35, y + 0.62 + (0 if i == 1 else (i - 1) * 0.1), C["teal"], 1.6)
    ls = lines_of(out)
    chip(s, x + 7.2, y + 0.45, w - 7.2, 0.5, "result is nums: " + ls[0].split()[-1], "green", fs=10, mono=True)


@need(3.4)
def v_copies(s, x, y, w, h, ns, out):
    g = [[1, 2], [3, 4]]
    sh, dp = copy.copy(g), copy.deepcopy(g)
    g[0][0] = 99
    rows = [["Question", "shallow", "deep"],
            ["grid[0][0] is now 99; copy [0][0]", repr(sh[0][0]), repr(dp[0][0])],
            ["inner list shared with grid?", "yes" if sh[0] is g[0] else "no", "yes" if dp[0] is g[0] else "no"]]
    cf = {(2, 1): C["amberLight"], (2, 2): C["greenLight"], (1, 1): C["amberLight"], (1, 2): C["greenLight"]}
    table(s, x, y, w, rows, [2.0, 0.9, 0.9], rowh=0.5, fs=9.5, cell_fill=cf, align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER})
    board = ns["board"]
    label(s, x, y + 1.7, w, "the trap: board = [[0] * 3] * 2, then board[0][0] = 9", 9.5)
    for r in range(2):
        for c in range(3):
            label_shape(s, x + c * 0.5, y + 2.0 + r * 0.42, 0.46, 0.38, repr(board[r][c]), C["redLight"] if board[r][c] else C["card"], C["ink"], size=10.5, line=C["line"], radius=0.1)
    tb(s, x + 1.7, y + 2.0, w - 1.7, 0.8, "board[0] is board[1]: %s. One inner list stands in both rows." % (board[0] is board[1]), 10, C["ink"], margin=(0, 0))


# ------------------------------------------------------------------ part 5
@need(1.7)
def v_random(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    rows = [["Call", "Printed"], ["random.choice(pets)", ls[0]], ["pets after shuffle", ls[1]], ["print(random.shuffle(pets))", ls[2]], ["random.randint(1, 6)", ls[3]]]
    table(s, x, y, w * 0.52, rows, [2.0, 2.2], rowh=0.34, fs=9.5, mono_cols=(0, 1))
    rng = random.Random(5)
    cnt = Counter(rng.randint(1, 6) for _ in range(6000))
    tb(s, x + w * 0.56, y - 0.02, w * 0.44, 0.22, "6000 more throws of randint(1, 6), seed 5", 9.5, C["muted"], italic=True, margin=(0, 0))
    chart(s, "col", x + w * 0.56, y + 0.18, w * 0.44, max(h - 0.2, 1.5), [str(k) for k in range(1, 7)], [("throws", [cnt[k] for k in range(1, 7)])], fs=9, legend=False, gap=40, vmax=1400, major=400)


@need(3.5)
def v_fairshuffle(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    orders = ast.literal_eval(ls[0])
    diffs = ast.literal_eval(ls[1])
    tb(s, x, y, w, 0.4, "count minus 1000 for each of the six orders", 10, C["muted"], italic=True, margin=(0, 0))
    chart(s, "col", x, y + 0.3, w, 2.5, orders, [("count minus 1000", diffs)], fs=9, legend=False, gap=40, vmax=60, major=20)
    chip(s, x, y + 2.9, w, 0.4, "all six orders appear; the largest distance from 1000 is %d" % max(abs(d) for d in diffs), "green", fs=9.5)


@need(3.5)
def v_matrix(s, x, y, w, h, ns, out):
    rows = out.split("\n")[:5]
    cw = min(0.23, (w - 0.1) / 16)
    label(s, x, y, w, "what the run printed, one cell per character", 9.5)
    for r, ln in enumerate(rows):
        ln = ln.ljust(16)
        for c, ch in enumerate(ln):
            label_shape(s, x + c * cw, y + 0.3 + r * cw, cw - 0.02, cw - 0.02, ch.strip(), C["greenLight"] if ch.strip() else C["card"], C["ink"], size=8 if cw < 0.22 else 9, line=C["line"], radius=0.08)
    yy = y + 0.3 + 5 * cw + 0.2
    arrow(s, x + 8 * cw, y + 0.3 + 5 * cw + 0.02, x + 8 * cw, yy - 0.02, C["teal"], 1.4)
    label(s, x, yy, w, "ctr: the 16 counters after the last row", 9.5)
    for c, v in enumerate(ns["ctr"]):
        label_shape(s, x + c * cw, yy + 0.28, cw - 0.02, cw - 0.02, str(v), C["amberLight"] if v else C["card"], C["ink"], size=8 if cw < 0.22 else 9, line=C["line"], radius=0.08)
    n_dig = sum(1 for r in rows for ch in r if ch.strip())
    chip(s, x, yy + 0.7, w, 0.34, "%d digits printed in 5 rows of 16 columns" % n_dig, "teal", fs=9.5)


@need(1.45)
def v_commacode(s, x, y, w, h, ns, out):
    f = ns["list_to_text"]
    rows = [["Test list", "list_to_text gives", "Rule used"]]
    for t in ns["tests"]:
        rule = "and between the two" if len(t) == 2 else ("the item alone" if len(t) == 1 else ("empty text" if not t else "commas, then ', and '"))
        rows.append([repr(t), repr(f(t)), rule])
    table(s, x, y, w, rows, [2.4, 3.2, 3.0], rowh=0.3, mono_cols=(0, 1))


@need(3.4)
def v_coinstreaks(s, x, y, w, h, ns, out):
    st = ns["streaks"]
    tb(s, x, y, w, 0.4, "10,000 experiments of 100 flips each", 10, C["muted"], italic=True, margin=(0, 0))
    chart(s, "col", x, y + 0.3, w, 2.5, ["with a streak of 6", "without a streak"], [("experiments", [st, 10000 - st])], fs=9.5, legend=False, gap=60, vmax=10000, major=2500, number_format="#,##0")
    chip(s, x, y + 2.9, w, 0.4, lines_of(out)[0], "teal", fs=10, mono=True)


CODE = {}
VISUALS = {"indexes": v_indexes, "nested": v_nested, "slices": v_slices, "dijkstra": v_dijkstra, "sequences": v_sequences, "change": v_change,
           "augmented": v_augmented, "searching": v_searching, "shortcircuit": v_shortcircuit, "sort": v_sort, "magic8": v_magic8, "loops": v_loops,
           "removal": v_removal, "unpack": v_unpack, "comprehension": v_comprehension, "input": v_input, "alias": v_alias, "argument": v_argument,
           "copies": v_copies, "random": v_random, "fairshuffle": v_fairshuffle, "matrix": v_matrix, "commacode": v_commacode, "coinstreaks": v_coinstreaks}
