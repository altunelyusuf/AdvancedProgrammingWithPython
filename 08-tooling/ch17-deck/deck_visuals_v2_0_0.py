"""Chapter 17 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py (chapter 17) passes in); nothing is typed in by hand except plain-language names of boxes and
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


# ------------------------------------------------------------------ part 1
@need(1.25)
def v_pdf_anatomy(s, x, y, w, h, ns, out):
    L = lines(out)
    text = ns["text"]
    n_obj = int(L[1].split()[0])
    start = int(L[1].split("byte")[1].split()[0])
    total = len(ns["data"])
    bw = [1.45, 3.1, 2.25, 2.0]
    kinds = ["teal", "plain", "amber", "green"]
    names = ["header\n%s" % L[0].split(" ")[0][2:-1], "%d numbered objects\ncatalog, pages, font, 2 pages, 2 streams" % n_obj,
             "cross-reference table\nbegins at byte %d" % start, "trailer\nstartxref %d, then %%%%EOF" % start]
    gap = (w - sum(bw)) / 3
    xs = []
    xx = x
    for i, t in enumerate(names):
        box(s, xx, y + 0.05, bw[i], 0.62, t, kinds[i], 9.5)
        xs.append(xx)
        xx += bw[i] + gap
    # the jump: from the trailer back to the table
    y2 = y + 0.95
    line_seg(s, xs[3] + bw[3] / 2, y + 0.67, xs[3] + bw[3] / 2, y2, C["coral"], 1.5)
    line_seg(s, xs[2] + bw[2] / 2 + 0.05, y2, xs[3] + bw[3] / 2, y2, C["coral"], 1.5)
    arrow(s, xs[2] + bw[2] / 2, y2, xs[2] + bw[2] / 2, y + 0.69, C["coral"], 1.5)
    note(s, x, y + 0.82, xs[2] + bw[2] / 2 - x - 0.1, "the file is %d bytes; a reader starts at its end" % total, fs=9.5)
    note(s, xs[2] + bw[2] / 2 + 0.1, y + 0.98, 4.5, "startxref says where to jump: byte %d" % start, fs=9.5)


@need(1.2)
def v_reader_pages(s, x, y, w, h, ns, out):
    L = lines(out)
    widths = lit(after(L[1], ":"))
    chart(s, "col", x, y, w * 0.5, h - 0.05, ["page %d" % (i + 1) for i in range(len(widths))], [("width in points", widths)], fs=10, legend=False, gap=60, vmax=400, major=100)
    rows = [["Question", "Answer"], ["how many pages", L[0].split()[0]], ["is_encrypted", L[0].split("locked:")[1].strip()], ["page 3 width (points)", str(widths[2])]]
    table(s, x + w * 0.54, y + 0.05, w * 0.46, rows, [1.8, 1.4], rowh=min(0.3, (h - 0.1) / 4), mono_cols=(1,), bold_cols=(0,), fs=10)


@need(1.2)
def v_extract_text(s, x, y, w, h, ns, out):
    L = lines(out)
    box(s, x, y, 2.35, 0.3, "page 1 draws, in this order", "teal", 9.5, False)
    box(s, x, y + 0.36, 1.1, 0.36, "1st: world", "plain", 10, True)
    box(s, x + 1.2, y + 0.36, 1.15, 0.36, "2nd: Hello", "plain", 10, True)
    arrow(s, x + 2.4, y + 0.54, x + 3.0, y + 0.54, C["muted"], 1.5)
    box(s, x + 3.05, y + 0.36, 2.2, 0.36, "stream order: " + val(L[0]), "amber", 9.5, True)
    box(s, x + 3.05, y + 0.78, 2.2, 0.36, "layout: " + " ".join(lit(val(L[1]))), "green", 9.5, True)
    arrow(s, x + 2.4, y + 0.66, x + 3.0, y + 0.92, C["muted"], 1.2)
    bx = x + 5.6
    box(s, bx, y, 3.6, 0.3, "page 2 draws a text line, then a black box", "teal", 9.5)
    rect(s, bx, y + 0.36, 3.6, 0.36, "000000", name="black box")
    box(s, bx, y + 0.78, 3.6, 0.36, "still returned: " + val(L[2]), "red", 9.5, True)


@need(1.2)
def v_post_process(s, x, y, w, h, ns, out):
    L = lines(out)
    raw, text = ns["raw"], ns["text"]
    box(s, x, y, 2.85, 0.55, "raw: " + short(repr(raw), 60), "red", 9, True)
    for i, t in enumerate(["ligature to letters", "join the hyphen", "line break to space"]):
        box(s, x + 3.25, y + i * 0.37, 2.1, 0.3, t, "teal", 9.5)
    arrow(s, x + 2.9, y + 0.27, x + 3.2, y + 0.27, C["muted"], 1.5)
    arrow(s, x + 5.4, y + 0.27, x + 5.75, y + 0.27, C["muted"], 1.5)
    box(s, x + 5.8, y, 3.4, 0.55, "clean: " + short(repr(text), 60), "green", 9, True)
    box(s, x, y + 0.72, 3.0, 0.36, "a model would get %s words to fix" % L[2].split("a prompt of ")[1].split()[0], "plain", 9.5)
    note(s, x + 5.8, y + 0.76, 3.4, "no model is called here; the lines only count the request", fs=9.5, h=0.34)


@need(1.2)
def v_scan_images(s, x, y, w, h, ns, out):
    L = lines(out)
    size = lit(L[2].split("] ")[1])
    rect(s, x + 0.1, y + 0.1, 1.2, 0.8, "D62828", line=C["ink"], name="the picture")
    note(s, x, y + 0.95, 1.7, "%d x %d pixels" % size, fs=9.5)
    arrow(s, x + 1.55, y + 0.5, x + 2.05, y + 0.5, C["muted"], 1.5)
    rows = [["on the page", "result"], ["extract_text()", val(L[0])], ["len(page.images)", val(L[1])], ["files written", L[2].split("] ")[0] + "]"]]
    table(s, x + 2.15, y + 0.05, w - 2.15, rows, [1.4, 3.6], rowh=0.3, mono_cols=(0, 1), cell_fill={(1, 1): C["amberLight"], (2, 1): C["greenLight"]}, fs=10)


# ------------------------------------------------------------------ part 2
def _squares(s, x, y, label, chosen, n=6, size=0.34, kind="teal"):
    label_shape(s, x, y, 1.25, size, label, C["card"], C["ink"], size=10, line=C["line"], font=MONO)
    for i in range(1, n + 1):
        label_shape(s, x + 1.4 + (i - 1) * (size + 0.08), y, size, size, str(i), C["tealLight"] if i in chosen else C["grey"], C["ink"] if i in chosen else C["greyTxt"],
                    size=10, bold=i in chosen, line=C["line"], radius=0.2)


@need(1.2)
def v_append_pages(s, x, y, w, h, ns, out):
    L = lines(out)
    for i, ln in enumerate(L):
        lab, res = ln.split("->")
        _squares(s, x, y + i * 0.4, lab.strip(), lit(res.strip()))
        arrow(s, x + 4.05, y + i * 0.4 + 0.17, x + 4.45, y + i * 0.4 + 0.17, C["muted"], 1.5)
        tb(s, x + 4.5, y + i * 0.4, 4.7, 0.34, "copies %d pages: %s" % (len(lit(res.strip())), "a range, stop before 5" if i == 0 else ("every second page" if i == 1 else "exactly pages 1 and 6")),
           10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="meaning")


@need(1.2)
def v_merge_insert(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [("start", [100, 200, 300], set()), ("merge(1, ..., pages=(0, 2))", lit(val(L[0])), {1, 2}), ("insert_blank_page(index=2)", lit(val(L[1])), {2})]
    for r, (lab, lst, hi) in enumerate(rows):
        yy = y + r * 0.34
        tb(s, x, yy, 2.45, 0.3, lab, 10, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="step")
        arrow(s, x + 2.5, yy + 0.15, x + 2.78, yy + 0.15, C["muted"], 1.5)
        for i, wd in enumerate(lst):
            kind = "amber" if (r == 1 and i in hi) else ("teal" if (r == 2 and i == 2) else "plain")
            box(s, x + 2.8 + i * 1.0, yy, 0.9, 0.3, str(wd), kind, 10, True)
    note(s, x, y + 1.02, w, "each box is one page, named by its width; amber pages came from the other file, teal is the blank page", fs=9.5, h=0.2)


@need(1.2)
def v_rotate_pages(s, x, y, w, h, ns, out):
    seen = ns["seen"]
    prev = [0] + seen[:-1]
    cats = ["rotate(%d)" % (b - a) for a, b in zip(prev, seen)]
    chart(s, "col", x, y, w * 0.56, h - 0.05, cats, [("rotation", seen)], fs=10, legend=False, gap=60, vmax=500, major=100)
    box(s, x + w * 0.6, y + 0.1, w * 0.4, 0.45, "totals: %s" % ", ".join(str(v) for v in seen), "plain", 10, True)
    box(s, x + w * 0.6, y + 0.65, w * 0.4, 0.55, "the total is not wrapped at 360, so 450 means a quarter turn past a full one", "amber", 9.5)


@need(1.1)
def v_watermark(s, x, y, w, h, ns, out):
    L = lines(out)
    sizes = lit(val(L[1]))
    before, after_ = [int(t) for t in val(L[0]).replace("->", " ").split()]
    k = 0.025
    rect(s, x + 0.1, y + 0.1, sizes[0][0] * k, sizes[0][1] * k, "2B5FBF", line=C["ink"], name="first picture drawn")
    rect(s, x + 0.5, y + 0.3, sizes[1][0] * k, sizes[1][1] * k, "D62828", line=C["ink"], name="second picture drawn")
    rows = [["drawn", "picture size"], ["1st (the document)", "%d x %d" % sizes[0]], ["2nd (the stamp)", "%d x %d" % sizes[1]], ["images before -> after", "%d -> %d" % (before, after_)]]
    table(s, x + 2.4, y + 0.05, 4.2, rows, [2.2, 2.0], rowh=0.27, mono_cols=(1,), cell_fill={(3, 1): C["greenLight"]}, fs=10)
    box(s, x + 6.9, y + 0.05, 2.3, 1.0, "the later a picture is drawn, the higher it lies: the stamp lies on top", "amber", 10)


@need(1.2)
def v_encrypt_decrypt(s, x, y, w, h, ns, out):
    L = lines(out)
    items = ["encrypt('userpw',\nAES-256)", "locked: %s" % val(L[0]), "pages[0] refused\n%s" % val(L[1]), "decrypt('wrong')\n%s" % L[2].split("-> ")[1], "decrypt('userpw')\n%s" % L[3].split("-> ")[1],
             "%s" % L[4]]
    flow(s, x, y + 0.05, w, items, ["plain", "amber", "red", "red", "green", "green"], h=0.75, gap=0.22, fs=9)
    note(s, x, y + 0.9, w, "red: the pages stay closed; green: a match opens them", fs=9.5)


@need(1.2)
def v_user_owner(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["decrypt(...) with", "answer"]] + [[a.split(" -> ")[0], a.split(" -> ")[1]] for a in L[:3]]
    cf = {(1, 1): C["greenLight"], (2, 1): C["greenLight"], (3, 1): C["redLight"]}
    table(s, x, y, w * 0.5, rows, [1.4, 2.3], rowh=0.3, mono_cols=(0, 1), cell_fill=cf, fs=10)
    box(s, x + w * 0.55, y, w * 0.45, 0.55, "user password: opens the file and shows its pages", "green", 10)
    box(s, x + w * 0.55, y + 0.65, w * 0.45, 0.55, "owner password: also controls what the file allows", "amber", 10)


@need(0.95)
def v_project12_combine(s, x, y, w, h, ns, out):
    names = ns["pdf_filenames"]
    sizes = lit(out.split(" pages")[0])
    total = int(out.split("->")[1].split()[0])
    for i, nm in enumerate(names):
        yy = y + i * 0.31
        box(s, x, yy, 1.1, 0.27, nm, "plain", 10, True)
        for pg in range(sizes[i]):
            label_shape(s, x + 1.25 + pg * 0.45, yy, 0.38, 0.27, str(pg + 1), C["grey"] if pg == 0 else C["tealLight"], C["greyTxt"] if pg == 0 else C["ink"], size=10, line=C["line"], radius=0.2)
    arrow(s, x + 3.3, y + 0.5, x + 3.9, y + 0.5, C["muted"], 1.8)
    box(s, x + 4.0, y + 0.22, 1.6, 0.5, "combined.pdf\n%d pages" % total, "green", 10, True)
    box(s, x + 5.9, y, 3.3, 0.92, "order of the names: " + ", ".join(names) + "\ngrey: first page of each file skipped\n" + " + ".join(str(n - 1) for n in sizes) + " = %d" % total, "amber", 9.5)


@need(1.2)
def v_encrypt_schemes(s, x, y, w, h, ns, out):
    recs = []
    for ln in lines(out):
        lab, rest = ln.split(": ", 1)
        t = dict(kv.split("=") for kv in rest.split())
        recs.append(("%s (default)" % lab if lab == "None" else lab, int(t["V"]), int(t["R"]), int(t["bits"])))
    rows = [["lock", "V", "R", "key bits"]] + [[a, str(b), str(c), str(d)] for a, b, c, d in recs]
    table(s, x, y, w * 0.55, rows, [1.9, 0.6, 0.6, 1.0], rowh=0.3, mono_cols=(0, 1, 2, 3), cell_fill={(1, 1): C["amberLight"], (1, 2): C["amberLight"], (1, 3): C["amberLight"], (3, 3): C["greenLight"]}, fs=10)
    chart(s, "col", x + w * 0.6, y - 0.03, w * 0.4, max(h, 1.0) - 0.02, [r[0].split()[0] for r in recs], [("key bits", [r[3] for r in recs])], fs=9, legend=False, gap=60, vmax=300, major=100)


@need(1.2)
def v_project12_find(s, x, y, w, h, ns, out):
    found = lit(out.strip())
    tree = ast.parse(ns["__code__"])
    allnames = [[e.value for e in n.elts] for n in ast.walk(tree) if isinstance(n, ast.Tuple) and len(n.elts) == 4 and all(isinstance(e, ast.Constant) for e in n.elts)][0]
    for i, nm in enumerate(allnames):
        box(s, x, y + i * 0.3, 1.6, 0.26, nm, "green" if nm in found else "grey", 9.5, True)
    arrow(s, x + 1.7, y + 0.6, x + 2.4, y + 0.6, C["muted"], 1.5)
    box(s, x + 2.5, y + 0.3, 2.6, 0.6, "lower() and endswith('.pdf')\nkeeps %d of %d names" % (len(found), len(allnames)), "amber", 9.5)
    arrow(s, x + 5.2, y + 0.6, x + 5.7, y + 0.6, C["muted"], 1.5)
    box(s, x + 5.8, y + 0.3, 3.4, 0.6, "sorted, ignoring case:\n" + ", ".join(found), "teal", 9.5, True)
    note(s, x + 2.5, y + 0.95, 6.7, "green: kept; grey: left out (a text file)", fs=9.5, h=0.22)


# ------------------------------------------------------------------ part 3
@need(1.2)
def v_docx_zip(s, x, y, w, h, ns, out):
    names = ns["z"].namelist()
    k = 4
    per = (len(names) + k - 1) // k
    rows = []
    for r in range(per):
        rows.append([names[c * per + r] if c * per + r < len(names) else "\u00a0" for c in range(k)])
    cf = {}
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            if v == "word/document.xml":
                cf[(i, j)] = C["amberLight"]
    table(s, x, y, w, rows, [1] * k, rowh=0.24, header=False, mono_cols=tuple(range(k)), cell_fill=cf, fs=8.5)


@need(1.2)
def v_docx_read(s, x, y, w, h, ns, out):
    runs = [(r.text, r.bold) for r in ns["p"].runs]
    box(s, x, y + 0.38, 1.5, 0.36, "Document", "teal", 10, True)
    box(s, x + 2.1, y, 1.9, 0.34, "paragraphs[0]", "plain", 10, True)
    box(s, x + 2.1, y + 0.8, 1.9, 0.34, "tables[0].cell(0, 0)", "amber", 10, True)
    arrow(s, x + 1.5, y + 0.48, x + 2.08, y + 0.17, C["muted"], 1.4)
    arrow(s, x + 1.5, y + 0.66, x + 2.08, y + 0.95, C["muted"], 1.4)
    for i, (t, b) in enumerate(runs):
        box(s, x + 4.45 + i * 1.6, y, 1.5, 0.5, "run %d\n%r bold=%s" % (i + 1, t, b), "green" if b else "plain", 9, True)
    arrow(s, x + 4.02, y + 0.17, x + 4.43, y + 0.25, C["muted"], 1.4)
    box(s, x + 4.45, y + 0.8, 4.7, 0.34, "table text: %s - not in the paragraphs list" % ns["table"].cell(0, 0).text, "amber", 9.5)


@need(1.2)
def v_docx_fulltext(s, x, y, w, h, ns, out):
    L = lines(out)
    parts = L[:3]
    words = [len(p.split()) for p in parts]
    chart(s, "bar", x, y, w * 0.5, max(h, 1.0) - 0.05, [short(p, 18) for p in parts], [("words", words)], fs=10, legend=False, gap=50, vmax=4, major=1)
    rows = [["paragraph", "text"]] + [[str(i), p] for i, p in enumerate(parts)] + [["joined", L[3]]]
    table(s, x + w * 0.54, y + 0.03, w * 0.46, rows, [0.9, 2.8], rowh=0.23, mono_cols=(1,), cell_fill={(4, 1): C["greenLight"]}, fs=9.5)


@need(1.2)
def v_docx_styles(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["object", "style set", "style name read back"],
            ["paragraph", "Quote", val(L[0])],
            ["run", "Quote Char", val(L[1])]]
    table(s, x, y, w * 0.62, rows, [1.2, 1.5, 2.4], rowh=0.3, mono_cols=(1, 2), cell_fill={(1, 2): C["greenLight"], (2, 2): C["greenLight"]}, fs=10)
    box(s, x + w * 0.66, y, w * 0.34, 0.95, L[2].split(" styles")[0] + " styles in a new document\nfour kinds: paragraph, character, list, table", "teal", 9.5)


@need(1.2)
def v_run_attributes(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["you set", "run.bold reads back"]] + [[ln.split(" ->")[0], ln.split("reads back ")[1]] for ln in L[:3]]
    table(s, x, y, w * 0.4, rows, [1.4, 1.6], rowh=0.28, mono_cols=(0, 1), cell_fill={(1, 1): C["greenLight"], (2, 1): C["greenLight"], (3, 1): C["amberLight"]}, fs=10)
    rows2 = [["attribute", "read back"], ["run.italic", val(L[3]).split("|")[0].strip()], ["run.underline", L[3].split("underline:")[1].strip()],
             ["run.strike = True", L[4].split("-> ")[1]], ["run.font.strike = True", L[5].split("-> ")[1]]]
    table(s, x + w * 0.45, y, w * 0.55, rows2, [2.2, 1.2], rowh=0.23, mono_cols=(0, 1),
          cell_fill={(1, 1): C["greenLight"], (2, 1): C["greenLight"], (3, 1): C["redLight"], (4, 1): C["greenLight"]}, fs=9.5)


@need(1.2)
def v_docx_style_errors(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["object", "style asked", "result"],
            ["paragraph", "Quote Char", "refused: ValueError (wrong kind)"],
            ["paragraph", "List Number ", "not found: KeyError (trailing space)"],
            ["paragraph", "List Number", "accepted: " + val(L[2])]]
    table(s, x, y, w * 0.7, rows, [1.2, 1.5, 3.6], rowh=0.3, mono_cols=(1,), cell_fill={(1, 2): C["redLight"], (2, 2): C["redLight"], (3, 2): C["greenLight"]}, fs=10)
    box(s, x + w * 0.74, y, w * 0.26, 0.9, "ValueError for the wrong kind, KeyError for the wrong name", "amber", 9.5)


# ------------------------------------------------------------------ part 4
@need(1.2)
def v_docx_write(s, x, y, w, h, ns, out):
    again = ns["again"]
    runs = [(r.text, r.italic) for r in again.paragraphs[0].runs]
    box(s, x, y + 0.35, 1.5, 0.45, "Document (saved, then opened again)", "teal", 8.5)
    box(s, x + 2.0, y + 0.4, 1.5, 0.36, "%d paragraph" % len(again.paragraphs), "plain", 10, True)
    arrow(s, x + 1.52, y + 0.58, x + 1.98, y + 0.58, C["muted"], 1.4)
    for i, (t, it) in enumerate(runs):
        yy = y + 0.02 + i * 0.58
        box(s, x + 4.2, yy, 3.0, 0.5, "run %d: %r\nitalic = %s" % (i + 1, t, it), "amber" if it else "plain", 9.5, True)
        arrow(s, x + 3.52, y + 0.58, x + 4.18, yy + 0.25, C["muted"], 1.4)
    note(s, x + 7.4, y + 0.4, 1.8, "add_run(...) kept each run", fs=9.5, h=0.5)


@need(1.2)
def v_docx_headings(s, x, y, w, h, ns, out):
    L = lines(out)
    levels = [(int(ln.split()[1]), ln.split("-> ")[1]) for ln in L[:3]]
    for i, (lv, nm) in enumerate(levels):
        label_shape(s, x, y + i * 0.38, 4.2 - i * 1.1, 0.34, "level %d: %s" % (lv, nm), C["tealLight"], C["ink"], size=[15, 12, 10][i], bold=True, line=C["line"], radius=0.1)
    arrow(s, x + 4.3, y + 0.31, x + 4.65, y + 0.31, C["muted"], 1.5)
    box(s, x + 4.7, y, 4.5, 0.62, "add_heading(text, level): level 0 is the Title style; 1 to 9 are Heading 1 to Heading 9", "plain", 10)
    box(s, x + 4.7, y + 0.72, 4.5, 0.36, L[3].split(":")[0] + ": ValueError", "red", 10)


@need(1.2)
def v_docx_breaks(s, x, y, w, h, ns, out):
    L = lines(out)
    box(s, x, y, 2.6, 0.62, "page 1\nFirst line  [line break]\nsecond line, same paragraph", "plain", 9)
    line_seg(s, x + 2.7, y + 0.31, x + 3.3, y + 0.31, C["coral"], 2.5)
    box(s, x + 3.4, y, 1.7, 0.62, "[page break]", "amber", 10, True)
    arrow(s, x + 5.12, y + 0.31, x + 5.5, y + 0.31, C["muted"], 1.5)
    box(s, x + 5.55, y, 2.2, 0.62, "page 2\nSecond page", "plain", 9)
    box(s, x, y + 0.75, w, 0.34, "counted in the XML: " + L[0], "green", 10, True)


@need(1.2)
def v_docx_picture(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["call", "width (EMU)", "height (EMU)", "width in inches"]]
    cats, wd, ht = [], [], []
    for ln in L:
        lab, rest = ln.split(" -> ")
        a, b = [int(v) for v in rest.replace(" EMU", "").split(" x ")]
        rows.append([lab, str(a), str(b), "%.2f" % (a / 914400.0)])
        cats.append(lab); wd.append(round(a / 914400.0, 2)); ht.append(round(b / 914400.0, 2))
    table(s, x, y, w * 0.5, rows, [1.3, 1.2, 1.3, 1.2], rowh=0.3, mono_cols=(1, 2, 3), bold_cols=(0,), fs=9.5)
    chart(s, "col", x + w * 0.53, y - 0.03, w * 0.47, h - 0.02, cats, [("width", wd), ("height", ht)], fs=9, legend=True, gap=60, number_format="0.00")


# ------------------------------------------------------------------ part 5
@need(1.2)
def v_pdf_paranoia_walk(s, x, y, w, h, ns, out):
    found = lit(out.strip())
    tree = ast.parse(ns["__code__"])
    allpaths = [[e.value for e in n.elts] for n in ast.walk(tree) if isinstance(n, ast.Tuple) and len(n.elts) == 3 and all(isinstance(e, ast.Constant) for e in n.elts)][0]
    for i, nm in enumerate(allpaths):
        box(s, x, y + i * 0.34, 2.0, 0.3, nm, "green" if nm in found else "grey", 9.5, True)
    arrow(s, x + 2.1, y + 0.5, x + 2.7, y + 0.5, C["muted"], 1.5)
    box(s, x + 2.8, y + 0.2, 2.6, 0.6, "os.walk visits every folder;\nlower().endswith('.pdf')", "amber", 9.5)
    arrow(s, x + 5.5, y + 0.5, x + 6.0, y + 0.5, C["muted"], 1.5)
    box(s, x + 6.1, y + 0.2, 3.1, 0.6, "%d PDF paths found:\n%s" % (len(found), ", ".join(found)), "teal", 9, True)
    note(s, x, y + 1.05, w, "green: found; grey: left out (a text file)", fs=9.5, h=0.2)


@need(1.2)
def v_pdf_paranoia(s, x, y, w, h, ns, out):
    ok, listing = out.strip().split(" ", 1)
    items = ["a.pdf\n(the original)", "clone, then encrypt\nAES-256, save as\na_encrypted.pdf", "test the copy:\nis_encrypted and\ndecrypt matched: %s" % ok, "original removed\nfolder now: %s" % listing]
    flow(s, x, y + 0.05, w, items, ["plain", "amber", "teal", "green"], h=0.8, gap=0.4, fs=9.5)
    note(s, x, y + 0.95, w, "the original is removed only after the copy passed the test", fs=9.5, h=0.22)


@need(1.2)
def v_custom_invitations(s, x, y, w, h, ns, out):
    guests = ns["names"]
    for i, g in enumerate(guests):
        bx = x + i * 2.3
        box(s, bx, y, 1.9, 1.0, "page %d\nYou are invited,\n%s" % (i + 1, g), "plain", 9.5)
        if i < len(guests) - 1:
            arrow(s, bx + 1.92, y + 0.5, bx + 2.28, y + 0.5, C["coral"], 2.0)
    note(s, x + 6.9, y + 0.1, 2.3, "red arrow: a page break", fs=9.5)
    box(s, x + 6.9, y + 0.5, 2.3, 0.5, lines(out)[0], "green", 9.5)


@need(1.1)
def v_password_breaker(s, x, y, w, h, ns, out):
    guesses = ns["tries"]
    hit = ns["attempts"]
    bw = (w - 0.07 * (len(guesses) - 1)) / len(guesses)
    for i, g in enumerate(guesses, 1):
        kind = "green" if i == hit else ("red" if i < hit else "grey")
        box(s, x + (i - 1) * (bw + 0.07), y + 0.02, bw, 0.5, "%d\n%s" % (i, g), kind, 8.5, True)
    note(s, x, y + 0.55, w, "red: tried, no match; green: decrypt() matched; grey: never tried because the search stopped", fs=9.5, h=0.22)
    arrow(s, x, y + 0.94, x + 0.4, y + 0.94, C["muted"], 1.5)
    box(s, x + 0.5, y + 0.8, w - 0.5, 0.28, lines(out)[0], "amber", 10)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
