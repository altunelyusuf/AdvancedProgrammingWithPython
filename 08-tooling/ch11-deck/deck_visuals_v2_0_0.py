"""Chapter 11 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a
drawn diagram (boxes joined by arrows). Every name, number and truth value shown is taken from the run of the example itself: the
printed text `out`, the namespace `ns` and the temporary folder in which the example ran (the current directory while a visual is
drawn); nothing is typed in by hand except the plain-language names of columns.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import ast
import os
from pathlib import Path
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from deck_kit_v2_0_0 import C, MONO, arrow, chart, label_shape, table as _table, tb, rect, line_seg


def table(s, x, y, w, rows, colw, fs=10.5, **kw):
    return _table(s, x, y, w, rows, colw, fs=fs, **kw)


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


def lines(out):
    return [l for l in out.splitlines()]


def lit(line):
    return ast.literal_eval(line)


def tree(s, x, y, nodes, edges, cw=1.5, ch=0.3, fs=9.5, kinds=None, gap=0.35):
    """nodes: {name: (col, row)}; edges: [(parent, child)]. Boxes with elbow-free straight arrows from parent's right edge to child's left edge."""
    kinds = kinds or {}
    pos = {}
    for n, (c_, r_) in nodes.items():
        px, py = x + c_ * (cw + gap), y + r_ * (ch + 0.12)
        pos[n] = (px, py)
        chip(s, px, py, cw, ch, n, kinds.get(n, "plain"), fs=fs)
    for a, b in edges:
        (ax, ay), (bx, by) = pos[a], pos[b]
        arrow(s, ax + cw, ay + ch / 2, bx, by + ch / 2, C["muted"], 1.1)
    return pos


# ------------------------------------------------------------------ part 1
@need(1.35)
def v_copy(s, x, y, w, h, ns, out):
    L = lines(out)
    listing = lit(L[2])
    chip(s, x, y + 0.42, 1.1, 0.34, "a.txt", "amber", fs=11)
    chip(s, x + 2.1, y, 1.7, 0.32, L[0], "teal", fs=10.5)
    chip(s, x + 2.1, y + 0.85, 1.7, 0.32, L[1], "teal", fs=10.5)
    arrow(s, x + 1.1, y + 0.52, x + 2.1, y + 0.16, C["teal"], 1.4)
    arrow(s, x + 1.1, y + 0.67, x + 2.1, y + 1.01, C["teal"], 1.4)
    rows = [["Target you gave", "Name of the copy", "Returned"],
            ["a folder: 'box'", Path(L[0]).name, L[0]], ["a file name: 'box/b.txt'", Path(L[1]).name, L[1]]]
    table(s, x + 4.2, y, w - 4.2, rows, [2.0, 1.2, 1.4], rowh=0.3, mono_cols=(0, 1, 2), fs=10)
    chip(s, x + 4.2, y + 1.0, w - 4.2, 0.3, "the folder box now holds %s" % listing, "green", fs=10)


@need(1.3)
def v_copytree(s, x, y, w, h, ns, out):
    L = lines(out)
    box = sorted(str(p.relative_to("box")) for p in Path("box").rglob("*"))
    bak = sorted(str(p.relative_to("bak")) for p in Path("bak").rglob("*"))
    tree(s, x, y, {"box": (0, 0), "inner": (1, 0), "y.txt": (1, 1)}, [("box", "inner"), ("box", "y.txt")], cw=0.75, kinds={"box": "teal"})
    arrow(s, x + 1.95, y + 0.3, x + 2.45, y + 0.3, C["amber"], 1.8)
    tree(s, x + 2.5, y, {"bak": (0, 0), "inner ": (1, 0), "y.txt ": (1, 1)}, [("bak", "inner "), ("bak", "y.txt ")], cw=0.75, kinds={"bak": "amber"})
    chip(s, x, y + 0.95, 4.4, 0.3, "entries in box: %d, in bak: %d, equal: %s" % (len(box), len(bak), box == bak), "green", fs=10)
    rows = [["Call", "Result"], ["copytree('box', 'bak')", L[0]], ["the same call again", "refused"], ["with dirs_exist_ok=True", L[2]]]
    table(s, x + 4.7, y, w - 4.7, rows, [2.5, 1.5], rowh=0.3, mono_cols=(0, 1), fs=10, cell_color={(2, 1): C["coral"], (1, 1): C["green"], (3, 1): C["green"]})


@need(1.35)
def v_copy2(s, x, y, w, h, ns, out):
    names = ["a.txt (set)", "c.txt (copy2)", "d.txt (copy)"]
    vals = [Path("a.txt").stat().st_mtime, Path("box/c.txt").stat().st_mtime, Path("box/d.txt").stat().st_mtime]
    chart(s, "col", x, y, w * 0.5, h, names, [("modification time, billions of seconds since 1970", [round(v / 1e9, 2) for v in vals])], fs=9, legend=False, gap=50, number_format="0.00")
    rows = [["File", "Time stamp (seconds)", "Same as a.txt?"]] + [[n.split()[0], str(int(v)), str(int(v) == int(vals[0]))] for n, v in zip(names, vals)]
    table(s, x + w * 0.53, y + 0.05, w * 0.47, rows, [1.1, 1.9, 1.5], rowh=0.3, mono_cols=(0, 1, 2), fs=10, cell_color={(2, 2): C["green"], (3, 2): C["coral"], (1, 2): C["green"]})
    tb(s, x + w * 0.53, y + 1.3, w * 0.47, 0.26, "chart: billions of seconds since 1970", 9, C["muted"], italic=True)


@need(1.15)
def v_move(s, x, y, w, h, ns, out):
    L = lines(out)
    chip(s, x, y, 1.7, 0.3, "spam/file1.txt", "amber", fs=10)
    arrow(s, x + 1.7, y + 0.15, x + 2.2, y + 0.15, C["muted"], 1.4)
    chip(s, x + 2.2, y, 1.7, 0.3, L[0], "teal", fs=10)
    chip(s, x, y + 0.55, 1.7, 0.3, "spam2/file1.txt", "amber", fs=10)
    arrow(s, x + 1.7, y + 0.7, x + 2.2, y + 0.7, C["muted"], 1.4)
    chip(s, x + 2.2, y + 0.55, 1.7, 0.3, L[1], "teal", fs=10)
    tb(s, x, y + 0.88, 4.0, 0.26, "into a folder; then moved and renamed in one step", 9, C["muted"], italic=True)
    content, src = L[2].split()
    rows = [["Move onto an existing file name", "Result"], ["spam2/f.txt now holds", content], ["spam/f.txt still exists", src]]
    table(s, x + 4.4, y, w - 4.4, rows, [3.0, 1.4], rowh=0.3, mono_cols=(1,), fs=10, cell_color={(1, 1): C["green"], (2, 1): C["coral"]})
    tb(s, x + 4.4, y + 0.95, w - 4.4, 0.26, "the old text was replaced; the source is gone", 9, C["muted"], italic=True)


# ------------------------------------------------------------------ part 2
@need(1.3)
def v_unlink(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Step", "What the run printed"], ["unlink a.txt", L[0]], ["rmdir on a full folder", L[1]], ["unlink the file, then rmdir", L[2]]]
    table(s, x, y, 6.0, rows, [2.3, 3.7], rowh=0.3, mono_cols=(1,), fs=10, cell_color={(2, 1): C["coral"]})
    chip(s, x + 6.3, y + 0.05, 0.85, 0.3, "a.txt", "amber", fs=10)
    arrow(s, x + 7.15, y + 0.2, x + 7.45, y + 0.2, C["coral"], 1.8)
    chip(s, x + 7.45, y + 0.05, 0.9, 0.3, "gone", "grey", fs=10)
    tb(s, x + 6.3, y + 0.45, 3.0, 0.5, "no recycle bin: os.unlink cannot be undone", 10.5, C["coral"], italic=True)


@need(1.2)
def v_rmtree(s, x, y, w, h, ns, out):
    L = lines(out)
    before = lit(L[0])
    tree(s, x, y, {"spam": (0, 0), "spam/eggs": (1, 0), "spam/eggs/f.txt": (2, 0)}, [("spam", "spam/eggs"), ("spam/eggs", "spam/eggs/f.txt")], cw=1.35, kinds={"spam": "teal"})
    arrow(s, x + 0.65, y + 0.34, x + 0.65, y + 0.62, C["coral"], 1.8)
    chip(s, x, y + 0.65, 1.35, 0.3, "rmtree('spam')", "red", fs=9.5)
    chip(s, x + 1.7, y + 0.65, 3.0, 0.3, L[1], "grey", fs=10)
    tb(s, x, y + 1.0, 5.2, 0.26, "ignore_errors=True: %s" % L[2], 10, C["muted"], italic=True)
    chart(s, "col", x + 5.6, y, w - 5.6, h, ["before", "after"], [("things under spam", [len(before), len(list(Path("spam").rglob("*")) if Path("spam").exists() else [])])], fs=9, legend=False, gap=60, vmax=3, major=1)


@need(1.3)
def v_dryrun(s, x, y, w, h, ns, out):
    L = lines(out)
    files = ["a.txt", "b.txt", "c.rxt"]
    rows = [["Pattern", "Files it matches", "Verdict"]]
    for pat, verdict in (("*.rxt", "typo: the wrong file"), ("*.txt", "the right list")):
        rows.append([pat, str(sorted(p.name for p in Path(".").glob(pat))), verdict])
    table(s, x, y, w * 0.62, rows, [1.2, 2.4, 2.2], rowh=0.3, mono_cols=(0, 1), fs=10, cell_color={(1, 2): C["coral"], (2, 2): C["green"]})
    for i, f in enumerate(files):
        chip(s, x + w * 0.67 + i * 1.0, y + 0.05, 0.95, 0.3, f, "green" if f.endswith(".txt") else "grey", fs=10)
    tb(s, x + w * 0.67, y + 0.42, 3.0, 0.5, "green: printed as 'would delete'\ngrey: stays untouched", 9.5, C["muted"], italic=True)
    chip(s, x, y + 0.98, w * 0.62, 0.3, "printed: %s; %s" % (L[1], L[2]), "amber", fs=10)


# ------------------------------------------------------------------ part 3
@need(1.4)
def v_listing(s, x, y, w, h, ns, out):
    L = lines(out)
    rows = [["Call", "What it returns"], ["os.listdir('spam')", L[0]], ["Path('spam').iterdir()", L[1]], ["glob('*.txt')", L[2]], ["rglob('*.txt')", L[3]]]
    table(s, x, y, w * 0.64, rows, [2.4, 4.0], rowh=0.27, mono_cols=(0, 1), fs=9)
    tree(s, x + w * 0.67, y, {"spam": (0, 0), "eggs": (1, 0), "f2.txt": (2, 0), "file1.txt": (1, 1), "b.pdf": (1, 2)}, [("spam", "eggs"), ("eggs", "f2.txt"), ("spam", "file1.txt"), ("spam", "b.pdf")], cw=0.8, ch=0.26, fs=8.5, kinds={"spam": "teal", "eggs": "teal"}, gap=0.2)


@need(1.4)
def v_walk(s, x, y, w, h, ns, out):
    L = lines(out)
    steps = L[:-1]
    rows = [["Step", "Folder", "Subfolders", "Files"]]
    for i, ln in enumerate(steps, 1):
        folder, rest = ln.split(" ", 1)
        subs, files = rest.split("] [")
        rows.append([str(i), folder, subs + "]", "[" + files])
    table(s, x, y, w * 0.7, rows, [0.5, 1.9, 1.9, 1.6], rowh=0.27, mono_cols=(1, 2, 3), align_cols={0: PP_ALIGN.CENTER}, fs=9)
    tree(s, x + w * 0.74, y, {"spam": (0, 0), "eggs": (1, 0), "bacon": (1, 1), "eggs2": (1, 2)}, [("spam", "eggs"), ("eggs", "bacon"), ("spam", "eggs2")], cw=0.7, ch=0.24, fs=8.5, kinds={"spam": "teal"})
    tb(s, x + w * 0.74, y + 1.05, w * 0.26, 0.5, L[-1], 9.5, C["muted"], italic=True)


@need(1.35)
def v_sizes(s, x, y, w, h, ns, out):
    sz = dict(sorted(ns["sizes"].items()))
    chart(s, "bar", x, y, w * 0.5, h, list(sz)[::-1], [("bytes", list(sz.values())[::-1])], fs=9, legend=False, gap=50, axis_title="bytes of files directly in the folder")
    rows = [["Folder", "Files in it", "Bytes"]]
    for f, b in sz.items():
        rows.append([f, str(sorted(p.name for p in Path(f).iterdir() if p.is_file())), str(b)])
    rows.append(["total", "", str(sum(sz.values()))])
    table(s, x + w * 0.53, y + 0.05, w * 0.47, rows, [1.3, 2.0, 0.8], rowh=0.3, mono_cols=(0, 1, 2), fs=9.5, align_cols={2: PP_ALIGN.RIGHT})


@need(1.25)
def v_mkdir(s, x, y, w, h, ns, out):
    L = lines(out)
    chip(s, x, y, 2.4, 0.3, "Path('x/y').mkdir()", "plain", fs=10)
    arrow(s, x + 2.4, y + 0.15, x + 3.0, y + 0.15, C["coral"], 1.4)
    chip(s, x + 3.0, y, 3.4, 0.3, L[0], "red", fs=10, mono=False)
    chip(s, x, y + 0.45, 2.4, 0.3, "mkdir(parents=True)", "plain", fs=10)
    arrow(s, x + 2.4, y + 0.6, x + 3.0, y + 0.6, C["green"], 1.4)
    tree(s, x + 3.0, y + 0.45, {"x": (0, 0), "y": (1, 0)}, [("x", "y")], cw=0.9, ch=0.3, fs=10, kinds={"x": "green", "y": "green"})
    chip(s, x, y + 0.9, 6.4, 0.3, "the tree below x now: %s" % L[1], "teal", fs=10)


# ------------------------------------------------------------------ part 4
@need(1.35)
def v_zipwrite(s, x, y, w, h, ns, out):
    info = ns["info"]
    chart(s, "col", x, y, w * 0.45, h, ["original", "stored in the ZIP"], [("bytes", [info.file_size, info.compress_size])], fs=9, legend=False, gap=60, axis_title="bytes")
    rows = [["Value", "From getinfo"], ["info.filename", info.filename], ["info.file_size", str(info.file_size)], ["info.compress_size", str(info.compress_size)],
            ["compress_size / file_size", "%.3f" % (info.compress_size / info.file_size)]]
    table(s, x + w * 0.49, y + 0.02, w * 0.51, rows, [2.4, 1.8], rowh=0.27, mono_cols=(0, 1), fs=9.5)


@need(1.2)
def v_zipmodes(s, x, y, w, h, ns, out):
    L = lines(out)
    members = lit(L[0])
    rows = [["Mode", "What it does", "Seen in the run"], ["'w'", "start a new archive", "a.txt written"], ["'a'", "add to an existing archive", "namelist: %s" % members],
            ["'r' (default)", "read an archive", "namelist, getinfo, extract"], ["'x'", "create, never overwrite", "refused: x.zip exists"]]
    table(s, x, y, w * 0.72, rows, [1.2, 2.3, 3.5], rowh=0.25, mono_cols=(0,), fs=9, cell_color={(4, 2): C["coral"]})
    chart(s, "col", x + w * 0.76, y, w * 0.24, h, ["after w", "after a"], [("members", [1, len(members)])], fs=9, legend=False, gap=50, vmax=3, major=1)


@need(1.25)
def v_extract(s, x, y, w, h, ns, out):
    L = lines(out)
    got = lit(L[0])
    tree(s, x, y, {"z.zip": (0, 0), "a.txt": (1, 0), "sub/b.txt": (1, 1)}, [("z.zip", "a.txt"), ("z.zip", "sub/b.txt")], cw=1.0, ch=0.28, kinds={"z.zip": "amber"})
    chip(s, x, y + 0.95, 4.2, 0.28, "extract() gave " + L[1], "green", fs=9.5)
    rows = [["extractall('out') made", "kind"]] + [[g, "folder" if Path(g).is_dir() else "file"] for g in got]
    table(s, x + 4.6, y, w - 4.6, rows, [3.2, 1.2], rowh=0.3, mono_cols=(0,), fs=10)


@need(1.4)
def v_archives(s, x, y, w, h, ns, out):
    L = lines(out)
    names, un = lit(L[1]), lit(L[2])
    rows = [["Inside the ZIP", "After unpack_archive"]]
    for i in range(max(len(names), len(un))):
        rows.append([names[i] if i < len(names) else "", un[i] if i < len(un) else ""])
    table(s, x, y, 6.0, rows, [2.6, 3.4], rowh=0.27, mono_cols=(0, 1), fs=9.5)
    chip(s, x + 6.3, y, 1.1, 0.3, "spam/", "teal", fs=10)
    arrow(s, x + 6.85, y + 0.3, x + 6.85, y + 0.5, C["amber"], 1.6)
    chip(s, x + 6.3, y + 0.5, 1.1, 0.3, L[0], "amber", fs=10)
    arrow(s, x + 6.85, y + 0.8, x + 6.85, y + 1.0, C["amber"], 1.6)
    chip(s, x + 6.3, y + 1.0, 1.1, 0.3, "un/", "teal", fs=10)
    tb(s, x + 7.5, y + 0.1, 1.7, 0.45, "make_archive packs", 9.5, C["muted"], italic=True)
    tb(s, x + 7.5, y + 0.85, 1.7, 0.45, "unpack_archive unpacks", 9.5, C["muted"], italic=True)


# ------------------------------------------------------------------ part 5 (narrow: the result stands in the right column, 3.25 in wide)
@need(1.0)
def v_backup(s, x, y, w, h, ns, out):
    L = lines(out)
    z1, z2 = L[0].split()
    members = lit(L[1])
    tree(s, x, y, {"spam": (0, 0), "eggs": (1, 0), "file2.txt": (2, 0), "file1.txt": (1, 1)}, [("spam", "eggs"), ("eggs", "file2.txt"), ("spam", "file1.txt")], cw=0.8, ch=0.28, fs=8.5, kinds={"spam": "teal"})
    tb(s, x, y + 0.85, w, 0.26, "the folder to back up", 9, C["muted"], italic=True)
    chip(s, x, y + 1.25, 1.4, 0.3, z1, "amber", fs=10)
    chip(s, x + 1.7, y + 1.25, 1.4, 0.3, z2, "amber", fs=10)
    arrow(s, x + 1.4, y + 1.4, x + 1.7, y + 1.4, C["amber"], 1.4)
    tb(s, x, y + 1.6, w, 0.26, "first run, then second run", 9, C["muted"], italic=True)
    rows = [["Members of spam_1.zip"]] + [[m] for m in members]
    table(s, x, y + 2.05, w, rows, [1], rowh=0.3, mono_cols=(0,), fs=10)
    chart(s, "col", x, y + 3.05, w, h - 3.05, ["spam_1.zip", "spam_2.zip"], [("files stored", [len(members), len(members)])], fs=8, legend=False, gap=40, vmax=3, major=1)


@need(1.0)
def v_selective(s, x, y, w, h, ns, out):
    L = lines(out)
    dest, src = lit(L[0]), lit(L[1])
    pdf_src = [f for f in src if f.lower().endswith(".pdf")]
    chart(s, "col", x, y, w, 1.8, ["PDFs in src", "other in src", "copied"], [("files", [len(pdf_src), len(src) - len(pdf_src), len(dest)])], fs=9, legend=False, gap=50, vmax=4, major=1)
    rows = [["File", "In src", "Copied"]] + [[f, "yes", "yes" if f in dest else "no"] for f in src]
    table(s, x, y + 1.95, w, rows, [1.7, 0.7, 0.8], rowh=0.3, mono_cols=(0,), fs=10, cell_color={(i, 2): (C["green"] if f in dest else C["greyTxt"]) for i, f in enumerate(src, 1)})


@need(1.0)
def v_large(s, x, y, w, h, ns, out):
    found = ns["found"]
    order = sorted(found.items(), key=lambda kv: -kv[1])
    chart(s, "bar", x, y, w, 1.8, [k for k, _ in order][::-1], [("bytes", [v for _, v in order][::-1])], fs=9, legend=False, gap=50, axis_title="bytes (limit: more than 1000)")
    allf = sorted((str(Path(d, f)), os.path.getsize(Path(d, f))) for d, _, fs_ in os.walk(".") for f in fs_)
    rows = [["File", "Bytes", "Above 1000?"]] + [[n, str(b), str(n in found)] for n, b in allf]
    table(s, x, y + 1.95, w, rows, [1.4, 0.7, 1.1], rowh=0.3, mono_cols=(0, 1, 2), fs=9.5, align_cols={1: PP_ALIGN.RIGHT},
          cell_color={(i, 2): (C["green"] if n in found else C["greyTxt"]) for i, (n, b) in enumerate(allf, 1)})


@need(1.0)
def v_dates(s, x, y, w, h, ns, out):
    before = ns["before"]
    pattern = ns["pattern"]
    rows = [["Before", "After"]]
    cc = {}
    for i, b in enumerate(before, 1):
        a = pattern.sub(r"\2-\1-\3", b) if pattern.search(b) else b
        rows.append([b, a])
        cc[(i, 1)] = C["green"] if a != b else C["greyTxt"]
    table(s, x, y, w, rows, [1.6, 1.6], rowh=0.45, mono_cols=(0, 1), cell_color=cc, fs=9)
    chip(s, x, y + 2.2, w, 0.3, "01-02-2020 : month 01, day 02", "teal", fs=9.5)
    arrow(s, x + w / 2, y + 2.5, x + w / 2, y + 2.8, C["amber"], 1.6)
    chip(s, x, y + 2.8, w, 0.3, "02-01-2020 : day 02, month 01", "amber", fs=9.5)
    tb(s, x, y + 3.2, w, 0.3, "%d of %d files renamed" % (sum(1 for b in before if pattern.search(b)), len(before)), 9.5, C["muted"], italic=True)


VISUALS = {"copy": v_copy, "copytree": v_copytree, "copy2": v_copy2, "move": v_move, "unlink": v_unlink, "rmtree": v_rmtree, "dryrun": v_dryrun,
           "listing": v_listing, "walk": v_walk, "sizes": v_sizes, "mkdir": v_mkdir, "zipwrite": v_zipwrite, "zipmodes": v_zipmodes, "extract": v_extract,
           "archives": v_archives, "backup": v_backup, "selective": v_selective, "large": v_large, "dates": v_dates}
