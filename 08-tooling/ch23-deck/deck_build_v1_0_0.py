#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 23 (Controlling the Keyboard and Mouse) on the CME classroom standard.

Same regime as chapters 10 to 22: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources, full-sentence takeaway
strips, stories with fact rows, consoles and programs (whole or honest excerpts, labelled with their line numbers) with their results as Python printed
them. Every console result and program transcript comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with PyAutoGUI
0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, PyTweening 1.2.0, PyGetWindow 0.0.9, MouseInfo 0.1.3, pyperclip 1.11.0, python3-xlib 0.15, Pillow 12.3.0, NumPy 2.5.4 and
OpenCV 5.0.0.93); the speaker notes are prose for the reader and carry only what the chapter's RDODI research package (03-materials/ch23/rdodi,
sen0414_ch23_rdodi_data_v1_0_2.py, findings F1 to F22), its records (08-tooling/ch23-page/*.json) or a program of this deck established.

What this chapter adds against chapter 22: EVERY PROGRAM RUNS ON A VIRTUAL X DISPLAY. PyAutoGUI sends input to a screen, and no screen of this machine may be touched,
so each program starts its own Xvfb (with the openbox window manager where it needs one) and real X clients on it (a Tk window that logs the events it receives,
xdotool, xclip, xterm, the MouseInfo window). What a program prints is what those clients received; nobody sees the screen. Every slide that shows such a program
says 'Virtual display' and 'not a real screen' and 'local stand-in' (honesty_check_v1_0_0.py requires the words). Twelve corpus programs of the chapter's
research (their lines are wider than a slide; they ran and are recorded but not shown, and their timing-dependent values are never quoted) and eighteen programs
written for the deck (the Cuts) were run, each twice, and the runner refuses a program whose transcript or picture differs between the two runs. Six pictures that
programs saved are placed on the slides as images; each caption names the program ('image <file> made by <program>') and program_check_v1_0_0.py runs that
program again and requires the slide to carry a picture byte-identical (or pixel-identical) to what the program saves now. What the research recorded on
13 October 2026 and the deck does not run again is on a slide as 'Recorded'. What could not be run is marked NOT EXECUTED on its slide (meta.notExecuted). The
eight narrative diagrams of the chapter (sen0414_ch23_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py) and
checked by diagram_check_v1_0_0.py; three tables (the same probe in five interpreters at check time, the release matrix, and the five replay rows of the
research) and two charts are native PowerPoint objects whose data the deck check computes again. All six stories are on slides; no photograph is used (the
single request to Wikimedia Commons answered 429).

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


ST = load("stories23", os.path.join(HERE, "..", "sen0414_ch23_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams23", os.path.join(HERE, "..", "sen0414_ch23_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi23", os.path.join(HERE, "..", "sen0414_ch23_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
CAP = "run under Python %s; no row reads the clock or the network" % PYV
G = {k: [[s, (o or "")] for s, o in v] for k, v in EX.items() if not k.startswith("_")}
PROGS = EX["_programs"]
IMGDIR = os.path.join(HERE, "images")
CQ1, CQ2 = RD.CQS
CW = 0.0088  # inches per character per point of Courier New, as the shared fit check measures it

L_NOTEXEC = "NOT EXECUTED"
L_REC = "Recorded"


def lines_of(rows):
    return sum(1 + (1 if out.strip() else 0) for _, out in rows)


ROWS_SHOWN = len(G["title"]) + len(G["pins"])  # the "lang" console is recorded but not shown


def con(group, x, y, w, fs=11, label=None, cap=True, rows=None):
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
        it["label"] = label
    return it, round(y + h + (0.26 if cap else 0), 2)


def span(pname, first, last=None):
    """1-based line numbers (a, b) of the program lines from the first containing `first` to the first containing `last`."""
    ls = PROGS[pname]["code"].rstrip("\n").split("\n")
    a = next(i for i, l in enumerate(ls, 1) if first in l)
    b = len(ls) if last is None else next(i for i, l in enumerate(ls, 1) if i >= a and last in l)
    return a, b


def body(pname):
    """the first line of a Cut that is shown: the 'with Desk(' line (or the import line of python-xlib above it, never shown)"""
    return span(pname, "with Desk(")[0]


def pw(pname, lines=None, out=True, fs=7.0):
    pr = PROGS[pname]
    L = pr["code"].rstrip("\n").split("\n")
    a, b = (1, len(L)) if lines is None else lines
    ws = [len(l) for l in L[a - 1:b]]
    if out and pr["transcript"]:
        t = pr["transcript"].split("\n")
        ws += [len(t[0]) + 7] + [len(x) for x in t[1:]]
    return round(max(ws) * CW * fs + 0.4, 2)


def bestfs(pname, lines, wmax, hmax, out=True, lo=7.0, hi=9.5):
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
    """A chapter program (or an honest excerpt) with its transcript, sized from its text; returns (item, bottom y)."""
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


def pfit(pname, x, y, wmax, hmax, a=None, b=None, right=False, lo=7.0, hi=9.0):
    """prog() of the lines a to b of a Cut (default: the body after 'd = wd()' to the last line) at the largest size that fits wmax x hmax;
    right=True puts the panel against the right margin. Returns (item, bottom y, a, b, x, w)."""
    a = body(pname) if a is None else a
    b = len(PROGS[pname]["code"].rstrip("\n").split("\n")) if b is None else b
    f = bestfs(pname, (a, b), wmax, hmax, lo=lo, hi=hi)
    w = pw(pname, (a, b), True, f)
    x = round(9.5 - w, 2) if right else x
    it, bot = prog(pname, x, y, w, fs=f, lines=(a, b), show_out=True)
    return it, bot, a, b, x, w


def factrow(sid, x=0.5, y=4.58, w=9.0):
    st = STORY[sid]
    host = st["link"].split("//")[1].split("/")[0].replace("www.", "")
    return {"t": "factrow", "x": x, "y": y, "w": w, "who": st["who"], "where": st["where"],
            "when": st["when"], "link": st["link"], "linkText": host}


def story_notes(sid):
    st = STORY[sid]
    return st["story"] + " The account rests on these sources. " + st["source"]


def card(head, body_, x, y, w, h, fs=11.5, accent=None):
    if len(head) > (w - 0.4) / 0.112:
        raise SystemExit("REFUSED: card heading %r does not fit one line of a %.2f in card" % (head, w))
    it = {"t": "card", "head": head, "body": body_, "x": x, "y": y, "w": w, "h": h, "fs": fs}
    if accent:
        it["accent"] = accent
    return it


def foot(body_, x, y, w, fs=9.5):
    h = round(DS.need_h(body_, w, fs) + 0.04, 2)
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body_}


def stack(bodies, x, y, w, fs=8.5, gap=0.04):
    out = []
    for b in bodies:
        f = foot(b, x, round(y, 2), w, fs=fs)
        out.append(f)
        y = f["y"] + f["h"] + gap
    return out


def diagram(did, kind, box, **kw):
    """The shapes item of a narrative diagram and its caption (which names the diagram and its measured grounding)."""
    d = DIAG[did]
    fn = {"activity": DS.activity, "sequence": DS.sequence, "lifecycle": DS.lifecycle_col, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
    it = fn(d["data"], box, **kw)
    h, n = d["grounding"]
    body_ = "diagram %s - %s pattern, %d of %d words grounded in the chapter's text" % (did, d["pattern"], h, n)
    cap = {"t": "foot", "x": box[0], "y": round(box[1] + box[3] + 0.03, 2), "w": box[2], "h": round(DS.need_h(body_, box[2], 8.5) + 0.04, 2), "fs": 8.5,
           "body": body_}
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
    body_ = "; ".join("image %s made by %s" % (fn, EX["_images"][fn]["program"]) for fn in fns)
    return foot(body_, x, y, w, fs=fs)


def tpanel(pname, x, y, w, fs=7.5):
    pr = PROGS[pname]
    t = pr["transcript"].split("\n")
    need = round(max(len(l) for l in t) * CW * fs + 0.4 + 0.5, 2)
    if need > w + 0.005:
        raise SystemExit("REFUSED: the transcript of %s needs %.2f in at %.1f pt, the panel has %.2f" % (pname, need, fs, w))
    h = round(len(t) * (fs * 1.22 / 72.0 + 0.02) + 0.30, 2)
    label = "transcript of program %s" % pname
    return {"t": "prog", "x": x, "y": max(y, 1.55), "w": w, "h": h, "lines": [], "fs": fs, "compact": True, "out": pr["transcript"], "outLabel": "prints", "label": label}, round(max(y, 1.55) + h, 2)


S = []
SHOWN = {}
NOTEXEC = []
RECORDED = []
STANDIN = {}
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


def hid(pn, a, b, what_before="imports, helpers, the folder and the download check", what_after=None):
    """The words that say which lines of the program are not on the slide: lines 1 to a-1, and lines b+1 to n."""
    n = len(PROGS[pn]["code"].rstrip("\n").split("\n"))
    out = []
    if a > 1:
        out.append(("Lines 1 to %d (%s) are not shown." % (a - 1, what_before)) if a > 2 else ("Line 1 (%s) is not shown." % what_before))
    if b < n:
        out.append(("Lines %d to %d (%s) are not shown." % (b + 1, n, what_after or "the rest")) if b + 1 < n else ("Line %d (%s) is not shown." % (n, what_after or "the rest")))
    return " ".join(out)



SAY_VD = "Virtual display: Xvfb with real X clients, a local stand-in for a screen, not a real screen; nobody sees it."
REC = "Recorded 13 Oct 2026"
NE = "NOT EXECUTED here"


def rec(t):
    return "Recorded 13 Oct 2026: " + t


def ne(t):
    return "NOT EXECUTED here: " + t


def capfoot(cap, extra, x, y, w, fs=8):
    """the caption of a diagram ('diagram <id> - <pattern> pattern, ...') followed by more text, as one foot placed where there is room"""
    return foot(cap["body"] + ". " + extra, x, y, w, fs=fs)


def cut(pn):
    return PROGS[pn]["code"].rstrip("\n").split("\n")


# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.25, 4.5, fs=8, cap=False)
S.append({"kind": "title", "title": "Ch. 23: Keyboard and Mouse",
          "sub": "Controlling the keyboard and mouse with PyAutoGUI: fail-safes, clicks, screenshots, typing and message boxes",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made, and every picture was saved by a program that is run again to check it. "
                             "Windows, macOS and a real screen were never used: every program ran on a virtual display, and what could not be run is marked on its slide.",
                             0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 22 taught a program to read pictures. Chapter 23 teaches a program to act on the screen: PyAutoGUI sends the movements of the mouse and the keys of the keyboard that a person would send, and it can take a screenshot and look for a picture in it. "
                   "The chapter has %d listings, %d figures and %d table, and ends with 13 practice questions and 3 practice programs. "
                   "This deck follows the chapter in its own order: the fail-safes, the mouse, the screen and images, the keyboard, and the message boxes, and it adds what the research found when the chapter's %d printed statements were run again. "
                   "Every program of the deck runs on a virtual X display, Xvfb, with real X clients such as a Tk window, xdotool, xclip and xterm, so what a program prints is what those windows received. "
                   "Nobody looks at that screen, which is why the deck calls it a virtual display, not a real screen. "
                   "Every output on the slides was printed by Python %s with PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1 and Pillow 12.3.0, the versions the console above prints. "
                   "Windows and macOS were never used, and neither were a real Wayland session, a second monitor or a high-resolution screen. "
                   "What could not be run is marked on its slide, and what the research measured and this deck does not run again is marked Recorded." % (25, 6, 1, 80, PYV),
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
_nb = len(DIAG["ControllingTheKeyboardAndMouseAtAGlance"]["data"]["branches"])
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.3, "fs": 11, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["%d branches" % _nb, "%d topics" % len(NODES), "%d console rows" % ROWS_SHOWN,
                    "%d programs run" % len(PROGS), "%d diagrams" % len(DIAG), "%d pictures" % len(EX["_images"]), "Python %s" % PYV]}],
        "The first question is the spine of the chapter, and the deck answers it slide by slide. On a machine with no real screen, a program can move a pointer, press buttons and keys, scroll, take a screenshot, find a picture in it and show a message box, and every one of those can be observed because X windows report what they receive. "
        "What cannot be shown to work is the part that needs a person's machine: Windows, macOS, a real Wayland compositor, a second monitor, a high-resolution screen and the games and chat programs the chapter mentions. "
        "The second question is the watch-out. The chapter's 25 listings hold 80 statements, and the research ran them as printed. "
        "With Python 3.14.6 and the newest packages 40 of the 80 matched the book's output, 52 ran without an exception and 28 raised; without OpenCV 40 matched, with PyScreeze 0.1.28 41 matched, under Python 3.12.3 with Tk 8.6.14 40 matched and 53 ran, and in an empty environment 1 matched. "
        "The statements that differ are the pointer positions, the pixel((50, 200)) call, the Box values, the window objects, mouseInfo() and the spiralDraw.py listing. Each slide says where a printed line differs and on what evidence.",
        "Know what can be shown to work and what can only be shown to fail.")

# ---- 4 what a script can do ---------------------------------------------------------------------------------------
dg, dcap = diagram("WhatAScriptCanDoWithPyAutoGUI", "usecases", (0.5, 1.4, 4.6, 2.75), fs=8)
c4, bot4 = con("pins", 5.3, 1.45, 4.2, fs=8, cap=True)
content("What a script can do with PyAutoGUI", "Eight uses; the chapter mentions release 1.0.0, which PyPI does not list",
        [dg, dcap, c4,
         foot(rec("PyPI lists 50 releases of PyAutoGUI, 0.9.54 the newest and none numbered 1.0.0; the chapter mentions 1.0.0 in 3 passages."), 5.3, round(bot4 + 0.08, 2), 4.2, fs=9),
         factrow("Mouse1968", y=4.58)],
        story_notes("Mouse1968") + " The use-case diagram lists what a script can do through PyAutoGUI: move the mouse with moveTo(), click with click(), drag with drag(), scroll with scroll(), take a screenshot, find an image with locateOnScreen(), type text with write() and show a message box with confirm(). "
        "They are independent calls to one library, which is why the picture is a set of uses and not a sequence. "
        "The console runs under the interpreter of the deck: the installed PyAutoGUI is older than 1.0.0 and the installed PyScreeze, which does the locating, is 1.0.0 or newer, and importing pyautogui in a process with no DISPLAY raises KeyError: 'DISPLAY', which shows that the import reads the DISPLAY variable. "
        "The card records what the research found on 13 October 2026 and this deck does not run again: the chapter's page returned 200 with 103,072 bytes and holds 25 listings, 6 figures and 1 table; the online materials are a zip of 91 files, 72 of them Python, and none of them is pyautogui.py, submit.png, screenshot.png or mouseInfoLog.txt, which the chapter names; "
        "PyScreeze has 29 releases and its 1.0.0 and 1.0.1 are of 20 August 2024. The installed set was PyAutoGUI 0.9.54, PyScreeze 1.0.1, PyMsgBox 2.0.1, PyTweening 1.2.0, PyGetWindow 0.0.9, MouseInfo 0.1.3 and python3-xlib 0.15.",
        "A script can do with code what a hand does with a mouse.", recorded=True)

# ---- 5 packages, display and session ------------------------------------------------------------------------------------
pn = "waylandCut_v1_0_0.py"
tbe = EX["_tables"]["environments"]["rows"]
tbl5 = {"t": "table", "x": 0.5, "y": 1.45, "w": 3.9, "colW": [0.8, 0.55, 0.55, 0.55, 0.55, 0.9], "fs": 7, "rowH": 0.22, "cellMargin": [0.02, 0.04, 0.02, 0.04], "rows": tbe}
p5, bot5, a5, b5, x5, w5 = pfit(pn, 4.6, 1.55, 5.1, 2.5, right=True)
content("Packages, display and session", "No DISPLAY, no import; under Wayland a screenshot fails while moveTo still works",
        [tbl5, p5,
         foot(SAY_VD + " " + hid(pn, a5, b5, "imports, the private display and the helpers that start child programs"), x5, round(bot5 + 0.05, 2), w5, fs=8),
         *stack([rec("the three backends are SendInput, mouse_event and keybd_event on Windows, CGEventPost and Quartz on macOS, and fake_input of the XTEST extension on Linux."),
                 ne("Windows, macOS, the accessibility permission of macOS and a real Wayland compositor; only the Linux path through X ran.")],
                0.5, 3.6, 3.9, fs=8, gap=0.05),
         factrow("XWindow1984", y=4.58)],
        story_notes("XWindow1984") + " The table runs one probe in five interpreters while the deck is checked: Python 3.14.6 with the newest packages, without OpenCV, with PyScreeze 0.1.28, Python 3.12.3 with Tk 8.6, and an empty Python 3.14.6. "
        "The probe imports pyautogui and calls size() on a virtual display, so every row with the packages answers 1920x1080, and the empty Python raises ModuleNotFoundError. "
        "The program starts three children on its own display. Without DISPLAY the import raises KeyError: 'DISPLAY'. With XDG_SESSION_TYPE set to wayland a screenshot raises PyScreezeException, while moveTo(300, 200) still works; the two results differ and the slide reports them as observed. "
        "That is a result of one program on one display and not a statement about a real Wayland compositor, which was never used; the Remote Desktop portal of XDG Desktop Portal and the Wayland protocol are documented in the research package. "
        "The research recorded that Windows documents SendInput as subject to UIPI and that macOS asks for the accessibility permission; none of those paths was run.",
        "The library needs an X display; nothing here ran on Windows or macOS.", notexec=True, recorded=True)

# ---- 6 how a click reaches a window --------------------------------------------------------------------------------------
pn = "xtestCut_v1_0_0.py"
dg, dcap = diagram("ScriptToXServer", "sequence", (0.5, 1.4, 4.7, 3.5), fs=8, head_w=0.9, gap0=0.0)
p6, bot6, a6, b6, x6, w6 = pfit(pn, 5.28, 1.55, 4.25, 2.8, right=True)
content("How a click reaches a window", "PyAutoGUI asks the X server to fake the input; the window cannot tell it from a mouse",
        [dg, p6,
         capfoot(dcap, SAY_VD + " " + rec("xterm discarded the 2 keystrokes ab sent with XSendEvent and took them only with allowSendEvents true."), x6, round(bot6 + 0.05, 2), w6)],
        "The sequence diagram follows one click(10, 5): the script calls PyAutoGUI, PyAutoGUI sends XTestFakeInput to the X server for the motion and for the press and release of the button, and the X server delivers the events to the window, which receives them as if from the real mouse. "
        "The program asks the question with real windows: the display has the XTEST extension, a click and a key press of PyAutoGUI reach the Tk window with send_event False, and the letter q sent with XSendEvent, the older way to put an event in a window, arrives with send_event True; both reached the entry. "
        "The line under the program records the finding about xterm: it discarded the 2 keystrokes ab sent with XSendEvent, received cd from PyAutoGUI and received ab only with allowSendEvents true, because a terminal may ignore events marked as sent unless that resource is true. That is why a program that fakes keys in an application may see them ignored, and why the XTEST route is the one PyAutoGUI uses. "
        "The Windows and macOS paths are named in the documentation and were never run.",
        "XTEST input looks like a real mouse to the window.", recorded=True)

# ---- 7 pauses and fail-safes ------------------------------------------------------------------------------------------------
pn = "pauseCut_v1_0_0.py"
dg, dcap = diagram("ACallWithTheFailSafeOn", "activity", (0.5, 1.4, 3.6, 2.6),
                   grid={"call": (0, 0), "pause": (0, 1), "corner": (0, 2), "raise": (0, 3), "next": (1, 2)},
                   cols=[(0.05, 1.6), (2.0, 1.6)], rows_n=4, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 3},
                   routes={("start", "call"): "h", ("corner", "next"): "h", ("raise", "end"): "h"}, fs=8, nh=0.44, dh=0.5)
p7, bot7, a7, b7, x7, w7 = pfit(pn, 4.3, 1.55, 5.2, 2.7, right=True)
content("Pauses and fail-safes", "A pause of 0.1 s follows each action call; a corner of the screen stops the program",
        [dg, dcap, p7,
         foot(SAY_VD, x7, round(bot7 + 0.04, 2), w7, fs=8),
         factrow("DeadMan1918", y=4.58)],
        story_notes("DeadMan1918") + " The flow chart is the fail-safe of the chapter: after a call, PyAutoGUI waits for the pause, then asks whether the cursor is in a corner of the screen; if it is, the next call raises the exception and the program stops, and if not the program goes on. "
        "The program sets PAUSE to 0.3 and times five calls. In the research PAUSE is 0.1 and 15 action functions pause after the call, 14 of them once and rightClick twice, while position, size, screenshot, pixel, onScreen and sleep do not. "
        "The program prints only whether a call waited longer than 0.25 seconds, because a duration changes from run to run and a boolean does not. "
        "The fail-safe is not a promise that the program stops by itself at once: the call that moves the pointer to a corner returns, and it is the next call that raises FailSafeException.",
        "Leave the fail-safe on; it is the way out of a runaway script.")

# ---- 8 corners ----------------------------------------------------------------------------------------------------------
pn = "cornersCut_v1_0_0.py"
p8, bot8, a8, b8, x8, w8 = pfit(pn, 0.5, 1.55, 5.7, 3.42)
xr = round(x8 + w8 + 0.2, 2)
content("Corners and the fail-safe points", "Four corners raise FailSafeException; the points are fixed when pyautogui is imported",
        [p8,
         *stack([SAY_VD, hid(pn, a8, b8, "imports, the private display and the helpers that start child programs"),
                 rec("the corners (0, 0), (1919, 0), (0, 1079) and (1919, 1079) made the next call raise FailSafeException, moveTo(0, 0) itself returned, and afterwards position, size and screenshot still ran while click, write and moveTo raised."),
                 rec("with 2 virtual monitors xrandr listed 3 monitors and size() still said (1920, 1080)."),
                 ne("a real second monitor, and what a real desktop does with hotkey('ctrl', 'alt', 'delete'); on the virtual display it only reached a window as three key presses.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.06)],
        "Only the four corners of the screen are fail-safe points, so a pointer at (1, 1) raises nothing, as the program prints. The points are computed when the module is imported: after the framebuffer was resized with xrandr from 1920 by 1080 to 1280 by 720, the process that was running kept the old corners and a new process saw (1279, 719). "
        "A script that runs for hours on a screen whose size can change must therefore be restarted, or must set its own points. The documentation says that only the primary monitor is handled, which fits what the research saw with two virtual monitors added: three monitors listed and a size that did not change. "
        "The chapter's hotkey('ctrl', 'alt', 'delete') was sent to a window of the virtual display, where the three keys arrived and were released in reverse order and nobody was logged out; what a real desktop does with them was never run.",
        "Four corners stop the program, and the list is fixed at import.", notexec=True, recorded=True)

# ---- 9 moving the mouse -------------------------------------------------------------------------------------------------------------
pn = "moveCut_v1_0_0.py"
p9, bot9, a9, b9, x9, w9 = pfit(pn, 0.5, 1.55, 5.4, 3.3)
xr = round(x9 + w9 + 0.2, 2)
ch9 = EX["_charts"]["moveEvents"]
chart9 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.4, "w": round(9.5 - xr, 2), "h": 1.9, "labels": ch9["labels"],
          "title": "Motion events by duration", "series": [{"name": "motion events", "data": ch9["values"]}], "dataLabels": True, "dlFs": 9}
content("Moving the mouse and where it is", "A longer duration means more small steps; points outside the screen are clamped",
        [p9, chart9,
         *stack([SAY_VD, hid(pn, a9, b9, "imports, the private display and the window that counts the motion events"),
                 rec("moveTo(40000, 500) raised struct.error, so the clamping stops at the limits of the X protocol.")],
                xr, 3.4, round(9.5 - xr, 2), fs=8, gap=0.05)],
        "A move without a duration is one jump, and a move with a longer duration is a series of small steps: the chart is the count of motion events the observer window received for the same move at five durations, and a duration of 0 and of 0.1 both gave a single event. "
        "In the research a duration of 0.25 made 6 events and 1.0 made 21; the numbers on the slide are this deck's own run of the same program. The steps follow the tweening function, a straight line unless a different one is passed. "
        "Points outside the screen do not raise an error: with the fail-safe off, (-50, -50) ended at (0, 0) and (5000, 5000) at the last pixel, because the X server clamps them. "
        "The program turns the fail-safe off for those two calls, which are on the screen's edge, and the point of the lines is that position() tells where the pointer really is, not where the script asked it to be.",
        "Time a move with duration; the pointer never leaves the screen.", recorded=True)

# ---- 10 clicking ----------------------------------------------------------------------------------------------------------------------
pn = "clickCut_v1_0_0.py"
p10, bot10, a10, b10, x10, w10 = pfit(pn, 0.5, 1.55, 5.8, 3.3)
xr = round(x10 + w10 + 0.2, 2)
content("Clicking", "Which button, how many clicks, how far apart; the window names a double click",
        [p10,
         *stack([SAY_VD, hid(pn, a10, b10, "imports, the private display and the window that records the buttons it receives")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.05)],
        "Each call is shown with the button presses that the observer window received. click() sends one left button press and release, button='middle' and rightClick() change the button to 2 and 3, and doubleClick() and tripleClick() send two and three presses in quick succession, which the Tk window reports as a Press followed by a DoubleClick, and by a DoubleClick and a TripleClick. "
        "click(clicks=2, interval=0.6) sends two clicks with a pause between them, and the window reports two single presses. "
        "Whether presses are a double click is decided by the window and its timing, not by PyAutoGUI, which only sends presses at the pointer. "
        "The call moves the pointer first when it is given coordinates, and clicks where it is when it is not, which is why the program moves to (700, 400) once and then calls click() with no arguments.",
        "A click is a press at the pointer; the window decides the rest.")

# ---- 11 dragging: the spiral ----------------------------------------------------------------------------------------------------------
pn = "dragCut_v1_0_0.py"
dg, dcap = diagram("TheLifeOfADrag", "lifecycle", (0.5, 1.4, 3.0, 2.2), fs=8, sw=1.4, sh=0.36, sfs=8, top=0.3, lab_w=1.5)
p11, bot11, a11, b11, x11, w11 = pfit(pn, 3.7, 1.55, 5.8, 3.0, a=span(pn, "distance, change")[0], right=True)
im11, ib11, _ = img("spiral.png", 0.5, round(dcap["y"] + dcap["h"] + 0.06, 2), 1.4, 0.95)
content("Dragging: the spiral", "drag() holds the button down while the pointer moves; the loop draws a square spiral",
        [dg, dcap, im11, imgcap(["spiral.png"], round(0.5 + im11["w"] + 0.1, 2), im11["y"], round(3.5 - im11["w"] - 0.6, 2), fs=8),
         p11,
         foot(SAY_VD + " " + hid(pn, a11, b11, "imports, the private display, the window that paints where the button is held and the first move"),
              x11, round(bot11 + 0.05, 2), w11, fs=8)],
        "The state diagram follows one drag: the cursor is at its place, drag() pushes the button down, the cursor moves in steps for the duration, and the button is released at the new location. "
        "The loop is the chapter's spiral: four drags per turn, each a little shorter than the one before, in a window that paints where the button is held; the program makes 32 calls and the picture is what the window painted, saved by the program. "
        "The press and release counts of the observer are 30 and 30, not 32, because the last two calls ask for a distance of zero and PyAutoGUI returns at once without pressing anything. "
        "The research recorded the first five calls, (300, 0), (0, 280), (-280, 0), (0, -260) and (260, 0), and a box of ink that is the same for the chapter's loop and for the shipped spiralDraw.py. That file has 580 bytes and 15 lines; it calls dragRel, waits with time.sleep(5) and uses a duration of 0.1 where the chapter prints 0.2, and the listing as printed in the chapter raises IndentationError.",
        "A drag is a press, a series of moves and a release.")

# ---- 12 scrolling --------------------------------------------------------------------------------------------------------------------------
pn = "scrollCut_v1_0_0.py"
p12, bot12, a12, b12, x12, w12 = pfit(pn, 0.5, 1.55, 5.5, 3.0)
xr = round(x12 + w12 + 0.2, 2)
ch12 = EX["_charts"]["scrollLines"]
chart12 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.4, "w": round(9.5 - xr, 2), "h": 2.0, "labels": ch12["labels"],
           "title": "Lines moved by scroll(n)", "series": [{"name": "lines", "data": ch12["values"]}], "dataLabels": True, "dlFs": 8}
content("Scrolling", "scroll(n) counts wheel clicks; a Tk 9 window moves fewer lines than a Tk 8.6 window",
        [p12, chart12,
         *stack([SAY_VD, hid(pn, a12, b12, "imports, the private display and the text window that reports its first visible line"),
                 rec("scroll(3) sent 3 presses of button 4, scroll(-2) 2 of button 5, hscroll(2) 2 of button 7 and hscroll(-1) 1 of button 6.")],
                xr, 3.5, round(9.5 - xr, 2), fs=8, gap=0.05)],
        "scroll(n) sends n wheel clicks, up for a positive number and down for a negative one, and what a click means is the toolkit's business: the same four calls moved a text widget by different numbers of lines under Tk 9.0.3 and under Tk 8.6.14. "
        "The program scrolls to the top before every call and prints how many lines the first visible line moved, and the chart plots the eight numbers it printed. The research found 1, 3, 5 and 19 lines under Tk 9.0.3 and 2, 5, 8 and 29 under Tk 8.6.14; the chart is this deck's own run. "
        "The chapter advises to experiment with the numbers, and the result agrees. The research also saw, on the X wire, that scroll sends the buttons 4 and 5 and hscroll the buttons 6 and 7, which is the card on the slide.",
        "Scroll units belong to the window, so test them where you run.", recorded=True)

# ---- 13 MouseInfo breaks under Tk 9 -----------------------------------------------------------------------------------------------------------
pn = "mouseinfoCut_v1_0_0.py"
p13, bot13, a13, b13, x13, w13 = pfit(pn, 0.5, 1.55, 6.0, 3.0)
xr = round(x13 + w13 + 0.2, 2)
im13, ib13, _ = img("mouseInfo.png", xr, 1.5, round(9.5 - xr, 2), 1.7)
content("MouseInfo breaks under Tk 9", "mouseInfo() is the chapter's tool for reading the pointer; it needs Tk 8.6",
        [p13, im13, imgcap(["mouseInfo.png"], xr, round(ib13 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_VD, hid(pn, a13, b13, "imports and the private display"),
                 rec("under Tk 8.6.14 F6 with the 3 Sec. Button Delay on logged 1600,850 after the pointer had moved from 1500,800, and with the delay off it logged 1500,800, 1600,850 and 1700,900; the Tcl 9.0 manual documents trace add variable and not the old trace variable.")],
                xr, round(ib13 + 0.35, 2), round(9.5 - xr, 2), fs=8, gap=0.05)],
        "MouseInfo is the small application that the chapter uses to read the position and the color under the pointer. pyautogui.mouseInfo() ends with TclError: bad option 'variable' under Tk 9.0.3, which comes with Python 3.13.14 up to 3.15.0b4, because MouseInfo 0.1.3 uses the old trace variable command and Tcl 9 documents trace add variable. "
        "The program starts it in two interpreters on its own display. The Python 3.14.6 process ended with the error and had no window; the Python 3.12.3 process with Tk 8.6.14 kept running and had a window, and the picture is that window. "
        "The caret that blinks in a field would make the picture differ from run to run, so the program moves the focus to a button before it crops the window. "
        "The delay card is the research's reading of the F6 key: the key logs the position at the end of the delay, not where the pointer was when it was pressed.",
        "mouseInfo() needs Tk 8.6; under Tk 9 it ends in an error.", recorded=True)

# ---- 14 screenshots and pixel colors ------------------------------------------------------------------------------------------------------------
pn = "shotCut_v1_0_0.py"
p14, bot14, a14, b14, x14, w14 = pfit(pn, 0.5, 1.55, 6.0, 2.95)
xr = round(x14 + w14 + 0.2, 2)
im14, ib14, _ = img("screen.png", xr, 1.5, round(9.5 - xr, 2), 1.3)
content("Screenshots and pixel colors", "screenshot() returns an image of the whole screen; pixel() reads one point of it",
        [p14, im14, imgcap(["screen.png"], xr, round(ib14 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_VD,
                 rec("a display of depth 16 returned (172, 174, 172) for a background of (176, 176, 175) and failed the match."),
                 ne("HiDPI scaling and real or multiple monitors.")],
                xr, round(ib14 + 0.3, 2), round(9.5 - xr, 2), fs=8, gap=0.04),
         factrow("Captcha2003", y=4.58)],
        story_notes("Captcha2003") + " The program draws a window with one gray button on a display of depth 24 and takes the screenshot: the image has the size of the screen, 1920 by 1080, and the pixel inside the window is (176, 176, 175) while the pixel outside it is black. "
        "pixelMatchesColor() is True for the exact color, False when one channel is off, and True again with tolerance=1. The call pixel(210, 160) returns RGB(red=176, green=176, blue=175), a named tuple, and the second form the chapter prints, pixel((50, 200)) with a tuple, raises TypeError: pixel() missing 1 required positional argument: 'y'. "
        "A display of depth 16 stores fewer bits for each color, so the same gray comes back a little different and an exact match fails; the research saw that on its own, and this deck does not run it. "
        "The picture is the screenshot reduced to 480 by 270 pixels. A real screen with scaling, and several monitors, change the size and the coordinates, and neither was available.",
        "Compare colors with a tolerance, and read a pixel with two numbers.", notexec=True, recorded=True)

# ---- 15 finding a button on the screen --------------------------------------------------------------------------------------------------------------
pn = "locateCut_v1_0_0.py"
dg, dcap = diagram("FindingAndClickingAButton", "activity", (0.5, 1.4, 3.1, 2.4),
                   grid={"shot": (0, 0), "loc": (0, 1), "found": (0, 2), "click": (0, 3), "exc": (1, 2)},
                   cols=[(0.05, 1.45), (1.8, 1.3)], rows_n=4, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 3},
                   routes={("start", "shot"): "h", ("found", "exc"): "h", ("click", "end"): "h", ("exc", "end"): "v"}, fs=8, nh=0.5, dh=0.42)
p15, bot15, a15, b15, x15, w15 = pfit(pn, 3.6, 1.55, 5.9, 3.0, right=True)
im15, ib15, _ = img("located.png", 0.5, 3.88, 1.7, 0.95)
content("Finding a button on the screen", "locateOnScreen() returns the box where the picture is; click() takes a box",
        [dg, im15, imgcap(["located.png"], round(0.5 + im15["w"] + 0.1, 2), im15["y"], round(x15 - 0.2 - 0.5 - im15["w"] - 0.1, 2), fs=8), p15,
         capfoot(dcap, SAY_VD + " " + hid(pn, a15, b15, "imports, the private display and the window with two buttons"), x15, round(bot15 + 0.05, 2), w15)],
        "The flow chart is the pattern of every script that clicks a button it can see: take a screenshot, call locateOnScreen() with the image of the button, and, if it is found, click the center of the box; if it is not, the call raises ImageNotFoundException. "
        "The program draws a window with two identical buttons, cuts one button out of the screenshot and saves it as submit.png, and asks for it on the screen. locateOnScreen() returns the first box, locateAllOnScreen() both, and click() accepts the file name or a box and presses the button it finds. "
        "A Box holds the numbers as np.int64 when OpenCV is installed and as int without it, which the research saw, so the program converts them with int() before it prints them. The picture shows the screenshot with the found box in red. "
        "The research found its button at (400, 300, 84, 35), and saw locateOnScreen() raise at once when the button was not there and, with minSearchTime=5, keep looking and find a button that appeared 1.2 seconds later; in this deck's run the window is placed differently and the box is the one the transcript prints.",
        "Cut the button out of a screenshot, then look for it.")

# ---- 16 exact matches, OpenCV and missing images ----------------------------------------------------------------------------------------------------------
pn = "matchCut_v1_0_0.py"
tbr = EX["_tables"]["releases"]["rows"]
tbl16 = {"t": "table", "x": 0.5, "y": 1.7, "w": 3.5, "colW": [0.62, 0.62, 0.4, 1.86], "fs": 7, "rowH": 0.19, "cellMargin": [0.01, 0.04, 0.01, 0.04], "rows": tbr}
p16, bot16, a16, b16, x16, w16 = pfit(pn, 4.1, 1.55, 5.4, 3.4, right=True)
content("Exact matches, OpenCV and missing images", "One pixel off is no match; confidence needs OpenCV; a missing image changed at 0.1.30",
        [foot(rec("the release matrix; 4 of its 14 combinations do not import."), 0.5, 1.42, 3.5, fs=8), tbl16, p16,
         foot(SAY_VD, 0.5, 4.64, 3.5, fs=8)],
        "The chapter says that a match must be exact, and the program shows it. A button cut from the screen is found; the same image with one pixel changed to black raises ImageNotFoundException with OpenCV and without; grayscale=True does not help; and confidence=0.9 finds the damaged image only when OpenCV is installed, "
        "and raises NotImplementedError otherwise. With PyScreeze 0.1.28 the missing image does not raise at all, the call returns None, so click('submit.png') raises a confusing TypeError further on. "
        "The table is the research's record of the release matrix, 14 combinations of PyAutoGUI and PyScreeze on Python 3.12 and 3.14.6, of which 4 do not import, and the deck check computes every cell again from the record. "
        "The program prints, for the exact image, the image with one pixel off, the same with confidence=0.9 and with grayscale=True, what each call returned in three environments; the slide leaves out the imports, the private display and the window with a button. The result is the advice to pin the two packages together, and to check for None or for the exception on the version in use. The release dates of PyScreeze 1.0.0 and 1.0.1 are the same day, 20 August 2024. The research also saw that the same button at a larger font, 109 by 45 pixels instead of 84 by 35, was not found, so a picture must come from the same screen settings as the screen it is searched in.",
        "Pin PyAutoGUI and PyScreeze together; a missing image acts differently.", recorded=True)

# ---- 17 window objects: Windows only -------------------------------------------------------------------------------------------------------------------------
pn = "windowCut_v1_0_0.py"
p17, bot17, a17, b17, x17, w17 = pfit(pn, 0.5, 1.55, 6.1, 3.4)
xr = round(x17 + w17 + 0.2, 2)
im17, ib17, _ = img("frame.png", xr, 1.5, round(9.5 - xr, 2), 1.5)
content("Window objects: Windows only", "On Linux none of the six window functions exists and pygetwindow does not import",
        [p17, im17, imgcap(["frame.png"], xr, round(ib17 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_VD,
                 rec("pygetwindow 0.0.9 raises NotImplementedError: PyGetWindow currently does not support Linux; PyAutoGUI 0.9.40 does not import at all, and the chapter's listings 17, 18 and 19 raise at their first getActiveWindow call."),
                 ne("Windows and macOS: getActiveWindow(), the Window objects and their move, resize and activate calls were never run.")],
                xr, round(ib17 + 0.3, 2), round(9.5 - xr, 2), fs=8, gap=0.04)],
        "The chapter teaches six window functions, getActiveWindow, getAllWindows, getWindowsAt, getWindowsWithTitle, getAllTitles and getActiveWindowTitle, and says they work on Windows only as of PyAutoGUI 1.0.0. "
        "On Linux the program finds none of them in pyautogui and importing pygetwindow raises NotImplementedError, so the chapter's three listings on window objects raise at the first call. "
        "What the program can show about windows on Linux is what the window manager and xdotool do: a Tk window placed at x 120 and y 80 has its client area at (121, 100), inside the frame that the openbox window manager adds, and after xdotool moves it to (300, 200) and resizes it to 640 by 360 the client area is at (301, 220), below the title bar. "
        "The picture is the window with that frame. The Windows window objects, with their left, top, width and height and their activate() and move calls, were not run.",
        "Window objects are for Windows; on Linux ask the window manager.", notexec=True, recorded=True)

# ---- 18 typing into the right window ---------------------------------------------------------------------------------------------------------------------------
pn = "typeCut_v1_0_0.py"
dg, dcap = diagram("TypingIntoTheRightWindow", "activity", (0.5, 1.4, 2.9, 1.9),
                   grid={"wait": (0, 0), "click": (0, 1), "write": (0, 2), "hot": (0, 3), "recv": (0, 4)},
                   cols=[(0.05, 2.35), (2.5, 0.35)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "wait"): "h", ("recv", "end"): "h"}, fs=8, nh=0.28, dh=0.4)
p18, bot18, a18, b18, x18, w18 = pfit(pn, 3.7, 1.55, 5.8, 3.42, right=True)
im18, ib18, _ = img("typed.png", 0.5, round(dcap["y"] + dcap["h"] + 0.06, 2), 2.9, 0.9)
content("Typing into the right window", "Click the window first; write() types each character, hotkey() presses a shortcut",
        [dg, dcap, im18, imgcap(["typed.png"], 0.5, round(ib18 + 0.02, 2), 2.9, fs=8), p18,
         foot(SAY_VD + " " + hid(pn, a18, b18, "imports, the private display and the window with a text field"), x18, round(bot18 + 0.05, 2), w18, fs=8)],
        "The flow chart is the order that makes typing reliable: wait a few seconds with sleep(), click the window to make it active, call write() to type the string, call hotkey() to press the shortcut, and the focused window receives the typing. "
        "The program clicks the text field first and then types: write('Hello, world!') arrives as the same string, with the Shift key pressed for the capital H and the exclamation mark, and a list of key names, with left arrows in it, edits the text in place. "
        "keyDown('shift'), press('4') and keyUp('shift') type a dollar sign, and hotkey('ctrl', 'a') followed by delete empties the field. The picture is the field after the program typed the sentence again. "
        "Without the click the keys go to whichever window has the focus, and that is the mistake the chapter warns about. Appendix B has typing mistakes of its own, which the research found: the answer to question 6 types Hello world! without the comma of the question, and the answer to question 13 misspells pyautogui as pyatuogui, a NameError.",
        "Click first so the keys go where you mean.")

# ---- 19 key names ---------------------------------------------------------------------------------------------------------------------------------------------------
pn = "keysCut_v1_0_0.py"
p19, bot19, a19, b19, x19, w19 = pfit(pn, 0.5, 1.55, 5.6, 2.95)
xr = round(x19 + w19 + 0.2, 2)
content("Key names: mistakes are silent", "A wrong key name raises nothing and types nothing; a character off the list vanishes",
        [p19,
         *stack([SAY_VD, hid(pn, a19, b19, "imports, the private display and the window with a text field"),
                 rec("hotkey('ctrl', 'nokey') raised nothing; an emoji vanished and write(12) raised TypeError; KEYBOARD_KEYS holds 194 names, every one of the 41 names of Table 23-1 and its text is in it, f13 and f24 exist, and the roadmap lists a strict mode as a plan.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.05),
         factrow("Qwerty1874", y=4.58)],
        story_notes("Qwerty1874") + " The program types into a text field and prints what arrived. press('nokey'), press('SHIFT') and keyDown('nokey') raise nothing and type nothing, because the key names are lower case and an unknown name is ignored; "
        "write(['a', 'nokey', 'b']) typed ab and write('café') typed caf, because the letter with the accent is not on the list, and the capital A is not in the list either, since a capital is typed with the Shift key. "
        "The consequence is that a script cannot tell a typo from a success, and the habit is to print the text that arrived, as the program does. The table of the chapter, Table 23-1, lists the key names, and every one of its 41 names is in KEYBOARD_KEYS.",
        "A wrong key name fails silently; print what arrived.", recorded=True)

# ---- 20 hotkeys and the clipboard ------------------------------------------------------------------------------------------------------------------------------------
pn = "clipCut_v1_0_0.py"
dg, dcap = diagram("CopyingTextWithTheClipboard", "sequence", (0.5, 1.4, 4.2, 2.5), fs=8, head_w=0.95, gap0=0.1)
p20, bot20, a20, b20, x20, w20 = pfit(pn, 4.9, 1.55, 4.6, 2.95, right=True)
content("Hotkeys and the clipboard", "hotkey() presses keys in order and releases them in reverse; pyperclip reads the copy",
        [dg, p20,
         capfoot(dcap, SAY_VD, 0.5, dcap["y"], 4.2),
         factrow("CutCopyPaste1974", y=4.58)],
        story_notes("CutCopyPaste1974") + " The sequence diagram is the round trip of the chapter: the script presses ctrl and a to select the text, ctrl and c to copy it, the window stores the text on the clipboard, the script calls pyperclip.paste(), and the clipboard returns the text of the window. "
        "The program shows two things. The keys of hotkey('ctrl', 'alt', 'shift', 's') went down in the order given and came up in the reverse order, which the window recorded as events. And the text of the field, selected and copied with the two shortcuts, came back from pyperclip.paste() and pasted again with ctrl and v. "
        "The program waits a second between the copy and the paste, because the copy is made by another process and the clipboard is not filled at once; the corpus programs that read the clipboard right away sometimes got an empty string, so their values are not quoted. "
        "The five files of the online materials that import pyperclip are alternatingText.py, ccwd.py, cliprec.py, phoneAndEmail.py and showmap.py.",
        "hotkey() is a chord; the clipboard is another process.")

# ---- 21 message boxes ------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "boxCut_v1_0_0.py"
p21, bot21, a21, b21, x21, w21 = pfit(pn, 0.5, 1.55, 6.1, 3.2)
xr = round(x21 + w21 + 0.2, 2)
content("Message boxes", "A box returns a button's text, '' or None; an unanswered box returns 'Timeout'",
        [p21,
         *stack([SAY_VD, hid(pn, a21, b21, "imports, the private display and the helper that starts a box and answers it with the keyboard"),
                 rec("the installed PyMsgBox 2.0.1 says __version__ 1.0.9, and its signatures carry type hints that 1.0.9 lacks.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.05)],
        "The message boxes of PyAutoGUI come from PyMsgBox: alert(), confirm(), prompt() and password(). The program starts each box in a child process on its own display, answers it with xdotool keys and prints what the call returned. "
        "Return on confirm returns 'OK' and Escape returns 'Cancel'; prompt returns an empty string for Return alone and None for Escape; password returns what was typed; and confirm with timeout=1500 returned 'Timeout' after about one and a half seconds, which the program prints as a boolean. "
        "A script that needs an answer must handle both the empty string and None. The installed PyMsgBox reports a version older than its release, which the research saw and which is only a label.",
        "Check for '' and None; a timeout is a string.", recorded=True)

# ---- 22 looking busy ----------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "busyCut_v1_0_0.py"
p22, bot22, a22, b22, x22, w22 = pfit(pn, 0.5, 1.55, 5.5, 3.3)
xr = round(x22 + w22 + 0.2, 2)
content("Looking busy and the idle clock", "Moving the pointer one pixel resets the idle time; reading the position does not",
        [p22,
         *stack([SAY_VD, hid(pn, a22, b22, "imports and the private display"),
                 rec("the sushigoroundbot repository answered 403 through the proxy of the study, and sumopaint.com was unreachable with an SSLError."),
                 ne("the Sushi Go Round game (no Flash player is installed here), a captcha and a real instant messenger.")],
                xr, 1.5, round(9.5 - xr, 2), fs=8, gap=0.05)],
        "A script that moves the pointer one pixel left and right keeps a screen from going idle, and the program shows the mechanism with the idle clock of the X server: the x positions are 799, 800, 799, 800, 799 and 800, and the script ends where it began. "
        "The idle time is reset by move(1, 0) and by press('shift') and not by position() or size(), so a script that only reads the screen does not look busy. The numbers are printed as booleans, because the idle time itself changes from run to run. "
        "The chapter's examples that use these ideas, a bot for a game, an instant messenger and a captcha, need a real screen and a real service and were not run; the repository of the game bot could not be fetched from the proxy of the study.",
        "Moving the pointer resets the idle clock; reading it does not.", notexec=True, recorded=True)

# ---- 23 the chapter replayed ---------------------------------------------------------------------------------------------------------------------------------------------
tbl23 = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [1.9, 0.9, 1.15, 1.15, 0.9, 1.7, 1.3], "fs": 8, "rowH": 0.26, "rows": EX["_tables"]["configurations"]["rows"]}
content("The chapter replayed in five environments", "Recorded: how many of the 80 printed statements match the book, by environment",
        [tbl23,
         card("Recorded 13 Oct 2026", "One program of 27 items ran under 12 interpreter rows: 3.12.3, 3.13.14, 3.14.2 to 3.14.6, 3.15.0b4 and 3.14.6 with OpenCV ran every item; 3.14.0 and 3.14.1 raised TclError: Can't find a usable init.tcl, and 3.11.17 had no tkinter. 14 of the 27 items differed between some pair of rows.",
              0.5, 3.4, 4.4, 1.5, fs=8.5, accent="slate"),
         card("NOT EXECUTED here", "Windows, macOS, the accessibility permission, a real Wayland compositor, real or multiple monitors, HiDPI scaling, a real screen, the Sushi Go Round bot, a captcha, a real instant messenger and Python 3.15 final, which was only the beta 3.15.0b4.",
              5.1, 3.4, 4.4, 1.5, fs=8.5, accent="orange")],
        "The table is the research's record of the chapter's 80 statements replayed as printed, and the deck check computes every cell again from the record. With Python 3.14.6 and the newest packages 40 matched the book and 52 ran without an exception; without OpenCV the numbers were the same; "
        "with PyScreeze 0.1.28 41 matched; under Python 3.12.3 with Tk 8.6.14 40 matched and 53 ran; and in an empty environment 1 matched and 1 ran. The statements that differ are the pointer positions, the pixel((50, 200)) call, the Box values, the window objects, mouseInfo() and the listing of spiralDraw.py. "
        "Across the 14 combinations of PyAutoGUI and PyScreeze, 7 of the 27 items differed, across 7 releases of Pillow, 9.5.0 to 12.3.0, 3 items differed only by a DeprecationWarning in 12.3.0, and across 3 releases of PyMsgBox the signatures differed. "
        "The photograph of the stories was not fetched, because the single request to Wikimedia Commons answered 429.",
        "The same book gives 1 to 41 matching statements, by environment.", notexec=True, recorded=True)

# ---- 24 summary: the mind map ----------------------------------------------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("ControllingTheKeyboardAndMouseAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. Installing and sending input: PyAutoGUI sends events through XTEST on Linux, a Wayland session does not accept them, and the window functions exist only on Windows; on slide 5 the session variable alone made the screenshot fail while the move still worked through X. "
        "Staying on track: the pause after each call is 0.1 seconds, a corner of the screen raises the fail-safe, and the exception stops the program. Mouse control: the origin (0, 0) is the top left corner, click() presses and releases the button, and drag() holds the button down. "
        "Screen and images: screenshot() returns an image, locateOnScreen() returns a box, and a missing image raises ImageNotFoundException with a recent PyScreeze. Windows and keyboard: write() types a string, an unknown key name is ignored and the focused window receives the typing. "
        "Scripts and practice: confirm() returns the button clicked, Looking Busy moves the cursor by one pixel, and Tk 9 breaks MouseInfo. "
        "Together they answer the first question of the chapter, what can be shown to work on a machine with no real screen and what can only be shown to fail, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ------------------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 23 - free online", PUB["P01"][2]],
         ["Appendix A: installing third-party modules", PUB["P05"][2]],
         ["Online materials of the 3rd edition (zip)", PUB["P02"][2]]]
_ref = [["PyAutoGUI documentation", PUB["P07"][2]],
        ["PyAutoGUI: mouse control functions", PUB["P09"][2]],
        ["PyAutoGUI: keyboard control functions", PUB["P10"][2]],
        ["MouseInfo documentation", PUB["P24"][2]]]
_hist = [["Computer mouse (Wikipedia)", STORY["Mouse1968"]["link"]],
         ["X Window System (Wikipedia)", STORY["XWindow1984"]["link"]],
         ["QWERTY (Wikipedia)", STORY["Qwerty1874"]["link"]],
         ["CAPTCHA (Wikipedia)", STORY["Captcha2003"]["link"]],
         ["Dead man's switch (Wikipedia)", STORY["DeadMan1918"]["link"]],
         ["Cut, copy, and paste (Wikipedia)", STORY["CutCopyPaste1974"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9, "groups": [
            {"head": "Stories", "rows": _hist}, {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the chapter; the online materials are the zip of 91 files, and Appendix A is where the book installs third-party packages. "
        "The reference links are the PyAutoGUI documentation and its pages on the mouse and keyboard functions, and the MouseInfo documentation. "
        "The six stories of the chapter are on slides with their own link, and their pages are the last group. "
        "The research package holds %d sources in all, among them the X.Org protocol documents, the manual page of xterm, the Microsoft documentation of SendInput, the PyPI metadata of the packages and the Tcl 9.0 manual. "
        "The research opened the chapter's own 13 external links too: 7 answered 200, 3 answered 302, youtu.be answered 303 and then 429, the game bot's repository answered 403 through the proxy of the study, and sumopaint.com was unreachable. No photograph of a person is used in the deck." % len(RD.PUBS),
        "Textbook, documentation, and history, all opened today.")

# ---- 26 closing ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "PyAutoGUI sends real input through the X server, and the window cannot tell it from a mouse.",
            "Leave the fail-safe on; a wrong key name or a missing image fails quietly.",
            "Pin PyAutoGUI and PyScreeze together, and test scroll units and Tk where you run.",
            "MouseInfo needs Tk 8.6, window objects are for Windows, and nothing ran on a real screen."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 10, "big": False,
          "items": ["%d console rows" % ROWS_SHOWN, "%d programs run" % len(PROGS), "%d diagrams" % len(DIAG), "%d pictures" % len(EX["_images"])]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The programs need PyAutoGUI, PyScreeze, Pillow, PyMsgBox, pyperclip, python3-xlib and a Tk, and the deck's own programs run on a virtual X display with Xvfb, openbox, xdotool, xclip, xterm and scrot. "
        "The rows were run again under Python 3.14.6 each time the deck was built, and the programs, and with them the pictures, were run again by the check that compares the slides with the recording. "
        "What was not run is marked on its slide: Windows and macOS, a real Wayland compositor, real or multiple monitors, HiDPI scaling, a real screen, the Sushi Go Round game, a captcha, a real instant messenger and Python 3.15 final. "
        "Nothing was ever shown to a person on a screen. Every count in this deck from a single run is a single run, and not a benchmark. The next chapter of the book moves on, and what this chapter taught about checking what a program receives carries over.",
        "Questions are welcome; bring a script to try.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("What a script can do", "What a script can do with PyAutoGUI", "How a click reaches a window"),
          ("Pauses and fail-safes", "Pauses and fail-safes", "Corners and the fail-safe points"),
          ("The mouse", "Moving the mouse and where it is", "MouseInfo breaks under Tk 9"),
          ("The screen and images", "Screenshots and pixel colors", "Window objects: Windows only"),
          ("The keyboard and message boxes", "Typing into the right window", "The chapter replayed in five environments"),
          ("Summary and resources", "The chapter in one map", "Where to go from here")]
_rows = ["%s (slides %d-%d)" % (name, _t[a], _t[b]) for name, a, b in _parts]
_ends = [_t[b] for _, _, b in _parts]
_starts = [_t[a] for _, a, _ in _parts]
if _starts[0] != 4 or any(_starts[i + 1] != _ends[i] + 1 for i in range(len(_parts) - 1)) or _ends[-1] != len(S) - 1:
    raise SystemExit("REFUSED: agenda ranges are not contiguous: %r %r (len S=%d)" % (_starts, _ends, len(S)))
_nstory = sum(1 for s in S for i in s["items"] if i.get("t") == "factrow")
_npic = sum(1 for s in S for i in s["items"] if i.get("t") == "img")
S[1]["items"] = [
    {"t": "numlist", "x": 0.5, "y": 1.4, "w": 6.3, "h": 3.55, "fs": 11.5, "items": _rows},
    {"t": "stat", "x": 7.05, "y": 1.5, "w": 2.45, "h": 3.4, "vert": True, "items": [
        {"n": str(len(S)), "label": "slides, numbered bottom-right"},
        {"n": "%d + %d" % (_nstory, len(ST.STORIES) - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, len(ST.STORIES) - _nstory)},
        {"n": str(_npic), "label": "pictures, each saved by a program that is run again"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from what a script can do to a map."
S[1]["notes"] = ("The route has six parts. It starts with what a script can do: the eight uses of PyAutoGUI, the packages and the display they need, and how a click reaches a window through the X server. "
                 "Then the pauses and fail-safes: the pause after each call and the four corners. The third part is the mouse: moving it, clicking, dragging in a spiral, scrolling, and the MouseInfo application, which breaks under Tk 9. "
                 "The fourth is the screen and images: screenshots and pixel colors, finding a button, exact matches and the releases that changed them, and the window objects that exist for Windows only. "
                 "The fifth is the keyboard and the message boxes: typing into the right window, key names, hotkeys and the clipboard, message boxes, looking busy, and the chapter replayed in five environments. "
                 "The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. All six stories are on slides, each with a link; the eight narrative diagrams of the chapter are drawn from the same specifications as the interactive page. "
                 "Every output was printed by Python %s with PyAutoGUI 0.9.54 and PyScreeze 1.0.1, the programs ran on a virtual display, and what could not be run is marked on its slide." % PYV)

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
plan = {"meta": {"title": "Ch. 23: Keyboard and Mouse", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "recorded": RECORDED,
                 "standin": {str(k): v for k, v in STANDIN.items()}}, "slides": S}
if LATE:
    raise SystemExit("REFUSED:\n" + "\n".join(LATE))
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; Recorded on slides", RECORDED)
