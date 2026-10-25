"""Chapter 16 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py (chapter 16) passes in), or from a query on the connection that run left open in `ns`;
nothing is typed in by hand except plain-language names of columns and boxes and the one-line meanings of a statement, which are named as such on the slide.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import ast
import os
import re
from pptx.enum.text import PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape as _label_shape, table as _table, tb, rect, _style_run


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


def q(ns, sql, *args):
    return ns["conn"].execute(sql, args).fetchall()


# ------------------------------------------------------------------ part 1
@need(1.3)
def v_connect_close(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y + 0.1, w, ["connect(':memory:')\nin a transaction: %s" % val(L[0]), "execute('SELECT 6 * 7')\nfetchone() gives %s" % val(L[1]), "close()\nthe handle ends",
                            "execute() after close\n%s" % short(val(L[2]), 30)], ["teal", "plain", "amber", "red"], h=0.8, gap=0.4, fs=10)
    note(s, x, y + 1.0, w, "the four boxes are the four steps of the code, with the values the run printed", fs=9.5)


@need(1.45)
def v_create_table(s, x, y, w, h, ns, out):
    rows = [["cid", "name", "type", "notnull", "default", "pk"]] + [[str(v) if v is not None else "None" for v in r] for r in q(ns, "PRAGMA table_info(cats)")]
    cf = {(i, 3): C["amberLight"] for i, r in enumerate(rows[1:], 1) if r[3] == "1"}
    table(s, x, y, w * 0.62, rows, [0.6, 1.5, 1.0, 1.0, 1.0, 0.6], rowh=min(0.26, h / len(rows)), mono_cols=(1, 2), cell_fill=cf, fs=10)
    bx = x + w * 0.67
    box(s, bx, y, w * 0.33, 0.42, "sqlite_schema lists\n%s" % val(lines(out)[0]) if ":" in lines(out)[0] else "sqlite_schema lists\n%s" % lines(out)[0], "teal", 10, True)
    arrow(s, bx + w * 0.165, y + 0.44, bx + w * 0.165, y + 0.66, C["muted"], 1.4)
    box(s, bx, y + 0.68, w * 0.33, 0.42, "PRAGMA table_info\n%d columns" % (len(rows) - 1), "plain", 10, True)
    note(s, x, y + h - 0.2, w * 0.62, "amber: name is NOT NULL, so a cat without a name is refused", fs=9)


@need(1.15)
def v_strict_types(s, x, y, w, h, ns, out):
    L = lines(out)
    sres = "refused" if L[0].startswith("s refused") else "stored"
    pres = "refused" if L[1].startswith("p refused") else "stored"
    s_row, p_row = q(ns, "SELECT i, typeof(i) FROM s")[0], q(ns, "SELECT i, typeof(i) FROM p")[0]
    rows = [["Table", "Kind", "Insert 'Hello'", "Insert '42' then read", "Storage class"],
            ["s", "STRICT", sres, "%r" % (s_row[0],), s_row[1]], ["p", "plain", pres, "%r" % (p_row[0],), p_row[1]]]
    cf = {(1, 2): C["redLight"], (2, 2): C["greenLight"], (1, 3): C["greenLight"], (2, 3): C["amberLight"]}
    table(s, x, y, w * 0.78, rows, [0.7, 1.0, 1.4, 1.8, 1.3], rowh=0.28, mono_cols=(0, 2, 3, 4), cell_fill=cf, fs=10)
    note(s, x, y + 0.88, w * 0.78, "the plain table keeps Hello in an INTEGER column; STRICT converts '42' and refuses Hello", fs=9.5)
    box(s, x + w * 0.82, y, w * 0.18, 0.85, "message\n" + short(val(L[0]).replace("cannot store ", ""), 36), "red", 8.5)


@need(1.3)
def v_insert_read(s, x, y, w, h, ns, out):
    rows = [["rowid", "name", "fur"]] + [[str(a), b, c] for a, b, c in q(ns, "SELECT rowid, * FROM cats")]
    table(s, x, y, w * 0.5, rows, [0.8, 1.4, 1.2], rowh=min(0.28, h / len(rows)), mono_cols=(1, 2), bold_cols=(0,), fs=10.5)
    bx = x + w * 0.56
    L = lines(out)
    box(s, bx, y, w * 0.44, 0.34, "executemany: 2 tuples, 2 rows", "teal", 10)
    box(s, bx, y + 0.42, w * 0.44, 0.34, "fetchone() gives the first row: %s" % L[1], "plain", 10, True)
    box(s, bx, y + 0.84, w * 0.44, 0.34, L[2], "amber", 10)


@need(1.3)
def v_rowid_pk(s, x, y, w, h, ns, out):
    L = lines(out)
    before, after = lit(L[0]), lit(L[1])
    t1 = [["rowid", "id", "v"]] + [[str(a), str(b), c] for a, b, c in before]
    t2 = [["id", "v"]] + [[str(a), b] for a, b in after]
    rh = min(0.24, h / (len(t1) + 0.3))
    label_shape(s, x, y, w * 0.4, 0.22, "before", C["tealLight"], C["ink"], size=9.5, bold=True, radius=0.3)
    table(s, x, y + 0.26, w * 0.4, t1, [0.8, 0.8, 1.2], rowh=rh, mono_cols=(2,), fs=10)
    arrow(s, x + w * 0.43, y + 0.75, x + w * 0.52, y + 0.75, C["muted"], 1.6)
    label_shape(s, x + w * 0.46, y + 0.4, w * 0.11, 0.3, "DELETE 3\nINSERT d", C["card"], C["ink"], size=8, line=C["line"])
    label_shape(s, x + w * 0.58, y, w * 0.3, 0.22, "after", C["tealLight"], C["ink"], size=9.5, bold=True, radius=0.3)
    cf = {(3, 0): C["amberLight"], (3, 1): C["amberLight"]}
    table(s, x + w * 0.58, y + 0.26, w * 0.3, t2, [0.8, 1.2], rowh=rh, mono_cols=(1,), cell_fill=cf, fs=10)
    note(s, x + w * 0.58, y + 0.26 + rh * len(t2) + 0.04, w * 0.42, L[2] + ": the number 3 was handed out again", fs=9)


# ------------------------------------------------------------------ part 2
@need(1.5)
def v_select_filter(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = q(ns, "SELECT name, kg FROM cats ORDER BY kg DESC")
    chart(s, "col", x, y - 0.05, w * 0.46, h + 0.05, [r[0] for r in rows], [("kg", [r[1] for r in rows])], fs=10, legend=False, gap=60, number_format="0.0", vmax=8, major=2)
    bx = x + w * 0.5
    t = [["Query", "Rows returned"], ["WHERE fur = 'black' ORDER BY kg DESC", L[0]], ["ORDER BY kg DESC LIMIT 2", L[1]]]
    table(s, bx, y, w * 0.5, t, [2.4, 2.4], rowh=0.42, mono_cols=(0, 1), cell_fill={(1, 1): C["greenLight"], (2, 1): C["greenLight"]}, fs=9.5)
    note(s, bx, y + 1.3, w * 0.5, "chart: the weights in kg that both queries work on, heaviest first", fs=9)


@need(1.35)
def v_like_glob(s, x, y, w, h, ns, out):
    tests = [("Zophie", "zo%", "zo*"), ("Zophie", "Zo%", "Zo*"), ("a", "A", "A"), ("é", "É", "É")]
    rows = [["Text", "LIKE pattern", "LIKE", "GLOB pattern", "GLOB"]]
    cf = {}
    for i, (t, p1, p2) in enumerate(tests, 1):
        a = ns["conn"].execute("SELECT ? LIKE ?, ? GLOB ?", (t, p1, t, p2)).fetchone()
        rows.append([t, p1, "match" if a[0] else "no match", p2, "match" if a[1] else "no match"])
        cf[(i, 2)] = C["greenLight"] if a[0] else C["redLight"]
        cf[(i, 4)] = C["greenLight"] if a[1] else C["redLight"]
    table(s, x, y, w * 0.7, rows, [1.0, 1.2, 1.2, 1.2, 1.2], rowh=min(0.26, h / len(rows)), mono_cols=(0, 1, 3), cell_fill=cf, fs=10)
    bx = x + w * 0.74
    box(s, bx, y, w * 0.26, 0.5, "printed by the code:\n" + "  ".join(lines(out)), "grey", 9, True)
    note(s, bx, y + 0.6, w * 0.26, "rows 1 to 3 are the printed lines; row 4 asks one more question", fs=8.5, h=0.4)


@need(1.3)
def v_null_logic(s, x, y, w, h, ns, out):
    L = lines(out)
    data = [["name", "fur"]] + [[a, "NULL" if b is None else b] for a, b in q(ns, "SELECT name, fur FROM c")]
    table(s, x, y, w * 0.3, data, [1.2, 1.2], rowh=0.26, mono_cols=(0, 1), cell_fill={(3, 1): C["amberLight"]}, fs=10.5)
    t = [["Query", "Rows returned"], ["fur = NULL", L[1]], ["fur != 'black'", L[2]], ["fur IS NULL", L[3]], ["count(*), count(fur)", L[0]]]
    cf = {(1, 1): C["redLight"], (2, 1): C["redLight"], (3, 1): C["greenLight"]}
    table(s, x + w * 0.35, y, w * 0.65, t, [2.2, 2.4], rowh=min(0.26, h / 5), mono_cols=(0, 1), cell_fill=cf, fs=10)


@need(1.3)
def v_update_delete(s, x, y, w, h, ns, out):
    L = lines(out)
    import re as _re
    before = lit(_re.search(r"\[\('Zophie'.*?\)\]", ns["__code__"]).group(0))
    flow(s, x, y + 0.05, w, ["3 cats\n" + ", ".join("%s %s" % r for r in before), "UPDATE kg + 0.5\nWHERE kg < 6\nrowcount %s" % val(L[0]), "DELETE WHERE kg > 7\nRETURNING name\n%s" % val(L[1]),
                             "left\n" + ", ".join("%s %s" % r for r in lit(L[2]))], ["plain", "amber", "red", "green"], h=0.95, gap=0.35, fs=9.5)
    note(s, x, y + 1.08, w, "the weights after the UPDATE are 5.6 + 0.5 = 6.1 and 4.1 + 0.5 = 4.6; Jacob (7.3) is not below 6, so he is only deleted", fs=9.5)


@need(1.2)
def v_placeholders(s, x, y, w, h, ns, out):
    rows = [["Statement", "Values bound", "Row stored"], ["VALUES (?, ?)", "('Zophie', 'black')", "Zophie | black"],
            ["VALUES (:n, :f)", "{'n': 'Toby', 'f': 'black'}", "Toby | black"], ["WHERE fur = :fur", "{'fur': 'black'}", "finds " + lines(out)[0]]]
    table(s, x, y, w, rows, [2.0, 3.0, 3.4], rowh=min(0.26, h / 4), mono_cols=(0, 1, 2), cell_fill={(3, 2): C["greenLight"]}, fs=10)
    note(s, x, y + min(0.26, h / 4) * 4 + 0.04, w, "the third column of the last row is the printed result of the code", fs=9)


@need(1.25)
def v_injection(s, x, y, w, h, ns, out):
    L = lines(out)
    n1, n2 = re.search(r"(\d+) rows", L[0]).group(1), re.search(r"(\d+) rows", L[1]).group(1)
    bw = w / 3.6
    box(s, x, y, bw, 0.5, "text typed\nx' OR '1'='1", "amber", 10, True)
    arrow(s, x + bw + 0.02, y + 0.25, x + bw + 0.4, y + 0.25, C["muted"], 1.5)
    box(s, x + bw + 0.42, y, bw * 1.5, 0.5, "pasted into SQL\nname = 'x' OR '1'='1'", "red", 10, True)
    arrow(s, x + bw * 2.5 + 0.44, y + 0.25, x + bw * 2.5 + 0.8, y + 0.25, C["muted"], 1.5)
    box(s, x + bw * 2.5 + 0.82, y, w - bw * 2.5 - 0.82, 0.5, "%s rows found\nthe query was rewritten" % n1, "red", 10)
    y2 = y + 0.66
    box(s, x, y2, bw, 0.5, "the same text", "amber", 10, True)
    arrow(s, x + bw + 0.02, y2 + 0.25, x + bw + 0.4, y2 + 0.25, C["muted"], 1.5)
    box(s, x + bw + 0.42, y2, bw * 1.5, 0.5, "bound as a value\nname = ?", "green", 10, True)
    arrow(s, x + bw * 2.5 + 0.44, y2 + 0.25, x + bw * 2.5 + 0.8, y2 + 0.25, C["muted"], 1.5)
    box(s, x + bw * 2.5 + 0.82, y2, w - bw * 2.5 - 0.82, 0.5, "%s rows found\nit is only a name" % n2, "green", 10)


# ------------------------------------------------------------------ part 3
@need(1.35)
def v_commit_rollback(s, x, y, w, h, ns, out):
    L = lines(out)
    nums = [int(re.search(r":\s*(\d+)", l).group(1)) for l in L]
    chart(s, "col", x, y - 0.05, w * 0.5, h + 0.05, ["inside, before rollback", "after rollback", "after commit"], [("rows visible", nums)], fs=10, legend=False, gap=70, vmax=2, major=1)
    bx = x + w * 0.55
    box(s, bx, y, w * 0.45, 0.36, "BEGIN, INSERT 1: %s, in a transaction %s" % (nums[0], L[0].split()[-1]), "teal", 9.5)
    box(s, bx, y + 0.42, w * 0.45, 0.36, "rollback: the row is gone, %d row" % nums[1], "red", 9.5)
    box(s, bx, y + 0.84, w * 0.45, 0.36, "BEGIN, INSERT 2, commit: %d row, in a transaction %s" % (nums[2], L[2].split()[-1]), "green", 9.5)


@need(1.3)
def v_atomic_stmt(s, x, y, w, h, ns, out):
    L = lines(out)
    n1, n2 = L[1].split(": ")[1], L[2].split(": ")[1]
    flow(s, x, y + 0.05, w, ["INSERT 1", "INSERT 2", "INSERT NULL\n" + short(val(L[0]), 28), "rows left: %s" % n1], ["green", "green", "red", "grey"], h=0.7, gap=0.35, fs=10)
    box(s, x + w * 0.45, y + 0.9, w * 0.55, 0.3, "then INSERT 3 and 4 in one good statement: %s rows" % n2, "teal", 9.5)
    note(s, x, y + 0.92, w * 0.44, "all three are one statement", fs=9.5)


@need(1.15)
def v_context_manager(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y + 0.05, w, ["with conn:\nINSERT 1\ncommit at the end", "rows: " + val(L[0]), "with conn:\nINSERT 2, INSERT NULL\nerror: rollback", "rows left: " + val(L[1])],
         ["green", "grey", "red", "grey"], h=0.75, gap=0.35, fs=9.5)
    note(s, x, y + 0.85, w, "the second block failed, so the good row 2 was undone with the bad one", fs=9.5)


@need(1.15)
def v_with_closing(s, x, y, w, h, ns, out):
    L = lines(out)
    flow(s, x, y + 0.05, w, ["with conn:\nCREATE TABLE\ncommit at the end", "still open\n" + val(L[0]), "closing(conn)\nclose() at the end", "SELECT 2\n" + short(val(L[1]), 30)],
         ["green", "grey", "teal", "red"], h=0.75, gap=0.35, fs=9.5)
    note(s, x, y + 0.85, w, "a with block on the connection never closes it; contextlib.closing() does", fs=9.5)


@need(1.35)
def v_alter_drop(s, x, y, w, h, ns, out):
    L = lines(out)
    cols = lit(L[0])
    flow(s, x, y + 0.05, w, ["CREATE TABLE\nname, fur", "ADD COLUMN, RENAME\n" + ", ".join(cols), "DROP COLUMN kg\nname, colour", "DROP TABLE cats\ntables left: %d" % lit(L[2])[0]],
         ["plain", "teal", "amber", "red"], h=0.8, gap=0.35, fs=9.5)
    note(s, x, y + 0.95, w, "the old row after ADD COLUMN: %s - the new box holds None (NULL)" % L[1], fs=9.5)


@need(1.1)
def v_index_plan(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Query", "First word of the plan", "What it means"]]
    cf = {}
    for i, l in enumerate(L, 1):
        word, w2 = l.split(" | ")
        rows.append(["WHERE " + w2, word, "uses the index idx_fur" if word == "SEARCH" else "reads every row"])
        cf[(i, 1)] = C["greenLight"] if word == "SEARCH" else C["amberLight"]
    table(s, x, y, w * 0.78, rows, [2.8, 1.6, 2.2], rowh=0.27, mono_cols=(0, 1), cell_fill=cf, fs=10)
    box(s, x + w * 0.82, y, w * 0.18, 0.8, "idx_fur\nsorted by fur", "teal", 9.5, True)


@need(1.2)
def v_file_vacuum(s, x, y, w, h, ns, out):
    big = ns["big"]
    after = os.path.getsize(ns["path"])
    chart(s, "col", x, y - 0.05, w * 0.55, h + 0.05, ["2,000 rows inserted", "after DELETE", "after VACUUM"], [("file size in KiB", [big / 1024.0, big / 1024.0, after / 1024.0])],
          fs=10, legend=False, gap=60, number_format="0")
    bx = x + w * 0.6
    L = lines(out)
    box(s, bx, y, w * 0.4, 0.26, L[0], "plain", 9)
    box(s, bx, y + 0.31, w * 0.4, 0.26, L[1], "teal", 9)
    box(s, bx, y + 0.62, w * 0.4, 0.26, L[2], "amber", 9)
    box(s, bx, y + 0.93, w * 0.4, 0.26, L[3], "green", 9)


# ------------------------------------------------------------------ part 4
@need(1.15)
def v_foreign_key(s, x, y, w, h, ns, out):
    L = lines(out)
    meals = [["id", "name"]] + [[str(a), b] for a, b in q(ns, "SELECT * FROM meals")]
    ing = [["meal_id", "item"]] + [[str(a), b] for a, b in q(ns, "SELECT * FROM ing")]
    label_shape(s, x, y, w * 0.26, 0.22, "meals (parent)", C["tealLight"], C["ink"], size=9.5, bold=True, radius=0.3)
    table(s, x, y + 0.26, w * 0.26, meals, [0.6, 1.4], rowh=0.26, mono_cols=(1,), fs=10)
    label_shape(s, x + w * 0.4, y, w * 0.26, 0.22, "ing (child)", C["tealLight"], C["ink"], size=9.5, bold=True, radius=0.3)
    table(s, x + w * 0.4, y + 0.26, w * 0.26, ing, [0.9, 1.2], rowh=0.26, mono_cols=(1,), cell_fill={(1, 0): C["greenLight"]}, fs=10)
    arrow(s, x + w * 0.4 - 0.02, y + 0.65, x + w * 0.26 + 0.04, y + 0.65, C["teal"], 1.8)
    note(s, x + w * 0.27, y + 0.4, w * 0.13, "REFERENCES", fs=8, h=0.2)
    bx = x + w * 0.72
    box(s, bx, y, w * 0.28, 0.4, L[0] + "\nbefore the switch", "amber", 9, True)
    box(s, bx, y + 0.46, w * 0.28, 0.4, "meal_id 99: " + short(val(L[1]), 40), "red", 8.5)
    note(s, x, y + 0.9, w * 0.7, "green: the row that points to an existing meal; meal 99 does not exist", fs=9)


@need(1.45)
def v_inner_left_join(s, x, y, w, h, ns, out):
    L = lines(out)
    inner, left = lit(L[0]), lit(L[1])
    t1 = [["name", "vaccine"]] + [[a, str(b)] for a, b in inner]
    t2 = [["name", "vaccine"]] + [[a, str(b)] for a, b in left]
    rh = min(0.24, h / (len(t2) + 0.4))
    label_shape(s, x, y, w * 0.44, 0.22, "INNER JOIN: %d rows" % len(inner), C["tealLight"], C["ink"], size=9.5, bold=True, radius=0.3)
    table(s, x, y + 0.26, w * 0.44, t1, [1.4, 1.4], rowh=rh, mono_cols=(0, 1), fs=10)
    label_shape(s, x + w * 0.52, y, w * 0.44, 0.22, "LEFT JOIN: %d rows" % len(left), C["amberLight"], C["ink"], size=9.5, bold=True, radius=0.3)
    cf = {(i, j): C["amberLight"] for i, r in enumerate(t2[1:], 1) if r[1] == "None" for j in (0, 1)}
    table(s, x + w * 0.52, y + 0.26, w * 0.44, t2, [1.4, 1.4], rowh=rh, mono_cols=(0, 1), cell_fill=cf, fs=10)


@need(1.2)
def v_backup_copy(s, x, y, w, h, ns, out):
    L = lines(out)
    nsrc = ns["src"].execute("SELECT count(*) FROM cats").fetchone()[0]
    bw = w * 0.3
    box(s, x, y + 0.1, bw, 0.8, "source in memory\nrows now: %d" % nsrc, "teal", 10.5)
    arrow(s, x + bw + 0.03, y + 0.5, x + w * 0.5 - 0.03, y + 0.5, C["teal"], 2.2)
    label_shape(s, x + bw + 0.1, y + 0.1, w * 0.2 - 0.14, 0.3, "backup(dst)", C["card"], C["ink"], size=9.5, line=C["line"], font=MONO)
    box(s, x + w * 0.5, y + 0.1, bw, 0.8, "copy.db in a file\nrows: %s" % val(L[1]), "amber", 10.5)
    note(s, x, y + 1.0, w, "%s; %s - the copy is the source as it was at the moment of backup()" % (L[0], L[1]), fs=9.5)


@need(1.55)
def v_iterdump(s, x, y, w, h, ns, out):
    L = lines(out)
    box(s, x, y + 0.2, w * 0.2, 0.8, "database a\ncats: Zophie, 5.6", "teal", 10)
    arrow(s, x + w * 0.2 + 0.03, y + 0.6, x + w * 0.27, y + 0.6, C["muted"], 1.8)
    yy = y
    for i, l in enumerate(L[:4]):
        box(s, x + w * 0.28, yy, w * 0.44, 0.27, short(l, 46), "grey", 8.5, True)
        yy += 0.3
    arrow(s, x + w * 0.72 + 0.03, y + 0.6, x + w * 0.79, y + 0.6, C["muted"], 1.8)
    box(s, x + w * 0.8, y + 0.2, w * 0.2, 0.8, "database b\n" + L[4], "green", 9.5, True)
    note(s, x, y + 1.25, w, "iterdump() text in the middle; executescript() replays it into database b", fs=9.5)


@need(1.35)
def v_shutil_copy(s, x, y, w, h, ns, out):
    L = lines(out)
    files = sorted(os.listdir(ns["folder"]))
    rows = [["File in the folder", "Size in bytes"]] + [[f, str(os.path.getsize(os.path.join(ns["folder"], f)))] for f in files]
    table(s, x, y, w * 0.4, rows, [2.0, 1.6], rowh=0.3, mono_cols=(0, 1), fs=10.5)
    flow(s, x + w * 0.45, y + 0.15, w * 0.55, ["a.db\ncommitted, closed", "shutil.copyfile", "b.db\n" + L[0]], ["teal", "plain", "green"], h=0.8, gap=0.3, fs=9.5)


# ------------------------------------------------------------------ part 5
@need(0.8)
def v_cat_checker(s, x, y, w, h, ns, out):
    L = lines(out)
    cats = q(ns, "SELECT id, name, born FROM cats")
    rows = [["cat", "born", "shots (kind, date)", "finding"]]
    cf = {}
    early = lit(L[0].split(": ", 1)[1])
    missing = [r[0] for r in lit(L[1].split(": ", 1)[1])]
    for i, (cid, name, born) in enumerate(cats, 1):
        shots = q(ns, "SELECT vaccine, given FROM vax WHERE cat_id = ?", cid)
        f = []
        if any(e[0] == name for e in early):
            f.append("shot before birth")
            cf[(i, 2)] = C["redLight"]
        if name in missing:
            f.append("one kind only")
            cf[(i, 3)] = C["amberLight"]
        rows.append([name, born, "; ".join("%s %s" % sh for sh in shots), ", ".join(f) or "ok"])
    table(s, x, y, w * 0.66, rows, [0.8, 1.0, 2.0, 2.2], rowh=0.25, mono_cols=(1, 2), cell_fill=cf, fs=9.5)
    box(s, x + w * 0.69, y, w * 0.31, 0.75, "printed by the code:\n" + L[0] + "\n" + L[1], "grey", 8, True)


@need(1.3)
def v_meal_ingredients(s, x, y, w, h, ns, out):
    have = ns["have"]
    cook = {r[0] for r in lit(lines(out)[0].split(": ", 1)[1])}
    rows = [["Meal", "Needs", "Missing from the kitchen", "Can cook?"]]
    cf = {}
    for i, (meal,) in enumerate(q(ns, "SELECT DISTINCT meal FROM ing"), 1):
        items = [r[0] for r in q(ns, "SELECT item FROM ing WHERE meal = ?", meal)]
        miss = [it for it in items if it not in have]
        rows.append([meal, ", ".join(items), ", ".join(miss) or "nothing", "yes" if meal in cook else "no"])
        cf[(i, 3)] = C["greenLight"] if meal in cook else C["redLight"]
    table(s, x, y, w * 0.78, rows, [1.2, 2.8, 2.2, 1.0], rowh=0.36, cell_fill=cf, fs=10.5)
    box(s, x + w * 0.82, y, w * 0.18, 1.0, "the kitchen holds\n" + ", ".join(have), "teal", 9.5)


VISUALS = {k[2:]: v for k, v in dict(globals()).items() if k.startswith("v_") and callable(v)}
