"""Chapter 10 deck visuals, version 4.0.0 (Lineage11; helpers as in the chapter 11 visuals): the result of every code example, drawn in the right column (3.25 in wide) beside the one code box.
Every name, number and truth value shown is taken from the run of the example itself: the printed text `out`, the namespace `ns` and the temporary folder in which the
example ran (the current directory while a visual is drawn). Nothing is typed in by hand except the plain-language column names.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "4.0.0"
import os
import re
import zipfile
from pathlib import Path
from pptx.enum.text import PP_ALIGN
from deck_kit_v2_1_0 import C, MONO, arrow, chart, label_shape, table as _table, tb


def need(h):
    def deco(f):
        f.need = h
        return f
    return deco


def short(t, n):
    t = str(t)
    return t if len(t) <= n else t[:n - 3] + "..."


def chip(s, x, y, w, h, text, kind="plain", fs=9.5):
    fill, col = {"plain": (C["card"], C["ink"]), "teal": (C["tealLight"], C["ink"]), "amber": (C["amberLight"], C["ink"]),
                 "green": (C["greenLight"], C["ink"]), "grey": (C["grey"], C["muted"]), "red": (C["redLight"], C["ink"])}[kind]
    return label_shape(s, x, y, w, h, text, fill, col, size=fs, font=MONO, line=C["line"], radius=0.15)


def heading(s, x, y, w, text):
    tb(s, x, y, w, 0.24, text, 10, C["muted"], bold=True)
    return y + 0.26


def printed(s, x, y, w, out, kind="teal", most=7):
    """What the run printed: one chip per non-empty line."""
    y = heading(s, x, y, w, "printed")
    L = [l for l in out.splitlines() if l.strip()]
    for l in L[:most]:
        chip(s, x, y, w, 0.27, short(l, 38), kind)
        y += 0.31
    if len(L) > most:
        tb(s, x, y, w, 0.22, "... and %d more lines" % (len(L) - most), 9, C["muted"], italic=True)
        y += 0.24
    return y


def entries(root="."):
    root = Path(root)
    return sorted(str(p.relative_to(root)) + ("/" if p.is_dir() else "") for p in root.rglob("*") if p.name != "__pycache__")


def folder_now(s, x, y, w, items=None, most=9, title="in the folder now", root="."):
    """The files and folders that exist after the run, as a native table, indented by depth."""
    y = heading(s, x, y, w, title)
    items = entries(root) if items is None else items
    shown = items[:most]
    rows = [["name"]] + [["  " * (it.rstrip("/").count("/")) + it.rstrip("/").split("/")[-1] + ("/" if it.endswith("/") else "")] for it in shown]
    if len(items) > most:
        rows.append(["... %d more" % (len(items) - most)])
    _table(s, x, y, w, rows, [w], fs=9, rowh=0.25, mono_cols=(0,))
    return y + 0.25 * len(rows) + 0.05


@need(2.0)
def v_pathobjects(s, x, y, w, h, ns, out):
    y = heading(s, x, y, w, "three ways, one path")
    rows = [["written as", "gives"], ["Path('spam', 'bacon', 'eggs')", str(Path("spam", "bacon", "eggs"))], ["Path('spam') / 'bacon' / 'eggs'", str(Path("spam") / "bacon" / "eggs")],
            ["Path('spam') / Path('bacon', 'eggs')", str(Path("spam") / Path("bacon", "eggs"))]]
    _table(s, x, y, w, rows, [2.1, w - 2.1], fs=8.5, rowh=0.34, mono_cols=(0, 1))
    chip(s, x, y + 1.5, w, 0.28, "joined with a file name: %s" % [l for l in out.splitlines() if l.strip()][-1], "teal", fs=9)


@need(1.8)
def v_locations(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "the four questions and the answers")
    rows = [["question", "answer"], ["cwd() is absolute?", a[0]], ["home() is absolute?", a[1]], ["spam/... is absolute?", a[2]], ["./spam.txt is spam.txt?", a[3]]]
    _table(s, x, y, w, rows, [2.3, w - 2.3], fs=9, rowh=0.3, mono_cols=(1,))


@need(2.2)
def v_anatomy(s, x, y, w, h, ns, out):
    p = ns["p"]
    y = heading(s, x, y, w, "the parts of the path")
    rows = [["part", "value"], ["drive", p.drive], ["anchor", p.anchor], ["parent", str(p.parent)], ["name", p.name], ["stem", p.stem], ["suffix", p.suffix]]
    _table(s, x, y, w, rows, [1.0, w - 1.0], fs=9, rowh=0.28, mono_cols=(1,))


@need(2.0)
def v_folders(s, x, y, w, h, ns, out):
    folder_now(s, x, y, w, entries("delicious"), title="below delicious", root="delicious", most=7)


@need(2.0)
def v_glob(s, x, y, w, h, ns, out):
    names = sorted(os.listdir("."))
    import fnmatch
    y = heading(s, x, y, w, "which files each pattern takes")
    rows = [["file", "*.txt", "project?.txt"]] + [[n, "yes" if fnmatch.fnmatch(n, "*.txt") else "-", "yes" if fnmatch.fnmatch(n, "project?.txt") else "-"] for n in names]
    _table(s, x, y, w, rows, [1.55, 0.7, w - 2.25], fs=9, rowh=0.28, mono_cols=(0,))


@need(2.0)
def v_fileinfo(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "what the run found out")
    rows = [["question", "answer"], ["exists, file, folder", a[0]], ["size in bytes", a[1]], ["last changed (UTC)", a[2]], ["nothere exists?", a[3]]]
    _table(s, x, y, w, rows, [1.45, w - 1.45], fs=9, rowh=0.36, mono_cols=(1,))


@need(1.6)
def v_wholefile(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "what each call gave back")
    rows = [["call", "returned"], ["write_text(...)", a[0]], ["read_text()", a[1]]]
    _table(s, x, y, w, rows, [1.5, w - 1.5], fs=9.5, rowh=0.34, mono_cols=(0, 1))
    chip(s, x, y + 1.2, w, 0.28, "13 characters written", "green")


@need(2.4)
def v_openclose(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    chart(s, "col", x, y, w, 1.9, ["write (w)", "append (a)"], [("characters", [int(a[0]), int(a[1])])], fs=9, legend=False, gap=60, axis_title="characters written by the call", number_format="#,##0")
    chip(s, x, y + 2.0, w, 0.28, "file now: %d bytes" % os.path.getsize("bacon.txt"), "amber")


@need(2.0)
def v_readmethods(s, x, y, w, h, ns, out):
    a = out.splitlines()
    y = heading(s, x, y, w, "what each step returned")
    rows = [["step", "result"], ["lines read", a[0]], ["first line", short(a[1], 24)], ["read() afterwards", a[2]]]
    _table(s, x, y, w, rows, [1.45, w - 1.45], fs=9, rowh=0.34, mono_cols=(1,))
    tb(s, x, y + 1.5, w, 0.5, "the cursor is at the end, so nothing is left", 10, C["muted"], italic=True)


@need(1.6)
def v_withstatement(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "after the with block")
    rows = [["what", "value"], ["content read", a[0]], ["file closed?", a[1]]]
    _table(s, x, y, w, rows, [1.5, w - 1.5], fs=9.5, rowh=0.34, mono_cols=(1,))


@need(2.0)
def v_modes(s, x, y, w, h, ns, out):
    y = heading(s, x, y, w, "the file after each step")
    rows = [["step", "mode", "file holds"]]
    for n, l in enumerate([l for l in out.splitlines() if l.strip()], 1):
        mode, rest = l.split(" ", 1)
        rows.append([str(n), mode, rest.replace("\\n", " ")])
    _table(s, x, y, w, rows, [0.55, 0.65, w - 1.2], fs=9, rowh=0.3, mono_cols=(1, 2))
    tb(s, x, y + 0.3 * len(rows) + 0.1, w, 0.5, "w starts the file again; a adds at the end", 10, C["muted"], italic=True)


@need(2.4)
def v_encoding(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    n, b = a[1].split()
    chart(s, "col", x, y, w, 1.9, ["characters", "bytes"], [("count", [int(n), int(b)])], fs=9, legend=False, gap=60, axis_title="in the word", number_format="0")
    chip(s, x, y + 2.0, w, 0.28, short(a[2], 38), "teal")


@need(1.8)
def v_shelve(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "read back from the file")
    rows = [["what", "value"], ["type", "DbfilenameShelf"], ["keys", a[1]], ["cats", a[2]]]
    _table(s, x, y, w, rows, [0.9, w - 0.9], fs=9, rowh=0.36, mono_cols=(1,))


@need(1.8)
def v_json(s, x, y, w, h, ns, out):
    a = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "dictionary to text and back")
    rows = [["step", "result"], ["dumps() gives", short(a[0], 28)], ["loads() equal?", a[1]]]
    _table(s, x, y, w, rows, [1.2, w - 1.2], fs=9, rowh=0.38, mono_cols=(1,))


@need(2.2)
def v_madlibs(s, x, y, w, h, ns, out):
    y = heading(s, x, y, w, "the saved story")
    tb(s, x, y, w, 1.1, out.strip(), 10, C["ink"], italic=True)
    folder_now(s, x, y + 1.2, w, entries("."), title="files now", most=4)


@need(2.0)
def v_regexsearch(s, x, y, w, h, ns, out):
    y = heading(s, x, y, w, "the matching lines")
    rows = [["file", "line", "text"]]
    for l in [l for l in out.splitlines() if l.strip()]:
        f, n, t = l.split(" ", 2)
        rows.append([f, n, short(t, 22)])
    _table(s, x, y, w, rows, [0.8, 0.5, w - 1.3], fs=9, rowh=0.3, mono_cols=(0, 2))
    tb(s, x, y + 0.3 * len(rows) + 0.1, w, 0.5, "SPAM in capitals is not matched; notes.csv is not read", 10, C["muted"], italic=True)


@need(2.0)
def v_quizquestion(s, x, y, w, h, ns, out):
    y = heading(s, x, y, w, "the four options")
    rows = [["letter", "option", "right?"]]
    for i in range(4):
        rows.append(["ABCD"[i], ns["options"][i], "yes" if ns["options"][i] == ns["correct"] else "-"])
    _table(s, x, y, w, rows, [0.7, w - 1.5, 0.8], fs=9, rowh=0.3, mono_cols=(0, 1))


@need(2.4)
def v_quizfiles(s, x, y, w, h, ns, out):
    key = open("quiz_key1.txt", encoding="UTF-8").read().split("\n")
    y = heading(s, x, y, w, "quiz_key1.txt")
    rows = [["question", "answer"]] + [[l.split(". ")[0], l.split(". ")[1]] for l in key if l.strip()]
    _table(s, x, y, w, rows, [1.2, w - 1.2], fs=9, rowh=0.28, mono_cols=(0, 1))
    chip(s, x, y + 0.28 * len(rows) + 0.1, w, 0.28, "quiz1.txt: 4 questions", "amber")


VISUALS = {"pathobjects": v_pathobjects, "locations": v_locations, "anatomy": v_anatomy, "folders": v_folders, "glob": v_glob, "fileinfo": v_fileinfo,
           "wholefile": v_wholefile, "openclose": v_openclose, "readmethods": v_readmethods, "withstatement": v_withstatement, "modes": v_modes,
           "encoding": v_encoding, "shelve": v_shelve, "json": v_json, "madlibs": v_madlibs, "regexsearch": v_regexsearch, "quizquestion": v_quizquestion,
           "quizfiles": v_quizfiles}
