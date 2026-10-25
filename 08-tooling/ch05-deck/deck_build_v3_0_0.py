#!/usr/bin/env python3
"""Builds the chapter 5 lecture deck 3.0.0 (Debugging) on the deck standard, and its chapter-code manifest.

A NEW tool (the decks of 1.0.0 to 2.0.0 and their builders stay untouched). Every code example of examples_v3_0_0.py is RUN here, each in a
fresh interpreter for the manifest's expected result and once in this process for the namespace the result visuals read; the two printed
results must be equal, and every number in a result visual comes from that run. One light background scheme, a number on every slide, a chip
'>>>' on every slide that is not a divider, native tables and charts, drawn diagrams with arrows.
Writes: 03-materials/ch05/SEN0414_Ch05_Debugging_3e_v3_0_0.pptx
        03-materials/ch05/page/chapter_code_ch05_v1_0_0.json   (order = slide order; the code exactly as the code boxes show it)
Usage:  python3 deck_build_v3_0_0.py
"""
__version__ = "3.0.0"
import contextlib
import io
import json
import logging
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
import deck_kit_v3_0_0 as K
from deck_kit_v3_0_0 import C, MONO, arrow, chart, code_box, label_shape, new_deck, new_slide, notes, picture, rect, table, tb
X = load("examples_v3_0_0", "examples_v3_0_0.py")
V = load("deck_visuals_v3_0_0", "deck_visuals_v3_0_0.py")
T = load("deck_content_v3_0_0", "deck_content_v3_0_0.py")

OUT_DECK = os.path.join(ROOT, "03-materials", "ch05", "SEN0414_Ch05_Debugging_3e_v3_0_0.pptx")
OUT_MAN = os.path.join(ROOT, "03-materials", "ch05", "page", "chapter_code_ch05_v1_0_0.json")
ASSETS = os.path.join(ROOT, "03-materials", "ch05", "assets")
PYV = platform.python_version()


# ------------------------------------------------------------------ run every example
def reset_logging():
    root = logging.getLogger()
    for h in list(root.handlers):
        root.removeHandler(h)
        h.close()
    root.setLevel(logging.WARNING)
    logging.disable(logging.NOTSET)


def run_fresh(ex):
    """the result the manifest records: the example alone, in a fresh isolated interpreter (what the page does with it)"""
    r = subprocess.run([sys.executable, "-I", "-c", X.code_text(ex)], capture_output=True, text=True, timeout=60, cwd=tempfile.mkdtemp())
    if r.returncode != 0:
        raise SystemExit("REFUSED: example %s failed in a fresh interpreter: %s" % (ex["id"], r.stderr[-300:]))
    return r.stdout


def run_here(ex):
    """the same code in this process, for the namespace the result visual reads"""
    reset_logging()
    buf = io.StringIO()
    ns = {}
    with contextlib.redirect_stdout(buf):
        exec(compile(X.code_text(ex), "<%s>" % ex["id"], "exec"), ns)
    reset_logging()
    return buf.getvalue(), ns


RUN = {}
for _ex in X.EXAMPLES:
    _fresh = run_fresh(_ex)
    _here, _ns = run_here(_ex)
    assert _fresh == _here, "example %s printed different results in a fresh interpreter and in the builder: %r vs %r" % (_ex["id"], _fresh, _here)
    RUN[_ex["id"]] = (_fresh, _ns)

# ------------------------------------------------------------------ the plan: slide kinds in order
PARTS = {
    1: ("Part 1: Exceptions and tracebacks", "A function refuses a bad call; the exception climbs; the traceback tells the way", [
        ("Raising Exceptions", "A function refuses a call it cannot serve by raising an exception."),
        ("Exception object", "Carries its class, its arguments and the message you gave it."),
        ("traceback", "The report of the calls an exception passed on its way up."),
        ("Notes", "Context that an except clause adds before it raises again."),
    ]),
    2: ("Part 2: Assertions", "Executable beliefs of the programmer, not checks on the user", [
        ("assert", "A statement that raises AssertionError when its condition is false."),
        ("Message", "The second expression explains the failure and is built only on failure."),
        ("User or bug?", "Errors of the user are raised; errors of the programmer are asserted."),
        ("python -O", "Optimised runs remove every assert statement from the program."),
    ]),
    3: ("Part 3: Logging", "A record of what the program did, without stopping it", [
        ("Levels", "Five names from DEBUG to CRITICAL, with the numbers 10 to 50."),
        ("basicConfig", "One call sets the threshold, the format and the destination."),
        ("filename", "Sends the log to a text file instead of the screen."),
        ("disable", "Silences logging up to a level without deleting any call."),
    ]),
    4: ("Part 4: Hunting bugs with the log", "Three small mistakes, each found by reading evidence", [
        ("Off by one", "A loop that starts at zero multiplies everything by zero."),
        ("Text, not number", "input() returns strings, and plus joins strings."),
        ("Type mismatch", "A number never equals a text, so the comparison always fails."),
        ("Log as proof", "The same log that finds a bug also proves the fix."),
    ]),
    5: ("Part 5: The debugger", "Pause the program, look at its variables, step through the lines", [
        ("Breakpoint", "A line at which the debugger pauses the running program."),
        ("Inspector pane", "Shows the values of the variables while the program is paused."),
        ("Step controls", "Step In, Step Over and Step Out move through the code."),
        ("pdb", "The standard debugger, started by the call breakpoint()."),
    ]),
}

PLAN = [("title",), ("route",), ("questions",),
        ("divider", 1), ("analogy", "A1"), ("story", "moth"), ("code", "boxprint"), ("code", "exceptionobj"), ("code", "unwinding"), ("code", "notes"),
        ("divider", 2), ("analogy", "A2"), ("code", "assertfails"), ("code", "assertmsg"), ("code", "optimised"),
        ("divider", 3), ("analogy", "A3"), ("story", "kernighan"), ("story", "pep282"), ("code", "levels"), ("code", "threshold"), ("code", "format"),
        ("code", "tofile"), ("code", "disable"), ("code", "lazy"),
        ("divider", 4), ("analogy", "A4"), ("code", "factorialbug"), ("code", "factorialfix"), ("code", "addingbug"), ("code", "cointossbug"), ("code", "cointossfix"),
        ("divider", 5), ("analogy", "A5"), ("analogy", "A6"), ("controls",), ("code", "stepper"), ("code", "breakpointfn"),
        ("instruments",), ("current",), ("summary",), ("practice",), ("resources",)]
N = len(PLAN)
NCONCEPTS = sum(len(a_[3]) for a_ in T.ANALOGIES) + 1          # the analogy rows, plus 'Practice Questions' on the practice slide
SLIDE_OF = {}      # ("code", id) -> slide number, ("divider", k) -> slide number
for i, p in enumerate(PLAN, 1):
    SLIDE_OF[p] = i
CODE_ORDER = [p[1] for p in PLAN if p[0] == "code"]
assert CODE_ORDER == [e["id"] for e in X.EXAMPLES], "the examples file must list the examples in slide order"


def part_slides(k):
    """slide numbers from divider k up to the slide before divider k+1 (or the instruments slide)"""
    a = SLIDE_OF[("divider", k)]
    b = SLIDE_OF[("divider", k + 1)] - 1 if k < 5 else SLIDE_OF[("instruments",)] - 1
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
    s = base(prs, "Debugging", None, chip=True, nt=T.NOTES["title"])
    s.shapes[-1].left, s.shapes[-1].top, s.shapes[-1].width, s.shapes[-1].height = Inches(0.6), Inches(1.7), Inches(8.8), Inches(0.9)
    for r in s.shapes[-1].text_frame.paragraphs[0].runs:
        r.font.size = K.Pt(38)
    tb(s, 0.6, 2.65, 8.8, 0.7, "Chapter 5 of Automate the Boring Stuff with Python, 3rd edition, for an advanced course", 16, C["muted"], name="subtitle")
    for i, (a, b) in enumerate([(str(len(X.EXAMPLES)), "code examples that run on the chapter page"), (str(len(T.STORIES)), "true stories with who, what, when, where, why and how"), (str(NCONCEPTS), "chapter concepts, each with an everyday picture")]):
        xx = 0.6 + i * 3.0
        rect(s, xx, 3.5, 2.8, 1.15, C["card"], line=C["line"], radius=0.08, name="card")
        tb(s, xx + 0.1, 3.55, 2.6, 0.5, a, 28, C["teal"], bold=True, name="stat")
        tb(s, xx + 0.1, 4.05, 2.6, 0.55, b, 11.5, C["ink"], name="stat label")
    tb(s, 0.6, 4.85, 8.0, 0.3, "SEN0414 Advanced Programming, Fall 2026. Yusuf Altunel, İstanbul Kültür Üniversitesi", 11, C["muted"], name="author")
    return s


def make_route(prs):
    s = base(prs, "Today's route", "Five parts; every range is a run of slides you can jump to", nt=T.NOTES["route"])
    rows = [["Part", "Slides", "Code examples", "You will run"]]
    runs = {1: "raise, except, traceback, notes", 2: "assert, messages, python -O", 3: "levels, basicConfig, file, disable",
            4: "factorial, string sum, coin toss", 5: "a line stepper, breakpoint(), pdb"}
    for k in range(1, 6):
        a, b = part_slides(k)
        nex = sum(1 for p in PLAN[a - 1:b] if p[0] == "code")
        rows.append([PARTS[k][0].split(": ", 1)[1], "%d - %d" % (a, b), str(nex), runs[k]])
    rows.append(["Instruments, changes, summary, practice, resources", "%d - %d" % (SLIDE_OF[("instruments",)], N), "-", "which tool for which question"])
    table(s, 0.5, 1.2, 9.0, rows, [3.6, 1.1, 1.3, 3.2], fs=13, rowh=0.55, bold_cols=(0,))
    takeaway(s, "Open the chapter-code tab of the page: the same %d examples, in this order." % len(X.EXAMPLES))
    return s


def make_questions(prs):
    s = base(prs, "Two questions this chapter answers", "Carry them through every part; the answers come back at the end", nt=T.NOTES["questions"])
    q = [("1", "Which constructs signal, check, record and inspect a program's behaviour, and what decides which one a problem calls for?",
          "Answer on slide %d: four instruments, chosen by the question you ask." % SLIDE_OF[("instruments",)]),
         ("2", "Which printed outputs and concepts of the chapter differ in current Python, and on what source?",
          "Answer on slide %d: notes, error locations and the attach of Python 3.14." % SLIDE_OF[("current",)])]
    for i, (n, qq, aa) in enumerate(q):
        yy = 1.3 + i * 1.75
        rect(s, 0.5, yy, 9.0, 1.55, C["card"], line=C["line"], radius=0.05, name="card")
        label_shape(s, 0.7, yy + 0.2, 0.5, 0.5, n, C["teal"], "FFFFFF", size=18, bold=True)
        tb(s, 1.4, yy + 0.12, 7.9, 0.75, qq, 15, C["ink"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="question")
        tb(s, 1.4, yy + 0.95, 7.9, 0.45, aa, 12.5, C["teal"], anchor=MSO_ANCHOR.MIDDLE, name="answer")
    takeaway(s, "Raise, assert, log, step: four instruments for four questions.")
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
        elif p[0] == "controls":
            items.append((i, "The controls of the debugger"))
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
    yy = 0.92
    fs = 12.5
    for lab in ("who", "what", "when", "where", "why", "how"):
        txt = st[lab]
        nlines = math.ceil((len(txt) + 7) / 64.0)
        h = max(0.44, nlines * 0.225 + 0.14)
        rect(s, 3.5, yy, 6.1, h, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, 3.55, yy, 6.0, h, [[(lab.upper() + "  ", {"bold": True, "color": C["teal"]}), (txt, {})]], fs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name=lab)
        yy += h + 0.06
    tb(s, 3.5, yy + 0.02, 6.1, 0.36, [[("READ  ", {"bold": True, "color": C["amber"]}), (st["linktext"], {"link": st["link"], "color": C["teal"]})]], fs, C["ink"], name="read")
    if yy + 0.4 > 5.15:
        print("WARN story %s: the cards end at %.2f in" % (sid, yy + 0.4))
    return s


def chunks(lines, limit=28):
    """split the lines of a group into code boxes of at most `limit` words (the deck standard allows 30 words in a text box; every line carries its '>>>' prompt as one word)"""
    out, cur, n = [], [], 0
    for l in lines:
        w = 1 + len(l.split())
        if cur and n + w > limit:
            out.append(cur); cur, n = [], 0
        cur.append(l); n += w
    if cur:
        out.append(cur)
    return out


def code_height(g, lh):
    cs = chunks(g)
    return sum(len(c) * lh + 0.16 for c in cs) + 0.03 * (len(cs) - 1)


def plan_code(ex, visual):
    """Choose layout and font: the largest code font (14 down to 9 pt) for which the code, its explanations and the result visual all fit.
    Layout 'side': the explanation stands right of each code box (needs a code box of at most 6.4 in); layout 'below': under each code box;
    layout 'left': the code and its explanations in a left column and the result visual in a right column (stepper only).
    The largest code font (12 down to 9 pt) for which the result visual still fits; at each size side before below."""
    maxlen = max(len(l) for l in X.code_lines(ex)) + 4
    top, gapv = 0.85, 0.06
    last = None
    if ex.get("layout") == "left":
        for fs in (10.5, 10, 9.5, 9):
            need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
            if need_w > 5.7:
                continue
            box_w = max(3.4, need_w)
            nfs = 11 if fs >= 10 else 10.5
            lh = fs * 1.22 / 72.0
            cpl = max(10, (box_w - 0.3) * 72.0 / (0.5 * nfs))
            rows = []
            for g, note in ex["groups"]:
                rows.append((code_height(g, lh), math.ceil(len(note) / cpl) * nfs * 1.25 / 72.0 + 0.14))
            total = sum(a + b for a, b in rows) + gapv * (len(rows) - 1)
            last = ("left", fs, nfs, box_w, box_w, rows, [a + b for a, b in rows], top + total, 5.04 - (top + total))
            if top + total <= 5.1:
                return last
        if last is None:
            raise SystemExit("REFUSED: %s has no 'left' layout in which its longest code line fits" % ex["id"])
        print("WARN %s: the left column ends at %.2f in" % (ex["id"], last[7]))
        return last
    cands = [(lay, fs) for fs in (12, 11, 10.5, 10, 9.5, 9) for lay in ("side", "below")]
    best = None
    for lay, fs in cands:
        need_w = (maxlen * 0.6 * fs + 14.4) / 72.0 + 0.08
        if lay == "side":
            box_w = max(3.2, need_w)
            if box_w > 6.4:
                continue
            expl_w = 9.2 - box_w + 0.02
        else:
            box_w, expl_w = 9.2, 9.2
            if need_w > 9.2:
                continue
        nfs = 12 if fs >= 12 else (11.5 if fs >= 11 else (11 if fs >= 10 else 10.5))
        lh = fs * 1.22 / 72.0
        cpl = max(10, (expl_w - 0.3) * 72.0 / (0.5 * nfs))
        rows = []
        for g, note in ex["groups"]:
            code_h = code_height(g, lh)
            n_h = math.ceil(len(note) / cpl) * nfs * 1.25 / 72.0 + 0.14
            rows.append((code_h, n_h))
        heights = [max(a, b, 0.42) for a, b in rows] if lay == "side" else [a + b for a, b in rows]
        total = sum(heights) + gapv * (len(heights) - 1)
        ry = top + total + 0.05
        avail = 5.1 - (ry + 0.25)
        last = (lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail)
        if best is None or avail > best[-1]:
            best = last
        if avail >= visual.need:
            return last
    if best is None:
        raise SystemExit("REFUSED: %s has no layout in which its longest code line fits the slide" % ex["id"])
    print("WARN %s: no layout leaves %.2f in for the result (wants %.2f); best is %s at %s pt" % (ex["id"], best[-1], visual.need, best[0], best[1]))
    return best


def make_code(prs, exid):
    ex = X.BY_ID[exid]
    out, ns = RUN[exid]
    s = base(prs, ex["title"], None, nt=T.NOTES[exid])
    visual = V.VISUALS[ex["visual"]]
    lay, fs, nfs, box_w, expl_w, rows, heights, ry, avail = plan_code(ex, visual)
    print("LAYOUT %-13s %-5s code %4.1f pt, visual room %.2f in (wants %.2f)" % (exid, lay, fs, avail, visual.need))
    y, gapv = 0.85, 0.06
    lh = fs * 1.22 / 72.0
    for (g, note), (ch_, nh_), hh in zip(ex["groups"], rows, heights):
        yy = y
        for c in chunks(g):
            hc = len(c) * lh + 0.16
            code_box(s, 0.4, yy, box_w, hc, c, fs)
            yy += hc + 0.03
        if lay == "side":
            tb(s, 0.4 + box_w - 0.02, y, expl_w, hh, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.14, 0.02))
        else:
            tb(s, 0.4, y + ch_ + 0.01, box_w, nh_, note, nfs, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="explanation", margin=(0.12, 0.02))
        y += hh + gapv
    if lay == "left":
        vx = 0.4 + box_w + 0.25
        tb(s, vx, 0.85, 9.6 - vx, 0.26, "What the run printed (Python %s)" % PYV, 11, C["teal"], bold=True, name="result label")
        visual(s, vx, 1.18, 9.6 - vx, 3.8, ns, out)
    else:
        tb(s, 0.4, ry, 6.0, 0.22, "What the run printed (Python %s)" % PYV, 10.5, C["teal"], bold=True, name="result label")
        visual(s, 0.4, ry + 0.25, 9.2, max(avail, 1.0), ns, out)
    takeaway(s, T.TAKEAWAY[exid])
    return s


def make_controls(prs):
    s = base(prs, "The controls of the debugger", "From the line x = add(2, 3), with a breakpoint on it", nt=T.NOTES["controls"])
    rows = [["Control", "What it does", "Pauses next at"],
            ["Continue", "Runs to the next breakpoint, or to the end", "the next red dot"],
            ["Step In", "Runs the line; enters a function it calls", "total = a + b"],
            ["Step Over", "Runs the line as a whole, calls included", "return add(x, 10)"],
            ["Step Out", "Runs the rest of this function, then pauses", "back in main"],
            ["Stop", "Ends the program at once", "nowhere"]]
    table(s, 0.4, 1.15, 5.0, rows, [1.0, 2.5, 1.5], fs=10.5, rowh=0.6, mono_cols=(2,), bold_cols=(0,))
    bx = 5.75
    label_shape(s, bx - 0.28, 1.28, 0.22, 0.22, "", C["coral"], C["ink"], size=6, radius=0.5)
    V.chip(s, bx, 1.2, 3.4, 0.38, "main:  x = add(2, 3)", "amber", fs=10.5)
    V.chip(s, bx, 2.15, 2.9, 0.38, "main:  return add(x, 10)", "teal", fs=10)
    V.chip(s, bx + 0.45, 3.1, 2.45, 0.38, "add:  total = a + b", "teal", fs=10)
    V.chip(s, bx + 0.45, 3.75, 2.45, 0.38, "add:  return total", "plain", fs=10)
    arrow(s, bx + 0.2, 1.6, bx + 0.2, 2.13, C["green"], 2.0)
    tb(s, bx + 0.3, 1.66, 1.0, 0.42, "Step Over", 10, C["green"], bold=True, anchor=MSO_ANCHOR.MIDDLE, name="label step over")
    arrow(s, bx + 3.0, 1.6, bx + 2.97, 3.3, C["teal"], 2.0)
    tb(s, bx + 3.1, 2.3, 0.75, 0.3, "Step In", 10, C["teal"], bold=True, name="label step in")
    arrow(s, bx + 0.5, 4.15, bx + 0.2, 2.55, C["coral"], 2.0)
    tb(s, bx - 0.33, 3.2, 0.8, 0.3, "Step Out", 10, C["coral"], bold=True, name="label step out")
    takeaway(s, "Step In enters, Step Over skips, Step Out leaves.")
    return s


def make_instruments(prs):
    s = base(prs, "Choose the instrument by the question", "Four instruments; each answers a different question", nt=T.NOTES["instruments"])
    rows = [["The question", "The instrument", "Everyday picture", "Seen on slides"],
            ["Can the caller do something about it?", "raise and except", "a fire alarm", "%d - %d" % (SLIDE_OF[("code", "boxprint")], SLIDE_OF[("code", "notes")])],
            ["Must this always be true, if my code is right?", "assert", "a tripwire", "%d - %d" % (SLIDE_OF[("code", "assertfails")], SLIDE_OF[("code", "optimised")])],
            ["What happened while the program ran?", "logging", "a logbook", "%d - %d" % (SLIDE_OF[("code", "levels")], SLIDE_OF[("code", "lazy")])],
            ["What is the state at this one line?", "the debugger", "a pause button", "%d - %d" % (SLIDE_OF[("controls",)], SLIDE_OF[("code", "breakpointfn")])]]
    table(s, 0.4, 1.2, 9.2, rows, [3.6, 1.9, 1.9, 1.5], fs=12, rowh=0.7, bold_cols=(1,), align_cols={3: PP_ALIGN.CENTER})
    takeaway(s, "Raise for the user, assert for the programmer, log for the record, step for the state.")
    return s


def make_current(prs):
    s = base(prs, "Current Python adds more", "Features newer than the book, from the chapter research", nt=T.NOTES["current"])
    rows = [["Feature", "Since", "What it gives you"],
            ["add_note and __notes__ on every exception", "3.11", "Context travels with the error and is printed after it"],
            ["Tracebacks mark the failing part of a line", "3.11", "A chained lookup shows which subscript failed"],
            ["basicConfig(force=True)", "3.8", "Replaces a set-up that already exists"],
            ["breakpoint() and PYTHONBREAKPOINT", "3.7", "One call starts the debugger; 0 switches it off"],
            ["python -m pdb -p PID", "3.14", "Attach the debugger to a running process"],
            ["assert is removed under -O", "all", "A check the program needs is never an assert"]]
    table(s, 0.5, 1.25, 9.0, rows, [3.8, 0.8, 4.4], rowh=0.55, bold_cols=(0,), align_cols={1: PP_ALIGN.CENTER})
    takeaway(s, "Run what the book printed; then check what changed.")
    return s


def make_summary(prs):
    s = base(prs, "Summary", None, nt=T.NOTES["summary"])
    rect(s, 0.4, 0.82, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 0.83, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("A summary is a packing list: only what you really need goes into the bag.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    pts = ["raise stops a function and tells the caller why; the traceback shows the way.",
           "assert states what must be true; python -O removes it.",
           "Logging has five levels, a format and a destination, and it can be switched off.",
           "The log is evidence: it finds a bug and proves the fix.",
           "A debugger pauses the program and shows its variables."]
    for i, t_ in enumerate(pts):
        yy = 1.5 + i * 0.62
        label_shape(s, 0.4, yy + 0.04, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 0.9, yy, 4.6, 0.52, t_, 11.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="point")
    per = [sum(1 for e in X.EXAMPLES if e["part"] == k) for k in range(1, 6)]
    tb(s, 5.7, 1.4, 3.9, 0.5, "code examples per part of the chapter", 10.5, C["teal"], bold=True, name="chart label")
    chart(s, "col", 5.6, 1.95, 4.0, 3.0, ["Raise", "Assert", "Log", "Hunt", "Debug"], [("examples", per)], fs=10, legend=False, gap=50, vmax=8, major=2)
    takeaway(s, "Four instruments, four questions.")
    return s


def make_practice(prs):
    s = base(prs, "Practice Questions", "Predict first, then run it on the chapter page", nt=T.NOTES["practice"])
    rect(s, 0.4, 1.05, 9.2, 0.5, C["amberLight"], radius=0.08, name="card")
    tb(s, 0.55, 1.06, 8.9, 0.48, [[("ANALOGY  ", {"bold": True, "color": C["amber"]}), ("Practice questions are finger scales for a pianist: short drills before the performance.", {})]], 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="analogy")
    qs = ["Why does factorial(3) print 0 when the loop is range(n + 1)? Change one character to fix it.",
          "What is the difference between raise and assert? Which one checks a value typed by a user?",
          "Your DEBUG lines show on the screen but the log file stays empty. Which basicConfig arguments decide this?",
          "How do you silence all logging at once without deleting a single logging call?"]
    for i, q in enumerate(qs):
        yy = 1.8 + i * 0.8
        rect(s, 0.4, yy, 9.2, 0.68, C["card"], line=C["line"], radius=0.08, name="card")
        label_shape(s, 0.55, yy + 0.14, 0.4, 0.4, str(i + 1), C["teal"], "FFFFFF", size=13, bold=True)
        tb(s, 1.1, yy + 0.04, 8.4, 0.6, q, 13, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="question")
    takeaway(s, "Each answer fits in one line you can run.")
    return s


def make_resources(prs):
    s = base(prs, "Resources: where to go next", "Reading and history, chosen for this chapter; every link is live", nt=T.NOTES["resources"])
    for i, (t, url, host) in enumerate(T.RESOURCES):
        col, row = divmod(i, 7)
        xx = 0.4 + col * 4.7
        yy = 1.1 + row * 0.57
        rect(s, xx, yy, 4.5, 0.5, C["card"], line=C["line"], radius=0.1, name="card")
        tb(s, xx + 0.08, yy + 0.01, 4.35, 0.48, [[(t, {"bold": True})], [(url if len(url) < 58 else host, {"link": url, "color": C["teal"], "size": 9})]], 10.5, C["ink"], anchor=MSO_ANCHOR.MIDDLE, name="resource")
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
        elif kind == "controls":
            make_controls(prs)
        elif kind == "instruments":
            make_instruments(prs)
        elif kind == "current":
            make_current(prs)
        elif kind == "summary":
            make_summary(prs)
        elif kind == "practice":
            make_practice(prs)
        elif kind == "resources":
            make_resources(prs)
    add_numbers(prs)
    prs.core_properties.title = "SEN0414 Chapter 5: Debugging (lecture deck 3.0.0)"
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
    man = {"chapter": 5, "version": "1.0.0", "kind": "chapter-code manifest",
           "deck": os.path.relpath(OUT_DECK, ROOT).replace(os.sep, "/"),
           "about": "The code examples of the chapter 5 deck, in the order of the code slides (order = slide order). The page's chapter-code tab lists them by NAME in this order; "
                    "every example is self-contained and runs with the Python standard library only, reads no keyboard (input() is scripted with an iterator) and prints its result; "
                    "the expected result is what the run printed in a fresh interpreter. The code is exactly the text of the deck's code boxes with the '>>> ' prompt removed. "
                    "Every example that sets up logging passes force=True, so it behaves the same after another example has run on the page.",
           "executed_with": {"python": PYV, "library": None},
           "library": {"file": None, "sha256": None, "data_files": [], "page_requirements": [
               "The Python standard library modules logging, traceback, sys, os, tempfile, time, random and pdb (import pdb only reads the class names), and the built-ins print, repr, int, sum, iter, next, isinstance, issubclass, hasattr, getattr, dict, type",
               "sys.settrace for the line stepper (the stepper example), and a writable temporary folder for the log file (the filename example)"]},
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
