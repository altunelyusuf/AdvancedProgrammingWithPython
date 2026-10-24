"""Chapter 9 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from a run of the example's own patterns (the namespace `ns`
and the printed text `out` that deck_build_v2_0_0.py passes in, or the same pattern re-run here on the same text); nothing is
typed in by hand except the plain-language names of columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg


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
                  "red": (C["redLight"], C["ink"])}.get(fills.get(i), (C["card"], C["ink"]))
        label_shape(s, x + i * cw, y, cw - 0.025, ch, vis(c), f, col, size=fs, font=MONO, line=C["line"], radius=0.1)
        if idx and (i % 5 == 0 or cw > 0.4):
            tb(s, x + i * cw, y + ch, cw - 0.025, 0.18, str(i), label_fs, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


# ------------------------------------------------------------------ part 1
@need(1.6)
def v_manual(s, x, y, w, h, ns, out):
    msg, ok = ns["message"], ns["is_phone_number"]
    hits = [i for i in range(len(msg) - 11) if ok(msg[i:i + 12])]
    miss = [0, 5, 19]
    rows = [["Window starts at", "The 12 characters", "is_phone_number says"]]
    cc, cf = {}, {}
    for k, i in enumerate(sorted(set(hits + miss)), 1):
        v = ok(msg[i:i + 12])
        rows.append([str(i), repr(msg[i:i + 12]), str(v)])
        cc[(k, 2)] = C["green"] if v else C["coral"]
        if v:
            cf[(k, 1)] = C["greenLight"]
    table(s, x, y, w * 0.68, rows, [1.3, 2.3, 1.6], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2), cell_color=cc, cell_fill=cf)
    chart(s, "col", x + w * 0.72, y, w * 0.28, h, ["windows tried", "windows that pass"], [("windows", [len(msg) - 11, len(hits)])], fs=9, legend=False, gap=50)


@need(1.5)
def v_objects(s, x, y, w, h, ns, out):
    phone = ns["phone"]
    text = "My number is 415-555-4242."
    mo = phone.search(text)
    a, b = mo.span()
    cw = (w - 0.1) / len(text)
    fills = {i: "amber" for i in range(a, b)}
    chip(s, x, y, 3.0, 0.3, "pattern " + phone.pattern, "teal", fs=9.5)
    arrow(s, x + 3.05, y + 0.15, x + 3.45, y + 0.15, C["teal"])
    chip(s, x + 3.5, y, 2.7, 0.3, "mo = phone.search(text)", "plain", fs=9.5)
    strip(s, x, y + 0.42, text, cw, 0.38, fills, fs=11)
    yy = y + 1.05
    chip(s, x, yy, 3.0, 0.3, "mo.group() = %r" % mo.group(), "amber", fs=10)
    chip(s, x + 3.15, yy, 2.2, 0.3, "mo.span() = %s" % (mo.span(),), "amber", fs=10)
    chip(s, x + 5.5, yy, 3.6, 0.3, "no digits: %s" % phone.search("no digits here"), "grey", fs=10)

@need(1.5)
def v_matchfns(s, x, y, w, h, ns, out):
    calls = [("match", "c", "abcdef"), ("match", "a", "abcdef"), ("search", "c", "abcdef"), ("fullmatch", "p.*n", "python"), ("fullmatch", "abc", "abcdef")]
    rows = [["Function", "Pattern", "Text", "Result"]]
    cc, cf = {}, {}
    for i, (f, p, tx) in enumerate(calls, 1):
        m = getattr(re, f)(p, tx)
        rows.append([f, repr(p), repr(tx), "None" if m is None else "%r at %s" % (m.group(), m.span())])
        cc[(i, 3)] = C["coral"] if m is None else C["green"]
    table(s, x, y, w * 0.62, rows, [1.3, 1.1, 1.2, 1.9], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1, 2, 3), cell_color=cc)
    tb(s, x + w * 0.66, y, w * 0.34, 0.26, "where each function looks in 'abcdef'", 9.5, C["muted"], italic=True)
    for k, (lab, kind, cells) in enumerate([("match", "teal", [0]), ("search", "amber", list(range(6))), ("fullmatch", "green", list(range(6)))]):
        strip(s, x + w * 0.66, y + 0.35 + k * 0.4, "abcdef", 0.3, 0.28, {i: kind for i in cells}, fs=10, idx=False)
        tb(s, x + w * 0.66 + 1.85, y + 0.35 + k * 0.4, 1.2, 0.28, lab, 10, C["ink"], font=MONO, anchor=MSO_ANCHOR.MIDDLE)


# ------------------------------------------------------------------ part 2
@need(1.6)
def v_grouping(s, x, y, w, h, ns, out):
    mo = ns["mo"]
    g0, g1, g2 = mo.group(0), mo.group(1), mo.group(2)
    text = "My number is 415-555-4242."
    cw = (w - 0.1) / len(text)
    a, b = mo.span(1)
    c, d = mo.span(2)
    fills = {i: "teal" for i in range(a, b)}
    fills.update({i: "amber" for i in range(c, d)})
    fills.update({i: "grey" for i in range(b, c)})
    strip(s, x, y + 0.9, text, cw, 0.36, fills, fs=11, idx=False)
    chip(s, x + b * cw - 2.05, y + 0.45, 2.0, 0.3, "group(1) = %r" % g1, "teal", fs=10)
    chip(s, x + c * cw + 0.1, y + 0.45, 2.4, 0.3, "group(2) = %r" % g2, "amber", fs=10)
    arrow(s, x + (a + b) / 2 * cw, y + 0.77, x + (a + b) / 2 * cw, y + 0.89, C["teal"], 1.2)
    arrow(s, x + (c + d) / 2 * cw, y + 0.77, x + (c + d) / 2 * cw, y + 0.89, C["amber"], 1.2)
    chip(s, x, y, 4.2, 0.32, "group(0) = %r   the whole match" % g0, "plain", fs=10)
    chip(s, x + 4.4, y, 4.7, 0.32, "groups() = %s" % (mo.groups(),), "plain", fs=10)


@need(1.5)
def v_alternation(s, x, y, w, h, ns, out):
    m = re.search(r"Cat(erpillar|astrophe|ch|egory)", "Catch me if you can.")
    alts = ["erpillar", "astrophe", "ch", "egory"]
    rows = [["Alternative after Cat", "Fits 'Catch me...'?"]] + [[a_, str(m.group(1) == a_)] for a_ in alts]
    cc = {(i + 1, 1): (C["green"] if m.group(1) == a_ else C["greyTxt"]) for i, a_ in enumerate(alts)}
    cf = {(i + 1, 1): C["greenLight"] for i, a_ in enumerate(alts) if m.group(1) == a_}
    table(s, x, y, w * 0.55, rows, [2.3, 2.3], rowh=min(0.3, h / 6), mono_cols=(0, 1), cell_color=cc, cell_fill=cf)
    m2 = re.search(r"(Cat|Dog)s?", "Dogs bark")
    chip(s, x + w * 0.6, y, 3.5, 0.32, "whole match: %r" % m.group(), "amber", fs=10)
    chip(s, x + w * 0.6, y + 0.45, 3.5, 0.32, "group(1): %r" % m.group(1), "teal", fs=10)
    chip(s, x + w * 0.6, y + 0.9, 3.5, 0.32, "(Cat|Dog)s? on 'Dogs bark': %r" % m2.group(), "plain", fs=9)


@need(1.5)
def v_named(s, x, y, w, h, ns, out):
    mo = ns["mo"]
    rows = [["Group name", "Text it holds"]] + [[k, repr(v)] for k, v in mo.groupdict().items()]
    table(s, x, y, 3.7, rows, [1.6, 2.1], rowh=0.34, mono_cols=(0, 1))
    text = "this is is a typo"
    m = re.search(r"\b(\w+) \1\b", text)
    a, b = m.span()
    cw = 0.3
    xs = x + 4.1
    strip(s, xs, y + 0.45, text, cw, 0.36, {i: "amber" for i in range(a, b)}, fs=11)
    chip(s, xs, y, 5.1, 0.3, r"\b(\w+) \1\b  finds %r at %s" % (m.group(), m.span()), "amber", fs=9.5)
    chip(s, xs + 0.2, y + 1.15, 2.0, 0.28, "group 1 = %r" % m.group(1), "teal", fs=9)
    arrow(s, xs + 0.2 + 0.3, y + 1.15, xs + 5 * cw + cw / 2, y + 0.45 + 0.36 + 0.2, C["teal"], 1.2)


@need(1.5)
def v_charsets(s, x, y, w, h, ns, out):
    text = ns["text"]
    sets = [r"[aeiouAEIOU]", r"[^aeiouAEIOU]"]
    rows = [["Pattern", "What findall returns", "Count"]]
    cnt = []
    for p in sets:
        r = re.findall(p, text)
        cnt.append(len(r))
        rows.append([p, str(r) if len(r) < 9 else "%d characters" % len(r), str(len(r))])
    table(s, x, y, w * 0.66, rows, [1.8, 3.9, 0.7], rowh=0.3, mono_cols=(0, 1), align_cols={2: PP_ALIGN.CENTER})
    strip(s, x, y + 1.05, text, 0.27, 0.3, {i: ("amber" if c in "aeiouAEIOU" else "teal") for i, c in enumerate(text)}, fs=9.5, idx=False)
    tb(s, x, y + 1.38, w, 0.26, "amber: found by the first set    teal: found by the second set", 10, C["muted"], italic=True)
    chart(s, "bar", x + w * 0.69, y, w * 0.31, 1.35, ["[aeiou]", "[^aeiou]"][::-1], [("matches", cnt[::-1])], fs=9, legend=False, gap=40)


@need(1.4)
def v_shorthand(s, x, y, w, h, ns, out):
    tests = [(r"\d+\s\w+", "12 drummers, 11 pipers, 10 lords"), (r".at", "The cat in the hat sat on the flat mat.")]
    rows = [["Pattern", "What findall returns", "Count"]]
    for p, tx in tests:
        r = re.findall(p, tx)
        rows.append([p, str(r), str(len(r))])
    table(s, x, y, w * 0.66, rows, [1.3, 4.6, 0.6], rowh=0.34, fs=10, mono_cols=(0, 1), align_cols={2: PP_ALIGN.CENTER})
    rows2 = [["Class", "Means"], [r"\d", "a digit"], [r"\w", "a letter, digit or _"], [r"\s", "a blank or line break"], [".", "any one character"]]
    table(s, x + w * 0.69, y, w * 0.31, rows2, [0.7, 2.2], rowh=0.28, fs=9.5, mono_cols=(0,))
    chart(s, "col", x, y + 1.15, w * 0.4, 1.0, [r"\d+\s\w+", ".at"], [("matches", [3, 5])], fs=9, legend=False, gap=60) if False else None


# ------------------------------------------------------------------ part 3
@need(1.5)
def v_repetition(s, x, y, w, h, ns, out):
    tests = [(r"42!?", "42"), (r"42!?", "42!"), (r"Eggs( and spam)*", "Eggs and spam and spam"), (r"Eggs( and spam)+", "Eggs")]
    rows = [["Pattern", "Text", "Result"]]
    cc = {}
    for i, (p, tx) in enumerate(tests, 1):
        m = re.search(p, tx)
        rows.append([p, repr(tx), "no match" if m is None else ("span %s" % (m.span(),) if len(m.group()) > 8 else "%r at %s" % (m.group(), m.span()))])
        cc[(i, 2)] = C["coral"] if m is None else C["green"]
    table(s, x, y, w * 0.68, rows, [1.8, 2.6, 2.0], rowh=min(0.32, h / len(rows)), mono_cols=(0, 1, 2), cell_color=cc)
    rows2 = [["Symbol", "Times"], ["?", "0 or 1"], ["*", "0 or more"], ["+", "1 or more"]]
    table(s, x + w * 0.71, y, w * 0.29, rows2, [0.8, 1.6], rowh=0.34, mono_cols=(0,))

@need(1.5)
def v_counts(s, x, y, w, h, ns, out):
    tests = [(r"(Ha){3,5}", "HaHaHaHa", "fullmatch"), (r"(Ha){3}", "HaHaHaHa", "fullmatch")]
    rows = [["Pattern", "Text", "Call", "Fits?"]]
    cc = {}
    for i, (p, tx, f) in enumerate(tests, 1):
        m = getattr(re, f)(p, tx)
        rows.append([p, repr(tx), f, str(m is not None)])
        cc[(i, 3)] = C["green"] if m else C["coral"]
    table(s, x, y, w * 0.6, rows, [1.5, 1.7, 1.3, 0.9], rowh=0.34, mono_cols=(0, 1, 2, 3), cell_color=cc)
    text = "1 22 333 4444 55555"
    found = re.findall(r"\d{2,4}", text)
    toks = text.split()
    chart(s, "col", x + w * 0.64, y, w * 0.36, h, toks, [("digits taken by \\d{2,4}", [len(re.fullmatch(r"\d{2,4}", t_) and t_ or (re.match(r"\d{2,4}", t_) or [""])[0]) for t_ in toks])], fs=9, legend=False, gap=50, vmax=5, major=1)
    tb(s, x, y + 1.15, w * 0.6, 0.5, "findall(r'\\d{2,4}') returns %s" % found, 10.5, C["muted"], italic=True)


@need(1.7)
def v_greedy(s, x, y, w, h, ns, out):
    tests = [(r"(Ha){3,5}", "HaHaHaHaHa", "greedy"), (r"(Ha){3,5}?", "HaHaHaHaHa", "lazy"), (r"<.*?>", "<To serve man> for dinner.>", "lazy"), (r"<.*>", "<To serve man> for dinner.>", "greedy")]
    res = [re.search(p, t).group() for p, t, _ in tests]
    chart(s, "col", x, y, w * 0.5, h, ["(Ha){3,5}", "(Ha){3,5}?", "<.*?>", "<.*>"], [("characters matched", [len(r) for r in res])], fs=9, legend=False, gap=50, vmax=30)
    rows = [["Pattern", "Kind", "It took"]] + [[p, k, short(r, 24)] for (p, t, k), r in zip(tests, res)]
    cf = {(i + 1, 1): (C["amberLight"] if k == "greedy" else C["tealLight"]) for i, (_, _, k) in enumerate(tests)}
    table(s, x + w * 0.53, y + 0.1, w * 0.47, rows, [1.5, 0.8, 2.0], rowh=min(0.36, (h - 0.1) / len(rows)), mono_cols=(0, 2), cell_fill=cf)


@need(1.4)
def v_anchors(s, x, y, w, h, ns, out):
    tests = ["1234567890", "12345xyz67890"]
    rows = [["Pattern", "Text", "Result"]]
    cc = {}
    for i, tx in enumerate(tests, 1):
        m = re.search(r"^\d+$", tx)
        rows.append([r"^\d+$", tx, "no match" if m is None else "match at %s" % (m.span(),)])
        cc[(i, 2)] = C["coral"] if m is None else C["green"]
    table(s, x, y, w * 0.58, rows, [1.1, 2.2, 1.9], rowh=0.32, mono_cols=(0, 1, 2), cell_color=cc)
    t_ = "12345xyz67890"
    xs = x + w * 0.62
    strip(s, xs, y, t_, 0.27, 0.32, {i: ("green" if c.isdigit() else "red") for i, c in enumerate(t_)}, fs=9.5, idx=False)
    tb(s, xs, y + 0.36, 3.5, 0.4, "the letters xyz break the run of digits, so the whole text cannot match", 9.5, C["muted"], italic=True)
    rows2 = [["Anchor", "Where it holds"], ["^", "at the start of the text"], ["$", "at the end, or before a final newline"], ["\\b", "at the edge of a word"], ["\\B", "anywhere that is not a word edge"]]
    table(s, x, y + 1.15, w * 0.58, rows2, [1.0, 4.2], rowh=0.25, fs=10, mono_cols=(0,)) if h > 2.2 else None


@need(1.5)
def v_boundaries(s, x, y, w, h, ns, out):
    t1 = "The cat found a catapult catalog in the catacombs."
    found = re.findall(r"\bcat\w*", t1)
    rows = [["Pattern", "Text", "Result"], [r"\bcat\w*", "The cat found a catapult ...", str(found)], [r"\Bcat\B", "certificate", str(re.findall(r"\Bcat\B", "certificate"))]]
    table(s, x, y, w * 0.68, rows, [1.2, 2.3, 3.2], rowh=0.4, fs=10, mono_cols=(0, 1, 2), cell_color={(1, 2): C["green"], (2, 2): C["green"]})
    t = "certificate"
    m = re.search(r"\Bcat\B", t)
    chip(s, x + w * 0.71, y, 2.6, 0.28, "inside a word: no edge", "amber", fs=9, mono=False)
    strip(s, x + w * 0.71, y + 0.38, t, 0.26, 0.34, {i: "amber" for i in range(*m.span())}, fs=10, idx=False)


@need(1.5)
def v_lookaround(s, x, y, w, h, ns, out):
    cases = [(r"\d+(?= dollars)", "5 dollars and 7 euros", "ahead"), (r"(?<=\$)\d+", "cost $30 or 40", "behind")]
    for k, (p, t, kind) in enumerate(cases):
        yy = y + k * 0.95
        m = re.search(p, t)
        a, b = m.span()
        fills = {i: "amber" for i in range(a, b)}
        if kind == "ahead":
            fills.update({i: "teal" for i in range(b, b + len(" dollars"))})
        else:
            fills.update({i: "teal" for i in range(a - 1, a)})
        strip(s, x, yy + 0.32, t, 0.33, 0.36, fills, fs=11)
        chip(s, x, yy, 3.4, 0.28, p, "plain", fs=9.5)
        res = re.findall(p, t)
        chip(s, x + 7.2, yy + 0.34, 2.0, 0.32, "returns " + str(res), "amber", fs=10)
        arrow(s, x + 6.95, yy + 0.5, x + 7.15, yy + 0.5, C["amber"])
    tb(s, x + 3.6, y, 5.5, 0.28, "amber: returned    teal: only checked, not taken", 10, C["muted"], italic=True)


# ------------------------------------------------------------------ part 4
@need(1.7)
def v_findall(s, x, y, w, h, ns, out):
    tests = [(r"\d{3}-\d{3}-\d{4}", "Cell: 415-555-9999 Work: 212-555-0000"), (r"(\w+)=(\d+)", "set width=20 and height=10"), (r"\d{3}", "123456")]
    rows = [["Pattern", "Groups in it", "What findall returns", "Item type"]]
    for p, t in tests:
        r = re.findall(p, t)
        rows.append([p, str(re.compile(p).groups), str(r), type(r[0]).__name__])
    rh = min(0.34, (h - 0.6) / len(rows))
    table(s, x, y, w, rows, [2.4, 1.2, 4.5, 1.1], rowh=rh, mono_cols=(0, 2, 3), align_cols={1: PP_ALIGN.CENTER})
    yy = y + rh * len(rows) + 0.15
    strip(s, x, yy, "123456", 0.42, 0.34, {0: "teal", 1: "teal", 2: "teal", 3: "amber", 4: "amber", 5: "amber"}, fs=12, idx=False)
    tb(s, x + 2.7, yy, 6.4, 0.34, "no overlap: the second match starts after the first ends", 10.5, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE)


@need(1.6)
def v_finditer(s, x, y, w, h, ns, out):
    text = ns["text"]
    ms = list(re.finditer(r"\w+ly\b", text))
    rows = [["start", "end", "group()"]] + [[str(m.start()), str(m.end()), m.group()] for m in ms]
    table(s, x, y, w * 0.4, rows, [0.8, 0.8, 1.9], rowh=0.34, mono_cols=(0, 1, 2), align_cols={0: PP_ALIGN.CENTER, 1: PP_ALIGN.CENTER})
    parts = re.split(r",\s*", "a, b,c,   d")
    chip(s, x + w * 0.45, y, 4.9, 0.3, "re.split(r',\\s*', 'a, b,c,   d')", "plain", fs=9.5)
    for i, p in enumerate(parts):
        chip(s, x + w * 0.45 + i * 1.3, y + 0.75, 1.2, 0.36, repr(p), "teal", fs=11)
    arrow(s, x + w * 0.45 + 2.0, y + 0.32, x + w * 0.45 + 2.0, y + 0.72, C["muted"], 1.2)
    chart(s, "col", x + w * 0.45, y + 1.2, w * 0.55, max(0.6, h - 1.2), [m.group() for m in ms], [("characters", [len(m.group()) for m in ms])], fs=9, legend=False, gap=60, vmax=12) if h > 1.9 else None


def word_row(s, x, y, words, kinds, cw=1.5, h=0.34, fs=10):
    for i, (wd, k) in enumerate(zip(words, kinds)):
        chip(s, x + i * (cw + 0.05), y, cw, h, wd, k, fs=fs)


@need(1.6)
def v_sub(s, x, y, w, h, ns, out):
    text = ns["text"]
    words = text.split()
    kinds = ["amber" if i in (0, 1, 3, 4) else "plain" for i in range(len(words))]
    r1 = re.sub(r"Agent \w+", "CENSORED", text)
    r2 = re.sub(r"Agent (\w)\w*", r"\1****", text)
    cw = 1.45
    tb(s, x, y, 2.2, 0.22, "original", 9.5, C["muted"], italic=True)
    word_row(s, x, y + 0.2, words, kinds, cw, h=0.3)
    for j, (res, lab) in enumerate([(r1, "sub(r'Agent \\w+', 'CENSORED', text)"), (r2, "sub(r'Agent (\\w)\\w*', r'\\1****', text)")]):
        yy = y + 0.55 + j * 0.6
        tb(s, x + 0.75, yy, 7.0, 0.2, lab, 8.5, C["muted"], font=MONO)
        arrow(s, x + 0.45, yy - 0.02, x + 0.45, yy + 0.22, C["muted"], 1.2)
        rw = res.split()
        word_row(s, x, yy + 0.21, rw, ["teal" if ("CENSORED" in q or "****" in q) else "plain" for q in rw], cw if len(rw) > 3 else cw * 1.6, h=0.3)


@need(1.7)
def v_subfunc(s, x, y, w, h, ns, out):
    t = "3 cats 12 dogs"
    nums = re.findall(r"\d+", t)
    for i, n in enumerate(nums):
        yy = y + i * 0.52
        chip(s, x, yy, 0.8, 0.38, n, "amber", fs=12)
        arrow(s, x + 0.85, yy + 0.19, x + 1.45, yy + 0.19, C["muted"])
        chip(s, x + 1.5, yy, 2.0, 0.38, "int(...) * 2", "plain", fs=10)
        arrow(s, x + 3.55, yy + 0.19, x + 4.15, yy + 0.19, C["muted"])
        chip(s, x + 4.2, yy, 0.8, 0.38, str(int(n) * 2), "green", fs=12)
    chip(s, x, y + 1.1, 5.0, 0.32, "result: " + re.sub(r"\d+", lambda m: str(int(m.group()) * 2), t), "teal", fs=10.5)
    rows = [["Call", "Gives"], ["re.escape('a.b*c')", repr(re.escape("a.b*c"))], ["re.subn('a', 'b', 'banana')", repr(re.subn("a", "b", "banana"))]]
    table(s, x + 5.3, y, w - 5.3, rows, [2.7, 1.5], rowh=0.4, fs=10, mono_cols=(0, 1))


@need(1.6)
def v_flags(s, x, y, w, h, ns, out):
    text = ns["text"]
    r1, r2, r3 = re.search("robocop", "ROBOCOP protects", re.I).group(), re.search(".*", text).group(), re.search(".*", text, re.DOTALL).group()
    chart(s, "col", x, y, w * 0.45, h, ["re.I", "dot only", "re.DOTALL"], [("characters matched", [len(r1), len(r2), len(r3)])], fs=9, legend=False, gap=50, vmax=55)
    rows = [["Call", "Matched"], ["'robocop', re.I", repr(r1)], ["'.*', no DOTALL", repr(short(r2, 24))], ["'.*', re.DOTALL", repr(short(r3, 24))]]
    table(s, x + w * 0.48, y + 0.1, w * 0.52, rows, [2.0, 2.7], rowh=min(0.36, (h - 0.1) / 4), mono_cols=(0, 1))


@need(1.5)
def v_verbose(s, x, y, w, h, ns, out):
    pat = ns["pattern"]
    lines = pat.split("\n")
    for i, ln in enumerate(lines):
        chip(s, x, y + i * 0.45, 3.8, 0.38, ln, "teal", fs=11)
    clean = "".join(re.sub(r"#.*", "", ln).replace(" ", "") for ln in lines)
    arrow(s, x + 3.95, y + 0.42, x + 4.6, y + 0.42, C["amber"], 2)
    chip(s, x + 4.7, y + 0.2, 2.4, 0.44, clean, "amber", fs=13)
    tb(s, x + 4.7, y + 0.72, 3.4, 0.4, "what the engine reads: the blanks and the comments are dropped", 10, C["muted"], italic=True)
    m = re.search(pat, "415-5551", re.VERBOSE)
    chip(s, x, y + 1.05, 3.8, 0.32, "match: %r at %s" % (m.group(), m.span()), "green", fs=10.5)

@need(1.5)
def v_combined(s, x, y, w, h, ns, out):
    both = ns["both"]
    flags = [("re.I", re.I, "ignore case"), ("re.S", re.S, "dot crosses a line break"), ("re.X", re.X, "blanks and comments ignored")]
    rows = [["Flag", "Value", "Effect"]] + [[n, str(int(f)), e] for n, f, e in flags] + [["re.I | re.S | re.X", str(int(both)), "all three at once"]]
    table(s, x, y, w * 0.62, rows, [1.9, 0.8, 2.9], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1), align_cols={1: PP_ALIGN.CENTER})
    chart(s, "col", x + w * 0.66, y, w * 0.34, h, ["I", "S", "X", "joined"], [("flag value", [int(f) for _, f, _ in flags] + [int(both)])], fs=9, legend=False, gap=40, vmax=100)


# ------------------------------------------------------------------ part 5
@need(1.0)
def v_project3(s, x, y, w, h, ns, out):
    phone, email, text, show = ns["phone"], ns["email"], ns["text"], ns["show"]
    rows = [["Phone found in the text", "Printed"]] + [[m.group(), show(m.groups())] for m in phone.finditer(text)]
    rh = min(0.23, h / 4)
    table(s, x, y, w * 0.6, rows, [3.0, 2.3], rowh=rh, fs=9.5, mono_cols=(0, 1))
    rows2 = [["E-mail found in the text"]] + [[e] for e in email.findall(text)]
    table(s, x + w * 0.63, y, w * 0.37, rows2, [1], rowh=rh, fs=9.5, mono_cols=(0,))


@need(1.3)
def v_phonegroups(s, x, y, w, h, ns, out):
    phone = ns["phone"]
    mo = phone.search("Call 415.555.9950 ext. 123")
    names = ["whole number", "area code", "separator", "first 3 digits", "separator", "last 4 digits",
             "extension clause", "ext, x or ext.", "extension digits"]
    halves = [range(1, 6), range(6, 10)]
    for k, rg in enumerate(halves):
        rows = [["Group (item)", "What it holds", "Text it caught"]]
        cf = {}
        for n, i in enumerate(rg, 1):
            g = mo.group(i)
            rows.append(["%d (%d)" % (i, i - 1), names[i - 1], repr(g if len(g) < 12 else g[:9] + "...")])
            if i == 7:
                cf[(n, 2)] = C["redLight"]
            if i == 9:
                cf[(n, 2)] = C["amberLight"]
        table(s, x + k * (w * 0.5 + 0.05), y, w * 0.495, rows, [0.95, 1.5, 1.7], rowh=0.24, fs=9.5, mono_cols=(0, 2), cell_fill=cf, align_cols={0: PP_ALIGN.CENTER})
    tb(s, x + w * 0.5 + 0.05, y + 1.24, w * 0.495, 0.4, ["red: group 7 (item 6), the clause the book joins", "amber: group 9 (item 8), the digits only"], 9.5, C["muted"], italic=True)


@need(1.9)
def v_strongpw(s, x, y, w, h, ns, out):
    rules = ns["rules"]
    pws = list(ns["pws"])
    rows = [["Password"] + list(rules) + ["Strong"]]
    cf, cc = {}, {}
    for i, pw in enumerate(pws, 1):
        r = [bool(re.search(rule, pw)) for rule in rules]
        rows.append([pw] + [str(v) for v in r] + [str(all(r))])
        for j, v in enumerate(r + [all(r)], 1):
            if v:
                cf[(i, j)] = C["greenLight"]
            else:
                cc[(i, j)] = C["greyTxt"]
    table(s, x, y, w, rows, [2.2, 1.3, 1.3, 1.3, 1.3, 1.3], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1, 2, 3, 4), cell_fill=cf, cell_color=cc, align_cols={j: PP_ALIGN.CENTER for j in range(1, 6)})


@need(1.5)
def v_regexstrip(s, x, y, w, h, ns, out):
    rs = ns["regex_strip"]
    cases = [(("  hi there \n",), "  hi there \n".strip()), (("xyhixy", "xy"), "xyhixy".strip("xy")), (("[[a]]", "[]"), "[[a]]".strip("[]"))]
    rows = [["Input", "regex_strip gives", "str.strip gives", "Same?"]]
    cc = {}
    for i, (args, ref) in enumerate(cases, 1):
        got = rs(*args)
        rows.append([", ".join(repr(a) for a in args), repr(got), repr(ref), str(got == ref)])
        cc[(i, 3)] = C["green"] if got == ref else C["coral"]
    table(s, x, y, w, rows, [3.2, 2.0, 2.0, 1.0], rowh=min(0.4, h / len(rows)), mono_cols=(0, 1, 2, 3), cell_color=cc, align_cols={3: PP_ALIGN.CENTER})


VISUALS = {"manual": v_manual, "objects": v_objects, "matchfns": v_matchfns, "grouping": v_grouping, "alternation": v_alternation, "named": v_named,
           "charsets": v_charsets, "shorthand": v_shorthand, "repetition": v_repetition, "counts": v_counts,
           "greedy": v_greedy, "anchors": v_anchors, "boundaries": v_boundaries, "lookaround": v_lookaround, "combined": v_combined, "findall": v_findall, "finditer": v_finditer, "sub": v_sub,
           "subfunc": v_subfunc, "flags": v_flags, "verbose": v_verbose, "project3": v_project3, "phonegroups": v_phonegroups, "strongpw": v_strongpw, "regexstrip": v_regexstrip}
