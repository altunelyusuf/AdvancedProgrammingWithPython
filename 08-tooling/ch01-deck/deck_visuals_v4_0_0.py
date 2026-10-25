"""Chapter 1 deck visuals, version 4.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from a run of the example's own expressions (the namespace `ns`
and the printed text `out` that deck_build_v4_0_0.py passes in, or the same expression evaluated here); nothing is typed in by
hand except the plain-language names of columns and the shapes of the diagrams.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "4.0.0"
import contextlib
import io
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v4_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def vis(s):
    return {" ": "·", "\n": "⏎", "\t": "⇥", "\r": "␍"}.get(s, s)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO if mono else None, line=C["line"], radius=0.15)


def strip(s, x, y, text, cw, ch, fills=None, fs=12, idx=True, label_fs=8):
    """A row of character cells with the index below; fills maps index -> kind."""
    fills = fills or {}
    for i, c in enumerate(text):
        f, col = {"teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]), "green": (C["greenLight"], C["ink"]),
                  "red": (C["redLight"], C["ink"]), "grey": (C["grey"], C["muted"])}.get(fills.get(i), (C["card"], C["ink"]))
        label_shape(s, x + i * cw, y, cw - 0.025, ch, vis(c), f, col, size=fs, font=MONO, line=C["line"], radius=0.1)
        if idx:
            tb(s, x + i * cw, y + ch, cw - 0.025, 0.18, str(i), label_fs, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def ev(expr):
    """value of an expression, or 'ErrorName: message' when it raises"""
    try:
        return eval(expr, {})
    except Exception as e:
        return "%s: %s" % (type(e).__name__, e)


def typ(v):
    return type(v).__name__


def say(f):
    """the text a print call writes"""
    b = io.StringIO()
    with contextlib.redirect_stdout(b):
        f()
    return b.getvalue()


# ------------------------------------------------------------------ part 1
@need(1.5)
def v_shell(s, x, y, w, h, ns, out):
    exprs = ["2 + 2", "'Py' + 'thon'", "2 + 3 * 6", "3 * (2 + 4)"]
    rows = [["Expression", "Value", "Type"]] + [[e, repr(ev(e)), typ(ev(e))] for e in exprs]
    table(s, x, y, w * 0.5, rows, [2.0, 1.4, 0.9], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2))
    steps = [("Read", "you type", "teal"), ("Evaluate", "Python computes", "amber"), ("Print", "value appears", "green"), ("Loop", "next prompt", "grey")]
    xs = x + w * 0.54
    cw = (w * 0.46 - 0.6) / 4
    for i, (a, b, k) in enumerate(steps):
        xx = xs + i * (cw + 0.2)
        chip(s, xx, y + 0.2, cw, 0.42, a, k, fs=10, mono=False)
        tb(s, xx - 0.1, y + 0.68, cw + 0.2, 0.4, b, 9.5, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
        if i < 3:
            arrow(s, xx + cw + 0.01, y + 0.41, xx + cw + 0.19, y + 0.41, C["muted"], 1.2)
    tb(s, xs, y + 1.15, w * 0.46, 0.3, "the shell repeats these four steps for every line", 10, C["muted"], italic=True)


@need(1.6)
def v_types(s, x, y, w, h, ns, out):
    vals = ["7", "3.5", "'Alice'", "7 + 1", "7 + 1.0"]
    rows = [["Value", "Data type", "What type() printed"]] + [[v, typ(ev(v)), "<class '%s'>" % typ(ev(v))] for v in vals]
    cf = {(i + 1, 1): {"int": C["tealLight"], "float": C["amberLight"], "str": C["greenLight"]}[typ(ev(v))] for i, v in enumerate(vals)}
    table(s, x, y, w * 0.58, rows, [1.4, 1.2, 2.3], rowh=min(0.28, h / len(rows)), mono_cols=(0, 1, 2), cell_fill=cf)
    xs = x + w * 0.64
    for k, (a, b, r) in enumerate([("int", "int", "int"), ("int", "float", "float")]):
        yy = y + 0.25 + k * 0.7
        chip(s, xs, yy, 0.6, 0.36, a, "teal" if a == "int" else "amber", fs=10)
        tb(s, xs + 0.62, yy, 0.25, 0.36, "+", 12, C["ink"], bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))
        chip(s, xs + 0.9, yy, 0.6, 0.36, b, "teal" if b == "int" else "amber", fs=10)
        arrow(s, xs + 1.55, yy + 0.18, xs + 1.95, yy + 0.18, C["muted"], 1.3)
        chip(s, xs + 2.0, yy, 0.7, 0.36, r, "teal" if r == "int" else "amber", fs=10)
    tb(s, xs, y + 1.65, 2.8, 0.3, "one float makes the result a float", 10, C["muted"], italic=True) if h > 2.0 else None


@need(1.6)
def v_ints(s, x, y, w, h, ns, out):
    exprs = ["7 + 1", "int('42') + 1", "int(4.7)", "2 ** 100"]
    vals = [ev(e) for e in exprs]
    chart(s, "col", x, y, w * 0.46, h, exprs, [("digits in the result", [len(str(v)) for v in vals])], fs=9, legend=False, gap=50, vmax=40, major=10)
    rows = [["Expression", "Result"]] + [[e, short(v, 22)] for e, v in zip(exprs, vals)]
    table(s, x + w * 0.5, y + 0.1, w * 0.5, rows, [1.8, 2.6], rowh=min(0.34, (h - 0.1) / len(rows)), mono_cols=(0, 1))
    tb(s, x + w * 0.5, y + 0.15 + 0.34 * len(rows), w * 0.5, 0.3, "the chart counts the digits of each result", 10, C["muted"], italic=True) if h > 2.1 else None


@need(1.6)
def v_floats(s, x, y, w, h, ns, out):
    exprs = ["0.1 + 0.2", "round(0.1 + 0.2, 2)", "0.1 + 0.2 == 0.3", "6 / 3", "4 * 3.75 - 1"]
    vals = [ev(e) for e in exprs]
    rows = [["Expression", "Result", "Type"]] + [[e, repr(v), typ(v)] for e, v in zip(exprs, vals)]
    cc = {(3, 1): C["coral"]}
    table(s, x, y, w * 0.6, rows, [2.3, 1.9, 0.9], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2), cell_color=cc)
    fl = [(e, v) for e, v in zip(exprs, vals) if isinstance(v, float)]
    chart(s, "col", x + w * 0.64, y, w * 0.36, h, ["0.1+0.2", "round", "6 / 3", "4*3.75-1"], [("digits after the point", [len(repr(v).split(".")[1]) for _, v in fl])],
          fs=9, legend=False, gap=50, vmax=20, major=5)


@need(1.7)
def v_strings(s, x, y, w, h, ns, out):
    t = "Hello, world!"
    cw = min(0.5, (w * 0.62) / len(t))
    tb(s, x, y, 5.0, 0.26, "len('Hello, world!') counts these cells", 10.5, C["teal"], bold=True)
    strip(s, x, y + 0.3, t, cw, 0.42, {i: ("grey" if c in ", !" else "teal") for i, c in enumerate(t)}, fs=13, idx=True)
    arrow(s, x + len(t) * cw + 0.05, y + 0.51, x + len(t) * cw + 0.4, y + 0.51, C["muted"], 1.3)
    chip(s, x + len(t) * cw + 0.45, y + 0.33, 0.9, 0.36, "len = %d" % len(t), "amber", fs=11)
    rows = [["Value", "Type", "Equal to the other?"], ["'7'", typ(ev("'7'")), repr(ev("'7' == 7"))], ["7", typ(7), repr(ev("'7' == 7"))]]
    table(s, x, y + 1.15, w * 0.6, rows, [1.2, 1.2, 2.4], rowh=0.3, mono_cols=(0, 1, 2), cell_color={(1, 2): C["coral"], (2, 2): C["coral"]})
    tb(s, x + w * 0.62, y + 1.15, w * 0.38, 0.9, "teal: letters, grey: comma, space and mark; all 13 count", 10, C["muted"], italic=True)


# ------------------------------------------------------------------ part 2
@need(1.9)
def v_ops(s, x, y, w, h, ns, out):
    ops = [("+", "add", "5 + 2"), ("-", "subtract", "5 - 2"), ("*", "multiply", "5 * 2"), ("/", "divide", "5 / 2"), ("//", "floor divide", "5 // 2"), ("%", "remainder", "5 % 2"), ("**", "power", "5 ** 2")]
    rows = [["Operator", "Name", "Expression", "Result"]] + [[o, n, e, repr(ev(e))] for o, n, e in ops]
    table(s, x, y, w * 0.62, rows, [0.9, 1.4, 1.3, 1.0], rowh=min(0.27, h / len(rows)), mono_cols=(0, 2, 3))
    chart(s, "bar", x + w * 0.65, y, w * 0.35, h, [o for o, _, _ in ops][::-1], [("result of 5 op 2", [float(ev(e)) for _, _, e in ops][::-1])], fs=9, legend=False, gap=40, vmax=30, major=10)


@need(1.8)
def v_prec(s, x, y, w, h, ns, out):
    exprs = ["2 + 3 * 6", "(2 + 3) * 6", "-3 ** 2", "(-3) ** 2", "8 / 2 * 3"]
    vals = [ev(e) for e in exprs]
    chart(s, "col", x, y, w * 0.58, h, exprs, [("value", [float(v) for v in vals])], fs=9, legend=False, gap=40, vmax=35, vmin=-10, major=10)
    rows = [["Order", "Operators"], ["1st", "**"], ["2nd", "*  /  //  %"], ["3rd", "+  -"], ["always first", "( )"]]
    table(s, x + w * 0.62, y + 0.1, w * 0.38, rows, [1.3, 2.0], rowh=min(0.34, (h - 0.1) / 5), mono_cols=(1,))
    tb(s, x + w * 0.62, y + 0.15 + 0.34 * 5, w * 0.38, 0.4, "equal rank: left to right", 10, C["muted"], italic=True) if h > 2.2 else None


@need(1.5)
def v_intdiv(s, x, y, w, h, ns, out):
    total, d = 23, 7
    q, r = total // d, total % d
    cw = min(0.4, (w - 0.1) / total)
    kinds = ["teal", "amber", "green"]
    for i in range(total):
        k = "red" if i >= q * d else kinds[(i // d) % 3]
        chip(s, x + i * cw, y + 0.38, cw - 0.04, 0.4, str(i + 1), k, fs=9, mono=True)
    for g in range(q):
        chip(s, x + g * d * cw, y, d * cw - 0.04, 0.3, "box %d of %d" % (g + 1, d), kinds[g % 3], fs=9.5, mono=False)
    chip(s, x + q * d * cw, y, r * cw - 0.04, 0.3, "left", "red", fs=9.5, mono=False)
    yy = y + 0.92
    chip(s, x, yy, 2.9, 0.34, "23 // 7 = %d  full boxes" % q, "teal", fs=10.5)
    arrow(s, x + 1.45, y + 0.8, x + 1.45, yy - 0.02, C["muted"], 1.2)
    chip(s, x + w - 2.9, yy, 2.9, 0.34, "23 %% 7 = %d  left over" % r, "red", fs=10.5)
    arrow(s, x + (q * d + r / 2.0) * cw, y + 0.8, x + w - 1.45, yy - 0.02, C["muted"], 1.2)
    rows = [["Expression", "Result"], ["-7 // 2", repr(ev("-7 // 2"))], ["23 / 7", short(repr(ev("23 / 7")), 18)]]
    table(s, x + 3.1, yy - 0.02, 2.9, rows, [0.9, 2.0], rowh=0.27, mono_cols=(0, 1))


@need(1.6)
def v_concat(s, x, y, w, h, ns, out):
    exprs = ["'Alice' + 'Bob'", "'Hello' + ' ' + 'world'", "'Alice' + 42", "'Alice' + str(42)"]
    vals = [ev(e) for e in exprs]
    rows = [["Expression", "Result"]] + [[e, short(repr(v), 44) if not (isinstance(v, str) and v.startswith("TypeError")) else short(v, 44)] for e, v in zip(exprs, vals)]
    cc = {(3, 1): C["coral"]}
    table(s, x, y, w * 0.68, rows, [2.4, 3.8], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1), cell_color=cc)
    xs = x + w * 0.72
    chip(s, xs, y + 0.1, 0.8, 0.34, "'Alice'", "teal", fs=9.5)
    tb(s, xs + 0.82, y + 0.1, 0.2, 0.34, "+", 12, C["ink"], bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))
    chip(s, xs + 1.05, y + 0.1, 0.7, 0.34, "'Bob'", "amber", fs=9.5)
    arrow(s, xs + 0.9, y + 0.48, xs + 0.9, y + 0.8, C["muted"], 1.3)
    chip(s, xs, y + 0.85, 1.75, 0.38, "'AliceBob'", "green", fs=10.5)
    tb(s, xs, y + 1.3, 2.4, 0.3, "two strips glued, no gap", 10, C["muted"], italic=True)


@need(1.6)
def v_repl(s, x, y, w, h, ns, out):
    exprs = ["'Alice' * 3", "3 * 'ab'", "'ab' * 0", "'Alice' * 2.5"]
    vals = [ev(e) for e in exprs]
    rows = [["Expression", "Result"]] + [[e, short(repr(v), 40) if not str(v).startswith("TypeError") else short(v, 40)] for e, v in zip(exprs, vals)]
    table(s, x, y, w * 0.62, rows, [2.0, 3.7], rowh=min(0.32, h / len(rows)), mono_cols=(0, 1), cell_color={(4, 1): C["coral"]})
    good = [(e, v) for e, v in zip(exprs, vals) if not str(v).startswith("TypeError")]
    chart(s, "col", x + w * 0.66, y, w * 0.34, h, ["'Alice' * 3", "3 * 'ab'", "'ab' * 0"], [("characters in the result", [len(v) for _, v in good])], fs=9, legend=False, gap=50, vmax=20, major=5)


# ------------------------------------------------------------------ part 3
@need(1.7)
def v_var(s, x, y, w, h, ns, out):
    stages = [("spam = 42", "spam", "42", "teal"), ("spam = spam + 1", "spam", "43", "amber"), ("print(Spam)", "Spam", "no jar", "red")]
    cw = 2.5
    for i, (code, name, val, k) in enumerate(stages):
        xx = x + i * (cw + 0.85)
        tb(s, xx, y, cw, 0.28, code, 10.5, C["muted"], font=MONO, align=PP_ALIGN.CENTER)
        chip(s, xx, y + 0.4, 0.95, 0.4, name, "grey", fs=11)
        arrow(s, xx + 0.98, y + 0.6, xx + 1.28, y + 0.6, C["muted"], 1.3)
        chip(s, xx + 1.3, y + 0.35, 1.1, 0.5, val, k, fs=13)
        if i < 2:
            arrow(s, xx + cw + 0.03, y + 0.6, xx + cw + 0.78, y + 0.6, C["teal"], 1.6)
    tb(s, x, y + 1.0, w, 0.5, "the tag (the name) points at a value; assigning again moves the tag to a new value; Spam is a different tag with nothing behind it", 10.5, C["muted"], italic=True)
    rows = [["Step", "spam", "Result"], ["1", "42", "print shows 42"], ["2", "43", "print shows 43"], ["3", "(no name Spam)", "NameError"]]
    table(s, x, y + 1.5, w * 0.6, rows, [0.7, 1.9, 2.2], rowh=0.27, mono_cols=(1, 2), cell_color={(3, 2): C["coral"]}) if h > 2.0 else None


@need(1.6)
def v_print(s, x, y, w, h, ns, out):
    calls = [("print('Hello,', 'world!')", lambda: print("Hello,", "world!")),
             ("print('Hello,', 'world!', sep='-', end=' <end>\\n')", lambda: print("Hello,", "world!", sep="-", end=" <end>\n")),
             ("print()", lambda: print()),
             ("print('the line above is empty')", lambda: print("the line above is empty"))]
    rows = [["Call", "Text written (· = space, ⏎ = end of line)"]] + [[c, "".join(vis(ch) for ch in say(f))] for c, f in calls]
    rh = min(0.25, (h - 0.5) / len(rows))
    table(s, x, y, w, rows, [4.6, 4.6], rowh=rh, fs=10, mono_cols=(0, 1))
    yy = y + rh * len(rows) + 0.2
    for k, (sep, end, lab) in enumerate([("·", "⏎", "default"), ("-", "·<end>⏎", "sep='-', end=' <end>\\n'")]):
        xx = x + k * 4.7
        chip(s, xx, yy, 0.85, 0.32, "Hello,", "teal", fs=10)
        chip(s, xx + 0.9, yy, 0.45, 0.32, sep, "amber", fs=10)
        chip(s, xx + 1.4, yy, 0.85, 0.32, "world!", "teal", fs=10)
        chip(s, xx + 2.3, yy, 0.9, 0.32, end, "green", fs=10)
        tb(s, xx + 3.3, yy, 1.3, 0.34, "amber: separator, green: ending", 8.5, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, margin=(0, 0))


@need(1.9)
def v_conv(s, x, y, w, h, ns, out):
    exprs = ["str(29)", "int('42')", "float('3.5')", "int(4.7)", "len('hello')", "len(str(12345))"]
    vals = [ev(e) for e in exprs]
    rows = [["Call", "Result", "Type of the result"]] + [[e, repr(v), typ(v)] for e, v in zip(exprs, vals)]
    table(s, x, y, w * 0.6, rows, [2.1, 1.1, 1.7], rowh=min(0.27, h / len(rows)), mono_cols=(0, 1, 2))
    xs = x + w * 0.65
    for k, (a, f, b) in enumerate([("'42'", "int()", "42"), ("29", "str()", "'29'"), ("3", "float()", "3.0")]):
        yy = y + 0.1 + k * 0.62
        chip(s, xs, yy, 0.65, 0.36, a, "grey", fs=10)
        arrow(s, xs + 0.7, yy + 0.18, xs + 0.95, yy + 0.18, C["muted"], 1.2)
        chip(s, xs + 1.0, yy, 0.8, 0.36, f, "teal", fs=10)
        arrow(s, xs + 1.85, yy + 0.18, xs + 2.1, yy + 0.18, C["muted"], 1.2)
        chip(s, xs + 2.15, yy, 0.75, 0.36, b, "amber", fs=10)


@need(1.4)
def v_errors(s, x, y, w, h, ns, out):
    cases = [("int('4.2')", "wrong content", "ValueError"), ("len(12345)", "wrong type", "TypeError")]
    rows = [["Call", "Error", "What Python said"]]
    for c, _, _ in cases:
        m = ev(c)
        rows.append([c, m.split(":")[0], short(m.split(": ", 1)[1], 52)])
    table(s, x, y, w, rows, [1.7, 1.3, 6.2], rowh=0.36, mono_cols=(0, 1, 2), cell_color={(1, 1): C["coral"], (2, 1): C["coral"]})
    yy = y + 1.25
    for k, (c, why, name) in enumerate(cases):
        xx = x + k * 4.65
        chip(s, xx, yy, 1.3, 0.36, c, "grey", fs=10)
        arrow(s, xx + 1.33, yy + 0.18, xx + 1.58, yy + 0.18, C["muted"], 1.2)
        chip(s, xx + 1.6, yy, 1.15, 0.36, why, "amber", fs=10, mono=False)
        arrow(s, xx + 2.78, yy + 0.18, xx + 3.03, yy + 0.18, C["muted"], 1.2)
        chip(s, xx + 3.05, yy, 1.0, 0.36, name, "red", fs=10)


@need(1.6)
def v_input(s, x, y, w, h, ns, out):
    steps = [("person types", "20", "grey"), ("input()", "returns", "teal"), ("a string", "'20'", "amber"), ("int()", "converts", "teal"), ("a number", "20", "green")]
    cw = 1.45
    for i, (a, b, k) in enumerate(steps):
        xx = x + i * (cw + 0.5)
        chip(s, xx, y, cw, 0.42, a, k, fs=10.5, mono=False)
        tb(s, xx, y + 0.45, cw, 0.28, b, 11, C["ink"], font=MONO, align=PP_ALIGN.CENTER, margin=(0, 0))
        if i < 4:
            arrow(s, xx + cw + 0.04, y + 0.21, xx + cw + 0.46, y + 0.21, C["muted"], 1.4)
    typed = "20"
    exprs = ["typed + '1'", "int(typed) + 1"]
    rows = [["Expression", "Result", "Type"]] + [[e, repr(eval(e, {"typed": typed})), typ(eval(e, {"typed": typed}))] for e in exprs]
    table(s, x, y + 0.95, w * 0.62, rows, [2.4, 1.4, 1.2], rowh=0.3, mono_cols=(0, 1, 2))
    tb(s, x + w * 0.66, y + 0.95, w * 0.34, 0.9, "text plus text glues; number plus number adds", 10.5, C["muted"], italic=True)


@need(1.6)
def v_module(s, x, y, w, h, ns, out):
    import math
    chip(s, x, y + 0.1, 1.5, 0.4, "import math", "teal", fs=11)
    arrow(s, x + 1.55, y + 0.3, x + 2.0, y + 0.3, C["muted"], 1.4)
    chip(s, x + 2.05, y + 0.1, 1.6, 0.4, "math: module", "amber", fs=11)
    for k, (call, val) in enumerate([("math.sqrt(16)", repr(math.sqrt(16))), ("math.pi", repr(math.pi))]):
        yy = y + 0.1 + k * 0.62 - (0.0 if k == 0 else 0.0)
        xs = x + 4.0
        arrow(s, x + 3.7, y + 0.3, xs - 0.05, yy + 0.2, C["muted"], 1.2)
        chip(s, xs, yy, 1.6, 0.4, call, "plain", fs=10.5)
        arrow(s, xs + 1.65, yy + 0.2, xs + 2.05, yy + 0.2, C["muted"], 1.2)
        chip(s, xs + 2.1, yy, 2.2, 0.4, val, "green", fs=10.5)
    rows = [["Expression", "Result", "Type"], ["type(math).__name__", repr(type(math).__name__), "str"], ["math.sqrt(16)", repr(math.sqrt(16)), typ(math.sqrt(16))], ["math.pi", repr(math.pi), typ(math.pi)]]
    table(s, x, y + 1.35, w * 0.7, rows, [2.4, 2.3, 1.0], rowh=0.27, mono_cols=(0, 1, 2)) if h > 1.9 else None


# ------------------------------------------------------------------ part 4
@need(1.0)
def v_first(s, x, y, w, h, ns, out):
    src = [l for l in __import__("examples_v4_0_0").code_lines(__import__("examples_v4_0_0").BY_ID["first"])]
    env = {}
    rows = [["Line", "What Python does"]]
    cf = {}
    for i, l in enumerate(src, 1):
        b = io.StringIO()
        with contextlib.redirect_stdout(b):
            exec(l, env)
        o = b.getvalue().rstrip("\n")
        if o:
            rows.append([str(i), "shows: " + short(o, 30)])
            cf[(len(rows) - 1, 1)] = C["greenLight"]
        else:
            name = l.split("=")[0].strip()
            rows.append([str(i), "stores %s in %s" % (repr(env[name]), name)])
            cf[(len(rows) - 1, 1)] = C["amberLight"]
    table(s, x, y, w, rows, [0.5, 3.0], rowh=min(0.42, h / len(rows)), fs=10, mono_cols=(), cell_fill=cf, align_cols={0: PP_ALIGN.CENTER})


@need(1.4)
def v_dissect(s, x, y, w, h, ns, out):
    name, age = ns["name"], ns["age"]
    parts = [("'Hello, '", "teal", 1.05), ("name", "amber", 0.6), ("'! You are '", "teal", 1.25), ("str(age)", "amber", 0.9), ("'.'", "teal", 0.4)]
    xx = x
    tb(s, x - 0.02, y - 0.03, 1.0, 0.24, "join with +", 9.5, C["muted"], italic=True)
    for t, k, ww in parts:
        chip(s, xx, y + 0.2, ww, 0.32, t, k, fs=10)
        xx += ww + 0.1
    arrow(s, x + 2.4, y + 0.56, x + 2.4, y + 0.82, C["muted"], 1.3)
    res = "Hello, %s! You are %s." % (name, age)
    chip(s, x, y + 0.86, 4.0, 0.34, res, "green", fs=10.5)
    xs = x + 5.0
    tb(s, xs - 0.02, y - 0.03, 2.5, 0.24, "fill slots with an f-string", 9.5, C["muted"], italic=True)
    fparts = [("f'Hello, ", "grey", 0.95), ("{name}", "amber", 0.7), ("! You are ", "grey", 0.95), ("{age}", "amber", 0.65), (".'", "grey", 0.35)]
    xx = xs
    for t, k, ww in fparts:
        chip(s, xx, y + 0.2, ww, 0.32, t, k, fs=9.5)
        xx += ww + 0.05
    arrow(s, xs + 1.8, y + 0.56, xs + 1.8, y + 0.82, C["muted"], 1.3)
    chip(s, xs, y + 0.86, 4.0, 0.34, res, "green", fs=10.5)
    tb(s, x, y + 1.27, w, 0.26, "the same sentence twice: the slots {name} and {age} need no str() and no plus signs", 10, C["muted"], italic=True) if h > 1.55 else None


@need(1.7)
def v_binary(s, x, y, w, h, ns, out):
    places = [128, 64, 32, 16, 8, 4, 2, 1]
    bits = format(5, "08b")
    cw = 0.46
    tb(s, x, y, 4.0, 0.24, "place value of each binary digit", 9.5, C["muted"], italic=True)
    for i, p in enumerate(places):
        tb(s, x + i * cw, y + 0.24, cw - 0.03, 0.22, str(p), 9, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
    strip(s, x, y + 0.48, bits, cw, 0.38, {i: ("amber" if b == "1" else "grey") for i, b in enumerate(bits)}, fs=13, idx=False)
    chip(s, x, y + 1.05, 3.6, 0.32, "00000101 = 4 + 1 = 5", "amber", fs=10.5)
    bits2 = format(255, "08b")
    chip(s, x, y + 1.45, 3.6, 0.32, "11111111 = 255, the biggest byte", "teal", fs=10.5) if h > 1.9 else None
    chart(s, "col", x + 4.1, y, w - 4.1, h, [str(p) for p in places], [("value of the place if its digit is 1", [p if b == "1" else 0 for p, b in zip(places, bits)])], fs=9, legend=False, gap=40, vmax=8, major=2)


VISUALS = {"shell": v_shell, "types": v_types, "ints": v_ints, "floats": v_floats, "strings": v_strings, "ops": v_ops, "prec": v_prec, "intdiv": v_intdiv,
           "concat": v_concat, "repl": v_repl, "var": v_var, "print": v_print, "conv": v_conv, "errors": v_errors, "input": v_input, "module": v_module, "first": v_first,
           "dissect": v_dissect, "binary": v_binary}
