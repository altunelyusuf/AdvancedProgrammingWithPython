#!/usr/bin/env python3
"""Builds the chapter 6 lecture deck 3.1.1 (Lists) on the deck standard, and its chapter-code manifest.

A NEW tool (the decks of 1.0.0 to 3.1.0 and their builders stay untouched; 3.1.1 differs from 3.1.0 only in the two corrections named in examples_v3_1_1.py and deck_visuals_v3_1_1.py). Every code example of examples_v3_1_1.py is RUN here, each in a
fresh interpreter for the manifest's expected result and once in this process for the namespace the result visuals read; the two printed
results must be equal, and every number in a result visual comes from that run. One light background scheme, a number on every slide, the corner brand-mark
'>>>' on every slide that is not a divider, ONE indented code box per code slide without prompt, native tables and charts, drawn diagrams with arrows.
Writes: 03-materials/ch06/SEN0414_Ch06_Lists_3e_v3_1_1.pptx
        03-materials/ch06/page/chapter_code_ch06_v1_1_1.json   (order = slide order; the code exactly as the code boxes show it)
Usage:  python3 deck_build_v3_1_1.py
"""
__version__ = "3.1.1"
import contextlib
import io
import json
import math
import os
import platform
import subprocess
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
import deck_kit_v3_1_0 as K
from deck_kit_v3_1_0 import C, MONO, arrow, chart, code_box, label_shape, new_deck, new_slide, notes, picture, rect, table, tb
X = load("examples_v3_1_1", "examples_v3_1_1.py")
V = load("deck_visuals_v3_1_1", "deck_visuals_v3_1_1.py")
T = load("deck_content_v3_1_0", "deck_content_v3_1_0.py")
V.CODE.update({e["id"]: X.code_text(e) for e in X.EXAMPLES})

OUT_DECK = os.path.join(ROOT, "03-materials", "ch06", "SEN0414_Ch06_Lists_3e_v3_1_1.pptx")
OUT_MAN = os.path.join(ROOT, "03-materials", "ch06", "page", "chapter_code_ch06_v1_1_1.json")
ASSETS = os.path.join(ROOT, "03-materials", "ch06", "assets")
PYV = platform.python_version()


# ------------------------------------------------------------------ run every example
def run_fresh(ex):
    """the result the manifest records: the example alone, in a fresh isolated interpreter (what the page does with it)"""
    r = subprocess.run([sys.executable, "-I", "-c", X.code_text(ex)], capture_output=True, text=True, timeout=60, cwd=tempfile.mkdtemp())
    if r.returncode != 0:
        raise SystemExit("REFUSED: example %s failed in a fresh interpreter: %s" % (ex["id"], r.stderr[-300:]))
    return r.stdout


def run_here(ex):
    """the same code in this process, for the namespace the result visual reads"""
    buf = io.StringIO()
    ns = {}
    with contextlib.redirect_stdout(buf):
        exec(compile(X.code_text(ex), "<%s>" % ex["id"], "exec"), ns)
    return buf.getvalue(), ns


RUN = {}
for _ex in X.EXAMPLES:
    _fresh = run_fresh(_ex)
    _here, _ns = run_here(_ex)
    assert _fresh == _here, "example %s printed different results in a fresh interpreter and in the builder: %r vs %r" % (_ex["id"], _fresh, _here)
    RUN[_ex["id"]] = (_fresh, _ns)

# ------------------------------------------------------------------ the plan: slide kinds in order
PARTS = {
    1: ("Part 1: The list as a value", "One value, many items, each reachable by a number", [
        ("List", "One value that holds many items in order."),
        ("Index", "A number from zero, or a minus number from the end."),
        ("Slice", "A part of a list, as a new list."),
        ("Sequence", "Strings and tuples share the numbering of lists."),
    ]),
    2: ("Part 2: Changing, combining, searching", "What a list can do, and which actions change the list itself", [
        ("In-place change", "The same list is rewritten, not replaced."),
        ("Combining", "Plus and star build lists; += changes one."),
        ("Searching", "in says whether, index says where."),
        ("Ordering", "sort changes the list; sorted returns a new one."),
    ]),
    3: ("Part 3: Loops and unpacking", "Walking a list, changing it safely, naming its items", [
        ("range and enumerate", "Walk by position, or by item and number."),
        ("The removal trap", "Never remove from the list you loop over."),
        ("Unpacking", "Give each item a name in one line."),
        ("Comprehension", "Build a new list from an old one in one line."),
    ]),
    4: ("Part 4: Names and copies", "A name is a tag; two tags can reach one list", [
        ("Reference", "A variable holds a way to reach a list."),
        ("Aliasing", "Two names, one list: change one, see both."),
        ("Shallow copy", "A new outer list that shares its inner lists."),
        ("Deep copy", "Every level copied; nothing is shared."),
    ]),
    5: ("Part 5: Random choices and programs", "Chance and lists make games, screens and simulations", [
        ("choice and shuffle", "Pick one item, or reorder the list itself."),
        ("A fair shuffle", "Every order has the same chance."),
        ("Counters", "A list of counters can animate a screen."),
        ("Simulation", "Repeat an experiment to measure a chance."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "an1"), ("story", "dijkstra"), ("code", "indexes"), ("code", "nested"), ("code", "slices"), ("code", "dijkstra"), ("code", "sequences"),
        ("divider", 2), ("analogy", "an2"), ("analogy", "an3"), ("code", "change"), ("code", "augmented"), ("analogy", "an4"), ("code", "searching"), ("code", "shortcircuit"), ("code", "sort"),
        ("story", "magic8"), ("code", "magic8"),
        ("divider", 3), ("analogy", "an5"), ("code", "loops"), ("code", "removal"), ("code", "unpack"), ("code", "comprehension"), ("code", "input"),
        ("divider", 4), ("analogy", "an7"), ("code", "alias"), ("code", "argument"), ("code", "copies"),
        ("divider", 5), ("analogy", "an6"), ("code", "random"), ("story", "fisher"), ("code", "fairshuffle"), ("story", "rain"), ("code", "matrix"), ("analogy", "an8"), ("code", "commacode"), ("code", "coinstreaks"),
        ("current",), ("summary",), ("practice",), ("resources",)]
PLAN = [q for p in PLAN for q in ((("teach", p[1]), p) if p[0] == "code" else (p,))]
N = len(PLAN)
NCONCEPTS = sum(len(a_[3]) for a_ in T.ANALOGIES)          # the analogy rows
SLIDE_OF = {}      # ("code", id) -> slide number, ("divider", k) -> slide number
for i, p in enumerate(PLAN, 1):
    SLIDE_OF[p] = i
CODE_ORDER = [p[1] for p in PLAN if p[0] == "code"]
assert CODE_ORDER == [e["id"] for e in X.EXAMPLES], "the examples file must list the examples in slide order"


def part_slides(k):
    """slide numbers from divider k up to the slide before divider k+1 (or the current-Python slide)"""
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
    s = base(prs, "Lists", None, chip=True, nt=T.NOTES["title"])
    s.shapes[-1].left, s.shapes[-1].top, s.shapes[-1].width, s.shapes[-1].height = Inches(0.6), Inches(1.7), Inches(8.8), Inches(0.9)
    for r in s.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.size = K.Pt(38)
    tb(s, 0.6, 2.65, 8.8, 0.7, "Chapter 6 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course", 16, C["muted"], name="subtitle")
    for i, (a, b) in enumerate([(str(len(X.EXAMPLES)), "code examples that run on the chapter page"), (str(len(T.STORIES)), "true stories told with real names, dates and places"), (str(NCONCEPTS), "chapter concepts, each with an everyday picture")]):
        xx = 0.6 + i * 3.0
        rect(s, xx, 3.5, 2.8, 1.15, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, xx + 0.1, 3.55, 2.6, 0.5, a, 28, C["teal"], bold=True, name="stat")
        tb(s, xx + 0.1, 4.05, 2.6, 0.55, b, 11.5, C["ink"], name="stat label")
    tb(s, 0.6, 4.85, 8.0, 0.3, "SEN0414 Advanced Programming, Fall 2026. Yusuf Altunel, İstanbul Kültür Üniversitesi", 11, C["muted"], name="author")
    return s


def make_route(prs):
    s = base(prs, "Today's route", "Five parts; every range is a run of slides you can jump to", nt=T.NOTES["route"])
    rows = [["Part", "Slides", "Code examples", "You will run"]]
    runs = {1: "indexes, slices, sequences", 2: "change, combine, search, sort", 3: "loops, unpacking, comprehensions", 4: "aliases and copies", 5: "random, fair shuffle, short programs"}
    for k in range(1, 6):
        a, b = part_slides(k)
        nex = sum(1 for p in PLAN[a - 1:b] if p[0] == "code")
        rows.append([PARTS[k][0].split(": ", 1)[1], "%d - %d" % (a, b), str(nex), runs[k]])
    rows.append(["Changes, summary, practice, resources", "%d - %d" % (SLIDE_OF[("current",)], N), "-", "what current Python adds"])
    table(s, 0.5, 1.2, 9.0, rows, [3.6, 1.1, 1.3, 3.2], fs=13, rowh=0.55, bold_cols=(0,))
    takeaway(s, "Open the chapter-code tab of the page: the same %d examples, in this order." % len(X.EXAMPLES))
    return s


def make_questions(prs):
    s = base(prs, "Three questions this chapter answers", "Carry them through every part; the answers come back at the end", nt=T.NOTES["questions"])
    q = [("1", "Which list operations read, replace, add, remove, find, order and combine items, and which change the list in place?",
          "Answer on slide %d: in place, a new list, or shared." % SLIDE_OF[("summary",)]),
         ("2", "How do names, copies and function arguments decide whether a change to a list is seen elsewhere?",
          "Answer on slides %d to %d: two names reach one list." % (SLIDE_OF[("code", "alias")], SLIDE_OF[("code", "copies")])),
         ("3", "Which printed results of the book differ in current Python, and what does the book leave out?",
          "Answer on slide %d: messages, unpacking and comprehensions." % SLIDE_OF[("current",)])]
    for i, (n, qq, aa) in enumerate(q):
        yy = 1.15 + i * 1.3
        rect(s, 0.5, yy, 9.0, 1.18, C["card"], line=C["line"], radius=0.05, name="card")
        label_shape(s, 0.7, yy + 0.3, 0.5, 0.5, n, C["teal"], "FFFFFF", size=18, bold=True)
        tb(s, 1.4, yy + 0.06, 7.9, 0.66, qq, 14, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="question")
        tb(s, 1.4, yy + 0.74, 7.9, 0.36, aa, 12, C["teal"], anchor=MSO_ANCHOR.MIDDLE, name="answer")
    takeaway(s, "Change in place, make a new list, or share one: ask it of every operation.")
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
        tb(s, 2.85, yy - 0.05, 2.8, 0.68, mean, 12, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="meaning")
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
    rh = min(0.5, 3.4 / (len(rows) + 1))
    table(s, 0.4, 1.6, 9.2, [["Chapter concept", "Everyday picture"]] + [[a, b] for a, b in rows], [3.2, 6.0], fs=12 if len(rows) > 6 else None, rowh=rh, bold_cols=(0,))
    return s


def make_story(prs, sid):
    st = T.STORIES[sid]
    s = base(prs, st["title"], None, nt=T.STORY_NOTES[sid])
    picture(s, os.path.join(ASSETS, st["img"]), 0.4, 0.95, 2.9, 3.2, "Picture for the story: " + st["title"].replace("Story: ", ""), "photo " + sid)
    tb(s, 0.4, 4.2, 2.9, 0.9, st["credit"], 9.5, C["muted"], name="credit")
    yy = 0.95
    for key in ("p1", "p2", "p3"):
        txt = st[key]
        nlines = math.ceil(len(txt) / 56.0)
        h = max(0.6, nlines * 0.27 + 0.18)
        rect(s, 3.5, yy, 6.1, h, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, 3.58, yy, 5.95, h, txt, 14, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="story")
        yy += h + 0.1
    tb(s, 3.5, yy + 0.02, 6.1, 0.36, [[(st["linktext"], {"link": st["link"], "color": C["teal"], "bold": True})]], 13, C["ink"], name="link")
    if yy + 0.4 > 5.15:
        print("WARN story %s: the cards end at %.2f in" % (sid, yy + 0.4))
    return s


def make_teach(prs, exid):
    tc = T.TEACH[exid]
    s = base(prs, tc["title"], None, nt=T.EX_NOTES[exid][0])
    cards = [("The idea", tc["idea"], C["card"], C["teal"]), ("The reason", tc["reason"], C["card"], C["teal"]), ("An everyday picture", tc["picture"], C["amberLight"], C["amber"])]
    yy = 0.92
    for head, txt, fill, hc in cards:
        h = 1.3
        rect(s, 0.4, yy, 4.4, h, fill, line=C["line"], radius=0.06, name="card")
        tb(s, 0.5, yy + 0.04, 4.2, 0.28, head, 12, hc, bold=True, name="card head")
        tb(s, 0.5, yy + 0.32, 4.2, h - 0.36, txt, 12.5, C["ink"], name="card text")
        yy += h + 0.09
    tb(s, 5.05, 0.92, 4.5, 0.3, "How it works, step by step", 12, C["teal"], bold=True, name="flow head")
    n = len(tc["flow"])
    bh, gap = 0.78, 0.2
    y0 = 1.3
    for i, (a, b) in enumerate(tc["flow"]):
        yb = y0 + i * (bh + gap)
        rect(s, 5.05, yb, 4.5, bh, C["tealLight"] if i < n - 1 else C["greenLight"], line=C["line"], radius=0.08, name="step")
        label_shape(s, 5.15, yb + 0.19, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True, name="step number")
        tb(s, 5.65, yb + 0.02, 3.85, 0.3, a, 13, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="step title")
        tb(s, 5.65, yb + 0.32, 3.85, 0.42, b, 11.5, C["muted"], anchor=MSO_ANCHOR.TOP, name="step detail")
        if i < n - 1:
            arrow(s, 7.3, yb + bh, 7.3, yb + bh + gap, C["teal"], 2)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def note_heights(notes, w, nfs):
    cpl = max(8, (w - 0.3) * 72.0 / (0.54 * nfs))
    return [math.ceil(len(n) / cpl) * nfs * 1.25 / 72.0 + 0.2 for n in notes]


def plan_code(ex, visual):
    """ONE code box per slide. Layout 'side': the box on the left, the short explanations stacked beside it, the result visual under the taller of the two.
    Layout 'left': the box and its explanations in a left column and the result visual in a right column (long examples).
    The largest code font (14 down to 9 pt) for which everything fits and the visual keeps its room."""
    lines = X.code_lines(ex)
    maxlen = max(len(l) for l in lines) + 1
    top, gap = 0.92, 0.08
    last = None
    if ex.get("layout") == "left":
        for fs in (11, 10.5, 10, 9.5, 9):
            need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
            if need_w > 5.2:
                continue
            box_w = max(3.4, need_w)
            lh = fs * 1.22 / 72.0
            box_h = len(lines) * lh + 0.2
            nfs = 11 if fs >= 10 else 10.5
            nh = note_heights(ex["notes"], box_w, nfs)
            total = box_h + 0.06 + sum(nh) + gap * (len(nh) - 1)
            last = ("left", fs, nfs, box_w, box_h, nh, top + total)
            if top + total <= 5.12:
                return last
        if last is None:
            raise SystemExit("REFUSED: %s has no 'left' layout in which its longest code line fits" % ex["id"])
        print("WARN %s: the left column ends at %.2f in" % (ex["id"], last[-1]))
        return last
    for fs in (14, 13, 12, 11.5, 11, 10.5, 10, 9.5, 9):
        need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
        box_w = max(3.4, need_w)
        if box_w > 6.0:
            continue
        ex_w = 9.6 - (0.4 + box_w + 0.12)
        lh = fs * 1.22 / 72.0
        box_h = len(lines) * lh + 0.2
        for nfs in (12.5, 12, 11.5, 11, 10.5):
            nh = note_heights(ex["notes"], ex_w, nfs)
            block = max(box_h, sum(nh) + gap * (len(nh) - 1))
            ry = top + block + 0.08
            avail = 5.04 - (ry + 0.3)
            last = ("side", fs, nfs, box_w, box_h, nh, block, ry, avail)
            if avail >= visual.need:
                return last
    print("WARN %s: no layout leaves %.2f in for the result (wants %.2f)" % (ex["id"], last[-1], visual.need))
    return last


def make_code(prs, exid):
    ex = X.BY_ID[exid]
    out, ns = RUN[exid]
    s = base(prs, ex["title"], None, nt=T.EX_NOTES[exid][1])
    visual = V.VISUALS[ex["visual"]]
    plan = plan_code(ex, visual)
    lay, fs, nfs, box_w, box_h, nh = plan[:6]
    lines = X.code_lines(ex)
    if lay == "left":
        print("LAYOUT %-13s left  code %4.1f pt, left column ends %.2f in" % (exid, fs, plan[-1]))
        code_box(s, 0.4, 0.92, box_w, box_h, lines, fs)
        yy = 0.92 + box_h + 0.06
        for note, h in zip(ex["notes"], nh):
            tb(s, 0.4, yy, box_w, h, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.12, 0.02))
            yy += h + 0.08
        vx = 0.4 + box_w + 0.25
        tb(s, vx, 0.92, 9.6 - vx, 0.26, "What the run printed (Python %s)" % PYV, 11, C["teal"], bold=True, name="result label")
        visual(s, vx, 1.25, 9.6 - vx, 3.75, ns, out)
    else:
        block, ry, avail = plan[6], plan[7], plan[8]
        print("LAYOUT %-13s side  code %4.1f pt, visual room %.2f in (wants %.2f)" % (exid, fs, avail, visual.need))
        code_box(s, 0.4, 0.92, box_w, block, lines, fs)
        ex_x = 0.4 + box_w + 0.12
        ex_w = 9.6 - ex_x
        spare = (block - sum(nh) - 0.08 * (len(nh) - 1)) / len(nh)
        yy = 0.92
        for note, h in zip(ex["notes"], nh):
            h = h + spare
            rect(s, ex_x, yy, ex_w, h, C["card"], line=C["line"], radius=0.06, name="note card")
            tb(s, ex_x + 0.05, yy, ex_w - 0.1, h, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation")
            yy += h + 0.08
        tb(s, 0.4, ry, 6.0, 0.22, "What the run printed (Python %s)" % PYV, 10.5, C["teal"], bold=True, name="result label")
        visual(s, 0.4, ry + 0.25, 9.2, max(avail, 1.0), ns, out)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def make_current(prs):
    s = base(prs, "Current Python adds more", "Differences and additions found in the chapter research", nt=T.NOTES["current"])
    rows = [["Feature", "Since", "What it gives you"],
            ["Message of index() for a missing item", "3.14", "list.index(x): x not in list, where older Python printed the item"],
            ["Message of a too long unpacking", "3.14", "too many values to unpack (expected 2, got 3) names both counts"],
            ["List comprehensions", "2.0", "One line builds a list from another"],
            ["Starred name in an unpacking", "3.0", "first, *rest = items collects the remaining items"],
            ["Unpacking inside a list display", "3.5", "[*a, *b] joins two lists in a new list"],
            ["Stable sort, key and reverse", "all", "Items with equal keys keep their order"],
            ["Slice, list() and list.copy()", "all", "Each makes a shallow copy of the list"]]
    table(s, 0.5, 1.1, 9.0, rows, [3.5, 0.7, 4.8], fs=12, rowh=0.46, bold_cols=(0,), align_cols={1: PP_ALIGN.CENTER})
    takeaway(s, "Run what the book printed; then check what changed.")
    return s


def make_summary(prs):
    s = base(prs, "Summary", None, nt=T.NOTES["summary"])
    rect(s, 0.4, 0.82, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.83, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("A summary is a postcard: a few lines that bring back everything you saw.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    pts = ["A list holds items in order; an index picks one and a slice cuts a part.",
           "append, insert, pop, del, remove and sort change the list itself.",
           "sorted, slices, plus and comprehensions return a new list.",
           "Assignment and arguments share one list; copy.deepcopy separates it.",
           "choice and shuffle bring chance; a seed makes it repeat."]
    for i, t_ in enumerate(pts):
        yy = 1.5 + i * 0.62
        label_shape(s, 0.4, yy + 0.04, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 0.9, yy, 4.6, 0.52, t_, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="point")
    per = [sum(1 for e in X.EXAMPLES if e["part"] == k) for k in range(1, 6)]
    tb(s, 5.7, 1.4, 3.9, 0.5, "code examples per part of the chapter", 10.5, C["teal"], bold=True, name="chart label")
    chart(s, "col", 5.6, 1.95, 4.0, 3.0, ["Value", "Change", "Loops", "Copies", "Chance"], [("examples", per)], fs=10, legend=False, gap=50, vmax=8, major=2)
    takeaway(s, "Change in place, make a new list, or share one.")
    return s


def make_practice(prs):
    s = base(prs, "Practice Questions", "Predict first, then run it on the chapter page", nt=T.NOTES["practice"])
    rect(s, 0.4, 1.05, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 1.06, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("Practice questions are finger scales for a pianist: short drills before the performance.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    qs = ["What do spam[-1] and spam[1:3] return for ['cat', 'bat', 'rat', 'elephant']?",
          "Why does 'for x in items: items.remove(x)' leave two items behind in a list of four?",
          "After eggs = spam and eggs[0] = 9, what does spam[0] hold, and why?",
          "Comma Code: make list_to_text turn ['a', 'b', 'c'] into 'a, b, and c'. Then estimate the Coin Flip Streaks chance."]
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
        col, row = divmod(i, 6)
        xx = 0.4 + col * 4.7
        yy = 1.1 + row * 0.66
        rect(s, xx, yy, 4.5, 0.58, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, xx + 0.08, yy + 0.02, 4.35, 0.54, [[(t, {"bold": True})], [(url if len(url) < 58 else host, {"link": url, "color": C["teal"], "size": 9})]], 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="resource")
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
        elif kind == "teach":
            make_teach(prs, p[1])
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
    prs.core_properties.title = "SEN0414 Chapter 6: Lists (lecture deck 3.1.1)"
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
    man = {"chapter": 6, "version": "1.1.1", "kind": "chapter-code manifest",
           "deck": os.path.relpath(OUT_DECK, ROOT).replace(os.sep, "/"),
           "about": "The code examples of the chapter 6 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                    "every example is self-contained and runs with the Python standard library only and prints its result; "
                    "the expected result is what the run printed in a fresh interpreter. The code is exactly the text of the deck's code boxes: indented per the Python standard, no prompt, no lambda. "
                    "The deck's slide order is the order of this list.",
           "executed_with": {"python": PYV, "library": None},
           "library": {"file": None, "sha256": None, "data_files": [], "page_requirements": ["random (seeded Mersenne Twister)", "copy", "collections.Counter"]},
           "prelude": "",
           "examples": exs}
    os.makedirs(os.path.dirname(OUT_MAN), exist_ok=True)
    with open(OUT_MAN, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    if "--manifest-only" in sys.argv:
        write_manifest()
        print("manifest only:", OUT_MAN)
        sys.exit(0)
    n = build()
    write_manifest()
    print("deck %s | %d slides | %d code examples | manifest %s" % (os.path.relpath(OUT_DECK, ROOT), n, len(X.EXAMPLES), os.path.relpath(OUT_MAN, ROOT)))
