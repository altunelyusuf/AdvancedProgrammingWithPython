#!/usr/bin/env python3
"""SEN0414 chapter 6 (Lists) deck v3.0.0 - the generator. A NEW tool file (nothing committed is edited).
Builds 03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_0_0.pptx and the chapter-code manifest 03-materials/ch06/page/chapter_code_ch06_v1_0_0.json
from deck_content_v3_0_0.py. Every code example is EXECUTED here under Python 3.14 and every table, chart and diagram of a result is read from that run.
Usage: python3 deck_build_v3_0_0.py [python3.14 path]        (python-pptx 1.0.2)"""
__version__ = "3.0.0"
import ast, hashlib, io, json, os, re, subprocess, sys, tempfile, contextlib
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_TICK_LABEL_POSITION
from pptx.oxml.ns import qn
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
import deck_content_v3_0_0 as C

PY = sys.argv[1] if len(sys.argv) > 1 else "/root/.local/bin/python3.14"
OUT = os.path.join(REPO, "03-materials", "ch06", "SEN0414_Ch06_Lists_3e_v3_0_0.pptx")
MAN = os.path.join(REPO, "03-materials", "ch06", "page", "chapter_code_ch06_v1_0_0.json")
ASSETS = os.path.join(REPO, "03-materials", "ch06", "assets")

# one smooth colour scheme, the look of the chapter's earlier decks (cream page, teal, orange, ink; dark code panels)
BG, ORANGE, TEAL, INK, MUTED, PANEL = "FAF6EF", "D97A14", "2F6D62", "2B2622", "6E655C", "23272E"
CARD, TEAL_L, ORANGE_L, WHITE = "FFFFFF", "DCEBE6", "F8E3CC", "FFFFFF"
HEAD, BODY, MONO = "Cambria", "Calibri", "Courier New"
rgb = lambda h: RGBColor.from_string(h)
WARN = []

# ------------------------------------------------------------------------------------------------ running the examples
def run_code(code):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "example.py")
        open(f, "w", encoding="utf-8").write(code + "\n")
        r = subprocess.run([PY, "-I", f], capture_output=True, text=True, cwd=d, timeout=120)
    assert r.returncode == 0, "example failed:\n%s\n%s" % (code, r.stderr)
    return r.stdout


def code_of(key):
    return "\n".join(l for box in C.EX[key]["boxes"] for l in box)


def exec_ns(code):
    ns = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(code, ns)
    return ns


RUN = {}
RUN_EXTRA = {}
for k in C.ORDER:
    out = run_code(code_of(k))
    RUN[k] = out.split("\n")[:-1] if out.endswith("\n") else out.split("\n")

RUN_EXTRA["matrix"] = lit_ = ast.literal_eval(run_code(code_of("matrix") + "\nprint(ctr)").split("\n")[-2])

# ------------------------------------------------------------------------------------------------ text estimation (as the overlap check does it)
IN = 914400.0


def est_lines(text, width_in, size, mono=False):
    a = (0.60 if mono else 0.50) * size / 72.0
    lines, cur = 1, 0.0
    if not text:
        return 1
    for w in text.split(" "):
        wl = len(w) * a
        if cur == 0:
            cur = wl
        elif cur + a + wl <= width_in:
            cur += a + wl
        else:
            lines += 1
            cur = wl
    return lines


def est_h(paras, width_in, size, mono=False, ins=(0.08, 0.04, 0.08, 0.04)):
    inner = width_in - ins[0] - ins[2]
    tot = 0.0
    for p in paras:
        runs = [(p, {})] if isinstance(p, str) else p
        text = "".join(t for t, _ in runs)
        sz = max([o.get("size", size) for _, o in runs] or [size])
        tot += est_lines(text, inner, sz, mono) * sz * 1.2 / 72.0
    return tot + ins[1] + ins[3]


# ------------------------------------------------------------------------------------------------ shape helpers
def fill_tf(tf, paras, size=12, color=INK, bold=False, italic=False, font=BODY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
            ins=(0.08, 0.04, 0.08, 0.04), space_after=0, wrap=True):
    tf.word_wrap = wrap
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left, tf.margin_top, tf.margin_right, tf.margin_bottom = [Inches(v) for v in ins]
    tf.vertical_anchor = anchor
    first = True
    for para in paras:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.space_after = Pt(space_after)
        p.space_before = Pt(0)
        runs = [(para, {})] if isinstance(para, str) else para
        for text, o in runs:
            r = p.add_run()
            r.text = text
            f = r.font
            f.size = Pt(o.get("size", size))
            f.bold = o.get("bold", bold)
            f.italic = o.get("italic", italic)
            f.name = o.get("font", font)
            f.color.rgb = rgb(o.get("color", color))
            if "link" in o:
                r.hyperlink.address = o["link"]


def tb(sl, x, y, w, h, paras, name=None, check=True, mono=False, **kw):
    if isinstance(paras, str):
        paras = [paras]
    s = sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        s.name = name
    fill_tf(s.text_frame, paras, **kw)
    if check:
        need = est_h(paras, w, kw.get("size", 12), mono, kw.get("ins", (0.08, 0.04, 0.08, 0.04)))
        if need > h + 0.05:
            WARN.append("text too tall (%.2f > %.2f) slide %s: %s" % (need, h, SLIDE_NO[0], str(paras)[:60]))
    return s


def card(sl, x, y, w, h, paras, fill=CARD, line=None, shape=MSO_SHAPE.ROUNDED_RECTANGLE, name=None, check=True, mono=False, radius=0.12, **kw):
    s = sl.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        s.name = name
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.shadow.inherit = False
    if fill:
        s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line); s.line.width = Pt(1)
    else:
        s.line.fill.background()
    if isinstance(paras, str):
        paras = [paras]
    kw.setdefault("anchor", MSO_ANCHOR.MIDDLE)
    kw.setdefault("align", PP_ALIGN.CENTER)
    fill_tf(s.text_frame, paras, **kw)
    if check and paras != [""]:
        need = est_h(paras, w, kw.get("size", 12), mono, kw.get("ins", (0.08, 0.04, 0.08, 0.04)))
        if need > h + 0.05:
            WARN.append("card text too tall (%.2f > %.2f) slide %s: %s" % (need, h, SLIDE_NO[0], str(paras)[:60]))
    return s


def bar(sl, x, y, w, h, color):
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = rgb(color); s.line.fill.background(); s.shadow.inherit = False
    return s


def arrow(sl, x1, y1, x2, y2, color=MUTED, width=1.75):
    c = sl.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
    ln = c.line._get_or_add_ln()
    t = etree.SubElement(ln, qn("a:tailEnd"))
    t.set("type", "triangle")
    return c


def node(sl, x, y, w, h, text, fill=TEAL_L, color=INK, size=11, bold=False, line=None, font=BODY, **kw):
    paras = text if isinstance(text, list) else [text]
    return card(sl, x, y, w, h, paras, fill=fill, line=line, size=size, color=color, bold=bold, font=font, ins=(0.04, 0.02, 0.04, 0.02),
                mono=(font == MONO), **kw)


SLIDE_NO = [0]
TOTAL = [0]


def new_slide(prs, title, chip=True, title_size=22):
    sl = prs.slides.add_slide(prs.slide_layouts[5])  # Title Only
    bg = sl.background.fill
    bg.solid(); bg.fore_color.rgb = rgb(BG)
    t = sl.shapes.title
    t.left, t.top, t.width, t.height = Inches(1.05 if chip else 0.5), Inches(0.17), Inches(8.6 if chip else 9.0), Inches(0.5)
    fill_tf(t.text_frame, [title], size=title_size, bold=True, font=HEAD, color=INK, anchor=MSO_ANCHOR.MIDDLE, ins=(0.04, 0.02, 0.04, 0.02))
    if est_lines(title, (8.6 if chip else 9.0) - 0.08, title_size) > 1:
        WARN.append("title wraps, slide %s: %s" % (SLIDE_NO[0], title))
    if chip:
        c = card(sl, 0.4, 0.22, 0.58, 0.38, [">>>"], fill=ORANGE, size=13, bold=True, font=MONO, color=WHITE, name="brand chip", mono=True, ins=(0.02, 0.02, 0.02, 0.02))
    return sl


def number(sl):
    tb(sl, 8.65, 5.28, 1.0, 0.26, ["%d / %d" % (SLIDE_NO[0], TOTAL[0])], size=10, color=MUTED, align=PP_ALIGN.RIGHT, name="slide number", ins=(0.02, 0.02, 0.02, 0.02))


def takeaway(sl, text):
    card(sl, 0.4, 5.0, 8.1, 0.32, [text], fill=TEAL, size=12, bold=True, color=WHITE, align=PP_ALIGN.LEFT, name="takeaway", radius=0.3, ins=(0.15, 0.02, 0.1, 0.02))


def lede(sl, text, y=0.68, h=0.32):
    assert len(text.split()) <= 30, text
    tb(sl, 0.4, y, 9.25, h, [text], size=11, italic=True, color=TEAL, name="lede")


def notes(sl, text):
    assert len(text.split()) <= 60, (len(text.split()), text)
    sl.notes_slide.notes_text_frame.text = text


def alt(shape, text):
    shape._element.xpath(".//p:cNvPr")[0].set("descr", text)


# ------------------------------------------------------------------------------------------------ code boxes
KW = {"def", "for", "in", "if", "else", "return", "import", "from", "try", "except", "as", "not", "and", "or", "is", "del", "lambda", "while", "True", "False", "None"}
BI = {"print", "len", "range", "list", "sorted", "enumerate", "sum", "max", "bool", "type", "repr", "id", "int", "str"}
TOK = re.compile(r"(#.*$)|('[^']*'|\"[^\"]*\")|(\b\d+(?:\.\d+)?\b)|([A-Za-z_][A-Za-z_0-9]*)|(\s+)|(.)")


def code_runs(line, size):
    runs = [(">>> ", {"size": size, "color": "7EE787", "font": MONO, "bold": True})]
    for m in TOK.finditer(line):
        t = m.group(0)
        if m.group(1):
            col = "8B949E"
        elif m.group(2):
            col = "A5D6FF"
        elif m.group(3):
            col = "79C0FF"
        elif m.group(4):
            col = "FF7B72" if t in KW else ("D2A8FF" if t in BI else "E6EDF3")
        else:
            col = "E6EDF3"
        runs.append((t, {"size": size, "color": col, "font": MONO}))
    return runs


def code_size(lines, w, target):
    room = (w - 0.16) * 72.0
    m = max(len(l) + 4 for l in lines)
    s = min(target, room / (0.6 * m))
    s = int(s * 4) / 4.0
    assert s >= 9.0, "code too wide: %s" % lines
    return s


def code_box(sl, x, y, w, lines, target=11.0, minh=0.0):
    size = code_size(lines, w, target)
    h = max(minh, len(lines) * size * 1.2 / 72.0 + 0.16)
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.name = "code"
    s.shadow.inherit = False
    s.fill.solid(); s.fill.fore_color.rgb = rgb(PANEL)
    s.line.fill.background()
    fill_tf(s.text_frame, [code_runs(l, size) for l in lines], size=size, font=MONO, color="E6EDF3", anchor=MSO_ANCHOR.TOP, ins=(0.08, 0.08, 0.08, 0.08), wrap=True)
    return s, h, size


# ------------------------------------------------------------------------------------------------ result visuals
def table(sl, x, y, w, header, rows, size=10, mono_cols=(), name="result table", maxw=None, rowh=0.25, align_cols=()):
    """a native table; the column widths follow the longest cell; returns (shape, width, height)"""
    nc = len(header)
    ad = lambda c, sz: (0.60 if c in mono_cols else 0.50) * sz / 72.0
    for sz in (size, size - 0.5, size - 1, size - 1.5):
        need = [max(len(str(r[c])) * ad(c, sz) for r in rows + [header]) + 0.22 for c in range(nc)]
        if sum(need) <= (maxw or w):
            break
    tw = sum(need)
    if tw < w and not maxw:
        k = w / tw
        need = [n * k for n in need]
        tw = w
    elif tw > (maxw or w) + 0.01:
        WARN.append("table too wide (%.2f > %.2f) slide %s %s" % (tw, maxw or w, SLIDE_NO[0], header))
    gf = sl.shapes.add_table(len(rows) + 1, nc, Inches(x), Inches(y), Inches(tw), Inches(rowh * (len(rows) + 1)))
    gf.name = name
    t = gf.table
    t.horz_banding = False
    for c in range(nc):
        t.columns[c].width = Inches(need[c])
    for r in range(len(rows) + 1):
        t.rows[r].height = Inches(rowh)
        for c in range(nc):
            cell = t.cell(r, c)
            txt = header[c] if r == 0 else str(rows[r - 1][c])
            cell.margin_left = cell.margin_right = Inches(0.09)
            cell.margin_top = cell.margin_bottom = Inches(0.025)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(TEAL if r == 0 else (CARD if r % 2 else "F1ECE2"))
            tf = cell.text_frame
            tf.word_wrap = False
            p = tf.paragraphs[0]
            p.text = ""
            run = p.add_run()
            run.text = txt
            run.font.size = Pt(sz)
            run.font.name = MONO if (c in mono_cols and r > 0) else BODY
            run.font.bold = r == 0
            run.font.color.rgb = rgb(WHITE if r == 0 else INK)
    alt(gf, "Result table: " + "; ".join("%s -> %s" % (r[0], r[-1]) for r in rows[:6]))
    return gf, tw, rowh * (len(rows) + 1)


def chart(sl, x, y, w, h, title, cats, vals, kind="bar", color=TEAL, name="result chart"):
    cd = CategoryChartData()
    cd.categories = cats
    cd.add_series(title, vals)
    ct = XL_CHART_TYPE.COLUMN_CLUSTERED if kind == "bar" else XL_CHART_TYPE.LINE_MARKERS
    gf = sl.shapes.add_chart(ct, Inches(x), Inches(y), Inches(w), Inches(h), cd)
    gf.name = name
    ch = gf.chart
    ch.has_legend = False
    ch.has_title = True
    ch.chart_title.text_frame.text = title
    for p in ch.chart_title.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(10.5); r.font.bold = True; r.font.name = BODY; r.font.color.rgb = rgb(INK)
    ch.font.size = Pt(9.5)
    ch.font.name = BODY
    ch.font.color.rgb = rgb(INK)
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.font.size = Pt(9.5)
    pl.data_labels.number_format = "General"
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END if kind == "bar" else XL_LABEL_POSITION.ABOVE
    ser = pl.series[0]
    if kind == "bar":
        pl.gap_width = 55
        ser.invert_if_negative = False
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = rgb(color)
    else:
        ser.format.line.color.rgb = rgb(color); ser.format.line.width = Pt(2.25)
        ser.smooth = False
        ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = rgb(ORANGE)
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.visible = False
    ch.category_axis.tick_labels.font.size = Pt(9)
    ch.category_axis.tick_label_position = XL_TICK_LABEL_POSITION.LOW
    alt(gf, "Chart: %s - %s" % (title, ", ".join("%s %s" % (a, b) for a, b in zip(cats, vals))))
    return gf


def lit(s):
    return ast.literal_eval(s)


def cut(s, n=34):
    return s if len(s) <= n else s[: n - 1] + "..."


# ---- diagrams (each one is drawn from the executed run) -------------------------------------------------------------------
def d_lockers(sl, x, y, w, h, key):
    items = lit("['cat', 'bat', 'rat', 'elephant']")
    n = len(items)
    bw = (w - 0.05 * (n - 1)) / n
    node(sl, x, y + 0.02, 0.8, 0.3, "spam", fill=ORANGE, color=WHITE, bold=True, size=11, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    arrow(sl, x + 0.4, y + 0.32, x + bw / 2, y + 0.62, ORANGE)
    for i, it in enumerate(items):
        node(sl, x + i * (bw + 0.05), y + 0.64, bw, 0.62, [[(it, {"bold": True, "size": 11})], [("%d | %d" % (i, i - n), {"size": 9.5, "color": MUTED})]], fill=TEAL_L, line=TEAL)
    tb(sl, x, y + 1.28, w, 0.24, ["door number | number from the end"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_grid(sl, x, y, w, h, key):
    g = lit("[['a', 'b'], ['c', 'd', 'e']]")
    for r, row in enumerate(g):
        yy = y + 0.12 + r * 0.62
        node(sl, x, yy + 0.03, 0.85, 0.34, "grid[%d]" % r, fill=ORANGE, color=WHITE, bold=True, size=10.5)
        arrow(sl, x + 0.85, yy + 0.2, x + 1.15, yy + 0.2, ORANGE)
        for c, it in enumerate(row):
            hot = (r, c) == (1, 2)
            node(sl, x + 1.2 + c * 0.62, yy, 0.55, 0.4, it, fill=ORANGE_L if hot else TEAL_L, line=ORANGE if hot else TEAL, bold=hot, size=12)
    tb(sl, x, y + 1.32, w, 0.24, ["grid[1][2] is the highlighted 'e'"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_ruler(sl, x, y, w, h, key):
    items = ["cat", "bat", "rat", "elephant"]
    n = len(items)
    bw = (w - 0.1) / n
    x0 = x + 0.05
    arrow(sl, x0 + 1 * bw, y + 0.32, x0 + 3 * bw, y + 0.32, ORANGE, 2.5)
    node(sl, x0 + 1 * bw + 0.1, y + 0.02, 2 * bw - 0.2, 0.28, "spam[1:3]", fill=ORANGE, color=WHITE, bold=True, size=10.5)
    for i, it in enumerate(items):
        hot = i in (1, 2)
        node(sl, x0 + i * bw + 0.02, y + 0.45, bw - 0.04, 0.5, it, fill=ORANGE_L if hot else TEAL_L, line=ORANGE if hot else TEAL, bold=hot, size=10.5)
    for i in range(n + 1):
        tb(sl, x0 + i * bw - 0.15, y + 1.0, 0.3, 0.26, [str(i)], size=10, color=MUTED, align=PP_ALIGN.CENTER, ins=(0.0, 0.0, 0.0, 0.0), name="mark")
    tb(sl, x, y + 1.28, w, 0.24, ["numbers sit between the items, like ruler marks"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_family(sl, x, y, w, h, key):
    node(sl, x + w / 2 - 0.8, y + 0.1, 1.6, 0.38, "sequence", fill=ORANGE, color=WHITE, bold=True, size=12)
    names = ["list [ ]", "str ' '", "tuple ( )", "range"]
    bw = (w - 0.15 * 3) / 4
    for i, nm in enumerate(names):
        bx = x + i * (bw + 0.15)
        arrow(sl, x + w / 2, y + 0.48, bx + bw / 2, y + 0.98, MUTED)
        node(sl, bx, y + 1.0, bw, 0.42, nm, fill=TEAL_L, line=TEAL, size=10.5)


def d_pets(sl, x, y, w, h, key):
    items = ["Zophie", "Pooka", "Fat-tail", "Pooka"]
    bw = (w - 0.05 * 3) / 4
    node(sl, x, y + 0.02, w - 0.3, 0.3, "pets.index('Pooka')  is  %s" % RUN[key][1], fill=ORANGE, color=WHITE, bold=True, size=10.5)
    arrow(sl, x + bw * 1.5 + 0.05, y + 0.32, x + bw * 1.5 + 0.05, y + 0.62, ORANGE)
    for i, it in enumerate(items):
        hot = it == "Pooka"
        node(sl, x + i * (bw + 0.05), y + 0.64, bw, 0.55, [[(it, {"bold": hot, "size": 10.5})], [("number %d" % i, {"size": 9, "color": MUTED})]], fill=ORANGE_L if hot else TEAL_L, line=ORANGE if hot else TEAL)
    tb(sl, x, y + 1.25, w, 0.24, ["count('Pooka') = %s" % RUN[key][3]], size=10, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_flow(sl, x, y, w, h, key):
    labs = ["spam is [] : false", "and stops here", "spam[0] never runs"]
    bw = (w - 0.3 * 2) / 3
    for i, t in enumerate(labs):
        node(sl, x + i * (bw + 0.3), y + 0.3, bw, 0.7, t, fill=ORANGE_L if i == 2 else TEAL_L, line=ORANGE if i == 2 else TEAL, size=10.5)
        if i < 2:
            arrow(sl, x + i * (bw + 0.3) + bw, y + 0.65, x + (i + 1) * (bw + 0.3), y + 0.65, MUTED)
    tb(sl, x, y + 1.1, w, 0.3, ["the guard saves us from an IndexError"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_sorting(sl, x, y, w, h, key):
    bw = (w - 0.55 * 2) / 2.2
    rows = [("nums.sort()", "same list, ordered", "returns " + RUN[key][4]), ("sorted(nums)", "a new ordered list", "nums unchanged")]
    for r, (a, b, c) in enumerate(rows):
        yy = y + 0.1 + r * 0.7
        node(sl, x, yy, 1.15, 0.4, a, fill=ORANGE, color=WHITE, bold=True, size=10, font=MONO)
        arrow(sl, x + 1.15, yy + 0.2, x + 1.5, yy + 0.2, ORANGE)
        node(sl, x + 1.5, yy, w - 1.5, 0.4, b, fill=TEAL_L, line=TEAL, size=10.5)
        tb(sl, x + 1.5, yy + 0.4, w - 1.5, 0.24, [c], size=9.5, italic=True, color=MUTED, name="diagram caption", ins=(0.04, 0.0, 0.04, 0.0))


def d_trap(sl, x, y, w, h, key):
    ns_states = TRAP_STATES
    labels = ["start", "after pass 1", "after pass 2"]
    for r, st in enumerate(ns_states):
        yy = y + 0.04 + r * 0.5
        tb(sl, x, yy + 0.03, 1.05, 0.34, [labels[r]], size=10, color=MUTED, name="step label", ins=(0.02, 0.02, 0.02, 0.02))
        for c, it in enumerate(st):
            hot = it == "b" and r > 0
            node(sl, x + 1.1 + c * 0.55, yy, 0.5, 0.36, it, fill=ORANGE_L if hot else TEAL_L, line=ORANGE if hot else TEAL, size=11, bold=hot)
        if r < len(ns_states) - 1:
            arrow(sl, x + 0.55, yy + 0.38, x + 0.55, yy + 0.52, MUTED, 1.5)
    tb(sl, x, y + 1.5, w, 0.24, ["'b' is never visited: it is skipped and stays"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_unpack(sl, x, y, w, h, key):
    items = ["fat", "gray", "loud"]
    names = ["size", "color", "mood"]
    bw = (w - 0.25 * 2) / 3
    for i in range(3):
        bx = x + i * (bw + 0.25)
        node(sl, bx, y + 0.1, bw, 0.42, items[i], fill=TEAL_L, line=TEAL, size=11, bold=True)
        arrow(sl, bx + bw / 2, y + 0.52, bx + bw / 2, y + 0.92, ORANGE)
        node(sl, bx, y + 0.94, bw, 0.4, names[i], fill=ORANGE, color=WHITE, bold=True, size=11)
    tb(sl, x, y + 1.38, w, 0.24, ["each item gets the name in the same position"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_input(sl, x, y, w, h, key):
    line = "4 8 15 16 23 42"
    stages = [("text", "'%s'" % line), ("split()", "6 words"), ("int()", "6 numbers")]
    bw = (w - 0.45 * 2) / 3
    for i, (a, b) in enumerate(stages):
        bx = x + i * (bw + 0.45)
        node(sl, bx, y + 0.25, bw, 0.7, [[(a, {"bold": True, "size": 10.5})], [(b, {"size": 9, "font": MONO if i == 0 else BODY})]], fill=ORANGE_L if i == 0 else TEAL_L, line=ORANGE if i == 0 else TEAL)
        if i < 2:
            arrow(sl, bx + bw, y + 0.6, bx + bw + 0.45, y + 0.6, MUTED)
    tb(sl, x, y + 1.05, w, 0.3, ["input() gives the first box; the others are our work"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_tags(sl, x, y, w, h, key):
    for i, nm in enumerate(["spam", "eggs"]):
        node(sl, x, y + 0.25 + i * 0.6, 0.9, 0.38, nm, fill=ORANGE, color=WHITE, bold=True, size=11)
        arrow(sl, x + 0.9, y + 0.44 + i * 0.6, x + 1.45, y + 0.72, ORANGE)
    node(sl, x + 1.45, y + 0.42, w - 1.45, 0.62, [[("one list", {"bold": True, "size": 10})], [(RUN[key][0], {"size": 9.5, "font": MONO})]], fill=TEAL_L, line=TEAL)
    tb(sl, x, y + 1.35, w, 0.24, ["two tags, one list"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_args(sl, x, y, w, h, key):
    for i, nm in enumerate(["nums (caller)", "items (function)"]):
        node(sl, x, y + 0.2 + i * 0.6, 1.35, 0.38, nm, fill=ORANGE, color=WHITE, bold=True, size=10)
        arrow(sl, x + 1.35, y + 0.39 + i * 0.6, x + 1.7, y + 0.7, ORANGE)
    node(sl, x + 1.7, y + 0.4, w - 1.7, 0.62, [[("one list", {"bold": True, "size": 10})], [("[1, 2, 3, 'Hello']", {"size": 9.5, "font": MONO})]], fill=TEAL_L, line=TEAL)
    tb(sl, x, y + 1.35, w, 0.24, ["the function works on the caller's list"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_copies(sl, x, y, w, h, key):
    rows = [("grid", "shared inner lists"), ("shallow", "shared inner lists"), ("deep", "its own inner lists")]
    node(sl, x + 1.1, y + 0.05, w - 1.1, 0.5, [[("inner lists of grid", {"bold": True, "size": 9.5})], [(COPY_SHARED, {"size": 9, "font": MONO})]], fill=TEAL_L, line=TEAL)
    node(sl, x + 1.1, y + 0.95, w - 1.1, 0.5, [[("inner lists of deep", {"bold": True, "size": 9.5})], [(COPY_OWN, {"size": 9, "font": MONO})]], fill=ORANGE_L, line=ORANGE)
    node(sl, x, y + 0.05, 0.85, 0.28, "grid", fill=ORANGE, color=WHITE, bold=True, size=10)
    node(sl, x, y + 0.42, 0.85, 0.28, "shallow", fill=ORANGE, color=WHITE, bold=True, size=10)
    node(sl, x, y + 1.05, 0.85, 0.28, "deep", fill=ORANGE, color=WHITE, bold=True, size=10)
    arrow(sl, x + 0.85, y + 0.19, x + 1.1, y + 0.25, ORANGE)
    arrow(sl, x + 0.85, y + 0.56, x + 1.1, y + 0.4, ORANGE)
    arrow(sl, x + 0.85, y + 1.19, x + 1.1, y + 1.19, ORANGE)


def d_hat(sl, x, y, w, h, key):
    rows = [("random.choice(pets)", "one item; the list is unchanged"), ("random.shuffle(pets)", "the same list, new order; returns None")]
    for r, (a, b) in enumerate(rows):
        yy = y + 0.1 + r * 0.7
        node(sl, x, yy, 1.85, 0.42, a, fill=ORANGE, color=WHITE, bold=True, size=9, font=MONO)
        arrow(sl, x + 1.85, yy + 0.21, x + 2.1, yy + 0.21, ORANGE)
        node(sl, x + 2.1, yy, w - 2.1, 0.42, b, fill=TEAL_L, line=TEAL, size=9.5)


def d_pick(sl, x, y, w, h, key):
    stages = [("messages", "a list of 4 answers"), ("randint(0, 3)", "a random index"), ("messages[pick]", "answer: " + RUN[key][2])]
    bw = (w - 0.4 * 2) / 3
    for i, (a, b) in enumerate(stages):
        bx = x + i * (bw + 0.4)
        node(sl, bx, y + 0.2, bw, 0.75, [[(a, {"bold": True, "size": 10, "font": MONO})], [(b, {"size": 9.5})]], fill=ORANGE_L if i == 2 else TEAL_L, line=ORANGE if i == 2 else TEAL)
        if i < 2:
            arrow(sl, bx + bw, y + 0.58, bx + bw + 0.4, y + 0.58, MUTED)
    tb(sl, x, y + 1.0, w, 0.26, ["list, index, answer"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_counters(sl, x, y, w, h, key):
    cs = RUN_EXTRA["matrix"]
    n = len(cs)
    bw = min(0.34, (w - 0.03 * (n - 1)) / n)
    tot = n * bw + 0.03 * (n - 1)
    x0 = x + (w - tot) / 2
    arrow(sl, x0 + tot / 2, y + 0.32, x0 + tot / 2, y + 0.5, MUTED, 1.5)
    node(sl, x0 + tot / 2 - 1.2, y + 0.02, 2.4, 0.3, "ctr after the last row", fill=ORANGE, color=WHITE, bold=True, size=10)
    for i, c in enumerate(cs):
        node(sl, x0 + i * (bw + 0.03), y + 0.52, bw, 0.38, str(c), fill=ORANGE_L if c else TEAL_L, line=ORANGE if c else TEAL, size=11, bold=bool(c))
    tb(sl, x, y + 0.95, w, 0.26, ["a counter above zero means a digit is falling there"], size=9.5, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_slice(sl, x, y, w, h, key):
    items = ["a", "b", "c"]
    bw = 0.7
    x0 = x + (w - 3.2) / 2
    node(sl, x0, y + 0.02, 2 * bw + 0.05, 0.3, "items[:-1]", fill=TEAL, color=WHITE, bold=True, size=10, font=MONO)
    node(sl, x0 + 2 * bw + 0.15, y + 0.02, 1.05, 0.3, "items[-1]", fill=ORANGE, color=WHITE, bold=True, size=10, font=MONO)
    for i, it in enumerate(items):
        hot = i == 2
        bx = x0 + i * (bw + 0.05) + (0.2 if hot else 0)
        arrow(sl, bx + bw / 2 if not hot else x0 + 2 * bw + 0.15 + 0.52, y + 0.34, bx + bw / 2, y + 0.5, ORANGE if hot else TEAL, 1.5)
        node(sl, bx, y + 0.52, bw, 0.4, it, fill=ORANGE_L if hot else TEAL_L, line=ORANGE if hot else TEAL, size=12, bold=True)
    tb(sl, x, y + 1.0, w, 0.26, ["result: " + RUN[key][0]], size=10, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="diagram caption")


def d_coin(sl, x, y, w, h, key):
    pct = float(re.search(r"([\d.]+) %", RUN[key][0]).group(1))
    n = round(pct * 100)
    chart(sl, x, y, w, h, "10,000 experiments", ["with a streak of 6", "without"], [n, 10000 - n], "bar")


DIAG = {"lockers": d_lockers, "grid": d_grid, "ruler": d_ruler, "family": d_family, "pets": d_pets, "flow": d_flow, "sorting": d_sorting, "trap": d_trap,
        "unpack": d_unpack, "pick": d_pick, "counters": d_counters, "slice": d_slice, "coin": d_coin, "input": d_input, "tags": d_tags, "args": d_args, "copies": d_copies, "hat": d_hat}

# facts read from real execution for diagrams and charts
_ns = exec_ns("items = ['a', 'b', 'c', 'd']\nstates = [list(items)]\nfor x in items:\n    items.remove(x)\n    states.append(list(items))")
TRAP_STATES = _ns["states"]
_ns = exec_ns("import copy\ngrid = [[1, 2], [3, 4]]\nshallow = copy.copy(grid)\ndeep = copy.deepcopy(grid)\ngrid[0][0] = 99")
COPY_SHARED, COPY_OWN = str(_ns["grid"]), str(_ns["deep"])


def lens_after(key, record):
    flat = [l for box in C.EX[key]["boxes"] for l in box]
    ns, out = {}, []
    for i, l in enumerate(flat):
        with contextlib.redirect_stdout(io.StringIO()):
            exec(l, ns)
        if i in record:
            out.append(len(ns["spam"]))
    return out


def chart_for(key):
    r = RUN[key]
    spec = C.EX[key]["vis"].split("chart:")[1].split("|")
    title, cats = spec[0], spec[1].split(",") if spec[1] else None
    if key == "dijkstra":
        return title, cats, lit(r[2]), "bar"
    if key == "change":
        return title, cats, lens_after("change", [0, 1, 2, 3, 5, 6, 7]), "line"
    if key == "augmented":
        return title, cats, lens_after("augmented", [0, 3, 4, 6]), "line"
    if key == "loops":
        return title, cats, [int(l.split()[2]) for l in r[4:8]], "bar"
    if key == "comprehension":
        return title, cats, lit(r[0]), "bar"
    if key == "fairshuffle":
        return title, lit(r[0]), lit(r[1]), "bar"
    raise KeyError(key)


# ------------------------------------------------------------------------------------------------ slide builders
def b_code(prs, key):
    ex = C.EX[key]
    sl = new_slide(prs, ex["title"])
    lede(sl, ex["lede"])
    vis = ex["vis"]
    ytop = 1.05
    boxes, say = ex["boxes"], ex["say"]
    cw, ex_x, ex_w = 5.4, 5.78, 3.87
    y = ytop
    for b, sy in zip(boxes, say):
        words = sum(len(("%s %s" % (">>>", l)).split()) for l in b)
        assert words <= 30, (key, words, b)
        eh = est_h([sy], ex_w - 0.2, 11.5) + 0.05
        sz = code_size(b, cw, 11.0)
        ch = len(b) * sz * 1.2 / 72.0 + 0.16
        hh = max(ch, eh)
        s, h, size = code_box(sl, 0.4, y, cw, b, target=11.0, minh=hh)
        bar(sl, ex_x + 0.04, y, 0.05, hh, ORANGE)
        tb(sl, ex_x, y, ex_w + 0.0, hh, [sy], size=11.5, anchor=MSO_ANCHOR.MIDDLE, name="explanation", ins=(0.2, 0.04, 0.08, 0.04))
        y += hh + 0.08
    yend = y - 0.08
    vy = yend + 0.12
    vh = 4.92 - vy
    r = RUN[key]
    kind = vis.split("+")[0]
    if vis.startswith("chart:"):
        t, cats, vals, ck = chart_for(key)
        chart(sl, 0.4, vy, 9.25, vh, t, cats, vals, ck)
    elif kind == "loops-table":
        rows = [(r[i].split()[0], r[i], r[4 + i]) for i in range(4)]
        rowh = min(0.25, vh / 5)
        gf, tw, th = table(sl, 0.4, vy, 5.4, ["i", "range(len(supplies))", "enumerate(supplies, 1)"], rows, size=10, mono_cols=(0, 1, 2), maxw=5.5, rowh=rowh)
        t, cats, vals, ck = chart_for(key)
        chart(sl, 0.4 + tw + 0.2, vy - 0.02, 9.65 - (0.4 + tw + 0.2), vh + 0.02, t, cats, vals, ck)
    else:
        labels = ex["labels"]
        assert len(labels) == len(r), (key, len(labels), len(r), r)
        rows = [(labels[i], cut(r[i], 60)) for i in range(len(r))]
        rowh = min(0.25, vh / (len(rows) + 1))
        if rowh < 0.205:
            WARN.append("table rows too tight slide %s (%.2f)" % (SLIDE_NO[0], rowh))
        gf, tw, th = table(sl, 0.4, vy, 5.6, ["printed", "result"], rows, size=10 if rowh >= 0.24 else 9.5, mono_cols=(1,), maxw=6.3, rowh=rowh)
        kinds = vis.split("+")[1]
        rx = 0.4 + tw + 0.2
        rw = 9.65 - rx
        if kinds.startswith("chart"):
            t, cats, vals, ck = chart_for(key)
            chart(sl, rx, vy - 0.02, rw, vh + 0.02, t, cats, vals, ck)
        elif rw < 2.5:
            WARN.append("diagram region too narrow (%.2f) slide %s" % (rw, SLIDE_NO[0]))
        else:
            DIAG[kinds](sl, rx, vy - 0.02, rw, vh, key)
    takeaway(sl, ex["take"])
    number(sl)
    notes(sl, ex["note"])
    return sl


def b_title(prs):
    sl = new_slide(prs, "Chapter 6: Lists", chip=False, title_size=36)
    t = sl.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.5), Inches(1.7), Inches(5.1), Inches(0.8)
    bar(sl, 0.5, 2.62, 1.2, 0.06, ORANGE)
    tb(sl, 0.5, 2.78, 5.1, 0.45, ["One ordered, changeable row of values"], size=16, italic=True, color=TEAL, name="subtitle")
    tb(sl, 0.5, 4.3, 5.1, 0.62, ["SEN0414 Advanced Programming - Fall 2026", "Yusuf Altunel, PhD - Istanbul Kultur University"], size=11, color=MUTED, name="course line")
    p = sl.shapes.add_picture(os.path.join(ASSETS, "book_fig_000100.jpg"), Inches(5.8), Inches(1.35), Inches(3.85), Inches(3.85 / 1.654))
    p.name = "picture: lists hold references"
    alt(p, "Figure 6-4 of the textbook: a list holds items, each reached by its number")
    tb(sl, 5.8, 3.75, 3.85, 0.4, ["Figure 6-4 - Sweigart, ATBS 3e, CC BY-NC-SA"], size=9, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="credit")
    number(sl)
    notes(sl, "Chapter 6 is about lists: one ordered, changeable row of values. The deck has five parts and ends with short programs. Every code box on these slides is also in the chapter-code tab of the course page, in the same order, and runs there.")
    return sl


def b_route(prs, rows):
    sl = new_slide(prs, "Today's route")
    lede(sl, "Five parts and a wrap-up; every number is a slide, every result a table, chart or drawing from the run.")
    table(sl, 0.4, 1.3, 9.25, ["Part", "What you learn", "Slides"], rows, size=12, rowh=0.4)
    takeaway(sl, "Five parts, then programs you can read line by line")
    number(sl)
    notes(sl, "The route has five parts and a wrap-up. The slide ranges are in the table, so you can jump. Each code slide shows its result as a table, chart or drawing. The hardest part is names and copies; mark it now and check it again at the summary.")
    return sl


def b_questions(prs):
    sl = new_slide(prs, "The questions this chapter answers")
    lede(sl, "Three competency questions frame the chapter; we come back to each one in the summary.")
    for i, q in enumerate(C.QUESTIONS):
        y = 1.3 + i * 1.12
        card(sl, 0.45, y + 0.12, 0.6, 0.6, [str(i + 1)], fill=ORANGE, color=WHITE, bold=True, size=22, font=HEAD, shape=MSO_SHAPE.OVAL, ins=(0, 0, 0, 0))
        card(sl, 1.25, y, 8.4, 0.88, [q], fill=CARD, line=TEAL_L, size=14, align=PP_ALIGN.LEFT, ins=(0.18, 0.06, 0.12, 0.06))
    takeaway(sl, "If you can answer these three, chapter 6 is yours")
    number(sl)
    notes(sl, "Three questions frame the chapter. They are printed here so you can return to them at the end. Which of the three could you already answer from what you know about variables and strings?")
    return sl


def b_map(prs, ranges):
    sl = new_slide(prs, "One chapter, six branches")
    lede(sl, "The map the whole chapter hangs on; the numbers under each branch are its slides.")
    node(sl, 3.9, 2.55, 2.2, 0.75, "a list", fill=ORANGE, color=WHITE, bold=True, size=18, font=HEAD)
    pos = [(0.45, 1.4), (0.45, 2.6), (0.45, 3.8), (6.95, 1.4), (6.95, 2.6), (6.95, 3.8)]
    for (px, py), name, rg in zip(pos, C.BRANCHES, ranges):
        left = px < 4
        if left:
            arrow(sl, 3.9, 2.92, px + 2.7, py + 0.35, TEAL, 1.5)
        else:
            arrow(sl, 6.1, 2.92, px, py + 0.35, TEAL, 1.5)
        node(sl, px, py, 2.7, 0.7, [[(name, {"bold": True, "size": 13})], [(rg, {"size": 10.5, "color": MUTED})]], fill=CARD, line=TEAL, size=13)
    takeaway(sl, "Six branches: every slide today lives on this map")
    number(sl)
    notes(sl, "A list is one idea with six branches. Each box names a branch and the slides that teach it. The fifth branch, random choices, and the sixth, short programs, are where lists meet chance and real code. The branches are the same as the five parts, with the last part split in two.")
    return sl


def b_divider(prs, key):
    d = C.DIVIDERS[key]
    sl = new_slide(prs, d["title"], chip=False, title_size=30)
    t = sl.shapes.title
    t.top, t.height = Inches(0.45), Inches(0.7)
    bar(sl, 0.5, 0.0, 9.0, 0.09, ORANGE)
    tb(sl, 0.5, 1.15, 9.0, 0.4, [d["sub"]], size=15, italic=True, color=TEAL, name="subtitle")
    n = len(d["items"])
    y0 = 1.85
    step = 0.78
    for i, (pill, mean) in enumerate(d["items"]):
        yy = y0 + i * step
        card(sl, 0.5, yy, 2.55, 0.5, [pill], fill=TEAL, color=WHITE, bold=True, size=13, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5, name="concept")
        tb(sl, 3.2, yy + 0.02, 3.4, 0.5, [mean], size=12.5, anchor=MSO_ANCHOR.MIDDLE, name="meaning")
    # picture and its caption (the caption follows the picture in the shape order)
    pic = os.path.join(ASSETS, d["pic"])
    from PIL import Image
    iw, ih = Image.open(pic).size
    pw = 2.9
    ph = pw * ih / iw
    px, py = 6.75, 2.0
    p = sl.shapes.add_picture(pic, Inches(px), Inches(py), Inches(pw), Inches(ph))
    p.name = "picture: %s" % d["cap"]
    alt(p, "Textbook figure for the part: " + d["title"])
    tb(sl, px, py + ph + 0.05, pw, 0.4, [d["cap"]], size=9, italic=True, color=MUTED, align=PP_ALIGN.CENTER, name="credit")
    number(sl)
    notes(sl, d["note"])
    return sl


def b_analogy(prs, key):
    cards = C.ANALOGIES[key]
    sl = new_slide(prs, C.ANALOGY_TITLES[key])
    lede(sl, "Each concept next to something from daily life; keep the picture, and the code will make sense.")
    n = len(cards)
    cols = 2 if n >= 4 else 1
    cw = 4.5 if cols == 2 else 9.25
    rows = (n + cols - 1) // cols
    ch = 0.98 if rows <= 2 else 0.98
    gap = 0.12
    if n == 5:
        ch = 0.98
    if cols == 1:
        ch = 1.0
    for i, (concept, text) in enumerate(cards):
        r, c = divmod(i, cols)
        x = 0.4 + c * (cw + 0.25)
        y = 1.3 + r * (ch + gap)
        if n == 5 and i == 4:
            x, cw_i = 0.4 + 0.0, 9.25
        else:
            cw_i = cw
        card(sl, x, y, cw_i, ch, [[("ANALOGY  ", {"bold": True, "color": ORANGE, "size": 10.5}), (concept, {"bold": True, "size": 12.5, "color": TEAL})], [(text, {"size": 12})]],
             fill=CARD, line=TEAL_L, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, ins=(0.15, 0.05, 0.12, 0.05), name="analogy", space_after=2)
    takeaway(sl, C.ANALOGY_TAKE[key])
    number(sl)
    notes(sl, C.ANALOGY_NOTES[key])
    return sl


def b_story(prs, key):
    s = C.STORIES[key]
    sl = new_slide(prs, s["title"])
    lede(sl, s["lede"], h=0.3)
    px, py = 0.4, 1.12
    p = sl.shapes.add_picture(os.path.join(ASSETS, s["pic"]), Inches(px), Inches(py), Inches(s["pw"]), Inches(s["ph"]))
    p.name = "picture: " + s["title"]
    alt(p, "Picture for the story: " + s["credit"])
    tb(sl, px, py + s["ph"] + 0.04, s["pw"], 0.42, [s["credit"]], size=9, italic=True, color=MUTED, name="credit")
    gx = px + s["pw"] + 0.25
    gw = 9.65 - gx
    cw = (gw - 0.12) / 2
    labs = ["WHO", "WHAT", "WHEN", "WHERE", "WHY", "HOW"]
    for i, lab in enumerate(labs):
        r, c = divmod(i, 2)
        x = gx + c * (cw + 0.12)
        y = 1.12 + r * 1.0
        txt = s[lab.lower()]
        assert len((lab + " " + txt).split()) <= 30
        card(sl, x, y, cw, 0.93, [[(lab + "  ", {"bold": True, "color": ORANGE, "size": 11}), (txt, {"size": 10.5})]], fill=CARD, line=TEAL_L,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE, ins=(0.1, 0.04, 0.08, 0.04), name="story " + lab.lower(), radius=0.08)
    card(sl, 0.4, 4.3, 9.25, 0.5, [[("READ  ", {"bold": True, "color": ORANGE, "size": 11}), (s["linktext"], {"size": 11.5, "link": s["link"]})]], fill=TEAL_L,
         align=PP_ALIGN.LEFT, ins=(0.15, 0.04, 0.1, 0.04), name="story read", radius=0.2)
    takeaway(sl, "A true story, with its picture and its source")
    number(sl)
    notes(sl, s["note"])
    return sl


def b_summary(prs):
    sl = new_slide(prs, "Summary: who changes, who copies, who shares")
    lede(sl, "Ask of every operation: does it change the list, return a new list, or share one?")
    table(sl, 0.4, 1.3, 9.25, ["Operation", "What happens to the list", "What you get back"], C.SUMMARY_ROWS, size=12, mono_cols=(0,), rowh=0.36)
    takeaway(sl, "Changes, copies or shares: ask it of every operation")
    number(sl)
    notes(sl, "Read the table as a decision guide. For every list operation ask three things: does it change the list, return a new list, or share one? Most list bugs come from mixing these up.")
    return sl


def b_practice(prs):
    sl = new_slide(prs, "Practice Questions and Practice Programs")
    lede(sl, "Try them before the next class; the course page has a question bank and the runnable code.")
    tb(sl, 0.4, 1.25, 4.5, 0.3, ["Practice Questions"], size=14, bold=True, color=TEAL, font=HEAD, name="heading")
    for i, q in enumerate(C.PRACTICE_Q):
        card(sl, 0.4, 1.6 + i * 1.05, 4.5, 0.95, [q], fill=CARD, line=TEAL_L, size=12, align=PP_ALIGN.LEFT, ins=(0.12, 0.05, 0.1, 0.05))
    tb(sl, 5.15, 1.25, 4.5, 0.3, ["Practice Programs"], size=14, bold=True, color=TEAL, font=HEAD, name="heading")
    for i, q in enumerate(C.PRACTICE_P):
        card(sl, 5.15, 1.6 + i * 1.05, 4.5, 0.95, [q], fill=ORANGE_L, line=ORANGE, size=12, align=PP_ALIGN.LEFT, ins=(0.12, 0.05, 0.1, 0.05))
    takeaway(sl, "Check yourself: three questions and two programs")
    number(sl)
    notes(sl, "Five tasks. The three questions check understanding of indexes, loops and references. The two programs check that you can combine slices, loops and random. Both programs appeared on earlier slides; try them blind first.")
    return sl


def b_resources(prs):
    sl = new_slide(prs, "Resources: where to go from here")
    lede(sl, "Free to read and to watch; every link below is live.")
    y = 1.2
    cols = [0.4, 5.1]
    ci = 0
    yy = [y, y]
    groups = C.RESOURCES
    order = [0, 1, 0, 1]
    for gi, (head, rows) in enumerate(groups):
        c = order[gi]
        x = cols[c]
        tb(sl, x, yy[c], 4.5, 0.28, [head], size=12, bold=True, color=ORANGE, name="heading", ins=(0.04, 0.02, 0.04, 0.02))
        yy[c] += 0.3
        for label, url in rows:
            card(sl, x, yy[c], 4.5, 0.34, [[(label, {"size": 11, "link": url})]], fill=CARD, line=TEAL_L, align=PP_ALIGN.LEFT, ins=(0.1, 0.02, 0.08, 0.02), radius=0.2, name="link")
            yy[c] += 0.38
        yy[c] += 0.08
    takeaway(sl, "Draw your lists in Python Tutor and watch the names")
    number(sl)
    notes(sl, "Everything here is free. Paste the aliasing example of this deck into Python Tutor and watch two name tags arrive on one list. Then read the official sorting HOWTO for the key argument.")
    return sl


def b_closing(prs):
    sl = new_slide(prs, "What you should now be able to say")
    lede(sl, "Four claims, each one proven by code that ran on a slide of this deck.")
    for i, t in enumerate(C.CLOSING):
        card(sl, 0.4, 1.35 + i * 0.8, 9.25, 0.65, [[("%d  " % (i + 1), {"bold": True, "color": ORANGE, "size": 16}), (t, {"size": 15})]], fill=CARD, line=TEAL_L,
             align=PP_ALIGN.LEFT, ins=(0.2, 0.05, 0.1, 0.05))
    takeaway(sl, "Four claims; the code on the slides is the proof")
    number(sl)
    notes(sl, "Four claims, each carried by code that ran on a slide. The course page carries the same code in its chapter-code tab, the stories with their sources and the question bank. Use the four claims as a self-test.")
    return sl


# ------------------------------------------------------------------------------------------------ the plan
PLAN = (["title", "route", "questions", "map", "div:A", "code:indexes", "code:nested", "story:dijkstra", "code:slices", "code:dijkstra", "code:sequences", "an:an1",
         "div:B", "code:change", "code:augmented", "code:searching", "code:shortcircuit", "code:sort", "an:an2", "an:an3", "story:magic8", "code:magic8", "an:an4",
         "div:C", "code:loops", "code:removal", "code:unpack", "code:comprehension", "code:input", "an:an5",
         "div:D", "code:alias", "code:argument", "code:copies", "an:an7",
         "div:E", "code:random", "story:fisher", "code:fairshuffle", "an:an6", "story:rain", "code:matrix", "code:commacode", "code:coinstreaks",
         "an:an8", "summary", "practice", "resources", "closing"])


def main():
    N = len(PLAN)
    TOTAL[0] = N
    pos = {p: i + 1 for i, p in enumerate(PLAN)}
    rg = lambda a, b: "slides %d-%d" % (pos[a], pos[b])
    route = [("Questions", "The questions and the map of the chapter", rg("route", "map")),
             ("1  The list as a value", "Indexes, slices, other sequences", rg("div:A", "an:an1")),
             ("2  Changing, combining, searching", "Methods, in-place change, sort, short-circuit", rg("div:B", "an:an4")),
             ("3  Loops and unpacking", "range, enumerate, the removal trap, unpacking", rg("div:C", "an:an5")),
             ("4  Names and copies", "References, aliasing, shallow and deep copies", rg("div:D", "an:an7")),
             ("5  Random choices and programs", "choice, shuffle, four short programs", rg("div:E", "an:an8")),
             ("Wrap-up", "Summary, practice, resources", rg("summary", "closing"))]
    ranges = [rg("div:A", "an:an1"), rg("div:B", "an:an4"), rg("div:C", "an:an5"), rg("div:D", "an:an7"), rg("div:E", "an:an6"), rg("story:rain", "code:coinstreaks")]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(9144000), Emu(5143500)
    manifest_ex = []
    for i, item in enumerate(PLAN, 1):
        SLIDE_NO[0] = i
        kind, _, key = item.partition(":")
        if kind == "title":
            b_title(prs)
        elif kind == "route":
            b_route(prs, route)
        elif kind == "questions":
            b_questions(prs)
        elif kind == "map":
            b_map(prs, ranges)
        elif kind == "div":
            b_divider(prs, key)
        elif kind == "code":
            b_code(prs, key)
            manifest_ex.append((i, key))
        elif kind == "story":
            b_story(prs, key)
        elif kind == "an":
            b_analogy(prs, key)
        elif kind == "summary":
            b_summary(prs)
        elif kind == "practice":
            b_practice(prs)
        elif kind == "resources":
            b_resources(prs)
        elif kind == "closing":
            b_closing(prs)
    prs.core_properties.title = "SEN0414 Chapter 6 - Lists"
    prs.core_properties.author = "Yusuf Altunel"
    prs.core_properties.subject = "SEN0414 Advanced Programming, chapter 6, deck v3.0.0"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    prs.save(OUT)
    # manifest
    exs = []
    for n, (slide_no, key) in enumerate(manifest_ex, 1):
        e = C.EX[key]
        exs.append({"order": n, "id": key, "name": e["name"], "slide": slide_no, "concepts": e["concepts"], "code": code_of(key), "expected": "\n".join(RUN[key]) + "\n"})
    ver = subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.split()[-1]
    man = {"chapter": 6, "version": "1.0.0", "kind": "chapter-code manifest", "deck": "03-materials/ch06/" + os.path.basename(OUT),
           "about": "The code examples of the chapter 6 deck, in the order of the code slides (order = slide order). The code of an example is the lines of the slide's code boxes, "
                    "boxes in order, each line with its four-character listing prompt removed. The page's chapter-code tab lists the examples by NAME in this order and runs "
                    "each one with the standard library only; the expected result is what the run printed.",
           "executed_with": {"python": ver, "library": "standard library only (random, copy, collections)"},
           "library": {"file": None, "page_requirements": ["random (seeded Mersenne Twister)", "copy", "collections.Counter"]},
           "prelude": "", "examples": exs}
    os.makedirs(os.path.dirname(MAN), exist_ok=True)
    json.dump(man, open(MAN, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    open(MAN, "a").write("\n")
    print("deck %s | %d slides | %d code examples | manifest %s" % (os.path.relpath(OUT, REPO), N, len(exs), os.path.relpath(MAN, REPO)))
    for w in WARN:
        print("WARN", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
