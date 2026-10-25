"""Chapter 12 deck visuals, version 2.0.0: the executed result of every code example drawn as a native table, a native chart or a drawn
diagram. Every number, string and truth value shown is taken from the run of the example's own code (the namespace `ns` and the
printed text `out` that deck_build_v2_0_0.py passes in); nothing is typed in by hand except plain-language names of columns and boxes.
Each function: visual(s, x, y, w, h, ns, out). The attribute .need is the least height (inches) it wants."""
__version__ = "2.0.0"
import shlex
import unicodedata
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
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


def chips_row(s, x, y, items, cw, h=0.3, fs=9.5, kinds=None, gap=0.08, arrows=False):
    """a row of chips; returns the x after the last chip"""
    for i, t in enumerate(items):
        k = kinds[i] if kinds else "plain"
        chip(s, x, y, cw, h, short(t, int(cw * 13)), k, fs=fs)
        if arrows and i < len(items) - 1:
            arrow(s, x + cw + 0.005, y + h / 2, x + cw + gap - 0.005, y + h / 2, C["muted"], 1.0)
        x += cw + gap
    return x


# ------------------------------------------------------------------ part 1
@need(1.1)
def v_terminal_cd(s, x, y, w, h, ns, out):
    rows = [["Terminal", "Python call", "What it gave"],
            ["cd Desktop", "os.chdir('Desktop')", "moved down into the new folder"],
            ["pwd", "os.getcwd()", repr(ns["where"])],
            ["cd ..", "os.chdir('..')", "moved back up one folder"]]
    table(s, x, y, w * 0.62, rows, [1.2, 2.0, 2.6], rowh=min(0.32, h / len(rows)), mono_cols=(0, 1))
    px = x + w * 0.66
    tb(s, px, y - 0.02, w * 0.34, 0.22, "the walk, folder by folder", 9.5, C["muted"], italic=True)
    chip(s, px, y + 0.25, 0.85, 0.3, "start", "grey", fs=9.5)
    arrow(s, px + 0.87, y + 0.4, px + 1.07, y + 0.4, C["muted"], 1.2)
    chip(s, px + 1.09, y + 0.25, 0.85, 0.3, "lab", "plain", fs=9.5)
    arrow(s, px + 1.96, y + 0.4, px + 2.16, y + 0.4, C["muted"], 1.2)
    chip(s, px + 2.18, y + 0.25, 0.9, 0.3, ns["where"], "amber", fs=9.5)
    tb(s, px, y + 0.7, w * 0.34, 0.5, "pwd printed %r; the cleanup removed the lab." % ns["where"], 9.5, C["muted"], italic=True)


@need(1.1)
def v_terminal_ls(s, x, y, w, h, ns, out):
    rows = [["Terminal", "Python", "Names it showed"],
            ["ls", "os.listdir(lab)", ", ".join(ns["listing"])],
            ["dir *.exe", "names ending in .exe", ", ".join(ns["programs"])]]
    table(s, x, y, w * 0.68, rows, [1.1, 1.9, 3.2], rowh=min(0.34, h / 3), mono_cols=(0, 1, 2))
    tb(s, x + w * 0.71, y - 0.02, w * 0.29, 0.22, "names each command shows", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.71, y + 0.2, w * 0.29, max(h - 0.2, 1.1), ["ls", "dir *.exe"], [("names", [len(ns["listing"]), len(ns["programs"])])], fs=9, legend=False, gap=60, vmax=4, major=1)


@need(1.1)
def v_path_text(s, x, y, w, h, ns, out):
    folders = ns["folders"]
    front = ["/home/al/Scripts"] + folders[:2]
    for k, (lab, items, kinds) in enumerate([("PATH as it is", folders, ["amber" if f == "/usr/bin" else "plain" for f in folders]),
                                             ("with /home/al/Scripts put first", front, ["teal"] + ["plain"] * 2)]):
        yy = y + k * 0.65
        tb(s, x, yy, 5.5, 0.22, lab + "  (searched from the left)", 10, C["teal"], bold=True)
        cw = (w - 0.1 * 4) / 4.4
        chips_row(s, x, yy + 0.26, ["%d  %s" % (i + 1, f) for i, f in enumerate(items)], cw, 0.3, 9.5, kinds, 0.1, True)


@need(1.2)
def v_path_which(s, x, y, w, h, ns, out):
    tb(s, x, y, 6.0, 0.22, "shutil.which('spam', path='a:b') over the two lab folders", 10, C["teal"], bold=True)
    chip(s, x, y + 0.3, 2.5, 0.32, "a  holds spam  (first)", "green", fs=10)
    arrow(s, x + 2.55, y + 0.46, x + 2.95, y + 0.46, C["green"], 1.5)
    chip(s, x + 3.0, y + 0.3, 2.6, 0.32, "found: %s" % ns["where"], "green", fs=10)
    chip(s, x, y + 0.72, 2.5, 0.32, "b  holds spam  (never reached)", "grey", fs=10)
    chip(s, x + 5.9, y + 0.3, 3.2, 0.32, "which('eggs') -> %s" % out.splitlines()[-1].split(": ")[1], "red", fs=10)
    tb(s, x + 5.9, y + 0.72, 3.2, 0.5, "None means: no folder of the path holds it", 9.5, C["muted"], italic=True)


# ------------------------------------------------------------------ part 2
@need(1.2)
def v_venv_cfg(s, x, y, w, h, ns, out):
    rows = [["pyvenv.cfg setting", "value"]] + [[k, v] for k, v in ns["settings"].items()]
    table(s, x, y, w * 0.55, rows, [2.7, 1.1], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1))
    bx = x + w * 0.6
    label_shape(s, bx, y, w * 0.4, 0.36, ".venv  (a folder)", C["tealLight"], C["ink"], size=10.5, line=C["line"], radius=0.1)
    for i, t in enumerate(["bin/  (activate, python, pip)", "pyvenv.cfg  (the settings)", "lib/  (the packages)"]):
        chip(s, bx + 0.25, y + 0.45 + i * 0.34, w * 0.4 - 0.25, 0.28, t, "plain", fs=9.5, mono=False)
        line_seg(s, bx + 0.1, y + 0.36, bx + 0.1, y + 0.59 + i * 0.34, C["line"], 1.0)
        arrow(s, bx + 0.1, y + 0.59 + i * 0.34, bx + 0.24, y + 0.59 + i * 0.34, C["muted"], 1.0)


@need(1.2)
def v_venv_activate(s, x, y, w, h, ns, out):
    before = ns["PATH"].split(":")
    after = [ns["bin_dir"]] + before
    for k, (lab, folders) in enumerate([("PATH before activate", before), ("PATH after activate", after)]):
        yy = y + k * 0.62
        tb(s, x, yy, 4, 0.22, lab, 10, C["teal"], bold=True)
        cw = (w * 0.7 - 0.08 * 4) / 4
        chips_row(s, x, yy + 0.25, [f.replace("/home/al/Scripts/", "") for f in folders], cw, 0.3, 9, ["teal" if (k and i == 0) else "plain" for i in range(len(folders))], 0.08, True)
    chip(s, x + w * 0.74, y + 0.25, w * 0.26, 0.5, "inside a venv: %s" % (ns["sys"].prefix != ns["sys"].base_prefix), "grey", fs=10)
    arrow(s, x + w * 0.72, y + 0.4, x + w * 0.72, y + 0.8, C["teal"], 1.4)


@need(1.2)
def v_pip(s, x, y, w, h, ns, out):
    name, sep, version = ns["name"], ns["sep"], ns["version"]
    tb(s, x, y - 0.02, 4.5, 0.22, "requirement.partition('==')", 10, C["teal"], bold=True, font=MONO)
    chip(s, x, y + 0.25, 2.2, 0.32, repr(name), "teal", fs=10.5)
    chip(s, x + 2.3, y + 0.25, 0.8, 0.32, repr(sep), "grey", fs=10.5)
    chip(s, x + 3.2, y + 0.25, 1.3, 0.32, repr(version), "amber", fs=10.5)
    for cx, lab in ((x + 1.1, "package name"), (x + 2.7, "separator"), (x + 3.85, "version")):
        arrow(s, cx, y + 0.8, cx, y + 0.59, C["muted"], 1.0)
        tb(s, cx - 0.7, y + 0.8, 1.4, 0.22, lab, 9, C["muted"], align=PP_ALIGN.CENTER)
    rows = [["Command in the terminal", "Does"],
            ["python -m pip install %s" % name, "newest"],
            ["python -m pip install %s==%s" % (name, version), "this version"],
            ["python -m pip list", "lists all"],
            ["python -m pip uninstall %s" % name, "removes"]]
    table(s, x + 4.6, y, w - 4.6, rows, [3.5, 1.0], rowh=min(0.27, h / len(rows)), mono_cols=(0,), fs=8.5)


# ------------------------------------------------------------------ part 3
@need(1.1)
def v_selfaware(s, x, y, w, h, ns, out):
    sy = ns["sys"]
    rows = [["The program asks", "Python expression", "Answer", "It can then"],
            ["Which kind of system?", "os.name", repr(ns["os"].name), "run " + ns["KINDS"][ns["os"].name] + " code"],
            ["A new enough Python?", "sys.version_info >= (3, 9)", str(sy.version_info >= (3, 9)), "refuse an old Python"],
            ["How detailed is the version?", "len(sys.version_info)", str(len(sy.version_info)), "compare it like a tuple"],
            ["Started from a file?", "'__file__' in globals()", str("__file__" in ns), "find files beside itself"]]
    cc = {(i, 2): (C["green"] if rows[i][2] == "True" else C["ink"]) for i in range(1, 5)}
    table(s, x, y, w, rows, [2.3, 2.6, 1.2, 2.6], rowh=min(0.3, h / len(rows)), mono_cols=(1, 2), cell_color=cc, fs=10)


@need(1.1)
def v_missingmod(s, x, y, w, h, ns, out):
    lines = out.splitlines()
    mod = lines[0].split("called ")[1]
    msg = lines[1].split(": ", 1)[1]
    bw = (w - 3 * 0.35) / 4
    boxes = [("import %s" % mod, "plain"), ("ModuleNotFoundError\nname = %r" % mod, "red"), ("sys.exit(message)", "amber"), ("SystemExit\ncode = %r" % short(msg, 24), "teal")]
    for i, (t, k) in enumerate(boxes):
        xx = x + i * (bw + 0.35)
        label_shape(s, xx, y + 0.05, bw, 0.62, t, {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"]}[k], C["ink"], size=9.5, line=C["line"], radius=0.12)
        if i < 3:
            arrow(s, xx + bw + 0.02, y + 0.36, xx + bw + 0.33, y + 0.36, C["muted"], 1.5)
    tb(s, x, y + 0.78, w, 0.4, "A real run prints the message to standard error and ends the program with exit code 1.", 10.5, C["muted"], italic=True)


@need(1.1)
def v_argv(s, x, y, w, h, ns, out):
    rows = [["Typed in the terminal", "sys.argv inside the script", "Items"]]
    counts = []
    for line in ns["typed"]:
        argv = shlex.split(line)[1:]
        rows.append([line, str(argv), str(len(argv))])
        counts.append(len(argv))
    table(s, x, y, w * 0.74, rows, [2.7, 2.9, 0.6], rowh=min(0.34, h / len(rows)), mono_cols=(0, 1, 2), fs=9)
    chart(s, "col", x + w * 0.77, y, w * 0.23, h, ["hello world", "quoted", "none"], [("items", counts)], fs=8, legend=False, gap=50, vmax=4, major=1)


@need(1.1)
def v_argparse_a(s, x, y, w, h, ns, out):
    p = ns["p"]
    rows = [["Words typed after snowstorm", "density", "verbose"]]
    dens = []
    for argv in ([], ["20", "-v"]):
        a = p.parse_args(argv)
        rows.append([" ".join(argv) or "(nothing)", str(a.density), str(a.verbose)])
        dens.append(a.density)
    table(s, x, y, w * 0.6, rows, [2.4, 1.0, 1.0], rowh=min(0.34, h / 3), mono_cols=(0, 1, 2))
    tb(s, x + w * 0.64, y - 0.02, w * 0.36, 0.22, "density the program receives", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.64, y + 0.2, w * 0.36, max(h - 0.2, 1.1), ["default", "20 -v"], [("density", dens)], fs=9, legend=False, gap=60, vmax=25, major=5)


@need(1.1)
def v_argparse_b(s, x, y, w, h, ns, out):
    msg = out.splitlines()[0].split("refused, ")[1]
    bw = (w - 3 * 0.35) / 4
    boxes = [("snowstorm lots", "plain"), ("type=int:\nint('lots') fails", "red"), ("ArgumentError", "amber"), (short(msg, 42), "teal")]
    for i, (t, k) in enumerate(boxes):
        xx = x + i * (bw + 0.35)
        label_shape(s, xx, y + 0.05, bw, 0.62, t, {"plain": C["card"], "red": C["redLight"], "amber": C["amberLight"], "teal": C["tealLight"]}[k], C["ink"], size=9.5, line=C["line"], radius=0.12)
        if i < 3:
            arrow(s, xx + bw + 0.02, y + 0.36, xx + bw + 0.33, y + 0.36, C["muted"], 1.5)
    tb(s, x, y + 0.78, w, 0.4, "argparse writes the usage message and, in a terminal, the program stops with exit code 2.", 10.5, C["muted"], italic=True)


# ------------------------------------------------------------------ part 4
@need(1.1)
def v_quiet(s, x, y, w, h, ns, out):
    p, report = ns["p"], ns["report"]
    modes = [("default", []), ("-v", ["-v"]), ("-q", ["-q"])]
    counts = [len(report(p.parse_args(a))) for _, a in modes]
    rows = [["Switch", "Lines", "What the user sees"]]
    for (lab, a), n in zip(modes, counts):
        rows.append([lab, str(n), short(" / ".join(report(p.parse_args(a))) or "nothing", 50)])
    table(s, x, y, w * 0.66, rows, [0.9, 0.8, 3.9], rowh=min(0.32, h / 4), mono_cols=(0, 1), fs=9.5)
    tb(s, x + w * 0.69, y - 0.02, w * 0.31, 0.22, "lines printed per switch", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.69, y + 0.2, w * 0.31, max(h - 0.2, 1.1), [m for m, _ in modes], [("lines", counts)], fs=9, legend=False, gap=50, vmax=4, major=1)


@need(1.1)
def v_chr(s, x, y, w, h, ns, out):
    rows = [["Constant", "chr(...)", "Character", "ord(...)", "Unicode name"]]
    for nm in ("TOP", "BOTTOM", "FULL"):
        ch = ns[nm]
        rows.append([nm, "chr(%d)" % ord(ch), ch * 3, str(ord(ch)), unicodedata.name(ch).lower()])
    table(s, x, y, w * 0.72, rows, [1.0, 1.2, 1.0, 0.9, 2.7], rowh=min(0.32, h / 4), mono_cols=(0, 1, 2, 3), fs=10)
    chip(s, x + w * 0.75, y, w * 0.25, 0.34, "os.system(%r)" % ns["clear_command"], "amber", fs=10)
    tb(s, x + w * 0.75, y + 0.4, w * 0.25, 0.5, "the text handed to the shell on this system", 9, C["muted"], italic=True)


SWATCH = {"black": "1F2933", "red": "D9534F", "green": "48A868", "yellow": "E8C547", "blue": "4A7CC0", "purple": "9B6BC8", "cyan": "3FB6C4", "white": "F4F1EA"}


@need(1.1)
def v_colour(s, x, y, w, h, ns, out):
    cols = ns["COLORS"]
    for k in range(2):
        part = cols[k * 4:(k + 1) * 4]
        rows = [["Name", "fg", "bg", "Looks like"]]
        cf = {}
        for i, c in enumerate(part, 1):
            rows.append([c, repr(ns["fg"](c)), repr(ns["bg"](c)), ""])
            cf[(i, 3)] = SWATCH[c]
        table(s, x + k * (w / 2 + 0.05), y, w / 2 - 0.05, rows, [0.9, 1.0, 1.0, 0.8], rowh=min(0.26, h / 5), mono_cols=(0, 1, 2), cell_fill=cf, fs=9)


@need(1.1)
def v_snowstorm(s, x, y, w, h, ns, out):
    rows = ns["rows"]
    fl = [len(r) - r.count(" ") for r in rows]
    d = ns["DENSITY"]
    tb(s, x, y - 0.02, w * 0.6, 0.22, "snowflakes in each of the 5 rows (40 cells)", 9.5, C["muted"], italic=True)
    chart(s, "col", x, y + 0.2, w * 0.6, max(h - 0.2, 1.1), ["row %d" % (i + 1) for i in range(len(fl))], [("flakes", fl)], fs=9, legend=False, gap=50, vmax=16, major=4)
    chip(s, x + w * 0.64, y + 0.1, w * 0.36, 0.3, "density %d percent" % d, "teal", fs=10)
    chip(s, x + w * 0.64, y + 0.5, w * 0.36, 0.3, "expected %.0f of 40 per row" % (40 * d / 100.0), "plain", fs=10)
    chip(s, x + w * 0.64, y + 0.9, w * 0.36, 0.3, "drawn: %d in 200 cells" % sum(fl), "amber", fs=10)


# ------------------------------------------------------------------ part 5
@need(1.1)
def v_launcher_text(s, x, y, w, h, ns, out):
    lines = ns["launcher"].splitlines()
    roles = ["names the interpreter", "enters the environment", "runs the script, forwards the arguments"]
    for i, (ln, r) in enumerate(zip(lines, roles)):
        yy = y + i * 0.4
        label_shape(s, x, yy, 0.4, 0.32, str(i + 1), C["teal"], "FFFFFF", size=11, bold=True)
        chip(s, x + 0.5, yy, 4.7, 0.32, ln, "plain", fs=9.5)
        arrow(s, x + 5.25, yy + 0.16, x + 5.65, yy + 0.16, C["muted"], 1.2)
        tb(s, x + 5.7, yy, 3.4, 0.32, r, 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE)


@need(1.1)
def v_launcher_chmod(s, x, y, w, h, ns, out):
    for k, (lab, mode) in enumerate([("before chmod u+x", ns["before"]), ("after chmod u+x", ns["after"])]):
        yy = y + k * 0.6
        tb(s, x, yy + 0.02, 1.9, 0.3, lab, 10, C["teal"], bold=True, anchor=MSO_ANCHOR.MIDDLE)
        for i, ch in enumerate(mode):
            kind = "amber" if (i == 3 and k == 1) else ("plain" if ch != "-" else "grey")
            chip(s, x + 2.0 + i * 0.4, yy, 0.36, 0.34, ch, kind, fs=11)
    arrow(s, x + 1.0, y + 0.34, x + 1.0, y + 0.6, C["teal"], 1.4)
    for lab, i0, n in (("type", 0, 1), ("owner", 1, 3), ("group", 4, 3), ("other", 7, 3)):
        tb(s, x + 2.0 + i0 * 0.4, y + 1.0, n * 0.4 - 0.04, 0.2, lab, 8.5, C["muted"], italic=True, align=PP_ALIGN.CENTER, margin=(0, 0))
    chip(s, x + 6.3, y + 0.3, 2.8, 0.34, "found by name on PATH: %s" % ns["on_path"], "green", fs=10)


@need(1.0)
def v_desktop(s, x, y, w, h, ns, out):
    ent = ns["c"]["Desktop Entry"]
    rows = [["Key", "Value", "Meaning"],
            ["Name", ent["name"], "the label in the menu"],
            ["Exec", ent["exec"], "what a click runs, in a terminal window"],
            ["Type", ent["type"], "an entry that starts a program"]]
    table(s, x, y, w, rows, [0.9, 4.6, 3.2], rowh=min(0.34, h / 4), mono_cols=(0, 1), fs=10)


@need(1.1)
def v_ccwd(s, x, y, w, h, ns, out):
    terminal, last = ns["terminal"], ns["clipboard"][-1]
    bw = 2.5
    label_shape(s, x, y + 0.05, bw, 0.7, "terminal\nworking directory %s" % terminal, C["card"], C["ink"], size=10, line=C["line"], radius=0.1)
    label_shape(s, x + 3.3, y + 0.05, bw, 0.7, "ccwd .. (a running program)\nworking directory %s" % last, C["tealLight"], C["ink"], size=10, line=C["line"], radius=0.1)
    label_shape(s, x + 6.6, y + 0.05, 2.5, 0.7, "clipboard\n%s" % last, C["amberLight"], C["ink"], size=10, line=C["line"], radius=0.1)
    arrow(s, x + bw + 0.02, y + 0.4, x + 3.28, y + 0.4, C["muted"], 1.5)
    tb(s, x + bw + 0.05, y + 0.1, 0.8, 0.26, "starts", 9.5, C["muted"], italic=True)
    arrow(s, x + 3.3 + bw + 0.02, y + 0.4, x + 6.58, y + 0.4, C["muted"], 1.5)
    tb(s, x + 3.3 + bw + 0.05, y + 0.1, 0.8, 0.26, "copies", 9.5, C["muted"], italic=True)
    tb(s, x, y + 0.9, w, 0.3, "After the program has changed folder, the terminal has not: it still stands in %s." % terminal, 10.5, C["ink"])


@need(1.3)
def v_cliprec(s, x, y, w, h, ns, out):
    texts = ns["texts"]
    prev, rows = "", [["Read", "Clipboard holds", "New?"]]
    cc = {}
    for i, t in enumerate(texts, 1):
        new = t != prev
        rows.append([str(i), t, "yes: printed" if new else "no: skipped"])
        cc[(i, 2)] = C["green"] if new else C["greyTxt"]
        prev = t
    table(s, x, y, w * 0.62, rows, [0.6, 1.6, 1.4], rowh=min(0.24, h / len(rows)), mono_cols=(0, 1), cell_color=cc, fs=9)
    tb(s, x + w * 0.66, y - 0.02, w * 0.34, 0.22, "reads against texts recorded", 9.5, C["muted"], italic=True)
    chart(s, "col", x + w * 0.66, y + 0.2, w * 0.34, max(h - 0.2, 1.1), ["reads", "recorded"], [("count", [len(texts), len(ns["recorded"])])], fs=9, legend=False, gap=60, vmax=6, major=1)


@need(1.2)
def v_pyinstaller(s, x, y, w, h, ns, out):
    words = ns["words"]
    roles = ["starts the interpreter", "run a module", "the module to run", "bundle into one file", "the script to pack"]
    cw = (w - 4 * 0.1) / 5
    for i, (wd, r) in enumerate(zip(words, roles)):
        xx = x + i * (cw + 0.1)
        chip(s, xx, y, cw, 0.32, wd, "teal" if i in (2, 3) else "plain", fs=10)
        arrow(s, xx + cw / 2, y + 0.66, xx + cw / 2, y + 0.35, C["muted"], 1.0)
        tb(s, xx, y + 0.67, cw, 0.3, r, 9.5, C["muted"], align=PP_ALIGN.CENTER)
    tb(s, x, y + 1.05, 1.6, 0.26, "the build leaves", 10, C["teal"], bold=True)
    chips_row(s, x + 1.6, y + 1.03, ns["left"], 1.5, 0.28, 9.5, ["amber"] * 3, 0.1)


@need(1.1)
def v_deployable(s, x, y, w, h, ns, out):
    rows = [["Project", "From chapter", "Third line of its launcher"]]
    for name, chap in ns["projects"].items():
        rows.append([name, str(chap), ns["LINE"].format(name=name)])
    table(s, x, y, w, rows, [1.8, 1.2, 5.2], rowh=min(0.3, h / len(rows)), mono_cols=(0, 2), fs=10)


VISUALS = {"terminal_cd": v_terminal_cd, "terminal_ls": v_terminal_ls, "path_text": v_path_text, "path_which": v_path_which, "venv_cfg": v_venv_cfg,
           "venv_activate": v_venv_activate, "pip": v_pip, "selfaware": v_selfaware, "missingmod": v_missingmod, "argv": v_argv, "argparse_a": v_argparse_a,
           "argparse_b": v_argparse_b, "quiet": v_quiet, "chr": v_chr, "colour": v_colour, "snowstorm": v_snowstorm, "launcher_text": v_launcher_text,
           "launcher_chmod": v_launcher_chmod, "desktop": v_desktop, "ccwd": v_ccwd, "cliprec": v_cliprec, "pyinstaller": v_pyinstaller, "deployable": v_deployable}
