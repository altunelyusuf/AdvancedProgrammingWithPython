"""Chapter 8 deck visuals, version 2.1.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from the run of the example (the namespace `ns` and the
printed text `out` that deck_build_v2_1_0.py passes in); nothing is typed in by hand except the research's own book figures
(marked as such on the slide) and the plain-language names of the columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.1.0"
import math
import re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_1_0 import C, MONO, arrow, chart, label_shape, table, tb, rect, line_seg


def vis(s):
    """what the eye sees for a character: blanks and line breaks get a visible stand-in"""
    return {" ": "·", "\n": "⏎", "\t": "⇥", "\r": "␍"}.get(s, s)


def show(t):
    return "".join(vis(c) for c in t)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def strip(s, x, y, text, cw, ch, fills=None, fs=14, idx=True, neg=True, label_fs=9):
    """A row of character cells with the index above/below; fills maps index -> (fill, text colour)."""
    fills = fills or {}
    n = len(text)
    for i, c in enumerate(text):
        f, col = fills.get(i, (C["card"], C["ink"]))
        label_shape(s, x + i * cw, y, cw - 0.03, ch, vis(c), f, col, size=fs, line=C["line"], radius=0.1)
        if idx:
            tb(s, x + i * cw, y + ch, cw - 0.03, 0.2, str(i), label_fs, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
        if neg:
            tb(s, x + i * cw, y + ch + 0.17, cw - 0.03, 0.2, str(i - n), label_fs, C["coral"], align=PP_ALIGN.CENTER, margin=(0, 0))


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=None, line=C["line"], radius=0.15)


# ------------------------------------------------------------------ part 1
@need(1.6)
def v_quotes(s, x, y, w, h, ns, out):
    lits = [("\"Alice's cat\"", "str"), ("'Bob\\'s cat'", "str"), ("b'a'", "bytes"), ("r'a'", "str")]
    rows = [["Literal you type", "Text it holds", "Length", "Type"]]
    for src, _ in lits:
        v = eval(src)
        rows.append([src, str(v), str(len(v)), type(v).__name__])
    table(s, x, y, w, rows, [3.2, 2.6, 1.0, 1.4], rowh=min(0.38, h / len(rows)), mono_cols=(0, 1))


@need(1.5)
def v_escapes(s, x, y, w, h, ns, out):
    esc = [("\\'", "apostrophe"), ('\\"', "double quote"), ("\\t", "tab"), ("\\n", "new line"), ("\\\\", "backslash")]
    rows = [["Escape"] + [e for e, _ in esc], ["Makes"] + [m for _, m in esc], ["Characters"] + [str(len(eval("'" + e + "'"))) for e, _ in esc]]
    table(s, x, y, w, rows, [1.3] + [1.5] * 5, rowh=min(0.42, h / 3), mono_cols=(), bold_cols=(0,), align_cols={j: PP_ALIGN.CENTER for j in range(1, 6)})


@need(1.7)
def v_raw(s, x, y, w, h, ns, out):
    rows = [("r'\\n'", r"\n"), ("'\\n'", "\n")]
    rh = min(0.55, (h - 0.1) / 2)
    for k, (src, val) in enumerate(rows):
        yy = y + k * (rh + 0.1)
        chip(s, x, yy, 1.5, rh, src, "teal", fs=14)
        arrow(s, x + 1.55, yy + rh / 2, x + 2.25, yy + rh / 2)
        for i, c in enumerate(val):
            chip(s, x + 2.35 + i * 0.62, yy, 0.55, rh, vis(c) if c != "\n" else "⏎", "amber" if k == 0 else "green", fs=16)
        tb(s, x + 2.5 + len(val) * 0.62, yy, 4.8, rh, "%d character%s%s" % (len(val), "" if len(val) == 1 else "s", " - the backslash is kept" if k == 0 else " - one line break"),
           12, C["ink"], anchor=MSO_ANCHOR.MIDDLE)


@need(1.75)
def v_index(s, x, y, w, h, ns, out):
    g = ns["greeting"]
    cw = 0.6
    x0 = x + (w - cw * len(g)) / 2
    picks = {0: "greeting[0]", 4: "greeting[4]", len(g) - 1: "greeting[-1]"}
    fills = {i: (C["tealLight"], C["ink"]) for i in picks}
    top = y + 0.62
    strip(s, x0, top, g, cw, 0.42, fills, fs=16)
    for i, lab in picks.items():
        cx = x0 + i * cw + cw / 2 - 0.03
        val = g[i]
        chip(s, cx - 0.85, y, 1.7, 0.3, "%s = %s" % (lab, repr(val)), "teal", fs=10)
        arrow(s, cx, y + 0.31, cx, top - 0.02, C["teal"])


@need(1.95)
def v_slice(s, x, y, w, h, ns, out):
    g = ns["greeting"]
    cw = 0.6
    x0 = x + (w - cw * len(g)) / 2
    fills = {i: (C["tealLight"], C["ink"]) for i in range(0, 5)}
    fills.update({i: (C["amberLight"], C["ink"]) for i in range(7, len(g) - 1)})
    top = y + 0.55
    strip(s, x0, top, g, cw, 0.42, fills, fs=16)
    c1 = x0 + 5 * cw / 2 - 0.03
    c2 = x0 + 9.5 * cw - 0.03
    chip(s, c1 - 1.3, y, 2.6, 0.3, "greeting[0:5] = %r" % g[0:5], "teal", fs=10)
    arrow(s, c1, y + 0.31, c1, top - 0.02, C["teal"])
    chip(s, c2 - 1.4, y, 2.8, 0.3, "greeting[7:-1] = %r" % g[7:-1], "amber", fs=10)
    arrow(s, c2, y + 0.31, c2, top - 0.02, C["amber"])
    chip(s, x0, top + 0.95, 6.6, 0.3, "greeting[::-1] = %r  (step -1 walks backwards)" % g[::-1], "grey", fs=10)


@need(1.45)
def v_in(s, x, y, w, h, ns, out):
    tests = ["'Hello' in 'Hello, World'", "'HELLO' in 'Hello, World'", "'' in 'spam'", "'cats' not in 'cats and dogs'", "name[0:7] + 'the' + name[8:12]"]
    rows = [["Expression", "Python answers"]]
    cc = {}
    for i, t in enumerate(tests, 1):
        v = eval(t, {}, {"name": ns["name"]})
        rows.append([t, repr(v)])
        if isinstance(v, bool):
            cc[(i, 1)] = C["green"] if v else C["coral"]
    table(s, x, y, w, rows, [5.2, 3.0], rowh=min(0.38, h / len(rows)), mono_cols=(0, 1), cell_color=cc)


# ------------------------------------------------------------------ part 2
@need(1.6)
def v_fstring(s, x, y, w, h, ns, out):
    tmpl = "My name is {name}. I am {age} years old."
    parts = [p for p in re.split(r"(\{[^}]*\})", tmpl) if p]
    n = len(parts)
    gap = 0.12
    cw = (w - gap * (n - 1)) / n
    yb = y + 0.95
    for i, p in enumerate(parts):
        xx = x + i * (cw + gap)
        field = p.startswith("{")
        chip(s, xx, y, cw, 0.38, p, "amber" if field else "plain", fs=11)
        val = str(eval(p[1:-1], {}, ns)) if field else p
        chip(s, xx, yb, cw, 0.38, val, "amber" if field else "plain", fs=11)
        arrow(s, xx + cw / 2, y + 0.4, xx + cw / 2, yb - 0.02, C["amber"] if field else C["muted"])
    tb(s, x, y + 0.45, 3, 0.25, "template", 9, C["muted"], italic=True)
    tb(s, x, yb + 0.42, 3, 0.25, "what is printed", 9, C["muted"], italic=True)


@need(1.7)
def v_fspec(s, x, y, w, h, ns, out):
    spec = [(3.14159, ".2f", "2 decimals"), (42, ">6", "width 6, right"), (42, "^6", "width 6, centred"), (1234567, ",", "thousands comma"), (255, "#x", "hexadecimal")]
    rows = [["Value", "After the colon", "Meaning", "Shown"]]
    for v, sp, mean in spec:
        rows.append([repr(v), sp, mean, "'" + format(v, sp) + "'"])
    rows.append(["n = 7", "= (as {n=})", "name and value", "'n=7'"])
    table(s, x, y, w, rows, [1.5, 2.0, 2.8, 2.0], rowh=min(0.38, h / len(rows)), mono_cols=(0, 1, 3))


@need(1.5)
def v_older(s, x, y, w, h, ns, out):
    name, age = ns["name"], ns["age"]
    srcs = [("f-string", "f'My name is {name}. I am {age} years old.'"), ("% operator", "'My name is %s. I am %s years old.' % (name, age)"),
            ("format()", "'My name is {}. I am {} years old.'.format(name, age)"), ("plus", "'My name is ' + name + '. I am ' + str(age) + ' years old.'")]
    vals = [eval(c) for _, c in srcs]
    rows = [["Style", "What you write", "Same text?"]]
    for (st, c), v in zip(srcs, vals):
        rows.append([st, c if len(c) < 56 else c[:53] + "...", "yes" if v == vals[0] else "no"])
    table(s, x, y, w, rows, [1.3, 6.0, 1.1], rowh=min(0.38, h / len(rows)), mono_cols=(1,), bold_cols=(0,), cell_color={(i, 2): C["green"] for i in range(1, 5)})


# ------------------------------------------------------------------ part 3
@need(1.5)
def v_case(s, x, y, w, h, ns, out):
    sx = ns["s"]
    rows = [["Call", "Python answers", "s changed?"],
            ["s.upper()", repr(sx.upper()), "no"], ["s.lower()", repr(sx.lower()), "no"],
            ["'great' == 'GREat'.lower()", repr('great' == 'GREat'.lower()), "-"], ["'straße'.casefold() == 'strasse'", repr('straße'.casefold() == 'strasse'), "-"],
            ["s (after all calls)", repr(sx), "same"]]
    table(s, x, y, w, rows, [4.2, 3.2, 1.4], rowh=min(0.38, h / len(rows)), mono_cols=(0, 1))


def matrix(s, x, y, w, h, words, methods, fs=None):
    rows = [["string"] + methods]
    cf, cc = {}, {}
    for i, wd in enumerate(words, 1):
        r = [repr(wd)]
        for j, m in enumerate(methods, 1):
            v = getattr(wd, m)()
            r.append(str(v))
            if v:
                cf[(i, j)] = C["greenLight"]
            else:
                cc[(i, j)] = C["greyTxt"]
        rows.append(r)
    table(s, x, y, w, rows, [1.7] + [1.3] * len(methods), fs=fs, rowh=min(0.38, h / len(rows)), mono_cols=(0,), cell_fill=cf, cell_color=cc,
          align_cols={j: PP_ALIGN.CENTER for j in range(1, len(methods) + 1)})


@need(1.7)
def v_chars(s, x, y, w, h, ns, out):
    matrix(s, x, y, w, h, ns["words"], ["isalpha", "isalnum", "isdecimal", "isspace"])


@need(1.7)
def v_casetests(s, x, y, w, h, ns, out):
    matrix(s, x, y, w, h, ns["words"], ["isupper", "islower", "istitle"])


@need(1.7)
def v_affixes(s, x, y, w, h, ns, out):
    rows = [("report.txt", "report", ".txt", "removesuffix('.txt')", "report"), ("test_a.py", "test_", "a.py", "removeprefix('test_')", "a.py")]
    rh = 0.36
    for k, (full, a, b, call, res) in enumerate(rows):
        yy = y + k * 0.5
        cwid = 0.2 + 0.095 * max(len(a), len(b))
        chip(s, x, yy, 1.1, rh, full, "plain", fs=10.5)
        chip(s, x + 1.2, yy, max(0.75, 0.095 * len(a) + 0.25), rh, a, "teal" if k == 0 else "red", fs=10.5)
        xx = x + 1.2 + max(0.75, 0.095 * len(a) + 0.25) + 0.05
        chip(s, xx, yy, max(0.75, 0.095 * len(b) + 0.25), rh, b, "red" if k == 0 else "teal", fs=10.5)
        arrow(s, xx + max(0.75, 0.095 * len(b) + 0.25) + 0.1, yy + rh / 2, x + 4.6, yy + rh / 2)
        tb(s, x + 4.65, yy, 2.2, rh, "." + call, 10.5, C["muted"], anchor=MSO_ANCHOR.MIDDLE)
        arrow(s, x + 6.85, yy + rh / 2, x + 7.2, yy + rh / 2)
        chip(s, x + 7.25, yy, 1.4, rh, res, "green", fs=10.5)
    chip(s, x, y + 1.05, 4.2, 0.32, "startswith('Hello') on 'Hello, world!'  ->  True", "grey", fs=9.5)
    chip(s, x + 4.4, y + 1.05, 4.2, 0.32, "'notes.txt'.endswith(('.py', '.txt'))  ->  True", "grey", fs=9.5)


@need(1.8)
def v_joinsplit(s, x, y, w, h, ns, out):
    src = [("join(...)", ", ".join(["cats", "rats", "bats"])), ("split('m')", "My name is Simon".split("m")), ("split()", "My name is Simon".split()),
           ("splitlines()", "one\r\ntwo\nthree".splitlines()), ("partition(' ')", "Monty Python".partition(" "))]
    cats = [c for c, _ in src]
    vals = [1 if isinstance(v, str) else len(v) for _, v in src]
    chart(s, "bar", x, y, w * 0.48, h, cats[::-1], [("pieces", vals[::-1])], fs=10, legend=False, gap=40, major=1)
    rows = [["Call", "Pieces"]]
    for c, v in src:
        rows.append([c, repr(v) if not isinstance(v, str) else repr(v)])
    table(s, x + w * 0.5, y + 0.05, w * 0.5, rows, [1.5, 3.4], rowh=min(0.27, (h - 0.1) / len(rows)), mono_cols=(0, 1))


@need(1.75)
def v_justify(s, x, y, w, h, ns, out):
    rows = [("'Hello'.rjust(10)", "Hello".rjust(10)), ("'Hello'.ljust(10, '-')", "Hello".ljust(10, "-")), ("'Hello'.center(20, '=')", "Hello".center(20, "="))]
    cw = 0.27
    for k, (call, val) in enumerate(rows):
        yy = y + k * 0.52
        tb(s, x, yy, 2.5, 0.38, call, 9.5, C["muted"], anchor=MSO_ANCHOR.MIDDLE)
        for i, c in enumerate(val):
            letter = c in "Hello"
            label_shape(s, x + 2.6 + i * cw, yy, cw - 0.03, 0.38, vis(c) if letter else (c if c != " " else ""), C["tealLight"] if letter else C["grey"], C["ink"], size=11, line=C["line"], radius=0.08)
        arrow(s, x + 2.6 + len(val) * cw + 0.05, yy + 0.19, x + 2.6 + len(val) * cw + 0.4, yy + 0.19)
        tb(s, x + 2.6 + len(val) * cw + 0.45, yy, 1.2, 0.38, "width %d" % len(val), 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE)


@need(1.6)
def v_strip(s, x, y, w, h, ns, out):
    sx = ns["s"]
    chart(s, "col", x, y, w * 0.6, h, ["s", "s.strip()", "s.lstrip()", "s.rstrip()"], [("characters", [len(sx), len(sx.strip()), len(sx.lstrip()), len(sx.rstrip())])], fs=10, legend=False, gap=60)
    rows = [["Call", "Left", "Right"], ["strip()", "cut", "cut"], ["lstrip()", "cut", "kept"], ["rstrip()", "kept", "cut"]]
    table(s, x + w * 0.63, y + 0.2, w * 0.37, rows, [1.4, 1, 1], rowh=0.3, mono_cols=(0,))


@need(1.75)
def v_search(s, x, y, w, h, ns, out):
    sx = ns["s"]
    cw = 0.6
    x0 = x + (w - cw * len(sx)) / 2
    hits = []
    i = sx.find("spam")
    while i != -1:
        hits.append(i)
        i = sx.find("spam", i + 1)
    fills = {}
    for hnd in hits:
        for k in range(hnd, hnd + 4):
            fills[k] = (C["amberLight"], C["ink"])
    strip(s, x0, y, sx, cw, 0.4, fills, fs=15, neg=False)
    ys = y + 0.78
    tgt = lambda i: x0 + i * cw + cw / 2 - 0.03
    chip(s, x0, ys, 2.3, 0.3, "find('spam') = %d" % sx.find("spam"), "amber", fs=10)
    arrow(s, tgt(0), ys - 0.02, tgt(0), y + 0.64, C["amber"])
    chip(s, x0 + 2.5, ys, 2.3, 0.3, "count('spam') = %d" % sx.count("spam"), "amber", fs=10)
    chip(s, x0 + 5.2, ys, 2.7, 0.3, "find('spam', 1) = %d" % sx.find("spam", 1), "amber", fs=10)
    arrow(s, tgt(10), ys - 0.02, tgt(10), y + 0.64, C["amber"])
    chip(s, x0, ys + 0.42, 6.0, 0.3, "replace('spam', 'ham', 1) -> %r" % sx.replace("spam", "ham", 1), "teal", fs=10)


# ------------------------------------------------------------------ part 4
@need(1.6)
def v_codepoints(s, x, y, w, h, ns, out):
    t = "Hello"
    chart(s, "col", x, y, w * 0.62, h, list(t), [("code point", [ord(c) for c in t])], fs=11, legend=False, gap=50, vmax=140)
    rows = [["Call", "Gives"], ["ord('A')", repr(ord("A"))], ["chr(65)", repr(chr(65))], ["chr(ord('A') + 1)", repr(chr(ord("A") + 1))], ["ord('a') - ord('A')", repr(ord("a") - ord("A"))]]
    table(s, x + w * 0.65, y + 0.1, w * 0.35, rows, [2.2, 1], rowh=0.3, mono_cols=(0, 1))


@need(1.6)
def v_encoding(s, x, y, w, h, ns, out):
    chars = "a€é"
    chart(s, "col", x, y, w * 0.55, h, list(chars), [("bytes in UTF-8", [len(c.encode("utf-8")) for c in chars])], fs=11, legend=False, gap=60, vmax=5, major=1)
    word = "café"
    cw = 0.42
    xx = x + w * 0.6
    tb(s, xx, y, 3.6, 0.25, "%r: %d characters, %d bytes" % (word, len(word), len(word.encode("utf-8"))), 10.5, C["ink"], bold=True)
    for i, c in enumerate(word):
        n = len(c.encode("utf-8"))
        label_shape(s, xx + i * 0.85, y + 0.4, 0.8, 0.4, c, C["tealLight"], C["ink"], size=14, line=C["line"], radius=0.1)
        for k, b in enumerate(c.encode("utf-8")):
            label_shape(s, xx + i * 0.85 + k * (0.8 / n), y + 1.0, 0.8 / n - 0.03, 0.34, "%02x" % b, C["amberLight"] if n > 1 else C["grey"], C["ink"], size=9.5, line=C["line"], radius=0.1)
        arrow(s, xx + i * 0.85 + 0.4, y + 0.82, xx + i * 0.85 + 0.4, y + 0.98, C["muted"], 1)


@need(1.7)
def v_bookcheck(s, x, y, w, h, ns, out):
    py = [int(v) for v in out.split()]
    chart(s, "col", x, y, w * 0.62, h, ["'Hello'.rjust(20)", "'Hello, World'.rjust(20)"], [("Book prints", [14, 9]), ("Python gives", py)], fs=10.5, gap=70, vmax=20)
    tb(s, x + w * 0.66, y + 0.2, w * 0.34, 1.4, ["Leading spaces counted.", "Book figures come from the chapter research (finding on printed outputs)."], 10.5, C["muted"], italic=True)


# ------------------------------------------------------------------ part 5
@need(1.9)
def v_alternate(s, x, y, w, h, ns, out):
    src = "Hello, world!"
    res = out.strip("\n")
    cw = 0.62
    x0 = x + (w - cw * len(src)) / 2
    for i, c in enumerate(src):
        up = res[i].isupper()
        label_shape(s, x0 + i * cw, y, cw - 0.04, 0.4, vis(c), C["card"], C["ink"], size=15, line=C["line"], radius=0.1)
        arrow(s, x0 + i * cw + cw / 2 - 0.02, y + 0.42, x0 + i * cw + cw / 2 - 0.02, y + 0.78, C["amber"] if up else C["teal"], 1.2)
        label_shape(s, x0 + i * cw, y + 0.8, cw - 0.04, 0.4, vis(res[i]), C["amberLight"] if up else C["tealLight"], C["ink"], size=15, line=C["line"], radius=0.1)
        tb(s, x0 + i * cw, y + 1.22, cw - 0.04, 0.2, str(i), 9, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
    tb(s, x, y + 1.42, w, 0.25, "even index: lower case (teal)   odd index: upper case (amber)", 10, C["muted"], align=PP_ALIGN.CENTER)


@need(1.5)
def v_piglatin(s, x, y, w, h, ns, out):
    cut, pig = ns["cut"], ns["pig"]
    rows = [["Word", "Opening consonants", "Rest", "Pig Latin"]]
    for wd in "my name is al".split():
        k = cut(wd)
        rows.append([wd, wd[:k] or "(none)", wd[k:], pig(wd)])
    table(s, x, y, w, rows, [1.2, 2.2, 1.6, 2.0], rowh=min(0.38, h / len(rows)), mono_cols=(0, 1, 2, 3))


@need(1.1)
def v_tableprinter(s, x, y, w, h, ns, out):
    table_ = ns["table"]
    rows = [list(r) for r in zip(*table_)]
    wd = ns["widths"]
    table(s, x, y, w * 0.55, rows, [wd[0], wd[1], wd[2]], rowh=min(0.38, h / len(rows)), header=False, mono_cols=(0, 1, 2),
          align_cols={0: PP_ALIGN.RIGHT, 1: PP_ALIGN.RIGHT, 2: PP_ALIGN.RIGHT})
    chart(s, "col", x + w * 0.6, y, w * 0.4, h, ["column 1", "column 2", "column 3"], [("width", list(wd))], fs=10, legend=False, gap=60, vmax=10)


@need(1.5)
def v_clipboard(s, x, y, w, h, ns, out):
    text0 = "Alice\nBob\nCarol"
    lines = text0.split("\n")
    starred = ["* " + l for l in lines]
    steps = [("paste()", repr(text0).replace("\\n", "⏎")), ("split('\\n')", repr(lines)), ("'* ' + line", repr(starred)), ("'\\n'.join(...)", repr("\n".join(starred)).replace("\\n", "⏎")), ("copy()", "back on the shelf")]
    n = len(steps)
    gap = 0.3
    cw = (w - gap * (n - 1)) / n
    for i, (a, b) in enumerate(steps):
        xx = x + i * (cw + gap)
        label_shape(s, xx, y, cw, 0.36, a, C["teal"], "FFFFFF", size=10, bold=True, radius=0.15)
        label_shape(s, xx, y + 0.45, cw, 0.95, b, C["card"], C["ink"], size=9, line=C["line"], radius=0.08)
        if i < n - 1:
            arrow(s, xx + cw + 0.02, y + 0.18, xx + cw + gap - 0.02, y + 0.18, C["amber"], 2)


VISUALS = {"quotes": v_quotes, "escapes": v_escapes, "raw": v_raw, "index": v_index, "slice": v_slice, "in": v_in, "fstring": v_fstring, "fspec": v_fspec,
           "older": v_older, "case": v_case, "chars": v_chars, "casetests": v_casetests, "affixes": v_affixes, "joinsplit": v_joinsplit,
           "justify": v_justify, "strip": v_strip, "search": v_search, "codepoints": v_codepoints, "encoding": v_encoding, "bookcheck": v_bookcheck,
           "alternate": v_alternate, "piglatin": v_piglatin, "tableprinter": v_tableprinter, "clipboard": v_clipboard}
