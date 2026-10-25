#!/usr/bin/env python3
"""Builds the chapter 10 lecture deck 2.0.0 (Reading and Writing Files) on the deck standard, and its chapter-code manifest.

A NEW tool (the deck of 1.0.0 and its builder stay untouched). Every code example of examples_v2_0_0.py is RUN here; the
printed result and every number in a result visual come from that run. One light background scheme, a number on every
slide, a chip '>>>' on every slide that is not a divider, native tables and charts, drawn diagrams with arrows.
Writes: 03-materials/ch10/SEN0414_Ch10_ReadingWritingFiles_3e_v2_0_0.pptx
        03-materials/ch10/page/chapter_code_ch10_v1_0_0.json   (order = slide order; the code exactly as the code boxes show it)
Usage:  python3 deck_build_v2_0_0.py
"""
__version__ = "2.0.0"
import contextlib
import io
import json
import math
import os
import platform
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

OUT_DECK = os.path.join(ROOT, "03-materials", "ch10", "SEN0414_Ch10_ReadingWritingFiles_3e_v2_0_0.pptx")
OUT_MAN = os.path.join(ROOT, "03-materials", "ch10", "page", "chapter_code_ch10_v1_0_0.json")
ASSETS = os.path.join(ROOT, "03-materials", "ch10", "assets")
PYV = platform.python_version()


# ------------------------------------------------------------------ run every example
def run_example(ex):
    code = X.code_text(ex)
    buf = io.StringIO()
    ns = {"__code__": code}
    cwd = os.getcwd()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<%s>" % ex["id"], "exec"), ns)
    finally:
        os.chdir(cwd)
    return buf.getvalue(), ns


RUN = {ex["id"]: run_example(ex) for ex in X.EXAMPLES}

# ------------------------------------------------------------------ the plan: slide kinds in order
PARTS = {
    1: ("Part 1: Filepaths", "Names, addresses and the parts of a path", [
        ("Path object", "A path is an object, built with Path() or the slash."),
        ("Working directory", "The folder that every short path starts from."),
        ("Absolute or relative", "A full address, or directions from where you stand."),
        ("Path parts", "Name, stem, suffix and parents of one path."),
    ]),
    2: ("Part 2: Folders and file facts", "Build folders, find files, ask the file system", [
        ("makedirs and mkdir", "Build one folder, or a whole chain of them at once."),
        ("glob", "Find files by a pattern with a question mark or a star."),
        ("exists", "Ask whether a path is really there before you use it."),
        ("stat", "Read the size and the time of a file."),
    ]),
    3: ("Part 3: Reading and writing text", "Open, read, write, close, and say how the letters are stored", [
        ("open and close", "Borrow a file object, use it, give it back."),
        ("read and write", "Take the whole text, one line, or a few characters."),
        ("with", "The block that closes the file for you."),
        ("Modes and encoding", "w, a and x decide what happens to old text."),
    ]),
    4: ("Part 4: Saving variables", "Keep Python values in a file between two runs", [
        ("shelve", "A dictionary that is kept in a file."),
        ("Shelf trap", "A list changed in place is not saved."),
        ("json", "A plain text format that other programs can read."),
        ("pickle warning", "Never open a shelf that came from a stranger."),
    ]),
    5: ("Part 5: Programs", "Two practice programs and Project 4, the quiz maker", [
        ("Mad Libs", "Fill the blanks of a story file with re.sub."),
        ("Regex Search", "Search every text file of a folder for a pattern."),
        ("Project 4", "Make quiz files and answer keys at random."),
        ("Summary", "Sort every tool: compute, ask or change."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("code", "pathobjects"), ("story", "pathlib"), ("analogy", "A2"), ("code", "locations"), ("code", "anatomy"),
        ("divider", 2), ("analogy", "A3"), ("code", "folders"), ("code", "glob"), ("code", "fileinfo"),
        ("divider", 3), ("analogy", "A4"), ("code", "wholefile"), ("story", "utf8"), ("code", "openclose"), ("code", "readmethods"), ("analogy", "A5"),
        ("code", "withstatement"), ("code", "modes"), ("code", "encoding"),
        ("divider", 4), ("analogy", "A6"), ("code", "shelve"), ("story", "dbm"), ("code", "json"), ("story", "json"),
        ("divider", 5), ("analogy", "A7"), ("code", "madlibs"), ("code", "regexsearch"), ("code", "quizquestion"), ("code", "quizfiles"),
        ("current",), ("summary",), ("practice",), ("resources",)]
N = len(PLAN)
NCONCEPTS = len({r[0].lower() for a_ in T.ANALOGIES for r in a_[3]})
SLIDE_OF = {p: i for i, p in enumerate(PLAN, 1)}
CODE_ORDER = [p[1] for p in PLAN if p[0] == "code"]
assert CODE_ORDER == [e["id"] for e in X.EXAMPLES], "the examples file must list the examples in slide order"


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


# ------------------------------------------------------------------ slide makers
def make_title(prs):
    s = base(prs, "Reading and Writing Files", None, chip=True, nt=T.NOTES["title"])
    s.shapes[-1].left, s.shapes[-1].top, s.shapes[-1].width, s.shapes[-1].height = Inches(0.6), Inches(1.7), Inches(8.8), Inches(0.9)
    for r in s.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.size = K.Pt(38)
    tb(s, 0.6, 2.65, 8.8, 0.7, "Chapter 10 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course", 16, C["muted"], name="subtitle")
    for i, (a, b) in enumerate([(str(len(X.EXAMPLES)), "code examples that run on the chapter page"), (str(len(T.STORIES)), "true stories with who, what, when, where, why and how"),
                                (str(NCONCEPTS), "distinct chapter concepts, each with an everyday picture")]):
        xx = 0.6 + i * 3.0
        rect(s, xx, 3.5, 2.8, 1.15, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, xx + 0.1, 3.55, 2.6, 0.5, a, 28, C["teal"], bold=True, name="stat")
        tb(s, xx + 0.1, 4.05, 2.6, 0.55, b, 11.5, C["ink"], name="stat label")
    tb(s, 0.6, 4.85, 8.0, 0.3, "SEN0414 Advanced Programming, Fall 2026. Yusuf Altunel, İstanbul Kültür Üniversitesi", 11, C["muted"], name="author")
    return s


def make_route(prs):
    s = base(prs, "Today's route", "Five parts; every range is a run of slides you can jump to", nt=T.NOTES["route"])
    rows = [["Part", "Slides", "Code examples", "You will run"]]
    runs = {1: "Path, slash, cwd, parts of a path", 2: "makedirs, glob, exists, stat", 3: "open, read, write, with, modes, encoding",
            4: "shelve and json", 5: "Mad Libs, Regex Search, Project 4"}
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
    q = [("1", "Which tools only compute a path, which ask the file system, and which change a file or a folder?",
          "Answer on slide %d: the summary sorts every tool of the chapter." % SLIDE_OF[("summary",)]),
         ("2", "Where do the printed outputs and programs of the book differ in current Python?",
          "Answer on slides %d and %d: Project 4 and the newer features." % (SLIDE_OF[("code", "quizfiles")], SLIDE_OF[("current",)]))]
    for i, (n, qq, aa) in enumerate(q):
        yy = 1.3 + i * 1.75
        rect(s, 0.5, yy, 9.0, 1.55, C["card"], line=C["line"], radius=0.05, name="card")
        label_shape(s, 0.7, yy + 0.2, 0.5, 0.5, n, C["teal"], "FFFFFF", size=18, bold=True)
        tb(s, 1.4, yy + 0.12, 7.9, 0.75, qq, 16, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="question")
        tb(s, 1.4, yy + 0.95, 7.9, 0.45, aa, 12.5, C["teal"], anchor=MSO_ANCHOR.MIDDLE, name="answer")
    takeaway(s, "Compute, ask, or change: every file tool is one of the three.")
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
    rows = [["Slide", "In this part"]] + [[str(i), t if len(t) < 41 else t[:38] + "..."] for i, t in items]
    rh = min(0.4, 3.5 / len(rows))
    table(s, 5.8, 1.55, 3.8, rows, [0.65, 3.8], fs=10.5, rowh=rh, name="table")
    return s


def make_analogy(prs, aid):
    _, title, head, rows = [a for a in T.ANALOGIES if a[0] == aid][0]
    s = base(prs, title, None, nt=T.NOTES[aid])
    rect(s, 0.4, 0.82, 9.2, 0.62, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.84, 8.9, 0.58, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), (head, {})]], 14, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    rh = min(0.5, 3.5 / (len(rows) + 1))
    table(s, 0.4, 1.58, 9.2, [["Chapter concept", "Everyday picture"]] + [[a, b] for a, b in rows], [3.2, 6.0], fs=11.5 if len(rows) > 7 else None, rowh=rh, bold_cols=(0,))
    return s


def make_story(prs, sid):
    st = T.STORIES[sid]
    s = base(prs, st["title"], None, nt=T.STORY_NOTES[sid])
    picture(s, os.path.join(ASSETS, st["img"]), 0.4, 0.95, 3.0, 3.2, "Picture for the story: " + st["title"].replace("Story: ", ""), "photo " + sid)
    tb(s, 0.4, 4.2, 3.0, 0.7, st["credit"], 9.5, C["muted"], name="credit")
    yy = 0.92
    for lab in ("who", "what", "when", "where", "why", "how"):
        txt = st[lab]
        nlines = math.ceil((len(txt) + 7) / 62.0)
        h = max(0.44, nlines * 0.235 + 0.14)
        rect(s, 3.6, yy, 6.0, h, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, 3.65, yy, 5.9, h, [[(lab.upper() + "  ", {"bold": True, "color": C["teal"]}), (txt, {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name=lab)
        yy += h + 0.07
    tb(s, 3.6, yy + 0.02, 6.0, 0.36, [[("READ  ", {"bold": True, "color": C["amber"]}), (st["linktext"], {"link": st["link"], "color": C["teal"]})]], 13, C["ink"], name="read")
    return s


def plan_code(ex, visual):
    """Choose layout and font: the largest code font (14 down to 9 pt) for which the code, its explanations and the result visual all fit.
    Order of preference: the explanation beside the code (side) at 11 pt or more, then below the code at 11 pt or more, then smaller."""
    maxlen = max(len(l) for l in X.code_lines(ex)) + 4
    forced_below = ex.get("layout") == "below"
    cands = []
    for fs in (14, 13, 12, 11, 10.5, 10, 9.5, 9):
        for lay in (["below"] if forced_below else ["side", "below"]):
            cands.append((lay, fs))
    top, gapv = 0.86, 0.04
    last = None
    for lay, fs in cands:
        need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
        if lay == "side":
            box_w = max(3.2, need_w)
            if box_w > 5.7:
                continue
            expl_w = 9.2 - box_w + 0.02
        else:
            box_w, expl_w = 9.2, 9.2
            if need_w > 9.2:
                continue
        nfs = 12.5 if fs >= 12 else (12 if fs >= 10.5 else 11)
        lh = fs * 1.22 / 72.0
        cpl = max(10, (expl_w - 0.3) * 72.0 / (0.5 * nfs))
        rows = []
        for g, note in ex["groups"]:
            code_h = len(g) * lh + 0.13
            n_h = math.ceil(len(note) / cpl) * nfs * 1.25 / 72.0 + 0.1
            rows.append((code_h, n_h))
        heights = [max(a, b, 0.36) for a, b in rows] if lay == "side" else [a + b for a, b in rows]
        total = sum(heights) + gapv * (len(heights) - 1)
        ry = top + total + 0.1
        avail = 5.1 - (ry + 0.26)
        cand = (lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail)
        if last is None or avail > last[-1]:
            last = cand
        if avail >= visual.need:
            return cand
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
    y, gapv = 0.92, 0.06
    for (g, note), (ch_, nh_), hh in zip(ex["groups"], rows, heights):
        if lay == "side":
            code_box(s, 0.4, y, box_w, hh, g, fs)
            tb(s, 0.4 + box_w - 0.02, y, expl_w, hh, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.14, 0.02))
        else:
            code_box(s, 0.4, y, box_w, ch_, g, fs)
            tb(s, 0.4, y + ch_ + 0.01, box_w, nh_, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.12, 0.02))
        y += hh + gapv
    tb(s, 0.4, ry, 6.0, 0.24, "What the run printed (Python %s)" % PYV, 10.5, C["teal"], bold=True, name="result label")
    visual(s, 0.4, ry + 0.27, 9.2, max(avail, 1.0), ns, out)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def make_current(prs):
    s = base(prs, "Current Python adds more", "Features newer than the book, from the chapter research", nt=T.NOTES["current"])
    rows = [["Feature", "Since", "What it gives you"],
            ["Path.walk() walks a folder tree", "3.12", "Folders and files of every level, top down"],
            ["glob(..., case_sensitive=...)", "3.12", "Choose whether capitals count, on any system"],
            ["st_ctime is deprecated on Windows", "3.12", "Use st_birthtime for the creation time"],
            ["dbm.sqlite3 is the first shelve backend", "3.13", "A new shelf is one file with the name you gave"],
            ["exists(), is_file(), is_dir() hide OSError", "3.14", "They return False instead of raising any OSError"],
            ["EncodingWarning (PEP 597)", "3.10", "Run with -X warn_default_encoding to find open() calls without encoding"],
            ["UTF-8 mode becomes the default (PEP 686)", "3.15", "open() without encoding will use UTF-8 on every system"]]
    table(s, 0.5, 1.15, 9.0, rows, [4.0, 0.7, 4.3], rowh=0.5, bold_cols=(0,), align_cols={1: PP_ALIGN.CENTER})
    takeaway(s, "Run what the book printed; then check what changed.")
    return s


def make_summary(prs):
    s = base(prs, "Summary", None, nt=T.NOTES["summary"])
    rect(s, 0.4, 0.82, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.83, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("A summary is a packing list: only what you really need goes into the bag.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    pts = ["A path is an object: join it, take it apart, ask where it starts.",
           "Folders are made with makedirs; files are found with glob.",
           "open, read, write and close; with closes for you.",
           "Modes w, a and x decide what happens to old text.",
           "A shelf keeps values in a file; json is the plain alternative."]
    for i, t_ in enumerate(pts):
        yy = 1.5 + i * 0.62
        label_shape(s, 0.4, yy + 0.04, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 0.9, yy, 4.6, 0.52, t_, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="point")
    kinds = T.OPERATION_KINDS
    tb(s, 5.7, 1.4, 3.9, 0.5, "tools of this chapter, by what they do", 10.5, C["teal"], bold=True, name="chart label")
    chart(s, "bar", 5.6, 1.95, 4.0, 3.0, list(kinds)[::-1], [("tools", [len(v) for v in kinds.values()][::-1])], fs=10, legend=False, gap=50, vmax=7, major=1)
    takeaway(s, "Computing is safe, asking is free, changing needs care.")
    return s


def make_practice(prs):
    s = base(prs, "Practice Questions", "Predict first, then run it on the chapter page", nt=T.NOTES["practice"])
    rect(s, 0.4, 1.05, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 1.06, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("Practice questions are finger scales for a pianist: short drills before the performance.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    qs = ["Why does Path('spam') / 'bacon' work, while 'spam' / 'bacon' raises a TypeError?",
          "What does the file hold after the modes w, a, a, w, and what does mode x do?",
          "Why is a list changed inside a shelf lost, and how do you keep the change?",
          "Change the quiz program so that the key file also names the right capital."]
    for i, q in enumerate(qs):
        yy = 1.8 + i * 0.8
        rect(s, 0.4, yy, 9.2, 0.68, C["card"], line=C["line"], radius=0.08, name="card")
        label_shape(s, 0.55, yy + 0.14, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 1.1, yy + 0.04, 8.4, 0.6, q, 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="question")
    takeaway(s, "Each answer fits in a few lines you can run.")
    return s


def make_resources(prs):
    s = base(prs, "Resources: where to go next", "Reading and watching, chosen for this chapter; every link is live", nt=T.NOTES["resources"])
    for i, (t, url, host) in enumerate(T.RESOURCES):
        col, row = divmod(i, 8)
        xx = 0.4 + col * 4.7
        yy = 1.05 + row * 0.51
        rect(s, xx, yy, 4.5, 0.46, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, xx + 0.08, yy + 0.0, 4.35, 0.46, [[(t, {"bold": True})], [(url if len(url) < 58 else host, {"link": url, "color": C["teal"], "size": 8.5})]], 10, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="resource", margin=(0.05, 0.0))
    takeaway(s, "Pick one link and read it before the next class.")
    return s


# ------------------------------------------------------------------ build
def build():
    prs = new_deck()
    for p in PLAN:
        kind = p[0]
        if kind == "title":
            make_title(prs)
        elif kind == "route":
            make_route(prs)
        elif kind == "questions":
            make_questions(prs)
        elif kind == "divider":
            make_divider(prs, p[1])
        elif kind == "analogy":
            make_analogy(prs, p[1])
        elif kind == "story":
            make_story(prs, p[1])
        elif kind == "code":
            make_code(prs, p[1])
        elif kind == "current":
            make_current(prs)
        elif kind == "summary":
            make_summary(prs)
        elif kind == "practice":
            make_practice(prs)
        elif kind == "resources":
            make_resources(prs)
    add_numbers(prs)
    prs.core_properties.title = "SEN0414 Chapter 10: Reading and Writing Files (lecture deck 2.0.0)"
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
    man = {"chapter": 10, "version": "1.0.0", "kind": "chapter-code manifest",
           "deck": os.path.relpath(OUT_DECK, ROOT).replace(os.sep, "/"),
           "about": "The code examples of the chapter 10 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                    "every example is self-contained and runs with the Python standard library only; the expected result is what the run printed. The code is exactly the text of the "
                    "deck's code boxes with the '>>> ' prompt removed. Examples that touch files first move into a fresh scratch folder (tempfile.mkdtemp), so no printed result holds a path.",
           "executed_with": {"python": PYV, "library": None},
           "library": {"file": None, "sha256": None, "data_files": [],
                       "page_requirements": ["The Python standard library modules pathlib, os, tempfile, time, shelve, json, re and random (imported by the examples that use them), and the built-ins print, open, repr, sorted, len, iter, next, enumerate, zip",
                                             "A writable temporary folder (tempfile.mkdtemp) and a folder-changing os.chdir; the shelve example writes a small dbm file there"]},
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
