"""Chapter 11 deck visuals, version 4.0.0 (Lineage11): the result of every code example, drawn in the right column (3.25 in wide) beside the one code box.
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
def v_copy(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out)
    folder_now(s, x, y + 0.05, w, [e for e in entries() if e.startswith(("file1", "spam"))])


@need(2.0)
def v_copytree(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out)
    a = entries("spam")
    b = entries("spam_backup")
    chip(s, x, y + 0.02, w, 0.28, "spam: %d entries, spam_backup: %d" % (len(a), len(b)), "amber")
    chip(s, x, y + 0.36, w, 0.28, "same names in both: %s" % (a == b), "green" if a == b else "red")
    folder_now(s, x, y + 0.72, w, entries("spam_backup"), title="in spam_backup", root=".")


@need(1.8)
def v_copy2(s, x, y, w, h, ns, out):
    t = [Path("spam/file1.txt").stat().st_mtime, Path("spam/kept.txt").stat().st_mtime]
    y = printed(s, x, y, w, out, "green")
    y = heading(s, x, y + 0.05, w, "time stamps (seconds since 1970)")
    rows = [["file", "time stamp"], ["spam/file1.txt", str(int(t[0]))], ["spam/kept.txt", str(int(t[1]))]]
    _table(s, x, y, w, rows, [1.6, w - 1.6], fs=9, rowh=0.27, mono_cols=(0, 1))
    tb(s, x, y + 0.9, w, 0.5, "the copy carries the time stamp of the original", 10, C["muted"], italic=True)


@need(1.8)
def v_move(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out)
    folder_now(s, x, y + 0.05, w, [e for e in entries() if e.startswith(("spam", "spam2"))])


@need(1.8)
def v_unlink(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "grey")
    folder_now(s, x, y + 0.05, w, entries(), title="what is left")
    tb(s, x, y + 1.1, w, 0.5, "no recycle bin: deleted for good", 10, C["coral"], italic=True)


@need(1.8)
def v_rmtree(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "red")
    y = heading(s, x, y + 0.05, w, "before and after the call")
    rows = [["path", "before", "after"]]
    for name, was in (("spam", True), ("spam/eggs", True), ("spam/eggs/file2.txt", True)):
        rows.append([name, "there" if was else "-", "there" if Path(name).exists() else "gone"])
    _table(s, x, y, w, rows, [1.65, 0.8, w - 2.45], fs=9, rowh=0.27, mono_cols=(0,))


@need(1.8)
def v_dryrun(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "amber")
    y = heading(s, x, y + 0.05, w, "files in the folder, by pattern")
    rows = [["file", "matches *.rxt"]] + [[n, str(Path(n).match("*.rxt"))] for n in sorted(os.listdir("."))]
    _table(s, x, y, w, rows, [1.6, w - 1.6], fs=9, rowh=0.27, mono_cols=(0, 1))
    tb(s, x, y + 0.3 * len(rows) + 0.05, w, 0.5, "only the typo's match is listed", 10, C["muted"], italic=True)


@need(2.0)
def v_listing(s, x, y, w, h, ns, out):
    L = [l for l in out.splitlines() if l.strip()]
    y = heading(s, x, y, w, "the two calls give the same names")
    chip(s, x, y, w, 0.27, short(L[0], 38), "teal")
    chip(s, x, y + 0.31, w, 0.27, "same count: %s" % (len(eval(L[0])) == len(L[1].split("), ")) ), "green")
    folder_now(s, x, y + 0.7, w, entries("spam"), title="inside spam", root="spam", most=8)


@need(2.5)
def v_walk(s, x, y, w, h, ns, out):
    L = out.splitlines()
    n_dirs = sum(1 for l in L if l.startswith("The current folder"))
    n_files = sum(1 for l in L if l.startswith("FILE INSIDE"))
    y = heading(s, x, y, w, "the tree that was walked")
    y = folder_now(s, x, y - 0.05, w, entries("spam"), title="spam, every level", root="spam", most=9)
    chip(s, x, y + 0.05, w, 0.28, "folders visited: %d" % n_dirs, "amber")
    chip(s, x, y + 0.39, w, 0.28, "files seen: %d" % n_files, "green")


@need(2.2)
def v_sizes(s, x, y, w, h, ns, out):
    sizes = {}
    for folder, subs, files in os.walk("spam"):
        sizes[folder] = sum(os.path.getsize(os.path.join(folder, f)) for f in files)
    names = sorted(sizes)
    chart(s, "bar", x, y, w, 2.0, names[::-1], [("bytes", [sizes[n] for n in names][::-1])], fs=9, legend=False, gap=50, axis_title="bytes of the files in each folder")
    chip(s, x, y + 2.1, w, 0.28, "printed total: %s bytes" % out.strip(), "green")


@need(1.5)
def v_mkdir(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "green")
    folder_now(s, x, y + 0.05, w, entries(), title="made by one call")


@need(2.5)
def v_zipwrite(s, x, y, w, h, ns, out):
    info = ns["info"]
    chart(s, "col", x, y, w, 2.2, ["original", "in the ZIP file"], [("bytes", [info.file_size, info.compress_size])], fs=9, legend=False, gap=60, axis_title="bytes", number_format="#,##0")
    chip(s, x, y + 2.3, w, 0.28, "%.0f times smaller" % (info.file_size / info.compress_size), "green")
    chip(s, x, y + 2.64, w, 0.28, short(out.strip(), 38), "teal")


@need(1.8)
def v_zipmodes(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "teal")
    with zipfile.ZipFile("example.zip") as z:
        rows = [["name in the ZIP file", "bytes"]] + [[i.filename, str(i.file_size)] for i in z.infolist()]
    _table(s, x, y + 0.1, w, rows, [2.1, w - 2.1], fs=9, rowh=0.27, mono_cols=(0, 1))


@need(1.8)
def v_extract(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "teal")
    folder_now(s, x, y + 0.05, w, [e for e in entries() if e.startswith(("out", "new"))], title="unpacked here")


@need(2.0)
def v_archives(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "teal")
    with zipfile.ZipFile("spam_backup.zip") as z:
        names = z.namelist()
    y = heading(s, x, y + 0.05, w, "inside spam_backup.zip")
    rows = [["name"]] + [[n] for n in names[:6]]
    _table(s, x, y, w, rows, [w], fs=9, rowh=0.25, mono_cols=(0,))
    chip(s, x, y + 0.3 * len(rows) + 0.05, w, 0.28, "unpacked into spam_copy: %d entries" % len(entries("spam_copy")), "green")


@need(2.5)
def v_backup(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "teal")
    with zipfile.ZipFile("spam_1.zip") as z:
        names = z.namelist()
    y = heading(s, x, y + 0.05, w, "inside spam_1.zip")
    rows = [["name"]] + [[n] for n in names[:6]]
    _table(s, x, y, w, rows, [w], fs=9, rowh=0.25, mono_cols=(0,))
    chip(s, x, y + 0.3 * len(rows) + 0.05, w, 0.28, "the next run makes spam_2.zip", "amber")


@need(1.8)
def v_selective(s, x, y, w, h, ns, out):
    y = printed(s, x, y, w, out, "green")
    src = sorted(f for _, _, fs in os.walk("src") for f in fs)
    chip(s, x, y + 0.05, w, 0.28, "files in src: %d, copied: %d" % (len(src), len(os.listdir("dest"))), "amber")
    folder_now(s, x, y + 0.45, w, entries("src"), title="in src", root="src", most=6)


@need(2.2)
def v_large(s, x, y, w, h, ns, out):
    found = {}
    for folder, subs, files in os.walk("spam"):
        for f in files:
            p = os.path.join(folder, f)
            found[p] = os.path.getsize(p)
    names = sorted(found, key=found.get)
    chart(s, "bar", x, y, w, 2.0, names, [("bytes", [found[n] for n in names])], fs=9, legend=False, gap=50, axis_title="bytes (the limit is 1000)", number_format="#,##0")
    chip(s, x, y + 2.1, w, 0.28, "printed: %d of %d files" % (len([l for l in out.splitlines() if l.strip()]), len(found)), "green")


@need(1.8)
def v_dates(s, x, y, w, h, ns, out):
    y = heading(s, x, y, w, "names after the run")
    rows = [["name", "date part"]]
    for n in sorted(os.listdir(".")):
        m = re.search(r"\d\d-\d\d-\d\d\d\d", n)
        rows.append([n, m.group(0) if m else "none"])
    _table(s, x, y, w, rows, [2.1, w - 2.1], fs=9, rowh=0.3, mono_cols=(0, 1))
    tb(s, x, y + 0.3 * len(rows) + 0.1, w, 0.5, "day and month changed places; notes.txt has no date and stays", 10, C["muted"], italic=True)


VISUALS = {"copy": v_copy, "copytree": v_copytree, "copy2": v_copy2, "move": v_move, "unlink": v_unlink, "rmtree": v_rmtree, "dryrun": v_dryrun,
           "listing": v_listing, "walk": v_walk, "sizes": v_sizes, "mkdir": v_mkdir, "zipwrite": v_zipwrite, "zipmodes": v_zipmodes, "extract": v_extract,
           "archives": v_archives, "backup": v_backup, "selective": v_selective, "large": v_large, "dates": v_dates}
