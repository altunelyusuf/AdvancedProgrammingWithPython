#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 21 (Making Graphs and Manipulating Images) on the CME classroom standard.

Same regime as chapters 10 to 20: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources, full-sentence takeaway
strips, stories with fact rows, consoles and whole programs (or honest excerpts of them, labelled with their line numbers) with their results as Python
printed them. Every console result and program transcript comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with
Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4 and pyperclipimg 0.2.0); the speaker notes are prose for the reader and carry only what the chapter's RDODI
research package (03-materials/ch21/rdodi, sen0414_ch21_rdodi_data_v1_0_2.py, findings F1 to F16), its records (08-tooling/ch21-page/*.json) or a program of
this deck established.

What this chapter adds against chapter 20: THE OUTPUTS ARE PICTURES. Sixteen pictures that programs saved (matplotlib graphs, Pillow drawings, the book's cat
photograph cropped, tiled, rotated and given a logo) are placed on the slides as images. Each picture is made by a program of the deck; a caption on its slide
names it ('image <file> made by <program>'); program_check_v1_0_0.py runs that program again and requires the slide to carry a picture byte-identical (or
pixel-identical) to what the program saves now, and the transcript of every picture's program prints the SHA-256 of the file. Twelve corpus programs and fifteen
programs written for the deck were run for real; the four that need the book's files download the publisher's zip and check every file against its SHA-256.
One program, the clipboard, runs on a virtual X display (Xvfb) with the real xclip, a local stand-in for a screen where nobody sees the picture; its slide says
so with the words honesty_check_v1_0_0.py requires ('Virtual display', 'local stand-in'). What the research recorded on 13 October 2026 and the deck does not run
again is on a slide as 'Recorded'. What could not be run is marked NOT EXECUTED on its slide (see the plan's meta.notExecuted). The eight narrative diagrams of
the chapter (sen0414_ch21_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py) and checked by diagram_check_v1_0_0.py; two
tables (the same probe run under four interpreters at check time, and the Pillow releases of the research) and one chart (kilobytes of the cat picture as PNG and as
JPEG) are native PowerPoint objects whose data the deck check computes again; no photograph of a person is used and the study's stories carry none (the single request
to Wikimedia Commons answered 429); four of the six stories are on slides and two (PNG and JPEG) are told in the notes of the saving slide.

Usage: python3 deck_build_v1_0_0.py   (writes deck_plan_v1_0_0.json and links_v1_0_0.json beside itself; needs rdflib)
"""
__version__ = "1.0.0"
import importlib.util
import json
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import diagram_shapes_v1_0_0 as DS


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ST = load("stories21", os.path.join(HERE, "..", "sen0414_ch21_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams21", os.path.join(HERE, "..", "sen0414_ch21_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi21", os.path.join(HERE, "..", "sen0414_ch21_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s; no row reads the clock or the network" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
IMGDIR = os.path.join(HERE, "images")
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

# the honesty lines (honesty_check_v1_0_0.py requires 'NOT EXECUTED' on every slide the plan lists and on no other, 'Recorded' likewise,
# and on every slide that shows the clipboard program the words the recording holds for it ('Virtual display'), besides 'local stand-in')
L_NOTEXEC = "NOT EXECUTED"
L_REC = "Recorded"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


USED = set()
ROWS_SHOWN = sum(len(G[g]) for g in G)


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
    USED.add(group)
    """A console panel sized from its rows; returns (item, bottom y)."""
    rr = rows if rows is not None else G[group]
    maxlen = max(max(len(st) + 4, len(out)) for st, out in rr)
    fs = min(fs, round((w - 0.4) / (maxlen * CW), 1))
    capt = CAP if w >= 3.9 else "run under Python %s; no clock, no network" % PYV
    if fs < 7:
        raise SystemExit("REFUSED: console %s cannot fit unwrapped in %.1f in (fs %.1f)" % (group, w, fs))
    L = lines_of(rr)
    h = round(L * fs * 1.23 / 72.0 + 0.36 + 0.02 * max(0, L - 1), 2)
    it = {"t": "code", "x": x, "y": y, "w": w, "h": h, "rows": rr, "fs": fs}
    if cap:
        it["cap"] = capt
    if label:
        if len(label) > (w - 0.1) / 0.0725:
            raise SystemExit("REFUSED: label %r is too long for a %.1f in panel" % (label, w))
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def span(pname, first, last=None, after=None):
    """1-based line numbers (a, b) of the program lines from the first containing `first` to the first containing `last`."""
    ls = PROGS[pname]["code"].rstrip("\n").split("\n")
    a = next(i for i, l in enumerate(ls, 1) if first in l)
    b = len(ls) if last is None else next(i for i, l in enumerate(ls, 1) if i >= a and last in l)
    return a, b


def pw(pname, lines=None, out=True, fs=7.0):
    """The panel width a program excerpt (and, when asked, its transcript inside the panel) needs at fs points."""
    pr = PROGS[pname]
    L = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(L)) if lines is None else lines
    ws = [len(l) for l in L[a - 1:b]]
    if out and pr["transcript"]:
        t = pr["transcript"].split("\n")
        ws += [len(t[0]) + 7] + [len(x) for x in t[1:]]
    return round(max(ws) * CW * fs + 0.4, 2)


def bestfs(pname, lines, wmax, hmax, out=True, lo=7.0, hi=9.5):
    """The largest font size (a multiple of 0.5 between lo and hi) at which an excerpt and its transcript fit unwrapped in wmax inches
    and hmax inches; the slide then uses it, so that a program is as large as its slide allows."""
    pr = PROGS[pname]
    a, b = lines
    n = (b - a + 1) + (pr["transcript"].count("\n") + 1 if out and pr["transcript"] else 0)
    fs = hi
    while fs >= lo:
        if pw(pname, lines, out, fs) <= wmax and n * (fs * 1.22 / 72.0 + 0.02) + 0.30 <= hmax:
            return fs
        fs -= 0.5
    raise SystemExit("REFUSED: %s lines %d-%d (%d lines with the transcript) do not fit %.2f x %.2f in at %.1f pt (width needs %.2f, height needs %.2f)"
                     % (pname, a, b, n, wmax, hmax, lo, pw(pname, lines, out, lo), n * (lo * 1.22 / 72.0 + 0.02) + 0.30))


def prog(pname, x, y, w, fs=7.0, lines=None, show_out=True):
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y).
    The excerpt is a verbatim slice and the label above the panel names it ('program <name>, lines a to b of n'), as
    program_check_v1_0_0.py verifies. The transcript, when shown, sits in the same panel."""
    y = max(y, 1.55)
    pr = PROGS[pname]
    all_lines = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(all_lines)) if lines is None else lines
    shown = all_lines[a - 1:b]
    out = pr["transcript"] if show_out else ""
    outlines = (out.count("\n") + 1) if out else 0
    need = pw(pname, (a, b), show_out, fs)
    if need > w + 0.005:
        raise SystemExit("REFUSED: program %s lines %d-%d cannot fit unwrapped in %.2f in at %.1f pt (needs %.2f)" % (pname, a, b, w, fs, need))
    L = len(shown) + outlines
    h = round(L * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    label = "program %s, lines %d to %d of %d" % (pname, a, b, len(all_lines))
    if len(label) > (w - 0.1) / 0.0725:
        raise SystemExit("REFUSED: caption %r is too long for a %.2f in panel" % (label, w))
    it = {"t": "prog", "x": x, "y": y, "w": w, "h": h, "lines": shown, "fs": fs, "compact": bool(out),
          "out": out if out else None, "outLabel": "prints", "label": label}
    return it, round(y + h, 2)


def factrow(sid, x=0.5, y=4.42, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return st["story"] + " The account rests on these sources. " + st["source"]


def card(head, body, x, y, w, h, fs=11.5, accent=None):
    if len(head) > (w - 0.4) / 0.112:
        raise SystemExit("REFUSED: card heading %r does not fit one line of a %.2f in card" % (head, w))
    it = {"t": "card", "head": head, "body": body, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


def foot(body, x, y, w, fs=9.5):
    h = round(DS.need_h(body, w, fs) + 0.04, 2)
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def stack(bodies, x, y, w, fs=8.5, gap=0.04):
    """Foot items one under another, each at the bottom of the one before."""
    out = []
    for b in bodies:
        f = foot(b, x, round(y, 2), w, fs=fs)
        out.append(f)
        y = f["y"] + f["h"] + gap
    return out


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "lifecycle_multi": DS.lifecycle_multi, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body}
    it["did"] = did
    return it, cap




def png_size(fn):
    with open(os.path.join(IMGDIR, fn), "rb") as f:
        head = f.read(24)
    return struct.unpack(">II", head[16:24])


def img(fn, x, y, maxw, maxh):
    """A picture a program saved, placed in the largest box of its own shape that fits maxw x maxh inches at (x, y); returns (item, bottom y, right x)."""
    if fn not in EX["_images"]:
        raise SystemExit("REFUSED: %s is not a picture of the recording" % fn)
    pw_, ph_ = png_size(fn)
    k = min(maxw / pw_, maxh / ph_)
    w, h = round(pw_ * k, 2), round(ph_ * k, 2)
    it = {"t": "img", "path": os.path.join(IMGDIR, fn), "x": x, "y": y, "w": w, "h": h}
    return it, round(y + h, 2), round(x + w, 2)


def imgcap(fns, x, y, w, fs=8.5):
    """The caption that names pictures and their programs ('image <file> made by <program>'), as program_check_v1_0_0.py reads it."""
    body = "; ".join("image %s made by %s" % (fn, EX["_images"][fn]["program"]) for fn in fns)
    return foot(body, x, y, w, fs=fs)


def tpanel(pname, x, y, w, fs=7.5):
    """A panel that shows only the transcript of a program (label 'transcript of program <name>'), sized from its text."""
    pr = PROGS[pname]
    t = pr["transcript"].split("\n")
    need = round(max(len(l) for l in t) * CW * fs + 0.4 + 0.5, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: the transcript of %s needs %.2f in at %.1f pt, the panel has %.2f" % (pname, need, fs, w))
    h = round(len(t) * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    label = "transcript of program %s" % pname
    return {"t": "prog", "x": x, "y": max(y, 1.55), "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": pr["transcript"], "outLabel": "prints", "label": label}, round(max(y, 1.55) + h, 2)

S = []
SHOWN = {}  # diagram id -> slide number
NOTEXEC = []  # slide numbers that carry the words NOT EXECUTED
RECORDED = []  # slide numbers that carry the word Recorded (a record of 13 Oct 2026 that the deck does not run again)
STANDIN = {}  # slide number -> the stand-in programs it shows


LATE = []


def content(title, sub, items, notes, take, lede=None, notexec=False, recorded=False):
    if lede and len(lede.split()) > 34:
        raise SystemExit("REFUSED: lede on %r runs past the gate" % title)
    if len(take.split()) > 24 or not take.endswith(".") or len(take) > 84:
        LATE.append("takeaway %r (%d)" % (take, len(take)))
    if len(title) > 44:
        LATE.append("title %r" % title)
    if len(sub) > 86:
        LATE.append("subtitle %r (%d)" % (sub, len(sub)))
    for it in items:
        if it["t"] in ("code", "prog", "shapes", "card", "boxes", "chips", "stat", "beats", "factrow", "numlist", "bullets", "links", "foot", "text", "img", "table", "chart"):
            if it["y"] + it.get("h", 0.4) + (0.26 if it.get("cap") and it["t"] == "code" else 0) > 5.0 or it["x"] + it["w"] > 9.56:
                raise SystemExit("REFUSED: item %s on %r reaches y %.2f / x %.2f (starts %.2f)" % (it["t"], title, it["y"] + it.get("h", 0.4), it["x"] + it["w"], it["y"]))
        if it["t"] == "shapes":
            SHOWN[it["did"]] = len(S) + 1
        if it["t"] == "prog":
            nm = it["label"].replace("transcript of program ", "").replace("program ", "").split(",")[0]
            if PROGS[nm]['kind'] == 'standin':
                STANDIN.setdefault(len(S) + 1, []).append(nm)
    blob = json.dumps(items)
    if notexec:
        NOTEXEC.append(len(S) + 1)
        if L_NOTEXEC not in blob:
            raise SystemExit("REFUSED: slide %r is declared NOT EXECUTED but says nothing of it" % title)
    if recorded:
        RECORDED.append(len(S) + 1)
        if L_REC not in blob:
            raise SystemExit("REFUSED: slide %r is declared Recorded but says nothing of it" % title)
    sl = {"kind": "content", "title": title, "sub": sub, "items": items, "notes": notes, "take": take, "bg": "light"}
    if lede:
        sl["lede"] = lede
    S.append(sl)




def hid(pn, a, b, what_before="imports and helpers", what_after=None):
    """The words that say which lines of the program are not on the slide: lines 1 to a-1, and lines b+1 to n."""
    n = len(PROGS[pn]["code"].rstrip("\n").split("\n"))
    out = []
    if a > 1:
        out.append("Lines 1 to %d (%s) are not shown." % (a - 1, what_before))
    if b < n:
        out.append("Lines %d to %d (%s) are not shown." % (b + 1, n, what_after or "the rest"))
    return " ".join(out)


W_HEAD = "imports, helpers, a download check"
SAY_VD = "Virtual display: Xvfb with the real xclip, a local stand-in for a screen; nobody sees the picture."

# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.4, 4.5, fs=10, cap=False)
S.append({"kind": "title", "title": "Ch. 21: Graphs and Images",
          "sub": "Making graphs and manipulating images: Pillow, ImageDraw, the clipboard and Matplotlib",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made, and every picture was saved by a program that is run again to check it. "
                             "Windows, macOS and a real screen were never used: the clipboard program ran on a virtual display, and what could not be run is marked on its slide.",
                             0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 20 taught a program to reach a person. Chapter 21 teaches a program to make pictures: edit them with Pillow, draw on them, put them on the clipboard, and draw graphs with Matplotlib. "
                   "The chapter has 31 listings, 20 figures and 1 table, and ends with 12 practice questions and 3 practice programs, Tile Maker, the photo folder finder and the seating cards. "
                   "This deck follows the chapter in its own order: colours and coordinates, cropping, pasting, resizing, rotating, pixels, Project 16 that adds a logo to every picture, shapes and text, the clipboard, and graphs with line, scatter, bar and pie. "
                   "It adds what the research found when every printed output was run again: Table 21-1 gives Green as the colour that CSS calls lime; a PNG saved without a dpi has no pixel density although the chapter says 72; "
                   "the fill of a rotated corner follows the mode of the image and not the operating system; Appendix A pins matplotlib==3.92, which does not exist; Appendix B answers 3, 6 and 12 wrongly or partly wrongly; "
                   "the printed listing of Project 16 has an en dash that stops it with a SyntaxError; textsize and getsize exist only in Pillow 9.5.0; and plt.pie returns a tuple up to Matplotlib 3.10.8 and a PieContainer from 3.11. "
                   "The outputs of this chapter are pictures, so the deck shows real ones: sixteen pictures that programs saved are on the slides as images, and each caption names the program that made the picture. "
                   "The build runs every such program again and refuses the deck unless the slide holds a picture that is byte for byte, or pixel for pixel, what the program saves now. "
                   "Every output on the slides was printed by Python 3.14.6, installed with uv, with Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4 and pyperclipimg 0.2.0. "
                   "Four programs download the publisher's zip of online materials and check each of the four files of the chapter against its SHA-256. "
                   "Windows and macOS were never used, and nobody looked at a real screen: the clipboard program ran on a virtual display, which the slide says. "
                   "What could not be run, Windows and macOS, the windows of Matplotlib and of Image.show on a real screen, and two Matplotlib releases on Python 3.14.6, is marked on its slide.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % ROWS_SHOWN,
                    "%d programs run" % len(PROGS), "8 diagrams", "16 pictures", "Python %s" % PYV]}],
        "The first question is the spine of the chapter, and the deck answers it slide by slide. On a machine with no screen, a program can make a picture, change it, draw on it, save it and read its pixels back, and the picture can be compared with what was meant; "
        "that is what can be shown to work. What can only be shown to fail on such a machine is the part that needs a person's screen: plt.show() and Image.show() open a window, and the clipboard needs a display and a clipboard owner. "
        "The research used a virtual X display, Xvfb, with the real xclip, and a Tk window on it, and took a screenshot of the screen; nobody looked at a real monitor, Windows and macOS were never used, and the deck says so where it comes up. "
        "The second question is the watch-out. The chapter's 138 interactive statements were replayed as printed in four environments. With Python 3.14.6, Pillow 12.3.0 and Matplotlib 3.11.2, 131 of 138 matched the book headless and 135 on a virtual X display; "
        "with the Pillow 10.4.0 and Matplotlib 3.9.2 that Appendix A pins, built from source on 3.14.6, 125 matched headless and 108 on the display; with the same pins as wheels on Python 3.13.14, 129 and 108; with an empty Python, 15. "
        "The three that still differ with the newest packages and a display are os.chdir to a Windows path, the font arial.ttf, and the printed tuple of plt.pie, which is a PieContainer. "
        "The online materials of the book, 91 files, hold the four files of this chapter and not the others the chapter names. Each slide says where a printed line differs and on what evidence.",
        "Know what can be shown to work and what can only be shown to fail.")

# ---- 4 what a program can do with an image ---------------------------------------------------------------------------
dg, dcap = diagram("WhatAProgramCanDoWithAnImage", "usecases", (0.5, 1.4, 4.6, 3.2), fs=8)
x4 = 5.3
content("What a program can do with an image", "Eight things through one object; the chapter adds graphs, a clipboard and a project",
        [dg, dcap,
         card("Two libraries and a clipboard", "Pillow edits and draws pictures, Matplotlib draws graphs, and pyperclipimg copies a picture to the clipboard. The chapter ends with 12 practice questions and 3 practice programs.",
              x4, 1.5, round(9.5 - x4, 2), 1.55, fs=9.5, accent="slate"),
         card("Recorded 13 Oct 2026", "The online materials hold 91 files, four of them for this chapter: zophie.png, catlogo.png, guests.txt and resizeAndAddLogo.py. The zip has no zophie_the_cat.jpg, no zophie_xmas_tree.png and no flower image, which the chapter mentions.",
              x4, 3.15, round(9.5 - x4, 2), 1.8, fs=9.5, accent="orange")],
        "The use-case diagram lists what the chapter does with one Pillow Image object: crop a rectangle with a box tuple, paste one image onto another, resize to integers, rotate and expand, flip with transpose, change one pixel with putpixel, draw shapes with ImageDraw, and save in a format chosen by the extension. "
        "They are independent uses of the same object and not a sequence, which is why the picture is a set of uses. The chapter teaches Pillow for pictures, pyperclipimg for the clipboard and Matplotlib for graphs: line, scatter, bar and pie. "
        "The chapter's page was read on 13 October 2026; it returned 200 with 119,144 bytes and holds 31 listings, 20 figures and 1 table, and its SHA-256 equals the digest that the book's own chapter ontology records. "
        "The card records what the research found on that day and this deck does not run again: the online materials of the third edition, a zip of 91 files, hold zophie.png of 816 by 1088 pixels in mode RGB, catlogo.png of 100 by 95 pixels in mode LA, guests.txt with 5 names and resizeAndAddLogo.py. "
        "The zip has none of zophie_xmas_tree.png, me_and_zophie.png, zophie_the_cat.jpg, or a file with flower in its name among 184 entries, although the chapter says a public domain flower image is available; and the publisher's book page has one occurrence of Making Graphs and none of Pillow, Matplotlib, zophie or catlogo. "
        "The deck downloads the zip while it runs and checks the SHA-256 of each of the four files; the cat picture is the book's own example, and the study did not check its licence, so it is used here for teaching only. "
        "The second edition's chapter 19, Manipulating Images, mentions Pillow 30 times, textsize 3 times and ImageFont 13 times and neither Matplotlib nor pyperclipimg; the third edition's chapter adds both and uses neither textsize nor getsize.",
        "One object, eight uses; the book's files are the starting point.", recorded=True)

# ---- 5 a picture is a grid of numbers: Kirsch -------------------------------------------------------------------------
c5, bot5 = con("grid", 0.5, 1.45, 4.9, fs=9, cap=False)
content("A picture is a grid of numbers", "1957: one of the first scanned photographs was 176 by 176 pixels, one bit each",
        [c5,
         {"t": "beats", "x": 5.7, "y": 1.5, "w": 3.8, "h": 2.6, "fs": 12, "items": [
             "1957: a drum scanner at the NBS",
             "176 x 176 = 30,976 pixels",
             "One bit each: black or white",
             "Today: mode '1' holds the same"]},
         factrow("Kirsch1957", y=4.5)],
        story_notes("Kirsch1957") + " The console on the slide uses only Pillow, so each row can be typed into a Python that has Pillow: Image.new('1', (176, 176)) makes a picture of mode 1, one bit for each pixel, "
        "size (176, 176), 30,976 pixels; tobytes() packs eight pixels into a byte, so it holds 3,872 bytes, which is 30,976 divided by 8. A new picture is all zero, black; putpixel() writes a 1 and returns None, and getpixel() reads it back, "
        "while the pixel beside it is still 0. The same two calls work for the RGB pictures of the rest of the chapter, with a tuple of three integers in place of 0 or 1. "
        "The chapter's own first section, Computer Image Fundamentals, says the same thing in words: a picture is a grid of pixels and each pixel is numbers.",
        STORY["Kirsch1957"]["lesson"] + ".")

# ---- 6 colours ---------------------------------------------------------------------------------------------------------
pn = "colorsSwatchCut_v1_0_0.py"
a6, b6 = span(pn, "names = ")
f6 = bestfs(pn, (a6, b6), 5.5, 3.25)
w6 = pw(pn, (a6, b6), True, f6)
p6, bot6 = prog(pn, 0.5, 1.55, w6, fs=f6, lines=(a6, b6), show_out=True)
x6 = round(0.5 + w6 + 0.2, 2)
im6, ib6, _ = img("swatches.png", x6, 1.5, round(9.5 - x6, 2), 0.7)
content("Colours, names and Table 21-1", "ImageColor.getcolor() turns a name into four integers from 0 to 255",
        [p6, im6, imgcap(["swatches.png"], x6, round(ib6 + 0.03, 2), round(9.5 - x6, 2), fs=8),
         card("Table 21-1: Green is lime", "The table gives Green as (0, 255, 0, 255), the colour CSS calls lime. Pillow returns (0, 128, 0, 255) for green, as the program prints; of the table's 8 rows only Green differs.",
              x6, round(ib6 + 0.4, 2), round(9.5 - x6, 2), 1.75, fs=9.5, accent="orange"),
         foot(hid(pn, a6, b6, W_HEAD), 0.5, round(bot6 + 0.06, 2), w6, fs=8.5)],
        "A colour in Pillow is a tuple of four integers from 0 to 255: red, green, blue and alpha. ImageColor.getcolor(name, 'RGBA') turns a colour name or a hex string into that tuple, and the name is not case sensitive: CornflowerBlue gives (100, 149, 237, 255), and #CCDDEE gives (204, 221, 238, 255). "
        "The strip of six colours under the program is the picture that the program saved; its caption names the program, and the build runs the program again and compares the picture with this one. "
        "The research compared Table 21-1 of the book with Pillow 12.3.0. Of its 8 rows only Green differs: the table says Green is (0, 255, 0, 255), but that is lime in the CSS list that Pillow follows, and the strip shows both side by side, a dark green and a bright one. "
        "ImageColor.colormap holds 148 names, from aliceblue to yellowgreen, where the Pillow page says some 140 and the chapter more than 100; and 'transparent' is not one of them, so getcolor() raises ValueError. "
        "The new picture of the chapter, Image.new('RGBA', (100, 200), 'purple'), has the pixel (128, 0, 128, 255); with no colour an RGBA picture is the invisible (0, 0, 0, 0). "
        "The program was cut from colorsAndModes_v1_0_0.py of the corpus, which also ran: RGBA to JPEG raised OSError with cannot write mode RGBA as JPEG, and an unknown extension raised ValueError.",
        "Green of Table 21-1 is lime; Pillow's green is (0, 128, 0).")

# ---- 7 coordinates and box tuples ---------------------------------------------------------------------------------------
c7, bot7 = con("box", 0.5, 1.45, 4.9, fs=9, cap=True)
im7, ib7, _ = img("boxTuple.png", 5.8, 1.5, 3.7, 2.95)
content("Coordinates and box tuples", "The origin is top left; a box keeps its left and top, not its right and bottom",
        [c7, im7, imgcap(["boxTuple.png"], 5.8, round(ib7 + 0.03, 2), 3.7, fs=8),
         foot("Appendix B, answer 3, calls the box left, top, width and height; the chapter, and Pillow, say left, top, right and bottom. The picture is Figure 21-2 drawn by a program: 6 columns and 5 rows are orange, the box (3, 1, 9, 6) is their size.",
              0.5, round(bot7 + 0.05, 2), 4.9, fs=9)],
        "A pixel is addressed by (x, y), with the origin at the top left, x growing to the right and y growing down; the last pixel of a 28 by 27 picture is (27, 26), (28, 0) raises IndexError with image index out of range, and a negative x counts from the right edge. "
        "A box tuple has four integers in the order left, top, right, bottom, and the box includes the left and top edge and excludes the right and bottom one. The box (3, 1, 9, 6) of Figure 21-2 covers 6 columns and 5 rows, which is 30 pixels; the width is right minus left, not the third number, and a box with right smaller than left raises ValueError with the text Coordinate 'right' is less than 'left'. "
        "The picture on the right is made by the program boxTupleCut: it paints the pixels 3 to 8 and 1 to 5 orange on a white 28 by 27 picture, crops the box (3, 1, 9, 6) and finds only orange in it, then crops one column more to the left and finds white; it then enlarges the picture ten times without smoothing and draws a grid so the pixels can be counted. "
        "Appendix B of the book answers question 3 by calling a box left, top, width and height, where the chapter says right and bottom; the next slide shows the answer to question 6. "
        "Rectangles in ImageDraw are different again: both end points are painted, which the drawing slide counts.",
        "Right and bottom are not in the box; the width is right minus left.")

# ---- 8 cropping ----------------------------------------------------------------------------------------------------------
pn = "cropFaceCut_v1_0_0.py"
a8, b8 = span(pn, "cat = ")
f8 = bestfs(pn, (a8, b8), 5.3, 2.4)
w8 = pw(pn, (a8, b8), True, f8)
p8, bot8 = prog(pn, 0.5, 1.55, w8, fs=f8, lines=(a8, b8), show_out=True)
x8 = round(0.5 + w8 + 0.2, 2)
im8, ib8, _ = img("face.png", x8, 1.5, 1.9, 1.45)
c8, bot8c = con("appb", x8, round(ib8 + 0.45, 2), round(9.5 - x8, 2), fs=8.5, cap=False)
content("Cropping a picture", "crop() takes one box tuple, returns a new Image and leaves the original alone",
        [p8, im8, imgcap(["face.png"], x8, round(ib8 + 0.03, 2), round(9.5 - x8, 2), fs=8),
         c8,
         foot(hid(pn, a8, b8, W_HEAD) + " The cat is zophie.png of the book's online materials.", 0.5, round(bot8 + 0.05, 2), w8, fs=8.5),
         foot("Appendix B answers question 6 with im.crop((0, 50, 50, 50)), whose size is (50, 0): an empty picture. The 50 by 50 lower-left quarter of a 100 by 100 picture is (0, 50, 50, 100), as the console shows.",
              0.5, round(bot8 + 0.5, 2), w8, fs=9)],
        "crop() takes one box tuple, not four arguments, and returns a new Image without changing the original: the face box (335, 345, 565, 560) of zophie.png, which is 816 by 1088 pixels in mode RGB, gives a picture of 230 by 215 pixels, and the original keeps its size. "
        "The picture on the right is that face, saved by the program, and the build compares it with what the program saves now. A box with right smaller than left raises ValueError, and a box that runs past the edge does not fail: crop((700, 1000, 900, 1200)) of the 816 by 1088 picture is still 200 by 200 and the pixels outside are black, (0, 0, 0). "
        "Appendix B of the book answers practice question 6 with im.crop((0, 50, 50, 50)); because the top and the bottom are both 50 that box is 50 wide and 0 high, and the console shows the size (50, 0), where the lower-left quarter of a 100 by 100 picture is (0, 50, 50, 100) and is 50 by 50. "
        "The program was cut from cropPasteTile_v1_0_0.py of the corpus, which also ran and printed that Pillow 12.3.0 gives the filename zophie.png; the Pillow releases 10.3.0, 10.4.0 and 11.0.0 give the absolute path, which is what the book's pinned Pillow 10.4.0 returns and the book's printed listing does not. "
        "The cat picture is the book's own example from its online materials; the study did not check the licence of the picture, so the deck uses it for teaching only.",
        "crop() returns a new picture; right and bottom are outside it.")

# ---- 9 pasting and tiling -----------------------------------------------------------------------------------------------
dg, dcap = diagram("TilingAPictureWithPaste", "activity", (0.5, 1.4, 3.7, 3.2),
                   grid={"crop": (0, 0), "copy": (0, 1), "left": (0, 2), "top": (0, 3), "paste": (0, 4), "more": (0, 5), "save": (0, 6)},
                   cols=[(0.4, 2.8), (3.3, 0.4)], rows_n=7, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 6},
                   routes={("start", "crop"): "h", ("more", "left"): "loopL", ("save", "end"): "h"}, fs=8, nh=0.36, dh=0.46)
pn = "tileCatCut_v1_0_0.py"
a9, b9 = span(pn, "tiled = cat.copy()")
f9 = bestfs(pn, (a9, b9), 5.05, 2.3)
w9 = pw(pn, (a9, b9), True, f9)
x9 = 4.45
p9, bot9 = prog(pn, x9, 1.55, w9, fs=f9, lines=(a9, b9), show_out=True)
im9, ib9, _ = img("tiled.png", x9, round(bot9 + 0.1, 2), 1.2, 4.95 - round(bot9 + 0.1, 2) - 0.0)
content("Pasting and tiling", "paste() changes the image it is called on and returns None, so copy first",
        [dg, dcap, p9, im9,
         imgcap(["tiled.png"], round(x9 + im9["w"] + 0.15, 2), round(bot9 + 0.1, 2), round(9.5 - x9 - im9["w"] - 0.15, 2), fs=8),
         foot(hid(pn, a9, b9, W_HEAD) + " 816 by 1088 holds 4 columns and 6 rows of the 230 by 215 face: 24 pastes, the last row and column cut off at the edge.",
              round(x9 + im9["w"] + 0.15, 2), round(bot9 + 0.55, 2), round(9.5 - x9 - im9["w"] - 0.15, 2), fs=9)],
        "paste(im, (left, top)) changes the picture it is called on and returns None, so the program copies the picture first with copy(); after the face is pasted into the copy the corner of the copy equals the corner of the face while the original's corner does not. "
        "paste() and copy() have nothing to do with the clipboard. The flow chart is the book's tiling loop: crop the face, copy the picture, take the next left in range(0, width, face width) and inside it the next top in range(0, height, face height), paste the face there, and repeat until the grid is full. "
        "On the 816 by 1088 picture with the 230 by 215 face that is 4 columns and 6 rows, 24 pastes from (0, 0) to the last, (690, 1075); the last column and row run past the edge and Pillow cuts them off, which the program shows. "
        "The picture is a thumbnail of the tiled copy, 204 by 272 pixels, made by the same program and compared by the build with the picture on the slide. "
        "The corpus program cropPasteTile_v1_0_0.py, which also ran, resized the same picture to twice its size, (1632, 2176), and showed that resize() with floats raises TypeError; the next slides use both.",
        "Copy first, then paste in two loops; the last tiles are cut off.")

# ---- 10 masks and alpha --------------------------------------------------------------------------------------------------
pn = "maskPairCut_v1_0_0.py"
a10, b10 = span(pn, "logo = ")
f10 = bestfs(pn, (a10, b10), 5.2, 2.75)
w10 = pw(pn, (a10, b10), True, f10)
p10, bot10 = prog(pn, 0.5, 1.55, w10, fs=f10, lines=(a10, b10), show_out=True)
x10 = round(0.5 + w10 + 0.2, 2)
im10, ib10, _ = img("maskPair.png", x10, 1.5, round(9.5 - x10, 2), 2.0)
content("Masks and the alpha channel", STORY["Alpha1970s"]["when"],
        [p10, im10, imgcap(["maskPair.png"], x10, round(ib10 + 0.03, 2), round(9.5 - x10, 2), fs=8),
         foot("Left: the logo pasted with itself as the mask. Right: the same call without the mask, so the invisible corner is copied as white and clear.",
              x10, round(ib10 + 0.35, 2), round(9.5 - x10, 2), fs=9),
         foot(hid(pn, a10, b10, W_HEAD), 0.5, round(bot10 + 0.04, 2), w10, fs=8.5),
         factrow("Alpha1970s", y=4.5)],
        story_notes("Alpha1970s") + " The third argument of paste() is a mask, and the program shows what it does with catlogo.png of the book's online materials, which is 100 by 95 pixels in mode LA, a grey channel and an alpha channel, with the corner pixel (255, 0): white and fully clear. "
        "Pasted onto a red picture with the logo as its own mask, the corner stays the red (200, 0, 0, 255); pasted without a mask the same corner is copied as (255, 255, 255, 0), so the invisible pixels of the copy overwrite what is below them. "
        "That is Figure 21-13 of the book, and the picture on the right shows both results next to each other. The last lines are the story's own experiment: a blue square at alpha 128 pasted over a red pixel with itself as the mask gives (127, 0, 128), half of each. "
        "In the corpus program tileMaker_v1_0_0.py, which also ran, pasting the LA logo onto an RGB picture with no mask runs without an error and gives white and black pixels, and with the logo as the mask the transparent corner stays white.",
        STORY["Alpha1970s"]["lesson"] + ".")

# ---- 11 resize, rotate, flip, pixel -------------------------------------------------------------------------------------------
pn = "rotateSheetCut_v1_0_0.py"
a11, b11 = span(pn, "im = Image.new", "c = im.copy()")
f11 = bestfs(pn, (a11, b11), 5.0, 3.25)
w11 = pw(pn, (a11, b11), True, f11)
p11, bot11 = prog(pn, 0.5, 1.55, w11, fs=f11, lines=(a11, b11), show_out=True)
x11 = round(0.5 + w11 + 0.2, 2)
im11, ib11, _ = img("rotateSheet.png", x11, 1.5, round(9.5 - x11, 2), 1.8)
content("Resize, rotate, flip and set a pixel", "The fill of a rotated corner follows the image's mode, not the operating system",
        [p11, im11, imgcap(["rotateSheet.png"], x11, round(ib11 + 0.03, 2), round(9.5 - x11, 2), fs=8),
         foot("The panels: the picture; rotate(20); an RGBA copy rotated; fillcolor='red'; expand=True; rotate(90).", x11, round(ib11 + 0.24, 2), round(9.5 - x11, 2), fs=9),
         card("NOT EXECUTED here", "Windows and macOS were never used, so black versus transparent is read, not run.",
              x11, 3.9, round(9.5 - x11, 2), 1.05, fs=9, accent="orange"),
         foot("Lines 1 to %d (imports, helpers) and %d to %d (the sheet) are not shown." % (a11 - 1, b11 + 1, len(PROGS[pn]["code"].rstrip().split("\n"))), 0.5, round(bot11 + 0.03, 2), w11, fs=8)],
        "rotate() turns a picture counterclockwise and keeps its size; the corners that no pixel reaches are filled. The chapter says that rotation gaps are black on Windows and transparent on macOS and Linux; on Linux the fill followed the mode of the picture: an RGB picture got (0, 0, 0), "
        "an RGBA copy got (0, 0, 0, 0), and the keyword fillcolor='red' gave (255, 0, 0). The Pillow page of rotate() names a fill colour and no operating system. Windows and macOS were never used, so that part of the chapter's sentence is read and not run. "
        "With expand=True the picture grows to hold the turned one: 120 by 80 becomes 142 by 118 at 20 degrees, and on the book's 816 by 1088 cat 6 degrees gives 926 by 1168; rotate(90) without expand keeps 120 by 80 and cuts the corners, with expand it is 80 by 120. "
        "transpose(Image.Transpose.FLIP_LEFT_RIGHT) mirrors the picture, so the left pixel is the old right pixel, and the old constant Image.FLIP_LEFT_RIGHT also still works. resize() takes integers: floats raise TypeError with the text 'float' object cannot be interpreted as an integer, which is why the chapter wraps the division in int(); "
        "and with no filter named it uses bicubic for an RGB picture. putpixel() returns None and takes a tuple, not a colour name; getpixel((-1, 0)) is the pixel of the last column. "
        "The sheet on the right is the picture the program saved: six panels on a beige ground, so the transparent corners of the RGBA copy show the ground and the others do not. The corpus program rotateFlipPixels_v1_0_0.py ran the same checks on a 60 by 40 gradient.",
        "The fill of a rotated corner follows the mode of the picture.", notexec=True)

# ---- 12 saving: PNG, JPEG and dpi --------------------------------------------------------------------------------------------------
pn = "saveFormatsCut_v1_0_0.py"
a12, b12 = span(pn, "cat = ", "print('RGBA to JPEG")
f12 = bestfs(pn, (a12, b12), 5.2, 3.3)
w12 = pw(pn, (a12, b12), True, f12)
p12, bot12 = prog(pn, 0.5, 1.55, w12, fs=f12, lines=(a12, b12), show_out=True)
x12 = round(0.5 + w12 + 0.2, 2)
ch12 = EX["_charts"]["jpegBytes"]
chart12 = {"t": "chart", "ctype": "bar", "x": x12, "y": 1.4, "w": round(9.5 - x12, 2), "h": 1.85, "labels": ch12["labels"],
           "title": "Kilobytes of the cat picture", "series": [{"name": "KB", "data": ch12["values"]}], "dataLabels": True, "dlFs": 9}
im12, ib12, _ = img("pngVsJpeg.png", x12, 3.3, round(9.5 - x12, 2), 1.35)
content("Saving: PNG, JPEG and pixel density", STORY["Png1996"]["when"],
        [p12, chart12, im12, imgcap(["pngVsJpeg.png"], x12, round(ib12 + 0.02, 2), round(9.5 - x12, 2), fs=8),
         foot("Lines 1 to %d (head) and %d to %d (the pair picture) are not shown." % (a12 - 1, b12 + 1, len(PROGS[pn]["code"].rstrip().split("\n"))), 0.5, round(bot12 + 0.03, 2), w12, fs=8)],
        "save() chooses the format from the extension. The cat, zophie.png, is 1,287,443 bytes as a PNG; saved as a JPEG at quality 95, 75, 50, 30 and 10 it is 327,361, 125,433, 81,267, 58,200 and 29,630 bytes, which the chart shows in kilobytes; "
        "the deck check computes the six numbers again every time it runs. JPEG is lossy: reading the quality 75 file back changes the largest channel value by 37, and the picture on the lower right shows the face as a PNG and as a JPEG of quality 10, side by side. "
        "A mode with an alpha channel cannot be written as JPEG, which raises OSError with cannot write mode RGBA as JPEG, and an extension Pillow does not know raises ValueError. "
        "The chapter says that Pillow's PNG files are 72 pixels per inch by default, and the program shows that they are not: a PNG saved with no dpi has no pHYs chunk and no density to read back, dpi is None; with dpi=(72, 72) the chunk holds 2835 pixels per metre, which Pillow reads as 72.009 dpi; "
        "a JPEG saved with the defaults has the density (1, 1) and unit 0, no unit at all; and a PNG that Matplotlib saves carries 100 dpi, as the graph slides show. The sums of the seating cards are right, 4 by 5 inches at 72 pixels per inch is 288 by 360 pixels, but that is arithmetic and not a property of the file. "
        + story_notes("Png1996") + " The story of JPEG, which the notes carry and the slide does not: " + STORY["Jpeg1992"]["story"] + " Source: " + STORY["Jpeg1992"]["source"],
        "A PNG has no dpi unless you give one; JPEG is lossy.")

# ---- 13 Project 16 as a workflow -----------------------------------------------------------------------------------------------
dg, dcap = diagram("AddingALogoToEveryPicture", "activity", (0.5, 1.4, 5.6, 3.2),
                   grid={"open": (0, 0), "loop": (0, 1), "ext": (0, 2), "size": (0, 3), "big": (0, 4), "paste": (0, 5), "save": (0, 6), "resize": (1, 4)},
                   cols=[(0.45, 2.9), (3.85, 1.7)], rows_n=7, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 1},
                   routes={("start", "open"): "h", ("ext", "loop"): "loopL", ("save", "loop"): "loopL2", ("loop", "end"): "h", ("resize", "paste"): "vh"},
                   fs=8, nh=0.34, dh=0.44)
x13 = 6.3
im13, ib13, _ = img("zophieLogo.png", x13, 1.45, 1.3, 1.75)
content("Project 16: a logo on every picture", "One loop over a folder, two decisions, and a paste with the logo as its own mask",
        [dg, dcap, im13,
         imgcap(["zophieLogo.png"], round(x13 + im13["w"] + 0.1, 2), 1.45, round(9.5 - x13 - im13["w"] - 0.1, 2), fs=8),
         card("Resize only big ones", "Both sides must be larger than 300. A strip of 1200 by 250 keeps its size, a panorama of 1200 by 400 becomes 300 by 100.",
              x13, 3.3, round(9.5 - x13, 2), 1.65, fs=9.5, accent="slate")],
        "The flow chart is the book's Project 16, Adding a Logo to Every Picture. It opens catlogo.png once, then loops over the names that os.listdir() returns, skips every name that does not end in .png or .jpg and the logo itself, opens the picture and reads its size, "
        "and resizes it only if both the width and the height are larger than 300, so that the longer side becomes 300. It pastes the logo in the lower-right corner with the logo as its own mask and saves the result in the folder withLogo, then goes back to the loop. "
        "The research ran the shipped file resizeAndAddLogo.py of the online materials, after its SHA-256 was checked, in a folder with four test pictures: a panorama of 1200 by 400, a strip of 1200 by 250, a tall.jpg and the cat zophie.png of 816 by 1088. The exit code was 0 and withLogo held four pictures: panorama.png of 300 by 100, strip.png of 1200 by 250, tall.jpg of 214 by 300 and zophie.png of 225 by 300. "
        "The strip kept its size because only one of its sides is larger than 300, and the cat shrank from 816 by 1088 to 225 by 300; the logo landed at (125, 205), the lower-right corner of the 225 by 300 picture, and the pixel there changed. "
        "The picture on the right is that cat with the logo, saved by the program of the next slide, and the build compares it with what the program saves now. The size is int(300 / 1088 * 816), which is 225; without int() the division gives 225.00000000000003, and resize() refuses a float. "
        "A file called UPPER.PNG was skipped, because the test endswith('.png') is case sensitive.",
        "Two decisions guard the paste: the extension, then the size.")

# ---- 14 Project 16 as printed and as shipped ------------------------------------------------------------------------------------------
pn = "addLogoCut_v1_0_0.py"
a14, b14 = span(pn, "Image.new('RGB', (1200, 400)")
f14 = 7.0
w14 = pw(pn, (a14, b14), True, f14)
p14, bot14 = prog(pn, 0.5, 1.55, w14, fs=f14, lines=(a14, b14), show_out=True)
x14 = round(0.5 + w14 + 0.2, 2)
c14, bot14c = con("logo", x14, 1.5, round(9.5 - x14, 2), fs=9, cap=True)
content("Project 16, as printed and as shipped", "The page has an en dash that stops the listing; the file in the zip has a minus sign",
        [p14, c14,
         foot(hid(pn, a14, b14, W_HEAD), 0.5, round(bot14 + 0.04, 2), w14, fs=8.5),
         card("NOT EXECUTED here", "The chapter's folder path C:\\folder_with_image_file is for Windows, never used here; the shipped file ran on Linux.",
              x14, 3.96, round(9.5 - x14, 2), 1.0, fs=9, accent="orange")],
        "The printed listing of Project 16 on the chapter's page holds an en dash, U+2013, where the file has a minus sign: compile() of a line with 816 followed by an en dash and 100 raises SyntaxError with invalid character '\u2013' (U+2013), and the same line with a minus sign compiles. "
        "Copying the listing from the page therefore stops with a SyntaxError, and copying the file from the zip does not. The research checked the shipped file for the character and found none; the SHA-256 of resizeAndAddLogo.py is one of the four that the deck checks while it runs. "
        "The program on the left makes three test pictures, runs the shipped file in that folder and lists withLogo: panorama.png (300, 100), strip.png (1200, 250) and zophie.png (225, 300), and UPPER.PNG is not in the list because the test is case sensitive; "
        "the console shows that 'UPPER.PNG'.endswith('.png') is False and 'UPPER.PNG'.lower().endswith('.png') is True. The sum 300 / 1088 * 816 is 225.00000000000003, which is why the shipped file wraps it in int(). "
        "The corpus program addLogoProject_v1_0_0.py ran the same file with one more test picture, tall.jpg, which became 214 by 300, and printed the messages of the shipped file, Adding logo to and Resizing. "
        "Nothing ran on Windows or macOS, so the folder path of the listing is read and not run.",
        "Copy the file from the zip, not the listing from the page.", notexec=True)

# ---- 15 drawing ----------------------------------------------------------------------------------------------------------------------------
pn = "drawingPngCut_v1_0_0.py"
a15, b15 = span(pn, "im = Image.new('RGBA'")
f15 = 7.0
w15 = pw(pn, (a15, b15), True, f15)
p15, bot15 = prog(pn, 0.5, 1.55, w15, fs=f15, lines=(a15, b15), show_out=True)
x15 = round(0.5 + w15 + 0.25, 2)
im15, ib15, _ = img("drawing.png", x15, 1.5, round(9.5 - x15, 2), 1.9)
content("Drawing shapes on a picture", "A rectangle includes its end points, so 41 by 31 pixels are blue, not 40 by 30",
        [p15, im15, imgcap(["drawing.png"], x15, round(ib15 + 0.03, 2), round(9.5 - x15, 2), fs=8),
         card("Colour names again", "'green' draws (0, 128, 0, 255), and the program finds no lime pixel. A box with its corners reversed raises ValueError.",
              x15, 3.78, round(9.5 - x15, 2), 1.2, fs=9, accent="slate")],
        "ImageDraw.Draw(im) draws on the picture it is given and changes it in place. The program draws a black frame with line(), a blue rectangle, a red ellipse, a brown polygon and a fan of green lines, then counts colours with getcolors(). "
        "The rectangle (20, 30, 60, 60) paints 41 by 31 pixels, 1,271 of them blue, because both end points are painted, where crop((20, 30, 60, 60)) of the same picture is 40 by 30: a drawing box and a cropping box are not the same kind of box. "
        "Drawing in the colour name green paints (0, 128, 0, 255), the colour of Table 21-1's mistake, and no pixel of lime appears. A rectangle whose corners are reversed raises ValueError with x1 must be greater than or equal to x0. "
        "The corpus program drawingPixelCounts_v1_0_0.py ran too: a rectangle with no fill and no outline still paints an outline in white; an ellipse in the box (0, 0, 99, 99) of a 100 by 100 picture touches all four edges; and the picture saved as a PNG and read back is 200 by 200, mode RGBA, with the pixel (0, 0, 255, 255) in the blue square. "
        "The picture on the right is the drawing as the program saved it; its caption names the program and the build compares the two. The listing of the chapter has the same calls; the lines the slide does not show are the head and the lines that save the picture.",
        "A drawing box includes its end points; a cropping box does not.")

# ---- 16 text and fonts ---------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("FromADrawingToAPngFile", "activity", (0.5, 1.4, 4.0, 3.2),
                   grid={"new": (0, 0), "draw": (0, 1), "shapes": (0, 2), "font": (0, 3), "text": (0, 4), "save": (0, 5), "other": (1, 3)},
                   cols=[(0.05, 2.2), (2.8, 1.2)], rows_n=6, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 5},
                   routes={("start", "new"): "h", ("save", "end"): "h", ("other", "font"): "uturn"}, fs=8, nh=0.34, dh=0.5)
pn = "textHowdyCut_v1_0_0.py"
a16, b16 = span(pn, "f = dejavu()")
f16 = 7.0
w16 = pw(pn, (a16, b16), True, f16)
x16 = round(9.5 - w16, 2)
p16, bot16 = prog(pn, x16, 1.55, w16, fs=f16, lines=(a16, b16), show_out=True)
im16, ib16, _ = img("howdy.png", x16, round(bot16 + 0.08, 2), 1.5, round(5.0 - bot16 - 0.08, 2))
content("Text and fonts", "textbbox() measures text; textsize() and getsize() are gone; arial.ttf is not on Linux",
        [dg, dcap, p16, im16,
         imgcap(["howdy.png"], round(x16 + im16["w"] + 0.1, 2), round(bot16 + 0.1, 2), round(9.5 - x16 - im16["w"] - 0.1, 2), fs=8)],
        "The flow chart is the book's way to a drawing: make an image, hand it to ImageDraw.Draw(), call line(), rectangle(), ellipse() and polygon(), then load a font. "
        "ImageFont.truetype('arial.ttf', 32) raised OSError with cannot open resource on this Linux machine, so the chapter's listing did not run as printed; if the font is not found you load a font by another file name, which here is DejaVuSans.ttf, and then draw the text and save. "
        "textbbox((20, 20), 'Howdy', font=f) returned (20, 26, 129, 57), 109 pixels wide and 31 high, and the program draws it as a red rectangle round the purple word, which is the picture on the lower right. "
        "ImageDraw has no textsize() and a font has no getsize(): both hasattr() calls print False, and the next slide shows the one Pillow release among those run that still had them. "
        "getlength('Howdy') gives 55, 109 and 218 pixels at the sizes 16, 32 and 64, so the width grows with the size. The book calls the size points and Pillow reads it as pixels: the same number gives the same height on every screen. "
        "The corpus program textAndFonts_v1_0_0.py also ran: the default font of Pillow 12.3.0 is a FreeTypeFont of size 10, text() returns None, textlength gives 109.06 and a box at (100, 150) runs past the right edge of a 200-pixel picture.",
        "Measure with textbbox() or getlength(), and read the size as pixels.")

# ---- 17 Pillow releases ------------------------------------------------------------------------------------------------------------------------
rt = EX["_tables"]["pillowReleases"]["rows"]
tbl17 = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [1.5] + [0.5357] * 14, "fs": 8, "rowH": 0.24, "rows": rt}
content("Pillow releases that changed the chapter", "Recorded: the same small programs under 14 releases, 9.5.0 to 12.3.0",
        [tbl17,
         card("Recorded 13 Oct 2026", "textsize() and getsize() exist only in 9.5.0 of these 14. The default font is a FreeTypeFont from 10.1.0, which also takes size=.",
              0.5, 3.05, 4.4, 1.35, fs=9.5, accent="orange"),
         card("Full path: three releases", "Image.open().filename is absolute only in 10.3.0, 10.4.0 and 11.0.0; the book's pin, 10.4.0, is one of them.",
              5.1, 3.05, 4.4, 1.35, fs=9.5, accent="slate"),
         factrow("Pil1995", y=4.5)],
        story_notes("Pil1995") + " The table is the research's record of small programs run under 14 Pillow releases on 13 October 2026, and the deck reads it from the record and does not run it again; "
        "the deck check computes the cells from the record every time it runs. In the 14 releases textsize() of ImageDraw and getsize() of a font exist only in 9.5.0 and are gone in 10.0.0; the default font is a bitmap ImageFont in 9.5.0 and 10.0.0 and a FreeTypeFont from 10.1.0, "
        "and load_default(size=20) is accepted from 10.1.0; Image.open('z.png').filename is an absolute path in 10.3.0, 10.4.0 and 11.0.0 and the name as given in the others. "
        "The book's Appendix A pins Pillow 10.4.0, so the cat's filename is the full path there and zophie.png in 12.3.0, and the second edition's textsize() fails in all of the last 13. "
        "The chapter uses neither textsize nor getsize, the second edition's chapter 19 uses textsize 3 times.",
        "Install Pillow, import PIL, and read the release notes.", recorded=True)

# ---- 18 practice programs -------------------------------------------------------------------------------------------------------------------------------
pn = "seatingCardsCut_v1_0_0.py"
a18, b18 = span(pn, "guests = ", "sheet.paste")
f18 = 7.0
w18 = pw(pn, (a18, b18), True, f18)
p18, bot18 = prog(pn, 0.5, 1.55, w18, fs=f18, lines=(a18, b18), show_out=True)
x18 = round(0.5 + w18 + 0.2, 2)
im18, ib18, _ = img("seatingCards.png", x18, 1.5, round(9.5 - x18, 2), 1.2)
t18, tb18 = tpanel("tileFolderCut_v1_0_0.py", 0.5, round(max(bot18 + 0.28, ib18 + 0.12), 2), 9.0, fs=7.5)
content("The practice programs: cards and folders", "Seating cards, Tile Maker and the photo folder finder, each run on test files",
        [p18, im18, imgcap(["seatingCards.png"], x18, round(ib18 + 0.03, 2), round(9.5 - x18, 2), fs=8),
         foot("Five cards of 288 by 360 pixels, 4 by 5 inches at 72 pixels per inch; the widest name, Col. Mustard, is 176 pixels.", x18, round(ib18 + 0.35, 2), round(9.5 - x18, 2), fs=9),
         foot(hid(pn, a18, b18, W_HEAD, "the prints and the saving of the strip"), x18, round(ib18 + 0.9, 2), round(9.5 - x18, 2), fs=8.5),
         t18],
        "The three practice programs of the chapter are Tile Maker, the photo folder finder and the seating cards. The seating cards program reads guests.txt of the online materials, five names, and makes a card of 288 by 360 pixels for each, which is 4 by 5 inches at 72 pixels per inch, "
        "with a black frame and the name centred with textbbox(); the widest name, Col. Mustard, is 176 pixels, so every name fits. The strip on the right is the five cards as thumbnails, saved by the program and compared by the build. "
        "The panel at the bottom is the transcript of a second program, tileFolderCut: make_tile('t.jpg', 6, 10) on a 20 by 50 picture gives a picture of (120, 500) and 60 tiles, the 120 by 500 that the book says, and the photo test, width and height both larger than 500, picks a.png and c.png of three pictures and a text file. "
        "The corpus programs tileMaker_v1_0_0.py and photoFolderFinder_v1_0_0.py ran as well. The first tiled the 100 by 95 logo over 400 by 300 in 16 pastes, with the logo as its own mask the transparent corner stays white, and without a mask the clear pixel is copied as (255, 255, 255, 0); "
        "the second walked a tree of four folders and found two with photos, ./a and ./b/c, and sorts the subfolders so that the lines are the same on every machine. "
        "The chapter says a public domain flower image is available; the zip has no file with flower in its name.",
        "Each practice program was run on files it made or on the book's.")

# ---- 19 the clipboard -----------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("CopyingAnImageToTheClipboard", "sequence", (0.5, 1.4, 3.55, 3.1), fs=8, head_w=1.0)
pn = "clipboardCut_v1_0_0.py"
a19, b19 = span(pn, "code = ")
f19 = 7.0
w19 = pw(pn, (a19, b19), True, f19)
x19 = round(9.5 - w19, 2)
p19, bot19 = prog(pn, x19, 1.55, w19, fs=f19, lines=(a19, b19), show_out=True)
content("The clipboard needs a display", "copy() and paste() worked on a virtual display and failed without one",
        [dg, dcap, p19,
         foot("NOT EXECUTED: Windows, macOS and a real screen. " + SAY_VD + " " + hid(pn, a19, b19, "the start of Xvfb and the helper").replace("Lines", "Lines", 1),
              x19, round(bot19 + 0.05, 2), w19, fs=8.5)],
        "The sequence diagram is the chapter's clipboard: the program calls pyperclipimg.copy() with an Image, the clipboard holds the image and copy() returns None, and a later paste() returns the image as an Image object; "
        "with text on the clipboard paste() raises UnidentifiedImageError. The program on the right ran for real on a virtual X display, Xvfb, with the real xclip and pyperclipimg 0.2.0, and it is a local stand-in for a screen, because nobody sees the picture. "
        "With DISPLAY set, copy() returned None and paste() returned a PNG image in mode RGB of 40 by 30 pixels whose pixels equal the original; without DISPLAY copy() also returned None, and paste() raised ChildProcessError with xclip's message that it cannot open the display. "
        "The research also found that with no xclip the import itself raised NotImplementedError, that the clipboard offered image/png, and that Image.show() started xdg-open and a display program, with a screenshot of the virtual screen matching 5 of 6 probe pixels of zophie.png. "
        "Windows and macOS were never used, and no real screen was looked at, so how the clipboard behaves there is read from the library's page and not run. The corpus program clipboardOnXvfb_v1_0_0.py is the same experiment with more checks. "
        "The program in the panel is the part of the program from the child's code onward; the start of Xvfb and the helper that runs the child with and without DISPLAY are not shown.",
        "A clipboard needs a display and a clipboard owner, even for pictures.", notexec=True)

# ---- 20 four graphs --------------------------------------------------------------------------------------------------------------------------------------
pn = "plotsFourCut_v1_0_0.py"
a20, b20 = span(pn, "def fig(", "autopct")
f20 = 7.0
w20 = pw(pn, (a20, b20), True, f20)
p20, bot20 = prog(pn, 0.5, 1.55, w20, fs=f20, lines=(a20, b20), show_out=True)
x20 = round(0.5 + w20 + 0.2, 2)
iw = round((9.5 - x20 - 0.08) / 2, 2)
ims = []
for k, fn in enumerate(("line.png", "scatter.png", "bar.png", "pie.png")):
    it, ib, _ = img(fn, round(x20 + (k % 2) * (iw + 0.08), 2), round(1.45 + (k // 2) * (iw * 0.8 + 0.06), 2), iw, round(iw * 0.8, 2))
    ims.append(it)
yb20 = round(1.45 + 2 * (iw * 0.8 + 0.06), 2)
content("Four graphs with pyplot", "plot, scatter, bar and pie each return an object; savefig writes 100 dpi",
        [p20] + ims + [imgcap(["line.png", "scatter.png", "bar.png", "pie.png"], 0.5, round(bot20 + 0.04, 2), w20, fs=8),
         foot(hid(pn, a20, b20, W_HEAD, "the prints of the colour and of the file, and the saving"), 0.5, round(bot20 + 0.5, 2), w20, fs=8),
         foot("Recorded 13 Oct 2026: pie() returns a tuple up to Matplotlib 3.10.8 and a PieContainer from 3.11.", x20, yb20, round(9.5 - x20, 2), fs=8.5)],
        "plt.plot(), plt.scatter(), plt.bar() and plt.pie() draw on the current axes of the current figure, and savefig() writes the figure as a PNG. The program makes the four graphs of the chapter at 3 by 2.4 inches, so each file is 300 by 240 pixels; the four pictures are the files it saved, and the build compares each with what the program saves now. "
        "plt.bar() returns a BarContainer whose heights are NumPy integers, which Matplotlib 3.11.2 with NumPy 2.5.4 prints as np.int64(3), np.int64(1) and np.int64(2); plt.pie() returned a PieContainer in 3.11.2, and with autopct it unpacks to three items, wedges, texts and autotexts. "
        "The research recorded that pie() returns a tuple up to Matplotlib 3.10.8 and a PieContainer from 3.11, so code that unpacks the result into two or three names breaks differently by release; the next slide runs both in the two environments. "
        "A line's colour is a tuple of three floats in 3.11.2 and a string in 3.9.2. The default figure is 6.4 by 4.8 inches, so with the default 100 dpi a PNG is 640 by 480 pixels; a PNG that Matplotlib saves is RGBA and carries the density 100 dpi, where Pillow's own PNGs carry none. "
        "The corpus program pyplotReturns_v1_0_0.py ran too: xlabel, ylabel and title return Text objects, legend() returns a Legend, scatter returns a PathCollection and hist returns three items.",
        "Each graph call returns an object, and its type depends on the release.", recorded=True)

# ---- 21 the pins ----------------------------------------------------------------------------------------------------------------------------------------------------
tbe = EX["_tables"]["environments"]["rows"]
tbl21 = {"t": "table", "x": 0.5, "y": 1.45, "w": 5.6, "colW": [1.45, 0.8, 1.0, 0.78, 1.57], "fs": 7.5, "rowH": 0.23, "rows": tbe}
c21, bot21 = con("pins", 6.3, 1.45, 3.2, fs=9, cap=True)
content("The pins of Appendix A, run now", "matplotlib==3.92 is not a release; the pins ran as a source build on 3.14.6",
        [tbl21, c21,
         *stack(["Recorded 13 Oct 2026: PyPI lists no Matplotlib 3.92 among 85 plain-numbered releases; the first CPython 3.14 wheels are Pillow 11.3.0 and Matplotlib 3.10.5.",
                 "NOT EXECUTED here: Matplotlib 3.10.0 on Python 3.14.6, where no wheel exists. 3.9.2 on 3.14.6 in the table is a build from source."],
                6.3, round(bot21 + 0.06, 2), 3.2, fs=8.5, gap=0.08),
         foot("The table runs the probe in four interpreters while the deck is checked.", 0.5, 4.75, 5.6, fs=9)],
        "Appendix A of the book pins pillow==10.4.0 and matplotlib==3.92. There is no Matplotlib 3.92: the release the book means is 3.9.2, and pip or uv answers that no such version exists. The console shows what a version parser makes of it, Version('3.92') is a different version from Version('3.9.2') "
        "and is greater than 3.11.2, so a pin written the way the book writes it can never be the old release. The table is the same probe run under four interpreters when the deck is built: Python 3.14.6 with the newest packages, Python 3.14.6 with the pins, built from source because neither Pillow 10.4.0 nor Matplotlib 3.9.2 has a wheel for 3.14, "
        "Python 3.13.14 with the pins as wheels, and an empty Python 3.14.6. Under the pins on 3.14.6 savefig() and legend() raised RecursionError, while on 3.13.14 the same pins saved and drew a Legend; the pie returned a tuple and a line's colour a string in both pin environments, and a PieContainer and a tuple of floats in the newest. "
        "Pillow's filename of an opened file is the full path in the pins and the bare name in 12.3.0, and the empty environment raises ModuleNotFoundError on import and PackageNotFoundError for both packages. "
        "The research also found that Matplotlib 3.9.2's TkAgg backend failed with ImportError against Tk 9.0 in Python 3.14.6 and 3.13.14, while 3.11.2 opened its windows. What the research could not run, Matplotlib 3.9.2 and 3.10.0 as wheels on Python 3.14.6, is marked on the slide because those wheels do not exist. "
        "The console needs the packaging module, so it does not run in a Python in a browser unless packaging is installed.",
        "Appendix A pins a version that does not exist.", notexec=True, recorded=True)

# ---- 22 the life of a pyplot figure -------------------------------------------------------------------------------------------------
dg, dcap = diagram("TheLifeOfAPyplotFigure", "lifecycle_multi", (0.5, 1.4, 4.4, 2.9), fs=8, sw=1.4, sh=0.36, sfs=8, top=0.28, lab_w=1.2, margin=1.4)
pn = "aggFigureCut_v1_0_0.py"
a22, b22 = span(pn, "def parts")
f22 = 7.0
w22 = pw(pn, (a22, b22), True, f22)
x22 = round(9.5 - w22, 2)
p22, bot22 = prog(pn, x22, 1.55, w22, fs=f22, lines=(a22, b22), show_out=True)
content("The life of a pyplot figure", "Agg keeps the figure after show(); every plot call adds to the current axes",
        [dg, dcap, p22,
         foot("NOT EXECUTED: the window of plt.show() on a real screen; Agg never opens one. " + hid(pn, a22, b22, W_HEAD).replace("Lines", "Lines", 1),
              x22, round(bot22 + 0.05, 2), w22, fs=8.5),
         foot("Appendix B, answer 12, says plt.show() resets the graph data; under Agg it did not.", 0.5, 4.65, 4.4, fs=8.5)],
        "pyplot remembers a current figure and a current axes, and every call draws on them. The state diagram is the chapter's and the program's: a new figure has no lines; plt.plot() draws on the current axes and the figure holds lines; "
        "under the Agg backend plt.show() returns None and keeps the figure, and so does savefig(); with a window backend the user closes the window and the figure is gone. The program shows the first part for real: two plot calls give two lines and the list of figures [1]; show() returns None and the list is still [1]; "
        "plt.bar() on the same axes adds two bars to the two lines, which is why the book's later examples draw on the figure of the earlier ones unless plt.figure() or plt.clf() is called; clf() and one plot leaves one line; plt.figure() makes figure 2 with nothing in it; close('all') leaves the empty list. "
        "Appendix B of the book answers question 12 with the statement that plt.show() resets the graph data, and with Agg it does not: the corpus program aggFigureLifecycle_v1_0_0.py saved the figure before and after show() and the two files were equal. "
        "The sentence is true only for a window backend, where closing the window closes the figure, and the research did not run a window on a real screen, so that half of the diagram is the chapter's word and is marked on the slide. "
        "The research did open Matplotlib 3.11.2's Tk windows on the virtual display. The diagram has two loops on the plotted state, show() and savefig(), which is why it is drawn with the loops at the left of the state.",
        "pyplot draws on the current figure until you start a new one.", notexec=True)

# ---- 23 showing a graph in a window -------------------------------------------------------------------------------------------------
dg, dcap = diagram("ShowingAGraphInAWindow", "sequence", (0.5, 1.4, 4.3, 2.75), fs=8, head_w=1.1)
x23 = 5.0
c23, bot23 = con("window", x23, 1.45, round(9.5 - x23, 2), fs=9, cap=True)
im23, ib23, _ = img("accumulated.png", x23, round(bot23 + 0.05, 2), 1.45, round(4.38 - bot23 - 0.05, 2))
content("Showing a graph in a window", "Save before you show; with a window backend the second savefig is blank",
        [dg, dcap, c23, im23,
         imgcap(["accumulated.png"], round(x23 + im23["w"] + 0.1, 2), round(bot23 + 0.05, 2), round(9.5 - x23 - im23["w"] - 0.1, 2), fs=8),
         foot("NOT EXECUTED: a window on a real screen. The blank image is the chapter's account of a window backend.",
              round(x23 + im23["w"] + 0.1, 2), round(bot23 + 0.5, 2), round(9.5 - x23 - im23["w"] - 0.1, 2), fs=8.5),
         factrow("Matplotlib2003", y=4.58)],
        story_notes("Matplotlib2003") + " The sequence diagram is the chapter's advice: call savefig() before show(), because show() blocks until the user closes the window, a second show() returns at once, and a savefig() after the window saves a blank image of a new figure. "
        "The console runs the part that can be run without a window: with the Agg backend, plt.plot() draws a line, calling show() twice changes nothing, and the current axes still hold the one line and the list of figures is still [1]; the backend is Agg. "
        "The small picture is the graph of the previous slide's program, a figure with two lines and two bars drawn on the same axes, saved by the program and compared by the build with what it saves now. "
        "The window was not shown on a real screen. The research opened a Tk window on the virtual display with Matplotlib 3.11.2 and took a screenshot of the display, and Matplotlib 3.9.2's TkAgg backend failed against Tk 9.0; "
        "neither is a statement about how the window looks to a person, and the blank second image is read from the chapter and not run.",
        "Save the figure first, then show it.", notexec=True)

# ---- 24 summary: the mind map --------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("MakingGraphsAndManipulatingImagesAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. Image fundamentals: a colour is four integers from 0 to 255, the origin is the top left pixel, and a box excludes its right and bottom edge. Image editing: paste() changes the image in place, resize() takes integers only, and rotate() fills the corners by the mode of the picture. "
        "The logo project: resize only if both sides are larger than 300, paste the logo with the logo as the mask, and remember that the page has an en dash where the file has a minus sign. Drawing and the clipboard: a rectangle includes its last pixel, textbbox() replaced textsize(), and copy() needs xclip and a display. "
        "Matplotlib graphs: Agg returns from show() at once, pie() returns a PieContainer in 3.11, and savefig() comes before show(). The book and practice: Green of Table 21-1 is lime, matplotlib==3.92 is not a release, and the second edition used textsize. "
        "Together they answer the first question of the chapter, what a program can be shown to do with a picture on a machine with no screen and what can only be shown to fail, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 21 - free online", PUB["P01"][2]],
         ["Appendix A: installing third-party modules", PUB["P05"][2]],
         ["Online materials of the 3rd edition (zip)", PUB["P02"][2]]]
_ref = [["Pillow: Image module", PUB["P08"][2]],
        ["Pillow: ImageDraw module", PUB["P10"][2]],
        ["Matplotlib: pyplot.pie", PUB["P30"][2]],
        ["pyperclipimg README", PUB["P38"][2]]]
_hist = [["PNG (Wikipedia)", STORY["Png1996"]["link"]],
         ["JPEG (Wikipedia)", STORY["Jpeg1992"]["link"]]]
_std = [["PNG specification, third edition (W3C)", PUB["P42"][2]],
        ["Pillow image file formats", PUB["P13"][2]]]
LINKS = [r[1] for r in _read + _ref + _hist + _std]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "Stories in the notes", "rows": _hist},
            {"head": "Standards", "rows": _std}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the chapter; the online materials are the zip of 91 files that the programs of this deck download and check by SHA-256, and Appendix A is where the book pins Pillow 10.4.0 and the Matplotlib release it writes as 3.92. "
        "The reference links are the pages of Pillow and Matplotlib that the chapter relies on and the README of pyperclipimg. Four of the six stories of the chapter are on slides with their own link, on the slide itself: Russell Kirsch and the first scanned picture, alpha compositing, the Python Imaging Library and Matplotlib. "
        "The other two, on PNG and on JPEG, are told in the notes of the slide about saving, and their pages are the third group. The last group is the PNG specification of the W3C and the Pillow page on file formats. "
        "The rest of the sixty sources of the research, among them the release notes of Pillow, the API changes of Matplotlib, the PyPI metadata and the standards for JPEG and JFIF, are in the research package. No photograph of a person is used in the deck.",
        "Textbook, documentation, standards and history, all opened today.")

# ---- 26 closing ------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "A box has its left and top, not its right and bottom; crop() and paste() copy first.",
            "A rotated corner is filled by the mode; a PNG has no dpi unless you give one.",
            "textbbox() measures text; the clipboard and a window need a display.",
            "Appendix A pins a release that does not exist; pie() changed in 3.11."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 10, "big": False,
          "items": ["%d console rows" % ROWS_SHOWN, "%d programs run" % len(PROGS), "8 diagrams", "16 pictures"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The console rows of the grid, the box, the answer of Appendix B, the Agg window and the pins need Pillow, Matplotlib or packaging, so they run in a Python that has those; the first three need only Pillow, and the version rows need packaging. "
        "The rows were run again under Python 3.14.6 each time the deck was built, and the programs, and with them the sixteen pictures, were run again by the check that compares the slides with the recording. "
        "What was not run is marked on its slide: Windows and macOS, a real screen, Matplotlib 3.9.2 and 3.10.0 as wheels on Python 3.14.6, and the licence of the cat picture was not checked. Nothing was ever shown to a person on a screen by the clipboard program. "
        "The next chapter of the book automates the keyboard and the mouse, and what this chapter taught about checking what a program saves, and about reading a printed output with care, carries over.",
        "Questions are welcome; bring a picture problem to run.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Colours, grids and coordinates", "What a program can do with an image", "Coordinates and box tuples"),
          ("Cropping, pasting, masks, rotating, saving", "Cropping a picture", "Saving: PNG, JPEG and pixel density"),
          ("Project 16: a logo on every picture", "Project 16: a logo on every picture", "Project 16, as printed and as shipped"),
          ("Drawing, text, Pillow releases, practice", "Drawing shapes on a picture", "The practice programs: cards and folders"),
          ("The clipboard and Matplotlib graphs", "The clipboard needs a display", "Showing a graph in a window"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nconsole = sum(1 for s in S for i in s["items"] if i.get("t") in ("code", "prog"))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
_npic = sum(1 for s in S for i in s["items"] if i.get("t") == "img")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, 6 - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, 6 - _nstory)},
        {"n": str(_npic), "label": "pictures, each saved by a program that is run again"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from a grid of numbers to a graph."
S[1]["notes"] = ("The route has six parts. It starts with colours, grids and coordinates: what a program can do with one image, the first scanned picture as a grid of numbers, colours and Table 21-1, and the coordinates and box tuples. "
                 "Then the editing: cropping, pasting and tiling, masks and the alpha channel, resizing, rotating and flipping, and saving as PNG or JPEG with the question of pixel density. The third part is Project 16, a logo on every picture, as a flow chart and as the file that ships. "
                 "The fourth is drawing shapes, text and fonts, the Pillow releases that changed the chapter, and the practice programs. The fifth is the clipboard and Matplotlib: the four graphs, the pins of Appendix A run now, the life of a pyplot figure and showing a graph in a window. "
                 "The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. Four of the six stories are on slides, each with a link, and two, on PNG and on JPEG, are told in the notes of the slide about saving; the eight narrative diagrams of the chapter are drawn from the same specifications as the interactive page. "
                 "Every output was printed by Python %s with Pillow 12.3.0, Matplotlib 3.11.2, NumPy 2.5.4 and pyperclipimg 0.2.0, the clipboard ran on a virtual display, and what could not be run is marked on its slide." % PYV)

for s in S:
    if not str(s.get("notes", "")).strip():
        raise SystemExit("REFUSED: slide %r has no speaker notes" % s["title"])
    for i in s["items"]:
        if i.get("t") == "bullets" and len(i["items"]) > 5:
            raise SystemExit("REFUSED: too many bullets on %r" % s["title"])
if len(S) != 26:
    raise SystemExit("REFUSED: %d slides, the plan is 26" % len(S))
if set(SHOWN) != set(DIAG):
    raise SystemExit("REFUSED: diagrams not on a slide: %r" % (set(DIAG) - set(SHOWN)))
_pics = [i["path"].split("/")[-1] for s in S for i in s["items"] if i.get("t") == "img"]
if sorted(_pics) != sorted(EX["_images"]):
    raise SystemExit("REFUSED: pictures on slides %r differ from the recording %r" % (sorted(_pics), sorted(EX["_images"])))
plan = {"meta": {"title": "Ch. 21: Graphs and Images", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "recorded": RECORDED,
                 "standin": {str(k): v for k, v in STANDIN.items()}}, "slides": S}
if LATE:
    raise SystemExit("REFUSED:\n" + "\n".join(LATE))
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; Recorded on slides", RECORDED)
