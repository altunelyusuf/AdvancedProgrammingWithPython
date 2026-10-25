#!/usr/bin/env python3
"""Builds the chapter 12 lecture deck 2.0.0 (Command Line Programs) on the deck standard, and its chapter-code manifest.

A NEW tool (the deck of 1.0.0 and its builder stay untouched, in this folder). Every code example of examples_v2_0_0.py is RUN here; the
printed result and every number in a result visual come from that run. One light background scheme, a number on every slide, a chip '>>>'
on every slide that is not a divider, native tables and charts, drawn diagrams with arrows, story pictures embedded with their licences.
Writes: 03-materials/ch12/SEN0414_Ch12_CommandLinePrograms_3e_v2_0_0.pptx
        03-materials/ch12/page/chapter_code_ch12_v1_0_0.json   (order = slide order; the code exactly as the code boxes show it)
Usage:  python3 deck_build_v2_0_0.py
"""
__version__ = "2.0.0"
import contextlib
import glob
import io
import json
import math
import os
import platform
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
import importlib.util


def load(name, fn):
    sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, fn))
    m = importlib.util.module_from_spec(sp)
    sys.modules[name] = m
    sp.loader.exec_module(m)
    return m


from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches
import deck_kit_v2_0_0 as K
from deck_kit_v2_0_0 import C, MONO, arrow, chart, code_box, label_shape, new_deck, new_slide, notes, picture, rect, table, tb
X = load("examples_v2_0_0", "examples_v2_0_0.py")
V = load("deck_visuals_v2_0_0", "deck_visuals_v2_0_0.py")
T = load("deck_content_v2_0_0", "deck_content_v2_0_0.py")

OUT_DECK = os.path.join(ROOT, "03-materials", "ch12", "SEN0414_Ch12_CommandLinePrograms_3e_v2_0_0.pptx")
OUT_MAN = os.path.join(ROOT, "03-materials", "ch12", "page", "chapter_code_ch12_v1_0_0.json")
ASSETS = os.path.join(ROOT, "03-materials", "ch12", "assets")
PYV = platform.python_version()
IMG = json.load(open(os.path.join(ASSETS, "story_images_v2_0_0.json"), encoding="utf-8"))
SUBJECT = {"pipes": "Douglas McIlroy", "norton": "Midnight Commander, screenshot", "pip": "pip in a terminal, screenshot", "shebang": "Dennis Ritchie, 2011"}


def research_labels():
    f = sorted(glob.glob(os.path.join(ROOT, "03-materials", "ch12", "rdodi", "sen0414_ch12_research_v*.ttl")), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    return re.findall(r"a sen0414:PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", open(f, encoding="utf-8").read())


RESEARCH = research_labels()


# ------------------------------------------------------------------ run every example
def run_example(ex):
    code = X.code_text(ex)
    buf = io.StringIO()
    ns = {"__name__": "__main__"}
    cwd = os.getcwd()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<%s>" % ex["id"], "exec"), ns)
    assert os.getcwd() == cwd, "example %s left the current folder" % ex["id"]
    return buf.getvalue(), ns


RUN = {ex["id"]: run_example(ex) for ex in X.EXAMPLES}

# ------------------------------------------------------------------ the plan: slide kinds in order
PARTS = {
    1: ("Part 1: Starting a program", "From a typed word to a running program: names, the terminal and PATH", [
        ("Program names", "Script, command and app name nearly the same thing."),
        ("Terminal", "A text window where you type short commands."),
        ("cd, pwd, ls", "Move, show the place, and list what is there."),
        ("PATH", "The list of folders searched, in order, for a program."),
    ]),
    2: ("Part 2: Isolating a program", "A virtual environment keeps one project's packages apart; pip fills it", [
        ("Virtual environment", "A folder that keeps one project's packages apart."),
        ("activate", "Puts the environment's folder first on PATH."),
        ("pip", "Installs packages into exactly the Python you name."),
        ("Version pin", "Two equals signs fix the version that is installed."),
    ]),
    3: ("Part 3: Programs that look around", "A program asks about its system and reads the words it was given", [
        ("os.name", "Tells which family of operating system runs the program."),
        ("sys.version_info", "Lets the program refuse a Python that is too old."),
        ("sys.argv", "The words typed after the name of the program."),
        ("argparse", "Declares the arguments once and checks them."),
    ]),
    4: ("Part 4: Designing the terminal output", "Quiet by default, characters for pictures, escape codes for colour", [
        ("Quiet default", "Print little, so that another program can read it."),
        ("chr and ord", "Convert between numbers and characters."),
        ("Escape codes", "Numbered signals that colour the text."),
        ("Snowstorm", "A flip-book animation drawn with block characters."),
    ]),
    5: ("Part 5: Deploying a program", "A launcher in a PATH folder, two small system programs, and a bundle", [
        ("Launcher", "A script in a PATH folder that starts the program."),
        ("chmod u+x", "Gives the owner the right to run the file."),
        ("ccwd, recorder", "Two small programs that touch the system."),
        ("PyInstaller", "Packs the interpreter and the script into one file."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("vocab",), ("code", "terminal_cd"), ("code", "terminal_ls"), ("code", "path_text"), ("code", "path_which"),
        ("divider", 2), ("analogy", "A2"), ("code", "venv_cfg"), ("code", "venv_activate"), ("code", "pip"), ("story", "pip"),
        ("divider", 3), ("analogy", "A3"), ("code", "selfaware"), ("code", "missingmod"), ("code", "argv"), ("code", "argparse_a"), ("code", "argparse_b"),
        ("divider", 4), ("analogy", "A4"), ("code", "quiet"), ("story", "pipes"), ("story", "norton"), ("code", "chr"), ("code", "colour"), ("tools",), ("code", "snowstorm"),
        ("divider", 5), ("analogy", "A5"), ("launchers",), ("code", "launcher_text"), ("code", "launcher_chmod"), ("story", "shebang"), ("code", "desktop"), ("code", "ccwd"), ("code", "cliprec"),
        ("code", "pyinstaller"), ("pyinfo",), ("code", "deployable"),
        ("current",), ("summary",), ("practice",), ("resources",)]
N = len(PLAN)
SLIDE_OF = {p: i for i, p in enumerate(PLAN, 1)}
CODE_ORDER = [p[1] for p in PLAN if p[0] == "code"]
assert CODE_ORDER == [e["id"] for e in X.EXAMPLES], "the examples file must list the examples in slide order"
STORY_COUNT = sum(1 for p in PLAN if p[0] == "story")


def part_slides(k):
    a = SLIDE_OF[("divider", k)]
    b = SLIDE_OF[("divider", k + 1)] - 1 if k < 5 else SLIDE_OF[("current",)] - 1
    return a, b


# ------------------------------------------------------------------ slide frames
def base(prs, title, sub=None, chip=True, nt=None):
    s = new_slide(prs)
    if chip:
        label_shape(s, 0.4, 0.28, 0.6, 0.36, ">>>", C["teal"], "FFFFFF", size=13, bold=True, font=MONO, radius=0.2, name="chip")
    tb(s, 1.15 if chip else 0.5, 0.18, 8.4 if chip else 9.0, 0.55, title, 22, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="title")
    if sub:
        tb(s, 1.15 if chip else 0.5, 0.72, 8.4, 0.3, sub, 12, C["muted"], name="subtitle")
    if nt:
        notes(s, nt)
    return s


def takeaway(s, text):
    rect(s, 0.4, 5.22, 0.07, 0.3, C["teal"], name="accent")
    tb(s, 0.55, 5.18, 7.9, 0.36, text, 12, C["muted"], italic=True, anchor=MSO_ANCHOR.MIDDLE, name="takeaway")


def add_numbers(prs):
    n = len(prs.slides)
    for i, s in enumerate(prs.slides, 1):
        tb(s, 8.6, 5.2, 1.0, 0.32, "%d / %d" % (i, n), 11, C["muted"], align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE, name="slide number")


def analogy_box(s, y, text, h=0.55, size=13):
    rect(s, 0.4, y, 9.2, h, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, y + 0.01, 8.9, h - 0.02, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), (text, {})]], size, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")


# ------------------------------------------------------------------ slide makers
def make_title(prs):
    s = base(prs, "Command Line Programs", None, chip=True, nt=T.NOTES["title"])
    s.shapes[-1].left, s.shapes[-1].top, s.shapes[-1].width, s.shapes[-1].height = Inches(0.6), Inches(1.7), Inches(8.8), Inches(0.9)
    for r in s.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.size = K.Pt(38)
    tb(s, 0.6, 2.65, 8.8, 0.7, "Chapter 12 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course", 16, C["muted"], name="subtitle")
    for i, (a, b) in enumerate([(str(len(X.EXAMPLES)), "code examples that run on the chapter page"), (str(STORY_COUNT), "true stories with who, what, when, where, why and how"),
                                (str(len(RESEARCH)), "distinct chapter concepts, each with an everyday picture")]):
        xx = 0.6 + i * 3.0
        rect(s, xx, 3.5, 2.8, 1.15, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, xx + 0.1, 3.55, 2.6, 0.5, a, 28, C["teal"], bold=True, name="stat")
        tb(s, xx + 0.1, 4.05, 2.6, 0.55, b, 11.5, C["ink"], name="stat label")
    tb(s, 0.6, 4.85, 8.0, 0.3, "SEN0414 Advanced Programming, Fall 2026. Yusuf Altunel, İstanbul Kültür Üniversitesi", 11, C["muted"], name="author")
    return s


def make_route(prs):
    s = base(prs, "Today's route", "Five parts; every range is a run of slides you can jump to", nt=T.NOTES["route"])
    rows = [["Part", "Slides", "Code examples", "You will run"]]
    runs = {1: "cd, pwd, ls as os calls; PATH and which", 2: "pyvenv.cfg, activate, pip pins", 3: "os.name, version, sys.argv, argparse",
            4: "quiet mode, chr, escape codes, snowstorm", 5: "launcher, ccwd, recorder, PyInstaller"}
    for k in range(1, 6):
        a, b = part_slides(k)
        nex = sum(1 for p in PLAN[a - 1:b] if p[0] == "code")
        rows.append([PARTS[k][0].split(": ", 1)[1], "%d - %d" % (a, b), str(nex), runs[k]])
    rows.append(["Changes, summary, practice, resources", "%d - %d" % (SLIDE_OF[("current",)], N), "-", "what current Python adds"])
    table(s, 0.5, 1.2, 9.0, rows, [3.0, 1.1, 1.3, 3.8], fs=13.5, rowh=0.55, bold_cols=(0,))
    takeaway(s, "Open the chapter-code tab of the page: the same %d examples, in this order." % len(X.EXAMPLES))
    return s


def make_questions(prs):
    s = base(prs, "Two questions this chapter answers", "Carry them through every part; the answers come back at the end", nt=T.NOTES["questions"])
    q = [("1", "How does a typed command become a running program, and how does the program learn what it was given?",
          "Answer on slides %d to %d: PATH, the launcher, sys.argv and argparse." % (SLIDE_OF[("code", "path_text")], SLIDE_OF[("code", "argparse_b")])),
         ("2", "Which printed outputs and launchers of the book differ in current Python or on a current system?",
          "Answer on slide %d: the changes, from the chapter research." % SLIDE_OF[("current",)])]
    for i, (n, qq, aa) in enumerate(q):
        yy = 1.3 + i * 1.75
        rect(s, 0.5, yy, 9.0, 1.55, C["card"], line=C["line"], radius=0.05, name="card")
        label_shape(s, 0.7, yy + 0.2, 0.5, 0.5, n, C["teal"], "FFFFFF", size=18, bold=True)
        tb(s, 1.4, yy + 0.12, 7.9, 0.75, qq, 16, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="question")
        tb(s, 1.4, yy + 0.95, 7.9, 0.45, aa, 12.5, C["teal"], anchor=MSO_ANCHOR.MIDDLE, name="answer")
    takeaway(s, "The terminal searches PATH; the program reads its arguments.")
    return s


def make_divider(prs, k):
    title, sub, concepts = PARTS[k]
    s = new_slide(prs)
    notes(s, T.NOTES["divider%d" % k])
    tb(s, 0.5, 0.2, 9.0, 0.7, title, 30, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="title")
    tb(s, 0.5, 0.92, 9.0, 0.34, sub, 14, C["muted"], name="subtitle")
    rect(s, 0.5, 1.33, 1.2, 0.05, C["teal"], name="rule")
    yy = 1.55
    for name, mean in concepts:
        label_shape(s, 0.5, yy, 2.2, 0.5, name, C["tealLight"], C["ink"], size=14, bold=True, radius=0.3)
        tb(s, 2.85, yy, 2.8, 0.6, mean, 12.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="meaning")
        yy += 0.72
    a, b = part_slides(k)
    items = []
    for i in range(a + 1, b + 1):
        p = PLAN[i - 1]
        if p[0] == "code":
            items.append((i, X.BY_ID[p[1]]["title"]))
        elif p[0] == "story":
            items.append((i, T.STORIES[p[1]]["title"]))
        elif p[0] == "analogy":
            items.append((i, [a_[1] for a_ in T.ANALOGIES if a_[0] == p[1]][0]))
        elif p[0] == "vocab":
            items.append((i, "A program by any other name"))
        elif p[0] == "tools":
            items.append((i, "Pop-ups, sound and colour: helpers"))
        elif p[0] == "launchers":
            items.append((i, "Launcher files on three systems"))
        elif p[0] == "pyinfo":
            items.append((i, "PyInstaller: what the file costs"))
    rows = [["Slide", "In this part"]] + [[str(i), t if len(t) < 41 else t[:38] + "..."] for i, t in items]
    rh = min(0.4, 3.5 / len(rows))
    table(s, 5.8, 1.55, 3.8, rows, [0.65, 3.8], fs=10.5, rowh=rh, name="table")
    return s


def make_analogy(prs, aid):
    _, title, head, rows = [a for a in T.ANALOGIES if a[0] == aid][0]
    s = base(prs, title, None, nt=T.NOTES[aid])
    analogy_box(s, 0.82, head, 0.62, 14)
    rh = min(0.5, 3.3 / (len(rows) + 1))
    table(s, 0.4, 1.55, 9.2, [["Chapter concept", "Everyday picture"]] + [[a, b] for a, b in rows], [3.6, 5.6], fs=11 if len(rows) > 7 else None, rowh=rh, bold_cols=(0,))
    return s


def framed(path, w, h):
    """Return a picture file of the frame's proportions: a wide or tall picture is centred, undistorted, on a white card so it fills the frame."""
    import tempfile
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    k = max(im.width / w, im.height / h)
    cw, ch = int(round(w * k)), int(round(h * k))
    bg = Image.new("RGBA", (cw, ch), (255, 255, 255, 255))
    bg.alpha_composite(im, ((cw - im.width) // 2, (ch - im.height) // 2))
    fd, out = tempfile.mkstemp(suffix=".png", prefix="ch12_story_")
    os.close(fd)
    bg.convert("RGB").save(out)
    return out


def make_story(prs, sid):
    st = T.STORIES[sid]
    rec = IMG[st["img"]]
    credit = "%s. Image: %s, %s, Wikimedia Commons." % (SUBJECT[sid], rec["Artist"] or "see file page", rec["LicenseShortName"])
    s = base(prs, st["title"], None, nt=T.STORY_NOTES[sid])
    picture(s, framed(os.path.join(ASSETS, st["img"]), 2.9, 3.2), 0.4, 0.95, 2.9, 3.2, "Picture for the story: " + st["title"].replace("Story: ", ""), "photo " + sid)
    tb(s, 0.4, 4.2, 2.9, 0.7, credit, 9.5, C["muted"], name="credit")
    yy = 0.92
    for lab in ("who", "what", "when", "where", "why", "how"):
        txt = st[lab]
        nlines = math.ceil((len(txt) + 7) / 64.0)
        h = max(0.44, nlines * 0.235 + 0.14)
        rect(s, 3.5, yy, 6.1, h, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, 3.55, yy, 6.0, h, [[(lab.upper() + "  ", {"bold": True, "color": C["teal"]}), (txt, {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name=lab)
        yy += h + 0.07
    tb(s, 3.5, yy + 0.02, 6.1, 0.36, [[("READ  ", {"bold": True, "color": C["amber"]}), (st["linktext"], {"link": st["link"], "color": C["teal"]})]], 13, C["ink"], name="read")
    return s


def plan_code(ex, visual):
    """Choose layout and font: the largest code font (14 down to 9 pt) for which the code, its explanations and the result visual all fit.
    Order of preference: the explanation beside the code (side) at 11 pt or more, then below the code at 11 pt or more, then smaller."""
    maxlen = max(len(l) for l in X.code_lines(ex)) + 4
    forced_below = ex.get("layout") == "below"
    cands = []
    for lay in (["below"] if forced_below else ["side", "below"]):
        for fs in (14, 13, 12, 11, 10.5, 10, 9.5, 9):
            cands.append((lay, fs))
    # from 11 pt up the layout comes first (side before below, each at every size); below 11 pt the larger font wins, side before below at each size
    cands.sort(key=lambda c: (0, 0) if c[1] >= 11 else (1, -c[1]))
    top, gapv = 0.86, 0.05
    last = None
    for lay, fs in cands:
        need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
        if lay == "side":
            box_w = max(3.2, need_w)
            if box_w > 6.2:
                continue
            expl_w = 9.2 - box_w + 0.02
        else:
            box_w, expl_w = 9.2, 9.2
            if need_w > 9.2:
                continue
        nfs = 12.5 if fs >= 12 else (12 if fs >= 10.5 else 11)
        lh = fs * 1.22 / 72.0
        cpl = max(10, (expl_w - 0.3) * 72.0 / (0.54 * nfs))
        rows = []
        for g, note in ex["groups"]:
            code_h = len(g) * lh + 0.15
            n_h = math.ceil(len(note) / cpl) * nfs * 1.25 / 72.0 + 0.14
            rows.append((code_h, n_h))
        heights = [max(a, b, 0.42) for a, b in rows] if lay == "side" else [a + b for a, b in rows]
        total = sum(heights) + gapv * (len(heights) - 1)
        ry = top + total + 0.08
        avail = 5.04 - (ry + 0.3)
        last = (lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail)
        if avail >= visual.need:
            return last
    if last is None:
        raise SystemExit("REFUSED: %s has no layout in which its longest code line fits the slide" % ex["id"])
    print("WARN %s: no layout leaves %.2f in for the result (wants %.2f)" % (ex["id"], last[-1], visual.need))
    return last


def make_code(prs, exid):
    ex = X.BY_ID[exid]
    out, ns = RUN[exid]
    s = base(prs, ex["title"], None, nt=T.NOTES[exid])
    visual = V.VISUALS[ex["visual"]]
    lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail = plan_code(ex, visual)
    y, gapv = 0.86, 0.05
    for (g, note), (ch_, nh_), hh in zip(ex["groups"], rows, heights):
        if lay == "side":
            code_box(s, 0.4, y, box_w, hh, g, fs)
            tb(s, 0.4 + box_w - 0.02, y, expl_w, hh, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.14, 0.02))
        else:
            code_box(s, 0.4, y, box_w, ch_, g, fs)
            tb(s, 0.4, y + ch_ + 0.01, box_w, nh_, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.12, 0.02))
        y += hh + gapv
    tb(s, 0.4, ry, 6.0, 0.26, "What the run printed (Python %s)" % PYV, 11, C["teal"], bold=True, name="result label")
    visual(s, 0.4, ry + 0.3, 9.2, max(avail, 1.0), ns, out)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def make_vocab(prs):
    s = base(prs, "A Program by Any Other Name", "Seven words for nearly the same thing", nt=T.NOTES["vocab"])
    analogy_box(s, 1.1, "One dish on many menus: dish, plate, course. The words differ by how the program is started.", 0.5, 13)
    table(s, 0.5, 1.8, 9.0, T.VOCAB, [1.7, 4.6, 2.7], rowh=0.4, mono_cols=(2,), bold_cols=(0,), fs=12)
    takeaway(s, "A script is run from source; a command is started from a terminal.")
    return s


def make_tools(prs):
    s = base(prs, "Pop-ups, sound and colour: the helpers", "Most are third-party packages; the page does not run them", nt=T.NOTES["tools"])
    table(s, 0.5, 1.25, 9.0, T.TOOLS, [2.6, 4.0, 2.4], rowh=0.5, mono_cols=(0,), bold_cols=(0,), fs=12)
    tb(s, 0.5, 4.5, 9.0, 0.5, "PyMsgBox offers alert, confirm, prompt and password. Bext offers fg, bg, clear, goto and get_key.", 12, C["muted"], italic=True, name="note")
    takeaway(s, "Check the package name before you install: the chapter and PyPI differ.")
    return s


def make_launchers(prs):
    s = base(prs, "Launcher files on three systems", "One idea in three spellings", nt=T.NOTES["launchers"])
    analogy_box(s, 1.1, "A launcher is a taxi dispatcher: you say where, it activates the environment and drives the program there.", 0.5, 13)
    table(s, 0.5, 1.85, 9.0, T.LAUNCHERS, [1.2, 5.6, 2.2], rowh=0.62, mono_cols=(2,), bold_cols=(0,), fs=12)
    takeaway(s, "Forward the arguments, or the script never receives them.")
    return s


def make_pyinfo(prs):
    s = base(prs, "PyInstaller: what the one file costs", "Measured in the chapter research with PyInstaller 6.22.3 and Python 3.14.6", nt=T.NOTES["pyinfo"])
    tb(s, 0.5, 1.15, 5.0, 0.3, "size of the Hello, world executable, in megabytes", 11, C["teal"], bold=True, name="chart label")
    chart(s, "bar", 0.4, 1.5, 5.4, 3.0, ["Measured on Ubuntu", "The chapter's text (Windows)"], [("megabytes", [12.95, 8.0])], fs=11, legend=False, gap=60, vmax=16, major=4)
    rows = [["Fact", "Value"], ["Source file", "23 bytes"], ["Executable (Ubuntu)", "12,950,120 bytes"], ["Build time", "about 15 seconds"], ["Leaves", "build, dist, a spec file"],
            ["Works on", "one system, one Python"]]
    table(s, 6.0, 1.5, 3.6, rows, [1.6, 2.0], rowh=0.45, fs=11, bold_cols=(0,))
    takeaway(s, "PyInstaller packs a copy of the interpreter with your script.")
    return s


def make_current(prs):
    s = base(prs, "Current Python and systems change more", "What differs from the book, from the chapter research", nt=T.NOTES["current"])
    table(s, 0.5, 1.15, 9.0, T.CURRENT, [4.3, 1.3, 3.4], rowh=0.46, bold_cols=(0,), fs=11, align_cols={1: PP_ALIGN.CENTER})
    takeaway(s, "Run what the book printed; then check what changed.")
    return s


def make_summary(prs):
    s = base(prs, "Summary", None, nt=T.NOTES["summary"])
    analogy_box(s, 0.82, "A summary is a packing list: only what you really need goes into the bag.", 0.5, 13)
    for i, t_ in enumerate(T.SUMMARY_POINTS):
        yy = 1.5 + i * 0.62
        label_shape(s, 0.4, yy + 0.04, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 0.9, yy, 4.6, 0.52, t_, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="point")
    per_part = [sum(1 for e in X.EXAMPLES if e["part"] == k) for k in range(1, 6)]
    tb(s, 5.7, 1.4, 3.9, 0.5, "code examples in each part of this deck", 10.5, C["teal"], bold=True, name="chart label")
    chart(s, "col", 5.6, 1.95, 4.0, 3.0, ["Part %d" % k for k in range(1, 6)], [("examples", per_part)], fs=10, legend=False, gap=50, vmax=6, major=1)
    takeaway(s, "The terminal searches PATH; the program reads its arguments.")
    return s


def make_practice(prs):
    s = base(prs, "Practice Questions", "Predict first, then run what you can on the chapter page", nt=T.NOTES["practice"])
    analogy_box(s, 1.05, "Practice questions are finger scales for a pianist: short drills before the performance.", 0.5, 13)
    for i, q in enumerate(T.PRACTICE):
        yy = 1.75 + i * 0.8
        rect(s, 0.4, yy, 9.2, 0.68, C["card"], line=C["line"], radius=0.08, name="card")
        label_shape(s, 0.55, yy + 0.14, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 1.1, yy + 0.04, 8.4, 0.6, q, 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="question")
    takeaway(s, "Each answer fits in a few lines you can run.")
    return s


def make_resources(prs):
    s = base(prs, "Resources: where to go next", "Reading and watching, chosen for this chapter; every link is live", nt=T.NOTES["resources"])
    for i, (t, url, host) in enumerate(T.RESOURCES):
        col, row = divmod(i, 7)
        xx = 0.4 + col * 4.7
        yy = 1.1 + row * 0.57
        rect(s, xx, yy, 4.5, 0.5, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, xx + 0.08, yy + 0.01, 4.35, 0.48, [[(t, {"bold": True})], [(url if len(url) < 58 else host, {"link": url, "color": C["teal"], "size": 9})]], 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="resource")
    takeaway(s, "Pick one link and read it before the next class.")
    return s


MAKERS = {"title": make_title, "route": make_route, "questions": make_questions, "vocab": make_vocab, "tools": make_tools, "launchers": make_launchers,
          "pyinfo": make_pyinfo, "current": make_current, "summary": make_summary, "practice": make_practice, "resources": make_resources}


# ------------------------------------------------------------------ build
def build():
    prs = new_deck()
    for p in PLAN:
        kind = p[0]
        if kind in MAKERS:
            MAKERS[kind](prs)
        elif kind == "divider":
            make_divider(prs, p[1])
        elif kind == "analogy":
            make_analogy(prs, p[1])
        elif kind == "story":
            make_story(prs, p[1])
        elif kind == "code":
            make_code(prs, p[1])
    add_numbers(prs)
    prs.core_properties.title = "SEN0414 Chapter 12: Command Line Programs (lecture deck 2.0.0)"
    prs.core_properties.author = "Yusuf Altunel"
    os.makedirs(os.path.dirname(OUT_DECK), exist_ok=True)
    prs.save(OUT_DECK)
    return len(prs.slides)


def write_manifest():
    exs = []
    for k, ex in enumerate(X.EXAMPLES, 1):
        out, _ = RUN[ex["id"]]
        exs.append({"order": k, "id": ex["id"], "name": ex["name"], "slide": SLIDE_OF[("code", ex["id"])], "concepts": ex["concepts"],
                    "code": X.code_text(ex), "expected": out})
    names = [e["name"] for e in exs]
    assert len(set(names)) == len(names)
    man = {"chapter": 12, "version": "1.0.0", "kind": "chapter-code manifest",
           "deck": os.path.relpath(OUT_DECK, ROOT).replace(os.sep, "/"),
           "about": "The code examples of the chapter 12 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                    "every example is self-contained and runs with the Python standard library only, reads no keyboard and starts no other program (a command line program is about how a "
                    "program is started, so each mechanism is shown on text or on a throw-away folder that the example removes); the expected result is what the run printed in a fresh "
                    "interpreter. The code is exactly the text of the deck's code boxes with the '>>> ' prompt removed.",
           "executed_with": {"python": PYV, "library": None},
           "library": {"file": None, "sha256": None, "data_files": [],
                       "page_requirements": ["The Python standard library modules os, shutil, tempfile, shlex, argparse, importlib.util, json, stat, configparser, random (imported by the examples that use them), and the built-ins print, repr, sorted, len, isinstance, chr, ord, dict, iter, next",
                                             "A writable temporary folder and os.chdir (the terminal, PATH, launcher and ccwd examples); no subprocess, no keyboard input, no network"]},
           "prelude": "",
           "examples": exs}
    os.makedirs(os.path.dirname(OUT_MAN), exist_ok=True)
    with open(OUT_MAN, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    n = build()
    write_manifest()
    print("deck %s | %d slides | %d code examples | manifest %s" % (os.path.relpath(OUT_DECK, ROOT), n, len(X.EXAMPLES), os.path.relpath(OUT_MAN, ROOT)))
