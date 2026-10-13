#!/usr/bin/env python3
"""Builds deck_plan_v1_0_0.json - SEN0414 chapter 22 (Recognizing Text in Images) on the CME classroom standard.

Same regime as chapters 10 to 21: numbered warm-ivory slides, an agenda with exact slide ranges, a summary before the resources, full-sentence takeaway
strips, stories with fact rows, consoles and programs (whole or honest excerpts, labelled with their line numbers) with their results as Python printed
them. Every console result and program transcript comes from examples_out_v1_0_0.json (made by examples_run_v1_0_0.py under Python 3.14.6 with pytesseract
0.3.13, Pillow 12.3.0, NumPy 2.5.4, OpenCV 5.0.0.93 and PyAutoGUI 0.9.54, and the Tesseract 5.3.4 of Ubuntu 24.04); the speaker notes are prose for the reader
and carry only what the chapter's RDODI research package (03-materials/ch22/rdodi, sen0414_ch22_rdodi_data_v1_0_2.py, findings F1 to F19), its records
(08-tooling/ch22-page/*.json) or a program of this deck established.

What this chapter adds against chapter 21: THE OUTPUT IS TEXT FROM A PICTURE, so the deck shows the picture beside the text Tesseract returned. Fourteen
pictures that programs saved (the book's scans cropped, a page with the words boxed, drawn test pages, a page cleaned, two columns, a screen) are placed on
the slides as images; each caption names the program ('image <file> made by <program>') and program_check_v1_0_0.py runs that program again and requires the
slide to carry a picture byte-identical (or pixel-identical) to what the program saves now. Twelve corpus programs and sixteen programs written for the deck
(the Cuts) were run for real; the corpus programs are named in the notes (their lines are wider than a slide), the Cuts are on the slides. One program, the
screen scraper, runs on a virtual X display (Xvfb) with the real ImageMagick display and the real PyAutoGUI, a local stand-in for a screen where nobody sees the
picture; its slide says so with the words honesty_check_v1_0_0.py requires ('Virtual display', 'local stand-in'). What the research recorded on 13 October 2026
and the deck does not run again is on a slide as 'Recorded'. What could not be run is marked NOT EXECUTED on its slide (meta.notExecuted). The eight narrative
diagrams of the chapter (sen0414_ch22_diagrams_v1_0_0.py, grounding 0.84 or more) are drawn as native shapes (diagram_shapes_v1_0_0.py) and checked by
diagram_check_v1_0_0.py; three tables (the same probe in four interpreters at check time, three Tesseract engines on three kinds of data, and the nine
configurations of the research) and two charts are native PowerPoint objects whose data the deck check computes again. Accuracy numbers are MEASURED single
runs with the Tesseract version named. No photograph of a person is used: the study's stories carry none (the single request to Wikimedia Commons answered
429); four of the six stories are on slides and two are told in the notes.

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


ST = load("stories22", os.path.join(HERE, "..", "sen0414_ch22_stories_v1_0_0.py"))
if ST.run_checks():
    raise SystemExit("REFUSED: the story companion fails its own checks")
STORY = {x["id"]: x for x in ST.STORIES}
DG = load("diagrams22", os.path.join(HERE, "..", "sen0414_ch22_diagrams_v1_0_0.py"))
NODES = DG.nodes_from_ttl(os.path.join(HERE, "..", ".."))
_bad = DG.run_checks(NODES)
if _bad:
    raise SystemExit("REFUSED: the diagrams fail their own checks: %r" % _bad[:3])
DIAG = {d["id"]: d for d in DG.DIAGRAMS}
RD = load("rdodi22", os.path.join(HERE, "..", "sen0414_ch22_rdodi_data_v1_0_2.py"))
EX = json.load(open(os.path.join(HERE, "examples_out_v1_0_0.json")))
PYV = EX["_python"]
TESS = EX["_tesseract"]
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
    """the first line of a Cut that is shown: the one after 'd = wd()'"""
    return span(pname, "d = wd()")[0] + 1


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
    fn = {"activity": DS.activity, "sequence": DS.sequence, "lifecycle_side": DS.lifecycle_side, "usecases": DS.usecases, "mindmap": DS.mindmap}[kind]
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


SAY_VD = "Virtual display: Xvfb with the real ImageMagick display and PyAutoGUI, a local stand-in for a screen; nobody sees the picture."
CORPUS = ("The corpus program %s ran too and is not shown, because its lines are wider than a slide; ")

# ---- 1 title ---------------------------------------------------------------------------------------------------
c1, _ = con("title", 5.0, 0.25, 4.5, fs=8, cap=False)
S.append({"kind": "title", "title": "Ch. 22: Recognizing Text",
          "sub": "Text in images: OCR with Tesseract and pytesseract, searchable PDFs and the screen",
          "items": [c1, foot("Every output on these slides was printed by the Python above when the deck was made, and every picture was saved by a program that is run again to check it. "
                             "Windows, macOS, a scanner and a real screen were never used: the screen program ran on a virtual display, and what could not be run is marked on its slide.",
                             0.6, 3.85, 8.8, fs=11)],
          "notes": "Chapter 21 taught a program to make pictures. Chapter 22 teaches a program to read them: Tesseract, an open-source engine that turns the letters of an image into text, and pytesseract, the Python wrapper that calls it. "
                   "The chapter has 8 listings and 2 figures, and ends with 7 practice questions and 1 practice program, the Browser Text Scraper. "
                   "This deck follows the chapter in its own order: reading an image in four lines, the mistakes in the result, preparing an image before it is read, other languages, a searchable PDF made with the NAPS2 application run from Python, and reading the screen. "
                   "It adds what the research found when every printed output was run again: Appendix A pins pytesseract 0.3.10, which cannot even be imported on Python 3.14; the first word of the book's Figure 22-1 is Iv in the book and In with the Tesseract of Ubuntu, because the engine, its data and its version all change the answer; "
                   "the chapter's advice on small, tilted and noisy pages is true, and the deck puts numbers on it; the language codes are not all what the chapter calls them; NAPS2 refuses to overwrite a file and still returns 0; "
                   "and the shipped preprocessing script calls names it never defines. "
                   "The output of this chapter is text from a picture, so the deck shows the picture next to the text: fourteen pictures that programs saved are on the slides as images, and each caption names the program that made the picture. "
                   "The build runs every such program again and refuses the deck unless the slide holds a picture that is byte for byte, or pixel for pixel, what the program saves now. "
                   "Every output on the slides was printed by Python 3.14.6, installed with uv, with pytesseract 0.3.13, Pillow 12.3.0, NumPy 2.5.4, OpenCV 5.0.0.93, PyAutoGUI 0.9.54 and the Tesseract 5.3.4 of Ubuntu 24.04. "
                   "Windows and macOS were never used, no scanner was attached, and nobody looked at a real screen: the screen program ran on a virtual display, which the slide says. "
                   "What could not be run is marked on its slide.",
          "bg": "light"})

# ---- 2 agenda (filled in at the end) -------------------------------------------------------------------------------
S.append({"kind": "content", "title": "Today's route", "sub": "", "items": [], "notes": "", "take": "", "bg": "light"})

# ---- 3 questions ------------------------------------------------------------------------------------------------
content("The questions this chapter answers", "The chapter's own competency questions; the summary comes back to each",
        [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 2.2, "fs": 13, "items": [CQ1, CQ2]},
         {"t": "chips", "x": 0.5, "y": 3.8, "w": 9.0, "h": 0.5, "fs": 10,
          "items": ["6 branches", "%d topics" % len(NODES), "%d console rows" % ROWS_SHOWN,
                    "%d programs run" % len(PROGS), "8 diagrams", "14 pictures", "Python %s" % PYV]}],
        "The first question is the spine of the chapter, and the deck answers it slide by slide. On a machine with no scanner and no screen, a program can read a picture, give back the words, their boxes and a confidence for each, and make a searchable PDF, and the result can be compared with the text that was printed on the page; "
        "that is what can be shown to work. What can only be shown to fail is the part that needs a person's machine: the Windows and macOS installers, the Flatpak of NAPS2, a scanner, a large language model and a real screen. "
        "The research used a virtual X display, Xvfb, with the real ImageMagick display and PyAutoGUI, and took a screenshot of that screen; nobody looked at a real monitor, and the deck says so where it comes up. "
        "The second question is the watch-out. The chapter's 22 statements that can be replayed were run as printed in nine configurations: with the Tesseract 5.3.4 of Ubuntu and its fast English data 18 of 22 matched the book; "
        "with 5.5.3 and the fast data 20, with 5.5.3 and the best data 18, with 4.1.1 and the fast data 20, with all the apt languages 19 and with all languages under 5.5.3 21; with the book's pins, 18 on Python 3.13.14, 8 on Python 3.14.6, and 0 in an empty Python. "
        "The statements that still differ are get_languages(), the first word Iv of Figure 22-1, the Japanese heading and the English gibberish read from the Japanese page. "
        "The online materials of the book, 91 files, hold the four files of this chapter and not the others the chapter creates or assumes. Each slide says where a printed line differs and on what evidence.",
        "Know what can be shown to work and what can only be shown to fail.")

# ---- 4 what pytesseract returns ---------------------------------------------------------------------------------------
dg, dcap = diagram("WhatPytesseractCanReturn", "usecases", (0.5, 1.4, 4.7, 2.75), fs=8)
x4 = 5.4
content("What a program can ask Tesseract for", "One wrapper, six calls; the chapter teaches the first and adds PDFs and the screen",
        [dg, dcap,
         card("Two programs and a wrapper", "Tesseract is the engine, a program of its own. pytesseract starts it and gives its answer back to Python. The chapter ends with 7 practice questions and 1 practice program, the Browser Text Scraper.",
              x4, 1.45, round(9.5 - x4, 2), 1.4, fs=9.5, accent="slate"),
         card("Recorded 13 Oct 2026", "The online materials hold 91 files, four of them for this chapter: ocr-example.png, frankenstein.png, frankenstein_jpn.png and preprocess_ocr.py. There is no ocrscreen.py, output.pdf, cat.png or spam.pdf.",
              x4, 2.95, round(9.5 - x4, 2), 1.45, fs=9.5, accent="orange"),
         factrow("Goldberg1915", y=4.5)],
        story_notes("Goldberg1915") + " The use-case diagram lists what the wrapper can return: the text with image_to_string(), the words with their boxes and confidence with image_to_data(), a searchable PDF with image_to_pdf_or_hocr(), "
        "the orientation of a page with image_to_osd(), the installed languages with get_languages(), and the engine version with get_tesseract_version(). They are independent calls to one program, which is why the picture is a set of uses and not a sequence. "
        "The chapter's page was read on 13 October 2026; it returned 200 with 40,521 bytes and holds 8 listings and 2 figures, and its SHA-256 equals the digest that the book's own chapter ontology records. "
        "The card records what the research found on that day and this deck does not run again: the online materials of the third edition, a zip of 91 files, hold ocr-example.png of 939 by 1198 pixels in mode RGBA, frankenstein.png of 1130 by 672 pixels in mode P, frankenstein_jpn.png of 1211 by 606 pixels in mode RGB and preprocess_ocr.py of 190 lines; "
        "they hold none of ocrscreen.py, output.pdf, cat.png, dog.png, moose.png, spam.pdf, eggs.pdf or output.txt, which the chapter creates or assumes, and the publisher's book page has one occurrence of Recognizing Text and none of Tesseract, OCR or NAPS2. "
        "The deck downloads the zip while it runs and checks the SHA-256 of each file it uses; the book's scans are the book's own examples, and the study did not check their licence, so they are used here for teaching only. "
        "Two more stories of the study, Emanuel Goldberg and his Statistical Machine of 1931 and Ray Kurzweil's reading machine of 1976, are told in the notes of the slides on PDFs and on the sizes of letters: " + STORY["Goldberg1931"]["story"] + " " + STORY["Kurzweil1976"]["story"],
        "One engine, six calls; the book's files are the starting point.", recorded=True)

# ---- 5 reading an image in four lines --------------------------------------------------------------------------------
pn = "fourLinesCut_v1_0_0.py"
dg, dcap = diagram("ReadingAnImageInFourLines", "activity", (0.5, 1.4, 3.05, 2.0),
                   grid={"imp": (0, 0), "open": (0, 1), "read": (0, 2), "str": (0, 3), "show": (0, 4)},
                   cols=[(0.05, 2.5), (2.65, 0.35)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "imp"): "h", ("show", "end"): "h"}, fs=8, nh=0.3, dh=0.4)
p5, bot5, a5, b5, x5, w5 = pfit(pn, 3.75, 1.55, 5.75, 2.9, a=body(pn), b=len(PROGS[pn]["code"].rstrip("\n").split("\n")) - 2)
im5, ib5, _ = img("ocrTop.png", 0.5, round(dcap["y"] + dcap["h"] + 0.04, 2), 3.05, 0.75)
content("Reading an image in four lines", "Import, open, image_to_string(), print; the result is one str that ends with a newline",
        [dg, dcap, p5, im5, imgcap(["ocrTop.png"], 0.5, round(ib5 + 0.02, 2), 3.05, fs=8),
         foot(hid(pn, a5, b5, "imports, helpers, the folder and the download check", "the saving of the picture")
              + " The page is ocr-example.png; the strip on the left is its top.", x5, round(bot5 + 0.05, 2), w5, fs=8.5)],
        "The four lines of the chapter are: import pytesseract and Pillow, open the file with Image.open(), pass the image to image_to_string(), and print the string. "
        "The program on the right is those lines run for real on ocr-example.png of the book's online materials, after the SHA-256 of the file was checked: the picture is 939 by 1198 pixels in mode RGBA, and Tesseract " + TESS.replace("tesseract ", "") + " (the Ubuntu 24.04 package, with the fast English data) returned a str of 2648 characters with 51 line breaks. "
        "The first four lines of the result are shown, and they follow the printed page including the hyphens that split dig-ital at the end of a line. The string ends with a newline, and ten of its lines are empty, the gaps between paragraphs. "
        "The strip under the flow chart is the top of the page that the program saved, so the picture and the text can be compared by eye, and the build runs the program again and compares the strip with the one on the slide. "
        "The corpus program ocrFundamentals_v1_0_0.py ran as well and is not shown, because its lines are wider than a slide: it checks the same file and also the types the other calls return. "
        "The chapter's own phrase, that Tesseract works best on clean scans of printed text, is the subject of the slides that follow.",
        "Four lines turn a picture into a string.")

# ---- 6 the same page, a different first word ---------------------------------------------------------------------------------
pn = "frankCut_v1_0_0.py"
a6 = body(pn)
b6 = span(pn, "print('the book prints")[0]
p6, bot6, a6, b6, x6, w6 = pfit(pn, 0.5, 1.55, 6.0, 2.55, a=a6, b=b6)
im6, ib6, _ = img("frankLine.png", 0.5, round(bot6 + 0.05, 2), w6, 0.3)
xr = round(0.5 + w6 + 0.2, 2)
content("The same page, a different first word", "The book prints Iv; this Tesseract returns In for the same picture",
        [p6, im6, imgcap(["frankLine.png"], xr, round(bot6 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         card("Iv, In, Ir or It", "With the fast data the first word is Iv under 4.1.1 and 5.5.3 and In under 5.3.4; with the best data it is Ir; with the legacy data It. The page shows an I and a small capital T.",
              xr, 1.5, round(9.5 - xr, 2), 2.0, fs=9.5, accent="orange"),
         foot(hid(pn, a6, b6, "imports, helpers, the folder and the download check", "the word comparison and the saving of the picture"), xr, 3.6, round(9.5 - xr, 2), fs=8.5),
         factrow("Frankenstein1831", y=4.58)],
        story_notes("Frankenstein1831") + " The page is Figure 22-1 of the book, frankenstein.png of the online materials, 1130 by 672 pixels in mode P. Tesseract 5.3.4 with the fast data returned 581 characters, and the book prints Iv as the first word of the sentence where this engine returns In; "
        "the picture shows the capital I followed by a small capital T, and the text of the page is IT was on a dreary night of November. Two words of the 106 differ from the printed page: IT came back as In, and motion as Motion, and the character error rate against the printed page is 0.0035 (a MEASURED single run with the Tesseract version named on the slide). "
        "The research ran the same page through the three engines the course built or installed and three kinds of English data (the next slides): the first word was Iv with 4.1.1 and with 5.5.3 and the fast data, In with the apt 5.3.4, Ir with the best data of all three, and It with the legacy data under 4.1.1 and 5.5.3. "
        "So the sentence the chapter prints, that the output looks like this, is true of one engine and one data set, and the exact text is a property of the version you installed. "
        "The corpus program frankensteinPage_v1_0_0.py ran too and is not shown, because its lines are wider than a slide; the program on the slide is cut from it.",
        "The exact text is a property of the engine and its data.")

# ---- 7 Appendix A pins on Python 3.14 -----------------------------------------------------------------------------------
tbe = EX["_tables"]["environments"]["rows"]
tbl7 = {"t": "table", "x": 0.5, "y": 1.45, "w": 5.2, "colW": [1.25, 0.75, 0.85, 0.95, 1.4], "fs": 7.5, "rowH": 0.3, "rows": tbe}
c7, bot7 = con("pins", 5.8, 1.45, 3.7, fs=8, cap=True)
content("Appendix A's pins, run on Python 3.14", "pytesseract 0.3.10 cannot be imported on Python 3.14; 0.3.13 can",
        [tbl7, c7,
         *stack(["Recorded 13 Oct 2026: PyPI lists 28 releases of pytesseract and none numbered 0.3.11 or 0.3.12; 0.3.10 imports pkgutil.find_loader, which Python 3.14 removed.",
                 "NOT EXECUTED here: the Windows and macOS installers of Tesseract, Homebrew, and pytesseract 0.3.4, 0.3.7 and 0.3.8, which install only from source."],
                5.8, round(bot7 + 0.04, 2), 3.7, fs=8, gap=0.06),
         foot("The table runs one probe in four interpreters while the deck is checked; the console is one session on the newest.", 0.5, 4.3, 5.1, fs=9)],
        "Appendix A of the book pins pytesseract==0.3.10 and Pillow==10.4.0. The table is the same probe run under four interpreters when the deck is built: Python 3.14.6 with the newest packages, Python 3.14.6 with the pins, Python 3.13.14 with the pins, and an empty Python 3.14.6. "
        "The probe imports pytesseract, reads a drawn line of text and counts the languages. With the pins on 3.14.6 the import raises ImportError, cannot import name 'find_loader' from 'pkgutil', because pytesseract 0.3.10 calls pkgutil.find_loader and Python 3.14 removed it; "
        "on 3.13.14 the same pins import and read, and the newest pytesseract, 0.3.13, no longer has find_loader, which the console shows by looking for the name in its source. The empty Python raises ModuleNotFoundError. "
        "Tesseract itself does not matter for the failure, because the exception is raised before any text is read. The console needs the packaging module for its last two rows, so it does not run in a Python in a browser unless packaging is installed. "
        "The research also recorded that PyPI has 28 releases of pytesseract, that none is numbered 0.3.11 or 0.3.12, and that three older ones, 0.3.4, 0.3.7 and 0.3.8, install only from source; the deck did not run those. "
        "Between pytesseract 0.3.9, 0.3.10 and 0.3.13 the only change the research found in one program was the type of the confidence, a str in 0.3.9 and an int from 0.3.10. "
        "The Windows and macOS installers of Tesseract, Homebrew, and the final release of Python 3.15 were never used here; the research ran Python 3.15 only as a beta, 3.15.0b4.",
        "A pinned release that predates your Python may not import.", notexec=True, recorded=True)

# ---- 8 how pytesseract talks to Tesseract -----------------------------------------------------------------------------------
pn = "errorsCut_v1_0_0.py"
dg, dcap = diagram("ProgramTalkingToTesseract", "sequence", (0.5, 1.35, 4.3, 3.25), fs=8, head_w=1.1, gap0=0.0)
p8, bot8, a8, b8, x8, w8 = pfit(pn, 4.9, 1.55, 4.6, 2.6, a=body(pn), b=len(PROGS[pn]["code"].rstrip("\n").split("\n")) - 1)
fh8 = foot(hid(pn, a8, b8, "imports, helpers and the folder", "the saving of the picture"), x8, round(bot8 + 0.04, 2), w8, fs=8)
im8, ib8, _ = img("readsLine.png", x8, round(fh8["y"] + fh8["h"] + 0.04, 2), 2.0, 0.3)
content("How pytesseract talks to Tesseract", "The wrapper starts the program, waits, and turns what it prints into a str or an error",
        [dg, dcap, p8, fh8, im8, imgcap(["readsLine.png"], round(x8 + im8["w"] + 0.1, 2), round(fh8["y"] + fh8["h"] + 0.04, 2), round(9.5 - x8 - im8["w"] - 0.1, 2), fs=8)],
        "The sequence diagram is the whole story of one call. The program calls image_to_string() with an image; pytesseract saves the image to a temporary file and starts the tesseract program with it; tesseract prints the text it recognised; pytesseract returns it as a str. "
        "The second half of the diagram is what happens with a language the engine does not have: tesseract reports an error opening the data file, and pytesseract raises TesseractError. "
        "The program on the right makes the line of text in the picture beside it with Pillow and runs the calls for real: the result is the line and a newline; lang='xyz' raises TesseractError and the message names xyz.traineddata; timeout=0.001 raises RuntimeError with the text Tesseract process timeout; "
        "an object that is not an image, bytes here, raises TypeError with Unsupported image object; and with tesseract_cmd pointed at a program that is not there the call raises TesseractNotFoundError. "
        "That last line is the error a reader gets after installing only the Python package, which is why the chapter makes the engine a separate installation. "
        "The corpus program pytesseractInternals_v1_0_0.py ran too and is not shown, because its lines are wider than a slide: it follows the wrapper's own source and the command line it builds.",
        "A wrapper is only as good as the program it starts.")

# ---- 9 words, boxes and confidence ------------------------------------------------------------------------------------------
pn = "wordsCut_v1_0_0.py"
a9 = body(pn) + 1
b9 = span(pn, "print('mean'")[0]
p9, bot9, a9, b9, x9, w9 = pfit(pn, 0.5, 1.55, 6.0, 2.9, a=a9, b=b9)
xr = round(0.5 + w9 + 0.2, 2)
im9, ib9, _ = img("wordBoxes.png", xr, 1.5, round(9.5 - xr, 2), 2.0)
content("Words, boxes and a confidence", "image_to_data() returns one row for every page, block, line and word",
        [p9, im9, imgcap(["wordBoxes.png"], xr, round(ib9 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         foot("Green boxes have a confidence of 90 or more, red boxes less: 43, In, open and the semicolon.", xr, round(ib9 + 0.3, 2), round(9.5 - xr, 2), fs=9),
         foot(hid(pn, a9, b9, "imports, helpers, the folder, the download check and the opening of the picture", "the drawing of the boxes"), 0.5, round(bot9 + 0.05, 2), w9, fs=8.5)],
        "image_to_data() with output_type=Output.DICT returns a dictionary of lists, one entry for each row of the table that Tesseract builds: 129 rows for frankenstein.png, of which 106 hold a word. "
        "The levels are 1 for the page, 2 for a block, 3 for a paragraph, 4 for a line and 5 for a word; the rows above the word level have the confidence -1, and each word row has its text, a confidence from 0 to 100, and the left, top, width and height of its box in pixels. "
        "The first words are In at (93, 278) with a confidence of 55, was with 96 and on with 96. The mean confidence of the 106 words is 94.55, and four words are below 90: 43 with 85, In with 55, open with 81 and the semicolon with 81. "
        "The picture is the page with every box drawn by the program, green for 90 and above and red below; the one wrong word of the first line, In for IT, is the lowest of all. "
        "In pytesseract 0.3.13 the confidence is an int; the research found it is a str in 0.3.9. The boxes are in the pixels of the picture that was read, so the same call on an enlarged copy returns boxes in the pixels of the copy. "
        "The mean of 94.55 and the list below 90 are MEASURED single runs with the Tesseract version named on the slide, 5.3.4.",
        "A confidence points at the words worth a second look.")

# ---- 10 what hurts ---------------------------------------------------------------------------------------------------------------
pn = "hurtsCut_v1_0_0.py"
a10 = body(pn) + 1
b10 = span(pn, "print('invert off")[0]
p10, bot10, a10, b10, x10, w10 = pfit(pn, 0.5, 1.55, 5.0, 3.4, a=a10 - 1, b=b10)
xr = round(0.5 + w10 + 0.2, 2)
ch10 = EX["_charts"]["cerBySize"]
chart10 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.4, "w": round(9.5 - xr, 2), "h": 1.35, "labels": ch10["labels"],
           "title": "Error rate by letter size", "series": [{"name": "error rate", "data": ch10["values"]}], "dataLabels": True, "dlFs": 8}
im10, ib10, _ = img("hurts.png", xr, 2.8, round(9.5 - xr, 2), 1.25)
content("What hurts: size, tilt and noise", "Characters wrong per character printed, on a drawn page of known text; 0.0 is perfect",
        [p10, chart10, im10, imgcap(["hurts.png"], xr, round(ib10 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         foot("MEASURED single runs, Tesseract %s, one 900-pixel page. " % TESS.split()[-1] + hid(pn, a10, b10, "imports, the page maker and the folder", "the sheet of four pages"), xr, round(ib10 + 0.28, 2), round(9.5 - xr, 2), fs=8)],
        "The program draws a page of 259 known characters with Pillow, reads it with Tesseract 5.3.4 and prints the character error rate, which is the edit distance between the known text and the result divided by the length of the known text, with every run of white space made one space. "
        "Every number is a MEASURED single run, one page, one font, one engine, and not a law. Letters of 6 pixels read at 1.0, which is nothing right; 8 pixels at 0.2394; 10 pixels at 0.0232; 12 pixels at 0.0154; and 24 pixels at 0.0116, which is the floor of this page, one wrong character in the whole text. "
        "A page turned by 2 degrees read at 0.0116, by 3 degrees at 0.6409, and by 5 degrees at 0.5328, so a slight tilt is harmless and a few degrees more is not. Noise of standard deviation 40 read at 0.0116 and of 60 at 1.0. "
        "White text on a black ground read at 0.0116, which is as good as black on white, because the engine inverts a light-on-dark page by itself (tessedit_do_invert is 1); with that turned off the result is 1.1042, more wrong characters than the text has. "
        "So the chapter's advice, dark text on a light ground, describes what the engine did not need here. The numbers in the research package (F9 and F10) were measured on a 700-pixel page and differ in size, for example 0.2278 at 8 pixels there and 0.2394 here; the pattern is the same, and the deck prints the numbers its own program printed. "
        "The corpus program whatHurtsAccuracy_v1_0_0.py ran too and is not shown. Ray Kurzweil's machine of 1976 was built because fonts mattered less than size: " + STORY["Kurzweil1976"]["lesson"] + ".",
        "Size, tilt and noise matter; the engine inverts a dark page itself.")

# ---- 11 cleaning a page --------------------------------------------------------------------------------------------------------------
pn = "cleanCut_v1_0_0.py"
dg, dcap = diagram("CleaningAPageBeforeReadingIt", "activity", (0.5, 1.4, 3.55, 3.0),
                   grid={"grey": (0, 0), "small": (0, 1), "up": (1, 1), "skew": (0, 2), "turn": (1, 2), "border": (0, 3), "read": (0, 4)},
                   cols=[(0.05, 1.65), (2.1, 1.45)], rows_n=5, starts=(1, 0), ends={"type": "dot", "col": 1, "row": 4},
                   routes={("start", "grey"): "h", ("small", "up"): "h", ("small", "skew"): "v", ("up", "skew"): "vh", ("skew", "turn"): "h",
                           ("skew", "border"): "v", ("turn", "border"): "vh", ("read", "end"): "h"}, fs=8, nh=0.4, dh=0.5)
p11, bot11, a11, b11, x11, w11 = pfit(pn, 4.1, 1.55, 5.4, 2.7, a=body(pn) + 1, b=span(pn, "print('with a 10 px border")[0])
im11, ib11, _ = img("cleaned.png", x11, round(bot11 + 0.05, 2), 2.6, 0.5)
content("Cleaning a page before reading it", "Enlarge small text, straighten a tilt, leave a white border; then read",
        [dg, dcap, p11, im11, imgcap(["cleaned.png"], round(x11 + im11["w"] + 0.1, 2), round(bot11 + 0.05, 2), round(9.5 - x11 - im11["w"] - 0.1, 2), fs=8),
         foot("MEASURED single runs, Tesseract %s. " % TESS.split()[-1] + hid(pn, a11, b11, "imports, the page maker and the folder", "the sheet that is saved"), x11, round(ib11 + 0.05, 2), w11, fs=8)],
        "The flow chart is the preparation the chapter recommends: convert the picture to grey, enlarge it if the text is smaller than about 10 pixels, straighten it if the page is turned by a few degrees, put a white border around the text, then read it and measure the error rate. "
        "The program shows three of the steps for real. A 9-pixel page reads at 0.0579; enlarged 2 times with LANCZOS it reads at 0.0154; and when the engine is told with --dpi 300 that a 9-pixel page is a 300 dpi scan, the result is 0.7452, a lot worse, because the dpi changes the size the engine expects the letters to have, so a wrong dpi is worse than none. "
        "The border is the surprise: a line of text cropped tight to its letters, 297 by 18 pixels, came back as tesseract reaas Ttnis line, and the same line with a 10-pixel white border, 317 by 38 pixels, as Tesseract reads this line. The picture shows the three versions of the page, the 9-pixel original, the enlarged copy and the framed line. "
        "These are MEASURED single runs with Tesseract 5.3.4 on pages the program draws; the research package gives 0.0579 and 0.0154 for the same pair, and the same tight crop and border. "
        "The chapter's link for more on preprocessing, autbor.com/preprocessingocr, answered 301 and then 200 and says on the page that it is a placeholder, so the advice has to come from the Tesseract documentation page on improving the quality of the output, which is on the resources slide.",
        "Enlarge the small, frame the tight, and never guess the dpi.")

# ---- 12 straightening and denoising ------------------------------------------------------------------------------------------------
pn = "cvCut_v1_0_0.py"
a12 = body(pn)
p12, bot12, a12, b12, x12, w12 = pfit(pn, 0.5, 1.55, 5.3, 3.3, a=a12, b=span(pn, "print('then Otsu")[0])
xr = round(0.5 + w12 + 0.2, 2)
im12, ib12, _ = img("cleanCv.png", xr, 1.5, round(9.5 - xr, 2), 1.9)
content("Straightening and denoising with OpenCV", "minAreaRect finds the angle; a median filter then Otsu removes the noise",
        [p12, im12, imgcap(["cleanCv.png"], xr, round(ib12 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         card("Recorded 13 Oct 2026", "The research measured Otsu on a noisy page as worse, 0.0154 to 0.0347; here the median filter comes first, and the order matters.",
              xr, round(ib12 + 0.4, 2), round(9.5 - xr, 2), 1.3, fs=9, accent="orange"),
         foot("MEASURED single runs, Tesseract %s. " % TESS.split()[-1] + hid(pn, a12, b12, "imports, the page maker and the folder", "the sheet that is saved"), 0.5, round(bot12 + 0.04, 2), w12, fs=8.5)],
        "OpenCV is a library for images that the chapter's preprocessing advice points to. The program turns a drawn page by 6 degrees, finds the dark pixels with findNonZero, and asks minAreaRect for the angle of the smallest rectangle round them: -6.0. "
        "Reading the turned page gives 0.6757; turning it back by 6 degrees with Pillow's rotate gives 0.0116, the floor of this page. The second half takes the page with noise of standard deviation 60, which read at 1.0, nothing right. "
        "A median filter of size 3 brings it to 0.0193, and an Otsu threshold after the filter, which picks the cut between dark and light from the histogram, to 0.0116. The picture shows four of the pages: turned, turned back, noisy and filtered. "
        "All four numbers are MEASURED single runs with Tesseract 5.3.4 on a 900-pixel page that the program draws. The card is the research's record, which the deck does not run again: on its 700-pixel noisy page an Otsu threshold alone raised the error rate from 0.0154 to 0.0347, "
        "so a threshold is not always a help, and the deck's order, filter first and threshold second, is the one that was measured to work on this page. "
        "The corpus program preprocessingWithOpenCV_v1_0_0.py ran too and is not shown. The book's own preprocess_ocr.py, 190 lines in the online materials, calls FileNotFileError, grayscale_image and open_image, which it never defines, and ends with NameError, so the program on this slide is not that file.",
        "Find the angle, turn back, filter, then threshold.", recorded=True)

# ---- 13 segmentation, whitelist, timeout ------------------------------------------------------------------------------------------------
pn = "psmCut_v1_0_0.py"
p13, bot13, a13, b13, x13, w13 = pfit(pn, 0.5, 1.55, 6.3, 3.0, a=span(pn, "print('two columns")[0], b=span(pn, "print('modes listed")[0])
xr = round(0.5 + w13 + 0.2, 2)
im13, ib13, _ = img("columns.png", xr, 1.5, round(9.5 - xr, 2), 1.5)
content("Segmentation modes, whitelist and timeout", "--psm tells Tesseract what the page is; a whitelist limits the characters it returns",
        [p13, im13, imgcap(["columns.png"], xr, round(ib13 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         card("Left out of the chapter", "The chapter uses none of the words psm, dpi, whitelist or timeout. Each changed the result here.",
              xr, round(ib13 + 0.42, 2), round(9.5 - xr, 2), 1.4, fs=9, accent="slate"),
         foot("MEASURED single runs, Tesseract %s. " % TESS.split()[-1] + hid(pn, a13, b13, "imports, helpers, the folder and the page of two columns", "the saving of the picture"), 0.5, round(bot13 + 0.04, 2), w13, fs=8.5)],
        "A page segmentation mode, --psm, says what kind of page Tesseract is looking at, and tesseract --help-psm lists 14 modes; the default reads a page of unknown layout. "
        "The program draws two columns of text only 4 pixels apart and reads them with the default mode: 0.2577, because lines of the two columns run together. Cut out the left column and read it with --psm 6, a single block of text, and the result is 0.0, no wrong character. "
        "The second half reads a one-line image, Order 4417-B shipped on 2026-10-13: the default and --psm 7 both return the whole line; a character whitelist, -c tessedit_char_whitelist=0123456789-, returns 4417-02026-10-13, "
        "in which the letter B was forced into a digit, the zero of the word on, and the spaces vanished, so a whitelist is a tool for fields that hold only digits and not for a line with words. "
        "timeout=0.001 raises RuntimeError with Tesseract process timeout, which is how a program stops a call that never finishes. All of these are MEASURED single runs with Tesseract 5.3.4. "
        "The research measured a six-line page with --psm 3, 4, 6 and 11 at 0.0116 and with --psm 7 and 13 at 0.9923 and 0.9961, so a single-line mode on a page of lines is the wrong tool; the deck did not run that again. "
        "The corpus program segmentationModes_v1_0_0.py ran too and is not shown, because its lines are wider than a slide.",
        "Tell the engine what the page is; limit what it may return.")

# ---- 14 hyphens and look-alikes ------------------------------------------------------------------------------------------------------------
pn = "hyphenCut_v1_0_0.py"
p14, bot14, a14, b14, x14, w14 = pfit(pn, 0.5, 1.55, 6.0, 2.6, a=span(pn, "broken = ")[0], b=span(pn, "o = norm(")[0])
im14, ib14, _ = img("hyphen.png", 0.5, round(bot14 + 0.05, 2), w14, 0.4)
xr = round(0.5 + w14 + 0.2, 2)
content("Hyphens, spaces and look-alike digits", "A hyphen at a line end stays in the text; 9-pixel digits turn 1 into 2 and 0 into o",
        [p14, im14, imgcap(["hyphen.png"], 0.5, round(ib14 + 0.02, 2), w14, fs=8),
         card("Join with a word list", "undo() joins the two halves only if the joined word is in the word list; the naive way turns well-known into wellknown.",
              xr, 1.5, round(9.5 - xr, 2), 1.45, fs=9.5, accent="slate"),
         foot(hid(pn, a14, b14, "imports, helpers, the folder, the download check, the OCR of the page, the word list /usr/share/dict/words of this machine and undo(t, strict)", "the saving of the picture"),
              xr, 3.05, round(9.5 - xr, 2), fs=8)],
        "ocr-example.png gave 51 lines, and 7 words are hyphenated at a line end in the result: dig-ital, pro-grams, compre-hend, pro-grams, straight-forward, pro-gramming and graph-ics. "
        "Tesseract returns the text as printed, so a program that wants whole words has to join them. The naive way, removing every hyphen at a line end, turns the real compound well-known into wellknown, as the program shows with a two-line sample; "
        "the strict way joins the two halves only if the joined word is in a word list, and leaves well-known alone, but it also leaves a real word that the list does not hold. "
        "The word list here is /usr/share/dict/words of this machine, so the output of the strict undo depends on that file, which a reader's machine may not have. "
        "The second half of the program reads a drawn line, Invoice 1058 Total 1,000.00 Order O8l0, at two sizes with --psm 7: at 12 pixels it returned the line exactly, and at 9 pixels Invoice 2058 Tetl 2,000.00 Order o810, at 0.1579, "
        "so 1 became 2, the word Total became Tetl, and the letter O of the order became a small o. Digits that look like letters, and letters that look like digits, are the mistakes a spell checker cannot find in an order number. "
        "These numbers are MEASURED single runs with Tesseract 5.3.4. The research found the same 7 hyphens. The corpus program hyphensAndDigits_v1_0_0.py ran too and is not shown.",
        "Join hyphenated words only with a word list.")

# ---- 15 mistakes a spell checker cannot see -------------------------------------------------------------------------------------------------------
pn = "confCut_v1_0_0.py"
p15, bot15, a15, b15, x15, w15 = pfit(pn, 0.5, 1.55, 6.2, 2.4, a=body(pn) + 1, b=span(pn, "print('lowest confidence")[0])
xr = round(0.5 + w15 + 0.2, 2)
im15, ib15, _ = img("lowWord.png", xr, 1.5, round(9.5 - xr, 2), 0.95)
content("Mistakes a spell checker cannot see", "In and Motion are real words, so only the confidence points at them",
        [p15, im15, imgcap(["lowWord.png"], xr, round(ib15 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         card("NOT EXECUTED here", "The chapter's step that sends the text to a large language model to fix the mistakes was never run. Its sample prompt has 419 characters.",
              xr, round(ib15 + 0.4, 2), round(9.5 - xr, 2), 1.45, fs=9, accent="orange"),
         foot(hid(pn, a15, b15, "imports, helpers, the folder, the download check and the data call", "the cut of the picture"), 0.5, round(bot15 + 0.04, 2), w15, fs=8.5),
         factrow("Recaptcha2009", y=4.58)],
        story_notes("Recaptcha2009") + " The two wrong words of the 106 on Figure 22-1 are IT read as In and motion read as Motion. Both are real English words, so a spell check against the 104,334 words of /usr/share/dict/words flags nothing; the program prints an empty list. "
        "The mean confidence is 94.55, and the wrong In has the lowest of all, 55, while Motion has 92, so the low confidence finds one of the two. The picture is the word In enlarged three times with its neighbours, an I followed by a small capital T. "
        "The chapter's last step is to give the text to a large language model with a prompt that asks it to fix the mistakes. The research did not run it: no model was called, and the sample prompt in the chapter has 419 characters. "
        "What the deck can say is what a program could hand to a model or to a person: the words with a low confidence, and the words a word list does not know. Both lists are short here, which is the point of reCAPTCHA's design, that people are asked only about the words the machine could not read. "
        "The deck makes no statement about how well a model would correct the text. The numbers are MEASURED single runs with Tesseract 5.3.4.",
        "Real-word mistakes need a confidence or a human, not a spell check.", notexec=True)

# ---- 16 other languages -----------------------------------------------------------------------------------------------------------------------------------
pn = "langCut_v1_0_0.py"
p16, bot16, a16, b16, x16, w16 = pfit(pn, 0.5, 1.55, 6.2, 3.35, a=body(pn), b=span(pn, "print('mixed line")[0])
xr = round(0.5 + w16 + 0.2, 2)
im16, ib16, _ = img("japanese.png", xr, 1.5, round(9.5 - xr, 2), 1.0)
content("Other languages: Japanese and mixed lines", "lang='jpn' reads the Japanese page; lang='eng' returns gibberish; 'eng+jpn' reads both",
        [p16, im16, imgcap(["japanese.png"], xr, round(ib16 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         foot("The picture is the top of frankenstein_jpn.png, Figure 22-2 of the book. The book prints 第 5 剖 and 芝鬱; this engine returns 第 5 剖 and 愛鬱.", xr, round(ib16 + 0.35, 2), round(9.5 - xr, 2), fs=9),
         foot(hid(pn, a16, b16, "imports, helpers, the folder and the download check", "the cut of the picture"), xr, round(ib16 + 1.05, 2), round(9.5 - xr, 2), fs=8.5)],
        "The Japanese page of the book, frankenstein_jpn.png, is 1211 by 606 pixels with 13 lines. With lang='jpn' Tesseract 5.3.4 returned 13 non-empty lines, and the first begins 第 5 剖 私が自分の労; the picture shows the heading 第 5 章 and the word 憂鬱. "
        "The research compared that with the text the book prints and found two characters different, in this engine 愛鬱 where the book has 芝鬱, and the fast data under Tesseract 5.5.3 equalled the book, while the best data returned 901 characters against 538, which is not a better answer but a longer one. "
        "With lang='eng' the same picture gave gibberish and not one Japanese character: the program counts 0 characters above U+2E80. The mixed line The cat is 猫 and the dog is 犬 today, drawn with a Japanese font, read at 0.0571 with eng, where the two characters came back as 4 and %, and at 0.0 with jpn and with eng+jpn. "
        "So a language string is a request for data files, joined with a plus sign, and the pack for the script must be installed; get_languages() lists what is installed here, deu, eng, fra, jpn, osd, rus and tur, which is why the chapter's printed list of two languages differs. "
        "These numbers are MEASURED single runs with Tesseract 5.3.4 and the fast data. The corpus program languagesAndPacks_v1_0_0.py ran too and is not shown, because its lines are wider than a slide.",
        "Install the pack for the script, and name it in lang.")

# ---- 17 language codes and data files -----------------------------------------------------------------------------------------------------------------------
pn = "packsCut_v1_0_0.py"
p17, bot17, a17, b17, x17, w17 = pfit(pn, 0.5, 1.55, 6.2, 3.3, a=span(pn, "def read(")[0], b=span(pn, "print('together")[0])
xr = round(0.5 + w17 + 0.2, 2)
ch17 = EX["_charts"]["dataBytes"]
chart17 = {"t": "chart", "ctype": "bar", "x": xr, "y": 1.4, "w": round(9.5 - xr, 2), "h": 1.75, "labels": ch17["labels"],
           "title": "eng.traineddata, megabytes", "series": [{"name": "MB", "data": ch17["values"]}], "dataLabels": True, "dlFs": 9}
im17, ib17, _ = img("germanLine.png", xr, 3.2, round(9.5 - xr, 2), 0.5)
content("Language codes and data files", "The code is the name of a file; 126 packs, 13 names are not three letters",
        [p17, chart17, im17, imgcap(["germanLine.png"], xr, round(ib17 + 0.02, 2), round(9.5 - xr, 2), fs=8),
         foot(hid(pn, a17, b17, "imports, the page maker and the folder", "the sizes and the saving of the picture"), 0.5, round(bot17 + 0.04, 2), w17, fs=8.5)],
        "A language string is the name of a file in the data folder: lang='deu' opens deu.traineddata. The chapter calls the strings ISO 639-3 codes while the Tesseract manual page says ISO 639-2, and German shows the difference: lang='deu' read the drawn line Die Größe der Straße exactly, "
        "lang='ger', the bibliographic code of German in ISO 639-2, raises TesseractError, and lang='German' raises the same error. A pack that is missing inside a combination raises nothing: 'eng+xyz' returned Die GrdBe der Strake, the English pack's reading of the umlaut and the sharp s. "
        "The full fast set that the research downloaded, tessdata_fast, has 126 packs and 362 MB of language files (706,776,225 bytes with the 37 script models, where the chapter says all languages add about 600MB); 13 of the 126 names are not three letters, for example chi_sim, chi_sim_vert and aze_cyrl; osd, the orientation data, is in the list although it is no language, and so is equ, the equation pack. "
        "The chart is the size of eng.traineddata in the three data sets, read from the files: 4,113,088 bytes in tessdata_fast, 15,400,601 in tessdata_best and 23,466,654 in the legacy set, each equal to the file its GitHub repository served on 13 October 2026; the apt package holds the fast one. "
        "The program prints those bytes; the chart is recomputed from the files by the deck check. The corpus program languagesAndPacks_v1_0_0.py ran too and is not shown.",
        "A language code is a file name, and the wrong code raises an error.")

# ---- 18 three engines and three kinds of data ---------------------------------------------------------------------------------------------------------------------
tbl18 = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [1.5, 2.5, 2.5, 2.5], "fs": 9, "rowH": 0.3, "rows": EX["_tables"]["engines"]["rows"]}
content("Three Tesseracts, three kinds of data", "The same page: the first word and the error rate, each a MEASURED single run",
        [tbl18,
         card("Fast, best, legacy", "Each cell is the first word that engine returned and its error rate against the printed page. The apt package has the fast data; the best data is 3.7 times larger and the legacy set 5.7 times.",
              0.5, 3.05, 4.4, 1.35, fs=9.5, accent="slate"),
         card("Built from source", "Tesseract 4.1.1 and 5.5.3 were built here with their own configure; 5.3.4 is the Ubuntu package. NAPS2 brings a 5.5.0 of its own.",
              5.1, 3.05, 4.4, 1.35, fs=9.5, accent="orange"),
         factrow("Tesseract1985", y=4.58)],
        story_notes("Tesseract1985") + " The table is computed when the deck is checked: three Tesseract programs, 4.1.1, 5.3.4 and 5.5.3, are run on frankenstein.png with three data sets, the fast and best sets of the LSTM models and the legacy set, which holds both the old engine and the new one, and each cell is the first word of the result and the error rate against the printed page. "
        "The research recorded the same pattern: the first word was Iv with 4.1.1 and with 5.5.3 and the fast data, In with 5.3.4, Ir with the best data and It with the legacy data under 4.1.1 and 5.5.3; the error rate was 0.0035 with the fast data and 0.0017 with the best and the legacy data. "
        "So more data is not always a different answer, but the answer depends on the data. eng.traineddata is 4,113,088 bytes in tessdata_fast, 15,400,601 in tessdata_best and 23,466,654 in tessdata, and the chapter does not say which one its install gets. "
        "The statements of the chapter replayed in six configurations of engine and data: 18 of 22 matched the book with the apt 5.3.4, 20 with 5.5.3 and the fast data, 18 with 5.5.3 and the best data, 20 with 4.1.1 and the fast data, 19 with all the apt languages and 21 with all languages under 5.5.3. "
        "The corpus program enginesAndData_v1_0_0.py ran too and is not shown. Every cell is a MEASURED single run with the engine named in its row.",
        "The answer depends on the engine and on the data it was given.")

# ---- 19 a searchable PDF with NAPS2 --------------------------------------------------------------------------------------------------------------------------------
pn = "naps2Cut_v1_0_0.py"
dg, dcap = diagram("MakingASearchablePdfWithNaps2", "activity", (0.5, 1.4, 4.1, 2.75),
                   grid={"build": (0, 0), "run": (0, 1), "found": (0, 2), "fail": (1, 2), "exists": (0, 3), "refuse": (1, 3), "pdf": (0, 4)},
                   cols=[(0.0, 2.05), (2.5, 1.15)], rows_n=5, starts=(1, 0), ends={"type": "bar", "x": 3.95, "row": 2, "row2": 4},
                   routes={("start", "build"): "h", ("found", "fail"): "h", ("found", "exists"): "v", ("fail", "end"): "h", ("exists", "refuse"): "h",
                           ("exists", "pdf"): "v", ("refuse", "run"): "loopR", ("pdf", "end"): "h"}, fs=8, nh=0.44, dh=0.42)
p19, bot19, a19, b19, x19, w19 = pfit(pn, 4.7, 1.55, 4.8, 3.1, a=span(pn, "args = ")[0], b=len(PROGS[pn]["code"].rstrip("\n").split("\n")), right=True)
content("A searchable PDF with NAPS2", "NAPS2 console reads the image with its own OCR and writes a PDF with the text under it",
        [dg, dcap, p19,
         foot("NOT EXECUTED here: the Windows and macOS installers, the Flatpak of NAPS2 and a scanner. Their paths raise FileNotFoundError.",
              0.5, round(dcap["y"] + dcap["h"] + 0.05, 2), 4.1, fs=8.5),
         foot(hid(pn, a19, b19, "imports, helpers, the folder and the download check"), x19, round(bot19 + 0.05, 2), w19, fs=8.5)],
        "NAPS2, Not Another PDF Scanner 2, is a scanning application whose console version the chapter runs from Python with subprocess. The flow chart is the call: build the arguments, naming the input image, the output PDF and the OCR language; run naps2 console; "
        "if the program is not found, subprocess.run() raises FileNotFoundError; if the output file already exists and -f is missing, NAPS2 refuses, so add -f; otherwise read the text of the PDF. "
        "The program runs the chapter's call for real with NAPS2 8.5.1 from its .deb package, which carries its own Tesseract 5.5.0: the Windows path C:\\Program Files\\NAPS2\\NAPS2.Console.exe and the Flatpak command both raise FileNotFoundError on this Linux machine, "
        "naps2 console returned 0, its stdout is bytes, its last line is Successfully saved PDF file to output.pdf, and pdfinfo and pdftotext of the poppler tools show 1 page with 579 characters of text and an error rate of 0.0035 against the printed page, a MEASURED single run with Tesseract 5.5.0 inside NAPS2. "
        "The chapter's arguments include --install ocr-eng, which asks NAPS2 to install the English OCR data. The Windows and macOS installers, the Flatpak and a flatbed scanner were never used here, so how the application is installed there, and scanning from a device, are read and not run. "
        "The corpus program naps2Pdf_v1_0_0.py ran too and is not shown, because its lines are wider than a slide. " + STORY["Goldberg1931"]["lesson"] + ", which is the whole idea of the PDF: " + STORY["Goldberg1931"]["story"],
        "A scan becomes searchable when text is put under the picture.", notexec=True)

# ---- 20 overwriting and picking pages in NAPS2 ---------------------------------------------------------------------------------------------------------------------------
pn = "overwriteCut_v1_0_0.py"
dg, dcap = diagram("AskingNaps2ToOverwriteAFile", "sequence", (0.5, 1.4, 3.3, 2.5), fs=8, head_w=1.1)
p20, bot20, a20, b20, x20, w20 = pfit(pn, 4.0, 1.55, 5.5, 2.8, a=span(pn, "base = [")[0], b=span(pn, "print('-i', spec")[0], right=True)
im20, ib20, _ = img("pagesPicked.png", 0.5, round(dcap["y"] + dcap["h"] + 0.06, 2), 3.3, 0.45)
content("Overwriting and picking pages in NAPS2", "Without -f NAPS2 says the file exists and still returns 0; [0:2] picks pages 0 and 1",
        [dg, dcap, p20, im20, imgcap(["pagesPicked.png"], 0.5, round(ib20 + 0.02, 2), 3.3, fs=8),
         foot(hid(pn, a20, b20, "imports, helpers, the folder, the download check, the maker of spam.pdf with seven pages and the helper pages(spec), which runs NAPS2 with the slice and returns the text of each page", "the sheet of seven pages and the saving of the picture"),
              x20, round(bot20 + 0.05, 2), w20, fs=8.5)],
        "The sequence diagram is one detail that costs a student an hour: run naps2 console with -f and the file is written and the return code is 0; run it without -f and NAPS2 prints File already exists. Use --force to overwrite. and still returns 0, so a program that checks only the return code believes it worked and finds the old file; run it again with -f and the file is written again. "
        "The program asks for exactly those three calls and prints the last line NAPS2 wrote each time. The second half makes a PDF of seven pages that read spam0 to spam6 and asks for pages with the chapter's slices: spam.pdf[0:2] gave the pages Spam0 and Spam1, spam.pdf[-2:] gave Spam5 and Spam6, and spam.pdf[1:6:2] gave Spam1, Spam3 and Spam5. "
        "The text of the pages is what the OCR inside NAPS2 read, and two of the pages were read with a stray character, Spam0O, Spam1l and Spamo6 in this run, so the text of a result is a MEASURED single run and not a given; the page that was picked is what the slices decide. "
        "One page of an earlier run of the same program came back empty on its first call and read correctly on three runs after it, a flake of the OCR inside NAPS2 that the deck cannot explain, which is why the program prints the read text and the deck check compares it again each time. "
        "The picture shows the seven pages with the three picked by the last slice in red. The Windows, macOS and Flatpak forms of the command were never used here.",
        "Without -f NAPS2 refuses and still says success.")

# ---- 21 other routes to a searchable PDF ---------------------------------------------------------------------------------------------------------------------------------
pn = "pdfCut_v1_0_0.py"
dg, dcap = diagram("TheLifeOfAScannedPage", "lifecycle_side", (0.5, 1.4, 4.7, 3.15), side="pdf", side_after="cleaned", fs=8, sw=1.0, sh=0.44, sfs=8.5, top=0.3, lab_w=1.0, margin=1.1, side_w=1.3)
p21, bot21, a21, b21, x21, w21 = pfit(pn, 5.28, 1.55, 4.22, 3.4, a=span(pn, "img = ")[0], b=len(PROGS[pn]["code"].rstrip("\n").split("\n")), right=True)
content("Three more routes to a searchable PDF", "Pillow makes a PDF with no text; pytesseract and ocrmypdf put the text in",
        [dg, dcap, p21,
         foot(hid(pn, a21, b21, "imports, helpers"), x21, round(bot21 + 0.04, 2), w21, fs=8)],
        "The state diagram follows one scanned page: an image file is opened as an Image object, optionally cleaned, read into a string, and the string may be fixed, or the cleaned image becomes a searchable PDF. "
        "The program takes the third route three ways. A PDF that Pillow saves from frankenstein.png holds 0 characters of text, because Pillow only embeds the picture. The PDF of image_to_pdf_or_hocr() is bytes that begin %PDF-, holds 578 characters, and its text layer has 106 word boxes, one for each word of Figure 22-1. "
        "ocrmypdf 17.13.0, a tool that adds a text layer to a PDF, exited with 2 for a PNG with no resolution recorded in it, with 0 once told --image-dpi 150, and then the text was 578 characters again; for a PDF that already has text it exited with 6, and with --skip-text it exited with 0. "
        "The exit codes are what a script has to check, because the messages go to the error stream. The research measured the error rate of these PDFs at 0.0138 for the pytesseract one and 0.0035 for the ocrmypdf one, MEASURED single runs with Tesseract 5.3.4. "
        "The corpus program pdfRoutes_v1_0_0.py ran too and is not shown, because its lines are wider than a slide; ocrmypdf is a separate install, in its own virtual environment here.",
        "Check the exit code; a PDF made by Pillow has no text.")

# ---- 22 reading the screen ------------------------------------------------------------------------------------------------------------------------------------------------------
pn = "screenCut_v1_0_0.py"
a22 = span(pn, "disp = ")[0]
p22, bot22, a22, b22, x22, w22 = pfit(pn, 0.5, 1.55, 6.2, 3.35, a=span(pn, "code = ")[0], b=span(pn, "print('CER of the second")[0])
xr = round(0.5 + w22 + 0.2, 2)
im22, ib22, _ = img("screenShot.png", xr, 1.5, round(9.5 - xr, 2), 1.2)
content("Reading the screen", "PyAutoGUI takes a screenshot, Tesseract reads a crop of it, the text goes to a file",
        [p22, im22, imgcap(["screenShot.png"], xr, round(ib22 + 0.03, 2), round(9.5 - xr, 2), fs=8),
         *stack([SAY_VD,
                 "NOT EXECUTED here: a real screen with a real browser; the Browser Text Scraper was never run.",
                 hid(pn, a22, b22, "imports, helpers, the start of Xvfb and of the viewer", "the saving of the picture")],
                xr, round(ib22 + 0.33, 2), round(9.5 - xr, 2), fs=8, gap=0.05)],
        "The screen scraper of the chapter takes a screenshot with PyAutoGUI, crops it to the box where the text is, reads the crop with Tesseract and appends the text to output.txt. "
        "The program on the slide ran on a virtual X display, Xvfb, 1280 by 1024, with the real ImageMagick display program showing frankenstein.png in the corner, and the three calls ran in a child Python with DISPLAY set. "
        "The template's own crop, (400, 200, 1000, 800), is 600 by 600 pixels of a screen on which the page is 1130 by 672, so it cut out part of the page and the call appended only 361 characters; the whole window, (0, 0, 1130, 672), gave 581 characters, and running it a second time appended the same 581 again, 1523 characters in all, because the file is opened to append and a screenshot never clears it. "
        "The error rate of the whole window is 0.0035 against the printed page, a MEASURED single run with Tesseract 5.3.4. The red rectangle in the picture is the template's crop on the 640 by 512 miniature of the screen. "
        "The research recorded that without DISPLAY the import of PyAutoGUI raised KeyError: 'DISPLAY'. Nobody saw this screen: a virtual display is a local stand-in, and a real screen with a real browser, which the practice program needs, was never used. "
        "The corpus program ocrscreenOnXvfb_v1_0_0.py ran on the same virtual display and is not shown, because its lines are wider than a slide.",
        "A screenshot is just another image; the crop decides what is read.", notexec=True)

# ---- 23 the nine configurations -----------------------------------------------------------------------------------------------------------------------------------------------------------
tbl23 = {"t": "table", "x": 0.5, "y": 1.45, "w": 9.0, "colW": [0.9, 0.9, 1.15, 1.0, 2.9, 2.15], "fs": 8, "rowH": 0.24, "rows": EX["_tables"]["configurations"]["rows"]}
content("Nine configurations, 22 statements", "Recorded: how many printed statements of the chapter match the book, by environment",
        [tbl23,
         card("Recorded 13 Oct 2026", "One program of 19 items printed the same under 11 interpreters, 3.11.17 to 3.15.0b4, and 9 items the same under 14 Pillow releases, 9.5.0 to 12.3.0.",
              0.5, 3.82, 4.4, 1.15, fs=8.5, accent="slate"),
         card("NOT EXECUTED here", "Python 3.15 final, pytesseract 0.3.4, 0.3.7 and 0.3.8 (source only), a scanner, Windows and macOS.",
              5.1, 3.82, 4.4, 1.15, fs=8.5, accent="orange")],
        "The table is the research's record of the chapter's 22 statements replayed as printed in nine configurations, and the deck check computes every cell again from the record. "
        "With the newest packages on Python 3.14.6 the apt Tesseract 5.3.4 with the fast data matched the book in 18 of 22 statements, 5.5.3 with the fast data in 20, 5.5.3 with the best data in 18, 4.1.1 with the fast data in 20, 5.3.4 with all the apt languages in 19 and 5.5.3 with all languages in 21. "
        "With the book's pins, Pillow 10.4.0 and pytesseract 0.3.10, 18 matched on Python 3.13.14, 8 on Python 3.14.6 and none in an empty Python. The statements that differ are get_languages(), the first word Iv, the Japanese heading and the English gibberish. "
        "The research also ran one program of 19 items under 11 interpreters, Python 3.11.17 to 3.15.0b4, and 9 items under 14 Pillow releases, 9.5.0 to 12.3.0, and the outputs were the same; between pytesseract 0.3.9, 0.3.10 and 0.3.13 the confidence changed from a str to an int. "
        "What the research could not run is marked: Python 3.15 was a beta only, pytesseract 0.3.4, 0.3.7 and 0.3.8 install only from source and did not run, and there was no scanner, no Windows and no macOS. "
        "The photograph of the stories was not fetched either, because the single request to Wikimedia Commons answered 429.",
        "The same book gives 8 to 21 matching statements, by environment.", notexec=True, recorded=True)

# ---- 24 summary: the mind map --------------------------------------------------------------------------------------------------------------
dg, dcap = diagram("RecognizingTextInImagesAtAGlance", "mindmap", (0.5, 1.4, 9.0, 3.2), fs=9, root_w=2.0)
content("The chapter in one map", "Six branches; the slides of each branch hold the examples",
        [dg, dcap],
        "These six branches are the route of the deck. Installing the tools: pytesseract 0.3.10 stops on Python 3.14, the engine is a separate program and the data folder holds the languages. Reading an image: image_to_string() returns a str, the first word varies with the engine, and hyphens at line ends stay in the text. "
        "Accuracy and preprocessing: small text and skew raise the error rate, enlarging helps nine-pixel text, and --psm 7 reads a single line. Languages and data: the code is the data file name, the fast set holds 126 languages and the best data is larger than the fast data. "
        "Searchable PDFs: NAPS2 refuses to overwrite without -f, ocrmypdf needs a dpi for an image and Pillow makes a PDF with no text. The book and practice: the shipped script calls undefined names, the preprocessing link is a placeholder, and the screen scraper needs a display. "
        "Together they answer the first question of the chapter, what can be shown to work on a machine with no scanner and no screen and what can only be shown to fail, and the slides that say where a printed line differs answer the second. The map is drawn from the same specification as the interactive page.",
        "If a branch feels unproven, its slides hold the example.")

# ---- 25 resources ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PUB = {p[0]: p for p in RD.PUBS}
_read = [["The textbook, chapter 22 - free online", PUB["P01"][2]],
         ["Appendix A: installing third-party modules", PUB["P05"][2]],
         ["Online materials of the 3rd edition (zip)", PUB["P02"][2]]]
_ref = [["Tesseract: improving the quality of the output", PUB["P08"][2]],
        ["Tesseract: data files", PUB["P10"][2]],
        ["NAPS2 command line documentation", PUB["P22"][2]],
        ["OCRmyPDF documentation", PUB["P24"][2]]]
_hist = [["Optical character recognition (Wikipedia)", STORY["Goldberg1915"]["link"]],
         ["Tesseract (Wikipedia)", STORY["Tesseract1985"]["link"]],
         ["ReCAPTCHA (Wikipedia)", STORY["Recaptcha2009"]["link"]],
         ["Frankenstein (Wikipedia)", STORY["Frankenstein1831"]["link"]]]
LINKS = [r[1] for r in _read + _ref + _hist]
json.dump({"_version": __version__, "links": LINKS}, open(os.path.join(HERE, "links_v1_0_0.json"), "w"), indent=1)
content("Where to go from here", "Every link was opened on the day this deck was made",
        [{"t": "links", "x": 0.5, "y": 1.4, "w": 9.0, "h": 3.55, "fs": 9, "groups": [
            {"head": "Read", "rows": _read}, {"head": "Reference", "rows": _ref}, {"head": "Stories", "rows": _hist}]}],
        "Every link on this slide was opened on the day the deck was made, and the build records the status each answered. The textbook chapter is free to read online and holds every listing of the chapter; the online materials are the zip of 91 files that the programs of this deck download and check by SHA-256, and Appendix A is where the book pins pytesseract 0.3.10 and Pillow 10.4.0. "
        "The reference links are the Tesseract documentation on improving the quality of the output and on the data files, the NAPS2 command line documentation and the OCRmyPDF documentation. "
        "Four of the six stories of the chapter are on slides with their own link, on the slide itself: Hyman Goldberg's patent of 1915, Mary Shelley's Frankenstein of 1831, Hewlett-Packard's Tesseract of 1985 and reCAPTCHA of 2009, and their pages are the last group. "
        "The other two, Emanuel Goldberg's Statistical Machine of 1931 and Kurzweil's reading machine of 1976, are told in the notes, and their pages are in the research package. "
        "The rest of the fifty-three sources of the research, among them the Tesseract manual page, the PyPI metadata, the ISO 639 code tables and Ray Smith's overview of the engine, are in the research package. No photograph of a person is used in the deck.",
        "Textbook, documentation, and history, all opened today.")

# ---- 26 closing ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
content("What you should now be able to say", "Four claims, each carried by a result you saw printed",
        [{"t": "bullets", "x": 0.6, "y": 1.5, "w": 8.8, "h": 2.4, "fs": 15, "items": [
            "image_to_string() returns a str; the first word depends on the engine and its data.",
            "Small, tilted or noisy text raises the error rate; enlarge, straighten, filter, add a border.",
            "The language code is a file name; NAPS2 needs -f and a check of the result.",
            "Appendix A's pytesseract does not import on Python 3.14; nothing ran on Windows or macOS."]},
         {"t": "chips", "x": 0.6, "y": 4.1, "w": 8.8, "h": 0.6, "fs": 10, "big": False,
          "items": ["%d console rows" % ROWS_SHOWN, "%d programs run" % len(PROGS), "8 diagrams", "14 pictures"]}],
        "Four claims, each carried by a result you saw printed. If you can say them in your own words and run the examples yourself, you have the chapter. The programs need Pillow, pytesseract and the tesseract program, and some need NumPy, OpenCV, poppler, NAPS2, ocrmypdf and an X display; the console rows need pytesseract, Pillow and, for the pins, packaging. "
        "The rows were run again under Python 3.14.6 each time the deck was built, and the programs, and with them the fourteen pictures, were run again by the check that compares the slides with the recording. "
        "What was not run is marked on its slide: Windows and macOS, the Flatpak of NAPS2, a scanner, the large language model, a real screen, Python 3.15 final and the three pytesseract releases that install only from source. The licence of the book's scans was not checked. Nothing was ever shown to a person on a screen by the screen program. "
        "Every accuracy figure in this deck is a single measured run with the Tesseract version named, and not a benchmark. The next chapter of the book moves on, and what this chapter taught about checking what a program returns, and about reading a printed output with care, carries over.",
        "Questions are welcome; bring a picture to read.")

# ---- agenda ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
_t = {s["title"]: i + 1 for i, s in enumerate(S)}
_parts = [("Reading an image", "What a program can ask Tesseract for", "The same page, a different first word"),
          ("Installing, and what pytesseract does", "Appendix A's pins, run on Python 3.14", "Words, boxes and a confidence"),
          ("Accuracy and preparing an image", "What hurts: size, tilt and noise", "Mistakes a spell checker cannot see"),
          ("Languages, data files and engines", "Other languages: Japanese and mixed lines", "Three Tesseracts, three kinds of data"),
          ("Searchable PDFs, the screen and releases", "A searchable PDF with NAPS2", "Nine configurations, 22 statements"),
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
        {"n": "%d + %d" % (_nstory, 6 - _nstory), "label": "true stories: %d on slides, %d in the notes" % (_nstory, 6 - _nstory)},
        {"n": str(_npic), "label": "pictures, each saved by a program that is run again"}]}]
S[1]["sub"] = "Six parts; every range is a run of slides you can jump to"
S[1]["take"] = "Six parts, from four lines of code to a screenshot."
S[1]["notes"] = ("The route has six parts. It starts with reading an image: what a program can ask Tesseract for, the four lines of the chapter, and the same page read by different engines with a different first word. "
                 "Then the installation and what pytesseract does: the pins of Appendix A run on Python 3.14, how the wrapper talks to the engine, and the words, boxes and confidence of image_to_data(). The third part is accuracy and preparing an image: what hurts, cleaning a page, straightening and denoising with OpenCV, segmentation modes, hyphens and look-alike digits, and the mistakes a spell checker cannot see. "
                 "The fourth is languages, data files and engines. The fifth is searchable PDFs, the screen and the releases: NAPS2, its overwrite rule and page slices, the other routes to a PDF, reading the screen, and the nine configurations of the research. "
                 "The last part is a one-map summary and the resources. The ranges name the exact slides, so you can return to the part you need. Four of the six stories are on slides, each with a link, and two, Emanuel Goldberg's Statistical Machine and Kurzweil's reading machine, are told in the notes; the eight narrative diagrams of the chapter are drawn from the same specifications as the interactive page. "
                 "Every output was printed by Python %s with pytesseract 0.3.13, Pillow 12.3.0 and the Tesseract 5.3.4 of Ubuntu, the screen program ran on a virtual display, and what could not be run is marked on its slide." % PYV)

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
plan = {"meta": {"title": "Ch. 22: Recognizing Text", "sub": "SEN0414, third-edition redesign",
                 "version": __version__, "python": PYV, "total": len(S), "diagrams": SHOWN, "notExecuted": NOTEXEC, "recorded": RECORDED,
                 "standin": {str(k): v for k, v in STANDIN.items()}}, "slides": S}
if LATE:
    raise SystemExit("REFUSED:\n" + "\n".join(LATE))
out = os.path.join(HERE, "deck_plan_v1_0_0.json")
json.dump(plan, open(out, "w"), indent=1)
print("written", out, "-", len(S), "slides; diagrams on slides", dict(sorted(SHOWN.items(), key=lambda kv: kv[1])), "; NOT EXECUTED on slides", NOTEXEC, "; Recorded on slides", RECORDED)
