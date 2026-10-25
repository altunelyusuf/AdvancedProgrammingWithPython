"""Chapter 4 deck visuals, version 3.1.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, name and value shown is taken from a run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v3_1_0.py passes in, or the same code re-run here in a fresh namespace); nothing is typed in
by hand except the plain-language names of columns and boxes.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants.
deck_build sets CUR (the example being drawn) and CODE (its code text) before each call."""
__version__ = "3.1.0"
import ast
import contextlib
import inspect
import io
import re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v3_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg

CUR = {}
CODE = ""


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def vis(t):
    """make blanks and line breaks visible"""
    return "".join({" ": "·", "\n": "⏎", "\t": "⇥"}.get(c, c) for c in t)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO if mono else None, line=C["line"], radius=0.15)


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def captured(expr, ns):
    """(printed text, value) of evaluating `expr` in ns (a copy of the example's namespace)"""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        val = eval(expr, dict(ns))
    return buf.getvalue(), val


def lines_of(out):
    return out.rstrip("\n").split("\n")


# ------------------------------------------------------------------ part 1
@need(1.15)
def v_hello(s, x, y, w, h, ns, out):
    names = re.findall(r"hello\('(\w+)'\)", CODE)
    for k, (nm, line) in enumerate(zip(names, lines_of(out))):
        yy = y + k * 0.58
        chip(s, x, yy, 1.9, 0.4, "hello(%r)" % nm, "plain", fs=10)
        arrow(s, x + 1.95, yy + 0.2, x + 2.3, yy + 0.2, C["muted"])
        chip(s, x + 2.35, yy, 1.8, 0.4, "name = %r" % nm, "amber", fs=10)
        arrow(s, x + 4.2, yy + 0.2, x + 4.55, yy + 0.2, C["muted"])
        chip(s, x + 4.6, yy, 2.5, 0.4, "'Hello, ' + name", "teal", fs=10)
        arrow(s, x + 7.15, yy + 0.2, x + 7.5, yy + 0.2, C["muted"])
        chip(s, x + 7.55, yy, 1.65, 0.4, line, "green", fs=10)


@need(1.2)
def v_dedup(s, x, y, w, h, ns, out):
    pasted, made = ns["pasted"], ns["made"]
    rows = [["Line", "Pasted copy", "Made by greeting()", "Same?"]]
    cc, cf = {}, {}
    for i, (a, b) in enumerate(zip(pasted, made), 1):
        rows.append([str(i), repr(a), repr(b), str(a == b)])
        cc[(i, 3)] = C["green"] if a == b else C["coral"]
        if a != b:
            cf[(i, 1)] = C["redLight"]
    table(s, x, y, w * 0.7, rows, [0.5, 2.6, 2.6, 0.9], rowh=0.33, mono_cols=(1, 2, 3), cell_color=cc, cell_fill=cf, align_cols={0: PP_ALIGN.CENTER})
    same = sum(1 for a, b in zip(pasted, made) if a == b)
    chart(s, "col", x + w * 0.74, y, w * 0.26, min(h, 1.45), ["same", "different"], [("lines", [same, len(pasted) - same])], fs=9, legend=False, gap=50, vmax=4, major=1)


@need(1.15)
def v_params(s, x, y, w, h, ns, out):
    pairs = re.findall(r"describe\('(\w+)', '(\w+)'\)", CODE)
    rows = [["Call", "animal gets", "sound gets", "The call gives"]]
    for (a, b), line in zip(pairs, lines_of(out)):
        rows.append(["describe(%r, %r)" % (a, b), repr(a), repr(b), repr(line)])
    table(s, x, y, w, rows, [3.0, 1.6, 1.6, 3.0], rowh=0.34, mono_cols=(0, 1, 2, 3), cell_fill={(2, 1): C["amberLight"], (2, 2): C["amberLight"]})
    tb(s, x, y + 0.34 * len(rows) + 0.08, w, 0.28, "second call: the arguments are swapped, so the meaning is swapped", 10, C["muted"], italic=True)


@need(1.2)
def v_returns(s, x, y, w, h, ns, out):
    dbl = ns["double"]
    xs = [("double(21)", "plain"), ("n = 21", "amber"), ("return n * 2", "teal"), (repr(dbl(21)), "green"), ("x = %r" % ns["x"], "green")]
    cw = 1.62
    for i, (t, k) in enumerate(xs):
        chip(s, x + i * (cw + 0.28), y, cw, 0.4, t, k, fs=10)
        if i:
            arrow(s, x + i * (cw + 0.28) - 0.26, y + 0.2, x + i * (cw + 0.28) - 0.02, y + 0.2, C["muted"])
    inner, outer = dbl(2), dbl(dbl(2))
    ys = y + 0.62
    for i, (t, k) in enumerate([("double(double(2))", "plain"), ("inner call double(2) = %r" % inner, "amber"), ("outer call double(%r) = %r" % (inner, outer), "green")]):
        wd = [2.4, 3.2, 3.2][i]
        xx = x + [0, 2.7, 6.2][i]
        chip(s, xx, ys, wd, 0.4, t, k, fs=10)
        if i:
            arrow(s, xx - 0.3, ys + 0.2, xx - 0.02, ys + 0.2, C["muted"])


@need(1.5)
def v_none(s, x, y, w, h, ns, out):
    exprs = ["shout('hi')", "len('hello')", "len([1, 2, 3])", "print('x')"]
    rows = [["Call", "It printed", "It gave back", "Type of that value"]]
    cc = {}
    for i, e in enumerate(exprs, 1):
        txt, val = captured(e, ns)
        rows.append([e, repr(txt) if txt else "nothing", repr(val), type(val).__name__])
        if val is None:
            cc[(i, 2)] = C["coral"]
            cc[(i, 3)] = C["coral"]
        else:
            cc[(i, 2)] = C["green"]
    table(s, x, y, w, rows, [2.4, 1.8, 1.8, 2.4], rowh=0.3, mono_cols=(0, 1, 2, 3), cell_color=cc)


@need(1.6)
def v_named(s, x, y, w, h, ns, out):
    calls = ["print('cats', 'dogs', 'mice')", "print('cats', 'dogs', 'mice', sep=', ')", "print('Hello', end='')", "print(' World')"]
    rows = [["Call", "What it printed (· blank, ⏎ line break)", "Characters"]]
    nums = []
    for c_ in calls:
        t, _ = captured(c_, {})
        rows.append([c_.replace("print(", "", 1)[:-1], vis(t), str(len(t))])
        nums.append(len(t))
    table(s, x, y, w * 0.68, rows, [2.7, 2.6, 0.9], rowh=0.3, fs=9.5, mono_cols=(0, 1), align_cols={2: PP_ALIGN.CENTER})
    chart(s, "bar", x + w * 0.71, y, w * 0.29, min(h, 1.6), ["1", "2", "3", "4"][::-1], [("characters printed by call", nums[::-1])], fs=9, legend=False, gap=40)


@need(1.45)
def v_defaults(s, x, y, w, h, ns, out):
    sig = inspect.signature(ns["area"])
    calls = [((3,), {}), ((3, 4), {}), ((3,), {"unit": "cm"})]
    rows = [["Call", "width", "height", "unit", "area gives"]]
    cf = {}
    for i, (a, k) in enumerate(calls, 1):
        given = sig.bind(*a, **k)
        full = sig.bind(*a, **k)
        full.apply_defaults()
        txt = "area(" + ", ".join([repr(v) for v in a] + ["%s=%r" % kv for kv in k.items()]) + ")"
        row = [txt]
        for j, p in enumerate(["width", "height", "unit"], 1):
            row.append(("%r" % full.arguments[p]) + ("" if p in given.arguments else " (default)"))
            if p not in given.arguments:
                cf[(i, j)] = C["amberLight"]
        row.append(repr(ns["area"](*a, **k)))
        rows.append(row)
    table(s, x, y, w, rows, [2.6, 0.9, 1.5, 1.5, 1.3], rowh=0.36, mono_cols=(0, 1, 2, 3, 4), cell_fill=cf)
    tb(s, x, y + 0.36 * len(rows) + 0.06, w, 0.26, "amber: filled in from the default, not from the call", 10, C["muted"], italic=True)


@need(1.45)
def v_mutable(s, x, y, w, h, ns, out):
    parts = re.findall(r"\[[^\]]*\]", out)
    calls = ["add_item('a')", "add_item('b')", "add_safe('a')", "add_safe('b')"]
    rows = [["Call", "The list that was printed", "Items"]]
    cf = {}
    for i, (c_, p) in enumerate(zip(calls, parts), 1):
        rows.append([c_, p, str(len(ast.literal_eval(p)))])
        if i <= 2:
            cf[(i, 1)] = C["redLight"]
        else:
            cf[(i, 1)] = C["greenLight"]
    table(s, x, y, w * 0.62, rows, [1.8, 2.6, 0.8], rowh=0.28, mono_cols=(0, 1), cell_fill=cf, align_cols={2: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.66, y, w * 0.34, min(h, 1.45), ["a1", "a2", "s1", "s2"], [("items in the printed list", [len(ast.literal_eval(p)) for p in parts])], fs=9, legend=False, gap=50, vmax=3, major=1)


# ------------------------------------------------------------------ part 2
@need(1.15)
def v_stack(s, x, y, w, h, ns, out):
    m = re.match(r"(\[.*\]) (\d+)", out.strip())
    a_res, top = ast.literal_eval(m.group(1)), int(m.group(2))
    depths = [("top level", top), ("a()", a_res[0]), ("b()", a_res[1][0]), ("c()", a_res[1][1])]
    bh = 0.235
    for name, d in depths:
        yy = y + (3 - d) * (bh + 0.045)
        chip(s, x + 0.2, yy, 2.4, bh, "%s   depth %d" % (name, d), ["grey", "teal", "teal", "amber"][d], fs=9.5)
        if d < 3:
            arrow(s, x + 1.4, yy + bh + 0.045, x + 1.4, yy + bh, C["muted"], 1.0)
    tb(s, x + 2.7, y + 0.02, 1.8, 0.5, "newest call on top; each arrow points to its caller", 9, C["muted"], italic=True)
    chart(s, "col", x + 4.6, y, w - 4.6, min(h, 1.15), [n for n, _ in depths], [("depth", [d for _, d in depths])], fs=8, legend=False, gap=60, vmax=3, major=1)


@need(1.45)
def v_frame(s, x, y, w, h, ns, out):
    tup = ast.literal_eval(re.search(r"\(.*?\)", out).group())
    probe = dict(ns)
    exec("top_pair = inner()", probe)   # called from module-level code: the caller frame is the module's own
    top_name = probe["top_pair"][1]
    boxes = [("frame of %s" % tup[0], "co_name %r" % tup[0], "amber"), ("frame of %s" % tup[1], "co_name %r" % tup[1], "teal"), ("frame of the top level", "co_name %r" % top_name, "grey")]
    for i, (a, b, k) in enumerate(boxes):
        xx = x + i * 3.1
        chip(s, xx, y, 2.3, 0.4, a, k, fs=10.5)
        tb(s, xx, y + 0.44, 2.3, 0.26, b, 9.5, C["muted"], font=MONO, align=PP_ALIGN.CENTER)
        if i < 2:
            arrow(s, xx + 2.35, y + 0.2, xx + 2.95, y + 0.2, C["teal"], 1.6)
            tb(s, xx + 2.35, y - 0.05, 0.6, 0.22, "f_back", 8.5, C["teal"], font=MONO, align=PP_ALIGN.CENTER, margin=(0, 0))
    rows = [["Expression in inner", "Value"], ["me.f_code.co_name", repr(tup[0])], ["caller.f_code.co_name", repr(tup[1])]]
    table(s, x, y + 0.85, w * 0.6, rows, [2.4, 1.5], rowh=0.3, mono_cols=(0, 1))


@need(1.5)
def v_localgone(s, x, y, w, h, ns, out):
    val = lines_of(out)[0]
    err = lines_of(out)[1]
    gnames = [k for k in ns if not k.startswith("__")]
    rect(s, x, y, 4.0, 1.4, C["card"], line=C["line"], radius=0.05, name="card")
    tb(s, x + 0.1, y + 0.03, 3.8, 0.26, "global scope", 11, C["teal"], bold=True)
    chip(s, x + 0.15, y + 0.34, 1.5, 0.34, ", ".join(gnames), "plain", fs=10)
    chip(s, x + 0.15, y + 0.8, 3.7, 0.34, "'eggs' in globals() is %s" % ("eggs" in ns), "red", fs=10)
    rect(s, x + 5.0, y, 4.1, 1.4, C["card"], line=C["line"], radius=0.05, name="card")
    tb(s, x + 5.1, y + 0.03, 3.9, 0.26, "local scope of one call of make()", 11, C["amber"], bold=True)
    chip(s, x + 5.15, y + 0.34, 1.9, 0.34, "eggs = %s" % val, "amber", fs=10)
    chip(s, x + 5.15, y + 0.8, 3.8, 0.34, "co_varnames = %s" % (ns["make"].__code__.co_varnames,), "plain", fs=9.5)
    arrow(s, x + 4.05, y + 0.45, x + 4.95, y + 0.45, C["teal"], 1.6)
    tb(s, x + 4.0, y + 0.1, 1.0, 0.3, "call", 9, C["teal"], align=PP_ALIGN.CENTER, margin=(0, 0))
    arrow(s, x + 4.95, y + 0.95, x + 4.05, y + 0.95, C["green"], 1.6)
    tb(s, x + 4.0, y + 0.98, 1.0, 0.3, "returns %s" % val, 9, C["green"], align=PP_ALIGN.CENTER, margin=(0, 0))
    tb(s, x, y + 1.45, w, 0.26, "outside the call, printing eggs raises %s" % err, 10, C["muted"], italic=True)


@need(1.4)
def v_walls(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    yv = re.search(r"y = '([^']*)'", CODE).group(1)
    cols = [("global scope", "x = %r" % ns["x"], "teal"), ("local scope of f", "y = %r" % yv, "amber"),
            ("local scope of g", "no local names" if not ns["g"].__code__.co_varnames else str(ns["g"].__code__.co_varnames), "grey")]
    cw, gap = 2.8, 0.4
    for i, (a, b, k) in enumerate(cols):
        xx = x + i * (cw + gap)
        rect(s, xx, y, cw, 0.95, C["card"], line=C["line"], radius=0.05, name="card")
        tb(s, xx + 0.08, y + 0.03, cw - 0.16, 0.26, a, 11, C["ink"], bold=True)
        chip(s, xx + 0.1, y + 0.4, cw - 0.2, 0.4, b, k, fs=9.5)
    arrow(s, x + cw + gap + 0.02, y + 0.55, x + cw - 0.02, y + 0.55, C["green"], 2.0)
    arrow(s, x + 2 * (cw + gap) + 0.02, y + 0.55, x + 2 * cw + gap - 0.02, y + 0.55, C["coral"], 2.0)
    chip(s, x + cw + gap - 0.9, y + 1.05, 2.6, 0.32, "f() gives %r" % ls[0], "green", fs=9.5)
    chip(s, x + 2 * (cw + gap) - 0.6, y + 1.05, 3.0, 0.32, "g() raises %s" % ls[1].split()[-1], "red", fs=9.5)


@need(1.35)
def v_samename(s, x, y, w, h, ns, out):
    vals = out.split()
    rows = [["Where the name spam lives", "Local variables of the code", "spam holds"],
            ["the global scope", "(module level)", repr(ns["spam"])]]
    for fn in ("one", "two"):
        rows.append(["local scope of %s()" % fn, str(ns[fn].__code__.co_varnames), repr(ns[fn]())])
    table(s, x, y, w, rows, [3.2, 3.4, 2.6], rowh=0.36, mono_cols=(1, 2), cell_fill={(1, 2): C["tealLight"], (2, 2): C["amberLight"], (3, 2): C["amberLight"]})


@need(1.4)
def v_globalstmt(s, x, y, w, h, ns, out):
    g1 = CUR["groups"][0][0]
    fresh = {}
    exec("\n".join(g1), fresh)
    steps = [("after the definitions", None), ("after without_global()", "without_global"), ("after with_global()", "with_global")]
    rows = [["Moment", "Global eggs holds", "Why"]]
    cf = {}
    prev = None
    why = ["nothing has run yet", "the assignment made a new local variable", "global eggs: the assignment reached the module"]
    for i, (lab, fn) in enumerate(steps, 1):
        if fn:
            fresh[fn]()
        rows.append([lab, repr(fresh["eggs"]), why[i - 1]])
        if prev is not None and fresh["eggs"] != prev:
            cf[(i, 1)] = C["amberLight"]
        prev = fresh["eggs"]
    table(s, x, y, w, rows, [2.5, 2.8, 3.9], rowh=0.34, mono_cols=(0, 1), cell_fill=cf)


@need(1.2)
def v_nonlocal(s, x, y, w, h, ns, out):
    vals = [int(v) for v in out.split()]
    t = ns["counter"]()
    rows = [["Call", "tick() returns", "count inside step is now"]]
    for i in range(1, 4):
        r = t()
        rows.append(["call %d of tick()" % i, str(r), str(t.__closure__[0].cell_contents)])
    table(s, x, y, w * 0.62, rows, [2.2, 1.8, 2.4], rowh=0.32, mono_cols=(1, 2), align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.66, y, w * 0.34, min(h, 1.3), ["call 1", "call 2", "call 3"], [("tick() returned", vals)], fs=9, legend=False, gap=50, vmax=4, major=1)


@need(1.2)
def v_identify(s, x, y, w, h, ns, out):
    rows = [["Function", "Local variables (co_varnames)", "Global names (co_names)", "Python treats eggs as"]]
    cf = {}
    for i, name in enumerate(("reads", "assigns", "declares"), 1):
        c_ = ns[name].__code__
        kind = "local" if "eggs" in c_.co_varnames else "global"
        rows.append([name, str(c_.co_varnames), str(c_.co_names), kind])
        cf[(i, 3)] = C["amberLight"] if kind == "local" else C["tealLight"]
    table(s, x, y, w, rows, [1.6, 2.8, 2.6, 2.2], rowh=0.34, mono_cols=(0, 1, 2, 3), cell_fill=cf)


@need(1.6)
def v_unbound(s, x, y, w, h, ns, out):
    mro = [c_.__name__ for c_ in ns["kind"].__mro__]
    steps = [("print(eggs)", "plain"), ("eggs is local here", "amber"), ("no value yet", "grey"), (ns["kind"].__name__, "red")]
    cw = 2.0
    for i, (t, k) in enumerate(steps):
        chip(s, x + i * (cw + 0.36), y, cw, 0.38, t, k, fs=10)
        if i:
            arrow(s, x + i * (cw + 0.36) - 0.34, y + 0.19, x + i * (cw + 0.36) - 0.02, y + 0.19, C["muted"])
    tb(s, x, y + 0.5, 4.0, 0.24, "the family of that exception (parent class to the right)", 10, C["muted"], italic=True)
    for i, n in enumerate(mro):
        chip(s, x + i * 1.85, y + 0.8, 1.6, 0.36, n, "red" if i == 0 else ("amber" if i == 1 else "plain"), fs=9)
        if i:
            arrow(s, x + i * 1.85 - 0.22, y + 0.98, x + i * 1.85 - 0.02, y + 0.98, C["muted"], 1.2)


# ------------------------------------------------------------------ part 3
@need(1.6)
def v_tryexcept(s, x, y, w, h, ns, out):
    args = [int(a) for a in re.findall(r"spam\((\d+)\)", CODE)]
    rows = [["Call", "Result", "Which block ran"]]
    cc = {}
    for i, a in enumerate(args, 1):
        r = ns["spam"](a)
        ex = isinstance(r, str)
        rows.append(["spam(%d)" % a, repr(r), "except" if ex else "try finished"])
        cc[(i, 2)] = C["coral"] if ex else C["green"]
    table(s, x, y, w * 0.68, rows, [1.2, 3.4, 1.6], rowh=0.3, mono_cols=(0, 1, 2), cell_color=cc)
    nums = [ns["spam"](a) for a in args]
    chart(s, "col", x + w * 0.71, y, w * 0.29, min(h, 1.5), ["spam(%d)" % a for a in args], [("number returned (0 when except ran)", [0 if isinstance(r, str) else r for r in nums])], fs=8, legend=False, gap=40)


@need(1.4)
def v_inloop(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    ns_ = [2, 0, 1]
    rows = [["n", "What happened", "Printed"]]
    cc = {}
    for i, (n, l) in enumerate(zip(ns_, ls), 1):
        bad = l.startswith("Error")
        rows.append([str(n), "except ran, the loop goes on" if bad else "try finished", l])
        cc[(i, 1)] = C["coral"] if bad else C["green"]
    table(s, x, y, w * 0.72, rows, [0.5, 3.0, 3.1], rowh=0.32, mono_cols=(0, 2), cell_color=cc, align_cols={0: PP_ALIGN.CENTER})
    ok = sum(1 for l in ls if not l.startswith("Error"))
    chart(s, "col", x + w * 0.75, y, w * 0.25, min(h, 1.4), ["result", "handled"], [("calls", [ok, len(ls) - ok])], fs=9, legend=False, gap=50, vmax=3, major=1)


@need(1.4)
def v_aroundall(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    fail = next(i for i, l in enumerate(ls) if l.startswith("Error"))
    ncalls = 3
    stat = ["ran and printed"] * fail + ["raised: except ran"] + ["never started"] * (ncalls - fail - 1)
    cols = {"ran and printed": "green", "raised: except ran": "red", "never started": "grey"}
    args = [2, 0, 1]
    for i, (a, st) in enumerate(zip(args, stat)):
        chip(s, x + i * 3.1, y, 2.9, 0.4, "spam(%d): %s" % (a, st), cols[st], fs=10)
        if i:
            arrow(s, x + i * 3.1 - 0.2, y + 0.2, x + i * 3.1 - 0.02, y + 0.2, C["muted"], 1.2)
    chart(s, "col", x, y + 0.55, w * 0.5, min(h - 0.55, 1.2), ["ran", "raised", "never started"], [("calls", [stat.count("ran and printed"), 1, stat.count("never started")])], fs=9, legend=False, gap=60, vmax=3, major=1)
    tb(s, x + w * 0.55, y + 0.7, w * 0.45, 0.8, "printed: %s" % " | ".join(ls), 10, C["muted"], italic=True, font=MONO)


@need(1.3)
def v_several(s, x, y, w, h, ns, out):
    rows = [["Input", "What int() raised", "parse() returns"]]
    cc = {}
    for i, v in enumerate(["12", "x", None], 1):
        try:
            int(v)
            raised = "nothing"
        except Exception as e:
            raised = type(e).__name__
        r = ns["parse"](v)
        rows.append([repr(v), raised, repr(r)])
        cc[(i, 1)] = C["green"] if raised == "nothing" else C["coral"]
    table(s, x, y, w * 0.75, rows, [1.4, 2.4, 2.4], rowh=0.34, mono_cols=(0, 1, 2), cell_color=cc)


@need(1.3)
def v_traceback(s, x, y, w, h, ns, out):
    names = ast.literal_eval(out.strip())
    try:
        1 / 0
    except ZeroDivisionError as e:
        exc = type(e).__name__
    items = ["%s()" % n for n in names] + ["1 / 0", exc]
    kinds = ["plain", "plain", "amber", "red"]
    cw = 2.0
    for i, (t, k) in enumerate(zip(items, kinds)):
        chip(s, x + i * (cw + 0.38), y, cw, 0.4, t, k, fs=10.5)
        if i:
            arrow(s, x + i * (cw + 0.38) - 0.36, y + 0.2, x + i * (cw + 0.38) - 0.02, y + 0.2, C["muted"])
    rows = [["Traceback entry (oldest first)", "Function"]] + [[str(i), n] for i, n in enumerate(names, 1)]
    table(s, x, y + 0.65, w * 0.55, rows, [2.4, 1.6], rowh=0.3, mono_cols=(1,))
    tb(s, x + w * 0.58, y + 0.7, w * 0.4, 0.6, "the path to the error, as the exception saved it", 10, C["muted"], italic=True)


# ------------------------------------------------------------------ part 4
@need(1.1)
def v_zigzag(s, x, y, w, h, ns, out):
    path = ns["path"]
    chart(s, "col", x, y, w, min(h, 1.6), [str(i) for i in range(len(path))], [("indent", list(path))], fs=8, legend=False, gap=20, vmax=20, major=10, axis_title="indent of the band, step by step")


@need(1.3)
def v_spike(s, x, y, w, h, ns, out):
    L = ns["lengths"]
    chart(s, "col", x, y, w * 0.72, min(h, 1.6), [str(i) for i in range(1, len(L) + 1)], [("dashes in the line", L)], fs=8, legend=False, gap=30, vmax=70, major=20, axis_title="dashes in each line")
    rows = [["Line", "Dashes"], ["4", str(L[3])], ["8", str(L[7])], ["14", str(L[-1])]]
    table(s, x + w * 0.76, y, w * 0.24, rows, [0.8, 1.0], rowh=0.3, mono_cols=(0, 1), align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})


@need(1.3)
def v_collatz(s, x, y, w, h, ns, out):
    seq = ns["seq"]
    chart(s, "col", x, y, w * 0.62, min(h, 1.6), [str(v) for v in seq], [("value", seq)], fs=9, legend=False, gap=40, axis_title="the sequence from 6")
    rows = [["The number is", "Next number"], ["even", "n // 2"], ["odd", "3 * n + 1"]]
    table(s, x + w * 0.66, y, w * 0.34, rows, [1.2, 1.4], rowh=0.34, mono_cols=(1,))
    tb(s, x + w * 0.66, y + 1.1, w * 0.34, 0.4, "steps to reach 1: %d" % (len(seq) - 1), 10.5, C["ink"], bold=True)


VISUALS = {"hello": v_hello, "dedup": v_dedup, "params": v_params, "returns": v_returns, "none": v_none, "named": v_named, "defaults": v_defaults,
           "mutable": v_mutable, "stack": v_stack, "frame": v_frame, "localgone": v_localgone, "walls": v_walls, "samename": v_samename,
           "globalstmt": v_globalstmt, "nonlocal": v_nonlocal, "identify": v_identify, "unbound": v_unbound, "tryexcept": v_tryexcept, "inloop": v_inloop,
           "aroundall": v_aroundall, "several": v_several, "traceback": v_traceback, "zigzag": v_zigzag, "spike": v_spike, "collatz": v_collatz}
