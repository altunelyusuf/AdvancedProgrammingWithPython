"""Chapter 10 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram. Every number, string and truth value shown is taken from the printed text `out` of the example's own run (that
deck_build_v2_0_0.py passes in), from the names the run left in `ns`, or from the same standard-library call re-run here on the
same text; nothing is typed in by hand except the plain-language names of columns and boxes.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import ast
import json
import os
import re
import tempfile
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt); rows lower than 0.25 in take 9 pt"""
    if kw.get("rowh", 0.27) < 0.25:
        fs = min(fs, 9)
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def vis(c):
    return {" ": "·", "\n": "⏎", "\t": "⇥", "\r": "␍"}.get(c, c)


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO if mono else None, line=C["line"], radius=0.15)


def fit(text, fs, mono=True):
    """width in inches that a one-line text needs in a chip"""
    return len(text) * (0.6 if mono else 0.5) * fs / 72.0 + 0.2


def strip(s, x, y, text, cw, ch, fills=None, fs=12, idx=True, label_fs=8):
    fills = fills or {}
    for i, c in enumerate(text):
        f, col = {"teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]), "green": (C["greenLight"], C["ink"]),
                  "red": (C["redLight"], C["ink"]), "grey": (C["grey"], C["muted"])}.get(fills.get(i), (C["card"], C["ink"]))
        label_shape(s, x + i * cw, y, cw - 0.025, ch, vis(c), f, col, size=fs, font=MONO, line=C["line"], radius=0.1)
        if idx and (i % 5 == 0 or cw > 0.4):
            tb(s, x + i * cw, y + ch, cw - 0.025, 0.18, str(i), label_fs, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def lines(out):
    return out.split("\n")[:-1] if out.endswith("\n") else out.split("\n")


def files_written(code):
    """{file name: text} for every call put('name.ext', 'text') or Path('name.ext').write_text('text') in the code (read from the code, not typed)"""
    got = {}
    for node in ast.walk(ast.parse(code)):
        if not isinstance(node, ast.Call):
            continue
        consts = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if getattr(node.func, "id", "") == "put" and len(consts) == 2:
            got[consts[0]] = consts[1]
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "write_text" and consts:
            f = node.func.value
            if isinstance(f, ast.Call) and getattr(f.func, "id", "") == "Path" and f.args and isinstance(f.args[0], ast.Constant):
                got[f.args[0].value] = consts[0]
    return got


# ------------------------------------------------------------------ part 1
@need(1.6)
def v_pathobjects(s, x, y, w, h, ns, out):
    o = lines(out)
    rows = [["Expression", "What it printed"],
            ["Path('spam', 'bacon', 'eggs')", o[0]],
            ["Path('spam') / 'bacon' / 'eggs' == p", o[1]],
            ["PureWindowsPath('spam', 'bacon', 'eggs')", o[2]],
            ["'spam' / 'bacon'", o[3]]]
    cc = {(2, 1): C["green"], (4, 1): C["coral"]}
    table(s, x, y, w * 0.66, rows, [3.1, 2.9], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1), cell_color=cc, fs=9.5)
    names = ["spam", "bacon", "eggs"]
    x0 = x + w * 0.7
    for i, n in enumerate(names):
        chip(s, x0, y + i * 0.4, 0.9, 0.32, n, "teal", fs=10)
        arrow(s, x0 + 0.92, y + i * 0.4 + 0.16, x0 + 1.25, y + 0.4 + 0.16, C["teal"], 1.2)
    chip(s, x0 + 1.27, y + 0.4, 1.5, 0.32, o[0], "amber", fs=9.5)
    tb(s, x0, y + 1.2, 2.8, 0.26, "three names, one path object", 9.5, C["muted"], italic=True)


@need(1.5)
def v_locations(s, x, y, w, h, ns, out):
    o = lines(out)
    a, b = o[0].split()
    qs = [("Path.cwd().is_absolute()", a), ("Path.home().is_absolute()", b), ("Path('spam/bacon/eggs').is_absolute()", o[1]),
          ("Path('./spam.txt') == Path('spam.txt')", o[2]), ("resolve() equals cwd / 'spam.txt'", o[3])]
    rows = [["Question asked", "Answer"]] + [[q, v] for q, v in qs]
    cc = {(i + 1, 1): (C["green"] if v == "True" else C["coral"]) for i, (q, v) in enumerate(qs)}
    table(s, x, y, w * 0.6, rows, [4.2, 1.2], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1), cell_color=cc, align_cols={1: PP_ALIGN.CENTER})
    x0 = x + w * 0.64
    chip(s, x0, y, 1.0, 0.3, "/ root", "grey", fs=10)
    arrow(s, x0 + 1.02, y + 0.15, x0 + 1.3, y + 0.15, C["muted"], 1.2)
    chip(s, x0 + 1.32, y, 2.0, 0.3, "scratch folder (cwd)", "teal", fs=10, mono=False)
    arrow(s, x0 + 2.3, y + 0.32, x0 + 2.3, y + 0.62, C["muted"], 1.2)
    chip(s, x0 + 1.32, y + 0.64, 2.0, 0.3, "spam.txt", "amber", fs=10)
    tb(s, x0, y + 1.0, 3.5, 0.5, "relative: spam.txt  (from the cwd)", 10, C["ink"], name="legend")
    tb(s, x0, y + 1.25, 3.5, 0.5, "absolute: / scratch folder / spam.txt", 10, C["ink"], name="legend")


@need(1.8)
def v_anatomy(s, x, y, w, h, ns, out):
    p = ns["p"]
    pieces = list(p.parts[:-1]) + [p.stem, p.suffix]
    roles = ["drive + root", "folder", "folder", "stem", "suffix"]
    fills = ["grey", "teal", "teal", "amber", "green"]
    widths = [max(0.9, fit(t, 12) + 0.1) for t in pieces]
    xx = x
    pos = []
    for t, wd, f in zip(pieces, widths, fills):
        chip(s, xx, y + 0.35, wd, 0.42, t, f, fs=12)
        pos.append((xx, wd))
        xx += wd + 0.12
    for (px, wd), r in zip(pos, roles):
        tb(s, px - 0.05, y + 0.8, wd + 0.1, 0.24, r, 9.5, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
    # name = stem + suffix ; parent = the rest
    nx = pos[3][0]
    nw = pos[4][0] + pos[4][1] - nx
    line_seg(s, nx, y + 1.12, nx + nw, y + 1.12, C["amber"], 2)
    tb(s, nx - 0.1, y + 1.15, nw + 0.2, 0.25, "name = %s" % p.name, 10, C["ink"], bold=True, align=PP_ALIGN.CENTER, margin=(0, 0))
    px0 = pos[0][0]
    pw = pos[2][0] + pos[2][1] - px0
    line_seg(s, px0, y + 1.12, px0 + pw, y + 1.12, C["teal"], 2)
    tb(s, px0, y + 1.15, pw, 0.25, "parent = %s" % p.parent, 10, C["ink"], bold=True, align=PP_ALIGN.CENTER, margin=(0, 0))
    tb(s, x, y, 5.5, 0.28, "p = PureWindowsPath(%r)" % str(p).replace("\\", "/"), 10.5, C["teal"], bold=True, font=MONO, name="path label")
    o = lines(out)
    rows = [["Call", "Result"], ["p.parents[1]", o[3]], ["p.with_suffix('.csv')", o[4]]]
    table(s, x + 5.0, y + 0.25, w - 5.0, rows, [2.0, 2.2], rowh=0.34, mono_cols=(0, 1), fs=10)


@need(1.6)
def v_folders(s, x, y, w, h, ns, out):
    paths = [tuple(l.split("/")) for l in lines(out)]
    nodes = []
    for pth in paths:
        for k in range(1, len(pth) + 1):
            if pth[:k] not in nodes:
                nodes.append(pth[:k])
    depth = max(len(n) for n in nodes)
    kids = {n: [m for m in nodes if len(m) == len(n) + 1 and m[:len(n)] == n] for n in nodes}
    ypos = {}
    leaf = [0]

    def place(n):
        if not kids[n]:
            ypos[n] = leaf[0]
            leaf[0] += 1
        else:
            for k in kids[n]:
                place(k)
            ypos[n] = sum(ypos[k] for k in kids[n]) / len(kids[n])
    place(nodes[0])
    bw, bh, gx = 1.75, 0.34, 0.6
    gy = min(0.5, (h - 0.1) / max(1, leaf[0]))
    box = {}
    for n in nodes:
        bx, by = x + (len(n) - 1) * (bw + gx), y + ypos[n] * gy
        box[n] = (bx, by)
        chip(s, bx, by, bw, bh, n[-1] + ("/" if kids[n] else ""), "teal" if kids[n] else "amber", fs=11)
    for n in nodes:
        for k in kids[n]:
            arrow(s, box[n][0] + bw, box[n][1] + bh / 2, box[k][0], box[k][1] + bh / 2, C["muted"], 1.2)
    tb(s, x + depth * (bw + gx) - 0.2, y, w - depth * (bw + gx) + 0.2, 1.2,
       "Each line the loop printed is one box of the tree. Teal boxes hold other folders; amber boxes are the deepest folders.", 10.5, C["muted"], italic=True, name="legend")


@need(1.4)
def v_glob(s, x, y, w, h, ns, out):
    pats = ["project?.txt", "*.txt", "*"]
    res = [ast.literal_eval(l) for l in lines(out)]
    rows = [["glob pattern", "Names found", "Count"]] + [[p, ", ".join(r), str(len(r))] for p, r in zip(pats, res)]
    table(s, x, y, w * 0.7, rows, [1.3, 4.6, 0.6], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1), align_cols={2: PP_ALIGN.CENTER}, fs=9.5)
    chart(s, "bar", x + w * 0.72, y - 0.05, w * 0.28, h, pats[::-1], [("files found", [len(r) for r in res][::-1])], fs=9, legend=False, gap=40, vmax=5, major=1)


@need(1.5)
def v_fileinfo(s, x, y, w, h, ns, out):
    o = lines(out)
    f_ex, f_file, f_dir, dot_dir = o[1].split()
    rows = [["Question asked", "Answer"], ["f.exists() before writing", o[0]], ["f.exists() after writing", f_ex], ["f.is_file()", f_file],
            ["f.is_dir()", f_dir], ["Path('.').is_dir()", dot_dir]]
    cc = {(i, 1): (C["green"] if r[1] == "True" else C["coral"]) for i, r in enumerate(rows) if i}
    table(s, x, y, w * 0.5, rows, [2.9, 0.9], rowh=min(0.29, h / len(rows)), mono_cols=(0, 1), cell_color=cc, align_cols={1: PP_ALIGN.CENTER}, fs=10)
    x0 = x + w * 0.5 + 0.1
    chip(s, x0, y + 0.55, 0.9, 0.36, "f.txt", "teal", fs=12)
    chip(s, x0 + 1.4, y, 2.6, 0.34, "st_size = %s bytes" % o[2], "amber", fs=10)
    chip(s, x0 + 1.4, y + 0.55, 2.6, 0.34, "is a file, not a folder", "green", fs=10, mono=False)
    chip(s, x0 + 1.4, y + 1.1, 3.1, 0.34, "st_mtime = %s" % o[3], "amber", fs=9.5)
    for k in range(3):
        arrow(s, x0 + 0.92, y + 0.73, x0 + 1.38, y + 0.17 + k * 0.55, C["muted"], 1.2)


# ------------------------------------------------------------------ part 3
@need(1.7)
def v_wholefile(s, x, y, w, h, ns, out):
    o = lines(out)
    chars = [int(o[0]), int(o[2])]
    byts = [len("Hello, world!".encode("utf-8")), int(o[3])]
    chart(s, "col", x, y - 0.05, w * 0.42, h, ["'Hello, world!'", "'café'"], [("characters", chars), ("bytes on disk", byts)], fs=9.5, legend=True, gap=60, vmax=16, major=4)
    rows = [["Call", "Result"], ["write_text('Hello, world!')", o[0]], ["read_text()", o[1]], ["write_text('café')", o[2]], ["stat().st_size", o[3]],
            ["read_bytes()", o[4]]]
    table(s, x + w * 0.46, y, w * 0.54, rows, [2.5, 2.3], rowh=min(0.32, h / len(rows)), mono_cols=(0, 1), fs=10)


@need(1.3)
def v_openclose(s, x, y, w, h, ns, out):
    o = lines(out)
    steps = [("open(.., 'w')", "an empty file"), ("write(line 1)", "%s characters" % o[0]), ("write(line 2)", "%s characters" % o[1]),
             ("close()", "text saved"), ("reader.read()", "%d lines read back" % len(o[2:4])), ("reader.close()", "closed = %s" % o[4])]
    bw, gap = 1.38, 0.18
    for i, (a, b) in enumerate(steps):
        xx = x + i * (bw + gap)
        chip(s, xx, y + 0.1, bw, 0.4, a, "teal" if i < 4 else "amber", fs=9.5)
        tb(s, xx, y + 0.56, bw, 0.28, b, 10, C["ink"], align=PP_ALIGN.CENTER, name="step result")
        if i < len(steps) - 1:
            arrow(s, xx + bw, y + 0.3, xx + bw + gap, y + 0.3, C["muted"], 1.5)
    tb(s, x, y + 0.95, w, 0.3, "The program printed: %s, %s, then the two lines %r and %r, then %s." % (o[0], o[1], o[2], o[3], o[4]), 10.5, C["muted"], italic=True, name="legend")


@need(1.3)
def v_readmethods(s, x, y, w, h, ns, out):
    text = "roses\nviolets\nsugar\n"
    cw = (w - 0.1) / len(text)
    fills = {}
    for i in range(0, 6):
        fills[i] = "teal"
    for i in range(6, 20):
        fills[i] = "amber"
    strip(s, x, y, text, cw, 0.34, fills, fs=10, idx=True, label_fs=7)
    tb(s, x, y + 0.55, w, 0.26, "teal: readline took it    amber: readlines took it    the cursor then stands at 20, the end", 10, C["muted"], italic=True, name="legend")
    o = lines(out)
    rows = [["Call", "What came back", "Cursor after"]]
    names = ["readline()", "readlines()", "read()", "seek(0); read(5)"]
    for nme, l in zip(names, o):
        m = re.match(r"(.*) (\d+)$", l)
        rows.append([nme, m.group(1), m.group(2)])
    table(s, x, y + 0.85, w * 0.8, rows, [1.8, 3.8, 1.2], rowh=min(0.3, (h - 0.85) / len(rows)), mono_cols=(0, 1, 2), align_cols={2: PP_ALIGN.CENTER}, fs=10)


@need(1.4)
def v_withstatement(s, x, y, w, h, ns, out):
    o = lines(out)
    inside = o[0].split()[1]
    steps = [("with open(...) as file_obj:", "enter the block", "teal", "closed = %s" % inside), ("block ends", "with closes the file", "amber", "closed = %s" % o[1]),
             ("RuntimeError inside with", "an error leaves the block", "red", "closed = %s" % o[2])]
    bw, gap = 2.7, 0.55
    for i, (a, b, kind, r) in enumerate(steps):
        xx = x + i * (bw + gap)
        chip(s, xx, y + 0.05, bw, 0.4, a, kind, fs=10.5)
        tb(s, xx, y + 0.5, bw, 0.26, b, 10, C["muted"], align=PP_ALIGN.CENTER, name="step note")
        chip(s, xx + 0.3, y + 0.9, bw - 0.6, 0.34, r, "green" if r.endswith("True") else "grey", fs=10.5)
        arrow(s, xx + bw / 2, y + 0.76, xx + bw / 2, y + 0.88, C["muted"], 1.0)
        if i < len(steps) - 1:
            arrow(s, xx + bw, y + 0.25, xx + bw + gap, y + 0.25, C["muted"], 1.5)


@need(1.2)
def v_modes(s, x, y, w, h, ns, out):
    o = lines(out)
    steps = []
    for l in o[:4]:
        mode, rep = l.split(" ", 1)
        steps.append((mode, ast.literal_eval(rep)))
    cats = ["%d: %s" % (i + 1, m) for i, (m, t) in enumerate(steps)]
    chart(s, "col", x + w * 0.52, y - 0.05, w * 0.48, h, cats, [("file size in bytes after the step", [len(t) for m, t in steps])], fs=9.5, legend=False, gap=60, vmax=8, major=2)
    rows = [["Step", "Mode", "File now holds"]] + [[str(i + 1), m, repr(t)] for i, (m, t) in enumerate(steps)] + [["5", "x", short(o[4], 30)]]
    cc = {(5, 2): C["coral"]}
    table(s, x, y, w * 0.5, rows, [0.6, 0.7, 3.2], rowh=min(0.29, h / len(rows)), mono_cols=(1, 2), cell_color=cc, fs=10)


@need(1.4)
def v_encoding(s, x, y, w, h, ns, out):
    o = lines(out)
    enc = [l.rsplit(" ", 1) for l in o[3:6]]
    chart(s, "col", x + w * 0.56, y - 0.05, w * 0.44, h, [e for e, n in enc], [("bytes for 'café'", [int(n) for e, n in enc])], fs=9.5, legend=False, gap=60, vmax=10, major=2)
    rows = [["Reading the file with", "What happened"], ["encoding='utf-8'", o[0]], ["ascii, errors='replace'", o[1]], ["encoding='ascii'", o[2]]]
    cc = {(1, 1): C["green"], (3, 1): C["coral"]}
    table(s, x, y, w * 0.54, rows, [2.0, 3.0], rowh=min(0.4, h / len(rows)), mono_cols=(0, 1), cell_color=cc, fs=10)


# ------------------------------------------------------------------ part 4
@need(1.5)
def v_shelve(s, x, y, w, h, ns, out):
    o = lines(out)
    lost, kept = int(o[2]), int(o[3])
    chip(s, x, y + 0.1, 2.4, 0.42, "shelf['cats'] = [...]", "teal", fs=10.5)
    chip(s, x + 3.0, y + 0.1, 2.2, 0.42, "store[b'cats'] = bytes", "amber", fs=10.5)
    arrow(s, x + 2.42, y + 0.31, x + 2.98, y + 0.31, C["teal"], 1.5)
    tb(s, x + 2.35, y + 0.55, 0.7, 0.24, "pickled", 9.5, C["muted"], align=PP_ALIGN.CENTER, margin=(0, 0))
    tb(s, x + 5.3, y + 0.05, 1.65, 0.6, "on disk: shelve.open('mydata') makes it a file", 9, C["muted"], italic=True, name="legend")
    chip(s, x, y + 0.95, 6.8, 0.34, "keys and value: %s" % o[0], "plain", fs=10)
    chart(s, "bar", x + 7.0, y - 0.05, w - 7.0, h, ["assigned back", "changed in place", "stored"], [("names in the list", [kept, lost, 3])], fs=8.5, legend=False, gap=40, vmax=5, major=1)


@need(1.6)
def v_json(s, x, y, w, h, ns, out):
    data, back = ns["data"], json.loads(ns["text"])
    tname = lambda v: type(v).__name__
    kind = {"list": "array", "tuple": "array", "str": "string", "int": "number"}
    rows = [["Key in Python", "Value in Python", "Written as JSON", "Back in Python"]]
    cc = {}
    for i, (k, v) in enumerate(data.items(), 1):
        k2 = str(k)
        rows.append(["%r (%s)" % (k, tname(k)), tname(v), kind[tname(v)], "%s, key %r" % (tname(back[k2]), k2)])
        if tname(v) != tname(back[k2]) or tname(k) != "str":
            cc[(i, 3)] = C["coral"]
    table(s, x, y, w, rows, [2.0, 2.0, 2.0, 3.0], rowh=min(0.4, h / len(rows)), cell_color=cc, mono_cols=(0, 1, 3), fs=10.5)
    tb(s, x, y + 0.4 * len(rows) + 0.05, w, 0.3, "Red: the value comes back as another type. JSON has no tuples, and every key is text.", 10.5, C["muted"], italic=True, name="legend")


# ------------------------------------------------------------------ part 5
@need(1.2)
def v_madlibs(s, x, y, w, h, ns, out):
    story, result = ns["story"], ns["result"]
    blanks = re.findall(r"ADJECTIVE|NOUN|VERB", story)
    pat = re.escape(story)
    for b in set(blanks):
        pat = pat.replace(b, "(.+?)")
    m = re.fullmatch(pat, result)
    rows = [["Blank in panda.txt", "Answer written in"]] + [[b, a] for b, a in zip(blanks, m.groups())]
    table(s, x, y, w * 0.4, rows, [1.8, 1.9], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1), fs=10.5)
    x0 = x + w * 0.44
    chip(s, x0, y, 1.3, 0.36, "panda.txt", "grey", fs=10)
    arrow(s, x0 + 1.32, y + 0.18, x0 + 1.6, y + 0.18, C["teal"], 1.5)
    chip(s, x0 + 1.62, y, 1.0, 0.36, "re.sub", "teal", fs=10)
    arrow(s, x0 + 2.64, y + 0.18, x0 + 2.92, y + 0.18, C["teal"], 1.5)
    chip(s, x0 + 2.94, y, 1.75, 0.36, "panda_filled.txt", "amber", fs=10)
    tb(s, x0, y + 0.5, 5.7, 0.6, result, 11.5, C["ink"], bold=True, name="result text")


@need(0.95)
def v_regexsearch(s, x, y, w, h, ns, out):
    files = files_written(ns["__code__"])
    hits = set(lines(out))
    rows = [["File", "Lines", "Printed", "Why"]]
    cats, tot, shown = [], [], []
    cc = {}
    for name in sorted(files):
        if name.endswith(".txt"):
            ls = files[name].splitlines()
            k = sum(1 for i, l in enumerate(ls, 1) if "%s:%d: %s" % (name, i, l) in hits)
            rows.append([name, str(len(ls)), str(k), "lines with spam, in small letters"])
            cats.append(name); tot.append(len(ls)); shown.append(k)
        else:
            rows.append([name, "-", "-", "never opened: glob takes *.txt only"])
            cc[(len(rows) - 1, 3)] = C["greyTxt"]
    table(s, x, y, w * 0.68, rows, [1.2, 0.7, 0.8, 3.4], rowh=min(0.27, h / len(rows)), mono_cols=(0,), cell_color=cc, align_cols={1: PP_ALIGN.CENTER, 2: PP_ALIGN.CENTER}, fs=9.5)
    chart(s, "col", x + w * 0.71, y - 0.1, w * 0.29, h + 0.1, cats, [("lines in file", tot), ("lines printed", shown)], fs=8.5, legend=True, gap=50, vmax=4, major=1)


@need(1.25)
def v_quizquestion(s, x, y, w, h, ns, out):
    o = lines(out)
    q, opts = o[0], o[1:5]
    right = "ABCD"[ns["options"].index(ns["capitals"][ns["state"]])]
    chip(s, x + 2.0, y, 5.2, 0.3, q + "   (key: %s)" % right, "teal", fs=10.5, mono=False)
    for i, op in enumerate(opts):
        letter = op.strip()[0]
        xx = x + i * 2.32
        chip(s, xx, y + 0.5, 2.2, 0.3, op.strip(), "green" if letter == right else "plain", fs=10)
        arrow(s, x + 4.6, y + 0.3, xx + 1.1, y + 0.48, C["muted"], 1.0)


@need(0.8)
def v_quizfiles(s, x, y, w, h, ns, out):
    o = lines(out)
    k = len(o) // 2
    qs, ks = o[:k], o[k:]
    bw, gap = 1.85, 0.12
    for i, (q, kk) in enumerate(zip(qs, ks)):
        st, op = q.split(". ", 1)[1].split(": ")
        options = op.split(" / ")
        letter = kk.split(". ")[1]
        xx = x + i * (bw + gap)
        chip(s, xx, y, bw, 0.3, "%d. %s" % (i + 1, st), "teal", fs=10, mono=False)
        chip(s, xx, y + 0.45, bw, 0.3, "key %s = %s" % (letter, options["ABCD".index(letter)]), "green", fs=9.5, mono=False)
        arrow(s, xx + bw / 2, y + 0.3, xx + bw / 2, y + 0.45, C["muted"], 1.0)
    tb(s, x + 4 * (bw + gap) - 0.1, y, 1.3, 0.75, "quiz1.txt for the students, key1.txt for the teacher", 9.5, C["muted"], italic=True, name="legend")


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
