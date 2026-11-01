"""Chapter 7 deck visuals, version 2.1.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from the run of the example (the namespace `ns` and the
printed text `out` that deck_build_v2_1_0.py passes in); nothing is typed in by hand except the plain-language names of the columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.1.0"
import ast
import os
import re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_1_0 import C, MONO, arrow, chart, label_shape, picture, table, tb, rect

ASSET = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "03-materials", "ch07", "assets"))


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True, bold=False):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"]),
                 "key": (C["teal"], "FFFFFF")}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, bold=bold, font=None, line=C["line"], radius=0.15)


def pairs(s, x, y, w, h, items, fs=10.5):
    """a drawn dictionary: a column of key chips, an arrow from each to its value chip"""
    n = len(items)
    gap = 0.06
    bh = min(0.4, (h - (n - 1) * gap) / n)
    kw = w * 0.38
    aw = 0.4
    for i, (k, v) in enumerate(items):
        yy = y + i * (bh + gap)
        chip(s, x, yy, kw, bh, str(k), "key", fs, bold=True)
        arrow(s, x + kw, yy + bh / 2, x + kw + aw, yy + bh / 2, C["teal"])
        chip(s, x + kw + aw, yy, w - kw - aw, bh, str(v), "plain", fs)


def flow(s, x, y, w, h, labels, hot=(), fs=11, mono=True):
    n = len(labels)
    gap = 0.3
    bw = (w - (n - 1) * gap) / n
    for i, lab in enumerate(labels):
        chip(s, x + i * (bw + gap), y, bw, h, lab, "amber" if i in hot else "teal", fs, mono=mono)
        if i < n - 1:
            arrow(s, x + i * (bw + gap) + bw, y + h / 2, x + (i + 1) * (bw + gap), y + h / 2, C["teal"])


def tbl(s, x, y, w, h, rows, colw, mono=(), bold=()):
    rh = min(0.36, h / len(rows))
    return table(s, x, y, w, rows, colw, rowh=rh, mono_cols=mono, bold_cols=bold)


def lines(out):
    return out.splitlines()


# ------------------------------------------------------------------ part 1
@need(1.1)
def v_dict_basics(s, x, y, w, h, ns, out):
    L = lines(out)
    pairs(s, x, y, 4.3, h, list(ns["my_cat"].items()), 11)
    tbl(s, x + 4.6, y, 4.6, h, [["Expression", "Printed"], ["my_cat['size']", L[0]], ["'My cat has ' + color", L[1]], ["len(my_cat)", L[2]]], [2.4, 2.2], mono=(0, 1))


@need(1.1)
def v_dict_vs_list(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Expression", "Printed", "Why"], ["spam == bacon", L[0], "the same items in a different order"], ["eggs == ham", L[1], "the same pairs, in any order"],
                        ["list(ham)", L[2], "the order of adding is still kept"]], [2, 3.4, 3.6], mono=(0, 1))


@need(1.2)
def v_insertion(s, x, y, w, h, ns, out):
    L = lines(out)
    a, b = ast.literal_eval(L[0]), ast.literal_eval(L[2])
    rh = (h - 0.12) / 2
    for r, (lab, keys, hot) in enumerate([("after the three assignments", a, ()), ("after del and adding again", b, (2,))]):
        yy = y + r * (rh + 0.12)
        tb(s, x, yy, 2.4, rh, lab, 11, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, name="row label")
        flow(s, x + 2.5, yy, 6.4, rh, keys, hot=hot, fs=12)


@need(1.1)
def v_hashable(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Key tried", "Allowed?", "Printed"], ["(1, 2)  a tuple", "yes", L[0]], ["[1, 2]  a list", "no, unhashable", L[1]], ["1, 1.0 and True", "yes, but one key", L[2]]],
        [3, 2.4, 5], mono=(2,))


# ------------------------------------------------------------------ part 2
@need(1.1)
def v_kvi(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Method", "Gives", "Printed"], ["spam.keys()", "the labels", L[0]], ["spam.values()", "the contents", L[1]], ["spam.items()", "both, as pairs", L[-1]]],
        [2, 2, 5], mono=(0, 2))


@need(1.4)
def v_exists(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Question", "Printed"], ["'cups' in picnic", L[0]], ["'eggs' not in picnic", L[1]], ["picnic.get('eggs', 0)", L[2]],
                        ["picnic.get('cups', 0)", L[3]], ["picnic['eggs']", L[4]]], [4, 4], mono=(0, 1))


@need(1.3)
def v_setdefault(s, x, y, w, h, ns, out):
    L = lines(out)
    d = ns["picnic"]
    chart(s, "col", x, y, 4.3, h, list(d), [("picnic", list(d.values()))], fs=10, legend=False, gap=50)
    tbl(s, x + 4.6, y, 4.6, min(h, 1.1), [["Call", "Printed", "What happened"], ["first", L[0], "key missing: 12 stored"], ["second", L[1], "key found: 99 unused"]], [1.2, 1.2, 3])


@need(1.4)
def v_change(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Line", "Printed"], ["spam.pop('color')", L[0]], ["print(spam)", L[1]], ["spam | {'name': 'Rex', 'legs': 4}", L[2]], ["print(spam) again", L[3]]], [4, 5], mono=(0, 1))


@need(1.5)
def v_views(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Name", "What it is", "Shows"], ["ks = stock.keys()", "a live view", L[0]], ["frozen = list(stock)", "a photograph", L[1]],
                        ["sorted(stock)", "a new sorted list", L[2]], ["reversed(stock)", "newest first", L[3]]], [3, 2.4, 4], mono=(0, 2))


# ------------------------------------------------------------------ part 3
@need(1.5)
def v_birthdays(s, x, y, w, h, ns, out):
    L = lines(out)
    tbl(s, x, y, w, h, [["Typed", "The program did", "Printed"], ["Alice", "found the key", L[0]], ["Eve, then Dec 5", "stored a new pair", L[1]], ["Eve", "found the new key", L[2]],
                        ["dictionary now", "%d pairs" % len(ns["birthdays"]), ", ".join(ns["birthdays"])]], [2, 2.4, 4.6])


@need(1.5)
def v_charcount(s, x, y, w, h, ns, out):
    L = lines(out)
    top = ast.literal_eval(L[0])
    tot, kinds = [int(t) for t in L[1].split()]
    chart(s, "col", x, y, 6.0, h, ["space" if k == " " else k for k, _ in top], [("count", [v for _, v in top])], fs=10, legend=False, gap=50)
    tbl(s, x + 6.3, y, 2.9, 0.9, [["Measure", "Value"], ["characters", tot], ["different ones", kinds]], [2, 1])


@need(1.5)
def v_counter(s, x, y, w, h, ns, out):
    L = lines(out)
    d = ast.literal_eval(L[3])
    chart(s, "col", x, y, 4.6, h, list(d), [("count", list(d.values()))], fs=10, legend=False, gap=50)
    tbl(s, x + 4.9, y, 4.3, min(h, 1.1), [["Expression", "Printed"], ["c.most_common(2)", L[0]], ["c['a'], c['z']", L[1]], ["sum(c.values())", L[2]]], [2.2, 2.4], mono=(0, 1))


@need(1.3)
def v_grouping(s, x, y, w, h, ns, out):
    L = lines(out)
    d = ast.literal_eval(L[0])
    pairs(s, x, y, 5.4, h, [(k, v) for k, v in d.items()], 11)
    tbl(s, x + 5.7, y, 3.5, 0.7, [["Is g2 == groups?", "Printed"], ["defaultdict result", L[1]]], [2.2, 1.2])


# ------------------------------------------------------------------ part 4
@need(1.5)
def v_board_model(s, x, y, w, h, ns, out):
    L = lines(out)
    pairs(s, x, y, 3.3, h, list(ns["board"].items()), 10)
    tbl(s, x + 3.6, y, 4.3, 0.9, [["Printed", "Meaning"], [L[0], "c6 occupied, a1 empty"], [L[1], "five keys, sorted"]], [2.6, 1.8], mono=(0,))
    picture(s, os.path.join(ASSET, "book_fig_000103.jpg"), x + 8.0, y - 0.05, 1.2, h + 0.02, "Figure 7-2 of the book: the chessboard of the model", "book figure 7-2")


@need(2.0)
def v_board_print(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["", "a", "b", "c", "d", "e", "f", "g", "h"]]
    for ln in L:
        t = ln.split()
        rows.append([t[0]] + ["" if c == ".." else c for c in t[1:]])
    cf = {}
    for i in range(1, 9):
        for j in range(1, 9):
            cf[(i, j)] = "B7A98F" if (j - 1 + (9 - i)) % 2 == 1 else "F0E6D2"
    table(s, x, y, 4.6, rows, [0.6] + [1] * 8, rowh=h / 9, cell_fill=cf, bold_cols=(0,), name="result table")
    pcs = sum(1 for r in rows[1:] for c in r[1:] if c)
    tbl(s, x + 4.9, y, 4.3, 1.2, [["Measure", "Value"], ["keys in the dictionary", pcs], ["squares drawn", 64], ["squares without a key", 64 - pcs]], [3, 1.2])


@need(1.4)
def v_moves(s, x, y, w, h, ns, out):
    L = lines(out)
    b, st = ast.literal_eval(L[1]), ast.literal_eval(L[2])
    flow(s, x, y, w, h * 0.6, ["START\n" + "  ".join(st), "board = copy.copy(START)\n" + "  ".join(st), "after the move\n" + "  ".join(b)], hot=(2,), fs=11)
    tb(s, x, y + h * 0.66, w, h * 0.3, "Printed report: " + L[0] + ".   START still holds " + " ".join(st) + ".", 11, C["teal"], bold=True, name="result note")


@need(0.75)
def v_validator(s, x, y, w, h, ns, out):
    m = re.match(r"(\[.*?\]) (\[.*?\]) (\w+)", lines(out)[0])
    bad, kings, ok = ast.literal_eval(m.group(1)), ast.literal_eval(m.group(2)), m.group(3) == "True"
    tbl(s, x, y, w, h, [["Rule of the game", "Looks at", "Found", "Verdict"], ["every key is a real square", "the keys", "bad squares: %s" % bad, "PASS" if not bad else "FAIL"],
                        ["one king of each colour", "the values", "kings: %s" % kings, "PASS" if ok else "FAIL"]], [3.2, 1.4, 3.2, 1.2])


@need(1.5)
def v_picnic(s, x, y, w, h, ns, out):
    L = lines(out)
    g = ns["guests"]
    items = []
    for d in g.values():
        for k in d:
            if k not in items:
                items.append(k)
    chart(s, "col", x, y, 5.6, h, items, [(n, [d.get(k, 0) for k in items]) for n, d in g.items()], fs=10, legend=True, gap=50)
    tbl(s, x + 5.9, y, 3.3, 1.0, [["Expression", "Printed"], ["total apples, cups", L[0]], ["Alice's pretzels", L[1]]], [2.4, 1])


@need(1.4)
def v_inventory(s, x, y, w, h, ns, out):
    L = lines(out)
    d = ns["stuff"]
    chart(s, "bar", x, y, 5.2, h, list(d), [("how many", list(d.values()))], fs=10, legend=False, gap=50)
    tbl(s, x + 5.5, y, 3.7, 0.7, [["Last line printed"], [L[-1]]], [1])


@need(1.5)
def v_loot(s, x, y, w, h, ns, out):
    L = lines(out)
    after = ast.literal_eval(L[0])
    before = {k: v - ns["loot"].count(k) for k, v in after.items() if v - ns["loot"].count(k) > 0}
    cats = list(after)
    chart(s, "col", x, y, 6.0, h, cats, [("before", [before.get(k, 0) for k in cats]), ("after", [after[k] for k in cats])], fs=10, legend=True, gap=50)
    tbl(s, x + 6.3, y, 2.9, 0.9, [["Measure", "Value"], ["items before", sum(before.values())], ["items after", L[1]]], [2, 1])


# ------------------------------------------------------------------ part 5
@need(1.5)
def v_copies(s, x, y, w, h, ns, out):
    L = lines(out)
    a, sh, dp = L[0].split()
    is_alias, is_shallow = L[1].split()
    inner = L[2] == "True"
    tbl(s, x, y, w, h, [["Name", "New outer dictionary?", "Shares the inner one?", "Apples after the change"],
                        ["alias", "no, same object" if is_alias == "True" else "yes", "yes", a],
                        ["shallow copy", "yes" if is_shallow == "False" else "no", "yes" if inner else "no", sh],
                        ["deep copy", "yes", "no", dp]], [2, 3, 3, 3])


@need(1.3)
def v_json(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y, w, h * 0.62, ["dictionary\ncat", "text (JSON)\n" + L[0], "equal again?\n" + L[1]], hot=(1,), fs=10.5)
    tb(s, x, y + h * 0.68, w, h * 0.3, "pprint printed: " + L[2].strip() + " " + L[3].strip() + " " + " ".join(l.strip() for l in L[4:]), 11, C["teal"], bold=True, name="result note")


@need(1.2)
def v_typed(s, x, y, w, h, ns, out):
    L = lines(out)
    tp, age = L[0].split()
    tbl(s, x, y, w, h, [["Tool", "At run time", "Who enforces it"], ["TypedDict Cat", "type(c).__name__ is '%s', age %s" % (tp, age), "a type checker, not Python"],
                        ["MappingProxyType", "age %s, length %s: read-only" % tuple(L[1].split()), "Python itself: item assignment fails"]], [2.4, 4.2, 3.6])


@need(1.2)
def v_match(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y, w, h * 0.65, ["cat\n{'name': 'Zophie', 'age': 8}", "case 1 fits\nname, age and a > 5", L[0]], hot=(2,), fs=10.5)
    tb(s, x, y + h * 0.7, w, h * 0.28, "case 2 is never tried: the first fitting case wins.", 11, C["teal"], bold=True, name="result note")


VISUALS = {"dict_basics": v_dict_basics, "dict_vs_list": v_dict_vs_list, "insertion": v_insertion, "hashable": v_hashable, "kvi": v_kvi, "exists": v_exists,
           "setdefault": v_setdefault, "change": v_change, "views": v_views, "birthdays": v_birthdays, "charcount": v_charcount, "counter": v_counter,
           "grouping": v_grouping, "board_model": v_board_model, "board_print": v_board_print, "moves": v_moves, "validator": v_validator, "picnic": v_picnic,
           "inventory": v_inventory, "loot": v_loot, "copies": v_copies, "json": v_json, "typed": v_typed, "match": v_match}
