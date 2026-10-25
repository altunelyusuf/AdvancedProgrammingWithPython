"""Chapter 2 deck visuals, version 4.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every value, truth value and branch shown is taken from a run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v4_0_0.py passes in, a trace of the same code, or the same expression evaluated again here);
nothing is typed in by hand except the plain-language names of columns and short reasons.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "4.0.0"
import re
import sys
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v4_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg
import examples_v4_0_0 as X


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


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


def tv(v):
    return C["green"] if v is True else (C["coral"] if v is False else C["ink"])


def trace(exid):
    """Run the code of example exid under a line tracer. Returns (lines, states): lines[i] = the 1-based line number run at step i;
    states[i] = a copy of the module variables just after that line ran (taken at the next step or at the end)."""
    src = X.code_text(X.BY_ID[exid])
    seen, snaps = [], []

    def tracer(frame, event, arg):
        if frame.f_code.co_filename != "<trace>":
            return tracer
        if event == "line":
            seen.append(frame.f_lineno)
            snaps.append({k: v for k, v in frame.f_globals.items() if not k.startswith("__")})
        elif event == "return" and frame.f_code.co_name == "<module>":
            snaps.append({k: v for k, v in frame.f_globals.items() if not k.startswith("__")})
        return tracer

    ns = {"__name__": "__trace__"}
    import io, contextlib
    old = sys.gettrace()
    sys.settrace(tracer)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src, "<trace>", "exec"), ns)
    finally:
        sys.settrace(old)
    return seen, snaps[1:]


# ------------------------------------------------------------------ part 1
@need(1.9)
def v_booleans(s, x, y, w, h, ns, out):
    exprs = ["True", "False", "True + True", "int(False)", "bool(0)", "bool(-3.5)"]
    rows = [["Expression", "Value", "Type"]]
    cc, nums = {}, []
    for i, e in enumerate(exprs, 1):
        v = eval(e)
        rows.append([e, repr(v), type(v).__name__])
        cc[(i, 1)] = tv(v)
        nums.append(int(v))
    table(s, x, y, w * 0.6, rows, [2.0, 1.2, 1.2], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2), cell_color=cc)
    tb(s, x + w * 0.63, y - 0.02, w * 0.37, 0.24, "the same values as numbers", 10, C["muted"], italic=True)
    chart(s, "col", x + w * 0.63, y + 0.2, w * 0.37, max(1.3, h - 0.2), [e if len(e) < 9 else e[:8] for e in exprs], [("as a number", nums)], fs=9, legend=False, gap=40, vmax=3, major=1)


@need(1.9)
def v_comparison(s, x, y, w, h, ns, out):
    import operator as op
    xv, yv = ns["x"], ns["y"]
    ops = [("==", op.eq, "equal to"), ("!=", op.ne, "not equal to"), ("<", op.lt, "less than"), ("<=", op.le, "less than or equal"),
           (">", op.gt, "greater than"), (">=", op.ge, "greater than or equal")]
    rows = [["Operator", "Reads as", "x op y", "Result"]]
    cc, vals = {}, []
    for i, (sym, f, rd) in enumerate(ops, 1):
        r = f(xv, yv)
        rows.append([sym, rd, "%d %s %d" % (xv, sym, yv), str(r)])
        cc[(i, 3)] = tv(r)
        vals.append(int(r))
    table(s, x, y, w * 0.64, rows, [0.9, 2.2, 1.3, 1.0], rowh=min(0.3, h / len(rows)), mono_cols=(0, 2, 3), cell_color=cc, bold_cols=(0,))
    tb(s, x + w * 0.67, y - 0.02, w * 0.33, 0.24, "True counts as 1, False as 0", 10, C["muted"], italic=True)
    chart(s, "col", x + w * 0.67, y + 0.2, w * 0.33, max(1.3, h - 0.2), [o[0] for o in ops], [("result", vals)], fs=9, legend=False, gap=40, vmax=2, major=1)


@need(1.9)
def v_equality(s, x, y, w, h, ns, out):
    items = [("42 == 42.0", "an int and a float with the same value are equal"),
             ("42 == '42'", "a number never equals a string"),
             ("'hello' == 'Hello'", "the case of a letter matters"),
             ("0.1 + 0.2 == 0.3", "the sum is %r, not 0.3" % (0.1 + 0.2)),
             ("'apple' < 'banana'", "a comes before b in the alphabet"),
             ("'Z' < 'a'", "character code %d is below %d" % (ord("Z"), ord("a")))]
    rows = [["Comparison", "Result", "Why"]]
    cc = {}
    for i, (e, why) in enumerate(items, 1):
        v = eval(e)
        rows.append([e, str(v), why])
        cc[(i, 1)] = tv(v)
    table(s, x, y, w, rows, [2.4, 0.9, 5.0], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1), cell_color=cc)


@need(1.9)
def v_chained(s, x, y, w, h, ns, out):
    age = ns["age"]
    x0, x1, top = x + 0.3, x + w * 0.62, y + 0.55
    scale = (x1 - x0) / 30.0
    px = lambda v: x0 + v * scale
    rect(s, px(10), top - 0.28, 10 * scale, 0.28, C["tealLight"], name="range")
    rect(s, px(10), top - 0.28 - 0.0, 2 * scale, 0.28, C["amberLight"], name="range")
    line_seg(s, x0, top, x1, top, C["muted"], 1.5)
    for v in range(0, 31, 5):
        line_seg(s, px(v), top, px(v), top + 0.07, C["muted"], 1.0)
        if v != age:
            tb(s, px(v) - 0.2, top + 0.09, 0.4, 0.2, str(v), 9, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
    chip(s, px(age) - 0.5, top + 0.4, 1.0, 0.3, "age = %d" % age, "teal", fs=10)
    arrow(s, px(age), top + 0.4, px(age), top + 0.03, C["teal"], 1.5)
    tb(s, px(10), y, 3.0, 0.24, "teal: 10 < age < 20    amber: 10 < age < 12", 9.5, C["muted"], italic=True)
    tests = ["10 < age < 20", "10 < age < 12", "1 < 2 > 1.5", "3 > 2 > 5"]
    for i, t in enumerate(tests):
        r = eval(t, {"age": age})
        yy = y + 0.05 + i * 0.4
        chip(s, x + w * 0.66, yy, 1.9, 0.32, t, "plain", fs=10)
        arrow(s, x + w * 0.66 + 1.93, yy + 0.16, x + w * 0.66 + 2.2, yy + 0.16, C["muted"])
        chip(s, x + w * 0.66 + 2.25, yy, 0.8, 0.32, str(r), "green" if r else "red", fs=10)


# ------------------------------------------------------------------ part 2
@need(1.75)
def v_truthtable(s, x, y, w, h, ns, out):
    rows = [["a", "b", "a and b", "a or b"]]
    cc = {}
    n_and = n_or = 0
    for i, ln in enumerate(out.strip().splitlines(), 1):
        t = ln.split()
        rows.append(t)
        for j, v in enumerate(t):
            cc[(i, j)] = C["green"] if v == "True" else C["coral"]
        n_and += t[2] == "True"
        n_or += t[3] == "True"
    table(s, x, y, w * 0.58, rows, [1, 1, 1.3, 1.3], rowh=min(0.32, h / len(rows)), mono_cols=(0, 1, 2, 3), cell_color=cc, align_cols={j: PP_ALIGN.CENTER for j in range(4)})
    tb(s, x + w * 0.62, y - 0.02, w * 0.38, 0.24, "how often the result is True", 10, C["muted"], italic=True)
    chart(s, "col", x + w * 0.62, y + 0.2, w * 0.38, max(1.3, h - 0.2), ["a and b", "a or b"], [("True results", [n_and, n_or])], fs=9, legend=False, gap=60, vmax=4, major=1)


@need(2.0)
def v_notprec(s, x, y, w, h, ns, out):
    exprs = ["not True", "not False", "not not True", "not 4 == 5", "True or False and False", "(True or False) and False", "not (True and False)"]
    rows = [["Expression", "Value"]]
    cc = {}
    for i, e in enumerate(exprs, 1):
        v = eval(e)
        rows.append([e, str(v)])
        cc[(i, 1)] = tv(v)
    table(s, x, y, w * 0.58, rows, [3.4, 1.0], rowh=min(0.25, h / len(rows)), fs=10, mono_cols=(0, 1), cell_color=cc)
    xs = x + w * 0.64
    tb(s, xs, y - 0.02, 3.2, 0.24, "which operator is applied first", 10, C["muted"], italic=True)
    names = [("1  comparisons: ==  <  >", "teal"), ("2  not", "amber"), ("3  and", "green"), ("4  or", "plain")]
    for i, (t, k) in enumerate(names):
        yy = y + 0.3 + i * 0.5
        chip(s, xs, yy, 3.2, 0.34, t, k, fs=10.5, mono=False)
        if i < 3:
            arrow(s, xs + 1.6, yy + 0.34, xs + 1.6, yy + 0.5, C["muted"], 1.2)


@need(1.4)
def v_mixing(s, x, y, w, h, ns, out):
    age, member = ns["age"], ns["member"]
    stmts = [("age >= 18", "member", "and", None), ("age < 13", "age > 65", "or", None), ("age >= 18 and member", None, "not", None)]
    for i, (a, b, o, _) in enumerate(stmts):
        yy = y + i * 0.5
        va = eval(a, {"age": age, "member": member})
        xx = x
        wa = 0.3 + 0.1 * len("%s = %s" % (a, va))
        chip(s, xx, yy, wa, 0.36, "%s = %s" % (a, va), "green" if va else "red", fs=9.5)
        xx += wa + 0.1
        if b:
            vb = eval(b, {"age": age, "member": member})
            arrow(s, xx, yy + 0.18, xx + 0.3, yy + 0.18, C["muted"])
            chip(s, xx + 0.35, yy, 0.6, 0.36, o, "amber", fs=11)
            arrow(s, xx + 0.95, yy + 0.18, xx + 1.25, yy + 0.18, C["muted"])
            wb = 0.3 + 0.1 * len("%s = %s" % (b, vb))
            chip(s, xx + 1.3, yy, wb, 0.36, "%s = %s" % (b, vb), "green" if vb else "red", fs=9.5)
            xx += 1.3 + wb + 0.1
            res = eval("%s %s %s" % (a, o, b), {"age": age, "member": member})
        else:
            arrow(s, xx, yy + 0.18, xx + 0.3, yy + 0.18, C["muted"])
            chip(s, xx + 0.35, yy, 0.6, 0.36, o, "amber", fs=11)
            xx += 1.0
            res = eval("not (%s)" % a, {"age": age, "member": member})
        arrow(s, xx, yy + 0.18, xx + 0.3, yy + 0.18, C["muted"])
        chip(s, xx + 0.35, yy, 1.4, 0.36, "result = %s" % res, "green" if res else "red", fs=9.5)


@need(1.9)
def v_shortcircuit(s, x, y, w, h, ns, out):
    exprs = ["1 or 1 / 0", "0 and 1 / 0", "'hi' and 'there'", "'' or 'default'", "0 or [] or None", "1 and 2 and 3"]
    rows = [["Expression", "Result", "Type", "Operands looked at"]]
    cc = {}
    tot, seen = [], []
    for i, e in enumerate(exprs, 1):
        op = "or" if " or " in e else "and"
        parts = e.split(" %s " % op)
        looked = 0
        for p in parts:
            v = eval(p)
            looked += 1
            if (op == "or" and v) or (op == "and" and not v):
                break
        r = eval(e)
        rows.append([e, repr(r), type(r).__name__, "%d of %d" % (looked, len(parts))])
        cc[(i, 3)] = C["teal"] if looked < len(parts) else C["muted"]
        tot.append(len(parts))
        seen.append(looked)
    table(s, x, y, w * 0.62, rows, [2.1, 1.1, 0.8, 1.5], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2), cell_color=cc, bold_cols=(3,))
    tb(s, x + w * 0.65, y - 0.02, w * 0.35, 0.24, "operands in the line and operands looked at", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.65, y + 0.2, w * 0.35, max(1.3, h - 0.2), [str(i) for i in range(1, 7)], [("operands", tot), ("looked at", seen)], fs=9, legend=True, gap=50, vmax=4, major=1,
          colors=[C["pale"], C["teal"]])


@need(1.7)
def v_truthiness(s, x, y, w, h, ns, out):
    vals = ns["values"]
    half = (len(vals) + 1) // 2
    nt = sum(1 for v in vals if v)
    for k, part in enumerate((vals[:half], vals[half:])):
        rows = [["value", "bool(value)"]] + [[repr(v), str(bool(v))] for v in part]
        cc = {(i, 1): tv(bool(v)) for i, v in enumerate(part, 1)}
        table(s, x + k * 2.45, y, 2.35, rows, [1.2, 1.2], rowh=0.27, mono_cols=(0, 1), cell_color=cc)
    chart(s, "col", x + 5.0, y, 2.2, 1.45, ["true", "false"], [("values", [nt, len(vals) - nt])], fs=9, legend=False, gap=60, vmax=6, major=2)
    g = ns["greeting"]
    chip(s, x, y + 1.45, 3.3, 0.28, "greeting == True gives %s" % (g == True), "red", fs=10)  # noqa: E712
    chip(s, x + 3.45, y + 1.45, 3.3, 0.28, "bool(greeting) gives %s" % bool(g), "green", fs=10)


# ------------------------------------------------------------------ part 3
def flow_node(s, x, y, w, h, text, ran, kind="plain"):
    chip(s, x, y, w, h, text, ("teal" if kind == "plain" else kind) if ran else "grey", fs=10, mono=True)


@need(1.7)
def v_block(s, x, y, w, h, ns, out):
    lines, _ = trace("block")
    code = X.code_lines(X.BY_ID["block"])
    ran = set(lines)
    cond = ns["age"] > 65
    bw = 1.95
    xs = [x, x + 2.25, x + 4.5, x + 6.75]
    nodes = [(2, "age > 65 ?"), (3, code[2].strip()), (4, code[3].strip()), (5, code[4].strip())]
    for (ln, t), xx in zip(nodes, xs):
        chip(s, xx, y + 0.15, bw, 0.4, t, ("amber" if ln == 2 else "teal") if ln in ran else "grey", fs=10)
    for i in range(3):
        a = xs[i] + bw
        b = xs[i + 1]
        arrow(s, a, y + 0.35, b, y + 0.35, C["teal"] if (i < 2 and cond) else C["line"], 1.8)
    tb(s, xs[0] + 1.0, y + 0.58, 1.9, 0.22, "True: enter the block" if cond else "False: skip", 9.5, C["teal"], italic=True)
    kc = C["muted"] if not cond else C["line"]
    x_a, x_b = xs[0] + bw / 2, xs[3] + bw / 2
    line_seg(s, x_a, y + 0.55, x_a, y + 0.95, kc, 1.2)
    line_seg(s, x_a, y + 0.95, x_b, y + 0.95, kc, 1.2)
    arrow(s, x_b, y + 0.95, x_b, y + 0.57, kc, 1.2)
    tb(s, x + 2.4, y + 0.97, 4.5, 0.24, "False: jump over the block to the next line", 9.5, C["muted"], italic=True)
    chip(s, x, y + 1.3, 5.3, 0.3, "lines run: %s of %d" % (sorted(ran), len(code)), "plain", fs=10)
    chip(s, x + 5.5, y + 1.3, 3.4, 0.3, "printed: %s" % " / ".join(out.split()), "green", fs=10)


@need(1.7)
def v_indent(s, x, y, w, h, ns, out):
    lines, _ = trace("indent")
    code = X.code_lines(X.BY_ID["indent"])
    ran = set(lines)
    rows = [["Line", "Code", "Indent", "Did it run?"]]
    cc = {}
    for i, c in enumerate(code, 1):
        ind = len(c) - len(c.lstrip())
        rows.append([str(i), c.strip(), "%d spaces" % ind if ind else "none", "yes" if i in ran else "no, skipped"])
        cc[(i, 3)] = C["green"] if i in ran else C["coral"]
    table(s, x, y, w * 0.66, rows, [0.6, 3.0, 1.0, 1.3], rowh=min(0.27, h / len(rows)), mono_cols=(0, 1, 2), cell_color=cc)
    nrun = len(ran)
    tb(s, x + w * 0.69, y - 0.02, w * 0.31, 0.24, "lines run and lines skipped", 10, C["muted"], italic=True)
    chart(s, "col", x + w * 0.69, y + 0.2, w * 0.31, max(1.2, h - 0.2), ["run", "skipped"], [("lines", [nrun, len(code) - nrun])], fs=9, legend=False, gap=60, vmax=6, major=2)


@need(1.8)
def v_password(s, x, y, w, h, ns, out):
    lines, _ = trace("password")
    ran = set(lines)
    nodes = [("username == 'Mary' ?", 3, "amber", x + 0.0, y + 0.55), ("print Hello, Mary", 4, "teal", x + 2.2, y + 0.55), ("password == 'swordfish' ?", 5, "amber", x + 4.2, y + 0.55),
             ("Access granted.", 6, "teal", x + 6.9, y + 0.05), ("Wrong password.", 8, "teal", x + 6.9, y + 1.05)]
    ws = {0: 1.9, 1: 1.75, 2: 2.2, 3: 1.7, 4: 1.7}
    for k, (t, ln, kind, xx, yy) in enumerate(nodes):
        chip(s, xx, yy, ws[k], 0.4, t, kind if ln in ran else "grey", fs=9.5)
    arrow(s, x + 1.9, y + 0.75, x + 2.2, y + 0.75, C["teal"], 1.8)
    arrow(s, x + 3.95, y + 0.75, x + 4.2, y + 0.75, C["teal"], 1.8)
    arrow(s, x + 6.4, y + 0.65, x + 6.9, y + 0.3, C["teal"] if 6 in ran else C["line"], 1.8)
    arrow(s, x + 6.4, y + 0.85, x + 6.9, y + 1.2, C["teal"] if 8 in ran else C["line"], 1.8)
    tb(s, x + 6.2, y + 0.3, 0.8, 0.2, "True", 9, C["green"], bold=True, margin=(0, 0))
    tb(s, x + 6.2, y + 1.15, 0.8, 0.2, "False", 9, C["coral"], bold=True, margin=(0, 0))
    chip(s, x, y + 1.5, 2.6, 0.3, "username is False: no output", "grey", fs=9.5, mono=False)
    arrow(s, x + 0.95, y + 0.95, x + 0.95, y + 1.5, C["line"], 1.2)
    chip(s, x + 3.2, y + 1.5, 3.6, 0.3, "printed: %s" % " / ".join(out.strip().splitlines()), "green", fs=10)


@need(3.0)
def v_elif(s, x, y, w, h, ns, out):
    name, age = ns["name"], ns["age"]
    conds = ["name == 'Alice'", "age < 12", "age > 2000", "age > 100"]
    rows = [["Rung", "Condition", "Result"]]
    cc = {}
    fired = False
    ntested = 0
    for i, c in enumerate(conds, 1):
        if fired:
            rows.append([str(i), c, "not tested"])
            cc[(i, 2)] = C["greyTxt"]
            continue
        r = eval(c, {"name": name, "age": age})
        ntested += 1
        rows.append([str(i), c, str(r)])
        cc[(i, 2)] = tv(r)
        fired = fired or r
    table(s, x, y, w, rows, [0.6, 2.3, 1.4], rowh=0.3, mono_cols=(1, 2), cell_color=cc, fs=10)
    chip(s, x, y + 1.6, w, 0.3, "printed: %s" % out.strip(), "green", fs=9.5)
    tb(s, x, y + 2.0, w, 0.24, "rungs tested and rungs skipped", 10, C["muted"], italic=True)
    chart(s, "col", x, y + 2.2, w, max(1.2, h - 2.25), ["tested", "skipped"], [("rungs", [ntested, len(conds) - ntested])], fs=9, legend=False, gap=80, vmax=5, major=1)


@need(3.0)
def v_elifOrder(s, x, y, w, h, ns, out):
    rungs = ["age < 12", "age > 100", "age > 2000"]
    rows = [["Age", "Printed", "Rungs tested"]]
    cf, tested, ages = {}, [], []
    for i, ln in enumerate(out.strip().splitlines(), 1):
        a, lab = ln.split()
        a = int(a)
        n = 0
        for r in rungs:
            n += 1
            if eval(r, {"age": a}):
                break
        tested.append(n)
        ages.append("age %d" % a)
        rows.append([str(a), lab, str(n)])
        if a > 2000:
            cf[(i, 1)] = C["redLight"]
    table(s, x, y, w, rows, [0.9, 1.6, 1.4], rowh=0.28, mono_cols=(0, 1, 2), cell_fill=cf, align_cols={2: PP_ALIGN.CENTER}, fs=10)
    tb(s, x, y + 1.45, w, 0.4, "red: 3000 stops at age > 100, so the vampire rung is never reached", 9.5, C["muted"], italic=True)
    tb(s, x, y + 1.9, w, 0.24, "rungs Python tested before it stopped", 10, C["muted"], italic=True)
    chart(s, "col", x, y + 2.1, w, max(1.2, h - 2.15), ages, [("rungs tested", tested)], fs=9, legend=False, gap=60, vmax=4, major=1)


# ------------------------------------------------------------------ part 4
@need(3.0)
def v_oppositeday(s, x, y, w, h, ns, out):
    lines, states = trace("oppositeday")
    code = X.code_lines(X.BY_ID["oppositeday"])
    rows = [["Line that ran", "say_it afterwards"]]
    cc = {}
    for k, (ln, st) in enumerate(zip(lines, states), 1):
        v = st.get("say_it", "not set yet")
        rows.append([short(code[ln - 1].strip(), 30), str(v)])
        cc[(k, 1)] = tv(v) if isinstance(v, bool) else C["greyTxt"]
    rh = min(0.3, (h - 0.7) / len(rows))
    table(s, x, y, w, rows, [2.6, 1.4], rowh=rh, fs=9.5, mono_cols=(0, 1), cell_color=cc)
    yy = y + rh * len(rows) + 0.12
    chip(s, x, yy, w, 0.3, "printed: %s" % out.strip(), "green", fs=9.5)
    tb(s, x, yy + 0.34, w, 0.24, "%d of %d lines ran; the else lines were skipped" % (len(lines), len(code)), 9.5, C["muted"], italic=True)


@need(3.0)
def v_capacity(s, x, y, w, h, ns, out):
    src = X.code_text(X.BY_ID["capacity"])
    rows = [["Unit", "Discrepancy", "Real capacity"]]
    cats, adv, real = [], [], []
    import io, contextlib
    for u in ("TB", "GB", "KB"):
        n2 = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src.replace("unit = 'TB'", "unit = %r" % u), "<cap>", "exec"), n2)
        rows.append([u, "%.4f" % n2["discrepancy"], "%.2f" % n2["real"]])
        cats.append(u)
        adv.append(n2["advertised"])
        real.append(round(n2["real"], 2))
    table(s, x, y, w, rows, [0.9, 1.5, 1.5], rowh=0.3, mono_cols=(0, 1, 2), align_cols={j: PP_ALIGN.CENTER for j in range(3)}, fs=10)
    chip(s, x, y + 1.3, w, 0.3, "this run printed: %s" % out.strip(), "green", fs=9.5)
    tb(s, x, y + 1.68, w, 0.24, "advertised against real capacity, by unit", 10, C["muted"], italic=True)
    chart(s, "col", x, y + 1.9, w, max(1.3, h - 1.95), cats, [("advertised", adv), ("real", real)], fs=9, legend=True, gap=50, vmax=12, major=2, number_format="0.00", colors=[C["pale"], C["teal"]])


# ------------------------------------------------------------------ part 5
@need(1.7)
def v_condexpr(s, x, y, w, h, ns, out):
    for i, ln in enumerate(out.strip().splitlines()[:2]):
        n = int(ln.split()[0])
        r = n % 2 == 0
        yy = y + i * 0.62
        chip(s, x, yy, 0.9, 0.4, "n = %d" % n, "plain", fs=10.5)
        arrow(s, x + 0.95, yy + 0.2, x + 1.3, yy + 0.2, C["muted"])
        chip(s, x + 1.35, yy, 2.4, 0.4, "n %% 2 == 0  is  %s" % r, "green" if r else "red", fs=10.5)
        arrow(s, x + 3.8, yy + 0.12, x + 4.3, yy + 0.04, C["teal"] if r else C["line"])
        arrow(s, x + 3.8, yy + 0.28, x + 4.3, yy + 0.36, C["teal"] if not r else C["line"])
        chip(s, x + 4.35, yy - 0.02, 1.3, 0.22, "'even'", "teal" if r else "grey", fs=9)
        chip(s, x + 4.35, yy + 0.22, 1.3, 0.22, "'odd'", "teal" if not r else "grey", fs=9)
        chip(s, x + 5.9, yy, 1.5, 0.4, "printed: %s" % ln.split()[1], "amber", fs=10.5)
    line = out.strip().splitlines()[2]
    chip(s, x, y + 1.35, 4.3, 0.3, "20 >= 18 is True, so 1 / 0 is never evaluated", "teal", fs=10, mono=False)
    chip(s, x + 4.5, y + 1.35, 2.2, 0.3, "printed: %s" % line, "green", fs=10)


def case_rows(exid, out):
    """Map each printed line of a match example to the case line that produced it (read from the code text)."""
    code = X.code_lines(X.BY_ID[exid])
    prints = []
    for i, c in enumerate(code):
        m = re.search(r"print\(.*?'([^']*)'", c)
        if m and "print" in c:
            j = i
            while j >= 0 and not code[j].strip().startswith("case"):
                j -= 1
            prints.append((m.group(1), code[j].strip().rstrip(":")))
    res = []
    for ln in out.strip().splitlines():
        for lit, cs in prints:
            if lit in ln:
                res.append((ln, cs))
                break
    return res


def looped_values(exid):
    """the values the for-loops of an example go through, read from the 'for NAME in (...):' lines of its code"""
    vals = []
    for c in X.code_lines(X.BY_ID[exid]):
        m = re.match(r"for \w+ in (.*):$", c)
        if m:
            vals += list(eval(m.group(1)))
    return vals


@need(3.0)
def v_match(s, x, y, w, h, ns, out):
    rc = case_rows("match", out)
    statuses = looped_values("match")
    rows = [["Status", "Printed", "Case that matched"]]
    for st, (ln, cs) in zip(statuses, rc):
        rows.append([str(st), ln.split(" ", 1)[1], cs])
    table(s, x, y, w, rows, [0.7, 1.3, 2.2], rowh=0.3, mono_cols=(0, 1, 2), fs=9.5)
    cases = ["case 200", "case 401 | 403 | 404", "case _"]
    y0 = y + 1.55
    tb(s, x, y0 - 0.02, w, 0.24, "each status lands on the first case that fits", 10, C["muted"], italic=True)
    for i, c in enumerate(cases):
        yy = y0 + 0.3 + i * 0.62
        chip(s, x + 1.2, yy, 2.4, 0.38, c, "teal", fs=10)
        if i < 2:
            arrow(s, x + 2.4, yy + 0.38, x + 2.4, yy + 0.62, C["muted"], 1.2)
    for st, (ln, cs) in zip(statuses, rc):
        i = cases.index(cs)
        yy = y0 + 0.3 + i * 0.62
        chip(s, x, yy + 0.04, 0.8, 0.3, str(st), "amber", fs=10)
        arrow(s, x + 0.82, yy + 0.19, x + 1.18, yy + 0.19, C["amber"], 1.5)


@need(3.0)
def v_matchseq(s, x, y, w, h, ns, out):
    rc = case_rows("matchseq", out)
    tested = [repr(c) for c in ns["commands"]]
    rows = [["Value tested", "Printed", "Case that matched"]]
    for t, (ln, cs) in zip(tested, rc):
        rows.append([t, ln, cs])
    table(s, x, y, w, rows, [1.25, 1.45, 1.7], rowh=0.32, mono_cols=(0, 1, 2), fs=9)
    n = [len(c) for c in ns["commands"]]
    tb(s, x, y + 1.7, w, 0.24, "items in each list tested", 10, C["muted"], italic=True)
    chart(s, "col", x, y + 1.9, w, max(1.2, h - 1.95), [" ".join(c) for c in ns["commands"]], [("items", n)], fs=9, legend=False, gap=80, vmax=3, major=1)


@need(3.0)
def v_matchguard(s, x, y, w, h, ns, out):
    rc = case_rows("matchguard", out)
    pts = looped_values("matchguard")
    rows = [["Point", "Printed", "Case that matched"]]
    for p, (ln, cs) in zip(pts, rc):
        rows.append([repr(p), ln, cs])
    table(s, x, y, w, rows, [1.0, 1.7, 2.2], rowh=0.34, mono_cols=(0, 1, 2), fs=9.5)
    tb(s, x, y + 1.2, w, 0.24, "the two items of each point", 10, C["muted"], italic=True)
    chart(s, "col", x, y + 1.4, w, max(1.2, h - 1.5), [repr(p) for p in pts], [("x", [p[0] for p in pts]), ("y", [p[1] for p in pts])], fs=9, legend=True, gap=60, vmax=5, major=1,
          colors=[C["teal"], C["amber"]])


@need(1.8)
def v_walrus(s, x, y, w, h, ns, out):
    names = ns["names"]
    sizes = [len(n) for n in names]
    rows = [["name", "size := len(name)", "size > 3", "printed?"]]
    cc = {}
    for i, (n, z) in enumerate(zip(names, sizes), 1):
        rows.append([repr(n), str(z), str(z > 3), "yes" if z > 3 else "no"])
        cc[(i, 2)] = tv(z > 3)
    table(s, x, y, w * 0.55, rows, [1.8, 1.8, 1.0, 1.0], rowh=min(0.32, h / 5), mono_cols=(0, 1, 2), cell_color=cc, align_cols={1: PP_ALIGN.CENTER})
    chip(s, x, y + 0.34 * 4 + 0.05, w * 0.55, 0.3, "last size kept after the loop: %s" % ns["size"], "teal", fs=10, mono=False)
    tb(s, x + w * 0.58, y - 0.02, w * 0.42, 0.24, "letters per name; the test is size > 3", 10, C["muted"], italic=True)
    chart(s, "bar", x + w * 0.58, y + 0.2, w * 0.42, max(1.3, h - 0.2), [n for n in names][::-1], [("letters", sizes[::-1])], fs=9, legend=False, gap=50, vmax=12, major=3)


VISUALS = {"booleans": v_booleans, "comparison": v_comparison, "equality": v_equality, "chained": v_chained, "truthtable": v_truthtable, "notprec": v_notprec,
           "mixing": v_mixing, "shortcircuit": v_shortcircuit, "truthiness": v_truthiness, "block": v_block, "indent": v_indent, "password": v_password,
           "elif": v_elif, "elifOrder": v_elifOrder, "oppositeday": v_oppositeday, "capacity": v_capacity, "condexpr": v_condexpr, "match": v_match,
           "matchseq": v_matchseq, "matchguard": v_matchguard, "walrus": v_walrus}
