"""Chapter 14 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py (chapter 14) passes in); nothing is typed in by hand except plain-language names of columns and boxes,
and the two measured figures of the research (finding F8, read-only memory), which are named as such on the slide.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from openpyxl.utils import get_column_letter
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape as _label_shape, table as _table, tb, rect, line_seg, _style_run


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


def chip(s, x, y, w, h, text, kind="plain", fs=10.5, mono=True):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO if mono else None, line=C["line"], radius=0.15)


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def note(s, x, y, w, text, h=0.24, fs=9.5):
    return tb(s, x, y, w, h, text, fs, C["muted"], italic=True, name="visual note")


def flow(s, x, y, w, items, kinds=None, h=0.5, fs=9.5, gap=0.32, font_mono=False):
    """a row of label shapes joined by arrows; items: texts (a line break makes two lines)"""
    n = len(items)
    bw = (w - gap * (n - 1)) / n
    fill = {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"], "green": C["greenLight"], "grey": C["grey"]}
    for i, t in enumerate(items):
        k = kinds[i] if kinds else "plain"
        xx = x + i * (bw + gap)
        label_shape(s, xx, y, bw, h, t, fill[k], C["ink"], size=fs, line=C["line"], radius=0.12, font=MONO if font_mono else None)
        if i < n - 1:
            arrow(s, xx + bw + 0.02, y + h / 2, xx + bw + gap - 0.02, y + h / 2, C["muted"], 1.5)
    return bw


def grid(s, x, y, w, cells, ncols, nrows, fills=None, fs=9, rowh=0.2, first_col=1, first_row=1, colw0=0.5, width_of=None, name="sheet grid"):
    """a drawn sheet: a native table with the column letters on top and the row numbers on the left.
    cells: {'A1': text}; fills: {'A1': colour}; the grid shows columns first_col.. first_col+ncols-1 and rows first_row.. first_row+nrows-1."""
    cols = [get_column_letter(first_col + j) for j in range(ncols)]
    rows = [[""] + cols]
    cf = {}
    for i in range(nrows):
        r = first_row + i
        rows.append([str(r)] + [str(cells.get("%s%d" % (c, r), "")) or " " for c in cols])
        for j, c in enumerate(cols):
            if fills and "%s%d" % (c, r) in fills:
                cf[(i + 1, j + 1)] = fills["%s%d" % (c, r)]
        cf[(i + 1, 0)] = C["grey"]
    colw = [colw0] + [(width_of(c) if width_of else 1.0) for c in cols]
    return table(s, x, y, w, rows, colw, fs=fs, rowh=rowh, cell_fill=cf, align_cols={j: PP_ALIGN.CENTER for j in range(ncols + 1)}, bold_cols=(0,), name=name)


def tabs(s, x, y, w, names, active, h=0.46, fs=10):
    """a row of sheet tabs; the active one is highlighted; each tab shows its index"""
    bw = min(1.9, (w - 0.1 * (len(names) - 1)) / len(names))
    for i, n in enumerate(names):
        a = n == active
        label_shape(s, x + i * (bw + 0.1), y, bw, h, "%d\n%s" % (i, short(n, 22)), C["amberLight"] if a else C["card"], C["ink"], size=fs, bold=a, line=C["amber"] if a else C["line"], radius=0.2)
    return bw


# ------------------------------------------------------------------ part 1
ZIP_ROLE = {"[Content_Types].xml": "what kind each part is", "_rels/.rels": "where to start reading", "docProps/app.xml": "which program wrote the file",
            "docProps/core.xml": "author and dates", "xl/_rels/workbook.xml.rels": "links from the workbook to its parts", "xl/styles.xml": "fonts, fills and number formats",
            "xl/theme/theme1.xml": "colours and fonts of the theme", "xl/workbook.xml": "the list of sheets", "xl/worksheets/sheet1.xml": "the cells of the first sheet"}


@need(1.95)
def v_xlsx_zip(s, x, y, w, h, ns, out):
    names = ns["names"]
    rows = [["Part inside the zip", "What it holds"]] + [[n, ZIP_ROLE.get(n, "another part")] for n in names]
    table(s, x, y, w * 0.68, rows, [3.0, 2.8], rowh=min(0.2, h / len(rows)), mono_cols=(0,), fs=8.5)
    bx = x + w * 0.72
    label_shape(s, bx, y + 0.05, w * 0.28, 0.5, "book.xlsx", C["tealLight"], C["ink"], size=10, line=C["line"], font=MONO)
    arrow(s, bx + w * 0.14, y + 0.57, bx + w * 0.14, y + 0.85, C["muted"], 1.2)
    label_shape(s, bx, y + 0.87, w * 0.28, 0.5, "a zip of %d\nXML parts" % len(names), C["amberLight"], C["ink"], size=10, line=C["line"])
    arrow(s, bx + w * 0.14, y + 1.39, bx + w * 0.14, y + 1.67, C["muted"], 1.2)
    label_shape(s, bx, y + 1.69, w * 0.28, 0.3, "openpyxl reads it", C["greenLight"], C["ink"], size=9.5, line=C["line"])


@need(1.3)
def v_sheets(s, x, y, w, h, ns, out):
    wb = ns["wb"]
    tabs(s, x, y + 0.2, w, wb.sheetnames, wb.active.title)
    note(s, x, y - 0.05, w, "the tabs of the reloaded workbook, with their index", fs=9.5)
    ai = wb.sheetnames.index(wb.active.title)
    bw = min(1.9, (w - 0.1 * (len(wb.sheetnames) - 1)) / len(wb.sheetnames))
    arrow(s, x + ai * (bw + 0.1) + bw / 2, y + 0.68, x + 1.8, y + 0.84, C["amber"], 1.5)
    chip(s, x, y + 0.85, 3.6, 0.3, "wb.active.title = %r" % wb.active.title, "amber", fs=9.5)
    chip(s, x + 3.8, y + 0.85, 5.0, 0.3, "wb.sheetnames = %s" % short(wb.sheetnames, 44), "plain", fs=9.5)


@need(1.45)
def v_cell_read(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    cells = {"%s%d" % (c, r): ws["%s%d" % (c, r)].value for c in "AB" for r in (1, 2, 3)}
    fills = {"A1": C["tealLight"], "B2": C["amberLight"], "B3": C["greenLight"]}
    grid(s, x, y, w * 0.5, cells, 3, 3, fills, fs=10, rowh=0.3, width_of=lambda c: 1.3 if c != "C" else 0.8)
    yy = y + 0.05
    for t, k in (("ws['A1']  =  %r" % ws["A1"].value, "teal"), ("ws.cell(row=2, column=2)  =  %r" % ws.cell(row=2, column=2).value, "amber"),
                 ("ws['B3'].coordinate  =  %r" % ws["B3"].coordinate, "green")):
        chip(s, x + w * 0.54, yy, w * 0.46, 0.3, t, k, fs=9.5)
        yy += 0.4
    note(s, x + w * 0.54, yy, w * 0.46, "max_row = %d, max_column = %d: the used area" % (ws.max_row, ws.max_column), fs=9.5)


@need(1.25)
def v_col_letters(s, x, y, w, h, ns, out):
    g, ci = ns["get_column_letter"], ns["column_index_from_string"]
    nums = (1, 2, 26, 27, 52, 53, 702, 703, 900)
    rows = [["number"] + [str(n) for n in nums], ["letters"] + [g(n) for n in nums]]
    table(s, x, y, w, rows, [1.0] + [0.9] * len(nums), rowh=0.32, mono_cols=(), bold_cols=(0,), fs=10, align_cols={j: PP_ALIGN.CENTER for j in range(len(nums) + 1)})
    chip(s, x, y + 0.8, 3.6, 0.32, "XFD = column %d, the last one" % ci("XFD"), "amber", fs=9.5)
    chip(s, x + 3.8, y + 0.8, 4.0, 0.32, "number 0 is refused: ValueError", "red", fs=9.5)
    note(s, x, y + 1.15, w, "letters count like digits without a zero: Z, then AA", fs=9.5)


@need(1.5)
def v_slices(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    cells = {"%s%d" % (c, r): ws["%s%d" % (c, r)].value for c in "ABC" for r in (1, 2, 3)}
    fills = {}
    for c in "ABC":
        for r in (1, 2):
            fills["%s%d" % (c, r)] = C["tealLight"]
    for r in (1, 2, 3):
        fills["B%d" % r] = C["greenLight"] if r < 3 else C["amberLight"]
    grid(s, x, y, w * 0.5, cells, 3, 3, fills, fs=10, rowh=0.3, width_of=lambda c: 1.2)
    chip(s, x + w * 0.54, y + 0.05, w * 0.46, 0.3, "ws['A1':'C2']: the teal cells", "teal", fs=9.5)
    chip(s, x + w * 0.54, y + 0.45, w * 0.46, 0.3, "ws['B']: column B, amber and green", "amber", fs=9.5)
    chip(s, x + w * 0.54, y + 0.85, w * 0.46, 0.3, "ws.rows, ws.columns: generators", "grey", fs=9.5)


@need(1.25)
def v_dates(s, x, y, w, h, ns, out):
    kinds = {"n": "number", "s": "text", "d": "date", "f": "formula"}
    rows = [["Cell", "Value", "data_type", "Python type", "A person would call it"]]
    cf = {}
    for i, c in enumerate(ns["ws"][1], 1):
        rows.append([c.coordinate, str(c.value), c.data_type, type(c.value).__name__, kinds.get(c.data_type, "other")])
        cf[(i, 2)] = {"n": C["tealLight"], "s": C["amberLight"], "d": C["greenLight"]}.get(c.data_type, C["grey"])
    table(s, x, y, w, rows, [0.9, 2.6, 1.2, 1.4, 2.0], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2, 3), cell_fill=cf, fs=10)
    note(s, x, y + 1.3, w, "SEPT2 stays text: only a spreadsheet application would turn it into a date", fs=9.5)


@need(1.7)
def v_touching(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    before, after = int(lines[0].split()[0]), int(lines[1].split()[0])
    tb(s, x, y - 0.02, w * 0.4, 0.22, "max_row of the sheet", 9.5, C["muted"], italic=True)
    chart(s, "col", x, y + 0.2, w * 0.42, max(h - 0.2, 1.3), ["before looking", "after cell(row=40)"], [("max_row", [before, after])], fs=9, legend=False, gap=60, vmax=50, major=10)
    rows = [["Moment", "dimensions"], ["before", lines[0].split(" ", 1)[1]], ["after", lines[1].split(" ", 1)[1]]]
    table(s, x + w * 0.47, y + 0.1, w * 0.53, rows, [1.2, 1.6], rowh=0.34, mono_cols=(1,), bold_cols=(0,), fs=10)
    note(s, x + w * 0.47, y + 1.25, w * 0.53, "A40 holds None, but the cell now exists", fs=9.5)


@need(1.75)
def v_read_only(s, x, y, w, h, ns, out):
    rows = [["row of the sheet", "column A", "column B"]] + [["row %d" % (i + 2), str(a), str(b)] for i, (a, b) in enumerate(ns["rows"])]
    table(s, x, y + 0.22, w * 0.5, rows, [1.6, 1.0, 1.0], rowh=min(0.3, (h - 0.22) / len(rows)), mono_cols=(1, 2), bold_cols=(0,), fs=9.5)
    tb(s, x, y - 0.02, w * 0.5, 0.22, "iter_rows(min_row=2, max_row=4, values_only=True) gave:", 9, C["muted"], italic=True)
    tb(s, x + w * 0.55, y - 0.02, w * 0.45, 0.22, "memory on the real census file (research finding F8)", 9, C["muted"], italic=True)
    chart(s, "col", x + w * 0.55, y + 0.2, w * 0.45, max(h - 0.2, 1.4), ["every cell in memory", "read_only, row by row"], [("MB", [114, 11])], fs=9, legend=False, gap=60, vmax=140, major=40)


# ------------------------------------------------------------------ part 2
@need(1.4)
def v_census_read(s, x, y, w, h, ns, out):
    sheet = ns["sheet"]
    cells = {"%s%d" % (c, r): sheet["%s%d" % (c, r)].value for c in "ABCD" for r in range(1, sheet.max_row + 1)}
    fills = {"%s1" % c: C["grey"] for c in "ABCD"}
    for r in range(2, sheet.max_row + 1):
        for c in "BCD":
            fills["%s%d" % (c, r)] = C["tealLight"]
    grid(s, x, y, w * 0.62, cells, 4, sheet.max_row, fills, fs=9.5, rowh=0.27, width_of=lambda c: 1.7 if c == "A" else 1.1)
    chip(s, x + w * 0.66, y + 0.05, w * 0.34, 0.3, "row 1: the headers", "grey", fs=9.5)
    chip(s, x + w * 0.66, y + 0.45, w * 0.34, 0.3, "B, C, D: read by the loop", "teal", fs=9.5)
    note(s, x + w * 0.66, y + 0.85, w * 0.34, "the loop printed %d rows, 2 to %d" % (len(out.splitlines()), sheet.max_row), fs=9.5)


@need(1.45)
def v_census_tally(s, x, y, w, h, ns, out):
    cd = ns["county_data"]
    rows = [["State", "County", "Tracts", "Population"]]
    pops, names = [], []
    for st in sorted(cd):
        for co, d in sorted(cd[st].items()):
            rows.append([st, co, str(d["tracts"]), "{:,}".format(d["pop"])])
            pops.append(d["pop"])
            names.append(co)
    table(s, x, y, w * 0.55, rows, [0.7, 1.6, 0.8, 1.2], rowh=min(0.32, h / len(rows)), mono_cols=(), bold_cols=(0,), fs=10, align_cols={2: PP_ALIGN.RIGHT, 3: PP_ALIGN.RIGHT})
    tb(s, x + w * 0.6, y - 0.02, w * 0.4, 0.22, "population by county", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.6, y + 0.2, w * 0.4, max(h - 0.2, 1.3), names, [("population", pops)], fs=9, legend=False, gap=60, vmax=8000, major=2000, number_format="#,##0")


@need(1.6)
def v_census_file(s, x, y, w, h, ns, out):
    flow(s, x, y, w, ["county_data\n(a dictionary)", "pprint.pformat\n(text)", "'allData = ...'\n(valid Python)", "exec(text)\nallData is back"], ["plain", "teal", "amber", "green"], h=0.58, gap=0.4, fs=10)
    lines = out.splitlines()
    tb(s, x, y + 0.75, w, 0.5, "\n".join(lines[:2]), 9.5, C["ink"], font=MONO, name="printed text")
    chip(s, x, y + 1.3, 3.8, 0.3, "allData['AK']['Anchorage']['pop'] = %s" % lines[-1], "green", fs=9.5)


@need(1.25)
def v_produce_update(s, x, y, w, h, ns, out):
    ws, up = ns["ws"], ns["updates"]
    rows = [["PRODUCE", "COST PER POUND", "POUNDS SOLD", "TOTAL (a formula, still text)", "price"]]
    cf = {}
    for i, r in enumerate(range(2, ws.max_row + 1), 1):
        name = ws.cell(row=r, column=1).value
        rows.append([name, "%.2f" % ws.cell(row=r, column=2).value, str(ws.cell(row=r, column=3).value), str(ws.cell(row=r, column=4).value),
                     "corrected" if name in up else "unchanged"])
        if name in up:
            for j in (1, 4):
                cf[(i, j)] = C["amberLight"]
    table(s, x, y, w, rows, [1.5, 1.6, 1.4, 2.6, 1.2], rowh=min(0.3, h / len(rows)), mono_cols=(3,), cell_fill=cf, bold_cols=(0,), fs=10, align_cols={1: PP_ALIGN.RIGHT, 2: PP_ALIGN.RIGHT})
    note(s, x, y + 0.3 * len(rows) + 0.02, w, "the amber cells were replaced; the total formulas were not touched, and they hold no result", fs=9.5)


# ------------------------------------------------------------------ part 3
@need(1.3)
def v_write_workbook(s, x, y, w, h, ns, out):
    steps = ["Workbook()\n1 sheet", "title and A1\nSpam Bacon Eggs Sheet", "create_sheet x2\n3 sheets", "remove\n%d sheets" % len(ns["wb"].sheetnames), "save and load\n%d sheets" % len(ns["copy"].sheetnames)]
    flow(s, x, y, w, steps, ["plain", "plain", "teal", "amber", "green"], h=0.6, gap=0.3, fs=9)
    tabs(s, x, y + 0.85, w * 0.7, ns["copy"].sheetnames, ns["copy"].active.title, h=0.42)
    chip(s, x + w * 0.74, y + 0.9, w * 0.26, 0.34, "A1 = %r" % ns["copy"]["Spam Bacon Eggs Sheet"]["A1"].value, "green", fs=9)


@need(1.7)
def v_formula_string(s, x, y, w, h, ns, out):
    kept, cached = ns["kept"], ns["cached"]
    rows = [["Cell", "what Python stored", "what data_only=True reads"]]
    cf = {}
    for i, c in enumerate(("A1", "A2", "A3"), 1):
        rows.append([c, str(kept[c].value), str(cached[c].value)])
    cf[(3, 2)] = C["redLight"]
    cf[(3, 1)] = C["amberLight"]
    table(s, x, y, w * 0.52, rows, [0.7, 1.7, 2.0], rowh=0.34, mono_cols=(0, 1, 2), cell_fill=cf, fs=10)
    flow(s, x + w * 0.56, y, w * 0.44, ["openpyxl writes\n%s" % ns["kept"]["A3"].value, "no program opened\nthe file", "the cached result\nis %s" % cached["A3"].value], ["amber", "grey", "red"], h=0.62, gap=0.0 + 0.2, fs=8.5)
    note(s, x, y + 1.45, w, "a spreadsheet program calculates the formula and stores its result when it saves the file", fs=9.5)


@need(1.5)
def v_round_halves(s, x, y, w, h, ns, out):
    rows = [["Exact half as text", "Python round(x, 2)", "spreadsheet ROUND (half up)", "the same?"]]
    cf = {}
    for i, line in enumerate(out.splitlines(), 1):
        t, py, up = line.split()
        same = float(py) == float(up)
        rows.append([t, py, up, "yes" if same else "NO"])
        cf[(i, 3)] = C["greenLight"] if same else C["redLight"]
    table(s, x, y, w * 0.72, rows, [1.6, 1.6, 2.1, 1.0], rowh=min(0.3, h / len(rows)), mono_cols=(0, 1, 2), cell_fill=cf, fs=10, align_cols={3: PP_ALIGN.CENTER})
    label_shape(s, x + w * 0.76, y, w * 0.24, 0.62, "Python rounds\nthe binary float", C["tealLight"], C["ink"], size=9.5, line=C["line"])
    label_shape(s, x + w * 0.76, y + 0.8, w * 0.24, 0.62, "a spreadsheet rounds\nthe decimal shown", C["amberLight"], C["ink"], size=9.5, line=C["line"])


@need(1.9)
def v_insert_rows(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    cells = {}
    fills = {}
    for r in range(1, 9):
        for c in "AB":
            v = ws["%s%d" % (c, r)].value
            cells["%s%d" % (c, r)] = "" if v is None else v
    for c in "AB":
        for r in (3, 4):
            fills["%s%d" % (c, r)] = C["amberLight"]
    fills["B8"] = C["redLight"]
    grid(s, x, y, w * 0.45, cells, 2, 8, fills, fs=8.5, rowh=0.19, width_of=lambda c: 1.0 if c == "A" else 1.6)
    chip(s, x + w * 0.5, y + 0.05, w * 0.5, 0.3, "amber: the two inserted blank rows", "amber", fs=9.5)
    chip(s, x + w * 0.5, y + 0.45, w * 0.5, 0.3, "red: B8 holds %s" % ws["B8"].value, "red", fs=9.5)
    note(s, x + w * 0.5, y + 0.85, w * 0.5, "the sum moved from B6 to B8,", fs=9.5)
    note(s, x + w * 0.5, y + 1.07, w * 0.5, "but it still adds B1:B5, not B1:B7", fs=9.5)


# ------------------------------------------------------------------ part 4
@need(1.35)
def v_mult_table(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    cells, fills = {}, {}
    for r in range(1, 6):
        for c in "ABCDE":
            v = ws["%s%d" % (c, r)].value
            cells["%s%d" % (c, r)] = "" if v is None else v
            if (r == 1 or c == "A") and v is not None:
                fills["%s%d" % (c, r)] = C["tealLight"]
    grid(s, x, y, w * 0.5, cells, 5, 5, fills, fs=9.5, rowh=0.22, width_of=lambda c: 1.0)
    chip(s, x + w * 0.55, y + 0.05, w * 0.45, 0.3, "teal: the headings, in bold", "teal", fs=9.5)
    chip(s, x + w * 0.55, y + 0.45, w * 0.45, 0.3, "A1 stays empty: %r" % ws["A1"].value, "grey", fs=9.5)
    note(s, x + w * 0.55, y + 0.85, w * 0.45, "cell (row i, column j) = i * j", fs=9.5)


@need(1.45)
def v_fonts(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    rows = [["Cell", "font.name", "font.sz", "bold", "italic"]]
    for c in ("A1", "B3", "C5"):
        f = ws[c].font
        rows.append([c, str(f.name), str(f.sz), str(bool(f.b)), str(bool(f.i))])
    cf = {(1, 1): C["amberLight"], (2, 2): C["amberLight"]}
    table(s, x, y, w * 0.55, rows, [0.7, 1.9, 0.9, 0.8, 0.8], rowh=0.32, mono_cols=(0, 1, 2), cell_fill=cf, fs=10)
    note(s, x, y + 1.35, w * 0.55, "amber: nothing was given, so nothing is stored", fs=9.5)
    f1, f2 = ws["A1"].font, ws["B3"].font
    label_shape(s, x + w * 0.6, y, w * 0.4, 0.55, "Hello, world!", C["card"], C["ink"], size=min(f1.sz, 18), line=C["line"], radius=0.05)
    label_shape(s, x + w * 0.6, y + 0.7, w * 0.4, 0.45, "Bold Times New Roman", C["card"], C["ink"], size=12, bold=bool(f2.b), line=C["line"], font=f2.name, radius=0.05)
    note(s, x + w * 0.6, y + 1.2, w * 0.4, "sample text; A1 is 24 pt here shown at 18", fs=9)


@need(1.7)
def v_dimensions(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    # the sheet's columns drawn at their widths (default 8.43 characters), the hidden one marked; rows 3 to 6 at their heights (default 15 points)
    dflt_w, dflt_h = 8.43, 15.0
    cols = ["A", "B", "C", "D"]
    wid = {c: (ws.column_dimensions[c].width if c in ws.column_dimensions and ws.column_dimensions[c].customWidth else dflt_w) for c in cols}
    hid = {c: bool(c in ws.column_dimensions and ws.column_dimensions[c].hidden) for c in cols}
    scale = 0.075
    xx = x + 0.45
    for c in cols:
        ww = 0.12 if hid[c] else wid[c] * scale
        label_shape(s, xx, y, ww, 0.28, "" if hid[c] else c, C["amberLight"] if hid[c] else C["tealLight"], C["ink"], size=10, line=C["line"], radius=0.05)
        if hid[c]:
            tb(s, xx - 0.1, y + 0.3, 1.0, 0.22, "D hidden", 9, C["muted"], italic=True)
        xx += ww + 0.03
    yy = y + 0.55
    for r in (4, 5, 6):
        hh = ((ws.row_dimensions[r].height if r in ws.row_dimensions and ws.row_dimensions[r].height else dflt_h)) * 0.0085
        label_shape(s, x, yy, 0.4, max(hh, 0.2), str(r), C["tealLight"], C["ink"], size=10, line=C["line"], radius=0.05)
        yy += max(hh, 0.2) + 0.03
    rows = [["Setting", "Value from the run"], ["row_dimensions[5].height", "%s points" % ws.row_dimensions[5].height], ["column_dimensions['B'].width", "%s characters" % ws.column_dimensions["B"].width],
            ["column_dimensions['D'].hidden", str(ws.column_dimensions["D"].hidden)]]
    table(s, x + w * 0.45, y, w * 0.55, rows, [2.6, 1.9], rowh=0.32, mono_cols=(0, 1), bold_cols=(), fs=9.5)
    note(s, x + w * 0.45, y + 1.4, w * 0.55, "column B is wider, row 5 is taller, column D has no width", fs=9.5)


@need(1.65)
def v_merge(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    note(s, x, y - 0.05, w * 0.4, "after merge_cells('F1:I3')", fs=9.5)
    label_shape(s, x, y + 0.2, w * 0.4, 0.9, "F1:I3: one real cell\n%r" % ws["F1"].value, C["tealLight"], C["ink"], size=9.5, line=C["line"], radius=0.05)
    arrow(s, x + w * 0.42, y + 0.65, x + w * 0.52, y + 0.65, C["muted"], 1.5)
    note(s, x + w * 0.54, y - 0.05, w * 0.46, "after unmerge_cells('F1:I3'): twelve cells again", fs=9.5)
    cells = {"F1": ws["F1"].value}
    fills = {"F1": C["amberLight"]}
    grid(s, x + w * 0.54, y + 0.2, w * 0.46, cells, 4, 3, fills, fs=7.5, rowh=0.24, first_col=6, width_of=lambda c: 1.0)
    note(s, x, y + 1.2, w, "type of G2 while merged: MergedCell, read-only; after: %s" % out.splitlines()[-1].split()[-1], fs=9.5)


@need(1.5)
def v_freeze(s, x, y, w, h, ns, out):
    lw = (w - 0.4) / 3
    for k, line in enumerate(out.splitlines()):
        setting, xs, ys = line.split()
        fc = int(float(xs)) if xs != "None" else 0
        fr = int(float(ys)) if ys != "None" else 0
        fills = {}
        for r in range(1, 5):
            for j in range(1, 5):
                if j <= fc or r <= fr:
                    fills["%s%d" % (get_column_letter(j), r)] = C["tealLight"]
        xx = x + k * (lw + 0.2)
        tb(s, xx, y - 0.04, lw, 0.22, "freeze_panes = %r" % setting, 9.5, C["ink"], font=MONO, name="setting")
        grid(s, xx, y + 0.2, lw, {}, 4, 4, fills, fs=7.5, rowh=0.22, colw0=0.3, width_of=lambda c: 1.0)
        note(s, xx, y + 1.4, lw, "frozen: %d column(s), %d row(s)" % (fc, fr), fs=9)


# ------------------------------------------------------------------ part 5
@need(1.5)
def v_chart_build(s, x, y, w, h, ns, out):
    ws = ns["ws"]
    vals = [ws["A%d" % i].value for i in range(1, 11)]
    tb(s, x, y - 0.02, w * 0.5, 0.22, "the chart the program asked for: My Chart, series 'First series'", 9.5, C["muted"], italic=True)
    chart(s, "col", x, y + 0.2, w * 0.58, max(h - 0.2, 1.4), [str(i) for i in range(1, 11)], [("First series", vals)], fs=8.5, legend=False, gap=40, vmax=120, major=40)
    chip(s, x + w * 0.62, y + 0.1, w * 0.38, 0.3, "ref = %s" % ns["ref"], "teal", fs=9)
    chip(s, x + w * 0.62, y + 0.5, w * 0.38, 0.3, "%d chart on the sheet" % len(ns["ws"]._charts), "green", fs=9.5)
    note(s, x + w * 0.62, y + 0.9, w * 0.38, "Excel or LibreOffice draws the bars", fs=9.5)


@need(1.7)
def v_reference_order(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    fills = {}
    for r in range(1, 11):
        fills["B%d" % r] = C["tealLight"]
    for j in range(1, 11):
        fills["%s2" % get_column_letter(j)] = C["amberLight"] if j != 2 else C["greenLight"]
    grid(s, x, y, w * 0.6, {}, 10, 6, fills, fs=7, rowh=0.2, colw0=0.4, width_of=lambda c: 1.0)
    note(s, x, y + 1.45, w * 0.6, "rows 1 to 6 of 10 are drawn; column B goes on down to row 10", fs=9)
    chip(s, x + w * 0.64, y + 0.05, w * 0.36, 0.3, "Reference(ws, 2, 1, 2, 10)", "teal", fs=9)
    chip(s, x + w * 0.64, y + 0.4, w * 0.36, 0.28, lines[0], "teal", fs=9)
    chip(s, x + w * 0.64, y + 0.82, w * 0.36, 0.3, "Reference(ws, 1, 2, 10, 2)", "amber", fs=9)
    chip(s, x + w * 0.64, y + 1.17, w * 0.36, 0.28, lines[1], "amber", fs=9)
    note(s, x + w * 0.64, y + 1.5, w * 0.36, "min_col, min_row, max_col, max_row", fs=9)


@need(1.4)
def v_chart_parts(s, x, y, w, h, ns, out):
    names = ns["names"]
    flow(s, x, y, w, ["ws.add_chart(chart)", "ws.parent.save(buf)", "the zip holds"], ["plain", "teal", "amber"], h=0.5, gap=0.4, fs=10, font_mono=True)
    yy = y + 0.65
    for n in [n for n in names if "chart" in n or "drawing" in n]:
        chip(s, x + 0.3, yy, 4.6, 0.28, n, "amber" if n.startswith("xl/charts") else "plain", fs=9.5)
        yy += 0.33
    label_shape(s, x + 5.3, y + 0.7, w - 5.3, 0.62, "an application draws\nthe bars from the XML", C["greenLight"], C["ink"], size=10, line=C["line"])


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
