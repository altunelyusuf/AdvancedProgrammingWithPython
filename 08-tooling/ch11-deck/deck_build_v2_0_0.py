#!/usr/bin/env python3
"""Builds the chapter 11 lecture deck 2.0.0 (Organizing Files) on the deck standard, and its chapter-code manifest.

A NEW tool (the deck of 1.0.0 and its builder stay untouched in this folder). Every code example of examples_v2_0_0.py is RUN
here, in its own temporary folder; the printed result and every number in a result visual come from that run. One light
background scheme, a number on every slide, a chip '>>>' on every slide that is not a divider, native tables and charts, drawn
diagrams with arrows, story pictures from 03-materials/ch11/assets (licences in ASSETS_PROVENANCE_v1_0_0.md).
Writes: 03-materials/ch11/SEN0414_Ch11_OrganizingFiles_3e_v2_0_0.pptx
        03-materials/ch11/page/chapter_code_ch11_v1_0_0.json   (order = slide order; the code exactly as the code boxes show it)
Usage:  python3 deck_build_v2_0_0.py
"""
__version__ = "2.0.0"
import contextlib
import io
import json
import math
import os
import platform
import shutil
import sys
import tempfile

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

OUT_DECK = os.path.join(ROOT, "03-materials", "ch11", "SEN0414_Ch11_OrganizingFiles_3e_v2_0_0.pptx")
OUT_MAN = os.path.join(ROOT, "03-materials", "ch11", "page", "chapter_code_ch11_v1_0_0.json")
ASSETS = os.path.join(ROOT, "03-materials", "ch11", "assets")
PYV = platform.python_version()
STORY_CREDITS = json.load(open(os.path.join(ASSETS, "story_credits_v1_0_0.json"), encoding="utf-8"))


# ------------------------------------------------------------------ run every example (each in its own temporary folder, kept until the deck is saved)
TMP = []


def run_example(ex):
    code = X.code_text(ex)
    buf = io.StringIO()
    ns = {}
    here = os.getcwd()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, "<%s>" % ex["id"], "exec"), ns)
        tmp = os.getcwd()
    finally:
        os.chdir(here)
    TMP.append(tmp)
    return buf.getvalue(), ns, tmp


RUN = {ex["id"]: run_example(ex) for ex in X.EXAMPLES}

# ------------------------------------------------------------------ the plan: slide kinds in order
PARTS = {
    1: ("Part 1: Copying and moving", "The shutil module relocates files and whole folders", [
        ("shutil.copy", "Copies one file; the original stays where it is."),
        ("shutil.copytree", "Copies a folder with everything inside it."),
        ("shutil.move", "Relocates or renames; it can overwrite a file."),
        ("Time stamp", "copy2 also keeps the modification time of the file."),
    ]),
    2: ("Part 2: Deleting, and staying safe", "Permanent deletion has no undo, so print before you delete", [
        ("unlink", "Deletes one file for good, with no recycle bin."),
        ("rmtree", "Removes a whole folder tree in one call."),
        ("Dry run", "Print what would go before anything is deleted."),
        ("send2trash", "A third-party module that uses the recycle bin."),
    ]),
    3: ("Part 3: Folders and trees", "List one folder, then walk a whole tree", [
        ("listdir and glob", "Names of one folder, filtered by a pattern."),
        ("walk", "Gives folder, subfolders and files at every step."),
        ("Folder sizes", "Add up bytes per folder while walking."),
        ("mkdir", "Builds a folder, or a whole chain of folders."),
    ]),
    4: ("Part 4: ZIP archives", "Many files in one parcel, and back again", [
        ("ZipFile", "Opens an archive to write, add or read."),
        ("Compression", "ZIP_DEFLATED shrinks repeated text a great deal."),
        ("extract", "Unpacks one member or all of them."),
        ("make_archive", "Packs a whole folder in a single call."),
    ]),
    5: ("Part 5: Programs that organize files", "Four programs that use everything so far", [
        ("backupToZip", "Backs a folder up into a numbered ZIP."),
        ("Selective copy", "Copies only the files of one extension."),
        ("Big files", "Finds the files above a size limit."),
        ("Date renaming", "Swaps day and month inside file names."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("code", "copy"), ("code", "copytree"), ("code", "copy2"), ("code", "move"),
        ("divider", 2), ("analogy", "A2"), ("code", "unlink"), ("code", "rmtree"), ("code", "dryrun"), ("send2trash",), ("story", "kare"),
        ("divider", 3), ("analogy", "A3"), ("code", "listing"), ("code", "walk"), ("code", "sizes"), ("code", "mkdir"), ("story", "multics"),
        ("divider", 4), ("analogy", "A4"), ("code", "zipwrite"), ("code", "zipmodes"), ("code", "extract"), ("code", "archives"), ("story", "katz"), ("story", "zlib"),
        ("divider", 5), ("analogy", "A5"), ("code", "backup"), ("code", "selective"), ("code", "large"), ("code", "dates"),
        ("current",), ("summary",), ("practice",), ("resources",)]
N = len(PLAN)
NCONCEPTS = len({r[0].lower() for a_ in T.ANALOGIES for r in a_[3]}) + 2
SLIDE_OF = {}
for i, p in enumerate(PLAN, 1):
    SLIDE_OF[p] = i
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
    tb(s, 1.15 if chip else 0.5, 0.18, 8.4 if chip else 9.0, 0.55, title, 22 if len(title) < 52 else 19, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="title")
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


def analogy_box(s, y, head, h=0.5, size=13):
    rect(s, 0.4, y, 9.2, h, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, y + 0.01, 8.9, h - 0.02, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), (head, {})]], size, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")


# ------------------------------------------------------------------ slide makers
def make_title(prs):
    s = base(prs, "Organizing Files", None, chip=True, nt=T.NOTES["title"])
    s.shapes[-1].left, s.shapes[-1].top, s.shapes[-1].width, s.shapes[-1].height = Inches(0.6), Inches(1.7), Inches(8.8), Inches(0.9)
    for r in s.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.size = K.Pt(38)
    tb(s, 0.6, 2.65, 8.8, 0.7, "Chapter 11 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course", 16, C["muted"], name="subtitle")
    for i, (a, b) in enumerate([(str(len(X.EXAMPLES)), "code examples that run on the chapter page"), (str(len(T.STORIES)), "true stories with who, what, when, where, why and how"), (str(NCONCEPTS), "distinct chapter concepts, each with an everyday picture")]):
        xx = 0.6 + i * 3.0
        rect(s, xx, 3.5, 2.8, 1.15, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, xx + 0.1, 3.55, 2.6, 0.5, a, 28, C["teal"], bold=True, name="stat")
        tb(s, xx + 0.1, 4.05, 2.6, 0.55, b, 11.5, C["ink"], name="stat label")
    tb(s, 0.6, 4.85, 8.0, 0.3, "SEN0414 Advanced Programming, Fall 2026. Yusuf Altunel, İstanbul Kültür Üniversitesi", 11, C["muted"], name="author")
    return s


def make_route(prs):
    s = base(prs, "Today's route", "Five parts; every range is a run of slides you can jump to", nt=T.NOTES["route"])
    rows = [["Part", "Slides", "Code examples", "You will run"]]
    runs = {1: "copy, copytree, copy2, move", 2: "unlink, rmdir, rmtree, a dry run", 3: "listdir, glob, walk, folder sizes, mkdir",
            4: "write, append, extract, make_archive", 5: "backup, selective copy, big files, date renaming"}
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
    q = [("1", "Which operations change the disk for good, and how can a program show what it will do first?",
          "Answer on slides %d and %d: unlink and rmtree, then the dry run." % (SLIDE_OF[("code", "unlink")], SLIDE_OF[("code", "dryrun")])),
         ("2", "How does a program visit every file of a folder tree and pack the result into one archive?",
          "Answer on slides %d and %d: os.walk, then the backup project." % (SLIDE_OF[("code", "walk")], SLIDE_OF[("code", "backup")]))]
    for i, (n, qq, aa) in enumerate(q):
        yy = 1.3 + i * 1.75
        rect(s, 0.5, yy, 9.0, 1.55, C["card"], line=C["line"], radius=0.05, name="card")
        label_shape(s, 0.7, yy + 0.2, 0.5, 0.5, n, C["teal"], "FFFFFF", size=18, bold=True)
        tb(s, 1.4, yy + 0.12, 7.9, 0.75, qq, 16, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="question")
        tb(s, 1.4, yy + 0.95, 7.9, 0.45, aa, 12.5, C["teal"], anchor=MSO_ANCHOR.MIDDLE, name="answer")
    takeaway(s, "Know what a call destroys before you run it.")
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
        elif p[0] == "send2trash":
            items.append((i, "send2trash: the recycle bin"))
    rows = [["Slide", "In this part"]] + [[str(i), t if len(t) < 41 else t[:38] + "..."] for i, t in items]
    rh = min(0.4, 3.5 / len(rows))
    table(s, 5.8, 1.55, 3.8, rows, [0.65, 3.8], fs=10.5, rowh=rh, name="table")
    return s


def make_analogy(prs, aid):
    _, title, head, rows = [a for a in T.ANALOGIES if a[0] == aid][0]
    s = base(prs, title, None, nt=T.NOTES[aid])
    analogy_box(s, 0.82, head, 0.62, 14)
    rh = min(0.5, 3.4 / (len(rows) + 1))
    table(s, 0.4, 1.6, 9.2, [["Chapter concept", "Everyday picture"]] + [[a, b] for a, b in rows], [3.0, 6.2], fs=12 if len(rows) > 7 else None, rowh=rh, bold_cols=(0,))
    return s


def make_story(prs, sid):
    st = T.STORIES[sid]
    cr = STORY_CREDITS[st["img"]]
    s = base(prs, st["title"], None, nt=T.STORY_NOTES[sid])
    picture(s, os.path.join(ASSETS, st["img"]), 0.4, 0.95, 2.9, 3.2, st["alt"], "photo " + sid)
    tb(s, 0.4, 4.2, 2.9, 0.8, cr["credit"], 9, C["muted"], name="credit")
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
    """Choose layout and font. 'side': each code box with its explanation beside it, the result visual under them; 'below': the explanation
    under its code box; 'left' (the examples that carry the layout flag): all code boxes with their explanations under them in the left
    column, the result visual in the right column. The largest code font (11 down to 9 pt) for which everything fits wins; when nothing
    fits, the candidate that leaves the most room for the result is taken and a WARN line says so."""
    maxlen = max(len(l) for l in X.code_lines(ex)) + 4
    flag = ex.get("layout")
    top, gapv = 0.9, 0.05
    best = None
    for lay in ([flag] if flag else ["side", "below"]):
        for fs in (11, 10.5, 10, 9.5, 9):
            need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
            if lay == "side":
                box_w = max(3.2, need_w)
                if box_w > 5.7:
                    continue
                expl_w = 9.2 - box_w + 0.02
            elif lay == "left":
                box_w = expl_w = 5.75
                if need_w > box_w:
                    continue
            else:
                box_w = expl_w = 9.2
                if need_w > 9.2:
                    continue
            nfs = 12 if fs >= 11 else (11 if fs >= 10 else 10.5)
            lh = fs * 1.22 / 72.0
            cpl = max(10, (expl_w - 0.3) * 72.0 / (0.5 * nfs))
            rows = []
            for g, note in ex["groups"]:
                code_h = len(g) * lh + 0.14
                n_h = math.ceil(len(note) / cpl) * nfs * 1.25 / 72.0 + 0.08
                rows.append((code_h, n_h))
            heights = [max(a, b, 0.34) for a, b in rows] if lay == "side" else [a + b for a, b in rows]
            total = sum(heights) + gapv * (len(heights) - 1)
            if lay == "left":
                avail = 5.1 - (top + total)          # must stay positive: the code column alone
                res = (lay, fs, nfs, box_w, expl_w, rows, heights, top + total, avail if avail >= 0 else -9)
                ok = avail >= 0
            else:
                ry = top + total + 0.04
                avail = 5.1 - (ry + 0.26)
                res = (lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail)
                ok = avail >= visual.need
            if ok:
                return res
            if best is None or res[-1] > best[-1]:
                best = res
    if best is None:
        raise SystemExit("REFUSED: %s has no layout in which its longest code line fits the slide" % ex["id"])
    print("WARN %s: no layout leaves %.2f in for the result (wants %.2f)" % (ex["id"], best[-1], visual.need))
    return best


def make_code(prs, exid):
    ex = X.BY_ID[exid]
    out, ns, tmp = RUN[exid]
    s = base(prs, ex["title"], None, nt=T.NOTES[exid])
    visual = V.VISUALS[ex["visual"]]
    lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail = plan_code(ex, visual)
    y, gapv = 0.9, 0.05
    for (g, note), (ch_, nh_), hh in zip(ex["groups"], rows, heights):
        if lay == "side":
            code_box(s, 0.4, y, box_w, hh, g, fs)
            tb(s, 0.4 + box_w - 0.02, y, expl_w, hh, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.14, 0.02))
        else:
            code_box(s, 0.4, y, box_w, ch_, g, fs)
            tb(s, 0.4, y + ch_ + 0.01, box_w, nh_, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.12, 0.02))
        y += hh + gapv
    here = os.getcwd()
    os.chdir(tmp)
    try:
        if lay == "left":
            tb(s, 6.35, 0.9, 3.25, 0.26, "What the run printed (Python %s)" % PYV, 10.5, C["teal"], bold=True, name="result label")
            visual(s, 6.35, 1.2, 3.25, 3.85, ns, out)
        else:
            tb(s, 0.4, ry, 6.0, 0.26, "What the run printed (Python %s)" % PYV, 11, C["teal"], bold=True, name="result label")
            visual(s, 0.4, ry + 0.28, 9.2, max(avail, 1.0), ns, out)
    finally:
        os.chdir(here)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def make_send2trash(prs):
    s = base(prs, "send2trash: the recycle bin", "A third-party helper; not in the standard library and not run on the chapter page", nt=T.NOTES["send2trash"])
    analogy_box(s, 1.1, "send2trash is the waste-paper basket: the page can still be pulled out until someone empties the bin.", 0.5)
    rows = [["", "os.unlink", "send2trash.send2trash"],
            ["Where the file goes", "nowhere, it is gone", "the recycle bin of the system"],
            ["Can you get it back?", "no", "yes, until the bin is emptied"],
            ["Where does it come from?", "the standard library", "pip install send2trash"],
            ["Run on the chapter page?", "yes", "no, it needs an installed module"]]
    table(s, 0.5, 1.8, 9.0, rows, [2.6, 2.7, 3.7], rowh=0.5, bold_cols=(0,), mono_cols=(), cell_color={(2, 1): C["coral"], (2, 2): C["green"]})
    takeaway(s, "When in doubt, send to the bin instead of deleting.")
    return s


def make_current(prs):
    s = base(prs, "Current Python adds more", "Features newer than the book, from the Python documentation", nt=T.NOTES["current"])
    rows = [["Feature", "Since", "What it gives you"],
            ["Path.walk() on a Path object", "3.12", "The same three values as os.walk, from a Path"],
            ["onexc in shutil.rmtree", "3.12", "Replaces onerror, which is deprecated"],
            ["ZipFile.mkdir()", "3.11", "Adds an empty folder entry to an archive"],
            ["Path.copy() and Path.move()", "3.14", "Copy and move without importing shutil"],
            ["recurse_symlinks in glob", "3.13", "Choose whether glob follows symbolic links"]]
    table(s, 0.5, 1.25, 9.0, rows, [3.6, 0.8, 4.6], rowh=0.55, bold_cols=(0,), mono_cols=(), align_cols={1: PP_ALIGN.CENTER})
    takeaway(s, "Run what the book printed; then check what changed.")
    return s


def make_summary(prs):
    s = base(prs, "Summary", None, nt=T.NOTES["summary"])
    analogy_box(s, 0.82, "A summary is a packing list: only what you really need goes into the bag.", 0.5)
    pts = ["copy keeps the original; move relocates and can overwrite.",
           "unlink, rmdir and rmtree cannot be undone; print first.",
           "os.walk gives folder, subfolders and files at every step.",
           "ZipFile writes, appends and reads archives; extract unpacks them.",
           "A short program can back up, copy by type or rename in bulk."]
    for i, t_ in enumerate(pts):
        yy = 1.5 + i * 0.62
        label_shape(s, 0.4, yy + 0.04, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 0.9, yy, 4.6, 0.52, t_, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="point")
    per = {k: sum(1 for e in X.EXAMPLES if e["part"] == k) for k in range(1, 6)}
    tb(s, 5.7, 1.4, 3.9, 0.5, "code examples in each part of this chapter", 10.5, C["teal"], bold=True, name="chart label")
    chart(s, "col", 5.6, 1.95, 4.0, 3.0, ["Copy, move", "Delete", "Trees", "ZIP", "Programs"], [("examples", [per[k] for k in range(1, 6)])], fs=10, legend=False, gap=50, vmax=6, major=1)
    takeaway(s, "Know what a call destroys before you run it.")
    return s


def make_practice(prs):
    s = base(prs, "Practice Questions", "Predict first, then run it on the chapter page", nt=T.NOTES["practice"])
    analogy_box(s, 1.05, "Practice questions are finger scales for a pianist: short drills before the performance.", 0.5)
    qs = ["What is the difference between shutil.copy and shutil.move for the original file?",
          "Why print the file names with a dry run before os.unlink is allowed to run?",
          "Which three values does every step of os.walk give you?",
          "Which ZipFile mode adds a file to an archive, and which refuses to overwrite one?"]
    for i, q in enumerate(qs):
        yy = 1.8 + i * 0.8
        rect(s, 0.4, yy, 9.2, 0.68, C["card"], line=C["line"], radius=0.08, name="card")
        label_shape(s, 0.55, yy + 0.14, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 1.1, yy + 0.04, 8.4, 0.6, q, 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="question")
    takeaway(s, "Each answer fits in one line you can run.")
    return s


def make_resources(prs):
    s = base(prs, "Resources: where to go next", "Reading and watching, chosen for this chapter; every link is live", nt=T.NOTES["resources"])
    for i, (t, url, host) in enumerate(T.RESOURCES):
        col, row = divmod(i, 7)
        xx = 0.4 + col * 4.7
        yy = 1.1 + row * 0.57
        rect(s, xx, yy, 4.5, 0.5, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, xx + 0.08, yy + 0.01, 4.35, 0.48, [[(t if len(t) < 60 else t[:57] + "...", {"bold": True})], [(url if len(url) < 58 else host, {"link": url, "color": C["teal"], "size": 9})]], 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="resource")
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
        elif kind == "send2trash":
            make_send2trash(prs)
        elif kind == "current":
            make_current(prs)
        elif kind == "summary":
            make_summary(prs)
        elif kind == "practice":
            make_practice(prs)
        elif kind == "resources":
            make_resources(prs)
    add_numbers(prs)
    prs.core_properties.title = "SEN0414 Chapter 11: Organizing Files (lecture deck 2.0.0)"
    prs.core_properties.author = "Yusuf Altunel"
    os.makedirs(os.path.dirname(OUT_DECK), exist_ok=True)
    prs.save(OUT_DECK)
    return len(prs.slides)


def write_manifest():
    exs = []
    for k, ex in enumerate(X.EXAMPLES, 1):
        out = RUN[ex["id"]][0]
        exs.append({"order": k, "id": ex["id"], "name": ex["name"], "slide": SLIDE_OF[("code", ex["id"])], "concepts": ex["concepts"],
                    "code": X.code_text(ex), "expected": out})
    names = [e["name"] for e in exs]
    assert len(set(names)) == len(names)
    man = {"chapter": 11, "version": "1.0.0", "kind": "chapter-code manifest",
           "deck": os.path.relpath(OUT_DECK, ROOT).replace(os.sep, "/"),
           "about": "The code examples of the chapter 11 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                    "every example is self-contained, works in its own new temporary folder (tempfile.mkdtemp) and runs with the Python standard library only; the expected result is what the run printed. "
                    "The code is exactly the text of the deck's code boxes with the '>>> ' (or '... ') prompt removed.",
           "executed_with": {"python": PYV, "library": None},
           "library": {"file": None, "sha256": None, "data_files": [], "page_requirements": ["The Python standard library modules os, shutil, tempfile, zipfile, re and pathlib; every example works in its own temporary folder and writes nothing outside it"]},
           "prelude": "",
           "examples": exs}
    os.makedirs(os.path.dirname(OUT_MAN), exist_ok=True)
    with open(OUT_MAN, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    n = build()
    write_manifest()
    for t in TMP:
        shutil.rmtree(t, ignore_errors=True)
    print("deck %s | %d slides | %d code examples | manifest %s" % (os.path.relpath(OUT_DECK, ROOT), n, len(X.EXAMPLES), os.path.relpath(OUT_MAN, ROOT)))
