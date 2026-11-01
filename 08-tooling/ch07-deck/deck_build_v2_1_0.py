#!/usr/bin/env python3
"""Builds the chapter 7 lecture deck 2.1.0 (Dictionaries and Structuring Data) on the deck standard, and its chapter-code manifest.

A NEW tool (the deck of 1.0.0 and its builder stay untouched). Every code example of examples_v2_1_0.py is RUN here; the
printed result and every number in a result visual come from that run. One light background scheme, a number on every
slide, a chip '>>>' on every slide that is not a divider, native tables and charts, drawn diagrams with arrows.
Writes: 03-materials/ch07/SEN0414_Ch07_Dictionaries_3e_v2_1_0.pptx
        03-materials/ch07/page/chapter_code_ch07_v1_1_0.json   (order = slide order; the code exactly as the code boxes show it)
Usage:  python3 deck_build_v2_1_0.py
"""
__version__ = "2.1.0"
import contextlib
import io
import json
import math
import os
import platform
import shutil
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
import deck_kit_v2_1_0 as K
from deck_kit_v2_1_0 import C, MONO, arrow, chart, code_box, label_shape, new_deck, new_slide, notes, picture, rect, table, tb
X = load("examples_v2_1_0", "examples_v2_1_0.py")
V = None if "--manifest-only" in sys.argv else load("deck_visuals_v2_1_0", "deck_visuals_v2_1_0.py")
MANIFEST_ONLY = "--manifest-only" in sys.argv
T = None if MANIFEST_ONLY else load("deck_content_v2_1_0", "deck_content_v2_1_0.py")

OUT_DECK = os.path.join(ROOT, "03-materials", "ch07", "SEN0414_Ch07_Dictionaries_3e_v2_1_0.pptx")
OUT_MAN = os.path.join(ROOT, "03-materials", "ch07", "page", "chapter_code_ch07_v1_1_0.json")
ASSETS = os.path.join(ROOT, "03-materials", "ch07", "assets")
PYV = platform.python_version()


# ------------------------------------------------------------------ run every example
def run_example(ex):
    code = X.code_text(ex)
    buf = io.StringIO()
    ns = {}
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<%s>" % ex["id"], "exec"), ns)
    return buf.getvalue(), ns


RUN = {ex["id"]: run_example(ex) for ex in X.EXAMPLES}

# ------------------------------------------------------------------ the plan: slide kinds in order
PARTS = {
    1: ("Part 1: The dictionary and its keys", "Pairs in braces, found by key", [
        ("Dictionary", "A collection of key-value pairs, found by key."),
        ("Key and value", "The key is the label; the value is what it finds."),
        ("Hashable keys", "A key must never change, so lists cannot be keys."),
        ("Insertion order", "Keys stay in the order they were added."),
    ]),
    2: ("Part 2: Reading and changing pairs", "Look at the parts, ask for a key, fill in defaults", [
        ("Keys, values, items", "Three views of the parts of a dictionary."),
        ("in and get()", "Ask whether a key exists without an error."),
        ("setdefault()", "Add a pair only when the key is missing."),
        ("Change a pair", "Assign, del, pop and merge change the contents."),
    ]),
    3: ("Part 3: Programs that count and learn", "A dictionary as the memory of a program", [
        ("birthdays.py", "A program that learns a new pair when asked."),
        ("characterCount.py", "Count every character of a text by key."),
        ("Counter", "One call builds the whole table of counts."),
        ("Grouping", "Lists as values collect items under one key."),
    ]),
    4: ("Part 4: Structuring data", "Model a real thing with dictionaries and lists", [
        ("Data model", "Decide what a real thing must record."),
        ("Chessboard", "Squares are keys and pieces are values."),
        ("Nested records", "A dictionary inside a dictionary holds records."),
        ("Inventory and loot", "Counts per item, built from lists."),
    ]),
    5: ("Part 5: Copies and writing data down", "Keep a copy safe, carry data out, check its shape", [
        ("Alias and copies", "Shallow copies share what is inside them."),
        ("JSON and pprint", "Text carries a dictionary out and back."),
        ("TypedDict", "Names the keys of a record for checkers."),
        ("match patterns", "Test the shape of a dictionary and bind values."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("code", "dict_basics"), ("code", "dict_vs_list"), ("code", "insertion_order"), ("story", "guido"), ("code", "hashable_keys"),
        ("divider", 2), ("analogy", "A2"), ("code", "keys_values_items"), ("code", "key_exists"), ("analogy", "A3"), ("code", "setdefault"), ("code", "change_pairs"), ("code", "views_follow"),
        ("divider", 3), ("analogy", "A4"), ("code", "birthdays"), ("code", "char_count"), ("story", "orwell"), ("code", "counter"), ("code", "grouping"),
        ("divider", 4), ("analogy", "A5"), ("code", "board_model"), ("story", "chess"), ("code", "board_print"), ("code", "chess_moves"), ("code", "validator"),
        ("analogy", "A6"), ("code", "picnic_nested"), ("code", "inventory"), ("code", "loot"),
        ("divider", 5), ("analogy", "A7"), ("code", "copies"), ("code", "json_pprint"), ("story", "json"), ("code", "typed_records"), ("code", "match_dict"),
        ("current",), ("summary",), ("practice",), ("resources",)]
N = len(PLAN)
SLIDE_OF = {}      # ("code", id) -> slide number, ("divider", k) -> slide number
for i, p in enumerate(PLAN, 1):
    SLIDE_OF[p] = i
PLAN = [q for p in PLAN for q in ((("teach", p[1]), p) if p[0] == "code" else (p,))]
N = len(PLAN)
SLIDE_OF = {p: i for i, p in enumerate(PLAN, 1)}
CODE_ORDER = [p[1] for p in PLAN if p[0] == "code"]
assert CODE_ORDER == [e["id"] for e in X.EXAMPLES], "the examples file must list the examples in slide order"


def part_slides(k):
    """slide numbers from divider k up to the slide before divider k+1 (or the changes slide)"""
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
    s = base(prs, "Dictionaries and Structuring Data", None, chip=True, nt=T.NOTES["title"])
    s.shapes[-1].left, s.shapes[-1].top, s.shapes[-1].width, s.shapes[-1].height = Inches(0.6), Inches(1.7), Inches(8.8), Inches(0.9)
    for r in s.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.size = K.Pt(32)
    tb(s, 0.6, 2.65, 8.8, 0.7, "Chapter 7 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course", 16, C["muted"], name="subtitle")
    nconc = len({a for _, _, _, rows in T.ANALOGIES for a, _ in rows})
    for i, (a, b) in enumerate([(str(len(X.EXAMPLES)), "code examples that run on the chapter page"), ("4", "true stories told with real names, dates and places"),
                                (str(nconc), "chapter concepts, each with an everyday picture")]):
        xx = 0.6 + i * 3.0
        rect(s, xx, 3.5, 2.8, 1.15, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, xx + 0.1, 3.55, 2.6, 0.5, a, 28, C["teal"], bold=True, name="stat")
        tb(s, xx + 0.1, 4.05, 2.6, 0.55, b, 11.5, C["ink"], name="stat label")
    tb(s, 0.6, 4.85, 8.0, 0.3, "SEN0414 Advanced Programming, Fall 2026. Yusuf Altunel, İstanbul Kültür Üniversitesi", 11, C["muted"], name="author")
    return s


def make_route(prs):
    s = base(prs, "Today's route", "Five parts; every range is a run of slides you can jump to", nt=T.NOTES["route"])
    rows = [["Part", "Slides", "Code examples", "You will run"]]
    runs = {1: "pairs, equality, order, hashable keys", 2: "keys, values, items, get, setdefault, merge", 3: "birthdays, character count, Counter, grouping",
            4: "chessboard, nesting, inventory, loot", 5: "copies, JSON, TypedDict, match"}
    for k in range(1, 6):
        a, b = part_slides(k)
        nex = sum(1 for p in PLAN[a - 1:b] if p[0] == "code")
        rows.append([PARTS[k][0].split(": ", 1)[1], "%d - %d" % (a, b), str(nex), runs[k]])
    rows.append(["Changes, summary, practice, resources", "%d - %d" % (SLIDE_OF[("current",)], N), "-", "what current Python adds"])
    table(s, 0.5, 1.2, 9.0, rows, [3.0, 1.1, 1.3, 3.8], fs=13.5, rowh=0.55, bold_cols=(0,))
    takeaway(s, "Open the chapter-code tab of the page: the same %d examples, in this order." % len(X.EXAMPLES))
    return s


def make_questions(prs):
    s = base(prs, "The questions this chapter answers", "Carry them through every part; the summary answers each one", nt=T.NOTES["questions"])
    qs = ["Which operations read, add, replace and remove the pairs of a dictionary?",
          "Which values may be keys, and why must a key be hashable?",
          "How are counting, grouping and nesting solved with dictionaries?",
          "How is a real thing modelled, displayed, copied and written down?",
          "Which terms must a learner look up, and what is each one in everyday life?"]
    for i, q in enumerate(qs):
        yy = 1.2 + i * 0.7
        rect(s, 0.5, yy, 9.0, 0.6, C["card"], line=C["line"], radius=0.1, name="card")
        label_shape(s, 0.6, yy + 0.08, 0.44, 0.44, str(i + 1), C["teal"], "FFFFFF", size=15, bold=True)
        tb(s, 1.2, yy, 8.2, 0.6, q, 14, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="question")
    takeaway(s, "The answers come back on slide %d." % SLIDE_OF[("summary",)])
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
        tb(s, 2.85, yy, 3.3, 0.6, mean, 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="meaning")
        yy += 0.72
    a, b = part_slides(k)
    items = []
    for i in range(a + 1, b + 1):
        p = PLAN[i - 1]
        if p[0] == "code":
            items.append((i, X.BY_ID[p[1]]["title"]))
        elif p[0] == "story":
            items.append((i, T.STORIES[p[1]]["title"].replace("Story: ", "Story: ")))
        elif p[0] == "analogy":
            items.append((i, [a_[1] for a_ in T.ANALOGIES if a_[0] == p[1]][0]))
    rows = [["Slide", "In this part"]] + [[str(i), t if len(t) < 46 else t[:43] + "..."] for i, t in items]
    rh = min(0.4, 3.3 / len(rows))
    table(s, 6.3, 1.45, 3.3, rows, [0.65, 3.4], rowh=rh, name="table")
    return s


def make_analogy(prs, aid):
    _, title, head, rows = [a for a in T.ANALOGIES if a[0] == aid][0]
    s = base(prs, title, None, nt=T.NOTES[aid])
    rect(s, 0.4, 0.82, 9.2, 0.62, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.84, 8.9, 0.58, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), (head, {})]], 14, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    rh = min(0.5, 3.45 / (len(rows) + 1))
    table(s, 0.4, 1.52, 9.2, [["Chapter concept", "Everyday picture"]] + [[a, b] for a, b in rows], [3.0, 6.2], fs=12 if len(rows) >= 6 else None, rowh=rh, bold_cols=(0,))
    return s


def make_story(prs, sid):
    st = T.STORIES[sid]
    s = base(prs, st["title"], None, nt=T.STORY_NOTES[sid])
    picture(s, os.path.join(ASSETS, st["img"]), 0.4, 0.95, 2.9, 3.2, "Picture for the story: " + st["title"].replace("Story: ", ""), "photo " + sid)
    tb(s, 0.4, 4.2, 2.9, 0.7, st["credit"], 9.5, C["muted"], name="credit")
    yy = 0.95
    for key in ("p1", "p2", "p3"):
        txt = st[key]
        if "%(" in txt:
            cc = RUN["char_count"][1]["count"]
            txt = txt % {"total": sum(cc.values()), "kinds": len(cc)}
        nlines = math.ceil(len(txt) / 56.0)
        h = max(0.6, nlines * 0.27 + 0.18)
        rect(s, 3.5, yy, 6.1, h, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, 3.58, yy, 5.95, h, txt, 14, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="story")
        yy += h + 0.1
    tb(s, 3.5, yy + 0.02, 6.1, 0.36, [[(st["linktext"], {"link": st["link"], "color": C["teal"], "bold": True})]], 13, C["ink"], name="link")
    return s


def make_teach(prs, exid):
    ex = X.BY_ID[exid]
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


def note_heights(notes, ex_w, nfs):
    cpl = max(8, (ex_w - 0.3) * 72.0 / (0.54 * nfs))
    return [math.ceil(len(n) / cpl) * nfs * 1.25 / 72.0 + 0.2 for n in notes]


def plan_code(ex, visual):
    """One code box on the left, the short explanations stacked beside it, the result visual below the taller of the two.
    The largest code font (14 down to 9 pt) and note font (12.5 down to 10.5 pt) for which everything fits and the visual keeps its room."""
    lines = X.code_lines(ex)
    maxlen = max(len(l) for l in lines) + 1
    top, gap = 0.92, 0.08
    last = None
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
            last = (fs, box_w, box_h, ry, avail, nfs, nh, block)
            if avail >= visual.need:
                return last
    print("WARN %s: no layout leaves %.2f in for the result (wants %.2f)" % (ex["id"], last[4], visual.need))
    return last


def make_code(prs, exid):
    ex = X.BY_ID[exid]
    out, ns = RUN[exid]
    s = base(prs, ex["title"], None, nt=T.EX_NOTES[exid][1])
    visual = V.VISUALS[ex["visual"]]
    fs, box_w, box_h, ry, avail, nfs, nh, block = plan_code(ex, visual)
    code_box(s, 0.4, 0.92, box_w, block, X.code_lines(ex), fs)
    ex_x = 0.4 + box_w + 0.12
    ex_w = 9.6 - ex_x
    gap = 0.08
    spare = (block - sum(nh) - gap * (len(nh) - 1)) / len(nh)
    yy = 0.92
    for note, h in zip(ex["notes"], nh):
        h = h + spare
        rect(s, ex_x, yy, ex_w, h, C["card"], line=C["line"], radius=0.06, name="note card")
        tb(s, ex_x + 0.05, yy, ex_w - 0.1, h, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation")
        yy += h + gap
    tb(s, 0.4, ry, 6.0, 0.26, "What the run printed (Python %s)" % PYV, 11, C["teal"], bold=True, name="result label")
    visual(s, 0.4, ry + 0.3, 9.2, max(avail, 1.0), ns, out)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def make_current(prs):
    s = base(prs, "Current Python adds more", "Features newer than the book, from the chapter research", nt=T.NOTES["current"])
    rows = [["Feature", "Since", "What it gives you"],
            ["Insertion order is a promise", "3.7", "Keys keep the order of adding; the book's no first item is out of date"],
            ["Reversible views, reversed(d)", "3.8", "Walk the newest key first; views show later changes"],
            ["Merge operators | and |=", "3.9", "d1 | d2 builds a new dictionary (PEP 584)"],
            ["match statement with mapping patterns", "3.10", "Test the keys of a dictionary and bind their values (PEP 634)"],
            ["TypedDict names the keys of a record", "3.8", "A type checker enforces it; at run time it is a plain dict (PEP 589)"],
            ["Equal keys must hash alike", "all", "A class with __eq__ but no __hash__ cannot be a key"]]
    table(s, 0.5, 1.25, 9.0, rows, [3.6, 0.8, 4.6], fs=13, rowh=0.56, bold_cols=(0,), mono_cols=(), align_cols={1: PP_ALIGN.CENTER})
    takeaway(s, "Teach the basics from the book and add what Python has learned since.")
    return s


def make_summary(prs):
    s = base(prs, "Summary", None, nt=T.NOTES["summary"])
    rect(s, 0.4, 0.82, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.83, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("A summary is like the last line of a recipe card: what you must remember when the cooking is done.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    pts = ["Assign to add or replace a pair; del and pop remove one; get() helps when a key may be missing.",
           "A key must be hashable: tuples are welcome, lists are not; keys keep their order since Python 3.7.",
           "Counting and grouping use setdefault, Counter or defaultdict; a view follows its dictionary.",
           "A chessboard is a dictionary of occupied squares; a nested dictionary holds a record in a record.",
           "copy.copy() shares the inner dictionaries, deepcopy() does not, and JSON writes the data as text."]
    for i, t in enumerate(pts):
        yy = 1.5 + i * 0.62
        label_shape(s, 0.4, yy + 0.04, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 0.9, yy, 4.6, 0.58, t, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="point")
    kinds = {"Read": ["keys", "values", "items", "get", "pop", "setdefault"], "Test": ["in", "not in", "==", "is"],
             "Change": ["pop", "update", "clear", "copy", "popitem"]}
    for nm in [n for v in kinds.values() for n in v if n.isidentifier() and n not in ("in", "is")]:
        assert hasattr(dict, nm), nm
    tb(s, 5.7, 1.4, 3.9, 0.5, "Dictionary tools in this chapter, by what they do", 10.5, C["teal"], bold=True, name="chart label")
    chart(s, "col", 5.6, 1.95, 4.0, 3.0, list(kinds), [("tools", [len(v) for v in kinds.values()])], fs=10, legend=False, gap=50, vmax=8)
    takeaway(s, "A key finds its value, and the order of adding is kept.")
    return s


def make_practice(prs):
    s = base(prs, "Practice questions", "Predict first, then run it on the chapter page", nt=T.NOTES["practice"])
    rect(s, 0.4, 0.95, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.96, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("Practice questions are like finger scales for a pianist: short drills before the performance.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    qs = ["What does the code for an empty dictionary look like?",
          "What is the main difference between a dictionary and a list?",
          "What happens if you try spam['foo'] when spam is {'bar': 100}?",
          "What is the difference between 'cat' in spam and 'cat' in spam.keys()?"]
    for i, q in enumerate(qs):
        yy = 1.6 + i * 0.62
        rect(s, 0.4, yy, 4.9, 0.54, C["card"], line=C["line"], radius=0.08, name="card")
        label_shape(s, 0.5, yy + 0.07, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 1.0, yy, 4.25, 0.54, q, 11, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="question")
    tb(s, 5.55, 1.55, 4.0, 0.3, "Practice programs", 13, C["teal"], bold=True, name="column head")
    progs = [("Chess Dictionary Validator", "Check that a board dictionary is a legal position."), ("Fantasy Game Inventory", "Display an inventory and add up its items."),
             ("List-to-Dictionary Loot Conversion", "Add a list of loot into the inventory.")]
    for i, (nm, what) in enumerate(progs):
        yy = 1.9 + i * 0.8
        rect(s, 5.55, yy, 4.05, 0.72, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, 5.65, yy + 0.02, 3.9, 0.68, [[(nm, {"bold": True})], [(what, {"size": 10.5})]], 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="program")
    takeaway(s, "Each answer fits in a few lines you can run.")
    return s


def make_resources(prs):
    s = base(prs, "Resources: where to go next", "Reading and watching, chosen for this chapter; every link is live", nt=T.NOTES["resources"])
    for i, (t, url, host) in enumerate(T.RESOURCES):
        col, row = divmod(i, 6)
        xx = 0.4 + col * 4.7
        yy = 1.2 + row * 0.66
        rect(s, xx, yy, 4.5, 0.58, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, xx + 0.08, yy + 0.02, 4.35, 0.54, [[(t, {"bold": True})], [(url if len(url) < 58 else host, {"link": url, "color": C["teal"], "size": 9.5})]], 11, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="resource")
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
    prs.core_properties.title = "SEN0414 Chapter 7: Dictionaries and Structuring Data (lecture deck 2.1.0)"
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
    man = {"chapter": 7, "version": "1.1.0", "kind": "chapter-code manifest",
           "deck": os.path.relpath(OUT_DECK, ROOT).replace(os.sep, "/"),
           "about": "The code examples of the chapter 7 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                    "every example is self-contained and runs with the Python standard library only; the expected result is what the run printed. The code is exactly the text of the "
                    "deck's code boxes: indented per the Python standard, no prompt, no lambda.",
           "executed_with": {"python": PYV, "library": None},
           "library": {"file": None, "sha256": None, "data_files": [], "page_requirements": ["the Python standard library: collections (Counter, defaultdict), copy, json, pprint, typing (TypedDict), types (MappingProxyType)", "the match statement (Python 3.10 or later)", "no keyboard input: birthdays.py is scripted with an iterator"]},
           "prelude": "",
           "examples": exs}
    os.makedirs(os.path.dirname(OUT_MAN), exist_ok=True)
    with open(OUT_MAN, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=1)
        f.write("\n")


if __name__ == "__main__":
    if MANIFEST_ONLY:
        write_manifest()
        print("manifest only:", OUT_MAN)
        sys.exit(0)
    n = build()
    write_manifest()
    print("deck %s | %d slides | %d code examples | manifest %s" % (os.path.relpath(OUT_DECK, ROOT), n, len(X.EXAMPLES), os.path.relpath(OUT_MAN, ROOT)))
