"""Chapter 18 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py (chapter 18) passes in); nothing is typed in by hand except plain-language names of boxes and
the one-line meanings of a step, which are named as such on the slide.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import ast
import re
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape as _label_shape, line_seg, table as _table, tb, rect, _style_run


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    """the kit table with the visuals' default font size (10.5 pt)"""
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


def label_shape(s, x, y, w, h, text, fill, color, size=11, bold=False, line=None, font=None, radius=0.12):
    """the kit's label shape; a text with line breaks becomes one centred paragraph per line"""
    parts = text.split("\n")
    sh = _label_shape(s, x, y, w, h, parts[0], fill, color, size=size, bold=bold, line=line, font=font, radius=radius)
    for t in parts[1:]:
        p = sh.text_frame.add_paragraph()
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = t
        _style_run(r, size, color, bold, False, font)
    return sh


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


FILL = {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"], "green": C["greenLight"], "grey": C["grey"]}


def box(s, x, y, w, h, text, kind="plain", fs=10, mono=False):
    return label_shape(s, x, y, w, h, text, FILL[kind], C["ink"], size=fs, line=C["line"], radius=0.12, font=MONO if mono else None)


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def note(s, x, y, w, text, h=0.24, fs=9.5):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def flow(s, x, y, w, items, kinds=None, h=0.5, fs=9.5, gap=0.32, mono=False):
    """a row of label shapes joined by arrows; items: texts (a line break makes two lines)"""
    n = len(items)
    bw = (w - gap * (n - 1)) / n
    for i, t in enumerate(items):
        xx = x + i * (bw + gap)
        box(s, xx, y, bw, h, t, kinds[i] if kinds else "plain", fs, mono)
        if i < n - 1:
            arrow(s, xx + bw + 0.02, y + h / 2, xx + bw + gap - 0.02, y + h / 2, C["muted"], 1.5)
    return bw


def lines(out):
    return out.rstrip("\n").split("\n")


def val(line):
    """the part of a printed line after the first ': '"""
    return line.split(": ", 1)[1] if ": " in line else line


def lit(text):
    return ast.literal_eval(text)


def after(line, sep):
    return line.split(sep, 1)[1].strip()


# ------------------------------------------------------------------ part 1: reading CSV files
@need(1.25)
def v_csv_split(s, x, y, w, h, ns, out):
    L = lines(out)
    pieces = lit(val(L[0]))
    fields = lit(val(L[1]))
    good = set(fields)
    tb(s, x, y + 0.04, 1.45, 0.4, "split(',')", 11, C["ink"], bold=True, font=MONO, anchor=MSO_ANCHOR.MIDDLE, name="row label")
    for i, p in enumerate(pieces):
        box(s, x + 1.5 + i * 1.62, y + 0.05, 1.5, 0.4, repr(p), "plain" if p in good else "red", 9.5, True)
    tb(s, x + 1.5 + len(pieces) * 1.62, y + 0.05, 1.3, 0.4, "%d pieces" % len(pieces), 11, C["coral"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="count")
    arrow(s, x + 0.7, y + 0.46, x + 0.7, y + 0.58, C["muted"], 1.5)
    tb(s, x, y + 0.6, 1.45, 0.4, "csv.reader", 11, C["ink"], bold=True, font=MONO, anchor=MSO_ANCHOR.MIDDLE, name="row label")
    for i, p in enumerate(fields):
        box(s, x + 1.5 + i * 2.1, y + 0.6, 2.0, 0.4, repr(p), "green", 9.5, True)
    tb(s, x + 1.5 + len(fields) * 2.1, y + 0.6, 1.4, 0.4, "%d fields" % len(fields), 11, C["green"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="count")
    note(s, x, y + 1.05, w, "red: the field with the comma was cut in two; green: the fields as the file means them. Then: " + L[2], fs=9.5, h=0.22)


@need(1.3)
def v_reader_list(s, x, y, w, h, ns, out):
    L = lines(out)
    data = ns["data"]
    rows = [["", "[0]", "[1]"]] + [["data[%d]" % i, r[0], r[1]] for i, r in enumerate(data)]
    table(s, x, y, w * 0.5, rows, [1.1, 1.2, 1.0], rowh=0.3, mono_cols=(0, 1, 2), cell_fill={(2, 1): C["greenLight"], (3, 2): C["amberLight"]}, fs=10)
    a, b = L[1].split()
    box(s, x + w * 0.55, y + 0.05, w * 0.45, 0.4, "data[1][0] -> %s" % a, "green", 10, True)
    box(s, x + w * 0.55, y + 0.5, w * 0.45, 0.4, "data[2][1] -> %r" % b, "amber", 10, True)
    box(s, x + w * 0.55, y + 0.95, w * 0.45, 0.3, "type of the 30: %s, not int" % L[2], "plain", 10, True)


@need(1.3)
def v_for_loop(s, x, y, w, h, ns, out):
    L = lines(out)
    recs = []
    for i, ln in enumerate(L[:3]):
        num = int(ln.split("#")[1].split()[0])
        recs.append((i + 1, num, ln.split(" ", 2)[2]))
    rows = [["record", "line_num", "row read"]] + [[str(a), str(b), short(c, 34)] for a, b, c in recs]
    cf = {(i + 1, 1): C["amberLight"] for i, (a, b, c) in enumerate(recs) if a != b}
    table(s, x, y, w * 0.62, rows, [0.9, 1.0, 3.6], rowh=0.3, mono_cols=(0, 1, 2), cell_fill=cf, fs=10)
    box(s, x + w * 0.66, y + 0.05, w * 0.34, 0.55, "amber: the line number is ahead of the record number", "amber", 9.5)
    box(s, x + w * 0.66, y + 0.68, w * 0.34, 0.5, L[3] + "  |  " + L[4], "plain", 9, True)


@need(1.3)
def v_next_header(s, x, y, w, h, ns, out):
    L = lines(out)
    box(s, x, y + 0.02, 2.2, 0.42, "next(reader) took\n" + val(L[0]), "teal", 9.5, True)
    arrow(s, x + 2.25, y + 0.23, x + 2.65, y + 0.23, C["muted"], 1.5)
    box(s, x + 2.7, y + 0.02, 4.0, 0.42, "list(reader) left\n" + val(L[1]), "green", 9.5, True)
    kept = lit(L[2])
    box(s, x, y + 0.62, 2.2, 0.5, "a header of two lines:\none record, line_num 2", "amber", 9.5)
    arrow(s, x + 2.25, y + 0.87, x + 2.65, y + 0.87, C["muted"], 1.5)
    box(s, x + 2.7, y + 0.62, 4.0, 0.5, "the line_num test keeps %d records:\nthe header is still there" % len(kept), "red", 9.5, True)
    note(s, x + 6.85, y + 0.62, 2.35, "next() skips the header, whatever its length", fs=9.5, h=0.5)


# ------------------------------------------------------------------ part 2: writing CSV files
@need(1.25)
def v_writer_basics(s, x, y, w, h, ns, out):
    L = lines(out)
    written = ns["out"].getvalue().split("\r\n")[:3]
    labels = ["4 words", "a field with a comma", "number, None, empty, True"]
    rows = [["row given", "returned", "line in the file"]] + [[labels[i], L[i], written[i]] for i in range(3)]
    table(s, x, y, w, rows, [2.2, 0.9, 4.0], rowh=0.3, mono_cols=(1, 2), cell_fill={(2, 2): C["amberLight"], (3, 2): C["greenLight"]}, fs=10)
    note(s, x, y + 1.25, w, "returned = characters written, the 2 of CRLF included; amber: a comma made quotes; green: None and '' became empty fields", fs=9.5, h=0.22)


@need(1.2)
def v_tabs(s, x, y, w, h, ns, out):
    L = lines(out)
    recs = [r.split("\t") for r in ns["out"].getvalue().split("\n") if r]
    rows = [["field 1", "field 2", "field 3"]] + [list(r) for r in recs]
    table(s, x, y, w * 0.55, rows, [1.0, 0.8, 1.4], rowh=0.27, mono_cols=(0, 1, 2), fs=10)
    box(s, x + w * 0.6, y + 0.05, w * 0.4, 0.5, "fields are told apart by a tab; a record ends with a line feed", "teal", 9.5)
    box(s, x + w * 0.6, y + 0.62, w * 0.4, 0.5, "read back with delimiter='\\t': %d rows of %d fields" % (len(ns["back"]), len(ns["back"][0])), "green", 9.5)


@need(1.2)
def v_newline_blank(s, x, y, w, h, ns, out):
    L = lines(out)
    back = list(ns["csv"].reader(ns["io"].StringIO(ns["write"]("\r\n").decode(), newline="")))
    box(s, x, y + 0.02, 3.6, 0.34, "newline='': a , b  CR LF  -> " + L[0].split()[-1] + " records", "green", 9.5, True)
    box(s, x, y + 0.42, 3.6, 0.34, "Windows: a , b  CR CR LF  -> " + L[1].split()[-1] + " records", "red", 9.5, True)
    note(s, x, y + 0.82, 3.6, "the extra CR makes the reader see an empty record after every row", fs=9.5, h=0.4)
    arrow(s, x + 3.7, y + 0.55, x + 4.1, y + 0.55, C["muted"], 1.5)
    rows = [["", "A", "B"]] + [[str(i + 1), r[0] if r else "", r[1] if r else ""] for i, r in enumerate(back)]
    cf = {(i + 1, j): (C["grey"] if not r else C["card"]) for i, r in enumerate(back) for j in range(3)}
    table(s, x + 4.2, y, 2.7, rows, [0.5, 0.9, 0.9], rowh=0.2, mono_cols=(0, 1, 2), cell_fill=cf, fs=9)
    box(s, x + 7.1, y + 0.1, 2.1, 0.9, "the spreadsheet of Figure 18-1: every second row is empty", "amber", 9.5)


@need(1.1)
def v_quoting(s, x, y, w, h, ns, out):
    recs = []
    for ln in lines(out):
        name, rep = ln.split(" ", 1)
        recs.append((name.replace("QUOTE_", ""), rep))
    cf = {(1, 1): C["greenLight"]}
    for k in range(2):
        part = recs[k * 3:k * 3 + 3]
        rows = [["QUOTE_", "line written"]] + [[a, b] for a, b in part]
        table(s, x + k * (w / 2 + 0.05), y, w / 2 - 0.05, rows, [1.3, 2.5], rowh=0.3, mono_cols=(0, 1), cell_fill=(cf if k == 0 else None), fs=9)


@need(1.3)
def v_encoding_bom(s, x, y, w, h, ns, out):
    L = lines(out)
    box(s, x, y + 0.02, 1.5, 0.4, "EF BB BF\nthe mark", "amber", 9.5, True)
    arrow(s, x + 1.52, y + 0.22, x + 1.58, y + 0.22, C["muted"], 1.5)
    box(s, x + 1.6, y + 0.02, 2.3, 0.4, "N a m e , C i t y ...\nthe text", "plain", 9.5, True)
    tb(s, x + 4.1, y + 0.02, 5.1, 0.4, "the file's first three bytes are not a letter; Excel adds them", 10, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, name="meaning")
    box(s, x, y + 0.55, 3.0, 0.42, "decoded as utf-8:\n" + L[1], "red", 9.5, True)
    box(s, x + 3.15, y + 0.55, 3.0, 0.42, "decoded as utf-8-sig:\n" + L[2], "green", 9.5, True)
    box(s, x + 6.3, y + 0.55, 2.9, 0.42, "DictReader keys:\n" + L[3], "red", 9.5, True)
    note(s, x, y + 1.02, w, "red: the invisible first character sits in the first key", fs=9.5, h=0.22)


@need(1.3)
def v_dict_rw(s, x, y, w, h, ns, out):
    L = lines(out)
    r1, r2 = lit(L[0]), lit(L[1])
    rows = [["Name", "Age"], [r1["Name"], r1["Age"]], [r2["Name"], r2["Age"]]]
    table(s, x, y, w * 0.38, [[str(c) for c in r] for r in rows], [1.2, 1.0], rowh=0.3, mono_cols=(0, 1), cell_fill={(2, 1): C["amberLight"]}, fs=10)
    note(s, x, y + 0.95, w * 0.38, "DictReader: a short row gives None", fs=9.5, h=0.24)
    arrow(s, x + w * 0.4, y + 0.45, x + w * 0.46, y + 0.45, C["muted"], 1.5)
    file_lines = lit(L[2])
    rows2 = [["file written by DictWriter"]] + [[l] for l in file_lines]
    table(s, x + w * 0.48, y, w * 0.34, rows2, [1], rowh=0.3, mono_cols=(0,), cell_fill={(3, 0): C["amberLight"]}, fs=10)
    note(s, x + w * 0.48, y + 1.25, w * 0.5, "DictWriter: a missing key gives an empty field", fs=9.5, h=0.24)


# ------------------------------------------------------------------ part 3: Project 13
@need(1.25)
def v_p13_loop(s, x, y, w, h, ns, out):
    names = list(ns["names"])
    shown = {ln.split("from ")[1].rstrip(".") for ln in lines(out)}
    for i, nm in enumerate(names):
        box(s, x, y + i * 0.3, 1.5, 0.26, nm, "green" if nm in shown else "grey", 9.5, True)
    arrow(s, x + 1.6, y + 0.6, x + 2.2, y + 0.6, C["muted"], 1.5)
    box(s, x + 2.3, y + 0.3, 2.9, 0.6, "sorted(os.listdir('.')) and\nendswith('.csv') keep %d of %d names" % (len(shown), len(names)), "amber", 9.5)
    arrow(s, x + 5.3, y + 0.6, x + 5.8, y + 0.6, C["muted"], 1.5)
    box(s, x + 5.9, y + 0.3, 3.3, 0.6, "printed, in order:\n" + ", ".join(sorted(shown)), "teal", 9.5, True)
    note(s, x + 2.3, y + 0.97, 6.9, "green: the program works on it; grey: skipped (a text file, and C.CSV because the test is case-sensitive)", fs=9.5, h=0.22)


@need(1.2)
def v_p13_read(s, x, y, w, h, ns, out):
    L = lines(out)
    cases = [("a file: a header and\none row", L[0]), ("an empty file", L[1])]
    for i, (lab, ln) in enumerate(cases):
        yy = y + i * 0.62
        a, b = ln.split(" -> ")
        box(s, x, yy, 2.2, 0.5, lab, "plain", 9.5)
        arrow(s, x + 2.25, yy + 0.25, x + 2.65, yy + 0.25, C["muted"], 1.5)
        box(s, x + 2.7, yy, 2.4, 0.5, "next(reader, None)\n-> " + a, "teal" if i == 0 else "amber", 9.5, True)
        arrow(s, x + 5.15, yy + 0.25, x + 5.55, yy + 0.25, C["muted"], 1.5)
        box(s, x + 5.6, yy, 3.6, 0.5, "list(reader)\n-> " + b, "green", 9.5, True)
    note(s, x, y + 1.27, w, "None instead of an error on the empty file: the loop simply has nothing to do", fs=9.5, h=0.22)


@need(1.15)
def v_p13_write(s, x, y, w, h, ns, out):
    recs = []
    for ln in lines(out):
        a = ln.split()
        recs.append((a[0], int(a[1]), int(a[3])))
    chart(s, "col", x, y, w * 0.5, max(h, 1.2) - 0.05, [r[0] for r in recs], [("rows before", [r[1] for r in recs]), ("rows after", [r[2] for r in recs])], fs=9, legend=True, gap=60, vmax=4, major=1)
    box(s, x + w * 0.55, y + 0.05, w * 0.45, 0.55, "the folder: " + ", ".join(r[0] for r in recs) + " and headerRemoved", "plain", 9.5, True)
    box(s, x + w * 0.55, y + 0.68, w * 0.45, 0.55, "headerRemoved holds the same names, each with one row less", "green", 9.5)


@need(1.25)
def v_col_total(s, x, y, w, h, ns, out):
    tot = ns["totals"]
    chart(s, "bar", x, y, w * 0.45, max(h, 1.2) - 0.05, list(tot), [("total sales", list(tot.values()))], fs=10, legend=False, gap=50, vmax=200, major=50)
    rows = [["region", "rows added", "total"]]
    for reg in tot:
        parts = [r.split(",")[1] for r in ns["text"].split("\r\n")[1:] if r.startswith(reg + ",")]
        rows.append([reg, " + ".join(parts), str(tot[reg])])
    table(s, x + w * 0.5, y + 0.05, w * 0.5, rows, [1.0, 1.4, 0.8], rowh=0.3, mono_cols=(0, 1, 2), cell_fill={(1, 2): C["greenLight"]}, fs=10)


# ------------------------------------------------------------------ part 4: JSON
@need(1.3)
def v_formats_compare(s, x, y, w, h, ns, out):
    L = lines(out)
    n = [int(t) for t in L[1].split(":")[1].split()]
    chart(s, "col", x, y, w * 0.42, max(h, 1.25) - 0.05, ["CSV", "JSON", "XML"], [("characters", n)], fs=10, legend=False, gap=60, vmax=140, major=40)
    for i, (lab, txt, k) in enumerate((("CSV", ns["as_csv"], "teal"), ("JSON", ns["as_json"], "amber"), ("XML", ns["as_xml"], "green"))):
        box(s, x + w * 0.46, y + 0.02 + i * 0.42, w * 0.54, 0.36, "%s: %s" % (lab, short(repr(txt), 52)), k, 9, True)


@need(1.45)
def v_json_loads(s, x, y, w, h, ns, out):
    data = ns["data"]
    kind = {"str": "string", "int": "number", "NoneType": "null", "bool": "true / false", "list": "array", "dict": "object", "float": "number"}
    rows = [["key", "Python value", "Python type", "JSON kind"]]
    for k, v in data.items():
        rows.append([k, repr(v), type(v).__name__, kind[type(v).__name__]])
    table(s, x, y, w, rows, [1.0, 2.6, 1.6, 1.6], rowh=min(0.24, (h + 0.05) / len(rows)), mono_cols=(0, 1, 2), cell_fill={(3, 1): C["amberLight"], (4, 1): C["amberLight"]}, fs=9.5)


@need(1.45)
def v_json_dumps(s, x, y, w, h, ns, out):
    import json
    d, back = ns["d"], ns["back"]
    rows = [["Python key: value", "JSON piece", "read back", "same?"]]
    cf = {}
    for i, (k, v) in enumerate(d.items(), 1):
        piece = json.dumps({k: v})[1:-1]
        bk = k if isinstance(k, str) else str(k)
        same = (bk == k) and back[bk] == v
        rows.append(["%r: %r" % (k, v), piece, "%r: %r" % (bk, back[bk]), "yes" if same else "no"])
        cf[(i, 3)] = C["greenLight"] if same else C["amberLight"]
    table(s, x, y, w, rows, [2.4, 2.4, 2.4, 0.7], rowh=min(0.24, (h + 0.05) / len(rows)), mono_cols=(0, 1, 2), cell_fill=cf, fs=9, align_cols={3: PP_ALIGN.CENTER})


@need(1.3)
def v_json_strict(s, x, y, w, h, ns, out):
    recs = []
    for ln in lines(out):
        a, b = ln.split(" -> ")
        recs.append((a, b))
    rows = [["text given to json.loads()", "what it says"]] + [[a, b] for a, b in recs]
    cf = {(i, 1): (C["greenLight"] if b == "accepted" else C["redLight"]) for i, (a, b) in enumerate(recs, 1)}
    table(s, x, y, w, rows, [3.0, 6.0], rowh=min(0.22, (h + 0.05) / len(rows)), mono_cols=(0, 1), cell_fill=cf, fs=9)


@need(1.3)
def v_json_files(s, x, y, w, h, ns, out):
    L = lines(out)
    items = ["dict with\nİstanbul", "json.dump(...,\nensure_ascii=False)", "file bytes\n" + short(L[0], 24), "json.load(f)", "equals the\noriginal: " + L[1]]
    flow(s, x, y + 0.02, w, items, ["plain", "teal", "amber", "teal", "green"], h=0.62, gap=0.28, fs=9)
    box(s, x, y + 0.82, 4.3, 0.34, "bytes with a BOM: " + L[2], "green", 9.5, True)
    box(s, x + 4.5, y + 0.82, 4.7, 0.34, L[3], "red", 9, True)


# ------------------------------------------------------------------ part 5: XML
@need(1.05)
def v_et_read(s, x, y, w, h, ns, out):
    root = ns["root"]
    kids = list(root)
    bw = 1.7
    gap = (w - bw * len(kids)) / (len(kids) - 1)
    box(s, x + w / 2 - 0.9, y, 1.8, 0.3, "<%s>  root" % root.tag, "teal", 10, True)
    for i, k in enumerate(kids):
        xx = x + i * (bw + gap)
        arrow(s, x + w / 2, y + 0.3, xx + bw / 2, y + 0.58, C["muted"], 1.2)
        attr = (" " + " ".join("%s=%s" % kv for kv in k.attrib.items())) if k.attrib else ""
        box(s, xx, y + 0.6, bw, 0.62, "<%s>%s\ntext: %r" % (k.tag, attr, k.text), "amber" if k.text is None else "plain", 9, True)
    note(s, x, y + 1.25, w, "amber: the empty element car has the text None, not an empty string", fs=9.5, h=0.22)


@need(1.3)
def v_et_traps(s, x, y, w, h, ns, out):
    L = lines(out)
    a = ns["a"]
    rows = [["XML given to ElementTree", "what ElementTree says"],
            ["'<a>\\n  <b>x</b>\\n</a>'", "a.text=%r, b.tail=%r, b.text=%r" % (a.text, a[0].tail, a[0].text)]]
    cf = {(1, 1): C["amberLight"]}
    for i, ln in enumerate(L[1:], 2):
        bad, msg = ln.split(" -> ")
        rows.append([repr(bad), "ParseError: " + msg])
        cf[(i, 1)] = C["redLight"]
    table(s, x, y, w, rows, [2.6, 6.4], rowh=0.26, mono_cols=(0, 1), cell_fill=cf, fs=9.5)


@need(1.45)
def v_et_write(s, x, y, w, h, ns, out):
    L = lines(out)
    compact = L[0]
    pretty = "\n".join(L[1:L.index("</person>") + 1])
    box(s, x, y + 0.02, 4.0, 0.7, "tostring: one line of %d characters\n%s" % (len(compact), short(compact, 70)), "amber", 8.5, True)
    arrow(s, x + 4.05, y + 0.37, x + 4.45, y + 0.37, C["muted"], 1.5)
    box(s, x + 4.5, y + 0.02, 4.7, 1.0, "ET.indent(p), then tostring:\n" + pretty, "green", 8.5, True)
    box(s, x, y + 0.8, 4.0, 0.3, "< became &lt;, & became &amp;", "plain", 9.5)
    note(s, x, y + 1.15, w, "write(..., xml_declaration=True) starts the file with: " + L[-1], fs=9, h=0.22)


@need(1.3)
def v_et_nil(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["expression", "result"], ["r[0].attrib", L[0]], ["r[0].text", L[1]], ["n.tag", L[2].split()[0]],
            ["n.find('{...}i').text, n.find('i').text", "%s and %s  (different elements)" % (L[2].split()[1], L[2].split()[2])]]
    table(s, x, y, w, rows, [3.0, 6.2], rowh=0.27, mono_cols=(0, 1), cell_fill={(1, 1): C["amberLight"], (2, 1): C["amberLight"]}, fs=9)


@need(1.2)
def v_xmltodict_rt(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["XML given", "dict returned by xmltodict.parse()"],
            ["person: name, age, phone with type", L[0]],
            ["one <b>1</b> inside <a>", L[1]],
            ["two <b> elements inside <a>", L[2]],
            ["parse(unparse(d)) == d", L[-1]]]
    table(s, x, y, w, rows, [2.4, 6.8], rowh=0.27, mono_cols=(1,), cell_fill={(2, 1): C["tealLight"], (3, 1): C["amberLight"], (4, 1): C["greenLight"]}, fs=9)


@need(1.15)
def v_xml_security(s, x, y, w, h, ns, out):
    L = lines(out)
    n = int(L[0].split()[3])
    box(s, x, y + 0.2, 2.5, 0.75, "document: entity a = lol,\nentity b = ten a's", "plain", 9.5, True)
    arrow(s, x + 2.55, y + 0.45, x + 3.0, y + 0.2, C["muted"], 1.5)
    arrow(s, x + 2.55, y + 0.7, x + 3.0, y + 0.95, C["muted"], 1.5)
    box(s, x + 3.05, y, 3.1, 0.4, "ElementTree: %d characters" % n, "amber", 9.5, True)
    box(s, x + 3.05, y + 0.75, 3.1, 0.4, "defusedxml: refuses the entities", "green", 9.5, True)
    box(s, x + 6.4, y + 0.1, 2.8, 0.95, "9 levels of ten: %s characters, almost 3 GB" % format(3 * 10 ** 9, ","), "red", 9.5)
    note(s, x, y + 1.2, w, "the document is under 1 KB in the large case; each level multiplies the text by ten", fs=9.5, h=0.22)


# ------------------------------------------------------------------ part 6: practice program
@need(1.1)
def v_xl_make(s, x, y, w, h, ns, out):
    wb = ns["again"]
    sales = [list(r) for r in wb["Sales"].iter_rows(values_only=True)]
    costs = [list(r) for r in wb["Costs"].iter_rows(values_only=True)]
    tb(s, x, y, 2.0, 0.24, "sheet Sales", 10, C["teal"], bold=True, name="sheet label")
    table(s, x, y + 0.26, 2.8, [["A", "B"]] + [[str(a), str(b)] for a, b in sales], [1.4, 1.0], rowh=0.24, mono_cols=(0, 1), cell_fill={(2, 1): C["greenLight"]}, fs=9.5, header=True)
    tb(s, x + 3.1, y, 2.0, 0.24, "sheet Costs", 10, C["teal"], bold=True, name="sheet label")
    table(s, x + 3.1, y + 0.26, 2.4, [["A", "B"]] + [[str(a), str(b)] for a, b in costs], [1.2, 1.0], rowh=0.24, mono_cols=(0, 1), fs=9.5)
    box(s, x + 5.8, y + 0.26, 3.4, 0.5, "saved into memory, loaded again:\n" + L0(out), "teal", 9.5, True)
    note(s, x + 5.8, y + 0.82, 3.4, "green: ['Sales']['B2'] holds 120, a number, not text", fs=9.5, h=0.4)


def L0(out):
    return lines(out)[0]


@need(1.15)
def v_xl_convert(s, x, y, w, h, ns, out):
    wb = ns["wb"]
    sheets = [ws.title for ws in wb.worksheets]
    box(s, x, y + 0.15, 1.9, 0.7, "workbook\nsheets: " + ", ".join(sheets), "teal", 9.5, True)
    for i, ln in enumerate(lines(out)):
        nm, n, _ = ln.split()
        content = [",".join(str(c) for c in r) for r in wb[nm[len("book-"):-len(".csv")]].iter_rows(values_only=True)]
        yy = y + i * 0.55
        arrow(s, x + 1.95, y + 0.5, x + 2.4, yy + 0.25, C["muted"], 1.5)
        box(s, x + 2.45, yy, 2.4, 0.46, "%s  (%s rows)" % (nm, n), "green", 9.5, True)
        box(s, x + 5.0, yy, 4.2, 0.46, "lines: " + short(repr(content), 52), "plain", 9, True)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
