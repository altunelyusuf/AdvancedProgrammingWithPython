"""Chapter 5 deck visuals, version 3.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from a run of the example's own code (the namespace `ns`
and the printed text `out` that deck_build_v3_0_0.py passes in, or the same logic re-run here on the same text); nothing is
typed in by hand except the plain-language names of columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "3.0.0"
import ast
import contextlib
import io
import logging
import re
import traceback
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v3_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg


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


def quiet(f, *a, **k):
    """call f, swallow what it prints, return (result, exception or None)"""
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            return f(*a, **k), None
    except Exception as e:  # noqa: BLE001 - the visual wants the exception object
        return None, e


def lines_of(out):
    return [l for l in out.split("\n") if l != ""]


# ------------------------------------------------------------------ part 1
@need(1.4)
def v_boxprint(s, x, y, w, h, ns, out):
    bp = ns["box_print"]
    calls = [("'ab', 5, 4", ("ab", 5, 4)), ("'*', 2, 4", ("*", 2, 4)), ("'*', 5, 1", ("*", 5, 1)), ("'*', 5, 4", ("*", 5, 4))]
    rows = [["box_print(...)", "What happened", "Message of the exception"]]
    cc = {}
    for i, (lab, args) in enumerate(calls, 1):
        _, err = quiet(bp, *args)
        rows.append([lab, "raised" if err else "printed a box", str(err) if err else "-"])
        cc[(i, 1)] = C["coral"] if err else C["green"]
    table(s, x, y, w * 0.72, rows, [1.3, 1.4, 4.0], rowh=min(0.32, h / len(rows)), fs=10, mono_cols=(0, 2), cell_color=cc)
    box = lines_of(out)
    cw = 0.2
    bx = x + w * 0.76
    tb(s, bx, y, 2.2, 0.22, "the box that was printed", 9.5, C["muted"], italic=True)
    for r, ln in enumerate(box):
        for c, ch in enumerate(ln):
            label_shape(s, bx + c * cw, y + 0.28 + r * cw, cw - 0.02, cw - 0.02, ch if ch != " " else "", C["tealLight"] if ch != " " else C["card"], C["ink"], size=8, line=C["line"], radius=0.1)


@need(1.6)
def v_exceptionobj(s, x, y, w, h, ns, out):
    e1 = Exception("custom message")
    rows = [["Expression", "Value"], ["type(err).__name__", repr(type(e1).__name__)], ["err.args", repr(e1.args)], ["str(err)", repr(str(e1))],
            ["isinstance(ValueError(), Exception)", str(isinstance(ValueError(), Exception))]]
    table(s, x, y, w * 0.55, rows, [2.6, 2.5], rowh=min(0.3, h / len(rows)), fs=10, mono_cols=(0, 1))
    mro = [c.__name__ for c in ValueError.__mro__][:3]            # ValueError, Exception, BaseException
    bx = x + w * 0.6
    chip(s, bx + 1.1, y, 1.8, 0.3, mro[2], "grey", fs=10)
    chip(s, bx + 1.1, y + 0.55, 1.8, 0.3, mro[1], "amber", fs=10)
    chip(s, bx, y + 1.1, 1.65, 0.3, mro[0], "teal", fs=10)
    chip(s, bx + 1.85, y + 1.1, 1.65, 0.3, AssertionError.__name__, "teal", fs=10)
    arrow(s, bx + 2.0, y + 0.55, bx + 2.0, y + 0.31, C["muted"], 1.2)
    arrow(s, bx + 0.9, y + 1.1, bx + 1.6, y + 0.86, C["muted"], 1.2)
    arrow(s, bx + 2.7, y + 1.1, bx + 2.3, y + 0.86, C["muted"], 1.2)
    tb(s, bx + 2.95, y + 0.55, 0.9, 0.3, "is a kind of", 9, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE)


@need(1.5)
def v_unwinding(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    names = ast.literal_eval(ls[1])
    caught = ls[0]
    cw, gap = 2.0, 0.4
    labels = {"<module>": "load({...})", "load": "read_age(...)", "read_age": "int(text) fails"}
    for i, n in enumerate(names):
        xx = x + i * (cw + gap)
        chip(s, xx, y, cw, 0.5, n if n != "<module>" else "<module> (the try)", "teal" if i < len(names) - 1 else "red", fs=10.5)
        tb(s, xx, y + 0.52, cw, 0.25, labels.get(n, ""), 9.5, C["muted"], align=PP_ALIGN.CENTER, font=MONO, margin=(0, 0))
        if i < len(names) - 1:
            arrow(s, xx + cw + 0.03, y + 0.25, xx + cw + gap - 0.03, y + 0.25, C["teal"], 1.6)
    last = x + (len(names) - 1) * (cw + gap) + cw / 2
    first = x + cw / 2
    tb(s, first, y + 0.8, last - first, 0.25, "the ValueError climbs back until a try claims it", 10, C["coral"], bold=True, align=PP_ALIGN.CENTER)
    arrow(s, last, y + 1.1, first, y + 1.1, C["coral"], 2.0)
    chip(s, x, y + 1.2, 6.6, 0.3, caught, "amber", fs=10)


@need(1.35)
def v_notes(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    try:
        try:
            int("x")
        except ValueError as e:
            e.add_note("while reading the age field")
            raise
    except ValueError as e:
        rep = traceback.format_exception(e)
    rows = [["Last lines of the report", "What the line is"], [rep[-2].strip(), "class and message of the error"], [rep[-1].strip(), "the note, printed after the message"]]
    table(s, x, y, w * 0.78, rows, [4.6, 3.0], rowh=0.36, fs=10, mono_cols=(0,))
    chip(s, x, y + 1.25, w * 0.78, 0.32, "e.__notes__ = " + ls[0], "amber", fs=10.5)


# ------------------------------------------------------------------ part 2
def age_row(s, x, y, ages, bad, label, kind_first, kind_last, cw=0.42):
    tb(s, x, y, 1.0, 0.32, label, 10.5, C["ink"], bold=True, font=MONO, anchor=MSO_ANCHOR.MIDDLE)
    for i, a in enumerate(ages):
        k = kind_first if i == 0 else (kind_last if i == len(ages) - 1 else "plain")
        fill = {"green": C["greenLight"], "red": C["redLight"], "plain": C["card"]}[k]
        label_shape(s, x + 1.05 + i * cw, y, cw - 0.03, 0.32, str(a), fill, C["ink"], size=10.5, font=MONO, line=C["line"], radius=0.1)


@need(1.5)
def v_assertfails(s, x, y, w, h, ns, out):
    ages = [26, 57, 92, 54, 22, 15, 17, 80, 47, 73]
    srt = sorted(ages)
    rev = list(reversed(srt))
    age_row(s, x, y, srt, False, "sort()", "green", "green")
    arrow(s, x + 5.35, y + 0.16, x + 5.5, y + 0.16, C["green"], 1.6)
    chip(s, x + 5.5, y, 3.6, 0.32, "%d <= %d is %s: the assert stays silent" % (srt[0], srt[-1], srt[0] <= srt[-1]), "green", fs=10)
    age_row(s, x, y + 0.6, rev, True, "reverse()", "red", "red")
    arrow(s, x + 5.35, y + 0.76, x + 5.5, y + 0.76, C["coral"], 1.6)
    chip(s, x + 5.5, y + 0.6, 3.6, 0.32, "%d <= %d is %s: AssertionError" % (rev[0], rev[-1], rev[0] <= rev[-1]), "red", fs=10)
    tb(s, x, y + 1.1, w, 0.3, "Printed: " + " | ".join(lines_of(out)), 10.5, C["muted"], italic=True, font=MONO)


@need(1.5)
def v_assertmsg(s, x, y, w, h, ns, out):
    avg = ns["average"]
    who = {"ValueError": "the user (bad input)", "AssertionError": "our own bug", None: "-"}
    stmt = {"ValueError": "raise", "AssertionError": "assert", None: "none fired"}
    rows = [["average(...)", "Result", "Statement", "Who can cause it"]]
    cf = {}
    for i, data in enumerate(([4, 6], [], [-5, 1]), 1):
        r, err = quiet(avg, data)
        kind = type(err).__name__ if err else None
        rows.append([str(data), str(r) if not err else short("%s: %s" % (kind, err), 46), stmt[kind], who[kind]])
        cf[(i, 2)] = {"raise": C["amberLight"], "assert": C["tealLight"], "none fired": C["greenLight"]}[stmt[kind]]
    table(s, x, y, w, rows, [1.3, 4.0, 1.2, 2.3], rowh=min(0.38, h / len(rows)), fs=10, mono_cols=(0, 1, 2), cell_fill=cf)


@need(1.6)
def v_optimised(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    tb(s, x, y, 1.6, 0.4, "normal run", 11, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE)
    chip(s, x + 1.6, y, 2.2, 0.4, "assert False, 'boom'", "plain", fs=10)
    arrow(s, x + 3.85, y + 0.2, x + 4.4, y + 0.2, C["coral"], 1.8)
    chip(s, x + 4.45, y, 2.5, 0.4, ls[0], "red", fs=10)
    chip(s, x + 7.05, y, 2.0, 0.4, "'reached' never printed", "grey", fs=9, mono=False)
    tb(s, x, y + 0.75, 1.6, 0.4, "python -O", 11, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE)
    chip(s, x + 1.6, y + 0.75, 2.2, 0.4, "assert removed", "grey", fs=10)
    arrow(s, x + 3.85, y + 0.95, x + 4.4, y + 0.95, C["green"], 1.8)
    chip(s, x + 4.45, y + 0.75, 2.5, 0.4, "prints " + repr(ls[1]), "green", fs=10)
    chip(s, x + 7.05, y + 0.75, 2.0, 0.4, "__debug__ is " + ls[2], "amber", fs=9.5)


# ------------------------------------------------------------------ part 3
@need(1.7)
def v_levels(s, x, y, w, h, ns, out):
    pairs = ast.literal_eval(lines_of(out)[0])
    chart(s, "col", x, y, w * 0.5, h, [n for n, _ in pairs], [("level number", [v for _, v in pairs])], fs=9, legend=False, gap=50, vmax=60, major=10)
    use = {"DEBUG": "details for the programmer", "INFO": "the program works as planned", "WARNING": "something unexpected (default)", "ERROR": "a part of the work failed", "CRITICAL": "the program may not go on"}
    rows = [["Call", "Number", "Typical use"]] + [["logging.%s()" % n.lower(), str(v), use[n]] for n, v in pairs]
    table(s, x + w * 0.53, y + 0.05, w * 0.47, rows, [1.55, 0.6, 2.2], rowh=min(0.3, (h - 0.05) / len(rows)), fs=9, mono_cols=(0,), align_cols={1: PP_ALIGN.CENTER})


def shown_at(threshold):
    """number of the five messages that a logger with this threshold lets through (a private logger and a private stream)"""
    buf = io.StringIO()
    lg = logging.getLogger("deck.shown.%d" % threshold)
    lg.handlers.clear()
    lg.propagate = False
    lg.setLevel(threshold)
    hd = logging.StreamHandler(buf)
    lg.addHandler(hd)
    for n in ("debug", "info", "warning", "error", "critical"):
        getattr(lg, n)(n)
    return len([l for l in buf.getvalue().split("\n") if l])


@need(1.7)
def v_threshold(s, x, y, w, h, ns, out):
    names = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    counts = [shown_at(getattr(logging, n)) for n in names]
    tb(s, x, y, w * 0.45, 0.24, "messages shown at each threshold", 10, C["teal"], bold=True)
    chart(s, "col", x, y + 0.26, w * 0.45, h - 0.26, names, [("messages shown", counts)], fs=9, legend=False, gap=50, vmax=6, major=1)
    ls = lines_of(out)
    rows = [["Printed at threshold INFO"]] + [[l] for l in ls]
    cc = {(i, 0): (C["coral"] if l.startswith(("ERROR", "CRITICAL")) else C["ink"]) for i, l in enumerate(ls, 1)}
    table(s, x + w * 0.5, y + 0.05, w * 0.5, rows, [1], rowh=min(0.3, (h - 0.05) / len(rows)), fs=10, mono_cols=(0,), cell_color=cc)


@need(1.5)
def v_format(s, x, y, w, h, ns, out):
    line = out.strip()
    parts = line.split(" - ", 2)
    fields = ["%(asctime)s", "%(levelname)s", "%(message)s"]
    cw = 2.85
    for i, (f_, p_) in enumerate(zip(fields, parts)):
        xx = x + i * (cw + 0.28)
        chip(s, xx, y, cw, 0.38, f_, "teal", fs=11)
        arrow(s, xx + cw / 2, y + 0.4, xx + cw / 2, y + 0.82, C["teal"], 1.6)
        chip(s, xx, y + 0.85, cw, 0.38, p_, "amber", fs=11)
    tb(s, x, y + 1.3, w, 0.3, "one log line: " + line, 10.5, C["muted"], italic=True, font=MONO)


@need(1.6)
def v_tofile(s, x, y, w, h, ns, out):
    chip(s, x, y, 2.2, 0.5, "logging.debug() and logging.critical()", "teal", fs=9, mono=False)
    arrow(s, x + 2.25, y + 0.25, x + 3.0, y + 0.25, C["green"], 2.0)
    chip(s, x + 3.05, y, 2.1, 0.5, "myProgramLog.txt", "green", fs=10.5)
    chip(s, x, y + 0.75, 2.2, 0.4, "the screen: nothing", "grey", fs=10, mono=False)
    tb(s, x, y + 1.2, 5.1, 0.3, "the messages go to the file, not to the screen", 10, C["muted"], italic=True)
    ls = lines_of(out)
    rows = [["Line", "Level", "Message"]] + [[str(i), l.split(" - ", 1)[0], l.split(" - ", 1)[1]] for i, l in enumerate(ls, 1)]
    table(s, x + 5.5, y, w - 5.5, rows, [0.5, 1.1, 1.9], rowh=0.34, fs=10, mono_cols=(1, 2), align_cols={0: PP_ALIGN.CENTER})


@need(1.6)
def v_disable(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    steps = [("critical('before disable')", "CRITICAL - before disable"), ("disable(CRITICAL), then critical(...)", "CRITICAL - after disable"),
             ("error('after disable')", "ERROR - after disable"), ("disable(NOTSET), then error(...)", "ERROR - after re-enabling")]
    rows = [["Call", "Printed?"]]
    cf = {}
    for i, (c_, expect) in enumerate(steps, 1):
        shown = expect in ls
        rows.append([c_, "printed" if shown else "silent"])
        cf[(i, 1)] = C["greenLight"] if shown else C["grey"]
    table(s, x, y, w * 0.6, rows, [3.5, 1.4], rowh=min(0.32, h / len(rows)), fs=10, mono_cols=(0,), cell_fill=cf)
    chip(s, x + w * 0.64, y, 3.2, 0.34, "%d of 4 calls printed" % sum(1 for _, e in steps if e in ls), "amber", fs=10.5, mono=False)
    tb(s, x + w * 0.64, y + 0.45, 3.3, 0.9, "disable(CRITICAL) silences everything up to CRITICAL, so even the error call stays quiet until NOTSET.", 10, C["muted"], italic=True)


@need(1.5)
def v_lazy(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    vals = [int(l.split(":")[1]) for l in ls]
    lazy, fstr = vals[0], vals[1] - vals[0]
    tb(s, x, y, w, 0.24, "calls of __str__ while a DEBUG message is below the threshold", 10, C["teal"], bold=True)
    chart(s, "col", x, y + 0.3, w, 1.9, ["arguments: log.debug('..%s', obj)", "f-string: log.debug(f'..')"], [("__str__ calls", [lazy, fstr])], fs=9, legend=False, gap=60, vmax=2, major=1)
    rows = [["Style", "Text built?", "__str__ calls"], ["arguments", "no", str(lazy)], ["f-string", "yes", str(fstr)]]
    table(s, x, y + 2.35, w, rows, [1.6, 1.5, 1.7], rowh=0.34, fs=10.5, align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER}, cell_fill={(1, 2): C["greenLight"], (2, 2): C["amberLight"]})


# ------------------------------------------------------------------ part 4
def log_pairs(out):
    res = []
    for l in lines_of(out):
        m = re.match(r"DEBUG - i is (\d+), total is (\d+)", l)
        if m:
            res.append((int(m.group(1)), int(m.group(2))))
    return res


def factorial_visual(s, x, y, w, h, out, bad):
    pairs = log_pairs(out)
    result = lines_of(out)[-1]
    tb(s, x, y, w, 0.24, "total after each step of the loop", 10, C["teal"], bold=True)
    chart(s, "col", x, y + 0.26, w, 1.65, ["i = %d" % i for i, _ in pairs], [("total after the step", [t for _, t in pairs])], fs=9, legend=False, gap=50, vmax=8, major=2)
    rows = [["i", "total", "log line"]] + [[str(i), str(t), "i is %d, total is %d" % (i, t)] for i, t in pairs]
    cc = {(k, 1): (C["coral"] if t == 0 else C["green"]) for k, (i, t) in enumerate(pairs, 1)}
    ty = y + 2.0
    table(s, x, ty, w, rows, [0.4, 0.7, 2.6], rowh=0.27, fs=9.5, mono_cols=(0, 1, 2), cell_color=cc, align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})
    chip(s, x, ty + 0.27 * len(rows) + 0.1, w, 0.3, "factorial(3) printed %s%s" % (result, "  (should be 6)" if bad else "  (correct)"), "red" if bad else "green", fs=10)


@need(1.8)
def v_factorialbug(s, x, y, w, h, ns, out):
    factorial_visual(s, x, y, w, h, out, True)


@need(1.8)
def v_factorialfix(s, x, y, w, h, ns, out):
    factorial_visual(s, x, y, w, h, out, False)


@need(1.5)
def v_addingbug(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    wrong = int(ls[0].split()[-1])
    right = int(ls[1].split()[-1])
    rows = [["Variable", "Value", "Type"]] + [[n, repr(ns[n]), type(ns[n]).__name__] for n in ("first", "second", "third")]
    table(s, x, y, w * 0.45, rows, [1.3, 1.2, 1.0], rowh=min(0.34, h / 4), fs=10.5, mono_cols=(0, 1, 2), cell_fill={(i, 2): C["amberLight"] for i in (1, 2, 3)})
    tb(s, x + w * 0.5, y, w * 0.5, 0.24, "the sum that was printed", 10, C["teal"], bold=True)
    chart(s, "col", x + w * 0.5, y + 0.26, w * 0.5, h - 0.26, ["'5' + '3' + '42'", "int sum"], [("printed sum", [wrong, right])], fs=9, legend=False, gap=60, vmax=6500, major=2000)


@need(1.7)
def v_cointossbug(s, x, y, w, h, ns, out):
    toss, guess = ns["toss"], ns["guess"]
    chip(s, x, y, 2.3, 0.42, "toss = %r  (%s)" % (toss, type(toss).__name__), "teal", fs=10.5)
    chip(s, x + 3.3, y, 2.6, 0.42, "guess = %r  (%s)" % (guess, type(guess).__name__), "amber", fs=10.5)
    arrow(s, x + 2.35, y + 0.21, x + 3.25, y + 0.21, C["muted"], 1.6)
    tb(s, x + 2.4, y - 0.02, 0.8, 0.2, "==", 11, C["muted"], bold=True, align=PP_ALIGN.CENTER, font=MONO, margin=(0, 0))
    chip(s, x + 6.0, y, 1.6, 0.42, "False", "red", fs=12)
    rows = [["toss", "guess", "toss == guess"]]
    cc = {}
    k = 0
    for t_ in (0, 1):
        for g_ in ("tails", "heads"):
            k += 1
            rows.append([repr(t_), repr(g_), str(t_ == g_)])
            cc[(k, 2)] = C["coral"]
    table(s, x, y + 0.6, w * 0.5, rows, [1.0, 1.4, 1.8], rowh=min(0.26, (h - 0.6) / len(rows)), fs=10, mono_cols=(0, 1, 2), cell_color=cc, align_cols={2: PP_ALIGN.CENTER})
    ls = lines_of(out)
    rows2 = [["g", "g not in ('heads', 'tails')"]] + [[l.split(" not in tuple: ")[0], l.split(": ")[-1]] for l in ls[2:]]
    table(s, x + w * 0.55, y + 0.6, w * 0.45, rows2, [0.9, 3.2], rowh=min(0.26, (h - 0.6) / len(rows2)), fs=10, mono_cols=(0, 1), cell_fill={(3, 1): C["amberLight"]})


@need(1.5)
def v_cointossfix(s, x, y, w, h, ns, out):
    ls = lines_of(out)[0].split()
    buggy, fixed = int(ls[2]), int(ls[5])
    tb(s, x, y, w * 0.55, 0.24, "wins out of 1000 tosses, always guessing heads", 10, C["teal"], bold=True)
    chart(s, "col", x, y + 0.26, w * 0.55, h - 0.26, ["buggy: toss == guess", "fixed: word == guess"], [("wins", [buggy, fixed])], fs=9, legend=False, gap=60, vmax=600, major=200)
    chip(s, x + w * 0.6, y + 0.2, w * 0.4, 0.4, "buggy wins: %d" % buggy, "red", fs=11, mono=False)
    chip(s, x + w * 0.6, y + 0.75, w * 0.4, 0.4, "fixed wins: %d" % fixed, "green", fs=11, mono=False)
    tb(s, x + w * 0.6, y + 1.25, w * 0.4, 0.3, "about half: a fair coin", 10, C["muted"], italic=True)


# ------------------------------------------------------------------ part 5
@need(1.2)
def v_stepper(s, x, y, w, h, ns, out):
    steps = [ast.literal_eval(l) for l in lines_of(out)]
    rows = [["Pause", "In", "Inspector pane"]]
    cf = {}
    for i, (name, loc) in enumerate(steps, 1):
        rows.append([str(i), name, ", ".join("%s=%s" % kv for kv in loc.items()) or "(nothing yet)"])
        cf[(i, 1)] = C["tealLight"] if name == "main" else C["amberLight"]
    table(s, x, y, w, rows, [0.5, 0.7, 2.4], rowh=min(0.42, h / len(rows)), fs=9.5, mono_cols=(1, 2), cell_fill=cf, align_cols={0: PP_ALIGN.CENTER})


@need(1.8)
def v_breakpointfn(s, x, y, w, h, ns, out):
    ls = lines_of(out)
    avail = ast.literal_eval(ls[2])
    pairs = [("Continue", "continue"), ("Step In", "step"), ("Step Over", "next"), ("Step Out", "return"), ("breakpoint", "break"), ("call stack", "where")]
    rows = [["Control of the editor", "pdb command", "In this Python?"]]
    for lab, cmd in pairs:
        rows.append([lab, cmd, "yes" if cmd in avail else "no"])
    table(s, x, y, w * 0.55, rows, [2.2, 1.6, 1.5], rowh=min(0.27, h / len(rows)), fs=10, mono_cols=(1,), cell_fill={(i, 2): C["greenLight"] for i in range(1, len(rows))}, align_cols={2: PP_ALIGN.CENTER})
    chip(s, x + w * 0.6, y, 3.5, 0.34, ls[0], "amber", fs=10)
    chip(s, x + w * 0.6, y + 0.5, 3.5, 0.34, "hook name: " + repr(ls[1]), "teal", fs=9.5)
    tb(s, x + w * 0.6, y + 0.95, 3.5, 0.6, "Stop has no pdb command of its own: quit leaves the debugger.", 10, C["muted"], italic=True)


VISUALS = {"boxprint": v_boxprint, "exceptionobj": v_exceptionobj, "unwinding": v_unwinding, "notes": v_notes, "assertfails": v_assertfails,
           "assertmsg": v_assertmsg, "optimised": v_optimised, "levels": v_levels, "threshold": v_threshold, "format": v_format, "tofile": v_tofile,
           "disable": v_disable, "lazy": v_lazy, "factorialbug": v_factorialbug, "factorialfix": v_factorialfix, "addingbug": v_addingbug,
           "cointossbug": v_cointossbug, "cointossfix": v_cointossfix, "stepper": v_stepper, "breakpointfn": v_breakpointfn}
